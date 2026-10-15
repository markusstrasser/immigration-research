"""Regression checks for source alignment and independently computed inference."""

import csv

import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster

from raw_audit import FIELDS, analysis_sample, fit_state_fe, parse_raw


def fixture_row(**updates):
    row = dict(zip(FIELDS, ["0100240", "01500100100000", "03", "19", 101, 2000, 1200, 700, 100]))
    row.update(updates)
    return row


def write_fixture(path, rows, trailer=""):
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([row[key] for key in FIELDS] + [trailer])


def test_trailing_blank_preserves_nces_id_and_amounts(tmp_path):
    path = tmp_path / "raw.csv"
    write_fixture(path, [fixture_row(), fixture_row(NCESID="0100250", V33=99)])
    raw, receipt = parse_raw(path, 2019)
    assert raw.iloc[0].NCESID == "0100240"
    assert raw.iloc[0].V33 == 101
    assert raw.iloc[0].TCURELSC == 2000
    assert receipt["trailing_blank_rows"] == 2
    chosen, _ = analysis_sample(raw)
    assert chosen.NCESID.tolist() == ["0100240"]


def test_nonempty_trailing_column_and_duplicate_ids_fail(tmp_path):
    path = tmp_path / "raw.csv"
    write_fixture(path, [fixture_row()], trailer="unexpected")
    with pytest.raises(ValueError, match="unexpected extra data"):
        parse_raw(path, 2019)
    write_fixture(path, [fixture_row(), fixture_row()])
    with pytest.raises(ValueError, match="duplicate valid NCESID"):
        parse_raw(path, 2019)


def test_component_identity_failure_is_not_silently_trimmed(tmp_path):
    path = tmp_path / "raw.csv"
    write_fixture(path, [fixture_row(TCURELSC=3000)])
    with pytest.raises(ValueError, match="component identity"):
        parse_raw(path, 2019)


def test_state_demeaning_and_cr1_match_explicit_dummy_wls():
    rng = np.random.default_rng(321)
    state = np.repeat(np.arange(8), np.arange(12, 20))
    x = rng.normal(size=len(state)) + state / 3
    weights = rng.uniform(1, 50, size=len(state))
    y = 0.72 * x + state * 2 + rng.normal(size=len(state)) * (1 + state / 3)
    actual = fit_state_fe(y, x, weights, state)
    dummies = (state[:, None] == np.unique(state)[None, :]).astype(float)
    design = np.column_stack([x, dummies])
    model = sm.WLS(y, design, weights=weights).fit()
    expected_se = np.sqrt(cov_cluster(model, state, use_correction=True)[0, 0])
    assert actual["beta"] == pytest.approx(model.params[0], rel=1e-12)
    assert actual["state_cluster_cr1_se"] == pytest.approx(expected_se, rel=1e-12)
    assert actual["parameters"] == design.shape[1]
    assert actual["t_df"] == 7
    # A state-common inflation correction changes intercepts, not the slope.
    deflated = fit_state_fe(y - state * 0.13, x, weights, state)
    assert actual["beta"] == pytest.approx(deflated["beta"], rel=1e-12)
    assert actual["state_cluster_cr1_se"] == pytest.approx(deflated["state_cluster_cr1_se"], rel=1e-12)


def test_known_slope_with_state_intercepts():
    state = np.repeat(["01", "02", "04"], 5)
    x = np.tile(np.arange(5), 3).astype(float)
    y = 0.83 * x + np.repeat([11, 22, 33], 5)
    actual = fit_state_fe(y, x, np.ones(15), state)
    assert actual["beta"] == pytest.approx(0.83)
    assert actual["state_cluster_cr1_se"] < 1e-12
