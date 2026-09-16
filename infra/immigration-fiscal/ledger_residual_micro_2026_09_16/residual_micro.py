#!/usr/bin/env python3
"""Person-level fiscal-ledger residuals by origin-generation.

Extends the *extended* annual ledger (gen_ledger_extension_2026_09_16) with the
government items that can still be measured in the SAME CPS ASEC 2025 microdata
or, for the institutional population that CPS does not cover, in ACS PUMS via
the Census API.

Items
  1a  Government-sourced educational assistance        (CPS ED_VAL / OED_TYP1-3)
  1b  Public higher-education operating subsidy        (CPS A_ENRLW/A_HSCOL/A_FTPT x SHEEO SHEF FY2024)
  2   ACA advance premium tax credits                  (CPS MRKS x CMS full-plan-year-2024 average APTC)
  3   Uncompensated hospital care of the uninsured     (CPS COV/NOCOV_CYR x AHA / Census uninsured)
  4   Institutional care: prisons + nursing facilities (ACS 1-year PUMS 2023 TYPEHUGQ x Vera/Census/BJS, CMS/KFF)
  5   Other unambiguously public transfers             (CPS WC_TYPE=1, DIS_SC 6/8/9; SPM_CAPHOUSESUB reported apart)

Everything reuses prepare()/allocate()/estimate() from
infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py through the peer lane's
extend_ledger.build(), so the group masks, SPM resource units, allocation rules
and 160-replicate SDR variance are identical by construction, and the peer
lane's -8,286 extended balance is reproduced as a gate before anything is added.
"""
from __future__ import annotations

import os
import subprocess
import sys

if os.environ.get("_RESIDUAL_MICRO_BOOTSTRAPPED") != "1":
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        env = dict(os.environ, _RESIDUAL_MICRO_BOOTSTRAPPED="1")
        cmd = ["uv", "run", "--with", "numpy>=2", "--with", "pandas>=2",
               "python3", os.path.abspath(__file__), *sys.argv[1:]]
        sys.exit(subprocess.call(cmd, env=env))

import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import urllib.request  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
PEER = HERE.parent / "gen_ledger_extension_2026_09_16"
sys.path.insert(0, str(PEER))
sys.path.insert(0, str(HERE.parent / "build"))

import analyze_cps_fiscal_2025 as base  # noqa: E402

# Person fields this lane needs on top of what the base generator and the peer
# lane read. PERSON is consumed as usecols at prepare() call time, so appending
# before build() is enough; prepare() also NaN-checks every listed column.
EXTRA_PERSON = [
    "ED_VAL", "ED_YN", "OED_TYP1", "OED_TYP2", "OED_TYP3",
    "A_ENRLW", "A_HSCOL", "A_FTPT",
    "MRK", "MRKS", "MRKUN",
    "COV", "NOCOV_CYR",
    "WC_VAL", "WC_TYPE",
    "DIS_VAL1", "DIS_VAL2", "DIS_SC1", "DIS_SC2",
]
for _f in EXTRA_PERSON:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

import extend_ledger as peer  # noqa: E402  (appends WSAL_VAL / SPM_RESOURCES itself)
from analyze_cps_fiscal_2025 import allocate, estimate  # noqa: E402

GROUPS = peer.GROUPS
REFERENCE = peer.REFERENCE

# ---------------------------------------------------------------------------
# Published parameters. Every one carries its URL in SOURCES below.
# ---------------------------------------------------------------------------

# SHEEO, State Higher Education Finance FY2024, p. 12: "In 2024, education
# appropriations per FTE increased 0.8% beyond inflation to $11,683."
SHEF_EDU_APPROPRIATIONS_PER_FTE_2024 = 11_683.0

# NCES Digest of Education Statistics 2024, Table 303.70, fall 2023 undergraduate
# enrollment: public 12,227,529 of 15,825,762 total.
NCES_PUBLIC_UNDERGRAD_SHARE = 12_227_529 / 15_825_762     # 0.7726
NCES_PUBLIC_SHARE_BRIEF_FALLBACK = 0.74

# CMS, Effectuated Enrollment: Early 2025 Snapshot and Full Year 2024 Average,
# Table 4: full plan year 2024 average APTC per month for consumers receiving
# APTC $527.64 (19,531,827 APTC enrollees of 20,968,847 effectuated).
CMS_APTC_PER_MONTH_2024 = 527.64
CMS_APTC_PER_YEAR_2024 = CMS_APTC_PER_MONTH_2024 * 12.0    # 6,331.68
CMS_APTC_SHARE_SUBSIDISED_2024 = 19_531_827 / 20_968_847   # 0.9315, fallback path

# AHA, Uncompensated Hospital Care Cost Fact Sheet (2020 update, latest edition):
# $42.67 billion in 2020. Census P60-274: 28.0 million uninsured at any point in
# 2020. The ratio is the uncompensated hospital cost per uninsured person-year.
AHA_UNCOMPENSATED_2020 = 42.67e9
CENSUS_UNINSURED_2020 = 28.0e6
UNCOMPENSATED_PER_UNINSURED = AHA_UNCOMPENSATED_2020 / CENSUS_UNINSURED_2020   # 1,524
# Hospital input prices rose about 20% from 2020 to 2024 (AHA Cost of Caring
# 2025); the high arm carries that forward. [INFERENCE on the deflator]
UNCOMPENSATED_2024_UPLIFT = 1.20

# Institutional care prices.
# Prisons: USAFacts, from the Census Annual Survey of State and Local Government
# Finances and BJS, reports $63.6bn of state corrections spending in 2023 and a
# $60,989 median state cost per prisoner. BJS Prisoners in 2023 puts the total
# prison population at 1,254,200, of which 155,972 federal, so 1,098,228 state
# prisoners. $63.6bn / 1,098,228 = $57,911 per state prisoner-year.
PRISON_STATE_SPENDING_2023 = 63.6e9
BJS_STATE_PRISONERS_2023 = 1_254_200 - 155_972
PRISON_COST_PER_YEAR = PRISON_STATE_SPENDING_2023 / BJS_STATE_PRISONERS_2023   # 57,911
PRISON_COST_LOW = 45_000.0     # jail-weighted low arm
PRISON_COST_HIGH = 70_000.0    # high arm

# Nursing facilities: KFF, 5 Key Facts About Nursing Facilities and Medicaid —
# "Medicaid paid for 44% of the $147 billion that the US spent on institutional
# long-term care in 2023" (= $64.7bn) across "nearly 15,000 federally certified
# nursing facilities and the 1.2 million people living in them".
MEDICAID_INSTITUTIONAL_LTC_2023 = 0.44 * 147e9
NURSING_FACILITY_RESIDENTS = 1.2e6
NURSING_COST_PER_YEAR = MEDICAID_INSTITUTIONAL_LTC_2023 / NURSING_FACILITY_RESIDENTS  # 53,900

ACS_YEAR = "2023"
ACS_AGE_BANDS = {"18_39": "18:39", "40_64": "40:64", "65_plus": "65:99", "25_64": "25:64"}

# ACS proxy for each ledger group. ACS PUMS has no parental birthplace, so every
# US-born row pools the second and third-plus generations.
ACS_PROXY = {
    "third_plus_nh_white": ("native_nh_white", "US-born non-Hispanic white (2nd+3rd gen pooled)"),
    "all_native": ("native_all", "all US-born (2nd+3rd gen pooled)"),
    "all_second_gen": ("native_all", "all US-born — NO second-generation proxy exists in ACS"),
    "mexican_second_gen": ("native_mexican", "US-born Mexican-origin self-ID (2nd+3rd gen pooled)"),
    "mexican_third_plus_selfid": ("native_mexican", "US-born Mexican-origin self-ID (2nd+3rd gen pooled)"),
    "mexico_born": ("foreign_mexican", "foreign-born Mexican"),
}

SOURCES = [
    ("CPS ASEC 2025 public-use microdata (income year 2024)",
     "https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip"),
    ("CPS ASEC 2025 data dictionary (ED_VAL, OED_TYP1-3, A_ENRLW, A_HSCOL, A_FTPT, MRK/MRKS/MRKUN, "
     "COV, NOCOV_CYR, WC_TYPE, DIS_SC1/2)",
     "https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf"),
    ("SHEEO, State Higher Education Finance FY2024: education appropriations $11,683 per FTE",
     "https://shef.sheeo.org/wp-content/uploads/2025/05/SHEEO_SHEF_FY24_Report.pdf"),
    ("NCES Digest 2024 Table 303.70: fall 2023 undergraduate enrollment, public 12,227,529 of 15,825,762",
     "https://nces.ed.gov/programs/digest/d24/tables/dt24_303.70.asp"),
    ("CMS, Effectuated Enrollment: Early 2025 Snapshot and Full Year 2024 Average, Table 4: "
     "full-year 2024 average APTC $527.64/month, 19,531,827 APTC enrollees of 20,968,847",
     "https://www.cms.gov/files/document/effectuated-enrollment-early-snapshot-2025-and-full-year-2024-average.pdf"),
    ("AHA, Uncompensated Hospital Care Cost Fact Sheet: $42.67bn in 2020 (latest edition)",
     "https://www.aha.org/system/files/media/file/2020/01/2020-Uncompensated-Care-Fact-Sheet.pdf"),
    ("Census P60-274, Health Insurance Coverage in the United States: 2020 — 28.0 million uninsured (8.6%)",
     "https://www.census.gov/content/dam/Census/library/publications/2021/demo/p60-274.pdf"),
    ("USAFacts, How much do states spend on housing prisoners? — $63.6bn state corrections spending 2023, "
     "median $60,989 per prisoner (Census ASSLGF + BJS)",
     "https://usafacts.org/articles/how-much-do-states-spend-on-prisons/"),
    ("BJS, Prisoners in 2023 – Statistical Tables — 1,254,200 total, 155,972 federal at yearend 2023",
     "https://bjs.ojp.gov/document/p23st.pdf"),
    ("KFF, 5 Key Facts About Nursing Facilities and Medicaid — Medicaid paid 44% of $147bn institutional "
     "long-term care in 2023; 1.2 million nursing facility residents",
     "https://www.kff.org/medicaid/5-key-facts-about-nursing-facilities-and-medicaid/"),
    ("ACS 1-year PUMS 2023 institutional group quarters (TYPEHUGQ=2) via the Census Data API tabulate endpoint",
     "https://api.census.gov/data/2023/acs/acs1/pums"),
]


def sdr(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    return float(values[0]), float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


# ---------------------------------------------------------------------------
# ACS institutional pull
# ---------------------------------------------------------------------------

def census_key() -> str:
    k = os.environ.get("CENSUS_API_KEY")
    if k:
        return k
    cfg = (HERE.parent / "acquire/config.local.env").read_text()
    m = re.search(r'CENSUS_API_KEY="?([A-Za-z0-9]+)', cfg)
    if not m:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not found in env or acquire/config.local.env")
    return m.group(1)


def acs_fetch(rows: list[str], extra: str, out: Path, age: str) -> None:
    if out.exists():
        return
    url = (f"https://api.census.gov/data/{ACS_YEAR}/acs/acs1/pums?tabulate=weight(PWGTP)&col+TYPEHUGQ"
           + "".join(f"&row+{r}" for r in rows) + f"&AGEP={age}{extra}&key={census_key()}")
    print(f"[stage] ACS pull {out.name}", flush=True)
    out.write_bytes(urllib.request.urlopen(url, timeout=180).read())


def acs_load(path: Path) -> dict[tuple[str, ...], tuple[float, float]]:
    """-> {(row values...): (institutional count, total count)}"""
    d = json.loads(path.read_text())
    hdr = d[0]
    tc = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    return {tuple(str(x) for x in r[len(tc):]): (float(r[tc["2"]]), float(sum(r[i] for i in tc.values())))
            for r in d[1:]}


def acs_institutional() -> pd.DataFrame:
    """Institutional-GQ counts and populations by proxy group and age band, 2023."""
    rows = []
    for band, age in ACS_AGE_BANDS.items():
        hp = HERE / f"acs_h_{band}.json"
        rp = HERE / f"acs_r_{band}.json"
        acs_fetch(["NATIVITY", "HISP"], "", hp, age)
        acs_fetch(["NATIVITY", "RAC1P"], "&HISP=01", rp, age)
        h, r = acs_load(hp), acs_load(rp)

        native = {k[1]: v for k, v in h.items() if k[0] == "1"}
        nat_inst = sum(v[0] for v in native.values())
        nat_pop = sum(v[1] for v in native.values())
        base_rate = nat_inst / nat_pop
        # Generic-Hispanic coding adjustment, same construction as the peer lane:
        # the excess of HISP=24 ("all other Hispanic") institutionalisation above
        # the all-native rate is reallocated to named origins by population share.
        oth_inst, oth_pop = native.get("24", (0.0, 0.0))
        named_pop = sum(v[1] for k, v in native.items() if k not in ("01", "24"))
        excess = max(0.0, oth_inst - base_rate * oth_pop)

        mex_inst, mex_pop = native.get("02", (0.0, 0.0))
        mex_inst_adj = mex_inst + (excess * mex_pop / named_pop if named_pop else 0.0)
        wht_inst, wht_pop = r.get(("1", "1"), (0.0, 0.0))
        fbm_inst, fbm_pop = h.get(("2", "02"), (0.0, 0.0))

        for name, (inst, pop, inst_adj) in {
            "native_all": (nat_inst, nat_pop, nat_inst),
            "native_nh_white": (wht_inst, wht_pop, wht_inst),
            "native_mexican": (mex_inst, mex_pop, mex_inst_adj),
            "foreign_mexican": (fbm_inst, fbm_pop, fbm_inst),
        }.items():
            rows.append({"band": band, "proxy": name, "institutional": inst, "institutional_adj": inst_adj,
                         "population": pop, "pct": 100 * inst / pop if pop else np.nan,
                         "pct_adj": 100 * inst_adj / pop if pop else np.nan})
    return pd.DataFrame(rows)


# KFF, same brief: "over 60%" of nursing facility residents had Medicaid as
# primary payer. The base arm charges every institutional resident 65+ the
# Medicaid-per-resident cost; this arm charges only the Medicaid-covered share,
# which matters because it is the one assumption that flips the item's sign.
NURSING_MEDICAID_PRIMARY_SHARE = 0.62


def institutional_cost_per_adult(acs: pd.DataFrame, prison_cost: float, adjusted: bool,
                                 nursing_share: float = 1.0) -> dict[str, float]:
    """Annual institutional-care cost per adult 25-64 of each ledger group.

    Numerator: the whole adult (18+) institutional population of the ACS proxy,
    priced at the state-prison cost below 65 and the Medicaid nursing-facility
    cost at 65+. Denominator: the proxy's 25-64 population. So the 65+ cost is
    attributed per-capita to the group's working-age adults, as the brief directs.
    """
    col = "institutional_adj" if adjusted else "institutional"
    tab = acs.set_index(["proxy", "band"])
    out = {}
    for group, (proxy, _note) in ACS_PROXY.items():
        cost = (tab.loc[(proxy, "18_39"), col] * prison_cost
                + tab.loc[(proxy, "40_64"), col] * prison_cost
                + tab.loc[(proxy, "65_plus"), col] * NURSING_COST_PER_YEAR * nursing_share)
        out[group] = float(cost / tab.loc[(proxy, "25_64"), "population"])
    return out


# ---------------------------------------------------------------------------
# CPS-side residual items
# ---------------------------------------------------------------------------

def add_residual_totals(state: dict) -> dict:
    d, index, n_units = state["d"], state["index"], state["n_units"]
    totals = state["totals"]
    diag = {}

    # --- 1a. government-sourced educational assistance ----------------------
    # ED_VAL is the COMBINED amount of Pell grant plus other educational
    # assistance; the file gives only source flags, never a per-source amount.
    #   OED_TYP1 = other GOVERNMENT assistance
    #   OED_TYP2 = scholarships/grants from the school (private)
    #   OED_TYP3 = other (employers, friends) (private)
    # Base rule: the whole amount counts as public when a government source is
    # reported (OED_TYP1 = 1) or when no private source is reported at all (the
    # Pell-only case, which is why ED_VAL exists for those records).
    # Proportional arm: split ED_VAL equally across the reported source channels
    # (Pell counted as one channel when no OED source is reported).
    ed_val = d.ED_VAL.clip(lower=0).to_numpy(dtype=float)
    gov_src = d.OED_TYP1.eq(1).to_numpy()
    priv_src = (d.OED_TYP2.eq(1) | d.OED_TYP3.eq(1)).to_numpy()
    has_ed = d.ED_YN.eq(1).to_numpy()
    ed_gov_base = ed_val * (gov_src | (has_ed & ~priv_src))
    n_channels = (gov_src.astype(float) + d.OED_TYP2.eq(1).to_numpy().astype(float)
                  + d.OED_TYP3.eq(1).to_numpy().astype(float))
    pell_only = has_ed & (n_channels == 0)
    n_channels = np.where(pell_only, 1.0, n_channels)
    gov_channels = gov_src.astype(float) + pell_only.astype(float)
    ed_gov_prop = np.divide(ed_val * gov_channels, n_channels,
                            out=np.zeros_like(ed_val), where=n_channels > 0)
    totals["edu_assistance_government"] = np.bincount(index, weights=ed_gov_base, minlength=n_units)
    totals["edu_assistance_government_proportional"] = np.bincount(index, weights=ed_gov_prop, minlength=n_units)
    diag["ed_recipients_unweighted"] = int(has_ed.sum())
    diag["ed_gov_source_unweighted"] = int((has_ed & gov_src).sum())
    diag["ed_private_only_unweighted"] = int((has_ed & priv_src & ~gov_src).sum())

    # --- 1b. public higher-education operating subsidy -----------------------
    # A_ENRLW is "last week enrolled in high school, college or university",
    # universe ages 16-54; A_HSCOL = 2 is college/university; A_FTPT gives the
    # full/part-time split, used as a crude FTE weight (part-time = 0.5).
    college = (d.A_ENRLW.eq(1) & d.A_HSCOL.eq(2) & d.A_AGE.between(18, 24)).to_numpy()
    fte = np.where(d.A_FTPT.eq(2).to_numpy(), 0.5, 1.0) * college
    for label, share in (("nces", NCES_PUBLIC_UNDERGRAD_SHARE), ("brief074", NCES_PUBLIC_SHARE_BRIEF_FALLBACK)):
        totals[f"higher_ed_subsidy_{label}"] = np.bincount(
            index, weights=fte * share * SHEF_EDU_APPROPRIATIONS_PER_FTE_2024, minlength=n_units)
    totals["college_fte_18_24"] = 1000.0 * np.bincount(index, weights=fte, minlength=n_units)
    diag["college_enrolled_18_24_unweighted"] = int(college.sum())

    # --- 2. ACA advance premium tax credits ---------------------------------
    # MRKS: "Any subsidized Marketplace coverage last year" (1 = yes). This is a
    # direct subsidy indicator, so the fallback (marketplace x national
    # subsidised share) is not needed; it is computed anyway as a cross-check.
    subsidised = d.MRKS.eq(1).to_numpy(dtype=float)
    any_marketplace = d.MRK.eq(1).to_numpy(dtype=float)
    totals["aptc_measured"] = np.bincount(index, weights=subsidised * CMS_APTC_PER_YEAR_2024, minlength=n_units)
    totals["aptc_fallback_share"] = np.bincount(
        index, weights=any_marketplace * CMS_APTC_SHARE_SUBSIDISED_2024 * CMS_APTC_PER_YEAR_2024,
        minlength=n_units)
    diag["marketplace_any_unweighted"] = int(any_marketplace.sum())
    diag["marketplace_subsidised_unweighted"] = int(subsidised.sum())
    diag["marketplace_unsubsidised_unweighted"] = int(d.MRKUN.eq(1).sum())

    # --- 3. uncompensated hospital care of the uninsured --------------------
    # COV = any health insurance coverage last year (2 = no); NOCOV_CYR = 3 is
    # "no coverage for full year", 2 is "no coverage for some of year". The base
    # arm charges full-year-uninsured persons the full annual amount and
    # part-year-uninsured persons half of it.
    full_unins = d.NOCOV_CYR.eq(3).to_numpy(dtype=float)
    part_unins = d.NOCOV_CYR.eq(2).to_numpy(dtype=float)
    ever_unins = d.COV.eq(2).to_numpy(dtype=float)
    exposure = full_unins + 0.5 * part_unins
    totals["uncompensated_care"] = np.bincount(
        index, weights=exposure * UNCOMPENSATED_PER_UNINSURED, minlength=n_units)
    totals["uncompensated_care_2024_prices"] = totals["uncompensated_care"] * UNCOMPENSATED_2024_UPLIFT
    totals["uncompensated_care_ever_uninsured"] = np.bincount(
        index, weights=ever_unins * UNCOMPENSATED_PER_UNINSURED, minlength=n_units)
    diag["uninsured_full_year_unweighted"] = int(full_unins.sum())
    diag["uninsured_part_year_unweighted"] = int(part_unins.sum())

    # --- 5. other unambiguously public transfers ----------------------------
    # WC_TYPE 1 = state worker's compensation (2 = employer/employer insurance,
    # 3 = own insurance, 4 = other). Only 1 is a public programme.
    wc_state = np.where(d.WC_TYPE.eq(1).to_numpy(), d.WC_VAL.clip(lower=0).to_numpy(dtype=float), 0.0)
    # DIS_SC codes: 6 = US railroad retirement disability, 8 = black lung miners'
    # disability, 9 = state temporary sickness. Codes 3 and 5 (federal and
    # state/local government EMPLOYEE disability) are deferred compensation of
    # public employment, not a transfer programme, and are excluded.
    public_dis_codes = [6, 8, 9]
    dis_public = np.zeros(len(d), dtype=float)
    for sc, val in (("DIS_SC1", "DIS_VAL1"), ("DIS_SC2", "DIS_VAL2")):
        dis_public += np.where(d[sc].isin(public_dis_codes).to_numpy(),
                               d[val].clip(lower=0).to_numpy(dtype=float), 0.0)
    totals["other_public_transfers"] = np.bincount(index, weights=wc_state + dis_public, minlength=n_units)
    diag["state_workers_comp_recipients_unweighted"] = int(d.WC_TYPE.eq(1).sum())
    diag["public_disability_recipients_unweighted"] = int((dis_public > 0).sum())

    # Housing subsidy: the capped SPM housing-subsidy resource value. Reported as
    # its own row, never folded into the running balance, because it is a capped
    # RESOURCE value to the household, not the programme's cost to government,
    # and the base generator explicitly holds it outside the fiscal ledger.
    totals["housing_subsidy_capped_resource"] = state["heads"].SPM_CAPHOUSESUB.to_numpy(dtype=float)

    state["diag"] = diag
    return state


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

RESIDUAL_ROWS = [
    ("edu_assistance_government", "Government educational assistance (ED_VAL)"),
    ("higher_ed_subsidy_nces", "Public higher-ed operating subsidy (18-24 FTE)"),
    ("aptc_measured", "ACA advance premium tax credits"),
    ("uncompensated_care", "Uncompensated hospital care (uninsured)"),
    ("other_public_transfers", "Other public transfers (state WC, RR/black-lung/sickness)"),
]
EXTRA_ROWS = [
    ("edu_assistance_government_proportional", "  alt: educational assistance, proportional source split"),
    ("higher_ed_subsidy_brief074", "  alt: higher-ed subsidy at the brief's 0.74 public share"),
    ("aptc_fallback_share", "  alt: APTC from marketplace coverage x national subsidised share"),
    ("uncompensated_care_2024_prices", "  alt: uncompensated care at 2024 hospital prices"),
    ("uncompensated_care_ever_uninsured", "  alt: uncompensated care, any uninsured spell at full cost"),
    ("housing_subsidy_capped_resource", "  memo: SPM capped housing subsidy resource (NOT in the balance)"),
    ("college_fte_18_24", "  diagnostic: college FTE 18-24 per adult (x1000)"),
]


def run(args):
    peer_args = argparse.Namespace(cps_zip=args.cps_zip)
    state = peer.build(peer_args)
    # peer.build() does not return heads; rebuild the head frame for SPM_CAPHOUSESUB.
    d = state["d"]
    state["heads"] = d.loc[d.SPM_HEAD.eq(1)].set_index("SPM_ID").sort_index()
    state = add_residual_totals(state)

    totals, group = state["totals"], state["group"]
    index, n_units = state["index"], state["n_units"]
    adults, weights = state["adults_25_64"], state["person_weights"]

    acs = acs_institutional()
    acs.to_csv(HERE / "acs_institutional_by_age_band.csv", index=False)
    inst_cost = {
        "base": institutional_cost_per_adult(acs, PRISON_COST_PER_YEAR, adjusted=False),
        "generic_hispanic_adjusted": institutional_cost_per_adult(acs, PRISON_COST_PER_YEAR, adjusted=True),
        "prison_45k": institutional_cost_per_adult(acs, PRISON_COST_LOW, adjusted=False),
        "prison_70k": institutional_cost_per_adult(acs, PRISON_COST_HIGH, adjusted=False),
        "nursing_medicaid_share_062": institutional_cost_per_adult(
            acs, PRISON_COST_PER_YEAR, adjusted=False, nursing_share=NURSING_MEDICAID_PRIMARY_SHARE),
        "nursing_062_and_hispanic_adj": institutional_cost_per_adult(
            acs, PRISON_COST_PER_YEAR, adjusted=True, nursing_share=NURSING_MEDICAID_PRIMARY_SHARE),
    }

    rows, lines = [], []

    def out(text=""):
        print(text)
        lines.append(text)

    out("Person-level fiscal-ledger residuals by origin-generation")
    out("CPS ASEC 2025 (income year 2024) + ACS 1-year PUMS 2023, SPM resource units,")
    out("person weights, adults 25-64, 160-replicate SDR standard errors.")
    out(f"CPS source: {state['cps']}")
    out(f"CPS validation: {json.dumps(state['validation'])}")
    out(f"microdata diagnostics: {json.dumps(state['diag'])}")
    out("")
    out("Baseline and extended rows reproduce gen_ledger_extension_2026_09_16/extend_ledger.py")
    out("exactly (same prepare(), same allocate(), same group masks, same composite).")

    gate_value = None
    for allocation, eligible in state["allocations"].items():
        per = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}

        # The peer lane's extended balance, rebuilt at person level exactly as
        # extend_ledger.analyse() does, so the SDR variance of the composite is
        # computed directly rather than summed componentwise.
        extended = (per["cash_noncash_tax_balance"] + per["employer_payroll"]
                    + per["sales_tax_share35"] + per["property_tax_owner"])

        reported = ([m for m, _ in RESIDUAL_ROWS] + [m for m, _ in EXTRA_ROWS]
                    + ["cash_noncash_tax_balance", "k12_cost_at_full_attendance"])
        rep: dict[tuple[str, str], np.ndarray] = {}
        for g, mask in group.items():
            use = adults & mask
            w = weights[use]
            values = np.stack([per[m][use] for m in reported])
            for metric, est in zip(reported, estimate(values, w)):
                rep[g, metric] = est
            rep[g, "extended_balance"] = (estimate(extended[use][None, :], w)[0]
                                          - peer.PUPIL_RATIO_NATIVE_ACS * rep[g, "k12_cost_at_full_attendance"])
            running = rep[g, "extended_balance"].copy()
            for metric, _label in RESIDUAL_ROWS:
                running = running - rep[g, metric]
                rep[g, f"after_{metric}"] = running.copy()
            rep[g, "residual_balance_cps_only"] = running.copy()

        if allocation == "equal_all_members":
            gate_value = sdr(rep["mexican_second_gen", "extended_balance"]
                             - rep[REFERENCE, "extended_balance"])

        out(f"\n{'=' * 140}")
        out(f"== allocation={allocation}  weighting=person  $ per adult 25-64, 2024 income year "
            f"(SDR se in parentheses) ==")
        out(f"{'=' * 140}")
        display = ([("EXTENDED BALANCE (peer lane)", "extended_balance")]
                   + [(lab, m) for m, lab in RESIDUAL_ROWS]
                   + [("= RESIDUAL BALANCE (CPS items only)", "residual_balance_cps_only")]
                   + [(lab, m) for m, lab in EXTRA_ROWS])
        out(f"{'row':60s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS))
        for label, metric in display:
            cells = "".join(f"{sdr(rep[g, metric])[0]:>11,.0f} ({sdr(rep[g, metric])[1]:,.0f})".rjust(18)
                            for g in GROUPS)
            out(f"{label:60s}{cells}")

        out()
        out(f"{'difference from 3rd+ NH white':60s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS))
        for label, metric in display:
            cells = ""
            for g in GROUPS:
                if g == REFERENCE:
                    cells += "—".rjust(18)
                else:
                    e, s = sdr(rep[g, metric] - rep[REFERENCE, metric])
                    cells += f"{e:>11,.0f} ({s:,.0f})".rjust(18)
            out(f"{label:60s}{cells}")

        # ---- the section-12 layout: running balance for every group ---------
        out()
        out("-- §12 layout: each item as a difference from 3rd+ NH white, with the running balance --")
        out(f"{'item':58s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS if g != REFERENCE))
        base_row = "".join(f"{sdr(rep[g, 'extended_balance'] - rep[REFERENCE, 'extended_balance'])[0]:>11,.0f} "
                           f"({sdr(rep[g, 'extended_balance'] - rep[REFERENCE, 'extended_balance'])[1]:,.0f})".rjust(18)
                           for g in GROUPS if g != REFERENCE)
        out(f"{'Extended balance (baseline for this lane)':58s}{base_row}")
        for metric, label in RESIDUAL_ROWS:
            delta = "".join(f"{-sdr(rep[g, metric] - rep[REFERENCE, metric])[0]:>11,.0f}".rjust(18)
                            for g in GROUPS if g != REFERENCE)
            out(f"{('- ' + label):58s}{delta}")
            run_row = "".join(
                f"{sdr(rep[g, f'after_{metric}'] - rep[REFERENCE, f'after_{metric}'])[0]:>11,.0f} "
                f"({sdr(rep[g, f'after_{metric}'] - rep[REFERENCE, f'after_{metric}'])[1]:,.0f})".rjust(18)
                for g in GROUPS if g != REFERENCE)
            out(f"{'    running balance':58s}{run_row}")

        # ---- institutional care, spliced on after the CPS items -------------
        out()
        out("-- institutional care (ACS PUMS proxy, no SDR se available) --")
        out(f"{'arm':34s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS))
        for arm, values in inst_cost.items():
            out(f"{arm:34s}" + "".join(f"{values[g]:>18,.0f}" for g in GROUPS))
        out()
        out(f"{'institutional, diff from white':34s}"
            + "".join(f"{g[:20]:>18s}" for g in GROUPS if g != REFERENCE))
        for arm, values in inst_cost.items():
            out(f"{arm:34s}" + "".join(f"{-(values[g] - values[REFERENCE]):>18,.0f}"
                                       for g in GROUPS if g != REFERENCE))
        out()
        final = {g: sdr(rep[g, "residual_balance_cps_only"])[0] - inst_cost["base"][g] for g in GROUPS}
        out(f"{'FULL RESIDUAL BALANCE (CPS + ACS)':34s}" + "".join(f"{final[g]:>18,.0f}" for g in GROUPS))
        out(f"{'  diff from 3rd+ NH white':34s}"
            + "".join(f"{final[g] - final[REFERENCE]:>18,.0f}" for g in GROUPS if g != REFERENCE))

        # ---- CSV rows -------------------------------------------------------
        all_metrics = ([m for m, _ in RESIDUAL_ROWS] + [m for m, _ in EXTRA_ROWS]
                       + ["extended_balance", "residual_balance_cps_only"]
                       + [f"after_{m}" for m, _ in RESIDUAL_ROWS])
        for g in GROUPS:
            use = adults & group[g]
            for metric in all_metrics:
                est, se = sdr(rep[g, metric])
                de, ds = sdr(rep[g, metric] - rep[REFERENCE, metric])
                rows.append({"allocation": allocation, "weighting": "person", "group": g,
                             "metric": metric, "source": "cps_asec_2025",
                             "n_adults_unweighted": int(use.sum()),
                             "weighted_adults": float(weights[use, 0].sum()),
                             "estimate": est, "se_sdr": se,
                             "difference_from_third_plus_nh_white": de, "se_sdr_difference": ds})
            for arm, values in inst_cost.items():
                rows.append({"allocation": allocation, "weighting": "person", "group": g,
                             "metric": f"institutional_care_{arm}", "source": "acs_pums_2023",
                             "n_adults_unweighted": int(use.sum()),
                             "weighted_adults": float(weights[use, 0].sum()),
                             "estimate": values[g], "se_sdr": np.nan,
                             "difference_from_third_plus_nh_white": values[g] - values[REFERENCE],
                             "se_sdr_difference": np.nan})
            rows.append({"allocation": allocation, "weighting": "person", "group": g,
                         "metric": "full_residual_balance_cps_plus_acs", "source": "combined",
                         "n_adults_unweighted": int(use.sum()),
                         "weighted_adults": float(weights[use, 0].sum()),
                         "estimate": final[g], "se_sdr": np.nan,
                         "difference_from_third_plus_nh_white": final[g] - final[REFERENCE],
                         "se_sdr_difference": np.nan})

    out()
    out("-- ACS institutional group-quarters rates, 2023, by proxy and age band (percent) --")
    out(acs.to_string(index=False))
    out()
    out("-- applied rates --")
    out(f"   SHEEO SHEF FY2024 education appropriations per FTE : ${SHEF_EDU_APPROPRIATIONS_PER_FTE_2024:,.0f}")
    out(f"   NCES public undergraduate share, fall 2023         : {NCES_PUBLIC_UNDERGRAD_SHARE:.4f}")
    out(f"   CMS full-year-2024 APTC per subsidised enrollee    : ${CMS_APTC_PER_YEAR_2024:,.2f}")
    out(f"   AHA/Census uncompensated care per uninsured        : ${UNCOMPENSATED_PER_UNINSURED:,.0f}")
    out(f"   State prison cost per person-year                  : ${PRISON_COST_PER_YEAR:,.0f}")
    out(f"   Medicaid nursing-facility cost per resident-year   : ${NURSING_COST_PER_YEAR:,.0f}")
    out()
    out("-- sources --")
    for label, url in SOURCES:
        out(f"   {label}\n     {url}")

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "residual_micro_by_generation.csv", index=False)

    gate = ["", "-- STEP A gate: peer-lane extended balance --",
            "Mexican 2nd gen minus 3rd+ NH white, EXTENDED balance, equal_all_members,",
            f"person weights, adults 25-64: {gate_value[0]:,.0f} (se {gate_value[1]:,.0f})",
            "Published in gen_ledger_extension_2026_09_16/RESULT.md and memo §12: -8,286 (se 443)",
            f"Deviation from the published -8,286: {gate_value[0] - (-8286):+,.2f}"]
    lines.extend(gate)
    print("\n".join(gate))
    (HERE / "residual_micro_result.txt").write_text("\n".join(lines) + "\n")
    if abs(gate_value[0] - (-8286)) > 50:
        raise SystemExit(f"[BLOCKED] Step A gate failed: {gate_value[0]:,.0f} is more than $50 from -8,286")
    print("[Step A gate] PASS (within $50 of the published -8,286)")
    print(f"\nWrote {HERE / 'residual_micro_by_generation.csv'}")
    print(f"Wrote {HERE / 'residual_micro_result.txt'}")
    print(f"Wrote {HERE / 'acs_institutional_by_age_band.csv'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cps-zip", type=Path, default=None,
                    help="CPS ASEC 2025 public-use CSV zip. Default: the peer lane's resolution order "
                         "(CPS_ASEC_2025_ZIP, PNY_DATA_ROOT, /Volumes/2TBPNY, lane cache).")
    args = ap.parse_args()
    if args.cps_zip is None:
        cached = PEER / "_cache" / "asecpub25csv.zip"
        if cached.exists() and not os.environ.get("CPS_ASEC_2025_ZIP"):
            args.cps_zip = cached
    run(args)


if __name__ == "__main__":
    main()
