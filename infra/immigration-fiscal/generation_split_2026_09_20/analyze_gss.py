"""Independent GSS adult benchmark; no CPS imputation or current-year estimate."""
from pathlib import Path
import argparse
import hashlib
from itertools import product
import json
import pandas as pd
import numpy as np
import pyreadstat

parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3])
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent/'derived/recovery')
args=parser.parse_args()
p=args.root/'infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta'
sha=hashlib.sha256(p.read_bytes()).hexdigest()
if sha != 'a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344':
 raise ValueError('GSS source hash changed')
args.output_dir.mkdir(parents=True,exist_ok=True)
cols=['year','born','parborn','granborn','hispanic','ethnic','age','wtssps','wtssnrps']
d,m=pyreadstat.read_dta(p,usecols=cols,encoding='latin1')
assert m.variable_value_labels['hispanic'][2]=='mexican, mexican american, chicano/a'
assert m.variable_value_labels['born'][1]=='yes'
assert m.variable_value_labels['parborn'][0]=='both born in the u.s.'
assert m.variable_value_labels['granborn'][0]=='none'
d=d.apply(pd.to_numeric,errors='coerce')
d['gen']=np.select([d.born.eq(2),d.born.eq(1)&d.parborn.isin([1,2,4,6,8]),d.born.eq(1)&d.parborn.eq(0)&d.granborn.between(1,4),d.born.eq(1)&d.parborn.eq(0)&d.granborn.eq(0)],['G1','G2','G3_generic','G4plus_generic'],default='unknown')
rows=[]
for start in [2000,2006,2010,2016,2021]:
 for label,origin in [('selfid_Mexican',d.hispanic.eq(2)),('family_origin_Mexico',d.ethnic.eq(17))]:
  x=d[origin&d.year.ge(start)&d.wtssps.gt(0)]
  for g,s in x.groupby('gen'):
   rows.append(dict(start=start,end=2024,origin=label,generation=g,n=len(s),weight=float(s.wtssps.sum()),share=float(s.wtssps.sum()/x.wtssps.sum())))
t=pd.DataFrame(rows)
t.to_csv(args.output_dir/'gss_generation_probe_20260920.csv',index=False)
print(t.to_string(index=False))
rows=[]
for start,weight in product([2016,2021],['wtssps','wtssnrps']):
 x=d[d.hispanic.eq(2)&d.year.between(start,2024)&d.born.eq(1)&d.parborn.eq(0)].copy()
 assert (np.isfinite(x[weight])&x[weight].gt(0)).all(), 'Invalid weight in target'
 x['ageband']=np.select([x.age.between(18,24),x.age.between(25,44),x.age.between(45,64),x.age.between(65,89)],['18-24','25-44','45-64','65+'],default='unknown')
 for band in ['all','18-24','25-44','45-64','65+','unknown']:
  z=x if band=='all' else x[x.ageband.eq(band)]
  for g in ['G3_generic','G4plus_generic','unknown']:
   s=z[z.gen.eq(g)]
   rows.append(dict(start=start,end=2024,weight_variable=weight,ageband=band,generation=g,n=len(s),denominator_n=len(z),weight=float(s[weight].sum()),share=float(s[weight].sum()/z[weight].sum()) if len(z) else None))
sub=pd.DataFrame(rows)
sub.to_csv(args.output_dir/'gss_generation_subgroup_20260920.csv',index=False)
assert np.allclose(sub[sub.denominator_n.gt(0)].groupby(['start','weight_variable','ageband']).share.sum(),1)
print(sub.to_string(index=False))
manifest=dict(source=str(p.resolve()),sha256=sha,rows=len(d),
 source_url='https://gss.norc.org/get-the-data.html',
 preferred_weight='wtssnrps',
 weight_labels={k:m.column_names_to_labels[k] for k in ['wtssps','wtssnrps']},
 labels={k:m.variable_value_labels[k] for k in ['born','parborn','granborn','hispanic']},
 limitations=['Pooled cross-sections, not a 2025 population allocation',
 'Generic foreign grandparent, country unavailable',
 'No design-based intervals or imputation; unknown grandparents remain in denominator'],
 outputs=['gss_generation_probe_20260920.csv','gss_generation_subgroup_20260920.csv'])
(args.output_dir/'gss_generation_probe_20260920_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
