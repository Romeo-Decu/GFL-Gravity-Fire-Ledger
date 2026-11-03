# FiF — First Physics Case Selection v0.1

**Date:** 2026-11-03  
**Status:** Provisional case selection; source-backed, pending raw-data verification  
**Selected evidence family:** BASS-II opposed-flow flame spread over PMMA  
**Primary source:** Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385 (October 2021), Section 2.3, pp. 31–44.

## 1. Decision

Select **opposed-flow flame spread over thin PMMA in the thermal regime**, using the BASS-II microgravity experiments and the corresponding normal-gravity downward-spread experiments as a cross-regime comparison case.

The first scientific question is:

> Under what explicitly stated conditions can the thermal-regime flame-spread relationship measured in BASS-II microgravity be transferred to normal-gravity downward spread over PMMA, and where does that transfer cease to be valid?

This is a **model reproduction and validity-boundary test**, not a claim of new combustion physics. The NASA report already performs a comparison and derives a transition thickness. FiF's contribution must be to encode the transfer assumptions, input provenance, uncertainty, domain checks and abstention in a reproducible engine, then test the result on data not used to calibrate the relationship.

## 2. Why this case

The NASA BASS-II summary report provides a rare, unusually well-documented bridge between:
- ISS microgravity experiments in a controlled opposed-flow duct;
- normal-gravity downward flame-spread experiments;
- multiple PMMA thicknesses;
- measured flame spread rates;
- a stated thermal-regime scaling model;
- a comparison of experimental and theoretical behavior.

For the microgravity setup, the report describes 2-cm-wide PMMA samples, approximately 95 mm long, with thicknesses from 100 to 400 µm; O2-N2 mixtures up to 21% O2; measured flow calibration; pressure monitoring; and top-view imaging. The normal-gravity downward tests used a different sample holder and piloted ignition at 101 kPa and 21% O2. These are similar but not identical experimental configurations; apparatus and ignition differences must remain explicit in the transfer model.

The report states that:
- the 100-µm sample had an average downward spread rate of about 2.0 mm/s;
- the highest microgravity spread rate for the same thickness was about 2.2 mm/s over a reported opposed-flow range of approximately 1–40 cm/s;
- spread-rate uncertainty from the image-tracking method was reported as 5% or less away from ignition;
- a de Ris flame coefficient of 4.76 was derived from a 2.2 mm/s thin-fuel result at 50 µm half-thickness;
- the thin/thick transition thickness was estimated as about 5.2 mm for downward spread in ambient air.

These are values reported by NASA authors, not independently reproduced FiF measurements.

## 3. Physical model and transfer hypothesis

The report's Section 2.3 develops thermal-regime thin- and thick-fuel spread relationships and derives a transition thickness by equating the two.

FiF must transcribe the equations from the source carefully, preserving the report's symbol definitions and units. The PDF text extraction renders some mathematical notation imperfectly; equation images and page layout must be checked before implementation.

The physical reasoning to preserve includes:
- thermally thin fuel: the heated solid layer spans the sample half-thickness;
- thermally thick fuel: the heated layer is determined by the balance of gas-to-solid heat transfer and conduction into the solid;
- thin-limit spread rate is independent of opposing-flow velocity under the stated thermal-regime assumptions;
- thick-limit spread rate depends on effective opposing-flow velocity;
- gravity can introduce buoyancy-driven opposing flow and kinetic effects, so normal-gravity downward spread cannot automatically be equated to microgravity opposed flow;
- Damköhler/residence-time effects can invalidate a purely thermal-regime transfer;
- radiative extinction at very low flow and kinetic blowoff at high flow are distinct validity boundaries.

The transfer hypothesis is therefore conditional, not universal:

**H1:** For the selected PMMA material, atmosphere and thermal regime, the thin-fuel spread relation inferred from BASS-II microgravity is consistent with normal-gravity downward-spread measurements within declared experimental and model uncertainty.

**H2:** The relation ceases to be transferable when the governing regime changes (for example, kinetic/buoyancy influence, radiative extinction, or the transition to thermally thick behavior).

## 4. Initial data anchors

| Evidence | Reported value / condition | Role |
|---|---|---|
| BASS-II B03 | 100 µm PMMA, 2 cm wide, ISS microgravity | Microgravity anchor |
| BASS-II B11 | 200 µm PMMA | Thickness-series evidence |
| BASS-II B4 | 300 µm PMMA | Thickness-series evidence |
| BASS-II B13 | 400 µm PMMA | Thickness-series evidence |
| Microgravity thin-fuel result | Maximum spread rate about 2.2 mm/s at 100 µm | Reported thin-limit calibration anchor; verify exact test/flow context |
| Normal-gravity downward result | About 2.0 mm/s at 100 µm | Cross-gravity comparison |
| Reported image-tracking uncertainty | ≤5% away from ignition | Measurement uncertainty input, not total uncertainty |
| Reported transition thickness | About 5.2 mm in downward ambient air | Published model output to reproduce independently |

The NASA report's Figure 2.20 labels the microgravity images B03 (100 µm), B11 (200 µm), B4 (300 µm), B13 (400 µm), and corresponding normal-gravity comparison images. This does not yet prove the full numeric record linkage for each test. The report's Appendix A test matrices and PSI raw records must be reconciled before creating a machine-readable fixture.

## 5. Data and provenance gate

No numerical model implementation is authorized until these items are checked:

1. Inspect the complete PDF pages for Section 2.3, including equations, figures and captions.
2. Inspect Appendix A.2 and any relevant PI test matrix to reconcile test identifiers, sample IDs, thicknesses, widths, flow values, O2, pressure and spread-rate values.
3. Retrieve the original still images/videos or reduced time-series for the selected BASS-II runs, where available.
4. Identify the normal-gravity downward-spread dataset and its raw/reduced provenance; do not assume it is contained in PSI-25.
5. Verify material grade and manufacturing route (cast/extruded), because the report notes dripping and unsteady spread for extruded PMMA versus steadier spread for cast PMMA.
6. Record sample holder, ignition method, image resolution, frame interval, tracking threshold, calibration and data reduction method.
7. Separate reported uncertainty (e.g. ≤5% image tracking) from uncertainty in material properties, model parameters, apparatus differences and model form.

If any critical field cannot be verified, it remains unknown and the corresponding transfer conclusion is limited or withheld.

## 6. Validation design

Do not calibrate and validate against the same observations.

Proposed sequence:
- **Reproduction:** independently reproduce the published thin-limit coefficient and transition-thickness calculation from the report's equations and stated properties.
- **Within-family check:** use a subset of thickness observations to test the predicted trend, holding at least one thickness/run out where data permit.
- **Cross-configuration check:** test against the normal-gravity downward-spread measurements, explicitly accounting for the different holder, ignition and buoyancy environment.
- **Regime-boundary check:** test cases near radiative extinction, kinetic blowoff, and the thin-to-thick transition as negative/abstention cases for the simple thermal model.
- **Sensitivity:** quantify how uncertainty in spread rate, thickness, thermal conductivity, density, specific heat, flame coefficient and effective flow changes the predicted result.

A result that only reproduces the report's own calibration point is not a successful validation.

## 7. What this case will and will not demonstrate

### It can demonstrate
- provenance-aware extraction of experimental conditions and outcomes;
- a machine-readable physical model with explicit assumptions;
- a bounded transfer calculation across two gravity/configuration contexts;
- uncertainty propagation and model-domain checks;
- reasoned abstention when the thermal-regime assumptions fail.

### It cannot yet demonstrate
- universal transferability across solid fuels;
- predictive spacecraft fire safety;
- generalization to SAFFIRE or gaseous/liquid combustion;
- a novel flame-spread law;
- independent experimental validation until raw/reduced data and held-out cases are verified.

## 8. Decision gate

Proceed to a computational proof only if the source audit yields a traceable subset with:
- verified experiment/sample linkage;
- sufficiently complete physical conditions;
- spread-rate observations and uncertainty;
- verified PMMA properties or a defensible property range;
- an independently identifiable validation subset.

Otherwise, change the first case rather than fill missing inputs with assumptions.

## 9. Sources

1. Olson, S. L. et al. (2021). *Burning and Suppression of Solids-II (BASS-II) Summary Report*. NASA/TM-20210011385. https://ntrs.nasa.gov/citations/20210011385
2. NASA Physical Sciences Informatics, PSI-25, BASS-II, DOI 10.60555/4qc4-de67. https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
3. Bhattacharjee et al., *Opposed-flow flame spread: A comparison of microgravity and normal gravity experiments to establish the thermal regime*. Fire Safety Journal (2016). https://www.sciencedirect.com/science/article/pii/S0379711215300424

---

**Status:** Selected provisionally. No model has been coded, no raw video has been analyzed, and no published result has been independently reproduced at this stage.
