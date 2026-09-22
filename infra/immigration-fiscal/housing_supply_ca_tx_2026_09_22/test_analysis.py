"""Unit tests for the CA/TX housing-supply lane.

Run from the repository root::

    uv run --no-project python3 -m pytest \
        infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/ -q

These tests exercise pure functions against inline fixtures and hand-computed
values.  They do not touch the network, ``_cache/`` or the PUMS archive.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis as A  # noqa: E402


# ---------------------------------------------------------------- BPS parser

BPS_FIXTURE = """Survey,FIPS,Region,Division,State,,1-unit,,,2-units,,,3-4 units,,,5+ units,,,1-unit rep,,,2-units rep
Date,State,Code,Code,Name,Bldgs,Units,Value,Bldgs,Units,Value,Bldgs,Units,Value,Bldgs,Units,Value,Bldgs,Units,Value,Bldgs,Units,Value

202312,06,4,9,California,10,11,1000,2,4,200,1,3,300,5,100,5000,9,9,900,1,2,100
202312,48,3,7,Texas,20,21,2000,3,6,300,2,7,700,6,200,6000,18,18,1800,2,4,200
202312,US,0,0,United States,30,32,3000,5,10,500,3,10,1000,11,300,11000,27,27,2700,3,6,300
"""


def test_parse_bps_sums_the_four_structure_classes():
    df = A.parse_bps(BPS_FIXTURE)
    assert len(df) == 3
    ca = df[df.fips == "06"].iloc[0]
    # 11 (1-unit) + 4 (2-unit) + 3 (3-4 unit) + 100 (5+) = 118.
    # The trailing "rep" (reported, non-imputed) block must not be counted.
    assert ca.total_units == 118
    assert ca.units_1unit == 11 and ca.units_2units == 4
    assert ca.units_3_4units == 3 and ca.units_5plus == 100
    tx = df[df.fips == "48"].iloc[0]
    assert tx.total_units == 21 + 6 + 7 + 200


def test_parse_bps_reads_survey_date_and_flags_aggregates():
    df = A.parse_bps(BPS_FIXTURE)
    assert set(df.year) == {2023}
    assert set(df.month) == {12}
    assert not df[df.fips == "06"].iloc[0].is_aggregate
    assert df[df.fips == "US"].iloc[0].is_aggregate


def test_parse_bps_skips_headers_and_blank_lines():
    df = A.parse_bps(BPS_FIXTURE)
    assert "Date" not in set(df.fips)
    assert len(df) == 3


def test_parse_bps_rejects_a_truncated_row():
    bad = BPS_FIXTURE + "202312,12,3,5,Florida,1,1,100\n"
    with pytest.raises(ValueError, match="at least 16"):
        A.parse_bps(bad)


def test_parse_bps_raises_when_nothing_parses():
    with pytest.raises(ValueError, match="no BPS data rows"):
        A.parse_bps("Survey,FIPS\nDate,State\n")


# ------------------------------------------------------------ FRED annualiser

def test_fred_annual_sums_full_years_and_drops_partial_ones():
    lines = ["observation_date,X"]
    for month in range(1, 13):
        lines.append(f"2020-{month:02d}-01,10")
    for month in range(1, 4):  # partial year, must be dropped
        lines.append(f"2021-{month:02d}-01,50")
    out = A.fred_annual("\n".join(lines))
    assert out.loc[2020] == 120
    assert 2021 not in out.index


# ---------------------------------------------------- mechanical price response

def test_mechanical_response_matches_hand_values():
    # d / (eps_S + eps_D)
    assert A.mechanical_response(1.0, 0.5, 0.5) == pytest.approx(1.0)
    assert A.mechanical_response(1.0, 2.3, 0.7) == pytest.approx(1.0 / 3.0)
    assert A.mechanical_response(2.0, 1.0, 1.0) == pytest.approx(1.0)
    assert A.mechanical_response(1.0, 0.626594, 0.7) == pytest.approx(
        1.0 / 1.326594, rel=1e-12)


def test_mechanical_response_is_lower_where_supply_is_more_elastic():
    la = A.mechanical_response(1.0, 0.626594, 0.7)   # Los Angeles
    houston = A.mechanical_response(1.0, 2.302, 0.7)
    assert la > houston
    assert la / houston == pytest.approx((2.302 + 0.7) / (0.626594 + 0.7))


def test_mechanical_response_refuses_a_non_positive_denominator():
    with pytest.raises(ValueError, match="non-positive denominator"):
        A.mechanical_response(1.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="non-positive denominator"):
        A.mechanical_response(1.0, -1.0, 0.5)
    with pytest.raises(ValueError):
        A.mechanical_response(1.0, float("nan"), 0.5)


# ------------------------------------------------------ replicate-weight SE

def test_replicate_se_matches_a_hand_computed_fixture():
    # SE^2 = 4/R * sum_r (t_r - t)^2 with R = 4 replicates.
    # deviations 2, -2, 1, -1 -> sum of squares 4+4+1+1 = 10; 4/4 * 10 = 10.
    assert A.replicate_se(100.0, np.array([102.0, 98.0, 101.0, 99.0])) == pytest.approx(
        math.sqrt(10.0))


def test_replicate_se_matches_the_formula_on_eighty_replicates():
    rng = np.random.default_rng(0)
    point = 1000.0
    reps = point + rng.normal(0, 25, 80)
    expected = math.sqrt(4.0 / 80.0 * float(np.sum((reps - point) ** 2)))
    assert A.replicate_se(point, reps) == pytest.approx(expected)


def test_replicate_se_is_zero_when_every_replicate_equals_the_estimate():
    assert A.replicate_se(50.0, np.full(80, 50.0)) == pytest.approx(0.0)


# ------------------------------------------------------------- metro matching

def _cbsa(names: list[str]) -> pd.DataFrame:
    parsed = [A.split_cbsa(n) for n in names]
    return pd.DataFrame({
        "NAME": names,
        "cities": [p[0] for p in parsed],
        "states": [p[1] for p in parsed],
        "first_city": [p[0][0] if p[0] else "" for p in parsed],
        "total": [100.0] * len(names),
        "mexican": [10.0] * len(names),
        "mex_share": [0.1] * len(names),
    })


def test_match_metro_joins_on_the_first_principal_city():
    cbsa = _cbsa(["Los Angeles-Long Beach-Anaheim, CA Metro Area",
                  "Houston-Pasadena-The Woodlands, TX Metro Area"])
    row, how = A.match_metro("Los Angeles, CA", cbsa)
    assert how == "first-city"
    assert row["NAME"].startswith("Los Angeles")


def test_match_metro_falls_back_to_any_principal_city():
    # Zillow says "Sarasota, FL"; the CBSA leads with a different principal city.
    cbsa = _cbsa(["North Port-Bradenton-Sarasota, FL Metro Area"])
    row, how = A.match_metro("Sarasota, FL", cbsa)
    assert how == "any-city"
    assert row["NAME"].startswith("North Port")


def test_match_metro_refuses_duplicate_names():
    """Two CBSAs sharing a principal city and state must NOT be silently joined."""
    cbsa = _cbsa(["Springfield-Example, IL Metro Area",
                  "Springfield-Other, IL Metro Area"])
    row, how = A.match_metro("Springfield, IL", cbsa)
    assert row is None
    assert how == "ambiguous-first-city(2)"


def test_match_metro_refuses_duplicates_on_the_any_city_fallback():
    cbsa = _cbsa(["Alpha-Shared City, TX Metro Area",
                  "Beta-Shared City, TX Metro Area"])
    row, how = A.match_metro("Shared City, TX", cbsa)
    assert row is None
    assert how.startswith("ambiguous-any-city")


def test_match_metro_reports_a_clean_miss():
    cbsa = _cbsa(["Los Angeles-Long Beach-Anaheim, CA Metro Area"])
    row, how = A.match_metro("Nowhere, ZZ", cbsa)
    assert row is None and how == "no-match"


def test_match_metro_requires_the_state_to_agree():
    cbsa = _cbsa(["Portland-Vancouver-Hillsboro, OR-WA Metro Area"])
    assert A.match_metro("Portland, ME", cbsa)[0] is None
    assert A.match_metro("Portland, OR", cbsa)[1] == "first-city"


def test_split_cbsa_handles_slashes_and_multi_state_names():
    cities, states = A.split_cbsa("Louisville/Jefferson County, KY-IN Metro Area")
    assert "louisville" in cities and "jefferson county" in cities
    assert states == ["KY", "IN"]
    cities, states = A.split_cbsa("Minneapolis-St. Paul-Bloomington, MN-WI Metro Area")
    assert cities[0] == "minneapolis" and "st paul" in cities
    assert states == ["MN", "WI"]


# ------------------------------------------------------------------- OLS HC1

def _naive_ols_hc1(y, X):
    """Independent, loop-based oracle for :func:`analysis.ols_hc1`."""
    y = np.asarray(y, float).ravel()
    X = np.asarray(X, float)
    n, k = X.shape
    xtx = np.zeros((k, k))
    xty = np.zeros(k)
    for i in range(n):
        xtx += np.outer(X[i], X[i])
        xty += X[i] * y[i]
    xtx_inv = np.linalg.inv(xtx)
    beta = xtx_inv @ xty
    meat = np.zeros((k, k))
    for i in range(n):
        e = y[i] - X[i] @ beta
        meat += (e ** 2) * np.outer(X[i], X[i])
    vcov = xtx_inv @ meat @ xtx_inv * (n / (n - k))
    return beta, np.sqrt(np.diag(vcov))


def test_ols_hc1_matches_an_independent_implementation():
    rng = np.random.default_rng(7)
    n = 40
    x = rng.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    y = 1.5 + 2.0 * x + rng.normal(0, np.abs(x) + 0.2)  # heteroskedastic on purpose
    got = A.ols_hc1(y, X, ["const", "x"])
    beta, se = _naive_ols_hc1(y, X)
    assert got["coef"] == pytest.approx(beta)
    assert got["se"] == pytest.approx(se)
    assert got["n"] == n and got["k"] == 2


def test_ols_hc1_recovers_an_exact_fit():
    X = np.column_stack([np.ones(3), [0.0, 1.0, 2.0]])
    y = np.array([1.0, 3.0, 5.0])  # y = 1 + 2x exactly
    res = A.ols_hc1(y, X, ["const", "x"])
    assert res["coef"] == pytest.approx([1.0, 2.0])
    assert res["se"] == pytest.approx([0.0, 0.0], abs=1e-9)
    assert res["r2"] == pytest.approx(1.0)


def test_ols_hc1_applies_the_hc1_finite_sample_factor():
    rng = np.random.default_rng(11)
    n, k = 25, 2
    x = rng.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    y = rng.normal(size=n)
    res = A.ols_hc1(y, X, ["const", "x"])
    # HC0 differs from HC1 by exactly n/(n-k).
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    xtx_inv = np.linalg.inv(X.T @ X)
    hc0 = xtx_inv @ ((X * (resid ** 2)[:, None]).T @ X) @ xtx_inv
    assert res["se"] ** 2 == pytest.approx(np.diag(hc0) * n / (n - k))


def test_ols_hc1_refuses_an_unidentified_regression():
    with pytest.raises(ValueError, match="not identified"):
        A.ols_hc1(np.array([1.0, 2.0]), np.ones((2, 2)), ["a", "b"])


# ------------------------------------------------------------------ redaction

def test_redact_removes_an_api_key_from_a_url():
    url = "https://api.census.gov/data/2023/acs/acs1?get=NAME&key=abcdef0123456789"
    out = A.redact(url)
    assert "abcdef0123456789" not in out
    assert "key=REDACTED" in out


# ---------------------------------------------------------------- PUMS cells

def _person(**kw):
    base = {"STATE": 6, "AGEP": 40, "SCHL": 21, "HISP": 1, "RAC1P": 1,
            "NATIVITY": 1, "MIGSP": np.nan, "PWGTP": 10}
    base.update(kw)
    for i in range(1, 81):
        base.setdefault(f"PWGTP{i}", base["PWGTP"])
    return base


def test_pums_cells_counts_residents_inflows_and_outflows():
    rows = [
        _person(STATE=6, MIGSP=np.nan, PWGTP=10),   # CA stayer
        _person(STATE=6, MIGSP=48, PWGTP=5),        # TX -> CA
        _person(STATE=48, MIGSP=6, PWGTP=7),        # CA -> TX
        _person(STATE=36, MIGSP=6, PWGTP=3),        # CA -> NY
    ]
    cells = A.pums_cells(pd.DataFrame(rows))

    def val(metric, state):
        sel = cells[(cells.metric == metric) & (cells.state == state)
                    & (cells.group == "nhwhite")]
        return float(sel["PWGTP"].sum())

    assert val("resident", "06") == 15      # stayer + TX->CA in-migrant
    assert val("inflow", "06") == 5
    assert val("outflow", "06") == 10       # CA->TX plus CA->NY
    assert val("resident", "48") == 7
    assert val("inflow", "48") == 7


def test_pums_cells_excludes_foreign_born_and_foreign_origin_moves():
    rows = [
        _person(STATE=6, NATIVITY=2, PWGTP=99),      # foreign born, dropped
        _person(STATE=6, MIGSP=109, PWGTP=50),       # arrived from France
    ]
    cells = A.pums_cells(pd.DataFrame(rows))
    # Filter on one group: nhwhite is nested inside all_native, so an unfiltered
    # sum counts an NH-white person once in each.
    res = cells[(cells.metric == "resident") & (cells.state == "06")
                & (cells.group == "nhwhite")]
    inf = cells[(cells.metric == "inflow") & (cells.state == "06")
                & (cells.group == "nhwhite")]
    assert float(res["PWGTP"].sum()) == 50   # the native counts as a resident
    assert float(inf["PWGTP"].sum()) == 0    # but a move from abroad is not an inflow


def test_pums_cells_ignores_within_state_moves():
    rows = [_person(STATE=6, MIGSP=6, PWGTP=12)]
    cells = A.pums_cells(pd.DataFrame(rows))
    nhw = cells[cells.group == "nhwhite"]
    assert float(nhw[nhw.metric == "inflow"]["PWGTP"].sum()) == 0
    assert float(nhw[nhw.metric == "outflow"]["PWGTP"].sum()) == 0
    assert float(nhw[nhw.metric == "resident"]["PWGTP"].sum()) == 12


def test_pums_cells_splits_education_at_a_bachelors_degree():
    rows = [_person(SCHL=21, PWGTP=4), _person(SCHL=20, PWGTP=6)]
    cells = A.pums_cells(pd.DataFrame(rows))
    res = cells[(cells.metric == "resident") & (cells.group == "nhwhite")]
    got = dict(zip(res.educ, res.PWGTP))
    assert got["ba_plus"] == 4
    assert got["less_than_ba"] == 6


def test_pums_cells_separates_nhwhite_from_all_natives():
    rows = [_person(RAC1P=1, HISP=1, PWGTP=5),    # NH white
            _person(RAC1P=2, HISP=1, PWGTP=8),    # native, not white
            _person(RAC1P=1, HISP=2, PWGTP=9)]    # white, Hispanic
    cells = A.pums_cells(pd.DataFrame(rows))

    def tot(group):
        return float(cells[(cells.metric == "resident")
                           & (cells.group == group)]["PWGTP"].sum())

    assert tot("nhwhite") == 5
    assert tot("all_native") == 22


def test_pums_cells_restricts_residents_to_ages_25_to_64():
    rows = [_person(AGEP=20, PWGTP=3), _person(AGEP=30, PWGTP=4),
            _person(AGEP=70, PWGTP=5)]
    cells = A.pums_cells(pd.DataFrame(rows))
    res = cells[(cells.metric == "resident") & (cells.group == "nhwhite")]
    p18 = cells[(cells.metric == "pop18plus") & (cells.group == "nhwhite")]
    assert float(res["PWGTP"].sum()) == 4        # only the 30-year-old
    assert float(p18["PWGTP"].sum()) == 12       # everyone 18 and over
