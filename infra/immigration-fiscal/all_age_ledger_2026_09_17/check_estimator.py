"""Hand-calculable regressions for the estimand and its failure boundaries."""
import numpy as np
from estimator import account, contrast, standardized_gap, sufficient, summarize, sum_cells


def cell(n, y, h):
    return {"n": np.repeat(np.array(n, float)[:, None], 161, axis=1),
            "y": np.repeat(np.array(y, float)[:, None, None], 161, axis=2),
            "h": np.repeat(np.array(h, float)[:, None, None], 161, axis=2)}


def main():
    # Band means: target30/10, reference10/20. Ntarget2/1, Nref4/2.
    target, ref = cell([2, 1], [60, 10], [2, 1]), cell([4, 2], [40, 40], [2, 1])
    gap, q = contrast(target, ref, [1], [0])
    assert np.allclose(gap, 30) and np.allclose(q, -1.5)
    shifted, _ = contrast(target, ref, [1], [2])
    assert np.allclose(shifted-gap, 2*q)
    std, sq = standardized_gap(target, ref, [1], [0], [.5, .5])
    assert np.allclose(std, 5) and np.allclose(sq, -.5)
    # Recompute ratio in each replicate: target band0 N goes2→3 but Y fixed.
    changed = {k: v.copy() for k, v in target.items()}
    changed["n"][0, 1] = 3
    g, _ = contrast(changed, ref, [1], [0])
    assert g[1] == 20 and g[0] == 30
    se = summarize(g, [2], np.array([[9]]))
    assert np.isclose(se["se_cps"]**2, 2.5)
    assert np.isclose(se["se_meps"], 6)
    double = sum_cells([target, target])
    gg, qq = contrast(double, ref, [1], [0])
    assert np.allclose(gg, 2*gap) and np.allclose(qq, 2*q)
    # Same source unit: unequal person weights can change weighted national
    # dollars under pure attribution; fixed unit-head weights cannot.
    shared = np.array([[10.], [10.]])
    direct = np.array([[100.], [-80.]])
    person = np.repeat(np.array([[2.], [1.]]), 161, axis=1)
    head = np.repeat(np.array([[2.], [2.]]), 161, axis=1)
    mask = {"all": np.ones(2, bool)}
    bands = np.zeros(2, int)
    e = np.ones((2, 1))
    s = sufficient(shared, e, head, mask, bands, 1, person, person)["all"]
    p = sufficient(direct, e, head, mask, bands, 1, person, person)["all"]
    assert np.allclose(s["y"], 40) and np.allclose(p["y"], 40)
    assert np.allclose(s["n"], 3) and np.allclose(s["h"], 3)
    assert np.allclose(shared.T@person, 30) and np.allclose(direct.T@person, 120)
    try:
        sufficient(shared, e, person, mask, bands, 2)
    except ValueError as err:
        assert "band 1" in str(err)
    else:
        raise AssertionError("Missing band did not fail")
    print("PASS: hand gaps, ratio replication, common ages, donor covariance, fixed-budget attribution and missing-cell guard")


if __name__ == "__main__":
    main()
