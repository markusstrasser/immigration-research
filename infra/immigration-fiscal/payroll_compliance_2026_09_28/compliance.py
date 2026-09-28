"""Do the group's credited payroll and income taxes assume full compliance? Measure the parts that do.

The account's national totals are BEA collections. The group's share of each line comes from CPS ASEC 2025 records
(income year 2024) through full_account_receipts_2026_09_20/builder.py's keys, which the benchmark lane's frame.py
copies. This script:

1. rebuilds the keys and CBO's income gradient (external_benchmarks_2026_09_24) and gates them against model.json
   and the benchmark lane's translation;
2. re-applies audit row 2, the case's scaling of the Latin-American-born imputed unauthorized's six tax keys to an
   on-books share, on the paper flag, and gates it against the CPS lane's `origin|<case>|audit_rules_alone`
   payloads;
3. compares the wages row 2 takes off the books with the off-books pay the compliance-gap lane's slopes imply
   (brief item 1);
4. builds each candidate item as a change to the person-level key vectors on top of row 2, and writes, per receipt
   line and allocation, r = the group's share after the item over its share before it (CBO's gradient kept where
   the case applies it), with a 160-replicate standard error. Each item holds the national total: it moves the
   group's share of a fixed collection. price.cjs applies r to the adopted case;
5. parses every parameter from the cached primary sources (acquire.py) and checks every quote.

Items:
  se_industry     self-employment income reaches tax returns at Alm & Erard's tax-return/CPS ratios, informal
                  supplier industries against the rest (TY2001); low: the informal gap at IRS's TY2014-16
                  nonfarm net misreporting of 57% with Alm & Erard's 39/46 split; high: plus Tamborini &
                  Villarreal's filing gap by ethnicity and generation (model 5, within occupation) for everyone
                  not flagged. It moves the self-employment line and, through unreported income at the unit's
                  marginal rate, the income taxes.
  income_nmp      sensitivity for the income taxes only: every other CPS income type also at IRS's net
                  misreporting percentage (wages 1%, interest and dividends 4%, rents 53%, ...).
  slopes          the compliance-gap lane's off-books slopes replace row 2's share for flagged workers in
                  construction, landscaping, janitorial work and restaurants (its low / central / high variants).
  other_unauth    row 2's rule applied to the imputed unauthorized born outside Latin America, whom the case
                  leaves unscaled: those without a bachelor's degree at the other-origin share 0.550 (0.401 and
                  0.683 as variants), and every flagged person as a bound.
  cash_consumption  the consumption key with the unpaid taxes of row 2's off-books part added back to SPM
                  resources and the credits row 2 denies taken out.
  authorized_bound  bound only: the compliance-gap lane's calibrated uncovered share taken as off-books pay of
                  every unflagged worker in those four industries.
  all             se_industry + slopes + other_unauth + cash_consumption together, at one on-books case throughout:
                  central; low cost at the on-books lane's high shares (row 2 0.635/0.683, the others 0.683) with
                  the low slopes and self-employment readings; high cost at its low shares (0.415/0.401, the
                  others 0.401) with the high readings. The ends are measured against row 2 at their own shares
                  and priced on the package's stack for that case; *_central_case holds row 2 at the central
                  shares, isolating what the items add.
  row2_r_route    row 2 itself (full compliance for the flagged, and the low and high shares) by this lane's rule,
                  to set against the package's stacks for the same change.

Each ratio is also written on the raw shares (r_raw: no CBO gradient), the convention the package uses when it
scales CBO's re-key by a stack's factor; price.cjs prices both.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/payroll_compliance_2026_09_28/compliance.py

Writes derived/ (CSV, JSON); writes nothing if a gate fails.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
CACHE = HERE / "_cache"
SRC = CACHE / "sources"
OUT = HERE / "derived"
BENCH = FISCAL / "external_benchmarks_2026_09_24"
sys.path.insert(0, str(BENCH))
sys.dont_write_bytecode = True
import frame as f  # noqa: E402  (the benchmark lane's CPS frame, keys and CBO groups, read-only)
import cbo_arm  # noqa: E402

f.CACHE = CACHE  # the frame loader keeps its parquet cache in this lane
GAP = FISCAL / "compliance_gap_2026_09_24"
ONBOOKS = FISCAL / "onbooks_share_2026_09_23"
STACK_CACHE = FISCAL / "cps_imputation_keys_2026_09_23/_cache/onbooks_lane_line_deltas.json"
ALLOCS = ("personal", "shared")
CASES = ("low", "central", "high")
METHODS = ("b_hotdeck_union_matched", "b_matched_over_pooled")  # the package's fill-in methods (price.cjs gates it)
# The lines whose group amounts make up the unpaid taxes the consumption item adds back (FICA, federal, state).
UNPAID_LINES = ("employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "federal_income_tax",
                "state_local_income_tax")
KEYS = ("wage", "wage_oasdi", "self_payroll", "positive_fica_worker", "federal_liability", "state_liability",
        "consumption")
# CBO's income gradient as the case applies it (cbo_arm.py bundle all_but_medicaid|2022).
CBO_SPEC = {"federal_income_tax": "individual_inc_tax=individual_inc_tax_gross|2022",
            "employee_oasdi": "payroll_taxes|2022", "employer_oasdi": "payroll_taxes|2022",
            "employee_hi": "payroll_taxes|2022", "employer_hi": "payroll_taxes|2022",
            "self_employment_oasdi_hi": "payroll_taxes|2022", "excise_selective_sales": "excise_taxes|2022"}
# Alm & Erard's 11 informal-supplier categories (their Table 1; "Food catering and roadside stands" has no CPS
# estimate) as CPS ASEC 2025 industry codes of the longest job (cpsmar25 Appendix A). Their crosswalk is published
# for construction only, so the rest is this lane's reading of the category names [INFERENCE].
INFORMAL = {
    "Direct sales": [5690],
    "Building maintenance/landscaping": [7690, 7770],
    "Forestry, fishing, hunting, and trapping": [190, 270, 280],
    "Arts and entertainment": [8561, 8562, 8563, 8564, 8590],
    "Construction": [770],
    "Teaching/lessons": [7890],
    "Care of children and elderly": [8170, 8370, 8470, 9290],
    "Personal services": [8970, 8980, 8990, 9070, 9090],
    "Auto repair and maintenance": [8770, 8780],
    "Other repair and maintenance": [8790, 8870, 8891],
    "Transportation and moving": [6170, 6190, 6380],
}
# The compliance-gap lane's four priced cells (edges_by_industry.csv) as CPS industry codes.
GAP_CELLS = {"c23": (770, "Construction"), "c56173": (7770, "Landscaping services"),
             "c5617z": (7690, "Services to buildings and dwellings"),
             "c722z": (8680, "Restaurants and other food services")}
US_BIRTH = [57, 60, 66, 69, 73, 78]  # frame.py masks(): the United States and its territories
BACHELOR = 43  # A_HGA: bachelor's degree
GATES: list[tuple[str, bool, str]] = []
QUOTES: list[dict] = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append((name, bool(ok), detail))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def num(s: str) -> float:
    return float(s.replace("−", "-").replace(",", ""))


# ---------------------------------------------------------------------------------------------- sources
def norm(s: str) -> str:
    """Quote matching ignores whitespace (pdftotext breaks lines and hyphenates) and typographic variants."""
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("−", "-"), ("­", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


TEXTS: dict[str, str] = {}


def text(name: str) -> str:
    if name not in TEXTS:
        TEXTS[name] = (SRC / name).read_text() if (SRC / name).exists() else (ROOT / name).read_text()
    return TEXTS[name]


def quote(source: str, locator: str, q: str) -> str:
    found = norm(q) in norm(text(source))
    QUOTES.append({"source": source, "locator": locator, "quote": q, "found": found})
    if not found:
        gate(f"quote_found:{source}:{locator}", False, q[:80])
    return q


def manifest_ok() -> dict:
    import acquire  # the lane's fetcher: its SOURCES name every file this script may read
    m = json.loads((SRC / "manifest.json").read_text())["files"]
    ok = all(sha(SRC / n) == e["sha256"] for n, e in m.items())
    gate("sources_are_the_pinned_files", ok and sorted(m) == sorted(acquire.SOURCES),
         f"{len(m)} files in _cache/sources/manifest.json, the {len(acquire.SOURCES)} acquire.py names, each matching "
         f"its recorded sha256 (acquire.py pins them)")
    return m


def irs_1415() -> dict:
    t = text("irs_p1415.txt")
    i = t.index("Table 5. Individual Income Tax Underreporting Tax Gap by Source")
    block = t[i:t.index("[1]", i)]
    labels = {"wages": "Wages, salaries, tips", "interest": "Interest income", "dividends": "Dividend income",
              "pensions": "Pensions & annuities", "unemployment": "Unemployment Compensation",
              "social_security": "Taxable Social Security benefits",
              "partnership": "Partnership, S-Corp, Estate & Trust, etc.", "capital_gains": "Capital gains [5]",
              "other_income": "Other income", "nonfarm_proprietor": "Nonfarm proprietor income",
              "farm": "Farm income", "rents": "Rents & royalties"}
    nmp = {}
    for k, lab in labels.items():
        m = re.search(r"^\s*" + re.escape(lab) + r"(?!\w).*?(\d+)%\s*$", block, re.M)
        if not m:
            raise SystemExit(f"[BLOCKED] Pub 1415 Table 5 has no row {lab!r}")
        nmp[k] = int(m.group(1)) / 100
    expect = {"wages": .01, "interest": .04, "dividends": .04, "pensions": .04, "unemployment": .12,
              "social_security": .13, "partnership": .12, "capital_gains": .18, "other_income": .42,
              "nonfarm_proprietor": .57, "farm": .64, "rents": .53}
    gate("irs_table_5_net_misreporting", nmp == expect,
         "Pub 1415 Table 5 (TY2014-16): " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in nmp.items()))
    j = t.index("Table 2. Tax Gap Estimates")
    t2 = t[j:t.index("Detail may not add to total due to rounding.", j)]
    se_under = re.search(r"^\s*Self-Employment Tax\s+\$(\d+)\s+11%", t2, re.M)
    se_nonfile = re.search(r"^\s*Self-Employment Tax\s+\$(\d+)\s+1%", t2, re.M)
    fica = re.search(r"^\s*FICA and FUTA Tax\s+\$(\d+)", t2, re.M)
    gaps = {"se_underreporting_bn": int(se_under.group(1)), "se_nonfiling_bn": int(se_nonfile.group(1)),
            "fica_futa_underreporting_bn": int(fica.group(1))}
    gate("irs_table_2_employment_tax_gaps", gaps == {"se_underreporting_bn": 53, "se_nonfiling_bn": 7,
                                                      "fica_futa_underreporting_bn": 29},
         f"Pub 1415 Table 2 (TY2014-16 annual averages, $bn): {gaps}")
    quote("irs_p1415.txt", "Table 5 note [2]", "The net misreporting percentage is the net misreported amount "
          "divided by the sum of the absolute values of the amounts that should have been reported, expressed as a "
          "percentage.")
    quote("irs_p1415.txt", "4.2.3", "The FICA and FUTA taxes associated with employers of agricultural and "
          "household workers are also excluded from the estimates due to lack of compliance data.")
    quote("irs_p1415.txt", "4.2.3", "It is estimated that the employer FICA and FUTA employment tax underreporting "
          "tax gap for TY 2014- 2016 is a combined $29 billion, with $28 billion from underreported FICA taxes and "
          "$1 billion from underreported FUTA taxes.")
    quote("irs_p1415.txt", "4.2.3", "The components of the employment tax underreporting tax gap estimate that are "
          "associated with employer reporting of FICA and FUTA are estimated using information available from the "
          "National Research Program (NRP) Employment Tax Study for TYs 2008-2010.")
    return {"nmp": nmp, "gaps": gaps}


def alm_erard() -> dict:
    t = text("tul1517.txt")
    t3 = t[t.index("TABLE 3"):t.index("TABLE 4")]
    rows = {}
    for lab in ("Construction", "Total"):
        m = re.search(r"^" + lab + r"\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", t3, re.M)
        rows[lab] = [float(x) for x in m.groups()]
    t2 = t[t.index("TABLE 2"):t.index("TABLE 3")]
    net = float(re.search(r"Total Net Self-employment Income\s+([\d.]+)", t2).group(1))
    mis = float(re.search(r"Total Misclassified Self-employment\s+([\d.]+)", t2).group(1))
    t6 = t[t.index("TABLE 6"):]
    y = {int(m.group(1)): (num(m.group(2)) / 1e6, num(m.group(3)) / 1e6, float(m.group(4)))
         for m in re.finditer(r"^\s*(\d{4})\s+([\d,]+)\s+([\d,]+)\s+([\d.]+)\s*$", t6, re.M)}
    share_income = int(re.search(r"account for about (\d+) percent of total Schedule C net self-", t).group(1))
    share_under = int(re.search(r"but for about (\d+) percent of total Schedule C net income", t).group(1))
    dce = float(re.search(r"categories of \$([\d.]+) billion\. Now our CPS-based", t).group(1))
    ok = (rows["Total"][0] == 159.5 and rows["Total"][2] == 55.7 and rows["Total"][4] == 98.4 and net == 113.9
          and mis == 45.6 and abs(net + mis - rows["Total"][0]) < 1e-9 and y[2001][:2] == (289.913774, 216.772496)
          and len(y) == 17 and share_income == 39 and share_under == 46 and dce == 209.1)
    gate("alm_erard_tables", ok,
         f"Table 3 total CPS {rows['Total'][0]} (Table 2: net SE {net} + misclassified {mis}), tax returns "
         f"{rows['Total'][2]}, audit-adjusted {rows['Total'][4]}; DCE {dce}; 39/46 percent split; Table 6 2001 CPS "
         f"{y[2001][0]:.1f} and returns {y[2001][1]:.1f} ($bn), 17 years 1996-2012")
    quote("tul1517.txt", "p.18-19", "After accounting for undetected noncompliance, the NRP estimates indicate that "
          "the 11 selected industry categories account for about 39 percent of total Schedule C net self- employment "
          "income (with the remaining 61 percent attributable to earnings among industries dominated by formal "
          "suppliers), but for about 46 percent of total Schedule C net income underreporting.")
    quote("tul1517.txt", "Table 3 note", "The tax returns estimate has been corrected by the NRP examiners to include "
          "self-employment earnings erroneously reported as income from another source, such as wages.")
    quote("tul1517.txt", "p.18", "may be an indication that some relatively low-earning informal suppliers, such as "
          "undocumented immigrants, are reluctant to report their income on the CPS survey.")
    # Tax-return over CPS ratios of self-employment income, TY2001: the 11 categories (returns / CPS net SE income,
    # both before the CPS wage misclassification Alm & Erard add) and the rest (Table 6 totals less the categories).
    inf_cps, inf_ret = net, rows["Total"][2]
    for_cps, for_ret = y[2001][0] - inf_cps, y[2001][1] - inf_ret
    rho_inf, rho_for = inf_ret / inf_cps, for_ret / for_cps
    # IRS TY2014-16: nonfarm net misreporting 57%, split as Alm & Erard's NRP split (39% of true income, 46% of
    # underreporting), gives reported/true in each part; their ratio is the relative gap if the CPS captures both
    # parts alike [INFERENCE].
    return {"rho_informal": rho_inf, "rho_formal": rho_for, "relative_2001": rho_inf / rho_for,
            "table3_total": rows["Total"], "table3_construction": rows["Construction"], "cps_net_se": net,
            "cps_misclassified": mis, "table6": {str(k): v for k, v in sorted(y.items())}, "share_income": share_income / 100,
            "share_underreporting": share_under / 100, "dce_bn": dce}


def matched_se_reporting() -> None:
    """A matched check on the level of the self-employment ratios: CPS ASEC respondents linked to their IRS and SSA
    records report more self-employment income to the survey than to the IRS."""
    quote("imboden_voorheis_weber_2022.txt", "abstract", "We show that self-employed individuals report 51 percent "
          "more to the CPS-ASEC than to the IRS, on average.")
    quote("imboden_voorheis_weber_2022.txt", "p.2", "And this difference is 44 percent larger than the same "
          "difference for wage-earners.")


def nmp_split(nmp_all: float, s_inc: float, s_under: float) -> tuple[float, float]:
    """Reported over true income in the informal and formal parts, given the overall net misreporting and the
    informal part's shares of true income and of underreporting."""
    return (s_inc - s_under * nmp_all) / s_inc, ((1 - s_inc) - (1 - s_under) * nmp_all) / (1 - s_inc)


def cells(block: str) -> list[str]:
    return [c.strip("  \xa0\n*") for c in re.split(r"[|\n]", block) if c.strip("  \xa0\n*")]


def row(cs: list[str], label: str, n: int, start: int = 0, skip: tuple[str, ...] = ()) -> list[float]:
    """The first n numbers after the cell `label` (standard errors in parentheses and `skip` labels passed over)."""
    i = cs.index(label, start)
    out = []
    for c in cs[i + 1:]:
        c = c.rstrip("* ")
        if c.startswith("(") or c in skip:
            continue
        if re.fullmatch(r"[−-]?\d+(\.\d+)?", c):
            out.append(num(c))
            if len(out) == n:
                return out
        else:
            break
    raise SystemExit(f"[BLOCKED] Tamborini & Villarreal: row {label!r} has fewer than {n} numbers")


def tamborini_villarreal() -> dict:
    t = text("tv2025_pmc.txt")

    def block(a: str, b: str) -> list[str]:
        i = t.index(a + "\n")
        return cells(t[i:t.index(b, i)])
    t1 = block("Table 1.", "Open in a new tab")
    t2 = block("Table 2.", "Open in a new tab")
    t4 = block("Table 4.", "Notes: Models 4 and 5")
    t6 = block("Table 6.", "Note: Models also control")
    shares = {k: row(t1, k, 2)[1] / 100 for k in ("Immigrant", "Second generation", "Third-plus generation", "White",
                                                   "Black", "Hispanic", "Asian", "Other")}
    tab2 = {k: row(t2, k, 4, skip=("CPS self-employed", "CPS wage/salary worker"))
            for k in ("A. Third-Plus Generation", "B. Immigrant", "C. Second-Generation Immigrant")}
    gen = {"Immigrant": row(t4, "Immigrant", 5), "Second generation": row(t4, "Second generation", 5)}
    race = {k: row(t4, k, 4) for k in ("Black", "Hispanic", "Asian", "Other")}
    mex = row(t6, "Immigrant × Mexican", 3)
    ok = (tab2["A. Third-Plus Generation"] == [3.9, 2.7, 8.0, 85.4] and tab2["B. Immigrant"] == [5.2, 3.0, 13.1, 78.7]
          and tab2["C. Second-Generation Immigrant"] == [3.3, 2.3, 8.4, 86.0]
          and race["Hispanic"] == [-0.087, -0.093, -0.120, -0.107] and race["Black"] == [-0.128, -0.110, -0.129, -0.136]
          and gen["Immigrant"] == [0.040, 0.041, 0.027, 0.029, 0.023] and gen["Second generation"][4] == 0.101
          and mex == [0.008, 0.037, -0.029] and abs(sum(shares[k] for k in ("Immigrant", "Second generation",
                                                                             "Third-plus generation")) - 1) < 1e-9)
    gate("tamborini_villarreal_tables", ok,
         f"Table 2 cells {tab2}; Table 4 Hispanic {race['Hispanic']} (models 2-5), Black {race['Black']}, immigrant "
         f"{gen['Immigrant']}, second generation {gen['Second generation']}; Table 6 Mexican immigrants CPS / tax "
         f"records / difference {mex}; Table 1 matched-sample shares {shares}")
    quote("tv2025_pmc.txt", "Data and Methods", "Note that because survey linkages with administrative records "
          "require respondents to have a corresponding Social Security number in SSA's Numident file, unauthorized "
          "immigrants are essentially excluded from our analytic sample.")
    quote("tv2025_pmc.txt", "Results", "The underreporting of self-employment earnings to tax authorities "
          "(\"under-the-table\" earnings) does not appear to account for the measurement error we observe; if they "
          "did, we would observe a higher rate of immigrants with self-employment earnings in the CPS not reporting "
          "self-employment earnings in their tax records.")
    quote("tv2025_pmc.txt", "Results", "the self-employment of immigrants from Mexico, Central America, and other "
          "Latin American countries is significantly understated in the CPS relative to the administrative records.")
    quote("vt2026_epmc.txt", "abstract", "Using a successful match with Social Security records allows us to rule "
          "out as being unauthorized half of all individuals otherwise classified as unauthorized.")
    # Agreement: the share of CPS self-employed men with a Schedule SE record, by generation (Table 2), weighted by
    # each generation's CPS self-employment in the matched sample (Table 1).
    wgen = {"A. Third-Plus Generation": shares["Third-plus generation"], "B. Immigrant": shares["Immigrant"],
            "C. Second-Generation Immigrant": shares["Second generation"]}
    num_ = sum(wgen[k] * tab2[k][0] for k in wgen)
    den = sum(wgen[k] * (tab2[k][0] + tab2[k][1]) for k in wgen)
    a_bar = num_ / den
    beta = {"Immigrant": gen["Immigrant"][4], "Second generation": gen["Second generation"][4],
            **{k: v[3] for k, v in race.items()}}  # model 5: main-job self-employment, occupation fixed effects
    mean_beta = sum(shares[k] * beta[k] for k in beta)
    return {"a_bar": a_bar, "a_ref": a_bar - mean_beta, "beta_model5": beta, "hispanic_models_2_5": race["Hispanic"],
            "table2": tab2, "shares": shares, "mexican_immigrants_cps_admin_diff": mex}


def ssa_sources() -> dict:
    quote("ssa_note151.txt", "p.2", "3.1 million unauthorized immigrants")
    quote("ssa_note151.txt", "p.2", "working and paying Social Security taxes in 2010")
    quote("ssa_note151.txt", "p.2", "OCACT estimates 1.8 million other immigrants worked")
    quote("ssa_note151.txt", "p.2", "3.9 million other immigrants worked in the underground")
    quote("ssa_note151.txt", "p.2", "and used an SSN that did not match their name in 2010.")
    quote("ssa_note151.txt", "p.2", "as much as $13 billion in payroll taxes to the OASDI")
    quote("ssa_note151.txt", "p.2", "program in 2010, only about $1 billion in benefit pay-")
    quote("ssa_note151.txt", "p.4", "declined to 7.0 million in 2010")
    quote("ssa_note151.txt", "p.4", "be assigned to the Earnings Suspense File. Due to")
    quote("ssa_oig_a0315500058.txt", "p.3", "As of October 2014, the ESF had accumulated over $1.2 trillion in "
          "uncredited wages and 333 million W-2s for TYs 1937 to 2012. Each year, SSA posts to the ESF 3 to 4 percent "
          "of the total W-2s and 1.4 to 1.8 percent of the total wages received from employers.")
    quote("ssa_oig_a0315500058.txt", "p.5", "For TYs 2008 to 2012, SSA suspended about 39 million W-2s, representing "
          "about $373 billion in wages.")
    quote("ssa_oig_022401.txt", "Earnings Suspense File", "As of September 2024, the Earnings Suspense File has "
          "accumulated more than $2.3 trillion in wages and over 415 million wage items for Tax Years 1937 through 2023.")
    quote("ssa_oig_a0321510130.txt", "p.6", "adding about 8 million wage items to the ESF each year.")
    esf_2012, esf_2023 = 1.2e3, 2.3e3  # $bn, cumulative, net of reinstatements
    return {"esf_cumulative_bn": {"TY1937-2012": esf_2012, "TY1937-2023": esf_2023},
            "esf_added_per_year_bn_TY2013_2023": (esf_2023 - esf_2012) / 11, "esf_per_year_bn_TY2008_2012": 373 / 5,
            "note151_2010": {"unauthorized_workers_m": 7.0, "paying_payroll_tax_m": 3.1, "mismatched_ssn_m": 1.8,
                             "underground_m": 3.9}}


def gap_lane() -> dict:
    e = pd.read_csv(GAP / "derived/edges_by_industry.csv").set_index("cell")
    u = pd.read_csv(GAP / "derived/uncovered_summary_by_cell.csv").set_index("cell")
    slopes = {c: {"code": code, "label": lab, "low": float(e.loc[c, "slope_low"]),
                  "central": float(e.loc[c, "slope_central"]), "high": float(e.loc[c, "slope_high"]),
                  "u_cal": float(u.loc[c, "U_cal"])} for c, (code, lab) in GAP_CELLS.items()}
    expect = {"c23": (0.54, 0.60, 0.88), "c56173": (0.29, 0.59, 0.59), "c5617z": (0.31, 0.74, 0.74),
              "c722z": (0.00, 0.01, 0.59)}
    ok = all(tuple(round(slopes[c][k], 2) for k in ("low", "central", "high")) == v for c, v in expect.items())
    gate("compliance_gap_slopes", ok and all(bool(e.loc[c, "priced"]) for c in GAP_CELLS),
         "edges_by_industry.csv low/central/high off-books slopes: " + "; ".join(
             f"{s['label']} {s['low']:.2f}/{s['central']:.2f}/{s['high']:.2f} (calibrated uncovered share "
             f"{s['u_cal']:.3f})" for s in slopes.values()))
    quote("infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md", "Revisions",
          "$2.27bn of the $4.53bn payroll tax")
    quote("infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md", "Revisions",
          "on $18.6bn of the $37.1bn implied off-books payroll")
    quote("infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md", "Test B",
          "Test B brackets the account's assumption; it does not give grounds to move it.")
    quote("infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md", "IRS tax gap",
          "It is inside the adopted account through the September 24 tax correction and is not priced here.")
    quote("infra/immigration-fiscal/compliance_gap_2026_09_24/RESULT.md", "Test B",
          "U is one minus QCEW employment over ACS private wage and salary workers, counted at the place of work.")
    return slopes


def onbooks_shares() -> dict:
    s = pd.read_csv(ONBOOKS / "derived/onbooks_split.csv").set_index("kind")
    out = {c: (float(s.loc[f"evidence_{c}", "s_mex"]), float(s.loc[f"evidence_{c}", "s_oth"])) for c in CASES}
    ok = [tuple(round(x, 3) for x in out[c]) for c in CASES] == [(0.415, 0.401), (0.526, 0.550), (0.635, 0.683)]
    gate("onbooks_shares", ok, f"onbooks_split.csv evidence rows (Mexico-born, other Latin-American-born): {out}")
    quote("infra/immigration-fiscal/onbooks_share_2026_09_23/RESULT.md", "Computation",
          "The script's parameter scales each imputed-unauthorized person's wages, liabilities, FICA-worker flag and "
          "ACTC by one number.")
    quote("infra/immigration-fiscal/onbooks_share_2026_09_23/RESULT.md", "Verdict",
          "Survey under-reporting of off-books pay would lower the effect by $0.9–2.4bn if the CPS misses 10–25% of that "
          "pay; no source measures it for this population.")
    quote("infra/immigration-fiscal/onbooks_share_2026_09_23/RESULT.md", "Survey under-reporting",
          "off-the-books earnings are absent from SSA's earnings records \"though they could be reported in the ASEC\"")
    return out


def industry_labels() -> dict:
    t = text("cpsmar25.txt")
    a = t[t.index("0170     Crop production"):]
    out = {}
    for code in sorted({c for v in INFORMAL.values() for c in v} | {c for c, _ in GAP_CELLS.values()}):
        m = re.search(r"^\s*" + f"{code:04d}" + r"\s+(\S.*?)\s{2,}", a, re.M)
        out[code] = m.group(1).strip() if m else None
    gate("industry_codes_in_the_asec_appendix", all(out.values()) and out[770] == "Construction"
         and out[7770] == "Landscaping services" and out[8680] == "Restaurants and other food services",
         f"{len(out)} codes found in cpsmar25 Appendix A, e.g. 0770 {out[770]!r}, 7690 {out[7690]!r}")
    return out


def cps_documentation() -> None:
    """How the unauthorized enter the ASEC, and what its tax items are (brief item 1)."""
    quote("cpsmar25.txt", "Estimation Procedure", "This survey's estimation procedure adjusts weighted sample results "
          "to agree with independently derived population controls of the civilian noninstitutionalized population")
    quote("cpsmar25.txt", "Estimation Procedure", "Age, sex, and Hispanic origin.")
    quote("cpsmar25.txt", "Estimation Procedure", "Net international migration of the foreign born;")
    quote("asec2025_ddl_pub_full.txt", "Tax Model Items", "SubTopic: Tax Model Items")
    quote("asec2025_ddl_pub_full.txt", "FEDTAX_BC", "Federal income tax liability, before refundable credits")
    quote("asec2025_ddl_pub_full.txt", "STATETAX_A", "State income tax liability, after all credits")
    quote("asec2025_ddl_pub_full.txt", "FICA", "Social security retirement payroll deduction")
    quote("asec2025_ddl_pub_full.txt", "I_ANNVAL", "Values: Levels 1-3 indicate imputations use of income range responses")


# ---------------------------------------------------------------------------------------------- CPS frame
def load() -> pd.DataFrame:
    gate("cps_zip_is_the_pinned_file", sha(f.CPS_ZIP) == f.CPS_SHA, f"{rel(f.CPS_ZIP)} sha256 {f.CPS_SHA[:12]}")
    d = f.load()
    extra = ["PH_SEQ", "PPPOS", "INDUSTRY", "MARG_TAX", "PNSN_VAL", "ANN_VAL", "OI_VAL"]
    with zipfile.ZipFile(f.CPS_ZIP) as z:
        x = pd.read_csv(z.open("pppub25.csv"), usecols=extra)
    aligned = (len(x) == len(d) and np.array_equal(x.PH_SEQ.to_numpy(), d.PH_SEQ.to_numpy())
               and np.array_equal(x.PPPOS.to_numpy(), d.PPPOS.to_numpy()))
    gate("extra_columns_align_with_the_frame", aligned, f"{len(x):,} person records in file order")
    if not aligned:
        raise SystemExit("[BLOCKED] extra CPS columns do not align")
    return pd.concat([d, x.drop(columns=["PH_SEQ", "PPPOS"])], axis=1)


class Frame:
    def __init__(self, d: pd.DataFrame):
        self.d = d
        self.n = len(d)
        self.civ, self.target = f.masks(d)
        self.W = f.weights(d)
        self.ids = d.SPM_ID.to_numpy()
        unauth, latin = f.status(d)
        self.unauth, self.latin = np.asarray(unauth, bool), np.asarray(latin, bool)
        self.row2 = self.unauth & self.latin
        self.mex = d.PENATVTY.eq(303).to_numpy()
        self.ind = d.INDUSTRY.to_numpy()
        self.wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
        self.seinc = np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
        self.pfw = d.FICA.gt(0).to_numpy(float)
        self.fedbc = d.FEDTAX_BC.to_numpy(float)
        self.st = d.STATETAX_A.to_numpy(float)
        self.agi = d.AGI.to_numpy(float)
        self.marg = d.MARG_TAX.to_numpy(float) / 100
        self.size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
        self.spm_codes = pd.factorize(self.ids)[0]
        # Unreported income lowers the liability of the tax-unit member who carries it: a carrier of tax-unit
        # amounts (AGI, liability or marginal rate) for their own income, the unit's largest-AGI carrier otherwise.
        tax = pd.factorize(d.TAX_ID)[0]
        carrier = (self.agi != 0) | (self.fedbc != 0) | (self.marg != 0)
        head = (pd.DataFrame({"u": tax, "a": np.abs(self.agi), "i": np.arange(self.n)})
                .sort_values(["u", "a", "i"], ascending=[True, False, True]).drop_duplicates("u").set_index("u").i)
        self.holder = np.where(carrier, np.arange(self.n), head.to_numpy()[tax])
        # Tamborini & Villarreal's groups: Hispanic of any race, else White, Black, Asian or Other; immigrant
        # (born abroad, not a citizen at birth), second generation (a parent born abroad) or third-plus.
        hisp = d.PEHSPNON.eq(1).to_numpy()
        race = d.PRDTRACE.to_numpy()
        self.tv_race = np.where(hisp, "Hispanic", np.where(race == 1, "White", np.where(race == 2, "Black",
                                np.where(race == 4, "Asian", "Other"))))
        foreign = d.PRCITSHP.isin([4, 5]).to_numpy()
        parent_abroad = ~(d.PEFNTVTY.isin(US_BIRTH).to_numpy() & d.PEMNTVTY.isin(US_BIRTH).to_numpy())
        self.tv_gen = np.where(foreign, "Immigrant", np.where(parent_abroad, "Second generation", "Third"))
        self.no_degree = d.A_HGA.lt(BACHELOR).to_numpy()
        g, _ = cbo_arm.groups(d)
        self.g = g

    def scale(self, s_mex: float, s_oth: float, mask: np.ndarray | None = None) -> np.ndarray:
        m = self.row2 if mask is None else mask
        return np.where(m, np.where(self.mex, s_mex, s_oth), 1.0)

    def vectors(self, uw=None, us=None, ui=None, scale=None, dres=None) -> dict:
        """The account's receipt key vectors (personal) after unreported wages uw and self-employment income us
        (both leave the payroll and income-tax keys), income unreported for income tax only ui, the row-2 scale
        and an addition to SPM resources."""
        z = np.zeros(self.n)
        uw, us, ui = (z if x is None else x for x in (uw, us, ui))
        scale = np.ones(self.n) if scale is None else scale
        wage = np.maximum(self.wage - uw, 0)
        ratio = np.divide(wage, self.wage, out=np.ones(self.n), where=self.wage > 0)
        se = .9235 * np.maximum(self.seinc - us, 0)
        se = np.where(se >= 400, se, 0)
        se_capped = np.minimum(se, np.maximum(f.OASDI_MAX - np.minimum(wage, f.OASDI_MAX), 0))
        U = np.bincount(self.holder, weights=uw + us + ui, minlength=self.n)
        fed = np.maximum(self.fedbc - self.marg * U, 0)
        st0 = np.clip(self.st, 0, None)
        st = np.where(self.agi > 0, st0 * np.clip(1 - U / np.where(self.agi > 0, self.agi, 1), 0, 1), st0)
        v = {"wage": wage, "wage_oasdi": np.minimum(wage, f.OASDI_MAX), "self_payroll": .124 * se_capped + .029 * se,
             "positive_fica_worker": self.pfw * ratio, "federal_liability": fed, "state_liability": st}
        v = {k: x * scale for k, x in v.items()}
        res = self.d.SPM_RESOURCES.to_numpy(float)
        if dres is not None:
            res = res + np.bincount(self.spm_codes, weights=dres)[self.spm_codes]
        v["consumption"] = np.clip(res, 0, None) / self.size
        return v

    def unpaid(self, scale: np.ndarray) -> np.ndarray:
        """Resources an off-books part keeps: its modelled FICA, federal tax before refundable credits and state tax,
        less the credits the audit's rules deny (all EITC and the off-books part of ACTC)."""
        d = self.d
        off = 1 - scale
        flagged = scale < 1
        return (off * (d.FICA.to_numpy(float) + self.fedbc + self.st)
                - np.where(flagged, d.EIT_CRED.to_numpy(float), 0) - off * d.ACTC_CRD.to_numpy(float))


def shares(F: Frame, v: dict, K: dict, lines: dict, W: np.ndarray) -> dict:
    """{(line, allocation): share array over the weight columns}: the target's share of the key over the civilian
    universe or, on the part of a line CBO's gradient covers (all of it, or the federal part of excise), the sum over
    CBO groups of the case's fixed group weight K[j] times the target's share of the key inside group j. An item
    therefore moves only the within-group shares there: CBO's between-group distribution comes from tax returns
    and already reflects compliance by income group."""
    out = {}
    cache = {}
    for line, (key, spec, part) in lines.items():
        for a in ALLOCS:
            if (key, a) not in cache:
                x = v[key] if a == "personal" else f.unit_equal(v[key], F.ids)
                raw = (x[F.target] @ W[F.target]) / (x[F.civ] @ W[F.civ])
                theta = {}
                for j in f.GROUPS:
                    m = F.civ & (F.g == j)
                    mt = m & F.target
                    den = x[m] @ W[m]
                    theta[j] = np.divide(x[mt] @ W[mt], den, out=np.zeros_like(den), where=den != 0)
                cache[(key, a)] = (raw, theta)
            raw, theta = cache[(key, a)]
            out[(line, a)] = raw if spec is None else (
                part * sum(K[(line, a)][j] * theta[j] for j in f.GROUPS) + (1 - part) * raw)
    return out


def main() -> int:
    OUT.mkdir(exist_ok=True)
    manifest = manifest_ok()
    irs = irs_1415()
    ae = alm_erard()
    tv = tamborini_villarreal()
    ssa = ssa_sources()
    slopes = gap_lane()
    ob = onbooks_shares()
    labels = industry_labels()
    cps_documentation()
    matched_se_reporting()

    d = load()
    F = Frame(d)
    W = F.W
    model = json.loads(f.MODEL.read_text())
    ref = model["receipts"]["reference"]
    national = {l["id"]: l["national_bn"] for l in model["receipts"]["lines"]}
    trans = pd.read_csv(BENCH / "derived/cbo_translation.csv")
    part = {}  # the share of the line CBO's gradient re-keys (the federal part of excise; all of the others)
    for line, spec in CBO_SPEC.items():
        r = trans.query("spec == @spec and line == @line")
        part[line] = float(r.national_bn.iloc[0]) / national[line]
    lines = {}
    for l in model["receipts"]["lines"]:
        key = l["cells"][ref]["shared"]["key"]
        if key in KEYS:
            lines[l["id"]] = (key, CBO_SPEC.get(l["id"]), part.get(l["id"], 0.0))
    gate("receipt_lines_on_the_seven_keys", sorted(lines) == sorted([
        "federal_income_tax", "state_local_income_tax", "other_personal_tax", "employee_oasdi", "employee_hi",
        "self_employment_oasdi_hi", "employer_oasdi", "employer_hi", "other_domestic_social_contributions",
        "corporate_labor", "general_sales_tax", "excise_selective_sales", "customs_duties",
        "personal_current_transfers"]), f"{len(lines)} receipt lines keyed by {', '.join(KEYS)}")

    # ------------------------------------------------------------ gates: the keys, CBO's gradient and row 2
    raw_v = F.vectors()
    frame_v = f.receipt_vectors(d)
    gate("key_vectors_are_the_accounts", all(np.array_equal(raw_v[k], frame_v[k]) for k in KEYS),
         "vectors() with no change equals frame.receipt_vectors (full_account_receipts builder::derive_keys) for "
         "the seven keys, element for element")
    # Why an item moves only the within-group shares where CBO's gradient applies: CBO's between-group distribution
    # is measured on tax records, so it already carries compliance by income group.
    quote("infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md", "Definitions differ",
          "CBO measures income from tax records and administrative transfers")
    cbo_rows = pd.read_csv(BENCH / "derived/cbo_group_shares.csv")
    cbo = {spec: {j: float(cbo_rows.query("spec == @spec and group == @j").cbo_share.iloc[0]) for j in f.GROUPS}
           for spec in set(CBO_SPEC.values())}
    # The case's group weights (cbo_arm.py): CBO's shares for a one-line concept; for payroll, each line's own
    # distribution scaled by CBO over the amount-weighted composite of the five lines (ratio_target), point values.
    K = {}
    w0 = W[:, 0]
    pay = [x for x, sp in CBO_SPEC.items() if sp == "payroll_taxes|2022"]
    pis = {x: cbo_arm.decompose(raw_v[lines[x][0]], w0, F.civ, F.target, F.g)[0] for x in pay}
    comp = {j: sum(national[x] * pis[x][j] for x in pay) / sum(national[x] for x in pay) for j in f.GROUPS}
    for line, spec in CBO_SPEC.items():
        for a in ALLOCS:
            if line not in pay:
                K[(line, a)] = cbo[spec]
                continue
            new = cbo_arm.ratio_target(pis[line], comp, cbo[spec])
            va = raw_v[lines[line][0]] if a == "personal" else f.unit_equal(raw_v[lines[line][0]], F.ids)
            pa = cbo_arm.decompose(va, w0, F.civ, F.target, F.g)[0]
            K[(line, a)] = {j: (new[j] / pis[line][j] * pa[j] if pis[line][j] else 0.0) for j in f.GROUPS}
    no_cbo = {line: (key, None, 0.0) for line, (key, _, _) in lines.items()}
    all_cbo = {line: (key, spec, 1.0) for line, (key, spec, _) in lines.items() if spec}
    s_raw = shares(F, raw_v, K, no_cbo, W)
    s_cbo = shares(F, raw_v, K, all_cbo, W)
    dev = max(abs(s_raw[(line, a)][0] - l["cells"][ref][a]["target_bn"] / l["national_bn"])
              for l in model["receipts"]["lines"] if l["id"] in lines for line in [l["id"]] for a in ALLOCS)
    gate("raw_shares_are_model_json", dev < 1e-9, f"largest gap between the rebuilt share and model.json's reference "
         f"cell over {len(lines)} lines x 2 allocations: {dev:.1e}")
    worst = 0.0
    for line, spec in CBO_SPEC.items():
        for a in ALLOCS:
            r = trans.query("spec == @spec and line == @line and allocation == @a")
            dev_line = max(abs(float(r.reweighted_share.iloc[0]) - s_cbo[(line, a)][0]),
                           abs(float(r.account_share.iloc[0]) - s_raw[(line, a)][0]))
            if dev_line > 1e-12:
                print(f"  ! {line} {a}: reweighted {float(r.reweighted_share.iloc[0]):.9f} vs {s_cbo[(line, a)][0]:.9f}, "
                      f"account {float(r.account_share.iloc[0]):.9f} vs {s_raw[(line, a)][0]:.9f}")
            worst = max(worst, dev_line)
    gate("cbo_gradient_reproduces_the_benchmark_lane", worst < 1e-12
         and all(abs(part[x] - 1) < 1e-12 for x in CBO_SPEC if x != "excise_selective_sales")
         and 0.2 < part["excise_selective_sales"] < 0.3,
         f"reweighted and account shares of the {len(CBO_SPEC)} lines the case re-keys with CBO's gradient equal "
         f"cbo_translation.csv to {worst:.1e} (federal income tax shared {s_cbo[('federal_income_tax', 'shared')][0]:.6f}); "
         f"the gradient covers each whole line but excise, where it covers the federal part, "
         f"{part['excise_selective_sales']:.4f} of the line")
    stacks = json.loads(STACK_CACHE.read_text())
    row2_worst = 0.0
    for c in CASES:
        v2 = F.vectors(scale=F.scale(*ob[c]))
        s2 = shares(F, v2, K, no_cbo, W)
        p = stacks[f"origin|{c}|audit_rules_alone"]["receipts"]
        for line in lines:
            for a in ALLOCS:
                want = p.get(line, {}).get(a, 0.0)
                row2_worst = max(row2_worst, abs(national[line] * (s2[(line, a)][0] - s_raw[(line, a)][0]) - want))
    gate("row_2_reproduces_the_cps_lane", row2_worst < 1e-6,
         f"on-books scaling of the paper flag's Latin-American-born unauthorized at the three cases reproduces "
         f"origin|<case>|audit_rules_alone ({rel(STACK_CACHE)}, sha256 {sha(STACK_CACHE)[:12]}) for every line to "
         f"{row2_worst:.1e}bn")

    # ------------------------------------------------------------ item 1: what row 2 already takes off the books
    w0 = W[:, 0]
    tot = lambda x, m: float((x * w0)[m & F.civ].sum() / 1e9)  # noqa: E731
    s_c = F.scale(*ob["central"])
    check_rows = []
    for cell, sl in slopes.items():
        m = F.ind == sl["code"]
        for who, mask in (("mexico_born", F.row2 & F.mex), ("other_latin_american_born", F.row2 & ~F.mex)):
            wages = tot(F.wage, m & mask)
            check_rows.append([sl["label"], who, wages, tot(F.wage * (1 - s_c), m & mask),
                               sl["low"] * wages, sl["central"] * wages, sl["high"] * wages])
    for who, mask in (("mexico_born", F.row2 & F.mex), ("other_latin_american_born", F.row2 & ~F.mex)):
        four = np.isin(F.ind, [s["code"] for s in slopes.values()])
        check_rows.append(["all industries", who, tot(F.wage, mask), tot(F.wage * (1 - s_c), mask),
                           None, None, None])
        check_rows.append(["outside the four", who, tot(F.wage, mask & ~four), tot(F.wage * (1 - s_c), mask & ~four),
                           0.0, 0.0, 0.0])
    off = pd.DataFrame(check_rows, columns=["industry", "flagged", "cps_wages_bn", "row2_off_books_bn",
                                            "slope_low_bn", "slope_central_bn", "slope_high_bn"])
    mx = off[(off.flagged == "mexico_born") & off.industry.isin([s["label"] for s in slopes.values()])]
    item1 = {"mexico_born_wages_bn": tot(F.wage, F.row2 & F.mex & F.target),
             "row2_removes_mexico_born_wages_bn": tot(F.wage * (1 - s_c), F.row2 & F.mex & F.target),
             "four_industries_row2_bn": float(mx.row2_off_books_bn.sum()),
             "four_industries_slopes_bn": {k: float(mx[f"slope_{k}_bn"].sum()) for k in ("low", "central", "high")},
             "flagged_persons_m": {"mexico_born_in_group": float(w0[F.row2 & F.mex & F.target].sum() / 1e6),
                                   "other_latin_american_born": float(w0[F.row2 & ~F.mex & F.civ].sum() / 1e6),
                                   "born_elsewhere": float(w0[F.unauth & ~F.latin & F.civ].sum() / 1e6),
                                   "born_elsewhere_no_degree": float(w0[F.unauth & ~F.latin & F.no_degree & F.civ].sum() / 1e6)},
             "social_security_received_by_flagged_bn": tot(d.SS_VAL.to_numpy(float), F.unauth)}
    inf = np.isin(F.ind, [c for v in INFORMAL.values() for c in v])
    se_mix = {"informal_share_of_cps_se_income": {"all": tot(F.seinc, inf) / tot(F.seinc, F.civ),
                                                  "group": tot(F.seinc, inf & F.target) / tot(F.seinc, F.target),
                                                  "others": tot(F.seinc, inf & ~F.target) / tot(F.seinc, F.civ & ~F.target)},
              "cps_se_income_bn": {"all": tot(F.seinc, F.civ), "group": tot(F.seinc, F.target)},
              "alm_erard_informal_share_2001": ae["cps_net_se"] / ae["table6"]["2001"][0]}
    gate("informal_mapping_matches_alm_erard_share", abs(se_mix["informal_share_of_cps_se_income"]["all"]
                                                         - se_mix["alm_erard_informal_share_2001"]) < 0.05,
         f"the 11 categories hold {se_mix['informal_share_of_cps_se_income']['all']:.3f} of CPS 2025 self-employment "
         f"income, against {se_mix['alm_erard_informal_share_2001']:.3f} in Alm & Erard's CPS for 2001 "
         f"({ae['cps_net_se']} of {ae['table6']['2001'][0]:.1f}); the group {se_mix['informal_share_of_cps_se_income']['group']:.3f}")

    # ------------------------------------------------------------ items
    rho = {"central": (ae["rho_informal"], ae["rho_formal"])}
    rep_inf, rep_for = nmp_split(irs["nmp"]["nonfarm_proprietor"], ae["share_income"], ae["share_underreporting"])
    rel_2016 = rep_inf / rep_for
    rho["low"] = (ae["rho_formal"] * rel_2016, ae["rho_formal"])
    dce_inf = ae["table3_total"][2] / ae["dce_bn"]
    dce_for = (ae["table6"]["2001"][1] - ae["table3_total"][2]) / (ae["dce_bn"] / ae["share_income"] - ae["dce_bn"])
    gate("self_employment_ratios", 0.45 < ae["rho_informal"] < 0.52 and 0.88 < ae["rho_formal"] < 0.95
         and abs(dce_inf / dce_for - ae["relative_2001"]) < 0.02,
         f"tax returns / CPS, TY2001: informal {ae['rho_informal']:.4f}, formal {ae['rho_formal']:.4f}, ratio "
         f"{ae['relative_2001']:.4f}; the same ratio on DCE-adjusted true income {dce_inf:.4f}/{dce_for:.4f} = "
         f"{dce_inf / dce_for:.4f}; TY2014-16 at 57% with the 39/46 split: {rep_inf:.4f}/{rep_for:.4f} = {rel_2016:.4f}")

    def rho_of(case: str) -> np.ndarray:
        ri, rf = rho[case]
        return np.where(inf, ri, rf)

    t_factor = np.ones(F.n)
    beta = tv["beta_model5"]
    for k in ("Black", "Hispanic", "Asian", "Other"):
        t_factor += np.where(F.tv_race == k, beta[k], 0) / tv["a_ref"]
    for k in ("Immigrant", "Second generation"):
        t_factor += np.where(F.tv_gen == k, beta[k], 0) / tv["a_ref"]
    t_factor = np.where(F.row2, 1.0, t_factor)  # the matched sample excludes the unauthorized
    base_scale = s_c

    def se_us(case: str, with_tv: bool = False) -> np.ndarray:
        c = rho_of(case) * (t_factor if with_tv else 1)
        return (1 - np.clip(c, 0, 1)) * F.seinc

    types = {"wages": d.WSAL_VAL.clip(lower=0), "interest": d.INT_VAL.clip(lower=0), "dividends": d.DIV_VAL.clip(lower=0),
             "rents": d.RNT_VAL.clip(lower=0), "capital_gains": d.CAP_VAL.clip(lower=0),
             "pensions": d.PNSN_VAL.clip(lower=0) + d.ANN_VAL.clip(lower=0), "unemployment": d.UC_VAL.clip(lower=0),
             "other_income": d.OI_VAL.clip(lower=0)}
    ui_nmp = sum(irs["nmp"][k] * types[k].to_numpy(float) for k in types)

    def c_scale(which: str, base: np.ndarray = base_scale) -> np.ndarray:
        s = base.copy()
        for sl in slopes.values():
            m = F.row2 & (F.ind == sl["code"])
            s = np.where(m, 1 - sl[which], s)
        return s

    def d_scale(s_other: float, restricted: bool, s: np.ndarray) -> np.ndarray:
        m = F.unauth & ~F.latin & (F.no_degree if restricted else True)
        return np.where(m, s_other, s)

    uw_bound = np.zeros(F.n)
    for sl in slopes.values():
        uw_bound = np.where(~F.row2 & (F.ind == sl["code"]), max(sl["u_cal"], 0) * F.wage, uw_bound)

    s_oth = ob["central"][1]
    specs = {
        ("se_industry", "central"): dict(us=se_us("central")),
        ("se_industry", "low"): dict(us=se_us("low")),
        ("se_industry", "high"): dict(us=se_us("central", True)),
        ("income_nmp", "central"): dict(us=se_us("central"), ui=ui_nmp),
        ("slopes", "central"): dict(scale=c_scale("central")),
        ("slopes", "low"): dict(scale=c_scale("low")),
        ("slopes", "high"): dict(scale=c_scale("high")),
        ("other_unauth", "central"): dict(scale=d_scale(s_oth, True, base_scale)),
        ("other_unauth", "share_0683"): dict(scale=d_scale(ob["high"][1], True, base_scale)),
        ("other_unauth", "share_0401"): dict(scale=d_scale(ob["low"][1], True, base_scale)),
        ("other_unauth", "every_flagged"): dict(scale=d_scale(s_oth, False, base_scale)),
        ("cash_consumption", "central"): dict(dres=F.unpaid(base_scale)),
        ("authorized_bound", "bound"): dict(uw=uw_bound),
    }
    # All together, at one on-books case throughout (row 2's shares and the other-origin share move together, since
    # one SSA count sets both): the central case; the low-cost end at the on-books lane's high shares with every
    # other item at its low-cost reading; the high-cost end at its low shares with every other item at its high-cost
    # reading. The low- and high-cost ends are measured against the case with row 2 at those shares, and
    # price.cjs applies them to the package's low and high stacks.
    row2_case = {}
    # (on-books case, slope reading, self-employment reading, with Tamborini & Villarreal's factor)
    # The same readings with row 2 held at the central shares isolate what the items add to the case.
    ends = {"central": ("central", "central", "central", False), "low_cost": ("high", "low", "low", False),
            "high_cost": ("low", "high", "central", True),
            "low_cost_central_case": ("central", "low", "low", False),
            "high_cost_central_case": ("central", "high", "central", True)}
    for case, (rc, sl_case, se_case, with_tv) in ends.items():
        sc = d_scale(ob[rc][1], True, c_scale(sl_case, F.scale(*ob[rc])))
        specs[("all", case)] = dict(us=se_us(se_case, with_tv), scale=sc, dres=F.unpaid(sc))
        row2_case[("all", case)] = rc
    # Row 2 itself by this lane's rule, to set against the package's own stacks for the same change (price.cjs):
    # full compliance for the flagged, and the on-books lane's low and high shares.
    specs[("row2_r_route", "without")] = dict(scale=np.ones(F.n))
    for c in ("low", "high"):
        specs[("row2_r_route", c)] = dict(scale=F.scale(*ob[c]))
    bases = {c: shares(F, F.vectors(scale=F.scale(*ob[c])), K, lines, W) for c in CASES}
    bases_raw = {c: shares(F, F.vectors(scale=F.scale(*ob[c])), K, no_cbo, W) for c in CASES}

    # Calibration to the case's basis. The case's stacks apply row 2 on the state-aware flag, with row 4's weights
    # and each fill-in method's re-imputed keys; the items here use the paper flag and the published keys. Row 2's
    # own effect measures the gap: for each case, line and allocation, c is the factor on the group's own part that
    # makes this lane's relative change for "without row 2" equal the package's (stack alone against the stack for
    # the case, the two methods averaged). Others' part is taken as measured here: the fill-in methods and row 4
    # act on the group. The consumption lines, which row 2 does not touch, take the unpaid-tax lines' c, weighted
    # by the group's own part.
    t0 = {(l["id"], a): l["cells"][ref][a]["target_bn"] for l in model["receipts"]["lines"] for a in ALLOCS}
    pay_d = lambda k, c, line, a: stacks[f"row4+status_state_aware|{c}|{k}"]["receipts"].get(line, {}).get(a, 0.0)  # noqa: E731
    calib, calib_rows = {}, []
    for rc in CASES:
        b = F.scale(*ob[rc])
        sb = bases_raw[rc]
        sJ, sG, sO = (shares(F, F.vectors(scale=sc), K, no_cbo, W)
                      for sc in (np.ones(F.n), np.where(F.target, 1.0, b), np.where(F.target, b, 1.0)))
        c = {}
        for line in lines:
            for a in ALLOCS:
                k = (line, a)
                tc = t0[k] + np.mean([pay_d(m, rc, line, a) for m in METHODS])
                rel_pkg = np.mean([pay_d(m, "alone", line, a) - pay_d(m, rc, line, a) for m in METHODS]) / tc if tc else 0.0
                gJ, gG, gO = ((x[k][0] - sb[k][0]) / sb[k][0] for x in (sJ, sG, sO))
                c[k] = (rel_pkg - gO) / gG if abs(gG) > 1e-9 else None
                calib_rows.append([rc, line, a, rel_pkg, gJ, gG, gO, c[k]])
        for a in ALLOCS:
            wts = {u: bases_raw[rc][(u, a)][0] * national[u] * ((sG[(u, a)][0] - sb[(u, a)][0]) / sb[(u, a)][0])
                   for u in UNPAID_LINES}
            c_unpaid = sum(c[(u, a)] * wts[u] for u in UNPAID_LINES) / sum(wts.values())
            for line in lines:
                if c[(line, a)] is None:
                    c[(line, a)] = c_unpaid
        calib[rc] = c
    calibration = pd.DataFrame(calib_rows, columns=["case", "line", "allocation", "package_relative_change",
                                                    "paper_joint", "paper_group_part", "paper_others_part", "c"])
    calibration["c_applied"] = [calib[r.case][(r.line, r.allocation)] for r in calibration.itertuples()]
    touched = calibration[calibration.package_relative_change.abs() > 1e-9]
    gate("calibration_factors_are_bounded", bool(touched.c.between(0.5, 1.5).all()),
         f"c on the group's own part, over {len(touched)} line x allocation x case cells row 2 touches: "
         f"{touched.c.min():.3f} to {touched.c.max():.3f} (federal income tax at central "
         f"{calib['central'][('federal_income_tax', 'shared')]:.3f} shared, payroll "
         f"{calib['central'][('employee_oasdi', 'shared')]:.3f})")

    items, rows = {}, []
    for (item, variant), kw in specs.items():
        kw = dict(kw)
        kw.setdefault("scale", base_scale)
        rc = row2_case.get((item, variant), "central")
        base, base_raw = bases[rc], bases_raw[rc]
        v = F.vectors(**kw)
        s, s_raw_item = shares(F, v, K, lines, W), shares(F, v, K, no_cbo, W)
        # The item's flag-based changes (on-books scale, resources added back) on group members alone: the part
        # the calibration moves.
        b_rc = F.scale(*ob[rc])
        kw_g = {"scale": np.where(F.target, kw["scale"], b_rc)}
        if kw.get("dres") is not None:
            kw_g["dres"] = kw["dres"] * F.target
        v_g = F.vectors(**kw_g)
        s_g, s_g_raw = shares(F, v_g, K, lines, W), shares(F, v_g, K, no_cbo, W)
        out = {}
        for line, (key, spec, _) in lines.items():
            out[line] = {}
            for a in ALLOCS:
                k = (line, a)
                r = s[k] / base[k]
                r_raw = s_raw_item[k] / base_raw[k]
                c = calib[rc][k]
                r_cal = r[0] + (c - 1) * (s_g[k][0] / base[k][0] - 1)
                r_cal_raw = r_raw[0] + (c - 1) * (s_g_raw[k][0] / base_raw[k][0] - 1)
                out[line][a] = {"r": float(r[0]), "r_se": f.sdr(r), "r_raw": float(r_raw[0]), "r_cal": float(r_cal),
                                "r_cal_raw": float(r_cal_raw)}
                rows.append([item, variant, rc, line, a, key, spec or "", base[k][0], s[k][0], r[0], f.sdr(r),
                             r_raw[0], r_cal, r_cal_raw, national[line] * (s[k][0] - base[k][0])])
        items.setdefault(item, {})[variant] = {"row2_case": rc, "lines": out}
    # By construction the calibrated raw ratio for "without row 2" reproduces the package's relative change, up to
    # the group and others' parts not adding exactly.
    w = items["row2_r_route"]["without"]["lines"]
    pkg_rel = calibration.query("case == 'central'").set_index(["line", "allocation"]).package_relative_change
    gap = max(abs(w[line][a]["r_cal_raw"] - 1 - pkg_rel[(line, a)]) / abs(pkg_rel[(line, a)])
              for line in lines for a in ALLOCS if abs(pkg_rel[(line, a)]) > 1e-9)
    gate("calibration_reproduces_the_package_row_2", gap < 0.02,
         f"the calibrated raw ratio for row 2 removed equals the package's relative change (stacks alone against "
         f"central) line by line to {gap:.2%} of it, the gap being the parts' non-additivity")
    gate("central_base_is_the_row_2_scale", np.array_equal(base_scale, F.scale(*ob["central"])),
         "the items' base is the key with row 2 at the central on-books shares")
    ratios = pd.DataFrame(rows, columns=["item", "variant", "row2_case", "line", "allocation", "key", "cbo_spec",
                                         "share_before", "share_after", "r", "r_se", "r_raw", "r_cal", "r_cal_raw",
                                         "change_on_model_national_bn"])
    # Items that do not touch a key leave its lines unchanged (r = 1 exactly), and no item moves corporate_labor
    # into the case (its receipt is indirect, response 0).
    untouched = ratios[(ratios.item == "cash_consumption") & (ratios.key != "consumption")]
    gate("items_touch_only_their_keys", bool((untouched.r == 1).all())
         and bool((ratios[(ratios.item == "slopes") & (ratios.key == "consumption")].r == 1).all()),
         "the consumption item leaves every tax key's lines at r = 1 and the slope item leaves the consumption lines")

    # ------------------------------------------------------------ evidence table
    evidence = [
        ["on-books share, Mexico-born imputed unauthorized", ob["central"][0], f"{ob['low'][0]}-{ob['high'][0]}",
         "measured head count (SSA 2010) carried to 2024 dollars with assumed erosion, protected share and pay ratio",
         "onbooks_share_2026_09_23"],
        ["tax-return / CPS self-employment income, informal categories, TY2001", ae["rho_informal"], "",
         "measured (NRP-corrected returns against the CPS, 11 categories)", "Alm & Erard Tables 2-3"],
        ["tax-return / CPS self-employment income, other industries, TY2001", ae["rho_formal"], "",
         "measured (SOI totals less the 11 categories against CPS totals)", "Alm & Erard Tables 3 and 6"],
        ["relative reporting, informal over other, TY2014-16", rel_2016, "",
         "IRS NMP 57% measured; the 39/46 split carried from TY2001 [assumed]", "Pub 1415 Table 5; Alm & Erard"],
        ["Hispanic gap in having a Schedule SE record given CPS self-employment (model 5)", beta["Hispanic"],
         ", ".join(f"{x:+.3f}" for x in tv["hispanic_models_2_5"]), "measured, matched CPS-SSA, SSN holders only",
         "Tamborini & Villarreal Table 4"],
        ["share of CPS self-employed with a Schedule SE record", tv["a_bar"], "", "measured (Table 2, weighted)",
         "Tamborini & Villarreal Tables 1-2"],
        ["off-books share of imputed-unauthorized wage workers, construction", slopes["c23"]["central"],
         f"{slopes['c23']['low']:.2f}-{slopes['c23']['high']:.2f}", "association across states; level check allows 0",
         "compliance_gap_2026_09_24"],
        ["on-books share, imputed unauthorized born outside Latin America", s_oth,
         f"{ob['low'][1]}-{ob['high'][1]}", "assumed: the case's other-origin share", "onbooks_share_2026_09_23"],
        ["employer FICA/FUTA underreporting, TY2014-16 ($bn)", irs["gaps"]["fica_futa_underreporting_bn"], "",
         "measured (NRP employment-tax study TY2008-10 rates); excludes household and farm employers", "Pub 1415"],
        ["self-employment tax gap, TY2014-16 ($bn)", irs["gaps"]["se_underreporting_bn"] + irs["gaps"]["se_nonfiling_bn"],
         "", "measured (underreporting 53 + nonfiling 7)", "Pub 1415 Table 2"],
        ["suspense-file wages added per year, TY2013-2023 ($bn)", ssa["esf_added_per_year_bn_TY2013_2023"], "",
         "measured cumulative totals, net of reinstatement", "SSA OIG A-03-15-50058, 022401"],
    ]
    pd.DataFrame(evidence, columns=["parameter", "value", "range", "status", "source"]).to_csv(
        OUT / "evidence.csv", index=False, lineterminator="\n")

    failed = [g for g in GATES if not g[1]]
    (OUT / "gates.json").write_text(json.dumps([{"gate": n, "pass": p, "detail": x} for n, p, x in GATES],
                                               indent=1) + "\n")
    if failed:
        for n, _, x in failed:
            print(f"[BLOCKED] gate {n}: {x}")
        return 1
    ratios.to_csv(OUT / "item_ratios.csv", index=False, lineterminator="\n", float_format="%.12g")
    off.to_csv(OUT / "item1_off_books_check.csv", index=False, lineterminator="\n", float_format="%.6f")
    calibration.to_csv(OUT / "calibration.csv", index=False, lineterminator="\n", float_format="%.9g")
    pd.DataFrame(QUOTES).to_csv(OUT / "quotes.csv", index=False, lineterminator="\n")
    with (OUT / "industry_map.csv").open("w", newline="") as h:
        wr = csv.writer(h, lineterminator="\n")
        wr.writerow(["category", "code", "asec_2025_label", "cps_se_income_bn", "group_cps_se_income_bn"])
        for cat, codes in INFORMAL.items():
            for c in codes:
                wr.writerow([cat, f"{c:04d}", labels[c], f"{tot(F.seinc, F.ind == c):.4f}",
                             f"{tot(F.seinc, (F.ind == c) & F.target):.4f}"])
    meta = {
        "sources": {n: {"sha256": e["sha256"], "url": e.get("final_url") or e["url"], "publisher_url": e["publisher_url"]}
                    for n, e in sorted(manifest.items())},
        "inputs": {rel(p): sha(p) for p in [f.CPS_ZIP, f.MODEL, BENCH / "derived/cbo_group_shares.csv",
                                            BENCH / "derived/cbo_translation.csv", STACK_CACHE,
                                            GAP / "derived/edges_by_industry.csv",
                                            GAP / "derived/uncovered_summary_by_cell.csv",
                                            ONBOOKS / "derived/onbooks_split.csv"]},
        "parameters": {"onbooks": ob, "rho": rho, "relative_informal_TY2014_16": rel_2016,
                       "tamborini_villarreal": tv, "slopes": slopes, "irs": irs, "ssa": ssa,
                       "alm_erard": {k: v for k, v in ae.items() if k != "table6"}},
        "item1": item1, "self_employment_mix": se_mix, "methods": list(METHODS),
        "rule": "r = the group's share after the item over its share with row 2 at the variant's on-books case "
                "(row2_case; central unless stated), per line and allocation; CBO's income gradient is kept for the "
                "lines the case re-keys with it, so the item moves only the group's shares inside CBO's income "
                "groups. r_raw is the same ratio on the raw shares. r_cal and r_cal_raw move the group's own part of "
                "the item's flag-based changes by the calibration factor c (calibration.csv): r_cal = r + (c - 1) x "
                "(r_group - 1). price.cjs moves each line's group amount in the package's model for row2_case by "
                "(ratio - 1) x that amount.",
    }
    (OUT / "items.json").write_text(json.dumps({"meta": meta, "items": items}, indent=1, sort_keys=True) + "\n")
    for n, _, x in GATES:
        print(f"  ✓ {n}: {x[:150]}")
    print(f"items: {', '.join(sorted(items))}; {len(ratios)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
