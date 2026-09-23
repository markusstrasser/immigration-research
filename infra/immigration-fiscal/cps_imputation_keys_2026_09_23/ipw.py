"""Step 4a: drop imputed items and reweight reported records by inverse probability.

For every CPS key and allocation convention, records whose key value is imputed get weight 0;
reported records in cell c get weight w * W_c / W_c(reported), recomputed under each of the 161
weights. Main cells (brief): age x sex x education x nativity x union. A cell without reported
records collapses to the next row of COLLAPSE. Variant cells add current labor-force status.
Derived keys (Census tax model, SPM resources) use the material-imputation rule of
common.material_status at 5% (main), 1% and any-flag (sensitivities).
Output: _cache/ipw_key_shares.npz (replicate shares, read by translate.py) and derived/ipw_keys.csv.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c

SPECS = {
    "a_brief_cells": [["age9", "sex", "edu5", "foreign_born", "union"],
                      ["age6", "sex", "edu4", "foreign_born", "union"],
                      ["age3", "sex", "foreign_born", "union"], ["foreign_born", "union"], ["union"]],
    "a_plus_labor_force": [["age9", "sex", "edu5", "foreign_born", "union", "lf5"],
                           ["age9", "sex", "edu5", "foreign_born", "union"],
                           ["age6", "sex", "edu4", "foreign_born", "union"],
                           ["age3", "sex", "foreign_born", "union"], ["foreign_born", "union"], ["union"]],
}
THRESHOLDS = {"material_5pct": 0.05, "material_1pct": 0.01, "any_flag": None}


def ipw_weights(W, reported, civ, frames):
    """Adjusted 161-column weights; each person's cell is the finest level with reported weight."""
    n = len(W)
    assigned = np.full(n, -1)
    level_codes = []
    for level, columns in enumerate(frames):
        codes = c.cell_codes(frames[level], list(frames[level].columns))
        ncell = codes.max() + 1
        rep_w = np.zeros((ncell, W.shape[1]))
        np.add.at(rep_w, codes[civ & reported], W[civ & reported])
        good = (rep_w > 0).all(axis=1)
        take = civ & (assigned < 0) & good[codes]
        assigned[take] = level * 10**7 + codes[take]
        level_codes.append(codes)
    if (assigned[civ] < 0).any():
        raise ValueError("A cell has no reported records at any collapse level")
    key = pd.factorize(assigned)[0]
    ncell = key.max() + 1
    tot = np.zeros((ncell, W.shape[1]))
    rep = np.zeros((ncell, W.shape[1]))
    np.add.at(tot, key[civ], W[civ])
    np.add.at(rep, key[civ & reported], W[civ & reported])
    factor = np.divide(tot, rep, out=np.zeros_like(tot), where=rep > 0)
    out = np.zeros_like(W)
    m = civ & reported
    out[m] = W[m] * factor[key[m]]
    levels_used = np.bincount((assigned[civ] // 10**7).astype(int), minlength=len(frames))
    return out, levels_used


def main():
    d = c.load_frame()
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    index = c.spm_index(d)
    cv = c.cell_vars(d)
    cv["union"] = union.astype(int)
    rvec = c.receipt_keys(d, index)
    svec = c.spending_vectors(d, index)
    base = {}
    for a in ["personal", "shared"]:
        base[a] = {**c.shares(rvec[a], W, civ, union), **c.shares(svec[a], W, civ, union)}
    rows, store = [], {}
    for tname, thr in THRESHOLDS.items():
        status, _, _ = c.key_status(d, thr)
        for spec, levels in SPECS.items():
            if tname != "material_5pct" and spec != "a_brief_cells":
                continue
            frames = [cv[cols] for cols in levels]
            cache = {}
            for a in ["personal", "shared"]:
                vectors = {**rvec[a], **svec[a]}
                for key, v in vectors.items():
                    if key in c.UNAFFECTED or key not in status[a]:
                        continue
                    derived = key in c.TAX_KEYS or key in ("consumption", "resources")
                    if tname != "material_5pct" and not derived:
                        continue
                    imputed = status[a][key]
                    sig = (a, imputed.tobytes().__hash__())
                    if sig not in cache:
                        cache[sig] = ipw_weights(W, ~imputed, civ, frames)
                    Wa, levels_used = cache[sig]
                    share = (v[union] @ Wa[union]) / (v[civ] @ Wa[civ])
                    delta = share - base[a][key]
                    label = f"{spec}|{tname}"
                    store[f"{label}|{a}|{key}"] = share
                    rows.append(dict(spec=spec, derived_rule=tname, allocation=a, key=key,
                                     share_published=base[a][key][0], share_ipw=share[0],
                                     delta_share=delta[0], delta_share_se=c.sdr(delta),
                                     relative_change=share[0] / base[a][key][0] - 1,
                                     relative_change_se=c.sdr(share / base[a][key] - 1),
                                     imputed_weight_share=float(W[civ & imputed, 0].sum() / W[civ, 0].sum()),
                                     cells_collapsed=int(levels_used[1:].sum())))
                    print(f"[ipw] {spec:20s} {tname:14s} {a:8s} {key:22s} "
                          f"{base[a][key][0]:.5f} -> {share[0]:.5f} ({rows[-1]['relative_change']:+.2%} "
                          f"± {rows[-1]['relative_change_se']:.2%})", flush=True)
    for a in ["personal", "shared"]:
        for k, v in base[a].items():
            store[f"base|{a}|{k}"] = v
    np.savez_compressed(c.CACHE / "ipw_key_shares.npz", **store)
    pd.DataFrame(rows).to_csv(c.OUT / "ipw_keys.csv", index=False)


if __name__ == "__main__":
    main()
