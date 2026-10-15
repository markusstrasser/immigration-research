"""Meaningful guards for the explicitly partial item-14 accounting bridge."""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("item14", Path(__file__).with_name("income_security.py"))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def test_complete_measurement_blocks_before_loading_sources():
    with pytest.raises(ValueError, match=r"\[BLOCKED\].*no measured program-complete"):
        M.build_item(require_complete=True)


def test_bea_budget_closure_and_retirement_investment_bounds():
    bea = M.bea_measurements()
    mass = bea["consumption_bn"]
    assert mass["total"] - mass["federal"] - mass["state_local"] == pytest.approx(.001)
    gross = bea["consumption_plus_gross_investment_bn"]
    assert sum(gross["federal"].values()) == pytest.approx(34.659)
    assert sum(gross["state_local"].values()) == pytest.approx(141.042)
    assert bea["gross_investment_bn"]["federal"] == pytest.approx(4.123)
    assert 0 < gross["federal"]["retirement"] < bea["gross_investment_bn"]["federal"]


def test_only_retirement_changes_in_partial_arm():
    bea = M.bea_measurements()
    keys = {a: {k: {"share": s, "ratio_to_current_cash_assistance": s / .2}
                for k, s in [("cash_assistance", .2), ("social_security", .05),
                             ("population", .12), ("ssi", .08), ("snap", .16),
                             ("medicaid_covered", .19), ("unemployment", .13), ("workers_comp", .14)]}
            for a in ["personal", "shared"]}
    arms = M.conditional_keys(bea, keys)
    for allocation in ["personal", "shared"]:
        assert arms["retirement_all_investment"]["by_allocation"][allocation]["share_ratio"] == pytest.approx(1)
        mid = arms["partial_retirement_proportional_investment"]["by_allocation"][allocation]
        low = arms["retirement_no_investment"]["by_allocation"][allocation]
        assert low["effective_share"] < mid["effective_share"] < .2
        fraction = arms["partial_retirement_proportional_investment"]["retirement_consumption_bn"] / 167.818
        assert mid["effective_share"] == pytest.approx((1 - fraction) * .2 + fraction * .05)


def test_cms_financing_shares_are_not_independent_program_masses():
    evidence = M.agency_evidence()
    total, federal, state = evidence["medicaid"]["national_row_dollars"]
    assert total == federal + state
    assert evidence["medicaid"]["calculation_use"] == "BESIDE_ONLY"
