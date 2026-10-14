"""Measure a checked child command using Python, without ps/sysctl/time -l."""
import resource
import subprocess
import sys
import time
from pathlib import Path


def main():
    args = sys.argv[1:]
    log = None
    if args and args[0] == '--log':
        log = Path(args[1])
        args = args[2:]
    if args and args[0] == '--':
        args = args[1:]
    if not args:
        raise SystemExit('usage: measured_run.py -- command [args]')
    start = time.perf_counter()
    result = subprocess.run(args, check=False)
    used = resource.getrusage(resource.RUSAGE_CHILDREN)
    rss_bytes = used.ru_maxrss if sys.platform == 'darwin' else used.ru_maxrss * 1024
    message = (f'MEASURED elapsed_seconds={time.perf_counter() - start:.3f} peak_rss_gb={rss_bytes / 1e9:.3f} '
               f'cpu_user_seconds={used.ru_utime:.3f} cpu_system_seconds={used.ru_stime:.3f} '
               f'major_faults={used.ru_majflt} swaps={used.ru_nswap} exit={result.returncode}')
    print(message, flush=True)
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(message + '\n')
    if rss_bytes > 2.5e9:
        raise SystemExit('[BLOCKED] child exceeded 2.5 GB memory budget')
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
