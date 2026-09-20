"""Validate pinned acquisition bytes and the complete 2023 MCBS PUF schema."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

import pandas as pd

ROOT = Path(__file__).parent
MANIFESTS = ('manifest.json', 'extra_manifest.json', 'fee_manifest.json')
ZIP_SHA256 = '56937f1a623b77a85d5b401c1fdc00791098772c240073f70cbbbdff9db86d41'
CSV_SHA256 = '3407a9a76e8ddb71d9b8e840c4c14c94ddd25648c2cc60bf7eeb1d537c96b188'
CODEBOOK_SHA256 = '865624a99f0cdbdca5c6903bc88c93e738046710ab1ade803abea9ca88712fed'
BASE_COLUMNS = [
    'PUF_ID', 'SURVEYYR', 'VERSION', 'CSP_AGE', 'CSP_SEX', 'CSP_RACE',
    'CSP_INCOME', 'CSP_NCHRNCND', 'PAMTDU', 'PAMTVU', 'PAMTHU', 'PAMTHH',
    'PAMTIP', 'PAMTMP', 'PAMTOP', 'PAMTPM', 'DUAEVNTS', 'VUAEVNTS', 'HUAEVNTS',
    'HHAEVNTS', 'IPAEVNTS', 'MPAEVNTS', 'OPAEVNTS', 'PMAEVNTS', 'PAMTTOT',
    'PAMTCARE', 'PAMTCAID', 'PAMTMADV', 'PAMTALPR', 'PAMTOOP', 'PAMTDISC',
    'PAMTOTH', 'PEVENTS', 'CSPUFWGT',
]
REPLICATES = [f'CSPUF{i:03d}' for i in range(1, 101)]
EXPECTED_COLUMNS = BASE_COLUMNS + REPLICATES


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def verify_assets(root=ROOT):
    cache = root / '_cache'
    require(cache.is_dir(), f'Required source directory absent: {cache}')
    verified, skipped, seen = [], [], set()
    for manifest_name in MANIFESTS:
        records = json.loads((root / manifest_name).read_text())
        require(isinstance(records, list) and len(records) > 0,
                f'Empty or invalid manifest: {manifest_name}')
        acquired_in_manifest = 0
        for record in records:
            name = record.get('filename', '')
            require(name and Path(name).name == name, f'Invalid filename in {manifest_name}: {name!r}')
            status = record.get('status')
            if status == 'failed':
                require(record.get('error'), f'Failed acquisition lacks reason: {name}')
                skipped.append(dict(manifest=manifest_name, filename=name,
                                    url=record.get('url'), status='skipped_failed_acquisition',
                                    error=record['error']))
                continue
            require(status == 'acquired', f'Unknown acquisition status {status!r}: {name}')
            require(name not in seen, f'Duplicate successful acquisition: {name}')
            seen.add(name)
            source = cache / name
            require(source.is_file(), f'Missing acquired source: {source}')
            require(isinstance(record.get('bytes'), int) and record['bytes'] > 0,
                    f'Missing positive source byte count: {name}')
            require(source.stat().st_size == record['bytes'], f'Byte-count mismatch: {name}')
            expected_hash = record.get('sha256', '')
            require(re.fullmatch(r'[0-9a-f]{64}', expected_hash) is not None,
                    f'Missing/invalid SHA256: {name}')
            require(digest(source) == expected_hash, f'SHA256 mismatch: {name}')
            if name.endswith('.zip'):
                with zipfile.ZipFile(source) as archive:
                    require(archive.testzip() is None, f'ZIP CRC failure: {name}')
                    members = [dict(name=i.filename, bytes=i.file_size) for i in archive.infolist()]
                    require(len(members) > 0 and members == record.get('members'),
                            f'ZIP member inventory mismatch: {name}')
            elif name.endswith('.pdf'):
                with source.open('rb') as stream:
                    require(stream.read(4) == b'%PDF', f'PDF signature missing: {name}')
            verified.append(dict(manifest=manifest_name, filename=name, bytes=record['bytes'],
                                 sha256=expected_hash, status='verified'))
            acquired_in_manifest += 1
        require(acquired_in_manifest > 0, f'No acquired assets in {manifest_name}')
    require(len(verified) > 0, 'No acquired assets verified')
    require({'CSPUF2023_Data.zip', 'CSPUF2023_Codebook.txt', 'CSPUF2023_Methodology.zip'} <= seen,
            'Required MCBS data/documentation missing from successful manifest entries')
    return dict(verified_count=len(verified), verified_bytes=sum(r['bytes'] for r in verified),
                verified=verified, skipped_failed_count=len(skipped), skipped_failed_acquisitions=skipped)


def validate(root=ROOT):
    receipt = verify_assets(root)
    cache = root / '_cache'
    require(digest(cache / 'CSPUF2023_Data.zip') == ZIP_SHA256, 'Pinned MCBS ZIP SHA256 mismatch')
    codebook = cache / 'CSPUF2023_Codebook.txt'
    require(digest(codebook) == CODEBOOK_SHA256, 'Pinned MCBS codebook SHA256 mismatch')
    codebook_columns = [line.split()[0] for line in codebook.read_text().splitlines()
                        if re.match(r'^[A-Z][A-Z0-9_]+\s+', line)]
    require(codebook_columns == EXPECTED_COLUMNS, 'Complete codebook schema differs from pinned 134 fields')
    with zipfile.ZipFile(cache / 'CSPUF2023_Data.zip') as archive:
        payload = archive.read('cspuf2023.csv')
        require(hashlib.sha256(payload).hexdigest() == CSV_SHA256, 'Pinned CSV member SHA256 mismatch')
        with archive.open('cspuf2023.csv') as stream:
            data = pd.read_csv(stream)
    require(list(data.columns) == EXPECTED_COLUMNS, 'CSV schema does not match all 134 codebook fields')
    require(len(data) == 6920 and data.PUF_ID.is_unique, 'Incorrect person count or duplicate IDs')
    require(data.SURVEYYR.eq(2023).all(), 'Unexpected survey year')
    require(data.CSPUFWGT.gt(0).all(), 'Invalid full sample weights')
    require(data[REPLICATES].notna().all().all() and data[REPLICATES].ge(0).all().all(),
            'Missing or negative replicate weight')
    race_counts = {1: 5091, 2: 732, 3: 753, 4: 344}
    require(data.CSP_RACE.value_counts().to_dict() == race_counts, 'Race frequencies differ from codebook')
    result = dict(rows=len(data), columns=len(data.columns), variables=list(data.columns),
                  zip_sha256=ZIP_SHA256, csv_sha256=CSV_SHA256, codebook_sha256=CODEBOOK_SHA256,
                  codebook_schema_exact_match=True, id_unique=True, survey_year=2023,
                  race_counts=race_counts, weight_sum=float(data.CSPUFWGT.sum()),
                  origin_field_review='All 34 nonreplicate labels/values manually reviewed: no country or parent birthplace or Mexican-origin field; 100 remaining fields are replicate weights',
                  source_weight='CSPUFWGT', replicate_weights=REPLICATES,
                  scope='Community entire year, excludes any facility/hospice/institution event/cost; costs topcoded99.5%; no linkage to other MCBS files',
                  asset_verification=receipt)
    output = root / 'derived'
    output.mkdir(exist_ok=True)
    (output / 'mcbs_validation.json').write_text(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    result = validate()
    print(json.dumps(dict(rows=result['rows'], columns=result['columns'],
                          **result['asset_verification']), indent=2))
