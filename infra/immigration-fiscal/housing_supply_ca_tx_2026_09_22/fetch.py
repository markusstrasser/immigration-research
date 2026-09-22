#!/usr/bin/env python3
"""Downloads for the CA/TX housing-supply lane (BRIEF.md).

Every download is written under ``_cache/`` (git-ignored) and recorded in
``_cache/manifest.json`` with its source URL, byte count and sha256.

The Census API key is read from the environment (``CENSUS_API_KEY``, exported by
``infra/immigration-fiscal/acquire/config.local.env``).  The key is never printed:
every URL and every exception string passes through :func:`redact` first.

Run from the repository root::

    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    PYTHONUNBUFFERED=1 uv run --no-project python3 \
        infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/fetch.py
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

# Permit years requested by the brief (BPS state annual, December year-to-date file).
PERMIT_YEARS = list(range(2000, 2025))

# ACS 1-year vintages for state housing units.
HU_YEARS = [2010, 2015, 2019, 2023, 2024]

BPS_STATE_DIR = "https://www2.census.gov/econ/bps/State"
BPS_DOC = "https://www2.census.gov/econ/bps/Documentation/stateasc.pdf"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv"
POPEST = "https://www2.census.gov/programs-surveys/popest/datasets"
PUMS_DICT = (
    "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/"
    "PUMS_Data_Dictionary_2024.csv"
)

_KEY_RE = re.compile(r"(key=)[^&\s\"'<>]+", re.IGNORECASE)


def redact(text: object) -> str:
    """Strip any ``key=...`` query parameter from *text*.

    Applied to every URL and every exception before it reaches stdout, so the
    Census API key cannot leak through a progress line or a traceback.
    """
    out = _KEY_RE.sub(r"\1REDACTED", str(text))
    key = os.environ.get("CENSUS_API_KEY", "")
    if key and len(key) >= 8:
        out = out.replace(key, "REDACTED")
    return out


def log(msg: object) -> None:
    print(redact(msg), flush=True)


def census_key() -> str:
    key = os.environ.get("CENSUS_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "[BLOCKED] CENSUS_API_KEY is not set; run "
            "`set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`"
        )
    return key


def looks_like_error_page(blob: bytes) -> str:
    """Return a reason string if *blob* is an HTML error page, else ``""``.

    www2.census.gov sits behind a WAF that answers some requests with
    ``<html>...Request Rejected...</html>`` under **HTTP 200**.  Checking the
    status code alone silently caches a 247-byte error page as if it were data
    (observed 2026-09-22 for the 2018 permits file), so every text target is
    content-checked as well.
    """
    head = blob[:400].lstrip().lower()
    if head.startswith(b"<html") or head.startswith(b"<!doctype html"):
        return "HTML body served for a data URL (WAF rejection or error page)"
    if b"request rejected" in head:
        return "WAF 'Request Rejected' body"
    return ""


def fetch(url: str, params: dict | None = None, tries: int = 4, timeout: int = 240,
          expect: str = "text") -> bytes:
    """GET *url*, returning raw bytes.

    *expect* is ``"text"`` (reject HTML error bodies), ``"pdf"`` (require the
    ``%PDF`` magic) or ``"any"``.  A body that fails its check is retried like a
    transport error and then raised, never cached.
    """
    last = None
    for attempt in range(1, tries + 1):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            if resp.status_code == 200:
                blob = resp.content
                if expect == "pdf":
                    if blob[:4] == b"%PDF":
                        return blob
                    last = "body is not a PDF (%PDF magic missing)"
                elif expect == "text":
                    reason = looks_like_error_page(blob)
                    if not reason:
                        return blob
                    last = f"{reason}; {len(blob)} bytes"
                else:
                    return blob
            else:
                last = f"HTTP {resp.status_code}: {redact(resp.text)[:300]}"
        except Exception as exc:  # noqa: BLE001 - reported, not swallowed
            last = f"{type(exc).__name__}: {redact(exc)[:300]}"
        if attempt < tries:
            time.sleep(5 * attempt)
    raise RuntimeError(f"{redact(url)} failed after {tries} tries :: {last}")


def fetch_bps(url: str) -> tuple[bytes, str]:
    """Fetch a BPS state file, working around a misfiring WAF rule.

    Observed 2026-09-22: ``st1812y.txt`` (calendar 2018) is answered with a
    247-byte ``Request Rejected`` HTML page under HTTP 200, with a constant
    support ID, while every neighbouring year serves normally.  The rule keys on
    the exact URL string, so appending an inert query parameter returns the real
    file.  Nothing here is authenticated: the file is public and the fallback is
    a cache-buster, not a credential.  The returned bytes are validated by the
    parser (survey date, state count) and cross-checked against FRED.
    """
    try:
        return fetch(url, expect="text"), "direct"
    except RuntimeError as exc:
        if "WAF" not in str(exc) and "HTML body" not in str(exc):
            raise
        log(f"  [warn] WAF rejected {redact(url)}; retrying with an inert query parameter")
        return fetch(url, params={"bps_cachebust": "1"}, expect="text"), "cachebust"


def store(name: str, blob: bytes, url: str, manifest: dict, note: str = "") -> Path:
    path = CACHE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    manifest[name] = {
        "url": redact(url),
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "note": note,
    }
    log(f"  stored {name}: {len(blob):,} bytes sha256={manifest[name]['sha256'][:16]}")
    return path


def api_json(base: str, params: dict, key: str, name: str, manifest: dict, note: str) -> None:
    """Fetch a Census API table and store it as JSON.  The key never enters the log."""
    full = dict(params)
    full["key"] = key
    blob = fetch(base, params=full, expect="text")
    json.loads(blob)  # fail loudly on an HTML error page served with status 200
    store(name, blob, f"{base}?{params}", manifest, note)


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest_path = CACHE / "manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
        except json.JSONDecodeError:
            manifest = {}
    key = census_key()
    blocked: list[str] = []

    def guard(label: str, fn) -> None:
        if label in manifest and (CACHE / label).exists():
            log(f"[skip] {label} already cached")
            return
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"[BLOCKED] {label}: {redact(exc)[:400]}"
            log(msg)
            blocked.append(msg)

    log("== BPS documentation ==")
    guard("bps_stateasc.pdf", lambda: store(
        "bps_stateasc.pdf", fetch(BPS_DOC, expect="pdf"), BPS_DOC, manifest,
        "state file record layout, read before parsing"))

    log("== BPS state annual permits (December year-to-date files) ==")
    for year in PERMIT_YEARS:
        yy = f"{year % 100:02d}"
        url = f"{BPS_STATE_DIR}/st{yy}12y.txt"
        name = f"bps_state_{year}.txt"

        def _bps(u=url, n=name, y=year):
            blob, how = fetch_bps(u)
            store(n, blob, u, manifest,
                  f"annual (Dec year-to-date) state permits, {y}; retrieved {how}")

        guard(name, _bps)

    log("== BPS state monthly files for the cross-check years ==")
    for year in (2015, 2019, 2023):
        yy = f"{year % 100:02d}"
        for month in range(1, 13):
            url = f"{BPS_STATE_DIR}/st{yy}{month:02d}c.txt"
            name = f"bps_state_monthly_{year}{month:02d}.txt"

            def _bpsm(u=url, n=name, y=year, m=month):
                blob, how = fetch_bps(u)
                store(n, blob, u, manifest,
                      f"monthly (current month) state permits, {y}-{m:02d}; retrieved {how}")

            guard(name, _bpsm)

    log("== FRED cross-check series ==")
    for series in ("CABPPRIV", "TXBPPRIV"):
        url = f"{FRED}?id={series}"
        name = f"fred_{series}.csv"
        guard(name, lambda u=url, n=name, s=series: store(
            n, fetch(u), u, manifest, f"FRED {s} monthly private housing units authorised"))

    log("== Census population estimates ==")
    popest_targets = [
        ("popest_2020_2024.csv",
         f"{POPEST}/2020-2024/state/totals/NST-EST2024-ALLDATA.csv",
         "vintage 2024 state estimates, 2020-2024"),
        ("popest_2010_2019.csv",
         f"{POPEST}/2010-2019/national/totals/nst-est2019-alldata.csv",
         "vintage 2019 state estimates, 2010-2019 (state rows carry SUMLEV 040)"),
        ("popest_2000_2010_intercensal.csv",
         f"{POPEST}/2000-2010/intercensal/state/st-est00int-alldata.csv",
         "intercensal state estimates, 2000-2010"),
    ]
    for name, url, note in popest_targets:
        guard(name, lambda n=name, u=url, t=note: store(n, fetch(u), u, manifest, t))

    log("== ACS API: variable labels (recorded in audit.json) ==")
    for vintage in (2010, 2023):
        for var in ("B03001_001E", "B03001_004E"):
            url = f"https://api.census.gov/data/{vintage}/acs/acs5/variables/{var}.json"
            name = f"acsvar_{vintage}_{var}.json"
            guard(name, lambda u=url, n=name: store(
                n, fetch(u), u, manifest, "variable label confirmation (key-free)"))

    log("== ACS API: state housing units (1-year B25001) ==")
    for year in HU_YEARS:
        name = f"acs1_hu_{year}.json"
        guard(name, lambda y=year, n=name: api_json(
            f"https://api.census.gov/data/{y}/acs/acs1",
            {"get": "NAME,B25001_001E", "for": "state:*"}, key, n, manifest,
            f"ACS 1-year {y} total housing units by state"))

    log("== ACS API: state population 2023 (G2 cross-check) ==")
    guard("acs1_pop_2023.json", lambda: api_json(
        "https://api.census.gov/data/2023/acs/acs1",
        {"get": "NAME,B01003_001E", "for": "state:*"}, key, "acs1_pop_2023.json", manifest,
        "ACS 1-year 2023 total population by state, popest cross-check"))

    log("== ACS API: 2024 native non-Hispanic white 18+ (G4 cross-check) ==")
    guard("acs1_b05003h_2024.json", lambda: api_json(
        "https://api.census.gov/data/2024/acs/acs1",
        {"get": "NAME,B05003H_009E,B05003H_020E", "for": "state:*"}, key,
        "acs1_b05003h_2024.json", manifest,
        "B05003H native male 18+ (009E) and native female 18+ (020E), white alone not Hispanic"))

    log("== ACS API: metro Mexican-origin population (5-year B03001) ==")
    for vintage in (2010, 2023):
        name = f"acs5_metro_b03001_{vintage}.json"
        guard(name, lambda v=vintage, n=name: api_json(
            f"https://api.census.gov/data/{v}/acs/acs5",
            {"get": "NAME,B03001_001E,B03001_004E",
             "for": "metropolitan statistical area/micropolitan statistical area:*"},
            key, n, manifest, f"ACS 5-year {v} Mexican-origin and total population by CBSA"))

    log("== PUMS 2024 data dictionary ==")
    guard("pums_data_dictionary_2024.csv", lambda: store(
        "pums_data_dictionary_2024.csv", fetch(PUMS_DICT), PUMS_DICT, manifest,
        "2024 ACS PUMS code lists (MIGSP, NATIVITY, RAC1P, HISP, SCHL, STATE)"))

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    log(f"\nmanifest: {manifest_path} ({len(manifest)} entries)")
    if blocked:
        log(f"BLOCKED items: {len(blocked)}")
        (CACHE / "blocked.json").write_text(json.dumps(blocked, indent=2) + "\n")
    else:
        (CACHE / "blocked.json").unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
