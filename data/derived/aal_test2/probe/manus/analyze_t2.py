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
