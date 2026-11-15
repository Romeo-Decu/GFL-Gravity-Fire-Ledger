#!/usr/bin/env python3
"""Three incidents named by the challenge, against the evidence map (RES-062).

For each incident: NASA's own words (checked word for word against the page text), the fire-safety functions it
involved, and what the archive holds for them: investigations agreed by all three extractors, and whether any run
table records the incident's atmosphere. Nothing is inferred beyond those counts.

    python tools/build_incidents.py --pages "<folder with NASA's pages as PDF>" --out data/derived/evidence_map/INCIDENTS_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import gfl_map  # noqa: E402


def page_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True, type=Path)
    ap.add_argument("--fixture", type=Path, default=ROOT / "research/fixtures/INCIDENTS_v1.json")
    ap.add_argument("--map", type=Path, default=ROOT / "data/derived/evidence_map/EVIDENCE_MAP_v2.json")
    ap.add_argument("--tables", type=Path, default=ROOT / "data/derived/evidence_map/RUN_TABLE_INVENTORY_v1.json")
    ap.add_argument("--evidence", type=Path, default=ROOT / "data/derived/evidence_map/RUN_TABLE_EVIDENCE_v1.json")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--page", type=Path)
    a = ap.parse_args(argv)
    fx, emap = json.loads(a.fixture.read_text(encoding="utf-8")), json.loads(a.map.read_text(encoding="utf-8"))
    ev = json.loads(a.evidence.read_text(encoding="utf-8"))["investigations"]
    inv = emap["investigations"]
    out = []
    for inc in fx["incidents"]:
        checks = []
        for fk, qk in (("file", "quote"), ("second_file", "second_quote"), ("file", "second_quote")):
            if inc.get(fk) and inc.get(qk) and not (qk == "second_quote" and fk == "file" and inc.get("second_file")):
                p = a.pages / inc[fk]
                txt = page_text(p)
                checks.append({"quote": inc[qk], "file": inc[fk], "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "found_word_for_word": gfl_map.quoted(inc[qk], txt)})
        fn = {f: sorted((x["study"] for x in emap["by_function"][f] if x["status"] == "agreed"), key=lambda s: int(s.split("-")[1])) for f in inc["functions"]}
        atm_text = sorted(i for i, v in inv.items() if v["slots"]["atmosphere"]["status"] == "agreed" and v["slots"]["atmosphere"]["value"] == inc["atmosphere"])
        atm_tables = sorted(i for i, d in ev.items() if d.get("atmosphere", {}).get("columns") and any(c.get("max") and (c["max"] * (100 if c["max"] <= 1 else 1)) > 30 for c in d["atmosphere"]["columns"]))
        solid_enriched = [i for i in atm_tables if inv[i]["slots"]["fuel_phase"]["value"] == "solid" and inv[i]["slots"]["fuel_phase"]["status"] == "agreed"]
        out.append({**{k: inc[k] for k in ("id", "name", "source", "functions", "atmosphere", "what_the_archive_needs")}, "quotes_checked": checks,
                    "agreed_investigations_by_function": fn,
                    "atmosphere_agreed_in_record_text": atm_text,
                    "run_tables_above_30_pct_oxygen": atm_tables if inc["atmosphere"] == "enriched oxygen" else None,
                    "of_which_solid_fuel": solid_enriched if inc["atmosphere"] == "enriched oxygen" else None})
    res = {"version": "1", "label": fx["label"], "incidents": out, "all_quotes_found": all(c["found_word_for_word"] for i in out for c in i["quotes_checked"])}
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if a.page:
        a.page.write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    for i in out:
        print(i["id"], [c["found_word_for_word"] for c in i["quotes_checked"]], {f: len(v) for f, v in i["agreed_investigations_by_function"].items()}, i["atmosphere_agreed_in_record_text"], i["run_tables_above_30_pct_oxygen"], i["of_which_solid_fuel"])
    return 0 if res["all_quotes_found"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
