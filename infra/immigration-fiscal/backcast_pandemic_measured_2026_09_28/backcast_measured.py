#!/usr/bin/env python3
"""Carry the programme back-cast's benefit lines with measured shares instead of the 2024 ratio.

Reads historical_backcast_2026_09_20 (its helpers, pinned BEA workbooks and published outputs) and
debt_legacy_2026_09_23 (the adopted case's programme version); edits neither. The measured input is this
lane's derived/measured_shares.csv (measure_shares.py).

The back-cast carries each 2024 line as target_bn x real national index x the group's population-share path:
the group's use of the programme relative to its population share (its relative use) stays at 2024. Here that
relative use is replaced by the CPS measurement on the same key and allocation, so the population path is
untouched and every 2024 anchor is reproduced.

Refundable tax credits (NIPA 3.12 line 25) held the economic impact payments in 2020 and 2021 (BEA: $274.7bn
and $569.2bn). In those years the line is split: the payments take the group's measured payment share under
each round's SSN rule, and the rest of the line keeps the account's credit key (EITC plus ACTC) at its measured
relative use.

Variants:
  refundable_pandemic        only the refundable-credit line, 2020-2021 (the brief's replacement), one row per
                             SSN treatment: modeled (Census, no SSN rule), borjas, borjas_own. The rest of the
                             line takes the same income year's credit key, the account's own convention.
  refundable_payment_timing  as refundable_pandemic (borjas), but the rest of the line takes the key of the tax
                             year NIPA pays it in: 2020 the 2019 key; 2021 the 2020 key, except the advance child
                             credit ($98.3bn, BEA's 2021 child credit less its 2020 level) at the 2021 ACTC key;
                             2022 the 2021 key.
  all_measured               every CPS-keyed benefit line, 2019-2023, refundable credits as refundable_pandemic
                             (borjas)

Also writes the measured relative use of every key against 2024 (derived/ratio_vs_2024.csv, task 3).

Run from the repository root after measure_shares.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/backcast_measured.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
BACKCAST = FISCAL / "historical_backcast_2026_09_20"
LEGACY = FISCAL / "debt_legacy_2026_09_23"
ACCOUNT = FISCAL / "full_account_spending_2026_09_20/derived"
sys.path.insert(0, str(BACKCAST))
from backcast import YEARS, series, workbook  # noqa: E402
from backcast_categories import BEA, CASES, Cells  # noqa: E402

# NIPA refundable tax credits: economic impact payments and the child tax credit by payment year, $bn nominal.
# BEA, "Effects of Selected Federal Pandemic Response Programs on Personal Income", 2022Q4 third estimate
# (March 2023), annual table lines 31 and 30; quotes `bea_annual_eip` and `bea_annual_ctc` in reads/quotes.json.
EIP_NOMINAL = {2020: 274.7, 2021: 569.2}
CTC_NOMINAL = {2019: 31.1, 2020: 30.2, 2021: 128.5, 2022: 94.3}
ADVANCE_CTC_2021 = CTC_NOMINAL[2021] - CTC_NOMINAL[2020]
RTC = "refundable_tax_credits"
RTC_CELL = "T31200-A:25"
SSN_STATUS = ("modeled", "borjas", "borjas_own")
PRIMARY_STATUS = "borjas"
MEASURED_YEARS = [2019, 2020, 2021, 2022, 2023]
PANDEMIC = [2020, 2021]
WINDOWS = {"10y_2015_2024": 2015, "15y_2010_2024": 2010, "20y_2005_2024": 2005}
ALLOCATION_OF_END = {"low": "shared", "high": "personal"}   # the account's convention, both case families
FLAG = 0.10


def load_measured(directory: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    m = pd.read_csv(directory / "measured_shares.csv")
    plain = m[m.status == "none"].set_index(["key", "allocation", "income_year"])
    eip = m[m.status != "none"].set_index(["key", "status", "allocation", "income_year"])
    return plain, eip


def eip_use(eip: pd.DataFrame, status: str, allocation: str) -> dict[int, float]:
    """The group's relative use of the payments made in each NIPA year. 2020: the EIP1 advance. 2021: EIP2 and
    the EIP1 catch-up (income-2020 units) with EIP3 (income-2021 units), weighted by their CPS national
    amounts, which split BEA's 2021 total."""
    def get(key: str, year: int) -> tuple[float, float] | None:
        idx = (key, status, allocation, year)
        return (eip.loc[idx, "relative_use"], eip.loc[idx, "national_bn"]) if idx in eip.index else None
    use_2020 = get("eip1_advance", 2020)[0]
    rounds = [r for r in (get("eip2", 2020), get("eip1_catchup", 2020), get("eip3", 2021)) if r is not None]
    use_2021 = sum(u * n for u, n in rounds) / sum(n for _, n in rounds)
    return {2020: use_2020, 2021: use_2021}


def credit_use(plain: pd.DataFrame, allocation: str, timing: str, line: pd.Series) -> dict[int, float]:
    """Relative use of the credit line's non-payment part (EITC, ACTC and the rest), by NIPA year."""
    u = lambda key, year: plain.loc[(key, allocation, year), "relative_use"]  # noqa: E731
    if timing == "same_year":
        return {year: u("refundable_credits", year) for year in MEASURED_YEARS}
    rest_2021 = line[2021] - EIP_NOMINAL[2021]
    return {2020: u("refundable_credits", 2019),
            2021: (ADVANCE_CTC_2021 * u("actc", 2021)
                   + (rest_2021 - ADVANCE_CTC_2021) * u("refundable_credits", 2020)) / rest_2021,
            2022: u("refundable_credits", 2021)}


class Paths:
    """The back-cast's national indexes and population-share path, rebuilt as backcast_categories.py builds
    them (same pinned workbooks and helpers)."""

    def __init__(self) -> None:
        self.cells = Cells(workbook(BEA / "Section3All_xls.xlsx"))
        annual = pd.read_csv(BACKCAST / "derived/backcast_annual.csv").set_index("year")
        price = series(workbook(BEA / "Section1All_xls.xlsx"), "T10109-A", "Gross domestic product")
        people = series(workbook(BACKCAST / "_cache/Section7All_xls.xlsx"), "T70100-A",
                        "Population (midperiod, thousands)")
        self.real = price[2024] / price.reindex(YEARS)
        share = annual.group_millions / (people.reindex(YEARS) / 1e3)
        self.share = (share / share[2024]).reindex(YEARS)
        self.rtc = self.cells.get(RTC_CELL)

    def index(self, reference: str) -> pd.Series:
        nominal = self.cells.get(reference)
        return nominal * self.real / nominal[2024]


def line_paths(paths: Paths, amount: float, cells: str, key: str, allocation: str, plain: pd.DataFrame,
               years: list[int], anchor: dict, eip_u: dict[int, float], rtc_u: dict[int, float]
               ) -> tuple[pd.Series, pd.Series]:
    """(old, new) real 2024 $bn path of one benefit line whose 2024 amount is `amount`."""
    old = amount * paths.index(cells) * paths.share
    new = old.copy()
    u24 = plain.loc[(key, allocation, 2024), "relative_use"]
    for year in years:
        if cells != RTC_CELL:
            new[year] = old[year] * plain.loc[(key, allocation, year), "relative_use"] / u24
            continue
        paid = EIP_NOMINAL.get(year, 0.0)
        rest = (paths.rtc[year] - paid) / paths.rtc[2024]
        per_person = anchor["pool"] * anchor["pop_share_2024"] * paths.real[year] * paths.share[year]
        new[year] = amount * paths.real[year] * paths.share[year] * rtc_u[year] / u24 * rest \
            + (per_person * eip_u[year] * paid if paid else 0.0)
    return old, new


def credit_parts(paths: Paths, amount: float, allocation: str, plain: pd.DataFrame, anchor: dict,
                 eip_u: dict[int, float], rtc_u: dict[int, float]) -> list[dict]:
    """The credit line in the payment years, split into the payments and the rest of the line, old and new."""
    u24 = plain.loc[("refundable_credits", allocation, 2024), "relative_use"]
    rows = []
    for year, paid in EIP_NOMINAL.items():
        carried = amount * paths.real[year] * paths.share[year] / paths.rtc[2024]
        per_person = anchor["pool"] * anchor["pop_share_2024"] * paths.real[year] * paths.share[year]
        rows.append(dict(year=year, old_payments_bn=carried * paid, old_rest_bn=carried * (paths.rtc[year] - paid),
                         new_payments_bn=per_person * eip_u[year] * paid,
                         new_rest_bn=carried * (paths.rtc[year] - paid) * rtc_u[year] / u24))
    return rows


def windows(net: pd.Series) -> dict[str, float]:
    return {w: float(net[net.index >= start].sum()) / 1e3 for w, start in WINDOWS.items()}


def pandemic_share(net: pd.Series) -> float:
    return float(net[PANDEMIC].sum() / net[net.index >= 2015].sum())


def variants(plain: pd.DataFrame, eip: pd.DataFrame, allocation: str, line: pd.Series):
    """(variant, status, years, lines or None for every measured line, EIP use, credit use)."""
    same = credit_use(plain, allocation, "same_year", line)
    for status in SSN_STATUS:
        yield "refundable_pandemic", status, PANDEMIC, {RTC}, eip_use(eip, status, allocation), same
    yield ("refundable_payment_timing", PRIMARY_STATUS, [2020, 2021, 2022], {RTC},
           eip_use(eip, PRIMARY_STATUS, allocation), credit_use(plain, allocation, "payment", line))
    yield "all_measured", PRIMARY_STATUS, MEASURED_YEARS, None, eip_use(eip, PRIMARY_STATUS, allocation), same


def sept20(paths: Paths, plain: pd.DataFrame, eip: pd.DataFrame, anchor: dict) -> tuple[list, list, list, list]:
    """The programme back-cast on the September 20 anchors (backcast_categories.py)."""
    categories = pd.read_csv(ACCOUNT / "categories.csv").set_index("category")
    spending = pd.read_csv(ACCOUNT / "allocations.csv")
    spending = spending[(spending.scenario_id == "complete_preferred_F_per_capita")
                        & (spending.response_class == "household_transfer")]
    cases = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv")
    published = pd.read_csv(BACKCAST / "derived/backcast_categories_annual.csv")
    published_windows = pd.read_csv(BACKCAST / "derived/backcast_categories_windows.csv").set_index(["case", "rule"])
    measured_keys = set(plain.index.get_level_values("key"))
    annual_rows, window_rows, line_rows, part_rows = [], [], [], []
    for name, profile, case_id, normalization in CASES:
        case = cases[(cases.profile == profile) & (cases.case_id == case_id)
                     & (cases.normalization == normalization)].iloc[0]
        allocation = case.allocation
        transfers = spending[spending.allocation == allocation]
        # The credit line's anchor is the national line x pool x the measured 2024 key, so the payment part
        # (pool x population share x relative use) is on the same footing as the account.
        implied = transfers.set_index("category").loc[RTC, "target_bn"] / (paths.rtc[2024] * anchor["pool"])
        if abs(implied - plain.loc[("refundable_credits", allocation, 2024), "share"]) > 1e-9:
            raise SystemExit(f"[BLOCKED] {name}: the credit anchor is not the measured 2024 key")
        control = sum(r.target_bn * paths.index(categories.loc[r.category, "source_cells"]) * paths.share
                      for r in transfers.itertuples())
        pub = published[published["case"] == name]
        gap = (control - pub[pub.rule == "programme"].set_index("year").transfers_bn).abs().max()
        if gap > 6e-5:
            raise SystemExit(f"[BLOCKED] {name}: transfers differ from the published back-cast by {gap:.2e}bn")
        for variant, status, years, only, eip_u, rtc_u in variants(plain, eip, allocation, paths.rtc):
            if variant == "refundable_pandemic":
                amount = transfers.set_index("category").loc[RTC, "target_bn"]
                part_rows += [dict(anchor="sept20", case=name, status=status, **row) for row in
                              credit_parts(paths, amount, allocation, plain, anchor, eip_u, rtc_u)]
            delta = pd.Series(0.0, index=YEARS)
            for r in transfers.itertuples():
                key = r.allocation_key
                if key not in measured_keys or (only is not None and r.category not in only):
                    continue
                old, new = line_paths(paths, r.target_bn, categories.loc[r.category, "source_cells"], key,
                                      allocation, plain, years, anchor, eip_u, rtc_u)
                delta += new - old
                line_rows += [dict(anchor="sept20", case=name, variant=variant, status=status, line=r.category,
                                   key=key, year=year, old_bn=old[year], new_bn=new[year]) for year in years]
            for rule in ("programme", "income"):
                net = pub[pub.rule == rule].set_index("year").net_cost_bn.reindex(YEARS)
                new_net = net + delta
                old_w, new_w = windows(net), windows(new_net)
                if abs(old_w["10y_2015_2024"] - published_windows.loc[(name, rule), "10y_2015_2024"]) > 1e-4:
                    raise SystemExit(f"[BLOCKED] {name}/{rule}: annual rows do not add to the published window")
                annual_rows += [dict(anchor="sept20", case=name, rule=rule, variant=variant, status=status,
                                     year=year, old_net_bn=net[year], delta_bn=delta[year],
                                     new_net_bn=new_net[year]) for year in YEARS]
                window_rows += [dict(anchor="sept20", case=name, rule=rule, variant=variant, status=status,
                                     window=w, old_tn=old_w[w], new_tn=new_w[w], change_tn=new_w[w] - old_w[w],
                                     pandemic_share_old=pandemic_share(net),
                                     pandemic_share_new=pandemic_share(new_net)) for w in WINDOWS]
    return annual_rows, window_rows, line_rows, part_rows


def sept27(paths: Paths, plain: pd.DataFrame, eip: pd.DataFrame, anchor: dict) -> tuple[list, list]:
    """The adopted case's programme version (debt_legacy_2026_09_23: cash lines, own-series receipts). Its
    benefit lines carry the account's corrections; the same measured ratios move them, and the payments part
    of the credit line is the group's measured payment share, independent of the corrected credit key."""
    categories = pd.read_csv(ACCOUNT / "categories.csv").set_index("category")
    keys = pd.read_csv(ACCOUNT / "allocations.csv")
    keys = keys[keys.scenario_id == "complete_preferred_F_per_capita"].drop_duplicates("category") \
        .set_index("category").allocation_key
    lines = pd.read_csv(LEGACY / "derived/federal_split_2024_lines.csv")
    lines = lines[(lines.convention == "central") & (lines.side == "spending") & (lines.financing == "cash")]
    gaps = pd.read_csv(LEGACY / "derived/federal_gap_annual.csv")
    table = pd.read_csv(LEGACY / "derived/adopted_backcast_windows.csv")
    measured_keys = set(plain.index.get_level_values("key"))
    annual_rows, window_rows = [], []
    for end, allocation in ALLOCATION_OF_END.items():
        mine = lines[lines.end == end].set_index("line").gap_bn
        for variant, status, years, only, eip_u, rtc_u in variants(plain, eip, allocation, paths.rtc):
            delta = pd.Series(0.0, index=YEARS)
            for line, amount in mine.items():
                key = keys.get(line)
                if key not in measured_keys or (only is not None and line not in only):
                    continue
                old, new = line_paths(paths, amount, categories.loc[line, "source_cells"], key, allocation,
                                      plain, years, anchor, eip_u, rtc_u)
                delta += new - old
            for rule, legacy_rule in (("programme", "programme"), ("income", "programme_income")):
                net = gaps[(gaps.benchmark == "main") & (gaps.rule == legacy_rule) & (gaps.end == end)
                           & (gaps.convention == "central")].set_index("year").fiscal_gap_real_bn.reindex(YEARS)
                new_net = net + delta
                published = table[(table.benchmark == "main") & (table.end == end) & (table.rule == legacy_rule)
                                  & (table.receipts_method == "own_series")].set_index("window_start")
                for w, start in WINDOWS.items():
                    if abs(net[net.index >= start].sum() / 1e3 - published.loc[start, "fiscal_gap_tn"]) > 1e-5:
                        raise SystemExit(f"[BLOCKED] debt legacy {end}/{rule}: annual gaps do not add to {w}")
                    change = float(delta[delta.index >= start].sum()) / 1e3
                    old_total = float(published.loc[start, "net_cost_tn"])
                    window_rows.append(dict(anchor="sept27", case=f"main_{end}", rule=rule, variant=variant,
                                            status=status, window=w, old_tn=old_total, new_tn=old_total + change,
                                            change_tn=change, pandemic_share_old=pandemic_share(net),
                                            pandemic_share_new=pandemic_share(new_net)))
                annual_rows += [dict(anchor="sept27", case=f"main_{end}", rule=rule, variant=variant, status=status,
                                     year=year, old_net_bn=net[year], delta_bn=delta[year],
                                     new_net_bn=new_net[year]) for year in YEARS]
    return annual_rows, window_rows


def ratio_table(plain: pd.DataFrame) -> pd.DataFrame:
    """Task 3: each key's measured relative use in 2019-2023 against the 2024 value the back-cast applies.
    The ratio's standard error treats the two survey years as independent samples; the CPS rotation overlaps
    adjacent years, so this overstates it."""
    account = pd.read_csv(ACCOUNT / "allocations.csv")
    account = account[(account.scenario_id == "complete_preferred_F_per_capita")
                      & (account.response_class == "household_transfer")]
    rows = []
    for (key, allocation, year), r in plain.iterrows():
        if year == 2024 or key == "population" or (key, allocation, 2024) not in plain.index:
            continue
        base = plain.loc[(key, allocation, 2024)]
        ratio = r.relative_use / base.relative_use
        se = ratio * np.hypot(r.relative_use_se / r.relative_use, base.relative_use_se / base.relative_use)
        keyed = account[(account.allocation == allocation) & (account.allocation_key == key)]
        rows.append(dict(key=key, allocation=allocation, income_year=year, relative_use=r.relative_use,
                         relative_use_se=r.relative_use_se, relative_use_2024=base.relative_use,
                         ratio_to_2024=ratio, ratio_se=se, z=(ratio - 1) / se, beyond_10pct=abs(ratio - 1) > FLAG,
                         account_lines=";".join(sorted(keyed.category)), account_2024_bn=keyed.target_bn.sum()))
    table = pd.DataFrame(rows).sort_values(["key", "allocation", "income_year"])
    # Diagnostic for the 2024 anchor itself: the six measured years averaged with equal weight.
    six = plain.reset_index()
    six = six[six.income_year.between(2019, 2024)].groupby(["key", "allocation"]).relative_use.mean()
    table["pooled_2019_2024_relative_use"] = [six[(k, a)] for k, a in zip(table.key, table.allocation)]
    table["account_2024_change_if_pooled_bn"] = table.account_2024_bn * (
        table.pooled_2019_2024_relative_use / table.relative_use_2024 - 1)
    return table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived",
                        help="reads measure_shares.py's output from here and writes beside it")
    args = parser.parse_args()
    plain, eip = load_measured(args.out_dir)
    pool = pd.read_csv(ACCOUNT / "allocations.csv").household_pool_fraction.unique()
    if len(pool) != 1:
        raise SystemExit("[BLOCKED] more than one household pool fraction")
    anchor = dict(pool=float(pool[0]), pop_share_2024=float(plain.loc[("population", "shared", 2024), "share"]))
    paths = Paths()
    if not all(0 < EIP_NOMINAL[y] < paths.rtc[y] for y in EIP_NOMINAL):
        raise SystemExit("[BLOCKED] BEA's payments do not fit inside NIPA line 25")
    annual, window_rows, line_rows, part_rows = sept20(paths, plain, eip, anchor)
    legacy_annual, legacy_windows = sept27(paths, plain, eip, anchor)
    eip_rows = []
    for a in ("personal", "shared"):
        for s in SSN_STATUS:
            for y, u in eip_use(eip, s, a).items():
                p = plain.loc[("population", a, y), "share"]            # that income year's population share
                share = u * p
                eip_rows.append(dict(allocation=a, status=s, nipa_year=y, eip_nominal_bn=EIP_NOMINAL[y],
                                     relative_use=u, share=share,
                                     per_person_vs_other_residents=share / (1 - share) / (p / (1 - p))))
    for a in ("personal", "shared"):                                   # the 2024 credit ratio the back-cast applies
        u, p = plain.loc[("refundable_credits", a, 2024), "relative_use"], plain.loc[("population", a, 2024), "share"]
        eip_rows.append(dict(allocation=a, status="credit_key_2024", nipa_year=2024, eip_nominal_bn=np.nan,
                             relative_use=u, share=u * p, per_person_vs_other_residents=u * p / (1 - u * p) / (p / (1 - p))))
    outputs = {"backcast_measured_annual.csv": pd.DataFrame(annual + legacy_annual),
               "backcast_measured_windows.csv": pd.DataFrame(window_rows + legacy_windows),
               "line_paths.csv": pd.DataFrame(line_rows),
               "credit_line_parts.csv": pd.DataFrame(part_rows),
               "eip_relative_use.csv": pd.DataFrame(eip_rows),
               "ratio_vs_2024.csv": ratio_table(plain)}
    for name, frame in outputs.items():
        frame.to_csv(args.out_dir / name, index=False, lineterminator="\n", float_format="%.10g")
    table = outputs["backcast_measured_windows.csv"]
    view = table[table.window == "10y_2015_2024"][["anchor", "case", "rule", "variant", "status", "old_tn", "new_tn",
                                                    "pandemic_share_old", "pandemic_share_new"]]
    print(view.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
