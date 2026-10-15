"""Read-only upstream replay; all writes are in this lane.

Native-First: subprocess existing Python/Node entrypoints with checked exits.
"""
from datetime import datetime, timezone
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    commands = [
        [sys.executable, str(HERE / "native_measure.py")],
        [sys.executable, str(HERE / "measure.py")],
        [sys.executable, str(HERE / "diagnostics.py")],
        ["node", str(HERE / "evaluate.cjs")],
    ]
    (HERE / "_cache").mkdir(exist_ok=True)
    log = HERE / "_cache/replay.log"
    for command in commands:
        start = time.perf_counter()
        stamp = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if sys.platform != "darwin":
            peak *= 1024
        receipt = f"{stamp} {Path(command[-1]).name}: exit={result.returncode} elapsed={time.perf_counter()-start:.3f}s cumulative_child_peakRSS={peak} bytes\n"
        with log.open("a") as stream:
            stream.write(receipt+result.stdout+result.stderr)
        print(receipt, end="", flush=True)
        if result.returncode:
            print(result.stdout+result.stderr)
            raise SystemExit(result.returncode)
        if peak >= 2_500_000_000:
            raise SystemExit("[BLOCKED] replay child exceeded 2.5GB RSS")


if __name__ == "__main__":
    main()
