"""Arms 2 and 3: NCVS victims' perception of offender Hispanic origin against police records, and
reporting to police by victim and perceived-offender ethnicity, from BJS's NCVS Select files.

    uv run --no-project --with pandas --with numpy python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/ncvs_select.py

Data (no login): NCVS Select personal victimization (`gcuy-rt5g`, record level, offender race/
Hispanic origin `offtracenew` from 2012 Q1, reporting `notify`, series-adjusted weight `newwgt`)
and personal population (`r4j4-fdwx`, weight `wgtpercy`, aggregated server-side by year x
race/Hispanic origin x region), https://api.ojp.gov/bjsdataset/v1/ . Collection-year basis,
legacy instrument (2024 is the legacy half-sample).

Offending rate of group g for offence o over a window = sum of annual victimizations attributed
to g / sum of annual residents of g aged 12+ (person-years; each year's weights are annual).
Offender groups follow `offtracenew`: 1 NH white, 2 NH Black, 3-5 NH other, 6 Hispanic, 7 unknown
race/origin, 10 mixed-race group, 11 unknown number. Allocation of 7/10/11:
    known     dropped
    victim    in proportion to known offenders within victim group x offence x window (the
              analogue of the NIBRS lane's allocation a; central)
    b / c     all to non-Hispanic groups (by the victim cell's non-Hispanic split) / all Hispanic
Standard errors: the files carry no design variables. A record bootstrap within year gives a
naive SE; it is scaled by the square root of the design effect measured against BJS's published
SEs for the 2022-2024 violent totals (CV2024 appendix table 2) [INFERENCE: approximation].
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "ncvs"
OUT = HERE / "derived"
VIC = CACHE / "ncvs_select_personal_victimization.csv"
POP = CACHE / "ncvs_select_population_year_race_region.csv"
API = "https://api.ojp.gov/bjsdataset/v1/"
CV24 = HERE.parent / "ncvs_victim_offender_2026_09_18" / "_cache" / "cv24"
OFFN = {1: "Rape/sexual assault", 2: "Robbery", 3: "Aggravated assault", 4: "Simple assault"}
VG = {1: "NHW", 2: "NHB", 3: "NHO", 4: "NHO", 5: "NHO", 6: "H"}
OG = {1: "NHW", 2: "NHB", 3: "NHO", 4: "NHO", 5: "NHO", 6: "H", 7: "U", 10: "MIX", 11: "U"}
GROUPS = ["H", "NHW", "NHB", "NHO"]
LOG: list[str] = []
rng = np.random.default_rng(20260924)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def fetch_population() -> pd.DataFrame:
    if not POP.exists():
        q = ("$select=year,race_ethnicity,region,sum(wgtpercy::number) as w,count(*) as n"
             "&$group=year,race_ethnicity,region&$where=year>='2012'&$limit=50000")
        url = API + "r4j4-fdwx.json?" + q.replace(" ", "%20").replace(">", "%3E").replace("'", "%27")
        r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "600", "-A", "Mozilla/5.0", url],
                           capture_output=True, text=True, check=True)
        d = pd.DataFrame(json.loads(r.stdout))
        if not {"year", "race_ethnicity", "region", "w", "n"} <= set(d.columns):
            raise SystemExit(f"[BLOCKED] population aggregate columns {list(d.columns)}")
        d.to_csv(POP, index=False, lineterminator="\n")
    p = pd.read_csv(POP)
    p["g"] = p.race_ethnicity.map(VG)
    return p


def cv24_number(table: str, row_label: str, col: int) -> float:
    """Read one number from a CV2024 csv (row identified by its label, value column index)."""
    for line in (CV24 / table).read_text(encoding="latin-1").splitlines():
        cells = next(iter(pd.read_csv(pd.io.common.StringIO(line), header=None, dtype=str).itertuples(index=False)))
        cells = [str(c) for c in cells]
        if any(c.strip() == row_label for c in cells[:4]):
            return float(cells[col].replace(",", ""))
    raise SystemExit(f"[BLOCKED] {table}: row {row_label!r} not found")


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    v = pd.read_csv(VIC)
    if len(v) != 68852 or not {"offtracenew", "notify", "newwgt", "newoff", "race_ethnicity", "region"} <= set(v.columns):
        raise SystemExit("[BLOCKED] NCVS Select victimization file: unexpected rows or columns")
    v = v[(v.year >= 2012) & v.newoff.isin(OFFN)].copy()
    v["offence"] = v.newoff.map(OFFN)
    v["vg"] = v.race_ethnicity.map(VG)
    v["og"] = v.offtracenew.map(OG)
    if v.og.isna().any() or v.vg.isna().any():
        raise SystemExit(f"[BLOCKED] unmapped codes: {v.loc[v.og.isna(), 'offtracenew'].unique()}")
    return v, fetch_population()


def gates(v: pd.DataFrame, p: pd.DataFrame) -> float:
    say("-- gates against published BJS tables --")
    t1 = {"Total violent crime/b": None, "Robbery": None, "Aggravated assault": None, "Simple assault": None,
          "Rape/sexual assault/c": None}
    cols = {2022: 13, 2023: 17, 2024: 21}
    for yr, c in cols.items():
        tot = v[v.year == yr]
        pub = cv24_number("cv24t01.csv", "Total violent crime/b", c)
        got = tot.newwgt.sum()
        gate(f"{yr} violent victimizations vs CV2024 table 1", abs(got / pub - 1) < 0.005, f"{got:,.0f} vs {pub:,.0f}")
    for lab, code in [("Robbery", 2), ("Aggravated assault", 3), ("Simple assault", 4)]:
        pub = cv24_number("cv24t01.csv", lab, 21)
        got = v[(v.year == 2024) & (v.newoff == code)].newwgt.sum()
        gate(f"2024 {lab} vs CV2024 table 1", abs(got / pub - 1) < 0.005, f"{got:,.0f} vs {pub:,.0f}")
    for yr, col in [(2023, 5), (2024, 6)]:
        pub = cv24_number("cv24at19.csv", "Hispanic", col)
        got = p[(p.year == yr) & (p.g == "H")].w.sum()
        gate(f"{yr} Hispanic population 12+ vs CV2024 appendix table 19", abs(got / pub - 1) < 0.001,
             f"{got:,.0f} vs {pub:,.0f}")
    # reporting by victim ethnicity, CV2024 table 5
    for yr, col in [(2023, 2), (2024, 4)]:
        pub = cv24_number("cv24t05.csv", "Hispanic", col)
        x = v[(v.year == yr) & (v.vg == "H")]
        got = 100 * x.loc[x.notify == 1, "newwgt"].sum() / x.newwgt.sum()
        gate(f"{yr} Hispanic victims' reporting rate vs CV2024 table 5", abs(got - pub) < 0.6, f"{got:.1f} vs {pub:.1f}")
    # design effect: published SE of violent totals vs naive SE sqrt(sum w^2)
    deffs = []
    for yr, c in [(2022, 9), (2023, 12), (2024, 15)]:
        pub_se = cv24_number("cv24at02.csv", "Total violent crime", c)
        naive = float(np.sqrt((v.loc[v.year == yr, "newwgt"] ** 2).sum()))
        deffs.append((pub_se / naive) ** 2)
        say(f"   {yr}: published SE {pub_se:,.0f}, naive {naive:,.0f}, design effect {(pub_se / naive) ** 2:.2f}")
    deff = float(np.mean(deffs))
    say(f"   design effect used for all SEs: {deff:.2f}")
    return deff


def rates(v: pd.DataFrame, p: pd.DataFrame, years, regions, alloc: str, w: str = "newwgt",
          subset=None) -> pd.DataFrame:
    """Hispanic / NH-white and Hispanic / all offending ratios by offence for a window."""
    x = v[v.year.isin(years) & v.region.isin(regions)]
    if subset is not None:
        x = x[subset(x)]
    pp = p[p.year.isin(years) & p.region.isin(regions)].groupby("g").w.sum()
    rows = []
    for o in list(OFFN.values()) + ["Violent excl. simple assault", "All violent"]:
        if o == "All violent":
            xo = x
        elif o == "Violent excl. simple assault":
            xo = x[x.offence != "Simple assault"]
        else:
            xo = x[x.offence == o]
        m = xo.pivot_table(index="vg", columns="og", values=w, aggfunc="sum").reindex(
            index=GROUPS, columns=GROUPS + ["U", "MIX"]).fillna(0.0)
        known = m[GROUPS]
        unk = m["U"] + m["MIX"]
        if alloc == "known":
            V = known.sum()
        elif alloc == "victim":
            sh = known.div(known.sum(axis=1), axis=0).fillna(known.sum() / known.sum().sum())
            V = (known + sh.mul(unk, axis=0)).sum()
        elif alloc == "b":
            nh = known[["NHW", "NHB", "NHO"]]
            sh = nh.div(nh.sum(axis=1), axis=0).fillna(nh.sum() / nh.sum().sum())
            V = known.sum()
            V[["NHW", "NHB", "NHO"]] += sh.mul(unk, axis=0).sum()
        elif alloc == "c":
            V = known.sum()
            V["H"] += unk.sum()
        else:
            raise ValueError(alloc)
        r = {g: V[g] / pp[g] for g in GROUPS}
        rall = V.sum() / pp.sum()
        rows.append(dict(offence=o, RR_H_NHW=r["H"] / r["NHW"], RR_H_all=r["H"] / rall, RR_NHB_NHW=r["NHB"] / r["NHW"],
                         share_H_offending=V["H"] / V.sum(), share_unknown=float(unk.sum() / m.to_numpy().sum()),
                         victimizations=float(m.to_numpy().sum()), records=int(len(xo))))
    return pd.DataFrame(rows)


def boot_se(v, p, years, regions, alloc, deff, reps=300, subset=None) -> pd.DataFrame:
    base = rates(v, p, years, regions, alloc, subset=subset).set_index("offence")
    x = v[v.year.isin(years)]
    sims = []
    for _ in range(reps):
        idx = np.concatenate([rng.choice(g.index.to_numpy(), size=len(g), replace=True) for _, g in x.groupby("year")])
        sims.append(rates(x.loc[idx].reset_index(drop=True), p, years, regions, alloc, subset=subset)
                    .set_index("offence")[["RR_H_NHW", "RR_H_all"]])
    s = pd.concat(sims)
    sd = s.groupby(level=0).std() * np.sqrt(deff)
    base["se_RR_H_NHW"] = sd.RR_H_NHW
    base["se_RR_H_all"] = sd.RR_H_all
    return base.reset_index()


def reporting(v: pd.DataFrame, years, deff) -> pd.DataFrame:
    x = v[v.year.isin(years)].copy()
    x["rep"] = (x.notify == 1).astype(float)
    rows = []
    for o in list(OFFN.values()) + ["Violent excl. simple assault", "All violent"]:
        if o == "All violent":
            xo = x
        elif o == "Violent excl. simple assault":
            xo = x[x.offence != "Simple assault"]
        else:
            xo = x[x.offence == o]
        for dim, col, groups in [("victim", "vg", GROUPS), ("offender", "og", GROUPS + ["U", "MIX"])]:
            for g in groups:
                y = xo[xo[col] == g]
                if len(y) == 0:
                    continue
                pr = float((y.rep * y.newwgt).sum() / y.newwgt.sum())
                # naive SE of a weighted proportion (linearised), scaled by the design effect
                wn = y.newwgt / y.newwgt.sum()
                se = float(np.sqrt(((wn * (y.rep - pr)) ** 2).sum()) * np.sqrt(deff))
                rows.append(dict(years=f"{min(years)}-{max(years)}", offence=o, dimension=dim, group=g,
                                 pct_reported=100 * pr, se=100 * se, records=len(y), victimizations=float(y.newwgt.sum())))
        for vg in GROUPS:
            for og in GROUPS:
                y = xo[(xo.vg == vg) & (xo.og == og)]
                if len(y) < 10:
                    continue
                pr = float((y.rep * y.newwgt).sum() / y.newwgt.sum())
                wn = y.newwgt / y.newwgt.sum()
                se = float(np.sqrt(((wn * (y.rep - pr)) ** 2).sum()) * np.sqrt(deff))
                rows.append(dict(years=f"{min(years)}-{max(years)}", offence=o, dimension="pair",
                                 group=f"victim {vg} / offender {og}", pct_reported=100 * pr, se=100 * se,
                                 records=len(y), victimizations=float(y.newwgt.sum())))
    return pd.DataFrame(rows)


def visible_factors(v: pd.DataFrame, years, deff: float, reps: int = 300) -> pd.DataFrame:
    """How much a police-visible (reported) count overstates or understates the Hispanic offending
    share, by offence and victim group: P_rep(offender H | victim g) / P_all(offender H | victim g),
    unknown offenders allocated within the cell (known offenders only in each subset); and the
    same for the Hispanic / NH-white offending ratio. Bootstrap within year, SE x sqrt(deff)."""
    x0 = v[v.year.isin(years)]

    def stat(x):
        out = {}
        for o in list(OFFN.values()) + ["All violent"]:
            xo = x if o == "All violent" else x[x.offence == o]
            for g in GROUPS + ["all"]:
                y = xo if g == "all" else xo[xo.vg == g]
                k = y[y.og.isin(GROUPS)]
                kr = k[k.notify == 1]
                pa = k.loc[k.og == "H", "newwgt"].sum() / k.newwgt.sum() if k.newwgt.sum() > 0 else np.nan
                pr = kr.loc[kr.og == "H", "newwgt"].sum() / kr.newwgt.sum() if kr.newwgt.sum() > 0 else np.nan
                out[(o, g, "p_all")] = pa
                out[(o, g, "p_reported")] = pr
                out[(o, g, "factor")] = pr / pa if pa else np.nan
                # reporting rates of H-offender and NHW-offender victimizations in this victim group
                for og in ["H", "NHW"]:
                    z = k[k.og == og]
                    out[(o, g, f"rep_{og}")] = (z.newwgt * (z.notify == 1)).sum() / z.newwgt.sum() if z.newwgt.sum() else np.nan
        return pd.Series(out)

    base = stat(x0)
    sims = []
    for _ in range(reps):
        idx = np.concatenate([rng.choice(g.index.to_numpy(), size=len(g), replace=True) for _, g in x0.groupby("year")])
        sims.append(stat(x0.loc[idx]))
    se = pd.concat(sims, axis=1).std(axis=1) * np.sqrt(deff)
    t = pd.DataFrame({"estimate": base, "se": se})
    t.index = pd.MultiIndex.from_tuples(t.index, names=["offence", "victim", "stat"])
    t = t.reset_index()
    t.insert(0, "years", f"{min(years)}-{max(years)}")
    return t


def rhovo_control(v: pd.DataFrame) -> pd.DataFrame:
    """Positive control: NCJ 250747 table 6 (2012-15), percent reported by victim x offender."""
    pub = pd.read_csv(HERE.parent / "ncvs_victim_offender_2026_09_18/derived/rhovo_t6_reported_to_police.csv")
    nm = {"White": "NHW", "Black": "NHB", "Hispanic": "H"}
    x = v[v.year.between(2012, 2015)]
    rows = []
    for r in pub.itertuples():
        y = x[(x.vg == nm[r.victim]) & (x.og == nm[r.offender])]
        got = 100 * y.loc[y.notify == 1, "newwgt"].sum() / y.newwgt.sum()
        rows.append(dict(victim=r.victim, offender=r.offender, published_pct=r.pct_reported_to_police, microdata_pct=got,
                         published_avg_annual=r.avg_annual_number, microdata_avg_annual=y.newwgt.sum() / 4,
                         records=len(y)))
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    v, p = load()
    deff = gates(v, p)
    ctl = rhovo_control(v)
    say("\n-- Positive control: NCJ 250747 table 6, percent of violent victimizations reported, 2012-15 --")
    say(ctl.to_string(index=False, float_format=lambda x: f"{x:,.1f}"))
    gate("microdata reproduce NCJ 250747 table 6 reporting shares within 3 points and counts within 10%",
         bool(((ctl.microdata_pct - ctl.published_pct).abs() < 3).all()
              and ((ctl.microdata_avg_annual / ctl.published_avg_annual - 1).abs() < 0.10).all()),
         f"max |d pct| {(ctl.microdata_pct - ctl.published_pct).abs().max():.2f}, "
         f"max |d count| {(ctl.microdata_avg_annual / ctl.published_avg_annual - 1).abs().max():.3f}")
    ctl.to_csv(OUT / "ncvs_control_rhovo_t6.csv", index=False, float_format="%.3f", lineterminator="\n")

    windows = {"2012-2024": range(2012, 2025), "2017-2024": range(2017, 2025), "2022-2024": range(2022, 2025)}
    regions = {"US": [1, 2, 3, 4], "South+West": [3, 4], "South": [3], "West": [4]}
    rows = []
    for wn, yrs in windows.items():
        for rn, reg in regions.items():
            for alloc in ["victim", "known", "b", "c"]:
                if alloc == "victim" and rn in ("US", "South+West"):
                    r = boot_se(v, p, list(yrs), reg, alloc, deff)
                else:
                    r = rates(v, p, list(yrs), reg, alloc)
                r.insert(0, "allocation", alloc)
                r.insert(0, "region", rn)
                r.insert(0, "years", wn)
                rows.append(r)
            # reported to police only (the police-visible subset), and not reported
            for lab, fn in [("reported to police", lambda d: d.notify == 1), ("not reported", lambda d: d.notify == 2)]:
                if rn in ("US", "South+West"):
                    r = boot_se(v, p, list(yrs), reg, "victim", deff, subset=fn)
                else:
                    r = rates(v, p, list(yrs), reg, "victim", subset=fn)
                r.insert(0, "allocation", f"victim; {lab} only")
                r.insert(0, "region", rn)
                r.insert(0, "years", wn)
                rows.append(r)
    R = pd.concat(rows, ignore_index=True)
    R.to_csv(OUT / "ncvs_offender_ratios.csv", index=False, float_format="%.5f", lineterminator="\n")
    say("\n-- NCVS perceived offending, Hispanic / NH white (victim-conditional allocation) --")
    say(R[R.allocation.isin(["victim", "victim; reported to police only", "victim; not reported only", "known"])]
        .pivot_table(index=["years", "region", "allocation"], columns="offence", values="RR_H_NHW", sort=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n-- standard errors (design-effect scaled), US and South+West, victim allocation --")
    se = R[R.allocation.eq("victim") & R.region.isin(["US", "South+West"])][
        ["years", "region", "offence", "RR_H_NHW", "se_RR_H_NHW", "RR_H_all", "se_RR_H_all", "records"]]
    say(se.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    rep = pd.concat([reporting(v, list(yrs), deff) for yrs in windows.values()], ignore_index=True)
    rep.to_csv(OUT / "ncvs_reporting.csv", index=False, float_format="%.3f", lineterminator="\n")
    say("\n-- Percent reported to police, 2012-2024, by perceived offender and by victim --")
    say(rep[rep.years.eq("2012-2024") & rep.dimension.isin(["offender", "victim"])]
        .pivot_table(index=["dimension", "group"], columns="offence", values="pct_reported", sort=False)
        .to_string(float_format=lambda x: f"{x:.1f}"))
    vf = pd.concat([visible_factors(v, list(windows[w]), deff) for w in ["2012-2024", "2022-2024"]], ignore_index=True)
    vf.to_csv(OUT / "ncvs_police_visible_factors.csv", index=False, float_format="%.5f", lineterminator="\n")
    say("\n-- Police-visible factor: P(offender H | victim g) among reported / among all (known offenders) --")
    say(vf[vf.stat.isin(["p_all", "p_reported", "factor", "rep_H", "rep_NHW"])]
        .pivot_table(index=["years", "offence", "victim"], columns="stat", values="estimate", sort=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say(vf[vf.stat.eq("factor") & vf.victim.isin(["all", "NHW", "H"])][["years", "offence", "victim", "estimate", "se"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    (OUT / "ncvs_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
