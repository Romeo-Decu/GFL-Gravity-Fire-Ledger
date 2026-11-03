# PMMA Source Reconciliation Audit v0.1

**Status:** preliminary documentary audit; not a validated experimental dataset  
**Primary source:** Olson et al., *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385 (October 2021), especially §2.3 and Appendix A.1.  
**Repository branch:** `docs/scientific-system-architecture-v0.1`

## 1. Purpose

Reconcile the PMMA experiments used in §2.3 and Figure 2.20 with the Bhattacharjee test matrix (Appendix A.1), and identify what is and is not established for a FiF transferability test.

## 2. Source structure verified

The report explicitly assigns Appendix A.1 to the **Bhattacharjee Test Matrix**; A.2 is Ferkul, not Bhattacharjee. The report identifies §2.3 as “Opposed-Flow Flame Spread: Comparison of Microgravity and Normal-Gravity Experiments to Establish Thermal Regime.”

Figure 2.20 identifies the BASS-II microgravity PMMA examples as:
- B03: 100 µm
- B11: 200 µm
- B4: 300 µm
- B13: 400 µm

The Appendix A.1 text extraction contains the corresponding test labels as B3, B11, B4 and B13. B03/B3 is therefore a likely formatting difference (zero-padding), but the canonical identifier mapping should be recorded as a cross-reference, not silently normalized.

## 3. Test-level facts visible in Appendix A.1

The Appendix A.1 matrix includes, among other fields:
- test number and sample number (distinct identifiers);
- material description and nominal dimensions;
- igniter and flow restrictor;
- fan display and air display;
- radiometer settings and camera acquisition metadata;
- calibrated and uncalibrated initial/final O2 values;
- initial/final CO2 and CO;
- operational observations and anomalies.

The B3 row is identified in the independent MicroFire Atlas transcription as a 100-µm PMMA film, 2 cm wide, opposed flow. That transcription reports 20.9 vol% in NASA's “Calibrated initial O2” column and 20.5 vol% in the corresponding final column, while preserving the crew/ground note “Probably 20.6 O2 to start”. The Atlas page explicitly flags the oxygen reading as possibly inaccurate and distinguishes enclosure gas readings from flame-zone measurements. Because this is a secondary hand transcription and the PDF's extracted multi-column table text is difficult to align reliably, FiF must not import these values as verified until the rendered NASA table row is checked. **The earlier draft's numeric pair 22.2/21.8 for B3 is withdrawn as unverified and should not be used.**

The B11 row identifies a 2-cm-wide, 0.2-mm PMMA film. The operational notes describe multiple velocities during steady spread and extinction at fan potentiometer setting 0.35. These entries describe a changing-flow test, not a single steady velocity condition.

The B4 row is identified in Figure 2.20 as 300 µm; Appendix A.1 includes a B4 entry described as a 300-µm PMMA film, 2 cm wide.

The B13 row is identified in Figure 2.20 as 400 µm; Appendix A.1 includes a B13 entry described as a 2-cm, 0.4-mm PMMA film. Its table context includes a separate test sequence and operational notes; full row-to-column association must be checked against the rendered page before importing all numeric fields.

**Important:** the extracted PDF text interleaves multi-column table content. Do not build a machine-readable record by copying adjacent extracted lines without checking the rendered page and preserving column alignment.

## 4. Conditions and instrumentation from §2.3

The report states:
- BASS-II and downward tests used a 2-cm-wide PMMA sample; the microgravity opposing flow was controlled in the BASS duct.
- Downward tests used a vertical stainless-steel holder and piloted ignition; the BASS holder had a built-in igniter.
- Downward tests were conducted at 101 kPa and 21% O2.
- Still images from BASS and downward tests were converted to videos and posted at flame.sdsu.edu.
- Flame Analyzer used top-view imagery and threshold-based leading-edge tracking. For the 100-µm comparison, the reported spread-rate uncertainty was below 5% away from ignition; averaging over 5 s produced reproducibility within 5%.
- The 100-µm normal-gravity downward average spread rate was reported as 2.0 mm/s. The highest microgravity spread rate was reported as about 2.2 mm/s, despite variation in opposing flow from about 40 to 1 cm/s. High flow produced kinetic blowoff; very low flow produced radiative extinction.
- The authors interpret the 21% O2 downward PMMA case as thermally controlled with minimal kinetic effect.

The report also explicitly identifies differences in holder and ignition method. These are configuration differences that must remain visible in FiF rather than being hidden by a single “same material” label.

## 5. Material identity and regime limitations

The report describes BASS-II PMMA samples as cast PMMA in its general apparatus description. In §2.3 it discusses extruded PMMA in the downward series, noting considerable dripping and unsteady spread, while cast PMMA is less susceptible to dripping and produces steadier spread. Material manufacturing route is therefore a required comparison field, not a cosmetic metadata field.

The thermal-regime argument assumes a bounded physical regime: chemical kinetics and radiation are negligible in the relevant range, while gas-to-solid conduction governs preheating. The report explains that too-high opposing flow can make finite-rate kinetics important (blowoff), while too-low flow can make radiative losses important (extinction). A change in governing regime invalidates an unqualified transfer of the thin-fuel thermal relationship.

The report's derived results include a de Ris flame coefficient F = 4.76 for 21% O2 / 79% N2 and a transition thickness of approximately 5.2 mm for downward spread in ambient air. These are published NASA results, not FiF reproductions.

## 6. FiF data-handling decisions

1. Preserve the source identifier exactly as printed (B3, B11, B4, B13); maintain a separate figure-label alias (B03 for B3).
2. Keep sample number distinct from test number.
3. Preserve all raw table text, including conflicting oxygen readings and crew notes.
4. Store calibrated and uncalibrated O2 readings as separate fields with source labels.
5. Do not interpret fan potentiometer settings as calibrated flow velocities.
6. Represent changing-flow tests as time-/stage-dependent configurations, not as one scalar flow value.
7. Record holder, ignition method, PMMA manufacturing route, geometry, atmosphere, pressure, flow profile, imaging and image-processing method as explicit configuration variables.
8. Do not treat Figure 2.20's nominal series condition (20.7% O2, 79% N2, 1 atm) as proof of every individual test's measured conditions.
9. Do not claim that the BASS and downward data are fully matched until the original images/videos, downward-run identifiers and materials are reconciled.

## 7. Next verification gates

- Inspect rendered Appendix A.1 pages to confirm exact row/column alignment for B3, B11, B4 and B13.
- Retrieve the corresponding BASS still images and downward videos from the SDSU archive or another verified source.
- Identify the specific normal-gravity run(s) used in Figure 2.19 and establish their material grade, thickness, geometry, holder, ignition, atmosphere and image provenance.
- Determine whether the NASA-reported 2.0 and 2.2 mm/s values can be independently reconstructed from source imagery or reduced time-series.
- Reproduce the thin-fuel formula and transition-thickness calculation independently, with all properties, temperatures and assumptions explicit.
- Define held-out observations and negative/abstention cases before fitting or calibrating any FiF model.

## 8. Current conclusion

The documentary source chain is stronger than before, but it is not yet a validated data chain. The first case remains scientifically promising as a **bounded reproduction and model-domain test**. It is not yet evidence that FiF has independently demonstrated cross-gravity transferability.

No raw video/image dataset has been downloaded or independently analyzed in this audit. No FiF physics engine or predictive model has been implemented.
