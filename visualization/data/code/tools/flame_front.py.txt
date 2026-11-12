"""FiF flame-front reconstruction from BASS-II top-view still images (NEF).

Implements docs/../research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md:
  * timing from EXIF DateTimeOriginal + SubSecTimeOriginal (same clock as the
    BASS video display, per the PSI proof sheet), never from a container FPS;
  * linear (gamma 1) demosaic, luminance normalised by exposure time so that
    bracketed frames are comparable (relative radiance, counts/s);
  * leading edge = last column of the width-averaged radiance profile above a
    threshold, inside a declared row band (holder opening);
  * thresholds are a predeclared set; the spread of results is reported as
    processing sensitivity, not tuned to match any published value.

    python tools/flame_front.py --nef-dir <FIF_DATA>/derived/b6_nef \
        --rows 655 1017 --t-window 13 53 --px-per-mm 14.7 --px-per-mm-rel-unc 0.03 \
        --track-out data/derived/B6_FRONT_TRACK_v0.1.csv \
        --result-out data/derived/B6_SPREAD_RATE_RESULT_v0.1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

import numpy as np

THRESHOLDS = (2e5, 5e5, 1e6)   # relative radiance (counts/s); predeclared before fitting


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def frame_time_and_exposure(path: Path) -> tuple[float, float]:
    import exifread
    with open(path, "rb") as f:
        t = exifread.process_file(f, details=False)
    dt = datetime.strptime(str(t["EXIF DateTimeOriginal"]), "%Y:%m:%d %H:%M:%S")
    sub = str(t.get("EXIF SubSecTimeOriginal", "0")).strip() or "0"
    num, den = (str(t["EXIF ExposureTime"]) + "/1").split("/")[:2]
    return dt.timestamp() + int(sub) / 10 ** len(sub), float(num) / float(den)


def relative_radiance(path: Path, exposure_s: float) -> np.ndarray:
    import rawpy
    with rawpy.imread(str(path)) as r:
        lin = r.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16,
                            half_size=True, use_camera_wb=True, user_flip=0)
    y = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    return (y / exposure_s).astype(np.float64)


def leading_edge(profile: np.ndarray, thr: float) -> int | None:
    idx = np.flatnonzero(profile > thr)
    return int(idx.max()) if idx.size else None


def linfit(t: np.ndarray, x: np.ndarray) -> tuple[float, float, np.ndarray]:
    a = np.vstack([t, np.ones_like(t)]).T
    coef, *_ = np.linalg.lstsq(a, x, rcond=None)
    r = x - a @ coef
    s2 = float(r @ r) / (len(t) - 2)
    se = float(np.sqrt(s2 * np.linalg.inv(a.T @ a)[0, 0]))
    return float(coef[0]), se, r


def track(nef_dir: Path, rows: tuple[int, int], exclude_after_s: float | None) -> list[dict]:
    files = sorted(nef_dir.glob("*.NEF"))
    recs, t0 = [], None
    for f in files:
        ts, exp = frame_time_and_exposure(f)
        t0 = ts if t0 is None else t0
        t = ts - t0
        if exclude_after_s is not None and t > exclude_after_s:
            continue
        y = relative_radiance(f, exp)
        prof = (y[rows[0]:rows[1]] - np.median(y)).mean(axis=0)
        sat_level = 65535.0 / exp
        rec = {"image": f.stem, "nef_sha256": sha256(f), "t_s": round(t, 3), "exposure_s": exp}
        for thr in THRESHOLDS:
            ok = thr < 0.9 * sat_level
            rec[f"x_px_thr_{thr:.0e}"] = leading_edge(prof, thr) if ok else None
        recs.append(rec)
    return recs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nef-dir", required=True, type=Path)
    ap.add_argument("--rows", nargs=2, type=int, required=True, help="row band (half-size px)")
    ap.add_argument("--t-window", nargs=2, type=float, required=True, help="fit interval, s from first frame")
    ap.add_argument("--exclude-after", type=float, default=80.0, help="drop frames after this time (post-burn)")
    ap.add_argument("--px-per-mm", type=float, required=True, help="half-size px/mm")
    ap.add_argument("--px-per-mm-rel-unc", type=float, required=True)
    ap.add_argument("--track-out", required=True, type=Path)
    ap.add_argument("--result-out", required=True, type=Path)
    a = ap.parse_args(argv)

    recs = track(a.nef_dir, tuple(a.rows), a.exclude_after)
    with open(a.track_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0]))
        w.writeheader()
        w.writerows(recs)

    per_thr = {}
    for thr in THRESHOLDS:
        k = f"x_px_thr_{thr:.0e}"
        pts = [(r["t_s"], r[k]) for r in recs if r[k] is not None and a.t_window[0] <= r["t_s"] <= a.t_window[1]]
        t, x = (np.array(v, float) for v in zip(*pts))
        b, se, res = linfit(t, x)
        per_thr[f"{thr:.0e}"] = {"n": len(t), "slope_px_s": round(b, 3), "slope_se_px_s": round(se, 3),
                                 "v_mm_s": round(b / a.px_per_mm, 4), "fit_se_mm_s": round(se / a.px_per_mm, 4),
                                 "resid_rms_px": round(float(res.std()), 2), "resid_max_px": round(float(abs(res).max()), 2)}
    v = np.array([d["v_mm_s"] for d in per_thr.values()])
    central = float(np.median(v))
    u_fit = float(max(d["fit_se_mm_s"] for d in per_thr.values()))
    u_thr = float((v.max() - v.min()) / 2)
    u_scale = central * a.px_per_mm_rel_unc
    u_tot = float(np.sqrt(u_fit ** 2 + u_thr ** 2 + u_scale ** 2))
    result = {
        "quantity": "opposed-flow flame spread rate, leading edge, top view",
        "evidence_status": "measured",
        "maturity": "provisional — scale plane correction pending (ISS-020)",
        "value_mm_s": round(central, 3),
        "standard_uncertainty_mm_s": round(u_tot, 3),
        "uncertainty_components_mm_s": {"fit": round(u_fit, 4), "threshold_sensitivity_half_range": round(u_thr, 4),
                                         "spatial_scale": round(u_scale, 4), "timing": "negligible (EXIF 0.01 s)"},
        "fit_window_s_from_first_frame": a.t_window,
        "row_band_half_px": a.rows,
        "px_per_mm_half_size": a.px_per_mm,
        "px_per_mm_rel_unc": a.px_per_mm_rel_unc,
        "thresholds_counts_per_s": list(THRESHOLDS),
        "per_threshold": per_thr,
        "input_frames": len(recs),
        "track_file": str(a.track_out),
    }
    a.result_out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("value_mm_s", "standard_uncertainty_mm_s", "uncertainty_components_mm_s")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
