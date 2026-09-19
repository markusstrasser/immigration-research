"""Common-definition civilian household wage distributions: ACS2024 vs CPS2025."""
from pathlib import Path
import argparse, json, zipfile
import numpy as np
import pandas as pd
from common import AW,CW,cps,quantile,sha,summary

HERE=Path(__file__).resolve().parent
WAGE_EDGES=[0,10000,25000,50000,100000,200000,np.inf]

def masks(d):
    s=d.selfid.to_numpy(bool); b=d.born.to_numpy(bool)
    return {'all':np.ones(len(d),bool),'selfid_mexican':s,'other_selfid':~s,
            'mexico_born':b,'other_born':~b,'selfid_or_mexico_born':s|b,'other_union':~(s|b)}

def aggregate(chunks,nreps):
    estimates={}; points=[]; nraw=0; nkeep=0
    for d in chunks:
        nraw+=int(d.attrs.get('raw_rows',len(d))); nkeep+=len(d)
        w=d[['w0']+[f'w{i}' for i in range(1,nreps+1)]].to_numpy(float)
        x=d.wage.to_numpy(float); earn=x>0; group=masks(d)
        points.append(d[['state','selfid','born','wage','w0']].loc[earn].copy())
        for region,geo in [('US',np.ones(len(d),bool)),('CA',d.state.eq(6).to_numpy()),('TX',d.state.eq(48).to_numpy())]:
            for g,m in group.items():
                keep=geo&m; k=keep&earn
                metrics={'population':np.ones(len(d)),'wage_recipients':earn.astype(float),'wage_sum':x}
                for j,(lo,hi) in enumerate(zip(WAGE_EDGES[:-1],WAGE_EDGES[1:])):
                    metrics[f'earner_band_{j}']=((x>0)&(x>=lo)&(x<hi)).astype(float)
                for metric,v in metrics.items():
                    key=(region,g,metric)
                    estimates[key]=estimates.get(key,np.zeros(nreps+1))+v[keep]@w[keep]
    point=pd.concat(points,ignore_index=True)
    rows=[]
    for (region,g,metric),v in list(estimates.items()):
        rows.append({'region':region,'group':g,'metric':metric,**summary(v)})
        if metric.startswith('earner_band_'):
            rows.append({'region':region,'group':g,'metric':metric+'_share',**summary(v/estimates[(region,g,'wage_recipients')])})
        if metric=='wage_sum':
            den=estimates[(region,g,'wage_recipients')]
            if np.any(den<=0): raise ValueError('Empty replicate earner domain')
            rows.append({'region':region,'group':g,'metric':'mean_per_earner',**summary(v/den)})
            rows.append({'region':region,'group':g,'metric':'wages_per_resident',**summary(v/estimates[(region,g,'population')])})
    for region,geo in [('US',np.ones(len(point),bool)),('CA',point.state.eq(6).to_numpy()),('TX',point.state.eq(48).to_numpy())]:
        for g,m in masks(point).items():
            part=point.loc[geo&m]
            for q in [.25,.5,.75]:
                rows.append({'region':region,'group':g,'metric':f'p{int(q*100)}_earner','estimate':quantile(part.wage,part.w0,q),'se_sampling':None,'ci95_low':None,'ci95_high':None})
        for target,rest in [('selfid_mexican','other_selfid'),('mexico_born','other_born'),('selfid_or_mexico_born','other_union')]:
            for metric in ['population','wage_recipients','wage_sum']:
                np.testing.assert_allclose(estimates[(region,'all',metric)],estimates[(region,target,metric)]+estimates[(region,rest,metric)],rtol=1e-12,atol=.1)
            relative_mean=(estimates[(region,target,'wage_sum')]/estimates[(region,target,'wage_recipients')])/(estimates[(region,rest,'wage_sum')]/estimates[(region,rest,'wage_recipients')])
            rows.append({'region':region,'group':target,'metric':'mean_ratio_to_complement',**summary(relative_mean)})
    return pd.DataFrame(rows),{'raw_rows':nraw,'retained_civilian_household_rows':nkeep,'quantile_se':'Not estimated; quantiles descriptive point estimates only','replicates':nreps}

def acs_chunks(path):
    fields=['AGEP','RELSHIPP','ESR','STATE','HISP','POBP','WAGP','ADJINC',*AW]
    with zipfile.ZipFile(path) as z:
        files=[p for p in z.namelist() if p.endswith('.csv') and 'psam_pus' in p]
        if len(files)!=2: raise ValueError('Expected two national ACS2024 person members')
        for name in files:
            for d in pd.read_csv(z.open(name),usecols=fields,chunksize=100000):
                n=len(d)
                d=d.loc[d.RELSHIPP.lt(37)&~d.ESR.isin([4,5])].copy()
                if d.loc[d.AGEP.ge(15),'WAGP'].isna().any(): raise ValueError('Missing adult ACS wages')
                d['wage']=d.WAGP.fillna(0)*d.ADJINC/1e6
                if d.wage.lt(0).any(): raise ValueError('Negative ACS wage sentinel')
                d=d.assign(state=d.STATE,selfid=d.HISP.eq(2),born=d.POBP.eq(303))
                d=d.rename(columns={a:f'w{i}' for i,a in enumerate(AW)})
                d.attrs['raw_rows']=n
                yield d

def cps_chunks(path):
    d=cps(path,2025); n=len(d)
    d=d.loc[d.civilian&d.household].copy()
    d=d.assign(state=d.GESTFIPS,selfid=d.PRDTHSP.eq(1),born=d.PENATVTY.eq(303),wage=d.WSAL_VAL)
    d=d.rename(columns={a:f'w{i}' for i,a in enumerate(CW)}); d.attrs['raw_rows']=n
    yield d

def run(args):
    root=args.source_root; out=args.out; out.mkdir(parents=True,exist_ok=True)
    acs=root/'sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip'
    cp=root/'infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    a,aa=aggregate(acs_chunks(acs),80); print('ACS complete',flush=True)
    if aa['raw_rows']!=3422888: raise ValueError('Unexpected ACS2024 national raw row count')
    c,ca=aggregate(cps_chunks(cp),160); print('CPS complete',flush=True)
    both=pd.concat([a.assign(survey='acs2024'),c.assign(survey='cps2025_income2024')],ignore_index=True)
    comp=a.merge(c,on=['region','group','metric'],suffixes=('_acs','_cps'),validate='one_to_one')
    comp['acs_vs_cps_pct']=100*(comp.estimate_acs/comp.estimate_cps-1)
    both.to_csv(out/'wage_distributions.csv',index=False); comp.to_csv(out/'acs_cps_comparison.csv',index=False)
    audit={'acs':aa,'cps':ca,'source_hashes':{str(p):sha(p) for p in [acs,cp,HERE/'acs_check.py',HERE/'common.py',root/'sources/immigration-fiscal/data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.csv']},
           'outputs':{f:sha(out/f) for f in ['wage_distributions.csv','acs_cps_comparison.csv']},
           'scope':'Civilian private-household persons, all ages for resident totals; wage recipients have positive wages (income universe15+). CPS HHSTATUS1..3 and PRPERTYP1/2; ACS RELSHIPP<37 and ESR not4/5.',
           'limits':['ACS rolling past12months adjusted to2024 dollars versus CPS calendar2024; no exact time equality','SelfID and birthplace common definitions do not reproduce full CPS parental-origin union','Both are household surveys; agreement is corroboration, not independent administrative validation','Quantile sampling intervals not computed; totals/means use official SDR replicates; no cross-survey z-test or causal interpretation']}
    (out/'acs_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(comp.query('region=="US" and metric in ["mean_per_earner","p50_earner","wage_sum"]')[['group','metric','estimate_acs','estimate_cps','acs_vs_cps_pct']].to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--source-root',type=Path,required=True); p.add_argument('--out',type=Path,default=HERE/'derived')
    run(p.parse_args())
