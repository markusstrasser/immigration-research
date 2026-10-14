"""The lanes' per-process memory budget, measured as the lifetime peak physical footprint.

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from memory_budget import require_within_budget
    ...
    require_within_budget("symmetric comparators")   # once, after the heavy work

Each analysis process stays under 2.5 GB (the machine has 19 GB and runs several lanes at once). Measure
the physical footprint (`proc_pid_rusage`, `ri_lifetime_max_phys_footprint`), not RSS. On macOS
`ru_maxrss` counts clean file-backed pages and moves with the machine's free memory: on 2026-10-14
`symmetric_comparators_oct14.py` read 2.08, 2.27 and 2.16 GB RSS on identical runs and once went over
2.5 GB, failing a correct parent rerun, while its footprint read 2.22, 2.26 and 2.26 GB. A gate on
RSS fails correct runs at random. Elsewhere `ru_maxrss` (kilobytes on Linux) is the fallback.

A wrapper that runs a child command cannot read the child's footprint after it exits; the check
belongs in the process that does the work.
"""
from __future__ import annotations

import ctypes
import ctypes.util
import os
import resource
import sys

LIMIT_BYTES = 2_500_000_000
_RUSAGE_INFO_V4 = 4
_FIELDS = (
    "ri_uuid0", "ri_uuid1", "ri_user_time", "ri_system_time", "ri_pkg_idle_wkups", "ri_interrupt_wkups",
    "ri_pageins", "ri_wired_size", "ri_resident_size", "ri_phys_footprint", "ri_proc_start_abstime",
    "ri_proc_exit_abstime", "ri_child_user_time", "ri_child_system_time", "ri_child_pkg_idle_wkups",
    "ri_child_interrupt_wkups", "ri_child_pageins", "ri_child_elapsed_abstime", "ri_diskio_bytesread",
    "ri_diskio_byteswritten", "ri_cpu_time_qos_default", "ri_cpu_time_qos_maintenance",
    "ri_cpu_time_qos_background", "ri_cpu_time_qos_utility", "ri_cpu_time_qos_legacy",
    "ri_cpu_time_qos_user_initiated", "ri_cpu_time_qos_user_interactive", "ri_billed_system_time",
    "ri_serviced_system_time", "ri_logical_writes", "ri_lifetime_max_phys_footprint", "ri_instructions",
    "ri_cycles", "ri_billed_energy", "ri_serviced_energy", "ri_interval_max_phys_footprint", "ri_runnable_time")


class _RUsageInfoV4(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint64) for name in _FIELDS]


def peak_bytes() -> int:
    """This process's lifetime peak physical footprint in bytes (peak RSS where that is unavailable)."""
    if sys.platform == "darwin":
        lib = ctypes.CDLL(ctypes.util.find_library("proc"), use_errno=True)
        info = _RUsageInfoV4()
        if lib.proc_pid_rusage(os.getpid(), _RUSAGE_INFO_V4, ctypes.byref(info)) != 0:
            raise OSError(ctypes.get_errno(), "proc_pid_rusage failed")
        return int(info.ri_lifetime_max_phys_footprint)
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def require_within_budget(label: str = "process") -> int:
    """Stop with [BLOCKED] when the peak footprint exceeds the budget; return the peak otherwise."""
    peak = peak_bytes()
    if peak > LIMIT_BYTES:
        raise SystemExit(f"[BLOCKED] {label}: peak physical footprint {peak / 1e9:.3f} GB exceeds the "
                         f"{LIMIT_BYTES / 1e9:.1f} GB budget")
    return peak
