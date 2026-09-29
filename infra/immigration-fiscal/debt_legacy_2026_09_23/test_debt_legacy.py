"""Permanent gates: `debt_legacy.py --case sept23`, `--case sept24`, `--case sept26` and `--case sept26_schools`
rebuild the files committed for those cases byte for byte, the default run rebuilds the derived/ files, and
`--case sept29` rebuilds derived/sept29/.

Since 2026-09-27 the default run is the main case of that day (sept27). The files of each earlier case are
the ones committed at its commit below, the last commit whose derived/ held that run. The ledger lane
(winners_losers_2026_09_24) rebuilds its September 23 reference this way, so this must keep passing.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/debt_legacy_2026_09_23/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT23_COMMIT = "96a5c3b"
SEPT24_COMMIT = "ed1b623"
SEPT26_COMMIT = "e62fccb"
SCHOOLS_COMMIT = "90c4b23"
DERIVED = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived"


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "debt_legacy.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit, count", [("sept23", SEPT23_COMMIT, 10), ("sept24", SEPT24_COMMIT, 12),
                                                 ("sept26", SEPT26_COMMIT, 13), ("sept26_schools", SCHOOLS_COMMIT, 14)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit, count):
    names = git("ls-tree", "--name-only", f"{commit}:{DERIVED}").decode().split()
    assert len(names) == count, names
    rebuild(tmp_path, "--case", case)
    differ = [n for n in names if (tmp_path / n).read_bytes() != git("show", f"{commit}:{DERIVED}/{n}")]
    assert not differ, differ


def test_default_rebuilds_derived(tmp_path):
    names = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())
    assert len(names) == 15, names
    rebuild(tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ


def test_sept29_rebuilds_its_directory(tmp_path):
    """The main case of 2026-09-29 writes derived/sept29/: the default run's files for its case, plus the bridge
    from September 27."""
    names = sorted(p.name for p in (HERE / "derived" / "sept29").iterdir())
    default = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())
    assert names == sorted(default + ["sept29_bridge_2024.csv"]), names
    rebuild(tmp_path, "--case", "sept29")
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    differ = [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / "sept29" / n).read_bytes()]
    assert not differ, differ
