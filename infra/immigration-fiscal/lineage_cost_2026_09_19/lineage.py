#!/usr/bin/env python3
"""100-year fiscal and crime account for one Mexico-born arrival's lineage,
against the same construction for one third-plus non-Hispanic white of the same age.

Period age profiles in 2024 dollars, survival-weighted, no productivity growth by
default, no behavioural response, no general equilibrium, no cohort projection.
Run: see README.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import inputs as I

LANE = Path(__file__).resolve().parent
OUT = LANE / "derived"
HORIZON = 100
CRIME_AGES = (25, 64)      # crime_cost_2026_09_16 prices per adult 25-64
PENALTY_AGES = (25, 64)    # status_impute_2026_09_16 prices per adult 25-64
FOUNDER_START_AGE = 25
GEN_LEN = 29

GROUP_BY_GEN = {1: "mexico_born", 2: "mexican_second_gen"}   # 3+ handled per arm


# --------------------------------------------------------------------- streams
def person_stream(profile: np.ndarray, table: pd.DataFrame, birth_year: int,
                  start_age: int, crime_rate: float, horizon: int = HORIZON):
    """Survival-weighted fiscal and crime flows by calendar year for one person.

    Exposure is NVSS Lx / lx[start_age], the convention in
    ledger_absolute_2026_09_17/lifetime.py; discounting is applied by the caller.
    """
    fis = np.zeros(horizon + 1)
    cri = np.zeros(horizon + 1)
    w = I.exposure(table, start_age, 100)
    for offset, age in enumerate(range(start_age, 101)):
        y = birth_year + age
        if y < 0 or y > horizon:
            continue
        fis[y] += w[offset] * profile[age]
        if CRIME_AGES[0] <= age <= CRIME_AGES[1]:
            cri[y] += w[offset] * crime_rate
    return fis, cri


def discount(stream: np.ndarray, rate: float, growth: float) -> float:
    t = np.arange(len(stream))
    return float((stream * (1.0 + growth) ** t / (1.0 + rate) ** t).sum())


# --------------------------------------------------------------------- profiles
def founder_profile(profiles, allocation, account, status, senior_rule, penalty,
                    legalise_year=None):
    """Mexico-born age profile, optionally carrying the imputed-unauthorized
    level difference over the working ages."""
    base = I.age_vector(profiles, "mexico_born", account, allocation).copy()
    if status == "mexico_born_average":
        return base, None
    adj = base.copy()
    lo, hi = PENALTY_AGES
    adj[lo:hi + 1] += penalty
    if senior_rule == "senior_zero":
        adj[65:] = 0.0
    if legalise_year is None:
        return adj, None
    # legalised at calendar year `legalise_year`: unauthorized profile until then
    switch_age = FOUNDER_START_AGE + legalise_year
    mixed = base.copy()
    mixed[:switch_age] = adj[:switch_age]
    return mixed, switch_age


def g3plus_profile(profiles, allocation, account, convergence, attr):
    """Third-plus descendants. `selfid` uses the CPS third-plus self-ID profile.
    `attrition_mixed` blends in ethnic attriters, who by the population lane retain
    only ~20% of the self-ID fiscal gap to white."""
    selfid = I.age_vector(profiles, "mexican_third_plus_selfid", account, allocation)
    if convergence == "selfid":
        return selfid
    white = I.age_vector(profiles, "third_plus_nh_white", account, allocation)
    retained = attr["attriter_retained_share_of_gap"]
    attriter = white + retained * (selfid - white)
    share = attr["attriter_share"]
    return (1.0 - share) * selfid + share * attriter


# ---------------------------------------------------------------------- lineage
def multiplier(tfr: float, attribution: str) -> float:
    """Descendants per lineage member per generation.

    `per_capita`   TFR/2 - each child is shared between two parents; the neutral
                   accounting, and the only one that conserves people.
    `maternal_full` TFR  - the founder is read as a woman and every child of a
                   lineage member is attributed whole to the lineage.
    `intermarried_half` TFR/4 - per_capita with mixed children counted half.
    """
    if attribution == "per_capita":
        return tfr / 2.0
    if attribution == "maternal_full":
        return tfr
    if attribution == "intermarried_half":
        return tfr / 4.0
    raise ValueError(f"unknown attribution rule: {attribution}")


def lineage(profiles, tables, cfg) -> dict:
    """Returns {label: (n_persons, fiscal_stream, crime_social, crime_tangible)}."""
    alloc, acct = cfg["allocation"], cfg["account"]
    tfr, attribution, gen_len = cfg["tfr"], cfg["attribution"], cfg["gen_len"]
    crime = cfg["crime"]
    mort = cfg["mortality"]

    if cfg["reference"]:
        prof_founder = I.age_vector(profiles, "third_plus_nh_white", acct, alloc)
        table_f = tables[mort["white"]]
        cr_f = crime["white"]
    else:
        prof_founder, _ = founder_profile(profiles, alloc, acct, cfg["founder_status"],
                                          cfg["senior_rule"], cfg["penalty"],
                                          cfg.get("legalise_year"))
        table_f = tables[mort["mexican"]]
        cr_f = crime["founder"]

    out = {}
    f, cs = person_stream(prof_founder, table_f, -FOUNDER_START_AGE, FOUNDER_START_AGE,
                          cr_f["social"])
    _, ct = person_stream(prof_founder, table_f, -FOUNDER_START_AGE, FOUNDER_START_AGE,
                          cr_f["tangible"])
    _, cn = person_stream(prof_founder, table_f, -FOUNDER_START_AGE, FOUNDER_START_AGE,
                          cr_f["social"] - cr_f["corrections"])
    out["G1"] = (1.0, f, cs, ct, cn, -FOUNDER_START_AGE)

    n = 1.0
    # G2 is born when the founder reaches `gen_len`; the founder is FOUNDER_START_AGE
    # in calendar year 0, so that is calendar year gen_len - FOUNDER_START_AGE.
    birth = gen_len - FOUNDER_START_AGE
    parent_group = "third_plus_nh_white" if cfg["reference"] else "mexico_born"
    gen = 2
    while birth <= HORIZON:
        n *= multiplier(tfr[parent_group], attribution)
        if cfg["reference"]:
            prof = I.age_vector(profiles, "third_plus_nh_white", acct, alloc)
            table = tables[mort["white"]]
            cr = crime["white"]
            group = "third_plus_nh_white"
        else:
            if gen == 2:
                group = "mexican_second_gen"
                prof = I.age_vector(profiles, group, acct, alloc)
            else:
                group = "mexican_third_plus_selfid"
                conv = cfg["convergence"] if gen >= 4 else "selfid"
                prof = g3plus_profile(profiles, alloc, acct, conv, cfg["attr"])
            table = tables[mort["mexican"]]
            cr = crime["descendant"]
        f, cs = person_stream(prof, table, birth, 0, cr["social"])
        _, ct = person_stream(prof, table, birth, 0, cr["tangible"])
        _, cn = person_stream(prof, table, birth, 0, cr["social"] - cr["corrections"])
        out[f"G{gen}"] = (n, n * f, n * cs, n * ct, n * cn, birth)
        parent_group = group
        birth += gen_len
        gen += 1
    return out


def summarise(L: dict, rate: float, growth: float) -> dict:
    tot = sum(v[1] for v in L.values())
    cs = sum(v[2] for v in L.values())
    ct = sum(v[3] for v in L.values())
    cn = sum(v[4] for v in L.values())
    return {"persons": float(sum(v[0] for v in L.values())),
            "founder_lifetime": discount(L["G1"][1], rate, growth),
            "lineage_fiscal": discount(tot, rate, growth),
            "crime_social": discount(cs, rate, growth),
            "crime_tangible": discount(ct, rate, growth),
            "crime_social_net_corrections": discount(cn, rate, growth)}


# ------------------------------------------------------------------- oracle check
def oracle_period_profiles(profiles, tables) -> pd.DataFrame:
    """Reproduce ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv with
    this lane's own stream machinery. A byte-level agreement there proves the age
    vector, the Lx exposure and the discounting all match the producing lane."""
    stored = pd.read_csv(I.P_ABS_LIFETIME)
    rows = []
    for _, r in stored.iterrows():
        last = 100 if r.horizon == "full_100plus" else 82
        prof = I.age_vector(profiles, r.group, r.account, r.allocation)
        tab = tables[r.mortality_table]
        ages = np.arange(r.start_age, last + 1)
        w = I.exposure(tab, int(r.start_age), last) * (1.0 + r.real_discount_rate) ** -(ages - r.start_age)
        mine = float(prof[r.start_age:last + 1] @ w)
        rows.append({"allocation": r.allocation, "account": r.account, "group": r.group,
                     "survival": r.survival, "horizon": r.horizon, "start_age": r.start_age,
                     "real_discount_rate": r.real_discount_rate,
                     "stored_npv": r.period_profile_npv, "recomputed_npv": mine,
                     "abs_diff": abs(mine - r.period_profile_npv)})
    return pd.DataFrame(rows)


def oracle_pronatal(profiles, tables) -> pd.DataFrame:
    """Independently locate the pronatal lane's lifetime balances in this lane's grid."""
    stored = pd.read_csv(I.P_PRONATAL)
    rows = []
    for _, r in stored.iterrows():
        best = None
        for alloc in ("shared", "personal"):
            for acct in ("partial", "expanded"):
                for mkey in ("total", "hispanic", "nh_white"):
                    for last in (100, 82):
                        prof = I.age_vector(profiles, r.group, acct, alloc)
                        ages = np.arange(r.start_age, last + 1)
                        w = I.exposure(tables[mkey], int(r.start_age), last) * (1.0 + r.rate) ** -(ages - r.start_age)
                        mine = float(prof[r.start_age:last + 1] @ w)
                        d = abs(mine - r.lifetime_balance)
                        if best is None or d < best["abs_diff"]:
                            best = {"allocation": alloc, "account": acct, "mortality_table": mkey,
                                    "last_age": last, "recomputed": mine, "abs_diff": d}
        rows.append({"group": r.group, "start_age": r.start_age, "rate": r.rate,
                     "stored_lifetime_balance": r.lifetime_balance, **best})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------- main
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    profiles = I.age_profiles()
    tables = I.survival()
    fert = I.fertility()
    pen = I.unauthorized_penalty()["penalty_per_adult_year"]
    crime = I.crime_rates()
    attr = I.attrition()

    checks = [I.check_shared_partial_equals_all_age_shared(profiles)]
    orc = oracle_period_profiles(profiles, tables)
    orc.to_csv(OUT / "oracle_period_profiles.csv", index=False)
    worst = float(orc.abs_diff.max())
    checks.append({"check": "reproduce ledger_absolute lifetime/period_profiles.csv",
                   "rows": int(len(orc)), "max_abs_diff_usd": worst, "pass": bool(worst < 1e-6)})
    if worst >= 1e-6:
        raise SystemExit(f"[BLOCKED] founder machinery does not reproduce the lane oracle: {worst}")
    pro = oracle_pronatal(profiles, tables)
    pro.to_csv(OUT / "oracle_pronatal.csv", index=False)
    checks.append({"check": "locate pronatal_equivalence lifetime balances",
                   "max_abs_diff_usd": float(pro.abs_diff.max()),
                   "identified_grid": sorted({f"{a}/{b}/{c}/last{int(d)}" for a, b, c, d in
                                              zip(pro.allocation, pro.account,
                                                  pro.mortality_table, pro.last_age)})})
    print(f"[oracle] period_profiles reproduced, max |diff| = {worst:.3e} USD over {len(orc)} rows")

    common = {"total": "total", "mexican": "total", "white": "total"}
    group_specific = {"mexican": "hispanic", "white": "nh_white"}

    crime_routes = {
        "A1_bjs_stock": {"founder": crime["A1_bjs_stock"]["mexican"],
                         "descendant": crime["A1_bjs_stock"]["mexican"],
                         "white": crime["A1_bjs_stock"]["white"]},
        "A2_acs_stock": {"founder": crime["A2_acs_stock"]["mexican"],
                         "descendant": crime["A2_acs_stock"]["mexican"],
                         "white": crime["A2_acs_stock"]["white"]},
        "status_founder": {"founder": crime["status_texas_arrests"]["undocumented"],
                           "descendant": crime["A1_bjs_stock"]["mexican"],
                           "white": crime["A1_bjs_stock"]["white"]},
    }

    def run(cfg_over: dict, rate: float, growth: float, crime_route: str) -> dict:
        base = {"allocation": "personal", "account": "expanded", "gen_len": GEN_LEN,
                "attribution": "per_capita", "founder_status": "unauthorized",
                "senior_rule": "senior_full", "convergence": "selfid",
                "mortality": {"mexican": "total", "white": "total"},
                "penalty": pen, "attr": attr, "reference": False,
                "crime": crime_routes[crime_route]}
        cfg = {**base, **cfg_over}
        mex = summarise(lineage(profiles, tables, cfg), rate, growth)
        wcfg = {**cfg, "reference": True}
        wht = summarise(lineage(profiles, tables, wcfg), rate, growth)
        row = {k: v for k, v in cfg.items()
               if k in ("allocation", "account", "founder_status", "senior_rule",
                        "convergence", "attribution", "gen_len")}
        row["fertility"] = cfg["fertility_label"]
        row["mortality"] = f"{cfg['mortality']['mexican']}/{cfg['mortality']['white']}"
        row["crime_route"] = crime_route
        row["real_growth"] = growth
        row["discount"] = rate
        row.update({f"mex_{k}": v for k, v in mex.items()})
        row.update({f"white_{k}": v for k, v in wht.items()})
        row["gap_lineage_fiscal"] = mex["lineage_fiscal"] - wht["lineage_fiscal"]
        row["gap_founder_lifetime"] = mex["founder_lifetime"] - wht["founder_lifetime"]
        row["gap_crime_social"] = mex["crime_social"] - wht["crime_social"]
        row["gap_crime_tangible"] = mex["crime_tangible"] - wht["crime_tangible"]
        row["gap_crime_social_net_corrections"] = (mex["crime_social_net_corrections"]
                                                   - wht["crime_social_net_corrections"])
        row["lineage_fiscal_per_year"] = mex["lineage_fiscal"] / HORIZON
        row["gap_lineage_per_year"] = row["gap_lineage_fiscal"] / HORIZON
        return row

    # ------------------------------------------------------------ arm 1: main grid
    rows = []
    for alloc in ("personal", "shared"):
        for acct in ("expanded", "partial"):
            for status in ("unauthorized", "mexico_born_average"):
                for flabel in ("low_cps2025", "high_nvsr2010"):
                    for attribution in ("per_capita", "maternal_full", "intermarried_half"):
                        for rate in (0.0, 0.03):
                            rows.append(run({"allocation": alloc, "account": acct,
                                             "founder_status": status,
                                             "tfr": fert[flabel], "fertility_label": flabel,
                                             "attribution": attribution},
                                            rate, 0.0, "A1_bjs_stock"))
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "lineage_table.csv", index=False)
    print(f"[written] lineage_table.csv ({len(table)} rows)")

    # -------------------------------------------------- generation breakdown (central)
    central = {"tfr": fert["low_cps2025"], "fertility_label": "low_cps2025"}
    brows = []
    for label, reference in (("mexican_lineage", False), ("white_reference", True)):
        cfg = {"allocation": "personal", "account": "expanded", "gen_len": GEN_LEN,
               "attribution": "per_capita", "founder_status": "unauthorized",
               "senior_rule": "senior_full", "convergence": "selfid",
               "mortality": {"mexican": "total", "white": "total"},
               "penalty": pen, "attr": attr, "reference": reference,
               "crime": crime_routes["A1_bjs_stock"], **central}
        L = lineage(profiles, tables, cfg)
        for gen, (n, f, cs, ct, cn, birth) in L.items():
            brows.append({"lineage": label, "generation": gen, "persons": n,
                          "birth_year_calendar": birth,
                          "fiscal_undiscounted": discount(f, 0.0, 0.0),
                          "fiscal_pv3": discount(f, 0.03, 0.0),
                          "crime_social_undiscounted": discount(cs, 0.0, 0.0),
                          "crime_tangible_undiscounted": discount(ct, 0.0, 0.0),
                          "crime_social_net_corrections_undiscounted": discount(cn, 0.0, 0.0)})
    pd.DataFrame(brows).to_csv(OUT / "generation_breakdown.csv", index=False)
    print("[written] generation_breakdown.csv")

    # ------------------------------------------------------------ white reference file
    wrows = []
    for acct in ("expanded", "partial"):
        for alloc in ("personal", "shared"):
            for flabel in ("low_cps2025", "high_nvsr2010"):
                for attribution in ("per_capita", "maternal_full", "intermarried_half"):
                    for rate in (0.0, 0.03):
                        cfg = {"allocation": alloc, "account": acct, "gen_len": GEN_LEN,
                               "attribution": attribution, "founder_status": "unauthorized",
                               "senior_rule": "senior_full", "convergence": "selfid",
                               "mortality": {"mexican": "total", "white": "total"},
                               "penalty": pen, "attr": attr, "reference": True,
                               "crime": crime_routes["A1_bjs_stock"],
                               "tfr": fert[flabel], "fertility_label": flabel}
                        s = summarise(lineage(profiles, tables, cfg), rate, 0.0)
                        wrows.append({"allocation": alloc, "account": acct, "fertility": flabel,
                                      "attribution": attribution, "discount": rate, **s})
    pd.DataFrame(wrows).to_csv(OUT / "white_reference.csv", index=False)
    print("[written] white_reference.csv")

    # ------------------------------------------------------------------ sensitivities
    srows = []

    def sens(name: str, over: dict, rate=0.0, growth=0.0, route="A1_bjs_stock"):
        r = run({**central, **over}, rate, growth, route)
        r["sensitivity"] = name
        srows.append(r)

    sens("central (personal/expanded, unauthorized, per-capita, low fertility, 0%)", {})
    sens("central at 3%", {}, rate=0.03)
    sens("2a G4+ attrition-corrected mixed profile", {"convergence": "attrition_mixed"})
    sens("2b founder legalised at year 10", {"legalise_year": 10})
    sens("2c G2 fertility at white TFR", {"tfr": {**fert["low_cps2025"],
                                                  "mexican_second_gen": fert["low_cps2025"]["third_plus_nh_white"],
                                                  "mexican_third_plus_selfid": fert["low_cps2025"]["third_plus_nh_white"]}})
    sens("senior rule: unauthorized 65+ balance set to zero", {"senior_rule": "senior_zero"})
    sens("founder status: Mexico-born average", {"founder_status": "mexico_born_average"})
    sens("generation length 26", {"gen_len": 26})
    sens("generation length 32", {"gen_len": 32})
    sens("group-specific mortality (Hispanic / NH white)",
         {"mortality": {"mexican": "hispanic", "white": "nh_white"}})
    sens("1% real growth in taxes and outlays", {}, growth=0.01)
    sens("1% real growth, 3% discount", {}, rate=0.03, growth=0.01)
    sens("account: main partial (all_age_shared)", {"allocation": "shared", "account": "partial"})
    sens("allocation: shared, expanded", {"allocation": "shared", "account": "expanded"})
    sens("high fertility (NVSR 2010 levels)", {"tfr": fert["high_nvsr2010"],
                                               "fertility_label": "high_nvsr2010"})
    sens("attribution: maternal full", {"attribution": "maternal_full"})
    sens("attribution: intermarried half", {"attribution": "intermarried_half"})
    sens("crime route A2 (ACS institutional stock)", {}, route="A2_acs_stock")
    sens("crime route: founder priced at Texas undocumented arrest rate", {}, route="status_founder")
    sd = pd.DataFrame(srows)
    front = ["sensitivity", "gap_lineage_fiscal", "mex_lineage_fiscal", "white_lineage_fiscal",
             "gap_founder_lifetime", "mex_persons", "white_persons",
             "gap_crime_social", "gap_crime_social_net_corrections",
             "mex_crime_social", "white_crime_social"]
    sd = sd[front + [c for c in sd.columns if c not in front]]
    sd.to_csv(OUT / "sensitivities.csv", index=False)
    print("[written] sensitivities.csv")

    # --------------------------------------------------------------------- manifest
    meta = {"lane": "lineage_cost_2026_09_19", "price_year": 2024, "horizon_years": HORIZON,
            "founder_start_age": FOUNDER_START_AGE, "generation_length_central": GEN_LEN,
            "inputs_sha256": I.manifest(),
            "fertility": fert, "unauthorized_penalty": I.unauthorized_penalty(),
            "crime_rates": crime, "attrition": attr, "checks": checks,
            "interpretation": ("survival-weighted period-profile lineage scenario; not a cohort "
                               "projection, not an admission-policy counterfactual, no general "
                               "equilibrium, no behavioural response, no wage growth by default"),
            "crime_line": ("reported separately from the fiscal line; the corrections component "
                           "is already inside the expanded fiscal account, so the incremental "
                           "crime cost is social minus corrections")}
    (OUT / "audit.json").write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
    print("[written] audit.json")

    c = sd[sd.sensitivity.str.startswith("central (")].iloc[0]
    print(f"\ncentral: lineage {c.mex_lineage_fiscal:,.0f}  white {c.white_lineage_fiscal:,.0f}  "
          f"gap {c.gap_lineage_fiscal:,.0f}  persons {c.mex_persons:.2f}/{c.white_persons:.2f}")


if __name__ == "__main__":
    main()
