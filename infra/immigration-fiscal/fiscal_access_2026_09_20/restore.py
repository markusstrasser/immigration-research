"""Restore only frozen successful sources without replacing any existing bytes."""
from pathlib import Path
import json
import os
import tempfile

import requests

from validate_mcbs import MANIFESTS, ROOT, digest, require, verify_assets


def download(url, destination):
    with requests.get(url, stream=True, timeout=(30, 90)) as response:
        response.raise_for_status()
        with destination.open('wb') as stream:
            for chunk in response.iter_content(1024 * 1024):
                stream.write(chunk)


def verify_source(path, record):
    require(path.is_file(), f'Expected regular source file: {path}')
    require(path.stat().st_size == record['bytes'], f'Byte-count mismatch: {path.name}')
    require(digest(path) == record['sha256'], f'SHA256 mismatch: {path.name}')


def restore(root=ROOT, fetch=download):
    records, failed, names = [], [], set()
    for manifest_name in MANIFESTS:
        manifest = json.loads((root / manifest_name).read_text())
        require(isinstance(manifest, list) and manifest, f'Empty manifest: {manifest_name}')
        successes = 0
        for record in manifest:
            if record.get('status') == 'failed':
                failed.append(dict(manifest=manifest_name, **record))
                continue
            require(record.get('status') == 'acquired', f'Unknown status: {record}')
            name = record.get('filename', '')
            require(name and Path(name).name == name, f'Unsafe source filename: {name!r}')
            require(name not in names, f'Duplicate successful source: {name}')
            require(isinstance(record.get('bytes'), int) and record['bytes'] > 0,
                    f'Invalid byte count: {name}')
            require(len(record.get('sha256', '')) == 64, f'Missing source SHA256: {name}')
            names.add(name)
            records.append(record)
            successes += 1
        require(successes > 0, f'No acquired sources in {manifest_name}')
    require(len(records) == 17, f'Expected frozen inventory of 17 successful sources, got {len(records)}')
    cache = root / '_cache'
    cache.mkdir(exist_ok=True)
    for record in records:
        destination = cache / record['filename']
        if destination.exists() or destination.is_symlink():
            verify_source(destination, record)
    restored = []
    for record in records:
        destination = cache / record['filename']
        if destination.exists():
            continue
        handle, temporary = tempfile.mkstemp(prefix='.restore-', dir=cache)
        os.close(handle)
        temporary = Path(temporary)
        try:
            fetch(record['url'], temporary)
            verify_source(temporary, record)
            try:
                os.link(temporary, destination)
            except FileExistsError:
                verify_source(destination, record)
            else:
                restored.append(record['filename'])
        finally:
            temporary.unlink(missing_ok=True)
    receipt = verify_assets(root)
    return dict(restored=restored, verified_count=receipt['verified_count'],
                verified_bytes=receipt['verified_bytes'],
                failed_source_attempts=failed)


if __name__ == '__main__':
    print(json.dumps(restore(), indent=2))
