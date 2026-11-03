> **Correction notice — 2026-11-03:** This update's earlier wording overstated the linkage between B3/B03 and the Section 2.3 spread-rate comparison. NASA Figure 2.20 labels B03 as the 100-µm microgravity image, and Appendix A.1 contains a B3 100-µm record, but the direct join to the Section 2.3 2.2-mm/s result is not established. Section 2.3 states 3 cm/s for the comparison microgravity experiment, whereas Appendix A.1 reports 2 cm/s in the B3 Air display field. Section 2.2's separate 2.2-mm/s extinction experiment must not be assigned to B3. The normal-gravity 100-µm NASA PMMA specimen is identified in Figure 2.20, but its run/sample identifier and raw-data linkage remain unknown. See `research/SECTION_2_3_100UM_DATA_LINKAGE_AUDIT_2026-11-03.md`. The earlier text below is retained as decision history and is superseded wherever it conflicts with this notice.

# FiF — PMMA Case Selection Update

**Date:** 2026-11-03  
**Applies to:** FIRST_PHYSICS_CASE_SELECTION_v0.1.md  
**Status:** Decision update; supersedes conflicting scope details in the earlier selection note.

## 1. Correct source-matrix reference

The correct test matrix for the Bhattacharjee experiments is **Appendix A.1 — Bhattacharjee Test Matrix** in NASA/TM-20210011385. Appendix A.2 is the Ferkul matrix. The earlier selection note's instruction to inspect Appendix A.2 was incorrect.

## 2. Revised first-case scope

Restrict the first computational case to the 100-µm PMMA comparison:

- Microgravity: BASS-II B03/B3, 100 µm, 20 mm wide, ISS.
- Normal gravity: 100-µm NASA PMMA downward-spread sample at SDSU, as identified in Figure 2.20.

Figure 2.20 identifies both 100-µm specimens as NASA PMMA. This is only a supplier-level match. Grade, batch, manufacturing route, thermal properties, and specimen history remain to be verified.

## 3. Why the four-thickness set is not a matched validation set

The Figure 2.20 caption describes the image array at 20.7% O2 / 79% N2 / 1 atm. The independent hand transcription of NASA Table A.1 published by MicroFire Atlas reports test-specific initial O2 values of 20.9% for B3 (flagged as possibly inaccurate), 20.6% for B4, and 20.1% for B11 and B13. B11 and B13 also contain changing-flow sequences and extinction during flow reduction.

Therefore:
- Do not treat B03/B3, B11, B4 and B13 as a four-point, matched-atmosphere validation series.
- Do not use the B11/B13 changing-flow sequences as single steady-flow points.
- Retain B4/B11/B13 as contextual thickness/regime evidence only.
- Do not assume the figure caption's nominal atmosphere describes each individual table record.
- Treat B3's initial oxygen condition as disputed until the rendered NASA row and original experimental record are checked.

The MicroFire Atlas records are secondary hand transcriptions, useful for cross-checking but not substitutes for NASA's original data or imagery.

## 4. Data gate before any model implementation

The 100-µm comparison remains provisional. Before a numerical transfer calculation is accepted, FiF must verify:
1. B03/B3 identifier and sample linkage.
2. Actual oxygen and pressure conditions for the microgravity run.
3. Material grade, manufacturing route, batch and thermal properties for both samples.
4. Original BASS still images and SDSU normal-gravity video or reduced time series.
5. The exact normal-gravity run corresponding to the 100-µm NASA specimen.
6. Image scale, frame interval, tracking threshold, calibration and uncertainty.
7. Reproducibility of the reported 2.2 mm/s and 2.0 mm/s values from traceable source data.

If these cannot be verified, FiF must keep the disputed variables unknown and withhold a quantitative transfer conclusion.

## 5. Decision

The first case remains **opposed-flow flame spread over 100-µm PMMA in the thermal regime**, but only as a bounded reproduction and validity-boundary study. No four-thickness matched dataset is claimed. No raw video has yet been downloaded or independently analyzed, and no FiF model has been implemented.
