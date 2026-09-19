#!/usr/bin/env python3
"""Positive controls for estim.py against statsmodels and closed-form IV."""
import numpy as np, pandas as pd, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estim
import statsmodels.api as sm

rng = np.random.default_rng(20260919)
n, G = 4000, 60
grp = rng.integers(0, G, n)
fe = rng.normal(0, 2, G)[grp]
w = rng.uniform(0.5, 5, n)

# ---- 1. WLS with FE dummies vs absorbed WLS -------------------------------
x1, x2 = rng.normal(size=n), rng.normal(size=n)
y = 1.5 * x1 - 0.7 * x2 + fe + rng.normal(0, 1, n)
df = pd.DataFrame({"y": y, "x1": x1, "x2": x2})
dm = estim.wdemean(df, ["y", "x1", "x2"], grp, w)
mine = estim.wls(dm["y"], dm[["x1", "x2"]], w, grp, ["x1", "x2"], k_absorbed=G)
D = pd.get_dummies(pd.Series(grp)).astype(float).to_numpy()  # full set, no constant
ref = sm.WLS(y, np.hstack([np.c_[x1, x2], D]), weights=w).fit(
    cov_type="cluster", cov_kwds={"groups": grp})
print(f"[wls] beta mine={mine['beta'][:2]} sm={ref.params[:2]}")
print(f"[wls] se   mine={mine['se'][:2]} sm={ref.bse[:2]}")
assert np.allclose(mine["beta"][:2], ref.params[:2], atol=1e-8), "WLS beta mismatch"
assert np.allclose(mine["se"][:2], ref.bse[:2], rtol=1e-6), "WLS cluster SE mismatch"

# ---- 2. Exactly identified 2SLS vs closed-form (Z'X)^-1 Z'y ---------------
z = rng.normal(size=n)
v = rng.normal(size=n)
xe = 0.8 * z + v                       # endogenous
y2 = 2.0 * xe + 0.5 * x2 + fe + (0.9 * v + rng.normal(0, 1, n))
df2 = pd.DataFrame({"y": y2, "xe": xe, "x2": x2, "z": z})
dm2 = estim.wdemean(df2, ["y", "xe", "x2", "z"], grp, w)
iv = estim.tsls(dm2["y"], dm2[["xe"]], dm2[["x2"]], dm2[["z"]], w, grp, ["xe"], ["x2"])
rw = np.sqrt(w)
Xs = np.c_[dm2["xe"], dm2["x2"]] * rw[:, None]
Zs = np.c_[dm2["z"], dm2["x2"]] * rw[:, None]
ys = dm2["y"].to_numpy() * rw
closed = np.linalg.solve(Zs.T @ Xs, Zs.T @ ys)
print(f"[2sls] beta mine={iv['beta']} closed={closed}  (true xe=2.0)")
assert np.allclose(iv["beta"], closed, atol=1e-9), "2SLS beta != closed form"
ols = estim.wls(dm2["y"], dm2[["xe", "x2"]], w, grp, ["xe", "x2"])
print(f"[2sls] OLS is biased as designed: {ols['beta'][0]:.3f} vs IV {iv['beta'][0]:.3f}")
assert abs(iv["beta"][0] - 2.0) < 0.12, "IV far from truth"
assert ols["beta"][0] - 2.0 > 0.2, "OLS should be upward biased here"

# ---- 3. Overidentified: J should not reject a valid instrument set --------
z2 = rng.normal(size=n)
xe3 = 0.8 * z + 0.6 * z2 + v
y3 = 2.0 * xe3 + 0.5 * x2 + fe + (0.9 * v + rng.normal(0, 1, n))
df3 = pd.DataFrame({"y": y3, "xe": xe3, "x2": x2, "z": z, "z2": z2})
dm3 = estim.wdemean(df3, ["y", "xe", "x2", "z", "z2"], grp, w)
iv3 = estim.tsls(dm3["y"], dm3[["xe"]], dm3[["x2"]], dm3[["z", "z2"]], w, grp,
                 ["xe"], ["x2"])
print(f"[over] beta={iv3['beta'][0]:.3f} F_first={iv3['F_first']:.1f} "
      f"J={iv3['J']:.2f} df={iv3['J_df']} p={iv3['J_p']:.3f}")
assert iv3["F_first"] > 50, "first-stage F implausibly weak"
assert iv3["J_p"] > 0.01, "J rejects a valid instrument set"

# ---- 4. Invalid instrument SHOULD be rejected by J ------------------------
zbad = 0.5 * v + rng.normal(size=n)     # correlated with the structural error
dm4 = estim.wdemean(pd.DataFrame({"y": y3, "xe": xe3, "x2": x2, "z": z, "zb": zbad}),
                    ["y", "xe", "x2", "z", "zb"], grp, w)
iv4 = estim.tsls(dm4["y"], dm4[["xe"]], dm4[["x2"]], dm4[["z", "zb"]], w, grp,
                 ["xe"], ["x2"])
print(f"[bad]  beta={iv4['beta'][0]:.3f} J p={iv4['J_p']:.4f} (should reject)")
assert iv4["J_p"] < 0.05, "J failed to flag an invalid instrument"
print("ALL ESTIMATOR CONTROLS PASSED")
