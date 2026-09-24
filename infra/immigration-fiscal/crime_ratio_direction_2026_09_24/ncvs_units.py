"""Victimizations per incident by perceived offender: NCVS Select microdata against the published
incident matrix the victim-cost lane uses.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/ncvs_units.py

The victim-cost lane (crime_victim_cost_2026_09_23) takes Hispanic-offender *incidents* from
Criminal Victimization table 13 (2022-2024, via ncvs_victim_offender_2026_09_18) and converts
them to *victimizations* with one ratio per victim group (N-DASH victimizations / table-13
incidents, 1.06-1.09), the same for every offender column. Unit costs are per victimization.
The Select file is victimization-level (series-adjusted weight `newwgt`) and uses the same
all-offenders rule for Hispanic groups (it reproduces NCJ 250747 table 6 to 1.2%; ncvs_log.txt).
So Select victimizations / table-13 incidents in each victim x offender cell measures
victimizations per incident by offender group, and the victim lane's conversion can be checked.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import ncvs_select as ns

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
NCVS = HERE.parent / "ncvs_victim_offender_2026_09_18"
VNAME = {"NHW": "White", "NHB": "Black", "H": "Hispanic", "NHO": "Other"}
ONAME = {"NHW": "White", "NHB": "Black", "H": "Hispanic", "NHO": "Other", "MIX": "Other", "U": "Unknown"}
VICTIMS = ["White", "Black", "Hispanic", "Other"]
OFFENDERS = ["White", "Black", "Hispanic", "Other", "Unknown"]
YEARS = [2022, 2023, 2024]
LOG: list[str] = []
rng = np.random.default_rng(20260924)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def micro_cells(v: pd.DataFrame, w: str = "newwgt") -> pd.DataFrame:
    x = v.assign(victim=v.vg.map(VNAME), offender=v.og.map(ONAME))
    return x.groupby(["year", "victim", "offender"])[w].sum().unstack("offender").reindex(columns=OFFENDERS, fill_value=0)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    v, _ = ns.load()
    v = v[v.year.isin(YEARS)].copy()
    pub = pd.read_csv(NCVS / "derived/cv_matrix_violent.csv")
    pub = pub[pub.year.isin(YEARS) & pub.measure.eq("count")].pivot_table(
        index=["year", "victim"], columns="offender", values="value", aggfunc="sum")[OFFENDERS]
    mic = micro_cells(v).reindex(pub.index)
    # gate: the published matrix is the one the victim lane pools (2022-2024 incident total)
    pooled = pd.read_csv(NCVS / "derived/matrix_pooled_2022_2024.csv")
    gate("published table-13 incidents 2022-2024 sum to the NCVS lane's pooled matrix",
         abs(pub.to_numpy().sum() - pooled["count"].sum()) < 1, f"{pub.to_numpy().sum():,.0f}")
    # gate: victimization totals equal CV2024 table 1 (checked in ncvs_select.py), re-checked here
    for yr, tot in [(2022, 6_624_950), (2023, 6_419_060), (2024, 6_671_640)]:
        got = float(v.loc[v.year == yr, "newwgt"].sum())
        gate(f"{yr} Select violent victimizations equal CV2024 table 1", abs(got / tot - 1) < 0.001, f"{got:,.0f}")

    rows = []
    for (yr, vic), p in pub.iterrows():
        m = mic.loc[(yr, vic)]
        for o in OFFENDERS:
            rows.append(dict(year=yr, victim=vic, offender=o, published_incidents=p[o], select_victimizations=m[o],
                             victimizations_per_incident=m[o] / p[o] if p[o] > 0 else np.nan))
    P = pub.groupby(level="victim").sum()
    M = mic.groupby(level="victim").sum()
    for vic in VICTIMS:
        for o in OFFENDERS:
            rows.append(dict(year="2022-2024", victim=vic, offender=o, published_incidents=P.loc[vic, o],
                             select_victimizations=M.loc[vic, o], victimizations_per_incident=M.loc[vic, o] / P.loc[vic, o]))
        rows.append(dict(year="2022-2024", victim=vic, offender="all (row)", published_incidents=P.loc[vic].sum(),
                         select_victimizations=M.loc[vic].sum(), victimizations_per_incident=M.loc[vic].sum() / P.loc[vic].sum()))
    for o in OFFENDERS:
        rows.append(dict(year="2022-2024", victim="all (column)", offender=o, published_incidents=P[o].sum(),
                         select_victimizations=M[o].sum(), victimizations_per_incident=M[o].sum() / P[o].sum()))
    for yr in YEARS:
        for o in OFFENDERS:
            a, b = pub.loc[yr][o].sum(), mic.loc[yr][o].sum()
            rows.append(dict(year=yr, victim="all (column)", offender=o, published_incidents=a, select_victimizations=b,
                             victimizations_per_incident=b / a))
    R = pd.DataFrame(rows)

    # the victim lane's own conversion: N-DASH victimizations / table-13 incidents by victim row
    nd = pd.read_csv(NCVS / "derived/ndash_rate_by_victim_race.csv")
    nd = nd[nd.year.between(2022, 2024) & nd.crimeType.isin(list(ns.OFFN.values()))]
    ndv = nd.pivot_table(index="victim_race", columns="crimeType", values="count", aggfunc="sum").sum(axis=1)
    lane_ratio = ndv / P.sum(axis=1)
    say("\n-- victimizations per incident, pooled 2022-2024: victim lane's row ratio (N-DASH) vs Select --")
    rr = R[R.year.eq("2022-2024") & R.victim.isin(VICTIMS)].pivot_table(
        index="victim", columns="offender", values="victimizations_per_incident", sort=False)
    rr["victim lane (N-DASH row)"] = lane_ratio
    say(rr.to_string(float_format=lambda x: f"{x:.3f}"))
    gate("Select row ratios within 0.03 of the victim lane's N-DASH row ratios (same survey, same unit)",
         (rr["all (row)"] - rr["victim lane (N-DASH row)"]).abs().max() < 0.03,
         ", ".join(f"{g} {rr.loc[g, 'all (row)']:.3f} vs {rr.loc[g, 'victim lane (N-DASH row)']:.3f}" for g in VICTIMS))

    # bootstrap within year for the pooled Hispanic-column factor (Select numerator; published
    # denominators held fixed, so the SE is conservative), scaled by the NCVS design effect
    deff = 1.29
    fac = {}
    for vic in VICTIMS + ["all"]:
        fac[vic] = []
    vv = v.assign(victim=v.vg.map(VNAME), offender=v.og.map(ONAME))
    parts = [vv[vv.year == y] for y in YEARS]
    for _ in range(300):
        bs = pd.concat([p.iloc[rng.integers(0, len(p), len(p))] for p in parts])
        h = bs[bs.offender.eq("Hispanic")].groupby("victim").newwgt.sum().reindex(VICTIMS, fill_value=0)
        f = h / P["Hispanic"] / lane_ratio
        for vic in VICTIMS:
            fac[vic].append(f[vic])
        fac["all"].append(h.sum() / (P["Hispanic"] * lane_ratio).sum())
    point = M["Hispanic"] / P["Hispanic"] / lane_ratio
    point_all = M["Hispanic"].sum() / (P["Hispanic"] * lane_ratio).sum()
    corr = pd.DataFrame([dict(victim=vic, hispanic_offender_incidents=P.loc[vic, "Hispanic"],
                              select_victimizations=M.loc[vic, "Hispanic"], lane_row_ratio=lane_ratio[vic],
                              lane_victimizations=P.loc[vic, "Hispanic"] * lane_ratio[vic],
                              factor=point[vic], se=float(np.std(fac[vic], ddof=1) * np.sqrt(deff)))
                         for vic in VICTIMS]
                        + [dict(victim="all", hispanic_offender_incidents=P["Hispanic"].sum(),
                                select_victimizations=M["Hispanic"].sum(), lane_row_ratio=np.nan,
                                lane_victimizations=(P["Hispanic"] * lane_ratio).sum(), factor=point_all,
                                se=float(np.std(fac["all"], ddof=1) * np.sqrt(deff)))])
    # the same factor for the white-offender column, as the control that should sit near 1
    wf = M["White"].sum() / (P["White"] * lane_ratio).sum()
    corr.to_csv(OUT / "ncvs_victimization_factor.csv", index=False, float_format="%.6f", lineterminator="\n")
    R.to_csv(OUT / "ncvs_victimizations_per_incident.csv", index=False, float_format="%.6f", lineterminator="\n")
    say("\n-- Hispanic-offender victimizations: Select vs the victim lane's conversion (pooled 2022-2024) --")
    say(corr.to_string(index=False, float_format=lambda x: f"{x:,.3f}" if abs(x) < 100 else f"{x:,.0f}"))
    say(f"   control, white-offender column: Select / lane conversion = {wf:.3f}")
    say("\n-- column ratios by year (Select victimizations / table-13 incidents) --")
    say(R[R.victim.eq("all (column)")].pivot_table(index="year", columns="offender",
                                                     values="victimizations_per_incident", sort=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    (OUT / "ncvs_units_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
