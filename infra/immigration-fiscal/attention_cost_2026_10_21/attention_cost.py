"""Attention, compliance, advocacy and agenda cost of immigration as a political issue, 2024.

Each component is reported in its own units (dollars, hours, shares); no comparison benchmark.

Arithmetic only: every input is a cited constant below or a pinned file in inputs/ / derived/.
Writes derived/attention_cost.csv. Dollars are nominal; DOT's value of time is 2023 dollars and is
not inflated (a 2.4% 2024 deflator step would move results by 2.4%).

Run: uv run --no-project python3 infra/immigration-fiscal/attention_cost_2026_10_21/attention_cost.py
"""
import collections
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
OUT = HERE / "derived" / "attention_cost.csv"

# --- Scale -------------------------------------------------------------------------------------
ADULTS_2024 = 267_181_678  # ACS 2024 1-year S0101_C01_026E, population 18+

# --- B. Attention ------------------------------------------------------------------------------
# Allen, Howland, Mobius, Rothschild & Watts 2020, Sci. Adv. 6:eaay3539: TV news 54 min + online
# news 9.7 min per person per day (Nielsen TV + desktop/mobile panels, Jan 2016-Dec 2018; broad
# news incl. morning shows, entertainment news, late-night comedy, portals).
NEWS_MIN_PER_DAY = 54.0 + 9.7
VALUE_TIME_DOT = 21.10  # USDOT BCA Guidance 2025, Table A-2, all purposes, 2023 $/person-hour
WAGE_2024 = 35.06  # BLS CES0500000003, avg hourly earnings, all private employees, 2024 annual avg
GALLUP_MIP_IMM_2024 = [0.20, 0.28, 0.28, 0.27]  # Jan-Apr 2024 share naming immigration (Gallup)
GDELT_LAST_DAY_2024 = "2024-10-10"  # Internet Archive TV feed in GDELT ends here for 2024

# --- A. Private dollars ------------------------------------------------------------------------
I9_HOURS = 33_207_976  # OMB 1615-0047, ICR 202401-1615-009 (approved 2024-05-14)
EVERIFY_HOURS = 1_966_051  # OMB 1615-0092, 88 FR 42091 (2023-06-29)
EVERIFY_COST = 1_887_000  # same notice, annual cost burden $
ICR_LOADED_WAGE = 43.45  # I-9 supporting statement: May 2022 BLS mean $29.76 x 1.46 benefits
LEGAL_SERVICES_2023_BN = 8.7  # IBISWorld via Research&Markets; proprietary model, grade low
LEGAL_SERVICES_2026_BN = 10.6  # IBISWorld 2026 page
PRO_MOVEMENT_FOUNDATION_BN = 0.280  # NCRP 2022 "A Ripple, Not a Wave": avg/yr 2016-2020 (Candid)
RESTRICTIONIST_990_EXP_BN = (7_453_094 + 1_015_093 + 6_782_419 + 3_315_911) / 1e9  # FAIR, NumbersUSA
#   Action + Ed. & Research Fdn, CIS: total functional expenses, tax year 2023 (ProPublica 990 API)

# --- C. Agenda ---------------------------------------------------------------------------------
BILLS_CSV = HERE / "derived" / "bills_policy_area_118.csv"  # from count_bills.py

# --- E. Attribution to the Mexican-origin group ------------------------------------------------
MEX_SHARES = {
    # Pew 2025-08-21: non-Mexico unauthorized 6.4M (2021) -> 9.7M (2023), total +3.5M,
    # so Mexico's share of the 2021-23 increase is (3.5 - 3.3) / 3.5.
    "low_surge_increment": (3.5 - (9.7 - 6.4)) / 3.5,
    "central_pew2023_stock": 0.30,  # Pew 2023: Mexico 4.3M = 30% of 14.0M unauthorized
    "high_dhs2022_stock": 4.81 / 10.99,  # DHS OHSS Jan 2022, Table 2
}
CBP_CSV = INPUTS / "cbp_sbo_encounters_fy23_fy26_aug.csv"  # CBP SW land border encounters, FY23-FY26


def cbp_fy24_mexico() -> tuple:
    mex = tot = 0
    with CBP_CSV.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["Fiscal Year"] != "2024":
                continue
            c = int(r["Encounter Count"].replace(",", ""))
            tot += c
            mex += c if r["Citizenship Grouping"].strip().upper() == "MEXICO" else 0
    if (mex, tot) != (653_684, 2_135_005):
        raise SystemExit(f"[BLOCKED] CBP FY2024 counts changed: {mex}/{tot}")
    return mex, tot


def gdelt_mean(name: str, year: int) -> dict:
    rows = collections.defaultdict(list)
    with (INPUTS / f"gdelt_tv_{name}_{year}.csv").open(encoding="utf-8-sig") as f:
        for r in csv.reader(f):
            if r[1] == "Series" or (year == 2024 and r[0] > GDELT_LAST_DAY_2024):
                continue
            rows[r[1]].append(float(r[2]) / 100)
    return {k: sum(v) / len(v) for k, v in rows.items()}


def main() -> None:
    out = []

    def add(component, item, value, unit, note):
        out.append([component, item, f"{value:.6g}", unit, note])


    # B. hours of news per year, adults
    news_hours = ADULTS_2024 * NEWS_MIN_PER_DAY / 60 * 365
    add("B", "adult_news_hours_per_year", news_hours / 1e9, "bn hours", "Allen et al. 2020 minutes x ACS 18+")
    narrow = gdelt_mean("immigration_narrow", 2024)
    border = gdelt_mean("immigration_border", 2024)
    mip = sum(GALLUP_MIP_IMM_2024) / len(GALLUP_MIP_IMM_2024)
    shares = {
        "low_cable_narrow_mean": sum(narrow.values()) / 3,
        "mid_cable_border_mean": sum(border.values()) / 3,
        "high_fox_border": border["FOXNEWS"],
    }
    for k, s in shares.items():
        add("B", f"immigration_share_{k}", s, "share", "GDELT TV 2024-01-01..10-10 mention-clip share")
    add("B", "gallup_mip_jan_apr_2024_mean", mip, "share of adults", "salience, not airtime; not used for hours")
    for k, s in shares.items():
        h = news_hours * s
        add("B", f"gross_hours_{k}", h / 1e9, "bn hours", "news hours x share")
        for vlabel, v in (("dot", VALUE_TIME_DOT), ("wage", WAGE_2024)):
            bn = h * v / 1e9
            add("B", f"gross_value_{k}_{vlabel}", bn, "$bn", f"x ${v}/h")
            for ak, a in MEX_SHARES.items():
                add("E", f"mex_{ak}_B_{k}_{vlabel}", bn * a, "$bn", f"attribution {a:.3f}")
    add("B", "net_of_substitution", float("nan"), "$bn", "unidentified; see RESULT")

    # A. compliance and advocacy
    i9 = I9_HOURS * ICR_LOADED_WAGE / 1e9
    ev = (EVERIFY_HOURS * ICR_LOADED_WAGE + EVERIFY_COST) / 1e9
    add("A", "i9_hours_value", i9, "$bn", "33.2M h x $43.45 (ICR wage basis)")
    add("A", "everify_value", ev, "$bn", "1.97M h x $43.45 + $1.887M")
    legal_2024 = LEGAL_SERVICES_2023_BN * (LEGAL_SERVICES_2026_BN / LEGAL_SERVICES_2023_BN) ** (1 / 3)
    add("A", "legal_services_revenue_2024_interp", legal_2024, "$bn", "IBISWorld 2023->2026 geometric; mostly admissions casework")
    adv = PRO_MOVEMENT_FOUNDATION_BN + RESTRICTIONIST_990_EXP_BN
    add("A", "advocacy_pro_foundation_grants", PRO_MOVEMENT_FOUNDATION_BN, "$bn", "NCRP 2016-20 avg")
    add("A", "advocacy_restrictionist_big3_exp", RESTRICTIONIST_990_EXP_BN, "$bn", "990 TY2023")
    a_total = i9 + ev + legal_2024 + adv
    add("A", "total_private_dollars", a_total, "$bn", "compliance + legal + advocacy (lobbying not separable)")
    for ak, a in MEX_SHARES.items():
        add("E", f"mex_{ak}_A_total", a_total * a, "$bn", f"attribution {a:.3f}")

    # C. agenda
    with BILLS_CSV.open() as f:
        bills = {r["policy_area"]: r for r in csv.DictReader(f)}
    imm, tot = bills["Immigration"], bills["TOTAL"]
    add("C", "bills_118_immigration_share", int(imm["introduced"]) / int(tot["introduced"]), "share", "H.R.+S. policy area")
    add("C", "laws_118_immigration_share", int(imm["became_law"]) / int(tot["became_law"]), "share", "policy area of enacted bills")

    mex, tot = cbp_fy24_mexico()
    add("E", "cbp_fy24_mexico_share", mex / tot, "share", "SW border encounters")
    for ak, a in MEX_SHARES.items():
        add("E", f"attribution_{ak}", a, "share", "")

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["component", "item", "value", "unit", "note"])
        w.writerows(out)
    print(f"  ✓ wrote {OUT.relative_to(HERE)} ({len(out)} rows)")


if __name__ == "__main__":
    main()
