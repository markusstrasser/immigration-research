"""P7 row replacement must not double-remove recipients; both sides of the budget response are paired."""
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


def funding_meta(rows, doc):
    """v8-shaped resource account on the frozen v7 rows: the pairing's fiscal row is the set cost at both ends."""
    case = json.loads((HERE.parent / "social_respending_2026_10_14/derived/case_inputs.json").read_text())
    before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                        and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    prior = {end: sum(d[f"union_{end}_bn"] + d[f"added_{end}_bn"] for d in doc["lineage_social_rows"]["rows"])
             for end in ("low", "high")}
    ends = {}
    for r in case["rows"]:
        if r["population_basis"] == "lineage":
            end, fiscal = r["end"], before[r["end"]] - prior[r["end"]]
            ends[end] = dict(accounting_basis="national_accounts",current_H_bn=r["current_budget_saving_bn"],
                capital_return_bn=r["capital_return_bn"],net_accrual_timing_bridge_bn=fiscal-r["cash_set_cost_bn"],
                private_wtp_bn=r["private_wtp_bn"],cash_cost_bn=r["cash_set_cost_bn"],set_cost_bn=fiscal,
                government_consumption_removed_bn=r["government_consumption_removed_bn"],
                government_consumption_national_bn=r["government_consumption_national_bn"])
    raw = dict(ends["low"], current_H_bn=ends["low"]["current_H_bn"]-4.7, cash_cost_bn=ends["low"]["cash_cost_bn"]-4.7,
               set_cost_bn=ends["low"]["set_cost_bn"]-4.7,
               government_consumption_removed_bn=ends["low"]["government_consumption_removed_bn"]-4.6)
    return {"social_resource_account": {"ends": ends, "raw_coded_low_end": raw}}


def government_ratio(end):
    rows = {r["item"]: float(r["central_bn"]) for r in csv.DictReader(
        (HERE.parent / "social_respending_2026_10_14/derived/items.csv").open())
        if r["population_basis"] == "lineage" and r["end"] == end and r["spending_denominator"] == "PCE"}
    return rows["pm25_government_mirror_budget_mix_arm"] / rows["pm25_government_mirror_legacy_response"]


def test_environment_pairs_both_budget_sides_and_replaces_boundary_adjusted_rows_once():
    rows, doc = frozen_rows()
    before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                       and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    cash_before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count_cash_set"
                            and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    meta = funding_meta(rows, doc)
    totals.apply_v8_environment(rows, doc, meta, {"v8": {"population": {"with_coverage": 45e6}}}, "fixed_v7_source_keys")
    variants = doc["v8_social_environment"]["variants"]
    for end in ("low", "high"):
        parts = variants["central"]["parts"][end]
        source = next(r for r in csv.DictReader((HERE.parent / "social_respending_2026_10_14/derived/conditional_stacks.csv").open())
                       if all(r[k] == v for k, v in dict(end=end, spending_denominator="PCE", mortality_valuation="uniform",
                               real_discount_rate="0", crash_arm="multivehicle_only", volunteering_proxy="primary_food",
                              displacement="1.0", market_demand_arm="False", pm_crash_recipient_boundary="lineage_exchangeable").items()))
        assert parts["pm_replacement_bn"] == pytest.approx(
            float(source["pm_gross_replacement_bn"]) - parts["current_H_bn"] * parts["pm_unit_harm_per_bn_spent"], abs=1e-9)
        assert parts["crash_replacement_bn"] == pytest.approx(float(source["crash_replacement_bn"]), abs=1e-9)
        active = next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                      and r["item"] == f"published pairing ({end})")
        assert active == pytest.approx(before[end] + sum(parts["terms"].values()), abs=1e-9)
        # Both sides of the budget response are central; on the v7 removed consumption the government side is the
        # producer's budget-mix arm on the legacy row's mortality weighting and receiver factor.
        government = parts["terms"]["government_side"]
        assert government == pytest.approx(float(source["government_mirror_bn"]) * government_ratio(end), abs=1e-9)
        assert "pm_respending" in parts["terms"] and "v8_added_people" not in parts["terms"]
        legacy = variants["government_legacy_response"]["pairing_bn"][end]
        assert legacy - active == pytest.approx(float(source["government_mirror_bn"]) - government, abs=1e-9)
        assert variants["respending_without_government_side"]["pairing_bn"][end] == pytest.approx(active - government, abs=1e-9)
        assert variants["neither_budget_side"]["pairing_bn"][end] == pytest.approx(
            active - government - parts["terms"]["pm_respending"], abs=1e-9)
        for name, variant in variants.items():
            terms = variant["parts"][end]["terms"]
            paired = ("pm_respending" in terms) == any(k in terms for k in ("government_side", "government_legacy_response"))
            assert paired or name == "respending_without_government_side"
        cash = next(r for r in rows if r["column"] == "pairing_on_priced_count_cash_set"
                    and r["item"] == f"published pairing ({end})")
        central = next(r for r in rows if r["column"] == "pairing_on_priced_count"
                       and r["item"] == f"published pairing ({end})")
        assert central["oct15"] - cash["oct15"] == pytest.approx(before[end] - cash_before[end], abs=1e-9)
        resource = variants["resource_wealth_equivalent"]["parts"][end]
        assert resource["spending_base_bn"] == pytest.approx(parts["current_H_bn"] +
            parts["resource_account"]["capital_return_bn"] + parts["resource_account"]["net_accrual_timing_bridge_bn"]
            - parts["market_income_lost_bn"], abs=1e-9)
        assert resource["spending_base_bn"] == pytest.approx(
            parts["resource_account"]["set_cost_bn"]-parts["city_income_lost_bn"], abs=1e-9)
        deferred = variants["resource_promises_deferred"]["parts"][end]
        assert deferred["spending_base_bn"] == pytest.approx(
            parts["resource_account"]["cash_cost_bn"]-parts["city_income_lost_bn"], abs=1e-9)
        assert abs(doc["joint_social_stack"]["ends"][end]["interaction_residual_bn"]) <= 1e-9
        assert doc["joint_social_stack"]["ends"][end]["fiscal_pairing_bn"] == pytest.approx(
            meta["social_resource_account"]["ends"][end]["set_cost_bn"], abs=1e-9)
    # The matched footing re-reads the raw-coded low end: fiscal, saving and removed consumption all move.
    raw, case = meta["social_resource_account"]["raw_coded_low_end"], meta["social_resource_account"]["ends"]["low"]
    low = variants["central"]["parts"]["low"]
    matched = variants["matched_justice_footing"]["pairing_bn"]
    expected = (variants["central"]["pairing_bn"]["low"] - 4.7 + 4.7 * low["pm_unit_harm_per_bn_spent"]
                - 4.6 * low["government_pm_per_removed_bn"])
    assert raw["set_cost_bn"] == pytest.approx(case["set_cost_bn"] - 4.7)
    assert matched["low"] == pytest.approx(expected, abs=1e-9)
    assert matched["high"] == pytest.approx(variants["central"]["pairing_bn"]["high"], abs=1e-9)


def test_pairing_fiscal_row_must_be_the_case():
    rows, doc = frozen_rows()
    meta = funding_meta(rows, doc)
    meta["social_resource_account"]["ends"]["low"]["set_cost_bn"] -= 4.7
    with pytest.raises(ValueError, match="fiscal row is not the case's set cost"):
        totals.apply_v8_environment(rows, doc, meta, {"v8": {"population": {"with_coverage": 45e6}}}, "fixed_v7_source_keys")


def test_v8_added_people_shares_from_the_live_case():
    meta = json.loads((HERE / "derived/oct15/band_variants.json").read_text())
    added = totals.v8_added_social(meta)
    assert added["people"]["completion"] == pytest.approx(meta["union_completion"]["counts"]["total"], abs=1e-6)
    assert added["people"]["coverage"] == pytest.approx(meta["post_engine"]["coverage"]["net_missing_people"], abs=1e-6)
    for end in ("low", "high"):
        assert all(0 < s < 0.2 for s in added["shares"][end].values())
    assert -0.1 < added["item11_consumption_factor"] < 0
    assert all(0 < s < 0.01 for s in added["completion_receiver_share"].values())
    assert totals.scope_people({"0-4": 5.0, "15-19": 5.0, "20-24": 1.0}, "5_17") == pytest.approx(3.0)
    assert totals.scope_people({"0-4": 5.0, "15-19": 5.0, "20-24": 1.0}, "18_plus") == pytest.approx(3.0)


def test_undeclared_population_transport_stops():
    rows, doc = frozen_rows()
    with pytest.raises(ValueError, match="undeclared v8 social transport"):
        totals.apply_v8_environment(rows, doc, {}, {}, "flat_headcount_scale")


def test_accounting_basis_mismatch_stops():
    rows, doc = frozen_rows()
    meta = funding_meta(rows, doc)
    meta["social_resource_account"]["ends"]["low"]["accounting_basis"] = "CE_survey"
    with pytest.raises(ValueError, match="accounting basis mismatch"):
        totals.apply_v8_environment(rows, doc, meta, {"v8": {"population": {"with_coverage": 45e6}}}, "fixed_v7_source_keys")
