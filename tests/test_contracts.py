import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULESET = json.loads((ROOT / "configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json").read_text())
VOCAB = json.loads((ROOT / "schemas/CONTROLLED_VOCABULARY_v0.1.json").read_text())
REQUEST_SCHEMA = json.loads((ROOT / "schemas/TRANSFER_ASSESSMENT_REQUEST_v0.1.schema.json").read_text())


class ContractIntegrityTests(unittest.TestCase):
    def test_request_schema_profiles_match_ruleset(self):
        self.assertEqual(set(REQUEST_SCHEMA["properties"]["inference"]["enum"]),
                         set(RULESET["intended_inference_profiles"]))

    def test_request_schema_gate_states_match_controlled_vocabulary(self):
        self.assertEqual(
            set(REQUEST_SCHEMA["properties"]["gates"]["additionalProperties"]["properties"]["status"]["enum"]),
            set(VOCAB["gate_status"]["enum"]),
        )

    def test_request_schema_conflict_states_are_explicit(self):
        self.assertEqual(
            set(REQUEST_SCHEMA["properties"]["conflicts"]["items"]["properties"]["status"]["enum"]),
            {"unresolved", "resolved"},
        )

    def test_example_requests_use_declared_profiles_and_gates(self):
        for path in sorted((ROOT / "examples").glob("*.json")):
            request = json.loads(path.read_text())
            self.assertIn(request["inference"], RULESET["intended_inference_profiles"])
            required = set(RULESET["intended_inference_profiles"][request["inference"]]["required_gates"])
            self.assertEqual(set(request["gates"]), required)
            for gate in request["gates"].values():
                self.assertIn(gate["status"], VOCAB["gate_status"]["enum"])

    def test_conflict_scope_names_known_ruleset_gates(self):
        known_gates = set(RULESET["gates"])
        for path in sorted((ROOT / "examples").glob("*.json")):
            request = json.loads(path.read_text())
            for conflict in request.get("conflicts", []):
                for gate_id in conflict.get("affects_gates", []):
                    self.assertIn(gate_id, known_gates)

    def test_fixture_ids_and_invariants_are_unique(self):
        fixtures = json.loads((ROOT / "tests/fixtures/PMMA100_TRANSFER_CASES_v0.1.json").read_text())
        case_ids = [case["test_id"] for case in fixtures["cases"]]
        invariant_ids = [item["id"] for item in fixtures["invariants"]]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertEqual(len(invariant_ids), len(set(invariant_ids)))
        self.assertEqual(len(case_ids), 15)
        self.assertEqual(len(invariant_ids), 12)


if __name__ == "__main__":
    unittest.main()
