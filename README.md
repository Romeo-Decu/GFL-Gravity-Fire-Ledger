# FiF

**Flame in Freefall** — physics-aware scientific intelligence and evidence-transferability platform for microgravity combustion research.

FiF separates three questions that are often conflated:

1. **Retrieval relevance:** does a source address the question?
2. **Physical comparability:** are the governing conditions sufficiently characterized for the selected phenomenon and outcome?
3. **Evidence transferability:** can a finding inform another context, and within what declared limits?

Core safeguards: unknown is not compatible; source conflicts are not automatically physical incompatibilities; source-reported values are not FiF measurements; and software execution does not validate combustion physics.

## Current research case

The initial bounded case is flame spread over nominal 100-µm PMMA, comparing BASS-II microgravity and normal-gravity downward-spread summaries. The B3 / Section 2.3 record linkage remains unresolved. The 2 cm/s and 3 cm/s source assertions remain separate; the reported 2.2 mm/s microgravity maximum is not attributed to B3.

## Repository map

- `src/fif_transfer/` — deterministic assessment kernel.
- `configs/` — versioned, case-specific decision rules.
- `schemas/` — controlled vocabulary, assessment request and canonical evidence graph contracts.
- `research/` — scientific source audits and evidence fixtures.
- `tests/` — software contract and regression tests.
- `visualization/` — read-only browser evidence explorer prototype.

## Run the deterministic engine

```bash
python -m unittest discover -s tests -v
python -m fif_transfer --ruleset configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json --request examples/PMMA100_DOCUMENTARY_SUMMARY_REQUEST_v0.1.json
```

## Run the visualization prototype

See [visualization/README.md](visualization/README.md). It uses ELK for layout, Cytoscape.js for graph interaction and Plotly.js for a source-reported documentary discrepancy chart.

## Scientific status

FiF v0.1 is a research and software prototype. It is not a fire-prediction system, spacecraft fire-safety certification tool, autonomous controller, or independently validated combustion model. Raw B3/B6 video reconstruction and quantitative transfer validation have not been completed. B3 remains the primary transferability case; B6 is a separate reconstruction/method-validation case.


## Project control and completion roadmap

The authoritative project map, implementation baseline, staged work breakdown and completion gates are maintained in:
- [Master Project Map & Completion Roadmap v1.0](docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md)
- [Source Acquisition & Evidence Gap Register v1.0](research/SOURCE_ACQUISITION_AND_EVIDENCE_GAP_REGISTER_v1.0.md)
- [Master Test & Validation Plan v1.0](docs/TEST_AND_VALIDATION_MASTER_PLAN_v1.0.md)

Stage 1 (project baseline and roadmap) is closed as a documentation/control milestone only. Scientific evidence acquisition, B3/B6 reconstruction, transferability validation and production-platform work remain open.
