"""Restore two public CMS2022 inputs; fail closed on HTTP, content, or SHA drift."""
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
FILES = {
    'CSPUF2022_Data.zip': (
        'https://data.cms.gov/sites/default/files/2025-01/13f8f755-6533-4adf-a4cf-5ca29161231f/CSPUF2022_Data.zip',
        'd500832a0d832419f7c5ff23df56d91ee5348bc092d53f0dd7345e01fb699875'),
    'CSPUF2022_Codebook.txt': (
        'https://data.cms.gov/sites/default/files/2025-01/CSPUF2022_Codebook.txt',
        '7b7da7f5f7ded9c5c424e5cd3805c4580179d20c0574348e70af052bce71655e'),
}


def main():
    cache = LANE / '_cache'
    cache.mkdir(exist_ok=True)
    manifest = []
    for name, (url, expected) in FILES.items():
        path = cache / name
        if path.exists():
            data = path.read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise RuntimeError(f'[BLOCKED] {name}: source SHA drift {actual}')
        if name.endswith('.zip'):
            import io
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                if archive.testzip() is not None:
                    raise RuntimeError('[BLOCKED] corrupt archive')
        elif b'CSP_RACE' not in data or b'6,621' not in data:
            raise RuntimeError('[BLOCKED] codebook content invalid')
        if not path.exists():
            path.write_bytes(data)
        manifest.append(dict(filename=name, url=url, sha256=actual, bytes=len(data),
                             acquired='2026-09-28', publisher='CMS', access='public use'))
    (cache / 'acquisition_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Verified CMS2022 ZIP and codebook against retained pins.')


if __name__ == '__main__':
    main()
