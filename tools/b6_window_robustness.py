#!/usr/bin/env python3
"""Robustness of the R-W2 primary B6 rate (AIR display 3 segment) to the rule's own choices.

Varies, one grid, nothing selected from it: G3 clipping factor {5, 10, 20, off},
G5 flow guard {2, 3, 4} s, overlay-to-still clock shift {-2..+2} s. Reports the
leading-edge rate (0.05 / 0.1 / 0.5 of frame peak) for every configuration that
meets the segment minimum (6 frames over >= 6 s). Also checks that the NEF-derived
profiles equal the blind band profiles used in WF-0011 (RES-019).

    python tools/b6_window_robustness.py --nef-dir <B6_NEF> \
        --overlay data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv \
        --blind-profiles <B6_band_profiles.csv> --out data/derived/B6_WINDOW_ROBUSTNESS_v1.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b6_window_rule as w  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nef-dir", required=True, type=Path)
    ap.add_argument("--overlay", required=True, type=Path)
    ap.add_argument("--blind-profiles", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    fr = w.frame_data(a.nef_dir)
    t = np.array([f["t_s"] for f in fr])
    prof = [f["profile"] for f in fr]
    sat = np.array([f["sat_px"] for f in fr])
    med = float(np.median(sat))

    with open(a.blind_profiles, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]
    rel_diff = max(float(np.max(np.abs(prof[i] - np.array(rows[i][1:], float))) / np.max(np.abs(prof[i])))
                   for i in range(len(fr)))

    ov_t, ov_air = [], []
    with open(a.overlay, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ov_t.append(float(r["still_t_s_est"]))
            ov_air.append(int(r["AIR_display"]))

    def rate(idx, frac):
        x = np.array([w.lead_rel(prof[i], frac) for i in idx], float)
        return float(np.polyfit(t[idx], x, 1)[0] / w.PX_PER_MM)

    grid = []
    for g3 in (5.0, 10.0, 20.0, None):
        for guard in (2.0, 3.0, 4.0):
            for shift in (-2, -1, 0, 1, 2):
                ts = [x + shift for x in ov_t]
                ch = [(ts[i - 1] + ts[i]) / 2 for i in range(1, len(ts)) if ov_air[i] != ov_air[i - 1]]
                lo, hi = ch[0], ch[1]          # the AIR = 3 interval
                sel = [i for i in range(len(fr)) if lo < t[i] < hi and t[i] < 73
                       and (g3 is None or sat[i] <= g3 * med)
                       and all(abs(t[i] - c) > guard for c in ch)
                       and w.lead_rel(prof[i], 0.05) is not None]
                ok = len(sel) >= w.MIN_SEG_FRAMES and t[sel[-1]] - t[sel[0]] >= w.MIN_SEG_SPAN_S if sel else False
                grid.append({"g3_factor": g3, "guard_s": guard, "clock_shift_s": shift, "frames": len(sel),
                             "t_range_s": [float(t[sel[0]]), float(t[sel[-1]])] if sel else None, "fitted": bool(ok),
                             **({f"rate_rel_{f}_mm_s": round(rate(sel, f), 4) for f in (0.05, 0.1, 0.5)} if ok else {})})
    r01 = [g["rate_rel_0.1_mm_s"] for g in grid if g["fitted"]]
    out = {"segment": "AIR display 3", "nef_vs_blind_profile_max_rel_diff": rel_diff,
           "configs": len(grid), "fitted_configs": len(r01),
           "rate_rel_0.1_mm_s": {"min": min(r01), "median": float(np.median(r01)), "max": max(r01)},
           "grid": grid}
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "grid"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
