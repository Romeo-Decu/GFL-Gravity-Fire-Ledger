#!/usr/bin/env python3
"""Send the evaluation packet and questionnaire to the evaluators, one call each, no history (docs/GFL_EVALUATION_PROTOCOL_v1.md).

Runs on the owner's machine. Configuration only from environment variables, never from the repository:
    AZURE_OPENAI_ENDPOINT   Foundry v1 endpoint, e.g. https://<resource>.services.ai.azure.com/openai/v1
    AZURE_OPENAI_API_KEY

    python tools/run_evaluation.py --packet evaluation/PACKET_v1.md --out evaluation/raw \
        --assign juror=grok-4.7 physicist=gpt-6-astra user=Kimi-K2.6
Responses are stored as received, with hashes, including failed calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import capability_probe as cp  # noqa: E402

ROLES = {"juror": "You are a hostile but fair judge of the NASA Space Apps Challenge. You look for claims that are untrue, not new, not useful, or badly shown.",
         "physicist": "You are a combustion scientist reviewing this work as you would a manuscript. You look for wrong physics, misused numbers and conclusions the data do not support.",
         "user": "You are a research engineer who is not a programmer and must use this platform tomorrow. You look for every place where you would get stuck or be misled."}


def questionnaire() -> str:
    doc = (ROOT / "docs/GFL_EVALUATION_PROTOCOL_v1.md").read_text(encoding="utf-8")
    a, b = doc.index("## Rules given to the evaluators"), doc.index("## How the answers are checked")
    return doc[a:b].strip()


def prompt(role: str, packet: str) -> str:
    return (f"{ROLES[role]}\n\nYou evaluate the project described in the packet below. You did not take part in it. "
            f"Answer the questionnaire that follows the packet. Your role is \"{role}\": in part I answer only the {role} questions.\n\n"
            f"<packet>\n{packet}\n</packet>\n\n{questionnaire()}\n\nReply with the JSON object only.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--assign", nargs="+", required=True, help="role=deployment, for juror, physicist and user")
    ap.add_argument("--budget", type=int, default=64000)
    ap.add_argument("--print-prompt", choices=list(ROLES), help="write the prompt of one role to stdout and stop (no call)")
    a = ap.parse_args(argv)
    packet = a.packet.read_text(encoding="utf-8")
    if a.print_prompt:
        sys.stdout.write(prompt(a.print_prompt, packet))
        return 0
    assign = dict(x.split("=", 1) for x in a.assign)
    assert set(assign) <= set(ROLES), f"roles are {list(ROLES)}"
    ep, key = os.environ.get("AZURE_OPENAI_ENDPOINT"), os.environ.get("AZURE_OPENAI_API_KEY")
    if not ep or not key:
        print("missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True, exist_ok=True)
    cp.SYSTEM = "You are an independent evaluator. Follow the instructions exactly. Answer in English."

    def one(item):
        role, model = item
        user = prompt(role, packet)
        res = cp.call(ep, key, model, user, a.budget)
        res.update({"role": role, "deployment": model, "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "packet_sha256": hashlib.sha256(packet.encode()).hexdigest(), "prompt_sha256": hashlib.sha256((cp.SYSTEM + "\n" + user).encode()).hexdigest()})
        if res.get("ok"):
            res["content_sha256"] = hashlib.sha256(res["content"].encode()).hexdigest()
        (a.out / f"{role}_{model}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(role, model, "ok" if res.get("ok") else "FAILED", res.get("seconds", ""), str(res.get("finish_reason", res.get("error", "")))[:120], flush=True)
        return role, bool(res.get("ok"))

    with ThreadPoolExecutor(max_workers=len(assign)) as ex:
        print(json.dumps(dict(ex.map(one, assign.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
