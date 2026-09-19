"""Acquire the public October CPS release; never replace a pinned source silently."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
BASE = 'https://www2.census.gov/programs-surveys/cps/'
URLS = {
    'oct24pub.zip': BASE + 'datasets/2024/supp/oct24pub.zip',
    'oct24rep.zip': BASE + 'datasets/2024/supp/oct24rep.zip',
    'cpsoct24.pdf': BASE + 'techdocs/cpsoct24.pdf',
    'cps_school_repwgt_oct24.sas': BASE + 'datasets/2024/supp/cps_school_repwgt_oct24.sas',
}

def acquire(name, cache):
    path = cache / name
    partial = cache / (name + '.part')
    # Interrupted first acquisitions are not immutable raw sources. Keep and
    # resume the partial bytes, but never pin or parse an incomplete archive.
    if path.exists() and name.endswith('.zip') and not zipfile.is_zipfile(path):
        if partial.exists():
            raise ValueError('Two partial files require explicit reconciliation')
        path.rename(partial)
    if not path.exists():
        head = subprocess.run(['curl', '-I', '-L', '--fail', '--silent', '--show-error', '--max-time', '30', URLS[name]], capture_output=True, text=True, check=True)
        (cache / (name + '.headers')).write_text(head.stdout)
        subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--max-time', '600', '-C', '-', URLS[name], '-o', str(partial)], check=True)
        if name.endswith('.zip') and not zipfile.is_zipfile(partial):
            raise ValueError('Incomplete or non-ZIP source; not promoted')
        partial.rename(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(file=name, url=URLS[name], bytes=path.stat().st_size, sha256=digest)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', type=Path, default=HERE / '_cache')
    parser.add_argument('--pin', action='store_true', help='Explicitly create the first reviewed source lock')
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(lambda name: acquire(name, args.cache), URLS))
    lock = HERE / 'sources.json'
    if args.pin:
        if lock.exists():
            raise ValueError('Existing source lock: review drift instead of repinning')
        lock.write_text(json.dumps(dict(acquired='2026-09-20', landing='https://www.census.gov/data/datasets/2024/demo/cps/cps-school-enrollment.html', files=entries), indent=2) + '\n')
    expected = {r['file']: r['sha256'] for r in json.loads(lock.read_text())['files']}
    assert all(r['sha256'] == expected[r['file']] for r in entries), 'Source changed'
    (args.cache / 'ACQUIRED.md').write_text('\n'.join(f"2026-09-20 | {r['file']} | {r['url']} | {r['bytes']} bytes | sha256:{r['sha256']}" for r in entries) + '\n')
    print(json.dumps(entries, indent=2))

if __name__ == '__main__':
    main()
