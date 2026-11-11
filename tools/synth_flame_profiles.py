#!/usr/bin/env python3
"""Synthetic flame-spread profiles with a known front speed (ground truth for AAL test 1).

Builds band profiles in the same format as the blind B6 package (one row per frame, one value
per half-size column, relative radiance in counts/s, frame median removed), from a front whose
position is known exactly. The truth (speeds, seed, shape parameters) comes from a JSON file kept
outside the repository until scoring; only its SHA-256 is sealed beforehand.

Physical model (stated, not claimed to be the real flame):
  I(x, t) = A(t) · σ(-(x - xf(t)) / s(t)) · σ((x - xf(t) + L) / s_tr)
  σ = logistic; xf = leading-edge half-maximum, the "front" whose speed is the truth;
  s(t) = leading-edge scale (constant in S1, shrinking in S2 as observed in B6);
  L = luminous length behind the front; A(t) = brightness, with an ignition flash.
  Camera: raw = I · exposure (auto-exposure aims at a target level, discrete shutter values),
  Gaussian read noise and shot noise on raw, saturation at full well, then divided by exposure;
  band mean over rows reduces noise. Frame times: about 1 s with jitter, one long gap at the end.

    python tools/synth_flame_profiles.py --truth <truth.json> --out <dir>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

NCOLS = 2160
PX_PER_MM = 14.7
SHUTTERS = [1/3, 1/30, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000]


def logistic(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def front_position_mm(t: float, x0_mm: float, schedule: list[dict]) -> float:
    """Piecewise-linear front position: speed v_mm_s within each [t0, t1) interval."""
    x = x0_mm
    for seg in schedule:
        a, b = seg["t0"], seg["t1"]
        if t <= a:
            break
        x += seg["v_mm_s"] * (min(t, b) - a)
    return x


def build(truth: dict, case: str) -> dict:
    c = truth["cases"][case]
    rng = np.random.default_rng(truth["seed"] + c["seed_offset"])
    x = np.arange(NCOLS) / PX_PER_MM  # mm
    times, t = [], 0.0
    while t <= truth["t_burn_end_s"]:
        times.append(round(t, 2))
        t += 1.0 + float(rng.choice([0.0, 0.0, 0.0, 0.07]))
    times += [round(times[-1] + truth["late_gap_s"] + k, 2) for k in (0.0, 4.8)]  # two post-burn frames
    rows, truth_rows = [], []
    for i, ts in enumerate(times):
        burning = truth["t_ignition_s"] <= ts <= truth["t_burn_end_s"]
        xf = front_position_mm(ts, c["x0_mm"], c["schedule"])
        s = c["s_lead_mm"][0] + (c["s_lead_mm"][1] - c["s_lead_mm"][0]) * min(max((ts - c["s_t"][0]) / (c["s_t"][1] - c["s_t"][0]), 0), 1)
        A = c["A0"] * (1 + c["A_growth_per_s"] * max(ts - truth["t_ignition_s"], 0))
        if truth["t_ignition_s"] <= ts < truth["t_ignition_s"] + truth["flash_s"]:
            A *= truth["flash_factor"]
        I = A * logistic(-(x - xf) / s) * logistic((x - xf + c["L_mm"]) / c["s_trail_mm"]) if burning else np.zeros(NCOLS)
        I = I + truth["background"]
        level = I.max()
        exp = min(SHUTTERS, key=lambda e: abs(np.log(level * e / truth["target_raw"]))) if burning else SHUTTERS[0]
        raw = I * exp
        noise = rng.normal(0, np.sqrt(truth["read_noise"] ** 2 + truth["shot_k"] * np.maximum(raw, 0)), (truth["band_rows"], NCOLS))
        frame = raw[None, :] + noise
        sat = frame >= truth["full_well"]
        if i in c.get("clip_frames", []):  # deliberate over-exposure: the frame keeps a too-long shutter
            frame = (raw * 4)[None, :] + noise
            sat = frame >= truth["full_well"]
            exp = exp * 4
        frame = np.minimum(frame, truth["full_well"])
        prof = (frame / exp).mean(axis=0)
        prof = prof - np.median(prof)
        rows.append({"t": ts, "exposure_s": exp, "profile": prof, "sat_px": int(sat.sum())})
        truth_rows.append({"t_s": ts, "front_mm": round(xf, 4) if burning else None, "front_col": round(xf * PX_PER_MM, 2) if burning else None,
                           "s_lead_mm": round(s, 4), "burning": burning})
    return {"rows": rows, "truth_rows": truth_rows}


def write_package(truth: dict, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    side, summary = {}, {}
    for case in truth["cases"]:
        b = build(truth, case)
        with (out / f"{case}_frames_metadata.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["image", "t_s", "exposure_s"])
            for k, r in enumerate(b["rows"]):
                w.writerow([f"{case}_{k:03d}", f"{r['t']:.2f}", f"{r['exposure_s']:.6f}"])
        with (out / f"{case}_band_profiles.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["image"] + [f"c{j}" for j in range(NCOLS)])
            for k, r in enumerate(b["rows"]):
                w.writerow([f"{case}_{k:03d}"] + [f"{v:.6g}" for v in r["profile"]])
        with (out / f"{case}_flow_display.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t_s", "AIR_display"])
            for seg in truth["cases"][case]["schedule"]:
                w.writerow([f"{seg['t0']:.1f}", seg["air"]])
        side[case] = {"sat_px": [r["sat_px"] for r in b["rows"]], "truth_rows": b["truth_rows"]}
        summary[case] = len(b["rows"])
    files = sorted(p.name for p in out.glob("*.csv"))
    sums = {n: hashlib.sha256((out / n).read_bytes()).hexdigest() for n in files}
    (out / "SHA256SUMS").write_text("".join(f"{v}  {k}\n" for k, v in sums.items()))
    return {"frames": summary, "files": sums, "side": side}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--truth", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path, help="analyst package directory")
    ap.add_argument("--side", required=True, type=Path, help="GFL-only side file (saturation counts, per-frame truth)")
    a = ap.parse_args(argv)
    truth = json.loads(a.truth.read_text())
    res = write_package(truth, a.out)
    a.side.write_text(json.dumps(res["side"], indent=1) + "\n")
    print(json.dumps({"frames": res["frames"], "files": res["files"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
