import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = json.loads((ROOT / "research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json").read_text())
SCHEMA = json.loads((ROOT / "schemas/EVIDENCE_GRAPH_v0.1.schema.json").read_text())


class EvidenceGraphContractTests(unittest.TestCase):
    def test_graph_declares_current_schema_version(self):
        self.assertEqual(GRAPH["schema_version"], SCHEMA["properties"]["schema_version"]["const"])

    def test_node_and_edge_ids_are_unique(self):
        node_ids = [node["id"] for node in GRAPH["nodes"]]
        edge_ids = [edge["id"] for edge in GRAPH["edges"]]
        self.assertEqual(len(node_ids), len(set(node_ids)))
        self.assertEqual(len(edge_ids), len(set(edge_ids)))

    def test_all_edges_reference_existing_nodes(self):
        node_ids = {node["id"] for node in GRAPH["nodes"]}
        for edge in GRAPH["edges"]:
            self.assertIn(edge["source"], node_ids, edge["id"])
            self.assertIn(edge["target"], node_ids, edge["id"])

    def test_source_locators_reference_source_nodes(self):
        nodes = {node["id"]: node for node in GRAPH["nodes"]}
        for node in GRAPH["nodes"]:
            for locator in node.get("source_locators", []):
                self.assertIn(locator["source_node_id"], nodes)
                self.assertEqual(nodes[locator["source_node_id"]]["type"], "source")

    def test_b3_and_section_23_are_not_asserted_as_same_run(self):
        b3 = next(n for n in GRAPH["nodes"] if n["id"] == "exp_b3")
        section = next(n for n in GRAPH["nodes"] if n["id"] == "exp_s23_microgravity_summary")
        self.assertNotEqual(b3["id"], section["id"])
        link = next(e for e in GRAPH["edges"] if e["id"] == "e_b3_possible_s23_record")
        self.assertEqual(link["status"], "unresolved")
        self.assertEqual(link["type"], "possible_record_correspondence")

    def test_flow_discrepancy_preserves_both_source_assertions(self):
        values = {
            n["attributes"]["value"]
            for n in GRAPH["nodes"]
            if n["id"] in {"assert_b3_flow_2", "assert_s23_flow_3"}
        }
        self.assertEqual(values, {2, 3})
        claim = next(n for n in GRAPH["nodes"] if n["id"] == "claim_b3_section_flow_discrepancy")
        self.assertEqual(claim["assertion_group_status"], "unresolved")

    def test_22_mm_s_maximum_is_not_linked_to_b3(self):
        assertion = next(n for n in GRAPH["nodes"] if n["id"] == "assert_s23_micro_max_2_2")
        self.assertEqual(assertion["attributes"]["value"], 2.2)
        self.assertEqual(assertion["attributes"]["statistic_type"], "maximum")
        self.assertEqual(assertion["attributes"]["run_linkage"], "not linked to B3")
        self.assertFalse(any(
            e["source"] == "assert_s23_micro_max_2_2" and e["target"] == "exp_b3"
            for e in GRAPH["edges"]
        ))

    def test_reported_mean_and_maximum_remain_distinct(self):
        mean = next(n for n in GRAPH["nodes"] if n["id"] == "assert_ground_avg_2_0")
        maximum = next(n for n in GRAPH["nodes"] if n["id"] == "assert_s23_micro_max_2_2")
        self.assertEqual(mean["attributes"]["statistic_type"], "average")
        self.assertEqual(maximum["attributes"]["statistic_type"], "maximum")

    def test_evidence_state_vocabulary_is_not_overloaded_with_conflict(self):
        for node in GRAPH["nodes"]:
            if "evidence_state" in node:
                self.assertNotEqual(node["evidence_state"], "conflicting")
        self.assertEqual(
            next(n for n in GRAPH["nodes"] if n["id"] == "claim_b3_section_flow_discrepancy")
            ["assertion_group_status"],
            "unresolved"
        )


if __name__ == "__main__":
    unittest.main()
