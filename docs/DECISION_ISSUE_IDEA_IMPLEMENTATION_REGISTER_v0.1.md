# FiF — Decision, Issue, Idea & Implementation Register v0.1

**Status:** Active project register  
**Date:** 2026-11-04  
**Owner:** FiF Project Manager  
**Branch:** acquisition/pmma100-bass-b3

## 1. Purpose

This is the durable register for material problems, decisions, solutions, ideas, risks and deferred implementation discovered during FiF work. It prevents rediscovery, context loss, premature implementation and stage closure while known in-scope issues remain unreviewed.

A conversation is not the project record. This register and its linked ADRs/specifications are authoritative.

## 2. Mandatory PM operating rule

Whenever a material issue, decision, solution or idea is identified:
1. Assign a stable ID.
2. Record the problem/opportunity and why it matters.
3. Record the selected decision or proposal; distinguish accepted from proposed.
4. Record evidence/source, confidence and limitations.
5. Assign the stage and precise implementation/review trigger.
6. Record dependencies, owner and acceptance criteria.
7. Link the detailed ADR/specification/issue.
8. Update this register before moving to another analytical task.

At stage entry, review all entries triggered by that stage. At stage exit, every applicable entry must be implemented and verified, resolved with evidence, explicitly accepted as a limitation with rationale and risk owner, or formally deferred with a named future trigger. A decision may be accepted while implementation remains open; never conflate those statuses.

## 3. Status vocabulary

Decision: accepted / proposed / rejected / superseded.  
Work: open / in_progress / blocked / verified / deferred / closed.  
Evidence states (unknown, inaccessible, conflicting, unverified) are separate from work status.

## 4. Register

| ID | Type | Problem / decision / idea | Current treatment | Implementation / review trigger | Status | Authoritative record |
|---|---|---|---|---|---|---|
| DEC-001 | Architecture | Graph layout, graph interaction and scientific plotting are different responsibilities. | Accepted: elkjs for layout, Cytoscape.js for interactive evidence graph, Plotly for scientific charts; canonical JSON is renderer-independent. | Visualization implementation and renderer changes. | Decision accepted; prototype partly implemented. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| DEC-002 | Platform | Need cross-platform access without coupling science services to desktop packaging. | Accepted: responsive browser-first application; desktop wrapper deferred until offline/local-instrument/institutional need is demonstrated. | UI implementation; reconsider only with documented user need. | Decision accepted; interaction specification incomplete. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| DEC-003 | Scientific UI | Semantic similarity or visual proximity must not imply physical equivalence. | Accepted: typed relations, provenance and evidence states; graph layout cannot imply equivalence. | All graph views, filters, exports and assessment screens. | Accepted; prototype coverage to verify. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md; docs/CANONICAL_EVIDENCE_GRAPH_CONTRACT_v0.1.md |
| DEC-004 | Data governance | Raw evidence must not be overwritten by normalized or derived data. | Accepted: immutable raw layer; versioned derivatives retain parent, method, parameters and provenance. | Acquisition, ingestion, normalization and export. | Accepted; enforcement coverage to verify. | docs/SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md; docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md |
| DEC-005 | Workflow | Analysis without durable records causes context loss and repeated loops. | Accepted: each bounded task produces a saved artefact; corrections preserve history; stage gates review the register. | Immediately; all stages. | Active operating rule. | This register; project control baseline. |
| DEC-006 | Evidence method | Multiple sources/files may represent the same experiment but are not automatically identical or independent. | Accepted: reconcile within each experiment first; candidate joins remain explicit; cross-experiment comparison follows reconciliation. | Evidence inventory and reconciliation, before normalization/scientific comparison. | Active; inventory incomplete. | docs/PROJECT_CONTROL_BASELINE_AND_EVIDENCE_RECONCILIATION_PLAN_v0.1.md |
| DEC-007 | Competitor audit | Competitor outputs may omit context, conflate records or overstate comparability. | Audit source selection, transformations, omissions, labels and claims. Do not infer intent without evidence. | After corresponding primary evidence family is reconciled. | Deferred. | docs/PROJECT_CONTROL_BASELINE_AND_EVIDENCE_RECONCILIATION_PLAN_v0.1.md |
| ISS-001 | UI | ADR-001 captures architecture and prototype criteria, but not a complete user-facing interaction specification. Without recording this, UI decisions may be rediscovered from zero. | Treat ADR-001 as binding architecture. Create a concise UI interaction specification before substantial UI expansion: user journeys, navigation, evidence detail, filters, comparison workspace, uncertainty/conflict presentation, responsive behavior and accessibility. Do not re-decide library choices absent new evidence. | Before next substantial UI implementation; mandatory at UI-stage entry. | Open; not a blocker for current evidence inventory. | ADR-001; UI specification to be created. |
| ISS-002 | Visualization | Exact ELK edge-section routing is not transferred into Cytoscape edge geometry. | Keep prototype status explicit; validate routing fidelity before calling graph geometry final. | Graph-view refinement/UI validation. | Open. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| ISS-003 | Accessibility | Accessibility beyond semantic labels and responsive behavior remain open. | UI acceptance must cover keyboard, screen-reader, non-colour evidence encoding, contrast, focus and touch/small-screen behavior. | Before UI milestone closure. | Open. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| ISS-004 | Performance | Large evidence graphs may require progressive loading and performance validation. | Define representative graph sizes and latency budgets before optimization decisions. | Before production-scale graph release. | Open; not current inventory blocker. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| ISS-005 | Licensing | ELK declares EPL-2.0 OR GPL-3.0-or-later; intended licence treatment and notices require review. | Preserve upstream notices; confirm distribution treatment before release. | Before external distribution/packaging. | Open. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| ISS-006 | Scientific visualization | Means, maxima and unlike statistics can be visually misrepresented as comparable. | Every chart exposes statistic type, unit, source, uncertainty and linkage status; abstain where comparison is unsupported. | Every chart implementation/review. | Active requirement; tests to verify. | docs/ADR_001_VISUALIZATION_ARCHITECTURE_v0.1.md |
| ISS-007 | Evidence lineage | Source-to-file/run/sample joins can be inferred from filenames or proximity. | Joins remain candidates until supported by exact source evidence. | Evidence inventory and all ingestion/reconciliation. | Active. | docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md |
| ISS-008 | BASS-II collection file manifest | PSI-25 root exposes 9 folder names, but nested current folder/file paths and metadata remain unavailable. The Experimental Table CSV has now been obtained separately. | Enumerate nested folders/files with exact paths and available metadata; do not infer current file count from version-history deltas. NASA's browser-mediated selective download is the supported current route; the public AWS PSI bucket is not verified as a BASS-II mirror. | Gate 1 BASS-II collection inventory; before B3 asset reconciliation. | Open; blocks collection-inventory closure. | research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md |

| ISS-009 | Table integrity | PSI page reports 130 Experimental Table records, but the supplied CSV contains 129 data records (130 physical lines including header). | Preserve both counts; do not assume page count includes header or CSV export omits a row. Reconcile against authoritative export/page behavior. | Before Gate 1 closure and before using the table as complete dataset inventory. | Open. | research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md |
| ISS-010 | Duplicate tracking entry | The nested PSI-25 file-tree retrieval is already tracked by ISS-008; this entry duplicates the same scope and closure condition. | Superseded by ISS-008. Preserve this ID and history; do not track the same manifest task twice. | Closed as duplicate on 2026-11-04; any new distinct file-manifest issue receives a new ID. | Closed (administrative; no evidence task closed). | research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md |
| ISS-011 | B3 material identity | B3 material cell says `100 micron film 2 cm wide`, omitting PMMA, unlike B1. | Preserve literal wording; PMMA attribution requires an explicit source-to-sample linkage from another authoritative source. | B3 evidence reconciliation; before any scientific comparison. | Open. | research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md |
| IDEA-001 | Product | A researcher-friendly evidence view and an advanced provenance graph should share one scientific truth. | Proposed: both consume the same canonical evidence model; validate simple task-oriented and advanced graph workflows. | UI specification stage; validate with target researcher tasks. | Proposed. | UI interaction specification to be created. |
| IDEA-002 | Product | Conflicts and missing metadata should be explorable, not hidden during cleanup. | Proposed discrepancy/conflict workbench filtered by experiment, source, parameter, evidence state and resolution status. | Evidence-management UI stage, after reconciliation record stabilizes. | Proposed. | Evidence-management UI design to be created. |
| IDEA-003 | Product | Users need to see an asset's lineage from capture through conversion, processing, publication and reuse. | Proposed provenance timeline with parent/child asset edges and transformation records. | Asset-ingestion/provenance UI stage. | Proposed. | Asset-lineage design to be created. |

## 5. UI decisions already made — do not rediscover

ADR-001 is the current architecture authority. These decisions are already recorded:
1. Browser-first responsive, platform-independent application shell.
2. Core scientific services and canonical data contracts remain frontend-independent.
3. ELK/elkjs performs graph layout, not rendering.
4. Cytoscape.js renders and supports interaction with evidence networks.
5. Plotly handles scientific charts, not graph networks.
6. Renderer is not the authoritative scientific database.
7. Visual links use stable FiF IDs and source locators.
8. Selecting a claim/measurement exposes source, units, transformation history and uncertainty.
9. Unknown, inferred, measured and source-reported evidence are visibly distinguished.
10. Filters must not silently hide contradictions or unknowns from audit views.
11. Desktop packaging is deferred until a demonstrated need exists.
12. GLSP is not adopted for the initial read/explore experience.

Not yet fully specified and therefore open for the UI stage:
- primary user roles and highest-priority tasks;
- information architecture and navigation;
- exact screen layouts and interaction states;
- experiment overview and evidence detail;
- discrepancy/conflict workbench;
- comparison workspace and explanation of non-comparability;
- search, filtering, saved views and export interactions;
- responsive breakpoints, keyboard and screen-reader behavior;
- user validation and usability acceptance criteria.

## 6. Stage-entry and stage-exit checklist

At stage entry, the PM reads the control baseline, this register, all entries triggered by the stage, linked ADRs/specifications and previous implementation status. Unresolved dependencies are carried forward into bounded tasks with acceptance criteria.

A stage is complete only when:
1. planned deliverables pass acceptance criteria;
2. every register entry triggered by that stage is verified/closed, or explicitly deferred with rationale, owner and trigger;
3. no unresolved blocker or hidden dependency remains;
4. tests/checks and review evidence are recorded;
5. stage report and artefacts are committed;
6. next-stage baseline identifies exactly what is complete and what remains.

Deferred means explicitly parked, not forgotten. Its trigger must be revisited when that stage begins.

## 7. Change control

New decisions receive new IDs; do not overwrite history. A changed decision records evidence, rationale and affected documents/code. Implementation is not inferred from a design decision. Closed issues require verification or closure rationale. If new evidence affects an earlier stage, reopen that gate.

## 8. Immediate PM actions

1. Keep ADR-001 as the visualization architecture authority.
2. Do not claim the whole UI is complete: architecture and a read-only prototype exist; interaction specification is still missing.
3. At UI-stage entry, create the missing interaction specification using this register and ADR-001, not a fresh debate.
4. Continue evidence inventory without reopening accepted visualization architecture.
5. Before closing inventory/reconciliation, review all relevant evidence, provenance, schema and dependency issues.

**PM rule:** no material decision, problem, solution or idea exists only in chat. Record it, link the detailed artefact, assign its implementation trigger, and revisit it at the appropriate stage gate.


### ISS-008 — retrieval subtask update (2026-11-04)

- **Confirmed:** PSI-25 Version 4 experimental table contains 130 records and 17 displayed columns; only the first 5 are currently transcribed.
- **Confirmed:** the page exposes 9 root folder names; nested file tree and exact paths remain unknown.
- **Retrieval limitation:** browser-indexed extraction returns only the first five rows; direct page opening and page-query variants did not expose subsequent pages through the current tool route. This does not prove that the data are unavailable from NASA.
- **NASA-supported narrow route:** the PSI tutorial specifies the Experimental Table as a `.csv` deliverable. If the browser data request cannot be recovered, obtain only the CSV under the `Experimental table` folder; do not request the Raw Data archive or full investigation ZIP.
- **Next attempt:** inspect the PSI page's browser data requests or use the narrow CSV export; avoid whole-collection downloads.
- **Closure criteria unchanged:** full table captured; current folder/file tree enumerated with exact paths and available metadata; B1/B3 candidate assets verified against exact paths.


### ISS-008 / ISS-009 / ISS-010 / ISS-011 update — 2026-11-04

- Experimental Table CSV received: 129 data rows, 17 columns; source SHA-256 and detailed cell-level audit recorded in `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md`.
- ISS-008 is now limited to the unresolved nested file manifest; the CSV acquisition subtask is complete.
- ISS-009 tracks the page-vs-CSV record-count discrepancy (130 vs 129). No explanation has been assumed.
- ISS-010 tracks nested PSI file-tree retrieval.
- ISS-011 tracks B3 material identity wording; B3's own CSV cell does not explicitly state PMMA.


### ISS-008 / ISS-009 / ISS-010 retrieval review — 2026-11-04

- **ISS-008 remains open.** Fresh indexed PSI-25 extraction confirms the page's `1–5 of 130` count, B3's exact table wording, and the nine root folder names; nested file paths and file metadata remain unavailable through the current browser retrieval route.
- NASA's documented download process supports selecting only required files/folders in the PSI browser. Requests above 1 GB are prepared for email delivery in multiple parts; NASA recommends smaller, targeted requests. The full investigation archive is not required for the next B1/B3 acquisition step.
- The AWS Registry of Open Data entry for the `nasa-psi` bucket describes the resource as DSI and OASIS data; it does not verify the bucket as a BASS-II / PSI-25 mirror. Do not use it as evidence that BASS-II files are absent.
- **ISS-009 remains open.** The official page again reports 130 records while the supplied CSV contains 129 data records. No source-supported explanation has been found.
- **ISS-010 is closed administratively as a duplicate of ISS-008.** No file-tree retrieval work is considered completed by closing this duplicate tracking entry.
- B3's page and CSV wording still omits PMMA. The separate NASA Figure 2.20 caption remains a candidate cross-source linkage, not a reason to alter the source transcription.

Source details and citations are recorded in `research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md`.

### ISS-008 — retrieval-path review (2026-11-04)

- A bounded public-source review did not identify a documented endpoint for enumerating the nested PSI-25 BASS-II file tree.
- NASA's PSI guide confirms browser-based folder expansion and selective download. NASA's large-download guidance confirms multipart email delivery for selected requests above 1 GB.
- NASA's public API catalogue documents an OSDR API, but no verified mapping to the PSI-25 file browser or BASS-II manifest was found. Do not treat OSDR API routes as PSI-25 file endpoints without evidence.
- Exact public searches for the four user-reported B3 filenames returned no indexed matches. This is not evidence of absence from the live PSI tree.
- **Status unchanged: Open.** No nested file paths, byte sizes, current version membership or B3 asset joins have been verified.
- **Next action:** inspect the PSI-25 Raw Data folder directly in the browser and capture the exact displayed hierarchy; then inspect only the minimum related metadata/document folders. Do not request the full investigation archive.


## 9. BASS-II B6 evidence reconciliation — 2026-11-04

| ID | Type | Problem / decision | Current treatment | Trigger | Status | Authoritative record |
|---|---|---|---|---|---|---|
| ISS-012 | Data quality / transcription | Secondary MicroFire Atlas B6 record presents 20.1 → 20.0 vol% as O₂ without preserving NASA's calibrated vs uncalibrated column distinction. NASA Table A.1 reports calibrated 21.0 → 20.9 and uncalibrated 20.1 → 20.0. | Use NASA calibrated columns for calibrated O₂; retain uncalibrated values as separate fields. Audit all 22 Bhattacharjee rows and then assess whether the mapping issue recurs elsewhere. Do not generalize from B6 alone. | Before importing secondary BASS-II datasets or closing data-quality review. | Open; B6 discrepancy verified, collection-wide audit pending. | research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md; data/derived/BASSII_B6_SOURCE_VALUES_v0.1.csv |
| ISS-013 | Physical parameter reconciliation | NASA B6 Fan/Air display sequences, Carmignani's initial-to-final flow values (1→7 cm/s) and Figure 5.8 anemometer trace are different representations whose exact mapping is unknown. | Carmignani Table A.2 explicitly defines flow entries as initial and final values; do not call 1–7 a range. Preserve source-specific representations. Resolve via calibration workbook, graph axes, anemometer response, voice confirmations and video timeline. | Before any B6 flow-dependent calculation or comparison. | Open. | research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md |
| ISS-014 | Derived data / reproducibility | Carmignani Figure 5.8 contains B6 derived flame/radiometer/flow information, but only approximate values have been extracted so far. | Digitize each series independently with axis calibration, point-level uncertainty and exact source image locator. Keep digitized series separate from raw measurements. | Before B6 video-derived metrics are compared with published results. | Open. | research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md |
| ISS-015 | Additional dataset acquisition | NASA PSI-62 describes a 2025 data release with two-color tomography of BASS/BASS-II imagery, but its ZIP contents and B6 coverage are unknown. | Retrieve and inventory the PSI-62 ZIP; establish experiment/run membership before using any data. | Next source-acquisition pass. | Open. | research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md |

### B6 evidence artefacts committed

- `research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md`
- `research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md`
- `research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md`
- `data/derived/BASSII_B6_SOURCE_VALUES_v0.1.csv`

**Interpretation rule:** NASA Table A.1 is the primary source for the test-level B6 record. Carmignani (2019) is a scientific secondary source for analysis and derived quantities. Approximate graph/discussion readings are not raw measurements. The PSI-62 landing-page description is not proof that its archive contains B6.


| ISS-016 | Source identity / terminology | Carmignani dissertation calls its appendix and figures “BASS” and does not expose NASA GMT188 or sample153m in the cited B6 table. Its B6/0.1-mm/20-mm/21%-O₂ conditions strongly match NASA BASS-II B6, but the exact join is not explicitly keyed by sample/GMT in the dissertation. | Preserve source nomenclature. Keep the BASS dissertation ↔ NASA BASS-II B6 link as a strongly supported cross-source match pending direct stream/metadata verification; do not silently relabel the dissertation. | Before claiming full B6 source identity closure or publishing a combined synchronized time series. | Open; high-confidence candidate join. | research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md; research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md |

### Additional dissertation extraction — 2026-11-04

- Carmignani Appendix A, Table A.2 note explicitly states flow values are **initial and final values**. B6 `1–7 cm/s` is initial-to-final, not a min–max range.
- FIAT processing is described: RGB→YCrCb intensity tracking with vertical luminance averaging and threshold-based leading/trailing edge detection; RGB-channel min/max thresholds for blue/yellow area tracking.
- The dissertation provides an image-measurement error model dependent on pixel/mm resolution, frame rate and observation interval.
- Figure 5.8 uses first-frame-per-second radiometer readings from side video; FIAT top-view analysis provides flame geometry/area; anemometer response is about one minute; flow steps are aligned using astronaut voice confirmations.
- Exact FIAT thresholds, software revision, calibration and timebase mapping remain open.
- The dissertation's source terminology is “BASS”; the link to NASA BASS-II B6 is strong but remains a candidate join pending direct media/metadata verification.

Updated detail: `research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md`.


## 9. Stage 1 closure — Master Project Map & Completion Roadmap (2026-11-04)

**Milestone:** MILESTONE-001 — Project baseline and completion roadmap  
**Status:** Closed as a documentary/control milestone. This does not close scientific or data gates.

Authoritative Stage 1 artefacts:
- `docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md`
- `research/SOURCE_ACQUISITION_AND_EVIDENCE_GAP_REGISTER_v1.0.md`
- `docs/TEST_AND_VALIDATION_MASTER_PLAN_v1.0.md`

The Stage 1 audit classified the existing repository implementation, schemas, ruleset, canonical graph fixture, CLI, tests, CI evidence, read-only visualization prototype and scientific documentation. It distinguishes the B3 primary transferability case from B6's role as a detailed reconstruction/method-validation case.

The source register records which sources have already been reviewed, which are metadata-only, which are user-held but not yet inspected by FiF, and which remain unidentified or inaccessible. The master test plan separates software verification from data integrity, measurement reconstruction, scientific validation, usability, security and release testing.

**Stage 1 exit evidence:**
1. Current main and working-branch SHAs recorded.
2. Repository tree reviewed.
3. Implementation claims separated from designed or unimplemented capabilities.
4. Existing CI runs PR #3 / 41769248025 and PR #4 / 41770394680 verified as successful for their tested commits.
5. Source acquisition backlog and dependencies recorded.
6. End-to-end work packages and acceptance gates documented.
7. README points to the authoritative roadmap and supporting registers.

**Next mandatory stage:** Stage 2 / Gate G1 — source acquisition and inventory closure. Begin with PSI-25 manifest and 130-vs-129 table discrepancy, then exact B3/B6 media verification, Fan calibration workbook dependency and PSI-62 archive inspection. Do not repeat general FiF architecture or literature discovery.

### MILESTONE-001 completion boundary

Closed:
- project map;
- implementation baseline;
- source register;
- full staged roadmap;
- test and validation plan.

Still open:
- ISS-001 through ISS-009 and ISS-011 through ISS-016 as applicable;
- all scientific acquisition, reconstruction, physical validation, transferability and production release gates listed in the master roadmap.

No direct changes to main. No merge authorized by this milestone.


| DEC-008 | Scientific case sequencing | The original PMMA-100 transferability case is B3/B03, while B6 has richer test-level metadata and thesis-derived measurements. Treating them as one case would blur the scientific objective. | Accepted PM decision: retain B3/B03 as the primary transferability case; use B6 as a separate detailed reconstruction / method-validation case; keep B1 as a candidate comparator, not a validated control. B6 does not replace B3 unless a later evidence-based decision explicitly changes scope. | All source acquisition, measurement and scientific analysis for the PMMA-100 workstream. | Decision accepted; B3/B6 evidence work remains open. | docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md; research/FIRST_PHYSICS_CASE_SELECTION_v0.1.md; B6 source dossier. |
| ISS-017 | CI branch coverage | The current workflow runs on pushes to main and selected historical feature branches, but not on pushes to acquisition/pmma100-bass-b3. Pull requests targeting main do trigger CI. | Before further code changes on the acquisition branch, either add the active branch to push triggers or rely on a mandatory PR check before merge; record the chosen enforcement. Current GitHub Free/manual review process remains the merge control. | Before the next code-bearing commit or before opening the next PR. | Open; no current scientific blocker. | .github/workflows/tests.yml; docs/TEST_AND_VALIDATION_MASTER_PLAN_v1.0.md |


## 17. Product-scope decisions — 2026-11-04

The following decisions are accepted by the Project Owner and are active. They are fully specified in `docs/FIF_PRODUCT_MODULE_TRACEABILITY_MATRIX_v1.0.md`.

| ID | Decision | Consequence | Status |
|---|---|---|---|
| DEC-009 | MVP comprises FiF Core plus all originally listed Extensible capabilities | CRAM-1/2/3, probabilistic anomaly detection, uncertainty quantification, advanced transferability and FiF Research & Control are MVP implementation targets, not post-MVP exclusions | Accepted |
| DEC-010 | Future Research items are documented as technically credible roadmaps; implementation is conditional on time, dependencies and evidence | Predictive models, multiphysics, fire scenarios, real MPC, ECLSS decision support and sensor/operational integration are not promised MVP capabilities | Accepted |
| DEC-011 | Retain CRAM names but replace unsupported structural-convexity-of-risk premise | CRAM-1 = Thermodynamic & Transport; CRAM-2 = Combustion Regime; CRAM-3 = Nonlinear Dynamics & Information | Accepted |
| DEC-012 | Original seven strategic stages remain the product lifecycle; 13 engineering stages/G0–G11 are execution controls | All engineering stages and gates must map to the seven original stages; no substitution of one structure for the other | Accepted |
| DEC-013 | A capability is not complete by documentation, placeholder or UI mock-up alone | Implementation, tests, validation and maturity must be separately evidenced | Accepted |

### Supersession note

Earlier roadmap language placing CRAM/nonlinear dynamics/Transfer Entropy and related analysis outside Release A/MVP is superseded by DEC-009. Historical entries are retained for auditability; they are not the active scope decision. No source-acquisition, scientific-validation or software-implementation issue is closed by these scope decisions.


## 18. Release A execution decisions and evidence updates — 2026-11-04

Accepted by the Project Owner on 2026-11-04. Full text: `docs/RELEASE_A_SCOPE_AND_ACCEPTANCE_v1.0.md`.

| ID | Decision / issue | Consequence | Status |
|---|---|---|---|
| DEC-014 | Release A ships all matrix modules with displayed maturity V / P / D | DEC-009 remains the long-term target; Release A presents no module above its evidenced level | Accepted |
| DEC-015 | Owner approves merges; Claude implements on branches via PR; ChatGPT reviews | Replaces the read-only HOLD role for Claude for the Release A workstream | Accepted |
| DEC-016 | Scientific anchor = BASS-II 100-µm / 20-mm PMMA family (B1, B3, B6, B9, B15, B16, B19, B20); B6 = method validation | Refines DEC-008: B3 stays in the family; B3 ↔ Section 2.3 join leaves the critical path | Accepted |
| DEC-018 | Minimum success condition = integrity and deviation layer (tamper-evident provenance, deviation register, explicit non-comparability refusal); measurement and transfer are stretch evidence | Founding principle of the Project Owner; see Release A scope §2 | Accepted |
| DEC-017 | Primary measurement source = top-view still sequence; side-view video for overlay values | Follows the BASS imaging layout documented in Carmignani (2019) and the PSI-25 Ops procedure | Accepted |
| ISS-008 | PSI-25 nested file manifest | **Closed.** Full manifest retrieved through the endpoint used by the public PSI page: 695 files, 274,631,106,141 bytes = 255.77 GiB, matching the page. `data/manifests/PSI-25_v4_manifest.json`; reproducible with `tools/psi25_fetch.py manifest`. | Closed |
| ISS-013 | Mapping of B6 Fan/Air sequences, thesis 1→7 cm/s and anemometer trace | **Path established, not yet resolved.** The B6 side-view stream carries a per-frame overlay `FUEL / AIR / FAN / RAD` with a 1-s clock; observed AIR values over the test include 4, 3, 4, 5, 7 (final 7 matches Carmignani's final value). Per-frame extraction pending (WP2). | Open |
| ISS-018 | Overlay / proof-sheet date one day after the NASA table date | B6 overlay shows 07/08/14 and the proof sheet "GMT 189 / 07-08-2014 (Date/Time set to BASS Video Display)", while the CSV gives 7/7/2014 GMT 188. The PSI-25 Ops document states the MSG Video Monitor date is "highly possible … one day off". Treat as a documented display artefact; keep NASA table date authoritative; preserve both. | Explained by source |
| ISS-019 | PSI file labelled TESTB15 with sample 175 / GMT183 | The table assigns sample 175m to B17 (GMT183); B15 is sample 149m / GMT188, for which a separate correctly named file set exists. The `…SAMPLE_175_TESTB15…` set is a candidate mislabel of B17. Flagged in `data/derived/BASSII_100UM_FAMILY_ASSETS_v0.1.csv`; excluded from B15 analysis; not renamed. | Open |
| ISS-020 | Spatial scale for B6 stills | Post-burn stills iss040e045733–738 show the illuminated holder (frame and a row of marks) in the fixed still-camera field; the Ops document references a "deployed scale". Calibrate on full-resolution originals (archive iss040e045728.zip, ~879 MB, member range to verify). | Open — WP2 |
| DEC-019 | Documentation rebuild (WP5, 10–12 Nov): consolidate into 7 canonical documents mapped to the 7 strategic stages; paragraph-by-paragraph claim check; superseded documents archived, not deleted; no new documents before 9 Nov | Prevents rewriting twice before results are stable | Accepted |
| DEC-020 | Product name **Gravity Fire Ledger**; tagline **"Mapping evidence for fire where gravity ends."**; short form **GFL**; logo = interlaced-ribbon mark (Project Owner's proposal 2), **provisional**: supplied SVG embeds a raster; vector redraw or replacement to be decided after WP5 | FiF / Flame in Freefall stays as the challenge and project reference. Brand avoids regulatory or authority claims (no "standard", "compliance", "codex"). Logo follow-ups: reduce the play-button reading of the centre triangle; add a flat monochrome variant for small sizes and light backgrounds | Accepted |
| ISS-009 | Page count 130 vs CSV 129 rows | Unchanged. Independent re-download through `tools/psi25_fetch.py` reproduces SHA-256 71e792bf…c042, 16,590 bytes, 129 data rows. | Open |

### B6 first FiF/GFL measurement — 2026-11-04

| ID | Item | Status |
|---|---|---|
| RES-001 | B6 opposed-flow spread rate measured from the 77 original NEF stills: **2.27 ± 0.09 mm/s** (fit 0.012, threshold sensitivity 0.063, scale 0.068). Timing from EXIF sub-second stamps. `tools/flame_front.py`; `data/derived/B6_SPREAD_RATE_RESULT_v0.1.json`; comparison in `data/derived/B6_COMPARISON_v0.1.json` | Measured, provisional (scale plane, ISS-020) |
| ISS-013 | Overlay AIR/FAN/RAD transcribed at 3-s steps (`data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv`): AIR 4 → 3 (≈7–31 s) → 4 → 5 → 6 → 7 after burnout; FAN 46 → 61 | Path implemented; automated OCR pending |
| ISS-020 | Ruler ("deployed scale") in illuminated post-burn stills: label period 294 px, minor tick ≈ 29.4 px at full resolution → 29.4 px/mm at the ruler plane (14.7 half-size). Ruler is defocused, so it likely lies off the sample plane; ±3 % carried as scale uncertainty | Open — plane correction |
| ISS-021 | 22–30 s window gives 2.61 mm/s vs 2.1–2.4 elsewhere; coincides with a bracketed frame of different exposure (t = 26.57 s, 1/60 s) | Candidate processing artefact; anomaly-prototype test case |
| ISS-022 | Still-camera clock offset, session GMT50 (B1, B3) | Every B1/B3 proof-sheet caption states "Date/Time is minus 1 day 6 min 10 sec from BASS Video Clock"; GMT183/188 captions state "Date/Time set to BASS Video Display". Without the correction, overlay flow values would be paired with stills ≈ 6 min off. Apply −1 d 6 min 10 s → video clock for GMT50 only; keep both clocks in records | Explained by source; must be applied |
| ISS-023 | Camera framing differs between sessions | B1 (GMT50) stills show a different field of view / magnification than B6 (GMT188); spatial scale must be established per session from that session's illuminated frames, never reused across sessions | Open — per-session scale |
| ISS-024 | Table "Total Frames Shot" vs archived NEF stills | B1 57/54, **B3 253/43**, B6 80/77, B9 45/51, **B15 122/74**, B16 94/101, B19 95/101, B20 111/115 (table / PSI NEF archive). Small differences may be counting conventions; B3 and B15 are large gaps — stills may be missing from PSI or the table counts something else. Do not infer which | Open |
| ISS-025 | Candidate partial burns B1 and B3 | Illuminated post-burn stills of B1 and B3 show unburned film with a curved burnt edge inside the holder, unlike B6 (complete burnout recorded). B3 has only 4 flame-bearing stills near the igniter. If confirmed, B3 cannot be the source of a steady-spread value; this bears directly on DEC-008 / R03 (2.2 mm/s not attributable to B3). Visual observation only — to be confirmed with video and crew notes | Open — high priority |
| ISS-026 | The 100-µm family is not homogeneous in burning behaviour | Stills show bright yellow flames (B1, B6, B9 early), dim/blue near-limit flames at 17 % O₂ (B16, B19, B20, long exposures) and a high-flow distorted flame in B15. Runs must be classified by regime before any pooled relation is fitted (CRAM-2 input) | Open — WP3 design input |
| DEC-021 | Competition entry: Universal (virtual) event, official Flame in Freefall challenge, compliance tracked in `docs/SPACE_APPS_2026_COMPLIANCE_CHECKLIST.md` | Avoid disqualification; items 6 (open licence / public materials) and 11 require owner decisions | Accepted (owner, 2026-11-04); licence timing open |

### Family evidence update — 2026-11-04 (evening)

| ID | Item | Status |
|---|---|---|
| ISS-025 | **Partial burns confirmed visually for B1 and B3.** Illuminated post-burn stills (B1 iss038e051117, B3 iss038e051308) show a U-shaped burnt edge ≈ 40 % along the holder and intact film beyond it. B3 side video (overlay 02/20/14 12:26:13–12:27:05): ignition ≈ 12:26:33 with AIR 2, then only a faint near-limit flame while AIR falls 2 → 1; no sustained bright spread. B1 video: bright flame 10:09:46–10:10:10 at AIR 5 / FAN 62; flame gone at 10:10:14 when FAN drops 62 → 41 (cause — extinction vs. crew action after extinction — not determined). Consequence: **B3 did not produce a steady full-length spread**; this strengthens R03 (2.2 mm/s not attributable to B3) and undermines B3 as a transfer anchor (DEC-008 / DEC-016) | Confirmed (visual); crew logs not yet consulted |
| ISS-022 | Clock offset verified with data: B1 still 10:03:47 + 6 min 10 s = 10:09:57, when the B1 video shows the flame | Verified |
| ISS-018 | B1/B3 video overlay shows 02/20/14 vs table 2/19/2014 — same one-day display offset as B6 | Explained by source |
| ISS-020 | Ruler lies **behind** the film (visible through burnt areas of B1, B3, B9, B16). Ruler label period at full resolution: B6 294.9 px, B16 299.7, B3 288.0, B1 290.6 (≈ 29–30 px/mm at the ruler plane, ±2 % across sessions). Sample-plane scale is therefore slightly larger and FiF/GFL rates slightly overestimated until corrected | Open — plane correction |
| ISS-027 | Automatic ruler detection locked onto holder edges for B9/B16/B3/B1 (≈ 20 px/mm, false). Replaced by visually declared ruler bands + automatic period measurement; declared bands recorded as parameters | Mitigated; method limitation recorded |
| ISS-028 | First automatic family run failed its own validation | With an automatic row band (whole frame) and weak abstention rules, B3 returned 2.23 mm/s over ~90 mm of "travel" although the illuminated still shows only ~60 mm burnt; B9 returned a negative rate; B1/B16 had residual RMS up to 250 px. Cause: glare, igniter glow and reflections tracked as flame. **No value from that run is reported.** Remedy: declared holder-opening row bands, quality gates (residual RMS ≤ 25 px, threshold sensitivity ≤ 15 %, travel ≤ 1.2 × burnt length) and status `rejected_qc` with reasons | Mitigated; rerun in progress |
| RES-002 | Family run with quality gates (`data/derived/BASSII_100UM_SPREAD_RATES_v0.1.json`): **measured** B6 2.32 ± 0.10 mm/s (relative-threshold rule set; consistent with RES-001 2.27 ± 0.09) and B15 2.39 ± 0.10 mm/s (same session, 21 % O₂, higher flow; short window 16–26 s, 9–10 frames). **Rejected by QC:** B1 (residuals, threshold sensitivity 77 %), B3 (tracked travel 94 mm > burnt length 64 mm), B9 (residuals 130–170 px, sign changes), B16/B19/B20 (residuals 28–215 px). Candidate values of rejected runs are kept in the file for diagnosis only and are not results. Observation: B6 vs B15 nearly equal despite higher B15 flow — consistent with thin-fuel thermal regime (observation, two runs) | 2 of 8 measured |
| ISS-029 | Dim near-limit flames (17 % O₂: B16, B19, B20) are not tracked reliably by the luminance rule set; B19 candidate (~1.12 mm/s, threshold-consistent) fails only the residual gate. Needs a colour-aware (blue-channel) front definition and per-run exposure handling before any cross-O₂ transfer test | Open — blocks the cross-O₂ holdout test |
