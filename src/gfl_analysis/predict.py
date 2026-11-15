"""Pre-registered tests: write down what you expect before you look, let GFL seal it, then score it.

How a physicist uses it:
  1. Choose a target run not yet analysed and a reference run already measured.
  2. GFL proposes the expected rate from the stated law (thin-fuel 1/thickness, or the empirical thickness exponent
     measured so far) with a band, or you state your own expectation and band.
  3. The prediction is sealed (SHA-256, time, ledger entry) before the target data are opened.
  4. When the target is measured with the frozen rule, GFL scores it: supported, not supported, or not testable.
     Not testable is never counted as supported. The ratio interval includes the reference run's own uncertainty.
A run outside the domain of the law (other oxygen level, width, material not named, regime not thermal) gets no
proposal: GFL says why instead.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from . import regime
from .gates import material_state

LAWS = {
    "thin_fuel_inverse_thickness": {"exponent": -1.0, "band_rel": 0.15,
                                    "basis": "de Ris thin-fuel thermal regime: rate proportional to 1/thickness, independent of flow"},
    "empirical_exponent_rw4": {"exponent": -1.192, "exponent_ci95": [-1.53, -0.854], "band_rel": 0.15,
                               "basis": "weighted fit over B6, B9, B11, B13 (RES-038, data/derived/rw4/THICKNESS_EXPONENT_v1.json)"},
}


def domain_check(ref: dict, tgt: dict) -> list[str]:
    why = []
    if material_state(tgt) != "named":
        why.append("material not named as PMMA in the record")
    if ref.get("o2_pct") is None or tgt.get("o2_pct") is None or abs(ref["o2_pct"] - tgt["o2_pct"]) > 0.5:
        why.append(f"oxygen differs ({ref.get('o2_pct')} vs {tgt.get('o2_pct')} %): flame temperature at other oxygen levels is not sourced")
    if ref.get("width_cm") != tgt.get("width_cm"):
        why.append(f"width differs ({ref.get('width_cm')} vs {tgt.get('width_cm')} cm): edge effects not modelled")
    if not regime.classify(tgt["air_display"])["regime"].startswith("thermal"):
        why.append("target flow level not in the thermal regime (CRAM-2)")
    return why


def propose(ref: dict, tgt: dict, law: str) -> dict:
    why = domain_check(ref, tgt)
    if why:
        return {"target": tgt["run"], "reference": ref["run"], "law": law, "proposal": None, "out_of_domain": why}
    L = LAWS[law]
    k = tgt["thickness_um"] / ref["thickness_um"]
    r = k ** L["exponent"]
    lo, hi = (min(k ** e for e in L["exponent_ci95"]), max(k ** e for e in L["exponent_ci95"])) if "exponent_ci95" in L else (r, r)
    band = [round(lo * (1 - L["band_rel"]), 4), round(hi * (1 + L["band_rel"]), 4)]  # law uncertainty, then the same +-15 % measurement tolerance
    return {"target": tgt["run"], "target_air_display": tgt["air_display"], "reference": ref["run"], "reference_air_display": ref["air_display"],
            "law": law, "basis": L["basis"], "expected_ratio": round(r, 4), "band_ratio": band,
            "expected_rate_mm_s": round(r * ref["rate_mm_s"], 4), "rule": "R-W4", "out_of_domain": [],
            "how_scored": "measured target rate / measured reference rate under R-W4 at the stated flow levels; supported if inside the band"}


def seal(proposal: dict, author: str = "GFL") -> dict:
    rec = dict(proposal, registered_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(), author=author)
    rec["sha256"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    return rec


def evaluate(pred: dict, measured: dict | None, ref: dict) -> dict:
    if measured is None:
        return {"verdict": "not testable", "why": "no measurement of the target"}
    if measured.get("rate_ref") == "none":
        return {"verdict": "pending", "why": "target not measured yet; it will be scored when measured with the frozen rule"}
    if measured.get("rate_mm_s") is None:
        return {"verdict": "not testable", "why": "no segment of the target passed the frozen rule at the predicted flow level"}
    r = measured["rate_mm_s"] / ref["rate_mm_s"]
    mlo, mhi = measured["interval_mm_s"]
    rlo, rhi = ref["interval_mm_s"]
    lo, hi = pred["band_ratio"]
    return {"ratio": round(r, 4), "ratio_interval_with_reference_uncertainty": [round(mlo / rhi, 4), round(mhi / rlo, 4)],
            "band_ratio": [lo, hi], "verdict": "supported" if lo <= r <= hi else "not supported",
            "interval_overlaps_band": (mlo / rhi) <= hi and (mhi / rlo) >= lo}
