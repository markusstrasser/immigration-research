"""The pension accrual's 2026 path for the accrual scripts' --case oct07 (main case v6, item 1). Not a script.

The v6 case (main_case_2026_10_07, meta.pension_accrual) takes pension_tr2026_2026_10_06's arm
all_2026_inputs_separate_funds: the OASDI accrual's factor on the 2026 reports' separate-funds payable path with every
2026 input that lane reads (TR 2026's new-issue rates, Note 2026.3's wage index, Table V.C1's COLAs and contribution
bases, the mortality decline, Medicare TR 2026's HI cost per beneficiary, the tax-on-benefits path), over Note
2025.7's basis on the 2025 tables' path; Part A on the 2026 HI path. The case's scheduled-benefits arm stays on the
2025 reports, so the oct07 accrual files carry the payable scenario only.

pension_tr2026.py is imported read-only (nothing is written beside it) and its own functions rebuild the arm's inputs
for any group that accrual_white.py's oasdi_ratio and part_a price:
  payable(P, prelim)  the arm's economy, its payable grid and the benefit-tax timing on its path;
  on_path(P, paths)   the patches under which the pension lane's part_a_pv and model runs read the arm's mortality, HI
                      costs and HI payable path (the survival cache cleared on entry and exit, as the 2026 lane does);
  union_row()         the arm's union row of the 2026 lane's derived/arms.csv, the scripts' gate on their union;
  case_check(meta)    the case payload's ratio_net and Part A accrual are that row's (5e-9, its printed precision).
"""
from __future__ import annotations

import sys
from contextlib import contextmanager
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import pandas as pd  # noqa: E402

FISCAL = Path(__file__).resolve().parent.parent
TR_LANE = FISCAL / "pension_tr2026_2026_10_06"
sys.path.insert(0, str(TR_LANE))
import pension_tr2026 as TR  # noqa: E402  (puts the pension lane on sys.path; TR.PA is pension_accrual)

ARM = "all_2026_inputs_separate_funds"
G, BASE = TR.G, TR.BASE


def blocked(msg):
    raise SystemExit(f"[BLOCKED] {msg}")


def check_module(P):
    if TR.PA is not P:
        blocked("pension_tr2026's pension lane is not the module the accrual script imported")


@contextmanager
def on_path(P, paths):
    """The arm's 2026 mortality decline, HI cost per beneficiary and HI payable path on the pension lane P."""
    check_module(P)
    mort = TR.T.quotes()["tr2026_mortality_decline"]["value"]
    TR.L.survival.cache_clear()
    try:
        with TR.patched(TR.L, "_decline", lambda: (mort["65plus"], mort["total"])), \
                TR.patched(P, "hi_cost_path", TR.hi_cost_path_tr2026), \
                TR.patched(P, "hi_payable", lambda _e: paths["hi_2026"]):
            yield
    finally:
        TR.L.survival.cache_clear()


def payable(P, prelim):
    """The arm's inputs for the payable scenario: (economy, grid, taus, paths). The grid's factor is the separate-funds
    path's k over Note 2025.7's basis on the 2025 tables' path at the 2025 economy (pension_tr2026.hybrid, as its main()
    builds the arm); the timing is tob_timing on the separate-funds path with TR 2026's tax-on-benefits share."""
    check_module(P)
    econ0 = TR.L.Economy()
    paths, _ = TR.build_paths(econ0)
    t25 = TR.grid(econ0, prelim, paths["oasdi_2025"], [G, BASE])
    ea = TR.economy_2026(rates=True, wages=True, parameters=True)
    with on_path(P, paths):
        grid = TR.hybrid(TR.grid(ea, prelim, paths["separate_2026"], [G]), t25)
        with TR.patched(P, "payable_path", lambda _e: paths["separate_2026"]):
            taus = P.tob_timing(ea, prelim, TR.tob_share_tr2026(), runs=[(G, "payable")])
    return ea, grid, taus, paths


def union_row():
    a = pd.read_csv(TR_LANE / "derived/arms.csv")
    r = a[(a.arm == ARM) & (a.group == "union")]
    if len(r) != 1:
        blocked(f"{len(r)} union rows of {ARM} in the 2026 lane's arms.csv")
    return r.iloc[0]


def case_check(meta):
    """The case's pension block is the arm's union row (ratio_net, Part A accrual), to arms.csv's 9 decimals."""
    r, pa = union_row(), meta["pension_accrual"]
    for k, col in (("ratio_net", "net_per_tax_dollar"), ("part_a_accrual_bn", "part_a_bn")):
        if abs(pa[k] - float(r[col])) > 5e-9 * max(1.0, abs(pa[k])):
            blocked(f"the case's pension_accrual.{k} {pa[k]} is not {ARM}'s union {col} {r[col]}")
    return r
