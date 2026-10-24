"""Post-results readings: A's acre-weighted mean (FHFA's concept) and B's CPI counties on house-price indexes."""
import io, json, runpy, sys, urllib.request
import pandas as pd
R = sys.argv[1]
a = runpy.run_path(f"{R}/A_assessor/scripts/build_prices.py", run_name="a")
out = {}
for c, k in (("06037", "la_df"), ("06073", "sd_df"), ("06071", "sb_df")):
    df = a[k]
    out[c] = dict(median=float(df._ppa24.median()), acre_weighted_mean=float((df._ppa24 * df._acres).sum() / df._acres.sum()),
                  mean=float(df._ppa24.mean()), n=len(df))
import os; os.chdir(f"{R}/B_transactions"); b = runpy.run_path(f"{R}/B_transactions/build_prices.py", run_name="b")
pb = pd.read_csv(f"{R}/B_transactions/prices.csv", dtype={"county_fips": str})
def fred(sid):
    t = urllib.request.urlopen(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=60).read().decode()
    s = pd.read_csv(io.StringIO(t)); s.columns = ["d", "v"]; s["y"] = pd.to_datetime(s.d).dt.year
    s = s[pd.to_numeric(s.v, errors="coerce").notna()]; s["v"] = s.v.astype(float)
    return s.groupby("y").v.mean()
for c, alt, hpi in (("06071", "cs_la", "ATNHPIUS40140Q"), ("06085", "cs_sf", "ATNHPIUS41940Q")):
    p = float(pb.loc[pb.county_fips == c, "price_per_acre_2024"].iloc[0])
    cpi_f = b["defl_period"]("cpi", 2005, 2010)
    cs_f = b["defl_period"](alt, 2005, 2010)
    h = fred(hpi); hpi_f = h[2024] / h.loc[2005:2010].mean()
    out[c + "_B"] = dict(cpi=p, case_shiller=p / cpi_f * cs_f, fhfa_house_hpi=p / cpi_f * hpi_f,
                         factors=dict(cpi=cpi_f, case_shiller=cs_f, house_hpi=float(hpi_f)))
print(json.dumps(out, indent=1))
