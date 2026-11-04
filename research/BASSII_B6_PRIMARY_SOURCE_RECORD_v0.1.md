# FiF — BASS-II B6 Primary-Source Record v0.1

**Status:** Source extraction recorded; independent raw-media verification pending  
**Date:** 2026-11-04  
**Experiment identity:** BASS-II / Bhattacharjee / B6 / GMT188 / sample 153m  
**Primary source:** Olson et al., *Burning and Suppression of Solids–II (BASS–II) Summary Report*, NASA/TM-20210011385 (October 2021), Appendix A, Table A.1 (Bhattacharjee test matrix).  
**Official record:** https://ntrs.nasa.gov/citations/20210011385  
**PDF:** https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf

---

## 1. Identity and matching evidence

NASA Table A.1 identifies the record as:
- PI: Bhattacharjee
- Test: B6
- Actual date: 7 July 2014
- GMT: 188
- Sample: 153m
- Fuel/sample: 2-cm, 0.1-mm PMMA film
- Flow configuration: opposed flow
- Ignition: integral igniter
- Flow restrictors: two

This matches the previously identified PSI-25 archive path and media naming:
`BASS_GMT188_SAMPLE_153_TESTB6`
and its `TESTB6` video/archive family. The identity match is supported by the shared test ID, GMT, sample ID, material, width and thickness. The raw streams themselves have not yet been independently inspected by FiF; therefore media-to-row linkage is **strongly supported, pending byte-level and visual verification**.

## 2. Source-transcribed B6 values

The following values are transcribed from NASA Appendix A, Table A.1. Display sequences and comments are retained as source representations; they are not converted into a single scalar.

| Field | NASA Table A.1 value | Interpretation / handling |
|---|---|---|
| Actual date | 7 July 2014 | Source-reported |
| GMT | 188 | Source-reported |
| Test | B6 | Source-reported |
| Sample | 153m | Preserve suffix |
| Fuel sample | 2 cm, 0.1 mm PMMA film | Source-reported |
| Configuration | Opposed flow | Source-reported |
| Igniter | Integral | Source-reported |
| Flow restrictors | 2 | Source-reported |
| Fan display | 0.9, 1.3, 2.75 | Ordered display sequence; no conversion applied |
| Air display | 3, 5, approaching 10 cm/s | Ordered crew/display sequence; final value is explicitly approximate |
| Total frames shot | 80 | Source-reported |
| **Calibrated initial O₂** | **21.0 vol%** | Use this field for calibrated initial O₂ |
| **Calibrated final O₂** | **20.9 vol%** | Use this field for calibrated final O₂ |
| Uncalibrated initial O₂ | 20.1 vol% | Separate field; do not relabel as calibrated |
| Uncalibrated final O₂ | 20.0 vol% | Separate field; do not relabel as calibrated |
| Initial CO₂ | 0.33 vol% | Source-reported |
| Final CO₂ | 0.41 vol% | Source-reported |
| Initial CO | 0 ppm | Source-reported |
| Final CO | 0.3 ppm | Source-reported |
| Crew observation | “Steady burning at 3 and 5 cm/s, did not reach 10 cm/s before end of sample, complete burnout, HCl –>0.3” | Verbatim source observation; preserve notation |

**Important:** The two oxygen pairs are separate source columns. The calibrated pair is 21.0 → 20.9 vol%; the uncalibrated pair is 20.1 → 20.0 vol%. Neither pair should overwrite the other.

## 3. Critical transcription discrepancy found in a secondary dataset

The public MicroFire Atlas B6 page displays O₂ as 20.1 → 20.0 vol% and describes these as readings from the NASA table. Its page does not preserve the distinction between the calibrated and uncalibrated O₂ columns in the NASA Table A.1 record.

This is a **secondary-source field-mapping error**, not a disagreement between NASA primary records:
- NASA calibrated O₂: 21.0 → 20.9 vol%.
- NASA uncalibrated O₂: 20.1 → 20.0 vol%.
- MicroFire Atlas currently presents the latter pair as its O₂ values without the calibrated/uncalibrated distinction.

Do not ingest the Atlas oxygen values into FiF's calibrated O₂ field. The Atlas remains a discovery/secondary transcription source only.

Secondary page: https://microfire-atlas.vercel.app/experiments/bass2-B6  
NASA report: https://ntrs.nasa.gov/citations/20210011385

## 4. Interpretation boundaries

- The crew observation supports steady burning at the displayed 3 and 5 cm/s steps and complete burnout before the flow display reached the attempted “approaching 10” step. It does **not** establish a precise extinction velocity.
- “Air display” and “Fan display” are not interchangeable physical measurements. Preserve both source fields and their sequence.
- The NASA report's table values are not a time series. They do not provide timestamps for each flow change.
- The table's frame count is not a substitute for the original video frame rate, frame timestamps or image sequence.
- CO₂ and CO are enclosure measurements reported before/after the test; they are not local flame composition measurements.
- Do not calculate oxygen consumption, heat release, flame spread rate or extinction threshold from the before/after table alone.

## 5. Source location and provenance

Primary source: NASA/TM-20210011385, Appendix A, Table A.1, Bhattacharjee test matrix, B6 row. The relevant row is in the extracted PDF text around the B6 record (source extraction lines 5526–5535 in the prior source review). Table A.1 is the authoritative source for the calibrated and uncalibrated O₂ column distinction.

Related independent source: Carmignani (2019), Appendix A, Table A.2, B6 row; see `research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md`.

## 6. Verification status

| Claim | Status |
|---|---|
| B6 identity, GMT188, sample153m | Source-reported; cross-source match |
| PMMA, 20 mm width, 0.1 mm thickness | Source-reported; corroborated by thesis |
| Calibrated O₂ 21.0 → 20.9% | Source-reported from NASA calibrated columns |
| Uncalibrated O₂ 20.1 → 20.0% | Source-reported from NASA uncalibrated columns |
| Crew observations / flow sequence | Source-reported |
| Exact time history of flow steps | Not present in this table |
| Raw sensor time series | Not yet acquired |
| Independent video-derived spread rate | Pending FiF processing |
| Byte-level integrity of the original B6 archive | Pending user-provided archive |
| Exact mapping between each stream and camera view | Archive member names known; technical inspection pending |

**Do not mark B6 fully reconstructed.** This record establishes a reliable test-level metadata baseline, not a complete run reconstruction.
