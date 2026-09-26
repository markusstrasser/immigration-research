"""Permanent gates: `backcast.py --case sept24` and `--case sept26` rebuild the files committed for those
cases byte for byte, and the default run (schools at full average cost, since 2026-09-26) rebuilds the
derived/ files.

The September 24 files are the ones committed at SEPT24_COMMIT and the September 26 files the ones
committed at SEPT26_COMMIT, the last commits whose derived/ held each run. debt_legacy.py reads each
case's concept columns, so they must keep their values.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/historical_backcast_2026_09_20/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT24_COMMIT = "da2b107"
SEPT26_COMMIT = "f5b4aae"
DERIVED = "infra/immigration-fiscal/historical_backcast_2026_09_20/derived"
NAMES = ("backcast_annual.csv", "backcast_windows.csv")


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "backcast.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit", [("sept24", SEPT24_COMMIT), ("sept26", SEPT26_COMMIT)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit):
    rebuild(tmp_path, "--case", case)
    committed = {n: subprocess.run(["git", "show", f"{commit}:{DERIVED}/{n}"], cwd=ROOT, capture_output=True,
                                   check=True).stdout for n in NAMES}
    differ = [n for n in NAMES if (tmp_path / n).read_bytes() != committed[n]]
    assert not differ, differ


def test_default_rebuilds_derived(tmp_path):
    rebuild(tmp_path)
    differ = [n for n in NAMES if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ
