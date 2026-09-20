"""Test restoration with local fixtures and no network or source mutation."""
from pathlib import Path
import json
import shutil
import tempfile

import restore as restorer

SOURCE = restorer.ROOT
TARGET = 'CSPUF2023_Data.zip'


def stage(root):
    (root / '_cache').mkdir()
    for name in restorer.MANIFESTS:
        shutil.copy2(SOURCE / name, root / name)
    for path in (SOURCE / '_cache').iterdir():
        if path.is_file():
            (root / '_cache' / path.name).symlink_to(path)


results = []
for case in ['valid missing restore', 'bad download', 'corrupt existing']:
    with tempfile.TemporaryDirectory(prefix='fiscal-restore-', dir='/private/tmp') as directory:
        root = Path(directory)
        stage(root)
        manifests_before = [(root / name).read_bytes() for name in restorer.MANIFESTS]
        target = root / '_cache' / TARGET
        target.unlink()
        if case == 'corrupt existing':
            target.write_bytes(b'corrupt-existing-do-not-overwrite')
        calls = []

        def fetch(url, destination):
            calls.append(url)
            if case == 'bad download':
                destination.write_bytes(b'wrong-vintage')
            else:
                shutil.copyfile(SOURCE / '_cache' / TARGET, destination)

        try:
            receipt = restorer.restore(root, fetch=fetch)
        except ValueError:
            if case == 'valid missing restore':
                raise
        else:
            if case != 'valid missing restore':
                raise RuntimeError(f'{case} unexpectedly passed')
            restorer.require(receipt['restored'] == [TARGET] and receipt['verified_count'] == 17,
                             'Missing-file restoration receipt incorrect')
        restorer.require(manifests_before == [(root / name).read_bytes() for name in restorer.MANIFESTS],
                         'Frozen manifest was modified')
        if case == 'bad download':
            restorer.require(not target.exists(), 'Invalid downloaded bytes installed')
        elif case == 'corrupt existing':
            restorer.require(not calls and target.read_bytes() == b'corrupt-existing-do-not-overwrite',
                             'Existing mismatched bytes overwritten or network called')
        restorer.require(not list((root / '_cache').glob('.restore-*')), 'Temporary download leaked')
        results.append(dict(case=case, passed=True))
(SOURCE / 'derived' / 'restore_checks.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
