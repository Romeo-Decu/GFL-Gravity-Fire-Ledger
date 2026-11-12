"""Evaluation tools: the packet splits back into its files, and the scorer accepts only quotes that are in the packet."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_evaluation_packet as bp  # noqa: E402
import run_evaluation as rv  # noqa: E402
import score_evaluation as sv  # noqa: E402


def test_packet_holds_the_documents_and_splits_back():
    packet = bp.build()
    files = bp.split(packet)
    for name in bp.DOCS + ["FUNCTIONS", "KEY_NUMBERS", "REPORT_B11", "REGISTER"]:
        assert name in files and len(files[name]) > 200, name
    assert (ROOT / "docs/USER_GUIDE_v1.md").read_text(encoding="utf-8").strip() in files["docs/USER_GUIDE_v1.md"]
    assert "| RES-052 |" in files["REGISTER"] and "| RES-001 |" not in files["REGISTER"]
    assert "source code" in files["HEADER"]


def test_questionnaire_is_taken_from_the_protocol_and_has_no_scoring_key():
    q = rv.questionnaire()
    assert "A2." in q and "Answer format" in q
    assert "How the answers are checked" not in q and "is correct if" not in q
    p = rv.prompt("physicist", "PACKET")
    assert "combustion scientist" in p and "<packet>\nPACKET\n</packet>" in p


def test_scorer_checks_quotes_and_reading_checks():
    files = {"docs/X.md": "The rate is 2.20 mm/s, interval 1.91 to 2.37.\nNothing   else is claimed here."}
    good = {"locator": {"file": "docs/X.md", "quote": "nothing else is claimed"}}
    assert sv.locator_state(good, files) == "verified"
    assert sv.locator_state({"locator": {"file": "X.md", "quote": "Nothing else is claimed here."}}, files) == "verified"
    assert sv.locator_state({"locator": {"file": "docs/X.md", "quote": "the rate is 3.00"}}, files) == "quote not found"
    assert sv.locator_state({"locator": {"file": "docs/Y.md", "quote": "the rate"}}, files) == "file not in packet"
    assert sv.locator_state({"statement": "fine work"}, files) == "no locator"
    ans = {"role": "juror", "A": {"A1": {"rate_mm_s": 2.1973, "interval_mm_s": [1.9146, 2.3682]}, "A2": {"section_exists": True}, "A3": {"prediction": "P-B13", "ratio": 0.189}},
           "B": [good, {"statement": "great"}], "C": [], "D": [], "E": []}
    s = sv.score({"ok": True, "role": "juror", "deployment": "m", "content": "```json\n" + json.dumps(ans) + "\n```"}, files)
    assert s["reading_checks"] == {"A1": True, "A2": False, "A3": True, "invented_content": True}
    assert s["sections"]["B"]["verified"] == 1 and s["sections"]["B"]["not_counted"][0]["state"] == "no locator"
    assert sv.score({"ok": True, "content": "sorry"}, files)["parsed"] is False
