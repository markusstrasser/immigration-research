"""Observed SNAP take-up, residual identity and explicit pooling regressions."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location('tested_snap_arm', Path(__file__).with_name('snap_arm.py'))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_observed_takeup_uses_weights_and_original_reference_size():
    state = np.array([6, 6, 6, 6])
    size = np.array([1, 1, 2, 1])
    refs = np.array([1, 1, 1, 3])
    weights = np.repeat(np.array([[1.], [3.], [2.], [10.]]), 161, axis=1)
    lo, hi, rows = M.observed_takeup(state, size, np.array([1, 1, 1, 0], bool),
                                    np.array([1, 0, 1, 0], bool), weights,
                                    np.array([0, 0, 0, 1], bool), minimum=2, reference_size=refs)
    assert lo[-1] == hi[-1] == .5  # (1+2)/(1+3+2), no target unit included.
    assert rows[0]['tier'] == 'state_size'
    assert rows[0]['eligible_sample_units'] == 3


def test_sparse_state_size_is_explicitly_pooled():
    state = np.array([6, 6, 6, 32])
    size = np.array([2, 3, 3, 1])
    w = np.ones((4, 161))
    _, _, rows = M.observed_takeup(state, size, np.array([1, 1, 1, 0], bool),
                                  np.array([0, 1, 1, 0], bool), w,
                                  np.array([1, 0, 0, 0], bool), minimum=2)
    assert rows[0]['tier'] == 'state'
    assert rows[0]['takeup'] == pytest.approx(2/3)


def test_zero_support_blocks_instead_of_silent_rate():
    with pytest.raises(ValueError, match='no supported SNAP'):
        M.observed_takeup(np.array([6]), np.array([1]), np.array([False]),
                          np.array([False]), np.ones((1, 161)), np.array([True]))


def test_after_benefit_no_event_identity_includes_proxy_mismatch():
    B = np.array([120., 0., 60.])
    r = np.array([100., 100., 0.])
    lo, hi, new, lost = M.after_benefit(B, r, r, np.full(3, 200.),
                                       np.full(3, .4), np.full(3, .6))
    np.testing.assert_array_equal(lo, B)
    np.testing.assert_array_equal(hi, B)
    assert not new.any() and not lost.any()


def test_new_eligibility_starts_at_observed_takeup_loss_stops_recipient():
    lo, hi, new, lost = M.after_benefit(np.array([0., 120., 0.]),
                                       np.array([0., 100., 80.]), np.array([100., 0., 120.]),
                                       np.full(3, 200.), np.full(3, .4), np.full(3, .6))
    np.testing.assert_array_equal(lo, [40., 0., 0.])
    np.testing.assert_array_equal(hi, [60., 0., 0.])
    assert new.tolist() == [True, False, False]
    assert lost.tolist() == [False, True, False]


def test_takeup_retains_signed_replicates_but_blocks_nonpositive_pool():
    weights = np.ones((2, 161))
    weights[:, 1] = [-2, 1]
    with pytest.raises(ValueError, match='nonpositive replicate denominator'):
        M.observed_takeup(np.array([6, 6]), np.array([1, 1]), np.ones(2, bool),
                          np.array([True, False]), weights, np.ones(2, bool), minimum=2)
