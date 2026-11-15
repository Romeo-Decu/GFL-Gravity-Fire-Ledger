"""A7. Export the GFL ledger as W3C PROV-O (JSON-LD), so provenance can be read with standard tools.

Mapping: an object (file) -> prov:Entity identified by its SHA-256 (urn:sha256:...); a ledger entry that records it ->
prov:Activity; the signing key -> prov:Agent (prov:SoftwareAgent for the pipeline key, prov:Person for the owner key);
derivation parents -> prov:wasDerivedFrom; supersession -> prov:wasRevisionOf; qualification -> a prov:Influence
with its qualifiers; anchors -> prov:Activity used on the ledger head. The signed ledger stays the source of truth;
this export is a view of it.
"""
from __future__ import annotations

import json
from pathlib import Path

CONTEXT = {"prov": "http://www.w3.org/ns/prov#", "xsd": "http://www.w3.org/2001/XMLSchema#",
           "gfl": "https://github.com/Romeo-Decu/GFL-Gravity-Fire-Ledger/ns#"}


def _ent(obj):
    return f"urn:sha256:{obj['sha256']}"


def export(ledger_path: Path, owner_key_ids: set[str] | None = None) -> dict:
    owner_key_ids = owner_key_ids or set()
    entries = [json.loads(l) for l in Path(ledger_path).read_text().splitlines() if l.strip()]
    by_hash = {e["entry_hash"]: e for e in entries}
    graph, agents = [], {}
    for e in entries:
        kid = e.get("key_id")
        if kid and kid not in agents:
            agents[kid] = {"@id": f"gfl:key/{kid}", "@type": ["prov:Agent", "prov:Person" if kid in owner_key_ids else "prov:SoftwareAgent"],
                           "gfl:keyId": kid}
        act = {"@id": f"gfl:entry/{e['entry_hash']}", "@type": "prov:Activity", "gfl:entryType": e["type"], "gfl:seq": e["seq"],
               "prov:endedAtTime": {"@value": e["recorded_utc"], "@type": "xsd:dateTime"}}
        if kid:
            act["prov:wasAssociatedWith"] = {"@id": f"gfl:key/{kid}"}
        obj = e.get("object")
        if obj:
            ent = {"@id": _ent(obj), "@type": "prov:Entity", "gfl:location": obj.get("location"), "gfl:bytes": obj.get("bytes"),
                   "prov:wasGeneratedBy": {"@id": act["@id"]}}
            if kid:
                ent["prov:wasAttributedTo"] = {"@id": f"gfl:key/{kid}"}
            parents = [by_hash[p]["object"] for p in e.get("parents", []) if p in by_hash and by_hash[p].get("object")]
            if parents:
                ent["prov:wasDerivedFrom"] = [{"@id": _ent(p)} for p in parents]
                act["prov:used"] = [{"@id": _ent(p)} for p in parents]
            if e["type"] == "supersession" and e.get("supersedes") in by_hash and by_hash[e["supersedes"]].get("object"):
                ent["prov:wasRevisionOf"] = {"@id": _ent(by_hash[e["supersedes"]]["object"])}
            m = e.get("method") or {}
            if m.get("tool"):
                act["gfl:tool"] = m["tool"]
                act["gfl:codeCommit"] = m.get("code_commit")
            graph.append(ent)
        if e["type"] == "qualification" and e.get("qualifies") in by_hash and by_hash[e["qualifies"]].get("object"):
            act["prov:qualifiedInfluence"] = {"@type": "prov:Influence", "prov:influencer": {"@id": _ent(by_hash[e["qualifies"]]["object"])},
                                              "gfl:qualifiers": e.get("qualifiers", []), "gfl:reason": e.get("reason")}
        if e["type"] == "anchor":
            act["gfl:anchor"] = e.get("anchor")
            act["gfl:coversHead"] = e.get("covers_head")
        graph.append(act)
    return {"@context": CONTEXT, "@graph": list(agents.values()) + graph}
