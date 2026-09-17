"""IIMMLA 2004 (ICPSR 22627) tabulations by ethnic-origin group and generation.
No survey weight exists in DS0001 -> all estimates UNWEIGHTED (quota sample)."""
import pandas as pd, numpy as np, os

BASE = "/Users/alien/Projects/immigration-research/infra/immigration-fiscal/iimmla_2026_09_17"
OUT = BASE
df = pd.read_csv(os.path.join(BASE, "raw/ICPSR_22627/DS0001/22627-0001-Data.tsv"), sep="\t", low_memory=False)
df.columns = [c.lower() for c in df.columns]
print("rows", len(df), "cols", len(df.columns))
print("gender codes:", df.gender.value_counts().to_dict())
print("generat4 x ethnos10==1:", df.loc[df.ethnos10==1,"generat4"].value_counts().to_dict())

# ---------------- outcome constructions ----------------
def yn(s, yes=1, na=(-9,-8,-7,3,4,9,10)):
    v = s.where(~s.isin(na))
    return (v == yes).astype(float).where(v.notna())

o = pd.DataFrame(index=df.index)
o["arrested"]   = df.evarre.astype(float)                    # 0/1, no missing
o["incarcerated"] = df.evpriso.astype(float)
o["no_hs"]      = (df.educred5 == 0).astype(float)
o["ba_plus"]    = (df.educred5 >= 4).astype(float)
# welfare: asked of a random half-sample (-9 = not applicable / not asked)
o["medicaid"]   = yn(df.q177_c)
o["tanf_ssi"]   = yn(df.q177_e)
o["any_welfare_asked"] = np.where(o.medicaid.notna() | o.tanf_ssi.notna(),
                            ((o.medicaid == 1) | (o.tanf_ssi == 1)).astype(float), np.nan)
# SKIP STRUCTURE (verified in data): q177_c/_e were asked ONLY of households with
# 2003 HH income (q176a) in 1-4 (< $50,000) plus DK/refused. Households at $50k+
# were skipped. The "asked" rates are therefore conditional on a low-income screen
# and NOT comparable across groups. Full-sample versions code the high-income skip
# as non-receipt (assumption; means-tested Medi-Cal/TANF, weaker for SSI/disability).
hi_inc_skip = df.q176a.isin([5,6,7]) & (df.q177_c == -9)
for src, dst in [("medicaid","medicaid_full"),("tanf_ssi","tanf_full"),("any_welfare_asked","any_welfare")]:
    o[dst] = np.where(hi_inc_skip, 0.0, o[src])
    o.loc[~hi_inc_skip & o[src].isna(), dst] = np.nan
# employment: currently working (q2_1), base = asked
emp = df.q2_1.where(df.q2_1 != -9)
o["employed"]   = emp.astype(float)
# homeownership q37: 2=own
h = df.q37.where(~df.q37.isin([6,7]))
o["owns_home"]  = (h == 2).astype(float).where(h.notna())
# personal income q171a 1..8 ordinal
# SKIP STRUCTURE (verified): q171a asked only when >=2 household earners (q175a>=2).
# Sole-earner households: impute from HH income (q176a, same brackets shifted by 1)
# when the respondent IS the earner (q175b==1), else "Nothing" (code 1).
inc = df.q171a.where(df.q171a.between(1,8))
hh = df.q176a.where(df.q176a.between(1,7))
sole = df.q175a == 1
inc = inc.copy()
inc.loc[inc.isna() & sole & (df.q175b == 1)] = hh[inc.isna() & sole & (df.q175b == 1)] + 1
inc.loc[inc.isna() & sole & (df.q175b == 2)] = 1
inc.loc[inc.isna() & (df.q175a == 0)] = 1
MID = {1:0, 2:6000, 3:16000, 4:25000, 5:40000, 6:60000, 7:85000, 8:125000}
o["inc_cat"]    = inc
o["inc_mid"]    = inc.map(MID)
o["inc_ge30k"]  = (inc >= 5).astype(float).where(inc.notna())

# intermarriage: among married/cohabiting with spouse data; pan-ethnic exogamy
sp_hisp = df.q72.where(~df.q72.isin([-9,3,4]))
def spr(v):  # spouse race dummy, -9 -> nan
    return df[v].where(df[v] != -9)
coupled = df.q63.isin([1,2])
resp_pan = df.paneth4
coeth = pd.Series(np.nan, index=df.index)
m = coupled & sp_hisp.notna()
coeth.loc[m & (resp_pan==1)] = (sp_hisp[m & (resp_pan==1)] == 1).astype(float)
# Asian co-ethnic: spouse race Asian/PI OR any specific Asian ancestry named
asian_cols = ["q76_3","q76_4"] + [f"q77_{i}" for i in range(1,14)]
a3 = pd.concat([spr(c) for c in asian_cols], axis=1).max(axis=1)
coeth.loc[m & (resp_pan==2)] = (a3[m & (resp_pan==2)] == 1).astype(float)
w1 = spr("q76_1"); b2 = spr("q76_2")
coeth.loc[m & (resp_pan==3)] = ((w1[m & (resp_pan==3)]==1) & (sp_hisp[m & (resp_pan==3)]==2)).astype(float)
coeth.loc[m & (resp_pan==4)] = ((b2[m & (resp_pan==4)]==1) & (sp_hisp[m & (resp_pan==4)]==2)).astype(float)
o["intermarried"] = 1 - coeth
# Mexican-specific national-origin exogamy: spouse Mexican ancestry (q73 1 or 3)
mexsp = df.q73.where(~df.q73.isin([-9,4,5]))
o["intermar_mex"] = np.where(m & (df.ethnos10==1), (~mexsp.isin([1,3])).astype(float), np.nan)
o.loc[~(m & (df.ethnos10==1)), "intermar_mex"] = np.nan

# parents' education (max of mother/father), 1..6
pm = df.q133a.where(df.q133a.between(1,6))
pf = df.q150a.where(df.q150a.between(1,6))
pmax = pd.concat([pm, pf], axis=1).max(axis=1)
o["pared3"] = pd.cut(pmax, [0,1,3,6], labels=["<HS","HS/voc","SomeColl+"])

# ---------------- group definitions ----------------
E, G, G4 = df.ethnos10, df.generat3, df.generat4
GROUPS = {
 "Mexican 1.5":        (E==1) & (G==1),
 "Mexican 2nd":        (E==1) & (G==2),
 "Mexican 3rd+":       (E==1) & (G==3),
 "SalvGuat 1.5+2nd":   (E==2) & G.isin([1,2]),
 "Chinese 1.5+2nd":    (E==4) & G.isin([1,2]),
 "Korean 1.5+2nd":     (E==5) & G.isin([1,2]),
 "Vietnamese 1.5+2nd": (E==6) & G.isin([1,2]),
 "Filipino 2nd":       (E==7) & (G==2),
 "Filipino 1.5+2nd":   (E==7) & G.isin([1,2]),
 "White NH 3rd+":      (E==9) & (G==3),
 "Black NH 3rd+":      (E==10) & (G==3),
}
RATES = ["arrested","incarcerated","no_hs","ba_plus","medicaid_full","tanf_full","any_welfare","any_welfare_asked",
         "employed","owns_home","inc_ge30k","intermarried"]

def cell(mask, col):
    s = o.loc[mask, col].dropna()
    return len(s), (s.mean() if len(s) else np.nan)

def table(sexlabel, sexmask):
    rows = []
    for gname, gm in GROUPS.items():
        mm = gm & sexmask
        r = {"group": gname, "sex": sexlabel, "n_total": int(mm.sum())}
        for c in RATES:
            n, p = cell(mm, c)
            r[c+"_n"] = n; r[c+"_pct"] = round(100*p,1) if n else np.nan
        inc_s = o.loc[mm,"inc_cat"].dropna()
        r["inc_n"] = len(inc_s)
        r["inc_median_cat"] = inc_s.median() if len(inc_s) else np.nan
        r["inc_median_mid$"] = o.loc[mm,"inc_mid"].dropna().median() if len(inc_s) else np.nan
        rows.append(r)
    return pd.DataFrame(rows)

male = df.gender == 1
female = df.gender == 0  # codebook: 0=Female, 1=Male
t = pd.concat([table("pooled", pd.Series(True, index=df.index)), table("men", male), table("women", female)])
t.to_csv(f"{OUT}/t1_groups_by_sex.csv", index=False)

# ratios to White NH 3rd+ (pooled)
pooled = t[t.sex=="pooled"].set_index("group")
ref = pooled.loc["White NH 3rd+"]
rat = pd.DataFrame({c: (pooled[c+"_pct"]/ref[c+"_pct"]).round(2) for c in RATES})
rat["inc_ratio"] = (pooled["inc_median_mid$"]/ref["inc_median_mid$"]).round(2)
rat.to_csv(f"{OUT}/t2_ratios_vs_white3plus.csv")

# ---------------- Mexican 2nd vs 3rd+, and 3rd+ split by grandparent birthplace ----------------
mex = E==1
sub = {
 "Mexican 2nd":                     mex & (G==2),
 "Mexican 3rd+ (self-ID, all)":     mex & (G==3),
 "Mexican 3rd (>=1 FB grandparent)":mex & (G4==3),
 "Mexican 4th+ (no FB grandparent)":mex & (G4==4),
}
rows = []
for k, mm in sub.items():
    r = {"group": k, "n_total": int(mm.sum())}
    for c in RATES:
        n, p = cell(mm, c); r[c+"_n"] = n; r[c+"_pct"] = round(100*p,1) if n else np.nan
    r["inc_median_mid$"] = o.loc[mm,"inc_mid"].dropna().median()
    r["intermar_mex_n"] = o.loc[mm,"intermar_mex"].dropna().shape[0]
    r["intermar_mex_pct"] = round(100*o.loc[mm,"intermar_mex"].dropna().mean(),1) if o.loc[mm,"intermar_mex"].notna().any() else np.nan
    rows.append(r)
pd.DataFrame(rows).to_csv(f"{OUT}/t3_mexican_generations.csv", index=False)

# ---------------- parental-education strata: Mexican 2nd vs White 3rd+ ----------------
rows = []
for gname in ["Mexican 2nd","Mexican 3rd+","White NH 3rd+"]:
    gm = GROUPS[gname]
    for lev in ["<HS","HS/voc","SomeColl+"]:
        mm = gm & (o.pared3 == lev)
        r = {"group": gname, "parent_educ": lev, "n": int(mm.sum())}
        for c in ["arrested","incarcerated","ba_plus","no_hs","any_welfare","employed"]:
            n, p = cell(mm, c); r[c+"_n"] = n; r[c+"_pct"] = round(100*p,1) if n else np.nan
        rows.append(r)
pd.DataFrame(rows).to_csv(f"{OUT}/t4_parental_education_strata.csv", index=False)

# diagnostics: who is missing on welfare / income
diag = pd.DataFrame({
  "welfare_asked_pct": df.groupby("ethnos10").apply(lambda g: 100*o.loc[g.index,"any_welfare"].notna().mean()),
  "income_asked_pct":  df.groupby("ethnos10").apply(lambda g: 100*o.loc[g.index,"inc_cat"].notna().mean()),
})
diag.to_csv(f"{OUT}/t5_item_coverage_by_ethnos10.csv")
print("written")
