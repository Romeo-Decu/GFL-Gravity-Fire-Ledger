#!/usr/bin/env python3
"""Export the B6 series the dashboard plots, and copy the sealed files it verifies.

- b6_series.json: per frame t, exposure, gate flags (R-W2 selection), leading edge at
  0.05 / 0.1 / 0.5 of frame peak and peak position, in mm from the first edge;
  the R-W2 segment fit and the robustness grid.
- files/<repo path>: byte copies of the repository files cited by the B6 storyline,
  so the browser can re-hash them against the ledger.

    python tools/build_dashboard_b6.py --profiles <B6_band_profiles.csv> --out visualization/data
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import b6_window_rule as w  # noqa: E402

PROFILES_SHA = "fece6e594aff18bdad49e63a8e01b485aa4c863a32c7b4ad0824edf8ac10be86"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    assert hashlib.sha256(a.profiles.read_bytes()).hexdigest() == PROFILES_SHA, "profile file hash mismatch"
    sel = json.loads((ROOT / "data/derived/B6_WINDOW_SELECTION_v2.json").read_text())
    rates = json.loads((ROOT / "data/derived/B6_SEGMENT_RATES_v2.json").read_text())
    rob = json.loads((ROOT / "data/derived/B6_WINDOW_ROBUSTNESS_v1.json").read_text())
    xval = json.loads((ROOT / "data/derived/WF0011_CROSS_VALIDATION_v0.1.json").read_text())
    with open(a.profiles, newline="") as f:
        rows = list(csv.reader(f))[1:]
    frames = []
    for r, s in zip(rows, sel["frames"]):
        assert r[0] == s["image"]
        p = np.array(r[1:], float)
        def mm(v):
            return None if v is None else round(v / w.PX_PER_MM, 3)
        frames.append({"image": s["image"], "t_s": s["t_s"], "exposure_s": s["exposure_s"],
                       "air": s["air_display"], "usable": s["usable"],
                       "gates": {g: s[g] for g in ("G1", "G2", "G3", "G4", "G5")},
                       "lead_mm": {str(fr): mm(w.lead_rel(p, fr)) for fr in (0.05, 0.1, 0.5)},
                       "peak_mm": mm(int(p.argmax())), "sat_px": s["sat_px"]})
    seg = next(x for x in rates["segments"] if x["fitted"])
    out = {"source": {"selection": "data/derived/B6_WINDOW_SELECTION_v2.json",
                      "rates": "data/derived/B6_SEGMENT_RATES_v2.json",
                      "robustness": "data/derived/B6_WINDOW_ROBUSTNESS_v1.json",
                      "profiles_sha256": PROFILES_SHA},
           "air_changes": sel["overlay_air_changes_s"], "frames": frames,
           "segment": {k: seg[k] for k in ("air_display", "t_start_s", "t_end_s", "frames", "definitions", "budget")},
           "union": {k: rates["union"][k] for k in ("t_range_s", "definitions")},
           "robustness": {"summary": rob["rate_rel_0.1_mm_s"], "grid": rob["grid"]},
           "cross_validation": {name: {"frames": e["frames"], "t_range_s": e["t_range_s"],
                                       "gfl_rel_0.1": e["gfl_definitions"]["rel_peak_0.1"].get("ols_mm_s"),
                                       "deepseek": e["blind_scripts"]["deepseek_v4"].get("SPREAD_RATE_MM_S"),
                                       "kimi_primary": e["blind_scripts"]["kimi26"].get("rate_ols_mm_s")}
                                for name, e in xval["sets"].items()},
           "headline": {"rate_mm_s": seg["budget"]["rate_mm_s"], "stat95": seg["budget"]["statistical_95_mm_s"],
                        "definitions_rel": [seg["definitions"]["rel_peak_0.1"]["ols_mm_s"],
                                            seg["definitions"]["rel_peak_0.5"]["ols_mm_s"]],
                        "rule_variants": [rob["rate_rel_0.1_mm_s"]["min"], rob["rate_rel_0.1_mm_s"]["max"]],
                        "superseded": {"value": 2.274, "pm": 0.094, "record": "RES-001"}}}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "b6_series.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    mem = json.loads((a.out / "experiment_memory.json").read_text())
    story_ids = {x for s in mem["storyline"]["steps"] for x in s["records"]}
    copied = 0
    for rec in mem["records"]:
        if rec["id"] not in story_ids:
            continue
        for h in rec["history"]:
            for f in h["files"]:
                src = ROOT / f["path"]
                if f["in_ledger"] and src.is_file() and src.stat().st_size < 2_000_000:
                    dst = a.out / "files" / f["path"]
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dst)
                    copied += 1
    print(json.dumps({"frames": len(frames), "files_copied": copied, "headline": out["headline"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
