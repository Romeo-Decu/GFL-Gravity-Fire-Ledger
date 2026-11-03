# FiF — Section 2.3 Data-Linkage Audit: 100-µm PMMA Comparison

**Date:** 2026-11-03  
**Status:** Primary-source audit; quantitative record linkage unresolved  
**Primary source:** Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385, Section 2.3, Figures 2.19–2.20, Appendix A.1.

## 1. Why this audit is necessary

The report contains several related but distinct 100-µm PMMA results. It is not safe to attach every value to the B3/B03 row in Appendix A.1 merely because Figure 2.20 labels a 100-µm BASS-II image as B03.

In particular, the often-repeated 2.2 mm/s value appears in more than one discussion context:
- Section 2.2 describes a separate microgravity extinction experiment on a 100-µm sample that reached 2.2 mm/s before flow was cut off; a second test reduced flow and extinguished near 1.1 cm/s.
- Section 2.3 reports the maximum microgravity spread rate of about 2.2 mm/s for 100-µm fuel in the comparison with normal-gravity downward spread, and reports 2.0 mm/s for the normal-gravity case.

These are not proven to be the same experimental run. The 2.2 mm/s result from Section 2.2 must not be treated as the measured value of B3/B03 without a direct record join.

## 2. What the primary report establishes

### Section 2.3 experimental configuration

- BASS-II samples: PMMA, 20 mm wide, approximately 95 mm long, 100–400 µm thick, in a 76-mm-square duct.
- Opposed O2/N2 flow; O2 at 21% or below.
- Pressure in the reported BASS-II tests: 99.2–99.5 kPa.
- Flow velocity calibrated using a hot-wire anemometer.
- Downward experiments: 20-mm-wide PMMA held vertically in a stainless-steel holder; piloted ignition; 101 kPa and 21% O2.
- The BASS holder has a built-in igniter, so the ignition configuration differs.
- NASA states that the 100-µm comparison used a 3 cm/s opposing flow in microgravity, with most other conditions kept similar.
- Normal-gravity average downward spread rate: 2.0 mm/s.
- Maximum microgravity spread rate for the same thickness: approximately 2.2 mm/s, over reported flow variation of about 40 to 1 cm/s.
- Image-tracking uncertainty: below 5% away from ignition; 5-s averages reproducible within 5% variability.
- Figure 2.20 identifies BASS-II B03 as the 100-µm microgravity image and a NASA PMMA 100-µm normal-gravity image at SDSU.

### Appendix A.1 B3 row

The B3 table row identifies:
- Test number: B3
- Sample number: 148
- Material: 100-µm PMMA film, 2 cm wide
- Flow restrictor: integral
- Flow direction: opposed
- Fan display: 47
- Air display: 2 cm/s
- Calibrated O2: 22.2% initial, 21.8% final
- Uncalibrated O2: 20.9% initial, 20.5% final
- Observation: “Probably 20.6 O2 to start; lower flow flames much more blue overall; still some soot though”

The Appendix A.1 row's air display of 2 cm/s does not match the Section 2.3 prose statement that the comparison microgravity experiment used 3 cm/s. This is a real linkage discrepancy requiring resolution, not a value to average or silently harmonize. The table also reports fan display separately from air display; fan display is not a velocity.

### Figure 2.20 caption

The caption identifies the microgravity image series as:
- B03, 100 µm;
- B11, 200 µm;
- B4, 300 µm;
- B13, 400 µm.

It identifies the normal-gravity series at SDSU as NASA PMMA at 100 µm, Astra PMMA at 200 µm, NASA PMMA at 300 µm, and NASA PMMA at 400 µm. It gives nominal caption conditions of 20.7% O2 / 79% N2 / 1 atm for the image series.

The caption does not provide the normal-gravity test/run identifier, sample/batch identifier, exact measured O2 record, or raw video filename. The normal-gravity specimen is therefore identified only at the level of material supplier label and nominal thickness.

## 3. Current linkage status

| Link | Status | What is established | What remains unresolved |
|---|---|---|---|
| Figure 2.20 B03 ↔ Appendix A.1 B3 | Probable, not fully proven | Same PI, 100-µm PMMA, 2-cm width, matching B03/B3 label | Original asset filename and exact sample/test join |
| Section 2.3 microgravity comparison ↔ B3 | Unresolved | Same nominal thickness and BASS-II context | Section 2.3 says 3 cm/s; B3 table air display says 2 cm/s; no explicit test ID in the comparison paragraph |
| Section 2.2 2.2-mm/s run ↔ B3 | Not established | Both concern 100-µm PMMA and 2.2 mm/s appears in discussion | No direct run ID/sample ID join; treat as separate until proven otherwise |
| Figure 2.20 normal-gravity 100-µm NASA PMMA ↔ Section 2.3 2.0 mm/s | Strong contextual association, run-level join missing | Same section, figure, material label and thickness | No run ID, sample/batch ID, raw filename or reduced-data row |

## 4. O2 calibration interpretation

NASA states that the CSA-CP O2 sensor was not recalibrated on orbit. The team used the Major Constituents Analyzer (MCA) data to determine the O2 sensor offset on a daily basis. The table separately presents calibrated and uncalibrated values.

For B3, the two pairs are:
- calibrated initial/final: 22.2 / 21.8 vol%;
- uncalibrated initial/final: 20.9 / 20.5 vol%.

The crew note says “Probably 20.6 O2 to start”. The Figure 2.20 caption gives 20.7% O2 / 79% N2 / 1 atm as the nominal image-series condition. These values are not interchangeable. The daily offset procedure explains why the values differ in principle, but does not by itself establish which value was used in the Section 2.3 comparison analysis or the Figure 2.20 caption.

## 5. FiF decision

1. Do not claim that B3 produced the Section 2.3 2.2-mm/s value until a direct record link is established.
2. Do not use Section 2.2's 2.2-mm/s result as a B3 measurement.
3. Preserve the B3 Appendix A.1 measured/calibrated fields, uncalibrated fields, air display, fan display, and crew note separately.
4. Record the 2 cm/s (Appendix A.1) versus 3 cm/s (Section 2.3) discrepancy explicitly.
5. Treat the Figure 2.20 nominal 20.7% O2 condition as a caption-level condition, not a verified B3 sensor measurement.
6. Treat the normal-gravity sample as an identified figure specimen, not yet a traceable experimental record.
7. Do not fit or validate a quantitative transfer model until the raw/reduced data join is established.

## 6. Next verification target

The next required asset is the SDSU flame.sdsu.edu archive cited by NASA for the BASS still-image-derived videos and downward-spread videos. The report states that Flame Analyzer was used to calculate instantaneous spread rates from top-view video. The required join is:

NASA Figure 2.19/2.20 curve or image → SDSU video/reduced time series → run/sample ID → Appendix A.1 row (where applicable) → extracted spread-rate observation.

The archive was not downloaded or independently inspected in this audit. No raw video, image sequence, or reduced time-series has yet been verified by FiF.

## 7. Primary-source references

- NASA report PDF: https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf
- Section 2.2, especially the 100-µm 2.2-mm/s extinction experiment.
- Section 2.3.5–2.3.7, report pp. 37–41: apparatus, comparison setup, data analysis, 2.0 and 2.2 mm/s results.
- Figure 2.19: microgravity/downward leading-edge and spread-rate comparison.
- Figure 2.20: specimen labels and caption-level nominal conditions.
- Appendix A.1, Table A.1: B3 test/sample row and measured fields.
- NASA NTRS record: https://ntrs.nasa.gov/citations/20210011385

**Conclusion:** The physics case remains promising, but the data lineage is not yet closed. FiF must preserve the distinction between a published comparison result and an identified experimental record.
