"""Small public inputs for the housing transfer lane, cached under _cache/ (ignored).

1. Published ACS 2024 one-year national totals (api.census.gov): the gate for the PUMS
   aggregates, with variable labels saved beside the values.
2. ACS 2021 one-year population and BLS QCEW March 2021 covered employment: the employment
   to population ratio that converts Wilson and Zhou's per-1%-of-employment worker-flow
   coefficients into per-1%-of-population terms.
3. Federal Reserve SCF 2022 summary extract: the Hispanic share of investment real estate,
   the only public owner-ethnicity source for rental property found.
4. Federal Reserve Z.1 (S.1M.b households, S.11.2.b noncorporate business): real estate at
   market value and residential structures at current cost, the land-share anchor of the
   long-run arm, and foreign direct investment in noncorporate real estate.
5. Census Rental Housing Finance Survey 2024 public-use file and codebook: rental units by
   ownership entity (individual investors, partnerships/LLCs, REITs, nonprofits, ...).

The Census key comes from the environment (config.local.env) and never appears in output.
Run from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/fetch.py
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
KEY = os.environ.get("CENSUS_API_KEY", "")
ACS24 = ["B25065_001E", "B25065_001M", "B25060_001E", "B25060_001M", "B25079_001E",
         "B25079_001M", "B25003_001E", "B25003_002E", "B25003_003E", "B01003_001E",
         "B03001_004E", "B03001_004M"]
FILES = {
    "qcew_2021q1_us.csv": "https://data.bls.gov/cew/data/api/2021/1/area/US000.csv",
    "scfp2022s.zip": "https://www.federalreserve.gov/econres/files/scfp2022s.zip",
    "z1_csv_files.zip": "https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip",
    "rhfspuf2024.csv": "https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/rhfspuf2024.csv",
    "rhfs2024_codebook.pdf": "https://www2.census.gov/programs-surveys/rhfs/data/public-use-files/2024/Codebook-Version-1.pdf",
}


def redact(text):
    return text.replace(KEY, "REDACTED") if KEY else text


def get(url, timeout=120):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = redact(str(e))[:160]
            print(f"  ! attempt {attempt + 1}: {last}")
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"[BLOCKED] {redact(url.split('?')[0])}: {last}")


def census(year, cols, name):
    path = CACHE / name
    if not path.exists():
        base = f"https://api.census.gov/data/{year}/acs/acs1"
        rows = json.loads(get(f"{base}?get={','.join(cols)}&for=us:1&key={KEY}"))
        labels = {}
        for c in cols:
            meta = json.loads(get(f"{base}/variables/{c}.json"))
            labels[c] = {"label": meta.get("label"), "concept": meta.get("concept")}
        path.write_text(json.dumps({"url": f"{base}?get=...&for=us:1", "rows": rows,
                                    "labels": labels}, indent=2))
    return json.loads(path.read_text())


def main():
    if not KEY:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
    CACHE.mkdir(exist_ok=True)
    census(2024, ACS24, "acs2024_us_totals.json")
    census(2021, ["B01003_001E"], "acs2021_us_population.json")
    manifest = {}
    for name, url in FILES.items():
        path = CACHE / name
        if not path.exists():
            path.write_bytes(get(url, timeout=300))
        manifest[name] = {"url": url, "bytes": path.stat().st_size,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
