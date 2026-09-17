"""Reconstruct reported biological-parent nativity from the parent interview roster.

The roster establishes who supplied a birthplace. No step/adoptive/guardian
birthplace becomes biological-parent birthplace merely because the person
answered the parent interview. This is not a country-specific ancestry measure.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import pandas as pd

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--lane-dir',type=Path,default=Path(__file__).resolve().parents[1])
P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy_family')
A=P.parse_args();O=A.output_dir;O.mkdir(parents=True,exist_ok=True)
base=pd.read_csv(A.lane_dir/'derived/nlsy/full_selected_data.csv').set_index('R0000100').sort_index()
extra=pd.read_csv(O/'parent_linkage_raw.csv').set_index('R0000100').sort_index()
assert len(extra)==8984 and extra.index.is_unique and base.index.equals(extra.index)
overlap=sorted(set(base)&set(extra))
for col in overlap:assert base[col].equals(extra[col]), f'Overlap mismatch: {col}'
d=base.join(extra.drop(columns=overlap),validate='one_to_one').copy(); audit={'verified_overlap':overlap};records=[];issues=[]

def valid(x):return x in (0,1)
def pos(x):return pd.notna(x) and x>0
def add(mapping,case,parent,source,value):
    if valid(value):records.append(dict(mapping=mapping,caseid=case,parent=parent,source=source,us_born=int(value)))

audit['PARHHI_slot_ID_disagreements']={str(slot):int((d[f'R{7036+slot:05}00'].gt(0)&d[f'R{7036+slot:05}00'].ne(slot)).sum()) for slot in range(1,10)}
audit['HHI2_slot_ID_disagreements']={str(slot):int((d[f'R{11009+slot:05}00'].gt(0)&d[f'R{11009+slot:05}00'].ne(slot)).sum()) for slot in range(1,17)}
for mapping in ['corrected_youth_HHI2','parent_roster_ID_mapped']:
    specs=[('mother','Z0501800',3,'R0533600','R0535100',2),('father','Z0502000',4,'R0532300','R0535000',1)] if mapping=='corrected_youth_HHI2' else [('mother','Z0501800',3,'R0733200','R0734600',2),('father','Z0502000',4,'R0731900','R0734500',1)]
    for case,r in d.iterrows():
        for parent,supplement,rel,bio_id,nonres_id,sex in specs:
            add(mapping,case,parent,'supplemental_'+supplement,r[supplement])
            pr_matches=pos(r.R0735000) and r.R0735000==r[bio_id]
            if pr_matches and r.R0734800==rel:
                add(mapping,case,parent,'responding_parent_R0551500_roster_confirmed',r.R0551500)
            elif pr_matches or r.R0734800==rel:
                issues.append(dict(mapping=mapping,caseid=case,parent=parent,issue='responding_parent_relationship_ID_disagreement'))
            spouse_candidates=[]
            if pos(r.R0735000):
                if mapping=='corrected_youth_HHI2':
                    slots=[j for j in range(1,17) if r[f'R{11009+j:05}00']==r.R0735000]
                    if len(slots)==1:
                        position=slots[0]
                        spouse_candidates=[r[f'R{11556+position:05}00'],r[f'R{11137+position:05}00']]
                    elif len(slots)>1:issues.append(dict(mapping=mapping,caseid=case,parent=parent,issue='duplicate_HHI2_responding_parent_ID'))
                else:
                    # PARHHI_ID.xx is NOT always equal to xx: join by stored ID.
                    slots=[j for j in range(1,10) if r[f'R{7036+j:05}00']==r.R0735000]
                    if len(slots)==1:spouse_candidates=[r[f'R{7295+slots[0]:05}00']]
            spouse_ids={v for v in spouse_candidates if pos(v)}
            if len(spouse_ids)==1 and r[bio_id] in spouse_ids:
                add(mapping,case,parent,'spouse_R0555000_biological_ID_confirmed',r.R0555000)
            if len(spouse_ids)>1:
                issues.append(dict(mapping=mapping,caseid=case,parent=parent,issue='ambiguous_spouse_partner_ID'))
            for n,identity,in_hh,sexvar,birth in [(1,'R0733400','R0733500','R0733700','R0559500'),(2,'R0733900','R0734000','R0734200','R0559600')]:
                # Household and nonresident IDs use different namespaces.
                target_id=r[bio_id] if r[in_hh]==1 else r[nonres_id] if r[in_hh]==0 else np.nan
                match=pos(r[identity]) and r[identity]==target_id
                sexmatch=r[sexvar]==sex
                if valid(r[birth]) and match and sexmatch:
                    add(mapping,case,parent,f'nonresponding_{n}_{birth}_roster_confirmed',r[birth])
                elif valid(r[birth]) and sexmatch:
                    issues.append(dict(mapping=mapping,caseid=case,parent=parent,issue=f'nonresponding_{n}_birth_unlinked'))

sources=pd.DataFrame(records)
sources.to_csv(O/'parent_nativity_sources.csv',index=False)
pd.DataFrame(issues,columns=['mapping','caseid','parent','issue']).to_csv(O/'linkage_issues.csv',index=False)
audit['linkage_issues']={mode:pd.Series([x['issue'] for x in issues if x['mapping']==mode],dtype=object).value_counts().to_dict() for mode in ['corrected_youth_HHI2','parent_roster_ID_mapped']}
for parent,supplement in [('mother','Z0501800'),('father','Z0502000')]:
    s=sources[sources.parent.eq(parent)&sources.mapping.eq('corrected_youth_HHI2')]
    grouped=s.groupby('caseid').us_born
    conflict=grouped.nunique().gt(1)
    values=grouped.first().mask(conflict)
    d[parent+'_us']=values.reindex(d.index)
    d[parent+'_conflict']=conflict.reindex(d.index,fill_value=False)
    d[parent+'_source_count']=grouped.size().reindex(d.index,fill_value=0)
    d[parent+'_sources']=s.groupby('caseid').source.agg('|'.join).reindex(d.index,fill_value='')
    d[parent+'_supplement_us']=d[supplement].where(d[supplement].isin([0,1]))
    roster=s[~s.source.str.startswith('supplemental_')].groupby('caseid').us_born
    d[parent+'_roster_only_us']=roster.first().mask(roster.nunique().gt(1)).reindex(d.index)
    par=sources[sources.parent.eq(parent)&sources.mapping.eq('parent_roster_ID_mapped')].groupby('caseid').us_born
    d[parent+'_parent_roster_us']=par.first().mask(par.nunique().gt(1)).reindex(d.index)
    audit[parent]=dict(known=int(values.notna().sum()),conflicts=int(conflict.sum()),
        supplemental_known=int(d[parent+'_supplement_us'].notna().sum()),by_source=s.source.value_counts().to_dict())

def coalesce(cols,name):
    a=d[cols].where(d[cols].isin([0,1]));conflict=a.nunique(axis=1).gt(1)
    audit[name]=dict(conflicts=int(conflict.sum()))
    return a.bfill(axis=1).iloc[:,0].mask(conflict)

d['own_us']=coalesce(['R5821400','S0191300','S2175900','S3952000','S7642200','T0135800'],'own')
for i,cols in enumerate([['S7639500','T0133500'],['S7639800','T0133800'],['S7640100','T0134100'],['S7640400','T0134400']]):d[f'gp{i}']=coalesce(cols,f'gp{i}')
gps=d[[f'gp{i}' for i in range(4)]];foreign_gp=gps.eq(0).any(axis=1);all_us_gp=gps.eq(1).all(axis=1)

def generations(mom,dad,exact):
    own_us=d.own_us.eq(1);foreign=d.own_us.eq(0);g2=own_us&(mom.eq(0)|dad.eq(0));usparents=own_us&mom.eq(1)&dad.eq(1)
    if exact:
        return np.select([foreign,g2,usparents&foreign_gp,usparents&all_us_gp,usparents],
            ['G1_foreign_born_childhood_resident','G2_USborn_at_least_one_foreign_biological_parent','G3_USborn_USparents_foreign_grandparent',
             'G4plus_USborn_USparents_all_four_USgrandparents','USborn_USparents_grandparents_unresolved'],default='Generation_unresolved')
    return np.select([foreign,g2,usparents],['G1_foreign_born_childhood_resident','G2_USborn_at_least_one_foreign_biological_parent','G3plus_USborn_both_biological_parents_US'],default='Generation_unresolved')

for name,mom,dad in [('linked',d.mother_us,d.father_us),('supplemental',d.mother_supplement_us,d.father_supplement_us),('roster_only',d.mother_roster_only_us,d.father_roster_only_us),('parent_roster',d.mother_parent_roster_us,d.father_parent_roster_us)]:
    d[name+'_exact']=generations(mom,dad,True);d[name+'_coarse']=generations(mom,dad,False)
    audit[name+'_exact']=d[name+'_exact'].value_counts().to_dict();audit[name+'_coarse']=d[name+'_coarse'].value_counts().to_dict()
    audit[name+'_strict_unresolved_like_prior']=int(d[name+'_exact'].isin(['Generation_unresolved','USborn_USparents_grandparents_unresolved']).sum())

mex=d[['R9702300','R9702400','R9702500']].isin([21,22,23]).any(axis=1)
known=d[['R9702300','R9702400','R9702500']].ge(1).any(axis=1)
d['identity']=np.select([mex,known],['Mexican_Chicano_self_ID','Other_self_ID'],default='Self_ID_unobserved')
d['comparison']=np.select([mex,d.R0538600.eq(0)&d.R0538700.eq(1)],['Mexican_Chicano_self_ID','Baseline_NH_White_not_Mexican_self_ID'],default='Other_or_unresolved')
d['sex']=d.R0536300.map({1:'Men',2:'Women'});d['weight']=d.U6365400/100
d['arrest']=d.E8033100.gt(0).astype(float).where(d.E8033100.ge(0));d['incarceration']=d.E8043100.gt(0).astype(float).where(d.E8043100.ge(0))
d['incarceration_exclude_incomplete']=d.incarceration.mask(d.E8043601.eq(1))
d['linked_classified']=d.linked_coarse.ne('Generation_unresolved')
d['supplemental_classified']=d.supplemental_coarse.ne('Generation_unresolved')

def table(groupby,filename):
    rows=[]
    for k,g in d.groupby(groupby,dropna=False):
        if not isinstance(k,tuple):k=(k,)
        for outcome in ['arrest','incarceration','incarceration_exclude_incomplete']:
            retained=g[g.weight.gt(0)];v=retained.dropna(subset=[outcome]);w=v.weight
            rows.append(dict(zip(groupby,k))|dict(outcome=outcome,baseline_n=len(g),positive_weight_n=len(retained),
                outcome_n=len(v),events=int(v[outcome].sum()),outcome_missing=len(retained)-len(v),
                unweighted_percent=100*v[outcome].mean(),weighted_percent=100*np.average(v[outcome],weights=w) if len(v) else np.nan,
                kish_effective_n=w.sum()**2/w.pow(2).sum() if len(v) else 0))
    pd.DataFrame(rows).to_csv(O/filename,index=False)
for mode in ['linked','supplemental','roster_only','parent_roster']:
    for resolution in ['exact','coarse']:
        table(['sex','identity',mode+'_'+resolution],f'{mode}_{resolution}_outcomes.csv')
table(['sex','comparison','linked_coarse'],'linked_comparison_outcomes.csv')
table(['sex','identity','linked_classified','supplemental_classified'],'classification_selection.csv')
pd.crosstab(d.supplemental_coarse,d.linked_coarse).to_csv(O/'generation_transition_counts.csv')
selected=['sex','identity','comparison','weight','own_us','mother_us','father_us','mother_conflict','father_conflict','mother_sources','father_sources',
          'linked_exact','linked_coarse','supplemental_exact','supplemental_coarse','roster_only_exact','roster_only_coarse','parent_roster_exact','parent_roster_coarse','arrest','incarceration','incarceration_exclude_incomplete']
d[selected].to_csv(O/'family_analysis_rows.csv')
audit['rows']=len(d);audit['positive_weight']=int(d.weight.gt(0).sum())
audit['incarceration_outcome_missing']=int(d.incarceration.isna().sum())
audit['semantics']={'unknowns':'negative codes and unresolved links are missing; conflicts remain unknown',
    'generation':'reported US birth, biological parent links, generic grandparent birth; not Mexico-specific lineage',
    'territory_caveat':'own and grandparent questions explicitly include US territories/Puerto Rico; parent questions say United States only. These are questionnaire-derived categories, not harmonized legal immigration generations.',
    'cohort':'official frame: 1980-1984 births resident in US at 1997 sampling; cumulative reported histories through 2023',
    'uncertainty':'weighted descriptions only; no survey-design standard errors; Kish n is not degrees of freedom',
    'grandparent_vintage':'same two waves as prior estimator to isolate parental reconstruction change'}
(O/'family_audit.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2),flush=True)
