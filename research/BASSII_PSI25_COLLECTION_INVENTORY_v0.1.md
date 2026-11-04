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

The accessible page excerpt contains the following first rows relevant to the 19 February 2014, GMT 50 session:

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
3. NASA, “A Year of Change for NASA’s Physical Sciences Informatics Database” (2025-07-24): https://science.data.nasa.gov/features-events/physical-sciences-informatics-updates.
4. NASA, “PSI Database is Live with New Features to Improve User Experience” (2024-10-24): https://science.nasa.gov/science-research/psi-database-is-live-with-new-features-to-improve-user-experience/.

---

**Gate status:** BASS-II collection inventory is **in progress**, not closed. The next bounded task is full manifest and table retrieval, not scientific comparison.
