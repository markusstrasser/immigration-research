"""Weighted fixed-effect absorption and cluster-robust WLS / 2SLS.

Kept deliberately small and inspectable: alternating projections (Frisch-Waugh)
to absorb high-dimensional fixed effects, then weighted least squares with a
cluster-robust sandwich. No linearmodels / pyfixest dependency.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def absorb(df: pd.DataFrame, cols: list[str], fes: list[str],
           w: np.ndarray, tol: float = 1e-10, maxit: int = 500) -> pd.DataFrame:
    """Return `cols` with the weighted group means of every fixed effect removed."""
    out = df[cols].to_numpy(dtype=float).copy()
    keys = [df[f].to_numpy() for f in fes]
    codes = [pd.factorize(k)[0] for k in keys]
    ngrp = [c.max() + 1 for c in codes]
    for _ in range(maxit):
        delta = 0.0
        for c, n in zip(codes, ngrp):
            wsum = np.bincount(c, weights=w, minlength=n)
            for j in range(out.shape[1]):
                gsum = np.bincount(c, weights=w * out[:, j], minlength=n)
                m = np.where(wsum > 0, gsum / np.where(wsum > 0, wsum, 1), 0.0)
                adj = m[c]
                out[:, j] -= adj
                delta = max(delta, float(np.max(np.abs(adj))))
        if delta < tol:
            break
    return pd.DataFrame(out, columns=cols, index=df.index)


def wls_cluster(y: np.ndarray, X: np.ndarray, w: np.ndarray,
                cluster: np.ndarray, absorbed: int = 0) -> dict:
    """WLS with a cluster-robust (CR1) sandwich. X must already include any
    constant, or be fully demeaned (then no constant is needed)."""
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw
    XtXi = np.linalg.pinv(XtX)
    beta = XtXi @ (Xw.T @ yw)
    resid = yw - Xw @ beta
    cl, _ = pd.factorize(cluster)
    G = cl.max() + 1
    meat = np.zeros_like(XtX)
    for g in range(G):
        m = cl == g
        s = Xw[m].T @ resid[m]
        meat += np.outer(s, s)
    n, k = X.shape
    dof = max(n - k - absorbed, 1)
    scale = (G / max(G - 1, 1)) * ((n - 1) / dof)
    V = XtXi @ meat @ XtXi * scale
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return {"beta": beta, "se": se, "t": beta / np.where(se > 0, se, np.nan),
            "n": n, "clusters": G, "dof": dof,
            "r2_within": float(1 - (resid @ resid) / max(float(yw @ yw), 1e-30))}


def tsls_cluster(y: np.ndarray, X: np.ndarray, Z: np.ndarray, w: np.ndarray,
                 cluster: np.ndarray, absorbed: int = 0) -> dict:
    """Just-identified or over-identified 2SLS with the same sandwich, plus the
    first-stage cluster-robust F on the excluded instrument(s)."""
    sw = np.sqrt(w)
    Xw, yw, Zw = X * sw[:, None], y * sw, Z * sw[:, None]
    ZtZi = np.linalg.pinv(Zw.T @ Zw)
    Pz_X = Zw @ (ZtZi @ (Zw.T @ Xw))
    A = np.linalg.pinv(Pz_X.T @ Xw)
    beta = A @ (Pz_X.T @ yw)
    resid = yw - Xw @ beta
    cl, _ = pd.factorize(cluster)
    G = cl.max() + 1
    bread = A
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in range(G):
        m = cl == g
        s = Pz_X[m].T @ resid[m]
        meat += np.outer(s, s)
    n, k = X.shape
    dof = max(n - k - absorbed, 1)
    scale = (G / max(G - 1, 1)) * ((n - 1) / dof)
    V = bread @ meat @ bread.T * scale
    se = np.sqrt(np.maximum(np.diag(V), 0))
    fs = wls_cluster(X[:, 0], Z, w, cluster, absorbed=absorbed)
    F = float((fs["beta"][0] / fs["se"][0]) ** 2) if fs["se"][0] > 0 else np.nan
    return {"beta": beta, "se": se, "t": beta / np.where(se > 0, se, np.nan),
            "n": n, "clusters": G, "first_stage_beta": float(fs["beta"][0]),
            "first_stage_se": float(fs["se"][0]), "first_stage_F": F}
