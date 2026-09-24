"""Download this lane's public sources into _cache/sources/ and check their content.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
        infra/immigration-fiscal/consumption_key_2026_09_24/fetch.py [name ...]

Python urllib fails TLS on this machine, so every download goes through curl. bls.gov answers 403
without browser headers. A file counts as fetched only when its content passes the check listed with
it (an xlsx opens and carries its expected title; a zip lists its expected member; a PDF's text, from
pdftotext, carries its expected phrase; a JSON body carries its expected string).

The corridor files (Banxico, BEA, CEMLA, USCIS) in _cache/sources/corridor/ were read by a research
subagent; their URLs, tables and quotes are listed in RESULT.md. The FDIC supplement pulls are
sender_pull.py's; the NIS-2003 archive is the repository's staged copy (nis_transfers.py).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import warnings
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "sources"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
BROWSER = ["-A", UA, "-H", 'sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
           "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-platform: "macOS"',
           "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
           "-H", "Accept-Language: en-US,en;q=0.9", "-H", "Sec-Fetch-Dest: document",
           "-H", "Sec-Fetch-Mode: navigate", "-H", "Sec-Fetch-Site: none", "-H", "Sec-Fetch-User: ?1",
           "-H", "Upgrade-Insecure-Requests: 1"]
TABLES_REFERER = ["-H", "Referer: https://www.bls.gov/cex/tables.htm"]
CE = "https://www.bls.gov/cex/tables/calendar-year/mean-item-share-average-standard-error/"
XT = "https://www.bls.gov/cex/tables/cross-tab/mean/"
AGES = ["under-25", "25-34", "35-44", "45-54", "55-64", "65-or-older"]
SIZES = ["1-person", "2-persons", "3-persons", "4-persons", "5-or-more-persons"]
# The keyless BLS API returns at most ten years per query.
CPI_YEARS = [("2003", "2012"), ("2015", "2024")]
CPI_QUERY = {a: json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": a, "endyear": b, "annualaverage": True})
             for a, b in CPI_YEARS}

# name -> (url, kind, expected content, extra curl arguments)
SOURCES = {
    "cu-income-deciles-before-taxes-2024.xlsx": (CE + "cu-income-deciles-before-taxes-2024.xlsx", "xlsx", "Deciles of income before taxes", TABLES_REFERER),
    "cu-income-quintiles-before-taxes-2024.xlsx": (CE + "cu-income-quintiles-before-taxes-2024.xlsx", "xlsx", "Quintiles of income before taxes", TABLES_REFERER),
    "reference-person-latino-2024.xlsx": (CE + "reference-person-latino-2024.xlsx", "xlsx", "Hispanic or Latino origin of reference person", TABLES_REFERER),
    **{f"reference-person-age-by-income-{a}-2023-2024.xlsx": (XT + f"reference-person-age-by-income-{a}-2023-2024.xlsx", "xlsx", "by income before taxes", TABLES_REFERER) for a in AGES},
    **{f"cu-size-by-income-{s}-2023-2024.xlsx": (XT + f"cu-size-by-income-{s}-2023-2024.xlsx", "xlsx", "by income before taxes", TABLES_REFERER) for s in SIZES},
    # The microdata server answers 403 to a same-origin Referer; it serves the bare browser headers.
    "intrvw24.zip": ("https://www.bls.gov/cex/pumd/data/csv/intrvw24.zip", "zip", "intrvw24/fmli242.csv", []),
    "ce-pumd-interview-diary-dictionary.xlsx": ("https://www.bls.gov/cex/pumd/ce-pumd-interview-diary-dictionary.xlsx", "xlsx", "variables with their flags and codes", []),
    "itep/ITEP-Who-Pays-7th-edition.pdf": ("https://sfo2.digitaloceanspaces.com/itep/ITEP-Who-Pays-7th-edition.pdf", "pdf", "U. S. Average", []),
    "cemla_2018_migracion_mexicana.pdf": ("https://www.cemla.org/PDF/remesaseinclusion/2018-04-migracion-mexicana.pdf", "pdf",
                                          "la remesa mensual promedio es de 380", []),
    "corridor/bea_2025-06_trans125.pdf": ("https://www.bea.gov/sites/default/files/2025-06/trans125.pdf", "pdf", "Personal transfers", []),
    **{f"bls_cpi_u_{a}_{b}.json": ("https://api.bls.gov/publicAPI/v2/timeseries/data/", "json", "REQUEST_SUCCEEDED",
                                   ["-X", "POST", "-H", "Content-Type: application/json", "--data", CPI_QUERY[a]])
       for a, b in CPI_YEARS},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xlsx_text(path: Path, rows: int = 12) -> str:
    import openpyxl
    warnings.filterwarnings("ignore")
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    out = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i >= rows:
            break
        out.extend(str(c) for c in row if c is not None)
    return " ".join(out)


def pdf_text(path: Path) -> str:
    txt = path.with_suffix(".txt")
    if not txt.exists() or txt.stat().st_mtime < path.stat().st_mtime:
        subprocess.run(["pdftotext", "-layout", str(path), str(txt)], check=True)
    return txt.read_text(errors="replace")


def check(path: Path, kind: str, expected: str) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        if kind == "xlsx":
            return expected.lower() in xlsx_text(path).lower()
        if kind == "zip":
            with zipfile.ZipFile(path) as z:
                return any(expected in n for n in z.namelist())
        if kind == "pdf":
            return expected in pdf_text(path)
        if kind == "json":
            return expected in path.read_text()
        return expected.encode() in path.read_bytes()
    except Exception:
        return False


def fetch(name: str, url: str, kind: str, expected: str, extra: list[str]) -> dict:
    dest = CACHE / name
    if not check(dest, kind, expected):
        dest.parent.mkdir(parents=True, exist_ok=True)
        part = dest.with_suffix(dest.suffix + ".part")
        headers = BROWSER if "bls.gov/cex" in url else []
        rc = subprocess.run(["curl", "-sS", "--fail", "-L", "--compressed", "--max-time", "900", *headers, *extra,
                             "-o", str(part), url]).returncode
        if rc != 0:
            part.unlink(missing_ok=True)
            return dict(name=name, url=url, ok=False, error=f"curl exit {rc}")
        part.replace(dest)
    ok = check(dest, kind, expected)
    return dict(name=name, url=url, ok=ok, sha256=sha(dest) if dest.exists() else None,
                check=f"{kind} contains {expected!r}")


def cpi_annual() -> dict:
    """CPI-U (CUUR0000SA0) annual averages from the fetched BLS API body, {year: index}."""
    out = {}
    for a, b in CPI_YEARS:
        body = json.loads((CACHE / f"bls_cpi_u_{a}_{b}.json").read_text())
        out.update({int(r["year"]): float(r["value"]) for r in body["Results"]["series"][0]["data"] if r["period"] == "M13"})
    return out


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or list(SOURCES)
    records = [fetch(n, *SOURCES[n]) for n in wanted]
    manifest = CACHE / "manifest.json"
    old = json.loads(manifest.read_text()) if manifest.exists() else {}
    old.update({r["name"]: r for r in records})
    manifest.write_text(json.dumps(old, indent=1) + "\n")
    bad = [r for r in records if not r["ok"]]
    for r in records:
        print(("ok   " if r["ok"] else "FAIL ") + r["name"] + ("" if r["ok"] else " — " + r.get("error", "content check failed")))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
