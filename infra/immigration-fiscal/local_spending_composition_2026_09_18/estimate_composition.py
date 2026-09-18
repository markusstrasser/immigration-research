#!/usr/bin/env python3
"""Descriptive long differences: county local-spending composition on immigrant share.

Design (descriptive, no instrument -- ladder 136 kills the post-2008 shift-share):

    D y_c = alpha_s + beta * D x_c + (covariates) + e_c

where y is a spending share or a real per-capita level, x is the county Hispanic
(or foreign-born, or Mexico-born) share of population, alpha_s is a state fixed
effect on the differenced equation (the long-difference analogue of state-by-year
effects), and standard errors are clustered on state.

Waves are Census-of-Governments years only (2012, 2017, 2022): the annual survey
individual-unit files enumerate only a sample of local units, so their county sums
are not comparable in composition. Tiburcio and Camarena make the same restriction.

Outputs land in derived/ as estimates_*.csv.
"""
import csv
import json
import os
import sys
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
DERIVED = os.path.join(HERE, "derived")

WAVES = [2012, 2017, 2022]
OPTIONAL_WAVES = [2007]          # from the Government Finance Database, may be absent
# The 2007 finance wave is paired with the 2005-2009 ACS, whose midpoint is 2007.
DEMOG_WAVE = {2007: 2009, 2012: 2012, 2017: 2017, 2022: 2022}
BASE_YEAR = 2022  # dollars

SHARE_OUTCOMES = ["education", "police", "corrections", "judicial", "law_order",
                  "welfare", "health_hosp", "highways"]
LEVEL_OUTCOMES = ["total_direct", "education", "police", "corrections", "judicial",
                  "law_order", "welfare", "health_hosp", "highways"]


# ---------------------------------------------------------------- deflator
def cpi_index():
    dest = os.path.join(CACHE, "cpi.json")
    if os.path.exists(dest):
        return {int(k): v for k, v in json.load(open(dest)).items()}
    out = {}
    for lo, hi in ((2000, 2009), (2010, 2019), (2020, 2024)):
        body = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": str(lo),
                           "endyear": str(hi), "annualaverage": True}).encode()
        req = urllib.request.Request("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                                     data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        for s in d["Results"]["series"]:
            for row in s["data"]:
                if row["periodName"] == "Annual":
                    out[int(row["year"])] = float(row["value"])
    json.dump(out, open(dest, "w"))
    return out


# ---------------------------------------------------------------- loading
def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def fnum(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def build_panel():
    fin = {}
    for r in load_csv(os.path.join(DERIVED, "county_finance.csv")):
        y = int(r["year"])
        if y not in WAVES + OPTIONAL_WAVES:
            continue
        rec = {k: fnum(v) for k, v in r.items() if k not in ("fips", "year")}
        rec["law_order"] = (rec.get("police") or 0) + (rec.get("corrections") or 0) \
            + (rec.get("judicial") or 0)
        fin[(r["fips"], y)] = rec

    dem = {}
    for r in load_csv(os.path.join(DERIVED, "county_shares.csv")):
        dem[(r["fips"], int(r["wave"]))] = {k: fnum(v) for k, v in r.items()
                                            if k not in ("fips", "wave")}

    cpi = cpi_index()
    defl = {y: cpi[BASE_YEAR] / cpi[y] for y in WAVES + OPTIONAL_WAVES}

    counties = sorted({f for f, _ in fin} & {f for f, _ in dem})
    panel = {}
    for fips in counties:
        rec = {}
        ok = True
        for y in WAVES + OPTIONAL_WAVES:
            f = fin.get((fips, y))
            d = dem.get((fips, DEMOG_WAVE[y]))
            if y in OPTIONAL_WAVES and (f is None or d is None
                                        or not f.get("total_direct") or not d.get("pop")):
                continue
            if f is None or d is None or not f.get("total_direct") or not d.get("pop"):
                ok = False
                break
            tot = f["total_direct"]
            pop = d["pop"]
            if tot <= 0 or pop <= 0:
                ok = False
                break
            for o in SHARE_OUTCOMES:
                rec[f"sh_{o}_{y}"] = 100.0 * (f.get(o) or 0) / tot
            for o in LEVEL_OUTCOMES:
                # thousands of dollars -> dollars, deflated, per resident
                v = 1000.0 * (f.get(o) or 0) * defl[y] / pop
                rec[f"pc_{o}_{y}"] = v
                # log per capita, the paper's own outcome; undefined at zero
                rec[f"lg_{o}_{y}"] = np.log(v) if v > 0 else None
            rec[f"sh_educ_elemsec_{y}"] = 100.0 * (f.get("educ_elemsec") or 0) / tot
            lo, ed = f.get("law_order") or 0, f.get("education") or 0
            rec[f"lgratio_lo_ed_{y}"] = np.log(lo / ed) if lo > 0 and ed > 0 else None
            kids = d.get("pop_u19") or 0
            rec[f"perchild_education_{y}"] = (
                1000.0 * (f.get("education") or 0) * defl[y] / kids if kids > 0 else None)
            rec[f"hisp_{y}"] = 100.0 * d["hisp"] / pop if d.get("hisp") is not None else None
            rec[f"fb_{y}"] = 100.0 * d["fb"] / pop if d.get("fb") is not None else None
            rec[f"mex_{y}"] = 100.0 * d["mex"] / pop if d.get("mex") is not None else None
            rec[f"pop_{y}"] = pop
            rec[f"eld_{y}"] = 100.0 * (d.get("pop_65p") or 0) / pop
            rec[f"inc_{y}"] = d.get("medhhinc")
            rec[f"nunits_{y}"] = f.get("n_units")
        if not ok:
            continue
        for y in (2000, 2009):
            d = dem.get((fips, y))
            if d and d.get("pop"):
                rec[f"hisp_{y}"] = 100.0 * d["hisp"] / d["pop"] if d.get("hisp") is not None else None
                base = d.get("pop_sf3") or d["pop"]
                rec[f"fb_{y}"] = 100.0 * d["fb"] / base if d.get("fb") is not None else None
        panel[fips] = rec
    return panel


# ---------------------------------------------------------------- estimation
def ols_cluster(y, X, groups):
    """OLS with cluster-robust (CR1) standard errors."""
    n, k = X.shape
    XtX = X.T @ X
    XtXi = np.linalg.pinv(XtX)
    beta = XtXi @ (X.T @ y)
    resid = y - X @ beta
    meat = np.zeros((k, k))
    uniq = np.unique(groups)
    for g in uniq:
        m = groups == g
        Xg = X[m]
        ug = resid[m]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    G = len(uniq)
    dof = (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    V = XtXi @ meat @ XtXi * dof
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    return beta, se, G


def wls_cluster(y, X, groups, w):
    """Weighted least squares with cluster-robust standard errors."""
    sw = np.sqrt(w)
    Xw = X * sw[:, None]
    yw = y * sw
    n, k = X.shape
    XtXi = np.linalg.pinv(Xw.T @ Xw)
    beta = XtXi @ (Xw.T @ yw)
    resid = yw - Xw @ beta
    meat = np.zeros((k, k))
    uniq = np.unique(groups)
    for g in uniq:
        m = groups == g
        s = Xw[m].T @ resid[m]
        meat += np.outer(s, s)
    G = len(uniq)
    dof = (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    V = XtXi @ meat @ XtXi * dof
    return beta, np.sqrt(np.clip(np.diag(V), 0, None)), G


def state_dummies(fips_list):
    states = sorted({f[:2] for f in fips_list})
    idx = {s: i for i, s in enumerate(states)}
    D = np.zeros((len(fips_list), len(states)))
    for i, f in enumerate(fips_list):
        D[i, idx[f[:2]]] = 1.0
    return D


def run_arm(panel, keys, dep_prefix, outcome, regressor, y0, y1,
            weighted=True, covariates=False, drop_top=0, placebo=False, trim=False,
            drop_states=()):
    rows_f, dy, dx, cov = [], [], [], []
    for f in keys:
        if f[:2] in drop_states:
            continue
        r = panel[f]
        a = r.get(f"{dep_prefix}{outcome}_{y0}")
        b = r.get(f"{dep_prefix}{outcome}_{y1}")
        if placebo:
            xa, xb = r.get(f"{regressor}_2000"), r.get(f"{regressor}_2009")
        else:
            xa, xb = r.get(f"{regressor}_{y0}"), r.get(f"{regressor}_{y1}")
        if None in (a, b, xa, xb):
            continue
        inc = r.get(f"inc_{y0}")
        if covariates and (inc is None or inc <= 0):
            continue
        rows_f.append(f)
        dy.append(b - a)
        dx.append(xb - xa)
        if covariates:
            cov.append([np.log(r[f"pop_{y0}"]), r[f"eld_{y0}"], np.log(inc),
                        np.log(r[f"pop_{y1}"]) - np.log(r[f"pop_{y0}"])])
    if len(rows_f) < 50:
        return None
    dy = np.asarray(dy)
    dx = np.asarray(dx)
    w = np.asarray([panel[f][f"pop_{y0}"] for f in rows_f])
    if trim:
        lo_y, hi_y = np.percentile(dy, [1, 99])
        lo_x, hi_x = np.percentile(dx, [1, 99])
        m = (w >= 10000) & (dy >= lo_y) & (dy <= hi_y) & (dx >= lo_x) & (dx <= hi_x)
        keep = np.flatnonzero(m)
        rows_f = [rows_f[i] for i in keep]
        dy, dx, w = dy[keep], dx[keep], w[keep]
        if cov:
            cov = [cov[i] for i in keep]
    if drop_top:
        keep = np.argsort(-w)[drop_top:]
        rows_f = [rows_f[i] for i in keep]
        dy, dx, w = dy[keep], dx[keep], w[keep]
        if cov:
            cov = [cov[i] for i in keep]
    D = state_dummies(rows_f)
    parts = [dx[:, None], D]
    if covariates:
        parts.insert(1, np.asarray(cov))
    X = np.hstack(parts)
    groups = np.asarray([f[:2] for f in rows_f])
    if weighted:
        beta, se, G = wls_cluster(dy, X, groups, w)
    else:
        beta, se, G = ols_cluster(dy, X, groups)
    return {"n": len(rows_f), "clusters": G, "coef": beta[0], "se": se[0],
            "coef10": 10 * beta[0], "se10": 10 * se[0],
            "t": beta[0] / se[0] if se[0] > 0 else float("nan"),
            "mean_y0": float(np.average([panel[f][f"{dep_prefix}{outcome}_{y0}"] for f in rows_f],
                                        weights=w if weighted else None)),
            "mean_dx": float(np.average(dx, weights=w if weighted else None))}


def stars(t):
    a = abs(t)
    return "***" if a > 2.576 else "**" if a > 1.96 else "*" if a > 1.645 else ""


def influence_report(panel, keys):
    """Which counties move the weighted education-share coefficient."""
    rows, dy, dx, w = [], [], [], []
    for f in keys:
        a, b = panel[f].get("sh_education_2012"), panel[f].get("sh_education_2022")
        xa, xb = panel[f].get("hisp_2012"), panel[f].get("hisp_2022")
        if None in (a, b, xa, xb):
            continue
        rows.append(f)
        dy.append(b - a)
        dx.append(xb - xa)
        w.append(panel[f]["pop_2012"])
    dy, dx, w = np.asarray(dy), np.asarray(dx), np.asarray(w)
    D = state_dummies(rows)
    groups = np.asarray([f[:2] for f in rows])
    base = wls_cluster(dy, np.hstack([dx[:, None], D]), groups, w)[0][0]
    order = np.argsort(-w)[:40]
    recs = []
    for i in order:
        m = np.ones(len(rows), bool)
        m[i] = False
        sub = [rows[j] for j in np.flatnonzero(m)]
        b = wls_cluster(dy[m], np.hstack([dx[m][:, None], state_dummies(sub)]),
                        groups[m], w[m])[0][0]
        recs.append({"fips": rows[i], "pop2012": int(w[i]), "d_hisp": dx[i],
                     "d_educ_share": dy[i], "coef_without": b,
                     "delta_coef": b - base})
    recs.sort(key=lambda r: -abs(r["delta_coef"]))
    path = os.path.join(DERIVED, "influence_education_share.csv")
    with open(path, "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=["fips", "pop2012", "d_hisp", "d_educ_share",
                                            "coef_without", "delta_coef"])
        wtr.writeheader()
        for r in recs:
            wtr.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    print(f"\n[influence] weighted education-share coefficient {base:.4f} per point "
          f"({10 * base:.2f} per 10 points)", flush=True)
    for r in recs[:6]:
        print(f"   drop {r['fips']} (pop {r['pop2012']:,}): coefficient -> {10 * r['coef_without']:.2f}"
              f" per 10 points", flush=True)
    print(f"[done] {path}", flush=True)


def main():
    os.makedirs(DERIVED, exist_ok=True)
    panel = build_panel()
    keys = sorted(panel)
    print(f"[panel] {len(keys)} counties present in all of {WAVES}", flush=True)

    arms = []

    def add(label, dep_prefix, outcome, regressor, y0, y1, **kw):
        res = run_arm(panel, keys, dep_prefix, outcome, regressor, y0, y1, **kw)
        if res is None:
            print(f"  [skip] {label} {outcome} — too few observations", flush=True)
            return
        res.update({"arm": label, "outcome": outcome, "regressor": regressor,
                    "window": f"{y0}-{y1}", "unit": "share_pp" if dep_prefix == "sh_" else "dollars_pc",
                    "stars": stars(res["t"])})
        arms.append(res)
        print(f"  {label:34s} {outcome:13s} {regressor:5s} "
              f"{res['coef10']:>10.3f} ({res['se10']:.3f}){res['stars']:3s} n={res['n']}",
              flush=True)

    print("\n[A] shares, 2012-2022, population weighted, no covariates", flush=True)
    for o in SHARE_OUTCOMES:
        add("A_share_wtd", "sh_", o, "hisp", 2012, 2022)
    print("\n[B] shares, 2012-2022, unweighted", flush=True)
    for o in SHARE_OUTCOMES:
        add("B_share_unwtd", "sh_", o, "hisp", 2012, 2022, weighted=False)
    print("\n[C] shares, 2012-2022, weighted, with covariates", flush=True)
    for o in SHARE_OUTCOMES:
        add("C_share_cov", "sh_", o, "hisp", 2012, 2022, covariates=True)
    print("\n[D] shares, foreign-born share regressor", flush=True)
    for o in SHARE_OUTCOMES:
        add("D_share_fb", "sh_", o, "fb", 2012, 2022)
    print("\n[E] shares, Mexico-born share regressor", flush=True)
    for o in SHARE_OUTCOMES:
        add("E_share_mex", "sh_", o, "mex", 2012, 2022)
    print("\n[F] shares, drop the 25 largest counties", flush=True)
    for o in SHARE_OUTCOMES:
        add("F_share_droptop25", "sh_", o, "hisp", 2012, 2022, drop_top=25)
    print("\n[G] real per-capita levels, 2022 dollars (denominator-masking check)", flush=True)
    for o in LEVEL_OUTCOMES:
        add("G_level_wtd", "pc_", o, "hisp", 2012, 2022)
    print("\n[H] real education spending per child under 19", flush=True)
    add("H_perchild", "perchild_", "education", "hisp", 2012, 2022)
    print("\n[I] sub-windows", flush=True)
    for o in SHARE_OUTCOMES:
        add("I_share_2012_2017", "sh_", o, "hisp", 2012, 2017)
    for o in SHARE_OUTCOMES:
        add("I_share_2017_2022", "sh_", o, "hisp", 2017, 2022)
    print("\n[J] pre-period placebo: 2000-2009 Hispanic-share change on the 2012-2022 outcome",
          flush=True)
    for o in SHARE_OUTCOMES:
        add("J_placebo_pre", "sh_", o, "hisp", 2012, 2022, placebo=True)
    print("\n[K] pre-period placebo, foreign-born", flush=True)
    for o in SHARE_OUTCOMES:
        add("K_placebo_fb", "sh_", o, "fb", 2012, 2022, placebo=True)
    print("\n[L] log real per-capita levels (the paper's own outcome)", flush=True)
    for o in LEVEL_OUTCOMES:
        add("L_log_wtd", "lg_", o, "hisp", 2012, 2022)
    for o in LEVEL_OUTCOMES:
        add("L_log_unwtd", "lg_", o, "hisp", 2012, 2022, weighted=False)
    print("\n[M] log(law-and-order / education), the composition claim in one number", flush=True)
    add("M_logratio_wtd", "lgratio_", "lo_ed", "hisp", 2012, 2022)
    add("M_logratio_unwtd", "lgratio_", "lo_ed", "hisp", 2012, 2022, weighted=False)
    add("M_logratio_cov", "lgratio_", "lo_ed", "hisp", 2012, 2022, covariates=True)
    add("M_logratio_fb", "lgratio_", "lo_ed", "fb", 2012, 2022)
    add("M_logratio_placebo", "lgratio_", "lo_ed", "hisp", 2012, 2022, placebo=True)
    print("\n[N] education share, elementary and secondary only", flush=True)
    add("N_elemsec_wtd", "sh_", "educ_elemsec", "hisp", 2012, 2022)
    add("N_elemsec_unwtd", "sh_", "educ_elemsec", "hisp", 2012, 2022, weighted=False)
    print("\n[R] the brief's long window, 2007-2022 (2007 from the Government Finance "
          "Database)", flush=True)
    add("R_logratio_2007_2022", "lgratio_", "lo_ed", "hisp", 2007, 2022)
    add("R_logratio_2007_2022_unwtd", "lgratio_", "lo_ed", "hisp", 2007, 2022, weighted=False)
    add("R_logratio_2007_2022_noCA", "lgratio_", "lo_ed", "hisp", 2007, 2022,
        drop_states=("06",))
    add("R_logratio_2007_2022_fb", "lgratio_", "lo_ed", "fb", 2007, 2022)
    for o in SHARE_OUTCOMES:
        add("R_share_2007_2022", "sh_", o, "hisp", 2007, 2022)
    for o in SHARE_OUTCOMES:
        add("R_share_2007_2022_unwtd", "sh_", o, "hisp", 2007, 2022, weighted=False)
    for o in LEVEL_OUTCOMES:
        add("R_log_2007_2022", "lg_", o, "hisp", 2007, 2022)
    for o in LEVEL_OUTCOMES:
        add("R_log_2007_2022_unwtd", "lg_", o, "hisp", 2007, 2022, weighted=False)
    add("R_logratio_2007_2012", "lgratio_", "lo_ed", "hisp", 2007, 2012)
    for o in SHARE_OUTCOMES:
        add("R_share_2007_2022_noCA", "sh_", o, "hisp", 2007, 2022, drop_states=("06",))
    add("R_placebo_2007_2022", "lgratio_", "lo_ed", "hisp", 2007, 2022, placebo=True)
    for o in SHARE_OUTCOMES:
        add("R_placebo_2007_2022", "sh_", o, "hisp", 2007, 2022, placebo=True)
    print("   leave-one-state-out on the 2007-2022 log ratio", flush=True)
    loo7 = []
    for st in sorted({k[:2] for k in keys}):
        r = run_arm(panel, keys, "lgratio_", "lo_ed", "hisp", 2007, 2022, drop_states=(st,))
        if r:
            loo7.append((r["coef10"], st, r["n"]))
    loo7.sort()
    print(f"   min {loo7[0][0]:.3f} dropping {loo7[0][1]}; max {loo7[-1][0]:.3f} dropping "
          f"{loo7[-1][1]}; median {loo7[len(loo7) // 2][0]:.3f}", flush=True)
    with open(os.path.join(DERIVED, "loo_state_logratio_2007_2022.csv"), "w", newline="") as fh:
        wtr = csv.writer(fh)
        wtr.writerow(["dropped_state_fips", "coef_per_10pts", "n"])
        for c, st, n in loo7:
            wtr.writerow([st, f"{c:.6g}", n])

    print("\n[P] drop California: the Local Control Funding Formula sends state money to "
          "districts with many English learners, which would raise the education share "
          "for a reason unrelated to local preferences", flush=True)
    add("P_noCA_logratio", "lgratio_", "lo_ed", "hisp", 2012, 2022, drop_states=("06",))
    add("P_noCA_logratio_unwtd", "lgratio_", "lo_ed", "hisp", 2012, 2022,
        drop_states=("06",), weighted=False)
    for o in SHARE_OUTCOMES:
        add("P_noCA_share", "sh_", o, "hisp", 2012, 2022, drop_states=("06",))
    for o in LEVEL_OUTCOMES:
        add("P_noCA_log", "lg_", o, "hisp", 2012, 2022, drop_states=("06",))
    print("\n[Q] leave-one-state-out on the log ratio", flush=True)
    states = sorted({k[:2] for k in keys})
    loo = []
    for st in states:
        r = run_arm(panel, keys, "lgratio_", "lo_ed", "hisp", 2012, 2022, drop_states=(st,))
        if r:
            loo.append((r["coef10"], st, r["n"]))
    loo.sort()
    print(f"   min {loo[0][0]:.3f} dropping {loo[0][1]}; max {loo[-1][0]:.3f} dropping "
          f"{loo[-1][1]}; median {loo[len(loo) // 2][0]:.3f}", flush=True)
    with open(os.path.join(DERIVED, "loo_state_logratio.csv"), "w", newline="") as fh:
        wtr = csv.writer(fh)
        wtr.writerow(["dropped_state_fips", "coef_per_10pts", "n"])
        for c, st, n in loo:
            wtr.writerow([st, f"{c:.6g}", n])
    print("\n[O] trimmed: drop counties under 10,000 residents and the 1%% tails of the "
          "share change", flush=True)
    for o in SHARE_OUTCOMES:
        add("O_share_trim", "sh_", o, "hisp", 2012, 2022, trim=True)
    for o in SHARE_OUTCOMES:
        add("O_share_trim_unwtd", "sh_", o, "hisp", 2012, 2022, trim=True, weighted=False)

    influence_report(panel, keys)

    out = os.path.join(DERIVED, "estimates_composition.csv")
    cols = ["arm", "outcome", "regressor", "window", "unit", "n", "clusters",
            "coef", "se", "coef10", "se10", "t", "stars", "mean_y0", "mean_dx"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in arms:
            w.writerow({c: (f"{r[c]:.6g}" if isinstance(r[c], float) else r[c]) for c in cols})
    print(f"\n[done] {out} {len(arms)} estimates", flush=True)

    # descriptive composition table
    desc = os.path.join(DERIVED, "composition_means.csv")
    with open(desc, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["outcome", "year", "mean_share_pop_wtd", "mean_share_unwtd",
                    "pc_dollars_2022", "national_total_bn_2022usd"])
        for y in WAVES:
            pops = np.asarray([panel[k][f"pop_{y}"] for k in keys])
            for o in SHARE_OUTCOMES:
                s = np.asarray([panel[k][f"sh_{o}_{y}"] for k in keys])
                pc = np.asarray([panel[k][f"pc_{o}_{y}"] for k in keys])
                w.writerow([o, y, f"{np.average(s, weights=pops):.3f}",
                            f"{s.mean():.3f}", f"{np.average(pc, weights=pops):.1f}",
                            f"{float((pc * pops).sum()) / 1e9:.1f}"])
    print(f"[done] {desc}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
