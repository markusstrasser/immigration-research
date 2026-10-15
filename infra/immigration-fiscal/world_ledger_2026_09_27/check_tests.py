"""Run the world lane's regression suite with an in-process footprint gate.

Includes test_live_contract.py and test_oct15_core.py, alongside the retained
P7 compensation/incidence/valuation/readings/fix and beside-arm controls.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget


def main():
    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    class Counts:
        passed = 0

        def pytest_sessionfinish(self, session, exitstatus):
            terminal = session.config.pluginmanager.get_plugin("terminalreporter")
            self.passed = len(terminal.stats.get("passed", []))

    counts = Counts()
    code = pytest.main(["-p", "no:cacheprovider", str(HERE), "-q", "--durations=10"], plugins=[counts])
    footprint = require_within_budget("world-ledger tests")
    log = HERE / "_cache/oct15_test_runs.jsonl"
    log.parent.mkdir(exist_ok=True)
    with log.open("a") as f:
        f.write(json.dumps(dict(started=started, seconds=time.perf_counter() - begin,
                              exit_code=code, passed=counts.passed, physical_footprint_bytes=footprint), sort_keys=True) + "\n")
    print(f"physical footprint bytes: {footprint}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
