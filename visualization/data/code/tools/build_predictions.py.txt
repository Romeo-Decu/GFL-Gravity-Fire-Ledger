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


def seg_dir(base: Path, run: str, air: int, tag: str) -> dict:
    d = json.loads((base / f"{run}_{tag}_RATES.json").read_text())
    s = next(s for s in d["segments"] if s["air_display"] == air and s.get("budget"))
    b = s["budget"]
    return {"air_display": air, "frames": s["frames"], "t_s": [s["t_start_s"], s["t_end_s"]], "rate_mm_s": b["rate_mm_s"],
            "interval_mm_s": b["reported_interval_mm_s"], "source": f"data/derived/rw4/{run}_{tag}_RATES.json"}


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
            p.update({"verdict": "not testable", "why": "R-W3 finds no usable frame in B11: the pre-burn reference still passes the brightness gate, so the burn record breaks at a 287 s gap (ISS-049). Under R-W4, declared and anchored afterwards to fix that gate, B11 becomes measurable; that result is shown separately and not counted."})
        else:
            r = m["rate_mm_s"] / ref["rate_mm_s"]
            p.update({"measured": m, "ratio": round(r, 3), "ratio_interval": [round(m["interval_mm_s"][0] / ref["interval_mm_s"][1], 3), round(m["interval_mm_s"][1] / ref["interval_mm_s"][0], 3)],
                      "verdict": "supported" if band[0] <= r <= band[1] else "not supported"})
        preds.append(p)
    preds[0]["why"] = "Run identity confirmed: the 51 stills match the B9 proof sheet exactly."
    preds[3]["why"] = (f"Ratio below the band; the interval ({preds[3]['ratio_interval'][0]:.2f}–{preds[3]['ratio_interval'][1]:.2f}, with the reference run's own uncertainty) does not exclude it. The edge of the 400 µm flame is broad and flickering "
                       "(r² 0.42 at the 0.5 reference), and the air display flickers between 3 and 2 inside the segment. Other airflow settings in the same run give 0.42–0.77 mm/s; the registered segment is kept. "
                       "The verdict depends on the front definition fixed beforehand (0.5 of peak): at 0.05, 0.1 and 0.2 of peak the ratio is 0.25, 0.26 and 0.23, inside the band (RES-039). "
                       "No explanation is claimed: the thin-fuel check finds no sign that this run alone became thermally thick (RES-043), and the table does not name its material as PMMA.")
    rw4 = ROOT / "data/derived/rw4"
    b11 = {a: seg_dir(rw4, "B11", a, "RW4") for a in (2, 0)}
    post = [{"id": "B11 under R-W4", "rule": "R-W4 (docs/WINDOW_RULE_R-W4.md), declared and anchored before this run; post-protocol",
             "display_2": b11[2], "display_0": b11[0], "ratio_display_2": round(b11[2]["rate_mm_s"] / ref["rate_mm_s"], 3),
             "ratio_interval_display_2": [round(b11[2]["interval_mm_s"][0] / ref["interval_mm_s"][1], 3), round(b11[2]["interval_mm_s"][1] / ref["interval_mm_s"][0], 3)],
             "display_0_slower_non_overlapping": b11[0]["interval_mm_s"][1] < b11[2]["interval_mm_s"][0],
             "note": "Information only: never counted as a supported prediction (the protocol fixed R-W3)."}]
    thick = {"B6": 100, "B9": 100, "B11": 200, "B13": 400}
    series = []
    for run, um in thick.items():
        d = json.loads((rw4 / f"{run}_RW4_RATES.json").read_text())
        for sg in d["segments"]:
            b = sg.get("budget")
            if b and b["reported_interval_mm_s"][0] > 0:
                series.append({"run": run, "thickness_um": um, "air_display": sg["air_display"], "frames": sg["frames"],
                               "rate_mm_s": b["rate_mm_s"], "interval_mm_s": b["reported_interval_mm_s"]})
    expo = json.loads((rw4 / "THICKNESS_EXPONENT_v1.json").read_text())
    sc = json.loads((ROOT / "data/derived/aal_test2/SCORES_v1.json").read_text())
    blind = [{"analyst": r["analyst"], "coverage": r["coverage"], "mean_rel_error": r["mean_rel_error"],
              "cases": {c: ({"speed": x["speed"], "ci95": x["ci95"], "covers": x["covers"]} if x else None) for c, x in r["cases"].items()}}
             for r in sc["rows"]]
    out = {"protocol": "docs/AAL_TEST2_PROTOCOL_v1.md", "registered": "2026-11-11, sealed and anchored before B9 and B13 were acquired and before R-W3 ran on real data",
           "rule": "R-W3 (docs/WINDOW_RULE_R-W3.md)", "reference": dict(ref, run="B6"), "predictions": preds, "post_protocol": post,
           "thickness_series": {"points": series, "note": "Every fitted segment with a positive lower bound, under R-W4 (identical to R-W3 except B11). Exploratory, not pre-registered: different air displays are shown together. B9 against B6 supports this at 100 µm; B13 does not establish it (0.42–0.77 mm/s across displays), and B11 is clearly slower at air display 0. Segments with a non-positive lower bound (B13 display 6) are left out of the plot, not of the data.",
                                "exponent": expo},
           "scorecard": {v: sum(p["verdict"] == v for p in preds) for v in ("supported", "not supported", "not testable")},
           "blind_test": {"name": "AAL test 2, synthetic cases with withheld truth", "truth_sha256": sc["truth_sha256"], "truth_mm_s": sc["truth_estimand_mm_s"],
                          "stress": {"T1": "asymmetric edge that sharpens", "T2": "edge that broadens, with flicker", "T3": "pre-burn frame and long gap",
                                     "T4": "luminous edge drifting relative to the true front"},
                          "rows": blind, "source": "data/derived/aal_test2/SCORES_v1.json",
                          "lesson": "Pooled coverage 15 of 24, below the 75 % threshold, driven by T4 (14 of 18 without it). In T4 every luminosity-based estimate, GFL's included, is 4–5 % high and only the widest interval covers the truth. GFL therefore reports luminous-edge rates, with intervals that exclude any change in the edge-to-front offset (ISS-050, DEC-056). An independent audit found a second, smaller instance the generator did not declare: in T1 the half-maximum edge runs 1.8 % faster than the true front, which explains two of the T1 misses (ISS-053)."}}
    (ROOT / "visualization/data/predictions.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(out["scorecard"], [(p["id"], p.get("ratio"), p["verdict"]) for p in preds])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
