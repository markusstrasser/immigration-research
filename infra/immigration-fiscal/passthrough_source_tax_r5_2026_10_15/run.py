"""Reproduce the item lane with Python wall-time/peak-RSS measurements.

Native-First: subprocess the source extractors and existing engines unchanged.
Volatile timing/date logs stay ignored; derived outputs remain deterministic.
"""
from __future__ import annotations

import json
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    started = time.perf_counter()
    (HERE / "_cache").mkdir(exist_ok=True)
    commands = [[sys.executable, str(script)] for script in [HERE / "income_sources.py", HERE / "owner_tax_sources.py", HERE / "job_keys.py"]]
    commands += [["node", str(HERE / "snapshot.cjs")], [sys.executable, str(HERE / "measure.py")],
                 ["node", str(HERE / "evaluate.cjs")]]
    log = []
    for command in commands:
        date = subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip()
        t0 = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        log.append(dict(started_utc=date, command=command, elapsed_seconds=time.perf_counter()-t0,
                        returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        (HERE / "_cache/run_log.json").write_text(json.dumps(log, indent=2) + "\n")
        print(f"{date} {Path(command[1]).name} exit={result.returncode} seconds={log[-1]['elapsed_seconds']:.3f}", flush=True)
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    rss_bytes = rss if sys.platform == "darwin" else rss * 1024
    metrics = dict(elapsed_seconds=time.perf_counter()-started, max_child_rss_bytes=rss_bytes)
    (HERE / "_cache/runtime.json").write_text(json.dumps(metrics, indent=2) + "\n")
    if rss_bytes >= 2_500_000_000:
        raise RuntimeError(f"[BLOCKED] memory budget: {metrics}")
    print(json.dumps(metrics))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
