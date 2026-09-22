#!/usr/bin/env python3
"""Submit, wait for and download the IPUMS-CPS ASEC extract that `build/load_cps_second_gen.py`
expects at <data_root>/external/cps/cps_2ndgen.csv.gz (recipe: research/immigration-gated-data-specs-2026-06-25.md §1).

The key is read from IPUMS_API_KEY in the environment or from acquire/config.local.env and is
never printed. Requires the account to hold an IPUMS CPS registration (the API answers 401
"not registered to IPUMS cps" otherwise).

Usage, from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/acquire/ipums_cps_second_gen.py run          # submit, wait, download
  uv run --no-project python3 infra/immigration-fiscal/acquire/ipums_cps_second_gen.py submit
  uv run --no-project python3 infra/immigration-fiscal/acquire/ipums_cps_second_gen.py status --number N
  uv run --no-project python3 infra/immigration-fiscal/acquire/ipums_cps_second_gen.py download --number N
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "build"))
from paths import data_root  # noqa: E402

API = "https://api.ipums.org"
COLLECTION = "cps"
DESCRIPTION = "immigration-research cps_2ndgen: ASEC 1994+, parental birthplace and outcomes (V02)"
FIRST_YEAR = 1994
VARIABLES = ["BPL", "FBPL", "MBPL", "NATIVITY", "CITIZEN", "YRIMMIG", "AGE", "SEX", "RACE", "HISPAN",
             "MARST", "EDUC", "EMPSTAT", "LABFORCE", "INCTOT", "INCWAGE", "UHRSWORKLY", "WKSWORK1",
             "NCHILD", "YNGCH", "ASECWT"]
POLL_SECONDS = 45
MAX_WAIT_SECONDS = 4 * 3600


def api_key() -> str:
    key = os.environ.get("IPUMS_API_KEY", "")
    env = HERE / "config.local.env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("IPUMS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("[BLOCKED] IPUMS_API_KEY missing (environment or acquire/config.local.env)")
    return key


def call(method: str, path: str, key: str, **kw) -> requests.Response:
    r = requests.request(method, f"{API}{path}", headers={"Authorization": key}, timeout=120, **kw)
    if r.status_code == 401:
        raise SystemExit(f"[BLOCKED] IPUMS says: {r.json().get('detail', r.text)[:200]}\n"
                         "  → the account needs an IPUMS CPS registration (User Management App → Create IPUMS CPS Registration)")
    if r.status_code >= 400:
        raise SystemExit(f"[FAILED] {method} {path}: {r.status_code} {r.text[:400]}")
    return r


def asec_samples(key: str) -> list[str]:
    names, page = [], 1
    while True:
        data = call("GET", f"/metadata/{COLLECTION}/samples?version=2&pageSize=500&pageNumber={page}", key).json()
        rows = data.get("data", [])
        names += [d["name"] for d in rows if d["name"].endswith("_03s") and int(d["name"][3:7]) >= FIRST_YEAR]
        if not data.get("links", {}).get("nextPage") or not rows:
            break
        page += 1
    if len(names) < 30:
        raise SystemExit(f"[FAILED] only {len(names)} ASEC samples found from {FIRST_YEAR}: {names}")
    return sorted(names)


def submit(key: str) -> int:
    samples = asec_samples(key)
    body = {"description": DESCRIPTION, "dataStructure": {"rectangular": {"on": "P"}}, "dataFormat": "csv",
            "samples": {s: {} for s in samples}, "variables": {v: {} for v in VARIABLES}}
    r = call("POST", f"/extracts?collection={COLLECTION}&version=2", key, json=body)
    number = r.json()["number"]
    print(f"  ✓ submitted extract {number}: {len(samples)} ASEC samples {samples[0]}…{samples[-1]}, {len(VARIABLES)} variables, csv")
    return number


def status(key: str, number: int) -> dict:
    return call("GET", f"/extracts/{number}?collection={COLLECTION}&version=2", key).json()


def download(key: str, number: int) -> Path:
    info = status(key, number)
    if info.get("status") != "completed":
        raise SystemExit(f"[BLOCKED] extract {number} is {info.get('status')}, not completed")
    url = info["downloadLinks"]["data"]["url"]
    out_dir = data_root() / "external" / "cps"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "cps_2ndgen.csv.gz"
    tmp = out.with_suffix(".gz.part")
    # Resumable, retried download: IPUMS drops long streams mid-way (seen 2026-09-22 at 26 of 131 MB).
    expected = None
    for attempt in range(1, 9):
        have = tmp.stat().st_size if tmp.exists() else 0
        headers = {"Authorization": key}
        if have:
            headers["Range"] = f"bytes={have}-"
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(30, 120)) as r:
                if have and r.status_code != 206:
                    raise SystemExit(f"[FAILED] server ignored the Range request (status {r.status_code}); delete {tmp} and rerun")
                r.raise_for_status()
                if expected is None:
                    total = r.headers.get("Content-Range", "").rsplit("/", 1)[-1] or r.headers.get("Content-Length")
                    expected = int(total) if total and total.isdigit() else None
                with open(tmp, "ab") as f:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        f.write(chunk)
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout) as exc:
            print(f"  ! attempt {attempt}: transfer broke at {tmp.stat().st_size / 1e6:.1f} MB ({type(exc).__name__}); resuming")
            time.sleep(min(60, 5 * attempt))
            continue
        size = tmp.stat().st_size
        if expected is not None and size != expected:
            print(f"  ! attempt {attempt}: have {size} of {expected} bytes; resuming")
            continue
        break
    else:
        raise SystemExit(f"[FAILED] download of extract {number} incomplete after 8 attempts; partial file kept at {tmp}")
    h = hashlib.sha256()
    with open(tmp, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    tmp.replace(out)
    manifest = {"extract_number": number, "collection": COLLECTION, "description": DESCRIPTION,
                "samples": sorted(info.get("samples", {})), "variables": sorted(info.get("variables", {})),
                "data_format": info.get("dataFormat"), "downloaded": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "path": str(out), "bytes": out.stat().st_size, "sha256": h.hexdigest()}
    (out_dir / "cps_2ndgen.manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  ✓ downloaded {out} ({manifest['bytes'] / 1e6:.1f} MB, sha256 {manifest['sha256'][:16]}…); manifest beside it")
    return out


def wait(key: str, number: int) -> None:
    started = time.time()
    while True:
        st = status(key, number).get("status")
        print(f"  ▸ extract {number}: {st} ({int(time.time() - started)}s)")
        if st == "completed":
            return
        if st in ("failed", "canceled"):
            raise SystemExit(f"[FAILED] extract {number} {st}")
        if time.time() - started > MAX_WAIT_SECONDS:
            raise SystemExit(f"[BLOCKED] extract {number} still {st} after {MAX_WAIT_SECONDS}s")
        time.sleep(POLL_SECONDS)


def main() -> None:
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["run", "submit", "status", "download"])
    p.add_argument("--number", type=int)
    a = p.parse_args()
    key = api_key()
    if a.command == "submit":
        submit(key)
    elif a.command == "status":
        info = status(key, a.number); print(json.dumps({k: info.get(k) for k in ("number", "status", "dataFormat")}))
    elif a.command == "download":
        download(key, a.number)
    else:
        number = submit(key); wait(key, number); download(key, number)


if __name__ == "__main__":
    main()
