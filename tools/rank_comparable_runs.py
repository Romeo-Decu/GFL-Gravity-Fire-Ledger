#!/usr/bin/env python3
"""Rank BASS-II runs by how comparable their recorded conditions are to a reference run.

Deterministic, no AI. Reads the NASA PSI-25 experimental table (verified against its ledger
seal before use), parses each row's recorded conditions and compares them with the reference
run dimension by dimension. Every dimension ends in one of three states:
  match    - the recorded value equals the reference within the stated tolerance
  differs  - the recorded value is known and differs
  unknown  - the cell is empty or cannot be parsed; unknown is never treated as a match

Levels (first that applies):
  not_comparable   material class or geometry class differs, or either is unknown
  same_conditions  every dimension matches
  close            exactly one dimension differs, none unknown
  distant          anything else (two or more differ, or any unknown)

This compares what the table records. It does not establish that two runs are physically
equivalent: conditions the table does not record (sample history, ignition energy, local
flow speed in cm/s, ISS-013) are outside the comparison and stated as such.

    python tools/rank_comparable_runs.py --table "<...>/PSI-25_Experimental table_BASS-II.csv" \
        --reference B6 --air 3 --out data/derived/BASSII_COMPARABLE_RUNS_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_LEDGER_LOCATION = "Experimental table/PSI-25_Experimental table_BASS-II.csv"
O2_TOL = 0.5  # % by volume
DIMENSIONS = ["material", "geometry", "thickness_um", "width_cm", "flow_restrictor", "air_setting", "initial_o2_pct"]
NOT_RECORDED = ["air velocity in cm/s for each display setting (ISS-013)", "sample conditioning and history",
                "ignition energy and igniter position", "camera exposure settings (recorded in the image files, not the table)"]


def norm(s: str) -> str:
    return " ".join((s or "").replace(" ", " ").split())


def parse_material(raw: str) -> dict:
    s = norm(raw).lower()
    out = {"material": None, "geometry": None, "thickness_um": None, "width_cm": None}
    if not s:
        return out
    if "sibal" in s:
        out["material"] = "SIBAL fabric"
    elif "nomex" in s:
        out["material"] = "Nomex"
    elif "wax" in s or "candle" in s:
        out["material"] = "wax"
    elif "pmma" in s or "rod" in s or "film" in s or "slab" in s:
        out["material"] = "PMMA"  # films and rods in this table are PMMA (clear/black cast acrylic)
    if "rod" in s:
        out["geometry"] = "rod"
    elif "spher" in s:
        out["geometry"] = "sphere"
    m = re.search(r"(\d+(?:\.\d+)?)\s*micron", s)
    if m:
        out["thickness_um"] = float(m.group(1))
    else:
        mm = re.findall(r"(\d+(?:\.\d+)?)\s*mm", s)
        if mm:
            out["thickness_um"] = float(mm[0]) * 1000
    w = re.search(r"(\d+(?:\.\d+)?)\s*cm", s)
    if w and out["geometry"] is None:
        out["width_cm"] = float(w.group(1))
    if out["geometry"] is None and out["thickness_um"] is not None:
        out["geometry"] = "film" if out["thickness_um"] <= 400 else "slab"
    if out["material"] == "SIBAL fabric" and out["geometry"] is None:
        out["geometry"] = "fabric"
    return out


def parse_air(raw: str) -> list[float] | None:
    s = norm(raw)
    if not s or "see fan" in s or "no ign" in s:
        return None
    s = s.split("(")[0]
    s = re.sub(r"pots?\s*[\d.\s]+", " ", s)          # potentiometer readings, not air display settings
    s = re.sub(r"\d+(?:\.\d+)?\s*pot", " ", s)
    s = re.sub(r"[<>~]\s*\d+(?:\.\d+)?", " ", s)     # bounds such as "<1" are not settings
    vals = [float(x) for x in re.findall(r"(?<![\d.])(\d+(?:\.\d+)?)(?![\d.])", s)]
    return vals or None


def num(raw: str) -> float | None:
    try:
        return float(norm(raw))
    except ValueError:
        return None


def row_conditions(r: dict) -> dict:
    c = parse_material(r.get("Fuel Sample Material", ""))
    c["flow_restrictor"] = num(r.get("Flow restrictor", ""))
    c["air_settings"] = parse_air(r.get("Air display", ""))
    c["initial_o2_pct"] = num(r.get("Calibrated  initial O2 % by vol ", ""))
    return c


def compare(ref: dict, c: dict, air: float) -> dict:
    st = {}
    for k in ("material", "geometry", "flow_restrictor"):
        st[k] = "unknown" if c[k] is None or ref[k] is None else ("match" if c[k] == ref[k] else "differs")
    for k in ("thickness_um", "width_cm"):
        st[k] = "unknown" if c[k] is None else ("match" if abs(c[k] - ref[k]) < 1e-9 else "differs")
    st["air_setting"] = "unknown" if c["air_settings"] is None else ("match" if air in c["air_settings"] else "differs")
    st["initial_o2_pct"] = "unknown" if c["initial_o2_pct"] is None else (
        "match" if abs(c["initial_o2_pct"] - ref["initial_o2_pct"]) <= O2_TOL else "differs")
    return st


def level(st: dict) -> str:
    if st["material"] != "match" or st["geometry"] != "match":
        return "not_comparable"
    vals = list(st.values())
    if all(v == "match" for v in vals):
        return "same_conditions"
    if vals.count("differs") == 1 and "unknown" not in vals:
        return "close"
    return "distant"


ORDER = {"same_conditions": 0, "close": 1, "distant": 2, "not_comparable": 3}


def rank(rows: list[dict], reference: str, air: float) -> dict:
    ref_row = next(r for r in rows if norm(r["Test #"]) == reference)
    ref = row_conditions(ref_row)
    out = []
    for i, r in enumerate(rows):
        test = norm(r["Test #"])
        if test == reference or not test:
            continue
        c = row_conditions(r)
        st = compare(ref, c, air)
        out.append({"test": test, "table_row": i + 2, "pi": norm(r["PI"]), "sample": norm(r["Sample #"]),
                    "material_as_recorded": norm(r["Fuel Sample Material"]), "air_display_as_recorded": norm(r["Air display"]),
                    "conditions": c, "states": st, "level": level(st),
                    "matches": sum(v == "match" for v in st.values())})
    out.sort(key=lambda x: (ORDER[x["level"]], -x["matches"], x["table_row"]))
    for n, x in enumerate(out, 1):
        x["rank"] = n
    counts = {k: sum(x["level"] == k for x in out) for k in ORDER}
    return {"reference": {"test": reference, "air_setting": air, "conditions": ref,
                          "material_as_recorded": norm(ref_row["Fuel Sample Material"])},
            "dimensions": DIMENSIONS, "o2_tolerance_pct": O2_TOL, "levels": list(ORDER),
            "not_recorded_in_table": NOT_RECORDED, "counts": counts, "runs": out}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sealed_sha() -> str | None:
    for line in (ROOT / "ledger/ledger.jsonl").read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if (e.get("object") or {}).get("location") == TABLE_LEDGER_LOCATION:
            return e["object"]["sha256"]
    return None


def load_rows(table: Path) -> list[dict]:
    with table.open(encoding="utf-8-sig", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True, type=Path)
    ap.add_argument("--reference", default="B6")
    ap.add_argument("--air", type=float, default=3.0)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    got, exp = sha256(a.table), sealed_sha()
    if got != exp:
        print(f"table SHA-256 {got[:12]} does not match the ledger seal {str(exp)[:12]}", file=sys.stderr)
        return 2
    res = rank(load_rows(a.table), a.reference, a.air)
    res["table"] = {"ledger_location": TABLE_LEDGER_LOCATION, "sha256": got}
    res["tool"] = "tools/rank_comparable_runs.py"
    text = json.dumps(res, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    print(json.dumps(res["counts"]))
    for x in res["runs"][:12]:
        print(x["rank"], x["test"], x["level"], x["matches"], x["material_as_recorded"], "|", x["air_display_as_recorded"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
