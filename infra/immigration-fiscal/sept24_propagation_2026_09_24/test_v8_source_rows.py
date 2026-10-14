"""P7 row replacement must not double-remove recipients or add beside arms."""
import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("v8_totals", HERE / "real_costs_totals.py")
totals = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(totals)


def test_blocked_stock_caller_reaches_financing_gate_and_restores_imports(monkeypatch, tmp_path):
    spec = importlib.util.spec_from_file_location("constant_choices_test", HERE / "constant_choices.py")
    choices = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(choices)
    debt = tmp_path/"debt"
    debt.mkdir()
    (debt/"dependency.py").write_text("VALUE=1\n")
    (debt/"debt_legacy.py").write_text(
        "import sys\ndef constant_parts(*args): return []\n"
        "def main():\n import dependency\n"
        " if sys.modules[__name__] is None: raise RuntimeError('missing module')\n"
        " raise SystemExit('[BLOCKED] missing financing timing')\n")
    monkeypatch.setattr(choices, "LANE", debt)
    original_path = sys.path[:]
    with pytest.raises(SystemExit, match="missing financing timing"):
        choices.debt_run("oct15", tmp_path/"out")
    assert sys.path == original_path
    assert "debt_legacy_choice" not in sys.modules
    sys.modules.pop("dependency", None)


def frozen_rows():
    doc = json.loads((HERE / "derived/oct14/real_costs_totals.json").read_text())
    with (HERE / "derived/oct14/real_costs_totals.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("sept23", "sept24", "oct14", "change"):
            row[key] = float(row[key]) if row[key] else None
        row["oct15"] = row.pop("oct14")
    doc["per_member_population_m"]["oct15"] = 45.0
    doc["without_round1_social_fixes_bn"] = {end: next(r["oct15"] for r in rows
        if r["column"] == "pairing_on_priced_count" and r["item"] == f"published pairing ({end})")
        for end in ("low", "high")}
    return rows, doc


def funding_meta():
    case = json.loads((HERE.parent / "social_respending_2026_10_14/derived/case_inputs.json").read_text())
    ends = {}
    for r in case["rows"]:
        if r["population_basis"] == "lineage":
            ends[r["end"]] = dict(accounting_basis="national_accounts",current_H_bn=r["current_budget_saving_bn"],
                capital_return_bn=r["capital_return_bn"],net_accrual_timing_bridge_bn=75.0,
                private_wtp_bn=r["private_wtp_bn"],cash_cost_bn=r["cash_set_cost_bn"],set_cost_bn=r["cash_set_cost_bn"]+75.0)
    return {"social_resource_account": {"ends": ends}}


def test_environment_replaces_boundary_adjusted_rows_once_and_keeps_mirror_beside():
    rows, doc = frozen_rows()
    before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                       and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    cash_before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count_cash_set"
                            and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    totals.apply_v8_environment(rows, doc, funding_meta(), {"v8": {"population": {"with_coverage": 45e6}}}, "fixed_v7_source_keys")
    detail = doc["lineage_social_rows"]["rows"]
    for end in ("low", "high"):
        parts = doc["v8_social_environment"]["variants"]["central"]["parts"][end]
        source = next(r for r in csv.DictReader((HERE.parent / "social_respending_2026_10_14/derived/conditional_stacks.csv").open())
                       if all(r[k] == v for k, v in dict(end=end, spending_denominator="PCE", mortality_valuation="uniform",
                               real_discount_rate="0", crash_arm="multivehicle_only", volunteering_proxy="primary_food",
                              displacement="1.0", market_demand_arm="False", pm_crash_recipient_boundary="lineage_exchangeable").items()))
        pm = next(d for d in detail if d["item"] == "pm25_consumption")
        gross_pm = pm[f"union_before_boundary_{end}_bn"] * (1 + pm[f"share_{end}"])
        assert parts["pm_replacement_bn"] == pytest.approx(
            float(source["pm_gross_replacement_bn"]) - parts["current_H_bn"] * parts["pm_unit_harm_per_bn_spent"], abs=1e-9)
        assert parts["crash_replacement_bn"] == pytest.approx(float(source["crash_replacement_bn"]), abs=1e-9)
        active = next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                      and r["item"] == f"published pairing ({end})")
        assert active == pytest.approx(before[end] + sum(parts["terms"].values()), abs=1e-9)
        mirror = doc["v8_social_environment"]["variants"]["government_mirror"]["pairing_bn"][end]
        assert mirror - active == pytest.approx(float(source["government_mirror_bn"]), abs=1e-9)
        assert "government_mirror" not in parts["terms"]
        cash = next(r for r in rows if r["column"] == "pairing_on_priced_count_cash_set"
                    and r["item"] == f"published pairing ({end})")
        central = next(r for r in rows if r["column"] == "pairing_on_priced_count"
                       and r["item"] == f"published pairing ({end})")
        assert central["oct15"] - cash["oct15"] == pytest.approx(before[end] - cash_before[end], abs=1e-9)
        resource = doc["v8_social_environment"]["variants"]["resource_wealth_equivalent"]["parts"][end]
        assert resource["spending_base_bn"] == pytest.approx(parts["current_H_bn"] +
            parts["resource_account"]["capital_return_bn"] + 75.0 - parts["market_income_lost_bn"], abs=1e-9)
        assert resource["spending_base_bn"] == pytest.approx(
            parts["resource_account"]["set_cost_bn"]-parts["city_income_lost_bn"], abs=1e-9)
        deferred = doc["v8_social_environment"]["variants"]["resource_promises_deferred"]["parts"][end]
        assert deferred["spending_base_bn"] == pytest.approx(
            parts["resource_account"]["cash_cost_bn"]-parts["city_income_lost_bn"], abs=1e-9)
        assert abs(doc["joint_social_stack"]["ends"][end]["interaction_residual_bn"]) <= 1e-9


def test_undeclared_population_transport_stops():
    rows, doc = frozen_rows()
    with pytest.raises(ValueError, match="undeclared v8 social transport"):
        totals.apply_v8_environment(rows, doc, {}, {}, "flat_headcount_scale")


def test_accounting_basis_mismatch_stops():
    rows, doc = frozen_rows()
    meta = funding_meta()
    meta["social_resource_account"]["ends"]["low"]["accounting_basis"] = "CE_survey"
    with pytest.raises(ValueError, match="accounting basis mismatch"):
        totals.apply_v8_environment(rows, doc, meta, {"v8": {"population": {"with_coverage": 45e6}}}, "fixed_v7_source_keys")
