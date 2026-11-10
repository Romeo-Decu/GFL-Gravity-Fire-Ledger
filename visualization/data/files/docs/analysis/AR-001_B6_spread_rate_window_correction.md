# AR-001 — B6 flame-spread rate: from a hand-chosen window to a slope-independent rule

| Field | Value |
|---|---|
| Analysis record | AR-001 |
| Date | 2026-11-10 |
| Author | Claude (GFL project manager and engineer) |
| Approval | Romeo Decu, Team Owner (DEC-041, 2026-11-10), approved in the project conversation; not yet signed with the owner key |
| Register | DEC-040, DEC-041, RES-017…RES-022, ISS-042 (§22–23) |
| Status | Adopted; provisional qualifiers in the ledger |
| Supersedes | RES-001 as the B6 headline (ledger supersession, entry seq 100) |

Labels: **[VERIFIED]** executed and reproduced by GFL from primary data; **[REPORTED BY SOURCE]** stated by a source and not measured by GFL; **[INFERENCE]** reasoning from verified facts; **[UNKNOWN]** not constrained by available data.

## 1. Summary
GFL's first B6 result, 2.274 ± 0.094 mm/s (RES-001), was obtained on a fit window (13–53 s) chosen by hand, across changes in opposed flow, with an independent-errors standard error. Two independent AI red teams (grok-4.7, GPT-5.5) challenged exactly these three points in AAL workflow WF-0011. A deterministic re-execution then showed that the 3× gap between the blind analyses and GFL came entirely from frame selection (RES-019).

This record replaces the hand-chosen window with a rule built only from frame properties that do not use the front's time trend, fixed in Git before any per-segment rate was computed. That is not a pre-registration: RES-001 and RES-019 were known, the committed selection file already lists each frame's front position, and the rule, the selection and the first fits were committed minutes apart by the same author (an AI, Claude). Under that rule B6 supports **one flow-specific rate: 1.99 mm/s at AIR display 3 (18.5–28.6 s)**, with a stated budget by component [VERIFIED]. The value is stable across 60 variants of the rule's own choices (1.88–2.07 mm/s) [VERIFIED]. It is lower than RES-001 by about the size of the flow-mixing effect [INFERENCE].

## 2. Background and question
- **Data.** NASA PSI-25 BASS-II test B6: 100 µm PMMA, opposed-flow spread on the ISS, 77 NEF raw stills (14-bit) with EXIF time and exposure, plus the side-view video with an on-screen overlay [REPORTED BY SOURCE].
- **RES-001 (2026-11-04):** leading edge at absolute radiance thresholds, OLS over 13–53 s, 40 frames: 2.21 / 2.27 / 2.34 mm/s; ±0.094 mm/s from the fit [VERIFIED].
- **Known issues before this record:**
  - flame radiance rises ×6.3 inside the window and the leading ramp sharpens from 8.8 to 4.0 mm (RES-007, RES-008);
  - the overlay's AIR display changes inside the window (RES-007);
  - residual lag-1 autocorrelation ≈ 0.8.
- **Challenge (WF-0011, RES-017/018):** "Is 13–53 s justified or chosen? ±0.094 is not a budget."
- **Re-execution (RES-019):** the same front definition gives 0.61 mm/s on all 77 frames and 2.12 on 13–53 s; the blind analysts' numbers were the all-frames number [VERIFIED].

**Question.** Which B6 rate can be defended without choosing the window by looking at the slope, and with what uncertainty?

## 3. Method
### 3.1 Rule R-W1 (docs/B6_WINDOW_RULE_v1.md), fixed before any rate
Per-frame gates, none of which uses the front's trend:

| Gate | Criterion |
|---|---|
| G1 flame present | band-profile peak > 20 × robust noise (1.4826 × MAD) |
| G2 front inside field | leading edge (5 % of frame peak) ≥ 50 half-size columns from both image edges |
| G3 no flame clipping | raw saturated pixels in the band ≤ 10 × run median (hot pixels ≈ 20–35, constant) |
| G4 continuity | ≤ 5 s since the previous frame; cumulative after the first gap |
| G5 flow guard | > 3 s from any AIR-display change (overlay sampled every 3 s) |

- **Segments:** one rate per constant-AIR segment; a segment is fitted only with ≥ 6 frames over ≥ 6 s.
- **Estimators:** OLS and Theil–Sen on eight front definitions:
  - relative leading edge at 0.05, 0.1, 0.2 and 0.5 of the frame's own peak;
  - absolute thresholds 2e5, 5e5 and 1e6 counts/s;
  - peak position.
- **Reference definition:** relative 0.1. It is brightness-invariant (RES-007) and was used by both GFL and the blind deepseek_v4 analysis (RES-019).
- **Uncertainty:**
  - Newey–West HAC with lag ⌈1.5 n^(1/3)⌉;
  - moving-block bootstrap (block length = lag, 4000 resamples, seed 20261110);
  - budget components reported separately, never added in quadrature as if random.

### 3.2 Evidence of order
| Step | Commit | Content |
|---|---|---|
| Rule + selection R-W1 | a986d4a | rule doc, tool, per-frame gates; no slope computed |
| R-W2 + selection | 41d1578 | segmentation fix only (§4.1); no slope computed |
| Fits R-W1 and R-W2 | 33842e2 | first per-segment rates |
| Re-check and adoption | 5d3f5c7 | robustness grid, supersession of RES-001 |

### 3.3 Deviation R-W2 (declared before any rate)
- **What went wrong:** R-W1 built segments from *consecutive* usable frames, so the single clipped frame at 26.57 s split the AIR 3 interval into 8 + 2 frames.
- **Change:** a segment is the set of usable frames between two AIR changes. Gates and thresholds are unchanged.
- **Reporting:** both versions are reported (§5).

## 4. Results
### 4.1 Selection [VERIFIED]
- **Usable frames:** 22 of 77.
- **Failing G3 (flame clipping):**
  - 5.4–17.5 s, the ignition and early brightening;
  - 26.57 s;
  - 51.6–66.6 s.
- **Failing G4:** after the 106 s gap (from 179.0 s), so the 6 post-burn stills drop out.

| AIR display | Usable frames | Span | Fitted |
|---|---|---|---|
| 3 | 10 (R-W2) / 8 (R-W1) | 18.5–28.6 s | yes |
| 4 | 6 | 35.6–40.6 s (5.0 s) | no (span < 6 s) |
| 5 | 4 | 47.6–50.6 s | no |
| 7 | 2 | 68.9–70.2 s | no |

### 4.2 Rates, AIR display 3 [VERIFIED]
| Definition | R-W2 OLS (mm/s) | Theil–Sen | R² | lag-1 autocorr. | 95 % block bootstrap | R-W1 OLS |
|---|---|---|---|---|---|---|
| relative 0.05 | 2.052 | 2.064 | 0.9993 | −0.20 | 1.96–2.11 | 2.024 |
| **relative 0.1 (reference)** | **1.989** | 1.973 | 0.9974 | 0.46 | **1.84–2.13** | 1.881 |
| relative 0.2 | 2.060 | 2.041 | 0.9980 | 0.43 | 1.86–2.18 | 1.973 |
| relative 0.5 | 2.197 | 2.194 | 0.9984 | 0.16 | 1.95–2.30 | 2.143 |
| absolute 2e5 | 2.255 | 2.041 | 0.9869 | 0.53 | 1.85–2.68 | 1.961 |
| absolute 5e5 | 2.334 | 2.313 | 0.9931 | 0.53 | 1.88–2.63 | 2.134 |
| absolute 1e6 | 2.543 | 2.507 | 0.9900 | 0.30 | 1.99–2.96 | 2.306 |
| peak position | 2.321 | 2.283 | 0.9955 | 0.28 | 2.09–2.61 | 2.217 |

### 4.3 Robustness of the rule's own choices [VERIFIED]
- **Grid:** clipping factor {5, 10, 20, off} × flow guard {2, 3, 4} s × overlay clock shift {−2 … +2} s = 60 variants, all fittable, nothing selected from the grid.
- **Result:** reference rate 1.88–2.07 mm/s, median 2.00.
- **With no clipping gate:** 20 frames from about 8 s, and the rate stays at 2.00–2.07.

### 4.4 Cross-checks [VERIFIED]
- **Inputs:** NEF-derived profiles equal the blind WF-0011 profiles within 2 × 10⁻⁴ relative.
- **Old window from the new inputs:** the 13–53 s reference rate from NEF is 2.1202, identical to RES-019.
- **Interval check:** the HAC t-interval with 8 degrees of freedom is 1.90–2.08, inside the bootstrap interval. The wider bootstrap interval is the one reported.

### 4.5 Uncertainty budget (headline)
| Component | Value | Status |
|---|---|---|
| Statistical (block bootstrap, 95 %) | 1.84–2.13 mm/s | [VERIFIED] computation; approximate, because it rests on 10 correlated frames with blocks of 4. The HAC t-interval is 1.90–2.08 |
| Front definition, relative | 1.99–2.20 mm/s | [VERIFIED]; systematic, from edge sharpening (RES-008) |
| Front definition, absolute (and peak position 2.32) | 2.26–2.54 mm/s | [VERIFIED]; also depends on EXIF exposure accuracy |
| Rule choices | 1.88–2.07 mm/s | [VERIFIED]; 60 variants but 20 distinct rates (clipping limits 5–20× select the same frames); segment minimums and the flame and edge gates were not varied |
| Spatial scale | ±3 % (±0.06 mm/s) | allowance, not a measurement: the ruler lies behind the sample plane (ISS-020 open) |
| Ruler-plane vs sample-plane parallax | — | [UNKNOWN] |
| Luminous edge vs pyrolysis front | — | [UNKNOWN] |
| AIR display → cm/s | — | [UNKNOWN] (ISS-013) |

## 5. Discussion
1. **Why the new value is lower than RES-001.** The 13–53 s window joined the AIR 3 interval with later frames that are brighter and at higher AIR settings. On those frames the relative edge moves faster: 2.12 for 13–53 s against 1.99 for AIR 3 [VERIFIED]. The 0.13 mm/s difference is the flow and brightening mix, not a contradiction [INFERENCE].
2. **Why within-segment errors are better behaved.** Lag-1 autocorrelation falls from ≈ 0.8 (13–53 s) to −0.2…+0.46 inside AIR 3 [VERIFIED]. The structured residuals came from mixing regimes [INFERENCE].
3. **What B6 cannot give.** A rate-versus-flow trend. AIR 4 and AIR 5 do not reach the segment minimum, and flame clipping removes 51.6–66.6 s [VERIFIED]. Any trend would need either the video, which has higher cadence but different optics, or a looser rule fixed in advance and applied to new data.
4. **Secondary union (all usable frames).** It is contaminated: the last two usable frames have the front stalled at the end of the sample (columns 1816–1847, stationary from about 61 s), and no gate covers burn-out (ISS-042) [VERIFIED]. Adding that gate now would be a change made after seeing results, so it is left for R-W3 on the next run, and the union is not used.
5. **Comparison with published values.** None is used to choose or validate the method. Agreement with the order of magnitude of published B6 values, if any, would be reported only after matching the comparator's own conditions (DEC-032 note).

## 6. Consequences
- **Headline:** RES-001 is superseded as headline and kept as history (DEC-041).
- **Family rates:** RES-002 (B6 2.32, B15 2.39 mm/s) used the pre-rule windows and iid errors. They are qualified as superseded method, to be re-measured once each run's overlay is transcribed.
- **Withdrawn:** the observation "B6 ≈ B15 despite higher B15 flow".
- **Wording corrected:** the earlier "3 → 5 cm/s" stated more than is known. The display-to-velocity mapping is open (ISS-013).

## 7. Reproduction
```
python tools/b6_window_rule.py select --rule R-W2 --nef-dir <B6_NEF> \
  --overlay data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv --out data/derived/B6_WINDOW_SELECTION_v2.json
python tools/b6_window_rule.py fit --nef-dir <B6_NEF> \
  --selection data/derived/B6_WINDOW_SELECTION_v2.json --out data/derived/B6_SEGMENT_RATES_v2.json
python tools/b6_window_robustness.py --nef-dir <B6_NEF> \
  --overlay data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv \
  --blind-profiles <B6_band_profiles.csv> --out data/derived/B6_WINDOW_ROBUSTNESS_v1.json
```

| Artefact | SHA-256 (prefix) | Ledger seq |
|---|---|---|
| data/derived/B6_WINDOW_SELECTION_v1.json | dd87d74943ff7d5a | 93 |
| data/derived/B6_SEGMENT_RATES_v1.json | 1398d2ddb9fa6d93 | 94 (qualified 95) |
| data/derived/B6_WINDOW_SELECTION_v2.json | 11a38a8ca83c7673 | 96 |
| data/derived/B6_SEGMENT_RATES_v2.json | dcddc395a40b9bc6 | 97; supersession 100 (qualified 101) |
| data/derived/B6_WINDOW_ROBUSTNESS_v1.json | 1b2012fa5b643546 | 99 |
| tools/b6_window_rule.py | 337ad416759c096e | in method of 93–98 |
| tools/b6_window_robustness.py | 54718be6928900cd | in method of 99 |

Raw NEF bytes are not in Git; their SHA-256 values are in the ledger and are checked on every run.
Unit tests: `tests/test_b6_window_rule.py` (5 tests).

## 8. Lessons
1. **A window chosen by eye is a hidden parameter.** It must be a rule, written down and committed before the numbers it produces are seen.
2. **One number across changing conditions is not a measurement of one thing.** Segment by the physical condition (here the flow) before fitting.
3. **A fit standard error is not an uncertainty budget.** Check residual structure, use autocorrelation-aware intervals, and list systematic components separately.
4. **Independent critics are useful only with re-execution behind them.** The red teams named the problem; the deterministic re-execution settled it (RES-019). The AI auditor without re-execution got it wrong (RES-014, RES-018).
5. **Declare a rule change even when it happens before the results** (R-W2). The record of what changed and why is what makes the result checkable.

## 9. Review notes (independent review, 2026-11-10)
An independent reviewer (a separate AI agent with no access to how the analysis was produced) found that the earlier version of this record and the dashboard presented the result more favourably than the analysis supports. Specifically:
- the reference rate is the lowest of the eight definitions;
- the full definition range reaches 2.54 mm/s;
- the robustness grid has 20 distinct rates, not 60;
- the statistical interval rests on 10 frames;
- the scale figure is an allowance;
- the result is provisional.

These are now stated here and on the page.
