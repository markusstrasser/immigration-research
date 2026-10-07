"""Federal-dollar effect of the two lane-constant splits where this lane and the ledger lane
(winners_losers_2026_09_24, federal_split()) chose differently.

  row 8   unallocable state-local general public services, +$2.0bn. This lane: federal only through
          grants, at the grant share of state-local general-government spending (0 under the low
          convention). Ledger lane: 0.
  row 10  foster care and adoption keyed by WIC, -$1.5bn. This lane: the federal fraction of
          other_state_welfare, the BEA 3.12 line 39 dollars the audit re-keys (dataset_integrity
          spending.md #9). Ledger lane: the federal fraction of family_and_general_assistance.

Part 1 evaluates both choices on the same split of 2024, so the difference is the choice alone. Part 2
re-runs debt_legacy.py on the case with each of the ledger lane's choices in turn (its constant_parts()
wrapped, nothing edited) to size the effect on the legacy stock and its 2024 interest, where the
constant is also carried back through its line's history. Gate: the re-run's 2024 federal part moves by
exactly part 1's difference.

Cases (--case). The base split is a run of debt_legacy.py --case CASE into a temporary directory, so it
does not depend on which case the debt lane's derived/ holds. On the September 26 cases audit row 8 has
a finite-removal piece (row8_finite: row 8's increment times row8_factor - 1, -$0.10bn): part 1 counts
it in row 8, and the ledger lane's choice zeroes it with row 8.
  sept24          the case adopted 2026-09-24 (the committed run)                -> derived/
  sept26          the one-year scenario, main_case_2026_09_26                    -> --out-dir DIR only
  sept26_schools  schools at full average cost                                   -> ../sept26_propagation_2026_09_26/derived/
  sept27          the September 27 case, main_case_long_run_2026_09_27 (default) -> ../sept27_propagation_2026_09_27/derived/
  sept29          the main case adopted 2026-09-29, main_case_2026_09_29          -> derived/sept29/
  oct05           the main case adopted 2026-10-05 (v5), main_case_2026_10_05    -> derived/oct05/
  oct07           main case v6 (v5 plus its meta.items), main_case_2026_10_07   -> derived/oct07/
On oct05 each row also carries the lineage's parts of it: audit row 8's change at the larger group
(v5_union_response:row8) and the added people's copies of the row 8, finite and row 10 parts
(v5_lineage:constants on their lines), which the ledger lane's choice moves alike. On oct07 the same parts carry
the age-mix lineage's amounts; no other item edits row 8's or row 10's line.
The federal part compared is the run's main profile (its summary.json case.main_profile; before September 27
cbo_category_lag_non_school_full). From September 27 the debt lane's fiscal_gap_bn and federal_bn are the
cash part only: the return on public capital and the displaced beneficiaries of capped programs sit in their
own columns and are never compounded. Both constants are cash, so the comparison is unchanged. From September 29
the debt lane compounds the cash set's flows and reports the pension accrual in its own column; both payloads carry
the two constants alike.

Writes constant_choices.csv (2024 split) and constant_choices_stock.csv (re-runs), after every gate.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/constant_choices.py [--case sept24|sept26|sept26_schools|sept27|sept29|oct05|oct07] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "debt_legacy_2026_09_23"
OUT_DIRS = dict(sept24=HERE / "derived", sept26=None, sept26_schools=HERE.parent / "sept26_propagation_2026_09_26" / "derived",
                sept27=HERE.parent / "sept27_propagation_2026_09_27" / "derived", sept29=HERE / "derived" / "sept29",
                oct05=HERE / "derived" / "oct05", oct07=HERE / "derived" / "oct07")
LINEAGE_ROW8 = "v5_union_response:row8"                  # October 5: the per-correction split's lineage components
LINEAGE_CONSTANTS = "v5_lineage:constants"
OLD_PROFILE = "cbo_category_lag_non_school_full"         # the main profile of every case before September 27
CENTRAL = dict(benchmark="main", rule="programme_income_pandemic_per_head", convention="central",
               rate_path="effective", window_start=2005, financing="all_borrowed")
ROW8 = ("lane_constants:row8", "finite_removal:row8")   # audit row 8's components in the per-correction split
ROW8_PARTS = ("row8", "row8_finite")                     # and its parts in debt_legacy.constant_parts()


def split_2024(base: Path):
    split = pd.read_csv(base / "corrections_federal_split_2024.csv")
    lines = pd.read_csv(base / "federal_split_2024_lines.csv")
    rows = []
    for (end, conv), part in split.groupby(["end", "convention"], sort=False):
        ln = lines[(lines.end == end) & (lines.convention == conv)].set_index("line")
        frac = lambda line: float(ln.loc[line, "federal_bn"] / ln.loc[line, "gap_bn"])  # noqa: E731
        r8 = part[part.component.isin(ROW8)]
        if (r8.component == ROW8[0]).sum() != 1 or (r8.component == ROW8[1]).sum() > 1:
            raise SystemExit(f"[BLOCKED] row 8 is not one constant and at most one finite piece ({end}, {conv})")
        finite = (r8.component == ROW8[1]).any()
        r10 = part[part.component == "lane_constants:row10"].iloc[0]
        if not np.isclose(r10.federal_bn / r10.effect_bn, frac("other_state_welfare"), rtol=0, atol=1e-6):
            raise SystemExit(f"[BLOCKED] row 10 share is not other_state_welfare's line fraction ({end}, {conv})")
        # October 5: the lineage's parts of both rows follow the same choice (debt_legacy constant_parts: audit row 8's
        # change at the larger group, a row8_finite part, and the added people's copy of each union part, which keeps
        # the part's name, line and share). None on earlier cases.
        lin8 = part[(part.component == LINEAGE_ROW8) | ((part.component == LINEAGE_CONSTANTS) & (part.line == r8.line.iloc[0]))]
        lin10 = part[(part.component == LINEAGE_CONSTANTS) & (part.line == "other_state_welfare")]
        # on amounts: the split file rounds to 6 decimals, coarse against the lineage's $0.05bn
        if len(lin10) and not np.allclose(lin10.federal_bn, lin10.effect_bn * frac("other_state_welfare"), rtol=0, atol=1.5e-6):
            raise SystemExit(f"[BLOCKED] the lineage's row 10 share is not other_state_welfare's line fraction ({end}, {conv})")
        amount10 = r10.effect_bn + lin10.effect_bn.sum()
        alt10 = amount10 * frac("family_and_general_assistance")
        for item, amount, ours, theirs, basis in (
                ("row 8", r8.effect_bn.sum() + lin8.effect_bn.sum(), r8.federal_bn.sum() + lin8.federal_bn.sum(), 0.0,
                 "grant share of state-local general government vs 0" + ("; with its finite-removal piece" if finite else "")
                 + ("; with the lineage's parts" if len(lin8) else "")),
                ("row 10", amount10, r10.federal_bn + lin10.federal_bn.sum(), alt10,
                 "other_state_welfare fraction vs family_and_general_assistance fraction"
                 + ("; with the lineage's part" if len(lin10) else ""))):
            rows.append(dict(end=end, convention=conv, item=item, amount_bn=amount, federal_this_lane_bn=ours,
                             federal_ledger_lane_bn=theirs, federal_difference_bn=ours - theirs,
                             share_this_lane=ours / amount, share_ledger_lane=theirs / amount, basis=basis))
    return pd.DataFrame(rows)


def debt_run(case: str, out: Path, item: str | None = None):
    """debt_legacy.py --case CASE --out-dir OUT, with the ledger lane's split of one constant (item) or none."""
    spec = importlib.util.spec_from_file_location("debt_legacy_choice", LANE / "debt_legacy.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    original = mod.constant_parts

    def ledger_choice(corner, conv, shares, extras, base_share):
        parts = original(corner, conv, shares, extras, base_share)
        for p in parts:
            if item == "row 8" and p["part"] in ROW8_PARTS:
                p["share"] = p["share"] * 0.0
            if item == "row 10" and p["part"] == "row10":
                p.update(sub="family_and_general_assistance", share=shares[conv]["family_and_general_assistance"],
                         carry="family_and_general_assistance")
        return parts

    if item:
        mod.constant_parts = ledger_choice
    argv, sys.argv = sys.argv, ["debt_legacy.py", "--case", case, "--out-dir", str(out)]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.main()
    except SystemExit as e:
        if e.code not in (0, None):
            raise SystemExit(f"[BLOCKED] debt_legacy.py --case {case}{' (' + item + ')' if item else ''}: {e.code}") from None
    finally:
        sys.argv = argv
    return pd.read_csv(out / "stocks.csv"), pd.read_csv(out / "federal_split_2024.csv")


def central(stocks):
    m = pd.Series(True, index=stocks.index)
    for k, v in CENTRAL.items():
        m &= stocks[k] == v
    return stocks[m].set_index("end")


def main():
    ap = argparse.ArgumentParser(description="Federal-dollar effect of the ledger lane's two constant splits.")
    ap.add_argument("--case", choices=tuple(OUT_DIRS), default="sept27")
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out = args.out_dir or OUT_DIRS[args.case]
    if out is None:
        ap.error(f"--case {args.case} writes only to --out-dir DIR")
    with tempfile.TemporaryDirectory() as tmp:
        base_stocks, base_split = debt_run(args.case, Path(tmp) / "base")
        choices = split_2024(Path(tmp) / "base")
        print(choices[["end", "convention", "item", "amount_bn", "share_this_lane", "share_ledger_lane", "federal_this_lane_bn",
                       "federal_ledger_lane_bn", "federal_difference_bn"]].round(4).to_string(index=False))
        profile = json.loads((Path(tmp) / "base" / "summary.json").read_text())["case"].get("main_profile", OLD_PROFILE)
        base_stocks = central(base_stocks)
        base_split = base_split[base_split.profile == profile]
        if len(base_split) != 6:
            raise SystemExit(f"[BLOCKED] expected 6 rows of the main profile {profile}, got {len(base_split)}")
        rows = []
        for item in ("row 8", "row 10"):
            stocks, fsplit = debt_run(args.case, Path(tmp) / item.replace(" ", ""), item)
            alt = central(stocks)
            fsplit = fsplit[fsplit.profile == profile]
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
    out.mkdir(parents=True, exist_ok=True)
    choices.to_csv(out / "constant_choices.csv", index=False, lineterminator="\n", float_format="%.6f")
    stock.to_csv(out / "constant_choices_stock.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(stock.round(4).to_string(index=False))
    print(f"[{args.case}] gates passed -> {out / 'constant_choices.csv'}, {out / 'constant_choices_stock.csv'}")


if __name__ == "__main__":
    main()
