import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fif_transfer import AssessmentInputError, assess

RULESET = json.loads((ROOT / "configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json").read_text())


def payload(inference="quantitative_transfer", statuses=None, **extra):
    statuses = statuses or {}
    gates = {
        gate_id: {
            "status": statuses.get(gate_id, "pass"),
            "reasons": ["test evidence state"],
            "evidence_refs": ["fixture:T11"],
            "rule_ids": ["PMMA-100-R01"],
        }
        for gate_id in RULESET["intended_inference_profiles"][inference]["required_gates"]
    }
    value = {
        "inference": inference,
        "gates": gates,
        "conflicts": [],
        "incompatibilities": [],
        "domain_statement": "Synthetic test domain only; not a scientific finding.",
        "prohibited_extrapolations": ["fire prediction", "safety certification"],
    }
    value.update(extra)
    return value


class TransferAssessmentTests(unittest.TestCase):
    def test_all_required_gates_pass_with_domain_is_directly_supported(self):
        result = assess(payload(), RULESET)
        self.assertEqual(result["conclusion"], "directly_supported")
        self.assertTrue(result["audit"]["deterministic"])
        self.assertEqual(result["audit"]["scientific_validation_status"],
                         "not_established_by_software_execution")

    def test_missing_gate_is_unknown_not_compatible(self):
        request = payload()
        del request["gates"]["material_geometry"]
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "undetermined")
        self.assertIn("material_geometry", result["missing_gate_ids"])

    def test_unresolved_conflict_is_not_physical_incompatibility(self):
        request = payload(conflicts=[{
            "id": "flow-2-vs-3-cm-s", "status": "unresolved",
            "description": "Two source assertions disagree."
        }])
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "undetermined")
        self.assertEqual(result["blocking_incompatibilities"], [])

    def test_explicit_critical_incompatibility_without_bridge_blocks_transfer(self):
        request = payload(incompatibilities=[{
            "id": "fuel-formulation", "critical": True, "bridge_status": "absent",
            "description": "Known material formulation mismatch.",
            "reasons": ["Synthetic material incompatibility fixture."],
            "evidence_refs": ["fixture:T04"],
            "rule_ids": ["PMMA-100-R07"]
        }])
        self.assertEqual(assess(request, RULESET)["conclusion"],
                         "not_transferable_on_current_evidence")

    def test_critical_incompatibility_outside_profile_does_not_block(self):
        request = payload("documentary_summary", {
            "source_identity": "partial", "claim_statistic_integrity": "partial"
        }, incompatibilities=[{
            "id": "quantitative-material-mismatch", "critical": True,
            "bridge_status": "absent", "affects_gates": ["material_geometry"],
            "reasons": ["Synthetic material incompatibility fixture."],
            "evidence_refs": ["fixture:T04"],
            "rule_ids": ["PMMA-100-R07"]
        }])
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "conditionally_informative")
        self.assertEqual(len(result["non_blocking_incompatibilities_for_this_inference"]), 1)

    def test_critical_incompatibility_relevant_to_profile_blocks(self):
        request = payload(incompatibilities=[{
            "id": "material-mismatch", "critical": True,
            "bridge_status": "absent", "affects_gates": ["material_geometry"],
            "reasons": ["Synthetic material incompatibility fixture."],
            "evidence_refs": ["fixture:T04"],
            "rule_ids": ["PMMA-100-R07"]
        }])
        self.assertEqual(assess(request, RULESET)["conclusion"],
                         "not_transferable_on_current_evidence")

    def test_conflict_outside_required_gates_does_not_block_inference(self):
        request = payload("documentary_summary", {
            "source_identity": "partial", "claim_statistic_integrity": "partial"
        }, conflicts=[{
            "id": "flow-condition", "status": "unresolved",
            "affects_gates": ["atmosphere_flow"],
        }])
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "conditionally_informative")
        self.assertEqual(len(result["non_blocking_conflicts_for_this_inference"]), 1)

    def test_unknown_bridge_status_keeps_transfer_undetermined(self):
        request = payload(incompatibilities=[{
            "id": "fuel-formulation", "critical": True, "bridge_status": "unknown",
            "reasons": ["Bridge validation status is unknown in this synthetic fixture."],
            "evidence_refs": ["fixture:T04"],
            "rule_ids": ["PMMA-100-R07"]
        }])
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "undetermined")
        self.assertEqual(len(result["unresolved_incompatibility_bridges"]), 1)

    def test_critical_incompatibility_requires_explicit_bridge_status(self):
        request = payload(incompatibilities=[{"id": "fuel-formulation", "critical": True}])
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_failed_gate_is_not_automatically_physical_incompatibility(self):
        request = payload(statuses={"run_identity": "fail"})
        result = assess(request, RULESET)
        self.assertEqual(result["conclusion"], "undetermined")
        self.assertEqual(result["blocking_incompatibilities"], [])

    def test_pass_requires_reason_evidence_and_rule_references(self):
        request = payload()
        request["gates"]["run_identity"]["evidence_refs"] = []
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_not_applicable_is_rejected_without_ruleset_authorization(self):
        request = payload()
        request["gates"]["run_identity"]["status"] = "not_applicable"
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_partial_documentary_evidence_is_conditionally_informative(self):
        result = assess(payload("documentary_summary", {
            "source_identity": "partial", "claim_statistic_integrity": "partial"
        }), RULESET)
        self.assertEqual(result["conclusion"], "conditionally_informative")

    def test_partial_mechanism_evidence_is_qualitative(self):
        result = assess(payload("qualitative_mechanism", {
            "source_identity": "partial", "mechanism_relevance": "partial"
        }), RULESET)
        self.assertEqual(result["conclusion"], "qualitatively_informative")

    def test_calibration_profile_does_not_claim_direct_support(self):
        self.assertEqual(assess(payload("model_calibration"), RULESET)["conclusion"],
                         "undetermined")

    def test_domain_statement_is_mandatory(self):
        request = payload()
        request["domain_statement"] = " "
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_invalid_gate_status_is_rejected(self):
        request = payload()
        request["gates"]["run_identity"]["status"] = "compatible"
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_malformed_inference_is_controlled_input_error(self):
        request = payload()
        request["inference"] = []
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_ruleset_unknown_required_gate_is_rejected(self):
        malformed = copy.deepcopy(RULESET)
        malformed["intended_inference_profiles"]["quantitative_transfer"]["required_gates"].append(
            "undeclared_gate"
        )
        with self.assertRaises(AssessmentInputError):
            assess(payload(), malformed)

    def test_same_versioned_inputs_produce_identical_output(self):
        request = payload()
        self.assertEqual(assess(request, RULESET),
                         assess(copy.deepcopy(request), copy.deepcopy(RULESET)))

    def test_audit_hashes_are_stable_and_present(self):
        result = assess(payload(), RULESET)
        self.assertEqual(len(result["audit"]["request_sha256"]), 64)
        self.assertEqual(len(result["audit"]["ruleset_sha256"]), 64)
        self.assertIn("do not validate", result["audit"]["hash_semantics"])

    def test_request_hash_changes_when_input_changes(self):
        request = payload()
        first = assess(request, RULESET)["audit"]["request_sha256"]
        request["domain_statement"] = "Changed synthetic domain."
        second = assess(request, RULESET)["audit"]["request_sha256"]
        self.assertNotEqual(first, second)

    def test_audit_preserves_rule_ids_and_evidence_refs(self):
        result = assess(payload(), RULESET)
        self.assertEqual(result["audit"]["rule_ids"], ["PMMA-100-R01"])
        self.assertEqual(result["audit"]["evidence_refs"], ["fixture:T11"])

    def test_unknown_rule_reference_is_rejected(self):
        request = payload()
        request["gates"]["run_identity"]["rule_ids"] = ["UNKNOWN-RULE"]
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_undeclared_input_gate_is_rejected(self):
        request = payload()
        request["gates"]["typo_gate"] = {"status": "unknown"}
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_malformed_conflict_status_is_controlled_input_error(self):
        request = payload(conflicts=[{"status": []}])
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_malformed_bridge_status_is_controlled_input_error(self):
        request = payload(incompatibilities=[{
            "critical": True, "bridge_status": []
        }])
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)

    def test_prohibited_extrapolations_must_be_a_list(self):
        request = payload()
        request["prohibited_extrapolations"] = "fire prediction"
        with self.assertRaises(AssessmentInputError):
            assess(request, RULESET)


if __name__ == "__main__":
    unittest.main()
