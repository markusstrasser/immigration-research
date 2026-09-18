"""Phase A: replace the repo's constructed terminal age with NVSS survival weights.

The repo's period-profile lifetime (pronatal_equivalence_2026_09_18/lifetime_profiles.py)
assumes every person lives exactly to age 83 and then stops: every age 0..82 carries weight
1.0 and every age 83+ carries weight 0.  This script swaps that deterministic weight for the
NVSS 2024 life-table person-years L(x), conditional on surviving to the start age:

    lifetime(g, S, start, r) = sum_{x=start}^{100} b_g(x) * L_S(x)/l_S(start) * (1+r)^{-(x-start)}

b_g(x) is the group's per-person-year balance at single year of age x, piecewise constant on
the eight CPS bands; the top band is 75+ in the CPS, so its value is carried to age 100.

Two of the changes run in opposite directions and are reported separately:
  - survival below 83 is less than 1, which REMOVES weight from the working ages (bad for a
    group whose working years are its positive years),
  - survival above 82 is positive, which ADDS weight to the 65+ years (the costly ones).

Arms, all on the partial account and on the complete account (uniform per-person-year shift
from the absolute ledger's waterfall step 14):
  terminal83          repo baseline, the gate
  common_white        White non-Hispanic life table for EVERY group (isolates profile effects)
  group_specific      Hispanic table for the three Mexican-origin groups, White NH for the
                      white reference and for all_native  (central)
  paradox_fades       Hispanic table for mexico_born only; White NH for 2nd and 3rd+ gen
  mortality_65plus    White NH survival to 65 for everyone, group-specific only after 65
  truncate83          group-specific survival but the sum still stops at 82
  male / female       single-sex life tables, as a bracket
  lt2023              the 2023 life tables instead of 2024, as a stability check

Outputs derived/survival_tables.csv, derived/longevity_lifetime.csv,
derived/longevity_gaps.csv, derived/longevity_audit.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(FISCAL / "homicide_cost_2026_09_18"))
import cost_model as CM  # noqa: E402  (load_profiles, by_age, BANDS, TERMINAL)

PRONATAL = FISCAL / "pronatal_equivalence_2026_09_18/derived/lifetime_equivalence.csv"
OMEGA = 100                      # last age in the NVSS complete life table ("100 and over")
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
          "third_plus_nh_white", "all_native"]
MEXICAN = GROUPS[:3]

# NVSS 2024 (NVSR Vol 75 No 5) and 2023 (Vol 74 No 6) table numbers
TABLES = {"hispanic": "04", "hispanic_male": "05", "hispanic_female": "06",
          "nh_white": "16", "nh_white_male": "17", "nh_white_female": "18",
          "total": "01"}


# --------------------------------------------------------------------- life tables
def read_life_table(year: int, key: str) -> pd.DataFrame:
    """Return ages 0..100 with lx and Lx from the NVSS spreadsheet."""
    path = CACHE / f"lt{year}_Table{TABLES[key]}.xlsx"
    raw = pd.read_excel(path, header=None)
    rows = []
    for _, r in raw.iterrows():
        label = str(r[0]).strip().replace("–", "-").replace("—", "-")
        if label.startswith("100 and"):
            age = 100
        elif "-" in label and label[0].isdigit():
            age = int(label.split("-")[0])
        else:
            continue
        rows.append(dict(age=age, qx=float(r[1]), lx=float(r[2]), Lx=float(r[4])))
    t = pd.DataFrame(rows).sort_values("age").reset_index(drop=True)
    if len(t) != OMEGA + 1 or t.age.tolist() != list(range(OMEGA + 1)):
        raise ValueError(f"{path.name}: expected ages 0..100, got {len(t)} rows")
    if abs(t.lx.iloc[0] - 100_000) > 1e-6:
        raise ValueError(f"{path.name}: radix is {t.lx.iloc[0]}, expected 100000")
    if (t.lx.diff().dropna() > 0).any():
        raise ValueError(f"{path.name}: lx is not monotone non-increasing")
    return t


def life_expectancy(t: pd.DataFrame, age: int = 0) -> float:
    """e(x) rebuilt from Lx, to check against the published ex column."""
    return float(t.Lx[t.age >= age].sum() / t.lx[t.age == age].iloc[0])


# [SOURCE: Fenelon A, Chinn JJ, Anderson RN. "A comprehensive analysis of the mortality
# experience of hispanic subgroups in the United States: variation by age, country of origin,
# and nativity." SSM - Population Health 2017;3:245-254, tables 3 (men) and 4 (women),
# Model 1 (unadjusted), Mexican-origin rows, non-Hispanic white = 1.00.]
# Mexican-origin mortality is ABOVE the white reference at ages 25-64 and below it at 65+,
# which the pooled Hispanic life table does not show, because the consistent Hispanic
# advantage sits with Dominican and Central/South American origins, not Mexican.
FENELON_HR = {"foreign_born": {"25_64": (1.18, 1.28), "65_plus": (0.71, 0.79)},
              "us_born": {"25_64": (1.22, 0.98), "65_plus": (0.87, 0.92)}}


def hazard_scaled(white: pd.DataFrame, hr_25_64: float, hr_65: float) -> pd.DataFrame:
    """Rebuild a life table from the white qx with a proportional hazard by age range."""
    q = white.qx.to_numpy().astype(float).copy()
    hr = np.ones(len(q))
    hr[25:65] = hr_25_64
    hr[65:] = hr_65
    q = 1.0 - np.power(1.0 - q, hr)
    q[OMEGA] = 1.0
    lx = np.empty(len(q))
    lx[0] = 100_000.0
    for i in range(1, len(q)):
        lx[i] = lx[i - 1] * (1.0 - q[i - 1])
    dx = lx * q
    w_lx, w_dx = white.lx.to_numpy(), white.lx.to_numpy() * white.qx.to_numpy()
    a0 = (white.Lx.to_numpy()[0] - w_lx[1]) / w_dx[0]     # fraction of the year lived by
    Lx = lx - 0.5 * dx                                     # infants who die before age 1
    Lx[0] = lx[1] + a0 * dx[0]
    e100_white = white.Lx.to_numpy()[OMEGA] / w_lx[OMEGA]
    Lx[OMEGA] = lx[OMEGA] * e100_white / max(hr_65, 1e-9)
    return pd.DataFrame(dict(age=white.age.to_numpy(), qx=q, lx=lx, Lx=Lx))


def fenelon_table(white: pd.DataFrame, nativity: str) -> pd.DataFrame:
    hr = FENELON_HR[nativity]
    return hazard_scaled(white, float(np.mean(hr["25_64"])), float(np.mean(hr["65_plus"])))


def hybrid_65(white: pd.DataFrame, group: pd.DataFrame) -> pd.DataFrame:
    """White survival to 65, then the group's own conditional survival after 65."""
    t = white.copy()
    scale = white.lx[white.age == 65].iloc[0] / group.lx[group.age == 65].iloc[0]
    late = group.age >= 65
    t.loc[late, "lx"] = group.loc[late, "lx"].to_numpy() * scale
    t.loc[late, "Lx"] = group.loc[late, "Lx"].to_numpy() * scale
    return t


# --------------------------------------------------------------------- lifetime sums
def band_profile(wide: pd.DataFrame, group: str, shift: float, omega: int) -> np.ndarray:
    """Per-person-year balance at every single year of age 0..omega (75+ band carried up)."""
    out = np.empty(omega + 1)
    for b, (lo, hi) in CM.BANDS.items():
        top = omega + 1 if b == max(CM.BANDS) else hi
        out[lo:top] = wide.loc[b, group]
    return out + shift


def lifetime_terminal(prof: np.ndarray, start: int, rate: float) -> float:
    """The repo's convention: weight 1 at ages start..82, zero after."""
    ages = np.arange(start, CM.TERMINAL)
    return float((prof[start:CM.TERMINAL] * (1 + rate) ** -(ages - start)).sum())


def lifetime_survival(prof: np.ndarray, start: int, rate: float, table: pd.DataFrame,
                      last_age: int = OMEGA) -> float:
    """Survival-weighted: person-years L(x) conditional on reaching `start`."""
    ages = np.arange(start, last_age + 1)
    w = table.Lx.to_numpy()[start:last_age + 1] / table.lx.to_numpy()[start]
    return float((prof[start:last_age + 1] * w * (1 + rate) ** -(ages - start)).sum())


# --------------------------------------------------------------------- main
def main() -> None:
    wide, shift = CM.load_profiles()
    tables = {}
    for year in (2024, 2023):
        for key in TABLES:
            tables[(year, key)] = read_life_table(year, key)

    # ---- audit of the tables themselves
    audit = {"life_expectancy_at_birth_rebuilt_from_Lx": {}, "published_ex_at_birth": {}}
    for (year, key), t in tables.items():
        audit["life_expectancy_at_birth_rebuilt_from_Lx"][f"{year}_{key}"] = round(life_expectancy(t), 3)
    e0h, e0w = life_expectancy(tables[(2024, "hispanic")]), life_expectancy(tables[(2024, "nh_white")])
    audit["hispanic_minus_white_e0_2024"] = round(e0h - e0w, 3)
    audit["hispanic_minus_white_e25_2024"] = round(
        life_expectancy(tables[(2024, "hispanic")], 25) - life_expectancy(tables[(2024, "nh_white")], 25), 3)
    audit["hispanic_minus_white_e65_2024"] = round(
        life_expectancy(tables[(2024, "hispanic")], 65) - life_expectancy(tables[(2024, "nh_white")], 65), 3)
    print(f"[life tables] 2024 e0: Hispanic {e0h:.2f}, White NH {e0w:.2f}, gap {e0h-e0w:+.2f}")
    print(f"              2024 e25 gap {audit['hispanic_minus_white_e25_2024']:+.2f}, "
          f"e65 gap {audit['hispanic_minus_white_e65_2024']:+.2f}")

    # gate: the hazard rebuild at HR = 1 must reproduce the white table it is built from
    identity = hazard_scaled(tables[(2024, "nh_white")], 1.0, 1.0)
    e0_err = abs(life_expectancy(identity) - e0w)
    print(f"[gate] hazard rebuild at HR=1 reproduces the White NH table: "
          f"|de0| = {e0_err:.4f} years -> {'PASS' if e0_err < 0.02 else 'FAIL'}")
    if e0_err >= 0.02:
        raise SystemExit(1)
    audit["gate_hazard_rebuild_e0_error_years"] = round(e0_err, 6)
    for nat in FENELON_HR:
        t = fenelon_table(tables[(2024, "nh_white")], nat)
        audit[f"fenelon_{nat}_e0"] = round(life_expectancy(t), 3)
        audit[f"fenelon_{nat}_e65"] = round(life_expectancy(t, 65), 3)
    print("[fenelon] rebuilt e0: foreign-born Mexican "
          f"{audit['fenelon_foreign_born_e0']:.2f}, US-born Mexican "
          f"{audit['fenelon_us_born_e0']:.2f}, White NH {e0w:.2f}")

    surv = []
    for (year, key), t in tables.items():
        for _, r in t.iterrows():
            surv.append(dict(year=year, table=key, age=int(r.age), lx=r.lx, Lx=r.Lx))
    pd.DataFrame(surv).to_csv(OUT / "survival_tables.csv", index=False)

    # ---- gate: reproduce the pronatal lane's stored lifetime numbers exactly
    stored = pd.read_csv(PRONATAL)
    worst = 0.0
    for _, r in stored.iterrows():
        prof = band_profile(wide, r.group, 0.0, CM.TERMINAL - 1)
        mine = lifetime_terminal(prof, int(r.start_age), float(r.rate))
        worst = max(worst, abs(mine - r.lifetime_balance))
    print(f"[gate] terminal-83 lifetimes reproduce lifetime_equivalence.csv: "
          f"max |diff| = ${worst:.6f} -> {'PASS' if worst < 0.01 else 'FAIL'}")
    if worst >= 0.01:
        raise SystemExit(1)
    audit["gate_max_abs_diff_vs_pronatal_usd"] = round(worst, 6)

    # ---- the arms: a survival table per group
    def arm_tables(name: str) -> dict[str, pd.DataFrame]:
        w24, h24 = tables[(2024, "nh_white")], tables[(2024, "hispanic")]
        if name == "common_white":
            return {g: w24 for g in GROUPS}
        if name == "group_specific":
            return {**{g: h24 for g in MEXICAN}, "third_plus_nh_white": w24, "all_native": w24}
        if name == "paradox_fades":
            return {"mexico_born": h24, "mexican_second_gen": w24, "mexican_third_plus_selfid": w24,
                    "third_plus_nh_white": w24, "all_native": w24}
        if name == "mortality_65plus":
            hyb = hybrid_65(w24, h24)
            return {**{g: hyb for g in MEXICAN}, "third_plus_nh_white": w24, "all_native": w24}
        if name in ("male", "female"):
            h, w = tables[(2024, f"hispanic_{name}")], tables[(2024, f"nh_white_{name}")]
            return {**{g: h for g in MEXICAN}, "third_plus_nh_white": w, "all_native": w}
        if name == "lt2023":
            h, w = tables[(2023, "hispanic")], tables[(2023, "nh_white")]
            return {**{g: h for g in MEXICAN}, "third_plus_nh_white": w, "all_native": w}
        if name == "fenelon_mexican":
            fb, ub = fenelon_table(w24, "foreign_born"), fenelon_table(w24, "us_born")
            return {"mexico_born": fb, "mexican_second_gen": ub,
                    "mexican_third_plus_selfid": ub, "third_plus_nh_white": w24,
                    "all_native": w24}
        if name == "truncate83":
            return {**{g: h24 for g in MEXICAN}, "third_plus_nh_white": w24, "all_native": w24}
        raise ValueError(name)

    ARMS = ["common_white", "group_specific", "paradox_fades", "mortality_65plus",
            "fenelon_mexican", "truncate83", "male", "female", "lt2023"]
    rows = []
    for account in ("partial", "complete"):
        for rate in (0.0, 0.03):
            for g in GROUPS:
                sh = shift[g] if account == "complete" else 0.0
                prof = band_profile(wide, g, sh, OMEGA)
                for start in ([0, 25] if g == "mexico_born" else [0, 25]):
                    rows.append(dict(arm="terminal83", account=account, rate=rate, group=g,
                                     start_age=start,
                                     lifetime=lifetime_terminal(prof, start, rate)))
                    for arm in ARMS:
                        t = arm_tables(arm)[g]
                        last = CM.TERMINAL - 1 if arm == "truncate83" else OMEGA
                        rows.append(dict(arm=arm, account=account, rate=rate, group=g,
                                         start_age=start,
                                         lifetime=lifetime_survival(prof, start, rate, t, last)))
    life = pd.DataFrame(rows)
    life.to_csv(OUT / "longevity_lifetime.csv", index=False)

    # ---- gaps against the white reference, and the longevity-only piece
    ref = (life[life.group.eq("third_plus_nh_white")]
           .set_index(["arm", "account", "rate", "start_age"]).lifetime)
    life["gap_vs_white"] = life.apply(
        lambda r: ref[(r.arm, r.account, r.rate, r.start_age)] - r.lifetime, axis=1)
    gaps = life[life.group.isin(MEXICAN + ["all_native"])].copy()

    base = (gaps[gaps.arm.eq("terminal83")]
            .set_index(["account", "rate", "group", "start_age"]).gap_vs_white)
    common = (gaps[gaps.arm.eq("common_white")]
              .set_index(["account", "rate", "group", "start_age"]).gap_vs_white)
    gaps["gap_change_vs_terminal83"] = gaps.apply(
        lambda r: r.gap_vs_white - base[(r.account, r.rate, r.group, r.start_age)], axis=1)
    gaps["longevity_only"] = gaps.apply(
        lambda r: r.gap_vs_white - common[(r.account, r.rate, r.group, r.start_age)], axis=1)
    gaps.to_csv(OUT / "longevity_gaps.csv", index=False)

    pd.set_option("display.width", 220)
    print("\n[lifetime balance per person, partial account, from age 0]")
    p = life[life.account.eq("partial") & life.start_age.eq(0)].pivot(
        index=["arm", "rate"], columns="group", values="lifetime")
    print(p.round(0).to_string())

    print("\n[gap vs third-plus NH white, complete account, from age 0]")
    q = gaps[gaps.account.eq("complete") & gaps.start_age.eq(0)].pivot(
        index=["arm", "rate"], columns="group", values="gap_vs_white")
    print(q.round(0).to_string())

    print("\n[longevity alone: arm gap minus the common-white-survival gap, $ per person]")
    r = gaps[gaps.arm.isin(["group_specific", "paradox_fades", "mortality_65plus",
                            "fenelon_mexican", "truncate83"])].pivot(
        index=["arm", "account", "rate", "start_age"], columns="group", values="longevity_only")
    print(r.round(0).to_string())

    audit["arms"] = ["terminal83"] + ARMS
    json.dump(audit, open(OUT / "longevity_audit.json", "w"), indent=2, sort_keys=True)
    print(f"\n[written] {OUT}/longevity_lifetime.csv, longevity_gaps.csv, "
          f"survival_tables.csv, longevity_audit.json")


if __name__ == "__main__":
    main()
