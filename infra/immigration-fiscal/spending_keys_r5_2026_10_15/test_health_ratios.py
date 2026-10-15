"""Item 21 pooled-ratio oracle and sparse-cap regression checks."""
import sys

sys.dont_write_bytecode = True

import json
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from health_ratios import Frame, RATIOS, build_ratios, cell_caps, verify_published


@pytest.fixture(scope="module")
def built():
    return build_ratios()


def test_published_plain_ratios_and_standard_errors(built):
    plain = [r for r in built if r["spec"] == "plain"]
    gate = verify_published(plain, pd.read_csv(RATIOS))
    assert gate["checked"] == 10
    assert gate["max_abs_ratio_error"] < 1e-12
    assert gate["max_abs_se_error"] < 1e-12


def test_reproducible_and_json_safe(built):
    assert built == build_ratios()
    json.dumps(built, allow_nan=False)
    assert len(built) == 20
    for row in built:
        assert 0 <= row["n_positive_num"] <= row["n_num"]
        assert 0 <= row["n_positive_den"] <= row["n_den"]
        assert row["n_positive_num"] <= row["n_positive_den"]
        assert row["cap_p995"] is None or row["cap_p995"] >= 0


def test_empty_cell_fails_loudly():
    fr = SimpleNamespace(valid=np.array([], bool), tb=np.array([], int),
                         born=np.array([], int), y={"ofd_stl": np.array([])}, w=np.array([]))
    with pytest.raises(ValueError, match="empty pooled transport cell"):
        cell_caps(fr, "ofd_stl")


def test_zero_quantile_does_not_erase_sparse_positive_spending():
    # One positive of 1,000 donors => q=.995 is zero. The producer intentionally
    # leaves such a cell uncapped; applying min(y, 0) would erase all its use.
    y = np.tile(np.r_[np.zeros(999), 100.0], 10)
    fr = SimpleNamespace(valid=np.ones(10000, bool), tb=np.repeat(np.arange(5), 2000),
                         born=np.tile(np.repeat([1, 2], 1000), 5),
                         y={"ofd_stl": y}, w=np.ones(10000))
    caps = cell_caps(fr, "ofd_stl")
    assert set(caps.values()) == {0.0}
    assert np.array_equal(Frame.capped(fr, "ofd_stl", caps), y)


def test_positive_caps_use_all_donors_and_source_capping():
    y = np.tile(np.arange(1000.0), 10)
    fr = SimpleNamespace(valid=np.ones(10000, bool), tb=np.repeat(np.arange(5), 2000),
                         born=np.tile(np.repeat([1, 2], 1000), 5),
                         y={"ofd_stl": y}, w=np.ones(10000))
    caps = cell_caps(fr, "ofd_stl")
    assert set(caps.values()) == {994.0}
    assert np.array_equal(Frame.capped(fr, "ofd_stl", caps), np.minimum(y, 994.0))


def test_oracle_mismatch_fails_loudly(built):
    changed = dict(built[0], ratio=built[0]["ratio"] + 0.1)
    with pytest.raises(ValueError, match="pooled oracle mismatch"):
        verify_published([changed], pd.read_csv(RATIOS))
