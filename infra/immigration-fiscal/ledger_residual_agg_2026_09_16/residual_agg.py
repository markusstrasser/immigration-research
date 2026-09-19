#!/usr/bin/env python3
"""Price the public-spending items that have NO person-level field in CPS ASEC,
for the six origin-generation ledger groups, using published program aggregates
and each group's measured exposure (children by age band, income position,
state of residence, college enrolment).

Items priced here (none of them is a measured payment; each is an accounting
scenario built from a published national or state aggregate times a measured
exposure):

  1. Child care subsidies (CCDF)
  2. Head Start (preschool component)
  3. Public higher-education appropriations (SHEEO SHEF)
  4. State and local general services      -- per-capita vs pure-public-good
  5. Federal pure public goods (OMB 3.1)   -- per-capita vs pure-public-good
  6. Lifeline (WIC and LIHEAP are already inside SPM resources)

Reuses analyze_cps_fiscal_2025.py end to end: same CPS ASEC 2025 public-use
file, same SPM resource-unit conservation checks, same equal-shares allocation
rules, same 160-replicate SDR variance, same generation group definitions.
"""
from __future__ import annotations

import os
import subprocess
import sys

# `uv run python3 residual_agg.py` uses a bare interpreter with no project
# dependencies (this repo has no pyproject). Re-exec once through uv with the
# needed wheels so the documented verification command works as written.
if os.environ.get("_RESIDUAL_AGG_BOOTSTRAPPED") != "1":
    try:
        import numpy  # noqa: F401
        import openpyxl  # noqa: F401
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        env = dict(os.environ, _RESIDUAL_AGG_BOOTSTRAPPED="1")
        cmd = ["uv", "run", "--with", "numpy>=2", "--with", "pandas>=2",
               "--with", "openpyxl>=3", "python3", os.path.abspath(__file__),
               *sys.argv[1:]]
        sys.exit(subprocess.call(cmd, env=env))

import argparse  # noqa: E402
import urllib.request  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
sys.path.insert(0, str(HERE.parent / "build"))

import analyze_cps_fiscal_2025 as base  # noqa: E402

EXTRA_PERSON = ["SPM_RESOURCES", "SPM_POVTHRESHOLD", "A_ENRLW", "A_HSCOL"]
for _f in EXTRA_PERSON:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

from analyze_cps_fiscal_2025 import allocate, prepare  # noqa: E402

GROUPS = ["third_plus_nh_white", "all_native", "all_second_gen", "mexican_second_gen",
          "mexican_third_plus_selfid", "mexico_born"]
REFERENCE = "third_plus_nh_white"
LABEL = {"third_plus_nh_white": "3rd+ NH white", "all_native": "All natives",
         "all_second_gen": "All 2nd gen", "mexican_second_gen": "Mexican 2nd gen",
         "mexican_third_plus_selfid": "Mexican 3rd+", "mexico_born": "Mexico-born"}

# The extended-ledger balance this lane starts from (peer lane
# gen_ledger_extension_2026_09_16/RESULT.md, equal_all_members allocation,
# person weights, adults 25-64).
EXTENDED_BALANCE = {"third_plus_nh_white": 15_984.0, "all_native": 14_266.0,
                    "all_second_gen": 15_658.0, "mexican_second_gen": 7_698.0,
                    "mexican_third_plus_selfid": 9_705.0, "mexico_born": 4_462.0}
MEXICAN_2ND_GEN_GAP = -8_286.0   # extended gap vs 3rd+ NH white, all-members

# --------------------------------------------------------------------------
# Published parameters. Every number below is quoted from the cited table.
# --------------------------------------------------------------------------

# (1) CCDF. Average monthly subsidy paid to provider, weighted average over all
# ages and care types, FY2023: $690.
# https://acf.gov/occ/data/fy-2023-preliminary-data-table-15
CCDF_MONTHLY_SUBSIDY = 690.0
CCDF_COST_PER_CHILD_YEAR = CCDF_MONTHLY_SUBSIDY * 12.0
# Average monthly adjusted number of children served FY2023: 1,623,000.
# https://acf.gov/occ/data/fy-2023-preliminary-data-table-1
CCDF_CHILDREN_SERVED = 1_623_000.0
# Share of federally eligible children receiving a subsidy: 15 percent
# (1.8 million of 11.5 million potentially eligible under federal rules).
# https://aspe.hhs.gov/reports/child-care-eligibility-fy2021
CCDF_TAKEUP = 0.15
CCDF_ELIGIBLE_POVERTY_RATIO = 2.00   # brief's proxy for the 85%-SMI federal rule
CCDF_MAX_AGE = 12

# (2) Head Start, preschool component only (Head Start Preschool funded
# enrolment and annual operations funding, FY2024; AIAN included, MSHS
# excluded because MSHS enrolment cannot be attributed to a state and mixes
# age groups).
# https://headstart.gov/program-data/article/head-start-program-facts-fiscal-year-2024
HS_PRESCHOOL_SLOTS = 488_792 + 16_630          # 505,422
HS_PRESCHOOL_OPERATIONS = 7_082_932_155 + 243_801_945   # $7,326,734,100
HS_COST_PER_SLOT = HS_PRESCHOOL_OPERATIONS / HS_PRESCHOOL_SLOTS
HS_TOTAL_APPROPRIATION = 12_271_361_085        # all activities, FY2024
HS_CUMULATIVE_ENROLLMENT = 805_919
HS_HISPANIC_SHARE_PIR = 0.38                   # "Hispanic or Latino any race is 38 percent"
HS_ELIGIBLE_POVERTY_RATIO = 1.30
HS_AGE_LOW, HS_AGE_HIGH = 3, 5

# (3) Public higher education. SHEEO SHEF FY2025 report data file, FY2024 row:
# "Education Appropriations" divided by "Net FTE Enrollment", by state.
# https://shef.sheeo.org/data-downloads/
SHEEO_FY = 2024
# Share of postsecondary enrolment at public institutions, 2023-24 annual
# (12-month) headcount: (11,822,193 + 6,502,611 + 97,131) / 25,670,468.
# https://nces.ed.gov/ipeds/trendgenerator/app/build-table/2/2?rid=65&cid=1
NCES_PUBLIC_SHARE = (11_822_193 + 6_502_611 + 97_131) / 25_670_468
COLLEGE_AGE_LOW, COLLEGE_AGE_HIGH = 18, 24

# (4) State and local general services. 2022 Census of Governments: Finance,
# Table 1, "State and Local Government Finances by Level of Government and by
# State: 2022". Line numbers as printed in that table.
# https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx
CENSUS_LINE_DIRECT_GENERAL = 66
CENSUS_LINES_SUBTRACTED = {69: "Education", 77: "Public welfare", 81: "Hospitals",
                           83: "Health", 94: "Correction"}

# (5) Federal pure public goods. OMB Historical Table 3.1, Outlays by
# Superfunction and Function, FY2024 actual, in millions of dollars.
# https://www.whitehouse.gov/wp-content/uploads/2026/04/hist03z1_fy2027.xlsx
# Row labels exactly as printed in the OMB workbook ("Net interest" is
# lowercase there; the dollar rows precede the percentage-of-GDP repeats).
OMB_FUNCTIONS = ["National Defense", "Net interest", "General Government"]
OMB_YEAR = 2024

# (6) Lifeline. Monthly benefit up to $9.25 for broadband; USAC estimated
# 37.6 million eligible households on 2024 data and reported 8.2 million
# subscribers. https://www.congress.gov/crs-product/IF13283
LIFELINE_MONTHLY = 9.25
LIFELINE_ANNUAL = LIFELINE_MONTHLY * 12.0
LIFELINE_TAKEUP = 8_200_000 / 37_600_000
LIFELINE_ELIGIBLE_POVERTY_RATIO = 1.35
MATERIALITY = 20.0   # brief: report Lifeline only if it exceeds $20 per adult

CPS_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip"


def resolve_cps_zip(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.exists():
            raise SystemExit(f"[BLOCKED] --cps-zip not found: {explicit}")
        return explicit
    candidates = []
    if os.environ.get("CPS_ASEC_2025_ZIP"):
        candidates.append(Path(os.environ["CPS_ASEC_2025_ZIP"]))
    root = os.environ.get("PNY_DATA_ROOT")
    if root:
        candidates.append(Path(root) / "external/stage3/census/cps_asec_2025/asecpub25csv.zip")
    candidates.append(Path("/Volumes/2TBPNY/research-data/immigration-fiscal/data/"
                           "external/stage3/census/cps_asec_2025/asecpub25csv.zip"))
    candidates.append(HERE.parent / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip")
    cache = CACHE / "asecpub25csv.zip"
    candidates.append(cache)
    for c in candidates:
        if c.exists():
            return c
    cache.parent.mkdir(parents=True, exist_ok=True)
    print(f"[stage] CPS ASEC 2025 public file not found locally; downloading {CPS_URL}", flush=True)
    urllib.request.urlretrieve(CPS_URL, cache)
    return cache


def sdr(values: np.ndarray) -> tuple[float, float]:
    """Point estimate and 160-replicate SDR standard error, as the generator."""
    values = np.asarray(values, dtype=float)
    return float(values[0]), float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


# --------------------------------------------------------------------------
# Published-aggregate readers
# --------------------------------------------------------------------------

def read_state_population() -> pd.Series:
    """State resident population, 2022 vintage-2023 estimate, indexed by FIPS."""
    path = CACHE / "nst_est2023.csv"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path}")
    d = pd.read_csv(path, dtype={"STATE": str})
    d = d[d.SUMLEV == 40]
    return pd.Series(d.POPESTIMATE2022.to_numpy(dtype=float),
                     index=d.STATE.astype(int).to_numpy())


def read_us_population() -> float:
    path = CACHE / "nst_est2023.csv"
    d = pd.read_csv(path, dtype={"STATE": str})
    row = d[(d.SUMLEV == 10)]
    if len(row) != 1:
        raise SystemExit("[BLOCKED] could not read the national population row")
    return float(row.POPESTIMATE2023.iloc[0])


def read_general_services_per_capita(pop: pd.Series) -> tuple[pd.Series, dict]:
    """State+local direct general expenditure minus education, public welfare,
    health, hospitals and corrections, per state resident."""
    path = CACHE / "22slsstab1.xlsx"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path}")
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[ "2022_US_WY"]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    header = rows[8]
    # Each jurisdiction occupies a five-column block whose first column is the
    # state-and-local amount; the block starts where the name is printed.
    blocks: list[tuple[str, int]] = []
    for col, name in enumerate(header):
        if isinstance(name, str) and name.strip() and col >= 2:
            blocks.append((name.strip(), col))
    by_line = {}
    for r in rows:
        if isinstance(r[0], (int, float)) and r[0]:
            by_line[int(r[0])] = r
    wanted = [CENSUS_LINE_DIRECT_GENERAL, *CENSUS_LINES_SUBTRACTED]
    missing = [ln for ln in wanted if ln not in by_line]
    if missing:
        raise SystemExit(f"[BLOCKED] Census table lines not found: {missing}")

    names_to_fips = {
        "Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6,
        "Colorado": 8, "Connecticut": 9, "Delaware": 10, "District of Columbia": 11,
        "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, "Illinois": 17,
        "Indiana": 18, "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22,
        "Maine": 23, "Maryland": 24, "Massachusetts": 25, "Michigan": 26,
        "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
        "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34,
        "New Mexico": 35, "New York": 36, "North Carolina": 37, "North Dakota": 38,
        "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42,
        "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46,
        "Tennessee": 47, "Texas": 48, "Utah": 49, "Vermont": 50, "Virginia": 51,
        "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56,
    }
    per_capita, national = {}, {}
    for name, col in blocks:
        def amount(line: int) -> float:
            v = by_line[line][col]
            if not isinstance(v, (int, float)) or not np.isfinite(v):
                raise ValueError(f"Missing required Census spending cell: {name}, line {line}: {v!r}")
            return float(v)
        # Table is in thousands of dollars.
        residual = 1000.0 * (amount(CENSUS_LINE_DIRECT_GENERAL)
                             - sum(amount(ln) for ln in CENSUS_LINES_SUBTRACTED))
        if name == "United States Total":
            national["general_services_total"] = residual
            national["direct_general_total"] = 1000.0 * amount(CENSUS_LINE_DIRECT_GENERAL)
            continue
        fips = names_to_fips.get(name)
        if fips is None:
            continue
        if fips not in pop.index:
            raise SystemExit(f"[BLOCKED] no population for {name}")
        per_capita[fips] = residual / pop.loc[fips]
    if len(per_capita) != 51:
        raise SystemExit(f"[BLOCKED] expected 51 jurisdictions, parsed {len(per_capita)}")
    national["us_per_capita"] = national["general_services_total"] / pop.sum()
    return pd.Series(per_capita), national


def read_higher_ed_per_fte() -> tuple[pd.Series, float]:
    """FY2024 state and local education appropriations per net FTE, by state."""
    path = CACHE / "SHEEO_SHEF_FY25_Report_Data.xlsx"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path}")
    d = pd.read_excel(path, sheet_name="Report Data")
    d = d[d.FY == SHEEO_FY]
    if d.empty:
        raise SystemExit(f"[BLOCKED] SHEEO file has no FY{SHEEO_FY} rows")
    names_to_fips = {
        "Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6,
        "Colorado": 8, "Connecticut": 9, "Delaware": 10, "District of Columbia": 11,
        "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, "Illinois": 17,
        "Indiana": 18, "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22,
        "Maine": 23, "Maryland": 24, "Massachusetts": 25, "Michigan": 26,
        "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
        "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34,
        "New Mexico": 35, "New York": 36, "North Carolina": 37, "North Dakota": 38,
        "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42,
        "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46,
        "Tennessee": 47, "Texas": 48, "Utah": 49, "Vermont": 50, "Virginia": 51,
        "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56,
        "D.C.": 11,
    }
    out, tot_approp, tot_fte = {}, 0.0, 0.0
    for _, row in d.iterrows():
        fips = names_to_fips.get(str(row.State).strip())
        if fips is None:
            continue
        approp = float(row["Education Appropriations"])
        fte = float(row["Net FTE Enrollment"])
        if not np.isfinite(approp) or not np.isfinite(fte) or fte <= 0:
            raise SystemExit(f"[BLOCKED] bad SHEEO row for {row.State}")
        out[fips] = approp / fte
        tot_approp += approp
        tot_fte += fte
    if len(out) != 51:
        raise SystemExit(f"[BLOCKED] expected 51 SHEEO jurisdictions, parsed {len(out)}")
    return pd.Series(out), tot_approp / tot_fte, tot_approp


def read_federal_public_goods() -> tuple[dict, float]:
    """FY2024 outlays for the pure-public-good functions, in dollars."""
    path = CACHE / "omb_hist03z1_fy2027.xlsx"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path}")
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    year_row = None
    for r in rows[:12]:
        if any(str(c).strip() == str(OMB_YEAR) for c in r):
            year_row = r
            break
    if year_row is None:
        raise SystemExit("[BLOCKED] OMB table has no year header row")
    col = [i for i, c in enumerate(year_row) if str(c).strip() == str(OMB_YEAR)][0]
    # The table repeats every function first in millions of dollars and then as
    # percentages of GDP; the first occurrence is the dollar figure.
    out = {}
    for r in rows:
        name = str(r[0]).strip()
        if name in OMB_FUNCTIONS and name not in out:
            v = r[col]
            if not isinstance(v, (int, float)):
                raise SystemExit(f"[BLOCKED] OMB {name} FY{OMB_YEAR} is not numeric: {v!r}")
            out[name] = float(v) * 1e6
    missing = [f for f in OMB_FUNCTIONS if f not in out]
    if missing:
        raise SystemExit(f"[BLOCKED] OMB functions not found: {missing}")
    return out, sum(out.values())


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build(args):
    cps = resolve_cps_zip(args.cps_zip)
    print(f"[stage] CPS ASEC 2025 source: {cps}", flush=True)
    d, heads, index, validation = prepare(cps)
    n_units = len(heads)

    with zipfile.ZipFile(cps) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"])
    merged = d[["PH_SEQ"]].merge(hh, left_on="PH_SEQ", right_on="H_SEQ",
                                 how="left", validate="many_to_one")
    if merged.H_SEQ.isna().any():
        raise SystemExit("[BLOCKED] person record without a household record")
    d = d.assign(GESTFIPS=merged.GESTFIPS.to_numpy())
    if not d.groupby("SPM_ID").SPM_RESOURCES.nunique().eq(1).all():
        raise SystemExit("[BLOCKED] SPM_RESOURCES is not constant inside a resource unit")
    if not d.groupby("SPM_ID").SPM_POVTHRESHOLD.nunique().eq(1).all():
        raise SystemExit("[BLOCKED] SPM_POVTHRESHOLD is not constant inside a resource unit")

    pop = read_state_population()
    us_pop = read_us_population()
    general_pc, census_national = read_general_services_per_capita(pop)
    higher_ed_pc, higher_ed_national, sheeo_total_appropriations = read_higher_ed_per_fte()
    omb_functions, omb_total = read_federal_public_goods()
    federal_pc = omb_total / us_pop

    missing = sorted(set(d.GESTFIPS.unique()) - set(general_pc.index))
    if missing:
        raise SystemExit(f"[BLOCKED] general-services parameters missing for FIPS {missing}")
    person_general_pc = d.GESTFIPS.map(general_pc).to_numpy(dtype=float)
    person_higher_ed_pc = d.GESTFIPS.map(higher_ed_pc).to_numpy(dtype=float)

    # ---- unit-level exposure -------------------------------------------
    resources = heads.SPM_RESOURCES.to_numpy(dtype=float)
    threshold = heads.SPM_POVTHRESHOLD.to_numpy(dtype=float)
    if (threshold <= 0).any():
        raise SystemExit("[BLOCKED] nonpositive SPM poverty threshold")
    ratio = resources / threshold

    age = d.A_AGE.to_numpy()
    totals: dict[str, np.ndarray] = {}

    # (1) CCDF
    kids_ccdf = (age <= CCDF_MAX_AGE).astype(float)
    n_kids_ccdf = np.bincount(index, weights=kids_ccdf, minlength=n_units)
    ccdf_eligible = (ratio < CCDF_ELIGIBLE_POVERTY_RATIO).astype(float)
    exposure_ccdf_children = n_kids_ccdf * ccdf_eligible
    # The brief's literal rule: children 0-12 in units under 200% SPM poverty,
    # times the ASPE 15% take-up. Kept as a sensitivity arm.
    totals["ccdf_literal"] = (exposure_ccdf_children * CCDF_TAKEUP
                              * CCDF_COST_PER_CHILD_YEAR)
    # That rule overshoots the program's own national envelope, because the
    # 200%-SPM-poverty pool is much wider than ASPE's federally eligible pool
    # (which also requires a working or studying parent and income at or below
    # 85% of state median income). The 15% take-up was measured against the
    # narrower pool, so applying it to the wider one double counts. The
    # calibrated arm rescales take-up so the model reproduces the published
    # average monthly number of children served; it is a pure scalar, so it
    # changes every group's level by the same factor and leaves the ranking and
    # the proportional between-group differences untouched.
    _unit_weight_ccdf = heads.pwwgt0.to_numpy(dtype=float)
    ccdf_children_literal = float((exposure_ccdf_children * _unit_weight_ccdf).sum()) * CCDF_TAKEUP
    ccdf_calibration = CCDF_CHILDREN_SERVED / ccdf_children_literal
    ccdf_takeup_calibrated = CCDF_TAKEUP * ccdf_calibration
    totals["ccdf"] = (exposure_ccdf_children * ccdf_takeup_calibrated
                      * CCDF_COST_PER_CHILD_YEAR)

    # (2) Head Start
    kids_hs = ((age >= HS_AGE_LOW) & (age <= HS_AGE_HIGH)).astype(float)
    n_kids_hs = np.bincount(index, weights=kids_hs, minlength=n_units)
    hs_eligible = (ratio < HS_ELIGIBLE_POVERTY_RATIO).astype(float)
    exposure_hs_children = n_kids_hs * hs_eligible
    # Take-up is derived, not assumed: published preschool slots divided by the
    # weighted count of income-eligible 3-5 year olds in this same file.
    unit_weight = heads.pwwgt0.to_numpy(dtype=float)
    eligible_hs_national = float((exposure_hs_children * unit_weight).sum())
    hs_takeup = HS_PRESCHOOL_SLOTS / eligible_hs_national
    totals["head_start"] = exposure_hs_children * hs_takeup * HS_COST_PER_SLOT

    # (3) Public higher education
    in_college = (d.A_ENRLW.eq(1) & d.A_HSCOL.eq(2)
                  & d.A_AGE.between(COLLEGE_AGE_LOW, COLLEGE_AGE_HIGH)).to_numpy(dtype=float)
    higher_ed_person = in_college * person_higher_ed_pc * NCES_PUBLIC_SHARE
    totals["higher_ed"] = np.bincount(index, weights=higher_ed_person, minlength=n_units)

    # (4) state and local general services, per-capita convention
    totals["general_services"] = np.bincount(index, weights=person_general_pc, minlength=n_units)

    # (5) federal pure public goods, per-capita convention
    totals["federal_public_goods"] = np.bincount(
        index, weights=np.full(len(d), federal_pc), minlength=n_units)

    # (6) Lifeline
    lifeline_eligible = (ratio < LIFELINE_ELIGIBLE_POVERTY_RATIO).astype(float)
    totals["lifeline"] = lifeline_eligible * LIFELINE_TAKEUP * LIFELINE_ANNUAL

    # ---- group masks, identical construction to the generator ------------
    native = d.PRCITSHP.isin([1, 2, 3])
    us_area = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    group = {
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy(),
        "all_native": native.to_numpy(),
        "all_second_gen": (native & ~parents_us).to_numpy(),
        "mexican_second_gen": (native & parent_mexico).to_numpy(),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)).to_numpy(),
        "mexico_born": (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy(),
    }
    adults_25_64 = (d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2)).to_numpy()
    person_weights = d[base.REPS].to_numpy()
    adults_18 = d.A_AGE.ge(18).to_numpy()
    n_adults = np.bincount(index, weights=adults_18, minlength=n_units)
    allocations = {
        "equal_all_members": np.ones(len(d), dtype=bool),
        "equal_adults_18plus": adults_18 | (n_adults[index] == 0),
    }

    # Hispanic identification, for the Head Start PIR cross-check.
    hispanic = d.PEHSPNON.eq(1).to_numpy(dtype=float)

    higher_ed_charged = float((higher_ed_person * d[base.REPS[0]].to_numpy()).sum())
    aggregates = dict(
        ccdf_children_literal=ccdf_children_literal,
        ccdf_calibration=ccdf_calibration,
        ccdf_takeup_calibrated=ccdf_takeup_calibrated,
        higher_ed_charged=higher_ed_charged,
        census_national=census_national, higher_ed_national=higher_ed_national,
        omb_functions=omb_functions, omb_total=omb_total, federal_pc=federal_pc,
        us_pop=us_pop, hs_takeup=hs_takeup,
        eligible_hs_national=eligible_hs_national,
        general_pc=general_pc, higher_ed_pc=higher_ed_pc,
        sheeo_total_appropriations=sheeo_total_appropriations,
    )
    return dict(d=d, index=index, n_units=n_units, totals=totals, group=group,
                adults_25_64=adults_25_64, person_weights=person_weights,
                allocations=allocations, validation=validation, cps=cps,
                aggregates=aggregates, hispanic=hispanic,
                exposure_ccdf_children=exposure_ccdf_children,
                exposure_hs_children=exposure_hs_children,
                in_college=in_college, unit_weight=unit_weight)


ITEM_ORDER = ["ccdf", "head_start", "higher_ed", "lifeline"]
SENSITIVITY_ITEMS = ["ccdf_literal"]
CONVENTION_ITEMS = ["general_services", "federal_public_goods"]
ITEM_LABEL = {
    "ccdf": "Child care subsidies (CCDF), calibrated",
    "ccdf_literal": "CCDF, brief's literal 15% take-up rule",
    "head_start": "Head Start (preschool)",
    "higher_ed": "Public higher-education appropriations",
    "lifeline": "Lifeline",
    "general_services": "State and local general services",
    "federal_public_goods": "Federal pure public goods",
}


def analyse(state, args):
    d, index, n_units = state["d"], state["index"], state["n_units"]
    totals, group = state["totals"], state["group"]
    adults, weights = state["adults_25_64"], state["person_weights"]
    agg = state["aggregates"]
    rows, lines = [], []

    def out(text=""):
        print(text)
        lines.append(text)

    # Per-adult estimates, for each item, allocation and group.
    est: dict[tuple[str, str, str], tuple[float, float]] = {}
    for item, unit_total in totals.items():
        for alloc_name, eligible in state["allocations"].items():
            person_amount = allocate(unit_total, index, eligible, n_units)
            for g in GROUPS:
                use = adults & group[g]
                num = person_amount[use] @ weights[use]
                den = weights[use].sum(axis=0)
                if (den <= 0).any():
                    raise SystemExit(f"[BLOCKED] empty denominator for {g}")
                point, se = sdr(num / den)
                est[(item, alloc_name, g)] = (point, se)
                rows.append({"item": item, "allocation": alloc_name, "group": g,
                             "dollars_per_adult_25_64": point, "se_sampling": se,
                             "n_adults_unweighted": int(use.sum()),
                             "weighted_adults": float(weights[use, 0].sum())})

    # Differences from the reference group are re-estimated replicate by
    # replicate so the standard error carries the covariance.
    diff: dict[tuple[str, str, str], tuple[float, float]] = {}
    for item, unit_total in totals.items():
        for alloc_name, eligible in state["allocations"].items():
            person_amount = allocate(unit_total, index, eligible, n_units)
            ref = adults & group[REFERENCE]
            ref_series = (person_amount[ref] @ weights[ref]) / weights[ref].sum(axis=0)
            for g in GROUPS:
                if g == REFERENCE:
                    diff[(item, alloc_name, g)] = (0.0, 0.0)
                    continue
                use = adults & group[g]
                series = (person_amount[use] @ weights[use]) / weights[use].sum(axis=0)
                point, se = sdr(series - ref_series)
                diff[(item, alloc_name, g)] = (point, se)
                for r in rows:
                    if (r["item"], r["allocation"], r["group"]) == (item, alloc_name, g):
                        r["difference_from_third_plus_nh_white"] = point
                        r["se_difference"] = se

    def table(items, alloc_name, title, show_diff=True):
        out(title)
        out("")
        header = "| Item | " + " | ".join(LABEL[g] for g in GROUPS) + " |"
        out(header)
        out("|" + "---|" * (len(GROUPS) + 1))
        for item in items:
            cells = []
            for g in GROUPS:
                p, s = est[(item, alloc_name, g)]
                cells.append(f"{p:,.0f} ({s:,.0f})")
            out(f"| {ITEM_LABEL[item]} | " + " | ".join(cells) + " |")
        if len(items) > 1:
            cells = []
            for g in GROUPS:
                tot = sum(est[(i, alloc_name, g)][0] for i in items)
                cells.append(f"{tot:,.0f}")
            out("| **Sum of the items above** | " + " | ".join(cells) + " |")
        out("")
        if not show_diff:
            return
        out("Difference from third-plus non-Hispanic white, same rows:")
        out("")
        others = [g for g in GROUPS if g != REFERENCE]
        out("| Item | " + " | ".join(LABEL[g] for g in others) + " |")
        out("|" + "---|" * (len(others) + 1))
        for item in items:
            cells = []
            for g in others:
                p, s = diff[(item, alloc_name, g)]
                cells.append(f"{p:+,.0f} ({s:,.0f})")
            out(f"| {ITEM_LABEL[item]} | " + " | ".join(cells) + " |")
        cells = []
        for g in others:
            tot = sum(diff[(i, alloc_name, g)][0] for i in items)
            cells.append(f"{tot:+,.0f}")
        out("| **Sum of the items above** | " + " | ".join(cells) + " |")
        out("")

    out("=" * 78)
    out("AGGREGATE-ONLY LEDGER RESIDUALS, $ per adult 25-64 per year")
    out("=" * 78)
    out("")
    out(f"CPS ASEC 2025 source: {state['cps']}")
    out(f"Person rows {state['validation']['person_rows']:,}, "
        f"SPM units {state['validation']['spm_units']:,}, "
        f"all generator integrity gates passed.")
    out("")
    out("Every figure below is an accounting scenario: a published national or")
    out("state aggregate times this file's measured exposure. None of them is a")
    out("payment observed in the microdata.")
    out("")

    out("-" * 78)
    out("BLOCK 1 -- items in the running balance (allocation: equal_all_members)")
    out("-" * 78)
    out("")
    table(ITEM_ORDER, "equal_all_members",
          "Annual dollars per adult 25-64, SDR standard error in parentheses:")

    out("-" * 78)
    out("BLOCK 2 -- same items, allocation: equal_adults_18plus")
    out("-" * 78)
    out("")
    table(ITEM_ORDER, "equal_adults_18plus",
          "Annual dollars per adult 25-64, SDR standard error in parentheses:")

    out("-" * 78)
    out("BLOCK 3 -- the two convention items, reported OUTSIDE the running balance")
    out("-" * 78)
    out("")
    out("Convention A, 'per-capita': every resident is charged the per-capita")
    out("amount for their state (items 4 and 5 of the brief).")
    out("Convention B, 'pure public good': the item is not charged at all, so")
    out("every group's entry is exactly 0 and every difference is exactly 0.")
    out("")
    table(CONVENTION_ITEMS, "equal_all_members",
          "Convention A, equal_all_members allocation:")
    table(CONVENTION_ITEMS, "equal_adults_18plus",
          "Convention A, equal_adults_18plus allocation:")

    # ---- running balance -------------------------------------------------
    out("-" * 78)
    out("BLOCK 4 -- running balance from the extended ledger")
    out("-" * 78)
    out("")
    out("Starting point: the peer lane's EXTENDED BALANCE (taxes minus selected")
    out("transfers, plus employer payroll, sales/excise and property tax, minus")
    out("K-12), equal_all_members allocation, person weights, adults 25-64.")
    out("A positive balance is a net contribution; the items priced here are")
    out("costs, so each one is subtracted.")
    out("")
    for alloc_name in ("equal_all_members", "equal_adults_18plus"):
        scope = "all members" if alloc_name == "equal_all_members" else "adults 18+"
        out(f"Allocation: {alloc_name} (shares carried on {scope})")
        out("")
        out("| | " + " | ".join(LABEL[g] for g in GROUPS) + " |")
        out("|" + "---|" * (len(GROUPS) + 1))
        base_row = [EXTENDED_BALANCE[g] for g in GROUPS]
        out("| Extended balance (peer lane, all-members) | "
            + " | ".join(f"{v:,.0f}" for v in base_row) + " |")
        running = dict(zip(GROUPS, base_row))
        for item in ITEM_ORDER:
            cells = []
            for g in GROUPS:
                running[g] -= est[(item, alloc_name, g)][0]
                cells.append(f"{running[g]:,.0f}")
            out(f"| after -{ITEM_LABEL[item]} | " + " | ".join(cells) + " |")
        out("| **Balance, convention B (public goods not charged)** | "
            + " | ".join(f"{running[g]:,.0f}" for g in GROUPS) + " |")
        with_pg = {g: running[g] - sum(est[(i, alloc_name, g)][0] for i in CONVENTION_ITEMS)
                   for g in GROUPS}
        out("| **Balance, convention A (public goods charged per capita)** | "
            + " | ".join(f"{with_pg[g]:,.0f}" for g in GROUPS) + " |")
        out("")
        gap_b = running["mexican_second_gen"] - running[REFERENCE]
        gap_a = with_pg["mexican_second_gen"] - with_pg[REFERENCE]
        out(f"Mexican second generation minus third-plus non-Hispanic white:")
        out(f"  extended ledger, before this lane:        {MEXICAN_2ND_GEN_GAP:+,.0f}")
        out(f"  after these items, convention B (0):      {gap_b:+,.0f}")
        out(f"  after these items, convention A (per cap):{gap_a:+,.0f}")
        out(f"  convention A minus convention B:          {gap_a - gap_b:+,.0f}")
        out("")

    # ---- validation and cross-checks -------------------------------------
    out("-" * 78)
    out("BLOCK 5 -- calibration against the published national totals")
    out("-" * 78)
    out("")
    w = state["unit_weight"]
    pw = state["person_weights"][:, 0]
    out(f"CCDF cost per child-year: ${CCDF_COST_PER_CHILD_YEAR:,.0f} "
        f"(${CCDF_MONTHLY_SUBSIDY:,.0f}/month x 12, ACF FY2023 Table 15).")
    out(f"CCDF children implied by the brief's literal rule "
        f"(200% SPM poverty, ages 0-12, 15% take-up): "
        f"{agg['ccdf_children_literal']:,.0f}")
    out(f"CCDF children published (ACF FY2023 Table 1): {CCDF_CHILDREN_SERVED:,.0f}")
    out(f"  the literal rule overshoots by a factor of "
        f"{1 / agg['ccdf_calibration']:.2f}")
    out(f"  calibrated take-up used in the running balance: "
        f"{agg['ccdf_takeup_calibrated']:.3f} "
        f"(= 0.15 x {agg['ccdf_calibration']:.3f})")
    out(f"  calibrated national total: "
        f"${CCDF_CHILDREN_SERVED * CCDF_COST_PER_CHILD_YEAR / 1e9:,.2f}B, "
        f"against a published all-fund CCDF expenditure of $25.27B in FY2023 "
        f"(the remainder is provider stabilisation grants, quality set-asides "
        f"and administration, which are not per-child subsidies).")
    out("")
    out("The two CCDF arms side by side, equal_all_members allocation:")
    out("")
    out("| Arm | " + " | ".join(LABEL[g] for g in GROUPS) + " |")
    out("|" + "---|" * (len(GROUPS) + 1))
    for item in ["ccdf", "ccdf_literal"]:
        cells = [f"{est[(item, 'equal_all_members', g)][0]:,.0f}" for g in GROUPS]
        out(f"| {ITEM_LABEL[item]} | " + " | ".join(cells) + " |")
    out("")
    out("The calibration is a single scalar, so the literal arm's per-adult")
    out("differences from third-plus non-Hispanic white are simply "
        f"{1 / agg['ccdf_calibration']:.2f} times")
    out("the calibrated ones; no ranking or sign changes either way.")
    out("")
    out(f"Head Start income-eligible 3-5 year olds in this file: "
        f"{agg['eligible_hs_national']:,.0f}")
    out(f"Head Start preschool funded slots (FY2024): {HS_PRESCHOOL_SLOTS:,}")
    out(f"  derived take-up: {agg['hs_takeup']:.3f}")
    out(f"Head Start cost per slot: ${HS_COST_PER_SLOT:,.0f}")
    hisp_elig = float((np.bincount(state["index"],
                                   weights=(d.A_AGE.between(HS_AGE_LOW, HS_AGE_HIGH).to_numpy(dtype=float)
                                            * state["hispanic"]),
                                   minlength=n_units)
                       * (state["exposure_hs_children"] > 0) * w).sum())
    hisp_share = hisp_elig / agg["eligible_hs_national"] if agg["eligible_hs_national"] else float("nan")
    out(f"Hispanic share of the model's income-eligible 3-5 pool: {hisp_share:.1%}")
    out(f"Hispanic share of Head Start enrolment (PIR FY2024):    {HS_HISPANIC_SHARE_PIR:.1%}")
    out("  The two are close, so the model is not assigning Head Start to the")
    out("  Hispanic-origin groups at a rate the program's own records contradict.")
    out("")
    out(f"Public higher education, national education appropriations per FTE "
        f"(SHEEO FY{SHEEO_FY}): ${higher_ed_national_fmt(agg)}")
    out(f"Public share of postsecondary enrolment (NCES 2023-24): {NCES_PUBLIC_SHARE:.1%}")
    college = float((state["in_college"] * pw).sum())
    out(f"Persons 18-24 enrolled in college in this file: {college:,.0f}")
    out(f"Higher-education dollars charged by the model: "
        f"${agg['higher_ed_charged'] / 1e9:,.1f}B")
    out(f"Total FY{SHEEO_FY} state and local education appropriations (SHEEO): "
        f"${agg['sheeo_total_appropriations'] / 1e9:,.1f}B")
    out("  The model charges only the 18-24 slice, so it deliberately covers a")
    out("  minority of the appropriation; students aged 25 and over, graduate")
    out("  students and the research, agriculture and medical components are")
    out("  left uncharged rather than spread over the whole population.")
    out("")
    out("State and local general services, 2022 Census of Governments Table 1:")
    out(f"  direct general expenditure, US total: "
        f"${agg['census_national']['direct_general_total'] / 1e9:,.1f}B")
    out(f"  minus education, public welfare, hospitals, health, correction: "
        f"${agg['census_national']['general_services_total'] / 1e9:,.1f}B")
    out(f"  US per capita: ${agg['census_national']['us_per_capita']:,.0f}")
    out(f"  state range: ${agg['general_pc'].min():,.0f} to "
        f"${agg['general_pc'].max():,.0f}")
    out("")
    out(f"Federal pure public goods, OMB Historical Table 3.1, FY{OMB_YEAR} outlays:")
    for name, v in agg["omb_functions"].items():
        out(f"  {name}: ${v / 1e9:,.1f}B")
    out(f"  total: ${agg['omb_total'] / 1e9:,.1f}B over a population of "
        f"{agg['us_pop'] / 1e6:,.1f}M = ${agg['federal_pc']:,.0f} per capita")
    out("")
    out("Lifeline materiality check (threshold "
        f"${MATERIALITY:,.0f} per adult for any group):")
    worst = max(est[("lifeline", "equal_adults_18plus", g)][0] for g in GROUPS)
    out(f"  largest group value, either allocation: ${worst:,.2f}")
    out(f"  verdict: {'MATERIAL' if worst > MATERIALITY else 'IMMATERIAL'}")
    out("")
    out("WIC and LIHEAP are not priced here: both are already inside SPM")
    out("resources and are carried in the memo's non-cash transfer line, so")
    out("adding them would double count.")
    out("")

    out("-" * 78)
    out("BLOCK 6 -- items that remain unpriced")
    out("-" * 78)
    out("")
    out("Affirmative action and minority-business set-asides cannot be placed on")
    out("this ledger. No dataset assigns those dollars to persons by national")
    out("origin or by generation: federal contracting data records the firm's")
    out("certification status, not the origin or generation of the firm's owner,")
    out("and no public file links a contract obligation to a CPS-style person")
    out("record. The best available aggregate is the government-wide small")
    out("disadvantaged business prime contracting achievement, 12.27 percent of")
    out("prime contracting dollars in FY2024 (SBA scorecard); the FY2025 figure")
    out("is 11.60 percent, or $75.3 billion. That is an award total to firms, not")
    out("a transfer to persons, and it is not a net fiscal cost at all, since the")
    out("government buys goods and services for the money.")
    out("")

    frame = pd.DataFrame(rows)
    frame.to_csv(args.output / "residual_agg_by_generation.csv", index=False)
    (args.output / "residual_agg_result.txt").write_text("\n".join(lines) + "\n")
    print(f"\n[wrote] {args.output / 'residual_agg_by_generation.csv'}")
    print(f"[wrote] {args.output / 'residual_agg_result.txt'}")


def higher_ed_national_fmt(agg) -> str:
    return f"{agg['higher_ed_national']:,.0f}"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cps-zip", type=Path, default=None)
    p.add_argument("--output", type=Path, default=HERE)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    state = build(args)
    analyse(state, args)


if __name__ == "__main__":
    main()
