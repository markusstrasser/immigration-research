"""Rebuild the lane and run its tests; timing is printed and saved only in ignored cache.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/top_income_share_2026_10_15/run_all.py
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    commands = [
        [sys.executable, str(HERE / "pool_cps.py")],
        [sys.executable, str(HERE / "outside_checks.py")],
        [sys.executable, str(HERE / "federal_arms.py")],
        [sys.executable, str(HERE / "state_correction.py")],
        ["node", str(HERE / "price_v8.cjs")],
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         str(HERE / "test_pool_cps.py"), str(HERE / "test_outside_checks.py"),
         str(HERE / "test_federal_arms.py"), str(HERE / "test_state_correction.py"),
         str(HERE / "test_v8.py")],
        [sys.executable, str(HERE / "render_result.py")],
    ]
    log = []
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    for command in commands:
        date = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M:%S UTC"], text=True).strip()
        start = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, env=env, check=False)
        elapsed = time.perf_counter() - start
        peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        peak_gib = peak / (1024**3 if sys.platform == "darwin" else 1024**2)
        row = dict(date_utc=date, command=" ".join(command), exit_code=result.returncode,
                   elapsed_seconds=elapsed, cumulative_child_peak_gib=peak_gib)
        log.append(row)
        print(json.dumps(row), flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
        if peak_gib >= 2.5e9 / 1024**3:
            raise SystemExit("[BLOCKED] cumulative child peak exceeds 2.5 GB")
    (HERE / "_cache/run_log.json").write_text(json.dumps(log, indent=2) + "\n")


if __name__ == "__main__":
    main()
