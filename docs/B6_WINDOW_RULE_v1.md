# B6 fit-window rule v1 (R-W1)

**Status:** fixed on 2026-11-10, committed **before** any per-segment slope was computed.
**Honest scope:** this is *not* a true pre-registration of the B6 result. RES-001 (2.274 mm/s on 13–53 s) and RES-019 were already known when the rule was written. What the rule does guarantee is narrower and checkable:
1. every criterion is computed from per-frame properties that do **not** use the front's time trend (no slope, no residual, no fit quality);
2. the per-flow-segment rates, which nobody has computed before, are produced by a rule frozen in Git before the first of them was calculated (commit order is the evidence).

Answers RT objections (grok47, gpt55; RES-017, RES-018): the 13–53 s window was chosen by hand; the flow changes inside it; ±0.094 mm/s is a fit standard error, not a budget.

## Inputs
- 77 NEF raw stills of B6 (14-bit, linear demosaic, half size), EXIF time and exposure (`tools/flame_front.py` conventions).
- Band: half-size rows 655–1016 inclusive (code slice 655:1017), band-averaged relative radiance per column.
- On-screen overlay transcription `data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv` (AIR display, sampled every 3 s, still-time estimate = video time + 1 s). Status: source-displayed, FiF-transcribed.

## Per-frame gates (a frame is usable only if all pass)
| Gate | Criterion | Why |
|---|---|---|
| G1 flame present | band-profile peak > 20 × robust noise (1.4826 × MAD of the profile) | no front can be defined without a flame |
| G2 front inside field | leading edge (5 % of frame peak) at least 50 half-size columns (≈3.4 mm) from both image edges | an edge at the border is truncated, not measured |
| G3 no flame clipping | raw saturated pixels in the band ≤ 10 × the median count over all frames (hot pixels are ~20–35, constant) | clipped flame flattens the peak and shifts relative thresholds |
| G4 continuity | time since previous frame ≤ 5 s | removes the 106 s gap and the post-burn stills after it |
| G5 flow guard | not within ±3 s of an AIR-display change (transcription cadence 3 s, sync uncertainty ≈1 s) | the rate depends on opposed flow; transitions mix regimes |

## Segments
- Consecutive usable frames with the same AIR display value form a **flow segment**.
- A segment is fitted only if it has **≥ 6 frames spanning ≥ 6 s**; shorter segments are reported, not fitted.
- **Primary result:** one rate per flow segment. A single "B6 rate" across segments is not reported as primary, because the opposed flow differs between them.
- **Continuity view (secondary):** the union of usable frames, fitted once, for comparison with RES-001 only.

## Estimators and uncertainty (fixed now)
- Front definitions, all reported: leading edge at 0.05 / 0.1 / 0.2 / 0.5 of the frame's own peak; absolute 2e5 / 5e5 / 1e6 counts/s; peak position. Direction: increasing columns (RES-001, RES-019).
- Rate: OLS slope and Theil–Sen slope.
- Statistical uncertainty: Newey–West (HAC) standard error with lag L = ⌈1.5 · n^(1/3)⌉, and moving-block bootstrap (block length L, 4000 resamples, fixed seed 20261110), 68 % and 95 % intervals.
- Budget, reported as separate components, never added in quadrature as if random:
  - statistical (above);
  - front definition: range across the definitions above (a systematic that follows from edge sharpening, RES-008);
  - spatial scale: ±3 % (ruler, RES-002);
  - parallax between the ruler plane and the sample plane: [UNKNOWN];
  - luminous edge vs pyrolysis front offset: [UNKNOWN];
  - EXIF exposure accuracy: qualifier (relative thresholds do not depend on it; absolute thresholds do).

## Not allowed after this commit
Changing a gate, threshold, guard or segment rule because of the rates it produces. Any change becomes R-W2, with the reason, and both versions are reported.
