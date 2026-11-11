# Dossier audit, G5a docs 26.1-26.1.3

Independent agent report, 2026-11-11 evening (brief: AUDIT_BRIEF.md in this folder). Ground truth: repository at that time.

# Audit: dossier files 26.1, 26.1.1, 26.1.2 and 26.1.3 against repo `/home/claude/fif` (HEAD 05f905a)

## 26.1. GFL Analiza 1 Etapa 2.md
Claude's first Stage-2 analysis, written 3–4 Nov. It covers a repo review, the PSI-25 feasibility check on all 129 table rows (verdict FEASIBLE WITH LIMITATIONS), the acquisition of the B6 archive and the calibration file, and a proposal to re-scope to Release A.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Limit FiF_Data to the 4 B3 files, the CSV and NASA/TM-20210011385 | data | superseded | DEC-016 (family anchor); 34 files acquired (GFL_MAP §2) | irrelevant |
| 2 | Acquisition phase does listing, hashing and metadata only; frame analysis waits for the quantitative phase | provenance | delivered | `data/manifests/PSI-25_acquisition_log.json` kept separate from `data/derived/` | nice |
| 3 | `.gitignore` rules for *.zip/*.mp4/raw data | provenance | delivered | `.gitignore` (FiF block); `tests/test_acquisition_tools.py::test_no_raw_media_committed` | important |
| 4 | At ingest, record exact PSI name, URL, date and SHA-256; never rename files | provenance | delivered | acquisition log; `src/gfl_ledger`; RES-003 (31/31 re-download identical) | critical |
| 5 | A stop criterion for the B3 ↔ §2.3 link, or change the case | governance | delivered | DEC-016 takes B3 off the critical path; ISS-025 (B3 partial burn); GFL_MAP §1 (B3 dropped 5 Nov, no DEC id) | important |
| 6 | Rule: check every PM request against the register | governance | not done | none found | nice |
| 7 | Feasibility check of all 129 rows; classify the 100-µm candidates; list the variations | data | delivered | `research/BASSII_PSI25_EXPERIMENTAL_TABLE_AUDIT_v0.1.md`; `tools/rank_comparable_runs.py`; `data/derived/BASSII_COMPARABLE_RUNS_v1.json` | important |
| 8 | Within-µg transferability test: V_f–flow relation fitted at one O₂ level, tested on held-out runs at another O₂, validity limit shown | analytics | not done | ISS-029 open (17 % runs untrackable); `capabilities.json` heldout = "designed". A substitute exists: cross-thickness ratio predictions (RES-037), not cross-O₂ | critical |
| 9 | 1g→µg transfer kept as documentary only, explicitly bounded | physics | delivered | RES-025; `docs/analysis/AR-001_LITERATURE_CROSSCHECK_v1.md` | important |
| 10 | Map video time to flow step (read the overlay) | data | delivered | `data/derived/B6/B9/B11/B13_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv` | important |
| 11 | Convert fan/air display to velocity using the calibration workbook | physics | not done | ISS-013 open; workbook never inspected (`research/BASSII_B6_EVIDENCE_GAPS…` GAP-B6-05) | critical (flow in cm/s at the sample is unknown) |
| 12 | Resolve the calibrated vs uncalibrated O₂ question for GMT50 | data | partial | `research/BASSII_O2_COLUMN_RECONCILIATION_2026-11-03.md`; ISS-012 open; moot since B1/B3 were rejected | nice |
| 13 | Acquire the calibration xlsx and the B6 original archive, with hashes | data | delivered | acquisition log, ledger | important |
| 14 | Release A pt 1: B6 measured from raw data with uncertainty, compared with Carmignani ~2 mm/s | analytics | delivered (provisional) | RES-001 → DEC-041 (1.99) → RES-033 (2.197, 1.915–2.368); AR-001 | critical |
| 15 | Release A pt 2: same measurement on B9, B15, B16, B19, B20 | analytics | partial | RES-002: 2 of 8 under the superseded rule set; under R-W3/R-W4 only B6 and B9 from the family (RES-035) | critical |
| 16 | The engine takes measured values next to source-reported ones; the UI shows limits | analytics | not done | METHODS §6: gate states are declared, not computed; config is still `configs/…RULESET_v0.1.json` | critical |
| 17 | CRAM-3 and anomaly detection only as "unvalidated" prototypes or research directions | analytics | documented only | `docs/specs/SPEC_cram.md`, `SPEC_anomaly_detection.md`; no code | important |
| 18 | Re-scope the MVP from 13 validated modules | governance | delivered | DEC-014, `docs/RELEASE_A_SCOPE_AND_ACCEPTANCE_v1.0.md` | important |
| 19 | Change roles: branch write access, owner approves PRs, ChatGPT reviews | governance | partial | DEC-015; DEC-024 (PR #6 merged without review) | nice |
| 20 | Check the Space Apps rules on work prepared beforehand, now | governance | partial | `docs/SPACE_APPS_2026_COMPLIANCE_CHECKLIST.md` (no item on prior work; owner's ruling given in chat only) | important |
| 21 | Freeze at 15 Nov 19:59 | governance | superseded | DEC-052 (freeze 15:00, submission before 19:59) | nice |

## 26.1.1. GFL Plan implementare v2.md
Claude's committed plan, 4 Nov. It has a 5-step calendar, the Release A module matrix with maturity targets (✅/🟡/📄), the 7-stage schedule and a stage-status snapshot.

**Calendar and stages**

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | 4–6 Nov: B6 front vs time from .ts, with uncertainty; difference from Carmignani reported | analytics | delivered (method changed to NEF stills, DEC-017) | AR-001; RES-001/033 | critical |
| 2 | 6–9 Nov: family of 5 more runs; V_f–flow relation; held-out runs; validity limit | analytics | not done | ISS-029, ISS-044; RES-002 (2/8) | critical |
| 3 | 9–11 Nov: engine and UI use measured values; abstention where data are insufficient | analytics / UI | partial | UI shows the measurements (`visualization/gfl.html`); the engine does not use them (METHODS §6) | critical |
| 4 | 12–13 Nov: independent audit, every demo claim backed by repo evidence | governance | partial (in progress) | RES-024, ISS-053; DEC-052 | critical |
| 5 | 14–15 Nov: competition package (video, slides, docs) | docs | not done (future) | none found | critical |
| 6 | Stage 5, MVP spec with per-module acceptance criteria (5 Nov) | docs | delivered | `docs/RELEASE_A_SCOPE_AND_ACCEPTANCE_v1.0.md` §3 | important |
| 7 | Stage 1, single *Concept & Scientific Foundation v1.0* (6 Nov) | docs | not done | GFL_MAP §2 (WP5 "partly met"; concept not consolidated) | important |
| 8 | Stage 2, NASA data catalogue of the 8-run family, media inventory, hashes (7 Nov) | data | delivered | `data/derived/BASSII_100UM_FAMILY_ASSETS_v0.1.csv`, `data/manifests/PSI-25_v4_manifest.json`, `PSI-25_NEF_archive_index.json` | important |
| 9 | Stage 3, physics framework: regimes, thin-fuel theory, validity domains, CRAM-1/2 (9 Nov) | physics | documented only | `research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md` (written before this plan); nothing computed | critical |
| 10 | Stage 4, architecture updated with the video pipeline and CRAM modules | docs | partial | METHODS_AND_VALIDATION_v1 §4 (pipeline); CRAM not in the architecture | nice |
| 11 | Stage 6, validation: B6 vs Carmignani, held-out test, independent audit | analytics | partial | RES-025 ("consistent, weakly"); RES-037 (ratio test, not the cross-O₂ test); ISS-053 | critical |
| 12 | Demo shows a ✅/🟡/📄 badge on every module | UI | partial | `visualization/data/capabilities.json` uses built/partial/designed ("built ≠ validated") rather than V/P/D, and some entries are stale (front says "one run (B6)") | important |
| 13 | Ruleset v0.2 with gates computed from data (stage-status remark) | physics | not done | no v0.2 config; model_validation gate still `fail` in v0.1 | critical |
| 14 | ChatGPT stays reviewer on PRs | governance | partial | DEC-015, DEC-024 | nice |

**Release A module matrix (every row)**

| Module | Target | Status vs target | Evidence | Criticality |
|---|---|---|---|---|
| NASA data intelligence (8-run family ingested: conditions, media, hashes, provenance) | ✅ | delivered | 695-file manifest; 34 files hashed; family asset index; NEF archive index. ISS-032: run-to-archive mapping for B19/B20 lost | important |
| Experiment comparison (8 runs, identical/different/unknown per condition) | ✅ | partial | `tools/rank_comparable_runs.py` ranks all 129 rows vs B6; cells cite the table row only, not every source (GFL_MAP) | important |
| Physics-based similarity (opposed-flow thin-fuel rules: regime, flow, O₂ with domain gates; engine extended) | ✅ | not done | METHODS §6; `capabilities.json` regime_gates = designed; `SPEC_regime_gates.md` | critical |
| Evidence-backed synthesis (deterministic text, LLM optional) | ✅ | partial | `tools/check_citations.py`, `tools/ai_second_check.py`; no deterministic narrative from the engine for a user question (GFL_MAP) | important |
| Interactive dashboard (family, measurements, transfer result) | ✅ | delivered (browser smoke-tested) | `visualization/gfl.html`, RES-023; family shown only partly; transfer section uses declared gates | important |
| FiF Advanced Analytics (video front position → spread rate; validated on B6 vs Carmignani) | ✅ | partial | the pipeline exists (`tools/flame_front.py`, `b6_window_rule.py`, `window_rule_r3/r4.py`) and runs on 4 runs. "Validated vs Carmignani" is not achievable: Carmignani gives no interval (RES-025). Headline changed 2.27 → 1.99 → 2.197 | critical |
| CRAM-1 Thermodynamics & transport (de Ris with literature PMMA properties) | 🟡 | not done | no code (grep "de Ris" in src/tools = 0); literature only (RES-025); GFL_MAP Q6 still asks for it | critical (needed to explain the P-B13 failure) |
| CRAM-2 Combustion regimes (radiative/thermal/kinetic on the V_f–flow curve) | ✅ / 🟡 | not done as a module | no classifier code. Observations only: B9/B6 ratio 0.91, exploratory thickness exponent −1.19 (RES-038, `tools/thickness_exponent.py`); ISS-026 says classify before pooling, not done | critical |
| CRAM-3 Nonlinear dynamics (flame-area oscillation, surrogate tests) | 🟡 | not done | `SPEC_cram.md` only | nice |
| Probabilistic anomaly detection (missing frames, time jumps, impossible values) | 🟡 | partial | QC gates inside the window rules plus planted anomalies in `tools/synth_flame_profiles.py`; no standalone detector; ISS-021 never used as a test case; `capabilities.json` = designed | important |
| Uncertainty quantification (scale, threshold, frame timing → V_f) | ✅ | partial | components reported separately (AR-001, rw4 files). ISS-050: interval misses the luminous-edge offset; pooled blind coverage 15/24; ISS-047 reference bias; scale ±3 % is an allowance, parallax unknown | critical |
| Advanced experiment transferability (V_f–flow at one O₂, held-out at another, validity limit) | ✅ | partial (different test) | cross-O₂ test not done (ISS-029). Cross-thickness ratio predictions instead: 1 supported, 1 not, 2 untestable (RES-037); RES-039 shows the verdicts depend on the front definition | critical |
| FiF Research & Control (reproducible configurable runs with provenance) | 🟡 | partial | scripts sealed with code hash in the ledger; no one-command rebuild (DEC-022 (1) not done) | important |
| 6 future research directions (credible spec each) | 📄 | delivered | 16 specs in `docs/specs/` | nice |

## 26.1.2. GFL Analiza Tehnica.md
Session log, 4 Nov. It covers the risk analysis, the literature search, the B6 usability check, opening up direct NASA access, the full manifest, the ruler scale, the first B6 measurement, DEC-018/019/020, the zero-trust ledger design and the family downloads.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Check that B6 is usable (time, overlay flow, front, scale) | data | delivered | ISS-013, ISS-018, ISS-020 rows | important |
| 2 | Fallback to published values labelled source_reported | provenance | delivered | `data/derived/BASSII_B6_SOURCE_VALUES_v0.1.csv`; AR-001 cross-check | important |
| 3 | Obtain the 3 Bhattacharjee 2016 papers | data | partial | Fire Saf. J. paper in the library (AR-001 S2); PCI and C&F papers not shown as acquired | important |
| 4 | Keep the PMMA rod family (Fernandez-Pello / Link 2015, 54 rates) as a documented plan B | data | not done | none found | nice |
| 5 | Full PSI-25 manifest (closes ISS-008) | data | delivered | `data/manifests/PSI-25_v4_manifest.json`; ISS-008 closed | important |
| 6 | Acquire 5 engineering/science docs; reconcile Test.Matrices.xlsx with the CSV | data | partial | acquired and hashed (acquisition log); reconciliation: none found | nice |
| 7 | Spatial scale from the deployed ruler; correct the ruler plane by cross-checking the 20-mm sample width | analytics | partial | `tools/ruler_scale.py`, ISS-020, ISS-027; plane correction not done (±3 % allowance, parallax "unknown") | critical |
| 8 | Sync stills and video on the same clock; resolve the 1-day date offset | data | delivered | ISS-018, ISS-022 | important |
| 9 | Primary source = top-view stills, video for overlay | analytics | delivered | DEC-017 | important |
| 10 | WP0 scope doc; WP1 `psi25_fetch.py`, family index, B15/B17 flag, no-media test, CI on feat/** | data / governance | delivered | `tools/psi25_fetch.py`, `tools/family_assets.py`, ISS-019, tests | important |
| 11 | B6 = 2.27 ± 0.09 mm/s with component budget | analytics | superseded | RES-001 → DEC-041 (1.99) → RES-033 (2.197) | critical |
| 12 | Claim: rate stays 2.1–2.4 while flow display rises 3→5, which "confirms the thermal regime" | physics | contradicted / unsupported | R-W2/R-W3 qualify only one B6 segment (display 3); RES-025 says thermal regime "plausible, not established" | critical |
| 13 | ISS-021 exposure spike becomes the first test case of the anomaly module | analytics | not done | ISS-021 still "candidate"; no detector | nice |
| 14 | DEC-018 minimum (a): tamper-evident chain, Ed25519, RFC 3161, `verify` | provenance | delivered | `src/gfl_ledger`, RES-004, `ledger/ledger.jsonl` (218 lines), `ledger/anchors/` | critical |
| 15 | DEC-018 (b): deviation register visible in the dashboard, each deviation with ≥2 sources and its blocked inferences | provenance / UI | delivered | register ISS rows; dashboard "Experiment memory" | critical |
| 16 | DEC-018 (c): explicit apples-vs-pears refusal with the reason shown | analytics | delivered | `src/fif_transfer/engine.py` (blocking gate named); ranking treats unknown as against | critical |
| 17 | Validated prediction (V): transfer model predicts V_f on held-out runs at another O₂, abstains out of domain | analytics | not done | ISS-029; RES-037 is a substitute (cross-thickness ratios) | critical |
| 18 | CRAM-1/2/3 and anomaly run on the verified store with maturity shown | analytics | not done | `capabilities.json` cram/anomaly = designed | critical |
| 19 | Every AI or analysis output enters the ledger as a derivation with input and method hashes | AI layer / provenance | partial | AI re-execution hashed (ISS-037); ISS-053: derivations seq 202–209 have no parent links | important |
| 20 | WP5: 7 canonical docs, old ones moved to `archive/` with a supersession note | docs | partial | GFL_MAP (WP5 "partly met"); `archive/` holds only `brand_v0` | important |
| 21 | Name GFL plus tagline; provisional logo, later vector redraw | other | delivered / superseded | DEC-020; logo replaced by DEC-026 (`archive/brand_v0/SUPERSEDED.md`) | nice |
| 22 | Dashboard: deviation map as graph nodes; measurements next to published values with error bars; click a point → NASA photo and its hash | UI | partial | B6 section and ledger present; `b6_series.json` has image IDs but one aggregate profile hash, so no per-point photo hash link was found | important |
| 23 | Breadth: other NASA families at catalogue level, level D | data | partial | `research/fixtures/NASA_FAMILIES_v1.json`, `visualization/data/families.json` (identified, not catalogued with data) | nice |
| 24 | Family NEF archives (6.5 GB) indexed and downloaded with hashes | data | delivered | `PSI-25_NEF_archive_index.json`; RES-003 | important |
| 25 | Per-session scale (ISS-023) and GMT50 clock correction (ISS-022) applied | analytics | delivered in RES-002 run | `data/derived/BASSII_100UM_MEASUREMENT_CONFIG_v0.1.json`; ISS-032: working directories and archive mapping lost | important |
| 26 | Classify runs by regime before pooling (CRAM-2, ISS-026) | analytics | not done | ISS-026 open | critical |
| 27 | Confirm B1/B3 partial burns on video and crew notes | data | partial | ISS-025 (video checked; crew logs not consulted) | nice |
| 28 | Explain the frame-count mismatch (B3 253/43, B15 122/74) | data | documented only | ISS-024 open | nice |

## 26.1.3. GFL Analiza Tehnica 2.md
Session log, 4 Nov evening. It covers the QC-gated family run, the external-credibility plan (DEC-022), the three pillars (DEC-023), the ledger as next package and the PR #6 merge discussion.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Family run with strict QC; failures marked rejected_qc with a reason, never given a number | analytics | delivered (then superseded by R-W3/R-W4) | RES-002, ISS-028, `tools/family_measure.py`, `data/derived/BASSII_100UM_SPREAD_RATES_v0.1.json` | important |
| 2 | B6 2.32 ± 0.10, B15 2.39 ± 0.10 mm/s | analytics | superseded | B15 never re-measured under R-W3/R-W4; ISS-032 (archive mapping lost) | important |
| 3 | B6 ≈ B15 at higher flow shows thermal-regime behaviour (an observation) | physics | not confirmed | B15 dropped from later work; B9/B6 0.91 is the only later flow-independence evidence (RES-035) | important |
| 4 | Colour-aware (blue-channel) front for the 17 % O₂ flames, to unblock the cross-O₂ test | analytics | not done | ISS-029 open; no colour code in tools | critical |
| 5 | DEC-022 (1): clean-room rebuild of everything from the manifest with one command | provenance | not done | only RES-003 (re-download) and RES-006 (B6 re-run); ISS-043 A8 | important |
| 6 | DEC-022 (2): independent re-check by a fresh agent plus ChatGPT, on raw data | governance | partial | RES-024 cold review, ISS-053 audit, WF-0011 blind analyses, red teams RES-005/008 | important |
| 7 | DEC-022 (3): pre-registered integrity checks on all of PSI-25 (129 tests, 695 files) | provenance / analytics | not done | ISS-043 A8; GFL_MAP ("breadth audit not done") | critical (the jury's "cherry-picked dataset" objection) |
| 8 | DEC-022 (3b): 1–2 more NASA investigations (SoFIE, SAFFIRE) at catalogue and integrity level | data | not done | DEC-048 defers SAFFIRE | nice |
| 9 | DEC-022 (4): wording rule ("sources disagree", never "NASA error") | governance | delivered | DEC-022; register phrasing | important |
| 10 | Three pillars; pillar 3 claims authenticity, not truth of the data | governance | delivered | DEC-023 | important |
| 11 | Ledger first (5–6 Nov), retroactive registration, `gfl verify` over everything | provenance | delivered | RES-004 (43 entries, FreeTSA anchor); now 211+ entries, 132 objects ok | critical |
| 12 | Dashboard with the challenge verbs: summarizes, ranks, interprets | UI / AI layer | partial | ranking + AI findings with citation check (DEC-046); "interpret" = declared-gate transfer section | critical |
| 13 | Merge PR #6 as a merge commit; declare the missing review as a deviation | governance | delivered | DEC-024 | nice |
| 14 | External confirmation from Bhattacharjee (email sent) | governance | not done | none found; DEC-045 (no external expert) | important |

## Cross-file findings
- **The analytics modules the files promised are missing as code.** CRAM-1 (de Ris), CRAM-2 (regime classifier), CRAM-3, the standalone anomaly detector and computed regime gates (ruleset v0.2) have no code in `src/` or `tools/`. Only specs exist (`docs/specs/SPEC_cram.md`, `SPEC_anomaly_detection.md`, `SPEC_regime_gates.md`). The dashboard itself labels them "designed" (`visualization/data/capabilities.json`). Three of these were Release A targets at ✅/🟡 in 26.1.1.
- **The thesis test promised in all four files was never run.** That test is: V_f–flow relation fitted at one O₂ level, checked on held-out runs at another O₂. It is blocked by ISS-029 (17 % flames not trackable) and nobody built the colour-aware front. What exists instead is a cross-thickness ratio test: 1 of 4 predictions supported (RES-037). RES-039 shows its verdicts depend on the front definition.
- **The family measurement covers less than claimed.** Of the 8-run 100-µm family, only B6 and B9 are measured under the current rules. B11 and B13 are other thicknesses. B15's 2.39 mm/s comes from the superseded RES-002 run, and the run-to-archive mapping for B19/B20 was lost (ISS-032).
- **The engine still does no physics.** 26.1.1's own diagnosis was that gates are declared, not computed, and v0.1 cannot return a positive validation. That is unchanged (METHODS §6, `configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json`). "Physics-based similarity ✅" and "Experiment comparison ✅" are not met.
- **The repo contradicts a scientific claim in 26.1.2.** It says B6's rate "stays 2.1–2.4 mm/s while flow rises 3→5, confirming the thermal regime". Under the fixed window rules only one B6 segment (display 3) qualifies, and RES-025 rates the thermal regime "plausible, not established". Separately, the B6 headline moved 2.27 → 1.99 → 2.197 mm/s, so the dossier's 2.27 ± 0.09 is obsolete and its ± understated. The current interval is 1.915–2.368, and ISS-050 shows the interval misses the luminous-edge offset.
- **"Validated vs Carmignani" can't be achieved as worded.** Carmignani gives about 2 mm/s with no interval or front definition, so the comparison can only be "consistent, weakly" (RES-025). The ✅ on FiF Advanced Analytics should be restated.
- **The flow axis has no physical units.** The calibration-workbook conversion (fan/air display → cm/s at the sample) was promised in 26.1 and never done (ISS-013 open). So every "rate vs flow" statement uses display units, which matters for any regime claim.
- **None of the DEC-022 robustness measures is done.** The one-command clean-room rebuild and the pre-registered breadth audit of all of PSI-25 are absent (ISS-043 A8). These were the answer to the jury's "you were lucky / you cherry-picked" objection.
- **Two contradictions between the documents and the repo:**
  - 26.1.1 first lists CRAM-1/2/3, anomaly detection and Research & Control as "outside Release A, research direction", then puts them in the Release A matrix at 🟡 or ✅. The repo follows the first reading in practice.
  - `capabilities.json` is out of date: it says the front measurement is "applied to one run (B6)", while GFL_MAP §6 says four runs. It also uses built/partial/designed rather than the promised V/P/D badges.
- **The integrity and deviation layer is the one area clearly delivered beyond plan.** That covers the ledger, RFC 3161 anchors, browser verification and the deviation register (DEC-018 minimum). One open defect: derivation entries seq 202–209 lack parent links (ISS-053), which is a small gap in the "every derivation names its parents" criterion.

No memory content was used beyond the project context.
