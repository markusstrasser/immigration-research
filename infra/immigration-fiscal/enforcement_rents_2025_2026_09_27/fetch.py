#!/usr/bin/env python3
"""Downloads for the 2025 enforcement-and-rents lane (BRIEF.md).

Every file lands under ``_cache/`` (git-ignored) and is recorded in
``_cache/manifest.json`` with its source URL, byte count and sha256.  Existing
files are kept unless ``--refresh`` is given, so a rerun costs nothing.

Requests carry a generic browser User-Agent and no personal identifier.  The
Census API key is read from ``CENSUS_API_KEY`` (exported by
``infra/immigration-fiscal/acquire/config.local.env``) and never printed: every
URL and exception passes through :func:`redact`.

Run from the repository root::

    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    uv run --no-project python3 infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/fetch.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

ZILLOW = "https://files.zillowstatic.com/research/public_csvs/zori"
BPS = "https://www2.census.gov/econ/bps"
POPEST = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025"
DDP_ICE = "https://github.com/deportationdata/ice/raw/refs/heads/main/data"
DDP_OFFICES = "https://github.com/deportationdata/ice-offices/raw/refs/heads/main/data"
BROOKINGS = "https://www.brookings.edu/wp-content/uploads/2026/09"

# (cache path, url, expected kind)
TARGETS: list[tuple[str, str, str]] = [
    # Zillow Observed Rent Index, metro and city, smoothed; the SA file is a check.
    ("zillow/Metro_zori_uc_sfrcondomfr_sm_month.csv",
     f"{ZILLOW}/Metro_zori_uc_sfrcondomfr_sm_month.csv", "text"),
    ("zillow/Metro_zori_uc_sfrcondomfr_sm_sa_month.csv",
     f"{ZILLOW}/Metro_zori_uc_sfrcondomfr_sm_sa_month.csv", "text"),
    ("zillow/City_zori_uc_sfrcondomfr_sm_month.csv",
     f"{ZILLOW}/City_zori_uc_sfrcondomfr_sm_month.csv", "text"),
    # Census building permits by metro, annual (2020 CBSA delineation through 2023).
    *[(f"bps/ma{y}a.txt", f"{BPS}/Metro%20(ending%202023)/ma{y}a.txt", "text")
      for y in (2019, 2020, 2021, 2022, 2023)],
    *[(f"bps/cbsa{y}a.txt", f"{BPS}/CBSA%20(beginning%20Jan%202024)/cbsa{y}a.txt", "text")
      for y in (2024, 2025)],
    # Census Vintage 2025 population estimates with components of change.
    ("popest/cbsa-est2025-alldata.csv", f"{POPEST}/metro/totals/cbsa-est2025-alldata.csv", "text"),
    ("popest/co-est2025-alldata.csv", f"{POPEST}/counties/totals/co-est2025-alldata.csv", "text"),
    ("popest/NST-EST2025-ALLDATA.csv", f"{POPEST}/state/totals/NST-EST2025-ALLDATA.csv", "text"),
    # ICE arrests (FOIA, Deportation Data Project) and county-to-AOR crosswalk.
    ("ice/arrests-latest.parquet", f"{DDP_ICE}/arrests-latest.parquet", "any"),
    ("ice/ice-aor-county-shp.parquet", f"{DDP_OFFICES}/ice-aor-county-shp.parquet", "any"),
    # Brookings "Beyond arrests" metro table (image PDF; transcribed to brookings_surge_metros.csv).
    ("web/Beyond-Arrests-Metro-Data.pdf", f"{BROOKINGS}/Beyond-Arrests-Metro-Data.pdf", "pdf"),
    ("web/Beyond-Arrests-Appendices.pdf", f"{BROOKINGS}/Beyond-Arrests-Appendices.pdf", "pdf"),
]

# ACS 1-year 2021, CBSA level: housing units, tenure, units in structure.
ACS_YEAR = 2021
ACS_VARS = ["NAME", "B25001_001E", "B25003_001E", "B25003_003E", "B25024_001E",
            "B25024_006E", "B25024_007E", "B25024_008E", "B25024_009E"]
ACS_GEO = "metropolitan statistical area/micropolitan statistical area:*"

_KEY_RE = re.compile(r"(key=)[^&\s\"'<>]+", re.IGNORECASE)


def redact(text: object) -> str:
    out = _KEY_RE.sub(r"\1REDACTED", str(text))
    key = os.environ.get("CENSUS_API_KEY", "")
    if key and len(key) >= 8:
        out = out.replace(key, "REDACTED")
    return out


def log(msg: object) -> None:
    print(redact(msg), flush=True)


def bad_body(blob: bytes, expect: str) -> str:
    """Reason string if *blob* is not the expected payload, else ``""``.

    www2.census.gov can answer a data URL with an HTML rejection page under
    HTTP 200, so text targets are content-checked, not only status-checked.
    """
    head = blob[:400].lstrip().lower()
    if expect == "pdf":
        return "" if blob[:4] == b"%PDF" else "missing %PDF magic"
    if expect == "text" and (head.startswith(b"<html") or head.startswith(b"<!doctype html")
                             or b"request rejected" in head):
        return "HTML body served for a data URL"
    if not blob:
        return "empty body"
    return ""


def fetch(url: str, expect: str, params: dict | None = None, tries: int = 4) -> bytes:
    last: object = None
    for attempt in range(1, tries + 1):
        try:
            r = requests.get(url, params=params, timeout=300, headers={"User-Agent": UA})
            if r.status_code == 200:
                why = bad_body(r.content, expect)
                if not why:
                    return r.content
                last = why
            else:
                last = f"HTTP {r.status_code}"
        except requests.RequestException as exc:  # transport error: retry
            last = exc
        log(f"  retry {attempt}/{tries} {url}: {last}")
        time.sleep(3 * attempt)
    raise SystemExit(f"[BLOCKED] {redact(url)}: {redact(last)}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    refresh = "--refresh" in sys.argv
    manifest_path = CACHE / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for rel, url, expect in TARGETS:
        path = CACHE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if refresh or not path.exists():
            log(f"GET {url}")
            path.write_bytes(fetch(url, expect))
        manifest[rel] = {"url": url, "bytes": path.stat().st_size, "sha256": sha256(path)}

    rel = f"acs/acs1_{ACS_YEAR}_cbsa_housing.json"
    path = CACHE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://api.census.gov/data/{ACS_YEAR}/acs/acs1"
    if refresh or not path.exists():
        key = os.environ.get("CENSUS_API_KEY", "").strip()
        if not key:
            raise SystemExit("[BLOCKED] CENSUS_API_KEY is not set; source "
                             "infra/immigration-fiscal/acquire/config.local.env first")
        log(f"GET {url} ({len(ACS_VARS)} variables, all CBSAs)")
        blob = fetch(url, "text", params={"get": ",".join(ACS_VARS), "for": ACS_GEO, "key": key})
        json.loads(blob)  # must parse
        path.write_bytes(blob)
    manifest[rel] = {"url": f"{url}?get={','.join(ACS_VARS)}&for={ACS_GEO}",
                     "bytes": path.stat().st_size, "sha256": sha256(path)}

    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    log(f"manifest: {len(manifest)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
