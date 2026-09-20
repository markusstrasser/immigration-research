"""Select parent identity/nativity fields; never materialize the full wide CSV."""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / "build"))
import paths as _data_paths

import argparse,hashlib,json,re,zipfile
from pathlib import Path
import pandas as pd

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--archive',type=Path,default=_data_paths.reused_surveys_root(require_exists=False) / 'nlsy/nlsy97_all_1997-2023.zip')
P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy_family')
A=P.parse_args();A.output_dir.mkdir(parents=True,exist_ok=True)
with A.archive.open('rb') as source:
    source_hash=hashlib.file_digest(source,'sha256').hexdigest()
assert source_hash=='8c513e4804e5b07fce0e6b913258747dcf8707c73bb9ae54cce88dbff6d23c28', 'Unverified full-archive version'
fields=['R0000100','R0535300','R0551500','R0555000','R0558500','R0558600','R0558700','R0558800',
        'R0558900','R0559000','R0559100','R0559200','R0559300','R0559400','R0559500','R0559600',
        'R0731800','R0731900','R0732800','R0733000','R0733200','R0733300','R0733400','R0733500','R0733700',
        'R0733800','R0733900','R0734000','R0734200','R0734500','R0734600','R0734800','R0735000','R0735100']
fields += [f'R{x:05}00' for x in range(7296,7305)]
fields += ['R0533600','R0532300','R0535100','R0535000']
fields += [f'R{x:05}00' for x in range(7037,7046)]
fields += [f'R{x:05}00' for x in range(11138,11154)]
fields += [f'R{x:05}00' for x in range(11557,11573)]
fields += [f'R{x:05}00' for x in range(11010,11026)]
metadata_fields=fields
header=re.compile(r'^([A-Z]\d{5})\.(\d{2})\s+\[')
blocks={};lines=[]
def save(lines):
    if lines:
        m=header.match(lines[0])
        if m and m[1]+m[2] in metadata_fields:blocks[m[1]+m[2]]=''.join(lines)
with zipfile.ZipFile(A.archive) as z:
    with z.open('nlsy97_all_1997-2023.cdb') as f:
        for raw in f:
            line=raw.decode()
            if header.match(line):save(lines);lines=[]
            lines.append(line)
        save(lines)
    assert set(blocks)==set(metadata_fields)
    (A.output_dir/'parent_linkage_codebook.json').write_text(json.dumps(blocks,indent=2))
    (A.output_dir/'parent_linkage_codebook.txt').write_text('\n'.join(blocks[k] for k in metadata_fields))
    with z.open('nlsy97_all_1997-2023.csv') as f:
        data=pd.read_csv(f,usecols=fields,low_memory=False)
assert len(data)==8984 and data.R0000100.is_unique
data.to_csv(A.output_dir/'parent_linkage_raw.csv',index=False)
(A.output_dir/'extraction.json').write_text(json.dumps({'archive':str(A.archive),'sha256':source_hash,'bytes':A.archive.stat().st_size,'rows':len(data),'fields':fields},indent=2)+'\n')
(A.output_dir/'parent_linkage_fields.NLSY97').write_text('\n'.join(fields)+'\n')
print('Extracted',data.shape,flush=True)
