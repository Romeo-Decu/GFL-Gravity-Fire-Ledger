#!/usr/bin/env python3
"""Draw the AAL test 2 truth at random within the protocol's ranges and write it without printing it.

    python tools/make_test2_truth.py --out <withheld truth.json>
Only the SHA-256 is printed; the values stay unseen until scoring.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from pathlib import Path

import numpy as np


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    seed = secrets.randbelow(10 ** 9)
    rng = np.random.default_rng(seed)
    u = lambda lo, hi: round(float(rng.uniform(lo, hi)), 3)  # noqa: E731

    def sched(v3, v2):
        return [{"t0": 0.0, "t1": 5.5, "air": 4, "v_mm_s": u(1.2, 2.0)},
                {"t0": 5.5, "t1": 32.5, "air": 3, "v_mm_s": v3},
                {"t0": 32.5, "t1": 44.5, "air": 2, "v_mm_s": v2},
                {"t0": 44.5, "t1": 80.0, "air": 1, "v_mm_s": u(0.8, 1.6)}]

    def sched_short(v2):  # T3: display 3 lasts only 7 s, display 2 is the estimand
        return [{"t0": 0.0, "t1": 8.0, "air": 5, "v_mm_s": u(1.4, 2.4)},
                {"t0": 8.0, "t1": 15.0, "air": 3, "v_mm_s": u(1.4, 2.4)},
                {"t0": 15.0, "t1": 42.0, "air": 2, "v_mm_s": v2},
                {"t0": 42.0, "t1": 80.0, "air": 0, "v_mm_s": u(0.5, 1.2)}]

    base = {"x0_mm": 8.0, "s_t": [10, 40], "L_mm": 30.0, "s_trail_mm": 6.0, "A0": 1.5e6, "A_growth_per_s": 0.03}
    cases = {
        "T1": dict(base, seed_offset=11, schedule=sched(u(1.2, 2.6), u(1.2, 2.6)), s_lead_mm=[u(2.6, 3.4), u(1.3, 1.9)],
                   skew_nu=u(0.35, 0.6), clip_frames=[int(rng.integers(12, 24))]),
        "T2": dict(base, seed_offset=12, schedule=sched(u(1.2, 2.6), u(1.2, 2.6)), s_lead_mm=[u(1.4, 2.0), u(2.8, 3.6)],
                   flicker=u(0.08, 0.15)),
        "T3": dict(base, seed_offset=13, schedule=sched_short(u(1.0, 2.2)), s_lead_mm=[2.5, 2.5], preburn_gap_s=u(240, 300)),
        "T4": dict(base, seed_offset=14, schedule=sched(u(1.2, 2.6), u(1.2, 2.6)), s_lead_mm=[2.5, 2.5],
                   offset_mm=[u(0.3, 0.8), u(2.0, 3.5)]),
    }
    truth = {"note": "AAL test 2 part S2 ground truth; withheld until scoring", "seed": seed,
             "t_ignition_s": 4.0, "flash_s": 4.0, "flash_factor": 6.0, "t_burn_end_s": 62.0, "late_gap_s": 0.0,
             "background": 0.0, "target_raw": 8000.0, "full_well": 16383.0, "read_noise": 30.0, "shot_k": 20.0, "band_rows": 362,
             "estimand_air": {"T1": 3, "T2": 3, "T3": 2, "T4": 3}, "cases": cases}
    a.out.write_text(json.dumps(truth, indent=1) + "\n")
    print(hashlib.sha256(a.out.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
