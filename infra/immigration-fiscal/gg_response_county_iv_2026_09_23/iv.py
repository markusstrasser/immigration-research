"""Linear IV with one endogenous regressor, state-clustered inference. numpy only.

Every estimator partials the exogenous block (intercept, controls, fixed effects) out of the
weighted variables first (Frisch-Waugh-Lovell), which leaves point estimates and cluster-robust
variances of the remaining coefficients unchanged. Small-sample factor CR1: G/(G-1) * (N-1)/(N-K),
K counting the partialled columns.

  ols(...)          y on x
  first_stage(...)  x on Z: coefficients, CR1 covariance, Montiel Olea-Pflueger effective F
  tsls(...)         2SLS, reduced form, Anderson-Rubin set, Hansen J (two-step GMM, L > 1)
  rotemberg(...)    Goldsmith-Pinkham, Sorkin and Swift decomposition of a shift-share 2SLS

Anderson-Rubin sets use chi-square critical values (3.841 for one instrument, 5.991 for two). With
one instrument the set is solved exactly from the quadratic; with two it is inverted on a grid.
"""
import math

import numpy as np

CHI2_95 = {1: 3.841458820694124, 2: 5.991464547107979}


class Prepared:
    def __init__(self, y, x, Z, W, weights, clusters):
        n = len(y)
        s = np.sqrt(weights / weights.mean())
        Ws = W * s[:, None]
        U, sv, _ = np.linalg.svd(Ws, full_matrices=False)
        keep = sv > sv.max() * max(Ws.shape) * np.finfo(float).eps
        q = U[:, keep]
        self.kw = int(keep.sum())
        part = lambda v: (v * s) - q @ (q.T @ (v * s))
        self.y = part(y)
        self.x = part(x)
        self.Z = np.column_stack([part(Z[:, j]) for j in range(Z.shape[1])]) if Z is not None and Z.size else None
        self.n = n
        codes, self.g = np.unique(clusters, return_inverse=True)
        self.G = len(codes)
        self.part = part

    def cr1(self, k_extra):
        k = self.kw + k_extra
        return self.G / (self.G - 1) * (self.n - 1) / (self.n - k)

    def cluster_sum(self, m):
        out = np.zeros((self.G,) + m.shape[1:])
        np.add.at(out, self.g, m)
        return out


def ols(p):
    xx = p.x @ p.x
    b = (p.x @ p.y) / xx
    u = p.y - p.x * b
    sc = p.cluster_sum(p.x * u)
    v = (sc @ sc) / xx ** 2 * p.cr1(1)
    return {"beta": float(b), "se": float(math.sqrt(v))}


def _coef_cov(p, X, r, k_extra):
    xtx_inv = np.linalg.inv(X.T @ X)
    b = xtx_inv @ (X.T @ r)
    e = r - X @ b
    sc = p.cluster_sum(X * e[:, None])
    V = xtx_inv @ (sc.T @ sc) @ xtx_inv * p.cr1(k_extra)
    return b, V, e


def first_stage(p):
    Z = p.Z
    pi, V, e = _coef_cov(p, Z, p.x, Z.shape[1])
    ztz = Z.T @ Z
    f_eff = float(pi @ ztz @ pi / np.trace(V @ ztz))
    wald = float(pi @ np.linalg.solve(V, pi) / len(pi))
    return {"pi": pi, "V": V, "F_eff": f_eff, "F_robust": wald, "resid": e}


def tsls(p, grid=(-6.0, 6.0, 0.0005)):
    Z = p.Z
    L = Z.shape[1]
    fs = first_stage(p)
    gam, Vg, ey = _coef_cov(p, Z, p.y, L)
    xhat = Z @ fs["pi"]
    beta = float((xhat @ p.y) / (xhat @ p.x))
    u = p.y - p.x * beta
    sc = p.cluster_sum(xhat * u)
    se = float(math.sqrt((sc @ sc) / (xhat @ xhat) ** 2 * p.cr1(1)))
    out = {"beta": beta, "se": se, "pi": fs["pi"], "pi_se": np.sqrt(np.diag(fs["V"])), "F_eff": fs["F_eff"],
           "F_robust": fs["F_robust"], "gamma": gam, "gamma_se": np.sqrt(np.diag(Vg))}
    if L == 1:
        out["ar"] = ar_exact(p, gam[0], fs["pi"][0], ey, fs["resid"])
    else:
        out["ar"] = ar_grid(p, grid)
        out["J"], out["J_p"], out["beta_gmm"] = hansen_j(p, beta)
    return out


def ar_exact(p, g, pi, ey, ex):
    z = p.Z[:, 0]
    zz = z @ z
    a = p.cluster_sum(z * ey) / zz
    b = p.cluster_sum(z * ex) / zz
    c = p.cr1(1)
    vyy, vxx, vyx = (a @ a) * c, (b @ b) * c, (a @ b) * c
    crit = CHI2_95[1]
    A = pi * pi - crit * vxx
    B = -2 * (g * pi - crit * vyx)
    C = g * g - crit * vyy
    disc = B * B - 4 * A * C
    if A > 0:
        if disc < 0:
            return {"type": "empty", "lo": math.nan, "hi": math.nan}
        r = sorted([(-B - math.sqrt(disc)) / (2 * A), (-B + math.sqrt(disc)) / (2 * A)])
        return {"type": "interval", "lo": r[0], "hi": r[1]}
    if disc < 0:
        return {"type": "real line", "lo": -math.inf, "hi": math.inf}
    r = sorted([(-B - math.sqrt(disc)) / (2 * A), (-B + math.sqrt(disc)) / (2 * A)])
    return {"type": "two rays", "lo": r[0], "hi": r[1]}


def ar_stat(p, b0):
    r = p.y - b0 * p.x
    gam, V, _ = _coef_cov(p, p.Z, r, p.Z.shape[1])
    return float(gam @ np.linalg.solve(V, gam))


def ar_grid(p, grid):
    """AR(b) = g(b)' V(b)^-1 g(b) with g(b) = gamma_y - b pi and cluster scores a_g - b c_g, on a grid."""
    lo, hi, step = grid
    L = p.Z.shape[1]
    crit = CHI2_95[L]
    pts = np.arange(lo, hi + step / 2, step)
    zinv = np.linalg.inv(p.Z.T @ p.Z)
    gy, gx = zinv @ (p.Z.T @ p.y), zinv @ (p.Z.T @ p.x)
    ey, ex = p.y - p.Z @ gy, p.x - p.Z @ gx
    a = p.cluster_sum(p.Z * ey[:, None]) @ zinv
    c = p.cluster_sum(p.Z * ex[:, None]) @ zinv
    k = p.cr1(L)
    Vyy, Vxx, Vyx = a.T @ a * k, c.T @ c * k, a.T @ c * k
    g = gy[None, :] - pts[:, None] * gx[None, :]
    V = Vyy[None] - pts[:, None, None] * (Vyx + Vyx.T)[None] + (pts ** 2)[:, None, None] * Vxx[None]
    stat = np.einsum("mi,mi->m", g, np.linalg.solve(V, g[..., None])[..., 0])
    ok = stat <= crit
    for b in (pts[len(pts) // 3], pts[len(pts) // 2]):
        direct = ar_stat(p, b)
        if abs(direct - float(stat[np.searchsorted(pts, b)])) > 1e-6 * max(1.0, direct):
            raise ValueError("vectorised Anderson-Rubin statistic disagrees with the direct regression")
    if not ok.any():
        return {"type": "empty on grid", "lo": math.nan, "hi": math.nan, "pieces": []}
    pieces, start = [], None
    for b, flag in zip(pts, ok):
        if flag and start is None:
            start = b
        if not flag and start is not None:
            pieces.append((start, prev))
            start = None
        prev = b
    if start is not None:
        pieces.append((start, prev))
    unbounded = ok[0] or ok[-1]
    kind = ("unbounded on grid" if unbounded else "interval") if len(pieces) == 1 else "disjoint"
    return {"type": kind, "lo": float(pieces[0][0]) if not ok[0] else -math.inf,
            "hi": float(pieces[-1][1]) if not ok[-1] else math.inf, "pieces": [(float(a), float(b)) for a, b in pieces]}


def hansen_j(p, beta1):
    Z = p.Z
    u1 = p.y - p.x * beta1
    s1 = p.cluster_sum(Z * u1[:, None])
    S = s1.T @ s1
    Sinv = np.linalg.inv(S)
    zx, zy = Z.T @ p.x, Z.T @ p.y
    beta2 = float((zx @ Sinv @ zy) / (zx @ Sinv @ zx))
    u2 = p.y - p.x * beta2
    gbar = Z.T @ u2
    J = float(gbar @ Sinv @ gbar)
    df = Z.shape[1] - 1
    pval = math.erfc(math.sqrt(J / 2)) if df == 1 else math.nan
    return J, pval, beta2


def rotemberg(p, components):
    """components: n x K matrix of shift-share pieces (weighted and partialled here)."""
    B = np.column_stack([p.part(components[:, k]) for k in range(components.shape[1])])
    num_x = B.T @ p.x
    num_y = B.T @ p.y
    alpha = num_x / num_x.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        beta_k = np.where(num_x != 0, num_y / num_x, np.nan)
    return alpha, beta_k, float(num_y.sum() / num_x.sum())
