import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_table_evidence", ROOT / "tools/run_table_evidence.py")
rte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rte)


def test_oxygen_reading_uses_fixed_bands_and_accepts_fractions():
    assert rte.oxygen_reading([21.0, 21.4]) == "air"
    assert rte.oxygen_reading([0.17, 0.18]) == "reduced oxygen"
    assert rte.oxygen_reading([13.6, 22.2]) == "varied"
    assert rte.oxygen_reading([30.0]) == "enriched oxygen"


def test_flow_reading():
    assert rte.flow_reading([0, 0]) == "quiescent"
    assert rte.flow_reading([5, 10]) == "forced flow"
    assert rte.flow_reading([0, 5]) == "several"
