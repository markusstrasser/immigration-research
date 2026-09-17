from pathlib import Path
import argparse, hashlib, json, re, subprocess, zipfile
import pyreadstat
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--raw-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'raw')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'derived/pew')
args = parser.parse_args()
ROOT = args.output_dir
ROOT.mkdir(parents=True, exist_ok=True)
paths = sorted(p for p in args.raw_dir.glob('*.zip') if 'Latino' in p.name or 'Hispanic' in p.name or 'PHCNSL201' in p.name)
assert len(paths) == 8
manifest = []
for p in paths:
    dest = ROOT / p.stem
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(p) as z:
        basenames = set()
        for n in z.namelist():
            if n.startswith('__MACOSX/') or n.endswith('/'):
                continue
            target = dest / Path(n).name
            if target.name in basenames:
                raise ValueError(f'Archive basename collision: {n}')
            basenames.add(target.name)
            target.write_bytes(z.read(n))
    record = {'archive': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size, 'files': []}
    for f in dest.iterdir():
        record['files'].append(f.name)
        if f.suffix == '.pdf':
            subprocess.run(['pdftotext', '-layout', str(f), str(f.with_suffix('.txt'))], check=True)
        if f.suffix == '.docx':
            with zipfile.ZipFile(f) as doc:
                xml = ET.fromstring(doc.read('word/document.xml'))
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text = '\n'.join(''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in xml.findall('.//w:p', ns))
            f.with_suffix('.txt').write_text(text)
        if f.suffix == '.sav':
            try:
                df, meta = pyreadstat.read_sav(f, user_missing=True)
                record['encoding'] = 'readstat-auto'
            except pyreadstat.ReadstatError as exc:
                record['encoding_warning'] = str(exc)
                record['encoding'] = 'latin1'
                df, meta = pyreadstat.read_sav(f, user_missing=True, encoding='latin1')
            m = {'rows': len(df), 'columns': list(df), 'labels': meta.column_names_to_labels,
                 'value_labels': meta.variable_value_labels, 'missing_ranges': meta.missing_ranges}
            (dest / 'metadata.json').write_text(json.dumps(m, indent=2))
            record['n'] = len(df)
            record['sav'] = str(f)
            record['focus'] = {k:v for k,v in m['labels'].items() if re.search(r'grand|parent|weight|ancestr|heritage|immig|citizen|party|identit|latin|hispan|born|deport|america|race', v or '', re.I)}
    manifest.append(record)
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
for r in manifest:
    print(r['archive'], 'N=', r['n'])
    print(json.dumps(r['focus'], indent=2))
