"""Validate recorded household splits, independently of the reconnaissance code."""
from collections import Counter
import json
from pathlib import Path

import numpy as np
import pandas as pd

from extract import CACHE, DERIVED, sha


def load_data():
    receipt = json.loads((CACHE / 'extract_receipt.json').read_text())
    assert sha(CACHE / 'persons.parquet') == receipt['parquet_sha256'], '[BLOCKED] stale extract'
    assert sha(Path(__file__).with_name('extract.py')) == receipt['script_sha256'], '[BLOCKED] rerun extract'
    return pd.read_parquet(CACHE / 'persons.parquet')


def relation(row, person):
    for i in range(1, 31):
        name = f'RREL_PNUM{i}'
        if name in row and pd.notna(row[name]) and int(row[name]) == int(person):
            assert f'RREL{i}' in row, '[BLOCKED] relationship ID lacks its relation column'
            return row[f'RREL{i}']
    return np.nan


def valid(row):
    return (row is not None and row.RIN_UNIV == 1 and pd.notna(row.ERESIDENCEID)
            and row.ERH_BMONTH <= row.MONTHCODE <= row.ERH_EMONTH)


def reported(row):
    return valid(row) and all(row[c] == 1 for c in ['ARESIDENCEID', 'ARH_BMONTH', 'ARH_EMONTH'])


def type2(row):
    if row is None:
        return {}
    return {str(int(row[f'ET2_LNO{i}'])).zfill(3): row[f'TT2_AGE{i}']
            for i in range(1, 11) if pd.notna(row[f'ET2_LNO{i}'])}


def build_events(d):
    records = {k:i for i,k in enumerate(zip(d.SSUID,d.PNUM,d.MONTHCODE))}
    # Retrieve full rows only for candidate checks, not every adult-month.
    def get(s, p, m):
        x = records.get((s, p, m))
        return d.iloc[x] if x is not None else None
    adults = d[d.TAGE_EHC.ge(18) & d.ERESIDENCEID.notna()][['SSUID', 'PNUM', 'MONTHCODE', 'ERESIDENCEID']]
    pair = adults.merge(adults, on=['SSUID', 'MONTHCODE', 'ERESIDENCEID'], suffixes=('_f', '_o'))
    pair = pair[pair.PNUM_f.ne(pair.PNUM_o)].copy()
    pair['t'] = pair.MONTHCODE+1
    nxt = adults.rename(columns={'MONTHCODE': 't', 'ERESIDENCEID': 'next'})
    pair = pair.merge(nxt.rename(columns={'PNUM': 'PNUM_f', 'next': 'home_f'}), on=['SSUID', 'PNUM_f', 't'])
    pair = pair.merge(nxt.rename(columns={'PNUM': 'PNUM_o', 'next': 'home_o'}), on=['SSUID', 'PNUM_o', 't'])
    pair = pair[pair.home_f.eq(pair.ERESIDENCEID) & pair.home_o.ne(pair.ERESIDENCEID)]
    candidates = [('tracked', r.SSUID, r.PNUM_f, r.PNUM_o, int(r.t)) for r in pair.itertuples()]
    # Identity-set differences, not raw slot indices; age is assessed before departure.
    t2cols = [f'{p}{i}' for p in ['ET2_LNO','TT2_AGE'] for i in range(1,11)]
    prev = d.groupby(['SSUID','PNUM'])[t2cols+['MONTHCODE','ERESIDENCEID','TAGE_EHC']].shift()
    same = d.MONTHCODE.eq(prev.MONTHCODE+1) & d.ERESIDENCEID.eq(prev.ERESIDENCEID)
    possible = pd.Series(False,index=d.index)
    for i in range(1,11):
        possible |= prev[f'TT2_AGE{i}'].ge(18) & prev[f'ET2_LNO{i}'].notna() & d[f'ET2_LNO{i}'].isna()
    for r in d.loc[possible & same & prev.TAGE_EHC.between(18,64),['SSUID','PNUM','MONTHCODE']].itertuples(index=False):
        before, after = type2(get(r.SSUID,r.PNUM,int(r.MONTHCODE)-1)), type2(get(r.SSUID,r.PNUM,int(r.MONTHCODE)))
        for person in sorted(before.keys()-after.keys()):
            if before[person] >= 18:
                candidates.append(('type2',r.SSUID,r.PNUM,person,int(r.MONTHCODE)))
    stages = {route: Counter() for route in ['tracked', 'type2']}
    accepted = []
    for route, s, f, o, t in candidates:
        c = stages[route]
        c['candidate_pairs'] += 1
        prior, now = get(s,f,t-1), get(s,f,t)
        if not (prior is not None and 18 <= prior.TAGE_EHC <= 64):
            continue
        c['baseline_working_age'] += 1
        if not 4 <= t <= 10:
            continue
        c['calendar_window'] += 1
        focal_pre = [get(s,f,m) for m in range(t-3,t)]
        if not all(valid(r) for r in focal_pre+[now]):
            continue
        if now.ERESIDENCEID != prior.ERESIDENCEID:
            continue
        c['focal_residence_universe'] += 1
        if route == 'tracked':
            other_pre = [get(s,o,m) for m in range(t-3,t)]
            other_now = get(s,o,t)
            if not all(valid(r) and r.TAGE_EHC >= 18 for r in other_pre+[other_now]):
                continue
            if not all(a.ERESIDENCEID == b.ERESIDENCEID for a,b in zip(focal_pre,other_pre)):
                continue
            if other_now.ERESIDENCEID == now.ERESIDENCEID:
                continue
            spell_boundary = other_now.ERH_BMONTH == t and other_pre[-1].ERH_EMONTH == t-1
            # Disappearance from the focal adult's relationship array corroborates the split.
            roster_agrees = pd.notna(relation(prior,o)) and pd.isna(relation(now,o))
            move_reason = other_now.EEHC_WHY
            prior_earner = other_pre[-1].RMESR in [1,2,3,4,5]
            reported_residence = all(reported(r) for r in focal_pre+[now]+other_pre+[other_now])
            post_other = [get(s,o,m) for m in range(t,t+3)]
            post_focal = [get(s,f,m) for m in range(t,t+3)]
            persistent = all(valid(a) and valid(b) and a.ERESIDENCEID != b.ERESIDENCEID
                             for a,b in zip(post_focal,post_other))
            returned = any(valid(a) and valid(b) and a.ERESIDENCEID == b.ERESIDENCEID
                           for a,b in zip(post_focal,post_other))
        else:
            if not all(type2(r).get(o, -1) >= 18 for r in focal_pre):
                continue
            spell_boundary = True  # No independent address history exists for a Type-2 person.
            roster_agrees = pd.notna(relation(prior,o)) and pd.isna(relation(now,o))
            move_reason, prior_earner = np.nan, np.nan
            reported_residence = all(reported(r) for r in focal_pre+[now])
            post_focal = [get(s,f,m) for m in range(t,t+3)]
            persistent = all(valid(r) and o not in type2(r) for r in post_focal)
            returned = any(valid(r) and o in type2(r) for r in post_focal)
        c['three_pre_co_resident'] += 1
        if not (spell_boundary and roster_agrees):
            c['failed_boundary_or_roster'] += 1
            continue
        c['validated_pairs'] += 1
        accepted.append({'route':route, 'SSUID':s,'PNUM':f,'other':o,'t':t,
                         'relationship':relation(prior,o), 'move_reason':move_reason,
                         'prior_departed_employed':prior_earner,
                         'reported_residence':reported_residence,'persistent':persistent,'returned':returned})
    pairs = pd.DataFrame(accepted)
    if pairs.empty:
        return pd.DataFrame(),pairs,{'stages':{r:dict(c) for r,c in stages.items()},'final':{}}
    # Retain every simultaneous loss at the first eligible event of that adult, per route.
    pairs = pairs[pairs.t.eq(pairs.groupby(['route','SSUID','PNUM']).t.transform('min'))].copy()
    rows = []
    homes = d.groupby(['SSUID','MONTHCODE','ERESIDENCEID']).TAGE_EHC.agg(lambda x: bool((x<18).any()))
    for (route,s,f,t), g in pairs.groupby(['route','SSUID','PNUM','t'], sort=True):
        prior = get(s,f,t-1)
        partner_ids = [prior.EPNSPOUS_EHC,prior.EPNCOHAB_EHC]
        partner = any(pd.notna(p) and str(int(p)).zfill(3) in set(g.other) for p in partner_ids)
        # The relationship-array classification is retained separately from the pointers.
        r = {'route':route,'SSUID':s,'PNUM':f,'t':int(t),'n_departing':len(g),
             'age':prior.TAGE_EHC,'sex':prior.ESEX,'mexican_focal':prior.EHISPAN==1,
             'children':bool(homes.get((s,t-1,prior.ERESIDENCEID),False)) or any(x<18 for x in type2(prior).values()),
             'partner':partner,'relationships':','.join(str(int(x)) for x in sorted(g.relationship.dropna().unique())),
             'reported_residence':bool(g.reported_residence.all()),'persistent':bool(g.persistent.all()),
             'returned':bool(g.returned.any()),'departed_employed':bool(g.prior_departed_employed.eq(True).any()) if route=='tracked' else None}
        follow = [get(s,f,m) for m in range(t,t+3)]
        r['post_records'] = all(x is not None for x in follow)
        r['post_in_universe'] = all(x is not None and x.RIN_UNIV==1 for x in follow)
        r['later_focal_move'] = any(x is not None and x.ERESIDENCEID != prior.ERESIDENCEID for x in follow)
        rows.append(r)
    events = pd.DataFrame(rows)
    audit = {'stages':{r:dict(c) for r,c in stages.items()}, 'final':{}}
    for route,g in events.groupby('route'):
        audit['final'][route] = {'focal_adults':len(g),'sample_units':g.SSUID.nunique(),
                                'departing_pairs':int(g.n_departing.sum()),
                                'post_records':int(g.post_records.sum()),'post_in_universe':int(g.post_in_universe.sum()),
                                'reported_residence':int(g.reported_residence.sum()),'persistent':int(g.persistent.sum()),
                                'returned':int(g.returned.sum()),'partner':int(g.partner.sum()),
                                'children':int(g.children.sum()),'later_focal_move':int(g.later_focal_move.sum())}
    return events,pairs,audit


def main():
    events,pairs,audit = build_events(load_data())
    events.to_parquet(CACHE/'events.parquet',index=False)
    pairs.to_parquet(CACHE/'pairs.parquet',index=False)
    receipt={'events_sha256':sha(CACHE/'events.parquet'),'script_sha256':sha(Path(__file__)),
             'extract_receipt_sha256':sha(CACHE/'extract_receipt.json')}
    (CACHE/'events_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (DERIVED/'event_audit.json').write_text(json.dumps(audit,indent=2,default=int)+'\n')
    comp = pairs.groupby(['route','relationship'],dropna=False).size().rename('pairs').reset_index()
    comp.to_csv(DERIVED/'relationships.csv',index=False,lineterminator='\n')
    pairs.groupby(['route','move_reason'],dropna=False).size().rename('pairs').reset_index().to_csv(
        DERIVED/'move_reasons.csv',index=False,lineterminator='\n')
    print(json.dumps(audit,indent=2,default=int))


if __name__ == '__main__':
    main()
