"""Basis/receipt, paired quantity and funding invariants for current readings."""
import numpy as np
import json
import pandas as pd
import pytest

import beside_arms as B
import cash_readings as C


def test_missing_receipt_cell_stops():
    I = dict(pension_basis="matched_cash", us_pension_basis="cash", pension_cash_adapter={"verified": True},
             glines=pd.DataFrame([dict(band_end="low", generation="G1", side="receipt", line="tax")]),
             vgen=pd.DataFrame([dict(end="low", generation="G1", side="spending", line="benefit", receipt_incidence_class="not_receipt")]))
    with pytest.raises(SystemExit, match="reading_receipt_cells_complete"):
        C.cash_contract(I)


def test_funding_does_not_change_recipient_values():
    m = pd.DataFrame([dict(item="pensions paid in Mexico", recipient_value_bn=4., recipient_value_pesos_bn=40.,
        fiscal_cost_bn=4., fiscal_cost_pesos_bn=40., source_pesos_bn=40.)])
    for share in (1., .5, 0.):
        out = C.pension_share(dict(mxb=m), share)["mxb"]
        assert out.recipient_value_bn.tolist() == [4.]
        assert out.recipient_value_pesos_bn.tolist() == [40.]
        assert out.fiscal_cost_bn.tolist() == [share*4.]


@pytest.mark.parametrize("end,value", [("low", 3.), ("high", 7.)])
def test_care_endpoint_matches_provider_quantity(monkeypatch, end, value):
    monkeypatch.setattr(B.W, "population_shares", lambda I: {"pop": {g: 1/3 for g in B.W.GENS}})
    import mexico_prices as M
    monkeypatch.setattr(M, "budget_values", lambda *a: ({}, {}, dict(low=0., central=0., high=0.)))
    rows = pd.DataFrame([dict(row=f"{kind}_{g}", low=0., central=0., high=0.)
                        for g in B.W.GENS for kind in ("uncompensated_received", "mexico_budget_lost")])
    ch = pd.DataFrame([dict(bn_low=-3., bn_central=-5., bn_high=-7.)], index=["unreimbursed_care"])
    out = B.health_rows(rows, dict(account_end=end, health_vg=(1.,)*3, ch=ch, mxb=None), "average_cost", care_vg=(1.,)*3)
    assert out[out.row.str.startswith("uncompensated_received")].central.sum() == pytest.approx(value)


def test_executed_readings_contract():
    path = C.V.DERIVED/"readings_cash_oct15.csv"
    if not path.exists():
        pytest.skip("numerical producer has not run yet")
    f = pd.read_csv(path)
    a = f[f.scope.eq("A_completed")]
    b = f[~f.scope.eq("A_completed")]
    assert len(a) == 288 and len(b) == 96
    keys = ["scope", "reading", "public_pension_share", "end", "g3_bound", "weighting"]
    assert not f.duplicated(keys).any()
    assert np.allclose(a.world_total_bn, a.group_total_bn+a.other_us_residents_bn+a.mexico_residents_bn, atol=1e-9, rtol=0)
    assert b.world_total_bn.isna().all() and not b.enters_total.any()
    for _, g in a.groupby(["reading", "end", "g3_bound", "weighting"]):
        assert g.group_total_bn.max()-g.group_total_bn.min() < 1e-9
        assert g.other_us_residents_bn.max()-g.other_us_residents_bn.min() < 1e-9
def test_component_expansion_has_one_scalar_receipt_per_component():
    parts = [dict(line="social_security", component_side="spending", cls="cash", G_bn=2., V_central_bn=2.),
             dict(line="federal_income_tax", component_side="receipt", cls="tax", G_bn=-1., V_central_bn=-1.)]
    raw = pd.DataFrame([dict(end="low", line="coverage_fixture_lane_residual", net_cost_bn=1.,
                            recipient_components_json=json.dumps(parts))])
    out = C.recipient_cells(raw, pd.DataFrame(columns=["end", "line"]))
    assert len(out) == 2 and "recipient_components_json" not in out
    assert out.net_cost_bn.sum() == 1. and out.V_central_bn.sum() == 1.


