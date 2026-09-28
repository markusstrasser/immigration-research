"""Air-pollution and CO2 damages that the Mexican-origin union (and, as a comparator, non-Hispanic
Black residents) impose on other US residents through their consumption. 2024 dollars.

Chain for PM2.5 (every input is in PARAMS with its source tag; RESULT.md explains each):
  national deaths from US anthropogenic PM2.5, 2024  = Bekbulat et al. 2019 deaths by CRF
        x emissions trend 2019->2024 (sector-weighted) x baseline deaths 2024/2019
  deaths caused by the group's consumption           = national x Tessum's personal-consumption
        share (83k of 102k) x population share x per-capita caused ratio r
  deaths falling on people outside the group          = caused x (1 - self-share sigma)
        sigma = L x iota + (1 - L) x s x E   (local share L lands at the metro group share iota;
        the rest spreads like consumption-caused exposure, which the group breathes at E x average)
  value                                               = deaths x VSL x morbidity multiplier
Normalized = against a same-size group of average residents, whose self-share is s:
        D x theta x s x [r (1 - sigma) - (1 - s)].
Low/high are the minimum and maximum over the full factorial grid of the discrete arms below.
"""
import itertools
import json
import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "derived"
CK = HERE.parent / "consumption_key_2026_09_24"

# ---------------------------------------------------------------- parameters
POP_ALL = 336_727_803.0            # [DATA: crime_victim_cost_2026_09_23 target_population_cps2025.csv]
GROUPS = {
    "mexican_origin": dict(n=40_896_574.2, n_mexico_born=12_220_781.9, income_pc=29_230),
    "nh_black": dict(n=41_954_494.0, n_mexico_born=0.0, income_pc=35_726),
}
INCOME_PC_ALL = 48_853             # [DATA: black_comparator_rough_2026_09_28 cps_profile.csv]

LN = math.log
D2019 = {                          # US anthropogenic PM2.5 deaths 2019, InMAP-ISRM on EQUATES
    "wu2020_65plus": 52_000.0,     # [SOURCE: Bekbulat et al. 2025 ES&T Lett, "~52,000 (Wu)"]
    "orellano2024": 96_000.0,      # [SOURCE: same, main CRF RR 1.095 per 10 ug/m3]
    "di2017_lt12_adults": 96_000.0 * LN(1.136) / LN(1.095),  # [CALCULATION: Di NEJM 2017 +13.6%/10 below 12]
}
D2019_CHECK_LEPEULE = 139_000.0    # [SOURCE: Bekbulat, "~139,000 (Lepeule)"]; RR 1.14 -> ratio check
SECTOR_2019 = {"electricity": 4_600, "industrial": 18_500, "transportation": 15_700,
               "agriculture": 22_800, "residential": 4_700}   # [SOURCE: Bekbulat ChemRxiv, Nasari CRF]
SECTOR_TREND = {                   # 2019->2024 emission-driven change in exposure [INFERENCE]
    "low": {"electricity": 0.50, "industrial": 0.90, "transportation": 0.75, "agriculture": 1.00, "residential": 0.95},
    "central": {"electricity": 0.60, "industrial": 0.95, "transportation": 0.80, "agriculture": 1.02, "residential": 1.00},
    "high": {"electricity": 0.70, "industrial": 1.00, "transportation": 0.85, "agriculture": 1.05, "residential": 1.02},
}
DEATHS_ALLCAUSE = {2019: 2_854_838, 2024: 3_072_666}  # [TRAINING-DATA 2019; SOURCE NCHS Data Brief 548 for 2024]
THETA_CONSUMPTION = 83 / 102       # [SOURCE: Tessum 2019, personal consumption incl. allocated private investment]
THETA_GOVERNMENT = 8 / 102         # [SOURCE: Tessum 2019]

ARMS = {  # low-damage / central / high-damage settings
    "crf": ["wu2020_65plus", "orellano2024", "di2017_lt12_adults"],
    "trend": ["low", "central", "high"],
    # per-capita caused exposure relative to average; central = Tessum Hispanic 0.69 x CE Mex/Hisp 0.9467
    "r": {"mexican_origin": [0.61, 0.69 * 0.9467, 0.73], "nh_black": [0.72, 0.77, 0.80]},
    # exposure experienced relative to average (Tessum 2015: Hispanic 1.12, Black 1.21)
    "E": {"mexican_origin": [1.20, 1.12, 1.05], "nh_black": [1.27, 1.21, 1.15]},   # ordered by damage to others
    "iota": {"mexican_origin": [0.33, 0.30, 0.27], "nh_black": [0.30, 0.25, 0.20]},
    "L": [0.45, 0.35, 0.25],
    "morbidity": [1.01, 1.03, 1.06],
}
GOV = {"use": {"mexican_origin": [0.9, 1.1, 1.3], "nh_black": [0.9, 1.0, 1.1]}, "response": [0.35, 0.55, 0.80]}
OZONE_RATIO = [0.02, 0.036, 0.15]  # ozone deaths / PM2.5 deaths; Fann 2012 4,700 / 130,000 central [TRAINING-DATA]
VSL_DOT_2024 = 13.7e6              # [DATA: crime_victim_cost_2026_09_23 unit_costs, US DOT 2024]
VSL_EPA_2006 = 7.4e6               # [TRAINING-DATA: EPA Guidelines central VSL, 2006$]

# CO2
SCC_2020USD = {"iwg2021_3pct": 55.0, "epa2023_2pct": 190 + 0.4 * (230 - 190), "epa2023_1p5pct": 340 + 0.4 * (380 - 340)}
US_SHARE = [0.07, 0.11, 0.23]      # IWG 2010 7-23% [TRAINING-DATA]; Nordhaus 10.6%, Ricke ~12% [SOURCE]
CO2 = {
    "w_direct": [0.30, 0.33, 0.36],   # household fuel + electricity + gasoline share of the footprint [INFERENCE]
    "rho_direct": {"mexican_origin": [0.75, 0.80, 0.90], "nh_black": [0.88, 0.93, 0.98]},
    "rho_total": {"mexican_origin": [0.653, 0.706, 0.73], "nh_black": [0.77, 0.802, 0.83]},
    "w_gov": 0.12, "gov_use": [0.9, 1.0, 1.1],
    "phi_origin": [1.0, 0.85, 0.7],   # migrants' counterfactual footprint / Mexico average (low damage first)
    "remit_bn": [15.4, 52.9, 56.4],   # [DATA: consumption_key remittance_flows.csv bea / corridor_net_h2 / corridor_full]
    "remit_kg_per_usd": [0.30, 0.40, 0.45],  # Mexico consumption CO2 per $ of final consumption [INFERENCE]
}


def cpi(year):
    for f in ("bls_cpi_u_2003_2012.json", "bls_cpi_u_2015_2024.json"):
        d = json.load(open(CK / "_cache/sources" / f))
        for s in d["Results"]["series"]:
            for r in s["data"]:
                if r["year"] == str(year) and r["period"] == "M13":
                    return float(r["value"])
    raise KeyError(year)


def owid(country, year, col):
    df = pd.read_csv(HERE / "_cache/owid-co2-data.csv", usecols=["country", "year", col])
    return float(df[(df.country == country) & (df.year == year)][col].iloc[0])


def national_deaths_2024(crf, trend):
    f_emis = sum(SECTOR_2019[k] * SECTOR_TREND[trend][k] for k in SECTOR_2019) / sum(SECTOR_2019.values())
    f_base = DEATHS_ALLCAUSE[2024] / DEATHS_ALLCAUSE[2019]
    return D2019[crf] * f_emis * f_base, f_emis, f_base


def pm_grid(group):
    g = GROUPS[group]
    s = g["n"] / POP_ALL
    rows = []
    for i_crf, i_tr, i_r, i_E, i_io, i_L, i_m in itertools.product(range(3), repeat=7):
        D, _, _ = national_deaths_2024(ARMS["crf"][i_crf], ARMS["trend"][i_tr])
        r = ARMS["r"][group][i_r]
        E, iota, L = ARMS["E"][group][i_E], ARMS["iota"][group][i_io], ARMS["L"][i_L]
        sigma = L * iota + (1 - L) * s * E
        base = D * THETA_CONSUMPTION * s
        rows.append(dict(i_crf=i_crf, i_tr=i_tr, i_r=i_r, i_E=i_E, i_io=i_io, i_L=i_L, i_m=i_m,
                         D=D, sigma=sigma, caused=base * r, others=base * r * (1 - sigma),
                         normalized=base * (r * (1 - sigma) - (1 - s)), morb=ARMS["morbidity"][i_m]))
    return pd.DataFrame(rows), s


def summarize(values, central):
    return float(values.min()), float(central), float(values.max())


def main():
    OUT.mkdir(exist_ok=True)
    cpi06, cpi20, cpi24 = cpi(2006), cpi(2020), cpi(2024)
    vsl_epa = VSL_EPA_2006 * cpi24 / cpi06
    items, params, national = [], [], []

    for crf in ARMS["crf"]:
        for tr in ARMS["trend"]:
            D, fe, fb = national_deaths_2024(crf, tr)
            national.append(dict(crf=crf, trend=tr, deaths_2019=D2019[crf], f_emissions=fe, f_baseline=fb,
                                 deaths_2024=D, consumption_deaths_2024=D * THETA_CONSUMPTION,
                                 damages_dot_vsl_bn=D * VSL_DOT_2024 / 1e9))
    pd.DataFrame(national).to_csv(OUT / "national_deaths.csv", index=False, lineterminator="\n")

    for group, g in GROUPS.items():
        grid, s = pm_grid(group)
        cen = grid[(grid[[c for c in grid.columns if c.startswith("i_")]] == 1).all(axis=1)].iloc[0]
        for measure in ("others", "normalized"):
            vals = grid[measure] * grid.morb * VSL_DOT_2024 / 1e9
            lo, c, hi = summarize(vals, cen[measure] * cen.morb * VSL_DOT_2024 / 1e9)
            items.append(dict(item="pm25_consumption", group=group,
                              measure="absolute" if measure == "others" else "normalized",
                              low_bn=lo, central_bn=c, high_bn=hi, per_member_usd=c * 1e9 / g["n"],
                              deaths_central=cen[measure], sigma_central=cen.sigma, caused_central=cen.caused))
        # EPA VSL alternative, absolute only
        vals = grid.others * grid.morb * vsl_epa / 1e9
        c = cen.others * cen.morb * vsl_epa / 1e9
        items.append(dict(item="pm25_consumption_epa_vsl", group=group, measure="absolute",
                          low_bn=vals.min(), central_bn=c, high_bn=vals.max(), per_member_usd=c * 1e9 / g["n"],
                          deaths_central=cen.others))
        # government-use emissions, removed in proportion to the budgets that respond to removal
        for measure in ("absolute", "normalized"):
            vals = []
            for (Dk, tr), iu, ir, ig in itertools.product([(k, t) for k in ARMS["crf"] for t in ARMS["trend"]],
                                                          range(3), range(3), range(3)):
                D, _, _ = national_deaths_2024(Dk, tr)
                use, resp = GOV["use"][group][iu], GOV["response"][ir]
                sigma = [grid.sigma.max(), cen.sigma, grid.sigma.min()][ig]
                base = D * THETA_GOVERNMENT * s * resp
                v = base * use * (1 - sigma) if measure == "absolute" else base * (use * (1 - sigma) - (1 - s))
                vals.append(v * VSL_DOT_2024 * 1.03 / 1e9)
            Dc, _, _ = national_deaths_2024("orellano2024", "central")
            basec = Dc * THETA_GOVERNMENT * s * GOV["response"][1]
            usec = GOV["use"][group][1]
            vc = basec * usec * (1 - cen.sigma) if measure == "absolute" else basec * (usec * (1 - cen.sigma) - (1 - s))
            c = vc * VSL_DOT_2024 * 1.03 / 1e9
            items.append(dict(item="pm25_government_use", group=group, measure=measure, low_bn=min(vals),
                              central_bn=c, high_bn=max(vals), per_member_usd=c * 1e9 / g["n"], deaths_central=vc))
        # ozone as a ratio to the PM2.5 consumption rows
        for measure in ("absolute", "normalized"):
            pm = [it for it in items if it["item"] == "pm25_consumption" and it["group"] == group
                  and it["measure"] == measure][0]
            combos = [pm["low_bn"] * OZONE_RATIO[0], pm["low_bn"] * OZONE_RATIO[2],
                      pm["high_bn"] * OZONE_RATIO[0], pm["high_bn"] * OZONE_RATIO[2]]
            c = pm["central_bn"] * OZONE_RATIO[1]
            items.append(dict(item="ozone_consumption", group=group, measure=measure, low_bn=min(combos),
                              central_bn=c, high_bn=max(combos), per_member_usd=c * 1e9 / g["n"]))

        # CO2 arm [FRAMING-SENSITIVE]
        fbar = (owid("United States", 2023, "consumption_co2") * owid("United States", 2024, "co2")
                / owid("United States", 2023, "co2") / owid("United States", 2024, "population") * 1e6)  # t per person
        mex_pc = owid("Mexico", 2023, "consumption_co2_per_capita")
        income_share = g["n"] * g["income_pc"] / (POP_ALL * INCOME_PC_ALL)
        res = {"absolute": [], "normalized": []}
        central = {}
        for i in itertools.product(range(3), repeat=9):
            wd, rd, rt, gu = CO2["w_direct"][i[0]], CO2["rho_direct"][group][i[1]], CO2["rho_total"][group][i[2]], CO2["gov_use"][i[3]]
            r_co2 = wd * rd + CO2["w_gov"] * gu + (1 - wd - CO2["w_gov"]) * rt
            origin = g["n_mexico_born"] * mex_pc * CO2["phi_origin"][i[4]] / 1e6            # Mt
            remit = (CO2["remit_bn"][i[5]] * CO2["remit_kg_per_usd"][i[5]] if group == "mexican_origin" else 0.0)  # Mt
            scc_key = list(SCC_2020USD)[i[6]]
            scc = SCC_2020USD[scc_key] * cpi24 / cpi20
            ush = US_SHARE[i[7]]
            oth = [1 - s, 1 - income_share][min(i[8], 1)]
            gross = g["n"] * fbar * r_co2 / 1e6                                                # Mt
            net_abs = gross - origin + remit
            net_norm = g["n"] * fbar * (r_co2 - 1) / 1e6 - origin + remit
            for m, net in (("absolute", net_abs), ("normalized", net_norm)):
                v = net * 1e6 * scc * ush * oth / 1e9
                res[m].append(v)
                if all(x == 1 for x in i[:8]) and i[8] == 1:
                    central[m] = (v, net, gross, r_co2, origin, remit, scc)
        for m in ("absolute", "normalized"):
            v, net, gross, r_co2, origin, remit, scc = central[m]
            items.append(dict(item="co2_net_addition_us_damages", group=group, measure=m, low_bn=min(res[m]),
                              central_bn=v, high_bn=max(res[m]), per_member_usd=v * 1e9 / g["n"],
                              net_mt_central=net, gross_mt_central=gross, r_co2_central=r_co2,
                              origin_mt_central=origin, remit_mt_central=remit, scc_2024usd_central=scc,
                              global_damages_bn_central=net * scc / 1e3))
        params.append(dict(group=group, pop_share=s, us_consumption_co2_t_per_capita_2024=fbar,
                           mexico_consumption_co2_t_per_capita_2023=mex_pc, income_share=income_share,
                           sigma_central=cen.sigma, sigma_min=grid.sigma.min(), sigma_max=grid.sigma.max(),
                           vsl_epa_2024usd=vsl_epa, cpi_2006=cpi06, cpi_2020=cpi20, cpi_2024=cpi24,
                           di_2019_adults=D2019["di2017_lt12_adults"],
                           di_2019_65plus=D2019["di2017_lt12_adults"] * (628_278 + 822_860 + 890_204) / 3_072_039,
                           lepeule_ratio_check=96_000 * LN(1.14) / LN(1.095) / D2019_CHECK_LEPEULE))

    df = pd.DataFrame(items)
    df.to_csv(OUT / "items_detail.csv", index=False, lineterminator="\n", float_format="%.6g")
    notes = {
        "pm25_consumption": (
            "contested (modelled): death totals and CRF contested; CE, ACS, NCHS inputs measured; 2019-2024 trend and local share assumed",
            "none in the fiscal account (it charges the group's own health use, not harm to others); congestion prices time and private fuel only; road-crash lane separate",
            "Bekbulat 2019 US-anthropogenic deaths by CRF x sector-weighted 2019-2024 emissions trend x NCHS deaths 2024/2019 x Tessum consumption share 83/102 x population share x per-capita caused ratio r (Tessum Hispanic 0.69 x CE 2024 Mexican/Hispanic spending 0.947) x (1 - self-share sigma) x DOT VSL $13.7m x morbidity 1.03; low/high = min/max of the full grid (Wu 65+ CRF ... Di <12 ug/m3 extended to adults)"),
        "pm25_consumption_epa_vsl": (
            "contested (modelled)", "alternative valuation of pm25_consumption; never add both",
            "as pm25_consumption with EPA's $7.4m (2006$) VSL x CPI-U = $11.5m"),
        "pm25_government_use": (
            "speculative (modelled; share of government emissions removed with the group assumed)",
            "fiscal account charges the dollar cost of these services, not their emissions; add only where the account lets those budgets respond",
            "Tessum government end-use share 8/102 x population share x use relative to average x responding share (0.35-0.80) x (1 - sigma) x DOT VSL x 1.03"),
        "ozone_consumption": (
            "speculative: ozone-to-PM2.5 death ratio from Fann et al. 2012 [TRAINING-DATA], long-term CRFs for the high arm",
            "none; separate pollutant, same consumption attribution as pm25_consumption",
            "pm25_consumption x ozone/PM2.5 deaths ratio 0.02 / 0.036 / 0.15"),
        "co2_net_addition_us_damages": (
            "[FRAMING-SENSITIVE] contested: SCC, US damage share and origin counterfactual are model or assumption driven",
            "none with the account or other social items; keep outside the social total as a flagged arm",
            "US consumption-based CO2 15.68 t/person (OWID/GCB 2023 scaled to 2024) x footprint ratio (direct energy, indirect spending, government) - Mexico-born origin footprint (Mexico 4.355 t x 0.7-1.0) + remittance-funded Mexican consumption; x EPA 2023 SC-CO2 for 2024 (2%, $250 in 2024$; IWG 3% $67 low; EPA 1.5% $431 high) x US share 7/11/23% x others' income share"),
    }
    base_item = df.item.map(lambda x: x)
    df["evidence_level"] = base_item.map(lambda x: notes[x][0])
    df["double_count_with"] = base_item.map(lambda x: notes[x][1])
    df["method_note"] = base_item.map(lambda x: notes[x][2])
    norm_note = (" Normalized: against a same-size group of average residents, whose self-share is its population"
                 " share: D x theta x s x [r(1 - sigma) - (1 - s)].")
    df.loc[df.measure == "normalized", "method_note"] += norm_note
    cols = ["item", "group", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd",
            "evidence_level", "double_count_with", "method_note"]
    assert ((df.low_bn <= df.central_bn + 1e-9) & (df.central_bn <= df.high_bn + 1e-9)).all(), "range order"
    df[cols].to_csv(OUT / "items.csv", index=False, lineterminator="\n", float_format="%.4f")
    pd.DataFrame(params).to_csv(OUT / "params.csv", index=False, lineterminator="\n", float_format="%.6g")
    pd.set_option("display.width", 250)
    print(pd.DataFrame(national).round(3).to_string(index=False))
    print(df[["item", "group", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd"]].round(2).to_string(index=False))
    print(pd.DataFrame(params).T.to_string())
    print(df[df.item.str.startswith("co2")][["group", "measure", "net_mt_central", "gross_mt_central", "r_co2_central",
                                              "origin_mt_central", "remit_mt_central", "scc_2024usd_central",
                                              "global_damages_bn_central"]].round(2).to_string(index=False))
    print(df[df.item == "pm25_consumption"][["group", "measure", "deaths_central", "sigma_central", "caused_central"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
