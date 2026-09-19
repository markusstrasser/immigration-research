#!/usr/bin/env python3
"""Weighted within-group OLS and 2SLS with cluster-robust inference.

All estimators absorb a single fixed-effect group by weighted demeaning, then
work on sqrt(w)-scaled data so the remaining algebra is ordinary least squares.
"""
import numpy as np
import pandas as pd


def wdemean(df, cols, group, w):
    """Weighted within-group demeaning (the WLS analogue of absorbing FE)."""
    out = pd.DataFrame(index=df.index)
    wv = np.asarray(w, dtype=float)
    g = np.asarray(group)
    sw = pd.Series(wv, index=df.index).groupby(g).transform("sum").to_numpy()
    for c in cols:
        x = np.asarray(df[c], dtype=float)
        num = pd.Series(wv * x, index=df.index).groupby(g).transform("sum").to_numpy()
        out[c] = x - num / sw
    return out


def _cluster_meat(score, clusters):
    """Sum of outer products of cluster-summed scores."""
    s = pd.DataFrame(score)
    s["_g"] = np.asarray(clusters)
    gs = s.groupby("_g").sum().to_numpy()
    return gs.T @ gs, gs.shape[0]


def wls(y, X, w, clusters, names, k_absorbed=0):
    w = np.asarray(w, float)
    rw = np.sqrt(w)
    ys = np.asarray(y, float) * rw
    Xs = np.asarray(X, float) * rw[:, None]
    XtX = Xs.T @ Xs
    beta = np.linalg.solve(XtX, Xs.T @ ys)
    u = ys - Xs @ beta
    meat, G = _cluster_meat(Xs * u[:, None], clusters)
    bread = np.linalg.inv(XtX)
    n, k = Xs.shape
    k += k_absorbed  # absorbed fixed effects still consume degrees of freedom
    adj = (G / (G - 1)) * ((n - 1) / (n - k))
    V = bread @ meat @ bread * adj
    se = np.sqrt(np.diag(V))
    r2 = 1 - (u @ u) / (ys @ ys) if ys @ ys > 0 else np.nan
    return {"names": list(names), "beta": beta, "se": se, "n": n, "G": G,
            "r2": r2, "resid": u, "V": V}


def tsls(y, Xend, Xexo, Z, w, clusters, names_end, names_exo, k_absorbed=0):
    """2SLS: Xend instrumented by Z, Xexo included. All inputs already demeaned."""
    w = np.asarray(w, float)
    rw = np.sqrt(w)
    ys = np.asarray(y, float) * rw
    Xe = np.asarray(Xend, float) * rw[:, None]
    Xx = (np.asarray(Xexo, float) * rw[:, None]
          if np.size(Xexo) else np.empty((len(ys), 0)))
    Zx = np.asarray(Z, float) * rw[:, None]
    X = np.hstack([Xe, Xx])
    Zfull = np.hstack([Zx, Xx])
    ZtZ = Zfull.T @ Zfull
    Pi = np.linalg.solve(ZtZ, Zfull.T @ X)
    Xhat = Zfull @ Pi
    A = np.linalg.inv(Xhat.T @ Xhat)
    beta = A @ (Xhat.T @ ys)
    u = ys - X @ beta
    meat, G = _cluster_meat(Xhat * u[:, None], clusters)
    n, k = X.shape
    k += k_absorbed
    adj = (G / (G - 1)) * ((n - 1) / (n - k))
    V = A @ meat @ A * adj
    se = np.sqrt(np.diag(V))

    # Cluster-robust first-stage F on the excluded instruments (first endogenous).
    y1 = Xe[:, 0]
    fs = wls(y1 / rw, np.hstack([Zx, Xx]) / rw[:, None], w, clusters,
             [f"z{i}" for i in range(Zx.shape[1])] + [f"x{i}" for i in range(Xx.shape[1])],
             k_absorbed=k_absorbed)
    q = Zx.shape[1]
    R = np.zeros((q, fs["beta"].size)); R[:, :q] = np.eye(q)
    Rb = R @ fs["beta"]
    RVR = R @ fs["V"] @ R.T
    F = float(Rb @ np.linalg.solve(RVR, Rb) / q)

    # Do not label a moment quadratic at the 2SLS estimate as Hansen J.
    # ivreg2's robust test requires the corresponding efficient-GMM estimate
    # (Baum/Schaffer/Stillman 2003, section 4.3). This within-only API lacks
    # the full FE moment design needed to certify that test in general.
    # Original-paper J is verified separately in hedonic_replay/src/verify_original.py.
    J, Jdf, Jp = np.nan, max(Zx.shape[1] - Xe.shape[1], 0), np.nan
    Jstatus = ("unavailable_requires_verified_efficient_GMM" if Jdf > 0
               else "not_applicable_exactly_identified")
    return {"names": list(names_end) + list(names_exo), "beta": beta, "se": se,
            "n": n, "G": G, "F_first": F, "J": J, "J_df": Jdf, "J_p": Jp,
            "J_status": Jstatus,
            "r2": np.nan, "resid": u, "V": V}


def row(res, focus):
    i = res["names"].index(focus)
    b, s = res["beta"][i], res["se"][i]
    return {"coef": b, "se": s, "t": b / s if s else np.nan,
            "n": res["n"], "clusters": res["G"],
            "F_first": res.get("F_first", np.nan),
            "J_p": res.get("J_p", np.nan),
            "J_status": res.get("J_status", "not_applicable_WLS"),
            "r2": res.get("r2", np.nan)}
