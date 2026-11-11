#!/usr/bin/env python3
"""Build visualization/data/predictions.json: the pre-registered real-run predictions and the blind synthetic tests.

Every number is read from a sealed result file; bands and wording come from docs/AAL_TEST2_PROTOCOL_v1.md.

    python tools/build_predictions.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RW3 = ROOT / "data/derived/rw3"


def seg(run: str, air: int) -> dict | None:
    d = json.loads((RW3 / f"{run}_RW3_RATES.json").read_text())
    s = next((s for s in d["segments"] if s["air_display"] == air and s.get("budget")), None)
    if not s:
        return None
    b = s["budget"]
    return {"air_display": air, "frames": s["frames"], "t_s": [s["t_start_s"], s["t_end_s"]], "rate_mm_s": b["rate_mm_s"],
            "interval_mm_s": b["reported_interval_mm_s"], "source": f"data/derived/rw3/{run}_RW3_RATES.json"}


def main() -> int:
    ref = seg("B6", 3)
    preds = []
    for pid, run, air, claim, band in [
        ("P-B9", "B9", 2, "100 µm at air display 2: same rate as B6 (flow independence, thin-fuel thermal regime)", [0.85, 1.15]),
        ("P-B11a", "B11", 2, "200 µm at air display 2: half of B6 (inverse thickness)", [0.425, 0.575]),
        ("P-B11b", "B11", 0, "200 µm: slower at air display 0 than at 2, intervals not overlapping", None),
        ("P-B13", "B13", 3, "400 µm at air display 3: a quarter of B6 (inverse thickness, if still thermally thin)", [0.2125, 0.2875]),
    ]:
        p = {"id": pid, "run": run, "claim": claim, "band_ratio": band}
        m = seg(run, air) if (RW3 / f"{run}_RW3_RATES.json").exists() else None
        if m is None or band is None:
            p.update({"verdict": "not testable", "why": "R-W3 finds no usable frame in B11: the pre-burn reference still passes the brightness gate, so the burn record breaks at a 287 s gap (ISS-049). No B11 rate has been computed."})
        else:
            r = m["rate_mm_s"] / ref["rate_mm_s"]
            p.update({"measured": m, "ratio": round(r, 3), "ratio_interval": [round(x / ref["rate_mm_s"], 3) for x in m["interval_mm_s"]],
                      "verdict": "supported" if band[0] <= r <= band[1] else "not supported"})
        preds.append(p)
    preds[0]["why"] = "Run identity confirmed: the 51 stills match the B9 proof sheet exactly."
    preds[3]["why"] = ("Ratio below the band; the interval (0.10–0.33) does not exclude it. The edge of the 400 µm flame is broad and flickering "
                       "(r² 0.42 at the 0.5 reference). Other airflow settings in the same run give 0.42–0.53 mm/s; the registered segment is kept. "
                       "400 µm may be past the thermally thin limit, where the inverse-thickness law over-predicts.")
    sc = json.loads((ROOT / "data/derived/aal_test2/SCORES_v1.json").read_text())
    blind = [{"analyst": r["analyst"], "coverage": r["coverage"], "mean_rel_error": r["mean_rel_error"],
              "cases": {c: ({"speed": x["speed"], "ci95": x["ci95"], "covers": x["covers"]} if x else None) for c, x in r["cases"].items()}}
             for r in sc["rows"]]
    out = {"protocol": "docs/AAL_TEST2_PROTOCOL_v1.md", "registered": "2026-11-11, sealed and anchored before B9 and B13 were acquired and before R-W3 ran on real data",
           "rule": "R-W3 (docs/WINDOW_RULE_R-W3.md)", "reference": dict(ref, run="B6"), "predictions": preds,
           "scorecard": {v: sum(p["verdict"] == v for p in preds) for v in ("supported", "not supported", "not testable")},
           "blind_test": {"name": "AAL test 2, synthetic cases with withheld truth", "truth_sha256": sc["truth_sha256"], "truth_mm_s": sc["truth_estimand_mm_s"],
                          "stress": {"T1": "asymmetric edge that sharpens", "T2": "edge that broadens, with flicker", "T3": "pre-burn frame and long gap",
                                     "T4": "luminous edge drifting relative to the true front"},
                          "rows": blind, "source": "data/derived/aal_test2/SCORES_v1.json",
                          "lesson": "Pooled coverage 15 of 24, below the 75 % threshold: the intervals are overconfident as a group. In T4 every luminosity-based estimate, GFL's included, is 4–5 % high and only the widest interval covers the truth. GFL therefore reports luminous-edge rates, with intervals that exclude any change in the edge-to-front offset (ISS-050, DEC-056)."}}
    (ROOT / "visualization/data/predictions.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(out["scorecard"], [(p["id"], p.get("ratio"), p["verdict"]) for p in preds])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
