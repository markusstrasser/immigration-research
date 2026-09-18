"""H1 robustness: does the Hispanic-share -> observed-litter association survive
controls for street homelessness, density, land use, and leave-one-group-out?"""
import json, pathlib, collections
import numpy as np, pandas as pd, statsmodels.formula.api as smf
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 260, "display.max_columns", 60)

raw = {r["nbhd"]: r for r in json.load(open(CD/"sf_nbhd_acs.json"))}
geo = pd.read_csv(HERE/"sf_nbhd_geo_context.csv").set_index("nbhd")
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
    grows.append(dict(group=g, pop=pop, hh=hh, area_km2=area,
        homeless_per_km2=homeless/area, pop_per_km2=pop/area,
        mean_hh_inc=sum((s["mean_hh_inc"] or 0)*s["hh"] for s in sub)/hh,
        hisp_pct=w("hisp_pct"), mex_pct=w("mex_pct"), fb_pct=w("fb_pct"),
        nhwhite_pct=w("nhwhite_pct"), nhasian_pct=w("nhasian_pct"),
        nhblack_pct=w("nhblack_pct"), owner_pct=wh("owner_pct"),
        crowded_pct=wh("crowded_pct"), pov_pct=w("pov_pct")))
G = pd.DataFrame(grows).set_index("group")

num = lambda s: pd.to_numeric(ev[s], errors="coerce")
ev["sidewalk_litter"] = num("select_the_statement_that_1")
ev["street_litter"]   = num("select_the_statement_that")
ev["litter_bad"]      = (ev.sidewalk_litter >= 4).astype(int)
ev["dumping_any"]     = (num("how_many_large_abandoned").fillna(0) > 0).astype(int)
ev["graffiti_tot"]    = sum(num(c).fillna(0) for c in
    ["how_many_instances_of_graffiti","how_many_instances_of_graffiti_1",
     "how_many_instances_of_graffiti_2"])
ev["feces"]           = num("how_many_instances_of_feces").fillna(0)
ev["commercial"]      = (num("is_this_route_predominantly") == 1).astype(int)
ev["period"]          = ev["evaluation_period"]
d = ev.dropna(subset=["analysis_neighborhoods"]).join(G, on="analysis_neighborhoods")
d = d.dropna(subset=["mean_hh_inc"])
d["log_inc"] = np.log(d.mean_hh_inc); d["log_dens"] = np.log(d.pop_per_km2)
d["log_homeless"] = np.log1p(d.homeless_per_km2)

OUT = ["sidewalk_litter","street_litter","litter_bad","dumping_any","graffiti_tot","feces"]
SPECS = {
 "A base (inc+landuse+period)": "{y} ~ hisp_pct + log_inc + commercial + C(period)",
 "B + density":                 "{y} ~ hisp_pct + log_inc + commercial + C(period) + log_dens",
 "C + street homelessness":     "{y} ~ hisp_pct + log_inc + commercial + C(period) + log_dens + log_homeless",
 "D + tenure, crowding, black": "{y} ~ hisp_pct + log_inc + commercial + C(period) + log_dens + log_homeless + owner_pct + crowded_pct + nhblack_pct",
 "E + poverty instead of inc":  "{y} ~ hisp_pct + pov_pct + commercial + C(period) + log_dens + log_homeless",
}
print("=== TABLE 8. Hispanic-share coefficient under progressive controls "
      "(route level, cluster-robust by evaluation group) ===")
res = []
for y in OUT:
    for name, f in SPECS.items():
        m = smf.ols(f.format(y=y), data=d).fit(cov_type="cluster",
                cov_kwds={"groups": d.analysis_neighborhoods})
        res.append(dict(outcome=y, spec=name, beta=m.params["hisp_pct"],
            t=m.tvalues["hisp_pct"], p=m.pvalues["hisp_pct"],
            per10pp_sd=10*m.params["hisp_pct"]/d[y].std(),
            homeless_t=m.tvalues.get("log_homeless", np.nan),
            inc_t=m.tvalues.get("log_inc", np.nan), R2=m.rsquared))
R = pd.DataFrame(res); print(R.round(3).to_string(index=False))
R.round(4).to_csv(HERE/"table8_sf_robustness.csv", index=False)

print("\n=== TABLE 9. Leave-one-group-out, spec C, outcome = sidewalk litter ===")
loo = []
for g in d.analysis_neighborhoods.unique():
    dd = d[d.analysis_neighborhoods != g]
    m = smf.ols(SPECS["C + street homelessness"].format(y="sidewalk_litter"),
                data=dd).fit(cov_type="cluster",
                cov_kwds={"groups": dd.analysis_neighborhoods})
    loo.append(dict(dropped=g, beta=m.params["hisp_pct"], t=m.tvalues["hisp_pct"]))
L = pd.DataFrame(loo).sort_values("beta")
print(L.round(4).to_string(index=False))
print(f"\nrange of beta across leave-one-out: {L.beta.min():.4f} to {L.beta.max():.4f}; "
      f"min |t| = {L.t.abs().min():.2f}")
L.round(4).to_csv(HERE/"table9_sf_leave_one_out.csv", index=False)

print("\n=== TABLE 10. Group residuals, spec C, sidewalk litter "
      "(observed minus predicted by income/density/homelessness/land use) ===")
m = smf.ols("sidewalk_litter ~ log_inc + commercial + C(period) + log_dens + log_homeless",
            data=d).fit()
d["resid"] = m.resid
rr = d.groupby("analysis_neighborhoods").agg(n=("resid","size"), resid=("resid","mean"),
        observed=("sidewalk_litter","mean")).join(
        G[["hisp_pct","mex_pct","nhasian_pct","mean_hh_inc","homeless_per_km2","pov_pct"]])
print(rr.sort_values("resid", ascending=False).round(3).to_string())
rr.round(4).to_csv(HERE/"table10_sf_group_residuals.csv")
