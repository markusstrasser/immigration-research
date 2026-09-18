"""Lifetime (period-profile) balances by group, including the white and all-native
references, and the fiscal budget equivalent to one additional reference-profile child.

Reuses the all-age lane's estimator for the `all_age_shared` scenario, full weight only.
Outputs derived/age_profiles_references.csv and derived/lifetime_equivalence.csv.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "all_age_ledger_2026_09_17"
sys.path.insert(0, str(LANE))
import analyze as A  # noqa: E402

BANDS = {0: (0, 18), 1: (18, 25), 2: (25, 35), 3: (35, 45), 4: (45, 55), 5: (55, 65), 6: (65, 75), 7: (75, 83)}
GROUPS = A.TARGETS[:3] + A.REFERENCES[:2]


def profiles() -> pd.DataFrame:
    cps = A.ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
    medical_zip = A.ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {name: state["group"][name] & civilian for name in GROUPS}
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    shared, _personal, _renter = A.matrices(state)
    medical, _anchors = A.read_meps(medical_zip, medical_sas)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    cells, codes, _cov = A.donor_model(medical, d, False)
    means = cells.mean_public_paid.to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:, None]
    stats = A.sufficient(shared, health, weights, groups, bands, 8,
                         population_weights=weights, health_weights=weights)
    rows = []
    for g in GROUPS:
        cell = stats[g]
        bal = A.account(cell, A.COEFFICIENTS, means)[:, 0]
        for b in range(8):
            rows.append(dict(group=g, band=b, population=float(cell["n"][b, 0]),
                             balance_per_person=float(bal[b] / cell["n"][b, 0])))
    return pd.DataFrame(rows)


def lifetime(profile: pd.Series, start_age: int, rate: float) -> float:
    total = 0.0
    for b, (lo, hi) in BANDS.items():
        for age in range(lo, hi):
            if age < start_age:
                continue
            total += profile[b] / (1 + rate) ** (age - start_age)
    return total


def main() -> None:
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    prof = profiles()
    prof.to_csv(out / "age_profiles_references.csv", index=False)
    stored = pd.read_csv(LANE / "derived/age_profiles.csv")
    stored = stored[stored.scenario.eq("all_age_shared") & stored.target.isin(A.TARGETS[:3])]
    merged = prof.merge(stored, left_on=["group", "band"], right_on=["target", "band"])
    err = float(np.max(np.abs(merged.balance_per_person_x - merged.balance_per_person_y)))
    print(f"[gate] target profiles reproduce stored age_profiles.csv: max |diff| = ${err:.4f} -> {'PASS' if err < 0.01 else 'FAIL'}")
    if err >= 0.01:
        raise SystemExit(1)
    pivot = prof.pivot(index="band", columns="group", values="balance_per_person")
    print("\n[per-band balance per person, all_age_shared]")
    print(pivot.round(0).to_string())
    rows = []
    for rate in [0.0, 0.02, 0.03, 0.05]:
        for g in GROUPS:
            for start in ([0] if g != "mexico_born" else [0, 25]):
                v = lifetime(pivot[g], start, rate)
                rows.append(dict(rate=rate, group=g, start_age=start, lifetime_balance=v))
    life = pd.DataFrame(rows)
    ref = life[life.group.eq("third_plus_nh_white") & life.start_age.eq(0)].set_index("rate").lifetime_balance
    life["budget_vs_white_child"] = life.apply(lambda r: ref[r.rate] - r.lifetime_balance, axis=1)
    life.to_csv(out / "lifetime_equivalence.csv", index=False)
    print("\n[lifetime balance per person, period profile, and budget = white-child lifetime minus group lifetime]")
    for rate, g in life.groupby("rate"):
        print(f"\n rate {rate:.0%}")
        print(g[["group", "start_age", "lifetime_balance", "budget_vs_white_child"]].round(0).to_string(index=False))


if __name__ == "__main__":
    main()
