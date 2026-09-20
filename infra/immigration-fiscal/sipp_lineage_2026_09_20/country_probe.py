import argparse,hashlib,json,zipfile
from pathlib import Path
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--zip',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
cols=['TBORNPLACE','TBIOMOMNAT','TBIODADNAT']
values={k:set() for k in cols};rows=0
with zipfile.ZipFile(a.zip) as z:
    members=[m for m in z.namelist() if m.endswith('.csv')]
    assert len(members)==1,members
    with z.open(members[0]) as f:
        for ch in pd.read_csv(f,sep='|',usecols=cols,chunksize=50000):
            rows+=len(ch)
            for col in cols:values[col].update(ch[col].dropna().unique().tolist())
result={'source':str(a.zip),'source_sha256':hashlib.file_digest(a.zip.open('rb'),'sha256').hexdigest(),'rows_scanned':rows,'code_support':{k:sorted(v) for k,v in values.items()}}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
