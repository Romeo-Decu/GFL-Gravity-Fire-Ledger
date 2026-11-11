# Dossier audit, G2 docs 5-10

Independent agent report, 2026-11-11 evening (brief: AUDIT_BRIEF.md in this folder). Ground truth: repository at that time.

# Commitment audit: dossier files 5 to 10 checked against `/home/claude/fif`

## 5. FiF Strategic finding an existing solution has surfaced.md
The 3 Nov strategy memo. It reviews the competitors Fotia and MicroFire Atlas, sets DECISION 04 (GFL competes on rigour rather than breadth) and DECISION 05 (the SIBAL BASS/BASS-II vs SAFFIRE case is the first validation case), drafts the comparability/transferability engine spec v0.1 and plans the PSI-25/PSI-98 audits.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Do not build another multi-dataset dashboard with conventional ML; compete on scientific rigour (DEC-04) | governance | delivered | RES-026; GFL_MAP §1 | important |
| 2 | Keep three separate questions apart: retrieval relevance, physical comparability, transferability | analytics | partial | relevance: `tools/indus_relevance.py`. Comparability: `tools/rank_comparable_runs.py`. Transfer: `src/fif_transfer/engine.py`. Comparability has no separate output of its own (ISS-043 A7) | critical |
| 3 | Cross-investigation evidence graph (experiments, materials, conditions, measurements, publications, findings) | data | partial | `schemas/EVIDENCE_GRAPH_v0.1.schema.json`, `research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json`. Covers one case and one investigation, not several investigations | important |
| 4 | Physical comparability engine covering scale, geometry, transport and combustion regime | analytics / physics | partial | `rank_comparable_runs.py` compares 7 table cells within PSI-25 only. Geometry/confinement descriptors and regime are not computed (GFL_MAP: "Physics-based similarity … not met") | critical |
| 5 | Transferability classes: direct / conditional / weak analogy / unsupported extrapolation | analytics | partial | engine conclusions are `directly_supported`, `conditionally_informative`, `qualitatively_informative`, `undetermined`, `not_transferable_on_current_evidence`. Gate states are declared by the caller, not derived | critical |
| 6 | SIBAL BASS/BASS-II vs Saffire I–IV as the first validation case, with the 8 acceptance criteria (rebuild the matrix, flag the Saffire-IV discrepancy, refuse pooling, …) | analytics / data | dropped by decision | DEC-048: deferred until after the contest; no SIBAL or SAFFIRE file acquired. SIBAL appears only in `rank_comparable_runs.py` as a material label | important |
| 7 | Comparison dimensions (mechanism, material, atmosphere, flow, geometry, confinement, ignition, measurement, outcome), each with value, unit, source+page, epistemic status, uncertainty, missingness, conflict | data / analytics | partial | rank tool: material, geometry, thickness, width, flow restrictor, air setting, O₂, each tied to a table locator. Confinement, ignition, measurement method and outcome are not compared (listed as NOT_RECORDED) | critical |
| 8 | Per-dimension states MATCH/PARTIAL/MISMATCH/UNKNOWN/NOT_APPLICABLE, then hard physical gates; no single weighted score | analytics | partial | rank tool uses match/differs/unknown; the engine gate vocabulary is pass/partial/fail/unknown/not_applicable. No weighted score anywhere (complies) | critical |
| 9 | Four-level comparability verdict (quantitative / conditional / qualitative / non-comparable) | analytics | partial | rank levels not_comparable/same_conditions/close/distant are a different, table-only scheme | important |
| 10 | Directional assessment source → target scenario, not a symmetric similarity | analytics | not done | the engine has no source/target or scenario objects; the rank tool is relative to a reference run only | critical |
| 11 | Compute Reynolds number, hydraulic diameter, sample-to-duct ratios, or state that they cannot be computed | physics | not done | no code (grep "hydraulic" returns 0; Reynolds appears only in docs) | important |
| 12 | Unknown is never compatible; missing geometry is never a match | analytics | delivered | `rank_comparable_runs.py` ("unknown is never treated as a match"); `tests/test_engine.py::test_missing_gate_is_unknown_not_compatible` | critical |
| 13 | Four engine rules: experiment identity mandatory, flow history, sample history, outcome definitions preserved | data | partial | identity: evidence-graph tests that B3 ≠ §2.3 run. Flow history: window rules use the overlay AIR/FAN time series. Sample history and outcome typing are not modelled | important |
| 14 | Separate configuration comparability from measurement comparability | analytics | not done | none found | important |
| 15 | Fotia technical benchmark (coverage, models, validation, limitations) | docs | partial | RES-026 (short landscape entry); `research/LANDSCAPE_AND_DIFFERENTIATION_DECISION_v0.1.md` predates Fotia | nice |
| 16 | PSI-25 raw file audit and extraction | data | delivered | `data/manifests/PSI-25_v4_manifest.json` (695 files), acquisition log, 31/31 re-downloads identical | critical |
| 17 | PSI-98 (Saffire-I) raw file / telemetry audit | data | dropped by decision | DEC-048 | nice |
| 18 | Keep three value tiers separate (published by researchers, extracted from NASA files, computed by FiF); discrepancies stay visible | provenance | delivered (for B6) | `data/derived/BASSII_B6_SOURCE_VALUES_v0.1.csv`, `B6_COMPARISON_v0.1.json`, ledger tiers (DEC-025/027) | critical |
| 19 | Do not validate the engine on the case used to design it; use an independent case | analytics | partial | four pre-registered predictions on held-out runs B9/B11/B13: 1 supported, 1 not, 2 untestable (RES-035–038) | critical |
| 20 | No predictive model until the data justify one | governance | delivered | DEC-010; predictions are pre-registered ratio tests only (`tools/build_predictions.py`) | important |
| 21 | FM² lunar partial-gravity comparison (later) | analytics | not done | docs mention only | irrelevant |
| 22 | No generic fire-risk score | governance | delivered | none in code | important |

## 6. FiF Data & Provenance Schema v1.0.md
The data and provenance contract: entities, the per-value contract, 5 epistemic categories, 3 quality assessments, comparability and transfer rules, a SQLite DDL, an importer, the claimed SIBAL import and BASS reconciliation, and the PSI access route.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Separate entities (Source, Investigation, Configuration, Specimen, Run, Measurement, DerivedResult, PublicationClaim, Asset, QCRecord, Comparison, TransferAssessment, Inference) | data | partial | graph node types in `EVIDENCE_GRAPH_v0.1.schema.json`. No relational store with these entities | important |
| 2 | Per-value contract (value, unit, status, source, asset, locator, instrument, time, uncertainty, qc) | provenance | partial | ledger entries plus sealed CSVs carry locators and hashes. No general typed parameter-value store | critical |
| 3 | Five epistemic categories (measured / reported / derived / estimated / inferred); null ≠ 0 | provenance | partial | `schemas/CONTROLLED_VOCABULARY_v0.1.json` uses source_reported/measured/derived/inferred/unknown (no "estimated"). No general no-default rule (I03 "Not implemented", `research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md`) | important |
| 4 | Three independent assessments: Data Quality, Experimental Completeness, Evidence Strength | analytics | not done | ISS-043 A6 (Evidence Strength absent); no completeness score either | important |
| 5 | Comparability statuses and the four-level verdict; a high similarity score cannot override a critical MISMATCH | analytics | partial | engine: a critical incompatibility without a bridge blocks the conclusion (`test_engine.py::test_explicit_critical_incompatibility_without_bridge_blocks_transfer`). The MATCH/PARTIAL dimension scheme is not implemented | critical |
| 6 | Directional transfer T(Eᵢ→Sⱼ) answering four questions (what transfers, under which conditions, which differences change it, what is missing) | analytics | not done | none found; engine output has domain_statement/prohibited_extrapolations only | critical |
| 7 | QC and audit trail: originals immutable, corrections as new versions, conversions keep formula, everything rebuildable, `reopen_trigger` | provenance | partial | `src/gfl_ledger` (append-only, supersession, `test_supersession_*`). No `reopen_trigger`; no one-command rebuild (GFL_MAP) | critical |
| 8 | Implementation order: ingestion → normalisation → QC → engine → transfer → report → UI → AI | governance | superseded | the order actually followed was measurement, ledger, dashboard, AI layer (GFL_MAP §1) | nice |
| 9 | SQLite schema v1.0 (22 tables) plus 4–5 integrity tests "PASS" | data | not done (in repo) | no SQLite file or DDL in the repo (grep finds only AAL mentions); the claimed artefacts exist only in the chat | important |
| 10 | JSON importer v1.0 with transactional import and dry-run tests "PASS" | data | not done (in repo) | none found | important |
| 11 | Parameter registry with synonyms, SI units and conversion rules; air_velocity vs nominal_flow not merged automatically | data | not done | none found (T08/I06 "Not implemented") | important |
| 12 | Mandatory DB tests (no source → refused, unknown unit kept, NULL not 0, BASS ≠ BASS-II, critical MISMATCH ≠ quantitative) | data | partial | only the last is covered (engine); the rest have no store to test | important |
| 13 | Two-way traceability test: conclusion ↔ raw value | provenance | partial | `tools/build_experiment_memory.py`, ledger `lineage()`, `test_evidence_graph.py::test_directed_traceability_chain_includes_unknown_measurement` | critical |
| 14 | SIBAL source dataset v1.0/v1.1 (36 configurations, 326 values; GMT222-T11 candidate mapping) | data | not done in repo; dropped by decision | DEC-048; no dataset or DB in the repo | important |
| 15 | PSI access via individual-file selection, recording names, checksums, formats and IDs; AWS bucket rejected | data | delivered | `tools/psi25_fetch.py`, `data/manifests/*` | important |
| 16 | Private GitHub repo with ingestion/provenance/qc/comparability/transferability/reporting packages and PR workflow | other | partial | the repo exists with PRs and CI; the `src/` layout differs (fif_transfer, gfl_ledger, gfl_mcp) | nice |

## 7. FiF Audit repo.md
The first repo audit and the 3 Nov research log: architecture doc, BASS-II preliminary audit, MicroFire Atlas landscape, first physics case (thin PMMA opposed flow, μg vs 1g downward), B3 oxygen column reconciliation, data-access route.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Scientific & System Architecture v0.1 doc (families, model, uncertainty, abstention, MVP, validation plan) | docs | delivered | `docs/SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md` | important |
| 2 | Do not pool families (BASS-II, SAFFIRE, ACME) | governance | delivered | DEC-016 (single family); SAFFIRE not ingested | important |
| 3 | BASS-II preliminary audit (fan display ≠ velocity; Test# ≠ Sample#; video needs fps and calibration) | data | delivered | `research/BASS_II_PSI25_PRELIMINARY_AUDIT.md`; ISS-013 (flow at the sample still unknown) | critical |
| 4 | Gold-standard trace: table → test → sample → raw → config → outcome | provenance | delivered (B6) | `research/fixtures/B6_STORY_v1.json` (13-step case file), ledger | critical |
| 5 | MicroFire Atlas landscape and differentiation decision | docs | delivered | `research/LANDSCAPE_AND_DIFFERENTIATION_DECISION_v0.1.md`, RES-026 | nice |
| 6 | Differentiators promised against Atlas: physical regime modelling, extrapolation validity, uncertainty propagation, a falsifiable physical hypothesis | physics / analytics | partial | uncertainty is reported per component (RES-021). Falsifiable test: pre-registered predictions. Regime modelling and CRAM-1 not met (GFL_MAP) | critical |
| 7 | First physics case: transfer the μg thermal-regime spread relation to 1g downward spread; reproduce the model (de Ris) independently and test on unseen data | physics | not done; scope superseded | DEC-016 (anchor = μg 100 µm family); CRAM-1 "not met"; no 1g data acquired | critical |
| 8 | Reproduce the published 2.2 mm/s (μg) and 2.0 mm/s (1g); test the thin/thick transition ≈5.2 mm | physics | partial | B6 measured 1.99 / 2.197 mm/s vs the 2.2 literature value (RES-025, AR-001). The 1g value is not reproduced. Thickness exponent is exploratory (`data/derived/rw4/THICKNESS_EXPONENT_v1.json`) | critical |
| 9 | Source reconciliation audits (A.1 vs A.2, B03/B3, O₂ calibrated vs uncalibrated, Carmignani cross-check, §2.3 linkage) | provenance | delivered | `research/PMMA_SOURCE_RECONCILIATION_AUDIT_v0.1.md`, `BASSII_O2_COLUMN_RECONCILIATION_2026-11-03.md`, `SOURCE_CORRECTION_B3_OXYGEN_COLUMNS_2026-11-03.md`, `CARMIGNANI_2019_BASS_B3_CROSS_SOURCE_AUDIT_2026-11-03.md`, `SECTION_2_3_100UM_DATA_LINKAGE_AUDIT_2026-11-03.md`; ISS-012 | important |
| 10 | Narrow the first experiment to B3 (μg) plus the NASA 100 µm 1g sample | analytics | dropped by decision | ISS-025 (B3 partial burn, no steady spread); DEC-016 (B6 = method case) | important |
| 11 | Retrieve B3 originals (video, telemetry, front position vs time) | data | partial | B3 original-videos zip acquired (`data/manifests/PSI-25_acquisition_log.json`); no B3 rate measured (rightly) | nice |
| 12 | Identify the exact 1g counterpart run and its raw data | data | not done | `PROJECT_MASTER_MAP…` items 9–10 still open | important |
| 13 | Data-access route audit (PSI first, AWS rejected, SDSU fallback) | data | delivered | `research/BASSII_DATA_ACCESS_ROUTE_AUDIT_2026-11-03.md` | nice |

## 8. FiF sesiunea 2.md
The 4 Nov session. It sets the P1–P6 plan, the SDSU video-method audit, the measurement and uncertainty protocol, the physics framework (thermal/kinetic/radiative regimes, six gates), the comparability matrix (eight gates), the deterministic rules and fixtures, engine v0.1, the visualization ADR, the auditor plan and cloud use.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | P1–P2: B3 file inventory, acquisition with SHA-256 | data | delivered | acquisition log, manifest, ledger | important |
| 2 | P3: evidence reconstruction test → sample → file → conditions → spread | provenance | delivered (B6, B9, B11, B13) | RES-033/035/036/038; proof-sheet identity for B9/B13 | critical |
| 3 | P4: normal-gravity counterpart identified | data | not done | none found | important |
| 4 | P5: reproduce NASA relations, propagate uncertainty, find the domain where transfer is justified | physics / analytics | partial | measurement plus interval (R-W3/R-W4); interval coverage measured in blind test 2 (ISS-050); no physical model reproduced (CRAM-1 not met) | critical |
| 5 | Reconstruct the NASA front method (intensity, width averaging, threshold, linear regression); no universal threshold | analytics | delivered | `tools/flame_front.py`, `b6_window_rule.py`, `window_rule_r3.py`, `window_rule_r4.py`; frozen rules `docs/WINDOW_RULE_R-W3.md`, `R-W4.md` | critical |
| 6 | Video Measurement & Uncertainty Protocol v0.1: calibration, timing, regression uncertainty, threshold sensitivity, measurement error kept apart from physical variation, the φ = f/(pV_f) descriptor | analytics | partial | protocol in `research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md`; sensitivity in `tools/b6_sensitivity.py` and `b6_radiometric_audit.py`; scale in `ruler_scale.py`. φ is never computed (absent from `tools/` and `data/derived`). The luminous-edge vs pyrolysis-front offset is excluded from the interval (DEC-056) | critical |
| 7 | Physics framework: three regimes and six verification gates | physics | documented only | `research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md`; `docs/specs/SPEC_regime_gates.md` (status "partial", gates declared, not computed) | critical |
| 8 | Comparability and transferability matrix PMMA-100 (8 gates; abstention is a valid outcome) | analytics | partial | matrix doc in `research/PHYSICAL_COMPARABILITY_AND_TRANSFERABILITY_MATRIX_PMMA100_v0.1.md`; ruleset `configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json`; the engine abstains (`undetermined`) | critical |
| 9 | Deterministic rules doc (10 rules, 12 case rules, 15 test cases, 12 invariants, pseudocode) | docs | delivered | `research/DETERMINISTIC_TRANSFER_RULES_AND_TEST_CASES_v0.1.md`, `tests/fixtures/PMMA100_TRANSFER_CASES_v0.1.json` | important |
| 10 | All of T01–T15 and I01–I12 executable | analytics | partial | `research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md`: T02, T08, T09, T11, T12 and T14 plus I03, I04 and I06 "Not implemented" | important |
| 11 | Controlled vocabulary, ruleset, fixtures as machine-readable contracts | data | delivered | `schemas/CONTROLLED_VOCABULARY_v0.1.json`, `configs/…RULESET…`, `tests/test_contracts.py` | important |
| 12 | Engine `assess()` with 5 profiles, conflict scoping, bridges, audit, CLI, JSON schema, examples, CI | analytics | delivered | `src/fif_transfer/engine.py` (v0.1.3), `cli.py`, `schemas/TRANSFER_ASSESSMENT_REQUEST_v0.1.schema.json`, `examples/`, `.github/workflows/tests.yml` | critical |
| 13 | Same evidence gives different conclusions per question (documentary → conditionally_informative; quantitative → undetermined) | analytics | delivered | `tests/test_case_assessment.py` | critical |
| 14 | Visualization architecture: elkjs layout, Cytoscape interaction, Plotly charts; data independent of the renderer | UI | delivered | `docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md`, DEC-001, `visualization/`; ISS-002 (ELK routing not transferred) open | important |
| 15 | Check the elkjs licence (EPL-2.0/GPL) before distribution | governance | not done | ISS-005 open | important |
| 16 | External audit: Claude full audit after freeze, Mistral red team, blind to each other, fixed commit SHA, findings triaged | governance | partial | AAL WF-0011 audits by Mistral, grok and gpt55 (RES-014–018); the final independent review is planned for 12–13 Nov (RELEASE_A). No human expert review (ISS-043 A3) | critical |
| 17 | Windows + Linux clean-environment testing (Azure), then AWS portability and performance tests | other | not done | GFL CI is ubuntu-only; Azure is used for AAL model calls only (RES-028) | nice |
| 18 | Canonical evidence graph, PMMA-100 viz prototype, scientific data layer | data / UI | partial | graph plus `visualization/index.html`; no general data layer | important |
| 19 | Three validation levels kept distinct (software / scientific / transferability) | governance | delivered | engine audit field `scientific_validation_status: not_established_by_software_execution`; DEC-013 | critical |

## 9. FIF Audit dupa prima etapa.md
The engine audit and hardening, evidence graph, Evidence Explorer, PR #3, the evidence acquisition protocol proposal, the multi-agent verification cycle, and the first statement of the zero-trust protocol.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Hardening: a pass needs reasons, evidence and rule IDs; not_applicable must be authorised; critical incompatibilities scoped per inference | analytics | delivered | `engine.py` lines 125–216; `test_engine.py` (`test_pass_requires_…`, `test_not_applicable_is_rejected_…`, `test_critical_incompatibility_outside_profile_does_not_block`) | critical |
| 2 | Evidence references verified against real sources, not just declared IDs | provenance | not done | the engine checks only that refs are non-empty strings | critical |
| 3 | Reproducibility: SHA-256 of request and ruleset, engine version | provenance | delivered | `engine.py` `_canonical_sha256`; `test_audit_hashes_are_stable_and_present` | important |
| 4 | Canonical graph schema plus PMMA-100 fixture plus regression tests | data | delivered | `schemas/EVIDENCE_GRAPH_v0.1.schema.json`, `tests/test_evidence_graph.py` (16 tests) | important |
| 5 | Evidence Explorer (ELK + Cytoscape + Plotly, 2 vs 3 cm/s shown separately, JSON export) with Chromium/Firefox tests | UI | delivered | `visualization/index.html`, `visualization/tests/browser-smoke.mjs`, CI job | important |
| 6 | Evidence Acquisition Protocol v0.1 as an official doc plus machine-readable format | provenance | delivered | `docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md`, `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`, `tests/test_acquisition_package.py` | important |
| 7 | First Claude acquisition package for B3 (sources, experiments, observations, claims, conflicts, log) through a PR | data | not done; superseded | `research/acquisition/PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json` has 0 source, asset, extraction and linkage records; the work moved to B6 (DEC-016) and to sealed CSVs | important |
| 8 | Adapter between the acquisition package and the evidence graph | data | not done | none found | nice |
| 9 | Verification cycle: Claude acquires → automated validation → ChatGPT verifies → correction → final review → Mistral challenge | governance | partial | DEC-015; ChatGPT red team RES-005 (`data/external/2026-11-05_chatgpt_redteam2_DEC-032.md`); AAL WF-0011; DEC-024 records a merge without the required review | important |
| 10 | Triple verification V1/V2/V3 per data record | provenance | partial | for measurements: blind independent analyses and GFL re-execution (WF-0011, AAL tests 1–2, `tools/wf0011_cross_validation.py`). Not per record | critical |
| 11 | Lifecycle states INGESTED → QUARANTINED → … → ELIGIBLE FOR USE; promotion blocked on failure | provenance | not done | none of the states exist in code (grep returns 0) | critical |
| 12 | Nobody (founder, PM, AI) can bypass validation; no force-approve; AI cannot approve its own output | governance | partial | ledger role separation: `test_pipeline_key_cannot_forge_approval`, `test_owner_key_cannot_write_data_entries` (DEC-031). No ingestion gate exists that could refuse a founder-entered value | critical |
| 13 | Fail-closed validation at every layer (UI, API/ingestion, schema, semantic, DB, engine, CI, audit) | provenance | partial | schema, engine, ledger and CI exist; there is no ingestion API, DB or input UI | critical |
| 14 | Adversarial tests with deliberately false, incomplete, contradictory, wrong-unit or unjustified records | analytics | partial | tamper tests in `tests/test_gfl_ledger.py`; malformed-input tests in `test_engine.py`; synthetic planted-truth tests (AAL tests 1–2). No false-record ingestion tests | critical |
| 15 | B3 pilot: refuse 2.2 mm/s as a B3 result | analytics | delivered | `test_evidence_graph.py::test_22_mm_s_maximum_is_not_linked_to_b3`; ISS-025 | important |
| 16 | Fix the architecture doc listing "conflicting" as an individual evidence state | docs | delivered | the term no longer appears in `docs/SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md`; `test_evidence_state_vocabulary_is_not_overloaded_with_conflict` | nice |
| 17 | Independent audit by a non-participant; release gate | governance | partial | planned 12–13 Nov (RELEASE_A); not yet done | critical |

## 9.1 FiF — Scientific Evidence Acquisition Protocol v0.1.md
The standalone version of the acquisition protocol (records, locators, transformations, conflicts, log, acceptance criteria, GitHub workflow) plus the B3/PMMA-100 acquisition task. It duplicates part of file 9, so only items with distinct status are listed.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Protocol with record types, locators, evidence_state vocabulary, acceptance criteria | provenance | delivered (as contract) | `docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md`, schema, tests | important |
| 2 | Transformation records (inputs, formula, software, parameters) for every derived value | provenance | partial | ledger `derivation` entries need a method (`test_derivation_without_method_refused`); no general unit-conversion lineage (I04, I06 not implemented) | critical |
| 3 | Conflict and uncertainty register with resolution states | provenance | partial | ISS records in the register; graph keeps both flow assertions (`test_flow_discrepancy_preserves_both_source_assertions`); no machine-readable conflict register | important |
| 4 | Extraction log per operation | provenance | partial | `data/manifests/PSI-25_acquisition_log.json`; experiment memory | nice |
| 5 | RQ: locate and access the B3 video | data | delivered | acquisition log (B3 original-videos zip); ISS-025 | nice |
| 6 | RQ: establish the actual opposing-flow velocity | physics | not done | ISS-013 open (air display → cm/s at the sample unknown) | critical |
| 7 | RQ: reconstruct the 100 µm rate from original imagery | analytics | delivered (B6, not B3) | AR-001; R-W3/R-W4 results in `data/derived/rw3`, `data/derived/rw4` | critical |
| 8 | RQ: method, frame rate, spatial calibration, threshold | analytics | delivered | `ruler_scale.py`, window rules; ISS-020/027 limits | critical |
| 9 | RQ: link 2.2 mm/s to B3 | provenance | delivered (negative result) | ISS-025: not attributable | important |
| 10 | RQ: trace the 1g 2.0 mm/s to its run | data | not done | none found | important |
| 11 | RQ: material equivalence (grade, preparation, thermal properties) | physics | not done | ISS-011 (B3 cell omits PMMA); no property data | important |
| 12 | Deliverables: populated registries plus validation report plus PR | data | not done | the package template is empty (see file 9, row 7) | important |

## 9.2 FiF Zero-Trust Scientific Integrity Protocol..md
The standalone version of the zero-trust protocol, with roles anonymised as x/y/z. Its commitments are identical to file 9, rows 9–17.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Admissibility, verification, validation, demonstration, independent verification and audit kept as distinct stages | governance | partial | DEC-013, DEC-030; ledger qualifiers; no stage machine | critical |
| 2 | Eight-state data lifecycle; corrections as linked new versions | provenance | partial | versioning via ledger supersession; no lifecycle states | critical |
| 3 | Transcription fidelity never conflated with physical truth | provenance | delivered | ledger tiers (DEC-025/027); vocabulary `source_reported` vs `measured` | critical |
| 4 | Zero trust including founder, admins, AI; no force-approve | governance | partial | DEC-031 role keys, owner-only approvals; no data-entry gate | critical |
| 5 | Multi-layer fail-closed protections (9 layers) | provenance | partial | 4 of 9 layers exist (schema, engine, ledger, CI) | critical |
| 6 | Supreme acceptance test: detect and block an error planted by the founder, PM or AI, shown by adversarial tests and independent audit | governance | partial | ledger detects alteration after sealing (`test_raw_byte_changed_is_sealed_alteration`, browser verification). Nothing blocks a false value entered before sealing; no planted-founder-error test found | critical |
| 7 | Transfer engine refuses ineligible data | analytics | not done | the engine takes caller-declared gate states and has no notion of eligibility | critical |

## 10. FiF Interfata si Graphs.md
Mermaid/ELK technology notes, the decision for two interfaces (human and AI/machine) on one shared core, the PR #3 review and removal of `validated_graph`.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Diagrams-as-code (Mermaid/ELK) for architecture | docs | delivered | `docs/diagrams/D01…D11*.mmd` | nice |
| 2 | Human interface: question- and activity-led navigation, guided forms with units, provenance, uncertainty and conflicts visible, explicit accepted/verified/undetermined states | UI | partial | `visualization/gfl.html` (case file, predictions, AI findings, capability map with states, DEC-043). No guided input forms; navigation follows sections, not user questions | important |
| 3 | Researcher can find, compare two experiments, see why a conclusion is accepted/conditional/undetermined, and see what is missing | UI | partial | comparable-run ranking and the engine verdict shown; no free two-experiment comparison | important |
| 4 | Progressive disclosure; graph as an expert view, not the entry point | UI | delivered | `gfl.html` is the entry point; graph in `index.html` | nice |
| 5 | AI/machine interface: typed graph, stable JSON contracts, deterministic queries, hashes and validation history, controlled access | AI layer | partial | `src/gfl_mcp/server.py` (read-only: search_memory, get_record, verify_ledger, rank_comparable_runs, assess_transfer, list_ai_findings), `tests/test_gfl_mcp.py`. No graph traversal API; access control is read-only only | important |
| 6 | One shared core and Zero Trust for both interfaces | AI layer | partial | MCP and dashboard read the same sealed files and ledger | important |
| 7 | Accessibility and responsive behaviour tested | UI | partial | phone viewport test (`visualization/tests/gfl-smoke.mjs:80`); no accessibility test | nice |
| 8 | Remove the graph-level `validated_graph` / lifecycle status; future validation bound to the graph hash | provenance | delivered (removal) / not done (binding) | `test_evidence_graph.py::test_graph_cannot_self_declare_validation_or_lifecycle_state`; no hash-bound validation record for the graph | important |
| 9 | Prototype in English and graph-first flagged as a defect to fix | UI | superseded | the dashboard `gfl.html` replaced the graph-first entry point | nice |

## Cross-file findings

- **Physics analytics are essentially absent as platform modules.** No regime classifier (thermal/kinetic/radiative), no de Ris/CRAM-1 calculation, no CRAM-3, no dimensionless descriptors (Re, hydraulic diameter, φ = f/(pV_f), sample/duct ratios). `SPEC_regime_gates.md` itself says the gates are "declared from the source audit, not computed". The six-gate and eight-gate frameworks of file 8 exist only as documents.
- **The transfer engine is a logic evaluator, not a transferability engine.** `engine.py` turns caller-declared gate states into a verdict. It does not compute comparability, is not directional (no source/target scenario), does not check evidence refs against sources, and has no notion of data eligibility. Many of the fixtures it was built against are not implemented (T02, T08, T09, T11, T12, T14; I03, I04, I06). The directional T(E→S) assessment promised in files 5 and 6 does not exist.
- **Comparability exists only as a single-investigation table ranking.** `rank_comparable_runs.py` compares 7 recorded PSI-25 cells against B6. It does not compare across investigations and does not represent geometry/confinement/ignition/measurement-method, which files 5–6 call the "core differentiator". The MATCH/PARTIAL/MISMATCH and four-level verdict schema is not implemented. Comparability has no separate output (ISS-043 A7).
- **File 6's claimed artefacts (SQLite 22 tables, importer, SIBAL DB with 36 configurations and 326 values, v1.1 reconciliation) are not in the repository.** If any jury material or document cites them, that is an unsupported claim. The SIBAL case is formally deferred (DEC-048), but the chat text reports these as built and tested.
- **The zero-trust data lifecycle is not implemented.** The eight states, quarantine, per-record V1/V2/V3 and multi-layer fail-closed ingestion do not exist. What exists is tamper-evidence after sealing (signed hash-chained ledger, role-separated keys). So "the platform will not let even the founder enter invalid data" (files 9/9.2) is not met: a false value can still be sealed. The ledger only proves it was not changed afterwards.
- **Evidence acquisition is a contract without content.** The schema and protocol exist, but the B3 package has 0 records, and no acquisition-package-to-graph adapter exists. Real provenance lives in ledger entries and sealed CSVs instead, so the documents and the repo describe two different provenance architectures.
- **The physics hypothesis was never tested.** Files 7–8 hypothesised that the μg thermal-regime relation transfers to 1g downward spread. Neither the 1g counterpart run nor the material equivalence was established. The jury-facing transfer evidence is instead four within-μg ratio predictions: 1 supported, 1 not supported, 2 untestable (GFL_MAP §6).
- **There is a scientific tension in the repo's own results.** GFL_MAP Q6 proposes a thin-to-thick transition near 400 µm to explain the failed B13 prediction. But `THICKNESS_EXPONENT_v1.json` gives n ≈ −1.1 to −1.2 at displays 3/4 using B13 data, which is consistent with thermally thin (∝1/τ) scaling, so it argues against that explanation. File 7 cites a ~5.2 mm transition thickness. I did not trace which configuration NASA's 5.2 mm applies to. All three statements need reconciling before any regime claim.
- **Uncertainty is reported but not fully propagated.** The intervals exclude the luminous-edge vs pyrolysis-front offset (DEC-056, ISS-050), and pooled coverage in blind test 2 was 15 of 24. Flow speed at the sample (ISS-013) stays unknown, which blocks any physical (cm/s) comparability or regime calculation.
- **Governance commitments are partly unmet.** Windows/Linux and Azure testing of GFL itself was not done (CI is ubuntu-only). The elkjs licence review is still open (ISS-005), which matters for the open-licence compliance item. The independent final audit and a human expert review (ISS-043 A3) are still outstanding. One merge bypassed the required review (DEC-024).
