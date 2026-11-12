#!/usr/bin/env python3
"""Window rule R-W3: R-W2 with three declared changes (docs/WINDOW_RULE_R-W3.md).

1. G4 (continuity) is applied from the start of the burn record, not from the first frame:
   frames before the first flame-present frame (G1) are outside the record but do not break it;
   the record ends at the first gap > 5 s after it starts (ISS-044).
2. Reference definition: leading edge at 0.5 of each frame's peak (ISS-047). 0.8 is added to the
   relative definitions so the systematic term is symmetric around the reference.
3. Reported interval: the statistical 95 % interval of the reference widened, on each side, by the
   definition systematic s = max(|r(0.2) - r(0.5)|, |r(0.8) - r(0.5)|), combined in quadrature.
   The full range over all definitions is still reported separately.
Everything else (gates G1–G3, G5, segment minimums, estimators, bootstrap) is R-W2 unchanged; the
R-W2 code (tools/b6_window_rule.py) stays frozen and is imported, not edited.

    python tools/window_rule_r3.py select --nef-dir <dir> --overlay <csv> --out <json>
    python tools/window_rule_r3.py fit --nef-dir <dir> --selection <json> --out <json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from argparse import Namespace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b6_window_rule as wr  # noqa: E402

RULE = "R-W3"
REF_FRACTION = 0.5
REL_FRACTIONS = (0.05, 0.1, 0.2, 0.5, 0.8)
SYS_PAIR = (0.2, 0.8)


def apply_g4_from_burn_start(rows: list[dict]) -> None:
    """Recompute G4 and 'usable' in place: continuity counted from the first flame-present frame."""
    start = next((i for i, r in enumerate(rows) if r["G1"]), None)
    in_record = [False] * len(rows)
    if start is not None:
        in_record[start] = True
        for i in range(start + 1, len(rows)):
            if rows[i]["t_s"] - rows[i - 1]["t_s"] > wr.G4_MAX_GAP_S:
                break
            in_record[i] = True
    for r, ok in zip(rows, in_record):
        r["G4"] = ok
        r["usable"] = bool(r["G1"] and r["G2"] and r["G3"] and ok and r["G5"] and r["air_display"] is not None)


def segments_rw2(rows: list[dict], changes: list[tuple]) -> list[dict]:
    bounds = [-math.inf] + [c[0] for c in changes] + [math.inf]
    segs = []
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        s = [r for r in rows if r["usable"] and lo < r["t_s"] < hi]
        if s:
            span = s[-1]["t_s"] - s[0]["t_s"]
            segs.append({"air_display": s[0]["air_display"], "t_start_s": s[0]["t_s"], "t_end_s": s[-1]["t_s"],
                         "frames": len(s), "images": [r["image"] for r in s],
                         "fitted": len(s) >= wr.MIN_SEG_FRAMES and span >= wr.MIN_SEG_SPAN_S})
    return segs


def cmd_select(a) -> int:
    tmp = a.out.with_suffix(".rw2tmp.json")
    wr.cmd_select(Namespace(nef_dir=a.nef_dir, overlay=a.overlay, out=tmp, rule="R-W2"))
    sel = json.loads(tmp.read_text())
    tmp.unlink()
    rows = sel["frames"]
    apply_g4_from_burn_start(rows)
    changes = [(c["t_s"], c["from"], c["to"]) for c in sel["overlay_air_changes_s"]]
    sel["segments"] = segments_rw2(rows, changes)
    sel["rule"], sel["rule_doc"] = RULE, "docs/WINDOW_RULE_R-W3.md"
    sel["parameters"]["G4_applied_from"] = "first flame-present frame (G1)"
    a.out.write_text(json.dumps(sel, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"usable": sum(r["usable"] for r in rows),
                      "segments": [{k: v for k, v in s.items() if k != "images"} for s in sel["segments"]]}, indent=1))
    return 0


def cmd_fit(a) -> int:
    sel = json.loads(a.selection.read_text(encoding="utf-8"))
    frames = {fr["image"]: fr for fr in wr.frame_data(a.nef_dir)}
    for r in sel["frames"]:
        assert frames[r["image"]]["nef_sha256"] == r["nef_sha256"], r["image"]
    rng = np.random.default_rng(wr.BOOT_SEED)
    defs = {f"rel_peak_{f}": (lambda p, f=f: wr.lead_rel(p, f)) for f in REL_FRACTIONS}
    defs.update({f"abs_{th:.0e}": (lambda p, th=th: wr.lead_abs(p, th)) for th in wr.ABS_THRESHOLDS})
    defs["peak_position"] = lambda p: int(p.argmax())

    def measure(images):
        t = np.array([frames[i]["t_s"] for i in images])
        res = {}
        for name, fn in defs.items():
            x = np.array([np.nan if (v := fn(frames[i]["profile"])) is None else v for i in images], float)
            res[name] = wr.rate_block(t, x, rng)
        ref = res[f"rel_peak_{REF_FRACTION}"]
        if "ols_mm_s" not in ref:
            return {"t_range_s": [float(t.min()), float(t.max())], "frames": len(images), "definitions": res, "budget": None}
        r0 = ref["ols_mm_s"]
        s = max(abs(res[f"rel_peak_{f}"]["ols_mm_s"] - r0) for f in SYS_PAIR if "ols_mm_s" in res[f"rel_peak_{f}"])
        lo, hi = ref["boot95_mm_s"]
        total = [round(r0 - math.hypot(r0 - lo, s), 4), round(r0 + math.hypot(hi - r0, s), 4)]
        ols_vals = [v["ols_mm_s"] for v in res.values() if "ols_mm_s" in v]
        budget = {"reference_definition": f"rel_peak_{REF_FRACTION}", "rate_mm_s": r0,
                  "statistical_95_mm_s": [lo, hi], "definition_systematic_mm_s": round(s, 4),
                  "reported_interval_mm_s": total,
                  "definition_range_mm_s": [round(min(ols_vals), 4), round(max(ols_vals), 4)],
                  "scale_rel": wr.SCALE_REL_UNC, "parallax": "[UNKNOWN]", "luminous_vs_pyrolysis_offset": "[UNKNOWN]"}
        return {"t_range_s": [float(t.min()), float(t.max())], "frames": len(images), "definitions": res, "budget": budget}

    out = {"rule": RULE, "selection_file_sha256": hashlib.sha256(a.selection.read_bytes()).hexdigest(),
           "bootstrap": {"n": wr.BOOT_N, "seed": wr.BOOT_SEED, "type": "moving block, block = HAC lag"}, "segments": []}
    for s in sel["segments"]:
        entry = {k: s[k] for k in ("air_display", "t_start_s", "t_end_s", "frames", "fitted")}
        if s["fitted"]:
            entry.update(measure(s["images"]))
        out["segments"].append(entry)
    a.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps([{k: (v["rate_mm_s"], v["reported_interval_mm_s"], v["definition_systematic_mm_s"]) if k == "budget" and v else v
                       for k, v in s.items() if k in ("air_display", "t_start_s", "t_end_s", "frames", "budget")} for s in out["segments"]], indent=1))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--nef-dir", required=True, type=Path)
    s.add_argument("--overlay", required=True, type=Path)
    s.add_argument("--out", required=True, type=Path)
    f = sub.add_parser("fit")
    f.add_argument("--nef-dir", required=True, type=Path)
    f.add_argument("--selection", required=True, type=Path)
    f.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    return cmd_select(a) if a.cmd == "select" else cmd_fit(a)


if __name__ == "__main__":
    raise SystemExit(main())
