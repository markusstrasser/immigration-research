#!/usr/bin/env python3
"""Stage a downloadable data release from the unified immigration.duckdb.

Produces dist/immigration-data-<version>/:
  immigration.duckdb        — the single self-contained warehouse (query-ready)
  parquet/<schema>__<t>.parquet  — every real table as typed Parquet (bulk/programmatic)
  DATA_DICTIONARY.md        — auto-generated column-level dictionary
  queries/                  — the headline SQL query pack (each cites its memo)
  README.md                 — what it is, how to query, provenance, license, caveats
  SHA256SUMS                — integrity
…then tars it to dist/immigration-data-<version>.tar.gz.

Everything here is a DERIVED aggregate over public US-government sources; the
compilation is shareable. Raw application-gated microdata (PSID, IRS PUF, LEHD)
is never included. Actual external publish is a human-gated step — see README.

Run: uv run --with duckdb python package_data_release.py [VERSION]
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from datetime import date
from pathlib import Path

from paths import unified_duckdb_path

REPO_ROOT = Path(__file__).resolve().parents[3]
QUERY_PACK = REPO_ROOT / "queries" / "immigration"


def _ok(m):
    print(f"  ✓ {m}")


def _header(s):
    print(f"\n[{s}]")


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _readme(con, version: str, db_size_mb: float) -> str:
    schemas = con.execute("SELECT * FROM main._schemas").fetchall()
    cat = con.execute("SELECT count(*), sum(n_rows) FROM main._catalog").fetchone()
    n_obj, total_rows = cat[0], int(cat[1])
    notes = con.execute(
        "SELECT schema_name, table_name, note FROM main._catalog "
        "WHERE note LIKE '%CONFLICT%' ORDER BY table_name"
    ).fetchall()
    schema_rows = "\n".join(
        f"| `{s}` | {n} | {r:,} |" for (s, n, r) in schemas
    )
    conflict_lines = "\n".join(
        f"- `{s}.{t}` — {note}" for (s, t, note) in notes
    ) or "- none"
    return f"""# Immigration fiscal & crime data — v{version}

A single self-contained DuckDB warehouse plus Parquet mirrors: the cleaned,
joined data stack behind the immigration fiscal/crime research. **{n_obj} objects,
{total_rows:,} rows**, {db_size_mb:.0f} MB.

> **Instrument note.** This compilation backs LLM-assisted research on a
> politically charged topic. Treat it as inspectable evidence, not a neutral
> verdict. Each query-pack file cites the memo it supports; conclusions live in
> the research repo, not in the numbers alone.

## Contents

| File | What |
|------|------|
| `immigration.duckdb` | The whole stack, query-ready (DuckDB ≥ 1.0). |
| `parquet/<schema>__<table>.parquet` | Every real table as typed Parquet (pandas/polars/Spark). |
| `DATA_DICTIONARY.md` | Column-level dictionary, generated from the warehouse. |
| `queries/` | Headline SQL — each file names its backing memo. |
| `SHA256SUMS` | Integrity check (`shasum -c SHA256SUMS`). |

## Schemas (provenance-namespaced)

| Schema | Objects | Rows |
|--------|--------:|-----:|
{schema_rows}

`context` = ACS/county/PUMA/zip context · `lifetime` = lifetime fiscal evidence ·
`fiscal` = cross-domain union (country tensor + materialized `v_*` join views).

## Query

```bash
duckdb immigration.duckdb "SELECT * FROM _catalog ORDER BY n_rows DESC"   # inventory
duckdb immigration.duckdb "SELECT * FROM acs_origin_national_2023"        # unqualified
duckdb immigration.duckdb "SELECT * FROM context.safmr_zip_2025"          # schema-qualified
duckdb immigration.duckdb "COPY (SELECT * FROM v_three_layer_annual) TO 'x.csv' (HEADER)"  # to CSV
```

Every base table is exposed unqualified in `main` for the query pack. Where a
table name exists in two source warehouses, `main` points at the canonical copy:

{conflict_lines}

## Provenance & license

Derived aggregates over **public US-government sources** — Census ACS/CPS PUMS,
CDC, HUD (CHAS/SAFMR/PIT), IRS SOI migration, CMS Medicaid, USDA SNAP, OMB, BEA,
SAIPE, EOIR, OHSS, and BJA SCAAP (criminal-alien custody reimbursements) — plus
published NPV benchmarks (NAS/NRC, Storesletten, Orrenius). Inputs are
public-domain or public-use; this compilation is shareable.

The **crime-by-status tables** (`crime_tx_arrests_by_status`,
`crime_spi_inmates_by_citizenship`, `crime_spi_incarceration_rate`) are derived
**aggregates** computed from two registration-gated archives — Light/He/Robey's
Texas DPS replication (openICPSR 124923) and BJS's Survey of Prison Inmates 2016
(ICPSR 37692). The archives' gating restricts redistribution of the underlying
microdata, not aggregate statistics; only counts/rates ship here. The SPI rate's
denominator is an IPUMS-derived population aggregate (the microdata itself stays
local-only). To rebuild these tables from scratch you must register for and
download the two archives yourself — see the MANUAL_ACQUIRE notes referenced in
`research/immigration-dataset-register.md`.

No license-restricted or application-gated microdata is included — IPUMS PUMS
(not redistributable; held local-only in `immigration_microdata.duckdb`), PSID,
IRS SOI PUF, Synthetic SIPP, FSRDC LEHD. Only derived aggregates ship here.
Full catalog + quirks: `research/immigration-dataset-register.md`.

## Reproduce from scratch

```bash
git clone <repo> && cd immigration-research/infra/immigration-fiscal
./reproduce.sh init && ./reproduce.sh all standard && ./reproduce.sh build unified
```

Reading order for the reasoning: `research/immigration-friend-reproduce-guide.md`.

## Publishing this release (maintainer)

External publication is human-gated. To publish:
- **GitHub Release** (recommended — repo-attached, no DOI ceremony):
  `gh release create data-v{version} dist/immigration-data-v{version}.tar.gz -t "Immigration data v{version}"`
- **Zenodo** (citable DOI) or **Hugging Face datasets** (versioned, viewer) — see README in repo.
"""


def build(version: str) -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb not installed — run via: uv run --with duckdb python package_data_release.py")

    db = unified_duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — build it first: reproduce.sh build unified")

    dist_root = REPO_ROOT / "dist"
    rel = dist_root / f"immigration-data-v{version}"
    if rel.exists():
        shutil.rmtree(rel)
    (rel / "parquet").mkdir(parents=True)

    _header(f"Stage release immigration-data-v{version}")
    shutil.copy2(db, rel / "immigration.duckdb")
    _ok(f"copied warehouse ({db.stat().st_size / 1e6:.1f} MB)")

    con = duckdb.connect(str(db), read_only=True)
    # one parquet per REAL table (schema-qualified; skip the redundant main.* alias views)
    reals = con.execute(
        "SELECT schema_name, table_name FROM main._catalog ORDER BY schema_name, table_name"
    ).fetchall()
    for sch, name in reals:
        out = rel / "parquet" / f"{sch}__{name}.parquet"
        con.execute(f"COPY (SELECT * FROM \"{sch}\".\"{name}\") TO '{out}' (FORMAT parquet)")
    _ok(f"exported {len(reals)} tables to parquet/")

    # data dictionary
    import emit_data_dictionary
    emit_data_dictionary.build(rel / "DATA_DICTIONARY.md")

    # query pack
    if QUERY_PACK.exists():
        shutil.copytree(QUERY_PACK, rel / "queries")
        _ok(f"copied query pack ({len(list((rel / 'queries').glob('*.sql')))} SQL files)")

    # readme
    (rel / "README.md").write_text(_readme(con, version, db.stat().st_size / 1e6))
    _ok("wrote README.md")
    con.close()

    # checksums (over everything staged)
    _header("Checksums + tarball")
    files = sorted(p for p in rel.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    sums = "\n".join(f"{_sha256(p)}  {p.relative_to(rel)}" for p in files)
    (rel / "SHA256SUMS").write_text(sums + "\n")
    _ok(f"SHA256SUMS over {len(files)} files")

    tarball = dist_root / f"immigration-data-v{version}.tar.gz"
    if tarball.exists():
        tarball.unlink()
    import tarfile
    with tarfile.open(tarball, "w:gz") as tf:
        tf.add(rel, arcname=rel.name)
    size_mb = tarball.stat().st_size / 1e6

    _header("Done")
    _ok(f"staged dir: {rel}")
    _ok(f"tarball:    {tarball}  ({size_mb:.1f} MB)")
    print("\n  Publish (human-gated):")
    print(f"    gh release create data-v{version} {tarball} -t 'Immigration data v{version}'")


if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else date.today().isoformat()
    build(v)
