# GFL methods and validation v1

**Release:** NASA Space Apps 2026 (Release A) · **Date:** 2026-11-10 · **Author:** Claude (PM), for team CCTI · **Status:** draft for owner review (ISS-043 A8)

This document states how GFL produces each output, how each part is checked, and what is not validated. Each section points to the code and to the register records (RES, DEC, ISS) that hold the evidence. A claim in this document with no pointer should be treated as unsupported.

## 1. Scope

GFL answers three separate questions about microgravity combustion evidence: relevance (does a source address the question), comparability (are the governing conditions characterised well enough) and transferability (can a finding inform another context, within which limits). Release A delivers these on one NASA investigation in depth, BASS-II (PSI-25, DOI 10.60555/4qc4-de67), with four runs measured from raw data (B6, B9, B11, B13) and the analysis modules in `src/gfl_analysis`. The other NASA combustion families are identified and kept separate, not pooled (`research/fixtures/NASA_FAMILIES_v1.json`). Ignition and extinction are outside the measured result (DEC-048).

### 1.1 Why GFL does not model chemical kinetics (a deliberate limit, DEC-059)

In opposed-flow spread over a thin solid, three regimes are distinguished by the opposing-flow speed (de Ris 1969; Bhattacharjee et al. 2016, in the project library):

- **Thermal regime** (intermediate flow). The gas-phase reaction is fast compared with the residence time of gas near the flame leading edge (Damköhler number large), so the spread rate is set by heat transfer from the flame to the unburnt fuel. The thin-fuel solution depends on gas conductivity, flame and vaporisation temperatures, and on the fuel's density, specific heat and thickness, and not on the reaction rate or the flow speed.
- **Kinetic regime** (high flow). The residence time shortens until finite-rate chemistry slows the flame; the rate falls with flow and the flame blows off.
- **Radiative regime** (very low flow, reachable only in microgravity). Radiative loss from the flame and the surface becomes comparable with the heat release; the rate falls and the flame quenches.

The runs GFL measures are intended to sit in the thermal regime, and the evidence so far is consistent with it: B9 and B6 (both 100 µm, different air displays) give the same rate within 9 % (RES-035), and the rate scales close to inverse thickness (exponent −1.19, 95 % interval −1.53 to −0.85; RES-038, exploratory). In that regime a kinetic model would add parameters that the measured rate cannot constrain. Chemistry matters near the limits: at blow-off (kinetic) and at low-flow quenching (radiative; B11 at air display 0 is slower, which may indicate the approach to it).

GFL therefore does not model kinetics. Its job is to **say which regime a run is in**, so that a finding from the thermal regime is not transferred to a case near a limit, where chemistry decides. That is the role of the regime classifier (CRAM-2, `docs/specs/SPEC_regime_gates.md`). Its present limit is stated: the Damköhler number needs the flow speed at the sample, which the air display does not give until the fan calibration is applied (ISS-013). Until then a run's regime is reported as evidence for or against the thermal regime, never as a computed classification.

## 2. Data acquisition and provenance

| Step | Method | Code / record |
|---|---|---|
| Inventory | PSI-25 Version 4 file list retrieved from the PSI file service: 695 files with sizes | `data/manifests/PSI-25_v4_manifest.json` |
| Acquisition | 31 files (7.1 GiB) downloaded into `FIF_DATA`, outside Git; SHA-256 recorded; re-downloaded later with 31/31 identical hashes | `tools/psi25_fetch.py`, `data/manifests/PSI-25_acquisition_log.json`, `PSI-25_reacquisition_check_2026-11-05.json` |
| Experimental table | NASA's BASS-II table, 129 data rows (the PSI page states 130; ISS-009 open), sealed as a tier-2 source table | ledger entry for `Experimental table/PSI-25_Experimental table_BASS-II.csv` |
| Joins | File-to-run and filename-to-table joins are flagged when unverified, never corrected silently | `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md` |
| Secondary sources | Values from reports, papers and dissertations are kept as source-reported, with locators, and never relabelled as GFL measurements | `research/*_EXTRACTION_*`, `*_AUDIT_*` |

## 3. Signed ledger

Every ingest, derivation, supersession, qualification, anchor and approval is one entry in `ledger/ledger.jsonl`. An entry's hash is SHA-256 of its canonical JSON (sorted keys, no whitespace, UTF-8) without the hash and signature; the signature is Ed25519 over that hash; each entry names the previous entry's hash. Two keys with separate roles: the pipeline key signs processing entries and cannot sign approvals; the owner's key, held offline by the owner, signs approvals only (DEC-031). The chain head is anchored in Git commits and RFC 3161 timestamps (FreeTSA). Entries are never edited: a changed file is sealed again by a supersession entry, and a doubt by a qualification entry (approximate, provisional, manual, declared, secondary_source, code_not_committed, unresolved_mapping, systematic_effect_open).

Verification recomputes every hash, link and signature and re-hashes every sealed file that is present; an absent file is reported as missing, never as verified (ISS-030). The same verification runs in Python (`python -m gfl_ledger verify`) and in the visitor's browser (`visualization/src/ledger-verify.js`, WebCrypto Ed25519), and the page re-hashes each data file it displays against its latest seal.

## 4. B6 flame-spread measurement

Full record: `docs/analysis/AR-001_B6_spread_rate_window_correction.md`; rule: `docs/B6_WINDOW_RULE_v1.md`.

1. **Images.** 77 top-view NEF raw stills (14-bit), decoded linearly without gamma (RES-008). Time from EXIF sub-second stamps; exposure from EXIF.
2. **Radiance.** Linear demosaiced values (gamma 1, no auto-brightening) divided by exposure time (counts/s), so auto-exposure does not masquerade as dimming or brightening; this rests on EXIF exposure accuracy, stated as a qualifier.
3. **Profile.** Mean over the sample band (rows 655–1016 of the half-size image) per column.
4. **Front definitions.** Eight: leading edge at 0.05, 0.1, 0.2 and 0.5 of each frame's own peak; absolute thresholds 2e5, 5e5 and 1e6 counts/s; peak position. Reference: 0.1 of peak, brightness-invariant. The spread between definitions is reported as a systematic effect of the sharpening flame edge (RES-008), not as noise.
5. **Scale.** 14.7 px/mm from the ruler; ±3 % allowance because the ruler lies behind the sample plane (ISS-020).
6. **Window rule (R-W2).** Per-frame gates that do not use the front's time trend (flame present, front inside the field, no flame clipping, continuity, ±3 s from airflow-display changes read from the video overlay); one rate per constant-flow segment with at least 6 frames over at least 6 s. Written and committed before any per-segment rate was computed; not a pre-registration, because earlier results were known (AR-001 §1).
7. **Estimators.** OLS and Theil–Sen; Newey–West HAC standard errors with lag ⌈1.5 n^(1/3)⌉; moving-block bootstrap, 4000 resamples, seed 20261110.
8. **Robustness.** The rule's own choices varied in a full grid (60 variants, 20 distinct rates); nothing selected from it (RES-022).

**Result.** One segment qualifies (air display 3 cm/s, 18.5–28.6 s, 10 frames): 1.99 mm/s; statistical 95 % 1.84–2.13 (bootstrap, approximate) and 1.90–2.08 (HAC t); definitions 1.99–2.54; rule variants 1.88–2.07; scale ±3 %; parallax, luminous-edge to pyrolysis offset and flow speed at the sample unknown. Status: provisional. The earlier 2.274 ± 0.094 mm/s (hand-chosen window) is superseded and kept (RES-001).

## 5. Comparable-run ranking

`tools/rank_comparable_runs.py` parses each row of the sealed BASS-II table (material, geometry, thickness, width, flow restrictor, air display sequence, calibrated initial O₂) and compares it with the reference run, dimension by dimension: match, differs, or unknown. Unknown never counts as a match. Levels: not comparable (material or geometry differs or is unknown), same recorded conditions, close (one dimension differs, none unknown), distant. The table's seal is checked before ranking. The ranking compares what the table records; conditions it does not record (flow speed at the sample, sample history, ignition energy) are listed as outside the comparison.

## 6. Transfer engine

`src/fif_transfer` applies a versioned ruleset (`configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json`) to a case and an inference profile (documentary summary, qualitative mechanism, quantitative transfer, model calibration, model validation). Each physical gate is pass, fail, unknown or not applicable; a failed or unknown critical gate blocks the conclusion and is named. For PMMA-100 the gate states are declared from the source audit, not yet computed from measured data; computing them is the designed next step (`docs/specs/SPEC_regime_gates.md`).

## 7. AI in the method

**Roles.** Claude was project manager and engineer: it wrote the code, the window rule, the analyses and this document, and holds the pipeline key (`docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md` §7). Other models worked in separate roles, coordinated through AAL, the team's own local-first system for governed multi-model analysis over MCP and API: blind analysts who never saw GFL's result, red teams, and an adversarial auditor (WF-0011).

**Controls.**
- Blind packages contain data and task only, with hashes (`blind_B6`, `blind_api_B6`).
- AI-written code is re-executed by GFL in a fresh directory with only hash-verified inputs, an empty environment and `python -I`; outputs are hashed into the ledger (ISS-037).
- AI claims are ranked by what re-execution and the data showed, not by model confidence (`research/fixtures/AI_FINDINGS_v1.json`).
- Summaries of findings must pass `tools/check_citations.py`: every sentence cites register records, every cited record exists, every number appears in a cited record. A second model can read each sentence against its cited records (`tools/ai_second_check.py`); its answers are evidence about the summaries, not about the physics.
- The read-only MCP server (`src/gfl_mcp`) lets an AI client query the memory, records, ledger, run ranking and transfer engine; answers name their sources.

**Known AI failures, kept as records:** a blind table not produced by its own code (RES-009), a sign error and false "measured" labels (RES-012), false audit certifications (RES-014, RES-016), fabricated line references (RES-018), and a human comment that reached an agent's packet (ISS-041).

## 8. Validation

| What | How | Where |
|---|---|---|
| Software correctness | 117 automated tests (pytest) on Python 3.10–3.13; dashboard contract tests; browser tests in Chromium and Firefox | `.github/workflows/tests.yml`, `tests/`, `visualization/tests/` |
| Ledger integrity | Full verification on every CI run and in every visitor's browser | `gfl_ledger verify`, `ledger-verify.js` |
| Reproduction | B6 result reproduced byte-identically from a fresh re-download (RES-006); NEF profiles equal the blind analysts' profiles to 2 × 10⁻⁴ (RES-022); RES-001 reproduced exactly from blind profiles (RES-019) | register |
| Independent analysis | Blind AI analyses re-executed; the 3× discrepancy explained entirely by frame selection (RES-019) | register |
| Literature | Magnitude consistent with NASA/TM-20210011385, Bhattacharjee et al. 2016 and Carmignani 2019; regime plausible, not established; flow label conflicts between sources (RES-025) | `docs/analysis/AR-001_LITERATURE_CROSSCHECK_v1.md` |
| Prediction | B11 rate predicted at 0.85–1.15 mm/s before acquisition, timestamped (DEC-047) | register, ledger anchors |

**Not validated.** No external human expert has reviewed the physics (DEC-045). The B6 result rests on one run and one flow segment of 10 frames. The flow speed at the sample, the ruler-to-sample parallax and the luminous-edge to pyrolysis offset are unknown. The transfer engine's gate states are declared, not computed. Software tests check the code, not the combustion physics.

## 9. Reproduction

```bash
python -m pytest -q tests
PYTHONPATH=src python -m gfl_ledger verify --allow-missing
python tools/rank_comparable_runs.py --table "$FIF_DATA/Experimental table/PSI-25_Experimental table_BASS-II.csv" --out /tmp/rank.json
python tools/b6_window_rule.py select --rule R-W2 --nef-dir <B6_NEF> ...   # see AR-001 §7
```

Raw NASA files are fetched with `tools/psi25_fetch.py`; their hashes are in the ledger, and `verify` checks them wherever they are present.
