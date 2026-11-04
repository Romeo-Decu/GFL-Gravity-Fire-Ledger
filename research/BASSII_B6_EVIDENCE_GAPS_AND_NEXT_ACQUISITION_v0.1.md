# FiF — BASS-II B6 Evidence Gaps & Next Acquisition v0.1

**Status:** Active gap register  
**Date:** 2026-11-04  
**Scope:** BASS-II thin-PMMA / 100-µm family, first detailed run B6  
**Related records:**  
- `research/BASSII_B6_PRIMARY_SOURCE_RECORD_v0.1.md`
- `research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md`
- `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md`
- `research/BASSII_PSI25_COLLECTION_INVENTORY_v0.1.md`

---

## 1. Confirmed source set

| ID | Source / artefact | What it contributes | Current state |
|---|---|---|---|
| SRC-B6-01 | NASA/TM-20210011385, Appendix A, Table A.1 | B6 identity, test conditions, fan/air displays, frame count, calibrated and uncalibrated gas readings, crew observation | Reviewed; primary source |
| SRC-B6-02 | Carmignani (2019) dissertation, Table A.2 | BASS test matrix, B6 PMMA geometry, O₂ and flow summary | Reviewed; scientific secondary analysis |
| SRC-B6-03 | Carmignani (2019), Figures 5.4, 5.6, 5.8 | B6 images, flame length/development length, radiometer, anemometer, FIAT area and 2D area | Figure content reviewed; no point-level digitization |
| SRC-B6-04 | PSI-25 B6 original video archive | Main view, second view and still-image sequence | Archive inventory reported by Claude; FiF byte-level inspection pending |
| SRC-B6-05 | PSI-25 B6 ProofSheet PDF | Still identifiers, camera metadata, time span and gap | Downloaded previously; needs explicit linkage to original streams |
| SRC-B6-06 | PSI-25 Fan calibration workbook | Potential mapping between fan/potentiometer/display and physical flow | Downloaded and ZIP/XLSX validity checked by Claude; workbook contents not yet inspected by FiF; external workbook link unresolved |
| SRC-B6-07 | MicroFire Atlas B6 page / public transcription | Secondary transcription and competitor audit target | Reviewed; calibrated/uncalibrated O₂ distinction lost |
| SRC-B6-08 | NASA PSI-62 data release | Post-processed BASS/BASS-II experimental imagery, two-color tomography, 3D soot/temperature reconstructions and comparison metrics | Landing-page metadata reviewed; ZIP contents not inspected |

## 2. B6 archive members known from prior browser inspection

Archive: `PSI-25_Raw Data_BASS_GMT188_SAMPLE_153_TESTB6 original videos.zip`  
Reported size: 32,841,516 bytes (31.32 MiB); ZIP reported valid; three members:

| Member | Reported size | Provisional role |
|---|---:|---|
| `BASS_GMT188_SAMPLE_153_TESTB6.ts` | 15,603,436 bytes | Main view |
| `BASS_GMT188_SAMPLE_153_TESTB6_2ND_VIEW.ts` | 15,728,080 bytes | Second camera view |
| `BASS_GMT188_SAMPLE_153_TESTB6_Still_Sequence.ts` | 6,491,828 bytes | Still-image sequence |

The archive's member names and sizes are reported from prior browser inspection, not independently re-hashed by FiF. “Main view” and “second camera view” are provisional interpretations based on filenames.

B6 folder reportedly also contains:
- `ProofSheet.pdf` (~501.7 KB);
- three MP4 files (conversion relationship to the TS streams not verified).

## 3. Outstanding gaps

| Gap ID | Missing evidence / unresolved question | Why it matters | Next action | Status |
|---|---|---|---|---|
| GAP-B6-01 | Original B6 TS streams not available in FiF workspace | Independent image/video reconstruction impossible | Import archive; hash archive and members; probe codecs, frame rates, timestamps and streams | Blocked on local archive transfer |
| GAP-B6-02 | Exact stream-to-camera / view mapping | Prevents false pairing of side/top view with sensors and FIAT | Inspect metadata and representative frames; compare proof sheet and video | Open |
| GAP-B6-03 | Figure 5.8 numerical series not digitized | Published derived data cannot yet be compared point by point | Digitize radiometer, anemometer, FIAT area and 2D area separately with uncertainty | Open |
| GAP-B6-04 | B6 flow field 1–7 cm/s vs NASA fan/air display sequence | Physical flow comparability and time-dependent conditions unresolved | Inspect workbook, figure axes, video overlays and source definitions | Open |
| GAP-B6-05 | Fan calibration workbook's external dependency | Calibration values may refer to a missing workbook | Inspect formulas, named ranges, external links and cached values; locate linked workbook | Open |
| GAP-B6-06 | Flow-change timestamps and actual response | Flow steps cannot be aligned to flame development from table alone | Extract voice confirmations, display changes and anemometer response from video | Open |
| GAP-B6-07 | Sensor calibration / uncertainty / response metadata | Needed for physical interpretation and uncertainty propagation | Locate sensor specifications and calibration sheets | Open |
| GAP-B6-08 | FIAT software, version, threshold and processing settings | Needed to reproduce thesis-derived flame metrics | Search cited theses/software appendix; contact/locate code only if necessary | Open |
| GAP-B6-09 | NASA Flame Analyzer vs dissertation FIAT relationship | Avoid conflating different tools and outputs | Compare cited method descriptions and implementations | Open |
| GAP-B6-10 | BASS-II source imagery in PSI-62 | Could provide processed 3D flame/soot/temperature data | Retrieve PSI-62 ZIP and inventory all files, metadata and licenses | Open |
| GAP-B6-11 | Raw sensor logs / full numerical time series | Published plots are not raw measurements | Search PSI-25, PSI-62, SDSU archive and thesis supplements for machine-readable data | Open |
| GAP-B6-12 | Exact relationship between BASS-II B6 and dissertation's BASS nomenclature | Avoid incorrect experiment identity claim | Preserve source labels; verify against Table A.1, sample ID and source citations | Partially resolved; cross-source identity strong |
| GAP-B6-13 | PMMA specimen batch, mass, length, surface preparation and sample reuse history | Influences reproducibility and physical comparability | Inspect full test matrix, NASA anomaly/sample records and source archive | Open |
| GAP-B6-14 | Timebase synchronization / clock offsets | Flame, flow and voice series may be offset | Build explicit clock mapping from video metadata, proof sheet and BASS video clock | Open |

## 4. Additional primary/secondary source discovered: NASA PSI-62

**Record:** PSI-62, *Concurrent Flame Spread Modeling using Flamelet Generated Manifolds in Microgravity with Comparison to BASS Experiments using Two-Color Tomography*.  
**NASA record:** https://psi.nasa.gov/physci/repo/data/investigations/PSI-62  
**DOI:** https://doi.org/10.60555/e9xp-ex83  
**Version:** 1; initial release 14 November 2025; CC0-1.0.  
**File listed:** `PSI-62_metadata_NEWID-7_Concurrent Flame Spr.zip`

NASA describes the release as involving post-processing of experimental imagery from BASS and BASS-II using two-color tomography and DSLR cameras, with 3D reconstructions of soot and temperature fields. Reported evaluation metrics include flame geometry, temperature distribution, soot volume fraction and flame spread rate.

**Important:** these are NASA landing-page descriptions. FiF has not inspected the ZIP, confirmed that it contains B6, or established which records/files are associated with BASS-II versus BASS. Do not assume B6 is included. This archive is a high-priority acquisition because it may contain numerical/derived data beyond the PSI-25 videos.

## 5. Other known data source: SDSU Flame Research Archive

NASA/TM-20210011385 states that BASS-II top-view imagery / test points were catalogued at:
https://flame.sdsu.edu/

NASA also describes a MATLAB-based Flame Analyzer used to estimate instantaneous flame spread rate from top-view video. The archive URL timed out during the previous access attempt. Its present availability is unverified.

Potential follow-up:
- try archive/CDN/alternate host paths;
- search institutional theses and publications for downloadable analysis files;
- preserve the fact that the archive is documented by NASA even if current access fails.

Do not spend disproportionate time on this before inspecting the thesis and PSI-62 data release.

## 6. Data quality issue to propagate across the full BASS-II collection

The MicroFire Atlas B6 record presents 20.1 → 20.0 vol% as O₂ values, while NASA Table A.1 contains:
- calibrated O₂: 21.0 → 20.9 vol%;
- uncalibrated O₂: 20.1 → 20.0 vol%.

This establishes a confirmed B6 secondary-source mapping error. It does **not yet prove** that every Atlas record has the same error. Audit all 22 Bhattacharjee rows and, if relevant, all other PI matrices before making a collection-wide claim.

## 7. Priority order

1. **Digitize Carmignani Figure 5.8** (B6 published derived evidence).
2. Inspect the PSI-62 ZIP and identify whether it contains BASS-II/B6 source or derived measurements.
3. Inspect Fan calibration workbook and resolve external workbook dependency.
4. Receive and process original B6 archive; hash every file; extract frame/time metadata.
5. Reconcile NASA display steps, dissertation flow range, anemometer trace and voice confirmations.
6. Expand the oxygen-field mapping audit across all 22 Bhattacharjee tests.
7. Only then create a B6 synchronized time-series dataset and perform independent spread-rate reconstruction.

## 8. Completion rule

A gap closes only when the missing evidence is acquired and its provenance/quality is recorded, or when the limitation is explicitly accepted with a reason and impact statement. A plan to inspect a file is not completion. A graph estimate is not raw data. A secondary transcription is not a primary source.
