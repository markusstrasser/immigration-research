#!/usr/bin/env python3
"""Put Indian G3+ (race/ID) on the same 2025 extended ledger as indian_ledger_2026_09_18.

Adds one group to the imported masks: US-born, both parents US-area-born, PRDASIAN=1.
Does not edit the 2026-09-18 lane. Same allocation, weights, MEPS health, age-std.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 ledger_g3.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INFRA = HERE.parent
sys.path.insert(0, str(INFRA / "indian_ledger_2026_09_18"))
sys.path.insert(0, str(INFRA / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(INFRA / "build"))

import analyze_cps_fiscal_2025 as base  # noqa: E402
import extend_ledger as ext  # noqa: E402
import ledger_india as li  # noqa: E402

G3 = "india_g3plus_race"
KEEP = [
    "third_plus_nh_white", "india_born", "india_second_gen",
    "asian_indian_native_selfid", G3,
]
METRICS = [
    "modeled_tax_total", "selected_cash_total", "selected_noncash_total",
    "cash_noncash_tax_balance", "k12_charged", "extended_balance_base",
    "health_age_birth", "extended_balance_after_health", "children_5_17",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cps-zip", type=Path, default=None)
    ap.add_argument("--meps-zip", type=Path, default=li._data_paths.data_root(require_exists=False)
                    / "external/stage3/ahrq/meps_2024/h256dat.zip")
    ap.add_argument("--meps-sas", type=Path, default=li._data_paths.data_root(require_exists=False)
                    / "external/stage3/ahrq/meps_2024/h256su.txt")
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    cps = li.resolve_cps(args.cps_zip)
    print(f"[1] CPS {cps.name}", flush=True)
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    groups = li.build_groups(d)
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(li.US_AREA) & d.PEMNTVTY.isin(li.US_AREA)
    groups[G3] = (native & parents_us & d.PRDASIAN.eq(1)).to_numpy()

    print("[2] MEPS", flush=True)
    health = li.health_person_means(d, args.meps_zip, args.meps_sas)
    age = d.A_AGE.to_numpy()
    civ = d.PRPERTYP.eq(2).to_numpy()
    adults = civ & (age >= 25) & (age <= 64)
    w0 = d.MARSUPWT.to_numpy(float)
    weights = d[base.REPS].to_numpy()
    ref_use = adults & groups[li.REFERENCE]
    shares = np.array([w0[ref_use & (age >= lo) & (age <= hi)].sum() for lo, hi in li.BANDS_25_64])
    std_share = shares / shares.sum()

    print("[3] estimate", flush=True)
    rows = []
    for allocation in ("equal_all_members", "equal_adults_18plus"):
        per = li.per_person_metrics(state, allocation, health)
        arms = (("raw", False), ("age_standardised", True)) if allocation == "equal_all_members" else (("raw", False),)
        for arm, std in arms:
            if std:
                ref = li.age_standardised_replicates(per, METRICS, ref_use, weights, age, std_share)
            else:
                ref = li.group_replicates(per, METRICS, ref_use, weights)
            for g in KEEP:
                use = adults & groups[g]
                n = int(use.sum())
                if n == 0:
                    continue
                if std:
                    reps = li.age_standardised_replicates(per, METRICS, use, weights, age, std_share)
                    if reps is None:
                        print(f"  skip age-std {g}: empty band", flush=True)
                        continue
                else:
                    reps = li.group_replicates(per, METRICS, use, weights)
                for m in METRICS:
                    est, se = li.sdr(reps[m])
                    dest, dse = li.sdr(reps[m] - ref[m])
                    rows.append({"allocation": allocation, "arm": arm, "group": g, "metric": m,
                                 "n_unweighted": n, "weighted_persons": float(weights[use, 0].sum()),
                                 "estimate": est, "se_sdr": se,
                                 "diff_vs_white": dest, "se_sdr_diff": dse})
                    if m == "extended_balance_after_health":
                        print(f"  {allocation:20} {arm:18} {g:28} n={n:5d}  {est:9,.0f}  "
                              f"gap {dest:+,.0f} ({dse:,.0f})", flush=True)
    pd.DataFrame(rows).to_csv(args.out / "india_g3_ledger.csv", index=False, float_format="%.6f")
    print(f"wrote {args.out / 'india_g3_ledger.csv'}", flush=True)


if __name__ == "__main__":
    main()
