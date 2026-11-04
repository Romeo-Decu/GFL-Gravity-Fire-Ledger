# Deterministic Transfer Engine — Input/Output Contract v0.1

**Status:** implementation contract for the first deterministic assessment core.  
**Scope:** software behavior only. This document does not validate the combustion science or the NASA source evidence.

## 1. Purpose

The engine evaluates an explicitly prepared evidence assessment against one versioned inference profile in the PMMA-100 ruleset. It returns a bounded conclusion and an audit record.

The engine does not:
- discover or extract evidence from source documents;
- normalize physical units or calculate combustion quantities;
- reconstruct flame-spread measurements from videos;
- decide whether a source assertion is factually correct;
- independently determine combustion regime;
- validate a physical model or certify safety.

Those functions require separate components and evidence.

## 2. Input contract

A request contains:

- `inference`: one profile declared by the ruleset (`documentary_summary`, `qualitative_mechanism`, `quantitative_transfer`, `model_calibration`, or `model_validation`);
- `gates`: gate ID to assessment object;
- `conflicts`: unresolved or resolved source-evidence disagreements;
- `incompatibilities`: explicitly assessed physical or observable incompatibilities;
- `domain_statement`: non-empty statement delimiting the requested conclusion;
- `prohibited_extrapolations`: explicit uses or conclusions outside that domain.

A gate assessment contains:
- `status`: `pass`, `partial`, `fail`, `unknown`, or `not_applicable`;
- `reasons`: human-readable rationale;
- `evidence_refs`: source/evidence references (an empty list means no reference was supplied);
- `rule_ids`: rules supporting the gate assessment.

An omitted required gate is recorded as `unknown`; it is never treated as compatible.

### Conflict scope

Each unresolved conflict may include `affects_gates`. A conflict blocks only an inference whose required gates overlap those affected gates. A conflict with no scope is conservatively treated as relevant to every inference.

This is essential because a documentary summary may remain useful while a specific quantitative transfer is undetermined. The conflict remains visible in the audit even when it does not block the selected inference.

### Incompatibility bridge status

A critical incompatibility must explicitly state its bridge status:
- `absent`: no validated bridge exists; the requested transfer is blocked;
- `unknown`: bridge status is unresolved; conclusion is undetermined;
- `validated`: a validated bridge is asserted by the caller and must be supported by evidence references.

A missing or failed evidence gate is not automatically a physical incompatibility.

## 3. Decision precedence

1. Explicit critical incompatibility with no validated bridge → `not_transferable_on_current_evidence`.
2. Relevant unresolved conflict, unknown critical bridge, or unmet required gate (`fail` / `unknown`) → `undetermined`.
3. All required gates pass or are explicitly not applicable → `directly_supported`, only if permitted by the inference profile.
4. Partial documentary evidence → `conditionally_informative`.
5. Partial mechanism evidence → `qualitatively_informative`.
6. Other partial evidence → `conditionally_informative`, subject to profile permissions.
7. If the profile does not permit the candidate conclusion, return `undetermined`.

These are deterministic software rules, not claims that the underlying evidence is scientifically sufficient.

## 4. Output contract

The result includes:
- engine and ruleset versions;
- selected inference and conclusion;
- primary reason;
- domain statement and prohibited extrapolations;
- gate-by-gate status, reasons, rule IDs and evidence references;
- missing gate IDs;
- relevant and non-blocking unresolved conflicts;
- blocking incompatibilities and unresolved bridge assessments;
- a compact audit containing rule IDs, evidence references and deterministic-execution status.

The output explicitly reports `scientific_validation_status = not_established_by_software_execution`.

## 5. Current PMMA-100 behavior expected

Using the current v0.1 gate configuration:
- `documentary_summary` → `conditionally_informative`;
- `quantitative_transfer` → `undetermined`;
- `model_calibration` → `undetermined`;
- `model_validation` → `undetermined`.

The B3 2-versus-3 cm/s conflict is scoped to `atmosphere_flow`. It remains visible, but does not by itself erase the value of a bounded documentary summary. It is relevant to quantitative transfer, which requires the atmosphere/flow gate.

## 6. Verification boundary

Unit and integration tests verify:
- deterministic output for identical versioned inputs;
- missing evidence remains unknown;
- unresolved conflicts are not recast as physical incompatibilities;
- conflict scope is inference-specific;
- explicit critical incompatibility and bridge status affect conclusions correctly;
- profile permissions are respected;
- the current PMMA-100 evidence-gate configuration yields the expected bounded conclusions.

Passing these tests establishes software behavior only. It does not establish physical comparability, transferability, measurement accuracy, or scientific validity.
