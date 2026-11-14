#!/usr/bin/env python3
"""Summarise the two human readings of the evidence map (amendment A4, RES-063).

    python tools/human_check_summary.py --out data/derived/evidence_map/HUMAN_CHECK_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data/derived/evidence_map/human_check"
READERS = ("Romeo", "Cristina")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--page", type=Path)
    a = ap.parse_args(argv)
    rows, files = {}, {}
    for r in READERS:
        p = DIR / f"GFL_HUMAN_CHECK_{r}.xlsx"
        files[r] = hashlib.sha256(p.read_bytes()).hexdigest()
        ws = load_workbook(p, data_only=True)["Check"]
        rows[r] = [[c.value for c in x] for x in ws.iter_rows(min_row=3) if x[0].value]
    n = len(rows[READERS[0]])
    count = lambda r, why, v: sum(1 for x in rows[r] if x[0] == why and x[6] == v)  # noqa: E731
    per = {r: {why: {v: count(r, why, v) for v in ("correct", "wrong", "cannot tell")} for why in ("flagged by INDUS", "random sample")} for r in READERS}
    agree = sum(1 for x, y in zip(*rows.values()) if x[6] == y[6])
    sample_n = sum(1 for x in rows[READERS[0]] if x[0] == "random sample")
    res = {"version": "1", "readers": list(READERS), "files_sha256": files, "items": n, "by_reader": per,
           "agreement_between_readers": {"same_verdict": agree, "of": n},
           "wrong_found": {r: sum(1 for x in rows[r] if x[6] == "wrong") for r in READERS},
           "random_sample_items": sample_n,
           "upper_bound_error_rate_95": round(3 / sample_n, 3),
           "label": "Two team members read each item against NASA's record, separately. They are not independent of the project, and each item showed the map's claim beside the passage, which favours agreement. With no wrong item among the sampled ones, the error rate of unflagged items is below about 3/n at 95 % confidence (rule of three), not zero."}
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if a.page:
        a.page.write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: res[k] for k in ("by_reader", "agreement_between_readers", "wrong_found", "upper_bound_error_rate_95")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
