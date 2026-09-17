"""Extract the frozen public field request from the existing full NLSY97 archive."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--raw-dir', type=Path, default=ROOT / 'raw')
parser.add_argument('--output-dir', type=Path, default=ROOT / 'derived/nlsy')
parser.add_argument('--baseline-archive', type=Path, default=Path(
    '/Users/alien/Projects/iq-sex-differences/data/nlsy/nlsy97_all_1997-2023.zip'))
args = parser.parse_args()
out = args.output_dir
out.mkdir(parents=True, exist_ok=True)
fields = Path(__file__).with_name('required_analyzed_fields.NLSY97').read_text().split()
assert len(fields) == len(set(fields)) == 98 and 'R0000100' in fields
parent_fields = ['R0000100', 'R1201300', 'R0538700'] + [f'R{i}00' for i in range(14885, 14893)]
assert set(parent_fields).issubset(fields), 'Parent supplement is outside the frozen field request'
header = re.compile(r'^([A-Z]\d{5})\.(\d{2})\s+\[')
codebook = {}


def save_block(lines):
    if lines:
        match = header.match(lines[0])
        if match and match[1] + match[2] in fields:
            codebook[match[1] + match[2]] = ''.join(lines)


with zipfile.ZipFile(args.baseline_archive) as archive:
    buffer = []
    with archive.open('nlsy97_all_1997-2023.cdb') as stream:
        for raw in stream:
            line = raw.decode('utf-8')
            if header.match(line):
                save_block(buffer)
                buffer = []
            buffer.append(line)
        save_block(buffer)
    assert set(codebook) == set(fields), f'Missing field definitions: {set(fields) - set(codebook)}'
    (out / 'audited_selected_codebook.json').write_text(json.dumps(codebook, indent=2))
    (out / 'audited_selected_codebook.txt').write_text('\n'.join(codebook[k] for k in sorted(codebook)))
    with archive.open('nlsy97_all_1997-2023.csv') as stream:
        data = pd.read_csv(stream, usecols=fields, low_memory=False)
    source_members = [{"name": x.filename, "bytes": x.file_size, "crc32": x.CRC}
                      for x in archive.infolist() if x.filename.endswith(('.csv', '.cdb'))]
assert len(data) == 8984 and data.R0000100.is_unique
data.to_csv(out / 'full_selected_data.csv', index=False)
# The legacy estimator reads this explicit region/race supplement as a validated ID join.
data[parent_fields].to_csv(out / 'parent_supplement.csv', index=False)
small = args.raw_dir / 'nlsy97_gen_crime_1 (9).zip'
with zipfile.ZipFile(small) as archive:
    with archive.open('nlsy97_gen_crime_1.csv') as stream:
        cols = pd.read_csv(stream, nrows=0).columns
    common = sorted(set(cols) & set(fields))
    with archive.open('nlsy97_gen_crime_1.csv') as stream:
        supplied = pd.read_csv(stream, usecols=common, low_memory=False)
    bundled = set(re.findall(r'[A-Z]\d{7}', archive.read('nlsy97_gen_crime_1.NLSY97').decode()))
assert len(supplied) == 8984 and supplied.R0000100.is_unique
assert set(supplied.R0000100) == set(data.R0000100)
supplied.to_csv(out / 'download_selected_data.csv', index=False)
standalone = set(re.findall(r'[A-Z]\d{7}', (args.raw_dir / 'gen_crime_2026.NLSY97').read_text()))
coverage = dict(bundled=len(bundled), standalone=len(standalone), overlap=len(bundled & standalone),
                standalone_not_exported=len(standalone - bundled), exported_not_standalone=len(bundled - standalone),
                key_variables={k: dict(in_export=k in bundled, in_standalone=k in standalone) for k in fields})
(out / 'tagset_coverage.json').write_text(json.dumps(coverage, indent=2))
(out / 'standalone_missing_from_export.NLSY97').write_text('\n'.join(sorted(standalone - bundled)) + '\n')
digest = hashlib.sha256()
with args.baseline_archive.open('rb') as stream:
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(block)
(out / 'baseline_provenance.json').write_text(json.dumps({
    'source': str(args.baseline_archive), 'bytes': args.baseline_archive.stat().st_size,
    'sha256': digest.hexdigest(), 'members': source_members,
    'selected_fields': fields, 'rows': len(data), 'overlap_fields': common,
    'release': 'existing 1997-2023 archive; not asserted to be the latest 2026 release'
}, indent=2))
print(f'Extracted {data.shape}; supplied overlap {supplied.shape}; all IDs unique')
