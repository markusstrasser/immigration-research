"""Live-case reproducibility and retirement of historical producer routes.

Earlier derived files stay frozen. These tests rebuild only oct15 into scratch.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def run(cmd, *, ok=True):
    result = subprocess.run(cmd, cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"},
                            capture_output=True, text=True, check=False)
    assert (result.returncode == 0) == ok, result.stdout[-2000:] + result.stderr[-2000:]
    return result


def test_case_ends_rebuild(tmp_path):
    run(["node", str(HERE / "case_ends.cjs"), "--out-dir", str(tmp_path)])
    name = "case_ends_oct15.json"
    assert (tmp_path / name).read_bytes() == (HERE / "derived" / name).read_bytes()


def test_live_case_rebuilds_its_directory(tmp_path):
    source = HERE / "derived" / "oct15"
    names = sorted(p.name for p in source.iterdir())
    assert len(names) == 13, names
    run([sys.executable, str(HERE / "distribute.py"), "--out-dir", str(tmp_path)])
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    assert all((tmp_path / n).read_bytes() == (source / n).read_bytes() for n in names)


@pytest.mark.parametrize("script,runner", [("case_ends.cjs", "node"), ("distribute.py", sys.executable)])
def test_previous_case_is_not_computed(tmp_path, script, runner):
    result = run([runner, str(HERE / script), "--case", "oct07", "--out-dir", str(tmp_path)], ok=False)
    assert "unknown case oct07" in result.stderr or "invalid choice" in result.stderr
    assert not list(tmp_path.iterdir())


def test_allocation_change_is_not_replayed_as_same_allocation():
    spec = importlib.util.spec_from_file_location("distribution_live", HERE / "distribute.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.DEFAULT_CASE == "oct15"
    assert list(module.LATER_CASES) == ["oct15"]
    fiscal = module.fiscal_totals()
    adopted = fiscal["adopted"]
    assert adopted["allocation"] == "personal"
    assert adopted["allocation_move_from_v6_all"][0] > 0
    for end, key in (("low", "A_low_cost"), ("high", "A_high_cost")):
        assert adopted[key] == adopted["production"]["ends"][end]["A_bn"]


def test_sorted_dimension_metadata_preserves_engine_coordinates():
    spec = importlib.util.spec_from_file_location("distribution_grid_order", HERE / "distribute.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    grid = json.loads((HERE.parent / "main_case_2026_10_15/derived/corrections.json").read_text())["production"]
    reordered = {**grid, "dims": dict(reversed(list(grid["dims"].items())))}
    cell = {k: grid["dims"][k][min(1, len(grid["dims"][k]) - 1)] for k in module.PRODUCTION_DIMS}
    code = "const fs=require('fs'),E=require(process.argv[1]),x=JSON.parse(fs.readFileSync(0,'utf8'));console.log(E.productionIndex({production:{dims:x.dims}},x.cell))"
    index = int(subprocess.run(["node", "-e", code, str(HERE.parent / "assumption_explorer_2026_09_21/engine.js")],
                              input=json.dumps({"dims": grid["dims"], "cell": cell}), text=True,
                              capture_output=True, check=True).stdout)
    expected = (grid["private_wtp_bn"][index], grid["induced_receipts_bn"][index])
    assert module.grid_cell(grid, **cell) == expected
    assert module.grid_cell(reordered, **cell) == expected
