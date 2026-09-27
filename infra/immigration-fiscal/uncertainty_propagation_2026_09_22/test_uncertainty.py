"""Checks for the uncertainty-propagation lane. Run propagate.py and audit.py first."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FA = HERE.parent / "full_account_2026_09_20/derived"


def _load(name):
    spec = importlib.util.spec_from_file_location(f"upl_{name}", HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = _load("audit")


def test_sdr_formula_matches_census_successive_difference():
    rng = np.random.default_rng(0)
    v = rng.normal(size=161)
    assert audit.sdr(v) == pytest.approx(np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()))


def test_ledger_base_se_reproduces_published_7_473981():
    base = audit.ledger_endpoint(["base"])
    assert base[0] == pytest.approx(50.238214, abs=1e-6)
    assert audit.sdr(base) == pytest.approx(7.473981, abs=1e-6)


def test_ledger_live_endpoint_se_reproduces_waterfall():
    check = audit.ledger_check().set_index("quantity")
    live = check.loc["live union complete endpoint (D,P on; E zero)"]
    assert live.rebuilt_bn == pytest.approx(live.published_bn, abs=1e-6)
    assert live.rebuilt_se_bn == pytest.approx(live.published_se_bn, abs=1e-6)
    assert live.published_se_bn == pytest.approx(8.700282, abs=1e-6)


def test_stale_8_81_is_a_superseded_vintage_not_reproducible_from_live_replicates():
    """The $8.81bn SE belongs to the Sept 17 build (-253.93bn). replicates.npz was rewritten by
    the Sept 18-19 rebuilds, so the same arm composition now gives a different point and SE.
    This test pins that fact so nobody quotes 8.81 as a live number."""
    stale = audit.ledger_check().set_index("quantity").loc[
        "Sept 17 union endpoint (stale vintage; D,P off; E stock; S half)"]
    assert abs(stale.rebuilt_bn - (-253.93)) > 1.0
    assert abs(stale.rebuilt_se_bn - 8.81) > 0.05


def test_replicate0_keys_equal_both_producers_and_receipt_ses_match():
    k = pd.read_csv(OUT / "key_replicate_check.csv").dropna(subset=["share_rebuilt"])
    assert len(k) >= 80
    np.testing.assert_allclose(k.share_rebuilt, k.share_published, rtol=1e-9, atol=0)
    r = k.dropna(subset=["se_published"])
    assert len(r) == 30
    np.testing.assert_allclose(r.se_rebuilt, r.se_published, rtol=1e-6, atol=0)


def test_every_published_headline_case_recomputed_within_0_1bn():
    table, _ = audit.formula_audit()
    assert set(table.object) == {"service_response_case", "headline_cases", "headline_summary"}
    assert (table.object == "service_response_case").sum() == 60
    assert (table.object == "headline_cases").sum() == 4
    assert table.abs_diff_bn.max() < 0.1
    assert table.abs_diff_bn.max() < 1e-9  # in fact exact to rounding


def test_published_headline_bands_are_the_recomputed_extremes():
    _, mine = audit.formula_audit()
    net = -mine.set_index("profile").welfare_bn
    assert net.loc["cbo_category_lag_non_school_full"].min() == pytest.approx(165.12, abs=0.01)
    assert net.loc["cbo_category_lag_non_school_full"].max() == pytest.approx(197.38, abs=0.01)
    assert net.loc["cbo_category_lag_non_school_fixed"].min() == pytest.approx(120.79, abs=0.01)
    assert net.loc["cbo_category_lag_non_school_fixed"].max() == pytest.approx(160.31, abs=0.01)
    assert net.loc["proportional_reference"].min() == pytest.approx(269.81, abs=0.01)
    assert net.loc["proportional_reference"].max() == pytest.approx(288.72, abs=0.01)


def test_propagated_point_equals_published_case():
    u = pd.read_csv(OUT / "case_uncertainty.csv")
    p = pd.read_csv(FA / "service_response_cases.csv")
    m = u.merge(p, on=["case_id", "normalization"])
    assert len(m) == 60
    np.testing.assert_allclose(m.net_cost_bn, -m.welfare_bn, atol=1e-9)
    assert (u.se_combined_independent_bn >= u.se_cps_fiscal_keys_bn).all()
    assert (u.se_all_positive_correlation_bn >= u.se_combined_independent_bn).all()


def test_meps_payer_covariance_reproduces_donor_model():
    prop = _load("propagate")
    d = prop.load_cps()
    md, cells, _, cov_public, _ = prop.meps_inputs(d)
    mine = prop.payer_covariance(md, cells, {"all": ["TOTMCR24", "TOTMCD24", "TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]})
    np.testing.assert_allclose(mine, cov_public, rtol=1e-10, atol=0)


def test_epsilon_rows_are_sensitivity_only():
    eps = pd.read_csv(OUT / "epsilon_cases.csv")
    inf = eps.loc[np.isinf(eps.epsilon)]
    np.testing.assert_allclose(inf.change_vs_headline_bn, 0, atol=1e-9)
    nest = pd.read_csv(HERE.parent / "production_nativity_nest_2026_09_22/derived/nest_headline.csv").query(
        "nest_option == 'A_by_nativity'")
    for e in [5.0, 7.0]:
        for norm in ["gdp", "cash"]:
            delta = nest.query("sigma_NI == @e and normalization == @norm").delta_vs_perfect_substitution_bn.iloc[0]
            rows = eps.query("epsilon == @e and normalization == @norm")
            np.testing.assert_allclose(rows.change_vs_headline_bn, -delta, atol=1e-6)
    # Headline outputs of the full account are untouched by this lane.
    assert json.loads((FA / "headline_summary.json").read_text())["category_service_response_sensitivity"][
        "cbo_category_lag_non_school_full"]["max_welfare_bn"] == pytest.approx(-165.12, abs=0.01)


@pytest.mark.parametrize("name, lane", json.loads((HERE / "later_cases.json").read_text()).items())
def test_later_cases_span_the_adopted_bands_at_the_payload_responses(name, lane):
    u = pd.read_csv(OUT / name / "case_uncertainty.csv")
    main = json.loads((HERE.parent / lane / "derived/summary.json").read_text())
    for case, band in ((name, main["main_case"]),
                       ("uncorrected_at_adopted_responses", main["uncorrected_at_adopted_responses"])):
        c = u[u.case == case]
        assert len(c) == 64
        np.testing.assert_allclose([c.net_cost_bn.min(), c.net_cost_bn.max()], band, atol=1e-6)
        assert (c.se_combined_independent_bn >= c.se_cps_fiscal_keys_bn).all()
        assert (c.se_all_positive_correlation_bn >= c.se_combined_independent_bn).all()
    gg, school = main["responses"]["general_government"], main["responses"]["school"]
    assert set(u.general_government_response) == {gg["low"], gg["high"]}
    assert set(u.school_response) == {school["growth"], school["decline"]}


def test_capital_case_carries_the_return_on_public_capital():
    """sept27: each specification's capital return is the case lane's (per_spec.csv, the methods' mean), the
    education derivatives give the K-12 and college returns, and the return's CPS part is positive."""
    found = 0
    for name, lane in json.loads((HERE / "later_cases.json").read_text()).items():
        u = pd.read_csv(OUT / name / "case_uncertainty.csv")
        if "capital_return_bn" not in u.columns:
            continue
        found += 1
        per = pd.read_csv(HERE.parent / lane / "derived/per_spec.csv").groupby("spec")[
            ["cost_bn", "capital_total_bn", "capital_k12_bn", "capital_college_bn"]].mean()
        c = u[u.case == name].reset_index(drop=True)
        np.testing.assert_allclose(c.net_cost_bn, per.cost_bn, atol=1e-9)
        np.testing.assert_allclose(c.capital_return_bn, per.capital_total_bn, atol=1e-9)
        np.testing.assert_allclose(c.capital_return_education_bn, per.capital_k12_bn + per.capital_college_bn, atol=1e-9)
        assert (c.se_cps_capital_part_bn > 0).all() and (c.se_cps_rental_and_enterprise_part_bn > 0).all()
    assert found >= 1


def test_joint_case_carries_the_benefit_keys_in_the_cps_block():
    """sept27 on (conceptual audit 2026-09-27, section A): the benefit keys' re-keying varies on the account's CPS
    replicates. The primary CPS error is the joint one and the combined error uses it; the published append
    (package_se.csv beside the account's combined error) stays beside it; the uncorrected frame has no benefit term."""
    found = 0
    for name in json.loads((HERE / "later_cases.json").read_text()):
        u = pd.read_csv(OUT / name / "case_uncertainty.csv")
        if "se_cps_account_keys_bn" not in u.columns:
            continue
        found += 1
        other = u.se_production_term_bn ** 2 + u.se_school_correction_bn ** 2 + u.se_meps_donor_bn ** 2
        np.testing.assert_allclose(u.se_combined_independent_bn, np.sqrt(u.se_cps_fiscal_keys_bn ** 2 + other), atol=1e-9)
        np.testing.assert_allclose(u.se_with_benefit_keys_bn,
                                   np.sqrt(u.se_cps_account_keys_bn ** 2 + other + u.se_benefit_keys_package_bn ** 2), atol=1e-9)
        c, base = u[u.case == name], u[u.case != name]
        acc, ben = c.se_cps_account_keys_bn, c.se_benefit_keys_replicate_bn
        np.testing.assert_allclose(c.se_cps_fiscal_keys_bn ** 2, acc ** 2 + ben ** 2 + 2 * c.corr_cps_benefit_keys * acc * ben,
                                   atol=1e-9)
        assert (c.corr_cps_benefit_keys < 0).all() and (c.se_cps_fiscal_keys_bn < c.se_cps_independent_append_bn).all()
        np.testing.assert_allclose(c.se_cps_factor_product_bn, c.se_cps_fiscal_keys_bn, atol=0.01)
        assert (base.se_benefit_keys_replicate_bn == 0).all()
        np.testing.assert_array_equal(base.se_cps_fiscal_keys_bn, base.se_cps_account_keys_bn)
        f = pd.read_csv(OUT / name / "benefit_factors.csv")
        np.testing.assert_allclose(f.shift_bn, f.delta_bn * f.stack_factor, rtol=1e-12)
    assert found >= 1
