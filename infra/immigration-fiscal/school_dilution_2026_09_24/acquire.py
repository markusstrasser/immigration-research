"""Fetch the Census F-33 district finance files FY2000-FY2024 and the published summary tables.

Individual-unit files (all items): elsecYY.txt, one per fiscal year, from the Census Annual Survey
of School System Finances directory. Summary tables for the gate years. The FY2015 technical
documentation for item definitions. Everything lands in ignored _cache/f33/. Beside it: SAIPE
school-district child poverty, the NCES Digest enrollment-by-race table, monthly CPI-U, and the
CCD LEA staff files 2018-19 and 2023-24 (teachers). CCD fall-2000 teachers and English learners
come from pull_ccd.py (Urban Institute API); other CCD falls reuse the school-flight lane's pull.

Content is validated, never status or size alone (census.gov has returned truncated bodies under
HTTP 200): the header must carry the items this lane reads, every row must parse to the header's
field count (the files carry one trailing empty field on data rows), and the row count must sit in
a plausible band. Writes derived/sources_f33.json with the URL, bytes, rows and SHA-256 per file.

The FY2022 all-items text file on census.gov is itself a 1,729-row subset (its size equals the
server's Content-Length, so the download is faithful). For that year the same release's .xlsx
(14,105 rows) is converted to elsec22_xlsx.csv and validated the same way.

    uv run --no-project --with pandas --with openpyxl \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/acquire.py
"""
import csv
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "f33"
OUT = HERE / "derived"
BASE = "https://www2.census.gov/programs-surveys/school-finances/tables/{y}/secondary-education-finance/{f}"
YEARS = range(2000, 2025)
NEEDED = ["V33", "TCURELSC", "TCURINST", "TCURSSVC", "E17", "E07", "E08", "E09", "V40", "V45", "V90", "V85",
          "TCUROTH", "E11", "TCAPOUT", "I86", "TOTALREV", "TFEDREV", "TSTREV", "TLOCREV", "NCESID"]
EXTRA = {
    2005: ["elsec05_sttables.xls"], 2010: ["elsec10_sttables.xls"], 2015: ["elsec15_sttables.xls", "school15doc.pdf"],
    2019: ["elsec19_sumtables.xls"], 2023: ["elsec23_sumtables.xlsx"], 2024: ["elsec24_sumtables.xlsx"],
}
FALLBACK_XLSX = {2022: "elsec22.xlsx"}   # the .txt of that year is a partial upload
CPI_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"   # monthly CPI-U, for fiscal-year means
DIGEST_URL = "https://nces.ed.gov/programs/digest/d23/tables/dt23_203.50.asp"
SAIPE_URL = "https://www2.census.gov/programs-surveys/saipe/datasets/{y}/{y}-school-districts/{f}"
SAIPE_YEARS = [2005, 2010, 2019, 2023]
NCES_URL = "https://nces.ed.gov/ccd/Data/zip/{f}.zip"   # CCD LEA staff files (teachers), for class_size.py
NCES_STAFF = ["ccd_lea_059_1819_l_1a_091019", "ccd_lea_059_2324_l_1a_073124"]


def unit_file_name(y):
    """The validated all-items CSV the builder reads for fiscal year y."""
    return f"elsec{y % 100:02d}_xlsx.csv" if y in FALLBACK_XLSX else f"elsec{y % 100:02d}.txt"


def xlsx_to_csv(xlsx, out):
    import pandas as pd
    d = pd.read_excel(xlsx, sheet_name=xlsx.stem, dtype=str)
    tmp = out.with_suffix(".part")
    d.to_csv(tmp, index=False, lineterminator="\n")
    tmp.replace(out)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def curl(url, out):
    tmp = out.with_suffix(out.suffix + ".part")
    r = subprocess.run(["curl", "-sS", "--fail", "-L", "--retry", "3", "--max-time", "900", "-o", str(tmp), url],
                       capture_output=True, text=True)
    if r.returncode:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] curl rc={r.returncode} {url}: {r.stderr.strip()}")
    tmp.replace(out)


def check_unit_file(path):
    """Header carries the needed items; every data row has the header's field count (+1 trailing)."""
    with open(path, newline="", encoding="latin-1") as f:
        rows = csv.reader(f)
        header = next(rows)
        missing = [c for c in NEEDED if c not in header]
        if missing:
            raise SystemExit(f"[BLOCKED] {path.name} header lacks {missing}")
        n, bad = 0, 0
        for row in rows:
            n += 1
            if len(row) not in (len(header), len(header) + 1):
                bad += 1
    if bad:
        raise SystemExit(f"[BLOCKED] {path.name}: {bad} rows with a field count off the header's {len(header)}")
    if not 13_000 <= n <= 20_000:
        raise SystemExit(f"[BLOCKED] {path.name}: {n} rows, outside the 13,000-20,000 band")
    return n, len(header)


def remote_length(url):
    """Content-Length from a HEAD request; older files end without a final newline, so size is the check."""
    r = subprocess.run(["curl", "-sSI", "--fail", "-L", "--max-time", "120", url], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"[BLOCKED] HEAD rc={r.returncode} {url}: {r.stderr.strip()}")
    lengths = [int(line.split(":", 1)[1]) for line in r.stdout.splitlines() if line.lower().startswith("content-length")]
    return lengths[-1] if lengths else None


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    log = []
    for y in YEARS:
        if y in FALLBACK_XLSX:
            src = FALLBACK_XLSX[y]
            url, xlsx = BASE.format(y=y, f=src), CACHE / src
            if not xlsx.exists():
                curl(url, xlsx)
            expected = remote_length(url)
            if expected is not None and expected != xlsx.stat().st_size:
                raise SystemExit(f"[BLOCKED] {src}: {xlsx.stat().st_size} bytes held, server says {expected}")
            path = CACHE / unit_file_name(y)
            if not path.exists():
                xlsx_to_csv(xlsx, path)
            rows, fields = check_unit_file(path)
            log.append({"file": path.name, "converted_from": src, "fiscal_year": y, "url": url,
                        "bytes_source": xlsx.stat().st_size, "sha256_source": sha256(xlsx), "rows": rows,
                        "header_fields": fields, "sha256": sha256(path),
                        "note": "elsec22.txt on census.gov holds 1,729 of 14,105 rows; the .xlsx is used"})
            print(f"ok {path.name} rows={rows} (from {src})", flush=True)
        else:
            name = unit_file_name(y)
            path, url = CACHE / name, BASE.format(y=y, f=name)
            if not path.exists():
                curl(url, path)
            rows, fields = check_unit_file(path)
            expected = remote_length(url)
            if expected is not None and expected != path.stat().st_size:
                raise SystemExit(f"[BLOCKED] {name}: {path.stat().st_size} bytes held, server says {expected}")
            log.append({"file": name, "fiscal_year": y, "url": url, "bytes": path.stat().st_size, "rows": rows,
                        "header_fields": fields, "sha256": sha256(path)})
            print(f"ok {name} rows={rows}", flush=True)
        for extra in EXTRA.get(y, []):
            p = CACHE / extra
            if not p.exists():
                curl(BASE.format(y=y, f=extra), p)
            head = p.read_bytes()[:8]
            ok = head.startswith(b"%PDF") or head.startswith(b"\xd0\xcf\x11\xe0") or head.startswith(b"PK")
            if not ok:
                raise SystemExit(f"[BLOCKED] {extra}: not a PDF/XLS/XLSX body ({head!r})")
            log.append({"file": extra, "fiscal_year": y, "url": BASE.format(y=y, f=extra), "bytes": p.stat().st_size,
                        "sha256": sha256(p)})
    for y in SAIPE_YEARS:                         # SAIPE school-district child poverty, fixed width
        name = f"ussd{y % 100:02d}.txt"
        url = SAIPE_URL.format(y=y, f=name)
        p = CACHE.parent / "saipe" / name
        p.parent.mkdir(exist_ok=True)
        if not p.exists():
            curl(url, p)
        lines = p.read_text(encoding="latin-1").splitlines()
        if not 12_000 <= len(lines) <= 15_000 or not all(line[:2].isdigit() for line in lines):
            raise SystemExit(f"[BLOCKED] {name}: {len(lines)} lines or a line without a state code")
        expected = remote_length(url)
        if expected is not None and expected != p.stat().st_size:
            raise SystemExit(f"[BLOCKED] {name}: {p.stat().st_size} bytes held, server says {expected}")
        log.append({"file": f"saipe/{name}", "url": url, "bytes": p.stat().st_size, "rows": len(lines),
                    "sha256": sha256(p)})
    digest = CACHE.parent / "dt23_203.50.html"    # national public enrollment by race, fall 1995-2022
    if not digest.exists():
        curl(DIGEST_URL, digest)
    text = digest.read_text(encoding="utf-8", errors="replace")
    if "Hispanic" not in text or "47,204" not in text:
        raise SystemExit(f"[BLOCKED] {digest.name}: no Hispanic column or no fall-2000 total (47,204 thousand)")
    log.append({"file": digest.name, "url": DIGEST_URL, "bytes": digest.stat().st_size, "sha256": sha256(digest)})
    cpi = CACHE.parent / "cpiaucsl_monthly.csv"
    if not cpi.exists():
        curl(CPI_URL, cpi)
    lines = cpi.read_text().splitlines()
    if lines[0] != "observation_date,CPIAUCSL" or not any(line.startswith("2024-12-01,") for line in lines):
        raise SystemExit(f"[BLOCKED] {cpi.name}: unexpected header or no December 2024 row")
    log.append({"file": cpi.name, "url": CPI_URL, "bytes": cpi.stat().st_size, "rows": len(lines) - 1,
                "sha256": sha256(cpi)})
    for name in NCES_STAFF:                       # nces.ed.gov serves ~50 KB/s; 8-10 MB each
        url, p = NCES_URL.format(f=name), CACHE.parent / "nces" / f"{name}.zip"
        p.parent.mkdir(exist_ok=True)
        if not p.exists():
            curl(url, p)
        expected = remote_length(url)
        if expected is not None and expected != p.stat().st_size:
            raise SystemExit(f"[BLOCKED] {p.name}: {p.stat().st_size} bytes held, server says {expected}")
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None or f"{name}.csv" not in z.namelist():
                raise SystemExit(f"[BLOCKED] {p.name}: corrupt member or no {name}.csv")
        log.append({"file": f"nces/{p.name}", "url": url, "bytes": p.stat().st_size, "sha256": sha256(p)})
    (OUT / "sources_f33.json").write_text(json.dumps(log, indent=1) + "\n")
    print(f"done: {len(log)} files", flush=True)


if __name__ == "__main__":
    sys.exit(main())
