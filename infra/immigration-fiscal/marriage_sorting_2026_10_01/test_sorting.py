"""Statistical failure guards for sorting.py; no raw-input writes."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location("sorting", Path(__file__).with_name("sorting.py"))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def test_random_matching_is_one_at_different_base_rates():
    for share in (.01, .1, .5, .9):
        totals = np.array([100., 100 * share, 100 * share])
        assert s.metric(totals, "log_K") == pytest.approx(0)


def test_ratio_replicates_preserve_reference_covariance():
    a = np.tile(np.array([100., 65., 8.])[:, None], (1, 161))
    a[1, 1:] += np.linspace(-2, 2, 160)
    b = a.copy() * 2
    point, se = s.pooled_value_se([a, b], "log_K", [a, b])
    assert point == pytest.approx(0)
    assert se == pytest.approx(0)
    point, se = s.pooled_value_se([a, b], "p")
    expected = 3 * np.sqrt(4 / 160 * np.square(a[1, 1:] - a[1, 0]).sum()) / 300
    assert point == pytest.approx(.65)
    assert se == pytest.approx(expected)


def test_spouse_stratum_changes_pool_and_replicates_recompute_it():
    pool = pd.DataFrame({"GESTFIPS": [1] * 4, "A_SEX": [2] * 4,
                         "ba": [0, 0, 1, 1], "ind_origin": [1, 0, 0, 0],
                         "mex_origin": [0] * 4, "nh_white": [0, 1, 1, 1], "nh_black": [0] * 4})
    weights = pd.DataFrame(np.ones((4, 161)), columns=s.base.WCOLS)
    weights.loc[0, "pwwgt1"] = 3
    pool = pd.concat([pool, weights], axis=1)
    ego = pd.DataFrame({"GESTFIPS": [1], "A_SEX": [1], "ba": [1], "sp_ba": [0]})
    q, pos, valid, _, _ = s.peer_shares(pool, ego, ("ba",), False)
    assert valid.all()
    assert q[pos[0], 0, 0] == pytest.approx(.5)
    assert q[pos[0], 0, 1] == pytest.approx(.75)
    own, ownpos, _, _, _ = s.peer_shares(pool, ego, ("ba",), True)
    assert own[ownpos[0], 0, 0] == 0


def test_missing_spouse_pool_fails_but_own_pool_is_explicitly_missing():
    pool = pd.DataFrame({"GESTFIPS": [1], "A_SEX": [2], **{f: [False] for f in s.FLAGS},
                         **{w: [1.] for w in s.base.WCOLS}})
    ego = pd.DataFrame({"GESTFIPS": [2], "A_SEX": [1]})
    with pytest.raises(ValueError, match="comparison cell missing"):
        s.peer_shares(pool, ego, (), False)
    _, _, valid, _, _ = s.peer_shares(pool, ego, (), True)
    assert not valid.any()


def test_unestimable_odds_and_nonpositive_pool_fail_loudly():
    with pytest.raises(ValueError, match="Boundary"):
        s.metric(np.array([100., 100., 5.]), "log_K")
    pool = pd.DataFrame({"GESTFIPS": [1], "A_SEX": [2], **{f: [False] for f in s.FLAGS},
                         **{w: [0.] for w in s.base.WCOLS}})
    ego = pd.DataFrame({"GESTFIPS": [1], "A_SEX": [1]})
    with pytest.raises(ValueError, match="Nonpositive replicate"):
        s.peer_shares(pool, ego, (), False)
