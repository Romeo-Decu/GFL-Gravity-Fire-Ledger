#!/usr/bin/env python3
"""Ask Foundry models to fill the evidence-map form for each PSI combustion investigation (DEC-071).

One call per investigation and model, no history. The model sees only NASA's own record text
(gfl_map.record_text). Answers are saved raw; nothing is interpreted here. Finished calls are skipped
on a second run. The key is read from the environment and never written.

    python tools/evidence_map_run.py --catalog data/manifests/PSI_CATALOG_v1.json --out evidence_map/raw --models grok-4.7 Kimi-K2.6
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import capability_probe as cp  # noqa: E402
import gfl_map  # noqa: E402

SYSTEM = "You extract what a document states. You add nothing the document does not state. Answer with one JSON object and nothing else."


def prompt(text: str) -> str:
    slots = "\n".join(f'  "{k}": one of {v}' for k, v in gfl_map.SLOTS.items())
    return f"""Below is NASA's own record of one combustion investigation from the Physical Sciences Informatics (PSI) repository.
Fill the form from this record only. Do not use anything you know from elsewhere.

Rules
1. Every value except "unknown" needs "quote": a passage copied from the record word for word, 12 to 300 characters, that supports it.
2. If the record does not state something, the value is "unknown" and the quote is null. Unknown is a correct answer; a guess is not.
3. "functions": the fire-safety functions this investigation gives evidence for, only from this list:
   {gfl_map.FUNCTIONS}
   For each: "statement" (one sentence, your words, what the record says the investigation contributes to that function) and "quote".
   Use "combustion fundamentals" when the record gives no fire-safety use.
4. "statements": up to 5 further facts a fire-safety engineer would need (fuel, sample geometry, measured quantities, stated results, stated limits), each with "statement" and "quote".

Form
{{"slots": {{
{slots}
  (each as {{"value": ..., "quote": ...}})
 }},
 "functions": [{{"function": ..., "statement": ..., "quote": ...}}],
 "statements": [{{"statement": ..., "quote": ...}}]}}

Record
------
{text}
------
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--budget", type=int, default=16000)
    ap.add_argument("--print-prompt", metavar="STUDY", help="write the prompt for one investigation and stop (no call)")
    a = ap.parse_args(argv)
    studies = [s for s in json.loads(a.catalog.read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    if a.print_prompt:
        sys.stdout.write(prompt(gfl_map.record_text(next(s for s in studies if s["id"] == a.print_prompt))))
        return 0
    ep, key = os.environ.get("AZURE_OPENAI_ENDPOINT"), os.environ.get("AZURE_OPENAI_API_KEY")
    if not ep or not key:
        print("missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True, exist_ok=True)
    cp.SYSTEM = SYSTEM

    def model_run(model: str) -> dict:
        done = {"ok": 0, "failed": 0, "skipped": 0}
        for s in studies:
            f = a.out / f"{s['id']}_{model}.json"
            if f.exists() and json.loads(f.read_text(encoding="utf-8")).get("ok"):
                done["skipped"] += 1
                continue
            text = gfl_map.record_text(s)
            user = prompt(text)
            for attempt in (1, 2, 3):
                res = cp.call(ep, key, model, user, a.budget)
                if res.get("ok") or "429" not in str(res.get("error")):
                    break
                time.sleep(45)
            res.update({"study": s["id"], "deployment": model, "attempt": attempt, "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "record_sha256": hashlib.sha256(text.encode()).hexdigest(), "prompt_sha256": hashlib.sha256((SYSTEM + "\n" + user).encode()).hexdigest()})
            if res.get("ok"):
                res["content_sha256"] = hashlib.sha256(res["content"].encode()).hexdigest()
            f.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            done["ok" if res.get("ok") else "failed"] += 1
            print(model, s["id"], "ok" if res.get("ok") else "FAILED", res.get("seconds", ""), str(res.get("finish_reason", res.get("error", "")))[:100], flush=True)
        return done

    with ThreadPoolExecutor(max_workers=len(a.models)) as ex:
        print(json.dumps(dict(zip(a.models, ex.map(model_run, a.models)))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
