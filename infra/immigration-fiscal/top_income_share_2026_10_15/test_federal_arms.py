import numpy as np
import pytest

from federal_arms import move_bin_share, nonincreasing, rake


def test_rake_preserves_both_margins_and_structural_zeros():
    x = np.array([[1., 1., 0.], [0., 1., 2.]])
    r = rake(x, [.3, .7], [.2, .3, .5])
    np.testing.assert_allclose(r.sum(axis=0), [.2, .3, .5], atol=1e-12)
    np.testing.assert_allclose(r.sum(axis=1), [.3, .7], atol=1e-12)
    assert r[0, 2] == r[1, 0] == 0


def test_isotonic_pools_only_violations_and_preserves_weighted_total():
    y, w = np.array([.04, .02, .035]), np.array([.24, .13, .31])
    out = nonincreasing(y, w)
    assert np.all(np.diff(out) <= 0)
    assert out[0] == y[0]
    assert out[1] == out[2]
    assert w @ out == pytest.approx(w @ y)


def test_cell_move_conserves_national_mass_and_hits_union_target():
    mass, theta = np.array([.1, .3]), np.array([0., .08])
    for target in [0., .01, .06, .3, 1.]:
        moved = move_bin_share(theta, mass, target)
        assert mass @ moved / mass.sum() == pytest.approx(target)
        assert np.all((moved >= 0) & (moved <= 1))
        assert (mass * moved + mass * (1-moved)).sum() == pytest.approx(mass.sum())


def test_unsupported_margin_stops():
    with pytest.raises(ValueError, match="unsupported"):
        rake([[1., 0.], [2., 0.]], [.5, .5], [.5, .5])
