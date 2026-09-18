"""Phases A and B on one footing: the timing adjustment run through the survival machinery.

Phase A changes how many years each age-band balance is applied for.  Phase B changes the
balance inside the working-age bands.  Neither answers the falsification question on its own,
because one is a lifetime total and the other a per-person-year flow.  This script adds the
Phase B per-band adjustment to the Phase A band profile and recomputes the lifetime gap under
every survival arm, so the two corrections are stated in the same units and can be summed.

The reported quantity is the lifetime balance gap against third-plus non-Hispanic whites,
and the per-person-year equivalent obtained by dividing that gap by the group's own expected
person-years from the start age under the same survival table.

Outputs derived/combined_lifetime.csv and derived/combined_summary.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FISCAL / "homicide_cost_2026_09_18"))
import cost_model as CM  # noqa: E402
import longevity as L  # noqa: E402

GROUPS = L.GROUPS + ["mexican_observed_total"]
MEXICAN = L.MEXICAN + ["mexican_observed_total"]
CENTRAL_B = dict(family_arm="observed_family", earnings_arm="individual",
                 self_employment=True, coverage_scale=1.0)
SURVIVAL_ARMS = ["terminal83", "common_white", "group_specific", "paradox_fades",
                 "mortality_65plus", "fenelon_mexican"]
TIMING_ARMS = ["none", "accrual_only", "cash_to_accrual"]


def band_adjustment(byband: pd.DataFrame, adjustment: str) -> dict[str, np.ndarray]:
    if adjustment == "none":
        return {g: np.zeros(8) for g in GROUPS}
    sel = byband[(byband.family_arm == CENTRAL_B["family_arm"])
                 & (byband.earnings_arm == CENTRAL_B["earnings_arm"])
                 & (byband.self_employment == CENTRAL_B["self_employment"])
                 & np.isclose(byband.coverage_scale, CENTRAL_B["coverage_scale"])
                 & (byband.adjustment == adjustment)]
    out = {}
    for g in GROUPS:
        v = sel[sel.group == g].sort_values("band").adjustment_per_person.to_numpy()
        if len(v) != 8:
            raise ValueError(f"{adjustment}/{g}: {len(v)} bands, expected 8")
        out[g] = v
    return out


def person_years(table: pd.DataFrame, start: int, rate: float, last: int) -> float:
    ages = np.arange(start, last + 1)
    w = table.Lx.to_numpy()[start:last + 1] / table.lx.to_numpy()[start]
    return float((w * (1 + rate) ** -(ages - start)).sum())


def main() -> None:
    wide, shift = CM.load_profiles()
    byband = pd.read_csv(OUT / "ss_timing_by_band.csv")
    tables = {}
    for key in L.TABLES:
        tables[(2024, key)] = L.read_life_table(2024, key)
        tables[(2023, key)] = L.read_life_table(2023, key)
    L_tables = tables

    def survival_for(arm: str) -> dict[str, pd.DataFrame]:
        w24, h24 = L_tables[(2024, "nh_white")], L_tables[(2024, "hispanic")]
        if arm == "common_white":
            return {g: w24 for g in GROUPS}
        if arm == "group_specific":
            return {**{g: h24 for g in MEXICAN}, "third_plus_nh_white": w24, "all_native": w24}
        if arm == "paradox_fades":
            return {"mexico_born": h24, "mexican_second_gen": w24,
                    "mexican_third_plus_selfid": w24, "mexican_observed_total": h24,
                    "third_plus_nh_white": w24, "all_native": w24}
        if arm == "mortality_65plus":
            hyb = L.hybrid_65(w24, h24)
            return {**{g: hyb for g in MEXICAN}, "third_plus_nh_white": w24, "all_native": w24}
        if arm == "fenelon_mexican":
            fb, ub = L.fenelon_table(w24, "foreign_born"), L.fenelon_table(w24, "us_born")
            pop = CM.load_profiles()[0]
            return {"mexico_born": fb, "mexican_second_gen": ub,
                    "mexican_third_plus_selfid": ub, "mexican_observed_total": fb,
                    "third_plus_nh_white": w24, "all_native": w24}
        raise ValueError(arm)

    rows = []
    for account in ("partial", "complete"):
        for rate in (0.0, 0.03):
            for timing in TIMING_ARMS:
                adj = band_adjustment(byband, timing)
                for surv in SURVIVAL_ARMS:
                    tabs = None if surv == "terminal83" else survival_for(surv)
                    for g in GROUPS:
                        sh = shift[g] if account == "complete" else 0.0
                        prof = L.band_profile(wide, g, sh, L.OMEGA)
                        for b, (lo, hi) in CM.BANDS.items():
                            top = L.OMEGA + 1 if b == max(CM.BANDS) else hi
                            prof[lo:top] += adj[g][b]
                        for start in (0, 25):
                            if surv == "terminal83":
                                v = L.lifetime_terminal(prof, start, rate)
                                py = float(((1 + rate) ** -np.arange(0, CM.TERMINAL - start)).sum())
                            else:
                                v = L.lifetime_survival(prof, start, rate, tabs[g], L.OMEGA)
                                py = person_years(tabs[g], start, rate, L.OMEGA)
                            rows.append(dict(account=account, rate=rate, timing=timing,
                                             survival=surv, group=g, start_age=start,
                                             lifetime=v, person_years=py))
    d = pd.DataFrame(rows)
    ref = d[d.group.eq("third_plus_nh_white")].set_index(
        ["account", "rate", "timing", "survival", "start_age"])[["lifetime", "person_years"]]
    d["gap_vs_white"] = d.apply(
        lambda r: r.lifetime - ref.lifetime[(r.account, r.rate, r.timing, r.survival, r.start_age)],
        axis=1)
    # annual equivalent: the lifetime gap spread over the white reference's own person-years,
    # which is the denominator the repo's per-person-year gap uses.
    d["gap_per_year"] = d.apply(
        lambda r: r.gap_vs_white / ref.person_years[(r.account, r.rate, r.timing, r.survival, r.start_age)],
        axis=1)
    d.to_csv(OUT / "combined_lifetime.csv", index=False)

    base = d[d.timing.eq("none") & d.survival.eq("terminal83")].set_index(
        ["account", "rate", "group", "start_age"]).gap_vs_white
    d["gap_change_vs_repo"] = d.apply(
        lambda r: r.gap_vs_white - base[(r.account, r.rate, r.group, r.start_age)], axis=1)

    summary = d[d.group.isin(MEXICAN)].copy()
    summary.to_csv(OUT / "combined_summary.csv", index=False)

    pd.set_option("display.width", 240)
    print("[lifetime gap vs third-plus NH white, complete account, undiscounted, from age 0]")
    print(d[d.account.eq("complete") & d.rate.eq(0.0) & d.start_age.eq(0)
            & d.group.isin(MEXICAN)]
          .pivot(index=["timing", "survival"], columns="group", values="gap_vs_white")
          .round(0).to_string())

    print("\n[same, at 3%]")
    print(d[d.account.eq("complete") & d.rate.eq(0.03) & d.start_age.eq(0)
            & d.group.isin(MEXICAN)]
          .pivot(index=["timing", "survival"], columns="group", values="gap_vs_white")
          .round(0).to_string())

    print("\n[annual-equivalent gap, complete account, undiscounted, from age 0, $ per year]")
    print(d[d.account.eq("complete") & d.rate.eq(0.0) & d.start_age.eq(0)
            & d.group.isin(MEXICAN + ["mexican_observed_total"] if False else MEXICAN)]
          .pivot(index=["timing", "survival"], columns="group", values="gap_per_year")
          .round(0).to_string())

    print("\n[change in the lifetime gap against the repo baseline, complete, undiscounted, age 0]")
    print(d[d.account.eq("complete") & d.rate.eq(0.0) & d.start_age.eq(0)
            & d.group.isin(MEXICAN)]
          .pivot(index=["timing", "survival"], columns="group", values="gap_change_vs_repo")
          .round(0).to_string())

    worst = d[d.group.isin(MEXICAN)].sort_values("gap_vs_white", ascending=False).head(5)
    print("\n[closest any arm comes to closing the gap: largest gap_vs_white among Mexican groups]")
    print(worst[["account", "rate", "timing", "survival", "group", "start_age",
                 "gap_vs_white", "gap_per_year"]].round(0).to_string(index=False))
    print(f"\n[written] {OUT}/combined_lifetime.csv, combined_summary.csv")


if __name__ == "__main__":
    main()
