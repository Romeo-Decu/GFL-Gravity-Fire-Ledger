import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*msgs):
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    p = subprocess.run([sys.executable, "-m", "gfl_mcp"], input="\n".join(json.dumps(m) for m in msgs) + "\n",
                       capture_output=True, text=True, env=env, cwd=ROOT, timeout=60)
    return [json.loads(x) for x in p.stdout.splitlines()]


def call(i, name, args):
    return {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": name, "arguments": args}}


def test_handshake_and_tools_are_read_only():
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}}}
    out = run(init, {"jsonrpc": "2.0", "method": "notifications/initialized"}, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert len(out) == 2  # notification gets no reply
    assert out[0]["result"]["serverInfo"]["name"] == "gfl"
    tools = out[1]["result"]["tools"]
    assert {t["name"] for t in tools} >= {"search_memory", "get_record", "verify_ledger", "rank_comparable_runs", "assess_transfer"}
    assert all(t["annotations"]["readOnlyHint"] for t in tools)


def test_tool_answers_cite_sources_and_reject_bad_input():
    out = run(call(1, "get_record", {"id": "RES-021"}), call(2, "get_record", {"id": "NOPE-1"}),
              call(3, "rank_comparable_runs", {"limit": 2}), call(4, "search_memory", {"bogus": 1}),
              call(5, "verify_ledger", {}), {"jsonrpc": "2.0", "id": 6, "method": "no/such"})
    r = {m["id"]: m for m in out}
    assert r[1]["result"]["structuredContent"]["record"]["id"] == "RES-021"
    assert r[2]["result"]["isError"] is True
    rank = r[3]["result"]["structuredContent"]
    assert rank["reference"]["test"] == "B6" and len(rank["runs"]) == 2 and "source" in rank
    assert r[4]["error"]["code"] == -32602
    assert r[5]["result"]["structuredContent"]["chain_ok"] is True
    assert r[6]["error"]["code"] == -32601
