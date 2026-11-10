"""Experiment memory (DEC-042): failures are kept, ledger links resolve, storyline is valid."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(tmp_path):
    out = tmp_path / "data" / "experiment_memory.json"
    subprocess.run([sys.executable, str(ROOT / "tools/build_experiment_memory.py"), "--out", str(out)],
                   check=True, capture_output=True)
    return json.loads(out.read_text(encoding="utf-8")), out.parent


def rec(mem, rid):
    return next(r for r in mem["records"] if r["id"] == rid)


def test_failures_are_kept_as_records(tmp_path):
    mem, _ = build(tmp_path)
    assert rec(mem, "DEC-032")["current_state"] == "withdrawn"
    assert len(rec(mem, "DEC-032")["history"]) >= 2          # proposal and withdrawal both kept
    assert rec(mem, "RES-009")["negative_record"]             # rejected blind result kept
    assert mem["negative_records"] > 0


def test_superseded_result_is_marked_from_the_ledger(tmp_path):
    mem, _ = build(tmp_path)
    r = rec(mem, "RES-001")
    assert r["current_state"] == "superseded" and r["superseded_in_ledger"]


def test_every_ledger_link_points_to_a_real_entry(tmp_path):
    mem, d = build(tmp_path)
    hashes = {json.loads(line)["entry_hash"] for line in (d / "ledger.jsonl").read_text().splitlines() if line}
    for r in mem["records"]:
        for h in r["history"]:
            for f in h["files"]:
                for s in f["ledger"]:
                    assert s["entry_hash"] in hashes


def test_storyline_cites_only_existing_records_and_public_keys_are_copied(tmp_path):
    mem, d = build(tmp_path)
    ids = {r["id"] for r in mem["records"]}
    assert all(x in ids for step in mem["storyline"]["steps"] for x in step["records"])
    assert (d / "release-a.pub.json").exists()
