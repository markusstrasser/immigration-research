"""Check the still-running Node bridge with the shared physical-footprint schema."""
import ctypes
import ctypes.util
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import memory_budget as memory


def main():
    pid = int(sys.argv[1])
    if pid <= 0 or sys.platform != 'darwin':
        raise SystemExit('[BLOCKED] Node physical-footprint probe needs a live Darwin PID')
    info = memory._RUsageInfoV4()
    lib = ctypes.CDLL(ctypes.util.find_library('proc'), use_errno=True)
    if lib.proc_pid_rusage(pid, memory._RUSAGE_INFO_V4, ctypes.byref(info)) != 0:
        raise OSError(ctypes.get_errno(), 'live Node footprint query failed')
    peak = int(info.ri_lifetime_max_phys_footprint)
    if peak > memory.LIMIT_BYTES:
        raise SystemExit(f'[BLOCKED] Node bridge physical footprint {peak} exceeds {memory.LIMIT_BYTES}')
    print(f'node_physical_footprint_bytes={peak}')


if __name__ == '__main__':
    main()
