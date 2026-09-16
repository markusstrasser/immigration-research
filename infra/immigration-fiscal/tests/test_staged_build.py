"""Regression check: warehouse builders build beside the target and replace it only on success.

Catalogued failure (2026-09-16 recovery probe): ``build_immigration_warehouse.py`` unlinked the
intact 70-table context warehouse before connecting, so a rebuild that died on missing causal
inputs would have left no warehouse at all (the other four builders had the same delete-first
shape). ``paths.staged_output`` / ``paths.commit_output`` give every builder a scratch file
beside the target and an atomic ``os.replace``; this test pins that contract. The builders
themselves are exercised by a dry run with the *_DUCKDB_PATH env overrides pointed at a scratch
directory (see the 2026-09-16 commit body).
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))

import paths  # noqa: E402


class StagedBuild(unittest.TestCase):
    def test_staged_path_is_sibling_and_parent_is_created(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "warehouse" / "x.duckdb"
            tmp = paths.staged_output(target)
            self.assertEqual(tmp, target.with_name("x.duckdb.building"))
            self.assertTrue(target.parent.is_dir())
            self.assertFalse(tmp.exists())

    def test_stale_staged_file_from_a_dead_build_is_removed(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "x.duckdb"
            stale = target.with_name("x.duckdb.building")
            stale.write_bytes(b"left by a killed build")
            tmp = paths.staged_output(target)
            self.assertEqual(tmp, stale)
            self.assertFalse(tmp.exists())

    def test_failed_build_leaves_target_intact(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "x.duckdb"
            target.write_bytes(b"last good warehouse")
            tmp = paths.staged_output(target)
            tmp.write_bytes(b"partial")
            # A builder that raises never reaches commit_output.
            self.assertEqual(target.read_bytes(), b"last good warehouse")
            self.assertTrue(tmp.exists(), "staged file is kept for diagnosis")

    def test_commit_replaces_target_and_removes_staged_file(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "x.duckdb"
            target.write_bytes(b"old")
            tmp = paths.staged_output(target)
            tmp.write_bytes(b"new")
            out = paths.commit_output(tmp, target)
            self.assertEqual(out, target)
            self.assertEqual(target.read_bytes(), b"new")
            self.assertFalse(tmp.exists())


if __name__ == "__main__":
    unittest.main()
