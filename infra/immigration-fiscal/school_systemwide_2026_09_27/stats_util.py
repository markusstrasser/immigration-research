"""Small, dependency-free estimation helpers: OLS with dummy fixed effects and CR1 cluster-robust
standard errors, Student-t p-values, and a seeded permutation test. numpy and pandas only."""
import math

import numpy as np
import pandas as pd


def _betacf(a, b, x):
    """Continued fraction for the regularized incomplete beta (Numerical Recipes, Lentz)."""
    tiny, eps = 1e-300, 3e-16
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbeta) * _betacf(a, b, x) / a
    return 1.0 - math.exp(lbeta) * _betacf(b, a, 1 - x) / b


def t_pvalue(t, df):
    """Two-sided p-value of a Student-t statistic."""
    return betainc(df / 2.0, 0.5, df / (df + t * t))


def t_quantile(p, df):
    """Quantile of Student t by bisection on the CDF (p in (0.5, 1))."""
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 1 - t_pvalue(mid, df) / 2 < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def ols(df, y, x, fe=(), cluster=None, weight=None):
    """OLS of y on regressors x plus dummy fixed effects fe (list of column names or tuples of names).

    Returns a dict per regressor with coef, CR1 cluster-robust se (clustered on `cluster`; HC1 if None),
    t, p (t with G-1 df), n, clusters. Rows with any missing value are dropped."""
    cols = [y] + list(x) + [c for f in fe for c in ((f,) if isinstance(f, str) else f)]
    cols += [cluster] if cluster else []
    cols += [weight] if weight else []
    d = df.dropna(subset=list(dict.fromkeys(cols))).copy()
    X = [d[list(x)].to_numpy(float)]
    names = list(x)
    for f in fe:
        key = d[f].astype(str) if isinstance(f, str) else d[list(f)].astype(str).agg("|".join, axis=1)
        dummies = pd.get_dummies(key, drop_first=True, dtype=float)
        X.append(dummies.to_numpy())
    X.append(np.ones((len(d), 1)))
    X = np.hstack(X)
    Y = d[y].to_numpy(float)
    w = d[weight].to_numpy(float) if weight else np.ones(len(d))
    sw = np.sqrt(w)
    Xw, Yw = X * sw[:, None], Y * sw
    # drop collinear columns deterministically (QR with a tolerance)
    q, r = np.linalg.qr(Xw)
    keep = np.abs(np.diag(r)) > 1e-9 * np.abs(np.diag(r)).max()
    if not keep[: len(names)].all():
        raise ValueError(f"regressor collinear with fixed effects: {[n for n, k in zip(names, keep) if not k]}")
    Xw, X = Xw[:, keep], X[:, keep]
    XtX_inv = np.linalg.inv(Xw.T @ Xw)
    beta = XtX_inv @ Xw.T @ Yw
    u = Yw - Xw @ beta
    n, k = Xw.shape
    if cluster:
        g = d[cluster].to_numpy()
        G = len(np.unique(g))
        meat = np.zeros((k, k))
        for gv in np.unique(g):
            idx = g == gv
            s = Xw[idx].T @ u[idx]
            meat += np.outer(s, s)
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
        dof = G - 1
    else:
        G = n
        meat = (Xw * u[:, None]).T @ (Xw * u[:, None])
        V = XtX_inv @ meat @ XtX_inv * n / (n - k)
        dof = n - k
    out = {}
    for i, nm in enumerate(names):
        se = float(np.sqrt(V[i, i]))
        t = float(beta[i] / se) if se > 0 else float("nan")
        out[nm] = {"coef": float(beta[i]), "se": se, "t": t, "p": t_pvalue(t, dof) if se > 0 else float("nan"),
                   "n": int(n), "clusters": int(G), "dof": int(dof)}
    return out


def permutation_p(df, y, x, fe=(), cluster=None, weight=None, perm_within=None, reps=2000, seed=20260927):
    """Two-sided permutation p-value for the coefficient on x[0]: the regressor's values are shuffled
    across the units in `perm_within` (a column naming the unit, e.g. state), keeping each unit's
    series intact."""
    base = ols(df, y, x, fe, cluster, weight)[x[0]]["coef"]
    rng = np.random.default_rng(seed)
    d = df.dropna(subset=[y] + list(x)).copy()
    units = sorted(d[perm_within].unique())
    hits = 0
    for _ in range(reps):
        perm = dict(zip(units, rng.permutation(units)))
        # map each unit's regressor series to another unit's, matching on the remaining index columns
        src = d.set_index([perm_within] + [c for c in d.columns if c.startswith("_key")])[x[0]]
        d2 = d.copy()
        keys = [perm_within] + [c for c in d.columns if c.startswith("_key")]
        d2[x[0]] = [src.get(tuple([perm[r[0]]] + list(r[1:])), np.nan) for r in d2[keys].itertuples(index=False)]
        c = ols(d2, y, x, fe, cluster, weight)[x[0]]["coef"]
        hits += abs(c) >= abs(base) - 1e-12
    return (hits + 1) / (reps + 1)


def ols_absorb(df, y, x, absorb, cluster, weight=None, tol=1e-10, max_iter=10000):
    """OLS of y on x with high-dimensional fixed effects absorbed by alternating projections
    (weighted group demeaning), CR1 cluster-robust SEs. Every absorbed group must nest within a
    cluster (e.g. district and state-by-year effects with state clusters), so no degrees-of-freedom
    correction for the absorbed effects is needed."""
    cols = [y] + list(x) + list(absorb) + [cluster] + ([weight] if weight else [])
    d = df.dropna(subset=list(dict.fromkeys(cols))).reset_index(drop=True)
    w = d[weight].to_numpy(float) if weight else np.ones(len(d))
    M = d[[y] + list(x)].to_numpy(float).copy()
    codes = [pd.factorize(d[a])[0] for a in absorb]
    wsum = [np.bincount(c, weights=w) for c in codes]
    for _ in range(max_iter):
        old = M.copy()
        for c, ws in zip(codes, wsum):
            for j in range(M.shape[1]):
                means = np.bincount(c, weights=w * M[:, j]) / ws
                M[:, j] -= means[c]
        if np.max(np.abs(M - old)) < tol:
            break
    else:
        raise RuntimeError("fixed-effect demeaning did not converge")
    Y, X = M[:, 0], M[:, 1:]
    sw = np.sqrt(w)
    Xw, Yw = X * sw[:, None], Y * sw
    XtX_inv = np.linalg.inv(Xw.T @ Xw)
    beta = XtX_inv @ Xw.T @ Yw
    u = Yw - Xw @ beta
    n, k = Xw.shape
    g = d[cluster].to_numpy()
    uniq = np.unique(g)
    G = len(uniq)
    meat = np.zeros((k, k))
    idx_sorted = pd.factorize(g)[0]
    S = np.zeros((G, k))
    np.add.at(S, idx_sorted, Xw * u[:, None])
    meat = S.T @ S
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
    out = {}
    for i, nm in enumerate(x):
        se = float(np.sqrt(V[i, i]))
        t = float(beta[i] / se)
        out[nm] = {"coef": float(beta[i]), "se": se, "t": t, "p": t_pvalue(t, G - 1), "n": int(n), "clusters": int(G),
                   "dof": int(G - 1)}
    return out
