"""Offline regression tests: selection and no-overwrite across both downloaders.

Copy into ENADID lane as test_acquisition.py, or pass --lane /path/to/lane.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import io
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.request
import zipfile

parser=argparse.ArgumentParser(add_help=False)
parser.add_argument('--lane',type=Path,default=Path(__file__).resolve().parent)
ARGS,TEST_ARGS=parser.parse_known_args()
LANE=ARGS.lane
PEER=b'concurrently completed peer source; preserve this evidence'

class AcquisitionTests(unittest.TestCase):
    def fixture(self,root,archive=False):
        for name in ['acquire.py','range_download.py']:
            shutil.copyfile(LANE/name,root/name)
        (root/'_cache').mkdir()
        if archive:
            stream=io.BytesIO()
            with zipfile.ZipFile(stream,'w') as z:
                z.writestr('sample.csv','field\nvalue\n')
            payload=stream.getvalue()
            name='enadid_2023_csv.zip'
            url='https://www.inegi.org.mx/contenidos/programas/enadid/2023/datosabiertos/conjunto_de_datos_enadid_2023_csv.zip'
        else:
            payload=b'%PDF- frozen source bytes'
            name='hogar_enadid18.pdf'
            url='https://www.inegi.org.mx/contenidos/programas/enadid/2018/doc/hogar_enadid18.pdf'
        pin=dict(filename=name,url=url,sha256=hashlib.sha256(payload).hexdigest(),
                 bytes=len(payload),status='verified_download')
        (root/'sources.json').write_text(json.dumps(dict(files=[pin])))
        return name,url,payload

    def fake_fetch(self,destination,url,payload,ranged=False):
        class Response(io.BytesIO):
            def __init__(self,data,status,headers,interleave=False):
                super().__init__(data)
                self.status,self.headers,self.url=status,headers,url
                self.interleave=interleave
            def read(self,*args):
                if self.interleave:
                    destination.write_bytes(PEER)
                    self.interleave=False
                return super().read(*args)
        def open_source(request,timeout):
            if isinstance(request,urllib.request.Request) and request.get_method()=='HEAD':
                return Response(b'',200,{'Content-Length':str(len(payload))})
            headers={'Content-Range':f'bytes 0-{len(payload)-1}/{len(payload)}'} if ranged else {}
            return Response(payload,206 if ranged else 200,headers,True)
        return open_source

    def test_unknown_selection_rejected_under_optimization(self):
        with tempfile.TemporaryDirectory(prefix='enadid-selection-') as d:
            root=Path(d)
            self.fixture(root)
            result=subprocess.run([sys.executable,'-O',str(root/'acquire.py'),'typo-source.zip'],
                                  capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0,'Unknown selection returned success')
            self.assertFalse((root/'manifest_extra.json').exists(),'Empty acquisition receipt published')

    def test_standard_download_preserves_concurrent_destination(self):
        with tempfile.TemporaryDirectory(prefix='enadid-standard-race-') as d:
            root=Path(d)
            name,url,payload=self.fixture(root)
            spec=importlib.util.spec_from_file_location('isolated_enadid_acquisition',root/'acquire.py')
            module=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            destination=root/'_cache'/name
            with patch('urllib.request.urlopen',self.fake_fetch(destination,url,payload)):
                receipt=module.fetch((name,url))
            self.assertEqual(destination.read_bytes(),PEER,'Concurrent source overwritten')
            self.assertEqual(receipt['status'],'failed','Mismatch did not fail acquisition')

    def test_range_download_preserves_concurrent_destination(self):
        with tempfile.TemporaryDirectory(prefix='enadid-range-race-') as d:
            root=Path(d)
            name,url,payload=self.fixture(root,archive=True)
            destination=root/'_cache'/name
            with patch('urllib.request.urlopen',self.fake_fetch(destination,url,payload,True)), \
                 patch.object(sys,'argv',['range_download.py','2023']):
                with self.assertRaises((ValueError,FileExistsError)):
                    runpy.run_path(str(root/'range_download.py'),run_name='__main__')
            self.assertEqual(destination.read_bytes(),PEER,'Concurrent source overwritten')

if __name__=='__main__':
    unittest.main(argv=[sys.argv[0],*TEST_ARGS])
