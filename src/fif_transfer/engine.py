"""Deterministic, auditable evidence-transfer assessment.

Evaluates declared evidence states; it does not infer physical truth, resolve
source provenance, reconstruct measurements, or validate a combustion model.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

GATE_STATES = {"pass", "partial", "fail", "unknown", "not_applicable"}
CONFLICT_STATES = {"unresolved", "resolved"}
BRIDGE_STATES = {"absent", "validated", "unknown"}
CONCLUSION_STATES = {
    "directly_supported", "conditionally_informative", "qualitatively_informative",
    "not_transferable_on_current_evidence", "undetermined"
}


class AssessmentInputError(ValueError):
    """Assessment request or ruleset violates the engine input contract."""


def _strings(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise AssessmentInputError(f"{field} must be a list of non-empty strings")
    return list(dict.fromkeys(x.strip() for x in value))


def _canonical_sha256(value: Mapping[str, Any], field: str) -> str:
    try:
        encoded = json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise AssessmentInputError(f"{field} must contain only finite JSON-compatible values") from exc
    return hashlib.sha256(encoded).hexdigest()


def _validate_ruleset(ruleset: Mapping[str, Any], inference: Any) -> tuple[Mapping[str, Any], list[str]]:
    profiles = ruleset.get("intended_inference_profiles")
    gates = ruleset.get("gates")
    if not isinstance(profiles, Mapping) or not isinstance(gates, Mapping):
        raise AssessmentInputError("ruleset must define intended_inference_profiles and gates mappings")
    if not isinstance(inference, str) or inference not in profiles:
        raise AssessmentInputError(f"unknown inference profile: {inference!r}")
    profile = profiles[inference]
    if not isinstance(profile, Mapping):
        raise AssessmentInputError(f"ruleset profile {inference!r} must be a mapping")
    required = profile.get("required_gates")
    if not isinstance(required, list) or any(not isinstance(x, str) or not x for x in required):
        raise AssessmentInputError("ruleset required_gates must be a list of non-empty strings")
    if not required:
        raise AssessmentInputError("ruleset required_gates must contain at least one gate")
    if len(required) != len(set(required)):
        raise AssessmentInputError("ruleset required_gates must not contain duplicates")
    unknown = sorted(set(required) - set(gates))
    if unknown:
        raise AssessmentInputError(f"ruleset profile references undeclared gates: {unknown}")
    for gate_id in required:
        if not isinstance(gates[gate_id], Mapping):
            raise AssessmentInputError(f"ruleset gate {gate_id} must be a mapping")

    permitted = profile.get("permitted_conclusions")
    if not isinstance(permitted, list) or any(
        not isinstance(x, str) or x not in CONCLUSION_STATES for x in permitted
    ):
        raise AssessmentInputError("ruleset permitted_conclusions contains an invalid conclusion")

    case_rules = ruleset.get("case_rules", [])
    if not isinstance(case_rules, list):
        raise AssessmentInputError("ruleset case_rules must be a list")
    rule_ids = [rule.get("id") for rule in case_rules if isinstance(rule, Mapping)]
    if len(rule_ids) != len(case_rules) or any(not isinstance(x, str) or not x for x in rule_ids):
        raise AssessmentInputError("each ruleset case_rule must define a non-empty id")
    if len(rule_ids) != len(set(rule_ids)):
        raise AssessmentInputError("ruleset case_rule IDs must be unique")
    return profile, required


def assess(payload: Mapping[str, Any], ruleset: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one inference profile and return a deterministic audit result."""
    if not isinstance(payload, Mapping) or not isinstance(ruleset, Mapping):
        raise AssessmentInputError("payload and ruleset must be mappings")

    inference = payload.get("inference")
    profile, required = _validate_ruleset(ruleset, inference)
    ruleset_gates = ruleset["gates"]
    known_rule_ids = {rule["id"] for rule in ruleset.get("case_rules", [])}

    domain = payload.get("domain_statement")
    if not isinstance(domain, str) or not domain.strip():
        raise AssessmentInputError("domain_statement is required and must be non-empty")
    prohibited = _strings(payload.get("prohibited_extrapolations", []), "prohibited_extrapolations")

    raw_gates = payload.get("gates", {})
    if not isinstance(raw_gates, Mapping):
        raise AssessmentInputError("gates must be a mapping")
    unknown_input_gates = sorted(set(raw_gates) - set(ruleset_gates))
    if unknown_input_gates:
        raise AssessmentInputError(f"request contains undeclared gates: {unknown_input_gates}")

    gate_audit, missing_gate_ids = [], []
    for gate_id in required:
        item = raw_gates.get(gate_id)
        if item is None:
            missing_gate_ids.append(gate_id)
            item = {"status": "unknown", "reasons": ["Required gate was not supplied."]}
        if not isinstance(item, Mapping):
            raise AssessmentInputError(f"gate {gate_id} must be a mapping")
        status = item.get("status", "unknown")
        if not isinstance(status, str) or status not in GATE_STATES:
            raise AssessmentInputError(f"invalid status for gate {gate_id}: {status!r}")

        reasons = _strings(item.get("reasons", []), f"{gate_id}.reasons")
        evidence_refs = _strings(item.get("evidence_refs", []), f"{gate_id}.evidence_refs")
        rule_ids = _strings(item.get("rule_ids", []), f"{gate_id}.rule_ids")
        unknown_rule_ids = sorted(set(rule_ids) - known_rule_ids)
        if unknown_rule_ids:
            raise AssessmentInputError(f"gate {gate_id} references undeclared rule IDs: {unknown_rule_ids}")

        if status == "pass" and not (reasons and evidence_refs and rule_ids):
            raise AssessmentInputError(
                f"gate {gate_id} marked pass requires non-empty reasons, evidence_refs and rule_ids"
            )
        if status == "not_applicable":
            gate_rule = ruleset_gates[gate_id]
            if gate_rule.get("allow_not_applicable") is not True:
                raise AssessmentInputError(f"gate {gate_id} does not permit not_applicable")
            if not (reasons and rule_ids):
                raise AssessmentInputError(
                    f"gate {gate_id} not_applicable requires a reason and rule_ids"
                )

        gate_audit.append({
            "gate_id": gate_id,
            "status": status,
            "reasons": reasons,
            "evidence_refs": evidence_refs,
            "rule_ids": rule_ids,
        })

    conflicts = payload.get("conflicts", [])
    if not isinstance(conflicts, list):
        raise AssessmentInputError("conflicts must be a list")
    unresolved_conflicts, non_blocking_conflicts = [], []
    for conflict in conflicts:
        if (not isinstance(conflict, Mapping)
                or not isinstance(conflict.get("status"), str)
                or conflict.get("status") not in CONFLICT_STATES):
            raise AssessmentInputError("each conflict needs status unresolved or resolved")
        if conflict["status"] == "unresolved":
            affected = _strings(conflict.get("affects_gates"), "conflict.affects_gates")
            unknown = sorted(set(affected) - set(ruleset_gates))
            if unknown:
                raise AssessmentInputError(f"conflict references undeclared gates: {unknown}")
            record = {
                "id": str(conflict.get("id", "unspecified")),
                "description": str(conflict.get("description", "Unresolved evidence conflict.")),
                "affects_gates": affected,
            }
            if not affected or set(affected).intersection(required):
                unresolved_conflicts.append(record)
            else:
                non_blocking_conflicts.append(record)

    incompatibilities = payload.get("incompatibilities", [])
    if not isinstance(incompatibilities, list):
        raise AssessmentInputError("incompatibilities must be a list")
    blocking, unresolved_bridges, non_blocking_incompatibilities = [], [], []
    for issue in incompatibilities:
        if not isinstance(issue, Mapping):
            raise AssessmentInputError("each incompatibility must be a mapping")
        if not isinstance(issue.get("critical"), bool):
            raise AssessmentInputError("each incompatibility needs a boolean critical field")
        affected = _strings(issue.get("affects_gates"), "incompatibility.affects_gates")
        unknown = sorted(set(affected) - set(ruleset_gates))
        if unknown:
            raise AssessmentInputError(f"incompatibility references undeclared gates: {unknown}")
        if issue["critical"]:
            bridge = issue.get("bridge_status")
            if not isinstance(bridge, str) or bridge not in BRIDGE_STATES:
                raise AssessmentInputError(
                    "critical incompatibility bridge_status must be absent, validated, or unknown"
                )
            reasons = _strings(issue.get("reasons", []), "incompatibility.reasons")
            evidence_refs = _strings(issue.get("evidence_refs", []), "incompatibility.evidence_refs")
            rule_ids = _strings(issue.get("rule_ids", []), "incompatibility.rule_ids")
            unknown_rule_ids = sorted(set(rule_ids) - known_rule_ids)
            if unknown_rule_ids:
                raise AssessmentInputError(
                    f"incompatibility references undeclared rule IDs: {unknown_rule_ids}"
                )
            if not (reasons and evidence_refs and rule_ids):
                raise AssessmentInputError(
                    "critical incompatibility requires reasons, evidence_refs and rule_ids"
                )
            record = {
                "id": str(issue.get("id", "unspecified")),
                "description": str(issue.get("description", "Critical incompatibility assessment.")),
                "affects_gates": affected,
                "bridge_status": bridge,
                "reasons": reasons,
                "evidence_refs": evidence_refs,
                "rule_ids": rule_ids,
            }
            relevant = not affected or bool(set(affected).intersection(required))
            if not relevant:
                non_blocking_incompatibilities.append(record)
            elif bridge == "absent":
                blocking.append(record)
            elif bridge == "unknown":
                unresolved_bridges.append(record)

    statuses = [g["status"] for g in gate_audit]
    all_pass = all(s == "pass" or s == "not_applicable" for s in statuses)
    any_unmet = any(s in {"fail", "unknown"} for s in statuses)
    any_partial = any(s == "partial" for s in statuses)

    if blocking:
        conclusion, reason = (
            "not_transferable_on_current_evidence",
            "Known critical incompatibility relevant to this inference has no validated bridge."
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

    if conclusion not in profile["permitted_conclusions"]:
        conclusion = "undetermined"
        reason += " Candidate conclusion is not permitted by this inference profile."

    return {
        "engine": "fif_deterministic_transfer_assessment",
        "engine_version": "0.1.3",
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
        "non_blocking_incompatibilities_for_this_inference": non_blocking_incompatibilities,
        "audit": {
            "rule_ids": sorted({x for g in gate_audit for x in g["rule_ids"]}),
            "evidence_refs": sorted({x for g in gate_audit for x in g["evidence_refs"]}),
            "request_sha256": _canonical_sha256(payload, "payload"),
            "ruleset_sha256": _canonical_sha256(ruleset, "ruleset"),
            "hash_semantics": "Canonical input identity only; hashes do not validate evidence truth.",
            "deterministic": True,
            "scientific_validation_status": "not_established_by_software_execution",
        },
    }
