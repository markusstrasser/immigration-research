"""Acquire public primary sources; raw downloads are immutable and hashed."""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, json, shutil, urllib.request, zipfile

SOURCES = {
 'asecpub24csv.zip':'https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asecpub24csv.zip',
 'asec2024_ddl_pub_full.pdf':'https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asec2024_ddl_pub_full.pdf',
 '2024_replicates.docx':'https://www2.census.gov/programs-surveys/cps/datasets/2024/march/2024_ASEC_Replicate_Weight_Usage_Instructions.docx',
 '23in12ms.xls':'https://www.irs.gov/pub/irs-soi/23in12ms.xls',
 '23in14ar.xls':'https://www.irs.gov/pub/irs-soi/23in14ar.xls',
 '22in12ms.xls':'https://www.irs.gov/pub/irs-soi/22in12ms.xls',
 '22in14ar.xls':'https://www.irs.gov/pub/irs-soi/22in14ar.xls',
 'p4801.pdf':'https://www.irs.gov/pub/irs-pdf/p4801.pdf',
}

def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def acquire(raw,source_root):
    raw.mkdir(parents=True,exist_ok=True)
    lock_path=Path(__file__).parent/'source_lock.json'
    lock=json.loads(lock_path.read_text()) if lock_path.exists() else {}
    def get(item):
        name,url=item; p=raw/name
        meta={}
        local=source_root/'sources/immigration-fiscal/data/census/cps_asec_2024_march.zip' if source_root and name=='asecpub24csv.zip' else None
        if local and local.exists():
            meta['existing_local_sha256']=sha(local)
            meta['existing_local_path']=str(local)
            if not p.exists(): shutil.copyfile(local,p)
        if not p.exists():
            request=urllib.request.Request(url,headers={'User-Agent':'research-public-source-check/1.0'})
            with urllib.request.urlopen(request,timeout=120) as r, p.with_suffix(p.suffix+'.part').open('wb') as f:
                meta={'last_modified':r.headers.get('Last-Modified'),'content_type':r.headers.get('Content-Type')}
                while b:=r.read(1024*1024): f.write(b)
            p.with_suffix(p.suffix+'.part').rename(p)
        if p.stat().st_size<1000: raise ValueError(f'Unexpectedly small source: {p}')
        digest=sha(p)
        if name in lock and digest!=lock[name]['sha256']: raise ValueError(f'Source changed: {name}')
        if meta.get('existing_local_sha256',digest)!=digest: raise ValueError('Local CPS archive differs from pinned source')
        if name.endswith('.zip'):
            with zipfile.ZipFile(p) as z:
                if z.testzip() is not None: raise ValueError('Corrupt source zip')
                meta['members']=z.namelist()
        return dict(name=name,url=url,bytes=p.stat().st_size,sha256=digest,**meta)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(get,SOURCES.items()))
    receipt={'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows}
    (raw/'acquisition.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--raw',type=Path,required=True); p.add_argument('--source-root',type=Path)
    args=p.parse_args(); acquire(args.raw,args.source_root)
