# Source Correction — B3 Oxygen Columns

**Date:** 2026-11-03  
**Supersedes:** the statement in PMMA_SOURCE_RECONCILIATION_AUDIT_v0.1.md that withdrew the calibrated B3 values 22.2/21.8 as unverified.

## Primary-source verification

Direct inspection of NASA/TM-20210011385, Table A.1, Appendix A.1, B3 row (report page 104; PDF text around lines 5384–5419) confirms the following values in the published column order:

| Field | B3 value |
|---|---:|
| Calibrated initial O2 | 22.2 vol% |
| Calibrated final O2 | 21.8 vol% |
| Initial O2 (uncalibrated/raw table field) | 20.9 vol% |
| Final O2 (uncalibrated/raw table field) | 20.5 vol% |
| Initial CO2 | 0.43 vol% |
| Final CO2 | 0.49 vol% |
| Initial CO | 12 ppm |
| Final CO | 19 ppm |

The operational note is: “Probably 20.6 O2 to start; lower flow flames much more blue overall; still some soot though”.

The earlier audit draft's 22.2/21.8 pair was in fact the NASA table's **calibrated** initial/final O2 values. It was incorrectly withdrawn because the secondary MicroFire Atlas transcription appears to have relabelled the 20.9/20.5 uncalibrated values as calibrated values. This is a secondary-transcription column-mapping error, not evidence that NASA's calibrated values are absent.

## Interpretation and remaining uncertainty

- The four oxygen fields must remain distinct; never collapse calibrated and uncalibrated values into one field.
- The crew/ground note “Probably 20.6 O2 to start” is an operational observation and must be retained alongside the sensor values.
- The discrepancy between calibrated readings (22.2/21.8), uncalibrated readings (20.9/20.5), and the crew note (20.6 starting O2) requires understanding the calibration/offset context. The report's general description says CSA-CP O2 readings were offset using MCA ambient-atmosphere data on a daily basis; this does not by itself explain the exact row-level difference.
- Figure 2.20's caption describes the selected image series at 20.7% O2 / 79% N2 / 1 atm. Do not assume this caption value is interchangeable with every Table A.1 sensor field. It may be the nominal comparison condition; the mapping between figure image, test row, and actual atmosphere must be explicitly resolved.
- Table A.1's PDF text extraction interleaves columns. The B3 values above are supported by the row context in the direct NASA PDF text, but the rendered table should still be visually checked before final machine-readable ingestion.

## FiF decision

The B3 row must store:
1. o2_calibrated_initial_vol_pct = 22.2
2. o2_calibrated_final_vol_pct = 21.8
3. o2_uncalibrated_initial_vol_pct = 20.9
4. o2_uncalibrated_final_vol_pct = 20.5
5. crew_note = “Probably 20.6 O2 to start; lower flow flames much more blue overall; still some soot though”

The calibrated and uncalibrated readings are not competing versions of the same field; they are separate source columns. Do not use the MicroFire Atlas transcription for these fields without correcting its column mapping.

## Source

Olson, S. L. et al. (2021), *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385, Appendix A.1, Table A.1, B3 row, report p. 104. Official NASA PDF: https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf
