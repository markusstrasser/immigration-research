"""Compare actual caller memory settings and v2's read-ahead control.

Requires a completed trial.py run at --input. Full receipts are ignored in _cache.
"""
import argparse
import itertools
import json
from pathlib import Path
import statistics
import sys
import time

from trial import (BASELINE, CANDIDATE, HERE, REPO, compatible, controls, digest,
                   json_value, quote, run_worker, save)

ARMS = {"baseline": (BASELINE, None), "v2_default": (CANDIDATE, -1),
        "v2_no_read_ahead": (CANDIDATE, 0)}


def worker(manifest_path, out, arm, profile_only=False):
    import duckdb
    package, depth = ARMS[arm]
    if duckdb.__version__ != package:
        raise RuntimeError(f"wrong package: {duckdb.__version__}")
    manifest = json.loads(manifest_path.read_text())
    result = dict(arm=arm, package=package, cases=[], python=sys.version)
    for case in manifest["cases"]:
        with duckdb.connect(case["db"] or ":memory:",
                            read_only=bool(case["db"])) as con:
            con.execute("SET threads=6")
            con.execute("SET TimeZone='UTC'")
            scratch = out.parent / (out.stem + "-scratch")
            scratch.mkdir(exist_ok=True)
            con.execute(f"SET temp_directory={quote(scratch)}")
            if depth is not None:
                con.execute(f"SET read_ahead_depth={depth}")
            result["engine"] = con.execute("SELECT version()").fetchone()[0]
            if depth is not None and not result["engine"].startswith("v2.0.0"):
                raise RuntimeError(f"candidate is not v2: {result['engine']}")
            result["memory_limit"] = con.execute(
                "SELECT current_setting('memory_limit')").fetchone()[0]
            executions = []
            if profile_only:
                path = out.parent / f"{arm}-{case['name']}-profile.json"
                con.execute("SET enable_profiling='json'")
                con.execute(f"SET profiling_output={quote(path)}")
                con.execute(case["sql"]).fetchall()
                con.execute("PRAGMA disable_profiling")
                if not path.is_file():
                    raise RuntimeError(f"profile missing: {path}")
                result["cases"].append(dict(name=case["name"], profile=str(path)))
                continue
            for phase in ("first", "warm"):
                start = time.perf_counter()
                cursor = con.execute(case["sql"])
                schema = [[d[0], str(d[1])] for d in cursor.description]
                rows = cursor.fetchall()
                seconds = time.perf_counter() - start
                converted = [json_value(row) for row in rows]
                converted.sort(key=lambda row: json.dumps(row, sort_keys=True))
                executions.append(dict(phase=phase, seconds=seconds,
                                       output=dict(schema=schema, rows=converted)))
            result["cases"].append(dict(name=case["name"], executions=executions))
    save(out, result)


def run(input_path, out):
    controls()
    input_path, out = input_path.resolve(), out.resolve()
    manifest = json.loads(input_path.read_text())
    if not all(digest(REPO / f["path"]) == f["sha256"] for f in manifest["inputs"]):
        raise RuntimeError("screening inputs/source have changed; rerun trial.py")
    out.mkdir(parents=True, exist_ok=False)
    names = {"ipums_weighted_scan", "acs_81_weight_cells"}
    manifest["cases"] = [c for c in manifest["cases"] if c["name"] in names]
    if {c["name"] for c in manifest["cases"]} != names:
        raise RuntimeError("required screening cases missing")
    manifest["settings"] = dict(threads=6, memory_limit="engine default", timezone="UTC")
    manifest["inputs"].extend(
        dict(path=str(p.relative_to(REPO)), bytes=p.stat().st_size, sha256=digest(p))
        for p in (HERE / "DIAGNOSTIC_PROTOCOL.md", Path(__file__).resolve()))
    manifest_path = out / "manifest.json"
    save(manifest_path, manifest)
    orders = list(itertools.permutations(ARMS))
    save(out / "registered_run.json", dict(orders=orders, manifest_sha256=digest(manifest_path)))

    def execute(arm, path, profiling=False):
        cmd = ["uv", "run", "--isolated", "--no-project", "--python", sys.executable,
               "--with", f"duckdb=={ARMS[arm][0]}", "python3", str(Path(__file__).resolve()),
               "--worker", str(manifest_path), "--arm", arm, "--out", str(path)]
        if profiling:
            cmd.append("--profile-only")
        run_worker(cmd, path)
        return json.loads(path.read_text())

    trials = []
    for i, order in enumerate(orders):
        for arm in order:
            trials.append(execute(arm, out / f"round-{i}-{arm}.json"))
            print(f"round {i + 1}/6: {arm} done", flush=True)
    if len({t["memory_limit"] for t in trials}) != 1:
        raise RuntimeError("default memory budgets differ between arms")
    cases = []
    for i, case in enumerate(manifest["cases"]):
        reference = trials[0]["cases"][i]["executions"][0]["output"]
        parity, exact, phases = True, True, {}
        for phase in ("first", "warm"):
            samples = {arm: [] for arm in ARMS}
            for t in trials:
                ex = next(e for e in t["cases"][i]["executions"] if e["phase"] == phase)
                parity &= compatible(reference, ex["output"])
                exact &= reference == ex["output"]
                samples[t["arm"]].append(ex["seconds"])
            phases[phase] = {arm: dict(median_s=statistics.median(times),
                                       range_s=[min(times), max(times)])
                             for arm, times in samples.items()}
        cases.append(dict(name=case["name"], parity=parity, exact=exact, phases=phases))
    # Collect profiles only after every timed round, so profiling cannot bias arm order.
    for arm in ARMS:
        execute(arm, out / f"{arm}-profiles.json", profiling=True)
    unchanged = all(digest(REPO / f["path"]) == f["sha256"] for f in manifest["inputs"])
    result = dict(cases=cases, memory_limit=trials[0]["memory_limit"],
                  inputs_unchanged=unchanged, manifest_sha256=digest(manifest_path))
    save(out / "summary.json", result)
    print(json.dumps(result, indent=2))
    if not unchanged or not all(c["parity"] for c in cases):
        raise SystemExit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "_cache/run/manifest.json")
    parser.add_argument("--out", type=Path, default=HERE / "_cache/diagnostic")
    parser.add_argument("--worker", type=Path)
    parser.add_argument("--arm", choices=ARMS)
    parser.add_argument("--profile-only", action="store_true")
    args = parser.parse_args()
    if args.worker:
        if not args.arm:
            parser.error("--worker requires --arm")
        worker(args.worker, args.out, args.arm, args.profile_only)
    else:
        run(args.input, args.out)
