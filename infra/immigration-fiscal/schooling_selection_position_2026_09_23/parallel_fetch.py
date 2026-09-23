"""Finish an IPUMS extract download with parallel byte-range requests.

IPUMS served extract #3 at roughly 15-20 KB/s per connection on 2026-09-23 (40 MB file), but
honours Range requests (206). This resumes from an existing .part file and fetches the rest in
parallel chunks, then verifies the total size and gzip integrity before renaming.

  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/parallel_fetch.py usa 3 us_mexborn
  ... parallel_fetch.py usa 3 us_mexborn --manifest-only    (re-verify an existing file, rewrite its manifest)

The finished file must match the sha256 IPUMS publishes for the extract.
"""
import gzip
import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ipums_api as api  # noqa: E402


def total_size(url: str) -> int:
    with requests.get(url, headers={"Authorization": api.api_key(), "Range": "bytes=0-0"}, stream=True,
                      timeout=(30, 60)) as r:
        return int(r.headers["Content-Range"].rsplit("/", 1)[1])


def fetch_range(url: str, start: int, end: int, path: Path) -> Path:
    for attempt in range(1, 20):
        have = path.stat().st_size if path.exists() else 0
        if start + have > end:
            return path
        try:
            with requests.get(url, headers={"Authorization": api.api_key(), "Range": f"bytes={start + have}-{end}"},
                              stream=True, timeout=(30, 120)) as r:
                if r.status_code != 206:
                    raise RuntimeError(f"status {r.status_code}")
                with open(path, "ab") as f:
                    for chunk in r.iter_content(chunk_size=1 << 16):
                        f.write(chunk)
        except Exception:  # noqa: BLE001 - retry any transport failure
            time.sleep(min(30, 3 * attempt))
    if path.stat().st_size != end - start + 1:
        raise SystemExit(f"[FAILED] chunk {start}-{end}")
    return path


def write_manifest(coll: str, number: int, name: str, info: dict) -> None:
    target = api.CACHE / f"{name}.data.csv.gz"
    h = hashlib.sha256(target.read_bytes()).hexdigest()
    published = info["downloadLinks"]["data"].get("sha256")
    if published and h != published:
        raise SystemExit(f"[FAILED] {target.name} sha256 {h[:16]} != IPUMS {published[:16]}")
    spec = info.get("extractDefinition", {})
    (api.CACHE / f"{name}.manifest.json").write_text(json.dumps({
        "collection": coll, "extract_number": number, "samples": sorted(spec.get("samples", {})),
        "variables": sorted(spec.get("variables", {})), "bytes": target.stat().st_size, "sha256": h,
        "sha256_matches_ipums": bool(published), "verified": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, indent=2))
    print(f"ok {target} {target.stat().st_size} bytes sha256 {h[:16]}")


def main() -> None:
    coll, number, name = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    info = api.status(coll, number)
    if "--manifest-only" in sys.argv:
        write_manifest(coll, number, name, info)
        return
    nchunks = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    url = info["downloadLinks"]["data"]["url"]
    size = total_size(url)
    part = api.CACHE / f"{name}.data.csv.gz.part"
    have = part.stat().st_size if part.exists() else 0
    step = (size - have + nchunks - 1) // nchunks
    ranges = [(s, min(size - 1, s + step - 1)) for s in range(have, size, step)]
    chunk_paths = [api.CACHE / f"{name}.chunk{i:02d}" for i in range(len(ranges))]
    print(f"size {size}, have {have}, fetching {len(ranges)} chunks", flush=True)
    with ThreadPoolExecutor(len(ranges)) as ex:
        list(ex.map(lambda a: fetch_range(url, a[0][0], a[0][1], a[1]), zip(ranges, chunk_paths)))
    with open(part, "ab") as out:
        for p in chunk_paths:
            out.write(p.read_bytes())
    if part.stat().st_size != size:
        raise SystemExit(f"[FAILED] assembled {part.stat().st_size} != {size}")
    with gzip.open(part, "rb") as g:  # integrity: must decompress end to end
        while g.read(1 << 24):
            pass
    target = api.CACHE / f"{name}.data.csv.gz"
    part.replace(target)
    for p in chunk_paths:
        p.unlink()
    write_manifest(coll, number, name, info)


if __name__ == "__main__":
    main()
