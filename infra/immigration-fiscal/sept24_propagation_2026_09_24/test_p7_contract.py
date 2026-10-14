"""The adopted totals cannot silently consume an incompatible social comparator."""
import copy
import csv
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tested_real_costs", HERE / "real_costs_totals.py")
totals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(totals)
LANE = HERE.parent / "social_costs_unpriced_2026_09_28"


def test_equal_population_security_stops_adopted_run():
    with pytest.raises(ValueError, match="equal-population"):
        totals.social_contract(LANE / "derived/p7_items.csv", dict(item="private_security", measure="normalized"))
    with pytest.raises(ValueError, match="incompatible comparator"):
        totals.social_contract(LANE / "derived/p7_items.csv", dict(item="private_security", comparator="equal_population"))
    with pytest.raises(ValueError, match="equal-population"):
        totals.social_items(totals.SOCIAL_ITEMS["oct14"])


@pytest.mark.parametrize("key,value", [("beneficiary_population", "all_residents"),
                                      ("valuation_basis", "unpriced"), ("overlap_set", "[]")])
def test_incompatible_contract_fields_stop(key, value):
    with pytest.raises(ValueError, match=f"incompatible {key}"):
        totals.social_contract(LANE / "derived/p7_items.csv", dict(item="private_security", **{key: value}))


def test_missing_source_or_item_declaration_stops():
    with pytest.raises(ValueError, match="no consumer declaration"):
        totals.social_contract(LANE / "derived/p7_items.csv", dict(item="new_unregistered_cost"))
    with pytest.raises(ValueError, match="undeclared source"):
        totals.social_contract(HERE / "derived/items.csv", dict(item="private_security"))


def test_typed_security_is_accepted_and_has_overlap_declaration():
    row = next(csv.DictReader((LANE / "derived/p7_items.csv").open()))
    contract = totals.social_contract(LANE / "derived/p7_items.csv", row)
    assert contract["comparator"] == "with_without"
    assert contract["beneficiary_population"] == "residents_outside_union"
    assert contract["overlap_set"]


def test_consumer_registry_covers_every_adopted_social_row():
    assert set(totals.SOCIAL_CONTRACTS) == set(totals.LINEAGE_ROW_KEYS)
    keys = json.loads((LANE / "derived/payment_keys.json").read_text())
    meta = json.loads((HERE / "derived/oct14/band_variants.json").read_text())
    for end in ("low", "high"):
        current = meta["items"]["lineage_social_keys_on_the_case"][f"{end}_end"]
        assert "consumption" in current["moved"]
        assert keys[end]["lineage_ratio_source"] == "meta.items.lineage_social_keys_on_the_case"
        assert keys[end]["added_bn"]/keys[end]["union_bn"] == pytest.approx(current["shares"]["consumption"], abs=1e-12)


def test_boundary_treats_benefits_as_signed_flows():
    keys = {"head_count": 0.1, "low_end": {}, "high_end": {}}
    for names in totals.LINEAGE_ROW_KEYS.values():
        for key in names:
            if key is not None:
                keys["low_end"][key] = keys["high_end"][key] = 0.1
    path = LANE / "inputs/baseline_restated_pairing.csv"
    raw = list(csv.DictReader(path.open()))
    social = []
    for end in ("low", "high"):
        selected = {r["item"]: float(r["restated"]) for r in raw if r["section"] == "row" and r["item"] != "fiscal" and r["end"] in (end, "both")}
        selected.update({r["item"]: float(r["restated"]) for r in raw if r["section"] == "row_5plus" and r["end"] in (end, "both")})
        social.append(sum(selected.values()))
    detail, _ = totals.lineage_social_rows(path, keys, social, {item: 0.01 for item in totals.LINEAGE_ROW_KEYS})
    benefit = next(r for r in detail if r["item"] == "housing_gain")
    assert benefit["union_to_added_low_bn"] < 0
    assert benefit["boundary_change_low_bn"] > 0
    for row in detail:
        assert row["added_low_bn"] == pytest.approx(row["gross_added_low_bn"] + row["boundary_change_low_bn"])


def test_p7_changes_only_declared_output_rows():
    with (LANE / "inputs/baseline_totals_oct14.csv").open() as handle:
        baseline = list(csv.DictReader(handle))
    with (HERE / "derived/oct14/real_costs_totals.csv").open() as handle:
        actual = list(csv.DictReader(handle))
    changed = {"full_span"}
    assert len(actual) == len(baseline) + 12
    for old, new in zip(baseline, actual[:len(baseline)]):
        if old["column"] in ("social_item_fear_avoidance", "social_item_private_security", "social_items_2026_09_28"):
            assert new["column"] == "historical_control_" + old["column"]
            assert new["oct14"] == old["oct14"]
            continue
        if old["column"] in changed or old["column"].startswith(("pairing_on_priced_count", "lineage_social_")):
            continue
        assert old == new
    doc = json.loads((HERE / "derived/oct14/real_costs_totals.json").read_text())
    assert doc["p7_crime"]["beneficiary_after_boundary"] == "residents_outside_lineage"
    for end in ("low", "high"):
        records = doc["lineage_social_rows"]["rows"]
        assert sum(r[f"added_{end}_bn"] for r in records) == pytest.approx(doc["lineage_social_rows"]["added_social_bn"][end])
