# BASS-II / PSI-25 Experimental Table — Source Audit v0.1

**Audit date:** 2026-11-04  
**Source file supplied:** `PSI-25_Experimental table_BASS-II.csv`  
**Source bytes:** 16,590  
**SHA-256:** `71e792bf6b5fb5ea620c5dd70fbbac05515992e12aefcf5dff47312caa48c042`  
**Encoding observed:** UTF-8 with BOM  
**Delimiter / line ending observed:** comma-separated / CRLF  
**Audit scope:** structural transcription and source-integrity checks only; no scientific interpretation or normalization.

## 1. Executive result

The supplied CSV parses as **129 data records and 17 columns**. The PSI-25 web page previously exposed a count of **130** experimental-table records. This discrepancy is unresolved. The CSV contains 130 physical lines: one header plus 129 data records. It is not yet known whether the page count includes a header-like item, whether the CSV export omits one record, or whether the web count and downloaded export represent different table states.

Do not silently force the CSV to 130 data records. Do not infer which record, if any, is absent.

## 2. Record distribution by PI

| PI | Data records |
|---|---:|
| Bhattacharjee | 22 |
| Ferkul | 4 |
| Miller | 20 |
| Olson | 27 |
| Fernandez-Pello | 27 |
| T'ien | 29 |
| **Total** | **129** |

All 129 `Test #` values are unique in this CSV.

## 3. Exact 17 source column names

1. `PI`
2. `Test #`
3. `Date`
4. `GMT`
5. `Sample #`
6. `Fuel Sample Material`
7. `Flow restrictor`
8. `Fan display`
9. `Air display`
10. `Radiometer gain   (1000   250   50   10)`
11. `Total Frames Shot`
12. `Calibrated  initial O2 % by vol `
13. `Calibrated final O2 % by vol`
14. `Initial CO2 % by vol`
15. `Final CO2 % by vol`
16. `Initial CO (ppm)`
17. `Final CO (ppm)`

Whitespace in column names is retained above as observed. A normalized schema may later add canonical field identifiers, but must preserve these original labels.

## 4. B1 and B3 exact source transcription

Values below are literal CSV cell contents after CSV parsing; no unit conversion or inference has been applied.

| Field | B1 | B3 |
|---|---|---|
| PI | Bhattacharjee | Bhattacharjee |
| Test # | B1 | B3 |
| Date | 2/19/2014 | 2/19/2014 |
| GMT | 50 | 50 |
| Sample # | 147 | 148 |
| Fuel Sample Material | 100 micron PMMA film   2 cm wide | 100 micron film   2 cm wide |
| Flow restrictor | 2 | 2 |
| Fan display | 62 | 47 |
| Air display | 5 | 2 |
| Radiometer gain | 50 | 50 |
| Total Frames Shot | 57 | 253 |
| Calibrated initial O2 % by vol | 22.2 | 22.2 |
| Calibrated final O2 % by vol | 22.2 | 21.8 |
| Initial CO2 % by vol | 0.44 | 0.43 |
| Final CO2 % by vol | 0.44 | 0.49 |
| Initial CO (ppm) | 0 | 12 |
| Final CO (ppm) | 6 | 19 |

**Important:** the B3 material cell does not explicitly contain “PMMA”; B1 does. This is a source-level distinction. It may be reconciled with other records only through an explicit evidence link, not by editing the CSV transcription.

## 5. Missing and literal sentinel values

The CSV contains:
- **19 empty cells** across the table;
- **16 cells containing the literal string `none`**.

These are different source states and must remain distinct in the raw layer. The current audit does not reinterpret `none` as null, zero, not applicable or failed measurement.

### Empty cells

| Column | Test # values |
|---|---|
| Fan display | M5; O3a; O3b; P1; P2; P3a; P3b; T6; T13; T14; T16; T17; T18 |
| Air display | O7; O8a; O8b; O9 |
| Final CO2 % by vol | B2 |
| Final CO (ppm) | B2 |

### Literal `none` cells

| Column | Test # values |
|---|---|
| Total Frames Shot | B2 |
| Calibrated final O2 % by vol | B14; F3 |
| Final CO2 % by vol | B14; F3; P3b; P22a; T28a |
| Initial CO2 % by vol | P22b; T28b |
| Initial CO (ppm) | P22b; T28b |
| Final CO (ppm) | B14; F3; P22a; T28a |

## 6. Sequence and representation observations

- Bhattacharjee records B1–B22 are all present in this CSV.
- Olson labels include letter-suffixed tests (e.g. O3a/O3b, O5a/O5b, O8a/O8b, O13a/O13b, O15a/O15b).
- Fernandez-Pello labels include suffixes and gaps in the visible numbering (P7 and P11 do not occur in this CSV).
- T'ien labels include T28a and T28b; T8 does not occur in this CSV.
- These are observations about the supplied CSV only. A gap in test numbering is not proof of a missing data row.
- Fan display and Air display contain multi-value sequences, annotations and mixed text; they are not single numeric scalars in every record.
- `Sample #` contains values with suffixes and case differences (e.g. `153m`, `141M`); retain as string, not integer.
- The CSV contains source spelling and capitalization variants (e.g. `SIBAL`, `Sibal`) and descriptive notes in material/display fields. No vocabulary harmonization was applied.

## 7. Data handling requirements derived from this audit

1. Preserve the supplied CSV unchanged as the raw source artifact in the local evidence package; record the SHA-256 above.
2. Parse all fields as strings in the immutable raw representation.
3. Keep empty string, literal `none`, numeric-looking text and mixed-format text distinct.
4. Do not coerce `Sample #` or `Test #` to numbers.
5. Do not split Fan/Air display sequences until a separately versioned extraction rule defines the semantics and provenance.
6. Any normalized/derived table must retain source filename, row locator (CSV line number), original column label, original cell value and transformation record.
7. The 130-vs-129 discrepancy must remain a visible issue until reconciled against the PSI page/export mechanism or an authoritative corrected export.

## 8. Open issues

| ID | Issue | Status | Closure evidence |
|---|---|---|---|
| ISS-009 | PSI web page reports 130 table records; supplied CSV has 129 data records | Open | Authoritative explanation or matching export with 130 data records, including exact identity of any differing record |
| ISS-008 | Full nested PSI-25 file manifest is still unavailable; the Experimental Table CSV has been obtained separately | Open | Enumerated current folder/file tree with exact paths and available metadata |
| ISS-011 | B3 material cell omits PMMA while other records/publications may identify the run differently | Open | Explicit source linkage establishing sample material identity; retain conflicting source wording |

## 9. Scope boundary

This audit does **not** establish:
- that all 129 records are complete or scientifically valid;
- that the CSV is the exact same snapshot as the page's 130-record count;
- that B3 is PMMA solely from this row;
- that a sample number maps to a particular video, image sequence, proof sheet or publication figure;
- that fan/air display text is a calibrated continuous flow time series;
- any flame-spread rate or physical comparability result.

The BASS-II collection inventory Gate 1 remains open because the nested file manifest and 130-vs-129 discrepancy are unresolved. No B1/B3 scientific comparison is authorized by this audit alone.


## 10. Register cross-reference correction — 2026-11-04

An earlier version of this audit assigned the outstanding nested PSI-25 file-manifest task to ISS-010. The authoritative Decision, Issue, Idea & Implementation Register subsequently consolidated that task under **ISS-008** and closed **ISS-010** administratively as a duplicate. This correction aligns the audit table with the register; it does not close or reduce the outstanding manifest-retrieval work. ISS-009 remains the separate 130-vs-129 Experimental Table count discrepancy.
