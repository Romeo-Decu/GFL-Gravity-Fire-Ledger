# ADR-001 — FiF Visualization Architecture

- **Status:** Accepted for prototype; production adoption remains gated by evaluation.
- **Date:** 2026-11-04
- **Decision owner:** FiF Project Manager
- **Scope:** Experiment maps, evidence provenance, process flows, scientific plots and multi-platform presentation.

## 1. Context

FiF must let researchers inspect how a conclusion is connected to source documents, investigations, experiments, samples, configurations, measurements, claims, comparisons, assessments and uncertainty. It must also present scientific observations without confusing visual proximity or semantic similarity with physical equivalence.

No single visualization library is appropriate for all these tasks. Graph layout, graph rendering and scientific plotting are separate responsibilities.

## 2. Decision

Adopt a layered, renderer-independent visualization architecture:

| Responsibility | Selected technology | Intended use |
|---|---|---|
| Automatic graph layout | Eclipse Layout Kernel via `elkjs` | Hierarchical experiment maps, directed evidence flows, ports and edge routing |
| Interactive graph rendering | Cytoscape.js | Provenance networks, source-to-claim traceability, filtering, selection and neighborhood exploration |
| Scientific plotting | Plotly / Plotly.js | Time series, spread-rate curves, uncertainty intervals, distributions, sensitivity plots and 3D scientific charts |
| Canonical visualization data | Versioned FiF graph/plot JSON contracts | Preserve identity, provenance and semantics independently of the renderer |
| Application shell | Web-first, platform-independent UI | Browser first; desktop packaging only when justified by user needs |

### 2.1 ELK is a layout engine, not a renderer

ELK/elkjs computes graph positions and edge routing. It does not render or style the diagram. The initial implementation will use ELK Layered for directed process and provenance views, with alternative algorithms evaluated only where the data structure requires them.

The initial prototype will pin a tested elkjs release. The package's dual EPL-2.0/GPL-3.0-or-later licensing must be reviewed and recorded before redistribution.

### 2.2 Cytoscape.js is the graph interaction layer

Cytoscape.js will render and support exploration of evidence networks. It will consume a FiF-owned graph representation; its internal graph model will not become the authoritative scientific database.

ELK coordinates will be adapted into Cytoscape element positions. A small adapter will isolate the two libraries and permit future renderer replacement.

### 2.3 Plotly is the scientific chart layer

Plotly will handle numerical and scientific plots. Graph-network renderers must not be used as substitutes for scientific charting.

Every plotted datum must retain a route to its source measurement or derived assertion, including units, processing method, uncertainty, and evidence state where applicable. Unknown or inferred values must be visibly distinguished from measured and source-reported values.

## 3. Why not adopt Eclipse GLSP immediately?

Eclipse GLSP is a capable framework for building graphical editors with client/server separation and integrations across web applications, Electron, VS Code and Eclipse-based platforms. It is not required for the first FiF visualization milestone.

FiF initially needs trustworthy read/explore views, not a general-purpose graphical language editor. GLSP would introduce a larger editing protocol, server framework and client integration surface before the requirements justify them.

Reconsider GLSP if FiF later requires users to author or edit formal graphical models, enforce graphical editing semantics, or integrate deeply into IDE platforms.

## 4. Multi-platform strategy

- The first target is a responsive browser application.
- Core scientific services and canonical data contracts remain independent of the frontend.
- Visualization adapters remain isolated behind stable interfaces.
- Desktop distribution (Electron or another wrapper) is deferred until there is a demonstrated need for offline workflows, local instrument integration or controlled institutional deployment.
- No cloud vendor lock-in is introduced by the visualization layer.

“Native rendering” means using the host platform's supported browser/WebView rendering stack initially. Native desktop packaging is a later deployment choice, not a reason to duplicate scientific logic.

## 5. Scientific and traceability constraints

1. Visual links must reference stable FiF entity IDs and source locations.
2. A graph edge must carry a typed relation, direction, provenance and evidence status.
3. Layout coordinates, visual clusters and proximity must never imply scientific equivalence.
4. Filters and visual emphasis must not silently remove contradictory or unknown evidence from the audit view.
5. Clicking a result or measurement must expose its source, units, transformation history and uncertainty.
6. A derived value must link to its parent assertions and calculation method.
7. Screenshots and exports must include the applicable dataset/ruleset versions and a timestamp or snapshot identifier.
8. Rendering must not mutate source records or assessment outcomes.

## 6. Prototype acceptance criteria

The first vertical slice will use the PMMA-100 case and demonstrate:

- source → investigation → experiment → sample → measurement → claim → comparison → assessment traceability;
- visible separation of source-reported, measured, derived, inferred and unknown evidence;
- visible unresolved B3 flow discrepancy (2 cm/s versus 3 cm/s) without silently choosing a value;
- selection of a conclusion and navigation back to supporting source locations;
- at least one time-series/scientific plot with unit and uncertainty metadata;
- deterministic export of the underlying graph/plot JSON;
- same canonical data rendered consistently in at least two supported browser engines.

The prototype will not invent missing B3 run links, infer a B3-to-2.2-mm/s join, or claim independent measurement reconstruction.

## 7. Consequences

Positive:
- Each library has a narrow, explicit responsibility.
- Scientific data remains portable and renderer-independent.
- The design supports future web/desktop clients without duplicating scientific logic.
- Traceability becomes a first-class interaction rather than a decorative graph.

Costs and risks:
- Three visualization technologies increase dependency and maintenance surface.
- elkjs licensing must be reviewed for the intended distribution model.
- Large evidence graphs require performance testing and progressive loading.
- Visual accessibility and color-independent evidence encoding must be tested.
- Cytoscape/ELK integration needs a stable coordinate and compound-node adapter.

## 8. References

- Eclipse Layout Kernel: https://eclipse.dev/elk/
- elkjs package: https://www.npmjs.com/package/elkjs
- Cytoscape.js: https://js.cytoscape.org/
- Plotly: https://plotly.com/graphs/
- Eclipse GLSP: https://eclipse.dev/glsp/documentation/overview/
