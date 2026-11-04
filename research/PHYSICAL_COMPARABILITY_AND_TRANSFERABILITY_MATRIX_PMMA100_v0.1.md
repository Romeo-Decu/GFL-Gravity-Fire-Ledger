# FiF — Physical Comparability & Evidence Transferability Matrix
**Case:** 100-µm PMMA, BASS-II microgravity opposed-flow vs normal-gravity downward spread  
**Version:** 0.1 | **Date:** 2026-11-04  
**Status:** Evidence assessment; not a validated transfer model

## 1. Purpose and outcome

This matrix evaluates whether published BASS-II microgravity evidence can inform the NASA normal-gravity downward flame-spread result for nominally 100-µm PMMA.

Three questions remain separate:
1. **Documentary linkage:** is each result tied to a specific experiment, sample, run and source asset?
2. **Physical comparability:** are governing variables sufficiently aligned for flame-spread rate?
3. **Evidence transferability:** within what bounded domain can one result inform the other?

The target observable is flame-spread rate derived from leading-edge position versus time.

NASA/TM-20210011385 Section 2.3 reports approximately 2.0 mm/s average for normal-gravity downward spread and a maximum approximately 2.2 mm/s for microgravity 100-µm PMMA. It describes 3 cm/s opposing flow for the microgravity comparison and interprets the downward case as thermally controlled with minimal kinetic influence. These are source-reported results; FiF has not independently reconstructed either rate.

BASS-II B3, sample 148, is a candidate record: Appendix A.1 identifies 100-µm PMMA, 20-mm width, and 2 cm/s air display. Carmignani (2019), Appendix A, Table A.2, independently lists B3 as 0.1-mm PMMA, 20-mm width, flow 2–0 cm/s, oxygen 22.2%. This corroborates B3 metadata, but does not link B3 to the Section 2.3 result. The separate Section 2.2 2.2-mm/s extinction-study result must not be assigned to B3.

The normal-gravity Figure 2.20 specimen is identified as NASA PMMA, 100 µm. The audited source does not provide its run ID, sample ID, batch ID, raw-video filename or reduced-data row.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| Aligned / supported | Evidence supports alignment for this outcome and purpose. |
| Intentional contrast | Deliberately different variable central to the question. |
| Manageable difference | Could be bounded or normalized if required evidence exists. |
| Critical mismatch / unresolved | May alter governing physics; evidence missing or contradictory. |
| Unknown | Source does not establish the value. Unknown is not compatible. |

No weighted aggregate score is used. A weighted score could hide a regime-changing mismatch behind multiple low-impact matches.

## 3. Physical comparability matrix

| Dimension | BASS-II microgravity | Normal-gravity downward | Status | Transfer consequence |
|---|---|---|---|---|
| Fuel family | PMMA | NASA PMMA | Aligned at family level | Does not prove formulation equivalence. |
| Grade / batch | Exact grade and batch unknown | Exact grade and batch unknown | Critical unresolved | Formulation, additives and manufacturing history can affect pyrolysis and heat feedback. |
| Nominal thickness | 100 µm in B3 metadata / Fig. 2.20 | 100 µm in Fig. 2.20 / Section 2.3 | Aligned nominally | Actual measured thickness and tolerance remain unknown. |
| Thickness method / tolerance | Unknown | Unknown | Unknown | Nominal labels are not measurements; thickness affects thermal inertia. |
| Width | 20 mm | 20 mm | Aligned at reported level | Reduces one geometric difference; edge and holder effects remain. |
| Length | BASS samples approximately 95 mm | Target ground length unknown | Manageable / unresolved | May limit steady propagation distance and fit window. |
| Thermal properties | No target-specimen density, heat capacity or conductivity established | Same | Critical for prediction | Quantitative de Ris-type prediction cannot be reproduced without defensible properties and conventions. |
| Oxidizer | O2/N2; caption nominal 20.7% O2 / 79% N2 / 1 atm; B3 calibrated O2 22.2/21.8%, uncalibrated 20.9/20.5% | Caption nominal 20.7% O2 / 79% N2 / 1 atm; prose says 21% O2 | Manageable only after provenance resolution | Caption values and B3 sensor readings are not interchangeable. |
| O2 calibration / scope | CSA-CP offset using MCA daily; calibrated and uncalibrated initial/final working-volume readings | Exact run-level O2 record not supplied | Critical unresolved | Cannot assert identical local flame-zone oxygen. |
| Diluent | Nitrogen in Fig. 2.20 caption | Nitrogen in Fig. 2.20 caption | Aligned at caption level | Nominal mixture similarity only; run-level composition unverified. |
| Pressure | Section 2.3: 99.2–99.5 kPa; caption: 1 atm | Section 2.3: 101 kPa; caption: 1 atm | Manageable / reporting inconsistency | Preserve body values and caption shorthand separately. |
| Gravity | ISS microgravity | Earth gravity | Intentional contrast | Buoyancy and natural convection alter the flow field. |
| Orientation | BASS opposed-flow configuration; exact target geometry needs confirmation | Downward spread | Intentional contrast; incomplete geometry | Gravity vector relative to sample and propagation direction matters. |
| Flow origin | Fan-driven forced opposed O2/N2 flow | Downward configuration with buoyancy contribution | Intentional contrast | Nominal forced flow and buoyancy-driven local flow are not interchangeable. |
| Opposing-flow velocity | Section 2.3: 3 cm/s; B3 Appendix A.1: 2 cm/s; Carmignani: 2–0 cm/s | Matched local velocity unknown | Critical mismatch | Do not average or harmonize 2 and 3 cm/s. |
| Velocity measurement | BASS hot-wire calibration; fan display distinct from air display | Equivalent run-level local velocity not established | Critical unresolved | Fan display, calibrated bulk velocity and leading-edge velocity differ. |
| Flow regime | NASA interprets target as thermal; broader BASS series includes kinetic blow-off and radiative extinction limits | NASA interprets downward case as thermally controlled | Conditional alignment by source interpretation | FiF has not independently verified regime inequalities or distance from boundaries. |
| Radiation | Target-specific radiative balance not quantified | Target-specific radiative balance not quantified | Unknown / potentially critical | Cannot assume radiation negligible from nominal flow alone. |
| Holder / mounting | BASS holder with built-in igniter | Stainless-steel holder / Flame Stabilizer | Critical difference | Contact conduction, heat sinking, edge conditions and flow disturbance may differ. |
| Ignition | Built-in Kanthal hot-wire ignition | Piloted ignition | Critical for transients | Exclude ignition transient and establish stable propagation interval. |
| Stabilization / apparatus | BASS duct, fan and flow conditioning | Ground Flame Stabilizer / stainless-steel holder | Critical / incompletely characterized | Apparatus boundary conditions may affect leading-edge region. |
| Imaging / view | Top-view BASS processing described; target asset not inspected | Downward videos described; target asset not inspected | Unknown at asset level | Camera, view, frame rate and spatial calibration cannot be assumed identical. |
| Image threshold | Section 2.3.6 does not state threshold for target 100-µm pair | Target threshold unknown | Critical unresolved | Threshold 30 is from separate Section 2.2 study; 70 is a 75-µm Figure 2.18 example. Neither is verified for this pair. |
| Processing method | Width-averaged intensity, fixed threshold, leading-edge tracking and linear regression described | Same general method described; exact settings unverified | Conditional at method-description level | Exact settings, calibration and fit window required for reproduction. |
| Spread-rate statistic | Microgravity maximum approx. 2.2 mm/s; B3 linkage unresolved | Downward average approx. 2.0 mm/s; run join unresolved | Summary-level only | Maximum and average are not equivalent statistics; proximity is suggestive, not validation. |
| Uncertainty | NASA reports <5% away from ignition and 5-s averages reproducible within 5%; FiF has not reproduced it | Same report-level statement; run-specific uncertainty unavailable | Source-reported only | Do not inherit NASA uncertainty as FiF uncertainty. |
| Run/sample provenance | B3/sample 148 metadata exists; Section 2.3 result join unresolved | Figure specimen identified; ground run/sample IDs missing | Critical mismatch | No complete raw asset → run → sample → outcome chain. |
| Raw/reduced data | PSI-25 candidate B3 assets; user ZIP inaccessible to FiF; SDSU archive access unverified | NASA names SDSU archive; target ground asset not verified | Critical unresolved | No independent trajectory reconstruction or regression yet. |

## 4. What is aligned, contrasted, or blocking

### Nominal similarities
- PMMA family;
- nominal 100-µm thickness;
- 20-mm width;
- O2/N2 atmosphere near air-like oxygen concentration;
- flame-spread rate as the primary observable.

These justify investigation, not a claim of physical equivalence.

### Intentional contrasts
- microgravity versus Earth gravity;
- forced fan-driven opposed flow versus normal-gravity downward flow with buoyancy;
- apparatus and sample support;
- ignition method.

These differences are part of the scientific question. Their effects must still be characterized; they cannot be erased by describing the tests as differing only in gravity.

### Potentially manageable
- pressure difference (99.2–99.5 versus 101 kPa);
- nominal oxygen near 21%, if calibration and run conditions are resolved;
- sample-length difference, if a stable propagation interval exists.

Manageable means a path to bounding the effect exists, not that it has already been corrected.

### Critical blockers
1. 2 cm/s in B3 Appendix A.1 versus 3 cm/s in Section 2.3.
2. No direct linkage of B3/sample 148 to the Section 2.3 2.2-mm/s result.
3. No identified ground run/sample/video join for the 2.0-mm/s result.
4. Unknown PMMA grade, batch and thermal properties.
5. Unknown actual thickness and tolerance.
6. No matched local flow-field measurement.
7. Unknown target 100-µm image threshold and exact settings.
8. No independent video reconstruction by FiF.

Blockers 1–3 alone prevent a claim of independently validated matched-pair evidence.

## 5. Outcome-specific transfer decision

| Intended use | Decision | Reason |
|---|---|---|
| State that NASA reports nominal 100-µm PMMA spread rates around 2.0–2.2 mm/s in the Section 2.3 comparison | **Conditionally informative** | Valid as a qualified summary-level statement only; preserve average versus maximum. |
| Claim BASS B3 specifically measured the Section 2.3 2.2 mm/s result | **Insufficient evidence** | Result-to-B3 linkage unresolved. |
| Claim gravity alone caused no meaningful change | **Not supported** | Other apparatus, flow, ignition, holder and provenance differences remain. |
| Motivate a bounded thermal-regime hypothesis | **Conditionally informative** | NASA's regime interpretation is a testable source claim, not FiF confirmation. |
| Calibrate or validate a quantitative predictive model | **Insufficient evidence** | No independent reconstruction, matched records, thermal properties or full uncertainty budget. |
| Transfer to other PMMA thicknesses/formulations, atmospheres, flow regimes or spacecraft scenarios | **Not transferable on current evidence** | No wider validated domain established. |
| Represent as a literature case with explicit caveats and abstention | **Supported with provenance caveats** | Evidence and unknowns can be represented transparently. |

**Overall verdict:** conditionally informative as a published bounded comparison; insufficient evidence for independent quantitative transfer validation.

## 6. Transfer gates

| Gate | Required evidence | Current status |
|---|---|---|
| 1. Record identity | Both run/sample IDs; each result linked to original video, image sequence or reduced data | **FAIL / OPEN** — B3 metadata exists; result join incomplete; ground identity missing |
| 2. Observable / method | Leading-edge definition; frame rate; spatial calibration; threshold/settings or declared FiF reconstruction; fit window; independent uncertainty | **OPEN** |
| 3. Material / geometry | Measured thickness and tolerance; grade/batch; geometry/mounting; thermal properties for model transfer | **PARTIAL** |
| 4. Atmosphere / flow | Run-specific O2/diluent and calibration; pressure; calibrated flow and reference frame; local velocity; resolve 2 vs 3 cm/s | **FAIL / OPEN** |
| 5. Regime equivalence | Evaluate Vg >> Vf, chemistry faster than gas residence, radiation not dominant, thermally thin condition, distance from regime boundaries | **PARTIAL** — NASA interpretation documented; FiF has not independently tested it |
| 6. Boundary sensitivity | Holder/contact heat loss, ignition, duct/stabilizer and flow-conditioning effects | **OPEN** |
| 7. Quantitative consistency | Reconstruct histories; calculate rates reproducibly; independent uncertainty per run; preserve max vs average | **FAIL / OPEN** |
| 8. Domain / abstention | Exact domain and exclusions stated; abstain when critical conditions unknown | **PASS for documentary specification only**, not physical validation |

## 7. Minimum evidence to upgrade

**P0 — Close linkage**
1. Locate the SDSU BASS and downward video assets identified by NASA.
2. Inspect PSI-25 B3 candidate files and archive members when accessible to FiF.
3. Locate the exact normal-gravity 100-µm NASA PMMA video and run/sample metadata.
4. Resolve 2 versus 3 cm/s and whether B3 is the relevant run.

**P1 — Reconstruct the observable**
5. Establish frame timing, spatial calibration, view and image-processing method for each asset.
6. Recover NASA's threshold; if unavailable, conduct threshold sensitivity analysis and label the threshold as FiF's choice.
7. Reconstruct leading-edge trajectories and spread-rate histories with transparent fit windows.
8. Calculate a FiF uncertainty budget; do not inherit NASA's <5% statement.

**P2 — Close physical comparability**
9. Recover grade/batch, measured thickness and thermal properties where possible.
10. Establish atmosphere and flow measurement provenance.
11. Quantify holder, ignition and apparatus effects or retain them as unresolved.
12. Independently assess thermal-regime assumptions and proximity to kinetic/radiative boundaries.

Only after P0–P2 should quantitative calibration or validation be considered.

## 8. Proposed machine-readable representation

Conceptual schema only; not an implemented database contract.

~~~yaml
comparison:
  id: bassii_b3_vs_nasa_downward_pm ma100
  outcome:
    name: flame_spread_rate
    operational_definition: leading_edge_position_vs_time_slope
    unit: mm/s
  evidence_status:
    documentary_linkage: unresolved
    physical_comparability: conditional
    quantitative_validation: insufficient_evidence
  dimensions:
    - id: nominal_thickness
      class: aligned
      microgravity: 100_um
      normal_gravity: 100_um
    - id: opposing_flow
      class: critical_unresolved
      microgravity_section_2_3: 3_cm_s
      microgravity_appendix_A1_B3: 2_cm_s
      normal_gravity_local_velocity: unknown
    - id: gravity
      class: intentional_contrast
      microgravity: ISS_microgravity
      normal_gravity: 1_g
  gates:
    record_identity: fail
    measurement_equivalence: open
    material_geometry: partial
    atmosphere_flow: fail
    regime_equivalence: partial
    boundary_sensitivity: open
    quantitative_consistency: fail
    domain_statement: pass
  decision:
    status: conditionally_informative
    permitted_claim: published_summary_level_comparison_only
  abstention:
    reason: critical_run_level_links_and_conditions_unresolved
~~~

Before implementation, normalize controlled vocabularies, source references, units, uncertainty representation and evidence-state transitions.

## 9. Rules derived for FiF

1. Comparability is outcome-specific.
2. A nominal match is not a measurement match.
3. A deliberate contrast is not a nuisance variable.
4. Apparatus differences remain causal candidates.
5. Summary values do not establish record identity.
6. Unknown is not compatible.
7. Do not average contradictions.
8. Preserve statistic type: maximum is not average or steady-state rate.
9. Do not inherit source uncertainty.
10. Abstention is a valid output; do not manufacture a confidence score.

## 10. Sources and related FiF records

**Primary:** Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385 (2021).
- https://ntrs.nasa.gov/citations/20210011385
- https://ntrs.nasa.gov/api/citations/20210011385/downloads/TM-20210011385.pdf
- Relevant: Section 2.3.3–2.3.7; Figures 2.18–2.20; Appendix A.1, Table A.1.

**Cross-source:** Carmignani (2019), *Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes*, UC San Diego / SDSU dissertation.
- https://escholarship.org/uc/item/0rb693zc
- Appendix A, Table A.2: B3 metadata (0.1-mm PMMA, 20-mm width, 2–0 cm/s, 22.2% O2).

Related FiF records:
- research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md
- research/SECTION_2_3_100UM_DATA_LINKAGE_AUDIT_2026-11-03.md
- research/CARMIGNANI_2019_BASS_B3_CROSS_SOURCE_AUDIT_2026-11-03.md
- research/SDSU_VIDEO_ARCHIVE_AND_FLAME_ANALYSIS_AUDIT_2026-11-04.md
- research/VIDEO_MEASUREMENT_AND_UNCERTAINTY_PROTOCOL_v0.1.md

## 11. Scope boundary

This matrix does not claim that FiF inspected the B3 ZIP or target videos, independently reproduced NASA's 2.0/2.2 mm/s values, validated the de Ris model numerically, established gravity as the only changed variable, or authorized extrapolation to other fuels, thicknesses, atmospheres, geometries, spacecraft scenarios or operational safety decisions.

**Bottom line:** the NASA comparison is valuable enough to motivate a rigorous transferability test. Current evidence supports a qualified literature-level comparison, not a completed matched-experiment validation. Close provenance and reconstruct the observable before building a quantitative transfer engine.
