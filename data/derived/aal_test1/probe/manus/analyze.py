import numpy as np
import pandas as pd

BASE = "/home/ubuntu/manus_package"
SCALE_COLUMNS_PER_MM = 14.7
FLOW_VALUE = 3
FLOW_START = 5.5
FLOW_END = 32.5
SMOOTH_WIDTH = 3
THRESHOLD_FRACTION = 0.50
BOOTSTRAPS = 20000
BOOTSTRAP_SEED = 20261111

# Method fixed before any fitted slope is calculated:
# - use every frame with FLOW_START <= t_s < FLOW_END;
# - smooth each band profile by a centered 3-column moving average;
# - define the front as the descending crossing, after the profile maximum,
#   of THRESHOLD_FRACTION times that profile's maximum; linearly interpolate;
# - fit ordinary least squares front-column position versus timestamp;
# - convert the slope using the supplied spatial scale;
# - obtain a 95% interval by seeded residual bootstrap, resampling fitted
#   residuals with replacement 20,000 times and taking the 2.5/97.5 percentiles.
# No fitted slope is used to select frames, choose a threshold, or change the method.

def moving_average_3(a):
    return (np.r_[a[0], a[:-1]] + a + np.r_[a[1:], a[-1]]) / 3.0


def front_column(profile):
    y = moving_average_3(np.asarray(profile, dtype=float))
    peak_index = int(np.argmax(y))
    threshold = THRESHOLD_FRACTION * y[peak_index]
    crossing = np.flatnonzero(y[peak_index:] <= threshold)
    if len(crossing) == 0:
        raise ValueError("No descending threshold crossing after profile maximum")
    j = peak_index + int(crossing[0])
    if j == peak_index:
        return float(j), peak_index, threshold
    x0, x1 = j - 1, j
    y0, y1 = y[x0], y[x1]
    if y1 == y0:
        x = float(j)
    else:
        x = x0 + (threshold - y0) / (y1 - y0)
    return float(x), peak_index, threshold


def ols(x, y):
    xbar = np.mean(x)
    ybar = np.mean(y)
    dx = x - xbar
    slope = np.sum(dx * (y - ybar)) / np.sum(dx * dx)
    intercept = ybar - slope * xbar
    fitted = intercept + slope * x
    return intercept, slope, fitted, y - fitted


def bootstrap_interval(t, front, seed):
    intercept, slope, fitted, residuals = ols(t, front)
    rng = np.random.default_rng(seed)
    sampled_residuals = rng.choice(residuals, size=(BOOTSTRAPS, len(residuals)), replace=True)
    y_boot = fitted[None, :] + sampled_residuals
    xbar = np.mean(t)
    dx = t - xbar
    slopes = np.sum(dx[None, :] * (y_boot - np.mean(y_boot, axis=1)[:, None]), axis=1) / np.sum(dx * dx)
    return np.percentile(slopes, [2.5, 97.5]) / SCALE_COLUMNS_PER_MM


def fit_speed(t, front):
    intercept, slope, fitted, residuals = ols(t, front)
    interval = bootstrap_interval(t, front, BOOTSTRAP_SEED)
    return slope / SCALE_COLUMNS_PER_MM, interval, intercept, residuals


def measure_case(case):
    metadata = pd.read_csv(f"{BASE}/{case}_frames_metadata.csv")
    profiles = pd.read_csv(f"{BASE}/{case}_band_profiles.csv")
    flow = pd.read_csv(f"{BASE}/{case}_flow_display.csv")
    if not np.array_equal(metadata["image"].to_numpy(), profiles["image"].to_numpy()):
        raise ValueError(f"{case}: metadata/profile image IDs do not match")

    selected = metadata[(metadata["t_s"] >= FLOW_START) & (metadata["t_s"] < FLOW_END)].copy()
    selected_idx = selected.index.to_numpy()
    profile_values = profiles.iloc[selected_idx, 1:].to_numpy(float)
    fronts = []
    peak_indices = []
    thresholds = []
    for row in profile_values:
        front, peak_index, threshold = front_column(row)
        fronts.append(front)
        peak_indices.append(peak_index)
        thresholds.append(threshold)
    fronts = np.asarray(fronts)
    peak_indices = np.asarray(peak_indices)
    thresholds = np.asarray(thresholds)
    times = selected["t_s"].to_numpy(float)
    speeds, interval, intercept, residuals = fit_speed(times, fronts)

    print(f"CASE {case}")
    print(f"flow_display_3_interval_s=[{FLOW_START:.1f}, {FLOW_END:.1f})")
    print(f"selected_frame_count={len(selected)}")
    print(f"selected_frame_ids={','.join(selected['image'])}")
    print(f"selected_time_min_s={times.min():.5f}")
    print(f"selected_time_max_s={times.max():.5f}")
    print(f"front_definition=descending crossing after profile maximum at {THRESHOLD_FRACTION:.2f}*per-frame maximum, centered moving-average width={SMOOTH_WIDTH}, linear interpolation")
    print(f"front_column_min={fronts.min():.5f}")
    print(f"front_column_max={fronts.max():.5f}")
    print(f"front_column_change={fronts[-1]-fronts[0]:.5f}")
    print(f"direction={'towards increasing column index' if fronts[-1] > fronts[0] else 'towards decreasing column index'}")
    print(f"scale_columns_per_mm={SCALE_COLUMNS_PER_MM:.1f}")
    print(f"ols_intercept_columns={intercept:.5f}")
    print(f"ols_slope_columns_per_s={speed if False else (speeds*SCALE_COLUMNS_PER_MM):.8f}")
    print(f"preferred_speed_mm_per_s={speeds:.8f}")
    print(f"bootstrap_method=residual bootstrap, B={BOOTSTRAPS}, seed={BOOTSTRAP_SEED}, percentile=[2.5,97.5]")
    print(f"speed_95_interval_mm_per_s=[{interval[0]:.8f}, {interval[1]:.8f}]")
    print(f"residual_rms_columns={np.sqrt(np.mean(residuals**2)):.5f}")
    print(f"threshold_min={thresholds.min():.5f}")
    print(f"threshold_max={thresholds.max():.5f}")

    print("sensitivity_threshold_fraction")
    for fraction in [0.25, 0.50, 0.75]:
        old = globals()["THRESHOLD_FRACTION"]
        globals()["THRESHOLD_FRACTION"] = fraction
        f2 = np.asarray([front_column(row)[0] for row in profile_values])
        s2 = ols(times, f2)[1] / SCALE_COLUMNS_PER_MM
        print(f"fraction={fraction:.2f}, speed_mm_per_s={s2:.8f}, front_change_columns={f2[-1]-f2[0]:.5f}")
        globals()["THRESHOLD_FRACTION"] = old

    long_exposure = selected[selected["exposure_s"] > 0.010]
    print(f"selected_exposure_min_s={selected['exposure_s'].min():.6f}")
    print(f"selected_exposure_max_s={selected['exposure_s'].max():.6f}")
    print(f"selected_long_exposure_count_gt_0.010_s={len(long_exposure)}")
    if len(long_exposure):
        print(f"selected_long_exposure_ids={','.join(long_exposure['image'])}")
    gaps = np.diff(metadata["t_s"].to_numpy(float))
    print(f"all_frame_count={len(metadata)}")
    print(f"all_time_gap_max_s={gaps.max():.5f}")
    print(f"all_time_gap_gt_2s_count={int(np.sum(gaps > 2.0))}")
    print(f"flow_schedule_rows={len(flow)}")
    print()

print("METHOD_FIXED_BEFORE_SLOPE=TRUE")
print(f"rules: interval=[{FLOW_START:.1f},{FLOW_END:.1f}), threshold={THRESHOLD_FRACTION:.2f}, smoothing_width={SMOOTH_WIDTH}, scale={SCALE_COLUMNS_PER_MM:.1f}, bootstrap_B={BOOTSTRAPS}, seed={BOOTSTRAP_SEED}")
print()
for case in ["S1", "S2"]:
    measure_case(case)
