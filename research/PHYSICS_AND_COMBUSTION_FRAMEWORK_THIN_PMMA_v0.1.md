# FiF — Physics & Combustion Framework: Thin-PMMA Opposed-Flow Case v0.1

**Date:** 2026-11-04  
**Status:** Scientific framework / design basis; not a validated numerical model  
**Scope:** 100-µm PMMA sheet, opposed-flow flame spread in BASS-II microgravity and normal-gravity downward configuration  
**Primary outcome:** Steady or interval-specific flame-spread rate  
**Primary purpose:** Establish experiment comparability and evidence-transfer limits for this outcome

---

## 1. Scientific question and bounded claim

**Question**

Under what explicitly stated physical and experimental conditions can evidence about flame-spread rate over a 100-µm PMMA sheet in BASS-II microgravity inform normal-gravity downward flame spread, and where does that transfer cease to be valid?

**Bounded working hypothesis**

For the specific 100-µm PMMA configuration and the tested atmosphere near 21 vol% oxygen at approximately atmospheric pressure, the published BASS-II microgravity and normal-gravity downward results are consistent with a thermally controlled spread-rate regime, within the limits of the source evidence and experimental uncertainty.

This is a hypothesis to audit and test. It is not a universal statement about PMMA, spacecraft fires, all microgravity flames, or all opposed-flow configurations.

**Target observable**

The primary observable is flame-front position as a function of time, from which a steady or interval-specific spread rate is estimated. Flame shape, extinction, and flow response are secondary observables and must not be silently substituted for spread rate.

## 2. Physical mechanism: continuous ignition of virgin fuel

Opposed-flow flame spread over a solid fuel can be understood as a continuous ignition process:

1. The established flame transfers heat to virgin solid ahead of the leading edge.
2. The solid preheats and reaches conditions for thermal decomposition / fuel-vapour release.
3. Fuel vapour mixes with the oxidizer.
4. Gas-phase reaction releases heat and sustains the flame.
5. Heat feedback advances the preheat and pyrolysis front.

The leading-edge process couples gas-phase transport and chemistry with solid-phase heating and decomposition. It is therefore not adequately represented by a single ambient variable such as oxygen concentration or flow velocity.

For this case, FiF must distinguish:
- flame leading edge;
- solid preheat region;
- pyrolysis / fuel-vapour generation region;
- gas-phase reaction zone;
- extinction or blow-off boundary.

The exact spatial definitions depend on camera view and diagnostic method. A visible luminous front is not automatically identical to the pyrolysis front or the solid thermal front.

## 3. Three competing regimes

NASA/TM-20210011385 Section 2.3 and the cited opposed-flow literature describe three relevant regimes for thin-solid opposed-flow flame spread.

### 3.1 Thermal regime

The dominant feedback sustaining spread is gas-to-solid heat transfer, with the preheat process setting the spread rate. In the simplified scale analysis:
- gas-phase conduction supplies heat to the virgin solid;
- the gas preheat length is approximately (L_g \sim \alpha_g/V_g);
- the gas residence time is approximately (t_{g,res} \sim \alpha_g/V_g^2);
- the solid residence time is approximately (t_{s,res} \sim \alpha_g/(V_g V_f)).

Here (\alpha_g) is gas thermal diffusivity evaluated consistently with the model, (V_g) is opposing-flow velocity in the flame reference frame (subject to the report's velocity convention), and (V_f) is flame-spread rate.

The thermal-regime assumptions include:
- (V_g \gg V_f), so the solid residence time is much greater than the gas residence time;
- gas-phase chemistry is fast relative to gas residence time;
- the flame is not so slow-flowing that radiation dominates;
- forward conduction in the solid is sufficiently small for the selected homogeneous thin-fuel approximation;
- the fuel is thermally thin across its thickness.

These are scale-analysis assumptions, not universal pass/fail constants. Each must be evaluated with the actual experiment's definitions, properties and uncertainty.

### 3.2 Kinetic regime

At sufficiently high opposing-flow velocity, gas residence time decreases. If it becomes comparable to the gas-phase chemical time, finite-rate chemistry affects the leading edge and flame spread can become kinetically limited; at the boundary, blow-off extinction can occur.

A useful conceptual ratio is:

\[
Da_{lead} = \frac{t_{g,res}}{t_{g,chem}}
\]

This is the residence-time / chemical-time convention used in the NASA discussion. A decrease in this ratio as opposing flow rises signals increasing kinetic limitation. The actual chemical time requires a justified kinetic model or experimentally supported estimate. It must not be replaced by an arbitrary Arrhenius-looking expression.

### 3.3 Radiative regime

At sufficiently low opposing-flow velocity, gas residence time becomes long and radiative effects can no longer be neglected. Radiative loss and feedback can alter the preheat balance and may cause extinction.

FiF must retain radiative effects as a distinct mechanism. It must not classify every low-flow extinction as kinetic blow-off or treat the thermal model as valid down to zero flow.

### 3.4 Regime classification is a prerequisite to transfer

A result from one regime cannot be transferred as though it were a result from another regime merely because the material, oxygen concentration, or nominal gravity level is similar.

For the selected case, the intended transfer is specifically between two observations argued by the NASA authors to lie in the thermal regime. FiF must independently assess whether the source evidence supports that classification and how much uncertainty remains.

## 4. Thermal-regime thin-fuel scaling

NASA Section 2.3 presents a de Ris-type thin-fuel expression. In structural form:

\[
V_{f,thin} \propto
\frac{\lambda_g}{\rho_s c_s \tau}
\,F
\]

where:
- (\lambda_g): gas thermal conductivity at the model's selected evaluation temperature;
- (\rho_s): solid density;
- (c_s): solid specific heat;
- (\tau): fuel half-thickness;
- (F): flame coefficient determined from the selected flame, vaporization and ambient temperatures.

The NASA report uses a (\pi/4) factor in its modified expression and reports a fitted coefficient for the stated oxygen/nitrogen mixture. The precise numerical implementation must follow the source equation and its stated property conventions; this framework deliberately does not hard-code a numerical prediction.

**Interpretation:** within the thin-fuel thermal regime, the simplified spread-rate expression is independent of opposing-flow velocity. For thermally thick fuel, the scaling changes and the spread rate depends on the opposing flow.

This is a regime-specific scaling relation, not a universal PMMA law. The NASA report itself notes ambiguity in accepted procedures for evaluating gas properties, flame temperature, vaporization temperature and boundary-layer effects. FiF must expose these choices as model inputs and assumptions.

## 5. Thermally thin versus thermally thick

The thin-fuel approximation requires the heated depth in the solid to span the fuel thickness. In NASA's scale analysis, a thermally thin fuel has (L_{sy} \approx \tau), where (L_{sy}) is the solid heating length and (\tau) is half-thickness.

A transition-thickness estimate follows from the thick-limit scale analysis, but its evaluation depends on material properties, gas properties, flame coefficient and the selected flow convention.

For this case:
- target sample thickness is 100 µm;
- target half-thickness is 50 µm;
- the NASA report's broader thickness series includes 100, 200, 300 and 400 µm;
- these thicknesses must not be treated as a matched validation series without run-level evidence and consistent conditions.

The report's transition thickness for downward spread is a contextual model result, not proof that all tests at every thickness share identical regimes.

## 6. Physical variables and evidence requirements

The variables below are grouped by their role in the selected outcome. A field can be reported, measured, derived, inferred or unknown. FiF must preserve that epistemic status.

| Variable / descriptor | Physical role | Minimum evidence / treatment |
|---|---|---|
| Fuel identity and formulation | Solid decomposition and thermal response | Material, grade, supplier, batch and manufacturing route where available |
| Fuel thickness (\delta) and half-thickness (\tau) | Thin/thick regime and solid heating | Measured value, tolerance, measurement method |
| Sample width and length | Geometry, edge effects, finite-width effects | Actual dimensions and mounting orientation |
| Density (\rho_s) | Solid thermal inertia | Source-specific value and temperature basis |
| Specific heat (c_s(T)) | Solid thermal inertia | Temperature-dependent data or justified constant approximation |
| Thermal conductivity (\lambda_s(T)) | Internal heat transport | Directional properties if anisotropic; do not assume isotropy for composites |
| Gas conductivity (\lambda_g(T)), diffusivity (\alpha_g(T)) | Gas preheat transport | Composition, pressure and evaluation temperature |
| Vaporization / pyrolysis temperature (T_v) | Onset of fuel-vapour release in simplified model | Definition and source; distinguish from ignition temperature |
| Flame temperature (T_f) | Flame coefficient / heat feedback | Measured, calculated or model-assumed; never mix definitions silently |
| Oxygen mole fraction (X_{O2}) | Oxidizer availability and kinetics | Initial/final readings, calibration status, spatial/temporal scope |
| Diluent composition | Diffusion, heat capacity, conductivity and chemistry | Identify N2 or other balance gas; equal O2 alone is insufficient |
| Pressure (P) | Density, transport and chemistry | Absolute pressure, time and uncertainty |
| Opposing-flow velocity (V_g) | Residence time and regime | Measured/calibrated value, location, response time and reference frame |
| Gravity / acceleration | Buoyancy-driven flow | Nominal gravity and residual acceleration where available |
| Orientation | Buoyancy direction relative to spread | Explicit sample orientation and propagation direction |
| Holder / boundary condition | Heat loss, contact and flow disturbance | Material, geometry, contact and thermal boundary |
| Ignition method | Initial condition and early transient | Igniter type, location, duration; exclude ignition transient from steady fit |
| Radiative properties | Loss / feedback | Emissivity, participating-gas assumptions, radiometer calibration |
| Flame-spread rate (V_f) | Primary outcome | Reconstructed measurement, fit interval, uncertainty and method |
| Extinction / blow-off | Regime boundary | Event definition and independently documented flow/oxygen condition |

### Critical distinction: measured local flow versus nominal apparatus setting

A fan voltage, potentiometer value, displayed airspeed, calibrated airspeed and effective velocity at the flame leading edge are not interchangeable. The source and calibration path must be retained. Boundary-layer development may cause the flame to encounter a velocity different from a nominal bulk value.

## 7. Dimensionless and scale-analysis descriptors

FiF must not calculate every familiar dimensionless number by default. It should calculate only those supported by the physical question, available inputs and a clearly defined characteristic length and velocity.

### 7.1 Residence-time ratio / Damköhler descriptor

Use the NASA convention for the leading-edge gas residence time relative to gas-phase chemical time:

\[
Da_{lead}=t_{g,res}/t_{g,chem}
\]

Purpose: assess whether finite-rate chemistry can affect the leading edge. It requires a defensible estimate of chemical time. If kinetics are unavailable, record (Da_{lead}) as not computable rather than manufacture a value.

### 7.2 Thermal Péclet descriptor

For a specified length (L) and velocity (U):

\[
Pe_T=\frac{UL}{\alpha_g}
\]

Purpose: compare advective and thermal-diffusive transport for a defined flow region. The characteristic (L), (U), gas properties and frame of reference must be recorded. Do not use one arbitrary fixed length for all geometries.

### 7.3 Solid thermal-diffusion descriptor

For a selected heating time (t) and half-thickness (\tau):

\[
Fo_s=\frac{\alpha_s t}{\tau^2}
\]

Purpose: assess whether heat can diffuse across the fuel thickness over the relevant preheat time. The relevant time must be derived from the flame/solid process, not selected merely to force a thin-fuel classification.

### 7.4 Radiation-to-heating comparison

Compare the relevant radiative timescale with solid or gas residence time, following the NASA scale analysis. This requires emissivity, relevant temperatures, participating-gas assumptions and geometry. If these are missing, radiation's relative importance remains unquantified; observed radiative extinction can still be retained as direct evidence.

### 7.5 Gravity / buoyancy descriptor

A buoyancy descriptor such as a Grashof or Rayleigh number may be useful only when the characteristic length, temperature difference, fluid properties and effective acceleration are defined. Nominal microgravity must not be represented as mathematically exact zero gravity when residual accelerations are unknown.

### 7.6 Similarity is not equivalence

A match in one or several dimensionless groups does not establish physical equivalence if material chemistry, boundary conditions, geometry, radiation, ignition, or regime differ. Dimensionless descriptors support a mechanistic argument; they do not replace source-level experimental comparison.

## 8. Experiment comparability for the selected pair

The comparison is not a search for two identical experiments. Gravity level is the intentional contrast. Other differences must be exposed and assessed.

| Dimension | BASS-II microgravity | Normal-gravity downward | FiF treatment |
|---|---|---|---|
| Fuel family | PMMA | PMMA reported | Same family; grade/batch equivalence unresolved |
| Nominal thickness | 100 µm | 100 µm | Nominal match; tolerance and sample identity required |
| Width | 20 mm | 20 mm reported | Verify exact sample records |
| Atmosphere | O2/N2 | Ambient air | Similar nominal O2, not automatically identical diluent composition |
| Oxygen | BASS calibrated and uncalibrated values both preserved | 21% reported | Sensor calibration and measurement scope must be reconciled |
| Pressure | Approximately 99.2–99.5 kPa | Approximately 101 kPa | Small but explicit difference; do not erase |
| Flow | Forced fan flow, reported comparison around 3 cm/s; B3 matrix air display 2 cm/s | Buoyancy-generated opposing flow | Unresolved flow discrepancy; different physical origin |
| Gravity | Microgravity | 1 g | Intended independent contrast |
| Orientation | Opposed-flow sample configuration | Downward spread | Document propagation and buoyancy orientation |
| Holder | BASS-II rail / sample mount | Flame Stabilizer / stainless holder | Boundary condition differs |
| Ignition | Manual Kanthal hot-wire | Piloted ignition | Initial conditions differ |
| Imaging | Top-view stills at 1 Hz plus side-view video | Top-view recording | Timing and calibration need asset-level verification |
| Outcome | Spread-rate history | Spread-rate history | Compare same stable interval and measurement definition |

**Interpretation:** NASA's published comparison is a valuable starting point, but FiF must not label it a perfectly controlled one-variable experiment. Gravity is the target contrast, yet atmosphere, flow generation, holder, ignition and material-batch identity are not all demonstrated to be identical.

## 9. Transferability decision logic

FiF should make an outcome-specific, evidence-based decision. No weighted aggregate score is used in v0.1.

### Gate A — Outcome identity
Are both sources measuring the same outcome with sufficiently similar operational definitions (e.g., steady leading-edge spread rate, not ignition delay or extinction velocity)?

- If no: not directly comparable for this outcome.
- If unknown: insufficient evidence.
- If yes: continue.

### Gate B — Material and geometry
Are fuel chemistry/formulation, thickness regime, width, orientation and relevant boundary conditions identified?

- A nominal PMMA label alone is insufficient for full material equivalence.
- A 100-µm label without tolerance is a nominal, not metrological, match.
- If a critical field is unknown, retain the limitation.

### Gate C — Atmosphere and pressure
Are oxygen concentration, diluent, pressure and their measurement/calibration basis known well enough for the target question?

- Similar O2 does not erase differences in diluent gas or pressure.
- Initial/final bulk-volume readings are not local continuous flame-zone measurements.

### Gate D — Regime identity
Is there evidence that both observations lie in the thermal regime for the stated interval?

Evidence may include:
- spread rate remaining approximately independent of opposing-flow velocity over a justified interval;
- absence of kinetic blow-off and radiative extinction in the accepted interval;
- source-supported scale analysis;
- agreement with the thin-fuel scaling, with property choices and uncertainty exposed.

No single criterion alone is sufficient.

### Gate E — Measurement comparability
Are image scale, timing, leading-edge definition, fit interval and uncertainty known?

If not, physical plausibility may be discussed, but quantitative reproduction must abstain.

### Gate F — Contradictions and missing links
Are source discrepancies (e.g., 2 versus 3 cm/s), run/sample IDs and data lineage resolved or explicitly carried?

If a discrepancy can change the regime classification or transfer conclusion, the decision must be qualified or withheld.

### Possible output states

- **Transfer supported within stated domain:** all critical gates pass; conclusion is bounded to the tested conditions and outcome.
- **Conditionally informative:** some non-critical differences remain; their effect is bounded or explicitly stated.
- **Not transferable for this outcome:** a critical physical mismatch or different regime is established.
- **Insufficient evidence:** required data are missing, ambiguous or contradictory.

Unknown is not compatible. No confidence score may conceal a failed critical gate.

## 10. What the published NASA result supports — and what it does not

NASA/TM-20210011385 Section 2.3.7 reports:
- approximately 2.0 mm/s average spread rate for the 100-µm normal-gravity downward sample;
- a highest microgravity spread rate of approximately 2.2 mm/s over the same nominal thickness, while opposing flow was varied over a broad range;
- kinetic blow-off at high flow and radiative extinction at very low flow;
- similar overall flame shape and spread rates, which the authors interpret as evidence that downward spread at 21% O2 can be considered thermally controlled with minimal kinetic effect.

These are NASA-reported results and interpretation, not FiF measurements.

The report's Section 2.3 comparison prose gives 3 cm/s for the microgravity comparison, while Appendix A.1 B3 row reports an air display of 2 cm/s. The specific link between B3 and the plotted 2.2 mm/s result is not established in the current source audit. Therefore FiF must not assign 2.2 mm/s to B3.

## 11. Explicit exclusions

This framework does not currently:
- predict ignition probability or time-to-ignition;
- predict spacecraft fire growth or crew risk;
- calculate a universal PMMA flammability boundary;
- model detailed gas-phase kinetics;
- simulate coupled 2D/3D gas-solid combustion;
- infer local flame-zone oxygen from bulk initial/final readings;
- certify spacecraft materials or safety procedures;
- recommend ventilation or suppression actuator commands.

Those require separate models, datasets, validation and safety review.

## 12. Next scientific tasks

1. Recover and verify the original B3 video and associated metadata.
2. Resolve the 2 cm/s versus 3 cm/s flow discrepancy at run level.
3. Identify the exact BASS-II and ground sample identities, grades, batches and dimensional tolerances.
4. Recover the normal-gravity run-level record and original video.
5. Reconstruct both spread-rate histories with a common, documented image-analysis protocol.
6. Quantify uncertainty and sensitivity before comparing values.
7. Evaluate thermal-regime assumptions using source-specific properties and timescales.
8. Only then test the bounded transfer hypothesis.

## 13. Primary references

1. Olson, S. L. et al. (2021), *Burning and Suppression of Solids-II (BASS-II) Summary Report*, NASA/TM-20210011385, especially Sections 2.3.1–2.3.8 and Appendix A.1. https://ntrs.nasa.gov/citations/20210011385
2. Bhattacharjee, S. et al. (2016), “Opposed-flow flame spread: A comparison of microgravity and normal gravity experiments to establish the thermal regime,” *Fire Safety Journal*, 79, 111–118. DOI: https://doi.org/10.1016/j.firesaf.2015.11.011
3. Olson, S. L. (1991), “Mechanisms of Microgravity Flame Spread Over a Thin Solid Fuel: Oxygen and Opposed Flow Effects,” *Combustion Science and Technology*, 76, 233–249. DOI: https://doi.org/10.1080/00102209108951711
4. Bhattacharjee et al. (2017), “Measurement of instantaneous flame spread rate over solid fuels using image analysis,” *Fire Safety Journal*, 91, 123–129. DOI: https://doi.org/10.1016/j.firesaf.2017.03.039

**Document status:** framework for subsequent scientific review. No new experimental result or quantitative transferability score is claimed.
