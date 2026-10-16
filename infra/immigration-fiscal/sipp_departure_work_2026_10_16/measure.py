"""Descriptive within-person changes; no causal or population-removal parameter."""
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

from events import load_data
from extract import CACHE, DERIVED, ROOT, sha

OUTCOMES = ['employment','hours','earnings','calendar_earnings']
SEED = 20261016


def outcomes(d):
    x = d.copy()
    inside = x.RIN_UNIV.eq(1)
    known = inside & x.RMESR.between(1,8)
    nojob = known & x.RMESR.ge(6)
    x['employment'] = np.where(known, x.RMESR.le(5).astype(float), np.nan)
    x['hours'] = x.TMWKHRS.where(inside)
    x.loc[nojob & x.TMWKHRS.isna() & x.AMWKHRS.eq(0),'hours'] = 0.
    # In-universe employed unpaid family workers have no remuneration imputed by SIPP.
    # Require explicit unpaid work, NIU earnings and no visible active paid-job spell.
    active = pd.Series(False,index=x.index)
    for j in range(1,7):
        active |= x.MONTHCODE.ge(x[f'EJB{j}_BMONTH']) & x.MONTHCODE.le(x[f'EJB{j}_EMONTH'])
    unpaid = known & x.RMESR.le(5) & x.ENJ_UPDWKYN.eq(1) & ~active
    for target,raw,flag in [('earnings','TPEARN_ALT','APEARN_ALT'),
                            ('calendar_earnings','TPEARN','APEARN')]:
        x[target] = x[raw].where(inside)
        zero = inside & x[raw].isna() & x[flag].eq(0) & (nojob | unpaid)
        x.loc[zero,target] = 0.
        x[target+'_structural_zero'] = zero
        x[target+'_unpaid_zero'] = zero & unpaid
    return x


def event_panel(events,d):
    # Same people at every relative month; no conditioning on subsequent location.
    long = events.merge(pd.DataFrame({'relative_month':range(-3,3)}),how='cross')
    long['MONTHCODE'] = long.t + long.relative_month
    cols = ['SSUID','PNUM','MONTHCODE','RIN_UNIV','ARESIDENCEID','WPFINWGT'] + OUTCOMES
    cols += [c for c in d if c.endswith(('_structural_zero','_unpaid_zero'))]
    if 'clean_hours' in d:
        cols += ['clean_employment','clean_hours','clean_earnings']
    long = long.merge(d[cols],on=['SSUID','PNUM','MONTHCODE'],how='left',validate='many_to_one')
    dec = d[d.MONTHCODE.eq(12)][['SSUID','PNUM','WPFINWGT']].rename(columns={'WPFINWGT':'dec_weight'})
    long = long.merge(dec,on=['SSUID','PNUM'],how='left',validate='many_to_one')
    assert not long.duplicated(['route','SSUID','PNUM','relative_month']).any()
    return long


def december_replicates(d):
    raw = ROOT/'sources/immigration-fiscal/data/external/stage3/census/sipp_2025/rw2025_csv.zip'
    cached = CACHE/'december_replicates.parquet'
    receipt = CACHE/'replicate_receipt.json'
    raw_hash = sha(raw)
    if cached.exists() and receipt.exists():
        r = json.loads(receipt.read_text())
        assert r['raw_sha256'] == raw_hash and r['parquet_sha256']==sha(cached), '[BLOCKED] stale replicate cache'
        return pd.read_parquet(cached)
    chunks = []
    with zipfile.ZipFile(raw) as z:
        with z.open('rw2025.csv') as f:
            for chunk in pd.read_csv(f,sep='|',dtype={'ssuid':str,'pnum':str},chunksize=20000):
                chunks.append(chunk[chunk.monthcode.eq(12)].copy())
    w = pd.concat(chunks,ignore_index=True)
    w = w.rename(columns={'ssuid':'SSUID','pnum':'PNUM'})
    assert not w.duplicated(['SSUID','PNUM']).any()
    assert {f'repwgt{i}' for i in range(241)} <= set(w.columns)
    dec = d[d.MONTHCODE.eq(12)][['SSUID','PNUM','WPFINWGT']]
    check = dec.merge(w,on=['SSUID','PNUM'],how='left',validate='one_to_one',indicator=True)
    missing = check._merge.eq('left_only')
    coverage = {'December_person_records':len(dec),'without_replicate_record':int(missing.sum()),
                'missing_replicates_positive_full_weight':int((missing & check.WPFINWGT.gt(0)).sum())}
    print(json.dumps(coverage))
    assert not (missing & check.WPFINWGT.gt(0)).any(), '[BLOCKED] positive-weight records lack replicates'
    matched = check[~missing]
    assert np.allclose(matched.repwgt0,matched.WPFINWGT,atol=.0001), '[BLOCKED] replicate/full weights disagree'
    w.to_parquet(cached,index=False)
    r={'raw_sha256':raw_hash,'source_url':'https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/rw2025_csv.zip',
       'parquet_sha256':sha(cached),'rows':len(w),'replicates':240,'fay_k':.5,'coverage':coverage}
    receipt.write_text(json.dumps(r,indent=2)+'\n')
    (DERIVED/'replicate_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    return w


def cluster_interval(values,groups):
    frame = pd.DataFrame({'g':groups,'v':values})
    c = frame.groupby('g').v.agg(['sum','count'])
    if len(c)<2:
        return np.nan,np.nan
    rng = np.random.default_rng(SEED)
    draws = rng.multinomial(len(c),np.repeat(1/len(c),len(c)),size=1999)
    means = (draws@c['sum'].to_numpy())/(draws@c['count'].to_numpy())
    return tuple(np.quantile(means,[.025,.975]))


def summarize(panel,replicates):
    rows,curves,attrition,distributions = [],[],[],[]
    key=['SSUID','PNUM']
    for route,allrows in panel.groupby('route'):
        meta=allrows.drop_duplicates(key).set_index(key)
        complete={o:allrows.pivot(index=key,columns='relative_month',values=o).notna().all(axis=1) for o in OUTCOMES}
        common=pd.concat([complete[o] for o in OUTCOMES[:3]],axis=1).all(axis=1)
        specs={'all':pd.Series(True,index=meta.index),
               'reported_residence':meta.reported_residence,
               'persistent':meta.persistent,'partner':meta.partner,'other_relationship':~meta.partner,
               'children':meta.children,'no_children':~meta.children,
               'common_outcomes':common,
               'female':meta.sex.eq(2),'male':meta.sex.eq(1)}
        if route=='tracked':
            specs.update({'departed_employed':meta.departed_employed.eq(True),
                          'departed_not_employed':meta.departed_employed.eq(False)})
        for outcome in OUTCOMES:
            matrix=allrows.pivot(index=key,columns='relative_month',values=outcome).reindex(columns=range(-3,3))
            attrition.append({'route':route,'outcome':outcome,'eligible_adults':len(meta),
                              'complete_six_months':int(complete[outcome].sum()),
                              'missing_pre':int(matrix.loc[:,[-3,-2,-1]].isna().any(axis=1).sum()),
                              'missing_post':int(matrix.loc[:,[0,1,2]].isna().any(axis=1).sum())})
            local_specs=dict(specs)
            clean_name='clean_'+('earnings' if 'earnings' in outcome else outcome)
            if clean_name in allrows:
                clean=allrows.pivot(index=key,columns='relative_month',values=clean_name).fillna(False).all(axis=1)
                local_specs['visible_components_unallocated']=clean
            if 'earnings' in outcome:
                unpaid=allrows.groupby(key)[outcome+'_unpaid_zero'].any()
                local_specs['unpaid_zero_as_missing']=~unpaid
            for spec,mask in local_specs.items():
                z=matrix.loc[mask & complete[outcome]].copy()
                if len(z)==0:
                    continue
                pre=z[[-3,-2,-1]].mean(axis=1); post=z[[0,1,2]].mean(axis=1)
                delta=post-pre
                lo,hi=cluster_interval(delta.to_numpy(),z.index.get_level_values('SSUID'))
                rows.append({'route':route,'specification':spec,'outcome':outcome,'weighting':'unweighted',
                             'adults':len(z),'clusters':z.index.get_level_values('SSUID').nunique(),
                             'pre':pre.mean(),'post':post.mean(),'change':delta.mean(),'ci_low':lo,'ci_high':hi,
                             'interval':'95% percentile cluster bootstrap; 1999 draws'})
                if spec=='all':
                    for m in range(-3,3):
                        ml,mh=cluster_interval(z[m].to_numpy(),z.index.get_level_values('SSUID'))
                        curves.append({'route':route,'outcome':outcome,'relative_month':m,'adults':len(z),
                                       'mean':z[m].mean(),'ci_low':ml,'ci_high':mh})
                    for contrast,change in [('three_month_average',delta),('immediate',z[0]-z[-1]),
                                            ('pre_trend',z[-1]-z[-3])]:
                        dl,dh=cluster_interval(change.to_numpy(),z.index.get_level_values('SSUID'))
                        distributions.append({'route':route,'outcome':outcome,'contrast':contrast,'adults':len(z),
                            'mean':change.mean(),'ci_low':dl,'ci_high':dh,'median':change.median(),
                            'p10':change.quantile(.1),'p90':change.quantile(.9),
                            'increase':int(change.gt(1e-8).sum()),'unchanged':int(change.abs().le(1e-8).sum()),
                            'decrease':int(change.lt(-1e-8).sum())})
                if spec in ['all','reported_residence','persistent','common_outcomes']:
                    zw=z.join(replicates.set_index(key)[[f'repwgt{i}' for i in range(241)]],how='left')
                    zw=zw[zw.repwgt0.gt(0)]
                    if len(zw)==0:
                        continue
                    weights=zw[[f'repwgt{i}' for i in range(241)]].to_numpy()
                    assert np.isfinite(weights).all()
                    before=zw[[-3,-2,-1]].mean(axis=1).to_numpy()
                    after=zw[[0,1,2]].mean(axis=1).to_numpy()
                    estimates=((after-before)@weights)/weights.sum(axis=0)
                    se=np.sqrt(np.sum((estimates[1:]-estimates[0])**2)/(240*.5**2))
                    rows.append({'route':route,'specification':spec,'outcome':outcome,'weighting':'December_weighted',
                                 'adults':len(zw),'clusters':zw.index.get_level_values('SSUID').nunique(),
                                 'pre':np.average(before,weights=weights[:,0]),'post':np.average(after,weights=weights[:,0]),
                                 'change':estimates[0],'ci_low':estimates[0]-1.96*se,'ci_high':estimates[0]+1.96*se,
                                 'interval':'95% normal Fay BRR; 240 December replicates, k=.5'})
    return [pd.DataFrame(v) for v in [rows,curves,attrition,distributions]]


def main():
    d=outcomes(load_data())
    components=CACHE/'component_flags.parquet'
    assert components.exists(), '[BLOCKED] run components.py before measuring'
    if components.exists():
        flags=pd.read_parquet(components)
        receipt=json.loads((CACHE/'component_allocation_receipt.json').read_text())
        assert receipt['status']=='complete' and receipt['script_sha256']==sha(Path(__file__).with_name('components.py'))
        assert receipt['definitions_sha256']==sha(Path(__file__).with_name('component_definitions.json'))
        assert receipt['output']['sha256']==sha(components), '[BLOCKED] stale component flags'
        flags['PNUM']=flags.PNUM.astype(str).str.zfill(3)
        keep=['SSUID','PNUM','MONTHCODE']
        for outcome in ['employment','hours','earnings']:
            flags['clean_'+outcome]=flags[outcome+'__complete_clean']
            keep.append('clean_'+outcome)
        flags=flags[keep]
        d=d.merge(flags,on=['SSUID','PNUM','MONTHCODE'],how='left',validate='one_to_one')
        assert d.clean_hours.notna().all()
    event_receipt=json.loads((CACHE/'events_receipt.json').read_text())
    assert event_receipt['events_sha256']==sha(CACHE/'events.parquet')
    assert event_receipt['script_sha256']==sha(Path(__file__).with_name('events.py')), '[BLOCKED] rerun events'
    assert event_receipt['extract_receipt_sha256']==sha(CACHE/'extract_receipt.json')
    events=pd.read_parquet(CACHE/'events.parquet')
    panel=event_panel(events,d)
    panel.to_parquet(CACHE/'event_panel.parquet',index=False)
    (CACHE/'panel_receipt.json').write_text(json.dumps({'panel_sha256':sha(CACHE/'event_panel.parquet'),
        'script_sha256':sha(Path(__file__)),'events_receipt_sha256':sha(CACHE/'events_receipt.json')},indent=2)+'\n')
    w=december_replicates(d)
    results=summarize(panel,w)
    for name,result in zip(['changes','monthly','attrition','distributions'],results):
        result.to_csv(DERIVED/f'{name}.csv',index=False,lineterminator='\n',float_format='%.10g')
    diagnostics={}
    for route,g in panel.groupby('route'):
        diagnostics[route]={'rows':len(g),'missing_hours_employed':int((g.employment.eq(1)&g.hours.isna()).sum()),
                            'earnings_unpaid_zeros':int(g.earnings_unpaid_zero.fillna(False).sum()),
                            'earnings_structural_zeros':int(g.earnings_structural_zero.fillna(False).sum())}
    (DERIVED/'outcome_coding.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    print(results[0].query('specification=="all"').to_string(index=False))


if __name__=='__main__':
    main()
