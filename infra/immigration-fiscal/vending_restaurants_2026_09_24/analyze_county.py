"""Designs (a) and (a2): California counties against counties in other states, event study around 2019.

(a)  log outcome = county FE + year FE + sum_k b_k * CA * 1[year = k], k != 2018.
     Control pools, fixed before any outcome was seen:
       P1  every non-California county with a 2013-2017 Hispanic share of at least 10%;
       P2  five nearest non-California neighbours per California county (with replacement) on
           Hispanic share, log 2017 restaurant (NAICS 7225) employment and 2012-2017 growth in it,
           each standardised; controls weighted by how often they are matched.
     Weights: none, or 2013-2017 population (ACS). Standard errors clustered by county. Because
     California is a single treated state, the report adds a permutation over placebo states: the
     same event study with each other state that has at least five P1 counties treated instead of
     California (California dropped), giving a rank p-value for b_2019 and mean(b_2022, b_2023).
(a2) Triple difference on all counties: log outcome = county FE + state x year FE
     + sum_k g_k * X * 1[year = k] + sum_k d_k * X * CA * 1[year = k], X = exposure (share, per 10
     points), k != 2018. d_k is the extra change in high-exposure California counties over the same
     gradient in other states; state x year effects absorb anything common to all of California.

Outcomes: CBP 2012-2023 (722511, 722513, 722330, 7225, 445110 x establishments, employment, payroll)
and QCEW 2014-2023 private (7225, 722511, 722513, 445110 x establishments, employment, wages).
Suppressed cells (employment or payroll 0 with establishments > 0; QCEW disclosure N) are missing;
each regression uses the counties observed in every year (balanced).

Writes derived/county_event_coefs.csv, derived/county_event_summary.csv,
derived/county_permutation.csv, derived/county_triple_coefs.csv, derived/county_triple_summary.csv,
derived/matched_controls.csv.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_county.py
"""
import warnings

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

from lib import CACHE, DERIVED

warnings.filterwarnings("ignore")
REF = 2018
CBP_YEARS = list(range(2012, 2024))
QCEW_YEARS = list(range(2014, 2024))
CBP_OUT = [(c, v) for c in ("722511", "722513", "722330", "445110") for v in ("estab", "emp", "payann")] + \
          [("7225", "emp")]
QCEW_OUT = [("7225", "estabs"), ("7225", "emp"), ("7225", "wages"), ("722511", "emp"), ("722513", "emp"),
            ("445110", "emp")]
PERM_OUT = [("cbp", "722511", "emp"), ("cbp", "722513", "emp"), ("cbp", "722330", "estab"),
            ("cbp", "7225", "emp"), ("cbp", "445110", "emp"), ("qcew", "7225", "emp")]
TRIPLE_OUT = [(c, v) for c in ("722511", "722513", "722330", "445110") for v in ("estab", "emp")]
EXPOSURES = ["hisp_share", "mexborn_share", "foodprep_hisp_share"]


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    cbp = pd.read_csv(CACHE / "cbp_county_panel.csv", dtype={"fips": str, "naics": str})
    cbp = cbp[~cbp["fips"].str.startswith("72")]
    for v in ("emp", "payann"):
        cbp.loc[(cbp[v] == 0) & (cbp["estab"] > 0), v] = np.nan
    q = pd.read_csv(CACHE / "qcew_county_panel.csv", dtype={"fips": str, "naics": str})
    q = q[(q["disclosed"] == 1) & ~q["fips"].str.startswith("72") & ~q["fips"].str.endswith("999")]
    ex = pd.read_csv(DERIVED / "exposure_county.csv", dtype={"fips": str})
    return cbp, q, ex


def balanced(df: pd.DataFrame, code: str, var: str, years: list) -> pd.DataFrame:
    d = df[(df["naics"] == code) & df["year"].isin(years)][["fips", "year", var]].dropna()
    d = d[d[var] > 0]
    n = d.groupby("fips")["year"].nunique()
    d = d[d["fips"].isin(n[n == len(years)].index)].copy()
    d["y"] = np.log(d[var])
    return d


def matched_controls(cbp: pd.DataFrame, ex: pd.DataFrame) -> pd.DataFrame:
    e = balanced(cbp, "7225", "emp", CBP_YEARS).pivot(index="fips", columns="year", values="y")
    m = pd.DataFrame({"lemp17": e[2017], "g1217": e[2017] - e[2012]}).join(ex.set_index("fips")["hisp_share"])
    m = m.dropna()
    z = (m - m.mean()) / m.std()
    ca = z[z.index.str.startswith("06")]
    pool = z[~z.index.str.startswith("06")]
    rows = []
    for f, r in ca.iterrows():
        dist = np.sqrt(((pool - r) ** 2).sum(axis=1)).nsmallest(5)
        rows += [{"ca_fips": f, "control_fips": c, "distance": round(float(d), 4)} for c, d in dist.items()]
    return pd.DataFrame(rows)


def event(d: pd.DataFrame, years: list, weight: str | None) -> tuple[pd.DataFrame, float]:
    d = d.copy()
    names = []
    for k in years:
        if k == REF:
            continue
        nm = f"d{k}"
        d[nm] = d["treat"] * (d["year"] == k)
        names.append(nm)
    fml = "y ~ " + " + ".join(names) + " | fips + year"
    m = pf.feols(fml, data=d, weights=weight, vcov={"CRV1": "fips"})
    b, se = m.coef(), m.se()
    out = pd.DataFrame({"year": [int(n[1:]) for n in names], "coef": b[names].values, "se": se[names].values})
    pre = [n for n in names if int(n[1:]) < REF]
    V = m._vcov
    idx = [list(b.index).index(n) for n in pre]
    bp = b[pre].values
    W = float(bp @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ bp)
    p_pre = float(1 - stats.chi2.cdf(W, len(pre)))
    return out, p_pre


def summarize(coefs: pd.DataFrame) -> dict:
    c = coefs.set_index("year")
    late = [k for k in (2022, 2023) if k in c.index]
    return {"b2019": c.loc[2019, "coef"], "se2019": c.loc[2019, "se"],
            "b2022_23": c.loc[late, "coef"].mean(), "b2020_21": c.loc[[2020, 2021], "coef"].mean(),
            "pre_max_abs": c.loc[c.index < REF, "coef"].abs().max()}


def main() -> None:
    cbp, q, ex = load()
    ex = ex.set_index("fips")
    match = matched_controls(cbp, ex.reset_index())
    match.to_csv(DERIVED / "matched_controls.csv", index=False, lineterminator="\n")
    mw = match["control_fips"].value_counts()
    p1 = set(ex.index[(ex["hisp_share"] >= 0.10) & ~ex.index.str.startswith("06")])
    print(f"  pools: P1 {len(p1)} counties; P2 {mw.size} distinct matched controls for "
          f"{match['ca_fips'].nunique()} California counties")
    sources = {"cbp": (cbp, CBP_YEARS), "qcew": (q, QCEW_YEARS)}
    coef_rows, summ_rows = [], []
    for src, outs in (("cbp", CBP_OUT), ("qcew", QCEW_OUT)):
        df, years = sources[src]
        for code, var in outs:
            base = balanced(df, code, var, years)
            base["treat"] = base["fips"].str.startswith("06").astype(int)
            base = base.join(ex[["pop"]], on="fips")
            for pool in ("P1", "P2"):
                if pool == "P1":
                    d = base[(base["treat"] == 1) | base["fips"].isin(p1)].copy()
                    d["w_match"] = 1.0
                else:
                    d = base[(base["treat"] == 1) | base["fips"].isin(mw.index)].copy()
                    d["w_match"] = np.where(d["treat"] == 1, 1.0, d["fips"].map(mw).fillna(0))
                for wname in ("none", "pop"):
                    d["w"] = d["w_match"] * (d["pop"] if wname == "pop" else 1.0)
                    co, p_pre = event(d, years, "w")
                    s = summarize(co)
                    nt = d.loc[d["treat"] == 1, "fips"].nunique()
                    nc = d.loc[d["treat"] == 0, "fips"].nunique()
                    tag = dict(source=src, naics=code, var=var, pool=pool, weight=wname, n_ca=nt, n_control=nc)
                    coef_rows += [{**tag, **r} for r in co.to_dict("records")]
                    summ_rows.append({**tag, **s, "p_pretrend": p_pre})
                    print(f"  {src} {code} {var} {pool} {wname}: CA {nt} / controls {nc}; b2019 {s['b2019']:+.4f} "
                          f"({s['se2019']:.4f}); b2022-23 {s['b2022_23']:+.4f}; pre-trend p {p_pre:.3f}", flush=True)
    pd.DataFrame(coef_rows).to_csv(DERIVED / "county_event_coefs.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")
    summ = pd.DataFrame(summ_rows)

    # permutation over placebo states (pool P1, California dropped)
    states = pd.Series(sorted(p1)).str[:2].value_counts()
    states = sorted(states[states >= 5].index)
    perm_rows = []
    for src, code, var in PERM_OUT:
        df, years = sources[src]
        base = balanced(df, code, var, years).join(ex[["pop"]], on="fips")
        for wname in ("none", "pop"):
            base["w"] = base["pop"] if wname == "pop" else 1.0
            for st in states:
                d = base[base["fips"].isin(p1)].copy()
                d["treat"] = d["fips"].str.startswith(st).astype(int)
                if d["treat"].sum() == 0 or d.loc[d["treat"] == 1, "fips"].nunique() < 3:
                    continue
                co, _ = event(d, years, "w")
                s = summarize(co)
                perm_rows.append({"source": src, "naics": code, "var": var, "weight": wname, "state": st,
                                  "n_treated": d.loc[d["treat"] == 1, "fips"].nunique(),
                                  "b2019": s["b2019"], "b2022_23": s["b2022_23"]})
            print(f"  permutation {src} {code} {var} {wname}: {sum(1 for r in perm_rows if r['source'] == src and r['naics'] == code and r['var'] == var and r['weight'] == wname)} placebo states", flush=True)
    perm = pd.DataFrame(perm_rows)
    perm.to_csv(DERIVED / "county_permutation.csv", index=False, lineterminator="\n", float_format="%.6g")
    for i, r in summ.iterrows():
        if r["pool"] != "P1":
            continue
        pp = perm[(perm["source"] == r["source"]) & (perm["naics"] == r["naics"]) & (perm["var"] == r["var"])
                  & (perm["weight"] == r["weight"])]
        if len(pp):
            for stat in ("b2019", "b2022_23"):
                summ.loc[i, f"perm_p_{stat}"] = (1 + (pp[stat].abs() >= abs(r[stat])).sum()) / (1 + len(pp))
                summ.loc[i, "perm_states"] = len(pp)
    summ.to_csv(DERIVED / "county_event_summary.csv", index=False, lineterminator="\n", float_format="%.6g")

    # triple difference
    trip_coefs, trip_summ = [], []
    for code, var in TRIPLE_OUT:
        base = balanced(cbp, code, var, CBP_YEARS).join(ex[["pop"] + EXPOSURES], on="fips")
        base["state"] = base["fips"].str[:2]
        base["ca"] = (base["state"] == "06").astype(int)
        for xname in EXPOSURES:
            d = base.dropna(subset=[xname]).copy()
            d["x"] = d[xname] * 10  # per 10 percentage points
            names = []
            for k in CBP_YEARS:
                if k == REF:
                    continue
                d[f"g{k}"] = d["x"] * (d["year"] == k)
                d[f"t{k}"] = d["x"] * d["ca"] * (d["year"] == k)
                names += [f"g{k}", f"t{k}"]
            for wname in ("none", "pop"):
                w = "pop" if wname == "pop" else None
                m = pf.feols("y ~ " + " + ".join(names) + " | fips + state^year", data=d, weights=w,
                             vcov={"CRV1": "fips"})
                b, se = m.coef(), m.se()
                tn = [n for n in names if n.startswith("t")]
                co = pd.DataFrame({"year": [int(n[1:]) for n in tn], "coef": b[tn].values, "se": se[tn].values})
                V = m._vcov
                pre = [n for n in tn if int(n[1:]) < REF]
                idx = [list(b.index).index(n) for n in pre]
                bp = b[pre].values
                Wst = float(bp @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ bp)
                tag = dict(naics=code, var=var, exposure=xname, weight=wname,
                           n_ca=d.loc[d["ca"] == 1, "fips"].nunique(), n_other=d.loc[d["ca"] == 0, "fips"].nunique())
                trip_coefs += [{**tag, **r} for r in co.to_dict("records")]
                s = summarize(co)
                trip_summ.append({**tag, **s, "p_pretrend": float(1 - stats.chi2.cdf(Wst, len(pre)))})
                print(f"  triple {code} {var} {xname} {wname}: b2019 {s['b2019']:+.4f} ({s['se2019']:.4f}); "
                      f"b2022-23 {s['b2022_23']:+.4f}", flush=True)
    pd.DataFrame(trip_coefs).to_csv(DERIVED / "county_triple_coefs.csv", index=False, lineterminator="\n",
                                    float_format="%.6g")
    pd.DataFrame(trip_summ).to_csv(DERIVED / "county_triple_summary.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")


if __name__ == "__main__":
    main()
