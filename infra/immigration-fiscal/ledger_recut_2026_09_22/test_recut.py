"""Re-tests the recut's written artefacts against the pinned ledger's outputs.

    uv run --no-project python3 -m pytest infra/immigration-fiscal/ledger_recut_2026_09_22/ -q
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
LEDGER = HERE.parent / "ledger_absolute_2026_09_17" / "derived"


@pytest.fixture(scope="module")
def audit():
    return json.loads((D / "audit.json").read_text())


@pytest.fixture(scope="module")
def cells():
    return pd.read_csv(D / "named_cells.csv").set_index("id")


@pytest.fixture(scope="module")
def moves():
    return pd.read_csv(D / "switch_moves.csv").set_index("id")


@pytest.fixture(scope="module")
def hulls():
    return pd.read_csv(D / "hulls.csv").set_index("hull")


@pytest.fixture(scope="module")
def arms():
    return pd.read_csv(LEDGER / "arms_matrix.csv")


def grid(arms, f, e, c, r):
    row = arms[(arms.F_arm == f) & (arms.E_arm == e) & (arms.C_arm == c) & (arms.R_arm == r)]
    assert len(row) == 1, (f, e, c, r)
    return float(row.union_absolute_bn.iloc[0])


def test_every_gate_passed(audit):
    failed = [k for k, g in audit["gates"].items() if not g["passed"]]
    assert not failed, failed
    assert audit["gates"]["grid_reproduced"]["cells"] == 63
    assert audit["gates"]["grid_reproduced"]["worst_abs_diff_bn"] < 1e-6


def test_inputs_unchanged_since_run(audit):
    import hashlib
    root = HERE.parents[2]
    for rel, digest in audit["inputs"].items():
        p = root / rel
        assert p.exists(), rel
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, f"{rel} changed since the recut ran"


def test_grid_cells_are_grid_cells(cells, arms):
    assert cells.loc["central", "union_absolute_bn"] == pytest.approx(grid(arms, "zero", "zero", "wage25_capital75", "central"), abs=1e-9)
    assert cells.loc["practitioner_pessimistic_grid", "union_absolute_bn"] == pytest.approx(grid(arms, "zero", "zero", "all_capital", "all_per_capita"), abs=1e-9)
    assert cells.loc["wishful_corner", "union_absolute_bn"] == pytest.approx(arms.union_absolute_bn.max(), abs=1e-9)
    assert cells.loc["second_object_stacked_corner", "union_absolute_bn"] == pytest.approx(arms.union_absolute_bn.min(), abs=1e-9)
    assert cells.loc["second_object_public_goods_on_central", "union_absolute_bn"] == pytest.approx(grid(arms, "per_capita", "zero", "wage25_capital75", "central"), abs=1e-9)


def test_named_cells_are_sums_of_switches(cells, moves):
    central = cells.loc["central", "union_absolute_bn"]
    pess = central + moves.loc[["R_all_per_capita", "C_all_capital", "E_targeted_with_R_central",
                                "F_general_government_response"], "delta_bn"].sum()
    assert cells.loc["practitioner_pessimistic", "union_absolute_bn"] == pytest.approx(pess, abs=1e-9)
    opt = central + moves.loc[["G_function_elasticities", "G_interest_like_federal",
                               "K_D_school_within_pupil_weighted"], "delta_bn"].sum()
    assert cells.loc["practitioner_optimistic", "union_absolute_bn"] == pytest.approx(opt, abs=1e-9)


def test_grid_switches_match_arms_matrix(moves, arms):
    c = grid(arms, "zero", "zero", "wage25_capital75", "central")
    assert moves.loc["R_all_zero", "delta_bn"] == pytest.approx(grid(arms, "zero", "zero", "wage25_capital75", "all_zero") - c, abs=1e-9)
    assert moves.loc["C_per_capita", "delta_bn"] == pytest.approx(grid(arms, "zero", "zero", "per_capita", "central") - c, abs=1e-9)
    assert moves.loc["F_per_capita", "delta_bn"] == pytest.approx(grid(arms, "per_capita", "zero", "wage25_capital75", "central") - c, abs=1e-9)
    assert moves.loc["E_stock_only_with_R_zero", "delta_bn"] == pytest.approx(
        grid(arms, "zero", "stock", "wage25_capital75", "all_zero") - grid(arms, "zero", "zero", "wage25_capital75", "all_zero"), abs=1e-9)


def test_f_split_adds_up(moves):
    parts = moves.loc[["F_defense_per_capita", "F_net_interest_per_capita", "F_general_government_per_capita"], "delta_bn"].sum()
    assert parts == pytest.approx(moves.loc["F_per_capita", "delta_bn"], abs=1e-6)


def test_enforcement_targeted_is_netted_not_stacked(moves, audit):
    stacked = moves.loc["E_stock_only_with_R_zero", "delta_bn"]
    netted = moves.loc["E_targeted_with_R_central", "delta_bn"]
    share = audit["e_targeted"]["union_headcount_share"]
    assert netted == pytest.approx(stacked * (1 - share), abs=1e-6)
    assert 0 > netted > stacked


def test_hulls_ordered_and_stretches_outside(cells, hulls):
    p = hulls.loc["practitioner"]
    assert p.low_bn < p.central_bn < p.high_bn < 0
    assert p.low_bn == pytest.approx(cells.loc["practitioner_pessimistic", "union_absolute_bn"])
    assert p.high_bn == pytest.approx(cells.loc["practitioner_optimistic", "union_absolute_bn"])
    d = hulls.loc["design_grid"]
    assert d.low_bn < p.low_bn and d.high_bn > p.high_bn
    for stretch in ("stretch_school_m_0_63_on_all_dialled", "wishful_corner", "no_congestible_services"):
        assert cells.loc[stretch, "union_absolute_bn"] > p.high_bn
    assert cells.loc["no_congestible_services", "union_absolute_bn"] > 0


def test_g_composition_and_dial(audit):
    comp = pd.read_csv(D / "g_composition.csv")
    assert comp.share.sum() == pytest.approx(1.0, abs=1e-9)
    assert (comp.share * comp.elasticity).sum() == pytest.approx(audit["g_dial"]["m_functions"], abs=1e-12)
    assert audit["g_dial"]["m_both"] == pytest.approx(audit["g_dial"]["m_functions"] - audit["g_dial"]["interest_share"], abs=1e-12)
    held = comp[comp.elasticity_source.str.startswith("none")]
    assert (held.elasticity == 1.0).all()
    # the scaling memo's across-state, year-effects column
    el = audit["elasticities"]
    assert el["police"]["beta"] == pytest.approx(1.037, abs=5e-4)
    assert el["admin"]["beta"] == pytest.approx(0.824, abs=5e-4)
    assert el["fire"]["beta"] == pytest.approx(1.085, abs=5e-4)
    assert el["highways_nontoll"]["beta"] == pytest.approx(0.727, abs=5e-4)
    assert el["school_within_pupil_weighted"]["beta"] == pytest.approx(0.836, abs=5e-4)
    assert el["school_within_unweighted"]["beta"] == pytest.approx(0.735, abs=5e-4)


def test_gross_flows_reproduce_central(cells):
    flows = pd.read_csv(D / "gross_flows.csv").set_index("line").bn
    assert flows["net"] == pytest.approx(cells.loc["central", "union_absolute_bn"], abs=1e-6)
    assert flows["gross receipts"] > 0 > flows["gross outlays"]
    assert set(flows.index) == {"gross receipts", "gross outlays", "net", "replicate standard error of the central"}


def test_point_only_rows_have_no_se(cells):
    for rid in ("stretch_plus_cbo_school_on_base_school", "personal_source_allocation"):
        assert np.isnan(cells.loc[rid, "se_bn"])
