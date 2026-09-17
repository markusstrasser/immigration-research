#!/usr/bin/env python3
"""Held CPS/GSS analysis. Raw sources read only; all products in --output-dir."""
import argparse, hashlib, json, math, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

P=argparse.ArgumentParser()
P.add_argument('--repo',type=Path,default=Path('/Users/alien/Projects/immigration-research'))
P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/social')
P.add_argument('--part',choices=['cps','gss','all'],default='all')
A=P.parse_args(); R=A.repo; O=A.output_dir; O.mkdir(parents=True,exist_ok=True)
REPS=[f'pwwgt{i}' for i in range(161)]
def se(e):return float(np.sqrt(4/160*np.square(e[1:]-e[0]).sum()))
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def groups(d):
    native=d.PRCITSHP.isin([1,2,3]); pu=d.PEFNTVTY.isin([57,60,66,69,73,78])&d.PEMNTVTY.isin([57,60,66,69,73,78])
    pm=d.PEFNTVTY.eq(303).astype(int)+d.PEMNTVTY.eq(303).astype(int)
    return {'white_g3':native&pu&d.PEHSPNON.eq(2)&d.PRDTRACE.eq(1),'mex_g2':native&pm.gt(0),'mex_g3_selfid':native&pu&d.PRDTHSP.eq(1),'mex_born':d.PRCITSHP.isin([4,5])&d.PENATVTY.eq(303),'mex_g2_one':native&pm.eq(1),'mex_g2_two':native&pm.eq(2)}
def cps():
    paths={2024:R/'sources/immigration-fiscal/data/census/cps_asec_2024_march.zip',2025:R/'infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip',2026:R/'infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip'}
    cols=['PH_SEQ','PPPOS','PERIDNUM','A_LINENO','A_SEX','A_AGE','PRPERTYP','PRCITSHP','PENATVTY','PEFNTVTY','PEMNTVTY','PEHSPNON','PRDTRACE','PRDTHSP','MARSUPWT','PRDISFLG','SS_YN','SS_VAL','RESNSS1','RESNSS2','SSI_YN','SSI_VAL','DIS_YN','DIS_VAL1','DIS_VAL2','DIS_SC1','DIS_SC2']
    ds={}; audit={'sources':{},'join_gates':{},'overlap':[]}
    for y,p in paths.items():
        with zipfile.ZipFile(p) as z:
            d=pd.read_csv(z.open(f'pppub{y%100}.csv'),usecols=cols,dtype={'PERIDNUM':str})
            w=pd.read_csv(z.open(f'asec_csv_repwgt_{y}.csv')).rename(columns={'h_seq':'PH_SEQ'})
        d=d.merge(w,on=['PH_SEQ','PPPOS'],validate='one_to_one',how='left')
        assert d[REPS].notna().all().all()
        assert np.max(abs(d.MARSUPWT/100-d.pwwgt0))<.01
        assert d.PERIDNUM.is_unique and d.PERIDNUM.str.len().eq(22).all()
        assert d.DIS_SC1.between(0,10).all() and d.DIS_SC2.between(0,10).all()
        if y==2025:assert len(d)==142125
        if y==2026:assert len(d)==134729
        ds[y]=d
        audit['sources'][str(y)]={'path':str(p),'sha256':digest(p)}
        audit['join_gates'][str(y)]={'n':len(d),'weight_sum':float(d.pwwgt0.sum()),'person_ids_unique':True,'weight_match_max':float(abs(d.MARSUPWT/100-d.pwwgt0).max())}
    for y,z in [(2024,2025),(2025,2026),(2024,2026)]:
        m=ds[y][['PERIDNUM','A_AGE','A_SEX']].merge(ds[z][['PERIDNUM','A_AGE','A_SEX']],on='PERIDNUM',suffixes=('_a','_b'),validate='one_to_one')
        ok=m.A_SEX_a.eq(m.A_SEX_b)&(m.A_AGE_b-m.A_AGE_a).between(z-y-1,z-y+1)
        audit['overlap'].append({'years':[y,z],'same_id_n':len(m),'demographically_consistent_n':int(ok.sum()),'warning':'ID consistency diagnoses overlap; not validated longitudinal weights or cross-year replicate alignment.'})
    d=ds[2025]; g=groups(d); ref=d.A_AGE.between(25,64)&d.PRPERTYP.eq(2)&d.PRDISFLG.isin([1,2])&g['white_g3']
    targets={}
    for name,s in [('all',ref),('male',ref&d.A_SEX.eq(1)),('female',ref&d.A_SEX.eq(2))]:
        hist=np.bincount(((d.loc[s,'A_AGE']-25)//5).astype(int),weights=d.loc[s,'pwwgt0'],minlength=8)
        targets[name]=hist/hist.sum()
    audit['fixed_2025_age_targets']={k:v.tolist() for k,v in targets.items()}
    annual=[]; vectors={}; checks=[]
    for year,d in ds.items():
        W=d[REPS].to_numpy(float); gg=groups(d); adult=d.A_AGE.between(25,64)&d.PRPERTYP.eq(2)&d.PRDISFLG.isin([1,2]); band=((d.A_AGE.to_numpy()-25)//5).clip(0,7)
        dis=d.PRDISFLG.eq(1).to_numpy(float)
        ss=d.SS_YN.eq(1)&(d.RESNSS1.eq(2)|d.RESNSS2.eq(2)); si=d.SSI_YN.eq(1)
        ssv=np.where(ss,d.SS_VAL,0); siv=np.where(si,d.SSI_VAL,0)
        other={key:np.zeros(len(d)) for key in ['coded_government','private','mixed_unknown']}
        for i in [1,2]:
            sc=d[f'DIS_SC{i}']; val=d[f'DIS_VAL{i}'].to_numpy(float)
            for key,codes in [('coded_government',[3,4,5,6,9]),('private',[2,7]),('mixed_unknown',[1,8,10])]:other[key]+=np.where(sc.isin(codes),val,0)
        expected=np.where(d.DIS_YN.eq(1),d.DIS_VAL1+d.DIS_VAL2,0)
        assert np.allclose(sum(other.values()),expected)
        metrics={'disability':dis,'ss_disability_reason_receipt':ss.to_numpy(float),'ssi_receipt':si.to_numpy(float),'ss_disability_reason_dollars':ssv,'ssi_dollars':siv,'ss_disability_plus_ssi_dollars':ssv+siv,'other_coded_government_dollars':other['coded_government'],'private_disability_dollars':other['private'],'mixed_unknown_disability_dollars':other['mixed_unknown'],'all_disability_income_dollars':ssv+siv+expected}
        subgroups={'all':adult,'male':adult&d.A_SEX.eq(1),'female':adult&d.A_SEX.eq(2),'birth1965_1984':adult&(year-d.A_AGE).between(1965,1984),'birth1985_1999':adult&(year-d.A_AGE).between(1985,1999)}
        for subgroup,sm in subgroups.items():
            for group,gm in gg.items():
                idx=np.flatnonzero(sm&gm); ww=W[idx]; n=len(idx)
                if not n:continue
                for metric,y in metrics.items():
                    if subgroup!='all' and metric!='disability':continue
                    crude=y[idx]@ww/ww.sum(axis=0)
                    variants={'crude':crude}
                    if subgroup in targets:
                        by=[]
                        for b in range(8):
                            ii=idx[band[idx]==b]; den=W[ii].sum(axis=0)
                            assert np.all(den>0),f'Unusable age band {year} {subgroup} {group} {b}'
                            by.append(y[ii]@W[ii]/den)
                        variants['age_std_fixed2025white']=targets[subgroup]@np.asarray(by)
                    for standard,e in variants.items():
                        key=(subgroup,group,metric,standard); vectors[(year,)+key]=e
                        annual.append(dict(year=year,subgroup=subgroup,group=group,metric=metric,standard=standard,n=n,events=int(dis[idx].sum()) if metric=='disability' else None,estimate=e[0],se=se(e)))
        if year==2025:
            prior=pd.read_csv(R/'infra/immigration-fiscal/disability_gen_2026_09_17/disability_by_generation.csv')
            for group,old in [('white_g3','third_plus_nh_white'),('mex_g2','mexican_second_gen'),('mex_g3_selfid','mexican_third_plus_selfid'),('mex_born','mexico_born')]:
                p=prior[(prior.group==old)&(prior.metric=='prdisflg_any')&(prior.standardisation=='age_std_to_third_plus_nh_white')].iloc[0]
                e=vectors[(year,'all',group,'disability','age_std_fixed2025white')]
                assert abs(p.estimate-e[0])<1e-10 and abs(p.se-se(e))<1e-10
                checks.append({'group':group,'prior_estimate':float(p.estimate),'reproduced':e[0]})
    contrasts=[]
    pairs=[('mex_g2','mex_born'),('mex_g2','white_g3'),('mex_g3_selfid','white_g3'),('mex_g3_selfid','mex_g2'),('mex_g2_one','mex_g2_two')]
    for (year,sub,group,metric,std),e in list(vectors.items()):
        for left,right in pairs:
            if group!=left:continue
            key=(year,sub,right,metric,std)
            if key not in vectors:continue
            diff=e-vectors[key]; contrasts.append(dict(year=year,subgroup=sub,group=left+' minus '+right,metric=metric,standard=std,estimate=diff[0],se=se(diff)))
    annual=pd.DataFrame(annual); contrast=pd.DataFrame(contrasts)
    pooled=[]
    for kind,table in [('level',annual),('contrast',contrast)]:
        for keys,dd in table.groupby(['subgroup','group','metric','standard']):
            assert len(dd)==3
            ses=dd.se.to_numpy(); est=float(dd.estimate.mean()); upper=float(ses.mean()); lower=max(0,2*ses.max()-ses.sum())/3
            pooled.append(dict(kind=kind,subgroup=keys[0],group=keys[1],metric=keys[2],standard=keys[3],estimate=est,se_unknown_cov_lower=lower,se_unknown_cov_upper=upper,se_independence_diagnostic=float(np.sqrt((ses**2).sum())/3),ci95_conservative_lo=est-1.96*upper,ci95_conservative_hi=est+1.96*upper,n_years=3))
    annual.to_csv(O/'cps_annual.csv',index=False);contrast.to_csv(O/'cps_direct_contrasts.csv',index=False);pd.DataFrame(pooled).to_csv(O/'cps_equal_year_pool.csv',index=False)
    audit['prior_gate']=checks; audit['pool_definition']='Arithmetic mean of three annual estimates with fixed 2025 reference age distribution; original year-specific population weights, not harmonized population-control vintages. Money is nominal year-specific income (2023-25) and never interpreted as real growth.'
    audit['covariance']='Exact cross-year design covariance not established. SE upper=sum(s_year)/3 follows Cauchy-Schwarz for any joint covariance; independence SE diagnostic only. ID overlap does not license independent years or aligned replicate numbers.'
    (O/'cps_audit.json').write_text(json.dumps(audit,indent=2));print('CPS PASS',len(annual),len(contrast),len(pooled),flush=True)

def gss():
    raw=pd.read_pickle(O/'gss_selected.pkl');d=raw[raw.year>=2000].reset_index(drop=True).copy()
    residual=d[['year','trust']].copy()
    for c in d:d[c]=pd.to_numeric(d[c],errors='coerce')
    gen=np.full(len(d),np.nan);gen[d.born.eq(2)]=1;gen[d.born.eq(1)&d.parborn.isin([1,2,4,6,8])]=2;gen[d.born.eq(1)&d.parborn.eq(0)]=3
    groups=np.full(len(d),'other_or_unknown',dtype=object)
    for v in [1,2,3]:groups[d.hispanic.ge(2)&(gen==v)]=f'Hisp G{v}'
    groups[d.race.eq(1)&d.hispanic.eq(1)&(gen==3)]='White G3'
    groups[d.race.eq(1)&d.hispanic.eq(1)&np.isin(gen,[1,2])]='White G12'
    d['group']=groups
    assert d[['vstrat','vpsu','wtssps']].notna().all().all()
    # Full design retained; zero influence outside each outcome/analysis domain.
    design=d.groupby(['vstrat','vpsu']).size(); npsu=design.groupby(level=0).size();assert npsu.ge(2).all()
    cross=d.groupby('vstrat').year.nunique(); assert cross.max()==1,'Strata must be round-unique, as NORC documents.'
    def covariance(influence):
        s=pd.DataFrame(influence).groupby([d.vstrat,d.vpsu]).sum()
        answer=np.zeros((s.shape[1],s.shape[1]))
        for st,ss in s.groupby(level=0):
            a=ss.to_numpy();center=a-a.mean(axis=0);answer+=len(a)/(len(a)-1)*(center.T@center)
        return answer
    assert d.loc[d.year.ge(2004),'wtssnrps'].notna().all(), 'Unexpected missing recommended weight'
    weights={'prior_wtssps':d.wtssps.to_numpy(),'recommended_NR_where_available':d.wtssnrps.fillna(d.wtssps).to_numpy()}
    dist=[];contrasts=[];adjusted=[];resids=[]
    for mode,w in weights.items():
        assert np.isfinite(w).all() and (w>0).all()
        for group in ['White G3','Hisp G1','Hisp G2','Hisp G3','other_or_unknown']:
            mask=(d.group==group).to_numpy()
            if not mask.any():continue
            codes=residual.trust.fillna('system_missing').astype(str)
            for code in sorted(codes.unique()):
                sel=mask&(codes==code).to_numpy();resids.append(dict(weight=mode,group=group,code=code,n=int(sel.sum()),weighted_share_all=float(w[sel].sum()/w[mask].sum())))
        for denom,valid in [('definite',d.trust.isin([1,2]).to_numpy()),('three_responses',d.trust.isin([1,2,3]).to_numpy())]:
            ifs={}
            for group in ['White G3','Hisp G1','Hisp G2','Hisp G3']:
                mask=valid&(d.group==group).to_numpy();den=w[mask].sum()
                for code in ([1,2] if denom=='definite' else [1,2,3]):
                    y=d.trust.eq(code).to_numpy(float);est=float(y[mask]@w[mask]/den)
                    influence=np.where(mask,w*(y-est)/den,0);variance=covariance(influence[:,None])[0,0]
                    dist.append(dict(weight=mode,denominator=denom,group=group,code=code,n=int(mask.sum()),estimate=est,se_design=math.sqrt(variance)))
                    if code==1:ifs[group]=(est,influence)
            for group in ['Hisp G1','Hisp G2','Hisp G3']:
                est=ifs[group][0]-ifs['White G3'][0];v=covariance((ifs[group][1]-ifs['White G3'][1])[:,None])[0,0]
                contrasts.append(dict(weight=mode,denominator=denom,group=group,estimate=est,se_design=math.sqrt(v)))
            # Same age/education/year-adjusted estimand as prior, with proper stratum-centred meat.
            mask=valid&d.group.isin(['White G3','Hisp G1','Hisp G2','Hisp G3','White G12']).to_numpy()&d.age.notna().to_numpy()&d.educ.notna().to_numpy()
            ix=np.flatnonzero(mask);s=d.loc[mask]; ww=w[mask]; yy=s.trust.eq(1).to_numpy(float)
            names=['Intercept','Hisp G1','Hisp G2','Hisp G3','White G12','age','age2','educ']+[f'year{v}' for v in sorted(s.year.unique())[1:]]
            X=np.column_stack([np.ones(len(s))]+[(s.group==g).to_numpy(float) for g in names[1:5]]+[s.age.to_numpy()/50,(s.age.to_numpy()/50)**2,s.educ.to_numpy()/10]+[s.year.eq(v).to_numpy(float) for v in sorted(s.year.unique())[1:]])
            bread=np.linalg.inv(X.T@(ww[:,None]*X));beta=bread@(X.T@(ww*yy));err=yy-X@beta
            infl=np.zeros((len(d),len(beta)));infl[ix]=(ww[:,None]*X*err[:,None])@bread
            cov=covariance(infl)
            # Previous statsmodels cluster sandwich, finite sample correction, on same model rows.
            scores=pd.DataFrame(infl[ix]).groupby([s.year.reset_index(drop=True),s.vstrat.reset_index(drop=True),s.vpsu.reset_index(drop=True)]).sum().to_numpy()
            old=scores.T@scores*len(scores)/(len(scores)-1)*(len(s)-1)/(len(s)-len(beta))
            for j,g in enumerate(names[1:4],1):adjusted.append(dict(weight=mode,denominator=denom,group=g,n=len(s),estimate=beta[j],se_design=math.sqrt(cov[j,j]),se_old_cluster=math.sqrt(old[j,j])))
            for left,right in [(2,1),(3,1),(3,2)]:
                v=cov[left,left]+cov[right,right]-2*cov[left,right]
                ov=old[left,left]+old[right,right]-2*old[left,right]
                adjusted.append(dict(weight=mode,denominator=denom,group=names[left]+' minus '+names[right],n=len(s),estimate=beta[left]-beta[right],se_design=math.sqrt(max(0,v)),se_old_cluster=math.sqrt(max(0,ov))))
    distr=pd.DataFrame(dist);adj=pd.DataFrame(adjusted)
    for key,ss in distr.groupby(['weight','denominator','group']):assert abs(ss.estimate.sum()-1)<1e-12
    prior=pd.read_csv(R/'infra/immigration-fiscal/attitudes_gen_2026_09_16/gss_gen_adjusted.csv')
    for g,oldg in [('Hisp G1','Hisp G1'),('Hisp G2','Hisp G2'),('Hisp G3','Hisp G3+')]:
        row=adj[(adj.weight=='prior_wtssps')&(adj.denominator=='definite')&(adj.group==g)].iloc[0];p=prior[(prior.item=='trust_yes')&(prior.contrast==oldg)].iloc[0]
        assert abs(row.estimate-p.coef)<.000051 and abs(row.se_old_cluster-p.se)<.000051,(row.to_dict(),p.to_dict())
    distr.to_csv(O/'gss_trust_distribution.csv',index=False);pd.DataFrame(contrasts).to_csv(O/'gss_trust_contrasts.csv',index=False);adj.to_csv(O/'gss_trust_adjusted.csv',index=False);pd.DataFrame(resids).to_csv(O/'gss_trust_residuals.csv',index=False)
    audit={'n':len(d),'strata':len(npsu),'psus':int(npsu.sum()),'min_psus_per_stratum':int(npsu.min()),'strata_cross_year_max':int(cross.max()),'primary_labels':json.loads((O/'gss_labels.json').read_text())['labels']['trust'],'year_weights':d.groupby('year')[['wtssps','wtssnrps']].sum().to_dict(),'unknown_group_n':int((d.group=='other_or_unknown').sum()),'prior_gate':'Coefficients and old cluster SE reproduced to stored rounding','variance':'Taylor ratio/WLS linearization; all full-sample design PSUs retained; sum_h n_h/(n_h-1) sum_j (PSU influence - stratum mean)^2; no invented design degrees of freedom; normal approximation for reported intervals.'}
    (O/'gss_audit.json').write_text(json.dumps(audit,indent=2));print('GSS PASS',len(dist),len(adjusted),flush=True)
if A.part in ['cps','all']:cps()
if A.part in ['gss','all']:gss()
