"""Reproducible, read-only DuckDB preview screening on this repo's real inputs.

Run from repo root: uv run --no-sync python3 <lane>/trial.py
Outputs, full result rows and captured SQL live in the ignored _cache directory.
The project interpreter builds cases; isolated uv environments execute each arm.
"""
from __future__ import annotations

import argparse
import datetime as dt
from decimal import Decimal
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASELINE = "1.5.5"
CANDIDATE = "2.0.0.dev2610011535"
REL_TOL, ABS_TOL = 1e-12, 1e-8


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def compatible(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        return (math.isnan(a) and math.isnan(b)) or math.isclose(
            a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    if isinstance(a, list):
        return len(a) == len(b) and all(compatible(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        if set(a) != set(b):
            return False
        if set(a) == {"decimal"}:
            return Decimal(a["decimal"]) == Decimal(b["decimal"])
        return all(compatible(a[k], b[k]) for k in a)
    return a == b


def controls():
    assert compatible([[1, None, 2.0]], [[1, None, 2.0 + 1e-13]])
    assert not compatible([[1, None]], [[2, None]])
    assert not compatible([[1, None]], [[1, 0]])
    assert not compatible({"columns": ["a"]}, {"columns": ["b"]})
    assert not compatible([[1.0]], [[1.1]])
    assert not compatible([[1.0]], [[1]])
    assert not compatible([[{"decimal": "1.01"}]], [[{"decimal": "1.02"}]])


def json_value(x):
    if isinstance(x, Decimal):
        return {"decimal": str(x)}
    if isinstance(x, (dt.date, dt.time, dt.datetime)):
        return {"temporal": x.isoformat()}
    if isinstance(x, bytes):
        return {"bytes": x.hex()}
    if isinstance(x, (list, tuple)):
        return [json_value(v) for v in x]
    if isinstance(x, dict):
        return {k: json_value(v) for k, v in x.items()}
    return x


def quote(path):
    return "'" + str(path).replace("'", "''") + "'"


def run_worker(cmd, output, timeout=240):
    """Keep diagnostics and stop the whole isolated worker group on timeout."""
    with subprocess.Popen(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = process.communicate()
            output.with_suffix(".stdout").write_text(stdout)
            output.with_suffix(".stderr").write_text(stderr)
            raise RuntimeError(f"worker interrupted or timed out; inspect {output.with_suffix('.stderr')}") from exc
        output.with_suffix(".stdout").write_text(stdout)
        output.with_suffix(".stderr").write_text(stderr)
        if process.returncode:
            raise RuntimeError(f"worker failed ({process.returncode}); inspect {output.with_suffix('.stderr')}")


def build_cases():
    ipums = REPO / "sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb"
    parq = REPO / "sources/immigration-fiscal/derived/ipums_usa"
    files = {HERE / "PREREGISTRATION.md", Path(__file__).resolve(), ipums}
    cases = []

    def add(name, db, sql, source, inputs):
        files.update([db, source, *inputs] if db else [source, *inputs])
        cases.append(dict(name=name, db=str(db) if db else None, sql=sql,
                          source=str(source.relative_to(REPO)), attach=[]))

    store = REPO / "infra/immigration-fiscal/ipums_usa_store_2026_09_23"
    pqfiles = sorted(parq.glob("*.parquet"))
    add("ipums_weighted_scan", ipums, """SELECT YEAR, BPL, EDUC, count(*) AS n,
        sum(PERWT) AS population, sum(PERWT * INCTOT) AS income
        FROM usa_00002 WHERE AGE BETWEEN 25 AND 64 GROUP BY ALL ORDER BY ALL""",
        store / "README.md", pqfiles)
    add("ipums_person_join", ipums, """SELECT a.YEAR, count(*) AS matched,
        sum(CASE WHEN a.AGE IS DISTINCT FROM b.AGE THEN 1 ELSE 0 END) AS age_diff,
        sum(a.PERWT) AS weight, sum(b.QEDUC) AS education_flags
        FROM usa_00004 a JOIN usa_00006 b USING (YEAR, SAMPLE, SERIAL, PERNUM)
        GROUP BY a.YEAR ORDER BY a.YEAR""", store / "organize.py", [])
    add("ipums_filtered_quality", ipums, """SELECT YEAR, count(*) AS n,
        sum(PERWT) AS weight, sum(PERWT * (QEDUC > 0)::INT) AS allocated_weight,
        count(*) FILTER (WHERE QEDUC IS NULL) AS missing_qeduc
        FROM usa_00013 WHERE YEAR BETWEEN 2020 AND 2024 GROUP BY YEAR ORDER BY YEAR""",
        store / "README.md", [])

    creative = REPO / "infra/immigration-fiscal/cultural_output_2026_09_19"
    source = creative / "scripts/02_arm_a_creative_labour.py"
    # Existing builder, rather than a copied/rephrased SQL implementation.
    # Its only import-time side effect is mkdir on the existing derived directory.
    if not (creative / "derived").is_dir():
        raise RuntimeError("creative lane's existing derived directory is missing")
    spec = importlib.util.spec_from_file_location("creative_query_source", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class Capture:
        def execute(self, sql):
            self.sql = sql
            return self

        def df(self):
            return self.sql

    add("acs_81_weight_cells", None, module.build_cells(Capture()), source, [module.PARQ])
    for source in sorted((REPO / "queries/immigration").glob("*.sql")):
        kind = source.name.split("_", 1)[0]
        db = REPO / "warehouse" / {
            "context": "immigration_context.duckdb",
            "union": "immigration_fiscal_union.duckdb",
            "life": "immigration_lifetime_evidence.duckdb",
        }[kind]
        add(source.stem, db, source.read_text(), source, [])
        if kind == "union":
            cases[-1]["attach"] = [
                ["ctx", str(REPO / "warehouse/immigration_context.duckdb")],
                ["life", str(REPO / "warehouse/immigration_lifetime_evidence.duckdb")],
            ]
    metadata = []
    for path in sorted(files):
        if not path.is_file():
            raise FileNotFoundError(path)
        metadata.append(dict(path=str(path.relative_to(REPO)), bytes=path.stat().st_size,
                             sha256=digest(path)))
    return dict(cases=cases, inputs=metadata, python=sys.version, platform=platform.platform(),
                settings=dict(threads=6, memory_limit="2GB", timezone="UTC"),
                baseline=BASELINE, candidate=CANDIDATE)


def worker(manifest_path, out, package):
    import duckdb
    if duckdb.__version__ != package:
        raise RuntimeError(f"wrong package: {duckdb.__version__} != {package}")
    engine = duckdb.sql("SELECT version()").fetchone()[0]
    if package == CANDIDATE and not engine.startswith("v2.0.0"):
        raise RuntimeError(f"candidate is not v2: {engine}")
    manifest = json.loads(manifest_path.read_text())
    result = dict(package=package, engine=engine, python=sys.version, cases=[])
    for case in manifest["cases"]:
        entry = dict(name=case["name"], executions=[])
        con = None
        try:
            con = duckdb.connect(case["db"] or ":memory:", read_only=bool(case["db"]))
            con.execute("SET threads = 6")
            con.execute("SET memory_limit = '2GB'")
            con.execute("SET TimeZone = 'UTC'")
            scratch = out.parent / f"scratch-{package}"
            scratch.mkdir(exist_ok=True)
            con.execute(f"SET temp_directory = {quote(scratch)}")
            for alias, db in case["attach"]:
                con.execute(f"ATTACH {quote(db)} AS {alias} (READ_ONLY)")
            statements = con.extract_statements(case["sql"])
            for phase in ("first", "warm"):
                batches = []
                start = time.perf_counter()
                for stmt in statements:
                    cursor = con.execute(stmt)
                    schema = [[d[0], str(d[1])] for d in cursor.description]
                    rows = cursor.fetchall()
                    batches.append((schema, rows))
                elapsed = time.perf_counter() - start
                output = []
                for schema, rows in batches:
                    converted = [json_value(row) for row in rows]
                    converted.sort(key=lambda row: json.dumps(row, sort_keys=True))
                    output.append(dict(schema=schema, rows=converted))
                entry["executions"].append(dict(phase=phase, seconds=elapsed, output=output))
        except Exception as exc:
            entry["error"] = f"{type(exc).__name__}: {exc}"
        finally:
            if con is not None:
                con.close()
        result["cases"].append(entry)
        save(out, result)
    result["peak_rss_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (
        1e6 if sys.platform == "darwin" else 1e3)
    save(out, result)
    if any("error" in c for c in result["cases"]):
        raise SystemExit(2)


def run(rounds, out):
    controls()
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest_path = out / "manifest.json"
    manifest = build_cases()
    save(manifest_path, manifest)
    save(out / "preregistered_run.json", dict(rounds=rounds, manifest_sha256=digest(manifest_path)))
    trials = []
    for round_no in range(rounds):
        order = [BASELINE, CANDIDATE] if round_no % 2 == 0 else [CANDIDATE, BASELINE]
        for package in order:
            path = out / f"round-{round_no}-{package}.json"
            cmd = ["uv", "run", "--isolated", "--no-project", "--python", sys.executable,
                   "--with", f"duckdb=={package}", "python3", str(Path(__file__).resolve()),
                   "--worker", str(manifest_path), "--out", str(path), "--package", package]
            run_worker(cmd, path)
            trials.append(json.loads(path.read_text()) | {"round": round_no})
            print(f"round {round_no + 1}/{rounds}: {package} done", flush=True)
    summary = []
    for i, case in enumerate(manifest["cases"]):
        reference = trials[0]["cases"][i]["executions"][0]["output"]
        equal, exact = True, True
        phases = {}
        for phase in ("first", "warm"):
            samples = {package: [] for package in (BASELINE, CANDIDATE)}
            for trial in trials:
                ex = next(e for e in trial["cases"][i]["executions"] if e["phase"] == phase)
                equal &= compatible(reference, ex["output"])
                exact &= reference == ex["output"]
                samples[trial["package"]].append(ex["seconds"])
            a, b = (statistics.median(samples[p]) for p in (BASELINE, CANDIDATE))
            phases[phase] = dict(baseline_median_s=a, candidate_median_s=b, speedup=a / b,
                                 baseline_range_s=[min(samples[BASELINE]), max(samples[BASELINE])],
                                 candidate_range_s=[min(samples[CANDIDATE]), max(samples[CANDIDATE])])
        summary.append(dict(name=case["name"], parity=equal, exact=exact, phases=phases))
    unchanged = all(digest(REPO / f["path"]) == f["sha256"] for f in manifest["inputs"])
    result = dict(rounds=rounds, cases=summary, inputs_unchanged=unchanged,
                  manifest_sha256=digest(manifest_path),
                  peak_rss_mb={p: [t["peak_rss_mb"] for t in trials if t["package"] == p]
                               for p in (BASELINE, CANDIDATE)})
    save(out / "summary.json", result)
    print(json.dumps(result, indent=2))
    if not unchanged or not all(c["parity"] for c in summary):
        raise SystemExit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path)
    parser.add_argument("--package")
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--out", type=Path, default=HERE / "_cache/run")
    args = parser.parse_args()
    if args.worker:
        worker(args.worker, args.out, args.package)
    else:
        if args.rounds < 2:
            parser.error("at least two alternating rounds required")
        run(args.rounds, args.out)
