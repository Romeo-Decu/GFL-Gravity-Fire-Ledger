#!/usr/bin/env python3
"""Register predictions for runs not yet measured (pre-registered tests, src/gfl_analysis/predict.py).

    python tools/register_predictions.py --out data/predictions/REGISTERED_2026-11-12.json
The file is committed, sealed in the ledger and anchored (Git, RFC 3161) before any target run is measured.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_analysis import predict, records  # noqa: E402

TARGETS = [("B15", 10), ("B8", 10), ("B16", 3), ("B20", 3), ("B19", 10), ("B10", 3), ("B7", 2), ("B4", 5)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    ref = records.record("B6", 3)
    preds, refused = [], []
    for run, disp in TARGETS:
        tgt = records.record(run, disp)
        assert tgt["rate_mm_s"] is None, f"{run} is already measured; a prediction now would not be pre-registered"
        for law in predict.LAWS:
            p = predict.propose(ref, tgt, law)
            (refused if p["out_of_domain"] else preds).append(p if p["out_of_domain"] else predict.seal(p))
    out = {"note": "Registered before the target runs were measured; to be scored with the frozen rule R-W4 on the official challenge data (DEC-058). "
                   "Out-of-domain targets get no prediction, with the reason.", "reference": {k: ref[k] for k in ("run", "air_display", "rate_mm_s", "interval_mm_s", "rate_ref")},
           "predictions": preds, "not_predicted": [{k: r[k] for k in ("target", "law", "out_of_domain")} for r in refused]}
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for p in preds:
        print(p["target"], p["law"], p["expected_ratio"], p["band_ratio"])
    print("not predicted:", sorted({(r["target"], r["out_of_domain"][0][:40]) for r in refused}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
