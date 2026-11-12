"""The breadth audit's checks on a small made-up inventory (the real one is run only after this code is anchored)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from psi25_breadth_audit import audit, norm_test  # noqa: E402


def f(name, size=10):
    return {"category": "Raw Data", "name": "PSI-25_Raw Data_" + name, "bytes": size}


ROWS = [{"Test #": "B6", "GMT": "188", "Sample #": "153m", "Total Frames Shot": "80"},
        {"Test #": "T3", "GMT": "178", "Sample #": "182m", "Total Frames Shot": "none"},
        {"Test #": "M9", "GMT": "100", "Sample #": "200", "Total Frames Shot": "5"}]
FILES = [f("BASS_GMT188_SAMPLE_153_TESTB6.mp4", 1), f("BASS_GMT188_SAMPLE_153_TESTB6_2ND_VIEW.mp4", 2),
         f("GMT2014_188_BASS_S153M_TPB6_ProofSheet.pdf", 3), f("GMT2014_178_BASS_S182M_TPT03_ProofSheet.pdf", 4),
         f("BASS_GMT179_SAMPLE_999_TEST_T3 original videos.zip", 5), f("BASS_GMT50_SAMPLE_1_TEST_Z1.mp4", 6),
         f("iss040e045850.zip", 7), f("iss040e045851.zip", 7), f("M10-lab-camera-LOS.mp4", 8)]


def test_norm():
    assert norm_test("T03") == "T3" and norm_test("o5b") == "O5b"


def test_checks():
    r = audit({"files": FILES}, ROWS)
    assert r["K1_parsing"]["unparsed"] == ["M10-lab-camera-LOS.mp4"] and r["K1_parsing"]["still_archives"] == 2
    k2 = r["K2_coverage"]
    assert k2["tests_with_no_file"] == ["M9"]
    assert k2["tests_with_no_video"] == [] and k2["tests_with_no_proof_sheet"] == []
    k3 = r["K3_disagreements"]
    assert [x["test_in_name"] for x in k3["test_in_name_not_in_table"]] == ["Z1"]
    assert [(x["test"], x["sample_in_name"]) for x in k3["sample_differs"]] == [("T3", "999")]
    assert [(x["test"], x["gmt_in_name"]) for x in k3["gmt_differs"]] == [("T3", "179")]
    assert r["K4_duplicates"]["same_kind_same_size"] == [{"kind": "still archive", "bytes": 7, "files": ["iss040e045850.zip", "iss040e045851.zip"]}]
    assert r["K5_counts"]["table_rows_recording_frames"] == 2
