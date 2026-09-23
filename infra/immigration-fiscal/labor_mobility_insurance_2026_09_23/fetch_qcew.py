"""Download BLS QCEW annual single files and reduce them to county totals and national sectors.

Payroll employment by place of work, as Cadena & Kovak's County Business Patterns measure, for
the shock years. Raw zips stay in _cache/qcew/ (ignored); the reduction writes
derived/qcew_county_total.csv (county x year, all ownerships, total covered, agglvl 70),
derived/qcew_national_sector.csv (NAICS sector x year, agglvl 14, summed over ownerships) and
derived/qcew_manifest.json (URL, bytes, SHA-256 of each zip).

Usage, from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/fetch_qcew.py
"""
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.csv as pacsv

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "qcew"
DERIVED = HERE / "derived"
YEARS = [2006, 2010, 2012, 2016, 2019, 2020, 2021, 2022, 2023]
UA = "Mozilla/5.0 (academic research)"  # BLS refuses curl's default agent; no personal contact sent
URL = "https://data.bls.gov/cew/data/files/{y}/csv/{y}_annual_singlefile.zip"


def fetch(year: int) -> Path:
    out = CACHE / f"{year}_annual_singlefile.zip"
    if out.exists() and zipfile.is_zipfile(out) and zipfile.ZipFile(out).testzip() is None:
        return out
    CACHE.mkdir(parents=True, exist_ok=True)
    rc = subprocess.run(["curl", "-s", "-L", "--retry", "5", "-A", UA, "-o", str(out), URL.format(y=year)]).returncode
    if rc != 0 or not zipfile.is_zipfile(out) or zipfile.ZipFile(out).testzip() is not None:
        raise SystemExit(f"[FAILED] QCEW {year}: download rc={rc} or corrupt zip")
    return out


def reduce(year: int, path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    zf = zipfile.ZipFile(path)
    member = [n for n in zf.namelist() if n.endswith(".csv")][0]
    cols = ["area_fips", "own_code", "industry_code", "agglvl_code", "year", "disclosure_code",
            "annual_avg_emplvl", "total_annual_wages"]
    types = {c: pa.string() for c in cols}
    types.update({"annual_avg_emplvl": pa.float64(), "total_annual_wages": pa.float64()})
    with zf.open(member) as fh:
        t = pacsv.read_csv(fh, convert_options=pacsv.ConvertOptions(include_columns=cols, column_types=types))
    d = t.to_pandas()
    county = d[(d["agglvl_code"] == "70") & (d["own_code"] == "0") & (d["industry_code"] == "10")]
    county = county[["area_fips", "annual_avg_emplvl", "total_annual_wages", "disclosure_code"]].assign(year=year)
    nat = d[(d["agglvl_code"] == "14") & (d["area_fips"] == "US000")]
    nat = (nat.groupby("industry_code", as_index=False)[["annual_avg_emplvl"]].sum().assign(year=year))
    return county, nat


def main() -> None:
    manifest, counties, nats = {}, [], []
    for y in YEARS:
        p = fetch(y)
        manifest[str(y)] = {"url": URL.format(y=y), "bytes": p.stat().st_size,
                            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        c, n = reduce(y, p)
        if len(c) < 3000 or n["annual_avg_emplvl"].sum() < 1e8:
            raise SystemExit(f"[FAILED] QCEW {y}: {len(c)} counties, national sectors sum {n['annual_avg_emplvl'].sum():.0f}")
        counties.append(c)
        nats.append(n)
        print(f"  ✓ {y}: {len(c)} counties, {n['annual_avg_emplvl'].sum() / 1e6:.1f}m in national sectors")
    DERIVED.mkdir(exist_ok=True)
    pd.concat(counties).to_csv(DERIVED / "qcew_county_total.csv", index=False)
    pd.concat(nats).to_csv(DERIVED / "qcew_national_sector.csv", index=False)
    (DERIVED / "qcew_manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
