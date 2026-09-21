"""Annual fiscal balances by birthplace for high-education origin groups, CPS ASEC 2025.

Question: is there a high-education immigrant group whose resident fiscal balance is not
positive? This lane reuses `education_origin_fiscal_2026_09_19/builder.py` UNCHANGED (same
repaired September 19 account, same CPS replicate and MEPS covariance) and only swaps in other
birthplace codes, read from Appendix J of cpsmar25.pdf. The builder's raw outputs go to the
ignored `_cache/builder/`; this script writes the tracked summary `derived/origin_screen.csv`.

Balances are descriptive annual accounts of current residents aged 25 and over, 2024 prices.
They are not admission effects, exclude institutional costs (N) and average public goods (F),
and transport medical spending by age band and US birth only.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BUILDER = HERE.parent / "education_origin_fiscal_2026_09_19" / "builder.py"
RAW = HERE / "_cache" / "builder"
OUT = HERE / "derived"

# PENATVTY codes, cpsmar25.pdf Appendix J (checked 2026-09-21). Note 217 Korea, 218 Kazakhstan,
# 220 South Korea. `mexico_born` stays because the builder validates its legacy anchor on it.
ORIGINS = {
    "mexico_born": [303],
    "india": [210],
    "china_mainland": [207],
    "taiwan_hong_kong": [209, 240],
    "korea": [217, 220],
    "philippines": [233],
    "japan": [215],
    "iran": [212],
    "pakistan_bangladesh": [231, 202],
    "former_ussr": [155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 218, 246],
    "russia_ukraine_ussr": [163, 164, 165],
    "poland": [128],
    "germany": [110],
    "united_kingdom": [138, 139, 140, 142],
    "canada": [301],
    "nigeria": [440],
    "egypt": [414],
    "venezuela": [373],
    "brazil": [362],
}
ACCOUNT = "expanded_excluding_N"


def load_builder():
    spec = importlib.util.spec_from_file_location("education_origin_builder", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_builder(builder):
    builder.ORIGIN_CODES = ORIGINS
    RAW.mkdir(parents=True, exist_ok=True)
    argv, sys.argv = sys.argv, [str(BUILDER), "--out", str(RAW)]
    try:
        builder.main()
    finally:
        sys.argv = argv
    recorded = json.loads((RAW / "manifest.json").read_text())["origin_codes"]
    if recorded != ORIGINS:
        raise ValueError("Builder did not run with this lane's origin codes")


def pooled(builder, nets, pops, grads, covariance, bands):
    """Per-person balance over a set of age bands, with the builder's own uncertainty."""
    population = pops[bands].sum(axis=0)
    if not (population > 0).all():
        return None
    value = nets[bands].sum(axis=0) / population
    gradient = grads[bands].sum(axis=0) / population[0]
    return builder.summarize(value, gradient, covariance)


def summarise(builder):
    profiles = pd.read_csv(RAW / "profiles.csv")
    support = pd.read_csv(RAW / "support.csv")
    comparisons = pd.read_csv(RAW / "comparisons.csv")
    z = np.load(RAW / "uncertainty.npz")
    nets, pops, grads = z["age_net_replicates"], z["age_population_replicates"], z["age_medical_gradients"]
    covariance, raw_n = z["medical_covariance"], z["raw_n"]
    scopes = {"25_64": slice(0, 4), "65_plus": slice(4, 6), "25_plus": slice(0, 6)}
    rows = []
    use = profiles[(profiles.account == ACCOUNT) & (profiles.entry == "stock")
                   & profiles.education.isin(["all", "ba_plus"])]
    for p in use.itertuples():
        i = p.profile_id
        everyone = profiles[(profiles.account == ACCOUNT) & (profiles.entry == "stock")
                            & (profiles.allocation == p.allocation) & (profiles.origin == p.origin)
                            & (profiles.education == "all")].profile_id.iloc[0]
        ba = profiles[(profiles.account == ACCOUNT) & (profiles.entry == "stock")
                      & (profiles.allocation == p.allocation) & (profiles.origin == p.origin)
                      & (profiles.education == "ba_plus")].profile_id.iloc[0]
        row = dict(origin=p.origin, education=p.education, allocation=p.allocation, account=ACCOUNT,
                   raw_n_25_64=int(raw_n[i, :4].sum()), raw_n_65_plus=int(raw_n[i, 4:].sum()),
                   population_25_plus=float(pops[i, :, 0].sum()),
                   ba_plus_share_25_64=float(pops[ba, :4, 0].sum() / pops[everyone, :4, 0].sum()),
                   share_65_plus_of_adults=float(pops[everyone, 4:, 0].sum() / pops[everyone, :, 0].sum()))
        sparse = support[(support.origin == p.origin) & (support.education == p.education)
                         & (support.entry == "stock")]
        row["unsupported_age_bands"] = int((~sparse.support.astype(bool)).sum())
        for label, bands in scopes.items():
            stats = pooled(builder, nets[i], pops[i], grads[i], covariance, bands)
            for key in ("estimate", "se_joint", "ci95_low", "ci95_high"):
                row[f"net_per_person_{label}_{key}"] = stats[key] if stats else np.nan
        gap = comparisons[(comparisons.profile_id == i) & (comparisons.reference == "all_native")
                          & (comparisons.reference_education == p.education)
                          & (comparisons.metric == "common_age_gap_per_person")]
        if len(gap):
            g = gap.iloc[0]
            row.update(gap_vs_native_same_education_common_age=g.estimate,
                       gap_ci95_low=g.ci95_low, gap_ci95_high=g.ci95_high, gap_standard_mass=g.standard_mass)
        rows.append(row)
    table = pd.DataFrame(rows).sort_values(["allocation", "education", "net_per_person_25_plus_estimate"])
    OUT.mkdir(exist_ok=True)
    table.to_csv(OUT / "origin_screen.csv", index=False, float_format="%.6g")
    return table


def main():
    builder = load_builder()
    if "--summarise-only" not in sys.argv:
        run_builder(builder)
    table = summarise(builder)
    show = table[(table.allocation == "personal") & (table.education == "all")]
    print("\n[personal allocation, all education, stock residents, 2024 dollars per person]")
    for r in show.itertuples():
        print(f"  {r.origin:22} n25-64={r.raw_n_25_64:5d} n65+={r.raw_n_65_plus:4d} BA+={r.ba_plus_share_25_64:5.1%} "
              f"65+share={r.share_65_plus_of_adults:5.1%} | 25-64 {r.net_per_person_25_64_estimate:+9,.0f} "
              f"| 65+ {r.net_per_person_65_plus_estimate:+9,.0f} | 25+ {r.net_per_person_25_plus_estimate:+9,.0f} "
              f"[{r.net_per_person_25_plus_ci95_low:+,.0f}, {r.net_per_person_25_plus_ci95_high:+,.0f}]")


if __name__ == "__main__":
    main()
