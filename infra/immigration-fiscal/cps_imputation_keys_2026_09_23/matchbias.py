"""Step 3: match-bias test. Within cells of basic-CPS match variables, compare the union's
imputed and reported amounts with other residents' reported amounts.

If the hot deck does not match on union membership (or anything that proxies it inside the
cell), the union's imputed mean drifts toward other residents' reported mean: the gap that
the union shows among reporters shrinks among its imputed records (Bollinger and Hirsch 2006).

Cells: sex x age (6) x education (4) x race (white, Black, other) x current labor-force status
(employed, unemployed, retired, disabled, other). Cell weights: the union's imputed weight.
Output: derived/match_bias.csv. SEs: 160 SDR replicates (cells re-weighted per replicate).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c

CELLS = ["sex", "age6", "edu4", "race3", "lf5"]
MIN_N = 2  # unweighted records per cell in each of the three compared groups


def cell_means(v, mask, codes, W, ncell):
    num = np.zeros((ncell, W.shape[1]))
    den = np.zeros((ncell, W.shape[1]))
    np.add.at(num, codes[mask], v[mask, None] * W[mask])
    np.add.at(den, codes[mask], W[mask])
    n = np.bincount(codes[mask], minlength=ncell)
    with np.errstate(invalid="ignore", divide="ignore"):
        return num / den, den, n


def test(v, imputed, reported, union, other, codes, W, ncell):
    ui, uiw, uin = cell_means(v, union & imputed, codes, W, ncell)
    ur, _, urn = cell_means(v, union & reported, codes, W, ncell)
    orr, _, orn = cell_means(v, other & reported, codes, W, ncell)
    oi, oiw, oin = cell_means(v, other & imputed, codes, W, ncell)
    ok = (uin >= MIN_N) & (urn >= MIN_N) & (orn >= MIN_N)
    okd = ok & (oin >= MIN_N)
    om = uiw * ok[:, None]
    omd = uiw * okd[:, None]
    agg = lambda m, x: np.nansum(m * np.nan_to_num(x), 0) / m.sum(0)
    A, B, C = agg(om, ui), agg(om, ur), agg(om, orr)
    Ad, Bd, Cd, Dd = agg(omd, ui), agg(omd, ur), agg(omd, orr), agg(omd, oi)
    coverage = om.sum(0) / uiw.sum(0)
    return dict(union_imputed=A, union_reported=B, other_reported=C,
                gap_reported=B - C, gap_imputed=A - C, retained=(A - C) / (B - C),
                union_imputed_minus_reported=A - B,
                did_union_minus_other=(Ad - Bd) - (Dd - Cd),
                log_gap_reported=np.log(B / C), log_gap_imputed=np.log(A / C),
                log_did_union_minus_other=np.log(Ad / Bd) - np.log(Dd / Cd),
                other_imputed_over_reported=Dd / Cd, coverage=coverage,
                n_cells=np.full(W.shape[1], ok.sum()))


def main():
    d = c.load_frame()
    civ, union = c.masks(d)
    other = civ & ~union
    W = d[c.REPS].to_numpy(float)
    ks, s, mat = c.key_status(d)
    full = d.FL_665.ne(1).to_numpy()
    adult = d.A_AGE.ge(15).to_numpy() & civ
    cv = c.cell_vars(d)
    codes = c.cell_codes(cv, CELLS)
    ncell = codes.max() + 1
    items = {name: (c.item_amount(d, name), s[name]) for name in
             ["wage", "self_employment", "interest", "dividends", "rent", "social_security", "ssi",
              "public_assistance", "unemployment", "veterans", "pensions_retirement"]}
    index = c.spm_index(d)
    fed = d.FEDTAX_BC.to_numpy(float)
    items["federal_liability_shared"] = (c.unit_equal(fed, index), ks["shared"]["federal_liability"])
    items["state_liability_shared"] = (c.unit_equal(d.STATETAX_A.clip(lower=0).to_numpy(float), index),
                                      ks["shared"]["state_liability"])
    items["refundable_credits_shared"] = (c.unit_equal((d.EIT_CRED + d.ACTC_CRD).to_numpy(float), index),
                                         ks["shared"]["refundable_credits"])
    counts = np.bincount(index).astype(float)[index]
    items["spm_resources_per_member"] = (np.maximum(d.SPM_RESOURCES.to_numpy(float) / counts, 0),
                                         ks["shared"]["consumption"])
    items["snap_per_member"] = (d.SPM_SNAPSUB.to_numpy(float) / counts, s["snap"])
    rows = []
    for name, (v, imp) in items.items():
        for variant, imputed in [("all_imputed", imp), ("whole_supplement", imp & full),
                                 ("item_level", imp & ~full)]:
            if variant != "all_imputed" and name.endswith(("_shared", "_member")):
                continue
            reported = ~imp
            res = test(v, imputed & adult, reported & adult, union, other, codes, W, ncell)
            row = dict(item=name, imputed_set=variant)
            for k, rep in res.items():
                row[k] = rep[0]
                if k not in ("n_cells",):
                    row[k + "_se"] = c.sdr(rep)
            rows.append(row)
            print(f"[match] {name:28s} {variant:16s} rep-gap {row['gap_reported']:10.1f} "
                  f"imp-gap {row['gap_imputed']:10.1f} retained {row['retained']:6.2f} "
                  f"log-DiD {row['log_did_union_minus_other']:+.3f} ({row['log_did_union_minus_other_se']:.3f}) "
                  f"coverage {row['coverage']:.2f}", flush=True)
    pd.DataFrame(rows).to_csv(c.OUT / "match_bias.csv", index=False)


if __name__ == "__main__":
    main()
