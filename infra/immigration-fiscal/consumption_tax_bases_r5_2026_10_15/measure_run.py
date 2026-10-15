#!/usr/bin/env python3
"""Run commands with Python timing/resource measurements, including subprocess failures.

Native-First: subprocess + perf_counter/getrusage; no ps, sysctl or time -l.
Measurements go to the ignored cache so output fingerprints remain deterministic.
"""
from pathlib import Path
import datetime
import json
import os
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def run(command):
    start = time.perf_counter()
    began = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                                        "OPENBLAS_NUM_THREADS": "1"})
    elapsed = time.perf_counter() - start
    raw_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    rss = raw_rss if sys.platform == "darwin" else raw_rss * 1024
    record = {"started_utc": began, "command": command, "seconds": elapsed,
              "child_maxrss_bytes": rss, "exit_code": result.returncode}
    (HERE / "_cache").mkdir(exist_ok=True)
    with (HERE / "_cache" / "timings.jsonl").open("a") as stream:
        stream.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)
    if rss >= 2.5e9:
        raise SystemExit("[BLOCKED] process memory exceeded 2.5GB")
    return result.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: measure_run.py COMMAND [ARG ...]")
    raise SystemExit(run(sys.argv[1:]))
