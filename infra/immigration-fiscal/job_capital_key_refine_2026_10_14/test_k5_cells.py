"""Checks for subsidy sign, closure and overlap-policy conservation."""
import json
from pathlib import Path

import numpy as np

from k5_cells import mapped_vector, parse_sut

HERE = Path(__file__).resolve().parent


def test_explicit_rounding_closes_each_primary_row():
    rows, totals = parse_sut(HERE / "_cache/k4_bea_supply_use.zip")
    for code, total in totals.items():
        assert abs(sum(r["national_bn"] for r in rows if r["source_row"] == code) - total) < 1e-6
    assert totals["T00OSUB"] != totals["T00SUB"]


def test_overlap_exclusions_are_exact_and_do_not_remove_unrelated_cells():
    cells = ["111CA", "624", "ORE", "482"]
    rows = [{"cell": c, "national_bn": a} for c, a in zip(cells + ["HS", "GSLE"], [10, 4, 2, 1, 50, 20])]
    assert np.array_equal(mapped_vector(rows, cells), [10, 4, 2, 1])
    assert np.array_equal(mapped_vector(rows, cells, 0, False, False), [0, 0, 0, 1])


def test_published_replicate_gates_and_live_carriers():
    result = json.loads((HERE / "derived/k5_cells_summary.json").read_text())
    assert all(g["passed"] for g in result["gates"])
    assert len(result["live_case_trace"]) == 4
    arms = result["arms"]
    for name, arm in arms.items():
        assert arm["union"]["delta_net_cost_bn"] > 0
        assert arm["lineage"]["delta_net_cost_bn"] >= arm["union"]["delta_net_cost_bn"]
        assert arm["response_low"] == arm["response_high"] == 1
    assert arms["ag1_624included_oreincluded"]["union"]["delta_net_cost_bn"] > arms["ag0_624included_oreincluded"]["union"]["delta_net_cost_bn"]
