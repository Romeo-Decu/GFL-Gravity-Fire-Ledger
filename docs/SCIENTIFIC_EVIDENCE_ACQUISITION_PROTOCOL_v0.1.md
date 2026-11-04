# FiF — Scientific Evidence Acquisition Protocol v0.1

**Status:** Proposed operational protocol; requires review before first acquisition PR  
**Initial case:** PMMA-100 / BASS-II B3 / sample 148 / Section 2.3 / normal-gravity downward counterpart  
**Package schema:** `schemas/EVIDENCE_ACQUISITION_PACKAGE_v0.1.schema.json`  
**Canonical graph:** `schemas/EVIDENCE_GRAPH_v0.1.schema.json`

## 1. Purpose and boundary

This protocol governs the discovery, retrieval, inventory and faithful transcription of scientific source material into a reviewable acquisition package.

The acquisition package is a **staging record**, not the canonical evidence graph, not an assessment, and not a validation attestation. It must preserve source identity, exact source wording/value, units, locators, file identity, unresolved joins and contradictions. A separate deterministic adapter and controlled review process may later map accepted records into the canonical graph.

Acquisition, verification and scientific validation are separate activities:

1. **Acquisition:** find and record what a source or asset actually contains.
2. **Verification:** independently check source identity, transcription, units, locators, asset integrity and proposed joins.
3. **Scientific validation:** determine whether evidence is adequate for a declared scientific use or inference.

An acquisition agent must not self-certify steps 2 or 3. A correct transcription is not automatically a valid measurement; a retrievable source is not automatically scientifically sufficient.

## 2. Non-negotiable rules

1. Preserve original source values and units exactly as reported. Never overwrite them with normalized or converted values.
2. Record exact identifiers as printed. Keep aliases separate and label their status; do not silently normalize B3 to B03 or vice versa.
3. Every extracted assertion must have a source ID and a precise locator (page, section, table/row, figure, file, dataset record or time interval).
4. Separate source-reported statements from FiF measurements, calculations and interpretations.
5. A value transcribed from a paper/report/table is `source_reported`, not `measured`.
6. Do not invent missing values, file names, run joins, sample identities, timestamps, checksums, calibrations, uncertainties or software lineage.
7. Preserve every conflicting source assertion independently. Do not average, choose a preferred value or silently resolve a conflict.
8. Unknown is a valid result. Missing, inaccessible and unresolved information must remain explicit.
9. Do not treat filename similarity, shared material, nominal thickness, figure resemblance or narrative proximity as proof of run identity.
10. Do not add validation/lifecycle fields or claims to the package. The schema intentionally has no such field.
11. Do not modify the canonical graph fixture, graph schema, controlled vocabulary, transfer rules or engine during an acquisition task.
12. Do not copy large copyrighted source passages or redistribute source files unless the source licence permits it. Record links, metadata and short locators instead.

## 3. Initial acquisition scope

The first acquisition package is deliberately narrow. It concerns:

- NASA BASS-II experiment B3, Appendix A.1, sample 148, nominal 100-µm PMMA;
- the separate Section 2.3 nominal 100-µm microgravity comparison;
- the normal-gravity downward 100-µm PMMA comparison;
- source records and assets needed to determine whether any of these records can be joined at run/sample/file level.

The package is intended to investigate, not assume resolution of, these gaps:

- Appendix A.1 B3 air-display flow of 2 cm/s versus Section 2.3.6 comparison flow of 3 cm/s;
- whether B3 is the exact microgravity run represented in the Section 2.3 comparison;
- whether the reported microgravity maximum of about 2.2 mm/s can be linked to B3 (currently it cannot);
- the B3-specific spread-rate result and its original image/video lineage;
- the normal-gravity downward run ID, sample identity, source video and result lineage;
- sample grade, batch, manufacturing route and relevant material-property records;
- original acquisition timing, image scale, image-analysis settings and uncertainty basis.

Do not broaden the first package into a general BASS-II data dump. Retrieve the smallest set of assets that can answer a defined question.

## 4. Source hierarchy and acquisition routes

Use the following order, while recording what was actually accessible:

1. **NASA PSI-25, BASS-II Version 4** — first route for the investigation record, raw data, engineering/reference documents, representative images and experimental table. Landing page: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
2. **NASA/TM-20210011385** — primary report and source of the published BASS-II summary. NTRS record: https://ntrs.nasa.gov/citations/20210011385
3. **SDSU flame.sdsu.edu archive** — NASA explicitly identifies this as the location where BASS still-image-derived videos and downward-experiment videos were posted. Access timed out during the 2026-11-04 audit; no archive file has yet been independently retrieved. Do not claim the archive is currently accessible or complete.
4. **Carmignani (2019) dissertation** — secondary cross-reference for BASS setup, B3/sample metadata and FIAT methodology. https://escholarship.org/uc/item/0rb693zc
5. **Bhattacharjee et al. (2017) methods paper** — methodological reference for image-based flame-spread measurement, not proof of the exact NASA Flame Analyzer implementation/settings. DOI: https://doi.org/10.1016/j.firesaf.2017.03.039
6. **SDSU research group / PI** — contact route only if public primary records remain inaccessible. No contact or permission may be implied unless it actually occurred.

The AWS `s3://nasa-psi` bucket is not an established BASS-II route. Its public index was found to expose DSI/OASIS/pk4 folders; do not use it as a BASS-II source unless a specific BASS-II object is independently located. GIPOC/SoFIE data custody is not evidence that BASS-II files are held there or available to FiF.

## 5. Candidate assets already identified — not yet independently verified

The 2026-11-04 SDSU archive audit records the following PSI-25 B3-folder entries as reported by the user:

- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4` — reported size 1.98 MB;
- `PSI-25_Raw Data_iss038e051295.zip` — reported size 534.48 MB;
- `PSI-25_Raw Data_GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf` — reported size 242.37 KB;
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip` — reported size 14.92 MB; the user reports downloading this ZIP locally.

These are **candidate inventory entries**, not independently inspected assets. Re-check the live PSI-25 listing and record exact displayed name, category, byte size, URL and version. Do not infer archive contents or checksum from a filename or reported size. The locally downloaded ZIP is not available to an agent unless it has actually been shared with that agent or placed in an accessible workspace.

A prior filename pattern in a PSI-25 change log is not proof of the exact B3 asset path. Do not fabricate a URL by extrapolating a naming convention.

## 6. Package structure and identifiers

Every acquisition PR must include one package JSON conforming to the acquisition package schema. The package has five collections:

- `source_records`: publications, reports, dataset landing pages, archives and other identifiable sources;
- `asset_records`: individual downloadable files or archive members, each with its own identity and retrieval state;
- `extraction_records`: one source assertion or metadata fact per record, preserving exact source text/value and locator;
- `linkage_candidates`: proposed relationships between records, with rationale and evidence references;
- `unresolved_questions`: explicit questions, affected records and the next evidence needed.

Use stable IDs with these prefixes: `src_`, `asset_`, `extract_`, `link_`, `q_`. Reuse existing source IDs where applicable (for example `src_nasa_tm_2021` and `src_carmignani_2019`); do not create duplicate IDs for the same source. The empty template records the repository commit at which it was authored; **replace `base_repository_commit` with the exact `main` SHA from which the acquisition branch is actually created**. Never leave a stale base SHA in a populated package.

For each numeric extraction, preserve at least:
- exact source value transcription (`source_value_text`);
- parsed literal value only if unambiguous (`parsed_value`);
- exact source unit (`unit_as_reported`);
- qualifiers/statistic type or scope exactly as stated (`qualifier_as_reported`);
- evidence state;
- exact source locator.

Do not add normalized values or perform unit conversions in the acquisition package. A later deterministic normalization stage will preserve the original and record the conversion method, version and parent assertion.

## 7. File and archive integrity procedure

For each candidate file:

1. Record its exact source URL, category, displayed name, version, size and access time.
2. If downloaded, hash the exact original bytes with SHA-256 and record the lowercase 64-character digest.
3. For an archive, preserve the archive hash and list member paths, uncompressed sizes and available timestamps without changing the archive.
4. If a member is extracted, hash the exact extracted member bytes separately and retain the parent archive ID and member path.
5. Preserve original filenames. Derivatives (converted, cropped, stabilized, annotated or transcoded) receive new asset IDs, hashes and parent-asset links.
6. Never write a checksum unless it was computed from the exact bytes. If download or hashing was not possible, leave the checksum absent and record the limitation.

No large source media should be committed to Git merely to demonstrate acquisition. Store source URLs, metadata, hashes and controlled references; use an approved storage route for large assets if one is later established.

## 8. Extraction and conflict handling

- Transcribe each source assertion separately, even when it disagrees with another source.
- Keep source identifiers and record granularity explicit: run-level, sample-level, section-summary, campaign-level or unknown.
- A value reported for a section-level comparison must not be assigned to B3 without an explicit source join.
- Keep calibrated and uncalibrated oxygen readings separate and retain their original labels and context.
- Do not convert oxygen readings into local flame-zone values; the B3 table entries are initial/final MSG working-volume readings, not continuous local flame-zone time series.
- Do not assign the 2.2 mm/s section-level maximum to B3 without explicit linkage.
- Do not treat the normal-gravity 2.0 mm/s section-level average as a run-matched measurement.
- Record a possible relationship as a linkage candidate with limitations, not as an established edge.
- If a source does not expose a value or identifier, record the question and the evidence needed; do not create a placeholder numeric value.

## 9. Image/video acquisition boundary

The acquisition task may inventory, download where permitted, hash and inspect file metadata. It must not report a FiF spread-rate measurement or quantitative reproduction unless the separate video-measurement protocol has been followed.

Use `research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md` for any later video analysis. In particular:

- do not assume container FPS equals acquisition frame rate;
- do not assume the 6-mm scale shown in NASA Figure 2.18 applies to B3;
- do not assume threshold 30 or 70 is the original threshold for the target 100-µm Section 2.3 comparison;
- do not conflate NASA's Flame Analyzer with the 2017 FIA/FIAT method without implementation-lineage evidence;
- do not copy NASA's reported <5% uncertainty as FiF's own uncertainty.

## 10. Separation of duties and review

The acquisition agent's role is source discovery and faithful extraction only. It must not mark its own output independently verified, scientifically validated, approved or transferable.

The review sequence is:

1. Structural validation against the acquisition package JSON Schema.
2. Source verification: exact source, version, licence, retrieval and locator.
3. Asset verification: exact file identity, archive/member relationship and hash.
4. Extraction verification: compare every proposed value with the original source and preserve exact units/context.
5. Linkage challenge: independently test each proposed run/sample/file join; filename and narrative similarity are insufficient.
6. Scientific review: combustion regime, experimental context, measurement definition and uncertainty limitations.
7. Controlled mapping: only accepted records are eligible for a deterministic mapping into the canonical evidence graph.

If a second source or genuinely independent reproduction is unavailable, record that limitation. Three agents reading the same source are not three independent confirmations. No missing verification may be fabricated or silently waived.

## 11. GitHub workflow and change boundary

- Create a dedicated acquisition branch from the latest `main`.
- Open a PR; do not commit directly to `main`.
- The PR must contain the package JSON and, if necessary, a concise acquisition note. Do not include engine, transfer-rule, canonical graph fixture/schema or UI changes.
- Do not modify an existing source assertion to make a new source agree with it. Add a new extraction record and preserve the conflict.
- Keep source media out of Git unless explicitly approved and licence-compatible.
- Include the base commit SHA in the package.
- The PR description must list sources accessed, assets actually downloaded, hashes actually computed, records extracted, unresolved issues and anything not completed.
- Do not request merge. The independent reviewer must inspect the PR and explicitly approve it first.

Git history and file hashes improve traceability but do not, by themselves, constitute the full append-only/tamper-evident validation-attestation architecture described in the canonical graph contract.

## 12. Completion criteria

An acquisition package is ready for independent review only when:

- it parses and validates against the package schema;
- every source and asset has a stable ID and exact locator/URL;
- every extracted value retains its exact source representation, unit and context;
- every file hash is computed from the exact bytes or explicitly absent;
- all proposed joins have supporting references and stated limitations;
- all conflicts and unknowns remain visible;
- no unsupported calculations, scientific conclusions or validation claims have been added;
- the PR contains no unrelated engine/rule/graph/UI changes.

Passing these criteria means **ready for review**, not scientifically validated and not approved for quantitative transfer.
