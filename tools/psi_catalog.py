#!/usr/bin/env python3
"""Catalogue of NASA PSI investigations, from the PSI metadata service (the data source named by the challenge).

For every study listed by PSI: identifier, title, the descriptive fields NASA wrote (objective, hypothesis, approach,
research impacts, hardware, research area), design descriptors and publications. Nothing is interpreted here and
nothing is written by a model: every value is copied from PSI. People's contact details are not kept.

    python tools/psi_catalog.py --out data/manifests/PSI_CATALOG_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://psi.nasa.gov/geode-py/ws"
UA = {"User-Agent": "GFL-catalog/1.0 (+research; NASA PSI public data)"}
FIELDS = ["Investigation Acronym", "Research Area", "SubResearch Area", "Objective", "Hypothesis", "Approach", "Research Impacts",
          "Experiment Hardware", "Flight Platform", "Managing NASA Center", "Project Type", "DOI", "Investigation Start Date", "Investigation End Date"]


def get(url: str) -> bytes:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:  # noqa: S310 - fixed public NASA host
                return r.read()
        except Exception:  # noqa: BLE001
            if attempt == 2:
                raise
            time.sleep(2)


def study(raw: bytes) -> dict:
    d = json.loads(raw)
    s = d["studies"][0]
    com = {c["name"]: (c.get("value") or "").strip() for c in s.get("comments", [])}
    return {"id": s["identifier"], "title": s.get("title", "").strip(), "description": (s.get("description") or "").strip(),
            "public_release": s.get("publicReleaseDate"), "version": d.get("version"),
            "fields": {k: com[k] for k in FIELDS if com.get(k)},
            "descriptors": [x["annotationValue"] for x in s.get("studyDesignDescriptors", []) if x.get("annotationValue")],
            "publications": [{"title": p.get("title", "").strip(), "doi": p.get("doi", "").strip(), "authors": p.get("authorList", "").strip()}
                             for p in s.get("publications", []) if p.get("title")],
            "metadata_sha256": hashlib.sha256(raw).hexdigest(), "source": f"{API}/studies/{s['identifier']}/metadata"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    ids = json.loads(get(f"{API}/studies"))["content"]
    out, failed = [], []
    for i in ids:
        try:
            out.append(study(get(f"{API}/studies/{i}/metadata")))
        except Exception as e:  # noqa: BLE001 - recorded, never hidden
            failed.append({"id": i, "error": f"{type(e).__name__}: {e}"[:200]})
    out.sort(key=lambda s: int(s["id"].split("-")[1]))
    res = {"source": f"{API}/studies", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "listed_by_psi": len(ids), "retrieved": len(out), "failed": failed,
           "note": "Values copied from NASA PSI; no interpretation. Contact details of people are not kept.", "studies": out}
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    areas = {}
    for s in out:
        areas[s["fields"].get("Research Area", "not stated")] = areas.get(s["fields"].get("Research Area", "not stated"), 0) + 1
    print(json.dumps({"listed": len(ids), "retrieved": len(out), "failed": len(failed), "by_research_area": areas}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
