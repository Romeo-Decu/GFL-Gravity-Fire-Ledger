#!/usr/bin/env python3
"""Run-level condition inventory of NASA's PSI combustion investigations (evidence-map protocol, amendment A5).

Each investigation may publish an "Experimental table": one row per run, with the conditions NASA recorded.
This tool downloads those tables (raw bytes stay outside the repository; only fingerprints, headers and counts
are kept) and reports, by fixed keyword rules on the column headers, which conditions are recorded per run.
No model is involved. A header is evidence that a column exists, not that its cells are filled or consistent.

    python tools/psi_run_tables.py fetch --dest "$FIF_DATA/psi_tables" --manifest data/manifests/PSI_EXPERIMENTAL_TABLES_v1.json
    python tools/psi_run_tables.py inventory --src "$FIF_DATA/psi_tables" --manifest data/manifests/PSI_EXPERIMENTAL_TABLES_v1.json --out data/derived/evidence_map/RUN_TABLE_INVENTORY_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psi25_fetch as P  # noqa: E402

# Fixed before the tables were read (only the three Saffire tables had been seen). Lower-case substrings of a header.
RULES = {
    "fuel or material": ["fuel", "material", "sample type", "fabric", "liquid", "droplet composition", "gas mixture"],
    "oxygen": ["o2", "oxygen", "oxidizer", "oxidiser"],
    "pressure": ["press", "psia", "kpa", "atm", "torr"],
    "flow": ["flow", "velocity", "air speed", "airspeed", "cm/s", "fan"],
    "gravity": ["gravity", "g-level", "g level", "accel"],
    "geometry": ["thick", "width", "length", "diameter", "radius", "size"],
    "diluent or suppressant": ["diluent", "n2", "nitrogen", "co2", "helium", "argon", "suppress", "inert"],
    "ignition": ["ignit", "igniter", "ignitor"],
    "outcome": ["spread", "burn", "extinct", "rate", "limit", "flame", "result", "comment", "note"],
}
SLOT_OF = {"fuel or material": "fuel_phase", "oxygen": "atmosphere", "flow": "flow", "gravity": "gravity"}  # which map slot a run-level column could settle


def classify(header: str) -> list[str]:
    h = header.lower()
    return [k for k, words in RULES.items() if any(w in h for w in words)]


def read_table(path: Path) -> dict:
    rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="replace", newline="")))
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return {"columns": [], "rows": 0}
    head = [c.strip() for c in rows[0]]
    body = rows[1:]
    cols = [{"header": h, "classes": classify(h), "filled": sum(1 for r in body if i < len(r) and r[i].strip())} for i, h in enumerate(head) if h]
    return {"columns": cols, "rows": len(body)}


def fetch(dest: Path, manifest: Path, catalog: Path) -> int:
    studies = [s for s in json.loads(catalog.read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    out = {"source": "NASA PSI public download API", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tables": [], "without_table": []}
    for s in sorted(studies, key=lambda s: int(s["id"].split("-")[1])):
        raw = P._http(f"{P.API}/files/v2", data=json.dumps({"folder": "", "fileType": "study", "studyId": s["id"], "version": s["version"]}).encode(), headers={"Content-Type": "application/json"})
        files = [f for f in P.flatten_tree(json.loads(raw)) if "experimental table" in (f["folder"] + f["name"]).lower() and f["name"].lower().endswith(".csv")]
        if not files:
            out["without_table"].append(s["id"])
        for f in files:
            P.STUDY = s["id"]
            r = P.download(f["name"], f["version"], dest)
            out["tables"].append({"study": s["id"], "name": f["name"], "psi_version": f["version"], "bytes": r["bytes"], "sha256": r["sha256"]})
            print(s["id"], f["name"], r["bytes"], flush=True)
    manifest.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    return 0


def inventory(src: Path, manifest: Path, out: Path) -> int:
    man = json.loads(manifest.read_text(encoding="utf-8"))
    inv = {}
    for t in man["tables"]:
        p = src / t["name"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != t["sha256"]:
            raise SystemExit(f"{t['name']}: not the file in the manifest")
        tab = read_table(p)
        e = inv.setdefault(t["study"], {"tables": [], "recorded": {}})
        e["tables"].append({"name": t["name"], "sha256": t["sha256"], **tab})
        for c in tab["columns"]:
            for k in c["classes"]:
                if c["filled"]:
                    e["recorded"].setdefault(k, []).append(c["header"])
    res = {"version": "1", "label": "Which conditions NASA's experimental tables record per run, by keyword rules on column headers. A column existing is not a value checked.",
           "rules": RULES, "slot_of": SLOT_OF, "manifest": str(manifest).replace("\\", "/"), "investigations": inv, "without_table": man["without_table"],
           "coverage": {k: sorted((i for i, e in inv.items() if k in e["recorded"]), key=lambda x: int(x.split("-")[1])) for k in RULES}}
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print({k: len(v) for k, v in res["coverage"].items()}, "of", len(inv), "investigations with a table;", len(man["without_table"]), "without")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("--dest", required=True, type=Path); f.add_argument("--manifest", required=True, type=Path)
    f.add_argument("--catalog", type=Path, default=Path("data/manifests/PSI_CATALOG_v1.json"))
    i = sub.add_parser("inventory"); i.add_argument("--src", required=True, type=Path); i.add_argument("--manifest", required=True, type=Path); i.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    return fetch(a.dest, a.manifest, a.catalog) if a.cmd == "fetch" else inventory(a.src, a.manifest, a.out)


if __name__ == "__main__":
    raise SystemExit(main())
