#!/usr/bin/env python3
"""Fetch QCEW annual averages, 2005-2024, and keep the national and state rows.

Source: BLS QCEW open data, one annual "singlefile" zip per year (all areas, all ownerships, all
NAICS levels), https://data.bls.gov/cew/data/files/<year>/csv/<year>_annual_singlefile.zip. The
open-data API slices start in 2014, so the singlefiles are used for every year alike. Each zip
(about 80 MB) is streamed once: rows for US000 and the 50 states plus DC (XX000) are written to
_cache/qcew/qcew_state_<year>.csv.gz and the zip is deleted. The manifest row per year
(derived/fetch_manifest_qcew.json) records the zip's bytes and sha256, its member, header, total
and kept row counts, and whether every expected key is present.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/compliance_gap_2026_09_24/fetch_qcew.py [years...]
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import subprocess
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "qcew"
MANIFEST = HERE / "derived" / "fetch_manifest_qcew.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
HEADERS = ["-H", 'sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
           "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-platform: "macOS"']
YEARS = list(range(2005, 2025))
STATES = {f"{f:02d}000" for f in [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22,
                                   23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                                   40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]}
AREAS = STATES | {"US000"}
KEEP = ["area_fips", "own_code", "industry_code", "agglvl_code", "size_code", "year", "qtr",
        "disclosure_code", "annual_avg_estabs", "annual_avg_emplvl", "total_annual_wages",
        "annual_avg_wkly_wage", "avg_annual_pay"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def fetch_year(year: int, manifest: dict) -> dict:
    out = CACHE / f"qcew_state_{year}.csv.gz"
    rec = manifest.get(str(year))
    if out.exists() and rec and rec.get("reduced_sha256") == sha256(out):
        return rec
    url = f"https://data.bls.gov/cew/data/files/{year}/csv/{year}_annual_singlefile.zip"
    zpath = CACHE / f"{year}_annual_singlefile.zip"
    tmp = zpath.with_suffix(".zip.part")
    r = subprocess.run(["curl", "-sS", "--fail", "-L", "-A", UA, *HEADERS, "--retry", "5",
                        "--retry-delay", "10", "-o", str(tmp), url])
    if r.returncode != 0:
        raise SystemExit(f"[FAILED] {url}: curl exit {r.returncode}")
    tmp.replace(zpath)
    with zipfile.ZipFile(zpath) as z:  # content check: a zip holding one CSV with the QCEW header
        names = [i.filename for i in z.infolist() if not i.is_dir()]
        if len(names) != 1 or not names[0].endswith(".csv"):
            raise SystemExit(f"[FAILED] {zpath.name}: unexpected members {names}")
        reader = csv.DictReader(io.TextIOWrapper(z.open(names[0]), encoding="utf-8", newline=""))
        header = reader.fieldnames
        missing = [k for k in KEEP if k not in header]
        if missing:
            raise SystemExit(f"[FAILED] {zpath.name}: expected columns missing {missing}")
        n = kept = 0
        areas_seen, years_seen = set(), set()
        part = out.with_suffix(".gz.part")
        with gzip.open(part, "wt", newline="") as g:
            w = csv.writer(g, lineterminator="\n")
            w.writerow(KEEP)
            for row in reader:
                n += 1
                if row["area_fips"] in AREAS:
                    w.writerow([row[k].strip() for k in KEEP])
                    kept += 1
                    areas_seen.add(row["area_fips"])
                    years_seen.add(row["year"])
        part.replace(out)
    rec = {"url": url, "zip_bytes": zpath.stat().st_size, "zip_sha256": sha256(zpath),
           "member": names[0], "header": header, "rows": n, "rows_kept": kept,
           "areas_kept": len(areas_seen), "years_in_file": sorted(years_seen),
           "expected_keys_present": True, "reduced_file": out.name, "reduced_sha256": sha256(out),
           "fetched": time.strftime("%Y-%m-%d")}
    if rec["areas_kept"] != len(AREAS) or rec["years_in_file"] != [str(year)]:
        raise SystemExit(f"[FAILED] {year}: areas {rec['areas_kept']} of {len(AREAS)}, years {rec['years_in_file']}")
    zpath.unlink()
    return rec


def main() -> None:
    years = [int(a) for a in sys.argv[1:]] or YEARS
    CACHE.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    for y in years:
        t = time.time()
        manifest = load_manifest()
        rec = fetch_year(y, manifest)
        manifest[str(y)] = rec
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        print(f"✓ {y}: {rec['rows']:,} rows, {rec['rows_kept']:,} kept ({time.time() - t:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
