"""Zero-response public-good recipient transport and inactive carrier regressions."""
import json

import numpy as np
import pandas as pd
import pytest

import coverage_recipient_values as R
import pension_cash as P
import valuation as V


def test_native_price_transport_equals_donor_cell_mean_transport():
    # Canonical dose is constant inside each age/sex/generation cell. A direct
    # donor price transport therefore equals weighted cell-mean transport.
    driver = np.array([1., 4., 2., 3.])
    counted = np.array([2., 3., 5., 7.])
    dose = np.array([.1, .1, -.02, -.02])
    missed = counted * dose
    amount = 12.0
    price = amount * driver / (driver @ counted)
    expected = sum((price[m] @ counted[m]) / counted[m].sum() * missed[m].sum()
                   for m in (np.array([True, True, False, False]), np.array([False, False, True, True])))
    assert R.transport_price(driver, counted, missed, amount) == pytest.approx(expected, abs=1e-12)
    with pytest.raises(SystemExit, match="nonfinite"):
        R.transport_price(np.array([np.nan]), np.ones(1), np.ones(1), 1.)


@pytest.fixture(scope="module")
def cash_values():
    artifact = json.loads((V.HERE / "inputs/pension_cash_cells_oct15.json").read_text())
    return P._value("oct15", artifact["results"]["cash"])


def test_inactive_alternative_carrier_has_no_recipient_value(cash_values):
    _, _, union = cash_values
    inactive = union[union.line.eq("union_completion_general_public_services_wages")]
    assert len(inactive) == 2
    assert inactive.amount_bn.ne(0).all()
    assert inactive.response.eq(0).all()
    assert inactive[["V_low_bn", "V_central_bn", "V_high_bn", "net_cost_bn"]].eq(0).all().all()
    defense = union[union.line.eq("defense")]
    assert defense.response.eq(0).all()
    assert defense.V_central_bn.gt(0).all()


def test_live_recipient_supplement_changes_no_fiscal_cell(cash_values):
    _, generations, _ = cash_values
    I = dict(case="oct15", vgen=generations)
    out = R.supplement(I, "oct15", "cash")
    original = out["vgen"].iloc[:len(generations)]
    pd.testing.assert_frame_equal(original[generations.columns].reset_index(drop=True), generations.reset_index(drop=True))
    extra = out["vgen"].iloc[len(generations):]
    assert set(extra.line) >= {"defense", "roads_vmt_fed"}
    assert extra.origin_line.str.startswith("coverage_").all()
    assert extra[["amount_bn", "G_bn", "net_cost_bn", "source_tax_credit_bn"]].eq(0).all().all()
    assert extra[extra.line.eq("defense")].groupby("end").V_central_bn.sum().gt(0).all()
    assert extra.groupby("end").net_cost_bn.sum().eq(0).all()
    assert "peak_physical_bytes" not in out["coverage_recipient_supplement"]
    assert "elapsed_seconds" not in out["coverage_recipient_supplement"]
