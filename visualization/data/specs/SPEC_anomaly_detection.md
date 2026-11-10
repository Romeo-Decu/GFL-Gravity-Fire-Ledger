# Probabilistic anomaly detection (data quality)

**Status:** designed. Rule-based checks already run inside the measurement (gates G1–G5 of the window rule); a general detector is not built.

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
