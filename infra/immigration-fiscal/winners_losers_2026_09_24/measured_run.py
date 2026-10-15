"""Run a command with portable wall-time and child peak-RSS measurements.

Native-First: subprocess plus stdlib resource avoids the denied ps/sysctl calls.
Timing logs are ignored cache artifacts, never deterministic derived output.
"""
import json
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def main():
    command = sys.argv[1:]
    if not command:
        raise SystemExit("usage: measured_run.py COMMAND [ARG ...]")
    started = time.perf_counter()
    result = subprocess.run(command, check=False)
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    rss = usage.ru_maxrss
    rss_mb = rss / (1024 * 1024 if sys.platform == "darwin" else 1024)
    row = dict(utc=datetime.now(timezone.utc).isoformat(), command=command,
               seconds=time.perf_counter() - started, peak_rss_mb=rss_mb,
               child_user_cpu_seconds=usage.ru_utime,child_system_cpu_seconds=usage.ru_stime,
               exit_code=result.returncode)
    cache = Path(__file__).resolve().parent / "_cache"
    cache.mkdir(exist_ok=True)
    with (cache / "timings.jsonl").open("a") as stream:
        stream.write(json.dumps(row) + "\n")
    print("[measurement]", json.dumps(row), flush=True)
    # Child RSS is informational. The calculation checks its own lifetime
    # physical footprint with scripts/memory_budget.py before successful exit.
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
