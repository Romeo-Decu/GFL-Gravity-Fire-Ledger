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
