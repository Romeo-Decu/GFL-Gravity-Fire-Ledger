# Sensor integration

**Status:** research direction (DEC-010). Not built.

## Problem
Ingest new measurement streams with full provenance, through the same vault and ledger:
- cameras (visible, IR);
- radiometers;
- gas analysers;
- anemometers.

## Design
- **Each stream** has an instrument record: model, calibration, clock, resolution. The record is sealed as tier 1 with its raw output.
- **Time alignment:** explicit offsets with uncertainty, never assumed (lesson from ISS-018, ISS-022).
- **Volumetric diagnostics** (from the v4 proposal) are not assumed. A stream is accepted only with a demonstrated, synchronised measurement.

## Validation
Synthetic streams with injected clock offsets and calibration errors must be detected; real streams are reconciled with existing NASA records.

## Blocking conditions
Hardware access; calibration data; synchronisation evidence.
