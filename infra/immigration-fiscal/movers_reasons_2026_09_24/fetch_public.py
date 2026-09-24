#!/usr/bin/env python3
"""Fetch the public inputs beside the IPUMS extracts into _cache/ (idempotent, content-checked).

  cps_api   Census public ASEC microdata via api.census.gov, movers only (MIGSAME=2), for
            2014, 2015 (diagnostic) and 2019-2025 (the brief's check on IPUMS coding), and the
            NXTRES value labels for 2019 and 2025 (the two code schemes).
  acs       ACS 1-year state and county tables 2005-2024 (no standard 2020 release):
            population, Hispanic and Mexican-origin counts, median gross rent, median home value,
            median household income.
  acs5      The same variables from the ACS 5-year release, vintages 2009-2024 (composition).
  s2s       ACS state-to-state migration flow tables 2005-2024 (Census published, with MOEs).
  cps_a1    Census CPS historical migration Table A-1 (national movers by type, 1948-2025).
  irs       IRS SOI state-to-state inflow/outflow files 2011-12..2022-23, the published
            California workbook for 2022-23, the 2022-23 and 2011-12 users' guides, and
            county-to-county outflow files for 2018-19..2022-23.
  itep      ITEP Who Pays? 7th edition pages for California and Texas.
  lit       The moving-cost sources the ledger reads (AMSA fact sheet, Bayer-Juessen, Kennan-Walker,
            IRS SOI Publication 1304 Table 1.4 for tax years 2014-2017).
  ipums_doc IPUMS's published case counts for MIGRATE1 and WHYMOVE (the extract gate).

Fetches go through curl (Python urllib fails TLS here). The Census key travels to curl on
stdin inside a config line, never in argv; every logged URL passes through redact().

Usage, from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/fetch_public.py all
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
MANIFEST = CACHE / "public_manifest.json"
ACS_YEARS = [y for y in range(2005, 2025) if y != 2020]
CPS_API_YEARS = [2014, 2015] + list(range(2019, 2026))
CPS_API_VARS = ["GESTFIPS", "MIG_ST", "MIGSAME", "NXTRES", "I_NXTRES", "FL_665", "A_AGE", "PENATVTY",
                "PEHSPNON", "PRDTRACE", "A_HGA", "PRCITSHP", "MARSUPWT"]
ACS_VARS = ["NAME", "B01003_001E", "B03001_001E", "B03001_003E", "B03001_004E", "B25064_001E",
            "B25077_001E", "B19013_001E"]
IRS_PAIRS = ["1112", "1213", "1314", "1415", "1516", "1617", "1718", "1819", "1920", "2021", "2122", "2223"]
IRS_COUNTY_PAIRS = ["1819", "1920", "2021", "2122", "2223"]


def redact(s: str) -> str:
    return re.sub(r"key=[^&\s\"']+", "key=<redacted>", s)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def record(path: Path, url: str) -> None:
    m = load_manifest()
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    m[str(path.relative_to(CACHE))] = {"url": redact(url), "bytes": path.stat().st_size, "sha256": h,
                                       "fetched": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")


def curl_to(url: str, out: Path, *, http11: bool = False, attempts: int = 4) -> bool:
    """Download url to out through a stdin config so a key in the URL never reaches argv."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".part")
    cfg = f'url = "{url}"\noutput = "{tmp}"\n'
    extra = ["--http1.1"] if http11 else []
    for a in range(1, attempts + 1):
        r = subprocess.run(["curl", "-sS", "--fail", "-L", "--max-time", "600", *extra, "--config", "-"],
                           input=cfg.encode(), capture_output=True)
        if r.returncode == 0 and tmp.exists():
            tmp.replace(out)
            return True
        print(f"  ! attempt {a} {redact(url)}: rc={r.returncode} {redact(r.stderr.decode(errors='replace'))[:160]}")
        time.sleep(4 * a)
    if tmp.exists():
        tmp.unlink()
    return False


def census_key() -> str:
    key = os.environ.get("CENSUS_API_KEY", "")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY missing; source acquire/config.local.env with set -a")
    return key


def fetch_json_rows(url: str, out: Path, expect_first: str) -> None:
    if out.exists():
        try:
            rows = json.loads(out.read_text())
            if rows and rows[0][0] == expect_first:
                return
        except (json.JSONDecodeError, IndexError, KeyError):
            pass
    if not curl_to(url, out):
        raise SystemExit(f"[FAILED] {redact(url)}")
    rows = json.loads(out.read_text())
    if not rows or rows[0][0] != expect_first or len(rows) < 2:
        raise SystemExit(f"[FAILED] unexpected content from {redact(url)}: {str(rows)[:200]}")
    record(out, url)
    print(f"  ok {out.relative_to(CACHE)} rows={len(rows) - 1}")


def cps_api() -> None:
    key = census_key()
    for y in CPS_API_YEARS:
        url = (f"https://api.census.gov/data/{y}/cps/asec/mar?get={','.join(CPS_API_VARS)}"
               f"&MIGSAME=2&key={key}")
        fetch_json_rows(url, CACHE / "cps_api" / f"asec_{y}_movers.json", "GESTFIPS")
    # the Census value labels of the reason variable, old and new code schemes (no key needed)
    for y in (2019, 2025):
        url = f"https://api.census.gov/data/{y}/cps/asec/mar/variables/NXTRES.json"
        out = CACHE / "census_meta" / f"NXTRES_{y}.json"
        test = lambda b: b"better neighborhood" in b and b"Main reason for moving" in b
        if not (out.exists() and test(out.read_bytes())):
            if not curl_to(url, out) or not test(out.read_bytes()):
                raise SystemExit(f"[FAILED] {url}")
            print(f"  ok {out.relative_to(CACHE)}")
        if str(out.relative_to(CACHE)) not in load_manifest():
            record(out, url)


def acs() -> None:
    key = census_key()
    for y in ACS_YEARS:
        for geo, tag in (("state:*", "state"), ("county:*", "county")):
            url = f"https://api.census.gov/data/{y}/acs/acs1?get={','.join(ACS_VARS)}&for={geo}&key={key}"
            fetch_json_rows(url, CACHE / "acs" / f"acs1_{tag}_{y}.json", "NAME")


def acs5() -> None:
    """ACS 5-year state and county composition and controls, vintages 2009-2024. The 1-year
    detailed Hispanic-origin table B03001 is filtered for 4-16 states and ~85% of counties each
    year, so the Mexican-origin share comes from the unfiltered 5-year release."""
    key = census_key()
    for y in range(2009, 2025):
        for geo, tag in (("state:*", "state"), ("county:*", "county")):
            url = f"https://api.census.gov/data/{y}/acs/acs5?get={','.join(ACS_VARS)}&for={geo}&key={key}"
            fetch_json_rows(url, CACHE / "acs" / f"acs5_{tag}_{y}.json", "NAME")


def s2s() -> None:
    page = CACHE / "acs_s2s" / "index.html"
    idx = "https://www.census.gov/data/tables/time-series/demo/geographic-mobility/state-to-state-migration.html"
    if not page.exists() and not curl_to(idx, page):
        raise SystemExit("[FAILED] state-to-state index page")
    links = sorted(set(re.findall(r'href="(//www2\.census\.gov/[^"]*state-to-state-migration/[^"]*\.xlsx?)"',
                                  page.read_text(errors="replace"))))
    single = [l for l in links if re.search(r"(table|Table)_?(\d{4})(_T13[^/]*)?\.xlsx?$", l)
              and not re.search(r"_\d{4}_\d{4}\.xls", l) and "flows_tables" not in l]
    for l in single:
        out = CACHE / "acs_s2s" / l.rsplit("/", 1)[1]
        if out.exists() and out.read_bytes()[:4] in (b"\xd0\xcf\x11\xe0", b"PK\x03\x04"):
            continue
        if not curl_to("https:" + l, out):
            raise SystemExit(f"[FAILED] {l}")
        if out.read_bytes()[:4] not in (b"\xd0\xcf\x11\xe0", b"PK\x03\x04"):
            raise SystemExit(f"[FAILED] {out.name} is not an Excel file")
        record(out, "https:" + l)
        print(f"  ok {out.relative_to(CACHE)}")


def cps_a1() -> None:
    url = ("https://www2.census.gov/programs-surveys/demo/tables/geographic-mobility/time-series/"
           "historic/hst_mig_a_1.xlsx")
    out = CACHE / "census_cps_tables" / "hst_mig_a_1.xlsx"
    if not (out.exists() and out.read_bytes()[:4] == b"PK\x03\x04"):
        if not curl_to(url, out) or out.read_bytes()[:4] != b"PK\x03\x04":
            raise SystemExit(f"[FAILED] {url}")
        print(f"  ok {out.relative_to(CACHE)}")
    if str(out.relative_to(CACHE)) not in load_manifest():
        record(out, url)


def irs() -> None:
    base = "https://www.irs.gov/pub/irs-soi/"
    names = [f"state{d}flow{p}.csv" for p in IRS_PAIRS for d in ("in", "out")]
    names += [f"countyoutflow{p}.csv" for p in IRS_COUNTY_PAIRS]
    for n in names:
        out = CACHE / "irs" / n
        ok = out.exists() and re.search(r"y1_statefips|y2_statefips", out.open(errors="replace").readline())
        if ok:
            continue
        if not curl_to(base + n, out, http11=True):
            raise SystemExit(f"[FAILED] {n}")
        if not re.search(r"y1_statefips|y2_statefips", out.open(errors="replace").readline()):
            raise SystemExit(f"[FAILED] {n}: header lacks statefips columns")
        record(out, base + n)
        print(f"  ok {out.relative_to(CACHE)}")
    out = CACHE / "irs" / "2223ca.xlsx"  # the published California state workbook, for gate G3
    if not (out.exists() and out.read_bytes()[:4] == b"PK\x03\x04"):
        if not curl_to(base + "2223ca.xlsx", out, http11=True) or out.read_bytes()[:4] != b"PK\x03\x04":
            raise SystemExit("[FAILED] 2223ca.xlsx")
        print(f"  ok {out.relative_to(CACHE)}")
    if "irs/2223ca.xlsx" not in load_manifest():
        record(out, base + "2223ca.xlsx")
    for n in ("2223inpublicmigdoc.pdf", "1112inpublicmigdoc.pdf"):
        out = CACHE / "irs" / n
        if out.exists() and out.read_bytes()[:5] == b"%PDF-":
            continue
        if curl_to(base + n, out, http11=True) and out.read_bytes()[:5] == b"%PDF-":
            record(out, base + n)
            print(f"  ok {out.relative_to(CACHE)}")
        else:
            print(f"  ! {n} unavailable")


def itep() -> None:
    """ITEP Who Pays? 7th edition state pages (2024 tax law at 2023 incomes, non-elderly families):
    state and local taxes as shares of family income by income group, California and Texas."""
    for s in ("california", "texas"):
        out = CACHE / "itep" / f"{s}.html"
        test = lambda b: b"TOTAL TAXES" in b and b"Who Pays? 7th Edition" in b
        if out.exists() and test(out.read_bytes()):
            continue
        url = f"https://itep.org/whopays/{s}/"
        if not curl_to(url, out) or not test(out.read_bytes()):
            raise SystemExit(f"[FAILED] {url}")
        record(out, url)
        print(f"  ok {out.relative_to(CACHE)}")


LIT = {  # moving-cost sources the ledger reads; the literature notes quote them (lit/moving_costs_and_surveys.md)
    "mibox_industry_fact_sheet.pdf": ("https://getmiboxsystem.com/the-market/industry_fact_sheet", b"%PDF-"),
    "bayer_juessen_iza_dp3330.pdf": ("https://docs.iza.org/dp3330.pdf", b"%PDF-"),
    "kennan_walker_2011_ecta4657.pdf": ("https://users.ssc.wisc.edu/~jfkennan/research/ECTA4657.pdf", b"%PDF-"),
    "14in14ar.xls": ("https://www.irs.gov/pub/irs-soi/14in14ar.xls", b"\xd0\xcf\x11\xe0"),
    "15in14ar.xls": ("https://www.irs.gov/pub/irs-soi/15in14ar.xls", b"\xd0\xcf\x11\xe0"),
    "16in14ar.xls": ("https://www.irs.gov/pub/irs-soi/16in14ar.xls", b"\xd0\xcf\x11\xe0"),
    "17in14ar.xls": ("https://www.irs.gov/pub/irs-soi/17in14ar.xls", b"\xd0\xcf\x11\xe0"),
}


def lit() -> None:
    m = load_manifest()
    for name, (url, magic) in LIT.items():
        out = CACHE / "lit" / name
        if not (out.exists() and out.read_bytes()[:len(magic)] == magic):
            if not curl_to(url, out, http11="irs.gov" in url) or out.read_bytes()[:len(magic)] != magic:
                raise SystemExit(f"[FAILED] {url}")
            print(f"  ok {out.relative_to(CACHE)}")
        if str(out.relative_to(CACHE)) not in m:
            record(out, url)
        if name.endswith(".pdf"):
            txt = out.with_suffix(".txt")
            if not txt.exists():
                subprocess.run(["pdftotext", "-layout", str(out), str(txt)], check=True)


def ipums_doc() -> None:
    """IPUMS's published per-sample case counts (the site's frequency JSON) and the variable pages
    that map its sample ids to names; the extract gate compares the data against them."""
    for v in ("MIGRATE1", "WHYMOVE"):
        for url, out, test in ((f"https://cps.ipums.org/cps-action/variables/{v}",
                                CACHE / "ipums_doc" / f"{v}.html", lambda b: b"codeData" in b),
                               (f"https://cps.ipums.org/cps-action/frequencies/{v}",
                                CACHE / "ipums_doc" / f"{v}_frequencies.json", lambda b: b[:1] == b"{")):
            if out.exists() and test(out.read_bytes()):
                continue
            if not curl_to(url, out) or not test(out.read_bytes()):
                raise SystemExit(f"[FAILED] {url}")
            record(out, url)
            print(f"  ok {out.relative_to(CACHE)}")


def main() -> None:
    p = argparse.ArgumentParser()
    steps = {"cps_api": cps_api, "acs": acs, "acs5": acs5, "s2s": s2s, "cps_a1": cps_a1, "irs": irs,
             "itep": itep, "lit": lit, "ipums_doc": ipums_doc}
    p.add_argument("what", choices=["all", *steps])
    a = p.parse_args()
    for name, fn in steps.items():
        if a.what in ("all", name):
            print(f"== {name}", flush=True)
            fn()


if __name__ == "__main__":
    main()
