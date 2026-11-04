const NODE_TYPES = new Set([
  "source", "investigation", "experiment", "configuration", "sample",
  "measurement", "assertion", "claim", "comparison", "assessment"
]);
const EVIDENCE_STATES = new Set(["measured", "source_reported", "derived", "inferred", "unknown"]);
const EDGE_STATUSES = new Set(["established", "provisional", "unresolved", "rejected"]);

export function validateGraph(graph) {
  const errors = [];
  if (!graph || typeof graph !== "object") return ["Graph must be an object."];
  if (graph.schema_version !== "0.1.0") errors.push("Unsupported graph schema version.");
  if (!Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) {
    return [...errors, "Graph nodes and edges must be arrays."];
  }

  const nodeIds = new Set();
  for (const node of graph.nodes) {
    if (!node?.id || nodeIds.has(node.id)) errors.push(`Missing or duplicate node ID: ${node?.id ?? "(missing)"}`);
    else nodeIds.add(node.id);
    if (!NODE_TYPES.has(node?.type)) errors.push(`Invalid node type for ${node?.id ?? "(missing)"}.`);
    if (!node?.label) errors.push(`Node ${node?.id ?? "(missing)"} has no label.`);
    if (node?.evidence_state && !EVIDENCE_STATES.has(node.evidence_state)) {
      errors.push(`Invalid evidence state on ${node.id}.`);
    }
    if (node?.evidence_state === "conflicting") {
      errors.push(`Conflict must be represented at assertion-group level, not evidence_state (${node.id}).`);
    }
  }

  const edgeIds = new Set();
  for (const edge of graph.edges) {
    if (!edge?.id || edgeIds.has(edge.id)) errors.push(`Missing or duplicate edge ID: ${edge?.id ?? "(missing)"}`);
    else edgeIds.add(edge.id);
    if (!nodeIds.has(edge?.source)) errors.push(`Edge ${edge?.id ?? "(missing)"} has unknown source node.`);
    if (!nodeIds.has(edge?.target)) errors.push(`Edge ${edge?.id ?? "(missing)"} has unknown target node.`);
    if (edge?.status && !EDGE_STATUSES.has(edge.status)) errors.push(`Invalid edge status on ${edge.id}.`);
  }

  for (const node of graph.nodes) {
    for (const locator of node.source_locators ?? []) {
      const source = graph.nodes.find(candidate => candidate.id === locator.source_node_id);
      if (!source || source.type !== "source") {
        errors.push(`Source locator on ${node.id} does not reference a source node.`);
      }
    }
  }
  return errors;
}

export function toElkGraph(graph) {
  return {
    id: "fif-root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "RIGHT",
      "elk.edgeRouting": "ORTHOGONAL",
      "elk.spacing.nodeNode": "36",
      "elk.layered.spacing.nodeNodeBetweenLayers": "72"
    },
    children: graph.nodes.map(node => ({
      id: node.id,
      width: node.type === "source" || node.type === "assessment" ? 230 : 210,
      height: 88
    })),
    edges: graph.edges.map(edge => ({
      id: edge.id,
      sources: [edge.source],
      targets: [edge.target]
    }))
  };
}

export function toCytoscapeElements(graph, layout) {
  const positions = new Map((layout?.children ?? []).map(node => [
    node.id,
    { x: node.x + node.width / 2, y: node.y + node.height / 2 }
  ]));

  const nodes = graph.nodes.map(node => ({
    data: {
      id: node.id,
      label: node.label,
      type: node.type,
      evidenceState: node.evidence_state ?? "not-stated",
      description: node.description ?? "",
      attributes: node.attributes ?? {},
      sourceLocators: node.source_locators ?? [],
      assertionGroupStatus: node.assertion_group_status ?? ""
    },
    position: positions.get(node.id) ?? { x: 0, y: 0 },
    classes: [node.type, node.evidence_state ?? "not-stated"].join(" ")
  }));

  const edges = graph.edges.map(edge => ({
    data: {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.type.replaceAll("_", " "),
      type: edge.type,
      status: edge.status ?? "established",
      description: edge.description ?? ""
    },
    classes: edge.status ?? "established"
  }));

  return [...nodes, ...edges];
}
