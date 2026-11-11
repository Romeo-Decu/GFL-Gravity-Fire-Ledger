#!/usr/bin/env python3
"""Capability probe: the same code-carrying task sent to every model, identical prompt, no history.

Part S of AAL test 1 (docs/AAL_TEST1_PROTOCOL_v1.md, amendment A1). Each model receives the task
text and the data schema with sample rows of the synthetic set; it cannot run code and must deliver
one script. Responses are stored as received with hashes; GFL's Validator then executes each
script on the full files and scores it against the withheld truth.

Configuration only from environment variables:
    AZURE_OPENAI_ENDPOINT (Foundry v1, e.g. https://<resource>.services.ai.azure.com/openai/v1)
    AZURE_OPENAI_API_KEY

    python tools/capability_probe.py --package data/synthetic/aal_test1 --out probe_out \
        --models gpt-5.5 gpt-6-astra grok-4.7 Kimi-K2.6 Mistral-Large-3 DeepSeek-V4-Pro Decision-1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

SYSTEM = "You are an independent scientific analyst. Follow the task exactly. Answer in English."


def call(endpoint: str, key: str, model: str, user: str, budget: int) -> dict:
    """Streaming chat completion (keeps long reasoning runs from being cut by idle timeouts)."""
    url = f"{endpoint.rstrip('/')}/chat/completions"
    last = None
    for budget_key in ("max_completion_tokens", "max_tokens"):
        body = json.dumps({"model": model, "stream": True, "stream_options": {"include_usage": True},
                           "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                           budget_key: budget}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "api-key": key})
        t0 = time.time()
        try:
            parts, finish, usage, model_rep = [], None, None, None
            with urllib.request.urlopen(req, timeout=1800) as r:
                for raw in r:
                    line = raw.decode(errors="replace").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    ev = json.loads(data)
                    model_rep = ev.get("model") or model_rep
                    usage = ev.get("usage") or usage
                    for ch in ev.get("choices") or []:
                        parts.append((ch.get("delta") or {}).get("content") or "")
                        finish = ch.get("finish_reason") or finish
            return {"ok": True, "seconds": round(time.time() - t0, 1), "model_reported": model_rep, "usage": usage,
                    "finish_reason": finish, "budget": budget, "content": "".join(parts)}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode(errors='replace')[:400]}"
            if e.code not in (400, 422):
                break
        except Exception as e:  # noqa: BLE001 - recorded, never hidden
            last = f"{type(e).__name__}: {e}"
            break
    return {"ok": False, "error": last, "budget": budget}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--budget", type=int, default=64000, help="completion token budget (reasoning included)")
    ap.add_argument("--attempt", type=int, default=1, help="attempt number, kept in the file name")
    a = ap.parse_args(argv)
    ep, key = os.environ.get("AZURE_OPENAI_ENDPOINT"), os.environ.get("AZURE_OPENAI_API_KEY")
    if not ep or not key:
        print("missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY", file=sys.stderr)
        return 2
    task = (a.package / "TASK_FOR_API_ANALYSTS.md").read_text(encoding="utf-8")
    schema = (a.package / "DATA_SCHEMA_AND_SAMPLE.md").read_text(encoding="utf-8")
    user = task + "\n\n---\n\n" + schema
    a.out.mkdir(parents=True, exist_ok=True)

    def one(m):
        res = call(ep, key, m, user, a.budget)
        res.update({"deployment": m, "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "prompt_sha256": hashlib.sha256((SYSTEM + "\n" + user).encode()).hexdigest()})
        if res.get("ok"):
            res["content_sha256"] = hashlib.sha256(res["content"].encode()).hexdigest()
        res["attempt"] = a.attempt
        (a.out / (f"{m}.json" if a.attempt == 1 else f"{m}.attempt{a.attempt}.json")).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(m, "ok" if res.get("ok") else "FAILED", res.get("seconds", ""), res.get("finish_reason", res.get("error", ""))[:120], flush=True)
        return m, res.get("ok")

    with ThreadPoolExecutor(max_workers=len(a.models)) as ex:
        results = list(ex.map(one, a.models))
    print(json.dumps(dict(results)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
