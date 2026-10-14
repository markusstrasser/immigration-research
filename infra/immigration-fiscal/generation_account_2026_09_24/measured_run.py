"""Run a command with Python timing/RSS, preserving its exit status.

Native-First: stdlib subprocess, perf_counter and getrusage; ps/sysctl are denied.
Darwin reports ru_maxrss in bytes. Exit 1 if a successful child exceeds 2.5 GB.
"""
import resource
import subprocess
import sys
import time


def main(argv):
    if not argv:
        raise SystemExit("usage: measured_run.py COMMAND [ARG ...]")
    start = time.perf_counter()
    completed = subprocess.run(argv, check=False)
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    print(f"[measured] seconds={time.perf_counter()-start:.3f} peak_bytes={peak} exit={completed.returncode}", flush=True)
    return completed.returncode if completed.returncode else (1 if peak > 2_500_000_000 else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
