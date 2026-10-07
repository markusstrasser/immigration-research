"""Stage the pooled lane's two IPUMS-CPS extracts as column-pruned parquet files in this lane's _cache.

Sources (read-only, staged by g3_identity_pooled_2026_10_05/extract.py and extract_monthly.py):
  _cache/asec_pooled.csv.gz   IPUMS-CPS extract 4, ASEC 1994-2026, parent pointers, INCWAGE, STATEFIP
  _cache/monthly_mis15.csv.gz IPUMS-CPS extract 5, basic monthly Jan 1994 - Aug 2026, MISH 1 and 5
DuckDB streams each gzipped CSV once (512 MB memory limit, 2 threads) and writes the columns vintage.py reads,
in file order, so vintage.py can read one survey year at a time and stay well under 2 GB. The parquet files are
ignored cache; derived/stage_audit.json records the source hashes and row counts.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/stage.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]
SRC = FISCAL / "g3_identity_pooled_2026_10_05/_cache"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

COMMON = ["YEAR", "MONTH", "SERIAL", "CPSID", "STATEFIP", "PERNUM", "CPSIDP", "AGE", "SEX", "RACE",
          "MOMLOC", "MOMLOC2", "MOMRULE", "POPLOC", "POPLOC2", "POPRULE", "BPL", "MBPL", "FBPL", "NATIVITY",
          "HISPAN", "EMPSTAT", "EDUC"]
FILES = {
    "asec": (SRC / "asec_pooled.csv.gz", COMMON + ["ASECWT", "INCWAGE"]),
    "monthly": (SRC / "monthly_mis15.csv.gz", COMMON + ["MISH", "WTFINL"]),
}
BIG = {"CPSID", "CPSIDP"}
FLOAT = {"ASECWT", "WTFINL"}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    (CACHE / "duckdb_tmp").mkdir(exist_ok=True)
    audit = {}
    for name, (path, cols) in FILES.items():
        types = {c: "BIGINT" if c in BIG else "DOUBLE" if c in FLOAT else "INTEGER" for c in cols}
        con = duckdb.connect()
        con.execute("SET memory_limit = '512MB'")
        con.execute("SET threads = 2")
        con.execute("SET preserve_insertion_order = true")
        con.execute(f"SET temp_directory = '{CACHE / 'duckdb_tmp'}'")
        out = CACHE / f"{name}.parquet"
        # all_varchar off, explicit types: a column with a non-integer value fails loudly here.
        src = f"read_csv('{path}', header = true, types = {types!r})"
        con.execute(f"COPY (SELECT {', '.join(cols)} FROM {src}) TO '{out}' (FORMAT parquet, ROW_GROUP_SIZE 200000)")
        n, years, nulls = con.execute(
            f"SELECT count(*), count(DISTINCT YEAR), sum(CASE WHEN {' OR '.join(c + ' IS NULL' for c in cols)} "
            f"THEN 1 ELSE 0 END) FROM read_parquet('{out}')").fetchone()
        con.close()
        if nulls:
            raise ValueError(f"{name}: {nulls} rows with a missing staged value")
        audit[name] = dict(source=str(path.relative_to(REPO)), sha256=sha(path), rows=int(n), years=int(years),
                           columns=cols)
        print(f"  ✓ {name}: {n:,} rows, {years} years -> {out.relative_to(REPO)}", flush=True)
    (DERIVED / "stage_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
