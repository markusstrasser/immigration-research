"""MASP (Telles-Ortiz) adult children, 1998-2002: G2 / G3 / G4+ levels and gaps to an external
white benchmark.

Generation reconstruction is copied from masp_2026_09_20/analyze.py (O2-only principal lineage;
c28/c29 reverse coding translated). MASP has no white sample, so the gap reference is GSS
2000-2004 (HISPANIC is first asked in 2000) non-Hispanic whites with US-born parents, reweighted to each MASP group's age bands
(external benchmark, national, not LA/San Antonio). SEs: 1,000 bootstrap draws of original
families (sibling clusters); the GSS benchmark is held fixed (its SE is small by comparison).
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "masp_2026_09_20/raw/masp_combined.dta"
SHA = "3aeb2699940a41cfebf14e7f46ab3c76218f5f85ede68b9b8a1615c69e9b4aae"
GSS = HERE.parent / "attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta"
B = 1000
BANDS = [30, 35, 40, 45, 50]


def masp():
    if hashlib.sha256(SRC.read_bytes()).hexdigest() != SHA:
        raise ValueError("MASP hash changed")
    raw, _ = pyreadstat.read_dta(SRC)
    d = raw[raw.v3.notna()].copy()
    assert len(d) == 758
    own = d.v75.where(d.v75.isin([1, 2, 3]))
    p1 = d.v75_O2.where(d.v75_O2.isin([1, 2, 3]))
    p2 = d.c19.where(d.c19.isin([1, 2, 3]))
    gp = pd.DataFrame({"a": d.v87_O2.where(d.v87_O2.isin([1, 2, 3])), "b": d.v91_O2.where(d.v91_O2.isin([1, 2, 3])),
                       "c": d.c28.map({1: 2, 2: 1, 3: 3}), "e": d.c29.map({1: 2, 2: 1, 3: 3})})
    parents_us = own.eq(1) & p1.eq(1) & p2.eq(1)
    d["generation"] = np.select(
        [own.eq(2), own.eq(3), own.eq(1) & (p1.isin([2, 3]) | p2.isin([2, 3])),
         parents_us & gp.isin([2, 3]).any(axis=1), parents_us & gp.eq(1).all(axis=1)],
        ["G1_Mexico", "G1_other", "G2", "G3", "G4plus"], default="Unresolved")
    counts = d.generation.value_counts().to_dict()
    # Gate: principal counts of masp_2026_09_20 RESULT.md.
    assert counts == {"G3": 245, "Unresolved": 232, "G2": 205, "G4plus": 38, "G1_Mexico": 35, "G1_other": 3}, counts
    d["ba_plus"] = d.v140.isin([5, 6, 7]).astype(float).where(d.v140.between(0, 7))
    d["grade_under12"] = d.v139.lt(12).astype(float).where(d.v139.between(0, 17))
    d["income_under30k"] = d.v348.between(1, 7).astype(float).where(d.v348.between(1, 21))
    ben = pd.DataFrame({k: d[f].eq(1).astype(float).where(d[f].isin([1, 2])) for k, f in
                        [("ssi", "v338"), ("afdc", "v340"), ("fs", "v341")]})
    d["any_three_benefits"] = ben.eq(1).any(axis=1).astype(float).where(ben.eq(1).any(axis=1) | ben.notna().all(axis=1))
    d["age"] = (d.v7 - d.v74).where(d.v74.between(1900, 1985))
    return d


def gss_ref():
    g, _ = pyreadstat.read_dta(GSS, usecols=["year", "born", "parborn", "hispanic", "race", "age", "degree", "educ", "wtssps"], encoding="latin1")
    g = g.apply(pd.to_numeric, errors="coerce")
    g = g[g.year.between(2000, 2004) & g.race.eq(1) & g.hispanic.eq(1) & g.born.eq(1) & g.parborn.eq(0) & g.wtssps.gt(0)]
    g = g[g.age.between(22, 70)].copy()
    g["ba_plus"] = (g.degree >= 3).astype(float).where(g.degree.between(0, 4))
    # MASP grade<12 counts years of schooling; the GSS analogue is EDUC<12.
    g["grade_under12"] = (g.educ < 12).astype(float).where(g.educ.between(0, 20))
    g["band"] = np.digitize(g.age, BANDS)
    return g


def ref_value(g, col, bands_share):
    x = g[g[col].notna()]
    by = x.groupby("band").apply(lambda s: np.average(s[col], weights=s.wtssps), include_groups=False)
    return float(sum(bands_share.get(b, 0) * by.get(b, np.nan) for b in bands_share)) * 100


def main():
    d = masp()
    g = gss_ref()
    rng = np.random.default_rng(20260927)
    fams = d.id.unique()
    fam_idx = {f: d.index[d.id == f] for f in fams}
    rows, crows = [], []
    gens = ["G2", "G3", "G4plus"]
    stats = {}
    for col in ["ba_plus", "grade_under12", "income_under30k", "any_three_benefits"]:
        for gen in gens:
            s = d[d.generation.eq(gen) & d[col].notna() & d.age.notna()]
            share = (np.digitize(s.age, BANDS)).astype(int)
            share = pd.Series(share).value_counts(normalize=True).to_dict()
            ref = ref_value(g, col, share) if col in ("ba_plus", "grade_under12") else np.nan
            stats[(col, gen)] = (s[col].mean() * 100, ref, share)
            rows.append(dict(source="MASP_1998_2002", frame="adult children of 1965 LA/San Antonio respondents; external GSS white ref",
                             measure=col, generation=gen, n=len(s), families=s.id.nunique(), mean_age=float(s.age.mean()),
                             value=s[col].mean() * 100, ref_value_age_matched=ref,
                             gap=s[col].mean() * 100 - ref if not np.isnan(ref) else np.nan, se=np.nan))
    # Family-cluster bootstrap of levels (reference held at its point value).
    boot = {k: [] for k in stats}
    for _ in range(B):
        draw = rng.choice(fams, size=len(fams), replace=True)
        bd = d.loc[np.concatenate([fam_idx[f] for f in draw])]
        for (col, gen) in stats:
            s = bd[bd.generation.eq(gen) & bd[col].notna() & bd.age.notna()]
            boot[(col, gen)].append(s[col].mean() * 100 if len(s) else np.nan)
    for r in rows:
        r["se"] = float(np.nanstd(boot[(r["measure"], r["generation"])], ddof=1))
        r["se_value"] = r["se"]
    for col in ["ba_plus", "grade_under12"]:
        for a, b in [("G2", "G3"), ("G3", "G4plus"), ("G2", "G4plus")]:
            ga = np.array(boot[(col, a)]) - stats[(col, a)][1]
            gb = np.array(boot[(col, b)]) - stats[(col, b)][1]
            pa, pb = stats[(col, a)][0] - stats[(col, a)][1], stats[(col, b)][0] - stats[(col, b)][1]
            rho = gb / ga
            crows.append(dict(source="MASP_1998_2002", frame="external GSS 2000-2004 white ref", measure=col,
                              generation=f"{a}->{b}", n=next(r["n"] for r in rows if r["measure"] == col and r["generation"] == b),
                              gap_from=pa, gap_to=pb, rho=pb / pa, se=float(np.nanstd(rho, ddof=1)),
                              rho_p05=float(np.nanpercentile(rho, 5)), rho_p95=float(np.nanpercentile(rho, 95)),
                              change_in_gap=pb - pa, se_change=float(np.nanstd(gb - ga, ddof=1)),
                              denominator_stable=bool(abs(pa) > 2 * np.nanstd(ga, ddof=1))))
    for name, rr in [("masp_gaps.csv", rows), ("masp_carryover.csv", crows)]:
        with open(HERE / "derived" / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rr[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rr)
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(2).to_string(index=False))
    print(pd.DataFrame(crows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
