"""Diagnose the observed CPS residual without assigning missing ancestry."""
from pathlib import Path
import importlib.util
import zipfile
import json
import hashlib
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[3]
outdir = Path(__file__).resolve().parent/'derived/recovery'
outdir.mkdir(parents=True,exist_ok=True)
src = root/'infra/immigration-fiscal/generation_split_2026_09_20/analyze_cps.py'
spec = importlib.util.spec_from_file_location('generation', src)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
if hashlib.sha256(m.RAW.read_bytes()).hexdigest() != m.SHA:
    raise ValueError('CPS2025 source hash changed')
with zipfile.ZipFile(m.RAW) as z:
    with z.open('pppub25.csv') as f:
        header = pd.read_csv(f, nrows=0).columns.tolist()
    cols = m.COLS + ['PERRP', 'PERIDNUM', 'A_SEX', 'PRDTRACE']
    with z.open('pppub25.csv') as f:
        d = pd.read_csv(f, usecols=cols, dtype={'PERIDNUM': str})
    with z.open('asec_csv_repwgt_2025.csv') as f:
        w = pd.read_csv(f, usecols=['h_seq', 'PPPOS'] + m.WEIGHTS).rename(columns={'h_seq':'PH_SEQ'})
source_n = len(d)
if not d.PERIDNUM.notna().all() or not d.PERIDNUM.is_unique:
    raise ValueError('Missing or duplicate longitudinal ID')
d = d.merge(w, on=['PH_SEQ', 'PPPOS'], validate='one_to_one')
if len(d) != source_n:
    raise ValueError('Weight join lost people')
weights = d[m.WEIGHTS].to_numpy(float)
m.validate_weights(weights)
np.testing.assert_allclose(d.MARSUPWT/100,weights[:,0],rtol=0,atol=.011)
unresolved = m.classify(d)['G3plus_unresolved']
base = m.population_masks(d)['G3plus']
n = len(d)
lookup = pd.Series(np.arange(n), index=pd.MultiIndex.from_frame(d[['PH_SEQ','A_LINENO']]))
bio = np.zeros((n,2), bool)
usable = np.zeros((n,2), bool)
gp = np.full((n,4), np.nan)
inconsistent = np.zeros(n, bool)
for slot in (1,2):
    line = d[f'PEPAR{slot}'].to_numpy()
    par = lookup.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(),line])).fillna(-1).to_numpy(int)
    p = np.maximum(par,0)
    bio[:,slot-1] = (line>0)&(par>=0)&d[f'PEPAR{slot}TYP'].eq(1).to_numpy()
    native_parent = np.isin(d.PENATVTY.to_numpy()[p],m.US)
    inconsistent |= bio[:,slot-1]&~native_parent
    usable[:,slot-1] = bio[:,slot-1]&native_parent
    for j,field in enumerate(['PEMNTVTY','PEFNTVTY']):
        mask = usable[:,slot-1]
        gp[mask,2*(slot-1)+j] = d[field].to_numpy()[p[mask]]
rows=[]
def add(label,mask,partition):
    mask = mask&unresolved
    for label_age, ages in [('all',np.ones(n,bool)),('under18',d.A_AGE.lt(18).to_numpy()),('18plus',d.A_AGE.ge(18).to_numpy())]:
        mask_age=mask&ages
        v=weights[mask_age].sum(axis=0)
        rows.append(dict(partition=partition,reason=label,age=label_age,n=int(mask_age.sum()),people=v[0],se=np.sqrt(4/160*((v[1:]-v[0])**2).sum())))
add('inconsistent_linked_biological_parent_birthplace',inconsistent,'exclusive')
add('no_biological_parent_link',~inconsistent&(bio.sum(axis=1)==0),'exclusive')
add('one_biological_parent_link',~inconsistent&(bio.sum(axis=1)==1),'exclusive')
add('two_biological_parent_links',~inconsistent&(bio.sum(axis=1)==2),'exclusive')
# Positive codes can include "Elsewhere"; these diagnostics do not establish
# a specifically named foreign country or an additional generation assignment.
add('grandparent_code_outside_US_and_Mexico',np.any((gp>0)&~np.isin(gp,m.US)&(gp!=303),axis=1),'overlapping')
add('all_four_positive_codes_not_all_US_no_Mexico',np.all(gp>0,axis=1)&~np.isin(gp,m.US).all(axis=1)&~(gp==303).any(axis=1),'overlapping')
add('some_linked_grandparent_item_missing',np.any(np.isfinite(gp)&(gp<=0),axis=1),'overlapping')
refs=d[d.PERRP.isin([40,41])][['PH_SEQ','PENATVTY','A_AGE']].rename(columns={'PENATVTY':'ref_birth','A_AGE':'ref_age'})
assert refs.PH_SEQ.is_unique
ref=d[['PH_SEQ']].merge(refs,on='PH_SEQ',how='left',validate='many_to_one')
add('reported_grandchild_of_Mexico_born_reference_person',d.PERRP.eq(49).to_numpy()&ref.ref_birth.eq(303).to_numpy(),'candidate_nonbiological_unknown')
add('reported_grandchild_of_US_born_reference_person',d.PERRP.eq(49).to_numpy()&ref.ref_birth.isin(m.US).to_numpy(),'candidate_nonbiological_unknown')
out=pd.DataFrame(rows)
out.to_csv(outdir/'generation_unresolved_reasons_20260920.csv',index=False)
assert np.isclose(out.query('partition=="exclusive" and age=="all"').people.sum(),weights[unresolved,0].sum())
print(out.query('age=="all"').to_string(index=False))
print('\nExclusive by age:\n'+out.query('partition=="exclusive" and age!="all"').to_string(index=False))
print('\nHeader name candidate fields:',[x for x in header if any(s in x.lower() for s in ['name','surname','firstn','lastn'])])
print('Header matching ID fields:',[x for x in header if 'ID' in x or x in ['PERRP','A_EXPRRP','A_FAMREL','PRFAMREL','PEPAR1','PEPAR2']])
print('Person PERIDNUM unique:',d.PERIDNUM.is_unique)
print('Source rows:',len(d),'columns:',len(header),'unresolved:',weights[unresolved,0].sum())
codes=np.unique(gp[unresolved][np.isfinite(gp[unresolved])])
print('Finite grandparent codes among unresolved:',codes.tolist())
audit=dict(source=str(m.RAW),sha256=m.SHA,rows=source_n,
           columns=len(header),unresolved_people=float(weights[unresolved,0].sum()),
           note='Reason partition only; overlapping diagnostics are not additional people.')
(outdir/'unresolved_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
