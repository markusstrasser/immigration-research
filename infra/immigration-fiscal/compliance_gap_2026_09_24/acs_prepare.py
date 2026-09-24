#!/usr/bin/env python3
"""Type the two IPUMS ACS worker extracts into Parquet and record their row counts and keys.

Inputs: _cache/ipums/{workers,workers_pre}.csv.gz (ipums_extract.py; sha256 equal to IPUMS's
published values). Outputs: _cache/ipums/{name}.parquet and derived/fetch_manifest_ipums.json
(rows, years, samples per year, expected columns present, unique person key).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/acs_prepare.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "ipums"
MANIFEST = HERE / "derived" / "fetch_manifest_ipums.json"
COLUMNS = {  # name -> DuckDB type
    "YEAR": "SMALLINT", "SERIAL": "INTEGER", "PERNUM": "SMALLINT", "PERWT": "DOUBLE",
    "STATEFIP": "TINYINT", "PWSTATE2": "TINYINT", "GQ": "TINYINT", "SEX": "TINYINT", "AGE": "SMALLINT",
    "HISPAN": "TINYINT", "BPL": "SMALLINT", "BPLD": "INTEGER", "CITIZEN": "TINYINT", "YRIMMIG": "SMALLINT",
    "HINSTRI": "TINYINT", "HINSCAID": "TINYINT", "HINSCARE": "TINYINT", "HINSVA": "TINYINT",
    "EDUC": "TINYINT", "EDUCD": "SMALLINT", "EMPSTAT": "TINYINT", "EMPSTATD": "TINYINT",
    "CLASSWKR": "TINYINT", "CLASSWKRD": "TINYINT", "IND": "SMALLINT", "IND1990": "SMALLINT",
    "INDNAICS": "VARCHAR", "WKSWORK2": "TINYINT", "UHRSWORK": "TINYINT", "INCWAGE": "INTEGER",
    "INCBUS00": "INTEGER", "INCSS": "INTEGER", "INCSUPP": "INTEGER", "VETSTAT": "TINYINT",
    "BPL_SP": "SMALLINT", "CITIZEN_SP": "TINYINT",
}
YEARS = {"workers": list(range(2012, 2025)), "workers_pre": list(range(2005, 2012))}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    con = duckdb.connect()
    con.execute("SET memory_limit='2GB'; SET threads=4; SET preserve_insertion_order=false")
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for name, years in YEARS.items():
        src = CACHE / f"{name}.csv.gz"
        out = CACHE / f"{name}.parquet"
        digest = sha256(src)
        rec = manifest.get(name, {})
        if not (out.exists() and rec.get("source_sha256") == digest):
            header = con.execute(f"SELECT * FROM read_csv('{src}', header=true, all_varchar=true) LIMIT 0").description
            have = {d[0] for d in header}
            missing = [c for c in COLUMNS if c not in have]
            if missing:
                raise SystemExit(f"[FAILED] {src.name}: expected columns missing {missing}")
            select = ", ".join(
                f"trim(\"{c}\") AS \"{c}\"" if t == "VARCHAR" else f"CAST(\"{c}\" AS {t}) AS \"{c}\""
                for c, t in COLUMNS.items())
            con.execute(f"COPY (SELECT {select} FROM read_csv('{src}', header=true, all_varchar=true)) "
                        f"TO '{out}' (FORMAT parquet, COMPRESSION zstd)")
        rows, n_years, dup, not_emp = con.execute(f"""SELECT count(*), count(DISTINCT "YEAR"),
            count(*) - count(DISTINCT ("YEAR", "SERIAL", "PERNUM")), count(*) FILTER (WHERE "EMPSTAT" <> 1)
            FROM '{out}'""").fetchone()
        by_year = dict(con.execute(f'SELECT "YEAR", count(*) FROM \'{out}\' GROUP BY 1 ORDER BY 1').fetchall())
        rec = {"source": src.name, "source_sha256": digest, "parquet": out.name, "rows": rows,
               "rows_by_year": {str(k): v for k, v in by_year.items()},
               "years_expected": years, "years_ok": sorted(by_year) == years,
               "duplicate_person_keys": dup, "rows_not_employed": not_emp,
               "expected_keys_present": True}
        if not rec["years_ok"] or dup or not_emp:
            raise SystemExit(f"[FAILED] {name}: years {sorted(by_year)}, duplicates {dup}, non-employed {not_emp}")
        manifest[name] = rec
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        print(f"✓ {name}: {rows:,} employed person records, {n_years} years, key unique")


if __name__ == "__main__":
    main()
