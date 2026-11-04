import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fif_transfer import assess

RULESET = json.loads((ROOT / "configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json").read_text())


def current_case_payload(inference):
    gate_inputs = {}
    for gate_id in RULESET["intended_inference_profiles"][inference]["required_gates"]:
        gate = RULESET["gates"][gate_id]
        gate_inputs[gate_id] = {
            "status": gate["current_case_status"],
            "reasons": [f"Configured current case status: {gate['current_case_status']}"],
            "evidence_refs": ["research:PMMA100_SOURCE_RECONCILIATION_AUDIT"],
            "rule_ids": ["PMMA-100-R01", "PMMA-100-R02", "PMMA-100-R11"],
        }
    return {
        "inference": inference,
        "gates": gate_inputs,
        "conflicts": [{
            "id": "B3-flow-2-vs-3-cm-s",
            "status": "unresolved",
            "affects_gates": ["atmosphere_flow"],
            "description": "Appendix A.1 reports 2 cm/s; Section 2.3 reports 3 cm/s."
        }],
        "incompatibilities": [],
        "domain_statement": (
            "Published-summary comparison of nominal 100-µm PMMA flame spread; "
            "not a matched-run quantitative validation."
        ),
        "prohibited_extrapolations": [
            "gravity-alone causality",
            "spacecraft fire prediction",
            "safety certification",
            "unmatched B3-to-2.2-mm/s attribution",
        ],
    }


class PMMA100CurrentCaseTests(unittest.TestCase):
    def test_documentary_summary_remains_conditionally_informative(self):
        result = assess(current_case_payload("documentary_summary"), RULESET)
        self.assertEqual(result["conclusion"], "conditionally_informative")

    def test_quantitative_transfer_remains_undetermined(self):
        result = assess(current_case_payload("quantitative_transfer"), RULESET)
        self.assertEqual(result["conclusion"], "undetermined")
        self.assertIn("run_identity", [g["gate_id"] for g in result["gate_assessments"]])
        self.assertEqual(len(result["unresolved_conflicts"]), 1)

    def test_model_calibration_and_validation_remain_undetermined(self):
        for profile in ("model_calibration", "model_validation"):
            with self.subTest(profile=profile):
                self.assertEqual(assess(current_case_payload(profile), RULESET)["conclusion"],
                                 "undetermined")


if __name__ == "__main__":
    unittest.main()
