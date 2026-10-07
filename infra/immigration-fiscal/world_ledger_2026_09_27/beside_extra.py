"""Beside arms, part 2 (2026-10-07, the lead's specs from the operator's questions): the premium's other readings (arms
1a-1c), the services' price basis (arm 3), the fiscal dollar's alternative use (arm 4), output at common prices (arm
5), the group's private gain on wages alone, and three stacked readings, on the world ledger's oct07 central, lineage
basis (42,752,213 members), beside beside_arms.py's arms. Each arm swaps one input of the central and is shown alone;
the readings stack them. None replaces a central input, and no reading is a new central.

Arm 1, the place premium (G1 and G2; G3+ at its zero bound throughout).
  1a. Mexican cells computed directly on the ENIGH 2024 persons in localities of 100,000+ (tam_loc 1: mexico.py's
      cells and young-by-parent tables on that subset), G2's schooling from the ESRU-EMOVI 2017 respondents who lived
      in a city of 100,000+ at 14, Mexican pay at household-consumption PPP (WDI 2024 PA.NUS.PRVT.PP, 10.80) instead
      of GDP PPP (9.92), CMP selection p56. Its parts: the urban cells alone, consumption PPP alone. Beside: Mexico
      City's cells (entidad 09; EMOVI residence at 14 there) at either PPP; the urban cells at CMP's p70 (the
      operator's best job in Mexico); urban pay divided by beside_arms.py's hedonic price level of localities of
      100,000+ (the research's recommendation, once a price ratio was sourced).
  1b. CMP's Re 2.46 as G1's annual US/Mexico ratio.
  1c. Within person, Hendricks and Schoellman (2018), Table II: G1's Mexican pay is E_US / r on the central row of
      each G1 convention, every row of the convention scaled by the same factor [ASSUMPTION: proportional; take-home
      pay and both Mexican taxes with it]. r 2.0 (the Mexican Migration Project, an hourly gain, read as annual) and
      1.8 (the NIS bin that holds Mexico), and both per person at the lane's own hours and employment, r / (H_MX /
      H_US) with H the employment rate times weekly hours of the central row (1.59 and 1.43). No CMP selection on
      top: the comparison holds the person fixed. The MMP sample is mostly return migrants observed in Mexico, and
      the pre-migration job is the actual one, often rural, not the best alternative. G2 keeps the rearing model,
      which Lagakos and Schoellman (2026) support for people raised in the US.
Arm 2, US regional prices: beside_arms.py's state RPP on each record's US earnings.
Arm 3, the services' price basis.
  3. US-price numeraire (recommended): Mexico's services forgone by the group, and the budget Mexico saves, at ICP
     2021 category PPPs instead of GDP PPP: health / 0.8137 (actual health), other government consumption / 0.5994
     (collective government), cash transfers and pensions at private-consumption PPP (x 9.9166 / 10.8013, WDI 2024,
     as pay); schooling stays at GDP PPP (ICP's education PPP, 0.166 of GDP PPP, is input-priced [UNVERIFIED as
     quality-equal]). US services stay at US cost times V/G. Check: the group's rows only, Mexico's budget saved at
     GDP PPP (the research's version).
  3a, 3b: beside_arms.py's: US health and social services at Mexican relative prices; public goods at their
     responsive cost [FRAMING-SENSITIVE: a non-rival good's value to its users is not its marginal cost].
  Mexican-price numeraire (the research's rule, extended to G2 and G3+): 3a, plus US public goods and justice at V
     x 0.5994, SNAP at V x 1.7631 (ICP food over GDP PPP) and cash at V x 1.0892 (WDI 2024 private-consumption PPP
     over GDP PPP); enterprise services and housing stay at US cost [ASSUMPTION: their ICP categories are not
     staged; the research puts housing at -$0.2bn for G1].
Arm 4, the fiscal dollar's alternative use: theta in place of lambda. Under the lane's lambda columns other residents'
   fiscal rows (fiscal_others, fiscal_future, induced_receipts) and Mexico's budget rows carry lambda per $1, the
   pension accrual and displaced beneficiaries $1 (world_ledger.row_weight). theta replaces lambda with what the
   dollar would otherwise do, as other residents value it:
   - state and local (the fiscal gap's state-local part, and the capital return less its federal part): a share s is
     re-spent, at m, the MVPF of marginal spending; the rest goes back as tax cuts, at lambda;
   - federal, borrowed (fiscal_future: the winners lane's FY2024 deficit share b of the federal part): lambda, for
     the later taxes, plus crowd-in d (SPC - 1);
   - federal, the rest (and the capital return's federal part): half spent at m, half tax cuts at lambda
     [ASSUMPTION; the research flags this 50/50 split and the average-share composition behind m as its weakest
     inputs]; under current-law scoring, at the borrowed rate.
   The parts are the case's own (debt_legacy_2026_09_23 federal_split_2024.csv, oct07, the mean of the band ends, as
   the ledger's central), so theta is one number for others today (theta_o) and one for future taxpayers (theta_f).
   Mexico's budget rows take theta_o, as they take lambda [ASSUMPTION]. The lambda columns are linear in those rows,
   so each party's lambda rows are S = (W_1.16 - W_equal) / 0.16 and W_theta = W_equal + (theta - 1) S; gates
   recompute the lambda 1.5 and lambda_h columns that way and compare with a direct evaluation. theta and lambda do
   not stack: lambda is the cost of raising the dollar, theta what the dollar would have done, lambda inside it.
   Central: s 0.60, m 0.967, lambda 1.25, d 0.33, SPC 1.1. Variants: lambda 1 (the alternative use alone), m 0.6875
   (the operator's waste point), m 1.317 (K-12 at MVPF 2), s 0.40 (Ladd's own-revenue windfall), current-law scoring,
   the waste point at lambda 1, and a labelled extreme, m 2.58 (K-12 and higher education at 5).
Arm 5, output at common prices [FRAMING-SENSITIVE: it values output at common prices, a different question from the
   migrant's purchasing power, for which consumption PPP stays right]. G1's and G2's E_US by the industry of the
   longest job last year (CPS ASEC 2025 INDUSTRY, 2022 census codes) in nine classes; the Mexican counterfactual's
   earnings split in the same shares [ASSUMPTION: ENIGH's cells are not industry-matched] and re-priced at the
   class's ICP 2021 category PPP instead of GDP PPP: E_MX x F, F = sum of share x GDP PPP / category PPP. Restaurants
   and hotels at 1111000; personal and household services, services to buildings, landscaping, social assistance and
   private households at actual miscellaneous goods and services, 9140000 [ASSUMPTION; furnishings and household
   maintenance, 1105000, is the alternative]; health at actual health, 9080000; retail at household consumption
   without housing, 9260000 [ASSUMPTION]; goods and every other class at GDP PPP. Variant: agriculture at food
   (1101100), construction at 1501200 and manufacturing at machinery and equipment (1501100) too.
The private gain on wages alone, per generation, in total, per member and per G1 adult: (a) the premium, less the US
   taxes the group pays (valuation_by_generation's tax class at cost, the mean of the band ends), plus the Mexican
   taxes it avoids (mexico_taxes_avoided), less Mexico's services forgone as valued (mexico_budget_lost); every US
   service and benefit at zero; remittances left out (they are the group's own spending). (b) (a) plus the old-age
   promises the members earn: the Social Security accrual (the social_security line) and Part A (the pension lane's
   Part A per HI tax dollar by generation, item pension_tr2026's arm, times the generation's HI taxes
   [ASSUMPTION]). US taxes stay nominal under arm 2. A reading with arm 5 takes its private gain from its
   consumption-PPP twin.
Readings. 1, recommended (research section 8): 1a + 2 + 3; with 1a deflated beside. 2, the operator's framing: the
   urban cells at p70 + 2 + 5 + 3a + 3b; its twin at consumption PPP in place of 5. 3, within person: reading 1 with
   G1 at 1c's 1.59; at 2.0 beside. Combined low: reading 2 with G1 at 1c's 1.59. Where arm 2 meets 1c, G1's Mexican
   pay is the nominal E_US / r: Hendricks and Schoellman's ratio is of pay where the migrant lives.

Gates: the staged sources' sha256; the central equals world_ledger_oct07.csv; the cells computed on every ENIGH person
equal mexico.py's, and the premium table on them g2_premium_lineage.csv; the identities (the central rows relabelled to
themselves, the lane's own ratio, F = 1, factors of 1, every share at lambda) reproduce the central; arms 2, 3a and 3b
equal beside_arms_oct07.csv; theta's post-processing equals a direct evaluation; the group's industry codes are on the
2022 list, whose sector ranges are the classes'.

Run from the repository root, after beside_arms.py (it reads derived/beside_arms_oct07.csv, its summary and its meta's
price level):
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/beside_extra.py
Outputs (derived/): beside_extra_oct07.csv (scenario x weighting x party), beside_extra_summary_oct07.csv,
beside_extra_private_gain_oct07.csv, beside_extra_industry_oct07.csv, beside_extra_meta_oct07.json.
"""
import json
import re
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd

import beside_arms as B
import g2_premium as G
import mexico as MX
import world_ledger as W

DERIVED, REPO, STAGE, CASE, BASIS, MEMBERS = B.DERIVED, B.REPO, B.STAGE, B.CASE, B.BASIS, B.MEMBERS
# Staged with an ACQUIRED.md beside each (acquire_beside.py fetches a missing one): path, sha256, URL.
EXTRA_SOURCES = {
    "icp2021_categories": (STAGE / "worldbank/icp2021/icp2021_mex_usa_categories.json",
                           "8f72455908f3cd249acf14909e0a5d4105312c700268aa53ba703d3ea0aa2bdb",
                           "https://api.worldbank.org/v2/sources/90/country/MEX;USA/series/1111000;1105000;9140000;"
                           "9260000;9100000;1101100;1501100;1501200;9110000/classification/PPPGlob;PX.WL;EXR/time/"
                           "YR2021/data?format=json&per_page=500"),
    "census_industry_2022": (STAGE / "census/industry_codes_2022/2022-Census-Industry-Code-List-with-Crosswalk.xlsx",
                             "c9d2e004b2735c3975f0768e7dac704df6d2e0b36b24d33f5dbc7109cab5628c",
                             "https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/"
                             "2022-Census-Industry-Code-List-with-Crosswalk.xlsx"),
}
SPLIT = REPO / "infra/immigration-fiscal/debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv"
SPLIT_PROFILE = "long_run_non_school_full"     # the main case's profile in the debt lane (its oct07 summary)
CASE_SET = (389.082553, 461.479709)            # main case v6, low / high (main_case_2026_10_07 summary.json)
PENSION_ARMS = REPO / "infra/immigration-fiscal/pension_tr2026_2026_10_06/derived/arms.csv"
PENSION_ARM = "all_2026_inputs_separate_funds"  # item pension_tr2026 of main case v6: 2026 Trustees, OASI and DI apart
GENERATION_RESULTS = REPO / "infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results_oct07.csv"
# The MVPF of a marginal state-local dollar: composition [TRAINING-DATA: Census state-local direct expenditure shares]
# times values from Hendren and Sprung-Keyser's Table II (reads/hendren_sprung_keyser_2020.md): K-12's two rows
# straddle 1 (Jackson et al. infinite, Michigan 0.65), so it is valued at cost; the adult-health category is 0.89
# [0.56, 1.57]; higher education and the rest (safety, roads, other) have no MVPF here and are valued at cost.
COMPOSITION = dict(k12=0.25, higher_education=0.10, health=0.30, other=0.35)
MVPF_VALUES = {
    "central": dict(k12=1.0, higher_education=1.0, health=0.89, other=1.0),
    # Michigan's K-12 row, health near the bottom of the adult-health interval, the rest at 0.70 [ASSUMPTION]
    "waste": dict(k12=0.65, higher_education=1.0, health=0.60, other=0.70),
    "education_2": dict(k12=2.0, higher_education=2.0, health=0.89, other=1.0),
    # A labelled extreme: schooling at the child programs' average (about 5), health at the top of its interval.
    "education_5": dict(k12=5.0, higher_education=5.0, health=1.60, other=1.0),
}
# Re-spent share of a released state-local dollar: the flypaper range, "a $1 grant increases the spending of the local
# agency by 25 cents; the high-end estimates are clustered around unity" (Hines and Thaler 1995, JEP 9(4), p. 219);
# 0.60 is its midpoint [INFERENCE]. The closest case to a released cost there, Ladd (1993): "for every $100 of higher
# state taxes generated by the changing federal definitions of income in the 1986 Tax Reform Act, state income tax
# collections rose by $40", a 0.40 variant [SOURCE: reads/hines_thaler_1995.md quotes 3 and 5].
# Crowd-in of a dollar less federal borrowing: d = 0.33 of it would have gone to private investment [TRAINING-DATA:
# CBO's rule of thumb, range 0.15-0.50], at the shadow price of capital 1.1: "a central SPC value of 1.1, with a
# reasonable range of 1.1 to 1.2" [SOURCE: reads/newell_pizer_prest_2023.md quote 1].
# lambda 1.25 for the tax-cut shares, between the lane's 1.16 and lambda_h (1.286) [ASSUMPTION: the lead's research
# note of 2026-10-07 takes 1.25, range 1.10-1.50].
BASE_THETA = dict(s=0.60, mvpf="central", lam=1.25, f=0.5, d=0.33, spc=1.1, current_law=False)
THETA_SETS = {
    "theta_central": {},
    "theta_alt_use": dict(lam=1.0),
    "theta_waste": dict(mvpf="waste"),
    "theta_education_2": dict(mvpf="education_2"),
    "theta_ladd": dict(s=0.40),
    "theta_current_law": dict(current_law=True),
    "theta_waste_alt_use": dict(mvpf="waste", lam=1.0),
    "theta_education_5_extreme": dict(mvpf="education_5"),
}
THETA_SETS = {k: dict(BASE_THETA, **v) for k, v in THETA_SETS.items()}
THETA_LABELS = dict(theta_central="theta, central", theta_alt_use="theta at lambda 1: the alternative use alone",
                    theta_waste="theta, the waste point (m 0.6875)", theta_education_2="theta, K-12 at MVPF 2 (m 1.317)",
                    theta_ladd="theta, re-spent share 0.40 (Ladd)",
                    theta_current_law="theta, current-law scoring (all federal at the borrowed rate)",
                    theta_waste_alt_use="theta, the waste point at lambda 1",
                    theta_education_5_extreme="theta, extreme: schooling at MVPF 5 (m 2.58)")
# mcpf's reconciliation (scratch mix_sens.py): its borrowed share, FY2024 deficit over outlays (OMB Historical Table
# 1.1 via the FAQ's entry 20, $1.83tn of $6.75tn), its crowd-in d (SPC - 1) = 0.033.
MCPF_BORROWED = 1.83 / 6.75
# Beside arm 4, in no total, with mcpf's formulas at each band end (scratch spc_calc.py, mix_calc.py). The shadow price
# of capital on the share of each part that displaces domestic investment, d (SPC - 1): state and local (with its
# displaced part) d = the payers' saving share (0.07-0.22, world_ledger.MSS_SAVING) x 0.58, the domestic share of a
# change in national saving (CBO, Huntley 2014: 33 of 57 cents), 0.04-0.13, central 0.08; federal (with its displaced
# part) 0.15-0.50, central 0.33 (CBO); the accrual 0 (to 0.08: benefit cuts, not taxes); the capital return 0 (already
# the opportunity cost of public capital); SPC 1.1, range 1.0-1.2 [SOURCE: the lead's researcher's note of 2026-10-07,
# F3-F4; reads/newell_pizer_prest_2023.md quote 1]. The policy arm: the federal half re-spent (mcpf's base) going to
# nondefense R&D at a marginal social benefit-cost ratio of 3.7-11.4 (Jones and Summers 2020, Table 7) instead of m
# [UNVERIFIED: through the same note; FRAMING-SENSITIVE: no budget rule sends the savings to research].
DISPLACED_SHARE = dict(state_local=(0.04, 0.08, 0.13), federal=(0.15, 0.33, 0.50), accrual=(0.0, 0.0, 0.08))
SPC_RANGE = (1.0, 1.1, 1.2)
RD_BCR = (3.7, 11.4)
# Hendricks and Schoellman (QJE 2018; accepted manuscript of 10 October 2017), Table II, hourly wage gain at
# migration: Mexican Migration Project 2.0 (GDP gap 2.9), the NIS bin whose most sampled countries are Mexico, Poland
# and Russia 1.8 (gap 3.0); "immigrants from Mexico are roughly unselected" (p. 21) [SOURCE:
# reads/hendricks_schoellman_2018.md]. Clemens, Montenegro and Pritchett's Re 2.46
# (reads/clemens_montenegro_pritchett_2009.md quote 3).
SAME_PERSON = {   # r, per hour (converted at the lane's hours and employment), arm, label
    "arm1b_cmp_re": (G.CMP_RE, False, "1b", "G1 at CMP's Re 2.46 as a year's ratio"),
    "arm1c_mmp_annual": (2.0, False, "1c", "G1 at MMP's 2.0, read as a year's ratio"),
    "arm1c_mmp_per_person": (2.0, True, "1c", "G1 at MMP's 2.0 an hour, per person at the lane's hours and employment"),
    "arm1c_nis_annual": (1.8, False, "1c", "G1 at the NIS bin's 1.8, read as a year's ratio"),
    "arm1c_nis_per_person": (1.8, True, "1c", "G1 at the NIS bin's 1.8 an hour, per person at the lane's hours"),
}
# Their Table II, Mexican MP: hourly wage before migration $2.96 (PWT 7.1 PPP) and after $6.04, 2003 US dollars; MMP's
# Mexicans have 7.1 years of schooling, 60% without high school (p. 23) [SOURCE: reads/hendricks_schoellman_2018.md
# quotes 1 and 5]. CPI-U (FRED CPIAUCSL, annual) 2003 184.000, 2024 313.698 [DATA:
# selection_curve_2026_09_27/_cache/cpiaucsl_annual.csv].
HS_MMP_WAGES_2003 = dict(pre=2.96, post=6.04)
CPI_2003, CPI_2024 = 184.000, 313.698
# ICP 2021 series (World Bank source 90) beyond beside_arms.py's: arm 5's categories and the Mexican numeraire's food.
ICP_FOOD = "1101100"
# Arm 5's classes: (class, census industry code ranges of the 2022 list, ICP series in arm 5, ICP series in its
# goods variant); None is GDP PPP. Codes in no class are 'others' (GDP PPP).
CLASSES = (
    ("agriculture", ((170, 290),), None, "1101100"),
    ("mining", ((370, 490),), None, None),
    ("construction", ((770, 770),), None, "1501200"),
    ("manufacturing", ((1070, 3990),), None, "1501100"),
    ("restaurants_hotels", ((8660, 8690),), "1111000", "1111000"),
    ("personal_household", ((8970, 9090), (9290, 9290), (7690, 7690), (7770, 7770), (8370, 8470)), "9140000",
     "9140000"),
    ("health", ((7970, 8290),), "9080000", "9080000"),
    ("retail", ((4670, 5791),), "9260000", "9260000"),
)
GOODS = ("agriculture", "mining", "construction", "manufacturing")
# The 2022 list's sector rows that bound the classes, (title, range) [SOURCE: the list's sheet "2022 Census Ind Code
# List "]; 9890, in the CPS file but not on the list, goes to 'others'.
SECTOR_RANGES = {"Agriculture, Forestry, Fishing and Hunting": (170, 290),
                 "Mining, Quarrying, and Oil and Gas Extraction": (370, 490), "Manufacturing": (1070, 3990),
                 "Retail Trade": (4670, 5791), "Health Care and Social Assistance": (7970, 8470),
                 "Accommodation and Food Services": (8660, 8690),
                 "Other Services, Except Public Administration": (8770, 9290)}
OFF_LIST = {9890}
LAMBDA_COLS = {"equal_lambda_1.16": 1.16, "equal_lambda_1.5": 1.5}
PARTY_THETA = dict(others_today="o", future_taxpayers="f", mexico_residents="o")
MONEY_COLS = ("mexico_earnings_bn", "mexico_take_home_bn", "mexico_withheld_tax_bn", "mexico_consumption_tax_bn")
KEYS = ["generation", "convention", "ppp", "diploma_reread", "mishra", "selection"]
CELL_MONEY = ("inc", "net", "tax", "ctax")
# HI's part of the self-employment tax (15.3%: OASDI 12.4, HI 2.9).
SE_HI_SHARE = 2.9 / 15.3
# Readings whose world total uses arm 5 take their private gain from the twin at consumption PPP.
PRIVATE_GAIN_TWIN = {"reading2": "reading2_consumption", "combined_low": "combined_low_consumption"}
SHOW_THETA = ("theta_central",)


def gate(name, ok, **detail):
    B.gate(name, ok, **detail)


def check_sources():
    out = B.check_sources()
    for k, (p, sha, url) in EXTRA_SOURCES.items():
        gate(f"source_{k}_present", p.is_file(), path=str(p), fetch="acquire_beside.py")
        got = B.sha256(p)
        gate(f"source_{k}_sha256", got == sha, path=str(p), got=got)
        out[k] = dict(path=str(p.relative_to(REPO)), sha256=sha, bytes=p.stat().st_size, url=url)
    return out


def icp_values():
    icp = {}
    for p in (B.SOURCES["icp2021"][0], EXTRA_SOURCES["icp2021_categories"][0]):
        for x in json.load(open(p))["source"]["data"]:
            v = {y["concept"]: y["id"] for y in x["variable"]}
            icp[(v["Country"], v["Series"], v["Classification"])] = x["value"]
    us = [v for (c, _, k), v in icp.items() if c == "USA" and k == "PPPGlob"]
    gate("icp_us_ppps_are_1", len(us) > 0 and all(v == 1 for v in us), us=us)
    gdp = icp[("MEX", B.ICP_GDP, "PPPGlob")]
    return {s: v / gdp for (c, s, k), v in icp.items() if c == "MEX" and k == "PPPGlob"}, gdp


# ------------------------------------------------------------------ arm 1: Mexican cells on a subset of persons
def cells_dicts(c, y):
    """g2_premium.mexico_cells' lookup tables for both PPPs from a cells table and a young-by-parent table."""
    out = {}
    for ppp in ("gdp", "consumption"):
        cols = dict(inc=f"gross_per_person_ppp_{ppp}", net=f"income_per_person_ppp_{ppp}",
                    tax=f"withheld_per_person_ppp_{ppp}", ctax=f"ctax_per_person_ppp_{ppp}", emp="employment_rate",
                    hrs="weekly_hours_employed")
        o = {k: {(r.sex, r.band, r.cat): getattr(r, col) for r in c.itertuples()} for k, col in cols.items()}
        o.update({f"y{k}": {(r.sex, r.band, r.parent_cat): getattr(r, col) for r in y.itertuples()}
                  for k, col in cols.items()})
        out[ppp] = o
    return out


def subset_cells(en, mask, rates):
    """mexico.py's cells and young-by-parent table on a subset of ENIGH persons, as mexico.py writes them (%.6g)."""
    s = en[mask]
    c = MX.cells(s)
    MX.add_ppp(c, rates)
    y = MX.young_by_parent(s, rates)
    return cells_dicts(B.as_written(c), B.as_written(y)), dict(persons_15plus_m=float(c.persons.sum() / 1e6),
                                                                records_15plus=int(c.n.sum()))


def same_cells(a, b):
    if a.keys() != b.keys():
        return False
    for k in a:
        if a[k].keys() != b[k].keys():
            return False
        x = np.array([a[k][j] for j in a[k]], float)
        z = np.array([b[k][j] for j in a[k]], float)
        if not np.array_equal(x, z, equal_nan=True):
            return False
    return True


def deflate(cells, P):
    """Every money lookup divided by a price level; employment and hours as they are."""
    return {ppp: {k: ({j: v / P for j, v in t.items()} if k.lstrip("y") in CELL_MONEY else t) for k, t in c.items()}
            for ppp, c in cells.items()}


def recompute(t, m):
    t.loc[m, "gain_bn"] = t.loc[m, "us_earnings_bn"] - t.loc[m, "mexico_earnings_bn"]
    t.loc[m, "gain_per_person"] = t.loc[m, "gain_bn"] * 1e3 / t.loc[m, "persons_m"]
    t.loc[m, "ratio_us_to_mexico"] = t.loc[m, "us_earnings_bn"] / t.loc[m, "mexico_earnings_bn"]


def table_gate(name, a, b):
    """Two premium tables agree: the money columns to 1e-9 ($bn), the gain, written to 6 significant digits and
    recomputed here from the money columns, to 2e-3."""
    cols = list(MONEY_COLS) + ["us_earnings_bn"]
    money = B.max_diff(a[cols].to_numpy(float).ravel(), b[cols].to_numpy(float).ravel())
    gain = B.max_diff(a.gain_bn, b.gain_bn)
    gate(name, len(a) == len(b) and money < 1e-9 and gain < 2e-3, money=money, gain=gain)


def with_central(tab, ppp="gdp", g1_sel="p56"):
    """The premium table with the rows world_ledger.premium_rows reads as central (G1 at GDP PPP and p56; G2's rearing
    rows at GDP PPP) holding the values of the given PPP's rows and G1 selection; every other row unchanged."""
    t = tab.copy()
    num = [c for c in t.columns if c not in KEYS and pd.api.types.is_numeric_dtype(t[c])]

    def put(gen, conv, sel_to, sel_from):
        base = (t.generation == gen) & (t.convention == conv) & ~t.mishra & (t.diploma_reread == 0.25)
        to, fr = base & (t.ppp == "gdp") & (t.selection == sel_to), base & (t.ppp == ppp) & (t.selection == sel_from)
        gate(f"with_central_rows_{gen}_{conv}_{sel_to}", int(to.sum()) == 1 and int(fr.sum()) == 1,
             n=[int(to.sum()), int(fr.sum())])
        t.loc[to, num] = t.loc[fr, num].to_numpy()

    for conv in ("own_schooling_all_ages", "own_schooling_25_64_arrived_20plus"):
        put("G1", conv, "p56", g1_sel)
    for sel in ("all", "none"):
        put("G2", "rearing", sel, sel)
    return t


def central_row(t, conv):
    c = t[(t.generation == "G1") & (t.convention == conv) & (t.ppp == "gdp") & (t.selection == "p56") & ~t.mishra
          & (t.diploma_reread == 0.25)]
    gate(f"one_central_row_{conv}", len(c) == 1, n=len(c))
    return c.iloc[0]


def annual_ratio(tab0, r, per_hour):
    """The ratio as a year's earnings per person, by G1 convention: per hour, r / (H_MX / H_US), H the employment rate
    times weekly hours of those 15+ on the lane's central row."""
    out = {}
    for conv in tab0[tab0.generation.eq("G1")].convention.unique():
        c = central_row(tab0, conv)
        h = (c.employment_mx_15plus * c.weekly_hours_mx_workers) / (c.employment_us_15plus * c.weekly_hours_us_workers)
        lane = float(c.us_earnings_bn / c.mexico_earnings_bn)
        out[conv] = dict(r_annual=r / h if per_hour else r, hours_employment_mx_over_us=float(h),
                         lane_ratio_annual=lane, lane_ratio_hourly=lane * float(h))
    return out


def same_person(tab, ratios, e_us_nominal):
    """G1's Mexican pay at the nominal E_US / r_annual on each convention's central row, every row of the convention
    scaled by the same factor (the selection, PPP and other rows keep their relation to it)."""
    t = tab.copy()
    info = {}
    for conv, s in t[t.generation.eq("G1")].groupby("convention"):
        gate(f"g1_{conv}_one_diploma_reread", set(s.diploma_reread) == {0.25})
        c = central_row(t, conv)
        k = e_us_nominal[conv] / ratios[conv]["r_annual"] / c.mexico_earnings_bn
        m = t.index.isin(s.index)
        for col in MONEY_COLS:
            t.loc[m, col] = t.loc[m, col] * k
        recompute(t, m)
        info[conv] = dict(ratios[conv], factor=float(k), e_us_nominal_bn=float(e_us_nominal[conv]))
    return t, info


def output_prices(tab, F):
    """Arm 5: G1's and G2's Mexican money at GDP PPP times F, on every GDP-PPP row of the generation."""
    t = tab.copy()
    for g, f in F.items():
        m = (t.generation == g) & (t.ppp == "gdp")
        for col in MONEY_COLS:
            t.loc[m, col] = t.loc[m, col] * f
        recompute(t, m)
    return t


# ------------------------------------------------------------------ arm 5: the group's industries
def industry_codes(d):
    """Each CPS record's census industry code (INDUSTRY, the longest job last year), aligned with load_asec's rows."""
    spec = G.importlib.util.spec_from_file_location("dist_base", G.FISCAL / "distribution_weights_2026_09_23/distribute.py")
    D = G.importlib.util.module_from_spec(spec)
    spec.loader.exec_module(D)
    with zipfile.ZipFile(D.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "INDUSTRY"])
    gate("industry_rows_aligned", np.array_equal(p.PH_SEQ.to_numpy(), d.PH_SEQ.to_numpy())
         and np.array_equal(p.PPPOS.to_numpy(), d.PPPOS.to_numpy()), records=len(d))
    return p.INDUSTRY.to_numpy()


def census_list():
    """The 2022 list's codes and its sector rows' ranges."""
    wb = openpyxl.load_workbook(EXTRA_SOURCES["census_industry_2022"][0], read_only=True)
    codes, sectors = set(), {}
    for r in wb["2022 Census Ind Code List "].iter_rows(values_only=True):
        c = "" if r[3] is None else str(r[3]).strip()
        if re.fullmatch(r"\d{4}", c):
            codes.add(int(c))
        elif re.fullmatch(r"\d{4}-\d{4}", c):
            sectors[str(r[0] or r[1]).strip()] = tuple(int(x) for x in c.split("-"))
    wb.close()
    return codes, sectors


def classify(ind):
    out = np.where(ind > 0, "others", "none").astype(object)
    for name, ranges, _, _ in CLASSES:
        for lo, hi in ranges:
            out[(ind >= lo) & (ind <= hi)] = name
    return out


def industry_table(d, ratio, e_mx):
    """Arm 5 by class: each generation's E_US share, its Mexican counterpart at GDP PPP (the lane's central E_MX split
    in the same shares) and at the class's category PPP, in arm 5 and its goods variant; F per generation."""
    rows, F = [], {}
    for g in ("G1", "G2"):
        s = d[d.gen.eq(g)]
        e = (s.pw * s.earn).groupby(s.cls).sum()
        tot = float(e.sum())
        F[g] = {}
        for var, pos in (("services", 2), ("goods_too", 3)):
            series = {c[0]: c[pos] for c in CLASSES}
            F[g][var] = sum(float(e.get(k, 0.0)) / tot / (ratio[series[k]] if series.get(k) else 1.0) for k in e.index)
        for k in [c[0] for c in CLASSES] + ["others", "none"]:
            share = float(e.get(k, 0.0)) / tot
            spec = {c[0]: c for c in CLASSES}.get(k)
            r5 = ratio[spec[2]] if spec and spec[2] else 1.0
            rg = ratio[spec[3]] if spec and spec[3] else 1.0
            mx = share * e_mx[g]
            rows.append(dict(generation=g, cls=k, icp_series=(spec[2] if spec else None) or "gdp",
                             icp_series_goods_too=(spec[3] if spec else None) or "gdp",
                             ppp_over_gdp_ppp=r5, ppp_over_gdp_ppp_goods_too=rg, e_us_share=share,
                             e_us_bn=share * tot / 1e9, e_mx_gdp_ppp_bn=mx, e_mx_category_bn=mx / r5,
                             e_mx_category_goods_too_bn=mx / rg, premium_gdp_ppp_bn=share * tot / 1e9 - mx,
                             premium_category_bn=share * tot / 1e9 - mx / r5,
                             premium_category_goods_too_bn=share * tot / 1e9 - mx / rg,
                             price_not_output_bn=(share * tot / 1e9 - mx) - (share * tot / 1e9 - mx / r5),
                             price_not_output_goods_too_bn=(share * tot / 1e9 - mx) - (share * tot / 1e9 - mx / rg)))
    t = pd.DataFrame(rows)
    for g in ("G1", "G2"):
        x = t[t.generation == g]
        gate(f"industry_shares_add_to_1_{g}", abs(x.e_us_share.sum() - 1) < 1e-12, total=float(x.e_us_share.sum()))
        gate(f"industry_F_is_the_tables_{g}", abs(x.e_mx_category_bn.sum() - F[g]["services"] * e_mx[g]) < 1e-9
             and abs(x.e_mx_category_goods_too_bn.sum() - F[g]["goods_too"] * e_mx[g]) < 1e-9)
    return t, F


# ------------------------------------------------------------------ arm 3: Mexico's budget and the US services
def mexico_budget_at(mxb, factors):
    m = mxb.copy()
    for cls, f in factors.items():
        m.loc[m.cls == cls, "bn"] = m.loc[m.cls == cls, "bn"] * f
    return m


def services_mexican_numeraire(vgen, r_health, r_social, r_public, r_food, r_cons):
    """The research's Mexico-price numeraire: 3a's health and social services, public goods and justice at V x the
    collective-government ratio, SNAP at V x food's, cash at V x private consumption's."""
    v = B.services_at_prices(vgen, r_health, r_social)
    for cls, f in (("public_good", r_public), ("justice", r_public), ("snap", r_food), ("cash", r_cons)):
        m = v.cls.eq(cls)
        for c in ("V_low_bn", "V_central_bn", "V_high_bn"):
            v.loc[m, c] = v.loc[m, c] * f
    return v


def change_by_class(v, v0):
    """Each generation's valued US budget by class, the scenario's less the lane's, at the mean of the band ends."""
    by = lambda x: x.groupby(["generation", "cls", "end"]).V_central_bn.sum().groupby(level=["generation", "cls"]).mean()  # noqa: E731
    d = by(v) - by(v0)
    return {g: {c: float(x) for c, x in d.xs(g, level="generation").items() if abs(x) > 1e-9} for g in W.GENS}


def evaluate(I, fac, pgc="average_cost", care_vg=None, mexico_health_vg=None, remit_rows=None, keep_rows=None):
    """beside_arms.evaluate, with keep_rows: rows (indexed by row id) whose values replace the scenario's."""
    rows, prem, _ = W.build_rows(I, pgc)
    if care_vg is not None or mexico_health_vg is not None:
        rows = B.health_rows(rows, I, pgc, care_vg, mexico_health_vg)
    for over in (remit_rows, keep_rows):
        if over is not None:
            rows = rows.set_index("row")
            rows.loc[over.index, ["low", "central", "high"]] = over[["low", "central", "high"]]
            rows = rows.reset_index()
    return rows, prem, W.totals(rows, prem, I, "central", fac, I["pos"])


# ------------------------------------------------------------------ arm 4: theta
def fiscal_parts():
    """The case's parts at the ledger's central (the mean of the two band ends), $bn: the debt lane's split."""
    t = pd.read_csv(SPLIT)
    t = t[(t.profile == SPLIT_PROFILE) & (t.convention == "central")].set_index("end")
    gate("split_has_both_ends", sorted(t.index) == ["high", "low"])
    gate("split_is_the_case", np.allclose([t.loc["low", "net_cost_bn"], t.loc["high", "net_cost_bn"]], CASE_SET,
                                          atol=1e-6), net_cost=t.net_cost_bn.to_dict())
    mid = lambda c: float(t[c].mean())   # noqa: E731
    return dict(state_local=mid("state_local_bn"), federal=mid("federal_bn"), capital_return=mid("resource_cost_bn"),
                capital_return_federal=mid("resource_cost_federal_bn"), accrual=mid("accrual_bn"),
                displaced=mid("displaced_bn"), net_cost=mid("net_cost_bn")), t


def mvpf(name):
    return sum(COMPOSITION[k] * MVPF_VALUES[name][k] for k in COMPOSITION)


def values(p):
    m = mvpf(p["mvpf"])
    v_borrowed = p["lam"] + p["d"] * (p["spc"] - 1)
    v_fed_today = v_borrowed if p["current_law"] else p["f"] * m + (1 - p["f"]) * p["lam"]
    return m, p["s"] * m + (1 - p["s"]) * p["lam"], v_fed_today, v_borrowed


def theta(parts, b, p):
    """theta_o (others today's lambda rows, and Mexico's) and theta_f (future taxpayers'), per $1."""
    m, v_sl, v_fed_today, v_borrowed = values(p)
    sl = parts["state_local"] + parts["capital_return"] - parts["capital_return_federal"]
    fed_today = (1 - b) * parts["federal"] + parts["capital_return_federal"]
    theta_o = (v_sl * sl + v_fed_today * fed_today) / (sl + fed_today)
    # Over the whole US fiscal cost: the lambda rows at theta, the accrual and the displaced beneficiaries at $1.
    borrowed, rest = b * parts["federal"], parts["accrual"] + parts["displaced"]
    blended = (theta_o * (sl + fed_today) + v_borrowed * borrowed + rest) / (sl + fed_today + borrowed + rest)
    return dict(mvpf=m, v_state_local=v_sl, v_federal_today=v_fed_today, v_borrowed=v_borrowed, theta_o=theta_o,
                theta_f=v_borrowed, others_base_bn=sl + fed_today, theta_on_the_fiscal_cost=blended)


def theta_mcpf(split, p):
    """mcpf's theta_eff at each band end (scratch mix_sens.py): the state-local part, its displaced part and the whole
    capital return at v_sl; the federal part and its displaced part at its borrowed share's mix; the accrual at $1;
    over the case's net cost."""
    _, v_sl, _, v_borrowed = values(p)
    b = 1.0 if p["current_law"] else MCPF_BORROWED
    v_fed = b * v_borrowed + (1 - b) * (p["f"] * mvpf(p["mvpf"]) + (1 - p["f"]) * p["lam"])
    out = {}
    for end, r in split.iterrows():
        sl = r.state_local_bn + (r.displaced_bn - r.displaced_federal_bn) + r.resource_cost_bn
        fed = r.federal_bn + r.displaced_federal_bn
        out[end] = float((sl * v_sl + fed * v_fed + r.accrual_bn) / r.net_cost_bn)
    return out


def capital_beside(split):
    """The shadow price of capital on displaced investment and the R&D policy arm at each band end, $bn."""
    m = mvpf("central")
    out = {}
    for end, r in split.iterrows():
        sl = r.state_local_bn + (r.displaced_bn - r.displaced_federal_bn)
        fed = r.federal_bn + r.displaced_federal_bn
        disp = [sl * DISPLACED_SHARE["state_local"][i] + fed * DISPLACED_SHARE["federal"][i]
                + r.accrual_bn * DISPLACED_SHARE["accrual"][i] for i in range(3)]
        re_spent = fed * (1 - MCPF_BORROWED) * BASE_THETA["f"]
        out[end] = dict(displaced_investment_bn=disp, spc_central_bn=disp[1] * (SPC_RANGE[1] - 1),
                        spc_range_bn=[disp[0] * (SPC_RANGE[0] - 1), disp[2] * (SPC_RANGE[2] - 1)],
                        rd_federal_re_spent_bn=re_spent, rd_policy_arm_bn=[re_spent * (x - m) for x in RD_BCR])
    return out


def lambda_rows(long):
    """Each scenario's lambda rows by party, S = (W_1.16 - W_equal) / 0.16, with its equal column and the whole long
    frame indexed (scenario, weighting, party)."""
    p = long.set_index(["scenario", "weighting", "party"]).bn
    eq = p.xs("equal", level="weighting")
    S = (p.xs("equal_lambda_1.16", level="weighting") - eq) / 0.16
    return S, eq, p


def derived_rows(party_tot):
    """W.totals' derived rows from the six parties' totals."""
    N = sum(party_tot[x] for x in W.PARTIES if x not in W.GROUP)
    N_us = party_tot["others_today"] + party_tot["future_taxpayers"]
    M = sum(party_tot[x] for x in W.GROUP)
    return dict(party_tot, non_group_total=N, group_total=M, world_total=N + M,
                breakeven_w=(-N / M) if (M > 0 and N < 0) else np.nan, us_residents_total=N_us,
                breakeven_w_us_only=(-N_us / M) if (M > 0 and N_us < 0) else np.nan)


def theta_long(long, thetas):
    """The theta columns of every scenario in long (scenario x weighting x party), from its equal and lambda 1.16
    columns."""
    S, eq, _ = lambda_rows(long)
    out = []
    for scen in long.scenario.unique():
        for name, th in thetas.items():
            tot = {}
            for party in W.PARTIES:
                k = PARTY_THETA.get(party)
                x = float(eq[(scen, party)])
                tot[party] = x + ((th[f"theta_{k}"] - 1) * float(S[(scen, party)]) if k else 0.0)
            for party, bn in derived_rows(tot).items():
                out.append(dict(scenario=scen, weighting=name, party=party, bn=bn))
    return pd.DataFrame(out)


def linearity_gate(long, lam_h, tol, name):
    S, eq, p = lambda_rows(long)
    diff = 0.0
    for col, lam in dict(LAMBDA_COLS, equal_lambda_hendren_a=lam_h).items():
        if col == "equal_lambda_1.16":
            continue
        for scen in long.scenario.unique():
            for party in W.PARTIES:
                diff = max(diff, abs(float(eq[(scen, party)]) + (lam - 1) * float(S[(scen, party)])
                                     - float(p[(scen, col, party)])))
    gate(f"lambda_columns_linear_in_their_rows_{name}", diff < tol, max_abs_diff=diff, tol=tol)
    return diff


# ------------------------------------------------------------------ the private gain on wages alone
def private_gain_inputs(vgen):
    """By generation, the mean of the band ends: the US taxes the group pays (the tax class at cost, negative), the
    Social Security accrual (the social_security line as valued), the HI taxes behind Part A, and Part A at the
    pension lane's rate per HI tax dollar."""
    v = vgen
    mean = lambda m, col: v[m].groupby(["generation", "end"])[col].sum().groupby(level="generation").mean()  # noqa: E731
    tax = mean(v.cls.eq("tax"), "G_bn")
    ss = mean(v.line.eq("social_security"), "V_central_bn")
    hi = -(mean(v.line.isin(["employee_hi", "employer_hi"]), "G_bn")
           + SE_HI_SHARE * mean(v.line.eq("self_employment_oasdi_hi"), "G_bn"))
    arms = pd.read_csv(PENSION_ARMS)
    arms = arms[arms.arm == PENSION_ARM].set_index("group")
    gate("pension_arm_has_each_generation", {"G1", "G2", "G3plus", "union"} <= set(arms.index), groups=list(arms.index))
    rate = {g: float(arms.loc[g.replace("+", "plus"), "part_a_per_hi_tax_dollar"]) for g in W.GENS}
    gate("tax_class_is_paid", all(tax[g] < 0 for g in W.GENS), tax=tax.to_dict())
    return {g: dict(us_taxes_bn=float(tax[g]), social_security_accrual_bn=float(ss[g]), hi_taxes_bn=float(hi[g]),
                    part_a_per_hi_tax_dollar=rate[g], part_a_accrual_bn=rate[g] * float(hi[g])) for g in W.GENS}, dict(
        union_part_a_pension_lane_bn=float(arms.loc["union", "part_a_bn"]),
        union_hi_tax_pension_lane_bn=float(arms.loc["union", "hi_tax_bn"]))


def private_gain(name, rows, inp, persons, g1_adults, source):
    c = rows.set_index("row").central
    out, tot = [], dict.fromkeys(("premium", "us_taxes", "mexico_taxes_avoided", "mexico_services_forgone",
                                  "social_security_accrual", "part_a_accrual"), 0.0)
    for g in W.GENS:
        x = dict(premium=float(c[f"premium_{g}"]), us_taxes=inp[g]["us_taxes_bn"],
                 mexico_taxes_avoided=float(c[f"mexico_taxes_avoided_{g}"]),
                 mexico_services_forgone=float(c[f"mexico_budget_lost_{g}"]),
                 social_security_accrual=inp[g]["social_security_accrual_bn"],
                 part_a_accrual=inp[g]["part_a_accrual_bn"])
        for k in tot:
            tot[k] += x[k]
        out.append((g, x, persons[g]))
    out.append(("group", tot, sum(persons.values())))
    res = []
    for g, x, n in out:
        a = x["premium"] + x["us_taxes"] + x["mexico_taxes_avoided"] + x["mexico_services_forgone"]
        b = a + x["social_security_accrual"] + x["part_a_accrual"]
        res.append(dict(scenario=name, from_scenario=source, generation=g, **{f"{k}_bn": v for k, v in x.items()},
                        wages_only_bn=a, with_old_age_accrual_bn=b, persons=n, wages_only_per_member_usd=a * 1e9 / n,
                        with_old_age_accrual_per_member_usd=b * 1e9 / n,
                        wages_only_per_g1_adult_usd=a * 1e9 / g1_adults if g == "G1" else np.nan,
                        with_old_age_accrual_per_g1_adult_usd=b * 1e9 / g1_adults if g == "G1" else np.nan))
    return res


# ------------------------------------------------------------------ checks
def tenure_check(d):
    """The lane's own US/Mexico pay ratio for G1 aged 25-64 by years in the US (2025 less PEINUSYR's band middle), per
    person and per hour (the cells' and the CPS's employment and weekly hours), at p56, GDP PPP. Hendricks and
    Schoellman's 2.0 is the gain at migration; the stock's US pay includes the years since."""
    cells = G.mexico_cells("gdp")
    g1 = d[d.gen.eq("G1") & d.A_AGE.between(25, 64)]
    yrs = g1.A_AGE - g1.arrival_age
    out = {}
    bins = (("arrived_2020_2024", 0, 5), ("arrived_2016_2019", 5.01, 10), ("arrived_2006_2015", 10.01, 20),
            ("arrived_before_2006", 20.01, 200))
    # MMP's schooling is low; the same ratios for the lane's cells below preparatoria and at primaria or less.
    extra = (("all", yrs.between(0, 200)), ("below_preparatoria", yrs.between(0, 200) & g1.own_cat.between(0, 3)),
             ("primaria_or_less", yrs.between(0, 200) & g1.own_cat.between(0, 2)))
    for lab, mask in tuple((b[0], yrs.between(b[1], b[2])) for b in bins) + extra:
        s = g1[mask]
        r = G.summarize("G1", lab, s, G.mexico_own_schooling(s, cells, 0.25, False), G.G1_SELECTION["p56"], {})
        h = (r["employment_mx_15plus"] * r["weekly_hours_mx_workers"]) / (r["employment_us_15plus"]
                                                                          * r["weekly_hours_us_workers"])
        us_hourly = r["us_earnings_bn"] * 1e9 / (r["persons_15plus_m"] * 1e6 * r["employment_us_15plus"]
                                                 * r["weekly_hours_us_workers"] * 52)
        out[lab] = dict(records=int(len(s)), persons_m=float(r["persons_m"]), ratio_per_person=float(r["ratio_us_to_mexico"]),
                        ratio_per_hour=float(r["ratio_us_to_mexico"] * h), us_pay_per_hour_2024usd=float(us_hourly),
                        mexico_pay_per_hour_ppp=float(us_hourly / (r["ratio_us_to_mexico"] * h)))
    gate("tenure_bins_cover_g1_25_64", sum(out[b[0]]["records"] for b in bins) == out["all"]["records"], bins=out)
    out["hs_mmp_2024usd"] = {k: v * CPI_2024 / CPI_2003 for k, v in HS_MMP_WAGES_2003.items()}
    return out


def summary_rows(name, arm, label, tot, prem, budget_bn, base, eqw):
    """One row per weighting: the party totals and the derived figures; prem: the premium by generation; base: the
    baseline's world total by weighting; eqw: the scenario's own world total at equal weights."""
    out = []
    for wt, g in tot.items():
        out.append(dict(scenario=name, arm=arm, label=label, weighting=wt, premium_G1_bn=prem["G1"],
                        premium_G2_bn=prem["G2"], premium_G3plus_bn=prem["G3+"], premium_bn=sum(prem.values()),
                        us_budget_value_bn=budget_bn, group_total_bn=g["group_total"],
                        others_today_bn=g["others_today"], future_taxpayers_bn=g["future_taxpayers"],
                        mexico_residents_bn=g["mexico_residents"], world_total_bn=g["world_total"],
                        us_residents_bn=g["us_residents_total"],
                        us_residents_incl_group_bn=g["us_residents_total"] + g["group_total"],
                        group_per_member_usd=g["group_total"] * 1e9 / MEMBERS, breakeven_w=g["breakeven_w"],
                        breakeven_w_us_only=g["breakeven_w_us_only"],
                        world_change_bn=g["world_total"] - base[wt], world_change_from_equal_bn=g["world_total"] - eqw))
    return out


def main():
    srcs = check_sources()
    I = W.load(CASE, BASIS)
    fac = W.channel_factors(I, "money")
    fac["_lambda"] = {f"equal_lambda_{k}": v for k, v in W.LAMBDAS.items()}
    lam_h = fac["fiscal_a"]["inv_g"]
    fac["_lambda"]["equal_lambda_hendren_a"] = lam_h
    gate("lambda_cols_are_the_lanes", {k: fac["_lambda"][k] for k in LAMBDA_COLS} == LAMBDA_COLS)

    # ---- the lane's central, reproduced; beside_arms.py's file
    rows0, prem0, t0 = evaluate(I, fac)
    ref = pd.read_csv(DERIVED / f"world_ledger_{CASE}.csv")
    ref = ref[(ref.mexico_taxes == "withheld_consumption") & (ref.scenario == "central_g3_zero")
              & (ref.pg_convention == "average_cost")]
    m = t0.merge(ref, on=["weighting", "party"], suffixes=("", "_ref"), validate="one_to_one")
    gate("central_reproduces_world_ledger", len(m) == len(t0) and B.max_diff(m.bn, m.bn_ref) < 1e-6,
         max_abs_diff=B.max_diff(m.bn, m.bn_ref))
    arms = pd.read_csv(DERIVED / f"beside_arms_{CASE}.csv")
    arms_sum = pd.read_csv(DERIVED / f"beside_arms_summary_{CASE}.csv")
    b0 = arms[arms.scenario == "baseline"].merge(t0, on=["weighting", "party"], suffixes=("", "_now"))
    gate("beside_arms_baseline_is_the_central", len(b0) == len(t0) and B.max_diff(b0.bn, b0.bn_now) < 1e-6,
         max_abs_diff=B.max_diff(b0.bn, b0.bn_now))
    remit0 = rows0.set_index("row").loc[["remit_G1", "remit_G2"]]

    # ---- inputs: the US records, Mexico's persons and cells, transitions, prices
    d = G.load_asec(BASIS)
    gate("members_are_the_lineage", abs(float(d.pw[d.gen.ne("")].sum()) - MEMBERS) < 1.0)
    parents, _ = G.parents_schooling()
    trans_nat = G.transitions()
    nat_cells = {p: G.mexico_cells(p) for p in ("gdp", "consumption")}
    tab0 = B.premium_table(d, parents, trans_nat, nat_cells)
    B.premium_table_gate(tab0)
    # The metros' municipalities (an ENOE read) are not needed here: localities by tam_loc, Mexico City by entidad.
    en = B.enigh_persons({})
    rates = MX.ppp()
    all_cells, _ = subset_cells(en, np.ones(len(en), bool), rates)
    gate("subset_cells_on_everyone_are_the_lanes", all(same_cells(all_cells[p], nat_cells[p]) for p in nat_cells))
    em = B.emovi_with_residence({})
    arms_meta = json.load(open(DERIVED / f"beside_arms_meta_{CASE}.json"))
    gate("beside_arms_meta_is_the_case", arms_meta["case"] == CASE and arms_meta["basis"] == BASIS)
    P_urban = arms_meta["prices"]["variants"]["large_localities"]["price_level"]
    cells, trans, cell_meta = {}, {}, {}
    for k, mask, emask in (("urban", en.tam_loc.eq(1).to_numpy(), em.city100k14.to_numpy()),
                           ("cdmx", en.ent.eq(9).to_numpy(), em.cdmx14.to_numpy())):
        cells[k], cell_meta[k] = subset_cells(en, mask, rates)
        tt, _, _ = MX.transitions(em[emask])
        trans[k], used = B.transition_dict(tt, fallback=trans_nat)
        cell_meta[k].update(emovi_respondents_at_14=int(emask.sum()), transitions_pooling=pd.Series(used).value_counts()
                            .to_dict())
    cells["urban_deflated"], trans["urban_deflated"] = deflate(cells["urban"], P_urban), trans["urban"]
    del en, em                                     # the run stays well under 2.5 GB
    state_rpp, _, _ = B.residence_prices(d)
    d_state = d.assign(earn=d.earn / (state_rpp / 100))
    ratio, ppp_gdp_2021 = icp_values()
    r_health, r_social, r_public = ratio[B.ICP_HEALTH], ratio[B.ICP_GOV_IND], ratio[B.ICP_GOV_COLL]
    r_cons = rates["PA.NUS.PRVT.PP"] / rates["PA.NUS.PPP"]
    gate("ppp_rates_are_wdi_2024", abs(rates["PA.NUS.PPP"] - 9.9166) < 1e-3 and abs(rates["PA.NUS.PRVT.PP"] - 10.8013)
         < 1e-3, rates=rates)

    # ---- arm 5's classes and factors
    codes, sectors = census_list()
    gate("census_list_has_266_codes", len(codes) == 266, n=len(codes))
    gate("census_sector_ranges_are_the_classes", all(sectors.get(k) == v for k, v in SECTOR_RANGES.items()),
         sectors={k: sectors.get(k) for k in SECTOR_RANGES})
    d["industry"] = industry_codes(d)
    d["cls"] = classify(d.industry.to_numpy())
    d_state["industry"], d_state["cls"] = d.industry, d.cls
    grp = d[d.gen.isin(["G1", "G2"])]
    earners = grp[grp.earn > 0]
    off = sorted(set(int(x) for x in earners.industry.unique()) - codes)
    gate("group_industry_codes_on_the_2022_list", set(off) <= OFF_LIST and not (earners.industry <= 0).any(), off=off,
         no_code=int((earners.industry <= 0).sum()))
    e_mx0 = {"G1": float(central_row(tab0, "own_schooling_all_ages").mexico_earnings_bn),
             "G2": float(prem0["G2"]["e_mx"]["central"])}
    ind_tab, F = industry_table(d, ratio, e_mx0)
    _, F_state = industry_table(d_state, ratio, e_mx0)
    off_share = {g: float((s.pw * s.earn)[s.industry.isin(OFF_LIST)].sum() / (s.pw * s.earn).sum())
                 for g, s in grp.groupby("gen")}

    # ---- the premium tables
    tables = {
        "national": tab0,
        "urban": B.premium_table(d, parents, trans["urban"], cells["urban"]),
        "urban_deflated": B.premium_table(d, parents, trans["urban_deflated"], cells["urban_deflated"]),
        "cdmx": B.premium_table(d, parents, trans["cdmx"], cells["cdmx"]),
        "rpp_national": B.premium_table(d_state, parents, trans_nat, nat_cells),
        "rpp_urban": B.premium_table(d_state, parents, trans["urban"], cells["urban"]),
        "rpp_urban_deflated": B.premium_table(d_state, parents, trans["urban_deflated"], cells["urban_deflated"]),
    }
    num = [c for c in tab0.columns if c not in KEYS and pd.api.types.is_numeric_dtype(tab0[c])]
    gate("with_central_identity", np.array_equal(with_central(tab0)[num].to_numpy(float), tab0[num].to_numpy(float),
                                                 equal_nan=True))
    table_gate("output_prices_at_1_is_the_lane", output_prices(tab0, {"G1": 1.0, "G2": 1.0}), tab0)
    e_us_nom = {conv: float(central_row(tab0, conv).us_earnings_bn) for conv in tab0[tab0.generation.eq("G1")]
                .convention.unique()}
    ratios = {k: annual_ratio(tab0, r, per_hour) for k, (r, per_hour, _, _) in SAME_PERSON.items()}
    lane = annual_ratio(tab0, 1.0, False)
    t_id, _ = same_person(tab0, {c: dict(v, r_annual=v["lane_ratio_annual"]) for c, v in lane.items()}, e_us_nom)
    table_gate("same_person_at_the_lane_ratio_is_the_lane", t_id, tab0)
    mx_us = mexico_budget_at(I["mxb"], dict(health=1 / r_health, public_good=1 / r_public, cash=1 / r_cons))
    gate("mexico_budget_at_1_is_the_lanes", B.max_diff(mexico_budget_at(I["mxb"], dict(health=1, public_good=1, cash=1))
                                                       .bn, I["mxb"].bn) == 0.0)
    v3a = B.services_at_prices(I["vgen"], r_health, r_social)
    v_mxnum = services_mexican_numeraire(I["vgen"], r_health, r_social, r_public, ratio[ICP_FOOD], r_cons)
    kw3a = dict(care_vg=(r_health,) * 3, mexico_health_vg=(1.0,) * 3)
    kw3ab = dict(kw3a, pgc="response_only")
    T = tables
    r2 = output_prices(with_central(T["rpp_urban"], "gdp", "p70"), {g: F_state[g]["services"] for g in F_state})
    r2c = with_central(T["rpp_urban"], "consumption", "p70")
    r1 = with_central(T["rpp_urban"], "consumption", "p56")
    sp = lambda tab, k: same_person(tab, ratios[k], e_us_nom)[0]   # noqa: E731

    # ---- the scenarios: (name, arm, label, inputs, evaluate's keywords)
    S = [("baseline", "central", "the lane's central (oct07, lineage, average cost, withheld + consumption taxes)", I, {})]
    one = lambda name, arm, label, tab, **kw: S.append((name, arm, label, dict(I, g2=tab), kw))   # noqa: E731
    one("arm1a_urban_consumption", "1a", "1a: localities of 100,000+, consumption PPP, p56",
        with_central(T["urban"], "consumption"))
    one("arm1a_urban", "1a", "1a's part: localities of 100,000+ at GDP PPP", T["urban"])
    one("arm1a_consumption", "1a", "1a's part: national cells at consumption PPP", with_central(tab0, "consumption"))
    one("arm1a_urban_deflated_consumption", "1a", f"1a with urban pay at the localities' price level ({P_urban:.4f})",
        with_central(T["urban_deflated"], "consumption"))
    one("arm1a_cdmx", "1a", "Mexico City's cells at GDP PPP (beside)", T["cdmx"])
    one("arm1a_cdmx_consumption", "1a", "Mexico City's cells at consumption PPP (beside)",
        with_central(T["cdmx"], "consumption"))
    one("arm1a_urban_p70", "1a", "localities of 100,000+ at CMP's p70, GDP PPP (the operator's best job)",
        with_central(T["urban"], "gdp", "p70"))
    for k, (_, _, arm, label) in SAME_PERSON.items():
        one(k, arm, label, sp(tab0, k))
    one("arm2_state_rpp", "2", "2: US earnings at national prices, state RPP", T["rpp_national"], remit_rows=remit0)
    S.append(("arm3_us_numeraire", "3", "3: Mexico's services forgone and saved at ICP category PPPs (US-price "
              "numeraire)", dict(I, mxb=mx_us), {}))
    S.append(("arm3a", "3a", "3a: US health and social services at Mexican relative prices", dict(I, vgen=v3a), kw3a))
    S.append(("arm3b", "3b", "3b: public goods at their responsive cost [FRAMING-SENSITIVE]", I,
              dict(pgc="response_only")))
    S.append(("arm3_mexican_numeraire", "3", "Mexican-price numeraire: 3a plus public goods, justice, SNAP and cash at "
              "Mexican relative prices", dict(I, vgen=v_mxnum), kw3a))
    one("arm5_output_prices", "5", "5: Mexican pay by industry at ICP category PPPs, services [FRAMING-SENSITIVE]",
        output_prices(tab0, {g: F[g]["services"] for g in F}))
    one("arm5_output_prices_goods_too", "5", "5 with goods at their own category PPPs too",
        output_prices(tab0, {g: F[g]["goods_too"] for g in F}))
    S.append(("reading1", "reading_1", "Reading 1 (recommended): 1a + 2 + 3", dict(I, g2=r1, mxb=mx_us),
              dict(remit_rows=remit0)))
    S.append(("reading1_deflated", "reading_1", f"Reading 1 with 1a's urban pay deflated ({P_urban:.4f})",
              dict(I, g2=with_central(T["rpp_urban_deflated"], "consumption"), mxb=mx_us), dict(remit_rows=remit0)))
    S.append(("reading2", "reading_2", "Reading 2 (the operator's framing): urban p70 + 2 + 5 + 3a + 3b",
              dict(I, g2=r2, vgen=v3a), dict(kw3ab, remit_rows=remit0)))
    S.append(("reading2_consumption", "reading_2", "Reading 2 at consumption PPP in place of 5 (its private gain)",
              dict(I, g2=r2c, vgen=v3a), dict(kw3ab, remit_rows=remit0)))
    S.append(("reading3", "reading_3", "Reading 3 (within person): reading 1 with G1 at 1c's 1.59",
              dict(I, g2=sp(r1, "arm1c_mmp_per_person"), mxb=mx_us), dict(remit_rows=remit0)))
    S.append(("reading3_mmp_annual", "reading_3", "Reading 3 with G1 at 1c's 2.0",
              dict(I, g2=sp(r1, "arm1c_mmp_annual"), mxb=mx_us), dict(remit_rows=remit0)))
    S.append(("combined_low", "combined_low", "Combined low: reading 2 with G1 at 1c's 1.59",
              dict(I, g2=sp(r2, "arm1c_mmp_per_person"), vgen=v3a), dict(kw3ab, remit_rows=remit0)))
    S.append(("combined_low_consumption", "combined_low", "Combined low at consumption PPP in place of 5 (its private "
              "gain)", dict(I, g2=sp(r2c, "arm1c_mmp_per_person"), vgen=v3a), dict(kw3ab, remit_rows=remit0)))
    names = [s[0] for s in S]
    gate("scenario_names_unique", len(names) == len(set(names)))

    evaluated, long = {}, []
    for name, arm, _, Ia, kw in S:
        rows, prem, t = evaluate(Ia, fac, **kw)
        evaluated[name] = (rows, prem, Ia)
        long.append(t.assign(scenario=name, arm=arm))
    long = pd.concat(long, ignore_index=True)
    gate("baseline_is_the_central", B.max_diff(long[long.scenario == "baseline"].bn, t0.bn) == 0.0)
    # The group-only check on arm 3: Mexico's budget saved stays at GDP PPP.
    saved = [f"mexico_budget_saved_{g}" for g in W.GENS]
    keep = rows0.set_index("row").loc[saved]
    rows_g, _, t_g = evaluate(dict(I, mxb=mx_us), fac, keep_rows=keep)
    evaluated["arm3_us_numeraire_group_only"] = (rows_g, evaluated["arm3_us_numeraire"][1], dict(I, mxb=mx_us))
    long = pd.concat([long, t_g.assign(scenario="arm3_us_numeraire_group_only", arm="3")], ignore_index=True)
    labels = {s[0]: s[2] for s in S}
    labels["arm3_us_numeraire_group_only"] = "3's check: the group's rows only (Mexico's budget saved at GDP PPP)"
    arm_of = {s[0]: s[1] for s in S}
    arm_of["arm3_us_numeraire_group_only"] = "3"
    # Arms 2, 3a and 3b are beside_arms.py's.
    for k in ("arm2_state_rpp", "arm3a", "arm3b"):
        a = arms[arms.scenario == k].merge(long[long.scenario == k], on=["weighting", "party"], suffixes=("", "_now"))
        gate(f"{k}_is_beside_arms", len(a) == len(t0) and B.max_diff(a.bn, a.bn_now) < 1e-6,
             max_abs_diff=B.max_diff(a.bn, a.bn_now))
    linearity_gate(long, lam_h, 1e-9, "here")

    # ---- arm 4: theta for every scenario; beside_arms.py's others from its file's 6 decimals
    parts, split = fiscal_parts()
    r0 = rows0.set_index("row").central
    others_rows = -(r0["fiscal_others"] + r0["induced_receipts"])
    future_rows = -r0["fiscal_future"]
    b = future_rows / parts["federal"]
    gate("borrowed_share_is_fy2024_deficit_over_outlays", 0.25 < b < 0.29, b=b)
    th_probe = theta(parts, b, THETA_SETS["theta_central"])
    # The winners channels print 6 decimals, and the ledger's fiscal rows add several of them.
    gate("others_lambda_rows_are_the_cases_parts", abs(others_rows - th_probe["others_base_bn"]) < 1e-5,
         ledger=others_rows, parts=th_probe["others_base_bn"])
    gate("accrual_row_is_the_cases", abs(-r0["fiscal_pension_accrual"] - parts["accrual"]) < 1e-5,
         ledger=-r0["fiscal_pension_accrual"], parts=parts["accrual"])
    thetas = {k: theta(parts, b, p) for k, p in THETA_SETS.items()}
    mcpf = {k: theta_mcpf(split, p) for k, p in THETA_SETS.items()}
    beside_capital = capital_beside(split)
    ident = {col: theta(parts, b, dict(BASE_THETA, s=0.0, lam=lam, f=0.0, d=0.0, spc=1.0))
             for col, lam in dict(LAMBDA_COLS, equal_lambda_hendren_a=lam_h).items()}
    part1 = arms[~arms.scenario.isin(set(long.scenario))]
    linearity_gate(part1, lam_h, 1e-5, "beside_arms")     # the file's 6 decimals bound the recomputation
    all_long = pd.concat([long[["scenario", "weighting", "party", "bn"]], part1[["scenario", "weighting", "party", "bn"]]],
                         ignore_index=True)
    th_long = theta_long(all_long, {**thetas, **{f"identity_{k}": v for k, v in ident.items()}})
    piv = all_long.set_index(["scenario", "weighting", "party"]).bn
    idd = 0.0
    for col in ident:
        x = th_long[(th_long.weighting == f"identity_{col}") & th_long.party.isin(W.PARTIES)]
        idd = max(idd, max(abs(r.bn - piv[(r.scenario, col, r.party)]) for r in x.itertuples()))
    gate("theta_at_lambda_reproduces_the_lambda_columns", idd < 1e-5, max_abs_diff=idd)
    th_long = th_long[~th_long.weighting.str.startswith("identity_")]
    th_idx = th_long.set_index(["scenario", "weighting", "party"]).bn
    direct = 0.0
    for name, (rows, prem, Ia) in evaluated.items():
        for tname, th in thetas.items():
            rr = rows.copy()
            ff = rr.row.eq("fiscal_future")
            rr.loc[ff, ["low", "central", "high"]] = rr.loc[ff, ["low", "central", "high"]] * th["theta_f"] / th["theta_o"]
            td = W.totals(rr, prem, Ia, "central", dict(fac, _lambda={"equal_lambda_theta": th["theta_o"]}), Ia["pos"])
            td = td[td.weighting == "equal_lambda_theta"].set_index("party").bn
            mine = np.array([float(th_idx[(name, tname, p)]) for p in td.index])
            direct = max(direct, B.max_diff(mine, td.to_numpy(float)))
    gate("theta_postprocessing_equals_direct_evaluation", direct < 1e-9, max_abs_diff=direct)

    # ---- the private gain on wages alone
    inp, inp_check = private_gain_inputs(I["vgen"])
    persons = {g: float(d.pw[d.gen.eq(g)].sum()) for g in W.GENS}
    gate("persons_are_the_lineage", abs(sum(persons.values()) - MEMBERS) < 1.0, persons=persons)
    gr = pd.read_csv(GENERATION_RESULTS)
    g1_adults = gr[(gr.convention == "a") & (gr.generation == "G1")].adults.unique()
    gate("one_g1_adult_count", len(g1_adults) == 1, adults=list(g1_adults))
    pg = []
    for name in evaluated:
        if name.startswith("arm5_"):
            continue                       # output at common prices: not a purchasing-power figure
        src = PRIVATE_GAIN_TWIN.get(name, name)
        pg += private_gain(name, evaluated[src][0], inp, persons, float(g1_adults[0]), src)
    pg = pd.DataFrame(pg)

    # ---- outputs
    keep_cols = ["case", "scenario", "arm", "weighting", "party", "bn"]
    arm_of.update({s: a for s, a in zip(arms_sum.scenario, arms_sum.arm) if s not in arm_of})
    labels.update({s: f"beside_arms.py: {lab}" for s, lab in zip(arms_sum.scenario, arms_sum.label) if s not in labels})
    out_long = pd.concat([long.drop(columns=["unknown_rows"]), th_long.assign(arm=th_long.scenario.map(arm_of))],
                         ignore_index=True).assign(case=CASE)[keep_cols]
    gate("every_scenario_has_an_arm", out_long.arm.notna().all())
    base_w = {**{w: float(piv[("baseline", w, "world_total")]) for w in B.WEIGHTINGS},
              **{w: float(th_idx[("baseline", w, "world_total")]) for w in thetas}}
    summ = []
    eq_sum = arms_sum[arms_sum.weighting == "equal"].set_index("scenario")
    for scen in all_long.scenario.unique():
        if scen in evaluated:
            c = evaluated[scen][0].set_index("row").central
            prem = {x: float(c[f"premium_{x}"]) for x in W.GENS}
            budget_bn = float(sum(c[f"us_budget_value_{x}"] for x in W.GENS))
            wts = B.WEIGHTINGS + tuple(thetas)
        else:
            e = eq_sum.loc[scen]
            prem = {"G1": float(e.premium_G1_bn), "G2": float(e.premium_G2_bn), "G3+": float(e.premium_G3plus_bn)}
            budget_bn, wts = float(e.us_budget_value_bn), tuple(thetas)
        tot = {}
        for wt in wts:
            src = all_long if wt in B.WEIGHTINGS else th_long
            g = src[(src.scenario == scen) & (src.weighting == wt)].set_index("party").bn
            tot[wt] = {k: float(v) for k, v in g.items()}
        summ += summary_rows(scen, arm_of[scen], labels[scen], tot, prem, budget_bn, base_w,
                             float(piv[(scen, "equal", "world_total")]))
    summary = pd.DataFrame(summ)
    out_long.to_csv(DERIVED / f"beside_extra_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    summary.to_csv(DERIVED / f"beside_extra_summary_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    pg.to_csv(DERIVED / f"beside_extra_private_gain_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    ind_tab.to_csv(DERIVED / f"beside_extra_industry_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    detail = {}
    for name, (_, prem, _) in evaluated.items():
        detail[name] = dict(e_mx_central_bn={g: prem[g]["e_mx"]["central"] for g in W.GENS},
                            e_us_bn={g: prem[g]["e_us"] for g in W.GENS},
                            mexico_taxes_central_bn={g: prem[g]["tax"]["central"] + prem[g]["ctax"]["central"]
                                                     for g in W.GENS})
    same = {k: same_person(tab0, ratios[k], e_us_nom)[1] for k in SAME_PERSON}
    meta = dict(case=CASE, basis=BASIS, members=MEMBERS, sources=srcs, scenario_detail=detail,
                arm1=dict(cells=cell_meta, urban_price_level=P_urban, urban_price_level_source=(
                    "beside_arms.py price_levels: 1 + s_h (R - 1), R the hedonic rent index of localities of 100,000+"),
                          same_person=dict(sets={k: dict(r=v[0], per_hour=v[1], label=v[3]) for k, v in SAME_PERSON.items()},
                                           detail=same, e_us_nominal_bn=e_us_nom)),
                arm3=dict(r_health=r_health, r_social=r_social, r_public=r_public, r_food=ratio[ICP_FOOD],
                          r_consumption_wdi_2024=r_cons, mexico_budget_factors=dict(
                              health=1 / r_health, public_good=1 / r_public, cash=1 / r_cons),
                          budget_change_by_class_bn=dict(arm3a=change_by_class(v3a, I["vgen"]),
                                                         mexican_numeraire=change_by_class(v_mxnum, I["vgen"]))),
                arm4=dict(parts_central_bn=parts, borrowed_share=b, lambda_h=lam_h, composition=COMPOSITION,
                          mvpf_values=MVPF_VALUES, sets=THETA_SETS, labels=THETA_LABELS, theta=thetas,
                          mcpf_theta_eff_by_end=mcpf, mcpf_borrowed_share=MCPF_BORROWED,
                          beside=dict(by_end=beside_capital, displaced_share=DISPLACED_SHARE, spc=SPC_RANGE,
                                      rd_benefit_cost=RD_BCR),
                          lambda_rows_central_bn=dict(others_today=-others_rows, future_taxpayers=-future_rows),
                          split_file=str(SPLIT.relative_to(REPO))),
                arm5=dict(F=F, F_state_rpp=F_state, icp_ratio_over_gdp_ppp=ratio, icp_gdp_ppp_2021=ppp_gdp_2021,
                          classes=[dict(cls=c[0], codes=[list(x) for x in c[1]], series=c[2], series_goods_too=c[3])
                                   for c in CLASSES], off_list_codes=sorted(OFF_LIST), off_list_earnings_share=off_share,
                          e_mx_central_bn=e_mx0, service_share_of_e_us={
                              g: float(ind_tab[(ind_tab.generation == g) & ~ind_tab.cls.isin(GOODS)].e_us_share.sum())
                              for g in ("G1", "G2")}),
                private_gain=dict(inputs=inp, check=inp_check, g1_adults=float(g1_adults[0]), persons=persons,
                                  twins=PRIVATE_GAIN_TWIN),
                tenure_check=tenure_check(d),
                gates=dict(theta_identity_max_abs_diff=idd, theta_direct_max_abs_diff=direct))
    json.dump(meta, open(DERIVED / f"beside_extra_meta_{CASE}.json", "w"), indent=1, sort_keys=True, default=float)
    show = summary[summary.weighting.isin(("equal", "equal_lambda_1.16") + SHOW_THETA)].set_index(
        ["scenario", "weighting"])[["premium_G1_bn", "premium_G2_bn", "world_total_bn", "us_residents_incl_group_bn",
                                    "group_per_member_usd", "breakeven_w", "breakeven_w_us_only"]]
    print(show.round(3).to_string(), file=sys.stderr)
    print({k: (round(v["theta_o"], 4), round(v["theta_f"], 4), round(v["theta_on_the_fiscal_cost"], 4),
               {e: round(x, 4) for e, x in mcpf[k].items()}) for k, v in thetas.items()}, file=sys.stderr)
    print(pg[pg.generation.isin(["G1", "group"])].set_index(["scenario", "generation"])[
        ["premium_bn", "us_taxes_bn", "mexico_taxes_avoided_bn", "mexico_services_forgone_bn", "wages_only_bn",
         "with_old_age_accrual_bn", "wages_only_per_g1_adult_usd"]].round(2).to_string(), file=sys.stderr)


if __name__ == "__main__":
    main()
