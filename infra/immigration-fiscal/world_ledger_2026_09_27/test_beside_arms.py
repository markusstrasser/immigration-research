"""Gates for beside_arms.py's outputs: the baseline and arm 3(b) are the world ledger's own central and response_only
central, the summary's figures follow from the party totals, the arms add up at equal weights, the staged sources
carry their pinned hashes, and the price levels, ratios and parameters sit where the RESULT says.

Run from the repository root (a worktree drops --no-project):
  uv run --no-project python3 -m pytest infra/immigration-fiscal/world_ledger_2026_09_27/test_beside_arms.py -q
Without the staged sources (acquire_beside.py fetches them) the hash test skips.
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
CENTRAL = dict(mexico_taxes="withheld_consumption", scenario="central_g3_zero")


@pytest.fixture(scope="module")
def long():
    return pd.read_csv(D / "beside_arms_oct07.csv")


@pytest.fixture(scope="module")
def summary():
    return pd.read_csv(D / "beside_arms_summary_oct07.csv")


@pytest.fixture(scope="module")
def meta():
    return json.load(open(D / "beside_arms_meta_oct07.json"))


def ledger(pgc):
    w = pd.read_csv(D / "world_ledger_oct07.csv")
    w = w[(w.pg_convention == pgc) & (w.mexico_taxes == CENTRAL["mexico_taxes"]) & (w.scenario == CENTRAL["scenario"])]
    return w.set_index(["weighting", "party"]).bn


@pytest.mark.parametrize("scenario,pgc", [("baseline", "average_cost"), ("arm3b", "response_only")])
def test_lane_central_reproduced(long, scenario, pgc):
    mine = long[long.scenario == scenario].set_index(["weighting", "party"]).bn
    ref = ledger(pgc)
    assert len(mine) == len(ref) == 96
    assert np.allclose(mine.reindex(ref.index), ref, atol=1e-6, equal_nan=True)


def test_every_scenario_complete(long, summary):
    per = long.groupby("scenario").size()
    assert (per == 96).all(), per[per != 96]
    assert set(summary.scenario) == set(per.index)
    assert (summary.groupby("scenario").size() == 3).all()


def test_summary_follows_from_party_totals(long, summary):
    p = long.set_index(["scenario", "weighting", "party"]).bn
    for r in summary.itertuples():
        g = lambda party: p[(r.scenario, r.weighting, party)]
        assert np.isclose(r.world_total_bn, g("world_total"), atol=1e-6)
        assert np.isclose(r.group_total_bn, g("group_total"), atol=1e-6)
        assert np.isclose(r.us_residents_incl_group_bn, g("us_residents_total") + g("group_total"), atol=2e-6)
        assert np.isclose(r.group_per_member_usd, g("group_total") * 1e9 / MEMBERS, atol=0.05)
        assert np.isclose(r.breakeven_w, -(g("world_total") - g("group_total")) / g("group_total"), atol=1e-5)
        assert np.isclose(r.breakeven_w_us_only, -g("us_residents_total") / g("group_total"), atol=1e-5)


def test_arms_add_at_equal_weights(summary):
    # The arms touch different rows (US earnings, Mexico pay, the valuation lines); the Mexican-tax rows they share
    # are transfers between the group and Mexico's residents, so at equal weights the changes add exactly.
    eq = summary[summary.weighting == "equal"].set_index("scenario").world_change_bn
    assert np.isclose(eq["combined"], eq["arm1_metros"] + eq["arm2_state_rpp"] + eq["arm3"], atol=1e-5)
    assert np.isclose(eq["arm3"], eq["arm3a"] + eq["arm3b"], atol=1e-5)
    assert np.isclose(eq["combined_cdmx"], eq["arm1_cdmx"] + eq["arm2_state_rpp"] + eq["arm3"], atol=1e-5)
    assert np.isclose(eq["combined_icp"], eq["arm1_metros"] + eq["arm2_state_rpp"] + eq["arm3_icp"], atol=1e-5)


def test_directions(summary):
    eq = summary[summary.weighting == "equal"].set_index("scenario")
    base = eq.loc["baseline"]
    # Dividing metro pay by the metro price level lowers Mexico's pay, so the premium rises against the nominal run.
    assert eq.loc["arm1_metros", "premium_bn"] > eq.loc["arm1_metros_nominal", "premium_bn"]
    # US earnings at national prices, with the group above the national price level: a smaller premium.
    assert eq.loc["arm2_state_rpp", "premium_bn"] < base.premium_bn
    # Arms 2 and 3 leave Mexico's pay alone; arm 1 and arm 3 leave US earnings alone.
    assert np.isclose(eq.loc["arm3", "premium_bn"], base.premium_bn, atol=1e-9)
    assert np.isclose(eq.loc["arm1_metros", "us_budget_value_bn"], base.us_budget_value_bn, atol=1e-9)
    # FHL's WTP sits below the ICP price ratio, so 3(c) values the budget below 3(a) + 3(b).
    assert eq.loc["arm3c_fhl", "us_budget_value_bn"] < eq.loc["arm3", "us_budget_value_bn"]
    assert (eq.loc["arm3c_fhl_low", "us_budget_value_bn"] < eq.loc["arm3c_fhl", "us_budget_value_bn"]
            < eq.loc["arm3c_fhl_high", "us_budget_value_bn"])


def test_parameters(meta):
    icp = meta["icp2021"]
    assert np.isclose(icp["r_health"], icp["ppp_actual_health"] / icp["ppp_gdp"])
    assert np.isclose(icp["r_social"], icp["ppp_individual_government"] / icp["ppp_gdp"])
    assert 0.80 < icp["r_health"] < 0.82 and 0.39 < icp["r_social"] < 0.40
    assert np.allclose(meta["fhl_wtp_per_dollar"], [793 / 3600, 1421 / 3600, 1675 / 3600])
    pr = meta["prices"]
    v = pr["variants"]
    assert 0.15 < pr["housing_share_national"] < 0.25
    assert 1.0 < v["metros"]["price_level"] < v["cdmx"]["price_level"] < 1.2
    for k in v:
        assert np.isclose(v[k]["price_level"], 1 + pr["housing_share_national"] * (v[k]["rent_index"] - 1))
    assert 1.0 < pr["coneval_urban_over_national"] < 1.1
    for g, r in meta["rpp_by_generation"].items():
        assert 100 < r["persons"] < 106, g


def test_ratios_file():
    r = pd.read_csv(D / "beside_arms_ratios.csv")
    assert (r.n_used >= 100).all()
    assert (r[["R_gross", "R_income", "R_ctax"]] > 0).all().all()
    assert set(r.variant) == {"metros", "cdmx", "guadalajara", "monterrey", "large_localities"}
    assert (r.groupby("variant").size() == 2 * 6 + 2 * 2).all()


def test_staged_sources_pinned(meta):
    repo = HERE.parents[2]
    paths = {k: repo / s["path"] for k, s in meta["sources"].items()}
    if not all(p.is_file() for p in paths.values()):
        pytest.skip("staged sources absent (acquire_beside.py)")
    for k, p in paths.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == meta["sources"][k]["sha256"], k
    # The manifest also lists beside_extra.py's sources (its test checks them).
    manifest = pd.read_csv(D / "beside_sources.csv")
    assert {s["sha256"] for s in meta["sources"].values()} <= set(manifest.sha256)
