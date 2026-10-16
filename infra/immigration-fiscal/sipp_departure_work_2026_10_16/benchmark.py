"""Calendar/baseline-standardized descriptive comparison, not a causal design."""
import json

import numpy as np
import pandas as pd

from events import load_data, type2
from extract import CACHE, DERIVED, HERE, sha
from measure import OUTCOMES, SEED, outcomes


def strata(frame,children=False):
    age=np.select([frame.age.le(29),frame.age.le(44)],[0,1],default=2)
    pre=frame[['employment_m3','employment_m2','employment_m1']].sum(axis=1)
    emp=np.select([pre.eq(0),pre.eq(3)],[0,2],default=1)
    labels=[str(t)+'|'+str(int(s))+'|'+str(a)+'|'+str(e)
            for t,s,a,e in zip(frame.t,frame.sex,age,emp)]
    if children:
        labels=[s+'|'+str(int(c)) for s,c in zip(labels,frame.children)]
    return labels


def build_controls(d):
    d=d.sort_values(['SSUID','PNUM','MONTHCODE']).reset_index(drop=True)
    valid=d.RIN_UNIV.eq(1)&d.ERESIDENCEID.notna()
    adults=d[valid & d.TAGE_EHC.ge(18)]
    sets=adults.groupby(['SSUID','MONTHCODE','ERESIDENCEID']).PNUM.agg(frozenset).to_dict()
    children=d[valid].groupby(['SSUID','MONTHCODE','ERESIDENCEID']).TAGE_EHC.agg(lambda x:bool(x.lt(18).any())).to_dict()
    # Public Type-2 numbers remain local to a focal roster; do not link them across respondents.
    member_sets=[]; child_flags=[]
    for r in d.itertuples(index=False):
        home=(r.SSUID,r.MONTHCODE,r.ERESIDENCEID)
        t2={str(int(getattr(r,f'ET2_LNO{i}'))).zfill(3):getattr(r,f'TT2_AGE{i}')
            for i in range(1,11) if pd.notna(getattr(r,f'ET2_LNO{i}'))}
        member_sets.append(sets.get(home,frozenset())|frozenset(k for k,v in t2.items() if v>=18))
        child_flags.append(children.get(home,False) or any(v<18 for v in t2.values()))
    d['members']=member_sets; d['children']=child_flags
    cols=['MONTHCODE','ERESIDENCEID','RIN_UNIV','TAGE_EHC','ESEX','members','children']+OUTCOMES
    groups=d.groupby(['SSUID','PNUM'],sort=False)
    shifts={k:groups[cols].shift(-k) for k in [-3,-2,-1,0,1,2]}
    now=shifts[0]; prior=shifts[-1]
    eligible=now.MONTHCODE.between(4,10)&prior.TAGE_EHC.between(18,64)&now.RIN_UNIV.eq(1)
    eligible &= now.ERESIDENCEID.eq(prior.ERESIDENCEID)
    for k in [-3,-2,-1]:
        eligible &= shifts[k].MONTHCODE.eq(now.MONTHCODE+k)&shifts[k].RIN_UNIV.eq(1)
        eligible &= shifts[k].ERESIDENCEID.eq(prior.ERESIDENCEID)
    ix=np.flatnonzero(eligible)
    keep=[]; future=[]
    for i in ix:
        pre=[shifts[k].at[i,'members'] for k in [-3,-2,-1]]
        # One adult other than the focal person must be co-resident throughout baseline.
        if len(pre[0]&pre[1]&pre[2])<2 or not pre[-1].issubset(now.at[i,'members']):
            continue
        keep.append(i)
        future.append(any(isinstance(shifts[k].at[i,'members'],frozenset)
                          and not pre[-1].issubset(shifts[k].at[i,'members']) for k in [1,2]))
    c=d.loc[keep,['SSUID','PNUM']].copy()
    c['t']=now.loc[keep,'MONTHCODE']; c['age']=prior.loc[keep,'TAGE_EHC']
    c['sex']=prior.loc[keep,'ESEX'];c['children']=prior.loc[keep,'children']
    c['future_departure']=future
    for k in [-3,-2,-1,0,1,2]:
        for o in OUTCOMES:
            c[f'{o}_'+('m'+str(-k) if k<0 else 'p'+str(k))]=shifts[k].loc[keep,o].where(
                shifts[k].loc[keep,'MONTHCODE'].eq(now.loc[keep,'MONTHCODE']+k))
    return c.reset_index(drop=True)


def make_events():
    receipt=json.loads((CACHE/'panel_receipt.json').read_text())
    assert receipt['panel_sha256']==sha(CACHE/'event_panel.parquet')
    assert receipt['script_sha256']==sha(HERE/'measure.py'), '[BLOCKED] rerun measure'
    assert receipt['events_receipt_sha256']==sha(CACHE/'events_receipt.json')
    p=pd.read_parquet(CACHE/'event_panel.parquet')
    meta=p.drop_duplicates(['route','SSUID','PNUM'])[['route','SSUID','PNUM','t','age','sex','children']]
    for o in OUTCOMES:
        mat=p.pivot(index=['route','SSUID','PNUM'],columns='relative_month',values=o)
        mat.columns=[f'{o}_'+('m'+str(-k) if k<0 else 'p'+str(k)) for k in mat.columns]
        meta=meta.merge(mat.reset_index(),on=['route','SSUID','PNUM'],validate='one_to_one')
    return meta


def standardize(e,c,outcome,with_children):
    columns=[f'{outcome}_{s}' for s in ['m3','m2','m1','p0','p1','p2']]
    employment=[f'employment_{s}' for s in ['m3','m2','m1']]
    e=e.dropna(subset=columns+employment).copy();c=c.dropna(subset=columns+employment).copy()
    e['stratum']=strata(e,with_children);c['stratum']=strata(c,with_children)
    support=c.groupby('stratum').SSUID.nunique()
    supported=set(support[support.ge(5)].index)&set(e.stratum)
    eligible=len(e);e=e[e.stratum.isin(supported)];c=c[c.stratum.isin(supported)]
    if len(e)==0:
        return [{'status':'unsupported_no_control_strata','contrast':contrast,'outcome':outcome,
                 'matching':'month_sex_age_prework'+('_children' if with_children else ''),
                 'eligible_event_adults':eligible,'supported_event_adults':0,
                 'control_person_anchors':0,'control_people':0,'control_clusters':0,
                 'future_departure_control_anchors':0,'strata':0,'event_change':np.nan,
                 'benchmark_change':np.nan,'difference':np.nan,'ci_low':np.nan,'ci_high':np.nan,
                 'valid_bootstrap_draws':0,'interval':'not estimable'}
                for contrast in ['three_month_change','pre_trend']]
    names=sorted(supported);smap={s:i for i,s in enumerate(names)}
    es=e.stratum.map(smap).to_numpy();cs=c.stratum.map(smap).to_numpy();n=len(names)
    clusters=sorted(set(e.SSUID)|set(c.SSUID));cluster_map={s:i for i,s in enumerate(clusters)}
    eg=e.SSUID.map(cluster_map).to_numpy();cg=c.SSUID.map(cluster_map).to_numpy()
    answer=[]
    for contrast in ['three_month_change','pre_trend']:
        def delta(frame):
            if contrast=='pre_trend':
                return (frame[f'{outcome}_m1']-frame[f'{outcome}_m3']).to_numpy()
            return (frame[[f'{outcome}_p{k}' for k in range(3)]].mean(axis=1)-
                    frame[[f'{outcome}_m{k}' for k in [3,2,1]]].mean(axis=1)).to_numpy()
        ey,cy=delta(e),delta(c)
        def calc(ew,cw):
            en=np.bincount(es,weights=ew,minlength=n);cn=np.bincount(cs,weights=cw,minlength=n)
            if en.sum()==0 or np.any((en>0)&(cn==0)):
                return np.nan,np.nan,np.nan
            means=np.divide(np.bincount(cs,weights=cw*cy,minlength=n),cn,out=np.zeros(n),where=cn>0)
            actual=np.sum(ew*ey)/en.sum();bench=np.sum(en*means)/en.sum()
            return actual,bench,actual-bench
        actual,bench,diff=calc(np.ones(len(e)),np.ones(len(c)))
        # Aggregate by original sample unit and stratum once, then resample.
        # This is the same statistic as the row-level loop, without revisiting
        # tens of thousands of control anchors for every bootstrap draw.
        matrices=[]
        for gids,sids,vals in [(eg,es,np.ones(len(e))),(eg,es,ey),
                              (cg,cs,np.ones(len(c))),(cg,cs,cy)]:
            matrix=np.zeros((len(clusters),n))
            np.add.at(matrix,(gids,sids),vals)
            matrices.append(matrix)
        weights=np.random.default_rng(SEED).poisson(1,(1999,len(clusters)))
        en,eysum,cn,cysum=[weights@matrix for matrix in matrices]
        valid=(en.sum(axis=1)>0)&~((en>0)&(cn==0)).any(axis=1)
        cm=np.divide(cysum,cn,out=np.zeros_like(cysum),where=cn>0)
        draws=np.divide(eysum.sum(axis=1)-(en*cm).sum(axis=1),en.sum(axis=1),
                        out=np.full(1999,np.nan),where=valid)
        finite=draws[np.isfinite(draws)]
        assert len(finite)>=1950, '[BLOCKED] unstable benchmark bootstrap support'
        lo,hi=np.quantile(finite,[.025,.975])
        answer.append({'status':'ok','contrast':contrast,'outcome':outcome,'matching':'month_sex_age_prework'+('_children' if with_children else ''),
                       'eligible_event_adults':eligible,'supported_event_adults':len(e),'control_person_anchors':len(c),
                       'control_people':len(c[['SSUID','PNUM']].drop_duplicates()),'control_clusters':c.SSUID.nunique(),
                       'future_departure_control_anchors':int(c.future_departure.sum()),'strata':n,
                       'event_change':actual,'benchmark_change':bench,'difference':diff,'ci_low':lo,'ci_high':hi,
                       'valid_bootstrap_draws':len(finite),'interval':'95% Poisson original-sample-unit bootstrap, 1999 draws'})
    return answer


def main():
    controls=build_controls(outcomes(load_data()))
    controls.to_parquet(CACHE/'controls.parquet',index=False)
    events=make_events();results=[]
    for route,e in events.groupby('route'):
        for o in OUTCOMES[:3]:
            for child in [False,True]:
                results += [dict(route=route,**r) for r in standardize(e,controls,o,child)]
    pd.DataFrame(results).to_csv(DERIVED/'benchmark.csv',index=False,lineterminator='\n',float_format='%.10g')
    print(pd.DataFrame(results).query('matching=="month_sex_age_prework" and contrast=="three_month_change"').to_string(index=False))


if __name__=='__main__':
    main()
