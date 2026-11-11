# Dynamic dependency analysis

**Status:** research direction (DEC-060; restored after the dossier audit found it had disappeared without a decision). Not built and not claimed.

## Problem
Find which measured quantities move together in time during a burn (front position, flame area, radiometer, flow display) and in which direction influence runs, without assuming a physical model.

## Governing theory and assumptions
- **Measures:** Pearson and Spearman correlation, cross-correlation with lags, mutual information, transfer entropy, autoregressive models.
- **Significance:** every dependence is tested against surrogate series (phase-randomised, AAFT) that keep the spectrum and destroy the coupling.
- **Assumption that limits it:** the series must be stationary over the analysed window; a flow step breaks stationarity.

## Architecture and interfaces
- **Inputs:** time series sealed in the ledger with their clocks aligned (EXIF stills, overlay transcription, radiometer).
- **Outputs:** dependence estimates with surrogate p-values and the window used; a derivation entry in the ledger.

## Required data
Series longer than the current segments: a BASS-II segment has 10–34 stills, too few for mutual information or transfer entropy to be defensible (doc 26.1.1). The radiometer and flame-area series exist only as overlays or figures (ISS-014).

## Validation and falsification
Synthetic coupled systems with known coupling direction and strength; the method must recover them and must not report coupling on independent surrogates beyond the nominal rate.

## Feasibility gaps and blocking conditions
Series length; digitised radiometer and flame area (ISS-014); aligned clocks across instruments.
