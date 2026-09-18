"""Design (a): does the native private-school share rise with the Hispanic/foreign-born
share of enrolled children in the metro?

Outcome   priv_wnh = private / (private + public) among US-born non-Hispanic white
          children 5-17, by CBSA-year, separately for elementary (5-12) and
          secondary (13-17).
Treatment hisp_share, fb_share = Hispanic / foreign-born share of ALL enrolled children.
Design    (1) long difference 2005->2023, weighted OLS, HC1
          (2) two-way fixed effects (CBSA, year), cluster-robust by CBSA
          (3) the same with Asian and Black shares entered alongside -- disconfirmation
          (4) 2SLS on the 2000-base shift-share instrument, with the first-stage F
          (5) reverse-timing placebo: earlier outcome change on later treatment change
          (6) counts version, directly comparable to Betts & Fairlie's "natives per
              immigrant" ratio
          (7) influence check: drop the five largest metros, and drop California

All estimates are written to derived/estimates.csv.
"""
import pathlib, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"
EMP = HERE.parent / "employment_entry_2026_09_18" / "derived"
MIN_ENR = 15000
ROWS = []


def rec(**kw):
    ROWS.append(kw)
    keys = ("spec", "level", "outcome", "treatment", "estimator", "n", "coef", "se",
            "t", "first_stage_F")
    print(" | ".join(f"{k}={kw.get(k)}" if not isinstance(kw.get(k), float)
                     else f"{k}={kw[k]:.4f}" for k in keys if k in kw), flush=True)


def wls(y, X, w):
    """Weighted least squares with HC1 standard errors."""
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yw - Xw @ b
    n, k = X.shape
    XtXi = np.linalg.inv(XtX)
    meat = (Xw * e[:, None]).T @ (Xw * e[:, None])
    V = XtXi @ meat @ XtXi * n / max(n - k, 1)
    return b, np.sqrt(np.diag(V))


def wls_cluster(y, X, w, g):
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yw - Xw @ b
    XtXi = np.linalg.inv(XtX)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for _, ix in pd.Series(range(len(g))).groupby(np.asarray(g)).groups.items():
        ix = np.asarray(ix)
        s = Xw[ix].T @ e[ix]
        meat += np.outer(s, s)
    G, n, k = len(set(g)), len(y), X.shape[1]
    adj = (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    V = XtXi @ meat @ XtXi * adj
    return b, np.sqrt(np.diag(V))


def tsls(y, D, Z, W, w):
    """Just-identified 2SLS: y on [D, W], D instrumented by [Z, W]. HC1."""
    X1 = np.column_stack([Z, W])
    bf, sef = wls(D, X1, w)
    Dhat = X1 @ bf
    X2 = np.column_stack([Dhat, W])
    b, se = wls(y, X2, w)
    # first-stage robust F on the excluded instrument
    F = (bf[0] / sef[0]) ** 2
    # second-stage SE must use the structural residual
    sw = np.sqrt(w)
    Xs = np.column_stack([D, W]) * sw[:, None]
    X2w = X2 * sw[:, None]
    e = (y * sw) - Xs @ b
    A = np.linalg.inv(X2w.T @ X2w)
    meat = (X2w * e[:, None]).T @ (X2w * e[:, None])
    V = A @ meat @ A * len(y) / max(len(y) - X2.shape[1], 1)
    return b, np.sqrt(np.diag(V)), F


def load():
    p = pd.read_csv(DERIVED / "metro_school_panel.csv", dtype={"cbsa": str})
    years = sorted(p.year.unique())
    keep = (p.groupby("cbsa")["enr_all"].min() >= MIN_ENR)
    full = p.groupby("cbsa").size() == len(years)
    ok = set(keep[keep].index) & set(full[full].index)
    p = p[p.cbsa.isin(ok)].copy()
    print(f"panel: {p.cbsa.nunique()} metros x {len(years)} years "
          f"(>= {MIN_ENR:,} enrolled children in every year)")
    return p, years


def instrument(p, years):
    """2000-base shift-share: metro's 2000 share of the national stock of each origin,
    times the national stock of that origin in year t, over the metro's 2000 population."""
    base = pd.read_csv(EMP / "metro_origin_base.csv", dtype={"cbsa": str})
    natl = pd.read_csv(EMP / "national_origin_stock.csv")
    pop = pd.read_csv(EMP / "metro_base_2000.csv", dtype={"cbsa": str})[["cbsa", "pop2000"]]
    natl = natl[natl.year.isin(years)]
    if natl.empty:
        return None
    m = base.merge(natl, on="origin", how="inner")
    m["pred"] = m.base_share * m.natl_stock
    z = m.groupby(["cbsa", "year"], as_index=False)["pred"].sum()
    z = z.merge(pop, on="cbsa", how="inner")
    z["z_fb"] = z.pred / z.pop2000
    mex = m[m.origin == "mexico"]
    if len(mex):
        zm = mex.groupby(["cbsa", "year"], as_index=False)["pred"].sum() \
               .rename(columns={"pred": "pred_mex"})
        z = z.merge(zm, on=["cbsa", "year"], how="left")
        z["z_mex"] = z.pred_mex / z.pop2000
    return z[["cbsa", "year"] + [c for c in ("z_fb", "z_mex") if c in z]]


def diffs(p, y0, y1, lvl):
    a = p[p.year == y0].set_index("cbsa")
    b = p[p.year == y1].set_index("cbsa")
    ix = a.index.intersection(b.index)
    d = pd.DataFrame(index=ix)
    for c in (f"priv_wnh_{lvl}", f"priv_nnh_{lvl}", f"priv_hnb_{lvl}",
              f"hisp_share_{lvl}", f"fb_share_{lvl}",
              f"asian_share_{lvl}", f"black_share_{lvl}", f"hisp_share_pub_{lvl}"):
        d["d_" + c] = b.loc[ix, c] - a.loc[ix, c]
    # first-generation (largely English-learner) vs second-generation Hispanic shares:
    # Betts & Fairlie find flight responds to NON-ENGLISH-SPEAKING immigrants only
    for g, nm in (("hisp_fb", "hispfb"), ("hisp_nb", "hispnb")):
        s0 = (a.loc[ix, f"{g}_pub_{lvl}"] + a.loc[ix, f"{g}_priv_{lvl}"]) / a.loc[ix, f"enr_{lvl}"]
        s1 = (b.loc[ix, f"{g}_pub_{lvl}"] + b.loc[ix, f"{g}_priv_{lvl}"]) / b.loc[ix, f"enr_{lvl}"]
        d[f"d_{nm}_share"] = s1 - s0
    d["w"] = a.loc[ix, f"wnh_enr_{lvl}"]
    d["enr0"] = a.loc[ix, f"enr_{lvl}"]
    d["state_fips"] = a.loc[ix, "state_fips"]
    d["cbsa_title"] = a.loc[ix, "cbsa_title"]
    # counts, per 100 children enrolled in the base year
    d["d_wnh_priv_n"] = (b.loc[ix, f"wnh_nb_priv_{lvl}"] - a.loc[ix, f"wnh_nb_priv_{lvl}"]) \
        / a.loc[ix, f"enr_{lvl}"] * 100
    # total enrolment growth, per 100 base: a growing metro adds Hispanic public pupils
    # AND white private pupils at once, so the count regression needs this control or it
    # picks up common growth rather than substitution
    d["d_enr_n"] = (b.loc[ix, f"enr_{lvl}"] - a.loc[ix, f"enr_{lvl}"]) \
        / a.loc[ix, f"enr_{lvl}"] * 100
    hp0 = a.loc[ix, f"hisp_nb_pub_{lvl}"] + a.loc[ix, f"hisp_fb_pub_{lvl}"]
    hp1 = b.loc[ix, f"hisp_nb_pub_{lvl}"] + b.loc[ix, f"hisp_fb_pub_{lvl}"]
    d["d_hisp_pub_n"] = (hp1 - hp0) / a.loc[ix, f"enr_{lvl}"] * 100
    fp0 = a.loc[ix, f"hisp_fb_pub_{lvl}"] + a.loc[ix, f"nonhisp_fb_pub_{lvl}"]
    fp1 = b.loc[ix, f"hisp_fb_pub_{lvl}"] + b.loc[ix, f"nonhisp_fb_pub_{lvl}"]
    d["d_fb_pub_n"] = (fp1 - fp0) / a.loc[ix, f"enr_{lvl}"] * 100
    return d.dropna()


def run_long(p, y0, y1, lvl, z=None, tag=""):
    d = diffs(p, y0, y1, lvl)
    w = d.w.to_numpy()
    one = np.ones(len(d))
    for treat in ("hisp_share", "fb_share"):
        X = np.column_stack([d[f"d_{treat}_{lvl}"].to_numpy(), one])
        b, se = wls(d[f"d_priv_wnh_{lvl}"].to_numpy(), X, w)
        rec(spec=f"long{tag} {y0}-{y1}", level=lvl, outcome="d priv share (wnh, US-born)",
            treatment=f"d {treat}", estimator="WLS HC1", n=len(d),
            coef=float(b[0]), se=float(se[0]), t=float(b[0] / se[0]))
    # horse race: Hispanic vs Asian vs Black share change
    X = np.column_stack([d[f"d_hisp_share_{lvl}"], d[f"d_asian_share_{lvl}"],
                         d[f"d_black_share_{lvl}"], one])
    b, se = wls(d[f"d_priv_wnh_{lvl}"].to_numpy(), X, w)
    for i, nm in enumerate(("d hisp_share", "d asian_share", "d black_share")):
        rec(spec=f"horse-race{tag} {y0}-{y1}", level=lvl,
            outcome="d priv share (wnh, US-born)", treatment=nm,
            estimator="WLS HC1", n=len(d), coef=float(b[i]), se=float(se[i]),
            t=float(b[i] / se[i]))
    # is the response white-specific? same regression for all US-born non-Hispanic
    # children, and for US-born Hispanic children
    for oc, wcol, nm in ((f"d_priv_nnh_{lvl}", f"nnh_enr_{lvl}", "all US-born non-Hispanic"),
                         (f"d_priv_hnb_{lvl}", f"hnb_enr_{lvl}", "US-born Hispanic")):
        s = d.dropna(subset=[oc])
        wv = p[p.year == y0].set_index("cbsa").loc[s.index, wcol].to_numpy()
        X = np.column_stack([s[f"d_hisp_share_{lvl}"].to_numpy(), np.ones(len(s))])
        bb, sse = wls(s[oc].to_numpy(), X, wv)
        rec(spec=f"by group{tag} {y0}-{y1}", level=lvl, outcome=f"d priv share ({nm})",
            treatment="d hisp_share", estimator="WLS HC1", n=len(s),
            coef=float(bb[0]), se=float(sse[0]), t=float(bb[0] / sse[0]))
    # generation split: foreign-born Hispanic (largely English-learner) vs US-born Hispanic
    X = np.column_stack([d["d_hispfb_share"], d["d_hispnb_share"], one])
    b, se = wls(d[f"d_priv_wnh_{lvl}"].to_numpy(), X, w)
    for i, nm in enumerate(("d hisp foreign-born share", "d hisp US-born share")):
        rec(spec=f"generation split{tag} {y0}-{y1}", level=lvl,
            outcome="d priv share (wnh, US-born)", treatment=nm,
            estimator="WLS HC1", n=len(d), coef=float(b[i]), se=float(se[i]),
            t=float(b[i] / se[i]))
    # counts: natives switching per Hispanic / per immigrant added to public schools
    for num, nm in (("d_hisp_pub_n", "d hispanic public enrol (per 100 base)"),
                    ("d_fb_pub_n", "d foreign-born public enrol (per 100 base)")):
        X = np.column_stack([d[num].to_numpy(), one])
        b, se = wls(d["d_wnh_priv_n"].to_numpy(), X, d.enr0.to_numpy())
        rec(spec=f"counts{tag} {y0}-{y1}", level=lvl,
            outcome="d wnh private enrol (per 100 base)", treatment=nm,
            estimator="WLS HC1", n=len(d), coef=float(b[0]), se=float(se[0]),
            t=float(b[0] / se[0]))
        # same regression with total enrolment growth controlled
        X = np.column_stack([d[num].to_numpy(), d["d_enr_n"].to_numpy(), one])
        b, se = wls(d["d_wnh_priv_n"].to_numpy(), X, d.enr0.to_numpy())
        rec(spec=f"counts, growth controlled{tag} {y0}-{y1}", level=lvl,
            outcome="d wnh private enrol (per 100 base)", treatment=nm,
            estimator="WLS HC1, + d total enrol", n=len(d), coef=float(b[0]),
            se=float(se[0]), t=float(b[0] / se[0]))
    # 2SLS
    if z is not None:
        zz = z.pivot(index="cbsa", columns="year")
        for zc in [c for c in ("z_fb", "z_mex") if c in z.columns]:
            if (y0 not in zz[zc].columns) or (y1 not in zz[zc].columns):
                continue
            dz = (zz[zc][y1] - zz[zc][y0]).reindex(d.index)
            m = dz.notna()
            if m.sum() < 30:
                continue
            b, se, F = tsls(d.loc[m, f"d_priv_wnh_{lvl}"].to_numpy(),
                            d.loc[m, f"d_fb_share_{lvl}"].to_numpy(),
                            dz[m].to_numpy(), np.ones(int(m.sum())),
                            d.loc[m, "w"].to_numpy())
            rec(spec=f"IV{tag} {y0}-{y1}", level=lvl,
                outcome="d priv share (wnh, US-born)", treatment="d fb_share",
                estimator=f"2SLS ({zc})", n=int(m.sum()), coef=float(b[0]),
                se=float(se[0]), t=float(b[0] / se[0]), first_stage_F=float(F))
    return d


def run_fe(p, lvl):
    d = p.dropna(subset=[f"priv_wnh_{lvl}", f"hisp_share_{lvl}"]).copy()
    cb = pd.get_dummies(d.cbsa, drop_first=True).to_numpy(float)
    yr = pd.get_dummies(d.year, drop_first=True).to_numpy(float)
    w = d[f"wnh_enr_{lvl}"].to_numpy()
    base = np.column_stack([cb, yr, np.ones(len(d))])
    for treat in ("hisp_share", "fb_share"):
        X = np.column_stack([d[f"{treat}_{lvl}"].to_numpy(), base])
        b, se = wls_cluster(d[f"priv_wnh_{lvl}"].to_numpy(), X, w, d.cbsa.to_numpy())
        rec(spec="two-way FE", level=lvl, outcome="priv share (wnh, US-born)",
            treatment=treat, estimator="WLS, cluster(CBSA)", n=len(d),
            coef=float(b[0]), se=float(se[0]), t=float(b[0] / se[0]))
    X = np.column_stack([d[f"hisp_share_{lvl}"], d[f"asian_share_{lvl}"],
                         d[f"black_share_{lvl}"], base])
    b, se = wls_cluster(d[f"priv_wnh_{lvl}"].to_numpy(), X, w, d.cbsa.to_numpy())
    for i, nm in enumerate(("hisp_share", "asian_share", "black_share")):
        rec(spec="two-way FE horse-race", level=lvl,
            outcome="priv share (wnh, US-born)", treatment=nm,
            estimator="WLS, cluster(CBSA)", n=len(d), coef=float(b[i]),
            se=float(se[i]), t=float(b[i] / se[i]))


def main():
    p, years = load()
    z = instrument(p, years)
    # ACS SCH=3 read "private school or college" through 2007 and "private school or
    # college OR HOME SCHOOL" from 2008 (checked against the Census API variable
    # dictionary, 2026-09-18). A long difference based on 2005 therefore mixes a
    # definitional change into the outcome, so the primary window starts at the first
    # year >= 2008; the 2005-based window is still reported, flagged.
    base = [y for y in years if y >= 2008]
    y0, y1 = (base[0] if base else years[0]), years[-1]
    if y0 == y1:
        y0 = years[0]
    mid = [y for y in years if y0 < y < y1]
    mid = mid[len(mid) // 2] if mid else y1
    for lvl in ("elem", "sec", "all"):
        run_long(p, y0, y1, lvl, z)
        if years[0] < y0:
            run_long(p, years[0], y1, lvl, z, tag=" [SCH def change]")
        run_fe(p, lvl)
    # reverse-timing placebo: does the EARLY outcome change predict the LATE treatment change?
    for lvl in (("elem", "sec") if len(years) >= 3 and mid not in (y0, y1) else ()):
        a = diffs(p, y0, mid, lvl)
        b_ = diffs(p, mid, y1, lvl)
        ix = a.index.intersection(b_.index)
        X = np.column_stack([b_.loc[ix, f"d_hisp_share_{lvl}"].to_numpy(), np.ones(len(ix))])
        bb, se = wls(a.loc[ix, f"d_priv_wnh_{lvl}"].to_numpy(), X, a.loc[ix, "w"].to_numpy())
        rec(spec=f"placebo pre-trend {y0}-{mid} on {mid}-{y1}", level=lvl,
            outcome=f"d priv share {y0}-{mid}", treatment=f"d hisp_share {mid}-{y1}",
            estimator="WLS HC1", n=len(ix), coef=float(bb[0]), se=float(se[0]),
            t=float(bb[0] / se[0]))
    # influence: drop the five largest metros, and drop California
    d = diffs(p, y0, y1, "sec")
    big5 = d.nlargest(5, "enr0").index
    for nm, sub in (("drop 5 largest metros", d.drop(index=big5)),
                    ("drop California", d[d.state_fips != 6])):
        X = np.column_stack([sub["d_hisp_share_sec"].to_numpy(), np.ones(len(sub))])
        b, se = wls(sub["d_priv_wnh_sec"].to_numpy(), X, sub.w.to_numpy())
        rec(spec=f"influence: {nm}", level="sec", outcome="d priv share (wnh, US-born)",
            treatment="d hisp_share", estimator="WLS HC1", n=len(sub),
            coef=float(b[0]), se=float(se[0]), t=float(b[0] / se[0]))
    out = pd.DataFrame(ROWS)
    out.to_csv(DERIVED / "estimates_flight.csv", index=False)
    print(f"\nwrote {DERIVED / 'estimates_flight.csv'} ({len(out)} rows)")


if __name__ == "__main__":
    main()
