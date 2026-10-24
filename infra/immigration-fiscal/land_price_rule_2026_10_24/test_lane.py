"""Checks on the land price rule's outputs (read derived/ only; never rebuild)."""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"


def load():
    return json.loads((D / "summary.json").read_text()), pd.read_csv(D / "land_by_line.csv")


def test_lines_add_to_total():
    s, by = load()
    for k in ["central", "low", "high"]:
        for i, end in enumerate(["low", "high"]):
            assert abs(by[f"charge_{k}_{end}_bn"].sum() - s[k]["case_rate_bn"][i]) < 1e-9
            assert abs(by[f"paired_{k}_{end}_bn"].sum() - s[k]["paired_theta_bn"][i]) < 1e-9


def test_range_brackets_central():
    s, by = load()
    for i in range(2):
        assert s["low"]["case_rate_bn"][i] <= s["central"]["case_rate_bn"][i] <= s["high"]["case_rate_bn"][i]
    assert (by.value_low_bn <= by.value_central_bn + 1e-9).all() and (by.value_central_bn <= by.value_high_bn + 1e-9).all()


def test_acres_split_closes():
    _, by = load()
    assert ((by.acres_urban + by.acres_rural - by.acres).abs() < 1e-6 * by.acres.clip(lower=1)).all()
    assert (by.acres_rural >= -1e-9).all()


def test_no_state_residential_fallback_left():
    p = pd.read_csv(D / "county_urban_prices.csv", dtype={"county": str})
    assert set(p.urban_level) <= {"urban_tracts", "county", "nearest_county", "missing"}
    s, _ = load()
    levels = s["coverage"]["urban_level_acres"]
    assert "state" not in levels


def test_factors_sourced():
    f = pd.read_csv(D / "factors.csv")
    assert f.source_and_page.str.len().gt(40).all()
    assert ((f.low <= f.central) & (f.central <= f.high)).all()


def test_rates_are_paired_anchor():
    s, _ = load()
    r = s["rates"]
    assert abs(r["theta"] - 0.4894) < 1e-3
    assert r["paired_central"]["federal"] > r["paired_central"]["state_local"] > r["case"]


def test_farm_prices_positive():
    f = pd.read_csv(D / "county_farm_prices.csv", dtype={"county": str})
    assert (f.farm24 > 0).all() and f.land_share.between(0.3, 1.0).all()
