# Claude Task Brief — FiF BASS-II Evidence Acquisition v0.1

**Role:** Read-only Scientific Data Acquisition Analyst  
**Case:** PMMA-100 / BASS-II B3 / sample 148  
**Protocol:** `docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md`  
**Package schema:** `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`  
**Working branch:** `acquisition/pmma100-bass-b3`  
**Package file:** `research/acquisition/PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json`

## 1. Mission

Prepare a source-traceable acquisition package for the bounded PMMA-100 case. Locate primary source records and candidate raw assets, inspect only what is genuinely accessible, inventory files, compute hashes only for bytes actually downloaded and accessible to you, and transcribe source assertions faithfully.

This is evidence acquisition, not a scientific conclusion. Do not prove transferability, resolve undocumented run joins by inference, reproduce flame-spread rate, or modify FiF scientific rules.

## 2. Mandatory access and change boundary

You are being connected through a **read-only GitHub integration**.

- The owner will authorize access to the **FiF repository only**, not all repositories.
- Use the `acquisition/pmma100-bass-b3` branch as the working reference.
- Read only the following FiF materials: this brief, the acquisition protocol, the acquisition package schema, the current acquisition package JSON, and any explicitly selected research references needed for the task.
- Do not request or use write permissions.
- Do not create branches, commits, files, pull requests, issues, comments, tags, releases or workflow runs.
- Do not attempt to change repository settings or permissions.
- Do not ask for credentials, tokens, private keys or account access.
- Do not access other repositories in the owner's GitHub account.
- Return your proposed package JSON and acquisition report in your response to the owner. The FiF Project Manager will independently inspect, validate and decide whether to incorporate any material into GitHub.

If your integration cannot operate read-only or requires broader access than the FiF repository, stop and report the limitation. Do not improvise another access route.

## 3. Operating constraints

1. Read the acquisition protocol and package schema before starting.
2. Preserve the exact `base_repository_commit` already recorded in the package. Do not change it.
3. Do not modify the canonical evidence graph fixture, graph schema, controlled vocabulary, engine, rulesets, tests or UI.
4. Do not commit source media, large archives, credentials, tokens, private keys or personal data.
5. Do not invent source URLs, archive members, file names, checksums, timestamps, identifiers or values.
6. Do not claim a file was downloaded, hashed or inspected unless you actually did so.
7. Do not label your own extraction as independently verified or scientifically validated.
8. Preserve source contradictions and missing information. Never silently choose one version.
9. Do not calculate normalized values, conversions, averages, regression results or physical interpretations.
10. If an asset is not accessible to you, report that fact. Do not imply that the owner's local copy is available to you.

## 4. Source order

Start with these sources:

1. NASA PSI-25 BASS-II Version 4: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
2. NASA/TM-20210011385: https://ntrs.nasa.gov/citations/20210011385
3. SDSU archive named in NASA §2.3.6: http://flame.sdsu.edu
4. Carmignani (2019) dissertation: https://escholarship.org/uc/item/0rb693zc
5. Bhattacharjee et al. (2017), DOI 10.1016/j.firesaf.2017.03.039, for method context only.

The AWS `s3://nasa-psi` bucket is not an established BASS-II data route. Do not assume it contains BASS-II assets. GIPOC/SoFIE data custody does not prove BASS-II availability.

## 5. Candidate PSI-25 entries to re-check

A prior FiF audit records these filenames and sizes as user-reported PSI-25 B3-folder entries, not independently verified inventory:

- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4` — 1.98 MB;
- `PSI-25_Raw Data_iss038e051295.zip` — 534.48 MB;
- `PSI-25_Raw Data_GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf` — 242.37 KB;
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip` — 14.92 MB.

Re-check each against the live repository. Record exact live name, URL, category, byte size and version. Do not infer ZIP contents or assume the still-sequence MP4 is the original acquisition video. The owner reports that the 14.92 MB ZIP is downloaded locally, but it is not available to you unless separately and explicitly supplied.

## 6. Evidence questions

Prioritize:

### A. B3 identity and configuration
- Exact test/run ID as reported; preserve B3 and any B03 alias separately.
- Sample ID 148 and nominal thickness/width.
- Date/GMT, investigation/test matrix row and explicit file-to-run mapping.
- Exact air-display/opposing-flow setting and its context.
- Calibrated and uncalibrated oxygen initial/final readings, retaining both columns and measurement context.
- Pressure, gas composition, fan setting, calibration records and time variation only where actually reported.

### B. Section 2.3 microgravity comparison
- Exact 100-µm comparison record identity and record granularity.
- Source location for the reported 3 cm/s setting.
- Source location and scope for the approximately 2.2 mm/s highest spread rate.
- Any explicit link from this comparison record to B3/sample 148.
- Do not assign 2.2 mm/s to B3 without an explicit source join.

### C. Normal-gravity downward counterpart
- Exact run/test ID, sample ID, date, material identity and source file(s).
- Whether the sample is identified as NASA PMMA; whether grade/batch/manufacturing route/history are stated.
- Exact source location and scope for the reported 2.0 mm/s average.
- Any run-level relationship between that average and a particular video or specimen.

### D. Image/video analysis lineage
- Original video versus still-image-derived video versus processed/composite video.
- Camera view/orientation, frame count, dimensions, codec, bit depth, timestamps, actual frame interval and evidence of conversion/resampling.
- Spatial scale and its source.
- Original NASA Flame Analyzer settings/code/configuration if available.
- Threshold used for the target 100-µm Section 2.3 comparison, if explicitly recoverable.
- Do not substitute 30 (separate Section 2.2.4 extinction study) or 70 (illustrated 75-µm Figure 2.18 example) as the target threshold.
- Do not conflate Flame Analyzer with FIA/FIAT without source evidence of implementation lineage.

## 7. Extraction discipline

For each extracted item:
- create one `extraction_record`;
- preserve exact source value text and unit;
- use `source_reported` for direct transcriptions;
- include an exact locator (page/section/table/row/figure/file/time interval);
- distinguish run-level from section-summary values;
- record extraction method and agent;
- keep any unambiguous numeric parse separate from the exact transcription.

This acquisition-only task must not create FiF `measured`, `derived` or `inferred` results. Quantitative reconstruction is a separate task.

If a source conflict exists, create separate extraction records and a question explaining the conflict. Candidate joins belong in `linkage_candidates`, never as established relationships.

## 8. Required response / deliverables

Return two clearly separated outputs:

**A. Acquisition report**
- sources accessed, versions and access dates;
- assets located, downloaded, inaccessible or not found;
- exact URLs and sizes where verified;
- checksums actually computed;
- extraction count and scope;
- candidate linkages and their limitations;
- unresolved questions;
- explicit limitations and work not performed.

**B. Complete proposed package JSON**
- Preserve package ID, version, case scope and base commit.
- Populate only with source-supported records.
- Conform to `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`.
- Do not add verification, validation, approval or transferability declarations.

If no raw asset can be downloaded, still return a useful source/asset inventory with accurate retrieval states. Do not fabricate completeness.

## 9. Stop conditions

Stop and report rather than improvise if:
- PSI-25 access requires an unavailable account or permission;
- an asset's identity cannot be tied to a source record;
- a file is too large or its licence/terms are unclear;
- a candidate URL is inferred rather than exposed by the source;
- the source uses ambiguous or contradictory identifiers;
- the local ZIP is needed but not actually available to you;
- read-only access is unavailable or broader repository permissions are required.

Do not request credentials. Ask the owner only for a specific missing file or permission when that is the only practical next step.

## 10. Handoff

Return the report and complete proposed JSON to the owner. Do not write to GitHub or open a PR. The FiF Project Manager will independently inspect source locators, values, units, asset hashes, candidate joins, schema compliance and cross-record integrity. A separate scientific review will determine whether any evidence can enter the canonical graph or support later quantitative analysis.
