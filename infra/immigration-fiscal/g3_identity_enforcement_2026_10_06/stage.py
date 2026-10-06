"""Stage the household rows and aggregates this lane needs from the pooled lane's cached IPUMS-CPS extracts.

Sources (read-only, never re-downloaded here): g3_identity_pooled_2026_10_05/_cache/
- monthly_mis15.csv.gz: IPUMS-CPS extract 5, every basic monthly sample January 1994 - August 2026 (October 2025
  was not fielded), case-selected to households at months-in-sample (MISH) 1 and 5;
- asec_pooled.csv.gz: IPUMS-CPS extract 4, the ASEC samples 1994-2026.

From 2003 on (the current Hispanic-origin question), each file's households holding anyone whose mother or father
was born in Mexico, elsewhere in Latin America or in South, Southeast or East Asia (IPUMS BPL 20000-30999 or
50000-52999) are written whole to _cache/<source>_hh.parquet. Every G2 or G3 person this lane analyses has such a
person in the household (the G2 person, or the G3 person's linked parent), and analyze.classify links parents only
within a household, so the filter drops no analysis person.

Aggregates over all rows (not only kept households):
- monthly_state_cells.parquet: persons, households and summed WTFINL by year, month, MISH and state. The state-mean
  weight (summed WTFINL over persons in the cell) stands in for the base weight, which no public file carries.
- monthly_composition.parquet: persons and summed WTFINL by year, month, MISH and flags (Hispanic, Mexican, child,
  foreign-born, Mexico-born, US-born with a Mexico-born parent).
- asec_composition.parquet: persons and summed ASECWT by year, child, Hispanic class (not Hispanic, Mexican, other
  Hispanic) and generation (1 foreign-born, 2 US-born with a foreign-born parent, 3 US-born of two US-born parents).

Each source's outputs record the source sha256 and the sha256 of the SQL that made them; a rerun skips a source whose
recorded hashes match.

Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/stage.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib
import json
import resource
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
POOLED = FISCAL / "g3_identity_pooled_2026_10_05" / "_cache"
CACHE = HERE / "_cache"
FIRST_YEAR = 2003
DUCK_MEMORY = "768MB"
LINEAGE_BPL = ("(MBPL BETWEEN 20000 AND 30999 OR FBPL BETWEEN 20000 AND 30999 "
               "OR MBPL BETWEEN 50000 AND 52999 OR FBPL BETWEEN 50000 AND 52999)")
PERSON = ["YEAR", "MONTH", "SERIAL", "CPSID", "CPSIDP", "CPSIDV", "STATEFIP", "PERNUM", "RELATE", "AGE", "SEX", "RACE",
          "MOMLOC", "MOMLOC2", "MOMRULE", "POPLOC", "POPLOC2", "POPRULE", "BPL", "MBPL", "FBPL", "NATIVITY", "HISPAN",
          "EMPSTAT", "EDUC"]
SOURCES = {
    "monthly": (POOLED / "monthly_mis15.csv.gz", PERSON + ["MISH", "WTFINL"], "WTFINL"),
    "asec": (POOLED / "asec_pooled.csv.gz", PERSON + ["ASECWT"], "ASECWT"),
}
BIG = {"CPSID", "CPSIDP", "CPSIDV"}
HISP = "HISPAN > 0 AND HISPAN < 900"
MEXICAN = "HISPAN BETWEEN 100 AND 109"
AGGREGATES = {
    "monthly": {
        "monthly_state_cells.parquet":
            "SELECT YEAR, MONTH, MISH, STATEFIP, count(*) AS n, sum(WTFINL) AS w, count(DISTINCT SERIAL) AS households "
            "FROM {src} WHERE YEAR >= {first} GROUP BY ALL ORDER BY ALL",
        "monthly_composition.parquet":
            f"SELECT YEAR, MONTH, MISH, {HISP} AS hispanic, {MEXICAN} AS mexican, AGE < 18 AS child, "
            "BPL >= 15000 AS foreign_born, BPL = 20000 AS mexico_born, "
            "BPL < 15000 AND (MBPL = 20000 OR FBPL = 20000) AS us_born_mexican_parent, count(*) AS n, sum(WTFINL) AS w "
            "FROM {src} WHERE YEAR >= {first} GROUP BY ALL ORDER BY ALL",
    },
    "asec": {
        "asec_composition.parquet":
            f"SELECT YEAR, AGE < 18 AS child, CASE WHEN {MEXICAN} THEN 1 WHEN {HISP} THEN 2 ELSE 0 END AS hisp_class, "
            "CASE WHEN BPL >= 15000 THEN 1 WHEN MBPL >= 15000 OR FBPL >= 15000 THEN 2 ELSE 3 END AS generation, "
            "count(*) AS n, sum(ASECWT) AS w FROM {src} WHERE YEAR >= {first} GROUP BY ALL ORDER BY ALL",
    },
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute(f"SET memory_limit = '{DUCK_MEMORY}'")
    con.execute("SET threads = 2")
    con.execute("SET preserve_insertion_order = false")
    con.execute(f"SET temp_directory = '{CACHE / 'duckdb_tmp'}'")
    return con


def stage(name: str) -> dict:
    path, cols, weight = SOURCES[name]
    types = {c: "BIGINT" if c in BIG else "DOUBLE" if c == weight else "INTEGER" for c in cols}
    src = f"read_csv('{path}', header = true, types = {types!r})"
    hh_sql = (f"CREATE TEMP TABLE hh AS SELECT YEAR, MONTH, SERIAL, count(*) AS n, bool_or({LINEAGE_BPL}) AS keep "
              f"FROM {src} WHERE YEAR >= {FIRST_YEAR} GROUP BY YEAR, MONTH, SERIAL")
    out = CACHE / f"{name}_hh.parquet"
    rows_sql = (f"SELECT {', '.join('s.' + c for c in cols)} FROM {src} s "
                "JOIN (SELECT YEAR, MONTH, SERIAL FROM hh WHERE keep) k USING (YEAR, MONTH, SERIAL) "
                f"WHERE s.YEAR >= {FIRST_YEAR} ORDER BY s.YEAR, s.MONTH, s.SERIAL, s.PERNUM")
    aggs = {f: q.format(src=src, first=FIRST_YEAR) for f, q in AGGREGATES[name].items()}
    spec = hashlib.sha256(json.dumps([hh_sql, rows_sql, aggs], sort_keys=True).encode()).hexdigest()
    meta_path = CACHE / f"{name}_hh.json"
    digest = sha(path)
    outputs = [out] + [CACHE / f for f in aggs]
    if meta_path.exists() and all(p.exists() for p in outputs):
        meta = json.loads(meta_path.read_text())
        if meta.get("source_sha256") == digest and meta.get("spec_sha256") == spec:
            print(f"  ✓ {name}: staged files current (source sha {digest[:12]}, spec {spec[:12]})", flush=True)
            return meta
    con = connect()
    con.execute(hh_sql)
    rows, households, kept_rows, kept_households = con.execute(
        "SELECT sum(n), count(*), sum(n) FILTER (WHERE keep), count(*) FILTER (WHERE keep) FROM hh").fetchone()
    tmp = out.with_suffix(".parquet.tmp")
    con.execute(f"COPY ({rows_sql}) TO '{tmp}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    written = con.execute(f"SELECT count(*) FROM read_parquet('{tmp}')").fetchone()[0]
    if written != kept_rows:
        raise SystemExit(f"[FAILED] {name}: wrote {written} rows, expected {kept_rows}")
    tmp.replace(out)
    for f, q in aggs.items():
        con.execute(f"COPY ({q}) TO '{CACHE / f}' (FORMAT PARQUET)")
    total = con.execute(f"SELECT sum(n) FROM read_parquet('{CACHE / next(iter(aggs))}')").fetchone()[0]
    con.close()
    if total != rows:
        raise SystemExit(f"[FAILED] {name}: aggregates hold {total} persons, the file {rows}")
    meta = dict(source=str(path.relative_to(FISCAL.parents[1])), source_sha256=digest, spec_sha256=spec,
                first_year=FIRST_YEAR, household_filter=LINEAGE_BPL, rows=int(rows), households=int(households),
                kept_rows=int(kept_rows), kept_households=int(kept_households), aggregates=sorted(aggs))
    meta_path.write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
    print(f"  ✓ {out.name}: {kept_rows:,} rows in {kept_households:,} of {households:,} households", flush=True)
    return meta


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    (CACHE / "duckdb_tmp").mkdir(exist_ok=True)
    for name in SOURCES:
        stage(name)
    print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MiB")


if __name__ == "__main__":
    main()
