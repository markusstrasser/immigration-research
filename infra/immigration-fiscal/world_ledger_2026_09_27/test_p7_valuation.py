"""P7 receipt incidence, fail-closed valuation and the nonmember-filer credit transfer."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import valuation as V


@pytest.fixture(scope="module")
def live_values():
    union, _ = V.value_case("oct14")
    generations = V.value_generations("oct14", union)
    return union, generations


def test_positive_control_recovers_pre_fix_oct14(live_values):
    """Undo the two isolated payer fixes and recover the committed pre-P7 result at its printed precision."""
    union, generations = live_values
    for values, filename, precision in ((union, "valuation.csv", 0.500001e-6),
                                         (generations, "valuation_by_generation.csv", 0.500001e-9)):
        rel = str(V.case_path(filename, "oct14").relative_to(V.REPO))
        before = V.pinned_csv("0b41a200", rel)
        keys = ["end", "side", "line"] + (["generation"] if "generation" in values else [])
        now, old = values.set_index(keys), before.set_index(keys)
        assert now.index.equals(old.index)
        for column in ("V_low_bn", "V_central_bn", "V_high_bn"):
            restored = now[column] - now.source_tax_credit_bn + now.child_credit_other_residents_bn
            assert (restored - old[column]).abs().max() < precision
        for column in ("amount_bn", "G_bn", "net_cost_bn"):
            assert (now[column] - old[column]).abs().max() < precision


def test_item6_uses_frozen_registry_and_never_debits_group(live_values):
    union, generations = live_values
    _, edits = V.item_edits(V.case_payload("oct14"), "job_capital_taxes")
    authoritative = {edit["line"] for edit in edits}
    for values in (union, generations):
        source = values[values.cls.eq("source_tax")]
        assert set(source.line) == authoritative
        assert source[["V_low_bn", "V_central_bn", "V_high_bn"]].eq(0).all().all()
        assert source.source_tax_credit_bn.gt(0).all()
        assert source.net_cost_bn.eq(-source.source_tax_credit_bn).all()
        assert set(source[source.line.eq("corporate_labor")].economic_payer) == {"group_workers_via_measured_wages"}
        assert set(source[~source.line.eq("corporate_labor")].economic_payer) == {"business_capital_owners_outside_group"}


def test_unknown_receipt_never_defaults_to_group_tax():
    row = SimpleNamespace(side="receipt", line="future_unclassified_receipt", amount_bn=1.0, effect_bn=1.0,
                          response=1.0)
    with pytest.raises(SystemExit, match="unclassified receipt"):
        V.valuation_row(row, V.RECEIPT_CLASS, V.RECEIPT_PAYER)


def test_receipt_without_economic_payer_is_blocked():
    row = SimpleNamespace(side="receipt", line="federal_income_tax", amount_bn=1.0, effect_bn=1.0, response=1.0)
    with pytest.raises(SystemExit, match="economic_payer"):
        V.valuation_row(row, V.RECEIPT_CLASS, {})


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
@pytest.mark.parametrize("field", ["amount_bn", "effect_bn", "response"])
def test_nonfinite_receipt_blocks_valuation(value, field):
    row = dict(side="receipt", line="federal_income_tax", amount_bn=1.0, effect_bn=1.0, response=1.0)
    row[field] = value
    with pytest.raises(SystemExit, match="finite_line"):
        V.valuation_row(SimpleNamespace(**row), V.RECEIPT_CLASS, V.RECEIPT_PAYER)


def test_all_live_receipts_name_their_economic_payer(live_values):
    for values in live_values:
        receipts = values[values.side.eq("receipt")]
        assert receipts.economic_payer.notna().all()
        assert receipts.economic_payer.str.len().gt(0).all()
        assert receipts.receipt_incidence_class.notna().all()


def test_state_price_nan_is_rejected_before_pandas_can_skip_it(monkeypatch, tmp_path):
    line = "state_price_health_services"
    pd.DataFrame({"line": [line, line], "function": ["a", "b"], "gap_bn": [1.0, 2.0],
                  "quantity_bn": [1.0, np.nan]}).to_csv(tmp_path / "state_price_quantity.csv", index=False)
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    monkeypatch.setattr(V, "_STATE_PRICE", {})
    with pytest.raises(SystemExit, match="finite_state_price"):
        V.state_price_functions(line)


def test_incidence_total_rejects_nan_instead_of_skipping_it(live_values):
    union, generations = live_values
    invalid = union.copy()
    invalid.loc[0, "source_tax_credit_bn"] = np.nan
    with pytest.raises(SystemExit, match="finite_incidence_union"):
        V.incidence_summary("oct14", invalid, generations)


def test_child_credits_move_only_frozen_item5b_to_nonmember_filers(live_values):
    union, generations = live_values
    child, _ = V.item_edits(V.case_payload("oct14"), "child_credits")
    expected = child["source_net_bn"] + child["added_people_bn"]
    for values in (union, generations):
        changed = values[values.child_credit_other_residents_bn.ne(0)]
        assert set(changed.line) == {"federal_income_tax", "refundable_tax_credits"}
        assert values.group_credit_adjustment_bn.eq(-values.child_credit_other_residents_bn).all()
        assert all(abs(value - expected) < 1e-9 for value in values.groupby("end").child_credit_other_residents_bn.sum())
    by = generations.groupby(["end", "generation"]).child_credit_other_residents_bn.sum()
    for end in ("low", "high"):
        for generation, amount in child["source_by_generation_bn"].items():
            name = generation.replace("G3plus", "G3+")
            expected_gen = amount + (child["added_people_bn"] if name == "G3+" else 0)
            assert abs(by.loc[(end, name)] - expected_gen) < 1e-9
    # The reverse adjustment in G1 is retained, rather than clipping all child terms to nonnegative values.
    assert by.loc[("low", "G1")] < 0


def test_foreign_parity_stress_excludes_corporate_labor(live_values):
    union, generations = live_values
    meta = V.incidence_summary("oct14", union, generations)
    for end, item in meta.items():
        foreign = item["foreign_capital_source_tax_exclusion"]
        assert foreign["mexico_bn"] is None and foreign["rest_of_world_bn"] is None
        assert "no empirical finite identification bound" in foreign["bound_kind"]
        assert abs(foreign["assumption_stress_upper_bn"] - item["capital_source_tax_credit_bn"]) < 1e-9
        assert abs(item["capital_source_tax_credit_bn"] + item["corporate_labor_credit_bn"]
                   - item["source_tax_credit_bn"]) < 1e-9


def test_new_item6_receipt_requires_explicit_incidence(monkeypatch):
    payload = {"meta": {"items": [{"id": "job_capital_taxes", "applied": True,
                                   "edits": {"first": 0, "count": 1}}]},
               "edits": [{"side": "receipt", "line": "new_source_tax"}]}
    monkeypatch.setattr(V, "case_payload", lambda case: payload)
    with pytest.raises(SystemExit, match="item6_explicit_receipt_incidence"):
        V.receipt_contract("oct14")


def test_child_credit_scenario_and_allocation_are_selected_not_summed(monkeypatch):
    payload = {"meta": {"items": [{"id": "child_credits", "applied": True,
        "edits": {"first": 0, "count": 3}, "parts": {
            "union_G2:normal": {"edit": 0, "by": {"personal": -2.0, "shared": -200.0}},
            "union_G2:other": {"edit": 1, "by": {"personal": -9.0, "shared": -900.0}},
            "lineage_g3plus:spending": {"edit": 2, "by": {"personal": 3.0, "shared": 300.0}}}}]},
        "edits": [{"side": "receipt", "line": "federal_income_tax", "scenario": scenario,
                   "by": {"personal": amount, "shared": amount * 100}}
                  for scenario, amount in (("normal", -2.0), ("other", -9.0))] +
                 [{"side": "spending", "line": "refundable_tax_credits", "key": "credits",
                   "by": {"personal": 3.0, "shared": 300.0}}]}
    monkeypatch.setattr(V, "case_payload", lambda case: payload)
    lines = pd.DataFrame([dict(band_end=end, generation=generation, allocation="personal", side=side, line=line,
                              key=key, response=1.0)
                          for end in ("low", "high") for generation in ("G1", "G2", "G3+")
                          for side, line, key in (("receipt", "federal_income_tax", "normal:tax"),
                                                  ("spending", "refundable_tax_credits", "credits"))])
    credits = V.child_credit_adjustments("oct14", lines)
    for end in ("low", "high"):
        assert sum(value for key, value in credits.items() if key[0] == end) == 5.0
        assert credits[(end, "G2", "receipt", "federal_income_tax")] == 2.0
        assert credits[(end, "G3+", "spending", "refundable_tax_credits")] == 3.0
