"""Verify pinned originals; --download restores missing files without replacing evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
def verified_bytes(name, download=False):
    sources = json.loads((ROOT/'sources.json').read_text())['sources']
    matches = [source for source in sources if source['name'] == name]
    if len(matches) != 1:
        raise ValueError(f'Missing or duplicate source: {name}')
    source = matches[0]
    if Path(name).name != name:
        raise ValueError(f'Unsafe source name: {name}')
    cache = ROOT/'_cache'
    cache.mkdir(exist_ok=True)
    path = cache/name
    if path.exists():
        data = path.read_bytes()
    elif download:
        with urllib.request.urlopen(source['url'], timeout=120) as response:
            data = response.read()
    else:
        raise FileNotFoundError(path)
    if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
        raise ValueError(f'Source changed or incomplete: {name}; retain as a new snapshot')
    try:
        with path.open('xb') as out:
            out.write(data)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ValueError(f'Concurrent source mismatch: {name}')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    sources = json.loads((ROOT/'sources.json').read_text())['sources']
    if not sources:
        raise ValueError('Empty source manifest')
    for source in sources:
        data = verified_bytes(source['name'], args.download)
        print(f"Verified {source['name']}: {len(data)} bytes")
    print(f'PASS: {len(sources)} pinned sources')
