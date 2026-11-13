#!/usr/bin/env python3
"""Check the GFL MCP server with a client GFL did not write: the official MCP Python SDK (`pip install mcp`).

Starts `python -m gfl_mcp` over stdio, performs the protocol handshake, lists the tools and calls each read-only tool
once with a plain question. Writes what the client saw. This is a protocol check with an independent client
implementation; it is not a language model using the tools.

    python tools/mcp_client_check.py --out data/derived/MCP_CLIENT_CHECK_v1.json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALLS = {"get_record": {"id": "RES-021"}}  # every other tool is called with no arguments


def _g(obj, *names):
    """The SDK renamed fields between versions (serverInfo / server_info); take whichever exists."""
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return None


async def run() -> dict:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=["-m", "gfl_mcp"], env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), cwd=str(ROOT))
    from importlib.metadata import version
    out = {"client": f"mcp Python SDK {version('mcp')}", "calls": []}
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            info = _g(init, "serverInfo", "server_info")
            out["server"] = {"name": info.name, "version": info.version, "protocol": _g(init, "protocolVersion", "protocol_version")}
            tools = (await s.list_tools()).tools
            out["tools"] = [{"name": t.name, "read_only": bool(t.annotations and _g(t.annotations, "readOnlyHint", "read_only_hint")), "required": (_g(t, "inputSchema", "input_schema") or {}).get("required", [])} for t in tools]
            for t in tools:
                args = CALLS.get(t.name, {})
                res = await s.call_tool(t.name, args)
                text = "".join(c.text for c in res.content if getattr(c, "text", None))
                out["calls"].append({"tool": t.name, "arguments": args, "is_error": bool(_g(res, "isError", "is_error")), "characters": len(text), "starts": text[:160]})
    out["all_tools_answered"] = all(not c["is_error"] and c["characters"] > 0 for c in out["calls"])
    out["all_tools_read_only"] = all(t["read_only"] for t in out["tools"])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    res = asyncio.run(run())
    if a.out:
        a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: res[k] for k in ("client", "server", "all_tools_answered", "all_tools_read_only")}), [(c["tool"], c["is_error"], c["characters"]) for c in res["calls"]])
    return 0 if res["all_tools_answered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
