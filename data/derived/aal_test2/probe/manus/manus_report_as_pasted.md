Completed entirely in the cloud sandbox. The rerun reproduced the captured stdout byte-for-byte.

Artifacts:

- [Complete unchanged code — analyze_t2.py](/home/ubuntu/manus_package_test2/analyze_t2.py)
- [Printed output — printed_output.txt](/home/ubuntu/manus_package_test2/printed_output.txt)

## Complete code run

```python
import numpy as np
import pandas as pd

SCALE_COLUMNS_PER_MM = 14.7
SMOOTH_WINDOW = 9
LAG_LIMIT = 100
BOOTSTRAPS = 20000
SEED = 20261111

CASES = {
    "T1": (3, 5.5, 32.5),
    "T2": (3, 5.5, 32.5),
    "T3": (2, 263.7, 290.7),
    "T4": (3, 5.5, 32.5),
}


def profile_columns(df):
    return [c for c in df.columns if c.startswith("c") and c[1:].isdigit()]


def lag_between(a, b):
    a = a - np.mean(a)
    b = b - np.mean(b)
    values = []
    for lag in range(-LAG_LIMIT, LAG_LIMIT + 1):
        if lag >= 0:
            u = a[:-lag or None]
            v = b[lag:]
        else:
            u = a[-lag:]
            v = b[:lag or None]
        denom = np.sqrt(np.dot(u, u) * np.dot(v, v))
        values.append(np.dot(u, v) / denom if denom else np.nan)
    return int(np.nanargmax(values) - LAG_LIMIT)


def front_column(profile):
    kernel = np.ones(SMOOTH_WINDOW) / SMOOTH_WINDOW
    smooth = np.convolve(profile, kernel, mode="same")
    gradient = np.gradient(smooth)
    peak = int(np.argmax(smooth[50:-50]) + 50)
    lo = peak + 20
    hi = min(peak + 500, len(profile) - 2)
    edge = int(lo + np.argmin(gradient[lo:hi]))
    if edge <= 0 or edge >= len(profile) - 1:
        return float(edge)
    y0, y1, y2 = gradient[edge - 1], gradient[edge], gradient[edge + 1]
    denominator = y0 - 2.0 * y1 + y2
    correction = 0.5 * (y0 - y2) / denominator if denominator != 0 else 0.0
    return float(edge + correction)


def ols_slope(t, x):
    tc = t - np.mean(t)
    xc = x - np.mean(x)
    return float(np.dot(tc, xc) / np.dot(tc, tc))


def bootstrap_ci(t, x, rng):
    n = len(t)
    slopes = np.empty(BOOTSTRAPS)
    for j in range(BOOTSTRAPS):
        idx = rng.integers(0, n, size=n)
        slopes[j] = ols_slope(t[idx], x[idx])
    lo, hi = np.percentile(slopes, [2.5, 97.5])
    return float(lo), float(hi)


print("METHOD direction=median_consecutive_profile_cross_correlation")
print("METHOD front=9_column_smoothed_strongest_falling_gradient_after_luminous_peak")
print("METHOD fit=ordinary_least_squares_front_column_on_recorded_time")
print("METHOD ci95=20000_pair_bootstrap_resamples_percentiles")
print("CALIBRATION columns_per_mm=14.7")

rng = np.random.default_rng(SEED)
for case, (display, interval_start, interval_end) in CASES.items():
    metadata = pd.read_csv(f"{case}_frames_metadata.csv")
    profiles = pd.read_csv(f"{case}_band_profiles.csv")
    columns = profile_columns(profiles)
    x_all = profiles[columns].to_numpy(dtype=float)
    t_all = metadata["t_s"].to_numpy(dtype=float)

    interval = (t_all >= interval_start) & (t_all < interval_end)
    indices = np.flatnonzero(interval)
    selected_profiles = x_all[indices]
    selected_times = t_all[indices]
    selected_edges = np.array([front_column(row) for row in selected_profiles])

    lags = np.array([
        lag_between(selected_profiles[j - 1], selected_profiles[j])
        for j in range(1, len(selected_profiles))
    ], dtype=int)
    median_lag = float(np.median(lags))
    direction = "increasing" if median_lag > 0 else "decreasing"

    slope_columns_per_s = ols_slope(selected_times, selected_edges)
    slope_mm_per_s = slope_columns_per_s / SCALE_COLUMNS_PER_MM
    ci_columns_per_s = bootstrap_ci(selected_times, selected_edges, rng)
    ci_mm_per_s = (ci_columns_per_s[0] / SCALE_COLUMNS_PER_MM,
                   ci_columns_per_s[1] / SCALE_COLUMNS_PER_MM)
    fitted = np.mean(selected_edges) + slope_columns_per_s * (selected_times - np.mean(selected_times))
    residuals = selected_edges - fitted
    rmse_columns = float(np.sqrt(np.mean(residuals ** 2)))
    max_gap_s = float(np.max(np.diff(selected_times))) if len(selected_times) > 1 else 0.0
    exposure_max_s = float(np.max(metadata.loc[indices, "exposure_s"]))

    print(
        f"DIAGNOSTIC {case} display={display} interval_start_s={interval_start:.6f} "
        f"interval_end_s={interval_end:.6f} frames={len(indices)} "
        f"median_lag_columns={median_lag:.6f} edge_rmse_columns={rmse_columns:.6f} "
        f"max_frame_gap_s={max_gap_s:.6f} max_exposure_s={exposure_max_s:.6f} "
        f"slope_columns_s={slope_columns_per_s:.9f}"
    )
    print(
        f"RESULT {case} speed_mm_s={slope_mm_per_s:.9f} "
        f"ci95_low={ci_mm_per_s[0]:.9f} ci95_high={ci_mm_per_s[1]:.9f} "
        f"direction={direction}"
    )
```

## Printed output, unchanged

```text
METHOD direction=median_consecutive_profile_cross_correlation
METHOD front=9_column_smoothed_strongest_falling_gradient_after_luminous_peak
METHOD fit=ordinary_least_squares_front_column_on_recorded_time
METHOD ci95=20000_pair_bootstrap_resamples_percentiles
CALIBRATION columns_per_mm=14.7
DIAGNOSTIC T1 display=3 interval_start_s=5.500000 interval_end_s=32.500000 frames=27 median_lag_columns=38.000000 edge_rmse_columns=6.501770 max_frame_gap_s=1.070000 max_exposure_s=0.016000 slope_columns_s=38.407865872
RESULT T1 speed_mm_s=2.612779991 ci95_low=2.594490912 ci95_high=2.634802788 direction=increasing
DIAGNOSTIC T2 display=3 interval_start_s=5.500000 interval_end_s=32.500000 frames=27 median_lag_columns=38.000000 edge_rmse_columns=6.473193 max_frame_gap_s=1.070000 max_exposure_s=0.005000 slope_columns_s=38.027865959
RESULT T2 speed_mm_s=2.586929657 ci95_low=2.566484861 ci95_high=2.609234146 direction=increasing
DIAGNOSTIC T3 display=2 interval_start_s=263.700000 interval_end_s=290.700000 frames=27 median_lag_columns=16.000000 edge_rmse_columns=6.490350 max_frame_gap_s=1.070000 max_exposure_s=0.004000 slope_columns_s=16.024639444
RESULT T3 speed_mm_s=1.090111527 ci95_low=1.069294290 ci95_high=1.115867449 direction=increasing
DIAGNOSTIC T4 display=3 interval_start_s=5.500000 interval_end_s=32.500000 frames=27 median_lag_columns=27.000000 edge_rmse_columns=8.139442 max_frame_gap_s=1.070000 max_exposure_s=0.005000 slope_columns_s=27.064119622
RESULT T4 speed_mm_s=1.841096573 ci95_low=1.809304326 ci95_high=1.869126185 direction=increasing
```

## Report

### Method and propagation direction

**[MEASURED by code]** Direction was determined from the median consecutive-profile cross-correlation lag. A positive lag means that the luminous structure shifts toward increasing column index.

**[MEASURED by code]** The median lag was `38.000000` columns for T1, `38.000000` columns for T2, `16.000000` columns for T3, and `27.000000` columns for T4.

**[INFERENCE]** Propagation is toward increasing column index for T1, T2, T3, and T4.

**[ASSUMPTION]** The tracked flame-front proxy is the strongest falling spatial-gradient edge after the luminous peak, after smoothing each profile over `9` columns. This tracks the advancing luminous edge of the flame structure. It is not necessarily identical to the physical burning-solid front.

### Speed estimates

| Case | Air display | Estimand interval | Speed | 95% interval | Direction |
|---|---:|---:|---:|---:|---|
| T1 | `3` | `5.500000` to `32.500000` seconds | `2.612779991` mm/s | `2.594490912` to `2.634802788` mm/s | increasing |
| T2 | `3` | `5.500000` to `32.500000` seconds | `2.586929657` mm/s | `2.566484861` to `2.609234146` mm/s | increasing |
| T3 | `2` | `263.700000` to `290.700000` seconds | `1.090111527` mm/s | `1.069294290` to `1.115867449` mm/s | increasing |
| T4 | `3` | `5.500000` to `32.500000` seconds | `1.841096573` mm/s | `1.809304326` to `1.869126185` mm/s | increasing |

**[MEASURED by code]** Each estimate used `27` frames.

### Uncertainty

**[MEASURED by code]** The spatial calibration used was `14.7` columns per millimetre.

**[MEASURED by code]** The reported intervals are percentile intervals from `20000` pair-bootstrap resamples of the selected frame-level front positions and recorded timestamps.

**[MEASURED by code]** Maximum frame-time spacing was `1.070000` seconds in every case.

**[MEASURED by code]** Maximum exposure time within the selected interval was `0.016000` seconds for T1, `0.005000` seconds for T2, `0.004000` seconds for T3, and `0.005000` seconds for T4.

**[MEASURED by code]** Front-position fit RMSE was `6.501770` columns for T1, `6.473193` columns for T2, `6.490350` columns for T3, and `8.139442` columns for T4.

**[ASSUMPTION]** The bootstrap interval is an appropriate representation of uncertainty from frame-to-frame front-position variation and irregular recorded timing.

**[UNKNOWN]** The supplied files do not quantify uncertainty in the `14.7` columns-per-millimetre calibration.

**[UNKNOWN]** The supplied files do not quantify systematic bias between the luminous edge and the physical burning-solid front.

**[UNKNOWN]** The supplied files do not quantify systematic bias caused by exposure-dependent motion blur, optical response, profile construction, or the selected gradient-edge definition.

### Dependencies of the result

**[MEASURED by code]** The result depends on the selected display interval, the timestamps in the metadata, the exposure values, the profile columns, the `14.7` columns-per-millimetre calibration, the `9`-column smoothing window, the cross-correlation direction rule, the falling-gradient edge definition, the ordinary-least-squares fit, and the `20000`-resample bootstrap procedure.

**[ASSUMPTION]** The display intervals are represented by the half-open timestamp ranges used in the code: `5.500000` to `32.500000` seconds for T1, T2, and T4, and `263.700000` to `290.700000` seconds for T3.

### Anomalies and inconsistencies

**[MEASURED by code]** The frame-time spacing is not perfectly uniform; the maximum gap is `1.070000` seconds.

**[MEASURED by code]** T4 has the largest front-fit RMSE at `8.139442` columns, compared with `6.501770` columns for T1, `6.473193` columns for T2, and `6.490350` columns for T3.

**[INFERENCE]** T4 therefore contains more unexplained frame-to-frame variation under the selected front definition than the other cases.

**[INFERENCE]** The direction result is internally consistent across all cases because all median cross-correlation lags are positive and all fitted speeds are positive.

**[UNKNOWN]** The data alone do not establish whether the measured luminous edge coincides with the physical flame front of the solid fuel.