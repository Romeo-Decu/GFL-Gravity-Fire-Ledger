"""Build the PSI-25 asset index for a set of Bhattacharjee test IDs.

Joins only what is explicit: the test ID / sample number written in each PSI
file name, checked against the official Experimental Table CSV. Filename
sample numbers that disagree with the table are flagged, never corrected.

    python tools/family_assets.py --tests B1 B3 B6 B9 B15 B16 B19 B20 \
        --table <FIF_DATA>/psi25/Experimental table/PSI-25_Experimental table_BASS-II.csv \
        --out data/derived/BASSII_100UM_FAMILY_ASSETS_v0.1.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

NAME_PATTERNS = [
    # BASS_GMT188_SAMPLE_153_TESTB6..., BASS_GMT50_SAMPLE_148_TEST_B3...
    re.compile(r"BASS_GMT(?P<gmt>\d+)_SAMPLE_(?P<sample>\d+)_TEST_?(?P<test>B\d+)(?!\d)"),
    # GMT2014_188_BASS_S153M_TPB6_ProofSheet.pdf
    re.compile(r"GMT\d{4}_(?P<gmt>\d+)_BASS_S(?P<sample>\d+)M?_TP(?P<test>B\d+)(?!\d)"),
]


def parse_name(name: str) -> dict | None:
    for pat in NAME_PATTERNS:
        m = pat.search(name)
        if m:
            return {"gmt": m["gmt"], "sample": m["sample"], "test": m["test"]}
    return None


def asset_kind(name: str) -> str:
    n = name.lower()
    if "proofsheet" in n:
        return "proof_sheet_pdf"
    if "original vid" in n:  # PSI spells one archive "original vidoes"
        return "original_video_archive"
    if "still_sequence" in n:
        return "still_sequence_video"
    if "2nd_view" in n:
        return "second_view_video"
    if n.endswith(".mp4"):
        return "main_view_video"
    return "other"


def load_table(path: Path) -> dict[str, dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head, body = rows[0], rows[1:]
    i_test, i_sample, i_gmt = head.index("Test #"), head.index("Sample #"), head.index("GMT")
    return {r[i_test].strip(): {"sample": r[i_sample].strip(), "gmt": r[i_gmt].strip()} for r in body}


def build(manifest: dict, table: dict[str, dict], tests: list[str]) -> list[dict]:
    out = []
    for f in manifest["files"]:
        p = parse_name(f["name"])
        if not p or p["test"] not in tests:
            continue
        t = table.get(p["test"], {})
        table_sample = re.sub(r"\D", "", t.get("sample", ""))
        issues = []
        if table_sample and p["sample"] != table_sample:
            issues.append(f"filename sample {p['sample']} != table sample {t['sample']} for {p['test']}")
            owner = [k for k, v in table.items() if re.sub(r"\D", "", v["sample"]) == p["sample"]]
            if owner:
                issues.append(f"table assigns sample {p['sample']} to {'/'.join(owner)}")
        if t.get("gmt", "").isdigit() and int(p["gmt"]) != int(t["gmt"]):  # "050" == "50"
            issues.append(f"filename GMT {p['gmt']} != table GMT {t['gmt']}")
        out.append({
            "test_id_in_filename": p["test"],
            "table_sample": t.get("sample", ""),
            "filename_sample": p["sample"],
            "filename_gmt": p["gmt"],
            "asset_kind": asset_kind(f["name"]),
            "psi_name": f["name"],
            "psi_version": f["version"],
            "bytes": f["bytes"],
            "join_status": "conflict_unresolved" if issues else "filename_matches_table",
            "issues": "; ".join(issues),
        })
    out.sort(key=lambda r: (int(r["test_id_in_filename"][1:]), r["filename_sample"], r["asset_kind"]))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", nargs="+", required=True)
    ap.add_argument("--manifest", default="data/manifests/PSI-25_v4_manifest.json")
    ap.add_argument("--table", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rows = build(json.loads(Path(a.manifest).read_text(encoding="utf-8")), load_table(Path(a.table)), a.tests)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} assets, {sum(r['join_status'] != 'filename_matches_table' for r in rows)} flagged -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
