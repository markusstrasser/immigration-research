"""Unit tests for the generation masks and the two conventions (run with pytest from the repository root)."""
import numpy as np
import pandas as pd

import frame as F

SPLIT = F.FISCAL / "generation_split_2026_09_20/derived/cps_generation_split.csv"


def _setup():
    d = F.load()
    civ, union, gens = F.masks(d)
    return d, civ, union, gens


def test_counts_match_generation_split():
    d, civ, union, gens = _setup()
    published = pd.read_csv(SPLIT).query("arm == 'canonical'")
    w = d.pwwgt0.to_numpy(float)
    ages = {"all": np.ones(len(d), bool), "under18": d.A_AGE.lt(18).to_numpy(), "18plus": d.A_AGE.ge(18).to_numpy()}
    for r in published.itertuples():
        m = gens[r.generation] & ages[r.age]
        assert int(m.sum()) == r.n, (r.generation, r.age)
        assert abs(w[m].sum() - r.people) < 1e-6, (r.generation, r.age)


def test_union_is_canonical_target():
    d, civ, union, gens = _setup()
    assert abs(d.pwwgt0.to_numpy(float)[union].sum() - F.TARGET_POP) < .01
    assert not (gens["G1"] & gens["G2"]).any() and not (gens["G2"] & gens["G3plus"]).any()


def test_conventions_partition_the_union():
    d, civ, union, gens = _setup()
    omega, rule, _ = F.assignments(d, civ, union, gens)
    w = d.pwwgt0.to_numpy(float)
    for name in ("a", "b"):
        assert np.allclose(omega[name][union].sum(axis=1), 1)
        assert abs((w[:, None] * omega[name]).sum() - F.TARGET_POP) < .01
    adults = union & d.A_AGE.ge(18).to_numpy()
    assert np.array_equal(omega["a"][adults], omega["b"][adults])  # (b) moves minors only
