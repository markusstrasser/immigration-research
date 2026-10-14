"""Run a lane script with Python timing, memory and optional profiling.

Run: uv run --no-project python3 {lane}/measured_run.py mortality.py
Uses no ps, sysctl or /usr/bin/time; writes nondeterministic diagnostics only
inside this lane's ignored _cache. Profiling records the >2-minute first run.
"""
import cProfile
import io
import json
import pstats
import resource
import runpy
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def main():
    target = (HERE / sys.argv[1]).resolve()
    if target.parent != HERE:
        raise SystemExit("[BLOCKED] runner target must be a script in this lane")
    started = time.perf_counter()
    profiling = "--profile" in sys.argv
    profiler = cProfile.Profile()
    if profiling:
        profiler.enable()
    runpy.run_path(str(target), run_name="__main__")
    if profiling:
        profiler.disable()
        buffer = io.StringIO()
        pstats.Stats(profiler, stream=buffer).sort_stats("cumulative").print_stats(35)
        (HERE / "_cache/profile.txt").write_text(buffer.getvalue())
    timing = dict(elapsed_seconds=time.perf_counter() - started,
                  peak_ru_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  cpu_user_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                  cpu_system_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime,
                  profiling=profiling)
    (HERE / "_cache/measured_run.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)


if __name__ == "__main__":
    main()
