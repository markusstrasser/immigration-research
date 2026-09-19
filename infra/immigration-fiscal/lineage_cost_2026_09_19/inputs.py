#!/usr/bin/env python3
"""Resolve, hash and load every input the lineage model uses.

Every constant the scratch script hard-coded is replaced by a read from a
named lane output. Nothing here invents a number: each loader returns the
value plus the file and row it came from, and `manifest()` records sha256
for all of them.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

FISCAL = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- file paths
P_ABS_PROFILES = FISCAL / "ledger_absolute_2026_09_17/derived/age_profiles.csv"
P_ABS_LIFETIME = FISCAL / "ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv"
P_ABS_WATERFALL = FISCAL / "ledger_absolute_2026_09_17/derived/waterfall.csv"
P_ALLAGE_PROFILES = FISCAL / "all_age_ledger_2026_09_17/derived/age_profiles.csv"
P_SURVIVAL = FISCAL / "lifetime_longevity_sstiming_2026_09_18/derived/survival_tables.csv"
P_FERT = FISCAL / "demo_momentum_2026_09_16/cps_fertility_agestd.csv"
P_CRIME_STOCK = FISCAL / "crime_cost_2026_09_16/crime_cost_by_group.csv"
P_CRIME_FIRSTGEN = FISCAL / "crime_cost_firstgen_2026_09_18/derived/firstgen_cost_weighted.csv"
P_CRIME_FIRSTGEN_AUDIT = FISCAL / "crime_cost_firstgen_2026_09_18/derived/audit.json"
P_STATUS = FISCAL / "status_impute_2026_09_16/RESULT.md"
P_ATTR_BOUNDS = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv"
P_ATTR_FISCAL = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm5_fiscal_implication.csv"
P_PRONATAL = FISCAL / "pronatal_equivalence_2026_09_18/derived/lifetime_equivalence.csv"

ALL_PATHS = [P_ABS_PROFILES, P_ABS_LIFETIME, P_ABS_WATERFALL, P_ALLAGE_PROFILES, P_SURVIVAL,
             P_FERT, P_CRIME_STOCK, P_CRIME_FIRSTGEN, P_CRIME_FIRSTGEN_AUDIT, P_STATUS,
             P_ATTR_BOUNDS, P_ATTR_FISCAL, P_PRONATAL]

# Single-age bands, copied from ledger_absolute_2026_09_17/lifetime.py BANDS so the
# age vector is built exactly as the lane that produced the profiles builds it.
BANDS = ((0, 18), (18, 25), (25, 35), (35, 45), (45, 55), (55, 65), (65, 75), (75, 101))
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
          "mexican_observed_total", "third_plus_nh_white", "all_native"]


def sha256(path: Path) -> str:
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def manifest() -> dict:
    return {str(p.relative_to(FISCAL)): sha256(p) for p in ALL_PATHS}


# ------------------------------------------------------------- fiscal profiles
def age_profiles() -> pd.DataFrame:
    """Per-person net balance by allocation x account x group x band, 2024$/year."""
    df = pd.read_csv(P_ABS_PROFILES)
    need = {"allocation", "account", "group", "band", "population", "net_per_person"}
    if not need.issubset(df.columns):
        raise ValueError("[BLOCKED] absolute-lane age profile schema changed")
    if set(df.allocation) != {"personal", "shared"} or set(df.account) != {"partial", "expanded"}:
        raise ValueError("[BLOCKED] expected both allocations and both account coverages")
    if not set(GROUPS).issubset(set(df.group)):
        raise ValueError("[BLOCKED] missing group in absolute-lane age profiles")
    return df


def age_vector(profiles: pd.DataFrame, group: str, account: str, allocation: str) -> np.ndarray:
    block = profiles[(profiles.group == group) & (profiles.account == account)
                     & (profiles.allocation == allocation)].sort_values("band")
    if block.band.tolist() != list(range(8)):
        raise ValueError(f"[BLOCKED] incomplete profile {allocation}/{account}/{group}")
    out = np.empty(101)
    for (_, row), (lo, hi) in zip(block.iterrows(), BANDS):
        out[lo:hi] = row.net_per_person
    return out


def check_shared_partial_equals_all_age_shared(profiles: pd.DataFrame) -> dict:
    """`shared`/`partial` in the absolute lane must equal the all_age lane's
    `all_age_shared` scenario; the brief names the latter as the main account."""
    other = pd.read_csv(P_ALLAGE_PROFILES)
    other = other[other.scenario == "all_age_shared"]
    maxdiff = 0.0
    for group in ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
                  "mexican_observed_total"]:
        a = age_vector(profiles, group, "partial", "shared")
        b = other[other.target == group].sort_values("band").balance_per_person.to_numpy()
        bb = np.empty(101)
        for value, (lo, hi) in zip(b, BANDS):
            bb[lo:hi] = value
        maxdiff = max(maxdiff, float(np.abs(a - bb).max()))
    return {"check": "shared/partial == all_age_shared", "max_abs_diff_usd": maxdiff,
            "pass": bool(maxdiff < 1e-6)}


def complete_account_addon_is_not_flat(profiles: pd.DataFrame) -> dict:
    """The scratch script added one flat per-person complete-account add-on from
    waterfall.csv. Measure how far from flat the true by-age add-on is."""
    wf = pd.read_csv(P_ABS_WATERFALL)
    final = wf.sort_values("step").groupby("group").cumulative_per_person.last()
    base = wf[wf.step == 0].set_index("group").cumulative_per_person
    flat = (final - base)
    rows = []
    for group in GROUPS:
        if group not in flat.index:
            continue
        gap = age_vector(profiles, group, "expanded", "shared") - age_vector(
            profiles, group, "partial", "shared")
        rows.append({"group": group, "flat_addon_usd": float(flat[group]),
                     "by_age_addon_min_usd": float(gap.min()),
                     "by_age_addon_max_usd": float(gap.max())})
    return {"check": "complete-account add-on flat by age?", "rows": rows}


# -------------------------------------------------------------------- survival
def survival() -> dict[str, pd.DataFrame]:
    df = pd.read_csv(P_SURVIVAL)
    df = df[df.year == 2024]
    out = {}
    for key in ("total", "hispanic", "nh_white"):
        t = df[df.table == key].sort_values("age").reset_index(drop=True)
        if t.age.tolist() != list(range(101)):
            raise ValueError(f"[BLOCKED] life table {key} is not single-year 0..100")
        if abs(t.lx.iloc[0] - 100000) > 1e-6 or (t.lx.diff().dropna() > 0).any():
            raise ValueError(f"[BLOCKED] life table {key} radix/order invalid")
        out[key] = t
    return out


def exposure(table: pd.DataFrame, start_age: int, last_age: int) -> np.ndarray:
    """NVSS Lx is person-years lived in the interval; lx[start] is the radix.
    This is the weighting ledger_absolute_2026_09_17/lifetime.py uses."""
    return table.Lx.to_numpy()[start_age:last_age + 1] / table.lx.iloc[start_age]


# ------------------------------------------------------------------- fertility
WHITE_TFR_2023 = 1.5325   # NVSR Vol. 74 No. 1 "Births: Final Data for 2023", Table 2
                          # (1,532.5 per 1,000 NH white, single race); quoted and gate-
                          # checked in demo_momentum_2026_09_16/RESULT.md gate (b).
MEX_TFR_2010 = 2.256      # NVSR Vol. 61 No. 1, Mexican-origin TFR 2010, via the same lane
WHITE_TFR_2010 = 1.791    # NVSR 74-01 Table 12 / 61-01, NH white 2010 bridged race, same lane

FERT_GROUPS = {"Mexico-born": "mexico_born",
               "Mexican 2nd gen": "mexican_second_gen",
               "Mexican 3rd+ gen": "mexican_third_plus_selfid",
               "NH white 3rd+ gen": "third_plus_nh_white"}


def fertility() -> dict[str, dict]:
    """Two sourced arms. `low_cps2025` rescales the CPS ASEC 2025 own-children-under-5
    age-standardised ratios by the published NH white TFR. `high_nvsr2010` uses the last
    published Mexican-origin / NH white TFR pair (2010). No invented level anywhere."""
    f = pd.read_csv(P_FERT).set_index("group")
    std = {FERT_GROUPS[k]: float(f.loc[k, "age_std"]) for k in FERT_GROUPS}
    white = std["third_plus_nh_white"]
    low = {g: v / white * WHITE_TFR_2023 for g, v in std.items()}
    high = {g: (WHITE_TFR_2010 if g == "third_plus_nh_white" else MEX_TFR_2010)
            for g in std}
    mean_age = mean_age_at_birth(f)
    return {"low_cps2025": low, "high_nvsr2010": high,
            "age_std_own_children": std, "mean_age_at_birth": mean_age}


def mean_age_at_birth(f: pd.DataFrame) -> dict[str, float]:
    """Mean maternal age implied by the own-children-under-5 age-specific rates.
    Births are distributed over mother's age as r_a * n_a; the child is 0-4 at
    observation, so subtract the 2.5-year mean child age to reach age at birth."""
    mid = {"15-19": 17.5, "20-24": 22.5, "25-29": 27.5,
           "30-34": 32.5, "35-39": 37.5, "40-44": 42.5}
    out = {}
    for label, group in FERT_GROUPS.items():
        w = np.array([f.loc[label, f"r_{k}"] * f.loc[label, f"n_{k}"] for k in mid])
        a = np.array(list(mid.values()))
        out[group] = float((a * w).sum() / w.sum() - 2.5)
    return out


# ------------------------------------------------------ unauthorized fiscal penalty
def unauthorized_penalty() -> dict:
    """Level difference, imputed-unauthorized minus Mexico-born pooled, corrected arm,
    per adult 25-64 per year, parsed from the status lane's own result table so the
    number is not retyped."""
    text = P_STATUS.read_text()
    line = [ln for ln in text.splitlines()
            if ln.startswith("| = Taxes − transfers |") and "−9,720" in ln]
    if len(line) != 1:
        raise ValueError("[BLOCKED] status lane corrected-arm row not found or ambiguous")
    cells = [c.strip() for c in line[0].strip("|").split("|")]
    def val(cell: str) -> float:
        body = cell.split("·")[-1].replace("**", "").split("(")[0].strip()
        return float(body.replace("−", "-").replace(",", ""))
    pooled, unauth = val(cells[2]), val(cells[3])
    return {"pooled_mexico_born": pooled, "imputed_unauthorized": unauth,
            "penalty_per_adult_year": unauth - pooled,
            "unit": "2024 USD per adult 25-64 per year, corrected arm (taxes - transfers)",
            "source": "status_impute_2026_09_16/RESULT.md section 3 corrected arm"}


# ------------------------------------------------------------------------ crime
def crime_rates() -> dict:
    """Per adult 25-64 per year, 2024$, national ACS/BJS stock routes; plus the
    Texas arrest-charge status route converted to a per-adult basis with the
    lane's own adult shares."""
    c = pd.read_csv(P_CRIME_STOCK)

    def pick(route: str, arm: str, col: str) -> float:
        row = c[(c.route == route) & (c.arm == arm)]
        if len(row) != 1:
            raise ValueError(f"[BLOCKED] crime row not unique: {route}/{arm}")
        return float(row.iloc[0][col])

    a1 = {  # BJS corrections stock, includes foreign-born; white = usborn+foreign NH white
        "white": {"social": pick("A1_bjs_stock", "+ victim tangible + intangible", "cost_a_per_adult2564"),
                  "tangible": pick("A1_bjs_stock", "+ victim tangible, amortised", "cost_a_per_adult2564"),
                  "corrections": pick("A1_bjs_stock", "corrections only (what the ledger already prices)", "cost_a_per_adult2564")},
        "mexican": {"social": pick("A1_bjs_stock", "+ victim tangible + intangible", "cost_b_per_adult2564"),
                    "tangible": pick("A1_bjs_stock", "+ victim tangible, amortised", "cost_b_per_adult2564"),
                    "corrections": pick("A1_bjs_stock", "corrections only (what the ledger already prices)", "cost_b_per_adult2564")}}
    a2 = {  # ACS institutional stock, US-born only
        "white": {"social": pick("A2_acs_stock", "BASE: tangible + intangible", "cost_a_per_adult2564"),
                  "tangible": pick("A2_acs_stock", "tangible only", "cost_a_per_adult2564"),
                  "corrections": pick("A2_acs_stock", "corrections only, all institutional GQ counted", "cost_a_per_adult2564")},
        "mexican": {"social": pick("A2_acs_stock", "BASE: tangible + intangible", "cost_b_per_adult2564"),
                    "tangible": pick("A2_acs_stock", "tangible only", "cost_b_per_adult2564"),
                    "corrections": pick("A2_acs_stock", "corrections only, all institutional GQ counted", "cost_b_per_adult2564")}}

    fg = pd.read_csv(P_CRIME_FIRSTGEN)
    fg = fg[(fg.denominator == "cms") & (fg.arm == "A")]
    shares = json.loads(P_CRIME_FIRSTGEN_AUDIT.read_text())["cms"]["shares_adult"]

    def status_rate(status: str, share_key: str) -> dict:
        row = fg[fg.status == status].set_index("cost").usd_per_person_year
        s = shares[share_key]
        return {"social": float(row["total"]) / s, "tangible": float(row["tangible"]) / s,
                "corrections": float(row["cjs"]) / s, "adult_share": s}

    status = {"undocumented": status_rate("undocumented", "noncitizen"),
              "foreign_born": status_rate("foreign_born", "foreign_born"),
              "usborn_citizen": status_rate("citizen", "usborn")}
    return {"A1_bjs_stock": a1, "A2_acs_stock": a2, "status_texas_arrests": status}


# -------------------------------------------------------------------- attrition
def attrition() -> dict:
    """Third-plus identification rate and the attriter's retained share of the
    fiscal gap, both read from the population lane."""
    b = pd.read_csv(P_ATTR_BOUNDS)
    central = b[b.assumption == "4th-plus identifies at the measured 3rd-generation rate"]
    if len(central) != 1:
        raise ValueError("[BLOCKED] attrition central bound row not unique")
    ident = float(central.iloc[0].fourth_plus_identification_rate)
    f = pd.read_csv(P_ATTR_FISCAL)
    row = f[(f.population_assumption == "4th-plus identifies at the measured 3rd-generation rate")
            & (f.attriter_characteristics.str.startswith("Duncan-Trejo selectivity"))]
    if len(row) != 1:
        raise ValueError("[BLOCKED] attrition fiscal row not unique")
    row = row.iloc[0]
    retained = float(row.attriter_gap_per_person) / float(row.gap_per_person_before)
    return {"fourth_plus_identification_rate": ident,
            "attriter_share": 1.0 - ident,
            "attriter_gap_per_person": float(row.attriter_gap_per_person),
            "selfid_gap_per_person": float(row.gap_per_person_before),
            "attriter_retained_share_of_gap": retained}
