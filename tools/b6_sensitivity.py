"""B6 robustness analysis requested by the red-team review (RES-005).

Questions answered, all on the same original NEF frames:
  Q1 front definition  - leading edge at 3 absolute + 3 relative thresholds, peak-radiance
                         position, radiance-weighted centroid;
  Q2 fit window        - every window with start 8..25 s, end 40..60 s, length >= 20 s
                         (no window chosen by looking at the slope), plus the predeclared
                         20-80 %-of-travel rule used for the family;
  Q3 statistics        - residual lag-1 autocorrelation, Durbin-Watson, moving-block
                         bootstrap slope SE (block 5 frames) vs ordinary least-squares SE;
  Q5 brightness       - per-frame relative thresholds (fraction of each frame's own peak), invariant
                         to the flame brightening during the window; peak radiance vs time reported.
  Q4 exposure          - exposure varies 1/400-1/60 s inside the window: residual vs log(exposure)
                         correlation, and the fit on the modal exposure (1/250 s) frames only.

    python tools/b6_sensitivity.py --nef-dir <FIF_DATA>/derived/b6_nef --out data/derived/B6_SENSITIVITY_v0.1.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import flame_front as ff

ROWS = (655, 1017)
PX_PER_MM = 14.7          # half-size, as in RES-001
EXCLUDE_AFTER = 80.0
ABS_THR = (2e5, 5e5, 1e6)
REL_THR = (0.1, 0.2, 0.4)
RNG = np.random.default_rng(20261105)   # fixed seed: reproducible bootstrap


def profiles(nef_dir: Path):
    out, t0 = [], None
    for f in sorted(nef_dir.glob("*.NEF")):
        ts, exp = ff.frame_time_and_exposure(f)
        t0 = ts if t0 is None else t0
        if ts - t0 > EXCLUDE_AFTER:
            continue
        y = ff.relative_radiance(f, exp)
        out.append({"t": ts - t0, "exp": exp, "p": (y[ROWS[0]:ROWS[1]] - np.median(y)).mean(axis=0),
                    "sat": 65535.0 / exp})
    return out


def fronts(pr):
    pmax = float(np.median([d["p"].max() for d in pr]))
    defs = {}
    for thr in ABS_THR:
        defs[f"leading_edge_abs_{thr:.0e}"] = [(d["t"], ff.leading_edge(d["p"], thr) if thr < 0.9 * d["sat"] else None, d["exp"]) for d in pr]
    for r in REL_THR:
        defs[f"leading_edge_rel_{r}"] = [(d["t"], ff.leading_edge(d["p"], r * pmax), d["exp"]) for d in pr]
    for r in (0.05, 0.1, 0.2, 0.3, 0.5):      # threshold relative to EACH frame's own peak (brightness-invariant)
        defs[f"leading_edge_frame_rel_{r}"] = [(d["t"], ff.leading_edge(d["p"], r * d["p"].max()), d["exp"]) for d in pr]
    defs["peak_radiance"] = [(d["t"], int(np.argmax(d["p"])) if d["p"].max() > 0.1 * pmax else None, d["exp"]) for d in pr]
    cen = []
    for d in pr:
        w = np.clip(d["p"], 0, None)
        cen.append((d["t"], float((w * np.arange(w.size)).sum() / w.sum()) if d["p"].max() > 0.1 * pmax else None, d["exp"]))
    defs["radiance_centroid"] = cen
    return {k: [(t, x, e) for t, x, e in v if x is not None] for k, v in defs.items()}


def fit(pts, lo, hi):
    s = [(t, x) for t, x, _ in pts if lo <= t <= hi]
    if len(s) < 6:
        return None
    t, x = (np.array(v, float) for v in zip(*s))
    b, se, res = ff.linfit(t, x)
    return b / PX_PER_MM, se / PX_PER_MM, res, t, x


def block_bootstrap_se(t, x, block=5, n=2000):
    a = np.vstack([t, np.ones_like(t)]).T
    coef, *_ = np.linalg.lstsq(a, x, rcond=None)
    fitted, res = a @ coef, x - a @ coef
    k = int(np.ceil(len(t) / block))
    slopes = []
    for _ in range(n):
        idx = np.concatenate([np.arange(s, s + block) for s in RNG.integers(0, len(t) - block + 1, k)])[:len(t)]
        xb = fitted + res[idx]
        slopes.append(np.linalg.lstsq(a, xb, rcond=None)[0][0])
    return float(np.std(slopes)) / PX_PER_MM


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nef-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    pr = profiles(a.nef_dir)
    F = fronts(pr)
    out = {"rules": __doc__.split("Questions answered, all on the same original NEF frames:")[1].split("python tools")[0].strip(),
           "frames": len(pr), "px_per_mm_half": PX_PER_MM, "row_band_half_px": list(ROWS), "front_definitions": {}}
    for name, pts in F.items():
        base = fit(pts, 13, 53)
        rec = {"n_points": len(pts)}
        if base:
            v, se, res, t, x = base
            r1 = float(np.corrcoef(res[:-1], res[1:])[0, 1])
            dw = float(np.sum(np.diff(res) ** 2) / np.sum(res ** 2))
            rec["reference_window_13_53_s"] = {"v_mm_s": round(v, 4), "ols_se_mm_s": round(se, 4),
                                               "block_bootstrap_se_mm_s": round(block_bootstrap_se(t, x), 4),
                                               "residual_lag1_autocorr": round(r1, 3), "durbin_watson": round(dw, 2),
                                               "resid_rms_px": round(float(res.std()), 2)}
            ex = np.array([e for tt, xx, e in pts if 13 <= tt <= 53])
            rec["reference_window_13_53_s"]["residual_vs_log_exposure_corr"] = round(float(np.corrcoef(res, np.log(ex))[0, 1]), 3)
            nb = [(tt, xx, e) for tt, xx, e in pts if abs(e - 0.004) < 1e-6]
            b2 = fit(nb, 13, 53)
            if b2:
                rec["reference_window_single_exposure_1_250_s_only"] = {"v_mm_s": round(b2[0], 4), "n": len(b2[3])}
        vs = []
        for lo in range(8, 26):
            for hi in range(40, 61):
                if hi - lo >= 20:
                    r = fit(pts, lo, hi)
                    if r:
                        vs.append(r[0])
        if vs:
            vs = np.array(vs)
            rec["all_windows"] = {"n_windows": int(vs.size), "min": round(float(vs.min()), 3), "p05": round(float(np.percentile(vs, 5)), 3),
                                  "median": round(float(np.median(vs)), 3), "p95": round(float(np.percentile(vs, 95)), 3),
                                  "max": round(float(vs.max()), 3)}
        t = np.array([p[0] for p in pts]); x = np.array([p[1] for p in pts], float)
        lo_x, hi_x = np.percentile(x, 5), np.percentile(x, 95)
        m = (x >= lo_x + 0.2 * (hi_x - lo_x)) & (x <= lo_x + 0.8 * (hi_x - lo_x))
        if m.sum() >= 6:
            b, se, _ = ff.linfit(t[m], x[m])
            rec["predeclared_20_80_travel_rule"] = {"v_mm_s": round(b / PX_PER_MM, 4), "n": int(m.sum()),
                                                    "t_window_s": [round(float(t[m].min()), 2), round(float(t[m].max()), 2)]}
        out["front_definitions"][name] = rec
    pk = [(d["t"], float(d["p"].max())) for d in pr if 13 <= d["t"] <= 53]
    tt, pp = np.array(pk).T
    out["brightness"] = {"peak_vs_time_corr": round(float(np.corrcoef(tt, pp)[0, 1]), 3),
                         "peak_ratio_last5_first5": round(float(pp[-5:].mean() / pp[:5].mean()), 2),
                         "camera": "ISO 1000 and f/2 fixed, aperture priority: shutter shortens as the scene brightens"}
    fr = [d["reference_window_13_53_s"]["v_mm_s"] for k, d in out["front_definitions"].items()
          if k.startswith("leading_edge_frame_rel") and "reference_window_13_53_s" in d]
    le = [d["reference_window_13_53_s"]["v_mm_s"] for k, d in out["front_definitions"].items()
          if k.startswith("leading_edge") and "reference_window_13_53_s" in d]
    allw = [d["all_windows"] for k, d in out["front_definitions"].items() if k.startswith("leading_edge") and "all_windows" in d]
    out["summary"] = {"leading_edge_per_frame_relative_range_mm_s": [min(fr), max(fr)],
                      "leading_edge_definitions_reference_window_range_mm_s": [min(le), max(le)],
                      "leading_edge_all_windows_p05_p95_mm_s": [min(w["p05"] for w in allw), max(w["p95"] for w in allw)]}
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["summary"]))
    for k, d in out["front_definitions"].items():
        r = d.get("reference_window_13_53_s", {})
        print(f"{k:28s} v={r.get('v_mm_s')} ols={r.get('ols_se_mm_s')} boot={r.get('block_bootstrap_se_mm_s')} "
              f"r1={r.get('residual_lag1_autocorr')} DW={r.get('durbin_watson')} win={d.get('all_windows', {}).get('p05')}-{d.get('all_windows', {}).get('p95')} "
              f"rule={d.get('predeclared_20_80_travel_rule', {}).get('v_mm_s')} exp1/250={d.get('reference_window_single_exposure_1_250_s_only', {}).get('v_mm_s')} r_exp={r.get('residual_vs_log_exposure_corr')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
