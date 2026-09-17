"""Public primary-source discovery; no credentials or account-gated access."""
import argparse, hashlib, json, urllib.request
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--output-dir', type=Path, required=True, help='New directory for this immutable access snapshot')
p.add_argument('--urls-json', type=Path, help='Optional JSON mapping filenames to public URLs')
a = p.parse_args()
a.output_dir.mkdir(parents=True, exist_ok=True)
if any(a.output_dir.iterdir()):
    raise SystemExit('Refusing to overwrite an existing snapshot; choose an empty output directory')
urls = {
    'dataverse_search.json': 'https://dataverse.harvard.edu/api/search?q=Naturalization&type=dataset&per_page=100',
    'author_publications.html': 'https://j-hai.github.io/publications/',
    'pnas_main.html': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4611668/',
    'pnas_supplement.pdf': 'https://pmc.ncbi.nlm.nih.gov/articles/instance/4611668/bin/pnas.1418794112.sapp.pdf',
}
if a.urls_json:
    urls=json.loads(a.urls_json.read_text())
def valid_payload(name,b):
    return not name.endswith('.pdf') or b.startswith(b'%PDF-')
assert not valid_payload('test.pdf',b'<html>Preparing to download ...</html>')
assert valid_payload('test.pdf',b'%PDF-1.7')
log=[]
for name,url in urls.items():
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            b=r.read()
            if not valid_payload(name,b):
                blocked_name=name+'.unexpected-response.html'
                (a.output_dir/blocked_name).write_bytes(b)
                raise ValueError('Expected PDF magic; saved unexpected response as '+blocked_name)
            (a.output_dir/name).write_bytes(b)
            log.append(dict(file=name,url=url,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
        if name.endswith('.json'):
            j=json.loads(b)
            for v in j.get('data',{}).get('items',[]):
                print(v.get('name'), v.get('global_id'), v.get('url'))
        elif name.endswith(('.html','.htm')):
            import re
            print(name,[(x[:200]) for x in re.findall(r'href="([^"]+)"',b.decode()) if any(s in x.lower() for s in ['sapp','replicat','dataverse','data.zip'])])
    except Exception as e:
        log.append(dict(file=name,url=url,error=str(e)))
        print(name,repr(e))
(a.output_dir/'acquisition.json').write_text(json.dumps(log,indent=2)+'\n')
if any('error' in x for x in log):
    raise SystemExit('DEGRADED: at least one primary-source retrieval failed; see acquisition.json')
