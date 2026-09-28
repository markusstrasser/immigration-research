"""Connectedness and named population components: Social Capital Atlas measures on Hispanic / Mexican-origin share,
the exposure vs friending-bias decomposition, and the connectedness -> outcome bridge with a
scale (log population) interaction. Cross-sectional OLS, state FE, CR1 SEs clustered by state.

Inputs (all under _cache/ except BEA CAINC4, reused read-only from causal_evidence_2026_09_20):
Atlas county/ZIP files, ACS 5-year 2014-2018 JSON (pull_acs.py), 2020 Gazetteer land area,
Opportunity Atlas county_outcomes_simple.csv. Outputs in derived/. Deterministic; no RNG.
"""
import csv, hashlib, json, math
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
C = LANE / "_cache"
D = LANE / "derived"
BEA = LANE.parent / "causal_evidence_2026_09_20/raw/county_outcomes/raw/bea_cainc4/CAINC4.csv"
INPUTS = [C / "sca/social_capital_county.csv", C / "sca/social_capital_zip.csv", C / "sca/readme.pdf",
          C / "acs/acs5_2018_county.json", C / "acs/acs5_2018_zcta.json",
          C / "gaz/2020_Gaz_counties_national.txt", C / "gaz/2020_Gaz_zcta_national.txt",
          C / "oa/county_outcomes_simple.csv", BEA,
          C / "acs/comp_county.json", C / "acs/comp_zcta.json", C / "acs/manifest_components.json"]
CONTROLS = ["ln_medinc", "pov", "ba_sh", "ln_dens", "black_sh"]


# ---------- statistics (numpy only: no scipy/statsmodels in the shared venv) ----------
def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d if abs(d) > 1e-300 else 1e300
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / d if abs(d) > 1e-300 else 1e300
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / d if abs(d) > 1e-300 else 1e300
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        de = d * c; h *= de
        if abs(de - 1) < 1e-14:
            break
    return h


def _betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1 - math.exp(lbt) * _betacf(b, a, 1 - x) / b


def t_p(t, df):
    return _betainc(df / 2, 0.5, df / (df + t * t))


def t_crit(df, alpha=0.05):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_p(mid, df) > alpha: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def ols(df, y, xs, fe="state", w=None, cluster="state"):
    """Weighted OLS with one absorbed FE (weighted within transform) and CR1 cluster SEs.
    Small-sample factor G/(G-1)*(N-1)/(N-K), K = len(xs): FE nested in clusters (reghdfe rule)."""
    cols = [y] + xs + [fe, cluster] + ([w] if w else [])
    d = df[list(dict.fromkeys(cols))].replace([np.inf, -np.inf], np.nan).dropna()
    if w:
        d = d[d[w] > 0]
    wt = d[w].to_numpy(float) if w else np.ones(len(d))
    Z = d[[y] + xs].to_numpy(float, copy=True)
    g = d[fe].to_numpy()
    codes, inv = np.unique(g, return_inverse=True)
    sw = np.bincount(inv, weights=wt)
    for j in range(Z.shape[1]):
        Z[:, j] -= (np.bincount(inv, weights=wt * Z[:, j]) / sw)[inv]
    yv, X = Z[:, 0], Z[:, 1:]
    XtWX = X.T @ (X * wt[:, None])
    Ainv = np.linalg.inv(XtWX)
    b = Ainv @ (X.T @ (wt * yv))
    u = yv - X @ b
    cl = d[cluster].to_numpy()
    cc, cinv = np.unique(cl, return_inverse=True)
    G, N, K = len(cc), len(d), len(xs)
    S = np.zeros((K, K))
    sc = np.zeros((G, K))
    np.add.at(sc, cinv, X * (wt * u)[:, None])
    S = sc.T @ sc
    V = Ainv @ S @ Ainv * (G / (G - 1)) * ((N - 1) / (N - K))
    se = np.sqrt(np.diag(V))
    return {"b": dict(zip(xs, b)), "se": dict(zip(xs, se)), "N": N, "G": G, "df": G - 1,
            "ymean": float(np.average(d[y], weights=wt)),
            "ysd": float(np.sqrt(np.cov(d[y], aweights=wt)))}


def row(res, x, scale, **meta):
    b, se, df = res["b"][x] * scale, res["se"][x] * scale, res["df"]
    tc = t_crit(df)
    return {**meta, "regressor": x, "coef": b, "se": se, "p": t_p(abs(b / se), df) if se > 0 else float("nan"),
            "ci_lo": b - tc * se, "ci_hi": b + tc * se, "mde80": (tc + 0.8416) * se,
            "N": res["N"], "clusters": res["G"], "y_mean": res["ymean"], "y_sd": res["ysd"],
            "coef_in_y_sd": b / res["ysd"] if res["ysd"] > 0 else float("nan")}


def write(path, rows):
    keys = list(rows[0])
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(keys)
        for r in rows:
            wr.writerow([f"{v:.6g}" if isinstance(v, float) else v for v in (r[k] for k in keys)])


# ---------- build ----------
def acs(name):
    raw = json.loads((C / f"acs/acs5_2018_{name}.json").read_text())
    df = pd.DataFrame(raw[1:], columns=raw[0])
    vars_ = json.loads((C / "acs/manifest.json").read_text())[name]["variables"]
    for k, v in vars_.items():
        x = pd.to_numeric(df[k], errors="coerce")
        df[v] = x.where(x >= 0)  # Census sentinels are large negatives
    return df


def shares(df):
    p = df["pop"]
    df["hisp_sh"] = df.hisp / p
    df["mex_sh"] = df.mexican / p
    df["nonmex_hisp_sh"] = (df.hisp - df.mexican) / p
    df["black_sh"] = df.nh_black / p
    df["white_sh"] = df.nh_white / p
    df["fb_sh"] = df.foreign_born / p
    oth = (1 - df.white_sh - df.black_sh - df.hisp_sh).clip(lower=0)
    # literature-comparison only: the four-group Herfindahl complement the cited papers use
    df["frac"] = 1 - (df.white_sh ** 2 + df.black_sh ** 2 + df.hisp_sh ** 2 + oth ** 2)
    df["ba_sh"] = (df.ed_ba + df.ed_ma + df.ed_prof + df.ed_phd) / df.ed_universe
    df["pov"] = df.pov_below / df.pov_universe
    df["ln_medinc"] = np.log(df.med_hh_income)
    df["ln_pop"] = np.log(p)
    df["ln_dens"] = np.log(p / df.aland_sqmi)
    return df


def components(name, key):
    """Named components: Asian share, limited-English households, Hispanic adults' schooling."""
    raw = json.loads((C / f"acs/{name}.json").read_text())
    df = pd.DataFrame(raw[1:], columns=raw[0])
    vars_ = json.loads((C / "acs/manifest_components.json").read_text())[name]["variables"]
    for k, v in vars_.items():
        x = pd.to_numeric(df[k], errors="coerce")
        df[v] = x.where(x >= 0)
    if key == "fips":
        df["fips"] = df.state + df.county
    else:
        df = df.rename(columns={"zip code tabulation area": "zcta"})
    df["lep_sh"] = (df.hh_lep_spanish + df.hh_lep_indoeuro + df.hh_lep_asian + df.hh_lep_other) / df.hh_total
    df["lep_spanish_sh"] = df.hh_lep_spanish / df.hh_total
    df["hisp_ba_sh"] = (df.hisp_ad_ba_m + df.hisp_ad_ba_f) / df.hisp_ad_universe
    return df[[key, "nh_asian", "lep_sh", "lep_spanish_sh", "hisp_ba_sh", "hisp_ad_universe"]]


def segregation():
    """County Hispanic / NH-white residential segregation from ACS tracts: dissimilarity
    D = 0.5 * sum|h_i/H - w_i/W|, NH-white exposure to Hispanics sum (w_i/W)(h_i/t_i), Hispanic isolation
    sum (h_i/H)(h_i/t_i). Defined for counties with >= 2 populated tracts and H, W > 0."""
    man = json.loads((C / "acs/manifest_components.json").read_text())
    frames = []
    for name in sorted(k for k in man if k.startswith("tract/")):
        raw = json.loads((C / f"acs/{name}.json").read_text())
        frames.append(pd.DataFrame(raw[1:], columns=raw[0]))
    t = pd.concat(frames, ignore_index=True)
    for k, v in man["tract/tract_01"]["variables"].items():
        t[v] = pd.to_numeric(t[k], errors="coerce").clip(lower=0)
    t = t[t["pop"] > 0].copy()
    t["fips"] = t.state + t.county
    g = t.groupby("fips")
    H, W, N = g.hisp.transform("sum"), g.nh_white.transform("sum"), g["pop"].transform("size")
    t["d_term"] = (t.hisp / H - t.nh_white / W).abs()
    t["wexp"] = (t.nh_white / W) * (t.hisp / t["pop"])
    t["hiso"] = (t.hisp / H) * (t.hisp / t["pop"])
    s = t.groupby("fips").agg(n_tracts=("pop", "size"), seg_hisp_n=("hisp", "sum"), d=("d_term", "sum"),
                              wexp=("wexp", "sum"), hiso=("hiso", "sum"), W=("nh_white", "sum"))
    ok = (s.n_tracts >= 2) & (s.seg_hisp_n > 0) & (s.W > 0)
    s["seg_d_hisp_white"] = (0.5 * s.d).where(ok)
    s["seg_white_exposure_hisp"] = s.wexp.where(ok)
    s["seg_hisp_isolation"] = s.hiso.where(ok)
    return s.reset_index()[["fips", "n_tracts", "seg_hisp_n", "seg_d_hisp_white", "seg_white_exposure_hisp",
                            "seg_hisp_isolation"]]


def gaz(fname, key):
    g = pd.read_csv(C / "gaz" / fname, sep="\t", dtype={"GEOID": str})
    g.columns = [c.strip() for c in g.columns]
    return g.rename(columns={"GEOID": key, "ALAND_SQMI": "aland_sqmi"})[[key, "aland_sqmi"]]


def bea_2018():
    b = pd.read_csv(BEA, dtype=str, encoding="latin-1")
    b["fips"] = b.GeoFIPS.str.replace('"', "").str.strip()
    b = b[b.LineCode.str.strip().isin(["20", "30", "35"])]
    b["v"] = pd.to_numeric(b["2018"], errors="coerce")
    p = b.pivot_table(index="fips", columns=b.LineCode.str.strip(), values="v", aggfunc="first")
    out = pd.DataFrame({"fips": p.index, "bea_pop": p["20"].values, "pcpi": p["30"].values,
                        "earn_pow_k": p["35"].values})
    out["ln_pcpi"] = np.log(out.pcpi)
    out["ln_earn_pc"] = np.log(out.earn_pow_k * 1000 / out.bea_pop)
    return out


def build_county():
    s = pd.read_csv(C / "sca/social_capital_county.csv", dtype={"county": str})
    s["fips"] = s.county.str.zfill(5)
    a = acs("county"); a["fips"] = a.state + a.county
    a = a.drop(columns=["state", "county"]).merge(gaz("2020_Gaz_counties_national.txt", "fips"), on="fips", how="left")
    a = shares(a).merge(components("comp_county", "fips"), on="fips", how="left").merge(segregation(), on="fips",
                                                                                         how="left")
    a["asian_sh"] = a.nh_asian / a["pop"]
    oa = pd.read_csv(C / "oa/county_outcomes_simple.csv")
    oa["fips"] = (oa.state * 1000 + oa.county).astype(int).astype(str).str.zfill(5)
    oa = oa[["fips", "kfr_pooled_pooled_p25", "kfr_white_pooled_p25", "kfr_hisp_pooled_p25"]]
    d = s.merge(a, on="fips", how="left").merge(oa, on="fips", how="left").merge(bea_2018(), on="fips", how="left")
    d["state"] = d.fips.str[:2]
    d["ln_medinc_nhw"] = np.log(d.med_hh_income_nhwhite)
    return d


def build_zip():
    s = pd.read_csv(C / "sca/social_capital_zip.csv", dtype={"zip": str, "county": str})
    s["zcta"] = s.zip.str.zfill(5)
    s["cty"] = s.county.str.zfill(5)
    a = acs("zcta").rename(columns={"zip code tabulation area": "zcta"}).drop(columns=["state"])
    a = a.merge(gaz("2020_Gaz_zcta_national.txt", "zcta"), on="zcta", how="left")
    a = shares(a).merge(components("comp_zcta", "zcta"), on="zcta", how="left")
    a["asian_sh"] = a.nh_asian / a["pop"]
    d = s.merge(a, on="zcta", how="left")
    d["state"] = d.cty.str[:2]
    return d


# ---------- tests ----------
COUNTY_Y = ["ec_county", "child_ec_county", "ec_grp_mem_county", "exposure_grp_mem_county",
            "bias_grp_mem_county", "child_exposure_county", "child_bias_county", "ec_high_county",
            "clustering_county", "support_ratio_county", "volunteering_rate_county",
            "civic_organizations_county"]
ZIP_Y = ["ec_zip", "ec_grp_mem_zip", "exposure_grp_mem_zip", "bias_grp_mem_zip", "nbhd_ec_zip",
         "nbhd_exposure_zip", "nbhd_bias_zip", "clustering_zip", "support_ratio_zip",
         "volunteering_rate_zip", "civic_organizations_zip"]
# Named components only. "lit_comparison_fractionalization" is kept solely to compare with the
# index-based literature (Putnam; Alesina-La Ferrara; Alesina-Baqir-Easterly); it is not an explanatory claim.
SHARE_SETS = {"hisp": ["hisp_sh"], "mex_split": ["mex_sh", "nonmex_hisp_sh"], "foreign_born": ["fb_sh"],
              "named_groups": ["hisp_sh", "asian_sh", "fb_sh", "black_sh"],
              "hisp_components": ["hisp_sh", "hisp_ba_sh", "lep_spanish_sh"],
              "hisp_components_segregation": ["hisp_sh", "hisp_ba_sh", "lep_spanish_sh", "seg_d_hisp_white"],
              "hisp_components_white_exposure": ["hisp_sh", "hisp_ba_sh", "lep_spanish_sh",
                                                 "seg_white_exposure_hisp"],
              "lit_comparison_fractionalization": ["frac"]}
UNIT_SCALE = {"seg_d_hisp_white": 0.10, "seg_white_exposure_hisp": 0.10}  # all regressors: per 0.10


def h1(d, ys, level, wvar, fes, sets=None):
    out = []
    for y in ys:
        for sname in sets or SHARE_SETS:
            sx = SHARE_SETS[sname]
            if sname.startswith("hisp_components_") and not level.startswith("county"):
                continue  # tract segregation is built for counties only
            for spec, ctrl in (("fe_only", []), ("controls", CONTROLS)):
                ctrl = [c for c in ctrl if c not in sx]
                for fe in fes:
                    for wname, w in (("unweighted", None), ("weighted_below_p50", wvar)):
                        r = ols(d, y, sx + ctrl, fe=fe, w=w)
                        for x in sx:
                            out.append(row(r, x, 0.10, level=level, outcome=y, share_set=sname, spec=spec,
                                           fe=fe, weight=wname))
    return out


def decomposition(d, level, pairs, wvar, fe="state"):
    """ln(EC_grp) = ln(exposure) + ln(1 - bias) exactly; the Hispanic-share slope splits additively."""
    out = []
    for tag, ec, ex in pairs:
        d = d.copy()
        d["ln_ec"] = np.log(d[ec]); d["ln_exp"] = np.log(d[ex]); d["ln_1mbias"] = d.ln_ec - d.ln_exp
        for wname, w in (("unweighted", None), ("weighted_below_p50", wvar)):
            for spec, ctrl in (("fe_only", []), ("controls", CONTROLS)):
                rs = {k: ols(d, k, ["hisp_sh"] + ctrl, fe=fe, w=w) for k in ("ln_ec", "ln_exp", "ln_1mbias")}
                be = rs["ln_ec"]["b"]["hisp_sh"]
                for k, r in rs.items():
                    rr = row(r, "hisp_sh", 0.10, level=level, pair=tag, component=k, spec=spec, fe=fe, weight=wname)
                    rr["share_of_ln_ec_slope"] = r["b"]["hisp_sh"] / be if be != 0 else float("nan")
                    out.append(rr)
    return out


def bridge(d):
    out = []
    d = d.copy()
    d["ln_pop_c"] = d.ln_pop - d.ln_pop.mean()
    for p in ("ec_county", "child_ec_county", "clustering_county", "support_ratio_county"):
        d[p + "_z"] = (d[p] - d[p].mean()) / d[p].std()
        d[p + "_z_x_lnpop"] = d[p + "_z"] * d.ln_pop_c
    for s in ("hisp_sh", "fb_sh", "frac"):
        d[s + "_x_lnpop"] = d[s] * d.ln_pop_c
    base = ["hisp_sh", "black_sh", "ba_sh", "ln_dens"]
    outcomes = ["kfr_pooled_pooled_p25", "kfr_white_pooled_p25", "ln_pcpi", "ln_earn_pc", "ln_medinc_nhw"]
    for y in outcomes:
        for p in ("ec_county", "child_ec_county", "clustering_county", "support_ratio_county"):
            for spec, extra in (("base", []), ("plus_income_poverty", ["ln_medinc", "pov"])):
                if y.startswith("ln_") and extra:
                    continue  # income on income is circular
                for wname, w in (("unweighted", None), ("weighted_below_p50", "num_below_p50")):
                    xs = [p + "_z", "ln_pop_c"] + base + extra
                    r = ols(d, y, xs, w=w)
                    out.append(row(r, p + "_z", 1.0, test="level", outcome=y, predictor=p, spec=spec, weight=wname))
                    xs2 = [p + "_z", "ln_pop_c", p + "_z_x_lnpop"] + base + extra
                    r2 = ols(d, y, xs2, w=w)
                    for x in (p + "_z", "ln_pop_c", p + "_z_x_lnpop"):
                        out.append(row(r2, x, 1.0, test="scale_interaction", outcome=y, predictor=p, spec=spec,
                                       weight=wname))
        # direct check of the operator's scale claim on named shares: does the ln(pop) slope fall with the
        # Hispanic (or foreign-born) share? Coefficients per 10 points of share per log point of population.
        for s, test in (("hisp_sh", "hisp_share_scale_interaction"), ("fb_sh", "fb_share_scale_interaction"),
                        ("frac", "lit_comparison_frac_scale_interaction")):
            others = [c for c in ["hisp_sh", "black_sh", "ba_sh", "ln_dens"] if c != s and not
                      (s == "frac" and c == "hisp_sh")]
            for wname, w in (("unweighted", None), ("weighted_below_p50", "num_below_p50")):
                xs = [s, "ln_pop_c", s + "_x_lnpop"] + others
                r = ols(d, y, xs, w=w)
                for x in (s, "ln_pop_c", s + "_x_lnpop"):
                    sc = 1.0 if (s == "frac" or x == "ln_pop_c") else 0.10
                    out.append(row(r, x, sc, test=test, outcome=y, predictor=s, spec="base", weight=wname))
    return out


def main():
    D.mkdir(exist_ok=True)
    write(D / "input_hashes.csv", [{"path": str(p.relative_to(LANE.parent)), "bytes": p.stat().st_size,
                                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in INPUTS])
    cty, zp = build_county(), build_zip()
    # gates: joins and the exact decomposition identity
    gates = []
    def gate(name, ok, detail):
        gates.append({"gate": name, "pass": bool(ok), "detail": detail})
    n_ec = cty.ec_county.notna().sum()
    n_ok = (cty.ec_county.notna() & cty.hisp_sh.notna() & cty.ln_dens.notna() & cty.ln_medinc.notna()).sum()
    gate("county_join", n_ok / n_ec > 0.99, f"{n_ok}/{n_ec} Atlas EC counties have ACS + land area")
    zj = (zp.ec_zip.notna() & zp.hisp_sh.notna() & zp.ln_dens.notna()).sum()
    gate("zip_join", zj / zp.ec_zip.notna().sum() > 0.95, f"{zj}/{zp.ec_zip.notna().sum()} Atlas EC ZIPs joined")
    popdiff = (cty["pop"] / cty.pop2018 - 1).abs().median()
    gate("county_pop_matches_atlas", popdiff < 0.01, f"median |ACS pop / Atlas pop2018 - 1| = {popdiff:.4g}")
    m = cty[["ec_grp_mem_county", "exposure_grp_mem_county", "bias_grp_mem_county"]].dropna()
    ident = (m.ec_grp_mem_county / m.exposure_grp_mem_county - (1 - m.bias_grp_mem_county)).abs().max()
    gate("decomposition_identity_county", ident < 1e-3, f"max |ec/exp - (1-bias)| = {ident:.3g}")
    oa_n = cty.kfr_pooled_pooled_p25.notna().sum()
    gate("oa_join", oa_n > 2800, f"{oa_n} counties with Opportunity Atlas kfr_pooled_p25")
    bea_n = cty.ln_pcpi.notna().sum()
    gate("bea_join", bea_n > 2900, f"{bea_n} counties with BEA 2018 per-capita income")
    hs = np.average(cty.hisp_sh.dropna(), weights=cty.loc[cty.hisp_sh.notna(), "pop"])
    gate("hisp_share_national", 0.17 < hs < 0.19, f"pop-weighted county Hispanic share {hs:.4f} (ACS 2018 ~0.18)")
    seg_n = cty.seg_d_hisp_white.notna().sum()
    elig = ((cty.n_tracts >= 2) & (cty.seg_hisp_n > 0)).sum()
    gate("segregation_coverage", seg_n == elig and seg_n > 2800,
         f"{seg_n} of {len(cty)} Atlas counties have tract-based Hispanic/NH-white dissimilarity; "
         f"{elig} have >=2 populated tracts and any Hispanic residents")
    big = cty[cty.seg_hisp_n >= 100000]
    dmed = float(big.seg_d_hisp_white.median())
    gate("segregation_plausible", 0.3 < dmed < 0.65,
         f"median Hispanic/NH-white D in {len(big)} counties with >=100k Hispanics = {dmed:.3f}")
    comp_n = (cty.ec_county.notna() & cty.lep_spanish_sh.notna() & cty.asian_sh.notna()).sum()
    gate("components_join", comp_n / n_ec > 0.99, f"{comp_n}/{n_ec} EC counties have LEP and Asian share")
    write(D / "gates.csv", gates)
    if not all(g["pass"] for g in gates):
        raise SystemExit("[BLOCKED] gate failure: " + "; ".join(g["gate"] for g in gates if not g["pass"]))

    write(D / "h1_county.csv", h1(cty, COUNTY_Y, "county", "num_below_p50", ["state"]))
    write(D / "h1_zip.csv", h1(zp, ZIP_Y, "zip", "num_below_p50", ["state", "cty"]))
    # dissimilarity is noisy where the Hispanic population is small: restricted arm
    seg_r = cty[(cty.seg_hisp_n >= 1000) & (cty.n_tracts >= 5)]
    write(D / "h1_county_seg_restricted.csv",
          h1(seg_r, ["ec_county", "exposure_grp_mem_county", "bias_grp_mem_county", "clustering_county",
                     "support_ratio_county"], "county_seg_restricted", "num_below_p50", ["state"],
             sets=["hisp_components_segregation", "hisp_components_white_exposure"]))
    write(D / "decomposition.csv",
          decomposition(cty, "county", [("adult", "ec_grp_mem_county", "exposure_grp_mem_county"),
                                        ("child", "child_ec_county", "child_exposure_county")], "num_below_p50")
          + decomposition(zp, "zip", [("adult", "ec_grp_mem_zip", "exposure_grp_mem_zip")], "num_below_p50")
          + decomposition(zp, "zip", [("adult", "ec_grp_mem_zip", "exposure_grp_mem_zip")], "num_below_p50", fe="cty"))
    br = bridge(cty)
    write(D / "bridge_county.csv", br)
    # leave-one-state-out for the H1 headline (EC on Hispanic share, controls, both weights)
    loso = []
    for st in sorted(cty.state.dropna().unique()):
        for wname, w in (("unweighted", None), ("weighted_below_p50", "num_below_p50")):
            r = ols(cty[cty.state != st], "ec_county", ["hisp_sh"] + CONTROLS, w=w)
            loso.append(row(r, "hisp_sh", 0.10, dropped_state=st, weight=wname))
    write(D / "h1_loso.csv", loso)
    # pre-stated verdict rules (brief step 4): H1 = EC slope on Hispanic share negative at p<0.05 under both
    # weights with controls; H2 = the EC x ln(pop) interaction positive at p<0.05 for a majority of the
    # connectedness-predictor x outcome cells under both weights (base spec).
    h1c = [r for r in h1(cty, ["ec_county"], "county", "num_below_p50", ["state"], sets=["hisp"])
           if r["share_set"] == "hisp" and r["spec"] == "controls"]
    h1_hold = all(r["coef"] < 0 and r["p"] < 0.05 for r in h1c)
    inter = [r for r in br if r["test"] == "scale_interaction" and r["regressor"].endswith("_x_lnpop")
             and r["spec"] == "base"]
    pos = sum(r["coef"] > 0 and r["p"] < 0.05 for r in inter)
    neg = sum(r["coef"] < 0 and r["p"] < 0.05 for r in inter)
    h2_hold = pos > len(inter) / 2
    write(D / "verdict.csv", [
        {"hypothesis": "H1_ec_lower_with_hispanic_share", "holds": h1_hold,
         "detail": "; ".join(f"{r['weight']}: {r['coef']:.4f} ({r['se']:.4f}) p={r['p']:.3g}" for r in h1c)},
        {"hypothesis": "H2_connectedness_scale_interaction", "holds": h2_hold,
         "detail": f"{len(inter)} interaction cells: {pos} positive p<0.05, {neg} negative p<0.05, "
                   f"{len(inter) - pos - neg} null"},
        {"hypothesis": "step4_sizing", "holds": h1_hold and h2_hold,
         "detail": "sizing run" if h1_hold and h2_hold else "not run: brief says stop if either fails"}])
    desc = []
    for v in ["ec_county", "exposure_grp_mem_county", "bias_grp_mem_county", "clustering_county", "hisp_sh",
              "mex_sh", "asian_sh", "fb_sh", "hisp_ba_sh", "lep_spanish_sh", "seg_d_hisp_white",
              "seg_white_exposure_hisp", "frac", "kfr_pooled_pooled_p25", "kfr_white_pooled_p25", "ln_pcpi", "ln_pop"]:
        x = cty[v].replace([np.inf, -np.inf], np.nan).dropna()
        desc.append({"variable": v, "n": len(x), "mean": float(x.mean()), "sd": float(x.std()),
                     "p10": float(x.quantile(.1)), "p50": float(x.median()), "p90": float(x.quantile(.9))})
    write(D / "descriptives_county.csv", desc)


if __name__ == "__main__":
    main()
