"""P7 reading-layer controls, finite gates, symmetric private gain and live endpoint contracts."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import beside_arms as B
import beside_extra as X
import world_ledger as W

D = Path(__file__).resolve().parent / "derived"


def fixture_valuation():
    return pd.DataFrame([dict(generation=g, line=line, cls=cls, end=end, G_bn=cost,
                             V_low_bn=value, V_central_bn=value, V_high_bn=value)
                         for g in W.GENS for end in ("low", "high")
                         for line, cls, cost, value in (("education_services", "education", 10.0, 0.0),
                                                       ("school_reprice", "education", 1.0, 0.0),
                                                       ("capital_k12", "education", 2.0, 0.0),
                                                       ("capital_k12_user_fees", "education", 0.5, 0.0),
                                                       ("college_rekey", "education", 3.0, 0.0),
                                                       ("general", "public_good", 5.0, 7.0),
                                                       ("health", "health", 4.0, 3.0))])


def test_bound_labels_and_zero_positive_control():
    obj = {"input": 1}
    expanded = B.bound_scenarios([("reading1", "reading_1", "Reading 1", obj, {"pgc": "average_cost"})])
    assert len(expanded) == 3
    assert expanded[0][0] == "reading1" and expanded[0][3] is obj
    assert expanded[0][4] == dict(pgc="average_cost", g3_bound="zero")
    for name, _, label, _, kw in expanded:
        assert "G3+" in label and B.G3_LABELS[B.scenario_bound(name)] in label
        assert kw["g3_bound"] == B.scenario_bound(name)
    assert B.base_name(expanded[2][0]) == "reading1"


def test_direct_cells_compensation_closes_after_source_rounding():
    common = dict(sex="male", band="25-44", cat=2, parent_cat=2, employment_rate=0.5,
                  weekly_hours_employed=40.0)
    for ppp in ("gdp", "consumption"):
        common.update({f"{field}_per_person_ppp_{ppp}": value for field, value in
                       (("gross", 100.0123), ("employer", 20.00123), ("compensation", 120.014),
                        ("withheld", 10.00123), ("total_tax", 30.003), ("income", 90.0), ("ctax", 8.0))})
    got = X.cells_dicts(pd.DataFrame([common]), pd.DataFrame([common]))
    for ppp in got:
        for pre in ("", "y"):
            for key in got[ppp][pre + "cash"]:
                assert got[ppp][pre + "inc"][key] == got[ppp][pre + "cash"][key] + got[ppp][pre + "employer"][key]
                assert got[ppp][pre + "tax"][key] == 10.00123 + got[ppp][pre + "employer"][key]


def test_wages_and_services_are_symmetric_positive_control():
    rows = []
    inp = {}
    for g in W.GENS:
        for name, value in (("premium", 10), ("mexico_taxes_avoided", 2), ("mexico_budget_lost", -7),
                            ("us_budget_value", 1), ("uncompensated_received", 2)):
            rows.append(dict(row=f"{name}_{g}", central=value))
        inp[g] = dict(us_taxes_bn=-4, us_wage_taxes_bn=-3, social_security_accrual_bn=3, part_a_accrual_bn=1)
    prem = {g: dict(tax=dict(central=1.5)) for g in W.GENS}
    got = pd.DataFrame(X.private_gain("reading1", pd.DataFrame(rows), inp,
                                    dict.fromkeys(W.GENS, 100), 80, "reading1", prem))
    generation = got[got.generation.ne("group")]
    # Prior asymmetric result is 10 - 4 + 2 - 7 = 1; wages alone restores the excluded Mexican services.
    assert np.allclose(generation.wages_only_bn, 8.5, atol=1e-12, rtol=0)
    assert np.allclose(generation.with_services_bn, 8 + 7 - 7, atol=1e-12, rtol=0)
    assert np.allclose(generation.with_old_age_accrual_bn, 12.5, atol=1e-12, rtol=0)
    for col in ("wages_only_bn", "with_services_bn", "with_old_age_accrual_bn"):
        assert abs(got[got.generation.eq("group")][col].iloc[0] - generation[col].sum()) < 1e-12


def test_wage_tax_whitelist_excludes_sales_property_and_source(monkeypatch):
    rows = [dict(generation=g, end=end, line=line, cls="tax", G_bn=-amount, V_central_bn=-amount)
            for g in W.GENS for end in ("low", "high")
            for line, amount in (("employee_hi", 2), ("employer_hi", 3),
                                 ("self_employment_oasdi_hi", 4), ("federal_income_tax", 5),
                                 ("general_sales_tax", 20), ("personal_property_tax", 30))]
    rows += [dict(generation=g, end=end, line="social_security", cls="cash", G_bn=7, V_central_bn=7)
             for g in W.GENS for end in ("low", "high")]
    arms = pd.DataFrame([dict(arm=X.PENSION_ARM, group=g, part_a_per_hi_tax_dollar=0.5,
                             part_a_bn=10, hi_tax_bn=20) for g in ("G1", "G2", "G3plus", "union")])
    monkeypatch.setattr(X.pd, "read_csv", lambda _: arms)
    inp, _ = X.private_gain_inputs(pd.DataFrame(rows))
    for g in W.GENS:
        assert inp[g]["us_wage_taxes_bn"] == -14
        assert inp[g]["us_taxes_bn"] == -64
        assert "general_sales_tax" not in X.WAGE_TAX_LINES
        assert "personal_property_tax" not in X.WAGE_TAX_LINES
        assert "corporate_labor" not in X.WAGE_TAX_LINES


def test_report_only_k12_changes_just_g3_k12():
    v = fixture_valuation()
    specs = pd.DataFrame(dict(end=["low", "high"], share=[0.7, 0.8])).set_index("end")
    got = X.g3_k12_at_cost(v, specs)
    selected = v.generation.eq("G3+") & v.line.isin(["education_services", "school_reprice", "capital_k12", "capital_k12_user_fees"])
    pd.testing.assert_frame_equal(got[~selected], v[~selected])
    for col in ("V_low_bn", "V_central_bn", "V_high_bn"):
        for r in got[selected].itertuples():
            expected = r.G_bn * (specs.loc[r.end, "share"] if r.line == "education_services" else 1.0)
            assert getattr(r, col) == expected
    assert got.V_central_bn.sum() - v.V_central_bn.sum() == 22.0


@pytest.mark.parametrize("elasticity", [0.5, 1.0])
def test_wtp_identity_then_one_change(elasticity):
    v = fixture_valuation()
    pos = pd.DataFrame([dict(measure="money", party=g, mean_y_pc=100.0)
                        for g in (*W.GENS, "other_residents")])
    equal, factors = X.public_goods_wtp(v, pos, elasticity)
    pd.testing.assert_frame_equal(equal, v)
    assert set(factors.values()) == {1.0}
    pos.loc[pos.party.eq("G1"), "mean_y_pc"] = 25.0
    got, factors = X.public_goods_wtp(v, pos, elasticity)
    assert factors["G1"] == 0.25 ** elasticity
    selected = v.generation.eq("G1") & v.cls.eq("public_good")
    pd.testing.assert_frame_equal(got[~selected], v[~selected])
    assert np.allclose(got.loc[selected, "V_central_bn"], 7 * factors["G1"], atol=1e-12, rtol=0)


def test_mexico_responsive_is_one_change():
    v = pd.DataFrame(dict(cls=["public_good", "health", "cash"], bn=[10.0, 4.0, 2.0]))
    got = X.mexico_public_goods_responsive(v)
    assert abs(got.bn.iloc[0] - 10 * W.MEXICO_PUBLIC_RESPONSE[1]) < 1e-12
    pd.testing.assert_frame_equal(got.iloc[1:], v.iloc[1:])


def test_endpoint_theta_from_lambda_slopes():
    rows = []
    for end in ("low", "high"):
        for name, extra in (("reading1", 0.0), ("reading2", 2.0)):
            for weight, increase in (("equal", 0), ("equal_lambda_1.16", 0.16)):
                rows.append(dict(scenario=name, end=end, g3_bound="zero", weighting=weight,
                                 group_total_bn=10 + extra, others_today_bn=-6 - 2 * increase,
                                 future_taxpayers_bn=-4 - increase, mexico_residents_bn=2 + increase,
                                 world_total_bn=2 + extra - 2 * increase))
    got = X.endpoint_theta_summary(pd.DataFrame(rows), {"theta_test": dict(theta_o=1.2, theta_f=1.3)})
    t = got[got.weighting.eq("theta_test")]
    assert np.allclose(t.other_us_residents_bn, -10.7, atol=1e-12, rtol=0)
    assert np.allclose(t.world_total_bn, np.where(t.scenario.eq("reading1"), 1.5, 3.5), atol=1e-12, rtol=0)
    assert np.allclose(t.world_change_bn, np.where(t.scenario.eq("reading1"), 0, 2), atol=1e-12, rtol=0)


def test_selected_theta_total_is_exact_full_positive_control():
    inp = W.load("oct14", "lineage")
    fac = W.channel_factors(inp, "money")
    fac["_lambda"] = {"equal_lambda_theta": 1.2}
    rows, prem, _ = W.build_rows(inp)
    full = W.totals(rows, prem, inp, "central", fac, inp["pos"])
    single = W.totals(rows, prem, inp, "central", fac, inp["pos"], requested_weightings=["equal_lambda_theta"])
    pd.testing.assert_frame_equal(single.reset_index(drop=True), full[full.weighting.eq("equal_lambda_theta")].reset_index(drop=True))


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_nonfinite_reading_totals_block(value):
    with pytest.raises(SystemExit, match="BLOCKED"):
        B.finite_gate("test", [0.0, value])
    with pytest.raises(SystemExit, match="BLOCKED"):
        X.derived_rows(dict.fromkeys(W.PARTIES, value))


def test_live_readings_each_bound_end_and_population():
    t = pd.read_csv(D / "p7_named_readings_oct14.csv")
    assert "us_residents_bn" not in t
    assert {"other_us_residents_bn", "us_residents_incl_group_bn"} <= set(t)
    assert set(t.end) == {"low", "high"}
    assert set(t.g3_bound) == set(B.G3_BOUNDS)
    assert {"equal", "equal_lambda_1.16", "equal_lambda_1.5", "equal_lambda_hendren_a"} <= set(t.weighting)
    assert t.label.str.contains("G3+", regex=False).all()
    by_name = t.assign(base=t.scenario.map(B.base_name)).groupby("base")
    for _, part in by_name:
        assert set(zip(part.end, part.g3_bound)) == {(e, b) for e in ("low", "high") for b in B.G3_BOUNDS}
    numbers = ["world_total_bn", "other_us_residents_bn", "us_residents_incl_group_bn", "group_total_bn", "mexico_residents_bn"]
    assert np.isfinite(t[numbers]).all().all()
    assert np.allclose(t.us_residents_incl_group_bn, t.other_us_residents_bn + t.group_total_bn, atol=2e-6, rtol=0)
    assert np.allclose(t.world_total_bn, t.us_residents_incl_group_bn + t.mexico_residents_bn, atol=2e-6, rtol=0)
    meta = json.loads((D / "beside_extra_meta_oct14.json").read_text())
    arms = pd.read_csv(D / "p7_beside_arms_endpoints_oct14.csv")
    arms = X.endpoint_theta_summary(arms, meta["arm4"]["theta"], reference="baseline")
    outer = pd.concat([t, arms])
    for wt, part in outer.groupby("weighting"):
        assert np.allclose(meta["p7"]["other_us_residents_outer_span_bn"][wt],
                           [part.other_us_residents_bn.min(), part.other_us_residents_bn.max()], atol=1e-6, rtol=0)


def test_live_private_forms_each_g3_bound():
    t = pd.read_csv(D / "p7_private_gain_oct14.csv")
    assert set(t.g3_bound) == set(B.G3_BOUNDS) and set(t.end) == {"low", "high"}
    assert np.allclose(t.wages_only_bn, t.premium_bn + t.us_wage_taxes_bn + t.mexico_wage_taxes_avoided_bn, atol=2e-6, rtol=0)
    assert np.allclose(t.with_services_bn, t.all_taxes_private_bn + t.us_services_bn + t.mexico_services_forgone_bn, atol=2e-6, rtol=0)
    g = t.groupby(["scenario", "end", t.generation.eq("group")]).wages_only_bn.sum().unstack()
    assert np.allclose(g[True], g[False], atol=2e-6, rtol=0)
