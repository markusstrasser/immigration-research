"""Measure an explicit command without ps, sysctl, or /usr/bin/time -l."""
from __future__ import annotations

import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main() -> int:
    command = sys.argv[1:]
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise SystemExit("usage: measure_run.py -- COMMAND [ARGS...]")
    start = time.perf_counter()
    child = subprocess.run(command, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"})
    elapsed = time.perf_counter() - start
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    peak_bytes = rss if sys.platform == "darwin" else rss * 1024
    print(f"[MEASURE] rc={child.returncode} elapsed_s={elapsed:.3f} peak_child_rss_bytes={peak_bytes}", file=sys.stderr)
    # Python producers gate their own physical footprint. A wrapper's RSS can
    # over-read it on macOS; report this diagnostic without a second RSS gate.
    return child.returncode


if __name__ == "__main__":
    raise SystemExit(main())
