"""Gates for beside_extra.py's outputs: theta follows from its parameters and the case's parts, matches mcpf's
theta_eff, and reproduces the world totals from each scenario's equal and lambda 1.16 columns; the same-person arms
move only G1's premium, to E_US (1 - 1/r); the readings are their arms' combinations; arm 5's table adds up to its
scenario; the private gain adds its terms; the summary's figures follow from the party totals; the tenure check adds up.

Run from the repository root (a worktree drops --no-project):
  uv run --no-project python3 -m pytest infra/immigration-fiscal/world_ledger_2026_09_27/test_beside_extra.py -q
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
MEMBERS = 42_752_213
PARTIES = ["others_today", "future_taxpayers", "G1", "G2", "G3+", "mexico_residents"]
GENS = ["G1", "G2", "G3+"]


@pytest.fixture(scope="module")
def meta():
    return json.load(open(D / "beside_extra_meta_oct07.json"))


@pytest.fixture(scope="module")
def summary():
    return pd.read_csv(D / "beside_extra_summary_oct07.csv")


@pytest.fixture(scope="module")
def eq(summary):
    return summary[summary.weighting == "equal"].set_index("scenario")


@pytest.fixture(scope="module")
def lane_columns():
    """Every scenario's equal and lambda 1.16 party totals: this file's and beside_arms.py's others."""
    x = pd.read_csv(D / "beside_extra_oct07.csv")
    a = pd.read_csv(D / "beside_arms_oct07.csv")
    a = a[~a.scenario.isin(set(x.scenario[x.weighting == "equal"]))]
    x = x[x.weighting.isin(["equal", "equal_lambda_1.16"])]
    return pd.concat([a, x], ignore_index=True).set_index(["scenario", "weighting", "party"]).bn


def test_theta_values(meta):
    a = meta["arm4"]
    p, b = a["parts_central_bn"], a["borrowed_share"]
    for name, s in a["sets"].items():
        m = sum(a["composition"][k] * a["mvpf_values"][s["mvpf"]][k] for k in a["composition"])
        v_sl = s["s"] * m + (1 - s["s"]) * s["lam"]
        v_b = s["lam"] + s["d"] * (s["spc"] - 1)
        v_ft = v_b if s["current_law"] else s["f"] * m + (1 - s["f"]) * s["lam"]
        sl = p["state_local"] + p["capital_return"] - p["capital_return_federal"]
        ft = (1 - b) * p["federal"] + p["capital_return_federal"]
        t = a["theta"][name]
        assert np.isclose(t["theta_o"], (v_sl * sl + v_ft * ft) / (sl + ft), atol=1e-12), name
        assert np.isclose(t["theta_f"], v_b, atol=1e-12), name
    assert 0.25 < b < 0.29
    assert np.isclose(a["theta"]["theta_education_5_extreme"]["mvpf"], 2.58, atol=1e-12)


def test_theta_matches_mcpf(meta):
    """mcpf's theta_eff at the band ends (the lead's note and mix_sens.py: 1.069 / 1.077 central)."""
    want = dict(theta_central=(1.069, 1.077), theta_alt_use=(0.984, 0.985), theta_waste=(0.944, 0.947),
                theta_education_2=(1.226, 1.240), theta_current_law=(1.082, 1.096),
                theta_waste_alt_use=(0.859, 0.855), theta_education_5_extreme=(1.793, 1.827))
    got = meta["arm4"]["mcpf_theta_eff_by_end"]
    for k, (lo, hi) in want.items():
        assert np.isclose(got[k]["low"], lo, atol=6e-4) and np.isclose(got[k]["high"], hi, atol=6e-4), (k, got[k])
    # This file's structure (displaced beneficiaries at $1, the capital return split by its federal part, the ledger's
    # midpoint) lands between mcpf's two ends.
    for k in want:
        t = meta["arm4"]["theta"][k]["theta_on_the_fiscal_cost"]
        lo, hi = sorted(got[k].values())
        assert lo - 6e-3 < t < hi + 6e-3, k


def test_capital_beside(meta):
    """The shadow price of capital and the R&D policy arm, beside and in no total: the lead's note's figures."""
    b = meta["arm4"]["beside"]
    for e, r in b["by_end"].items():
        assert np.isclose(r["spc_central_bn"], r["displaced_investment_bn"][1] * (b["spc"][1] - 1), atol=1e-9), e
        assert np.isclose(r["spc_range_bn"][1], r["displaced_investment_bn"][2] * (b["spc"][2] - 1), atol=1e-9), e
    lo, hi = b["by_end"]["low"], b["by_end"]["high"]
    assert round(lo["spc_central_bn"], 1) == 3.1 and round(hi["spc_central_bn"], 1) == 4.3
    assert np.isclose(lo["rd_policy_arm_bn"][0], 39.4, atol=0.05) and np.isclose(hi["rd_policy_arm_bn"][1], 263.5,
                                                                                    atol=0.05)


def test_theta_order(meta, summary):
    th = meta["arm4"]["theta"]
    w = summary[summary.scenario == "baseline"].set_index("weighting").world_total_bn
    same_f = sorted((k for k, v in th.items() if np.isclose(v["theta_f"], th["theta_central"]["theta_f"])),
                    key=lambda k: th[k]["theta_o"])
    assert list(w[same_f]) == sorted(w[same_f], reverse=True)
    assert w["theta_alt_use"] > w["theta_central"] and w["theta_waste_alt_use"] > w["theta_waste"]


def test_theta_from_lambda_columns(meta, summary, lane_columns):
    th = meta["arm4"]["theta"]
    p = lane_columns
    for r in summary[summary.weighting.str.startswith("theta_")].itertuples():
        t = th[r.weighting]
        world = 0.0
        for party in PARTIES:
            e = p[(r.scenario, "equal", party)]
            S = (p[(r.scenario, "equal_lambda_1.16", party)] - e) / 0.16
            k = {"others_today": "theta_o", "mexico_residents": "theta_o", "future_taxpayers": "theta_f"}.get(party)
            world += e + ((t[k] - 1) * S if k else 0.0)
        assert np.isclose(world, r.world_total_bn, atol=2e-5), (r.scenario, r.weighting)
        assert np.isclose(r.world_change_from_equal_bn, r.world_total_bn - p[(r.scenario, "equal", "world_total")],
                          atol=1e-5)


def test_summary_follows_from_party_totals(summary):
    x = pd.read_csv(D / "beside_extra_oct07.csv").set_index(["scenario", "weighting", "party"]).bn
    for r in summary.itertuples():
        g = lambda party: x[(r.scenario, r.weighting, party)]   # noqa: E731
        assert np.isclose(r.world_total_bn, g("world_total"), atol=1e-6)
        assert np.isclose(r.group_total_bn, sum(g(q) for q in GENS), atol=3e-6)
        assert np.isclose(r.us_residents_incl_group_bn, g("us_residents_total") + g("group_total"), atol=2e-6)
        assert np.isclose(r.group_per_member_usd, g("group_total") * 1e9 / MEMBERS, atol=0.05)
        assert np.isclose(r.breakeven_w, -(g("world_total") - g("group_total")) / g("group_total"), atol=1e-5)
        assert np.isclose(r.breakeven_w_us_only, -g("us_residents_total") / g("group_total"), atol=1e-5)


def test_arms_alone_are_beside_arms(eq):
    a = pd.read_csv(D / "beside_arms_summary_oct07.csv")
    a = a[a.weighting == "equal"].set_index("scenario")
    for k in ("baseline", "arm2_state_rpp", "arm3a", "arm3b"):
        for c in ("world_total_bn", "premium_bn", "us_budget_value_bn", "us_residents_incl_group_bn"):
            assert np.isclose(eq.loc[k, c], a.loc[k, c], atol=2e-6), (k, c)


def test_same_person_moves_only_g1(meta, eq):
    sp = meta["arm1"]["same_person"]
    e_us = sp["e_us_nominal_bn"]["own_schooling_all_ages"]
    base = eq.loc["baseline"]
    for name, d in sp["detail"].items():
        x = d["own_schooling_all_ages"]
        assert np.isclose(eq.loc[name, "premium_G1_bn"], e_us * (1 - 1 / x["r_annual"]), atol=1e-6), name
        assert np.isclose(eq.loc[name, "premium_G2_bn"], base.premium_G2_bn, atol=1e-9)
        assert np.isclose(eq.loc[name, "premium_G3plus_bn"], base.premium_G3plus_bn, atol=1e-9)
        # Mexico's taxes on the group are transfers, so at equal weights the world moves by the premium alone.
        assert np.isclose(eq.loc[name, "world_change_bn"], eq.loc[name, "premium_bn"] - base.premium_bn, atol=1e-5)
        s = sp["sets"][name]
        want = s["r"] / x["hours_employment_mx_over_us"] if s["per_hour"] else s["r"]
        assert np.isclose(x["r_annual"], want, atol=1e-12), name
    # The lead's per-person conversions, 2.0 x (38.7 / 46.4) x (67.2 / 70.5) and the same for 1.8.
    assert round(sp["detail"]["arm1c_mmp_per_person"]["own_schooling_all_ages"]["r_annual"], 2) == 1.59
    assert round(sp["detail"]["arm1c_nis_per_person"]["own_schooling_all_ages"]["r_annual"], 2) == 1.43


def test_readings_are_their_arms(meta, eq):
    det = meta["scenario_detail"]
    r = meta["arm1"]["same_person"]["detail"]["arm1c_mmp_per_person"]["own_schooling_all_ages"]
    e_nom = meta["arm1"]["same_person"]["e_us_nominal_bn"]["own_schooling_all_ages"]
    # Reading 3: reading 1 with G1's Mexican pay at the nominal E_US / r; arm 2's E_US.
    assert np.isclose(det["reading3"]["e_mx_central_bn"]["G1"], e_nom / r["r_annual"], atol=1e-9)
    assert np.isclose(det["reading3"]["e_us_bn"]["G1"], det["arm2_state_rpp"]["e_us_bn"]["G1"], atol=1e-12)
    assert np.isclose(eq.loc["reading3", "premium_G2_bn"], eq.loc["reading1", "premium_G2_bn"], atol=1e-9)
    # The combined low: reading 3's G1 and reading 2's G2 and services.
    assert np.isclose(eq.loc["combined_low", "premium_G1_bn"], eq.loc["reading3", "premium_G1_bn"], atol=1e-9)
    assert np.isclose(eq.loc["combined_low", "premium_G2_bn"], eq.loc["reading2", "premium_G2_bn"], atol=1e-9)
    for k in ("reading2_consumption", "combined_low", "combined_low_consumption"):
        assert np.isclose(eq.loc[k, "us_budget_value_bn"], eq.loc["reading2", "us_budget_value_bn"], atol=1e-9)
    # Arm 3's US-price numeraire moves Mexico's rows only: the US budget as valued is the central's.
    for k in ("arm3_us_numeraire", "arm3_us_numeraire_group_only", "reading1", "reading3"):
        assert np.isclose(eq.loc[k, "us_budget_value_bn"], eq.loc["baseline", "us_budget_value_bn"], atol=1e-9)
    # Its group-only check leaves Mexico's residents at the central's; the symmetric arm does not.
    assert np.isclose(eq.loc["arm3_us_numeraire_group_only", "mexico_residents_bn"],
                      eq.loc["baseline", "mexico_residents_bn"], atol=1e-6)
    assert eq.loc["arm3_us_numeraire", "mexico_residents_bn"] > eq.loc["baseline", "mexico_residents_bn"]
    assert np.isclose(eq.loc["arm3_us_numeraire", "group_total_bn"],
                      eq.loc["arm3_us_numeraire_group_only", "group_total_bn"], atol=1e-6)
    # Reading 1 at equal weights adds its arms' changes up to their small interaction.
    parts = sum(eq.loc[k, "world_change_bn"] for k in ("arm1a_urban_consumption", "arm2_state_rpp",
                                                       "arm3_us_numeraire"))
    assert abs(eq.loc["reading1", "world_change_bn"] - parts) < 1.0


def test_arm5_table(meta, eq):
    t = pd.read_csv(D / "beside_extra_industry_oct07.csv")
    F = meta["arm5"]["F"]
    for g in ("G1", "G2"):
        x = t[t.generation == g]
        assert np.isclose(x.e_us_share.sum(), 1.0, atol=1e-6)
        assert np.isclose((x.e_us_share / x.ppp_over_gdp_ppp).sum(), F[g]["services"], atol=1e-6)
        assert np.isclose((x.e_us_share / x.ppp_over_gdp_ppp_goods_too).sum(), F[g]["goods_too"], atol=1e-6)
        assert np.isclose(x.price_not_output_bn.sum(), x.premium_gdp_ppp_bn.sum() - x.premium_category_bn.sum(),
                          atol=1e-5)
        col = "premium_G1_bn" if g == "G1" else "premium_G2_bn"
        assert np.isclose(x.premium_gdp_ppp_bn.sum(), eq.loc["baseline", col], atol=2e-3)
        assert np.isclose(x.premium_category_bn.sum(), eq.loc["arm5_output_prices", col], atol=2e-3)
        assert np.isclose(x.premium_category_goods_too_bn.sum(), eq.loc["arm5_output_prices_goods_too", col], atol=2e-3)
        goods = x.cls.isin(["agriculture", "mining", "construction", "manufacturing"])
        assert np.isclose(1 - x.e_us_share[goods].sum(), meta["arm5"]["service_share_of_e_us"][g], atol=1e-6)
    assert all(v < 0.01 for v in meta["arm5"]["off_list_earnings_share"].values())


def test_private_gain_adds_up(meta, eq):
    p = pd.read_csv(D / "beside_extra_private_gain_oct07.csv")
    inp = meta["private_gain"]["inputs"]
    for r in p.itertuples():
        a = r.premium_bn + r.us_taxes_bn + r.mexico_taxes_avoided_bn + r.mexico_services_forgone_bn
        assert np.isclose(r.wages_only_bn, a, atol=1e-5), r.scenario
        assert np.isclose(r.with_old_age_accrual_bn, a + r.social_security_accrual_bn + r.part_a_accrual_bn, atol=1e-5)
        assert np.isclose(r.wages_only_per_member_usd, r.wages_only_bn * 1e9 / r.persons, atol=0.05)
        if r.generation == "G1":
            assert np.isclose(r.wages_only_per_g1_adult_usd, r.wages_only_bn * 1e9 / meta["private_gain"]["g1_adults"],
                              atol=0.05)
        if r.generation in GENS:
            x = inp[r.generation]
            assert np.isclose(r.us_taxes_bn, x["us_taxes_bn"], atol=1e-6) and x["us_taxes_bn"] < 0
            assert np.isclose(r.part_a_accrual_bn, x["part_a_per_hi_tax_dollar"] * x["hi_taxes_bn"], atol=1e-6)
            col = {"G1": "premium_G1_bn", "G2": "premium_G2_bn", "G3+": "premium_G3plus_bn"}[r.generation]
            assert np.isclose(r.premium_bn, eq.loc[r.from_scenario, col], atol=2e-6), r.scenario
    g = p.groupby(["scenario", p.generation.eq("group")]).wages_only_bn.sum().unstack()
    assert np.allclose(g[True], g[False], atol=1e-5)
    assert np.isclose(p[p.generation == "group"].persons, MEMBERS, atol=1.0).all()
    assert not p.scenario.str.startswith("arm5_").any()


def test_staged_sources_pinned(meta):
    repo = HERE.parents[2]
    paths = {k: repo / s["path"] for k, s in meta["sources"].items()}
    if not all(p.is_file() for p in paths.values()):
        pytest.skip("staged sources absent (acquire_beside.py)")
    for k, p in paths.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == meta["sources"][k]["sha256"], k
    manifest = pd.read_csv(D / "beside_sources.csv")
    assert set(manifest.sha256) == {s["sha256"] for s in meta["sources"].values()}
    assert {"icp2021_categories", "census_industry_2022"} <= set(meta["sources"])


def test_tenure_check(meta):
    t = meta["tenure_check"]
    bins = [k for k in t if k.startswith("arrived_")]
    assert len(bins) == 4 and sum(t[k]["records"] for k in bins) == t["all"]["records"]
    for k, v in t.items():
        if k == "hs_mmp_2024usd":
            continue
        assert np.isclose(v["ratio_per_hour"], v["us_pay_per_hour_2024usd"] / v["mexico_pay_per_hour_ppp"], rtol=1e-9)
    assert np.isclose(t["hs_mmp_2024usd"]["post"], 6.04 * 313.698 / 184.0)
