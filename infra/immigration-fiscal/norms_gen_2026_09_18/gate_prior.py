"""Gate: reproduce the 2026-09-17 social lane's adjusted GSS trust gaps
(three-response denominator, NORC preferred weights, full design variance)."""
import numpy as np, pandas as pd
from norms_lib import *
from estimate import covariates, wls, contrast

d = load(); d, lab = assign_groups(d); des = Design(d)
valid = d.trust.isin([1, 2, 3]).to_numpy()
y = d.trust.eq(1).to_numpy(float)
sample = valid & (lab["NHWhite G3+"] | lab["Hisp G1"] | lab["Hisp G2"] |
                 lab["Hisp G3+"] | lab["NHWhite G1-2"])
Z, Zn = covariates(d, use_educ=True, use_income=False)
# prior lane dropped rows with missing age or educ rather than imputing
have = d.age.notna().to_numpy() & d.educ.notna().to_numpy()
fit = wls(d, des, np.where(valid, y, np.nan), sample & have,
          [(g, lab[g]) for g in ["Hisp G1", "Hisp G2", "Hisp G3+", "NHWhite G1-2"]], Z, Zn)
TARGET = {"Hisp G1": (-11.81, 1.55), "Hisp G2": (-11.22, 2.01), "Hisp G3+": (-9.73, 1.99)}
ok = True
print("gate vs frontier_execution_2026_09_17/social (pp):")
for g, (te, ts) in TARGET.items():
    e, s = contrast(fit, {g: 1.0})
    de, ds = abs(e * 100 - te), abs(s * 100 - ts)
    ok &= de < 0.06 and ds < 0.06
    print(f"  {g:9s} mine {e*100:7.3f} ({s*100:.3f})   theirs {te:7.2f} ({ts:.2f})   d={de:.3f}/{ds:.3f}")
print("n =", fit["n"], "| GATE:", "PASS" if ok else "FAIL")
assert ok
