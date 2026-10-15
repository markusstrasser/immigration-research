#!/usr/bin/env python3
"""State-law food/SNAP basket transport; the national tax take remains fixed.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/household.py
All upstream imports and source files are read-only. No upstream cache is built.
The public Interview survey cannot identify true food purchases after its redesign:
published Diary-integrated food means anchor the level; Interview groceries give
only the within-decile shape. This is a modelled transport, not measured lineage
consumption. See derived/household_meta.json for remaining limitations.
"""
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
import zipfile

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CONSUMPTION = FISCAL / 'consumption_key_2026_09_24'
sys.path.insert(0, str(CONSUMPTION))
import saving
import ce_tables
import remittance

FILES = ('241x', '242', '243', '244', '251')


def require(ok, message):
    if not ok:
        raise ValueError('[BLOCKED] household baskets: ' + message)


def taxable_basket(consumption, food, snap, exemption, arm):
    """SNAP purchases are a subset of food: the union removes them only once."""
    c = np.maximum(np.asarray(consumption, float), 0)
    f = np.clip(food, 0, c)
    s = np.clip(snap, 0, f)
    e = np.asarray(exemption, float)
    require(bool(np.all((e >= 0) & (e <= 1))), 'exemption outside [0,1]')
    removed = {'full': np.zeros_like(c), 'grocery': e*f,
               'snap': s, 'joint': e*f+(1-e)*s}[arm]
    return c-removed


def ce_food():
    """Read only needed FMLI columns; retain no person-level derived archive."""
    rows = []
    with zipfile.ZipFile(CONSUMPTION/'_cache/sources/intrvw24.zip') as z:
        for q in FILES:
            path = f'intrvw24/fmli{q}.csv'
            columns = pd.read_csv(z.open(path), nrows=0).columns
            base = ['NEWID','FINLWT21','FINCBTXM','TOTEXPPQ','TOTEXPCQ',
                    'PERINSPQ','PERINSCQ','CASHCOPQ','CASHCOCQ',
                    'FS_AMTXM','FS_MTHI','TFOODHOP','TFOODHOC']
            grocer = ['GROCERPQ','GROCERCQ'] if q != '241x' else ['FDHOMEPQ','FDHOMECQ']
            require(all(c in columns for c in base+grocer), 'missing CE columns '+q)
            d = pd.read_csv(z.open(path), usecols=base+grocer).fillna(0)
            # In 2024Q1 FDHOME is trip groceries + the BLS 80% allocation
            # of ordinary all-grocery purchases. Undo only that allocation.
            trip = 4*(d.TFOODHOP+d.TFOODHOC)
            grocery = 4*(d[grocer[0]]+d[grocer[1]])
            if q == '241x':
                grocery = trip + (grocery-trip)/0.8
            c = 4*(d.TOTEXPPQ+d.TOTEXPCQ-d.PERINSPQ-d.PERINSCQ-d.CASHCOPQ-d.CASHCOCQ)
            out = pd.DataFrame({'file':q,'weight':d.FINLWT21,'income':d.FINCBTXM,
                                'consumption':c,'groceries':grocery,'trip_food':trip,
                                'snap':d.FS_AMTXM*d.FS_MTHI})
            out = out[out.weight>0].copy()
            ix = out.sort_values('income',kind='mergesort').index
            out.loc[ix,'rank'] = (out.loc[ix,'weight'].cumsum()-out.loc[ix,'weight']/2)/out.weight.sum()
            rows.append(out)
    d = pd.concat(rows,ignore_index=True)
    table = ce_tables.parse(saving.DECILE_TABLE)
    concepts = ce_tables.concepts(table)
    pub_food = np.array(table['Food at home'][1:])
    pub_c = np.array(concepts['consumption'][1:])
    bins = saving.rank_bins(d['rank'],50)
    W = d.weight.to_numpy()
    C = np.bincount(bins,weights=W*d.consumption,minlength=50)
    G = np.bincount(bins,weights=W*d.groceries,minlength=50)
    S = np.bincount(bins,weights=W*d.snap,minlength=50)
    F = np.empty(50)
    dec = np.arange(50)//5
    controls = []
    for k in range(10):
        m = dec==k
        target = pub_food[k]/pub_c[k]
        # Calibrate aggregate food/consumption ratio to published CE decile.
        F[m] = G[m]/C[m]*target/(G[m].sum()/C[m].sum())
        controls.append({'decile':k+1,'food_share':target,
                         'calibrated_food_share':float(np.sum(F[m]*C[m])/C[m].sum()),
                         'ce_snap_share':float(S[m].sum()/C[m].sum()),
                         'groceries_share':float(G[m].sum()/C[m].sum())})
    # Same bottom-decile pooling rule as the adopted saving transport.
    F[:5] = pub_food[0]/pub_c[0]
    snap_share = S/C
    snap_share[:5] = S[:5].sum()/C[:5].sum()
    require(bool(np.isfinite(F).all() and np.all((F>=0)&(F<1))), 'food share support')
    return F, np.clip(snap_share,0,F), pd.DataFrame(controls), d


def load_frame():
    cache = CONSUMPTION/'_cache/cps_arrays.npz'
    require(cache.exists(),'upstream CPS cache absent; no implicit rebuild')
    with np.load(cache,allow_pickle=False) as z:
        a = {k:z[k] for k in z.files if k!='weights'}
        a['weights'] = z['weights'][:,0].copy()
    require(a['weights'].ndim==1,'only full CPS weight required')
    return a


def original_consumption(a):
    """Exact adopted saving curve and original central corridor calibration."""
    pumd = saving.pumd_ranked()
    curve = saving.ce_curve('consumption',50,pumd,saving.published_deciles(),within=True)
    factor = saving.unit_factor(a,curve,'ratio')
    un = remittance.units(a)
    per = remittance.per_theta(a,un,remittance.sender_rates(),0.5)
    v = np.where(un['any_target'],per,0)[a['unit']]/a['size']
    theta = (remittance.BANXICO_US-remittance.H2_ALLOWANCE['central'])*1e9/(v@a['weights'])
    check = pd.read_csv(CONSUMPTION/'derived/remittance_flows.csv')
    expected = float(check.loc[check.spec.eq('corridor_net_h2'),'theta_share_of_earnings'].iloc[0])
    require(abs(theta-expected)<1e-12,'original remittance theta does not reproduce')
    unit_c = factor*np.maximum(un['resources']-theta*per,0)
    return unit_c[a['unit']]/a['size'],theta


def row4_weights(a):
    r = json.loads((FISCAL/'main_case_candidate_2026_09_28/derived/production_row4.json').read_text())
    w = a['weights'].copy()
    for label,code in [('naturalized',4),('noncitizen',5)]:
        m = (a['penatvty']==303)&(a['citizen']==code)&~np.isin(a['state_fips'],[6,48])
        ref = r['row4_factors'][label]
        require(int(m.sum())==ref['records'],'row4 record gate '+label)
        require(abs(w[m].sum()-ref['cps_population'])<1e-3,'row4 published-weight gate '+label)
        w[m] *= ref['factor']
    require(abs(w[a['target']].sum()-r['populations']['row4'])<1e-3,'row4 39.712493M population gate')
    return w,r['populations']['row4']


def groups(a):
    # Read race only, matching IDs rather than assuming source ordering.
    archive = FISCAL/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    with zipfile.ZipFile(archive) as z:
        d = pd.read_csv(z.open('pppub25.csv'),usecols=['PH_SEQ','PPPOS','PRDTRACE'])
    idx = pd.MultiIndex.from_arrays([a['ph_seq'],a['pppos']])
    race = d.set_index(['PH_SEQ','PPPOS']).PRDTRACE.reindex(idx).to_numpy()
    require(bool(np.isfinite(race).all()),'race join support')
    payload = json.loads((FISCAL/'main_case_2026_10_15/derived/corrections.json').read_text())
    added = payload['meta']['union_completion']['observed_records']
    completed = idx.isin([(v['PH_SEQ'],v['PPPOS']) for v in added])
    require(int(completed.sum())==len(added),'completion person ID gate')
    return {'union':a['target'], 'union_completed':a['target']|completed,
            'g3plus':a['third_plus'],
            'white':a['civilian']&(race==1)&~a['hispanic']}


def build(out_dir=None):
    started=time.perf_counter()
    out = HERE/'derived' if out_dir is None else Path(out_dir)
    out.mkdir(parents=True,exist_ok=True)
    fshare,sshare,controls,ce = ce_food()
    controls.to_csv(out/'household_ce_deciles.csv',index=False,lineterminator='\n')
    a = load_frame()
    c,theta = original_consumption(a)
    w,population = row4_weights(a)
    group = groups(a)
    bins = saving.rank_bins(saving.cps_units(a)['rank'],50)[a['unit']]
    food = c*fshare[bins]
    snap = np.minimum(np.maximum(a['snap'],0)/a['size'],food)
    ce_snap = c*sshare[bins]
    rules = pd.read_csv(HERE/'inputs/grocery_state_2024.csv')
    require(set(rules.state_fips)==set(np.unique(a['state_fips'])),'all CPS state laws present')
    exemption = pd.Series(rules.exempt_fraction.to_numpy(),index=rules.state_fips).reindex(a['state_fips']).to_numpy()
    rows=[]
    for snap_source,sp in [('cps_reported',snap),('ce_rank',ce_snap)]:
        for arm in ['full','grocery','snap','joint']:
            taxable = taxable_basket(c,food,sp,exemption,arm)
            nat=float(taxable[a['civilian']]@w[a['civilian']])
            raw_nat=float(c[a['civilian']]@w[a['civilian']])
            for st in [0]+sorted(set(a['state_fips'])):
                state=np.ones(len(c),bool) if st==0 else a['state_fips']==st
                civ=state&a['civilian']
                state_key=float(taxable[civ]@w[civ]); raw_state=float(c[civ]@w[civ])
                for name,mask in group.items():
                    m=state&mask&a['civilian']
                    g=float(taxable[m]@w[m]); raw=float(c[m]@w[m])
                    # Empty state/group cells have no price contribution. A factor
                    # of one preserves that zero without manufacturing a member.
                    relative=g/raw if raw>0 else 1.
                    rows.append({'snap_source':snap_source,'arm':arm,'state_fips':int(st),'group':name,
                                 'group_key':g,'group_raw_key':raw,'national_key':nat,'national_raw_key':raw_nat,
                                 'state_key':state_key,'state_raw_key':raw_state,
                                 'group_share_national':g/nat,'group_share_state':g/state_key,
                                 'factor_national':relative/(nat/raw_nat),
                                 'factor_state':relative/(state_key/raw_state)})
    pd.DataFrame(rows).to_csv(out/'household_state_factors.csv',index=False,lineterminator='\n')
    meta={'status':'state-law taxable-basket proxy; proposed, not adopted',
          'row4_population':population,'remittance_theta':theta,
          'consumption':'adopted both_corridor_net_h2 per-person key; original saving ranks and calibration, then row4 weights',
          'food':'BLS published 2024 decile Food at home / consumption; Interview grocery shape rescaled within decile; bottom decile pooled',
          'snap':'central CPS annual SPM_SNAPSUB / actual SPM unit size capped at imputed food; CE annual FS_AMTXM * FS_MTHI rank-share sensitivity',
          'overlap':'joint removes exempt_fraction*food + (1-exempt_fraction)*SNAP; never add isolated SNAP and food effects',
          'normalization':'factor_state=(group taxable/group raw)/(state taxable/state raw); factor_national uses civilian national denominator. Keep each tax collection pool fixed.',
          'white_definition':'CPS PRDTRACE==1 and not Hispanic, all civilian ages; not an ancestry-specific proxy',
          'completion':'union_completed includes exact v8 observed IDs; original union retained for the row4 gate',
          'limits':['State statutory food/general rate ratio only; local grocery levies not imputed without county data. Use as state-law arm, not exact combined state/local tax.',
                    'Food-category candy, soda, hot/prepared-food exceptions cannot be identified here; all food at home treated as qualifying groceries.',
                    'Consumer units are not SPM units; rank transport assumes equal food shares within income rank across origin, nativity, age and state.',
                    'CPS SNAP underreporting and benefit-redemption timing are not corrected; cap binds when reported benefit exceeds imputed food.',
                    'Latent descendants and PES-missed persons cannot be identified. g3plus/white are proxy factors for explicit caller choices; no full-lineage claim.',
                    'Item11 mixed-household fiscal response and item12 coverage-price response require parent integration; do not silently hold them fixed in an adopted item.'],
          'ce_rows':len(ce),'ce_dictionary_checks':{'TFOODHOP':'trip groceries only','FS_AMTXM':'last SNAP receipt amount, imputation mean','FS_MTHI':'months received in past 12'},
          'snap_cap_weighted_bn':float((np.maximum(a['snap'],0)/a['size']-snap)[a['civilian']]@w[a['civilian']]/1e9)}
    source_paths = [CONSUMPTION/'_cache/sources/intrvw24.zip',
                    CONSUMPTION/'_cache/sources/ce-pumd-interview-diary-dictionary.xlsx',
                    CONSUMPTION/'_cache/sources'/saving.DECILE_TABLE,
                    CONSUMPTION/'_cache/cps_arrays.npz',
                    CONSUMPTION/'derived/sender_rates_pooled.csv',
                    FISCAL/'main_case_candidate_2026_09_28/derived/production_row4.json',
                    FISCAL/'main_case_2026_10_15/derived/corrections.json',
                    HERE/'inputs/grocery_state_2024.csv']
    meta['source_sha256']={str(p.relative_to(FISCAL)):hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
                           for p in source_paths}
    (out/'household_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    elapsed=time.perf_counter()-started
    print(json.dumps({'seconds':elapsed,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'row4_population':population,'rows':len(rows),'output':str(out)},indent=2))
    return pd.DataFrame(rows),meta


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out-dir',type=Path)
    build(ap.parse_args().out_dir)
