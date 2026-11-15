# Probabilistic anomaly detection (data quality)

**Status:** built (DEC-060, RES-046): `src/gfl_analysis/anomaly.py` checks records, frames and the flow overlay with declared thresholds; scored on synthetic planted anomalies (all detectable ones found, no false flags) and run on the NASA table. A probabilistic version with calibrated false-alarm rates needs labelled data and is not built.

## What we want
Every data stream is scanned for faults before analysis, and each fault is recorded:
- frame gaps;
- clock jumps;
- duplicated timestamps;
- impossible values;
- exposure steps;
- sensor clipping;
- metadata that contradicts the files.

## Design
- **Detectors per signal:**
  - change-point detection on exposure and brightness;
  - gap statistics on timestamps;
  - a saturation census on raw sensor values;
  - schema checks against the source tables.
- **Output:** an anomaly entry in the ledger, with its location, the detector, its parameters and the affected downstream results.
- **No calibrated probabilities are claimed** until a fault-injection study measures detection rates.

## Validation
- Fault injection on copies of real data: inserted gaps, shifted clocks and clipped frames must be detected.
- The false-alarm rate is reported.

## Blocking conditions
- Ground truth for real anomalies is scarce; detection rates must come from injection studies.
