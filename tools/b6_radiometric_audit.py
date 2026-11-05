"""B6 radiometric and morphological audit (red team #2, IDEA-032-A/B).

Per frame in 13-53 s: raw-DN peak before exposure normalisation, saturated raw pixels in the
holder band (white level), integrated band signal, flame area at 0.1 of the frame peak,
R/G and B/G inside the flame, and the width of the leading ramp (distance between the
0.05 and 0.5 per-frame crossings). Trends are reported as correlation with time and as
last-5 / first-5 frame ratios.

    python tools/b6_radiometric_audit.py --nef-dir <FIF_DATA>/derived/b6_nef --out data/derived/B6_RADIOMETRIC_AUDIT_v0.1.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import flame_front as ff

ROWS_HALF = (655, 1017)
PX_PER_MM = 14.7


def main(argv=None) -> int:
    import rawpy
    ap = argparse.ArgumentParser()
    ap.add_argument("--nef-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    rows, t0 = [], None
    for f in sorted(a.nef_dir.glob("*.NEF")):
        ts, e = ff.frame_time_and_exposure(f)
        t0 = ts if t0 is None else t0
        t = ts - t0
        if not 13 <= t <= 53:
            continue
        with rawpy.imread(str(f)) as r:
            raw = r.raw_image_visible
            wl, bl = int(r.white_level), float(np.mean(r.black_level_per_channel))
            lin = r.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16, half_size=True,
                                use_camera_wb=True, user_flip=0).astype(float)
        band_raw = raw[2 * ROWS_HALF[0]:2 * ROWS_HALF[1]]
        sat = band_raw >= wl - 1
        y = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
        b = (y - np.median(y))[ROWS_HALF[0]:ROWS_HALF[1]]
        p = b.mean(0)
        m = b > 0.1 * b.max()
        rgb = [lin[ROWS_HALF[0]:ROWS_HALF[1], :, k][m].sum() for k in range(3)]
        pf = p / p.max()
        ramp = (np.flatnonzero(pf > 0.05).max() - np.flatnonzero(pf > 0.5).max()) / PX_PER_MM
        rows.append({"t_s": round(t, 2), "exposure_s": e, "raw_dn_p9999": float(np.percentile(band_raw.astype(float) - bl, 99.99)),
                     "saturated_px_band": int(sat.sum()), "saturated_frac_band": float(sat.mean()),
                     "integrated_signal_dn": float(b[b > 0].sum()), "integrated_radiance": float(b[b > 0].sum() / e),
                     "flame_area_px_rel01": int(m.sum()), "r_over_g": rgb[0] / rgb[1], "b_over_g": rgb[2] / rgb[1],
                     "leading_ramp_mm": float(ramp)})
    t = np.array([r["t_s"] for r in rows])
    trends = {}
    for k in ("raw_dn_p9999", "saturated_px_band", "integrated_signal_dn", "integrated_radiance", "flame_area_px_rel01",
              "r_over_g", "b_over_g", "leading_ramp_mm"):
        v = np.array([r[k] for r in rows], float)
        trends[k] = {"corr_with_time": round(float(np.corrcoef(t, v)[0, 1]), 3),
                     "last5_over_first5": round(float(v[-5:].mean() / v[:5].mean()), 3)}
    v = np.array([r["leading_ramp_mm"] for r in rows])
    trends["leading_ramp_mm"]["slope_mm_s"] = round(float(np.polyfit(t, v, 1)[0]), 4)
    e = np.array([r["exposure_s"] for r in rows])
    out = {"window_s": [13, 53], "frames": rows, "trends": trends,
           "exposure_ratio_first5_over_last5": round(float(e[:5].mean() / e[-5:].mean()), 3),
           "format": "NEF raw, 14-bit (white level 16383), linear demosaic gamma 1, no auto-brightness"}
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(trends, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
