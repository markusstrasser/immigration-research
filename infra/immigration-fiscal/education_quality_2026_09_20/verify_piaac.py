"""Independent raw-file PIAAC calculation with QR WLS; analyzer not imported."""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import json
import math
import statistics
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.linalg import lstsq
from scipy.stats import norm, t

ROOT=Path(__file__).resolve().parent/'derived/piaac'
DATA=_data_paths.reused_surveys_root(require_exists=False)
WCOLS=['SPFWT'+str(k) for k in range(46)]
PV={d:[p+str(k) for k in range(1,11)] for d,p in [('literacy','PVLIT'),('numeracy','PVNUM')]}
FACTORS=['EDCAT8','J_Q04A','J_Q06A','J_Q07A','RACETHN_5CAT','AGEG5LFSEXT','GENDER_R']
COLS=FACTORS+WCOLS+PV['literacy']+PV['numeracy']+['VENREPS','VEFAYFAC']
reported=json.loads((ROOT/'replicate_pv_estimates.json').read_text())
components={}; supports={}; data={}; checks=[]; checks_n=0
def compare(label,actual,expected):
    global checks_n
    a=np.asarray(actual,dtype=float);e=np.asarray(expected,dtype=float)
    assert a.shape==e.shape,(label,a.shape,e.shape)
    assert np.allclose(a,e,rtol=1e-8,atol=1e-8,equal_nan=True),(label,float(np.nanmax(abs(a-e))))
    checks.append({'name':label,'max_abs_difference':float(np.nanmax(abs(a-e))) if a.size else 0})
    checks_n+=a.size
def combine(values):
    full=values[0].tolist()
    point=statistics.mean(full)
    sampling=statistics.mean([math.fsum((float(values[r,p])-full[p])**2 for r in range(1,46)) for p in range(10)])
    between=1.1*statistics.variance(full)
    se=math.sqrt(sampling+between)
    return {'estimate':point,'se':se,'sampling_variance':sampling,'plausible_value_variance':between,
            'low95_normal':point-norm.ppf(.975)*se,'high95_normal':point+norm.ppf(.975)*se,
            'low95_t45':point-t.ppf(.975,45)*se,'high95_t45':point+t.ppf(.975,45)*se}
def domain_mean(frame,mask,domain):
    sub=frame.loc[mask & frame[PV[domain]].notna().all(axis=1)]
    y=sub[PV[domain]].to_numpy(float);w=sub[WCOLS].to_numpy(float)
    result=np.empty((46,10))
    for r in range(46):
        den=math.fsum(w[:,r]);assert den>0
        for p in range(10):result[r,p]=math.fsum(float(wi)*float(yi) for wi,yi in zip(w[:,r],y[:,p]))/den
    main=w[:,0]; total=math.fsum(main)
    support={'eligible_n':int(mask.sum()),'scored_n':len(sub),'missing_scores_n':int(mask.sum())-len(sub),
             'kish_n':total*total/math.fsum(x*x for x in main),'max_weight_share':max(main)/total,'weight_sum':total}
    return result,support
metadata={}; secondary=[]
for wave in ['2012_14','2017']:
    if wave=='2012_14':
        with zipfile.ZipFile(DATA/'docs/2016667REV_HHPUF.zip') as z:
            with z.open('SAS/prgushp1_puf.sas7bdat') as f: d=pd.read_sas(f,format='sas7bdat',encoding='utf-8')
        d.columns=d.columns.str.upper()
        d=d[COLS+['VEMETHOD']].copy()
    else:
        d=pd.read_csv(DATA/'piaac/prgusap1_2017.csv',sep='|',usecols=COLS+['VEMETHOD'],low_memory=False)
    assert set(d.VEMETHOD)=={'JK2'}
    for c in COLS:d[c]=pd.to_numeric(d[c],errors='coerce')
    assert d.VENREPS.eq(45).all() and d.VEFAYFAC.eq(0).all()
    assert len(d)==({'2012_14':8670,'2017':3660}[wave])
    assert np.isfinite(d[WCOLS]).all().all() and d[WCOLS].ge(0).all().all() and d.SPFWT0.gt(0).all()
    extracted=pd.read_csv(ROOT/f'{wave}_source_extract.csv',low_memory=False)
    compare(wave+'.source_values',d[COLS],extracted[COLS])
    data[wave]=d
    metadata[wave]={'n':len(d),'factor_distributions':{c:{str(k):int(v) for k,v in d[c].value_counts(dropna=False).items()} for c in FACTORS},'PV_missing':{domain:int(d[names].isna().all(axis=1).sum()) for domain,names in PV.items()}}
    ages=d.AGEG5LFSEXT.isin(range(3,11))
    for domain in PV:
        a,s=domain_mean(d,ages,domain);key=f'{wave}|benchmark|{domain}'
        components[key]=a;supports[key]=s
        if wave=='2012_14':
            ba,_=domain_mean(d,ages & d.EDCAT8.isin([6,7,8]),domain)
            target={'literacy':(304,1.6),'numeracy':(295,1.8)}[domain]
            b=combine(ba);assert abs(b['estimate']-target[0])<.51 and abs(b['se']-target[1])<.051
            secondary.append({'wave':wave,'domain':domain,'all_BAplus_national':b})
    for credential in ['BAplus','BA_only']:
        ba=d.EDCAT8.isin([6,7,8] if credential=='BAplus' else [6])
        native=d.J_Q04A.eq(1)&d.J_Q06A.eq(1)&d.J_Q07A.eq(1)
        sample=ages & ba & native & d.RACETHN_5CAT.isin([1,2])
        for domain in PV:
            for name,code in [('Hispanic',1),('NH_white',2)]:
                a,s=domain_mean(d,sample & d.RACETHN_5CAT.eq(code),domain)
                key=f'{wave}|{credential}|{domain}|{name}';components[key]=a;supports[key]=s
            key=f'{wave}|{credential}|{domain}'
            components[key+'|difference']=components[key+'|Hispanic']-components[key+'|NH_white']
            sub=d.loc[sample & d[PV[domain]].notna().all(axis=1) & d.GENDER_R.isin([1,2])]
            # A complete weighted QR solve, re-estimated for each replicate/PV.
            x=np.array([[1,int(r.RACETHN_5CAT==1),int(r.GENDER_R==2)]+[int(r.AGEG5LFSEXT==k) for k in range(4,11)] for r in sub.itertuples()],dtype=float)
            y=sub[PV[domain]].to_numpy(float);w=sub[WCOLS].to_numpy(float)
            fit=np.empty((46,10))
            ranks=[]
            for r in range(46):
                rootw=np.sqrt(w[:,r]);coefs,_,rank,_=lstsq(x*rootw[:,None],y*rootw[:,None],lapack_driver='gelsy')
                assert rank==x.shape[1];ranks.append(int(rank));fit[r]=coefs[1]
            components[key+'|adjusted']=fit
            supports[key+'|adjusted']={'scored_n':len(sub),'hispanic_n':int(sub.RACETHN_5CAT.eq(1).sum()),'white_n':int(sub.RACETHN_5CAT.eq(2).sum()),'missing_sex_n':int((sample & ~d.GENDER_R.isin([1,2])).sum())}
for key,a in components.items():compare(key+'.460_estimates',a,reported[key])
assert set(components)==set(reported)
for filename in ['means','contrasts','benchmarks']:
    for r in pd.read_csv(ROOT/f'{filename}.csv').to_dict('records'):
        if filename=='benchmarks':key=f"{r['wave']}|benchmark|{r['domain']}"
        elif filename=='means':key=f"{r['wave']}|{r['credential']}|{r['domain']}|{r['group']}"
        else:key=f"{r['wave']}|{r['credential']}|{r['domain']}|"+('difference' if r['adjustment']=='none' else 'adjusted')
        result=combine(components[key])
        for field,value in result.items():compare(key+'.'+field,value,r[field])
        if filename!='contrasts':
            for field,value in supports[key].items():compare(key+'.'+field,value,r[field])
        if filename=='benchmarks':
            assert abs(result['estimate']-r['published_mean'])<.51 and abs(result['se']-r['published_se'])<.051
for r in pd.read_csv(ROOT/'adjustment_support.csv').to_dict('records'):
    key=f"{r['wave']}|{r['credential']}|{r['domain']}|adjusted"
    for field,value in supports[key].items():compare(key+'.'+field,value,r[field])
for r in pd.read_csv(ROOT/'composition.csv').to_dict('records'):
    d=data[r['wave']];degree=d.EDCAT8.isin([6,7,8] if r['credential']=='BAplus' else [6])
    m=d.AGEG5LFSEXT.isin(range(3,11))&degree&d.J_Q04A.eq(1)&d.J_Q06A.eq(1)&d.J_Q07A.eq(1)&d.RACETHN_5CAT.eq(1 if r['group']=='Hispanic' else 2)
    member=m&d[r['variable']].eq(r['category']);compare('composition.n',int(member.sum()),r['n'])
    compare('composition.share',math.fsum(d.loc[member,'SPFWT0'])/math.fsum(d.loc[m,'SPFWT0']),r['weighted_share'])
max_naive_se_error=0
for key in components:
    if not key.endswith('|difference'):continue
    start=key.rsplit('|',1)[0]
    true=combine(components[key])['se']
    naive=math.hypot(combine(components[start+'|Hispanic'])['se'],combine(components[start+'|NH_white'])['se'])
    max_naive_se_error=max(max_naive_se_error,abs(true-naive))
result={'verdict':'PASS','component_matrices':len(components),'all_replicate_PV_estimates_checked':len(components)*460,
        'scalar_checks_including_raw_extract_cells':checks_n,'max_abs_difference':max(x['max_abs_difference'] for x in checks),
        'variance':'45 JK2 replicate deviations summed per PV; average across 10; add 1.1 times sample variance of 10 full-PV estimates',
        'regression':'independent pivoted QR via scipy.linalg.lstsq/gelsy; all replicate ranks full',
        'max_error_from_incorrect_independent_group_SE':max_naive_se_error,'raw':metadata,'secondary_benchmarks':secondary,
        'summary_counts':{'means':16,'contrasts':16,'benchmarks':4,'adjusted_models':8},
        'limits':['Hispanic broadly, not Mexican ancestry; parent variables include guardians.','Current English adult skill among observed BA holders, not institutional causal quality.','Small Hispanic cells; approximate intervals are not exact finite-sample NCES small-domain intervals.','Self/parents/guardians US-born does not establish G3 vs G4 or US-obtained degrees.']}
(ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='raw'},indent=2))
