"""Positive controls: the lane's CPS vectors reproduce the account's published target shares,
the CBO parse reproduces the published cells, the translation is an identity at no change, the
hospital reports' numbers are found verbatim, and the hospital translation reproduces the adopted
uncompensated-care part at equal use.

Run from the repository root:
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow --with pytest \
  python3 -m pytest infra/immigration-fiscal/external_benchmarks_2026_09_24/test_benchmarks.py -q
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402
import cbo_arm  # noqa: E402

RECEIPT_KEYS = f.FISCAL / "full_account_receipts_2026_09_20/derived/allocation_keys.csv"
SPENDING_KEYS = f.FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"


@pytest.fixture(scope="module")
def cps():
    d = f.load()
    civ, target = f.masks(d)
    return d, civ, target, d.pwwgt0.to_numpy(float)


def share(v, w, civ, target):
    return float((v[target] @ w[target]) / (v[civ] @ w[civ]))


def test_target_population(cps):
    d, civ, target, w = cps
    assert abs(w[target].sum() - f.TARGET_POP) < .02


def test_receipt_keys_reproduce_published(cps):
    d, civ, target, w = cps
    keys = f.receipt_keys(d)
    published = pd.read_csv(RECEIPT_KEYS).query("allocation_key != 'resident_population'")
    assert len(published) == 28
    for row in published.itertuples():
        got = share(keys[row.allocation][row.allocation_key], w, civ, target)
        assert abs(got - row.target_key_share) < 1e-9, (row.allocation, row.allocation_key, got)


def test_spending_keys_reproduce_published(cps):
    d, civ, target, w = cps
    keys = f.spending_keys(d)
    published = pd.read_csv(SPENDING_KEYS)
    published = published[~published.key.isin(["school_operating", "postsecondary", "education_mix"])]
    assert len(published) == 52  # 26 CPS and MEPS keys x 2 allocations
    for row in published.itertuples():
        got = share(keys[row.allocation][row.key], w, civ, target)
        assert abs(got - row.target_share) < 1e-9, (row.allocation, row.key, got)


def test_cbo_cells_match_published_csv():
    cbo = cbo_arm.cbo_shares(2022)
    assert cbo.loc["top1", "individual_inc_tax"] == pytest.approx(0.403)
    assert cbo.loc["q1", "medicaid_and_chip"] == pytest.approx(0.445)
    assert cbo.loc["q5", "payroll_taxes"] == pytest.approx(0.453)
    # Q5's detail groups partition it within the 0.1-point rounding of each cell.
    for col in ["individual_inc_tax", "payroll_taxes", "excise_taxes", "medicaid_and_chip", "snap"]:
        parts = cbo.loc[["p81_90", "p91_95", "p96_99", "top1"], col].sum()
        assert abs(parts - cbo.loc["q5", col]) <= 0.0025, col
    # Social-insurance shares built from averages x households sum to one with the residual,
    # up to the rounding of the four Q5 detail cells against the Q5 cell.
    assert cbo.loc[f.GROUPS, "social_security"].sum() == pytest.approx(1.0, abs=0.01)


def test_groups_hold_equal_people(cps):
    d, civ, target, w = cps
    g, _ = cbo_arm.groups(d)
    people = pd.Series(w).groupby(g).sum() / w.sum()
    for q in ["q2", "q3", "q4"]:
        assert abs(people[q] - .2) < .01, (q, people[q])
    assert abs(people[["p81_90", "p91_95", "p96_99", "top1"]].sum() - .2) < .01


def test_reweight_is_identity_without_change(cps):
    d, civ, target, w = cps
    g, _ = cbo_arm.groups(d)
    v = f.receipt_keys(d)["personal"]["federal_liability"]
    pi, theta = cbo_arm.decompose(v, w, civ, target, g)
    assert cbo_arm.reweighted_share(pi, theta) == pytest.approx(share(v, w, civ, target), abs=1e-12)


def test_hospital_report_numbers_found_verbatim():
    import hospital_arm
    for name in hospital_arm.REPORTS:
        assert hospital_arm.report(name) == hospital_arm.REPORTS[name][0]


def test_hospital_translation_reproduces_adopted_uncompensated_part(cps):
    import hospital_arm
    d, civ, target, w = cps
    un, _ = f.status(d)
    un = un & civ
    exposure = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    py = {k: (w[m] * exposure[m]).sum() / 1e6 for k, m in
          [("all", civ), ("u", un), ("t", target), ("tu", un & target)]}
    lines = {l["id"]: l for l in f.model()["spending"]["lines"]}
    keys = {"medicaid": "medicaid_and_chip_other_medical", "medicare": "medicare", "health_other": "health_services"}
    keys = {k: lines[l]["keys"][lines[l]["preferred_key"]]["personal"]["target_bn"] / lines[l]["national_bn"]
            for k, l in keys.items()}
    keys["per_head"] = hospital_arm.PER_HEAD_SHARE
    summary = pd.read_json(hospital_arm.UC_SUMMARY, typ="series")
    lo, hi, _ = hospital_arm.inside_arms(py["tu"], py["t"] - py["tu"], py["u"], py["all"] - py["u"], keys)
    assert (lo, hi) == pytest.approx(tuple(summary["inside_undercharged_bn_use_1.0"]), abs=1e-9)


def test_node_gate_reproduces_adopted_bands(tmp_path):
    empty = tmp_path / "zero.json"
    empty.write_text('{"zero": {"receipts": {}, "spending": {}}}')
    out = tmp_path / "out.csv"
    done = subprocess.run(["node", str(f.HERE / "translate_main_case.js"), str(empty), str(out)],
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    rows = pd.read_csv(out)
    assert np.allclose(rows.change_low_bn, 0, atol=1e-6) and np.allclose(rows.change_high_bn, 0, atol=1e-6)
