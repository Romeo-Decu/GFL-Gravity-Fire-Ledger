# Comparison with the official challenge data (pre-registered)

**Registered:** 2026-11-11 evening, before NASA publishes the Space Apps resources for "Flame in Freefall" (expected 13 Nov). **Decision:** DEC-058 (owner).

## Status of everything measured so far

Every GFL result obtained before the official resources are published is **open**: B6, B9, B11, B13 rates under R-W2, R-W3 and R-W4, the four predictions (RES-037), the post-protocol B11 result (RES-038), the thickness exponent and the AAL test results. They were computed from PSI-25 BASS-II files downloaded by GFL from the NASA PSI archive (DOI 10.60555/4qc4-de67), not from the files NASA designates for the challenge. None of them is final until the comparison below has run.

## Step 1: identity of the files (no analysis)

For every file in the official resources that corresponds to a file GFL already holds (same run, same kind), compare SHA-256 against the ingest entries in `ledger/ledger.jsonl`.

| Outcome | Consequence |
|---|---|
| identical bytes | the open results apply to the official data unchanged; status becomes "confirmed on official data", no re-run needed |
| same run, different bytes (other version, other processing, other format) | re-run the frozen rule on the official files without changing any parameter; report both results side by side, and the difference |
| run in official data that GFL does not hold | ingest, then run the frozen rules; no prediction is claimed for it after the fact |
| run GFL holds that is not in the official data | result stays as an open PSI-25 result, labelled as such |

## Step 2: what is frozen during the comparison

The window rules R-W3 and R-W4 as anchored, the prediction bands, the definitions and the interval method. A difference between official and PSI-25 results is a finding, not a reason to change a rule. If a rule change is still needed, it is declared, sealed and anchored before it runs, as R-W4 was.

## What is not claimed

Why NASA chose this challenge. The owner's working hypothesis (IDEA-047) is recorded as a hypothesis; it guides where we look, not what we report.
