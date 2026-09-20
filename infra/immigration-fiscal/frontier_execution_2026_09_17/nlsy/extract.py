"""Extract only declared public score/design and crime timing fields."""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "build"))
import paths as _data_paths

from pathlib import Path
import argparse,json,re,zipfile,hashlib
import pandas as pd
P=argparse.ArgumentParser();P.add_argument('--archive',type=Path,default=_data_paths.reused_surveys_root(require_exists=False) / 'nlsy/nlsy97_all_1997-2023.zip');P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy');A=P.parse_args();O=A.output_dir;O.mkdir(parents=True,exist_ok=True)
fixed={'R0000100','R1489700','R1489800','R9829600','R1236101','R0536300','R0536401','R0536402','T6657200','R1205300','T5206900'}
head=re.compile(r'^([A-Z]\d{5})\.(\d{2})\s+\[([^]]+)\]')
codebook={};candidates={};lines=[]
def save(lines):
    if not lines:return
    m=head.match(lines[0]);text=''.join(lines)
    if not m:return
    ref=m[1]+m[2];q=m[3]
    if ref in fixed:codebook[ref]=text
    if q.startswith(('ARREST','INCARC')) and any(x in text[:400].upper() for x in ['AGE','FIRST','MONTH']):candidates[ref]=text
with zipfile.ZipFile(A.archive) as z:
    with z.open('nlsy97_all_1997-2023.cdb') as f:
        for raw in f:
            line=raw.decode()
            if head.match(line):save(lines);lines=[]
            lines.append(line)
        save(lines)
    assert set(codebook)==fixed
    (O/'crime_timing_candidates.json').write_text(json.dumps(candidates,indent=2))
    # Hold these diagnostic timing variables, but no outcome is defined from them without reading semantics.
    selected={**codebook,**candidates}
    (O/'selected_codebook.json').write_text(json.dumps(selected,indent=2))
    with z.open('nlsy97_all_1997-2023.csv') as f:d=pd.read_csv(f,usecols=list(selected),low_memory=False)
d.to_csv(O/'selected.csv',index=False)
assert len(d)==8984 and d.R0000100.is_unique
(O/'extraction.json').write_text(json.dumps({'source':str(A.archive),'bytes':A.archive.stat().st_size,'csv_sha256':hashlib.sha256((O/'selected.csv').read_bytes()).hexdigest(),'rows':len(d),'fields':list(d),'release':'1997-2023'},indent=2))
print('extracted',d.shape)
print('crime timing fields:',len(candidates))
