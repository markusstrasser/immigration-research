#!/usr/bin/env python3
"""Debt legacy of past federal gaps for the Mexican-origin union and its comparators, like for like (sept29 case).

The debt legacy lane (`debt_legacy_2026_09_23/debt_legacy.py`, imported read-only, never edited) carries the union's
2024 per-programme position back to 2005 with the programme rule (each line on its own national BEA series and each
year's measured federal share; receipts on their own government's series and scaled by the group's measured relative
income; the 2020-2022 refundable-credit excess per head) and compounds the federal part at OMB effective rates. This
script runs the same machinery, the same function (`programme_federal`), for each comparator:

  - the 2024 line amounts are the group's own (group_lines.py -> derived/group_lines_sept29.csv, the white lane's
    sept29 re-key on audit row 4's frame); the responses, federal shares, national series and rates are the case's;
  - replacement framing: every group follows the union's measured headcount path (the back-cast's group series), so
    only the per-capita position differs;
  - relative income: the union keeps the back-cast's measured ACS series; third-plus NH whites take the ACS S0201
    NH-white-alone series (acs_inputs.py); the all-residents slice is 1 by definition. Before 2008 every group is held
    at its 2008 value, as the back-cast holds the union;
  - union-only terms stay with the union: the use-keyed justice and uncompensated-care increments (their federal
    parts jf, ucf), the lane constants, school reprice, college re-key and the induced receipts F of the production
    model. The comparators carry their justice and Medicaid lines at the lines' average federal shares and no F.

The lines_at seam: programme_federal reads a corner's lines through `lines_at(corner)`. A corner here may carry
`_table`, the group's line table (the case's lines and responses with the group's amounts); a patched lines_at returns
it and otherwise calls the lane's own function. Nothing else in the lane is replaced.

Bases. Cash: the cash set compounded (benefits when paid; the lane's headline). Accrual: the set compounded, Social
Security and Part A charged on the accrual the group's 2024 payroll taxes earn (the adopted case's basis), carried back
with the lines' own series -- the lane's benchmark main_with_accrual, applied to every group.

Windows. 2005 (the lane's), 2000 and 1990. The pre-2005 pass extends the lane's YEARS to 1990: NIPA Sections 1, 3, 7
reach 1929; OMB Tables 3.1, 7.1 and 12.3 reach 1940; NHEA Table 3's Medicaid federal share has 1990 and 2000-2024 and
is interpolated linearly in 1991-1999. The union's headcount before 2005 is the 1990 (CP-3-3) and 2000 (SF1) census
counts at the back-cast's account scaling, linear between census points and the 2005 ACS. Gates: the extended pass
reproduces the standard pass for 2005-2024 (1e-9) and has no missing value.

Parity gate (stops the run): the engine union through this code path reproduces the lane's derived/sept29 stocks.csv
(2024 interest 30.75 / 41.48bn cash, main_with_accrual on accrual) and federal_gap_annual.csv to 1e-6.
Outputs in derived/: legacy_main.csv, legacy_differences.csv, legacy_conventions.csv, federal_gap_by_group.csv,
paths.csv, gates.json. Run from the repository root after group_lines.py and acs_inputs.py:
  OPENBLAS_NUM_THREADS=1 uv run python3 infra/immigration-fiscal/legacy_comparators_2026_09_30/legacy.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
LANE = FISCAL / "debt_legacy_2026_09_23"
CASE = "sept29"
GROUPS = ("mexican_origin_engine", "mexican_origin_rough", "A1_third_plus_nh_white", "all_residents_slice")
UNION = ("mexican_origin_engine", "mexican_origin_rough")
BASES = ("cash", "accrual")
ENDS = ("low", "high")
WINDOWS = (2005, 2000, 1990)
EXT_FIRST = 1990
TOL = 1e-6


def load_lane():
    spec = importlib.util.spec_from_file_location("debt_legacy", LANE / "debt_legacy.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["debt_legacy"] = module
    spec.loader.exec_module(module)
    return module


D = load_lane()
_LINES_AT = D.lines_at
_NHEA = D.nhea_medicaid_federal_share


def lines_at(corner: dict) -> pd.DataFrame:
    return corner["_table"].copy() if "_table" in corner else _LINES_AT(corner)


def nhea_interpolated() -> pd.Series:
    """NHEA Table 3 has 1990 and 2000-2024; the years between are linear (extended pass only)."""
    s = _NHEA()
    return s.interpolate(limit_area="inside") if s.isna().any() else s


D.lines_at = lines_at


def setup() -> dict:
    """The lane's main() through section 1 for the case: shares, the History, the corners and the constant parts."""
    wb = D.Workbook(D.BEA / "Section3All_xls.xlsx")
    D.check_pins()
    responses = D.case_payload(CASE)["meta"]["responses"]
    shares, extras = D.federal_shares(wb, D.Grants(), *D.finite_components(responses))
    D.case_shares(shares, wb)                   # main() does both for a case with profiles; case_shares adds columns
    D.subfunction_levels(responses, extras)
    cash_payload = D.case_payload(CASE, "cash")
    run_shares, _ = D.v4_shares(shares, extras, wb, D.apply_corrections(D.MODEL, cash_payload), cash_payload["meta"])
    jf = D.justice_federal(wb)
    ucf = D.uncompensated_federal(float(shares["central"].loc[D.LAST, "medicaid_and_chip_other_medical"]))
    hist = D.History(wb)
    D.COMPONENTS.clear()
    first = D.case_payload(next(iter(D.LATER_CASES)))
    D.COMPONENTS.update(D.sept26_components(json.loads(D.CORRECTIONS_FILE.read_text()), first))
    D.COMPONENTS["edits"] = D.COMPONENTS["edits"] + [
        dict(component="enterprise_rekey", **e) for e in D.rekey_edits(D.case_payload(D.previous_case(CASE)), first)]
    run = D.case_split(CASE, run_shares, extras, jf, ucf)
    prof = run["main_profile"]
    return dict(wb=wb, shares=run_shares, extras=extras, jf=jf, ucf=ucf, hist=hist, run=run, prof=prof,
                corners={"cash": run["anchors"][prof], "accrual": run["set_anchors"][prof]})


def group_table(base: pd.DataFrame, lines: pd.DataFrame, group: str, where: str) -> pd.DataFrame:
    """The case's lines at a corner with the group's 2024 amounts. Gates: the same line set wherever either side has a
    responsive amount; the dump's responses are the corner's (1e-9); the engine union's amounts are the corner's."""
    g = lines[lines.side != "scalar"].set_index(["side", "line"])
    t = base.copy()
    key = list(zip(t.side, t.id))
    extra = set(g.index) - set(key)
    if any(abs(g.amount_bn[k] * g.response[k]) > 1e-9 for k in extra):
        raise SystemExit(f"[BLOCKED] {where}: group lines absent from the corner: {sorted(extra)}")
    amount = np.array([g.amount_bn.get(k, 0.0) for k in key])
    missing = [k for k, r in zip(key, t.responsive_bn) if k not in g.index and abs(r) > 1e-9]
    if missing:
        raise SystemExit(f"[BLOCKED] {where}: responsive corner lines without a group amount: {missing}")
    resp = np.array([g.response.get(k, np.nan) for k in key])
    have = ~np.isnan(resp)
    if np.abs(resp[have] - t.response.to_numpy()[have]).max() > 1e-9:
        raise SystemExit(f"[BLOCKED] {where}: the dump's responses are not the corner's")
    if group == "mexican_origin_engine":
        worst = float(np.abs(amount[have] - t.amount_bn.to_numpy()[have]).max())
        if worst > 1e-6:
            raise SystemExit(f"[BLOCKED] {where}: the engine union's dump amounts differ from the corner by {worst}")
    t["amount_bn"] = amount
    t["responsive_bn"] = t.amount_bn * t.response
    return t


def income_paths(hist, acs: pd.DataFrame) -> dict[str, pd.Series]:
    """Receipts scale by relative income / its 2024 value. The union: the back-cast's series (History.income; before
    2008 at 2008). NH whites: ACS S0201 POPGROUP 451 over 001, interpolated where the profile has no year (2010,
    2020, as the back-cast), 2008 held back. All residents: 1."""
    years = hist.income.index
    w = acs[acs.series == "relative_per_capita_income_nh_white"].set_index("year").value.astype(float)
    w = w.reindex(range(min(years), max(years) + 1)).interpolate(limit_area="inside").bfill().reindex(years)
    one = pd.Series(1.0, index=years)
    return {"mexican_origin_engine": hist.income, "mexican_origin_rough": hist.income,
            "A1_third_plus_nh_white": w / w[D.LAST], "all_residents_slice": one}


def federal_path(ctx: dict, group: str, basis: str, end: str, conv: str, lines: pd.DataFrame, income: pd.Series):
    """The central rule's federal part and fiscal gap by year (real 2024 $bn): programme_income_pandemic_per_head."""
    corner = ctx["corners"][basis][end]
    union = group in UNION
    table = group_table(_LINES_AT(corner), lines, group, f"{group} {basis} {end}")
    c = dict(corner, _table=table)
    jf, ucf = ctx["jf"], ctx["ucf"]
    parts = ctx["run"]["parts"].get((ctx["prof"], end, conv))
    if not union:
        c.update(justice=0.0, uc=0.0)
        jf = {k: 0.0 for k in jf}
        ucf = {arm: {k: 0.0 for k in v} for arm, v in ucf.items()}
        parts = None
        for lid in ("lane_constants", "school_reprice", "college_rekey"):
            if (table.id == lid).any() and abs(float(table.responsive_bn[table.id == lid].sum())) > 1e-12:
                raise SystemExit(f"[BLOCKED] {group}: union-only line {lid} is not zero")
    prog = D.programme_federal(ctx["hist"], c, end, conv, ctx["shares"], ctx["extras"], jf, ucf, parts,
                               series=D.RECEIPT_SERIES_V4, signed_receipts=D.SIGNED_RECEIPTS_V4)
    induced, induced_fed = (prog.induced, prog.induced_fed) if union else (0.0, 0.0)
    fed = prog.spending_fed - prog.receipts_fed * income - prog.population_fed - induced_fed - prog.rtc_excess_fed
    gap = prog.spending - prog.receipts * income - prog.population - induced - prog.rtc_excess
    return fed, gap


def payroll_carry(hist, lines_all: pd.DataFrame, group: str, end: str, income: pd.Series) -> pd.Series:
    """Sensitivity for the accrual basis (real 2024 $bn by year, all federal): the lane's main_with_accrual carries
    the Social Security accrual with the benefit series (NIPA 3.12 line 5) and the Part A accrual inside Medicare's
    (line 6). Accrual is earned on payroll taxes, so the alternative carries both with the group's own payroll-tax
    path: the OASDI (NIPA 3.6 lines 24 + 5) and HI (25 + 6) series times the receipt rule's relative-income scale.
    Returns the change in the federal part; the programme rule is linear in each line, so this adds to it."""
    pick = lambda basis, lid: float(lines_all[(lines_all.group == group) & (lines_all.basis == basis)  # noqa: E731
                                              & (lines_all.end == end) & (lines_all.side == "spending")
                                              & (lines_all.line == lid)].amount_bn.iloc[0])
    part_a_share = D.case_payload(CASE)["meta"]["pension_accrual"]["part_a_share"]
    ss = pick("accrual", "social_security")
    part_a = pick("accrual", "medicare") - (1 - part_a_share) * pick("cash", "medicare")
    idx_ss, idx_mc = hist.index("T31200-A:5"), hist.index("T31200-A:6")
    idx_oasdi, idx_hi = hist.index("T30600-A:24;T30600-A:5"), hist.index("T30600-A:25;T30600-A:6")
    return hist.share * (ss * (idx_oasdi * income - idx_ss) + part_a * (idx_hi * income - idx_mc))


def extend(ctx_years: list[int]):
    D.YEARS = ctx_years
    D.FIRST = ctx_years[0]
    D.nhea_medicaid_federal_share = nhea_interpolated if ctx_years[0] < 2005 else _NHEA


def extended_history(hist, std_hist, acs: pd.DataFrame) -> dict:
    """The union's headcount 1990-2024: census 1990 and 2000 and the back-cast's series from 2005, all at the
    back-cast's account scaling (group = ACS count x group_2024 / count_2024); linear between points."""
    inputs = pd.read_csv(D.BACKCAST / "inputs/acs_mexican_origin.csv").set_index("year")
    factor = std_hist.group[2005] / inputs.acs_mexican_origin[2005]
    factor24 = std_hist.group[D.LAST] / inputs.acs_mexican_origin[D.LAST]
    if abs(factor - factor24) > 1e-9:
        raise SystemExit("[BLOCKED] the back-cast's scaling is not one factor")
    census = acs[acs.series == "mexican_origin_count"].set_index("year").value.astype(float)
    group = pd.Series(np.nan, index=D.YEARS)
    group[1990], group[2000] = census[1990] * factor, census[2000] * factor     # factor: millions per person
    group.loc[2005:] = std_hist.group.to_numpy()
    group = group.interpolate()
    share = group / (hist.people.reindex(D.YEARS) / 1e3)
    hist.group, hist.share = group, share / share[D.LAST]
    hist.income = std_hist.income.reindex(D.YEARS).bfill()
    return dict(scale_factor=float(factor), census_1990_m=float(census[1990] / 1e6),
                census_2000_m=float(census[2000] / 1e6))


def effective_rates(standard: pd.Series) -> pd.Series:
    """OMB net interest over average debt held by the public, fiscal years 1991-2025 (rate_paths' formula; gate: equal
    to the lane's effective path for 2005-2025)."""
    interest, debt = D.omb_net_interest(), D.omb_debt_held_by_public()
    fy = list(range(EXT_FIRST + 1, 2026))
    r = pd.Series({s: interest[s] / ((debt[s - 1] + debt[s]) / 2) for s in fy})
    if (r.reindex(standard.index) - standard).abs().max() > 1e-15:
        raise SystemExit("[BLOCKED] the extended effective rates differ from the lane's")
    return r


def zero_audit(wb, carried: set[str]) -> dict:
    """Series the programme rule reads that are zero in some pre-2005 year while nonzero in 2005: the lane's
    Workbook fills missing cells with 0, so each such year is listed for inspection."""
    cats = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    lines = {D.SYNTHETIC_CARRY.get(i, i) for i in carried}
    refs = {f"spending:{i}": cats.loc[i, "source_cells"] for i in cats.index if i in lines}
    for i, (f, s) in D.RECEIPT_SERIES_V4.items():
        if i not in carried:
            continue
        for lvl, cells in (("fed", f), ("sl", s)):
            if cells:
                refs[f"receipt:{i}:{lvl}"] = cells
    out = []
    for name, ref in sorted(refs.items()):
        v = wb.cells(ref)
        zeros = [int(y) for y in v.index if y < 2005 and v[y] == 0 and v[2005] != 0]
        if zeros:
            out.append(dict(series=name, cells=ref, zero_years=zeros))
    return dict(series_audited=len(refs), zero_before_2005=out)


def main() -> None:
    lines_all = pd.read_csv(HERE / "derived/group_lines_sept29.csv")
    acs = pd.read_csv(HERE / "derived/acs_inputs.csv")
    count_m = D.member_count()
    gates: dict = {}

    # 1. Standard pass (the lane's years), with the parity gate.
    std = setup()
    rates = D.rate_paths()
    lane_stocks = pd.read_csv(LANE / "derived/sept29/stocks.csv")
    lane_annual = pd.read_csv(LANE / "derived/sept29/federal_gap_annual.csv")
    inc_std = income_paths(std["hist"], acs)
    paths = {}
    for group in GROUPS:
        for basis in BASES:
            for end in ENDS:
                sel = lines_all[(lines_all.group == group) & (lines_all.basis == basis) & (lines_all.end == end)]
                for conv in D.CONVENTIONS:
                    paths[("std", group, basis, end, conv)] = federal_path(std, group, basis, end, conv, sel,
                                                                           inc_std[group])
    parity = []
    for basis, bench in (("cash", "main"), ("accrual", "main_with_accrual")):
        for end in ENDS:
            for conv in D.CONVENTIONS:
                fed, _ = paths[("std", "mexican_origin_engine", basis, end, conv)]
                want = lane_annual[(lane_annual.benchmark == bench) & (lane_annual.rule == D.CENTRAL["rule"])
                                   & (lane_annual.end == end) & (lane_annual.convention == conv)].set_index("year")
                d_ann = float((fed - want.federal_real_bn.reindex(D.YEARS)).abs().max())
                st = D.stock(D.History.nominal(std["hist"], fed), rates["effective"], 2005, 1.0)
                row = lane_stocks[(lane_stocks.benchmark == bench) & (lane_stocks.rule == D.CENTRAL["rule"])
                                  & (lane_stocks.end == end) & (lane_stocks.convention == conv)
                                  & (lane_stocks.rate_path == "effective") & (lane_stocks.window_start == 2005)
                                  & (lane_stocks.financing == "all_borrowed")].iloc[0]
                d_int = abs(st["legacy_interest_2024_bn"] - row.legacy_interest_2024_bn)
                d_stock = abs(st["stock_entering_2024_bn"] - row.stock_entering_2024_bn)
                parity.append(dict(basis=basis, benchmark=bench, end=end, convention=conv,
                                   interest_bn=st["legacy_interest_2024_bn"], lane_interest_bn=row.legacy_interest_2024_bn,
                                   stock_bn=st["stock_entering_2024_bn"], lane_stock_bn=row.stock_entering_2024_bn,
                                   max_abs_diff=max(d_ann, d_int, d_stock)))
                print(f"  parity {basis:7s} {end:4s} {conv:7s} interest {st['legacy_interest_2024_bn']:.6f} "
                      f"(lane {row.legacy_interest_2024_bn:.6f}) stock {st['stock_entering_2024_bn']:.4f}; "
                      f"max |diff| {max(d_ann, d_int, d_stock):.2e}")
    worst = max(p["max_abs_diff"] for p in parity)
    gates["parity"] = dict(rows=parity, max_abs_diff=worst, tolerance=TOL)
    if worst > TOL:
        raise SystemExit(f"[BLOCKED] parity: the engine union through this path differs from the lane by {worst:.3e}bn")
    print(f"  ✓ parity gate: {len(parity)} specifications within {worst:.2e}bn (tolerance {TOL})")

    # 2. Extended pass: 1990-2024.
    extend(list(range(EXT_FIRST, D.LAST + 1)))
    try:
        ext = setup()
        gates["pre2005_population"] = extended_history(ext["hist"], std["hist"], acs)
        inc_ext = income_paths(ext["hist"], acs)
        for group in GROUPS:
            for basis in BASES:
                for end in ENDS:
                    sel = lines_all[(lines_all.group == group) & (lines_all.basis == basis) & (lines_all.end == end)]
                    for conv in D.CONVENTIONS:
                        fed, gap = federal_path(ext, group, basis, end, conv, sel, inc_ext[group])
                        if fed.isna().any() or gap.isna().any():
                            raise SystemExit(f"[BLOCKED] extended pass: missing values {group} {basis} {end} {conv}")
                        s_fed, s_gap = paths[("std", group, basis, end, conv)]
                        d = max(float((fed.loc[2005:] - s_fed).abs().max()), float((gap.loc[2005:] - s_gap).abs().max()))
                        if d > 1e-9:
                            raise SystemExit(f"[BLOCKED] the extended pass moves 2005-2024 by {d} ({group} {basis} {end} {conv})")
                        paths[("ext", group, basis, end, conv)] = (fed, gap)
                        if basis == "accrual" and conv == "central":
                            adj = payroll_carry(ext["hist"], lines_all, group, end, inc_ext[group])
                            if abs(adj[D.LAST]) > 1e-9:
                                raise SystemExit("[BLOCKED] the payroll carry moves 2024")
                            paths[("ext", group, "accrual_payroll_carry", end, conv)] = (fed + adj, gap + adj)
        cats = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
        if (cats.loc["social_security", "source_cells"], cats.loc["medicare", "source_cells"]) != ("T31200-A:5", "T31200-A:6"):
            raise SystemExit("[BLOCKED] the lane's Social Security or Medicare series is not the one payroll_carry replaces")
        gates["extended_equals_standard_2005_2024"] = "all groups, bases, ends and conventions within 1e-9"
        live = lines_all[(lines_all.side != "scalar")]
        live = live[(live.amount_bn * live.response).abs() > 1e-12]
        gates["pre2005_zero_cells"] = zero_audit(ext["wb"], set(live.line))
        hist = ext["hist"]
        real = hist.real.copy()
        ext_nhea = D.nhea_medicaid_federal_share()
    finally:
        extend(list(range(2005, D.LAST + 1)))
    r_ext = effective_rates(rates["effective"])
    nominal = lambda s: s / real  # noqa: E731  (History.nominal on the extended deflator)

    # 3. Stocks, interest, per member.
    rows, annual = [], []
    for (tag, group, basis, end, conv), (fed, gap) in sorted(paths.items()):
        if tag != "ext":
            continue
        nom = nominal(fed)
        for year in fed.index:
            if conv == "central":
                annual.append(dict(group=group, basis=basis, end=end, year=int(year), fiscal_gap_real_bn=gap[year],
                                   federal_real_bn=fed[year], federal_nominal_bn=nom[year]))
        for start in WINDOWS:
            st = D.stock(nom, r_ext, start, 1.0)
            rows.append(dict(group=group, basis=basis, window_start=start, end=end, convention=conv,
                             stock_entering_2024_bn=st["stock_entering_2024_bn"],
                             interest_2024_bn=st["legacy_interest_2024_bn"],
                             interest_per_member_usd=st["legacy_interest_2024_bn"] * 1e9 / (count_m * 1e6),
                             stock_per_member_usd=st["stock_entering_2024_bn"] * 1e9 / (count_m * 1e6),
                             federal_flow_2024_bn=st["flow_2024_bn"],
                             sum_flows_nominal_bn=st["sum_flows_nominal_bn"], rate_2024=st["rate_2024"]))
    stocks = pd.DataFrame(rows)
    # Gate: the extended 2005 window is the standard pass's (the parity rows) for the engine union.
    for p in parity:
        got = stocks[(stocks.group == "mexican_origin_engine") & (stocks.basis == p["basis"]) & (stocks.end == p["end"])
                     & (stocks.convention == p["convention"]) & (stocks.window_start == 2005)].interest_2024_bn.iloc[0]
        if abs(got - p["lane_interest_bn"]) > TOL:
            raise SystemExit("[BLOCKED] the extended run's 2005 window is not the lane's")
    main_t = stocks[stocks.convention == "central"].drop(columns="convention")
    conv_t = stocks[(stocks.window_start == 2005) & stocks.basis.isin(BASES)]
    diffs = []
    for basis in (*BASES, "accrual_payroll_carry"):
        for start in WINDOWS:
            for end in ENDS:
                pick = main_t[(main_t.basis == basis) & (main_t.window_start == start) & (main_t.end == end)].set_index("group")
                for ref in UNION:
                    for comp in ("A1_third_plus_nh_white", "all_residents_slice"):
                        a, b = pick.loc[ref], pick.loc[comp]
                        diffs.append(dict(basis=basis, window_start=start, end=end, union=ref, comparator=comp,
                                          stock_diff_bn=a.stock_entering_2024_bn - b.stock_entering_2024_bn,
                                          interest_diff_bn=a.interest_2024_bn - b.interest_2024_bn,
                                          interest_diff_per_member_usd=a.interest_per_member_usd - b.interest_per_member_usd))
    # Sign and scale gates: the average slice's 2024 federal flow lies between the union's and the white slice's on
    # cash at both ends (a ranking the 2024 account already shows), and no stock exceeds debt held by the public.
    debt_2023 = float(rates.loc[2023, "debt_held_by_public_bn"])
    if stocks.stock_entering_2024_bn.abs().max() > debt_2023:
        raise SystemExit("[BLOCKED] a stock exceeds debt held by the public")
    gates["member_count_m"] = count_m
    gates["debt_held_by_public_end_fy2023_bn"] = debt_2023
    paths_t = pd.DataFrame(dict(year=hist.group.index, union_headcount_m=hist.group.to_numpy(),
                                population_share_rel_2024=hist.share.to_numpy(),
                                **{f"income_scale_{g}": inc_ext[g].to_numpy() for g in ("mexican_origin_engine",
                                                                                      "A1_third_plus_nh_white",
                                                                                      "all_residents_slice")},
                                medicaid_federal_share=ext_nhea.to_numpy(),
                                effective_rate_fy=r_ext.reindex(hist.group.index).to_numpy()))
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    main_t.round(6).to_csv(out / "legacy_main.csv", index=False, lineterminator="\n")
    pd.DataFrame(diffs).round(6).to_csv(out / "legacy_differences.csv", index=False, lineterminator="\n")
    conv_t.round(6).to_csv(out / "legacy_conventions.csv", index=False, lineterminator="\n")
    pd.DataFrame(annual).round(6).to_csv(out / "federal_gap_by_group.csv", index=False, lineterminator="\n")
    paths_t.round(6).to_csv(out / "paths.csv", index=False, lineterminator="\n")

    def plain(v):
        if isinstance(v, dict):
            return {k: plain(x) for k, x in v.items()}
        if isinstance(v, list):
            return [plain(x) for x in v]
        if isinstance(v, (float, np.floating)):
            return round(float(v), 9)
        if isinstance(v, np.integer):
            return int(v)
        return v
    (out / "gates.json").write_text(json.dumps(plain(gates), indent=1, sort_keys=True) + "\n")
    show = main_t.copy()
    print(show.pivot_table(index=["basis", "window_start", "group"], columns="end",
                           values=["stock_entering_2024_bn", "interest_2024_bn", "interest_per_member_usd"]).round(2)
          .to_string())
    print("[written] derived/legacy_main.csv, legacy_differences.csv, legacy_conventions.csv, federal_gap_by_group.csv, "
          "paths.csv, gates.json")


if __name__ == "__main__":
    main()
