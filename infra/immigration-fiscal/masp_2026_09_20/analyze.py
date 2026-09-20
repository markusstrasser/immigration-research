"""MASP held-author-file audit. Aggregate-only outputs; no national inference."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import pyreadstat

LANE = Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,default=LANE / 'raw/masp_combined.dta')
ap.add_argument('--output-prefix',default=str(LANE / 'derived/lineage'))
ap.add_argument('--parent-source',choices=['O2_only','O2_plus_I_assumed_codes'],default='O2_only')
a=ap.parse_args()
Path(a.output_prefix).resolve().parent.mkdir(parents=True, exist_ok=True)
digest=hashlib.sha256(a.source.read_bytes()).hexdigest()
assert digest=='3aeb2699940a41cfebf14e7f46ab3c76218f5f85ede68b9b8a1615c69e9b4aae'
raw,meta=pyreadstat.read_dta(a.source)
assert raw.shape==(1850,2560)
d=raw[raw.v3.notna()].copy()
assert len(d)==758 and d[['v3','prefix']].duplicated().sum()==0
assert d.prefix.isin([2,3]).all() and d.id.eq(d.v3).all()
assert d.v24.value_counts().to_dict()=={2:552,1:206}
assert (d.v24.eq(1)==d.v25.notna()).all()
assert meta.variable_value_labels['v140'][5]=='ba/bs'
audit={'hash':digest,'raw_rows':len(raw),'child_interviews':len(d),'source_families':d.id.nunique(),'full_original_family_ids':raw.id.nunique(),'known_child_country':int(d.v75.isin([1,2,3]).sum()),'child_years':d.v7.value_counts().to_dict(),'methods':{'identity':'v12-v23 original mention ranks; v25 closest only if v24==1. Text-coded Other left unresolved. v26-v37 describe to others, not substitutes. v51 is race response, never used for ethnic attrition.','lineage':'coalesce O2 and informant I after retaining conflicts unknown; c28/c29 reverse coding translated; generic nativity separate from confirmed Mexican ancestor.','variance':'unweighted local family descendants, sibling clusters; no population/design confidence intervals','income':'v348 valid1..21; respondent and spouse/partner gross income bin; nominal1996 label despite1998-2002 interviews. No bin midpoint mean.'}}
audit['parent_source']=a.parent_source
audit['methods']['lineage'] = ('Labeled O2 original-parent follow-up only; informant I excluded.'
    if a.parent_source == 'O2_only' else 'O2 coalesced with I under assumed I numeric codes; conflicts unknown.')
audit['methods']['benefits'] = 'Past-year respondent and spouse/partner receipt; not dollars or respondent-only incidence.'
audit['methods']['nativity'] = 'Questionnaire country-defined US/Other, not Census citizenship nativity. C19 Other includes Puerto Rico and Guam.'
audit['informant_numeric_code_limit']='I items have country labels but no value labels in held data/codebook. O2_only is primary; combining I assumes its country codes match O2 and is conditional sensitivity only.'
for field in ['v75','v87','v91']:
    x=d[field+'_O2'].where(d[field+'_O2'].isin([1,2,3]))
    y=d[field+'_I'].where(d[field+'_I'].isin([1,2,3]))
    if a.parent_source=='O2_only':
        y=pd.Series(np.nan,index=d.index)
    conflict=x.notna()&y.notna()&x.ne(y)
    d[field+'_parent_coalesced']=x.combine_first(y).mask(conflict)
    audit[field+'_source_counts']={'O2':int(x.notna().sum()),'I':int(y.notna().sum()),'conflict':int(conflict.sum()),'known':int(d[field+'_parent_coalesced'].notna().sum())}
own=d.v75.where(d.v75.isin([1,2,3]))
p1=d.v75_parent_coalesced
p2=d.c19.where(d.c19.isin([1,2,3]))
gp=pd.DataFrame({'rp_mother':d.v87_parent_coalesced,'rp_father':d.v91_parent_coalesced,'other_mother':d.c28.map({1:2,2:1,3:3}),'other_father':d.c29.map({1:2,2:1,3:3})})
parents_us=own.eq(1)&p1.eq(1)&p2.eq(1)
d['generation']=np.select([own.eq(2),own.eq(3),own.eq(1)&(p1.isin([2,3])|p2.isin([2,3])),parents_us&gp.isin([2,3]).any(axis=1),parents_us&gp.eq(1).all(axis=1)],['G1_Mexico','G1_other','G2','G3','G4plus'],default='Unresolved')
d['mex_ancestor_verified']=own.eq(2)|p1.eq(2)|p2.eq(2)|gp.eq(2).any(axis=1)|d[['v98_O2','v99_O2','v100_O2','v101_O2']].eq(1).any(axis=1)
d['G3_MexGP']=d.generation.eq('G3')&gp.eq(2).any(axis=1)
d['G4_MexGreatGP']=d.generation.eq('G4plus')&d[['v98_O2','v99_O2','v100_O2','v101_O2']].eq(1).any(axis=1)
audit['generation_counts']=d.generation.value_counts().to_dict()
audit['confirmed_mex_G3']=int(d.G3_MexGP.sum())
audit['confirmed_mex_G4_from_one_branch']=int(d.G4_MexGreatGP.sum())
audit['lineage_missing']={'own':int(own.isna().sum()),'original_parent':int(p1.isna().sum()),'other_parent':int(p2.isna().sum()),'us_parents_GP_unresolved':int((parents_us&~gp.isin([2,3]).any(axis=1)&~gp.eq(1).all(axis=1)).sum())}
mention=d[[f'v{k}' for k in range(12,24)]].apply(lambda s:s.between(1,6))
single=mention.sum(axis=1).eq(1)&d.v24.eq(2)
preferred=pd.Series(np.nan,index=d.index)
for k in range(12,22):
    preferred.loc[single&mention[f'v{k}']]=k-11
preferred.loc[d.v24.eq(1)]=pd.to_numeric(d.loc[d.v24.eq(1),'v25'].where(d.v25.between(1,10))).astype(float)
d['preferred_identity']=np.select([preferred.isin([1,2]),preferred.isin([3,4,9]),preferred.isin([5,6,7,8])],['Anglo_or_American','Hispanic_Latino_Spanish','Mexican_Chicano'],default='Other_or_unresolved')
latin=mention[[f'v{k}' for k in range(14,21)]].any(axis=1)
anglo=mention[['v12','v13']].any(axis=1)
other=mention[['v21','v22','v23']].any(axis=1)
d['any_mention_identity']=np.select([latin,anglo&~latin&~other],['Any_Mexican_Latino_Spanish','Only_Anglo_American'],default='Other_or_unresolved')
audit['identity_preferred']=d.preferred_identity.value_counts().to_dict()
audit['identity_any_mention']=d.any_mention_identity.value_counts().to_dict()
audit['single_flag_mention_count_mismatch']=int((d.v24.eq(2)&~mention.sum(axis=1).eq(1)).sum())
audit['race_white_with_Latino_selfmention']=int((d.v51.eq(1)&latin).sum())
d['ba_plus']=d.v140.isin([5,6,7]).astype(float).where(d.v140.between(0,7))
d['no_degree']=d.v140.eq(0).astype(float).where(d.v140.between(0,7))
d['grade_under12']=d.v139.lt(12).astype(float).where(d.v139.between(0,17))
d['income_under30k']=d.v348.between(1,7).astype(float).where(d.v348.between(1,21))
d['income_50kplus']=d.v348.between(12,21).astype(float).where(d.v348.between(1,21))
for out,field in [('ssi','v338'),('afdc_public_welfare','v340'),('food_stamps','v341')]:
    d[out]=d[field].eq(1).astype(float).where(d[field].isin([1,2]))
benef=d[['ssi','afdc_public_welfare','food_stamps']]
d['any_three_benefits']=benef.eq(1).any(axis=1).astype(float).where(benef.eq(1).any(axis=1)|benef.notna().all(axis=1))
# Year difference is an approximate age. Do not expose birth dates or records.
d['approx_age']=(d.v7-d.v74).where(d.v74.between(1900,1985))
d['joint_valid']=d[['ba_plus','income_under30k','any_three_benefits','approx_age']].notna().all(axis=1)
rows=[]
scopes={'all_children':pd.Series(True,index=d.index),'US_born':own.eq(1),'G3':d.generation.eq('G3'),'G4plus':d.generation.eq('G4plus'),'G3_MexGP':d.G3_MexGP,'G4_MexGreatGP':d.G4_MexGreatGP}
for scope,mask in scopes.items():
    for scheme in ['preferred_identity','any_mention_identity']:
        for identity,z in [('All',d[mask])]+list(d[mask].groupby(scheme)):
            for mode,v in [('endpoint',z),('joint_valid',z[z.joint_valid])]:
                for outcome in ['ba_plus','no_degree','grade_under12','income_under30k','income_50kplus','ssi','afdc_public_welfare','food_stamps','any_three_benefits','approx_age']:
                    valid=v[outcome].notna(); n=int(valid.sum())
                    # Suppress means of tiny identity-generation cells; keep counts.
                    est=float(v.loc[valid,outcome].mean())*(1 if outcome=='approx_age' else 100) if n>=20 else None
                    rows.append({'scope':scope,'scheme':scheme,'identity':identity,'sample':mode,'outcome':outcome,'n_total':len(v),'families':v.id.nunique(),'n_valid':n,'missing':int((~valid).sum()),'events':float(v.loc[valid,outcome].sum()) if outcome!='approx_age' and n>=20 else None,'estimate':est,'suppressed_n_under20':n<20})
pd.DataFrame(rows).to_csv(a.output_prefix+'-outcomes.csv',index=False)
ct=pd.crosstab(d.generation,d.any_mention_identity)
ct.to_csv(a.output_prefix+'-generation-identity.csv')
Path(a.output_prefix+'-audit.json').write_text(json.dumps(audit,indent=2,default=lambda x:int(x)))
print(json.dumps(audit,indent=2,default=lambda x:int(x)))
o=pd.DataFrame(rows)
print(o[(o.scope=='all_children')&(o['sample']=='endpoint')&o.outcome.isin(['ba_plus','income_under30k','any_three_benefits','approx_age'])].round(3).to_string(index=False))
print(ct.to_string())
