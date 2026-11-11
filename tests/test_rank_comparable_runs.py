import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rank_comparable_runs import parse_air, parse_material, rank  # noqa: E402

COLS = {"PI": "X", "Sample #": "1", "Flow restrictor": "2", "Calibrated  initial O2 % by vol ": "21"}


def row(test, material, air, **kw):
    r = dict(COLS, **{"Test #": test, "Fuel Sample Material": material, "Air display": air})
    r.update(kw)
    return r


def test_material_parsing():
    assert parse_material("2 cm 0.1 mm PMMA film") == {"material": "PMMA", "geometry": "film", "thickness_um": 100.0, "width_cm": 2.0}
    assert parse_material("100 micron PMMA film   2 cm wide")["thickness_um"] == 100.0
    assert parse_material('1/4" clear rod')["geometry"] == "rod"
    assert parse_material("2 cm SIBAL")["material"] == "SIBAL fabric"
    assert parse_material("")["material"] is None


def test_air_parsing_ignores_pots_and_bounds():
    assert parse_air("3  0.5 pot   0.4 pot") == [3.0]
    assert parse_air("2   <1") == [2.0]
    assert parse_air("5   pots 0.4   0.36   0.32   off") == [5.0]
    assert parse_air("see fan") is None and parse_air("") is None


def test_levels_and_unknown_never_matches():
    rows = [row("R", "2 cm 0.1 mm PMMA film", "3   5"),
            row("SAME", "2 cm 0.1 mm PMMA film", "3"),
            row("THICK", "2 cm 0.2 mm PMMA film", "5  3"),
            row("NOAIR", "2 cm 0.1 mm PMMA film", ""),
            row("ROD", '1/4" clear rod', "3"),
            row("O2", "2 cm 0.1 mm PMMA film", "3", **{"Calibrated  initial O2 % by vol ": "17.3"})]
    res = rank(rows, "R", 3.0)
    lv = {x["test"]: x["level"] for x in res["runs"]}
    assert lv == {"SAME": "same_conditions", "THICK": "close", "O2": "close", "NOAIR": "distant", "ROD": "not_comparable"}
    noair = next(x for x in res["runs"] if x["test"] == "NOAIR")
    assert noair["states"]["air_setting"] == "unknown"
    assert [x["test"] for x in res["runs"]][0] == "SAME" and res["runs"][-1]["test"] == "ROD"


def test_material_not_named_in_the_record_is_inferred_never_matched():
    assert parse_material("2 cm 0.4 mm thick film")["material"] == "PMMA (inferred)"
    rows = [row("R", "2 cm 0.1 mm PMMA film", "3"), row("F", "2 cm 0.1 mm film", "3")]
    f = rank(rows, "R", 3.0)["runs"][0]
    assert f["states"]["material"] == "inferred" and f["level"] == "distant"
