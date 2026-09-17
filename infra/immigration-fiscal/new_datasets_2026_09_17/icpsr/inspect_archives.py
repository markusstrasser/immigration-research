from pathlib import Path
import hashlib
import json
import subprocess
import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--raw-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'raw')
parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parents[1] / 'derived/icpsr')
args = parser.parse_args()
ROOT = args.out
ROOT.mkdir(parents=True, exist_ok=True)
DOWNLOADS = args.raw_dir
inventory = []
for name in ['ICPSR_30302-V1.zip', 'ICPSR_20862-V6.zip']:
    candidates = list(DOWNLOADS.rglob(name))
    if len(candidates) != 1:
        raise ValueError(f'Expected one archive named {name}; found {candidates}')
    archive = candidates[0]
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    with zipfile.ZipFile(archive) as z:
        records = [{'path': info.filename, 'bytes': info.file_size} for info in z.infolist()]
        inventory.append({'archive': str(archive), 'sha256': digest, 'files': records})
        for info in z.infolist():
            target = ROOT / info.filename
            if target.resolve().is_relative_to(ROOT.resolve()):
                z.extract(info, ROOT)
            else:
                raise ValueError(f'Unsafe archive member {info.filename}')
for pdf in ROOT.rglob('*.pdf'):
    subprocess.run(['pdftotext', '-layout', str(pdf), str(pdf.with_suffix('.txt'))], check=True)
(ROOT / 'archive_inventory.json').write_text(json.dumps(inventory, indent=2))
print(json.dumps([{'archive': r['archive'], 'files': len(r['files']), 'sha256': r['sha256']} for r in inventory], indent=2))
