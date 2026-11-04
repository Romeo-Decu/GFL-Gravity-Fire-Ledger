import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def run_example(self, request_name):
        command = [
            sys.executable, "-m", "fif_transfer",
            "--ruleset", str(ROOT / "configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json"),
            "--request", str(ROOT / "examples" / request_name),
            "--compact",
        ]
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env)

    def test_documentary_example_runs_and_returns_conditional_conclusion(self):
        result = self.run_example("PMMA100_DOCUMENTARY_SUMMARY_REQUEST_v0.1.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["conclusion"], "conditionally_informative")

    def test_quantitative_example_runs_and_abstains(self):
        result = self.run_example("PMMA100_QUANTITATIVE_TRANSFER_REQUEST_v0.1.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["conclusion"], "undetermined")
        self.assertEqual(len(output["unresolved_conflicts"]), 1)

    def test_missing_request_returns_nonzero(self):
        command = [
            sys.executable, "-m", "fif_transfer",
            "--ruleset", str(ROOT / "configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json"),
            "--request", str(ROOT / "examples/does-not-exist.json"),
        ]
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
