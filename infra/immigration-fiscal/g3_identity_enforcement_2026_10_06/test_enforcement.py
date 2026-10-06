"""Checks for the enforcement-identification lane: the estimator on synthetic data with known answers, and the
derived outputs against the pooled lane's published counts.

Run from the repository root (after analyze.py):
  uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/ -q
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
POOLED = HERE.parent / "g3_identity_pooled_2026_10_05" / "derived"

spec = importlib.util.spec_from_file_location("g3_enforcement_analyze", HERE / "analyze.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def synthetic(drop: float, seed: int = 7, households: int = 6000, slope: float = 0.0) -> tuple[pd.DataFrame, np.ndarray]:
    """Households of 1-4 people interviewed once in 2019-01..2026-08; identification is a household-level draw with
    rate 0.86 (+ slope per year since 2019), lowered by `drop` from February 2025."""
    rng = np.random.default_rng(seed)
    size = rng.integers(1, 5, households)
    t_hh = rng.integers(m.ym(2019, 1), m.ym(2026, 8) + 1, households)
    p = 0.86 + slope * (t_hh - m.ym(2019, 1)) / 12 - drop * (t_hh >= m.DRIVE)
    y_hh = (rng.random(households) < p).astype(float)
    hh = np.repeat(np.arange(households), size)
    r = pd.DataFrame({"t": t_hh[hh], "cluster": hh + 10**9, "age_band": rng.integers(0, 7, len(hh)),
                      "sex": rng.integers(1, 3, len(hh)), "state_group": rng.integers(0, 3, len(hh))})
    return r, y_hh[hh]


@pytest.mark.parametrize("baseline", ["mean", "trend"])
def test_planted_drop_is_recovered(baseline):
    """Positive control: a 6 pp household-level drop from February 2025 is recovered within 3 SE, and detected."""
    r, y = synthetic(drop=0.06)
    est, se = m.window_effect(r, y, np.ones(len(r)), (m.DRIVE, m.ym(2026, 8)), baseline, False)[:2]
    assert abs(est + 6.0) < 3 * se
    assert est / se < -1.96


def test_null_is_not_detected():
    r, y = synthetic(drop=0.0, seed=11)
    for baseline in ("mean", "trend", "same_months"):
        est, se = m.window_effect(r, y, np.ones(len(r)), (m.DRIVE, m.ym(2026, 8)), baseline, False)[:2]
        assert abs(est / se) < 3


def test_trend_baseline_extrapolates_exactly():
    """With no noise, a linear baseline and a window shifted by -4 pp off its extrapolation, the trend test returns
    -4 exactly, whatever the window's own slope."""
    t = np.arange(m.ym(2019, 1), m.ym(2026, 8) + 1)
    tt = (t - m.TREND[0]) / 12
    y = 0.80 + 0.01 * tt
    win = t >= m.DRIVE
    y = np.where(win, y - 0.04 + 0.003 * (tt - tt[win].mean()), y)
    r = pd.DataFrame({"t": t, "cluster": np.arange(len(t))})
    est = m.window_effect(r, y, np.ones(len(t)), (m.DRIVE, m.ym(2026, 8)), "trend", False)[0]
    assert est == pytest.approx(-4.0, abs=1e-9)


def test_cluster_robust_variance_matches_hand_formula():
    """CR1 variance of a difference in means when no cluster spans both groups."""
    rng = np.random.default_rng(3)
    cl = np.repeat(np.arange(400), 3)
    D = (cl >= 250).astype(float)
    y = (rng.random(len(cl)) < 0.8).astype(float)
    X = np.column_stack([np.ones(len(cl)), D])
    beta, V = m.wls(y, X, np.ones(len(cl)), cl)
    n1, n0 = D.sum(), (1 - D).sum()
    e = y - np.where(D == 1, y[D == 1].mean(), y[D == 0].mean())
    eg = pd.Series(e).groupby(cl).sum().to_numpy()
    g1 = pd.Series(D).groupby(cl).first().to_numpy() == 1
    G, n = 400, len(cl)
    hand = G / (G - 1) * (n - 1) / (n - 2) * ((eg[g1] ** 2).sum() / n1 ** 2 + (eg[~g1] ** 2).sum() / n0 ** 2)
    assert beta[1] == pytest.approx(y[D == 1].mean() - y[D == 0].mean())
    assert V[1, 1] == pytest.approx(hand, rel=1e-10)


def test_pooled_lane_counts_reproduced():
    """Positive control on the data: analyze.py's G3 rows reproduce the pooled lane's published counts."""
    gates = pd.read_csv(DERIVED / "gates.csv")
    assert gates.passed.all()
    pub = pd.read_csv(POOLED / "monthly_counts.csv").set_index(["rows", "years", "min_age"])
    got = gates.set_index("gate").value
    assert int(got["pooled monthly_counts.csv monthly_nodedup 2022_2025 18+ G3anc"]) == \
        int(pub.loc[("monthly_nodedup", "2022_2025", 18), "G3anc"]) == 1380
    assert int(got["pooled monthly_counts.csv monthly_mis1 2022_2025 18+ G3anc_id"]) == \
        int(pub.loc[("monthly_mis1", "2022_2025", 18), "G3anc_id"])


@pytest.mark.skipif(not (HERE / "_cache" / "monthly_hh.parquet").exists(), reason="stage.py has not been run")
def test_series_month_rebuilt_from_staged_rows():
    """One month of the published series rebuilt from the staged rows through the pooled lane's classify."""
    d = pd.read_parquet(HERE / "_cache" / "monthly_hh.parquet", filters=[("YEAR", "=", 2025), ("MONTH", "=", 3)])
    rows = m.persons(d, "monthly")
    g3 = rows[rows.g3_mex & (rows.mish == 1)]
    s = pd.read_csv(DERIVED / "series_monthly.csv")
    pub = s[(s.group == "g3_mex") & (s.frame == "all") & (s.outcome == "mexican") & (s.mis == "1")
            & (s.weight == "unweighted") & (s.month == "2025-03")].iloc[0]
    assert len(g3) == pub.n
    assert g3.mexican.mean() == pytest.approx(pub.share, rel=1e-5)


def test_identity_is_carried_forward():
    """Design fact the timing rests on: fewer than 2% of G3-lineage persons change Mexican identification between
    their MIS 1 and MIS 5 records."""
    c = pd.read_csv(DERIVED / "carry_forward.csv")
    row = c[(c.link == "CPSIDV") & (c.group == "g3_mex") & (c.mis1_year == "2003-2025")].iloc[0]
    assert row.linked > 10_000 and row.share_mexican_changed < 0.02


def test_audit_covers_latest_month():
    audit = json.loads((DERIVED / "audit.json").read_text())
    assert audit["last_month"] == "2026-08"
    assert audit["windows"]["feb_2025_latest"] == ["2025-02", "2026-08"]
