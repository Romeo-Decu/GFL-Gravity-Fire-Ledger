# FiF Scientific & System Architecture v0.1

**Status:** Working architecture baseline  
**Date:** 2026-11-03  
**Repository:** `Romeo-Decu/GFL-Gravity-Fire-Ledger`  
**Branch:** `docs/scientific-system-architecture-v0.1`

## 1. Purpose and design thesis

Flame in Freefall (FiF) is a physics-aware scientific intelligence platform for discovering, organizing, comparing and interpreting evidence from reduced-gravity combustion research, with an initial emphasis on spacecraft fire safety.

FiF must do more than retrieve papers or summarize experiment descriptions. Its central capability is to determine **what evidence is relevant, what evidence is physically comparable, and what conclusions—if any—can be transferred from one experimental context to another**.

The system must never turn semantic similarity into physical equivalence. A shared keyword, material family, or microgravity environment is not sufficient to establish comparability.

### Core rule

> Evidence first. Physics before similarity. Transferability only within declared limits.

FiF is a research-support system. It is not a fire-prediction authority, a spacecraft safety certification system, or an autonomous operational decision-maker.

## 2. Scientific scope and initial evidence families

NASA's Physical Sciences Informatics (PSI) repository provides public data from physical-science investigations conducted in reduced-gravity environments. NASA notes that repository population is not necessarily complete; dataset availability and completeness must therefore be verified per investigation and version.

Initial candidate families:

| Family | Scientific character | Initial FiF treatment |
|---|---|---|
| BASS / BASS-II | Burning and suppression of solid fuels; ignition, flame growth, spread and extinction in low-velocity forced flows | Candidate first validation family for solid-fuel evidence |
| SAFFIRE I–III and later series | Larger-scale spacecraft fire experiments; flame spread, material flammability, smoke/fire characterization, and changing flow/atmosphere conditions | Separate evidence family; do not pool indiscriminately with small-scale tests |
| ACME / BRE | ACME includes independent gaseous-flame investigations; BRE uses gaseous combustion to emulate selected thermal/combustion characteristics of condensed fuels | Separate gaseous-flame / emulation family; BRE is not direct observation of a burning solid sample |

The initial implementation should not assume that these families share a common experimental ontology beyond a small set of general descriptors. Their apparatus, scale, fuel phase, boundary conditions, objectives and observables can differ substantially.

### Source register (initial)

- NASA PSI investigation catalogue: https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
- BASS-II, NASA PSI-25, DOI 10.60555/4qc4-de67: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
- SAFFIRE-I, NASA PSI-98, DOI 10.60555/0t15-1z43: https://psi.nasa.gov/physci/repo/data/investigations/PSI-98
- NASA ACME facility description: https://science.nasa.gov/biological-physical/investigations/acme/
- NASA BRE investigation description: https://science.nasa.gov/biological-physical/investigations/bre/
- NASA SAFFIRE overview: https://www.nasa.gov/wp-content/uploads/2025/07/spacecraft-fire-safety-demonstration-saffire.pdf

These references establish investigation-level context only. They do **not** establish that FiF has downloaded, parsed, quality-checked or independently validated the underlying raw data. That work remains pending.

## 3. Evidence model

FiF should maintain a traceable chain from source to interpretation. Every scientific statement shown to a user must be traceable to one or more source records and, where applicable, to a specific data file, table, figure, time interval or derived calculation.

### 3.1 Core entities

1. **Source** — publication, NASA investigation record, report, dataset landing page or other authoritative source.
2. **Dataset** — a versioned collection of files associated with an investigation or release.
3. **FileAsset** — a specific downloadable file, with checksum, format, size, source URL and retrieval timestamp.
4. **Experiment** — a defined experimental run or test, not merely the overall mission or investigation.
5. **Configuration** — apparatus and boundary-condition state applicable to an experiment.
6. **Sample** — material specimen, fuel, composition, dimensions, orientation and preparation/history.
7. **Measurement** — an observed quantity with value, unit, method, sensor, uncertainty and time/space context.
8. **Claim** — a scientifically meaningful statement supported by cited evidence.
9. **Comparison** — a structured relation between two or more experiments or claims.
10. **Assessment** — a reasoned evaluation of relevance, comparability or transferability, including its limitations.

### 3.2 Minimum experiment descriptor

Each experiment record should capture the following fields when available:

- Identity: investigation, campaign, run/test identifier, date, source references.
- Gravity regime: microgravity / partial gravity / normal gravity / unknown; platform and known residual-acceleration context.
- Combustion mode: solid, liquid, gaseous; premixed/non-premixed where applicable; diffusion/other mechanism when established.
- Fuel/sample: material identity, composition, mass, dimensions, thickness, orientation, surface condition, conditioning and prior exposure.
- Atmosphere: oxidizer composition, oxygen concentration or partial pressure, diluent, total pressure, humidity and measurement basis.
- Flow: forced/natural/mixed, velocity, direction, profile, turbulence descriptor, and measurement or estimation method.
- Geometry: chamber/duct dimensions, confinement, sample placement, distance to boundaries and relevant blockage.
- Ignition: source, location, energy/power where known, duration and initiation protocol.
- Thermal/radiative context: boundary temperatures, radiative environment, heat-loss conditions and relevant properties where available.
- Diagnostics: camera/spectral/imaging setup, thermometry, gas analysis, heat-flux or mass-loss measurement, sampling frequency and calibration.
- Outcomes: ignition success/failure, spread rate, flame dimensions, extinction, heat release, mass consumption, smoke/soot/toxic products and other measured outputs.
- Data quality: missingness, uncertainty, calibration, synchronization, known anomalies and source quality.
- Provenance: exact source, file, page/table/figure/row or time interval supporting each value.

A field must distinguish at least four states: **measured**, **reported but not independently verified**, **derived**, and **unknown**. Do not silently replace unknown values with defaults.

### 3.3 Immutable raw layer

Original source files and original reported values are immutable inputs. FiF may create normalized and derived representations, but must retain:

- original value and unit;
- normalized value and unit, if conversion is valid;
- conversion formula and constants;
- provenance and software/version used;
- quality flags and uncertainty;
- distinction between source-reported, FiF-derived and FiF-inferred content.

No inferred value may overwrite a source value. Corrections create a new version with an audit trail.

## 4. Three distinct analytical questions

FiF must calculate and present these separately.

### A. Retrieval relevance

**Question:** Is this source or experiment potentially relevant to the user's query?

Inputs may include text, metadata, material names, research objectives and scientific concepts. Semantic retrieval is useful here, but it is only a discovery mechanism.

Output: ranked candidate evidence with reasons and source links. Retrieval rank must never be presented as physical comparability.

### B. Physical comparability

**Question:** Are the experiments sufficiently alike in the variables that govern the phenomenon being compared?

Comparability is question-specific. Two experiments may be comparable for one outcome and not another. For example, two tests may support a qualitative comparison of ignition behavior while being unsuitable for a quantitative flame-spread-rate comparison.

The comparison engine should therefore require an explicitly selected **target phenomenon / outcome** and use a phenomenon-specific variable profile.

Potential dimensions include:

- combustion mechanism and fuel phase;
- sample material, composition and geometry;
- oxidizer composition, pressure and humidity;
- gravity regime and residual acceleration;
- flow regime, velocity and direction;
- confinement and apparatus geometry;
- ignition method and location;
- thermal/radiative boundary conditions;
- measurement definition, instrumentation and temporal/spatial resolution.

Classify each dimension as:
- **Compatible** — evidence supports equivalence within a declared tolerance.
- **Different** — known mismatch.
- **Unknown** — insufficient evidence.
- **Not applicable** — not relevant to the selected comparison question.

The system must not treat unknown as compatible.

### C. Evidence transferability

**Question:** To what extent can a finding from experiment A inform a conclusion about experiment B?

Transferability is a reasoned, bounded assessment—not a universal similarity score. It must identify:

1. the source finding and its measured outcome;
2. the target context to which it may be transferred;
3. the governing variables and known differences;
4. the physical rationale for expecting the finding to remain relevant;
5. the assumptions and extrapolation distance;
6. uncertainty and evidence gaps;
7. the permitted conclusion type.

Permitted conclusion types should include:
- **Directly supported** — same relevant conditions and measurement meaning, within declared limits.
- **Conditionally informative** — useful only if stated conditions/assumptions hold.
- **Qualitatively informative** — mechanism or trend may inform interpretation, but quantitative transfer is not justified.
- **Not transferable on current evidence** — a material mismatch or missing critical information prevents a defensible transfer.
- **Undetermined** — available evidence is insufficient to decide.

A numerical score may later summarize a transparent, validated assessment, but it must not replace the explanation or imply physical equivalence. No opaque weighted sum in v0.1.

## 5. Hard gates and uncertainty policy

Some mismatches are potentially disqualifying for a specific comparison. Examples include:

- comparing solid-fuel flame spread directly with a gaseous burner flame without a validated bridging model;
- comparing different measured quantities as if they were the same outcome;
- ignoring a major difference in oxygen concentration, pressure or flow when that variable governs the target phenomenon;
- quantitative transfer across materially different sample geometry or confinement without a justified model;
- claiming a match where a critical variable is unknown.

These are not universal rules that every mismatch invalidates every comparison. They are **question-dependent gates**. The scientific rationale and selected outcome determine which variables are critical.

Uncertainty must be visible and decomposed where possible:
- measurement uncertainty;
- source/reporting uncertainty;
- data-processing uncertainty;
- model/assumption uncertainty;
- between-experiment heterogeneity;
- extrapolation uncertainty.

FiF must be allowed to return “insufficient evidence”. A system that abstains for a defensible reason is behaving correctly.

## 6. Processing and system architecture

Recommended logical pipeline:

1. **Source registry** — authoritative source metadata, DOI/identifier, licence, version and retrieval status.
2. **Ingestion** — controlled download, checksum, file inventory and immutable raw storage.
3. **Extraction** — format-specific parsing (CSV, XLSX, PDF, images/video metadata, structured records).
4. **Normalization** — units, controlled vocabularies, identifiers and explicit missing-value states.
5. **Quality control** — schema checks, range checks, consistency checks and provenance validation; flags never silently delete source data.
6. **Scientific representation** — experiment, configuration, sample, measurement and claim records.
7. **Discovery** — keyword/semantic search over sources and structured metadata.
8. **Comparison engine** — question-specific variable profiles, compatibility matrix and hard gates.
9. **Transferability assessment** — evidence-grounded explanation, bounded conclusion and uncertainty.
10. **User interface** — source-first exploration, side-by-side comparison, evidence trace and explicit caveats.
11. **Audit and evaluation** — reproducible processing runs, versioned rules, test cases and expert review.

### Separation of responsibilities

- Language models may assist with extraction, classification proposals, literature synthesis and explanation.
- Deterministic code must handle unit conversion, schema validation, numerical calculations, thresholds and reproducible comparisons.
- A model-generated field is a proposal until validated against source evidence or an explicit review process.
- Every generated claim must retain citations to the underlying source passages or data.
- The interface must distinguish source facts, computed results and model-generated interpretations.

## 7. MVP definition

The MVP should prove one narrow capability end-to-end rather than promise comprehensive coverage of NASA combustion science.

### Proposed MVP question

**Given two documented solid-fuel combustion experiments, can FiF explain which measured findings are comparable, which are not, and why?**

### Initial scope

- One carefully selected evidence family, provisionally BASS-II.
- A small, manually verified subset of experiment records and source files.
- Structured experiment metadata and provenance.
- One or two target outcomes selected after inspecting actual available data.
- Retrieval relevance, comparison matrix and bounded transferability explanation.
- Explicit unknowns and a reproducible audit trail.

SAFFIRE should be added as a separate family after the BASS-II ingestion and comparison workflow is tested. BRE/ACME should not be merged into the solid-fuel comparison set; a future bridging analysis may be possible, but only with an explicit physical model and validation.

### MVP acceptance criteria

1. Every displayed experimental value links to its source and original unit.
2. Every normalized value records its conversion and software/rule version.
3. Unknown critical variables remain unknown and block unsupported conclusions.
4. The system distinguishes retrieval relevance from physical comparability.
5. The comparison result changes appropriately when a critical boundary condition changes.
6. A reviewer can reproduce the comparison from stored inputs and versioned rules.
7. At least one positive, one negative and one indeterminate comparison are tested.
8. No generated statement is presented as a measured fact without traceable evidence.

## 8. Validation strategy

Validation must be layered:

- **Source validation:** identity, licence, version, completeness and integrity of downloaded files.
- **Extraction validation:** compare parsed values with the original tables/figures or source records.
- **Scientific validation:** domain-expert review of descriptors, critical variables and comparison rules.
- **Computational validation:** unit tests for conversions, missingness, thresholds and deterministic calculations.
- **Behavioral validation:** adversarial cases where semantic similarity is high but physics differs, and cases where terminology differs but physical conditions are comparable.
- **Reproducibility validation:** rerun the same pipeline with the same versions and confirm identical deterministic outputs.

No claim of scientific validation should be made solely because software tests pass.

## 9. Immediate research and engineering sequence

1. Inspect the PSI records and available files for BASS-II (PSI-25), including version metadata and licence.
2. Download a small representative subset; inventory formats, data dictionaries, run identifiers and actual measured variables.
3. Select one target outcome only after verifying that it is present and consistently defined.
4. Build the first experiment schema from observed data, not from an imagined universal schema.
5. Manually annotate a small gold-standard set of experiments and comparisons.
6. Implement deterministic normalization and comparison rules.
7. Test positive, negative and indeterminate cases.
8. Only then add model-assisted extraction and natural-language explanation.

## 10. Known limitations and open questions

- The PSI catalogue itself warns that repository population may be incomplete.
- Investigation-level summaries are not substitutes for run-level data dictionaries and raw measurements.
- Published descriptions may omit variables required for quantitative comparison.
- Different studies may use different operational definitions for nominally similar outcomes.
- Residual acceleration, transient conditions and sensor limitations may be incompletely reported.
- A transferability assessment may require combustion theory or validated numerical models beyond metadata matching.
- The appropriate comparison variables depend on the outcome; there is no single universal comparability vector.

These limitations are design constraints, not defects to hide.

## 11. Decision log

| ID | Decision | Rationale | Status |
|---|---|---|---|
| D-001 | Separate retrieval relevance, physical comparability and evidence transferability | Prevent semantic similarity from being mistaken for physical equivalence | Adopted |
| D-002 | Preserve raw data and source values immutably | Provenance and reproducibility | Adopted |
| D-003 | Treat unknown as a first-class state | Prevent false certainty and fabricated completeness | Adopted |
| D-004 | Use question-specific comparison profiles | Governing variables depend on the outcome | Adopted |
| D-005 | Begin with a narrow BASS-II candidate subset | Solid-fuel focus offers a bounded initial validation problem | Provisional; subject to file inspection |
| D-006 | Keep SAFFIRE and ACME/BRE as distinct evidence families initially | Different scale, apparatus, fuel phase and scientific objectives | Adopted as initial data architecture |

---

**Version note:** v0.1 is a proposed scientific/system architecture. It is not a claim that source files have been ingested, that transferability rules are validated, or that the MVP has been implemented.
