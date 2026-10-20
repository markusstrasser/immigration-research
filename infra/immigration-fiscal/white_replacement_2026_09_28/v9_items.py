"""Origin-neutral v9 rules on comparator-owned lines and source keys.

16/17 are Mexican-only and arrive in the canonical full-minus-observed overlay.
13/14/15 mutate spending,18 receipts,20 capital. Fees/Pell stay fixed. Item21
is explicit none here: the rough comparator already uses OFD+STL, without a
pooled ethnic translation. This is separate from the case's pooled-health rule.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import zipfile
import numpy as np

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0,str(FISCAL/'scripts'))
from memory_budget import require_within_budget


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


@lru_cache(maxsize=1)
def source():
    return {n: json.loads((FISCAL / f'spending_keys_r5_2026_10_15/derived/item{n}.json').read_text()) for n in (13,14,15)}


@lru_cache(maxsize=1)
def raw_roster(cps_zip):
    import pandas as pd
    with zipfile.ZipFile(cps_zip) as archive:
        return pd.read_csv(archive.open('pppub25.csv'),usecols=['PH_SEQ','PPPOS','A_AGE'])


def comparator_roster(R):
    d=raw_roster(R.ZIP)
    if not (np.array_equal(d.PH_SEQ,R.d.PH_SEQ) and np.array_equal(d.A_AGE,R.d.A_AGE)):
        raise SystemExit('[BLOCKED] source IDs and comparator person roster differ')
    return d


def calibrated_overlay_ages(W):
    """Signed native-minor calibration by actual person age, Mexican membership only."""
    import pandas as pd
    # The generation parquet sorts by SPM_ID/PPPOS; the comparator preserves the
    # original person CSV order. Join the source factors on actual person IDs.
    d = comparator_roster(W.R)
    keys = pd.MultiIndex.from_frame(d[['PH_SEQ','PPPOS']])
    frame = pd.read_parquet(FISCAL / 'count_composition_r5_2026_10_15/derived/native_person_factors.parquet',
                            columns=['PH_SEQ','PPPOS','central_member_factor'])
    factors = aligned_factors(d,frame)
    active = W.R.MASK['mex'].copy()
    records = W.META['union_completion']['observed_records']
    completion = [(r['PH_SEQ'],r['PPPOS']) for r in records if r['central_reporter'] or r['observed_nonreporter']]
    active |= keys.isin(completion)
    # Count16's producer prices float-precision source kernel weights, whereas
    # the rough frame reconstructs rounded survey weights. Carry its exact
    # person weights for this source-owned age/count addition.
    with np.load(FISCAL/'coverage_bound_2026_10_14/_cache/oct15_final_routing/set/pricing.npz') as kernel:
        source_keys=pd.MultiIndex.from_arrays([kernel['person_ph_seq'],kernel['person_pppos']])
        source_weights=kernel['weights'][:,0].copy()
        nonreporter=pd.MultiIndex.from_tuples([(r['PH_SEQ'],r['PPPOS']) for r in records if r['observed_nonreporter']])
        source_weights+=kernel['added_weights'][:,0]*source_keys.isin(nonreporter)
    if not source_keys.is_unique:
        raise SystemExit('[BLOCKED] native source kernel person IDs are not unique')
    source_weights=pd.Series(source_weights,index=source_keys).reindex(keys).to_numpy()
    required=active & (factors!=1)
    if not np.isfinite(source_weights[required]).all():
        raise SystemExit('[BLOCKED] native source kernel lacks comparator person ID')
    delta = np.zeros(len(d))
    delta[required] = source_weights[required]*(factors[required]-1)
    expected = W.META['population_v9']['without_coverage']-W.META['population_v8']['without_coverage']
    if abs(float(delta.sum())-expected)>1e-6:
        raise SystemExit(f'[BLOCKED] native age-vector count closure: {delta.sum()} versus {expected}')
    return np.bincount(np.minimum(d.A_AGE.to_numpy(int)//5,16),weights=delta,minlength=17)


def aligned_factors(roster,frame):
    import pandas as pd
    keys=pd.MultiIndex.from_frame(roster[['PH_SEQ','PPPOS']])
    source=frame.set_index(['PH_SEQ','PPPOS']).central_member_factor
    if not keys.is_unique or not source.index.is_unique:
        raise SystemExit('[BLOCKED] calibration person IDs are not unique')
    factors=source.reindex(keys).to_numpy()
    if not np.isfinite(factors).all():
        raise SystemExit('[BLOCKED] native calibration factor lacks comparator person ID')
    return factors


@lru_cache(maxsize=1)
def basket():
    path = HERE / '_cache/v9_basket.npz'
    receipt = json.loads((HERE / 'derived/v9_basket_inputs.json').read_text())
    if digest(path) != receipt['array_sha256']:
        raise SystemExit('[BLOCKED] comparator basket array changed; rebuild v9_basket.py')
    for name, expected in receipt['sha256'].items():
        if digest(FISCAL/name) != expected:
            raise SystemExit('[BLOCKED] comparator basket source changed: ' + name)
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def basket_indexer(roster,b):
    import pandas as pd
    source=pd.MultiIndex.from_arrays([b['ph_seq'],b['pppos']])
    target=pd.MultiIndex.from_frame(roster[['PH_SEQ','PPPOS']])
    if not source.is_unique or not target.is_unique:
        raise SystemExit('[BLOCKED] own basket person IDs are not unique')
    index=source.get_indexer(target)
    if (index<0).any() or not np.array_equal(b['age'][index],roster.A_AGE.to_numpy()):
        raise SystemExit('[BLOCKED] own basket lacks matching comparator person IDs/ages')
    return index


@lru_cache(maxsize=1)
def aligned_basket(cps_zip):
    b=basket()
    index=basket_indexer(raw_roster(cps_zip),b)
    return dict(b,**{k:b[k][index] for k in ('state','consumption','taxable')})


def basket_factor(W, sc):
    cached = sc.get('_v9_basket_cache')
    if cached is not None and cached[0] is W.R.w:
        return cached[1]
    comparator_roster(W.R)
    b = aligned_basket(W.R.ZIP)
    w, cw = W.R.w, sc['cps_w']
    state, raw, taxed = b['state'], b['consumption'], b['taxable']
    old = new = 0.
    for st, tax in zip(b['tax_states'], b['tax_shares']):
        m = state == st
        den_old, den_new = float(raw[m] @ w[m]), float(taxed[m] @ w[m])
        if den_old <= 0 or den_new <= 0:
            raise SystemExit('[BLOCKED] own basket state denominator is empty')
        old += tax * float(raw[m] @ cw[m]) / den_old
        new += tax * float(taxed[m] @ cw[m]) / den_new
    factor = new / old if old > 0 else 1.
    sc['_v9_basket_cache'] = (W.R.w, factor)
    return factor


def apply_lines(W, sc, amt, nat, response, ik):
    """Mutate own amounts and return typed additive cost changes; no case delta is scaled."""
    m = source()
    parts = []
    def change(item, line, delta, kind, before=None):
        key = 'spending|' + line
        prior = amt[key] if before is None else before
        amt[key] += delta
        parts.append(dict(item=str(item), source_line=line, kind=kind, population='observed_comparator',
                          before_bn=prior, after_bn=prior+delta, delta_bn=delta*response[key]))
    comp = m[13]
    change(13, comp['line'], amt['spending|'+comp['line']]*(comp['response']-1), 'compensation')
    for row in comp['extension']['lines']:
        line = row['line']
        fraction = 1. if row['fraction'] == 1 else comp['extension']['health_bridge']['central_national_bn']/nat['spending|'+line]
        amount = amt['spending|'+line]*fraction
        change(13, line, -amount, row.get('part', 'military_service'), before=amount)
    caseload = (W.R.d.SS_VAL.to_numpy(float)>0).astype(float)
    own_ss = float(sc['cps_w'] @ caseload)/float(W.R.w @ caseload)
    line = 'income_security_services'
    old_key = amt['spending|'+line]/nat['spending|'+line]
    retirement = m[14]['central']['retirement_consumption_bn']
    change(14, line, retirement*(own_ss-old_key), 'retirement_caseload_partial')
    use = ik['use'] if ik is not None else sc['share']['college']
    operating = m[15]['national_exposure_bn']*use
    change(15, 'education_services', operating*(m[15]['central_response']-1), 'college_operating', before=operating)
    key = 'receipts|general_sales_tax'
    prior = amt[key]
    factor = basket_factor(W, sc)
    amt[key] *= factor
    parts.append(dict(item='18', source_line='general_sales_tax', kind='household_joint', population='observed_comparator',
                      before_bn=prior, after_bn=amt[key], delta_bn=-(amt[key]-prior)*response[key], own_factor=factor))
    parts.append(dict(item='21', source_line='health_services', kind='none_already_OFD_STL_no_pooled_translation',
                      population='observed_comparator', before_bn=0.,after_bn=0.,delta_bn=0.))
    return parts


def capital(W, components, old_rate):
    """College15 then20; expose the15×20 term explicitly in20's delta."""
    rate = W.META['one_rate']['flat_real_equivalent']
    response = source()[15]['central_response']
    prior = sum(v for _, v in components)
    college = sum(v for cid,v in components if cid in ('college','college_user_fees'))
    d15 = college*(response-1)
    d20 = (prior+d15)*(rate/old_rate-1) if old_rate else 0.
    parts = [dict(item='15',source_line='college',kind='college_capital',population='observed_comparator',
                  before_bn=college,after_bn=college+d15,delta_bn=d15),
             dict(item='20',source_line='capital',kind='capital_rate_including_15x20',population='observed_comparator',
                  before_bn=prior+d15,after_bn=prior+d15+d20,delta_bn=d20)]
    return prior+d15+d20, parts
