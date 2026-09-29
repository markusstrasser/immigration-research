#!/usr/bin/env python3
"""Who is here now: the India-born stock by arrival wave, the US-born with an India-born parent,
and India-born adults by language spoken at home.

1. India-born stock, ACS 2024 (all ages, group quarters included): weighted count, share and age
   distribution by arrival cohort.
2. US-born with an India-born parent:
   - CPS ASEC 2024-2025 (IPUMS extract, all ages; FBPL or MBPL = India; mean of the two years'
     weights): total and age distribution. The CPS has parents' birthplace but not their arrival year.
   - ACS 2024: US-born children of the householder (any age, co-resident only) with an India-born
     householder or spouse, by that parent's arrival cohort (the earlier-arriving India-born parent
     when both are).
3. Language at home (ACS 2021-2024 pooled; Census PUMS LANP, 2016+ code frame, which carries the same
   languages as IPUMS LANGUAGED; LANX 2 = English only). The language x cohort table adds 2020+
   noncitizen arrivals 18+ split by BA status. Language is
   a proxy for the home region in India, not for caste or religion. Adults 25-64 for outcomes, age-
   standardised to the pooled India-born 25-64 age mix; stock is the four-year mean of weights.
   Children: US-born children 0-17 of the householder, classified by their India-born parent's
   language (householder first, else spouse).

Outputs: derived/stock_by_cohort.csv, derived/g2_stock.csv, derived/language_profile.csv,
         derived/language_by_cohort.csv, derived/language_children.csv
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/stock_language.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import acs_cohorts as A  # noqa: E402

cps_curve = C.cps_curve
AGES = [(0, 17), (18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 120)]
LANG = {1350: "Hindi", 1450: "Gujarati", 1730: "Telugu", 1765: "Tamil", 1420: "Punjabi",
        1380: "Bengali", 1750: "Malayalam", 1440: "Marathi", 1737: "Kannada", 1360: "Urdu"}
CPS_SRC = C.SC.parents[2] / "sources" / "immigration-fiscal" / "data" / "external" / "cps" / "cps_2ndgen.csv.gz"


def age_group(a: pd.Series) -> pd.Series:
    out = pd.Series("", index=a.index)
    for lo, hi in AGES:
        out[(a >= lo) & (a <= hi)] = f"{lo}-{hi}" if hi < 120 else "65+"
    return out


def stock_by_cohort(d: pd.DataFrame) -> list[dict]:
    s = d[(d.YEAR == 2024) & d.india].copy()
    s["ag"] = age_group(s.AGEP)
    tot = s.PWGTP.sum()
    rows = []
    for lab in ["all"] + [c[2] for c in C.COHORTS]:
        g = s if lab == "all" else s[s.cohort == lab]
        w = g.PWGTP
        row = {"survey": "ACS 2024", "cohort": lab, "n": len(g), "weighted": float(w.sum()),
               "share_of_india_born": float(w.sum() / tot), "mean_age": float(np.average(g.AGEP, weights=w)),
               "median_age": float(g.AGEP.repeat(w.astype(int)).median())}
        for lo, hi in AGES:
            k = f"{lo}-{hi}" if hi < 120 else "65+"
            row[f"age_{k}"] = float(w[g.ag == k].sum() / w.sum())
        rows.append(row)
    return rows


def g2_stock(d: pd.DataFrame) -> list[dict]:
    q = f"""SELECT YEAR AS year, AGE AS age, CAST(ASECWT AS DOUBLE) AS w, FBPL AS fbpl, MBPL AS mbpl
            FROM read_csv_auto('{CPS_SRC}', header=true)
            WHERE YEAR IN (2024, 2025) AND NATIVITY IN (2, 3, 4) AND (FBPL = 52100 OR MBPL = 52100)"""
    c = duckdb.sql(q).df()
    c["w"] = c.w / 2
    c["ag"] = age_group(c.age)
    rows = []
    for lab, g in (("either parent India-born", c),
                   ("both parents India-born", c[(c.fbpl == 52100) & (c.mbpl == 52100)])):
        row = {"source": "CPS ASEC 2024-25", "group": lab, "parent_cohort": "not observed", "n": len(g),
               "weighted": float(g.w.sum())}
        for lo, hi in AGES:
            k = f"{lo}-{hi}" if hi < 120 else "65+"
            row[f"age_{k}"] = float(g.w[g.ag == k].sum() / g.w.sum())
        rows.append(row)
    # ACS 2024 co-resident children of the householder, by India-born parent's arrival cohort
    h = d[d.YEAR == 2024]
    codes = A.REL["new"]
    par = h[h.rel.isin(codes["head"] | codes["spouse"]) & h.india]
    pc = par.groupby("SERIALNO").YOEP.min()
    kids = h[h.rel.isin(codes["child"]) & (h.NATIVITY == 1)].join(pc.rename("par_yoep"), on="SERIALNO")
    kids = kids[kids.par_yoep.notna()].copy()
    kids["par_cohort"] = C.cohort_of(kids.par_yoep.to_numpy())
    kids["ag"] = age_group(kids.AGEP)
    for lab in ["all"] + [c[2] for c in C.COHORTS]:
        g = kids if lab == "all" else kids[kids.par_cohort == lab]
        if len(g) == 0:
            continue
        w = g.PWGTP.astype(float)
        row = {"source": "ACS 2024 co-resident", "group": "US-born child of householder, India-born parent",
               "parent_cohort": lab, "n": len(g), "weighted": float(w.sum())}
        for lo, hi in AGES:
            k = f"{lo}-{hi}" if hi < 120 else "65+"
            row[f"age_{k}"] = float(w[g.ag == k].sum() / w.sum())
        rows.append(row)
    return rows


def lang_of(d: pd.DataFrame) -> pd.Series:
    lab = d.LANP.map(LANG).fillna("other language")
    lab[d.LANX == 2] = "English only"
    lab[d.LANX.isna()] = "not asked (under 5)"
    return lab


def language(d: pd.DataFrame) -> tuple[list[dict], list[dict], list[dict]]:
    p = d[(d.YEAR >= 2021) & d.india].copy()
    p["lang"] = lang_of(p)
    p["occ_truck"] = p.SOCP.fillna("").astype(str).str.startswith("5330")
    order = list(LANG.values()) + ["English only", "other language"]
    adults = p[(p.band >= 0) & p.civ].copy()
    adults["w"] = adults.PWGTP.astype(float)
    rs = adults.groupby("band").w.sum() / adults.w.sum()
    prof = []
    for lab in ["all"] + order:
        g = adults if lab == "all" else adults[adults.lang == lab]
        allages = p if lab == "all" else p[p.lang == lab]
        row = {"language": lab, "n_adults_25_64": len(g), "stock_all_ages": float(allages.PWGTP.sum() / 4),
               "stock_25_64": float(g.w.sum() / 4)}
        for var in ("p_edu", "p_earn"):
            m = g[var].notna().to_numpy()
            ws = cps_curve.std_weights(g, m, rs)
            row[f"{var}_mean"], row[f"{var}_se"] = cps_curve.wmean_se(g.loc[m, var].to_numpy(), ws)
        w = cps_curve.std_weights(g, np.ones(len(g), bool), rs)
        emp = g.employed.to_numpy(bool)
        for c in ("ba_plus", "graduate", "citizen", "employed"):
            row[c] = A.wshare(w, g[c].to_numpy(bool))
        for c in ("occ_computer", "occ_physician", "occ_health_pract", "ind_retail", "ind_accom_food",
                  "occ_truck", "self_emp"):
            row[f"{c}_of_employed"] = A.wshare(w, g[c].to_numpy(bool), emp)
        cw = g.w.to_numpy()
        for _, _, cl in C.COHORTS:
            row[f"cohort_{cl}"] = float(cw[(g.cohort == cl).to_numpy()].sum() / cw.sum())
        prof.append(row)
    # language x arrival cohort, India-born 18+, column shares (which languages each wave brought)
    a18 = p[p.AGEP >= 18]
    xt = []
    for _, _, cl in C.COHORTS:
        g = a18[a18.cohort == cl]
        tot = g.PWGTP.sum()
        row = {"cohort": cl, "n": len(g), "weighted_avg_2021_24": float(tot / 4)}
        for lab in order:
            row[lab] = float(g.PWGTP[g.lang == lab].sum() / tot)
        xt.append(row)
    # the post-2020 inflow the surveys see least well: noncitizens 18+ arrived 2020+, by BA status
    rec = a18[(a18.YOEP >= 2020) & (a18.CIT == 5)]
    for lab, g in (("2020+ noncitizen, BA+", rec[rec.ba_plus]), ("2020+ noncitizen, no BA", rec[~rec.ba_plus]),
                   ("2020+ noncitizen, no BA, status residual", rec[~rec.ba_plus & rec.status_unauth_residual])):
        tot = g.PWGTP.sum()
        row = {"cohort": lab, "n": len(g), "weighted_avg_2021_24": float(tot / 4)}
        for ln in order:
            row[ln] = float(g.PWGTP[g.lang == ln].sum() / tot)
        xt.append(row)
    # children: US-born children 0-17 of the householder, by India-born parent's language
    h = d[d.YEAR >= 2021].copy()
    h["lang"] = lang_of(h)
    codes = A.REL["new"]
    heads = h[h.rel.isin(codes["head"]) & h.india][["YEAR", "SERIALNO", "lang"]]
    sps = h[h.rel.isin(codes["spouse"]) & h.india][["YEAR", "SERIALNO", "lang"]]
    pl = pd.concat([heads, sps]).drop_duplicates(["YEAR", "SERIALNO"], keep="first")
    kids = h[h.rel.isin(codes["child"]) & (h.NATIVITY == 1) & (h.AGEP <= 17)].merge(
        pl, on=["YEAR", "SERIALNO"], suffixes=("", "_par"))
    kt = kids.PWGTP.sum()
    ch = [{"parent_language": lab, "n": int((kids.lang_par == lab).sum()),
           "children_avg_2021_24": float(kids.PWGTP[kids.lang_par == lab].sum() / 4),
           "share": float(kids.PWGTP[kids.lang_par == lab].sum() / kt)} for lab in order]
    return prof, xt, ch


def main() -> int:
    cps = C.cps_prepared()
    ref = C.Reference(cps)
    d = A.prepare(A.load(), ref)
    for y in (2016, 2019, 2021, 2024):
        codes = d[(d.YEAR == y) & d.india].LANP.value_counts().head(12)
        if not set(LANG) & set(codes.index.astype(int)):
            raise SystemExit(f"[BLOCKED] LANP code frame differs in {y}: {codes.to_dict()}")
    C.write_csv(C.DER / "stock_by_cohort.csv", stock_by_cohort(d))
    C.write_csv(C.DER / "g2_stock.csv", g2_stock(d))
    prof, xt, ch = language(d)
    C.write_csv(C.DER / "language_profile.csv", prof)
    C.write_csv(C.DER / "language_by_cohort.csv", xt)
    C.write_csv(C.DER / "language_children.csv", ch)
    pd.set_option("display.width", 300)
    for f in ("stock_by_cohort", "g2_stock", "language_profile", "language_by_cohort", "language_children"):
        print(f"== {f}")
        print(pd.read_csv(C.DER / f"{f}.csv").round(3).T.to_string() if f == "language_profile"
              else pd.read_csv(C.DER / f"{f}.csv").round(3).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
