#!/usr/bin/env python3
"""One store for the IPUMS USA extracts on the operator's account: link, complete, catalog, convert, join.

Steps, in order (each prints one line per item; every step can be re-run; nothing is ever deleted):
  api       fetch the definitions of extracts 1-15 (samples, variables, case selections, quality
            flags, IPUMS's published bytes and sha256) into _cache/api/
  download  fetch extracts 7 and 8, which the crime lane submitted but never downloaded, into
            _cache/downloads/; verify them against IPUMS's sha256; hard-link them into the crime
            lane's _cache/ipums/ as acs_movers and acs_us
  ddi       fetch the DDI of extracts whose lane kept only the basic .cbk (3, 12, 13)
  link      hard-link every held extract into the store as usa_000NN_<slug>.csv.gz and .xml
  verify    sha256 of each held data file and DDI against IPUMS's published values
  count     CSV rows (gzip -dc | wc -l, minus the header)
  parquet   typed Parquet per extract (types from the DDI) under sources/immigration-fiscal/derived/ipums_usa/
  duckdb    ipums_usa_extracts.duckdb: one view per extract, catalog, variables, value_labels, the
            person-level allocation-flag view qflags, and usa_000NN_q join views
  joins     gates per extract, and the match rate of every pair of extracts whose samples and
            universes overlap, on YEAR, SAMPLE, SERIAL, PERNUM
  catalog   catalog.json and CATALOG.md in the store; tracked copies in derived/
  register  sha256 lines in the raw-file MANIFEST.md and a section in the IPUMS README

Hard links keep every lane's cache paths working, including a lane that is still running. A name
that already exists is skipped when it is the same inode and stops the run otherwise.

Run from the repository root (no step names = all steps):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \\
      infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py [step ...]
The IPUMS key comes from IPUMS_API_KEY or acquire/config.local.env and is never printed.
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

os.environ.setdefault("PYTHONUNBUFFERED", "1")

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
IPUMS = ROOT / "sources/immigration-fiscal/data/external/ipums"
STORE = IPUMS / "usa_extract"
# Where the usa_000NN_<slug> names go. build/load_ipums_borjas_panel.py resolves usa_00002.csv.gz
# by exact name since 4767db7; before that it loaded the last-sorting usa_*.csv.gz in STORE.
LINK_DIR = STORE
MANIFEST = ROOT / "sources/immigration-fiscal/data/MANIFEST.md"
DERIVED = ROOT / "sources/immigration-fiscal/derived"
PARQ = DERIVED / "ipums_usa"
DB = DERIVED / "ipums_usa_extracts.duckdb"
CACHE = HERE / "_cache"
DL = CACHE / "downloads"
OUT = HERE / "derived"
API = "https://api.ipums.org"
KEYS = ["YEAR", "SAMPLE", "SERIAL", "PERNUM"]
TODAY = "2026-09-23"

CRIME = FISCAL / "crime_selection_cohorts_2026_09_23"
SCHOOL = FISCAL / "schooling_selection_position_2026_09_23"
ANCESTRY = FISCAL / "ancestry_iv_congestion_wages_2026_09_23"
CRIME_RESULT = "infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/RESULT.md"
SCHOOL_RESULT = "infra/immigration-fiscal/schooling_selection_position_2026_09_23/RESULT.md"
ANCESTRY_RESULT = "infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/RESULT.md"

# Hand-written per extract: slug (sample_universe[_content]), the held copy, who made it, the
# universe in plain words, where it was used, and what else it can answer. Samples, variables,
# selections and hashes come from the API and the files.
EXTRACTS = {
    1: dict(slug="census1980-2000+acs2010+acs2023_all-v1", data=None, ddi=None,
            lane="operator, usa.ipums.org browser, 2026-06-23",
            universe="Every person in the 1980, 1990 and 2000 5% censuses and the 2010 and 2023 ACS",
            used=["Never downloaded; superseded the same day by extract 2, which adds BPL, CITIZEN and YRIMMIG"],
            beyond="Nothing that extract 2 cannot: same samples, fewer variables."),
    2: dict(slug="census1980-2000+acs2010+acs2023_all", data=STORE / "usa_00002.csv.gz", ddi=None,
            lane="operator, usa.ipums.org browser, 2026-06-23",
            universe="Every person, all ages, in the 1980, 1990 and 2000 5% censuses and the 2010 and 2023 "
                     "one-year ACS; no SEX, HISPAN or wage variables",
            used=["infra/immigration-fiscal/build/load_ipums_borjas_panel.py -> immigration_microdata.duckdb "
                  "table ipums_usa_borjas_panel",
                  "research/immigration-borjas-supply-shock-panel-2026-06-23.md",
                  "research/immigration-employment-entry-displacement-2026-09-18.md",
                  "research/immigration-mexican-arrival-cohorts-2026-09-18.md",
                  "infra/immigration-fiscal/apportionment_2026_09_18/kids_ipums.py",
                  "infra/immigration-fiscal/projection_backtest_2026_09_19/cohorts.py",
                  "infra/immigration-fiscal/scale_spillovers_2026_09_23/sample_weights.py",
                  SCHOOL_RESULT + " (count cross-check)"],
            beyond="Joined to extracts 10 and 11 it gains SEX, HISPAN, wages, hours and commute for ages "
                   "16-64 in 1990, 2000 and 2010, so the Borjas panel can be cut by sex without a new "
                   "extract (view usa_00002_sex); the flag extracts 6, 13, 14 and 15 mark imputed "
                   "birthplace, arrival year, education and citizenship for the records they cover "
                   "(men 18-40 in 1980-2000, the Mexican-born, the institutionalized)."),
    3: dict(slug="census1980-2000+acs2005-2024_mexborn", data=SCHOOL / "_cache/us_mexborn.data.csv.gz", ddi=None,
            lane="schooling_selection_position_2026_09_23",
            universe="Every Mexico-born person (BPL 200), all ages, in the 1980, 1990 and 2000 5% censuses and "
                     "every one-year ACS 2005-2024",
            used=[SCHOOL_RESULT + " (position.py)"],
            beyond="Naturalization, school enrolment and schooling of Mexican-born people by arrival cohort, "
                   "age and sex for 1980-2024; with extract 12 an unbroken 2000-2024 ACS series, and with "
                   "extract 13 every figure can be recomputed without imputed education."),
    4: dict(slug="census1980-2000_men18-40", data=CRIME / "_cache/ipums/census.csv.gz",
            ddi=CRIME / "_cache/ipums/census.xml", lane="crime_selection_cohorts_2026_09_23",
            universe="Men aged 18-40, every birthplace, in the 1980, 1990 and 2000 5% censuses, with "
                     "group-quarters type (institution type only in 1980; 1990 and 2000 say 'institution')",
            used=[CRIME_RESULT + " (analyze_census.py, admin_check.py, census_se_check.py)"],
            beyond="Institutionalization by birthplace for any origin country, not only Mexico (Cuba, "
                   "El Salvador, Vietnam, India), against native Hispanic and non-Hispanic white men; "
                   "arrival-cohort institutionalization for every origin group; in 1980 only, by "
                   "institution type (correctional, mental, elderly and disabled)."),
    5: dict(slug="acs2006-2024-no2020_mexborn-men18-40_repwt", data=CRIME / "_cache/ipums/acs_mex.csv.gz",
            ddi=CRIME / "_cache/ipums/acs_mex.xml", lane="crime_selection_cohorts_2026_09_23",
            universe="Mexico-born men aged 18-40 in every one-year ACS 2006-2024 except 2020, with the 80 "
                     "person replicate weights",
            used=[CRIME_RESULT + " (analyze_acs.py)"],
            beyond="Replicate-weight standard errors for any statistic on young Mexican-born men "
                   "(citizenship, schooling, state, group quarters) by arrival cohort; with extract 13, "
                   "education allocation for the same men."),
    6: dict(slug="census1980-2000_men18-40_qflags", data=CRIME / "_cache/ipums/census_q.csv.gz",
            ddi=CRIME / "_cache/ipums/census_q.xml", lane="crime_selection_cohorts_2026_09_23",
            universe="The same people as extract 4 (men 18-40, 1980-2000 5% censuses) with the allocation "
                     "flags QBPL, QYRIMM and QEDUC",
            used=[CRIME_RESULT + " (analyze_census.py, admin_check.py: drop-allocated check)"],
            beyond="How much of any 1980-2000 immigrant-native gap for young men rests on imputed "
                   "birthplace, arrival year or education, by origin and census year; it flags records "
                   "of extracts 2, 3, 10 and 11 as well."),
    7: dict(slug="acs2019+2023+2024_usborn-men18-40_repwt", data=DL / "usa_00007.csv.gz", ddi=DL / "usa_00007.xml",
            crime_name="acs_movers", lane="crime_selection_cohorts_2026_09_23 (submitted; downloaded by this lane)",
            universe="Men aged 18-40 born in the 50 states or DC, in the one-year ACS 2019, 2023 and 2024, "
                     "with the 80 person replicate weights",
            used=["Not yet used; the crime lane ran on extract 9 with a household jackknife "
                  "(" + CRIME_RESULT + ", section on movers)"],
            beyond="Replicate-weight SEs for the interstate mover-versus-stayer comparison (birth state "
                   "against current state) and for native young men's schooling and group quarters by "
                   "race, Hispanic origin and state."),
    8: dict(slug="acs2006-2024-no2020_usborn-men18-40", data=DL / "usa_00008.csv.gz", ddi=DL / "usa_00008.xml",
            crime_name="acs_us", lane="crime_selection_cohorts_2026_09_23 (submitted; downloaded by this lane)",
            universe="Men aged 18-40 born in the 50 states or DC, in every one-year ACS 2006-2024 except "
                     "2020, main weight only",
            used=["Not yet used; the crime lane took its native reference rates from the Census API"],
            beyond="Native reference rates by single year of age, race, Hispanic origin, education and "
                   "state for 18 years: institutionalization and schooling of US-born Hispanic men (all "
                   "second or later generation) against non-Hispanic white men."),
    9: dict(slug="acs2019+2023+2024_usborn-men18-40", data=CRIME / "_cache/ipums/acs_movers_lite.csv.gz",
            ddi=CRIME / "_cache/ipums/acs_movers_lite.xml", lane="crime_selection_cohorts_2026_09_23",
            universe="The same people as extract 7 without replicate weights",
            used=[CRIME_RESULT + " (analyze_movers.py -> derived/acs_movers.csv)"],
            beyond="Nothing beyond extract 7, which has the same records plus replicate weights; kept "
                   "because the crime lane's results were computed from it."),
    10: dict(slug="census2000+acs2010+acs2009-2011_age16-64", data=ANCESTRY / "_cache/ipums/core.csv.gz",
             ddi=ANCESTRY / "_cache/ipums/core.xml", lane="ancestry_iv_congestion_wages_2026_09_23",
             universe="Every person aged 16-64 in the 2000 5% census, the 2010 one-year ACS and the "
                      "2009-2011 three-year ACS, with wages, hours, commute, PUMA and 2013 metro area",
             used=[ANCESTRY_RESULT + " (build_pums.py; lane still running)"],
             beyond="Wages, employment and commute time of natives and immigrants by education, "
                    "citizenship and metro area in 2000 and 2010; the Mexican-born wage gap by "
                    "citizenship at fixed 2013 metro geography; SEX and HISPAN for extract 2's working-age "
                    "records."),
    11: dict(slug="census1990_age16-64", data=ANCESTRY / "_cache/ipums/pre.csv.gz",
             ddi=ANCESTRY / "_cache/ipums/pre.xml", lane="ancestry_iv_congestion_wages_2026_09_23",
             universe="Every person aged 16-64 in the 1990 5% census, with the same variables as extract 10 "
                      "and 1990 metro area and county",
             used=[ANCESTRY_RESULT + " (build_pums_1990.py; pre-trend placebo)"],
             beyond="The 1990 baseline for any 1990-2000-2010 metro panel of wages, employment and "
                    "commute by nativity and education; county-level figures for large counties in 1990."),
    12: dict(slug="acs2000-2004_mexborn", data=SCHOOL / "_cache/us_mexborn_acs0004.data.csv.gz", ddi=None,
             lane="schooling_selection_position_2026_09_23",
             universe="Every Mexico-born person, all ages, in the ACS 2000-2004 (the pre-2005 ACS "
                      "samples, households only)",
             used=[SCHOOL_RESULT + " (instrument_checks.py)"],
             beyond="Fills 2000-2004 in the annual Mexican-born series of extract 3; sees the 1995-2004 "
                    "arrival cohorts within a few years of arrival."),
    13: dict(slug="census1980-2000+acs2000-2024_mexborn_qeduc", data=SCHOOL / "_cache/us_mexborn_qeduc.data.csv.gz",
             ddi=None, lane="schooling_selection_position_2026_09_23",
             universe="Every Mexico-born person in the samples of extracts 3 and 12, with the education "
                      "allocation flag QEDUC",
             used=[SCHOOL_RESULT + " (instrument_checks.py: allocation diagnostic)"],
             beyond="How often Mexican-born people's education is imputed, 1980-2024, and "
                    "allocation-robust education for any IPUMS analysis of them; it flags the "
                    "Mexican-born records of extracts 2, 4, 5, 10 and 11."),
    14: dict(slug="census1980-2000_inst-men18-40_qflags", data=CRIME / "_cache/ipums/census_inst_q.csv.gz",
             ddi=CRIME / "_cache/ipums/census_inst_q.xml", lane="crime_selection_cohorts_2026_09_23",
             universe="Institutionalized men aged 18-40 (GQ 3) in the 1980, 1990 and 2000 5% censuses, with "
                      "the flags QBPL and QCITIZEN",
             used=[CRIME_RESULT + " (analyze_census.py, admin_check.py)"],
             beyond="Whether imputed nativity or citizenship drives institutionalization rates for any "
                    "origin group, not only Mexico; the imputed share of noncitizen inmates by census."),
    15: dict(slug="census2000_inst-allages_qflags", data=CRIME / "_cache/ipums/census2000_inst.csv.gz",
             ddi=CRIME / "_cache/ipums/census2000_inst.xml", lane="crime_selection_cohorts_2026_09_23",
             universe="Every institutionalized person (GQ 3), all ages, in the 2000 5% census, with "
                      "the flags QBPL and QCITIZEN; GQTYPE does not name the institution type in 2000",
             used=[CRIME_RESULT + " (admin_check.py: 2000 inmate nativity against BJS)"],
             beyond="The institutionalized population of every age in 2000 by nativity, citizenship, "
                    "arrival year and state, with age standing in for the type the file does not record "
                    "(65+ mostly nursing homes, young men mostly correctional): e.g. elderly immigrants' "
                    "institutional care against natives', and how much of it rests on imputed nativity."),
}
FLAG_FILES = {6: ["QBPL", "QYRIMM", "QEDUC"], 13: ["QEDUC"], 14: ["QBPL", "QCITIZEN"], 15: ["QBPL", "QCITIZEN"]}
QVARS = ["QBPL", "QYRIMM", "QEDUC", "QCITIZEN"]
# Extract 2's DDI expired before anyone saved it; these two variables appear in no other DDI.
# Widths from the IPUMS USA variable pages; a value that does not fit stops the Parquet step.
FALLBACK_WIDTH = {"WKSWORK1": 2, "INCTOT": 7}
NS = {"d": "ddi:codebook:2_5"}

_KEY = None


def say(step: str, msg: str) -> None:
    print(f"[{step}] {msg}", flush=True)


def api_key() -> str:
    global _KEY
    if _KEY:
        return _KEY
    key = os.environ.get("IPUMS_API_KEY", "")
    env = FISCAL / "acquire" / "config.local.env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            line = line.removeprefix("export ").strip()
            if line.startswith("IPUMS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        raise SystemExit("[BLOCKED] IPUMS_API_KEY missing")
    _KEY = key
    return key


def red(text: str) -> str:
    """Remove the key from anything printed or written."""
    text = re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", str(text))
    return text.replace(_KEY, "<KEY>") if _KEY else text


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT)) if str(Path(p).resolve()).startswith(str(ROOT)) else str(p)


def name(n: int, ext: str) -> str:
    return f"usa_{n:05d}_{EXTRACTS[n]['slug']}.{ext}"


def load_json(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


def save_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=str) + "\n")
    tmp.replace(p)


def sha256(p: Path) -> str:
    """sha256, cached by inode, size and mtime so re-runs do not re-read 1.9 GB."""
    cache_p = CACHE / "hashes.json"
    cache = load_json(cache_p, {})
    st = p.stat()
    tag = f"{st.st_ino}:{st.st_size}:{st.st_mtime_ns}"
    if cache.get(tag):
        return cache[tag]
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    cache[tag] = h.hexdigest()
    save_json(cache_p, cache)
    return cache[tag]


# ---------------------------------------------------------------- api

def get(path: str) -> requests.Response:
    for attempt in range(1, 6):
        try:
            r = requests.get(f"{API}{path}", headers={"Authorization": api_key()}, timeout=120)
            if r.status_code < 500:
                return r
        except requests.exceptions.RequestException as exc:
            say("api", f"attempt {attempt}: {type(exc).__name__}")
        time.sleep(5 * attempt)
    raise SystemExit(f"[FAILED] GET {red(path)}")


def definition(n: int) -> dict:
    p = CACHE / "api" / f"extract_{n:02d}.json"
    if not p.exists():
        raise SystemExit(f"[BLOCKED] {rel(p)} missing: run the api step")
    return json.loads(p.read_text())


def published() -> dict:
    return load_json(CACHE / "api" / "published.json", {})


def step_api() -> None:
    pub = published()
    for n in range(1, 16):
        r = get(f"/extracts/{n}?collection=usa&version=2")
        if r.status_code != 200:
            raise SystemExit(f"[FAILED] extract {n}: HTTP {r.status_code} {red(r.text[:300])}")
        j = r.json()
        j.pop("email", None)
        save_json(CACHE / "api" / f"extract_{n:02d}.json", json.loads(red(json.dumps(j))))
        links = j.get("downloadLinks") or {}
        # IPUMS drops the links when the files expire; keep the first published hashes for good.
        seen = pub.setdefault(str(n), {})
        for kind, meta in links.items():
            if isinstance(meta, dict) and meta.get("sha256"):
                seen.setdefault(kind, {"bytes": meta.get("bytes"), "sha256": meta["sha256"],
                                       "first_seen": TODAY})
        seen["files_at_ipums"] = "available" if links else "expired"
        d = j["extractDefinition"]
        say("api", f"extract {n:2d}: {j['status']}, files {seen['files_at_ipums']}, "
                   f"{len(d['samples'])} samples, {len(d['variables'])} variables")
    save_json(CACHE / "api" / "published.json", pub)


# ---------------------------------------------------------------- download

def fetch_ranged(url: str, out: Path, total: int, want_sha: str, parts: int = 16) -> None:
    """Ranged parallel download into one preallocated .part file, renamed after the sha256 check.
    IPUMS serves one stream at about 40 KB/s (crime lane, 2026-09-23); ranges in parallel add up.
    Pattern from crime_selection_cohorts_2026_09_23/ipums_extract.py, without piece files."""
    tmp = out.with_name(out.name + ".part")
    with open(tmp, "wb") as f:
        f.truncate(total)
    size = -(-total // parts)
    spans = [(lo, min(total, lo + size) - 1) for lo in range(0, total, size)]

    def one(span):
        lo, hi = span
        pos = lo
        for attempt in range(1, 11):
            try:
                with requests.get(url, headers={"Authorization": api_key(), "Range": f"bytes={pos}-{hi}"},
                                  stream=True, timeout=(30, 120)) as r:
                    if r.status_code != 206:
                        raise requests.exceptions.ConnectionError(f"status {r.status_code}")
                    with open(tmp, "r+b") as f:
                        f.seek(pos)
                        for chunk in r.iter_content(chunk_size=1 << 16):
                            chunk = chunk[: hi + 1 - pos]
                            f.write(chunk)
                            pos += len(chunk)
                if pos == hi + 1:
                    return
            except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout) as exc:
                say("download", f"  {out.name} bytes {lo}-{hi}: {type(exc).__name__}, attempt {attempt}; resuming")
                time.sleep(min(60, 5 * attempt))
        raise SystemExit(f"[FAILED] {out.name}: range {lo}-{hi} incomplete")

    with ThreadPoolExecutor(parts) as ex:
        list(ex.map(one, spans))
    got = sha256(tmp)
    if got != want_sha:
        raise SystemExit(f"[FAILED] {out.name}: sha256 {got[:16]} is not IPUMS's {want_sha[:16]}")
    tmp.replace(out)


def fetch_published(n: int, kind: str, out: Path) -> str:
    """Download one published file of extract n unless a verified copy is already there."""
    pub = published().get(str(n), {})
    meta = pub.get(kind)
    if out.exists():
        if meta and sha256(out) != meta["sha256"]:
            raise SystemExit(f"[BLOCKED] {rel(out)} exists but does not match IPUMS's sha256")
        return "present"
    links = definition(n).get("downloadLinks") or {}
    if kind not in links or not meta:
        return "expired"
    out.parent.mkdir(parents=True, exist_ok=True)
    fetch_ranged(links[kind]["url"], out, int(meta["bytes"]), meta["sha256"],
                 parts=16 if int(meta["bytes"]) > 5_000_000 else 1)
    return "downloaded"


def link(src: Path, dst: Path) -> str:
    """Hard-link src to dst. Same inode already: skip. Different file at dst: stop."""
    if dst.exists():
        if dst.stat().st_ino == src.stat().st_ino:
            return "exists"
        if sha256(dst) == sha256(src):
            return "exists as a separate copy with the same sha256"
        raise SystemExit(f"[BLOCKED] {rel(dst)} exists and differs from {rel(src)}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.link(src, dst)
    return "linked"


def step_download() -> None:
    for n in (7, 8):
        e = EXTRACTS[n]
        t0 = time.time()
        say("download", f"extract {n}: {published().get(str(n), {}).get('data', {}).get('bytes', '?')} bytes to fetch "
                        f"unless present")
        got = fetch_published(n, "data", e["data"])
        size = f"{e['data'].stat().st_size / 1e6:.1f} MB, " if e["data"].exists() else ""
        say("download", f"extract {n}: data {got} ({size}{time.time() - t0:.0f} s)")
        say("download", f"extract {n}: DDI {fetch_published(n, 'ddiCodebook', e['ddi'])}")
        for src, ext in ((e["data"], "csv.gz"), (e["ddi"], "xml")):
            if src.exists():
                dst = CRIME / "_cache" / "ipums" / f"{e['crime_name']}.{ext}"
                say("download", f"extract {n}: {rel(dst)} {link(src, dst)}")


# ---------------------------------------------------------------- link

def held() -> list[int]:
    return [n for n, e in EXTRACTS.items() if e["data"] is not None and e["data"].exists()]


def ddi_path(n: int) -> Path | None:
    e = EXTRACTS[n]
    if e["ddi"] is not None and e["ddi"].exists():
        return e["ddi"]
    fetched = DL / f"usa_{n:05d}.xml"
    return fetched if fetched.exists() else None


def step_ddi() -> None:
    """The schooling lane kept only the basic .cbk; the Parquet types need the DDI."""
    for n in held():
        if EXTRACTS[n]["ddi"] is None:
            say("ddi", f"extract {n:2d}: DDI {fetch_published(n, 'ddiCodebook', DL / f'usa_{n:05d}.xml')}")


def step_link() -> None:
    for n in held():
        e = EXTRACTS[n]
        say("link", f"extract {n:2d}: {rel(LINK_DIR / name(n, 'csv.gz'))} {link(e['data'], LINK_DIR / name(n, 'csv.gz'))}")
        ddi = ddi_path(n)
        if ddi is None:
            say("link", f"extract {n:2d}: no DDI (files expired at IPUMS)")
        else:
            say("link", f"extract {n:2d}: {rel(LINK_DIR / name(n, 'xml'))} {link(ddi, LINK_DIR / name(n, 'xml'))}")


# ---------------------------------------------------------------- verify, count

def gate_rows() -> list[dict]:
    return load_json(CACHE / "gates.json", [])


def record_gate(extract, gate, expected, observed, ok, note="") -> None:
    rows = [g for g in gate_rows() if not (g["extract"] == extract and g["gate"] == gate)]
    rows.append(dict(extract=extract, gate=gate, expected=expected, observed=observed,
                     result="pass" if ok else "FAIL", note=note))
    save_json(CACHE / "gates.json", sorted(rows, key=lambda g: (str(g["extract"]), g["gate"])))


def step_verify() -> None:
    pub = published()
    for n in held():
        e, p = EXTRACTS[n], pub.get(str(n), {})
        got = sha256(e["data"])
        want = p.get("data", {}).get("sha256")
        if want:
            record_gate(n, "data sha256 = IPUMS", want, got, got == want)
        else:
            record_gate(n, "data sha256 = IPUMS", "not published (files expired at IPUMS)", got, True,
                        "first recorded hash of the June download")
        ddi = ddi_path(n)
        if ddi is not None and p.get("ddiCodebook"):
            dgot = sha256(ddi)
            record_gate(n, "DDI sha256 = IPUMS", p["ddiCodebook"]["sha256"], dgot, dgot == p["ddiCodebook"]["sha256"])
        want_bytes = p.get("data", {}).get("bytes")
        if want_bytes:
            record_gate(n, "data bytes = IPUMS", want_bytes, e["data"].stat().st_size,
                        int(want_bytes) == e["data"].stat().st_size)
        ok = (not want or got == want)
        say("verify", f"extract {n:2d}: sha256 {got[:16]} {'matches IPUMS' if want and ok else 'MISMATCH' if want else 'recorded (no IPUMS hash)'}")
        if not ok:
            raise SystemExit(f"[FAILED] extract {n}: sha256 mismatch")


def csv_rows(p: Path) -> int:
    counts = load_json(CACHE / "rows.json", {})
    digest = sha256(p)
    if digest in counts:
        return counts[digest]
    gz = subprocess.Popen(["gzip", "-dc", str(p)], stdout=subprocess.PIPE)
    wc = subprocess.run(["wc", "-l"], stdin=gz.stdout, capture_output=True, text=True, check=True)
    gz.stdout.close()
    if gz.wait() != 0:
        raise SystemExit(f"[FAILED] gzip -dc {rel(p)} exited {gz.returncode}")
    counts[digest] = int(wc.stdout.split()[0]) - 1
    save_json(CACHE / "rows.json", counts)
    return counts[digest]


def step_count() -> None:
    for n in held():
        rows = csv_rows(EXTRACTS[n]["data"])
        say("count", f"extract {n:2d}: {rows:,} CSV rows")


# ---------------------------------------------------------------- parquet

def parse_ddi(p: Path) -> dict:
    out = {}
    for v in ET.parse(p).getroot().iter(f"{{{NS['d']}}}var"):
        loc, fmt = v.find("d:location", NS), v.find("d:varFormat", NS)
        out[v.get("name")] = dict(
            width=int(loc.get("width")), dcml=int(v.get("dcml") or 0),
            kind=fmt.get("type") if fmt is not None else "numeric",
            label=(v.findtext("d:labl", default="", namespaces=NS) or "").strip(),
            cats=[(c.findtext("d:catValu", default="", namespaces=NS).strip(),
                   (c.findtext("d:labl", default="", namespaces=NS) or "").strip())
                  for c in v.findall("d:catgry", NS)])
    return out


def all_ddis() -> dict[int, dict]:
    return {n: parse_ddi(p) for n in held() if (p := ddi_path(n)) is not None}


def duck_type(width: int, dcml: int, kind: str) -> str:
    if kind == "character":
        return "VARCHAR"
    if dcml:
        return "DOUBLE"
    return "TINYINT" if width <= 2 else "SMALLINT" if width <= 4 else "INTEGER" if width <= 9 else "BIGINT"


def header(p: Path) -> list[str]:
    with gzip.open(p, "rt") as f:
        return next(csv.reader([f.readline()]))


def column_types(n: int, ddis: dict) -> list[dict]:
    cols = []
    for c in header(EXTRACTS[n]["data"]):
        own = ddis.get(n, {}).get(c)
        src = f"DDI of extract {n}" if own else None
        meta = own
        if meta is None:
            for m, d in sorted(ddis.items()):
                if c in d:
                    meta, src = d[c], f"DDI of extract {m}"
                    break
        if meta is None and c in FALLBACK_WIDTH:
            meta, src = dict(width=FALLBACK_WIDTH[c], dcml=0, kind="numeric", label=""), "IPUMS variable page width"
        if meta is None:
            raise SystemExit(f"[BLOCKED] extract {n}: no type source for column {c}")
        cols.append(dict(name=c, duck_type=duck_type(meta["width"], meta["dcml"], meta["kind"]),
                         width=meta["width"], dcml=meta["dcml"], label=meta.get("label", ""), type_source=src))
    return cols


def parquet_path(n: int) -> Path:
    return PARQ / name(n, "parquet")


def step_parquet() -> None:
    import duckdb
    ddis = all_ddis()
    man_p = PARQ / "manifest.json"
    man = load_json(man_p, {})
    con = duckdb.connect()
    for n in held():
        e, out = EXTRACTS[n], parquet_path(n)
        src_sha, rows = sha256(e["data"]), csv_rows(e["data"])
        if out.exists():
            got = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()[0]
            rec = man.get(out.name, {})
            if rec.get("source_sha256") == src_sha and got == rows:
                say("parquet", f"extract {n:2d}: {rel(out)} present, {got:,} rows")
                record_gate(n, "Parquet rows = CSV rows", rows, got, True)
                continue
            raise SystemExit(f"[BLOCKED] {rel(out)} exists but does not match its source; move it aside by hand")
        cols = column_types(n, ddis)
        spec = ", ".join(f"'{c['name']}': '{c['duck_type']}'" for c in cols)
        tmp = out.with_name(out.name + ".part")
        PARQ.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        con.execute(f"""COPY (SELECT * FROM read_csv('{e["data"]}', header=true, delim=',', quote='"',
                            auto_detect=false, compression='gzip', columns={{{spec}}}))
                        TO '{tmp}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 1000000,
                                    KV_METADATA {{ipums_extract: '{n}', source_sha256: '{src_sha}'}})""")
        got = con.execute(f"SELECT count(*) FROM read_parquet('{tmp}')").fetchone()[0]
        record_gate(n, "Parquet rows = CSV rows", rows, got, got == rows)
        if got != rows:
            raise SystemExit(f"[FAILED] extract {n}: Parquet {got:,} rows, CSV {rows:,}")
        tmp.replace(out)
        man[out.name] = dict(extract=n, source=rel(e["data"]), source_sha256=src_sha, rows=got,
                             bytes=out.stat().st_size, columns=cols, built=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        save_json(man_p, man)
        say("parquet", f"extract {n:2d}: {rel(out)} {got:,} rows, {out.stat().st_size / 1e6:.0f} MB, "
                       f"{time.time() - t0:.0f} s")


# ---------------------------------------------------------------- duckdb

def selections(n: int) -> dict[str, list[int]]:
    v = definition(n)["extractDefinition"]["variables"]
    return {k: [int(c) for c in x["caseSelections"]["general"]] for k, x in v.items() if "caseSelections" in x}


def pred_sql(n: int, cols: set[str]) -> str | None:
    """Extract n's case selection as SQL on general codes; None when cols lack a selection variable."""
    sel = selections(n)
    if any(v not in cols for v in sel):
        return None
    return " AND ".join(f'"{v}" IN ({", ".join(map(str, codes))})' for v, codes in sel.items()) or "TRUE"


def view(n: int) -> str:
    return f"usa_{n:05d}"


def flag_union(have: list[int]) -> str:
    """Every flag extract's records with all four flag columns, NULL where that extract lacks one."""
    parts = []
    for f, qs in FLAG_FILES.items():
        if f in have:
            cols = ", ".join(q if q in qs else f"NULL::TINYINT AS {q}" for q in QVARS)
            parts.append(f"SELECT {', '.join(KEYS)}, {cols}, {f} AS src FROM {view(f)}")
    return " UNION ALL ".join(parts)


def step_duckdb() -> None:
    import duckdb
    ddis = all_ddis()
    man = load_json(PARQ / "manifest.json", {})
    con = duckdb.connect(str(DB))
    have = []
    for n in held():
        p = parquet_path(n)
        if not p.exists():
            raise SystemExit(f"[BLOCKED] {rel(p)} missing: run the parquet step")
        con.execute(f"CREATE OR REPLACE VIEW {view(n)} AS SELECT * FROM read_parquet('{p}')")
        con.execute(f"COMMENT ON VIEW {view(n)} IS '{EXTRACTS[n]['slug']}: {EXTRACTS[n]['universe'].replace(chr(39), '')}'")
        have.append(n)
        say("duckdb", f"view {view(n)} -> {rel(p)}")
    con.execute("""CREATE OR REPLACE TABLE variables (extract INTEGER, name VARCHAR, label VARCHAR, width INTEGER,
                   dcml INTEGER, duck_type VARCHAR, type_source VARCHAR)""")
    con.executemany("INSERT INTO variables VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [(man[parquet_path(n).name]["extract"], c["name"], c["label"], c["width"], c["dcml"],
                      c["duck_type"], c["type_source"]) for n in have for c in man[parquet_path(n).name]["columns"]])
    con.execute("CREATE OR REPLACE TABLE value_labels (extract INTEGER, variable VARCHAR, code VARCHAR, code_int BIGINT, label VARCHAR)")
    con.executemany("INSERT INTO value_labels VALUES (?, ?, ?, TRY_CAST(? AS BIGINT), ?)",
                    [(n, var, code, code, lab) for n, d in ddis.items() for var, meta in d.items() for code, lab in meta["cats"]])
    say("duckdb", f"tables variables ({con.execute('SELECT count(*) FROM variables').fetchone()[0]:,} rows) and "
                  f"value_labels ({con.execute('SELECT count(*) FROM value_labels').fetchone()[0]:,} rows)")
    # One row per person record that any flag extract covers. NULL = flag not extracted for that
    # record; 0 = extracted and not allocated. q_extracts lists the covering extracts.
    maxes = ", ".join(f"max({q}) AS {q}" for q in QVARS)
    con.execute(f"""CREATE OR REPLACE VIEW qflags AS
        SELECT {', '.join(KEYS)}, {maxes}, list(src ORDER BY src) AS q_extracts
        FROM ({flag_union(have)}) GROUP BY {', '.join(KEYS)}""")
    con.execute("COMMENT ON VIEW qflags IS 'IPUMS allocation flags per person record from extracts 6, 13, 14 and 15; NULL means not extracted for that record, 0 means reported'")
    say("duckdb", "view qflags from extracts " + ", ".join(str(f) for f in FLAG_FILES if f in have))
    cols = {n: {r[0] for r in con.execute(f"DESCRIBE {view(n)}").fetchall()} for n in have}
    samples = {n: {r[0] for r in con.execute(f"SELECT DISTINCT SAMPLE FROM {view(n)}").fetchall()} for n in have}
    for b in have:
        if b in FLAG_FILES:
            continue
        over = []
        for f in FLAG_FILES:
            shared = samples[b] & samples[f] if f in have else set()
            if not shared:
                continue
            # Sharing samples is not enough: US-born extracts never meet Mexico-born extract 13.
            pf = pred_sql(f, cols[b])
            s_in = ", ".join(map(str, sorted(shared)))
            if pf is None or con.execute(f"SELECT count(*) FROM {view(b)} WHERE SAMPLE IN ({s_in}) AND {pf}").fetchone()[0]:
                over.append(f)
        if not over:
            continue
        extra = [q for q in QVARS if q not in cols[b]]
        con.execute(f"""CREATE OR REPLACE VIEW {view(b)}_q AS
            SELECT b.*, {', '.join(f'q.{q}' for q in extra)}, q.q_extracts
            FROM {view(b)} b LEFT JOIN qflags q USING ({', '.join(KEYS)})""")
        say("duckdb", f"view {view(b)}_q = {view(b)} + flags from extracts {', '.join(map(str, over))}")
    if all(n in have for n in SEX_SOURCES + (2,)):
        con.execute(sex_view_sql(samples[2]))
        say("duckdb", "view usa_00002_sex = usa_00002 + SEX from extracts "
                      + ", ".join(map(str, SEX_SOURCES)) + ", and by absence where an extract holds every man")
    con.close()


# Extract 2 has no SEX; extracts 3, 4, 8, 10 and 11 carry it for many of the same people. Where an
# extract holds every man of a group, a record of that group missing from it is a woman: 1980 ages
# 18-40 (extract 4) and 2023 US-born ages 18-40 (extract 8). The joins step tests the rule where
# SEX is observed directly: 1990 and 2000 against extract 4, 2010 against extract 8.
SEX_SOURCES = (3, 4, 8, 10, 11)


def sex_rules() -> dict[str, str]:
    us51 = ", ".join(map(str, selections(8)["BPL"]))
    return {"inferred: 1980, age 18-40, not in extract 4": "p.YEAR = 1980 AND p.AGE BETWEEN 18 AND 40",
            "inferred: 2023, US-born, age 18-40, not in extract 8":
                f"p.YEAR = 2023 AND p.AGE BETWEEN 18 AND 40 AND p.BPL IN ({us51})"}


def sex_view_sql(samples2: set[int]) -> str:
    keys, s2 = ", ".join(KEYS), ", ".join(map(str, sorted(samples2)))
    src = " UNION ALL ".join(f"SELECT {keys}, SEX, {n} AS src FROM {view(n)} WHERE SAMPLE IN ({s2})"
                             for n in SEX_SOURCES)
    rules = sex_rules()
    inferred = " OR ".join(f"({r})" for r in rules.values())
    label = " ".join(f"WHEN {r} THEN '{lab}'" for lab, r in rules.items())
    return f"""CREATE OR REPLACE VIEW usa_00002_sex AS
        WITH d AS (SELECT {keys}, max(SEX) AS SEX, list(src ORDER BY src) AS sex_extracts FROM ({src}) GROUP BY ALL)
        SELECT p.*, coalesce(d.SEX, CASE WHEN {inferred} THEN 2 END) AS SEX,
               CASE WHEN d.SEX IS NOT NULL THEN 'extract ' || array_to_string(d.sex_extracts, ', ') {label} END
                 AS sex_source
        FROM usa_00002 p LEFT JOIN d USING ({keys})"""


def sex_gates(con, have: list[int]) -> None:
    if not all(n in have for n in SEX_SOURCES + (2,)):
        return
    keys = ", ".join(KEYS)
    union = " UNION ALL ".join(f"SELECT {keys}, SEX FROM {view(n)}" for n in SEX_SOURCES)
    conflicts = con.execute(f"""SELECT count(*) FROM (SELECT {keys}, count(DISTINCT SEX) AS k FROM ({union})
                                GROUP BY ALL) WHERE k > 1""").fetchone()[0]
    record_gate("2 SEX", "SEX agrees across extracts 3, 4, 8, 10, 11", 0, conflicts, conflicts == 0)
    n4, men4 = con.execute(f"""SELECT count(*), count(*) FILTER (WHERE SEX = 1) FROM (
        SELECT {keys}, SEX FROM usa_00010 WHERE YEAR = 2000 AND AGE BETWEEN 18 AND 40
        UNION ALL SELECT {keys}, SEX FROM usa_00011 WHERE AGE BETWEEN 18 AND 40) x
        ANTI JOIN usa_00004 USING ({keys})""").fetchone()
    record_gate("2 SEX", "rule check: 1990/2000 ages 18-40 missing from extract 4 are all women", 0, men4,
                men4 == 0 and n4 > 0, f"{n4:,} records checked against SEX in extracts 10 and 11")
    us51 = ", ".join(map(str, selections(8)["BPL"]))
    n8, men8 = con.execute(f"""SELECT count(*), count(*) FILTER (WHERE SEX = 1) FROM (
        SELECT {keys}, SEX FROM usa_00010 WHERE YEAR = 2010 AND AGE BETWEEN 18 AND 40 AND BPL IN ({us51})) x
        ANTI JOIN usa_00008 USING ({keys})""").fetchone()
    record_gate("2 SEX", "rule check: 2010 US-born ages 18-40 missing from extract 8 are all women", 0, men8,
                men8 == 0 and n8 > 0, f"{n8:,} records checked against SEX in extract 10")
    rows = con.execute("""SELECT YEAR, count(*) AS records, count(SEX) AS with_sex,
            round(sum(PERWT) FILTER (WHERE SEX IS NOT NULL) / sum(PERWT), 4) AS weighted_share_with_sex,
            count(*) FILTER (WHERE sex_source LIKE 'inferred%') AS inferred_women,
            round(sum(PERWT) FILTER (WHERE SEX = 1) / sum(PERWT) FILTER (WHERE SEX = 2), 4) AS men_per_woman_where_known
        FROM usa_00002_sex GROUP BY YEAR ORDER BY YEAR""").fetchall()
    with open(OUT / "sex_coverage.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["YEAR", "records", "with_sex", "weighted_share_with_sex", "inferred_women", "men_per_woman_where_known"])
        w.writerows(rows)
    say("joins", f"usa_00002_sex: SEX conflicts {conflicts}; rule checks {men4} men of {n4:,} and {men8} of {n8:,}; "
                 f"coverage by year -> {rel(OUT / 'sex_coverage.csv')}")


# ---------------------------------------------------------------- joins and gates

def one_way_note(a: int, b: int, cols: dict, a_lacks: bool) -> str:
    """Name the extract that cannot be filtered to the other's universe, and why."""
    short, full = (a, b) if a_lacks else (b, a)
    missing = [v for v in selections(full) if v not in cols[short]]
    return (f"one-way: extract {short} has no {', '.join(missing)}, so only extract {full}'s records "
            f"were checked against it")

def step_joins() -> None:
    import duckdb
    con = duckdb.connect(str(DB))
    have = [n for n in held() if parquet_path(n).exists()]
    cols = {n: [r[0] for r in con.execute(f"DESCRIBE {view(n)}").fetchall()] for n in have}
    samples = {n: {r[0] for r in con.execute(f"SELECT DISTINCT SAMPLE FROM {view(n)}").fetchall()} for n in have}
    for n in have:
        api_samples = definition(n)["extractDefinition"]["samples"]
        record_gate(n, "samples in data = samples requested", len(api_samples), len(samples[n]),
                    len(api_samples) == len(samples[n]))
        dups = con.execute(f"""SELECT count(*) FROM (SELECT {', '.join(KEYS)} FROM {view(n)}
                              GROUP BY ALL HAVING count(*) > 1)""").fetchone()[0]
        record_gate(n, "person key unique", 0, dups, dups == 0, "key = YEAR, SAMPLE, SERIAL, PERNUM")
        own = pred_sql(n, set(cols[n]))
        bad = con.execute(f"SELECT count(*) FROM {view(n)} WHERE NOT ({own})").fetchone()[0]
        record_gate(n, "case selection holds", 0, bad, bad == 0, own if len(own) < 120 else own[:117] + "...")
        say("joins", f"extract {n:2d}: {len(samples[n])} samples, {dups} duplicate keys, {bad} records outside its selection")
    over = ", ".join(f"count(*) FILTER (WHERE n_{q} > 1)" for q in QVARS)
    distinct = ", ".join(f"count(DISTINCT {q}) AS n_{q}" for q in QVARS)
    conflicts = con.execute(f"""SELECT {over} FROM (SELECT {distinct} FROM ({flag_union(have)})
                                GROUP BY {', '.join(KEYS)})""").fetchone()
    for q, c in zip(QVARS, conflicts):
        record_gate("qflags", f"{q} agrees across flag extracts", 0, c, c == 0)
    say("joins", "qflags: records whose flag differs between extracts: " + ", ".join(f"{q} {c}" for q, c in zip(QVARS, conflicts)))
    OUT.mkdir(parents=True, exist_ok=True)
    sex_gates(con, have)

    rows = []
    for i, a in enumerate(have):
        for b in have[i + 1:]:
            shared = sorted(samples[a] & samples[b])
            if not shared:
                continue
            s_in = ", ".join(map(str, shared))
            pb_on_a, pa_on_b = pred_sql(b, set(cols[a])), pred_sql(a, set(cols[b]))
            A = f"(SELECT * FROM {view(a)} WHERE SAMPLE IN ({s_in}) AND {pb_on_a or 'TRUE'})"
            B = f"(SELECT * FROM {view(b)} WHERE SAMPLE IN ({s_in}) AND {pa_on_b or 'TRUE'})"
            if pb_on_a is None and pa_on_b is None:
                rows.append(dict(a=a, b=b, shared_samples=len(shared), n_a=None, n_b=None, matched=None,
                                 rate_a=None, rate_b=None, columns_compared=0, disagreements="{}", result="untestable",
                                 note="neither extract carries the other's selection variables"))
                continue
            n_a = con.execute(f"SELECT count(*) FROM {A}").fetchone()[0] if pb_on_a else None
            n_b = con.execute(f"SELECT count(*) FROM {B}").fetchone()[0] if pa_on_b else None
            common = [c for c in cols[a] if c in cols[b] and c not in KEYS]
            diff = ", ".join(f'sum(CASE WHEN a."{c}" IS DISTINCT FROM b."{c}" THEN 1 ELSE 0 END)' for c in common)
            res = con.execute(f"SELECT count(*){', ' + diff if diff else ''} FROM {A} a JOIN {B} b "
                              f"USING ({', '.join(KEYS)})").fetchone()
            matched, dis = res[0], {c: int(x) for c, x in zip(common, res[1:]) if x}
            ok = (n_a is None or matched == n_a) and (n_b is None or matched == n_b)
            empty = (n_a == 0) or (n_b == 0)
            rows.append(dict(a=a, b=b, shared_samples=len(shared), n_a=n_a, n_b=n_b, matched=matched,
                             rate_a=round(matched / n_a, 6) if n_a else None,
                             rate_b=round(matched / n_b, 6) if n_b else None,
                             columns_compared=len(common), disagreements=json.dumps(dis),
                             result="disjoint" if empty and ok else ("pass" if ok and not dis else
                                                                     "keys pass, values differ" if ok else "FAIL"),
                             note="" if pb_on_a and pa_on_b else one_way_note(a, b, cols, pb_on_a is None)))
            r = rows[-1]
            say("joins", f"{a:2d} x {b:2d}: {r['result']}, matched {matched:,} of "
                         f"{n_a if n_a is not None else '?'} / {n_b if n_b is not None else '?'}"
                         + (f"; differing columns {dis}" if dis else ""))
    OUT.mkdir(parents=True, exist_ok=True)
    fields = ["a", "b", "shared_samples", "n_a", "n_b", "matched", "rate_a", "rate_b", "columns_compared",
              "disagreements", "result", "note"]
    with open(OUT / "joins.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    gates = gate_rows()
    with open(OUT / "gates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["extract", "gate", "expected", "observed", "result", "note"])
        w.writeheader()
        w.writerows(gates)
    con.execute(f"CREATE OR REPLACE TABLE joins AS SELECT * FROM read_csv('{OUT / 'joins.csv'}', header=true)")
    con.execute(f"CREATE OR REPLACE TABLE gates AS SELECT * FROM read_csv('{OUT / 'gates.csv'}', header=true, all_varchar=true)")
    con.close()
    failed = [g for g in gates if g["result"] != "pass"] + [r for r in rows if r["result"] == "FAIL"]
    say("joins", f"{len(rows)} pairs, {len(gates)} gates, {len(failed)} failures -> {rel(OUT / 'joins.csv')}, {rel(OUT / 'gates.csv')}")


# ---------------------------------------------------------------- catalog

def compact(names: list[str]) -> str:
    """us2005a, us2006a, ..., us2024a -> us2005a-us2024a."""
    out, run = [], []
    for s in names:
        m = re.fullmatch(r"us(\d{4})a", s)
        if m and run and int(m.group(1)) == int(run[-1][2:6]) + 1:
            run.append(s)
            continue
        if run:
            out.append(run[0] if len(run) == 1 else f"{run[0]}-{run[-1]}")
        run = [s] if m else []
        if not m:
            out.append(s)
    if run:
        out.append(run[0] if len(run) == 1 else f"{run[0]}-{run[-1]}")
    return ", ".join(out)


def catalog_records() -> list[dict]:
    pub, man = published(), load_json(PARQ / "manifest.json", {})
    counts = load_json(CACHE / "rows.json", {})
    recs = []
    for n, e in EXTRACTS.items():
        j = definition(n)
        d = j["extractDefinition"]
        v = d["variables"]
        is_held = e["data"] is not None and e["data"].exists()
        digest = sha256(e["data"]) if is_held else None
        files = pub.get(str(n), {}).get("files_at_ipums")
        status = "superseded" if n == 1 else "held" if is_held else "expired" if files == "expired" else "not held"
        ddi = LINK_DIR / name(n, "xml")
        pq = man.get(name(n, "parquet"), {})
        recs.append(dict(
            number=n, file=rel(LINK_DIR / name(n, "csv.gz")) if is_held else None, slug=e["slug"], status=status,
            files_at_ipums=files, description=d.get("description"),
            samples=list(d["samples"]), samples_compact=compact(list(d["samples"])),
            universe=e["universe"],
            case_selection={k: x["caseSelections"]["general"] for k, x in v.items() if "caseSelections" in x},
            quality_flags=[k for k, x in v.items() if x.get("dataQualityFlags")],
            variables=[k for k, x in v.items() if not x.get("preselected")],
            technical_variables=[k for k, x in v.items() if x.get("preselected")],
            data_columns=[c["name"] for c in pq.get("columns", [])],
            rows=counts.get(digest) if digest else None, bytes=e["data"].stat().st_size if is_held else None,
            sha256=digest, sha256_ipums=pub.get(str(n), {}).get("data", {}).get("sha256"),
            ddi=rel(ddi) if ddi.exists() else None,
            parquet=rel(parquet_path(n)) if parquet_path(n).exists() else None,
            parquet_bytes=parquet_path(n).stat().st_size if parquet_path(n).exists() else None,
            lane=e["lane"], same_file_as=same_inode(n) if is_held else [],
            used_in=e["used"], beyond_its_lane=e["beyond"]))
    return recs


def same_inode(n: int) -> list[str]:
    """Every known name of extract n's data file: the lane cache paths the store links to."""
    e = EXTRACTS[n]
    cands = [e["data"], LINK_DIR / name(n, "csv.gz")]
    if e.get("crime_name"):
        cands.append(CRIME / "_cache" / "ipums" / f"{e['crime_name']}.csv.gz")
    ino = e["data"].stat().st_ino
    return sorted({rel(p) for p in cands if p.exists() and p.stat().st_ino == ino})


def md_catalog(recs: list[dict]) -> str:
    lines = [
        "# IPUMS USA extracts on the operator's account",
        "",
        f"Generated by `infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py` ({TODAY}); do not edit by hand.",
        "Every held file is a hard link: the lane cache paths in `catalog.json` (`same_file_as`) are the same bytes.",
        "The typed Parquet copies and the join views are in `sources/immigration-fiscal/derived/ipums_usa/` and",
        "`sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb`. Every extract also carries the IPUMS",
        "technical variables YEAR, SAMPLE, SERIAL, HHWT, CLUSTER, STRATA, GQ, PERNUM, PERWT (and CBSERIAL",
        "where requested) and the detailed twin of each variable that has one (BPLD, EDUCD, ...).",
        "",
        "| # | File | Status | Samples | Universe | Variables (flags) | Rows | Bytes | sha256 | Used by |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in recs:
        flags = f" (flags: {', '.join(r['quality_flags'])})" if r["quality_flags"] else ""
        used = "; ".join(r["used_in"])
        lines.append(
            f"| {r['number']} | {('`' + Path(r['file']).name + '`') if r['file'] else '`usa_' + format(r['number'], '05d') + '` (' + r['slug'] + ')'} "
            f"| {r['status']}{'' if r['files_at_ipums'] == 'available' else ', files expired at IPUMS'} "
            f"| {r['samples_compact']} | {r['universe']} | {' '.join(r['variables'])}{flags} "
            f"| {format(r['rows'], ',') if r['rows'] is not None else '-'} "
            f"| {format(r['bytes'], ',') if r['bytes'] is not None else '-'} "
            f"| {('`' + r['sha256'] + '`') if r['sha256'] else '-'} | {used} |")
    lines += ["", "## What each extract can answer beyond its lane", ""]
    lines += [f"- **{r['number']}.** {r['beyond_its_lane']}" for r in recs]
    lines.append("")
    return "\n".join(lines)


def step_catalog() -> None:
    recs = catalog_records()
    doc = dict(generated=TODAY, generator=rel(Path(__file__)), store=rel(LINK_DIR),
               parquet_dir=rel(PARQ), duckdb=rel(DB), extracts=recs)
    for p in (STORE / "catalog.json", OUT / "catalog.json"):
        save_json(p, doc)
    for p in (STORE / "CATALOG.md", OUT / "CATALOG.md"):
        p.write_text(md_catalog(recs))
    import duckdb
    flat = [{k: json.dumps(v) if isinstance(v, dict) else v for k, v in r.items()} for r in recs]
    save_json(CACHE / "catalog_rows.json", flat)
    con = duckdb.connect(str(DB))
    con.execute(f"CREATE OR REPLACE TABLE catalog AS SELECT * FROM read_json('{CACHE / 'catalog_rows.json'}', "
                f"format='array') ORDER BY number")
    n = con.execute("SELECT count(*) FROM catalog").fetchone()[0]
    con.close()
    say("catalog", f"{len(recs)} extracts -> {rel(STORE / 'catalog.json')}, {rel(STORE / 'CATALOG.md')}; "
                   f"DuckDB table catalog {n} rows")


# ---------------------------------------------------------------- register

def step_register() -> None:
    text = MANIFEST.read_text()
    head = "## IPUMS USA extracts 2–15, one store (2026-09-23)"
    add = []
    if head not in text:
        add += ["", head, "",
                "Registered in `research/immigration-dataset-register.md` under IPUMS_USA_EXTRACTS_2026_09_23; "
                "catalog in `external/ipums/usa_extract/CATALOG.md`. Paths are hard links to the lane caches.",
                ""]
    for n in held():
        for p in (LINK_DIR / name(n, "csv.gz"), LINK_DIR / name(n, "xml")):
            if not p.exists():
                continue
            relp = str(p.relative_to(MANIFEST.parent))
            line = f"{sha256(p)}  {relp}  (IPUMS USA extract {n}, added {TODAY})"
            if relp not in text:
                add.append(line)
    if add:
        with open(MANIFEST, "a") as f:
            f.write("\n".join(add) + "\n")
    say("register", f"MANIFEST.md: {sum(1 for x in add if re.match(r'[0-9a-f]{64}  ', x))} sha256 lines appended")
    readme = IPUMS / "README.md"
    section = "## Extracts 2–15 in one store (2026-09-23)"
    where = rel(LINK_DIR).removeprefix("sources/immigration-fiscal/data/external/ipums/")
    if section not in readme.read_text():
        with open(readme, "a") as f:
            f.write(f"""
{section}
- Every IPUMS USA extract on the operator's account is catalogued in `usa_extract/CATALOG.md` and
  `usa_extract/catalog.json` (samples, universe, variables, rows, bytes, sha256, lanes). Extract 1 was
  superseded by 2; the files of 1 and 2 have expired at IPUMS, so `usa_00002.csv.gz` is the only copy
  and has no DDI.
- Held files are `{where}/usa_000NN_<samples>_<universe>[_<content>].csv.gz` with the DDI as `.xml`,
  hard links to the lane caches, not second copies. `build/load_ipums_borjas_panel.py` resolves
  `usa_00002.csv.gz` by exact name (4767db7), so the other names here do not reach the Borjas panel.
- Typed Parquet: `sources/immigration-fiscal/derived/ipums_usa/`. DuckDB with one view per extract, the
  allocation-flag view `qflags`, `usa_000NN_q` join views, `usa_00002_sex`, and the tables `catalog`,
  `variables`, `value_labels`, `joins` and `gates`: `sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb`.
- Rebuild: `infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py` (README there).
""")
        say("register", f"{rel(readme)}: section appended")
    else:
        say("register", f"{rel(readme)}: section present")


STEPS = {"api": step_api, "download": step_download, "ddi": step_ddi, "link": step_link, "verify": step_verify,
         "count": step_count, "parquet": step_parquet, "duckdb": step_duckdb, "joins": step_joins,
         "catalog": step_catalog, "register": step_register}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("steps", nargs="*", help=f"any of {', '.join(STEPS)}; none = all, in order")
    a = p.parse_args()
    unknown = [s for s in a.steps if s not in STEPS]
    if unknown:
        p.error(f"unknown step(s) {unknown}; choose from {list(STEPS)}")
    for s in a.steps or list(STEPS):
        t0 = time.time()
        STEPS[s]()
        say(s, f"done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        if exc.code not in (None, 0):
            print(red(str(exc.code)), file=sys.stderr)
            sys.exit(1)
        raise
