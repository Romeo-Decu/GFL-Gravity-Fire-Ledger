# Data schema and sample (the full files stay with the Validator)

Two cases, S1 and S2, with the same structure. Row order of profiles = row order of metadata.

## <case>_frames_metadata.csv — about 63 rows + header
Columns: image, t_s (seconds from the first frame), exposure_s (shutter chosen by the camera).

First 6 rows of S1:
```
image,t_s,exposure_s
S1_000,0.00,0.333333
S1_001,1.00,0.333333
S1_002,2.00,0.333333
S1_003,3.00,0.333333
S1_004,4.00,0.001000
S1_005,5.00,0.001000
```

## <case>_band_profiles.csv — same number of rows + header
Columns: `image`, then `c0` … `c2159` (one value per image column along the propagation direction).
Values: relative radiance in counts per second (raw divided by exposure time, frame median removed, mean over the rows that see the fuel strip).

First 3 data rows of S1, first 10 value columns only:
```
image,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9
S1_000,-6.44842,0.318465,-2.90302,2.61257,-1.25557,7.36822,2.71575,-0.0735276,1.84377,5.39802
S1_001,5.37537,0.518018,3.91005,-2.12417,2.89242,-11.1211,3.66539,4.9906,1.08916,-5.2606
S1_002,3.27597,0.449542,-4.72186,-2.01487,-2.72769,2.31193,-0.83223,0.317682,-4.51791,-0.952332
```

## <case>_flow_display.csv — the air-flow display setting from each time on
S1 (S2 has the same schedule):
```
t_s,AIR_display
0.0,4
5.5,3
32.5,5
44.5,8
56.5,10
```

Spatial scale: 14.7 columns per mm.
