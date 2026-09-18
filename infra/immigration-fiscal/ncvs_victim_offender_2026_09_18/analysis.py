#!/usr/bin/env python3
"""Victim x offender ethnicity of non-fatal violent crime, and its cost.

Inputs: everything build.py wrote under derived/.
Outputs: the matrices, rates, offence-mix cost weights and disconfirmation arms
named in the lane brief, all under derived/.

Run:
  cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 analysis.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)

FAILS: list[str] = []
_lines: list[str] = []


def say(s: str = "") -> None:
    print(s)
    _lines.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"  {'✓' if ok else '✗'} [{name}] {detail}")
    if not ok:
        FAILS.append(name)


def header(s: str) -> None:
    say()
    say(f"[{s}]")


GROUPS = ["White", "Black", "Hispanic", "Other"]
OFF_COLS = ["White", "Black", "Hispanic", "Other", "Unknown"]
KNOWN = ["White", "Black", "Hispanic", "Other"]

# ---------------------------------------------------------------------------
# McCollister, French & Fang (2010), Table 3/4/5, 2008 dollars.  Copied from
# infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py, which reconstructs
# the published totals exactly; the same reconstruction is gated again below.
#   offence: (victim, cjs, career, intangible, published_total)
# ---------------------------------------------------------------------------
MCC = {
    "sexual":  (5_556, 26_479, 9_212, 199_642, 240_776),   # rape / sexual assault
    "robbery": (3_299, 13_827, 4_272, 22_575, 42_310),
    "assault": (8_700, 8_641, 2_126, 95_023, 107_020),     # aggravated assault
}
NCVS_TO_MCC = {
    "Rape/sexual assault": "sexual",
    "Robbery": "robbery",
    "Aggravated assault": "assault",
    # "Simple assault" has no McCollister unit cost; priced in two arms below.
}


def unit_costs(cpi: dict[int, float]) -> pd.DataFrame:
    infl = cpi[2024] / cpi[2008]
    rows = []
    for off, (vic, cjs, car, intang, total) in MCC.items():
        removed = (vic + cjs + car + intang) - total
        gate(f"mcc_reconstruct_{off}", abs(removed) < 1_000_000,
             f"risk-of-homicide slice removed from the victim column = {removed:,.0f} (2008$)")
        rows.append(
            {
                "offence": off,
                "social_total_2024": total * infl,
                "cjs_2024": cjs * infl,
                "victim_tangible_2024": vic * infl,
                "intangible_2024": intang * infl,
            }
        )
    return pd.DataFrame(rows).set_index("offence")


# ---------------------------------------------------------------------------
# 1. The pooled matrices
# ---------------------------------------------------------------------------
def pooled_matrix(m: pd.DataFrame, years: list[int], victims: list[str]) -> pd.DataFrame:
    """Sum counts across years; SE of the sum under between-year independence."""
    d = m[(m.year.isin(years)) & (m.victim.isin(victims)) & (m.measure == "count")]
    g = d.groupby(["victim", "offender"]).agg(
        count=("value", "sum"),
        var=("value_se", lambda s: float((s.astype(float) ** 2).sum())),
        n_years=("value", "size"),
    ).reset_index()
    gate(
        f"pooled_years_{min(years)}_{max(years)}",
        (g.n_years == len(years)).all(),
        f"every cell present in all {len(years)} years",
    )
    g["se"] = np.sqrt(g["var"])
    return g.drop(columns=["var", "n_years"])


def to_wide(g: pd.DataFrame, victims: list[str], offenders: list[str],
            field: str = "count") -> pd.DataFrame:
    return (
        g.pivot(index="victim", columns="offender", values=field)
        .reindex(index=victims, columns=offenders)
    )


def shares(w: pd.DataFrame, axis: str, cols: list[str]) -> pd.DataFrame:
    sub = w[cols]
    if axis == "row":
        return sub.div(sub.sum(axis=1), axis=0)
    return sub.div(sub.sum(axis=0), axis=1)


def main() -> None:
    m = pd.read_csv(DERIVED / "cv_matrix_violent.csv")
    ms = pd.read_csv(DERIVED / "cv_matrix_violent_excl_simple.csv")
    t11 = pd.read_csv(DERIVED / "cv_offender_marginal.csv")
    pop = pd.read_csv(DERIVED / "cv_population_12plus.csv")
    nd = pd.read_csv(DERIVED / "ndash_rate_by_victim_race.csv")
    cpi = dict(
        pd.read_csv(DERIVED / "cpi_u_annual.csv").itertuples(index=False, name=None)
    )

    header("integrity gates on the published tables")
    uc = unit_costs(cpi)

    # Column sums of the matrix must reproduce the offender marginal in table 11.
    for y in (2022, 2023, 2024):
        w = to_wide(
            m[(m.year == y) & (m.measure == "count")]
            .rename(columns={"value": "count"})[["victim", "offender", "count"]],
            GROUPS, OFF_COLS,
        )
        t = t11[t11.year == y].set_index("group")
        got_w = w["White"].sum()
        got_b = w["Black"].sum()
        got_h = w["Hispanic"].sum()
        got_o = w["Other"].sum()
        want_o = (t.loc["Asian", "offender_incidents"] + t.loc["Other", "offender_incidents"]
                  + t.loc["MultipleVarious", "offender_incidents"])
        ok = all(
            abs(a - b) <= 100
            for a, b in (
                (got_w, t.loc["White", "offender_incidents"]),
                (got_b, t.loc["Black", "offender_incidents"]),
                (got_h, t.loc["Hispanic", "offender_incidents"]),
                (got_o, want_o),
            )
        )
        gate(f"colsum_matches_t11_{y}", ok,
             f"W {got_w:,.0f}/{t.loc['White', 'offender_incidents']:,.0f}  "
             f"B {got_b:,.0f}/{t.loc['Black', 'offender_incidents']:,.0f}  "
             f"H {got_h:,.0f}/{t.loc['Hispanic', 'offender_incidents']:,.0f}  "
             f"O {got_o:,.0f}/{want_o:,.0f}")

        # Row totals must reproduce the victim marginal (Asian + Other combined).
        rt = m[(m.year == y) & (m.measure == "count")].groupby("victim").row_total.first()
        want_v = t.loc["Asian", "victim_incidents"] + t.loc["Other", "victim_incidents"]
        gate(f"rowsum_matches_t11_{y}", abs(rt["Other"] - want_v) <= 100,
             f"Other victim row {rt['Other']:,.0f} vs Asian+Other in table 11 {want_v:,.0f}")

    # ---------------------------------------------------------------------
    header("(a) victim x offender matrix, pooled 2022-2024, violent incidents")
    # ---------------------------------------------------------------------
    YRS = [2022, 2023, 2024]
    g = pooled_matrix(m, YRS, GROUPS)
    W = to_wide(g, GROUPS, OFF_COLS)
    SE = to_wide(g, GROUPS, OFF_COLS, "se")
    say(W.map(lambda v: f"{v:,.0f}").to_string())
    say()
    say("standard errors (between-year independence assumed; NCVS's rotating panel makes")
    say("adjacent years positively correlated, so these understate the true SE):")
    say(SE.map(lambda v: f"{v:,.0f}").to_string())

    unk = W["Unknown"].sum() / W[OFF_COLS].values.sum()
    gate("unknown_offender_share", 0.10 < unk < 0.30,
         f"offender ethnicity unknown in {unk:.1%} of pooled 2022-2024 violent incidents")

    row_incl = shares(W, "row", OFF_COLS)
    row_excl = shares(W, "row", KNOWN)
    col = shares(W, "col", KNOWN)

    say()
    say("row shares INCLUDING the unknown-offender column (arm: unknown kept):")
    say(row_incl.round(3).to_string())
    say()
    say("row shares EXCLUDING it (arm: offender ethnicity known):")
    say(row_excl.round(3).to_string())
    say()
    say("column shares = victim distribution of each offender group "
        "(directly comparable with the homicide matrix):")
    say(col.round(3).to_string())

    out = g.copy()
    out["row_share_incl_unknown"] = [
        row_incl.loc[r.victim, r.offender] for r in g.itertuples()
    ]
    out["row_share_excl_unknown"] = [
        row_excl.loc[r.victim, r.offender] if r.offender in KNOWN else np.nan
        for r in g.itertuples()
    ]
    out["col_share"] = [
        col.loc[r.victim, r.offender] if r.offender in KNOWN else np.nan
        for r in g.itertuples()
    ]
    out.insert(0, "years", "2022-2024")
    out.to_csv(DERIVED / "matrix_pooled_2022_2024.csv", index=False)

    # Longer window, three victim rows only (2021 publishes no "Other" victim row).
    g4 = pooled_matrix(m, [2021, 2022, 2023, 2024], ["White", "Black", "Hispanic"])
    W4 = to_wide(g4, ["White", "Black", "Hispanic"], OFF_COLS)
    col4 = shares(W4, "col", KNOWN)
    g4["col_share_3victims"] = [col4.loc[r.victim, r.offender] if r.offender in KNOWN
                                else np.nan for r in g4.itertuples()]
    g4.insert(0, "years", "2021-2024")
    g4.to_csv(DERIVED / "matrix_pooled_2021_2024_three_victim_rows.csv", index=False)

    # ---------------------------------------------------------------------
    header("(a2) serious violent and simple assault, 2019 (the only year with both)")
    # ---------------------------------------------------------------------
    v19 = to_wide(
        m[(m.year == 2019) & (m.measure == "count")]
        .rename(columns={"value": "count"})[["victim", "offender", "count"]],
        ["White", "Black", "Hispanic"], ["White", "Black", "Hispanic", "Other"],
    )
    s19 = to_wide(
        ms[(ms.year == 2019) & (ms.measure == "count")]
        .rename(columns={"value": "count"})[["victim", "offender", "count"]],
        ["White", "Black", "Hispanic"], ["White", "Black", "Hispanic", "Other"],
    )
    simple19 = v19 - s19
    gate("simple_assault_nonneg_2019", (simple19.values >= 0).all(),
         f"min residual cell {simple19.values.min():,.0f}")
    crime_split = []
    for name, tab in (("violent", v19), ("serious_violent", s19), ("simple_assault", simple19)):
        c = shares(tab, "col", ["White", "Black", "Hispanic", "Other"])
        say(f"{name}: column shares (victim distribution of each offender group), 2019")
        say(c.round(3).to_string())
        say()
        for v in c.index:
            for o in c.columns:
                crime_split.append({"year": 2019, "scope": name, "victim": v,
                                    "offender": o, "count": tab.loc[v, o],
                                    "col_share": c.loc[v, o]})
    pd.DataFrame(crime_split).to_csv(DERIVED / "matrix_by_crime_type_2019.csv", index=False)

    # ---------------------------------------------------------------------
    header("(b) single-offender restriction — BJS NCJ 250747, 2012-15")
    # ---------------------------------------------------------------------
    t2 = pd.read_csv(DERIVED / "rhovo_t2_offender_by_offender_count.csv")
    t2 = t2[t2.offender != "Total"].set_index("offender")
    t2["single_minus_total_pp"] = t2.single_pct - t2.total_pct
    say(t2[["total_pct", "single_pct", "multiple_pct", "single_minus_total_pp"]].to_string())
    t2.to_csv(DERIVED / "single_vs_multiple_offender_2012_2015.csv")
    say()
    say("The SHR homicide universe is single-victim/single-offender.  Restricting NCVS the")
    say("same way moves the Hispanic offender share of all violent victimisations from")
    say(f"{t2.loc['Hispanic', 'total_pct']}% to {t2.loc['Hispanic', 'single_pct']}% "
        f"({t2.loc['Hispanic', 'single_minus_total_pp']:+.1f} pp), while the white share moves "
        f"{t2.loc['White', 'single_minus_total_pp']:+.1f} pp and the Black share "
        f"{t2.loc['Black', 'single_minus_total_pp']:+.1f} pp.")

    # ---------------------------------------------------------------------
    header("(c) victimisation rate per 1,000, by victim group and by offender group")
    # ---------------------------------------------------------------------
    P = pop[pop.year.isin(YRS)].groupby("group").population.sum()  # person-years
    rate_rows = []
    for gname in GROUPS:
        vict = W.loc[gname, OFF_COLS].sum()
        denom = P[gname] if gname != "Other" else (P["Other"] + P["Asian"])
        rate_rows.append({"group": gname, "side": "victim", "incidents": vict,
                          "person_years": denom, "rate_per_1000": 1000 * vict / denom})
    for gname in KNOWN:
        offd = W[gname].sum()
        denom = P[gname] if gname != "Other" else (P["Other"] + P["Asian"])
        rate_rows.append({"group": gname, "side": "offender", "incidents": offd,
                          "person_years": denom, "rate_per_1000": 1000 * offd / denom})
    rates = pd.DataFrame(rate_rows)
    say(rates.assign(rate_per_1000=lambda d: d.rate_per_1000.round(2)).to_string(index=False))
    rates.to_csv(DERIVED / "rates_by_victim_and_offender_2022_2024.csv", index=False)

    # Cross-check the victim rate against N-DASH, which is built from the same survey.
    ndv = nd[(nd.year.isin(YRS)) & (nd.crimeType == "Violent victimization")]
    ndr = ndv.groupby("victim_race").apply(
        lambda d: d["count"].sum() / (P.reindex(
            ["Other", "Asian"] if d.name == "Other" else [d.name]).sum()) * 1000,
        include_groups=False,
    )
    say()
    say("N-DASH victimisation rate per 1,000 over the same years (victimisations, not")
    say("incidents, so it runs above the incident rate by the multiple-victim factor):")
    say(ndr.round(2).to_string())
    ratio = (ndr / rates[rates.side == "victim"].set_index("group").rate_per_1000)
    gate("victimisation_vs_incident_ratio", ((ratio > 1.0) & (ratio < 1.5)).all(),
         "victimisations per incident by victim group: "
         + ", ".join(f"{k} {v:.2f}" for k, v in ratio.items()))

    # ---------------------------------------------------------------------
    header("(d) cross-group shares")
    # ---------------------------------------------------------------------
    cross = []
    for o in KNOWN:
        for v in GROUPS:
            cross.append({"offender": o, "victim": v, "col_share": col.loc[v, o],
                          "row_share_excl_unknown": row_excl.loc[v, o]})
    cross_df = pd.DataFrame(cross)
    cross_df.to_csv(DERIVED / "cross_group_shares_2022_2024.csv", index=False)
    say(f"Hispanic offender -> white victim:   {col.loc['White', 'Hispanic']:.3f}")
    say(f"Hispanic offender -> Hispanic victim: {col.loc['Hispanic', 'Hispanic']:.3f}")
    say(f"White offender -> Hispanic victim:    {col.loc['Hispanic', 'White']:.3f}")
    say(f"White offender -> white victim:       {col.loc['White', 'White']:.3f}")
    say(f"Black offender -> Black victim:       {col.loc['Black', 'Black']:.3f}")

    popshare = {gname: (P[gname] if gname != "Other" else P["Other"] + P["Asian"]) / P.sum()
                for gname in GROUPS}
    conc = pd.DataFrame(
        [{"group": gname, "intra_group_col_share": col.loc[gname, gname],
          "population_share": popshare[gname],
          "concentration_ratio": col.loc[gname, gname] / popshare[gname]}
         for gname in GROUPS]
    )
    say()
    say("Intra-group share against the victim group's own population share:")
    say(conc.round(3).to_string(index=False))
    conc.to_csv(DERIVED / "intra_group_concentration_2022_2024.csv", index=False)

    # ---------------------------------------------------------------------
    header("(e) offence-mix cost weighting")
    # ---------------------------------------------------------------------
    mix = (
        nd[(nd.year.isin(YRS)) & (nd.crimeType.isin(list(NCVS_TO_MCC) + ["Simple assault"]))]
        .groupby(["victim_race", "crimeType"])["count"].sum().unstack()
    )
    mix_sh = mix.div(mix.sum(axis=1), axis=0)
    say("offence mix by victim group, pooled 2022-2024 victimisations (N-DASH):")
    say(mix_sh.round(3).to_string())
    mix_sh.to_csv(DERIVED / "offence_mix_by_victim_group.csv")

    cost_rows = []
    for arm, simple_price in (("simple_at_zero", 0.0), ("simple_at_aggravated", 1.0)):
        for pricing in ("social_total_2024", "cjs_2024"):
            for gname in GROUPS:
                per = 0.0
                for ct, key in NCVS_TO_MCC.items():
                    per += mix_sh.loc[gname, ct] * uc.loc[key, pricing]
                per += mix_sh.loc[gname, "Simple assault"] * simple_price * uc.loc["assault", pricing]
                r = rates[(rates.group == gname) & (rates.side == "victim")].rate_per_1000.iloc[0]
                cost_rows.append({"arm": arm, "pricing": pricing, "group": gname,
                                  "cost_per_incident": per,
                                  "rate_per_1000": r,
                                  "cost_per_1000_persons": per * r})
    costs = pd.DataFrame(cost_rows)
    costs.to_csv(DERIVED / "cost_of_victimisation_by_group.csv", index=False)
    for arm in costs.arm.unique():
        for pricing in costs.pricing.unique():
            sub = costs[(costs.arm == arm) & (costs.pricing == pricing)]
            say(f"{arm} / {pricing}: " + "  ".join(
                f"{r.group} ${r.cost_per_incident:,.0f}/incident, "
                f"${r.cost_per_1000_persons:,.0f} per 1,000 persons"
                for r in sub.itertuples()))

    # Inter-group cost transfer per capita of the OFFENDER group.
    transfer_rows = []
    for arm, simple_price in (("simple_at_zero", 0.0), ("simple_at_aggravated", 1.0)):
        for pricing in ("social_total_2024", "cjs_2024"):
            per_victim = {}
            for gname in GROUPS:
                per = sum(mix_sh.loc[gname, ct] * uc.loc[key, pricing]
                          for ct, key in NCVS_TO_MCC.items())
                per += mix_sh.loc[gname, "Simple assault"] * simple_price * uc.loc["assault", pricing]
                per_victim[gname] = per
            for o in KNOWN:
                denom = P[o] if o != "Other" else P["Other"] + P["Asian"]
                intra = W.loc[o, o] * per_victim[o]
                inter = sum(W.loc[v, o] * per_victim[v] for v in GROUPS if v != o)
                transfer_rows.append({
                    "arm": arm, "pricing": pricing, "offender": o,
                    "intra_group_cost": intra, "inter_group_cost": inter,
                    "inter_group_cost_per_capita": inter / denom * 3,  # 3 pooled years
                    "total_cost_per_capita": (intra + inter) / denom * 3,
                })
    tr = pd.DataFrame(transfer_rows)
    tr.to_csv(DERIVED / "inter_group_cost_transfer.csv", index=False)
    say()
    say("Cost imposed per resident-year of the offender group (pooled 2022-2024 / 3), "
        "inter-group and total:")
    for arm in tr.arm.unique():
        for pricing in tr.pricing.unique():
            sub = tr[(tr.arm == arm) & (tr.pricing == pricing)]
            say(f"  {arm} / {pricing}")
            for r in sub.itertuples():
                say(f"    {r.offender:<9} inter-group ${r.inter_group_cost_per_capita:>8,.0f}"
                    f"   total ${r.total_cost_per_capita:>8,.0f}")

    # ---------------------------------------------------------------------
    header("disconfirmation arms")
    # ---------------------------------------------------------------------
    arms = []

    # C1. Unknown-offender reallocation, three rules.
    base = col.copy()
    arms.append({"arm": "C1a_unknown_dropped", **{f"intra_{gname}": base.loc[gname, gname]
                                                  for gname in GROUPS}})
    # proportional within each victim row (unknowns look like that row's known offenders)
    Wp = W[KNOWN].add(
        W[KNOWN].div(W[KNOWN].sum(axis=1), axis=0).mul(W["Unknown"], axis=0), fill_value=0
    )
    cp = shares(Wp, "col", KNOWN)
    arms.append({"arm": "C1b_unknown_proportional_within_victim_row",
                 **{f"intra_{gname}": cp.loc[gname, gname] for gname in GROUPS}})
    # all unknowns are out-group offenders, split by each other group's population
    Wo = W[KNOWN].copy().astype(float)
    for v in GROUPS:
        others = [o for o in KNOWN if o != v]
        wts = np.array([(P[o] if o != "Other" else P["Other"] + P["Asian"]) for o in others],
                       dtype=float)
        wts = wts / wts.sum()
        for o, wt in zip(others, wts):
            Wo.loc[v, o] += W.loc[v, "Unknown"] * wt
    co = shares(Wo, "col", KNOWN)
    arms.append({"arm": "C1c_unknown_all_out_group",
                 **{f"intra_{gname}": co.loc[gname, gname] for gname in GROUPS}})
    # all unknowns are in-group offenders (the opposite bound)
    Wi = W[KNOWN].copy().astype(float)
    for v in GROUPS:
        Wi.loc[v, v] += W.loc[v, "Unknown"]
    ci = shares(Wi, "col", KNOWN)
    arms.append({"arm": "C1d_unknown_all_in_group",
                 **{f"intra_{gname}": ci.loc[gname, gname] for gname in GROUPS}})

    # C2. Reported-to-police only, and injury only (2012-15, three groups).
    t6 = pd.read_csv(DERIVED / "rhovo_t6_reported_to_police.csv")
    t8 = pd.read_csv(DERIVED / "rhovo_t8_injury.csv")
    for label, tab, pctcol in (("C2_reported_to_police_only", t6, "pct_reported_to_police"),
                               ("C3_injury_only", t8, "pct_injured")):
        sub = tab.copy()
        sub["weighted"] = sub.avg_annual_number * sub[pctcol] / 100.0
        piv_all = sub.pivot(index="victim", columns="offender", values="avg_annual_number")
        piv_w = sub.pivot(index="victim", columns="offender", values="weighted")
        c_all = piv_all.div(piv_all.sum(axis=0), axis=1)
        c_w = piv_w.div(piv_w.sum(axis=0), axis=1)
        arms.append({"arm": f"{label}_baseline_2012_2015",
                     **{f"intra_{gname}": c_all.loc[gname, gname]
                        for gname in ["White", "Black", "Hispanic"]}})
        arms.append({"arm": label,
                     **{f"intra_{gname}": c_w.loc[gname, gname]
                        for gname in ["White", "Black", "Hispanic"]}})

    # C3b. The same three-group restriction the 2012-15, 2018 and 2019 tables impose,
    # applied to the pooled 2022-2024 matrix, so those arms have a like-for-like baseline.
    W3 = W.loc[["White", "Black", "Hispanic"], ["White", "Black", "Hispanic"]]
    c3 = shares(W3, "col", ["White", "Black", "Hispanic"])
    arms.append({"arm": "C3b_2022_2024_three_group_restricted",
                 **{f"intra_{gname}": c3.loc[gname, gname]
                    for gname in ["White", "Black", "Hispanic"]}})

    # C4. The 2018 and 2019 vintages, which use different offender conventions.
    for y, tab, meas in ((2018, m, "percent"), (2019, m, "count")):
        d = tab[(tab.year == y) & (tab.measure == meas)]
        vics = sorted(d.victim.unique())
        offs = [o for o in ["White", "Black", "Hispanic", "Asian", "Other", "MultipleVarious"]
                if o in set(d.offender)]
        wy = d.pivot(index="victim", columns="offender", values="value").reindex(
            index=vics, columns=offs)
        if meas == "percent":
            tot = d.groupby("victim").row_total.first().reindex(vics)
            wy = wy.div(100.0).mul(tot, axis=0)
        cy = shares(wy, "col", [o for o in offs if o in KNOWN])
        arms.append({"arm": f"C4_year_{y}_own_convention",
                     **{f"intra_{gname}": cy.loc[gname, gname]
                        for gname in ["White", "Black", "Hispanic"]}})

    # C5. Serious violent only, and simple assault only, 2019.
    for name, tab in (("C5_serious_violent_2019", s19), ("C5_simple_assault_2019", simple19)):
        c = shares(tab, "col", ["White", "Black", "Hispanic"])
        arms.append({"arm": name, **{f"intra_{gname}": c.loc[gname, gname]
                                     for gname in ["White", "Black", "Hispanic"]}})

    arms_df = pd.DataFrame(arms)
    arms_df.to_csv(DERIVED / "disconfirmation_arms.csv", index=False)
    say(arms_df.round(3).to_string(index=False))

    # ---------------------------------------------------------------------
    header("comparison with the cleared-homicide matrix")
    # ---------------------------------------------------------------------
    # SHR universe A, 2019-2023, ethnicity known both sides, from
    # research/immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md §2.1,
    # "Victim distribution of each offender group".  Rows are offenders there; here the
    # dict is keyed [offender][victim] to match.
    HOM_FULL = {
        "Hispanic": {"Hispanic": 0.717, "White": 0.156, "Black": 0.110, "Other": 0.016},
        "White":    {"Hispanic": 0.081, "White": 0.809, "Black": 0.092, "Other": 0.018},
        "Black":    {"Hispanic": 0.064, "White": 0.112, "Black": 0.813, "Other": 0.011},
        "Other":    {"Hispanic": 0.077, "White": 0.165, "Black": 0.095, "Other": 0.663},
    }
    HOM = {o: HOM_FULL[o][o] for o in HOM_FULL}
    HOM_IMPUTED_HISP = 0.667
    cell = []
    for o in GROUPS:
        for v in GROUPS:
            cell.append({
                "offender": o, "victim": v,
                "homicide_share": HOM_FULL[o][v],
                "ncvs_violent_share": col.loc[v, o],
                "difference": col.loc[v, o] - HOM_FULL[o][v],
                "ncvs_over_homicide": col.loc[v, o] / HOM_FULL[o][v],
            })
    cell_df = pd.DataFrame(cell)
    cell_df.to_csv(DERIVED / "comparison_with_homicide_all_cells.csv", index=False)
    say("Every cell, offender -> victim share, cleared homicide against non-fatal violence:")
    say(cell_df.round(3).to_string(index=False))
    say()
    cmp_rows = []
    for gname in GROUPS:
        cmp_rows.append({
            "offender_group": gname,
            "homicide_intra_share_known": HOM[gname],
            "ncvs_violent_intra_share_2022_2024": col.loc[gname, gname],
            "difference": col.loc[gname, gname] - HOM[gname],
            "ncvs_concentration_ratio": conc.set_index("group").loc[gname, "concentration_ratio"],
        })
    cmp = pd.DataFrame(cmp_rows)
    say(cmp.round(3).to_string(index=False))
    cmp.to_csv(DERIVED / "comparison_with_homicide.csv", index=False)
    say()
    say(f"Under the homicide lane's joint imputation the Hispanic figure is "
        f"{HOM_IMPUTED_HISP}; the NCVS figure is "
        f"{col.loc['Hispanic', 'Hispanic']:.3f}.")
    gate("intra_group_lower_off_murder_margin",
         all(col.loc[gname, gname] < HOM[gname] for gname in GROUPS),
         "every group's intra-group share is lower for non-fatal violence than for "
         "cleared homicide")

    (DERIVED / "analysis_log.txt").write_text("\n".join(_lines) + "\n")
    if FAILS:
        raise SystemExit("gates failed: " + ", ".join(FAILS))
    say()
    say("[done] analysis.py")
    (DERIVED / "analysis_log.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
