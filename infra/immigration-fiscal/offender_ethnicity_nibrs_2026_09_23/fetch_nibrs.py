"""Fetch FBI NIBRS incident files by state and the UCR participation file from the CDE store.

    uv run --no-project python3 fetch_nibrs.py participation TX-2022 TX-2023 AZ-2022 AZ-2023 CA-2022 CA-2023

Keys follow the Crime Data Explorer signed-URL store, `nibrs/incident/{year}/{ST}-{year}.zip`
(the layout of the 2025-02-08 archive.org mirror `fbi-cde`, confirmed live 2026-09-23). No API
key is needed for the store. Disk preflight before every download: the file must leave at least
1.5x its size free on the destination, else the script stops with dest/free/need. Files arrive in
8 MB ranges over parallel connections, each range on a freshly signed URL (signatures last 900 s;
one connection ran at 30-550 KB/s). Each file's size and sha256 go to derived/source_manifest.csv
as soon as it lands.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
MANIFEST = HERE / "derived/source_manifest.csv"
STORE = "https://cde.ucr.cjis.gov/LATEST/s3/signedurl?key="
PARTICIPATION = "additional-datasets/ucr/ucr_participation_1960_2025.csv"
CHUNK = 8 << 20
WORKERS = 6


def signed(key: str) -> str:
    with urllib.request.urlopen(STORE + urllib.parse.quote(key, safe="/"), timeout=120) as r:
        d = json.loads(r.read())
    if key not in d:
        raise SystemExit(f"[BLOCKED] CDE store has no object {key} (response {d})")
    return d[key]


def get_range(key: str, lo: int, hi: int, tries: int = 4) -> bytes:
    for t in range(tries):
        try:
            req = urllib.request.Request(signed(key), headers={"Range": f"bytes={lo}-{hi}"})
            with urllib.request.urlopen(req, timeout=300) as r:
                b = r.read()
            if len(b) == hi - lo + 1:
                return b
        except OSError as e:
            print(f"  range {lo}-{hi} try {t + 1} failed: {type(e).__name__}", flush=True)
    raise SystemExit(f"[BLOCKED] {key}: range {lo}-{hi} failed {tries} times")


def remote_size(key: str) -> int:
    req = urllib.request.Request(signed(key), headers={"Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return int(r.headers["Content-Range"].split("/")[-1])


def preflight(size: int) -> None:
    free = shutil.disk_usage(CACHE).free
    if free - size < 1.5 * size:
        raise SystemExit(f"[BLOCKED] dest={CACHE} free={free / 1e9:.2f} GB need={2.5 * size / 1e9:.2f} GB")
    print(f"  preflight ok: free {free / 1e9:.1f} GB, file {size / 1e6:.1f} MB", flush=True)


def fetch(key: str) -> dict:
    dest = CACHE / Path(key).name
    size = remote_size(key)
    if dest.exists() and dest.stat().st_size == size:
        print(f"  cached {dest.name} ({size / 1e6:.1f} MB)", flush=True)
    else:
        preflight(size)
        spans = [(lo, min(lo + CHUNK, size) - 1) for lo in range(0, size, CHUNK)]
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as f:
            f.truncate(size)
        done = 0
        with ThreadPoolExecutor(WORKERS) as ex, open(tmp, "r+b") as f:
            for (lo, hi), b in zip(spans, ex.map(lambda s: get_range(key, *s), spans)):
                f.seek(lo)
                f.write(b)
                done += 1
                if done % 4 == 0 or done == len(spans):
                    print(f"  [{done}/{len(spans)}] {dest.name}", flush=True)
        tmp.rename(dest)
        print(f"  downloaded {dest.name} ({size / 1e6:.1f} MB)", flush=True)
    if dest.suffix == ".zip":
        with zipfile.ZipFile(dest) as z:
            bad = z.testzip()
            if bad:
                raise SystemExit(f"[BLOCKED] {dest.name}: corrupt member {bad}")
    h = hashlib.sha256(dest.read_bytes()).hexdigest()
    return dict(key=key, file=dest.name, bytes=size, sha256=h, fetched=date.today().isoformat(),
                url=STORE + key)


def fetch_agency_list(st: str) -> dict:
    """Every agency in the state, NIBRS or not, with its counties (CDE agency endpoint, no key).
    Sheriffs' residual jurisdictions subtract all city agencies, reporting or not."""
    url = f"https://cde.ucr.cjis.gov/LATEST/agency/byStateAbbr/{st}"
    dest = CACHE / f"cde_agencies_{st}.json"
    if not (dest.exists() and dest.stat().st_size > 1000):
        with urllib.request.urlopen(url, timeout=300) as r:
            body = r.read()
        json.loads(body)
        dest.write_bytes(body)
    b = dest.read_bytes()
    print(f"  {dest.name} ({len(b) / 1e3:.0f} kB)", flush=True)
    return dict(key=f"agency/byStateAbbr/{st}", file=dest.name, bytes=len(b),
                sha256=hashlib.sha256(b).hexdigest(), fetched=date.today().isoformat(), url=url)


def write_manifest(rows: dict) -> None:
    with MANIFEST.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["key", "file", "bytes", "sha256", "fetched", "url"])
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: r["key"]))


def main(args: list[str]) -> None:
    CACHE.mkdir(exist_ok=True)
    MANIFEST.parent.mkdir(exist_ok=True)
    rows = {r["key"]: r for r in csv.DictReader(MANIFEST.open())} if MANIFEST.exists() else {}
    for a in args:
        if a.startswith("agencies-"):
            r = fetch_agency_list(a.split("-")[1])
            rows[r["key"]] = r
        else:
            key = PARTICIPATION if a == "participation" else "nibrs/incident/{1}/{0}-{1}.zip".format(*a.split("-"))
            print(f"[fetch] {key}", flush=True)
            rows[key] = fetch(key)
        write_manifest(rows)


if __name__ == "__main__":
    main(sys.argv[1:])
