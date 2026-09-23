"""Checks for the removal arithmetic, geography and inputs in arms.py.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/congestion_2026_09_23/ -q
"""
import importlib.util
import pathlib

import numpy as np
import pandas as pd
import pytest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("arms", HERE / "arms.py")
arms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arms)


def test_bpr_removal_is_the_integral_of_the_marginal_external_cost():
    # Others' delay as the removed share x rises from 0 to psi: D (1 - x)^beta. The saving is the
    # integral of the marginal external cost beta (1 - x)^(beta - 1), not beta * psi.
    psi, beta = 0.3, 4.0
    x = np.linspace(0, psi, 200001)
    mec = beta * (1 - x) ** (beta - 1)
    integral = np.sum(0.5 * (mec[1:] + mec[:-1]) * np.diff(x))
    assert abs(arms.bpr_saving(psi, beta) - integral) < 1e-9
    assert arms.bpr_saving(psi, beta, marginal=True) == pytest.approx(beta * psi)
    assert arms.bpr_saving(psi, beta) < beta * psi


def test_fill_in_shrinks_the_traffic_cut():
    psi, beta = 0.2, 4.0
    assert arms.bpr_saving(psi, beta, eta=1.0) == pytest.approx(1 - 0.8 ** 4)
    assert arms.bpr_saving(psi, beta, eta=0.44) == pytest.approx(1 - (0.8 ** 0.44) ** 4)
    assert arms.bpr_saving(psi, beta, eta=0.32) < arms.bpr_saving(psi, beta, eta=0.48) < arms.bpr_saving(psi, beta)


def test_supply_curve_equilibrium_matches_the_closed_form():
    # Solve C = ((1 - psi) VKT_o(C))^k with VKT_o = C^-sigma (C = 1 with the group in) by
    # bisection on x = ln C; excess(x) = x - k (ln(1 - psi) - sigma x) rises in x.
    for theta, sigma, psi in ((0.13, 16.0, 0.2), (0.19, 0.0, 0.35), (0.07, 8.0, 0.05)):
        k = theta / (1 - theta)
        lo, hi = -1.0, 0.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if mid - k * (np.log1p(-psi) - sigma * mid) > 0:
                hi = mid
            else:
                lo = mid
        assert lo == pytest.approx(arms.supply_exponent(theta, sigma) * np.log1p(-psi), rel=1e-9)


def test_surplus_fraction_is_the_area_under_demand():
    for sigma, c0 in ((0.0, 0.97), (16.0, 0.995), (8.0, 0.98), (1.0, 0.99)):
        c = np.linspace(c0, 1.0, 200001)
        demand = c ** -sigma
        area = np.sum(0.5 * (demand[1:] + demand[:-1]) * np.diff(c))
        assert arms.surplus_fraction(np.log(c0), sigma) == pytest.approx(area, rel=1e-8)


def test_period_split_preserves_the_all_day_share():
    phi, pi, p_other = 0.25, 0.9, 0.41
    peak, off = arms.periods(phi, pi, p_other)
    p_group = pi * p_other
    peak_total = phi * p_group + (1 - phi) * p_other
    assert peak * peak_total + off * (1 - peak_total) == pytest.approx(phi)


def test_time_cost_fall_is_capped_at_the_delay_share():
    e = pd.DataFrame({"other_persons": [100.0, 100.0], "group_persons": [400.0, 10.0],
                      "h_other_2022": [300.0, 300.0], "passenger_delay_ph": [900.0, 900.0],
                      "truck_delay_ph": [50.0, 50.0], "passenger_fuel_gal": [10.0, 10.0],
                      "truck_fuel_gal": [5.0, 5.0], "gas_price": [3.0, 3.0], "diesel_price": [4.0, 4.0]})
    vot = pd.Series({"all_purposes_local": 20.0, "truck_driver": 37.0})
    res = arms.time_cost_arm(e, np.log(np.array([0.5, 0.999])), 0.0, 0.1, 0.8, vot, 2022, 1.0)
    d = arms.delay_share(e, 2022, 1.0)
    assert res["capped"].tolist() == [True, False]
    assert res["pass_ph"][0] == pytest.approx(arms.others_hours(e, 2022)[0] * d[0])


def test_proportional_residual_uses_decreasing_returns():
    assert arms.proportional_elasticity("T5 col 6 IV2", 0.0) == pytest.approx(0.04 / 0.87)
    k = 0.13 / 0.87
    assert arms.proportional_elasticity("T5 col 6 IV2", 16.0) == pytest.approx(0.04 / 0.87 / (1 + 16 * k))


def test_allocation_preserves_totals_and_rejects_missing_pumas():
    wide = pd.DataFrame({"STATE": ["01", "01"], "PUMA": ["00100", "00200"], "group_x": [10.0, 5.0],
                         "other_x": [90.0, 45.0]})
    alloc = pd.DataFrame({"state": ["01", "01", "01"], "puma": ["00100", "00100", "00200"],
                          "ua": ["A", "B", "B"], "afact": [0.3, 0.9, 1.0]})
    areas = arms.allocate(wide, alloc, "ua")
    assert areas["group_x"].sum() == pytest.approx(15.0)
    assert areas.loc["A", "other_x"] == pytest.approx(90.0 * 0.25)
    with pytest.raises(ValueError):
        arms.allocate(wide, alloc[alloc.puma == "00100"], "ua")


def test_umr_names_parse_with_multi_state_suffixes():
    assert arms.parse_umr_name("Louisville-Jefferson County KY-IN") == ("louisville-jefferson county", ["KY", "IN"])
    assert arms.parse_umr_name("Walla Walla WA-OR") == ("walla walla", ["WA", "OR"])
    assert arms.parse_umr_name("New York-Newark NY-NJ-CT") == ("new york-newark", ["NY", "NJ", "CT"])


def test_umr_positive_control_reproduces_the_national_totals():
    u, summary = arms.load_umr()
    control = arms.positive_control(u, summary)
    assert control["passed"]
    assert control["sum_of_494_areas"]["congestion_cost_bn_2024usd"] == pytest.approx(268.724)


def test_value_of_time_method_reproduces_the_2015_guidance():
    _, checks = arms.vot_2024()
    assert checks["reproduce_2015_personal"] == pytest.approx(13.60, abs=0.05)
    assert checks["reproduce_2015_business"] == pytest.approx(25.40, abs=0.05)
    assert checks["reproduce_2015_all_purposes"] == pytest.approx(14.10, abs=0.05)
    assert checks["reproduce_2015_truck_driver"] == pytest.approx(27.20, abs=0.05)
