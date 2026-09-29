#!/usr/bin/env python3
"""India-born adults by arrival cohort, ACS one-year PUMS 2005-2024 (no 2020), and the parents of
today's children with an India-born parent.

Every adult 25-64 is placed in the selection-curve reference (CPS ASEC G3+ NH white, same survey
year and five-year age band) through `common.Reference`; ACS wages are moved to 2024 dollars with
the selection-curve lane's CPI table (ACS year Y dollars -> factor of ASEC year Y+1).

Outputs:
  derived/acs_cohorts.csv          cohort x view: n, percentiles, BA+/graduate, occupation, industry,
                                   self-employment, citizenship, degree field, status proxy
  derived/acs_future_g2_parents.csv children 0-17 with an India-born householder or spouse, by
                                   survey year: parents' cohort mix and child-weighted percentiles
  derived/acs_calibration.csv      ACS vs CPS India-born mean percentiles on the same years
  derived/acs_recent_arrivals.csv  India-born noncitizens 18-64 by arrival year, ACS 2023 and 2024
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/acs_cohorts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

cps_curve = C.cps_curve
YEARS = list(range(2005, 2020)) + [2021, 2022, 2023, 2024]

# household relationship codes by ACS vintage
REL = {"old": {"gq": {13, 14}, "child": {2}, "head": {0}, "spouse": {1, 10}},        # 2005-2007 REL
       "mid": {"gq": {16, 17}, "child": {2, 3, 4}, "head": {0}, "spouse": {1, 13}},  # 2008-2018
       "new": {"gq": {37, 38}, "child": {25, 26, 27}, "head": {20}, "spouse": {21, 22, 23, 24}}}
# Borjas rule (h), SOC prefixes for licensed occupations [INFERENCE: the paper lists examples only]
LICENSED_SOC = ("291", "2310", "332", "333", "5320")
FOD = [("computer/IT", (2100, 2199)), ("engineering", (2400, 2599)), ("health/medicine", (6100, 6199)),
       ("business", (6200, 6299)), ("math/physical/life science", (3600, 5099))]


def vintage(y: int) -> str:
    return "old" if y <= 2007 else "mid" if y <= 2018 else "new"


def load() -> pd.DataFrame:
    frames = []
    for y in YEARS:
        d = pd.read_parquet(C.CACHE / f"acs_india_{y}.parquet")
        d["rel"] = d[[c for c in ("REL", "RELP", "RELSHIPP") if c in d][0]]
        adj = d["ADJINC"] if "ADJINC" in d else d["ADJUST"]
        d["adj"] = adj / 1e6
        d["vint"] = vintage(y)
        frames.append(d.drop(columns=[c for c in ("REL", "RELP", "RELSHIPP", "ADJINC", "ADJUST") if c in d]))
    d = pd.concat(frames, ignore_index=True)
    for c in d.columns:
        if c not in ("SERIALNO", "SOCP", "NAICSP", "vint") and d[c].dtype == object:
            d[c] = pd.to_numeric(d[c].replace(r"^\s*$", np.nan, regex=True))
    return d


def prepare(d: pd.DataFrame, ref: C.Reference) -> pd.DataFrame:
    cpi = cps_curve.cpi_factor()
    old = d.YEAR <= 2007
    d["educ"] = np.where(old, d.SCHL.map(C.SCHL05_TO_EDUC), d.SCHL.map(C.SCHL08_TO_EDUC))
    d["earn24"] = d.WAGP.fillna(0) * d.adj * d.YEAR.map(lambda y: cpi[y + 1])
    d["band"] = C.band_of(d.AGEP.to_numpy())
    d["gq"] = False
    for v, codes in REL.items():
        m = d.vint == v
        d.loc[m, "gq"] = d.loc[m, "rel"].isin(codes["gq"])
    d["civ"] = ~d.ESR.isin([4, 5]) & ~d.gq
    adult = (d.band >= 0).to_numpy()
    d["p_edu"] = np.nan
    d["p_earn"] = np.nan
    ok = adult & d.educ.notna().to_numpy()
    d.loc[ok, "p_edu"] = ref.pct("educ", d.YEAR.to_numpy()[ok], d.band.to_numpy()[ok], d.educ.to_numpy()[ok])
    ok = adult & d.WAGP.notna().to_numpy()
    d.loc[ok, "p_earn"] = ref.pct("earn", d.YEAR.to_numpy()[ok], d.band.to_numpy()[ok], d.earn24.to_numpy()[ok])
    d["ysm"] = d.YEAR - d.YOEP
    d["cohort"] = C.cohort_of(d.YOEP.fillna(0).to_numpy())
    d["india"] = d.POBP == C.INDIA_ACS
    soc = d.SOCP.fillna("").astype(str)
    naics = d.NAICSP.fillna("").astype(str)
    d["occ_computer"] = soc.str.startswith("151")
    d["occ_physician"] = soc.str.match(r"^(29106|29121|29122|29124)")    # physicians and surgeons, 2000/2010/2018 SOC
    d["occ_health_pract"] = soc.str.startswith("291")
    d["ind_retail"] = naics.str.match(r"^(44|45|4M)")
    d["ind_accom_food"] = naics.str.startswith("72")
    d["employed"] = d.ESR.isin([1, 2])
    d["self_emp"] = d.COW.isin([6, 7])
    d["citizen"] = d.CIT.isin([3, 4])
    d["ba_plus"] = d.educ.isin(C.BA_PLUS)
    d["graduate"] = d.educ.isin(C.GRAD)
    for lab, (lo, hi) in FOD:
        d[f"fod_{lab}"] = d.FOD1P.between(lo, hi)
    d["status_unauth_residual"] = borjas_residual(d)
    return d


def borjas_residual(d: pd.DataFrame) -> np.ndarray:
    """Borjas (2017) residual on ACS fields; rule (f) (subsidised housing) is not in the person file,
    and HINS items start in 2008. See status_impute_2026_09_16 for the CPS version."""
    fb = (d.CIT == 5).to_numpy() | (d.CIT == 4).to_numpy()
    legal = ((d.YOEP < 1980) | d.CIT.isin([3, 4]) | (d.SSP.fillna(0) > 0) | (d.SSIP.fillna(0) > 0)
             | d.MIL.isin([1, 2, 3]) | d.COW.isin([3, 4, 5])
             | d.SOCP.fillna("").astype(str).str.startswith(LICENSED_SOC))
    for c in ("HINS3", "HINS4", "HINS5", "HINS6"):
        if c in d:
            legal |= d[c].eq(1)
    legal = legal.to_numpy()
    # rule (i): householder <-> spouse, iterated to a fixpoint
    head = np.zeros(len(d), bool)
    sp = np.zeros(len(d), bool)
    for v, codes in REL.items():
        m = (d.vint == v).to_numpy()
        head |= m & d.rel.isin(codes["head"]).to_numpy()
        sp |= m & d.rel.isin(codes["spouse"]).to_numpy()
    key = d.YEAR.astype(str) + "|" + d.SERIALNO.astype(str)
    idx = pd.Series(np.arange(len(d)))
    head_of = pd.Series(idx[head].to_numpy(), index=key[head].to_numpy())
    head_of = head_of[~head_of.index.duplicated()]
    partner = np.full(len(d), -1)
    hrow = head_of.reindex(key[sp].to_numpy()).to_numpy()
    sp_rows = np.flatnonzero(sp)
    good = ~np.isnan(hrow)
    partner[sp_rows[good]] = hrow[good].astype(int)
    first_sp = pd.Series(sp_rows[good], index=hrow[good].astype(int))
    first_sp = first_sp[~first_sp.index.duplicated()]
    partner[first_sp.index.to_numpy()] = first_sp.to_numpy()
    has = partner >= 0
    for _ in range(10):
        nxt = legal | (has & legal[np.where(has, partner, 0)])
        if np.array_equal(nxt, legal):
            break
        legal = nxt
    return fb & ~legal


def wshare(w: np.ndarray, x: np.ndarray, base: np.ndarray | None = None) -> float:
    m = np.ones(len(w), bool) if base is None else base
    return float((w[m] * x[m]).sum() / w[m].sum()) if w[m].sum() > 0 else float("nan")


def summarise(d: pd.DataFrame, ref_share: pd.Series, view: str, cohort: str) -> dict:
    """Means and shares under one set of age-standardised weights (band mix `ref_share`)."""
    row = {"source": "ACS", "view": view, "cohort": cohort, "n": len(d)}
    if len(d) == 0:
        return row
    d = d.assign(w=d.PWGTP.astype(float))
    for var in ("p_edu", "p_earn"):
        mm = d[var].notna().to_numpy()
        ws = cps_curve.std_weights(d, mm, ref_share)
        row[f"{var}_mean"], row[f"{var}_se"] = cps_curve.wmean_se(d.loc[mm, var].to_numpy(), ws)
    w = cps_curve.std_weights(d, np.ones(len(d), bool), ref_share)
    g = {c: d[c].to_numpy(bool) for c in ("ba_plus", "graduate", "citizen", "status_unauth_residual",
                                           "employed", "occ_computer", "occ_physician", "occ_health_pract",
                                           "ind_retail", "ind_accom_food", "self_emp")}
    for c in ("ba_plus", "graduate", "citizen", "status_unauth_residual"):
        row[c] = wshare(w, g[c])
    row["unauth_residual_no_ba"] = wshare(w, g["status_unauth_residual"] & ~g["ba_plus"])
    row["employed"] = wshare(w, g["employed"])
    for c in ("occ_computer", "occ_physician", "occ_health_pract", "ind_retail", "ind_accom_food", "self_emp"):
        row[f"{c}_of_employed"] = wshare(w, g[c], g["employed"])
    ba = g["ba_plus"] & d.FOD1P.notna().to_numpy()
    for lab, _ in FOD:
        row[f"fod_{lab}_of_ba"] = wshare(w, d[f"fod_{lab}"].to_numpy(bool), ba) if ba.any() else float("nan")
    row["mean_age"] = wshare(w, d.AGEP.to_numpy(float))
    row["mean_ysm"] = wshare(w, d.ysm.to_numpy(float))
    return row


def cohort_tables(d: pd.DataFrame, cps: pd.DataFrame) -> list[dict]:
    ind = d[d.india & d.civ & (d.band >= 0) & d.YOEP.notna()].copy()
    r = cps.loc[cps.ref.to_numpy()]

    def ref_share(lo=25, hi=64, years=None):
        rr = r[r.age.between(lo, hi)]
        if years is not None:
            rr = rr[rr.year.isin(years)]
        return rr.groupby("band").w.sum() / rr.w.sum()

    def own_mix(m):
        s = ind[m]
        return s.groupby("band").PWGTP.sum() / s.PWGTP.sum()

    # stock views: the white reference's age mix (selection-curve rule) and, at 25-54, the
    # India-born view's own mix; fixed-duration views: the pooled India-born view's own mix
    specs = {
        "stock_2021_2024": (ind.YEAR >= 2021, ref_share(years=[2021, 2022, 2023, 2024])),
        "stock_2015_2019": (ind.YEAR.between(2015, 2019), ref_share(years=list(range(2015, 2020)))),
        "stock_2021_2024_age25_54": (ind.YEAR.ge(2021) & ind.AGEP.between(25, 54), None),
        "ysm_0_5_age25_54": (ind.ysm.between(0, 5) & ind.AGEP.between(25, 54), None),
        "ysm_6_10_age25_54": (ind.ysm.between(6, 10) & ind.AGEP.between(25, 54), None),
        "age35_44_ysm_10_19": (ind.ysm.between(10, 19) & ind.AGEP.between(35, 44), None),
        "ysm_0_5_age25_54_arrived22plus": (ind.ysm.between(0, 5) & ind.AGEP.between(25, 54)
                                           & (ind.AGEP - ind.ysm >= 22), None),
    }
    views = {k: (m, rs if rs is not None else own_mix(m)) for k, (m, rs) in specs.items()}
    rows = []
    for view, (m, rs) in views.items():
        sub = ind[m]
        rows.append(summarise(sub, rs, view, "all"))
        for _, _, lab in C.COHORTS:
            s = sub[sub.cohort == lab]
            if len(s) >= 30:
                rows.append(summarise(s, rs, view, lab))
    # fixed duration by five-year arrival window (finer than the cohort labels)
    rs = views["ysm_0_5_age25_54"][1]
    for lo in range(2000, 2021, 5):
        s = ind[ind.YOEP.between(lo, lo + 4) & ind.ysm.between(0, 5) & ind.AGEP.between(25, 54)]
        if len(s) >= 30:
            rows.append(summarise(s, rs, "ysm_0_5_age25_54_by5yr", f"{lo}-{lo + 4}"))
    return rows


def calibration(d: pd.DataFrame, cps: pd.DataFrame) -> list[dict]:
    """ACS India-born adults vs the CPS India G1 on the same survey years, same age standardisation."""
    rows = []
    for years in ([2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024], list(range(2005, 2015))):
        r = cps[cps.ref & cps.year.isin(years)]
        rs = r.groupby("band").w.sum() / r.w.sum()
        a = d[d.india & d.civ & (d.band >= 0) & d.YEAR.isin(years)].assign(w=lambda x: x.PWGTP.astype(float))
        c = cps[(cps.gen == 1) & (cps.origin == C.INDIA_CPS) & cps.year.isin(years)]
        for var in ("p_edu", "p_earn"):
            ma = a[var].notna().to_numpy()
            ea = cps_curve.wmean_se(a.loc[ma, var].to_numpy(), cps_curve.std_weights(a, ma, rs))
            mc = c[var].notna().to_numpy()
            ec = cps_curve.wmean_se(c.loc[mc, var].to_numpy(), cps_curve.std_weights(c, mc, rs))
            rows.append({"years": f"{min(years)}-{max(years)}", "outcome": var, "acs_mean": ea[0], "acs_se": ea[1],
                         "cps_mean": ec[0], "cps_se": ec[1], "acs_minus_cps": ea[0] - ec[0]})
    return rows


def future_g2(d: pd.DataFrame) -> list[dict]:
    """Children 0-17 of the householder with an India-born householder or spouse."""
    rows = []
    for y in (2005, 2010, 2015, 2019, 2023, 2024):
        h = d[d.YEAR == y]
        codes = REL[vintage(y)]
        par = h[h.rel.isin(codes["head"] | codes["spouse"])]
        par_ind = par[par.india]
        kids = h[h.rel.isin(codes["child"]) & (h.AGEP <= 17)]
        kids = kids[kids.SERIALNO.isin(set(par_ind.SERIALNO))]
        # parents' measures: India-born householder/spouse, mean over the India-born parents
        pm = par_ind.groupby("SERIALNO").agg(p_edu=("p_edu", "mean"), p_earn=("p_earn", "mean"),
                                             ba_plus=("ba_plus", "mean"), yoep=("YOEP", "mean"),
                                             n_ind_par=("india", "size"),
                                             unauth=("status_unauth_residual", "max"))
        k = kids.join(pm, on="SERIALNO", rsuffix="_par")
        k["par_cohort"] = C.cohort_of(np.floor(k.yoep_par.fillna(0).to_numpy()) if "yoep_par" in k else
                                      np.floor(k.yoep.fillna(0).to_numpy()))
        for nat, lab in ((1, "US-born child (future G2)"), (2, "foreign-born child (G1.5)")):
            kk = k[k.NATIVITY == nat]
            w = kk.PWGTP.astype(float)
            row = {"survey_year": y, "children": lab, "n": len(kk), "weighted": float(w.sum())}
            for c, col in (("p_edu", "p_edu_par"), ("p_earn", "p_earn_par"), ("ba_plus", "ba_plus_par")):
                src = col if col in kk else c
                ok = kk[src].notna()
                row[f"parent_{c}"] = float(np.average(kk.loc[ok, src], weights=w[ok])) if ok.any() else float("nan")
                row[f"parent_{c}_n"] = int(ok.sum())
            row["both_parents_india"] = float(w[kk.n_ind_par >= 2].sum() / w.sum())
            row["parent_unauth_residual"] = float(w[kk.unauth.astype(bool)].sum() / w.sum())
            for _, _, cl in C.COHORTS:
                row[f"par_cohort_{cl}"] = float(w[kk.par_cohort == cl].sum() / w.sum())
            rows.append(row)
    return rows


def recent_arrivals(d: pd.DataFrame) -> list[dict]:
    """Weighted India-born noncitizens 18-64 by arrival year, ACS 2023 and 2024: the survey's view of
    the post-2020 inflow, for comparison with CBP encounter counts and unauthorized estimates."""
    rows = []
    for y in (2023, 2024):
        s = d[(d.YEAR == y) & d.india & d.AGEP.between(18, 64) & (d.CIT == 5) & (d.YOEP >= y - 6)]
        for yo, g in s.groupby("YOEP"):
            w = g.PWGTP.astype(float)
            rows.append({"survey_year": y, "arrival_year": int(yo), "n": len(g), "weighted": float(w.sum()),
                         "weighted_no_ba": float(w[~g.ba_plus].sum()),
                         "weighted_less_than_hs": float(w[g.educ < 73].sum()),
                         "weighted_status_residual_no_ba": float(w[g.status_unauth_residual & ~g.ba_plus].sum())})
    return rows


def main() -> int:
    cps = C.cps_prepared()
    ref = C.Reference(cps)
    d = prepare(load(), ref)
    rows = cohort_tables(d, cps)
    C.write_csv(C.DER / "acs_cohorts.csv", rows)
    cal = calibration(d, cps)
    C.write_csv(C.DER / "acs_calibration.csv", cal)
    C.write_csv(C.DER / "acs_recent_arrivals.csv", recent_arrivals(d))
    fut = future_g2(d)
    C.write_csv(C.DER / "acs_future_g2_parents.csv", fut)
    pd.set_option("display.width", 250)
    print(pd.DataFrame(cal).round(2).to_string())
    print(pd.DataFrame(rows).round(3).to_string())
    print(pd.DataFrame(fut).round(3).T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
