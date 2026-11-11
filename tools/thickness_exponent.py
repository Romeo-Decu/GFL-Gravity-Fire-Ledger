#!/usr/bin/env python3
"""Exploratory fit of spread rate against film thickness, V ∝ τ^n (not pre-registered; RES-038).

Weighted least squares of ln V on ln τ, weights from each reported interval (σ_lnV = ln(hi/lo) / (2·1.96)),
95 % interval on n from the t distribution with N−2 degrees of freedom and the weighted residual scale.
Run for both B13 segment choices, because the result depends on it.

    python tools/thickness_exponent.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RW4 = ROOT / "data/derived/rw4"
T975 = {2: 4.303, 3: 3.182, 4: 2.776}


def point(run: str, air: int) -> tuple[float, float, float]:
    s = next(s for s in json.loads((RW4 / f"{run}_RW4_RATES.json").read_text())["segments"] if s["air_display"] == air and s.get("budget"))
    b = s["budget"]
    return b["rate_mm_s"], *b["reported_interval_mm_s"]


def fit(pts: list[tuple[float, float, float, float]]) -> dict:
    x = np.log([p[0] for p in pts])
    y = np.log([p[1] for p in pts])
    sig = np.array([math.log(p[3] / p[2]) / (2 * 1.96) for p in pts])
    w = 1 / sig ** 2
    X = np.column_stack([np.ones_like(x), x])
    cov = np.linalg.inv(X.T @ (w[:, None] * X))
    beta = cov @ X.T @ (w * y)
    dof = len(pts) - 2
    chi2 = float(np.sum(w * (y - X @ beta) ** 2))
    scale = max(1.0, chi2 / dof)  # never shrink the interval below the measurement errors
    se = math.sqrt(cov[1, 1] * scale)
    ols = np.polyfit(x, y, 1)[0]
    return {"n_weighted": round(float(beta[1]), 3), "se": round(se, 3), "ci95": [round(float(beta[1]) - T975[dof] * se, 3), round(float(beta[1]) + T975[dof] * se, 3)],
            "chi2_per_dof": round(chi2 / dof, 2), "n_unweighted_ols": round(float(ols), 3), "points": len(pts)}


def main() -> int:
    base = [(100, *point("B6", 3)), (100, *point("B9", 2)), (200, *point("B11", 2))]
    out = {"note": "exploratory, not pre-registered; mixes air displays; inverse-thickness law is n = -1",
           "B13_display_3": fit(base + [(400, *point("B13", 3))]), "B13_display_4": fit(base + [(400, *point("B13", 4))])}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
