"""Parity with the debt legacy lane, and sign and scale checks on the comparators' legacies.

  uv run python3 -m pytest infra/immigration-fiscal/legacy_comparators_2026_09_30/ -q
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
DER = HERE / "derived"


@pytest.fixture(scope="module")
def legacy():
    spec = importlib.util.spec_from_file_location("legacy_comparators", HERE / "legacy.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["legacy_comparators"] = module
    spec.loader.exec_module(module)
    return module


def test_parity_live(legacy):
    """The engine union through this lane's path (group amounts, patched lines_at) gives the lane's 2024 legacy
    interest, 30.75 / 41.48bn, to 1e-6bn on the cash set."""
    D = legacy.D
    ctx = legacy.setup()
    lines = pd.read_csv(DER / "group_lines_sept29.csv")
    lane = pd.read_csv(legacy.LANE / "derived/sept29/stocks.csv")
    for end, printed in (("low", 30.75), ("high", 41.48)):
        sel = lines[(lines.group == "mexican_origin_engine") & (lines.basis == "cash") & (lines.end == end)]
        fed, _ = legacy.federal_path(ctx, "mexican_origin_engine", "cash", end, "central", sel, ctx["hist"].income)
        st = D.stock(D.History.nominal(ctx["hist"], fed), D.rate_paths()["effective"], 2005, 1.0)
        want = lane[(lane.benchmark == "main") & (lane.rule == D.CENTRAL["rule"]) & (lane.end == end)
                    & (lane.convention == "central") & (lane.rate_path == "effective") & (lane.window_start == 2005)
                    & (lane.financing == "all_borrowed")].legacy_interest_2024_bn.iloc[0]
        assert abs(st["legacy_interest_2024_bn"] - want) < 1e-6
        assert round(st["legacy_interest_2024_bn"], 2) == printed


def test_parity_recorded():
    import json
    gates = json.loads((DER / "gates.json").read_text())
    assert gates["parity"]["max_abs_diff"] < 1e-6
    assert len(gates["parity"]["rows"]) == 12


def test_sign_and_scale():
    m = pd.read_csv(DER / "legacy_main.csv")
    gates = __import__("json").loads((DER / "gates.json").read_text())
    at = lambda basis, g, end, w=2005: m[(m.basis == basis) & (m.group == g) & (m.end == end)  # noqa: E731
                                       & (m.window_start == w)].iloc[0]
    for end in ("low", "high"):
        for basis in ("cash", "accrual"):
            u, avg = at(basis, "mexican_origin_rough", end), at(basis, "all_residents_slice", end)
            assert u.interest_2024_bn > avg.interest_2024_bn > 0
        # accrual: the 2024 account ranks union > average > third-plus whites; the legacy keeps that order
        assert at("accrual", "all_residents_slice", end).interest_2024_bn > at("accrual", "A1_third_plus_nh_white", end).interest_2024_bn
    # interest is the 2024 effective rate on the stock; per member divides by the row-4 count
    # (the rate is written to 6 decimals, so the tolerance scales with the stock)
    assert ((m.interest_2024_bn - m.rate_2024 * m.stock_entering_2024_bn).abs()
            < 5e-7 * m.stock_entering_2024_bn.abs() + 1e-5).all()
    assert ((m.interest_per_member_usd - m.interest_2024_bn * 1e3 / gates["member_count_m"]).abs() < 1e-2).all()
    # no stock above 15% of debt held by the public entering FY2024
    assert (m.stock_entering_2024_bn.abs() < 0.15 * gates["debt_held_by_public_end_fy2023_bn"]).all()
    # the 2024 flow does not depend on the window
    assert m.groupby(["group", "basis", "end"]).federal_flow_2024_bn.nunique().max() == 1
