"""Regression checks for fail-closed evidence verification, including optimized Python."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from acquire_sources import acquire
from source_contract import load_manifest,verify

ROOT=Path(__file__).resolve().parent

class ContractTests(unittest.TestCase):
    def test_publication_preserves_concurrent_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            source=root/'held'
            source.mkdir()
            (source/'input').write_bytes(b'valid')
            destination=root/'_cache/input'
            record=dict(file='input',local_file='_cache/input',source_path='input',
                        bytes=5,sha256=hashlib.sha256(b'valid').hexdigest())
            real_copy=shutil.copyfile
            def concurrent_copy(src,tmp):
                real_copy(src,tmp)
                destination.write_bytes(b'peer evidence')
            with patch('acquire_sources.load_manifest',return_value=[record]), \
                 patch('acquire_sources.shutil.copyfile',side_effect=concurrent_copy):
                with self.assertRaises(FileExistsError):
                    acquire(root,source_repo=source,offline=True)
            self.assertEqual(destination.read_bytes(),b'peer evidence')

    def test_empty_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'manifest.json').write_text('[]')
            with self.assertRaisesRegex(ValueError,'nonempty'):
                load_manifest(root)

    def test_missing_principal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            records=json.loads((ROOT/'manifest.json').read_text())
            (root/'manifest.json').write_text(json.dumps(records[:1]))
            with self.assertRaisesRegex(ValueError,'principal'):
                load_manifest(root)

    def test_corrupt_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'input'
            path.write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError,'SHA256'):
                verify(path,dict(bytes=3,sha256=hashlib.sha256(b'yes').hexdigest()))

    def test_optimized_probe_rejects_empty_and_missing_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ['probe.py','source_contract.py']:
                shutil.copyfile(ROOT/name,root/name)
            (root/'manifest.json').write_text('[]')
            missing=subprocess.run([sys.executable,'-O',str(root/'probe.py')],capture_output=True,text=True)
            self.assertNotEqual(missing.returncode,0)
            self.assertIn('Required _cache',missing.stderr)
            (root/'_cache').mkdir()
            empty=subprocess.run([sys.executable,'-O',str(root/'probe.py')],capture_output=True,text=True)
            self.assertNotEqual(empty.returncode,0)
            self.assertIn('nonempty list',empty.stderr)

if __name__=='__main__':
    unittest.main()
