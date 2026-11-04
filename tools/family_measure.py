"""Measure leading-edge spread rate for every run of a family with one predeclared rule set.

Rules (fixed before looking at any family result):
  * timing: EXIF DateTimeOriginal + SubSecTimeOriginal;
  * radiance: linear demosaic / exposure time, minus frame median;
  * frames with a bright background (illuminated / post-burn) are excluded;
  * row band: rows where the flame mask (relative threshold 0.2) is present in
    >= 30 % of flame frames;
  * leading edge: last column of the band-averaged profile above a threshold;
    thresholds are RELATIVE: {0.1, 0.2, 0.4} x the run's median per-frame
    profile maximum, so dim near-limit flames and bright flames are treated alike;
  * propagation direction: sign of the overall front displacement;
  * fit window: frames whose leading edge lies between 20 % and 80 % of its
    total travel (excludes igniter-dominated start and holder-end region);
  * abstain (no rate) if < 6 frames in the window or travel < 15 mm.

    python tools/family_measure.py --config data/derived/BASSII_100UM_MEASUREMENT_CONFIG_v0.1.json \
        --out data/derived/BASSII_100UM_SPREAD_RATES_v0.1.json
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

import flame_front as ff

REL_THR = (0.1, 0.2, 0.4)
BRIGHT_BG = 5e4          # counts/s; above = illuminated frame
MIN_FRAMES, MIN_TRAVEL_MM = 6, 15.0


def load_run(nef_dir: Path):
    frames = []
    for f in sorted(nef_dir.glob("*.NEF")):
        ts, exp = ff.frame_time_and_exposure(f)
        y = ff.relative_radiance(f, exp)
        bg = float(np.median(y))
        if bg >= BRIGHT_BG:
            continue
        frames.append({"image": f.stem, "ts": ts, "exp": exp, "s": (y - bg).astype(np.float32)})
    return frames


def measure(frames, px_per_mm_half: float, rel_unc: float) -> dict:
    if not frames:
        return {"status": "abstain", "reason": "no flame frames"}
    t0 = frames[0]["ts"]
    peaks = np.array([np.percentile(fr["s"], 99.9) for fr in frames])
    lit = peaks > 3 * np.median(np.abs([np.percentile(fr["s"], 50) for fr in frames]) + 1)
    flame = [fr for fr, k in zip(frames, lit) if k]
    if len(flame) < MIN_FRAMES:
        return {"status": "abstain", "reason": f"only {len(flame)} flame-bearing frames", "n_flame_frames": len(flame)}
    ref = float(np.median([fr["s"].max() for fr in flame]))
    occ = np.mean([(fr["s"] > 0.2 * ref).any(axis=1) for fr in flame], axis=0)
    rows = np.flatnonzero(occ >= 0.3)
    if rows.size < 5:
        return {"status": "abstain", "reason": "no persistent flame row band"}
    r0, r1 = int(rows.min()), int(rows.max()) + 1
    profs = [(fr["ts"] - t0, fr["s"][r0:r1].mean(axis=0), fr["image"]) for fr in flame]
    pmax = float(np.median([p.max() for _, p, _ in profs]))
    out = {"row_band_half_px": [r0, r1], "n_flame_frames": len(flame), "per_threshold": {}}
    rates = []
    for rel in REL_THR:
        pts = [(t, int(np.flatnonzero(p > rel * pmax).max()), im) for t, p, im in profs if (p > rel * pmax).any()]
        if len(pts) < MIN_FRAMES:
            continue
        t = np.array([p[0] for p in pts]); x = np.array([p[1] for p in pts], float)
        direction = 1.0 if x[-1] >= x[0] else -1.0
        x = direction * x
        lo, hi = np.percentile(x, 5), np.percentile(x, 95)
        travel_mm = (hi - lo) / px_per_mm_half
        a, b = lo + 0.2 * (hi - lo), lo + 0.8 * (hi - lo)
        m = (x >= a) & (x <= b)
        rec = {"n_window": int(m.sum()), "travel_mm": round(float(travel_mm), 1), "direction": int(direction)}
        if m.sum() >= MIN_FRAMES and travel_mm >= MIN_TRAVEL_MM:
            s, se, res = ff.linfit(t[m], x[m])
            rec.update(v_mm_s=round(s / px_per_mm_half, 4), fit_se_mm_s=round(se / px_per_mm_half, 4),
                       resid_rms_px=round(float(res.std()), 1), t_window_s=[round(float(t[m].min()), 2), round(float(t[m].max()), 2)])
            rates.append(rec["v_mm_s"])
        out["per_threshold"][str(rel)] = rec
    if len(rates) < 2:
        out.update(status="abstain", reason="fewer than two thresholds give a valid fit window")
        return out
    v = np.array(rates); c = float(np.median(v))
    u_fit = max(d.get("fit_se_mm_s", 0) for d in out["per_threshold"].values())
    u_thr = float((v.max() - v.min()) / 2); u_sc = c * rel_unc
    out.update(status="measured", value_mm_s=round(c, 3),
               standard_uncertainty_mm_s=round(float(np.sqrt(u_fit ** 2 + u_thr ** 2 + u_sc ** 2)), 3),
               components_mm_s={"fit": round(u_fit, 4), "threshold_half_range": round(u_thr, 4), "scale": round(u_sc, 4)})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    cfg = json.loads(a.config.read_text(encoding="utf-8"))
    root = Path(os.environ.get("FIF_DATA", Path.home() / "FiF_Data"))
    results = {"rules": __doc__.split("Rules")[1].split("python tools")[0].strip(), "runs": {}}
    for run in cfg["runs"]:
        frames = load_run(root / run["nef_dir"])
        r = measure(frames, run["px_per_mm_full"] / 2.0, run["scale_rel_unc"])
        r.update({k: run[k] for k in ("test", "session", "scale_source", "px_per_mm_full")})
        results["runs"][run["test"]] = r
        print(run["test"], r.get("status"), r.get("value_mm_s"), r.get("standard_uncertainty_mm_s"), r.get("reason", ""))
    a.out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
