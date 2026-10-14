"""Regression checks for compensation, price conversion and fail-closed aggregation."""
import copy

import numpy as np
import pandas as pd
import pytest

import world_ledger as W
from employer_ui_basis import load_basis


def test_remittance_primary_price_conversion():
    r = W.remittance_price_factor("gdp")
    assert r == pytest.approx(W.wdi_mexico_2024("PA.NUS.FCRF") / W.wdi_mexico_2024("PA.NUS.PPP"), abs=1e-12)
    c = W.remittance_price_factor("consumption")
    assert c == pytest.approx(W.wdi_mexico_2024("PA.NUS.FCRF") / W.wdi_mexico_2024("PA.NUS.PRVT.PP"), abs=1e-12)
    assert r > c > 1


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_nonfinite_row_blocks_before_totals(bad):
    rows = pd.DataFrame([dict(party="G1", row="premium_G1", price_basis="US$", low=bad, central=1, high=1)])
    with pytest.raises(SystemExit, match="row_amounts_finite"):
        W.totals(rows, {}, {}, "low", {"_lambda": {}}, None)


def test_price_mix_blocks():
    rows = pd.DataFrame([
        dict(party="mexico_residents", price_basis=b, low=1, central=1, high=1)
        for b in ("PPP-GDP", "PPP-consumption")])
    with pytest.raises(SystemExit, match="one_price_basis"):
        W.validate_rows(rows)


def test_log_cannot_weight_nominal_mexican_dollars():
    rows = pd.DataFrame([dict(party="mexico_residents", price_basis="US$", low=1, central=1, high=1)])
    with pytest.raises(SystemExit, match="log_mexico_rows_are_ppp"):
        W.validate_rows(rows, logarithmic=True)


def test_nonpositive_log_consumption_blocks():
    prem = {g: dict(persons=1, e_us=1, e_mx=dict(central=1)) for g in W.GROUP}
    rows = []
    for g in W.GROUP:
        for prefix, value in (("mexico_budget_lost", 0), ("us_budget_value", -2), ("ingroup_victims", 0),
                              ("uncompensated_received", 0)):
            rows.append(dict(party=g, row=f"{prefix}_{g}", central=value))
    I = dict(wmeta=dict(us_reference=dict(per_capita=dict(y_ref_other_mean=1))))
    with pytest.raises(SystemExit, match="log_consumption"):
        W.group_log(pd.DataFrame(rows), prem, I, "central")


def test_employer_receipts_add_once_and_zero_bound_remains_zero():
    I = W.load("oct14", "lineage")
    p = W.premium_rows(I)
    for g in W.GROUP:
        amount = -I["vgen"].loc[I["vgen"].generation.eq(g)
            & I["vgen"].line.isin(["employer_oasdi", "employer_hi"]), "net_cost_bn"].sum() / 2
        amount -= (I["vgen"].loc[I["vgen"].generation.eq(g)
            & I["vgen"].line.eq("other_domestic_social_contributions"), "net_cost_bn"].sum() / 2
            * load_basis()["employer_fraction"])
        assert p[g]["e_us"] - p[g]["e_us_cash"] == pytest.approx(amount, abs=1e-9)
    assert p["G3+"]["gain"]["central"] == 0
    assert p["G3+"]["e_mx"]["central"] == p["G3+"]["e_us"]


def test_nan_employer_receipt_blocks():
    I = W.load("oct14", "lineage")
    I["vgen"] = I["vgen"].copy()
    m = I["vgen"].line.eq("employer_hi") & I["vgen"].generation.eq("G1")
    I["vgen"].loc[m, "net_cost_bn"] = np.nan
    with pytest.raises(SystemExit, match="employer_compensation"):
        W.premium_rows(I)


def test_requested_weighting_reproduces_full_totals_exactly():
    I = W.load("oct14", "lineage")
    rows, prem, _ = W.build_rows(I)
    fac = W.channel_factors(I, "money")
    fac["_lambda"] = {"equal_lambda_1.16": 1.16}
    full = W.totals(rows, prem, I, "central", fac, I["pos"])
    only = W.totals(rows, prem, I, "central", fac, I["pos"], requested_weightings=["equal_lambda_1.16"])
    pd.testing.assert_frame_equal(only.reset_index(drop=True),
        full[full.weighting.eq("equal_lambda_1.16")].reset_index(drop=True), check_exact=True)


def test_unknown_requested_weighting_blocks():
    with pytest.raises(SystemExit, match="requested_weightings_declared"):
        W.totals(pd.DataFrame(), {}, {}, "central", {"_lambda": {}}, None, requested_weightings=["typo"])


def test_nonfinite_distributed_channel_cannot_be_skipped_by_sum():
    I = {"dist": pd.DataFrame([dict(measure="money", bn=np.nan, percentile=1, persons_m=1)])}
    with pytest.raises(SystemExit, match="distributed_channel_inputs_finite"):
        W.channel_factors(I, "money")
