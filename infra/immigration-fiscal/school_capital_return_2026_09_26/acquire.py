"""Stage the primary files for the school capital return lane (2026-09-26).

Downloads each source into `_cache/` (skipped when present, unless --refresh), converts the
legacy .xls workbooks and the OMB documents to text the main script can read without extra
wheels, and writes `derived/sources.csv` (file, url, bytes, sha256, fetched_utc).

    uv run --no-project --with xlrd python3 \
        infra/immigration-fiscal/school_capital_return_2026_09_26/acquire.py [--refresh]

xlrd is needed only here: the repo venv lacks it, so `capital_return.py` reads the CSV
extracts written below and checks that each one still matches its source workbook's sha256.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# file name in _cache -> URL (all public; no API key is used anywhere in this lane)
SOURCES = {
    # evidence that BEA's detailed fixed-asset files cover private assets and consumer durables only
    "fa_details_index.html": "https://apps.bea.gov/national/FA2004/Details/Index.htm",
    "fa_Section7All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section7All_xls.xlsx",
    "fa_TablesRegister.txt": "https://apps.bea.gov/national/FixedAssets/Release/TXT/TablesRegister.txt",
    "nipa_Section5All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section5All_xls.xlsx",
    "nipa_Section7All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx",
    "nipa_TablesRegister.txt": "https://apps.bea.gov/national/Release/TXT/TablesRegister.txt",
    "nipa_SeriesRegister.txt": "https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt",
    "c30_stateha.xls": "https://www.census.gov/construction/c30/xls/stateha.xls",
    "c30_stateha1.xls": "https://www.census.gov/construction/c30/xls/stateha1.xls",
    "c30_stateha2.xlsx": "https://www.census.gov/construction/c30/xlsx/stateha2.xlsx",
    "c30_state.xlsx": "https://www.census.gov/construction/c30/xlsx/state.xlsx",
    "cog_22slsstab1.xlsx": "https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx",
    "elsec24_sumtables.xlsx": "https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24_sumtables.xlsx",
    "elsec19_sumtables.xls": "https://www2.census.gov/programs-surveys/school-finances/tables/2019/secondary-education-finance/elsec19_sumtables.xls",
    "nces_d23_tabn236.10.xlsx": "https://nces.ed.gov/programs/digest/d23/tables/xls/tabn236.10.xlsx",
    "treasury_real_yield_2024.csv": ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
                                     "daily-treasury-rates.csv/2024/all?type=daily_treasury_real_yield_curve"
                                     "&field_tdr_date_value=2024&page&_format=csv"),
    "omb_a4_2023.pdf": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/11/CircularA-4.pdf",
    "omb_a4_2003.html": "https://obamawhitehouse.archives.gov/omb/circulars_a004_a-4/",
    "omb_m25_15.pdf": "https://www.whitehouse.gov/wp-content/uploads/2025/03/M-25-15-Recission-and-Reinstatement-of-Circular-A-4.pdf",
}
XLS_TO_CSV = {"c30_stateha.xls": None, "c30_stateha1.xls": None, "elsec19_sumtables.xls": ["9", "10", "19"]}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(name: str, url: str, refresh: bool) -> None:
    out = CACHE / name
    if out.exists() and out.stat().st_size > 0 and not refresh:
        return
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
    if len(body) < 1000:
        raise SystemExit(f"[BLOCKED] {name}: {len(body)} bytes from {url}")
    out.write_bytes(body)


def xls_to_csv(name: str, sheets: list[str] | None) -> None:
    import xlrd  # only here; see module docstring
    src = CACHE / name
    wb = xlrd.open_workbook(str(src))
    for sh in wb.sheets():
        if sheets is not None and sh.name not in sheets:
            continue
        out = CACHE / f"{src.stem}__{sh.name}.csv"
        with out.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow([f"#source_sha256={sha256(src)}", f"#sheet={sh.name}"])
            for i in range(sh.nrows):
                w.writerow(sh.row_values(i))


def text_extracts() -> None:
    subprocess.run(["pdftotext", "-layout", str(CACHE / "omb_a4_2023.pdf"), str(CACHE / "omb_a4_2023.txt")], check=True)
    subprocess.run(["pdftotext", "-layout", str(CACHE / "omb_m25_15.pdf"), str(CACHE / "omb_m25_15.txt")], check=True)
    import html
    import re
    t = (CACHE / "omb_a4_2003.html").read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    (CACHE / "omb_a4_2003.txt").write_text(t)


def main() -> None:
    refresh = "--refresh" in sys.argv
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    fetched = {}
    for name, url in SOURCES.items():
        existed = (CACHE / name).exists()
        fetch(name, url, refresh)
        fetched[name] = None if existed and not refresh else dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for name, sheets in XLS_TO_CSV.items():
        xls_to_csv(name, sheets)
    text_extracts()
    prev = {}
    reg = DERIVED / "sources.csv"
    if reg.exists():
        with reg.open() as f:
            prev = {r["file"]: r for r in csv.DictReader(f)}
    with reg.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["file", "url", "bytes", "sha256", "fetched_utc"])
        for name, url in SOURCES.items():
            p = CACHE / name
            mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat(timespec="seconds")
            when = fetched[name] or prev.get(name, {}).get("fetched_utc") or mtime
            w.writerow([name, url, p.stat().st_size, sha256(p), when])
    print(f"staged {len(SOURCES)} files in {CACHE}; registry {reg}")


if __name__ == "__main__":
    main()
