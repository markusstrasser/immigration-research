"""Second robustness pass: residential-only routes, city cleaning effort as a
control, and a low-income subsample."""
import json, pathlib, collections
import numpy as np, pandas as pd, statsmodels.formula.api as smf
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 250, "display.max_columns", 40)

raw = {r["nbhd"]: r for r in json.load(open(CD/"sf_nbhd_acs.json"))}
geo = pd.read_csv(HERE/"sf_nbhd_geo_context.csv").set_index("nbhd")

# 311 street/sidewalk cleaning volume per km2 per year = city cleaning effort proxy
rows311 = json.load(open(CD/"sf311_nbhd_service_year.json"))
clean = collections.defaultdict(float)
for r in rows311:
    if int(r["yr"]) < 2022: continue
    if r.get("service_name") != "Street and Sidewalk Cleaning": continue
    if r.get("analysis_neighborhood"): clean[r["analysis_neighborhood"]] += int(r["n"])

ev = pd.DataFrame(json.load(open(CD/"sf_street_eval_2022_2025.json")))
groups = sorted(ev["analysis_neighborhoods"].dropna().unique())
g2n = {g: [s.strip() for s in g.split(" - ",1)[1].split(",")] for g in groups}
grows = []
for g, ns in g2n.items():
    sub = [raw[n] for n in ns if n in raw]
    pop = sum(s["pop"] for s in sub); hh = sum(s["hh"] for s in sub)
    area = sum(geo.loc[n,"area_km2"] for n in ns if n in geo.index)
    homeless = sum(geo.loc[n,"tents_struct_veh_per_quarter"] for n in ns if n in geo.index)
    w  = lambda k: sum((s[k] or 0)*s["pop"] for s in sub)/pop
    wh = lambda k: sum((s[k] or 0)*s["hh"] for s in sub)/hh
    grows.append(dict(group=g, pop=pop, area_km2=area,
        homeless_per_km2=homeless/area, pop_per_km2=pop/area,
        clean311_per_km2=sum(clean[n] for n in ns)/4.0/area,
        mean_hh_inc=sum((s["mean_hh_inc"] or 0)*s["hh"] for s in sub)/hh,
        hisp_pct=w("hisp_pct"), mex_pct=w("mex_pct"),
        nhasian_pct=w("nhasian_pct"), nhblack_pct=w("nhblack_pct"),
        owner_pct=wh("owner_pct"), crowded_pct=wh("crowded_pct"), pov_pct=w("pov_pct")))
G = pd.DataFrame(grows).set_index("group")

num = lambda s: pd.to_numeric(ev[s], errors="coerce")
ev["sidewalk_litter"] = num("select_the_statement_that_1")
ev["street_litter"]   = num("select_the_statement_that")
ev["dumping_any"]     = (num("how_many_large_abandoned").fillna(0) > 0).astype(int)
ev["commercial"]      = (num("is_this_route_predominantly") == 1).astype(int)
ev["period"]          = ev["evaluation_period"]
d = (ev.dropna(subset=["analysis_neighborhoods"]).join(G, on="analysis_neighborhoods")
       .dropna(subset=["mean_hh_inc"]))
d["log_inc"] = np.log(d.mean_hh_inc); d["log_dens"] = np.log(d.pop_per_km2)
d["log_homeless"] = np.log1p(d.homeless_per_km2)
d["log_clean"] = np.log1p(d.clean311_per_km2)

BASE = "{y} ~ hisp_pct + log_inc + commercial + C(period) + log_dens + log_homeless"
tests = {
 "all routes, spec C":                 (d, BASE),
 "+ city cleaning effort":             (d, BASE + " + log_clean"),
 "residential routes only":            (d[d.commercial == 0],
                                        "{y} ~ hisp_pct + log_inc + C(period) + log_dens + log_homeless"),
 "commercial routes only":             (d[d.commercial == 1],
                                        "{y} ~ hisp_pct + log_inc + C(period) + log_dens + log_homeless"),
 "below-median-income groups only":    (d[d.mean_hh_inc < d.mean_hh_inc.median()], BASE),
 "above-median-income groups only":    (d[d.mean_hh_inc >= d.mean_hh_inc.median()], BASE),
 "drop Bayview, Tenderloin, SoMa":     (d[~d.analysis_neighborhoods.str.contains(
                                          "Bayview|Tenderloin|South of Market")], BASE),
}
print("=== TABLE 15. Further robustness, outcome = sidewalk litter (1-5) ===")
res = []
for name, (dd, f) in tests.items():
    m = smf.ols(f.format(y="sidewalk_litter"), data=dd).fit(
        cov_type="cluster", cov_kwds={"groups": dd.analysis_neighborhoods})
    res.append(dict(test=name, n=int(m.nobs), groups=dd.analysis_neighborhoods.nunique(),
                    beta=m.params["hisp_pct"], t=m.tvalues["hisp_pct"],
                    p=m.pvalues["hisp_pct"],
                    clean_t=m.tvalues.get("log_clean", np.nan), R2=m.rsquared))
R = pd.DataFrame(res); print(R.round(4).to_string(index=False))
R.round(5).to_csv(HERE/"table15_sf_robustness2.csv", index=False)

print("\n=== TABLE 16. City cleaning effort vs observed litter, by group ===")
t = d.groupby("analysis_neighborhoods").agg(
    sidewalk_litter=("sidewalk_litter","mean"), n=("sidewalk_litter","size")).join(
    G[["clean311_per_km2","homeless_per_km2","hisp_pct","mean_hh_inc","pov_pct"]])
print(t.sort_values("clean311_per_km2", ascending=False).round(1).to_string())
t.round(3).to_csv(HERE/"table16_sf_cleaning_effort.csv")
