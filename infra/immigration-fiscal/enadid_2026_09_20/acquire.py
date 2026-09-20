import concurrent.futures
import datetime
import hashlib
import json
import os
import sys
import uuid
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
CACHE = ROOT/'_cache'
CACHE.mkdir(exist_ok=True)
PINNED={x['filename']:x for x in json.loads((ROOT/'sources.json').read_text())['files']}
BASE = 'https://www.inegi.org.mx/'
URLS = {
 'enadid_2018_csv.zip': BASE+'contenidos/programas/enadid/2018/datosabiertos/conjunto_de_datos_enadid_2018_csv.zip',
 'hogar_enadid18.pdf': BASE+'contenidos/programas/enadid/2018/doc/hogar_enadid18.pdf',
 'metadata2023.xml': BASE+'rnm/index.php/metadata/export/981/ddi',
 'metadata2018.xml': BASE+'rnm/index.php/metadata/export/554/ddi',
 'diseno_muestral_enadid23.pdf': BASE+'contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463916413.pdf',
 'enadid_2023_csv.zip': BASE+'contenidos/programas/enadid/2023/datosabiertos/conjunto_de_datos_enadid_2023_csv.zip',
 'hogar_enadid23.pdf': BASE+'contenidos/programas/enadid/2023/doc/hogar_enadid23.pdf',
 'manual_conceptual_enadid23.pdf': BASE+'contenidos/programas/enadid/2023/doc/manual_conceptual_enadid23.pdf',
 'resultados_enadid23.pdf': BASE+'contenidos/programas/enadid/2023/doc/resultados_enadid23.pdf',
 'terminos.html': BASE+'inegi/terminos.html',
 'tmigrante2023_metadata.html': BASE+'rnm/index.php/catalog/981/data-dictionary/F18',
 'enadid2023_catalog.html': BASE+'rnm/index.php/catalog/981',
}

def fetch(item):
 name,url=item
 dst=CACHE/name
 info={'filename':name,'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  pin=PINNED[name]
  if url!=pin['url']: raise ValueError('URL differs from frozen source manifest')
  if dst.exists():
   if hashlib.sha256(dst.read_bytes()).hexdigest()!=pin['sha256']: raise ValueError('Cached source differs from frozen hash')
   return dict(pin,cache_verified=True)
  with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'),timeout=60) as r:
   info['head_status']=r.status
   info['head_headers']=dict(r.headers)
  if not dst.exists():
   partial=dst.with_name(f'.{dst.name}.{uuid.uuid4().hex}.part')
   with urllib.request.urlopen(url,timeout=180) as r, partial.open('xb') as out:
    info['get_status']=r.status
    info['final_url']=r.url
    info['get_headers']=dict(r.headers)
    while chunk:=r.read(1024*1024): out.write(chunk)
   if hashlib.sha256(partial.read_bytes()).hexdigest()!=pin['sha256']: raise ValueError('Downloaded bytes differ from frozen hash; partial preserved')
   os.link(partial,dst)  # Fail if another writer installed a completed file.
   partial.unlink()
  info['bytes']=dst.stat().st_size
  info['sha256']=hashlib.sha256(dst.read_bytes()).hexdigest()
  if info['sha256']!=pin['sha256']: raise ValueError('Completed source differs from frozen hash')
  if name.endswith('.zip'):
   with zipfile.ZipFile(dst) as z:
    info['zip_test_error']=z.testzip()
    if info['zip_test_error'] is not None: raise ValueError('ZIP CRC failure')
    info['members']=[{'name':m.filename,'bytes':m.file_size,'compressed_bytes':m.compress_size} for m in z.infolist()]
  elif name.endswith('.pdf'):
   if dst.read_bytes()[:5]!=b'%PDF-': raise ValueError('Not PDF bytes')
  info['status']='verified_download'
  dst.chmod(0o444)
 except Exception as e:
  info['status']='failed'
  info['error']=repr(e)
 print(json.dumps({k:v for k,v in info.items() if k in ['filename','status','bytes','error']}),flush=True)
 return info

if __name__=='__main__':
 unknown=set(sys.argv[1:])-set(URLS)
 if unknown: raise SystemExit(f'Unknown source names: {sorted(unknown)}')
 selected={k:v for k,v in URLS.items() if not sys.argv[1:] or k in sys.argv[1:]}
 if not selected: raise SystemExit('No sources selected')
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  rows=list(pool.map(fetch,selected.items()))
 manifest=ROOT/('manifest_extra.json' if sys.argv[1:] else 'manifest.json')
 manifest.write_text(json.dumps(rows,indent=2))
 if any(r['status']=='failed' for r in rows): raise SystemExit(1)
