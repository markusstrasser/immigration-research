#!/usr/bin/env python3
"""Question 4 and the winners-and-losers rows.

Moving costs: the number of US-born adults who leave California giving "wanted better
neighborhood/less crime" as their main reason (reasons.py -> q4_counts.csv), converted to
households, times per-household moving costs read from published sources:
  low      IRS SOI Table 1.4, moving-expense adjustment, all returns, tax years 2014-2017:
           amount / returns (deductible job-move costs), inflated to 2024 dollars;
  central  AMSA Industry Fact Sheet: "Average cost of an interstate household move: About
           $4,300 ... (2009)", inflated to 2024 dollars;
  high     Bayer & Juessen (IZA DP 3330, 2008), structural migration cost including non-pecuniary
           costs, "US$ 18,285" per migration (dollar year not stated; used as printed).
Inflation uses IPUMS CPI99 (CPI-U based): a calendar-year-Y dollar is multiplied by
CPI99(ASEC Y+1) / CPI99(ASEC 2025).

Tax base moved: IRS SOI net California-to-Texas AGI (irs_flows.py) times ITEP Who Pays? 7th
edition state-and-local tax shares for the fourth income quintile (2024 law, 2023 incomes):
  low      individual sales and excise taxes plus personal income tax;
  central  total taxes less property taxes (the vacated home stays on the roll);
  high     total taxes.

Writes derived/q4_costs.csv, derived/tax_transfer.csv and derived/winners_losers_rows.csv.

Run from the repository root after reasons.py and irs_flows.py (xlrd reads the IRS .xls files):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd --with beautifulsoup4 python3 infra/immigration-fiscal/movers_reasons_2026_09_24/ledger.py
"""
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from lane_common import BUILD, CACHE, DERIVED, con, write_csv


def cpi_factor(year: int) -> float:
    c = con()
    cpi = dict(c.execute(f"select YEAR, max(CPI99) from read_parquet('{BUILD / 'movers.parquet'}') group by 1").fetchall())
    return cpi[year + 1] / cpi[2025]


def irs_moving() -> pd.DataFrame:
    cols = {"14in14ar.xls": (2014, 95, 96), "15in14ar.xls": (2015, 95, 96), "16in14ar.xls": (2016, 95, 96),
            "17in14ar.xls": (2017, 97, 98)}
    rows = []
    for f, (ty, cn, ca) in cols.items():
        df = pd.read_excel(CACHE / "lit" / f, sheet_name=0, header=None, dtype=object)
        head = " ".join(str(df.iat[r, cn]) for r in range(2, 7))
        if "Moving expenses" not in head or str(df.iat[8, 0]).strip() != "All returns, total":
            raise SystemExit(f"[FAILED] {f}: moving-expense column or total row not where expected ({head!r})")
        n, amt = float(df.iat[8, cn]), float(df.iat[8, ca]) * 1000
        rows.append({"tax_year": ty, "returns": n, "amount_usd": amt, "per_return_nominal": amt / n,
                     "per_return_2024usd": amt / n * cpi_factor(ty)})
    return pd.DataFrame(rows)


def amsa() -> float:
    t = (CACHE / "lit" / "mibox_industry_fact_sheet.txt").read_text(errors="replace")
    t = re.sub(r"\s+", " ", t)
    m = re.search(r"Average cost of an interstate household move: About \$([\d,]+), based on an average weight of "
                  r"([\d,]+) pounds and average distance of ([\d,]+) miles \((\d{4})\)", t)
    if not m or m.group(4) != "2009":
        raise SystemExit("[FAILED] AMSA fact-sheet sentence not found as quoted")
    return float(m.group(1).replace(",", ""))


def bayer_juessen() -> float:
    t = re.sub(r"\s+", " ", (CACHE / "lit" / "bayer_juessen_iza_dp3330.txt").read_text(errors="replace"))
    if "The estimated migration costs are US$ 18,285" not in t:
        raise SystemExit("[FAILED] Bayer-Juessen sentence not found as quoted")
    return 18285.0


def itep_rates(state: str) -> dict:
    """Fourth-quintile shares of family income, percent, from the ITEP state table."""
    soup = BeautifulSoup((CACHE / "itep" / f"{state}.html").read_text(errors="replace"), "html.parser")
    table = soup.find("table")
    rows = {}
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c]
        if len(cells) >= 8:
            rows[cells[0]] = cells[1:8]
    groups = rows["Income Group"]
    q4 = groups.index("Fourth 20%")
    val = lambda k: float(rows[k][q4].rstrip("%"))
    r = {"group": "Fourth 20%", "range": rows["Income Range"][q4], "avg_income": rows["Average Income in Group"][q4],
         "total": val("TOTAL TAXES"), "property": val("Property Taxes"), "pit": val("Personal Income Taxes"),
         "sales_ind": val("General Sales–Individuals") + val("Other Sales & Excise–Ind")}
    r["low"] = r["pit"] + r["sales_ind"]
    r["central"] = r["total"] - r["property"]
    r["high"] = r["total"]
    return r


def main() -> None:
    irs_m = irs_moving()
    low_cost = float(irs_m.per_return_2024usd.mean())
    amsa_2009 = amsa()
    central_cost = amsa_2009 * cpi_factor(2009)
    high_cost = bayer_juessen()
    costs = {"low": (low_cost, "IRS SOI Table 1.4 moving-expense adjustment, TY2014-2017 mean per return, 2024$"),
             "central": (central_cost, "AMSA average interstate household move $4,300 (2009), 2024$"),
             "high": (high_cost, "Bayer & Juessen (2008) structural migration cost US$18,285, dollar year not stated")}

    q4 = pd.read_csv(DERIVED / "q4_counts.csv")
    ca = q4[q4.population == "US-born adults leaving California"].set_index("window")
    main_w = ca.loc["2005-2025"]
    recent = ca.loc["2020-2025"]
    # low: the smaller of the CPS level and the ACS-scaled mean over years with a published ACS ratio
    low_opts = [(main_w.nbhd_crime_households_per_year_cps, main_w.nbhd_crime_persons_per_year_cps, "CPS level, 2005-2025"),
                (main_w.nbhd_crime_households_per_year_acs_own_years_only, main_w.nbhd_crime_persons_per_year_acs_own_years_only,
                 "ACS-scaled, 2005-2025 years with a published ACS ratio only")]
    counts = {"low": min(low_opts, key=lambda t: t[0]),
              "central": (main_w.nbhd_crime_households_per_year_acs_scaled, main_w.nbhd_crime_persons_per_year_acs_scaled,
                          "ACS-scaled one year at a time, 2005-2025"),
              "high": (recent.nbhd_crime_households_per_year_acs_scaled, recent.nbhd_crime_persons_per_year_acs_scaled,
                       "ACS-scaled one year at a time, 2020-2025")}
    cost_rows = []
    for k in ("low", "central", "high"):
        hh, pp, clab = counts[k]
        cst, slab = costs[k]
        cost_rows.append({"case": k, "households_per_year": round(hh), "persons_per_year": round(pp), "count_basis": clab,
                          "cost_per_household_usd": round(cst), "cost_basis": slab,
                          "total_musd_per_year": round(hh * cst / 1e6, 2)})
    for k, (cst, slab) in costs.items():  # full grid for the record
        for kk, (hh, pp, clab) in counts.items():
            cost_rows.append({"case": f"grid cost={k} count={kk}", "households_per_year": round(hh), "persons_per_year": round(pp),
                              "count_basis": clab, "cost_per_household_usd": round(cst), "cost_basis": slab,
                              "total_musd_per_year": round(hh * cst / 1e6, 2)})
    cdf = pd.DataFrame(cost_rows)
    write_csv(cdf, "q4_costs.csv")
    write_csv(irs_m.round(2), "irs_moving_expenses.csv")

    # ---- tax base moved
    irs = pd.read_csv(DERIVED / "irs_ca_tx.csv")
    ca_r, tx_r = itep_rates("california"), itep_rates("texas")
    iw = pd.read_csv(DERIVED / "income_weighted_shares.csv").set_index(["population", "reason"])
    s_out = iw.loc[("householders leaving California", "neighborhood_crime"), "income_weighted_share_pct"] / 100
    s_in = iw.loc[("householders moving into California", "neighborhood_crime"), "income_weighted_share_pct"] / 100
    tt = []
    # The per-year rows price one year's net cohort. The "stock" rows sum the net flows of every pair
    # 2011-12..2022-23: the income base California held less by 2022-23 because of net out-migration
    # since 2011, at each cohort's move-year AGI (no income growth, deaths or later moves).
    nb_all = irs.ca_to_us_agi_bn * s_out - irs.us_to_ca_agi_bn * s_in
    stock = {"net_ca_to_tx_agi_bn": float(irs.net_ca_to_tx_agi_bn.sum()), "net_ca_to_us_agi_bn": float(irs.net_ca_to_us_agi_bn.sum()),
             "nbhd_crime_net_agi_bn": float(nb_all.sum()),
             "net_ca_to_tx_individuals": float((irs.ca_to_tx_individuals - irs.tx_to_ca_individuals).sum())}
    for win, sel in (("mean 2011-12 to 2022-23", irs.index == irs.index), ("mean 2019-20 to 2022-23", irs.pair >= "2019-2020"),
                     ("stock: sum 2011-12 to 2022-23", None)):
        if sel is None:
            net_tx, net_us, nb_net, net_ind = (stock["net_ca_to_tx_agi_bn"], stock["net_ca_to_us_agi_bn"],
                                               stock["nbhd_crime_net_agi_bn"], stock["net_ca_to_tx_individuals"])
        else:
            d = irs[sel]
            net_tx = float(d.net_ca_to_tx_agi_bn.mean())
            net_us = float(d.net_ca_to_us_agi_bn.mean())
            nb_net = float((d.ca_to_us_agi_bn * s_out - d.us_to_ca_agi_bn * s_in).mean())
            net_ind = float((d.ca_to_tx_individuals - d.tx_to_ca_individuals).mean())
        for k in ("low", "central", "high"):
            tt.append({"window": win, "rate_case": k, "net_ca_to_tx_agi_bn": round(net_tx, 3),
                       "net_ca_to_tx_individuals": round(net_ind),
                       "ca_rate_pct": ca_r[k], "tx_rate_pct": tx_r[k],
                       "ca_revenue_loss_bn": round(net_tx * ca_r[k] / 100, 3),
                       "tx_revenue_gain_bn": round(net_tx * tx_r[k] / 100, 3),
                       "net_ca_to_all_states_agi_bn": round(net_us, 3),
                       "ca_revenue_loss_all_states_bn": round(net_us * ca_r[k] / 100, 3),
                       "nbhd_crime_net_agi_bn": round(nb_net, 3),
                       "ca_revenue_loss_nbhd_crime_bn": round(nb_net * ca_r[k] / 100, 4)})
    tdf = pd.DataFrame(tt)
    write_csv(tdf, "tax_transfer.csv")

    # ---- winners and losers
    per_person = lambda k: counts[k][0] * costs[k][0] / counts[k][1]
    m = tdf[tdf.window == "mean 2011-12 to 2022-23"].set_index("rate_case")
    src_cost = ("lit/moving_costs_and_surveys.md: IRS SOI Table 1.4 (14in14ar-17in14ar.xls); AMSA Industry Fact Sheet; "
                "Bayer & Juessen IZA DP 3330 p. 19; counts derived/q4_counts.csv")
    src_tax = ("IRS SOI state migration files 2011-12 to 2022-23 (derived/irs_ca_tx.csv); ITEP Who Pays? 7th ed. "
               "California and Texas tables, fourth quintile (itep.org/whopays)")
    st = tdf[tdf.window == "stock: sum 2011-12 to 2022-23"].set_index("rate_case")
    nb_pop = counts["central"][1] / 1e6
    ind_m = float(m.loc["central", "net_ca_to_tx_individuals"]) / 1e6
    ind_stock_m = float(st.loc["central", "net_ca_to_tx_individuals"]) / 1e6
    us_ind_m = float((irs.ca_to_us_individuals - irs.us_to_ca_individuals).mean()) / 1e6
    us_ind_stock_m = float((irs.ca_to_us_individuals - irs.us_to_ca_individuals).sum()) / 1e6
    ALL_FLOW = "taxes on net income moved to all other states (one year's net cohort)"
    TX_FLOW = "taxes on the net income moved from California at Texas rates (one year's net cohort)"
    ALL_STOCK = "taxes on the net income moved out 2011-12..2022-23, as of 2022-23 (stock)"
    TX_STOCK = "taxes on the net income moved from California 2011-12..2022-23 at Texas rates, as of 2022-23 (stock)"
    rows = [
        {"group": "US-born adults leaving California who cite better neighborhood/less crime",
         "channel": "moving costs (household goods, travel; high case adds non-pecuniary costs)", "direction": "loss",
         "bn_low": round(cdf.iloc[0].total_musd_per_year / 1e3, 4), "bn_central": round(cdf.iloc[1].total_musd_per_year / 1e3, 4),
         "bn_high": round(cdf.iloc[2].total_musd_per_year / 1e3, 4), "population_m": round(nb_pop, 4),
         "per_person_usd": round(per_person("central")), "basis": "modelled", "relation_to_account": "beside",
         "counterfactual": ("without the conditions they cite they stay, so the moving cost is a floor on their loss from "
                            "those conditions; an upper bound for moves driven by ethnic composition, which the category "
                            "cannot isolate"),
         "source": src_cost},
        {"group": "US-born adults leaving California who cite better neighborhood/less crime",
         "channel": "the neighborhood and crime conditions they report leaving", "direction": "loss",
         "bn_low": None, "bn_central": None, "bn_high": None, "population_m": round(nb_pop, 4), "per_person_usd": None,
         "basis": "unpriced", "relation_to_account": "beside",
         "counterfactual": ("without the conditions they cite: what they bore before leaving and the California location "
                            "they gave up; not measured here"), "source": "derived/reasons_ca_leavers.csv"},
        {"group": "US-born adults leaving California who cite better neighborhood/less crime",
         "channel": "gain from the destination they chose (revealed preference)", "direction": "gain",
         "bn_low": None, "bn_central": None, "bn_high": None, "population_m": round(nb_pop, 4), "per_person_usd": None,
         "basis": "unpriced", "relation_to_account": "beside",
         "counterfactual": ("against staying with the conditions they cite (a different baseline from the rows above); "
                            "Kennan & Walker (2011) Table V put the average realized move's net cost below zero"),
         "source": "lit/moving_costs_and_surveys.md 1(c)"},
        {"group": "California state and local budgets", "channel": ALL_FLOW, "direction": "loss",
         "bn_low": m.loc["low", "ca_revenue_loss_all_states_bn"], "bn_central": m.loc["central", "ca_revenue_loss_all_states_bn"],
         "bn_high": m.loc["high", "ca_revenue_loss_all_states_bn"], "population_m": round(us_ind_m, 4),
         "per_person_usd": round(m.loc["central", "ca_revenue_loss_all_states_bn"] * 1e9 / (us_ind_m * 1e6)) if us_ind_m else None,
         "basis": "modelled", "relation_to_account": "beside",
         "counterfactual": "the net movers stay; a transfer to other states, and California also stops serving them",
         "source": src_tax},
        {"group": "California state and local budgets", "channel": "taxes on net income moved to Texas (one year's net cohort)",
         "direction": "loss", "bn_low": m.loc["low", "ca_revenue_loss_bn"], "bn_central": m.loc["central", "ca_revenue_loss_bn"],
         "bn_high": m.loc["high", "ca_revenue_loss_bn"], "population_m": round(ind_m, 4),
         "per_person_usd": round(m.loc["central", "ca_revenue_loss_bn"] * 1e9 / (ind_m * 1e6)) if ind_m else None,
         "basis": "modelled", "relation_to_account": f"overlaps:{ALL_FLOW}",
         "counterfactual": "the movers stay; a transfer between states, and California also stops serving them", "source": src_tax},
        {"group": "Texas state and local budgets", "channel": TX_FLOW,
         "direction": "gain", "bn_low": m.loc["low", "tx_revenue_gain_bn"], "bn_central": m.loc["central", "tx_revenue_gain_bn"],
         "bn_high": m.loc["high", "tx_revenue_gain_bn"], "population_m": round(ind_m, 4),
         "per_person_usd": round(m.loc["central", "tx_revenue_gain_bn"] * 1e9 / (ind_m * 1e6)) if ind_m else None,
         "basis": "modelled", "relation_to_account": "beside",
         "counterfactual": "the movers stay in California; Texas also takes on the cost of serving them", "source": src_tax},
        {"group": "California state and local budgets",
         "channel": "taxes on net income moved by households citing better neighborhood/less crime (all destinations)",
         "direction": "loss", "bn_low": m.loc["low", "ca_revenue_loss_nbhd_crime_bn"],
         "bn_central": m.loc["central", "ca_revenue_loss_nbhd_crime_bn"], "bn_high": m.loc["high", "ca_revenue_loss_nbhd_crime_bn"],
         "population_m": None, "per_person_usd": None, "basis": "modelled", "relation_to_account": f"overlaps:{ALL_FLOW}",
         "counterfactual": "those households stay; income-weighted CPS reason shares applied to IRS gross flows",
         "source": src_tax + "; derived/income_weighted_shares.csv"},
        {"group": "California state and local budgets", "channel": ALL_STOCK, "direction": "loss",
         "bn_low": st.loc["low", "ca_revenue_loss_all_states_bn"], "bn_central": st.loc["central", "ca_revenue_loss_all_states_bn"],
         "bn_high": st.loc["high", "ca_revenue_loss_all_states_bn"], "population_m": round(us_ind_stock_m, 4),
         "per_person_usd": round(st.loc["central", "ca_revenue_loss_all_states_bn"] * 1e9 / (us_ind_stock_m * 1e6)),
         "basis": "modelled", "relation_to_account": f"overlaps:{ALL_FLOW}",
         "counterfactual": ("the net movers of 2011-12..2022-23 stay; each cohort at its move-year AGI (no income growth, "
                            "deaths or later moves); California also stops serving them"),
         "source": src_tax},
        {"group": "Texas state and local budgets", "channel": TX_STOCK, "direction": "gain",
         "bn_low": st.loc["low", "tx_revenue_gain_bn"], "bn_central": st.loc["central", "tx_revenue_gain_bn"],
         "bn_high": st.loc["high", "tx_revenue_gain_bn"], "population_m": round(ind_stock_m, 4),
         "per_person_usd": round(st.loc["central", "tx_revenue_gain_bn"] * 1e9 / (ind_stock_m * 1e6)),
         "basis": "modelled", "relation_to_account": f"overlaps:{TX_FLOW}",
         "counterfactual": "the net movers of 2011-12..2022-23 stay in California; Texas also serves them",
         "source": src_tax},
        {"group": "California state and local budgets", "channel": "spending no longer needed for the net movers",
         "direction": "gain", "bn_low": None, "bn_central": None, "bn_high": None, "population_m": round(us_ind_m, 4),
         "per_person_usd": None, "basis": "unpriced", "relation_to_account": "beside",
         "counterfactual": ("the net movers stay and use California services; pricing needs the account's incidence and "
                            "response rules, because the ITEP rows count only taxes families bear"),
         "source": ""},
        {"group": "Texas state and local budgets", "channel": "spending to serve the net movers from California",
         "direction": "loss", "bn_low": None, "bn_central": None, "bn_high": None, "population_m": round(ind_m, 4),
         "per_person_usd": None, "basis": "unpriced", "relation_to_account": "beside",
         "counterfactual": "the net movers stay in California; same pricing requirement as California's row",
         "source": ""},
        {"group": "Natives who stay in California", "channel": "housing-cost relief from lower demand", "direction": "gain",
         "bn_low": None, "bn_central": None, "bn_high": None, "population_m": None, "per_person_usd": None,
         "basis": "unpriced", "relation_to_account": "beside",
         "counterfactual": "the leavers stay; not measured in this lane", "source": ""},
        {"group": "California owners and landlords", "channel": "lower rents and prices (the other side of the relief)",
         "direction": "loss", "bn_low": None, "bn_central": None, "bn_high": None, "population_m": None, "per_person_usd": None,
         "basis": "unpriced", "relation_to_account": "overlaps:housing-cost relief from lower demand",
         "counterfactual": "the leavers stay; a transfer inside California", "source": ""},
        {"group": "Texas residents", "channel": "housing costs and congestion from in-movers (renters lose, owners gain)",
         "direction": "loss", "bn_low": None, "bn_central": None, "bn_high": None, "population_m": None, "per_person_usd": None,
         "basis": "unpriced", "relation_to_account": "beside", "counterfactual": "the movers stay in California", "source": ""},
    ]
    wl = pd.DataFrame(rows, columns=["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m",
                                     "per_person_usd", "basis", "relation_to_account", "counterfactual", "source"])
    write_csv(wl, "winners_losers_rows.csv")
    print(cdf.head(3).to_string(index=False))
    print(irs_m.round(0).to_string(index=False))
    print(f"ITEP CA {ca_r}\nITEP TX {tx_r}")
    print(tdf.to_string(index=False))
    print(wl[["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "basis"]].to_string(index=False))


if __name__ == "__main__":
    main()
