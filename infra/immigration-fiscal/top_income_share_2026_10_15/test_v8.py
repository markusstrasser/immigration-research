"""Data-contract checks on the engine-priced arms, not a duplicate pricing implementation."""
import csv
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / "derived" / name).read_text())


def test_live_gate_and_baseline_principal():
    gates = read("v8_gates.json")["gates"]
    assert len(gates) >= 200 and all(g["pass"] for g in gates)
    rows = list(csv.DictReader((HERE / "derived/arms_v8.csv").open()))
    current = [r for r in rows if r["arm"] == "current"]
    assert len(current) == 4
    for r in current:
        assert float(r["cost_change_bn"]) == pytest.approx(0, abs=1e-12)
        expected = {("set", "low"): 365.7919302554848, ("set", "high"): 455.9817845889793,
                    ("cash", "low"): 281.75256367607324, ("cash", "high"): 371.9424180095669}
        assert float(r["cost_bn"]) == pytest.approx(expected[r["set"], r["end"]], abs=1e-9)


def test_prices_close_and_set_cash_tax_shifts_match():
    rows = list(csv.DictReader((HERE / "derived/arms_v8.csv").open()))
    for r in rows:
        delta = float(r["federal_cost_change_bn"]) + float(r["state_cost_change_bn"])
        assert float(r["cost_change_bn"]) == pytest.approx(delta, abs=1e-12)
        assert float(r["cost_bn"]) - float(r["baseline_bn"]) == pytest.approx(delta, abs=1e-9)
    by_arm = {}
    for r in rows:
        by_arm.setdefault(r["arm"], []).append(float(r["cost_change_bn"]))
    for values in by_arm.values():
        assert max(values) - min(values) < 1e-9


def test_isotonic_fit_preserves_total_upper_tail_mass():
    arms = read("federal_arms.json")["arms"]
    assert arms["pooled_monotone_central"]["share"] == pytest.approx(arms["pooled_unconstrained"]["share"], abs=1e-12)
    top = arms["pooled_monotone_central"]["upper_bin_shares"]
    assert top[0] >= top[1] >= top[2]
    assert arms["carry_500k"]["share_change"] < 0
    assert arms["fixed_1_5pct"]["share_change"] < arms["carry_500k"]["share_change"]
