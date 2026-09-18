"""Disconfirmation: does survey mode move the Hispanic-white gaps?
GSS 2022 and 2024 are the only rounds where in-person, phone and web coexist, so the
Hispanic-white gap can be estimated separately within web and within interviewer-administered
modes, holding the year fixed."""
import numpy as np, pandas as pd, math
from norms_lib import *
from outcomes import build
from estimate import covariates, wls, contrast

d = load(); d, lab = assign_groups(d); des = Design(d)
Y, L = build(d)
web = d["mode"].eq(4).to_numpy()
mixed_years = d.year.isin([2022, 2024]).to_numpy()
print("2022+2024 mode counts:", pd.Series(d.loc[mixed_years, "mode"]).value_counts().to_dict())
KEY = ["con_index_all13","con_index_gov3","tolscale_core9","tolscale_mslm3","obey_top2",
       "polhitok_yes","cappun_favor","redist","helppoor_r","police_spread","con_within_sd"]
WH = lab["NHWhite G3+"]; HP = lab["Hisp G1"] | lab["Hisp G2"] | lab["Hisp G3+"]
rows = []
for item in KEY:
    y = Y[item].to_numpy(float)
    for arm, m in [("web", mixed_years & web), ("interviewer", mixed_years & ~web)]:
        Z, Zn = covariates(d, True, True)
        fit = wls(d, des, y, (WH | HP) & m, [(g, lab[g]) for g in ["Hisp G1","Hisp G2","Hisp G3+"]], Z, Zn)
        if fit is None: continue
        for g in ["Hisp G1","Hisp G2","Hisp G3+"]:
            r = contrast(fit, {g: 1.0})
            if r: rows.append(dict(item=item, arm=arm, group=g, estimate=r[0], se=r[1], n=fit["n"]))
R = pd.DataFrame(rows); R.to_csv("derived/gss_mode_check.csv", index=False)
R["cell"] = R.apply(lambda r: f"{r.estimate:+.3f} ({r.se:.3f})", axis=1)
pd.set_option("display.width", 220)
print("\nAdjusted Hispanic gap vs NH white G3+, GSS 2022 and 2024 only, by mode:")
print(R.pivot(index="item", columns=["arm","group"], values="cell").reindex(KEY).to_string())
print("\nn per arm:", R.groupby("arm").n.max().to_dict())

# Approximate web-minus-interviewer difference. The two arms are disjoint respondent
# sets, so treating them as independent is an approximation: they share design strata,
# and the stratified estimator induces a small covariance through stratum centring.
P = R.pivot(index=["item","group"], columns="arm", values=["estimate","se"])
D = pd.DataFrame({
    "diff": P[("estimate","web")] - P[("estimate","interviewer")],
    "se_approx": np.sqrt(P[("se","web")]**2 + P[("se","interviewer")]**2)})
D["z"] = D["diff"] / D.se_approx
D.round(3).to_csv("derived/gss_mode_difference.csv")
print("\nweb minus interviewer-administered, approximate z:")
print(D.round(3).sort_values("z", key=abs, ascending=False).head(8).to_string())
