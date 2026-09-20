"""Check derivatives, missing-age envelopes, and full-frame survey variance."""
from itertools import product
import numpy as np
import pandas as pd
from estimate import Design, age_bands, masks_for_case, ratio_influence


def test_ratio_derivative():
    w = np.array([2., 3., 5., 7.])
    num, den = np.array([1, 0, 0, 0]), np.array([1, 1, 1, 0])
    p, influence = ratio_influence(w, num, den)
    np.testing.assert_allclose(influence.sum(), 0, atol=1e-14)
    assert influence[-1] == 0
    eps = 1e-6
    for i in range(len(w)):
        high, low = w.copy(), w.copy()
        high[i] *= np.exp(eps); low[i] *= np.exp(-eps)
        numerical = (ratio_influence(high, num, den)[0]
                     - ratio_influence(low, num, den)[0])/(2*eps)
        np.testing.assert_allclose(numerical, influence[i], atol=1e-9)
    assert p == .2


def test_missing_age_outer_envelope():
    # Four occupied age cells, unknown grandparents and unknown ages together.
    age = np.array([0, 0, 1, 1, 2, 2, 3, 3, -1, -1, -1])
    generation = np.array([3, 4, 3, 0, 3, 4, 3, 4, 3, 4, 0])
    w = np.arange(1., 12.)
    target = np.array([.2, .4, .3, .1])
    domain = np.ones(len(w), bool)
    bounds = []
    for case in ['unknown_age_outer_lower', 'unknown_age_outer_upper']:
        p = [ratio_influence(w, *masks_for_case(
            domain, age, h, generation == 3, generation == 4, case))[0]
             for h in range(4)]
        bounds.append(target @ p)
    for age_values in product(range(4), repeat=3):
        complete_age = age.copy(); complete_age[age < 0] = age_values
        for gp_values in product([3, 4], repeat=2):
            complete_gen = generation.copy(); complete_gen[generation == 0] = gp_values
            fractions = [np.average((complete_gen == 4)[complete_age == h],
                                    weights=w[complete_age == h]) for h in range(4)]
            point = target @ fractions
            assert bounds[0]-1e-12 <= point <= bounds[1]+1e-12


def test_full_frame_variance():
    frame = pd.DataFrame(dict(year=[2021]*5, vstrat=[1, 1, 1, 2, 2],
                              vpsu=[1, 2, 3, 1, 2], w=np.ones(5)))
    # Outside-domain PSUs remain as zeros; 2021 need not have two PSUs/stratum.
    influence = np.array([[2., 1.], [0., 0.], [0., 0.], [3., -2.], [-1., 4.]])
    expected = np.zeros((2, 2))
    for indices in [[0, 1, 2], [3, 4]]:
        values = influence[indices]
        centered = values-values.mean(axis=0)
        expected += len(indices)/(len(indices)-1)*centered.T@centered
    np.testing.assert_allclose(Design(frame).cov(influence), expected, atol=1e-12)
    a = np.array([.3, .7])
    np.testing.assert_allclose(Design(frame).cov((influence@a)[:, None])[0, 0],
                               a@expected@a, atol=1e-12)
    np.testing.assert_array_equal(age_bands([17, 18, 24, 25, 44, 45, 64, 65, 89, np.nan]),
                                  [-1, 0, 0, 1, 1, 2, 2, 3, 3, -1])


if __name__ == '__main__':
    test_ratio_derivative()
    test_missing_age_outer_envelope()
    test_full_frame_variance()
    print('PASS: ratio derivatives, 256 ancestry/age completions, full-frame variance, age boundaries')
