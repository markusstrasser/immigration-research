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


@pytest.mark.parametrize("case", ["sept29", "oct15"])
def test_parity_live(legacy, case):
    """The engine union through this lane's path (group amounts, patched lines_at) gives the lane's 2024 legacy
    interest, 30.75 / 41.48bn, to 1e-6bn on the cash set."""
    D = legacy.D
    legacy.CASE = case
    ctx = legacy.setup()
    lines = pd.read_csv(DER / f"group_lines_{case}.csv")
    lane = pd.read_csv(legacy.LANE / "derived" / case / "stocks.csv")
    for end, printed in (("low", 30.75), ("high", 41.48)):
        sel = lines[(lines.group == "mexican_origin_engine") & (lines.basis == "cash") & (lines.end == end)]
        fed, _ = legacy.federal_path(ctx, "mexican_origin_engine", "cash", end, "central", sel, ctx["hist"].income)
        st = D.stock(D.History.nominal(ctx["hist"], fed), D.rate_paths()["effective"], 2005, 1.0)
        want = lane[(lane.benchmark == "main") & (lane.rule == D.CENTRAL["rule"]) & (lane.end == end)
                    & (lane.convention == "central") & (lane.rate_path == "effective") & (lane.window_start == 2005)
                    & (lane.financing == "all_borrowed")].legacy_interest_2024_bn.iloc[0]
        assert abs(st["legacy_interest_2024_bn"] - want) < 1e-6
        if case == "sept29":
            assert round(st["legacy_interest_2024_bn"], 2) == printed


@pytest.mark.parametrize("subdir", ["", "oct15"])
def test_parity_recorded(subdir):
    import json
    gates = json.loads((DER / subdir / "gates.json").read_text())
    assert gates["parity"]["max_abs_diff"] < 1e-6
    assert len(gates["parity"]["rows"]) == 12


@pytest.mark.parametrize("subdir", ["", "oct15"])
def test_sign_and_scale(subdir):
    m = pd.read_csv(DER / subdir / "legacy_main.csv")
    gates = __import__("json").loads((DER / subdir / "gates.json").read_text())
    at = lambda basis, g, end, w=2005: m[(m.basis == basis) & (m.group == g) & (m.end == end)  # noqa: E731
                                       & (m.window_start == w)].iloc[0]
    for end in ("low", "high"):
        for basis in ("cash", "accrual"):
            u, avg = at(basis, "mexican_origin_rough", end), at(basis, "all_residents_slice", end)
            assert u.interest_2024_bn > avg.interest_2024_bn
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


def test_v8_frame_derives_split_and_requires_complete_debt_count(legacy):
    meta = {"population_v8": {"with_coverage": 44_000_000, "without_coverage": 43_000_000,
                             "completion": 1_000_000, "coverage": 1_000_000},
            "union_completion": {"counts": {"baseline_account_union": 39_000_000,
                "baseline_lineage_population": 42_000_000, "reporting_union": 39_900_000,
                "reporters": 900_000, "nonreporters": 100_000, "added_lineage": 100_000,
                "lineage_population": 43_000_000, "by_generation": {"G3plus": 1_000_000}}}}
    result = legacy.complete_population_split(meta, 44)
    assert result == dict(account_union=40_900_000, added=3_100_000, lineage_population=44_000_000)
    with pytest.raises(SystemExit, match="debt member_count"):
        legacy.complete_population_split(meta, 43)
    meta["population_v8"]["coverage"] += .000002
    with pytest.raises(SystemExit, match="do not close"):
        legacy.complete_population_split(meta, 44)


def test_live_comparison_contract_rejects_mixed_engines(legacy):
    C = legacy.COMPARISON
    C.require_same_engine({"engine": C.engine_for("mexican_origin_rough")},
                          {"engine": C.engine_for("A1_third_plus_nh_white")})
    with pytest.raises(SystemExit, match="different engine tags"):
        C.require_same_engine({"engine": C.engine_for("mexican_origin_engine")},
                              {"engine": C.engine_for("A1_third_plus_nh_white")})


def test_base_mortality_metadata_inherits_general_and_rejects_other_conventions():
    spec = importlib.util.spec_from_file_location("legacy_line_metadata_probe", HERE / "group_lines.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    general = module.MORTALITY.GENERAL
    assert module.annual_mortality_label([{"mortality_convention": general}] * 2) == general
    for rows in ([], [{}], [{"mortality_convention": module.MORTALITY.MIXED}],
                 [{"mortality_convention": general}, {"mortality_convention": module.MORTALITY.OWN}]):
        with pytest.raises(SystemExit, match="authoritative whole-population mortality"):
            module.annual_mortality_label(rows)


def test_recorded_live_differences_are_same_engine_and_bridge_is_separate():
    diffs = pd.read_csv(DER / "oct15/legacy_differences.csv")
    assert set(diffs.union) == {"mexican_origin_rough"}
    assert (diffs.lineage_engine == diffs.comparator_engine).all()
    assert set(diffs.lineage_engine) == {"rough"}
    assert set(diffs.mortality_convention) == {"whole-population mortality"}
    bridges = pd.read_csv(DER / "oct15/case_rough_stock_bridge.csv")
    assert set(bridges.row_type) == {"bridge"}
    assert set(bridges.lineage_engine) == {"case"}
    assert set(bridges.comparator_engine) == {"rough"}
