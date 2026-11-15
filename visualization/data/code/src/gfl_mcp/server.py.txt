"""GFL read-only MCP server (stdio, JSON-RPC 2.0, no third-party dependency).

Lets any MCP client (Claude Desktop, AAL, other agents) query GFL without changing it:
the experiment memory, one record with its history, the ledger verification, the
comparability ranking of BASS-II runs and the transfer engine. Every answer names the
files and ledger entries it comes from, so a model citing GFL can be checked.

Nothing here writes: no ledger append, no file write, no network access.

    python -m gfl_mcp            # from the repository with PYTHONPATH=src
Client configuration (example):
    {"command": "python", "args": ["-m", "gfl_mcp"], "env": {"PYTHONPATH": "<repo>/src"}}
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = "2025-06-18"
SERVER = {"name": "gfl", "title": "Gravity Fire Ledger (read-only)", "version": "0.1.0"}
NEGATIVE = {"superseded", "withdrawn", "rejected"}


def _load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _memory() -> dict:
    return _load("visualization/data/experiment_memory.json")


def search_memory(query: str = "", kind: str = "", state: str = "", failures_only: bool = False, limit: int = 20) -> dict:
    q = query.lower().split()
    out = []
    for r in _memory()["records"]:
        text = " ".join(h["text"] for h in r["history"]).lower()
        if kind and r["kind"] != kind:
            continue
        if state and r["current_state"] != state:
            continue
        if failures_only and not r["negative_record"]:
            continue
        if q and not all(w in text or w in r["id"].lower() for w in q):
            continue
        out.append({"id": r["id"], "kind": r["kind"], "state": r["current_state"], "negative_record": r["negative_record"],
                    "superseded_in_ledger": r["superseded_in_ledger"], "summary": r["history"][-1]["text"][:300]})
    return {"query": query, "matches": len(out), "records": out[: max(1, min(limit, 100))],
            "source": "visualization/data/experiment_memory.json (built from docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md and ledger/ledger.jsonl)"}


def get_record(id: str) -> dict:  # noqa: A002 - MCP argument name
    for r in _memory()["records"]:
        if r["id"].upper() == id.upper():
            return {"record": r, "source": "visualization/data/experiment_memory.json"}
    return {"error": f"no record {id!r} in the experiment memory", "hint": "use search_memory to find record ids"}


def verify_ledger() -> dict:
    from gfl_ledger.core import Ledger, load_key_roles, load_public_keys, verify
    data = Path(os.environ.get("FIF_DATA", Path.home() / "FiF_Data"))
    res = verify(Ledger(ROOT / "ledger/ledger.jsonl"), load_public_keys(ROOT / "ledger/keys"),
                 {"repo": ROOT, "fif_data": data}, load_key_roles(ROOT / "ledger/keys"))
    return {"entries": res["entries"], "head": res["head"], "chain_ok": res["chain_ok"], "chain_errors": res["chain_errors"],
            "objects": res["objects"], "sealed_altered": res["sealed_altered"],
            "note": "missing means the raw NASA bytes are not on this machine; it is never counted as verified"}


def rank_comparable_runs(reference: str = "B6", air: float = 3.0, limit: int = 10, level: str = "") -> dict:
    rel = "data/derived/BASSII_COMPARABLE_RUNS_v1.json"
    d = _load(rel)
    ref = d["reference"]
    if reference != ref["test"] or float(air) != float(ref["air_setting"]):
        table = Path(os.environ.get("FIF_DATA", Path.home() / "FiF_Data")) / d["table"]["ledger_location"]
        if not table.exists():
            return {"error": f"only the sealed ranking for {ref['test']} at air setting {ref['air_setting']} is available here",
                    "hint": "set FIF_DATA to a folder holding the PSI-25 experimental table to rank another reference"}
        sys.path.insert(0, str(ROOT / "tools"))
        from rank_comparable_runs import load_rows, rank, sha256
        if sha256(table) != d["table"]["sha256"]:
            return {"error": "the experimental table on this machine does not match its ledger seal"}
        d = rank(load_rows(table), reference, float(air))
        rel = f"computed now from {table.name} (seal verified)"
    runs = [x for x in d["runs"] if not level or x["level"] == level]
    keep = ("rank", "test", "table_row", "pi", "sample", "material_as_recorded", "air_display_as_recorded", "level", "states")
    return {"reference": d["reference"], "counts": d["counts"], "levels": d["levels"],
            "not_recorded_in_table": d["not_recorded_in_table"],
            "runs": [{k: x[k] for k in keep} for x in runs[: max(1, min(limit, 130))]], "source": rel,
            "note": "compares what the NASA table records; it does not establish physical equivalence"}


def assess_transfer(profile: str = "quantitative_transfer") -> dict:
    sys.path.insert(0, str(ROOT / "tests"))
    from fif_transfer import assess
    from test_case_assessment import RULESET, current_case_payload
    if profile not in RULESET["intended_inference_profiles"]:
        return {"error": f"unknown profile {profile!r}", "profiles": RULESET["intended_inference_profiles"]}
    return {"case": "PMMA-100: BASS-II microgravity vs normal-gravity downward spread", "profile": profile,
            "assessment": assess(current_case_payload(profile), RULESET),
            "ruleset": f"{RULESET['rule_set_id']}@{RULESET['version']}",
            "note": "gate states are declared from the source audit, not yet computed from measured data"}


def list_ai_findings(min_status: str = "") -> dict:
    rel = "visualization/data/ai_findings.json"
    if not (ROOT / rel).exists():
        return {"error": "ai_findings.json not built yet"}
    d = _load(rel)
    items = [f for f in d["findings"] if not min_status or f["status"] == min_status]
    return {"ranking_rule": d["ranking_rule"], "findings": items, "source": rel}


TOOLS = {
    "search_memory": (search_memory, "Search GFL's experiment memory (results, decisions, issues, ideas), including failures and superseded results.",
                      {"query": {"type": "string", "description": "words that must all appear"},
                       "kind": {"type": "string", "enum": ["", "result", "decision", "issue", "idea"]},
                       "state": {"type": "string"}, "failures_only": {"type": "boolean"},
                       "limit": {"type": "integer", "minimum": 1, "maximum": 100}}),
    "get_record": (get_record, "One record (e.g. RES-021, DEC-041) with its full history, citations and sealed files.",
                   {"id": {"type": "string"}}),
    "verify_ledger": (verify_ledger, "Recompute every hash, chain link and Ed25519 signature of the GFL ledger and check sealed files.", {}),
    "rank_comparable_runs": (rank_comparable_runs, "Rank NASA BASS-II runs by how comparable their recorded conditions are to a reference run (deterministic; unknown never counts as a match).",
                             {"reference": {"type": "string"}, "air": {"type": "number"},
                              "limit": {"type": "integer", "minimum": 1, "maximum": 130},
                              "level": {"type": "string", "enum": ["", "same_conditions", "close", "distant", "not_comparable"]}}),
    "assess_transfer": (assess_transfer, "Run GFL's deterministic transfer engine on the PMMA-100 case for one inference profile.",
                        {"profile": {"type": "string"}}),
    "list_ai_findings": (list_ai_findings, "AI-produced findings (blind analyses, red team, cross-validation) ranked by whether GFL reproduced them.",
                         {"min_status": {"type": "string"}}),
}
REQUIRED = {"get_record": ["id"]}


def tools_list() -> list[dict]:
    return [{"name": n, "description": d, "annotations": {"readOnlyHint": True, "openWorldHint": False},
             "inputSchema": {"type": "object", "properties": p, "required": REQUIRED.get(n, []), "additionalProperties": False}}
            for n, (_, d, p) in TOOLS.items()]


def handle(msg: dict) -> dict | None:
    mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if mid is None:  # notification
        return None
    try:
        if method == "initialize":
            result = {"protocolVersion": params.get("protocolVersion", PROTOCOL), "capabilities": {"tools": {"listChanged": False}},
                      "serverInfo": SERVER,
                      "instructions": "Read-only access to Gravity Fire Ledger. Cite record ids and file paths from the answers; "
                                      "unknown is never compatible; source-reported values are not GFL measurements."}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": tools_list()}
        elif method == "tools/call":
            name, args = params.get("name"), params.get("arguments") or {}
            if name not in TOOLS:
                return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool {name}"}}
            fn, _, props = TOOLS[name]
            bad = set(args) - set(props)
            if bad:
                return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown arguments {sorted(bad)}"}}
            out = fn(**args)
            result = {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}], "structuredContent": out,
                      "isError": "error" in out}
        else:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    except Exception as e:  # noqa: BLE001 - reported to the client, never swallowed
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def serve(stdin=sys.stdin, stdout=sys.stdout) -> None:
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}) + "\n")
            stdout.flush()
            continue
        resp = handle(msg)
        if resp is not None:
            stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            stdout.flush()
