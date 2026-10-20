"""Capture or byte-verify the exact oct16 source-cell artifact.

The artifact ships as deterministic gzip (57 MB of JSON, 3.3 MB compressed); its pin hashes the JSON content.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

from gz_io import gzip_bytes, read_artifact

HERE = Path(__file__).resolve().parent
TARGET = HERE / "inputs/pension_cash_cells_oct16.json.gz"


def run(capture=False):
    from v9_snapshot import require_adopted, verify
    if capture:
        require_adopted("oct16")
    verify()
    with tempfile.TemporaryDirectory(prefix="world-v9-cells-") as directory:
        output = Path(directory) / "cells.json"
        result = subprocess.run(["node", str(HERE / "v9_cells.cjs"), str(output)])
        if result.returncode:
            raise SystemExit(result.returncode)
        body = output.read_bytes()
    pins_path = HERE / "inputs/pension_cash_pins.json"
    pins = json.loads(pins_path.read_text())
    if capture:
        TARGET.write_bytes(gzip_bytes(body))
        pins["artifacts"]["oct16_cash"] = dict(case="oct16", package_set="cash", path=str(TARGET.relative_to(HERE)),
            sha256=hashlib.sha256(body).hexdigest(), provenance="[WORKTREE INPUT] exact v9 cells; typed source posts, source joint16/17 and complete before/after hashes")
        pins_path.write_text(json.dumps(pins, indent=2) + "\n")
    elif not TARGET.is_file() or read_artifact(TARGET) != body or hashlib.sha256(body).hexdigest() != pins["artifacts"].get("oct16_cash", {}).get("sha256"):
        raise SystemExit("[BLOCKED] oct16 source-cell artifact differs; explicit --capture required after source review")
    artifact = json.loads(body)
    for basis, block in artifact["results"].items():
        suffix = "_cash" if basis == "cash" else ""
        pd.DataFrame(block["lines"]).to_csv(HERE / f"derived/generation_lines_oct16{suffix}.csv", index=False,
            lineterminator="\n", float_format="%.12f")
    verify()
    print("oct16 exact source-cell artifact " + ("CAPTURED" if capture else "IDENTICAL"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    run(parser.parse_args().capture)
