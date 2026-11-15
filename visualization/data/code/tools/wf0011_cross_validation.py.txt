#!/usr/bin/env python3
"""WF-0011 LOCAL_VALIDATION: cross re-execution on identical frame sets.

Question (raised by red team grok47 and gpt55): is the gap between the blind
analyses (0.4-0.8 mm/s) and GFL (2.1-2.3 mm/s) caused by the frame/time window
rather than by the front definition?

Method
- Frame sets are cut in the DATA, never in the code. The blind scripts run
  unmodified (ISS-037: own empty dir, env -i, python3 -I, 120 s timeout, input
  hashes checked).
- The same frame sets are measured with GFL's front definitions applied to the
  same blind band profiles (so every method sees identical inputs):
  * leading edge relative to each frame's own peak (fractions 0.05/0.1/0.2/0.5),
  * leading edge at absolute radiance 2e5/5e5/1e6 counts/s,
  * peak-radiance position.
  Direction is INCREASING columns (determined in RES-001; agreed by kimi26 and by
  deepseek_v4's own front slope).
- Frame sets (t = seconds after the first frame):
  ALL      all 77 frames (includes the 106 s gap and 6 post-burn stills)
  PRE_GAP  t <= 72.9 s (71 frames, gap removed)
  ACTIVE   13 <= t <= 53 s (GFL's window)
  NOCLIP   17 < t < 52.5 s (ACTIVE minus frames with real flame clipping, RES-008)

Usage: python3 tools/wf0011_cross_validation.py BLIND_DIR SCRIPTS_DIR OUT_JSON
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

PX_PER_MM = 14.7
EXPECTED = {
    "B6_band_profiles.csv": "fece6e594aff18bdad49e63a8e01b485aa4c863a32c7b4ad0824edf8ac10be86",
    "B6_frames_metadata.csv": "767e0fa7e2b1f23b019bb1718fa7e4da4d7b4c91064f7efae694dba1f1143461",
}
SETS = {
    "ALL": lambda t: np.ones_like(t, dtype=bool),
    "PRE_GAP": lambda t: t <= 72.95,
    "ACTIVE": lambda t: (t >= 13) & (t <= 53),
    "NOCLIP": lambda t: (t > 17) & (t < 52.5),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def theil_sen(t, x):
    i, j = np.triu_indices(len(t), 1)
    dt = t[j] - t[i]
    ok = dt > 0
    return float(np.median((x[j] - x[i])[ok] / dt[ok]))


def fit(t, x):
    """OLS slope, R², Theil-Sen slope, all in mm/s."""
    ok = np.isfinite(x)
    t, x = t[ok], x[ok]
    if len(t) < 3:
        return {"n": int(len(t))}
    a, b = np.polyfit(t, x, 1)
    r2 = 1 - np.sum((x - (a * t + b)) ** 2) / np.sum((x - x.mean()) ** 2)
    return {
        "n": int(len(t)),
        "ols_mm_s": round(a / PX_PER_MM, 4),
        "r2": round(float(r2), 3),
        "theil_sen_mm_s": round(theil_sen(t, x) / PX_PER_MM, 4),
    }


def gfl_fronts(prof: np.ndarray) -> dict:
    """GFL front definitions on band profiles; direction = increasing columns."""
    out = {}
    peak_col = prof.argmax(axis=1)
    peak_val = prof.max(axis=1)
    out["peak_position"] = peak_col.astype(float)
    cols = np.arange(prof.shape[1])

    def leading(level):
        res = np.full(len(prof), np.nan)
        for k, row in enumerate(prof):
            lv = level[k] if np.ndim(level) else level
            above = np.where((row >= lv) & (cols >= peak_col[k]))[0]
            if len(above):
                res[k] = above.max()
        return res

    for f in (0.05, 0.1, 0.2, 0.5):
        out[f"rel_peak_{f}"] = leading(f * peak_val)
    for a in (2e5, 5e5, 1e6):
        out[f"abs_{a:.0e}"] = leading(a)
    return out


def run_blind(script: Path, meta: pd.DataFrame, prof: pd.DataFrame) -> dict:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        meta.to_csv(d / "B6_frames_metadata.csv", index=False)
        prof.to_csv(d / "B6_band_profiles.csv", index=False)
        shutil.copy(script, d / "script.py")
        try:
            p = subprocess.run(
                ["/usr/bin/env", "-i", "PATH=/usr/bin:/bin:/usr/local/bin",
                 "python3", "-I", "script.py"],
                cwd=d, capture_output=True, text=True, timeout=120,
            )
            return {"exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr[-2000:]}
        except subprocess.TimeoutExpired:
            return {"exit": "timeout", "stdout": "", "stderr": ""}


def parse_blind(name: str, stdout: str) -> dict:
    keys = {
        "kimi26": ["direction_conclusion", "rate_ols_mm_s", "rate_theil_sen_mm_s",
                   "rate_thr_5.0x_mad_ts_mm_s", "rate_thr_10.0x_mad_ts_mm_s"],
        "deepseek_v4": ["DIRECTION_MEAN_LAG", "SPREAD_RATE_MM_S",
                        "RATE_MEAN_ACROSS_THRESHOLDS"],
    }[name]
    found = {}
    for line in stdout.splitlines():
        for k in keys:
            for sep in (": ", "="):
                if line.startswith(k + sep):
                    found[k] = line.split(sep, 1)[1].strip()
    return found


def main():
    blind, scripts, out_json = map(Path, sys.argv[1:4])
    for f, h in EXPECTED.items():
        assert sha256(blind / f) == h, f"hash mismatch {f}"
    meta = pd.read_csv(blind / "B6_frames_metadata.csv")
    prof = pd.read_csv(blind / "B6_band_profiles.csv")
    assert (meta["image"].values == prof["image"].values).all()
    t_all = meta["unix_time_s"].values - meta["unix_time_s"].values[0]
    p_all = prof.drop(columns="image").values
    fronts = gfl_fronts(p_all)

    result = {"inputs": EXPECTED, "px_per_mm": PX_PER_MM, "sets": {}}
    for set_name, sel in SETS.items():
        m = sel(t_all)
        entry = {"frames": int(m.sum()),
                 "t_range_s": [round(float(t_all[m].min()), 2), round(float(t_all[m].max()), 2)],
                 "gfl_definitions": {k: fit(t_all[m], v[m]) for k, v in fronts.items()},
                 "blind_scripts": {}}
        for name in ("kimi26", "deepseek_v4"):
            r = run_blind(scripts / f"{name}_script.py",
                          meta[m].reset_index(drop=True), prof[m].reset_index(drop=True))
            entry["blind_scripts"][name] = {"exit": r["exit"], **parse_blind(name, r["stdout"])}
            if r["exit"] != 0:
                entry["blind_scripts"][name]["stderr_tail"] = r["stderr"]
        result["sets"][set_name] = entry
        print(set_name, json.dumps(entry, indent=1)[:4000])
    out_json.write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
