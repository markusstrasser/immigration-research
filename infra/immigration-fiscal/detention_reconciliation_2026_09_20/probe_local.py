"""Inspect Census identifiers and functional-code coverage; do not estimate ICE spending."""
from collections import Counter
import json
import io
from pathlib import Path
import zipfile
from acquire import verified_bytes

ROOT = Path(__file__).resolve().parent
with zipfile.ZipFile(io.BytesIO(verified_bytes('census_2024_units.zip'))) as archive:
    if archive.testzip() is not None:
        raise ValueError('Census ZIP CRC failure')
    member = '2024_Individual_Unit_Files/2024FinEstDAT_07152026modp.txt'
    rows = archive.read(member).decode('ascii').splitlines()
if len(rows) != 511362 or set(map(len, rows)) != {32}:
    raise ValueError('Unexpected finance record count or layout')
codes = Counter(row[12:15] for row in rows)
ids = {row[:12] for row in rows}
if len(ids) != 24520 or not {'E04', 'E05', 'B89'} <= codes.keys():
    raise ValueError('Unexpected government or functional-code coverage')
result = dict(member=member, rows=len(rows), government_ids=len(ids),
              record_lengths=sorted(set(map(len, rows))), item_codes=dict(sorted(codes.items())),
              scope='Broad government functions, not ICE-purpose costs or matched reimbursements')
(ROOT/'derived').mkdir(exist_ok=True)
(ROOT/'derived'/'unit_probe.json').write_text(json.dumps(result, indent=2)+'\n')
print(f'PASS: {len(rows)} records, {len(ids)} government IDs, {len(codes)} functional item codes')
