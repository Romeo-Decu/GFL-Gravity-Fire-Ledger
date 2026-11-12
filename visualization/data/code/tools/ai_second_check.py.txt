#!/usr/bin/env python3
"""Second-model check of the AI findings summaries, through the team's Azure OpenAI deployment.

The first check (tools/check_citations.py) is deterministic: citations exist and numbers appear
in the cited records. This one asks a different model, from a different provider than the
summaries' author, whether each sentence is supported by the records it cites. The model only
sees the sentence and the cited record texts; it does not see GFL's verdict or the other findings.
Its answers are recorded as they are, with the deployment name and a hash of every response;
they are evidence about the summaries, not a validation of the physics.

Configuration comes only from environment variables (never from the repository or the page):
    AZURE_OPENAI_ENDPOINT     e.g. https://<resource>.services.ai.azure.com/openai/v1 (Foundry v1)
                              or https://<resource>.openai.azure.com (deployment-path API)
    AZURE_OPENAI_API_KEY
    AZURE_OPENAI_DEPLOYMENT   the deployment name
    AZURE_OPENAI_API_VERSION  optional, default 2024-10-21

    python tools/ai_second_check.py --out data/derived/AI_FINDINGS_SECOND_CHECK_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_citations import CITE, SENT, memory_texts  # noqa: E402

SYSTEM = ("You check whether sentences are supported by source records. For each sentence answer with one label: "
          "SUPPORTED (the cited records state it), PARTLY (some of it is stated, some is not), NOT_SUPPORTED (the records do "
          "not state it or contradict it). Judge only against the records given; use no outside knowledge. "
          'Reply with JSON only: {"sentences":[{"n":1,"label":"SUPPORTED|PARTLY|NOT_SUPPORTED","reason":"<= 25 words"}]}')


def call(endpoint: str, key: str, deployment: str, version: str, user: str) -> tuple[dict, str]:
    ep = endpoint.rstrip("/")
    if ep.endswith("/openai/v1"):  # Foundry v1 API: model named in the body
        url, extra = f"{ep}/chat/completions", {"model": deployment}
    else:
        url, extra = f"{ep}/openai/deployments/{deployment}/chat/completions?api-version={version}", {}
    body = json.dumps({**extra, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                       "response_format": {"type": "json_object"}, "max_completion_tokens": 1200}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "api-key": key})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode()
    data = json.loads(raw)
    return data, data["choices"][0]["message"]["content"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", type=Path, default=ROOT / "research/fixtures/AI_FINDINGS_v1.json")
    ap.add_argument("--memory", type=Path, default=ROOT / "visualization/data/experiment_memory.json")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    env = {k: os.environ.get(k) for k in ("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT")}
    missing = [k for k, v in env.items() if not v]
    if missing:
        print(f"missing environment variables: {missing}", file=sys.stderr)
        return 2
    version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
    texts = memory_texts(json.loads(a.memory.read_text(encoding="utf-8")))
    findings = json.loads(a.findings.read_text(encoding="utf-8"))["findings"]
    results, model_seen = [], set()
    for f in findings:
        sentences = [s.strip() for s in SENT.split(f["summary"].strip()) if s.strip()]
        ids = sorted({x.strip() for s in sentences for c in CITE.findall(s) for x in c.split(",")})
        user = "RECORDS:\n" + "\n\n".join(f"[{i}] {texts[i]}" for i in ids) + "\n\nSENTENCES:\n" + \
               "\n".join(f"{n}. {s}" for n, s in enumerate(sentences, 1))
        data, content = call(env["AZURE_OPENAI_ENDPOINT"], env["AZURE_OPENAI_API_KEY"], env["AZURE_OPENAI_DEPLOYMENT"], version, user)
        model_seen.add(data.get("model", "unknown"))
        try:
            labels = json.loads(content)["sentences"]
        except (json.JSONDecodeError, KeyError):
            labels = [{"n": 0, "label": "UNPARSEABLE", "reason": content[:200]}]
        results.append({"id": f["id"], "sentences": sentences, "labels": labels,
                        "prompt_sha256": hashlib.sha256(user.encode()).hexdigest(),
                        "response_sha256": hashlib.sha256(content.encode()).hexdigest()})
        print(f["id"], [x.get("label") for x in labels])
        time.sleep(0.5)
    tally = {}
    for r in results:
        for x in r["labels"]:
            tally[x.get("label")] = tally.get(x.get("label"), 0) + 1
    out = {"checker": "second model via Azure OpenAI", "deployment": env["AZURE_OPENAI_DEPLOYMENT"],
           "models_reported": sorted(model_seen), "api_version": version,
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "system_prompt": SYSTEM,
           "tally": tally, "results": results,
           "note": "a second model's reading of sentences against cited records; evidence about the summaries, not about the physics"}
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(tally))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
