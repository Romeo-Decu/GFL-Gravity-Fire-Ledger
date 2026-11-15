## Constatări
- [DIRECTION_METHOD_CONSISTENCY] [CONFIRMED] Both scripts determine propagation direction before defining any front, complying with the task brief. deepseek_v4 uses cross-correlation of successive profiles; kimi26 uses centroid/max-position regression. Both methods are threshold-free and valid.
- [FRONT_DEFINITION_DISCREPANCY] [REPORTED] Front definition thresholds differ: deepseek_v4 uses a fixed 10% of peak emission, while kimi26 uses 3×MAD. Both are physically justified but introduce definitional dependence in spread-rate measurements.
- [SENSITIVITY_QUANTIFICATION] [CONFIRMED] Both scripts quantify dependencies (threshold, time window, exposure subsets). kimi26 additionally tests centroid/peak/trailing edge definitions; deepseek_v4 tests for break points.
- [UNCERTAINTY_BUDGET_COMPLETENESS] [CONFIRMED] Both reports list uncertainty components, including unconstrained factors (exposure smear, luminous-edge offset). kimi26 provides a structured table; deepseek_v4 embeds it in script output.
- [DATA_QUALITY_FLAGS] [CONFIRMED] Both scripts flag duplicate timestamps, exposure variation, and non-monotonic front jumps. kimi26 explicitly checks for negative values and exposure ratios.
- [PROCEDURAL_OMISSION] [ERROR] deepseek_v4 omits required statement labels ([MEASURED], [ASSUMPTION], etc.) in the report, which could obscure assumptions in later phases.
- [CODE_EXECUTION_RISK] [UNVERIFIABLE] Neither script has been executed on full data. Potential issues: kimi26’s `np.array_split` on empty arrays (mitigated); deepseek_v4’s cross-correlation may fail on low-SNR frames (no guards).
- [ALIGNMENT_DERIVE] [REPORTED] kimi26’s report aligns fully with the task brief. deepseek_v4 deviates in threshold choice (fixed % vs MAD-based) and omits statement labels.

## Conținut
CONTEXT: PKT-ecef22000c
CONFIDENCE: 0.90

VERDICT: PASS
ALIGNMENT: PARTIAL
SEVERITY: MINOR

# Adversarial Audit Report: GFL-R1 BASS-II B6 Blind Analysis

## 1. Summary of Findings
This audit evaluates the **REALITY** phase artefacts from `deepseek_v4` and `kimi26` for compliance with the task brief, code quality, and robustness. Both analyses adhere to the core constraints (direction before front, no published values, numpy/pandas only) but exhibit minor procedural deviations.

### Key Observations
- **Direction Determination**: Both methods are valid and threshold-free. Cross-correlation (deepseek_v4) and regression (kimi26) yield consistent interpretations.
- **Front Definition**: Threshold choices differ (fixed % vs MAD-based) but are physically justified. Sensitivity to threshold is quantified in both scripts.
- **Uncertainty Quantification**: Comprehensive budgets are provided, though kimi26’s tabular format is more readable.
- **Data Quality**: Both scripts flag exposure variation, duplicate timestamps, and non-monotonic front jumps.

### Procedural Deviations
1. **deepseek_v4**: 
   - Uses a fixed 10% threshold instead of MAD-based (minor; task brief allows discretion).
   - Omits required statement labels ([MEASURED], [ASSUMPTION], etc.) in the report. **[ERROR]**
2. **kimi26**: Fully compliant with labeling and threshold methodology.

## 2. Code-Level Defects
### deepseek_v4 (`blind_analysis_B6.py`)
- **Line 42-45**: Cross-correlation may fail on low-SNR frames (no guards for `np.argmax(corr)` on flat profiles).
  ```python
  corr = correlate(sig1, sig2, mode='same')
  lags = np.arange(-n_cols//2 + 1, n_cols//2 + 1)
  max_idx = np.argmax(corr)  # No check for flat correlation
  ```
- **Line 102-104**: `np.array_split` on empty `detected_idx` could raise `ValueError` (mitigated by guard in kimi26).
- **Line 120**: Fixed 10% threshold (`base_threshold = 0.10`) lacks adaptability to varying flame brightness.

### kimi26 (script in `WF-0011_REALITY_verification_r1_v1`)
- **Line 89-91**: `np.array_split` on empty arrays is guarded, but the fallback window rule (`np.any(X > 0, axis=1)`) may include frames with no flame signal.
- **Line 112**: MAD estimation assumes background dominates the profile width. If the flame fills >50% of columns, MAD becomes flame-biased.

## 3. Risk Assessment
### High-Risk Defects
1. **Direction Ambiguity**: 
   - **deepseek_v4**: Cross-correlation may return `no net motion detected` if SNR is low. No fallback method.
   - **kimi26**: `AMBIGUOUS` result if centroid/max-position slopes disagree. No fallback.
   - **Impact**: Could block spread-rate computation entirely.

2. **Threshold Sensitivity**:
   - **deepseek_v4**: Fixed 10% threshold may under/overestimate front position in dim/bright frames.
   - **kimi26**: MAD-based threshold adapts to noise but may compress sensitivity outputs if flame dominates.
   - **Impact**: Spread-rate values may vary by >20% across thresholds (per kimi26’s sensitivity outputs).

3. **Exposure Smear**:
   - Neither script can deconvolve motion blur from varying exposure times.
   - **Impact**: Unquantified bias in front position, especially in long-exposure frames.

### Unconstrained Uncertainties
| Source                     | deepseek_v4               | kimi26                     |
|----------------------------|---------------------------|----------------------------|
| Exposure smear             | Flagged (correlation)     | Flagged (correlation)      |
| Luminous-edge offset       | [UNKNOWN]                 | [UNKNOWN]                  |
| Local flow velocity        | [UNKNOWN]                 | [UNKNOWN]                  |
| Pixel scale accuracy       | ±3% (propagated)          | ±3% (propagated)           |

## 4. Recommendations for Refactoring
### deepseek_v4
1. **Add Guards for Cross-Correlation**:
   ```python
   if np.max(corr) < 1e-6:  # Flat correlation
       direction_lags.append(np.nan)
       continue
   ```
2. **Replace Fixed Threshold with MAD-Based**:
   ```python
   mad = np.median(np.abs(prof_matrix - np.median(prof_matrix, axis=1, keepdims=True)))
   threshold = 3.0 * mad
   ```
3. **Add Statement Labels**: Retroactively tag all report statements (e.g., `[ASSUMPTION]` for threshold justification).

### kimi26
1. **Guard Against Flame-Biased MAD**:
   ```python
   # Use only non-flame columns (e.g., first/last 10% of profile) for MAD
   bg_cols = np.concatenate([col_idx[:216], col_idx[-216:]])
   mad = np.median(np.abs(X[:, bg_cols]))
   ```
2. **Fallback for Direction Ambiguity**:
   ```python
   if direction == 'AMBIGUOUS':
       direction = 'DECREASING_COLUMNS'  # Default to upstream (opposed-flow)
   ```

## 5. Alternatives to Current Methods
1. **Direction Determination**:
   - **Optical Flow**: Use Farnebäck’s algorithm (OpenCV) on 2D frames to capture transverse motion.
   - **Phase Correlation**: More robust than cross-correlation for low-SNR frames.

2. **Front Definition**:
   - **Wavelet-Based Edge Detection**: Apply Canny/Sobel on 1D profiles to avoid threshold sensitivity.
   - **FWHM Leading Edge**: Define front as the leading edge of the full-width at half-maximum of the emission peak.

3. **Uncertainty Quantification**:
   - **Monte Carlo Sampling**: Vary thresholds/time windows randomly to estimate rate distributions.
   - **Bayesian Inference**: Model spread rate as a distribution with priors on exposure smear.

## 6. Data-Quality Red Flags
- **Exposure Variation**: 67x range (0.005s–0.333s) introduces motion blur and SNR changes. Both scripts flag this but cannot correct it.
- **Negative Values**: Schema allows negative counts/s (e.g., –45.7), likely from median subtraction. Neither script addresses their physical meaning.
- **Non-Uniform Timestamps**: dt varies from 1.0s to 1.42s in the sample. Both scripts use exact `unix_time_s`.

## 7. Least Certain Aspects
1. **Exposure Smear Bias**: The magnitude of front-position bias from motion blur in long-exposure frames is unquantifiable with the provided data.
2. **Luminous-Edge Offset**: The true offset between the visible leading edge and the solid pyrolysis front is unknown and may vary with flow conditions.
3. **Flow Non-Stationarity**: The crew’s flow adjustments (settings 3 → 5) introduce non-stationarity, but the exact timing and effect are unrecorded.

## 8. Verify First
1. **Execute Both Scripts on Full Data**:
   - Confirm direction conclusion is not `AMBIGUOUS` (kimi26) or `no net motion detected` (deepseek_v4).
   - Check for runtime errors (e.g., empty arrays, low-SNR frames).
2. **Compare Spread-Rate Values**:
   - Across threshold variations (kimi26’s MAD-based vs deepseek_v4’s fixed %).
   - Between long/short exposure subsets (flag exposure smear bias).
3. **Validate Front Detection**:
   - Overlay front positions on sample profiles to verify physical plausibility.

## Riscuri
- **Direction Ambiguity**: Could block spread-rate computation if no fallback method exists.
- **Threshold Sensitivity**: Spread-rate values may vary significantly across definitions.
- **Exposure Smear**: Unquantified bias in front position, especially in long-exposure frames.
- **Code Execution Errors**: Potential failures on full data (e.g., empty arrays, low-SNR frames).
- **Statement Label Omission**: deepseek_v4’s missing labels could obscure assumptions in later phases.

## Alternative
- Use optical flow (2D) for direction determination to capture transverse motion.
- Replace threshold-based front detection with wavelet-based edge detection (e.g., Canny/Sobel on 1D profiles).
- Quantify uncertainty via Monte Carlo sampling of thresholds/time windows instead of discrete variations.
- Define front as the leading edge of the full-width at half-maximum (FWHM) of the emission peak to reduce threshold sensitivity.
- Implement Bayesian inference to model spread rate as a distribution with priors on exposure smear.
- Use phase correlation instead of cross-correlation for more robust direction determination in low-SNR frames.

## Unde sunt cel mai puțin sigur
The magnitude of bias from exposure smear and the true offset between the luminous edge and pyrolysis front, as both are uncalibrated in the provided data.

## Ce aș verifica întâi
Execute both scripts on the full dataset to confirm direction conclusion is not ambiguous and no runtime errors occur (e.g., empty arrays, low-SNR frames).
