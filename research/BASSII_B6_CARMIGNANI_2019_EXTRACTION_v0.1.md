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
- flow velocity field/range: 1–7 cm/s (as represented in this table).

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

## 5. Flow-field discrepancy requiring resolution

| Source | B6 flow representation |
|---|---|
| NASA/TM-20210011385, Table A.1 | Fan display: 0.9, 1.3, 2.75; Air display: 3, 5, approaching 10 cm/s |
| Carmignani (2019), Appendix A, Table A.2 | Flow velocity field/range: 1–7 cm/s |
| Carmignani (2019), Chapter 5 narrative / Figures 5.4 and 5.6 | B6 discussed at nominal 3 cm/s; B6/B1 comparisons include 3 and 5 cm/s conditions |

These values are not necessarily contradictory: they may represent different quantities, calibration mappings, time windows, or a summary range versus commanded display steps. However, the currently available material does not establish the transformation. **Do not average, substitute or harmonize these values.**

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
