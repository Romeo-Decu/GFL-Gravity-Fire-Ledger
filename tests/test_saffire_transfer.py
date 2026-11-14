import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_saffire_transfer", ROOT / "tools/build_saffire_transfer.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

# Stand-in tables with the layout of NASA's files (headers as published) and invented values.
T1 = "Sample Number ,Material,Sample Thickness (cm),Sample Length (cm),Sample Width (cm),Air Flow (cm/s),Percent O2,Ignition Power (W),Ignition Time (s),Burn Time (s),Flow Direction ,Camera 1,Camera 2\nS1,SIBAL Fabric,0.37,40,100,20,21.0 - 21.2,182,8,500,Concurrent,S1C1,S1C2\n"
T2 = ("Sample Number,Material,Samle Thickness ,Sample Length ,Sample Width (cm),Air Flow (cm/s),Percent O2 (Note 1),Ignition Power (W),Ignition Time (s),Burn Time (s),Flow Direction,?-g Burn Length,?-g Spread Length,1-g Burn Length,1-g Spread Rate,Camera 1,Camera 2\n"
      "2-4,Silicone,037 mm,29 cm,5 cm,20 cm/s,~ 21.0,80 W,9.2 s,Insignificant,Opposed,~ 0,n/a,Complete,0.6 mm/s,S4C1,S4C2\n"
      "2-5,Cotton-Fiberglass (SIBAL),037 mm,29 cm,5 cm,20 cm/s,~ 21.0,80 W,9.2 s,145 s,Concurrent,29 cm,2.0 mm/s,Complete,Acceleratory,S5C1,S5C2\n"
      "2-6,,037 mm,29 cm,5 cm,20 cm/s,~ {o2},80 W,9.2 s,100 s,Concurrent,29 cm,2.9 mm/s,Complete,Acceleratory,S6C1,S6C2\n")


def run(tmp_path, o2="21.0"):
    (tmp_path / st.T1).write_text(T1, encoding="utf-8")
    (tmp_path / st.T2).write_text(T2.format(o2=o2), encoding="utf-8")
    out = tmp_path / "o.json"
    assert st.main(["--src", str(tmp_path), "--out", str(out)]) == 0
    return json.loads(out.read_text(encoding="utf-8"))


def test_values_are_read_as_recorded_and_the_arithmetic_is_shown(tmp_path):
    d = run(tmp_path)
    assert [s["sample"] for s in d["small_samples"]] == ["2-5", "2-6"]  # the silicone and opposed rows are left out
    assert d["small_samples"][1]["material_as_recorded"] is None and "SIBAL" in d["small_samples"][1]["material_read_as"]
    assert d["small_samples"][0]["average_rate_derived_mm_s"] == 2.0 and d["small_samples"][1]["derived_over_reported"] == 1.0
    assert (d["large_sample"]["width_cm"], d["large_sample"]["length_cm"]) == (40.0, 100.0)  # swapped headers are recorded, not trusted
    assert d["large_sample"]["average_rate_derived_mm_s"] == 2.0 and d["comparison"]["large_inside_small_range"]
    assert len(d["deviations"]) == 5 and d["assumptions"]


def test_missing_uncertainty_blocks_the_quantitative_transfer_but_not_the_comparison(tmp_path):
    d = run(tmp_path)
    assert d["assessment"]["quantitative_transfer"]["conclusion"] == "undetermined"
    assert d["assessment"]["source_reported_comparison"]["conclusion"] == "conditionally_informative"
    assert d["gates"]["atmosphere_flow"]["status"] == "pass"


def test_an_oxygen_difference_above_one_point_fails_the_gate_and_the_comparison_no_longer_stands(tmp_path):
    d = run(tmp_path, o2="23.5")
    assert d["gates"]["atmosphere_flow"]["status"] == "fail"
    assert d["assessment"]["source_reported_comparison"]["conclusion"] not in ("conditionally_informative", "directly_supported")
