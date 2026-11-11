# Data schema and sample (the full files stay with the Validator)

Four cases, T1 to T4, with the same structure. Row order of profiles = row order of metadata.

## <case>_frames_metadata.csv — about 62 rows + header
Columns: image, t_s (seconds from the first frame), exposure_s (shutter chosen by the camera).

First 4 rows of T1:
```
image,t_s,exposure_s
T1_000,0.00,0.333333
T1_001,1.07,0.333333
T1_002,2.07,0.333333
T1_003,3.07,0.333333
```
First 4 rows of T3 (note the time of the second frame):
```
image,t_s,exposure_s
T3_000,0.00,0.333333
T3_001,248.68,0.333333
T3_002,249.68,0.333333
T3_003,250.68,0.333333
```

## <case>_band_profiles.csv — same number of rows + header
Columns: `image`, then `c0` … `c2159` (one value per image column along the propagation direction).
Values: relative radiance in counts per second (raw divided by exposure time, frame median removed, mean over the rows that see the fuel strip).

First 2 data rows of T1, first 10 value columns only:
```
image,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9
T1_000,-0.796977,-4.5899,3.09387,-2.54827,-0.576213,-2.71626,-0.281662,-2.53272,-6.62445,1.33872
T1_001,1.51316,0.962194,3.81828,-3.04333,-3.69982,0.431587,7.26221,-0.451499,0.0272519,-5.20765
```

## <case>_flow_display.csv — the air-flow display setting from each time on
T1 (T2 and T4 have the same schedule):
```
t_s,AIR_display
0.0,4
5.5,3
32.5,2
44.5,1
```
T3:
```
t_s,AIR_display
248.7,5
256.7,3
263.7,2
290.7,0
```

Spatial scale: 14.7 columns per mm.
