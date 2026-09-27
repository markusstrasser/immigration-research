"""Download the public Mexican microdata and PPP series this lane reads, into the ignored _cache/, and
record each file's URL, size and sha256 in derived/sources_manifest.csv.

Sources (all public, no registration):
- INEGI ENOE 2024, quarters 1-2 (CSV): a cross-check on earnings, hours and employment.
- INEGI ENIGH 2024 (nueva serie): persons, jobs and income records, for annual labor income.
- ESRU-EMOVI 2017 (CEEY), the public Google Drive file linked from ceey.org.mx: parents' schooling
  and the respondent's schooling (household income only, in minimum-wage brackets; no personal income).
- World Bank WDI API: PPP conversion factors for Mexico (GDP and private consumption), GDP, population,
  government health spending per head, education spending and homicide rates (Mexico-side comparators).

Run from the repository root:  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/world_ledger_2026_09_27/acquire.py
Existing files are kept; the manifest is rewritten from what is on disk.
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "mexico"
DERIVED = HERE / "derived"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
INEGI = "https://www.inegi.org.mx/contenidos/programas/"
# ENIGH first: it carries annual labor income and is small. ENOE (a cross-check on earnings and hours)
# is limited to the first two quarters of 2024; INEGI's server drops or refuses the larger later files.
FILES = {
    **{f"enigh2024_ns_{t}_csv.zip": f"{INEGI}enigh/nc/2024/microdatos/enigh2024_ns_{t}_csv.zip"
       for t in ("poblacion", "trabajos", "ingresos", "concentradohogar")},
    **{f"enoe_2024_trim{q}_csv.zip": f"{INEGI}enoe/15ymas/microdatos/enoe_2024_trim{q}_csv.zip" for q in (1, 2)},
}
EMOVI_ID = "1hko58nfnlexpw5kiB1K0kqeXlOPAaGyr"   # "BASES DE DATOS", ESRU-EMOVI 2017, ceey.org.mx/contenido/que-hacemos/emovi/
WDI = "https://api.worldbank.org/v2/country/MEX;USA/indicator/{ind}?format=json&date=2015:2024&per_page=100"
WDI_SERIES = ("PA.NUS.PPP", "PA.NUS.PRVT.PP", "PA.NUS.FCRF", "NY.GDP.MKTP.PP.CD", "NY.GDP.MKTP.CN", "SP.POP.TOTL",
              "SH.XPD.GHED.PP.CD", "SH.XPD.CHEX.PP.CD", "SE.XPD.TOTL.GD.ZS", "VC.IHR.PSRC.P5", "GC.TAX.TOTL.GD.ZS",
              "NE.CON.GOVT.ZS", "GC.REV.XGRT.GD.ZS", "GC.TAX.GSRV.CN", "NE.CON.PRVT.CN")


def get(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read(), r.headers.get("Content-Type", "")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch(name: str, url: str) -> None:
    """curl with retries and resume: INEGI's server drops long transfers (IncompleteRead on urllib)."""
    out = CACHE / name
    part = out.with_suffix(out.suffix + ".part")
    if out.exists() and out.stat().st_size > 0:
        return
    for _ in range(8):
        rc = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--retry", "5", "--retry-all-errors",
                             "-C", "-", "-o", str(part), url]).returncode
        if rc == 0:
            break
    else:
        raise SystemExit(f"[BLOCKED] {url}: curl failed repeatedly (last rc {rc})")
    with open(part, "rb") as fh:
        if name.endswith(".zip") and fh.read(2) != b"PK":
            raise SystemExit(f"[BLOCKED] {url} did not return a zip")
    if name.endswith(".zip") and subprocess.run(["unzip", "-tq", str(part)], capture_output=True).returncode:
        raise SystemExit(f"[BLOCKED] {url}: the zip fails its integrity test")
    part.rename(out)


def fetch_drive(file_id: str, name: str) -> None:
    """A public Google Drive file; large files answer with a confirmation form first."""
    out = CACHE / name
    if out.exists() and out.stat().st_size > 0:
        return
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
    data, ctype = get(url)
    if data[:2] != b"PK" and b"<form" in data[:20000]:
        html = data.decode("utf-8", "replace")
        fields = dict(re.findall(r'name="([^"]+)" value="([^"]*)"', html))
        action = re.search(r'action="([^"]+)"', html).group(1)
        query = "&".join(f"{k}={v}" for k, v in fields.items())
        data, ctype = get(f"{action}?{query}")
    if data[:2] != b"PK":
        raise SystemExit(f"[BLOCKED] Drive file {file_id} did not return a zip ({ctype}, {len(data)} bytes)")
    out.write_bytes(data)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    for name, url in FILES.items():
        fetch(name, url)
    fetch_drive(EMOVI_ID, "esru_emovi_2017_bases.zip")
    for ind in WDI_SERIES:
        out = CACHE / f"wdi_{ind}.json"
        if not out.exists():
            data, _ = get(WDI.format(ind=ind))
            # The API answers an unknown or retired code with HTTP 200 and a message list; refuse it.
            r = json.loads(data)
            if len(r) < 2 or not r[1]:
                raise SystemExit(f"[BLOCKED] WDI {ind}: no data rows ({str(r[0])[:200]})")
            out.write_bytes(data)
    urls = {**FILES, "esru_emovi_2017_bases.zip": f"https://drive.google.com/file/d/{EMOVI_ID}/view",
            **{f"wdi_{i}.json": WDI.format(ind=i) for i in WDI_SERIES}}
    with open(DERIVED / "sources_manifest.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["file", "url", "bytes", "sha256"])
        for name in sorted(urls):
            p = CACHE / name
            w.writerow([f"_cache/mexico/{name}", urls[name], p.stat().st_size, sha(p)])
    print(f"manifest: {len(urls)} files", file=sys.stderr)


if __name__ == "__main__":
    main()
