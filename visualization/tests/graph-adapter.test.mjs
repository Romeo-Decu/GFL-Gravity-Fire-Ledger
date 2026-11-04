import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { validateGraph, toElkGraph, toCytoscapeElements } from "../src/graph-adapter.js";

const here = dirname(fileURLToPath(import.meta.url));
const graphPath = resolve(here, "../../research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json");
const graph = JSON.parse(readFileSync(graphPath, "utf8"));

test("canonical PMMA graph passes adapter validation", () => {
  assert.deepEqual(validateGraph(graph), []);
});

test("ELK adapter preserves every node and typed edge", () => {
  const elk = toElkGraph(graph);
  assert.equal(elk.children.length, graph.nodes.length);
  assert.equal(elk.edges.length, graph.edges.length);
  assert.equal(elk.layoutOptions["elk.algorithm"], "layered");
  assert.equal(elk.layoutOptions["elk.direction"], "RIGHT");
});

test("Cytoscape adapter preserves IDs, evidence states and edge statuses", () => {
  const fakeLayout = {
    children: graph.nodes.map((node, index) => ({
      id: node.id, x: index * 10, y: index * 5, width: 200, height: 80
    }))
  };
  const elements = toCytoscapeElements(graph, fakeLayout);
  const nodes = elements.filter(item => item.data.id && !item.data.source);
  const edges = elements.filter(item => item.data.source);
  assert.equal(nodes.length, graph.nodes.length);
  assert.equal(edges.length, graph.edges.length);
  assert.equal(nodes.find(item => item.data.id === "assert_b3_flow_2").data.evidenceState, "source_reported");
  assert.equal(edges.find(item => item.data.id === "e_b3_possible_s23_record").data.status, "unresolved");
});

test("adapter rejects unknown edge endpoints", () => {
  const broken = structuredClone(graph);
  broken.edges[0].target = "missing-node";
  assert.ok(validateGraph(broken).some(error => error.includes("unknown target")));
});

test("adapter rejects conflict as an individual evidence state", () => {
  const broken = structuredClone(graph);
  broken.nodes[0].evidence_state = "conflicting";
  assert.ok(validateGraph(broken).some(error => error.includes("assertion-group level")));
});
