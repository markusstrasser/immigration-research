"""Read only selected fields from the held NCES public file; no source mutation."""
import hashlib
import json
import argparse
from pathlib import Path
import re
import pandas as pd

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir', type=Path, required=True)
parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent / '_cache')
args = parser.parse_args()
SOURCE, OUT = args.source_dir, args.out
OUT.mkdir(parents=True, exist_ok=True)
dictionary = SOURCE / 'ECLSK_Kto8_child_STATA.dct'
data = SOURCE / 'childk8p.dat'
lock = json.loads((Path(__file__).resolve().parent / 'sources.json').read_text())
dictionary_sha = hashlib.sha256(dictionary.read_bytes()).hexdigest()
if dictionary_sha != lock['dictionary_sha256']:
    raise ValueError('Dictionary differs from verified release')
requested = '''CHILDID S1_ID S2_ID S3_ID S4_ID T1_ID T2_ID T4_ID GENDER RACE
WKLANGST WKSESL WKSESQ5 P2CHPLAC P2CNTRYB A1CLASS A2CLASS A4CLASS
A4KOTLA A4KLEP A4KNUML A4KTOTR A4KWHIT T4GLVL
A1LEP A1NUMLE A1TOTAG A1TOTRA A1WHITE A1HISP A1PHIS
A4LEP A4NUMLE A4TOTAG A4TOTRA A4WHITE A4HISP A4PHIS
A1NOESL A1ESLRE A1ESLOU A4NOESL A4ESLRE A4ESLOU
A1OTLAN A4OTLA A1CSPNH A4CSPNH A1PRESC A2ENGLS A4IENGL
FKCHGTCH FKCHGSCH BYCOMW0 Y2COMW0 C1_4PW0 BYCOMSTR BYCOMPSU Y2COMSTR Y2COMPSU
R1_KAGE R2_KAGE R3AGE R4AGE C1WEIGHT C2WEIGHT C3WEIGHT C4WEIGHT
C1R4RSCL C2R4RSCL C3R4RSCL C4R4RSCL
C1R4MSCL C2R4MSCL C3R4MSCL C4R4MSCL
C1RDGFLG C2RDGFLG C3RDGFLG C4RDGFLG
C1MTHFLG C2MTHFLG C3MTHFLG C4MTHFLG'''.split()
layout = {}
line_number = 1
for line in dictionary.read_text(encoding='latin1').splitlines():
    match = re.search(r'_line\((\d+)\)', line)
    if match:
        line_number = int(match.group(1))
    match = re.search(r'_column\((\d+)\)\s+(\w+)\s+(\w+)\s+%(\d+)(?:\.\d+)?\w+\s+"(.*)"', line)
    if match and match.group(3) in requested:
        start, kind, name, width, label = match.groups()
        layout[name] = {'line': line_number, 'start': int(start)-1, 'width': int(width), 'kind': kind, 'label': label}
missing = set(requested) - set(layout)
if missing:
    raise ValueError(f'Missing fields {missing}')
rows = []
digest = hashlib.sha256()
with data.open('rb') as stream:
    while True:
        lines = [stream.readline() for _ in range(15)]
        if not any(lines):
            break
        if not all(lines):
            raise ValueError('Partial trailing record')
        for line in lines:
            digest.update(line)
        row = {}
        for name, spec in layout.items():
            line = lines[spec['line']-1].rstrip(b'\r\n')
            start, width = spec['start'], spec['width']
            if len(line) < start + width:
                raise ValueError(f'Short physical line {name}')
            row[name] = line[start:start+width].decode('ascii').strip()
        rows.append(row)
frame = pd.DataFrame(rows)
if len(frame) != 21409 or frame.CHILDID.duplicated().any():
    raise ValueError(f'Unexpected rows or IDs: {len(frame)}')
if digest.hexdigest() != lock['data_sha256'] or data.stat().st_size != lock['data_bytes']:
    raise ValueError('Data differs from verified release')
for name, spec in layout.items():
    if not spec['kind'].startswith('str'):
        frame[name] = pd.to_numeric(frame[name], errors='raise')
frame.to_parquet(OUT / 'selected.parquet', index=False)
summary = {name: {'label': layout[name]['label'], 'unique': int(frame[name].nunique()), 'frequencies': {str(k): int(v) for k,v in frame[name].value_counts().head(12).items()}} for name in requested if name not in ['CHILDID'] and not name.endswith(('SCL','WEIGHT','AGE'))}
manifest = {'data': str(data), 'data_bytes': data.stat().st_size, 'data_sha256': digest.hexdigest(), 'dictionary_sha256': dictionary_sha, 'rows': len(frame), 'fields': layout, 'coverage': summary, 'selected_sha256': hashlib.sha256((OUT / 'selected.parquet').read_bytes()).hexdigest()}
(OUT / 'probe.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps({'rows': len(frame), 'bytes': data.stat().st_size, 'coverage': {k: summary[k] for k in ['S1_ID','S4_ID','T1_ID','T4_ID','P2CHPLAC','RACE','A1LEP','A1NUMLE','A4LEP','A4NUMLE','A1WHITE','A4WHITE','A1PHIS','A4PHIS']}}))
