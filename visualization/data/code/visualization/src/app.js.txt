import * as FIFGraphAdapter from "./graph-adapter.js";

const GRAPH_URL = "/research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.2.json";
const graphCanvas = document.getElementById("graph");
const detailPanel = document.getElementById("details");
const statusLine = document.getElementById("status");
const searchInput = document.getElementById("search");
const exportButton = document.getElementById("export-graph");

function renderDetails(title, lines, links = []) {
  detailPanel.replaceChildren();
  const heading = document.createElement("h3");
  heading.textContent = title;
  detailPanel.append(heading);
  for (const [key, value] of lines) {
    const row = document.createElement("div");
    row.className = "detail-row";
    const label = document.createElement("span");
    label.className = "detail-key";
    label.textContent = key;
    const text = document.createElement("span");
    text.className = "detail-value";
    text.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    row.append(label, text);
    detailPanel.append(row);
  }
  for (const link of links) {
    const anchor = document.createElement("a");
    anchor.href = link.url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.textContent = link.label;
    detailPanel.append(anchor);
  }
}

function sourceUrl(sourceNodeId) {
  const source = window.fifGraph?.nodes.find(node => node.id === sourceNodeId);
  return source?.attributes?.url ?? null;
}

function nodeDetails(node) {
  const attributes = node.data("attributes");
  const lines = [
    ["ID", node.data("id")],
    ["Type", node.data("type")],
    ["Evidence state", node.data("evidenceState")],
    ["Assertion group", node.data("assertionGroupStatus") || "not specified"],
    ["Description", node.data("description") || "—"],
    ["Attributes", attributes]
  ];
  const links = node.data("sourceLocators").map(locator => ({
    label: `${locator.location_type}: ${locator.locator} (source node ${locator.source_node_id})`,
    url: sourceUrl(locator.source_node_id)
  })).filter(link => link.url);
  if (attributes.url) links.push({ label: "Open source record", url: attributes.url });
  renderDetails(node.data("label"), lines, links);
}

function edgeDetails(edge) {
  renderDetails(edge.data("label"), [
    ["ID", edge.data("id")],
    ["Relation", edge.data("type")],
    ["Status", edge.data("status")],
    ["From", edge.data("source")],
    ["To", edge.data("target")],
    ["Description", edge.data("description") || "—"]
  ]);
}

function drawFlowDiscrepancy(graph) {
  const b3 = graph.nodes.find(node => node.id === "assert_b3_flow_2");
  const section = graph.nodes.find(node => node.id === "assert_s23_flow_3");
  const records = [
    {
      x: b3.attributes.value,
      y: "B3 — Appendix A.1",
      customdata: ["source_reported", "NASA/TM-20210011385, Appendix A.1, B3 row", "not reported"]
    },
    {
      x: section.attributes.value,
      y: "Section 2.3 summary",
      customdata: ["source_reported", "NASA/TM-20210011385, §2.3.6", "not reported"]
    }
  ];
  Plotly.newPlot("plot", [{
    type: "scatter",
    mode: "markers+text",
    x: records.map(item => item.x),
    y: records.map(item => item.y),
    text: records.map(item => `${item.x} cm/s`),
    textposition: "middle right",
    customdata: records.map(item => item.customdata),
    marker: { size: 14, symbol: ["circle", "diamond"] },
    hovertemplate: "<b>%{y}</b><br>Reported value: %{x} cm/s<br>Evidence: %{customdata[0]}<br>Source: %{customdata[1]}<br>Uncertainty: %{customdata[2]}<extra></extra>"
  }], {
    margin: { l: 150, r: 28, t: 18, b: 48 },
    paper_bgcolor: "#16212f", font: { color: "#d8e1ea" },
    plot_bgcolor: "#16212f",
    xaxis: { title: "Reported opposing-flow setting (cm/s)", rangemode: "tozero", gridcolor: "#26364a" },
    yaxis: { automargin: true, gridcolor: "#1c2a3b" },
    annotations: [{
      x: 0.5, y: -0.42, xref: "paper", yref: "paper",
      text: "Record correspondence unresolved. Values are not established as the same run. Uncertainty not reported for these settings.",
      showarrow: false, font: { size: 11, color: "#e8a46a" }
    }],
    showlegend: false
  }, { responsive: true, displaylogo: false });
}

async function start() {
  try {
    statusLine.textContent = "Loading canonical evidence graph…";
    if (typeof ELK === "undefined" || typeof cytoscape === "undefined" || typeof Plotly === "undefined") {
      throw new Error("A visualization library failed to load. Check the network/CDN connection.");
    }
    const elk = new ELK({ algorithms: ["layered"] });
    const response = await fetch(GRAPH_URL);
    if (!response.ok) throw new Error(`Graph request failed: ${response.status}`);
    const graph = await response.json();
    window.fifGraph = graph;
    exportButton.addEventListener("click", () => {
      const snapshot = JSON.stringify(graph, null, 2) + "\n";
      const blob = new Blob([snapshot], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${graph.graph_id}.json`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });

    const errors = FIFGraphAdapter.validateGraph(graph);
    if (errors.length) throw new Error(errors.join(" "));
    statusLine.textContent = `${graph.nodes.length} nodes · ${graph.edges.length} edges · published records and GFL measurements`;

    const elkGraph = await elk.layout(FIFGraphAdapter.toElkGraph(graph));
    const elements = FIFGraphAdapter.toCytoscapeElements(graph, elkGraph);
    const cy = cytoscape({
      container: graphCanvas,
      elements,
      layout: { name: "preset", fit: true, padding: 36 },
      minZoom: 0.15,
      maxZoom: 2.5,
      wheelSensitivity: 0.18,
      pixelRatio: 1,
      style: [
        { selector: "node", style: {
          "label": "data(label)", "text-wrap": "wrap", "text-max-width": 180,
          "font-size": 10, "font-family": "Inter, Arial, sans-serif",
          "color": "#d8e1ea", "text-valign": "center", "text-halign": "center",
          "background-color": "#1c2a3b", "border-width": 1.5, "border-color": "#8a9bb0",
          "width": 210, "height": 76, "shape": "round-rectangle", "padding": 8
        }},
        { selector: "node.source", style: { "background-color": "#1c2a3b", "border-color": "#6cb4ff" }},
        { selector: "node.assertion", style: { "background-color": "#16261f", "border-color": "#5fc79a" }},
        { selector: "node.claim", style: { "background-color": "#2a1e12", "border-color": "#e8a46a", "border-style": "dashed" }},
        { selector: "node.assessment", style: { "background-color": "#211c33", "border-color": "#b39ae6", "border-width": 2.5 }},
        { selector: "node.unknown", style: { "border-style": "dotted", "border-width": 3 }},
        { selector: "node.inferred", style: { "border-style": "dashed" }},
        { selector: "edge", style: {
          "curve-style": "bezier", "width": 1.5, "line-color": "#5b6675",
          "target-arrow-color": "#8a9bb0", "target-arrow-shape": "triangle",
          "arrow-scale": 0.85, "label": "data(label)", "font-size": 7,
          "text-rotation": "autorotate", "text-background-opacity": 0.9,
          "text-background-color": "#16212f", "text-background-padding": 2,
          "color": "#8a9bb0"
        }},
        { selector: "edge.unresolved", style: { "line-style": "dashed", "line-color": "#e8833a", "target-arrow-color": "#e8833a", "width": 2.5 }},
        { selector: "edge.provisional", style: { "line-style": "dotted", "line-color": "#8a9bb0" }},
        { selector: "edge.rejected", style: { "line-style": "dashed", "line-color": "#e8833a", "target-arrow-color": "#e8833a" }},
        { selector: ":selected", style: { "border-width": 4, "border-color": "#6cb4ff", "line-color": "#6cb4ff", "target-arrow-color": "#6cb4ff" }}
      ]
    });

    window.fifCy = cy;
    cy.on("tap", "node", event => nodeDetails(event.target));
    cy.on("tap", "edge", event => edgeDetails(event.target));
    cy.on("tap", event => {
      if (event.target === cy) renderDetails("Evidence details", [["Instruction", "Select a node or edge to inspect provenance and evidence state."]]);
    });

    searchInput.addEventListener("input", () => {
      const term = searchInput.value.trim().toLowerCase();
      cy.nodes().forEach(node => {
        const haystack = [node.data("label"), node.data("id"), node.data("type"), node.data("evidenceState")].join(" ").toLowerCase();
        node.style("opacity", !term || haystack.includes(term) ? 1 : 0.12);
      });
      cy.edges().forEach(edge => {
        if (!term) {
          edge.style("opacity", 1);
          return;
        }
        const source = cy.getElementById(edge.data("source"));
        const target = cy.getElementById(edge.data("target"));
        const related = Number(source.style("opacity")) > 0.5 || Number(target.style("opacity")) > 0.5;
        edge.style("opacity", related ? 0.9 : 0.08);
      });
    });

    drawFlowDiscrepancy(graph);
    renderDetails("PMMA-100 evidence graph", [
      ["Case", graph.case_id],
      ["Graph status", graph.status],
      ["Purpose", graph.metadata.purpose],
      ["Important", "The graph preserves unresolved source-record correspondence; it does not prove B3 is the Section 2.3 run."]
    ]);
  } catch (error) {
    statusLine.textContent = "Prototype could not load.";
    renderDetails("Load error", [["Error", error.message]]);
  }
}

start();
