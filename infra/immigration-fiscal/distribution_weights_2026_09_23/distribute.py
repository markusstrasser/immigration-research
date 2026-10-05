"""Who among other residents gains and loses from the Mexican-origin union's presence, by income,
and the income-weighted net.

Frame (brief, not changed): the complete annual account's stationary 2024 comparison with and
without the 40.896574m CPS Mexican-origin residents, effects on all other US residents, a dollar
counted as a dollar. Each channel's total is taken as given from its lane and divided among other
residents; no total is re-estimated.

Income frame: CPS ASEC 2025 (income year 2024), the account's sha-gated archive and canonical
target. Every other resident gets an equivalized income y_i and a person-weighted percentile:
SPM resources / SPM equivalence scale (central) or household money income / sqrt(size) (check).
Persons living with target members keep their own place; only non-target persons count.

Resolution: channels measured on the CPS are carried per person. Channels whose input is another
survey (ACS rents and capital income, SCF rental holdings) are placed in 1,000 percentile cells
of that survey's own other-resident ranking and spread over the CPS persons in the same cell.
Binned inputs (NCVS income brackets, CBO and ITEP tax groups, CEX quintiles) are spread within
each bin by the microdata's distribution of the channel's base. Quintiles, deciles and the
percentile table (derived/channel_by_percentile.csv, central channels only) are for display only.

Weights: (max(y_i, y_floor) / ybar)^(-eta), eta in {0, 1, 1.3, 1.4, 2}, ybar the unfloored
person-weighted mean over other residents, y_floor the 5th percentile (1st and 10th as
sensitivities). The quintile-bin version sum_q (ybar_q / ybar)^(-eta) Delta_q is reported beside
it, with unfloored and floored bin means, and each weighted sum is also given relative to the
median and as an equal-split equivalent (divided by the mean weight). Signs are from other
residents' point of view: a cost is negative.

Cases: the fiscal channel is the adopted main case's direct response A plus the central induced
receipts F. --case sept24 moves A at each band end by the change from the September 23 to the
September 24 case (main_case_2026_09_24/derived/main_case_bands.csv); the package edits receipts
and keyed spending only, so P and F do not move. Each later case (LATER_CASES, one entry per case)
moves A again by its change at each band end (the lane's summary.json "change"): --case sept26 (CBO's
one-year school response, 0.63-0.66) by the consumption key and the finite-removal responses, then
--case sept26_schools (the default since the second decision of 2026-09-26) by schools at full
average cost. These edit receipts and the responses of general government and schools, never P or F,
and each case keeps the allocation at each band end (shared low, personal high), so again only A
moves. --case sept23, sept24 or sept26 with --out-dir <dir> reproduces the files committed before
each switch byte for byte. Every channel outside the budget is the same in every case.

--case sept27 (the default since 2026-09-27) moves A again, by the long-run road and park responses, rental
assistance, the government enterprises and the return on public capital. Two parts of its A are split out at
each band end (node case_ends.cjs writes derived/case_ends_sept27.json; run it first):
  - the return on public capital, an imputed resource cost of the budgets that hold the capital. It stays in the
    fiscal channel under both conventions and is also reported alone (fiscal_resource_*, beside fiscal_cash_*);
  - the capped programs, rental assistance and LIHEAP. Without the group their slots go to eligible households,
    so their amount falls on eligible non-recipients (displaced_beneficiaries), not on the budget, under both
    conventions. TANF-type aid is a block grant that states can move to other uses, so it stays with the budget.
The range variants of the fiscal channel carry the displaced beneficiaries at the same band end.

--case sept29 (candidate v4, adopted 2026-09-29; SEPT29_LANE) writes derived/sept29/ and leaves the September 27
files, the default, as they are (node case_ends.cjs --case sept29 first). Its payload also puts the engine's production
term on the account's row-4 weights, which moves P and F, never A. So A moves by the case's change less the engine's
change in P + F at each band end (case_ends_sept29.json production; gated against the engine's own A), and the lane's
production scenarios are re-solved on row-4 weights (row4_nest_rows, gated against the case's grid): their P goes to
the wage channel and their F to the fiscal channel. The published September 20 band keeps the published production.
Two more splits follow the debt lane's financing columns: public housing's enterprise deficit (a receipt line at the
rental line's key) is capped like rental assistance, on rental assistance's eligible non-recipients (CAPPED_KEY_OF);
and the pension accrual (the case less its cash set, $76.7/73.0bn at the band ends) stays in the fiscal channel but
leaves its cash part: fiscal_accrual_* reports it, so fiscal = cash + resource + accrual.

--case oct05 (main case v5, adopted 2026-10-05; OCT05_LANE) writes derived/oct05/ (node case_ends.cjs --case oct05
first). v5 adds 3.04M people, descendants who no longer report Mexican origin, priced at G3+ members' and third-plus
whites' amounts; its production grid is September 29's plus the added G3+ members' P and F (whites carry none). So A
moves by the change from September 29 less that production delta at each band end (case_ends_oct05.json production
`previous`, the September 29 grid at the same cell). The lane's production scenarios are solved on row-4 weights as for
September 29 (gated against September 29's grid) and then take the lineage's delta (lineage_rows): within each scenario
the wage changes by skill cell and the capital columns are scaled so that P and F reach the v5 grid at the scenario's
cell [ASSUMPTION: the added members' effects fall on other residents' cells as the union's do].
The added people cannot be found in the CPS frame: they do not report Mexican origin, so they sit there among the
other residents, as natives, and this lane leaves them there [ASSUMPTION: about 3.04M of the frame's other residents,
about 1%, are the added people].

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py [--case sept24 --out-dir DIR]
The first run reads the ACS PUMS ZIPs in chunks (about two minutes) and caches the needed
columns in _cache/; later runs take seconds.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
CACHE = HERE / "_cache"
SOURCES = CACHE / "sources"

ETAS = (0.0, 1.0, 1.3, 1.4, 2.0)
FLOORS = {"p1": 0.01, "p2": 0.02, "p3": 0.03, "p5": 0.05, "p10": 0.10}
CENTRAL_FLOOR = "p5"
CELLS = 1000
MEASURES = ("spm", "money")
# Channels in the percentile table: the central ones and their totals. Its checks raise instead of
# calling gate(), so gates.json (and the September 23 byte-for-byte rebuild) does not change.
PERCENTILE_CHANNELS = ("fiscal_a", "fiscal_b", "wages", "renters", "landlords", "housing_net", "crime",
                       "unreimbursed_care", "TOTAL_a", "TOTAL_b")

# ---------------------------------------------------------------- pinned inputs, with sources
TARGET_TOTAL = 40_896_574.15235156
CIVILIAN_TOTAL = 336_727_803          # brief: other residents = 336.727803m - 40.896574m
TAU = (0.384, 0.426)                  # nest builder TAU: labor tax rate, lower / upper skill cell

# BJS, Criminal Victimization 2023 (NCJ 309335, revised June 9, 2025) Table 3 for 2022, and
# Criminal Victimization 2024 (NCJ 310547, September 2025) Table 3 for 2023 and 2024: rate of
# violent victimization per 1,000 persons age 12 or older, by household income. "serious" is
# the table's "violent crime excluding simple assault" (rape or sexual assault, robbery,
# aggravated assault). Persons age 12+ by household income: CV 2024 appendix table 19.
NCVS_BRACKETS = (25_000, 50_000, 100_000, 200_000)
NCVS = {  # year: (violent rates, serious rates, persons 12+)
    2022: ((42.4, 26.6, 18.5, 16.4, 23.4), (19.3, 12.5, 6.8, 6.6, 7.9),
           (38_445_470, 61_575_030, 88_540_080, 68_027_520, 25_716_540)),
    2023: ((39.0, 23.9, 21.4, 17.4, 15.7), (18.7, 10.2, 8.3, 5.1, 4.0),
           (35_790_580, 58_586_650, 89_260_250, 72_096_720, 29_122_830)),
    2024: ((38.3, 22.4, 23.5, 17.7, 22.1), (23.4, 6.5, 8.0, 5.7, 8.0),
           (33_401_030, 54_519_490, 88_435_240, 76_661_880, 33_355_570)),
}
NCVS_LABELS = ("Less than $25,000", "$25,000–$49,999", "$50,000–$99,999",
               "$100,000–$199,999", "$200,000 or more")

# CBO, The Distribution of Household Income, 2022 (January 2026, publication 61911), additional
# data for researchers, table 12 (share of federal taxes, %) and table 10 (share of income before
# transfers and taxes, %), all households, 2022. Groups: quintiles 1-4, then percentiles 81-90,
# 91-95, 96-99 and the top 1 percent. "after": households ranked by income after transfers and
# taxes; "before": ranked by income before transfers and taxes.
CBO_EDGES = (0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0)
CBO_GROUPS = ("lowest_quintile", "second_quintile", "middle_quintile", "fourth_quintile",
              "percentiles_81_90", "percentiles_91_95", "percentiles_96_99", "top_1_percent")
CBO_FED_SHARE = {"after": (1.7, 4.7, 8.8, 16.0, 13.8, 10.9, 16.8, 26.9),
                 "before": (0.3, 3.9, 8.6, 16.8, 14.6, 11.3, 17.0, 27.3)}
CBO_INCOME_SHARE = {"after": (4.7, 8.5, 12.9, 19.3, 14.2, 10.0, 13.4, 17.8),
                    "before": (3.7, 8.4, 13.2, 19.7, 14.4, 10.1, 13.5, 17.8)}
# ITEP, Who Pays? 7th edition (January 2024), Figure 1 and Appendix A "Average Across All
# States": state and local taxes as a share of income, non-senior residents, 2024 law at 2023
# incomes; groups lowest/second/middle/fourth 20%, next 15%, next 4%, top 1%. The next 15% rate
# is used for CBO's 81-90 and 91-95 groups.
ITEP_RATE = (11.4, 10.4, 10.5, 10.3, 9.5, 9.5, 8.3, 7.2)
# BEA NIPA Tables 3.2 and 3.3, 2024, pinned workbook (published August 26, 2026), $ millions.
BEA_WORKBOOK = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"

PATHS = dict(
    cps=FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
    builder=FISCAL / "full_account_spending_2026_09_20/builder.py",
    service_cases=FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv",
    headline_cases=FISCAL / "full_account_2026_09_20/derived/headline_cases.csv",
    nest=FISCAL / "production_nativity_nest_2026_09_22/derived/nest_scenarios.csv",
    branches=FISCAL / "production_nativity_nest_2026_09_22/derived/branch_composition.csv",
    wage_grid=FISCAL / "wage_distribution_2026_09_23/derived/wage_distribution_grid.csv",
    housing_arms=FISCAL / "housing_transfer_2026_09_23/derived/arms_headline.csv",
    housing_exposure=FISCAL / "housing_transfer_2026_09_23/derived/cbsa_exposure.csv",
    xwalk=FISCAL / "employment_entry_2026_09_18/_cache/xwalk_puma22.csv",
    county_cbsa=FISCAL / "hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv",
    scf=FISCAL / "housing_transfer_2026_09_23/_cache/scf/rscfp2022.dta",
    acs=ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr",
    crime_offence=FISCAL / "crime_victim_cost_2026_09_23/derived/cost_by_offence_central.csv",
    crime_victim=FISCAL / "crime_victim_cost_2026_09_23/derived/cost_by_victim_and_offence_central.csv",
    crime_arms=FISCAL / "crime_victim_cost_2026_09_23/derived/arms.csv",
    uncompensated=FISCAL / "uncompensated_care_2026_09_23/derived/added_cost_arms.csv",
    cex=FISCAL / "consumer_price_benefit_2026_09_18/derived/partA_price_results.csv",
    main_case_bands=FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv",
    main_case_inputs=FISCAL / "main_case_2026_09_23/derived/inputs.json",
    main_case24_bands=FISCAL / "main_case_2026_09_24/derived/main_case_bands.csv",
    main_case24_summary=FISCAL / "main_case_2026_09_24/derived/summary.json",
)


class Case(NamedTuple):
    lane: str                     # the main-case lane
    base: str                     # the lane's summary.json key and band variant for the case it starts from
    profile: str = "cbo_category_lag_non_school_full"   # the case's profile in main_case_bands.csv
    ends: str | None = None       # case_ends.cjs output in derived/: capital return and capped programs at the ends
    out: str | None = None        # its files' directory under derived/ when they sit beside the default case's
    summary: str | None = None    # the summary.json key for the case it starts from, where it is not `base`
    grid_base: str | None = None  # the lane whose production grid the row-4 solve reproduces, where the case's adds to it


# Main cases after September 24, in adoption order. Adding a case is one entry here. September 29 (candidate v4,
# adopted 2026-09-29) writes derived/sept29/, beside the September 27 files, which stay the default; so does October 5
# (main case v5, derived/oct05/).
SEPT29_LANE = "main_case_2026_09_29"
OCT05_LANE = "main_case_2026_10_05"
LATER_CASES = {"sept26": Case("main_case_2026_09_26", "adopted_2026_09_24"),
               "sept26_schools": Case("main_case_schools_full_2026_09_26", "adopted_2026_09_26"),
               "sept27": Case("main_case_long_run_2026_09_27", "schools_case", "long_run_non_school_full",
                              "case_ends_sept27.json"),
               # Its summary.json names September 27 adopted_2026_09_27; its band variant is sept27_case.
               "sept29": Case(SEPT29_LANE, "sept27_case", "long_run_non_school_full", "case_ends_sept29.json", "sept29",
                              "adopted_2026_09_27"),
               # v5's summary.json names September 29 adopted_2026_09_29; its band variant is sept29_case. Its grid is
               # September 29's plus the lineage's production delta.
               "oct05": Case(OCT05_LANE, "sept29_case", "long_run_non_school_full", "case_ends_oct05.json", "oct05",
                             "adopted_2026_09_29", SEPT29_LANE)}
DEFAULT_CASE = "sept27"
# From September 29 the case's production grid is the account's row-4 weights (production_row4.json): the Mexico-born
# outside California and Texas raked by citizenship to ACS 2024 totals. Its P and F move the wage and fiscal channels,
# never A. The lane's own production scenarios are re-solved on those weights (row4_nest_rows).
MEXICO_BIRTHPLACE = 303
ROW4_STATUS = {4: "naturalized", 5: "noncitizen"}
ROW4_EXCLUDED_STATES = (6, 48)     # California, Texas
NEST_DIR = FISCAL / "production_nativity_nest_2026_09_22"

# Capped programs (from the September 27 case). Rental assistance and LIHEAP are capped and rationed among
# eligible households: without the group, eligible households who now go without take its slots. Each program's
# amount falls on its eligible non-recipients among other residents, equal per household (household weight),
# split equally over the household's other-resident members. Proxies, on the CPS ASEC 2025 household file:
# - rental assistance: renter households paying cash rent (H_TENURE 2) with money income below 50% of their
#   state's median household money income (all households, household weights), neither in public housing
#   (HPUBLIC) nor paying lower rent because a government pays part (HLORENT; the account's rental key uses the
#   same two flags). HUD's voucher rule is "very low income": 50% of the area's median family income, adjusted
#   for family size (24 CFR 5.603, 982.201(b)). The proxy uses the state median household income, unadjusted;
# - LIHEAP: households with money income below 150% of the 2024 HHS poverty guideline for their size (89 FR
#   2961; Alaska and Hawaii have their own), receiving no energy assistance (HENGAST). The statute's ceiling is
#   the greater of 150% of poverty and 60% of the state median income (42 U.S.C. 8624(b)(2)(B)); the proxy omits
#   the second.
CAPPED_SOURCES = CACHE / "capped"
POVERTY_GUIDELINE_2024 = {"contiguous": (15_060, 5_380), 2: (18_810, 6_730), 15: (17_310, 6_190)}  # 2 AK, 15 HI
RENTAL_INCOME_LIMIT = 0.5          # of the state median household money income
LIHEAP_POVERTY_MULTIPLE = 1.5
# From September 29 public housing's enterprise deficit (the receipt line housing_enterprise_surplus, at the rental
# line's key) is capped too (case_ends.cjs). Its eligible non-recipients are rental assistance's: the same very-low-
# income renters outside public or subsidized housing, on the same waiting lists.
CAPPED_KEY_OF = {"housing_enterprise_surplus": "housing_subsidies"}
GATES: dict[str, dict] = {}


def gate(name, ok, **detail):
    GATES[name] = dict(passed=bool(ok), **{k: (float(v) if isinstance(v, (np.floating, float, int, np.integer)) else v)
                                         for k, v in detail.items()})
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ------------------------------------------------------------------------- rank helpers
def position_rank(x, w, tiebreak=None):
    """Person-weighted percentile in (0, 1): the midpoint of each record's weight in sorted order.
    Ties are broken by record order (or by tiebreak), so tied records spread over adjacent cells
    instead of piling into one; tied records have the same income, so no weight changes."""
    order = np.lexsort((np.arange(len(x)) if tiebreak is None else tiebreak, x))
    cw = np.cumsum(w[order])
    out = np.empty(len(x))
    out[order] = (cw - w[order] / 2) / cw[-1]
    return out


def wquantile(x, w, q):
    order = np.argsort(x, kind="stable")
    cw = np.cumsum(w[order]) / w.sum()
    return x[order][np.minimum(np.searchsorted(cw, q, side="left"), len(x) - 1)]


def bins(p, n):
    return np.minimum((p * n).astype(int), n - 1)


# ------------------------------------------------------------------------- CPS frame
def load_cps():
    spec = importlib.util.spec_from_file_location("account_builder", PATHS["builder"])
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    if builder.sha(PATHS["cps"]) != builder.CPS_SHA:
        raise SystemExit("[BLOCKED] CPS source changed")
    person = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
              "PEMNTVTY", "PRDTHSP", "SPM_ID", "SPM_RESOURCES", "SPM_EQUIVSCALE", "PEARNVAL",
              "WSAL_VAL", "A_HGA", "INT_VAL", "DIV_VAL", "RNT_VAL", "PRIV", "FEDTAX_AC", "FICA",
              "STATETAX_A", "PRDTRACE", "PEHSPNON"]
    with zipfile.ZipFile(PATHS["cps"]) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=person)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]
                        ).rename(columns={"h_seq": "PH_SEQ"})
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HTOTVAL", "H_NUMPER", "HSUP_WGT"]
                        ).rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(h, on="PH_SEQ", validate="many_to_one", how="left")
    if d[["pwwgt0", "HTOTVAL", "H_NUMPER", "HSUP_WGT"]].isna().any().any():
        raise SystemExit("[BLOCKED] CPS person records without weights or household")
    civ, target = builder.canonical_target(d)
    pw = d.pwwgt0.to_numpy(float)
    gate("cps_canonical_target", abs(pw[target].sum() - TARGET_TOTAL) < 0.01,
         target=pw[target].sum(), expected=TARGET_TOTAL)
    gate("cps_civilian_total", abs(pw[civ].sum() - CIVILIAN_TOTAL) < 1.0,
         civilian=pw[civ].sum(), expected=CIVILIAN_TOTAL)
    other = civ & ~target
    gate("cps_other_residents", abs(pw[other].sum() - (CIVILIAN_TOTAL - TARGET_TOTAL)) < 1.0,
         other=pw[other].sum(), expected=CIVILIAN_TOTAL - TARGET_TOTAL)
    n_rec = d.groupby("PH_SEQ").PH_SEQ.transform("size").to_numpy()
    gate("cps_household_size_matches_records", np.array_equal(n_rec, d.H_NUMPER.to_numpy()),
         mismatches=int((n_rec != d.H_NUMPER.to_numpy()).sum()))
    spm_n = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    d["civ"], d["target"], d["other"], d["pw"] = civ, target, other, pw
    d["y_spm"] = d.SPM_RESOURCES / d.SPM_EQUIVSCALE
    d["y_money"] = d.HTOTVAL / np.sqrt(d.H_NUMPER)
    d["resources_pc"] = d.SPM_RESOURCES / spm_n          # per-capita SPM resources
    d["money_pc"] = d.HTOTVAL / d.H_NUMPER               # per-capita household money income
    # Households, split over their other-resident members, for per-household dollars.
    n_other = d.groupby("PH_SEQ").other.transform("sum").to_numpy()
    d["hh_frac"] = np.where(other, d.HSUP_WGT / 100 / np.maximum(n_other, 1), 0.0)
    # CPS tax fields, per capita within the household (check key only).
    cps_tax = (d.FEDTAX_AC + 2 * d.FICA + d.STATETAX_A).groupby(d.PH_SEQ).transform("sum")
    d["cps_tax_pc"] = cps_tax / d.H_NUMPER
    d["capital"] = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0)
    return d


def rank_frame(d, measure):
    """Percentiles of other residents (display, cells) and of all civilians (published bins)."""
    y = d[f"y_{measure}"].to_numpy(float)
    pw, other, civ = d.pw.to_numpy(), d.other.to_numpy(), d.civ.to_numpy()
    p_other = np.full(len(d), np.nan)
    p_other[other] = position_rank(y[other], pw[other])
    p_all = np.full(len(d), np.nan)
    p_all[civ] = position_rank(y[civ], pw[civ])
    ybar = float(np.average(y[other], weights=pw[other]))
    floors = {k: float(wquantile(y[other], pw[other], q)) for k, q in FLOORS.items()}
    return dict(y=y, p_other=p_other, p_all=p_all, ybar=ybar, floors=floors,
                median=float(wquantile(y[other], pw[other], 0.5)),
                q5=np.where(other, bins(np.nan_to_num(p_other), 5), -1),
                q10=np.where(other, bins(np.nan_to_num(p_other), 10), -1),
                cell=np.where(other, bins(np.nan_to_num(p_other), CELLS), -1))


def spread_cells(cell_amount, R, d):
    """Cell totals ($) to CPS other residents in the same percentile cell, per person weight."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    W = np.bincount(R["cell"][other], weights=pw[other], minlength=CELLS)
    if np.any((cell_amount != 0) & (W == 0)):
        raise SystemExit("[BLOCKED] percentile cell with an amount but no CPS persons")
    per = np.divide(cell_amount, W, out=np.zeros(CELLS), where=W > 0)
    out = np.zeros(len(d))
    out[other] = per[R["cell"][other]]
    return out


def per_person(d, key, total_bn, mask=None):
    """$ per person record so that the weighted sum equals total_bn, proportional to key."""
    pw = d.pw.to_numpy()
    m = d.other.to_numpy() if mask is None else (d.other.to_numpy() & mask)
    k = np.where(m, key, 0.0)
    den = float((pw * k).sum())
    if den == 0:
        raise SystemExit("[BLOCKED] empty distribution key")
    return total_bn * 1e9 * k / den


# ------------------------------------------------------------------------- channel totals
def fiscal_totals(case="sept23"):
    """Direct fiscal response A of the published main case and of the adopted main case.
    A = welfare - (P + F); the adopted case adds general government (0.59-0.84), justice by use
    and the under-charged part of uncompensated care to A (main_case_2026_09_23). With case
    "sept24" the adopted case is the September 24 one and the September 23 one is kept beside it;
    with a later case (LATER_CASES) it is that case, and every earlier one is kept beside it."""
    cases = pd.read_csv(PATHS["service_cases"])
    main = cases[cases.profile == "cbo_category_lag_non_school_full"].copy()
    heads = pd.read_csv(PATHS["headline_cases"])
    pf = heads.groupby("normalization").private_plus_receipts_bn.agg(["min", "max"])
    if not np.allclose(pf["min"], pf["max"]):
        raise SystemExit("[BLOCKED] production term differs across allocations")
    main["A_bn"] = main.welfare_bn - main.normalization.map(pf["min"])
    gate("fiscal_band_reproduced", np.isclose(-main.welfare_bn.max(), 165.1200005, atol=1e-6)
         and np.isclose(-main.welfare_bn.min(), 197.3841008, atol=1e-6),
         low=-main.welfare_bn.max(), high=-main.welfare_bn.min(), cases=len(main))
    A = np.unique(main.A_bn.round(9))
    pub = dict(A_low_cost=float(A.max()), A_high_cost=float(A.min()), A_mid=float((A.max() + A.min()) / 2),
               band=[float(-main.welfare_bn.max()), float(-main.welfare_bn.min())])
    bands = pd.read_csv(PATHS["main_case_bands"])
    bands = bands[bands.profile == "cbo_category_lag_non_school_full"].set_index("variant")
    inp = json.loads(PATHS["main_case_inputs"].read_text())
    gg_lo = bands.loc["gg_0.59", "cost_low_bn"] - bands.loc["published", "cost_low_bn"]
    gg_hi = bands.loc["gg_0.84", "cost_high_bn"] - bands.loc["published", "cost_high_bn"]
    just = inp["justice_change_bn"]["central"]
    unc = (inp["uncompensated_inside_bn"]["equal_low"], inp["uncompensated_inside_bn"]["equal_high"])
    d_lo, d_hi = gg_lo + just + unc[0], gg_hi + just + unc[1]
    gate("adopted_band_is_published_plus_changes",
         np.isclose(bands.loc["adopted", "cost_low_bn"], pub["band"][0] + d_lo, atol=1e-3)
         and np.isclose(bands.loc["adopted", "cost_high_bn"], pub["band"][1] + d_hi, atol=1e-3),
         adopted=[float(bands.loc["adopted", "cost_low_bn"]), float(bands.loc["adopted", "cost_high_bn"])],
         rebuilt=[pub["band"][0] + d_lo, pub["band"][1] + d_hi])
    ado = dict(A_low_cost=pub["A_low_cost"] - d_lo, A_high_cost=pub["A_high_cost"] - d_hi,
               band=[float(bands.loc["adopted", "cost_low_bn"]), float(bands.loc["adopted", "cost_high_bn"])],
               general_government=[float(gg_lo), float(gg_hi)], justice=float(just))
    ado["A_mid"] = (ado["A_low_cost"] + ado["A_high_cost"]) / 2
    out = dict(published=pub, adopted=ado, uncomp_inside=list(unc),
               PF_cash=float(pf.loc["cash", "min"]), PF_gdp=float(pf.loc["gdp", "min"]))
    if case == "sept23":
        return out
    # September 24: the package edits receipts and keyed spending, never P or F, so its change at
    # each band end moves A at that end.
    b24 = pd.read_csv(PATHS["main_case24_bands"])
    b24 = b24[b24.profile == "cbo_category_lag_non_school_full"].set_index("variant")
    s24 = json.loads(PATHS["main_case24_summary"].read_text())
    base24 = [float(b24.loc["adopted_2026_09_23", "cost_low_bn"]), float(b24.loc["adopted_2026_09_23", "cost_high_bn"])]
    band24 = [float(x) for x in s24["main_case"]]
    gate("sept24_base_is_sept23_adopted", np.allclose(base24, ado["band"], atol=1e-4), sept24_file=base24, sept23_file=ado["band"])
    gate("sept24_summary_matches_bands", np.allclose(band24, [b24.loc["adopted", "cost_low_bn"], b24.loc["adopted", "cost_high_bn"]],
                                                     atol=1e-4), summary=band24)
    change = [band24[0] - s24["adopted_2026_09_23"][0], band24[1] - s24["adopted_2026_09_23"][1]]
    gate("sept24_change_matches_summary", np.allclose(change, s24["change"], atol=1e-12), change=change)
    rebuilt = [pub["band"][0] + d_lo + change[0], pub["band"][1] + d_hi + change[1]]
    gate("sept24_band_rebuilt_from_A", np.allclose(rebuilt, band24, atol=1e-3), rebuilt=rebuilt, band=band24)
    a24 = dict(A_low_cost=ado["A_low_cost"] - change[0], A_high_cost=ado["A_high_cost"] - change[1], band=band24,
               general_government=ado["general_government"], justice=ado["justice"], sept24_change=change)
    a24["A_mid"] = (a24["A_low_cost"] + a24["A_high_cost"]) / 2
    if case == "sept24":
        out.update(adopted=a24, adopted_2026_09_23=ado, case=case)
        return out
    # Later cases: the consumption key edits receipts, and the responses (engine state, corrections.json
    # meta.responses) act on general government and schools, never on P or F; the allocation at each
    # band end stays (shared low, personal high), so the change at each band end again moves A there.
    prev_case, prev, prev_band, prev_rebuilt = "sept24", a24, band24, rebuilt
    kept, changes = dict(adopted_2026_09_23=ado, adopted_2026_09_24=a24), dict(sept24_change=change)
    for name, c in LATER_CASES.items():
        lane, base_key, summary_key = c.lane, c.base, c.summary or c.base
        kept.setdefault(base_key, prev)
        b = pd.read_csv(FISCAL / lane / "derived/main_case_bands.csv")
        b = b[b.profile == c.profile].set_index("variant")
        s = json.loads((FISCAL / lane / "derived/summary.json").read_text())
        responses = json.loads((FISCAL / lane / "derived/corrections.json").read_text())["meta"]["responses"]
        if responses != s["responses"]:
            raise SystemExit(f"[BLOCKED] {name}: corrections.json meta.responses differ from summary.json's")
        base = [float(b.loc[base_key, "cost_low_bn"]), float(b.loc[base_key, "cost_high_bn"])]
        band = [float(x) for x in s["main_case"]]
        gate(f"{name}_base_is_{prev_case}_adopted", np.allclose(base, prev_band, atol=1e-4)
             and np.allclose(s[summary_key], prev_band, rtol=0, atol=1e-9), **{f"{name}_file": base, f"{prev_case}_file": prev_band})
        gate(f"{name}_summary_matches_bands", np.allclose(band, [b.loc["adopted", "cost_low_bn"], b.loc["adopted", "cost_high_bn"]],
                                                         atol=1e-4), summary=band)
        ch = [band[0] - s[summary_key][0], band[1] - s[summary_key][1]]
        gate(f"{name}_change_matches_summary", np.allclose(ch, s["change"], rtol=0, atol=1e-12), change=ch)
        now_rebuilt = [prev_rebuilt[0] + ch[0], prev_rebuilt[1] + ch[1]]
        gate(f"{name}_band_rebuilt_from_A", np.allclose(now_rebuilt, band, atol=1e-3), rebuilt=now_rebuilt, band=band)
        changes[f"{name}_change"] = ch
        ends = case_ends(name, c, band) if c.ends else {}
        # A case that replaces the production grid moves P + F by d_pf at each end; since cost = -(P + F) - A,
        # A moves by -(change + d_pf). Before September 29, d_pf = 0. A grid after another case's (October 5 on
        # September 29's) moves P + F by its difference from that grid at the same cell.
        prod = ends.pop("production", None)
        if prod and "production" in prev:
            d_pf = production_change_after(name, prod, prev["production"], prev_case)
        else:
            d_pf = production_change(name, prod, pf) if prod else [0.0, 0.0]
        entry = dict(A_low_cost=prev["A_low_cost"] - ch[0] - d_pf[0], A_high_cost=prev["A_high_cost"] - ch[1] - d_pf[1],
                     band=band, responses=responses, justice=ado["justice"], **changes)
        entry["A_mid"] = (entry["A_low_cost"] + entry["A_high_cost"]) / 2
        entry.update(ends)
        if prod:
            engine_A = [prod["ends"][e]["A_bn"] for e in ("low", "high")]
            gate(f"{name}_A_is_the_engine_A_after_the_production_change",
                 np.allclose([entry["A_low_cost"], entry["A_high_cost"]], engine_A, rtol=0, atol=1e-3),
                 A=[entry["A_low_cost"], entry["A_high_cost"]], engine=engine_A,
                 A_if_production_were_booked_in_A=[prev["A_low_cost"] - ch[0], prev["A_high_cost"] - ch[1]])
            entry["production"] = dict(prod, change_P_plus_F_bn=d_pf)
        if name == case:
            out.update(adopted=entry, **kept, case=case)
            return out
        prev_case, prev, prev_band, prev_rebuilt = name, entry, band, now_rebuilt
    raise SystemExit(f"[BLOCKED] unknown case {case}")


def case_ends(name, c, band):
    """The case's capital return and capped programs at its band ends, from case_ends.cjs (costs, $bn)."""
    e = json.loads((DERIVED / c.ends).read_text())
    stale = [rel for rel, h in e["inputs"].items() if sha(FISCAL / rel) != h]
    if (e["case"], e["lane"], e["profile"]) != (name, c.lane, c.profile) or stale:
        raise SystemExit(f"[BLOCKED] {c.ends} is stale or for another case ({stale}); rerun node case_ends.cjs")
    ends = [e["ends"]["low"], e["ends"]["high"]]
    gate(f"{name}_case_ends_are_the_band", np.allclose([x["cost_bn"] for x in ends], band, rtol=0, atol=1e-9),
         case_ends=[x["cost_bn"] for x in ends], band=band)
    out = dict(capital_return=[x["capital_return_bn"] for x in ends],
               capital_return_by_level={lv: [x["capital_return_by_level_bn"][lv] for x in ends]
                                        for lv in ("state_local", "federal")},
               capped_programs={k: [x["capped_bn"][k] for x in ends] for k in e["capped_lines"]},
               block_grant={k: [x["block_grant_bn"][k] for x in ends] for k in (e["block_grant_line"],)})
    if "production" in e:     # the case replaces the production grid (September 29 on)
        out["production"] = e["production"]
    if "pension_accrual" in e:    # the pension switch's accrual inside A (September 29 on)
        out["pension_accrual"] = [e["pension_accrual"]["ends"]["low"], e["pension_accrual"]["ends"]["high"]]
    return out


def production_change(name, prod, pf):
    """The case's P + F at each band end less model.json's at the same production cell, $bn (case_ends.cjs).

    model.json's grid is every earlier case's, so its P + F at each end must be the account's production term for
    that end's normalization (headline_cases.csv, from which fiscal_totals takes every earlier A); gated to 1e-8,
    the grid's 1e-9 rounding of P and of F."""
    d = []
    for end in ("low", "high"):
        x = prod["ends"][end]
        base = x["model_json"]["P_bn"] + x["model_json"]["F_bn"]
        account = float(pf.loc[x["normalization"], "min"])
        gate(f"{name}_{end}_model_json_production_is_the_account_term", np.isclose(base, account, rtol=0, atol=1e-8),
             model_json=base, account=account, normalization=x["normalization"])
        d.append(x["case"]["P_bn"] + x["case"]["F_bn"] - base)
    return d


def production_change_after(name, prod, prev_prod, prev_case):
    """A grid built on an earlier case's: the case's P + F at each band end less the earlier grid's at the same cell, $bn.

    case_ends.cjs gives the earlier grid's P and F there (`previous`); they must be the earlier case's own P and F at its
    end (same cell, exact), so A moves only by what the later grid adds (October 5: the lineage's production delta)."""
    d = []
    for end in ("low", "high"):
        x, y = prod["ends"][end], prev_prod["ends"][end]
        gate(f"{name}_{end}_previous_grid_is_{prev_case}_s_production",
             x["previous"]["lane"] == LATER_CASES[name].grid_base and x["cell_index"] == y["cell_index"]
             and x["normalization"] == y["normalization"] and x["previous"]["P_bn"] == y["case"]["P_bn"]
             and x["previous"]["F_bn"] == y["case"]["F_bn"], previous=x["previous"], earlier_case=y["case"], cell=x["cell_index"])
        d.append(x["case"]["P_bn"] + x["case"]["F_bn"] - x["previous"]["P_bn"] - x["previous"]["F_bn"])
    return d


def nest_rows(normalization="cash"):
    cols = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
            "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share",
            "nest_option", "sigma_NI", "wage_pct_native_cell0", "wage_pct_native_cell1",
            "wage_pct_other_fb_cell0", "wage_pct_other_fb_cell1", "native_production_gain_bn",
            "other_immigrant_production_gain_bn", "induced_current_receipts_bn",
            "private_plus_receipts_bn", "capital_gain_bn", "capital_tax_gain_bn",
            "capital_private_residual_bn"]
    s = pd.read_csv(PATHS["nest"], usecols=cols)
    return s[(s.excluded_capital_owner_share == 0) & (s.nest_option == "A_by_nativity")
             & (s.proxy == "PEARNVAL") & (s.labor_supply_elasticity == 0)
             & (s.capital_tax_retention == 1.0) & (s.normalization == normalization)
             & (s.labor_share == 0.65)].copy()


def pick(s, split, sigma, cap, eps):
    r = s[(s.split == split) & (s.sigma == sigma) & (s.capital_adjustment == cap)
          & (s.sigma_NI == eps)]
    if len(r) != 1:
        raise SystemExit(f"[BLOCKED] nest row not unique: {split} {sigma} {cap} {eps} ({len(r)})")
    return r.iloc[0]


# The lane's production scenarios (split, sigma, capital adjustment, sigma_NI); main() picks from them, and the
# winners-losers lane also reads the account's split at sigma_NI 3.
LANE_SCENARIOS = [("below_ba", 2.0, 1.0, np.inf), ("hs_or_less", 2.0, 1.0, np.inf), ("below_ba", 2.0, 1.0, 3.0),
                  ("below_ba", 2.0, 0.0, np.inf)] + [(s, g, 1.0, np.inf) for s in ("hs_or_less", "below_ba") for g in (1.5, 2.5)] \
                 + [("hs_or_less", 2.0, 1.0, 3.0)]


def as_gdp(row, factor):
    """A cash-normalized nest row at the GDP normalization: every $bn column times GDP over the cash scale (the nest
    builder's two scales; row4_nest_rows gives the factor for each set of weights)."""
    out = row.copy()
    for k in out.index:
        if k.endswith("_bn"):
            out[k] = out[k] * factor
    out["normalization"] = "gdp"
    return out


def grid_cell(grid, **cell):
    """P and F of a production grid ({dims, private_wtp_bn, induced_receipts_bn}, engine order) at one cell."""
    i = 0
    for k, levels in grid["dims"].items():
        i = i * len(levels) + next(j for j, x in enumerate(levels) if x == cell[k] or (
            isinstance(x, float) and abs(x - cell[k]) < 1e-9))
    return grid["private_wtp_bn"][i], grid["induced_receipts_bn"][i]


def row4_nest_rows(d, nest, prod, lane):
    """The lane's production scenarios on the case's production weights (September 29 on: the account's row 4).

    Row 4 rakes the Mexico-born outside California and Texas to ACS 2024 household-population totals by citizenship
    (the grid's source, production_row4.json row4_factors: naturalized x 0.856, noncitizen x 0.778, point factors), so
    only the union's Mexico-born branch moves. The four-branch earnings by skill cell are rebuilt on this CPS frame,
    on the published weights and on row 4, and every lane scenario is re-solved with the nest lane's own make_case and
    solve_case (production_nativity_nest_2026_09_22/builder.py) and the account's tax partition
    (matched_benefits_2026_09_19/model.py fiscal_and_private), as the nest builder builds its rows (point estimate).
    Gates: the grid file is the one the case's payload pins (sha256); the frame's reweighted populations are the grid
    file's (1e-9 relative) and no civilian outside the group is reweighted; the published four-branch earnings are
    branch_composition.csv's (1e-9 relative); on the published weights every scenario reproduces its nest_scenarios.csv
    row (1e-9); on row 4 every scenario with perfect native-immigrant substitution (sigma_NI infinite) has the case
    grid's P and F at its cell (1e-6 bn; the grid rounds to 1e-9). Returns nest_rows()'s columns for LANE_SCENARIOS."""
    grid_file = FISCAL / prod["grid"]["file"]
    if sha(grid_file) != prod["grid"]["sha256"]:
        raise SystemExit(f"[BLOCKED] {prod['grid']['file']} is not the grid the case's payload pins")
    r4 = json.loads(grid_file.read_text())
    grid = json.loads((FISCAL / lane / "derived/corrections.json").read_text())["production"]
    spec = importlib.util.spec_from_file_location("nest_builder", NEST_DIR / "builder.py")
    B = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(NEST_DIR))
    try:
        spec.loader.exec_module(B)
    finally:
        sys.path.remove(str(NEST_DIR))
    model = B.load(FISCAL / "matched_benefits_2026_09_19/model.py", "matched_stationary_model")
    with zipfile.ZipFile(PATHS["cps"]) as z:
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).set_index("H_SEQ").GESTFIPS
    state = d.PH_SEQ.map(h).to_numpy()
    pw, civ, target = d.pw.to_numpy(), d.civ.to_numpy(), d.target.to_numpy()
    factor = np.ones(len(d))
    for status, label in ROW4_STATUS.items():
        m = (d.PENATVTY.eq(MEXICO_BIRTHPLACE) & d.PRCITSHP.eq(status)).to_numpy() & ~np.isin(state, ROW4_EXCLUDED_STATES)
        f = r4["row4_factors"][label]
        gate(f"row4_{label}_population_is_the_grid_file_s", np.isclose(pw[m].sum(), f["cps_population"], rtol=1e-9, atol=0),
             frame=pw[m].sum(), grid_file=f["cps_population"], records=int(m.sum()))
        gate(f"row4_{label}_reweights_only_the_group", not np.any(m & civ & ~target))
        factor[m] = f["factor"]
    weights = {"published": pw, "row4": pw * factor}
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    branches = {"native_non_union": civ & native & ~target, "union_us_born": civ & native & target,
                "other_foreign_born": civ & ~native & ~target, "union_mexico_born": civ & ~native & target}
    earn = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    published = pd.read_csv(NEST_DIR / "derived/branch_composition.csv")
    published = published[published.proxy == "PEARNVAL"].set_index(["split", "skill", "branch"]).earnings_estimate
    cases = {}
    for split in ("hs_or_less", "below_ba"):
        cut = 39 if split == "hs_or_less" else 42
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        for name, w in weights.items():
            four = np.array([[(earn * mask * cell) @ w for cell in cells] for mask in branches.values()])[:, :, None]
            if name == "published":
                want = np.array([[published[(split, k, b)] for k in (0, 1)] for b in branches])
                gate(f"row4_published_branches_{split}", np.allclose(four[:, :, 0], want, rtol=1e-9, atol=0),
                     max_rel=float(np.max(np.abs(four[:, :, 0] / want - 1))))
            total = four.sum(axis=0)
            cases[(name, split)] = dict(shares=total / total.sum(axis=0), four_share=four / total[None, :, :],
                                        union_share=(four[1] + four[3]) / total, national=total)
    # The GDP normalization's factor over cash for each set of weights: GDP (the nest builder's gdp_billions) over the
    # cash scale, labor income / labor share. Both splits cover the same earners, so the factor is one per weights.
    gdp_bn = json.loads((NEST_DIR / "derived/audit.json").read_text())["gdp_billions"]
    cash_scale = {name: cases[(name, "hs_or_less")]["national"].sum(axis=0)[0] / 0.65 for name in weights}
    gate("row4_cash_scale_is_one_for_both_splits", all(np.isclose(cases[(name, "below_ba")]["national"].sum(axis=0)[0] / 0.65,
                                                                  cash_scale[name], rtol=1e-12, atol=0) for name in weights))
    gdp_factor = {name: float(gdp_bn * 1e9 / cash_scale[name]) for name in weights}
    tau = np.asarray(B.TAU).reshape(2, 1)
    rows = {"published": [], "row4": []}
    for name in rows:
        for split, sigma, cap, eps in LANE_SCENARIOS:
            c = cases[(name, split)]
            scale = c["national"].sum(axis=0)[0] / 0.65
            res = B.solve_case(c, "A_by_nativity", eps, sigma, 0.65, cap, 0.0)
            part = model.fiscal_and_private(res, B.TAU, B.CAPITAL_TAX, 1.0, 0.0)
            private = ((1 - tau) * (res["labor_gain_by_branch"] - res["disutility_by_branch"])).sum(axis=1)
            wage = res["wage_without_over_with"]
            rows[name].append(dict(
                proxy="PEARNVAL", split=split, normalization="cash", labor_share=0.65, sigma=sigma, capital_adjustment=cap,
                labor_supply_elasticity=0.0, capital_tax_retention=1.0, excluded_capital_owner_share=0.0,
                nest_option="A_by_nativity", sigma_NI=eps,
                **{f"wage_pct_{b}_cell{k}": float(100 * (wage[i, k, 0] - 1)) for i, b in enumerate(("native", "other_fb"))
                   for k in (0, 1)},
                native_production_gain_bn=float(scale * private[0, 0] / 1e9),
                other_immigrant_production_gain_bn=float(scale * private[1, 0] / 1e9),
                induced_current_receipts_bn=float(scale * part["current_receipts_gain"][0] / 1e9),
                private_plus_receipts_bn=float(scale * part["private_plus_receipts"][0] / 1e9),
                capital_gain_bn=float(scale * res["capital_gain"][0] / 1e9),
                capital_tax_gain_bn=float(scale * part["capital_tax_gain"][0] / 1e9),
                capital_private_residual_bn=float(scale * (res["capital_gain"][0] - part["capital_tax_gain"][0]) / 1e9)))
    out = {k: pd.DataFrame(v)[nest.columns] for k, v in rows.items()}
    numeric = [c for c in nest.columns if c.endswith("_bn") or c.startswith("wage_pct")]
    control = 0.0
    for r in out["published"].itertuples(index=False):
        ref = pick(nest, r.split, r.sigma, r.capital_adjustment, r.sigma_NI)
        control = max(control, max(abs(getattr(r, k) - ref[k]) for k in numeric))
    gate("row4_published_solve_reproduces_nest_scenarios", control < 1e-9, max_abs=control, rows=len(out["published"]))
    # The published GDP factor reproduces nest_scenarios.csv's GDP rows (relative, the file's precision).
    gdp_rows = nest_rows("gdp")
    control_gdp = 0.0
    for _, r in out["published"].iterrows():
        g, ref = as_gdp(r, gdp_factor["published"]), pick(gdp_rows, r.split, r.sigma, r.capital_adjustment, r.sigma_NI)
        control_gdp = max(control_gdp, max(abs(g[k] - ref[k]) / max(abs(ref[k]), 1.0) for k in numeric if k.endswith("_bn")))
    gate("row4_published_gdp_factor_reproduces_nest_scenarios", control_gdp < 1e-9, max_rel=control_gdp,
         factor=gdp_factor["published"])
    worst = 0.0
    for _, row in out["row4"].iterrows():
        if np.isinf(row.sigma_NI):
            for norm, r in (("cash", row), ("gdp", as_gdp(row, gdp_factor["row4"]))):
                P, F = grid_cell(grid, proxy="PEARNVAL", split=r.split, normalization=norm, labor_share=0.65, sigma=r.sigma,
                                 capital_adjustment=r.capital_adjustment, labor_supply_elasticity=0.0,
                                 capital_tax_retention=1.0, excluded_capital_owner_share=0.0)
                # The grid's P is the private total: the two branches' labor gains and the capital residual.
                worst = max(worst, abs(r.native_production_gain_bn + r.other_immigrant_production_gain_bn
                                       + r.capital_private_residual_bn - P), abs(r.induced_current_receipts_bn - F))
    gate("row4_scenarios_are_the_case_grid", worst < 1e-6, max_abs_bn=worst)
    return out["row4"], dict(weights="row4", grid=prod["grid"],
                             factors={k: r4["row4_factors"][k]["factor"] for k in ROW4_STATUS.values()},
                             gdp_factor=gdp_factor, published_solve_max_abs_diff_vs_nest_scenarios=control,
                             published_gdp_factor_max_rel_diff=control_gdp, row4_max_abs_diff_vs_case_grid_bn=worst)


def lineage_rows(d, rows, base_lane, lane):
    """The lane's production scenarios with the lineage's production delta (October 5 on September 29's grid).

    The case's grid is the base case's plus the added G3+ members' P and F (main_case_lineage_2026_10_05: G3+'s
    first-order attribution per member times the added members; whites carry none). A scenario on the grid takes it
    as follows [ASSUMPTION: the added members' wage effects fall on other residents' skill cells as the union's do]:
    its wage changes, both branches, are scaled by lambda_c in skill cell c and its capital columns by kappa, two
    unknowns solved so that
      P = sum_c (1 - tau_c) lambda_c W_c + kappa x the capital residual,  F = sum_c tau_c lambda_c W_c + kappa x the
      capital tax gain
    are the case grid's P and F at the scenario's cell (W_c: the cell's pre-tax wage change of other residents on the
    CPS earnings bases). Without capital terms (capital adjusting) the unknowns are lambda_0 and lambda_1 (kappa 1);
    with them (capital fixed) one lambda for both cells and kappa. A scenario off the grid (sigma_NI 3) takes the
    factors of its sibling at sigma_NI infinite.
    Gates: every row's labor and tax parts reproduce it on the CPS bases (1e-6 bn); every grid row is the base grid's
    P and F at its cell before (1e-6 bn) and the case grid's after (1e-9 bn); every lambda and kappa is within 10% of 1."""
    base = json.loads((FISCAL / base_lane / "derived/corrections.json").read_text())["production"]
    grid = json.loads((FISCAL / lane / "derived/corrections.json").read_text())["production"]
    pw, tau = d.pw.to_numpy(), np.asarray(TAU, float)
    bases = {s: {k: float((pw * e).sum() / 1e9) for k, e in wage_basis(d, s).items()} for s in ("below_ba", "hs_or_less")}
    out, info, factors = [], [], {}
    worst_parts = worst_before = worst_after = 0.0
    for _, r in rows.iterrows():
        L = {(tag, c): -r[f"wage_pct_{tag}_cell{c}"] / 100 * bases[r.split][(tag, c)] for tag in ("native", "other_fb") for c in (0, 1)}
        W = np.array([L[("native", c)] + L[("other_fb", c)] for c in (0, 1)])
        gains = {tag: sum((1 - tau[c]) * L[(tag, c)] for c in (0, 1)) for tag in ("native", "other_fb")}
        worst_parts = max(worst_parts, abs(gains["native"] - r.native_production_gain_bn),
                          abs(gains["other_fb"] - r.other_immigrant_production_gain_bn),
                          abs(float(tau @ W) + r.capital_tax_gain_bn - r.induced_current_receipts_bn))
        key = (r.split, r.sigma, r.capital_adjustment)
        if np.isinf(r.sigma_NI):
            cell = dict(proxy="PEARNVAL", split=r.split, normalization="cash", labor_share=0.65, sigma=r.sigma,
                        capital_adjustment=r.capital_adjustment, labor_supply_elasticity=0.0, capital_tax_retention=1.0,
                        excluded_capital_owner_share=0.0)
            (P0, F0), (P1, F1) = grid_cell(base, **cell), grid_cell(grid, **cell)
            P = r.native_production_gain_bn + r.other_immigrant_production_gain_bn + r.capital_private_residual_bn
            worst_before = max(worst_before, abs(P - P0), abs(r.induced_current_receipts_bn - F0))
            if r.capital_private_residual_bn == 0 and r.capital_tax_gain_bn == 0:
                kappa, lam = 1.0, np.linalg.solve(np.array([(1 - tau) * W, tau * W]), np.array([P1, F1]))
            else:
                one, kappa = np.linalg.solve(np.array([[float((1 - tau) @ W), r.capital_private_residual_bn],
                                                       [float(tau @ W), r.capital_tax_gain_bn]]), np.array([P1, F1]))
                lam = np.array([one, one])
            factors[key] = (lam, float(kappa), (P1, F1))
        if key not in factors:
            raise SystemExit(f"[BLOCKED] lineage_rows: no sigma_NI-infinite sibling for {key}")
        lam, kappa, target = factors[key]
        new = r.copy()
        for tag in ("native", "other_fb"):
            for c in (0, 1):
                new[f"wage_pct_{tag}_cell{c}"] = r[f"wage_pct_{tag}_cell{c}"] * lam[c]
        new["native_production_gain_bn"] = sum((1 - tau[c]) * lam[c] * L[("native", c)] for c in (0, 1))
        new["other_immigrant_production_gain_bn"] = sum((1 - tau[c]) * lam[c] * L[("other_fb", c)] for c in (0, 1))
        for k in ("capital_gain_bn", "capital_tax_gain_bn", "capital_private_residual_bn"):
            new[k] = r[k] * kappa
        new["induced_current_receipts_bn"] = float(tau @ (lam * W)) + new["capital_tax_gain_bn"]
        P_new = new["native_production_gain_bn"] + new["other_immigrant_production_gain_bn"] + new["capital_private_residual_bn"]
        new["private_plus_receipts_bn"] = P_new + new["induced_current_receipts_bn"]
        if np.isinf(r.sigma_NI):
            worst_after = max(worst_after, abs(P_new - target[0]), abs(new["induced_current_receipts_bn"] - target[1]))
        # JSON has no infinity: an infinite sigma_NI is written "inf", as nest_scenarios.csv writes it.
        info.append(dict(split=r.split, sigma=float(r.sigma), capital_adjustment=float(r.capital_adjustment),
                         sigma_NI="inf" if np.isinf(r.sigma_NI) else float(r.sigma_NI),
                         lambda_cell0=float(lam[0]), lambda_cell1=float(lam[1]), kappa=float(kappa),
                         delta_P_bn=float(P_new - (r.native_production_gain_bn + r.other_immigrant_production_gain_bn
                                                    + r.capital_private_residual_bn)),
                         delta_F_bn=float(new["induced_current_receipts_bn"] - r.induced_current_receipts_bn)))
        out.append(new)
    gate("lineage_rows_parts_reproduce_each_scenario", worst_parts < 1e-6, max_abs_bn=worst_parts)
    gate("lineage_rows_start_from_the_base_grid", worst_before < 1e-6, max_abs_bn=worst_before, base=base_lane)
    gate("lineage_rows_reach_the_case_grid", worst_after < 1e-9, max_abs_bn=worst_after, case=lane)
    spread = max(max(abs(x["lambda_cell0"] - 1), abs(x["lambda_cell1"] - 1), abs(x["kappa"] - 1)) for x in info)
    gate("lineage_rows_factors_within_10pct_of_1", spread < 0.1, max_abs_deviation=spread)
    return pd.DataFrame(out)[rows.columns], dict(
        rule="the case's grid less the base's at each scenario's cell: the wage changes of skill cell c scaled by lambda_c "
             "and the capital columns by kappa so that P and F are the case grid's (two lambdas without capital terms, one "
             "lambda and kappa with them); sigma_NI 3 takes its sigma_NI-infinite sibling's factors [ASSUMPTION: the added "
             "members' effects fall on other residents' cells as the union's do]", base=base_lane, scenarios=info,
        max_abs_diff_vs_case_grid_bn=worst_after)


# ------------------------------------------------------------------------- wages
def wage_basis(d, split, proxy="PEARNVAL"):
    """Per-person earnings of other residents by branch (native, other foreign-born) and cell."""
    earn = np.maximum(d[proxy].to_numpy(float), 0)
    cut = 39 if split == "hs_or_less" else 42
    cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    other = d.other.to_numpy()
    basis = {}
    for tag, br in (("native", native), ("other_fb", ~native)):
        for c in (0, 1):
            basis[(tag, c)] = np.where(other & br & cells[c], earn, 0.0)
    return basis


def wage_delta(basis, row, after_tax):
    out = 0.0
    for (tag, c), e in basis.items():
        w = row[f"wage_pct_{tag}_cell{c}"] / 100
        out = out + (-w * e) * ((1 - TAU[c]) if after_tax else 1.0)
    return out


def wage_receipts_bn(basis, row, pw):
    return sum(TAU[c] * (-row[f"wage_pct_{tag}_cell{c}"] / 100) * (pw * e).sum()
               for (tag, c), e in basis.items()) / 1e9


# ------------------------------------------------------------------------- ACS and SCF
def read_zip(name, members, usecols, dtype):
    with zipfile.ZipFile(PATHS["acs"] / name) as z:
        for member in members:
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=usecols, dtype=dtype,
                                       chunksize=200_000)


def acs_extract():
    cache = CACHE / "acs_extract.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    persons = []
    for ch in read_zip("csv_pus.zip", ["psam_pusa.csv", "psam_pusb.csv"],
                       ["SERIALNO", "PWGTP", "RELSHIPP", "HISP", "POBP", "INTP", "ADJINC"],
                       {"SERIALNO": str}):
        persons.append(pd.DataFrame({
            "SERIALNO": ch.SERIALNO.to_numpy(), "pw": ch.PWGTP.to_numpy(float),
            "p1": (ch.HISP.eq(2) | ch.POBP.eq(303)).to_numpy(),
            "head": ch.RELSHIPP.eq(20).to_numpy(), "gq": ch.RELSHIPP.isin([37, 38]).to_numpy(),
            "intp": ch.INTP.fillna(0).to_numpy(float) * ch.ADJINC.to_numpy(float) / 1e6}))
    persons = pd.concat(persons, ignore_index=True)
    households = []
    for ch in read_zip("csv_hus.zip", ["psam_husa.csv", "psam_husb.csv"],
                       ["SERIALNO", "STATE", "PUMA", "WGTP", "NP", "TYPEHUGQ", "TEN", "RNTP",
                        "VALP", "HINCP", "ADJINC", "ADJHSG"],
                       {"SERIALNO": str, "STATE": str, "PUMA": str}):
        ch = ch[ch.TYPEHUGQ.eq(1) & ch.NP.gt(0)]
        adj = ch.ADJHSG.to_numpy(float) / 1e6
        households.append(pd.DataFrame({
            "SERIALNO": ch.SERIALNO.to_numpy(), "STATE": ch.STATE.to_numpy(),
            "PUMA": ch.PUMA.to_numpy(), "wgtp": ch.WGTP.to_numpy(float), "np": ch.NP.to_numpy(float),
            "ten": ch.TEN.to_numpy(),
            "rent": np.where(ch.TEN.eq(3), ch.RNTP.fillna(0).to_numpy(float), 0) * 12 * adj,
            "value": np.where(ch.TEN.isin([1, 2]), ch.VALP.fillna(0).to_numpy(float), 0) * adj,
            "hinc": ch.HINCP.fillna(0).to_numpy(float) * ch.ADJINC.to_numpy(float) / 1e6}))
    households = pd.concat(households, ignore_index=True)
    CACHE.mkdir(exist_ok=True)
    out = dict(persons=persons, households=households)
    pd.to_pickle(out, cache)
    return out


def puma_exposure(households):
    """Each PUMA's share of rent due to the group, f = 1 - (1 - s)^e, averaged over its areas."""
    xw = pd.read_csv(PATHS["xwalk"], dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(PATHS["county_cbsa"], dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    expo = pd.read_csv(PATHS["housing_exposure"], dtype={"area": str})[["area", "group_share"]]
    alloc = alloc.merge(expo, on="area", how="left", validate="many_to_one")
    if alloc.group_share.isna().any():
        raise SystemExit("[BLOCKED] crosswalk area without a group share")
    key = households.STATE + "|" + households.PUMA
    if not key.isin(alloc.state + "|" + alloc.puma).all():
        raise SystemExit("[BLOCKED] ACS PUMA missing from the crosswalk")
    return alloc


def acs_channels(acs, arms):
    """Other renters' extra rent, other owners' value gain, and the ACS capital-income key,
    in 1,000 percentile cells of ACS other residents ranked by HINCP / sqrt(NP)."""
    P, H = acs["persons"], acs["households"]
    head = P[P["head"]].drop_duplicates("SERIALNO").set_index("SERIALNO")["p1"]
    H = H.assign(head_p1=H.SERIALNO.map(head))
    if H.head_p1.isna().any():
        raise SystemExit("[BLOCKED] ACS household without a householder record")
    H["y"] = H.hinc / np.sqrt(H.np)
    y_of = H.set_index("SERIALNO")["y"]
    ref = P[~P.p1 & ~P.gq].copy()
    ref["y"] = ref.SERIALNO.map(y_of)
    if ref.y.isna().any():
        raise SystemExit("[BLOCKED] ACS person outside an occupied household")
    y_ref, w_ref = ref.y.to_numpy(), ref.pw.to_numpy()
    # Members of a household are adjacent in the sort (ties broken by serial number); the
    # household's percentile is the mean of its other-resident members' positions.
    ref["p"] = position_rank(y_ref, w_ref, pd.factorize(ref.SERIALNO)[0])
    H["p"] = H.SERIALNO.map(ref.groupby("SERIALNO").p.mean())
    H = H[~(H.p.isna() & H.head_p1.astype(bool))].copy()
    if H.p.isna().any():
        raise SystemExit("[BLOCKED] ACS household without an other-resident member")
    H["cell"] = bins(H.p.to_numpy(), CELLS)
    H["q5"] = bins(H.p.to_numpy(), 5)
    ref["cell"] = bins(ref.p.to_numpy(), CELLS)
    alloc = puma_exposure(H)
    s_nat = TARGET_TOTAL / 340.110988e6
    out = {}
    renters = (H.ten.eq(3) & ~H.head_p1.astype(bool)).to_numpy()
    owners = (H.ten.isin([1, 2]) & ~H.head_p1.astype(bool)).to_numpy()
    key = (H.STATE + "|" + H.PUMA).to_numpy()
    for (level, geography), r in arms.items():
        e = r["elasticity"]
        if geography == "metro_local":
            a = alloc.assign(f=alloc.afact * (1 - (1 - alloc.group_share) ** e))
            f_puma = a.groupby(a.state + "|" + a.puma).f.sum()
            f = pd.Series(key).map(f_puma).to_numpy()
        else:
            f = np.full(len(H), 1 - (1 - s_nat) ** e)
        rent_x = np.where(renters, f * H.rent.to_numpy() * H.wgtp.to_numpy(), 0.0)
        value_x = np.where(owners, f * H.value.to_numpy() * H.wgtp.to_numpy(), 0.0)
        gate(f"acs_rent_{level}_{geography}", np.isclose(rent_x.sum() / 1e9,
             r["other_renters_extra_rent_bn"], rtol=1e-6),
             acs=rent_x.sum() / 1e9, lane=r["other_renters_extra_rent_bn"])
        gate(f"acs_owner_value_{level}_{geography}", np.isclose(value_x.sum() / 1e9,
             r["other_owner_value_gain_stock_bn"], rtol=1e-6),
             acs=value_x.sum() / 1e9, lane=r["other_owner_value_gain_stock_bn"])
        out[(level, geography)] = dict(
            rent_cells=np.bincount(H.cell, weights=rent_x, minlength=CELLS),
            value_cells=np.bincount(H.cell, weights=value_x, minlength=CELLS),
            rent_q5=np.bincount(H.q5, weights=rent_x, minlength=5),
            renter_households_q5=np.bincount(H.q5, weights=np.where(renters, H.wgtp, 0.0), minlength=5))
    intp = ref.intp.clip(lower=0).to_numpy() * ref.pw.to_numpy()
    out["intp_cells"] = np.bincount(ref.cell, weights=intp, minlength=CELLS)
    out["acs_checks"] = dict(
        other_persons_m=float(w_ref.sum() / 1e6),
        other_renter_households_m=float(H.wgtp[renters].sum() / 1e6),
        group_share_of_positive_intp=float(
            (P.intp.clip(lower=0) * P.pw)[P.p1 & ~P.gq].sum() / (P.intp.clip(lower=0) * P.pw)[~P.gq].sum()))
    return out


def scf_cells():
    d = pd.read_stata(PATHS["scf"], columns=["y1", "wgt", "income", "kids", "married", "oresre"])
    size = 1 + (d.married == 1).astype(float) + d.kids.astype(float)
    y = (d.income / np.sqrt(size)).to_numpy(float)
    pw = (d.wgt * size).to_numpy(float)
    p = position_rank(y, pw)
    cells = np.bincount(bins(p, CELLS), weights=(d.wgt * d.oresre).to_numpy(float), minlength=CELLS)
    gate("scf_families", np.isclose(d.wgt.sum() / 1e6, 131.306, atol=0.01), families_m=d.wgt.sum() / 1e6)
    return cells, dict(families_m=float(d.wgt.sum() / 1e6), oresre_tn=float((d.wgt * d.oresre).sum() / 1e12),
                       top10pct_share=float(cells[900:].sum() / cells.sum()),
                       top1pct_share=float(cells[990:].sum() / cells.sum()))


# ------------------------------------------------------------------------- tax keys
def bea_totals():
    x = pd.ExcelFile(BEA_WORKBOOK)
    out = {}
    for sheet, lines in (("T30200-A", {"tax": "Current tax receipts", "row": "Taxes from the rest of the world",
                                        "si": "Contributions for government social insurance",
                                        "si_row": "From the rest of the world"}),
                         ("T30300-A", {"tax": "Current tax receipts",
                                       "si": "Contributions for government social insurance"})):
        t = pd.read_excel(x, sheet, header=None)
        col = [j for j, v in enumerate(t.iloc[7]) if str(v).startswith("2024")][0]
        lab = t.iloc[:, 1].astype(str).str.replace(r"\\\d+\\", "", regex=True).str.strip()
        vals = {}
        for k, label in lines.items():
            hit = t.index[lab == label]
            vals[k] = float(t.iloc[hit[0], col]) / 1e3   # $bn
        out[sheet] = vals
    fed = out["T30200-A"]
    F = fed["tax"] - fed["row"] + fed["si"] - fed["si_row"]
    S = out["T30300-A"]["tax"] + out["T30300-A"]["si"]
    gate("bea_2024_totals", 4900 < F < 5100 and 2500 < S < 2600, federal_bn=F, state_local_bn=S)
    return F, S


def tax_key(d, R, ranking, F, S):
    """Taxes attributed to each civilian: CBO federal shares and ITEP state-local rates by
    all-resident percentile group, spread within group by per-capita household money income."""
    civ, pw = d.civ.to_numpy(), d.pw.to_numpy()
    base = np.where(civ, np.maximum(d.money_pc.to_numpy(float), 0), 0.0)
    g = np.where(civ, np.searchsorted(CBO_EDGES[1:-1], np.nan_to_num(R["p_all"]), side="right"), -1)
    fed_share = np.array(CBO_FED_SHARE[ranking]) / sum(CBO_FED_SHARE[ranking])
    sl_group = np.array(ITEP_RATE) * np.array(CBO_INCOME_SHARE[ranking])
    sl_share = sl_group / sl_group.sum()
    fed = np.zeros(len(d))
    sl = np.zeros(len(d))
    for k in range(len(CBO_GROUPS)):
        m = g == k
        den = float((pw[m] * base[m]).sum())
        fed[m] = fed_share[k] * base[m] / den
        sl[m] = sl_share[k] * base[m] / den
    tax = F * fed + S * sl
    return tax, dict(other_share_of_taxes=float((pw * tax)[d.other.to_numpy()].sum() / (pw * tax)[civ].sum()),
                     state_local_group_shares=sl_share.round(4).tolist())


# ------------------------------------------------------------------------- crime key
def ncvs_rates():
    pops = np.array([NCVS[y][2] for y in NCVS], float)
    violent = (np.array([NCVS[y][0] for y in NCVS]) * pops).sum(0) / pops.sum(0)
    serious = (np.array([NCVS[y][1] for y in NCVS]) * pops).sum(0) / pops.sum(0)
    cum = np.cumsum(pops.sum(0)) / pops.sum()
    return dict(violent=violent, serious=serious, simple=violent - serious, cum=cum[:-1],
                pops=pops.sum(0))


def verify_ncvs_text():
    """Positive control: the pinned cells appear in the cached BJS text (when cached)."""
    found = {}
    for fname, years in (("bjs_cv23.txt", (2022, 2023)), ("bjs_cv24.txt", (2023, 2024))):
        path = SOURCES / fname
        if not path.exists():
            print(f"[DEGRADED] {fname} not cached; NCVS cells not re-verified against the report")
            return False
        text = path.read_text()
        block = text[text.index("Rate of violent victimization, by type of crime and"):]
        block = block[:block.index("Note: Rates are per 1,000")]
        for k, label in enumerate(NCVS_LABELS):
            rows = [[float(v) for v in re.findall(r"\d+\.\d", l.split(label)[1])]
                    for l in block.splitlines() if label in l]
            nums = next(r for r in rows if len(r) >= 4)
            expect = (NCVS[years[0]][0][k], NCVS[years[1]][0][k], NCVS[years[0]][1][k], NCVS[years[1]][1][k])
            found[f"{fname}:{label}"] = nums
            if tuple(nums[:4]) != expect:
                raise SystemExit(f"[BLOCKED] NCVS pin differs from {fname} {label}: {nums} vs {expect}")
    gate("ncvs_cells_match_bjs_text", True, rows=len(found))
    return True


def verify_published_text():
    """Positive controls for the CBO and ITEP pins against the cached documents (when cached)."""
    root = SOURCES / "cbo_61911/61911-additional-data-for-researchers/CBO_distribution_household_income_2022_data"
    if root.exists():
        for ranking, stem in (("after", "inc_after_trans_tax"), ("before", "inc_before_trans_tax")):
            t12 = pd.read_csv(root / f"households_ranked_by_{stem}_table_12_federal_tax_shares_1979_2022.csv")
            t10 = pd.read_csv(root / f"households_ranked_by_{stem}_table_10_household_income_shares_1979_2022.csv")
            a12 = t12[(t12.household_type == "all_households") & (t12.year == 2022)].set_index("income_group")
            a10 = t10[(t10.household_type == "all_households") & (t10.year == 2022)].set_index("income_group")
            got_f = tuple(a12.loc[list(CBO_GROUPS), "federal_taxes"])
            got_i = tuple(a10.loc[list(CBO_GROUPS), "inc_before_transfers_taxes"])
            if got_f != CBO_FED_SHARE[ranking] or got_i != CBO_INCOME_SHARE[ranking]:
                raise SystemExit(f"[BLOCKED] CBO pins differ from table 12/10 ({ranking}): {got_f} {got_i}")
        gate("cbo_pins_match_tables", True)
    else:
        print("[DEGRADED] CBO researcher tables not cached; pins not re-verified")
    itep = SOURCES / "itep_ITEP-Who-Pays-7th-edition.txt"
    if itep.exists():
        text = itep.read_text()
        at = text.index("Average Across")
        got = tuple(float(v) for v in re.findall(r"(\d+\.\d)%", text[at:at + 300])[:7])
        pinned = ITEP_RATE[:4] + ITEP_RATE[5:]
        gate("itep_pins_match_appendix", got == pinned, text=str(got), pinned=str(pinned))
    else:
        print("[DEGRADED] ITEP text not cached; pins not re-verified")


def crime_key(d, R_money_all, rates, mode):
    """Victimization risk per other resident age 12+, by household-income bracket."""
    htot = d.HTOTVAL.to_numpy(float)
    age = d.A_AGE.to_numpy()
    if mode == "rank":
        # NCVS bracket populations (2022-2024 pooled) give each bracket's percentile band of
        # persons 12+ ranked by household income; CPS persons 12+ (all civilians) are ranked
        # by HTOTVAL and placed in the same bands.
        idx = np.searchsorted(rates["cum"], np.nan_to_num(R_money_all), side="right")
    else:
        idx = np.searchsorted(NCVS_BRACKETS, htot, side="right")
    idx = np.clip(idx, 0, 4)
    old = age >= 12
    return {k: np.where(old, rates[k][idx], 0.0) for k in ("violent", "serious", "simple")}, idx


# ------------------------------------------------------------------------- capped programs
def verify_capped_text():
    """Positive controls for the capped programs' rules against the cached texts (when cached)."""
    checks = {"fr_2024-00796.txt": ["$15,060", "add $5,380", "$18,810", "add $6,730", "$17,310", "add $6,190"],
              "usc42_8624.html": ["150 percent of the poverty level", "60 percent of the State median income"],
              "cfr24_5.603.html": ["50 percent of the median family income for the area"],
              "cfr24_982.201.html": ["very low income"]}
    found = {}
    for fname, needles in checks.items():
        path = CAPPED_SOURCES / fname
        if not path.exists():
            print(f"[DEGRADED] {fname} not cached; the capped-program rules are not re-verified against it")
            continue
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", path.read_text(errors="replace")))
        missing = [n for n in needles if n not in text]
        if missing:
            raise SystemExit(f"[BLOCKED] {fname} lacks the pinned text {missing}")
        found[fname] = sha(path)
    pinned = POVERTY_GUIDELINE_2024
    gate("capped_rules_match_texts", len(found) == len(checks) and pinned["contiguous"] == (15_060, 5_380)
         and pinned[2] == (18_810, 6_730) and pinned[15] == (17_310, 6_190), files=len(found))
    return found


def capped_keys(d):
    """Per-person keys of each capped program's eligible non-recipients: every eligible household with other
    residents counts once (household weight), split equally over its other-resident members."""
    with zipfile.ZipFile(PATHS["cps"]) as z:
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS", "H_TENURE", "HPUBLIC", "HLORENT",
                                                        "HENGAST", "HTOTVAL", "H_NUMPER", "HSUP_WGT"])
    h = h[h.H_SEQ.isin(d.PH_SEQ.unique())].set_index("H_SEQ")          # households with person records
    codes = {"H_TENURE": {1, 2, 3}, "HPUBLIC": {0, 1, 2}, "HLORENT": {0, 1, 2}, "HENGAST": {1, 2}}
    gate("capped_cps_codes", all(set(h[k].unique()) <= v for k, v in codes.items()) and h.GESTFIPS.nunique() == 51,
         households=len(h), states=h.GESTFIPS.nunique())
    hw = h.HSUP_WGT / 100
    median = {st: float(wquantile(g.HTOTVAL.to_numpy(float), g.HSUP_WGT.to_numpy(float), 0.5))
              for st, g in h.groupby("GESTFIPS")}
    base, step = (np.array(v, float) for v in zip(*[POVERTY_GUIDELINE_2024.get(st, POVERTY_GUIDELINE_2024["contiguous"])
                                                     for st in h.GESTFIPS]))
    guideline = base + step * (h.H_NUMPER.to_numpy(float) - 1)
    recipient = {"housing_subsidies": h.HPUBLIC.eq(1) | h.HLORENT.eq(1), "energy_assistance": h.HENGAST.eq(1)}
    eligible = {"housing_subsidies": h.H_TENURE.eq(2) & (h.HTOTVAL < RENTAL_INCOME_LIMIT * h.GESTFIPS.map(median)),
                "energy_assistance": h.HTOTVAL < LIHEAP_POVERTY_MULTIPLE * guideline}
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    keys, info = {}, {}
    for line in eligible:
        flag = eligible[line] & ~recipient[line]
        on_person = d.PH_SEQ.map(flag)
        if on_person.isna().any():
            raise SystemExit(f"[BLOCKED] {line}: a person record without its household")
        m = other & on_person.to_numpy(bool)
        if np.any(pw[m] <= 0):
            raise SystemExit(f"[BLOCKED] {line}: an eligible other resident without a person weight")
        keys[line] = np.where(m, d.hh_frac.to_numpy() / np.where(m, pw, 1.0), 0.0)
        with_other = flag & h.index.isin(d.PH_SEQ[other])
        gate(f"capped_{line}_equal_per_household", np.isclose((pw * keys[line]).sum(), hw[with_other].sum(), rtol=1e-12),
             key_sum=(pw * keys[line]).sum(), households=hw[with_other].sum())
        info[line] = dict(eligible_non_recipient_households_m=float(hw[with_other].sum() / 1e6),
                          other_residents_in_them_m=float(pw[m].sum() / 1e6),
                          eligible_households_all_m=float(hw[eligible[line]].sum() / 1e6),
                          recipient_households_all_m=float(hw[recipient[line]].sum() / 1e6))
    info["state_median_household_income"] = dict(min=min(median.values()), max=max(median.values()),
                                                  national=float(wquantile(h.HTOTVAL.to_numpy(float),
                                                                           h.HSUP_WGT.to_numpy(float), 0.5)))
    return keys, info


# ------------------------------------------------------------------------- weights and tables
def person_weights(d, R, eta, floor):
    """(max(y, floor) / ybar)^(-eta) for other residents; None if the floor is not positive
    (the 1st percentile of SPM resources is below zero, so its weight is undefined)."""
    f = R["floors"][floor]
    if eta > 0 and f <= 0:
        return None
    y = np.maximum(R["y"], f)
    out = np.zeros(len(d))
    m = d.other.to_numpy()
    out[m] = (y[m] / R["ybar"]) ** (-eta)
    return out


def weighted(delta, d, R, eta, floor):
    w = person_weights(d, R, eta, floor)
    if w is None:
        return float("nan")
    return float((d.pw.to_numpy() * w * delta).sum() / 1e9)


def bin_weighted(delta, d, R, eta, nbin, floor=None):
    """sum_q (ybar_q / ybar)^(-eta) Delta_q. The brief's version uses unfloored bin means; with
    `floor` the bin means are of floored incomes, so only the resolution differs from the
    per-person sum at that floor."""
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    q = R["q5"] if nbin == 5 else R["q10"]
    y = R["y"] if floor is None else np.maximum(R["y"], R["floors"][floor])
    tot = np.bincount(q[other], weights=(pw * delta)[other], minlength=nbin)
    ybin = (np.bincount(q[other], weights=(pw * y)[other], minlength=nbin)
            / np.bincount(q[other], weights=pw[other], minlength=nbin))
    return float(((ybin / R["ybar"]) ** (-eta) * tot).sum() / 1e9)


def by_bin(delta, d, R, nbin=5):
    other, pw = d.other.to_numpy(), d.pw.to_numpy()
    q = (R["q5"] if nbin == 5 else R["q10"])[other]
    x = (pw * delta)[other]
    return dict(net=np.bincount(q, weights=x, minlength=nbin) / 1e9,
                loss=np.bincount(q, weights=np.minimum(x, 0), minlength=nbin) / 1e9,
                gain=np.bincount(q, weights=np.maximum(x, 0), minlength=nbin) / 1e9)


def main():
    ap = argparse.ArgumentParser(description="Distribution of the account's channels among other residents.")
    ap.add_argument("--case", choices=(*reversed(list(LATER_CASES)), "sept24", "sept23"), default=DEFAULT_CASE,
                    help="a case after September 24 (default sept27: long-run responses, rental assistance, government "
                         "enterprises and the return on public capital; sept29: candidate v4, adopted 2026-09-29, "
                         "written to derived/sept29/; oct05: main case v5, adopted 2026-10-05, written to "
                         "derived/oct05/; sept26_schools: schools at full average cost; sept26: CBO's "
                         "one-year school response, 0.63-0.66), or an earlier adopted case")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="default derived/, or derived/<dir> for a case whose files sit beside the default case's")
    args = ap.parse_args()
    sub = LATER_CASES[args.case].out if args.case in LATER_CASES else None
    out_dir = args.out_dir or (DERIVED / sub if sub else DERIVED)
    out_dir.mkdir(parents=True, exist_ok=True)
    verify_published_text()
    ncvs_verified = verify_ncvs_text()
    d = load_cps()
    pw, other = d.pw.to_numpy(), d.other.to_numpy()
    fiscal = fiscal_totals(args.case)
    adopted = fiscal["adopted"]
    # The budget's part of A. From the September 27 case the capped programs leave it for their eligible
    # non-recipients (D, a cost at each band end), and the capital return K is also reported alone.
    budget_mid = adopted["A_mid"]
    capped = "capped_programs" in adopted
    if capped:
        capped_texts = verify_capped_text()
        capped_key, capped_info = capped_keys(d)
        # Each capped program's key (public housing takes rental assistance's), in the case's order of programs.
        program_key = {k: capped_key[CAPPED_KEY_OF.get(k, k)] for k in adopted["capped_programs"]}
        D_end = [sum(v[j] for v in adopted["capped_programs"].values()) for j in (0, 1)]
        D_mid = (D_end[0] + D_end[1]) / 2
        K_mid = (adopted["capital_return"][0] + adopted["capital_return"][1]) / 2
        budget_mid = adopted["A_mid"] + D_mid

        def displaced(j=None, lines=tuple(program_key)):
            """Per-person loss of eligible non-recipients: at band end j, or the mean of the two ends."""
            at = {k: (v[0] + v[1]) / 2 if j is None else v[j] for k, v in adopted["capped_programs"].items()}
            return sum(per_person(d, program_key[k], -at[k]) for k in lines)
    # The pension accrual (September 29 on) sits in A and is not financed today: the cash part leaves it out and
    # fiscal_accrual_* reports it (a cost at each band end, ACC).
    accrual = adopted.get("pension_accrual")
    ACC_mid = (accrual[0] + accrual[1]) / 2 if accrual else 0.0
    F_total, S_total = bea_totals()
    rates = ncvs_rates()

    # ---- production term: after-tax wages P to workers, induced receipts F to the budget. From September 29 the
    # case's production grid is on row-4 weights, so the lane's scenarios are re-solved on them (row4_nest_rows) and
    # the case's P and F go to the wage and fiscal channels; the published September 20 band keeps the published ones.
    nest = nest_rows()
    prod = adopted.get("production")
    # October 5 on: the row-4 solve reproduces the base case's grid, and the lineage's production delta is added to it.
    case_def = LATER_CASES.get(args.case)
    rows, prod_info = row4_nest_rows(d, nest, prod, case_def.grid_base or case_def.lane) if prod else (nest, None)
    if prod and case_def.grid_base:
        rows, prod_info["lineage"] = lineage_rows(d, rows, case_def.grid_base, case_def.lane)
    central = pick(rows, "below_ba", 2.0, 1.0, np.inf)
    account = pick(rows, "hs_or_less", 2.0, 1.0, np.inf)
    eps3 = pick(rows, "below_ba", 2.0, 1.0, 3.0)
    short = pick(rows, "below_ba", 2.0, 0.0, np.inf)
    central_published = pick(nest, "below_ba", 2.0, 1.0, np.inf)
    account_pf = fiscal["PF_cash"]
    if prod:
        grid = json.loads((FISCAL / LATER_CASES[args.case].lane / "derived/corrections.json").read_text())["production"]
        account_pf = sum(grid_cell(grid, proxy="PEARNVAL", split="hs_or_less", normalization="cash", labor_share=0.65,
                                   sigma=2.0, capital_adjustment=1.0, labor_supply_elasticity=0.0,
                                   capital_tax_retention=1.0, excluded_capital_owner_share=0.0))
    gate("account_production_term", np.isclose(account.private_plus_receipts_bn, account_pf, rtol=1e-9),
         nest=account.private_plus_receipts_bn, account=account_pf)
    branches = pd.read_csv(PATHS["branches"])
    basis = {s: wage_basis(d, s) for s in ("below_ba", "hs_or_less")}
    for split in basis:
        for (tag, c), e in basis[split].items():
            name = "native_non_union" if tag == "native" else "other_foreign_born"
            ref = branches[(branches.proxy == "PEARNVAL") & (branches.split == split)
                           & (branches.skill == c) & (branches.branch == name)].earnings_estimate.iloc[0]
            gate(f"wage_base_{split}_{tag}_cell{c}", np.isclose((pw * e).sum(), ref, rtol=1e-9),
                 cps=(pw * e).sum() / 1e9, nest=ref / 1e9)
    scen = {"below_ba_s2.0": ("below_ba", central), "hs_or_less_s2.0": ("hs_or_less", account),
            "below_ba_s2.0_eps3": ("below_ba", eps3)}
    for split in ("hs_or_less", "below_ba"):
        for sig in (1.5, 2.5):
            scen[f"{split}_s{sig}"] = (split, pick(nest, split, sig, 1.0, np.inf))
    for label, (split, row) in scen.items():
        after = (pw * wage_delta(basis[split], row, True)).sum() / 1e9
        rec = wage_receipts_bn(basis[split], row, pw)
        P = row.native_production_gain_bn + row.other_immigrant_production_gain_bn
        gate(f"wage_after_tax_equals_P_{label}", np.isclose(after, P, rtol=1e-8, atol=1e-9), cps=after, nest=P)
        gate(f"wage_receipts_equal_F_{label}", np.isclose(rec, row.induced_current_receipts_bn, rtol=1e-8),
             cps=rec, nest=row.induced_current_receipts_bn)
    F_c = float(central.induced_current_receipts_bn)
    P_c = float(central.native_production_gain_bn + central.other_immigrant_production_gain_bn)
    F_published = float(central_published.induced_current_receipts_bn)   # F_c before September 29

    # ---- housing arms (long run, form A, central ownership, householder rule)
    ha = pd.read_csv(PATHS["housing_arms"]).drop_duplicates(["arm", "level", "form", "geography", "ownership"])
    ha = ha[(ha.arm == "long_run") & (ha.form == "A") & (ha.ownership == "central")]
    arms = {(r.level, r.geography): r._asdict() for r in ha.itertuples()}
    acs = acs_channels(acs_extract(), arms)
    scf, scf_info = scf_cells()

    # ---- crime victims' harm
    off = pd.read_csv(PATHS["crime_offence"]).set_index("offence")
    carms = pd.read_csv(PATHS["crime_arms"]).set_index("arm")
    crime_equal = float(off.loc["Total", "cost_full"]) / 1e9
    crime_tangible_equal = float(off.loc["Total", "cost_tangible"]) / 1e9
    crime_custody = float(carms.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"])
    env_low = float(carms.loc["ENVELOPE low, miller2021", "full_bn"])
    env_high = float(carms.loc["ENVELOPE high, miller2021_dot_vsl", "full_bn"])
    gate("crime_central", np.isclose(crime_equal, 28.9229, atol=5e-4) and np.isclose(crime_custody, 32.3381, atol=5e-4),
         equal_footing=crime_equal, custody_footing=crime_custody)
    serious_off = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault"]
    serious_share = float(off.loc[serious_off, "cost_full"].sum() / off.loc["Total", "cost_full"])
    serious_share_tan = float(off.loc[serious_off, "cost_tangible"].sum() / off.loc["Total", "cost_tangible"])
    vic = pd.read_csv(PATHS["crime_victim"])
    vic["cls"] = np.where(vic.offence.eq("Simple assault"), "simple", "serious")
    by_race = vic.groupby(["victim", "cls"]).cost_full.sum() / vic.cost_full.sum()

    # ---- unreimbursed hospital care (outside budgets); the inside part is in the adopted case
    unc = pd.read_csv(PATHS["uncompensated"])
    eq = unc[unc.use_intensity == 1.0]
    out_lo, out_hi = float(eq.outside_accounts_bn.min()), float(eq.outside_accounts_bn.max())
    in_lo, in_hi = float(eq.inside_undercharged_bn.min()), float(eq.inside_undercharged_bn.max())
    gate("uncompensated_inside_matches_main_case",
         np.isclose(in_lo, fiscal["uncomp_inside"][0], atol=1e-4) and np.isclose(in_hi, fiscal["uncomp_inside"][1], atol=1e-4),
         lane=[in_lo, in_hi], main_case=fiscal["uncomp_inside"])
    unreimbursed_mid = (out_lo + out_hi) / 2

    cex = pd.read_csv(PATHS["cex"])
    cex = cex[(cex.arm == "published_jpe_2008") & (cex.shock == "lf_adjusted")
              & (cex.scope == "narrow_immigrant_intensive")].iloc[0]
    cex_q = np.array([cex[f"loss_bn_{k}"] for k in ("q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest")])

    # NCVS ranking: all civilians 12+ by unequivalized household money income.
    htot = d.HTOTVAL.to_numpy(float)
    m12 = d.civ.to_numpy() & (d.A_AGE.to_numpy() >= 12)
    p12 = np.full(len(d), np.nan)
    p12[m12] = position_rank(htot[m12], pw[m12])
    keys_rank, idx_rank = crime_key(d, p12, rates, "rank")
    keys_dollar, idx_dollar = crime_key(d, p12, rates, "dollar")
    bracket_share = {mode: (np.bincount(idx[m12], weights=pw[m12], minlength=5) / pw[m12].sum()).round(4).tolist()
                     for mode, idx in (("rank", idx_rank), ("dollar", idx_dollar))}
    hisp = d.PEHSPNON.eq(1).to_numpy()
    race = np.select([~hisp & d.PRDTRACE.eq(1).to_numpy(), ~hisp & d.PRDTRACE.eq(2).to_numpy(), hisp],
                     ["White", "Black", "Hispanic"], "Other")
    priv = d.PRIV.eq(1).to_numpy()
    R_money = rank_frame(d, "money")

    tables = {k: [] for k in ("frame", "quintile", "decile", "weighted", "regress", "weights", "ranges",
                              "percentile")}
    notes = {}
    for measure in MEASURES:
        R = R_money if measure == "money" else rank_frame(d, measure)
        ranking = "after" if measure == "spm" else "before"
        tax, tax_info = tax_key(d, R, ranking, F_total, S_total)
        notes[f"tax_{measure}"] = tax_info
        keys = {"a": tax, "b": np.ones(len(d))}
        ch = {}

        def crime_split(k, total, s_share=serious_share):
            return per_person(d, k["serious"], -total * s_share) + per_person(d, k["simple"], -total * (1 - s_share))

        # Central channels.
        for conv, key in keys.items():
            ch[f"fiscal_{conv}"] = per_person(d, key, budget_mid + F_c)
        ch["wages"] = wage_delta(basis["below_ba"], central, True)
        ch["renters"] = -spread_cells(acs[("central", "metro_local")]["rent_cells"], R, d)
        landlord = {}
        for (level, geo), a in arms.items():
            tot = a["other_renters_extra_rent_bn"] + a["net_other_residents_welfare_bn"]
            li = per_person(d, spread_cells(acs["intp_cells"], R, d), tot)
            ls = per_person(d, spread_cells(scf, R, d), tot)
            landlord[(level, geo)] = dict(intp=li, scf=ls, mid=(li + ls) / 2)
        ch["landlords"] = landlord[("central", "metro_local")]["mid"]
        ch["crime"] = crime_split(keys_rank, crime_custody)
        ch["unreimbursed_care"] = per_person(d, priv.astype(float), -unreimbursed_mid)
        ch["housing_net"] = ch["renters"] + ch["landlords"]
        central_parts = ["wages", "renters", "landlords", "crime", "unreimbursed_care"]
        if capped:
            ch["displaced_beneficiaries"] = displaced()
            central_parts.append("displaced_beneficiaries")
        for conv in keys:
            ch[f"TOTAL_{conv}"] = ch[f"fiscal_{conv}"] + sum(ch[p] for p in central_parts)

        # Display and sensitivity channels.
        # Check key for (a): the CPS tax fields (federal income tax after credits, payroll tax
        # with the employer half, state income tax), per capita within the household. They omit
        # property, sales and excise taxes.
        ch["fiscal_a_cps_tax_fields"] = per_person(d, np.maximum(d.cps_tax_pc.to_numpy(float), 0), budget_mid + F_c)
        ch["wages_pretax"] = wage_delta(basis["below_ba"], central, False)
        if capped:
            # The three financing columns: cash financing and the resource cost (the capital return) by each
            # convention, the displaced beneficiaries by program; fiscal = cash + resource.
            for conv, key in keys.items():
                ch[f"fiscal_cash_{conv}"] = per_person(d, key, budget_mid + K_mid + ACC_mid + F_c)
                ch[f"fiscal_resource_{conv}"] = per_person(d, key, -K_mid)
                if accrual:
                    ch[f"fiscal_accrual_{conv}"] = per_person(d, key, -ACC_mid)
            for k in program_key:
                ch[f"displaced_{k}"] = displaced(lines=(k,))
        for conv, key in keys.items():
            ch[f"fiscal_A_only_{conv}"] = per_person(d, key, budget_mid)
            ch[f"TOTAL_{conv}_pretax_wages"] = (ch[f"fiscal_A_only_{conv}"] + ch["wages_pretax"]
                                                + sum(ch[p] for p in central_parts if p != "wages"))
            # Published September 20 band: fiscal A+F, the under-charged part of uncompensated
            # care financed by the same convention, crime on the equal footing (justice per head).
            # Its production is the published one (the same as the case's before September 29).
            ch[f"fiscal_published_{conv}"] = per_person(d, key, fiscal["published"]["A_mid"] + F_published)
            ch[f"uncomp_inside_published_{conv}"] = per_person(d, key, -(in_lo + in_hi) / 2)
        ch["crime_equal_footing"] = crime_split(keys_rank, crime_equal)
        wages_published = ch["wages"] if not prod else wage_delta(basis["below_ba"], central_published, True)
        for conv in keys:
            ch[f"TOTAL_{conv}_published_band"] = (ch[f"fiscal_published_{conv}"] + ch[f"uncomp_inside_published_{conv}"]
                                                  + wages_published + ch["renters"] + ch["landlords"]
                                                  + ch["crime_equal_footing"] + ch["unreimbursed_care"])
        tan_custody = crime_custody * crime_tangible_equal / crime_equal
        ch["crime_tangible"] = crime_split(keys_rank, tan_custody, serious_share_tan)
        ch["crime_intangible"] = ch["crime"] - ch["crime_tangible"]
        ch["crime_all_violent_key"] = per_person(d, keys_rank["violent"], -crime_custody)
        ch["crime_dollar_brackets"] = crime_split(keys_dollar, crime_custody)
        rr = np.zeros(len(d))
        for grp in ("White", "Black", "Hispanic", "Other"):
            m = race == grp
            for cls in ("serious", "simple"):
                rr += per_person(d, keys_rank[cls], -crime_custody * by_race[(grp, cls)], m)
        ch["crime_race_mix"] = rr
        ch["wages_account_split"] = wage_delta(basis["hs_or_less"], account, True)
        ch["wages_eps3"] = wage_delta(basis["below_ba"], eps3, True)
        ch["wages_short_run_pretax"] = (wage_delta(basis["below_ba"], short, False)
                                        + per_person(d, d.capital.to_numpy(float), short.capital_gain_bn))
        for (level, geo) in arms:
            ch[f"renters_{geo}_{level}"] = -spread_cells(acs[(level, geo)]["rent_cells"], R, d)
            for kname in ("intp", "scf", "mid"):
                ch[f"landlords_{kname}_{geo}_{level}"] = landlord[(level, geo)][kname]
            ch[f"owner_value_stock_{geo}_{level}"] = spread_cells(acs[(level, geo)]["value_cells"], R, d)
        qm = R_money["q5"]
        cx = np.zeros(len(d))
        for q in range(5):
            m = other & (qm == q)
            cx[m] = cex_q[q] * 1e9 / pw[m].sum()
        ch["consumer_prices_side_view"] = cx

        # Range variants: every low or every high choice, per channel, on the weighted scale.
        rng = {}
        for conv, key in keys.items():
            if capped:
                rng[f"fiscal_{conv}"] = {f"A={v:.2f}": per_person(d, key, v + D_end[j] + F_c) + displaced(j)
                                         for j, v in enumerate((adopted["A_low_cost"], adopted["A_high_cost"]))}
            else:
                rng[f"fiscal_{conv}"] = {f"A={v:.2f}": per_person(d, key, v + F_c)
                                         for v in (fiscal["adopted"]["A_low_cost"], fiscal["adopted"]["A_high_cost"])}
            # A wage scenario also moves the induced receipts; the difference from the central
            # F is financed by the same convention, so fiscal + wages stays consistent.
            rng[f"wages_{conv}"] = {lab: wage_delta(basis[s], r, True)
                                    + per_person(d, key, float(r.induced_current_receipts_bn) - F_c)
                                    for lab, (s, r) in scen.items()}
        rng["housing"] = {f"{geo}_{level}_{k}": ch[f"renters_{geo}_{level}"] + landlord[(level, geo)][k]
                          for (level, geo) in arms for k in ("intp", "scf", "mid")}
        rng["crime"] = {"envelope_low": crime_split(keys_rank, env_low),
                        "envelope_high": crime_split(keys_rank, env_high),
                        "equal_footing": ch["crime_equal_footing"], "custody_footing": ch["crime"],
                        "all_violent_key": ch["crime_all_violent_key"],
                        "dollar_brackets": ch["crime_dollar_brackets"], "race_mix": ch["crime_race_mix"]}
        rng["unreimbursed_care"] = {"low": per_person(d, priv.astype(float), -out_lo),
                                    "high": per_person(d, priv.astype(float), -out_hi)}

        # ---- gates: splits sum back to the given totals; eta = 0 equals the unweighted sum
        a_c = arms[("central", "metro_local")]
        given = {
            "fiscal_a": budget_mid + F_c, "fiscal_b": budget_mid + F_c, "fiscal_a_cps_tax_fields": budget_mid + F_c,
            "wages": P_c, "renters": -a_c["other_renters_extra_rent_bn"],
            "landlords": a_c["other_renters_extra_rent_bn"] + a_c["net_other_residents_welfare_bn"],
            "housing_net": a_c["net_other_residents_welfare_bn"], "crime": -crime_custody,
            "crime_equal_footing": -crime_equal, "crime_race_mix": -crime_custody,
            "crime_all_violent_key": -crime_custody, "crime_dollar_brackets": -crime_custody,
            "unreimbursed_care": -unreimbursed_mid, "consumer_prices_side_view": float(cex_q.sum()),
            "owner_value_stock_metro_local_central": a_c["other_owner_value_gain_stock_bn"],
            "TOTAL_a": fiscal["adopted"]["A_mid"] + F_c + P_c + a_c["net_other_residents_welfare_bn"]
            - crime_custody - unreimbursed_mid,
        }
        given["TOTAL_b"] = given["TOTAL_a"]
        if capped:
            given["displaced_beneficiaries"] = -D_mid
            for conv in keys:
                given[f"fiscal_cash_{conv}"] = budget_mid + K_mid + ACC_mid + F_c
                given[f"fiscal_resource_{conv}"] = -K_mid
                if accrual:
                    given[f"fiscal_accrual_{conv}"] = -ACC_mid
            for k, v in adopted["capped_programs"].items():
                given[f"displaced_{k}"] = -(v[0] + v[1]) / 2
        for name, tot in given.items():
            got = (pw * ch[name]).sum() / 1e9
            gate(f"sum_{measure}_{name}", np.isclose(got, tot, rtol=1e-9, atol=1e-9), split=got, given=tot)
        for name, delta in ch.items():
            gate(f"eta0_{measure}_{name}", np.isclose(weighted(delta, d, R, 0.0, CENTRAL_FLOOR),
                 (pw * delta).sum() / 1e9, rtol=1e-12, atol=1e-9))

        # ---- income frame
        for nbin, key in ((5, "q5"), (10, "q10")):
            qv, wv, yv = R[key][other], pw[other], R["y"][other]
            for q in range(nbin):
                m = qv == q
                tables["frame"].append(dict(
                    measure=measure, bins=nbin, bin=q + 1, persons_m=wv[m].sum() / 1e6,
                    households_m=d.hh_frac.to_numpy()[other][m].sum() / 1e6,
                    ybar_bin=np.average(yv[m], weights=wv[m]), y_min=yv[m].min(), y_max=yv[m].max(),
                    resources_pc_bn=(wv * d.resources_pc.to_numpy()[other])[m].sum() / 1e9,
                    money_pc_bn=(wv * d.money_pc.to_numpy()[other])[m].sum() / 1e9))
        tables["frame"].append(dict(measure=measure, bins=0, bin=0, persons_m=pw[other].sum() / 1e6,
                                    households_m=d.hh_frac.sum() / 1e6, ybar_bin=R["ybar"],
                                    y_median=R["median"], **{f"floor_{k}": v for k, v in R["floors"].items()}))
        fr = pd.DataFrame(tables["frame"])
        f5 = fr[(fr.measure == measure) & (fr.bins == 5)].sort_values("bin")
        ybar_q = f5.ybar_bin.to_numpy()
        mean_w = {}
        for eta in ETAS:
            for fl in FLOORS:
                ww = person_weights(d, R, eta, fl)
                mean_w[(eta, fl)] = float((pw * ww)[other].sum() / pw[other].sum()) if ww is not None else np.nan
            ww = person_weights(d, R, eta, CENTRAL_FLOOR)
            mq = np.bincount(R["q5"][other], weights=(pw * ww)[other], minlength=5) / (f5.persons_m.to_numpy() * 1e6)
            for q in range(5):
                tables["weights"].append(dict(measure=measure, eta=eta, quintile=q + 1,
                                              bin_weight=(ybar_q[q] / R["ybar"]) ** (-eta),
                                              mean_person_weight_p5=mq[q]))
            tables["weights"].append(dict(measure=measure, eta=eta, quintile=0,
                                          median_normalization_factor=(R["median"] / R["ybar"]) ** eta,
                                          **{f"mean_person_weight_{fl}": mean_w[(eta, fl)] for fl in FLOORS}))

        # ---- matrix, deciles, weighted totals, regressivity
        hh_q = np.bincount(R["q5"][other], weights=d.hh_frac.to_numpy()[other], minlength=5)
        persons_q = f5.persons_m.to_numpy() * 1e6
        resources_q = f5.resources_pc_bn.to_numpy()
        for name, delta in ch.items():
            q = by_bin(delta, d, R)
            tot = float(q["net"].sum())
            if not np.isclose(tot, (pw * delta).sum() / 1e9, rtol=1e-9, atol=1e-9):
                raise SystemExit(f"[BLOCKED] quintile split of {name} does not sum")
            for k in range(5):
                tables["quintile"].append(dict(
                    measure=measure, channel=name, quintile=k + 1, bn=q["net"][k], loss_bn=q["loss"][k],
                    gain_bn=q["gain"][k], usd_per_household=q["net"][k] * 1e9 / hh_q[k],
                    usd_per_person=q["net"][k] * 1e9 / persons_q[k],
                    pct_of_resources=100 * q["net"][k] / resources_q[k]))
            tables["quintile"].append(dict(
                measure=measure, channel=name, quintile=0, bn=tot, loss_bn=q["loss"].sum(), gain_bn=q["gain"].sum(),
                usd_per_household=tot * 1e9 / hh_q.sum(), usd_per_person=tot * 1e9 / persons_q.sum(),
                pct_of_resources=100 * tot / resources_q.sum()))
            q10 = by_bin(delta, d, R, 10)
            for k in range(10):
                tables["decile"].append(dict(measure=measure, channel=name, decile=k + 1, bn=q10["net"][k]))
            L, G = q["loss"].sum(), q["gain"].sum()
            tables["regress"].append(dict(
                measure=measure, channel=name, net_bn=tot, gross_loss_bn=L, gross_gain_bn=G,
                loss_share_bottom2=(q["loss"][:2].sum() / L) if L < 0 else np.nan,
                gain_share_top2=(q["gain"][3:].sum() / G) if G > 0 else np.nan,
                net_share_q1=q["net"][0] / tot if tot else np.nan, net_share_q5=q["net"][4] / tot if tot else np.nan,
                pct_resources_q1=100 * q["net"][0] / resources_q[0],
                pct_resources_q5=100 * q["net"][4] / resources_q[4]))
            for eta in ETAS:
                row = dict(measure=measure, channel=name, eta=eta, unweighted_bn=tot)
                for fl in FLOORS:
                    row[f"person_{fl}"] = weighted(delta, d, R, eta, fl)
                row["quintile_bins"] = bin_weighted(delta, d, R, eta, 5)
                row["decile_bins"] = bin_weighted(delta, d, R, eta, 10)
                row["quintile_bins_floored_p5"] = bin_weighted(delta, d, R, eta, 5, CENTRAL_FLOOR)
                row["decile_bins_floored_p5"] = bin_weighted(delta, d, R, eta, 10, CENTRAL_FLOOR)
                # Equal-split equivalent: the weighted net divided by the mean weight, i.e. the
                # total that, split equally per person, has the same weighted value. It does not
                # depend on whether weights are normalized to the mean or the median.
                for fl in FLOORS:
                    row[f"equal_split_{fl}"] = row[f"person_{fl}"] / mean_w[(eta, fl)]
                row["median_normalized_p5"] = row[f"person_{CENTRAL_FLOOR}"] * (R["median"] / R["ybar"]) ** eta
                tables["weighted"].append(row)
        # ---- percentiles: 100 person-weighted cells of other residents on this measure's ranking.
        # A binned input keeps the within-bin shape of its microdata key; it gains no resolution.
        p100 = bins(np.nan_to_num(R["p_other"][other]), 100)
        if not np.array_equal(p100 // 20, R["q5"][other]):
            raise SystemExit(f"[BLOCKED] percentiles of {measure} do not nest in its quintiles")
        wv = pw[other]
        persons_p = np.bincount(p100, weights=wv, minlength=100)
        resources_p = np.bincount(p100, weights=wv * d.resources_pc.to_numpy()[other], minlength=100) / 1e9
        ybar_p = np.bincount(p100, weights=wv * R["y"][other], minlength=100) / persons_p
        for name in PERCENTILE_CHANNELS[:-2] + ("displaced_beneficiaries",) * capped + PERCENTILE_CHANNELS[-2:]:
            x = (pw * ch[name])[other]
            net = np.bincount(p100, weights=x, minlength=100) / 1e9
            loss = np.bincount(p100, weights=np.minimum(x, 0), minlength=100) / 1e9
            if not np.allclose(net.reshape(5, 20).sum(1), by_bin(ch[name], d, R)["net"], rtol=1e-9, atol=1e-9):
                raise SystemExit(f"[BLOCKED] percentiles of {name} ({measure}) do not sum to its quintiles")
            for k in range(100):
                tables["percentile"].append(dict(
                    measure=measure, channel=name, percentile=k + 1, persons_m=persons_p[k] / 1e6,
                    ybar_bin=ybar_p[k], bn=net[k], loss_bn=loss[k], usd_per_person=net[k] * 1e9 / persons_p[k],
                    pct_of_resources=100 * net[k] / resources_p[k]))
        # A-4 treatment of victims' harm: population-average values of life and quality of life
        # are already income-weighted, so only the tangible part carries a weight; the intangible
        # part enters at face value on every scale (mean-normalized, median-normalized, equal split).
        intang = float((pw * ch["crime_intangible"]).sum() / 1e9)
        for label, base in (("crime_A4_intangible_unweighted", "crime"),
                            ("TOTAL_a_A4_crime", "TOTAL_a"), ("TOTAL_b_A4_crime", "TOTAL_b")):
            rest = ch[base] - ch["crime_intangible"]
            for eta in ETAS:
                row = dict(measure=measure, channel=label, eta=eta,
                           unweighted_bn=float((pw * ch[base]).sum() / 1e9))
                split = {}
                for fl in FLOORS:
                    wt = weighted(rest, d, R, eta, fl)
                    row[f"person_{fl}"] = wt + intang if np.isfinite(wt) else np.nan
                    split[f"equal_split_{fl}"] = wt / mean_w[(eta, fl)] + intang if np.isfinite(wt) else np.nan
                row["quintile_bins"] = bin_weighted(rest, d, R, eta, 5) + intang
                row["decile_bins"] = bin_weighted(rest, d, R, eta, 10) + intang
                row["quintile_bins_floored_p5"] = bin_weighted(rest, d, R, eta, 5, CENTRAL_FLOOR) + intang
                row["decile_bins_floored_p5"] = bin_weighted(rest, d, R, eta, 10, CENTRAL_FLOOR) + intang
                row.update(split)
                wt = weighted(rest, d, R, eta, CENTRAL_FLOOR)
                row["median_normalized_p5"] = wt * (R["median"] / R["ybar"]) ** eta + intang
                if eta == 0:
                    gate(f"eta0_{measure}_{label}", np.isclose(row[f"person_{CENTRAL_FLOOR}"], row["unweighted_bn"],
                                                              rtol=1e-12, atol=1e-9))
                tables["weighted"].append(row)
        # Ranges, stacked on the weighted scale at every eta.
        for eta in ETAS:
            for conv in keys:
                lo = hi = 0.0
                parts = {}
                for grp in (f"fiscal_{conv}", f"wages_{conv}", "housing", "crime", "unreimbursed_care"):
                    vals = {lab: weighted(v, d, R, eta, CENTRAL_FLOOR) for lab, v in rng[grp].items()}
                    unw = {lab: float((pw * v).sum() / 1e9) for lab, v in rng[grp].items()}
                    kmin, kmax = min(vals, key=vals.get), max(vals, key=vals.get)
                    parts[grp] = (vals[kmin], kmin, unw[kmin], vals[kmax], kmax, unw[kmax])
                    lo += vals[kmin]
                    hi += vals[kmax]
                    tables["ranges"].append(dict(measure=measure, eta=eta, convention=conv, group=grp,
                                                 most_costly_weighted=vals[kmin], most_costly_variant=kmin,
                                                 most_costly_unweighted=unw[kmin], least_costly_weighted=vals[kmax],
                                                 least_costly_variant=kmax, least_costly_unweighted=unw[kmax],
                                                 most_costly_equal_split=vals[kmin] / mean_w[(eta, CENTRAL_FLOOR)],
                                                 least_costly_equal_split=vals[kmax] / mean_w[(eta, CENTRAL_FLOOR)]))
                tables["ranges"].append(dict(measure=measure, eta=eta, convention=conv, group="TOTAL",
                                             most_costly_weighted=lo, least_costly_weighted=hi,
                                             most_costly_unweighted=sum(p[2] for p in parts.values()),
                                             least_costly_unweighted=sum(p[5] for p in parts.values()),
                                             most_costly_equal_split=lo / mean_w[(eta, CENTRAL_FLOOR)],
                                             least_costly_equal_split=hi / mean_w[(eta, CENTRAL_FLOOR)]))

    fr = pd.DataFrame(tables["frame"])
    fr.to_csv(out_dir / "income_frame.csv", index=False)
    pd.DataFrame(tables["quintile"]).to_csv(out_dir / "channel_by_quintile.csv", index=False)
    pd.DataFrame(tables["decile"]).to_csv(out_dir / "channel_by_decile.csv", index=False)
    pd.DataFrame(tables["percentile"]).to_csv(out_dir / "channel_by_percentile.csv", index=False)
    pd.DataFrame(tables["weighted"]).to_csv(out_dir / "weighted_totals.csv", index=False)
    pd.DataFrame(tables["regress"]).to_csv(out_dir / "regressivity.csv", index=False)
    pd.DataFrame(tables["weights"]).to_csv(out_dir / "weights.csv", index=False)
    pd.DataFrame(tables["ranges"]).to_csv(out_dir / "ranges_weighted.csv", index=False)
    rq = []
    for (level, geo) in arms:
        a = acs[(level, geo)]
        for k in range(5):
            rq.append(dict(level=level, geography=geo, acs_quintile=k + 1, extra_rent_bn=a["rent_q5"][k] / 1e9,
                           renter_households_m=a["renter_households_q5"][k] / 1e6,
                           usd_per_renter_household=a["rent_q5"][k] / a["renter_households_q5"][k]))
    pd.DataFrame(rq).to_csv(out_dir / "rent_per_renter_household_acs.csv", index=False)
    wages = []
    for lab, (s, r) in scen.items():
        wages.append(dict(scenario=lab, split=s, sigma=float(r.sigma), eps=float(r.sigma_NI),
                          P_after_tax_bn=float(r.native_production_gain_bn + r.other_immigrant_production_gain_bn),
                          F_induced_receipts_bn=float(r.induced_current_receipts_bn),
                          pretax_bn=float((pw * wage_delta(basis[s], r, False)).sum() / 1e9),
                          native_cell0_pct=float(-r.wage_pct_native_cell0), native_cell1_pct=float(-r.wage_pct_native_cell1)))
    wages.append(dict(scenario="short_run_below_ba_s2.0", split="below_ba", sigma=2.0, eps=np.inf,
                      pretax_bn=float((pw * wage_delta(basis["below_ba"], short, False)).sum() / 1e9),
                      capital_gain_bn=float(short.capital_gain_bn)))
    pd.DataFrame(wages).to_csv(out_dir / "wage_scenarios.csv", index=False)

    inputs = dict(
        fiscal=fiscal, federal_taxes_2024_bn=F_total, state_local_taxes_2024_bn=S_total,
        production=dict(central_P=P_c, central_F=F_c, account_P_plus_F=float(account.private_plus_receipts_bn)),
        crime=dict(equal_footing=crime_equal, custody_footing=crime_custody, tangible_equal=crime_tangible_equal,
                   envelope=[env_low, env_high], serious_share=serious_share,
                   victim_race_shares={f"{k[0]}|{k[1]}": float(v) for k, v in by_race.items()}),
        ncvs=dict(pooled_violent=rates["violent"].round(3).tolist(), pooled_serious=rates["serious"].round(3).tolist(),
                  pooled_simple=rates["simple"].round(3).tolist(), pooled_persons=rates["pops"].tolist(),
                  bracket_cum_share=rates["cum"].round(4).tolist(), cps_bracket_share_12plus=bracket_share,
                  verified_against_text=ncvs_verified),
        unreimbursed_care=dict(outside_low=out_lo, outside_high=out_hi, outside_mid=unreimbursed_mid,
                               inside_low=in_lo, inside_high=in_hi),
        consumer_prices_side_view_q=cex_q.round(4).tolist(),
        acs=acs["acs_checks"], scf=scf_info, tax_spm=notes["tax_spm"], tax_money=notes["tax_money"],
        housing={f"{k[0]}|{k[1]}": dict(renters=v["other_renters_extra_rent_bn"],
                                        net=v["net_other_residents_welfare_bn"],
                                        owners_stock=v["other_owner_value_gain_stock_bn"])
                 for k, v in arms.items()})
    if prod:
        # September 29 on: the case's production scenarios are on row-4 weights; A moved by the case's change less the
        # change in the engine's P + F at each band end (fiscal.adopted.production).
        acct_pub = pick(nest, "hs_or_less", 2.0, 1.0, np.inf)
        inputs["production"].update(
            case_weights=prod_info,
            published=dict(central_P=float(central_published.native_production_gain_bn
                                           + central_published.other_immigrant_production_gain_bn),
                           central_F=F_published, account_P_plus_F=float(acct_pub.private_plus_receipts_bn)),
            engine_change_P_plus_F_at_band_ends_bn=adopted["production"]["change_P_plus_F_bn"])
    if capped:
        # Welfare signs (a cost is negative); cash + resource + displaced = A + F at each band end.
        inputs["financing_columns"] = {end: dict(
            cash_financing_bn=a + D_end[j] + adopted["capital_return"][j] + (accrual[j] if accrual else 0.0) + F_c,
            resource_cost_bn=-adopted["capital_return"][j],
            resource_cost_federal_bn=-adopted["capital_return_by_level"]["federal"][j],
            displaced_beneficiaries_bn=-D_end[j], **({"pension_accrual_bn": -accrual[j]} if accrual else {}),
            A_plus_F_bn=a + F_c)
            for j, (end, a) in enumerate((("low_cost_end", adopted["A_low_cost"]), ("high_cost_end", adopted["A_high_cost"])))}
        housing = "housing_enterprise_surplus" in adopted["capped_programs"]
        inputs["capped_programs"] = dict(
            rule=("rental assistance, public housing's enterprise deficit (rental assistance's key) and LIHEAP"
                  if housing else "rental assistance and LIHEAP")
                 + " fall on their eligible non-recipients among other residents, equal per "
                 "household, under both financing conventions; TANF-type aid (a block grant) stays with the budget",
            rental_assistance="renter households paying cash rent (H_TENURE 2), money income below 50% of the state's "
                              "median household money income (CPS ASEC 2025), neither HPUBLIC nor HLORENT; HUD's "
                              "very-low-income rule, 24 CFR 5.603 and 982.201(b), without its family-size adjustment",
            liheap="households with money income below 150% of the 2024 HHS poverty guideline for their size "
                   "(89 FR 2961), no energy assistance (HENGAST); 42 U.S.C. 8624(b)(2)(B)(i), without the 60% of "
                   "state median income alternative",
            amounts_at_band_ends_bn=adopted["capped_programs"], block_grant_at_band_ends_bn=adopted["block_grant"],
            texts_sha256=capped_texts, **capped_info)
    (out_dir / "inputs.json").write_text(json.dumps(inputs, indent=1, default=float))
    (out_dir / "gates.json").write_text(json.dumps(GATES, indent=1, default=float))
    manifest = [dict(file=str(p.relative_to(HERE)), bytes=p.stat().st_size, sha256=sha(p))
                for p in sorted(SOURCES.glob("*")) if p.is_file() and p.suffix in (".pdf", ".txt", ".zip", ".html")]
    pd.DataFrame(manifest).to_csv(out_dir / "sources_manifest.csv", index=False)
    print(f"{sum(g['passed'] for g in GATES.values())} gates passed")


if __name__ == "__main__":
    main()
