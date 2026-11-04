# FiF — Release A Scope, Maturity Levels and Acceptance Criteria v1.0

**Date:** 2026-11-04
**Status:** Accepted by the Project Owner (2026-11-04). Controls the NASA Space Apps 2026 deliverable.
**Supersedes for Release A:** the "all 13 modules implemented" reading of DEC-009. DEC-009 remains the long-term product target.
**Deadline control:** submission closes Sun 15 Nov 2026 23:59 local; internal freeze target **Sun 15 Nov 19:59** (4 h reserve).

## 1. Decisions

| ID | Decision |
|---|---|
| DEC-014 | Release A ships every module of the traceability matrix with an explicit, displayed maturity level: **V** = implemented and validated on NASA data; **P** = implemented, bounded prototype, labelled "not validated"; **D** = documented research direction only. No module is presented above its evidenced level. |
| DEC-015 | Roles for Release A: Project Owner approves every merge to `main`. Claude implements on feature branches and opens PRs. ChatGPT reviews PRs and scientific claims; it does not coordinate implementation. Raw NASA bytes never enter Git. |
| DEC-016 | Scientific anchor = the BASS-II nominal 100-µm, 20-mm PMMA family (B1, B3, B6, B9, B15, B16, B19, B20; three O₂ levels by session). B6 is the method-validation case (FiF measurement vs. Carmignani 2019 and NASA/TM-20210011385). B3 remains in the family; the B3 ↔ Section 2.3 join (DEC-008) is no longer on the critical path. |
| DEC-018 | **Minimum success condition = the integrity and deviation layer** (Project Owner's founding principle: analyses on uncertain or non-comparable data are worthless, so FiF must first prove deviations). Release A must demonstrate (1) tamper-evident provenance: every raw byte and every derivation hashed and chained to its source, any alteration detected; (2) a visible deviation register: each conflict with its sources, why it matters and which inferences it blocks; (3) explicit refusal of non-comparable ("apples vs. pears") comparisons with the reason shown. B6 measurement and the family transfer test are **stretch evidence** ("prove more"); FiF re-measuring a published value is itself a deviation check. | Accepted |
| DEC-017 | Measurement primary source = top-view still sequence (≈1 s cadence, per-image timestamps, same clock as the video overlay); side-view video (29.97 fps) supplies overlay AIR/FAN/RAD values and continuous position where scale allows. |

## 2. Minimum success condition (DEC-018)

| Capability | Acceptance criterion | Seed evidence already found (2026-11-04) |
|---|---|---|
| Tamper-evident provenance (zero-trust: not even an administrator can alter data undetected) | Append-only ledger: every ingest, extraction, derivation and AI/analysis output is an entry carrying the previous entry's hash and an Ed25519 signature of the producing process; chain head anchored externally (Git commit + RFC 3161 timestamp); `fif verify` recomputes every hash, signature and link and fails on any alteration; every derived value names its parent hashes and method. Claim wording: tamper-evident, not tamper-proof. | PSI-25 manifest + acquisition log (9 + 1 files, hashes reproduced by independent routes) |
| Deviation register | Every deviation lists ≥ 2 source locators, the affected inferences and its status; shown in the dashboard and in the graph | ISS-019 TESTB15 files carry sample 175 (table: B17); ISS-013 three B6 flow representations; ISS-018 one-day display date offset; ISS-012 secondary source drops calibrated/uncalibrated O₂ distinction; R03 2.2 mm/s not joinable to B3 |
| Non-comparability refusal | Engine returns `undetermined` / `not_transferable` with the blocking dimension named whenever a required dimension is unknown or conflicting (existing engine behaviour, extended to computed gates) | 67 existing engine/contract tests |

## 3. Module maturity targets

| Module | Release A deliverable | Target | Acceptance criterion |
|---|---|---|---|
| NASA data intelligence | PSI-25 full manifest; 100-µm family asset index; reproducible fetch with SHA-256 | V | Manifest = 695 files / 255.77 GiB as published; every acquired byte hashed and size-matched; filename↔table joins flagged, never corrected |
| Experiment comparison | Family table: matching / differing / unknown conditions per run | V | Every condition cell carries source + evidence status; unknown ≠ compatible (tested) |
| Physics-based similarity | Thin-fuel opposed-flow regime gates computed from data (ruleset v0.2) | V | Gates derived from measured/source values with rule IDs; abstains when inputs missing |
| Evidence-backed synthesis | Deterministic narrative from engine output; LLM optional, never source of truth | V | Every sentence maps to evidence refs; abstention text tested |
| Interactive dashboard | Existing explorer extended with family, measurements and transfer result | V | Browser smoke tests; maturity badge on every module |
| FiF Advanced Analytics | Flame-front tracking → spread rate with uncertainty | V | B6 reproduced against published ≈2 mm/s within declared uncertainty, or discrepancy reported with cause |
| CRAM-1 Thermodynamic & transport | de Ris thin-fuel thermal-regime comparison using literature PMMA properties | P | Units/dimension tests; property provenance; labelled not validated |
| CRAM-2 Combustion regime | Radiative / thermal / kinetic classification on the measured V_f–flow curve | V if family spans regimes, else P | Classification rules traceable to Bhattacharjee framework; counterexample tests |
| CRAM-3 Nonlinear dynamics | Flame-area/position oscillation analysis with surrogate tests | P | Synthetic-signal verification; surrogate significance reported |
| Probabilistic anomaly detection | Data-quality anomalies (frame gaps, clock jumps, impossible values) | P | Synthetic fault injection detected; no calibrated-probability claim |
| Uncertainty quantification | Scale, timing, threshold and fit components propagated to V_f | V | Components reported separately per VIDEO_MEASUREMENT protocol §4 |
| Advanced experiment transferability | V_f–flow relation fitted at one O₂ level, tested on held-out runs at another; validity limit shown | V | Holdout split fixed before fitting; out-of-domain cases abstain |
| FiF Research & Control | Reproducible, parameterised analysis runs with provenance manifest | P | Same inputs → identical outputs; no actuation |
| Future research (6 items) | Technical specification per §17.2 of the roadmap | D | Each spec lists data, theory, validation and blocking conditions |

## 4. Schedule

| Window | Work package | Exit evidence |
|---|---|---|
| 4–6 Nov | WP0 scope (this file); WP1 acquisition; WP2 B6 measurement | B6 V_f with uncertainty and comparison record |
| 6–9 Nov | WP3 family measurement + transfer holdout + CRAM-1/2 | Family table; holdout result; regime classification |
| 9–11 Nov | WP4 ruleset v0.2, engine integration, dashboard, CRAM-3/anomaly prototypes | End-to-end run reproducible from manifest |
| 12–13 Nov | Independent review (ChatGPT + fresh agent), remediation, demo freeze | Every demo claim mapped to repository evidence |
| 14–15 Nov | Competition package; upload rehearsal on 14 Nov | Final package ready by 15 Nov 19:59 |

## 5. Data policy

Raw PSI bytes live under `FIF_DATA` (default `~/FiF_Data`, outside the repository). Git holds only manifests, hashes, acquisition logs, derived numeric tables and code. `.gitignore` and `tests/test_acquisition_tools.py` enforce this.
