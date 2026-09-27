"""Permanent gates: `distribute.py --case sept23`, `--case sept24`, `--case sept26` and `--case sept26_schools`
rebuild the files committed for those cases byte for byte, and the default run rebuilds the derived/ files,
its case_ends.cjs input included.

Since 2026-09-27 the default run is the main case of that day (sept27). The files of each earlier case are the
ones committed at its commit below, the last commit whose derived/ held that run (SEPT23_COMMIT is also the
ledger lane's base).

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
SEPT26_COMMIT = "f697514"
SCHOOLS_COMMIT = "39b854b"
DERIVED = "infra/immigration-fiscal/distribution_weights_2026_09_23/derived"
CASE_ENDS = "case_ends_sept27.json"      # written by case_ends.cjs, read by distribute.py


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "distribute.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit, count", [("sept23", SEPT23_COMMIT, 12), ("sept24", SEPT24_COMMIT, 13),
                                                 ("sept26", SEPT26_COMMIT, 13), ("sept26_schools", SCHOOLS_COMMIT, 13)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit, count):
    names = git("ls-tree", "--name-only", f"{commit}:{DERIVED}").decode().split()
    assert len(names) == count, names
    rebuild(tmp_path, "--case", case)
    differ = [n for n in names if (tmp_path / n).read_bytes() != git("show", f"{commit}:{DERIVED}/{n}")]
    assert not differ, differ


def test_case_ends_rebuild(tmp_path):
    run = subprocess.run(["node", str(HERE / "case_ends.cjs"), "--out-dir", str(tmp_path)], cwd=ROOT,
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
    assert (tmp_path / CASE_ENDS).read_bytes() == (HERE / "derived" / CASE_ENDS).read_bytes()


def test_default_rebuilds_derived(tmp_path):
    names = sorted(p.name for p in (HERE / "derived").iterdir() if p.name != CASE_ENDS)
    assert len(names) == 13, names
    rebuild(tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ
