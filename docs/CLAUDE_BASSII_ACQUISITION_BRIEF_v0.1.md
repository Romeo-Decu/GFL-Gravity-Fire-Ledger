# Claude Task Brief — FiF BASS-II Evidence Acquisition v0.1

**Role:** Scientific Data Acquisition Agent  
**Case:** PMMA-100 / BASS-II B3 / sample 148  
**Protocol:** `docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md`  
**Package schema:** `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`  
**Base:** latest `main`, after the protocol PR has been merged

## 1. Mission

Build one source-traceable acquisition package for the bounded PMMA-100 case. Locate primary source records and candidate raw assets, inspect what is genuinely accessible, inventory and hash files actually downloaded, and transcribe relevant source assertions into the acquisition package.

Your output is evidence acquisition, not a scientific conclusion. Do not attempt to prove transferability, resolve an undocumented run join by inference, reproduce flame spread rate, or modify FiF's scientific rules.

## 2. Required operating constraints

1. Read the acquisition protocol and package schema before starting.
2. Create a new branch from the latest `main`; do not work on the protocol branch. Record that exact starting commit in `base_repository_commit`, replacing the template's older authoring commit.
3. Create/update only the acquisition package JSON under `research/acquisition/` and a concise package README if genuinely necessary.
4. Do not modify the canonical evidence graph fixture, graph schema, controlled vocabulary, engine, rulesets, tests or UI.
5. Do not commit source media, large archives, credentials, tokens, private keys or personal data.
6. Do not invent source URLs, archive members, file names, checksums, timestamps, identifiers or values.
7. Do not claim a file was downloaded or inspected unless you actually did so.
8. Do not label your own extraction as independently verified or scientifically validated.
9. Preserve source contradictions and missing information. Never silently choose one version.
10. Open a PR for review; do not merge it and do not request that the owner merge it before independent review.

## 3. Source order

Start with these sources:

1. NASA PSI-25 BASS-II Version 4: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
2. NASA/TM-20210011385: https://ntrs.nasa.gov/citations/20210011385
3. SDSU archive named in NASA §2.3.6: http://flame.sdsu.edu
4. Carmignani (2019) dissertation: https://escholarship.org/uc/item/0rb693zc
5. Bhattacharjee et al. (2017), DOI 10.1016/j.firesaf.2017.03.039, for method context only.

The AWS `s3://nasa-psi` bucket is not an established BASS-II data route. Do not use it unless you independently locate a specific BASS-II object. GIPOC/SoFIE data custody does not prove BASS-II availability.

## 4. Candidate PSI-25 entries to re-check

A prior FiF audit records these filenames and sizes as user-reported PSI-25 B3-folder entries, not independently verified inventory:

- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4` — 1.98 MB;
- `PSI-25_Raw Data_iss038e051295.zip` — 534.48 MB;
- `PSI-25_Raw Data_GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf` — 242.37 KB;
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip` — 14.92 MB.

Re-check each against the live repository. Record the exact live name, URL, category, byte size and version. Do not assume that the ZIP contains the target video or that the still-sequence MP4 is the original acquisition video. The owner reports that the 14.92 MB ZIP is downloaded locally, but it is not automatically available to you unless it is present in your workspace.

## 5. Specific evidence questions

Prioritize records that can help answer:

### A. B3 identity and configuration
- Exact test/run ID as reported (preserve B3 and any B03 alias separately).
- Sample ID 148 and nominal thickness/width.
- Date/GMT, investigation/test matrix row and any explicit file-to-run mapping.
- Exact air-display/opposing-flow setting and its context.
- Calibrated and uncalibrated oxygen initial/final readings, retaining both columns and the stated measurement context.
- Pressure, gas composition, fan setting, calibration records and any relevant time variation, only where the source actually reports them.

### B. Section 2.3 microgravity comparison
- Exact 100-µm comparison record identity and record granularity.
- The source location for the reported 3 cm/s setting.
- The source location and scope for the approximately 2.2 mm/s highest spread rate.
- Any explicit link from this comparison record to B3/sample 148.
- Do not assign 2.2 mm/s to B3 without an explicit source join.

### C. Normal-gravity downward counterpart
- Exact run/test ID, sample ID, date, material identity and source file(s).
- Whether the sample is identified as NASA PMMA, and whether grade/batch/manufacturing history are stated.
- Exact source location and scope for the reported 2.0 mm/s average.
- Any run-level relationship between the reported average and a particular video or specimen.

### D. Image/video analysis lineage
- Original video versus still-image-derived video versus processed/composite video.
- Camera view and orientation.
- Frame count, frame dimensions, codec, bit depth, timestamps, actual frame interval and any evidence of frame conversion/resampling.
- Spatial scale and its source.
- Original NASA Flame Analyzer settings/code/configuration if available.
- Threshold used for the target 100-µm Section 2.3 comparison, if explicitly recoverable.
- Do not substitute 30 (separate Section 2.2.4 extinction study) or 70 (illustrated 75-µm Figure 2.18 example) as the target threshold.
- Do not conflate Flame Analyzer with FIA/FIAT without source evidence of implementation lineage.

## 6. Extraction discipline

For each extracted item:
- create one `extraction_record`;
- preserve exact source value text and unit;
- use `source_reported` for values transcribed from a report, table or paper;
- use `source_reported` for direct transcriptions; this acquisition-only task must not create FiF `measured`, `derived` or `inferred` results — any quantitative reconstruction is a separate task;
- include the exact locator (page/section/table/row/figure/file/time interval);
- distinguish run-level from section-summary values;
- record the extraction method and agent;
- keep any parse of a numeric value separate from the exact transcription.

Do not add normalized values, conversions, averages, regression results or physical interpretations. If a source conflict exists, create separate extraction records and a question explaining the conflict.

## 7. Candidate linkages

You may propose relationships only as `linkage_candidates`. Each must identify both records, explain the basis and cite the evidence records supporting it. Explicitly state what is missing.

Examples requiring caution:
- B3 versus B03 alias;
- B3/sample 148 versus Section 2.3 100-µm comparison;
- the 2 cm/s Appendix A.1 value versus the 3 cm/s Section 2.3 value;
- the 2.2 mm/s section-level maximum versus a B3 run result;
- a normal-gravity video versus the 2.0 mm/s section-level average.

Do not mark a candidate linkage established. That decision belongs to independent review and the later controlled graph-mapping stage.

## 8. Deliverables

Create:

`research/acquisition/PMMA100_B3_ACQUISITION_PACKAGE_v0.1.json`

The JSON must conform to `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`.

Your PR description must include:
- exact base commit SHA;
- sources accessed and their versions;
- assets found, downloaded, inaccessible or not found;
- checksums actually computed;
- number and scope of extraction records;
- candidate linkages proposed;
- unresolved questions;
- explicit limitations and work not performed.

If no raw asset can be downloaded, still return a useful source/asset inventory with accurate retrieval states. Do not fabricate completeness.

## 9. Stop conditions

Stop and report rather than improvise if:
- PSI-25 access requires an unavailable account or permission;
- an asset's identity cannot be tied to a source record;
- a file is too large or its licence/terms are unclear;
- a candidate URL is inferred rather than exposed by the source;
- the source uses ambiguous or contradictory identifiers;
- the local ZIP is needed but not actually available to you.

Do not request credentials. Ask the owner only for a specific missing file or permission when that is the only practical next step.

## 10. Handoff

Open the PR as **ready for independent review**, not as validated. The FiF reviewer will independently inspect source locators, values, units, asset hashes, candidate joins and schema compliance. A separate scientific review will determine whether any evidence can enter the canonical graph or support a later quantitative analysis.
