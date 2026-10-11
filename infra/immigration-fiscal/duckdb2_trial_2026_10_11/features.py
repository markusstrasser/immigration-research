"""Persist the real IPUMS catalog as JSON/VARIANT and check every record.

This is a fidelity probe on fifteen existing records, not a storage/speed benchmark.
Run with the pinned preview, using uv --isolated --no-project --with duckdb==...
"""
import argparse
import hashlib
import json
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def main(out):
    source = REPO / "sources/immigration-fiscal/data/external/ipums/usa_extract/catalog.json"
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    records = json.loads(source.read_text())["extracts"]
    out.mkdir(parents=True, exist_ok=False)
    db = out / "catalog.duckdb"
    con = duckdb.connect(str(db))
    con.execute("CREATE TABLE original (id INTEGER, payload JSON)")
    con.executemany("INSERT INTO original VALUES (?, ?::JSON)",
                    [(i, json.dumps(r)) for i, r in enumerate(records)])
    con.execute("CREATE TABLE variant AS SELECT id, payload::VARIANT AS payload FROM original")
    engine = con.execute("SELECT version()").fetchone()[0]
    if not engine.startswith("v2.0.0"):
        raise RuntimeError(f"not the v2 preview: {engine}")
    threshold = con.execute("SELECT value FROM duckdb_settings() WHERE name = "
                            "'variant_minimum_shredding_size'").fetchone()[0]
    con.execute("CHECKPOINT")
    con.close()
    con = duckdb.connect(str(db), read_only=True)
    roundtrip = [json.loads(r[0]) for r in con.execute(
        "SELECT payload::JSON FROM variant ORDER BY id").fetchall()]
    if roundtrip != records:
        raise RuntimeError("persisted VARIANT changed raw records")
    # A JSON string cast to VARCHAR remains JSON text, including its quotes.
    # VARIANT's scalar cast returns the string itself. Compare equivalent reads.
    scalar_casts = {
        table: con.execute(f"SELECT id, payload.status::VARCHAR FROM {table} "
                           "ORDER BY id").fetchall()
        for table in ("original", "variant")
    }
    queries = [
        (
            "SELECT id, payload.number::INTEGER, payload.rows::BIGINT, "
            "json_extract_string(payload, '$.status') FROM original ORDER BY id",
            "SELECT id, payload.number::INTEGER, payload.rows::BIGINT, "
            "payload.status::VARCHAR FROM variant ORDER BY id",
        ),
        (
            "SELECT id, payload.samples::JSON, payload.quality_flags::JSON, "
            "payload.used_in::JSON FROM original ORDER BY id",
            "SELECT id, payload.samples::JSON, payload.quality_flags::JSON, "
            "payload.used_in::JSON FROM variant ORDER BY id",
        ),
    ]
    checks = []
    for json_sql, variant_sql in queries:
        a = con.execute(json_sql).fetchall()
        b = con.execute(variant_sql).fetchall()
        # JSON text key ordering is not meaningful; raw roundtrip above verifies shape.
        normalize = lambda rows: [[json.loads(v) if isinstance(v, str) and
                                   v.startswith(("[", "{")) else v for v in row] for row in rows]
        if normalize(a) != normalize(b):
            raise RuntimeError("JSON/VARIANT projection mismatch")
        checks.append(dict(json_sql=json_sql, variant_sql=variant_sql, rows=len(a), parity=True))
    after = hashlib.sha256(source.read_bytes()).hexdigest()
    if before != after:
        raise RuntimeError("catalog source changed")
    result = dict(engine=engine, source=str(source.relative_to(REPO)), source_sha256=before,
                  records=len(records), roundtrip_parity=True, projection_checks=checks,
                  variant_minimum_shredding_size=threshold, scalar_casts=scalar_casts,
                  note="Small real fixture: validates fidelity, not shredding performance.")
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    con.close()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=HERE / "_cache/features")
    main(p.parse_args().out)
