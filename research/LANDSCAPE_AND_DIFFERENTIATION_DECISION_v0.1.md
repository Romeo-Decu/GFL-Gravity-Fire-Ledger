# FiF — Landscape Review and Differentiation Decision v0.1

**Date:** 2026-11-03  
**Status:** Strategic decision record; based on public materials and a limited source-code inspection  
**Repository reviewed:** A-K-M-Asifuzzaman/MicroFire-Atlas  
**FiF branch:** `docs/scientific-system-architecture-v0.1`

## 1. Executive finding

A substantial public project already exists for the exact NASA Space Apps 2026 challenge, **Flame in Freefall**: [MicroFire Atlas](https://github.com/A-K-M-Asifuzzaman/MicroFire-Atlas), with a live site at https://microfire-atlas.vercel.app.

This is not a superficial dashboard. Its public README describes:
- curated BASS-II, SAFFIRE and LUCI evidence;
- 56 page-cited BASS-II tests, 20 SAFFIRE runs and 2 LUCI burns;
- a source manifest, evidence graph and verified findings;
- condition-by-condition evidence ranking and an evidence ladder;
- gap analysis and research-planning heuristics;
- an AI claim-checking pipeline;
- Flame Vision image segmentation;
- an experimental-outcome model trained on a restricted BASS-II subset, with a domain gate and abstention;
- extensive automated tests and an evaluation corpus.

The project publicly identifies itself as built for NASA Space Apps 2026, Flame in Freefall. The overlap with FiF's initial concept is therefore direct and material.

**Decision:** FiF must not become a second evidence dashboard, educational experience, NASA-report summarizer, or clone of MicroFire Atlas. Its initial architecture must be differentiated before implementation proceeds.

## 2. What was actually inspected

### Public project evidence

1. Public repository and README:
   https://github.com/A-K-M-Asifuzzaman/MicroFire-Atlas
2. Public source/data page:
   https://microfire-atlas.vercel.app/sources
3. Public example BASS-II record:
   https://microfire-atlas.vercel.app/experiments/bass2-B15
4. Public example BASS-II record:
   https://microfire-atlas.vercel.app/experiments/bass2-B4

### Limited code inspection

The following files were read from the public repository:
- `apps/web/lib/ontology.ts`
- `apps/web/lib/finding-relevance.ts`
- `apps/web/lib/research-planning.ts`
- `apps/web/lib/mission-scenarios.ts`
- `apps/web/app/model-lab/page.tsx`
- `apps/web/lib/types.ts` (relevant type definitions)

The full repository, all data, all tests, source PDFs, and every application route have **not** been independently audited. Performance and scientific validity claims in its README are treated as claims by that project, not as independently reproduced results.

## 3. Capability overlap

| Capability | MicroFire Atlas public implementation | FiF initial proposal | Implication |
|---|---|---|---|
| NASA source discovery and curation | Yes | Yes | Not differentiating |
| BASS-II / SAFFIRE evidence records | Yes | Planned | Not differentiating |
| Provenance and page-level citations | Yes | Planned | Baseline requirement |
| Experiment-condition comparison | Yes | Planned | Not differentiating by itself |
| Evidence ladder / analogical support | Yes | Planned | Significant overlap |
| Evidence gaps and candidate research questions | Yes | Planned | Significant overlap |
| AI synthesis and claim checks | Yes | Planned | Not differentiating |
| Image-based flame measurements | Yes, classical segmentation | Not in MVP | Avoid duplication |
| Experimental-outcome ML with domain gate | Yes, limited BASS-II subset | Not in MVP | Avoid as initial focus |
| Child-facing / educational exploration | Yes | No | Not FiF's target |
| Explicit, question-specific physical transferability with validated model assumptions and uncertainty propagation | Not established by inspected materials | Proposed core | Potential differentiation; must be demonstrated |

The last row is a **research opportunity**, not a claim that MicroFire lacks all relevant reasoning. Its ontology and ladder already encode meaningful physical distinctions and explicit caveats. FiF cannot claim novelty merely because it uses the words “physics-aware” or “transferability”.

## 4. Technical observations from inspected code

The inspected ontology has several good design choices:
- BASS-II, SAFFIRE and LUCI preserve separate family-specific records before being exposed through shared comparison dimensions.
- Missing condition values are represented as unknown differences rather than silently treated as matches.
- Gravity differences receive additional ranking weight.
- Liquid- and gas-phase evidence is treated as mechanistic rather than direct solid-fuel outcome evidence.
- The LUCI record carries an explicit simulated-lunar-gravity caveat.
- Research-planning candidates are explicitly hypothetical and do not manufacture completed experimental records or outcomes.
- The finding-ranking implementation distinguishes publication-level findings from explicitly row-linked findings.

The inspected comparison model also reveals a clear boundary that FiF could investigate:
- shared comparison dimensions are currently material, gravity, oxygen, pressure and airflow;
- tolerance settings are project-level thresholds (oxygen ±1.5 percentage points, pressure ±10 kPa, airflow ±50% with a 1 cm/s floor);
- the inspected direct/analogous ladder does not itself model a full causal/physical state including sample thickness, geometry, confinement, flow direction/profile, ignition, radiative boundary conditions, thermal properties, apparatus effects, or measurement-system equivalence;
- the inspected condition comparison is a transparent evidence-coverage heuristic, not a combustion similarity solution or a validated transfer model.

This is not a defect in the educational/research-atlas product's declared scope. It is a boundary between evidence navigation and a more demanding physical transferability engine.

## 5. FiF differentiation decision

### New product thesis

**FiF is a scientific transferability workbench: it evaluates whether, why, and within what quantified limits a finding from one combustion experiment can inform another experimental or mission context.**

The unit of analysis is not simply “the closest NASA test”. It is:

`Source finding → physical assumptions → governing variables → target regime → transfer model → uncertainty → bounded conclusion`

FiF should focus on a small number of technically defensible transfer cases, rather than broad coverage or a polished exploration interface.

### Candidate differentiating capabilities

1. **Outcome-specific physical state**
   - Separate physical state variables from metadata and narrative.
   - Build distinct governing-variable profiles for ignition, flame spread, extinction, heat release and smoke/combustion products.
   - Do not use one universal condition vector.

2. **Regime-aware transfer**
   - Identify whether source and target are within the same physical regime.
   - Detect when changes may alter the governing mechanism (for example, buoyancy/forced-flow balance, radiative/convective heat loss, oxygen transport, or confinement effects).
   - Require a justified bridging model for regime transitions.

3. **Dimensionless and mechanistic reasoning**
   - Where source data support it, evaluate relevant dimensionless groups and scaling relationships rather than raw-condition proximity alone.
   - Candidate groups may include Reynolds, Grashof/Richardson, Damköhler, Peclet and radiative/thermal parameters, but no group is to be used until its definition, applicability, required properties and data availability are justified for the selected phenomenon.
   - Do not compute a dimensionless group from guessed material properties or unverified flow values.

4. **Uncertainty propagation**
   - Propagate measurement and parameter uncertainty through a declared transfer model.
   - Separate uncertainty in the source measurement, model parameters, model form and extrapolation.
   - Permit abstention when the uncertainty or model validity domain is inadequate.

5. **Model validity domain**
   - Every model has an explicit training/validation domain, assumptions, excluded regimes and applicability checks.
   - A result outside the domain is an abstention, not an extrapolated prediction disguised as confidence.

6. **Falsifiable transfer case**
   - Each supported transfer claim must specify what evidence would falsify it.
   - Validation should use held-out experiments or independent published results where possible, not merely internal consistency checks.

## 6. Recommended first technical experiment

Do not begin by building a full platform.

Select one narrow BASS-II phenomenon and determine whether the available records and source documentation support a defensible physics-based transfer analysis. A candidate is opposed-flow flame spread or extinction in a controlled PMMA subset, but the exact target must be chosen after raw data and source papers are inspected.

The first FiF proof should answer:

> Can FiF derive a physically justified, uncertainty-aware relationship from a documented set of experiments, then correctly identify where that relationship ceases to be valid?

A meaningful demonstration should include:
- one source dataset with traceable raw/reduced values;
- one explicitly defined outcome;
- one physical model or scaling hypothesis;
- a parameter and uncertainty ledger;
- a validation case not used to construct the model;
- at least one regime or condition where the engine refuses transfer;
- a reproducible report explaining the result and its limits.

If the evidence cannot support such a case, FiF must narrow or change the target phenomenon. It must not manufacture a physics model to create superficial novelty.

## 7. What FiF should not build now

- A second NASA experiment catalogue or generic dashboard.
- A duplicate evidence ladder based on fixed tolerances.
- A generic RAG chatbot over NASA publications.
- A flame-image segmentation feature.
- A generic classifier of whether a flame ignites or persists.
- An opaque “transferability score”.
- A broad multi-family dataset before one transfer case is validated.
- A user interface before the scientific kernel is demonstrated.

## 8. Risk and opportunity

### Risk

The original FiF concept overlaps materially with a sophisticated existing implementation. Reproducing the same product category would consume scarce development time while producing little defensible differentiation.

### Opportunity

MicroFire Atlas has already done substantial work in evidence curation, source traceability, educational communication and evidence navigation. FiF can use its public outputs as a landscape reference and, where licences and source provenance permit, independently verify or cite the underlying NASA sources. FiF should not copy its code or curated data without reviewing licence, provenance and attribution obligations.

A complementary relationship is possible in principle, but no collaboration or data-sharing agreement is assumed.

## 9. Decision log

| ID | Decision | Status |
|---|---|---|
| D-007 | Do not build a duplicate NASA evidence dashboard or educational atlas | Adopted |
| D-008 | Reposition FiF around physical transferability, model validity and uncertainty | Adopted as product hypothesis |
| D-009 | Do not claim novelty until a validated transfer case demonstrates a capability beyond evidence ranking/coverage heuristics | Adopted |
| D-010 | Defer broad UI and multi-family ingestion until the scientific kernel passes a falsifiable proof | Adopted |
| D-011 | Treat MicroFire Atlas README performance and validation metrics as unverified claims until independently reproduced | Adopted |

---

**Conclusion:** FiF remains viable only if it demonstrates a distinct scientific capability. The project should now optimize for one defensible transferability proof, not feature breadth.
