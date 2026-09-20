"""Full-frame design estimates and distinct historical/cohort comparators."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import pyreadstat
from scipy.stats import t
from estimate import Design as SurveyDesign

ROOT=Path(__file__).resolve().parents[3]
INFRA=ROOT/'infra/immigration-fiscal'
BASE=INFRA/'new_datasets_2026_09_17/derived'
OUT=Path(__file__).resolve().parent/'derived/historical'
OUT.mkdir(parents=True, exist_ok=True)
audit={'sources':[], 'method':'Full-frame with-replacement Taylor ratio linearization; no finite population correction; fullframe and occupied-domain PSU-minus-strata critical-value sensitivities'}
results=[]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

class Design:
    def __init__(self,d):
        assert d[['stratum','psu']].notna().all().all()
        self.frame=d
        self.keys=pd.MultiIndex.from_frame(d[['stratum','psu']])
        self.grid=self.keys.unique().sort_values()
        self.count=pd.Series(1,index=self.grid).groupby(level=0).sum()
        assert self.count.ge(2).all()
        self.df=len(self.grid)-len(self.count)
        # Reuse the established variance engine. Unit placeholder weights only
        # retain all design cells; actual outcome weights enter the influence.
        frame=d.assign(vstrat=d.stratum, vpsu=d.psu, w=1., year=d.get('year',2023))
        self.engine=SurveyDesign(frame)
    def variance(self,u):
        return float(self.engine.cov(np.asarray(u)[:,None])[0,0])
    def ratio(self,num,den,w):
        num,den,w=map(lambda x:np.asarray(x,float),(num,den,w))
        assert np.isfinite(w).all() and (w>=0).all()
        assert (num>=0).all() and (num<=den).all()
        total=w@den
        assert total>0
        point=float(w@num/total)
        influence=w*(num-point*den)/total
        se=np.sqrt(self.variance(influence))
        active=(den>0)&(w>0)
        support=self.frame.loc[active,['stratum','psu']].drop_duplicates()
        domain_df=len(support)-support.stratum.nunique()
        status='insufficient_domain_df' if domain_df<1 else 'degenerate_zero_variance' if se==0 else 'linearized_approximation'
        row={'point':point,'se':se,'n':int(active.sum()),'events':int(((num>0)&(w>0)).sum()),'weight_denom':float(total),'fullframe_df':self.df,'domain_df':domain_df,'domain_psus':len(support),'domain_strata':support.stratum.nunique(),'status':status}
        for tag,df in [('fullframe',self.df),('domain',domain_df)]:
            crit=t.ppf(.975,df) if df>0 else np.nan
            row[f'ci95_{tag}_lo']=point-crit*se
            row[f'ci95_{tag}_hi']=point+crit*se
        return row

paths={'family':BASE/'nlsy_family/family_analysis_rows.csv','base':BASE/'nlsy/full_selected_data.csv','design':INFRA/'frontier_execution_2026_09_17/derived/nlsy/selected.csv'}
hashes={'family':'8372ae35fe32bd97d8a17ca40d11f6c9b158cb32f1499c7e2f5fb5df13e837a6',
        'base':'8e684c96d86bc97af92d65b9ea8c58438f5a54a535ed97988dc582b66b8d59d6',
        'design':'422b0964b568c60a5a9da6139ee6dc31ffc14a5a02dcae3e059f8809495bac3b'}
for name,path in paths.items():
    assert digest(path)==hashes[name], f'NLSY {name} source hash changed'
d=pd.read_csv(paths['family']).set_index('R0000100').sort_index()
for key in ['base','design']:
    z=pd.read_csv(paths[key]).set_index('R0000100').sort_index()
    assert d.index.is_unique and z.index.is_unique and d.index.equals(z.index)
    for c in set(d)&set(z):
        pd.testing.assert_series_equal(d[c],z[c],check_names=False)
    d=d.join(z.drop(columns=list(set(d)&set(z))))
assert len(d)==8984
d=d.copy()
d['stratum']=d.R1489700
d['psu']=d.R1489800
design=Design(d)
assert design.df==117 and len(design.grid)==234
w=d.U6365400.to_numpy()/100
np.testing.assert_allclose(w,d.weight)
# Verify the same public-design principal check independently, retaining all8984 rows.
score=d.R9829600.to_numpy()/1000
valid=score>=0
bw=d.R1236101.to_numpy()/100
point=float(bw[valid]@score[valid]/bw[valid].sum())
u=bw*np.where(valid,score-point,0)/bw[valid].sum()
se=np.sqrt(design.variance(u))
assert valid.sum()==7093 and abs(point-50.410)<.0006 and abs(se-.638)<.0006
audit['nlsy_design_check']={'n':int(valid.sum()),'mean':point,'se':se,'strata':117,'psus':234,'df':117,'benchmark_source':'https://www.nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects'}
domain=(d.identity.eq('Mexican_Chicano_self_ID')&d.own_us.eq(1)&d.mother_us.eq(1)&d.father_us.eq(1)).to_numpy()
g3=d.linked_exact.eq('G3_USborn_USparents_foreign_grandparent').to_numpy()
g4=d.linked_exact.eq('G4plus_USborn_USparents_all_four_USgrandparents').to_numpy()
for metric,num,den in [('G3',domain&g3,domain),('G4plus',domain&g4,domain),('Unresolved',domain&~(g3|g4),domain),('G4plus_MAR',domain&g4,domain&(g3|g4))]:
    results.append({'source':'NLSY97_R21','period':'2023_retention_1980_1984_births','window':'exact_1980_1984','metric':metric,**design.ratio(num,den,w)})
for name,path in paths.items():
    audit['sources'].append({'name':'nlsy_'+name,'path':str(path),'sha256':digest(path)})

gss_path=INFRA/'attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta'
assert digest(gss_path)=='a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344'
data,metadata=pyreadstat.read_dta(gss_path,usecols=['year','id','age','hispanic','born','parborn','granborn','vstrat','vpsu','wtssnrps'],encoding='latin1')
data=data.apply(pd.to_numeric,errors='coerce')
assert metadata.variable_value_labels['hispanic'][2]=='mexican, mexican american, chicano/a'
assert metadata.variable_value_labels['parborn'][0]=='both born in the u.s.'
gss_audit=[]
for start in [2016,2021]:
    d=data[data.year.between(start,2024)].reset_index(drop=True).copy()
    d['stratum']=d.vstrat
    d['psu']=d.vpsu
    assert d.groupby('stratum').year.nunique().eq(1).all()
    design=Design(d)
    w=d.wtssnrps.to_numpy()
    assert np.isfinite(w).all() and (w>0).all()
    base=(d.hispanic.eq(2)&d.born.eq(1)&d.parborn.eq(0)).to_numpy()
    birth=(d.year-d.age).where(d.age.between(18,120))
    g3=d.granborn.isin([1,2,3,4]).to_numpy()
    g4=d.granborn.eq(0).to_numpy()
    for window,lo,hi in [('approx_1980_1984',1980,1984),('inner_1981_1983',1981,1983),('wide_1979_1985',1979,1985),('shifted_1981_1985',1981,1985),('certain_members_1981_1984',1981,1984),('possible_members_1980_1985',1980,1985)]:
        domain=base&birth.between(lo,hi).to_numpy()
        for metric,num,den in [('G3',domain&g3,domain),('G4plus',domain&g4,domain),('Unresolved',domain&~(g3|g4),domain),('G4plus_MAR',domain&g4,domain&(g3|g4))]:
            results.append({'source':'GSS_NRPS','period':f'{start}_2024','window':window,'metric':metric,**design.ratio(num,den,w)})
        gss_audit.append({'period':f'{start}_2024','window':window,'full_n':len(d),'target_n':int(domain.sum()),'target_with_birthyear_missing_n':int((base&birth.isna().to_numpy()).sum()),'fullframe_strata':len(design.count),'fullframe_psus':len(design.grid),'year_counts':{str(int(k)):int(v) for k,v in d.loc[domain].year.value_counts().sort_index().items()}})
audit['gss_cohort_domain']=gss_audit
audit['sources'].append({'name':'gss','path':str(gss_path),'sha256':digest(gss_path)})
res=pd.DataFrame(results)
res.to_csv(OUT/'design_cohort_estimates.csv',index=False)

target_path=INFRA/'generation_estimation_2026_09_20/derived/cps_age_target.csv'
target=pd.read_csv(target_path).set_index('ageband').adult_share
assert np.isclose(target.sum(),1)
historical=pd.read_csv(OUT/'generation_age_comparators.csv')
standard=[]
for source in ['Pew2015_identifiers','Pew2015_16_nonidentifiers']:
    z=historical[(historical.source==source)&historical.age_band.isin(target.index)]
    pivot=z.pivot(index='age_band',columns='generation',values='percent')/100
    pivot=pivot.reindex(target.index)
    assert np.isfinite(pivot.to_numpy()).all()
    assert np.allclose(pivot.sum(axis=1),1)
    for metric,p in [('G3',pivot.G3),('G4plus',pivot.G4plus),('Unresolved',pivot.Unresolved),('G4plus_MAR',pivot.G4plus/(pivot.G3+pivot.G4plus))]:
        standard.append({'source':source,'metric':metric,'age_standardized_share':float(target@p),'method':'CPS2025 full adultG3+ fouragecell standardization; no design SE; unresolved age omitted; no pooling across identity targets'})
pd.DataFrame(standard).to_csv(OUT/'pew_standardized.csv',index=False)
audit['sources'].append({'name':'cps_target','path':str(target_path),'sha256':digest(target_path)})
(OUT/'design_followup_audit.json').write_text(json.dumps(audit,indent=2))
print(res[['source','period','window','metric','n','point','se','domain_df','ci95_domain_lo','ci95_domain_hi']].round(4).to_string(index=False))
print(pd.DataFrame(standard)[['source','metric','age_standardized_share']].to_string(index=False))
