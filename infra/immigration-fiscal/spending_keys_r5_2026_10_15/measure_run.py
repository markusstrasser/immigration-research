"""Time/peak-memory wrapper; writes its machine-dependent log outside the lane.

Usage: uv run --no-project python3 <lane>/measure_run.py --log <scratch.json> -- <command>
"""
import argparse
import datetime
import json
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cmd = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not cmd:
        parser.error('a command is required')
    start = time.perf_counter()
    date = subprocess.check_output(['date', '+%Y-%m-%d %H:%M:%S %Z'], text=True).strip()
    completed = subprocess.run(cmd, check=False)
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    rss = usage.ru_maxrss if sys.platform == 'darwin' else usage.ru_maxrss * 1024
    row = {'date': date, 'elapsed_seconds': time.perf_counter()-start,
           'maxrss_bytes': rss, 'exit_code': completed.returncode, 'command': cmd}
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text(json.dumps(row, indent=2) + '\n')
    print(json.dumps(row), flush=True)
    if rss > 2_500_000_000:
        raise SystemExit('[BLOCKED] child process exceeded 2.5GB physical memory')
    raise SystemExit(completed.returncode)


if __name__ == '__main__':
    main()
