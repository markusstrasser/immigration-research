"""Fingerprint the pricing route's actual repository reads; block unreviewed drift.

Native-First: read-path guards plus streaming hashlib; no copied source constants.
Capture is an explicit discovery command. Normal runs stop before stale reads.
"""
import builtins
import hashlib
import io
import json
import sys
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import numpy as np
import pyarrow as pa

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
MANIFEST = LANE / "inputs/pricing_dependencies.json"


def runtime():
    return {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pa.__version__}


def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] pricing dependency: " + why)


def digest(path, opener=io.open):
    with opener(path, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def validate_manifest(manifest=None, route="coverage oct14 personal flat pricing"):
    manifest = MANIFEST if manifest is None else manifest
    require(manifest.exists(), "missing manifest; explicit capture is required")
    data = json.loads(manifest.read_text())
    require(data.get("route") == route, "mismatched manifest route")
    require(data.get("runtime") == runtime(), "changed numerical runtime; recapture and reproduce pricing")
    paths = [x["path"] for x in data["files"]]
    require(paths and len(paths) == len(set(paths)), "empty or duplicate dependency manifest")
    for entry in data["files"]:
        path = ROOT / entry["path"]
        require(path.exists() and path.is_file(), "missing " + entry["path"])
        require(path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"],
                "stale " + entry["path"])
    return {x["path"]: x for x in data["files"]}


class ReadGuard:
    def __init__(self, capture, manifest=None, route="coverage oct14 personal flat pricing"):
        self.capture = capture
        self.manifest = MANIFEST if manifest is None else manifest
        self.route = route
        self.entries = {} if capture else validate_manifest(self.manifest, route)
        self.reads = set()
        self.opener = io.open

    def observe(self, value):
        if not isinstance(value, (str, bytes, Path)):
            return
        path = Path(value.decode() if isinstance(value, bytes) else value).resolve()
        if not path.is_relative_to(ROOT) or path.is_relative_to(LANE) or not path.is_file():
            return
        if {".venv", "node_modules"} & set(path.relative_to(ROOT).parts):
            return  # numerical runtime versions are recorded separately; these are not research inputs
        rel = str(path.relative_to(ROOT))
        if rel in self.reads:
            return
        if self.capture:
            self.entries[rel] = {"path": rel, "bytes": path.stat().st_size, "sha256": digest(path, self.opener)}
        else:
            require(rel in self.entries, "new unpinned read " + rel)
            # validate_manifest hashed every prior input before scientific execution begins.
            require(path.stat().st_size == self.entries[rel]["bytes"], "input changed during run " + rel)
        self.reads.add(rel)

    def finish(self):
        for module in list(sys.modules.values()):
            filename = getattr(module, "__file__", None)
            if filename and str(filename).endswith(".py"):
                self.observe(filename)
        for name in ("uv.lock", "pyproject.toml"):
            self.observe(ROOT / name)
        if self.capture:
            payload = {"route": self.route,
                       "runtime": runtime(),
                       "method": "actual Python read paths, pandas Parquet paths, and imported repository modules",
                       "files": [self.entries[p] for p in sorted(self.entries)]}
            self.manifest.write_text(json.dumps(payload, indent=2) + "\n")
        return digest(self.manifest, self.opener)


@contextmanager
def guard(capture=False, manifest=None, route="coverage oct14 personal flat pricing"):
    tracker = ReadGuard(capture, manifest, route)
    old_builtin, old_io, old_parquet = builtins.open, io.open, pd.read_parquet

    def wrapped(opener):
        def call(file, mode="r", *args, **kwargs):
            if "r" in mode and not any(c in mode for c in ("w", "a", "+")):
                tracker.observe(file)
            return opener(file, mode, *args, **kwargs)
        return call

    def parquet(path, *args, **kwargs):
        tracker.observe(path)
        return old_parquet(path, *args, **kwargs)

    builtins.open, io.open, pd.read_parquet = wrapped(old_builtin), wrapped(old_io), parquet
    try:
        yield tracker
    finally:
        builtins.open, io.open, pd.read_parquet = old_builtin, old_io, old_parquet
