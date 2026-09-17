"""CILS 1991-2006 (ICPSR 20520) tabulations. Read-only on raw/."""
import pandas as pd, numpy as np

RAW = "raw/ICPSR_20520/DS0001/20520-0001-Data.tsv"
D = pd.read_csv(RAW, sep="\t", low_memory=False)

def num(c):
    v = pd.to_numeric(D[c].astype("string").str.strip().replace("", pd.NA), errors="coerce")
    return pd.Series(np.asarray(v, dtype="float64"), index=D.index)

f = pd.DataFrame(index=D.index)
f["caseid"] = num("CASEID")
f["site"] = num("V2").map({1: "Miami", 3: "FtLaud", 4: "SanDiego"})
f["sd"] = num("V2") == 4
f["male"] = num("V18") == 1
f["sex"] = np.where(num("V18") == 1, "men", np.where(num("V18") == 2, "women", None))
f["byear"] = num("V20")

# generation: V21A birth country, 0 = United States
b = num("V21A")
f["gen"] = np.where(b == 0, "2nd", np.where(b.notna(), "1.5", None))

C3LAB = {1: "Cuban", 2: "Mexican", 3: "Nicaraguan", 4: "Colombian", 7: "Dominican",
         8: "Central American", 18: "South American", 21: "Haitian", 22: "Jamaican",
         23: "West Indian", 30: "Filipino", 31: "Vietnamese", 32: "Laotian",
         33: "Cambodian", 34: "Hmong", 38: "Chinese", 45: "Other Asian",
         50: "Middle East/Africa", 60: "Europe/Canada"}
c3 = num("C3")
f["c3"] = c3
f["origin"] = c3.map(C3LAB)

# wave III
f["w3"] = num("V400") == 1
f["arr5"] = num("V448J")     # "I was arrested" (last 5 years)
f["inc5"] = num("V448L")     # "I spent time in reform school/detention/jail/prison" (last 5 years)
f["fam_arr5"] = num("V448I")
f["fam_inc5"] = num("V448K")

v407 = num("V407")
f["v407"] = v407
f["noHS"] = np.where(v407.isin([1]), 1.0, np.where(v407.isin([2, 3, 4, 5, 6, 7, 8, 9]), 0.0, np.nan))
f["BAplus"] = np.where(v407.isin([6, 7, 8, 9]), 1.0, np.where(v407.isin([1, 2, 3, 4, 5]), 0.0, np.nan))
v411 = num("V411")
f["employed"] = np.where(v411.isin([1, 2]), 1.0, np.where(v411.isin([3, 4, 5, 6, 7, 8, 9]), 0.0, np.nan))
f["welfare"] = num("V424")
f["enrolled"] = num("V409")
f["married"] = np.where(num("V402").isin([1]),1.0,np.where(num("V402").notna(),0.0,np.nan))

# wave I parental SES
P56MID = {1: 0, 2: 500, 3: 2000, 4: 4000, 5: 6250, 6: 8750, 7: 12500, 8: 17500,
          9: 22500, 10: 30000, 11: 42500, 12: 62500, 13: 87500, 14: 150000, 15: 250000}
p56 = num("P56")
f["p56"] = p56
f["faminc_w1"] = p56.map(P56MID)
v36, v41 = num("V36"), num("V41")
f["pedu6"] = pd.concat([v36, v41], axis=1).max(axis=1)     # child report, 1-6
f["pedu_str"] = pd.cut(f["pedu6"], [0, 3, 4, 6], labels=["<HS", "HS grad", "Some college+"])
p31, p47 = num("P31"), num("P47")
f["pedu11"] = pd.concat([p31, p47], axis=1).max(axis=1)    # parent report, 0-11
f["ses_w1"] = num("V148")
f["gpa_w1"] = num("V139")
f["gpa_95"] = num("V332")
f["intact"] = np.where(num("V28") == 1, 1.0, np.where(num("V28").notna(), 0.0, np.nan))
f["dropout95"] = num("V337")
# V220: 1 Never, 2 Once or twice, 3 More than twice -> any fight = 1
f["fight_w2"] = np.where(num("V220").isin([2, 3]), 1.0, np.where(num("V220").isin([1]), 0.0, np.nan))

f["inc_str"] = pd.cut(f["faminc_w1"], [-1, 15000, 35000, 1e9],
                      labels=["<$15k", "$15-35k", "$35k+"])

def pct(s):
    s = pd.Series(s).dropna()
    return (len(s), round(100 * s.mean(), 1) if len(s) else np.nan)

def row(sub, label, gen, sex):
    n1 = len(sub)
    w3 = sub[sub["w3"]]
    d = {"origin": label, "generation": gen, "sex": sex, "n_wave1": n1, "n_wave3": len(w3),
         "retention_pct": round(100 * len(w3) / n1, 1) if n1 else np.nan}
    for key, col in [("arrest5", "arr5"), ("incarc5", "inc5"), ("noHS", "noHS"),
                     ("BAplus", "BAplus"), ("employed", "employed"), ("welfare", "welfare"),
                     ("enrolled", "enrolled")]:
        n, p = pct(w3[col])
        d[f"{key}_n"], d[f"{key}_pct"] = n, p
    fi = sub["faminc_w1"].dropna()
    d["faminc_w1_n"] = len(fi)
    d["faminc_w1_median"] = float(fi.median()) if len(fi) else np.nan
    pe = sub["pedu6"].dropna()
    d["paredu_w1_n"] = len(pe)
    d["paredu_w1_mean_1to6"] = round(float(pe.mean()), 2) if len(pe) else np.nan
    d["paredu_w1_ltHS_pct"] = round(100 * float((pe <= 3).mean()), 1) if len(pe) else np.nan
    d["paredu_w1_coll_pct"] = round(100 * float((pe >= 5).mean()), 1) if len(pe) else np.nan
    ses = sub["ses_w1"].dropna()
    d["ses_w1_mean"] = round(float(ses.mean()), 3) if len(ses) else np.nan
    return d

# ---------------- T1 ----------------
COMBOS = {"Lao/Hmong/Cambodian": [32, 33, 34], "Jamaican+West Indian": [22, 23]}
rows = []
origins = [o for o in C3LAB.values() if (f["origin"] == o).sum() >= 60]
for label in origins + list(COMBOS):
    m = f["origin"] == label if label in origins else f["c3"].isin(COMBOS[label])
    for gen in ["1.5", "2nd", "both"]:
        gm = m if gen == "both" else (m & (f["gen"] == gen))
        for sex in ["men", "women", "pooled"]:
            sm = gm if sex == "pooled" else (gm & (f["sex"] == sex))
            sub = f[sm]
            if len(sub) == 0:
                continue
            rows.append(row(sub, label, gen, sex))
for gen in ["1.5", "2nd", "both"]:
    gm = f["gen"].notna() if gen == "both" else (f["gen"] == gen)
    for sex in ["men", "women", "pooled"]:
        sm = gm if sex == "pooled" else (gm & (f["sex"] == sex))
        rows.append(row(f[sm], "POOLED (all origins)", gen, sex))
t1 = pd.DataFrame(rows)
t1.to_csv("t1_origin_by_generation.csv", index=False)

# ---------------- T2 attrition ----------------
AT = [("gpa_w1", "mean"), ("ses_w1", "mean"), ("intact", "pct"), ("gpa_95", "mean"),
      ("dropout95", "pct"), ("fight_w2", "pct"), ("pedu6", "mean"), ("faminc_w1", "mean")]
arows = []
for label in ["POOLED (all origins)"] + origins + list(COMBOS):
    if label == "POOLED (all origins)":
        m = pd.Series(True, index=f.index)
    elif label in origins:
        m = f["origin"] == label
    else:
        m = f["c3"].isin(COMBOS[label])
    sub = f[m]
    d = {"origin": label, "n_wave1": len(sub), "n_wave3": int(sub["w3"].sum()),
         "retention_pct": round(100 * sub["w3"].mean(), 1)}
    for col, kind in AT:
        r, l = sub.loc[sub["w3"], col].dropna(), sub.loc[~sub["w3"], col].dropna()
        mult = 100 if kind == "pct" else 1
        rv = round(mult * float(r.mean()), 2) if len(r) else np.nan
        lv = round(mult * float(l.mean()), 2) if len(l) else np.nan
        d[f"{col}_retained"], d[f"{col}_lost"] = rv, lv
        d[f"{col}_diff"] = round(rv - lv, 2) if (len(r) and len(l)) else np.nan
        if len(r) > 1 and len(l) > 1:
            se = np.sqrt(r.var(ddof=1) / len(r) + l.var(ddof=1) / len(l)) * mult
            d[f"{col}_z"] = round((rv - lv) / se, 2) if se > 0 else np.nan
        else:
            d[f"{col}_z"] = np.nan
    arows.append(d)
pd.DataFrame(arows).to_csv("t2_attrition.csv", index=False)

# ---------------- T3 Rumbaut reconciliation ----------------
v21 = num("V21")
def rum_eth(i):
    c, v = f["c3"].iat[i], v21.iat[i]
    if c == 2: return "Mexican"
    if v in (8, 9): return "Salvadoran, Guatemalan"
    if c in (1, 3, 4, 7, 8, 18): return "Other Latin American"
    if c == 38 and v in (36, 37, 38): return "Chinese"
    if v == 40: return "Korean"
    if c == 30: return "Filipino"
    if c == 31: return "Vietnamese"
    if c in (32, 33, 34): return "Laotian, Cambodian"
    return "All other nationalities"
f["rum_eth"] = [rum_eth(i) for i in range(len(f))]

IIM = {  # from ../iimmla_2026_09_17/t6_rumbaut_reproduction.csv (ages 20-39)
    ("Total sample", "1.5"): (787, 13.7, 7.5),
    ("Total sample", "2nd"): (871, 21.1, 11.8),
    ("Mexican", "1.5"): (138, 22.5, 12.3),
    ("Mexican", "2nd"): (265, 28.7, 20.0),
    ("Salvadoran, Guatemalan", "1.5"): (87, 21.8, 11.5),
    ("Salvadoran, Guatemalan", "2nd"): (96, 35.4, 16.7),
}
BENCH = {  # Rumbaut Table 4, Police Foundation Appendix D pp.132
    ("Total sample", "1.5"): (13.2, 7.8), ("Total sample", "2nd"): (20.7, 12.1),
    ("Mexican", "1.5"): (22.3, 11.9), ("Mexican", "2nd"): (29.8, 20.4),
    ("Salvadoran, Guatemalan", "1.5"): (21.3, 11.2), ("Salvadoran, Guatemalan", "2nd"): (36.7, 17.3),
    ("Other Latin American", "1.5"): (17.4, 15.2), ("Other Latin American", "2nd"): (21.3, 11.5),
    ("Chinese", "1.5"): (5.8, 2.9), ("Chinese", "2nd"): (7.4, 1.9),
    ("Korean", "1.5"): (11.6, 3.9), ("Korean", "2nd"): (18.1, 2.8),
    ("Filipino", "1.5"): (13.3, 8.2), ("Filipino", "2nd"): (9.6, 5.7),
    ("Vietnamese", "1.5"): (8.1, 5.8), ("Vietnamese", "2nd"): (12.7, 9.9),
    ("Laotian, Cambodian", "1.5"): (8.4, 8.4), ("Laotian, Cambodian", "2nd"): (20.0, 20.0),
    ("All other nationalities", "1.5"): (12.3, 7.0), ("All other nationalities", "2nd"): (21.7, 11.9),
}
BENCH_N = {"Total sample": 2971, "Mexican": 787, "Salvadoran, Guatemalan": 187,
           "Other Latin American": 107, "Chinese": 245, "Korean": 201, "Filipino": 475,
           "Vietnamese": 294, "Laotian, Cambodian": 88, "All other nationalities": 200}

men_sd = f[(f["male"]) & (f["w3"]) & (f["sd"])]
men_all = f[(f["male"]) & (f["w3"])]
rrows = []
for eth in ["Total sample"] + sorted(set(f["rum_eth"])):
    for gen in ["1.5", "2nd"]:
        for scope, frame in [("CILS San Diego", men_sd), ("CILS both sites", men_all)]:
            s = frame if eth == "Total sample" else frame[frame["rum_eth"] == eth]
            s = s[s["gen"] == gen]
            na, pa = pct(s["arr5"]); ni, pi = pct(s["inc5"])
            d = {"ethnicity": eth, "generation": gen, "scope": scope,
                 "cils_n_arr": na, "cils_arrest5_pct": pa,
                 "cils_n_inc": ni, "cils_incarc5_pct": pi}
            bm = BENCH.get((eth, gen))
            d["rumbaut_arrested_pct"], d["rumbaut_incarcerated_pct"] = bm if bm else (np.nan, np.nan)
            ii = IIM.get((eth, gen))
            if ii and na:
                n_i, a_i, c_i = ii
                d["iimmla_n"], d["iimmla_arrested_pct"], d["iimmla_incarc_pct"] = n_i, a_i, c_i
                d["merged_n"] = n_i + na
                d["merged_arrested_pct"] = round((n_i * a_i + na * pa) / (n_i + na), 1)
                d["merged_incarc_pct"] = round((n_i * c_i + ni * pi) / (n_i + ni), 1)
                if bm:
                    d["delta_arrest_pts"] = round(d["merged_arrested_pct"] - bm[0], 1)
                    d["delta_incarc_pts"] = round(d["merged_incarc_pct"] - bm[1], 1)
                    d["gate_2pts"] = "PASS" if (abs(d["delta_arrest_pts"]) <= 2 and
                                                abs(d["delta_incarc_pts"]) <= 2) else "FAIL"
            d["rumbaut_table4_n_allgen"] = BENCH_N.get(eth, np.nan)
            rrows.append(d)
pd.DataFrame(rrows).to_csv("t3_rumbaut_reconciliation.csv", index=False)

# ---------------- T4 parental SES strata ----------------
srows = []
def strat_row(sub, grp, stratum, kind, gen):
    d = {"group": grp, "stratum_kind": kind, "stratum": stratum, "generation": gen,
         "n_wave1": len(sub), "n_wave3": int(sub["w3"].sum())}
    w3 = sub[sub["w3"]]
    for key, col in [("arrest5", "arr5"), ("incarc5", "inc5"), ("BAplus", "BAplus"),
                     ("noHS", "noHS")]:
        n, p = pct(w3[col]); d[f"{key}_n"], d[f"{key}_pct"] = n, p
    d["flag_small_cell"] = "YES(<40)" if d["arrest5_n"] < 40 else ""
    return d

for gen in ["2nd", "1.5", "both"]:
    gm = f["gen"].notna() if gen == "both" else (f["gen"] == gen)
    groups = {"Mexican": f["origin"] == "Mexican",
              "All other origins": (f["origin"] != "Mexican") & f["origin"].notna(),
              "Cuban": f["origin"] == "Cuban", "Filipino": f["origin"] == "Filipino",
              "Vietnamese": f["origin"] == "Vietnamese",
              "Lao/Hmong/Cambodian": f["c3"].isin([32, 33, 34]),
              "Nicaraguan": f["origin"] == "Nicaraguan",
              "Haitian+West Indian": f["c3"].isin([21, 22, 23])}
    for grp, gmask in groups.items():
        for kind, col in [("parental education (child report, V36/V41)", "pedu_str"),
                          ("wave-I family income (P56)", "inc_str")]:
            for st in f[col].cat.categories:
                sub = f[gm & gmask & (f[col] == st)]
                if len(sub) == 0:
                    continue
                srows.append(strat_row(sub, grp, str(st), kind, gen))
            sub = f[gm & gmask]
            srows.append(strat_row(sub, grp, "ALL (no stratum)", kind, gen))
pd.DataFrame(srows).to_csv("t4_parental_ses_strata.csv", index=False)

# ---------------- console diagnostics ----------------
print("N", len(f), "| wave3", int(f['w3'].sum()), "| SanDiego", int(f['sd'].sum()))
print("gen counts\n", f["gen"].value_counts(dropna=False))
print("\narr5 by w3:\n", pd.crosstab(f["w3"], f["arr5"].isna()))
print("\nV407 nonnull", f["v407"].notna().sum(), "| V408H nonnull", num("V408H").notna().sum())
print("\nV408H asked by V407:\n", pd.crosstab(f["v407"], num("V408H").notna()))
print("\nmen w3 SD by gen:\n", men_sd.groupby("gen").size())
print("\nmen w3 SD Mexican:\n", men_sd[men_sd["rum_eth"] == "Mexican"].groupby("gen")[["arr5", "inc5"]].agg(["count", "mean"]))
print("\nweight-var scan:", [c for c in D.columns if "W" == c[0] and c[1:].isdigit()][:10])
print("\nP-var coverage: P1 interview done:"); print(num("P1").value_counts(dropna=False))
print("P31 nonnull", f["pedu11"].notna().sum(), "| P56 nonnull", f["p56"].notna().sum(),
      "| V36/V41 max nonnull", f["pedu6"].notna().sum())
print("\nV448J nonnull by V400:"); print(pd.crosstab(f["w3"], f["arr5"].notna()))
print("\nV424 nonnull by V400:"); print(pd.crosstab(f["w3"], f["welfare"].notna()))
print("\nV407 nonnull by V400:"); print(pd.crosstab(f["w3"], f["v407"].notna()))
print("\nV407 dist:"); print(f["v407"].value_counts().sort_index())
print("\nenrolled among w3:", f.loc[f["w3"],"enrolled"].mean())
print("\nage at w3 (byear):"); print(f.loc[f["w3"],"byear"].describe())
print("\nsite x gen (Mexican):"); print(pd.crosstab(f.loc[f["origin"]=="Mexican","site"], f.loc[f["origin"]=="Mexican","gen"]))
print("\nmen w3 by site:"); print(f[f["male"]&f["w3"]].groupby(["site","gen"]).size())
print("\nP56 nonnull by site:"); print(f.groupby("site")["p56"].apply(lambda x: x.notna().mean()))
