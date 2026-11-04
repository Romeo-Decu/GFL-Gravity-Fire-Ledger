"""Spatial scale from the BASS 'deployed scale' (ruler) in illuminated post-burn stills.

For each candidate frame the ruler band is located automatically (row band with
the strongest periodic signal), then the label period (10 mm) is measured by
autocorrelation and cross-checked with the minor-tick period (1 mm).
Output: px/mm at full resolution, per frame and pooled, with spread.

    python tools/ruler_scale.py --nef iss040e045734.NEF iss040e045736.NEF ...
"""
from __future__ import annotations

import argparse
import json

import numpy as np


def load_gray(path: str) -> np.ndarray:
    import rawpy
    with rawpy.imread(path) as r:
        rgb = r.postprocess(use_camera_wb=True, output_bps=8, user_flip=0)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]).astype(float)


def periodicity(profile: np.ndarray, lo: int, hi: int) -> tuple[float, float]:
    p = profile - np.convolve(profile, np.ones(4 * hi + 1) / (4 * hi + 1), "same")
    p = p[2 * hi:-2 * hi]
    if p.size < 3 * hi or not np.any(p):
        return float("nan"), 0.0
    ac = np.correlate(p, p, "full")[p.size - 1:]
    ac = ac / ac[0]
    k = np.arange(lo, min(hi, ac.size - 1))
    i = k[np.argmax(ac[k])]
    y0, y1, y2 = ac[i - 1], ac[i], ac[i + 1]
    den = y0 - 2 * y1 + y2
    return float(i + (0.5 * (y0 - y2) / den if den else 0.0)), float(y1)


def ruler_scale(gray: np.ndarray, label_px=(200, 450), band_h=140, step=35) -> dict:
    h, w = gray.shape
    x0, x1 = int(0.08 * w), int(0.85 * w)
    best = None
    for r0 in range(int(0.25 * h), int(0.85 * h) - band_h, step):
        per, q = periodicity(gray[r0:r0 + band_h, x0:x1].mean(0), *label_px)
        if np.isfinite(per) and (best is None or q > best["quality"]):
            best = {"row0": r0, "label_period_px": per, "quality": q}
    if best is None:
        return {"ok": False}
    # minor ticks: search just above the label band
    tick = None
    for r0 in range(max(0, best["row0"] - 3 * step), best["row0"] + step, step // 2):
        per, q = periodicity(gray[r0:r0 + 60, x0:x0 + (x1 - x0) // 3].mean(0), 15, 60)
        if np.isfinite(per) and (tick is None or q > tick[1]):
            tick = (per, q)
    best.update({"ok": True, "px_per_mm": best["label_period_px"] / 10.0,
                 "minor_tick_px": tick[0] if tick else None,
                 "label_to_tick_ratio": (best["label_period_px"] / tick[0]) if tick else None})
    return best


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nef", nargs="+", required=True)
    ap.add_argument("--min-quality", type=float, default=0.4)
    a = ap.parse_args(argv)
    rows = []
    for f in a.nef:
        r = ruler_scale(load_gray(f))
        r["image"] = f.rsplit("/", 1)[-1]
        rows.append(r)
    good = [r for r in rows if r.get("ok") and r["quality"] >= a.min_quality]
    if good:  # robust: drop frames whose band locked onto another periodic feature
        med = float(np.median([r["px_per_mm"] for r in good]))
        for r in good:
            r["outlier"] = abs(r["px_per_mm"] - med) / med > 0.05
        good = [r for r in good if not r["outlier"]]
    vals = np.array([r["px_per_mm"] for r in good])
    out = {"frames": rows,
           "pooled_px_per_mm_full_res": float(np.median(vals)) if vals.size else None,
           "spread_rel": float((vals.max() - vals.min()) / 2 / np.median(vals)) if vals.size > 1 else None,
           "n_used": int(vals.size),
           "assumption": "numbered ruler labels every 10 mm; checked by ~10 minor ticks per label"}
    print(json.dumps(out, indent=1, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
