"""The clean-room rebuild from sealed derived files must reproduce every compared output (DEC-022)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rebuild_from_derived_files_reproduces_the_sealed_outputs():
    r = subprocess.run([sys.executable, "tools/rebuild_all.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-500:]
    assert "differs" not in r.stdout and "not produced" not in r.stdout
