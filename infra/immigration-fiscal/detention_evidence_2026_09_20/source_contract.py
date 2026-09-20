"""Required evidence contract shared by acquisition and verification."""
import hashlib
import json
from pathlib import Path

REQUIRED={'ice_fy2024_yearend.xlsx','scaap_fy2024_awards.pdf',
          'scaap_fy2024_awards.csv','scaap_fy2024_codebook.pdf','bjs_jails2023_table12.csv'}

def require(condition,message):
    if not condition:
        raise ValueError(message)

def load_manifest(root):
    records=json.loads((root/'manifest.json').read_text())
    require(isinstance(records,list) and bool(records),'Manifest must be a nonempty list')
    names=[r['file'] for r in records]
    require(len(set(names))==len(names),'Duplicate manifest file names')
    require(REQUIRED<=set(names),'Manifest omits required principal sources')
    for record in records:
        path=Path(record['local_file'])
        require(not path.is_absolute() and '..' not in path.parts,'Unsafe local_file path')
        require(path.name==record['file'],'Manifest file/path disagreement')
        require(record.get('sha256') and record.get('bytes',0)>0,'Missing source hash/size')
        require(record.get('url') or record.get('producer'),'No acquisition URL or producer')
    return records

def verify(path,record):
    require(path.is_file(),f'Required source missing: {path}')
    require(path.stat().st_size==record['bytes'],f'Size mismatch: {path}')
    require(hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],f'SHA256 mismatch: {path}')
