# Advanced transferability: held-out validation

**Status:** designed. Blocked by data (see below).

## What we want
Fit a spread-rate versus flow relation at one oxygen level, then test it on runs at another oxygen level that were held out before fitting. Show where the relation stops being valid, and abstain outside that domain.

## Design
- **Split:** the hold-out split is fixed and signed in the ledger before any fit (pre-registration, as for the window rule DEC-040).
- **Model:** a physically motivated form from the thermal regime, plus an empirical alternative. Both are reported.
- **Validity limit:** the domain is defined by the regime gates. A prediction outside the domain returns "not transferable on current evidence".

## Validation
- Prediction error on held-out runs, with uncertainty.
- A refusal test: out-of-domain requests must abstain.

## Blocking conditions
- Today only B6 and B15 are measured, and both are being re-measured under the window rule (DEC-041).
- No second oxygen level is measured yet.
- The AIR display to cm/s mapping is open (ISS-013).
