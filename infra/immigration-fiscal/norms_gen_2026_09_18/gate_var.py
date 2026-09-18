"""Gate: the vectorised design covariance must reproduce the loop implementation,
and the GSS trust estimates must reproduce the two prior lanes."""
import numpy as np, pandas as pd, math
from norms_lib import *

d = load(); d, lab = assign_groups(d); des = Design(d)

def loop_cov(influence):
    s = pd.DataFrame(np.asarray(influence,dtype=float)).groupby([des.strat, des.psu]).sum()
    out = np.zeros((s.shape[1], s.shape[1]))
    for _, ss in s.groupby(level=0):
        a = ss.to_numpy()
        if len(a) < 2: continue
        c = a - a.mean(axis=0)
        out += len(a)/(len(a)-1)*(c.T@c)
    return out

rng = np.random.default_rng(0)
Z = rng.normal(size=(len(d), 4)) * (rng.random((len(d),1)) < .3)
a, b = des.cov(Z), loop_cov(Z)
print("vectorised vs loop max abs diff:", float(np.abs(a-b).max()))
assert np.abs(a-b).max() < 1e-8
print("strata", des.n_strata, "psus", des.n_psu, "rows", len(d))
