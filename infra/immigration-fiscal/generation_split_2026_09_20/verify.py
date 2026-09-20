"""Boundary checks: absent ancestry is not native; step links are not biological."""
import numpy as np
import pandas as pd
from analyze_cps import COLS, classify, validate_weights


def family():
    d = pd.DataFrame(0, index=range(3), columns=COLS)
    d['PH_SEQ'], d['A_LINENO'] = 1, [1, 2, 3]
    d['A_AGE'], d['PRPERTYP'], d['PRCITSHP'] = [10, 35, 36], 2, 1
    d['PRDTHSP'] = 1
    d[['PENATVTY', 'PEMNTVTY', 'PEFNTVTY']] = 57
    d[['PEPAR1', 'PEPAR2', 'PEPAR1TYP', 'PEPAR2TYP']] = -1
    d.loc[0, ['PEPAR1', 'PEPAR2', 'PEPAR1TYP', 'PEPAR2TYP']] = [2, 3, 1, 1]
    return d


def category(d, strict=False):
    return [k for k, v in classify(d, strict).items() if v[0]]


d = family()
assert category(d) == ['G4plus_all_US_GP_observed']
d.loc[0, 'PEPAR2'] = -1
assert category(d) == ['G3plus_unresolved']
d.loc[1, 'PEMNTVTY'] = 303
assert category(d) == ['G3_Mexico_GP_observed']
d.loc[0, 'PEPAR1TYP'] = 2
assert category(d) == ['G3plus_unresolved']
d = family()
d.loc[1, 'PEMNTVTY'] = -2
assert category(d) == ['G3plus_unresolved']
d.loc[1, 'PEMNTVTY'] = 303
d.loc[1, 'PXMNTVTY'] = 41
assert category(d) == ['G3_Mexico_GP_observed']
assert category(d, strict=True) == ['G3plus_unresolved']
d.loc[2, 'PENATVTY'] = 303
assert category(d) == ['G3plus_unresolved']
d = family()
d.loc[0, 'PEPAR2'] = 2
try:
    classify(d)
except ValueError as error:
    assert 'Same parent' in str(error)
else:
    raise AssertionError('Duplicate parent slots accepted')
# Regression for initial guard: valid negative SDR weights must not be clipped.
w = np.array([[100., -20., 200.], [50., 100., 20.]])
validate_weights(w)
assert w[0, 1] == -20
for invalid in [np.array([[-1., 20.]]), np.array([[1., np.nan]])]:
    try:
        validate_weights(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid survey weights accepted')
print('PASS: missing ancestry, partial proof, step-parent, allocation, conflict, duplicate and SDR-weight boundaries')
