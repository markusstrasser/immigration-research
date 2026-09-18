#!/usr/bin/env python3
"""Can age composition explain the offender-rate ranking?

The NCVS publishes perceived-offender age only as a national marginal in three
bands (12-17, 18-29, 30 or older), never crossed with race or Hispanic origin.
So a direct age-standardised offender rate by group is not identified.  What IS
identified is a bound: apply the national age-specific offending rate implied by
CV2024 table 11 to each group's own age structure (indirect standardisation) and
see how much of the between-group spread age composition can generate.

Population by group and age comes from ACS 2023 1-year detailed tables
B01001H (white alone, not Hispanic), B01001B (Black or African American alone)
and B01001I (Hispanic or Latino).

Run:
  cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 age_standardise.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
CACHE.mkdir(exist_ok=True)

TABLES = {"White": "B01001H", "Black": "B01001B", "Hispanic": "B01001I"}

# B01001H/B/I line numbers -> (male line, female line, age low, age high inclusive).
# Verified against https://api.census.gov/data/2023/acs/acs1/groups/B01001I.json
# (cached as _cache/b01001i_vars.json): 14 age brackets per sex, male 003-016,
# female 018-031.  These race/ethnicity tables collapse 20-24 into one bracket,
# unlike the all-population B01001.
BRACKETS = [
    (3, 18, 0, 4), (4, 19, 5, 9), (5, 20, 10, 14), (6, 21, 15, 17),
    (7, 22, 18, 19), (8, 23, 20, 24), (9, 24, 25, 29), (10, 25, 30, 34),
    (11, 26, 35, 44), (12, 27, 45, 54), (13, 28, 55, 64), (14, 29, 65, 74),
    (15, 30, 75, 84), (16, 31, 85, 99),
]

FAILS: list[str] = []


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'✓' if ok else '✗'} [{name}] {detail}")
    if not ok:
        FAILS.append(name)


def census_key() -> str:
    """CENSUS_API_KEY from the environment, else from the repo's acquire config."""
    if os.environ.get("CENSUS_API_KEY"):
        return os.environ["CENSUS_API_KEY"]
    cfg = REPO / "infra/immigration-fiscal/acquire/config.local.env"
    if not cfg.exists():
        cfg = Path.home() / "Projects/immigration-research/infra/immigration-fiscal/acquire/config.local.env"
    for line in cfg.read_text().splitlines():
        line = line.strip()
        if line.startswith("CENSUS_API_KEY") or line.startswith("export CENSUS_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("CENSUS_API_KEY not found in config.local.env")


def fetch_table(table: str, key: str) -> dict[str, float]:
    cache = CACHE / f"acs2023_{table}.json"
    if cache.exists():
        payload = json.loads(cache.read_text())
    else:
        cols = []
        for m, f, _, _ in BRACKETS:
            cols += [f"{table}_{m:03d}E", f"{table}_{f:03d}E"]
        url = (
            "https://api.census.gov/data/2023/acs/acs1?get="
            + ",".join(cols)
            + "&for=us:1&key="
            + urllib.parse.quote(key)
        )
        with urllib.request.urlopen(url, timeout=120) as r:
            payload = json.loads(r.read().decode())
        cache.write_text(json.dumps(payload))
    head, row = payload[0], payload[1]
    return {h: float(v) for h, v in zip(head, row) if h.endswith("E")}


def bands(vals: dict[str, float], table: str) -> dict[str, float]:
    """Collapse to the NCVS offender bands, splitting 10-14 three fifths at age 12."""
    out = {"12-17": 0.0, "18-29": 0.0, "30+": 0.0}
    for m, f, lo, hi in BRACKETS:
        n = vals[f"{table}_{m:03d}E"] + vals[f"{table}_{f:03d}E"]
        if hi < 12:
            continue
        if lo == 10:
            out["12-17"] += n * 3 / 5  # ages 12,13,14 of the 10-14 bracket
        elif hi <= 17:
            out["12-17"] += n
        elif hi <= 29:
            out["18-29"] += n
        else:
            out["30+"] += n
    return out


# The finer bands CV2024 table 3 publishes a victimisation rate for.  The NCVS
# never publishes an offender rate on this grid, so the victim-age curve stands in
# for the offender-age curve; in violent crime the two are close in age.
FINE = ["12-17", "18-24", "25-34", "35-49", "50-64", "65+"]


def fine_bands(vals: dict[str, float], table: str) -> dict[str, float]:
    """Collapse to the CV table 3 age bands; 45-54 is split in half at 50."""
    out = {k: 0.0 for k in FINE}
    for m, f, lo, hi in BRACKETS:
        n = vals[f"{table}_{m:03d}E"] + vals[f"{table}_{f:03d}E"]
        if hi < 12:
            continue
        if lo == 10:
            out["12-17"] += n * 3 / 5
        elif hi <= 17:
            out["12-17"] += n
        elif hi <= 24:
            out["18-24"] += n
        elif hi <= 34:
            out["25-34"] += n
        elif hi <= 44:
            out["35-49"] += n
        elif lo == 45:
            out["35-49"] += n / 2      # 45-49
            out["50-64"] += n / 2      # 50-54
        elif hi <= 64:
            out["50-64"] += n
        else:
            out["65+"] += n
    return out


def main() -> None:
    key = census_key()
    rows = []
    for g, tbl in TABLES.items():
        b = bands(fetch_table(tbl, key), tbl)
        tot = sum(b.values())
        rows.append({"group": g, **b, "total_12plus": tot,
                     **{f"share_{k}": v / tot for k, v in b.items()}})
    age = pd.DataFrame(rows)
    print("\nACS 2023 1-year population age 12+ by group and NCVS age band:")
    print(age.round(4).to_string(index=False))
    age.to_csv(DERIVED / "age_structure_by_group_acs2023.csv", index=False)

    # National age-specific offender rate implied by CV2024 table 11.
    # Population and offender incidents by band, 2024, from cv24t11 (cached parse).
    t11_pop = {"12-17": 25_687_710, "18-29": 51_911_950, "30+": 208_773_550}
    t11_off = {"12-17": 437_050, "18-29": 860_880, "30+": 3_320_330}
    nat = {k: 1000 * t11_off[k] / t11_pop[k] for k in t11_pop}
    print("\nNational perceived-offender incidents per 1,000 residents of the band, 2024:")
    for k, v in nat.items():
        print(f"  {k}: {v:.2f}")
    gate("age_gradient_is_weak_in_published_bands",
         max(nat.values()) / min(nat.values()) < 1.5,
         f"ratio of the highest to the lowest band rate = "
         f"{max(nat.values()) / min(nat.values()):.2f} — the published 30-or-older band is "
         "so wide that the age-crime curve is almost invisible in it")

    # Indirect standardisation: the offender rate each group would show if the only
    # thing that differed between groups were its age structure.
    expected = []
    for _, r in age.iterrows():
        e = (r["12-17"] * nat["12-17"] + r["18-29"] * nat["18-29"]
             + r["30+"] * nat["30+"]) / r["total_12plus"]
        expected.append({"group": r["group"], "expected_rate_per_1000_from_age_alone": e})
    ex = pd.DataFrame(expected)
    base = ex.expected_rate_per_1000_from_age_alone
    ex["index_vs_white"] = base / base[ex.group == "White"].iloc[0]
    print("\nOffender rate per 1,000 each group would show if only its age structure "
          "differed:")
    print(ex.round(3).to_string(index=False))
    ex.to_csv(DERIVED / "age_expected_offender_rate.csv", index=False)

    # Variant B: the same indirect standardisation on the finer grid CV2024 table 3
    # publishes, where the age gradient is real (4.6x from 18-24 to 65 or older).
    # CV2024 table 3, total violent crime, rate per 1,000 persons age 12 or older, 2024.
    VICTIM_AGE_RATE = {"12-17": 29.3, "18-24": 34.8, "25-34": 31.7,
                       "35-49": 27.1, "50-64": 20.4, "65+": 7.5}
    gate("fine_age_gradient_is_real",
         max(VICTIM_AGE_RATE.values()) / min(VICTIM_AGE_RATE.values()) > 3.0,
         f"ratio of the highest to the lowest fine-band rate = "
         f"{max(VICTIM_AGE_RATE.values()) / min(VICTIM_AGE_RATE.values()):.2f}")
    fine_rows = []
    for g, tbl in TABLES.items():
        fb = fine_bands(fetch_table(tbl, key), tbl)
        tot = sum(fb.values())
        e = sum(fb[k] * VICTIM_AGE_RATE[k] for k in FINE) / tot
        fine_rows.append({"group": g, "expected_rate_fine_grid": e,
                          **{f"share_{k}": fb[k] / tot for k in FINE}})
    fine = pd.DataFrame(fine_rows)
    fine["index_vs_white_fine"] = (
        fine.expected_rate_fine_grid / fine.loc[fine.group == "White",
                                                "expected_rate_fine_grid"].iloc[0]
    )
    print("\nVariant B, fine grid: the rate each group would show if only its age "
          "structure differed")
    print(fine.round(4).to_string(index=False))
    fine.to_csv(DERIVED / "age_expected_offender_rate_fine_grid.csv", index=False)
    ex = ex.merge(fine[["group", "expected_rate_fine_grid", "index_vs_white_fine"]],
                  on="group")

    obs = pd.read_csv(DERIVED / "rates_by_victim_and_offender_2022_2024.csv")
    obs = obs[obs.side == "offender"].set_index("group").rate_per_1000
    cmp = ex.set_index("group").join(obs.rename("observed_rate_per_1000"))
    cmp["observed_index_vs_white"] = cmp.observed_rate_per_1000 / cmp.loc["White", "observed_rate_per_1000"]
    cmp["age_explains_pp_of_index"] = cmp.index_vs_white - 1.0
    print("\nObserved against age-expected:")
    print(cmp.round(3).to_string())
    cmp.to_csv(DERIVED / "age_arm_observed_vs_expected.csv")

    spread_obs = cmp.observed_index_vs_white.max() - cmp.observed_index_vs_white.min()
    spread_age = cmp.index_vs_white.max() - cmp.index_vs_white.min()
    spread_fine = cmp.index_vs_white_fine.max() - cmp.index_vs_white_fine.min()
    gate("age_cannot_explain_the_spread_coarse", spread_age < 0.25 * spread_obs,
         f"the published offender bands generate a {spread_age:.3f} spread in the index "
         f"against {spread_obs:.3f} observed — but the bands are too coarse to carry an "
         "age effect, so this is a fact about the instrument")
    gate("age_cannot_explain_the_spread_fine", spread_fine < 0.25 * spread_obs,
         f"the fine victim-age grid generates a {spread_fine:.3f} spread against "
         f"{spread_obs:.3f} observed; age composition can move the Hispanic index to "
         f"{cmp.loc['Hispanic', 'index_vs_white_fine']:.3f} and the Black index to "
         f"{cmp.loc['Black', 'index_vs_white_fine']:.3f}")

    if FAILS:
        raise SystemExit("gates failed: " + ", ".join(FAILS))
    print("\n[done] age_standardise.py")


if __name__ == "__main__":
    sys.exit(main())
