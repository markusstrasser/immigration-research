"""P7 Mexican compensation: statutory provenance, conservation and cash positive controls."""
import io
import json

import numpy as np
import pandas as pd
import pytest

import mexico as M
import mexico_compensation as MC


def test_primary_source_hash_fails_closed(tmp_path, monkeypatch):
    p = tmp_path / "changed.txt"
    p.write_text("not the pinned primary source")
    (tmp_path / "pins.json").write_text(json.dumps({"files": {
        "changed.txt": {"path": "changed.txt", "sha256": "0" * 64}}}))
    monkeypatch.setattr(M, "INPUTS", tmp_path)
    monkeypatch.setattr(M, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="primary_source_sha256"):
        M.pinned_text("changed.txt")


def test_2024_schedule_is_parsed_and_contributions_add_once():
    p = M.employer_parameters()
    # Independent formula at five UMA: use the source's own parsed values, the last
    # 2024 CEAV tier, and the fixed UMA quota. Detect wrong year, duplicate SAR or caps.
    g = np.array([0.0, 5 * M.UMA_YEAR, 50 * M.UMA_YEAR])
    c = M.mx_employer_contributions(g)
    base = np.minimum(g, p["cap_uma"] * M.UMA_YEAR)
    expected = ((base * (p["cash_benefit"] + p["pension_medical"] + p["disability_life"]
                          + p["daycare"] + p["risk"] + p["retirement"]
                          + p["ceav_rates"][-1] + p["housing"]))
                + p["excess"] * np.maximum(base - 3 * M.UMA_YEAR, 0)
                + p["fixed"] * M.UMA_YEAR * (g > 0))
    np.testing.assert_allclose(c["total"], expected, rtol=0, atol=1e-9)
    np.testing.assert_allclose(c["total"], c["imss"] + c["housing"] + c["retirement"], rtol=0, atol=1e-9)
    assert c["total"][0] == 0
    for component in c:
        assert (c[component] >= 0).all()


def test_occupational_risk_bound_and_unknown_duration_are_explicit():
    p = M.employer_parameters()
    g = np.array([0., 1000., 5 * M.UMA_YEAR])
    central = M.mx_employer_contributions(g)
    low = M.mx_employer_contributions(g, p["risk_min"])
    high = M.mx_employer_contributions(g, p["risk_max"])
    full = M.mx_employer_contributions(g, full_year=True)
    assert (low["total"] <= central["total"]).all()
    assert (high["total"] >= central["total"]).all()
    assert (full["total"] >= central["total"]).all()
    assert full["total"][0] == 0
    with pytest.raises(SystemExit, match="risk_inside_statute"):
        M.mx_employer_contributions(g, p["risk_min"] / 2)


@pytest.mark.parametrize("g", [[np.nan], [np.inf], [-1.]])
def test_nonfinite_or_negative_formal_pay_blocks(g):
    with pytest.raises(SystemExit, match="pay_finite_nonnegative"):
        M.mx_employer_contributions(g)


@pytest.fixture(scope="module")
def enigh():
    return M.load_enigh()


def test_formal_only_and_cash_tax_basis_stays_unchanged(enigh):
    d = enigh
    assert (d.employer_mxn[d.formal_net_mxn == 0] == 0).all()
    np.testing.assert_allclose(d.compensation_mxn, d.gross_mxn + d.employer_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.total_tax_mxn, d.withheld_tax_mxn + d.employer_imss_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.employer_assets_mxn, d.employer_retirement_mxn + d.employer_housing_mxn,
                               rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.compensation_mxn - d.total_tax_mxn,
                               d.gross_mxn - d.withheld_tax_mxn + d.employer_assets_mxn, rtol=0, atol=1e-7)
    np.testing.assert_allclose(d.ctax_mxn, d.gross_mxn * d.ctax_rate, rtol=0, atol=1e-7)


@pytest.mark.parametrize("young", [False, True])
def test_current_oct14_cash_and_employee_tax_positive_control(enigh, young):
    name = "mexico_young_by_parent.csv" if young else "mexico_earnings_cells.csv"
    baseline = pd.read_csv(io.StringIO(M.pinned_text(f"positive_control_{name}")))
    rates = M.ppp()
    if young:
        new = M.young_by_parent(enigh, rates)
        keys = ["sex", "band", "parent_cat"]
    else:
        new = M.cells(enigh)
        M.add_ppp(new, rates)
        keys = ["sex", "band", "cat"]
    old = baseline.set_index(keys).sort_index()
    new = new.set_index(keys).sort_index()
    assert old.index.equals(new.index)
    # Existing CSV precision is six significant digits; compare the serialized old
    # columns byte-for-byte after regenerating, not a newly relaxed numeric tolerance.
    columns = [c for c in old if c in new]
    numeric = [c for c in columns if pd.api.types.is_numeric_dtype(old[c])]
    text = new[numeric].to_csv(index=False, float_format="%.6g", lineterminator="\n")
    expected = old[numeric].to_csv(index=False, float_format="%.6g", lineterminator="\n")
    assert text == expected
    for ppp in ("gdp", "consumption"):
        assert f"compensation_per_person_ppp_{ppp}" in new
        assert f"total_tax_per_person_ppp_{ppp}" in new
        assert f"employer_per_person_ppp_{ppp}" in new


def test_unknown_receipt_component_and_class_fail_closed(monkeypatch):
    with pytest.raises(SystemExit, match="receipt_component_declared"):
        MC.receipt_rows({"unclassified": np.array([1.])})
    monkeypatch.setitem(MC.RECEIPTS, "income_tax", ("unclassified", "mexico_public", "worker", "test"))
    with pytest.raises(SystemExit, match="receipt_class_declared"):
        MC.receipt_rows({"income_tax": np.array([1.])})


def test_minimum_wage_employee_ceav_paid_by_employer_keeps_worker_owner():
    c = M.mx_employer_contributions(np.array([M.MW_YEAR, 5 * M.UMA_YEAR]))
    assert c["employer_employee_ceav"][0] > 0 and c["employer_employee_ceav"][1] == 0
    rows = MC.receipt_rows({"employee_ceav": np.array([1.]),
                            "employer_employee_ceav": np.array([1.]), "employer_ceav": np.array([1.])})
    assert {r["receipt_class"] for r in rows} == {"worker_asset"}
    assert {r["owner"] for r in rows} == {"worker"}
    assert not any(r["member_paid_tax"] for r in rows)


def test_partial_year_minimum_wage_branch_does_not_depend_on_quotient_rounding():
    # The former g/(g/MW_YEAR) sometimes landed one ulp above MW_YEAR and
    # removed the legally employer-paid employee quotas. An exact source-level
    # branch gives a continuous deposit proportional to exposure below the floor.
    g = np.linspace(1., M.MW_YEAR - 1., 10001)
    c = M.mx_employer_contributions(g)
    np.testing.assert_allclose(c["employer_employee_ceav"], g * M.AFORE_RATE, rtol=0, atol=1e-8)
    assert (c["employer_employee_health_cash"] > 0).all()


def test_government_quota_is_classified_but_never_member_tax():
    rows = MC.receipt_rows({"government_health_fixed": 10., "government_cuota_social": 5.})
    assert rows[0]["receipt_class"] == "pooled_public" and rows[1]["receipt_class"] == "worker_asset"
    assert not any(r["member_paid_tax"] for r in rows)


def test_ownership_switch_moves_only_tax_not_compensation():
    cash = np.array([1000., 50000., 100000.])
    new = MC.pay_arrays(M, cash, cash / 2, 10., 0.1)
    old = MC.pay_arrays(M, cash, cash / 2, 10., 0.1, assets_as_tax=True)
    np.testing.assert_array_equal(new["inc"], old["inc"])
    np.testing.assert_allclose(old["tax"] - new["tax"], new["assets"], rtol=0, atol=1e-7)


def test_g3_zero_uses_statutory_caps_and_total_compensation():
    p = pd.DataFrame(dict(ppp="gdp", ppp_divisor=10., pw=[1e6, 2e6, 1e6],
        us_cash=[1000., 200000., 400000.], formal_fraction=[0., 1., 1.],
        upper_cash=[500., 50000., 100000.], upper_formal=[0., 50000., 100000.],
        upper_ctax=[50., 5000., 10000.]))
    x = MC.zero_arrays(M, p, 20.)
    a = MC.aggregate(p, x)
    assert abs(a["inc"] - ((p.pw * p.us_cash).sum() / 1e9 + 20.)) < 1e-9
    assert abs(a["inc"] - a["cash"] - a["employer"]) < 1e-9
    # Both high pay cells exceed 25 UMA; retirement/housing/IMSS do not scale with US cash.
    assert abs(x["assets"][1] - x["assets"][2]) < 1e-7
    assert abs(x["employer"][1] - x["employer"][2]) < 1e-7
    assert x["tax"][2] > x["tax"][1]


def test_g3_upper_avoided_contributions_are_the_same_cells_as_compensation():
    p = pd.DataFrame(dict(ppp="consumption", ppp_divisor=10.8, pw=[1e6, 2e6],
        us_cash=[50000., 100000.], formal_fraction=[0.4, 0.6],
        upper_cash=[10000., 20000.], upper_formal=[4000., 12000.], upper_ctax=[1000., 2000.]))
    x = MC.upper_arrays(M, p)
    a = MC.aggregate(p, x)
    assert abs(a["inc"] - a["cash"] - a["employer"]) < 1e-9
    assert abs(a["tax"] - a["withheld"] - a["employer"] + a["assets"]) < 1e-9


def test_g3_zero_statutory_discontinuity_uses_same_two_cells():
    cash = 4 * M.UMA_YEAR / 10.
    low = MC.pay_arrays(M, np.array([cash]), np.array([cash]), 10., 0.1)
    high = MC.pay_arrays(M, np.array([cash + 1e-7]), np.array([cash + 1e-7]), 10., 0.1)
    target = (low["inc"][0] + high["inc"][0]) / 2
    assert high["inc"][0] > low["inc"][0] + 1.
    p = pd.DataFrame(dict(ppp="gdp", ppp_divisor=[10.], pw=[1e6],
        us_cash=[target], formal_fraction=[1.], upper_cash=[cash], upper_formal=[cash], upper_ctax=[cash * 0.1]))
    x = MC.zero_arrays(M, p, 0.)
    assert abs(x["inc"][0] - target) < 1e-7
    assert low["assets"][0] < x["assets"][0] < high["assets"][0]


def test_g3_legacy_isolation_copies_profiles_before_ownership_adjustment():
    p = pd.DataFrame(dict(ppp="gdp", ppp_divisor=[10.], pw=[1e6], us_cash=[50000.], formal_fraction=[1.],
        upper_inc=[25000.], upper_cash=[20000.], upper_formal=[20000.], upper_employer=[5000.],
        upper_tax=[4000.], upper_assets=[2000.], upper_withheld=[1000.], upper_net=[19000.], upper_ctax=[2000.]))
    before = p.copy(deep=True)
    x = MC.zero_arrays(M, p, 1., assets_as_tax=True, statutory=False)
    pd.testing.assert_frame_equal(p, before)
    assert abs(MC.aggregate(p, x)["inc"] - 51.) < 1e-9


@pytest.mark.parametrize("statutory", [False, True])
def test_state_payroll_tax_reenters_zero_compensation_solver(statutory):
    p = pd.DataFrame(dict(ppp="gdp", ppp_divisor=[10.], pw=[1e6], us_cash=[50000.], formal_fraction=[0.6],
        upper_inc=[25000.], upper_cash=[20000.], upper_formal=[12000.], upper_employer=[5000.],
        upper_tax=[4000.], upper_assets=[2000.], upper_withheld=[1000.], upper_net=[19000.], upper_ctax=[2000.]))
    x = MC.zero_arrays(M, p, 1., statutory=statutory, isn_rate=0.03)
    a = MC.aggregate(p, x)
    assert abs(a["inc"] - 51.) < 1e-9
    assert abs(a["inc"] - a["cash"] - a["employer"]) < 1e-9
    assert abs(a["isn"] - a["formal"] * 0.03) < 1e-9
    assert a["isn"] > 0
    # All public payroll taxes include ISN, with no extra worker-asset deposit.
    assert abs(a["tax"] - a["withheld"] - a["employer"] + a["assets"]) < 1e-9


def test_state_payroll_tax_is_pooled_and_excluded_from_assets():
    rows = MC.receipt_rows({"employer_state_payroll": np.array([100.])})
    assert rows[0]["receipt_class"] == "pooled_public" and rows[0]["owner"] == "mexico_public"
    a = MC.pay_arrays(M, np.array([50000.]), np.array([30000.]), 10., 0.1)
    b = MC.pay_arrays(M, np.array([50000.]), np.array([30000.]), 10., 0.1, isn_rate=0.03)
    np.testing.assert_array_equal(a["assets"], b["assets"])
    for k in ("inc", "tax", "employer"):
        np.testing.assert_allclose(b[k] - a[k], np.array([900.]), rtol=0, atol=1e-7)


def test_beside_health_reads_recipient_values_without_moving_fiscal_cost():
    import beside_arms as B
    import mexico_prices as MP
    rows = pd.DataFrame([dict(row=f"{kind}_{g}", party=g, low=0., central=0., high=0.)
                         for g in B.W.GENS for kind in ("mexico_budget_lost", "uncompensated_received")])
    raw = pd.DataFrame([dict(generation=g, cls=cls, bn=1., item=cls)
                        for g in B.W.GENS for cls in MP.BUDGET_CLASSES])
    budget = MP.budget_from_gdp(raw, 10.)
    health = budget.cls.eq('health')
    budget.loc[health, 'recipient_value_bn'] *= 0.25
    budget.loc[health, 'recipient_value_pesos_bn'] *= 0.25
    # The old alias deliberately lies: only the explicit recipient field is authoritative.
    budget['bn'] = 1000.
    before = budget.fiscal_cost_bn.copy()
    I = dict(health_vg=(0.2, 0.4, 0.6), mxb=budget,
             ch=pd.DataFrame([dict(item='unreimbursed_care', bn_low=0., bn_central=0., bn_high=0.)]).set_index('item'),
             ages=pd.DataFrame(dict(generation=B.W.GENS, persons=[1., 1., 1.])))
    out = B.health_rows(rows, I, 'average_cost').set_index('row')
    np.testing.assert_allclose(out.loc['mexico_budget_lost_G1', ['low', 'central', 'high']].to_numpy(float),
                               np.array([-2.15, -2.1, -2.05]), rtol=0, atol=1e-12)
    pd.testing.assert_series_equal(budget.fiscal_cost_bn, before)


@pytest.mark.parametrize("is_national,expected_formal", [(False, 40.), (True, 80.)])
def test_area_formal_pay_uses_observed_share_and_national_identity(monkeypatch, is_national, expected_formal):
    import beside_arms as B
    key = ('female', '15-19', 5)
    values = dict(inc=130., cash=100., employer=30., assets=20., formal=80., withheld=10.,
                  tax=20., ctax=10., net=90., emp=0.5, hrs=40.)
    nat = {pre + k: {key: v} for pre in ('', 'y') for k, v in values.items()}
    monkeypatch.setattr(B.G, 'mexico_cells', lambda ppp: nat)
    ratio = {f'R_{col}': 1. for col in B.MONEY.values()}
    ratio.update(R_emp=1., R_hrs=1., R_formal_gross=1. if is_national else 2.,
                 formal_cash_share=0.4, formal_cash_numerator_mxn=40., formal_cash_denominator_mxn=100.,
                 is_national=is_national)
    ratios = pd.DataFrame([dict(kind='adult', sex='female', key=5, **ratio),
                           dict(kind='young', sex='female', key='15-19', **ratio)])
    cells = B.area_cells('gdp', ratios, 1.)
    for pre in ('', 'y'):
        assert cells[pre + 'formal'][key] == expected_formal
        for unchanged in ('cash', 'employer', 'assets', 'withheld', 'tax', 'inc'):
            assert cells[pre + unchanged][key] == nat[pre + unchanged][key]


def test_area_ratio_metadata_is_raw_same_pool_fraction(enigh):
    import beside_arms as B
    rates = M.ppp()
    c = M.cells(enigh)
    M.add_ppp(c, rates)
    y = M.young_by_parent(enigh, rates)
    ratios = B.pay_ratios(enigh, lambda a: np.ones(len(a), bool), c, y)
    assert ratios.is_national.all()
    positive = ratios.formal_cash_denominator_mxn.gt(0)
    np.testing.assert_allclose(ratios.loc[positive, 'formal_cash_share'],
        ratios.loc[positive, 'formal_cash_numerator_mxn'] / ratios.loc[positive, 'formal_cash_denominator_mxn'],
        rtol=0, atol=1e-12)
    assert ratios.formal_cash_share.between(0, 1).all()
