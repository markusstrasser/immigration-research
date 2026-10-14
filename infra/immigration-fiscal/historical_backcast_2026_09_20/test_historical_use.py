"""Measurement gates: coverage denominator, year gaps, source integrity and 2014 weights."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location("historical_use_tested", Path(__file__).with_name("historical_use.py"))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def test_relative_use_uses_programme_population_denominator():
    assert h.relative_use(100, 20, 50, 15) == (.2, .3, 1.4999999999999998)
    with pytest.raises(ValueError, match="denominator"):
        h.relative_use(100, 20, 0, 0)
    with pytest.raises(ValueError, match="nest"):
        h.relative_use(100, 20, 30, 21)


def test_school_age_bounds_and_2014_half_weights():
    d = pd.DataFrame(dict(YEAR=[2014] * 5, ASECFLAG=[1] * 5, ASECWT=[2.] * 5,
                          AGE=[4, 5, 17, 18, 6], BPL=[20000, 20000, 9900, 9900, 9900],
                          MBPL=[20000, 20000, 9900, 9900, 20000], FBPL=[20000, 20000, 9900, 9900, 9900],
                          HISPAN=[100, 100, 100, 0, 100]))
    r = h.school_sums(d).loc[2013]
    assert r.national_population == 5
    assert r.national_key_population == 3
    assert r.union_population == 4
    assert r.union_key_population == 3
    assert r.g3plus_key_population == 1


def test_missing_year_is_blocked(tmp_path):
    p = tmp_path / "school.csv.gz"
    pd.DataFrame(dict(YEAR=[2025], ASECFLAG=[1], ASECWT=[1], AGE=[6], BPL=[20000],
                      MBPL=[20000], FBPL=[20000], HISPAN=[100])).to_csv(p, index=False)
    with pytest.raises(ValueError, match="missing school years"):
        h.school_measure(p)


def test_pin_detects_changed_source(tmp_path):
    p = tmp_path / "raw"
    p.write_bytes(b"changed")
    with pytest.raises(ValueError, match="source changed"):
        h.verified_source(p, "0" * 64)


def test_coverage_replicate_se_recomputes_ratio():
    d = pd.DataFrame({"MCAID": [1, 2, 1, 2]})
    weights = np.ones((4, 161))
    weights[0, 1:] = 2
    reps = []
    r = h.coverage_row(d, weights, np.array([1, 1, 0, 0], bool), np.ones(4, bool),
                       2025, "union", "test", reps)
    assert r["relative_use"] == 1
    expected = ((2 / 3) / (3 / 5) - 1) * 2
    assert r["relative_use_se"] == pytest.approx(expected)
    assert [value["replicate"] for value in reps] == list(range(161))
    assert reps[0]["relative_use"] == r["relative_use"]
    assert reps[1]["relative_use"] == pytest.approx((2 / 3) / (3 / 5))
    weights[:, 1] = 0
    with pytest.raises(ValueError, match="partition"):
        h.coverage_row(d, weights, np.array([1, 1, 0, 0], bool), np.ones(4, bool), 2025, "union", "test")


def test_group_cannot_escape_national_universe():
    with pytest.raises(ValueError, match="outside"):
        h.partition_gate(np.ones(2), np.array([1, 0], bool), np.array([0, 1], bool))
