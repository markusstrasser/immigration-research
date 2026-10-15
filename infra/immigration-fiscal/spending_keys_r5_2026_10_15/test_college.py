"""Accounting/scope gates for the item-15 bridge, not a causal-response test."""

import importlib.util
import json
from pathlib import Path

import pytest
import pandas as pd

SPEC = importlib.util.spec_from_file_location("item15_college", Path(__file__).with_name("college.py"))
college = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(college)


@pytest.fixture(scope="module")
def item():
    return college.build_item()


def test_primary_totals_and_function_closure(item):
    totals = item["measured_totals_bn"]
    assert item["finance_units"] == 1888
    assert sum(totals[k] for k in college.FUNCTIONS) == pytest.approx(totals["total_expenses"], abs=1e-9)
    assert totals["public_service"] == pytest.approx(20.128745339, abs=1e-9)
    assert item["national_exposure_bn"] == pytest.approx(234.029706937839, abs=1e-9)


def test_central_net_bridge_closes_and_preserves_tuition(item):
    bridge = item["bridge"]
    totals = item["measured_totals_bn"]
    sales = bridge["tuition_sales_bn"] + totals["education_activity_sales"] + totals["auxiliary_sales"]
    assert bridge["gross_in_scope_bn"] - sales == pytest.approx(bridge["ipeds_net_bn"], abs=1e-9)
    assert bridge["responsive_net_bn"] + bridge["invariant_net_bn"] == pytest.approx(bridge["ipeds_net_bn"], abs=1e-9)
    assert bridge["invariant_net_bn"] == pytest.approx(totals["public_service"], abs=1e-9)
    assert item["apply_to"]["tuition_response"] == 1
    # Distinct use and fee keys: only the use cost changes, not lost tuition.
    n, t, u, fee_share = 234.0, 104.0, 0.116, 0.098
    before = u * (n + t) - fee_share * t
    after = before + (item["central_response"] - 1) * u * n
    assert after - before == pytest.approx((item["central_response"] - 1) * u * n)
    assert after - before != pytest.approx((item["central_response"] - 1) * before)


def test_research_and_hospital_expense_do_not_reduce_central_consumption(item):
    values = item["measured_totals_bn"].copy()
    original = college.bridge(values)
    values["research"] *= 2
    values["hospitals"] *= 2
    values["hospital_sales"] *= 3
    assert college.bridge(values) == original


def test_arms_name_assumptions_and_bound_response(item):
    arms = item["arms"]
    assert arms["public_service_outside_education"]["response"] == pytest.approx(1)
    assert arms["unclassified_other_fixed"]["response"] < item["central_response"]
    assert arms["education_sales_public_service"]["response"] > item["central_response"]
    for arm in arms.values():
        assert 0 <= arm["response"] <= 1
        assert arm["national_delta_bn"] == pytest.approx((arm["response"] - 1) * item["national_exposure_bn"])
    assert item["capital_response"] == item["central_response"]
    assert 0 < item["capital_expense_mix_arm"]["response"] < 1
    json.dumps(item, allow_nan=False)


def test_unknown_tuition_convention_fails_loud(item):
    with pytest.raises(ValueError, match="BLOCKED.*tuition"):
        college.bridge(item["measured_totals_bn"], tuition_basis="unknown")


def test_only_primary_not_applicable_flag_permits_zero():
    source = pd.DataFrame({"amount": [float("nan"), 2.0], "Xamount": ["A", "R"]})
    numeric, counts = college.finance_numeric(source, {"amount"})
    assert numeric.amount.tolist() == [0.0, 2.0]
    assert counts == {"amount": 1}
    for bad in ["B", "D", "H", "R"]:
        source.loc[0, "Xamount"] = bad
        with pytest.raises(ValueError, match="BLOCKED.*missing applicable"):
            college.finance_numeric(source, {"amount"})
