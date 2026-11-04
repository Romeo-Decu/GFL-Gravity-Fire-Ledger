# FiF — Source Acquisition & Evidence Gap Register v1.0

**Purpose:** Prevent repeated discovery work by maintaining one prioritized list of source documents, datasets, files, methods and standards needed to complete FiF.  
**Baseline:** 2026-11-04  
**Authority:** Use with docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md and docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md.

## 1. Status rules

- **Reviewed / extracted:** content was inspected and the relevant findings are recorded in a linked FiF document.
- **Metadata only:** landing page or bibliographic record inspected; archive/document contents not inspected.
- **User-held / not in FiF workspace:** owner reports possession/download; FiF has not independently hashed or inspected the bytes in its current workspace.
- **Candidate / path not verified:** filename or URL is a lead, not a confirmed current asset.
- **Not retrieved:** source is identified but contents are not available.
- **Not yet identified:** exact source/file/run identifier is unknown.
- **Required:** needed for the stated work package.
- **Conditional:** required only if the related capability or evidence family is included in the release.

Never upgrade a status because a URL exists or a document is mentioned in another source.

## 2. Priority A — required for the first validated PMMA-100 case

| ID | Source / asset | Exact locator | Current status | Required information / why | Next action / closure evidence |
|---|---|---|---|---|---|
| SRC-A01 | NASA PSI-25 BASS-II Version 4 | https://psi.nasa.gov/physci/repo/data/investigations/PSI-25 ; DOI 10.60555/4qc4-de67 | Collection metadata reviewed; 9 root folders known; nested manifest incomplete | Exact current folder tree, version membership, file names, paths, sizes and links to tests | Enumerate selected folders and nested paths; preserve retrieval date/version and file metadata. Closes ISS-008. |
| SRC-A02 | PSI-25 Experimental Table CSV | Source filename: PSI-25_Experimental table_BASS-II.csv | Acquired and structurally audited; 129 rows, 17 columns; SHA-256 recorded | Explain page count 130 versus 129 CSV data rows; preserve all original cells | Compare CSV with authoritative PSI export/API/page data; identify exact missing/different record or document source limitation. Closes ISS-009. |
| SRC-A03 | NASA BASS-II Summary Report | NASA/TM-20210011385, October 2021; https://ntrs.nasa.gov/citations/20210011385 ; PDF: https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf | Reviewed and extracted for B3/B6; Appendix A test matrices recorded | Primary source for test-level conditions, sensor fields, frame counts and crew observations; Sections 2.2/2.3 for published summary outcomes and image-processing method | Preserve exact locators and create per-test source assertions where needed. Already cited in B3/B6 dossiers; do not repeat general report search. |
| SRC-A04 | Carmignani PhD dissertation (2019) | Luca Carmignani, Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes; https://escholarship.org/uc/item/0rb693zc ; PDF: https://escholarship.org/content/qt0rb693zc/qt0rb693zc.pdf | Reviewed; B3 and B6 extractions exist | BASS experiment matrix, FIAT methodology, imaging/measurement error, B3/B6 analyses, Figure 5.8 | Digitize Figure 5.8; record exact plotted axes and uncertainty. Preserve source label “BASS”; do not silently relabel BASS-II. |
| SRC-A05 | B3 original media archive | Candidate PSI-25 filename: PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip | User-reported local candidate; current exact PSI path, bytes and archive contents not independently verified by FiF | Original B3 media, camera views, frame timing and asset lineage | Verify exact PSI path; inspect archive members; hash archive and each member; classify original video vs still-sequence-derived video. |
| SRC-A06 | B3 still-sequence / large archive / proof sheet | Candidate names: BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4; iss038e051295.zip; GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf | Candidate files reported by owner; proof-sheet reviewed in earlier work; exact current PSI paths and bytes not verified | Image IDs, timestamps, camera details, timebase and stream relationship | Re-verify exact PSI path and media membership; link proof-sheet IDs to streams without assuming filename proves identity. |
| SRC-A07 | B6 original media archive | PSI-25 candidate: PSI-25_Raw Data_BASS_GMT188_SAMPLE_153_TESTB6 original videos.zip; reported 32,841,516 bytes, 3 TS members | User-held / previously browser-inventoried by Claude; not byte-level inspected or hashed by FiF | Main view, second view, still sequence; independent reproduction of B6/FIAT results | When archive bytes are made available to FiF, hash archive/members, probe stream metadata and inspect representative frames. |
| SRC-A08 | B6 proof sheet and MP4 derivatives | B6 folder ProofSheet.pdf and three MP4 files (reported by Claude) | Candidate inventory only; conversion lineage unverified | Camera identity, frame/time mapping, relation to TS streams | Verify exact file paths, hashes, metadata and parent/child conversion lineage. |
| SRC-A09 | PSI-25 Fan calibration workbook | Fan calibration data.xlsx (official PSI-25 Reference Data folder; exact path to re-confirm) | User downloaded; Claude verified XLSX container; contents not inspected by FiF; external link to missing workbook reported | Mapping between fan/potentiometer/display and physical flow | Inspect formulas, named ranges, hidden sheets, cached values, external links and calibration conditions. Do not infer mapping from display values alone. |
| SRC-A10 | Workbook external-link dependency | External workbook referenced by SRC-A09; exact file name/path not yet established | Not acquired / not identified | Calibration may depend on a second workbook; cached values may be incomplete or stale | Extract exact external-link target from workbook metadata; search PSI-25 Reference Data and related engineering docs for that exact target. |
| SRC-A11 | NASA PSI-62 tomography archive | https://psi.nasa.gov/physci/repo/data/investigations/PSI-62 ; DOI https://doi.org/10.60555/e9xp-ex83 ; listed ZIP: PSI-62_metadata_NEWID-7_Concurrent Flame Spr.zip | Landing-page metadata reviewed; ZIP contents not inspected; B6 coverage unknown | Potential 3D soot/temperature reconstruction and flame geometry / spread metrics | Retrieve ZIP; inventory files; inspect metadata; establish BASS vs BASS-II run membership before use. |
| SRC-A12 | SDSU Flame Research Archive | https://flame.sdsu.edu/ | NASA report documents archive; prior direct access attempts timed out; current contents unavailable | Original BASS imagery, FIAT/Flame Analyzer data, time series and tutorials | Try alternate institutional/archive routes and thesis references; record exact access attempt and outcome. Do not claim data exist in an uninspected archive. |
| SRC-A13 | FIAT / Flame Analyzer software source | Carmignani dissertation references FIAT; NASA TM describes MATLAB Flame Analyzer; archive tutorials reportedly at flame.sdsu.edu | Methods described; exact software source/version/thresholds not acquired | Reproducibility of published image-derived metrics; determine whether tools are related or distinct | Retrieve and compare software/manuals; preserve separate tool identities unless source proves lineage. |
| SRC-A14 | Nadertabar MA thesis (2019) | “Flame analyzer: a matlab based flame spread analysis tool”, SDSU; exact public URL not yet located | Bibliographic lead from Carmignani references | NASA/SDSU Flame Analyzer implementation details, thresholds and analysis method | Search SDSU institutional repository by exact title and author; obtain thesis and inspect methods/code appendices. |
| SRC-A15 | Celniker MA thesis (2017) | “Flame Analyzer 2: A fully two dimensional flame spread video analysis tool”, SDSU; exact public URL not yet located | Bibliographic lead from Carmignani references | Second implementation / two-dimensional image analysis method | Search SDSU institutional repository by exact title and author; compare with FIAT and NASA Flame Analyzer without assuming equivalence. |
| SRC-A16 | Bhattacharjee et al. opposed-flow flame spread paper | “Opposed-flow flame spread: A comparison of microgravity and normal gravity experiments to establish the thermal regime”, Fire Safety Journal (2016); DOI 10.1016/j.firesaf.2015.11.011 | Bibliographic source identified; relevant published findings/methods reviewed | Cross-check thermal-regime argument and video-derived spread-rate method | Extract exact experimental IDs, data sources, uncertainty and any supplementary data; determine overlap with NASA TM and dissertation. |
| SRC-A17 | Normal-gravity downward 100-µm NASA PMMA data | NASA TM Figure 2.20(e)/Section 2.3 and SDSU Flame Stabilizer research records; exact run/sample/file not identified | Not yet identified | Run ID, sample ID, video or reduced time series, sample grade/batch, geometry, ignition and analysis lineage for the 2.0 mm/s average | Search NASA/SDSU primary records and source references; contact research group only after exact missing item is defined. |
| SRC-A18 | PMMA specimen properties and provenance | BASS-II specimen records, engineering documents, NASA/SDSU material records; exact grade/batch/manufacturing record unknown | Partially source-reported; target specimen properties unknown | Density, heat capacity, conductivity, thickness tolerance, mass, surface condition, batch and manufacturing route | Retrieve sample-preparation and engineering records; use literature/material datasheets only as secondary properties and label them accordingly. |

## 3. Priority B — required for a complete research platform, not necessarily first PMMA vertical slice

| ID | Source family / standard | Exact locator | Current status | Why needed | Acquisition / use rule |
|---|---|---|---|---|---|
| SRC-B01 | NASA PSI investigation catalogue | https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/ | Catalogue route identified | Discovery of additional combustion investigations | Record investigation IDs, DOI, version, licence and files per investigation. |
| SRC-B02 | SoFIE investigation datasets | NASA PSI / SoFIE official investigation record; exact PSI identifier and dataset list not yet registered | Family identified in FiF research; dataset-level inventory incomplete | Solid-fuel ignition/extinction; second solid-fuel family after BASS-II | Acquire official record, metadata, experimental tables, raw/analyzed data and validation publications. |
| SRC-B03 | SAFFIRE I–III and later records | SAFFIRE-I PSI-98, DOI 10.60555/0t15-1z43; https://psi.nasa.gov/physci/repo/data/investigations/PSI-98 | Investigation identity recorded; full versions/files not inventoried | Larger-scale spacecraft fire, flame spread and smoke/fire characterization | Separate evidence family; do not pool directly with small BASS tests. Acquire reports, videos, metadata and data lineage. |
| SRC-B04 | ACME investigations | NASA ACME facility description: https://science.nasa.gov/biological-physical/investigations/acme/ | Family context identified; individual investigations not inventoried | Gaseous-flame combustion and fundamental combustion physics | Inventory individual ACME investigations and data; keep gaseous flame phenomena separate from solid fuel spread. |
| SRC-B05 | BRE investigations | NASA BRE description: https://science.nasa.gov/biological-physical/investigations/bre/ | Family context identified; individual data not inventoried | Gaseous combustion used to emulate selected condensed-fuel thermal/combustion characteristics | Do not treat BRE as direct observation of a burning solid sample. |
| SRC-B06 | FLEX / FLEX-2 | NASA investigation records; exact PSI record IDs and dataset versions to be registered | Family identified in FiF research; full inventory not complete | Droplet combustion and flame-extinguishment mechanisms | Separate liquid-fuel evidence family and outcomes. |
| SRC-B07 | SAME / SAME-R | NASA investigation records; exact PSI record IDs and versions to be registered | Family identified; full inventory not complete | Smoke and aerosol measurements | Use for aerosol/smoke diagnostics, not as direct flame-spread evidence. |
| SRC-B08 | NASA-STD-6001 Test 1 | NASA technical standard; current revision and exact official PDF to be registered | Referenced in BASS-II purpose; current revision not recorded in this register | Ground material flammability test context and comparison limitations | Retrieve current official revision; record version/date and applicable sections. |
| SRC-B09 | NASA-STD-3001, Volume 2 — Fire Protection technical brief | NASA Human Systems Integration / Fire Protection technical brief; exact current URL/revision to be registered | Identified in prior FiF research, current version not pinned | Safety context and requirements, not experimental source data | Retrieve official version, date, scope and requirement traceability. |
| SRC-B10 | Official NASA Space Apps 2026 challenge statement and judging criteria | Official challenge page and project-specific brief; exact archived snapshot not yet committed | Challenge context reviewed in prior research; snapshot not pinned in repo | Ensure MVP still satisfies the actual challenge request and evaluation rubric | Save official challenge brief, criteria and access date; map each requirement to a demo feature and test. |
| SRC-B11 | NASA PSI data-user/database guide | Official PSI guide describing folder organization and browser download workflow; exact version/URL to be pinned | Guidance reviewed; exact snapshot not committed | Reproducible acquisition route and interpretation of raw/analyzed/gravity folders | Preserve current guide and version; do not generalize its folder structure beyond what it states. |

## 4. Priority C — optional or research-extension sources

| ID | Source | Status | Trigger |
|---|---|---|---|
| SRC-C01 | Newer peer-reviewed work on microgravity flame spread, extinction, soot and radiation | Literature search is ongoing; no single comprehensive pinned bibliography yet | Before expanding physical models beyond thin-PMMA case. |
| SRC-C02 | PMMA thermal decomposition / pyrolysis kinetics and property datasets | Not yet curated as a versioned FiF property library | When a quantitative solid-phase model requires properties not available in NASA records. |
| SRC-C03 | Detailed transport / gas-phase kinetic mechanisms | Not yet selected or validated for target case | Only when the chosen model includes gas-phase chemistry beyond empirical transfer assessment. |
| SRC-C04 | Residual acceleration / ISS g-jitter records for specific BASS tests | Not yet acquired at run-level | If gravity/residual acceleration is shown to govern the selected outcome or model validity. |
| SRC-C05 | CFD / multiphysics benchmark datasets | Not selected | Only after a model and validation target are defined; no generic CFD expansion. |

## 5. Already reviewed sources — do not rediscover

The following have already been identified and reviewed sufficiently for the current baseline:
- NASA/TM-20210011385, including BASS-II Appendix A matrices and B3/B6 rows.
- Carmignani (2019) dissertation, including B3/B6 conditions, FIAT method and Figures 5.4, 5.6, 5.8.
- PSI-25 collection metadata, version 4, DOI and root folder names.
- PSI-25 supplied Experimental Table CSV structural audit (129 rows / 17 columns).
- NASA PSI-25 source organization guidance at summary level.
- NASA PSI-62 landing-page metadata and listed ZIP filename.
- MicroFire Atlas B6 secondary record; the calibrated/uncalibrated O₂ mapping error is recorded.
- BASS-II video processing methodology described in NASA TM and Carmignani.
- BASS-II B3 proof-sheet timing metadata from prior review.

Existing FiF records:
- research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md
- research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md
- research/BASSII_DATA_ACCESS_ROUTE_AUDIT_2026-11-03.md
- research/CARMIGNANI_2019_BASS_B3_CROSS_SOURCE_AUDIT_2026-11-03.md
- research/SECTION_2_3_100UM_DATA_LINKAGE_AUDIT_2026-11-03.md
- research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md
- research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md
- research/BASSII_B6_EVIDENCE_GAPS_AND_NEXT_ACQUISITION_v0.1.md

## 6. Source acquisition order

1. Close the PSI-25 table count and nested manifest (SRC-A01/A02).
2. Verify B3/B1/B6 media and exact archive membership (SRC-A05 to A08).
3. Inspect the Fan calibration workbook and identify its external dependency (SRC-A09/A10).
4. Retrieve and inspect PSI-62 archive (SRC-A11).
5. Obtain FIAT/Flame Analyzer software/theses and digitize Carmignani Figure 5.8 (SRC-A04, A12–A16).
6. Identify the normal-gravity downward 100-µm run and its original media/data (SRC-A17).
7. Retrieve target specimen/material properties and provenance (SRC-A18).
8. Only after the PMMA-100 case is reconstructed, expand to priority B families.
9. Priority C sources are acquired only when a defined model or feature requires them.

## 7. Acquisition record requirements

For every source or asset added:
- source ID and stable record ID;
- exact title, author/organization and publication/release date;
- official URL / DOI / repository path;
- version, licence and access date;
- exact filename and parent folder path;
- byte size, MIME/file format and SHA-256 for downloaded bytes;
- archive member inventory and member hashes where relevant;
- retrieval status and reason if unavailable;
- experiment/run/sample linkage evidence;
- exact source locators for every extracted value;
- source-reported vs measured vs derived vs inferred status;
- unresolved questions and next evidence required.

No source should be searched again unless its register status or a newly identified question justifies it.


## Product-scope and source-demand reconciliation — 2026-11-04

The active product baseline is **MVP = FiF Core + all Extensible modules**. This register therefore treats source acquisition not only as a B3/B6 case-study task but also as the evidence foundation for the in-scope analysis modules. See [FiF Product & Module Traceability Matrix](../docs/FIF_PRODUCT_MODULE_TRACEABILITY_MATRIX_v1.0.md).

### Evidence requirements by MVP module

- **NASA Data Intelligence / Experiment Comparison:** primary landing pages, exact investigation and run identities, raw/processed asset manifests, metadata, publications, acquisition/processing descriptions and version history.
- **Physics-Based Similarity / Advanced Transferability:** material and geometry properties, boundary/initial conditions, gravity level, flow and gas composition, pressure/temperature, ignition method, instrumentation, calibration, uncertainty, timebase and outcome definitions. Missing values remain unknown.
- **Evidence-Backed Synthesis / FiF Advanced Analytics:** source text/table/figure locators, extraction method, claim lineage, conflicting assertions and reference datasets for method testing.
- **CRAM-1:** thermophysical properties and transport parameters with source, temperature/pressure dependence, units and validity ranges; calibrated measurements needed for relevant state variables.
- **CRAM-2:** time-resolved flame/combustion observations, regime labels/definitions, operating conditions and independent reference classifications.
- **CRAM-3:** sufficiently sampled time series, sampling interval, synchronization, instrument response, missingness and measurement-noise characterization; data adequacy must be assessed before nonlinear/information estimators are selected.
- **Probabilistic Anomaly Detection:** representative normal/abnormal cases or defensible synthetic/reference distributions, labels and class prevalence assumptions.
- **Uncertainty Quantification:** measurement calibration, repeatability, resolution, extraction sensitivity, parameter uncertainty, covariance and transformation uncertainty.
- **FiF Research & Control:** source/configuration versions, method parameters, execution logs, decision provenance and controlled review records.

### Future-research source requirements

Predictive models, multiphysics, fire scenarios, MPC, ECLSS decision support and sensor integration require additional data and system interfaces beyond the present PMMA-100 source audit. Their source needs, candidate NASA datasets, property databases, system documentation, sensor specifications and validation benchmarks must be recorded as research gaps. These are not presumed available and are not MVP acceptance prerequisites unless the Project Owner changes scope.

### Acquisition priority clarification

The immediate B3/B6 and PSI-25/PSI-62 work remains necessary and is not displaced. However, the source catalogue must identify which evidence families can support each MVP module and where evidence is insufficient. Do not claim CRAM, probabilistic detection or predictive validity from a single case or from metadata that lacks the required temporal/measurement resolution.
