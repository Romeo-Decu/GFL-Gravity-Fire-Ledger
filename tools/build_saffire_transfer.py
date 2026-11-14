#!/usr/bin/env python3
"""A transfer worked end to end between two NASA investigations, from NASA's run tables (RES-059).

Question: Saffire-II burned 5 cm wide strips of SIBAL fabric; Saffire-I burned the same fabric 40.6 cm wide.
Does the small-sample spread rate inform the large one? Record text could not say (evidence map, three extractors).
Here the run-level experimental tables are read instead. Every number is NASA's, as printed in those tables, or is
derived from them by the arithmetic shown; GFL measured nothing from the Saffire images.

    python tools/build_saffire_transfer.py --src "$FIF_DATA/psi_tables" --out data/derived/evidence_map/SAFFIRE_TRANSFER_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fif_transfer.engine import assess  # noqa: E402

T1, T2 = "PSI-98_Experimental table_SAFFIRE-1.csv", "PSI-99_Experimental table_SAFFIRE-2.csv"
RULESET = ROOT / "configs/SAFFIRE_SIBAL_RULESET_v0.1.json"


def table(path: Path) -> list[dict]:
    rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="replace", newline="")))
    head = [h.strip() for h in rows[0]]
    return [dict(zip(head, (c.strip() for c in r))) for r in rows[1:] if any(c.strip() for c in r)]


def numbers(text: str) -> list[float]:
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text or "")]


def _g(status, reasons, refs, rules):
    return {"status": status, "reasons": reasons, "evidence_refs": refs, "rule_ids": rules}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--page", type=Path, help="also write the copy the dashboard reads")
    a = ap.parse_args(argv)
    sha = {n: hashlib.sha256((a.src / n).read_bytes()).hexdigest() for n in (T1, T2)}
    s1 = next(r for r in table(a.src / T1) if r["Sample Number"] == "S1")
    t2 = table(a.src / T2)
    k2 = lambda r, start: next(v for k, v in r.items() if k.startswith(start))  # noqa: E731  (headers carry stray spaces and one replaced character)
    small = []
    for i, r in enumerate(t2):
        mat = r["Material"] or (t2[i - 1]["Material"] if i else "")
        if "SIBAL" not in mat or r["Flow Direction"] != "Concurrent":
            continue
        length_cm, burn_s = numbers(r["?-g Burn Length"] if "?-g Burn Length" in r else k2(r, "?-g Burn"))[0], numbers(r["Burn Time (s)"])[0]
        rep = numbers(k2(r, "?-g Spread"))[0]
        small.append({"sample": r["Sample Number"], "material_as_recorded": r["Material"] or None, "material_read_as": mat,
                      "thickness_as_recorded": k2(r, "Samle Thickness"), "width_cm": numbers(r["Sample Width (cm)"])[0], "length_cm": numbers(k2(r, "Sample Length"))[0],
                      "flow_cm_s": numbers(r["Air Flow (cm/s)"])[0], "o2_pct_as_recorded": r["Percent O2 (Note 1)"], "o2_pct": numbers(r["Percent O2 (Note 1)"]),
                      "direction": r["Flow Direction"], "burn_length_cm": length_cm, "burn_time_s": burn_s,
                      "spread_rate_reported_mm_s": rep, "average_rate_derived_mm_s": round(10 * length_cm / burn_s, 3), "derived_over_reported": round(10 * length_cm / burn_s / rep, 3)})
    big = {"sample": "S1", "material_as_recorded": s1["Material"], "thickness_as_recorded": s1["Sample Thickness (cm)"] + " (column headed cm)",
           "width_as_recorded": s1["Sample Width (cm)"], "length_as_recorded": s1["Sample Length (cm)"], "flow_cm_s": numbers(s1["Air Flow (cm/s)"])[0],
           "o2_pct_as_recorded": s1["Percent O2"], "o2_pct": numbers(s1["Percent O2"]), "direction": s1["Flow Direction"], "burn_time_s": numbers(s1["Burn Time (s)"])[0]}
    # the two dimensions of the large sample: NASA's operations note gives 0.4 m wide by 0.94 m tall; the table lists them under the opposite headers
    dims = sorted(numbers(s1["Sample Width (cm)"]) + numbers(s1["Sample Length (cm)"]))
    big["width_cm"], big["length_cm"] = dims[0], dims[1]
    big["average_rate_derived_mm_s"] = round(10 * big["length_cm"] / big["burn_time_s"], 3)
    rep = [s["spread_rate_reported_mm_s"] for s in small]
    der = [s["average_rate_derived_mm_s"] for s in small]
    proxy = {"what": "burn length divided by burn time, against the spread rate NASA reports, on the samples where the table gives both",
             "ratios": {s["sample"]: s["derived_over_reported"] for s in small}, "worst_relative_difference": round(max(abs(s["derived_over_reported"] - 1) for s in small), 3)}
    do2 = [round(abs(x - y), 2) for x in big["o2_pct"] for s in small for y in s["o2_pct"]]
    deviations = [
        {"id": "SAF-D1", "what": "thickness unit", "detail": f"Saffire-I table: {s1['Sample Thickness (cm)']} under a header in cm; Saffire-II table: '{small[0]['thickness_as_recorded']}' in mm for the same fabric; Saffire-III table: '.33 cm'. Not corrected; the numeric value is not used."},
        {"id": "SAF-D2", "what": "width and length of the large sample", "detail": f"Saffire-I table lists width {s1['Sample Width (cm)']} and length {s1['Sample Length (cm)']} cm; the Saffire-III table and NASA's operations note give 40.6 cm wide by 94 cm long. Read here as {big['width_cm']} cm wide, {big['length_cm']} cm long."},
        {"id": "SAF-D3", "what": "length of the small samples", "detail": "Saffire-II table and readme: 29 cm; Saffire-I operations note: 25 cm. The table value is used for the burn length because the table reports the burn length itself (29 cm)."},
        {"id": "SAF-D4", "what": "column header", "detail": "The Saffire-II column headed 'Spread Length' holds values in mm/s; read as the reported spread rate."},
        {"id": "SAF-D5", "what": "blank material cell", "detail": "Sample 2-6 has no material in the table; read as the row above (SIBAL), as the readme describes two SIBAL samples. Stated, not silent."},
    ]
    gates = {
        "run_identity": _g("pass", ["each run is a named row of NASA's experimental table for its investigation"], [T1, T2], ["S-ID"]),
        "observable_equivalence": _g("partial", [f"small samples: spread rate reported by NASA; large sample: average derived as length over burn time. On the small samples the derived average is within {proxy['worst_relative_difference'] * 100:.0f} % of the reported rate"], [T1, T2], ["S-OBS"]),
        "material_geometry": _g("partial", ["same named fabric (SIBAL cotton-fiberglass); thickness unit differs between NASA's tables (SAF-D1)"], [T1, T2], ["S-MAT"]),
        "atmosphere_flow": _g("pass" if max(do2) <= 0.5 else ("partial" if max(do2) <= 1 else "fail"), [f"oxygen {big['o2_pct_as_recorded']} against {', '.join(sorted({s['o2_pct_as_recorded'] for s in small}))} % (largest difference {max(do2)} points); flow {big['flow_cm_s']:g} and {small[0]['flow_cm_s']:g} cm/s, both concurrent; pressure not in the tables"], [T1, T2], ["S-ATM"]),
        "regime_validity": _g("unknown", ["GFL's regime module covers opposed flow over PMMA; it says nothing about concurrent spread over fabric"], ["src/gfl_analysis/regime.py"], ["S-BC"]),
        "boundary_conditions": _g("partial", [f"width {small[0]['width_cm']:g} against {big['width_cm']:g} cm, length {small[0]['length_cm']:g} against {big['length_cm']:g} cm: the scale differs by design, it is the variable Saffire tested"], [T1, T2], ["S-BC"]),
        "measurement_reconstruction": _g("unknown", ["no rate was measured by GFL from the Saffire images; all values are source-reported or derived from the tables"], [T1, T2], ["S-OBS"]),
        "uncertainty_and_reproducibility": _g("unknown", ["NASA's tables give no uncertainty; two small samples, one large"], [T1, T2], ["S-UQ"]),
        "domain_statement": _g("pass", ["domain stated in the request"], [str(RULESET.relative_to(ROOT))], ["S-ID"]),
    }
    ruleset = json.loads(RULESET.read_text(encoding="utf-8"))
    res = {}
    for inf in ("source_reported_comparison", "quantitative_transfer"):
        r = assess({"inference": inf, "gates": gates, "domain_statement": "Concurrent-flow spread over SIBAL fabric at 20 cm/s in microgravity, Saffire-II 5 cm strips to the Saffire-I 40.6 cm sample; source-reported values.",
                    "prohibited_extrapolations": ruleset["scope"]["prohibited_uses"], "conflicts": [], "incompatibilities": []}, ruleset)
        res[inf] = {"conclusion": r["conclusion"], "primary_reason": r.get("primary_reason"), "gates": {g["gate_id"]: g["status"] for g in r["gate_assessments"]}}
    lo, hi = min(rep), max(rep)
    out = {"version": "1", "label": "Source-reported values from NASA's experimental tables, and averages derived from them. Not GFL measurements.",
           "question": "Does the spread rate of the 5 cm SIBAL strips of Saffire-II inform the 40.6 cm SIBAL sample of Saffire-I?",
           "sources": [{"study": "PSI-98", "file": T1, "sha256": sha[T1]}, {"study": "PSI-99", "file": T2, "sha256": sha[T2]}],
           "small_samples": small, "large_sample": big, "proxy_check": proxy, "deviations": deviations, "gates": gates, "assessment": res,
           "comparison": {"small_reported_mm_s": [lo, hi], "small_derived_mm_s": [min(der), max(der)], "large_derived_mm_s": big["average_rate_derived_mm_s"],
                          "large_inside_small_range": lo <= big["average_rate_derived_mm_s"] <= hi,
                          "reading": "exploratory: one large sample, two small ones, no uncertainties; the large-sample value rests on the assumption that the whole length burned; an average over the whole burn hides growth and steady phases"},
           "assumptions": ["the Saffire-I table gives a burn time but no burn length: the whole sample length is taken as burned in that time",
                           "burn time is taken as the time the flame travelled, although it may include ignition and burn-out"],
           "not_done": ["a rate measured by GFL from the Saffire image sets, which are public", "the opposed-flow samples (the table gives no burn length for them)", "Saffire-III at 30 cm/s (its table gives no burn time)"]}
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if a.page:
        a.page.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"small": [(s["sample"], s["spread_rate_reported_mm_s"], s["average_rate_derived_mm_s"]) for s in small], "large_derived": big["average_rate_derived_mm_s"],
                      "proxy": proxy["ratios"], "o2_diff": max(do2), "assessment": {k: v["conclusion"] for k, v in res.items()}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
