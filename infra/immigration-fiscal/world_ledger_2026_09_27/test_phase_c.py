"""Pin tampering, unknown financing and source-side carrier regression checks."""
import json
import subprocess
from types import SimpleNamespace
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import committed_inputs as C
import debt_current as D
import valuation as V


def test_pin_must_match_working_file(monkeypatch, tmp_path):
    (tmp_path / "input.csv").write_bytes(b"changed\n")
    monkeypatch.setattr(C.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout=b"pinned\n"))
    with pytest.raises(SystemExit, match="pin does not match file"):
        C.checked_bytes("commit", "input.csv", repo=tmp_path)
    (tmp_path / "input.csv").write_bytes(b"pinned\n")
    assert C.checked_bytes("commit", "input.csv", repo=tmp_path) == b"pinned\n"


def split_rows():
    return pd.DataFrame([dict(basis="set", convention="central", end=end, financing=financing,
                             responsive_bn=amount, federal_bn=federal, state_local_bn=state)
                         for end in ("low", "high")
                         for financing, amount, federal, state in (("cash", 9., 4., 5.),
                                                                   ("unlocated", 1., np.nan, np.nan))])


def test_unlocated_split_never_sums_missing_government_to_zero():
    parts = D.map_parts(split_rows(), [10., 10.], "set")
    assert parts.status.eq("[BLOCKED: no oct15 federal split]").all()
    assert parts.unlocated_bn.eq(1.).all()
    assert parts.federal_bn.eq(4.).all()
    assert parts.state_local_bn.eq(5.).all()


def test_debt_total_gate_is_absolute_micro_billion():
    with pytest.raises(SystemExit, match="do not match case"):
        D.map_parts(split_rows(), [10.000002, 10.], "set")


def test_undeclared_missing_financing_stops():
    rows = split_rows()
    rows.loc[rows.financing.eq("cash"), "federal_bn"] = np.nan
    with pytest.raises(SystemExit, match="undeclared missing"):
        D.map_parts(rows, [10., 10.], "set")


def test_unknown_financing_category_cannot_be_called_identified():
    rows = split_rows()
    rows.loc[rows.financing.eq("cash"), "financing"] = "cash_v2"
    with pytest.raises(SystemExit, match="unknown financing category"):
        D.map_parts(rows, [10., 10.], "set")


def test_finite_but_wrong_government_shares_stop():
    rows = split_rows()
    rows.loc[rows.financing.eq("cash"), "federal_bn"] += 1.
    with pytest.raises(SystemExit, match="government shares do not close"):
        D.map_parts(rows, [10., 10.], "set")


def test_capital_uses_registry_stock_by_id_and_accepts_zero_response():
    module = Path(__file__).with_name("capital_amount.cjs")
    js = """const {capitalAmount}=require(process.argv[1]);
const registry={rates:{low:.02},components:[{id:'other',stock_charged_bn:999},{id:'x',stock_charged_bn:100}]};
if(capitalAmount({id:'x',key:.5,response:0,return_bn:0},registry,'low')!==1)process.exit(1);
for(const c of [{id:'missing',key:1,response:1,return_bn:0},{id:'x',key:NaN,response:1,return_bn:0}]) {
let rejected=false;try{capitalAmount(c,registry,'low');}catch(e){rejected=true;}if(!rejected)process.exit(2);}
"""
    subprocess.run(["node", "-e", js, str(module)], check=True)


def test_capital_completion_inherits_offset_class(monkeypatch):
    monkeypatch.setitem(V.ITEM_CLASS, "capital_fixture_offset", "education")
    payload = {"meta": {"union_completion": {"carriers": {"new": {
        "kind": "capital", "parent_line": "fixture_offset"}}}}}
    assert V.completion_incidence(payload, {}, {})["new"]["incidence_class"] == "education"


def test_v8_does_not_repeat_inherited_child_credit_adjustment():
    assert V.child_credit_adjustments("oct15", pd.DataFrame()) == {}


def test_signed_receipt_carrier_preserves_incidence_and_debit(monkeypatch):
    name = "fixture_signed_receipt"
    monkeypatch.setitem(V.ITEM_CLASS, name, "tax")
    monkeypatch.setitem(V.CARRIER_PAYER, name, "group_filers")
    monkeypatch.setattr(V, "CARRIER_RECEIPTS", {name})
    row = SimpleNamespace(side="spending", line=name, amount_bn=-3., response=1., effect_bn=3.)
    valued = V.valuation_row(row, {}, {})
    assert valued["receipt_incidence_class"] == "tax"
    assert valued["economic_payer"] == "group_filers"
    assert valued["V_central_bn"] == -3.


def test_coverage_tax_parent_and_authorized_residual_mix(monkeypatch, tmp_path):
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    parts = [dict(generation="G1", line="tax", source_line="tax", source_side="receipt",
                  economic_class="fiscal_line", coverage_bn=-2.),
             dict(generation="G1", line="residual", economic_class="unclassified_residual", coverage_bn=1.)]
    payload = {"meta": {"coverage": {"by_end": {"low": {"decomposition": {"line_parts": parts}}}}}}
    lines = pd.DataFrame([dict(end="low", side="coverage", line=f"coverage_{i}_G1_{p['line']}",
                               amount_bn=p["coverage_bn"], response=1., effect_bn=-p["coverage_bn"])
                          for i, p in enumerate(parts)])
    monkeypatch.setattr(V, "receipt_contract", lambda case: ({"tax": "tax"}, {"tax": "group_filers"}))
    donors = pd.DataFrame([dict(band_end="low", generation="G1", side="spending", line="social_security",
                                amount_bn=10., response=1., effect_bn=-10.)])
    V.prepare_coverage_values("oct15", donors, lines, payload=payload)
    result = pd.read_csv(tmp_path / "coverage_valuation_contract_oct15.csv")
    assert result.loc[0, "incidence_class"] == "tax"
    assert result.loc[1, "incidence_class"] == "proportional_mix"
