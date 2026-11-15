"""A5. Three-layer uncertainty for a measured spread rate.

Layer 1, statistical (aleatory): the bootstrap 95 % interval of the reference definition.
Layer 2, analyst choice: the spread of the rate across front definitions the analyst could have chosen.
Layer 3, physical unknowns (epistemic): effects no analysis of these images can remove; listed with a bound when
one exists, never added into the interval when none does.
"""
from __future__ import annotations

import json
from pathlib import Path

EPISTEMIC = [
    {"id": "luminous_edge_offset", "what": "change of the offset between the luminous edge and the pyrolysis front",
     "bound": None, "evidence": "synthetic test 2: +5 % (T4) and +1.8 % (T1) bias, undetected by any analyst (ISS-050, ISS-053)",
     "reduced_by": "a front measurement independent of luminosity (surface temperature, thermocouple)"},
    {"id": "scale_plane", "what": "ruler and sample in different planes (parallax)", "bound_rel": 0.03,
     "evidence": "ISS-020; +-3 % is an allowance, not a measurement", "reduced_by": "plane correction from the 20 mm sample width"},
    {"id": "flow_at_sample", "what": "opposing-flow speed at the sample surface",
     "bound": None, "evidence": "calibration is on the duct centreline (A0, flow.py); boundary layer not characterised",
     "reduced_by": "anemometry at the sample position"},
]


def layers(budget: dict, definitions: dict | None = None) -> dict:
    rate = budget["rate_mm_s"]
    stat = budget["statistical_95_mm_s"]
    out = {"rate_mm_s": rate, "reference_definition": budget.get("reference_definition"),
           "layer1_statistical_95_mm_s": stat,
           "layer2_analyst_choice": {"systematic_mm_s": budget.get("definition_systematic_mm_s"),
                                     "definition_range_mm_s": budget.get("definition_range_mm_s")},
           "reported_interval_mm_s": budget["reported_interval_mm_s"],
           "layer3_physical_unknowns": EPISTEMIC,
           "reading": "layers 1 and 2 are in the reported interval; layer 3 is not, and only the scale term has a bound"}
    if definitions:
        rates = {k: v["ols_mm_s"] for k, v in definitions.items() if isinstance(v, dict) and "ols_mm_s" in v}
        out["layer2_analyst_choice"]["all_definitions_mm_s"] = rates
    s = next(e for e in EPISTEMIC if e["id"] == "scale_plane")["bound_rel"]
    lo, hi = budget["reported_interval_mm_s"]
    out["interval_with_bounded_unknowns_mm_s"] = [round(lo * (1 - s), 4), round(hi * (1 + s), 4)]
    return out


def from_rates_file(path: Path, air_display: int) -> dict:
    d = json.loads(Path(path).read_text())
    seg = next(s for s in d["segments"] if s["air_display"] == air_display and s.get("budget"))
    return layers(seg["budget"], seg.get("definitions"))
