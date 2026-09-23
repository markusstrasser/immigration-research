"""Download and fingerprint the congestion lane's external inputs.

Every file lands in _cache/ (ignored) and its sha256 is recorded in _cache/manifest.json.
Sources that block scripted downloads (USDOT, the HAL copy of Couture-Duranton-Turner) were
retrieved through Firecrawl's PDF parser and saved as text; the manifest records the source URL
and the hash of the saved text.

  python3 fetch.py            # files and the Geocorr PUMA->urban-area crosswalk
  python3 fetch.py geocorr    # only the crosswalk
  python3 fetch.py census     # only the Census API tables (key from acquire/config.local.env)

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/fetch.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache"
MANIFEST = CACHE / "manifest.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

FILES = {
    # Texas A&M Transportation Institute, 2025 Urban Mobility Report (2024 data), 494 urban areas.
    "complete-data-2025-umr-by-tti.xlsx":
        "https://static.tti.tamu.edu/tti.tamu.edu/documents/umr/data/complete-data-2025-umr-by-tti.xlsx",
    "mobility-report-2025.pdf": "https://static.tti.tamu.edu/tti.tamu.edu/documents/mobility-report-2025.pdf",
    "mobility-report-2025-appx-a.pdf":
        "https://static.tti.tamu.edu/tti.tamu.edu/documents/mobility-report-2025-appx-a.pdf",
    "mobility-report-2025-appx-b.pdf":
        "https://static.tti.tamu.edu/tti.tamu.edu/documents/mobility-report-2025-appx-b.pdf",
    "mobility-report-2025-appx-c.pdf":
        "https://static.tti.tamu.edu/tti.tamu.edu/documents/mobility-report-2025-appx-c.pdf",
    # National Household Travel Survey public-use files.
    "nhts2022_csv.zip": "https://nhts.ornl.gov/media/2022/download/csv.zip",
    "nhts2022_codebook.xlsx": "https://nhts.ornl.gov/media/2022/doc/codebook.xlsx",
    "nhts2017_csv.zip": "https://nhts.ornl.gov/media/2016/download/csv.zip",
    # Couture, Duranton and Turner, "Speed" (NBER w18234, 2012) and Duranton and Turner,
    # "The Fundamental Law of Road Congestion" (NBER w15376, 2009).
    "w18234.pdf": "https://www.nber.org/system/files/working_papers/w18234/w18234.pdf",
    "w15376.pdf": "https://www.nber.org/system/files/working_papers/w15376/w15376.pdf",
    # Census Table H-8, median household income by state (CPS ASEC), the USDOT income base.
    "census_h08.xlsx":
        "https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h08.xlsx",
    # NCHRP Report 716 (2012), Travel Demand Forecasting: Parameters and Techniques (BPR tables).
    "nchrp_rpt_716.pdf": "https://transportation.ky.gov/Planning/Documents/Travel%20Demand%20Forecasting.pdf",
}
# Retrieved with Firecrawl (PDF parser) because the hosts refuse scripted clients.
FIRECRAWL = {
    "usdot_vtts_2016_rev2.firecrawl.md":
        "https://www.transportation.gov/sites/dot.gov/files/docs/2016%20Revised%20Value%20of%20Travel%20Time%20Guidance.pdf",
    "cdt_speed_2016_hal.firecrawl.md": "https://sciencespo.hal.science/hal-03459352/document",
    "bls_ocwage_may2024.firecrawl.md": "https://www.bls.gov/news.release/archives/ocwage_04022025.pdf",
}
# BLS public API v1 (no key): ECEC compensation and wage cost per hour, civilian workers, all and
# transportation and material moving occupations, 2015-2024.
BLS_ECEC = {"file": "bls_ecec_2015_2024.json",
            "series": ["CMU1010000000000D", "CMU1020000000000D", "CMU1010000520000D", "CMU1020000520000D"]}

BROKER = "https://mcdc.missouri.edu/cgi-bin/broker"
STATES = ['Al01', 'Ak02', 'Az04', 'Ar05', 'Ca06', 'Co08', 'Ct09', 'De10', 'Dc11', 'Fl12', 'Ga13',
          'Hi15', 'Id16', 'Il17', 'In18', 'Ia19', 'Ks20', 'Ky21', 'La22', 'Me23', 'Md24', 'Ma25',
          'Mi26', 'Mn27', 'Ms28', 'Mo29', 'Mt30', 'Ne31', 'Nv32', 'Nh33', 'Nj34', 'Nm35', 'Ny36',
          'Nc37', 'Nd38', 'Oh39', 'Ok40', 'Or41', 'Pa42', 'Ri44', 'Sc45', 'Sd46', 'Tn47', 'Tx48',
          'Ut49', 'Vt50', 'Va51', 'Wa53', 'Wv54', 'Wi55', 'Wy56']
BLANKS = ("title", "oropt", "counties", "metros", "uaucs", "places", "latitude", "longitude",
          "locname", "distance", "nrings", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9",
          "r10", "lathi", "latlo", "longhi", "longlo")

# ACS 2024 one-year tables for the commuting gate and the value-of-time income base.
CENSUS = {
    "acs2024_b08301_us.json": ("acs/acs1", "B08301", "us:1"),
    "acs2024_b08301_cbsa.json": ("acs/acs1", "B08301", "metropolitan statistical area/micropolitan statistical area:*"),
    "acs2024_b08303_us.json": ("acs/acs1", "B08303", "us:1"),
    "acs2024_b08133_us.json": ("acs/acs1", "B08133", "us:1"),
    "acs2024_b19013_us.json": ("acs/acs1", "B19013", "us:1"),
    "acs2024_b01001_us.json": ("acs/acs1", "B01001", "us:1"),
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def record(manifest, name, url, method):
    path = CACHE / name
    manifest[name] = {"url": url, "method": method, "bytes": path.stat().st_size,
                      "sha256": sha256(path),
                      "recorded": manifest.get(name, {}).get("recorded") or time.strftime("%Y-%m-%d")}


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as out:
        while block := r.read(1 << 20):
            out.write(block)


def fetch_files(manifest):
    for name, url in FILES.items():
        dest = CACHE / name
        if not dest.exists():
            print("download", name, flush=True)
            download(url, dest)
        record(manifest, name, url, "http")
    for name, url in FIRECRAWL.items():
        if not (CACHE / name).exists():
            print(f"[GAP] {name} must be re-retrieved with Firecrawl from {url}")
            continue
        record(manifest, name, url, "firecrawl pdf parser, markdown saved")


def geocorr_state(state, tries=3):
    q = {"_PROGRAM": "apps.geocorr2022.sas", "_SERVICE": "MCDC_long", "_debug": "0",
         "state": state, "g1_": "puma22", "g2_": "ua", "wtvar": "pop20", "nozerob": "1",
         "csvout": "1", "fileout": "1", "filefmt": "csv", "lstfmt": "txt", "namoptf": "b",
         "namoptr": "b", "kiloms": "0"}
    q.update({k: "" for k in BLANKS})
    url = BROKER + "?" + urllib.parse.urlencode(q)
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                html = r.read().decode("utf-8", "replace")
            m = re.search(r'"\s*(/temp/geocorr\w*_[^"\s]+\.csv)\s*"', html)
            if not m:
                raise RuntimeError(f"no csv link for {state}")
            with urllib.request.urlopen("https://mcdc.missouri.edu" + m.group(1), timeout=300) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - retried, then raised
            if attempt == tries - 1:
                raise
            sys.stderr.write(f"retry {state}: {exc}\n")
            time.sleep(5)


def fetch_bls(manifest):
    dest = CACHE / BLS_ECEC["file"]
    if not dest.exists():
        body = json.dumps({"seriesid": BLS_ECEC["series"], "startyear": "2015", "endyear": "2024"}).encode()
        req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body,
                                     headers={"Content-Type": "application/json", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            dest.write_bytes(r.read())
    record(manifest, dest.name, "https://api.bls.gov/publicAPI/v1/timeseries/data/ "
           + ",".join(BLS_ECEC["series"]) + " 2015-2024", "bls api v1")


def fetch_geocorr(manifest):
    out = CACHE / "xwalk_puma22_ua20.csv"
    if not out.exists():
        rows = []
        for st in STATES:
            reader = csv.DictReader(io.StringIO(geocorr_state(st)))
            next(reader)  # second header line of labels
            rows.extend(reader)
            print("geocorr", st, len(rows), flush=True)
            time.sleep(1)
        with out.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    record(manifest, out.name, BROKER + " (apps.geocorr2022.sas, puma22 -> ua, pop20 weights)", "http")


def fetch_census(manifest):
    env = ROOT / "infra/immigration-fiscal/acquire/config.local.env"
    key = os.environ.get("CENSUS_API_KEY")
    for line in env.read_text().splitlines():
        line = line.strip().removeprefix("export ").strip()
        if not key and line.startswith("CENSUS_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY missing from acquire/config.local.env")
    for name, (dataset, table, geo) in CENSUS.items():
        dest = CACHE / name
        if dest.exists():
            record(manifest, name, f"api.census.gov/data/2024/{dataset} group({table}) for={geo}", "census api")
            continue
        params = {"get": f"NAME,group({table})", "for": geo, "key": key}
        url = f"https://api.census.gov/data/2024/{dataset}?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                data = r.read()
        except Exception as exc:  # noqa: BLE001 - never echo the URL, it carries the key
            raise SystemExit(f"[BLOCKED] census api {table} {geo}: {type(exc).__name__}") from None
        dest.write_bytes(data)
        record(manifest, name, f"api.census.gov/data/2024/{dataset} group({table}) for={geo}", "census api")
        print("census", name, len(data), flush=True)


def main():
    CACHE.mkdir(exist_ok=True)
    manifest = load_manifest()
    parts = sys.argv[1:] or ["files", "geocorr", "census"]
    if "files" in parts:
        fetch_files(manifest)
        fetch_bls(manifest)
    if "geocorr" in parts:
        fetch_geocorr(manifest)
    if "census" in parts:
        fetch_census(manifest)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(json.dumps({k: v["sha256"][:12] for k, v in manifest.items()}, indent=1))


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
