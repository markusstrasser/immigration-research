"""Independent full-dummy FWL check of all32 adjusted peer models.

Only reads producer inputs. Saves verification evidence under --out. Requires
numpy/pandas/pyarrow, no producer import or hard-coded expected coefficients.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

def require(condition,message):
    if not condition:
        raise ValueError(message)

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--data-dir',type=Path,required=True)
p.add_argument('--results',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--source-lock',type=Path)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
raw=a.data_dir/'selected.parquet'
d=pd.read_parquet(raw)
expected=json.loads(a.results.read_text())
manifest=json.loads((a.data_dir/'probe.json').read_text())
h=hashlib.sha256(raw.read_bytes()).hexdigest()
require(expected['selected_sha256']==manifest['selected_sha256']==h,'Selected-data hash mismatch')
require(expected['source_sha256']==manifest['data_sha256'],'Original-source hash mismatch')
require(len(d)==manifest['rows'] and not d.CHILDID.duplicated().any(),'Invalid row count or duplicate IDs')
if a.source_lock is not None:
    lock=json.loads(a.source_lock.read_text())
    for field in ['data_sha256','dictionary_sha256','data_bytes']:
        require(manifest[field]==lock[field],'Source-lock mismatch: '+field)
exposures=['anyell','ell10pp','nonwhite10pp','allwhite']
expected_keys={(period,f'{domain}{ep}',f'{exposure}{wave}',spec)
    for period,wave,ep in [('kindergarten',1,2),('spring_2000_followup',4,4)]
    for domain in ['reading','math'] for exposure in exposures
    for spec in ['baseline','school_fe']}
model_index={}
for row in expected['models']:
    if row['specification'] not in ['baseline','school_fe']:
        continue
    key=tuple(row[k] for k in ['period','outcome','exposure','specification'])
    require(key not in model_index,'Duplicate expected model: '+str(key))
    model_index[key]=row
require(set(model_index)==expected_keys and len(model_index)==32,'Expected-model coverage mismatch')

def nonnegative(c):
    s=pd.to_numeric(d[c],errors='raise')
    return s.where(s>=0)

def counts(other,lep,count):
    c=pd.Series(np.nan,index=d.index)
    yes=(d[lep]==1)&(d[count]>=0)
    c.loc[yes]=d.loc[yes,count]
    require(not ((d[other]==2)&(d[lep]==1)).any(),'Contradictory language gates')
    require(not (((d[other]==2)|(d[lep]==2))&(d[count]>0)).any(),'Count contradicts zero gate')
    c.loc[(d[other]==2)|(d[lep]==2)]=0
    return c

for w in [1,4]:
    size=nonnegative(f'A{w}TOTRA');white=nonnegative(f'A{w}WHITE')
    n=counts('A1OTLAN','A1LEP','A1NUMLE') if w==1 else counts('A4OTLA','A4LEP','A4NUMLE')
    if w==4:
        k=d.A4CLASS.isin([1,2,3]);nk=d.A4CLASS==4
        n=n.where(nk);size=size.where(nk);white=white.where(nk)
        n.loc[k]=counts('A4KOTLA','A4KLEP','A4KNUML')[k]
        size.loc[k]=nonnegative('A4KTOTR')[k]
        white.loc[k]=nonnegative('A4KWHIT')[k]
    class_ok=size.between(5,45)&~(white>size)
    ell_ok=class_ok&n.notna()&(n<=size)
    race_ok=class_ok&white.notna()
    d[f'anyell{w}']=np.where(ell_ok,(n>0).astype(float),np.nan)
    d[f'ell10pp{w}']=(10*n/size).where(ell_ok)
    d[f'nonwhite10pp{w}']=(10*(1-white/size)).where(race_ok)
    d[f'allwhite{w}']=pd.Series((white==size).astype(float),index=d.index).where(race_ok)
    s=d[f'S{w}_ID'].astype(str)
    d[f'school{w}']=s.where(s.str.fullmatch(r'\d{4}')&~s.str.startswith('999'))
for domain,suffix in [('reading','RSCL'),('math','MSCL')]:
    for w in [1,2,4]:
        v=nonnegative(f'C{w}R4{suffix}');wc=f'C{w}WEIGHT'
        ok=v.notna()&(d[wc]>0)
        mean=np.average(v[ok],weights=d.loc[ok,wc])
        sd=np.sqrt(np.average((v[ok]-mean)**2,weights=d.loc[ok,wc]))
        require(np.isfinite(sd) and sd>0,'Invalid scale')
        require(np.isclose(sd,expected['scales'][f'{domain}{w}']['sd'],rtol=1e-12,atol=1e-12),'Scale mismatch')
        d[f'{domain}{w}']=(v-mean)/sd
        for power in [2,3]:
            d[f'{domain}{w}_{power}']=d[f'{domain}{w}']**power
d['ses']=d.WKSESL.where(d.WKSESL>-8)
d['female']=d.GENDER.map({1:0,2:1})
d['age1']=nonnegative('R1_KAGE')/12
for c,start,end,upper in [('duration_k','R1_KAGE','R2_KAGE',1),('duration_g1','R2_KAGE','R4AGE',2)]:
    duration=(nonnegative(end)-nonnegative(start))/12
    d[c]=duration.where(duration.between(0,upper,inclusive='neither'))
target=d[(d.RACE==1)&(d.P2CHPLAC==1)&(d.WKLANGST==2)]
base1=[f'{dom}1{post}' for dom in ['reading','math'] for post in ['', '_2','_3']]
base2=[f'{dom}2{post}' for dom in ['reading','math'] for post in ['', '_2','_3']]
rows=[]
seen=set()
for label,w,ep,wc,sc,duration,base in [
    ('kindergarten',1,2,'BYCOMW0','school1','duration_k',base1),
    ('spring_2000_followup',4,4,'Y2COMW0','school4','duration_g1',base2+base1)]:
    cov=['ses','female','age1']+base+[duration]
    for domain in ['reading','math']:
        yname=f'{domain}{ep}'
        for exposure in exposures:
            tname=f'{exposure}{w}'
            sample=target.dropna(subset=[yname,tname,wc,sc]+cov)
            sample=sample[sample[wc]>0]
            sample=sample[sample.groupby(sc)[sc].transform('size')>1]
            yy=sample[yname].to_numpy(float);tt=sample[tname].to_numpy(float)
            weights=sample[wc].to_numpy(float,copy=True);weights/=weights.mean();rw=np.sqrt(weights)
            g,levels=pd.factorize(sample[sc],sort=True);G=len(levels);N=len(sample)
            require(N>100 and G>20,'Insufficient sample')
            for spec,fixed in [('baseline',False),('school_fe',True)]:
                z=np.column_stack([sample[cov].to_numpy(float),np.eye(G)[g] if fixed else np.ones((N,1))])
                zw=z*rw[:,None];yt=np.column_stack([yy,tt])*rw[:,None]
                gamma,_,rank,_=np.linalg.lstsq(zw,yt,rcond=None)
                require(rank==zw.shape[1] and N>rank+1,'Invalid design rank or degrees of freedom')
                rr=yt-zw@gamma;ry,rt=rr[:,0],rr[:,1]
                den=np.dot(rt,rt)
                require(np.isfinite(den) and den>0,'No residual exposure variation')
                beta=np.dot(rt,ry)/den
                score=np.bincount(g,weights=rt*(ry-beta*rt),minlength=G)
                correction=G/(G-1)*(N-1)/(N-rank-1)
                se=np.sqrt(np.dot(score,score)/den**2*correction)
                key=(label,yname,tname,spec)
                require(key not in seen,'Duplicate verified model');seen.add(key)
                e=model_index[key]
                require(N==e['n'] and G==e['schools'],'Sample mismatch: '+str(key))
                require(np.isfinite(beta) and np.isfinite(se),'Nonfinite estimate')
                require(abs(beta-e['beta'])<1e-10,'Coefficient mismatch: '+str(key))
                require(abs(se-e['se_school_cr1'])<1e-10,'SE mismatch: '+str(key))
                row=dict(period=label,outcome=yname,exposure=tname,specification=spec,n=N,schools=G,beta=beta,se=se,
                    beta_difference=beta-e['beta'],se_difference=se-e['se_school_cr1'],
                    class_forms={str(k):int(v) for k,v in sample.A4CLASS.value_counts().items()},
                    teacher_reported_grades={str(k):int(v) for k,v in sample.T4GLVL.value_counts().items()} if 'T4GLVL' in sample else {})
                rows.append(row)
require(len(rows)==32 and seen==expected_keys,'Incomplete model verification')
output=dict(status='PASS',verified_models=len(rows),method='Independent exposures; full school dummies and weighted FWL',
    selected_sha256=h,results_sha256=hashlib.sha256(a.results.read_bytes()).hexdigest(),
    source_lock_sha256=hashlib.sha256(a.source_lock.read_bytes()).hexdigest() if a.source_lock else None,models=rows)
(a.out/'final_verification.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
pd.DataFrame(rows).to_csv(a.out/'final_verification.csv',index=False)
print(json.dumps({'status':'PASS','verified_models':len(rows),
    'max_beta_difference':max(abs(r['beta_difference']) for r in rows),
    'max_se_difference':max(abs(r['se_difference']) for r in rows),
    'allwhite_math':[r for r in rows if r['period']=='spring_2000_followup' and r['outcome']=='math4' and r['exposure']=='allwhite4']},indent=2))
