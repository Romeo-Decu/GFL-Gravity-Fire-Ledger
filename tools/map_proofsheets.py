#!/usr/bin/env python3
"""Map NASA proof sheets (run identity) to NEF archives by the image numbers listed on each sheet (ISS-032).

For each proof sheet in <FIF_DATA>/Raw Data: read the image IDs it lists, find the archive(s) in the PSI-25 NEF archive
index whose image-number range contains them, and report exact matches. When the archive is held locally, its member
names are compared file by file.

    FIF_DATA=<root> python tools/map_proofsheets.py --out data/derived/PROOFSHEET_ARCHIVE_MAP_v1.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sheet_ids(pdf: Path) -> list[str]:
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    return sorted(set(re.findall(r"iss0\d\de0\d{5}", txt)))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    raw = Path(os.environ["FIF_DATA"]) / "Raw Data"
    idx = json.loads((ROOT / "data/manifests/PSI-25_NEF_archive_index.json").read_text())["archives"]
    out = {}
    for pdf in sorted(raw.glob("*Proof*Sheet*.pdf")) + sorted(raw.glob("*ProofSheet*.pdf")):
        if pdf.name in out:
            continue
        m = re.search(r"S(\d+M)_TP(B\d+)", pdf.name)
        ids = sheet_ids(pdf)
        prefix = {i[:8] for i in ids}
        nums = [int(i[-6:]) for i in ids]
        cands = [n for n, v in idx.items() if any(p in n for p in prefix) and v["first"] <= min(nums) and v["last"] >= max(nums)]
        rec = {"run": m.group(2) if m else None, "sample": m.group(1) if m else None, "sheet_images": len(ids),
               "first": ids[0] if ids else None, "last": ids[-1] if ids else None, "archives_covering_range": cands}
        for c in cands:
            z = raw / c
            if z.exists():
                names = sorted({Path(x).stem for x in zipfile.ZipFile(z).namelist() if x.upper().endswith(".NEF")})
                inside = [n for n in names if min(nums) <= int(n[-6:]) <= max(nums)]
                rec.setdefault("checked_locally", {})[c] = {"archive_images": len(names), "sheet_images_in_archive": len(set(ids) & set(names)),
                                                            "exact_match": names == ids, "archive_images_in_sheet_range": len(inside)}
        rec["verdict"] = ("confirmed file by file" if any(v.get("exact_match") for v in rec.get("checked_locally", {}).values())
                          else "range match, archive not held locally" if len(cands) == 1 else
                          "ambiguous" if cands else "no archive covers the sheet")
        out[pdf.name] = rec
    a.out.write_text(json.dumps({"method": "proof-sheet image IDs vs NEF archive index ranges; file-by-file when held", "sheets": out}, indent=1) + "\n")
    for k, v in out.items():
        print(v["run"], v["sheet_images"], v["first"], v["last"], v["archives_covering_range"], v["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
