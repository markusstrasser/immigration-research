"""v8 source-class conservation and public-reader regression controls."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("oct15_core_test_module", HERE / "winners_losers.py")
wl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wl)


def financing_fixture(monkeypatch):
    wl.CASE.clear()
    wl.CASE.update(model="live", debt="pinned", case="oct16")
    records = []
    classes = {"cash": (7., 3., 4.), "pension_accrual": (5., 5., 0.),
        "resource_cost": (2., 1., 1.), "displaced_beneficiaries": (1., .5, .5),
        "unlocated": (4., np.nan, np.nan), "private_production": (-3., 0., 0.)}
    for end in ("low", "high"):
        for convention in ("low", "central", "high"):
            for financing, (amount, federal, state_local) in classes.items():
                records.append(dict(basis="set", end=end, convention=convention, financing=financing,
                    responsive_bn=amount, federal_bn=federal, state_local_bn=state_local))
    raw = pd.DataFrame(records).to_csv(index=False, lineterminator="\n").encode()
    contract = json.dumps(dict(case="oct16", historical_stock_identified=False)).encode()
    monkeypatch.setattr(wl, "read_input", lambda key: raw if key == "debt_source_parts" else contract)
    return {"live": {"ends": {end: dict(cost_bn=16., A_bn=-21., F_bn=2.) for end in ("low", "high")}}}


def test_current_flow_keeps_unlocated_out_of_borrowing(monkeypatch):
    fin = financing_fixture(monkeypatch)
    result, info = wl.current_flow_split(fin)
    row = result[("live", "low", "central")]
    assert row["cost_bn"] == 19.
    assert row["federal_bn"] == 3.
    assert row["state_local_bn"] == 4.
    assert row["unlocated_bn"] == 4.
    assert row["accrual_bn"] == 5.
    assert row["source_production_bridge_bn"] == 0.
    assert "zero borrowing" in info["unlocated_rule"]


def test_current_flow_unknown_class_fails_loudly(monkeypatch):
    fin = financing_fixture(monkeypatch)
    original = wl.read_input
    monkeypatch.setattr(wl, "read_input", lambda key: original(key).replace(b"unlocated", b"unknown_class")
                        if key == "debt_source_parts" else original(key))
    with pytest.raises(SystemExit, match="financing_classes_declared"):
        wl.current_flow_split(fin)


def test_completed_members_do_not_receive_other_resident_wages():
    wl.CASE.clear()
    wl.CASE.update(current_flows_only=True)
    d = pd.DataFrame(dict(pw=[2., 3., 5., 7.], other=[True, False, True, False]))
    raw = np.array([10., 20., -4., -3.])
    B = SimpleNamespace(wage_delta=lambda *args: raw.copy())
    got = wl.payer_wage_delta(B, d, {}, {}, True)
    assert np.all(got[~d.other] == 0)
    for sign in (-1, 1):
        assert np.dot(d.pw, np.maximum(sign * got, 0)) == pytest.approx(np.dot(d.pw, np.maximum(sign * raw, 0)))


def test_live_parser_cannot_regenerate_oct14():
    assert wl.parse_args([]).case == "oct16"
    with pytest.raises(SystemExit):
        wl.parse_args(["--case", "oct14"])


def test_exported_trust_uses_fund_class_and_explicit_nontrust_timing():
    """A whole-case timing difference must not enter the payroll-payer block.

    The coverage profile calibration has a small nontrust set/cash movement.
    Treating the net difference as fund accrual loses it in the cohort frame,
    despite stationary arithmetic cancelling the mistaken classification.
    """
    exported_path = HERE / "derived/oct15/p7_trust_inputs.json"
    if not exported_path.exists():
        pytest.skip("generate current oct15 source exports before artifact regression")
    exported = json.loads(exported_path.read_text())
    source = pd.read_csv(HERE.parent / "debt_legacy_2026_09_23/derived/oct15/current_flow_source_parts_2024.csv")
    assert_exported_trust_scope(exported, source)
    wrong_scope = json.loads(json.dumps(exported))
    for end in ("low", "high"):
        wrong_scope["rows"][end]["accrual_bn"] = wrong_scope["timing_bridge"][end]["net_set_minus_cash_bn"]
    with pytest.raises(AssertionError):
        assert_exported_trust_scope(wrong_scope, source)
    missing_bridge = json.loads(json.dumps(exported))
    missing_bridge["timing_bridge"]["low"]["nontrust_timing_bridge_bn"] = 0.
    with pytest.raises(AssertionError):
        assert_exported_trust_scope(missing_bridge, source)


def assert_exported_trust_scope(exported, source):
    source = source[source.convention.eq("central")]
    for end in ("low", "high"):
        current = source[source.end.eq(end)]
        trust_rows = current[current.basis.eq("set") & current.financing.eq("pension_accrual")]
        parent = trust_rows.source_line.where(trust_rows.source_line.notna(), trust_rows.id.str.removesuffix(":set_minus_cash"))
        assert set(parent) <= {"federal_income_tax", "social_security", "medicare"}
        trust = float(trust_rows.responsive_bn.sum())
        totals = current.groupby("basis").responsive_bn.sum()
        net = float(totals["set"] - totals["cash"])
        component = current[current.side.eq("coverage") & current.id.eq("net_profile_calibration:set_minus_cash")]
        component_totals = component.groupby("basis").responsive_bn.sum()
        bridge = float(component_totals.get("set", 0.) - component_totals.get("cash", 0.))
        assert exported["rows"][end]["accrual_bn"] == pytest.approx(trust, rel=0, abs=1e-9)
        timing = exported["timing_bridge"][end]
        assert timing["trust_accrual_bn"] == pytest.approx(trust, rel=0, abs=1e-9)
        assert timing["net_set_minus_cash_bn"] == pytest.approx(net, rel=0, abs=1e-9)
        assert timing["nontrust_timing_bridge_bn"] == pytest.approx(bridge, rel=0, abs=1e-9)
        assert trust + bridge == pytest.approx(net, rel=0, abs=1e-9)
        assert "net_profile_calibration:set_minus_cash" in timing["source"]
        assert abs(trust - net) > .01
