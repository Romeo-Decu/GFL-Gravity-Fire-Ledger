import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json").read_text())
PACKAGE = json.loads((ROOT / "research/acquisition/PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json").read_text())
VOCABULARY = json.loads((ROOT / "schemas/CONTROLLED_VOCABULARY_v0.1.json").read_text())
GRAPH_SCHEMA = json.loads((ROOT / "schemas/EVIDENCE_GRAPH_v0.1.schema.json").read_text())


class EvidenceAcquisitionPackageContractTests(unittest.TestCase):
    def test_schema_and_template_are_valid_json(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(PACKAGE["package_version"], SCHEMA["properties"]["package_version"]["const"])

    def test_template_contains_all_required_root_fields_and_no_unknown_fields(self):
        self.assertTrue(set(SCHEMA["required"]).issubset(PACKAGE))
        self.assertTrue(set(PACKAGE).issubset(SCHEMA["properties"]))
        self.assertIs(SCHEMA["additionalProperties"], False)

    def test_template_collections_are_present_and_empty(self):
        collections = (
            "source_records",
            "asset_records",
            "extraction_records",
            "linkage_candidates",
            "unresolved_questions",
        )
        for field in collections:
            self.assertEqual(PACKAGE[field], [])

    def test_package_has_no_self_asserted_validation_or_lifecycle_fields(self):
        forbidden = {
            "status",
            "validation_status",
            "lifecycle_state",
            "validated",
            "validation_attestation",
            "approval",
        }
        self.assertTrue(forbidden.isdisjoint(SCHEMA["properties"]))
        self.assertTrue(forbidden.isdisjoint(PACKAGE))

    def test_acquisition_evidence_states_match_canonical_vocabulary(self):
        expected = VOCABULARY["evidence_state"]["enum"]
        actual = SCHEMA["$defs"]["extraction_record"]["properties"]["evidence_state"]["enum"]
        self.assertEqual(actual, expected)
        self.assertNotIn("conflicting", actual)

    def test_source_locator_vocabulary_matches_canonical_graph(self):
        acquisition = SCHEMA["$defs"]["source_locator"]["properties"]["location_type"]["enum"]
        graph = GRAPH_SCHEMA["properties"]["nodes"]["items"]["properties"]["source_locators"]["items"]["properties"]["location_type"]["enum"]
        self.assertEqual(acquisition, graph)

    def test_package_schema_uses_closed_record_objects(self):
        for name in (
            "source_record",
            "asset_record",
            "source_locator",
            "extraction_record",
            "linkage_candidate",
            "unresolved_question",
        ):
            self.assertIs(SCHEMA["$defs"][name]["additionalProperties"], False)

    def test_template_base_commit_is_a_full_sha(self):
        self.assertRegex(PACKAGE["base_repository_commit"], re.compile(r"^[0-9a-f]{40}$"))


if __name__ == "__main__":
    unittest.main()
