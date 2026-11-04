# FiF — Product, Module & Implementation Traceability Matrix v1.0

**Date:** 2026-11-04  
**Branch:** `acquisition/pmma100-bass-b3`  
**Authority:** Product-scope clarification confirmed by Project Owner on 2026-11-04.  
**Purpose:** Trace the original FiF product plan into implementation, architecture, validation and research documentation. This matrix is a scope baseline, not evidence that listed modules are already implemented.

## 1. Binding scope decision

**FiF MVP = FiF Core + every module originally classified as Extensible.** The Extensible label describes the architecture's modularity and progressive implementation strategy; it does not exclude these capabilities from the MVP target.

The Future Research group is documented as a credible technical/scientific roadmap. Its items may be implemented if time and evidence permit, but remain outside the committed MVP acceptance boundary unless the Project Owner explicitly changes scope.

The seven original product stages remain the strategic lifecycle. The 13 engineering stages and G0–G11 gates in the Master Roadmap remain the execution/control breakdown. The latter must be mapped to, and must not replace, the former.

## 2. Product scope baseline

### 2.1 MVP — committed product target

| ID | Capability | MVP status | Minimum demonstrable outcome | Validation expectation |
|---|---|---|---|---|
| MVP-01 | NASA Data Intelligence | In scope | Discover, ingest and structure relevant NASA combustion evidence with source/version/provenance links | Source completeness, exact transcription, asset integrity and lineage tests |
| MVP-02 | Experiment Comparison | In scope | Compare selected experiments and outcomes with explicit matching, differing and unknown conditions | Reproducible comparison fixtures; no silent joins or normalization |
| MVP-03 | Physics-Based Similarity | In scope | Question- and phenomenon-specific physical comparability assessment | Dimensional/physical rules, domain limits, sensitivity and counterexample tests |
| MVP-04 | Evidence-Backed Synthesis | In scope | Human-readable conclusions linked to evidence, conflicts, uncertainty and limitations | Claim-to-evidence traceability; unsupported-claim and abstention tests |
| MVP-05 | Interactive Dashboard | In scope | Interactive scientific workspace for evidence, comparisons, analysis and limitations | Functional journeys, state coverage, usability and browser tests |
| MVP-06 | FiF Advanced Analytics | In scope | Integrated analytical capability beyond document retrieval and static display; implemented methods must be named and bounded | Numerical verification, reference datasets, uncertainty and reproducibility tests |
| MVP-07 | CRAM-1: Thermodynamic & Transport Analysis | In scope | Modular analysis of thermodynamic state and heat/mass transport, using available measured/derived variables | Equation/unit verification, physical-domain checks, benchmark comparisons |
| MVP-08 | CRAM-2: Combustion Regime Analysis | In scope | Characterization/classification of combustion regimes and transitions within documented validity limits | Regime-definition traceability, labeled/reference cases, false-classification analysis |
| MVP-09 | CRAM-3: Nonlinear Dynamics & Information Analysis | In scope | Time-series and information-dynamics tools selected according to data sufficiency and assumptions | Synthetic/reference tests, stationarity/embedding/surrogate checks where applicable |
| MVP-10 | Probabilistic Anomaly Detection | In scope | Anomaly evidence with calibrated probability/score semantics and explicit uncertainty | Labeled or defensible reference data, calibration and false-positive/negative evaluation |
| MVP-11 | Uncertainty Quantification | In scope | Quantify measurement, extraction, transformation and model uncertainty where supported | Analytical/numerical propagation checks and sensitivity/robustness studies |
| MVP-12 | Advanced Experiment Transferability | In scope | Explain what evidence transfers, to which target context, under what assumptions and limits | Cross-case validation; explicit unknown/conflict handling; no opaque universal score |
| MVP-13 | FiF Research & Control | In scope | Research/analysis workflow and controlled user interaction with analytical processes; no operational spacecraft actuation claim | Workflow, permission, reproducibility and safe-boundary tests |

**Implementation rule:** all 13 capabilities belong to the MVP target. They may be delivered incrementally and at different maturity levels, but each must have a defined minimum outcome, owner/dependency, acceptance criteria and honest maturity label. A placeholder, mock screen or design document is not an implemented capability.

### 2.2 Future research — documented, conditionally implemented

| ID | Research direction | Required documentation before any capability claim | Implementation status |
|---|---|---|---|
| FUT-01 | Validated predictive models | Governing model, assumptions, training/calibration data if applicable, validation domain, benchmark and out-of-domain behaviour | Document/design; implement only if time and validation evidence permit |
| FUT-02 | Multiphysics simulation | Coupled governing equations, coupling strategy, boundary/initial conditions, solver strategy, verification and validation plan | Document/design; implementation conditional |
| FUT-03 | Fire-scenario analysis | Scenario ontology, initiating conditions, geometry/material/system boundaries, uncertainty and scenario validation | Document/design; implementation conditional |
| FUT-04 | Real Model Predictive Control | Dynamic plant model, state/parameter estimation, objective/constraints, optimizer, stability/safety analysis and hardware/software boundary | Document/design; implementation conditional; no real actuator control in MVP |
| FUT-05 | ECLSS decision support | ECLSS interfaces, variables, operational constraints, hazard analysis, decision authority and human-in-the-loop requirements | Document/design; implementation conditional |
| FUT-06 | Sensor and operational-system integration | Sensor/interface inventory, calibration, synchronization, quality flags, cybersecurity, data governance and operational validation | Document/design; implementation conditional |

For every future-research item, documentation must distinguish: (a) established science, (b) FiF design proposal, (c) unverified hypothesis, and (d) implementation dependency. It must state what data and infrastructure are needed, what can be reused from MVP, what remains to be researched, how it could be tested, and what would falsify or block the approach. Documentation is not proof of feasibility or validation.

## 3. CRAM scientific correction

The CRAM names are retained, but the former unsupported “structural convexity of risk” premise is not retained as a scientific measurement claim.

- **CRAM-1 — Thermodynamic & Transport Analysis:** thermodynamic state, properties, gradients and heat/mass transport.
- **CRAM-2 — Combustion Regime Analysis:** combustion regime characterization, transitions, flame spread/ignition/extinction/stability where evidence and model scope support them.
- **CRAM-3 — Nonlinear Dynamics & Information Analysis:** time-dependent nonlinear behaviour and information-theoretic methods, only where data quantity, sampling, stationarity and assumptions justify use.

Method selection is conditional, not a checklist mandate. Transfer Entropy, Lyapunov exponents, surrogate-data tests, mutual information, correlation and autoregressive methods must each have documented assumptions, minimum data requirements, null models and failure/abstention conditions. No method is to be presented as valid merely because it is available in a library.

## 4. Required architecture layers and shared services

The architecture must preserve the following logical flow:

1. **NASA/source acquisition and intelligence:** source registry, retrieval, ingestion, immutable raw capture, asset identity and provenance.
2. **Evidence and data foundation:** canonical evidence graph, experiment/run/sample/result identity, typed quantities, units, calibration state, quality flags, uncertainty and conflict management.
3. **Physics foundation:** physical parameter/property registry, governing equations, dimensional groups, domain-of-validity declarations, assumptions and model/version registry.
4. **Analysis engines:** comparison, physical similarity, CRAM-1/2/3, probabilistic anomaly detection and uncertainty quantification.
5. **Transferability and synthesis:** evidence transfer assessment, claim-to-source synthesis, explanation of limits and explicit abstention.
6. **Research & Control workspace:** human-governed orchestration of analysis, configuration, reproducibility and review; not spacecraft actuation.
7. **Interactive dashboard and interfaces:** human-first exploration and machine-readable interfaces over the same canonical scientific core.
8. **Validation/calibration framework (cross-cutting):** reference cases, numerical verification, experimental validation, benchmark datasets, uncertainty and regression evidence.

The future-research layer may extend these interfaces with predictive models, multiphysics, scenarios, MPC, ECLSS and sensors. MVP architecture must avoid choices that make these extensions needlessly impossible, but must not implement speculative complexity prematurely.

## 5. Maturity and claim vocabulary

Every module and output must be labeled using a consistent maturity scale:

- **M0 — Documented:** concept/specification only.
- **M1 — Prototype:** partial working implementation; not yet accepted.
- **M2 — Functionally verified:** defined software acceptance tests pass.
- **M3 — Numerically verified:** calculations checked against analytical solutions, independent implementations or trusted benchmarks as applicable.
- **M4 — Experimentally validated within stated domain:** compared with suitable experimental evidence and uncertainty.
- **M5 — Operationally qualified:** separately approved operational assurance; not an MVP assumption.

A module may have different maturity by method, dataset or use case. Software tests do not confer M4. A model validated for one regime/material/scale is not automatically validated outside that domain.

## 6. Traceability obligations

Each module must be traceable through:
- product requirement and user/scientific question;
- inputs, data contracts and provenance requirements;
- outputs and their semantics;
- equations/algorithms, assumptions and validity domain;
- upstream/downstream dependencies and interfaces;
- implementation artefacts and exact repository paths;
- unit, contract, integration, numerical and scientific validation tests;
- known limitations, maturity level and open issues;
- demonstration evidence and competition claims.

The detailed implementation backlog must be decomposed from this matrix. This matrix itself does not assert implementation.

## 7. Relationship to the original seven stages

| Original stage | Product/scientific outcome | Engineering roadmap relationship |
|---|---|---|
| 1. Concept & Scientific Scope | FiF Concept & Scientific Foundation v1.0; product boundary and scientific claims | Baseline, scope, requirements and decision-control work |
| 2. NASA Data Audit | NASA Combustion Research Data Catalogue | Source acquisition, inventory, reconciliation and evidence quality |
| 3. Physics & Combustion Framework | FiF Physics & Combustion Framework | Physics registry, equations, CRAM specifications, dimensional analysis and validation foundations |
| 4. System Architecture | FiF Technical Architecture & ADRs | Data contracts, engines, services, interfaces, UI and ADRs |
| 5. MVP Specification | FiF MVP Functional & Technical Specification | Module backlog, dependencies, acceptance criteria, delivery increments |
| 6. Validation & Demonstration | FiF Validation Report & Demonstration Scenario | Software/numerical/scientific validation gates and end-to-end demonstration |
| 7. Competition Package | Honest, reproducible product/demo/documentation/presentation | Release, packaging, evidence and claim audit |

The 13 engineering stages and G0–G11 gates must be mapped to these seven strategic stages in the Master Roadmap. Stage numbers are not interchangeable.

## 8. Scope-control decisions

- **DEC-SCOPE-001:** MVP includes FiF Core and all originally listed Extensible capabilities.
- **DEC-SCOPE-002:** Future Research items are required as technically credible documentation; implementation is conditional on time, dependencies and evidence.
- **DEC-SCOPE-003:** CRAM names retained; scientific foundation corrected as in Section 3.
- **DEC-SCOPE-004:** Seven original product stages are the strategic lifecycle; 13 engineering stages/gates are the execution-control breakdown.
- **DEC-SCOPE-005:** No feature or maturity claim is accepted without implementation evidence and the relevant tests/validation.
- **DEC-SCOPE-006:** Project Owner retains final scope and merge authority.

These decisions supersede any conflicting earlier wording that classifies CRAM, Advanced Analytics, uncertainty quantification, anomaly detection, advanced transferability or Research & Control as outside the MVP target. Earlier text remains historical context, not the active scope baseline.

## 9. Immediate document-control actions

1. Update the Master Roadmap with this scope and a seven-stage ↔ engineering-stage map.
2. Update the Master Test Plan so every MVP module has test/validation coverage and every future-research item has design-review/feasibility criteria.
3. Update source/evidence register to show data requirements and source gaps by MVP module and future research direction.
4. Update decision/issue register with the scope decisions and superseded classification.
5. Keep Stage 1 documentary closure distinct from completion of original Stage 1 product deliverable. The original Concept & Scientific Scope is not declared complete until the required foundation document is reconciled and accepted.
6. Continue Stage 2 / Gate G1 source inventory without losing the source-acquisition work already completed.

---
**Status:** Scope baseline established; module specifications, implementation and scientific validation remain open unless separately evidenced.
