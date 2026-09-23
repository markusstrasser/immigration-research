#!/usr/bin/env python3
"""External check of the 2000-census birthplace allocation against administrative prison counts,
and its effect on Rumbaut et al. (2006) Table 1.

Admin floor (prisons only; jails, INS detention and other institutions come on top):
  BJS, Prison and Jail Inmates at Midyear 2002 (NCJ 198877), Table 6: noncitizens held in State or
  Federal prisons at midyear 2000 = 89,676 (Federal 36,090, State 53,586); by jurisdiction only for
  6/30/2001: California 20,616, Texas 7,332.
Census side: IPUMS extract `census2000_inst` (2000 5% sample, every institutional person, all ages,
both sexes, with QBPL/QCITIZEN). Noncitizen = foreign-born with CITIZEN 3 (not a citizen).
Reassignment as in analyze_census.reassignment: records whose birthplace was allocated to a US
state are spread over nativity x citizenship groups in the mix of records with a reported
birthplace, within state group (CA, TX, rest) x sex x race/Hispanic origin. nativity_high spreads
all of them; nativity_low spreads the share measured in 1990 (institutional men 18-40 whose
citizenship item was allocated too, from extract `census_inst_q`). The 2000 file never flags
citizenship for the US-born, so 2000 itself cannot be split.

Rumbaut: men 18-39, Hispanic origin Mexican (HISPAN 1), US-born (BPL < 100) vs foreign-born
(BPL >= 150), institutional share (GQ 3; Rumbaut used the census "correctional" category, which the
IPUMS 2000 file does not separate). Population from extracts `census` + `census_q`.

Run from the repository root (after the extracts are downloaded):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/admin_check.py
Out: derived/admin_check_2000.csv, derived/rumbaut_2000.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
IPUMS = HERE / "_cache" / "ipums"
DERIVED = HERE / "derived"
GROUPS = ["us", "mex_noncit", "mex_nat", "oth_noncit", "oth_nat", "other"]


def p_1990() -> float:
    q = pd.read_csv(IPUMS / "census_inst_q.csv.gz", usecols=["YEAR", "PERWT", "BPL", "QBPL", "QCITIZEN"])
    m = (q.YEAR == 1990) & (q.BPL < 100) & (q.QBPL > 0)
    return float(q.PERWT[m & (q.QCITIZEN > 0)].sum() / q.PERWT[m].sum())


def subgroup(d: pd.DataFrame) -> np.ndarray:
    nh = d.HISPAN == 0
    return np.select([nh & (d.RACE == 1), nh & (d.RACE == 2), d.HISPAN == 1, d.HISPAN.between(2, 4)],
                     ["nhw", "nhb", "mexorig", "hisp_other"], "other")


def spread(d: pd.DataFrame, cats: list[str], keys: list[str], p: float) -> pd.DataFrame:
    """Weighted counts by keys x category after moving a share p of the allocated-to-US pool into
    the reported mix of its keys cell."""
    rows = []
    for k, g in d.groupby(keys):
        cur = g.groupby("cat").PERWT.sum().reindex(cats, fill_value=0.0)
        rep = g[g.QBPL == 0].groupby("cat").PERWT.sum().reindex(cats, fill_value=0.0)
        u = p * g.PERWT[(g.QBPL > 0) & (g.cat == "us")].sum()
        if rep.sum() > 0:
            cur["us"] -= u
            cur += u * rep / rep.sum()
        rows.append(pd.Series(cur, name=k if isinstance(k, tuple) else (k,)))
    out = pd.DataFrame(rows)
    out.index = pd.MultiIndex.from_tuples(out.index, names=keys)
    return out


def admin_counts(p_low: float) -> pd.DataFrame:
    d = pd.read_csv(IPUMS / "census2000_inst.csv.gz")
    if not (d.GQ == 3).all():
        raise SystemExit("[FAILED] census2000_inst holds non-institutional records")
    fb = (d.BPL >= 150) & (d.BPL < 900) & (d.CITIZEN != 1)
    noncit = d.CITIZEN.isin([3, 4, 5])
    d["cat"] = np.select([d.BPL < 100, fb & (d.BPL == 200) & noncit, fb & (d.BPL == 200),
                          fb & noncit, fb], GROUPS[:5], "other")
    d["sub"] = subgroup(d)
    d["state"] = np.select([d.STATEFIP == 6, d.STATEFIP == 48], ["CA", "TX"], "rest")
    d["men_18_64"] = (d.SEX == 1) & d.AGE.between(18, 64)
    rows = []
    for variant, p in (("as_published", 0.0), ("nativity_low", p_low), ("nativity_high", 1.0)):
        t = spread(d, GROUPS, ["state", "SEX", "sub"], p)
        t18 = spread(d[d.men_18_64], GROUPS, ["state", "sub"], p)
        for scope, cond in (("US", None), ("CA", "CA"), ("TX", "TX")):
            a = t if cond is None else t.xs(cond, level="state", drop_level=False)
            m = t18 if cond is None else t18.xs(cond, level="state", drop_level=False)
            sel = pd.Series(True, index=d.index) if cond is None else d.state == cond
            rows.append(dict(variant=variant, scope=scope, share_spread=p,
                             noncitizen_all=float(a[["mex_noncit", "oth_noncit"]].sum().sum()),
                             noncitizen_mexico_born=float(a["mex_noncit"].sum()),
                             noncitizen_men=float(a.xs(1, level="SEX")[["mex_noncit", "oth_noncit"]].sum().sum()),
                             noncitizen_men_18_64=float(m[["mex_noncit", "oth_noncit"]].sum().sum()),
                             foreign_born_all=float(a[GROUPS[1:5]].sum().sum()),
                             institutional_total=float(a.sum().sum()),
                             birthplace_allocated_share=float(d.PERWT[(d.QBPL > 0) & sel].sum() / d.PERWT[sel].sum())))
    return pd.DataFrame(rows)


def rumbaut(p_low: float) -> pd.DataFrame:
    cols = ["YEAR", "SERIAL", "PERNUM", "PERWT", "GQ", "AGE", "BPL", "HISPAN", "RACE", "CITIZEN"]
    c = pd.read_csv(IPUMS / "census.csv.gz", usecols=cols)
    c = c[(c.YEAR == 2000) & c.AGE.between(18, 39) & (c.HISPAN == 1)]
    q = pd.read_csv(IPUMS / "census_q.csv.gz", usecols=["YEAR", "SERIAL", "PERNUM", "QBPL"])
    c = c.merge(q[q.YEAR == 2000], on=["YEAR", "SERIAL", "PERNUM"], how="left", validate="1:1")
    if c.QBPL.isna().any():
        raise SystemExit("[FAILED] census_q misses records of census")
    c["cat"] = np.select([c.BPL < 100, c.BPL >= 150], ["us", "foreign"], "other")
    c["inst"] = np.where(c.GQ == 3, "inst", "non")
    rows = []
    for variant, p in (("as_published", 0.0), ("nativity_low", p_low), ("nativity_high", 1.0)):
        t = spread(c, ["us", "foreign", "other"], ["inst"], p)
        pop = t.sum()
        for cat in ("foreign", "us"):
            rows.append(dict(variant=variant, group=f"{cat}_mexican_origin_men_18_39",
                             institutional=float(t.loc[("inst",), cat]), population=float(pop[cat]),
                             rate=float(t.loc[("inst",), cat] / pop[cat])))
    out = pd.DataFrame(rows)
    ratio = out.pivot(index="variant", columns="group", values="rate")
    out["us_over_foreign"] = out.variant.map(ratio["us_mexican_origin_men_18_39"] / ratio["foreign_mexican_origin_men_18_39"])
    return out


def main() -> None:
    p = p_1990()
    a = admin_counts(p)
    a.to_csv(DERIVED / "admin_check_2000.csv", index=False, float_format="%.6g")
    r = rumbaut(p)
    r.to_csv(DERIVED / "rumbaut_2000.csv", index=False, float_format="%.6g")
    pd.set_option("display.width", 250)
    print(f"  share spread in nativity_low: {p:.3f}")
    print(a.round(3).to_string(index=False))
    print(r.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
