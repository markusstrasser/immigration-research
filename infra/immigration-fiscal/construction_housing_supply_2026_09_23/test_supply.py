"""Checks for the supply offset in supply.py.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/construction_housing_supply_2026_09_23/ -q
"""
import importlib.util
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("supply", HERE / "supply.py")
supply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supply)
arms = supply.arms
S = arms.TARGET / arms.RESIDENTS


def test_pass_through_is_the_supply_demand_share():
    # pi = eS / (eD + eS) with the Cobb-Douglas supply elasticity eS = (1 - a) / a.
    for level in supply.LEVELS:
        hp = supply.housing_params(level)
        e_s = (1 - hp["a"]) / hp["a"]
        assert abs(hp["pi"] - e_s / (hp["eD"] + e_s)) < 1e-12
        assert abs(hp["e_d"] - 1 / (hp["eD"] + e_s)) < 1e-12


def test_land_part_vanishes_at_unit_demand_elasticity():
    # With eD = 1 spending on housing is fixed, so cheaper structures leave land rent unchanged.
    e_total, e_land = supply.elasticities("low", -0.02, np.array([S]))
    assert abs(e_land[0] - supply.housing_params("low")["e_d"]) < 1e-12
    assert e_total[0] < e_land[0]


def test_zero_cost_change_reproduces_the_housing_lane():
    areas, _ = arms.load_areas()
    for geography in ("national_uniform", "metro_local"):
        s = np.full(len(areas), S) if geography == "national_uniform" else areas["group_share"].to_numpy()
        e_total, e_land = supply.elasticities("central", np.zeros(len(areas)), s)
        base = arms.evaluate(areas, "long_run", "central", "A", geography, "central")
        new = arms.evaluate(areas, "long_run", "central", "A", geography, "central", e_override=np.asarray(e_total))
        for key in ("other_renters_extra_rent_bn", "net_other_residents_welfare_bn",
                    "other_owner_value_gain_stock_bn"):
            assert abs(base[key] - new[key]) < 1e-9 * max(1, abs(base[key]))


def test_log_rent_change_adds_demand_and_supply():
    # Form A with e_total gives ln(P1/P0) = e_d ln(1/(1-s)) + pi dlnc exactly.
    dlnc = -0.015
    e_total, _ = supply.elasticities("central", dlnc, np.array([S]))
    f, _ = arms.effect("A", e_total, np.array([S]))
    hp = supply.housing_params("central")
    assert abs(-np.log(1 - f[0]) - (hp["e_d"] * -np.log(1 - S) + hp["pi"] * dlnc)) < 1e-12


def test_cost_change_is_the_share_weighted_wage_change():
    inp = supply.load_inputs()
    theta, ell, wages = inp["theta"], inp["ell"], inp["wages"]
    total, a_part, b_part = supply.cost_change("A_central", inp)
    dw_low, dw_high = wages["hs_or_less"][2.0]
    share = ell["hs_or_less"]
    assert b_part == 0 and abs(total - theta["central"] * (share * dw_low + (1 - share) * dw_high)) < 1e-15
    # The account's CES: with the group present low-skill wages are lower, high-skill higher.
    assert dw_low < 0 < dw_high


def test_premiums_add_to_the_account_part():
    # Every premium case keeps the A part of its sigma and theta and adds a cost reduction.
    inp = supply.load_inputs()
    for case, (sigma, level, premium, split) in supply.COST_CASES.items():
        total, a_part, b_part = supply.cost_change(case, inp)
        dw_low, dw_high = inp["wages"][split][sigma]
        share = inp["ell"][split]
        assert abs(a_part - inp["theta"][level] * (share * dw_low + (1 - share) * dw_high)) < 1e-15
        assert (b_part == 0) == (premium is None) and b_part <= 0 and abs(total - a_part - b_part) < 1e-15
    # The Bratsberg-Raaum dose is construction's excess immigrant intensity, so it is positive.
    assert 0 < inp["br_dose"] < 0.2
