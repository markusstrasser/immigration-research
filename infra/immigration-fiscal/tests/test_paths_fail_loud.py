"""Regression check: path resolvers must fail loud on a missing legacy root.

Catalogued failure (2026-09-16 recovery probe): with DERIVED_ROOT unset, ``paths.derived_root()``
returned ``sources/immigration-fiscal/data/derived`` even though that path was a dangling symlink
into a data tree that had vanished from the SSD in mid-August 2026. Builds "succeeded" against a
path that did not exist, which is how the loss stayed hidden for a month. Explicit environment
overrides are still honoured verbatim (they may point at a directory that a build is about to
create); only the implicit fallback is checked for existence.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))

import paths  # noqa: E402


class PathsFailLoud(unittest.TestCase):
    def test_env_override_is_returned_verbatim(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "not-created-yet"
            with mock.patch.dict(os.environ, {"PNY_DATA_ROOT": str(target), "DERIVED_ROOT": str(target)}):
                self.assertEqual(paths.data_root(), target)
                self.assertEqual(paths.derived_root(), target)

    def test_missing_legacy_root_raises(self):
        with tempfile.TemporaryDirectory() as d:
            env = {k: v for k, v in os.environ.items() if k not in {"PNY_DATA_ROOT", "DERIVED_ROOT"}}
            with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(paths, "_REPO_ROOT", Path(d)):
                with self.assertRaises(FileNotFoundError) as ctx:
                    paths.data_root()
                self.assertIn("PNY_DATA_ROOT", str(ctx.exception))
                with self.assertRaises(FileNotFoundError):
                    paths.derived_root()

    def test_dangling_symlink_raises(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / "sources").symlink_to(repo / "vanished-ssd-tree")
            env = {k: v for k, v in os.environ.items() if k not in {"PNY_DATA_ROOT", "DERIVED_ROOT"}}
            with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(paths, "_REPO_ROOT", repo):
                with self.assertRaises(FileNotFoundError):
                    paths.derived_root()

    def test_existing_legacy_root_is_used(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            derived = repo / "sources" / "immigration-fiscal" / "derived"
            derived.mkdir(parents=True)
            env = {k: v for k, v in os.environ.items() if k not in {"PNY_DATA_ROOT", "DERIVED_ROOT"}}
            with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(paths, "_REPO_ROOT", repo):
                self.assertEqual(paths.derived_root(), derived)


if __name__ == "__main__":
    unittest.main()
