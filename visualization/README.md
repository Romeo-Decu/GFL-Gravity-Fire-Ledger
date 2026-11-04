# FiF Evidence Explorer — Prototype v0.1

A browser-first, read-only prototype for inspecting the canonical PMMA-100 evidence graph.

## What it demonstrates

- ELK Layered computes graph node positions.
- Cytoscape.js renders the interactive provenance graph.
- Selecting a node or edge exposes its identity, evidence state, attributes, relation status and source locator.
- Unresolved and provisional edges are visually distinguished from established edges.
- Plotly renders the B3 2 cm/s and Section 2.3 3 cm/s source-reported flow assertions as two separate documentary records. It explicitly states that run correspondence is unresolved and that uncertainty for these flow settings is not reported.
- The graph is loaded from the canonical JSON fixture. The browser adapter does not rewrite the source data.

## Run locally

From the repository root, use Python's static server:

```bash
python -m http.server 8000
```

Open:

```
http://localhost:8000/visualization/
```

Internet access is required for the pinned CDN-hosted ELK, Cytoscape.js and Plotly.js prototype libraries.

## Run adapter tests

From the repository root:

```bash
npm --prefix visualization test
npm --prefix visualization run check
```

The tests use Node's built-in test runner and require Node.js 20 or later. No npm runtime dependencies are installed by this prototype package.

## Important limitations

- This is a research visualization prototype, not a production application.
- It is read-only; no graph editing, persistence or scientific inference is performed in the browser.
- The graph validator checks basic graph integrity. It does not yet validate all JSON Schema constraints, source truth, physical compatibility or complete provenance lineage.
- ELK node positions are adapted to Cytoscape. Exact ELK edge-section routing is not yet transferred into Cytoscape's edge geometry.
- Browser rendering has not yet been validated in two browser engines or against accessibility/performance criteria.
- No raw B3 video is loaded or reconstructed.
- The Plotly chart displays source-reported documentary settings, not measured values or a proven same-run difference.

## Library versions and licensing notes

- elkjs 0.12.1 — package declares EPL-2.0 OR GPL-3.0-or-later; prototype elects EPL-2.0 for the unmodified dependency, subject to distribution review.
- Cytoscape.js 3.34.4 — MIT.
- Plotly.js 4.1.2 — MIT.

Production bundling and third-party notice packaging remain future tasks.
