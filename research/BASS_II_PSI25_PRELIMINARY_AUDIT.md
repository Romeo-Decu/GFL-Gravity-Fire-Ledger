# BASS-II / NASA PSI-25 — Preliminary Data Audit

**Audit status:** Metadata and repository-interface inspection only  
**Date:** 2026-11-03  
**Source:** NASA Physical Sciences Informatics, PSI-25, BASS-II  
**DOI:** 10.60555/4qc4-de67  
**Observed repository version:** Version 4  
**Version update shown by NASA:** 24-Nov-2025  
**Licence shown by NASA:** CC0-1.0  
**Branch:** `docs/scientific-system-architecture-v0.1`

## 1. Scope and evidence boundary

This audit records what is visible on the NASA PSI-25 investigation page. It is not a raw-file audit. No underlying CSV, spreadsheet, video, engineering document or report has yet been downloaded and independently inspected.

The PSI-25 page reports:
- Investigation: Burning and Suppression of Solids-II (BASS-II).
- Platform: International Space Station.
- Investigation period: 2010–2022.
- Research area: Combustion Science; sub-area: Spacecraft Fire Safety.
- Licence: CC0-1.0.
- Displayed repository version: Version 4, updated 24-Nov-2025.
- Version history indicates 694 files added and 131 files removed in the Version 4 change record. These are version-change counts, **not a verified current total file count**.
- Experimental Table: 130 records.
- No associated Modeling Table is displayed.

Source page: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25

## 2. Scientific scope visible in the record

NASA describes BASS-II as investigating ignition, flame growth, flame spread and extinction limits for solid fuels burning in low-velocity forced flows in microgravity.

The page identifies principal variables including:
- forced-flow speed and direction;
- ambient oxygen concentration, adjusted through nitrogen vitiation;
- sample geometry, including rods, spherical sections, slabs, films and fabric sheets.

The experiment apparatus is described as a small wind tunnel installed in the Microgravity Science Glovebox, with airflow speeds up to 40 cm/s. Flame appearance, growth and spread were studied in opposed and concurrent flow.

This makes BASS-II a strong candidate for a first bounded FiF dataset, but the PSI landing-page summary is not enough to define quantitative comparison rules. Actual run-level files and technical documentation must be inspected.

## 3. Experimental table: visible fields

The page exposes 130 experimental records and displays at least the following columns:

- PI
- Test #
- Date
- GMT
- Sample #
- Fuel Sample Material
- Flow restrictor
- Fan display
- Air display
- Radiometer gain (1000 / 250 / 50 / 10)
- Total Frames Shot
- Calibrated initial O2 % by vol
- Calibrated final O2 % by vol
- Initial CO2 % by vol
- Final CO2 % by vol
- Initial CO (ppm)
- Final CO (ppm)

The first five visible records are B1–B5, dated 19-Feb-2014, with PMMA films of differing nominal thicknesses and displayed O2 / CO2 / CO readings. The table includes missing or unusual-looking entries (for example, a blank final gas reading in some rows and an O2 final value of 1.6 in one displayed row). These must be checked against the source record and data dictionary; they must not be silently corrected or interpreted as physical truth.

## 4. Immediate data-model implications

The visible table already demonstrates that a single flat experiment table is insufficient for robust physical comparison.

### 4.1 Preserve display settings separately from physical quantities

`Fan display`, `Air display` and `Flow restrictor` appear to be instrument or apparatus settings. The landing page does not establish that they are calibrated physical airflow velocities.

**Rule:** Do not map these directly to m/s or cm/s without the engineering documentation, calibration relation and configuration context.

### 4.2 Separate sample identity from sample properties

`Fuel Sample Material` contains free-text descriptions with composition/material and dimensions combined (e.g. PMMA film, nominal thickness, width). These should be retained verbatim and parsed into proposed structured fields only with source provenance and review.

### 4.3 Gas measurements require measurement context

Initial/final O2 and CO2 and CO readings are not interchangeable with a continuous time series or local flame-zone measurements. FiF must capture:
- initial/final sampling time or protocol;
- sensor identity and calibration;
- sample location / gas volume context;
- units and basis;
- missing-value semantics;
- whether values are calibrated, reported or derived.

### 4.4 Experimental run identity needs reconciliation

The table includes Test # and Sample #. These are separate identifiers and must not be conflated. A run may relate to a sample, but the exact relationship and repeat-test structure must be confirmed from the data dictionary and files.

### 4.5 Imaging metadata is scientifically relevant

`Total Frames Shot` and radiometer gain are acquisition metadata, not flame-spread outcomes. They may be needed to interpret video-derived measurements and compare diagnostic quality. Video frame counts alone do not establish frame rate, calibration or temporal coverage.

## 5. Proposed first ingestion inventory

Before selecting the first outcome for MVP, obtain and inspect a representative, traceable subset:

1. PSI-25 investigation metadata and data dictionary / FAQ / README files, including version history.
2. One raw video corresponding to a table record with known Test # and Sample #.
3. Relevant engineering requirements and hardware documentation for the wind tunnel, fan, flow restrictor and diagnostics.
4. Any associated analyzed/reduced data for the same test, if available.
5. BASS-II Summary Report and relevant publications listed by NASA.

For each downloaded asset, record:
- exact PSI file path/name;
- source URL and retrieval timestamp;
- version / release context;
- file size and format;
- SHA-256 checksum;
- licence / usage notes;
- associated test and sample identifiers, if known;
- parser status and QC findings.

Do not assume the table's 130 rows map one-to-one to 130 raw videos or 130 complete experiments.

## 6. Candidate MVP outcome — not yet selected

Potential outcomes visible from BASS-II's stated objectives include ignition success, flame growth, flame spread and extinction limits. The first outcome must be selected only after the corresponding source files are verified for consistent definitions, units and sufficient experimental metadata.

A sensible initial investigation may be a narrow PMMA subset, because the visible table includes multiple nominal film thicknesses. This is only a candidate: the relevant flow, oxygen, geometry, ignition and measurement conditions must first be reconciled.

## 7. Risks and blockers

| Risk / blocker | Why it matters | Required evidence |
|---|---|---|
| Instrument display values mistaken for flow velocity | Invalid physical comparisons | Engineering calibration and operating documentation |
| Free-text sample descriptions | Incorrect material/geometry normalization | Sample inventory and source documentation |
| Missing or anomalous gas values | False assumptions about atmosphere or combustion products | Data dictionary, sensor protocol, original records |
| Test/sample identifiers misunderstood | Broken joins and provenance | PSI metadata and run logs |
| Video treated as quantitative data without calibration | Invalid flame metrics | Frame rate, scale calibration, camera geometry and synchronization |
| Dataset version changes ignored | Non-reproducible results | Version-specific inventory and checksums |

## 8. Audit conclusion

**BASS-II remains the recommended first evidence family for FiF, but ingestion design must now be driven by the actual PSI-25 data structures.**

The landing page confirms a useful experimental table, explicit material/flow/oxygen dimensions, a substantial supporting-file collection and a CC0-1.0 licence. It does not yet establish which raw measurements can be reliably extracted, whether all run-level metadata are complete, or which outcome is suitable for the first quantitative comparison.

### Next gate

Do not implement a numerical comparability or transferability score yet.

First complete the file-level inventory and inspect a matched set of:
- one table row;
- its raw asset(s);
- the corresponding engineering/configuration record;
- the relevant data dictionary or report.

Only after this join is verified should FiF define the first normalized experiment schema and MVP test case.
