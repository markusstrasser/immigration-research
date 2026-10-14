"""Measure authorized commands without ps, sysctl or /usr/bin/time -l."""
import datetime
import json
import resource
import subprocess
import sys
import time
from pathlib import Path


def main():
    command = sys.argv[1:]
    if not command:
        raise SystemExit("[BLOCKED] measured_run.py requires a command")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t = time.perf_counter()
    result = subprocess.run(command)
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    memory_bytes = r.ru_maxrss if sys.platform == "darwin" else r.ru_maxrss * 1024
    entry = dict(started=started, command=command, exit_code=result.returncode,
                 seconds=time.perf_counter() - t, peak_memory_bytes=memory_bytes)
    log = Path(__file__).resolve().parent / "_cache/p7_timings.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    print(f"[timing] rc={result.returncode} seconds={entry['seconds']:.2f} peak_GB={memory_bytes / 1e9:.3f}",
          file=sys.stderr)
    if memory_bytes > 2.5e9:
        raise SystemExit("[BLOCKED] command exceeded 2.5 GB memory budget")
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
