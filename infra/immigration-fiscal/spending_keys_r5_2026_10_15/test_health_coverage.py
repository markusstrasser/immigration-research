"""Deterministic price transport checks independent of the item21 amount fit."""
import sys

sys.dont_write_bytecode = True

import numpy as np
import pytest
from types import SimpleNamespace

import health_coverage

from health_coverage import add_ends, build, capital_rate_pieces, integrate, rekey_piece_prices, validate_pieces


def fixture():
    data = {"generation": np.array([0, 0, 1, 2]), "weights": np.array([[2.], [3.], [4.], [5.]]),
            "added_weights": np.array([[0.], [0.], [0.], [2.]])}
    old = np.array([.2, .4, 0., 0.])
    data["base_piece_prices"] = np.array([old])
    data["constructed_piece_prices"] = np.array([old])
    p = {"end": "low", "generation": "G1", "line": "health_services",
         "source_line": "health_services", "source_side": "spending",
         "economic_class": "fiscal_line", "category": "health", "level": "unclassified"}
    return data, {"denominator_pieces": [p]}


def test_rekey_uses_raw_driver_and_observed_amount_not_generation_mean():
    data, audit = fixture()
    p = rekey_piece_prices(data, audit, 0, np.array([1., 3., 8., 9.]), 2.2, old_factor=.5)
    # Raw mass 2*1+3*3=11 => new prices .2/.6; old residual .1/.2.
    assert np.allclose(p["base_price"], [.1, .4, 0, 0], atol=1e-15)
    assert np.array_equal(p["base_price"], p["constructed_price"])
    validate_pieces([p], data)
    assert abs(float(p["base_price"] @ data["weights"][:, 0]) - 1.4) < 1e-12


def test_typed_fiscal_and_capital_plus_population_scopes():
    data, audit = fixture()
    p = rekey_piece_prices(data, audit, 0, np.ones(4), 1.6)
    cal = {**p, "line": "added_calibration", "generation": "G3plus", "population": "added",
           "base_price": np.array([0., 0., 0., .3]), "constructed_price": np.array([0., 0., 0., .3])}
    capital = {**cal, "line": "health_capital", "economic_class": "capital_return", "level": "state_local"}
    z = integrate([p, cal, capital], np.array([1., 0., 0., 10.]), np.array([0., 0., 0., 2.]), basis="cash")["low"]
    assert z["by_generation_bn"]["G3plus"] == pytest.approx(1.2)
    assert z["decomposition"]["capital_by_level_bn"]["state_local"] == pytest.approx(.6)
    assert z["total_bn"] == pytest.approx(sum(z["by_generation_bn"].values()))
    assert z["decomposition"]["classified_cash_fiscal_bn"] == pytest.approx(z["total_bn"]-.6)


def test_generation_leak_and_duplicate_identity_fail():
    data, audit = fixture()
    p = rekey_piece_prices(data, audit, 0, np.ones(4), 1.6)
    with pytest.raises(ValueError, match="duplicate price-piece"):
        validate_pieces([p, p], data)
    leaked = {**p, "base_price": np.ones(4)}
    with pytest.raises(ValueError, match="leak outside"):
        validate_pieces([leaked], data)


def test_conditional_item17_is_joint_minus_item16():
    a = {e: {"by_generation_bn": {"G1": 1., "G2": 3., "G3plus": 5.}} for e in ("low", "high")}
    b = {e: {"by_generation_bn": {"G1": .5, "G2": 2., "G3plus": 4.}} for e in ("low", "high")}
    conditional = add_ends(a, b, -1)
    assert conditional["low"] == {"total_bn": 2.5, "by_generation_bn": {"G1": .5, "G2": 1., "G3plus": 1.}}


def test_missing_driver_mass_blocks_nonzero_amount():
    data, audit = fixture()
    with pytest.raises(ValueError, match="no raw driver mass"):
        rekey_piece_prices(data, audit, 0, np.zeros(4), 1.)


def test_zero_delta_full_source_coverage_and_count_route():
    def unchanged(data, audit, basis, vintage):
        return [{**p, "base_price": np.zeros_like(data["age"], dtype=float),
                 "constructed_price": np.zeros_like(data["age"], dtype=float)}
                for p in audit["denominator_pieces"] if p["source_line"] == "health_services"]

    result = build(unchanged)
    assert set(result["sets"]) == {"set", "cash"}
    for data in result["sets"].values():
        for scenario in data["scenarios"].values():
            assert all(z["total_bn"] == 0 for z in scenario["ends"].values())
        for scenario in data["count_scenarios"].values():
            assert all(z["total_bn"] == 0 for z in scenario.values())
        assert data["count_parts"]
        for entry in data["item_overrides"].values():
            assert "population_change" not in entry
            assert all(z["total_bn"] == 0 for z in entry["by_end"].values())


def test_common_rate_only_changes_capital_and_preserves_source_arrays():
    data, audit = fixture()
    fiscal = rekey_piece_prices(data, audit, 0, np.ones(4), 1.6)
    capital = {**fiscal, "line": "health_capital", "economic_class": "capital_return", "level": "state_local"}
    original = capital["base_price"].copy()
    pieces = [fiscal, capital]
    assert capital_rate_pieces(pieces) is pieces
    changed = capital_rate_pieces(pieces, .025)
    assert changed[0] is fiscal
    assert np.array_equal(changed[1]["base_price"], original * 1.25)
    assert np.array_equal(capital["base_price"], original)
    with pytest.raises(ValueError, match="invalid common capital rate"):
        capital_rate_pieces(pieces, float("nan"))


def test_common_rate_recomputes_every_coverage_and_count_channel(monkeypatch):
    data, audit = fixture()
    data["age"] = np.array([10, 30, 50, 70])
    data["person_ph_seq"] = np.arange(4)
    data["person_pppos"] = np.ones(4)
    f = np.array([.1, .2, .3, .4])
    runtime = SimpleNamespace(
        load=lambda: ({}, {}), load_kernel=lambda basis, vintage: (data, audit),
        C=SimpleNamespace(factors=lambda data, rates, base, **options: (f, np.zeros(4))),
        DEFINITIONS={"central": {}, "arm": {}},
        person_inputs=lambda data: (np.ones(4), np.array([2., 1., 1., 1.])),
        item10_flags=lambda data, payload: {"nonreporter": np.zeros(4, bool)},
        fixed_count_tenure=lambda *args: (np.full(4, .2), []),
        transfer_count_tenure=lambda *args: np.full(4, .3),
    )
    monkeypatch.setattr(health_coverage, "source_runtime", lambda: runtime)

    def prices(data, audit, basis, vintage):
        p = audit["denominator_pieces"][0]
        return [{**p, "end": end, "line": name, "economic_class": kind, "level": level,
                 "base_price": np.array(vector), "constructed_price": np.array(vector)}
                for end in ("low", "high")
                for name, kind, level, vector in (
                    ("fiscal", "fiscal_line", "unclassified", [.1, .1, 0., 0.]),
                    ("capital", "capital_return", "state_local", [.2, .4, 0., 0.]))]

    original = build(prices, bases=("set",))["sets"]["set"]
    changed = build(prices, bases=("set",), capital_rate=.04)["sets"]["set"]
    for scenario, block in changed["scenarios"].items():
        for end, row in block["ends"].items():
            before = original["scenarios"][scenario]["ends"][end]
            factor = .04 / (.02 if end == "low" else .03)
            cap = before["decomposition"]["capital_by_level_bn"]["state_local"]
            assert row["total_bn"] == pytest.approx(before["total_bn"] + (factor-1)*cap)
            assert row["decomposition"]["classified_fiscal_line_bn"] == before["decomposition"]["classified_fiscal_line_bn"]
    for row, before in zip(changed["count_parts"], original["count_parts"], strict=True):
        factor = .04 / (.02 if row["end"] == "low" else .03) if row["economic_class"] == "capital_return" else 1.
        for field in ("observed_change_bn", "coverage_change_bn", "change_bn"):
            assert row[field] == pytest.approx(before[field] * factor)
    for end in ("low", "high"):
        for scenario, values in changed["count_scenarios"].items():
            parts = [r for r in changed["count_parts"] if r["scenario"] == scenario and r["end"] == end]
            assert values[end]["total_bn"] == pytest.approx(sum(r["change_bn"] for r in parts))
        assert changed["declared_item12_deltas_bn"][end]["health_residual_key"] == changed["ends"][end]["total_bn"]
        assert changed["ends"][end]["total_bn"] == pytest.approx(
            sum(changed["ends"][end]["adult_cost_by_generation_bn"].values())
            + sum(changed["ends"][end]["minor_cost_by_generation_bn"].values()))
        assert changed["item_overrides"]["native_minor_calibration"]["by_end"][end] == changed["count_scenarios"]["item16"][end]
        conditional = add_ends(changed["count_scenarios"]["joint"], changed["count_scenarios"]["item16"], -1)
        assert changed["item_overrides"]["coverage_tenure"]["by_end"][end] == conditional[end]
