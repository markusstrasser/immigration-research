"""Tests for lane pension_tr2026_2026_10_06: the positive control through the pension lane's own code, the payable paths
against every printed share, the swap's identity on equal paths, and the engine run's gates and bands. The last two
read derived/, so pension_tr2026.py and case_tr2026.cjs run first (the rerun command list runs them in order).

Run from the repository root (about half a minute):
  uv run --no-project python3 -m pytest infra/immigration-fiscal/pension_tr2026_2026_10_06/ -q
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # the imports reach other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pytest  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pension_tr2026 as M  # noqa: E402

DERIVED = HERE / "derived"
MAIN_CASE = HERE.parent / "main_case_2026_10_05" / "derived" / "summary.json"


@pytest.fixture(scope="module")
def lane():
    return M.Lane()


@pytest.fixture(scope="module")
def built(lane):
    return M.build_paths(lane.econ)


@pytest.fixture(scope="module")
def lane_grid(lane, built):
    paths, _ = built
    return M.grid(lane.econ, lane.prelim, paths["oasdi_lane_2025"], [M.G, M.BASE])


def test_positive_control_reproduces_the_pension_lane(lane, built, lane_grid):
    """The pension lane's central through its own code: per tax dollar by generation, the benefit-tax shares,
    ratio_net, Part A, every hi_arms.csv row and the case on accrual (gate_control stops with [BLOCKED] otherwise)."""
    paths, _ = built
    control = M.run_arm(lane, lane_grid, paths["oasdi_lane_2025"], None, hi_full=True)
    gates = M.gate_control(control)
    assert gates["hi_arms_rows"] == 448 and gates["hi_arms_worst_abs"] <= 5.1e-7
    lane_summary = json.loads((M.PENSION_DERIVED / "summary.json").read_text())
    assert control["ratio_net"] == pytest.approx(lane_summary["ratio_net"], rel=1e-12)
    assert control["case"]["low"]["case_on_accrual_net_bn"] == pytest.approx(
        lane_summary["case_on_accrual_net_bn"]["low"], rel=1e-12)


def test_swap_is_the_identity_on_equal_paths(lane, built, lane_grid):
    """Table 3 x k_new / mwr_base_old reduces to the lane's own factor when the new path is the old one."""
    paths, _ = built
    own = M.run_arm(lane, lane_grid, paths["oasdi_lane_2025"], None)
    same = M.run_arm(lane, M.hybrid(lane_grid, lane_grid), paths["oasdi_lane_2025"], None)
    assert same["ratio_net"] == own["ratio_net"] and same["part_a_bn"] == own["part_a_bn"]
    assert set(same["groups"]) == set(M.GROUPS)


def test_paths_reproduce_every_printed_share(built):
    paths, info = built
    gates = M.path_gates(paths, info)
    assert len(gates) == 16 and bool(gates.passed.all())
    assert {k: v["depletion_year"] for k, v in info.items()} == {
        "oasdi_2025": 2034, "oasdi_2026": 2034, "oasi_2025": 2033, "oasi_2026": 2032, "hi_2025": 2033, "hi_2026": 2033}
    # full benefits before depletion; a share in (0, 1] after it, below 1 in the first year after
    for k, inf in info.items():
        v, d = paths[k], inf["depletion_year"]
        assert np.all(v[(M.YEARS >= 2025) & (M.YEARS < d)] == 1.0), k
        after = v[(M.YEARS > d) & (M.YEARS <= 2100)]
        assert np.all((after > 0) & (after <= 1)) and after[0] < 1, k


def test_engine_run_gates_and_bands():
    c = json.loads((DERIVED / "case_oct05.json").read_text())
    v5 = json.loads(MAIN_CASE.read_text())
    s = json.loads((DERIVED / "summary.json").read_text())
    assert len(c["gates"]) == 13 and all(g["passed"] for g in c["gates"])
    assert c["arms"]["control"]["band_bn"] == pytest.approx(v5["main_case"], abs=1e-9)
    assert c["arms"]["control"]["band_change_bn"] == [0, 0]
    assert c["cash_set_band_bn"] == pytest.approx(v5["cash_set"]["band_bn"], abs=1e-9)
    assert c["engine_change_minus_edit_sum_worst_bn"] < 1e-9
    assert c["arms"]["control"]["per_member_usd"] == pytest.approx(v5["v5"]["per_member_usd"]["set"], abs=1e-6)
    for name, a in c["arms"].items():
        assert a["band_specs"] == [48, 11], name
        assert all(math.isfinite(x) for x in a["per_member_usd"]), name
        src = s["arms"].get(name) or s["beside"][name]
        assert a["ratio_net"] == src["ratio_net"] and a["part_a_bn"] == src["part_a_bn"], name
    assert set(c["arms"]) == set(s["arms"]) | set(s["beside"])


def test_case_rows_add_up():
    """Each arm's change at each end is its four parts (union and lineage, OASDI and Part A), to the csv's rounding."""
    with open(DERIVED / "case_oct05.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows
    for r in rows:
        parts = sum(float(r[k]) for k in ("change_union_oasdi_bn", "change_union_part_a_bn", "change_lineage_oasdi_bn",
                                          "change_lineage_part_a_bn"))
        assert abs(float(r["change_bn"]) - parts) <= 3e-6, (r["arm"], r["end"])
        assert abs(float(r["arm_bn"]) - float(r["case_bn"]) - float(r["change_bn"])) <= 2e-6, (r["arm"], r["end"])


def test_outputs_use_lf():
    for f in sorted(DERIVED.glob("*.csv")) + sorted(DERIVED.glob("*.json")):
        assert b"\r\n" not in f.read_bytes(), f.name
