# FiF — Master Project Map & Completion Roadmap v1.0

**Document role:** Single authoritative project map, implementation baseline and end-to-end completion plan  
**Baseline date:** 2026-11-04  
**Baseline branch:** acquisition/pmma100-bass-b3  
**Baseline commit before this document:** 71703338d0f53d6a3b306706f4ec5f83d1386046  
**Repository:** https://github.com/Romeo-Decu/FiF  
**Project owner:** Romeo Decu  
**Project Manager / Scientific Lead:** ChatGPT  
**Status:** Stage 1 documentary closure; subsequent delivery gates remain open

---

## 0. How this document must be used

This is the master reference for continuing FiF. It supersedes repeated ad-hoc status summaries in chat, but does not erase earlier scientific records or decision history.

Before starting any new work, the Project Manager must:
1. Read this map and the linked source/register/test documents.
2. Check the current repository branch and commit.
3. Identify the exact work-package ID and its dependencies.
4. Reuse existing source audits and decisions; do not repeat research unless a defined gap requires it.
5. Update the relevant register and artefact as part of the same work package.
6. Record evidence and test results before marking a task complete.

**Completion rule:** an item is complete only when its deliverable exists, its acceptance criteria pass, and the evidence is recorded in GitHub. A proposal, analysis, code draft, successful import, or passing software test is not by itself scientific validation.

### Status vocabulary

- **Implemented and verified:** artefact exists and the stated verification has been performed.
- **Implemented, partially verified:** implementation exists but coverage or acceptance remains incomplete.
- **Documented / designed:** architecture, method or requirements are recorded; no working implementation is implied.
- **Acquired / source-reported:** a source record or value has been obtained/transcribed; it is not an independent FiF measurement.
- **Open / blocked:** work remains, with the missing evidence or dependency stated.
- **Deferred:** intentionally outside the current release scope; it must have a trigger for reconsideration.
- **Not started:** no implementation or verification evidence is present.

Never use “done” without naming exactly what is done.

---

## 1. Project definition and target

### 1.1 Product definition

Flame in Freefall (FiF) is a physics-aware scientific intelligence and evidence-transferability platform for microgravity / reduced-gravity combustion research, initially oriented toward spacecraft fire safety.

FiF must transform heterogeneous experimental research into traceable, comparable and bounded scientific evidence. It must not collapse the following distinct questions:

1. **Retrieval relevance:** does a source address the research question?
2. **Physical comparability:** are the governing conditions sufficiently characterized for the selected phenomenon and outcome?
3. **Evidence transferability:** can a finding inform another context, and within what declared limits?

Core rules:
- Physics before semantic similarity.
- Evidence before inference.
- Unknown is not compatible.
- Source conflict is not automatically physical incompatibility.
- Source-reported values are not FiF measurements.
- A software result does not validate combustion physics.
- No opaque universal weighted similarity score.
- A valid abstention (“insufficient evidence”) is a correct system outcome.
- No capability claim without an implementation path, evidence and validation criterion.

### 1.2 Initial scientific demonstration

The first scientific case remains **opposed-flow flame spread over nominal 100-µm PMMA**, using the BASS/BASS-II microgravity evidence and a normal-gravity downward-spread comparison.

There are two distinct BASS-II data roles. Do not merge them:

**Primary transferability case — B3 / B03**
- Original case selection: BASS-II B3, sample 148, nominal 100-µm film, 20-mm width.
- Intended comparison: NASA Section 2.3 microgravity 100-µm result versus the 100-µm normal-gravity downward result.
- The B3-to-Section 2.3 result linkage remains unresolved.
- B3 Appendix A.1 Air display = 2 cm/s; Section 2.3 reports 3 cm/s; Carmignani Appendix A.2 lists B3 flow as initial/final 2→0 cm/s.
- The approximately 2.2 mm/s microgravity maximum must not be attributed to B3 without an explicit run/result join.
- The approximately 2.0 mm/s ground average is a section-level statistic; its exact run/sample/video linkage remains unresolved.

**Detailed reconstruction / method-validation case — B6**
- BASS-II B6, GMT188, sample153m, 0.1-mm PMMA film, 20-mm width.
- NASA Table A.1 provides detailed test-level metadata and separate calibrated / uncalibrated gas readings.
- Carmignani (2019) provides B6-related image-derived analysis and Figure 5.8 with radiometer, anemometer and FIAT flame-area information.
- This is a strong candidate for testing FiF's source-reconciliation and video-analysis pipeline.
- It does **not** replace B3 as the originally selected transferability case unless a recorded project decision explicitly changes the scope.
- The dissertation uses “BASS” terminology and does not expose NASA GMT188/sample153m in its B6 table; the join to BASS-II B6 is strongly supported but still requires direct media/metadata verification.

B1 is a separate candidate within-session comparator, not a validated control. Do not silently combine B1, B3 and B6.

### 1.3 Release levels

**Release A — NASA Space Apps / demonstrable MVP**
- A bounded, working evidence-intelligence vertical slice.
- One well-documented experiment family and a clearly scoped scientific question.
- Source-linked discovery, structured evidence, physical-comparability assessment, bounded transferability conclusion, uncertainty/conflict display and an interactive human-readable result.
- No autonomous fire prediction, suppression, spacecraft actuation, certification or operational control claims.

**Release B — complete FiF platform v1**
- Reusable ingestion and source registry.
- General experiment/evidence model, not only PMMA-100.
- Deterministic evidence and transfer engine with typed quantities, provenance, conflicts and uncertainty.
- Human-first application and machine-readable AI interface over the same scientific core.
- Reproducible end-to-end operation, validation and release controls.

**Research extensions — outside v1 unless separately approved**
- CRAM / nonlinear dynamics / Transfer Entropy.
- Predictive combustion models and multiphysics simulation.
- Operational fire-risk forecasting or spacecraft system integration.
- Broader family coverage beyond the prioritized NASA evidence families.

---

## 2. Repository and implementation baseline

### 2.1 Repository state at Stage 1

- Private repository: Romeo-Decu/FiF.
- Default branch: main.
- Working branch: acquisition/pmma100-bass-b3.
- Main baseline SHA: 96a739d92c50b195a00fbeca93439922657930e5.
- Working branch SHA before this roadmap: 71703338d0f53d6a3b306706f4ec5f83d1386046.
- Working branch was 33 commits ahead of main and 0 behind at baseline.
- Main is unchanged by this Stage 1 work.
- No merge or pull request is implied by this document.
- Keep the repository private. Do not commit raw source media, credentials, tokens or private keys.
- Work on a named branch; review changes before any merge. Repository owner retains final merge authority.

The working branch contains the additional B6 source-extraction and PSI-25 audit documents. The code, canonical graph, ruleset, schemas, tests and visualization prototype were already merged into main through PRs #2, #3 and #4.

### 2.2 What is actually implemented

| Component | Repository artefact | Current state | What this means |
|---|---|---|---|
| Python package | pyproject.toml; src/fif_transfer/ | Implemented | Small Python package, version 0.1.3, standard-library runtime dependencies. |
| Deterministic assessment kernel | src/fif_transfer/engine.py | Implemented, partially verified | Evaluates caller-supplied gate states, conflicts and incompatibilities. It is not yet a physical-comparability or evidence-validation engine. |
| CLI | src/fif_transfer/cli.py; src/fif_transfer/__main__.py | Implemented | Reads ruleset and request JSON and returns deterministic assessment JSON. |
| PMMA-100 ruleset | configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json | Implemented as configuration | Versioned gates and inference profiles exist; ruleset validity and scientific content are not fully independently validated. |
| Request schema | schemas/TRANSFER_ASSESSMENT_REQUEST_v0.1.schema.json | Implemented as contract | Static contract exists; CLI does not yet execute full JSON Schema validation. |
| Canonical evidence graph schema | schemas/EVIDENCE_GRAPH_v0.1.schema.json | Implemented as contract | Defines node/edge/evidence semantics; not a production database or full scientific ontology. |
| Controlled vocabulary | schemas/CONTROLLED_VOCABULARY_v0.1.json | Implemented | Evidence states and controlled labels exist. |
| PMMA-100 graph fixture | research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json | Implemented documentary fixture | Preserves B3/Section 2.3 as separate records, 2 vs 3 cm/s, unknown B3 rate, separate mean/maximum and unresolved joins. |
| Acquisition package schema | schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json | Implemented as contract | Defines a staging package for sources, assets, extractions, linkage candidates and open questions. |
| Acquisition package template | research/acquisition/PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json | Empty template | No populated, accepted B3 acquisition package yet. |
| Evidence acquisition protocol | docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md | Implemented / reviewed | Defines source capture, integrity, provenance and separation of acquisition, verification and validation. |
| Visualization architecture | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md | Accepted for prototype | ELK for layout, Cytoscape.js for graph interaction, Plotly for scientific charts; browser-first. |
| Browser visualization | visualization/ | Read-only prototype implemented | Loads canonical PMMA graph, displays provenance graph and documentary flow discrepancy, exposes node/edge details and exports canonical JSON. |
| Automated software tests | tests/ and visualization/tests/ | Implemented | Current suite contains 67 Python test methods and 5 Node graph-adapter tests, plus a browser smoke suite. |
| CI workflow | .github/workflows/tests.yml | Implemented | Python 3.10–3.13 matrix, Node tests, syntax checks and Chromium/Firefox browser smoke tests on configured push/PR events. |
| Research documentation | research/ and docs/ | Substantial, fragmented but now mapped | Scientific framework, source audits, comparability matrix, video protocol, data-access and issue registers exist. |

### 2.3 What has been verified by CI

Two relevant GitHub Actions runs are recorded:

- PR #3, run 41769248025: Python 3.10, 3.11, 3.12 and 3.13 all passed; graph-adapter tests, JavaScript syntax checks, Playwright installation, Chromium and Firefox smoke tests all passed.
- PR #4, run 41770394680: the same Python matrix and visualization/browser jobs passed.

These are software checks on the respective PR commits. They do **not** establish scientific validity, data correctness, or a successful test of the current B6/B3 scientific case.

The latest working-branch documentation commits were not themselves the subject of a new CI run. No local test execution is claimed in this Stage 1 audit.

### 2.4 What is not implemented

The following must not be described as existing capabilities:

- No complete NASA PSI ingestion pipeline.
- No complete current PSI-25 nested file manifest.
- No complete 130-record experimental table; supplied CSV has 129 data records.
- No raw source archive repository or automated asset hashing workflow executed end-to-end.
- No populated and independently reviewed B3 acquisition package.
- No general source registry or source-reference resolver.
- No production experiment database or persistent evidence store.
- No general-purpose PDF/XLSX/CSV/video ingestion pipeline.
- No general typed-quantity, unit conversion and transformation-lineage service.
- No complete experiment/run/sample/result identity-join validator.
- No general statistic-equivalence engine (mean, maximum, transient, median, etc.).
- No complete physical-comparability engine.
- No independently verified physical bridge/model subsystem.
- No video reconstruction or FiF spread-rate measurement for B3 or B6.
- No validated uncertainty propagation or image-threshold sensitivity engine.
- No general retrieval / RAG / AI synthesis service connected to the canonical graph.
- No backend API or production persistence layer.
- No complete human-first product UX specification or production UI.
- No production deployment, packaging, monitoring or user-management system.
- No formal hash-bound independent validation-attestation service.
- No complete security, privacy, licensing and performance release audit.

---

## 3. Current scientific evidence position

### 3.1 BASS-II PSI-25 collection

The PSI-25 BASS-II Version 4 record is identified by DOI 10.60555/4qc4-de67 and is licensed CC0-1.0 according to the recorded collection metadata.

The PSI page exposes 130 Experimental Table records and 9 root folder names. The supplied CSV has:
- 16,590 bytes in the audited copy;
- SHA-256 71e792bf6b5fb5ea620c5dd70fbbac05515992e12aefcf5dff47312caa48c042;
- 17 source columns;
- 129 data rows (130 physical lines including the header);
- all 22 Bhattacharjee test IDs B1–B22 present in that CSV.

The 130 page count versus 129 CSV data rows remains unresolved (ISS-009). The 694 files added and 131 removed are version-history counts, not a verified current file count. The nested current folder/file manifest remains incomplete (ISS-008).

The source CSV must be retained unchanged. Blank cells, literal “none”, numeric-looking strings, sample suffixes and multi-value Fan/Air display text must not be silently normalized.

### 3.2 B3 / B03 evidence

Known source assertions:
- B3 / sample 148 / GMT50 / 19 February 2014.
- PSI table material wording: “100 micron film 2 cm wide”; PMMA is not explicit in that cell.
- B3 Air display 2; Fan display 47; flow restrictor 2; 253 frames; calibrated O₂ 22.2 → 21.8%.
- Carmignani Table A.2 corroborates nominal 0.1-mm PMMA, 20-mm width, B3 and flow 2→0 cm/s.
- NASA Figure 2.20 labels B03 as a 100-µm PMMA image.
- NASA Section 2.3 reports 3 cm/s for its microgravity comparison and approximately 2.2 mm/s as a maximum; no proven join to B3.
- NASA Section 2.3 reports approximately 2.0 mm/s average for the normal-gravity downward case; exact ground run/sample/video join is not established.
- B3 proof-sheet was reviewed in earlier work; its image/time identifiers and clock offset are recorded in the project history, but the original video bytes have not been independently processed by FiF.
- Candidate B3 media names remain user-reported until exact current PSI paths and bytes are checked.

### 3.3 B6 evidence

The following records are on the working branch:
- research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md
- research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md
- research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md
- data/derived/BASSII_B6_SOURCE_VALUES_v0.1.csv

NASA Table A.1 B6 values include:
- 7 July 2014, GMT188, test B6, sample153m;
- 2-cm, 0.1-mm PMMA film;
- opposed flow, integral igniter, two restrictors;
- Fan display sequence 0.9, 1.3, 2.75;
- Air display sequence 3, 5, approaching 10 cm/s;
- 80 frames;
- calibrated O₂ 21.0 → 20.9%;
- uncalibrated O₂ 20.1 → 20.0%;
- CO₂ 0.33 → 0.41%;
- CO 0 → 0.3 ppm;
- crew observation: steady burning at 3 and 5 cm/s; did not reach 10 cm/s before end of sample; complete burnout; HCl notation as transcribed in the source.

A secondary MicroFire Atlas transcription loses the calibrated/uncalibrated distinction for B6. NASA's calibrated values remain authoritative. Audit the other Bhattacharjee rows before generalizing this issue.

Carmignani (2019) provides:
- B6 conditions in Appendix A, Table A.2;
- B6/B1 imagery and comparisons in Figures 5.4 and 5.6;
- Figure 5.8 with FIAT flame area, 2D area estimate, radiometer and anemometer-related data;
- approximate discussion values around 34 mV, 400–600 mm² FIAT area and ~120 mm² increase in 2D area;
- approximately 2 mm/s spread-rate discussion in the relevant B6/B1 analysis;
- FIAT method and image-measurement error discussion.

These are source-reported / approximate thesis outputs, not FiF-reconstructed time series. The thesis flow entry 1→7 cm/s is explicitly an initial-to-final pair, not a min–max range. The mapping to NASA Fan/Air display sequences and Figure 5.8 anemometer trace remains unresolved. The dissertation uses “BASS” terminology and the BASS-II B6 cross-source join remains a candidate pending media/metadata verification.

### 3.4 Existing scientific framework

Already documented:
- research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md
- research/PHYSICAL_COMPARABILITY_AND_TRANSFERABILITY_MATRIX_PMMA100_v0.1.md
- research/FIRST_PHYSICS_CASE_SELECTION_v0.1.md
- research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md
- research/DETERMINISTIC_TRANSFER_RULES_AND_TEST_CASES_v0.1.md
- research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md

These are design/scientific frameworks and behavioural specifications. They are not a validated combustion model, a completed video analysis, or proof of transferability.

---

## 4. Master architecture map

The intended end-state architecture has one canonical scientific core and two user-facing interaction surfaces.

### 4.1 Data and evidence path

1. Source registry and investigation catalogue.
2. Source acquisition and immutable raw asset inventory.
3. Format-specific extraction (PDF, CSV, XLSX, image, video, publication).
4. Source assertions and exact locators.
5. Experiment/sample/configuration/measurement identity resolution.
6. Typed quantities, original units, normalized values and transformation lineage.
7. Canonical evidence graph / evidence store.
8. Provenance and integrity validation.
9. Physics-aware, outcome-specific comparability assessment.
10. Evidence-transfer assessment with uncertainty and explicit limits.
11. Machine-readable audit result and human-readable explanation.

### 4.2 Scientific engine

- Phenomenon and observable definitions.
- Combustion mode / regime classification with evidence and domain limits.
- Physical-condition profiles and question-specific critical gates.
- Typed quantities, units, statistics and conversions.
- Physical incompatibility and validated bridge records.
- Measurement reconstruction and uncertainty propagation.
- Deterministic transfer decision kernel.
- Reproducible calculation records and versioned rulesets.

LLMs may assist discovery, extraction, classification and synthesis. They must not be the authority for unit conversion, deterministic calculations, threshold logic, or source-of-truth updates.

### 4.3 Application surfaces

**Human-first interface**
- task-oriented navigation and guided workflows;
- experiment and source discovery;
- source detail and asset lineage;
- evidence/conflict workbench;
- comparison workspace;
- explanation of unknown, incompatible and non-transferable dimensions;
- accessible charts and export;
- progressive disclosure so researchers do not need to understand the internal graph model.

**AI / agent interface**
- canonical graph and schemas;
- stable IDs and source locators;
- structured query / retrieval APIs;
- machine-readable assessments and audit trails;
- same scientific gates as the human UI; no bypass.

Both surfaces must use the same canonical data and validation controls.

### 4.4 Visualization decisions already accepted

Do not reopen these without new evidence:
- browser-first, responsive application shell;
- ELK/elkjs for graph layout;
- Cytoscape.js for graph interaction;
- Plotly for scientific charts;
- canonical data remains renderer-independent;
- visualization must not mutate scientific records;
- desktop packaging deferred until justified;
- GLSP not required for the initial read/explore experience.

Open UI issues ISS-001 to ISS-006 remain tracked in the register.

---

## 5. End-to-end work breakdown and completion sequence

The sequence below is the required project path. Tasks may run in parallel only when their dependencies are satisfied. No stage may silently skip an exit gate.

### STAGE 1 — Project baseline and roadmap
**Status: CLOSED — documentary/control baseline only.**

Deliverables:
- authoritative implementation inventory;
- scientific scope and case roles (B3 primary; B6 reconstruction support);
- architecture map;
- source acquisition register;
- full work breakdown and acceptance gates;
- master testing and validation plan;
- repository links and open-issue mapping.

Exit:
- all existing artefacts classified as implemented, designed, source-reported, open or deferred;
- no capability claim is confused with implementation;
- every remaining work package has a deliverable and acceptance criterion;
- source gaps are registered;
- roadmap committed to the working branch.

This stage does not close PSI-25 inventory, scientific reconciliation, transferability or release validation.

### STAGE 2 — Source acquisition and inventory closure
**Gate: G1 — Source and asset inventory complete for the selected case.**

Tasks:
1. Retrieve and preserve the complete PSI-25 Experimental Table export.
2. Reconcile 130 page records versus 129 CSV records; identify the exact missing/extra/different record or establish the page-count semantics.
3. Enumerate all current PSI-25 root and nested folders with exact path, filename, file type, size and version metadata.
4. Verify B3/B1/B6 candidate files against exact PSI paths; record actual bytes and archive membership.
5. Retrieve the B6 original video archive and Fan calibration workbook from the owner-held files when available to the analysis workspace; hash each file and each archive member.
6. Inspect the workbook formulas, named ranges, cached values and external link. Locate the referenced workbook; do not substitute guessed calibration data.
7. Retrieve and inventory the PSI-62 archive. Establish which BASS/BASS-II experiments it actually contains before treating it as evidence for B6.
8. Reattempt the SDSU Flame Research Archive using documented institutional/archive routes; record access result, not just URL existence.
9. Retrieve relevant thesis/software sources for FIAT / Flame Analyzer and distinguish the implementations.
10. Identify the exact normal-gravity 100-µm dataset, run/sample IDs and media/reduced-data path.
11. Record all source versions, licences, retrieval times, SHA-256 checksums and inaccessible items.

Required source register: research/SOURCE_ACQUISITION_AND_EVIDENCE_GAP_REGISTER_v1.0.md.

Exit criteria:
- complete table with all rows and exact raw CSV hash;
- 130-vs-129 discrepancy resolved or formally blocked by NASA response/source limitation;
- current PSI nested manifest recorded for the selected folders and relevant experiments;
- selected media/archive member inventory exact and checksummed;
- calibration workbook dependency identified;
- PSI-62 contents and run coverage known;
- all still-missing items have a named source, retrieval path and impact statement.

### STAGE 3 — Experiment identity and within-experiment reconciliation
**Gate: G2 — Source-to-experiment-to-asset chain reviewed.**

Tasks:
1. Build separate dossiers for B3, B1, B6 and the ground counterpart.
2. Preserve B3/B03 as separate labels until the source-level alias is justified.
3. Verify sample IDs, dates, GMT identifiers, materials, dimensions, ignition, holder, flow configuration and atmosphere.
4. Reconcile B3 PMMA wording using exact source joins; do not edit the raw PSI cell.
5. Reconcile B3 2 cm/s, Carmignani 2→0 cm/s and Section 2.3 3 cm/s as separate assertions.
6. Reconcile calibrated and uncalibrated O₂ columns across all 22 Bhattacharjee rows; investigate the MicroFire Atlas mapping error.
7. Reconcile B6 NASA Fan/Air displays, Carmignani initial/final flow values, anemometer trace, calibration and voice confirmations.
8. Establish the source terminology and identity join between Carmignani B6 and NASA BASS-II B6.
9. Identify exact ground run/sample/video underlying the normal-gravity downward 2.0 mm/s average.
10. Identify whether NASA report and Carmignani thesis use overlapping original datasets; do not treat documentary cross-references as independent experimental replications.

Exit:
- each identity join is classified established / candidate / unresolved / rejected with evidence;
- no filename-only or figure-proximity join;
- all conflicts and unknowns retained;
- B3 2.2 mm/s attribution remains prohibited unless explicit source linkage is obtained;
- B6 remains a separate reconstruction case.

### STAGE 4 — Canonical evidence model and data pipeline
**Gate: G3 — Source-faithful, schema-validated evidence package.**

Tasks:
1. Finalize versioned source, dataset, asset, experiment, configuration, sample, measurement, assertion, claim, comparison and assessment contracts.
2. Define typed physical quantities: value, unit, quantity kind, basis, uncertainty, statistic type, temporal/spatial scope and source locator.
3. Define immutable raw source storage and separate normalized/derived layers.
4. Implement source registry and stable IDs.
5. Implement file acquisition, checksum and archive-member manifest.
6. Implement extraction adapters for CSV and XLSX first, then PDF and image/video metadata.
7. Preserve empty string, literal “none”, zero, negative, missing and unknown as distinct source states.
8. Implement conversion records that preserve source value/unit, conversion formula, constants, software version and uncertainty.
9. Implement cross-record ID uniqueness and reference-integrity validation; JSON Schema shape validation alone is insufficient.
10. Implement a controlled adapter from reviewed acquisition packages to the canonical evidence graph.
11. Add source assertion groups for contradictory values without overwriting individual source assertions.
12. Bind every derived value to its parent assertions and calculation record.

Exit:
- populated B3/B6/ground acquisition packages pass Draft 2020-12 schema validation;
- cross-record uniqueness/reference checks pass;
- all source assertions have precise locators;
- raw source layer remains immutable;
- normalized and derived values have transformation lineage;
- no unverified assertion enters the canonical graph as an established fact.

### STAGE 5 — Scientific case reconstruction and measurement
**Gate: G4 — Reproducible measurement evidence for the selected case.**

Tasks:
1. Probe original B3 and B6 media: container, codec, streams, frame rate/timebase, dimensions, bit depth, timestamps, metadata and checksums.
2. Determine camera/view roles; preserve top-view still sequence and side-view sensor/overlay video as separate streams.
3. Map clock offsets and discontinuities using proof sheets, BASS video clock, stream timestamps and voice confirmations.
4. Establish spatial calibration independently for each camera/view; never reuse a scale without evidence.
5. Retrieve and document original NASA Flame Analyzer and FIAT methods/settings; do not conflate tools.
6. Digitize Carmignani Figure 5.8 series separately (radiometer, anemometer, FIAT area, 2D area) with axis calibration, point-level digitization uncertainty and source image locator.
7. Implement FiF image processing using the documented FIAT/NASA method only after defining a reproducible protocol and sensitivity analysis.
8. Define leading-edge and trailing-edge segmentation; test threshold sensitivity and segmentation repeatability.
9. Extract flame-front position versus time and calculate spread rate using a justified fitting window.
10. Quantify uncertainty from spatial scale, frame interval, timestamp uncertainty, segmentation, fit window and physical variability.
11. Reconstruct the B6 published result independently first, then B3 if its media and joins permit.
12. Reconstruct the ground downward result only after exact run/sample/video identity is established.
13. Compare FiF reconstruction with source-reported values using compatible statistics and uncertainty intervals.

Exit:
- raw media hashes and metadata recorded;
- frame/time and spatial calibration documented;
- algorithm, parameters and software revision pinned;
- reproducible measurement outputs and uncertainty decomposition available;
- thesis figure digitization is clearly distinguished from original measurements;
- any disagreement is documented, not tuned away;
- if source media are insufficient, record a bounded non-result rather than fabricate a rate.

### STAGE 6 — Physics and transferability model
**Gate: G5 — Scientific rules and domain limits independently reviewed.**

Tasks:
1. Freeze the target observable and inference question (initially leading-edge flame-spread rate).
2. Define the physical mechanism and combustion-regime hypotheses for thin PMMA opposed-flow spread.
3. Separate solid-phase heating/conduction/degradation/pyrolysis from gas-phase transport, mixing, reaction and flame feedback.
4. Establish governing equations and assumptions; check dimensions and limiting cases.
5. Define thermal-thin/thick assumptions and the relevant solid thermal-diffusion timescale.
6. Define only the dimensionless groups relevant to available data (e.g. Reynolds, thermal/mass Péclet, Schmidt, Lewis, Damköhler, Rayleigh / residual acceleration, radiation and pyrolysis descriptors where defensible).
7. Verify material properties, oxygen basis, pressure, local flow and apparatus boundary conditions.
8. Classify each dimension as compatible, different, unknown or not applicable for the chosen outcome.
9. Define question-specific critical gates and the evidence required to pass them.
10. Define validated physical bridge records; a caller-supplied “validated” flag is not sufficient.
11. Define uncertainty components: measurement, source/reporting, processing, model/assumption, between-run variability and extrapolation.
12. Make transferability outcome-specific; do not produce an opaque universal score.
13. Create scientifically reviewed B3/B6/ground assessment examples and counterexamples.

Exit:
- every equation, parameter and assumption has a source/rationale and validity domain;
- independent scientific review has no unresolved critical defect;
- no unsupported local-flow, oxygen, material or run identity is silently assumed;
- all transfer conclusions include evidence, limits, uncertainty and prohibited extrapolations;
- engine abstains on unresolved critical evidence.

### STAGE 7 — Deterministic engine v0.2
**Gate: G6 — End-to-end evidence assessment kernel.**

Tasks:
1. Enforce request/ruleset JSON Schemas at the CLI/API boundary.
2. Resolve evidence references against the source registry and canonical graph.
3. Validate evidence state, provenance, source locator and assertion lineage.
4. Implement typed quantities, unit conversions and conversion lineage.
5. Implement run/sample/result identity and alias/linkage validation.
6. Implement statistic type and observable equivalence checks.
7. Implement criticality and profile-specific treatment of unknowns.
8. Implement physical incompatibility and independently evidenced bridge validation.
9. Implement measurement and uncertainty provenance.
10. Implement outcome-specific comparability and transfer logic using the reviewed scientific rules.
11. Add deterministic replay metadata: request/ruleset/graph/source hashes, software version and commit identifier.
12. Add structured machine-readable explanations and human-readable reason codes.
13. Make malformed input fail closed with controlled errors.
14. Implement every in-scope T01–T15 / I01–I12 fixture as an executable test; explicitly defer only those whose scientific subsystem is genuinely out of scope, with trigger and rationale.
15. Keep deterministic numerical operations in code; use LLMs only as non-authoritative assistants.

Exit:
- all in-scope fixture cases pass;
- every deferred case has a documented reason and future trigger;
- no positive gate can be accepted without resolvable provenance;
- same versioned inputs produce identical outputs;
- all decisions are explainable and auditable.

### STAGE 8 — Ingestion, retrieval and AI service layer
**Gate: G7 — Data-to-answer services work on the canonical core.**

Tasks:
1. Implement source and investigation catalogue.
2. Implement controlled ingestion jobs and job status/error records.
3. Implement metadata and structured-data extraction services.
4. Implement full-text/document retrieval with source locators.
5. Implement semantic retrieval only as candidate discovery, not physical equivalence.
6. Implement query parsing into phenomenon, material, atmosphere, gravity, flow and target outcome.
7. Implement retrieval ranking with visible reasons and source coverage.
8. Implement AI synthesis constrained to retrieved, source-addressable evidence.
9. Require citations for factual statements and show missing evidence.
10. Add refusal/abstention behavior when evidence is inadequate or contradictory.
11. Add prompt-injection and untrusted-source handling; source content cannot alter system rules.
12. Implement API contracts and versioning for human UI and AI agents.
13. Add audit logging without exposing credentials or sensitive operational data.

Exit:
- an end-to-end query retrieves the correct evidence and locators;
- AI synthesis cannot silently turn unknown into known or source-reported into measured;
- unsupported claims are caught by deterministic validation;
- retrieval relevance is visibly distinct from physical comparability and transferability.

### STAGE 9 — Human-first application and AI interface
**Gate: G8 — Researchers can complete core tasks without knowing the internal graph model.**

Tasks:
1. Write the missing user interaction specification (ISS-001): roles, user journeys, navigation, screen states and acceptance criteria.
2. Define primary researcher tasks and information architecture.
3. Build experiment/source discovery and filters.
4. Build experiment and asset detail with provenance timeline.
5. Build a discrepancy/conflict workbench (IDEA-002).
6. Build a comparison workspace with dimension-by-dimension explanations.
7. Build assessment explanation and source-to-claim navigation.
8. Build accessible scientific charts with statistic type, units, source and uncertainty.
9. Keep expert graph view as an advanced mode, not the only interface.
10. Build AI/agent API over the same graph and gates.
11. Implement deterministic export of evidence, assessment and report packages.
12. Complete responsive layouts, keyboard navigation, screen-reader semantics, contrast and non-colour evidence states.
13. Resolve ELK edge-routing fidelity (ISS-002), accessibility (ISS-003), graph performance (ISS-004), licensing/notices (ISS-005) and chart semantics (ISS-006).

Exit:
- a researcher can complete the principal workflow unaided;
- the UI and AI interface return the same underlying scientific outcome;
- conflicts and unknowns cannot be hidden by filters or visual styling;
- accessibility and responsive acceptance tests pass;
- visual rendering never mutates canonical evidence.

### STAGE 10 — Integrated validation and benchmark programme
**Gate: G9 — Software, data, scientific and user validation complete.**

Execute the test plan in docs/TEST_AND_VALIDATION_MASTER_PLAN_v1.0.md. Required test families:
- unit and property tests;
- JSON Schema and contract tests;
- source/asset integrity tests;
- cross-record and provenance tests;
- numerical and dimensional regression tests;
- video measurement and uncertainty tests;
- physical-comparability and transferability scenario tests;
- end-to-end ingestion-to-answer tests;
- AI retrieval/citation/abstention/adversarial tests;
- browser, accessibility, responsive and usability tests;
- security, dependency, licensing and privacy checks;
- reproducibility, performance and deployment tests.

Exit:
- all release-blocking tests pass;
- all scientific benchmark results are reproducible from a pinned snapshot;
- no unresolved critical issue is hidden;
- independent review findings are dispositioned;
- all remaining limitations are stated in the release documentation.

### STAGE 11 — Independent audit and remediation
**Gate: G10 — Independent audit accepted.**

Tasks:
1. Freeze a release-candidate commit and immutable audit bundle.
2. Give Claude read-only access or a frozen source bundle.
3. Give Mistral the same snapshot and independent adversarial questions.
4. Do not let either auditor see the other's report before submission.
5. Audit scientific correctness, provenance, data, model assumptions, software, security, reproducibility and user claims.
6. Record every finding as confirmed defect / plausible concern / missing evidence / optional improvement.
7. Accept, reject or defer each finding with rationale.
8. Implement accepted fixes and add regression tests.
9. Repeat affected validation suites.
10. Bind any future validation attestation to the exact content hash, versions, scope, independent verifier, results and tamper-evident audit reference.

Exit:
- no open critical/high audit finding;
- all accepted fixes verified;
- audit report and disposition register committed;
- no self-declared “validated” status.

### STAGE 12 — Release, demonstration and handover
**Gate: G11 — Release candidate / public demonstration ready.**

Tasks:
1. Finalize product name, scope, user guide and scientific limitations.
2. Complete technical documentation, architecture, data dictionary and API documentation.
3. Complete third-party dependency notices and licence review.
4. Build reproducible release artifacts.
5. Prepare deployment instructions, environment variables and secure secret handling.
6. Define cost, quota, backup, recovery and shutdown procedures for any cloud deployment.
7. Run clean-install and clean-environment tests.
8. Prepare a demonstration scenario from a frozen dataset and fixed query.
9. Prepare final report, screenshots/video and NASA Space Apps submission materials if applicable.
10. Ensure every displayed result links to the correct evidence and version.
11. Tag the release and publish changelog and known limitations.

Exit:
- clean installation and deployment verified;
- demo reproducible from a pinned release;
- all claims match actual implementation and validation;
- owner approves release.

### STAGE 13 — Post-release expansion and maintenance
**Gate: G12 — Sustainable platform operation.**

Tasks:
1. Add new NASA evidence families in a controlled sequence.
2. Start with SoFIE / SAFFIRE / ACME-BRE / FLEX / SAME only after source inventories and domain-specific schemas exist.
3. Do not pool unlike combustion modes or observables into one undifferentiated dataset.
4. Version source snapshots, re-ingestion and schema migrations.
5. Monitor data freshness, extraction failures, retrieval quality and user feedback.
6. Add performance and cost monitoring.
7. Maintain dependency and security updates.
8. Re-run the benchmark suite on every scientific ruleset or ingestion change.
9. Reopen earlier gates if new evidence changes an accepted conclusion.

---

## 6. Critical path and dependency order

The critical path for the first validated PMMA-100 demonstration is:

**G1 source inventory → G2 identity reconciliation → G3 canonical evidence data → G4 measurement reconstruction → G5 scientific model/review → G6 deterministic engine → G7 retrieval/AI service → G8 human UI → G9 integrated validation → G10 independent audit → G11 release.**

Parallel work is permitted only where it does not assume unresolved evidence:
- UI interaction specification may be drafted while G1/G2 continue, but production comparison screens depend on stable data contracts.
- Schema and data-pipeline design may proceed while sources are acquired, but no source assertion may be promoted before review.
- B6 figure digitization and PSI-62 acquisition can proceed in parallel.
- B3 and ground-run acquisition can proceed in parallel with B6, but no matched-pair transfer claim can be made until identity joins are established.
- Advanced CRAM / Transfer Entropy research is deferred until time-series data and a defined scientific question justify it.

**Do not start a downstream stage merely because its predecessor has a document. Start it when the predecessor's exit evidence exists.**

---

## 7. Current open issues and register linkage

The following register entries remain active or deferred:

| ID | Topic | Status / trigger |
|---|---|---|
| ISS-001 | Human-first UI interaction specification | Open; required at Stage 9 entry. |
| ISS-002 | ELK edge routing fidelity | Open; Stage 9 visualization validation. |
| ISS-003 | Accessibility | Open; Stage 9 / G9. |
| ISS-004 | Large-graph performance | Open; Stage 9 / G9. |
| ISS-005 | ELK and third-party licensing/notices | Open; before external distribution. |
| ISS-006 | Scientific chart statistic/uncertainty semantics | Active requirement; every chart and G9. |
| ISS-007 | Evidence lineage and source-to-asset/run/sample joins | Active throughout Stages 2–5. |
| ISS-008 | Complete PSI-25 nested file manifest | Open; blocks G1 closure. |
| ISS-009 | PSI page count 130 vs CSV 129 | Open; blocks full table inventory closure. |
| ISS-010 | Duplicate manifest issue | Closed administratively as duplicate of ISS-008; no evidence task was closed by this action. |
| ISS-011 | B3 material identity wording | Open; Stage 3. |
| ISS-012 | B6 calibrated / uncalibrated O₂ secondary transcription error | B6 correction recorded; audit all 22 Bhattacharjee rows. |
| ISS-013 | B6 flow representation reconciliation | Open; calibration, anemometer and timeline. |
| ISS-014 | Carmignani Figure 5.8 digitization | Open; Stage 5. |
| ISS-015 | PSI-62 archive contents and B6 coverage | Open; Stage 2. |
| ISS-016 | Carmignani BASS vs NASA BASS-II B6 identity join | Open candidate join; Stage 3. |
| IDEA-001 | Human-first and expert graph views share one scientific core | Proposed; Stage 9. |
| IDEA-002 | Evidence discrepancy/conflict workbench | Proposed; Stage 9. |
| IDEA-003 | Asset provenance timeline | Proposed; Stage 4/9. |

The register remains the authoritative location for status changes and decision history. This map summarizes, but does not silently close, those entries.

---

## 8. Stage 1 closure record

**Stage 1 is closed as a project-control and documentary baseline.**

Completed in this closure:
- current repository tree and working branch reviewed;
- existing code, schemas, ruleset, fixtures, tests and visualization classified;
- CI evidence from PR #3 and PR #4 checked;
- scientific scope clarified into B3 primary transfer case and B6 reconstruction-support case;
- current source/data position summarized;
- source acquisition register created;
- complete staged roadmap and gate sequence created;
- test and validation master plan created;
- links to existing decisions and issue register preserved.

Not closed by Stage 1:
- PSI-25 Gate 1 inventory;
- complete B3/B6/ground acquisition;
- source identity and data reconciliation;
- video measurement;
- scientific model validation;
- transferability;
- production application;
- release or certification.

**Stage 1 acceptance condition:** the Project Owner can use these documents to see, without returning to previous chats, what exists, what is missing, which sources are needed, what happens next and what evidence is required to call each stage complete.

---

## 9. Mandatory operating protocol from this point

1. One bounded work package at a time.
2. Every work package has an ID, objective, input sources, dependencies, output artefacts and acceptance criteria.
3. The Project Manager checks the repository before creating new documents or repeating a search.
4. New source discoveries update the source register and affected dossier in the same work package.
5. New decisions/issues receive stable IDs; existing IDs are never recycled.
6. Source values are immutable; corrections are additional records with provenance.
7. No raw source video or large archive is committed to GitHub unless licence, size and storage policy explicitly allow it. Store hashes and retrieval locators instead.
8. Do not modify main directly. Use branches and review.
9. No PR merge without Project Manager review and Project Owner authorization.
10. Do not report a test as passed unless the exact run/commit and test scope are known.
11. A passing software test never closes a scientific validation gate.
12. No new architecture debate unless new evidence invalidates an accepted decision.
13. At every stage exit, update this roadmap, the issue register and the relevant artefacts.
14. At project completion, archive the exact release snapshot, data hashes, ruleset, software version, tests, audit reports and release limitations.

---

## 10. Authoritative linked documents

### Project control
- docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md
- docs/PROJECT_CONTROL_BASELINE_AND_EVIDENCE_RECONCILIATION_PLAN_v0.1.md
- docs/EXTERNAL_AUDIT_AND_CLOUD_GOVERNANCE_v0.1.md

### Architecture and contracts
- docs/SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md
- docs/DETERMINISTIC_TRANSFER_ENGINE_CONTRACT_v0.1.md
- docs/CANONICAL_EVIDENCE_GRAPH_CONTRACT_v0.1.md
- docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md
- docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md

### Scientific evidence and analysis
- research/NASA_COMBUSTION_EVIDENCE_FAMILY_INVENTORY_v0.1.md
- research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md
- research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md
- research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md
- research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md
- research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md
- research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md
- research/PHYSICAL_COMPARABILITY_AND_TRANSFERABILITY_MATRIX_PMMA100_v0.1.md
- research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md
- research/DETERMINISTIC_TRANSFER_RULES_AND_TEST_CASES_v0.1.md
- research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md

### This Stage 1 package
- docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md
- research/SOURCE_ACQUISITION_AND_EVIDENCE_GAP_REGISTER_v1.0.md
- docs/TEST_AND_VALIDATION_MASTER_PLAN_v1.0.md

---

**Project Manager directive:** the next work package is G1. Start by resolving the PSI-25 manifest/table discrepancy and acquiring the already identified source files. Do not begin another general FiF architecture review.


## 11. Case sequencing and CI control addendum

**DEC-008 — case sequencing:** B3/B03 remains the primary PMMA-100 transferability case. B6 is a separate detailed reconstruction and method-validation case. B1 remains a candidate comparator, not a validated control. B6 does not replace B3 without an explicit later decision supported by evidence.

**ISS-017 — CI branch coverage:** the current GitHub Actions push trigger does not include the active acquisition branch. Pull requests targeting main do trigger the workflow. Before the next code-bearing commit, either add the active working branch to the push trigger or make the PR check a mandatory pre-merge control. The current repository process uses manual review/owner authorization; no enforced branch protection is assumed.

This addendum is a refinement of the Stage 1 baseline and does not change the Stage 2 priority.


## 17. Binding product-scope reconciliation — 2026-11-04

The active product-scope baseline is defined in [FiF Product & Module Traceability Matrix v1.0](FIF_PRODUCT_MODULE_TRACEABILITY_MATRIX_v1.0.md). This section supersedes conflicting release-scope wording earlier in this document; earlier sections remain an audit of the baseline as it stood before the Project Owner's clarification.

### 17.1 Correct MVP boundary

**MVP = FiF Core + all originally listed Extensible capabilities.** Therefore CRAM-1, CRAM-2, CRAM-3, Probabilistic Anomaly Detection, Uncertainty Quantification, Advanced Experiment Transferability and FiF Research & Control are in the MVP implementation target. “Extensible” means modular and progressively implemented, not excluded from MVP. FiF Advanced Analytics is also an MVP capability. The minimum demonstrable outcome, maturity and validation evidence for every module must be specified; a placeholder or design document is not implementation.

### 17.2 Future research boundary

Validated Predictive Models, Multiphysics Simulation, Fire-Scenario Analysis, real MPC, ECLSS Decision Support and sensor/operational-system integration are **documented research directions**. Each requires a technically credible specification: scientific/operational problem, governing theory and assumptions, architecture/interfaces, required data, dependencies, validation/verification strategy, feasibility gaps and falsification/blocking conditions. Implementation may be attempted if time and evidence permit; otherwise it remains explicitly suspended, not represented as delivered.

### 17.3 Original seven-stage strategic lifecycle

The original strategic stages remain authoritative:
1. Concept & Scientific Scope — FiF Concept & Scientific Foundation v1.0.
2. NASA Data Audit — NASA Combustion Research Data Catalogue.
3. Physics & Combustion Framework — FiF Physics & Combustion Framework.
4. System Architecture — FiF Technical Architecture & ADRs.
5. MVP Specification — FiF MVP Functional & Technical Specification.
6. Validation & Demonstration — FiF Validation Report & Demonstration Scenario.
7. Competition Package — product, demonstration, documentation and presentation.

The 13 engineering stages and G0–G11 gates in this roadmap are a finer-grained execution and control breakdown. They must be mapped to the seven strategic stages; they do not replace or renumber them. The Stage 1 documentary/control milestone previously recorded is not equivalent to acceptance of original strategic Stage 1's Concept & Scientific Foundation deliverable.

### 17.4 Architecture and delivery implications

The roadmap must include an explicit path from source/evidence foundation to physics registry, analysis engines, uncertainty/anomaly services, transferability, evidence-backed synthesis, Research & Control and interactive dashboard. Shared validation/calibration services are cross-cutting. Future-research interfaces should be anticipated without prematurely building unvalidated models or operational control.

### 17.5 Status correction

This is a scope and planning correction, not a claim that any newly included module has been implemented. Existing implementation inventory in Section 2 remains the factual code baseline. Module implementation status and acceptance must be updated only when repository artefacts and test/validation evidence exist.

### 17.6 Required mapping

The new traceability matrix is the controlling module inventory. The engineering work breakdown must be reconciled against it before declaring architecture or MVP specification complete. Stage 2 / Gate G1 source inventory continues; this scope correction does not close evidence-acquisition gaps.

## 18. Explicit strategic-stage ↔ engineering-stage synchronization — 2026-11-04

The following mapping is binding for planning and reporting. Engineering stages may support more than one strategic stage; this is intentional because the seven-stage plan is a product lifecycle and the 13-stage plan decomposes technical execution.

| Original strategic stage | Original deliverable | Engineering stages mapped to it | Completion interpretation |
|---|---|---|---|
| 1. Concept & Scientific Scope | FiF Concept & Scientific Foundation v1.0 | STAGE 1 (baseline/control), with requirements and scope decisions carried through STAGE 6 | Documentary project baseline is closed; original scientific foundation deliverable remains to be reconciled/accepted. |
| 2. NASA Data Audit | NASA Combustion Research Data Catalogue | STAGE 2 (source acquisition), STAGE 3 (identity/reconciliation), source portions of STAGE 4 and STAGE 8 | Inventory, source identity, assets, metadata, provenance and acquisition completeness. G1/G2 and relevant G3/G7 work. |
| 3. Physics & Combustion Framework | FiF Physics & Combustion Framework | Scientific portions of STAGE 3; STAGE 5 (reconstruction/measurement); STAGE 6 (physics/transferability model) | Physical variables, equations, regimes, dimensional analysis, CRAM foundations, model assumptions and validity domains. |
| 4. System Architecture | FiF Technical Architecture & ADRs | STAGE 4 (canonical model/pipeline), architecture portions of STAGE 6, STAGE 7 (engine), STAGE 8 (services), architecture portions of STAGE 9 | Data contracts, modules, interfaces, services, orchestration, security and dashboard architecture. |
| 5. MVP Specification | FiF MVP Functional & Technical Specification | Requirements and acceptance decomposition across STAGE 4, STAGE 6–9 | Every MVP capability in the traceability matrix gets inputs, outputs, dependencies, implementation increments and acceptance criteria. |
| 6. Validation & Demonstration | FiF Validation Report & Demonstration Scenario | STAGE 5 (measurement evidence), STAGE 10 (integrated validation), STAGE 11 (independent audit/remediation) | Reproducible measurements, numerical/physical validation, integrated scenario, user validation and independent review. |
| 7. Competition Package | Product, demonstration, documentation and presentation | STAGE 12 (release/demo/handover) | Honest claims, frozen demo, documentation, reproducibility and presentation. |
| Post-competition lifecycle (not an eighth original stage) | Platform expansion and maintenance | STAGE 13 | Expansion only after the competition package; not a prerequisite to the original seven-stage competition lifecycle. |

### Engineering gate mapping

| Engineering gate | Engineering stage | Strategic stage(s) supported |
|---|---|---|
| G1 — Source inventory | STAGE 2 | 2 |
| G2 — Identity and reconciliation | STAGE 3 | 2, 3 |
| G3 — Evidence model | STAGE 4 | 2, 4, 5 |
| G4 — Measurement | STAGE 5 | 3, 6 |
| G5 — Science and domain limits | STAGE 6 | 3, 4, 5, 6 |
| G6 — Deterministic engine | STAGE 7 | 4, 5 |
| G7 — Data/retrieval/AI services | STAGE 8 | 2, 4, 5 |
| G8 — Product UX and interfaces | STAGE 9 | 4, 5 |
| G9 — Integrated validation | STAGE 10 | 6 |
| G10 — Independent audit | STAGE 11 | 6, 7 |
| G11 — Release and demonstration | STAGE 12 | 7 |
| G12 — Post-release expansion | STAGE 13 | Post-competition lifecycle |

**Control rule:** status reporting must name both levels where relevant (for example, “original Stage 2 / engineering STAGE 2 / G1”). Do not call original strategic Stage 1 complete solely because engineering STAGE 1 documentary baseline is closed. The original stage deliverables listed above remain the acceptance basis.
