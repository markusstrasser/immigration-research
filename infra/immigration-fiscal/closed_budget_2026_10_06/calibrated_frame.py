"""Source-owned oct16 weights, with completion and unlocated coverage distinct.

No identities are created by the ACS rake. Coverage household placement is a
separate proportional-within-generation assumption and can be disabled.
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd

FISCAL = Path(__file__).resolve().parent.parent
FACTOR_FILE = FISCAL / 'count_composition_r5_2026_10_15/derived/native_person_factors.parquet'


def calibration_factors(d):
    f = pd.read_parquet(FACTOR_FILE, columns=['PH_SEQ', 'PPPOS', 'central_member_factor'])
    if f.duplicated(['PH_SEQ', 'PPPOS']).any() or d.duplicated(['PH_SEQ', 'PPPOS']).any():
        raise ValueError('[BLOCKED] nonunique calibration person keys')
    source = f.set_index(['PH_SEQ', 'PPPOS']).central_member_factor
    values = source.reindex(pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']]))
    # Source publishes the complete CPS universe, with explicit1 outside its
    # eligible native-minor cells. Missing source keys never imply factor1.
    missing = source.index.difference(pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']]))
    if len(missing):
        raise ValueError('[BLOCKED] calibration source persons missing from CPS')
    if values.isna().any():
        raise ValueError('[BLOCKED] CPS persons missing explicit calibration factors')
    out = values.to_numpy(float)
    if not np.isfinite(out).all() or np.any(out < 0):
        raise ValueError('[BLOCKED] invalid central_member_factor')
    return out


def complete_calibrated(d, weights, target, payload, gate, *, coverage=False):
    meta = payload['meta']
    weights, target = weights.copy(), target.copy()
    index = pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']])
    gate('calibrated_frame_unique_person_ids', index.is_unique)
    completion = np.zeros(len(d), bool)
    for row in meta['union_completion']['observed_records']:
        pos = index.get_loc((row['PH_SEQ'], row['PPPOS']))
        gate('completion_own_record_outside_original', not target[pos] and bool(d.civ.iloc[pos]))
        completion[pos], target[pos], weights[pos] = True, True, row['people']
    factor = calibration_factors(d)
    # Latent descendants are held fixed; the observed member's portion alone
    # receives its own origin-stratum calibration.
    ordinary = d.pw_row4.to_numpy(float)
    observed = np.where(target, ordinary, 0.)
    weights[target] += observed[target]*(factor[target]-1.)
    counts = meta['population_v9']
    gate('calibrated_located_people_close_to_payload',
         abs(float(weights[target].sum())-counts['without_coverage']) < 1e-2,
         people=float(weights[target].sum()), expected=counts['without_coverage'])
    located = weights.copy()
    usb = d.PRCITSHP.isin([1,2,3]).to_numpy()
    par = (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy()
    groups = {'G1':target & ~usb, 'G2':target & usb & par, 'G3plus':target & usb & ~par}
    missing = meta['coverage'].get('counts_by_generation_folded')
    if missing is None:
        source = meta['coverage']['counts_by_generation']
        missing = {g:source[g]+(source.get('added',0) if g=='G3plus' else 0) for g in groups}
    else:
        missing = dict(missing)
    for item in ('native_minor_calibration','coverage_tenure'):
        for g,delta in meta.get(item,{}).get('coverage_people_change_by_generation',{}).items():
            missing[g] += delta
    # The final missing count is the inherited construction plus16/17 once.
    # Do not additionally use the historical population_v8 count.
    gate('coverage_counts_close_complete_denominator',
         abs(sum(missing.values())-(counts['with_coverage']-counts['without_coverage'])) < 1e-5)
    if coverage:
        for g, mask in groups.items():
            if missing[g] == 0:
                continue
            gate(f'coverage_{g}_has_placement', weights[mask].sum()>0)
            weights[mask] *= 1+missing[g]/weights[mask].sum()
        gate('constructed_complete_count_matches_payload',
             abs(float(weights[target].sum())-counts['with_coverage']) < 1e-2)
    return weights,target,{'located_people':float(located[target].sum()),
        'coverage_people':missing,'coverage_in_weights':coverage,
        'complete_people':counts['with_coverage'],
        'calibration':'own central_member_factor on observed member weight; latent addition held fixed',
        'coverage_rule':'[ASSUMPTION] proportional within generation; unlocated people, no new identified applicants' if coverage else '[UNLOCATED] coverage excluded from eligible CPS cells'}
