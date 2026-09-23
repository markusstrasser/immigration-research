"""Step 5b: how the imputation correction changes the income-distribution lane's inputs.

distribution_weights_2026_09_23 divides the adopted fiscal cost (A_mid + F_c = -$227.9bn) among
other residents. Its central tax-share key ("fiscal_a") takes CBO federal shares and ITEP
state-local rates by all-resident percentile group (ranked by SPM resources per equivalence
scale) and spreads each group's share by per-capita household money income. Its check key uses
the CPS tax fields (FEDTAX_AC + 2 x FICA + STATETAX_A per capita in the household). CPS
imputation reaches these inputs three ways: the fiscal total, the ranking, and the within-group
spread. This script imports the lane's own functions (read only; nothing is written there),
reproduces its published quintile splits (gate), then:

1. re-ranks and re-spreads on the union-matched hot-deck microdata (and on the pooled-donor
   control) at the published total, 5 seeds each (main specification of run_hotdeck.py);
2. moves the total by each method's change to the adopted main case
   (derived/main_case_translation.csv, midpoint of the low and high changes).

Output: derived/distribution_check.csv.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/cps_imputation_keys_2026_09_23/distribution_check.py
"""
from __future__ import annotations

import importlib.util
import sys

import numpy as np
import pandas as pd

import common as c
import hotdeck

sys.dont_write_bytecode = True
DIST_DIR = c.FISCAL / "distribution_weights_2026_09_23"
SEEDS = [20260923 + i for i in range(5)]
MONEY = [col for b in hotdeck.BLOCKS.values() for col in b if col != "CAP_VAL"]  # money income excludes capital gains
METHODS = ["a_ipw_brief_cells", "b_hotdeck_union_matched", "b_matched_over_pooled"]


def load_dist():
    spec = importlib.util.spec_from_file_location("distribute", DIST_DIR / "distribute.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def split(dist, dd, total, F, S):
    R = dist.rank_frame(dd, "spm")
    tax, _ = dist.tax_key(dd, R, "after", F, S)
    pw = dd.pw.to_numpy()
    q = R["q5"]
    out = {}
    for name, key in [("fiscal_a", tax), ("fiscal_a_cps_tax_fields", np.maximum(dd.cps_tax_pc.to_numpy(float), 0))]:
        amount = dist.per_person(dd, key, total) * pw / 1e9
        out[name] = np.array([amount[q == k].sum() for k in range(5)])
    return out


def with_hotdeck(dd, d, new):
    """The distribution frame with the re-imputed incomes, taxes and SPM resources."""
    change = pd.DataFrame({"PH_SEQ": d.PH_SEQ.to_numpy(), "PPPOS": d.PPPOS.to_numpy(),
                           "SPM_RESOURCES": new.SPM_RESOURCES.to_numpy(float),
                           "d_fedac": ((new.FEDTAX_BC - new.EIT_CRED - new.ACTC_CRD)
                                       - (d.FEDTAX_BC - d.EIT_CRED - d.ACTC_CRD)).to_numpy(float),
                           "FICA": new.FICA.to_numpy(float), "STATETAX_A": new.STATETAX_A.to_numpy(float),
                           "d_money": (new[MONEY].sum(axis=1) - d[MONEY].sum(axis=1)).to_numpy(float)})
    out = dd.drop(columns=["SPM_RESOURCES", "FICA", "STATETAX_A"]).merge(
        change, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if out.SPM_RESOURCES.isna().any() or len(out) != len(dd):
        raise SystemExit("[BLOCKED] hot-deck frame does not align with the distribution frame")
    out["FEDTAX_AC"] = out.FEDTAX_AC + out.d_fedac
    out["HTOTVAL"] = out.HTOTVAL + out.groupby("PH_SEQ").d_money.transform("sum")
    out["y_spm"] = out.SPM_RESOURCES / out.SPM_EQUIVSCALE
    out["money_pc"] = out.HTOTVAL / out.H_NUMPER
    cps_tax = (out.FEDTAX_AC + 2 * out.FICA + out.STATETAX_A).groupby(out.PH_SEQ).transform("sum")
    out["cps_tax_pc"] = cps_tax / out.H_NUMPER
    return out


def main():
    dist = load_dist()
    dd = dist.load_cps()
    F, S = dist.bea_totals()
    pub = pd.read_csv(DIST_DIR / "derived/channel_by_quintile.csv").query("measure == 'spm'")
    pub = {ch: g.set_index("quintile").bn for ch, g in pub.groupby("channel")}
    total = float(pub["fiscal_a"].loc[0])
    base = split(dist, dd, total, F, S)
    worst = max(np.abs(base[ch] - pub[ch].loc[[1, 2, 3, 4, 5]].to_numpy()).max() for ch in base)
    print(f"[dist] published quintile splits reproduced, max difference {worst:.2e} bn (total {total:.3f})", flush=True)
    if worst > 1e-6:
        raise SystemExit("[BLOCKED] distribution lane's quintile split not reproduced")

    d = c.load_frame()
    runs = {"matched": [], "pooled": []}
    for seed in SEEDS:
        for variant, cells in [("matched", hotdeck.BASE), ("pooled", [])]:
            print(f"[dist] hot deck seed {seed} {variant}", flush=True)
            new, _ = hotdeck.run(d, seed=seed, verbose=False, base=cells)
            runs[variant].append(split(dist, with_hotdeck(dd, d, new), total, F, S))

    trans = pd.read_csv(c.OUT / "main_case_translation.csv").query("profile == 'cbo_category_lag_non_school_full'")
    trans = trans.set_index("method")
    rows = []
    for ch in base:
        pub_share = base[ch] / total
        mean = {v: np.mean([r[ch] for r in runs[v]], axis=0) for v in runs}
        sd = {v: np.std([r[ch] for r in runs[v]], axis=0, ddof=1) for v in runs}
        for k in range(5):
            row = dict(channel=ch, quintile=k + 1, published_bn=float(pub[ch].loc[k + 1]), reproduced_bn=base[ch][k],
                       published_share=pub_share[k],
                       rerank_matched_bn=mean["matched"][k], rerank_matched_seed_sd_bn=sd["matched"][k],
                       rerank_pooled_bn=mean["pooled"][k], rerank_pooled_seed_sd_bn=sd["pooled"][k],
                       rerank_match_effect_bn=mean["matched"][k] - mean["pooled"][k])
            for m in METHODS:
                dtot = -(trans.loc[m, "change_low_bn"] + trans.loc[m, "change_high_bn"]) / 2
                row[f"total_{m}_bn"] = total + dtot
                row[f"with_{m}_bn"] = base[ch][k] + dtot * pub_share[k]
            rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(c.OUT / "distribution_check.csv", index=False)
    show = ["channel", "quintile", "published_bn", "published_share", "rerank_matched_bn", "rerank_pooled_bn",
            "rerank_match_effect_bn"] + [f"with_{m}_bn" for m in METHODS]
    print(out[show].round(3).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
