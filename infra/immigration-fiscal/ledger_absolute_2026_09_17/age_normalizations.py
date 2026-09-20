#!/usr/bin/env python3
"""Hold age-specific fiscal rates fixed and vary only the age structure.

Native-First: consumes the verified annual age-profile export and the verified
period-profile export through `lifetime.py`; no new estimator or forecast.

Four structures, per person per year: each group's own ages today, the
third-plus non-Hispanic white reference's ages today, the observed Mexican-origin
union's ages today, and a stationary population (US-total 2024 NVSS person-years,
full life course, no discounting). The stationary row is the 0% period-profile
NPV divided by its person-years, so it inherits every limitation of that export:
current cross-sectional rates, no cohort change, outmigration or descendants.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from lifetime import BANDS, LANE, ROOT, load_age_profiles, load_period_profiles, read_life_table

WHITE, UNION = "third_plus_nh_white", "mexican_observed_total"
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid", UNION, WHITE, "all_native"]
RECEIPTS = {"tax", "employer", "sales", "X", "owner_property", "C"}


def band_shares(profiles: pd.DataFrame, allocation: str, group: str) -> np.ndarray:
    block = profiles[(profiles.allocation == allocation) & (profiles.account == "expanded")
                     & (profiles.group == group)].sort_values("band")
    return (block.population / block.population.sum()).to_numpy()


def stationary_shares(table: pd.DataFrame) -> np.ndarray:
    years = np.array([table.Lx.to_numpy()[lo:hi].sum() for lo, hi in BANDS])
    return years / years.sum()


def calculate(profiles: pd.DataFrame, components: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    expanded = components[components.account == "expanded"].copy()
    expanded["side"] = np.where(expanded.component.isin(RECEIPTS), "receipts", "spending")
    dollars = expanded.groupby(["allocation", "group", "band", "side"]).signed_total.sum().unstack("side")
    population = profiles[profiles.account == "expanded"].set_index(["allocation", "group", "band"]).population
    rates = dollars.div(population, axis=0)
    rates["net"] = rates.receipts + rates.spending
    rows = []
    for allocation in ("shared", "personal"):
        structures = {"own_ages_today": None,
                      "white_ages_today": band_shares(profiles, allocation, WHITE),
                      "union_ages_today": band_shares(profiles, allocation, UNION),
                      "stationary_life_course": stationary_shares(table)}
        for structure, weights in structures.items():
            for group in GROUPS:
                own = weights is None
                group_w = band_shares(profiles, allocation, group) if own else weights
                white_w = band_shares(profiles, allocation, WHITE) if own else weights
                value = rates.loc[(allocation, group)].sort_index().to_numpy().T @ group_w
                reference = rates.loc[(allocation, WHITE)].sort_index().to_numpy().T @ white_w
                columns = rates.columns.tolist()
                row = dict(allocation=allocation, structure=structure, group=group)
                for name, amount, ref in zip(columns, value, reference):
                    row[f"{name}_per_person"] = amount
                    row[f"{name}_gap_vs_white"] = amount - ref
                rows.append(row)
    return pd.DataFrame(rows)


def verify(result: pd.DataFrame, profiles: pd.DataFrame, period: pd.DataFrame, gaps: pd.DataFrame) -> None:
    raw = profiles[profiles.account == "expanded"].groupby(["allocation", "group"])[["net_total", "population"]].sum()
    raw = (raw.net_total / raw.population).rename("expected")
    own = result[result.structure == "own_ages_today"].set_index(["allocation", "group"]).join(raw)
    if not np.allclose(own.net_per_person, own.expected, rtol=1e-10):
        raise ValueError("[BLOCKED] own-age nets do not reproduce the annual export")
    life = period[(period.account == "expanded") & (period.survival == "common_total")
                  & (period.horizon == "full_100plus") & (period.start_age == 0)
                  & (period.real_discount_rate == 0.0)].set_index(["allocation", "group"])
    expected = (life.period_profile_npv / life.discounted_person_years).rename("expected")
    still = result[result.structure == "stationary_life_course"].set_index(["allocation", "group"]).join(expected)
    if still.expected.isna().any() or not np.allclose(still.net_per_person, still.expected, rtol=1e-9):
        raise ValueError("[BLOCKED] stationary nets do not reproduce the 0% period-profile export")
    published = gaps[gaps.reference == WHITE].set_index("group").complete_common_age_gap_per_person
    white = result[(result.structure == "white_ages_today") & (result.allocation == "shared")].set_index("group")
    ratio = white.net_gap_vs_white.reindex(published.index) / published
    if not ratio.between(0.98, 1.02).all():
        raise ValueError(f"[BLOCKED] eight-band white-age gaps leave the published finer-cell gaps: {ratio.to_dict()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    derived = root / LANE / "derived"
    profiles, _ = load_age_profiles(root)
    components = pd.read_csv(derived / "age_profile_components.csv")
    period = load_period_profiles(derived / "lifetime", root)
    result = calculate(profiles, components, read_life_table(root, "total"))
    verify(result, profiles, period, pd.read_csv(derived / "complete_gaps.csv"))
    target = derived / "age_normalizations.csv"
    result.to_csv(target, index=False, float_format="%.6f")
    print(f"[written] {len(result)} rows: {target}")
    view = result[result.allocation == "shared"].pivot(index="structure", columns="group", values="net_gap_vs_white")
    print(view[GROUPS[:4]].round(0).to_string())


if __name__ == "__main__":
    main()
