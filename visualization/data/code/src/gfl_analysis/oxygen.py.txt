"""A8. Oxygen sensitivity of the spread rate, from measured runs only (exploratory, not pre-registered).

Compares runs of the same recorded material and thickness at two initial oxygen levels and reports
  ratio      = rate(low O2) / rate(reference O2), with the interval of both runs carried into it
  exponent n = ln(ratio) / ln(X_low / X_ref), the local power law  rate ~ X_O2^n
No flame temperature is assumed: GFL has no sourced value below 21 %. For the thin-fuel thermal formula
(cram1), where oxygen enters only through F = (T_f - T_v)/(T_v - T_inf), the measured ratio is therefore
reported as the constraint F(low)/F(ref) would have to meet, not as a test the formula passed or failed.
Limits stated with every result: the flow differs between the runs, each condition was flown once, and the
rates are luminous-edge rates.
"""
from __future__ import annotations

import math


def _ratio(seg: dict, ref: dict) -> dict:
    r = seg["rate_mm_s"] / ref["rate_mm_s"]
    lo, hi = seg["interval_mm_s"][0] / ref["interval_mm_s"][1], seg["interval_mm_s"][1] / ref["interval_mm_s"][0]
    return {"ratio": round(r, 3), "ratio_interval": [round(lo, 3), round(hi, 3)]}


def sensitivity(ref: dict, low: list[dict]) -> dict:
    """ref: {run, o2_pct, air_display, rate_mm_s, interval_mm_s}; low: the same keys for each segment at the other oxygen level."""
    rows = []
    for s in low:
        if not s.get("o2_pct") or not ref.get("o2_pct") or s["o2_pct"] == ref["o2_pct"] or s["interval_mm_s"][0] <= 0:
            continue
        q = _ratio(s, ref)
        lx = math.log(s["o2_pct"] / ref["o2_pct"])
        n = sorted(math.log(v) / lx for v in q["ratio_interval"])
        rows.append({"run": s["run"], "o2_pct": s["o2_pct"], "air_display": s["air_display"], "flow_cm_s": s.get("flow_cm_s"), "frames": s.get("frames"),
                     "rate_mm_s": s["rate_mm_s"], "interval_mm_s": s["interval_mm_s"], **q,
                     "exponent": round(math.log(q["ratio"]) / lx, 2), "exponent_interval": [round(n[0], 2), round(n[1], 2)],
                     "excludes_no_change": q["ratio_interval"][1] < 1})
    firm = [r for r in rows if r["excludes_no_change"]]
    return {"status": "exploratory, not pre-registered: the runs were measured before this comparison was written",
            "reference": ref, "segments": rows,
            "summary": {"segments": len(rows), "slower_beyond_both_intervals": len(firm),
                        "ratio_range": [min(r["ratio"] for r in firm), max(r["ratio"] for r in firm)] if firm else None,
                        "exponent_range": [min(r["exponent"] for r in firm), max(r["exponent"] for r in firm)] if firm else None},
            "constraint_on_theory": "In the thin-fuel thermal formula oxygen enters only through F = (T_f - T_v)/(T_v - T_inf). To reproduce these rates, F at the lower oxygen level "
                                    "would have to be the stated ratio times its value at the reference level. GFL has no sourced flame temperature below 21 %, so this is a constraint, not a test.",
            "limits": ["the forced flow differs between the reference and the low-oxygen segments", "one flight per condition", "luminous-edge rates; a dimmer flame may shift the edge relative to the front",
                       "two oxygen levels only: the exponent is a local slope, not a law"]}
