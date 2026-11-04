# FiF — BASS-II / PSI-25 Collection-Level Inventory v0.1

**Status:** Partial collection inventory; file-level enumeration incomplete  
**Date:** 2026-11-04  
**Working branch:** `acquisition/pmma100-bass-b3`  
**Parent inventory:** `research/NASA_COMBUSTION_EVIDENCE_FAMILY_INVENTORY_v0.1.md`  
**Primary collection record:** [NASA PSI-25, Version 4](https://psi.nasa.gov/physci/repo/data/investigations/PSI-25)  
**DOI:** [10.60555/4qc4-de67](https://doi.org/10.60555/4qc4-de67)

---

## 1. Purpose and scope

This record advances Gate 1 from family discovery to a collection-level inventory for BASS-II. It records what the PSI-25 landing page and NASA's PSI guidance expose, distinguishes collection metadata from individual experiment records and files, and identifies the next retrieval tasks.

This is **not** a complete file manifest, an integrity audit, or a declaration that all 694 files added in Version 4 have been inspected. The landing page's visible excerpt is insufficient to enumerate every file and its folder path.

## 2. Collection identity — source-reported

| Field | PSI-25 record |
|---|---|
| Investigation | Burning and Suppression of Solids - II (BASS-II) |
| PSI identifier | PSI-25 |
| Version inspected | Version 4 |
| DOI | 10.60555/4qc4-de67 |
| Research area | Combustion Science |
| Subresearch area | Spacecraft Fire Safety |
| Project type | Microgravity Investigation |
| Flight platform | International Space Station |
| Investigation start | 2010-01-01 |
| Investigation end | 2022-12-31 |
| Submitting date | 2022-12-31 |
| Initial release | 2022-12-31 |
| Version 4 update | 2025-11-24 |
| Version 4 change note | Metadata update |
| Licence | CC0-1.0 |
| NASA centre | Glenn Research Center |
| Sponsoring agency | NASA |

**Interpretation control:** collection start/end dates describe the investigation record's overall period. They do not date every test or every file. Version 4's “Metadata update” label does not establish that all file bytes or scientific values changed.

## 3. Scope and experimental design — source-reported

The PSI-25 description states that BASS-II objectives include studying ignition, flame growth, flame spread and extinction limits for solid fuels burning in low-velocity forced flows in microgravity, and bridging normal-gravity NASA-STD-6001 Test #1, ground-based microgravity tests and actual material flammability in microgravity.

The record identifies primary variables as:
- forced-flow velocity (speed and direction);
- ambient oxygen concentration, adjusted by nitrogen vitiation of the working volume;
- sample geometry, including rods, spherical sections, slabs, films and fabric sheets.

The approach description states:
- tests were conducted aboard the ISS;
- crew provided active real-time “lab partner” support;
- the wind tunnel was installed in the Microgravity Science Glovebox (MSG);
- the MSG supplied power, imaging and a level of containment;
- the fuel sample was mounted inside a small wind tunnel;
- imposed airflow could reach 40 cm/s;
- flame appearance, growth and spread rates were determined in opposed- and concurrent-flow configurations.

These are collection-level descriptions. They must not be copied to every run as if every listed geometry, flow condition or measurement was used in every test.

## 4. Experimental table — observed rows

The PSI-25 landing page exposes an experimental table with, among other fields:
PI, Test #, Date, GMT, Sample #, Fuel Sample Material, Flow restrictor, Fan display, Air display, Radiometer gain, Total Frames Shot, calibrated initial/final O2, initial/final CO2 and initial/final CO.

The PSI-25 page reports **130 experimental-table records** and is configured to show 5 records per page by default (`1–5 of 130`). The accessible indexed page exposes only the first five rows relevant to the 19 February 2014, GMT 50 session. Thus the total record count is confirmed, but 125 rows remain untranscribed. The table has 17 columns, listed below:

| Test | Sample | Fuel sample material (exact source wording) | Flow restrictor | Fan display | Air display | Radiometer gain | Frames | Calibrated O2 initial → final | CO2 initial → final | CO initial → final |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---|
| B1 | 147 | 100 micron PMMA film 2 cm wide | 2 | 62 | 5 | 50 | 57 | 22.2 → 22.2% | 0.44 → 0.44% | 0 → 6 ppm |
| B2 | 155 | 200 micron PMMA film 2 cm wide | 2 | 62 | 5 | 50 | none | 22.2 → 1.6% | 0.44 → blank | 6 → blank |
| B3 | 148 | 100 micron film 2 cm wide | 2 | 47 | 2 | 50 | 253 | 22.2 → 21.8% | 0.43 → 0.49% | 12 → 19 ppm |
| B4 | 159 | 300 micron PMMA film 2 cm wide | 2 | 61 | 5 | 50 | 137 | 22.2 → 22.2% | 0.44 → 0.51% | -1 → 10 ppm |
| B5 | 156 | 200 micron 2 cm wide | 2 | 59 | 5 | 50 | 206 | 22.2 → 21.9% | 0.43 → 0.43% | 0 → 12 ppm |

**Exactness rules:**
- Blank, “none”, negative values and unusual values are preserved as displayed; no correction is inferred here.
- B3's table description does not explicitly say PMMA. The separate NASA Figure 2.20 caption labels B03 as 100-µm PMMA. The relationship is a candidate join to be documented in the B3 reconciliation dossier, not silently rewritten in this table.
- “Fan display” and “Air display” are recorded display fields. Do not relabel them as calibrated physical measurements without the relevant calibration/source documentation.
- The table's calibrated oxygen values are not interchangeable with uncalibrated values reported elsewhere.
- The visible rows are not the complete experimental table.

## 5. Version history and file inventory — what is currently established

The PSI-25 Version 4 landing page states:
- Version 4 updated 2025-11-24;
- change note: “Metadata update”;
- 694 files added;
- 131 files removed.

The visible current file-browser root exposes these folder names: `PSI-25`, `Investigation Metadata Files`, `Engineering Documents`, `Raw Data`, `Reference Data`, `Science Documents`, `Reports`, `Representative Image(s)`, and `Experimental table`. These are root-level entries only; nested contents, exact full paths, sizes and file counts remain unenumerated.

The visible “Files Added” excerpt includes:
1. `PSI-25_metadata_PSI_metadata_PSI-101_BASS-II.zip`
2. `PSI-25_Engineering Documents_BASS-II_Engineering Requirements.pptx`
3. `PSI-25_Raw Data_BASS_GMT50_SAMPLE_147_TEST_B1.mp4`

The visible “Files Removed” excerpt begins with repeated entries named `BASS-II data FAQ.docx`. The repeated display does not establish whether these are duplicate paths, versions, or separate records.

**Critical limitation:** “694 files added” and “131 files removed” are version-history counts. They are not the total current file count, number of experiments, number of tests, or number of unique data assets. The current full folder/file tree has not yet been retrieved.

### 5.1 User-reported candidate B3 filenames — not independently verified in this inventory

The project research notes report the following local/downloaded candidate names:
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4`
- `PSI-25_Raw Data_iss038e051295.zip`
- `PSI-25_Raw Data_GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf`
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip`

These names are retained as user-reported acquisition leads only. Their presence in the current PSI-25 Version 4 tree, exact paths, bytes, archive membership, camera source and relationship to B3 have not been independently verified here. Do not treat a filename as proof of asset identity.

## 6. PSI file organization guidance

NASA's PSI database guide states that investigation files are organized into separate folders by file type. “Raw Data” and “Analyzed Data” are additionally separated by “Reduced Gravity” or “Earth Gravity”; further subfolders may be present depending on the investigation. The guide describes selecting individual files or entire folders for download through the browser.

This describes the repository's general organization guidance. It does not establish the exact BASS-II folder tree, nor that every BASS-II asset follows an identical hierarchy.

**FiF ingestion implication:** preserve the exact repository path and folder ancestry for every asset. Do not flatten the collection into a single filename list and lose the raw/analyzed or reduced-/Earth-gravity distinctions.

## 7. Collection relationships and publication references

The PSI-25 landing page lists related publications and reports, including:
- “Results from on-board CSA-CP and CDM Sensor Readings during the Burning and Suppression of Solids - II (BASS-II) Experiment in the Microgravity Science Glovebox (MSG)” (Olson et al.; DOI 10.1016/j.proci.2014.06.125);
- “Radiative, thermal, and kinetic regimes of opposed-flow flame spread: A comparison between experiment and theory” (DOI 10.1016/j.proci.2016.06.025);
- “Concurrent flame growth, spread, and quenching over composite fabric samples in low speed purely forced flow in microgravity” (DOI 10.1016/j.proci.2016.06.028);
- “A Study of the Effectiveness of a Narrow Channel Apparatus in Simulating Microgravity Flame Spread over Thin Fuels” (DOI 10.2514/6.2012-3493);
- BASS-II Summary Report;
- “Correlation of normal gravity mixed convection blowoff limits with microgravity forced flow blowoff limits”.

These are collection-linked bibliographic records. Their listing does not establish that every paper uses the same runs, data versions or analysis pipeline. Each publication must receive its own source ID and be linked to specific experiments only when its methods, tables, figures or acknowledgements support the join.

## 8. Collection-level acquisition status

| Inventory item | Status | What is needed to close it |
|---|---|---|
| PSI-25 identity, DOI, version, licence | Source-reported and recorded | Preserve landing-page snapshot/access date |
| Collection scope/objectives | Source-reported and recorded | No further collection-level action |
| Experimental table | Partial visible rows recorded | Retrieve/export complete table and preserve exact fields/blank values |
| Version history | Summary counts and visible excerpt recorded | Retrieve complete version history and exact file paths |
| Current file/folder tree | Not retrieved | Obtain full manifest/tree with paths, sizes, file types and version membership |
| B3 candidate files | User-reported filenames only | Verify exact current PSI paths and downloadable bytes |
| B1 MP4 | Filename visible on PSI landing page | Retrieve and inspect metadata; establish camera/stream identity |
| ZIP archives | Candidate names only | Verify archive contents, file manifest, checksums and nested paths |
| Engineering documents | One PPTX filename visible | Retrieve and inspect scope, revision and links to test hardware |
| Processed/analyzed data | Not inventoried | Enumerate folders and identify scripts, outputs, thresholds and lineage |
| Ground-gravity data | Folder structure described generally by PSI guide | Identify exact BASS-II ground-test files and links to specific samples/runs |

## 9. Open issues and next actions

1. **Manifest retrieval:** obtain the complete current PSI-25 file/folder tree, including exact paths, sizes, types and version information. Do not infer it from the “694 added” count.
2. **Experimental table export:** capture all rows and all columns, including blanks, notes, units and any hidden/expandable fields.
3. **B1 asset verification:** retrieve the listed B1 MP4; inspect container metadata, codec, duration, frame rate, dimensions, timestamps and embedded overlays. Do not infer camera stream from extension.
4. **B3 asset verification:** verify the user-reported Still_Sequence, proofsheet and ZIP names against the PSI tree; inspect archive manifests before deciding which asset is minimally necessary.
5. **Raw/analyzed separation:** enumerate the actual folder tree and map all original-to-derived relationships.
6. **Version history:** preserve the Version 4 history and determine which files were added/removed relative to Version 3, without assuming scientific data changed.
7. **Publication linkage:** build a bibliography register and map each paper/report to the exact experiment/run/sample identifiers it actually uses.
8. **Only after the above:** complete the BASS-II collection inventory gate, then begin B3 within-experiment reconciliation.

## 10. Source references

1. NASA PSI-25, Version 4, BASS-II investigation landing page: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25 (DOI 10.60555/4qc4-de67).
2. NASA, *Data Files and Documents*, PSI Database Guide: https://science.nasa.gov/wp-content/uploads/2024/11/psi-database-guide.pdf.
3. NASA, PSI Tutorial: Portal & Workspaces, section “Association Categories for Commonly Delivered Files” (Experimental Table is a `.csv`): https://assets.science.nasa.gov/content/dam/science/bps/bps-general/bps-data_osdr_psi/PSI%20Tutorial_Portal%20%20Workspaces.pdf.
4. NASA, “New File Download Process for PSI Large Requests” (2025-09-29): https://science.nasa.gov/uncategorized/new-file-download-process-for-large-requestspsi-new-file-download-process/.
5. NASA, “A Year of Change for NASA’s Physical Sciences Informatics Database” (2025-07-24): https://science.data.nasa.gov/features-events/physical-sciences-informatics-updates.
6. NASA, “PSI Database is Live with New Features to Improve User Experience” (2024-10-24): https://science.nasa.gov/science-research/psi-database-is-live-with-new-features-to-improve-user-experience/.

---

**Gate status:** BASS-II collection inventory is **in progress**, not closed. The next bounded task is full manifest and table retrieval, not scientific comparison.


## 11. Additional PSI-25 page inspection — 2026-11-04

A fresh indexed extraction of the official PSI-25 Version 4 page exposed additional collection-level structure:

- The experimental table reports **1–5 of 130** records with 5 items per page by default.
- The table has 17 displayed columns: PI; Test #; Date; GMT; Sample #; Fuel Sample Material; Flow restrictor; Fan display; Air display; Radiometer gain (1000 250 50 10); Total Frames Shot; Calibrated initial O2 % by vol; Calibrated final O2 % by vol; Initial CO2 % by vol; Final CO2 % by vol; Initial CO (ppm); Final CO (ppm).
- The visible file-browser root lists: PSI-25; Investigation Metadata Files; Engineering Documents; Raw Data; Reference Data; Science Documents; Reports; Representative Image(s); Experimental table.
- The page extract does not expose nested file entries, full paths, sizes or the complete file tree.

### Retrieval attempt and current limitation

The official page is dynamically rendered. The indexed public extraction exposes the first five table rows and the total count, while direct opening through the available browser interface returns no readable page lines; attempted `?page=1`, `?page=2` and `?page=3` variants were not accessible through that interface. This is a limitation of the current retrieval route, **not evidence that NASA does not provide the records**.

NASA's PSI tutorial specifies that the Experimental Table is to be uploaded as a `.csv` file and describes the file categories expected in a complete investigation record. NASA's 2025 large-download guidance describes selecting files/folders in the PSI browser and submitting large requests for email delivery when the request exceeds 1 GB. These sources confirm a browser-mediated acquisition route, but do not document a public API for enumerating the BASS-II tree. The next retrieval attempt should identify the PSI browser's underlying data request or use a narrowly selected export of the Experimental Table CSV; do not request or download the entire collection.

### Updated status

| Item | Current verified state |
|---|---|
| Experimental-table record count | 130, source-reported by PSI page |
| Rows transcribed from the supplied CSV | 129 data rows of 130 page-reported records; discrepancy open |
| Displayed table columns | 17, source-reported |
| Visible root folder names | 9 |
| Nested folder/file paths | Not retrieved |
| Current total file count | Unknown |
| Version-history delta | 694 added / 131 removed, not a current inventory |
| B1/B3 exact asset paths and bytes | Not verified |
| Experimental Table CSV | Supplied by user; 129 data rows, 17 columns; SHA-256 recorded in audit report |

**Gate 1 remains open.** The newly confirmed table count and root folder names improve the collection inventory but do not satisfy the full-table or full-manifest exit criteria.


### Narrow acquisition fallback

If the PSI browser's table endpoint cannot be discovered programmatically, the minimum useful handoff is **the single CSV stored under the PSI-25 `Experimental table` folder**. Do not upload the Raw Data archive or the complete investigation ZIP for this step. NASA's PSI tutorial explicitly lists the Experimental Table as a CSV deliverable and says published datasets should include the files necessary to enable replication. Exact BASS-II CSV filename and path remain to be confirmed in the browser.


## 12. Experimental Table CSV received and audited — 2026-11-04

The file `PSI-25_Experimental table_BASS-II.csv` was supplied and structurally audited. It parses as 129 data records and 17 columns. The PSI-25 page previously reported 130 records; the discrepancy remains open and is not silently reconciled. The CSV has 130 physical lines including its header.

Record distribution: Bhattacharjee 22; Ferkul 4; Miller 20; Olson 27; Fernandez-Pello 27; T'ien 29. All 129 Test # values are unique within the CSV. There are 19 empty cells and 16 literal `none` cells. The raw audit preserves these as distinct states and records exact affected rows/columns.

B1 and B3 are transcribed exactly in `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md`. B3's material cell reads `100 micron film   2 cm wide` and does not explicitly say PMMA. No sample-to-video/proofsheet linkage is established by the CSV.

Audit report: `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md`.

The uploaded source file SHA-256 is `71e792bf6b5fb5ea620c5dd70fbbac05515992e12aefcf5dff47312caa48c042` (16,590 bytes; UTF-8 BOM; CRLF). The source file has not been modified or normalized in the audit. Gate 1 remains open: reconcile 130-vs-129 and retrieve the nested file manifest.


## 13. Additional retrieval-path verification — 2026-11-04

### 13.1 Current PSI page re-check

A fresh public indexed extraction of the official PSI-25 Version 4 page again exposes:
- Experimental Table pagination: **1–5 of 130**;
- B3 row: Bhattacharjee; B3; 2/19/2014; GMT 50; sample 148; material wording `100 micron film 2 cm wide`; flow restrictor 2; fan display 47; air display 2; radiometer gain 50; 253 frames; calibrated O2 22.2 → 21.8%; CO2 0.43 → 0.49%; CO 12 → 19 ppm;
- the same nine root folder names listed in Section 5;
- a visible Files Added excerpt that includes the B1 MP4 filename, but no B3 candidate asset names in the indexed excerpt.

This independently re-confirms the page-side 130 count and literal B3 table wording. It does **not** explain why the supplied CSV has 129 data rows, and it does not establish any B3 asset path.

### 13.2 Public AWS mirror check — not a BASS-II manifest source

The AWS Registry of Open Data entry for NASA PSI identifies the public bucket `arn:aws:s3:::nasa-psi` in `us-west-2`, but its listed resource description is specifically **Directional Solidification Insert (DSI) and Observation and Analysis of Smectic Islands In Space (OASIS) data**. The bucket's browser page exposes a generic PSI Data Explorer, but the registry metadata does not identify BASS-II / PSI-25 as part of that bucket resource.

**Acquisition decision:** do not treat this S3 bucket as a verified mirror of PSI-25 and do not use it to infer that BASS-II files are absent. It is not currently a supported route for closing ISS-008.

### 13.3 Official PSI download procedure

NASA's 2025 PSI large-download guidance confirms the supported browser workflow: select only the required files/folders and choose Download Zip; requests larger than 1 GB are prepared and delivered by email, in multiple parts, with links valid for 7 days. NASA recommends downloading only what is needed and splitting very large requests.

**FiF acquisition rule:** first obtain the file-browser manifest and select only B1/B3 candidate assets plus the minimum associated metadata/proof-sheet material. Do not request the full investigation archive. The PSI guide describes general file organization, but the exact BASS-II nested hierarchy still requires direct inspection in the PSI browser.

### 13.4 Current status after this check

| Question | Result |
|---|---|
| Does the current public PSI page still report 130? | Yes; 1–5 of 130 |
| Does the indexed B3 row explicitly say PMMA? | No; it says 100 micron film 2 cm wide |
| Are B3 candidate files confirmed in current tree? | No |
| Is the public AWS bucket verified as a BASS-II mirror? | No; registry resource description names DSI and OASIS |
| Is a narrow browser-mediated download route documented? | Yes; select required files/folders; >1 GB via email multi-part delivery |
| Is the nested BASS-II manifest retrieved? | No |

**Gate 1 remains open.** The remaining critical retrieval work is direct inspection/export of the nested PSI-25 file tree and an authoritative explanation for the 130-vs-129 table count. No scientific B1/B3 comparison is authorized by this retrieval check.

## 14. Source references added

7. NASA PSI-25 Version 4 indexed page extract (current table count, B3 row, visible folder roots and version history): https://psi.nasa.gov/physci/repo/data/investigations/PSI-25.
8. AWS Registry of Open Data, NASA PSI entry (public bucket metadata and resource description): https://registry.opendata.aws/nasa-psi/.
9. NASA, “New File Download Process for PSI Large Requests” (2025-09-29): https://science.nasa.gov/uncategorized/new-file-download-process-for-large-requestspsi-new-file-download-process/.

## 14. PSI manifest retrieval-path review — 2026-11-04

### 14.1 What the public sources establish

- The current indexed PSI-25 Version 4 page exposes the investigation record, the Experimental Table excerpt, nine root folder names and a visible file-browser section. It does not expose the nested current folder/file paths, byte sizes or a complete manifest in the indexed extraction.
- NASA's PSI Database Guide describes a browser file tree in which users expand folders, select individual files or folders, and download the selection. It notes that Raw Data and Analyzed Data may be separated by Reduced Gravity or Earth Gravity, with investigation-specific subfolders.
- NASA's 2025 large-download guidance documents the browser's selective Download Zip workflow and multipart email delivery for requests above 1 GB.
- NASA's public API catalogue documents an Open Science Data Repository (OSDR) API. No source-supported mapping from that API to PSI-25's current investigation file browser or its nested BASS-II file manifest has been established in this review. Do not treat an OSDR endpoint as a PSI-25 file endpoint without explicit documentation or a verified response.

### 14.2 Search and access attempts

- Direct opening of the PSI-25 landing page through the available browser retrieval interface returned no readable page lines; indexed extraction remains limited to the visible excerpt.
- Public web searches for the four user-reported B3 candidate filenames returned no indexed matches. This is a search-index limitation, not evidence that the files are absent from the live PSI tree.
- No exact download URL, nested path, byte size, or current version membership was recovered for the B3 candidates.
- No undocumented endpoint or guessed URL is used. The local execution environment also could not resolve the PSI host directly; this is an environment limitation and says nothing about NASA service availability.

### 14.3 Current retrieval decision

The next step is direct browser inspection of the PSI-25 file tree. Begin with the Raw Data root and record every visible child folder/file name exactly as displayed, including indentation/hierarchy. Then inspect the minimum related folders needed for B3: Investigation Metadata Files, Engineering Documents, Science Documents, Reports and Experimental table. Do not download the full investigation archive.

For each discovered entry, record exact displayed name, parent path, category, displayed size/date/version if present, and whether the file itself has been downloaded. A filename or displayed size is not a checksum; compute SHA-256 only from exact downloaded bytes.

**ISS-008 remains open.** The nested manifest is not retrieved, and the B3 candidate asset paths remain unverified. The public index's failure to return a candidate filename must not be converted into a not found in NASA claim.

### 14.4 Sources

1. NASA PSI-25 Version 4 landing page: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25.
2. NASA, Data Files and Documents, PSI Database Guide: https://science.nasa.gov/wp-content/uploads/2024/11/psi-database-guide.pdf.
3. NASA, New File Download Process for PSI Large Requests (2025-09-29): https://science.nasa.gov/uncategorized/new-file-download-process-for-large-requestspsi-new-file-download-process/.
4. NASA Open APIs catalogue, Open Science Data Repository Public API section: https://api.nasa.gov/.
