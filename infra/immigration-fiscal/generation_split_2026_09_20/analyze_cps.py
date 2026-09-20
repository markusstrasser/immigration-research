"""Partial G3/G4+ separation in the existing CPS civilian Mexican-origin stock.

Grandparents are observed only through linked biological co-resident parents.
Missing links stay unresolved. No population imputation or fiscal reallocation.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = _data_paths.data_root(require_exists=False) / 'external/stage3/census/cps_asec_2025/asecpub25csv.zip'
SHA = '318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b'
US = [57, 60, 66, 69, 73, 78]
WEIGHTS = [f'pwwgt{i}' for i in range(161)]
COLS = ['PH_SEQ', 'PPPOS', 'A_LINENO', 'A_AGE', 'PRPERTYP', 'PRCITSHP',
        'PRDTHSP', 'PENATVTY', 'PEMNTVTY', 'PEFNTVTY', 'MARSUPWT',
        'PEPAR1', 'PEPAR2', 'PEPAR1TYP', 'PEPAR2TYP', 'PXHSPNON',
        'PXNATVTY', 'PXMNTVTY', 'PXFNTVTY', 'PXPAR1', 'PXPAR2',
        'PXPAR1TYP', 'PXPAR2TYP']


def population_masks(d):
    """Match extend_ledger.py group definitions and receipt civilian scope."""
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    g1 = d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(303).to_numpy()
    g2 = native & (d.PEMNTVTY.eq(303) | d.PEFNTVTY.eq(303)).to_numpy()
    g3plus = native & (d.PEMNTVTY.isin(US) & d.PEFNTVTY.isin(US)
                       & d.PRDTHSP.eq(1)).to_numpy()
    return {k: v & civilian for k, v in [('G1', g1), ('G2', g2), ('G3plus', g3plus)]}


def classify(d, unallocated_only=False):
    n = len(d)
    keys = pd.MultiIndex.from_frame(d[['PH_SEQ', 'A_LINENO']])
    if not keys.is_unique:
        raise ValueError('Duplicate person linkage key')
    lookup = pd.Series(np.arange(n), index=keys)
    gp = np.full((n, 4), np.nan)
    consistent = np.ones(n, bool)
    for slot in (1, 2):
        line = d[f'PEPAR{slot}'].to_numpy()
        query = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), line])
        parent = lookup.reindex(query).fillna(-1).to_numpy(dtype=int)
        linked = (line > 0) & (parent >= 0)
        if np.any((line > 0) & ~linked) or np.any(linked & (parent == np.arange(n))):
            raise ValueError('Broken or self parent link')
        bio = linked & d[f'PEPAR{slot}TYP'].eq(1).to_numpy()
        p = np.maximum(parent, 0)
        pb = d.PENATVTY.to_numpy()[p]
        # A linked biological parent's record must agree with native parentage.
        consistent &= ~bio | np.isin(pb, US)
        usable = bio & np.isin(pb, US)
        if unallocated_only:
            usable &= (d.PXNATVTY.to_numpy()[p] == 0)
            usable &= d[f'PXPAR{slot}'].isin([-1, 0]).to_numpy()
            usable &= d[f'PXPAR{slot}TYP'].isin([-1, 0]).to_numpy()
        for j, (field, flag) in enumerate([('PEMNTVTY', 'PXMNTVTY'),
                                          ('PEFNTVTY', 'PXFNTVTY')]):
            keep = usable.copy()
            if unallocated_only:
                keep &= d[flag].to_numpy()[p] == 0
            gp[keep, 2*(slot-1)+j] = d[field].to_numpy()[p[keep]]
    duplicate = (d.PEPAR1.gt(0) & d.PEPAR1.eq(d.PEPAR2)).to_numpy()
    if duplicate.any():
        raise ValueError('Same parent appears in both slots')
    if unallocated_only:
        consistent &= d[['PXNATVTY', 'PXMNTVTY', 'PXFNTVTY', 'PXHSPNON']].eq(0).all(axis=1).to_numpy()
    base = population_masks(d)['G3plus']
    g3 = base & consistent & (gp == 303).any(axis=1)
    g4 = base & consistent & np.isin(gp, US).all(axis=1)
    result = {'G3_Mexico_GP_observed': g3, 'G4plus_all_US_GP_observed': g4,
              'G3plus_unresolved': base & ~(g3 | g4)}
    if np.any(g3 & g4) or not np.array_equal(sum(result.values()), base.astype(int)):
        raise ValueError('Later-generation partition does not close')
    return result


def summarize(masks, d, weights, arm):
    target = np.logical_or.reduce(list(population_masks(d).values()))
    rows = []
    for age, ages in [('all', np.ones(len(d), bool)),
                      ('under18', d.A_AGE.lt(18).to_numpy()),
                      ('18plus', d.A_AGE.ge(18).to_numpy())]:
        total = weights[target & ages].sum(axis=0)
        if np.any(total <= 0):
            raise ValueError('Nonpositive replicate population denominator')
        for name, mask in masks.items():
            use = mask & ages
            v = weights[use].sum(axis=0)
            pct = 100*v/total
            rows.append(dict(arm=arm, age=age, generation=name, n=int(use.sum()),
                             people=v[0], se_people=np.sqrt(4/160*np.square(v[1:]-v[0]).sum()),
                             pct_of_target=pct[0], se_pct=np.sqrt(4/160*np.square(pct[1:]-pct[0]).sum())))
    return rows


def validate_weights(weights):
    # Source: CPS2025 technical documentation, PDF p.376. Negative replicate
    # weights from family equalization must be retained for the SDR variance.
    if not np.isfinite(weights).all() or (weights[:, 0] < 0).any():
        raise ValueError('Invalid weights')


def main():
    if hashlib.sha256(RAW.read_bytes()).hexdigest() != SHA:
        raise ValueError('CPS source hash changed')
    with zipfile.ZipFile(RAW) as z:
        with z.open('pppub25.csv') as f:
            d = pd.read_csv(f, usecols=COLS)
        with z.open('asec_csv_repwgt_2025.csv') as f:
            w = pd.read_csv(f, usecols=['h_seq', 'PPPOS']+WEIGHTS).rename(columns={'h_seq': 'PH_SEQ'})
    original_n = len(d)
    d = d.merge(w, on=['PH_SEQ', 'PPPOS'], validate='one_to_one')
    if len(d) != original_n:
        raise ValueError('Person-weight merge lost rows')
    np.testing.assert_allclose(d.MARSUPWT/100, d.pwwgt0, rtol=0, atol=.011)
    weights = d[WEIGHTS].to_numpy(float)
    validate_weights(weights)
    base = population_masks(d)
    target = np.logical_or.reduce(list(base.values()))
    if np.any(sum(base.values()) > 1):
        raise ValueError('Overlapping canonical groups')
    expected_path = HERE.parent/'full_account_receipts_2026_09_20/derived/allocation_keys.csv'
    expected = pd.read_csv(expected_path).query('allocation == "personal" and allocation_key == "population"')
    if len(expected) != 1:
        raise ValueError('Missing current account population anchor')
    np.testing.assert_allclose(weights[target, 0].sum(), expected.target_key_total.iloc[0], rtol=0, atol=.1)
    rows = summarize(base, d, weights, 'canonical')
    reported = classify(d)
    for arm, strict in [('reported_linkage', False), ('unallocated_linkage', True)]:
        part = classify(d, strict) if strict else reported
        rows += summarize(part, d, weights, arm)
        for k in ['G3_Mexico_GP_observed', 'G4plus_all_US_GP_observed']:
            if strict and np.any(part[k] & ~reported[k]):
                raise ValueError('Unallocated classification expanded observed class')
    out = HERE/'derived'
    out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'cps_generation_split.csv', index=False)
    audit = dict(source=str(RAW), sha256=SHA, source_rows=original_n,
                 target_people=float(weights[target, 0].sum()),
                 negative_replicate_weights_preserved=int((weights[:, 1:] < 0).sum()),
                 source_url='https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip',
                 definition='CPS2025 civilian household Mexican-origin union, all ages; reported nativity; US areas native',
                 checks=['source hash', 'one-to-one weight join', 'weight scale', 'valid unique parent links',
                         'disjoint generation partition', 'canonical target total', 'unallocated subset'],
                 limitation='Co-residence selection and missing ancestry are not included in sampling SE; G4+ is not exact G4.')
    (out/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(pd.DataFrame(rows).query('age == "all"').to_string(index=False))


if __name__ == '__main__':
    main()
