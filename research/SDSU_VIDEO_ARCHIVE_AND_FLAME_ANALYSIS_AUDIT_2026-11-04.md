# FiF — SDSU Video Archive and Flame-Analysis Route Audit

**Date:** 2026-11-04  
**Status:** Documentary route identified; archive contents and run-level linkage not independently verified  
**Case:** 100-µm PMMA opposed-flow flame spread, BASS-II / normal-gravity downward comparison

## 1. Primary-source identification of the archive

NASA/TM-20210011385, Section 2.3.6 (Data Analysis), explicitly states that still images from the BASS experiments were converted to videos and posted together with the downward-experiment videos at:

- http://flame.sdsu.edu

The same report states that San Diego State University developed a MATLAB-based image-processing application called **Flame Analyzer** to obtain flame-spread rate and other information from top-view video. Appendix A.1 also directs readers to this archive for details of the Bhattacharjee test matrix.

This makes the SDSU archive a primary-source-designated route for the image-derived videos and associated experimental detail. It is not merely a third-party mirror.

**Access result on 2026-11-04:** A direct automated page retrieval attempt timed out. Search indexing did not expose a usable directory listing. No archive file was independently opened or downloaded during this audit. The archive's current availability, directory structure, file naming, and completeness therefore remain unverified.

## 2. What the NASA report says about the image-analysis chain

Section 2.3.6 describes the following processing chain:

1. Start with a top-view color image/video.
2. Select a central image slice.
3. Convert RGB pixel values to intensity using MATLAB tools.
4. Average intensity across the sample width to produce a one-dimensional representation along the axial direction.
5. Apply a fixed intensity threshold to locate the flame leading edge.
6. Track leading-edge position over successive frames.
7. Estimate spread rate as the slope of a linear regression of leading-edge position against time.

Figure 2.18 shows a representative downward-spread image at 18 seconds after ignition. The displayed spatial reference dots are 6 mm apart. The report gives a threshold value of 70 for tracking the leading edge in that particular illustrated test.

**Important restriction:** The threshold of 70 is a reported example for the Figure 2.18 test; it must not be silently treated as a validated universal threshold for the 100-µm BASS-II B3 video or its normal-gravity counterpart. FiF must determine whether the same threshold, image processing, spatial calibration, and temporal sampling apply to each asset.

## 3. Reported uncertainty and reproducibility

For the 100-µm comparison, NASA states that consecutive leading-edge positions were used to obtain spread rate through linear regression. The report states:

- spread-rate uncertainty below 5% away from ignition;
- 5-second propagation averages reproducible within 5% variability;
- uncertainty near ignition is higher and should not be treated as covered by the stated below-5% figure.

These are source-reported performance statements about the NASA analysis. They are not yet independently reproduced by FiF.

## 4. Relationship to the files visible in PSI-25

The user reported that the PSI-25 B3 folder lists:

- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3_Still_Sequence.mp4` — 1.98 MB;
- `PSI-25_Raw Data_iss038e051295.zip` — 534.48 MB;
- `PSI-25_Raw Data_GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf` — 242.37 KB;
- `PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip` — 14.92 MB.

The user has downloaded the 14.92 MB ZIP to a local Desktop folder named FiF. The file is not available in the assistant's current working environment, so its contents, checksum, and relationship to the SDSU archive cannot yet be verified.

The filename indicates a likely B3/sample-148 asset association, but filename semantics alone do not prove that the archive contains the exact video or reduced data used in Figure 2.19.

## 5. Required FiF verification when the asset becomes accessible

Do not begin quantitative fitting until the following are checked:

1. List all archive members without modifying or extracting source files in place.
2. Record archive SHA-256, member paths, sizes, and available timestamps.
3. Identify whether files are still images, image-derived video, original camera video, reduced data, or metadata.
4. Establish which camera/view each video represents and whether it is top-view or side-view.
5. Determine frame rate / frame interval and whether timestamps are original or generated during conversion.
6. Establish spatial calibration from scale references or metadata; do not assume the 6-mm Figure 2.18 reference applies to every video.
7. Link the relevant asset to test ID, sample ID, date/GMT, and Appendix A.1 row.
8. Reconstruct the leading-edge trajectory and spread rate independently, preserving threshold sensitivity and uncertainty.
9. Keep the 2 cm/s (Appendix A.1 B3 air display) versus 3 cm/s (Section 2.3 comparison prose) discrepancy open until the original records resolve it.
10. Identify the corresponding normal-gravity downward video and its run/sample metadata independently.

## 6. Current decision

The SDSU archive is the next documentary/data route to investigate because NASA itself identifies it as the location of the BASS still-image-derived videos and downward videos.

The PSI-25 B3 still-sequence MP4 and the user-downloaded 14.92 MB ZIP are candidate assets, not verified evidence of the Section 2.3 comparison run. No raw-video analysis, independent reproduction of 2.0/2.2 mm/s, or run-level cross-link has been completed by FiF.

## 7. Primary references

- Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385, Section 2.3.6, Figures 2.18–2.20, Appendix A.1.
- NASA NTRS record: https://ntrs.nasa.gov/citations/20210011385
- NASA report PDF: https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf
- SDSU archive named by NASA: http://flame.sdsu.edu


## 8. Threshold provenance correction — keep the three contexts separate

A closer page-level check of NASA/TM-20210011385 establishes three distinct facts:

- **Section 2.2.4, Figure 2.7 (report p. 22):** the separate radiative-extinction study describes a threshold intensity of **30**, reported to work for almost all tests in that study. The same subsection describes the 100-µm extinction experiment that reached 2.2 mm/s before flow was cut off. This is not the Section 2.3 microgravity/normal-gravity comparison dataset.
- **Section 2.3.6, Figure 2.18 (report p. 39):** the illustrated downward-spread example is a **75-µm** sample, and the report says a threshold of **70** worked for tracking the leading edge in that test.
- **Section 2.3.6, 100-µm comparison (Figure 2.19):** the report describes tracking consecutive leading-edge locations and fitting a linear regression, but the text does **not state the numerical intensity threshold used for the 100-µm microgravity/downward comparison**.

Therefore neither 30 nor 70 is a verified threshold for the target 100-µm Section 2.3 comparison. FiF must recover the actual analysis setting from the original assets, Flame Analyzer configuration/source, or additional primary records. If that setting cannot be recovered, FiF must conduct a documented threshold-sensitivity analysis and label its own selected threshold as a reconstruction choice, not as NASA's original setting.

This correction supersedes any reading of the earlier paragraph that might imply that 70 was used for the target 100-µm comparison. It also prevents the threshold of 30 from the distinct Section 2.2 study being transferred to the Section 2.3 target by proximity in the report.



## 9. Independent methodological reference for video-measurement uncertainty

A relevant peer-reviewed methods paper by the same research group is:

Bhattacharjee, S., Carmignani, L., Celniker, G., and Rhoades, B. (2017), **“Measurement of instantaneous flame spread rate over solid fuels using image analysis,”** *Fire Safety Journal*, 91, 123–129. DOI: https://doi.org/10.1016/j.firesaf.2017.03.039

The paper develops a MATLAB-based Flame Image Analyzer (FIA) methodology and an error analysis for instantaneous flame-spread histories. Its abstract and accessible text identify **frame rate** and **spatial resolution in pixels per millimetre** as the two principal imaging parameters governing measurement quality. It proposes the non-dimensional imaging parameter:

\[
\varphi = \frac{f}{p V_f}
\]

where \(f\) is frame rate (frames/s), \(p\) is spatial resolution (pixels/mm), and \(V_f\) is flame spread rate (mm/s).

This publication is methodological support, not proof that the exact FIA implementation, settings, or error bound were used for the specific 100-µm Section 2.3 comparison in the NASA report. Do not conflate the 2017 FIA paper/tool with the NASA report's named Flame Analyzer software without verifying implementation lineage.

**FiF consequence:** frame rate and spatial scale are mandatory inputs to any quantitative video reconstruction. If either is unknown, FiF may extract qualitative trajectories or report a conditional estimate, but must not claim a validated measurement uncertainty. The reported NASA “less than 5%” result cannot simply be copied as FiF's own uncertainty.

