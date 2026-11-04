# FiF v0.1 Fixture-to-Test Traceability Matrix

**Date:** 2026-11-04  
**Purpose:** Distinguish implemented software checks from fixture requirements that need new data models or scientific evidence.  
**Important:** A test marked “covered” verifies software behavior only. It does not validate the scientific premise or source data.

## 1. Test inventory

| Test asset | Current scope |
|---|---|
| `tests/test_engine.py` | Gate-state evaluation, missing/unknown gates, conflicts, scoped incompatibilities, positive-gate metadata, N/A policy, deterministic output fingerprints |
| `tests/test_case_assessment.py` | Current PMMA-100 documentary summary, quantitative abstention, calibration/validation abstention |
| `tests/test_contracts.py` | Request/ruleset/vocabulary consistency, example request profiles/gates, fixture IDs and invariant IDs |
| `tests/test_evidence_graph.py` | PMMA-100 graph IDs, edge endpoints, source locators, unresolved record linkage, statistic distinction, B3 attribution safeguard |
| `visualization/tests/graph-adapter.test.mjs` | Canonical graph adapter validation, ELK input mapping, Cytoscape mapping, invalid endpoint/evidence-state rejection |

## 2. T01–T15 disposition

| ID | Expected behavior | Status | Evidence / next action |
|---|---|---|---|
| T01 | Documentary summary remains conditionally informative; quantitative transfer abstains | **Partially covered** | `test_case_assessment.py`; does not yet assert every listed must-preserve/must-not-claim item from the fixture |
| T02 | Gravity-alone causal claim blocked by holder, ignition, flow and run-linkage differences | **Not implemented** | Requires typed causal claim and explicit confounder/boundary-condition model |
| T03 | B3-to-2.2-mm/s attribution requires an explicit run/result join | **Partially represented** | Graph keeps B3 and §2.3 records separate and tests no direct attribution; no general join-validation engine exists |
| T04 | Known critical material mismatch without bridge blocks quantitative transfer | **Partially covered** | Generic critical-incompatibility test; does not validate material identity or bridge evidence |
| T05 | Missing critical oxygen remains unknown | **Partially represented** | Missing required gate becomes unknown; no run-level quantity ingestion/defaulting subsystem exists |
| T06 | Conflicting 2/3 cm/s assertions remain unresolved; never average/select silently | **Partially covered** | Engine conflict test and graph fixture preserve separate values; no general assertion-resolution service |
| T07 | Maximum and mean are not equivalent statistics | **Partially represented** | Graph stores 2.2 maximum and 2.0 average separately; no general statistic-compatibility evaluator |
| T08 | Unit conversion preserves source value/unit and records conversion lineage | **Not implemented** | Requires typed quantity and transformation records |
| T09 | Gravity difference may be bridged only by validated model within domain | **Not implemented** | Current `bridge_status=validated` is a caller declaration, not independently verified bridge evidence |
| T10 | Source-reported regime interpretation remains distinct from FiF regime assessment | **Partially represented** | Graph/evidence contract separates source assertions and assessments; no dedicated regime evaluator/test |
| T11 | Independent raw-video reconstruction and uncertainty agreement support bounded validation | **Not implemented** | No target-video processing or independent measurement reconstruction has been performed |
| T12 | Threshold/calibration sensitivity that cannot be bounded forces abstention | **Not implemented** | Requires image-measurement and uncertainty pipeline |
| T13 | Non-critical unknown does not automatically block unrelated inference | **Partially represented** | Conflict scope is tested; gate criticality/non-critical unknown policy is not implemented |
| T14 | Observable or combustion-phase mismatch without validated mapping blocks transfer | **Not implemented** | Requires typed observable/phenomenon ontology and mapping rules |
| T15 | NASA-reported uncertainty is never labelled FiF-reconstructed | **Partially represented** | Documentation and graph distinguish source-reported data; no general uncertainty-provenance service |

## 3. I01–I12 invariant disposition

| ID | Invariant | Status | Current coverage / gap |
|---|---|---|---|
| I01 | Unknown remains unknown after normalization | **Partially covered** | Missing gate becomes unknown; no general normalization layer exists |
| I02 | Conflicting assertions remain separately addressable | **Covered for PMMA-100 fixture** | Separate B3/§2.3 assertions and unresolved record relation are tested |
| I03 | Missing oxygen, pressure, velocity or thickness receives no implicit default | **Not implemented as a general rule** | No general experiment-condition ingestion/normalization subsystem |
| I04 | Every derived value links to parent assertions | **Not implemented** | Graph supports `derived_from`; no derived-value lineage validation |
| I05 | Mean, maximum, median and transient values are never silently equated | **Partially covered** | PMMA-100 mean/maximum distinction tested; no general statistic engine |
| I06 | Unit conversion preserves original value and unit | **Not implemented** | Quantity/conversion subsystem required |
| I07 | Failed critical gate cannot be offset by compatible dimensions | **Covered** | Direct regression test in `tests/test_engine.py`: a fail gate alone yields undetermined, not physical incompatibility |
| I08 | Every conclusion carries domain and prohibited extrapolations | **Partially covered** | Domain required; prohibited list is preserved but not required to be non-empty |
| I09 | Source interpretation and FiF assessment remain separate | **Partially represented** | Graph has separate assertion and assessment nodes; generalized policy test pending |
| I10 | Same versioned inputs/rules yield deterministic output | **Covered** | Determinism and input-hash tests in `test_engine.py` |
| I11 | Every status includes rule IDs, evidence refs and reasons | **Partially covered** | Positive `pass` requires all three; partial/fail/unknown states may still lack some metadata |
| I12 | Source-reported uncertainty is never labelled independently reproduced by FiF | **Partially represented** | Research docs and graph labels preserve distinction; no uncertainty provenance engine |

## 4. Interpretation

The present engine should be described as a deterministic, conservative **assessment kernel**. It can enforce selected decision-path rules on caller-supplied statuses. It cannot yet execute the entire scientific fixture contract.

The next engineering increments should not be a large all-at-once implementation. Build separate, testable contracts for:
1. source assertions and assertion groups;
2. typed quantities, units, statistics and conversions;
3. run/sample/result identity joins;
4. physical incompatibility and validated bridge evidence;
5. measurement reconstruction and uncertainty provenance;
6. outcome-specific observable and regime mapping.

A fixture may remain deliberately deferred until the corresponding scientific data and subsystem exist. Do not convert a scientific acceptance requirement into a synthetic pass merely to increase test coverage.
