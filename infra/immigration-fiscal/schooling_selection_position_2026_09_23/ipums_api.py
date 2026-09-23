"""Minimal IPUMS API v2 client for this lane: probe access, submit, poll, download.

The key comes from IPUMS_API_KEY (source acquire/config.local.env with `set -a`) and is never
printed. Downloads land in this lane's `_cache/`, which is git-ignored; IPUMS microdata must not
leave it.

Usage, from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/ipums_api.py probe
"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
API = "https://api.ipums.org"


def api_key() -> str:
    key = os.environ.get("IPUMS_API_KEY", "")
    if not key:
        env = HERE.parent / "acquire" / "config.local.env"
        for line in env.read_text().splitlines() if env.exists() else []:
            if line.startswith("IPUMS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("[BLOCKED] IPUMS_API_KEY missing")
    return key


def call(method: str, path: str, **kw) -> requests.Response:
    r = requests.request(method, f"{API}{path}", headers={"Authorization": api_key()},
                         timeout=120, **kw)
    return r


def samples(collection: str) -> list[dict]:
    out, page = [], 1
    while True:
        r = call("GET", f"/metadata/{collection}/samples?version=2&pageSize=2500&pageNumber={page}")
        if r.status_code != 200:
            raise SystemExit(f"[BLOCKED] {collection} samples: {r.status_code} {r.text[:300]}")
        data = r.json()
        rows = data.get("data", [])
        out += rows
        if not data.get("links", {}).get("nextPage") or not rows:
            break
        page += 1
    return out


def submit(collection: str, body: dict) -> int:
    r = call("POST", f"/extracts?collection={collection}&version=2", json=body)
    if r.status_code >= 400:
        raise SystemExit(f"[FAILED] submit {collection}: {r.status_code} {r.text[:800]}")
    return int(r.json()["number"])


def status(collection: str, number: int) -> dict:
    r = call("GET", f"/extracts/{number}?collection={collection}&version=2")
    if r.status_code >= 400:
        raise SystemExit(f"[FAILED] status {collection} {number}: {r.status_code} {r.text[:300]}")
    return r.json()


def wait(collection: str, number: int, max_seconds: int, poll: int = 60) -> str:
    started = time.time()
    while True:
        st = status(collection, number).get("status")
        print(f"  extract {collection}#{number}: {st} ({int(time.time() - started)}s)", flush=True)
        if st in ("completed", "failed", "canceled"):
            return st
        if time.time() - started > max_seconds:
            return st
        time.sleep(poll)


def download(collection: str, number: int, name: str) -> Path:
    info = status(collection, number)
    if info.get("status") != "completed":
        raise SystemExit(f"[BLOCKED] {collection}#{number} is {info.get('status')}")
    CACHE.mkdir(exist_ok=True)
    links = info["downloadLinks"]
    out = None
    for kind, meta in links.items():
        url = meta["url"] if isinstance(meta, dict) else None
        if not url:
            continue
        target = CACHE / f"{name}.{kind}{''.join(Path(url.split('?')[0]).suffixes[-2:])}"
        tmp = target.with_name(target.name + ".part")
        for attempt in range(1, 9):
            have = tmp.stat().st_size if tmp.exists() else 0
            headers = {"Authorization": api_key()}
            if have:
                headers["Range"] = f"bytes={have}-"
            try:
                with requests.get(url, headers=headers, stream=True, timeout=(30, 180)) as r:
                    if have and r.status_code != 206:
                        tmp.unlink()
                        continue
                    r.raise_for_status()
                    total = r.headers.get("Content-Range", "").rsplit("/", 1)[-1] or r.headers.get("Content-Length")
                    with open(tmp, "ab") as f:
                        for chunk in r.iter_content(chunk_size=1 << 20):
                            f.write(chunk)
                if total and total.isdigit() and tmp.stat().st_size != int(total):
                    continue
                break
            except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                time.sleep(min(60, 5 * attempt))
        else:
            raise SystemExit(f"[FAILED] download {kind} of {collection}#{number}")
        tmp.replace(target)
        if kind == "data":
            out = target
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    (CACHE / f"{name}.manifest.json").write_text(json.dumps({
        "collection": collection, "extract_number": number, "samples": sorted(info.get("samples", {})),
        "variables": sorted(info.get("variables", {})), "bytes": out.stat().st_size, "sha256": h,
        "downloaded": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, indent=2))
    return out


def probe() -> None:
    for coll in ("ipumsi", "usa"):
        r = call("GET", f"/metadata/{coll}/samples?version=2&pageSize=5&pageNumber=1")
        detail = r.text[:200] if r.status_code != 200 else f"{r.json().get('totalCount', '?')} samples"
        print(f"{coll}: HTTP {r.status_code} {detail}")


if __name__ == "__main__":
    if sys.argv[1:] == ["probe"]:
        probe()
