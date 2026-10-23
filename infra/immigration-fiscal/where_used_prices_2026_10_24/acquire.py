"""Acquire missing primary IPEDS inputs; never execute downloaded Python.

Run with ``uv run --no-project python3 -I .../acquire.py``. Existing sources are
read in place. New files live under this lane's ignored _cache/ipeds/ only.
"""
from __future__ import annotations

import hashlib
import json
import os
import resource
import shutil
import sys
import time
import urllib.request
import urllib.parse
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "_cache/ipeds"
BASE = "https://nces.ed.gov/ipeds/datacenter/data/"
FILES = ["EFFY2023.zip", "EFFY2023_Dict.zip", "F2223_F2.zip", "F2223_F2_Dict.zip",
         "F2223_F1A_Dict.zip", "EFIA2023_Dict.zip", "FLAGS2023_Dict.zip"]
PARK_FILES = {
    "acs5_2024_place.json": "https://api.census.gov/data/2024/acs/acs5?get=NAME%2CB03001_001E%2CB03001_004E&for=place%3A%2A",
    "acs5_2024_us.json": "https://api.census.gov/data/2024/acs/acs5?get=NAME%2CB03001_001E%2CB03001_004E&for=us%3A%2A",
    "B03001.json": "https://api.census.gov/data/2024/acs/acs5/groups/B03001.json",
    "Staffing_Spending_Volunteers_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx": "https://parkserve.tpl.org/downloads/cpf/Staffing_Spending_Volunteers_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx",
    "Acreage_Park_System_Highlights_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx": "https://parkserve.tpl.org/downloads/cpf/Acreage_Park_System_Highlights_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx",
    "2024_CPF_Methodology.pdf": "https://parkserve.tpl.org/downloads/cpf/2024_CPF_Methodology.pdf",
    "census_classification.pdf": "https://www2.census.gov/govs/class/classfull.pdf",
}
MAX_FILE = 100_000_000
MAX_CACHE = 5_000_000_000
MIRRORS = {
    "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip": ("https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip", "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"),
    "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/F2223_F1A.zip": (BASE + "F2223_F1A.zip", "beabdb0384f000a2fa487e7083512f880013c897d8e10bab9682f4c836687de9"),
    "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/EFIA2023.zip": (BASE + "EFIA2023.zip", "87229fac9a64563df477b47f392d5af7913e474363b440739a70a636c449560d"),
    "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/FLAGS2023.zip": (BASE + "FLAGS2023.zip", "df763ac04b15821bbcaa1dac238cbea9c2d88a5ae1b3532e2d1cd90489c8e3d3"),
    "sources/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv": ("https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv", "b8b50bd345d8a5f33d5c8a28c95aeaa0a50971356f000d9b48276a65fd9022a7"),
}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def source(path):
    """One resolver for exact-byte mirrors after a shared source mount loss."""
    if path.exists():
        return path
    relative = str(path.relative_to(REPO))
    alternative = HERE / "_cache/source_mirror" / path.name
    if relative not in MIRRORS or not alternative.exists():
        raise ValueError(f"[BLOCKED] raw source unavailable; run acquire.py: {relative}")
    return alternative


def fetch(name):
    target = CACHE / name
    url = BASE + name
    if not target.exists():
        request = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(request, timeout=45) as response:
            size = int(response.headers.get("Content-Length", 0))
            if size <= 0 or size > MAX_FILE:
                raise ValueError(f"[BLOCKED] unexpected download size {name}: {size}")
        partial = target.with_suffix(".part")
        with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as stream:
            size = 0
            while block := response.read(1 << 20):
                size += len(block)
                if size > MAX_FILE:
                    raise ValueError(f"[BLOCKED] download too large: {name}")
                stream.write(block)
        if not zipfile.is_zipfile(partial):
            raise ValueError(f"[BLOCKED] non-ZIP response: {name}")
        partial.rename(target)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"[BLOCKED] corrupt archive: {name}")
        members = archive.namelist()
    return {"path": str(target.relative_to(REPO)), "url": url,
            "bytes": target.stat().st_size, "sha256": sha(target), "members": members}


def census_key():
    names = ["CENSUS_API_KEY", "DATA_GOV_API_KEY", "CENSUS_KEY"]
    values = {}
    config = REPO / "infra/immigration-fiscal/acquire/config.local.env"
    if config.exists():
        for line in config.read_text().splitlines():
            if "=" in line:
                key, value = line.strip().removeprefix("export ").split("=", 1)
                if key in names:
                    values[key] = value.strip().strip("\"").strip("'")
    key = next((os.environ.get(name) or values.get(name) for name in names if os.environ.get(name) or values.get(name)), None)
    if not key:
        raise ValueError("[BLOCKED] Census API key unavailable; credentials never printed")
    return key


def fetch_park(name, url):
    target = HERE / "_cache/parks" / name
    target.parent.mkdir(exist_ok=True)
    if not target.exists():
        actual = url + ("&" if "?" in url else "?") + "key=" + urllib.parse.quote(census_key()) if "api.census.gov" in url else url
        try:
            with urllib.request.urlopen(actual, timeout=60) as response:
                raw = response.read(MAX_FILE + 1)
        except Exception:
            raise ValueError(f"[BLOCKED] primary request failed: {name}; URL suppressed") from None
        if not raw or len(raw) > MAX_FILE:
            raise ValueError(f"[BLOCKED] unexpected size: {name}")
        target.write_bytes(raw)
    if name.endswith(".json"):
        try:
            data = json.loads(target.read_bytes())
        except (ValueError, UnicodeError):
            raise ValueError(f"[BLOCKED] non-JSON Census response: {name}") from None
        if name.startswith("acs5_") and (not isinstance(data, list) or "B03001_004E" not in data[0]):
            raise ValueError(f"[BLOCKED] unexpected ACS schema: {name}")
    if name.endswith(".xlsx") and not zipfile.is_zipfile(target):
        raise ValueError(f"[BLOCKED] non-XLSX response: {name}")
    if name.endswith(".pdf") and not target.read_bytes().startswith(b"%PDF"):
        raise ValueError(f"[BLOCKED] non-PDF response: {name}")
    return {"path": str(target.relative_to(REPO)), "url": url,
            "bytes": target.stat().st_size, "sha256": sha(target)}


def recover_sources():
    """Recover exact pinned bytes locally if the external source disk is absent.

    No raw source is moved/changed, and a different release cannot replace it.
    The explicit receipt is separate so original acquisition provenance remains
    identical when a mount comes and goes.
    """
    receipt = []
    mirror = HERE / "_cache/source_mirror"
    for rel, (url, wanted) in MIRRORS.items():
        original = REPO / rel
        target = mirror / original.name
        if original.exists():
            continue
        mirror.mkdir(exist_ok=True)
        if not target.exists():
            print(f"[SOURCE-MIRROR] missing external input; recovering pinned {original.name}", flush=True)
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=45) as response:
                expected = int(response.headers.get("Content-Length", 0))
            if expected <= 0 or expected >= 2_000_000_000 or shutil.disk_usage(HERE).free < expected + 500_000_000:
                raise ValueError(f"[BLOCKED] source recovery size/disk check: {original.name}")
            partial = target.with_suffix(target.suffix + ".part")
            count, previous = 0, 0
            with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as stream:
                while block := response.read(8 << 20):
                    count += len(block)
                    if count > expected:
                        raise ValueError("[BLOCKED] source recovery exceeded advertised length")
                    stream.write(block)
                    if count - previous >= 100_000_000:
                        print(f"[SOURCE-MIRROR] {original.name}: {count}/{expected} bytes", flush=True)
                        previous = count
            if count != expected or sha(partial) != wanted:
                raise ValueError(f"[BLOCKED] recovered source differs from pinned bytes: {original.name}")
            partial.rename(target)
        if sha(target) != wanted:
            raise ValueError(f"[BLOCKED] corrupt source mirror: {original.name}")
        receipt.append({"original": rel, "mirror": str(target.relative_to(REPO)), "url": url, "sha256": wanted, "bytes": target.stat().st_size})
    if receipt:
        (mirror / "recovery_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main():
    started = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = [fetch(name) for name in FILES]
    rows += [fetch_park(name, url) for name, url in PARK_FILES.items()]
    recover_sources()
    size = sum(path.stat().st_size for path in (HERE / "_cache").rglob("*") if path.is_file())
    if size >= MAX_CACHE:
        raise ValueError(f"[BLOCKED] lane cache exceeds 5 GB: {size}")
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    manifest = {"source": "NCES IPEDS complete data files", "vintage": "2022-23",
                "files": rows, "cache_limit_bytes": MAX_CACHE}
    path = out / "acquisition.json"
    # Acquisition is idempotent and pins a release rather than accepting drift.
    if path.exists():
        current = {row["path"]: row for row in rows}
        for old in json.loads(path.read_text())["files"]:
            if current.get(old["path"]) != old:
                raise ValueError("[BLOCKED] primary download manifest changed; inspect release before repinning")
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"files": len(rows), "cache_bytes": size,
                      "elapsed_seconds": time.perf_counter() - started,
                      "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "python_isolated": bool(sys.flags.isolated)}, sort_keys=True))


if __name__ == "__main__":
    main()
