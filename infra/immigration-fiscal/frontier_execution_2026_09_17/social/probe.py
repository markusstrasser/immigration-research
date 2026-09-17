from pathlib import Path
import argparse, hashlib, json, zipfile, xml.etree.ElementTree as ET
import pandas as pd
import pyreadstat
P=argparse.ArgumentParser()
P.add_argument('--repo',type=Path,default=Path('/Users/alien/Projects/immigration-research'))
P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/social')
A=P.parse_args();R=A.repo;O=A.output_dir;O.mkdir(parents=True,exist_ok=True)
paths={2024:R/'sources/immigration-fiscal/data/census/cps_asec_2024_march.zip',2025:R/'infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip',2026:R/'infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip'}
for year,p in paths.items():
    with zipfile.ZipFile(p) as z:
        d=pd.read_csv(z.open(f'pppub{year%100}.csv'),nrows=4,dtype=str)
        print(year,[c for c in d if any(s in c.upper() for s in ['IDNUM','HHID','MIS','SEX','DIS_SC','LINENO'])])
doc=R/'sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/2025_ASEC_Replicate_Weight_Usage_Instructions.docx'
with zipfile.ZipFile(doc) as z:
    root=ET.fromstring(z.read('word/document.xml'))
    text='\n'.join(''.join(n.itertext()) for n in root if n.tag.endswith('body'))
    O.joinpath('cps_replicate_instructions.txt').write_text(text)
cols=['year','wtssps','wtssnrps','wtssall','vpsu','vstrat','born','parborn','hispanic','race','trust','age','educ']
d,m=pyreadstat.read_dta(str(R/'infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta'),usecols=cols,user_missing=True,encoding='latin1')
print('GSS labels',json.dumps({c:m.variable_value_labels.get(c) for c in ['born','parborn','trust']},indent=2))
print('GSS missing',m.missing_user_values)
print('GSS design',d[d.year>=2000].groupby('year').agg(n=('year','size'),strata=('vstrat','nunique'),psu=('vpsu','nunique'),nr=('wtssnrps','count')).to_string())
O.joinpath('gss_labels.json').write_text(json.dumps({'labels':m.variable_value_labels,'missing':m.missing_user_values},indent=2))
d.to_pickle(O/'gss_selected.pkl')
source=R/'infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta'
(O/'gss_provenance.json').write_text(json.dumps({'source':str(source),'sha256':hashlib.file_digest(source.open('rb'),'sha256').hexdigest(),'selected_sha256':hashlib.sha256((O/'gss_selected.pkl').read_bytes()).hexdigest()},indent=2)+'\n')
