"""Bounded parallel HTTP ranges for INEGI's slow single-stream downloads."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parent
def require(condition,message):
 if not condition: raise ValueError(message)

year=int(sys.argv[1])
url=f'https://www.inegi.org.mx/contenidos/programas/enadid/{year}/datosabiertos/conjunto_de_datos_enadid_{year}_csv.zip'
out=ROOT/'_cache'/f'enadid_{year}_csv.zip'
pin=next(x for x in json.loads((ROOT/'sources.json').read_text())['files'] if x['filename']==out.name)
require(pin['url']==url,'URL differs from frozen manifest')
if out.exists():
 require(hashlib.sha256(out.read_bytes()).hexdigest()==pin['sha256'],'Existing archive differs from frozen hash; preserved')
 print(f'{year}: existing archive verified; no download')
 raise SystemExit(0)
with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=45) as r:
 size=int(r.headers['Content-Length'])
 headers=dict(r.headers)
parts=ROOT/'_cache'/'ranges'/str(year)
parts.mkdir(parents=True,exist_ok=True)

def get_range(bounds):
 lo,hi=bounds
 path=parts/f'{lo}-{hi}'
 if path.exists() and path.stat().st_size==hi-lo+1: return path
 req=urllib.request.Request(url,headers={'Range':f'bytes={lo}-{hi}'})
 with urllib.request.urlopen(req,timeout=180) as r:
  require(r.status==206,f'Expected206, got{r.status}')
  require(r.headers['Content-Range']==f'bytes {lo}-{hi}/{size}','Unexpected Content-Range')
  with path.open('wb') as f:
   while chunk:=r.read(1024*1024): f.write(chunk)
 require(path.stat().st_size==hi-lo+1,'Wrong range byte length')
 print(f'{year}: range {lo}-{hi} verified',flush=True)
 return path

step=2*1024*1024
bounds=[(lo,min(lo+step-1,size-1)) for lo in range(0,size,step)]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 paths=list(pool.map(get_range,bounds))
partial=out.with_name(f'.{out.name}.{uuid.uuid4().hex}.part')
with partial.open('xb') as f:
 for p in paths: f.write(p.read_bytes())
require(partial.stat().st_size==size,'Wrong assembled byte length')
require(hashlib.sha256(partial.read_bytes()).hexdigest()==pin['sha256'],'Downloaded archive differs from frozen hash; partial preserved')
with zipfile.ZipFile(partial) as z:
 require(z.testzip() is None,'ZIP CRC failure')
 members=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size} for i in z.infolist()]
os.link(partial,out)  # Preserve any concurrently installed completed archive.
partial.unlink()
record={'filename':out.name,'url':url,'head_status':200,'head_headers':headers,'bytes':size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':members,'range_count':len(bounds),'range_status':206,'status':'verified_download'}
(ROOT/f'manifest_range_{year}.json').write_text(json.dumps(record,indent=2))
out.chmod(0o444)
print(f'{year}: {size} bytes verified; sha256={record["sha256"]}',flush=True)
