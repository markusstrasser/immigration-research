"""Gates on the job-capital taxes lane's tracked outputs (derived/), re-checked from the files alone.

  uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/job_capital_taxes_2026_10_14/test_gates.py -q
"""
import csv
import json
import math
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
LINES = ["c_and_i_property", "other_production_taxes", "corporate"]
READINGS = ["low", "high"]
MINING = ("211", "212", "213")


def load(name):
    return json.loads((DERIVED / name).read_text())


def rows(name):
    with (DERIVED / name).open() as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def summary():
    return load("summary.json")


@pytest.mark.parametrize("name", ["case_keys.json", "national.json", "summary.json"])
def test_every_build_gate_passed(name):
    gates = load(name)["gates"]
    assert gates and all(g["passed"] for g in gates), [g["gate"] for g in gates if not g["passed"]]


def test_line_cells_add_to_the_national_amounts():
    nat = load("national.json")["national_bn"]
    table = rows("national_by_industry.csv")
    for line in LINES:
        assert abs(sum(float(r[f"{line}_bn"]) for r in table) - nat[line]) < 1e-6
    case = load("case_keys.json")["national_bn"]
    assert all(abs(nat[line] - case[line]) < 1e-9 for line in LINES)


def test_no_housing_or_household_tax_in_the_item_cells():
    table = {r["cell"]: r for r in rows("national_by_industry.csv")}
    for cell in ("RESIDENTIAL", "HH814"):
        assert float(table[cell]["corporate_bn"]) == 0 and float(table[cell]["c_and_i_property_bn"]) == 0
    assert float(table["HH814"]["other_production_taxes_bn"]) == 0
    res = load("national.json")["residential_split"]["residential_parts_bn"]
    assert abs(float(table["RESIDENTIAL"]["other_production_taxes_bn"]) - sum(res.values())) < 1e-6


def test_mining_responds_at_zero_and_the_arm_adds_its_part(summary):
    for r in rows("wages_by_industry.csv"):
        if r["cell"] in MINING:
            assert r["responds"] == "0" and float(r["union_item_low_bn"]) == 0 and float(r["union_item_high_bn"]) == 0
        elif r["sector"] not in ("none",):
            assert r["responds"] == "1"
    for rd in READINGS:
        for a in ("personal", "shared"):
            added = summary["arms"]["mining_as_other_industries"][rd][a]["value_bn"] - summary["central"][rd][a]["value_bn"]
            assert abs(added - summary["mining"]["added_by_the_arm_bn"][rd][a]["value_bn"]) < 1e-8 and added < 0
            assert summary["central_by_sector_bn"][rd][a]["mining"] == 0


def test_the_corporate_response_moves_with_the_reading(summary):
    p = summary["parameters"]
    nr = load("national.json")["normal_return"]
    assert p["corporate_response"] == {"low": 1.0, "high": nr["share"]} and nr["share"] == 0.37
    assert abs(2 * nr["ota_2021_labor_share_pct"] / 100 - nr["share"]) < 1e-12
    assert nr["power_frerick"]["2003_2013"] == 0.25 and nr["power_frerick"]["1992_2002"] == 0.40
    for a in ("personal", "shared"):
        low, high = (summary["central"][rd][a]["by_line_bn"] for rd in READINGS)
        assert abs(high["corporate"] - nr["share"] * low["corporate"]) < 1e-8
        assert all(abs(high[ln] - low[ln]) < 1e-12 for ln in ("c_and_i_property", "other_production_taxes"))


def test_the_plain_wage_share_arm_is_the_receipt_lanes_ceiling(summary):
    c = summary["arms"]["plain_wage_share_ceiling"]
    assert abs(c["shared"] + 86.848983) < 1e-6 and abs(c["personal"] + 80.976701) < 1e-6


def test_items_add_by_line_and_generation(summary):
    items = rows("items.csv")
    for rd in READINGS:
        for a in ("personal", "shared"):
            sel = [r for r in items if r["row"] == "central" and r["reading"] == rd and r["allocation"] == a]
            parts = [float(r["value_bn"]) for r in sel if r["line"] in LINES]
            total = next(float(r["value_bn"]) for r in sel if r["line"] == "all")
            assert len(parts) == 3 and abs(sum(parts) - total) < 1e-8
            assert abs(total - summary["central"][rd][a]["value_bn"]) < 1e-8
            gens = summary["generations"][rd][a]
            assert abs(sum(gens[g]["item_bn"] for g in ("G1", "G2", "G3plus")) - gens["union"]["item_bn"]) < 1e-6
            assert abs(sum(summary["central_by_sector_bn"][rd][a].values()) - total) < 1e-6


def test_the_business_property_response_is_its_formula(summary):
    p = summary["parameters"]
    r_b = 1 - p["lambda_b"] * (1 - p["delta_L"]["group_population"])
    assert abs(p["r_b"]["group_population"] - r_b) < 1e-8
    assert abs(p["business_property_response"] - (p["tau"] + (1 - p["tau"]) * r_b)) < 1e-8
    assert 0 < p["lambda_b"] < 1 and 0 < p["tau"] < 1 and 0 <= p["delta_L"]["group_population"] <= 1


def test_shares_are_shares_and_thin_cells_are_pooled(summary):
    n_min = summary["pooling"]["n_min"]
    pooled = set(summary["pooling"]["pooled_cells"])
    for r in rows("wages_by_industry.csv"):
        for k in ("union_own_share", "union_share", "G1_share", "G2_share", "G3plus_share", "white_share"):
            assert 0 <= float(r[k]) <= 1
        if r["cell"] in pooled:
            assert int(r["cps_earners"]) < n_min and r["share_pooled_over"] != "own"
        elif r["sector"] != "none":
            assert int(r["cps_earners"]) >= n_min and r["share_pooled_over"] == "own"


def test_the_by_industry_table_adds_to_the_central(summary):
    table = rows("wages_by_industry.csv")
    for rd in READINGS:
        for a in ("personal", "shared"):
            got = sum(float(r[f"union_item_{rd}_bn"]) for r in table if r["allocation"] == a)
            assert abs(got - summary["central"][rd][a]["value_bn"]) < 1e-6


def test_the_crosswalk_table_covers_every_code():
    inputs = {r["census_code"]: r["bea_industry"] for r in csv.DictReader((HERE / "inputs/census_industry_crosswalk.csv").open())}
    table = rows("industry_crosswalk.csv")
    assert {r["census_code"]: r["bea_industry"] for r in table} == inputs
    assert all(0 <= float(r["union_wage_share"]) <= 1 for r in table if r["union_wage_share"])


def test_every_arm_has_both_readings_and_allocations_and_a_finite_value(summary):
    for name, arm in summary["arms"].items():
        cells = [arm[a] for a in ("personal", "shared")] if name == "plain_wage_share_ceiling" else \
            [arm[rd][a]["value_bn"] for rd in READINGS for a in ("personal", "shared")]
        assert all(math.isfinite(v) and v < 0 for v in cells), name


ITEM_LINES = ["corporate", "other_production_taxes", "business_property"]
FACTORS = ["G1", "G2", "G3plus", "white_nh", "black_nh", "union"]
ALLOCS = ["personal", "shared"]


def test_the_item_file_meets_main_case_v7s_contract(summary):
    """The checks main_case_2026_10_14 item_job_capital.cjs makes on read, on the central and every arm."""
    item = load("item.json")
    case = load("case_keys.json")
    pws = case["case_wage_key"]["shares"]["union"]
    nat = {"corporate": case["national_bn"]["corporate"], "other_production_taxes": case["national_bn"]["other_production_taxes"],
           "business_property": case["national_bn"]["c_and_i_property"]}
    for name, b in [("central", item)] + list(item["arms"].items()):
        for g in ITEM_LINES:
            ln = b["lines"][g]
            assert math.isfinite(ln["national_bn"]) and all(math.isfinite(ln["response"][rd]) for rd in READINGS), name
            for a in ALLOCS:
                assert abs(ln["group_bn"][a] - ln["key_share"][a] * ln["national_bn"]) <= 1e-9, (name, g, a)
                assert abs(sum(b["by_generation"][G][g][a] for G in ("G1", "G2", "G3plus")) - ln["group_bn"][a]) <= 1e-9, (name, g, a)
                assert abs(b["factor"]["union"][g][a] - ln["key_share"][a] / ln["plain_wage_share"][a]) <= 1e-9, (name, g, a)
                assert ln["plain_wage_share"][a] == pws[a], (name, g, a)
                assert all(math.isfinite(b["factor"][F][g][a]) for F in FACTORS), (name, g, a)
                for rd in READINGS:
                    assert abs(ln["item_bn"][rd][a] - ln["response"][rd] * ln["group_bn"][a]) <= 1e-12, (name, g, a, rd)
        for rd in READINGS:
            for a in ALLOCS:
                assert abs(sum(b["lines"][g]["item_bn"][rd][a] for g in ITEM_LINES) - b["central_bn"][rd][a]) <= 1e-9, name
    for g in ITEM_LINES:
        assert abs(item["lines"][g]["national_bn"] - nat[g]) <= 1e-6
    assert item["lines"]["other_production_taxes"]["response"] == {"low": 1.0, "high": 1.0}
    assert item["lines"]["corporate"]["response"] == {"low": 1.0, "high": 0.37}
    for rd in READINGS:
        for a in ALLOCS:
            assert abs(item["net_cost_change_bn"][rd][a] - summary["central"][rd][a]["value_bn"]) < 1e-8
    pw = item["per_wage_dollar"]
    for rd in READINGS:
        for F in FACTORS + ["national"]:
            assert all(math.isfinite(pw[rd][F]["all"][a]) and pw[rd][F]["all"][a] > 0 for a in ALLOCS), (rd, F)
    assert all({"name", "passed", "value"} <= set(g) and g["passed"] for g in item["gates"])
