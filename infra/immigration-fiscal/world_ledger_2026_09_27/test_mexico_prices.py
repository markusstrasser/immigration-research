import numpy as np
import pandas as pd
import pytest
from mexico_prices import (budget_from_gdp, budget_values, mixture_divisor,
                           numeric_row_metadata, price_budget, scale_peso_rows,
                           validate_numeric_rows)


def source():
    return budget_from_gdp(pd.DataFrame([
        dict(generation="G1", cls=cls, bn=amount)
        for cls, amount in (("education", 4), ("health", 6), ("cash", 3), ("public_good", 10))
    ]), 10)


def test_value_arm_leaves_fiscal_pesos_and_saved_rows_unchanged():
    base = source()
    changed = price_budget(base, dict(education=2, health=8, cash=11, public_good=6), recipient_only=True)
    before = budget_values(base, "G1", (0.5, 0.6, 0.7), (0.6, 0.725, 0.85))
    after = budget_values(changed, "G1", (0.5, 0.6, 0.7), (0.6, 0.725, 0.85))
    assert before[:2] == after[:2]
    assert before[2] != after[2]
    assert changed.fiscal_cost_pesos_bn.equals(base.fiscal_cost_pesos_bn)


def test_repeated_response_below_floor_blocks():
    with pytest.raises(SystemExit, match="public_response_floor"):
        budget_values(source(), "G1", (1, 1, 1), (0.6 * 0.725, 0.725**2, 0.85 * 0.725))


def test_shared_field_scaling_cannot_disguise_a_second_fiscal_response():
    budget = source()
    selected = budget.cls.eq("public_good")
    budget.loc[selected, "fiscal_cost_pesos_bn"] *= 0.725
    budget.loc[selected, "fiscal_cost_bn"] *= 0.725
    with pytest.raises(SystemExit, match="fiscal_cost_is_full_source_cost"):
        budget_values(budget, "G1", (1, 1, 1), (0.6, 0.725, 0.85))


def test_ppp_mix_is_harmonic_and_scaling_invariant():
    p = dict(education=40, health=60, cash=30, public_good=100)
    d = dict(education=2, health=8, cash=11, public_good=6)
    expected = sum(p.values()) / sum(p[c] / d[c] for c in p)
    assert mixture_divisor(p, d) == expected
    assert mixture_divisor({k: v * 3 for k, v in p.items()}, d) == pytest.approx(expected, abs=1e-12)


def test_legacy_r1_assigned_label_cannot_pass_numeric_gate():
    rows = pd.DataFrame([dict(row="mexico_taxes_lost_G1", party="mexico_residents",
                              price_basis="PPP-GDP", low=-10, central=-10, high=-10)])
    with pytest.raises(SystemExit, match="numeric_price_contract_present"):
        validate_numeric_rows(rows)


def test_numeric_basis_detects_false_gdp_conversion():
    pesos = dict.fromkeys(("low", "central", "high"), -100)
    metadata = numeric_row_metadata(pesos, 11, "consumption")
    rows = pd.DataFrame([dict(party="mexico_residents", low=-10, central=-10, high=-10, **metadata)])
    with pytest.raises(SystemExit, match="actual_numeric_conversion"):
        validate_numeric_rows(rows)


def test_peso_scaling_scales_each_mexico_flow_and_party_total():
    rows = []
    for pesos, divisor, basis in ((120, 6, "services"), (-90, 9, "budget_mix"), (220, 11, "consumption")):
        amounts = dict.fromkeys(("low", "central", "high"), pesos / divisor)
        rows.append(dict(party="mexico_residents", **amounts,
                         **numeric_row_metadata(dict.fromkeys(amounts, pesos), divisor, basis)))
    table = pd.DataFrame(rows)
    got = scale_peso_rows(table, 2.5)
    assert np.allclose(got[["low", "central", "high"]], table[["low", "central", "high"]] * 2.5,
                       atol=1e-12, rtol=0)
    assert got.central.sum() == table.central.sum() * 2.5
