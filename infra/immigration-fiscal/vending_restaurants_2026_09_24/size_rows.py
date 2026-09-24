"""Size of street-food vending against restaurant sales, and the winners-and-losers rows.

Vending size (read and quoted in reads/): City of Los Angeles, about 10,000 food vendors (Bureau of
Street Services estimate, CLA report CF 13-1493, 26 Nov 2014, p. 2) at $10,098 revenue per vendor per
year (2014 student survey, Economic Roundtable "Sidewalk Stimulus" 2015, p. 3): $101m a year, the
report's "over $100 million" (p. 5). Both inputs are weak (an unsourced count, a convenience sample),
so the band is half to double: $50m-$202m in 2014 dollars. Each year is restated with the CPI for
food away from home (BLS CUUR0000SEFV, annual average) and set against that year's taxable sales of
food services and drinking places (CDTFA C08), one year at a time.

California: the City's figure scaled by Hispanic residents (ACS 2013-2017), California over the City.
LA's vending density is probably the state's highest, so this is an upper extrapolation.

Rows (derived/winners_losers_rows.csv), $bn a year in 2024 dollars. Licensed food trucks get no row:
their measured sign is mixed (RESULT.md section 5.6). Rows whose values are all
non-negative are magnitudes in the stated direction. The two measured rows are signed from the
group's side (positive = better off; a negative bn_low means the interval includes a loss), with the
direction set by the central, which is how the winners-losers lane reads signed rows.

Writes derived/size_by_year.csv, derived/winners_losers_rows.csv, derived/size_inputs.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/size_rows.py
"""
import csv
import json

import pandas as pd

from lib import CACHE, DERIVED

FOOD_VENDORS, REV_PER_VENDOR = 10_000, 10_098          # CLA 2014 p.2; Sidewalk Stimulus 2015 p.3
ALL_VENDORS = 50_000                                    # CLA 2014 p.2
BAND = (0.5, 1.0, 2.0)                                  # low, central, high multipliers on the size
CONTRIB_MARGIN = (0.20, 0.35, 0.50)                     # assumed share of lost sales that is lost profit
SALES_TAX_LA = 0.095                                    # City of LA combined rate from 2017 [assumed from CDTFA rate tables]
PERMITS_PER_YEAR = 944                                  # CAO fee study 2023 p.3
NET_SHARE = 0.29                                        # Sidewalk Stimulus p.4: 71% of revenue spent on inputs
PROGRAM_COST_M, PERMIT_RECEIPTS_M = 3.8, 0.238          # CAO fee study 2023 p.3 ($m, FY2023-24; average receipts)
YEAR = 2024


def cpi() -> dict:
    out = {}
    for f in ("cpi_sefv.json", "cpi_sefv_2024.json"):
        d = json.loads((CACHE / "bls" / f).read_text())
        for r in d["Results"]["series"][0]["data"]:
            if r["period"] == "M13":
                out[int(r["year"])] = float(r["value"])
    return out


def main() -> None:
    idx = cpi()
    city = pd.read_csv(CACHE / "cdtfa_city_annual.csv")
    cty = pd.read_csv(CACHE / "cdtfa_county_annual.csv")
    cty = cty.loc[:, ~cty.columns.duplicated()]
    la = city[(city["city"] == "Los Angeles") & (city["group"] == "C08") & (city["quarters"] == 4)].set_index("year")
    ca = cty[(cty["group"] == "C08") & (cty["quarters"] == 4)].groupby("year")["taxable"].sum()
    place = json.loads((CACHE / "acs" / "acs5_2017_place_ca.json").read_text())
    ph = dict(zip(place[0], next(r for r in place[1:] if r[place[0].index("place")] == "44000")))
    la_hisp, la_pop_m = float(ph["B03002_012E"]), float(ph["B03002_001E"]) / 1e6
    ex = pd.read_csv(DERIVED / "exposure_county.csv", dtype={"fips": str})
    exca = ex[ex["fips"].str.startswith("06")]
    ca_hisp = float((exca["pop"] * exca["hisp_share"]).sum())
    ca_pop = float(exca["pop"].sum())
    scale = ca_hisp / la_hisp
    rows = []
    for y in range(2015, 2026):
        if y not in la.index or y not in idx:
            continue
        v = FOOD_VENDORS * REV_PER_VENDOR * idx[y] / idx[2014]
        rows.append({"year": y, "cpi_fafh": idx[y], "food_vending_la_city_m": round(v / 1e6, 2),
                     "c08_la_city_m": round(la.loc[y, "taxable"] / 1e6, 1),
                     "share_la_city_pct": round(100 * v / la.loc[y, "taxable"], 3),
                     "share_la_city_low_pct": round(100 * BAND[0] * v / la.loc[y, "taxable"], 3),
                     "share_la_city_high_pct": round(100 * BAND[2] * v / la.loc[y, "taxable"], 3),
                     "food_vending_ca_upper_m": round(v * scale / 1e6, 1),
                     "c08_ca_m": round(ca.loc[y] / 1e6, 1),
                     "share_ca_pct": round(100 * v * scale / ca.loc[y], 3)})
    by_year = pd.DataFrame(rows)
    by_year.to_csv(DERIVED / "size_by_year.csv", index=False, lineterminator="\n")
    r24 = by_year.set_index("year").loc[YEAR]
    v24 = r24["food_vending_la_city_m"] / 1e3        # $bn, LA City, central
    v24_ca = r24["food_vending_ca_upper_m"] / 1e3    # $bn, California upper extrapolation

    # CBP California restaurants, 2023 (latest): owners = establishments, workers = employment, pay
    cbp = pd.read_csv(CACHE / "cbp_county_panel.csv", dtype={"fips": str, "naics": str})
    c23 = cbp[(cbp["year"] == 2023) & (cbp["naics"] == "7225") & cbp["fips"].str.startswith("06")]
    ca_estab, ca_emp, ca_pay = c23["estab"].sum(), c23["emp"].sum(), c23["payann"].sum() * 1e3
    pay_ratio = ca_pay / (ca.loc[2023])  # restaurant payroll per dollar of C08 taxable sales
    # measured changes after legalization: California county regression of C08 sales on Hispanic share
    ss = pd.read_csv(DERIVED / "sales_event_summary.csv")
    m = ss[(ss["level"] == "county") & (ss["exposure"] == "hisp_share") & (ss["outcome"] == "l_c08")
           & (ss["weight"] == "pop")].iloc[0]
    exca = exca.copy()
    cty24 = cty[(cty["group"] == "C08") & (cty["year"] == YEAR)].set_index("county")["taxable"]
    exca["unit"] = exca["NAME"].str.replace(" County, California", "", regex=False).str.upper()
    exca["sales24"] = exca["unit"].map(cty24)
    exca = exca.dropna(subset=["sales24"])
    hmin = exca["hisp_share"].min()
    lever = float(((exca["hisp_share"] - hmin) * 10 * exca["sales24"]).sum())  # $ x (10-point units above min)
    ch = {k: lever * b / 1e9 for k, b in (("central", m["b2019"]), ("low", m["b2019"] - 1.96 * m["se2019"]),
                                          ("high", m["b2019"] + 1.96 * m["se2019"]))}
    # signed from the group's side (positive = better off), as the winners-losers lane reads signed rows
    own = {k: ch[k] * CONTRIB_MARGIN[1] for k in ch}
    wrk = {k: ch[k] * pay_ratio for k in ch}
    inputs = {"year": YEAR, "cpi_fafh_2014": idx[2014], "cpi_fafh_2024": idx[YEAR], "la_city_hispanic": la_hisp,
              "ca_hispanic": ca_hisp, "ca_pop": ca_pop, "scale_ca_over_la_city": scale,
              "food_vending_la_city_bn_2024": v24, "food_vending_ca_upper_bn_2024": v24_ca,
              "ca_7225_estab_2023": int(ca_estab), "ca_7225_emp_2023": int(ca_emp), "ca_7225_payroll_bn_2023": ca_pay / 1e9,
              "payroll_per_c08_dollar_2023": pay_ratio, "county_c08_b2019": m["b2019"], "county_c08_se2019": m["se2019"],
              "hisp_min_ca_county": hmin, "lever_bn": lever / 1e9, "sales_change_bn": ch}
    (DERIVED / "size_inputs.json").write_text(json.dumps(inputs, indent=1, default=float) + "\n")

    W = []

    def row(group, channel, direction, lo, ce, hi, pop_m, basis, rel, cf, src):
        pp = "" if ce == "" or pop_m in ("", 0) else round(ce * 1e9 / (pop_m * 1e6), 2)
        W.append({"group": group, "channel": channel, "direction": direction,
                  "bn_low": "" if lo == "" else round(lo, 4), "bn_central": "" if ce == "" else round(ce, 4),
                  "bn_high": "" if hi == "" else round(hi, 4), "population_m": pop_m, "per_person_usd": pp,
                  "basis": basis, "relation_to_account": rel, "counterfactual": cf, "source": src})

    cf_law = "California before SB 946 (vending a misdemeanor in most cities, still widespread)"
    cf_none = "no street-food vending at all"
    row("licensed restaurant owners", "restaurant sales after legalization, 2019, from high- vs low-Hispanic counties",
        "gain" if own["central"] > 0 else "loss", own["low"], own["central"], own["high"], round(ca_estab / 1e6, 4),
        "measured",
        "beside", cf_law,
        "CALCULATION: size_rows.py; county C08 taxable-sales event study (analyze_sales.py), pop-weighted, x 0.35 margin")
    row("licensed restaurant owners", "bound: every street-food dollar taken from restaurants, lost at the margin "
        "(low = no displacement)", "loss", 0.0, v24_ca * CONTRIB_MARGIN[1], v24_ca * BAND[2] * CONTRIB_MARGIN[2],
        round(ca_estab / 1e6, 4), "modelled", "beside", cf_none,
        "Sidewalk Stimulus 2015 p.3,5; CLA 2014 p.2; CDTFA C08; LA City size scaled to California by Hispanic "
        "residents; margin 0.35 central, 0.50 high, assumed")
    row("restaurant workers", "restaurant payroll after legalization, 2019, from high- vs low-Hispanic counties",
        "gain" if wrk["central"] > 0 else "loss", wrk["low"], wrk["central"], wrk["high"], round(ca_emp / 1e6, 3),
        "measured", "beside", cf_law,
        "CALCULATION: size_rows.py; same regression x CBP 2023 payroll per C08 dollar")
    row("restaurant workers", "bound: payroll on every displaced street-food dollar, before re-employment "
        "(low = no displacement)", "loss", 0.0, v24_ca * pay_ratio, v24_ca * BAND[2] * pay_ratio,
        round(ca_emp / 1e6, 3), "modelled", "overlaps:production_term", cf_none,
        "as above x CBP 2023 California restaurant payroll per C08 sales dollar; gross of re-employment")
    row("vendors", "net income of street-food vendors (level, City of LA): revenue less the 71% spent on inputs",
        "gain", v24 * BAND[0] * NET_SHARE, v24 * NET_SHARE, v24 * BAND[2] * NET_SHARE, FOOD_VENDORS / 1e6, "modelled",
        "beside", cf_none + " (vendors' next-best earnings not deducted)",
        "Sidewalk Stimulus 2015 p.3 ($10,098 per vendor), p.4 (71% of revenue spent on inputs); CLA 2014 p.2; CPI-FAFH")
    row("vendors", "gain from legalization itself (no arrests or criminal records, fewer confiscations)", "gain",
        "", "", "", ALL_VENDORS / 1e6, "unpriced", "beside", cf_law,
        "unpriced: no measure of vendor numbers, hours or incomes before and after 2019; LAPD 42.00 arrests fell 1,219 (2013) to 4 (2018)")
    row("vendors' customers", "cheaper and closer food, variety", "gain", "", "", "", "", "unpriced",
        "overlaps:consumer_price_benefit", cf_none,
        "unpriced: no price or quantity data; the consumer-price lane's broad scope includes food away from home")
    row("budget", "income and payroll tax on vendors' earnings", "loss", "", "", "", round(ca_pop / 1e6, 2), "unpriced",
        "inside", "vendors' earnings reported like wages",
        "inside the adopted account: Tax records correction (Census tax model status and compliance, CPS fill-ins, "
        "Mexico-born recount, state-aware status flag; audit rows 2, 13, 4; +$19.9/21.2bn), main_case_2026_09_24")
    row("budget", "sales tax not remitted on street-food sales (City of LA, 9.5%)", "loss", v24 * BAND[0] * SALES_TAX_LA,
        v24 * SALES_TAX_LA, v24 * BAND[2] * SALES_TAX_LA, round(la_pop_m, 2), "modelled", "beside", "all vending sales taxed",
        "size above x 9.5%; Sidewalk Stimulus p.6 puts all vendors (food and merchandise) at >= $33m")
    row("budget", "City of LA vending program net of permit receipts (FY2023-24)", "loss",
        PROGRAM_COST_M / 1e3 - PERMIT_RECEIPTS_M / 1e3, PROGRAM_COST_M / 1e3 - PERMIT_RECEIPTS_M / 1e3,
        PROGRAM_COST_M / 1e3 - PERMIT_RECEIPTS_M / 1e3, round(la_pop_m, 2), "measured", "beside",
        "no city vending program (the pre-2019 LAPD enforcement cost it replaced is not netted)",
        "CAO Sidewalk and Park Vending Fee Study Update, 25 Jul 2023, p.3; pre-2019 LAPD enforcement cost not measured")
    row("residents near vending", "litter, obstruction, noise", "loss", "", "", "", "", "unpriced", "beside", cf_none,
        "unpriced: MyLA311 has no vending request type 2015-2026 [VERIFIED NEGATIVE]; no other complaint series found")
    with (DERIVED / "winners_losers_rows.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(W[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(W)
    print(by_year.to_string(index=False))
    print(json.dumps(inputs, indent=1, default=float))
    for r in W:
        print(r["group"], "|", r["channel"], "|", r["bn_low"], r["bn_central"], r["bn_high"], "|", r["per_person_usd"])


if __name__ == "__main__":
    main()
