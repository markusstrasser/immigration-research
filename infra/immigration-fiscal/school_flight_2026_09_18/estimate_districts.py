"""Design (b): does district spending and local tax effort move with the Hispanic share?

Outcomes (2020 dollars per pupil): current spending, instructional spending, local
revenue, local property-tax revenue, state revenue.
Treatment: Hispanic share of district enrollment, and an ethnic fractionalisation index.

Specifications, each weighted by enrolment and clustered on the district:
  A  district FE + year FE                  -- national within-district variation
  B  district FE + STATE x YEAR FE          -- the brief's spec; absorbs every change in
                                               a state's funding formula, so the
                                               comparison is between districts inside the
                                               same state in the same year
  C  B plus the county elderly share (Poterba's control) and its interaction with the
     Hispanic share
  D  B on local revenue and property-tax revenue only -- "tax effort"
  E  long difference 2000->2020

Fixed effects are absorbed by alternating within-transformations (Gaure/Correia), not
dummies: 13,000+ district effects cannot be inverted directly.
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"
ROWS = []


def rec(**kw):
    ROWS.append(kw)
    print(" | ".join(
        f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
        for k, v in kw.items() if k in ("spec", "outcome", "treatment", "n", "coef",
                                        "se", "t")), flush=True)


def absorb(M, groups, tol=1e-9, maxit=200):
    """Alternating projections: demean every column of M within each grouping."""
    M = np.asarray(M, float).copy()
    codes = [pd.factorize(g)[0] for g in groups]
    ns = [c.max() + 1 for c in codes]
    for _ in range(maxit):
        prev = M.copy()
        for c, n in zip(codes, ns):
            cnt = np.bincount(c, minlength=n).astype(float)
            for j in range(M.shape[1]):
                s = np.bincount(c, weights=M[:, j], minlength=n)
                M[:, j] -= (s / cnt)[c]
        if np.max(np.abs(M - prev)) < tol:
            break
    return M


def wabsorb(M, w, groups, tol=1e-9, maxit=200):
    """Weighted version: demean by weighted group means."""
    M = np.asarray(M, float).copy()
    codes = [pd.factorize(g)[0] for g in groups]
    ns = [c.max() + 1 for c in codes]
    for _ in range(maxit):
        prev = M.copy()
        for c, n in zip(codes, ns):
            sw = np.bincount(c, weights=w, minlength=n)
            for j in range(M.shape[1]):
                s = np.bincount(c, weights=M[:, j] * w, minlength=n)
                M[:, j] -= (s / sw)[c]
        if np.max(np.abs(M - prev)) < tol:
            break
    return M


def fit(y, X, w, cluster, k_absorbed):
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yw - Xw @ b
    XtXi = np.linalg.inv(XtX)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for _, ix in pd.Series(range(len(cluster))).groupby(np.asarray(cluster)).groups.items():
        ix = np.asarray(ix)
        s = Xw[ix].T @ e[ix]
        meat += np.outer(s, s)
    G, n = len(set(cluster)), len(y)
    dof = max(n - X.shape[1] - k_absorbed, 1)
    adj = (G / max(G - 1, 1)) * ((n - 1) / dof)
    V = XtXi @ meat @ XtXi * adj
    return b, np.sqrt(np.diag(V))


def run(d, outcome, treats, fes, label, extra=()):
    cols = [outcome] + list(treats) + list(extra)
    sub = d.dropna(subset=cols).copy()
    if len(sub) < 200:
        print(f"skip {label}/{outcome}: n={len(sub)}")
        return
    w = sub.pupils.to_numpy(float)
    groups = [sub[f].to_numpy() for f in fes]
    M = wabsorb(sub[cols].to_numpy(float), w, groups)
    k_abs = sum(len(pd.unique(g)) for g in groups)
    y, X = M[:, 0], M[:, 1:]
    b, se = fit(y, X, w, sub.leaid.to_numpy(), k_abs)
    for i, t in enumerate(list(treats) + list(extra)):
        rec(spec=label, outcome=outcome, treatment=t, estimator="WLS, cluster(district)",
            n=len(sub), coef=float(b[i]), se=float(se[i]), t=float(b[i] / se[i]),
            fe="+".join(fes))


def main():
    d = pd.read_csv(DERIVED / "district_panel.csv",
                    dtype={"leaid": str, "cofips": str, "state_year": str})
    print(f"panel {len(d):,} district-years, {d.leaid.nunique():,} districts")
    d["year_f"] = d.year.astype(str)
    outs = ["pp_current", "pp_instruction", "pp_rev_local", "pp_rev_proptax",
            "pp_rev_state", "pp_rev_total", "local_effort", "proptax_effort"]

    for o in outs:
        run(d, o, ["hisp_share"], ["leaid", "year_f"], "A district+year FE")
    for o in outs:
        run(d, o, ["hisp_share"], ["leaid", "state_year"], "B district+state-year FE")
    for o in ("pp_current", "pp_rev_local"):
        run(d, o, ["elf"], ["leaid", "state_year"], "B-elf district+state-year FE")
    # Poterba control. share65 is centred on its enrolment-weighted mean so that the
    # hisp_share coefficient is the effect at the average elderly share, not at zero
    # (which is outside the sample).
    dd = d.copy()
    m65 = float((dd.share65 * dd.pupils).sum() / dd.loc[dd.share65.notna(), "pupils"].sum())
    print(f"[poterba] enrolment-weighted mean county 65+ share = {m65:.4f}; centred")
    dd["share65_c"] = dd.share65 - m65
    dd["hisp_x_65"] = dd.hisp_share * dd.share65_c
    for o in ("pp_current", "pp_rev_local", "pp_rev_proptax"):
        run(dd, o, ["hisp_share", "share65_c", "hisp_x_65"], ["leaid", "state_year"],
            "C + elderly share (Poterba)")
    # long difference over the full available window
    ya, yb = int(d.year.min()), int(d.year.max())
    a = d[d.year == ya].set_index("leaid")
    b_ = d[d.year == yb].set_index("leaid")
    ix = a.index.intersection(b_.index)
    ld = pd.DataFrame(index=ix)
    for c in [o for o in outs] + ["hisp_share", "elf", "share65"]:
        ld["d_" + c] = b_.loc[ix, c] - a.loc[ix, c]
    ld["pupils"] = a.loc[ix, "pupils"]
    ld["fips"] = a.loc[ix, "fips"]
    ld["leaid"] = ix
    ld["state_year"] = ld.fips.astype(str)
    ld["year_f"] = "1"
    for o in outs:
        run(ld.reset_index(drop=True), "d_" + o, ["d_hisp_share"],
            ["state_year"], f"E long diff {ya}-{yb}, state FE")

    # F. reverse-timing placebo: does the EARLY change in the outcome move with the
    # LATE change in the Hispanic share? A non-zero coefficient means the association is
    # a pre-existing trend, not a response.
    yrs = sorted(d.year.unique())
    if len(yrs) >= 3:
        y0, ym, y1 = yrs[0], yrs[len(yrs) // 2], yrs[-1]
        A = d[d.year == y0].set_index("leaid")
        M = d[d.year == ym].set_index("leaid")
        Z = d[d.year == y1].set_index("leaid")
        ix = A.index.intersection(M.index).intersection(Z.index)
        pt = pd.DataFrame(index=ix)
        for o in outs:
            pt["d_" + o] = M.loc[ix, o] - A.loc[ix, o]
        pt["d_hisp_late"] = Z.loc[ix, "hisp_share"] - M.loc[ix, "hisp_share"]
        pt["d_hisp_early"] = M.loc[ix, "hisp_share"] - A.loc[ix, "hisp_share"]
        pt["pupils"] = A.loc[ix, "pupils"]
        pt["state_year"] = A.loc[ix, "fips"].astype(str)
        pt["leaid"] = ix
        for o in ("pp_current", "pp_rev_local", "pp_rev_proptax"):
            run(pt.reset_index(drop=True), "d_" + o, ["d_hisp_late"], ["state_year"],
                f"F placebo: d outcome {y0}-{ym} on d hisp {ym}-{y1}, state FE")
        # and the honest version: early outcome change on early treatment change
        for o in ("pp_current", "pp_rev_local", "pp_rev_proptax"):
            run(pt.reset_index(drop=True), "d_" + o, ["d_hisp_early"], ["state_year"],
                f"E2 long diff {y0}-{ym}, state FE")

    out = pd.DataFrame(ROWS)
    out.to_csv(DERIVED / "estimates_districts.csv", index=False)
    print(f"\nwrote {DERIVED/'estimates_districts.csv'} ({len(out)} rows)")


if __name__ == "__main__":
    main()
