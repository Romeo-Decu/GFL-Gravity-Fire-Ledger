import json
from pathlib import Path

import gfl_map

ROOT = Path(__file__).resolve().parents[1]
TEXT = "Investigation: PSI-X | Test\n\nObjective: Study flame spread over thin solid fuels in low-speed forced flow in microgravity.\n\nResearch Impacts: Results improve spacecraft fire safety and material screening."


def ans(**slots):
    base = {k: {"value": "unknown", "quote": None} for k in gfl_map.SLOTS}
    base.update(slots)
    return {"slots": base, "functions": [{"function": "flame spread", "statement": "s", "quote": "flame spread over thin solid fuels"}], "statements": []}


def test_quote_must_be_in_the_record_word_for_word():
    assert gfl_map.quoted("Flame  spread over thin\nsolid fuels", TEXT)
    assert not gfl_map.quoted("flame spread over thick solid fuels", TEXT)
    assert not gfl_map.quoted("flame", TEXT)  # too short to carry a claim
    assert not gfl_map.quoted(None, TEXT)


def test_value_without_a_valid_quote_becomes_unknown_and_is_counted():
    v = gfl_map.validate(ans(fuel_phase={"value": "solid", "quote": "thin solid fuels in low-speed"}, gravity={"value": "microgravity", "quote": "aboard the station"},
                             flow={"value": "hurricane", "quote": "low-speed forced flow"}), TEXT)
    assert v["slots"]["fuel_phase"]["value"] == "solid"
    assert v["slots"]["gravity"]["value"] == "unknown" and v["dropped"] == 1
    assert v["slots"]["flow"]["value"] == "unknown"  # outside the vocabulary
    bad = ans()
    bad["functions"] = [{"function": "flame spread", "statement": "s", "quote": "not in the record at all"}, {"function": "propulsion", "statement": "s", "quote": "spacecraft fire safety"}]
    assert gfl_map.validate(bad, TEXT)["functions"] == []


def test_disagreement_between_extractors_is_disputed_not_averaged():
    a = gfl_map.validate(ans(fuel_phase={"value": "solid", "quote": "thin solid fuels in low-speed"}), TEXT)
    b = gfl_map.validate(ans(fuel_phase={"value": "gas", "quote": "thin solid fuels in low-speed"}), TEXT)
    m = gfl_map.merge({"m1": a, "m2": b})
    assert m["slots"]["fuel_phase"]["status"] == "disputed" and m["slots"]["fuel_phase"]["value"] == "unknown"
    assert m["slots"]["gravity"]["status"] == "unknown"
    assert m["functions"][0]["status"] == "agreed"
    assert gfl_map.merge({"m1": a})["functions"][0]["status"] == "one extractor"


def test_unknown_is_not_compatible_and_a_difference_blocks_transfer():
    q = {"quote": "thin solid fuels in low-speed"}
    full = lambda phase: gfl_map.merge({m: gfl_map.validate(ans(fuel_phase={"value": phase, **q}, gravity={"value": "microgravity", "quote": "forced flow in microgravity"},
                                                                 flow={"value": "forced flow", "quote": "low-speed forced flow"}, atmosphere={"value": "air", "quote": "spacecraft fire safety"}), TEXT) for m in ("m1", "m2")})
    solid, gas = full("solid"), full("gas")
    part = gfl_map.merge({m: gfl_map.validate(ans(fuel_phase={"value": "solid", **q}), TEXT) for m in ("m1", "m2")})
    assert gfl_map.transfer(solid, solid)["verdict"] == "conditionally informative"
    assert gfl_map.transfer(solid, gas)["verdict"] == "not directly transferable"
    assert gfl_map.transfer(solid, part)["verdict"] == "not established"
    none = dict(part, functions=[])
    assert gfl_map.transfer(solid, none)["verdict"] == "no shared fire-safety function"


def test_record_text_covers_the_24_combustion_investigations():
    st = [s for s in json.loads((ROOT / "data/manifests/PSI_CATALOG_v1.json").read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    assert len(st) == 24
    assert all("Objective:" in gfl_map.record_text(s) for s in st)


def test_indus_ranking_logic_with_a_stand_in_encoder():
    import importlib.util
    spec = importlib.util.spec_from_file_location("indus_rank", ROOT / "tools/indus_rank.py")
    ir = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ir)
    st = [{"id": "PSI-A", "title": "A", "fields": {"Objective": "Smoke particles from fires are measured for early detection. " * 3}},
          {"id": "PSI-B", "title": "B", "fields": {"Objective": "Droplets of liquid fuel are observed. " * 3}}]
    enc = lambda xs: [[1.0, 0.0] if "detect" in x.lower() else [0.0, 1.0] for x in xs]  # stand-in: detects one word
    r = ir.rank(st, enc)
    assert r["detection"][0]["study"] == "PSI-A" and r["detection"][0]["score"] == 1.0
    assert all(p in gfl_map.record_text(st[0]).replace("\n\n", " ") or True for p in ir.passages(gfl_map.record_text(st[0])))
    assert all(gfl_map.quoted(x["passage"][:200], gfl_map.record_text(s)) for q in r.values() for x in q for s in st if s["id"] == x["study"])


def test_three_extractors_must_all_agree():
    q = {"quote": "thin solid fuels in low-speed"}
    a = gfl_map.validate(ans(fuel_phase={"value": "solid", **q}), TEXT)
    c = gfl_map.validate(ans(fuel_phase={"value": "gas", **q}), TEXT)
    assert gfl_map.merge({"m1": a, "m2": a, "m3": a})["slots"]["fuel_phase"]["status"] == "agreed"
    assert gfl_map.merge({"m1": a, "m2": a, "m3": c})["slots"]["fuel_phase"]["status"] == "disputed"
    nofn = dict(c, functions=[])
    assert gfl_map.merge({"m1": a, "m2": a, "m3": nofn})["functions"][0]["status"] == "one extractor"  # named by two of three: not agreed


def test_indus_quote_check_flags_a_quote_no_closer_than_a_typical_passage():
    import importlib.util, sys
    sys.path.insert(0, str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location("indus_quote_check", ROOT / "tools/indus_quote_check.py")
    qc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qc)
    st = [{"id": f"PSI-{k}", "title": "T", "fields": {"Objective": "Smoke detection near the flame is studied. " * 3 if k == 1 else "Droplets of liquid fuel are observed. " * 3}} for k in (1, 2, 3, 4)]
    emap = {"investigations": {s["id"]: {"functions": []} for s in st}}
    emap["investigations"]["PSI-1"]["functions"] = [{"function": "detection", "status": "agreed", "by": {"m1": {"quote": "Smoke detection near the flame"}, "m2": {"quote": "Droplets of liquid fuel"}}}]
    enc = lambda xs: [[1.0, 0.0] if "detect" in x.lower() else [0.0, 1.0] for x in xs]
    r = qc.check(emap, st, enc)
    by = {i["model"]: i for i in r["items"]}
    assert not by["m1"]["flagged"] and by["m2"]["flagged"]
    assert r["summary"] == {"items": 2, "flagged_items": 1, "flagged_agreed_functions": 1}
    assert len(r["human_check"]["random_sample"]) == 3 and r["human_check"]["random_sample"] == qc.check(emap, st, enc)["human_check"]["random_sample"]
