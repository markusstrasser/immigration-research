"""Regression probes for missing account coverage and concurrent source corruption."""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

SRC = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root/'_cache').mkdir()
    for name in ['probe_sf133.py', 'acquire.py', 'sources.json']:
        shutil.copyfile(SRC/name, root/name)
    shutil.copyfile(SRC/'_cache'/'dhs_fy2024_fileab.zip', root/'_cache'/'dhs_fy2024_fileab.zip')
    member = 'FY2024_XML_SF133_Department_of_Homeland_Security.xml'
    with zipfile.ZipFile(SRC/'_cache'/'dhs_sf133_2024.zip') as archive:
        xml = ET.fromstring(archive.read(member))
    for parent in xml.iter():
        for child in list(parent):
            if child.tag == 'treasury-account' and child.get('treasury-account-code') != '5382':
                parent.remove(child)
    changed = root/'_cache'/'dhs_sf133_2024.zip'
    with zipfile.ZipFile(changed, 'w') as archive:
        archive.writestr(member, ET.tostring(xml))
    def expect_failure(fragment):
        result = subprocess.run([sys.executable, '-O', str(root/'probe_sf133.py')], capture_output=True, text=True)
        if result.returncode == 0 or fragment not in result.stderr:
            raise RuntimeError(f'Expected {fragment}: {result}')
    expect_failure('Source changed or incomplete')
    manifest = json.loads((root/'sources.json').read_text())
    for row in manifest['sources']:
        if row['name'] == changed.name:
            row.update(bytes=changed.stat().st_size, sha256=hashlib.sha256(changed.read_bytes()).hexdigest())
    (root/'sources.json').write_text(json.dumps(manifest))
    expect_failure('Missing selected ICE account coverage')

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root/'_cache').mkdir()
    shutil.copyfile(SRC/'acquire.py', root/'acquire.py')
    source = json.loads((SRC/'sources.json').read_text())['sources'][0]
    (root/'sources.json').write_text(json.dumps({'sources': [source]}))
    data = (SRC/'_cache'/source['name']).read_bytes()
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            (root/'_cache'/source['name']).write_bytes(b'concurrent corrupted file')
            return data
    with patch.object(sys, 'argv', ['acquire.py', '--download']), patch.object(urllib.request, 'urlopen', return_value=Response()):
        try:
            runpy.run_path(str(root/'acquire.py'), run_name='__main__')
        except ValueError as error:
            if 'Concurrent source mismatch' not in str(error):
                raise
        else:
            raise RuntimeError('Concurrent corruption was silently accepted')
print('PASS: changed source, missing account and concurrent-corruption regressions')
