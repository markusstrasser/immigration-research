"""Failure-path regressions; original acquired files are never modified."""
from pathlib import Path
import json
import shutil
import tempfile

import validate_mcbs as validator


def stage(root):
    (root / '_cache').mkdir()
    for name in validator.MANIFESTS:
        shutil.copy2(validator.ROOT / name, root / name)
    for source in (validator.ROOT / '_cache').iterdir():
        if source.is_file():
            (root / '_cache' / source.name).symlink_to(source)


def reject(label, change, expected):
    with tempfile.TemporaryDirectory(prefix='fiscal-integrity-', dir='/private/tmp') as directory:
        root = Path(directory)
        stage(root)
        change(root)
        try:
            validator.validate(root)
        except ValueError as error:
            if expected not in str(error):
                raise RuntimeError(f'{label}: unexpected failure: {error}') from error
        else:
            raise RuntimeError(f'{label}: corrupted fixture passed')
    return dict(case=label, rejected=True, expected=expected)


def all_failed(root):
    record = dict(filename='missing.pdf', status='failed', error='deliberate fixture failure')
    (root / 'manifest.json').write_text(json.dumps([record]))


def tamper(root):
    path = root / '_cache' / 'census_linkage_inventory.pdf'
    payload = path.read_bytes()
    path.unlink()
    path.write_bytes(payload[:-1] + bytes([payload[-1] ^ 1]))


def member_mismatch(root):
    path = root / 'manifest.json'
    records = json.loads(path.read_text())
    row = next(r for r in records if r['filename'] == 'CSPUF2023_Data.zip')
    row['members'][0]['bytes'] += 1
    path.write_text(json.dumps(records))


results = [
    reject('empty manifest', lambda p: (p / 'manifest.json').write_text('[]'), 'Empty or invalid manifest'),
    reject('zero acquired selection', all_failed, 'No acquired assets'),
    reject('changed bytes same length', tamper, 'SHA256 mismatch'),
    reject('wrong member metadata', member_mismatch, 'ZIP member inventory mismatch'),
    reject('raw fallback forbidden', lambda p: (p / '_cache').rename(p / 'raw'), 'Required source directory absent'),
]
(validator.ROOT / 'derived' / 'validation_failure_checks.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
