"""Supply side of the housing channel: construction costs with and without the group, priced in
the housing lane's own long-run model as an offset to its demand-only transfers.

Model (housing lane, long run): housing services from fixed land and reproducible structures at
unit cost c, Cobb-Douglas with land share a, per-capita demand elasticity eD. Log changes with
versus without the group:
  dlnP          = e_d dlnN + pi dlnc      e_d = a / (1 - a(1 - eD))    pi = (1 - a) / (1 - a(1 - eD))
  a dln(land r) = e_d dlnN + a(1 - eD) pi dlnc      (the land-rent part of the price change)
  dlnH          = dlnN - eD dlnP                     (the housing stock)
The housing lane's long-run arm is dlnc = 0. Along the arrival path ln c moves in proportion to
ln(1 + lambda g), so both paths keep the lane's constant-elasticity form A with
  e_total = e_d + pi dlnc / ln(1 + g)       e_land = e_d + a(1 - eD) pi dlnc / ln(1 + g)
and the lane's own evaluate() prices them unchanged: e_total gives renters' gross extra rent and
owners' value (constant price-to-rent, the lane's convention); e_land gives the land-rent transfer
to landlords and the welfare net, the lane's Z item. The structure part of the rent change,
e_total - e_land, is a cost pass-through: landlords' costs fall with their rents.

Construction cost with versus without the group, dlnc (negative = cheaper with the group):
  A  the account's own factor prices. Construction's labour share of gross output theta, split
     by its earnings mix (low-skill share ell), times the CES wage changes of the adopted
     production term (hs_or_less split, capital fully adjusting, so the rental rate is
     unchanged); intermediate inputs are priced at the numeraire. This is the relative-price
     side of P: the same factor-price changes the account already counts.
  B  A plus a construction-specific premium, the case where the group's concentration in
     construction moves construction wages more than low-skill wages in general. Monras (2020),
     1990-2000 decade IV: native low-skill wages inside construction minus native low-skill wages
     in all sectors, per unit of Mexican inflow relative to low-skilled labour, at the group's
     national dose m / (1 - m).
  C  A plus a premium from Bratsberg and Raaum (2012), Norway 1998-2005, relative effects across
     16 construction activities per unit ln(1 + M/N). The dose is construction's excess
     ln(1 + M/N) over all sectors within the below-BA cell, on earnings (efficiency units), so the
     account's skill-level wage change in A is not counted twice. C_wage applies the native-wage
     coefficient to below-BA labour cost; C_price_* apply the building-cost price coefficient to
     the whole construction price. Their price indices are cost-based with fixed input weights and
     include the lower pay of immigrant workers, so C_price_* are upper bounds.
Geographies: national-uniform (one national cost change) and metro-local (each area's change
scaled by its union share of construction-trades earnings relative to the national share).

Wage-premium cases (B, C_wage) also get an incidence row: the premium is a transfer from other
residents' construction earnings to buyers of construction, plus a net triangle 1/2 x premium x
the group's earnings in the cell.

Outputs: derived/supply_grid.csv (every case), derived/supply_headline.csv,
derived/supply_premium_incidence.csv, derived/supply_parameters.csv, derived/supply_checks.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/supply.py
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
HOUSING = ROOT / "infra/immigration-fiscal/housing_transfer_2026_09_23"
SCENARIOS = ROOT / "infra/immigration-fiscal/matched_benefits_2026_09_19/derived/scenarios.csv"

spec = importlib.util.spec_from_file_location("housing_arms", HOUSING / "arms.py")
arms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arms)

OTHER_RESIDENTS = arms.RESIDENTS - arms.TARGET
LEVELS = ("low", "central", "high")
# Monras (2020, JPE) 1990-2000 IV, per unit of Mexican inflow relative to low-skilled labour:
# native low-skill wage inside construction (Table D10 col. 6) and in all sectors (Table 9).
MONRAS = {
    "state": {"construction": -0.454, "construction_se": 0.213, "all": -0.255, "all_se": 0.160},
    "metro": {"construction": -0.765, "construction_se": 0.330, "all": -0.384, "all_se": 0.232},
}
# Monras Table 10, long-run IV of log rent on the same regressor (sensitivity arm only).
MONRAS_RENT = {"state": (-0.548, 0.366), "metro": (-1.171, 0.518)}
# Bratsberg and Raaum (2012), CReAM DP 06/10 text, per unit ln(1 + M/N) in the activity: native
# log daily wage with individual FE (Table 1 col. 2); log building-cost price index, all
# activities and without plumbing and electrical (Table 5 cols. 1 and 4).
BR = {"wage": (-0.724, 0.202), "price_all": (-1.155, 0.214), "price_excl_licensed": (-0.387, 0.088)}
COST_CASES = {
    # name: (sigma, theta level, premium or None, the account's skill split)
    "A_low": (2.5, "low", None, "hs_or_less"),
    "A_central": (2.0, "central", None, "hs_or_less"),
    "A_high": (1.5, "high", None, "hs_or_less"),
    "A_central_below_ba": (2.0, "central", None, "below_ba"),
    "B_state": (2.0, "central", "monras_state", "hs_or_less"),
    "B_metro": (2.0, "central", "monras_metro", "hs_or_less"),
    "B_high": (1.5, "high", "monras_metro", "hs_or_less"),
    "C_wage": (2.0, "central", "br_wage", "hs_or_less"),
    "C_price_excl_licensed": (2.0, "central", "br_price_excl_licensed", "hs_or_less"),
    "C_price_all": (2.0, "central", "br_price_all", "hs_or_less"),
}
# Education cells of construction_national.csv that form each split's lower skill group.
LOW_GROUP = {"hs_or_less": "hs_or_less", "below_ba": "below_ba"}
# The cell whose construction wages each wage premium moves.
PREMIUM_CELL = {"monras_state": "hs_or_less", "monras_metro": "hs_or_less", "br_wage": "below_ba"}


def load_inputs():
    bea = pd.read_csv(DERIVED / "inputs_bea.csv").set_index("item")["value"]
    theta = {
        "low": bea["construction_labour_share_2024_low"],
        "central": 0.5 * (bea["construction_labour_share_2024_central"]
                          + bea["single_family_labour_share_2017_central"]),
        "high": bea["single_family_labour_share_2017_high"],
    }
    nat = pd.read_csv(DERIVED / "construction_national.csv")
    pick = lambda dim, cat, edu, grp: nat[(nat.dimension == dim) & (nat.category == cat)
                                          & (nat.education == edu) & (nat.measure == "earnings")
                                          & (nat.group_set == grp)].iloc[0]
    industry_all = pick("industry_total", "construction_industry", "all", "all")["total"]
    ell = {split: pick("industry_total", "construction_industry", cell, "all")["total"] / industry_all
           for split, cell in LOW_GROUP.items()}
    trades_union_share = pick("trades_total", "all_trades", "all", "union")["share"]
    # Earnings in each premium cell of the construction industry: the union's and everyone else's.
    cell_earnings = {}
    for cell in set(PREMIUM_CELL.values()):
        row = pick("industry_total", "construction_industry", cell, "union")
        cell_earnings[cell] = (row["group_total"], row["total"] - row["group_total"])
    # Bratsberg-Raaum dose: construction's ln(1 + M/N) minus all sectors', below-BA earnings.
    log_ratio = lambda share: np.log1p(share / (1 - share))
    br_dose = (log_ratio(pick("industry_total", "construction_industry", "below_ba", "union")["share"])
               - log_ratio(pick("all_workers", "all", "below_ba", "union")["share"]))
    scen_all = pd.read_csv(SCENARIOS)
    wages, m = {}, {}
    for split in LOW_GROUP:
        scen = scen_all[(scen_all.capital_adjustment == 1) & (scen_all.labor_supply_elasticity == 0)
                        & (scen_all.proxy == "PEARNVAL") & (scen_all.split == split)
                        & (scen_all.normalization == "gdp") & (scen_all.labor_share == 0.65)]
        wages[split] = {}
        for sigma, sub in scen.groupby("sigma"):
            row = sub.iloc[0]
            if sub[["wage_low_without_over_with", "wage_high_without_over_with"]].nunique().max() != 1:
                raise ValueError("wage ratios differ within a sigma")
            # With minus without, in logs.
            wages[split][float(sigma)] = (-np.log(row.wage_low_without_over_with),
                                          -np.log(row.wage_high_without_over_with))
        m[split] = float(scen.iloc[0].target_low_efficiency_share)
    return {"theta": theta, "ell": ell, "trades_union_share": trades_union_share, "wages": wages,
            "m": m, "br_dose": float(br_dose), "cell_earnings": cell_earnings}


def wage_premium(premium, inp):
    """Construction-specific log wage change in the premium's cell, with minus without."""
    if premium.startswith("monras_"):
        est = MONRAS[premium.removeprefix("monras_")]
        m = inp["m"]["hs_or_less"]
        return (est["construction"] - est["all"]) * m / (1 - m)
    if premium == "br_wage":
        return BR["wage"][0] * inp["br_dose"]
    raise KeyError(premium)


def cost_change(case, inp):
    """Log construction cost change with minus without the group: (total, A part, premium part)."""
    sigma, level, premium, split = COST_CASES[case]
    theta = inp["theta"][level]
    dw_low, dw_high = inp["wages"][split][sigma]
    share = inp["ell"][split]
    a_part = theta * (share * dw_low + (1 - share) * dw_high)
    b_part = 0.0
    if premium in PREMIUM_CELL:
        b_part = theta * inp["ell"][PREMIUM_CELL[premium]] * wage_premium(premium, inp)
    elif premium:
        b_part = BR[premium.removeprefix("br_")][0] * inp["br_dose"]
    return a_part + b_part, a_part, b_part


def housing_params(level):
    a, ed = arms.LAND[level], arms.DEMAND[level]
    denom = 1 - a * (1 - ed)
    return {"a": a, "eD": ed, "e_d": a / denom, "pi": (1 - a) / denom, "land_pass": a * (1 - ed) * (1 - a) / denom}


def elasticities(level, dlnc, s):
    hp = housing_params(level)
    log1g = -np.log1p(-np.asarray(s, float))
    safe = np.where(log1g > 1e-12, log1g, 1.0)
    e_total = np.where(log1g > 1e-12, hp["e_d"] + hp["pi"] * dlnc / safe, hp["e_d"])
    e_land = np.where(log1g > 1e-12, hp["e_d"] + hp["land_pass"] * dlnc / safe, hp["e_d"])
    return e_total, e_land


def main():
    areas, _ = arms.load_areas()
    metro = pd.read_csv(DERIVED / "construction_metro.csv", dtype={"area": str})
    inp = load_inputs()
    theta, ell, trades_share, wages, m = (inp[k] for k in ("theta", "ell", "trades_union_share", "wages", "m"))
    ratio = (metro.set_index("area")["trades_earnings_union_share"] / trades_share)
    mapped = areas["area"].map(ratio)
    if mapped.isna().any():
        raise ValueError(f"areas without a construction share: {areas.loc[mapped.isna(), 'area'].tolist()[:5]}")
    areas["cost_ratio"] = mapped.to_numpy()
    s_uniform = np.full(len(areas), arms.TARGET / arms.RESIDENTS)
    renters = areas["other_renter_households"].sum()
    rows = []
    for case, level, geography, own in itertools.product(COST_CASES, LEVELS,
                                                         ("national_uniform", "metro_local"), arms.OWN):
        dlnc, a_part, b_part = cost_change(case, inp)
        hp = housing_params(level)
        if geography == "national_uniform":
            s, dlnc_area = s_uniform, np.full(len(areas), dlnc)
        else:
            s, dlnc_area = areas["group_share"].to_numpy(), dlnc * areas["cost_ratio"].to_numpy()
        e_total, e_land = elasticities(level, dlnc_area, s)
        dem = arms.evaluate(areas, "long_run", level, "A", geography, own)
        tot = arms.evaluate(areas, "long_run", level, "A", geography, own, e_override=np.asarray(e_total))
        land = arms.evaluate(areas, "long_run", level, "A", geography, own, e_override=np.asarray(e_land))
        offset = dem["other_renters_extra_rent_bn"] - tot["other_renters_extra_rent_bn"]
        row = {
            "cost_case": case, "level": level, "geography": geography, "ownership": own,
            "sigma": COST_CASES[case][0], "theta": theta[COST_CASES[case][1]],
            "split": COST_CASES[case][3], "ell": ell[COST_CASES[case][3]],
            "dlnc": dlnc, "dlnc_A": a_part, "dlnc_B": b_part, "pass_through_pi": hp["pi"],
            "land_rent_pass": hp["land_pass"], "e_d": hp["e_d"],
            "other_renters_extra_rent_demand_only_bn": dem["other_renters_extra_rent_bn"],
            "other_renters_extra_rent_with_supply_bn": tot["other_renters_extra_rent_bn"],
            "offset_to_other_renters_bn": offset,
            "offset_share_of_demand_only": offset / dem["other_renters_extra_rent_bn"],
            "offset_land_rent_part_bn": dem["other_renters_extra_rent_bn"] - land["other_renters_extra_rent_bn"],
            "offset_structure_part_bn": land["other_renters_extra_rent_bn"] - tot["other_renters_extra_rent_bn"],
            "land_rent_transfer_other_renters_with_supply_bn": land["other_renters_extra_rent_bn"],
            "group_renters_extra_rent_demand_only_bn": dem["group_renters_extra_rent_bn"],
            "group_renters_extra_rent_with_supply_bn": tot["group_renters_extra_rent_bn"],
            "other_owner_value_gain_demand_only_tn": dem["other_owner_value_gain_stock_bn"] / 1e3,
            "other_owner_value_gain_with_supply_tn": tot["other_owner_value_gain_stock_bn"] / 1e3,
            "owner_value_offset_tn": (dem["other_owner_value_gain_stock_bn"]
                                      - tot["other_owner_value_gain_stock_bn"]) / 1e3,
            "owner_value_offset_land_part_tn": (dem["other_owner_value_gain_stock_bn"]
                                                - land["other_owner_value_gain_stock_bn"]) / 1e3,
            "net_frame_demand_only_bn": dem["net_other_residents_frame_bn"],
            "net_frame_with_supply_bn": land["net_other_residents_frame_bn"],
            "net_welfare_demand_only_bn": dem["net_other_residents_welfare_bn"],
            "net_welfare_with_supply_bn": land["net_other_residents_welfare_bn"],
            "offset_per_other_renter_household": offset * 1e9 / renters,
            "offset_per_other_resident": offset * 1e9 / OTHER_RESIDENTS,
            "offset_per_group_member": offset * 1e9 / arms.TARGET,
        }
        if geography == "national_uniform":
            dlnn = -np.log1p(-arms.TARGET / arms.RESIDENTS)
            dlnp_dem = hp["e_d"] * dlnn
            dlnp_tot = dlnp_dem + hp["pi"] * dlnc
            row["stock_with_over_without_demand_only"] = np.exp(dlnn - hp["eD"] * dlnp_dem)
            row["stock_with_over_without_with_supply"] = np.exp(dlnn - hp["eD"] * dlnp_tot)
            row["rent_with_over_without_demand_only"] = np.exp(dlnp_dem)
            row["rent_with_over_without_with_supply"] = np.exp(dlnp_tot)
            # Construction-cost reduction at which the group's net rent effect is zero.
            row["breakeven_dlnc_for_zero_rent_effect"] = -dlnp_dem / hp["pi"]
        rows.append(row)
    grid = pd.DataFrame(rows)
    grid.to_csv(DERIVED / "supply_grid.csv", index=False)
    head = grid[grid.ownership == "central"]
    head.to_csv(DERIVED / "supply_headline.csv", index=False)

    # Sensitivity arm: Monras's local long-run rent coefficients transported to the national
    # Mexico-born stock, the way the housing lane's short-run arm transports local demand
    # estimates. A total effect (demand and supply together), not an offset.
    nat = pd.read_csv(DERIVED / "construction_national.csv")
    low = nat[(nat.dimension == "all_workers") & (nat.education == "hs_or_less")
              & (nat.measure == "employed")]
    mx = float(low[low.group_set == "mx_born"].group_total.iloc[0])
    union = float(low[low.group_set == "union"].group_total.iloc[0])
    total_low = float(low[low.group_set == "all"].total.iloc[0])
    # Monras's regressor is Mexican immigrants over low-skilled workers; the Mexico-born dose is
    # his treatment, the union dose also removes the US-born members his variation does not cover.
    doses = {"mexico_born": mx / (total_low - mx), "union": union / (total_low - union)}
    dose = doses["mexico_born"]
    other_rent = areas["other_renter_rent"].sum()
    monras_rows = []
    for (geo, (beta, se)), (basis, d) in itertools.product(MONRAS_RENT.items(), doses.items()):
        for label, b in (("point", beta), ("ci_low", beta - 1.96 * se), ("ci_high", beta + 1.96 * se)):
            f = 1 - np.exp(-b * d)  # share of today's rent due to the group's presence
            monras_rows.append({"geography": geo, "dose_basis": basis, "estimate": label,
                                "coefficient": b, "dose": d, "rent_share_due_to_group": f,
                                "other_renters_extra_rent_bn": f * other_rent / 1e9})
    pd.DataFrame(monras_rows).to_csv(DERIVED / "supply_monras_transport.csv", index=False)

    # Incidence of the construction-specific wage premiums (B, C_wage): other residents'
    # construction earnings fall by the premium (a transfer to buyers of construction); the net
    # gain to non-members is the triangle over the group's own earnings in the cell.
    s_group = arms.TARGET / arms.RESIDENTS
    incidence = []
    for premium, cell in PREMIUM_CELL.items():
        dw = wage_premium(premium, inp)
        group_earn, other_earn = inp["cell_earnings"][cell]
        triangle = -0.5 * dw * group_earn / 1e9
        incidence.append({
            "premium": premium, "cell": cell, "wage_premium_dlnw": dw,
            "group_cell_earnings_bn": group_earn / 1e9, "other_cell_earnings_bn": other_earn / 1e9,
            "transfer_from_other_construction_workers_bn": -dw * other_earn / 1e9,
            "net_triangle_bn": triangle,
            # Buyers' share by population, an assumption: the group buys about s of construction.
            "net_triangle_other_residents_bn": triangle * (1 - s_group),
            "gross_gain_to_buyers_bn": -dw * other_earn / 1e9 + triangle,
            "cases": ";".join(c for c, spec in COST_CASES.items() if spec[2] == premium),
        })
    pd.DataFrame(incidence).to_csv(DERIVED / "supply_premium_incidence.csv", index=False)

    params = [
        ("theta_low", theta["low"], "construction labour share of gross output, 2024, 0.5 x proprietors' income [DATA: inputs_bea.csv]"),
        ("theta_central", theta["central"], "mean of construction 2024 and single-family 2017 at 0.67 x proprietors' income [CALCULATION]"),
        ("theta_high", theta["high"], "single-family residential 2017, all proprietors' income as labour [DATA: inputs_bea.csv]"),
        ("ell_hs_or_less", ell["hs_or_less"], "SCHL<=17 share of construction-industry earnings, ACS 2024 [DATA: construction_national.csv]"),
        ("ell_below_ba", ell["below_ba"], "SCHL<=20 share of construction-industry earnings, ACS 2024 [DATA: construction_national.csv]"),
        ("trades_union_earnings_share", trades_share, "union share of construction-trades earnings, ACS 2024 [DATA]"),
    ] + [(f"m_low_efficiency_share_{s}", v, "target share of the lower skill group's efficiency units, account CES [DATA: matched_benefits scenarios.csv]")
         for s, v in m.items()] \
      + [(f"dlnw_low_{s}_sigma{k}", v[0], "log lower-group wage, with minus without, account CES [DATA]")
         for s, d in wages.items() for k, v in d.items()] \
      + [(f"dlnw_high_{s}_sigma{k}", v[1], "log upper-group wage, with minus without, account CES [DATA]")
         for s, d in wages.items() for k, v in d.items()] \
      + [(f"monras_{g}_{k}", v, "Monras 2020 Table D10 col. 6 / Table 9 [SOURCE: doi:10.1086/707764]")
         for g, d in MONRAS.items() for k, v in d.items()] \
      + [(f"bratsberg_raaum_{k}", v[0], f"SE {v[1]}; CReAM DP 06/10 Tables 1 and 5 [SOURCE: doi:10.1111/j.1468-0297.2012.02540.x]")
         for k, v in BR.items()] \
      + [("bratsberg_raaum_dose", inp["br_dose"], "construction minus all-sector ln(1 + M/N), below-BA earnings, ACS 2024 [CALCULATION]"),
         ("mexico_born_low_skill_dose", dose, "Mexico-born / other low-skill employed, ACS 2024 [DATA]")]
    pd.DataFrame(params, columns=["parameter", "value", "source"]).to_csv(DERIVED / "supply_parameters.csv", index=False)
    checks = {
        "cost_changes": {c: dict(zip(("total", "A", "premium"), cost_change(c, inp))) for c in COST_CASES},
        "areas": int(len(areas)),
        "other_renter_households": float(renters),
    }
    (DERIVED / "supply_checks.json").write_text(json.dumps(checks, indent=2, default=float))
    cols = ["cost_case", "level", "geography", "dlnc", "other_renters_extra_rent_demand_only_bn",
            "other_renters_extra_rent_with_supply_bn", "offset_to_other_renters_bn",
            "offset_land_rent_part_bn", "offset_share_of_demand_only", "owner_value_offset_tn",
            "net_welfare_demand_only_bn", "net_welfare_with_supply_bn"]
    pd.set_option("display.width", 250)
    print(head[cols].round(3).to_string(index=False))
    print(pd.DataFrame(monras_rows).round(3).to_string(index=False))
    print(pd.DataFrame(incidence).round(3).to_string(index=False))
    print(json.dumps(checks, indent=1, default=float))


if __name__ == "__main__":
    main()
