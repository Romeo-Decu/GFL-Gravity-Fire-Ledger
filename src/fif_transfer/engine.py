"""Deterministic, auditable evidence-transfer assessment.

Evaluates declared evidence states; it does not infer physical truth, reconstruct
measurements, or validate a combustion model.
"""
from __future__ import annotations
from typing import Any, Mapping

GATE_STATES = {"pass", "partial", "fail", "unknown", "not_applicable"}
CONFLICT_STATES = {"unresolved", "resolved"}


class AssessmentInputError(ValueError):
    """Assessment request violates the engine input contract."""


def _strings(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise AssessmentInputError(f"{field} must be a list of non-empty strings")
    return list(dict.fromkeys(value))


def assess(payload: Mapping[str, Any], ruleset: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one inference profile and return a deterministic audit result."""
    if not isinstance(payload, Mapping) or not isinstance(ruleset, Mapping):
        raise AssessmentInputError("payload and ruleset must be mappings")
    inference = payload.get("inference")
    profiles = ruleset.get("intended_inference_profiles", {})
    if inference not in profiles:
        raise AssessmentInputError(f"unknown inference profile: {inference!r}")
    domain = payload.get("domain_statement")
    if not isinstance(domain, str) or not domain.strip():
        raise AssessmentInputError("domain_statement is required and must be non-empty")
    prohibited = _strings(payload.get("prohibited_extrapolations", []), "prohibited_extrapolations")

    raw_gates = payload.get("gates", {})
    if not isinstance(raw_gates, Mapping):
        raise AssessmentInputError("gates must be a mapping")
    required = profiles[inference].get("required_gates", [])
    if not isinstance(required, list) or any(not isinstance(x, str) for x in required):
        raise AssessmentInputError("ruleset required_gates must be a list of strings")

    gate_audit, missing_gate_ids = [], []
    for gate_id in required:
        item = raw_gates.get(gate_id)
        if item is None:
            missing_gate_ids.append(gate_id)
            item = {"status": "unknown", "reasons": ["Required gate was not supplied."]}
        if not isinstance(item, Mapping):
            raise AssessmentInputError(f"gate {gate_id} must be a mapping")
        status = item.get("status", "unknown")
        if status not in GATE_STATES:
            raise AssessmentInputError(f"invalid status for gate {gate_id}: {status!r}")
        gate_audit.append({
            "gate_id": gate_id,
            "status": status,
            "reasons": _strings(item.get("reasons", []), f"{gate_id}.reasons"),
            "evidence_refs": _strings(item.get("evidence_refs", []), f"{gate_id}.evidence_refs"),
            "rule_ids": _strings(item.get("rule_ids", []), f"{gate_id}.rule_ids"),
        })

    conflicts = payload.get("conflicts", [])
    if not isinstance(conflicts, list):
        raise AssessmentInputError("conflicts must be a list")
    unresolved_conflicts, non_blocking_conflicts = [], []
    for conflict in conflicts:
        if not isinstance(conflict, Mapping) or conflict.get("status") not in CONFLICT_STATES:
            raise AssessmentInputError("each conflict needs status unresolved or resolved")
        if conflict["status"] == "unresolved":
            affected = _strings(conflict.get("affects_gates"), "conflict.affects_gates")
            record = {
                "id": str(conflict.get("id", "unspecified")),
                "description": str(conflict.get("description", "Unresolved evidence conflict.")),
                "affects_gates": affected,
            }
            # Unscoped conflicts are conservatively relevant to this inference.
            if not affected or set(affected).intersection(required):
                unresolved_conflicts.append(record)
            else:
                non_blocking_conflicts.append(record)

    incompatibilities = payload.get("incompatibilities", [])
    if not isinstance(incompatibilities, list):
        raise AssessmentInputError("incompatibilities must be a list")
    blocking, unresolved_bridges = [], []
    for issue in incompatibilities:
        if not isinstance(issue, Mapping):
            raise AssessmentInputError("each incompatibility must be a mapping")
        if issue.get("critical") is True:
            bridge = issue.get("bridge_status")
            if bridge not in {"absent", "validated", "unknown"}:
                raise AssessmentInputError(
                    "critical incompatibility bridge_status must be absent, validated, or unknown"
                )
            record = {
                "id": str(issue.get("id", "unspecified")),
                "description": str(issue.get("description", "Critical incompatibility assessment.")),
            }
            if bridge == "absent":
                blocking.append(record)
            elif bridge == "unknown":
                unresolved_bridges.append(record)

    statuses = [g["status"] for g in gate_audit]
    all_pass = all(s in {"pass", "not_applicable"} for s in statuses)
    any_unmet = any(s in {"fail", "unknown"} for s in statuses)
    any_partial = any(s == "partial" for s in statuses)

    # Missing evidence is not proof of physical incompatibility.
    if blocking:
        conclusion, reason = (
            "not_transferable_on_current_evidence",
            "Known critical incompatibility has no validated bridge."
        )
    elif unresolved_conflicts or unresolved_bridges or any_unmet:
        conclusion, reason = (
            "undetermined",
            "Critical evidence or bridge status is missing or conflicting; no physical incompatibility is inferred."
        )
    elif all_pass:
        conclusion, reason = "directly_supported", "All required gates pass within the declared domain."
    elif any_partial and inference == "documentary_summary":
        conclusion, reason = (
            "conditionally_informative",
            "The source-level comparison is informative subject to explicit limitations."
        )
    elif any_partial and inference == "qualitative_mechanism":
        conclusion, reason = (
            "qualitatively_informative",
            "Mechanism-level information is available, but critical conditions remain partial."
        )
    elif any_partial:
        conclusion, reason = "conditionally_informative", "One or more required gates remain partial."
    else:
        conclusion, reason = "undetermined", "The available evidence does not satisfy a declared decision path."

    if conclusion not in profiles[inference].get("permitted_conclusions", []):
        conclusion = "undetermined"
        reason += " Candidate conclusion is not permitted by this inference profile."

    return {
        "engine": "fif_deterministic_transfer_assessment",
        "engine_version": "0.1.0",
        "ruleset_id": ruleset.get("rule_set_id"),
        "ruleset_version": ruleset.get("version"),
        "inference": inference,
        "conclusion": conclusion,
        "primary_reason": reason,
        "domain_statement": domain.strip(),
        "prohibited_extrapolations": prohibited,
        "gate_assessments": gate_audit,
        "missing_gate_ids": missing_gate_ids,
        "unresolved_conflicts": unresolved_conflicts,
        "non_blocking_conflicts_for_this_inference": non_blocking_conflicts,
        "blocking_incompatibilities": blocking,
        "unresolved_incompatibility_bridges": unresolved_bridges,
        "audit": {
            "rule_ids": sorted({x for g in gate_audit for x in g["rule_ids"]}),
            "evidence_refs": sorted({x for g in gate_audit for x in g["evidence_refs"]}),
            "deterministic": True,
            "scientific_validation_status": "not_established_by_software_execution",
        },
    }
