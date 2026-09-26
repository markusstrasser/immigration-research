"""Permanent gates: `distribute.py --case sept23` and `--case sept24` rebuild the files committed for
those cases byte for byte, and the default September 26 run rebuilds the derived/ files.

Since 2026-09-26 the default run is the adopted September 26 case. The September 23 files are the ones
committed at SEPT23_COMMIT and the September 24 files the ones committed at SEPT24_COMMIT, the last
commits whose derived/ held each run (SEPT23_COMMIT is also the ledger lane's base).

Run from the repository root (about a minute per case with the ACS cache in _cache/):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/distribution_weights_2026_09_23/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT23_COMMIT = "5b8957e"
SEPT24_COMMIT = "6e554a3"
DERIVED = "infra/immigration-fiscal/distribution_weights_2026_09_23/derived"


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "distribute.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit, count", [("sept23", SEPT23_COMMIT, 12), ("sept24", SEPT24_COMMIT, 13)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit, count):
    names = git("ls-tree", "--name-only", f"{commit}:{DERIVED}").decode().split()
    assert len(names) == count, names
    rebuild(tmp_path, "--case", case)
    differ = [n for n in names if (tmp_path / n).read_bytes() != git("show", f"{commit}:{DERIVED}/{n}")]
    assert not differ, differ


def test_sept26_rebuilds_derived(tmp_path):
    names = [Path(p).name for p in git("ls-files", DERIVED).decode().split()]
    assert len(names) == 13, names
    rebuild(tmp_path)
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ
