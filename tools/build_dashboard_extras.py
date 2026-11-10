#!/usr/bin/env python3
"""Dashboard data beyond B6: capability map, transfer-engine results, vault summary, specs.

- capabilities.json: research/fixtures/GFL_CAPABILITIES_v1.json, checked (icons and
  spec files exist, cited records exist in the experiment memory).
- transfer_pmma100.json: the deterministic engine (src/fif_transfer) run on the current
  PMMA-100 case for every inference profile, with gate definitions from the ruleset.
- vault.json: ledger entries by tier, keys and roles, anchors, owner approvals.
- specs/*.md: copies of docs/specs.

    python tools/build_dashboard_extras.py --out visualization/data
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
from fif_transfer import assess  # noqa: E402
from test_case_assessment import RULESET, current_case_payload  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    out = a.out
    mem = json.loads((out / "experiment_memory.json").read_text(encoding="utf-8"))
    ids = {r["id"] for r in mem["records"]}

    caps = json.loads((ROOT / "research/fixtures/GFL_CAPABILITIES_v1.json").read_text(encoding="utf-8"))
    icons = ROOT / "visualization/assets/brand/icons"
    for g in caps["groups"]:
        for it in g["items"]:
            assert (icons / f"{it['icon']}.svg").exists(), it["icon"]
            if it.get("spec"):
                assert (ROOT / "docs/specs" / it["spec"]).exists(), it["spec"]
            for r in it.get("records", []):
                assert r in ids, f"{it['id']} cites unknown record {r}"
    (out / "capabilities.json").write_text(json.dumps(caps, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    profiles = {}
    for name in RULESET["intended_inference_profiles"]:
        profiles[name] = assess(current_case_payload(name), RULESET)
    transfer = {"case": "PMMA-100: BASS-II microgravity vs normal-gravity downward spread, published summaries",
                "gate_state_origin": "declared per gate from the source-reconciliation audit (current_case_status); not yet computed from measured data",
                "decision_policy": RULESET["decision_policy"], "gates": RULESET["gates"],
                "profiles": profiles, "ruleset": f"{RULESET['rule_set_id']}@{RULESET['version']}"}
    (out / "transfer_pmma100.json").write_text(json.dumps(transfer, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    entries = [json.loads(x) for x in (ROOT / "ledger/ledger.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    tiers = {}
    for e in entries:
        tiers.setdefault(str(e.get("tier")), 0)
        tiers[str(e.get("tier"))] += 1
    sealed = [{"seq": e["seq"], "tier": e["tier"], "kind": (e.get("instrument") or {}).get("kind"), "location": e["object"]["location"], "root": e["object"].get("root"),
               "sha256": e["object"].get("sha256"), "bytes": e["object"].get("bytes")}
              for e in entries if e.get("tier") in (1, 2) and e.get("object")]
    keys = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "ledger/keys").glob("*.pub.json"))]
    anchors = [{"seq": e["seq"], "kind": (e.get("anchor") or {}).get("kind") or (e.get("anchor") or {}).get("type"),
                "recorded_utc": e.get("recorded_utc"), "anchor": e.get("anchor")} for e in entries if e.get("type") == "anchor"]
    approvals = [{"seq": e["seq"], "decision": (e.get("approves") or {}).get("decision_id"), "key_id": e["key_id"]}
                 for e in entries if e.get("type") == "approval"]
    tier1_kinds = {}
    for e in entries:
        if e.get("tier") == 1:
            k = (e.get("instrument") or {}).get("kind", "unknown")
            src = "NASA" if (e.get("object") or {}).get("root") == "fif_data" else "project"
            tier1_kinds[f"{k} ({src})"] = tier1_kinds.get(f"{k} ({src})", 0) + 1
    vault = {"entries_by_tier": tiers, "tier1_by_kind": tier1_kinds, "sealed_objects": sealed,
             "keys": [{k: v for k, v in key.items() if k != "public_key_b64"} for key in keys],
             "anchors": anchors, "owner_approvals": approvals,
             "tsa_tokens": sorted(p.name for p in (ROOT / "ledger/anchors").glob("*.tsr"))}
    (out / "vault.json").write_text(json.dumps(vault, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    fam = json.loads((ROOT / "research/fixtures/NASA_FAMILIES_v1.json").read_text(encoding="utf-8"))
    assert all(1 <= f["stage"] <= len(fam["stages"]) for f in fam["families"])
    (out / "families.json").write_text(json.dumps(fam, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    comp = ROOT / "data/derived/BASSII_COMPARABLE_RUNS_v1.json"
    shutil.copyfile(comp, out / "comparable_runs.json")
    sys.path.insert(0, str(ROOT / "tools"))
    from check_citations import build as build_findings
    findings = build_findings(json.loads((ROOT / "research/fixtures/AI_FINDINGS_v1.json").read_text(encoding="utf-8")), mem)
    assert findings["all_passed"], "an AI finding summary failed the citation check"
    sc_path = ROOT / "data/derived/AI_FINDINGS_SECOND_CHECK_v1.json"
    if sc_path.exists():
        from check_citations import SENT
        sc = json.loads(sc_path.read_text(encoding="utf-8"))
        by = {r["id"]: r for r in sc["results"]}
        for f in findings["findings"]:
            r = by.get(f["id"])
            if not r:
                continue
            now = [x.strip() for x in SENT.split(f["summary"].strip()) if x.strip()]
            f["second_check"] = {"labels": r["labels"], "checked_sentences": r["sentences"],
                                 "state": "current wording" if now == r["sentences"] else "wording corrected after this check"}
        findings["second_check"] = {"model": ", ".join(sc["models_reported"]), "deployment": sc["deployment"], "run_utc": sc["run_utc"],
                                    "tally": sc["tally"], "file": "data/derived/AI_FINDINGS_SECOND_CHECK_v1.json", "note": sc["note"]}
    (out / "ai_findings.json").write_text(json.dumps(findings, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    (out / "specs").mkdir(exist_ok=True)
    for p in sorted((ROOT / "docs/specs").glob("*.md")):
        shutil.copyfile(p, out / "specs" / p.name)
    print(json.dumps({"capabilities": sum(len(g["items"]) for g in caps["groups"]),
                      "transfer": {k: v["conclusion"] for k, v in profiles.items()},
                      "tiers": tiers, "sealed": len(sealed), "anchors": len(anchors), "approvals": len(approvals)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
