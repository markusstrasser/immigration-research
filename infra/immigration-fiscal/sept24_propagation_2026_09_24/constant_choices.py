"""Federal-dollar effect of the two lane-constant splits where this lane and the ledger lane
(winners_losers_2026_09_24, federal_split()) chose differently.

  row 8   unallocable state-local general public services, +$2.0bn. This lane: federal only through
          grants, at the grant share of state-local general-government spending (0 under the low
          convention). Ledger lane: 0.
  row 10  foster care and adoption keyed by WIC, -$1.5bn. This lane: the federal fraction of
          other_state_welfare, the BEA 3.12 line 39 dollars the audit re-keys (dataset_integrity
          spending.md #9). Ledger lane: the federal fraction of family_and_general_assistance.

Part 1 evaluates both choices on the same September 24 split of 2024, so the difference is the
choice alone. Part 2 re-runs debt_legacy.py on the adopted case with each of the ledger lane's
choices in turn (its constant_parts() wrapped, nothing edited) to size the effect on the legacy
stock and its 2024 interest, where the constant is also carried back through its line's history.
Gate: the re-run's 2024 federal part moves by exactly part 1's difference.

Writes derived/constant_choices.csv (2024 split) and derived/constant_choices_stock.csv (re-runs).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/constant_choices.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "debt_legacy_2026_09_23"
DEBT = LANE / "derived"
CENTRAL = dict(benchmark="main", rule="programme_income_pandemic_per_head", convention="central",
               rate_path="effective", window_start=2005, financing="all_borrowed")


def split_2024():
    split = pd.read_csv(DEBT / "corrections_federal_split_2024.csv")
    lines = pd.read_csv(DEBT / "federal_split_2024_lines.csv")
    rows = []
    for (end, conv), part in split.groupby(["end", "convention"], sort=False):
        ln = lines[(lines.end == end) & (lines.convention == conv)].set_index("line")
        frac = lambda line: float(ln.loc[line, "federal_bn"] / ln.loc[line, "gap_bn"])  # noqa: E731
        r8 = part[part.component == "lane_constants:row8"].iloc[0]
        r10 = part[part.component == "lane_constants:row10"].iloc[0]
        if not np.isclose(r10.federal_bn / r10.effect_bn, frac("other_state_welfare"), rtol=0, atol=1e-6):
            raise SystemExit(f"[BLOCKED] row 10 share is not other_state_welfare's line fraction ({end}, {conv})")
        alt10 = r10.effect_bn * frac("family_and_general_assistance")
        for item, amount, ours, theirs, basis in (
                ("row 8", r8.effect_bn, r8.federal_bn, 0.0, "grant share of state-local general government vs 0"),
                ("row 10", r10.effect_bn, r10.federal_bn, alt10,
                 "other_state_welfare fraction vs family_and_general_assistance fraction")):
            rows.append(dict(end=end, convention=conv, item=item, amount_bn=amount, federal_this_lane_bn=ours,
                             federal_ledger_lane_bn=theirs, federal_difference_bn=ours - theirs,
                             share_this_lane=ours / amount, share_ledger_lane=theirs / amount, basis=basis))
    return pd.DataFrame(rows)


def rerun(item):
    """debt_legacy.py on the adopted case with the ledger lane's split of one constant."""
    spec = importlib.util.spec_from_file_location("debt_legacy_choice", LANE / "debt_legacy.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    original = mod.constant_parts

    def ledger_choice(corner, conv, shares, extras, base_share):
        parts = original(corner, conv, shares, extras, base_share)
        for p in parts:
            if item == "row 8" and p["part"] == "row8":
                p["share"] = p["share"] * 0.0
            if item == "row 10" and p["part"] == "row10":
                p.update(sub="family_and_general_assistance", share=shares[conv]["family_and_general_assistance"],
                         carry="family_and_general_assistance")
        return parts

    mod.constant_parts = ledger_choice
    with tempfile.TemporaryDirectory() as tmp:
        argv, sys.argv = sys.argv, ["debt_legacy.py", "--out-dir", tmp]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                mod.main()
        finally:
            sys.argv = argv
        return pd.read_csv(Path(tmp) / "stocks.csv"), pd.read_csv(Path(tmp) / "federal_split_2024.csv")


def central(stocks):
    m = pd.Series(True, index=stocks.index)
    for k, v in CENTRAL.items():
        m &= stocks[k] == v
    return stocks[m].set_index("end")


def main():
    choices = split_2024()
    choices.to_csv(HERE / "derived" / "constant_choices.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(choices[["end", "convention", "item", "amount_bn", "share_this_lane", "share_ledger_lane", "federal_this_lane_bn",
                   "federal_ledger_lane_bn", "federal_difference_bn"]].round(4).to_string(index=False))
    base_stocks = central(pd.read_csv(DEBT / "stocks.csv"))
    base_split = pd.read_csv(DEBT / "federal_split_2024.csv").query("profile == 'cbo_category_lag_non_school_full'")
    rows = []
    for item in ("row 8", "row 10"):
        stocks, fsplit = rerun(item)
        alt = central(stocks)
        fsplit = fsplit.query("profile == 'cbo_category_lag_non_school_full'")
        for end in ("low", "high"):
            for conv in ("low", "central", "high"):
                got = (fsplit[(fsplit.end == end) & (fsplit.convention == conv)].federal_bn.iloc[0]
                       - base_split[(base_split.end == end) & (base_split.convention == conv)].federal_bn.iloc[0])
                want = -choices[(choices.end == end) & (choices.convention == conv) & (choices.item == item)].federal_difference_bn.iloc[0]
                if not np.isclose(got, want, rtol=0, atol=2e-6):
                    raise SystemExit(f"[BLOCKED] re-run moves the 2024 federal part by {got}, part 1 says {want} ({item}, {end}, {conv})")
            rows.append(dict(item=item, end=end, ledger_minus_this_federal_2024_bn=float(
                             -choices[(choices.end == end) & (choices.convention == "central") & (choices.item == item)].federal_difference_bn.iloc[0]),
                             ledger_minus_this_stock_bn=alt.loc[end, "stock_entering_2024_bn"] - base_stocks.loc[end, "stock_entering_2024_bn"],
                             ledger_minus_this_interest_2024_bn=alt.loc[end, "legacy_interest_2024_bn"] - base_stocks.loc[end, "legacy_interest_2024_bn"]))
    stock = pd.DataFrame(rows)
    stock.to_csv(HERE / "derived" / "constant_choices_stock.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(stock.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
