import pandas as pd, numpy as np
D = pd.read_csv("raw/ICPSR_20520/DS0001/20520-0001-Data.tsv", sep="\t", low_memory=False)
def num(c):
    v = pd.to_numeric(D[c].astype("string").str.strip().replace("", pd.NA), errors="coerce")
    return pd.Series(np.asarray(v, dtype="float64"), index=D.index)
f = pd.DataFrame(index=D.index)
b = num("V21A"); f["gen"] = np.where(b == 0, "2nd", np.where(b.notna(), "1.5", None))
f["male"] = num("V18") == 1; f["sd"] = num("V2") == 4; f["w3"] = num("V400") == 1
f["arr5"] = num("V448J"); f["inc5"] = num("V448L")
f["famarr"] = num("V448I"); f["faminc"] = num("V448K")
f["mex"] = num("C3") == 2; f["v22"] = num("V22")
f["ganghood"] = np.where(num("P112").isin([2, 3]), 1.0, np.where(num("P112").isin([1]), 0.0, np.nan))
f["ganghood_big"] = np.where(num("P112").isin([3]), 1.0, np.where(num("P112").isin([1, 2]), 0.0, np.nan))
f["gangschool"] = np.where(num("V214").isin([1, 2]), 1.0, np.where(num("V214").isin([3, 4]), 0.0, np.nan))
v36, v41 = num("V36"), num("V41")
f["pedu6"] = pd.concat([v36, v41], axis=1).max(axis=1)
f["pedu_str"] = pd.cut(f["pedu6"], [0, 3, 4, 6], labels=["<HS", "HS grad", "Some college+"])
print("== V22 (US stay length at wave I) among foreign-born ==")
print(f.loc[f["gen"] == "1.5", "v22"].value_counts(dropna=False).sort_index())
m = f[f["male"] & f["w3"] & f["sd"] & f["mex"]]
print("\n== GATE ROBUSTNESS: Mexican men, San Diego, wave III ==")
for lab, sub in [("all 1.5", m[m.gen == "1.5"]),
                 ("1.5 arrived >=5y before W1 (V22 in 1..3)", m[(m.gen == "1.5") & (m.v22 <= 3)]),
                 ("2nd", m[m.gen == "2nd"])]:
    print(f"{lab:45s} n={sub['arr5'].notna().sum():4d} arr={100*sub['arr5'].mean():.1f} "
          f"inc={100*sub['inc5'].mean():.1f}")
print("\n== Family-member arrest / incarceration (last 5y), wave III, by gen ==")
for g in ["1.5", "2nd"]:
    for lab, mask in [("ALL", f["gen"] == g), ("Mexican", (f["gen"] == g) & f["mex"])]:
        s = f[mask & f["w3"]]
        print(f"gen {g:4s} {lab:8s} n={s['famarr'].notna().sum():4d} "
              f"fam_arrested={100*s['famarr'].mean():.1f} fam_jailed={100*s['faminc'].mean():.1f}")
print("\n== Neighbourhood gangs a problem (P112, parent report W1) / gangs at school (V214, W2) ==")
for g in ["1.5", "2nd"]:
    for lab, mask in [("ALL", f["gen"] == g), ("Mexican", (f["gen"] == g) & f["mex"])]:
        s = f[mask]
        print(f"gen {g:4s} {lab:8s} hood_gang={100*s['ganghood'].mean():.1f} (n={s['ganghood'].notna().sum()})"
              f"  hood_gang_BIG={100*s['ganghood_big'].mean():.1f}  school_gang={100*s['gangschool'].mean():.1f} (n={s['gangschool'].notna().sum()})")
print("\n== MEN ONLY: Mexican 2nd vs other-origin 2nd within parental-education strata ==")
w3m = f[f["w3"] & f["male"] & (f["gen"] == "2nd")]
for st in ["<HS", "HS grad", "Some college+"]:
    for lab, mask in [("Mexican", w3m["mex"]), ("Other origins", ~w3m["mex"])]:
        s = w3m[mask & (w3m["pedu_str"] == st)]
        n = s["arr5"].notna().sum()
        print(f"{st:15s} {lab:14s} n={n:4d} arr={100*s['arr5'].mean():.1f} inc={100*s['inc5'].mean():.1f}")
