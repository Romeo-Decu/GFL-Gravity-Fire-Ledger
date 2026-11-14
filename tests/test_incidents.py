import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_incident_quotes_were_found_and_the_enriched_oxygen_gap_is_stated():
    d = json.loads((ROOT / "data/derived/evidence_map/INCIDENTS_v1.json").read_text(encoding="utf-8"))
    assert d["all_quotes_found"]
    a1 = next(i for i in d["incidents"] if i["id"] == "apollo1")
    assert a1["of_which_solid_fuel"] == []  # no solid material in enriched oxygen anywhere in the run tables
    assert next(i for i in d["incidents"] if i["id"] == "apollo13")["functions"] == []
