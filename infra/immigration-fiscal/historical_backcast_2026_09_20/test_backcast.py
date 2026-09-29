"""Permanent gates: `backcast.py --case sept24`, `--case sept26` and `--case sept26_schools` rebuild the
files committed for those cases byte for byte, and the default run (the main case of 2026-09-27) rebuilds
the derived/ files, its case_components.cjs input included. The main case adopted on 2026-09-29 (`--case sept29`)
writes derived/sept29/ and derived/case_components_sept29.json beside them; its run rebuilds both.

The files of each earlier case are the ones committed at its commit below, the last commit whose derived/
held that run. debt_legacy.py reads each case's concept columns, so they must keep their values.

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
SCHOOLS_COMMIT = "c0297e4"
DERIVED = "infra/immigration-fiscal/historical_backcast_2026_09_20/derived"
NAMES = ("backcast_annual.csv", "backcast_windows.csv")
PARTS = ("case_parts_windows.csv", "case_parts_annual.csv")
DEFAULT_NAMES = NAMES + PARTS


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "backcast.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit", [("sept24", SEPT24_COMMIT), ("sept26", SEPT26_COMMIT),
                                          ("sept26_schools", SCHOOLS_COMMIT)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit):
    rebuild(tmp_path, "--case", case)
    committed = {n: subprocess.run(["git", "show", f"{commit}:{DERIVED}/{n}"], cwd=ROOT, capture_output=True,
                                   check=True).stdout for n in NAMES}
    differ = [n for n in NAMES if (tmp_path / n).read_bytes() != committed[n]]
    assert not differ, differ
    assert not any((tmp_path / n).exists() for n in PARTS)


@pytest.mark.parametrize("case", ["sept27", "sept29"])
def test_case_components_rebuild(tmp_path, case):
    run = subprocess.run(["node", str(HERE / "case_components.cjs"), "--case", case, "--out-dir", str(tmp_path)], cwd=ROOT,
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
    name = f"case_components_{case}.json"
    assert (tmp_path / name).read_bytes() == (HERE / "derived" / name).read_bytes()


def test_default_rebuilds_derived(tmp_path):
    rebuild(tmp_path)
    differ = [n for n in DEFAULT_NAMES if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ


def test_sept29_rebuilds_its_directory(tmp_path):
    rebuild(tmp_path, "--case", "sept29")
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(p.name for p in (HERE / "derived" / "sept29").iterdir())
    differ = [n for n in DEFAULT_NAMES if (tmp_path / n).read_bytes() != (HERE / "derived" / "sept29" / n).read_bytes()]
    assert not differ, differ
