"""Scratch regression probes, no lane mutations."""
from pathlib import Path
import importlib.util
import math
import sys
import copy
import json

import pandas as pd
import pytest

sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location("capital_source", Path(__file__).with_name("capital_source.py"))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

project_spec = importlib.util.spec_from_file_location("mexico_capital_test", Path(__file__).with_name("mexico_capital.py"))
C = importlib.util.module_from_spec(project_spec)
project_spec.loader.exec_module(C)


def input_projection():
    sectors = pd.read_csv(C.checked_input("capital-enigh-industry.csv"), dtype={"sector": str}).sector
    values = {sector: (10.0 if sector == "11" else 0.0) for sector in sectors}
    values["__TOTAL_CASH__"] = 20.0
    return {gen: dict(values) for gen in ("G1", "G2", "G3+")}


def test_wrapper_pure_central_pay_fixed_across_fiscal_ends_and_receipts():
    I = {"capital_projected_gen_industry_wages": input_projection(), "account_end": "low"}
    prem = {gen: {"cash_mx": {"low": 1.0, "central": 2.0, "high": 99.0}, "mexico_ppp_divisor": 10.0}
            for gen in ("G1", "G2", "G3+")}
    before = copy.deepcopy(I)
    low = C.mexico_source_tax(I, prem, "low")
    assert I == before
    I["account_end"] = "high"
    high = C.mexico_source_tax(I, prem, "high")
    assert high["industry_wages_mxn"] == low["industry_wages_mxn"]
    assert math.isclose(high["pesos_bn"], .37 * low["pesos_bn"], rel_tol=1e-12)
    assert low["national_corporate_receipts_pesos_bn"] == 1154.322
    assert low["raw_subordinate_fractions"] == {gen: .5 for gen in prem}
    assert math.isclose(sum(low["industry_wages_mxn"].values()), 30e9)


def test_source_input_hash_guard(tmp_path, monkeypatch):
    name = "capital-sat-sector-isr.csv"
    path = C.checked_input(name)
    pins = json.loads((C.INPUTS / "capital_pins.json").read_text())
    (tmp_path / name).write_bytes(path.read_bytes() + b"\n")
    (tmp_path / "capital_pins.json").write_text(json.dumps(pins))
    monkeypatch.setattr(C, "INPUTS", tmp_path)
    with pytest.raises(ValueError, match="stale capital input"):
        C.checked_input(name)


def test_old_frame_not_silently_used_for_oct15():
    with pytest.raises(ValueError, match="explicit completed capital_people"):
        C.projected_shapes({"case": "oct15", "basis": "lineage"})


def test_source_numeric_rules():
    shares = {"manufacturing": 0.2, "mining": 0.7}
    taxes = {"corporate": {"manufacturing": 100.0, "mining": 1000.0}}
    responses = {"corporate": {"low": 1.0, "high": 0.37}}
    r = S.source_taxes(shares, taxes, responses, ["mining"])
    assert r["total"] == {"low": 20.0, "high": 7.4}
    scaled = {line: {sector: tax * 3 for sector, tax in values.items()} for line, values in taxes.items()}
    rs = S.source_taxes(shares, scaled, responses, ["mining"])
    assert all(math.isclose(rs["total"][rd], 3 * r["total"][rd]) for rd in r["total"])
    for premise in ("short_run_fixed_capital", "output_mix_no_new_capital"):
        assert all(v == 0 for v in S.source_taxes(shares, taxes, responses, ["mining"], premise)["total"].values())


def test_unknown_industry_stops():
    try:
        S.source_taxes({"a": 0.2}, {"corporate": {"b": 100}}, {"corporate": {"low": 1, "high": .37}})
    except ValueError as error:
        assert "[BLOCKED]" in str(error)
    else:
        raise AssertionError("missing wage industry did not stop")


def test_counterfactual_not_clamped_and_labor_not_removed():
    assert S.shares_from_wages({"a": 150.0}, {"a": 100.0}) == {"a": 1.5}
    r = S.foreign_parity_remainder(100, 35)
    assert r["rest_of_world_parity_high"] == 65
    assert "corporate_labor" in r["us_basis"]
    assert S.foreign_parity_remainder(100, 110)["mexico_exceeds_us_parity"] == 10


def test_only_thin_management_cell_pooled_and_government_mining_zero():
    national = {"21": 100.0, "93": 100.0, "52": 100.0, "54": 100.0, "55": 10.0}
    group = {"21": 20.0, "93": 20.0, "52": 10.0, "54": 30.0, "55": 10.0}
    tax = {key: 100.0 for key in national}
    r = S.mexico_corporate_source(group, national, tax, 0, residual_policy="pooled_private",
                                 pool_sectors=("52", "54", "55"))
    parts = r["lines"]["corporate"]["by_industry"]
    assert parts["52"] == 10.0 and parts["54"] == 30.0
    assert math.isclose(parts["55"], 100 * 50 / 210)
    assert parts["21"] == parts["93"] == 0.0
    assert S.mexico_corporate_source(group, national, tax, 0, residual_policy="pooled_private",
                                    premise="output_mix_no_new_capital")["total"] == {"low": 0.0, "high": 0.0}


if __name__ == "__main__":
    test_source_numeric_rules()
    test_unknown_industry_stops()
    test_counterfactual_not_clamped_and_labor_not_removed()
    test_only_thin_management_cell_pooled_and_government_mining_zero()
    print("PASS: source rules, scale, missing industry stop, counterfactual ratio, foreign remainder")
