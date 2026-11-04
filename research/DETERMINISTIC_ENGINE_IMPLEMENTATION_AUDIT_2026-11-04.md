# Deterministic Engine v0.1 — Implementation Audit
Date: 2026-11-04
Scope: Static review of the merged evaluator, CLI, PMMA-100 ruleset, request schema, fixtures and tests on feat/visualization-architecture-v0.1. No new local test execution is claimed.

## Executive finding
The current implementation is a deterministic evaluator of caller-supplied gate states. It is not yet an evidence-integrity validator, physical-comparability engine, measurement system, or implementation of every T01–T15 fixture. A software result cannot establish scientific validity.

## Confirmed gaps
1. **Evidence trust boundary:** all required gates can be marked pass with empty or unresolved evidence references and yield directly_supported. The evaluator does not resolve references or verify source/assertion lineage. Require reason/evidence/rule metadata for positive states and add a separate provenance validator before evidence can supply pass.
2. **Unauthorized not_applicable:** the evaluator treats not_applicable as pass for required gates without per-gate authorization or justification. Default required gates to non-bypassable; allow N/A only with explicit ruleset permission, reason and rule reference.
3. **Incompatibility scope:** every critical incompatibility with bridge_status=absent blocks every inference. Add affects_gates or explicit profile scope and apply inference-specific relevance as with conflicts. Unscoped issues remain conservatively global.
4. **Fail is not physical incompatibility:** a failed gate currently yields undetermined unless a separate critical incompatibility is declared. Preserve this distinction.
5. **Fixture coverage:** T01–T15 and I01–I12 are not all executed. Contract tests currently verify IDs/counts, not scenario behavior. T02/T03/T07/T08/T12/T14 and I04–I06/I09/I12 need structured claim, run-linkage, quantity, measurement or provenance semantics beyond this evaluator. Add a fixture-to-test/deferred-subsystem traceability matrix.
6. **Schema not enforced:** CLI loads JSON and calls assess(); it does not validate against TRANSFER_ASSESSMENT_REQUEST schema. Implement dependency-free boundary validation or a pinned validator with explicit dependency policy.
7. **Ruleset validation partial:** validate duplicate/unknown gate IDs, permitted conclusions and consistency between profiles and declared gates. Fail closed on malformed rulesets.
8. **Replay metadata incomplete:** output lacks canonical request/ruleset hashes and build/commit identifier. Add versioned reproducibility metadata; hashes identify inputs, not their truth.
9. **CLI malformed-input gaps:** malformed nested shapes may escape handled errors. Strengthen boundary validation and add tests without broadly swallowing programmer errors.

## Fixture disposition
- T01: partially represented by current-case tests.
- T02–T03: structured causality and exact run/result linkage required.
- T04: partially represented by generic incompatibility declaration; validation provenance absent.
- T05–T06: partially represented by unknown gates/conflicts.
- T07: typed statistic semantics required.
- T08: quantity/conversion model with source preservation required.
- T09: generic bridge field exists; validation provenance absent.
- T10: source interpretation and FiF assessment need separate objects.
- T11–T12: independent measurement and uncertainty pipeline required.
- T13: gate criticality and profile-specific non-critical unknown semantics required.
- T14: typed observable/phenomenon semantics required.
- T15: uncertainty provenance types required.
- I01–I03/I07–I08/I10–I11: partly testable now; coverage expansion required.
- I04–I06/I09/I12: provenance/measurement model required.

Partially represented does not mean passed. The fixture file is a behavioral specification, not an executed test report.

## Required order
1. Harden evaluator boundary, N/A policy, evidence metadata, incompatibility scope and CLI errors.
2. Map every T/I fixture to an executable test or explicitly deferred subsystem.
3. Version output with canonical hashes and build provenance.
4. Define canonical evidence graph entities and typed provenance edges.
5. Build visualization only over that canonical graph.

## Safeguards
Unknown is not compatible. Gate failure and source conflict are not automatically physical incompatibility. N/A cannot silently bypass a required gate. Evidence references are not proof. Source interpretation, FiF assessment and independent reconstruction remain separate. Do not link B3 to 2.2 mm/s without explicit source join evidence. Preserve the unresolved 2 cm/s versus 3 cm/s discrepancy.

## Conclusion
The merged v0.1 kernel is a useful conservative starting point, but is not yet a complete transferability engine. Close evaluator contract gaps and connect fixture specifications to executable tests before broadening the engine. Visualization must not hide these limitations.
