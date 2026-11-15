import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_citations import build, check_summary  # noqa: E402

TEXTS = {"RES-1": "rate 2.120 on the active interval, 77 frames", "RES-2": "a sign error in the script"}


def test_passes_grounded_summary():
    r = check_summary("The rate is 2.120 on the active interval [RES-1]. The direction is a sign error [RES-1, RES-2].", TEXTS)
    assert r == {"sentences": 2, "passed": True, "errors": []}


def test_rejects_uncited_unknown_and_invented_numbers():
    assert "C1" in check_summary("The rate is fine. Really [RES-1].", TEXTS)["errors"][0]
    assert "C2" in check_summary("Rate known [RES-9].", TEXTS)["errors"][0]
    bad = check_summary("The rate is 2.12 on 78 frames [RES-1].", TEXTS)
    assert not bad["passed"] and sum("C3" in e for e in bad["errors"]) == 2  # rounded 2.12 and invented 78
    # a number from a record the sentence does not cite does not count
    assert not check_summary("A sign error at 2.120 [RES-2].", TEXTS)["passed"]


def test_release_findings_pass_and_rank_by_verdict():
    findings = json.loads((ROOT / "research/fixtures/AI_FINDINGS_v1.json").read_text(encoding="utf-8"))
    memory = json.loads((ROOT / "visualization/data/experiment_memory.json").read_text(encoding="utf-8"))
    res = build(findings, memory)
    assert res["all_passed"], [f["citation_check"]["errors"] for f in res["findings"] if not f["citation_check"]["passed"]]
    order = ["upheld", "partly_upheld", "not_upheld", "fabricated"]
    ranks = [order.index(f["verdict"]) for f in res["findings"]]
    assert ranks == sorted(ranks)
