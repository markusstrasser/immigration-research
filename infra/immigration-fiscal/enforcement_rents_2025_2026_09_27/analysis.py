#!/usr/bin/env python3
"""Did 2025-26 interior enforcement lower rents?  Cross-metro test of the DHS post of 2026-09-25.

The post makes three claims: the rent figures, the premise that inflows raise rents, and the
attribution of the recent declines to enforcement.  This script covers the measurable parts:

* rent growth by metro (Zillow ZORI) for 2023-2026, including the post's metros;
* ICE arrests per 1,000 residents by state and by area of responsibility (Deportation Data
  Project FOIA file), and the Texas share of arrests by month;
* the multifamily supply proxy (Census BPS 5+ unit permits 2021-2023 per 1,000 housing units);
* the brief's regressions (change in rent growth on enforcement, with the supply control, the
  pre-trend and a placebo year), clustered at the level where enforcement varies;
* stacked placebo-differenced estimates, and checks added after the first run (July window,
  supply by period, level contrasts against 2023 and 2024, lost inflow), listed in RESULT.md;
* counterexamples and the magnitude arithmetic.

Inputs are the files ``fetch.py`` puts in ``_cache/`` plus two tracked hand-entered tables
(``brookings_surge_metros.csv``, ``index_readings.csv``).  Outputs go to ``derived/``.  Every
float is written at fixed precision and the bootstrap has a fixed seed, so two runs are
byte-identical.

Run from the repository root::

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/analysis.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"

SEED = 20260927
BOOT_REPS = 9999

# The post's figures, as printed (percent change, sign added: all are declines).
DHS_FIGURES = {
    "San Antonio, TX": -4.8, "Austin, TX": -4.3, "Dallas, TX": -3.0, "Houston, TX": -3.0,
    "Miami, FL": -2.6, "Phoenix, AZ": -4.2, "Atlanta, GA": -3.2, "Nashville, TN": -5.3,
    "New Orleans, LA": -8.0,
}
EXTRA_METROS = ["Denver, CO"]  # the brief's counterexample

MONTHS = {  # label -> ZORI column
    "2022-07": "2022-07-31", "2022-08": "2022-08-31", "2022-12": "2022-12-31",
    "2023-07": "2023-07-31", "2023-08": "2023-08-31", "2023-12": "2023-12-31",
    "2024-07": "2024-07-31", "2024-08": "2024-08-31", "2024-12": "2024-12-31",
    "2025-07": "2025-07-31", "2025-08": "2025-08-31", "2025-12": "2025-12-31",
    "2026-07": "2026-07-31", "2026-08": "2026-08-31",
}

# Arrest windows (inclusive dates) and the population year used as denominator.
WINDOWS = {
    "y2024": ("2024-01-01", "2024-12-31", 2024),
    "y2025": ("2025-01-01", "2025-12-31", 2025),
    "w2526": ("2025-08-01", "2026-07-31", 2025),
}

# CBSA codes that changed between the 2020 delineation (BPS through 2023, ACS 2021) and the
# 2023 delineation (Census V2025 estimates).
CODE_2023_TO_2020 = {"17410": "17460",   # Cleveland, OH <- Cleveland-Elyria, OH
                     "28880": "39100"}   # Kiryas Joel-Poughkeepsie-Newburgh <- Poughkeepsie-Newburgh-Middletown

# Magnitude inputs that are claims or assumptions, kept visible.
DHS_DEPARTURES_CLAIM = 3_000_000   # "more than 3 million ... departed" since 20 Jan 2025 (DHS, Sept 2026)
DHS_DEPARTURES_MONTHS = 20         # 20 Jan 2025 to mid-Sept 2026, rounded
BROOKINGS_MULTIPLIER = 4.0         # employment shortfall / excess arrests, 6 months after a surge
LADDER180_PER_PP = 3.0             # +0.030 log points of rent growth per point of share, x100
SAIZ_ELASTICITY = 1.0              # rent % per 1% of population


# ----------------------------------------------------------------------------------------
# small utilities

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pct(a, b):
    return 100.0 * (a / b - 1.0)


def fmt(x, nd=4):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return ""
    if isinstance(x, (bool, np.bool_)):
        return str(bool(x))
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        v = round(float(x), nd)
        return f"{v:.{nd}f}" if v != 0 else f"{0.0:.{nd}f}"
    return str(x)


def write_csv(path: Path, rows: list[dict], cols: list[str], nd: int = 4) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([fmt(r.get(c), nd) for c in cols])


def norm_city(name: str) -> str:
    name = name.lower().replace(".", "").replace("'", "")
    return re.sub(r"[^a-z ]", " ", name).strip()


def split_cbsa(name: str) -> tuple[list[str], list[str]]:
    """``"Dallas-Fort Worth-Arlington, TX"`` -> (["dallas", "fort worth", "arlington"], ["TX"])."""
    head, _, tail = name.partition(",")
    cities = [re.sub(r"\s+", " ", norm_city(c)) for c in re.split(r"-+|/", head)]
    cities = [c for c in cities if c]
    states = [s.strip().upper() for s in tail.split("-") if s.strip()]
    return cities, states


# ----------------------------------------------------------------------------------------
# Student t and regression helpers (numpy only; scipy is not in the project venv)

def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the regularized incomplete beta (Numerical Recipes 6.4)."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-16:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t: float, df: float) -> float:
    """Two-sided p-value of a Student t statistic."""
    if not math.isfinite(t):
        return float("nan")
    x = df / (df + t * t)
    return betainc(df / 2.0, 0.5, x)


def ols_cluster(y: np.ndarray, X: np.ndarray, groups: np.ndarray) -> dict:
    """OLS with CR1 cluster-robust covariance (Stata's small-sample factor)."""
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    resid = y - X @ beta
    uniq = np.unique(groups)
    g = len(uniq)
    meat = np.zeros((k, k))
    for u in uniq:
        idx = groups == u
        s = X[idx].T @ resid[idx]
        meat += np.outer(s, s)
    factor = (g / (g - 1.0)) * ((n - 1.0) / (n - k))
    V = factor * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.diag(V))
    tss = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / tss if tss > 0 else float("nan")
    return {"beta": beta, "se": se, "resid": resid, "n": n, "g": g, "r2": r2}


WEBB = np.array([-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5)])


def wild_cluster_p(y: np.ndarray, X: np.ndarray, groups: np.ndarray, j: int,
                   rng: np.random.Generator, reps: int = BOOT_REPS, b0: float = 0.0) -> float:
    """Restricted wild-cluster bootstrap p-value for H0: beta_j = b0 (Webb six-point weights)."""
    full = ols_cluster(y, X, groups)
    t_obs = (full["beta"][j] - b0) / full["se"][j]
    Xr = np.delete(X, j, axis=1)
    y0 = y - b0 * X[:, j]
    br = np.linalg.lstsq(Xr, y0, rcond=None)[0]
    fit_r, e_r = Xr @ br + b0 * X[:, j], y0 - Xr @ br
    uniq, inv = np.unique(groups, return_inverse=True)
    n, k = X.shape
    g = len(uniq)
    XtX_inv = np.linalg.inv(X.T @ X)
    factor = (g / (g - 1.0)) * ((n - 1.0) / (n - k))
    count = 0
    for _ in range(reps):
        w = WEBB[rng.integers(0, 6, size=g)][inv]
        ys = fit_r + w * e_r
        b = XtX_inv @ (X.T @ ys)
        r = ys - X @ b
        S = np.zeros((g, k))
        np.add.at(S, inv, X * r[:, None])
        V = factor * XtX_inv @ (S.T @ S) @ XtX_inv
        ts = (b[j] - b0) / math.sqrt(V[j, j])
        if abs(ts) >= abs(t_obs):
            count += 1
    return (count + 1.0) / (reps + 1.0)


def wild_cluster_ci(y: np.ndarray, X: np.ndarray, groups: np.ndarray, j: int, seed: int,
                    reps: int = 4999, alpha: float = 0.05) -> tuple[float, float]:
    """95% interval by inverting the restricted wild-cluster test on a grid of nulls.

    Each grid point reuses the same seed, so the interval is a deterministic function of the data.
    """
    fit = ols_cluster(y, X, groups)
    b, se = float(fit["beta"][j]), float(fit["se"][j])
    grid = b + se * np.arange(-5.0, 5.0001, 0.1)
    keep = [b0 for b0 in grid
            if wild_cluster_p(y, X, groups, j, np.random.default_rng(seed), reps, b0) > alpha]
    return (min(keep), max(keep)) if keep else (float("nan"), float("nan"))


# ----------------------------------------------------------------------------------------
# loaders

def load_zori(fname: str) -> pd.DataFrame:
    z = pd.read_csv(CACHE / "zillow" / fname)
    z = z[z["RegionType"] == "msa"].copy()
    out = z[["RegionID", "SizeRank", "RegionName", "StateName"]].copy()
    for lab, col in MONTHS.items():
        out[f"z_{lab}"] = z[col].astype(float)
    date_cols = [c for c in z.columns if re.fullmatch(r"\d{4}-\d{2}-\d{2}", c)]
    vals = z[date_cols].to_numpy(dtype=float)
    peak_idx = np.nanargmax(np.where(np.isnan(vals), -np.inf, vals), axis=1)
    out["z_peak_month"] = [date_cols[i][:7] for i in peak_idx]
    out["z_peak"] = vals[np.arange(len(vals)), peak_idx]
    out["z_last_month"] = date_cols[-1][:7]
    return out.reset_index(drop=True)


def add_growth(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["g_cal2023"] = pct(d["z_2023-12"], d["z_2022-12"])
    d["g_cal2024"] = pct(d["z_2024-12"], d["z_2023-12"])
    d["g_cal2025"] = pct(d["z_2025-12"], d["z_2024-12"])
    for y in (2023, 2024, 2025, 2026):
        d[f"g_jul{y}"] = pct(d[f"z_{y}-07"], d[f"z_{y - 1}-07"])
    for y in (2023, 2024, 2025, 2026):
        d[f"g_aug{y}"] = pct(d[f"z_{y}-08"], d[f"z_{y - 1}-08"])
    d["dg_cal2025"] = d["g_cal2025"] - d["g_cal2024"]
    d["dg_cal2024"] = d["g_cal2024"] - d["g_cal2023"]
    d["dg_jul2026"] = d["g_jul2026"] - d["g_jul2025"]
    d["dg_jul2025"] = d["g_jul2025"] - d["g_jul2024"]
    d["dg_jul2024"] = d["g_jul2024"] - d["g_jul2023"]
    d["dg_aug2026"] = d["g_aug2026"] - d["g_aug2025"]
    d["dg_aug2025"] = d["g_aug2025"] - d["g_aug2024"]
    d["dg_aug2024"] = d["g_aug2024"] - d["g_aug2023"]
    d["from_peak"] = pct(d["z_2026-08"], d["z_peak"])
    return d


def load_popest() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    p = pd.read_csv(CACHE / "popest" / "cbsa-est2025-alldata.csv", encoding="latin-1",
                    dtype={"CBSA": str, "MDIV": str, "STCOU": str})
    cbsa = p[p["LSAD"] == "Metropolitan Statistical Area"].copy()
    counties = p[p["LSAD"] == "County or equivalent"].copy()
    counties["fips"] = counties["STCOU"].str.zfill(5)
    st = pd.read_csv(CACHE / "popest" / "NST-EST2025-ALLDATA.csv", encoding="latin-1",
                     dtype={"STATE": str})
    st = st[(st["SUMLEV"] == 40)].copy()
    st["STATE"] = st["STATE"].str.zfill(2)
    return cbsa, counties, st


def load_all_counties() -> pd.DataFrame:
    c = pd.read_csv(CACHE / "popest" / "co-est2025-alldata.csv", encoding="latin-1",
                    dtype={"STATE": str, "COUNTY": str})
    c = c[c["SUMLEV"] == 50].copy()
    c["fips"] = c["STATE"].str.zfill(2) + c["COUNTY"].str.zfill(3)
    return c


def parse_bps(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, encoding="latin-1") as f:
        lines = f.read().splitlines()
    for line in lines[2:]:
        if not line.strip():
            continue
        parts = next(csv.reader([line]))
        if len(parts) < 17 or not parts[2].strip().isdigit():
            continue
        units = [float(parts[i] or 0) for i in (6, 9, 12, 15)]
        rows.append({"cbsa": parts[2].strip(), "bps_name": parts[4].strip(),
                     "units_total": sum(units), "units_5plus": units[3]})
    d = pd.DataFrame(rows)
    if d["cbsa"].duplicated().any():
        raise SystemExit(f"[BLOCKED] duplicate CBSA rows in {path.name}")
    return d


def load_supply() -> pd.DataFrame:
    frames = []
    for y in (2021, 2022, 2023):
        b = parse_bps(CACHE / "bps" / f"ma{y}a.txt").set_index("cbsa")
        frames.append(b[["units_total", "units_5plus"]].add_suffix(f"_{y}"))
    names = parse_bps(CACHE / "bps" / "ma2023a.txt").set_index("cbsa")["bps_name"]
    s = pd.concat(frames, axis=1, join="inner").join(names)
    s["permits_5plus_2123"] = s[[f"units_5plus_{y}" for y in (2021, 2022, 2023)]].sum(axis=1)
    s["permits_all_2123"] = s[[f"units_total_{y}" for y in (2021, 2022, 2023)]].sum(axis=1)
    acs = json.loads((CACHE / "acs" / "acs1_2021_cbsa_housing.json").read_text())
    a = pd.DataFrame(acs[1:], columns=acs[0])
    a = a.rename(columns={"metropolitan statistical area/micropolitan statistical area": "cbsa"})
    for c in a.columns:
        if c.startswith("B25"):
            a[c] = pd.to_numeric(a[c], errors="coerce")
    a["hu_2021"] = a["B25001_001E"]
    a["renter_hh_2021"] = a["B25003_003E"]
    a["mf5_stock_2021"] = a[["B25024_006E", "B25024_007E", "B25024_008E", "B25024_009E"]].sum(axis=1)
    s = s.join(a.set_index("cbsa")[["NAME", "hu_2021", "renter_hh_2021", "mf5_stock_2021"]],
               how="left")
    s["supply_mf"] = 1000.0 * s["permits_5plus_2123"] / s["hu_2021"]
    s["supply_all"] = 1000.0 * s["permits_all_2123"] / s["hu_2021"]
    s["supply_mf_per_renter"] = 1000.0 * s["permits_5plus_2123"] / s["renter_hh_2021"]
    return s.reset_index()


def load_arrests() -> pd.DataFrame:
    cols = ["apprehension_date", "apprehension_state_filled_in", "apprehension_aor",
            "apprehension_method_simple", "duplicate_drop_row"]
    d = pq.read_table(CACHE / "ice" / "arrests-latest.parquet", columns=cols).to_pandas()
    d = d[~d["duplicate_drop_row"].astype(bool)].copy()
    d["date"] = pd.to_datetime(d["apprehension_date"])
    d["state"] = d["apprehension_state_filled_in"].str.upper()
    aor = d["apprehension_aor"].str.replace(" Area of Responsibility", "", regex=False)
    d["aor"] = aor.str.replace("St. Paul", "St Paul", regex=False)
    d["at_large"] = d["apprehension_method_simple"].eq("At-Large Arrest")
    return d[["date", "state", "aor", "at_large"]]


def load_aor_counties() -> pd.DataFrame:
    t = pq.read_table(CACHE / "ice" / "ice-aor-county-shp.parquet",
                      columns=["GEOID", "STUSPS", "area_of_responsibility_name"]).to_pandas()
    t = t.rename(columns={"GEOID": "fips", "area_of_responsibility_name": "aor"})
    return t


# ----------------------------------------------------------------------------------------
# matching

def match_zillow(zname: str, cbsa: pd.DataFrame) -> tuple[str | None, str]:
    """Zillow metro name -> one CBSA code (first principal city + state; ambiguity refused)."""
    head, _, tail = zname.partition(",")
    state = tail.strip().upper()
    cands = [norm_city(head), norm_city(head.split("-")[0])]
    for how, pick in (("first-city", lambda cs: cs[:1]), ("any-city", lambda cs: cs)):
        for city in dict.fromkeys(cands):
            hit = cbsa[cbsa["cities"].apply(lambda cs: city in pick(cs))
                       & cbsa["states"].apply(lambda ss: state in ss)]
            if len(hit) == 1:
                return hit.iloc[0]["CBSA"], how
            if len(hit) > 1:
                return None, f"ambiguous-{how}({len(hit)})"
    return None, "no-match"


# ----------------------------------------------------------------------------------------

def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    manifest = json.loads((CACHE / "manifest.json").read_text())
    for rel, meta in manifest.items():
        if sha256(CACHE / rel) != meta["sha256"]:
            raise SystemExit(f"[BLOCKED] {rel} changed since fetch.py recorded it")

    gates: list[dict] = []

    def gate(name: str, ok: bool, detail: str) -> None:
        gates.append({"gate": name, "ok": bool(ok), "detail": detail})
        if not ok:
            print(f"GATE FAIL {name}: {detail}", flush=True)

    # --- populations and geography --------------------------------------------------------
    cbsa, cbsa_counties, states = load_popest()
    cbsa[["cities", "states"]] = cbsa["NAME"].apply(lambda n: pd.Series(split_cbsa(n)))
    all_counties = load_all_counties()
    aor_cty = load_aor_counties()

    state_pop = states.set_index(states["NAME"].str.upper())[
        ["STATE", "POPESTIMATE2024", "POPESTIMATE2025", "INTERNATIONALMIG2024",
         "INTERNATIONALMIG2025", "NPOPCHG_2025"]]
    fips_to_state = dict(zip(states["STATE"], states["NAME"].str.upper()))

    cty = all_counties[["fips", "STATE", "POPESTIMATE2024", "POPESTIMATE2025"]].merge(
        aor_cty[["fips", "aor"]], on="fips", how="left")
    # Counties missing from the AOR file inherit the AOR when their state has only one.
    one_aor = aor_cty.groupby(aor_cty["fips"].str[:2])["aor"].agg(
        lambda s: s.iloc[0] if s.nunique() == 1 else None)
    miss = cty["aor"].isna()
    cty.loc[miss, "aor"] = cty.loc[miss, "STATE"].map(one_aor)
    still = cty["aor"].isna()
    gate("county_aor_coverage", cty.loc[still, "POPESTIMATE2025"].sum() < 0.001 * cty["POPESTIMATE2025"].sum(),
         f"{int(still.sum())} counties without an AOR, population {int(cty.loc[still, 'POPESTIMATE2025'].sum())}")
    cty["state"] = cty["STATE"].map(fips_to_state)

    # --- arrests: state, AOR, monthly Texas share -----------------------------------------
    arr = load_arrests()
    arr_rows, aor_rows = [], []
    rates_state: dict[str, dict[str, float]] = {}
    rates_aor: dict[str, dict[str, float]] = {}
    aor_pop = cty.groupby("aor")[["POPESTIMATE2024", "POPESTIMATE2025"]].sum()
    for wname, (lo, hi, popyr) in WINDOWS.items():
        win = arr[(arr["date"] >= lo) & (arr["date"] <= hi)]
        by_state = win.groupby("state").agg(n=("at_large", "size"), n_at_large=("at_large", "sum"))
        by_aor = win.groupby("aor").agg(n=("at_large", "size"), n_at_large=("at_large", "sum"))
        for sname, r in state_pop.iterrows():
            n = int(by_state["n"].get(sname, 0))
            nl = int(by_state["n_at_large"].get(sname, 0))
            pop = float(r[f"POPESTIMATE{popyr}"])
            rates_state.setdefault(sname, {})[wname] = 1000.0 * n / pop
            rates_state[sname][wname + "_al"] = 1000.0 * nl / pop
            arr_rows.append({"state": sname, "window": wname, "arrests": n, "arrests_at_large": nl,
                             "population": int(pop), "per_1000": 1000.0 * n / pop,
                             "at_large_per_1000": 1000.0 * nl / pop})
        for aname, r in aor_pop.iterrows():
            n = int(by_aor["n"].get(aname, 0))
            nl = int(by_aor["n_at_large"].get(aname, 0))
            pop = float(r[f"POPESTIMATE{popyr}"])
            rates_aor.setdefault(aname, {})[wname] = 1000.0 * n / pop
            rates_aor[aname][wname + "_al"] = 1000.0 * nl / pop
            aor_rows.append({"aor": aname, "window": wname, "arrests": n, "arrests_at_large": nl,
                             "population": int(pop), "per_1000": 1000.0 * n / pop,
                             "at_large_per_1000": 1000.0 * nl / pop})
        known = win["state"].isin(state_pop.index)
        gate(f"state_known_{wname}", known.mean() > 0.9,
             f"{known.mean():.4f} of {len(win)} arrests carry a US state")
        gate(f"aor_known_{wname}", win["aor"].isin(aor_pop.index).mean() > 0.97,
             f"{win['aor'].isin(aor_pop.index).mean():.4f} of arrests carry a mapped AOR")
    for s in rates_state.values():
        s["d2524"] = s["y2025"] - s["y2024"]
    for s in rates_aor.values():
        s["d2524"] = s["y2025"] - s["y2024"]
    write_csv(DERIVED / "state_arrests.csv",
              sorted(arr_rows, key=lambda r: (r["window"], r["state"])),
              ["window", "state", "arrests", "arrests_at_large", "population", "per_1000",
               "at_large_per_1000"])
    write_csv(DERIVED / "aor_arrests.csv", sorted(aor_rows, key=lambda r: (r["window"], r["aor"])),
              ["window", "aor", "arrests", "arrests_at_large", "population", "per_1000",
               "at_large_per_1000"])

    arr["ym"] = arr["date"].dt.strftime("%Y-%m")
    monthly = arr[arr["date"] >= "2024-01-01"].groupby("ym").agg(
        arrests=("state", "size"),
        state_known=("state", lambda s: int(s.isin(state_pop.index).sum())),
        texas=("state", lambda s: int((s == "TEXAS").sum())))
    monthly["texas_share_all"] = monthly["texas"] / monthly["arrests"]
    monthly["texas_share_known"] = monthly["texas"] / monthly["state_known"]
    mrows = [{"month": k, **{c: v for c, v in r.items()}} for k, r in monthly.iterrows()]
    write_csv(DERIVED / "arrests_monthly_texas.csv", mrows,
              ["month", "arrests", "state_known", "texas", "texas_share_all", "texas_share_known"])
    last_full = "2026-07"
    gate("arrests_reach_july_2026", last_full in monthly.index and monthly.loc[last_full, "arrests"] > 1000,
         f"July 2026 arrests {int(monthly.loc[last_full, 'arrests']) if last_full in monthly.index else 0}")

    # --- metro exposure (population-weighted over counties) -------------------------------
    cc = cbsa_counties[["CBSA", "fips", "POPESTIMATE2025"]].merge(
        cty[["fips", "state", "aor"]], on="fips", how="left")
    gate("cbsa_county_state", cc["state"].notna().all(), f"{int(cc['state'].isna().sum())} CBSA counties lack a state")
    expo_rows = []
    for code, grp in cc.groupby("CBSA"):
        w = grp["POPESTIMATE2025"].to_numpy(float)
        row = {"CBSA": code}
        for key in ("y2024", "y2025", "w2526", "d2524", "y2025_al", "w2526_al"):
            vs = np.array([rates_state[s][key] for s in grp["state"]])
            row[f"st_{key}"] = float((w * vs).sum() / w.sum())
            va = np.array([rates_aor.get(a, {}).get(key, np.nan) for a in grp["aor"]])
            ok = np.isfinite(va)
            row[f"aor_{key}"] = float((w[ok] * va[ok]).sum() / w[ok].sum()) if ok.any() else np.nan
        row["cluster_state"] = grp.groupby("state")["POPESTIMATE2025"].sum().idxmax()
        row["cluster_aor"] = grp.groupby("aor")["POPESTIMATE2025"].sum().idxmax()
        row["n_states"] = grp["state"].nunique()
        row["n_aors"] = grp["aor"].nunique()
        expo_rows.append(row)
    expo = pd.DataFrame(expo_rows)

    # --- rents, matching, supply ----------------------------------------------------------
    zori = add_growth(load_zori("Metro_zori_uc_sfrcondomfr_sm_month.csv"))
    zsa = add_growth(load_zori("Metro_zori_uc_sfrcondomfr_sm_sa_month.csv"))
    gate("zori_last_month", zori["z_last_month"].iloc[0] == "2026-08",
         f"ZORI last month {zori['z_last_month'].iloc[0]}")
    matches = [match_zillow(n, cbsa) for n in zori["RegionName"]]
    zori["CBSA"] = [m[0] for m in matches]
    zori["match_how"] = [m[1] for m in matches]
    # A CBSA claimed twice keeps its first-city match; an any-city claimant is a different
    # place with the same name (e.g. Ashland, OH against Huntington-Ashland, WV-KY-OH).
    dupl = zori["CBSA"].notna() & zori["CBSA"].duplicated(keep=False)
    loser = dupl & (zori["match_how"] != "first-city")
    zori.loc[loser, "match_how"] = "dropped-duplicate-any-city"
    zori.loc[loser, "CBSA"] = None
    failures = zori[zori["CBSA"].isna()][["RegionName", "SizeRank", "match_how"]]
    write_csv(DERIVED / "zillow_match_failures.csv", failures.to_dict("records"),
              ["RegionName", "SizeRank", "match_how"])
    dup = zori["CBSA"].dropna().duplicated(keep=False)
    gate("zillow_cbsa_unique", not dup.any(),
         f"{int(dup.sum())} Zillow metros share a CBSA: {sorted(zori.loc[zori['CBSA'].notna() & zori['CBSA'].duplicated(keep=False), 'RegionName'])}")
    for name in list(DHS_FIGURES) + EXTRA_METROS:
        row = zori[zori["RegionName"] == name]
        gate(f"match_{name}", len(row) == 1 and pd.notna(row["CBSA"].iloc[0]),
             f"{name} -> {row['CBSA'].iloc[0] if len(row) else 'missing'}")

    supply = load_supply()
    # Two large CBSAs changed code in the 2023 delineation; permits and ACS 2021 use the old one.
    supply["cbsa"] = supply["cbsa"].map({v: k for k, v in CODE_2023_TO_2020.items()}).fillna(supply["cbsa"])
    # Period-specific supply for a robustness check: 5+ permits two and three years before the growth
    # year (2024 permits come in the 2023 delineation, which the codes above now use).
    p24 = parse_bps(CACHE / "bps" / "cbsa2024a.txt").set_index("cbsa")["units_5plus"]
    supply["units_5plus_2024"] = supply["cbsa"].map(p24)
    for a, b in ((2021, 2022), (2022, 2023), (2023, 2024)):
        supply[f"supply_mf_{a % 100}{b % 100}"] = (1000.0 * (supply[f"units_5plus_{a}"] + supply[f"units_5plus_{b}"])
                                                  / supply["hu_2021"])
    cb = cbsa[["CBSA", "NAME", "POPESTIMATE2023", "POPESTIMATE2024", "POPESTIMATE2025",
               "NPOPCHG2024", "NPOPCHG2025", "INTERNATIONALMIG2024", "INTERNATIONALMIG2025",
               "DOMESTICMIG2024", "DOMESTICMIG2025"]].rename(columns={"NAME": "cbsa_name"})
    panel = zori.merge(cb, on="CBSA", how="inner").merge(expo, on="CBSA", how="left")
    panel = panel.merge(supply[["cbsa", "bps_name", "permits_5plus_2123", "permits_all_2123",
                                "hu_2021", "renter_hh_2021", "supply_mf", "supply_all",
                                "supply_mf_per_renter", "supply_mf_2122", "supply_mf_2223", "supply_mf_2324"]],
                        left_on="CBSA", right_on="cbsa", how="left").drop(columns=["cbsa"])
    panel["pop_growth_2025"] = 100.0 * panel["NPOPCHG2025"] / panel["POPESTIMATE2024"]
    panel["pop_growth_2024"] = 100.0 * panel["NPOPCHG2024"] / panel["POPESTIMATE2023"]
    panel["nim_per_1000_2024"] = 1000.0 * panel["INTERNATIONALMIG2024"] / panel["POPESTIMATE2023"]
    panel["nim_per_1000_2025"] = 1000.0 * panel["INTERNATIONALMIG2025"] / panel["POPESTIMATE2024"]
    panel["nim_drop_per_1000"] = panel["nim_per_1000_2024"] - panel["nim_per_1000_2025"]
    sa = zsa.set_index("RegionName")
    for c in ("g_cal2025", "g_cal2024", "dg_cal2025", "dg_aug2026"):
        panel[f"sa_{c}"] = panel["RegionName"].map(sa[c])

    brk = pd.read_csv(LANE / "brookings_surge_metros.csv", dtype=str)
    brk_key = {(r.metro, r.state) for r in brk.itertuples()}
    heads = panel["cbsa_name"].str.partition(",")
    panel["brookings_surge"] = [(h.strip(), s.strip()) in brk_key for h, s in zip(heads[0], heads[2])]
    matched_brk = {(h.strip(), s.strip()) for h, s, f in zip(heads[0], heads[2], panel["brookings_surge"]) if f}
    unmatched_brk = sorted(brk_key - matched_brk)

    need = ["g_cal2023", "g_cal2024", "g_cal2025", "g_aug2024", "g_aug2025", "g_aug2026",
            "g_jul2023", "g_jul2024", "g_jul2025", "g_jul2026"]
    panel["zori_complete"] = panel[need].notna().all(axis=1)
    panel["has_supply"] = panel["supply_mf"].notna()
    panel = panel.sort_values(["POPESTIMATE2025", "CBSA"], ascending=[False, True]).reset_index(drop=True)

    panel_cols = ["RegionName", "SizeRank", "CBSA", "cbsa_name", "match_how", "POPESTIMATE2025",
                  "cluster_state", "cluster_aor", "n_states", "n_aors",
                  "z_2024-12", "z_2025-12", "z_2026-07", "z_2026-08", "z_peak_month", "z_peak",
                  "from_peak", "g_cal2023", "g_cal2024", "g_cal2025", "g_jul2023", "g_jul2024",
                  "g_jul2025", "g_jul2026", "g_aug2024", "g_aug2025", "g_aug2026", "dg_cal2024",
                  "dg_cal2025", "dg_jul2025", "dg_aug2025", "dg_aug2026",
                  "sa_g_cal2024", "sa_g_cal2025", "sa_dg_cal2025", "sa_dg_aug2026",
                  "st_y2024", "st_y2025", "st_w2526", "st_d2524", "st_y2025_al", "st_w2526_al",
                  "aor_y2024", "aor_y2025", "aor_w2526", "aor_d2524", "aor_y2025_al", "aor_w2526_al",
                  "brookings_surge", "permits_5plus_2123", "permits_all_2123", "hu_2021",
                  "renter_hh_2021", "supply_mf", "supply_all", "supply_mf_per_renter",
                  "supply_mf_2122", "supply_mf_2223", "supply_mf_2324",
                  "pop_growth_2024", "pop_growth_2025", "nim_per_1000_2024", "nim_per_1000_2025",
                  "nim_drop_per_1000", "dg_jul2026", "zori_complete", "has_supply"]
    write_csv(DERIVED / "metro_panel.csv", panel.to_dict("records"), panel_cols)

    # --- samples --------------------------------------------------------------------------
    base = panel[panel["zori_complete"] & panel["has_supply"] & panel["st_y2025"].notna()]
    samples = {
        "main_250k": base[base["POPESTIMATE2025"] >= 250_000],
        "big_500k": base[base["POPESTIMATE2025"] >= 500_000],
        "all_msa": base,
    }
    gate("main_sample_size", len(samples["main_250k"]) >= 100, f"main sample N={len(samples['main_250k'])}")
    dropped_supply = panel[panel["zori_complete"] & ~panel["has_supply"] & (panel["POPESTIMATE2025"] >= 250_000)]
    gate("supply_coverage_main", len(dropped_supply) <= 5,
         f"{len(dropped_supply)} MSAs >=250k with complete ZORI lack supply: {list(dropped_supply['RegionName'])}")
    lack_ps = samples["main_250k"][samples["main_250k"][["supply_mf_2122", "supply_mf_2223", "supply_mf_2324"]]
                                   .isna().any(axis=1)]
    gate("supply_by_period_coverage_main", len(lack_ps) <= 5,
         f"{len(lack_ps)} main-sample MSAs lack a period supply measure: {list(lack_ps['RegionName'])}")

    # --- regressions ----------------------------------------------------------------------
    rng = np.random.default_rng(SEED)
    reg_rows = []

    def run(spec: str, sample: str, d: pd.DataFrame, y: str, treat: str, controls: list[str],
            cluster: str, weight: str | None = None, boot: bool = True) -> dict:
        dd = d.dropna(subset=[y, treat, *controls])
        Y = dd[y].to_numpy(float)
        X = np.column_stack([np.ones(len(dd)), dd[treat].to_numpy(float),
                             *[dd[c].to_numpy(float) for c in controls]])
        G = dd[cluster].to_numpy()
        if weight:
            sw = np.sqrt(dd[weight].to_numpy(float))
            Y, X = Y * sw, X * sw[:, None]
        fit = ols_cluster(Y, X, G)
        b, se = float(fit["beta"][1]), float(fit["se"][1])
        t = b / se
        p = t_two_sided_p(t, fit["g"] - 1)
        pb = wild_cluster_p(Y, X, G, 1, rng) if boot else float("nan")
        row = {"spec": spec, "sample": sample, "outcome": y, "treatment": treat,
               "controls": "+".join(controls) if controls else "none", "cluster": cluster,
               "weight": weight or "none", "coef": b, "se": se, "t": t, "p_t_G-1": p,
               "p_wild_webb": pb, "ci95_lo": b - 1.96 * se, "ci95_hi": b + 1.96 * se,
               "n": fit["n"], "clusters": fit["g"], "r2": fit["r2"],
               "treat_mean": float(dd[treat].mean()), "treat_sd": float(dd[treat].std(ddof=1)),
               "y_mean": float(dd[y].mean())}
        for i, c in enumerate(controls):
            row[f"coef_{c}"] = float(fit["beta"][2 + i])
            row[f"se_{c}"] = float(fit["se"][2 + i])
        reg_rows.append(row)
        return row

    measures = [("st_y2025", "cluster_state"), ("aor_y2025", "cluster_aor"),
                ("st_y2025_al", "cluster_state"), ("st_d2524", "cluster_state"),
                ("brookings_surge", "cluster_state")]
    for sname, d in samples.items():
        d = d.copy()
        d["brookings_surge"] = d["brookings_surge"].astype(float)
        for treat, cl in measures:
            boot = sname == "main_250k" or treat == "st_y2025"
            run("A1", sname, d, "dg_cal2025", treat, [], cl, boot=boot)
            run("A2", sname, d, "dg_cal2025", treat, ["supply_mf"], cl, boot=boot)
            run("A3", sname, d, "dg_cal2025", treat, ["supply_mf", "g_cal2024"], cl, boot=boot)
            run("P1", sname, d, "dg_cal2024", treat, [], cl, boot=boot)
            run("P2", sname, d, "dg_cal2024", treat, ["supply_mf"], cl, boot=boot)
            run("P3", sname, d, "dg_cal2024", treat, ["supply_mf", "g_cal2023"], cl, boot=boot)
        for treat, cl in (("st_w2526", "cluster_state"), ("aor_w2526", "cluster_aor"),
                          ("st_w2526_al", "cluster_state")):
            boot = sname == "main_250k" or treat == "st_w2526"
            run("B1", sname, d, "dg_aug2026", treat, [], cl, boot=boot)
            run("B2", sname, d, "dg_aug2026", treat, ["supply_mf"], cl, boot=boot)
            run("B3", sname, d, "dg_aug2026", treat, ["supply_mf", "g_aug2025"], cl, boot=boot)
            run("L1", sname, d, "g_aug2026", treat, [], cl, boot=boot)
            run("L2", sname, d, "g_aug2026", treat, ["supply_mf"], cl, boot=boot)
            run("L3", sname, d, "g_aug2026", treat, ["supply_mf", "g_aug2025"], cl, boot=boot)
            # placebos for the post's window: the year to August 2024, before the surge
            run("PB1", sname, d, "dg_aug2024", treat, [], cl, boot=boot)
            run("PB2", sname, d, "dg_aug2024", treat, ["supply_mf"], cl, boot=boot)
            run("PB3", sname, d, "dg_aug2024", treat, ["supply_mf", "g_aug2023"], cl, boot=boot)
            run("LP1", sname, d, "g_aug2024", treat, [], cl, boot=boot)
            run("LP2", sname, d, "g_aug2024", treat, ["supply_mf"], cl, boot=boot)
    m = samples["main_250k"].copy()
    run("A3w", "main_250k", m, "dg_cal2025", "st_y2025", ["supply_mf", "g_cal2024"], "cluster_state",
        weight="POPESTIMATE2025")
    run("B3w", "main_250k", m, "dg_aug2026", "st_w2526", ["supply_mf", "g_aug2025"], "cluster_state",
        weight="POPESTIMATE2025")
    run("A3sa", "main_250k", m, "sa_dg_cal2025", "st_y2025", ["supply_mf", "sa_g_cal2024"], "cluster_state")
    run("A3jul", "main_250k", m, "dg_jul2025", "st_y2025", ["supply_mf", "g_jul2024"], "cluster_state")
    run("P3jul", "main_250k", m, "dg_jul2024", "st_y2025", ["supply_mf", "g_jul2023"], "cluster_state")
    run("A3all", "main_250k", m, "dg_cal2025", "st_y2025", ["supply_all", "g_cal2024"], "cluster_state")
    run("A3pop", "main_250k", m, "dg_cal2025", "st_y2025", ["supply_mf", "g_cal2024", "pop_growth_2024"],
        "cluster_state")

    # Placebo-differenced estimate: stack the pre year and the post year for every metro and
    # let every slope differ by period.  The enforcement x post coefficient is the change in
    # the enforcement gradient between the placebo year and the treated year.  A lag of None
    # stacks growth levels with no lagged-growth control.
    def stacked(spec: str, sample: str, d: pd.DataFrame, pre: tuple[str, str], post: tuple[str, str],
                treat: str, cluster: str, boot: bool = True, ci: bool = False,
                supply: tuple[str, str] = ("supply_mf", "supply_mf")) -> dict:
        (y0, lag0), (y1, lag1) = pre, post
        s0, s1 = supply   # supply measure for the placebo-year rows and the treated-year rows
        dd = d.dropna(subset=[c for c in (y0, lag0, y1, lag1, treat, s0, s1) if c])
        long = pd.concat([
            pd.DataFrame({"y": dd[y0], "lag": dd[lag0] if lag0 else 0.0, "post": 0.0}),
            pd.DataFrame({"y": dd[y1], "lag": dd[lag1] if lag1 else 0.0, "post": 1.0})])
        e = pd.concat([dd[treat], dd[treat]]).to_numpy(float)
        s = pd.concat([dd[s0], dd[s1]]).to_numpy(float)
        g = pd.concat([dd[cluster], dd[cluster]]).to_numpy()
        post_ = long["post"].to_numpy(float)
        lag = long["lag"].to_numpy(float)
        cols = [np.ones(len(long)), e * post_, post_, e, s, s * post_] + ([lag, lag * post_] if lag0 else [])
        X = np.column_stack(cols)
        Y = long["y"].to_numpy(float)
        fit = ols_cluster(Y, X, g)
        b, se = float(fit["beta"][1]), float(fit["se"][1])
        pb = wild_cluster_p(Y, X, g, 1, rng) if boot else float("nan")
        row = {"spec": spec, "sample": sample, "outcome": f"{y0}->{y1}", "treatment": f"{treat}_x_post",
               "controls": (("post+treat+supply_mf(x post)" if s0 == s1 else f"post+treat+{s0}/{s1} by period(x post)")
                            + ("+lagged growth(x post)" if lag0 else ", growth levels")), "cluster": cluster,
               "weight": "none", "coef": b, "se": se, "t": b / se,
               "p_t_G-1": t_two_sided_p(b / se, fit["g"] - 1), "p_wild_webb": pb,
               "ci95_lo": b - 1.96 * se, "ci95_hi": b + 1.96 * se, "n": fit["n"], "clusters": fit["g"],
               "r2": fit["r2"], "treat_mean": float(dd[treat].mean()), "treat_sd": float(dd[treat].std(ddof=1)),
               "y_mean": float(dd[y1].mean()), "coef_pre_gradient": float(fit["beta"][3]),
               "se_pre_gradient": float(fit["se"][3])}
        # the other slopes: supply and lagged growth in the pre period, and their changes
        for i, name in ((2, "post"), (4, "supply_mf"), (5, "supply_x_post"), (6, "lag"), (7, "lag_x_post")):
            if i < X.shape[1]:
                row[f"coef_{name}"], row[f"se_{name}"] = float(fit["beta"][i]), float(fit["se"][i])
        if ci:
            row["wild_ci_lo"], row["wild_ci_hi"] = wild_cluster_ci(Y, X, g, 1, SEED)
        reg_rows.append(row)
        return row

    cal = (("dg_cal2024", "g_cal2023"), ("dg_cal2025", "g_cal2024"))
    aug = (("dg_aug2024", "g_aug2023"), ("dg_aug2026", "g_aug2025"))
    no_tx = samples["main_250k"][samples["main_250k"]["cluster_state"] != "TEXAS"]
    samples_x = {"main_250k": samples["main_250k"], "big_500k": samples["big_500k"],
                 "all_msa": samples["all_msa"], "main_no_texas": no_tx}
    for sname, d in samples_x.items():
        boot = sname in ("main_250k", "main_no_texas")
        ci = sname == "main_250k"
        stacked("S_A", sname, d, *cal, "st_y2025", "cluster_state", boot=boot, ci=ci)
        stacked("S_B", sname, d, *aug, "st_w2526", "cluster_state", boot=boot, ci=ci)
        stacked("S_A", sname, d, *cal, "aor_y2025", "cluster_aor", boot=boot)
        stacked("S_B", sname, d, *aug, "aor_w2526", "cluster_aor", boot=boot)
        stacked("S_A", sname, d.assign(brookings_surge=d["brookings_surge"].astype(float)), *cal,
                "brookings_surge", "cluster_state", boot=boot)
    for spec, y, treat, ctl in (("A3", "dg_cal2025", "st_y2025", ["supply_mf", "g_cal2024"]),
                                ("P3", "dg_cal2024", "st_y2025", ["supply_mf", "g_cal2023"]),
                                ("B3", "dg_aug2026", "st_w2526", ["supply_mf", "g_aug2025"]),
                                ("PB3", "dg_aug2024", "st_w2526", ["supply_mf", "g_aug2023"]),
                                ("L1", "g_aug2026", "st_w2526", []),
                                ("LP1", "g_aug2024", "st_w2526", [])):
        run(spec, "main_no_texas", no_tx, y, treat, ctl, "cluster_state")
    # Leave one state out: the range of the placebo-differenced gradient.
    loso_rows = []
    main = samples["main_250k"]
    for st_name in sorted(main["cluster_state"].unique()):
        sub = main[main["cluster_state"] != st_name]
        before = len(reg_rows)
        ra = stacked("S_A", f"loso_{st_name}", sub, *cal, "st_y2025", "cluster_state", boot=False)
        rb = stacked("S_B", f"loso_{st_name}", sub, *aug, "st_w2526", "cluster_state", boot=False)
        del reg_rows[before:]
        loso_rows.append({"dropped_state": st_name, "n": ra["n"] // 2, "S_A_coef": ra["coef"],
                          "S_A_se": ra["se"], "S_B_coef": rb["coef"], "S_B_se": rb["se"]})
    write_csv(DERIVED / "leave_one_state_out.csv", loso_rows,
              ["dropped_state", "n", "S_A_coef", "S_A_se", "S_B_coef", "S_B_se"])

    # Added after the first full run, below every earlier bootstrap so those draws are unchanged.
    # The post's own month: Test B on year-over-year growth to July 2026.
    run("B3jul", "main_250k", m, "dg_jul2026", "st_w2526", ["supply_mf", "g_jul2025"], "cluster_state")
    run("PB3jul", "main_250k", m, "dg_jul2024", "st_w2526", ["supply_mf", "g_jul2023"], "cluster_state")
    run("L1jul", "main_250k", m, "g_jul2026", "st_w2526", [], "cluster_state")
    run("LP1jul", "main_250k", m, "g_jul2024", "st_w2526", [], "cluster_state")
    stacked("S_Bjul", "main_250k", m, ("dg_jul2024", "g_jul2023"), ("dg_jul2026", "g_jul2025"),
            "st_w2526", "cluster_state", ci=True)
    # Placebos for the population-weighted checks A3w and B3w.
    run("P3w", "main_250k", m, "dg_cal2024", "st_y2025", ["supply_mf", "g_cal2023"], "cluster_state",
        weight="POPESTIMATE2025")
    run("PB3w", "main_250k", m, "dg_aug2024", "st_w2526", ["supply_mf", "g_aug2023"], "cluster_state",
        weight="POPESTIMATE2025")
    # Lost inflow in place of arrests: the fall in Census net international migration per 1,000
    # residents, V2025 year (to June 2025) against V2024 year.  Census allocates NIM to counties
    # from ACS patterns, so this is an exposure measure, not a locally counted flow.  A larger
    # fall should lower rent growth: the sign test is a negative coefficient.
    for spec, y, ctl in (("N1", "dg_cal2025", []), ("N3", "dg_cal2025", ["supply_mf", "g_cal2024"]),
                         ("NP1", "dg_cal2024", []), ("NP3", "dg_cal2024", ["supply_mf", "g_cal2023"])):
        run(spec, "main_250k", m, y, "nim_drop_per_1000", ctl, "cluster_state")
    stacked("S_N", "main_250k", m, *cal, "nim_drop_per_1000", "cluster_state", ci=True)
    # Supply by period instead of one 2021-23 proxy: permits 2021-22 for the placebo years (2024),
    # 2022-23 for calendar 2025 and 2023-24 for the year to August 2026.
    stacked("S_A_ps", "main_250k", m, *cal, "st_y2025", "cluster_state", ci=True,
            supply=("supply_mf_2122", "supply_mf_2223"))
    stacked("S_B_ps", "main_250k", m, *aug, "st_w2526", "cluster_state", ci=True,
            supply=("supply_mf_2122", "supply_mf_2324"))
    # The level gradient in the year to August 2023, before the border inflow began to fall
    # (mid-2024), so no part of the placebo year overlaps it.
    run("LP0", "main_250k", m, "g_aug2023", "st_w2526", [], "cluster_state")
    run("LP0s", "main_250k", m, "g_aug2023", "st_w2526", ["supply_mf"], "cluster_state")
    # The same as a stacked difference in growth levels, against the year to August 2023 and,
    # for comparison, against the year to August 2024.
    stacked("S_L23", "main_250k", m, ("g_aug2023", None), ("g_aug2026", None), "st_w2526", "cluster_state", ci=True)
    stacked("S_L24", "main_250k", m, ("g_aug2024", None), ("g_aug2026", None), "st_w2526", "cluster_state", ci=True)

    reg_cols = ["spec", "sample", "outcome", "treatment", "controls", "cluster", "weight", "coef",
                "se", "t", "p_t_G-1", "p_wild_webb", "ci95_lo", "ci95_hi", "n", "clusters", "r2",
                "treat_mean", "treat_sd", "y_mean", "coef_supply_mf", "se_supply_mf",
                "coef_g_cal2024", "se_g_cal2024", "coef_g_aug2025", "se_g_aug2025",
                "coef_g_cal2023", "se_g_cal2023", "coef_g_aug2023", "se_g_aug2023",
                "coef_pre_gradient", "se_pre_gradient", "wild_ci_lo", "wild_ci_hi",
                "coef_g_jul2023", "se_g_jul2023", "coef_g_jul2024", "se_g_jul2024",
                "coef_g_jul2025", "se_g_jul2025", "coef_sa_g_cal2024", "se_sa_g_cal2024",
                "coef_supply_all", "se_supply_all", "coef_pop_growth_2024", "se_pop_growth_2024",
                "coef_post", "se_post", "coef_supply_x_post", "se_supply_x_post",
                "coef_lag", "se_lag", "coef_lag_x_post", "se_lag_x_post"]
    write_csv(DERIVED / "regressions.csv", reg_rows, reg_cols)

    # --- supply's explanatory power -------------------------------------------------------
    r2_rows = []
    d = samples["main_250k"]
    d = d.assign(g_cum_2225=pct(d["z_2025-12"], d["z_2022-12"]))
    for y in ("g_cal2023", "g_cal2024", "g_cal2025", "g_aug2024", "g_aug2026", "g_cum_2225",
              "dg_cal2025", "dg_aug2026"):
        for xs in (["supply_mf"], ["st_y2025"], ["supply_mf", "st_y2025"], ["st_w2526"],
                   ["supply_mf", "st_w2526"]):
            dd = d.dropna(subset=[y, *xs])
            X = np.column_stack([np.ones(len(dd)), *[dd[c].to_numpy(float) for c in xs]])
            fit = ols_cluster(dd[y].to_numpy(float), X, dd["cluster_state"].to_numpy())
            row = {"outcome": y, "regressors": "+".join(xs), "n": fit["n"], "r2": fit["r2"]}
            for i, c in enumerate(xs):
                key = "supply" if c.startswith("supply") else "enforcement"
                row[f"coef_{key}"] = float(fit["beta"][1 + i])
                row[f"se_{key}"] = float(fit["se"][1 + i])
            r2_rows.append(row)
    write_csv(DERIVED / "supply_r2.csv", r2_rows,
              ["outcome", "regressors", "n", "r2", "coef_supply", "se_supply", "coef_enforcement",
               "se_enforcement"])

    # --- the post's metros ----------------------------------------------------------------
    dhs_rows = []
    for name in list(DHS_FIGURES) + EXTRA_METROS:
        r = panel[panel["RegionName"] == name].iloc[0]
        dhs_rows.append({"metro": name, "dhs_figure": DHS_FIGURES.get(name, float("nan")),
                         "cbsa_name": r["cbsa_name"], "zori_yoy_2026_08": r["g_aug2026"],
                         "zori_yoy_2026_07": r["g_jul2026"], "zori_yoy_2025_07": r["g_jul2025"],
                         "zori_yoy_2024_07": r["g_jul2024"], "zori_yoy_2023_07": r["g_jul2023"],
                         "zori_cal2023": r["g_cal2023"], "zori_cal2024": r["g_cal2024"],
                         "zori_cal2025": r["g_cal2025"], "zori_peak_month": r["z_peak_month"],
                         "zori_from_peak_2026_08": r["from_peak"], "supply_mf": r["supply_mf"],
                         "supply_mf_rank_main": int((samples["main_250k"]["supply_mf"] > r["supply_mf"]).sum() + 1),
                         "st_y2024": r["st_y2024"], "st_y2025": r["st_y2025"], "st_w2526": r["st_w2526"],
                         "aor": r["cluster_aor"], "aor_y2025": r["aor_y2025"], "aor_w2526": r["aor_w2526"],
                         "brookings_surge": r["brookings_surge"], "pop_growth_2024": r["pop_growth_2024"],
                         "pop_growth_2025": r["pop_growth_2025"], "nim_per_1000_2024": r["nim_per_1000_2024"],
                         "nim_per_1000_2025": r["nim_per_1000_2025"]})
    dhs_cols = list(dhs_rows[0].keys())
    write_csv(DERIVED / "dhs_metros.csv", dhs_rows, dhs_cols)

    # --- the Texas gap by year: Texas metros against the rest of the main sample -----------
    d = samples["main_250k"]
    is_tx = d["cluster_state"] == "TEXAS"
    gap_rows = []
    for c in ("g_cal2023", "g_cal2024", "g_cal2025", "g_jul2023", "g_jul2024", "g_jul2025", "g_jul2026",
              "g_aug2023", "g_aug2024", "g_aug2025", "g_aug2026"):
        rk = d[c].rank(method="min")
        row = {"growth": c, "texas_n": int(is_tx.sum()), "texas_mean": float(d.loc[is_tx, c].mean()),
               "rest_n": int((~is_tx).sum()), "rest_mean": float(d.loc[~is_tx, c].mean()),
               "gap": float(d.loc[is_tx, c].mean() - d.loc[~is_tx, c].mean()), "of_n": int(len(d))}
        for name in ("San Antonio, TX", "Austin, TX", "Dallas, TX", "Houston, TX"):
            row["rank_" + name.split(",")[0].lower().replace(" ", "_")] = int(rk[d["RegionName"] == name].iloc[0])
        gap_rows.append(row)
    write_csv(DERIVED / "texas_gap.csv", gap_rows, list(gap_rows[0].keys()))

    # --- published index readings next to the post and ZORI --------------------------------
    idx = pd.read_csv(LANE / "index_readings.csv")
    for r in idx[idx["source"] == "Zillow report"].itertuples():
        mine = float(panel.loc[panel["RegionName"] == r.metro, "g_aug2026"].iloc[0])
        gate(f"zori_matches_zillow_report_{r.metro}", abs(mine - r.value) <= 0.051,
             f"computed {mine:.3f} vs published {r.value}")
    own = []
    for name in DHS_FIGURES:
        r = panel[panel["RegionName"] == name].iloc[0]
        for lab, col in (("2026-08", "g_aug2026"), ("2026-07", "g_jul2026")):
            own.append({"metro": name, "source": "Zillow ZORI (this lane)", "geography": "metro",
                        "month": lab, "measure": "ZORI all homes YoY", "value": float(r[col]),
                        "url": "derived/metro_panel.csv"})
    idx = pd.concat([idx[idx["source"] != "Zillow report"], pd.DataFrame(own)], ignore_index=True)
    idx["dhs_figure"] = idx["metro"].map(DHS_FIGURES)
    idx["abs_gap_to_dhs"] = (idx["value"] - idx["dhs_figure"]).abs()
    src_rows = idx.sort_values(["metro", "abs_gap_to_dhs", "source"]).to_dict("records")
    write_csv(DERIVED / "source_check.csv", src_rows,
              ["metro", "dhs_figure", "source", "geography", "month", "measure", "value",
               "abs_gap_to_dhs", "url"], nd=2)
    exact = idx[idx["abs_gap_to_dhs"] <= 0.051]
    per_source = idx.groupby("source").apply(
        lambda g: pd.Series({"readings": len(g),
                             "within_0p15": int((g["abs_gap_to_dhs"] <= 0.15).sum()),
                             "within_0p5": int((g["abs_gap_to_dhs"] <= 0.5).sum())}),
        include_groups=False)

    # --- counterexamples: high-supply metros by enforcement tercile ------------------------
    d = samples["main_250k"].copy()
    q80 = d["supply_mf"].quantile(0.8)
    terc = d["st_y2025"].quantile([1 / 3, 2 / 3]).to_numpy()
    d["enf_tercile"] = np.where(d["st_y2025"] <= terc[0], "low",
                                np.where(d["st_y2025"] <= terc[1], "mid", "high"))
    hs = d[d["supply_mf"] >= q80]
    ce_rows = []
    for _, r in hs.sort_values(["enf_tercile", "supply_mf"], ascending=[True, False]).iterrows():
        ce_rows.append({"metro": r["RegionName"], "state": r["cluster_state"], "enf_tercile": r["enf_tercile"],
                        "st_y2025": r["st_y2025"], "supply_mf": r["supply_mf"], "g_cal2024": r["g_cal2024"],
                        "g_cal2025": r["g_cal2025"], "g_aug2026": r["g_aug2026"],
                        "dg_cal2025": r["dg_cal2025"], "dg_aug2026": r["dg_aug2026"],
                        "from_peak": r["from_peak"], "zori_peak_month": r["z_peak_month"]})
    write_csv(DERIVED / "counterexamples.csv", ce_rows, list(ce_rows[0].keys()))
    grp = hs.groupby("enf_tercile")[["g_cal2024", "g_cal2025", "g_aug2026", "dg_cal2025", "dg_aug2026",
                                     "supply_mf", "st_y2025"]].mean()
    grp_n = hs.groupby("enf_tercile").size()
    ce_summary = [{"enf_tercile": k, "n": int(grp_n[k]), **{c: float(v) for c, v in r.items()}}
                  for k, r in grp.iterrows()]
    write_csv(DERIVED / "counterexamples_summary.csv", ce_summary,
              ["enf_tercile", "n", "supply_mf", "st_y2025", "g_cal2024", "g_cal2025", "g_aug2026",
               "dg_cal2025", "dg_aug2026"])

    # --- magnitude --------------------------------------------------------------------------
    # National rates cover the 50 states and DC: the state file also carries Puerto Rico.
    us50 = states[states["STATE"] != "72"]
    us = us50["POPESTIMATE2025"].sum()
    tx = state_pop.loc["TEXAS"]
    nat = {}
    for w, (lo, hi, _) in WINDOWS.items():
        win = arr[(arr["date"] >= lo) & (arr["date"] <= hi)]
        nat[w] = {"us": int(len(win)), "tx": int((win["state"] == "TEXAS").sum()),
                  "pr": int((win["state"] == "PUERTO RICO").sum())}
    tx_metros = ["San Antonio, TX", "Austin, TX", "Dallas, TX", "Houston, TX"]
    txm = panel[panel["RegionName"].isin(tx_metros)]
    txm_pop = float(txm["POPESTIMATE2025"].sum())
    txm_nim24 = float(txm["INTERNATIONALMIG2024"].sum())
    txm_nim25 = float(txm["INTERNATIONALMIG2025"].sum())
    txm_zori_aug26 = {r.RegionName: float(r.g_aug2026) for r in txm.itertuples()}
    us_nim24 = float(us50["INTERNATIONALMIG2024"].sum())
    us_nim25 = float(us50["INTERNATIONALMIG2025"].sum())
    tx_rate = 100.0 * nat["w2526"]["tx"] / float(tx["POPESTIMATE2025"])       # % of population
    us_rate = 100.0 * (nat["w2526"]["us"] - nat["w2526"]["pr"]) / float(us)
    st_w = pd.Series({s: v["w2526"] for s, v in rates_state.items() if s != "PUERTO RICO"})
    median_state_rate = 100.0 * float(st_w.median()) / 1000.0
    tx_share_w = nat["w2526"]["tx"] / nat["w2526"]["us"]
    dhs_dep_year = DHS_DEPARTURES_CLAIM * 12.0 / DHS_DEPARTURES_MONTHS
    scen = [
        ("arrests_only", "every Texas arrest Aug 2025-Jul 2026 removes one resident", tx_rate),
        ("arrests_x4", "each arrest carries four departures (Brookings employment ratio)",
         BROOKINGS_MULTIPLIER * tx_rate),
        ("dhs_departures_by_arrest_share",
         "DHS's own 3M+ departures claim, annualised, allocated to Texas by its arrest share",
         100.0 * dhs_dep_year * tx_share_w / float(tx["POPESTIMATE2025"])),
        ("texas_over_median_state", "Texas arrest rate minus the median state's (what a cross-state test sees)",
         tx_rate - median_state_rate),
        ("lost_inflow_texas_v2025", "fall in Texas net international migration, V2025 year vs V2024 year",
         100.0 * (float(tx["INTERNATIONALMIG2024"]) - float(tx["INTERNATIONALMIG2025"])) / float(tx["POPESTIMATE2024"])),
        ("lost_inflow_us_v2025", "fall in US net international migration, V2025 year vs V2024 year",
         100.0 * (us_nim24 - us_nim25) / float(us50["POPESTIMATE2024"].sum())),
        ("lost_inflow_tx_metros_v2025", "fall in net international migration, four Texas metros",
         100.0 * (txm_nim24 - txm_nim25) / float(txm["POPESTIMATE2024"].sum())),
    ]
    mag_rows = []
    for key, desc, pop_pct in scen:
        mag_rows.append({"scenario": key, "description": desc, "population_change_pct": -pop_pct,
                         "rent_pct_saiz_1": -SAIZ_ELASTICITY * pop_pct,
                         "rent_pct_ladder180_3": -LADDER180_PER_PP * pop_pct})
    write_csv(DERIVED / "magnitude.csv", mag_rows,
              ["scenario", "description", "population_change_pct", "rent_pct_saiz_1", "rent_pct_ladder180_3"])

    # Gradients in the regressions' units: percentage points of annual rent growth per extra
    # ICE arrest per 1,000 residents (one arrest per 1,000 residents is 0.1% of the population).
    tx_gap = 10.0 * tx_rate - float(st_w.median())            # arrests per 1,000 above the median state
    dhs_tx = float(np.mean([DHS_FIGURES[n] for n in tx_metros]))
    zori_tx = float(np.mean([txm_zori_aug26[n] for n in tx_metros]))
    zori_rest = float(samples["main_250k"].loc[samples["main_250k"]["cluster_state"] != "TEXAS",
                                               "g_aug2026"].mean())
    grad_rows = [
        {"gradient": "mechanical, Saiz elasticity 1", "pp_per_arrest_per_1000": -0.1 * SAIZ_ELASTICITY},
        {"gradient": "four departures per arrest, Saiz elasticity 1",
         "pp_per_arrest_per_1000": -0.1 * SAIZ_ELASTICITY * BROOKINGS_MULTIPLIER},
        {"gradient": "mechanical, ladder 180 association", "pp_per_arrest_per_1000": -0.1 * LADDER180_PER_PP},
        {"gradient": "four departures per arrest, ladder 180 association",
         "pp_per_arrest_per_1000": -0.1 * LADDER180_PER_PP * BROOKINGS_MULTIPLIER},
        {"gradient": "post's Texas figures, all attributed to Texas's extra arrests",
         "pp_per_arrest_per_1000": dhs_tx / tx_gap},
        {"gradient": "ZORI Texas metros minus other main-sample metros, per extra arrest",
         "pp_per_arrest_per_1000": (zori_tx - zori_rest) / tx_gap},
    ]
    for r in reg_rows:
        if r["sample"] == "main_250k" and r["spec"] in ("S_A", "S_B") and r["treatment"] in (
                "st_y2025_x_post", "st_w2526_x_post"):
            grad_rows.append({"gradient": f"estimated {r['spec']} ({r['outcome']})",
                              "pp_per_arrest_per_1000": r["coef"], "se": r["se"],
                              "wild_ci_lo": r.get("wild_ci_lo"), "wild_ci_hi": r.get("wild_ci_hi")})
    write_csv(DERIVED / "implied_gradients.csv", grad_rows,
              ["gradient", "pp_per_arrest_per_1000", "se", "wild_ci_lo", "wild_ci_hi"])

    # --- summary ----------------------------------------------------------------------------
    def pick(spec, sample, treat):
        for r in reg_rows:
            if r["spec"] == spec and r["sample"] == sample and r["treatment"] == treat:
                return {k: r[k] for k in ("coef", "se", "p_t_G-1", "p_wild_webb", "n", "clusters", "r2")}
        return None

    summary = {
        "zori_last_month": zori["z_last_month"].iloc[0],
        "arrests_last_date": str(arr["date"].max().date()),
        "texas_share_july_2026": float(monthly.loc["2026-07", "texas_share_all"]),
        "texas_share_july_2025": float(monthly.loc["2025-07", "texas_share_all"]),
        "texas_share_2024_mean_monthly": float(monthly.loc["2024-01":"2024-12", "texas_share_all"].mean()),
        "arrests_by_window": nat,
        "texas_arrest_rate_w2526_per_1000": 10.0 * tx_rate,
        "us_arrest_rate_w2526_per_1000": 10.0 * us_rate,
        "median_state_rate_w2526_per_1000": float(st_w.median()),
        "median_state_rate_y2025_per_1000": float(np.median(
            [v["y2025"] for s, v in rates_state.items() if s != "PUERTO RICO"])),
        "us_nim_2024": us_nim24, "us_nim_2025": us_nim25,
        "texas_nim_2024": float(tx["INTERNATIONALMIG2024"]), "texas_nim_2025": float(tx["INTERNATIONALMIG2025"]),
        "texas_popchg_2025": float(tx["NPOPCHG_2025"]),
        "tx_metros_pop_2025": txm_pop, "tx_metros_nim_2024": txm_nim24, "tx_metros_nim_2025": txm_nim25,
        "tx_metros_zori_yoy_2026_08": txm_zori_aug26,
        "samples": {k: int(len(v)) for k, v in samples.items()},
        "main_A1": pick("A1", "main_250k", "st_y2025"), "main_A2": pick("A2", "main_250k", "st_y2025"),
        "main_A3": pick("A3", "main_250k", "st_y2025"), "main_P3": pick("P3", "main_250k", "st_y2025"),
        "main_A3_aor": pick("A3", "main_250k", "aor_y2025"), "main_P3_aor": pick("P3", "main_250k", "aor_y2025"),
        "main_B3": pick("B3", "main_250k", "st_w2526"), "main_L1": pick("L1", "main_250k", "st_w2526"),
        "main_L3": pick("L3", "main_250k", "st_w2526"),
        "main_B3jul": pick("B3jul", "main_250k", "st_w2526"),
        "main_PB3jul": pick("PB3jul", "main_250k", "st_w2526"),
        "main_S_Bjul": pick("S_Bjul", "main_250k", "st_w2526_x_post"),
        "main_N3": pick("N3", "main_250k", "nim_drop_per_1000"),
        "main_NP3": pick("NP3", "main_250k", "nim_drop_per_1000"),
        "main_S_N": pick("S_N", "main_250k", "nim_drop_per_1000_x_post"),
        "main_S_A_ps": pick("S_A_ps", "main_250k", "st_y2025_x_post"),
        "main_S_B_ps": pick("S_B_ps", "main_250k", "st_w2526_x_post"),
        "source_exact_matches": int(len(exact)),
        "source_agreement": {k: {c: int(v) for c, v in r.items()} for k, r in per_source.iterrows()},
        "brookings_unmatched": [f"{a}, {b}" for a, b in unmatched_brk],
        "zillow_match_failures": int(len(failures)),
        "gates_failed": [g["gate"] for g in gates if not g["ok"]],
        "inputs": {rel: meta["sha256"] for rel, meta in sorted(manifest.items())},
        "tracked_inputs": {p.name: sha256(p) for p in (LANE / "brookings_surge_metros.csv",
                                                      LANE / "index_readings.csv")},
    }
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True,
                                                     default=lambda o: round(float(o), 6)) + "\n")
    write_csv(DERIVED / "gates.csv", gates, ["gate", "ok", "detail"])
    failed = [g["gate"] for g in gates if not g["ok"]]
    print(f"gates: {len(gates) - len(failed)}/{len(gates)} pass" + (f"; FAILED {failed}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
