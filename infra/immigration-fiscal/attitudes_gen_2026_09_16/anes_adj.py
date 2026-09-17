"""Adjusted ANES models: net in-group warmth, immigration restriction, guaranteed jobs.
Reuses the loader from anes_gen.py (same variables, weights, generation coding), adds
age, a harmonized 5-band education control and a 2024 year dummy."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf

_g = open("anes_gen.py").read()
src = _g.split("D=pd.concat")[0] + _g.split('def grp(r):')[1].split('D["grp"]')[0].join(["def grp(r):", ""])
SPEC_EXTRA = {2020: dict(age="V201507x", educ="V201510"),
              2024: dict(age="V241458x", educ="V241463")}
exec(src.replace('SPEC={', 'SPEC_BASE={'), globals())
SPEC = {y: {**SPEC_BASE[y], **SPEC_EXTRA[y]} for y in SPEC_BASE}
D = pd.concat([load(2020), load(2024)], ignore_index=True)
D["grp"] = D.apply(grp, axis=1)

# age: -9 refused (2020), -2 missing exact birthdate (2024); 80 = topcode, keep
D["age"] = D.age.where(D.age.between(18, 80))
# education harmonised to 5 bands: 1 <HS, 2 HS grad, 3 some college/associate, 4 BA, 5 graduate
def educ5(r):
    e = r.educ
    if pd.isna(e) or e < 0 or e >= 95: return np.nan
    if r.year == 2020:
        return {1:1, 2:2, 3:3, 4:3, 5:3, 6:4, 7:5, 8:5}.get(int(e), np.nan)
    if e <= 8: return 1
    if e == 9: return 2
    if e <= 12: return 3
    if e == 13: return 4
    return 5
D["educ5"] = D.apply(educ5, axis=1)
D["y24"] = (D.year == 2024).astype(int)
D["cl"] = D.year.astype(str) + "_" + D.st.astype(str) + "_" + D.psu.astype(str)
D["grp"] = pd.Categorical(D.grp, categories=["NHWhite G3+", "Hisp G1", "Hisp G2", "Hisp G3+", "NHWhite G1-2"])

TERMS = ["C(grp)[T.Hisp G1]", "C(grp)[T.Hisp G2]", "C(grp)[T.Hisp G3+]", "C(grp)[T.NHWhite G1-2]"]
rows = []
for col in ["net", "immig_reduce", "guarjob"]:
    base = D[D[col].notna() & D.w.notna() & (D.w > 0) & D.grp.notna()].copy()
    base["yv"] = base[col].astype(float)
    # unadjusted: group dummies only (gate -- must equal differences of pooled means)
    mu = smf.wls("yv ~ C(grp)", data=base, weights=base.w).fit(
        cov_type="cluster", cov_kwds={"groups": base.cl})
    s = base[base.age.notna() & base.educ5.notna()].copy()
    ma = smf.wls("yv ~ C(grp) + age + I(age**2) + C(educ5) + y24", data=s, weights=s.w).fit(
        cov_type="cluster", cov_kwds={"groups": s.cl})
    for t in TERMS:
        rows.append(dict(item=col, group=t.split("T.")[1][:-1],
                         unadj=round(mu.params[t], 4), unadj_se=round(mu.bse[t], 4), n_unadj=int(mu.nobs),
                         adj=round(ma.params[t], 4), adj_se=round(ma.bse[t], 4), n_adj=int(ma.nobs)))
R = pd.DataFrame(rows); R.to_csv("anes_gen_adjusted.csv", index=False)
print(R.to_string(index=False))

# GATE: unadjusted coefficients must equal differences of pooled means in anes_gen_results.csv
g = pd.read_csv("anes_gen_results.csv"); g = g[g["sample"] == "pooled"]
print("\nGATE unadjusted coef vs pooled-mean difference (tolerance 0.1):")
ok = True
for _, r in R.iterrows():
    ref = g[(g.item == r["item"]) & (g.group == "NHWhite G3+")]["mean"].values
    own = g[(g.item == r["item"]) & (g.group == r["group"])]["mean"].values
    if not len(ref) or not len(own): continue
    d = own[0] - ref[0]; gap = abs(d - r["unadj"]); ok &= gap < 0.1
    print(f"  {r['item']:13s} {r['group']:13s} coef={r['unadj']:8.3f} meandiff={d:8.3f} |diff|={gap:.4f}")
print("GATE:", "PASS" if ok else "FAIL")
