#!/usr/bin/env python3
"""Tests for the second-generation-by-origin estimators.

Two kinds of test. The estimator tests run the fast Schur-complement weighted least squares
against a dense dummy-variable regression on synthetic data, so the shortcut has to return the
same number the textbook design matrix returns. The code tests read the shipped IPUMS DDI and
assert that every code this lane keys on still carries the label the lane assumes.

Run:  uv run --no-project python3 -m pytest infra/immigration-fiscal/second_generation_by_origin_2026_09_22/ -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis as A  # noqa: E402


# ---------------------------------------------------------------------------------------------
# helpers: build a synthetic person-level sample and its (group x FE) tables
# ---------------------------------------------------------------------------------------------

def synthetic(n=4000, n_groups=5, n_fe=7, seed=0, y_kind="continuous"):
    rng = np.random.default_rng(seed)
    g = rng.integers(0, n_groups, n)
    f = rng.integers(0, n_fe, n)
    w = rng.gamma(2.0, 1.0, n)
    group_effect = rng.normal(0, 1, n_groups)
    fe_effect = rng.normal(0, 1, n_fe)
    y = group_effect[g] + fe_effect[f] + rng.normal(0, 0.5, n)
    if y_kind == "binary":
        y = (y > np.median(y)).astype(float)
    W = np.zeros((n_groups, n_fe))
    Y = np.zeros((n_groups, n_fe))
    np.add.at(W, (g, f), w)
    np.add.at(Y, (g, f), w * y)
    return dict(g=g, f=f, w=w, y=y, W=W, Y=Y, n_groups=n_groups, n_fe=n_fe)


def dense_wls(s, ref):
    """Textbook WLS: dummies for every non-reference group plus every FE cell."""
    n = len(s["g"])
    others = [k for k in range(s["n_groups"]) if k != ref]
    X = np.zeros((n, len(others) + s["n_fe"]))
    for j, k in enumerate(others):
        X[s["g"] == k, j] = 1.0
    for j in range(s["n_fe"]):
        X[s["f"] == j, len(others) + j] = 1.0
    sw = np.sqrt(s["w"])
    beta, *_ = np.linalg.lstsq(X * sw[:, None], s["y"] * sw, rcond=None)
    out = np.zeros(s["n_groups"])
    for j, k in enumerate(others):
        out[k] = beta[j]
    return out


# ---------------------------------------------------------------------------------------------
# estimator tests
# ---------------------------------------------------------------------------------------------

@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_wls_gaps_matches_dense_regression(seed):
    s = synthetic(seed=seed)
    got, status = A.wls_gaps(s["W"], s["Y"], ref=0)
    assert status == "ok"
    want = dense_wls(s, ref=0)
    assert np.allclose(got, want, atol=1e-8), (got, want)
    assert got[0] == 0.0


def test_wls_gaps_matches_dense_regression_binary_outcome():
    s = synthetic(seed=7, y_kind="binary")
    got, _ = A.wls_gaps(s["W"], s["Y"], ref=2)
    assert np.allclose(got, dense_wls(s, ref=2), atol=1e-8)


def test_wls_gaps_recovers_a_planted_gap_with_composition_confounded():
    """Groups deliberately placed in different FE cells: the raw gap is wrong, the adjusted one is
    right. This is the whole reason the regression exists."""
    rng = np.random.default_rng(11)
    n_fe, n = 4, 60000
    fe_effect = np.array([0.0, 1.0, 2.0, 3.0])
    planted = np.array([0.0, -0.50, 0.25])
    # group 0 sits mostly in low-FE cells, group 1 mostly in high-FE cells
    probs = np.array([[0.55, 0.25, 0.15, 0.05],
                      [0.05, 0.15, 0.25, 0.55],
                      [0.25, 0.25, 0.25, 0.25]])
    g = rng.integers(0, 3, n)
    f = np.array([rng.choice(n_fe, p=probs[k]) for k in g])
    w = np.full(n, 1.0)
    y = planted[g] + fe_effect[f] + rng.normal(0, 0.05, n)
    W = np.zeros((3, n_fe)); Y = np.zeros((3, n_fe))
    np.add.at(W, (g, f), w)
    np.add.at(Y, (g, f), w * y)
    adj, _ = A.wls_gaps(W, Y, ref=0)
    raw = A.raw_gaps(W, Y, ref=0)
    assert np.allclose(adj, planted - planted[0], atol=0.01), adj
    assert raw[1] > 1.0, raw   # composition alone moves the raw gap the wrong way by >1.0
    assert abs(raw[1] - adj[1]) > 1.0


def test_wls_gaps_is_invariant_to_rescaling_the_weights():
    s = synthetic(seed=5)
    a, _ = A.wls_gaps(s["W"], s["Y"], ref=1)
    b, _ = A.wls_gaps(s["W"] * 1000.0, s["Y"] * 1000.0, ref=1)
    assert np.allclose(a, b, atol=1e-9)


def test_wls_gaps_equals_raw_gap_when_composition_is_identical():
    """With every group spread identically over the FE cells, adjustment changes nothing."""
    n_fe = 5
    share = np.array([0.1, 0.3, 0.2, 0.25, 0.15])
    means = np.array([1.0, 1.4, 0.7])
    W = np.outer(np.array([100.0, 250.0, 60.0]), share)
    fe_effect = np.array([0.0, 0.5, -0.2, 0.9, 0.3])
    Y = W * (means[:, None] + fe_effect[None, :])
    adj, _ = A.wls_gaps(W, Y, ref=0)
    raw = A.raw_gaps(W, Y, ref=0)
    assert np.allclose(adj, raw, atol=1e-9)
    assert np.allclose(adj, means - means[0], atol=1e-9)


def test_wls_gaps_drops_empty_groups_and_empty_fe_cells():
    s = synthetic(seed=3, n_groups=6, n_fe=8)
    s["W"][4, :] = 0.0
    s["Y"][4, :] = 0.0
    s["W"][:, 6] = 0.0
    s["Y"][:, 6] = 0.0
    got, status = A.wls_gaps(s["W"], s["Y"], ref=0)
    assert status == "ok"
    assert np.isnan(got[4])
    assert np.isfinite(got[[1, 2, 3, 5]]).all()


def test_wls_gaps_honours_the_design_keep_mask():
    s = synthetic(seed=4, n_groups=5)
    keep = np.array([True, True, True, False, True])
    got, _ = A.wls_gaps(s["W"], s["Y"], ref=0, keep=keep)
    assert np.isnan(got[3])
    # dropping a group must also drop its people from the FE denominators
    Wk, Yk = s["W"][keep], s["Y"][keep]
    sub = dict(s)
    m = keep[s["g"]]
    sub.update(g=np.searchsorted(np.where(keep)[0], s["g"][m]), f=s["f"][m],
               w=s["w"][m], y=s["y"][m], n_groups=int(keep.sum()))
    want = dense_wls(sub, ref=0)
    assert np.allclose(got[keep], want, atol=1e-8)


def test_wls_gaps_returns_nan_when_the_reference_is_empty():
    s = synthetic(seed=6)
    s["W"][0, :] = 0.0
    s["Y"][0, :] = 0.0
    got, status = A.wls_gaps(s["W"], s["Y"], ref=0)
    assert status == "reference-empty"
    assert np.isnan(got).all()


def test_raw_gaps_is_the_difference_in_weighted_means():
    s = synthetic(seed=8)
    got = A.raw_gaps(s["W"], s["Y"], ref=0)
    means = s["Y"].sum(1) / s["W"].sum(1)
    assert np.allclose(got, means - means[0], atol=1e-12)
    assert got[0] == 0.0


# ---------------------------------------------------------------------------------------------
# closing ratio
# ---------------------------------------------------------------------------------------------

def test_closing_ratio_definition():
    assert A.closing_ratio(-1.0, -0.5) == pytest.approx(0.5)
    assert A.closing_ratio(-1.0, 0.0) == pytest.approx(1.0)     # gap fully closed
    assert A.closing_ratio(-1.0, -1.0) == pytest.approx(0.0)    # nothing closed
    assert A.closing_ratio(-1.0, -1.5) == pytest.approx(-0.5)   # gap widened
    assert A.closing_ratio(-1.0, 0.5) == pytest.approx(1.5)     # overshoots past the reference
    assert A.closing_ratio(0.4, 0.1) == pytest.approx(0.75)     # sign of the gap does not matter


def test_closing_ratio_is_nan_on_a_zero_or_missing_first_generation_gap():
    assert np.isnan(A.closing_ratio(0.0, -0.5))
    assert np.isnan(A.closing_ratio(np.nan, -0.5))
    assert np.isnan(A.closing_ratio(-1.0, np.nan))


# ---------------------------------------------------------------------------------------------
# taxonomy plumbing
# ---------------------------------------------------------------------------------------------

def test_taxonomy_matrix_sums_members_and_rejects_overlap():
    groups = [("a", [0, 1]), ("b", [2]), ("c", [3, 4])]
    M = A.taxonomy_matrix(groups, 5)
    W = np.arange(5 * 3, dtype=float).reshape(5, 3)
    assert np.allclose(M @ W, np.vstack([W[:2].sum(0), W[2], W[3:].sum(0)]))
    with pytest.raises(AssertionError):
        A.taxonomy_matrix([("a", [0, 1]), ("b", [1, 2])], 3)


def test_region_of_follows_the_loader_map():
    assert A.region_of(20000 // 100) == "Mexico"
    assert A.region_of(21030 // 100) == "Central America"
    assert A.region_of(25000 // 100) == "Caribbean"      # Cuba, general 250
    assert A.region_of(26010 // 100) == "Caribbean"      # Dominican Republic, general 260
    assert A.region_of(30025 // 100) == "South America"
    assert A.region_of(45300 // 100) == "Europe"
    assert A.region_of(51500 // 100) == "Asia"
    assert A.region_of(53000 // 100) == "Asia"           # Iran, general 530
    assert A.region_of(60031 // 100) == "Africa"
    assert A.region_of(15000 // 100) == "Canada"
    assert A.region_of(70010 // 100) == "Other"          # Australia
    assert A.region_of(31000 // 100) == "Other"          # Americas, n.s.
    assert A.region_of(11000 // 100) == "US outlying"    # Puerto Rico
    assert A.region_of(12090 // 100) == "US outlying"
    assert set(A.REGIONS) == {A.region_of(c // 100) for c in
                              (20000, 21030, 25000, 30025, 45300, 51500, 60031, 15000, 70010, 11000)}


def test_reference_index_finds_exactly_one_reference():
    tax = {"t": [("a", [0]), (A.REF_GROUP, [1]), ("b", [2])]}
    assert A.reference_index(tax) == {"t": 1}
    with pytest.raises(AssertionError):
        A.reference_index({"t": [("a", [0]), ("b", [1])]})


# ---------------------------------------------------------------------------------------------
# binning engine and the cluster bootstrap
# ---------------------------------------------------------------------------------------------

def _tiny_frame(n=900, seed=2):
    rng = np.random.default_rng(seed)
    years = rng.choice(A.YEARS, n)
    order = np.argsort(years, kind="stable")
    years = years[order]
    serial = np.zeros(n, dtype=np.int64)
    for y in np.unique(years):
        m = years == y
        serial[m] = rng.integers(1, 40, m.sum())
    df = pd.DataFrame({
        "year": years, "serial": serial, "w": rng.gamma(2, 1, n),
        "age": rng.integers(25, 65, n), "sex": rng.integers(1, 3, n),
    }).sort_values(["year", "serial"]).reset_index(drop=True)
    return df


def test_engine_bins_cover_every_row_and_respect_the_fe_layout():
    df = _tiny_frame()
    fine = np.random.default_rng(0).integers(0, 6, len(df))
    e = A.Engine(df, fine, 6)
    assert e.bin.min() >= 0 and e.bin.max() < e.nbins
    band = np.clip((df.age.to_numpy() - 25) // 5, 0, A.NBAND - 1)
    assert (e.fe // A.NY == band * 2 + (df.sex.to_numpy() - 1)).all()
    assert (e.fe % A.NY == df.year.to_numpy() - A.YEARS[0]).all()


def test_engine_tables_reproduce_weighted_sums():
    df = _tiny_frame()
    rng = np.random.default_rng(1)
    fine = rng.integers(0, 4, len(df))
    e = A.Engine(df, fine, 4)
    y = rng.normal(0, 1, len(df))
    o = dict(name="t", label="t", gaps=True, mask=np.ones(len(df), bool), y=y)
    e.prepare([o])
    W, Y = e.tables(o, None)
    assert W.sum() == pytest.approx(df.w.sum())
    assert Y.sum() == pytest.approx(float((df.w.to_numpy() * y).sum()))
    for k in range(4):
        assert W[k].sum() == pytest.approx(df.w.to_numpy()[fine == k].sum())
    assert (o["n_obs_fine"].sum(1) == np.bincount(fine, minlength=4)).all()


def test_engine_mask_restricts_the_tables():
    df = _tiny_frame()
    rng = np.random.default_rng(3)
    fine = rng.integers(0, 3, len(df))
    e = A.Engine(df, fine, 3)
    mask = df.age.to_numpy() < 45
    o = dict(name="t", label="t", gaps=True, mask=mask, y=np.ones(len(df)))
    e.prepare([o])
    W, Y = e.tables(o, None)
    assert W.sum() == pytest.approx(df.w.to_numpy()[mask].sum())
    assert int(o["n_obs_fine"].sum()) == int(mask.sum())


def test_cluster_bootstrap_multipliers_preserve_the_household_count_per_year():
    df = _tiny_frame()
    e = A.Engine(df, np.zeros(len(df), dtype=np.int64), 1)
    rng = np.random.default_rng(42)
    for _ in range(5):
        mult = e.draw_multipliers(rng)
        assert mult.shape == (e.n_hh,)
        assert (mult >= 0).all()
        for lo, hi in e.year_blocks:
            assert mult[lo:hi].sum() == pytest.approx(hi - lo)
        assert mult.sum() == pytest.approx(e.n_hh)


def test_cluster_bootstrap_keeps_a_household_together():
    """Every person in a resampled household carries the same multiplier — that is what makes
    this a cluster bootstrap rather than a person bootstrap."""
    df = _tiny_frame()
    e = A.Engine(df, np.zeros(len(df), dtype=np.int64), 1)
    mult = e.draw_multipliers(np.random.default_rng(9))
    per_person = mult[e.hh]
    key = df.year.astype(str) + "_" + df.serial.astype(str)
    assert pd.Series(per_person).groupby(key.to_numpy()).nunique().max() == 1


def test_cluster_bootstrap_spread_exceeds_the_independent_person_bootstrap():
    """Positively correlated households must widen the standard error; if the resample were at the
    person level the SE would be too small, which is the failure this test guards."""
    rng = np.random.default_rng(5)
    n_hh, per_hh = 800, 4
    hh = np.repeat(np.arange(n_hh), per_hh)
    y = np.repeat(rng.normal(0, 1, n_hh), per_hh) + rng.normal(0, 0.05, n_hh * per_hh)
    df = pd.DataFrame({"year": 1994, "serial": hh + 1, "w": 1.0,
                       "age": 30, "sex": 1})
    e = A.Engine(df, np.zeros(len(df), dtype=np.int64), 1)
    o = dict(name="t", label="t", gaps=True, mask=np.ones(len(df), bool), y=y)
    e.prepare([o])
    boot = []
    for _ in range(300):
        W, Y = e.tables(o, e.draw_multipliers(rng))
        boot.append(Y.sum() / W.sum())
    cluster_se = float(np.std(boot, ddof=1))
    iid_se = float(np.std(y, ddof=1) / np.sqrt(len(y)))
    assert cluster_se > 1.6 * iid_se, (cluster_se, iid_se)


# ---------------------------------------------------------------------------------------------
# DDI code assertions against the shipped codebook
# ---------------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ddi():
    if not A.DDI.exists():
        pytest.skip(f"DDI codebook not staged at {A.DDI}")
    return A.parse_ddi(A.DDI)


def test_ddi_parses_every_variable_this_lane_keys_on(ddi):
    for var in ("EMPSTAT", "LABFORCE", "EDUC", "HISPAN", "RACE", "CITIZEN", "NATIVITY", "BPL"):
        assert var in ddi and ddi[var], var


def test_ddi_employment_codes(ddi):
    assert ddi["EMPSTAT"][10] == "At work"
    assert ddi["EMPSTAT"][12] == "Has job, not at work last week"
    assert ddi["EMPSTAT"][1] == "Armed Forces"
    assert ddi["LABFORCE"][2] == "Yes, in the labor force"
    assert ddi["LABFORCE"][1] == "No, not in the labor force"
    assert ddi["LABFORCE"][0] == "NIU"


def test_ddi_education_bracket_is_the_one_the_lane_assumes(ddi):
    assert ddi["EDUC"][71] == "12th grade, no diploma"
    assert ddi["EDUC"][73] == "High school diploma or equivalent"
    assert ddi["EDUC"][111] == "Bachelor's degree"
    # nothing between the two thresholds may be misfiled by the >=/<= tests
    for code, lab in ddi["EDUC"].items():
        if code in A.EDUC_NIU:
            continue
        if code <= A.EDUC_LT_HS_MAX:
            assert not lab.lower().startswith(("high school diploma", "bachelor")), (code, lab)
        if code >= A.EDUC_COLLEGE_PLUS_MIN:
            assert any(k in lab.lower() for k in
                       ("bachelor", "master", "doctorate", "professional", "college")), (code, lab)


def test_ddi_origin_and_reference_codes(ddi):
    assert ddi["BPL"][20000] == "Mexico"
    assert ddi["RACE"][100] == "White"
    assert ddi["HISPAN"][0] == "Not Hispanic"
    for code in A.HISPAN_MEXICAN:
        assert "mexic" in ddi["HISPAN"][code].lower() or "chican" in ddi["HISPAN"][code].lower()
    # no Mexican-identifying label may sit outside the set the lane uses
    for code, lab in ddi["HISPAN"].items():
        low = lab.lower()
        if ("mexic" in low or "chicano" in low) and code not in A.HISPAN_MEXICAN:
            raise AssertionError(f"HISPAN {code} = {lab} is Mexican but not in HISPAN_MEXICAN")
    assert ddi["CITIZEN"][1] == "Born in U.S"
    assert ddi["CITIZEN"][4] == "Naturalized citizen"
    assert ddi["CITIZEN"][5] == "Not a citizen"
    assert ddi["NATIVITY"][1] == "Both parents native-born"
    assert ddi["NATIVITY"][4] == "Both parents foreign"
    assert ddi["NATIVITY"][5] == "Foreign born"


def test_ddi_us_area_birthplaces_fall_in_the_us_outlying_band(ddi):
    us_labels = ("United States", "American Samoa", "Guam", "Northern Mariana", "Puerto Rico",
                 "U.S. Virgin Islands", "U.S. outlying")
    for code, lab in ddi["BPL"].items():
        if lab.startswith(us_labels):
            assert code // 100 <= A.BPL_US_MAX_GENERAL, (code, lab)
            assert A.region_of(code // 100) in ("US outlying", "Other"), (code, lab)


def test_ddi_code_report_runs_and_labels_every_decision_code(ddi):
    rep = A.ddi_code_report(ddi)
    assert rep["EMPSTAT.employed"] == {"10": "At work", "12": "Has job, not at work last week"}
    assert rep["BPL.mexico"] == {"20000": "Mexico"}
    for key, labels in rep.items():
        assert labels, key
        for code, lab in labels.items():
            assert isinstance(lab, str) and lab.strip(), (key, code)


def test_ddi_code_report_fails_loudly_on_a_code_the_codebook_does_not_have(ddi):
    broken = {k: dict(v) for k, v in ddi.items()}
    del broken["EMPSTAT"][12]
    with pytest.raises(AssertionError):
        A.ddi_code_report(broken)
