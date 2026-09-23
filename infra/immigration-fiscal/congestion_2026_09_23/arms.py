"""Road congestion cost to other US residents of the Mexican-origin group's traffic, 2024.

Frame (brief, not changed): the complete annual account's stationary comparison of 2024 with and
without the 40.896574m CPS Mexican-origin residents; effects on all other residents. Money is
2024 dollars a year.

Approach A, network delay on a fixed road network.
  Base: Texas A&M Transportation Institute, 2025 Urban Mobility Report (UMR), 2024 delay in 494
  urban areas (person-hours of passengers and of truck occupants, excess fuel), split into weekday
  peak periods and the rest.
  A1 (the brief's BPR arm). Per-vehicle delay on a link rises as (V/C)^beta. Removing the share psi
  of vehicles scales every remaining vehicle's delay by (1 - psi)^beta, so other residents save
  D_other * [1 - (1 - psi)^beta]: the integral over the group's whole (inframarginal) traffic; the
  marginal approximation beta * psi is reported beside it. "Trips fixed" keeps everyone else's
  travel as it is. "DT fill-in" lets others' driving replace part of the group's: at fixed lanes,
  metro traffic rises with population at elasticity eta = 0.32-0.48 (Duranton-Turner 2009, table 2
  panel A), so traffic falls by 1 - (1 - psi)^eta instead of psi.
  A2 (city-level supply curve, Couture-Duranton-Turner 2018, "CDT"): with lanes fixed the time cost
  of a km is C = Omega * VKT^k, k = theta / (1 - theta). Others' demand VKT_o = Gamma * C^-sigma.
  Removing the share psi of VKT moves C to (1 - psi)^(k / (1 + k sigma)); others gain
  T_o * (1 - C0^(1 - sigma)) / (1 - sigma), T_o their current vehicle-occupant hours.
Approach B, city size: the elasticity of travel speed with respect to metro population, applied to
  the group's population share and valued on others' total vehicle-occupant hours.
  B1. Lanes held fixed: -0.12 (SE 0.035), CDT table 10 column 6, speed on log lanes and log
      population, 100 MSAs, 2008.
  B2. Lanes as they vary across metros: the unconditional elasticity -0.072 (CDT section 6).
  B3. Proportional capacity: the residual when lanes (or road spending) grow with population, from
      CDT's decreasing returns, (theta - a) / (1 - theta), divided by (1 + k sigma) when others'
      demand responds; or 0.12 - 0.066 from the table 10 column 6 regression.
Trucks enter every arm through the UMR truck delay and the group's share of truck traffic tau.
Other residents' vehicle-occupant hours come from NHTS 2022 (2017 variant) hours per person by
urban-area size; area populations are the UMR's, shares are the ACS PUMA allocation's.

Outputs (derived/): umr_positive_control.json, ua_exposure.csv, cbsa_commute.csv, vot_2024.csv,
parameters.csv, arms_grid.csv, arms_summary.csv, metro_distribution.csv, checks.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/arms.py
"""
from __future__ import annotations

import itertools
import json
import pathlib
import re

import numpy as np
import openpyxl
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
XWALK_UA = CACHE / "xwalk_puma22_ua20.csv"
XWALK_COUNTY = ROOT / "infra/immigration-fiscal/employment_entry_2026_09_18/_cache/xwalk_puma22.csv"
COUNTY_CBSA = ROOT / "infra/immigration-fiscal/hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv"
ACCOUNT_MODEL = ROOT / "infra/immigration-fiscal/assumption_explorer_2026_09_21/derived/model.json"

TARGET = 40.896574e6          # CPS ASEC 2025 union, complete account
RESIDENTS = 340.110988e6      # complete-account denominator (= ACS 2024 B01003)

# UMR 2025, Appendix A, Exhibit A-11 and text (national constants, 2024).
UMR_OCC, TRUCK_OCC, UMR_VOT, UMR_CVOT = 1.50, 1.14, 24.01, 80.16
# UMR 2025 Exhibit 15 (share of weekly delay by weekday, 2024) and Exhibits 10 and 13 (share of
# weekday delay in the 6-10 a.m. and 3-7 p.m. peaks, freeways and arterials, 2024), read from charts.
WEEKDAY_SHARE = 0.143 + 0.167 + 0.173 + 0.178 + 0.175
PEAK_FREEWAY, PEAK_ARTERIAL = 0.651, 0.608
DELTA = WEEKDAY_SHARE * (PEAK_FREEWAY + PEAK_ARTERIAL) / 2   # share of delay in weekday peaks

# USDOT, Revised Departmental Guidance on Valuation of Travel Time (2016, Revision 2), tables 1-4.
PERSONAL_SHARE = {"low": 0.35, "central": 0.50, "high": 0.60}     # of hourly household income
BUSINESS_SHARE = {"low": 0.80, "central": 1.00, "high": 1.20}     # of hourly compensation
LOCAL_MIX = (0.954, 0.046)                                        # personal, business
HOURS_PER_YEAR = 2080
# 2024 inputs: Census table H-8 (CPS ASEC 2025), median household income 2024, current dollars;
# BLS OEWS May 2024 news release (2 April 2025) table 1 medians; ECEC 2015Q2 and 2024Q2 via the API.
MEDIAN_HH_INCOME_2024 = 83_160
MEDIAN_WAGE_2024 = 23.80
TRUCK_DRIVERS_2024 = {"heavy": (2_070_480, 27.62), "light": (994_410, 21.22)}
UNDER5_SHARE = 18_365_047 / 340_110_990      # ACS 2024 B01001 (003E + 027E) / 001E

# CDT "Speed" (REStat 2018); table and section numbers are those of the 2016 working paper on HAL.
THETA = {"low": 0.07, "central": 0.13, "high": 0.19}            # table 8 range, table 5 col 6
SIGMA = {"0": 0.0, "8": 8.0, "16": 16.0, "32": 32.0}            # table 8, from Duranton-Turner
POP_FIXED_LANES = {"low": 0.085, "central": 0.12, "high": 0.155}  # table 10 col 6, +/- 1 SE
LANES_COEF_T10 = 0.066                                           # table 10 col 6, log lane
POP_UNCONDITIONAL = 0.072                                        # section 6, 100 MSAs
# Supply-side decreasing returns: (log lane, -log VTT) pairs from table 5 and the PMSA text; the
# footnote 19 construction-cost version puts a - theta at -0.06 to -0.07.
DECREASING_RETURNS = {"T5 col 0": (0.073, 0.094), "T5 col 2": (0.083, 0.11), "T5 col 4 FE": (0.064, 0.085),
                      "T5 col 6 IV2": (0.090, 0.13), "T5 col 8 IV4": (0.096, 0.14), "PMSA text": (0.15, 0.20)}
COST_BASIS = {"fn19 -0.06": 0.06, "fn19 -0.07": 0.07}
# Duranton-Turner 2009 (NBER w15376) table 2 panel A, ln population at fixed interstate lane km,
# columns 2, 3 and 5: fill-in of the group's traffic by others.
FILL_IN = {"trips fixed": 1.0, "DT 0.48": 0.48, "DT 0.44": 0.44, "DT 0.32": 0.32}
# NCHRP Report 716 (2012) p. 77: average BPR functions fitted to 18 MPOs' curves, arterials 3.001,
# freeways 5.883 (Table 4.26's parameter averages for large MPOs are higher, 4.40 and 6.95); original 4.
BETA = {"low": 3.001, "central": 4.0, "high": 5.883}
HEAVY_RAIL = ("New York", "Chicago", "Washington", "Boston", "Philadelphia", "San Francisco",
              "Atlanta", "Baltimore", "Miami", "Los Angeles", "Cleveland")
UMR_OVERRIDES = {"Louisville-Jefferson County KY-IN": "51755", "Boise ID": "08785",
                 "Coeur d'Alene ID": "18451", "East Stoudsburg PA-NJ": "25849"}


# ----------------------------------------------------------------------------- inputs

def load_umr():
    wb = openpyxl.load_workbook(CACHE / "complete-data-2025-umr-by-tti.xlsx", read_only=True, data_only=True)
    rows = [r for r in wb["urban areas"].iter_rows(values_only=True)][5:]
    cols = {0: "area_group", 1: "name", 2: "state", 3: "size", 5: "pop_k", 7: "auto_commuters_k",
            8: "freeway_dvmt_k", 9: "arterial_dvmt_k", 10: "vot", 11: "commercial_vot", 12: "gas_price",
            13: "diesel_price", 17: "fuel_kgal", 21: "delay_kph", 23: "delay_per_auto_commuter",
            25: "tti", 31: "cost_musd", 33: "cost_per_auto_commuter", 35: "truck_delay_kph",
            37: "truck_fuel_kgal", 39: "truck_cost_musd"}
    u = pd.DataFrame([{v: r[k] for k, v in cols.items()} for r in rows if str(r[4]) == "2024"])
    for c in cols.values():
        if c not in ("area_group", "name", "state", "size"):
            u[c] = pd.to_numeric(u[c])
    summary = {r[1]: r for r in wb["summaries"].iter_rows(values_only=True) if r[3] in ("2024", 2024)}
    return u, summary


def positive_control(u, summary):
    """Reproduce the UMR's published 2024 national totals and each area's cost from its parts."""
    pub = summary["494 Area Sum"]
    pas_time = (u.delay_kph - u.truck_delay_kph) * u.vot / 1e3
    pas_fuel = (u.fuel_kgal - u.truck_fuel_kgal) * u.gas_price / 1e3
    truck = u.truck_delay_kph / TRUCK_OCC * u.commercial_vot / 1e3 + u.truck_fuel_kgal * u.diesel_price / 1e3
    rebuilt = pas_time + pas_fuel + truck
    big = u.cost_musd >= 50
    out = {
        "report_exhibit_1_2024": {"travel_delay_bn_hours": 9.8, "congestion_cost_bn_2024usd": 269,
                                  "truck_congestion_cost_bn": 35.8, "wasted_fuel_bn_gallons": 2.8,
                                  "cost_per_auto_commuter_usd": 1480},
        "sum_of_494_areas": {"travel_delay_bn_hours": u.delay_kph.sum() / 1e6,
                             "congestion_cost_bn_2024usd": u.cost_musd.sum() / 1e3,
                             "truck_congestion_cost_bn": u.truck_cost_musd.sum() / 1e3,
                             "wasted_fuel_bn_gallons": u.fuel_kgal.sum() / 1e6,
                             "total_cost_over_auto_commuters_usd": u.cost_musd.sum() / u.auto_commuters_k.sum() * 1e3},
        "summaries_sheet_494_area_sum": {"delay_kph": pub[20], "cost_musd": pub[30], "truck_cost_musd": pub[38]},
        "cost_rebuilt_from_parts_bn": float(rebuilt.sum() / 1e3),
        "cost_rebuilt_max_abs_rel_error_areas_over_50m": float((rebuilt[big] / u.cost_musd[big] - 1).abs().max()),
        "truck_cost_rebuilt_bn": float(truck.sum() / 1e3),
        "passenger_time_cost_bn": float(pas_time.sum() / 1e3),
        "passenger_fuel_cost_bn": float(pas_fuel.sum() / 1e3),
    }
    # UMR Eq. A-4: peak-period delay over auto commuters plus other delay over population. With
    # the chart-read peak share DELTA it should return Exhibit 1's 63 hours per auto commuter.
    passenger = (u.delay_kph - u.truck_delay_kph).sum() * 1e3
    out["eq_a4_hours_per_auto_commuter_national_delta"] = float(
        DELTA * passenger / (u.auto_commuters_k.sum() * 1e3) + (1 - DELTA) * passenger / (u.pop_k.sum() * 1e3))
    out["report_exhibit_1_2024"]["delay_per_auto_commuter_hours"] = 63
    s = out["sum_of_494_areas"]
    out["passed"] = bool(abs(s["travel_delay_bn_hours"] - 9.8) < 0.05 and abs(s["congestion_cost_bn_2024usd"] - 269) < 0.5
                         and abs(s["truck_congestion_cost_bn"] - 35.8) < 0.05
                         and abs(out["eq_a4_hours_per_auto_commuter_national_delta"] / 63 - 1) < 0.03
                         and out["cost_rebuilt_max_abs_rel_error_areas_over_50m"] < 0.015)
    return out


def parse_umr_name(name):
    m = re.match(r"^(.*?)[\s-]+([A-Z]{2}(?:-[A-Z]{2})*)$", name.strip())
    return m.group(1).lower(), m.group(2).split("-")


def match_umr(u, xw):
    """UMR urban area -> 2020 Census urban area: exact name, else first city, else any city, same state."""
    ua = xw[xw.ua != "99999"].groupby(["ua", "uaname"], as_index=False)["pop20"].sum()
    split = ua.uaname.str.rsplit(", ", n=1)
    ua["cities"] = split.str[0].str.replace("--", "-").str.lower()
    ua["states"] = split.str[1].str.split("--")
    ua["first"] = ua.cities.str.split("-").str[0]
    out = []
    for _, r in u.iterrows():
        if r["name"] in UMR_OVERRIDES:
            c = ua[ua.ua == UMR_OVERRIDES[r["name"]]].iloc[0]
            out.append((c.ua, c.uaname, "override", c.pop20))
            continue
        cities, _ = parse_umr_name(r["name"])
        same_state = ua.states.map(lambda s: r.state in s)
        for how, test in (("exact", ua.cities.eq(cities)), ("first_city", ua["first"].eq(cities.split("-")[0])),
                          ("any_city", ua.cities.map(lambda n: any(t in n.split("-") for t in cities.split("-"))))):
            cand = ua[test & same_state]
            if len(cand):
                c = cand.sort_values("pop20", ascending=False).iloc[0]
                out.append((c.ua, c.uaname, how, c.pop20))
                break
        else:
            out.append((None, None, "puerto_rico" if r.state == "PR" else "unmatched", np.nan))
    u = u.copy()
    u["ua"], u["ua_name"], u["match"], u["ua_pop20"] = zip(*out)
    return u


def load_cells():
    cells = pd.read_csv(DERIVED / "pums_puma_commute.csv", dtype={"STATE": str, "PUMA": str})
    wide = cells.pivot_table(index=["STATE", "PUMA"], columns="group", aggfunc="sum", fill_value=0)
    wide.columns = [f"{g}_{v}" for v, g in wide.columns]
    return wide.reset_index()


def allocate(wide, alloc, key):
    """Spread PUMA cells over areas by population allocation factors, preserving national totals."""
    alloc = alloc.copy()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    merged = wide.merge(alloc, left_on=["STATE", "PUMA"], right_on=["state", "puma"], how="left",
                        validate="one_to_many")
    if merged[key].isna().any():
        raise ValueError(f"PUMAs without allocation rows: {merged[merged[key].isna()][['STATE', 'PUMA']].head()}")
    values = [c for c in wide.columns if c not in ("STATE", "PUMA")]
    merged[values] = merged[values].mul(merged["afact"], axis=0)
    areas = merged.groupby(key)[values].sum()
    for c in values:
        if not np.isclose(areas[c].sum(), wide[c].sum(), rtol=1e-9):
            raise ValueError(f"allocation lost {c}")
    return areas


def ua_areas(wide):
    xw = pd.read_csv(XWALK_UA, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"].str.strip())
    xw["pop20"] = pd.to_numeric(xw["pop20"])
    xw = xw.rename(columns={"puma22": "puma"})
    return allocate(wide, xw[["state", "puma", "ua", "afact"]], "ua"), xw


def cbsa_areas(wide):
    xw = pd.read_csv(XWALK_COUNTY, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(COUNTY_CBSA, dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa", "cbsa_title"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    titles = xw.dropna(subset=["cbsa"]).drop_duplicates("cbsa").set_index("cbsa")["cbsa_title"]
    return allocate(wide, alloc, "area"), titles


def scaled(g, o, scale):
    """Move the group count up to the CPS union, taking the difference out of the others."""
    return scale * g, o - (scale - 1) * g


def vot_2024():
    ecec = json.loads((CACHE / "bls_ecec_2015_2024.json").read_text())
    val = {(s["seriesID"], x["year"], x["period"]): float(x["value"])
           for s in ecec["Results"]["series"] for x in s["data"]}
    ratio = {y: val[("CMU1010000000000D", y, "Q02")] / val[("CMU1020000000000D", y, "Q02")] for y in ("2015", "2024")}
    ratio_tmm = {y: val[("CMU1010000520000D", y, "Q02")] / val[("CMU1020000520000D", y, "Q02")] for y in ("2015", "2024")}
    emp = sum(e for e, _ in TRUCK_DRIVERS_2024.values())
    truck_wage = sum(e * w for e, w in TRUCK_DRIVERS_2024.values()) / emp
    hourly_income = MEDIAN_HH_INCOME_2024 / HOURS_PER_YEAR
    rows = []
    for level in ("low", "central", "high"):
        personal = PERSONAL_SHARE[level] * hourly_income
        business = BUSINESS_SHARE[level] * MEDIAN_WAGE_2024 * ratio["2024"]
        rows.append({"level": level, "personal_local": personal, "business": business,
                     "all_purposes_local": LOCAL_MIX[0] * personal + LOCAL_MIX[1] * business,
                     "truck_driver": BUSINESS_SHARE[level] * truck_wage * ratio_tmm["2024"]})
    # The brief paraphrases personal travel as 50% of the median wage; the guidance (p. 13) uses
    # 50% of hourly median household income. The literal paraphrase is kept as a sensitivity.
    literal = 0.5 * MEDIAN_WAGE_2024
    rows.append({"level": "brief_literal", "personal_local": literal, "business": rows[1]["business"],
                 "all_purposes_local": LOCAL_MIX[0] * literal + LOCAL_MIX[1] * rows[1]["business"],
                 "truck_driver": rows[1]["truck_driver"]})
    table = pd.DataFrame(rows).set_index("level")
    checks = {
        # The guidance's own 2015 values from its 2015 inputs (table 4: 13.60, 25.40, 14.10; truck 27.20).
        "reproduce_2015_personal": 0.5 * 56_516 / HOURS_PER_YEAR,
        "reproduce_2015_business": 17.40 * ratio["2015"],
        "reproduce_2015_all_purposes": 0.954 * 0.5 * 56_516 / HOURS_PER_YEAR + 0.046 * 17.40 * ratio["2015"],
        "reproduce_2015_truck_driver": 17.71 * ratio_tmm["2015"],
        "ecec_ratio_2015q2_all": ratio["2015"], "ecec_ratio_2015q2_transport": ratio_tmm["2015"],
        "ecec_ratio_2024q2_all": ratio["2024"], "ecec_ratio_2024q2_transport": ratio_tmm["2024"],
        "truck_driver_median_wage_2024": truck_wage,
    }
    return table, checks


# ----------------------------------------------------------------------------- exposure

def build_exposure(u, ua, hours, inp, scale):
    """Per UMR urban area: group population share s, group share of vehicle traffic phi, levels."""
    e = u.merge(ua.add_prefix("acs_"), left_on="ua", right_index=True, how="left")
    e["in_scope"] = e["match"].isin(["exact", "first_city", "any_city", "override"])
    g_pop, o_pop = scaled(e.acs_group_persons, e.acs_other_persons, scale)
    e["s"] = g_pop / (g_pop + o_pop)
    g_vm, o_vm = scaled(e.acs_group_vehicle_minutes, e.acs_other_vehicle_minutes, scale)
    e["c_commute"] = g_vm / (g_vm + o_vm)
    odds = e.c_commute / (1 - e.c_commute) * inp["rho"]
    e["phi_commute_route"] = odds / (1 + odds)
    odds_pop = e.s / (1 - e.s) * inp["r_all"]
    e["phi_population_route"] = odds_pop / (1 + odds_pop)
    # Levels on the UMR's own area population; the ACS allocation supplies shares only.
    e["q"] = e.pop_k * 1e3 / (e.acs_group_persons + e.acs_other_persons)
    e["persons"] = e.pop_k * 1e3
    e["other_persons"] = e.persons * (1 - e.s)
    e["group_persons"] = e.persons * e.s
    e["other_commuters"] = scaled(e.acs_group_commuters, e.acs_other_commuters, scale)[1] * e.q
    e["other_car_commuters"] = scaled(e.acs_group_car_commuters, e.acs_other_car_commuters, scale)[1] * e.q
    # NHTS urban-area size class; vehicle-occupant hours per person aged 5+.
    size = np.select([e.ua_pop20 < 200_000, e.ua_pop20 < 500_000, e.ua_pop20 < 1_000_000,
                      e["name"].str.startswith(HEAVY_RAIL)], [1, 2, 3, 4], 5)
    e["urbansize"] = size
    h = hours.set_index(["survey", "urbansize", "cut"])["pov_hours_per_person"]
    for year in (2022, 2017):
        e[f"h_other_{year}"] = [h[(year, int(k), "non_hispanic")] for k in size]
    e["passenger_delay_ph"] = (e.delay_kph - e.truck_delay_kph) * 1e3
    e["truck_delay_ph"] = e.truck_delay_kph * 1e3
    e["passenger_fuel_gal"] = (e.fuel_kgal - e.truck_fuel_kgal) * 1e3
    e["truck_fuel_gal"] = e.truck_fuel_kgal * 1e3
    veh_p = e.passenger_delay_ph / UMR_OCC
    veh_t = e.truck_delay_ph / TRUCK_OCC
    e["w_truck"] = veh_t / (veh_p + veh_t)
    return e


# ----------------------------------------------------------------------------- arms

def periods(phi, pi_peak, p_other):
    """Group share of vehicles in weekday peaks and at other times, given the all-day share phi."""
    p_group = min(pi_peak * p_other, 0.999)
    peak = phi * p_group / (phi * p_group + (1 - phi) * p_other)
    off = phi * (1 - p_group) / (phi * (1 - p_group) + (1 - phi) * (1 - p_other))
    return peak, off


def bpr_saving(psi, beta, eta=1.0, marginal=False):
    """Fraction of remaining vehicles' delay removed when traffic falls by 1 - (1 - psi)^eta."""
    psi_eff = 1 - (1 - psi) ** eta
    return beta * psi_eff if marginal else 1 - (1 - psi_eff) ** beta


def arm_a1(e, phi, tau, beta, occ, pi_peak, p_other, vot, eta=1.0, marginal=False, umr_values=False):
    """BPR removal on UMR delay. Returns per-area others' savings (hours and dollars)."""
    phi_pk, phi_off = periods(phi, pi_peak, p_other)
    res = {"pass_ph": 0.0, "truck_ph": 0.0, "fuel_usd": 0.0}
    for period, weight, ph in (("peak", DELTA, phi_pk), ("off", 1 - DELTA, phi_off)):
        psi = (1 - e.w_truck) * ph + e.w_truck * tau
        f = bpr_saving(psi, beta, eta, marginal)
        others_person_share = (1 - ph) / (1 - ph + ph * occ)
        res[f"pass_ph_{period}"] = weight * e.passenger_delay_ph * others_person_share * f
        res["pass_ph"] = res["pass_ph"] + res[f"pass_ph_{period}"]
        res["truck_ph"] = res["truck_ph"] + weight * e.truck_delay_ph * (1 - tau) * f
        res["fuel_usd"] = res["fuel_usd"] + weight * f * (
            e.passenger_fuel_gal * (1 - ph) * e.gas_price + e.truck_fuel_gal * (1 - tau) * e.diesel_price)
    if umr_values:
        res["time_usd"] = res["pass_ph"] * UMR_VOT + res["truck_ph"] / TRUCK_OCC * UMR_CVOT
    else:
        res["time_usd"] = res["pass_ph"] * vot["all_purposes_local"] + res["truck_ph"] * vot["truck_driver"]
    res["usd"] = res["time_usd"] + res["fuel_usd"]
    return res


def others_hours(e, year):
    """Other residents' annual vehicle-occupant hours (aged 5+), NHTS hours per person by size class."""
    return e.other_persons * (1 - UNDER5_SHARE) * e[f"h_other_{year}"]


def delay_share(e, year, r_hours):
    """UMR passenger delay as a share of all residents' vehicle-occupant hours."""
    total = (e.other_persons + e.group_persons * r_hours) * (1 - UNDER5_SHARE) * e[f"h_other_{year}"]
    return (e.passenger_delay_ph / total).clip(upper=0.6)


def surplus_fraction(log_c0, sigma):
    """Others' gain as a share of their current travel time when the time cost falls to C0."""
    if sigma == 1:
        return -log_c0
    return (1 - np.exp((1 - sigma) * log_c0)) / (1 - sigma)


def time_cost_arm(e, log_c0, sigma, tau, phi, vot, year, r_hours):
    """Dollar value of a proportional fall in the time cost of travel (arms A2 and B).

    The fall is capped at the delay share of travel time: without the group, travel cannot become
    faster than free flow. Large group shares (El Paso 0.80, Riverside 0.54) hit the cap under the
    city-size elasticities, whose cross-city variation also carries built-environment differences.
    """
    g_raw = surplus_fraction(log_c0, sigma)
    d = delay_share(e, year, r_hours)
    g = np.minimum(g_raw, d)
    res = {"pass_ph": others_hours(e, year) * g, "capped": g_raw > d,
           "uncapped_pass_ph": others_hours(e, year) * g_raw}
    # Trucks and excess fuel: delay is the share d of travel time, so a fall g in the time cost of
    # travel removes g / d of their delay.
    res["truck_ph"] = e.truck_delay_ph * (1 - tau) * g / d
    res["fuel_usd"] = (e.passenger_fuel_gal * (1 - phi) * e.gas_price
                       + e.truck_fuel_gal * (1 - tau) * e.diesel_price) * g / d
    res["time_usd"] = res["pass_ph"] * vot["all_purposes_local"] + res["truck_ph"] * vot["truck_driver"]
    res["usd"] = res["time_usd"] + res["fuel_usd"]
    return res


def supply_exponent(theta, sigma):
    """Elasticity of the equilibrium time cost with respect to the group's traffic, lanes fixed (A2)."""
    k = theta / (1 - theta)
    return k / (1 + k * sigma)


def arm_a2(e, phi, tau, theta, sigma, vot, year, r_hours):
    psi = (1 - e.w_truck) * phi + e.w_truck * tau
    return time_cost_arm(e, supply_exponent(theta, sigma) * np.log1p(-psi), sigma, tau, phi, vot, year, r_hours)


def arm_pop(e, share, elasticity, sigma, tau, phi, vot, year, r_hours):
    """Population elasticity of the time cost of travel, applied to the group's share (arms B)."""
    return time_cost_arm(e, elasticity * np.log1p(-share), sigma, tau, phi, vot, year, r_hours)


def proportional_elasticity(label, sigma):
    """Elasticity of the time cost with respect to population when capacity grows with it (B3)."""
    if label in DECREASING_RETURNS:
        a, theta = DECREASING_RETURNS[label]
        supply = (theta - a) / (1 - theta)
    elif label in COST_BASIS:
        theta = THETA["central"]
        supply = COST_BASIS[label] / (1 - theta)
    else:
        raise KeyError(label)
    return supply / (1 + theta / (1 - theta) * sigma)


# ----------------------------------------------------------------------------- driver

def umr_convention_hours(res, e):
    """UMR Eq. A-4 per other auto commuter: peak savings over car commuters, the rest over residents."""
    return res["pass_ph_peak"] / e.other_car_commuters + res["pass_ph_off"] / e.other_persons


def summarise(res, e, mask):
    usd, hours = res["usd"][mask].sum(), res["pass_ph"][mask].sum()
    extra = {}
    if "capped" in res:
        extra["areas_at_free_flow_cap"] = int(res["capped"][mask].sum())
        extra["uncapped_others_passenger_hours_m"] = float(res["uncapped_pass_ph"][mask].sum() / 1e6)
    if "pass_ph_peak" in res:
        per = umr_convention_hours(res, e)[mask]
        extra["umr_eq_a4_hours_per_other_car_commuter"] = float((per * e.other_car_commuters[mask]).sum()
                                                                / e.other_car_commuters[mask].sum())
    return {**extra, "others_passenger_hours_m": float(hours / 1e6),
            "others_truck_person_hours_m": float(res["truck_ph"][mask].sum() / 1e6),
            "time_bn": float(res["time_usd"][mask].sum() / 1e9),
            "fuel_bn": float(res["fuel_usd"][mask].sum() / 1e9),
            "total_bn": float(usd / 1e9),
            "usd_per_other_commuter": float(usd / e.other_commuters[mask].sum()),
            "hours_per_other_commuter": float(hours / e.other_commuters[mask].sum()),
            "usd_per_other_car_commuter": float(usd / e.other_car_commuters[mask].sum()),
            "usd_per_other_resident": float(usd / e.other_persons[mask].sum())}


def grid(factors):
    """Full factorial over {factor: {label: value}}; yields (labels, values, is_central)."""
    names = list(factors)
    for combo in itertools.product(*(factors[n].items() for n in names)):
        labels = {n: lab for n, (lab, _) in zip(names, combo)}
        values = {n: val for n, (_, val) in zip(names, combo)}
        yield labels, values


def main():
    DERIVED.mkdir(exist_ok=True)
    u, summary = load_umr()
    control = positive_control(u, summary)
    (DERIVED / "umr_positive_control.json").write_text(json.dumps(control, indent=2, default=float))
    if not control["passed"]:
        raise SystemExit("[POSITIVE CONTROL FAILED] UMR totals not reproduced")

    checks_pums = json.loads((DERIVED / "pums_commute_checks.json").read_text())
    scale = TARGET / checks_pums["group_persons_acs"]
    wide = load_cells()
    ua, xw = ua_areas(wide)
    u = match_umr(u, xw)
    rat = pd.read_csv(DERIVED / "nhts_ratios.csv").set_index(["survey", "cut"])
    hours = pd.read_csv(DERIVED / "nhts_hours_by_urbansize.csv")
    by = pd.read_csv(DERIVED / "nhts_by_origin.csv").set_index(["survey", "cut"])
    vot, vot_checks = vot_2024()
    vot.to_csv(DERIVED / "vot_2024.csv")

    # NHTS inputs; central is the 2017 southwestern cut (CA, TX, AZ, NM), the closest proxy for
    # the Mexican-origin group among the files that identify Hispanic origin but not Mexican.
    def nhts_set(r):
        return dict(rho=r.rho_all_over_commute_H_vs_N, r_all=r.r_all_driver_vmt_per_person_H_vs_N,
                    occ=r.occupancy_ratio_H_vs_N, pi=r.peak_share_H / r.peak_share_N,
                    r_hours=r.r_pov_hours_per_person_H_vs_N)
    nhts = {"2017 southwest": nhts_set(rat.loc[(2017, "southwest")]),
            "2022 national": nhts_set(rat.loc[(2022, "national")]),
            "2017 national": nhts_set(rat.loc[(2017, "national")])}
    p_other = float(by.loc[(2022, "non_hispanic"), "peak_share_of_driver_vmt"])
    nat = pd.read_csv(DERIVED / "pums_commute_national.csv").set_index(["group", "item"])["estimate"]
    acs_pi = float(nat[("group", "peak_share_of_vehicles")] / nat[("other", "peak_share_of_vehicles")])
    income_share = float(scale * nat[("group_share", "personal_income")])
    pop_share = TARGET / RESIDENTS
    tau = {"low": income_share, "central": (income_share + pop_share) / 2, "high": pop_share}
    vots = {lv: vot.loc[lv] for lv in ("low", "central", "high")}
    literal = vot.loc["brief_literal"]

    exposures = {k: build_exposure(u, ua, hours, inp, scale) for k, inp in nhts.items()}
    e = exposures["2017 southwest"]
    scope = e["in_scope"].to_numpy()
    e.to_csv(DERIVED / "ua_exposure.csv", index=False)

    # Metro tabulation on the housing lane's CBSA route (descriptive, the brief's metro geography).
    cb, titles = cbsa_areas(wide)
    cb = cb.copy()
    cb["title"] = cb.index.map(titles)
    for item in ("persons", "commuters", "car_commuters", "vehicles", "vehicle_minutes", "vehicles_peak",
                 "carpooled", "transit_commuters", "means_worked_from_home"):
        cb[f"group_share_{item}"] = cb[f"group_{item}"] / (cb[f"group_{item}"] + cb[f"other_{item}"])
    for g in ("group", "other"):
        cb[f"{g}_mean_one_way_minutes"] = cb[f"{g}_commuter_minutes"] / cb[f"{g}_commuters"]
        cb[f"{g}_peak_share_of_vehicles"] = cb[f"{g}_vehicles_peak"] / cb[f"{g}_vehicles"]
        cb[f"{g}_vehicles_per_car_commuter"] = cb[f"{g}_vehicles"] / cb[f"{g}_car_commuters"]
    cb["group_share_persons_scaled"] = scale * cb["group_share_persons"]
    cb.sort_values("other_commuters", ascending=False).to_csv(DERIVED / "cbsa_commute.csv")

    rows, central = [], {}

    def record(approach, labels, res, ex, is_central=False, key=None, note=""):
        rows.append({"approach": approach, **{f"f_{k}": v for k, v in labels.items()}, "note": note,
                     "is_central": is_central, **summarise(res, ex, scope)})
        if key:
            central[key] = (res, ex)

    national_uniform = {k: float((ex.phi_commute_route * ex.passenger_delay_ph)[scope].sum()
                                 / ex.passenger_delay_ph[scope].sum()) for k, ex in exposures.items()}

    # A1: BPR on UMR delay, full factorial.
    a1 = {"beta": BETA, "vot": vots, "tau": tau, "nhts": nhts, "pi_source": {"nhts": None, "acs": acs_pi},
          "fill_in": FILL_IN}
    for lab, val in grid(a1):
        ex = exposures[lab["nhts"]]
        pi = val["nhts"]["pi"] if lab["pi_source"] == "nhts" else acs_pi
        res = arm_a1(ex, ex.phi_commute_route, val["tau"], val["beta"], val["nhts"]["occ"], pi, p_other,
                     val["vot"], eta=val["fill_in"])
        approach = "A1 BPR, trips fixed" if lab["fill_in"] == "trips fixed" else "A1 BPR, DT fill-in"
        is_c = (lab["beta"] == "central" and lab["vot"] == "central" and lab["tau"] == "central"
                and lab["nhts"] == "2017 southwest" and lab["pi_source"] == "nhts"
                and lab["fill_in"] in ("trips fixed", "DT 0.44"))
        record(approach, lab, res, ex, is_c, key=("A1" if lab["fill_in"] == "trips fixed" else "A1 fill-in") if is_c else None)
    c1 = dict(tau=tau["central"], beta=BETA["central"], occ=nhts["2017 southwest"]["occ"],
              pi_peak=nhts["2017 southwest"]["pi"], p_other=p_other, vot=vots["central"])
    one_at_a_time = [
        ("marginal beta * psi, not integrated", dict(marginal=True), e.phi_commute_route),
        ("UMR's own values of time ($24.01 person, $80.16 truck)", dict(umr_values=True), e.phi_commute_route),
        ("phi from population share x NHTS VMT ratio", {}, e.phi_population_route),
        ("national-uniform traffic share", {}, pd.Series(national_uniform["2017 southwest"], index=e.index)),
    ]
    for note, kw, phi in one_at_a_time:
        record("A1 BPR, trips fixed", {"variant": "one-at-a-time"}, arm_a1(e, phi, **c1, **kw), e, note=note)
    # Network-level beta: the UMR's own 2019-2021 national swing (an upper bound for a uniform cut,
    # since peak traffic fell and returned more than daily traffic), and the beta at which BPR on the
    # UMR delay base has CDT's slope k (theta 0.13) = beta x delay share of travel time.
    panel = pd.read_csv(DERIVED / "umr_panel_elasticity.csv")
    swing = panel[(panel.dependent == "pdelay") & panel.years.isin(["2019-2020", "2020-2021"])]
    d_share = float(e.passenger_delay_ph[scope].sum() / (e.passenger_delay_ph / delay_share(e, 2022, nhts["2017 southwest"]["r_hours"]))[scope].sum())
    network_beta = {"UMR 2019-2021 national swing": float(swing.implied_beta.mean()),
                    "CDT-equivalent k / delay share": supply_exponent(THETA["central"], 0.0) / d_share}
    for label, b in network_beta.items():
        for fill_label in ("trips fixed", "DT 0.44"):
            approach = "A1 BPR, trips fixed" if fill_label == "trips fixed" else "A1 BPR, DT fill-in"
            record(approach, {"variant": "one-at-a-time", "fill_in": fill_label},
                   arm_a1(e, e.phi_commute_route, **{**c1, "beta": b}, eta=FILL_IN[fill_label]), e,
                   note=f"network beta {b:.2f} ({label})")

    # A2: CDT supply curve with lanes fixed.
    a2 = {"theta": THETA, "sigma": SIGMA, "vot": vots, "tau": tau, "nhts": nhts, "hours": {"2022": 2022, "2017": 2017}}
    for lab, val in grid(a2):
        ex = exposures[lab["nhts"]]
        res = arm_a2(ex, ex.phi_commute_route, val["tau"], val["theta"], val["sigma"], val["vot"], val["hours"],
                     val["nhts"]["r_hours"])
        is_c = (lab["theta"] == "central" and lab["sigma"] == "16" and lab["vot"] == "central" and lab["tau"] == "central"
                and lab["nhts"] == "2017 southwest" and lab["hours"] == "2022")
        record("A2 CDT supply curve, lanes fixed", lab, res, ex, is_c, key="A2" if is_c else None)
    r_h = nhts["2017 southwest"]["r_hours"]
    record("A2 CDT supply curve, lanes fixed", {"variant": "one-at-a-time"},
           arm_a2(e, pd.Series(national_uniform["2017 southwest"], index=e.index), tau["central"], THETA["central"],
                  SIGMA["16"], vots["central"], 2022, r_h), e, note="national-uniform traffic share")

    # B1 and B2: population elasticities with lanes fixed and as they vary across metros.
    for approach, elasticities, key in (("B1 population elasticity, lanes fixed", POP_FIXED_LANES, "B1"),
                                        ("B2 population elasticity, lanes as across metros",
                                         {"central": POP_UNCONDITIONAL}, "B2")):
        fb = {"elasticity": elasticities, "share": {"population": "s", "traffic": "phi"}, "vot": vots, "tau": tau,
              "nhts": nhts, "hours": {"2022": 2022, "2017": 2017}}
        for lab, val in grid(fb):
            ex = exposures[lab["nhts"]]
            share = ex.s if val["share"] == "s" else ex.phi_commute_route
            res = arm_pop(ex, share, val["elasticity"], 0.0, val["tau"], ex.phi_commute_route, val["vot"], val["hours"],
                          val["nhts"]["r_hours"])
            is_c = (lab["elasticity"] == "central" and lab["share"] == "population" and lab["vot"] == "central"
                    and lab["tau"] == "central" and lab["nhts"] == "2017 southwest" and lab["hours"] == "2022")
            record(approach, lab, res, ex, is_c, key=key if is_c else None)
        record(approach, {"variant": "one-at-a-time"},
               arm_pop(e, pd.Series(pop_share, index=e.index), elasticities["central"], 0.0, tau["central"],
                       e.phi_commute_route, vots["central"], 2022, r_h), e, note="national-uniform population share")

    # B3: proportional capacity residual.
    residuals = {f"{lab}, sigma {sig:g}": proportional_elasticity(lab, sig)
                 for lab in list(DECREASING_RETURNS) + list(COST_BASIS) for sig in (0.0, 16.0)}
    residuals["T10 col 6: 0.12 - 0.066 lanes"] = POP_FIXED_LANES["central"] - LANES_COEF_T10
    fb3 = {"residual": residuals, "vot": vots, "tau": tau, "nhts": nhts, "hours": {"2022": 2022, "2017": 2017}}
    for lab, val in grid(fb3):
        ex = exposures[lab["nhts"]]
        res = arm_pop(ex, ex.s, val["residual"], 0.0, val["tau"], ex.phi_commute_route, val["vot"], val["hours"],
                      val["nhts"]["r_hours"])
        is_c = (lab["residual"] == "T10 col 6: 0.12 - 0.066 lanes" and lab["vot"] == "central" and lab["tau"] == "central"
                and lab["nhts"] == "2017 southwest" and lab["hours"] == "2022")
        record("B3 proportional capacity, residual", {**lab, "elasticity_value": round(val["residual"], 5)},
               res, ex, is_c, key="B3" if is_c else None)

    # Proportional reference as the account keys it: economic affairs responds on the resources key,
    # so capacity shrinks by the group's resource share while population falls by s.
    line = next(x for x in json.loads(ACCOUNT_MODEL.read_text())["spending"]["lines"]
                if x["id"] == "economic_affairs_services")
    key = line["keys"][line["preferred_key"]]["personal"]
    log_c0 = POP_FIXED_LANES["central"] * np.log1p(-e.s) - LANES_COEF_T10 * np.log1p(-key["share"])
    record("B3 proportional capacity, residual", {"variant": "one-at-a-time"},
           time_cost_arm(e, log_c0, 0.0, tau["central"], e.phi_commute_route, vots["central"], 2022, r_h), e,
           note=f"T10 col 6, lanes shrink by the account's {line['preferred_key']} key {key['share']:.4f} "
                f"(${key['target_bn']:.2f}bn of ${line['national_bn']:.1f}bn)")

    note = "personal time at 50% of the median wage (brief's wording), not of household income"
    record("A1 BPR, trips fixed", {"variant": "one-at-a-time"}, arm_a1(e, e.phi_commute_route, **{**c1, "vot": literal}),
           e, note=note)
    record("A1 BPR, DT fill-in", {"variant": "one-at-a-time"},
           arm_a1(e, e.phi_commute_route, **{**c1, "vot": literal}, eta=FILL_IN["DT 0.44"]), e, note=note)
    record("A2 CDT supply curve, lanes fixed", {"variant": "one-at-a-time"},
           arm_a2(e, e.phi_commute_route, tau["central"], THETA["central"], SIGMA["16"], literal, 2022, r_h), e, note=note)
    record("B1 population elasticity, lanes fixed", {"variant": "one-at-a-time"},
           arm_pop(e, e.s, POP_FIXED_LANES["central"], 0.0, tau["central"], e.phi_commute_route, literal, 2022, r_h),
           e, note=note)

    table = pd.DataFrame(rows)
    table.to_csv(DERIVED / "arms_grid.csv", index=False)

    summ = []
    for approach, sub in table.groupby("approach", sort=False):
        c = sub[sub.is_central]
        fact = sub[sub["f_variant"].isna()] if "f_variant" in sub else sub
        for _, crow in c.iterrows():
            summ.append({"approach": approach, "central_label": crow.get("f_fill_in", ""),
                         "central_bn": crow.total_bn, "factorial_min_bn": fact.total_bn.min(),
                         "factorial_max_bn": fact.total_bn.max(), "min_bn": sub.total_bn.min(), "max_bn": sub.total_bn.max(),
                         "central_time_bn": crow.time_bn, "central_fuel_bn": crow.fuel_bn,
                         "central_others_passenger_hours_m": crow.others_passenger_hours_m,
                         "central_hours_per_other_commuter": crow.hours_per_other_commuter,
                         "central_usd_per_other_commuter": crow.usd_per_other_commuter,
                         "central_usd_per_other_resident": crow.usd_per_other_resident, "n_rows": len(sub)})
    summary_table = pd.DataFrame(summ)
    summary_table.to_csv(DERIVED / "arms_summary.csv", index=False)
    fill = table[table.approach.eq("A1 BPR, DT fill-in") & table.f_beta.eq("central") & table.f_vot.eq("central")
                 & table.f_tau.eq("central") & table.f_nhts.eq("2017 southwest") & table.f_pi_source.eq("nhts")]

    # Distribution across metros under each central arm.
    dist = e.loc[scope, ["name", "ua", "ua_name", "match", "pop_k", "s", "phi_commute_route", "passenger_delay_ph",
                         "truck_delay_ph", "delay_per_auto_commuter", "cost_musd", "other_commuters", "other_persons"]].copy()
    for key, (res, ex) in central.items():
        label = key.replace(" ", "_")
        dist[f"{label}_bn"] = res["usd"][scope] / 1e9
        dist[f"{label}_hours_per_other_commuter"] = res["pass_ph"][scope] / ex.other_commuters[scope]
        dist[f"{label}_usd_per_other_commuter"] = res["usd"][scope] / ex.other_commuters[scope]
        if "pass_ph_peak" in res:
            dist[f"{label}_umr_eq_a4_hours"] = umr_convention_hours(res, ex)[scope]
    dist = dist.sort_values("A1_bn", ascending=False)
    for key in central:
        label = key.replace(" ", "_")
        dist[f"{label}_cumulative_share"] = dist[f"{label}_bn"].cumsum() / dist[f"{label}_bn"].sum()
    dist.to_csv(DERIVED / "metro_distribution.csv", index=False)

    c = nhts["2017 southwest"]
    params = [
        ("scale_cps_over_acs", scale, "CPS union 40.896574m / ACS HISP=02 or POBP=303 persons [DATA]"),
        ("delta_peak_share_of_delay", DELTA, "UMR 2025 Exhibit 15 weekday share x mean of Exhibits 10 and 13 peak shares [DATA, chart read]"),
        ("p_other_peak_share", p_other, "NHTS 2022 non-Hispanic weekday peak share of driver VMT [CALCULATION]"),
        ("rho_central", c["rho"], "NHTS 2017 southwest, Hispanic vs non-Hispanic all-purpose/commute driver VMT [CALCULATION]"),
        ("r_all_central", c["r_all"], "NHTS 2017 southwest, Hispanic / non-Hispanic driver VMT per person [CALCULATION]"),
        ("r_hours_central", c["r_hours"], "NHTS 2017 southwest, Hispanic / non-Hispanic vehicle-occupant hours per person [CALCULATION]"),
        ("occupancy_ratio_central", c["occ"], "NHTS 2017 southwest, POV person-miles per driver mile, H / N [CALCULATION]"),
        ("pi_peak_central", c["pi"], "NHTS 2017 southwest, peak share of driver VMT, H / N [CALCULATION]"),
        ("pi_peak_acs", acs_pi, "ACS 2024 share of commute vehicles departing 6-10 a.m., group / other [CALCULATION]"),
        ("tau_low", tau["low"], "group share of ACS personal income x CPS scale [CALCULATION]"),
        ("tau_central", tau["central"], "midpoint of low and high [INFERENCE]"),
        ("tau_high", tau["high"], "group share of residents [DATA]"),
        ("beta", json.dumps(BETA), "NCHRP 716 average MPO curves: arterials 3.001, freeways 5.883; original BPR 4 [SOURCE]"),
        ("fill_in_eta", json.dumps(FILL_IN), "Duranton-Turner 2009 table 2 panel A, ln pop at fixed lanes, cols 2, 3, 5 [SOURCE]"),
        ("theta", json.dumps(THETA), "CDT table 5 col 6 = 0.13 (SE 0.035); table 8 range 0.07-0.19 [SOURCE]"),
        ("sigma", json.dumps(SIGMA), "CDT section 7 and table 8, from Duranton-Turner (2009) demand estimate 16; range 8-32 [SOURCE]"),
        ("pop_elasticity_fixed_lanes", json.dumps(POP_FIXED_LANES), "CDT table 10 col 6, -0.12 (SE 0.035), +/- 1 SE [SOURCE]"),
        ("pop_elasticity_unconditional", POP_UNCONDITIONAL, "CDT section 6 [SOURCE]"),
        ("proportional_residuals", json.dumps({k: round(v, 5) for k, v in residuals.items()}),
         "CDT table 5 columns, PMSA text, footnote 19; table 10 col 6 [CALCULATION]"),
        ("under5_share", UNDER5_SHARE, "ACS 2024 B01001 [DATA]"),
        ("vot_all_purposes", json.dumps({k: round(float(v["all_purposes_local"]), 2) for k, v in vots.items()}),
         "USDOT 2016 rev. 2 method, 2024 inputs [CALCULATION]"),
        ("vot_truck_driver", json.dumps({k: round(float(v["truck_driver"]), 2) for k, v in vots.items()}),
         "USDOT 2016 rev. 2 method, 2024 inputs [CALCULATION]"),
    ]
    pd.DataFrame(params, columns=["parameter", "value", "source"]).to_csv(DERIVED / "parameters.csv", index=False)

    w = e.passenger_delay_ph.where(scope, 0)
    d = delay_share(e, 2022, r_h)
    g_vm, o_vm = scaled(nat[("group", "vehicle_minutes")], nat[("other", "vehicle_minutes")], scale)
    c_nat = g_vm / (g_vm + o_vm)
    odds_c, odds_s = c_nat / (1 - c_nat) * c["rho"], pop_share / (1 - pop_share) * c["r_all"]
    checks = {
        "national_commute_vehicle_minute_share_scaled": float(c_nat),
        "national_phi_commute_route": float(odds_c / (1 + odds_c)),
        "national_phi_population_route": float(odds_s / (1 + odds_s)),
        "umr_areas": int(len(e)), "in_scope_areas": int(scope.sum()),
        "match_counts": e["match"].value_counts().to_dict(),
        "umr_areas_sharing_a_census_ua": e[scope].groupby("ua")["name"].apply(list)[lambda x: x.map(len) > 1].to_dict(),
        "delay_share_in_scope": float(e.delay_kph[scope].sum() / e.delay_kph.sum()),
        "delay_share_puerto_rico": float(e.delay_kph[e["match"].eq("puerto_rico")].sum() / e.delay_kph.sum()),
        "delay_share_unmatched": float(e.delay_kph[e["match"].eq("unmatched")].sum() / e.delay_kph.sum()),
        "umr_pop_over_acs_allocation_delay_weighted": float((e.q * w).sum() / w.sum()),
        "umr_pop_over_acs_allocation_quartiles": e.q[scope].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).round(3).to_dict(),
        "group_share_persons_delay_weighted": float((e.s * w).sum() / w.sum()),
        "phi_delay_weighted": float((e.phi_commute_route * w).sum() / w.sum()),
        "phi_population_route_delay_weighted": float((e.phi_population_route * w).sum() / w.sum()),
        "c_commute_delay_weighted": float((e.c_commute * w).sum() / w.sum()),
        "national_uniform_phi": national_uniform,
        "group_share_persons_in_scope": float(e.group_persons[scope].sum() / e.persons[scope].sum()),
        "in_scope_residents_m": float(e.persons[scope].sum() / 1e6),
        "others_in_scope_m": float(e.other_persons[scope].sum() / 1e6),
        "others_commuters_in_scope_m": float(e.other_commuters[scope].sum() / 1e6),
        "others_car_commuters_in_scope_m": float(e.other_car_commuters[scope].sum() / 1e6),
        "others_vehicle_hours_bn_2022": float(others_hours(e, 2022)[scope].sum() / 1e9),
        "delay_share_of_travel_time_hours_weighted": float(e.passenger_delay_ph[scope].sum()
                                                           / (e.passenger_delay_ph / d)[scope].sum()),
        "delay_share_clipped_areas": int((d[scope] >= 0.6).sum()),
        # Implied elasticity of time per km with respect to traffic: BPR beta x delay share vs CDT k.
        "bpr_implied_time_elasticity": {lv: float(b * e.passenger_delay_ph[scope].sum()
                                                  / (e.passenger_delay_ph / d)[scope].sum()) for lv, b in BETA.items()},
        "cdt_supply_exponent": {f"theta {t}, sigma {s:g}": supply_exponent(t, s) for t in THETA.values() for s in SIGMA.values()},
        "umr_average_cost_share_of_group_bn": float((e.phi_commute_route * e.cost_musd)[scope].sum() / 1e3),
        "vot": vot_checks, "tau": tau, "delta": DELTA, "acs_pi": acs_pi, "p_other": p_other,
        "a1_fill_in_central_rows": fill[["f_fill_in", "total_bn"]].to_dict("records"),
        "network_beta": network_beta, "delay_share_used_for_cdt_equivalent_beta": d_share,
    }
    (DERIVED / "checks.json").write_text(json.dumps(checks, indent=2, default=float))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    pd.set_option("display.max_colwidth", 60)
    print(json.dumps(control, indent=1, default=float))
    print(vot.round(2).to_string())
    print(summary_table.round(3).to_string(index=False))
    print(table[table.note.ne("")][["approach", "note", "total_bn", "usd_per_other_commuter"]].round(2).to_string(index=False))
    print(json.dumps(checks, indent=1, default=float))


if __name__ == "__main__":
    main()
