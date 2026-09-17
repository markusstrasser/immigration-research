"""Independent scalar/covariance probe retained from numerical review."""
import numpy as np
import estimator as m

rng = np.random.default_rng(607)
n, k, j, b = 90, 8, 4, 10
values = rng.normal(100, 20, (n, k))
exposures = np.eye(j)[np.arange(n) % j]
population_weights = rng.uniform(1, 4, (n, 161))
dollar_weights = rng.uniform(1, 4, (n, 161))
bands = np.arange(n) % b
masks = {'a': np.arange(n) < 30, 'b': (np.arange(n) >= 30) & (np.arange(n) < 60), 'ref': np.ones(n, bool)}
coefficients = np.array([1, -1, -1, 1, 1, 1, -1, 1])
means = np.array([4., 10., 5., 14.])
stats = m.sufficient(values, exposures, dollar_weights, masks, bands, b, population_weights, population_weights)
for label, mask in masks.items():
    for band in range(b):
        use = mask & (bands == band)
        for r in range(161):
            assert np.isclose(stats[label]['n'][band, r], sum(population_weights[i, r] for i in np.flatnonzero(use)))
            for component in range(k):
                assert np.isclose(stats[label]['y'][band, component, r], sum(values[i, component] * dollar_weights[i, r] for i in np.flatnonzero(use)))
            for cell in range(j):
                assert np.isclose(stats[label]['h'][band, cell, r], sum(exposures[i, cell] * population_weights[i, r] for i in np.flatnonzero(use)))

shares = np.arange(1, b+1, dtype=float)
shares /= shares.sum()
for label in ['a', 'b']:
    target, ref = stats[label], stats['ref']
    for matched in [True, False]:
        gap, gradient = m.contrast(target, ref, coefficients, means, matched)
        for r in range(161):
            target_totals = [sum(target['y'][band, c, r] * coefficients[c] for c in range(k)) - sum(target['h'][band, c, r] * means[c] for c in range(j)) for band in range(b)]
            ref_totals = [sum(ref['y'][band, c, r] * coefficients[c] for c in range(k)) - sum(ref['h'][band, c, r] * means[c] for c in range(j)) for band in range(b)]
            if matched:
                manual = sum(target_totals[band] - target['n'][band, r] / ref['n'][band, r] * ref_totals[band] for band in range(b))
            else:
                manual = sum(target_totals) - target['n'][:, r].sum() / ref['n'][:, r].sum() * sum(ref_totals)
            assert np.isclose(gap[r], manual)
        for cell in range(j):
            moved = means.copy()
            moved[cell] += .001
            changed, _ = m.contrast(target, ref, coefficients, moved, matched)
            assert np.isclose((changed[0]-gap[0])/.001, gradient[cell], rtol=1e-7, atol=1e-7)
    standardized, gradient = m.standardized_gap(target, ref, coefficients, means, shares)
    manual = sum(shares[band] * (m.account(target, coefficients, means)[band] / target['n'][band] - m.account(ref, coefficients, means)[band] / ref['n'][band]) for band in range(b))
    assert np.allclose(standardized, manual)
    for cell in range(j):
        moved = means.copy()
        moved[cell] += .001
        changed, _ = m.standardized_gap(target, ref, coefficients, moved, shares)
        assert np.isclose((changed[0]-standardized[0])/.001, gradient[cell], rtol=1e-7, atol=1e-7)

union = m.sum_cells([stats['a'], stats['b']])
g, q = m.contrast(union, stats['ref'], coefficients, means)
ga, qa = m.contrast(stats['a'], stats['ref'], coefficients, means)
gb, qb = m.contrast(stats['b'], stats['ref'], coefficients, means)
assert np.allclose(g, ga+gb)
assert np.allclose(q, qa+qb)
factor = rng.normal(size=(j, j))
cov = factor @ factor.T
result = m.summarize(g, q, cov)
hand_cps_variance = .025 * sum((g[r]-g[0])**2 for r in range(1, 161))
hand_donor_variance = sum(q[a]*cov[a, bb]*q[bb] for a in range(j) for bb in range(j))
assert np.isclose(result['se_joint']**2, hand_cps_variance+hand_donor_variance)
# Disable medical explicitly: means and donor covariance zero.
g0, q0 = m.contrast(union, stats['ref'], coefficients, means*0)
nohealth = m.summarize(g0, q0, cov*0)
assert nohealth['se_meps'] == 0
assert nohealth['se_joint'] == nohealth['se_cps']
# Identical health/population under alternative dollars cancels donor gradients.
altered = {key: value.copy() for key, value in stats['a'].items()}
altered['y'] += rng.normal(size=altered['y'].shape)
paired, qp = m.contrast(altered, stats['ref'], coefficients, means)
assert np.array_equal(qp, qa)
assert m.summarize(paired-ga, qp-qa, cov)['se_meps'] == 0
sa, qa = m.standardized_gap(stats['a'], stats['ref'], coefficients, means, shares)
sb, qb = m.standardized_gap(stats['b'], stats['ref'], coefficients, means, shares)
direct, qdirect = m.standardized_gap(stats['a'], stats['b'], coefficients, means, shares)
assert np.allclose(sa-sb, direct) and np.allclose(qa-qb, qdirect)
print('PASS: scalar 10-band/8-component/4-donor arithmetic; 161 replicate contrasts; numerical gradients; joint and aggregate covariance; fixed-population donor cancellation; no-health arm')
