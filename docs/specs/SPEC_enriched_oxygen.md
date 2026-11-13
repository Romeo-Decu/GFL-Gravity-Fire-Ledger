# Enriched-oxygen atmospheres

**Status:** specified, not built (DEC-071). GFL is not a fire-prediction or safety-certification tool (DEC-013).

## Problem
Exploration vehicles and habitats are planned with lower pressure and a higher oxygen fraction than the ISS (about 34 % oxygen at 56.5 kPa is the commonly cited exploration atmosphere). Most of the flight evidence GFL has measured is at 21 % and 17 % oxygen at one atmosphere. The question: which existing NASA results may inform an enriched-oxygen cabin, and which may not.

## Design
- **Atmosphere as a gate with numbers:** oxygen fraction and pressure of each run from NASA's tables, replacing the record-level label "air / reduced / enriched" of the evidence map.
- **Per material:** the oxygen range over which a rate was measured, and the gap to the target atmosphere, shown as a gap and never extrapolated across.
- **Sources:** PSI-25 and PSI-26 (BASS, BASS-II), PSI-98 to PSI-102 (Saffire), and normal-gravity limiting-oxygen tests where NASA publishes them.

## Required data
Run-level tables of the investigations above; the evidence map (built) says which records state an atmosphere at all.

## Validation
A held-out test: predict the direction of change of the spread rate between two measured oxygen levels before measuring the second. No statement outside the measured oxygen range.

## Blocking conditions
Flight data at the exploration atmosphere are scarce; dim near-limit flames are not measurable under the frozen rule (ISS-029, B16).
