import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gfl_analysis import anomaly, cram1, flow, gates, measure, prov, records, regime, uq

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "data/synthetic/aal_test2"


def test_flow_uses_nasa_calibration_and_states_its_limits():
    f = flow.air_display_to_velocity(3)
    assert math.isclose(f["value_cm_s"], 3.0198)
    assert "centreline" in f["location"] and f["not_known"]
    assert flow.air_display_to_velocity(None)["status"] == "unknown"


def test_uq_keeps_the_unbounded_unknown_outside_the_interval():
    out = uq.from_rates_file(ROOT / "data/derived/rw4/B6_RW4_RATES.json", 3)
    assert len(out["reported_interval_mm_s"]) == 2
    edge = next(e for e in out["layer3_physical_unknowns"] if e["id"] == "luminous_edge_offset")
    assert edge["bound"] is None
    lo, hi = out["interval_with_bounded_unknowns_mm_s"]
    assert lo < out["reported_interval_mm_s"][0] and hi > out["reported_interval_mm_s"][1]


def test_cram1_thin_theory_scales_inversely_with_thickness_and_never_uses_fitted_F():
    a, b = cram1.predict(100), cram1.predict(200)
    for k in a["rate_mm_s_by_constant"]:
        assert math.isclose(a["rate_mm_s_by_constant"][k], 2 * b["rate_mm_s_by_constant"][k], rel_tol=1e-3)
    assert a["F_from_properties"] != 4.76
    assert a["band_mm_s"][0] < a["rate_mm_s_by_constant"]["Delichatsios_pi_over_4"] < a["band_mm_s"][1]


def test_regime_groups_move_the_right_way_with_flow():
    slow, fast = regime.classify(1), regime.classify(30)
    assert slow["radiation_number"] > fast["radiation_number"]
    assert slow["damkohler"] > fast["damkohler"]
    assert regime.classify(3)["regime"] == "thermal"
    assert regime.classify(0)["regime"].startswith("radiative side")
    assert regime.classify(60)["regime"].startswith("kinetic")


def _frames(case):
    side = json.loads((SYN / "withheld/side_test2.json").read_text())
    prof = {r[0]: np.array(r[1:], float) for r in csv.reader((SYN / f"{case}_band_profiles.csv").open()) if r[0] != "image"}
    meta = list(csv.DictReader((SYN / f"{case}_frames_metadata.csv").open()))
    return [{"t_s": float(m["t_s"]), "exposure_s": float(m["exposure_s"]), "brightness": float(np.clip(prof[m["image"]], 0, None).sum()),
             "sat_px": side[case]["sat_px"][k]} for k, m in enumerate(meta)]


def test_anomaly_detector_finds_every_detectable_planted_anomaly_and_nothing_else():
    found = {c: {(f["check"], f.get("frame")) for f in anomaly.frame_checks(_frames(c)) if f.get("severity") != "info"} for c in ("T1", "T2", "T3", "T4")}
    assert found["T1"] == {("saturation", 18)}
    assert found["T2"] == {("brightness_flicker", None)}
    assert found["T3"] == {("time_gap", 1)}
    assert found["T4"] == set()  # the luminous-edge offset is invisible in the images by construction (uq layer 3)


def test_overlay_flicker_is_flagged():
    assert anomaly.overlay_checks([(0, 3), (3, 2), (6, 3), (9, 3)])[0]["values"] == [3, 2, 3]


def test_computed_gates_infer_rather_than_match_an_unnamed_material():
    a = gates.assess_pair(records.record("B6", 3), records.record("B13", 3))
    g = {x["gate_id"]: x["status"] for x in a["gate_assessments"]}
    assert g["run_identity"] == "pass" and g["observable_equivalence"] == "pass"
    assert g["material_geometry"] == "partial"
    assert g["uncertainty_and_reproducibility"] == "partial"
    assert a["conclusion"] == "conditionally_informative"


def test_different_rules_are_not_the_same_observable():
    s, t = records.record("B6", 3), records.record("B9", 2)
    t["rule"] = "R-W2"
    assert gates.compute_gates(s, t)["observable_equivalence"]["status"] == "fail"


def test_measurement_module_reproduces_the_sealed_synthetic_result(tmp_path):
    out = measure.measure_synthetic(SYN, SYN / "withheld/side_test2.json", "T1", tmp_path)
    ref = json.loads((SYN.parents[1] / "derived/aal_test2/T1_rw3_rates.json").read_text())
    seg = lambda d: {s["air_display"]: s["budget"]["rate_mm_s"] for s in d["segments"] if s.get("budget")}  # noqa: E731
    assert seg(out) == seg(ref)


def test_prov_export_links_every_known_parent():
    d = prov.export(ROOT / "ledger/ledger.jsonl")
    assert d["@context"]["prov"] == "http://www.w3.org/ns/prov#"
    ents = [x for x in d["@graph"] if x.get("@type") == "prov:Entity"]
    assert ents and all(x["@id"].startswith("urn:sha256:") for x in ents)
    assert any("prov:wasDerivedFrom" in x for x in ents) and any("prov:wasRevisionOf" in x for x in ents)
