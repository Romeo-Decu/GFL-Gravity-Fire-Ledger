#!/usr/bin/env python3
"""Apply measurement rule R-S1 (docs/SAFFIRE_RULE_R-S1.md) to one Saffire image set.

    python tools/saffire_measure.py --images DIR --grid GRID.jpg --label "Saffire-II 2-5" --out OUT.json [--nasa 2.1]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

THRESH, SENS, GATE, WIN, NBG, SEED = 0.5, (0.3, 0.7), 40.0, (0.2, 0.8), 30, 20261114


def scale_px_per_mm(grid: Path) -> dict:
    a = np.asarray(Image.open(grid).convert("L"), float)
    long_axis = 1 if a.shape[1] >= a.shape[0] else 0
    prof = a.mean(axis=0 if long_axis == 1 else 1)
    prof = prof - prof.mean()
    ac = np.correlate(prof, prof, "full")[len(prof) - 1:]
    ac /= ac[0]
    # first minimum then the next maximum: the full checker period (two blocks)
    d = np.diff(ac)
    first_min = next(i for i in range(1, len(d)) if d[i - 1] < 0 <= d[i])
    period = first_min + int(np.argmax(ac[first_min:first_min * 3]))
    return {"grid": grid.name, "period_px": int(period), "px_per_mm": round(period / 60.0, 4), "long_axis": "columns" if long_axis == 1 else "rows"}


def luminance(path: Path, long_axis: str) -> np.ndarray:
    a = np.asarray(Image.open(path).convert("RGB"), float)
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    if long_axis == "rows":
        y = y.T
    h = y.shape[0]
    return y[h // 4: h - h // 4].mean(axis=0)


def edge(p: np.ndarray, frac: float, from_left: bool):
    pk = p.max()
    if pk < GATE:
        return None
    idx = np.nonzero(p >= frac * pk)[0]
    return float(idx.max() if from_left else idx.min())


def fit(t, x):
    A = np.vstack([t, np.ones_like(t)]).T
    return float(np.linalg.lstsq(A, x, rcond=None)[0][0])


def boot(t, x, block_s=1.0, n=2000):
    rng = np.random.default_rng(SEED)
    dt = np.median(np.diff(t))
    b = max(2, int(round(block_s / dt)))
    starts = np.arange(0, len(t) - b + 1)
    k = int(np.ceil(len(t) / b))
    out = []
    for _ in range(n):
        idx = np.concatenate([np.arange(s, s + b) for s in rng.choice(starts, k)])[: len(t)]
        if np.ptp(t[idx]) > 0:
            out.append(fit(t[idx], x[idx]))
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def smooth(p: np.ndarray, k: int = 9) -> np.ndarray:
    return np.convolve(p, np.ones(k) / k, mode="same")


def measure_rs2(images: list[Path], grid: Path) -> dict:
    """R-S2 (docs/SAFFIRE_RULE_R-S2.md): the dark front in backlit images."""
    sc = scale_px_per_mm(grid)
    times = np.array([int(re.search(r"(\d{12,})", p.name).group(1)) for p in images], float) / 1000.0
    order = np.argsort(times)
    images = [images[i] for i in order]
    times = times[order] - times[order][0]
    prof = np.array([smooth(luminance(p, sc["long_axis"])) for p in images])
    L = prof.shape[1]
    tenth = max(1, L // 10)
    valid = [i for i in range(len(prof)) if 60 <= np.percentile(prof[i], 95) <= 240]
    if not valid:
        return {"status": "not measurable", "reason": "no frame with the backlight on and not saturated", "scale": sc}
    f0 = prof[valid[0]]
    ign_left = f0[:tenth].mean() < f0[-tenth:].mean()
    res = {"scale": sc, "frames_total": len(images), "frames_valid": len(valid), "ignition_end": "left" if ign_left else "right"}
    for frac in (THRESH,) + SENS:
        pos, ts = [], []
        for i in valid:
            p = prof[i] if ign_left else prof[i][::-1]          # ignition end at index 0
            ref = np.median(p[-tenth:])
            below = np.nonzero(p[::-1] < frac * ref)[0]           # scan from the far end
            if not len(below):
                continue
            x = L - 1 - below[0]                                  # distance from the ignition end, pixels
            if WIN[0] <= x / (L - 1) <= WIN[1]:
                pos.append(x / sc["px_per_mm"]); ts.append(times[i])
        if len(pos) < 20:
            res[f"t{frac}"] = {"status": "not measurable", "frames": len(pos)}
            continue
        t, x = np.array(ts), np.array(pos)
        r = {"frames": len(pos), "t_s": [round(float(t[0]), 2), round(float(t[-1]), 2)], "rate_mm_s": round(fit(t, x), 4)}
        if frac == THRESH:
            r["interval_mm_s"] = [round(v, 4) for v in boot(t, x)]
            r["r2"] = round(float(np.corrcoef(t, x)[0, 1] ** 2), 4)
        res[f"t{frac}"] = r
    return res


def measure(images: list[Path], grid: Path) -> dict:
    sc = scale_px_per_mm(grid)
    times = np.array([int(re.search(r"(\d{12,})", p.name).group(1)) for p in images], float) / 1000.0
    order = np.argsort(times)
    images = [images[i] for i in order]
    times = times[order] - times[order][0]
    prof = np.array([luminance(p, sc["long_axis"]) for p in images])
    bg = np.median(prof[:NBG], axis=0)
    sub = prof - bg
    L = sub.shape[1]
    first = next((i for i in range(len(sub)) if sub[i].max() >= GATE), None)
    if first is None:
        return {"status": "not measurable", "reason": "no frame passes the brightness gate", "scale": sc}
    from_left = int(np.argmax(sub[first])) < L / 2
    res = {"scale": sc, "frames_total": len(images), "first_valid_frame_s": round(float(times[first]), 3), "ignition_end": "left" if from_left else "right"}
    for frac in (THRESH,) + SENS:
        e = [edge(sub[i], frac, from_left) for i in range(len(sub))]
        keep = [i for i, v in enumerate(e) if v is not None and WIN[0] <= ((v if from_left else L - 1 - v) / (L - 1)) <= WIN[1]]
        if len(keep) < 20:
            res[f"t{frac}"] = {"status": "not measurable", "frames": len(keep)}
            continue
        t = times[keep]
        x = np.array([e[i] if from_left else L - 1 - e[i] for i in keep]) / sc["px_per_mm"]
        r = {"frames": len(keep), "t_s": [round(float(t[0]), 2), round(float(t[-1]), 2)], "rate_mm_s": round(fit(t, x), 4)}
        if frac == THRESH:
            r["interval_mm_s"] = [round(v, 4) for v in boot(t, x)]
            r["r2"] = round(float(np.corrcoef(t, x)[0, 1] ** 2), 4)
        res[f"t{frac}"] = r
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True, type=Path)
    ap.add_argument("--grid", required=True, type=Path)
    ap.add_argument("--label", required=True)
    ap.add_argument("--nasa", type=float)
    ap.add_argument("--rule", choices=["R-S1", "R-S2"], default="R-S1")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    imgs = sorted(p for p in a.images.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg"))
    res = {"rule": f"{a.rule} (docs/SAFFIRE_RULE_{a.rule}.md)", "label": a.label, "image_count": len(imgs),
           "image_list_sha256": hashlib.sha256("\n".join(p.name for p in imgs).encode()).hexdigest(), **(measure(imgs, a.grid) if a.rule == "R-S1" else measure_rs2(imgs, a.grid))}
    m = res.get(f"t{THRESH}", {})
    if a.nasa and m.get("rate_mm_s"):
        res["nasa_reported_mm_s"] = a.nasa
        res["relative_difference"] = round(m["rate_mm_s"] / a.nasa - 1, 4)
        res["reproduces_within_20pct"] = abs(res["relative_difference"]) <= 0.20
    a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: res.get(k) for k in ("label", "image_count", "scale", "t0.5", "t0.3", "t0.7", "nasa_reported_mm_s", "relative_difference", "reproduces_within_20pct")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
