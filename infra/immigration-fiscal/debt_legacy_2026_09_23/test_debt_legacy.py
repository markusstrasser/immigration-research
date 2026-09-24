"""Permanent gate: `debt_legacy.py --case sept23` rebuilds the September 23 outputs byte for byte.

Since 2026-09-24 the default run is the adopted September 24 case. The September 23 files are the ones
committed at SEPT23_COMMIT, the last commit whose derived/ held that run. The ledger lane
(winners_losers_2026_09_24) rebuilds its September 23 reference this way, so this must keep passing.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/debt_legacy_2026_09_23/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT23_COMMIT = "96a5c3b"
DERIVED = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived"


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def test_sept23_rebuilds_committed_files(tmp_path):
    names = git("ls-tree", "--name-only", f"{SEPT23_COMMIT}:{DERIVED}").decode().split()
    assert len(names) == 10, names
    run = subprocess.run([sys.executable, str(HERE / "debt_legacy.py"), "--case", "sept23", "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]
    differ = [n for n in names if (tmp_path / n).read_bytes() != git("show", f"{SEPT23_COMMIT}:{DERIVED}/{n}")]
    assert not differ, differ
