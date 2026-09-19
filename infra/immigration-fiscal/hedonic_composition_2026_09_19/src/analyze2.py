#!/usr/bin/env python3
"""Placebo, cross-period (independent-sample) arms, heterogeneity, metro demand."""
import pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estim, prep
from prep import QUAL_D, LEV0

DERIVED = prep.DERIVED
C2 = [c + "_z" for c in QUAL_D + LEV0]


def fitrow(d, y, focus, controls, w, fe, extra=(), cluster=None, min_grp=10,
           min_fe=5, min_n=200):
    cols = [y, focus] + list(extra) + controls
    extra_cols = [c for c in [w, fe, cluster] if c]
    sub = d[cols + extra_cols].dropna()
    n = sub.groupby(fe)[y].transform("size")
    sub = sub[n >= min_grp]
    if len(sub) < min_n or sub[fe].nunique() < min_fe:
        return None
    dm = estim.wdemean(sub, cols, sub[fe], sub[w])
    reg = [focus] + list(extra) + controls
    clus = sub[cluster] if cluster else sub[fe].str.split("_").str[0]
    res = estim.wls(dm[y], dm[reg], sub[w], clus, reg,
                    k_absorbed=sub[fe].nunique())
    out = {k: estim.row(res, k) for k in [focus] + list(extra)}
    flat = {}
    for k, v in out.items():
        for kk, vv in v.items():
            flat[f"{k}__{kk}"] = vv
    flat["n"], flat["cbsa_periods"] = res["n"], sub[fe].nunique()
    return flat


def build_cross(p):
    """Tracts observed in both periods, A and B variables side by side."""
    keep = ["geoid", "cbsa", "dlog_rent", "dlog_value", "d_fb_share", "d_hisp_share",
            "d_mex_share", "own_units_0", "rent_units_0", "log_rent_0", "log_value_0",
            "fb_share_0", "hisp_share_0", "mex_share_0"] + QUAL_D + LEV0
    keep = list(dict.fromkeys(keep))  # LEV0 repeats nhwhite_share_0
    a = p[p.period == "A"][keep].add_suffix("_A").rename(columns={"geoid_A": "geoid",
                                                                 "cbsa_A": "cbsa"})
    b = p[p.period == "B"][keep].add_suffix("_B").rename(columns={"geoid_B": "geoid",
                                                                 "cbsa_B": "cbsa"})
    return a.merge(b, on=["geoid", "cbsa"], how="inner")


def main():
    p = prep.load()
    out_rows = []

    # ---------- placebo and cross-period (independent ACS samples) ----------
    c = build_cross(p)
    for sfx in ["_A", "_B"]:
        z = prep.standardize(c, [x + sfx for x in QUAL_D + LEV0])
        for col in z.columns:
            c[col + "_z"] = z[col]
    for outcome in ["rent", "value"]:
        wcol = "own_units_0_A" if outcome == "value" else "rent_units_0_A"
        c["_w"] = c[wcol]
        c["cbsa_period"] = c["cbsa"] + "_X"
        for grp in ["fb", "hisp", "mex"]:
            CA = [x + "_A_z" for x in QUAL_D + LEV0]
            # PLACEBO: earlier price growth on LATER composition change
            r = fitrow(c, f"dlog_{outcome}_A", f"d_{grp}_share_B", CA, "_w", "cbsa_period")
            if r:
                r.update(arm="placebo_priceA_on_shareB", outcome=outcome, treat=grp,
                         coef=r[f"d_{grp}_share_B__coef"], se=r[f"d_{grp}_share_B__se"],
                         t=r[f"d_{grp}_share_B__t"])
                out_rows.append(r)
            # FORWARD: later price growth on EARLIER composition change
            r = fitrow(c, f"dlog_{outcome}_B", f"d_{grp}_share_A", CA, "_w", "cbsa_period")
            if r:
                r.update(arm="forward_priceB_on_shareA", outcome=outcome, treat=grp,
                         coef=r[f"d_{grp}_share_A__coef"], se=r[f"d_{grp}_share_A__se"],
                         t=r[f"d_{grp}_share_A__t"])
                out_rows.append(r)
            # SAME-PERIOD reference on the identical tract set, both periods
            for per, sfx in [("A", "_A"), ("B", "_B")]:
                CC = [x + sfx + "_z" for x in QUAL_D + LEV0]
                r = fitrow(c, f"dlog_{outcome}{sfx}", f"d_{grp}_share{sfx}", CC,
                           "_w", "cbsa_period")
                if r:
                    r.update(arm=f"same_period_{per}", outcome=outcome, treat=grp,
                             coef=r[f"d_{grp}_share{sfx}__coef"],
                             se=r[f"d_{grp}_share{sfx}__se"],
                             t=r[f"d_{grp}_share{sfx}__t"])
                    out_rows.append(r)
    pl = pd.DataFrame(out_rows)[["outcome", "treat", "arm", "coef", "se", "t", "n",
                                 "cbsa_periods"]]
    pl.sort_values(["outcome", "treat", "arm"]).to_csv(
        DERIVED / "results_placebo_crossperiod.csv", index=False, float_format="%.6g")
    print("[placebo/cross-period]")
    print(pl.sort_values(["outcome", "treat", "arm"]).to_string(index=False))

    # ---------- heterogeneity (Saiz-Wachter Table 2 analogues) -------------
    het = []
    for outcome in ["rent", "value"]:
        d = prep.valid(p, outcome)
        z = prep.standardize(d, QUAL_D + LEV0)
        for col in z.columns:
            d[col + "_z"] = z[col]
        d["val_q"] = (d.groupby("cbsa_period")[f"log_{outcome}_0"]
                      .transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop")))
        y = f"dlog_{outcome}"
        for grp in ["fb", "hisp", "mex"]:
            tv = f"d_{grp}_share"
            sh0 = f"{grp}_share_0"
            d["x_white"] = d[tv] * d["nhwhite_share_0"]
            d["x_valq"] = d[tv] * d["val_q"]
            d["x_lagshare"] = d[tv] * d[sh0]
            for nm, ex in [("x_white_T2col1", ["x_white"]),
                           ("x_valq_T2col2", ["x_valq"]),
                           ("x_lagshare_tipping", ["x_lagshare"])]:
                r = fitrow(d, y, tv, C2, "_w", "cbsa_period", extra=ex)
                if r:
                    r.update(arm=nm, outcome=outcome, treat=grp,
                             main_coef=r[f"{tv}__coef"], main_se=r[f"{tv}__se"],
                             int_coef=r[f"{ex[0]}__coef"], int_se=r[f"{ex[0]}__se"],
                             int_t=r[f"{ex[0]}__t"])
                    het.append(r)
        # supply-response split (realized quantity response, NOT Saiz elasticity)
        g = d.groupby("cbsa_period").agg(hu0=("hh_0", "sum"), hu1=("hh_1", "sum"),
                                         p0=("pop_0", "sum"), p1=("pop_1", "sum"))
        g["supply_proxy"] = (np.log(g.hu1 / g.hu0)) / np.log(g.p1 / g.p0).replace(0, np.nan)
        g["elastic"] = (g.supply_proxy > g.supply_proxy.median()).astype(int)
        d = d.merge(g[["elastic", "supply_proxy"]], left_on="cbsa_period",
                    right_index=True)
        for grp in ["hisp", "mex"]:
            for lab, sel in [("elastic", d.elastic == 1), ("inelastic", d.elastic == 0)]:
                r = fitrow(d[sel], y, f"d_{grp}_share", C2, "_w", "cbsa_period")
                if r:
                    r.update(arm=f"supply_{lab}", outcome=outcome, treat=grp,
                             main_coef=r[f"d_{grp}_share__coef"],
                             main_se=r[f"d_{grp}_share__se"],
                             int_coef=np.nan, int_se=np.nan, int_t=np.nan)
                    het.append(r)
    h = pd.DataFrame(het)[["outcome", "treat", "arm", "main_coef", "main_se",
                           "int_coef", "int_se", "int_t", "n", "cbsa_periods"]]
    h.sort_values(["outcome", "treat", "arm"]).to_csv(
        DERIVED / "results_heterogeneity.csv", index=False, float_format="%.6g")
    print("\n[heterogeneity]")
    print(h.sort_values(["outcome", "treat", "arm"]).to_string(index=False))

    # ---------- metro-level demand effect ----------------------------------
    mrows = []
    for outcome in ["rent", "value"]:
        d = prep.valid(p, outcome)
        d["_num0"] = d[f"med_{outcome}_0"] * d["_w"]
        d["_num1"] = d[f"med_{outcome}_1"] * d["_w"]
        g = d.groupby(["cbsa", "period"]).agg(
            num0=("_num0", "sum"), num1=("_num1", "sum"), wsum=("_w", "sum"),
            fb0=("fb_count_0", "sum"), fb1=("fb_count_1", "sum"),
            h0=("hisp_share_0", "mean"), pop0=("pop_0", "sum"), pop1=("pop_1", "sum"),
            hc0=("hisp_share_0", "size")).reset_index()
        hs = d.assign(hn0=d.hisp_share_0 * d.pop_0, hn1=d.hisp_share_1 * d.pop_1)
        hg = hs.groupby(["cbsa", "period"]).agg(hn0=("hn0", "sum"),
                                                hn1=("hn1", "sum")).reset_index()
        g = g.merge(hg, on=["cbsa", "period"])
        g = g[g.hc0 >= 10].copy()
        g["dlog"] = np.log(g.num1 / g.wsum) - np.log(g.num0 / g.wsum)
        g["imm_pc"] = (g.fb1 - g.fb0) / g.pop0
        g["hisp_pc"] = (g.hn1 - g.hn0) / g.pop0
        g["_w"] = g.pop0
        g["period_fe"] = g["period"]
        for tv in ["imm_pc", "hisp_pc"]:
            for lab, gg in [("pooled", g), ("A", g[g.period == "A"]),
                            ("B", g[g.period == "B"])]:
                r = fitrow(gg, "dlog", tv, [], "_w", "period_fe", cluster="cbsa",
                           min_grp=1, min_fe=1, min_n=30)
                if r:
                    mrows.append({"outcome": outcome, "level": "metro_ACS",
                                  "period": lab, "treat": tv,
                                  "coef": r[f"{tv}__coef"], "se": r[f"{tv}__se"],
                                  "t": r[f"{tv}__t"], "n": r["n"]})
        g.to_csv(DERIVED / f"metro_{outcome}.csv", index=False, float_format="%.6g")
    m = pd.DataFrame(mrows)
    m.to_csv(DERIVED / "results_metro.csv", index=False, float_format="%.6g")
    print("\n[metro demand]")
    print(m.to_string(index=False))


if __name__ == "__main__":
    main()
