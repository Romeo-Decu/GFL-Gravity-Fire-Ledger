"""Fire-safety evidence map across NASA PSI combustion investigations (DEC-071).

Deterministic part only: the record text shown to the extracting models, the check that every
extracted statement quotes that text verbatim, the agreement between extractors, and the transfer
gates between investigations. No model is called from here.
"""
from __future__ import annotations

import json
import re

FIELDS = ["Objective", "Hypothesis", "Approach", "Research Impacts", "Experiment Hardware", "SubResearch Area", "Flight Platform"]
SLOTS = {  # categorical slots and their closed vocabularies
    "fuel_phase": ["solid", "liquid", "gas", "mixed", "unknown"],
    "gravity": ["microgravity", "partial gravity", "normal gravity", "several levels", "unknown"],
    "flow": ["quiescent", "forced flow", "buoyant flow", "several", "unknown"],
    "atmosphere": ["air", "reduced oxygen", "enriched oxygen", "varied", "inert or diluted", "unknown"],
}
FUNCTIONS = ["material flammability", "ignition", "flame spread", "extinction", "detection", "suppression", "soot and smoke", "combustion fundamentals"]


def record_text(study: dict) -> str:
    """The exact text an extractor sees for one investigation; quotes are checked against it."""
    f = study["fields"]
    parts = [f"Investigation: {study['id']} | {study['title']}"]
    parts += [f"{k}: {f[k]}" for k in FIELDS if f.get(k)]
    if study.get("descriptors"):
        parts.append("Descriptors: " + "; ".join(study["descriptors"]))
    return "\n\n".join(parts)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip().lower()


def quoted(quote, text: str) -> bool:
    """True when the quote is in the record word for word (case and white space aside), at least 12 characters."""
    return isinstance(quote, str) and len(_norm(quote)) >= 12 and _norm(quote) in _norm(text)


def parse(content: str):
    """The first JSON object in a model answer, or None."""
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def validate(answer: dict, text: str) -> dict:
    """Keep only what quotes the record. A slot without a valid quote becomes unknown; a statement without one is dropped."""
    out = {"slots": {}, "functions": [], "statements": [], "dropped": 0}
    for slot, vocab in SLOTS.items():
        v = (answer.get("slots") or {}).get(slot) or {}
        val = v.get("value") if v.get("value") in vocab else "unknown"
        if val != "unknown" and not quoted(v.get("quote"), text):
            val, out["dropped"] = "unknown", out["dropped"] + 1
        out["slots"][slot] = {"value": val, "quote": v.get("quote") if val != "unknown" else None}
    for key, dest in (("functions", "functions"), ("statements", "statements")):
        for it in answer.get(key) or []:
            if not isinstance(it, dict) or not quoted(it.get("quote"), text) or (key == "functions" and it.get("function") not in FUNCTIONS):
                out["dropped"] += 1
                continue
            out[dest].append({k: it[k] for k in ("function", "statement", "quote") if k in it})
    return out


def merge(by_model: dict) -> dict:
    """Agreement between extractors. A slot value stands only when every extractor gave it; otherwise it is disputed."""
    models = sorted(by_model)
    slots = {}
    for slot in SLOTS:
        vals = {m: by_model[m]["slots"][slot]["value"] for m in models}
        known = set(vals.values())
        if len(known) == 1 and len(models) > 1:
            v = known.pop()
            slots[slot] = {"value": v, "status": "unknown" if v == "unknown" else "agreed", "quotes": {m: by_model[m]["slots"][slot]["quote"] for m in models}}
        else:
            slots[slot] = {"value": "unknown", "status": "single extractor" if len(models) < 2 else "disputed", "given": vals,
                           "quotes": {m: by_model[m]["slots"][slot]["quote"] for m in models}}
    funcs = {}
    for m in models:
        for it in by_model[m]["functions"]:
            funcs.setdefault(it["function"], {})[m] = {"statement": it.get("statement"), "quote": it["quote"]}
    functions = [{"function": f, "status": "agreed" if len(by) == len(models) > 1 else "one extractor", "by": by} for f, by in sorted(funcs.items())]
    return {"slots": slots, "functions": functions, "statements": {m: by_model[m]["statements"] for m in models},
            "dropped": {m: by_model[m]["dropped"] for m in models}}


def transfer(a: dict, b: dict) -> dict:
    """Can a finding of investigation a inform investigation b? Gates on the agreed slots. Unknown is not compatible."""
    shared = sorted({f["function"] for f in a["functions"] if f["status"] == "agreed"} & {f["function"] for f in b["functions"] if f["status"] == "agreed"})
    gates = {}
    for slot in SLOTS:
        x, y = a["slots"][slot], b["slots"][slot]
        if x["status"] != "agreed" or y["status"] != "agreed":
            gates[slot] = "unknown"
        else:
            gates[slot] = "pass" if x["value"] == y["value"] else "fail"
    if not shared:
        verdict = "no shared fire-safety function"
    elif "fail" in gates.values():
        verdict = "not directly transferable"
    elif "unknown" in gates.values():
        verdict = "not established"
    else:
        verdict = "conditionally informative"
    return {"shared_functions": shared, "gates": gates, "verdict": verdict}
