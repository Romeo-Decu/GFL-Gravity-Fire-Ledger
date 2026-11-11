"""Run records for the measured BASS-II runs: NASA table fields as recorded, proof-sheet identity, frozen-rule rates."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / "data/derived/BASSII_COMPARABLE_RUNS_v1.json"
RATES = ROOT / "data/derived/rw4"
# NEF stills used == stills listed on the NASA proof sheet (checked file name by file name)
IDENTITY = {"B6": "77/77 stills match GMT2014_188_BASS_S153M_TPB6_ProofSheet.pdf",
            "B9": "51/51 stills match GMT2014_188_BASS_S154M_TPB9_ProofSheet.pdf (RES-035)",
            "B11": "136/136 stills match GMT2014_188_BASS_S158M_TPB11_ProofSheet.pdf",
            "B13": "188/188 stills match GMT2014_188_BASS_S162M_TPB13_ProofSheet.pdf (RES-036)"}


def _table_row(run: str) -> dict:
    d = json.loads(TABLE.read_text())
    if d["reference"]["test"] == run:
        return d["reference"]
    return next(r for r in d["runs"] if r["test"] == run)


def record(run: str, air_display: int, rule: str = "R-W4") -> dict:
    row = _table_row(run)
    c = row["conditions"]
    rec = {"run": run, "material": row["material_as_recorded"], "thickness_um": c["thickness_um"], "width_cm": c["width_cm"],
           "restrictor": c["flow_restrictor"], "o2_pct": c["initial_o2_pct"], "air_display": air_display,
           "identity_confirmed": run in IDENTITY, "identity_ref": IDENTITY.get(run, "none"), "rule": rule,
           "reference_definition": None, "rate_mm_s": None, "interval_mm_s": None, "rate_ref": "none"}
    f = RATES / f"{run}_RW4_RATES.json"
    if f.exists():
        seg = next((s for s in json.loads(f.read_text())["segments"] if s["air_display"] == air_display and s.get("budget")), None)
        if seg:
            b = seg["budget"]
            rec.update(reference_definition=b["reference_definition"], rate_mm_s=b["rate_mm_s"],
                       interval_mm_s=b["reported_interval_mm_s"], rate_ref=str(f.relative_to(ROOT)))
    return rec


def thickness_um(material: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)\s*mm", material)
    return float(m.group(1)) * 1000 if m else None
