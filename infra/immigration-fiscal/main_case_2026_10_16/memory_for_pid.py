"""Read the canonical memory metric for a still-live Node process, without ps/sysctl."""
from __future__ import annotations

import ctypes
import ctypes.util
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from memory_budget import LIMIT_BYTES, _RUSAGE_INFO_V4, _RUsageInfoV4


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("[BLOCKED] usage: memory_for_pid.py NODE_PID NODE_PEAK_RSS_KIB")
    pid, rss_kib = map(int, sys.argv[1:])
    if pid <= 0 or rss_kib < 0:
        raise SystemExit("[BLOCKED] invalid target PID or RSS diagnostic")
    if sys.platform == "darwin":
        lib = ctypes.CDLL(ctypes.util.find_library("proc"), use_errno=True)
        info = _RUsageInfoV4()
        if lib.proc_pid_rusage(pid, _RUSAGE_INFO_V4, ctypes.byref(info)) != 0:
            raise SystemExit(f"[BLOCKED] proc_pid_rusage({pid}): errno={ctypes.get_errno()}")
        peak, metric = int(info.ri_lifetime_max_phys_footprint), "lifetime_peak_physical_footprint"
    else:
        peak, metric = rss_kib * 1024, "peak_rss_fallback"
    if peak <= 0:
        raise SystemExit("[BLOCKED] nonpositive principal memory measurement")
    result = {"metric": metric, "peak_bytes": peak, "limit_bytes": LIMIT_BYTES, "pass": peak <= LIMIT_BYTES}
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
