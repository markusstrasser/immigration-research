#!/usr/bin/env python3
"""Who wins and who loses from the compliance edge, in the columns the winners-and-losers lane
ingests (../winners_losers_2026_09_24, key templates industry_owner:<NAICS>, industry_worker:<NAICS>).

Dollar rows are the account year 2024 from edges.py (derived/edges_totals.csv, column
account_year_2024), for the four industries whose off-books share is estimated (construction,
landscaping, janitorial and other services to buildings, restaurants). Groups the lane cannot
price carry basis "unpriced" and the reason. Lost payroll taxes are already inside the adopted
account through the September 24 tax correction; the rows that carry them say so and are marked
inside or overlapping, never beside.

Output: derived/winners_losers_rows.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/winners_losers.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from edges import FICA, PRICED  # noqa: E402

DER = HERE / "derived"
COLUMNS = ["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m", "per_person_usd",
           "basis", "relation_to_account", "counterfactual", "source"]
OTHER_RESIDENTS_M = 299.2  # the account's other residents, 2024 stationary comparison
TAX_CORRECTION = ("the September 24 correction 'Tax records: the Census tax model's status and compliance, CPS "
                  "fill-ins, Mexico-born recount, state-aware status flag' (audit rows 2, 13, 4; "
                  "../main_case_2026_09_24)")
INDUSTRIES = "construction (NAICS 23), landscaping (NAICS 561730), janitorial (NAICS 5617) and restaurants (NAICS 722)"
SRC_EDGE = "compliance_gap_2026_09_24/edges.py -> derived/edges_totals.csv, account_year_2024"


def lvl(t: pd.DataFrame, name: str) -> tuple[float, float, float]:
    return tuple(float(t.loc[f"{name}_{k}", "account_year_2024"]) for k in ("low", "central", "high"))


def main() -> None:
    t = pd.read_csv(DER / "edges_totals.csv", index_col=0)
    yr = pd.read_csv(DER / "edges_by_industry_year.csv")
    rates = pd.read_csv(DER / "edges_by_industry.csv").set_index("cell")
    y24 = yr[yr.year == 2024].set_index("cell")
    con = duckdb.connect()
    q = con.execute(f"""SELECT cell, estabs, emp FROM '{HERE}/_cache/panel/qcew_cells.parquet'
        WHERE st = 0 AND year = 2024""").df().set_index("cell")
    covered_jobs_m = float(q.loc[PRICED, "emp"].sum()) / 1e6
    estabs_m = float(q.loc[PRICED, "estabs"].sum()) / 1e6
    taxes, wc, under = lvl(t, "taxes_bn"), lvl(t, "workers_comp_bn"), lvl(t, "underpayment_bn")
    kept, edge = lvl(t, "employee_fica_kept_by_worker_bn"), lvl(t, "edge_bn")
    off, workers = lvl(t, "offbooks_payroll_bn"), lvl(t, "offbooks_workers_m")
    # the budget loses employer and employee Social Security and Medicare and state UI on every
    # off-books dollar, whichever side keeps the employee share
    budget = tuple(float(sum((2 * FICA + rates.loc[c, "ui_contributions_over_wages"]) * y24.loc[c, f"offbooks_payroll_bn_{k}"]
                             for c in PRICED)) for k in ("low", "central", "high"))
    # the low end is the smaller of the slope's low and the level check (edges.py): the national
    # uncovered share calibrated on low-exposure industries, priced at the low edge rates
    lev = {c: float(y24.loc[c, "levelcheck_offbooks_payroll_bn"]) for c in PRICED}
    ui = {c: float(rates.loc[c, "ui_contributions_over_wages"]) for c in PRICED}
    lev_low = {"taxes": sum((FICA + ui[c]) * lev[c] for c in PRICED),
               "wc": sum(max(rates.loc[c, "e1_employer_legal_low"] - FICA - ui[c], 0.0) * lev[c] for c in PRICED),
               "budget": sum((2 * FICA + ui[c]) * lev[c] for c in PRICED)}
    taxes = (min(taxes[0], lev_low["taxes"]), taxes[1], taxes[2])
    wc = (min(wc[0], lev_low["wc"]), wc[1], wc[2])
    budget = (min(budget[0], lev_low["budget"]), budget[1], budget[2])
    kept = (0.0, kept[1], kept[0])  # all captured by the employer at one end, none at the other
    level_note = (f" Low end: the level check (national uncovered share calibrated on low-immigrant industries) "
                  f"puts 2024 off-books pay of the group in these industries at ${sum(lev.values()):.1f}bn, against "
                  f"${off[0]:.1f}-{off[2]:.1f}bn from the cross-state slope")
    pop_w = workers[1]
    rows = []

    def add(group, channel, direction, v, pop, basis, relation, cf, source):
        lo, ce, hi = (sorted(v)[0], v[1], sorted(v)[2]) if v else (None, None, None)
        per = ce * 1e9 / (pop * 1e6) if (v and pop) else None
        rows.append(dict(group=group, channel=channel, direction=direction, bn_low=lo, bn_central=ce, bn_high=hi,
                         population_m=pop, per_person_usd=per, basis=basis, relation_to_account=relation,
                         counterfactual=cf, source=source))

    cf_on = "the same workers paid on the books at the same gross wage;" + level_note
    add(f"noncompliant employers in {INDUSTRIES}",
        "payroll taxes not paid on off-books wages: employer Social Security and Medicare, state unemployment "
        "insurance, and the employee share where the employer keeps it through a lower cash wage", "gain", taxes,
        None, "modelled", "overlaps:tax_corrections_2026_09_24",
        f"{cf_on}. The same dollars are the budget's loss, carried inside the account by {TAX_CORRECTION}; "
        "a transfer from taxpayers to the employer, not a new cost", SRC_EDGE + "; IRS Pub 15 (2024) 6.2% + 1.45%")
    add(f"noncompliant employers in {INDUSTRIES}",
        "workers' compensation premiums (with federal unemployment tax, which ECEC Table 4 does not split out) "
        "not paid", "gain", wc, None, "modelled", "beside",
        f"{cf_on}; ECEC legally required costs per dollar of wages less 7.65% and the industry's QCEW state UI rate",
        SRC_EDGE + "; BLS ECEC Table 4, June 2026")
    add(f"noncompliant employers in {INDUSTRIES}", "wage-and-hour underpayment of their off-books workers", "gain",
        under, None, "modelled", "beside",
        "paid what wage-and-hour law requires; central rate = WHD back wages per employee-year among workers found "
        "underpaid over the industry's average covered pay (1.5-2.5%), high = twice that, low = none",
        SRC_EDGE + "; enforcement.py -> derived/enforcement_by_cell.csv")
    add(f"informal and unauthorized workers paid off the books in {INDUSTRIES} (mostly the group: a within-group "
        "item)", "wage-and-hour underpayment", "loss", under, pop_w, "modelled", "beside",
        "paid what wage-and-hour law requires; the mirror of the employers' underpayment row",
        SRC_EDGE + "; population = off-books workers, central")
    add(f"informal and unauthorized workers paid off the books in {INDUSTRIES} (within-group item)",
        "employee Social Security and Medicare not withheld and kept in cash", "gain", kept, pop_w, "modelled",
        "overlaps:tax_corrections_2026_09_24",
        "withheld on the books; the row's low end pairs with the employers' tax row's high end (the employer keeps "
        f"all of it through a lower cash wage). Inside the account through {TAX_CORRECTION}", SRC_EDGE)
    add(f"informal and unauthorized workers paid off the books in {INDUSTRIES} (within-group item)",
        "no workers' compensation coverage: injury costs fall on the worker, charity care or public programs",
        "loss", wc, pop_w, "assumed", "overlaps:uncompensated_care",
        "covered by workers' compensation; valued at the premium the employer avoids, an upper bound on the "
        "expected benefits lost because premiums include insurers' costs; the public part of injury care is "
        "inside the account's uncompensated-care line", SRC_EDGE)
    add("the budget: Social Security and Medicare trust funds and state unemployment-insurance funds",
        "payroll taxes not collected on off-books wages (employer and employee Social Security and Medicare, "
        "state UI; income tax not included here)", "loss", budget, OTHER_RESIDENTS_M, "modelled", "inside",
        f"collected on the books. Carried inside the adopted account by {TAX_CORRECTION}; not added again. "
        "Per person over the account's 299.2m other residents." + level_note,
        SRC_EDGE + "; (2 x 7.65% + state UI rate) x off-books pay")
    add(f"customers of {INDUSTRIES}", "lower prices where noncompliant firms' cost edge is competed away", "gain",
        (0.0, 0.5 * edge[1], edge[2]), OTHER_RESIDENTS_M, "assumed", "overlaps:production_term",
        "the edge kept by noncompliant employers. Pass-through is unmeasured: none (the edge stays with the "
        "employer), half of the central edge (assumed midpoint) and all of the high edge. A share of the "
        "employers' rows, never additional to them; overlaps the production term and the consumer-price lane",
        SRC_EDGE)
    add(f"compliant owners in {INDUSTRIES}", "jobs or margin lost to noncompliant rivals", "loss", None, None,
        "unpriced", "beside",
        f"no measured loss. {estabs_m:.2f}m covered establishments in 2024. Covered establishment and employment "
        "growth show no negative association with growth in the group's share (state-year and industry-year "
        "fixed effects, 2012-2023); the specialty-trade association with year effects only disappears net of the "
        "state's low-exposure industries; the pre-registered E-Verify test fails its pre-trend check; the one "
        "firm-level study (Georgia 1995-2005) finds rivals' undocumented hiring insignificant in construction, "
        "agriculture and hospitality", "compliance_gap_2026_09_24/panel_c.py, everify.py; reads/LIT_FIRMS_EVERIFY.md S1")
    pc = pd.read_csv(DER / "panel_c.csv")
    ld = pc[(pc.design == "long difference 2012-13 to 2022-23") & (pc["sample"] == "focus cells")
            & (pc.y == "dy_wkwage") & (pc.x == "dm_unauth")].iloc[0]
    cc = pd.read_csv(DER / "composition_check.csv").set_index("cell")
    add(f"workers of compliant firms in {INDUSTRIES}", "wages", "loss", None, covered_jobs_m, "unpriced",
        "overlaps:wage_split",
        "no robust association: covered average wages fall with the group's share within states across industries "
        f"(long difference {ld.coef:+.2f} per unit share, SE {ld.se:.2f}) but not across states within an industry "
        f"(construction {cc.loc['c23', 'ld_coef']:+.2f}, SE {cc.loc['c23', 'ld_se']:.2f}; restaurants "
        f"{cc.loc['c722z', 'ld_coef']:+.2f}, SE {cc.loc['c722z', 'ld_se']:.2f}); the account's wage split already "
        "prices the group's effect on other residents' wages. Population = covered jobs 2024",
        "compliance_gap_2026_09_24/panel_c.py, composition.py")
    add("noncompliant employers in agriculture (NAICS 111, 112, 115) and private households (NAICS 814)",
        "the same edge: payroll taxes, workers' compensation, underpayment", "gain", None, None, "unpriced", "beside",
        "the off-books share is not identified: the uncovered-share slope is negative across states in crop "
        "production (state UI coverage of farms differs), not distinguishable from zero in animal production and "
        "private households (22 states), and farm labour contractors are coded to crop production in the ACS",
        "compliance_gap_2026_09_24/uncovered.py -> derived/uncovered_slopes.csv")
    out = pd.DataFrame(rows, columns=COLUMNS)
    out.to_csv(DER / "winners_losers_rows.csv", index=False, lineterminator="\n", float_format="%.4f")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 60)
    print(out[["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m", "per_person_usd",
               "basis", "relation_to_account"]].to_string(index=False, float_format="%.3f"))
    print(f"off-books payroll 2024 $bn {off}; off-books workers m {workers}; edge $bn {edge}")
    print(f"covered jobs 2024 in the four industries {covered_jobs_m:.3f}m; establishments {estabs_m:.3f}m")


if __name__ == "__main__":
    main()
