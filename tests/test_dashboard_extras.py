"""Dashboard extras (function map, transfer engine output, vault summary): consistency checks."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_extras_build_and_are_consistent(tmp_path):
    out = tmp_path / "data"
    subprocess.run([sys.executable, str(ROOT / "tools/build_experiment_memory.py"), "--out", str(out / "experiment_memory.json")],
                   check=True, capture_output=True)
    subprocess.run([sys.executable, str(ROOT / "tools/build_dashboard_extras.py"), "--out", str(out)], check=True, capture_output=True)
    caps = json.loads((out / "capabilities.json").read_text())
    items = [it for g in caps["groups"] for it in g["items"]]
    assert {it["status"] for it in items} <= {"built", "partial", "designed"}
    for it in items:
        if it["status"] == "designed":
            assert it.get("spec") and (out / "specs" / it["spec"]).exists()   # designed => a real specification
    tr = json.loads((out / "transfer_pmma100.json").read_text())
    assert tr["profiles"]["quantitative_transfer"]["conclusion"] == "undetermined"       # refusal is shown, not hidden
    assert tr["profiles"]["documentary_summary"]["conclusion"] == "conditionally_informative"
    vault = json.loads((out / "vault.json").read_text())
    assert {k["role"] for k in vault["keys"]} == {"owner", "pipeline"}
    assert all("public_key_b64" not in k for k in vault["keys"])
