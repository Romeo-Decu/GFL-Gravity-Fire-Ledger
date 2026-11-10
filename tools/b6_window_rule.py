#!/usr/bin/env python3
"""B6 fit-window rule R-W1 (docs/B6_WINDOW_RULE_v1.md).

Two stages, run and committed separately so the commit order proves the rule
came first:

  select  per-frame gates G1-G5 and flow segments; computes NO slope.
  fit     rates per flow segment (primary) and on the union (secondary), with
          HAC and moving-block-bootstrap uncertainty and a component budget.

    python tools/b6_window_rule.py select --nef-dir <B6_NEF> \
        --overlay data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv \
        --out data/derived/B6_WINDOW_SELECTION_v1.json
    python tools/b6_window_rule.py fit --nef-dir <B6_NEF> \
        --selection data/derived/B6_WINDOW_SELECTION_v1.json \
        --out data/derived/B6_SEGMENT_RATES_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flame_front as ff  # noqa: E402

ROWS = (655, 1017)            # half-size slice; rows 655-1016 inclusive
PX_PER_MM = 14.7
SCALE_REL_UNC = 0.03
# R-W1 parameters (frozen; see docs/B6_WINDOW_RULE_v1.md)
G1_PEAK_OVER_NOISE = 20.0
G2_EDGE_MARGIN_COLS = 50
G3_SAT_FACTOR = 10.0
G4_MAX_GAP_S = 5.0
G5_FLOW_GUARD_S = 3.0
MIN_SEG_FRAMES = 6
MIN_SEG_SPAN_S = 6.0
REL_FRACTIONS = (0.05, 0.1, 0.2, 0.5)
ABS_THRESHOLDS = (2e5, 5e5, 1e6)
BOOT_N = 4000
BOOT_SEED = 20261110


def frame_data(nef_dir: Path):
    """Per-frame time, exposure, band profile and raw saturated-pixel count."""
    import rawpy
    out, t0 = [], None
    for f in sorted(nef_dir.glob("*.NEF")):
        ts, exp = ff.frame_time_and_exposure(f)
        t0 = ts if t0 is None else t0
        y = ff.relative_radiance(f, exp)
        prof = (y[ROWS[0]:ROWS[1]] - np.median(y)).mean(axis=0)
        with rawpy.imread(str(f)) as r:
            raw = r.raw_image_visible
            sat = int((raw[2 * ROWS[0]:2 * ROWS[1]] >= int(r.white_level) - 1).sum())
        out.append({"image": f.stem, "nef_sha256": ff.sha256(f), "t_s": round(ts - t0, 3),
                    "exposure_s": exp, "profile": prof, "sat_px": sat})
    return out


def lead_rel(prof: np.ndarray, frac: float) -> int | None:
    pk = int(prof.argmax())
    idx = np.flatnonzero(prof[pk:] >= frac * prof[pk])
    return int(pk + idx.max()) if idx.size else None


def lead_abs(prof: np.ndarray, thr: float) -> int | None:
    pk = int(prof.argmax())
    idx = np.flatnonzero(prof[pk:] >= thr)
    return int(pk + idx.max()) if idx.size else None


def air_at(overlay: list[tuple[float, int]], t: float) -> int | None:
    """AIR display value in force at still time t (last sample at or before t)."""
    val = None
    for ts, air in overlay:
        if ts <= t:
            val = air
    return val


def cmd_select(a) -> int:
    frames = frame_data(a.nef_dir)
    ov = []
    with open(a.overlay, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ov.append((float(r["still_t_s_est"]), int(r["AIR_display"])))
    ov.sort()
    # change times: midpoint between the two samples that differ
    changes = [((ov[i - 1][0] + ov[i][0]) / 2, ov[i - 1][1], ov[i][1])
               for i in range(1, len(ov)) if ov[i][1] != ov[i - 1][1]]
    sat_med = float(np.median([fr["sat_px"] for fr in frames]))
    ncols = len(frames[0]["profile"])
    rows, prev_t = [], None
    for fr in frames:
        p, t = fr["profile"], fr["t_s"]
        noise = 1.4826 * float(np.median(np.abs(p - np.median(p))))
        peak = float(p.max())
        g1 = noise > 0 and peak > G1_PEAK_OVER_NOISE * noise
        edge = lead_rel(p, 0.05) if g1 else None
        g2 = edge is not None and G2_EDGE_MARGIN_COLS <= edge <= ncols - 1 - G2_EDGE_MARGIN_COLS
        g3 = fr["sat_px"] <= G3_SAT_FACTOR * sat_med
        g4 = prev_t is None or (t - prev_t) <= G4_MAX_GAP_S
        g5 = all(abs(t - c[0]) > G5_FLOW_GUARD_S for c in changes)
        in_overlay = ov[0][0] <= t <= ov[-1][0] + 3.0
        air = air_at(ov, t) if in_overlay else None
        rows.append({"image": fr["image"], "nef_sha256": fr["nef_sha256"], "t_s": t,
                     "exposure_s": fr["exposure_s"], "peak_over_noise": round(peak / noise, 1) if noise > 0 else None,
                     "lead_0.05_col": edge, "sat_px": fr["sat_px"], "air_display": air,
                     "G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5, "in_overlay": in_overlay,
                     "usable": bool(g1 and g2 and g3 and g4 and g5 and air is not None)})
        prev_t = t
    # G4 is cumulative: once a >5 s gap occurs, every later frame is outside the continuous record
    broken = False
    for r in rows:
        broken = broken or not r["G4"]
        if broken:
            r["G4"] = False
            r["usable"] = False
    segs = []
    if a.rule == "R-W1":
        # R-W1 (frozen 2026-11-10): consecutive usable frames; any failed frame splits a segment
        cur = []
        for r in rows:
            if r["usable"] and cur and r["air_display"] == cur[-1]["air_display"]:
                cur.append(r)
            else:
                if cur:
                    segs.append(cur)
                cur = [r] if r["usable"] else []
        if cur:
            segs.append(cur)
    else:
        # R-W2: a segment is the interval between two AIR changes; frames that fail a gate are
        # dropped but do not split it (R-W1 defect: one clipped frame at 26.57 s split AIR=3)
        bounds = [-math.inf] + [c[0] for c in changes] + [math.inf]
        for lo, hi in zip(bounds[:-1], bounds[1:]):
            s = [r for r in rows if r["usable"] and lo < r["t_s"] < hi]
            if s:
                segs.append(s)
    seg_out = []
    for s in segs:
        span = s[-1]["t_s"] - s[0]["t_s"]
        seg_out.append({"air_display": s[0]["air_display"], "t_start_s": s[0]["t_s"], "t_end_s": s[-1]["t_s"],
                        "frames": len(s), "images": [r["image"] for r in s],
                        "fitted": len(s) >= MIN_SEG_FRAMES and span >= MIN_SEG_SPAN_S})
    out = {"rule": a.rule, "rule_doc": "docs/B6_WINDOW_RULE_v1.md",
           "parameters": {"G1_peak_over_noise": G1_PEAK_OVER_NOISE, "G2_edge_margin_cols": G2_EDGE_MARGIN_COLS,
                          "G3_sat_factor": G3_SAT_FACTOR, "sat_median_px": sat_med, "G4_max_gap_s": G4_MAX_GAP_S,
                          "G5_flow_guard_s": G5_FLOW_GUARD_S, "min_seg_frames": MIN_SEG_FRAMES,
                          "min_seg_span_s": MIN_SEG_SPAN_S, "rows_half_slice": list(ROWS)},
           "overlay_air_changes_s": [{"t_s": c[0], "from": c[1], "to": c[2]} for c in changes],
           "frames": rows, "segments": seg_out,
           "note": "selection only; no slope computed in this stage"}
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"usable": sum(r["usable"] for r in rows), "segments": [
        {k: v for k, v in s.items() if k != "images"} for s in seg_out],
        "air_changes": out["overlay_air_changes_s"]}, indent=1))
    return 0


def theil_sen(t, x):
    i, j = np.triu_indices(len(t), 1)
    dt = t[j] - t[i]
    ok = dt > 0
    return float(np.median((x[j] - x[i])[ok] / dt[ok]))


def ols(t, x):
    tm = t - t.mean()
    b = float((tm * (x - x.mean())).sum() / (tm ** 2).sum())
    return b, x - x.mean() - b * tm, tm


def hac_se(t, x, lag):
    b, e, tm = ols(t, x)
    s = (tm * e) ** 2
    s = s.sum()
    for l in range(1, lag + 1):
        w = 1 - l / (lag + 1)
        s += 2 * w * (tm[l:] * e[l:] * tm[:-l] * e[:-l]).sum()
    return math.sqrt(max(s, 0.0)) / (tm ** 2).sum()


def block_boot(t, x, lag, rng):
    n = len(t)
    nb = math.ceil(n / lag)
    starts_max = n - lag
    out = np.empty(BOOT_N)
    for k in range(BOOT_N):
        idx = np.concatenate([np.arange(s, s + lag) for s in rng.integers(0, starts_max + 1, nb)])[:n]
        tt, xx = t[idx], x[idx]
        if np.ptp(tt) == 0:
            out[k] = np.nan
            continue
        out[k] = ols(tt, xx)[0]
    return out[np.isfinite(out)]


def rate_block(t, x, rng):
    ok = np.isfinite(x)
    t, x = t[ok], x[ok]
    n = len(t)
    if n < 3:
        return {"n": n}
    lag = max(1, math.ceil(1.5 * n ** (1 / 3)))
    b, e, _ = ols(t, x)
    r2 = 1 - (e ** 2).sum() / ((x - x.mean()) ** 2).sum()
    ac1 = float(np.corrcoef(e[:-1], e[1:])[0, 1]) if n > 3 else None
    se_iid = math.sqrt((e ** 2).sum() / (n - 2) / ((t - t.mean()) ** 2).sum())
    boot = block_boot(t, x, lag, rng)
    q = np.percentile(boot, [2.5, 16, 84, 97.5])
    k = 1 / PX_PER_MM
    return {"n": n, "lag": lag, "ols_mm_s": round(b * k, 4), "theil_sen_mm_s": round(theil_sen(t, x) * k, 4),
            "r2": round(float(r2), 4), "resid_lag1_autocorr": round(ac1, 3) if ac1 is not None else None,
            "se_iid_mm_s": round(se_iid * k, 4), "se_hac_mm_s": round(hac_se(t, x, lag) * k, 4),
            "boot68_mm_s": [round(q[1] * k, 4), round(q[2] * k, 4)],
            "boot95_mm_s": [round(q[0] * k, 4), round(q[3] * k, 4)]}


def cmd_fit(a) -> int:
    sel = json.loads(a.selection.read_text(encoding="utf-8"))
    frames = {fr["image"]: fr for fr in frame_data(a.nef_dir)}
    for r in sel["frames"]:
        assert frames[r["image"]]["nef_sha256"] == r["nef_sha256"], r["image"]
    rng = np.random.default_rng(BOOT_SEED)
    defs = {f"rel_peak_{f}": (lambda p, f=f: lead_rel(p, f)) for f in REL_FRACTIONS}
    defs.update({f"abs_{th:.0e}": (lambda p, th=th: lead_abs(p, th)) for th in ABS_THRESHOLDS})
    defs["peak_position"] = lambda p: int(p.argmax())

    def measure(images):
        t = np.array([frames[i]["t_s"] for i in images])
        res = {}
        for name, fn in defs.items():
            x = np.array([np.nan if (v := fn(frames[i]["profile"])) is None else v for i in images], float)
            res[name] = rate_block(t, x, rng)
        ols_vals = [v["ols_mm_s"] for v in res.values() if "ols_mm_s" in v]
        ref = res["rel_peak_0.1"]
        stat95 = ref.get("boot95_mm_s")
        budget = {"reference_definition": "rel_peak_0.1",
                  "rate_mm_s": ref.get("ols_mm_s"),
                  "statistical_95_mm_s": stat95,
                  "definition_range_mm_s": [round(min(ols_vals), 4), round(max(ols_vals), 4)],
                  "scale_rel": SCALE_REL_UNC,
                  "scale_abs_mm_s": round(SCALE_REL_UNC * ref["ols_mm_s"], 4) if "ols_mm_s" in ref else None,
                  "parallax": "[UNKNOWN]", "luminous_vs_pyrolysis_offset": "[UNKNOWN]",
                  "exif_exposure": "qualifier: affects absolute thresholds only"}
        return {"t_range_s": [float(t.min()), float(t.max())], "frames": len(images), "definitions": res, "budget": budget}

    out = {"rule": sel["rule"], "selection_file_sha256": hashlib.sha256(a.selection.read_bytes()).hexdigest(),
           "bootstrap": {"n": BOOT_N, "seed": BOOT_SEED, "type": "moving block, block = HAC lag"},
           "segments": [], "union": None}
    for s in sel["segments"]:
        entry = {k: s[k] for k in ("air_display", "t_start_s", "t_end_s", "frames", "fitted")}
        if s["fitted"]:
            entry.update(measure(s["images"]))
        out["segments"].append(entry)
    union = [r["image"] for r in sel["frames"] if r["usable"]]
    out["union"] = measure(union)
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    brief = {"segments": [{k: (v if k != "definitions" else {d: (x.get("ols_mm_s"), x.get("boot95_mm_s")) for d, x in v.items()})
                           for k, v in s.items()} for s in out["segments"]],
             "union_budget": out["union"]["budget"], "union_t": out["union"]["t_range_s"]}
    print(json.dumps(brief, indent=1))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--nef-dir", required=True, type=Path)
    s.add_argument("--overlay", required=True, type=Path)
    s.add_argument("--out", required=True, type=Path)
    s.add_argument("--rule", choices=["R-W1", "R-W2"], default="R-W1")
    f = sub.add_parser("fit")
    f.add_argument("--nef-dir", required=True, type=Path)
    f.add_argument("--selection", required=True, type=Path)
    f.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    return cmd_select(a) if a.cmd == "select" else cmd_fit(a)


if __name__ == "__main__":
    raise SystemExit(main())
