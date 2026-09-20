
import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "build"))
import paths as _data_paths

import argparse,json,pathlib
import numpy as np,pandas as pd
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[1]/'derived/nlsy');p.add_argument('--profile-source-dir',type=pathlib.Path,default=_data_paths.reused_surveys_root(require_exists=False) / 'nlsy');args=p.parse_args();out=args.output_dir
d=pd.read_csv(out/'full_selected_data.csv'); s=pd.read_csv(out/'download_selected_data.csv')
audit={}
for name,x in [('full',d),('supplied',s)]:
    assert len(x)==8984 and x.R0000100.is_unique
    audit[name]=dict(rows=len(x),unique_ids=x.R0000100.nunique(),min_id=int(x.R0000100.min()),max_id=int(x.R0000100.max()))
d=d.set_index('R0000100').sort_index().copy();s=s.set_index('R0000100').sort_index();assert d.index.equals(s.index)
audit['supplied_overlap']={c:int((d[c].ne(s[c])&~(d[c].isna()&s[c].isna())).sum()) for c in s.columns}
ability=pd.read_csv(args.profile_source_dir/'hu2025_nlsy97_mgcfa_input.csv');assert ability.caseid.is_unique
audit['ability']=dict(rows=len(ability),matched=int(ability.caseid.isin(d.index).sum()),columns=ability.columns.tolist())
if 'female' in ability:
    linked=ability.set_index('caseid').join(d.R0536300,how='left',validate='one_to_one')
    audit['ability']['sex_disagreements']=int(linked.female.ne(linked.R0536300-1).sum())
raw=pd.read_parquet(args.profile_source_dir/'profile_outcomes/source_extract.parquet').set_index('caseid').sort_index();assert raw.index.is_unique
mapping={'R1193000':'household','T8129600':'degree','T8123600':'adult_age','T8135900':'weight_2013','T8122000':'main_job','T8976500':'wage_receipt','T8976700':'wage_amount'}
audit['profile_source_cache']=dict(rows=len(raw),matched=len(raw.index.intersection(d.index)),mismatches={k:int(d[k].ne(raw[v]).sum()) for k,v in mapping.items()})
def coalesce_binary(codes,label):
    x=d[codes].where(d[codes].isin([0,1]));conflict=x.nunique(axis=1)>1
    result=x.bfill(axis=1).iloc[:,0].mask(conflict)
    audit[label]=dict(observed=int(result.notna().sum()),conflicts=int(conflict.sum()))
    return result
own=['R5821400','S0191300','S2175900','S3952000','S7642200','T0135800']
d['own_us']=coalesce_binary(own,'own_birth')
gp_pairs=[['S7639500','T0133500'],['S7639800','T0133800'],['S7640100','T0134100'],['S7640400','T0134400']]
for i,cols in enumerate(gp_pairs):d[f'gp{i}']=coalesce_binary(cols,f'gp{i}')
gps=d[[f'gp{i}' for i in range(4)]];any_foreign=gps.eq(0).any(axis=1);all_us=gps.eq(1).all(axis=1)
d['gp_history']=np.select([any_foreign,all_us],['At_least_one_foreign_born_grandparent','All_four_US_born_grandparents'],default='Grandparent_history_unresolved')
ethcols=['R9702300','R9702400','R9702500'];mex=d[ethcols].isin([21,22,23]).any(axis=1);eth_known=d[ethcols].ge(1).any(axis=1)
d['mexican_self_id']=np.select([mex,eth_known],['Mexican_Chicano_self_ID','Other_self_ID'],default='ASVAB_origin_not_observed')
mom=d.Z0501800.where(d.Z0501800.isin([0,1]));dad=d.Z0502000.where(d.Z0502000.isin([0,1]))
d['strict_generation']=np.select([d.own_us.eq(0),d.own_us.eq(1)&(mom.eq(0)|dad.eq(0)),d.own_us.eq(1)&mom.eq(1)&dad.eq(1)&any_foreign,d.own_us.eq(1)&mom.eq(1)&dad.eq(1)&all_us],['Foreign_born_childhood_resident','G2_known_biological_parent_foreign','G3_known_US_parents_foreign_grandparent','G4plus_known_US_parents_and_grandparents'],default='Generation_unresolved')
d['sex']=d.R0536300.map({1:'Men',2:'Women'}); d['weight']=d.U6365400/100
d['arrest_reported']=d.E8033100.gt(0).astype(float).where(d.E8033100.ge(0))
d['incarc_reported']=d.E8043100.gt(0).astype(float).where(d.E8043100.ge(0))
d['incarc_without_incomplete_flag']=d.incarc_reported.mask(d.E8043601.eq(1))
d['hispanic_informant']=d.R0538600.map({0:'Not_Hispanic_informant',1:'Hispanic_informant'})
audit['coverage']=dict(positive_2023_weight=int(d.weight.gt(0).sum()),incarceration_invalid=int(d.incarc_reported.isna().sum()),incomplete_history_flag=int(d.E8043601.eq(1).sum()),strict_generation=d.strict_generation.value_counts().to_dict(),self_id=d.mexican_self_id.value_counts().to_dict())
if (out/'parent_supplement.csv').exists():
    extra=pd.read_csv(out/'parent_supplement.csv').set_index('R0000100');assert extra.index.is_unique and set(extra.index)==set(d.index)
    for c in extra.columns:
        if c in d:assert d[c].equals(extra[c].reindex(d.index))
        else:d[c]=extra[c]
    d['mexcam_parent_record']=np.where(d.R1489100.gt(0),'Mexico_CentralAmerica_parent_recorded','No_Mexico_CentralAmerica_parent_recorded')
    d['any_foreign_parent_record']=np.where(d[[f'R{i}00' for i in range(14885,14893)]].sum(axis=1).gt(0),'Foreign_region_parent_recorded','No_foreign_region_parent_recorded')
    audit['parent_vs_identity']=pd.crosstab(d.mexcam_parent_record,d.mexican_self_id).to_dict()
    d['comparison_group']=np.select([mex,d.R0538600.eq(0)&d.R0538700.eq(1)],['Mexican_Chicano_self_ID','Baseline_NH_White_not_Mexican_self_ID'],default='Other_or_unresolved')

def table(groupby,name,condition=None):
    x=d[d.weight.gt(0)].copy()
    if condition is not None:x=x[condition.reindex(x.index)]
    rows=[]
    for keys,g in x.groupby(groupby,dropna=False):
        if not isinstance(keys,tuple):keys=(keys,)
        for outcome in ['arrest_reported','incarc_reported','incarc_without_incomplete_flag']:
            v=g.dropna(subset=[outcome]);w=v.weight;rate=np.average(v[outcome],weights=w) if len(v) else np.nan
            rows.append(dict(zip(groupby,keys))|dict(outcome=outcome,n_group=len(g),n_observed=len(v),events=int(v[outcome].sum()),missing=len(g)-len(v),weighted_percent=rate*100,unweighted_percent=v[outcome].mean()*100,n_eff=float(w.sum()**2/(w*w).sum()) if len(v) else 0,birth_year_mean=float(np.average(v.R0536402,weights=w)) if len(v) else np.nan))
    pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False)
table(['sex','mexican_self_id'],'t1_self_identity')
table(['sex','mexican_self_id','gp_history'],'t2_USborn_grandparent_history',d.own_us.eq(1))
table(['sex','mexican_self_id','strict_generation'],'t3_strict_generation')
if 'mexcam_parent_record' in d:
    table(['sex','mexcam_parent_record','mexican_self_id'],'t4_parent_region_vs_identity')
    table(['sex','mexican_self_id','any_foreign_parent_record','gp_history'],'t5_USborn_parent_region_GP',d.own_us.eq(1))
    table(['sex','comparison_group'],'t6_NHWhite_comparison')
d[['sex','mexican_self_id','strict_generation','gp_history','weight','arrest_reported','incarc_reported']].to_csv(out/'analysis_rows.csv')
(out/'join_and_coverage.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2),flush=True)
print(pd.read_csv(out/'t1_self_identity.csv').to_string(index=False),flush=True)
