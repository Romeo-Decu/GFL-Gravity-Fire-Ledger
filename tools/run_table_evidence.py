#!/usr/bin/env python3
"""Evidence from NASA's run tables beside the conditions the record text leaves open (evidence-map amendment A6).

For each investigation and each condition slot that is not agreed by all extractors, if NASA's experimental table
has a matching column, list what that column holds. For oxygen and flow, where the values are numbers, a fixed
numeric reading is added; for fuel the material names are shown and not classified. This adds evidence beside the
map; it changes no verdict. Rules written on 2026-11-14 after the extractor disputes were seen (stated in the protocol).

    python tools/run_table_evidence.py --src "$FIF_DATA/psi_tables" --out data/derived/evidence_map/RUN_TABLE_EVIDENCE_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONC = re.compile(r"(%|percent|xo2|mole fraction|conc)", re.I)       # an oxygen concentration, not a mass flow
SPEED = re.compile(r"(cm/s|velocity|air flow|fan display)", re.I)      # a flow speed or its setting
NUM = re.compile(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def oxygen_reading(vals: list[float]) -> str:
    pct = [v * 100 if v <= 1 else v for v in vals]
    cls = {"reduced oxygen" if p < 20.5 else "air" if p <= 22.0 else "enriched oxygen" for p in pct}
    return cls.pop() if len(cls) == 1 else "varied"


def flow_reading(vals: list[float]) -> str:
    if all(v == 0 for v in vals):
        return "quiescent"
    return "forced flow" if all(v > 0 for v in vals) else "several"


def column_values(path: Path, header: str) -> list[str]:
    rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="replace", newline="")))
    head = [h.strip() for h in rows[0]]
    i = head.index(header)
    return [r[i].strip() for r in rows[1:] if i < len(r) and r[i].strip()]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--map", type=Path, default=ROOT / "data/derived/evidence_map/EVIDENCE_MAP_v2.json")
    ap.add_argument("--inventory", type=Path, default=ROOT / "data/derived/evidence_map/RUN_TABLE_INVENTORY_v1.json")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--page", type=Path)
    a = ap.parse_args(argv)
    emap, inv = json.loads(a.map.read_text(encoding="utf-8")), json.loads(a.inventory.read_text(encoding="utf-8"))
    out = {}
    for sid, e in inv["investigations"].items():
        for cls, slot in inv["slot_of"].items():
            s = emap["investigations"][sid]["slots"][slot]
            if s["status"] == "agreed" or cls not in e["recorded"]:
                continue
            cols = []
            for t in e["tables"]:
                p = a.src / t["name"]
                if hashlib.sha256(p.read_bytes()).hexdigest() != t["sha256"]:
                    raise SystemExit(f"{t['name']}: not the file in the manifest")
                for c in t["columns"]:
                    if cls not in c["classes"] or not c["filled"]:
                        continue
                    if cls == "oxygen" and (not CONC.search(c["header"]) or "final" in c["header"].lower()):
                        continue
                    if cls == "flow" and not SPEED.search(c["header"]):
                        continue
                    vals = column_values(p, c["header"])
                    entry = {"table": t["name"], "column": c["header"], "distinct_values": sorted(set(vals))[:8], "distinct_count": len(set(vals))}
                    nums = [float(m) for v in vals for m in NUM.findall(v)[:1]]
                    if cls == "oxygen" and c["header"].upper().startswith("X"):  # a mole fraction cannot exceed 1: such cells are counted, not read
                        bad = [v for v in nums if v > 1]
                        nums = [v for v in nums if v <= 1]
                        if bad:
                            entry["out_of_range_cells"] = len(bad)
                    if cls in ("oxygen", "flow") and nums and "display" not in c["header"].lower():
                        entry.update(min=min(nums), max=max(nums), reading=(oxygen_reading if cls == "oxygen" else flow_reading)(nums))
                    cols.append(entry)
            if cols:
                readings = sorted({c["reading"] for c in cols if "reading" in c})
                out.setdefault(sid, {})[slot] = {"map_status": s["status"], "given_by_extractors": s.get("given"), "columns": cols,
                                                 "table_reading": readings[0] if len(readings) == 1 else ("several columns disagree" if readings else None)}
    res = {"version": "1", "label": "What NASA's run tables hold for conditions the record text leaves open. Evidence beside the map; no verdict is changed.",
           "rules": {"oxygen": "concentration columns only, final values excluded, mole fractions above 1 counted as out of range and not read; below 20.5 % reduced, 20.5 to 22.0 % air, above 22.0 % enriched, more than one class: varied",
                     "flow": "speed columns only; all zero quiescent, all above zero forced flow, mixed several", "fuel": "material names shown, not classified"},
           "investigations": out}
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if a.page:
        a.page.write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    for sid, d in out.items():
        for slot, v in d.items():
            print(sid, slot, v["map_status"], v.get("given_by_extractors"), "->", v["table_reading"], [(c["column"], c.get("min"), c.get("max"), c["distinct_values"][:3]) for c in v["columns"]][:2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
