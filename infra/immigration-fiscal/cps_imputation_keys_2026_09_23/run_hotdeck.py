"""Step 4b driver: union-matched hot deck and its pooled-donor control, over several seeds.

For each seed the same procedure runs twice: donors matched on union membership and nativity
(the brief's re-imputation) and donors pooled across groups (a control that shares every other
choice of this lane's hot deck). The union's key shares are recomputed under all 161 weights.
Reported: matched vs published (the brief's comparison), pooled vs published (procedure drift),
and matched minus pooled (the part due to matching on union status and nativity).
Specifications: `main` keeps item-level property, retirement and other income at the Census
values; `all_items` re-imputes them too. Seeds: 20260923 + 0..4 (main), + 0..2 (all_items).
Output: derived/hotdeck_keys.csv, derived/hotdeck_diagnostics.csv, _cache/hotdeck_key_shares.npz
(seed means under `{spec}|{variant}|…`, each seed under `{spec}|{variant}@{seed}|…`).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c
import hotdeck

SPECS = {"main": (False, [20260923 + i for i in range(5)]),
         "all_items": (True, [20260923 + i for i in range(3)])}


def key_shares(frame, W, civ, union, index):
    rk = c.receipt_keys(frame, index)
    sk = c.spending_vectors(frame, index)
    out = {}
    for a in ["personal", "shared"]:
        for k, v in {**c.shares(rk[a], W, civ, union), **c.shares(sk[a], W, civ, union)}.items():
            out[(a, k)] = v
    return out


def main():
    d = c.load_frame()
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    index = c.spm_index(d)
    base = key_shares(d, W, civ, union, index)
    store, rows, diags = {}, [], []
    for (a, k), b in base.items():
        store[f"base|{a}|{k}"] = b
    for spec, (item_property, seeds) in SPECS.items():
        results = {"matched": [], "pooled": []}
        for seed in seeds:
            for variant, cells in [("matched", hotdeck.BASE), ("pooled", [])]:
                print(f"[hotdeck] {spec} seed {seed} {variant}", flush=True)
                new, diag = hotdeck.run(d, seed=seed, verbose=False, base=cells, item_property=item_property)
                diag["spec"], diag["seed"], diag["variant"] = spec, seed, variant
                diags.append(diag)
                results[variant].append(key_shares(new, W, civ, union, index))
                for (a, k), v in results[variant][-1].items():
                    store[f"{spec}|{variant}@{seed}|{a}|{k}"] = v
        for (a, k), b in base.items():
            m = np.mean([r[(a, k)] for r in results["matched"]], axis=0)
            p = np.mean([r[(a, k)] for r in results["pooled"]], axis=0)
            store[f"{spec}|matched|{a}|{k}"] = m
            store[f"{spec}|pooled|{a}|{k}"] = p
            store[f"{spec}|match_effect|{a}|{k}"] = b * m / p
            if np.allclose(m, b) and np.allclose(p, b):
                continue
            sd = lambda xs: float(np.std(xs, ddof=1)) if len(xs) > 1 else np.nan
            rows.append(dict(spec=spec, allocation=a, key=k, share_published=b[0], share_matched=m[0],
                             share_pooled=p[0], rel_matched=m[0] / b[0] - 1, rel_matched_se=c.sdr(m / b - 1),
                             rel_pooled=p[0] / b[0] - 1, rel_pooled_se=c.sdr(p / b - 1),
                             rel_match_effect=m[0] / p[0] - 1, rel_match_effect_se=c.sdr(m / p - 1),
                             seed_sd_matched=sd([r[(a, k)][0] / b[0] for r in results["matched"]]),
                             seed_sd_match_effect=sd([r[(a, k)][0] / q[(a, k)][0] for r, q in
                                                      zip(results["matched"], results["pooled"])]),
                             seeds=len(seeds)))
    np.savez_compressed(c.CACHE / "hotdeck_key_shares.npz", **store)
    pd.concat(diags).to_csv(c.OUT / "hotdeck_diagnostics.csv", index=False)
    out = pd.DataFrame(rows)
    out.to_csv(c.OUT / "hotdeck_keys.csv", index=False)
    print(out.query("spec == 'main'")[["allocation", "key", "rel_matched", "rel_matched_se", "rel_pooled",
                                       "rel_match_effect", "rel_match_effect_se", "seed_sd_matched"]]
          .round(4).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
