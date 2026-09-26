"""Tests for compare.py: band mapping, the SDR formula on a toy case, standardization weights,
and gates that fail loudly. None of them reads the PUMS zips.

  uv run --no-project python3 -m pytest infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/ -q
"""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare as C  # noqa: E402

# The brief's main mapping, written out independently of compare.py.
EXPECTED_BAND = {
    1: "lt_lower_secondary", 2: "lt_lower_secondary", 3: "lt_lower_secondary", 4: "lt_lower_secondary",
    5: "lt_lower_secondary", 6: "lt_lower_secondary", 7: "lt_lower_secondary", 8: "lt_lower_secondary",
    9: "lt_lower_secondary", 10: "lt_lower_secondary", 11: "lt_lower_secondary", 12: "lower_secondary",
    13: "upper_secondary", 14: "upper_secondary", 15: "upper_secondary", 16: "upper_secondary",
    17: "upper_secondary", 18: "upper_secondary", 19: "tertiary", 20: "tertiary", 21: "tertiary",
    22: "tertiary", 23: "tertiary", 24: "tertiary",
}


def test_band_mapping_matches_brief():
    assert C.SCHL_BAND == EXPECTED_BAND
    C.check_schooling_maps()


def test_years_scale_reused_from_schooling_lane():
    assert (C.SCHL_YEARS[1], C.SCHL_YEARS[9], C.SCHL_YEARS[12], C.SCHL_YEARS[16]) == (0.0, 6.0, 9.0, 12.0)
    assert (C.SCHL_YEARS[18], C.SCHL_YEARS[19], C.SCHL_YEARS[21], C.SCHL_YEARS[24]) == (12.0, 14.0, 16.5, 16.5)


def test_outcome_codings():
    schl = np.array([1, 12, 16, 17, 18, 19])
    main = C.outcomes(schl, "main")
    assert np.allclose(main[:, :4].sum(axis=1), 1.0)
    assert main[4, C.BAND_ORDER.index("upper_secondary")] == 1.0
    a = C.outcomes(schl, "a")
    assert a[4, C.BAND_ORDER.index("tertiary")] == 1.0 and a[4, C.YEARS_COL] == 13.0
    assert np.array_equal(a[:4], main[:4])
    b = C.outcomes(schl, "b")
    for i in (2, 3):  # SCHL 16 and 17: half lower secondary, half upper secondary, 10.5 years
        assert b[i, C.BAND_ORDER.index("lower_secondary")] == 0.5
        assert b[i, C.BAND_ORDER.index("upper_secondary")] == 0.5
        assert b[i, C.YEARS_COL] == 10.5
    assert np.allclose(b[:, :4].sum(axis=1), 1.0)
    e = C.outcomes(schl, "e", break_years=2.5)
    assert e[0, C.YEARS_COL] == 2.5 and np.array_equal(e[1:], main[1:]) and np.array_equal(e[:, :4], main[:, :4])
    with pytest.raises(C.GateFailure):
        C.outcomes(schl, "e")


def test_sdr_formula_toy_case():
    y = np.array([[1.0], [0.0]])
    W = np.ones((2, 81))
    W[:, 1] = [3.0, 1.0]    # replicate 1: 0.75
    W[:, 2] = [-1.0, 3.0]   # replicate 2, a negative replicate weight kept: -0.5
    theta = C.estimate(y, W)
    assert theta[0, 0] == 0.5 and theta[0, 1] == 0.75 and theta[0, 2] == -0.5
    expected = math.sqrt(4 / 80 * (0.25 ** 2 + 1.0 ** 2))
    assert C.sdr_se(theta)[0] == pytest.approx(expected, rel=1e-12)


def test_sdr_needs_81_columns_and_positive_totals():
    with pytest.raises(C.GateFailure):
        C.sdr_se(np.zeros((1, 80)))
    with pytest.raises(C.GateFailure):
        C.estimate(np.ones((2, 1)), np.zeros((2, 81)))


def test_standardization_weights_sum_to_one():
    ret, _, _ = C.load_returnees()
    for wave in C.WAVES:
        for s, (_, cells) in C.STANDARDIZED.items():
            p = C.standardization_weights(ret, wave, cells)
            assert p.shape == (len(cells), len(C.MEASURES))
            assert np.allclose(p.sum(axis=0), 1.0, atol=1e-12)
            assert (p >= 0).all()


def test_standardize_is_a_weighted_average():
    t1, t2 = np.full((5, 81), 0.2), np.full((5, 81), 0.6)
    p = np.array([[0.25] * 5, [0.75] * 5])
    assert np.allclose(C.standardize([t1, t2], p), 0.5)


def test_undercount_multiplier_touches_only_low_band_noncitizens():
    cit = np.array([5, 5, 5, 4, 3, 5])
    schl = np.array([9, 12, 16, 9, 12, 21])
    assert list(C.undercount_multiplier(cit, schl, 1.75)) == [1.75, 1.75, 1.0, 1.0, 1.0, 1.0]


def test_enadid_gates_pass_and_fail_loudly():
    ret, linked, coverage = C.load_returnees()
    text = C.ENADID_RESULT.read_text(encoding="utf-8")
    assert len(C.gate_returnees(ret, linked, coverage, C.parse_enadid_result(text))) >= 40
    tampered = text.replace("| Tertiary | 11.18 | 1.46 |", "| Tertiary | 11.28 | 1.46 |", 1)
    assert tampered != text
    with pytest.raises(C.GateFailure):
        C.gate_returnees(ret, linked, coverage, C.parse_enadid_result(tampered))
    with pytest.raises(C.GateFailure):  # a missing table stops the parse
        C.parse_enadid_result(text.split("### By sex")[0])
    bad = dict(ret)
    key = (2018, "sex:men|age:30-39", "tertiary")
    bad[key] = {**bad[key], "estimate": bad[key]["estimate"] + 0.01}
    with pytest.raises(C.GateFailure):  # a cell that no longer aggregates to its slice
        C.gate_returnees(bad, linked, coverage, C.parse_enadid_result(text))


def _fake_mx(total: float) -> dict:
    W = np.full((2, 81), total / 2)
    W[0, 1:] += np.linspace(-1000, 1000, 80)  # replicate totals that vary, as real ones do
    return {"cit": np.array([4, 5]), "W": W}


def test_anchor_gate():
    pub = C.ANCHOR[2018]["estimate"]
    row = C.anchor_row(2018, _fake_mx(pub * 1.001))
    assert row["within_tolerance"] and row["gap"] == round(pub * 0.001)
    with pytest.raises(C.GateFailure):
        C.anchor_row(2018, _fake_mx(pub * 1.01))


def test_pums_sha_gate(tmp_path, monkeypatch):
    fake = tmp_path / "csv_pus_2018.zip"
    fake.write_bytes(b"not the pinned file")
    monkeypatch.setitem(C.PUMS, 2018, {**C.PUMS[2018], "zip": fake})
    with pytest.raises(C.GateFailure):
        C.read_mexico_born(2018, {"pums": {}})


def test_schooling_map_gate(monkeypatch):
    monkeypatch.setitem(C.SCHL_BAND, 18, "tertiary")
    with pytest.raises(C.GateFailure):
        C.check_schooling_maps()


def test_derived_files_use_lf():
    for p in sorted((HERE / "derived").glob("*")):
        assert b"\r\n" not in p.read_bytes(), p.name
