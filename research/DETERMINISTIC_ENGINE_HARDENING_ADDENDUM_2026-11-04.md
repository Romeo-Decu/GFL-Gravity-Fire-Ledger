# Deterministic Engine v0.1 — Hardening Addendum

**Date:** 2026-11-04  
**Baseline audit:** `research/DETERMINISTIC_ENGINE_IMPLEMENTATION_AUDIT_2026-11-04.md`  
**Implementation:** `src/fif_transfer/engine.py` (engine version 0.1.3)

This addendum records which audit findings have been addressed in the current feature branch. It does not supersede the original audit's scientific limitations.

## Finding disposition

| Finding | Current disposition | Implementation / remaining limit |
|---|---|---|
| F-01 Evidence trust boundary | **Partially addressed** | A gate marked `pass` requires reasons, evidence refs and declared rule IDs; unknown rule IDs are rejected. The engine still does not resolve evidence refs or independently verify their source content. |
| F-02 Unauthorized N/A | **Addressed in evaluator** | `not_applicable` requires explicit per-gate `allow_not_applicable: true`, a reason and declared rule IDs. No PMMA-100 gate currently authorizes it. |
| F-03 Incompatibility scope | **Addressed in evaluator** | Critical incompatibilities require reasons, evidence refs and declared rule IDs; they can specify `affects_gates`; out-of-profile issues are retained as non-blocking. Missing/empty scope remains conservatively global. Evidence references are not independently resolved. |
| F-04 Gate failure vs physical incompatibility | **Regression-tested** | A failed gate alone yields `undetermined`; a separate critical incompatibility declaration is needed for a non-transferable conclusion. |
| F-05 Fixture coverage | **Traceability documented** | `research/FIXTURE_TRACEABILITY_MATRIX_v0.1.md` maps T01–T15 and I01–I12 to tests or deferred subsystems. Most scientific acceptance scenarios remain outside the current evaluator. |
| F-06 Request schema enforcement | **Open** | CLI still does not execute the JSON Schema validator. Engine-level contract validation has improved but does not enforce every schema constraint. |
| F-07 Ruleset validation | **Partially addressed** | Required gates must be non-empty, unique and declared; gate definitions must be mappings; permitted conclusions must be known; case-rule IDs must be present/unique; request rule references must be declared. Full schema/version validation remains open. |
| F-08 Replay metadata | **Addressed for input identity** | Output includes canonical SHA-256 fingerprints for request and ruleset. No runtime build/commit identifier is injected yet. Hashes identify inputs, not evidence truth. |
| F-09 Malformed input handling | **Partially addressed** | Inference, gate, conflict status and bridge status validation now reject several malformed structures with `AssessmentInputError`. The CLI boundary still needs broader malformed-ruleset/schema tests. |

## Verified software checks

GitHub Actions run for commit `769a7c36938f311db9cd7cf72dbba58205e92669` completed successfully:
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13
- Node visualization adapter tests and JavaScript syntax checks

The earlier failed CI run at commit `b87237f1e608e1542c8d12960055bdb99cf4470a` exposed a test fixture mismatch: the test helper still used an undeclared placeholder rule ID. The fixture helper was corrected to use the actual PMMA ruleset ID, then the full matrix passed on the later commit. This history is retained rather than hidden.

## Remaining non-negotiable limits

- Evidence refs are not resolved against a source registry.
- A caller-supplied pass remains a declared status, not an engine-verified scientific finding.
- `bridge_status=validated` remains a declaration; no bridge model/evidence validation subsystem exists.
- Unit conversions, run/result joins, statistic equivalence, combustion-regime validation, raw-video reconstruction and uncertainty propagation remain unimplemented.
- No software result constitutes scientific validation or safety certification.
