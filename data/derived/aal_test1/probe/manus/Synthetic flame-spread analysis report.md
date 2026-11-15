# Synthetic flame-spread analysis report

## Method and scope

[ASSUMPTION] The air-display value applies from its listed time until the next listed time; therefore the display-3 interval is the half-open interval `[5.5, 32.5)` s, as used by the code.

[ASSUMPTION] The flame front is represented by the descending crossing after the per-frame profile maximum at `0.50` of that frame's maximum, after centered moving-average smoothing with width `3`; the crossing is linearly interpolated.

[ASSUMPTION] The supplied spatial scale is `14.7` columns/mm.

[ASSUMPTION] Ordinary least squares of front column versus timestamp is an adequate speed estimator for the selected frames.

[ASSUMPTION] The residual-bootstrap interval is appropriate for uncertainty quantification: `20,000` resamples, seed `20261111`, with the `2.5` and `97.5` percentiles reported.

[MEASURED from these files] The code selected every frame with timestamp in `[5.5, 32.5)` s and did not select frames using a fitted slope.

[MEASURED from these files] The code checked that metadata and profile image IDs match before analysis.

## Case S1

[MEASURED from these files] The selected set contains `27` frames, IDs `S1_006` through `S1_032` as listed in the program output, with selected timestamps from `6.00000` s to `32.28000` s.

[MEASURED from these files] The front column ranges from `264.88165` to `1037.10161`, a change of `772.21997` columns.

[INFERENCE] The propagation direction is towards increasing column index.

[MEASURED from these files] The OLS slope is `29.45892333` columns/s, which converts to the preferred speed `2.00400839` mm/s using `14.7` columns/mm.

[MEASURED from these files] The residual-bootstrap 95 % interval is `[1.97627824, 2.03196855]` mm/s.

[MEASURED from these files] The OLS intercept is `88.78297` columns and the residual RMS is `8.11994` columns.

[MEASURED from these files] The per-frame threshold values range from `511840.00000` to `4663028.33333` in the profile units.

[MEASURED from these files] Threshold sensitivity is: fraction `0.25` gives `2.00138313` mm/s and a front change of `771.78187` columns; fraction `0.50` gives `2.00400839` mm/s and `772.21997` columns; fraction `0.75` gives `2.00649625` mm/s and `772.35095` columns.

[MEASURED from these files] Selected exposure times range from `0.001000` s to `0.016000` s. There is `1` selected exposure greater than `0.010` s: `S1_022`.

## Case S2

[MEASURED from these files] The selected set contains `27` frames, IDs `S2_006` through `S2_032` as listed in the program output, with selected timestamps from `6.07000` s to `32.49000` s.

[MEASURED from these files] The front column ranges from `267.32856` to `982.39304`, a change of `715.06448` columns.

[INFERENCE] The propagation direction is towards increasing column index.

[MEASURED from these files] The OLS slope is `26.98303454` columns/s, which converts to the preferred speed `1.83558058` mm/s using `14.7` columns/mm.

[MEASURED from these files] The residual-bootstrap 95 % interval is `[1.80921739, 1.86109830]` mm/s.

[MEASURED from these files] The OLS intercept is `106.36768` columns and the residual RMS is `7.48324` columns.

[MEASURED from these files] The per-frame threshold values range from `511910.00000` to `4606563.33333` in the profile units.

[MEASURED from these files] Threshold sensitivity is: fraction `0.25` gives `1.79110391` mm/s and a front change of `699.25756` columns; fraction `0.50` gives `1.83558058` mm/s and `715.06448` columns; fraction `0.75` gives `1.87381416` mm/s and `729.52035` columns.

[MEASURED from these files] Selected exposure times range from `0.001000` s to `0.016000` s. There is `1` selected exposure greater than `0.010` s: `S2_016`.

## Dependencies and limitations

[MEASURED from these files] The numerical result depends on the display-3 interval `[5.5, 32.5)` s, the `27` selected frames in each case, the front threshold fraction `0.50`, smoothing width `3`, spatial scale `14.7` columns/mm, OLS fitting, and the residual-bootstrap settings `20,000` replicates and seed `20261111`.

[MEASURED from these files] The code reports `5` rows in each flow schedule.

[UNKNOWN] The files do not provide an externally validated front location or an uncertainty model independent of the assumptions above.

[UNKNOWN] The files do not establish whether the selected long-exposure frames should be excluded; the preferred results retain them because the predeclared selection rule is based on timestamp within the display-3 interval.

## Anomalies

[MEASURED from these files] Each case has `1` selected exposure greater than `0.010` s, namely `S1_022` for S1 and `S2_016` for S2, while the selected exposure range in each case is `0.001000` s to `0.016000` s.

[MEASURED from these files] Each metadata set has an all-frame maximum time gap of `110.00000` s and `2` gaps greater than `2.0` s.

[INFERENCE] The `110.00000` s gap is a substantial discontinuity in the full time series and is relevant if frames outside the display-3 interval are analyzed.

[UNKNOWN] The cause of the long time gaps and the selected long exposures cannot be determined from the supplied files alone.
