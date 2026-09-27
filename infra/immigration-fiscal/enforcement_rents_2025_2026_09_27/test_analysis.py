"""Checks for the enforcement-and-rents lane.

Run from the repository root::

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest \
        infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/ -q

The statistics helpers are checked against closed forms; the hand-transcribed Brookings
table is checked against the two identities its columns obey; the derived files are checked
for the claims RESULT.md makes about them.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import analysis as A  # noqa: E402

DERIVED = LANE / "derived"


def test_t_p_values_match_tables():
    # two-sided critical values from standard t tables
    assert A.t_two_sided_p(2.228139, 10) == pytest.approx(0.05, abs=1e-5)
    assert A.t_two_sided_p(2.014103, 45) == pytest.approx(0.05, abs=1e-5)
    assert A.t_two_sided_p(1.959964, 1e7) == pytest.approx(0.05, abs=1e-5)
    assert A.t_two_sided_p(0.0, 20) == pytest.approx(1.0, abs=1e-12)
    # Cauchy (df=1): p = 1 - 2 atan(t)/pi
    assert A.t_two_sided_p(3.0, 1) == pytest.approx(1 - 2 * math.atan(3.0) / math.pi, abs=1e-10)


def test_cluster_se_reduces_to_hc1_with_singleton_clusters():
    rng = np.random.default_rng(1)
    n = 60
    X = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
    y = X @ np.array([1.0, 0.5, -0.2]) + rng.normal(size=n) * (1 + np.abs(X[:, 1]))
    fit = A.ols_cluster(y, X, np.arange(n))
    XtX_inv = np.linalg.inv(X.T @ X)
    e = y - X @ fit["beta"]
    hc0 = XtX_inv @ (X.T * e ** 2) @ X @ XtX_inv
    # CR1 with G = n singleton clusters: (n/(n-1)) * ((n-1)/(n-k)) = n/(n-k), which is HC1
    hc1 = hc0 * n / (n - X.shape[1])
    assert np.allclose(fit["se"], np.sqrt(np.diag(hc1)), rtol=1e-10)


def test_cluster_se_invariant_to_group_labels():
    rng = np.random.default_rng(2)
    n = 90
    g = np.repeat(np.arange(15), 6)
    X = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = X @ np.array([0.3, 1.0]) + np.repeat(rng.normal(size=15), 6) + rng.normal(size=n)
    a = A.ols_cluster(y, X, g)
    b = A.ols_cluster(y, X, np.array([f"s{v:02d}" for v in (g * 7) % 15]))
    assert np.allclose(a["se"], b["se"])


def test_wild_bootstrap_is_deterministic_and_sane():
    rng = np.random.default_rng(3)
    n = 120
    g = np.repeat(np.arange(24), 5)
    X = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = 0.8 * X[:, 1] + np.repeat(rng.normal(size=24), 5) + rng.normal(size=n)
    p1 = A.wild_cluster_p(y, X, g, 1, np.random.default_rng(9), reps=999)
    p2 = A.wild_cluster_p(y, X, g, 1, np.random.default_rng(9), reps=999)
    assert p1 == p2
    assert p1 < 0.01  # a strong true effect is detected
    # testing the true value of the slope is not rejected
    fit = A.ols_cluster(y, X, g)
    p_at_est = A.wild_cluster_p(y, X, g, 1, np.random.default_rng(9), reps=999, b0=float(fit["beta"][1]))
    assert p_at_est > 0.9


def test_brookings_transcription_obeys_its_identities():
    b = pd.read_csv(LANE / "brookings_surge_metros.csv")
    assert len(b) == 64
    # excess = arrests in onset months 0-6 minus seven twelfths of the 2024 baseline.  The
    # published table itself misses this by 1.2 for Omaha (row re-read from the image at 2x;
    # the printed digits are as entered).
    implied = b["arrests_onset_0_6"] - b["baseline_arrests_2024"] * 7 / 12
    assert (implied - b["excess_level"]).abs().max() <= 1.2
    assert ((implied - b["excess_level"]).abs() > 1.0).sum() == 1
    # excess per 1,000 workers = unrounded excess / employment; the published column departs
    # from this by at most 0.0094 (median 0.0032), so any typo of a digit would show up
    per_k = 1000 * implied / b["employment_2024"]
    assert (per_k - b["excess_per_1k_workers"]).abs().max() <= 0.01
    # employment effect = about -0.432% of employment (the table rounds the rate)
    ratio = b["employment_effect_6m"] / b["employment_2024"]
    assert ratio.between(-0.00434, -0.00430).all(), b.loc[~ratio.between(-0.00434, -0.00430), "metro"]


def test_zillow_matching_rules():
    cbsa = pd.DataFrame({"CBSA": ["12420", "49180", "26420", "11111"],
                         "NAME": ["Austin-Round Rock-San Marcos, TX", "Winston-Salem, NC",
                                  "Houston-Pasadena-The Woodlands, TX", "Huntington-Ashland, WV-KY-OH"]})
    cbsa[["cities", "states"]] = cbsa["NAME"].apply(lambda n: pd.Series(A.split_cbsa(n)))
    assert A.match_zillow("Austin, TX", cbsa) == ("12420", "first-city")
    assert A.match_zillow("Austin, MN", cbsa)[0] is None
    assert A.match_zillow("Winston-Salem, NC", cbsa)[0] == "49180"
    assert A.match_zillow("The Woodlands, TX", cbsa) == ("26420", "any-city")


@pytest.mark.skipif(not (DERIVED / "summary.json").exists(), reason="run analysis.py first")
class TestDerived:
    def test_all_gates_pass(self):
        g = pd.read_csv(DERIVED / "gates.csv")
        assert g["ok"].all(), g[~g["ok"]]

    def test_post_metros_present(self):
        d = pd.read_csv(DERIVED / "dhs_metros.csv")
        assert len(d) == 10
        assert set(A.DHS_FIGURES) <= set(d["metro"])

    def test_no_index_reproduces_the_post(self):
        s = pd.read_csv(DERIVED / "source_check.csv")
        s = s[s["dhs_figure"].notna()]
        assert (s["abs_gap_to_dhs"] > 0.05).all()          # no reading equals a post figure
        close = s.assign(close=s["abs_gap_to_dhs"] <= 0.5).groupby("source")["close"].mean()
        assert (close < 0.5).all(), close                   # no source is within 0.5 on half its readings

    def test_texas_share_of_july_2026_arrests_is_about_a_quarter(self):
        m = pd.read_csv(DERIVED / "arrests_monthly_texas.csv").set_index("month")
        assert 0.23 < m.loc["2026-07", "texas_share_all"] < 0.26
        assert m.loc["2024-01":"2024-12", "texas_share_all"].mean() > m.loc["2026-07", "texas_share_all"]

    def test_stacked_estimates_are_not_negative_in_any_sample(self):
        r = pd.read_csv(DERIVED / "regressions.csv")
        s = r[r["spec"].isin(["S_A", "S_B"]) & ~r["sample"].str.startswith("loso")]
        assert len(s) >= 16
        assert (s["coef"] > 0).all()
        loso = pd.read_csv(DERIVED / "leave_one_state_out.csv")
        assert (loso["S_A_coef"] > 0).all() and (loso["S_B_coef"] > 0).all()

    def test_placebo_gradient_negative_before_the_surge(self):
        r = pd.read_csv(DERIVED / "regressions.csv")
        main = r[(r["sample"] == "main_250k") & (r["treatment"] == "st_y2025")].set_index("spec")
        assert main.loc["P3", "coef"] < main.loc["A3", "coef"] < 0

    def test_july_window_period_supply_and_lost_inflow(self):
        r = pd.read_csv(DERIVED / "regressions.csv").set_index("spec")
        assert r.loc["S_Bjul", "coef"] > 0
        assert r.loc["S_A_ps", "coef"] > 0 and r.loc["S_B_ps", "coef"] > 0
        # lost inflow: no negative change, and ladder 180's mechanical -0.3 per 1 per 1,000 is excluded
        assert r.loc["S_N", "wild_ci_lo"] < 0 < r.loc["S_N", "wild_ci_hi"]
        assert r.loc["S_N", "wild_ci_lo"] > -0.3

    def test_level_contrast_against_2023_is_null_and_excludes_the_post(self):
        r = pd.read_csv(DERIVED / "regressions.csv").set_index("spec")
        lo, hi = r.loc["S_L23", "wild_ci_lo"], r.loc["S_L23", "wild_ci_hi"]
        assert lo < 0 < hi
        g = pd.read_csv(DERIVED / "implied_gradients.csv").set_index("gradient")
        assert g.loc["post's Texas figures, all attributed to Texas's extra arrests", "pp_per_arrest_per_1000"] < lo

    def test_texas_gap_predates_the_surge(self):
        g = pd.read_csv(DERIVED / "texas_gap.csv").set_index("growth")
        assert (g["gap"] < -1.0).all()                                # Texas trails in every year
        assert g.loc["g_aug2024", "gap"] < g.loc["g_aug2026", "gap"]  # widest before the surge
        assert g.loc["g_cal2023", "gap"] < g.loc["g_cal2025", "gap"]
