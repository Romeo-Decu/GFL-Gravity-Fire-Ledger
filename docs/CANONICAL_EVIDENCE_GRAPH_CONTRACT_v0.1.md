# FiF Canonical Evidence Graph — Data Contract v0.1

**Status:** Working contract / prototype input  
**Schema:** `schemas/EVIDENCE_GRAPH_v0.1.schema.json`  
**Case fixture:** `research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json`

## 1. Purpose

The canonical graph is the renderer-independent representation of scientific evidence lineage. It is not the scientific database schema in its final form, and it does not itself assess physical transferability. Its purpose is to preserve identity, provenance, source assertions, relationships, uncertainty states and inference outcomes in a form that can be rendered by different clients without changing their meaning.

## 2. Node classes

| Node type | Meaning |
|---|---|
| source | A document, dataset, archive or other source record |
| investigation | A named research campaign or investigation |
| experiment | A run, experiment or explicitly aggregated experiment record |
| configuration | Declared apparatus, atmosphere, flow or operating conditions |
| sample | A physical specimen or sample identity |
| measurement | A measurement object with quantity, unit, method and uncertainty metadata |
| assertion | A source-reported, measured, derived or inferred statement/value |
| claim | A bounded proposition that may be supported, challenged or left unresolved |
| comparison | An outcome-specific comparison of evidence objects |
| assessment | A versioned inference result for one intended inference |

Node IDs are stable graph-local identifiers. Source IDs and run IDs must not be silently normalized into one identity. Aliases are explicit metadata, not replacements.

## 3. Evidence semantics

Use the controlled vocabulary in `schemas/CONTROLLED_VOCABULARY_v0.1.json`:
- `measured`
- `source_reported`
- `derived`
- `inferred`
- `unknown`

Do not use `conflicting` as an individual evidence state. Conflicts belong to assertion-group or dimension status. Multiple assertions remain individually addressable, each retaining its source and source locator.

A source-reported value must never be relabelled as independently measured by FiF. A derived value must eventually link to its parent assertion(s) and a recorded calculation/transformation method.

## 4. Edge semantics

Edges are directed and typed. v0.1 supports:
- documentary/provenance: `documents`, `reports`
- experimental structure: `part_of`, `uses_configuration`, `uses_sample`, `produces`
- evidence logic: `supports`, `contradicts`, `derived_from`
- analysis: `compares`, `assesses`, `contextualizes`
- uncertain identity linkage: `possible_record_correspondence`

The edge's status is one of `established`, `provisional`, `unresolved`, or `rejected`. A provisional or unresolved edge must not be rendered as an established join. Unscoped or missing joins are not filled by visual proximity.

## 5. Presentation metadata

The optional `presentation` object is renderer-only metadata (coordinates, grouping, collapsed state and style key). It must never be used by the assessment engine, evidence normalizer or physical-comparability rules. ELK may calculate positions; Cytoscape may render and interact with them. Neither may change evidence or edge status.

## 6. PMMA-100 fixture invariants

The fixture deliberately preserves:
1. BASS-II B3 / sample 148 and the Section 2.3 nominal 100-µm microgravity comparison as separate experiment records.
2. B3 Appendix A.1 flow of 2 cm/s and Section 2.3 flow of 3 cm/s as separate source-reported assertions.
3. The possible record correspondence between B3 and the Section 2.3 comparison as unresolved, not established.
4. The reported ~2.2 mm/s microgravity maximum as a section-level maximum, not a B3 measurement.
5. The reported 2.0 mm/s normal-gravity downward average as a separate statistic and experiment summary.
6. B3 calibrated and uncalibrated oxygen readings as separate assertions.
7. Unknown sample grade/batch and missing run-level linkage as unknown, not compatible.

The graph is a documentary representation of the current source audit. It is not an independent reconstruction of the NASA measurements and not a validation result.

## 7. Validation responsibilities

The JSON Schema checks object shape and allowed enumerations. It does not establish cross-reference integrity, source truth, scientific consistency or physical equivalence. The test suite separately checks:
- node/edge ID uniqueness;
- edge endpoint existence;
- source locator references;
- B3 / Section 2.3 identity separation;
- unresolved flow-record relationship;
- no B3 attribution of the 2.2 mm/s maximum;
- mean/maximum statistic separation.

A future graph validator must also check source-node references, edge-type endpoint constraints, provenance completeness for derived assertions, and graph-version compatibility.

## 8. Visualization requirements

- Preserve node and edge IDs in all renderer adapters and exports.
- Make source-reported, measured, derived, inferred and unknown states visually distinguishable without relying on color alone.
- Make unresolved/provisional edges visibly different from established edges.
- Never hide unresolved assertions or conflicts through filtering without an explicit “show all evidence” route.
- Selecting a claim or assessment must expose supporting and contradictory evidence plus source locators.
- Graph layout must be deterministic for a fixed graph and pinned layout-engine version where feasible.
- Export the canonical graph, not a Cytoscape/ELK-specific graph as the scientific record.

## 9. Known limitations

The v0.1 schema is intentionally permissive for `attributes` and does not yet encode complete dimensional quantity objects, uncertainty decomposition, transformation lineage, or inference-specific gate assessments. Those require dedicated versioned subcontracts; they must not be improvised in renderer metadata.
