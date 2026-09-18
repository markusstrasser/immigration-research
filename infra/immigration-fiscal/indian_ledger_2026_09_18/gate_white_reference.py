#!/usr/bin/env python3
"""Gate: this lane's white-reference per-adult net must equal the upstream lane's figure.

Upstream: infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv
(group=third_plus_nh_white, allocation=equal_all_members, weighting=person, adults 25-64).
Checked metrics: the baseline net (taxes minus selected transfers) and the extended balance,
plus the four extension components. Tolerance: $1.00 (the brief's "to the dollar").

Run: uv run --no-project --with "pandas>=2" python3 gate_white_reference.py
Exit 0 = PASS, exit 1 = FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
UPSTREAM = (HERE.parent / "gen_ledger_extension_2026_09_16" / "extended_ledger_by_generation.csv")
MINE = HERE / "derived" / "india_ledger_long.csv"

PAIRS = [
    # (upstream metric, this lane's metric)
    ("cash_noncash_tax_balance", "cash_noncash_tax_balance"),
    ("extended_balance_base", "extended_balance_base"),
    ("modeled_tax_total", "modeled_tax_total"),
    ("selected_cash_total", "selected_cash_total"),
    ("selected_noncash_total", "selected_noncash_total"),
    ("employer_payroll", "employer_payroll"),
    ("sales_tax_share35", "sales_tax_share35"),
    ("property_tax_owner", "property_tax_owner"),
    ("k12_charged_acs_native", "k12_charged"),
]
TOL = 1.00


def main() -> int:
    for p in (UPSTREAM, MINE):
        if not p.exists():
            print(f"✗ missing input: {p}")
            return 1
    up = pd.read_csv(UPSTREAM).query(
        "allocation == 'equal_all_members' and weighting == 'person' "
        "and group == 'third_plus_nh_white'").set_index("metric")
    mine = pd.read_csv(MINE).query(
        "universe == 'adults_25_64' and allocation == 'equal_all_members' "
        "and weighting == 'person' and arm == 'raw' "
        "and group == 'third_plus_nh_white'").set_index("metric")

    ok = True
    print(f"{'metric':32s}{'upstream':>18s}{'this lane':>18s}{'delta':>12s}  result")
    for up_metric, my_metric in PAIRS:
        a = float(up.loc[up_metric, "estimate"])
        b = float(mine.loc[my_metric, "estimate"])
        delta = b - a
        good = abs(delta) <= TOL
        ok &= good
        print(f"{my_metric:32s}{a:>18,.4f}{b:>18,.4f}{delta:>12,.4f}  {'✓ PASS' if good else '✗ FAIL'}")

    n_up = int(up.loc["cash_noncash_tax_balance", "n_adults_unweighted"])
    n_mine = int(mine.loc["cash_noncash_tax_balance", "n_unweighted"])
    same_n = n_up == n_mine
    ok &= same_n
    print(f"{'white-reference cell n':32s}{n_up:>18,d}{n_mine:>18,d}{n_mine - n_up:>12,d}  "
          f"{'✓ PASS' if same_n else '✗ FAIL'}")

    print("\nGATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
