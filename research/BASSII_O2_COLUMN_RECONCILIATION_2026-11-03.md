# BASS-II Oxygen Column Reconciliation — B3, B4, B11, B13

**Date:** 2026-11-03  
**Primary source:** Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385, Appendix A.1, Table A.1.  
**Status:** Source-column reconciliation; table text extraction checked against the published column order. Visual page-level QA remains desirable before final structured-data ingestion.

## 1. Finding

NASA Table A.1 contains four separate oxygen fields: calibrated initial O2, calibrated final O2, initial O2, and final O2. The public MicroFire Atlas test pages display the latter (uncalibrated) pair but label it as coming from NASA's calibrated initial O2 column. This is a systematic column-attribution error in the secondary transcription, not a discrepancy in the NASA table.

The NASA report explains that CSA-CP O2 readings were offset using Major Constituents Analyzer (MCA) readings on a daily basis. The table preserves both calibrated and uncalibrated values. FiF must retain both, along with crew observations, and must not choose one as the uniquely “true” atmosphere without understanding the calibration procedure and measurement context.

## 2. Reconciled records

| Test | Sample no. | Material | Calibrated initial/final O2 (vol%) | Uncalibrated initial/final O2 (vol%) | Air display (cm/s) | Crew/ground observation |
|---|---:|---|---:|---:|---|---|
| B3 | 148 | 100-µm PMMA film, 2 cm wide | 22.2 / 21.8 | 20.9 / 20.5 | 2 | “Probably 20.6 O2 to start; lower flow flames much more blue overall; still some soot though” |
| B4 | 159 | 300-µm PMMA film, 2 cm wide | 22.2 / 22.2 | 20.6 / 20.6 | 5 | “Bubble layer thickness increases with sample thickness” |
| B11 | 158m | 2-cm, 0.2-mm PMMA film | 21.0 / 20.7 | 20.1 / 19.8 | 5, 3, 1, <1 | “Multiple velocities for steady spread, extinguished at pot 0.35” |
| B13 | 162m | 2-cm, 0.4-mm thick film | 21.0 / 20.5 | 20.1 / 19.6 | 10, 5, 4, 3, 2, 1 | “Multiple velocities for steady spread, extinguished at pot 0.35” |

The table also reports other combustion-product fields. They should be captured independently, with the same source-column discipline, rather than inferred from the oxygen values.

## 3. Secondary-source transcription issue

The MicroFire Atlas pages for B3, B4, B11 and B13 show oxygen values 20.9, 20.6, 20.1 and 20.1 respectively, and label them as NASA's “Calibrated initial O2” values. In NASA Table A.1, those values are in the uncalibrated initial O2 column. The actual calibrated initial values are 22.2, 22.2, 21.0 and 21.0 respectively.

The Atlas is still useful as a discovery and cross-reference layer, but this column mapping must not be inherited into FiF. Cite NASA Table A.1 as the primary source and record the Atlas transcription as secondary with this known correction.

## 4. Experimental interpretation constraints

1. B3 and B4 have single displayed air-velocity values of 2 and 5 cm/s respectively in the table. Do not substitute fan-display values for air-display values.
2. B11 and B13 are changing-flow sequences. They are not single steady-flow datapoints. Their observations explicitly report extinction during reduction of fan potentiometer setting to 0.35.
3. The later fan-potentiometer values are not calibrated velocities. Keep them as controller settings, not cm/s.
4. The O2/CO2/CO values are initial/final measurements of the Microgravity Science Glovebox working volume. They are not continuous, local flame-zone measurements.
5. The B3 crew note explicitly questions the starting oxygen reading. Preserve this as an anomaly; do not replace sensor fields with the note.
6. Figure 2.20 describes a comparison image series at 20.7% O2 / 79% N2 / 1 atm. Do not assume that caption condition is interchangeable with each individual Table A.1 sensor reading. The figure-to-row-to-image linkage and calibration context require separate reconciliation.
7. B3/B03 is a likely formatting alias, but FiF should preserve the exact source identifier in each source and store aliases separately.

## 5. FiF schema requirements

For each test record, store distinct fields for:
- `o2_calibrated_initial_vol_pct`
- `o2_calibrated_final_vol_pct`
- `o2_uncalibrated_initial_vol_pct`
- `o2_uncalibrated_final_vol_pct`
- `o2_crew_note`
- `air_display_cm_s` (only where the table explicitly identifies it as air display)
- `fan_display_or_pot_setting` (separate field; preserve raw sequence)
- `sample_number`
- `test_number`
- `material_raw_description`
- `observations_raw`
- source page, table, column name, extraction method, and verification status

Do not normalize missing, anomalous, or ambiguous values silently. Store raw source text alongside parsed values.

## 6. Source references

- NASA report PDF: https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf
- NASA NTRS record: https://ntrs.nasa.gov/citations/20210011385
- NASA Table A.1 is Appendix A.1, report pp. 103–104. The relevant text extraction is around PDF lines 4725–4950 and 5384–5459.
- Secondary pages showing the column-attribution problem: https://microfire-atlas.vercel.app/experiments/bass2-B3 ; https://microfire-atlas.vercel.app/experiments/bass2-B4 ; https://microfire-atlas.vercel.app/experiments/bass2-B11 ; https://microfire-atlas.vercel.app/experiments/bass2-B13

## 7. Decision

For FiF, NASA Table A.1 takes precedence over the secondary transcription. All four oxygen fields must be preserved. The calibrated/uncalibrated difference is a provenance and calibration issue to be understood, not a reason to discard either column. No transfer fit should use a single oxygen value until the intended measurement basis and figure-to-test linkage are verified.
