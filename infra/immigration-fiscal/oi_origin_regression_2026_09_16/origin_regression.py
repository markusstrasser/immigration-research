"""Regression toward which mean? Second-generation child income rank by parent income ventile and parents'
country of origin, Opportunity Insights race_table6b_nonpar.csv / race_table6a_parametric.csv (children born
1978-83, income measured 2014-15; country of origin = father's, from the 2000 long form / ACS).
Tests the X claim (2026-09-16, @Ne_pas_couvrir) that children of high-scoring immigrant parents regress toward
the mean of their origin population rather than the US mean. Run: uv run --with pandas python3 origin_regression.py
"""
import pandas as pd, numpy as np, pathlib
HERE = pathlib.Path(__file__).resolve().parent
b = pd.read_csv(HERE / "race_table6b_nonpar.csv")
a = pd.read_csv(HERE / "race_table6a_parametric.csv")
usa = b[b.country == "USA"].set_index("par_ventile")
rows = []
for c, g in b.groupby("country"):
    g = g.set_index("par_ventile").reindex(range(1, 21))
    d = {"country": c, "n_M": int(np.nansum(g.n_kir_M)), "n_F": int(np.nansum(g.n_kir_F))}
    for k in ("kir_M", "kir_F", "kfr_P"):
        diff = (g[k] - usa[k]) * 100  # percentile points relative to US-born parents at the same ventile
        d[f"{k}_bottom_v1-4"] = round(np.nanmean(diff.loc[1:4]), 1)
        d[f"{k}_mid_v9-12"] = round(np.nanmean(diff.loc[9:12]), 1)
        d[f"{k}_top_v17-20"] = round(np.nanmean(diff.loc[17:20]), 1)
        ok = g[k].notna()
        x = np.arange(1, 21)[ok.values]; y = g[k].values[ok.values] * 100
        if len(x) >= 8:
            slope, icpt = np.polyfit(x, y, 1)
            d[f"{k}_slope_per_ventile"] = round(slope, 2)
    rows.append(d)
out = pd.DataFrame(rows).sort_values("kir_M_top_v17-20", ascending=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("Child income rank minus US-born-parent child rank at the same parent ventile (percentile points); "
      "kir_M sons, kir_F daughters, kfr_P household.\n")
cols = ["country", "n_M", "kir_M_bottom_v1-4", "kir_M_mid_v9-12", "kir_M_top_v17-20", "kir_M_slope_per_ventile",
        "kir_F_top_v17-20", "kfr_P_bottom_v1-4", "kfr_P_top_v17-20", "kfr_P_slope_per_ventile"]
print(out[cols].to_string(index=False))
us_slope = np.polyfit(np.arange(1, 21), usa.kir_M.values * 100, 1)[0]
print(f"\nUSA sons slope per ventile: {us_slope:.2f}  (rank-rank slope ≈ {us_slope*20/100:.3f})")
# 6a parametric p25/p75 for the same countries
a2 = a[["country", "kir_M_p25", "kir_M_p75", "kir_F_p25", "kir_F_p75", "kfr_P_p25", "kfr_P_p75", "n_kir_M"]].copy()
for k in ("kir_M_p25", "kir_M_p75", "kir_F_p25", "kir_F_p75", "kfr_P_p25", "kfr_P_p75"):
    a2[k] = (a2[k] * 100).round(1)
usa_a = a2[a2.country == "USA"].iloc[0]
a2["sons_p75_minus_USA"] = (a2.kir_M_p75 - usa_a.kir_M_p75).round(1)
a2["sons_p25_minus_USA"] = (a2.kir_M_p25 - usa_a.kir_M_p25).round(1)
print("\nTable 6a parametric: predicted son rank at parent p25 / p75, all countries with n>=1000 sons\n")
print(a2[a2.n_kir_M >= 1000].sort_values("sons_p75_minus_USA", ascending=False).to_string(index=False))
out.to_csv(HERE / "origin_regression_by_ventile.csv", index=False)
a2.to_csv(HERE / "origin_p25_p75.csv", index=False)
