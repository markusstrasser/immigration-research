"""Exact matched-cash source cells, payer contract and pension-funding isolation."""
from copy import deepcopy
import hashlib
import io
import json

import numpy as np
import pandas as pd
import pytest

import mexico_pensions as M
import pension_cash as P
import world_ledger as W


@pytest.fixture(scope="module")
def artifact():
    return json.loads((P.HERE / "inputs/pension_cash_cells_oct15.json").read_text())


@pytest.fixture(scope="module")
def inputs(artifact):
    raw=artifact["results"]["set"]
    glines,vgen,val=P._value("oct15",raw,basis="set")
    pins=W.PINS["oct15"]
    channels=W.pinned_csv(pins["winners"],pins["dirs"]["winners"]+"/channels.csv").set_index("id")
    return dict(case="oct15",pension_basis="full_accrual",glines=glines,vgen=vgen,val=val,
                specs=pd.DataFrame(raw["specs"]).set_index("band_end"),ch=channels,
                gen=pd.read_csv(io.StringIO(raw["generation_results_csv"])),
                mxb=pd.DataFrame([dict(item="pensions paid",bn=7.5),dict(item="health",bn=2.0)]))


@pytest.fixture(scope="module")
def cash_values(artifact):
    return P._value("oct15", artifact["results"]["cash"])


@pytest.fixture(scope="module")
def cash_builder(inputs, cash_values):
    def build(case, raw, basis):
        return ((inputs["glines"], inputs["vgen"], inputs["val"])
                if basis == "set" else cash_values)
    return build


@pytest.fixture(scope="module")
def cash(inputs, cash_builder):
    return P.adapt_cash(inputs, valuation_builder=cash_builder)


def test_exact_cash_source_cells_reproduce_live_principal(artifact, cash_values):
    raw=artifact["results"]["cash"]
    assert artifact["case"]=="oct15" and artifact["package_set"]=="cash"
    assert artifact["mode"]=="exact_package_cash"
    assert raw["ends"]==[16,11]
    assert raw["oracle_bn"]==pytest.approx([281.752564,371.942418],abs=1e-6,rel=0)
    glines,vgen,val=cash_values
    checks=P._closure(raw,glines,vgen,val)
    assert max(checks.values())<1e-6
    assert len(artifact["sources"])>0
    assert all(len(r["sha256"])==64 for r in artifact["sources"])
    for end,spec in zip(("low","high"),raw["specs"]):
        assert spec["A_bn"]+spec["P_bn"]+spec["F_bn"]==pytest.approx(-spec["cost_bn"],abs=1e-9,rel=0)
        assert val[val.end.eq(end)].net_cost_bn.sum()==pytest.approx(-spec["A_bn"],abs=1e-9,rel=0)


def test_cash_adapter_uses_pooled_payers_and_no_v7_financing(inputs, cash):
    before=deepcopy(inputs)
    assert cash["financing_basis"]=="pooled_no_debt_split"
    assert cash["pension_basis"]=="matched_cash"
    assert cash["pension_meta"]["financing"]=={}
    assert cash["pension_meta"]["full_accrual_status"].startswith("[BLOCKED]")
    assert cash["pension_cash_adapter"]["artifact_key"]=="oct15_cash"
    for end in ("low","high"):
        assert np.isnan(cash["ch"].loc["future_taxpayers",f"bn_{end}"])
        assert cash["ch"].loc[["fiscal","displaced_beneficiaries","wages"],f"bn_{end}"].sum()==pytest.approx(
            -cash["specs"].loc[end,"cost_bn"],abs=1e-6,rel=0)
    for name in ("glines","vgen","val","specs","ch","gen","mxb"):
        pd.testing.assert_frame_equal(inputs[name],before[name])


def test_p032_funding_does_not_change_recipient_value(inputs, cash, cash_builder):
    central=cash
    for share in (0.0,0.5,1.0):
        arm=P.adapt_cash(inputs,public_pension_share=share,valuation_builder=cash_builder)
        pd.testing.assert_series_equal(arm["mxb"].recipient_bn,central["mxb"].recipient_bn)
        assert arm["mxb"].loc[0,"fiscal_bn"]==pytest.approx(7.5*share,abs=1e-12)
        pd.testing.assert_frame_equal(arm["vgen"],central["vgen"])
        assert arm["pension_meta"]["status"].startswith("[DEGRADED]")


def test_absent_receipt_cells_fail_before_world_reading(artifact):
    raw=deepcopy(artifact["results"]["cash"])
    raw["union_lines"]=[r for r in raw["union_lines"] if not(r["side"]=="receipt" and r["line"]=="federal_income_tax")]
    glines,vgen,val=P._value("oct15",raw)
    with pytest.raises(M.PensionBlocked,match="cash_generation_union_keys"):
        P._closure(raw,glines,vgen,val)


def test_stale_live_cash_artifact_is_rejected(inputs,tmp_path):
    source=P.HERE/"inputs/pension_cash_cells_oct15.json"
    bad=tmp_path/source.name
    bad.write_bytes(source.read_bytes()+b"changed")
    with pytest.raises(M.PensionBlocked,match="cash_source_artifact_stale"):
        P.adapt_cash(inputs,cells_path=bad)
    record=json.loads((P.HERE/"inputs/pension_cash_pins.json").read_text())["artifacts"]["oct15_cash"]
    assert record["sha256"]==hashlib.sha256(source.read_bytes()).hexdigest()
