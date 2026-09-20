#!/usr/bin/env python3
"""Disconfirmation arm -- is the reproduced attrition rate an artefact of imputation?

CPS ASEC allocates parental birthplace and Hispanic origin for non-respondents by
hot deck.  If the hot deck matches on Hispanic origin, a child's imputed grandparent
birthplace would agree with the child's own Hispanic identification by construction,
which would push the measured attrition rate DOWN and could by itself explain why
this lane's third-generation rate is half Duncan and Trejo's.

This script re-runs the third- and second-generation attrition on records where
neither the child's Hispanic origin nor either parent's birthplace fields were
allocated, and reports the rate alongside the all-records rate.

Allocation flags: PXHSPNON (child), PXMNTVTY / PXFNTVTY (the parent's own parents),
PXNATVTY (the parent's birthplace).  Code 00 is "not allocated"; 01/02/03 are
blank / don't know / refused with no change; 10 and above are imputed values.
[SOURCE: 2025 ASEC data dictionary, "Allocation Flags" subtopic]

Inputs : the raw CPS ASEC 2025 zip (read-only)
Outputs: derived/arm3_allocation_check.csv
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
ZIP = (_data_paths.data_root(require_exists=False) / 'external/stage3/census'
       / "cps_asec_2025/asecpub25csv.zip")

MEXICO = 303
US_AREA = (57, 60, 66, 69, 73, 78)
REP_N = 160
COLS = ["PH_SEQ", "A_LINENO", "A_AGE", "PRCITSHP", "PEHSPNON", "PRDTHSP",
        "PENATVTY", "PEMNTVTY", "PEFNTVTY", "PEPAR1", "PEPAR2", "MARSUPWT",
        "PXHSPNON", "PXNATVTY", "PXMNTVTY", "PXFNTVTY"]


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    cache = CACHE / "cps_alloc_flags.parquet"
    if cache.exists():
        d = pd.read_parquet(cache)
    else:
        with zipfile.ZipFile(ZIP) as z, z.open("pppub25.csv") as fh:
            d = pd.read_csv(fh, usecols=COLS, low_memory=False)
        d = d.sort_values(["PH_SEQ", "A_LINENO"], kind="mergesort").reset_index(drop=True)
        d.to_parquet(cache, index=False, compression="zstd")
    n = len(d)
    print(f"records: {n:,}", flush=True)
    for c in ("PXHSPNON", "PXNATVTY", "PXMNTVTY", "PXFNTVTY"):
        vc = d[c].value_counts().sort_index()
        print(f"  {c}: " + " ".join(f"{k}={v:,}" for k, v in vc.items()), flush=True)

    key = d["PH_SEQ"].to_numpy().astype(np.int64)
    line = d["A_LINENO"].to_numpy().astype(np.int64)
    row_of = pd.Series(np.arange(n), index=pd.Index(key * 100 + line))
    par_idx = np.full((n, 2), -1, dtype=np.int64)
    for j, col in enumerate(("PEPAR1", "PEPAR2")):
        ln = d[col].to_numpy().astype(np.int64)
        ok = ln > 0
        looked = row_of.reindex(key[ok] * 100 + ln[ok]).to_numpy()
        par_idx[ok, j] = np.where(np.isnan(looked), -1, np.nan_to_num(looked, nan=-1.0))

    def pattr(arr: np.ndarray, slot: int) -> np.ndarray:
        out = np.full(n, np.nan)
        ok = par_idx[:, slot] >= 0
        out[ok] = arr[par_idx[ok, slot]]
        return out

    pen, pmn, pfn = (d[c].to_numpy() for c in ("PENATVTY", "PEMNTVTY", "PEFNTVTY"))
    hisp = (d["PEHSPNON"] == 1).to_numpy()
    mex_id = hisp & (d["PRDTHSP"] == 1).to_numpy()
    native = d["PRCITSHP"].isin([1, 2, 3]).to_numpy()
    w = d["MARSUPWT"].to_numpy(dtype=float)

    present = par_idx >= 0
    n_par = present.sum(axis=1)
    par_born = np.stack([pattr(pen, 0), pattr(pen, 1)], axis=1)
    gp_mex = np.where(present, (np.stack([pattr(pmn, 0), pattr(pmn, 1)], axis=1) == MEXICO)
                      .astype(float)
                      + (np.stack([pattr(pfn, 0), pattr(pfn, 1)], axis=1) == MEXICO)
                      .astype(float), 0.0).sum(axis=1)
    any_mexborn = np.where(present, par_born == MEXICO, False).any(axis=1)
    all_us = np.where(present, np.isin(par_born, US_AREA), True).all(axis=1) & (n_par > 0)
    child_native = native & ~(pen == MEXICO)
    g2 = child_native & (n_par > 0) & any_mexborn
    g3 = child_native & (n_par > 0) & ~any_mexborn & all_us & (gp_mex > 0)

    # clean = nothing imputed on the child's own ethnicity, or on either linked
    # parent's own birthplace or their parents' birthplaces
    def par_flag_clean(col: str) -> np.ndarray:
        arr = d[col].to_numpy()
        ok = np.ones(n, bool)
        for s in (0, 1):
            v = pattr(arr.astype(float), s)
            ok &= ~((par_idx[:, s] >= 0) & (v >= 10))
        return ok

    child_clean = d["PXHSPNON"].to_numpy() < 10
    par_clean = (par_flag_clean("PXNATVTY") & par_flag_clean("PXMNTVTY")
                 & par_flag_clean("PXFNTVTY"))
    clean = child_clean & par_clean
    print(f"\n  child ethnicity not allocated:      {child_clean.mean()*100:5.1f}%", flush=True)
    print(f"  parent birthplace fields not allocated: {par_clean.mean()*100:5.1f}%",
          flush=True)

    rows = []
    for gname, base in (("2nd generation", g2), ("3rd generation", g3)):
        for aname, sub in (("all records", np.ones(n, bool)),
                           ("child ethnicity not allocated", child_clean),
                           ("parent birthplace not allocated", par_clean),
                           ("neither allocated", clean)):
            m = base & sub
            den = float(w[m].sum())
            num = float(w[m & ~mex_id].sum())
            nh = float(w[m & ~hisp].sum())
            rows.append({"generation": gname, "restriction": aname,
                         "not_mexican_pct": round(100 * num / den, 2) if den else None,
                         "not_hispanic_pct": round(100 * nh / den, 2) if den else None,
                         "weighted_base": round(den, 1),
                         "unweighted_n": int(m.sum())})
            print(f"  {gname:<16} {aname:<34} not-Mexican {100*num/den:6.2f}%  "
                  f"not-Hispanic {100*nh/den:5.2f}%  n={int(m.sum()):,}", flush=True)
    pd.DataFrame(rows).to_csv(DERIVED / "arm3_allocation_check.csv", index=False)
    print("\nwrote derived/arm3_allocation_check.csv", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
