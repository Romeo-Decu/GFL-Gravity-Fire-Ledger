# FiF — Video Measurement Protocol and Uncertainty Framework v0.1

**Date:** 2026-11-04  
**Status:** Proposed analysis protocol; not yet applied to B3 assets  
**Target:** 100-µm PMMA, BASS-II / normal-gravity downward comparison  
**Purpose:** Define what FiF must verify before it reports a flame-spread rate from video.

## 1. Evidence boundary

This document defines a reproducible FiF procedure. It does not claim that FiF has processed the B3 video or reproduced NASA's published values.

Three kinds of statements must remain distinct:

1. **NASA-reported:** what NASA/TM-20210011385 says about its apparatus, image analysis, results, and uncertainty.
2. **Method literature:** what the 2017 image-analysis paper establishes about video-based flame-spread measurement and imaging parameters.
3. **FiF-proposed:** the checks, calculations, sensitivity tests, and acceptance rules defined here.

The NASA report describes its own Flame Analyzer workflow. Bhattacharjee et al. (2017) describe a MATLAB-based **Flame Image Analyzer (FIA)** method and an imaging-error framework. Similarity of purpose and research group does not prove that the implementations, settings, or analysis outputs are identical. FiF must not merge these software identities without source evidence.

## 2. Measurement model

Let:

- (n) = frame index;
- (t_n) = acquisition time associated with frame (n), in seconds;
- (x_n) = tracked leading-edge position, in pixels;
- (p) = spatial resolution, in pixels/mm;
- (f) = frame rate, in frames/s, only where constant acquisition cadence is verified;
- (b) = fitted leading-edge displacement, in pixels/frame.

For verified constant frame cadence, a linear fit of (x_n) against frame index gives slope (b), and:

\[
V_f = \frac{b f}{p}
\]

where (V_f) is flame-spread rate in mm/s.

For nonuniform frame times, generated still-image videos, or variable-frame-rate files, FiF must not infer acquisition timing from the video container's nominal FPS. It must use verified per-frame acquisition timestamps or a documented frame interval. In that case, fit physical position against acquisition time:

\[
x_{mm}(t_n) = \frac{x_n-x_0}{p}, \qquad
V_f = \frac{d x_{mm}}{dt}
\]

If acquisition timing cannot be established, report a spatial trajectory against frame index only; do not report mm/s as a measured quantity.

## 3. Imaging parameters and the non-dimensional imaging parameter

Bhattacharjee et al. (2017), *Measurement of instantaneous flame spread rate over solid fuels using image analysis*, identify frame rate and spatial resolution as the two most important imaging parameters controlling spread-rate measurement error and temporal resolution. The paper proposes:

\[
\varphi = \frac{f}{p V_f}
\]

with (f) in frames/s, (p) in pixels/mm, and (V_f) in mm/s.

FiF will record φ as a diagnostic descriptor when all three inputs are known. It is not, by itself, an uncertainty estimate or a universal acceptance threshold. The numerical criterion must be taken from the paper's applicable analysis and the actual measurement regime, not invented by FiF.

Reference: Bhattacharjee, S., Carmignani, L., Celniker, G., and Rhoades, B. (2017), *Fire Safety Journal*, 91, 123–129. DOI: https://doi.org/10.1016/j.firesaf.2017.03.039.

## 4. Uncertainty decomposition

For the constant-cadence expression (V_f = bf/p), and assuming independent input uncertainties as a first-order approximation:

\[
\left(\frac{u(V_f)}{V_f}\right)^2
\approx
\left(\frac{u(b)}{b}\right)^2
+
\left(\frac{u(f)}{f}\right)^2
+
\left(\frac{u(p)}{p}\right)^2
\]

This is a FiF propagation model, not a quoted NASA uncertainty formula. If inputs are correlated, covariance terms must be included. The calculation must state whether each component is a standard uncertainty, expanded uncertainty, repeatability estimate, or bounded sensitivity.

FiF must keep at least these components separate:

| Component | Meaning | Evidence required |
|---|---|---|
| Spatial calibration | Uncertainty in pixels/mm | Scale target, known dimensions, calibration image, lens/perspective assessment |
| Timing | Uncertainty in acquisition time or frame interval | Original timestamps, camera metadata, acquisition log |
| Front localization | Ambiguity in the leading-edge position | Image quality, threshold/filter choice, tracking definition |
| Regression | Uncertainty in fitted position-time slope | Number and distribution of points, residuals, fit interval |
| Processing sensitivity | Dependence on threshold, ROI, filtering, edge definition | Repeated analysis under predeclared alternatives |
| Physical variability | Real flame unsteadiness or changing regime | Time history and repeat tests where available |

Do not collapse these into a single percentage before their provenance and statistical meaning are clear.

## 5. Physical variability is not measurement error

A flame may accelerate, decelerate, pulsate, or transition between regimes. Such changes are physical behavior, not automatically noise.

FiF must distinguish:

- **measurement uncertainty:** uncertainty in locating and timing the front;
- **fit uncertainty:** uncertainty in the estimated slope over a stated interval;
- **temporal variation:** changes in the actual spread rate during the experiment;
- **between-test variability:** differences among nominally repeated experiments.

A single global linear fit is justified only for an interval where the position-time relation is adequately linear for the stated purpose. If residuals show systematic curvature or change points, FiF must not conceal this by reporting only one average rate. Report interval-specific rates or a time-dependent trajectory, with the segmentation rule disclosed.

## 6. Leading-edge definition and threshold sensitivity

The leading edge must have an operational definition appropriate to the camera view and experiment. “Brightest pixel”, “first pixel above threshold”, and “width-averaged intensity crossing” are not interchangeable definitions.

NASA/TM-20210011385 describes a width-averaged intensity threshold for its analysis. Its report mentions:
- threshold 30 in the separate Section 2.2.4 extinction study;
- threshold 70 for the illustrated 75-µm downward-spread example in Figure 2.18;
- no numerical threshold in the text for the target 100-µm Section 2.3 comparison.

Neither 30 nor 70 is established as the original threshold for the target 100-µm comparison.

FiF procedure:
1. Recover NASA's original setting if possible from code, configuration, video annotation, or a linked analysis record.
2. If unrecoverable, state that the original threshold is unknown.
3. Define a physically interpretable threshold range from image inspection, not by selecting the value that best reproduces 2.0 or 2.2 mm/s.
4. Re-track the same video across the predeclared threshold range and any justified ROI/filter alternatives.
5. Quantify how the estimated slope and front trajectory change.
6. Report the selected reconstruction settings and sensitivity envelope separately from NASA's result.

A constant spatial offset in front location can leave a fitted slope unchanged. A threshold-dependent offset that changes over time can bias the slope. FiF must therefore test trajectory and slope sensitivity, not merely compare one frame.

## 7. Video and source-file integrity checks

Before image processing, record:

- original file name and source path;
- archive name and SHA-256;
- archive member path and uncompressed size;
- file SHA-256 after extraction;
- container, codec, dimensions, color format and bit depth;
- nominal FPS and actual frame timestamps;
- frame count and duration;
- evidence of frame duplication, dropped frames, resampling, or conversion;
- camera/view orientation and whether the source is original camera footage, still-image sequence, or derivative video.

For still-image sequences converted to video, the container FPS may be an export setting rather than the original experiment sampling rate. Do not treat it as acquisition cadence without corroboration.

Original assets must remain immutable. All converted, cropped, stabilized, or annotated files are derivatives with their own hashes and transformation records.

## 8. Calibration and geometry checks

Before converting pixels to millimetres:

1. Identify a scale reference visible in the same imaging plane as the flame front, or a traceable calibration record.
2. Verify whether the scale is applicable to the entire tracked region.
3. Assess perspective, camera angle, lens distortion, and sample-plane alignment.
4. Confirm the propagation axis and image-coordinate sign convention.
5. Document any crop, rotation, stabilization, or perspective correction.
6. If scale varies across the image, use a spatial calibration function rather than one global pixels/mm value.

The 6-mm reference dots shown in NASA Figure 2.18 belong to that illustrated downward-spread example. They must not be assumed to calibrate B3 or another video.

## 9. FiF minimum analysis output

For every analysed video, FiF must produce:

1. immutable source-file identity and hash;
2. verified timing basis and frame map;
3. calibration record and uncertainty;
4. declared leading-edge definition;
5. frame-by-frame or sampled front coordinates;
6. position-time plot;
7. fit interval and regression method;
8. residual diagnostics;
9. mean or interval-specific spread rate, with uncertainty components;
10. threshold/ROI/filter sensitivity results;
11. explicit exclusions and reasons;
12. source links and a machine-readable processing manifest.

The output must distinguish a **reconstructed FiF estimate** from a **NASA-reported value**.

## 10. Acceptance gates for the B3 case

No quantitative comparison against NASA's Section 2.3 result is accepted until:

- the asset is linked to the relevant experiment/test/sample, not just named B3 by filename;
- acquisition timing is established;
- spatial calibration is traceable;
- the leading-edge definition is reproducible;
- threshold and processing sensitivity are reported;
- the fit interval is justified;
- the 2 cm/s Appendix A.1 versus 3 cm/s Section 2.3 flow discrepancy is either resolved or explicitly carried as an unresolved condition;
- the oxygen and pressure records used for the comparison are identified with calibration status;
- a corresponding normal-gravity record is identified at run level.

If one or more critical gates fail, the output state is **insufficient evidence for quantitative reproduction**. FiF may still present a qualified qualitative observation if the underlying image evidence supports it.

## 11. NASA-reported uncertainty versus FiF uncertainty

NASA reports less than 5% spread-rate uncertainty away from ignition and reproducibility within 5% for 5-second propagation averages in the target comparison discussion. These are source-reported statements about NASA's analysis.

FiF must not:
- adopt 5% as its own uncertainty by default;
- claim reproduction merely because a FiF estimate falls within 5% of a NASA value;
- compare estimates without matching the time interval, physical conditions, measurement definition, and uncertainty meaning.

A valid reproduction requires traceable inputs and an independently implemented measurement chain. Agreement is meaningful only after the data linkage and comparability gates pass.

## 12. Current status

- Protocol: defined in this document.
- B3 original video ZIP: downloaded by the user locally, but not accessible to the assistant's current runtime.
- Archive member inventory and hashes: not yet measured.
- Frame timing and spatial calibration: unknown.
- Original 100-µm Section 2.3 threshold: unknown.
- Independent B3 spread-rate reconstruction: not performed.
- Normal-gravity run-level video linkage: unresolved.

**Decision:** implement no numerical result and no transferability claim from video until the required source and measurement gates pass.
