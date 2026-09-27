"""GSS 2000-2024: Mexican-identifying respondents by generation (GRANBORN) against whites.

Generation masks are the generation_split_2026_09_20/analyze_gss.py definitions (G3/G4+ here are
generic: GRANBORN counts foreign-born grandparents of any country). Reference: non-Hispanic white,
US-born, both parents US-born (all GRANBORN), and alternatively white G4+ (GRANBORN=0).
Whites are reweighted to each group's age-band x sex mix. SEs: 400 bootstrap draws of
(year, VSTRAT, VPSU) clusters within year x stratum; ratios are formed within each draw.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta"
SHA = "a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344"
COLS = ["year", "born", "parborn", "granborn", "hispanic", "race", "sex", "age", "educ", "degree",
        "realrinc", "prestg10", "wrkstat", "wtssps", "vstrat", "vpsu"]
B = 400
GENS = ["G1", "G2", "G3_generic", "G4plus_generic", "G3plus_all"]
PAIRS = [("G1", "G2"), ("G2", "G3_generic"), ("G3_generic", "G4plus_generic"), ("G2", "G3plus_all")]


def load():
    if hashlib.sha256(SRC.read_bytes()).hexdigest() != SHA:
        raise ValueError("GSS source hash changed")
    d, m = pyreadstat.read_dta(SRC, usecols=COLS, encoding="latin1")
    assert m.variable_value_labels["hispanic"][2] == "mexican, mexican american, chicano/a"
    assert m.variable_value_labels["degree"][3] == "bachelor's"
    d = d.apply(pd.to_numeric, errors="coerce")
    d = d[d.year.ge(2000) & d.wtssps.gt(0)].copy()
    d["gen"] = np.select(
        [d.born.eq(2), d.born.eq(1) & d.parborn.isin([1, 2, 4, 6, 8]),
         d.born.eq(1) & d.parborn.eq(0) & d.granborn.between(1, 4),
         d.born.eq(1) & d.parborn.eq(0) & d.granborn.eq(0)],
        ["G1", "G2", "G3_generic", "G4plus_generic"], default="unknown")
    mex = d.hispanic.eq(2)
    white = d.race.eq(1) & d.hispanic.eq(1) & d.born.eq(1) & d.parborn.eq(0)
    d["grp"] = np.where(mex, "M_" + d.gen, np.where(white, "W", ""))
    d["W4"] = white & d.granborn.eq(0)
    d["G3plus_all"] = mex & d.born.eq(1) & d.parborn.eq(0)
    d["cell"] = np.digitize(d.age, [35, 45, 55]) * 2 + (d.sex - 1)
    d["ba"] = (d.degree >= 3).astype(float).where(d.degree.between(0, 4))
    d["lths"] = (d.degree == 0).astype(float).where(d.degree.between(0, 4))
    d["educ_years"] = d.educ.where(d.educ.between(0, 20))
    d["employed"] = d.wrkstat.isin([1, 2, 3]).astype(float).where(d.wrkstat.between(1, 8))
    d["log_realrinc"] = np.log(d.realrinc.where(d.realrinc > 0))
    d["realrinc_v"] = d.realrinc.where(d.realrinc > 0)
    d["prestige"] = d.prestg10.where(d.prestg10 > 0)
    d["clu"] = d.year.astype(int).astype(str) + "_" + d.vstrat.astype("Int64").astype(str) + "_" + d.vpsu.astype("Int64").astype(str)
    return d


MEASURES = {"ba_plus": ("ba", 100), "less_than_hs": ("lths", 100), "educ_years": ("educ_years", 1),
            "employed": ("employed", 100), "log_realrinc": ("log_realrinc", 1),
            "realrinc_1986usd": ("realrinc_v", 1), "prestige_prestg10": ("prestige", 1)}


def gaps_once(d, w, refname):
    out = {}
    age_ok = d.age.between(25, 64)
    for m, (col, sc) in MEASURES.items():
        ok = age_ok & d[col].notna()
        ref = ok & (d.grp.eq("W") if refname == "white_USparents" else d.W4)
        rc = d.cell[ref].to_numpy().astype(int)
        rw = w[ref.to_numpy()]
        rx = d[col][ref].to_numpy()
        for g in GENS:
            use = ok & (d.G3plus_all if g == "G3plus_all" else d.grp.eq("M_" + g))
            if use.sum() == 0:
                continue
            gw = w[use.to_numpy()]
            gc = d.cell[use].to_numpy().astype(int)
            sg = np.bincount(gc, weights=gw, minlength=8)
            sr = np.bincount(rc, weights=rw, minlength=8)
            f = np.divide(sg / sg.sum(), sr, out=np.zeros(8), where=sr > 0)
            wr = rw * f[rc]
            v = np.average(d[col][use], weights=gw) * sc
            r = np.average(rx, weights=wr) * sc
            out[(m, g)] = (v, r, v - r, int(use.sum()), float(np.average(d.age[use], weights=gw)))
    return out


def main():
    d = load()
    d = d[(d.grp != "") | d.G3plus_all].reset_index(drop=True)
    rng = np.random.default_rng(20260927)
    w0 = d.wtssps.to_numpy()
    rows, crows = [], []
    for refname in ["white_USparents", "white_G4plus"]:
        base = gaps_once(d, w0, refname)
        # Cluster bootstrap: resample clusters within year x stratum; multiplicity scales weights.
        strata = d.year.astype(int).astype(str) + "_" + d.vstrat.astype("Int64").astype(str)
        clu_codes, clu_idx = np.unique(d.clu, return_inverse=True)
        clu_stratum = pd.Series(strata.to_numpy()).groupby(clu_idx).first()
        by_stratum = {s: np.array(idx) for s, idx in clu_stratum.groupby(clu_stratum).groups.items()}
        boots = []
        for _ in range(B):
            mult = np.zeros(len(clu_codes))
            for s, cl in by_stratum.items():
                draw = rng.choice(cl, size=len(cl), replace=True)
                np.add.at(mult, draw, 1)
            boots.append(gaps_once(d, w0 * mult[clu_idx], refname))
        for k, (v, r, gap, n, age) in base.items():
            bs = np.array([b[k][2] for b in boots if k in b])
            rows.append(dict(source="GSS_2000_2024", frame=f"age 25-64, ref {refname}", measure=k[0], generation=k[1],
                             n=n, mean_age=age, value=v, ref_value_age_matched=r, gap=gap, se=float(bs.std(ddof=1))))
        for m in MEASURES:
            for a, b in PAIRS:
                if (m, a) not in base or (m, b) not in base:
                    continue
                rho = base[(m, b)][2] / base[(m, a)][2]
                br = np.array([bb[(m, b)][2] / bb[(m, a)][2] for bb in boots if (m, a) in bb and (m, b) in bb])
                bd = np.array([bb[(m, b)][2] - bb[(m, a)][2] for bb in boots if (m, a) in bb and (m, b) in bb])
                sa = np.std([bb[(m, a)][2] for bb in boots], ddof=1)
                crows.append(dict(source="GSS_2000_2024", frame=f"age 25-64, ref {refname}", measure=m,
                                  generation=f"{a}->{b}", n=base[(m, b)][3], gap_from=base[(m, a)][2],
                                  gap_to=base[(m, b)][2], rho=rho, se=float(np.std(br, ddof=1)),
                                  rho_p05=float(np.percentile(br, 5)), rho_p95=float(np.percentile(br, 95)),
                                  change_in_gap=base[(m, b)][2] - base[(m, a)][2], se_change=float(np.std(bd, ddof=1)),
                                  denominator_stable=bool(abs(base[(m, a)][2]) > 2 * sa)))
    for name, rr in [("gss_gaps.csv", rows), ("gss_carryover.csv", crows)]:
        with open(HERE / "derived" / name, "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rr[0]), lineterminator="\n")
            wr.writeheader()
            wr.writerows(rr)
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print(pd.DataFrame(crows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
