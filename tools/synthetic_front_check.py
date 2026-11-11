#!/usr/bin/env python3
"""Run GFL's frozen B6 window rule (tools/b6_window_rule.py, R-W2) on a synthetic package.

Mechanical adapter only: frames come from the package CSVs instead of NEF files, saturation
counts from the generator's side file, and the flow display is sampled once per second from
the package's schedule (as the B6 overlay was sampled from video). No parameter of the rule or
of the estimators is changed. Scoring against the truth happens in a separate step.

    python tools/synthetic_front_check.py --package <dir> --side <side.json> --case S1 --out-dir <dir>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from argparse import Namespace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b6_window_rule as wr  # noqa: E402


def load_frames(package: Path, side: dict, case: str) -> list[dict]:
    meta = list(csv.DictReader((package / f"{case}_frames_metadata.csv").open()))
    profs = {r[0]: np.array(r[1:], float) for r in csv.reader((package / f"{case}_band_profiles.csv").open()) if r[0] != "image"}
    out = []
    for k, m in enumerate(meta):
        p = profs[m["image"]]
        out.append({"image": m["image"], "nef_sha256": hashlib.sha256(p.tobytes()).hexdigest(), "t_s": float(m["t_s"]),
                    "exposure_s": float(m["exposure_s"]), "profile": p, "sat_px": side[case]["sat_px"][k]})
    return out


def overlay_csv(package: Path, case: str, t_max: float, out: Path) -> Path:
    sched = [(float(r["t_s"]), int(r["AIR_display"])) for r in csv.DictReader((package / f"{case}_flow_display.csv").open())]
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["still_t_s_est", "AIR_display"])
        t = 0.0
        while t <= t_max:
            w.writerow([f"{t:.1f}", [a for t0, a in sched if t0 <= t][-1]])
            t += 1.0
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True, type=Path)
    ap.add_argument("--side", required=True, type=Path)
    ap.add_argument("--case", required=True)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--rule", choices=["R-W2", "R-W3"], default="R-W2")
    a = ap.parse_args(argv)
    a.out_dir.mkdir(parents=True, exist_ok=True)
    frames = load_frames(a.package, json.loads(a.side.read_text()), a.case)
    burn_end = max(fr["t_s"] for fr in frames)
    wr.frame_data = lambda _nef_dir: frames  # the only substitution
    ov = overlay_csv(a.package, a.case, burn_end, a.out_dir / f"{a.case}_overlay.csv")
    tag = "" if a.rule == "R-W2" else "_rw3"
    sel = a.out_dir / f"{a.case}{tag}_selection.json"
    if a.rule == "R-W2":
        wr.cmd_select(Namespace(nef_dir=None, overlay=ov, out=sel, rule="R-W2"))
        wr.cmd_fit(Namespace(nef_dir=None, selection=sel, out=a.out_dir / f"{a.case}_rates.json"))
    else:
        import window_rule_r3 as r3
        r3.cmd_select(Namespace(nef_dir=None, overlay=ov, out=sel))
        r3.cmd_fit(Namespace(nef_dir=None, selection=sel, out=a.out_dir / f"{a.case}{tag}_rates.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
