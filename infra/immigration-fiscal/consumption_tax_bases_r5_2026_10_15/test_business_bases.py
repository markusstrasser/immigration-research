"""Source identity, tax denominator and conditional purchaser-allocation gates."""
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("business_bases_l3a", HERE / "business_bases.py")
business = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(business)


@pytest.fixture(scope="module")
def bridge():
    return business.build_bridge()


def test_current_shares_do_not_substitute_dated_estimates(bridge):
    assert len(bridge["state_sales"]) == 51
    assert len({r["state_fips"] for r in bridge["state_sales"]}) == 51
    assert all(r["central_2024_business_share"] is None for r in bridge["state_sales"])
    assert all(r["share_lower"] == 0 and r["share_upper"] == 1 for r in bridge["state_sales"])
    with pytest.raises(ValueError, match="central unavailable"):
        business.require_identified_central(bridge)


def test_state_denominators_and_forecasts_remain_distinct(bridge):
    states = {r["state_fips"]: r for r in bridge["state_sales"]}
    texas = states["48"]["dated_source_estimates"]
    assert {r["year"] for r in texas} == {2025, 2027}
    assert all(r["forecast"] and not r["usable_as_2024_central"] for r in texas)
    assert texas[0]["business_share"] == pytest.approx(22727 / 54835.6)
    assert all(sum(r["conditional_business_industry_weights"].values()) == pytest.approx(1) for r in texas)
    mn = states["27"]["dated_source_estimates"]
    assert next(r for r in mn if r["year"] == 2023 and r["denominator"].startswith("state"))["business_share"] == 0.48
    local = [r for r in mn if r["denominator"].startswith("local")]
    assert all(not r["compatible_with_general_sales_tax"] for r in local)
    assert bridge["crosscheck_only"]["usable_as_central"] is False


def test_bea_principal_and_commodity_totals_conserve(bridge):
    arm = bridge["customs_proportional_arm"]
    assert arm["measured_total_import_duties_bn"] == 83.587
    assert arm["measured_all_tax_on_products_bn"] == 1015.461
    assert sum(c["import_duties_million"] for c in arm["commodities"]) / 1000 == pytest.approx(83.587)
    assert sum(r["share_of_total_duties"] for r in arm["purchaser_weights"]) == pytest.approx(1, abs=1e-14)
    assert sum(r["conditional_duties_bn"] for r in arm["purchaser_weights"]) == pytest.approx(83.587, abs=1e-11)
    assert arm["conditional_household_share"] + arm["conditional_intermediate_share"] + arm["conditional_unkeyed_final_demand_share"] == pytest.approx(1)
    assert arm["conditional_household_share"] == pytest.approx(0.4621685640650344)


def test_keys_keep_mining_and_missing_final_demand_visible(bridge):
    rows = bridge["customs_proportional_arm"]["purchaser_weights"]
    assert {r["io_code"] for r in rows if r["production_response"] == 0} == business.MINING
    assert next(r for r in rows if r["io_code"] == "525")["key"] == "523"
    assert all(r["key"] == "GOVF" for r in rows if r["io_code"] in ("GFGD", "GFGN", "GFE"))
    assert all(r["production_response"] is None for r in rows if r["kind"] == "unkeyed_final_demand")
    housing = next(r for r in rows if r["io_code"] == "HS")
    assert housing["kind"] == "unkeyed_intermediate" and housing["production_response"] is None
    wages = business.ROOT / "infra/immigration-fiscal/job_capital_taxes_2026_10_14/derived/wages_by_industry.csv"
    import csv
    with wages.open() as handle:
        wage_keys = {r["cell"] for r in csv.DictReader(handle)}
    assert all(r["key"] in wage_keys for r in rows if r["kind"] == "intermediate")
    assert not {"F030", "F040"} & {r["io_code"] for r in rows}
    assert bridge["national_taxes"]["excise_selective_sales"]["central_business_share"] is None


def test_bad_source_fails_loudly():
    inputs = json.loads(business.SOURCE_FILE.read_text())
    inputs["sources"]["tx2025"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        business.verify_sources(inputs)


def test_conditional_evaluator_blocks_missing_final_purchaser_response(bridge):
    arm = bridge["customs_proportional_arm"]
    rows = arm["purchaser_weights"]
    responses = {r["key"]: 0.1 for r in rows if r["kind"] == "intermediate"}
    with pytest.raises(ValueError, match="customs purchaser responses missing: F02E"):
        business.customs_group_share(bridge, 0.1, responses)
    responses.update({r["key"]: 0.1 for r in rows if r["kind"] == "unkeyed_final_demand"})
    with pytest.raises(ValueError, match="customs purchaser responses missing: HS"):
        business.customs_group_share(bridge, 0.1, responses)
    responses["HS"] = 0.1
    mining = sum(r["share_of_total_duties"] for r in rows if r["io_code"] in business.MINING)
    assert business.customs_group_share(bridge, 0.1, responses) == pytest.approx(0.1 * (1 - mining))
    responses["F02E"] = -0.1
    with pytest.raises(ValueError, match="invalid purchaser response F02E"):
        business.customs_group_share(bridge, 0.1, responses)


def test_row_scoped_value_validation_rejects_number_elsewhere():
    rows = [{"source_id": "mn", "state_fips": "27", "denominator": "state general sales/use tax",
             "total_million": 8167, "published_business_percent": 48.0}]
    good = " General sales/use tax 8,167 18.3% 47.1% 4.9% 48.0% 100.0%\n"
    business.verify_estimate_rows(rows, {"mn": good})
    with pytest.raises(ValueError, match="MN tax row mismatch"):
        business.verify_estimate_rows(rows, {"mn": good.replace("48.0%", "47.0%") + "48.0% elsewhere"})


def test_stable_serialization(bridge):
    saved = json.loads((HERE / "inputs/business_bridge.json").read_text())
    assert saved == bridge
    assert b"\r\n" not in (HERE / "inputs/business_bridge.json").read_bytes()
