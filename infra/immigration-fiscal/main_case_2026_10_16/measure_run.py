"""Report elapsed time/RSS; physical-footprint guards run inside producers."""
from __future__ import annotations

import os
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from memory_budget import require_within_budget


def main() -> int:
    command = sys.argv[1:]
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise SystemExit("usage: measure_run.py -- COMMAND [ARGS...]")
    start = time.perf_counter()
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    child = subprocess.run(command, env=env)
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    peak = rss if sys.platform == "darwin" else rss * 1024
    print(
        f"[MEASURE] rc={child.returncode} elapsed_s={time.perf_counter()-start:.3f} peak_child_rss_bytes={peak}",
        file=sys.stderr,
    )
    require_within_budget("v9 command wrapper")
    return child.returncode


if __name__ == "__main__":
    raise SystemExit(main())
