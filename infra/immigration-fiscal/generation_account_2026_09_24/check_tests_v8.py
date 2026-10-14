"""Run the lane's Python regressions with the in-process footprint gate."""
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget
import pytest


def main():
    start = time.perf_counter()
    tests = sys.argv[1:] or [str(HERE)]
    code = pytest.main([*tests, "-q", "-o", f"cache_dir={HERE}/_cache/pytest"])
    peak = require_within_budget("generation Python regressions")
    print(f"tests seconds={time.perf_counter()-start:.3f} physical_peak_bytes={peak} diagnostic_maxrss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
    raise SystemExit(code)


if __name__ == "__main__":
    main()
