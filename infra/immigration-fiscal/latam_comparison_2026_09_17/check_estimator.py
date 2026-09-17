#!/usr/bin/env python3
"""Deterministic arithmetic checks; no desired country ranking in assertions."""
import numpy as np
import pandas as pd
from analyze import estimates, linearized_estimates, masks, uncertainty


def main():
    # Unequal stratum counts distinguish standardization from a crude average.
    full = np.zeros((1, 8, 2, 161))
    full[:, 0, 0] = 20
    full[:, 0, 1] = 80
    full[:, 1, 0] = 10
    full[:, 1, 1] = 8
    full[:, 4] = full[:, 0]
    shares = np.array([.5, .5])
    crude = estimates(full, [0, 1], "crude", shares)
    standard = estimates(full, [0, 1], "age_sex_standardized", shares)
    assert np.allclose(crude[:, 0], .18)
    assert np.allclose(standard[:, 0], .30)
    # A fixed-denominator numerator perturbation has an exactly linear effect.
    delta = np.zeros_like(full)
    delta[:, 1, 0, 1:] = 2
    direct = estimates(full + delta, [0, 1], "age_sex_standardized", shares) - standard
    linear = linearized_estimates(full[..., 0], delta, [0, 1], "age_sex_standardized", shares)
    assert np.allclose(direct, linear)
    # Single-block SDR and unknown-covariance sum agree with hand arithmetic.
    vector = np.ones((2, 161))
    vector[0, 1:] += .1
    vector[1, 1:] += .2
    upper, independent = uncertainty(vector)
    assert np.isclose(upper, .6)
    assert np.isclose(independent, np.sqrt(.2 ** 2 + .4 ** 2))
    assert np.isclose(uncertainty(vector - vector)[0], 0)
    # Empty stratum is unavailable, never silently renormalized.
    empty = full.copy()
    empty[:, 0, 1] = 0
    assert np.isnan(estimates(empty, [0, 1], "age_sex_standardized", shares)[:, 0]).all()
    # Mixed-origin G2 belongs in both countries but once in aggregate;
    # unknown parent birth cannot enter the established-native benchmark.
    data = pd.DataFrame(dict(PENATVTY=[57, 57, 303, 57], PEFNTVTY=[303, 57, 303, 57],
                             PEMNTVTY=[327, 57, 303, -1], PRCITSHP=[1, 1, 5, 1],
                             PEHSPNON=[1, 2, 1, 2], PRDTRACE=[1, 1, 1, 1]))
    group = masks(data)
    assert group["g2_Mexico"].tolist() == [True, False, False, False]
    assert group["g2_Cuba"].tolist() == [True, False, False, False]
    assert group["g2_LATAM"].sum() == 1
    assert not group["g2_two_Mexico"].any()
    assert not group["g2_one_us_Mexico"].any()
    data.loc[0, "PEMNTVTY"] = 303
    assert masks(data)["g2_two_Mexico"].iloc[0]
    data.loc[0, "PEMNTVTY"] = 57
    assert masks(data)["g2_one_us_Mexico"].iloc[0]
    assert group["white_us_parents"].tolist() == [False, True, False, False]
    assert group["g1_Mexico"].tolist() == [False, False, True, False]
    print("PASS: standardization, replication, sparse failure, mixed origins and benchmark gates")


if __name__ == "__main__":
    main()
