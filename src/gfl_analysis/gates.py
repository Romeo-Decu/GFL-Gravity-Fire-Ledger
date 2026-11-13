"""A2. Transfer gates computed from measured and recorded values (ruleset v0.2).

The v0.1 engine evaluated gate states declared by hand. Here every gate state is computed from a run record:
NASA table fields, proof-sheet identity, the frozen-rule rate files, CRAM-1 and CRAM-2. The deterministic engine
(src/fif_transfer) then applies its unchanged decision policy.
"""
from __future__ import annotations

import json
from pathlib import Path

from fif_transfer.engine import assess

from . import regime

ROOT = Path(__file__).resolve().parents[2]
RULESET = ROOT / "configs" / "BASSII_RUN_TO_RUN_RULESET_v0.2.json"


def _g(status, reasons, refs, rules):
    return {"status": status, "reasons": reasons, "evidence_refs": refs, "rule_ids": rules}


def material_state(record: dict) -> str:
    m = (record.get("material") or "").lower()
    return "named" if "pmma" in m else ("inferred" if "film" in m else "unknown")


def compute_gates(src: dict, tgt: dict) -> dict:
    """src / tgt: run records with keys run, material, thickness_um, width_cm, restrictor, o2_pct, air_display,
    identity_confirmed (bool), rule, reference_definition, rate_mm_s (or None), interval_mm_s, rate_ref."""
    g = {}
    ids = [r["run"] for r in (src, tgt)]
    ok = src.get("identity_confirmed") and tgt.get("identity_confirmed")
    g["run_identity"] = _g("pass" if ok else "partial", [f"proof-sheet identity {'confirmed' if ok else 'not confirmed'} for {ids}"],
                           [src.get("identity_ref", "none"), tgt.get("identity_ref", "none")], ["R2-ID"])
    same_obs = src.get("rule") == tgt.get("rule") and src.get("reference_definition") == tgt.get("reference_definition")
    g["observable_equivalence"] = _g("pass" if same_obs else "fail", [f"same rule and optical definition ({src.get('rule')} / {tgt.get('rule')}, {src.get('reference_definition')} / {tgt.get('reference_definition')}): the same procedure, both luminous-edge rates"],
                                     [src.get("rate_ref", "none"), tgt.get("rate_ref", "none")], ["R2-OBS"])
    ms = (material_state(src), material_state(tgt))
    if "unknown" in ms:
        mg = "unknown"
    elif ms != ("named", "named"):
        mg = "partial"
    elif src["thickness_um"] != tgt["thickness_um"]:
        mg = "partial"
    else:
        mg = "pass"
    g["material_geometry"] = _g(mg, [f"material {ms}, thickness {src['thickness_um']} / {tgt['thickness_um']} um"
                                     + (" (bridged by thin-fuel 1/thickness scaling, bounded assumption)" if src["thickness_um"] != tgt["thickness_um"] else "")],
                                ["PSI-25 Experimental table"], ["R2-MAT", "R2-THK"])
    reg = (regime.classify(src["air_display"]), regime.classify(tgt["air_display"]))
    do2 = abs((src.get("o2_pct") or 0) - (tgt.get("o2_pct") or 0)) if src.get("o2_pct") and tgt.get("o2_pct") else None
    if do2 is None:
        af = "unknown"
    elif do2 > 0.5:
        af = "fail"
    else:
        af = "pass" if all(r["regime"] == "thermal" for r in reg) else "partial"
    notes = [f"{r['run']}: {r['flow_note']}" for r in (src, tgt) if r.get("flow_note")]
    if notes and af == "pass":
        af = "partial"
    g["atmosphere_flow"] = _g(af, [f"O2 difference {do2} points; flow {[r.get('u_cm_s') for r in reg]} cm/s on the duct centreline" + ("; " + "; ".join(notes) if notes else "")],
                              ["PSI-25 Experimental table", "PSI-25 fan calibration (A0)"], ["R2-O2", "R2-REG"])
    regs = [r["regime"] for r in reg]
    rv = "pass" if all(x == "thermal" for x in regs) else ("partial" if all(x.startswith("thermal") for x in regs) else "fail")
    g["regime_validity"] = _g(rv, [f"CRAM-2 regimes {regs}"], ["src/gfl_analysis/regime.py"], ["R2-REG"])
    bc = src.get("width_cm") == tgt.get("width_cm") and src.get("restrictor") == tgt.get("restrictor")
    g["boundary_conditions"] = _g("partial", [f"recorded width {src.get('width_cm')} / {tgt.get('width_cm')} cm and restrictor {src.get('restrictor')} / {tgt.get('restrictor')} "
                                              + ("are equal" if bc else "differ") + "; mounting, pressure history and the flow at the sample are not recorded, and unknown is not counted as equal"],
                                  ["PSI-25 Experimental table"], ["R2-BC"])
    mr = src.get("rate_mm_s") is not None and tgt.get("rate_mm_s") is not None
    g["measurement_reconstruction"] = _g("pass" if mr else "unknown", [f"rates {src.get('rate_mm_s')} / {tgt.get('rate_mm_s')} mm/s"],
                                         [src.get("rate_ref", "none"), tgt.get("rate_ref", "none")], ["R2-OBS"])
    g["uncertainty_and_reproducibility"] = _g("partial", ["statistical and analyst-choice layers reported; luminous-edge offset unbounded (A5)"],
                                              ["src/gfl_analysis/uq.py", "ISS-050"], ["R2-UQ"])
    g["domain_statement"] = _g("pass", ["domain stated in the request"], ["configs/BASSII_RUN_TO_RUN_RULESET_v0.2.json"], ["R2-ID"])
    return g


def assess_pair(src: dict, tgt: dict) -> dict:
    ruleset = json.loads(RULESET.read_text())
    payload = {"inference": "quantitative_transfer", "gates": compute_gates(src, tgt),
               "domain_statement": f"Luminous-edge spread rate, thin PMMA film, microgravity, BASS-II {src['run']} to {tgt['run']}, frozen rule {src.get('rule')}.",
               "prohibited_extrapolations": ruleset["scope"]["prohibited_uses"], "conflicts": [], "incompatibilities": []}
    return assess(payload, ruleset)
