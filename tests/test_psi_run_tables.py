import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("psi_run_tables", ROOT / "tools/psi_run_tables.py")
rt = importlib.util.module_from_spec(spec)
import sys
sys.path.insert(0, str(ROOT / "tools"))
spec.loader.exec_module(rt)


def test_headers_are_classified_by_the_fixed_rules():
    assert rt.classify("Percent O2") == ["oxygen"]
    assert rt.classify("Percent O2 (Note 1)") == ["oxygen", "outcome"]  # a known misfire of the fixed rules ("note"); outcome is not a condition
    assert "flow" in rt.classify("Air Flow (cm/s)")
    assert rt.classify("Sample Thickness (cm)") == ["geometry"]
    assert rt.classify("Camera 1") == []


def test_a_column_with_no_filled_cell_is_not_counted_as_recorded(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("Material,Percent O2,Pressure (psia)\nPMMA,21,\nPMMA,17,\n\n", encoding="utf-8")
    t = rt.read_table(p)
    assert t["rows"] == 2
    assert {c["header"]: c["filled"] for c in t["columns"]} == {"Material": 2, "Percent O2": 2, "Pressure (psia)": 0}
