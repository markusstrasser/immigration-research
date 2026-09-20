#!/usr/bin/env python3
"""Bounded public SIPP lineage-support audit; aggregate outputs only."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import pandas as pd
import numpy as np

BASE = ['SSUID','PNUM','SPANEL','SWAVE','MONTHCODE','TAGE_EHC','ESEX','WPFINWGT','RIN_UNIV','EBORNUS','ABORNUS','TBORNPLACE','EORIGIN','AORIGIN','EHISPAN','AHISPAN','EEDUC','TPEARN','RSNAP_MNYN','RTANF_MNYN','RSSI_MNYN']
BASE += ['EBIOMOMUS','EBIODADUS','ABIOMOMUS','ABIODADUS','TBIOMOMNAT','TBIODADNAT','ABIOMOMNAT','ABIODADNAT']
for j in [1,2]:
    BASE += [f'EPNPAR{j}',f'EPAR{j}TYP',f'APNPAR{j}',f'APAR{j}TYP']

def extract(path, out):
    cache=out.with_suffix('.parquet')
    cachemeta=out.with_suffix('.cache.json')
    expected={'source_sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),'columns':BASE}
    if cache.exists() and cachemeta.exists() and json.loads(cachemeta.read_text())==expected:
        return pd.read_parquet(cache)
    chunks=[]
    with zipfile.ZipFile(path) as z:
        member=[n for n in z.namelist() if n.endswith('.csv')]
        assert len(member)==1,member
        with z.open(member[0]) as f:
            for ch in pd.read_csv(f,sep='|',usecols=BASE,chunksize=30000,dtype={'SSUID':'str'}):
                chunks.append(ch)
    df=pd.concat(chunks,ignore_index=True)
    assert not df.duplicated(['SPANEL','SSUID','PNUM','MONTHCODE']).any()
    df.to_parquet(cache,index=False)
    cachemeta.write_text(json.dumps(expected)+'\n')
    return df

def run(path, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    df=extract(path,out)
    assert not df.duplicated(['SPANEL','SSUID','PNUM','MONTHCODE']).any()
    # Principal-source guard: these public birthplace fields are REGION recodes.
    # Never interpret Americas/Caribbean as Mexico, including in parent links.
    assert set(df.TBIOMOMNAT.dropna().unique()) <= {1,3,4,5,6,7,8}
    assert set(df.TBIODADNAT.dropna().unique()) <= {1,3,4,5,6,7,8}
    # Raw release has two 99 unknown codes in addition to documented regions.
    assert set(df.loc[df.TBORNPLACE>60,'TBORNPLACE'].dropna().unique()) <= {61,62,63,64,65,66,99}
    # Person fields are repeated across months: verify rather than assume.
    key=['SPANEL','SSUID','PNUM']
    const=[c for c in BASE if c not in key+['MONTHCODE','TAGE_EHC','WPFINWGT','RIN_UNIV','TPEARN','RSNAP_MNYN','RTANF_MNYN','RSSI_MNYN']]
    nc=df.groupby(key,sort=False)[const].nunique(dropna=False)
    assert not (nc>1).any().any(),nc.max()[nc.max()>1].to_dict()
    persons=df.drop_duplicates(key).set_index(key)
    records=persons.to_dict('index')
    target=df[(df.MONTHCODE==12)&(df.RIN_UNIV==1)&(df.WPFINWGT>0)].copy().set_index(key)
    sums=df.groupby(key).agg(months=('MONTHCODE','size'),earnings=('TPEARN','sum'),snap=('RSNAP_MNYN',lambda x:int((x==1).any())),tanf=('RTANF_MNYN',lambda x:int((x==1).any())),ssi=('RSSI_MNYN',lambda x:int((x==1).any())))
    target=target.join(sums)

    def mother_father(k,strict):
        row=records[k]; links={1:[],2:[]}
        for j in [1,2]:
            if row[f'EPAR{j}TYP']!=1: continue
            if strict and (row[f'APAR{j}TYP']!=1 or row[f'APNPAR{j}']!=1): continue
            p=row[f'EPNPAR{j}']
            if pd.isna(p) or p<101: continue
            pk=(k[0],k[1],int(p))
            if pk not in records: continue
            sex=records[pk]['ESEX']
            if sex in links: links[sex].append(pk)
        # ESEX 1 male / 2 female. Ambiguous duplicate-sex biological links unknown.
        return [links[2][0] if len(links[2])==1 else None,links[1][0] if len(links[1])==1 else None]

    def own_us(k,strict):
        r=records[k]
        if strict and r['ABORNUS']!=1: return None
        return int(r['EBORNUS']) if r['EBORNUS'] in [1,2] else None

    def parent_us(k,strict):
        r=records[k]; result=[]
        for tag,pk in zip(['MOM','DAD'],mother_father(k,strict)):
            v=r[f'EBIO{tag}US']
            reported=int(v) if v in [1,2] and (not strict or r[f'ABIO{tag}US']==1) else None
            linked=own_us(pk,strict) if pk else None
            if reported and linked and reported!=linked:
                result.append(None)
            else: result.append(reported or linked)
        return result

    rows=[]
    for strict in [False,True]:
        mode='released_fields' if not strict else 'birth_parentlink_flags_as_reported_1'
        work=target.copy(); cats=[]; gpcounts=[]; parentid=[]
        for k,r in work.iterrows():
            links=mother_father(k,strict)
            parents=parent_us(k,strict)
            gps=sum([parent_us(pk,strict) if pk else [None,None] for pk in links],[])
            gpcounts.append(sum(x is not None for x in gps))
            parentid.append(any(records[pk]['EORIGIN']==1 and records[pk]['EHISPAN']==1 for pk in links if pk))
            if own_us(k,strict)!=1: c='not_confirmed_US_born'
            elif parents!=[1,1]: c='not_confirmed_two_US_born_parents'
            elif 2 in gps: c='generic_G3'
            elif gps==[1,1,1,1]: c='generic_G4plus'
            else:c='G3plus_unresolved'
            cats.append(c)
        work['generation']=cats;work['known_grandparents']=gpcounts;work['mexican_parent_identifier']=parentid
        work['identity']=np.where((work.EORIGIN==1)&(work.EHISPAN==1),'Mexican_identifier',np.where(work.EORIGIN==2,'non_Hispanic', 'other_or_unknown'))
        for age_name,mask in [('all',work.TAGE_EHC>=0),('adult18plus',work.TAGE_EHC>=18),('age25to64',work.TAGE_EHC.between(25,64))]:
            for (ident,gen),g in work[mask].groupby(['identity','generation']):
                w=g.WPFINWGT
                rows.append(dict(mode=mode,age=age_name,identity=ident,generation=gen,n=len(g),weighted_n=w.sum(),kish_neff=w.sum()**2/(w*w).sum(),known_all4_n=(g.known_grandparents==4).sum(),mexican_parent_identifier_n=g.mexican_parent_identifier.sum(),age_min=g.TAGE_EHC.min(),age_max=g.TAGE_EHC.max(),n_earnings_positive=(g.earnings>0).sum(),n_snap=g.snap.sum(),n_tanf=g.tanf.sum(),n_ssi=g.ssi.sum(),n_bachelorplus=(g.EEDUC>=43).sum()))
    pd.DataFrame(rows).to_csv(out.with_suffix('.csv'),index=False)
    counts={c:df.drop_duplicates(key)[c].fillna(-999).value_counts().sort_index().to_dict() for c in ['TBORNPLACE','TBIOMOMNAT','TBIODADNAT','ABIOMOMNAT','ABIODADNAT','ABIOMOMUS','ABIODADUS','ABORNUS','EPAR1TYP','ESEX']}
    info=dict(source=str(path),source_sha256=hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),person_months=len(df),unique_persons=len(persons),december_positive_weight_in_frame=len(target),panels=sorted(df.SPANEL.unique().tolist()),waves=sorted(df.SWAVE.unique().tolist()),field_counts=counts,exact_mexican_birthplace_observable=False,definition='US-born from EBORNUS; biological parents from sex-resolved EPAR1/2TYP=1 pointers; grandparents from linked parents parental US birth answers or recursive resident lookup; unknown and contradictory stay unknown; generic G3 requires any foreign grandparent, G4plus requires all four US born. These are generic generations, not Mexican lineage. Kish neff is weight concentration only, not design effective n.',outcomes='Support counts only; no estimated earnings/benefit contrast. SNAP/TANF/SSI are respondent coverage, not household dollars.')
    out.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps({k:v for k,v in info.items() if k!='field_counts'},indent=2),flush=True)
    print(pd.DataFrame(rows).query("age=='adult18plus' and identity=='Mexican_identifier'").to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--zip',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.zip,a.out)
