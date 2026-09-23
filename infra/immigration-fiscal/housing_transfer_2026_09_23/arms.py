"""Rent and home-value transfers from the Mexican-origin group's presence, by arm.

Frame (brief, not changed): the complete annual account's stationary comparison of 2024 with
and without the 40.896574m CPS Mexican-origin residents, effects on all other residents.
Higher rents move money from renters to landlords; the net for other residents is the extra
rent the group pays to landlords who are other residents, less the extra rent other renters
pay to landlords outside that set (the group itself, foreign owners). Owners' home-value gain
is a stock and is never added to the annual flow.

Rent effect of the group's presence, as a share of today's (with-group) rent:
  population without the group N0 = N (1 - s), where s is the group's population share;
  rent path along the arrival of the group, lambda in [0, 1]: N(lambda) = N0 (1 + lambda g),
  g = s / (1 - s); P(lambda)/P(0) under four forms of the per-point elasticity e (rent
  elasticity with respect to population, the per-1%-of-population coefficient of the
  literature):
    A constant elasticity   (1 + lambda g)^e                       [central]
    B linear in the inflow  1 + e lambda g                          (Saiz-style per-point, linear)
    C semi-log in inflow    exp(e lambda g)
    D support-limited       arm elasticity on the first 3 points of population, the long-run
                            land elasticity beyond them (the per-point estimates come from
                            inflows of 0-5 points; a 12-point, or locally 40-point, stock lies
                            outside that support)
  f = 1 - P(0)/P(1) is the share of today's rent due to the group.
Arms: short run (no supply response) e in {1.0, 1.5, 2.0}; long run (supply of structures
adjusts, the rent effect is land scarcity) e = a / (1 - a (1 - eD)) for land cost share a and
housing demand elasticity eD, {0.25, 0.39, 0.60}. Geography: metro-local (each 2013 CBSA at
its own group share; non-metro remainder by state) or national-uniform (12.02% everywhere).

Two readings of the net for other residents:
  frame (rectangle): (1 - leak_g) dR_g - leak_o dR_o, dR = f x current contract rent;
  welfare (integral): other renters also lose the housing they give up (short run) or the
    landowners' gain accrues along the path (long run), so the group's contribution is
    kappa dR_g, kappa = [P(1) - mean P] / [P(1) - P(0)], about one half:
    short run  (kappa - leak_g) dR_g - leak_o dR_o
    long run   (1 - leak_g) kappa dR_g - leak_o dR_o
  where leak_o = group + foreign share of the ownership of other-occupied rentals and leak_g
  the same for group-occupied rentals.

Outputs: derived/cbsa_exposure.csv, derived/arms_grid.csv, derived/arms_headline.csv,
derived/parameters.csv, derived/checks.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/arms.py
"""
from __future__ import annotations

import itertools
import json
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
XWALK = ROOT / "infra/immigration-fiscal/employment_entry_2026_09_18/_cache/xwalk_puma22.csv"
COUNTY_CBSA = ROOT / "infra/immigration-fiscal/hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv"
METRO_PANEL = ROOT / "infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/derived/metro_housing_panel.csv"
CA_TX_PANEL = ROOT / "infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/derived/metro_panel.csv"

TARGET = 40.896574e6        # CPS ASEC 2025 union, complete account
RESIDENTS = 340.110988e6    # complete-account denominator (= ACS 2024 B01003)
SUPPORT = 0.03              # population share covered by the per-point estimates
LAMBDA = np.linspace(0, 1, 401)

LAND = {"low": 0.25, "central": 0.35, "high": 0.46}
DEMAND = {"low": 1.0, "central": 0.7, "high": 0.5}   # high demand elasticity -> low effect
ARMS = {
    "short_run": {"low": 1.0, "central": 1.5, "high": 2.0},
    "long_run": {k: LAND[k] / (1 - LAND[k] * (1 - DEMAND[k])) for k in LAND},
}
# Ownership of rental units outside the beneficiary set (group and foreign owners).
OWN = {
    "low": {"group_of_other": 0.010, "group_of_group": 0.02, "foreign": 0.007},
    "central": {"group_of_other": 0.020, "group_of_group": 0.05, "foreign": 0.015},
    "high": {"group_of_other": 0.030, "group_of_group": 0.10, "foreign": 0.030},
}
PARAMETERS = [
    ("s_national", TARGET / RESIDENTS, "CPS union 40.896574m / ACS 2024 residents 340.110988m [DATA]"),
    ("support_share", SUPPORT, "per-point estimates come from inflows of about 1-5% of population "
     "(Saiz annual ~1%, Wilson-Zhou weighted mean 3.1% of employment ~2.3% of population, "
     "ladder 183 mean +2.17 points) [SOURCE: lanes cited in RESULT.md]"),
    ("e_short_run_low", 1.0, "Saiz 2007 rents ~1 per inflow of 1% of population (as reported by "
     "Wilson-Zhou p.44 and the Sep 16 housing lane); Monras author rescaling ~1 [SOURCE]"),
    ("e_short_run_central", 1.5, "midpoint of the two short-horizon anchors; = 1/eD at eD 0.67 [ASSUMPTION]"),
    ("e_short_run_high", 2.0, "Wilson-Zhou 1.438 per 1% of employment in worker flow = 1.79-1.90 per "
     "1% of population on covered employment, 2.1-2.2 on private (derived/inputs_wz.csv); "
     "Cabral-Steingress ~2 as reported by Wilson-Zhou [CALCULATION/SOURCE]"),
    ("e_repo_decade", 1.4 / 1.125, "ladder 183 ancestry IV +1.4% per point of foreign-born share "
     "(SE 1.4) / 1.125 (dlnN = ds/(1-s), s = 0.111 in 2000); CI spans both arms [CALCULATION]"),
    ("land_share_low", LAND["low"], "Z.1 2019Q4 owner-occupied land share of value 0.35 net of "
     "structure depreciation in the rent (user-cost) share [CALCULATION/ASSUMPTION]"),
    ("land_share_central", LAND["central"], "Z.1 2024Q4 owner-occupied land share of value 0.405, "
     "rent share with 2% structure depreciation at a 5% return about 0.34 [CALCULATION]"),
    ("land_share_high", LAND["high"], "Z.1 2024Q4 noncorporate residential land share of value 0.461 [DATA]"),
    ("demand_elasticity_low_effect", DEMAND["low"], "housing demand elasticity 1.0 [ASSUMPTION, as ladder 180]"),
    ("demand_elasticity_central", DEMAND["central"], "0.7 [ASSUMPTION, as ladder 180]"),
    ("demand_elasticity_high_effect", DEMAND["high"], "0.5 [ASSUMPTION, as ladder 180]"),
    ("own_group_of_other_central", OWN["central"]["group_of_other"], "SCF 2022 Hispanic share of "
     "other residential real estate 2.9% x Mexican-origin share of Hispanic householders 55% = "
     "1.6%; ACS group share of interest/dividend/rental income 2.2%; group share of on-site "
     "owners of 2-4 unit buildings 6.0% [CALCULATION]"),
    ("own_group_of_group_central", OWN["central"]["group_of_group"], "co-ethnic landlords of the "
     "group's own rentals: unmeasured; 2-10% range [ASSUMPTION]"),
    ("own_foreign_central", OWN["central"]["foreign"], "Z.1 foreign direct investment in "
     "noncorporate real estate 0.7% of its value (2024Q4), plus foreign holdings of corporate and "
     "REIT landlords, unmeasured; 0.7-3% [DATA/ASSUMPTION]"),
    ("rhfs_2024_units_by_entity", np.nan, "RHFS 2024 PUF, share of reported rental units: individual "
     "investors 35.4%, trustee 4.2%, general partnership/tenants in common 1.7%, LLP/LP/LLC 48.3%, "
     "REIT 1.5%, real estate corporation 3.4%, nonprofit/cooperative/other institution 5.5% "
     "(derived/inputs_rhfs.csv); institutions are counted through their beneficial owners [DATA]"),
]


def load_areas():
    if not XWALK.exists():
        raise SystemExit(f"[BLOCKED] missing {XWALK}; run employment_entry_2026_09_18/fetch_crosswalks.py")
    cells = pd.read_csv(DERIVED / "pums_puma_cells.csv", dtype={"STATE": str, "PUMA": str})
    xw = pd.read_csv(XWALK, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(COUNTY_CBSA, dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa", "cbsa_title"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    merged = cells.merge(alloc, left_on=["STATE", "PUMA"], right_on=["state", "puma"], how="left",
                         validate="one_to_many")
    if merged["area"].isna().any():
        raise ValueError(f"PUMAs without crosswalk rows: {merged[merged.area.isna()][['STATE','PUMA']].head()}")
    value_cols = [c for c in cells.columns if c not in ("STATE", "PUMA")]
    for c in value_cols:
        merged[c] = merged[c] * merged["afact"]
    areas = merged.groupby("area")[value_cols].sum()
    for c in value_cols:  # allocation must preserve every national total
        if not np.isclose(areas[c].sum(), cells[c].sum(), rtol=1e-9):
            raise ValueError(f"allocation lost {c}")
    titles = xw.dropna(subset=["cbsa"]).drop_duplicates("cbsa").set_index("cbsa")["cbsa_title"]
    out = pd.DataFrame({
        "persons": areas["persons"],
        "group_persons_acs": areas["grp_persons"],
        "other_renter_rent": areas["other_renter_contract_rent_annual"],
        "group_renter_rent": areas["group_renter_contract_rent_annual"],
        "other_renter_gross_rent": areas["other_renter_gross_rent_annual"],
        "group_renter_gross_rent": areas["group_renter_gross_rent_annual"],
        "other_renter_households": areas["other_renter_households"],
        "group_renter_households": areas["group_renter_households"],
        "other_owner_value": areas["other_owner_owner_value"],
        "group_owner_value": areas["group_owner_owner_value"],
        "other_owner_households": areas["other_owner_households"],
    })
    out["title"] = out.index.map(titles)
    scale = TARGET / out["group_persons_acs"].sum()
    out["group_share"] = (scale * out["group_persons_acs"] / out["persons"]).clip(upper=0.95)
    panel = pd.read_csv(METRO_PANEL, dtype={"cbsa": str})[["cbsa", "elasticity"]]
    out = out.join(panel.set_index("cbsa")["elasticity"].rename("saiz_elasticity"))
    # The causal lane's code match misses Los Angeles; fill unmatched metros by exact title
    # from the California-Texas lane's name-matched panel (2023 CBSA titles).
    ca_tx = pd.read_csv(CA_TX_PANEL)
    ca_tx["title"] = ca_tx["cbsa_2023"].str.replace(" Metro Area", "", regex=False)
    by_title = ca_tx.drop_duplicates("title").set_index("title")["elasticity"]
    fill = out["title"].map(by_title)
    out["saiz_source"] = np.where(out["saiz_elasticity"].notna(), "causal_lane_code",
                                  np.where(fill.notna(), "ca_tx_lane_title", "none"))
    out["saiz_elasticity"] = out["saiz_elasticity"].fillna(fill)
    return out.reset_index().rename(columns={"index": "area"}), scale


def path(form, e, s, e_lr=None):
    """P(lambda)/P(0) on the LAMBDA grid; s is an array of population shares."""
    g = (s / (1 - s))[:, None]
    lam = LAMBDA[None, :]
    if form == "A":
        return (1 + lam * g) ** e
    if form == "B":
        return 1 + e * lam * g
    if form == "C":
        return np.exp(e * lam * g)
    if form == "D":
        log_n = np.log1p(lam * g)
        cap = -np.log1p(-SUPPORT)
        return np.exp(e * np.minimum(log_n, cap) + e_lr * np.maximum(log_n - cap, 0))
    raise ValueError(form)


def effect(form, e, s, e_lr=None):
    p = path(form, np.asarray(e)[:, None] if np.ndim(e) else e, s, e_lr)
    f = 1 - p[:, 0] / p[:, -1]
    mean_p = np.trapezoid(p, LAMBDA, axis=1)
    rise = p[:, -1] - p[:, 0]
    # kappa -> 1/2 as the rise -> 0 (areas with no group members).
    kappa = np.where(rise > 1e-12, (p[:, -1] - mean_p) / np.where(rise > 1e-12, rise, 1), 0.5)
    return f, kappa


def evaluate(areas, arm, level, form, geography, own, e_override=None):
    e = ARMS[arm][level] if e_override is None else e_override
    s = areas["group_share"].to_numpy() if geography == "metro_local" else np.full(
        len(areas), TARGET / RESIDENTS)
    if isinstance(e, np.ndarray):
        f, kappa = effect(form, e, s)
    else:
        f, kappa = effect(form, e, s, ARMS["long_run"]["central"] if form == "D" else None)
    d_other = (f * areas["other_renter_rent"]).sum()
    d_group = (f * areas["group_renter_rent"]).sum()
    kappa_g = (kappa * f * areas["group_renter_rent"]).sum() / d_group
    o = OWN[own]
    leak_o, leak_g = o["group_of_other"] + o["foreign"], o["group_of_group"] + o["foreign"]
    frame_net = (1 - leak_g) * d_group - leak_o * d_other
    if arm == "short_run":
        # Fixed stock: landlords gain on the whole stock; other renters also give up the units
        # the group occupies, valued between the old and new rent.
        renters_welfare_loss = d_other + (1 - kappa_g) * d_group
        owners_welfare_gain = d_other + d_group
        welfare_net = (kappa_g - leak_g) * d_group - leak_o * d_other
    else:
        # Land scarcity: landowners' gain is the integral of total housing over the rent path;
        # other renters' own reduced consumption enters only through leak_o (second order).
        renters_welfare_loss = d_other
        owners_welfare_gain = d_other + kappa_g * d_group
        welfare_net = (1 - leak_g) * kappa_g * d_group - leak_o * d_other
    renters_o = areas["other_renter_households"].sum()
    return {
        "arm": arm, "level": level, "elasticity": e if np.isscalar(e) else np.nan, "form": form,
        "geography": geography, "ownership": own, "leak_other_occupied": leak_o,
        "leak_group_occupied": leak_g,
        "other_renters_extra_rent_bn": d_other / 1e9,
        "other_renters_share_of_rent": d_other / areas["other_renter_rent"].sum(),
        "group_renters_extra_rent_bn": d_group / 1e9,
        "landlord_gain_from_other_renters_to_others_bn": (1 - leak_o) * d_other / 1e9,
        "landlord_gain_from_other_renters_leaked_bn": leak_o * d_other / 1e9,
        "landlord_gain_from_group_to_others_bn": (1 - leak_g) * d_group / 1e9,
        "landlord_gain_from_group_leaked_bn": leak_g * d_group / 1e9,
        "net_other_residents_frame_bn": frame_net / 1e9,
        "kappa_group": kappa_g,
        "other_renters_welfare_loss_bn": renters_welfare_loss / 1e9,
        "landlords_welfare_gain_all_owners_bn": owners_welfare_gain / 1e9,
        "net_other_residents_welfare_bn": welfare_net / 1e9,
        "other_owner_value_gain_stock_bn": (f * areas["other_owner_value"]).sum() / 1e9,
        "group_owner_value_gain_stock_bn": (f * areas["group_owner_value"]).sum() / 1e9,
        "extra_rent_per_other_renter_household": d_other / renters_o,
    }


def national_rules(arm, level, form, own):
    """National-uniform application to each household rule's totals."""
    tab = pd.read_csv(DERIVED / "pums_tabulation.csv")
    rows = []
    for rule in ("householder", "any_member", "person_share", "householder_hisp02"):
        t = tab[(tab.rule == rule) & (tab.tenure == "renter")]
        v = tab[(tab.rule == rule) & (tab.tenure == "owner") & (tab.variable == "owner_value")]
        get = lambda g, var: float(t[(t.group == g) & (t.variable == var)].estimate.iloc[0])
        areas = pd.DataFrame({
            "group_share": [TARGET / RESIDENTS],
            "other_renter_rent": [get("other", "contract_rent_annual")],
            "group_renter_rent": [get("group", "contract_rent_annual")],
            "other_renter_households": [get("other", "households")],
            "other_owner_value": [float(v[v.group == "other"].estimate.iloc[0])],
            "group_owner_value": [float(v[v.group == "group"].estimate.iloc[0])]})
        row = evaluate(areas, arm, level, form, "national_uniform", own)
        row["rule"] = rule
        rows.append(row)
    return rows


def native_per_household(areas, arm, level):
    """Per renter household with a US-born householder outside the group, householder rule."""
    tab = pd.read_csv(DERIVED / "pums_tabulation.csv")
    t = tab[(tab.rule == "householder") & (tab.group == "other_native_head") & (tab.tenure == "renter")]
    rent = float(t[t.variable == "contract_rent_annual"].estimate.iloc[0])
    households = float(t[t.variable == "households"].estimate.iloc[0])
    out = {}
    for geography in ("metro_local", "national_uniform"):
        r = evaluate(areas, arm, level, "A", geography, "central")
        # Native-born renters are assumed to face the other-renter average local effect.
        out[geography] = r["other_renters_share_of_rent"] * rent / households
    return out, households, rent


def main():
    areas, scale = load_areas()
    areas.to_csv(DERIVED / "cbsa_exposure.csv", index=False)
    pd.DataFrame(PARAMETERS, columns=["parameter", "value", "source"]).to_csv(
        DERIVED / "parameters.csv", index=False)
    grid = []
    for arm, level, form, geography, own in itertools.product(
            ARMS, ("low", "central", "high"), "ABCD", ("metro_local", "national_uniform"), OWN):
        if arm == "long_run" and form == "D":
            continue
        row = evaluate(areas, arm, level, form, geography, own)
        row["rule"] = "householder"
        grid.append(row)
    for arm, level in itertools.product(ARMS, ("low", "central", "high")):
        grid.extend(national_rules(arm, level, "A", "central"))
    # Long run with each metro at its own Saiz (2010) elasticity, 1/(eS + eD), eD central;
    # unmatched areas take the rent-weighted mean of the matched ones.
    saiz = areas["saiz_elasticity"]
    local_e = 1 / (saiz + DEMAND["central"])
    w = areas["other_renter_rent"].where(saiz.notna())
    fill = float((local_e * w).sum() / w.sum())
    local_e = local_e.fillna(fill).to_numpy()
    for geography in ("metro_local", "national_uniform"):
        row = evaluate(areas, "long_run", "saiz_local", "A", geography, "central", e_override=local_e)
        row["rule"] = "householder"
        row["elasticity"] = fill
        grid.append(row)
    # Repo's own decade estimate (ladder 183), per 1% of population.
    for geography in ("metro_local", "national_uniform"):
        e183 = 1.4 / 1.125
        row = evaluate(areas, "short_run", "ladder183_decade", "A", geography, "central", e_override=e183)
        row["rule"] = "householder"
        row["arm"] = "decade_repo"
        grid.append(row)
    grid = pd.DataFrame(grid)
    grid.to_csv(DERIVED / "arms_grid.csv", index=False)
    head = grid[(grid.form == "A") & (grid.rule == "householder") & (grid.ownership == "central")
                & grid.level.isin(["low", "central", "high"]) & grid.arm.isin(ARMS)]
    head.to_csv(DERIVED / "arms_headline.csv", index=False)
    # Ranges per arm over elasticity level, functional forms A-C, ownership and geography
    # (householder rule); the support-limited form D is reported separately.
    metrics = ["other_renters_extra_rent_bn", "group_renters_extra_rent_bn",
               "landlord_gain_from_other_renters_to_others_bn",
               "landlord_gain_from_group_to_others_bn", "net_other_residents_frame_bn",
               "net_other_residents_welfare_bn", "other_owner_value_gain_stock_bn",
               "extra_rent_per_other_renter_household"]
    summary = []
    for arm in ARMS:
        core = grid[(grid.arm == arm) & (grid.rule == "householder")
                    & grid.level.isin(["low", "central", "high"])]
        for metric in metrics:
            row = {"arm": arm, "metric": metric}
            for geography in ("national_uniform", "metro_local"):
                c = core[(core.level == "central") & (core.form == "A") & (core.ownership == "central")
                         & (core.geography == geography)]
                row[f"central_{geography}"] = float(c[metric].iloc[0])
            abc = core[core.form.isin(list("ABC"))]
            row["min_ABC"], row["max_ABC"] = float(abc[metric].min()), float(abc[metric].max())
            d = core[(core.form == "D") & (core.level == "central") & (core.ownership == "central")]
            row["central_formD_uniform_local"] = (
                "; ".join(f"{v:.2f}" for v in d.sort_values("geography", ascending=False)[metric])
                if len(d) else "")
            summary.append(row)
    pd.DataFrame(summary).to_csv(DERIVED / "arms_summary.csv", index=False)

    exposure = {}
    for base in ("other_renter_rent", "group_renter_rent", "other_owner_value", "persons"):
        exposure[base] = float((areas["group_share"] * areas[base]).sum() / areas[base].sum())
    natives = {f"{arm}_{level}": native_per_household(areas, arm, level)[0]
               for arm in ARMS for level in ("low", "central", "high")}
    # Common leak share (group + foreign owners of all rentals) at which the net is zero.
    breakeven = {}
    for arm, geography in itertools.product(ARMS, ("national_uniform", "metro_local")):
        r = head[(head.arm == arm) & (head.level == "central") & (head.geography == geography)].iloc[0]
        dg, do, k = (r.group_renters_extra_rent_bn, r.other_renters_extra_rent_bn, r.kappa_group)
        breakeven[f"{arm}_{geography}"] = {
            "frame": dg / (dg + do),
            "welfare": k * dg / (do + dg) if arm == "short_run" else k * dg / (do + k * dg)}
    checks = {
        "group_scale_cps_over_acs": scale, "areas": int(len(areas)),
        "metro_areas": int(areas["area"].str.match(r"^\d").sum()),
        "saiz_matched_areas": int(areas["saiz_elasticity"].notna().sum()),
        "saiz_matched_share_of_other_rent": float(areas.loc[areas.saiz_elasticity.notna(), "other_renter_rent"].sum()
                                                  / areas["other_renter_rent"].sum()),
        "saiz_local_long_run_fill_elasticity": fill,
        "exposure_mean_group_share_weighted_by": exposure,
        "long_run_elasticities": ARMS["long_run"],
        "native_head_renters": native_per_household(areas, "short_run", "central")[1:],
        "extra_rent_per_native_head_renter_household": natives,
        "breakeven_common_leak_share": breakeven,
    }
    (DERIVED / "checks.json").write_text(json.dumps(checks, indent=2, default=float))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    cols = ["arm", "level", "elasticity", "geography", "other_renters_extra_rent_bn",
            "group_renters_extra_rent_bn", "net_other_residents_frame_bn",
            "net_other_residents_welfare_bn", "kappa_group", "other_owner_value_gain_stock_bn",
            "extra_rent_per_other_renter_household"]
    print(head[cols].round(3).to_string(index=False))
    print(json.dumps(checks, indent=1, default=float))


if __name__ == "__main__":
    main()
