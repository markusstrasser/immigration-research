"""Live-only dispatch and fail-loud input gates, without rebuilding any case or consuming candidate outputs."""
import sys

import pandas as pd
import pytest

import beside_extra as E
import split_residual as S
import valuation as V
import cash_readings as CR


def test_live_valuation_does_not_rebuild_historical_cases(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["valuation.py"])
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    monkeypatch.setattr(V, "require_pins", lambda *a: None)
    monkeypatch.setattr(V, "mexico_budget", lambda b: pd.DataFrame({"cls": ["tax"], "bn": [1.0]}))
    calls = []
    monkeypatch.setattr(CR, "prepare", lambda case: calls.append([case]))
    V.main()
    assert calls == [["oct16"]]
    assert not list(tmp_path.glob("valuation*oct07*"))


def test_missing_oct14_pins_never_fall_back_to_previous_case(monkeypatch):
    monkeypatch.setitem(V.PINS, "oct14", {"winners": None, "distribution": None, "generation": None,
                                        "main_case": None})
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] oct14: missing committed winners/distribution/generation/main_case"):
        V.require_pins("oct14", "winners", "distribution", "generation")


def test_missing_debt_split_stops_with_live_path(monkeypatch, tmp_path):
    monkeypatch.setattr(E, "CASE", "oct14")
    monkeypatch.setattr(E, "SPLIT", tmp_path / "oct14" / "federal_split_2024.csv")
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] oct14: missing live debt split"):
        E.fiscal_parts()


def test_debt_gate_uses_absolute_micro_billion_tolerance(monkeypatch, tmp_path):
    monkeypatch.setattr(E, "CASE", "oct14")
    split = tmp_path / "federal_split_2024.csv"
    pd.DataFrame({"profile": [E.SPLIT_PROFILE] * 2, "convention": ["central"] * 2,
                  "end": ["low", "high"], "net_cost_bn": [338.001, 422.0]}).to_csv(split, index=False)
    monkeypatch.setattr(E, "SPLIT", split)
    monkeypatch.setattr(E.W, "require_pins", lambda *a: None)
    monkeypatch.setattr(E.W, "git_show", lambda *a: '{"v7": {"band_bn": [338.0, 422.0]}}')
    with pytest.raises(SystemExit, match="split_is_the_case"):
        E.fiscal_parts()


def test_low_end_residual_replays_personal_cells(monkeypatch, tmp_path):
    """Shared shifts differ by 100x: assigning low to shared would fail the correction-replay gate."""
    monkeypatch.setattr(S, "DERIVED", tmp_path)
    monkeypatch.setattr(sys, "argv", ["split_residual.py", "--case", "oct15"])
    monkeypatch.setattr(S, "require_pins", lambda *a: None)
    monkeypatch.setitem(S.PINS, "oct15", dict(S.PINS["oct15"], generation="fixture"))
    models, payloads = {}, {}
    for i, gen in enumerate(S.GENS, 1):
        models[gen] = {"receipts": {"lines": [{"id": "corporate_capital", "national_bn": 100,
            "cells": {"reference": {"personal": {"target_bn": i}, "shared": {"target_bn": 10 * i}}}}]}}
        payloads[gen] = {"edits": [{"side": "receipt", "line": "corporate_capital", "scenario": "reference",
                                   "by": {"personal": 1, "shared": 100}}]}
    monkeypatch.setattr(S, "git_json", lambda pin, rel: {"payloads": {"a": payloads}}
                        if "corrections" in rel else next(models[g] for g in S.GENS if f"model_{g}.json" in rel))
    for corrected in (True, False):
        rows = []
        for end, spec, response in (("low", 16, 1.0), ("high", 11, 0.37)):
            for i, gen in enumerate(S.GENS, 1):
                amount = i + int(corrected)
                head = {"band_end": end, "spec": spec, "allocation": "personal", "generation": gen}
                rows.append(dict(head, side="receipt", line="corporate_capital", key="reference:corporate",
                                 amount_bn=amount, response=response, effect_bn=amount * response))
                post = 0.75 * int(corrected)
                for line, value in (("mixed_unit_removal", 0.25 * int(corrected)), ("coverage", 0.5 * int(corrected))):
                    rows.append(dict(head, side="post_engine", line=line, key="", amount_bn=value, response=1,
                                     effect_bn=-value))
                for line, effect in (("direct_fiscal", -amount * response), ("capital_return", 0), ("post_engine", post)):
                    rows.append(dict(head, side="total", line=line, key="", amount_bn=0, response=0,
                                     effect_bn=effect))
        suffix = "" if corrected else "_uncorrected"
        pd.DataFrame(rows).to_csv(tmp_path / f"generation_lines{suffix}_oct15.csv", index=False, lineterminator="\n")
    S.main()
    out = pd.read_csv(tmp_path / "generation_split_residual_oct15.csv")
    assert len(out) == 18
    assert set(out.allocation) == {"personal"}
    assert out[out.side.eq("receipt")].groupby("band_end").lane_bn.sum().to_dict() == {"high": -3.33, "low": -9.0}
    assert out[out.side.eq("post_engine")].groupby("band_end").lane_bn.sum().to_dict() == {"high": 2.25, "low": 2.25}
