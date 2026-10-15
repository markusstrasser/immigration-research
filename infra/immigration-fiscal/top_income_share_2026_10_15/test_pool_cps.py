"""Checks for bin boundaries, pooled replicate ratios and case-key compatibility."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("top_pool_test", HERE / "pool_cps.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)


def test_irs_bins_and_pool_mapping():
    agi = np.array([-1, 0, 1, 4999, 5000, 199999, 200000, 499999, 500000, 999999, 1000000, 5000000])
    b = P.band19(agi)
    np.testing.assert_array_equal(b, [0, 0, 1, 1, 2, 11, 12, 12, 13, 13, 14, 17])
    np.testing.assert_array_equal(P.band14(b), [0, 0, 0, 0, 1, 10, 11, 11, 12, 12, 13, 13])
    assert P.bin_select("200k-500k")[0] == [12]
    assert P.bin_select("200k+")[0] == list(range(12, 19))


def test_pooled_replication_perturbs_each_year_with_other_years_fixed():
    n1 = np.full(161, 2.)
    n2 = np.full(161, 8.)
    d1 = np.full(161, 10.)
    d2 = np.full(161, 30.)
    n1[1:] = 3
    n2[1:] = 10
    value, independent, bound = P.ratio_summary([n1, n2], [d1, d2])
    assert value == .25
    np.testing.assert_allclose(independent, np.sqrt((2 * .025) ** 2 + (2 * .05) ** 2))
    np.testing.assert_allclose(bound, .15)


def test_real2023_uses_income_year_annual_cpi():
    cp = P.cpi()
    assert cp[2018] == 251.107 and cp[2024] == 313.689
    assert cp[2023] / cp[2024] < 1


def test_2025_baseline_reproduces_canonical_raw_and_raked_shares():
    cells = pd.read_csv(HERE / "derived/cps_cells.csv")
    base = cells[cells["sample"] == "baseline_2025_nominal"]
    totals = base.pivot(index="cbo_group", columns="bin14", values="total_fedtax")
    union = base.pivot(index="cbo_group", columns="bin14", values="union_fedtax")
    cbo = P.KEYS.cbo_shares()
    groups = [g for g in P.BF.GROUPS if cbo[g] > 0]
    t = totals.loc[groups].to_numpy()
    u = union.loc[groups].to_numpy()
    rows = np.array([cbo[g] for g in groups])
    cols = P.KEYS._pool14(P.KEYS.irs_2023()[1])
    r = rows[:, None] * t / t.sum(axis=1, keepdims=True)
    for _ in range(20000):
        r *= cols / r.sum(axis=0)
        r *= (rows / r.sum(axis=1))[:, None]
        if np.max(np.abs(r.sum(axis=0) - cols)) < 1e-12:
            break
    else:
        raise AssertionError("baseline raking failed")
    value = np.sum(r * np.divide(u, t, out=np.zeros_like(u), where=t > 0))
    import json
    ref = json.loads((P.FISCAL / "tax_key_heldout_2026_09_28/derived/translation_inputs.json").read_text())
    want = ref["reweighted_share"]["personal"] + ref["share_change"]["irs_2023_raked_with_cbo_groups"]["personal"]
    assert abs(value - want) < 1e-12
    bins = pd.read_csv(HERE / "derived/cps_bins.csv")
    nominal = bins[bins["sample"] == "baseline_2025_nominal"]
    assert int(nominal[nominal.bin19 == "1M+"].union_records.iloc[0]) == 15
    # A positive finite top share requires observed taxed carriers; zero is never silently imputed.
    assert nominal[nominal.bin19 == "1M+"].union_share.iloc[0] > 0
    tails = pd.read_csv(HERE / "derived/cps_tail_support.csv")
    nominal_tail = tails[tails["sample"] == "baseline_2025_nominal"].set_index("threshold")
    assert nominal_tail.loc[1e6, "union_records"] == 15
    assert nominal_tail.loc[1.5e6, "union_records"] == 0
    assert nominal_tail.loc[1.5e6, "all_records"] == 33
    assert nominal_tail.loc[5e6, "all_records"] == 0
