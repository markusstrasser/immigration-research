"""Independent balanced-panel demeaning/cluster-score check of the main export."""
from pathlib import Path
import csv
import math

import numpy as np

HERE = Path(__file__).resolve().parent
with (HERE/'derived/panel.csv').open() as stream:
    rows = [r for r in csv.DictReader(stream) if int(r['level']) == 1]
with (HERE/'derived/estimates.csv').open() as stream:
    targets = [r for r in csv.DictReader(stream) if r['spec'] == 'full']
years = sorted({int(r['year']) for r in rows})
states = sorted({int(r['state']) for r in rows})
lookup = {(int(r['state']), int(r['year'])): r for r in rows}
assert len(rows) == len(lookup) == len(states)*len(years) == 350
x = np.array([[math.log(float(lookup[s,t]['population'])) for t in years] for s in states])
y = np.array([[math.log(float(lookup[s,t]['admin'])) for t in years] for s in states])
population = np.array([float(lookup[s,years[0]]['base_population']) for s in states])
assert len(targets) == 2
for weighted in (False, True):
    weights = population/population.mean() if weighted else np.ones(len(states))

    def demean(a):
        return (a - a.mean(axis=1)[:,None]
                - np.average(a, axis=0, weights=weights)[None,:]
                + np.average(a.mean(axis=1), weights=weights))

    xd, yd = demean(x), demean(y)
    denominator = np.sum(weights[:,None]*xd*xd)
    beta = np.sum(weights[:,None]*xd*yd)/denominator
    errors = yd-beta*xd
    scores = np.sum(weights[:,None]*xd*errors, axis=1)
    n, g, k = y.size, len(states), len(states)+len(years)
    se = math.sqrt(g/(g-1)*(n-1)/(n-k)*np.sum(scores*scores)/denominator**2)
    target = next(r for r in targets if r['weighted'] == str(weighted))
    np.testing.assert_allclose([beta, se], [float(target['beta']), float(target['se_CR1'])], atol=1e-10, rtol=0)
    print(f'PASS independent main calculation: weighted={weighted}, beta={beta:.10f}, SE={se:.10f}')

# Confirm the input-vintage guard fails before accepting an altered fingerprint.
import analyze
source = next(iter(analyze.EXPECTED_HASHES))
analyze.EXPECTED_HASHES[source] = 'invalid-fingerprint-for-guard-check'
try:
    analyze.record(analyze.BASE/source)
except ValueError as exc:
    assert 'Unreviewed input vintage' in str(exc)
else:
    raise AssertionError('Changed input fingerprint was accepted')
print('PASS input-vintage rejection')
