"""Offline regression checks: valid binary PDF versus HTML disguised as a PDF."""
import io
import json
import runpy
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

script=Path(__file__).with_name('acquire.py')
class Response(io.BytesIO):
    url='https://example.invalid/source.pdf'

for payload, success in [(b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n',True),(b'<html>Preparing to download</html>',False)]:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); mapping=root/'urls.json'; mapping.write_text(json.dumps({'sample.pdf':Response.url}))
        output=root/'snapshot'; exited=False
        with patch.object(sys,'argv',[str(script),'--output-dir',str(output),'--urls-json',str(mapping)]), patch('urllib.request.urlopen',return_value=Response(payload)), redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(str(script),run_name='__main__')
            except SystemExit:
                exited=True
        log=json.loads((output/'acquisition.json').read_text())
        assert len(log)==1 and ('error' not in log[0])==success
        assert exited != success
        assert (output/'sample.pdf').exists()==success
        if success:assert (output/'sample.pdf').read_bytes()==payload
        else:assert (output/'sample.pdf.unexpected-response.html').read_bytes()==payload
print('PASS: binary PDF succeeds once; HTML-as-PDF fails loudly; no network used')
