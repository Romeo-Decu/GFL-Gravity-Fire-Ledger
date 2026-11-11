# Dossier audit, G1 docs 0.0-4

Independent agent report, 2026-11-11 evening (brief: AUDIT_BRIEF.md in this folder). Ground truth: repository at that time.

## 0.0 Analiza Concepte Initiale si Corectii.md
A scientific critique of FiF v4 (physics, CRAM, dimensionless numbers, sensors, EKF, MPC, code) with proposed corrections. It sets the three-level split between the Space Apps deliverable, research and advanced work.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Build the Space Apps deliverable as "exploitation of NASA experimental data", with Research and Advanced kept as later directions | governance | delivered | DEC-010, DEC-014 (V/P/D maturity); `research/fixtures/GFL_CAPABILITIES_v1.json` "Research extensions (not delivered)" | critical |
| 2 | Transport model keeps advection, diffusion, reaction and residual acceleration (no "pure diffusion") | physics | documented only | `research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md`; no code | important |
| 3 | Add material inputs: fuel nature, geometry, heat flux, k/cp, pyrolysis kinetics, species, O₂, pressure, diffusivities, ventilation, aerosols | physics/data | not done | `rank_comparable_runs.py` uses 7 table fields only (material, geometry, thickness, width, restrictor, air display, O₂); no property data, no pressure | important |
| 4 | Keep heating, pyrolysis, mixing, ignition and spread/extinction separate in the information model | physics | documented only | physics framework §2; ignition and extinction out of the measured result (DEC-048) | important |
| 5 | Jensen convexity removed from its role as physical validation | analytics | dropped by decision | DEC-011 | nice |
| 6 | Fix d²R/dt² (divide by Δt², handle noise and uneven sampling) and relate it statistically to real events | analytics | dropped by decision | the CRAM single score was abandoned (DEC-011); no temporal-acceleration indicator exists | nice |
| 7 | Keep Lyapunov/Takens as an experimental indicator, with a corrected method (Theiler window, validated embedding) | analytics | not done | grep "lyapunov" finds nothing in code; CRAM-3 is "designed" (`docs/specs/SPEC_cram.md`) | nice |
| 8 | Treat the CRAM score as a heuristic (units, normalisation, calibration, uncertainty) | analytics | dropped by decision | replaced by an indicator vector, DEC-011 | important |
| 9 | Reduced kinetic model per material before computing Damköhler | physics | not done | grep "damk" finds nothing in code | important |
| 10 | Compute Re, Pe_T, Pe_m, Ra (with g_eff), Da, Sc and Le as the phenomenon requires | physics/analytics | not done | none of these appear in `src/` or `tools/`; mentioned only in `docs/specs/SPEC_regime_gates.md` | critical |
| 11 | Real Mahalanobis distance with covariance and uncertainty | analytics | superseded | 0.2 §1.7 makes it optional and later; no code | nice |
| 12 | Dimensionless similarity alone is not enough: also compare fuel, geometry, pressure, configuration, mechanism and boundary conditions | analytics | partial | `tools/rank_comparable_runs.py` (BASS-II only; no pressure, mechanism or boundary conditions); engine gates are declared, not computed (`docs/METHODS_AND_VALIDATION_v1.md` §6) | critical |
| 13 | Separate what sensors measure from what models estimate; research instruments are not flight sensors | data | dropped by decision | DEC-010; `docs/specs/SPEC_sensor_integration.md` (designed) | irrelevant |
| 14 | EKF not presented as validated estimation | analytics | dropped by decision | not carried forward; no EKF code | irrelevant |
| 15 | Suspend automatic MPC control; analysis and recommendation only | governance | dropped by decision | DEC-010; `docs/specs/SPEC_real_mpc.md`; "no actuation" in Release A | important |
| 16 | No "Flight-Grade", "NASA-certified" or "guaranteed" wording | docs | delivered | grep finds none in README, docs or `visualization/gfl.html` | important |
| 17 | Do not pool FLEX, ACME, SoFIE, SAFFIRE and SAME in one vector database without metadata | data | delivered | `research/fixtures/NASA_FAMILIES_v1.json` "families are not pooled" | important |

## 0.1 FiF Directii de Dezvoltare si GFL v1.md
Proposal V1, "Knowledge & Intelligence Engine". It covers the architecture, CRAM-1/2/3, Dynamic Dependency Analysis, the AAL test design, a claims register, a six-stage plan, the MVP list and a three-level split.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Answer 9 question types (which experiments, conditions, variables, results, supported conclusions, contradictions, physical comparability, gaps, safety implications) | AI layer | partial | only for BASS-II/PMMA-100 through the register, memory and MCP (`src/gfl_mcp/server.py`); no question answering across NASA findings; "fire-safety insight today" still open (ISS-043) | critical |
| 2 | Layered architecture: data engineering → physics engine → AI engine → validation → dashboard | other | partial | data, provenance and dashboard are built; no physics engine (no physics code in `src/`) | critical |
| 3 | Physics-Based Experiment Similarity from a user scenario: why comparable, what differs, what transfers, what does not, what is missing | analytics | partial | ranking takes a fixed reference run plus an air setting, inside BASS-II only (`rank_comparable_runs.py`, MCP `rank_comparable_runs`); transfer engine has one case (`visualization/data/transfer_pmma100.json`); no free scenario input | critical |
| 4 | CRAM-1 Thermodynamic State (heat and mass transport, gradients, properties, anomalies) | analytics/physics | not done | `docs/specs/SPEC_cram.md` "designed. Not built."; GFL_MAP lists CRAM-1 as not met | critical |
| 5 | CRAM-2 Combustion Dynamics (kinetics, pyrolysis, ignition, spread, extinction, stability) | analytics/physics | partial | only "first evidence": B9/B6 flow independence and a thickness exponent from −1.0 to −1.2 (RES-038, `tools/thickness_exponent.py`, exploratory); no classifier | critical |
| 6 | CRAM-3 Nonlinear (regime changes, anomalies, transfer entropy, Lyapunov, uncertainty) | analytics | not done | no matching code; SPEC_cram | important |
| 7 | Replace the single risk score with an indicator vector with explanations and uncertainty | analytics | partial | B6 reported as a set of kinematic indicators (DEC-033) with separate uncertainty components; no thermodynamic indicators | important |
| 8 | Dynamic Dependency Analysis module (Pearson/Spearman, MI, TE, cross-correlation, AR models, surrogate tests, confidence intervals) | analytics | not done | none found | important |
| 9 | AAL tested on organisational, scientific and self-correction axes | AI layer | partial | WF-0011, AAL tests 1 and 2 (RES-011…020, RES-032, RES-034, DEC-054) | nice |
| 10 | AAL test scenarios: Known Physics, Conflicting Evidence, Unknown Scenario, each with 9 metrics | AI layer | partial | known-truth synthetic tests done (DEC-053, RES-032/034); no Conflicting-Evidence or Unknown-Scenario test found | nice |
| 11 | Adversarial test: independent agents, same problem, results checked against literature and independent calculation, undetected errors counted | AI layer | delivered | `blind_B6`, `blind_api_B6`; RES-019; RES-034 (pooled coverage 15/24) | important |
| 12 | Explicit claims register (supported / plausible / undemonstrated) | governance/docs | partial | the deviation register plus DEC-029 claim wording; no claims-verdict table found | important |
| 13 | Stage 1: correct physics, identify available NASA data, classify experiments, define variables and units | physics/data | partial | `NASA_FAMILIES_v1.json` (8 families, 7 still at ladder stage 1–2); controlled vocabulary in `schemas/` | important |
| 14 | Stage 2: ingestion, metadata schema, experiment similarity, retrieval with source checks, knowledge graph | data | partial | PSI-25 manifest and fetch; `schemas/EVIDENCE_GRAPH_v0.1.schema.json`; graph prototype for PMMA-100 only; INDUS retrieval (RES-030) | critical |
| 15 | Stage 3: physics engine (transport equations, dimensionless parameters, kinetic models, validation on experiments) | physics | not done | none found | critical |
| 16 | Stage 4: CRAM rebuild (validated indicators, nonlinear analysis, TE, uncertainty and prediction) | analytics | not done | SPEC_cram; GFL_MAP | critical |
| 17 | Stage 5: dashboard with search and comparison of experiments, physical visualisations, AI interpretation with sources | UI | partial | `visualization/gfl.html` (capabilities, predictions, transfer, relevance, families); no free search across experiments; AI summaries cover AAL findings, not NASA findings | critical |
| 18 | Stage 6 (risk prediction, real MPC, cyber-physical simulation, safety) as research only | governance | delivered | DEC-010; specs for predictive, MPC, multiphysics and ECLSS (designed) | nice |
| 19 | MVP: structured database of relevant NASA experiments | data | partial | BASS-II table sealed (129 rows); the other families are not acquired | critical |
| 20 | MVP: semantic search plus filtering by physical parameters | AI layer/UI | partial | INDUS relevance over 24 PDFs, run offline (RES-030); filtering limited to BASS-II rows | important |
| 21 | MVP: AI interpretation module with evidence citations | AI layer | partial | `tools/check_citations.py`, `tools/ai_second_check.py`, `data/derived/AI_FINDINGS_SECOND_CHECK_v1.json` (scope is GFL's own records, not NASA findings) | critical |
| 22 | MVP: a demonstration study answering a concrete fire-safety problem | analytics | partial | B6 spread rate plus the transfer case (µg vs 1g downward) is not a fire-safety scenario answer (ISS-043) | critical |
| 23 | "Five experiments analysed rigorously" | data/analytics | partial | one investigation (BASS-II); four runs measured (B6, B9, B11, B13; RES-033…038) | critical |
| 24 | Level 2: knowledge graph of experiments, materials, fuels and phenomena | data | partial | graph prototype for PMMA-100 only (`research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json`) | important |
| 25 | Level 2: temporal analysis and anomaly detection where series exist | analytics | partial | window-rule gates flag clipping, gaps and flow changes (`tools/window_rule_r4.py`); no standalone detector (anomaly marked "designed") | important |
| 26 | Level 3: "documented, and demonstrable on the platform as in development" | UI/docs | delivered | DEC-043: designed cards open their specs in `visualization/spec.html` | important |
| 27 | Rule: no capability claim without an implementation path, evidence and a validation criterion | governance | delivered | DEC-013, DEC-014; specs list validation and blocking conditions | critical |

## 0.2 FiF Audit si PLan v1.md
Working baseline v0.1 (3 Nov): consolidated scientific audit of v4, NASA family priorities, new architecture, five MVP modules, three generations of future modules, a seven-stage plan and seven competitiveness criteria.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | New positioning: a physics-aware platform for traceable, comparable insights (not fire prediction) | governance | delivered | README; METHODS §1 (relevance / comparability / transferability) | critical |
| 2 | Species and energy transport equations, solid and gas phases modelled separately (pyrolysis, vapour flux) | physics | documented only | physics framework doc; no code | important |
| 3 | Classify phenomena (droplet, gas non-premixed, solid, surface spread, smoulder, aerosol, extinction) and keep them separate | data | partial | `NASA_FAMILIES_v1.json` separates by phase; no per-experiment phenomenon classifier | important |
| 4 | Remove the hypothetical sensor array from the MVP | other | dropped by decision | DEC-010 | irrelevant |
| 5 | Lyapunov only as an experimental module if the data justify it | analytics | not done | SPEC_cram (CRAM-3) | nice |
| 6 | CRAM indicator vector: each indicator with physical definition, unit, validity domain, data source, uncertainty and validation method | analytics | not done | no indicator registry; only B6 kinematic indicators (DEC-033) | critical |
| 7 | Dimensionless set (Re, Pe_T, Pe_m, Sc, Le, Da, Ra, radiative and pyrolysis parameters) chosen per phenomenon | physics | not done | none found in code | critical |
| 8 | Matching dimensionless numbers does not imply equivalence; also check 10 listed factors (fuel, geometry, pressure, O₂, boundary conditions, regime, chemistry, radiation, configuration) | analytics | partial | engine policy plus the ranking's `NOT_RECORDED` list; pressure, radiation and chemistry are not dimensions | critical |
| 9 | Transfer entropy as a CRAM research module, compared with Pearson/Spearman/MI/AR and tested against surrogates | analytics | not done | none found | important |
| 10 | Physics-Based Similarity Engine with a multidimensional comparability matrix (compatible / different / unknown), explanation, and no single "magic score" | analytics | partial | `rank_comparable_runs.py` (match/differs/unknown, BASS-II only); vocabulary `dimension_status` in `schemas/CONTROLLED_VOCABULARY_v0.1.json`; engine `no_score: true` | critical |
| 11 | Mahalanobis later, on normalised features with a valid covariance | analytics | not done | none | nice |
| 12 | No actuator control; recommendations with evidence only | governance | dropped by decision | DEC-010; SPEC_real_mpc | important |
| 13 | Remove the RLM/MCTS/INT4/latency/radiation claims | docs | delivered | not present in the repo's public docs or page | important |
| 14 | Proper FMEA; HUD shows problem, evidence level, uncertainty, recommendation, reason and source | UI/docs | partial | the page shows evidence state, uncertainty and source per item; no FMEA found | nice |
| 15 | Remove impact claims (30–60 min warning, automatic prevention, commercialisation, Flight-Grade) | docs | delivered | none found | important |
| 16 | Family selection SoFIE / BASS-II / SAFFIRE / SAME / FLEX / ACME-BRE, each verified for data availability, format, numeric values, metadata, reproducibility and citability | data | partial | BASS-II at ladder stage 6; SAFFIRE at stage 2; the others at stage 1 "not yet located" (`NASA_FAMILIES_v1.json`) | critical |
| 17 | First activity: Data Availability Audit | data | delivered | `research/BASS_II_PSI25_PRELIMINARY_AUDIT.md`, `BASSII_DATA_ACCESS_ROUTE_AUDIT_2026-11-03.md`, `NASA_COMBUSTION_EVIDENCE_FAMILY_INVENTORY_v0.1.md` | critical |
| 18 | Common per-experiment schema (ID/DOI, configuration, fuel, atmosphere, flow, gravity, phenomenon, results with units and uncertainty, provenance down to page/table/figure) | data | partial | `schemas/EVIDENCE_GRAPH_v0.1.schema.json` (node types, evidence_state, source_locators); no experiment-profile records beyond the PMMA-100 fixture (ISS-043 A2) | critical |
| 19 | Every value has provenance; AI never fills gaps unmarked | provenance | delivered | `src/gfl_ledger`; evidence_state vocabulary; DEC-004 | critical |
| 20 | Physics engine: regime identification, dimensionless calculation, dimensional-consistency check, incompatibility detection, transferability limits | physics/analytics | partial | incompatibility and limits in `src/fif_transfer/engine.py` (gates declared); regime, dimensionless numbers and dimensional checks not done (SPEC_regime_gates: designed) | critical |
| 21 | Intelligence engine: search documentation, find experiments, extract conclusions, compare, find contradictions, synthesise | AI layer | partial | INDUS relevance (relevance only), AI findings and citation check; no extraction of conclusions from NASA papers; no cross-source synthesis for a question (GFL_MAP) | critical |
| 22 | AI never decides physical equivalence; explicit rules do | AI layer | delivered | deterministic engine and ranking; DEC-046(3) | critical |
| 23 | Validation layer per conclusion: source, data, reasoning, assumptions, confidence, missing info, contradictions | provenance | partial | ledger, deviation register, experiment memory (DEC-042); no per-conclusion confidence object | critical |
| 24 | MVP module: NASA Research Explorer (search and filter investigations) | UI | partial | families section lists 8 families; no search or filter across investigations | important |
| 25 | MVP module: Experiment Intelligence (extract and synthesise results) | AI layer | partial | B6 extraction only; synthesis designed (`docs/specs/SPEC_evidence_synthesis.md`) | critical |
| 26 | MVP module: Physics-Based Similarity | analytics | partial | see #10; GFL_MAP lists "physics-based similarity: not met" | critical |
| 27 | MVP module: Evidence & Transferability | analytics | partial | engine on one case; held-out test 1/4 supported (RES-037) | critical |
| 28 | MVP module: Interactive Dashboard | UI | delivered | `visualization/gfl.html`; RES-023 browser tests | critical |
| 29 | Central demo: material plus O₂, pressure and low-velocity ventilation → most relevant experiments (BASS-II, SoFIE, SAFFIRE, SAME, ACME-BRE) and how transferable they are | analytics | not done | only BASS-II is used; cross-family case deferred (DEC-048, SIBAL vs SAFFIRE) | critical |
| 30 | Show the difference between ignition, spread and smoke experiments | analytics | partial | stated in the families fixture; ignition and extinction out of the measured scope (DEC-048) | important |
| 31 | Extensible modules (CRAM-1/2/3, probabilistic anomaly detection, UQ, advanced transferability) | analytics | partial | DEC-009 made them MVP targets; status in GFL_MAP: CRAM-1 not met, CRAM-2 first evidence, CRAM-3 not met, anomaly partly met, UQ partly met, held-out partly met | critical |
| 32 | Seven stage deliverables: Concept & Sci Foundation, NASA Data Catalogue, Physics Framework, Tech Architecture & ADRs, MVP Spec, Validation Report & Demo, Submission | docs | partial | `PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md`, `SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md`, `ADR_001`, family inventory, METHODS draft; the 7 canonical documents are not consolidated (DEC-019, GFL_MAP) | critical |
| 33 | Seven competitiveness criteria (scientific accuracy, data integrity, physical intelligence, analytical value, explainability, feasibility, originality) | governance | partial | integrity and explainability strong; "physical intelligence" (computed comparability) weak | important |
| 34 | Negative evidence: say "not comparable" or "data insufficient" | analytics | delivered | engine returns `undetermined` / `not_transferable` with the blocking gate named; ranking treats unknown as against (DEC-018) | critical |
| 35 | Compare FiF output with a manual analysis on the same sources to show a measurable improvement | analytics | not done | none found (blind AI vs GFL exists, manual vs FiF does not) | important |

## 1. FiF Definirea Problemei.md
Working rules plus the central hypothesis and the distinctive contribution.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | No scientific claim without equations, units, assumptions, sources and validity domain | governance | partial | AR-001 and METHODS follow it; no physics equations implemented | important |
| 2 | No promised feature without an implementable mechanism and an acceptance criterion | governance | delivered | DEC-013/014; Release A acceptance table; specs | critical |
| 3 | Decision register (accepted, rejected, why, what evidence would reopen) | governance | delivered | `docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md` | critical |
| 4 | Distinctive contribution: explain how far findings apply to a new scenario and where the comparison stops being valid | analytics | partial | transfer engine (one case, declared gates); held-out predictions 1/4 supported (RES-037) | critical |
| 5 | Check whether NASA already has similar internal tools | other | partial | landscape reviewed competitors (RES-026, `LANDSCAPE_AND_DIFFERENTIATION_DECISION_v0.1.md`); NASA internal tools not checked | nice |
| 6 | Keep the AAL-coordinated "Plan A" separate and do not mix its results with FiF | governance | partial | AAL is used inside GFL as blind analysis (DEC-049/053); results kept as separate records | nice |

## 2. FiF Project Governance .md
Project charter: mission, decision authority, five frozen strategic decisions, roadmap and initial thesis.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Success condition: a working demo whose claims, data and outputs survive independent scrutiny | governance | partial | cold review (RES-024), independent audit (ISS-053), blind tests; no human expert (DEC-045) | critical |
| 2 | Keep a decision log including rejected alternatives | governance | delivered | register (e.g. withdrawn DEC-032, superseded RES-001) | important |
| 3 | Distinguish implemented capabilities from future research | governance | delivered | DEC-043/044 capability map with built/partial/designed states | critical |
| 4 | Rebuild from the scientific foundation; v4 is only a source of ideas | governance | delivered | no v4 code in the repo | important |
| 5 | Solve the actual challenge, not autonomous fire control | governance | partial | fire control dropped (DEC-010); the challenge's verbs "summarize, rank, interpret NASA findings" only partly met (ISS-043 A1; DEC-046) | critical |
| 6 | Physics before AI; AI cannot invent equivalence | AI layer | delivered | deterministic engine and ranking | critical |
| 7 | Data availability determines the architecture | data | delivered | Data Audit; DEC-016 anchor chosen from the audited data | important |
| 8 | Differentiator: physics-based comparison and transferability | analytics | partial | see 0.2 #10 and #27; regime gates not computed from data | critical |
| 9 | Roadmap: Physics & Combustion Framework (mechanisms, equations, dimensionless parameters, validity) | physics | documented only | physics framework doc (thin PMMA only) | critical |
| 10 | Independent validation: calculations, provenance, physical comparisons, AI outputs and failure cases | governance | partial | software, provenance and AI outputs validated; physical comparisons are not validated (METHODS §8, "Not validated") | critical |
| 11 | Answer five research questions: relevance, legitimate transfer, which differences invalidate transfer, supporting evidence, unknowns | analytics | partial | answered for BASS-II/PMMA-100 only | critical |

## 3. FiF — Concept & Scientific Foundation v1.0.md
Foundation baseline (3 Nov): problem, objective, RQ1–RQ6, comparability framework, scope, principles, acceptance criteria and risks.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Keep apart: NASA measured / researchers concluded / FiF calculated / FiF inferred / unknown | provenance | delivered | `evidence_state` enum (measured, source_reported, derived, inferred, unknown) in schemas and graph | critical |
| 2 | Four analytical levels: discovery, interpretation, comparison, transferability | analytics | partial | comparison and transferability inside BASS-II; discovery limited to INDUS relevance; interpretation for B6 only | critical |
| 3 | RQ1: evidence-backed discovery and ranking of investigations | analytics | partial | ranking covers runs inside BASS-II, not investigations | critical |
| 4 | RQ2: structured experimental profiles | data | partial | table parsing in `rank_comparable_runs.py`; profile records not produced (ISS-043 A2) | critical |
| 5 | RQ3: interpretable comparison, not a black box | analytics | delivered (BASS-II) | per-dimension match/differs/unknown in `data/derived/BASSII_COMPARABLE_RUNS_v1.json` | critical |
| 6 | RQ4: qualified transferability assessment | analytics | partial | engine on one case; RES-037 | critical |
| 7 | RQ5: gaps, contradictions, negative evidence | provenance/analytics | delivered | deviation register; engine refusals | critical |
| 8 | RQ6: AI synthesis without distortion, verified at source level | AI layer | partial | citation checker plus second model (DEC-046); scope is GFL's records, not NASA literature | important |
| 9 | Comparability framework across 9 dimensions (fuel, regime, O₂/pressure, geometry, flow/transport, gravity, thermal/radiative, instrumentation/uncertainty, scale/boundary conditions) | analytics | partial | 7 table dimensions in ranking; pressure, gravity, radiative, instrumentation and scale absent | critical |
| 10 | Per-dimension status: comparable / partial / materially different / unknown / not applicable | analytics | delivered | `dimension_status` vocabulary; engine gate_status | important |
| 11 | Optional aggregate score never hides mismatches | analytics | delivered | engine `no_score: true`; ranking uses levels, not a score | important |
| 12 | Primary use case: solid-material ignition, spread or extinction evidence → ranked investigations, sources, parameters with provenance, comparison, transferable findings, limits | analytics | partial | spread only; ignition and extinction out of scope (DEC-048); one investigation | critical |
| 13 | In-scope Core: discovery and indexing, profiles, document extraction, comparison, ranking, synthesis, uncertainty and transferability, visual exploration | other | partial | document extraction and synthesis not built (SPEC_evidence_synthesis: designed) | critical |
| 14 | Conditional: nonlinear time series, probabilistic models, advanced indicators, uncertainty propagation, CRAM | analytics | not done | DEC-009 later made these MVP targets; GFL_MAP: CRAM not met | important |
| 15 | Out of scope: prediction, control, crew instructions, flight certification | governance | delivered | DEC-010 | important |
| 16 | Principles: unknown is valid, uncertainty visible, reproducible, fail visibly | provenance | delivered | ranking treats unknown as against; ledger; experiment memory keeps failures | critical |
| 17 | Acceptance criteria: traceability, data integrity, classification, physical comparison, ranking, transferability, negative evidence, AI reliability, reproducibility | governance | partial | integrity, traceability, negative evidence and reproducibility met; classification of combustion regimes and physics-based comparison not met; no one-command rebuild (GFL_MAP) | critical |
| 18 | Risk mitigation for "physics engine becomes descriptive" | analytics | partial | the risk materialised: no computed physics module | critical |
| 19 | Decision: first target is solid-material fire safety, subject to data | governance | delivered | DEC-016 | important |
| 20 | Decision: CRAM is a research direction, not validated | governance | superseded | DEC-009 raised CRAM to MVP; DEC-014 sets it as P/D with display | important |
| 21 | Audit SoFIE, BASS, SAFFIRE, FLEX and ACME/BRE for availability, formats, variables, uncertainty and suitability | data | partial | BASS-II full; SAFFIRE at stage 2; the rest at stage 1 | important |

## 4. FiF — Data Audit, preliminary finding 01.md
First data audit: PSI as a dataset repository, preliminary family inventory, decisions 01–03 (BASS-II pilot), the data-object model and BASS-II table quality observations.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Proper ingestion and provenance layer (formats, versions, incomplete records, large downloads) | provenance | delivered | `tools/psi25_fetch.py`, manifests, ledger, re-acquisition 31/31 (RES-003); truncation defect fixed (ISS-048) | critical |
| 2 | Decision 01: BASS-II is the pilot dataset | data | delivered | DEC-016 | critical |
| 3 | Decision 02: SoFIE not assumed | data | delivered | SoFIE "not yet located" (`NASA_FAMILIES_v1.json`) | nice |
| 4 | Decision 03: common metadata and provenance framework, with domain-specific analytical modules per family | data/analytics | partial | common framework exists; only a BASS-II module exists; no module for SAFFIRE, SAME-R or FLEX | important |
| 5 | Inventory: SAFFIRE-I PSI-98 (74 files), SAME-R PSI-101 (342 files, 66 points), FLEX PSI-69 described as "verified evidence" | data | partial (contradicted) | repo: SAFFIRE "not inspected" (stage 2); SAME, SAME-R and FLEX "not yet located" (stage 1) | important |
| 6 | BASS-II table: 130 records | data | superseded | CSV has 129 data rows; ISS-009 open | important |
| 7 | BASS-II: 694 files in v4 | data | superseded | full manifest has 695 files / 255.77 GiB (ISS-008 closed) | nice |
| 8 | Check that the 130 rows are not 130 independent complete experiments | data | delivered | table audit; partial burns B1/B3 (ISS-025); B13 frame mismatch (ISS-051) | important |
| 9 | File-level steps: table schema, metadata ZIP, raw files, units, record↔file mapping, reproduce one published result | data/analytics | delivered | table audit, NEF index, proof-sheet identity (RES-035/036); B6 matches the published ≈2 mm/s (RES-025, AR-001) | critical |
| 10 | Fan and air display are settings, not calibrated velocities | physics | delivered | ISS-013 open, stated on the page; RES-027 | critical |
| 11 | Calibration and uncertainty verified | data | partial | O₂ calibrated vs uncalibrated reconciled (`research/BASSII_O2_COLUMN_RECONCILIATION_2026-11-03.md`); fan calibration workbook and flow speed at the sample unresolved | critical |
| 12 | Data objects Investigation / TestCase / EvidenceAsset with explicit IDs | data | partial | graph node types investigation/experiment/sample/source/measurement; the named objects do not exist | important |
| 13 | Milestone: one experiment, one traceable dataset, one reproducible analysis | analytics | delivered | B6 (AR-001), reproduced byte-identically (RES-006) | critical |
| 14 | Investigate B2 final O₂ 1.6 %, missing final CO₂/CO, B4 CO −1 ppm, unchanged O₂ readings | data | documented only | CSV confirms 1.6 and −1; the table audit lists only B2's blanks; no ISS record or automatic value check for 1.6 % / −1 ppm | important |
| 15 | Keep original values; separate QC layer; no imputation, clipping or overwrite | provenance | partial | raw table sealed and empty vs `none` kept distinct (table audit §5, DEC-004); no QC-layer module or flags file (no "qc" or "anomaly" code) | critical |

## Cross-file findings
- **No computed physics.** There is no code for Re, Pe, Ra, Da, Sc, Le, de Ris, kinetics, transport equations or dimensional-consistency checks. Docs 0.0, 0.1, 0.2, 2 and 3 all name this as the core. Status ranges from "documented only" (`research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md`, `docs/specs/SPEC_regime_gates.md`) to nothing. The transfer engine's gate states are declared by hand, not computed (METHODS §6).
- **CRAM-1/2/3 and Dynamic Dependency Analysis are absent.** No Lyapunov, transfer entropy, mutual information, Pearson/Spearman, surrogate tests, autoregressive models or Mahalanobis. DEC-009 promoted CRAM to an MVP target, but only `SPEC_cram.md` exists. The only CRAM-2-like evidence is the exploratory thickness exponent and the B9/B6 flow independence (RES-038).
- **Anomaly detection is not a module.** It exists only as window-rule gates; the capability map marks it "designed". Doc 4's concrete anomalies (B2 final O₂ 1.6 %, B4 CO −1 ppm) are real in the CSV but are not recorded as issues or flagged by any check.
- **"Physics-based similarity" is really table-field matching inside one investigation.** `rank_comparable_runs.py` covers 7 recorded BASS-II fields against a fixed reference run. The promised 9-dimension framework (pressure, gravity, radiative, instrumentation, scale), the free user scenario and cross-family comparison are not built. GFL_MAP itself rates this "not met".
- **The central demonstration was never built.** Doc 0.2's demo (spacecraft material plus O₂, pressure and ventilation → BASS-II, SoFIE, SAFFIRE, SAME, ACME-BRE with transferability) and doc 0.1's "five experiments analysed rigorously" were replaced by one investigation and four runs. The SAFFIRE cross-case is deferred (DEC-048), and the "fire-safety insight today" question is still open (ISS-043).
- **The challenge's verbs (summarise, rank, interpret NASA findings) are only partly met.** The AI summaries and citation checks cover GFL's own AI-analysis records, not NASA research findings. INDUS gives relevance only, run offline. There is no extraction of conclusions from NASA papers and no synthesis across sources for a user question (GFL_MAP, "evidence-backed synthesis: partly met").
- **Doc 4 conflicts with the repo.** Doc 4 presents SAFFIRE-I (74 files), SAME-R PSI-101 (342 files) and FLEX as "verified evidence from PSI". The repo's family ladder says SAME, SAME-R and FLEX are "not yet located" and SAFFIRE is "not inspected". Doc 4's 130 records and 694 files are superseded by 129 rows (ISS-009 open) and 695 files (ISS-008 closed).
- **The dossier's data-object model was not implemented as named.** Investigation, TestCase and EvidenceAsset (doc 4) and per-experiment profiles (docs 0.2 and 3) do not exist; the graph schema covers this only partly, for the PMMA-100 fixture.
- **What is genuinely delivered and strong:** the provenance and integrity layer (signed ledger, re-acquisition, browser verification), negative evidence and refusal, the separation of evidence states, the B6 measurement reproduced against the literature, blind adversarial AI tests, the maturity labelling, and the removal of all v4 overclaims ("Flight-Grade", control, prediction). These match the DEC-018 minimum but not the analytics that docs 0.0–3 framed as the differentiator.
- **Planned but not delivered:**
  - a comparison of FiF output against a manual analysis (doc 0.2 §7);
  - the AAL "Conflicting Evidence" and "Unknown Scenario" tests (doc 0.1);
  - an explicit claims-verdict register (doc 0.1 §12);
  - the seven canonical documents (doc 0.2 §6, DEC-019).

  None of these were found.
