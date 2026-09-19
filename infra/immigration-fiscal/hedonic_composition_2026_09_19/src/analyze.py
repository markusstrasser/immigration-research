#!/usr/bin/env python3
"""Main estimation: OLS, gravity IV, shift-share IV, placebo, heterogeneity, metro."""
import json, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estim, prep
from prep import QUAL_D, LEV0, ORIGINS

DERIVED = prep.DERIVED
LATIN = ["mex", "camer", "carib", "samer"]
BETA_MAIN = 1.0


def fit(d, y, focus, controls, weights, fe, instruments=None, extra_endog=None):
    """Demean everything on fe, then WLS or 2SLS. Returns a result row dict."""
    endog = [focus] + (extra_endog or [])
    cols = [y] + endog + controls + (instruments or [])
    sub = d[cols + [weights, fe]].dropna()
    if len(sub) < 200:
        return None
    n = sub.groupby(fe)[y].transform("size")
    sub = sub[n >= 10]
    ngrp = sub[fe].nunique()
    if len(sub) < 200 or ngrp < 5:
        return None
    dm = estim.wdemean(sub, cols, sub[fe], sub[weights])
    clus = sub[fe].str.split("_").str[0]
    if instruments:
        res = estim.tsls(dm[y], dm[endog], dm[controls] if controls else np.empty((len(dm), 0)),
                         dm[instruments], sub[weights], clus, endog, controls,
                         k_absorbed=ngrp)
    else:
        res = estim.wls(dm[y], dm[endog + controls], sub[weights], clus,
                        endog + controls, k_absorbed=ngrp)
    out = estim.row(res, focus)
    out["cbsa_periods"] = ngrp
    return out


def main():
    p = prep.load()
    rows, notes = [], []
    notes.append(f"panel rows (metro, in-CBSA) = {len(p)}")
    notes.append(f"sw_sample cutoff (5-yr FB growth / initial pop) = "
                 f"{p.attrs['sw_cut']:.4f}; selected {p.attrs['sw_n']} of "
                 f"{p.attrs['sw_total']} CBSA-periods (>=76.5% of metro FB growth, "
                 f"the paper's coverage target)")

    for outcome in ["rent", "value"]:
        d = prep.valid(p, outcome)
        notes.append(f"[{outcome}] estimation universe rows={len(d)} "
                     f"cbsa-periods={d.cbsa_period.nunique()} "
                     f"tracts={d.geoid.nunique()}")
        # instruments (computed once per outcome universe)
        for grp, sh in [("fb", "fb_share_0"), ("hisp", "hisp_share_0"),
                        ("mex", "mex_share_0")]:
            d[f"pull_{grp}"] = prep.gravity_pull(d, sh, BETA_MAIN)
            d[f"pull_{grp}_x_lag"] = d[f"pull_{grp}"] * d[sh]
            d[f"pull_{grp}_x_msa"] = d[f"pull_{grp}"] * d["msa_imm_pc"]
        d["pull_fb_b2"] = prep.gravity_pull(d, "fb_share_0", 2.0)
        d["pull_fb_b2_x_lag"] = d["pull_fb_b2"] * d["fb_share_0"]
        d["pull_fb_b2_x_msa"] = d["pull_fb_b2"] * d["msa_imm_pc"]
        bart_fb, g_all, shares = prep.shift_share(d)
        d["bartik_fb"] = bart_fb
        gsub = {o: g_all[o] for o in LATIN}
        d["bartik_hisp"] = sum(shares[o] * gsub[o] for o in LATIN)
        d["bartik_mex"] = shares["mex"] * g_all["mex"]
        notes.append(f"[{outcome}] national origin growth {prep.ORIGINS} -> "
                     + ", ".join(f"{o}:{g_all[o]:+.3f}" for o in ORIGINS))

        zc = prep.standardize(d, QUAL_D + LEV0)
        for c in zc.columns:
            d[c + "_z"] = zc[c]
        C2 = [c + "_z" for c in QUAL_D + LEV0]
        C3 = C2 + [f"log_{outcome}_0"]
        y = f"dlog_{outcome}"

        for samp, mask in [("sw", d["sw_sample"] == 1), ("full", d[y].notna())]:
            ds = d[mask]
            for grp, tv in prep.TREATS.items():
                lag = {"fb": "fb_share_0", "hisp": "hisp_share_0",
                       "mex": "mex_share_0"}[grp]
                specs = [
                    ("ols1_feonly", [], None, None),
                    ("ols2_baseline", C2, None, None),
                    ("ols3_meanrev", C3, None, None),
                    ("iv_gravity_simple", C2, [f"pull_{grp}"], None),
                    ("iv_gravity_full", C2 + [lag, f"pull_{grp}"],
                     [f"pull_{grp}_x_lag", f"pull_{grp}_x_msa"], None),
                    ("iv_shiftshare", C2, [f"bartik_{grp}"], None),
                ]
                if grp == "fb":
                    specs.append(("iv_gravity_full_beta2",
                                  C2 + [lag, "pull_fb_b2"],
                                  ["pull_fb_b2_x_lag", "pull_fb_b2_x_msa"], None))
                for name, ctrl, iv, _ in specs:
                    for per in ["pooled", "A", "B"]:
                        dd = ds if per == "pooled" else ds[ds["period"] == per]
                        r = fit(dd, y, tv, ctrl, "_w", "cbsa_period", iv)
                        if r:
                            r.update(arm=name, outcome=outcome, treat=grp,
                                     sample=samp, period=per)
                            rows.append(r)
        d.to_csv(DERIVED / f"est_universe_{outcome}.csv", index=False,
                 float_format="%.6g")

    res = pd.DataFrame(rows)[
        ["outcome", "treat", "sample", "period", "arm", "coef", "se", "t", "n",
         "clusters", "cbsa_periods", "F_first", "J_p", "r2"]]
    res = res.sort_values(["outcome", "treat", "sample", "period", "arm"])
    res.to_csv(DERIVED / "results_main.csv", index=False, float_format="%.6g")
    (DERIVED / "analyze_notes.txt").write_text("\n".join(notes) + "\n")
    print("\n".join(notes))
    print(f"[main] {len(res)} estimates written")
    hl = res[(res["sample"] == "sw") & (res["period"] == "pooled")
             & (res["treat"].isin(["fb", "hisp"]))]
    print(hl.to_string(index=False))


if __name__ == "__main__":
    main()
