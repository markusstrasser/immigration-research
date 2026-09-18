"""Weighted descriptive means and design-based WLS with arbitrary linear contrasts."""
import numpy as np, pandas as pd, math


def covariates(d, use_educ=True, use_income=True):
    """Returns (matrix, names). Income missing is median-imputed with a flag so the
    income control does not silently shrink every cell."""
    age = d.age.to_numpy(dtype=float)
    age = np.where(np.isfinite(age), age, np.nanmedian(age))
    cols = [np.ones(len(d)), age / 50.0, (age / 50.0) ** 2]
    names = ["const", "age", "age2"]
    if use_educ:
        e = d.educ.to_numpy(dtype=float)
        e = np.where(np.isfinite(e), e, np.nanmedian(e))
        cols.append(e / 10.0); names.append("educ")
    if use_income:
        inc = d.coninc.to_numpy(dtype=float)
        miss = ~np.isfinite(inc) | (inc <= 0)
        filled = np.where(miss, np.nanmedian(inc[~miss]), inc)
        cols.append(np.log(filled) / 10.0); names.append("loginc")
        cols.append(miss.astype(float)); names.append("inc_missing")
    # Survey-year fixed effects are NOT added here: an item fielded in a subset of
    # years would otherwise carry a full set of dummies summing to the intercept and
    # the model would be rank deficient. wls() builds them inside the estimation sample.
    return np.column_stack(cols), names


def wls(d, design, y, sample, dummies, Z, Znames, year_fe=True):
    """Design-linearised WLS. dummies: list of (name, boolean array) added to Z.
    Returns dict name -> index, beta, and the full design covariance."""
    y = np.asarray(y, dtype=float)
    m = sample & np.isfinite(y)
    if m.sum() < 30:
        return None
    ix = np.flatnonzero(m)
    D = np.column_stack([v[m].astype(float) for _, v in dummies]) if dummies else None
    parts, names = [Z[m]], list(Znames)
    if year_fe:
        yr = d.year.to_numpy()[m]
        present = sorted(np.unique(yr))[1:]          # first year present is the reference
        if present:
            parts.append(np.column_stack([(yr == v).astype(float) for v in present]))
            names += [f"y{int(v)}" for v in present]
    if D is not None:
        parts.append(D); names += [n for n, _ in dummies]
    X = np.column_stack(parts)
    # drop all-zero / collinear dummy columns
    keep = np.array([X[:, j].std() > 0 or names[j] == "const" for j in range(X.shape[1])])
    X, names = X[:, keep], [n for n, k in zip(names, keep) if k]
    w = d.w.to_numpy()[m]
    XtWX = X.T @ (w[:, None] * X)
    if np.linalg.matrix_rank(XtWX) < XtWX.shape[0]:
        return None
    bread = np.linalg.inv(XtWX)
    beta = bread @ (X.T @ (w * y[m]))
    err = y[m] - X @ beta
    infl = np.zeros((len(d), len(beta)))
    infl[ix] = (w[:, None] * X * err[:, None]) @ bread
    return dict(names=names, beta=beta, cov=design.cov(infl), n=int(m.sum()))


def contrast(fit, spec):
    """spec: dict name -> weight. Returns (estimate, se) or None if a name is absent."""
    if fit is None:
        return None
    idx = {n: i for i, n in enumerate(fit["names"])}
    if any(k not in idx for k in spec):
        return None
    c = np.zeros(len(fit["beta"]))
    for k, v in spec.items():
        c[idx[k]] = v
    est = float(c @ fit["beta"])
    se = math.sqrt(max(0.0, float(c @ fit["cov"] @ c)))
    return est, se
