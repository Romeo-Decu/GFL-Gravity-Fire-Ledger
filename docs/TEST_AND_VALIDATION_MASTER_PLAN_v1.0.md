# FiF — Master Test & Validation Plan v1.0

> **Historical planning document (early November 2026, when the project was called FiF), kept as written.** Current state of every function: `research/fixtures/GFL_CAPABILITIES_v1.json` and the Functions section of the dashboard.

**Purpose:** Define all software, data, scientific, user and release tests required from the current prototype through complete FiF v1.  
**Baseline:** 2026-11-04  
**Authority:** docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md  
**Rule:** software correctness, data integrity and scientific validity are separate test domains.

---

## 1. Current test baseline

### 1.1 Existing test assets

| Test area | Current files | Current coverage |
|---|---|---|
| Engine unit/regression | tests/test_engine.py | Gate-state behavior, unknowns, conflict scope, critical incompatibilities, N/A policy, deterministic outputs and input hashes. |
| Graph contract/invariants | tests/test_evidence_graph.py | Schema alignment, IDs, edge endpoints, source locators, B3/Section 2.3 separation, 2-vs-3 cm/s preservation, no B3-to-2.2-mm/s attribution, mean/maximum separation and explicit unknown B3 rate. |
| Case assessment | tests/test_case_assessment.py | Documentary summary remains conditional; quantitative transfer, model calibration and model validation abstain. |
| Contract tests | tests/test_contracts.py | Request schema/ruleset alignment, vocabulary, conflict and incompatibility contract, examples and fixture identifiers. |
| CLI tests | tests/test_cli.py | Documentary and quantitative examples, missing-request error. |
| Acquisition package tests | tests/test_acquisition_package.py | JSON shape/template, closed schema, controlled vocabulary, source-locator alignment and no self-asserted validation fields. |
| Visualization adapter | visualization/tests/graph-adapter.test.mjs | Canonical graph validation, preservation of node/edge IDs and evidence states, rejection of invalid endpoints and conflict-as-evidence-state. |
| Browser smoke | visualization/tests/browser-smoke.mjs | Browser graph loading, graph/Plotly rendering, source-link inspection, unknown measurement inspection and canonical JSON export. |

Current source contains **67 Python test methods** and **5 Node graph-adapter tests**, plus the browser smoke suite. This is a code inventory count, not a statement that all scientific acceptance scenarios are implemented.

### 1.2 Existing CI evidence

- PR #3 workflow run 41769248025: all Python 3.10–3.13 jobs passed; Node adapter tests, JS syntax checks, Playwright setup and Chromium/Firefox smoke tests passed.
- PR #4 workflow run 41770394680: same matrix and visualization/browser jobs passed.

These runs validate the tested software commits only. They do not validate NASA source values, video measurements, combustion physics or transferability.

The latest documentation-only commits on the current acquisition branch were not rerun through CI. No local test execution is claimed in this Stage 1 activity.

---

## 2. Test strategy and evidence hierarchy

Every release candidate must pass these independent layers:

1. **Static / schema checks** — source artefacts conform to contracts.
2. **Unit tests** — individual functions and rules behave as specified.
3. **Property / invariant tests** — forbidden states and silent data mutation cannot occur.
4. **Data integrity tests** — hashes, file manifests, IDs, references and source locators are valid.
5. **Numerical tests** — calculations, units, dimensions and uncertainty propagation are correct.
6. **Scientific regression tests** — outputs reproduce source-supported benchmark results within justified uncertainty.
7. **Integration tests** — ingestion, graph, engine, API and UI work as one system.
8. **AI/retrieval tests** — citations, retrieval quality, abstention and adversarial source handling.
9. **User / accessibility tests** — researchers can complete tasks correctly and safely.
10. **Security / licensing / privacy tests** — release does not expose secrets, violate source terms or create unsafe access.
11. **Performance / reproducibility tests** — same versioned inputs reproduce outputs under documented environments.
12. **Independent audit** — external reviewers challenge the exact release candidate.

A pass at one layer does not substitute for a pass at another. In particular, passing a unit test does not prove the scientific rule encoded by that test is physically valid.

---

## 3. Required software and contract tests

### 3.1 Schema validation

Implement full JSON Schema Draft 2020-12 validation for:
- acquisition packages;
- canonical evidence graph;
- assessment requests;
- rulesets;
- typed quantity and transformation records;
- source and asset records;
- validation/audit records when that subsystem is implemented.

Test:
- required and forbidden fields;
- enum and identifier constraints;
- nested object closure;
- numeric bounds and finite values;
- URI / date-time formats;
- invalid units and quantity types;
- malformed / truncated / oversized inputs;
- version compatibility and migration behavior.

Current gap: the CLI does not execute the full request schema validator. Static contract tests are not a substitute.

### 3.2 Engine unit and regression tests

Extend tests/test_engine.py to cover:
- every inference profile;
- missing and unknown gates;
- pass/partial/fail/N/A semantics;
- per-gate N/A authorization;
- scoped and unscoped conflicts;
- scoped and unscoped critical incompatibilities;
- validated / absent / unknown bridge status;
- evidence-reference resolution, not merely presence;
- unknown source ID and unknown locator rejection;
- source assertions that conflict;
- multiple sources supporting one claim;
- deterministic output and stable hashes;
- versioned ruleset and graph mismatch;
- malformed nested structures;
- fail-closed behavior for invalid input;
- replay with a different software build or ruleset version.

No positive inference may rely on an unresolved or nonexistent evidence reference.

### 3.3 Evidence graph and data-contract tests

Test:
- globally unique IDs within their declared namespace;
- all edges point to existing nodes;
- every source locator resolves to an actual source/file/table/page/figure/row/time interval;
- no graph node or metadata field can self-declare validation;
- every derived value links to its parent assertion(s) and method;
- source-reported, measured, derived, inferred and unknown states remain distinct;
- conflict groups preserve every source assertion;
- unresolved joins remain unresolved;
- graph export/import is lossless;
- renderer metadata cannot mutate scientific evidence;
- schema migration preserves IDs and provenance.

### 3.4 CLI and API tests

Test:
- successful invocation for every supported request profile;
- missing/invalid file paths;
- invalid JSON and invalid schema;
- unsupported schema/ruleset versions;
- controlled error codes and useful messages;
- deterministic machine-readable output;
- no traceback or secret leakage for user input errors;
- API authentication and authorization once API exists;
- pagination, query validation, rate limits and audit events.

---

## 4. Source, acquisition and data integrity tests

### 4.1 File integrity

For every acquired source asset:
- compute SHA-256 after download;
- verify byte size and format;
- verify archive opens and member list is complete;
- hash archive members;
- reject silent file replacement;
- record source URL, exact path, version and retrieval time;
- distinguish inaccessible, missing, removed, superseded and not-yet-retrieved assets;
- verify that a later re-download matches or create a new source version.

### 4.2 Table / structured data integrity

For PSI-25 CSV:
- confirm exact encoding, BOM, delimiter and line endings;
- preserve the 17 source column labels exactly;
- preserve original cell strings;
- preserve blank vs literal “none” vs zero vs negative value;
- preserve sample/test IDs as strings;
- test row uniqueness without assuming a missing test number is a missing record;
- reconcile page count 130 with 129 data rows;
- verify row-level hashes or a stable raw-file hash;
- compare normalized data against raw source cell-by-cell.

### 4.3 Cross-record integrity

Test:
- unique source, dataset, asset, experiment, sample and measurement IDs;
- no orphan extraction records;
- no dangling parent/child asset references;
- no source-to-experiment link without a locator;
- no experiment-to-file link based only on filename similarity;
- no measurement-to-run link without explicit evidence;
- no conversion or derived value without parent references;
- no hidden duplicate source IDs or aliases;
- candidate joins cannot be promoted by an acquisition agent's self-assertion.

### 4.4 Source reconciliation regression cases

The following values and unresolved differences must remain explicit:
- B3 PSI table: Air display 2 cm/s.
- B3 Carmignani: flow initial/final 2→0 cm/s.
- NASA Section 2.3: 3 cm/s.
- B3 calibrated O₂ 22.2→21.8%; uncalibrated 20.9→20.5%.
- B6 calibrated O₂ 21.0→20.9%; uncalibrated 20.1→20.0%.
- B6 NASA Fan display 0.9, 1.3, 2.75; Air display 3, 5, approaching 10 cm/s.
- B6 Carmignani Table A.2 flow 1→7 cm/s (initial/final, not a range).
- B3-specific spread rate remains unknown until a source/run join and measurement exist.
- Section 2.3 ~2.2 mm/s microgravity maximum remains a section-level maximum, not a B3 result.
- Section 2.3 ~2.0 mm/s ground average remains a separate statistic and unjoined run summary.

A regression test must fail if software silently selects, averages, overwrites or relabels any of these values.

---

## 5. Numerical and physical-model tests

### 5.1 Dimensional and unit tests

For every physical calculation:
- verify dimensional consistency symbolically or through explicit unit tests;
- use a controlled unit library or a documented dependency-free conversion table;
- reject incompatible dimensions;
- preserve original value and unit;
- record normalized value, conversion formula and constants;
- propagate conversion uncertainty where relevant;
- test round-trip conversion within numerical tolerance;
- test extreme, zero, negative and missing inputs.

### 5.2 Equation and limiting-case tests

For each model equation:
- document source, assumptions, derivation and validity range;
- verify units on every term;
- test limiting cases;
- compare with analytical solutions where available;
- compare with independent reference calculations;
- test numerical stability and sensitivity;
- verify that the model abstains outside its domain.

No equation should enter the production engine solely because it appears in a paper or prior FiF document.

### 5.3 Combustion-regime tests

For the thin-PMMA case:
- test regime classification against independently reviewed source evidence;
- distinguish thermal, kinetic and radiative limits;
- test sensitivity to local flow, oxygen, pressure, geometry, sample properties and heat losses;
- distinguish solid-phase heating/pyrolysis from gas-phase transport/reaction;
- do not infer a regime from one scalar indicator;
- do not assume microgravity means zero advection or zero effective acceleration;
- verify all selected dimensionless groups are relevant and computable from available inputs.

### 5.4 Transferability tests

For each target observable:
- identify source and target contexts;
- verify observable/statistic equivalence;
- identify critical and non-critical variables;
- test unknown critical values;
- test intentional differences such as gravity;
- require a validated bridge before quantitative transfer across critical differences;
- test qualitative vs quantitative conclusions separately;
- verify prohibited extrapolations;
- verify uncertainty and extrapolation limits are visible;
- require abstention when the evidence is insufficient.

---

## 6. Video measurement and uncertainty tests

Use research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md as the method baseline.

### 6.1 Media metadata and integrity

Test:
- archive/member hashes;
- stream count and stream identity;
- codec, dimensions, bit depth and pixel aspect ratio;
- acquisition frame rate versus container frame rate;
- variable frame rate and dropped/duplicated frames;
- timestamp monotonicity, gaps and discontinuities;
- audio and video clock alignment;
- original versus converted/still-sequence-derived media lineage.

### 6.2 Spatial and temporal calibration

Test:
- pixel/mm calibration from a source-supported reference in the same view;
- calibration uncertainty;
- perspective and lens distortion where material;
- camera orientation and sample geometry;
- timestamp offset and uncertainty;
- frame interval consistency;
- no reuse of a scale or threshold from another experiment without justification.

### 6.3 Image-analysis reproducibility

Test:
- segmentation on a blinded representative frame set;
- leading-edge and trailing-edge definition;
- threshold sensitivity;
- illumination and colour-space sensitivity;
- manual reference masks / independent annotators;
- repeatability across runs and analysts;
- FIAT/NASA method comparison;
- software version and parameter capture;
- failure detection when flame boundary is obscured or image quality is insufficient.

### 6.4 Spread-rate measurement

Test:
- selected fit interval is physically justified;
- ignition transient is excluded with documented rule;
- leading-edge position vs time is plotted with source frames;
- linear fit diagnostics and residuals are recorded;
- non-linear or regime-changing intervals are not forced into one slope;
- independent implementation or analyst reproduces the result;
- uncertainty includes spatial scale, timebase, segmentation, fit interval and between-frame variability;
- published NASA uncertainty is not copied as FiF uncertainty.

### 6.5 Figure digitization

For Carmignani Figure 5.8:
- retain the source figure image and page locator;
- calibrate axes independently for each plotted series;
- record digitization tool and version;
- preserve each point's coordinate and uncertainty;
- mark occluded/ambiguous points missing;
- do not infer timestamps from spacing unless defined by the figure;
- do not label digitized points as raw sensor measurements.

---

## 7. AI, retrieval and citation tests

These tests become mandatory when the AI/retrieval layer is implemented.

### 7.1 Retrieval quality
- Recall of known relevant sources and runs.
- Precision of top-ranked candidates.
- Correct source version and licence.
- Correct retrieval of exact table, page, figure and row.
- Correct distinction between similar names and different experiment IDs.
- Retrieval relevance is not displayed as physical comparability.

### 7.2 Synthesis fidelity
- Every factual claim has a resolvable citation.
- Citations support the exact claim and statistic.
- No source values or units are altered.
- No mean/maximum or run/section-level statistics are conflated.
- Unknown, conflict and missingness remain visible.
- Source interpretation is distinguished from FiF assessment.
- The model abstains when evidence is absent.
- The model cannot invent a source locator, file, run ID or value.

### 7.3 Adversarial tests
- Prompt injection embedded in source documents.
- Malicious or misleading metadata.
- Conflicting primary and secondary sources.
- False run joins suggested by similar filenames.
- Incorrect unit conversions and implausible values.
- Secondary source mislabelling calibrated/uncalibrated fields.
- Requests to overstate prediction, certification or operational capability.

---

## 8. Integration and end-to-end acceptance tests

The complete vertical slice must execute:

1. User submits a bounded combustion research question.
2. Query is parsed into target phenomenon, observable, material and conditions.
3. Retrieval finds source documents, investigation records and candidate experiments.
4. Every candidate has source locators and retrieval rationale.
5. Source assertions are extracted without changing original values.
6. Identity and provenance validators resolve or expose missing links.
7. Physical comparability is evaluated by dimension and target outcome.
8. Transferability engine evaluates gates, conflicts, bridges and uncertainty.
9. Result includes supported / conditional / qualitative / not transferable / undetermined outcome as justified.
10. UI displays the result, source chain, contradictions, unknowns and prohibited extrapolations.
11. User exports a deterministic evidence and assessment snapshot.
12. Replaying the same pinned inputs produces the same deterministic core output.

Acceptance scenarios:
- B3 documentary summary can be informative while quantitative transfer remains undetermined.
- B3 2 cm/s and Section 2.3 3 cm/s remain separate and unresolved.
- B3 is never assigned the 2.2 mm/s result without an explicit source join.
- B6 calibrated O₂ is 21.0→20.9%, not 20.1→20.0%.
- B6 flow representations remain source-specific until calibration/time synchronization is verified.
- Mean and maximum are never treated as the same statistic.
- Unknown critical oxygen/flow/material/run identity blocks quantitative transfer.
- A non-critical unknown does not block an unrelated inference.
- A validated bridge is accepted only when its evidence and domain are independently verifiable.
- The application can explain why it abstains.

---

## 9. User interface, accessibility and usability tests

### 9.1 Core task usability
A researcher must be able to:
- find an investigation and experiment;
- inspect exact source and asset lineage;
- understand the evidence state of a value;
- see what is missing or contradictory;
- compare two experiments for a named observable;
- understand why transfer is allowed, limited or withheld;
- navigate from a conclusion back to source evidence;
- export a reproducible result.

Test with representative users who did not build the UI. Record task success, errors, time, comprehension and confidence calibration.

### 9.2 Accessibility
- Keyboard-only operation.
- Visible focus state and logical focus order.
- Screen-reader labels and meaningful names.
- Contrast and non-colour encoding of evidence states.
- Scalable text and responsive layout.
- Accessible tables and charts / text alternatives.
- Reduced motion where applicable.
- Touch target size and small-screen behavior.

Target WCAG 2.2 AA for release, with documented exceptions if any.

### 9.3 Visualization integrity
- Graph position and visual proximity never imply scientific equivalence.
- Unresolved/provisional edges remain visually distinct.
- Filters cannot silently hide contradictory/unknown evidence from audit views.
- Chart statistic, unit, source, uncertainty and linkage status are visible.
- Exported graph is identical to canonical graph data.
- Large graph performance is measured against declared graph-size targets.

---

## 10. Security, privacy, licensing and operations tests

Before release:
- secret scanning and credential audit;
- dependency and vulnerability scan;
- least-privilege API and agent access;
- authorization tests for read/write roles;
- input validation and file-upload safety;
- protection against malicious PDF/HTML/CSV content;
- prompt-injection controls for retrieved sources;
- audit log integrity and retention;
- privacy review for user queries and any uploaded material;
- source licence and redistribution review;
- third-party dependency licence notices (including ELK, Cytoscape, Plotly, Playwright);
- backup/restore and disaster recovery;
- cloud budget, quotas, alerts and automatic teardown;
- no secrets or large source archives in Git history.

---

## 11. Reproducibility and release tests

A release candidate must be reproducible from:
- exact Git commit;
- Python and Node versions;
- dependency lock/pinned dependency versions;
- source snapshot identifiers and SHA-256 hashes;
- schemas and ruleset versions;
- processing code and configuration;
- raw input references;
- generated outputs and audit records.

Test:
- clean install from a fresh environment;
- full test suite;
- deterministic output replay;
- export/import round trip;
- clean deployment and rollback;
- supported browser matrix;
- release build hash;
- documentation links;
- user guide and known limitations;
- demo scenario replay.

---

## 12. Fixture traceability: T01–T15 and I01–I12

The current disposition in research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md is the baseline. The table below summarizes what must be achieved before the relevant scientific engine release.

### 12.1 T-series

| ID | Required behavior | Current status | Required completion |
|---|---|---|---|
| T01 | Documentary summary remains conditional; quantitative transfer abstains | Partially covered | Add full must-preserve / must-not-claim assertions. |
| T02 | Gravity-alone causal claim blocked by holder, ignition, flow and run-linkage differences | Not implemented | Typed causal claim and confounder/boundary-condition model. |
| T03 | B3-to-2.2-mm/s attribution requires explicit run/result join | Partially represented | General join validator and explicit source evidence. |
| T04 | Critical material mismatch without bridge blocks quantitative transfer | Partially covered | Validate material identity and bridge evidence. |
| T05 | Missing critical oxygen remains unknown | Partially represented | Typed quantity ingestion and no-default rules. |
| T06 | Conflicting 2/3 cm/s assertions remain unresolved | Partially covered | General assertion-group and conflict-resolution service. |
| T07 | Maximum and mean are not equivalent statistics | Partially represented | General statistic-type compatibility evaluator. |
| T08 | Unit conversion preserves source value and conversion lineage | Not implemented | Typed quantity/conversion service. |
| T09 | Gravity difference requires a validated physical bridge | Not implemented | Independently verifiable bridge record and domain validation. |
| T10 | Source regime interpretation differs from FiF regime assessment | Partially represented | Dedicated regime assessment contract and tests. |
| T11 | Independent raw-video reconstruction and uncertainty agreement | Not implemented | Video pipeline, measurement and uncertainty tests. |
| T12 | Threshold/calibration sensitivity forces abstention when unbounded | Not implemented | Image-measurement sensitivity subsystem. |
| T13 | Non-critical unknown does not block unrelated inference | Partially represented | Gate criticality and profile-specific unknown policy. |
| T14 | Observable/combustion-phase mismatch blocks transfer without mapping | Not implemented | Typed observable/phenomenon ontology and bridge rules. |
| T15 | NASA-reported uncertainty is not labelled FiF-reconstructed | Partially represented | Uncertainty provenance service and tests. |

### 12.2 I-series

| ID | Required invariant | Current status | Required completion |
|---|---|---|---|
| I01 | Unknown remains unknown after normalization | Partially covered | General normalization invariant tests. |
| I02 | Conflicting assertions remain separately addressable | Covered for PMMA fixture | Generalized source conflict tests. |
| I03 | Missing oxygen/pressure/velocity/thickness receives no default | Not implemented generally | Typed condition ingestion and no-default policy. |
| I04 | Every derived value links to parent assertions | Not implemented | Derived-value lineage validation. |
| I05 | Mean/max/median/transient are not silently equated | Partially covered | General statistic semantics. |
| I06 | Unit conversion preserves original value/unit | Not implemented | Conversion records and tests. |
| I07 | Failed critical gate cannot be offset by compatible dimensions | Covered | Preserve regression test. |
| I08 | Every conclusion carries domain and prohibited extrapolations | Partially covered | Enforce profile/domain-specific prohibited-use semantics. |
| I09 | Source interpretation and FiF assessment remain separate | Partially represented | General policy tests. |
| I10 | Same versioned inputs/rules produce deterministic output | Covered | Add graph/source/build hashes to replay metadata. |
| I11 | Every status includes rule IDs, evidence refs and reasons | Partially covered | Enforce metadata for every relevant state. |
| I12 | Source-reported uncertainty is not labelled independently reproduced | Partially represented | General uncertainty provenance tests. |

A fixture that requires a subsystem not yet built remains deferred. It must not be marked passed merely to increase test coverage.

---

## 13. Release gate checklist

A release candidate cannot be accepted unless every in-scope item below is satisfied.

### G1 — Source inventory
- [ ] Full PSI-25 table and count discrepancy reconciled.
- [ ] Selected PSI-25 nested file manifest captured.
- [ ] B3/B6/ground assets verified and hashed.
- [ ] Calibration workbook and external dependency inspected.
- [ ] PSI-62 archive inventoried and coverage established.
- [ ] Required publication/software sources acquired or documented inaccessible.

### G2 — Identity and reconciliation
- [ ] B3/B03 identity and sample linkage supported.
- [ ] B3 2 vs 3 cm/s discrepancy resolved or explicitly bounded.
- [ ] B3 material identity supported by source join.
- [ ] B6 flow and O₂ mappings reconciled.
- [ ] Ground run/sample/video identified.
- [ ] Source overlap and independence assessed.

### G3 — Evidence model
- [ ] Populated acquisition packages schema-valid.
- [ ] Cross-record references and IDs valid.
- [ ] All source assertions have precise locators.
- [ ] Raw source values immutable.
- [ ] Derived quantities have lineage and units.

### G4 — Measurement
- [ ] Original media hashes and stream metadata recorded.
- [ ] Camera/view and timebase mapping established.
- [ ] Spatial calibration and uncertainty established.
- [ ] Segmentation and threshold sensitivity tested.
- [ ] Independent spread-rate reconstruction completed or bounded abstention documented.
- [ ] Published and FiF-derived quantities remain distinct.

### G5/G6 — Science and engine
- [ ] Equations and assumptions reviewed.
- [ ] Combustion regime and domain limits justified.
- [ ] Physical comparability gates are outcome-specific.
- [ ] Transfer rules pass counterexample tests.
- [ ] Evidence references are resolvable.
- [ ] Engine abstains on critical unknowns/conflicts.
- [ ] T01–T15 / I01–I12 in-scope coverage complete.

### G7/G8 — Platform and UX
- [ ] Ingestion-to-query integration passes.
- [ ] Retrieval citations resolve.
- [ ] AI synthesis cannot override deterministic gates.
- [ ] Human-first task workflows pass usability tests.
- [ ] Accessibility and responsive acceptance pass.
- [ ] AI interface uses the same canonical data and gates.

### G9/G10 — Validation and audit
- [ ] All software, data, scientific, UI, security and reproducibility suites pass.
- [ ] Independent Claude and Mistral audits completed on same frozen snapshot.
- [ ] No unresolved critical/high audit finding.
- [ ] Accepted findings fixed and regression-tested.
- [ ] Validation record bound to exact snapshot and scope.

### G11 — Release
- [ ] Clean installation and deployment verified.
- [ ] Licence and third-party notices complete.
- [ ] Documentation and known limitations complete.
- [ ] Demo reproducible from pinned release.
- [ ] Project Owner approves release.

---

## 14. Test reporting template

Every test report must record:
- test ID and category;
- tested commit SHA;
- source/data snapshot IDs and hashes;
- schema/ruleset/software versions;
- environment and dependency versions;
- exact command or procedure;
- expected result;
- actual result;
- pass/fail/blocked status;
- logs and artefacts;
- defect / issue ID if failed;
- reviewer and review date.

Do not record “all tests pass” without the exact commit and scope.

---

**Current decision:** software prototype tests have passed on PR #3 and PR #4. The scientific validation programme remains largely open. The next project gate is G1 source inventory, not another general software architecture review.


## 15. CI trigger coverage gap

The current workflow has push triggers for main and selected historical feature branches, but does not include acquisition/pmma100-bass-b3. Pull requests targeting main do trigger CI.

Before the next code-bearing commit on the acquisition branch:
- either add the active working branch to the push trigger;
- or ensure a PR targeting main is opened and the full CI suite passes before merge.

This is tracked as ISS-017. Until branch coverage is corrected, do not interpret the absence of a workflow run on a branch commit as a passing test. Manual review and Project Owner merge authorization remain required.


## Product-scope test coverage reconciliation — 2026-11-04

The active MVP boundary is **FiF Core + all Extensible modules**, as defined by [FiF Product & Module Traceability Matrix v1.0](FIF_PRODUCT_MODULE_TRACEABILITY_MATRIX_v1.0.md). The test plan must not treat CRAM-1/2/3, probabilistic anomaly detection, uncertainty quantification, advanced experiment transferability or FiF Research & Control as optional post-MVP features. They are in-scope MVP capabilities with progressive implementation and explicit maturity labels.

### Mandatory module-level coverage additions

| MVP module | Minimum verification/validation coverage to add to the detailed test backlog |
|---|---|
| NASA Data Intelligence | Source/version identity, acquisition completeness, immutable raw capture, checksum, provenance and parser fidelity |
| Experiment Comparison | Identity joins, field-level comparability, missing/conflicting values, outcome/statistic semantics and deterministic reproducibility |
| Physics-Based Similarity | Dimensional consistency, physical constraints, domain limits, sensitivity, unknown handling and counterexamples |
| Evidence-Backed Synthesis | Claim-to-evidence links, source-vs-derived distinction, contradiction preservation, unsupported-claim detection and abstention |
| Interactive Dashboard | Core user journeys, data-state rendering, conflicts/uncertainty display, accessibility, responsive and browser compatibility |
| FiF Advanced Analytics | Method-specific reference fixtures, numerical tolerances, reproducibility, data sufficiency and invalid-input behaviour |
| CRAM-1 | Thermodynamic/property/unit tests; analytical transport cases; conservation/physical bounds where applicable; independent benchmark |
| CRAM-2 | Regime definitions and labeled/reference cases; boundary cases; classification uncertainty; out-of-domain abstention |
| CRAM-3 | Synthetic signals with known properties; sampling/stationarity diagnostics; surrogate/null tests; estimator bias and confidence |
| Probabilistic Anomaly Detection | Calibration, discrimination, false-positive/negative rates, class imbalance, drift and threshold sensitivity |
| Uncertainty Quantification | Analytical propagation cases, Monte Carlo convergence, correlated-input handling, interval coverage and sensitivity |
| Advanced Experiment Transferability | Cross-case holdout, known-compatible/incompatible/unknown fixtures, explanation audit and no universal opaque score |
| FiF Research & Control | Workflow state, parameter/configuration provenance, permissions, reproducible runs, review/approval and no unintended operational actuation |

Each method must have a defined reference or synthetic fixture, assumptions, tolerance/acceptance rule, failure modes and maturity label. A passing software test is not scientific validation. Experimental validation must use independent, appropriate evidence and declare its domain.

### Future-research design-review coverage

Future-research items remain outside the committed MVP acceptance boundary unless scope is explicitly changed. They still require documented review criteria: model/theory adequacy, required data, interface compatibility, computational feasibility, verification/validation strategy, operational/safety boundary and unresolved research questions. A documented concept must not be reported as implemented or validated.

### Plan status

This addendum defines required coverage; it does not claim that these test cases have already been authored, executed or passed. The detailed test inventory and gate mapping must be updated as module specifications are decomposed. Existing CI evidence remains limited to the commits and checks previously recorded in this plan.

## Strategic-stage alignment for validation gates — 2026-11-04

The test gates below are engineering acceptance controls, not replacements for the original seven strategic stages. Their mapping is:

| Test/validation gate | Engineering stage | Original strategic stage(s) |
|---|---|---|
| G1 Source inventory | STAGE 2 | 2 — NASA Data Audit |
| G2 Identity and reconciliation | STAGE 3 | 2 — NASA Data Audit; 3 — Physics & Combustion Framework |
| G3 Evidence model | STAGE 4 | 2 — NASA Data Audit; 4 — System Architecture; 5 — MVP Specification |
| G4 Measurement | STAGE 5 | 3 — Physics & Combustion Framework; 6 — Validation & Demonstration |
| G5 Science and domain limits | STAGE 6 | 3 — Physics & Combustion Framework; 4 — System Architecture; 5 — MVP Specification; 6 — Validation & Demonstration |
| G6 Deterministic engine | STAGE 7 | 4 — System Architecture; 5 — MVP Specification |
| G7 Data/retrieval/AI services | STAGE 8 | 2 — NASA Data Audit; 4 — System Architecture; 5 — MVP Specification |
| G8 Product UX and interfaces | STAGE 9 | 4 — System Architecture; 5 — MVP Specification |
| G9 Integrated validation | STAGE 10 | 6 — Validation & Demonstration |
| G10 Independent audit | STAGE 11 | 6 — Validation & Demonstration; 7 — Competition Package |
| G11 Release/demo | STAGE 12 | 7 — Competition Package |
| G12 Post-release expansion | STAGE 13 | Post-competition lifecycle; outside the original seven-stage competition sequence |

The detailed module-level test coverage in this plan must be read together with the Product & Module Traceability Matrix. All 13 MVP capabilities are in scope. Future-research directions receive design/feasibility review criteria, not MVP implementation acceptance tests unless scope is formally changed.

The original strategic Stage 1 deliverable (FiF Concept & Scientific Foundation v1.0) remains distinct from the already-recorded engineering Stage 1 documentary/control milestone.
