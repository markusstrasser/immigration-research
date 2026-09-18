#!/usr/bin/env python3
"""Fetch and cache every source this lane uses; write a sha256 manifest.

Idempotent: a file already in _cache/ with a non-zero size is not re-fetched.
Run:
  cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" python3 fetch.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
CACHE.mkdir(exist_ok=True)
DERIVED.mkdir(exist_ok=True)

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)

# name -> url.  BJS moved its document root twice; the paths below are the ones that
# actually return bytes as of 2026-09-18 (verified by size + file type, see manifest).
SOURCES: dict[str, str] = {
    # BJS Criminal Victimization annual data tables (zip of CSVs, estimates + SEs)
    "cv18.zip": "https://bjs.ojp.gov/redirect-legacy/content/pub/sheets/cv18.zip",
    "cv19.zip": "https://bjs.ojp.gov/redirect-legacy/content/pub/sheets/cv19.zip",
    "cv21.zip": "https://bjs.ojp.gov/content/pub/sheets/cv21.zip",
    "cv22.zip": "https://bjs.ojp.gov/document/cv22.zip",
    "cv23.zip": "https://bjs.ojp.gov/document/cv23.zip",
    "cv24.zip": "https://bjs.ojp.gov/document/cv24.zip",
    # The reports themselves (for footnote text quoted in the memo)
    "cv19.pdf": "https://bjs.ojp.gov/redirect-legacy/content/pub/pdf/cv19.pdf",
    "cv21.pdf": "https://bjs.ojp.gov/content/pub/pdf/cv21.pdf",
    "cv24.pdf": "https://bjs.ojp.gov/document/cv24.pdf",
    # BJS special report NCJ 250747 — the published 2012-15 victim x offender matrix
    "rhovo1215.pdf": "https://bjs.ojp.gov/content/pub/pdf/rhovo1215.pdf",
    # BJS NCJ 255578 — violent victimisation rate by victim race 2005-2019 (cross-check)
    "vvre0519.pdf": "https://bjs.ojp.gov/content/pub/pdf/vvre0519.pdf",
    # BJS N-DASH static data: victim race/Hispanic origin x crime type, 1993-2024
    "nd_person_race_all.csv": (
        "https://ncvs.bjs.ojp.gov/data/custom-graphics/person/racehispanicorigin_all.csv"
    ),
    "nd_person_all_all.csv": (
        "https://ncvs.bjs.ojp.gov/data/custom-graphics/person/all_all.csv"
    ),
    # N-DASH application bundle — the evidence that no offender characteristic exists
    "ndash_app.js": "https://ncvs.bjs.ojp.gov/js/app.c7ab787c.js",
    # N-DASH static data: victim injury by crime type, for the simple-assault injury share
    "nd_person_injury_all.csv": (
        "https://ncvs.bjs.ojp.gov/data/custom-graphics/person/injury_all.csv"
    ),
    # Miller, Cohen & Wiersema (1996), NIJ NCJ 155282, full research report
    "victcost.pdf": "https://www.ojp.gov/pdffiles/victcost.pdf",
}

# Miller et al. (2021), JBCA 12(1):24-54, doi:10.1017/bca.2020.36.  Paywalled at
# Cambridge (the /article/abs/ page offers "Get access"/"Purchase"; OpenAlex reports
# oa_status "closed"; SSRN sits behind a Cloudflare challenge).  The PDF in _cache/ was
# retrieved through the repo's research MCP (fetch_paper by DOI) and is checked by
# sha256 rather than re-downloaded here.
MANUAL = {
    "miller2021_jbca.pdf":
        "cccb174d99a8102b3732cfa86f5d44a1c4ce2880e4c6e076acc66a0f49586103",
}

# Route 1 (ICPSR microdata) probes: recorded, not downloadable.  Each entry is
# (label, url); fetch.py records the HTTP status and any redirect target.
ICPSR_PROBES = [
    ("icpsr_study_page", "https://www.icpsr.umich.edu/web/NACJD/studies/38963"),
    (
        "icpsr_download_zipcart",
        "https://www.icpsr.umich.edu/cgi-bin/bob/zipcart2"
        "?path=NACJD&study=38963&bundle=all&ds=1&dups=yes",
    ),
    (
        "icpsr_download_delimited",
        "https://www.icpsr.umich.edu/web/NACJD/studies/38963/datasets/0001/download/delimited?path=NACJD",
    ),
]

BLS_SERIES = "CUUR0000SA0"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curl(url: str, out: Path, follow: bool = True) -> tuple[int, str]:
    cmd = [
        "curl", "-sS", "--http1.1", "-A", UA, "-m", "600", "-o", str(out),
        "-w", "%{http_code} %{redirect_url}",
    ]
    if follow:
        cmd.append("-L")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    parts = r.stdout.strip().split(" ", 1)
    return int(parts[0]), (parts[1] if len(parts) > 1 else "")


def check_manual() -> list[dict]:
    """Files that cannot be fetched by URL; verify the cached copy by digest."""
    rows = []
    for name, want in MANUAL.items():
        dest = CACHE / name
        if not dest.exists():
            raise SystemExit(
                f"{name} is not in _cache/ and cannot be downloaded (paywalled). "
                "Retrieve it with the research MCP: fetch_paper(doi='10.1017/bca.2020.36')."
            )
        got = sha256(dest)
        if got != want:
            raise SystemExit(f"{name} sha256 {got} != expected {want}")
        print(f"[manual] {name} verified ({dest.stat().st_size:,} bytes)")
        rows.append({"name": name, "url": "doi:10.1017/bca.2020.36 (paywalled; via research MCP)",
                     "bytes": dest.stat().st_size, "sha256": got, "status": "manual"})
    return rows


def fetch_all() -> list[dict]:
    rows = []
    for name, url in SOURCES.items():
        dest = CACHE / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"[cache] {name} ({dest.stat().st_size:,} bytes)")
            status = "cached"
        else:
            print(f"[fetch] {name} <- {url}")
            code, _ = curl(url, dest)
            if code != 200 or dest.stat().st_size == 0:
                raise SystemExit(f"fetch failed for {name}: HTTP {code}")
            status = "fetched"
        rows.append(
            {
                "name": name,
                "url": url,
                "bytes": dest.stat().st_size,
                "sha256": sha256(dest),
                "status": status,
            }
        )
    return rows


def probe_icpsr() -> list[dict]:
    rows = []
    for label, url in ICPSR_PROBES:
        tmp = CACHE / f"probe_{label}.out"
        code, redirect = curl(url, tmp, follow=False)
        print(f"[probe] {label}: HTTP {code} redirect={redirect or '-'}")
        rows.append(
            {"probe": label, "url": url, "http_status": code, "redirect_url": redirect}
        )
    return rows


def fetch_cpi() -> dict[int, float]:
    """CPI-U annual averages, BLS public API v2, cached as JSON."""
    import urllib.request

    out: dict[int, float] = {}
    for lo, hi in ((1992, 2001), (2002, 2007), (2008, 2015), (2016, 2025)):
        key = CACHE / f"cpi_{lo}_{hi}.json"
        if key.exists():
            payload = json.loads(key.read_text())
        else:
            body = json.dumps(
                {
                    "seriesid": [BLS_SERIES],
                    "startyear": str(lo),
                    "endyear": str(hi),
                    "annualaverage": True,
                }
            ).encode()
            req = urllib.request.Request(
                "https://api.bls.gov/publicAPI/v2/timeseries/data/",
                data=body,
                headers={"Content-Type": "application/json", "User-Agent": UA},
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                payload = json.loads(r.read().decode())
            key.write_text(json.dumps(payload))
        for s in payload["Results"]["series"]:
            for row in s["data"]:
                if row["periodName"] == "Annual":
                    out[int(row["year"])] = float(row["value"])
    return out


def unzip_cv() -> None:
    for name in SOURCES:
        if not name.endswith(".zip"):
            continue
        stem = name[:-4]
        dest = CACHE / stem
        dest.mkdir(exist_ok=True)
        with zipfile.ZipFile(CACHE / name) as z:
            z.extractall(dest)
        print(f"[unzip] {name} -> {stem}/ ({len(list(dest.glob('*.csv')))} csv)")


def main() -> None:
    rows = fetch_all() + check_manual()
    unzip_cv()
    probes = probe_icpsr()
    cpi = fetch_cpi()
    print(f"[cpi] 2008={cpi[2008]} 2024={cpi[2024]} ratio={cpi[2024] / cpi[2008]:.5f}")

    with (DERIVED / "source_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "url", "bytes", "sha256", "status"])
        w.writeheader()
        for r in sorted(rows, key=lambda x: x["name"]):
            w.writerow({**r, "status": ""})  # status varies by run; not part of the artefact

    with (DERIVED / "icpsr_route_probe.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["probe", "url", "http_status", "redirect_url"])
        w.writeheader()
        for r in probes:
            w.writerow(r)

    with (DERIVED / "cpi_u_annual.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "cpi_u"])
        for y in sorted(cpi):
            w.writerow([y, cpi[y]])

    print("[done] fetch.py")


if __name__ == "__main__":
    sys.exit(main())
