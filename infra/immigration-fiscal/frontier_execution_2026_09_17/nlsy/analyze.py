"""Public NLSY97 descendant descriptions, survey-linearized contrasts and sensitivities."""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "build"))
import paths as _data_paths

import argparse,hashlib,json,re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm,t

P=argparse.ArgumentParser();P.add_argument('--lane-dir',type=Path,default=Path(__file__).resolve().parents[2]/'new_datasets_2026_09_17');P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy');P.add_argument('--profile-dir',type=Path,default=_data_paths.reused_surveys_root(require_exists=False) / 'nlsy/profile_outcomes');A=P.parse_args();O=A.output_dir
paths={'family':A.lane_dir/'derived/nlsy_family/family_analysis_rows.csv','base':A.lane_dir/'derived/nlsy/full_selected_data.csv','new':O/'selected.csv','adult':A.profile_dir/'source_extract.parquet'}
d=pd.read_csv(paths['family']).set_index('R0000100').sort_index()
for key in ['base','new']:
    z=pd.read_csv(paths[key]).set_index('R0000100').sort_index();assert d.index.equals(z.index)
    for c in set(d)&set(z):assert d[c].equals(z[c]),f'{key}:{c} mismatch'
    d=d.join(z.drop(columns=list(set(d)&set(z)))).copy()
adult=pd.read_parquet(paths['adult']).set_index('caseid').sort_index();assert d.index.equals(adult.index)
for src,col in [('T8129600','degree'),('T8135900','weight_2013'),('T8976500','wage_receipt'),('T8976700','wage_amount')]:assert d[src].equals(adult[col]),src
assert len(d)==8984 and d.index.is_unique
audit={'rows':len(d),'adult_overlap_verified':['degree','weight_2013','wage_receipt','wage_amount']}
d['wbase']=d.R1236101/100;d['w2013']=d.T8135900/100;d['w2023']=d.U6365400/100
d['stratum']=d.R1489700;d['psu']=d.R1489800
design=pd.MultiIndex.from_frame(d[['stratum','psu']]);grid=design.unique().sort_values();counts=pd.Series(1,index=grid).groupby(level=0).sum();assert counts.eq(2).all();df=int(counts.sum()-len(counts));critical=float(t.ppf(.975,df))
audit['design']={'strata':len(counts),'pseudo_psus':len(grid),'degrees_freedom':df,'method':'Taylor linearized weighted domain ratios, with-replacement ultimate-cluster approximation; full sample design grid retained; no finite population correction'}

def variance(u):
    totals=pd.Series(np.asarray(u),index=design).groupby(level=[0,1]).sum().reindex(grid,fill_value=0)
    centered=totals-totals.groupby(level=0).transform('mean')
    return float(2*centered.pow(2).sum())

def estimate(y,w,mask):
    valid=mask & y.notna() & w.gt(0);wt=w.where(valid,0);total=wt.sum();n=int(valid.sum())
    if not total:return {'n':0,'mean':np.nan,'se':np.nan,'low':np.nan,'high':np.nan,'neff':0,'events':np.nan},np.zeros(len(d))
    mu=float((wt*y.fillna(0)).sum()/total);u=(wt*(y.fillna(0)-mu)/total).to_numpy();se=variance(u)**.5
    result={'n':n,'mean':mu,'se':se,'low':mu-critical*se,'high':mu+critical*se,'neff':float(total**2/wt.pow(2).sum()),'events':int(y[valid].sum()) if y[valid].isin([0,1]).all() else np.nan,'domain_psus':len(design[valid].unique()),'domain_strata':d.loc[valid,'stratum'].nunique()}
    return result,u

d['afqt_percentile']=d.R9829600.where(d.R9829600.ge(0))/1000
benchmark,u=estimate(d.afqt_percentile,d.wbase,pd.Series(True,index=d.index))
audit['official_afqt_benchmark']={'published_mean':50.410,'published_se':.638,'published_n':7093,'observed':benchmark}
assert benchmark['n']==7093 and abs(benchmark['mean']-50.410)<.0006 and abs(benchmark['se']-.638)<.0006,'Official principal variance benchmark failed'
refs=d.comparison.eq('Baseline_NH_White_not_Mexican_self_ID')&d.linked_exact.str.startswith('G4plus')
refvalid=refs&d.afqt_percentile.notna();refw=d.loc[refvalid,'wbase'];refscore=d.loc[refvalid,'afqt_percentile'];refmu=np.average(refscore,weights=refw);refsd=np.sqrt(np.average((refscore-refmu)**2,weights=refw))
d['afqt_percentile_white_G4_SD']=(d.afqt_percentile-refmu)/refsd
scores=d[d.afqt_percentile.notna()].groupby('afqt_percentile').wbase.sum().sort_index();mid=(scores.cumsum()-.5*scores)/scores.sum();rankmap=pd.Series(norm.ppf(mid),index=scores.index)
d['afqt_weighted_rank_normal']=d.afqt_percentile.map(rankmap)
audit['score_reference']={'white_G4_n':int(refvalid.sum()),'white_G4_percentile_mean':float(refmu),'white_G4_percentile_sd':float(refsd),'rank_normal':'normal inverse CDF of individual weighted empirical midranks among all7093 score respondents; not raw AFQT/IQ SD; reference distribution treated fixed in descriptive SE'}
degree=d.T8129600.where(d.T8129600.between(0,7))
d['BAplus_2013']=degree.ge(4).astype(float).where(degree.notna());d['regular_HSplus_2013']=degree.ge(2).astype(float).where(degree.notna());d['GED_or_HSplus_2013']=degree.ge(1).astype(float).where(degree.notna())
d['wage2012_receipt']=d.T8976500.where(d.T8976500.isin([0,1]))
d['wage2012_known_including_zero']=d.T8976700.where(d.T8976700.ge(0));d.loc[d.T8976500.eq(0),'wage2012_known_including_zero']=0
d['log_positive_wage2012']=np.log(d.T8976700.where(d.T8976700.gt(0)))
d['arrest_ever_reported']=d.arrest;d['incarc_ever_reported']=d.incarceration
d['incarc_ever_exclude_incomplete']=d.incarceration.where(d.E8043601.ne(1))
cb=json.loads((O/'selected_codebook.json').read_text());monthly={}
for k,block in cb.items():
    m=re.search(r'\[((?:ARREST|INCARC)_STATUS)_(\d{4})\.(\d{2})\]',block[:100])
    if m:monthly[(m[1],int(m[2]),int(m[3]))]=k
for prefix,name in [('ARREST_STATUS','arrest_age12_before30'),('INCARC_STATUS','incarc_age12_before30')]:
    vals=[]
    for _,r in d.iterrows():
        by,bm=r.R0536402,r.R0536401
        if not (1980<=by<=1984 and 1<=bm<=12):vals.append(np.nan);continue
        yr=int(by+30-(bm==1));mo=int(12 if bm==1 else bm-1);value=r[monthly[(prefix,yr,mo)]]
        if prefix=='ARREST_STATUS':
            valid=0<=value<=99
            # An undated arrest cannot be assigned to a side of the age cutoff.
            if value==0 and r.E8033300<r.E8033100:valid=False
        else:valid=value in (0,1,99)
        vals.append(float(value>0) if valid else np.nan)
    d[name]=vals
# The first-event summaries provide an independent chronology check on array zeros.
# Pre-age-12 events are outside this estimand; contradictory post-age-12 histories stay unknown.
cutoff=(d.R0536402+30-d.R0536401.eq(1))*100+d.R0536401.sub(1).replace({0:12})
twelfth=(d.R0536402+12)*100+d.R0536401
timing_audit={}
for first,name in [('E8043000','incarc_age12_before30'),('E8033000','arrest_age12_before30')]:
    contradiction=d[first].ge(twelfth)&d[first].le(cutoff)&d[name].eq(0)
    pre12=d[first].gt(0)&d[first].lt(twelfth)&d[name].eq(0)
    timing_audit[name]={'contradictory_post12_first_date_array_zero_excluded':int(contradiction.sum()),'excluded_Mexican_self_ID':int((contradiction&d.comparison.eq('Mexican_Chicano_self_ID')).sum()),'first_date_before12_array_zero_expected':int(pre12.sum())}
    d.loc[contradiction,name]=np.nan
# E80430 invalid skip (-3) does not establish that no event occurred before 30.
# Valid skip (-4) is the no-incarceration route and must remain distinguishable.
undated_zero=d.E8043000.eq(-3)&d.incarc_age12_before30.eq(0)
timing_audit['incarc_age12_before30']['invalid_first_date_array_zero_excluded']=int(undated_zero.sum())
timing_audit['incarc_age12_before30']['invalid_first_date_positive_weight_excluded']=int((undated_zero&d.w2023.gt(0)).sum())
timing_audit['incarc_age12_before30']['invalid_first_date_excluded_by_identity']=d.loc[undated_zero,'comparison'].value_counts().to_dict()
d.loc[undated_zero,'incarc_age12_before30']=np.nan
audit['timing_crosscheck']=timing_audit
(O/'timing_crosscheck.json').write_text(json.dumps(timing_audit,indent=2))
d['incarc_age12_before30_exclude_incomplete']=d.incarc_age12_before30.where(d.E8043601.ne(1))
d['detail']=d.linked_exact
g2=d.linked_exact.str.startswith('G2')
d.loc[g2&d.mother_us.eq(0)&d.father_us.eq(0),'detail']='G2_two_foreign_born_parents'
d.loc[g2&((d.mother_us.eq(0)&d.father_us.eq(1))|(d.mother_us.eq(1)&d.father_us.eq(0))),'detail']='G2_one_foreign_one_US_parent'
d.loc[g2&(d.mother_us.isna()|d.father_us.isna()),'detail']='G2_foreign_parent_other_unknown'
metrics={k:'wbase' for k in ['afqt_percentile','afqt_percentile_white_G4_SD','afqt_weighted_rank_normal']}
metrics.update({k:'w2013' for k in ['BAplus_2013','regular_HSplus_2013','GED_or_HSplus_2013','wage2012_receipt','wage2012_known_including_zero','log_positive_wage2012']})
metrics.update({k:'w2023' for k in ['arrest_ever_reported','incarc_ever_reported','incarc_ever_exclude_incomplete','arrest_age12_before30','incarc_age12_before30','incarc_age12_before30_exclude_incomplete']})
means=[];contrasts=[];allmask=pd.Series(True,index=d.index)
for sex in ['All','Men','Women']:
    sm=allmask if sex=='All' else d.sex.eq(sex)
    for variant in ['linked_exact','detail']:
        for identity in d.comparison.unique():
            for group in d[variant].unique():
                mask=sm&d.comparison.eq(identity)&d[variant].eq(group)
                if not mask.any():continue
                for metric,wcol in metrics.items():
                    e,u=estimate(d[metric],d[wcol],mask)
                    means.append({'sex':sex,'comparison':identity,'variant':variant,'group':group,'metric':metric,'weight':wcol,'baseline_group_n':int(mask.sum()),'weight_positive_n':int((mask&d[wcol].gt(0)).sum()),**e})
    mx=d.comparison.eq('Mexican_Chicano_self_ID');groups={tag:d.linked_exact.str.startswith(tag) for tag in ['G2','G3_','G4plus']};groups['whiteG4']=refs
    for high,low in [('G3_','G2'),('G4plus','G3_'),('G2','whiteG4'),('G3_','whiteG4'),('G4plus','whiteG4')]:
        hm=sm&groups[high]&(allmask if high=='whiteG4' else mx);lm=sm&groups[low]&(allmask if low=='whiteG4' else mx)
        for metric,wcol in metrics.items():
            eh,uh=estimate(d[metric],d[wcol],hm);el,ul=estimate(d[metric],d[wcol],lm)
            delta=eh['mean']-el['mean'];se=variance(uh-ul)**.5
            contrasts.append({'sex':sex,'high':high,'low':low,'metric':metric,'n_high':eh['n'],'n_low':el['n'],'difference':delta,'design_se':se,'low95':delta-critical*se,'high95':delta+critical*se,'p_two_sided':2*t.sf(abs(delta/se),df) if se else np.nan})
    for metric,wcol in metrics.items():
        eh,uh=estimate(d[metric],d[wcol],sm&mx&d.detail.eq('G2_one_foreign_one_US_parent'))
        el,ul=estimate(d[metric],d[wcol],sm&mx&d.detail.eq('G2_two_foreign_born_parents'))
        delta=eh['mean']-el['mean'];se=variance(uh-ul)**.5
        contrasts.append({'sex':sex,'high':'G2_one_foreign_one_US_parent','low':'G2_two_foreign_born_parents','metric':metric,'n_high':eh['n'],'n_low':el['n'],'difference':delta,'design_se':se,'low95':delta-critical*se,'high95':delta+critical*se,'p_two_sided':2*t.sf(abs(delta/se),df) if se else np.nan})
pd.DataFrame(means).to_csv(O/'means.csv',index=False);pd.DataFrame(contrasts).to_csv(O/'contrasts.csv',index=False)

# Sensitivity to source definitions and the known-US-parent/unknown-grandparent pool.
classification=[]
for sex in ['All','Men','Women']:
    sm=allmask if sex=='All' else d.sex.eq(sex)
    mx=d.comparison.eq('Mexican_Chicano_self_ID')
    scenarios={k:d[k] for k in ['linked_exact','roster_only_exact','parent_roster_exact','supplemental_exact']}
    gpunknown=d.linked_exact.eq('USborn_USparents_grandparents_unresolved')
    for target in ['G3_','G4plus']:
        labels=d.linked_exact.copy();labels.loc[gpunknown]=target;scenarios['all_GP_unknown_assigned_'+target]=labels
    for scenario,labels in scenarios.items():
        for metric,wcol in metrics.items():
            eh,uh=estimate(d[metric],d[wcol],sm&mx&labels.str.startswith('G4plus'))
            el,ul=estimate(d[metric],d[wcol],sm&mx&labels.str.startswith('G3_'))
            delta=eh['mean']-el['mean'];se=variance(uh-ul)**.5
            classification.append({'sex':sex,'scenario':scenario,'metric':metric,'n_G3':el['n'],'n_G4plus':eh['n'],'mean_G3':el['mean'],'mean_G4plus':eh['mean'],'G4minusG3':delta,'design_se':se,'low95':delta-critical*se,'high95':delta+critical*se})
pd.DataFrame(classification).to_csv(O/'classification_sensitivity.csv',index=False)
classification_tips=[]
for sex in ['All','Men','Women']:
    sm=allmask if sex=='All' else d.sex.eq(sex)
    mx=d.comparison.eq('Mexican_Chicano_self_ID')
    for metric,wcol in metrics.items():
        valid=sm&mx&d[metric].notna()&d[wcol].gt(0)
        sums=[]
        for group in ['G3_','G4plus','USborn_USparents_grandparents_unresolved']:
            mask=valid&d.linked_exact.str.startswith(group)
            sums.append((float((d.loc[mask,wcol]*d.loc[mask,metric]).sum()),float(d.loc[mask,wcol].sum())))
        (a3,b3),(a4,b4),(c,b)=sums
        f0=(a4+c)*b3-a3*(b4+b);f1=a4*(b3+b)-(a3+c)*b4
        q=f0/(f0-f1) if f0!=f1 else np.nan
        classification_tips.append({'sex':sex,'metric':metric,'GP_unknown_fraction_assigned_G3_for_equal_means':q,'feasible_0_1':0<=q<=1,'assumption':'Allocate remaining GP-unknown pool to G4plus; same fraction q of every pool outcome/weight assigned G3, a sensitivity scenario not estimated lineage'})
pd.DataFrame(classification_tips).to_csv(O/'classification_tipping_points.csv',index=False)

# Finite baseline-weight completion bounds, conditional on observed family classification.
bounds=[]
for sex in ['All','Men','Women']:
    sm=allmask if sex=='All' else d.sex.eq(sex)
    for group in d.linked_exact.unique():
        mask=sm&d.comparison.eq('Mexican_Chicano_self_ID')&d.linked_exact.eq(group)
        for metric in ['incarc_ever_reported','incarc_age12_before30','BAplus_2013','regular_HSplus_2013']:
            w=d.wbase.where(mask,0);obs=mask&d[metrics[metric]].gt(0)&d[metric].notna();total=w.sum()
            if not total:continue
            observed_weight=w[obs].sum();events=(w[obs]*d.loc[obs,metric]).sum();low=events/total;missing=1-observed_weight/total
            bounds.append({'sex':sex,'group':group,'metric':metric,'baseline_n':int(mask.sum()),'observed_n':int(obs.sum()),'observed_baseline_weight_rate':events/observed_weight if observed_weight else np.nan,'lower':low,'upper':low+missing,'missing_weight_fraction':missing})
bd=pd.DataFrame(bounds);bd.to_csv(O/'completion_bounds.csv',index=False)
tips=[]
for sex in ['All','Men','Women']:
    for metric in ['incarc_ever_reported','incarc_age12_before30','BAplus_2013','regular_HSplus_2013']:
        z=bd[(bd.sex==sex)&(bd.metric==metric)];g3=z[z.group.str.startswith('G3_')].iloc[0];g4=z[z.group.str.startswith('G4plus')].iloc[0]
        for q3 in [0,.1,.2,.3,.5,1]:
            q4=(g3.lower+g3.missing_weight_fraction*q3-g4.lower)/g4.missing_weight_fraction
            tips.append({'sex':sex,'metric':metric,'assumed_missing_G3_rate':q3,'missing_G4_rate_for_equal_completed_means':q4,'feasible_0_1':0<=q4<=1})
pd.DataFrame(tips).to_csv(O/'retention_tipping_points.csv',index=False)
d[['comparison','sex','linked_exact','detail','mother_us','father_us','stratum','psu','wbase','w2013','w2023','E8043000',*metrics]].to_csv(O/'analysis_rows.csv')
audit['identity_score_selection']=d.groupby('comparison').apply(lambda x:pd.Series({'baseline_n':len(x),'valid_AFQT_n':x.afqt_percentile.notna().sum()}),include_groups=False).astype(int).to_dict('index')
audit['source_hashes']={k:{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for k,path in paths.items()}
audit['sources']=['https://pmc.ncbi.nlm.nih.gov/articles/PMC10836839/','https://www.nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects','https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/administration-cat-asvab','https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/crime/crime-delinquency-arrest']
audit['limitations']=['Self-ID plus generic birthplace cannot reproduce restricted Mexico-country ancestry','No parental DNA or fractions measured','SE accounts public design but not nonresponse bias or family-history misclassification','Rank transform and white reference distribution held fixed for descriptive SE','Common age array starts age12 and can contain imputed dates; undated arrests excluded when no dated prior event','No multiple-comparison confirmation claim','2012 job wages omit self-employment; top2percent assigned group mean; missing amounts not zero except known nonreceipt']
(O/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2),flush=True)
