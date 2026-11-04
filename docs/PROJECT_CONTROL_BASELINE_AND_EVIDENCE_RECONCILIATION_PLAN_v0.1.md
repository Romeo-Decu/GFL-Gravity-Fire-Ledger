# FiF — Project Control Baseline & Evidence Reconciliation Plan v0.1

**Status:** Active working baseline  
**Date:** 2026-11-04  
**Project Manager:** ChatGPT  
**Repository:** https://github.com/Romeo-Decu/FiF  
**Working branch:** `acquisition/pmma100-bass-b3`  
**Default branch:** `main`  
**Authority:** This document records the current project decisions and the next controlled work sequence. It does not replace the scientific evidence acquisition protocol or schemas.

---

## 1. Why this document exists

FiF research has been distributed across multiple conversations. During those conversations, additional discrepancies were discovered, but the findings were not consolidated into one durable, versioned project record quickly enough. This created repetition, context loss, possible duplication of findings, and a risk that an earlier interpretation would be repeated as fact.

This document establishes the first project-control baseline for the evidence-reconciliation phase.

**Operating rule from this point forward: every completed analytical step must produce a saved artifact before the next analytical step begins.** A conversation is not the project record. The repository is the durable project record.

No finding is promoted to fact merely because it appeared in an earlier assistant response. Every finding must have a source, locator, status and review history.

## 2. Project-level decision

The project will not proceed directly from heterogeneous source data to scientific comparison.

The work sequence is now:

1. Inventory experiments, datasets, sources and digital artefacts.
2. Identify which records and files refer to the same experiment, sample, run or measurement.
3. Reconcile representations of the same evidence across independent documents, repositories, files and publications.
4. Reconstruct acquisition, instrumentation, calibration, processing, conversion, storage and publication lineage.
5. Record discrepancies, omissions, ambiguities and confirmed relationships without silently resolving them.
6. Only after reconciliation, create controlled normalized/derived data while preserving all originals.
7. Compare different experiments and assess physical comparability for a declared question.
8. Conduct scientific analysis and evaluate evidence transferability.
9. Audit competitor representations against the same primary-source record.

**Core principle:** first establish what the evidence is and how it came to exist in its current form; only then decide what can be cleaned, compared, calculated or inferred.

## 3. Evidence pairing model

The first unit of work is not a comparison between different experiments. It is a reconciliation of multiple representations of the same evidence.

For each experiment/run/sample, identify and pair, where available:

- experiment or investigation record;
- test/run matrix row and sample identifier;
- primary report and technical publications;
- dataset landing page and repository record;
- original instrument outputs;
- image sequences and original video streams;
- proof sheets, stills, processed video and derived media;
- sensor logs, calibration records and environmental measurements;
- analysis software, scripts, configuration and parameter settings;
- tables, figures, reported results and later reproductions;
- derivative datasets and competitor-platform records.

Pairing is a hypothesis until supported. Similar filenames, shared dates, nominal material/thickness, matching figures or narrative proximity do not independently prove identity.

A single experiment can have multiple distinct data streams. A single source can reproduce another source rather than provide independent confirmation. The evidence graph must represent these distinctions.

## 4. Reconciliation record — minimum fields

Each source assertion and each artefact must be independently addressable.

### 4.1 Source identity
- stable source ID;
- source title/type/author/organization;
- DOI, NASA ID, repository identifier or URL;
- version/revision/publication date;
- access date and licence/access conditions;
- exact locator: page, section, table/row, figure, record, file path or timestamp.

### 4.2 Experiment identity and context
- investigation, campaign, experiment, test/run and sample IDs exactly as reported;
- aliases kept separately, with evidence for the alias relationship;
- date/GMT/time and record granularity;
- material identity, grade, batch, geometry, thickness and sample history;
- gravity/acceleration environment;
- pressure, gas composition, oxygen readings and flow conditions;
- boundary conditions, ignition method and orientation;
- all reported values retain original units and qualifiers.

### 4.3 Instrumentation and acquisition
- instrument/camera/sensor make and model, where stated;
- camera position, orientation, field of view and resolution;
- sensor location, range, response time and sampling frequency;
- calibration method, calibration date and reference;
- synchronization/timebase and timestamp information;
- raw output format, container/codec, bit depth and file structure;
- missing or undocumented instrumentation details explicitly marked unknown.

### 4.4 Processing and lineage
- original source asset and checksum, when exact bytes are available;
- every conversion/transcoding/extraction step;
- software/tool name and version;
- scripts, settings, thresholds, filters and spatial/temporal calibration;
- parent-child relationship between original and derivative files;
- exact transformation inputs/outputs and responsible actor;
- publication figure/table or result generated from the processed asset, where traceable.

### 4.5 Epistemic status
Use explicit distinctions:
- source-reported;
- measured by FiF;
- derived by FiF;
- inferred by FiF;
- unknown;
- conflicting;
- unverified;
- inaccessible.

A source-reported value is not a FiF measurement. An unknown value is not zero. Conflicting values remain separate assertions. A secondary publication is not an independent experiment.

## 5. Initial discrepancy register — PMMA-100 / BASS-II

The following is a starting register reconstructed from the research record available on 2026-11-04. It is not yet the complete audit of every claim made in every earlier conversation. Each item must be rechecked against exact source locators before acceptance into the acquisition package.

| ID | Topic | Current observation | Status / next verification |
|---|---|---|---|
| D-001 | B3 / B03 identity | Appendix/table references B3; NASA figure caption uses B03. | Alias candidate only; prove identity from source records. |
| D-002 | B3 flow | NASA §2.3.6 states 3 cm/s for the 100-µm comparison; Appendix A.1 B3 row reports air display 2 cm/s; Carmignani Appendix A.2 reports B3 2–0 cm/s. | Unresolved; preserve each assertion and its context. |
| D-003 | B3 oxygen | Appendix A.1 reports calibrated 22.2→21.8%; uncalibrated 20.9→20.5%; note suggests probably 20.6% at start. Figure 2.20 caption reports 20.7% O2. | Unresolved; distinguish measurement channel, calibration and summary context. |
| D-004 | B1 vs B3 | Same day/GMT 50, nominal 100-µm film, 2-cm width and flow restrictor 2. B1 air display 5 cm/s and 57 frames; B3 2 cm/s and 253 frames. B1 table explicitly says PMMA; B3 row says “film”. | Candidate within-session comparator, not a validated control. Confirm sample/material and image-stream lineage. |
| D-005 | B3 result linkage | Section 2.3 reports a microgravity maximum of about 2.2 mm/s, but no demonstrated run-level join to B3. | Do not attribute 2.2 mm/s to B3 without explicit linkage. |
| D-006 | Ground result linkage | Section 2.3 reports 2.0 mm/s average for normal-gravity downward 100-µm PMMA. Exact ground run/sample/video linkage is not yet established. | Section-level summary only until run-level source found. |
| D-007 | Material identity | NASA figure identifies NASA PMMA and Astra PMMA for ground samples; exact grade, batch, manufacturing route and history are not identified. | Unknown; seek specimen and material records. |
| D-008 | BASS-II cameras | Nikon D300s top-view stills (reported 4320×2968 px, about 1 frame/s) and Panasonic WV-CP654 side-view video (760×480 px) are distinct streams. | Preserve as separate asset families; establish file/run mappings. |
| D-009 | MP4 provenance | Still-image-derived video is described in NASA report; candidate PSI files include MP4 products. MP4 extension alone does not identify original acquisition stream. | Verify each exact file, metadata and lineage. |
| D-010 | Flame Analyzer / FIAT | NASA report describes MATLAB Flame Analyzer; Carmignani describes FIAT/FIA. Same implementation or parameter lineage has not been established. | Do not conflate tools. Locate code, methods and settings. |
| D-011 | Image threshold | Threshold 70 is illustrated for a 75-µm example; threshold 30 is reported in a separate extinction analysis. Numeric threshold for the target 100-µm comparison is not established. | Unknown until target-specific source found. |
| D-012 | Frame count | B3 253 frames; B1 57 frames. Two camera streams and converted video products exist. | Do not infer frame rate or temporal resolution from counts alone. |
| D-013 | NASA vs Carmignani independence | Carmignani and the NASA report may reproduce or discuss overlapping experimental data. | Treat as documentary cross-references, not independent experimental replication unless proven otherwise. |
| D-014 | MicroFire Atlas | Identified analysis asset is a separate August 2014 BASS-II image/session, one frame, not B3 time-series evidence. | Not a validation of B3 spread rate or NASA Flame Analyzer. |
| D-015 | Dataset counts | PSI record count, NASA test count and PSI file/version counts describe potentially different entities. | Never compare counts until entity types and scope are established. |

### 5.1 Important controls on prior interpretations

The following statements are explicitly not established:

- 2.2 mm/s is not established as the B3 spread rate.
- 253 frames is not an established frame rate or temporal sampling interval.
- B1 is not yet a valid experimental control for B3.
- A file named “Still_Sequence.mp4” is not proven to be top-view stills or original camera footage until inspected.
- NASA Flame Analyzer and Carmignani FIAT are not proven to be the same software.
- Competitor intent to manipulate evidence is not established. We can audit omissions, transformations, labels and unsupported conclusions; intent requires separate evidence.

## 6. Competitor audit — evidence standard

Competitor platforms are evaluated only after the corresponding primary evidence family is reconciled.

For each competitor claim or displayed record, compare:
1. source selected and exact source version;
2. experiment/run/sample identity;
3. original values, units, qualifiers and calibration status;
4. experimental conditions and instrumentation;
5. asset identity and image/video lineage;
6. processing and transformation method;
7. omitted/unknown/conflicting fields;
8. conclusions and whether they exceed the evidence.

Classify findings as:
- faithfully represented;
- transformed with documented method;
- transformed without sufficient provenance;
- omitted;
- mislabeled;
- conflated across records;
- unsupported inference;
- not assessable from available evidence.

Do not allege deliberate manipulation without direct evidence. FiF's competitive advantage is the ability to preserve heterogeneity, reconstruct provenance and expose unsupported equivalence—not to make accusations.

## 7. Work sequence and gates

### Gate 0 — Project baseline
- This document is committed and becomes the working control baseline.
- Earlier findings are not automatically validated; this register is a queue for source re-verification.

### Gate 1 — Evidence inventory
- enumerate experiment/data families and all known sources/assets;
- assign stable IDs;
- identify duplicate/reproduced publications;
- map candidate relationships without asserting them;
- record access state and missing artefacts.

**Exit:** every known record is inventoried or explicitly listed as unresolved.

### Gate 2 — Within-experiment reconciliation
For each experiment/run/sample, reconcile all representations of the same evidence across sources and artefacts. Complete source, experimental context, instrumentation, acquisition, processing and storage records.

**Exit:** a reviewable reconciliation dossier exists for the experiment; conflicts and unknowns are explicit; no unsupported joins remain.

### Gate 3 — Verification
Independently verify source locators, exact transcriptions, file identity, hashes, conversions and proposed joins.

**Exit:** every claim is either verified at the stated level or visibly remains unverified/inaccessible.

### Gate 4 — Controlled normalization
Only after Gates 1–3:
- preserve raw values and files;
- create versioned derived representations;
- record conversion formulas, units, software versions and parameters;
- quantify uncertainty introduced by transformations;
- record why each transformation is necessary and its consequences.

**Exit:** reproducible derived data with complete lineage; originals remain immutable.

### Gate 5 — Cross-experiment comparison
Compare experiments only after their within-experiment evidence dossiers are reconciled. Comparability is question- and outcome-specific. Unknown does not imply compatible. Do not use a universal weighted score.

**Exit:** explicit matching, differing and unknown conditions; justified comparison scope and exclusions.

### Gate 6 — Scientific analysis and transferability
Run physical analysis only on evidence whose provenance and limitations are understood. Separate source conclusions from FiF calculations and inferences. Document uncertainty and validity boundaries.

### Gate 7 — Competitor audit
Apply the same evidence baseline to competitor outputs. Produce claim-to-source comparisons and reproducible discrepancy reports.

## 8. Brick-by-brick documentation rule

This is a mandatory Project Manager operating rule:

1. Before a new analysis, identify the current baseline document and the exact open question.
2. Perform one bounded task.
3. Record sources, locators, method, findings, uncertainty, corrections and next action.
4. Update the relevant register/package/document in the working branch.
5. Run structural and consistency checks where applicable.
6. Report the saved artifact path and commit SHA to the project owner.
7. Only then start the next bounded task.

If a task produces no durable artefact, it is not considered a completed project step.

Do not repeatedly reopen settled questions unless new evidence appears or an explicit audit identifies a prior error. If a conclusion changes, append a correction record and cite the evidence that caused the change. Never silently rewrite project history.

## 9. Immediate next actions

The next task is **Gate 1 — evidence inventory**, not more combustion-model analysis.

1. Create a complete inventory of all known NASA combustion evidence families already in FiF scope (BASS/BASS-II, FLEX/FLEX-2, ACME, BRE, SoFIE, SAFFIRE, SAME and other relevant collections already identified in the baseline research). This is an inventory, not an assumption that all are suitable for the same comparison.
2. For each family, list primary landing pages, reports/publications, data repositories, raw/processed file families, instruments, acquisition/processing methods and known secondary platforms.
3. Mark every field as confirmed, source-reported, candidate, unknown, conflicting or inaccessible.
4. Select one bounded experiment/run as the first complete reconciliation case. BASS-II B3 remains the pilot because the current evidence record already contains specific candidate sources and unresolved joins.
5. Keep B1 as a separate second dossier. Do not merge B1 and B3 or treat B1 as a control before independent reconciliation.
6. Do not populate the acquisition JSON with unsupported links or extracted claims. Do not modify the canonical evidence graph or scientific engine during inventory.

## 10. Current repository state and change boundary

At baseline creation:
- repository is private: `Romeo-Decu/FiF`;
- default branch is `main`;
- current working branch is `acquisition/pmma100-bass-b3`;
- existing acquisition protocol and Claude task brief are present on that branch;
- `PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json` remains an empty staging template;
- no raw B3 assets have been independently acquired or hashed by this workflow;
- no PR is opened by this baseline action;
- no changes are made to `main`, schemas, engine, rulesets, tests or visualization.

The acquisition branch was previously reported as based on main commit `1a62566ccfc34ba2a11124ab63448f6750c611f5`. This baseline does not claim that the branch has been merged or that the acquisition package is complete.

---

**Project Manager decision:** Evidence inventory and within-experiment reconciliation take priority over further scientific modelling. Every subsequent step must be saved as a versioned repository artefact before the next step begins.


## 11. Gate 1 inventory artefact

The initial family-level discovery inventory has been created at:

- `research/NASA_COMBUSTION_EVIDENCE_FAMILY_INVENTORY_v0.1.md`

It records the currently identified BASS, BASS-II, SoFIE, SAFFIRE, SAME, SAME-R, FLEX, FLEX-2, ACME, BRE and SPICE families, plus LUCI as an adjacent competitor-reference item rather than a confirmed NASA family. It distinguishes family-level discovery from investigation-level and file-level verification. Its status is intentionally **initial / incomplete**. The next bounded task is to complete the BASS-II family-level collection and asset inventory, not to begin another physics analysis.


## 12. Decision, issue, idea and implementation register

The durable register is now established at:

- `docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md`

It records accepted architecture and platform decisions, open UI and visualization issues, scientific evidence constraints, proposed product ideas, and the stage at which each item must be implemented or reviewed. It also defines mandatory stage-entry and stage-exit checks.

**UI answer:** visualization architecture and important interaction principles were already recorded in `docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md`. A read-only browser prototype is recorded as implemented. However, a complete user-facing interaction specification (journeys, navigation, screen states, conflict workbench, comparison workspace, responsive/accessibility criteria) has not yet been created. This is now explicitly registered as ISS-001 and must be completed at UI-stage entry. Existing architecture decisions must not be rediscovered or casually reopened.

**New operating rule:** every material problem, solution, decision or idea must be registered with a stable ID, evidence, status, dependencies and implementation/review trigger before the PM moves to the next task. A stage cannot close until all in-scope register entries are verified, resolved, or explicitly deferred with rationale and a future trigger.
