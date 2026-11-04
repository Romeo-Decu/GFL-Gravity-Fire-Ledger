# FiF — Deterministic Transfer Rules & Test Cases
**Version:** 0.1 | **Date:** 2026-11-04  
**Status:** Behavioral specification; no production engine implemented

## 1. Purpose

This document converts the PMMA-100 physical comparability matrix and Scientific System Architecture v0.1 into deterministic, testable decision behavior.

It defines:
- the order in which evidence is checked;
- how missing, contradictory and physically different values are represented;
- which conclusions are permitted for a selected outcome;
- a first acceptance-test suite based on the BASS-II / normal-gravity PMMA-100 case.

This is not a numerical combustion model. It does not calculate flame spread, infer missing experimental values, or assign a weighted comparability score.

## 2. Governing design rules

1. **Outcome-specific:** evaluate comparability for a named observable and intended inference, not for two experiments in the abstract.
2. **Provenance first:** every decision-relevant value must point to a source record, location and evidence state.
3. **No silent imputation:** unknown values remain unknown; defaults cannot create compatibility.
4. **Contradictions remain visible:** conflicting source values are represented as separate assertions until resolved.
5. **Intentional contrasts are explicit:** a difference such as gravity is not automatically a defect, but its physical consequences must be addressed for the chosen outcome.
6. **No compensating score:** a critical failure cannot be offset by several matching descriptors.
7. **Deterministic core:** unit conversion, range checks, gate evaluation and final status are deterministic; an LLM may propose extraction but cannot silently resolve evidence conflicts.
8. **Abstention is valid:** return Undetermined or Not transferable on current evidence when required evidence is missing or a critical incompatibility exists.
9. **Source claims are not FiF measurements:** preserve whether a value is measured, source-reported, derived or inferred.
10. **No extrapolation by similarity:** a result cannot be transferred outside the declared domain without an explicit physical bridge and supporting evidence.

## 3. Input contract

Each comparison request must declare:

~~~yaml
comparison_request:
  comparison_id: string
  outcome:
    id: flame_spread_rate
    definition: leading_edge_position_vs_time_slope
    unit: mm/s
  intended_inference:
    one_of:
      - documentary_summary
      - qualitative_mechanism
      - quantitative_transfer
      - model_calibration
      - model_validation
  source_experiment_id: string
  target_experiment_id: string
  domain_statement: string
  rule_set_version: string
~~~

Each parameter assertion must retain value, unit, evidence state and provenance:

~~~yaml
parameter_assertion:
  parameter_id: opposing_flow_velocity
  value: 2
  unit: cm/s
  evidence_state: source_reported
  source_id: NASA_TM_20210011385
  source_location: Appendix_A1_Table_A1_B3
  uncertainty: unknown
  notes: air_display
~~~

Required evidence states:
- measured;
- source_reported;
- derived;
- inferred;
- unknown;
- conflicting.

A derived value must retain its derivation method and parent assertions. An inferred value must never be presented as measured.

## 4. Output contract

Every assessment returns:

~~~yaml
assessment:
  comparison_id: string
  outcome_id: string
  conclusion_type:
    one_of:
      - directly_supported
      - conditionally_informative
      - qualitatively_informative
      - not_transferable_on_current_evidence
      - undetermined
  documentary_linkage:
    status: pass | partial | fail | unknown
    reasons: []
  dimension_assessments: []
  gates: []
  permitted_claims: []
  prohibited_claims: []
  unresolved_conflicts: []
  uncertainty_components: []
  domain_limits: []
  abstention:
    required: true | false
    reason: string | null
  rule_set_version: string
~~~

The conclusion type vocabulary follows the Scientific System Architecture v0.1. The PMMA matrix shorthand “conditionally informative” maps to the same architecture status.

## 5. Deterministic evaluation sequence

The engine must execute the following sequence. It must not jump directly from metadata similarity to a transfer conclusion.

### Stage 0 — Validate the request
- Confirm the outcome is defined and the operational definition is available.
- Confirm the intended inference is explicit.
- Confirm source and target experiment identifiers exist.
- Confirm rule-set version is recorded.

If the outcome or intended inference is absent, return **Undetermined** with a request-validation reason. Do not evaluate a generic similarity.

### Stage 1 — Validate provenance and evidence state
For every decision-critical assertion:
- require a source identifier and source location;
- preserve original value, unit and exact wording/context;
- preserve evidence state;
- preserve source version and retrieval status where available.

Rules:
- Missing provenance for a critical value => critical unknown.
- Two incompatible source assertions => conflict; do not average, select by convenience or overwrite.
- Source-reported values must not be relabelled as independently measured by FiF.
- A value derived from another value must retain its derivation chain.

If source/target result identity cannot be established, quantitative transfer cannot be **Directly supported**.

### Stage 2 — Check observable equivalence
Compare:
- named physical quantity;
- operational definition;
- unit;
- spatial/temporal basis;
- statistic type (mean, maximum, median, steady-state value, transient value);
- measurement and processing method.

Rules:
- Different physical quantities with no validated mapping => **Not transferable on current evidence** for quantitative transfer.
- Same quantity but materially different operational definitions with no mapping => quantitative transfer blocked.
- Mean versus maximum is not equivalent. The statistic distinction must remain explicit.
- Unknown method settings do not prove methods differ, but prevent a claim of demonstrated measurement equivalence.

### Stage 3 — Classify physical dimensions
For each relevant dimension, assign exactly one:
- compatible;
- different;
- unknown;
- not_applicable;
- conflicting.

Compatibility requires a declared comparison rule and supporting evidence. Tolerances must be supplied by a validated, outcome-specific rule set; they must not be invented ad hoc by an LLM.

A known difference must not be stored as unknown. A source contradiction must not be stored as a simple difference.

### Stage 4 — Evaluate question-specific critical gates
The rule set identifies which dimensions are critical for the selected outcome and intended inference.

For flame-spread-rate transfer in the present PMMA case, candidate critical dimensions include:
- sample identity and fuel formulation;
- actual thickness and relevant geometry;
- oxidizer composition and pressure;
- flow type, direction, velocity and reference location;
- gravity/orientation and the resulting flow regime;
- thermal/radiative boundary conditions;
- outcome definition and image-analysis calibration;
- run-level provenance.

A critical dimension that is unknown or conflicting blocks quantitative transfer unless an explicitly documented physical bridge makes it non-critical for this particular inference.

### Stage 5 — Evaluate regime and mechanism
For a thermal-regime flame-spread inference, evaluate the stated assumptions and supporting evidence, including:
- gas-flow and flame-spread velocity relationship;
- gas residence time relative to chemical time;
- radiative-loss importance;
- thermally thin fuel assumption;
- distance from kinetic blow-off and radiative extinction boundaries.

The engine must not infer that the thermal regime applies merely because a source labels it thermal. Store source interpretation separately from FiF's independent assessment.

If regime cannot be established, quantitative transfer is blocked; qualitative interpretation may remain possible.

### Stage 6 — Evaluate boundary-condition effects
Check whether differences in:
- holder/contact heat transfer;
- ignition and transient history;
- duct/confinement;
- flow conditioning and stabilization;
- sample support and edge conditions

are quantified, bounded or explicitly unresolved.

If a boundary-condition difference can plausibly affect the selected outcome and is not bounded, the engine must not claim direct quantitative transfer.

### Stage 7 — Evaluate quantitative evidence and uncertainty
For quantitative transfer or model calibration/validation:
- require run-level linkage;
- require compatible observable definitions;
- require raw/reduced data sufficient to reproduce the outcome;
- require a declared processing method;
- require uncertainty components appropriate to the evidence;
- preserve between-run and between-configuration heterogeneity;
- compare like statistics and state the comparison domain.

A source's published uncertainty is retained as source-reported until independently reconstructed.

### Stage 8 — Assign conclusion type

Use the following precedence. A lower-level positive result cannot override a higher-level blocker.

1. **Not transferable on current evidence** if there is a known, outcome-critical physical incompatibility with no justified bridge, or the compared quantities are not meaningfully mappable.
2. **Undetermined** if a critical question cannot be decided because evidence is missing or contradictory and no defensible bounded conclusion can be made.
3. **Directly supported** only if provenance, observable, critical physical conditions, regime, boundary conditions and uncertainty all pass within declared tolerances and domain.
4. **Conditionally informative** if a physically reasoned, explicit set of assumptions/conditions bounds the conclusion, but one or more conditions remain conditional.
5. **Qualitatively informative** if mechanism/trend is relevant but quantitative transfer is unjustified.
6. If none can be justified, return **Undetermined**.

The order between Not transferable and Undetermined depends on evidence semantics:
- known incompatibility => Not transferable on current evidence;
- unknown or unresolved conflict => Undetermined for the affected inference.

A comparison may therefore be qualitatively informative while quantitatively undetermined. The output must be outcome- and inference-specific.

## 6. Rules for the current PMMA-100 case

These rules are specific to flame-spread rate and the evidence currently audited.

| Rule ID | Condition | Deterministic effect |
|---|---|---|
| PMMA-100-R01 | Section 2.3 reports approx. 2.0 mm/s average and approx. 2.2 mm/s microgravity maximum | Preserve as source-reported summary values; do not call them a matched pair or equivalent statistics. |
| PMMA-100-R02 | B3 Appendix A.1 gives 2 cm/s, while Section 2.3 gives 3 cm/s | Mark opposing-flow assertion as conflicting; block B3-specific quantitative linkage pending resolution. |
| PMMA-100-R03 | No explicit source join connects B3/sample 148 to the Section 2.3 2.2-mm/s value | Documentary linkage = partial/fail; prohibit B3-specific rate claim. |
| PMMA-100-R04 | Ground 100-µm result lacks run/sample/video join in audited evidence | Ground result identity = incomplete; block matched-run validation. |
| PMMA-100-R05 | Figure 2.20 nominal O2 caption and B3 calibrated/uncalibrated readings are different evidence assertions | Retain separately; do not substitute caption value for run sensor values. |
| PMMA-100-R06 | Target image-analysis threshold is not stated | Measurement-method equivalence remains unproven; do not borrow threshold 30 or 70 from other tests. |
| PMMA-100-R07 | PMMA grade/batch and thermal properties are unknown | Block quantitative predictive-model validation requiring these properties; retain nominal material-family match. |
| PMMA-100-R08 | Holder and ignition arrangements differ | Require transient exclusion and boundary-condition assessment; no claim that gravity is the only changed variable. |
| PMMA-100-R09 | NASA interprets the case as thermally controlled | Store as source interpretation; FiF regime gate remains partial until independently assessed. |
| PMMA-100-R10 | NASA reports <5% spread-rate uncertainty/reproducibility | Store as source-reported uncertainty; never copy into FiF measurement uncertainty. |
| PMMA-100-R11 | No target videos independently reconstructed by FiF | Quantitative validation = insufficient evidence. |
| PMMA-100-R12 | Nominal PMMA, thickness, width and atmosphere are similar | Permit a literature-level, conditional comparison; do not infer full physical equivalence. |

## 7. Initial acceptance-test suite

Tests below are specification tests. Synthetic cases are deliberately hypothetical and must not be confused with NASA observations.

| Test ID | Scenario | Expected conclusion | Required engine behavior |
|---|---|---|---|
| T01 | Current audited BASS-II / ground PMMA-100 evidence; summary rates available, run joins incomplete, 2/3 cm/s conflict | **Conditionally informative** for literature-level summary; **Undetermined** for B3-specific quantitative transfer | Support only the narrow source-summary claim; preserve conflict and block validation |
| T02 | Same case, user requests claim that gravity alone caused equal spread rate | **Not transferable on current evidence** | Reject single-variable causal claim; list apparatus/flow/ignition/support differences |
| T03 | Same case, ask whether B3 specifically produced 2.2 mm/s | **Undetermined** | Require explicit run/result join; do not infer from proximity or table membership |
| T04 | Same nominal material/thickness, but fuel formulation known to differ materially and no bridging model exists | **Not transferable on current evidence** for quantitative rate transfer | Treat known critical material incompatibility as blocker |
| T05 | Critical oxygen value absent for one experiment | **Undetermined** for quantitative transfer if oxygen is critical to the regime/domain | Do not default to air or copy the other experiment's value |
| T06 | Source A reports 2 cm/s and source B reports 3 cm/s for the same asserted run/condition, no resolution | **Undetermined** for flow-dependent quantitative inference | Preserve both assertions and provenance; never average |
| T07 | Same numerical outcome but one is a maximum and the other a mean | **Not directly supported** as an equivalent quantitative pair | Preserve statistic type; require matched statistic or distribution |
| T08 | Different units but same defined quantity and valid conversion is available | Continue evaluation | Convert deterministically and preserve original value/unit and conversion |
| T09 | Gravity differs intentionally; flow regime, local flow field and all other critical outcome conditions are independently characterized and a validated physical model bridges the difference | **Conditionally informative** or **Directly supported**, depending on full gate evidence | Do not auto-fail on gravity difference; require model/domain validation |
| T10 | Thermal regime asserted by source but required timescale/property data unavailable | **Qualitatively informative** or **Undetermined** for quantitative transfer | Preserve source interpretation; mark FiF regime assessment incomplete |
| T11 | Raw videos and run joins available; identical processing protocol independently reconstructed; uncertainty intervals overlap; all critical gates pass within validated tolerances | **Directly supported** within declared domain | Permit only bounded conclusion; do not extrapolate beyond domain |
| T12 | Raw videos exist but image calibration/threshold sensitivity changes estimated rate materially and cannot be bounded | **Undetermined** for quantitative transfer | Fail measurement robustness gate; report sensitivity |
| T13 | One non-critical descriptive field is unknown and documented rule set marks it non-critical for this outcome | Continue evaluation | Unknown must remain visible; it need not automatically block every outcome |
| T14 | Evidence is semantically similar but combustion phase or observable differs with no validated mapping | **Not transferable on current evidence** | Semantic similarity cannot override physical/outcome mismatch |
| T15 | Source's stated uncertainty is available, but FiF has not reproduced measurement | Do not upgrade quantitative validation | Keep uncertainty state source_reported, not FiF_measured |

## 8. First executable decision logic (pseudocode)

~~~text
function assess(comparison):
    validate_request(comparison)
    preserve_all_source_assertions()

    if outcome_is_missing or intended_inference_is_missing:
        return UNDETERMINED("comparison request incomplete")

    provenance = evaluate_provenance()
    observable = evaluate_observable_equivalence()
    dimensions = classify_relevant_dimensions()
    conflicts = detect_conflicting_assertions()
    critical_gates = evaluate_question_specific_gates()
    regime = evaluate_regime_evidence()
    boundaries = evaluate_boundary_conditions()
    uncertainty = evaluate_uncertainty_and_reproducibility()

    if observable.has_unmappable_quantity:
        return NOT_TRANSFERABLE("outcomes are not meaningfully mappable")

    if known_critical_incompatibility_without_bridge:
        return NOT_TRANSFERABLE("known physical mismatch")

    if critical_unknown_or_unresolved_conflict:
        quantitative_status = UNDETERMINED
    else if not all_quantitative_gates_pass:
        quantitative_status = QUALITATIVELY_INFORMATIVE
    else:
        quantitative_status = DIRECTLY_SUPPORTED

    if source_summary_is_relevant and assumptions_are_explicit:
        summary_status = CONDITIONALLY_INFORMATIVE
    else:
        summary_status = UNDETERMINED

    return assessment_by_intended_inference(
        summary_status,
        quantitative_status,
        provenance,
        observable,
        dimensions,
        conflicts,
        critical_gates,
        regime,
        boundaries,
        uncertainty
    )
~~~

This pseudocode is illustrative. Production behavior requires formal schemas, explicit rule configuration, versioned tolerances and automated tests.

## 9. Test assertions and invariants

The following must always hold:

- **I01 — Unknown preservation:** unknown input remains unknown after normalization.
- **I02 — Conflict preservation:** conflicting assertions remain separately addressable.
- **I03 — No implicit default:** missing oxygen, pressure, velocity or thickness never receives a default value.
- **I04 — Provenance closure:** every derived or normalized value links to its source assertion(s).
- **I05 — Statistic integrity:** mean, maximum, median and transient values are never silently equated.
- **I06 — Unit integrity:** conversion preserves original value and unit.
- **I07 — Gate non-compensation:** a failed critical gate cannot be offset by other compatible dimensions.
- **I08 — Scope integrity:** every conclusion carries a domain statement and prohibited extrapolations.
- **I09 — Model/source separation:** source interpretation and FiF assessment are stored separately.
- **I10 — Reproducibility:** same versioned inputs and rule set yield the same deterministic result.
- **I11 — Auditability:** every status is accompanied by rule IDs, evidence references and reasons.
- **I12 — No false validation:** source-reported values or uncertainty cannot be labelled independently reproduced by FiF.

## 10. Implementation boundary

Do not implement a universal scoring algorithm yet.

Next implementation-ready artefacts, in order:
1. a controlled vocabulary for evidence states, dimension states, gate states and conclusion types;
2. a versioned rule configuration for the PMMA-100 flame-spread outcome;
3. machine-readable fixtures for T01–T15;
4. deterministic unit tests for invariants I01–I12;
5. only then a small assessment function and audit record.

The first software milestone is not “predict the flame”. It is “never make an unsupported transfer claim, and explain exactly why”.

## 11. Source basis

- FiF Scientific System Architecture v0.1, especially evidence states, dimension classes, transferability conclusion types, question-specific hard gates and uncertainty policy.
- FiF Physical Comparability and Transferability Matrix PMMA-100 v0.1.
- NASA/TM-20210011385, Section 2.3.3–2.3.7, Figures 2.18–2.20, Appendix A.1 Table A.1: https://ntrs.nasa.gov/citations/20210011385
- Carmignani (2019), Appendix A Table A.2: https://escholarship.org/uc/item/0rb693zc

This specification intentionally does not resolve source conflicts or add new physical facts. It formalizes how FiF must represent and reason about the evidence already audited.
