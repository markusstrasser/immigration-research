"""Acquire pinned official CMS inputs; never overwrite an existing raw file."""
from pathlib import Path
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent


def acquire():
    pins = json.loads((HERE / 'source_pins.json').read_text())
    raw = HERE / 'raw'
    raw.mkdir(exist_ok=True)
    for item in pins['files']:
        path = raw / item['name']
        if not path.exists():
            payload = item.get('post_json')
            request = urllib.request.Request(item['url'],
                data=json.dumps(payload).encode() if payload else None,
                headers={'Content-Type': 'application/json'} if payload else {})
            with urllib.request.urlopen(request, timeout=90) as response:
                content = response.read()
            if hashlib.sha256(content).hexdigest() != item['sha256']:
                raise RuntimeError(f'Published source changed: {item["url"]}; do not overwrite the pin')
            path.write_bytes(content)
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError(f'Existing raw file fails source pin: {path}')
        print(item['name'], path.stat().st_size, 'verified')


if __name__ == '__main__':
    acquire()
