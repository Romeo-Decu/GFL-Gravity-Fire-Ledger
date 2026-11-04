# FiF — Carmignani (2019) BASS/BASS-II B6 Evidence Extraction v0.1

**Status:** Relevant dissertation content extracted from the accessible scholarly record and prior PDF review; graph digitization and raw-data acquisition pending  
**Author:** Luca Carmignani  
**Title:** *Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes*  
**Year:** 2019  
**Institution:** University of California San Diego / San Diego State University  
**Repository record:** https://escholarship.org/uc/item/0rb693zc  
**PDF:** https://escholarship.org/content/qt0rb693zc/qt0rb693zc.pdf

---

## 1. Why this source matters

The dissertation is a scientific analysis source, not simply a second copy of the NASA experimental matrix. It connects BASS microgravity experiments to:
- experimental flame images;
- flame geometry and development;
- flame spread / leading-edge evolution;
- radiometer measurements;
- anemometer / flow measurements;
- FIAT (Flame Image Analyzer Tool) image analysis.

It therefore supplies published derived evidence that can be compared with a future FiF reconstruction from the original B6 media. It must not be mistaken for the original instrument data or an independently acquired experiment.

## 2. B6 identity and conditions

### Appendix A, Table A.2 — experimental conditions

The dissertation's Table A.2 lists B6 among the BASS experimental runs and records:
- test: B6;
- fuel: PMMA;
- thickness: 0.1 mm;
- width: 20 mm;
- oxygen concentration: 21%;
- flow velocity: 1–7 cm/s. The table note explicitly states that the flow-velocity values indicate **initial and final values**; `1–7` is therefore an initial-to-final pair, not a min–max range.

The same table lists B1 and B3 among the thin-PMMA test family. The table is a dissertation summary of experimental conditions. Its flow-velocity field is not automatically equivalent to NASA Table A.1's separate `Fan display` and `Air display` entries.

### Chapter 5 — narrative and figures

The dissertation explicitly discusses B6 in the microgravity opposed-flow analysis:
- Figure 5.4 presents computed flames and experimental images for B6 (above the red line) and B1 (below), with the B6/B1 image comparison associated with 0.1-mm PMMA and the 3 and 5 cm/s flow conditions.
- Figure 5.6 compares experimental flame length against development length for B3, B6 and B1 at nominal flow conditions of 2, 3 and 5 cm/s.
- The narrative identifies B6 at 3 cm/s and B1 at 5 cm/s in the comparison discussed in that section; the reported spread rates are approximately 2 mm/s for both cases. This is a dissertation-level reported result and must not be re-labelled as a FiF measurement or as a direct NASA Table A.1 value.

## 3. Figure 5.8 — B6 time-dependent measurements

Figure 5.8 is particularly valuable. It presents B6-related measurements and image-derived quantities, including:
- radiometer signal (mV);
- anemometer / flow information;
- FIAT-measured flame area;
- a two-dimensional area estimate derived from flame length × 20 mm sample width;
- still images at 10-second intervals;
- corresponding leading-edge / position information in millimetres.

The accompanying discussion states:
- the radiometer signal is approximately stable around 34 mV over the plotted 40–70 mm region;
- the 2D area estimate increases by approximately 120 mm², corresponding to about 6 mm of flame-length increase for a 20 mm width;
- the FIAT-measured flame area oscillates approximately in the 400–600 mm² range.

These are approximate values read/reported in the dissertation's discussion of Figure 5.8. They are **not** a recovered raw CSV, not a full numerical time series, and not precision-digitized points. FiF must retain this distinction.

## 4. Image-processing method described

The dissertation describes processing of BASS top-view video/still-image material with FIAT to derive the evolution of:
- leading-edge position;
- flame spread rate;
- flame length;
- total flame area;
- yellow flame area;
as functions of time.

These image-derived outputs are matched against radiometer and anemometer data from side-view video. The discussion also notes an anemometer response time of approximately one minute and describes matching flow changes with astronaut vocal confirmations.

This creates an important synchronization limitation: the apparent temporal alignment between image-derived flame quantities, flow measurements and spoken crew confirmations requires careful reconstruction. A one-minute sensor response is not negligible relative to a short test. FiF must not assume that a displayed flow step instantaneously equals the local flow experienced by the flame.

**Terminology control:** the dissertation calls its image-processing tool FIAT (Flame Image Analyzer Tool). NASA's report also describes a MATLAB-based “Flame Analyzer.” Do not assume they are the same software or implementation without further evidence.

## 5. Flow representations requiring reconciliation

| Source | B6 flow representation |
|---|---|
| NASA/TM-20210011385, Table A.1 | Fan display: 0.9, 1.3, 2.75; Air display: 3, 5, approaching 10 cm/s |
| Carmignani (2019), Appendix A, Table A.2 | Flow velocity: 1–7 cm/s (initial and final values, per the table note) |
| Carmignani (2019), Chapter 5 narrative / Figures 5.4 and 5.6 | B6 discussed at nominal 3 cm/s; B6/B1 comparisons include 3 and 5 cm/s conditions |

The values are not directly interchangeable. Carmignani's Table A.2 explicitly describes its flow entries as initial and final values; the B6 entry is therefore an initial-to-final change from 1 to 7 cm/s. NASA Table A.1 records Fan display and Air display sequences, including commanded/display steps and a final attempted setting. Carmignani's Figure 5.8 additionally plots an anemometer-derived flow trace, while the narrative says flow adjustments were synchronized using astronaut voice confirmations because the anemometer response time is approximately one minute. This is a plausible explanation for why the representations differ, but the exact mapping between the NASA display settings, the anemometer trace and the table's initial/final values is not yet established. **Do not average, substitute or harmonize these values.**

Required follow-up:
1. inspect the exact Table A.2 column heading and its notes/footnotes;
2. inspect Figure 5.8 axes, plotted anemometer series and time alignment;
3. inspect the PSI-25 Fan calibration workbook and its external-link dependency;
4. inspect the original B6 side-view stream and any sensor/telemetry overlay;
5. establish whether the 1–7 cm/s range is measured, calibrated, commanded, inferred or a rounded summary.

## 6. Evidence status by item

| Item | Current status |
|---|---|
| B6 is a 0.1-mm × 20-mm PMMA test | Corroborated by NASA report and dissertation |
| Nominal oxygen near 21% | Corroborated at summary level; use NASA calibrated 21.0% for precise Table A.1 field |
| B6 nominal 3 cm/s discussion | Dissertation narrative / figure association |
| B6 spread rate approximately 2 mm/s | Dissertation-reported approximate result; exact point/time interval not recovered |
| Radiometer approximately 34 mV | Approximate graph/discussion reading |
| 2D flame area increase approximately 120 mm² | Approximate graph/discussion reading |
| FIAT flame area approximately 400–600 mm² | Approximate graph/discussion reading |
| Full Figure 5.8 time series | Not digitized |
| FIAT source code / exact version / settings | Not acquired |
| Original input images used by FIAT | Not yet paired to PSI-25 media |
| Sensor calibration and timing | Incomplete |
| Numerical uncertainty of digitized plots | Not established |

## 7. Source locators

- Dissertation Appendix A, Table A.2: BASS experimental conditions, B1–B22, including B6.
- Chapter 5, Figure 5.4: experimental images / computed flames for B6 and B1.
- Chapter 5, Figure 5.6: flame length versus development length for B3, B6 and B1.
- Chapter 5, Figure 5.8 and accompanying discussion: B6 radiometer, anemometer, FIAT flame area, 2D area and time-indexed stills.
- Chapter 5 discussion: FIAT image processing and anemometer response/synchronization.

The prior PDF extraction review located Figure 5.4 around dissertation PDF text lines 1819–1821, Figure 5.6 around lines 1813–1818, Figure 5.8 and its discussion around lines 1871–1888, and Appendix A Table A.2 around lines 2343–2373. These line references are extraction locators, not printed page numbers.

## 8. Required next extraction

The next useful operation is not another general literature search. It is a controlled digitization of Figure 5.8 and, if possible, Figures 5.4/5.6:
- preserve the source image;
- record axis calibration and units;
- digitize each plotted series independently;
- retain point-level digitization uncertainty;
- record ambiguous/occluded points as missing;
- do not infer timestamps from image spacing unless the figure explicitly defines the interval;
- compare only after confirming which series and time bases refer to the same B6 run.

The original B6 video and the thesis figure are two evidence representations to be reconciled, not interchangeable ground truth.


## 9. Source terminology and identity-linkage caution

The dissertation's Appendix A heading is **“The BASS Experiments”**, and the figure captions refer to “BASS” experiments. The dissertation does not, in the cited table/figure captions, explicitly label the dataset “BASS-II”.

The candidate linkage to NASA BASS-II B6 is strongly supported by the matching test label B6, PMMA thickness 0.1 mm, sample width 20 mm, oxygen concentration 21%, and the B6-specific 3 cm/s case in Figure 5.4. However, Table A.2 does not provide the NASA GMT188 or sample 153m identifiers. Preserve the dissertation's own “BASS” terminology and record the BASS-II B6 linkage as a strong cross-source match pending direct media/metadata verification; do not silently rewrite the dissertation's source label.

## 10. FIAT method and image-measurement uncertainty

The dissertation provides more detail on FIAT than the B6-specific figure discussion alone:

### 10.1 Intensity tracking

- The image is transformed from RGB to YCrCb.
- The Y channel represents luminance; Cr and Cb are chrominance channels.
- Y intensity is averaged in the direction perpendicular to flame propagation to form a 2D representation.
- Thresholds on Y define flame leading and trailing edges.
- Flame length is the distance between those two edge locations.

### 10.2 Area / color tracking

- Frames remain in RGB.
- Minimum and maximum values are selected for each 8-bit color channel (0–255).
- Pixels outside the selected channel intervals are excluded.
- This allows isolation and measurement of regions such as the blue flame and yellow/sooty region.
- Repeating the process frame by frame produces flame area, edge positions, position history and spread-rate history.

### 10.3 Measurement error model

The dissertation's error analysis identifies frame rate (f) and spatial resolution (p) (pixels/mm) as direct imaging parameters. If the leading edge moves (n_p) pixels over (n_f) frames, the spread-rate estimate depends on both counts and on (f/p). The stated relative error bound is:

\[
\epsilon = \frac{1}{\Delta t}\left(\frac{1}{pV_f}+\frac{1}{f}\right)
\]

where \(V_f\) is flame spread rate and \(\Delta t\) is the observation interval. This is the dissertation's image-measurement error analysis; it is not a universal uncertainty guarantee for every camera or B6 stream. Actual FiF uncertainty must use the verified pixel/mm scale, frame rate, segmentation repeatability, edge-location uncertainty and chosen time window.

### 10.4 B6 synchronization details

The dissertation states that:
- FIAT analysis of top-view video created from BASS still images yields leading-edge position, spread rate, flame length, total area and yellow area versus time;
- these are matched with radiometer and anemometer data printed on side-view video frames;
- the anemometer response time is approximately one minute;
- flow adjustments are matched with astronauts' vocal confirmations recorded during the experiments;
- no time delay is applied to the radiometer;
- B6 radiometer readings are taken from the first frame of each second of the side video;
- total flame area is measured directly with FIAT area tracking;
- 2D area is independently calculated as FIAT intensity-tracked flame length × 20 mm sample width.

This is a concrete reconstruction protocol, but it still depends on access to the source top-view still sequence and side-view video, correct timebase mapping, and the original FIAT thresholds/settings.

## 11. Source locators added

- Dissertation PDF printed page 19 / extracted lines 1346–1363: FIAT intensity and area tracking methods.
- Dissertation PDF printed pages 19–20 / extracted lines 1364–1476: image-resolution, frame-rate and spread-rate error analysis.
- Dissertation Appendix A, printed page 105 / extracted lines 4088–4126: BASS experiment matrix; note that flow velocity values indicate initial and final values.
- Dissertation printed page 80 / extracted lines 3200–3225: B6 FIAT/radiometer/anemometer synchronization and approximate Figure 5.8 values.
- Dissertation printed page 81 / extracted lines 3227–3231: Figure 5.8 caption and plotted data types.
