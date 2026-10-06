"""Did the 2025 immigration-enforcement drive lower Mexican-origin identification among the CPS third generation?

Hadah and Denteh (April 2026) find that Secure Communities lowered parent-reported Hispanic identity of
third-generation White children of Latin-American heritage by 5.9 pp (CPS 2004-13). The account (income year 2024)
runs on the CPS ASEC 2025, fielded February-April 2025. This lane tests whether reported Mexican origin among
third-generation (G3) people fell from February 2025.

Data: stage.py's lineage households, from the pooled lane's IPUMS-CPS extracts: basic monthly MIS 1 and 5,
January 2003 - August 2026 (October 2025 was not fielded), and the ASEC 2003-2026.

Groups: analyze.classify of g3_identity_pooled_2026_10_05, imported read-only. G3 = US-born, both own parents
US-born, civilian, every linked co-resident parent US-born, and a Mexico-born grandparent read from a linked parent's
MBPL/FBPL, at any age; children under 18 are the Hadah-Denteh frame. Identifiers report a Mexican HISPAN code.
Comparison groups use the same rule with the lineage birthplaces recoded before classify: G3 with an Asia-born
grandparent and no Latin American one (outcome: an Asian race reported), G3 with a Spanish-speaking Latin American
grandparent (any Hispanic origin), and G2, US-born with a Mexico-born parent (Mexican origin; the account keys G2
by birthplace, so its identification does not enter the count).

Timing: the CPS asks Hispanic origin once, at a household's first interview (MIS 1) or when a person joins the
roster, and carries it forward (CPS Technical Paper 77, Table 3-2.7). MIS 1 records are fresh reports dated by their
interview month; MIS 5 records mostly carry the report made at MIS 1 a year earlier. carry_forward() measures this.

Weights: unweighted; state-mean (summed WTFINL over persons in the year x month x MIS x state cell, a stand-in for
the base weight, which no public file carries); final (WTFINL, raked to national Hispanic totals by age and sex).

Tests: WLS of the indicator on a window dummy against the 2022-24 mean, the same months of 2022-24, or a 2019-24
linear trend (the window gets its own intercept and slope, so the trend is fitted on the baseline alone), with
household-clustered (CPSID, CR1) SEs; an adjusted variant adds age band x sex and state-group (CA, TX, other) dummies.
In-time placebos repeat the main tests in every earlier year; a planted-drop simulation gives the power against a
Hadah-Denteh-sized drop.

ASEC frame: the same G3 rule on the ASEC 2019-2026, by year, and the ASEC 2025-26 records by when their identity was
reported (the household's first-in-sample month, digits 1-6 of CPSIDP; IPUMS codes the oversample's month 13).

Run from the repository root (stage.py first; this script calls it and it skips when its files are current):
  uv run --no-project python3 infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/stage.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/analyze.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # imports from other lanes must not write their __pycache__

import csv
import importlib.util
import json
import math
import resource
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
POOLED = FISCAL / "g3_identity_pooled_2026_10_05"
POP = FISCAL / "mexican_origin_population_total_2026_09_19/derived"
ARMS = FISCAL / "identity_loss_propagation_2026_09_27/derived/population_arms.csv"
V5 = FISCAL / "main_case_lineage_2026_10_05/derived/v5_summary.json"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load("g3_asec", POOLED / "analyze.py")
stage = _load("g3_enforcement_stage", HERE / "stage.py")

SEED = 20261007
SIM_DRAWS = 200
HD_DROP = 0.059  # Hadah-Denteh third-generation ATT, 5.9 pp
ASIA = (50000, 52999)  # IPUMS BPL: East, Southeast and South Asia
LATAM = [20000, 21020, 21030, 21040, 21050, 21060, 21070, 21090, 25000, 26010, 30005, 30010, 30020, 30025, 30030,
         30050, 30060, 30065, 30070, 30090]  # Spanish-speaking Latin America (no Belize, Brazil, Guyana, Caribbean English)
ABROAD_OTHER = 96000  # IPUMS BPL "Other, n.e.c. and unknown": abroad and in no lineage set
ASIAN_RACE = [651, 803, 806, 808, 809, 811, 812, 813, 814, 818, 819]  # RACE codes that include Asian
BA_PLUS = 111
STATE_GROUPS = {6: 1, 48: 2}  # California, Texas; every other state is 0
AGE_BANDS = [0, 5, 10, 15, 18, 25, 35, 200]


def ym(y: int, m: int) -> int:
    return y * 12 + m - 1


def label(t: int) -> str:
    return f"{t // 12}-{t % 12 + 1:02d}"


SERIES_START = ym(2019, 1)
BASE = (ym(2022, 1), ym(2024, 12))
TREND = (ym(2019, 1), ym(2024, 12))
COVID = (ym(2020, 3), ym(2020, 12))
DRIVE = ym(2025, 2)  # first month wholly after the 20 January 2025 inauguration

# Group specs: (group, frame, outcome). Frames are masks on the analysis rows.
FRAMES = {"all": "all ages", "child": "under 18", "adult": "18+", "hd": "under 18, White only (Hadah-Denteh)",
          "hd_two": "under 18, White only, two linked parents", "child_ba": "under 18, a linked parent BA+",
          "child_noba": "under 18, no linked parent BA+"}
SPECS = ([("g3_mex", f, o) for f in FRAMES for o in ("mexican", "hispanic")]
         + [("g2_mex", f, o) for f in ("all", "child", "adult") for o in ("mexican", "hispanic")]
         + [("g3_latam", f, "hispanic") for f in ("all", "child", "hd")]
         + [("g3_asia", f, "asian_race") for f in ("all", "child", "adult")])
GROUP_DESC = {"g3_mex": "G3, Mexico-born grandparent", "g2_mex": "G2, Mexico-born parent",
              "g3_latam": "G3, Spanish-speaking Latin American grandparent",
              "g3_asia": "G3, Asia-born grandparent and no Latin American one"}
MIS_SETS = {"1": (1,), "5": (5,), "1+5": (1, 5)}
WEIGHTS = ["unweighted", "state_mean", "final"]


def windows(last: int) -> dict:
    return {"feb_apr_2025": (DRIVE, ym(2025, 4)), "feb_2025_latest": (DRIVE, last),
            "feb_2025_jan_2026": (DRIVE, ym(2026, 1)), "feb_2026_latest": (ym(2026, 2), last)}


TESTS = [  # (name, window, baseline, adjusted)
    ("feb_apr_2025 vs 2022-24", "feb_apr_2025", "mean", False),
    ("feb_2025_latest vs 2022-24", "feb_2025_latest", "mean", False),
    ("feb_apr_2025 vs 2019-24 trend", "feb_apr_2025", "trend", False),
    ("feb_2025_latest vs 2019-24 trend", "feb_2025_latest", "trend", False),
    ("feb_apr_2025 vs feb_apr 2022-24", "feb_apr_2025", "same_months", False),
    ("feb_2025_latest vs 2019-24 trend, no Mar-Dec 2020", "feb_2025_latest", "trend_no_covid", False),
    ("feb_2025_jan_2026 vs 2022-24", "feb_2025_jan_2026", "mean", False),
    ("feb_2026_latest vs 2022-24", "feb_2026_latest", "mean", False),
    ("feb_apr_2025 vs 2022-24, adjusted", "feb_apr_2025", "mean", True),
    ("feb_2025_latest vs 2022-24, adjusted", "feb_2025_latest", "mean", True),
]


def write(rows: list[dict], path: Path) -> None:
    def fmt(v):
        if isinstance(v, (float, np.floating)):
            return "" if not np.isfinite(v) else f"{float(v):.6g}"
        return v
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows([{k: fmt(v) for k, v in r.items()} for r in rows])


# ---------------------------------------------------------------- persons

def recoded(d: pd.DataFrame, inset) -> pd.DataFrame:
    """Parents' birthplaces with a lineage set mapped to classify's Mexico code (and Mexico itself, when it is not in
    the set, to an abroad code), so classify's G3 rule reads 'a grandparent born in the set'."""
    out = {}
    for c in ("MBPL", "FBPL"):
        v = d[c].to_numpy()
        out[c] = np.where(inset(v), an.MEXICO, np.where(v == an.MEXICO, ABROAD_OTHER, v))
    return d.assign(**out)


def parent_max(d: pd.DataFrame, sample: np.ndarray, col: str) -> np.ndarray:
    """Largest `col` over a person's linked parents (-1 when none), linked within (sample, SERIAL) by PERNUM as in
    analyze.classify."""
    pern = d.PERNUM.to_numpy(np.int64)
    key = (sample * 100_000 + d.SERIAL.to_numpy(np.int64)) * 100 + pern
    order = np.argsort(key)
    skey = key[order]
    hh = key - pern
    val = d[col].to_numpy()
    out = np.full(len(d), -1)
    for loc, _ in an.PARENT_LINKS:
        line = d[loc].to_numpy(np.int64)
        pos = np.minimum(np.searchsorted(skey, hh + line), len(d) - 1)
        found = (line > 0) & (skey[pos] == hh + line)
        out = np.where(found, np.maximum(out, val[order[pos]]), out)
    return out


def persons(d: pd.DataFrame, source: str) -> pd.DataFrame:
    """Analysis rows of one survey year's households: the three G3 lineages and Mexican G2, every age."""
    if source == "monthly":
        sample = d.YEAR.to_numpy(np.int64) * 100 + d.MONTH.to_numpy(np.int64)
    else:
        sample = d.YEAR.to_numpy(np.int64)
    g = an.classify(d, False, sample)
    gl = an.classify(recoded(d, lambda v: np.isin(v, LATAM)), False, sample)
    ga = an.classify(recoded(d, lambda v: (v >= ASIA[0]) & (v <= ASIA[1])), False, sample)
    keep = g["G3anc"] | g["G2"] | gl["G3anc"] | ga["G3anc"]
    hisp = d.HISPAN.to_numpy()
    out = pd.DataFrame({
        "year": d.YEAR.to_numpy(), "month": d.MONTH.to_numpy(),
        "mish": d.MISH.to_numpy() if "MISH" in d else np.zeros(len(d), int),
        "serial": d.SERIAL.to_numpy(), "cpsid": d.CPSID.to_numpy(), "cpsidp": d.CPSIDP.to_numpy(),
        "cpsidv": d.CPSIDV.to_numpy(), "statefip": d.STATEFIP.to_numpy(), "age": d.AGE.to_numpy(),
        "sex": d.SEX.to_numpy(), "race": d.RACE.to_numpy(), "hispan": hisp,
        "w_final": d["WTFINL" if source == "monthly" else "ASECWT"].to_numpy(float),
        "g3_mex": g["G3anc"], "g2_mex": g["G2"], "g3_latam": gl["G3anc"], "g3_asia": ga["G3anc"] & ~gl["G3anc"],
        "two_parents": g["both"], "parent_educ": parent_max(d, sample, "EDUC"),
        "mexican": np.isin(hisp, an.MEX_HISPAN).astype(float), "hispanic": (hisp > 0).astype(float),
        "asian_race": np.isin(d.RACE.to_numpy(), ASIAN_RACE).astype(float)})
    return out[keep].reset_index(drop=True)


def load_rows(source: str) -> pd.DataFrame:
    d = pd.read_parquet(CACHE / f"{source}_hh.parquet")
    if source == "asec":
        d = d[d.YEAR >= 2019]
    parts = []
    years = d.YEAR.to_numpy()
    for y in np.unique(years):
        parts.append(persons(d[years == y], source))
    rows = pd.concat(parts, ignore_index=True)
    rows["t"] = rows.year * 12 + rows.month - 1
    hh = -(rows.t.astype(np.int64) * 100_000 + rows.serial.astype(np.int64))
    rows["cluster"] = np.where(rows.cpsid > 0, rows.cpsid, hh)
    rows["age_band"] = np.digitize(rows.age, AGE_BANDS[1:-1])
    rows["state_group"] = rows.statefip.map(STATE_GROUPS).fillna(0).astype(int)
    return rows


def frame_mask(r: pd.DataFrame, frame: str) -> np.ndarray:
    child, white = (r.age < 18).to_numpy(), (r.race == 100).to_numpy()
    return {"all": np.ones(len(r), bool), "child": child, "adult": ~child, "hd": child & white,
            "hd_two": child & white & r.two_parents.to_numpy(),
            "child_ba": child & (r.parent_educ >= BA_PLUS).to_numpy(),
            "child_noba": child & (r.parent_educ >= 0).to_numpy() & (r.parent_educ < BA_PLUS).to_numpy()}[frame]


# ---------------------------------------------------------------- estimators

def wls(y: np.ndarray, X: np.ndarray, w: np.ndarray, cl: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """WLS coefficients and their cluster-robust (CR1) covariance; `cl` holds cluster codes."""
    Xw = X * w[:, None]
    A = X.T @ Xw
    beta = np.linalg.solve(A, Xw.T @ y)
    u = Xw * (y - X @ beta)[:, None]
    codes = np.unique(cl, return_inverse=True)[1]
    G = codes.max() + 1
    S = np.stack([np.bincount(codes, weights=u[:, j], minlength=G) for j in range(X.shape[1])], axis=1)
    Ainv = np.linalg.inv(A)
    n, k = X.shape
    V = (G / (G - 1)) * ((n - 1) / (n - k)) * Ainv @ (S.T @ S) @ Ainv
    return beta, V


def design(r: pd.DataFrame, w: np.ndarray, win: tuple, baseline: str, adjusted: bool, base: tuple = BASE,
           trend: tuple = TREND):
    """Rows used and the design matrix; column 1 is the window effect.

    Mean baselines: [1, D]. Trend baselines: [1, D, tt(1 - D) + tbar D, D (tt - tbar)], tt in years since the
    trend's first month and tbar the window's weighted mean tt. The baseline rows fit a + b tt; the window rows get
    their own line, which WLS passes through the window's weighted mean at tbar, so the D coefficient is the window
    mean minus the baseline trend extrapolated to tbar."""
    t = r.t.to_numpy()
    in_w = (t >= win[0]) & (t <= win[1])
    if baseline == "mean":
        in_b = (t >= base[0]) & (t <= base[1])
    elif baseline == "same_months":
        months = {m % 12 for m in range(win[0], win[1] + 1)}
        in_b = (t >= base[0]) & (t <= base[1]) & np.isin(t % 12, list(months))
    else:
        in_b = (t >= trend[0]) & (t <= trend[1])
        if baseline == "trend_no_covid":
            in_b &= ~((t >= COVID[0]) & (t <= COVID[1]))
    use = in_w | in_b
    D = in_w[use].astype(float)
    cols = [np.ones(use.sum()), D]
    if baseline.startswith("trend") and in_w.any():
        tt = (t[use] - trend[0]) / 12.0
        tbar = np.average(tt[D == 1], weights=w[use][D == 1])
        cols += [tt * (1 - D) + tbar * D, D * (tt - tbar)]
    if adjusted:
        cell = (r.age_band.to_numpy() * 2 + (r.sex.to_numpy() == 2))[use]
        cols += [(cell == c).astype(float) for c in np.unique(cell)[1:]]
        sg = r.state_group.to_numpy()[use]
        cols += [(sg == c).astype(float) for c in np.unique(sg)[1:]]
    return use, in_w, in_b, np.column_stack(cols)


def window_effect(r, y, w, win, baseline, adjusted, base=BASE, trend=TREND):
    """Window effect in pp with its cluster-robust SE, and the row masks."""
    use, in_w, in_b, X = design(r, w, win, baseline, adjusted, base, trend)
    if in_w.sum() < 2 or in_b.sum() < 2:
        return None
    beta, V = wls(y[use], X, w[use], r.cluster.to_numpy()[use])
    return 100 * beta[1], 100 * math.sqrt(V[1, 1]), use, in_w, in_b


def test_row(r, spec, mis, weight, test, win, baseline, adjusted, w):
    y = r[spec[2]].to_numpy(float)
    res = window_effect(r, y, w, win, baseline, adjusted)
    if res is None:
        return None
    est, se, use, in_w, in_b = res
    cl = r.cluster.to_numpy()
    z = est / se if se > 0 else math.nan
    return dict(group=spec[0], frame=spec[1], outcome=spec[2], mis=mis, weight=weight, test=test,
                window=f"{label(win[0])}..{label(win[1])}", estimate_pp=est, se_pp=se, z=z,
                p=math.erfc(abs(z) / math.sqrt(2)), ci95_low_pp=est - 1.96 * se, ci95_high_pp=est + 1.96 * se,
                mde80_pp=2.8 * se, n_window=int(in_w.sum()), n_window_not=int((in_w & (y == 0)).sum()),
                hh_window=int(len(np.unique(cl[in_w]))), n_base=int(in_b.sum()),
                n_base_not=int((in_b & (y == 0)).sum()), hh_base=int(len(np.unique(cl[in_b]))),
                share_window=float(np.average(y[in_w], weights=w[in_w])),
                share_base=float(np.average(y[in_b], weights=w[in_b])))


def period_stats(r: pd.DataFrame, y: np.ndarray, w: np.ndarray, period: np.ndarray) -> pd.DataFrame:
    """Weighted share by period with a household-clustered SE (linearised ratio mean)."""
    df = pd.DataFrame({"p": period, "y": y, "w": w, "cl": r.cluster.to_numpy()})
    g = df.groupby("p")
    sw, swy = g.w.sum(), (df.w * df.y).groupby(df.p).sum()
    mean = swy / sw
    df["e"] = df.w * (df.y - df.p.map(mean))
    cs = df.groupby(["p", "cl"]).e.sum()
    G = cs.groupby(level=0).size()
    var = (cs ** 2).groupby(level=0).sum() / sw ** 2 * G / (G - 1).clip(lower=1)
    return pd.DataFrame({"n": g.size(), "households": G, "n_not": (df.y == 0).groupby(df.p).sum(), "share": mean,
                         "se": np.sqrt(var)})


# ---------------------------------------------------------------- analyses

def weight_vector(r: pd.DataFrame, weight: str) -> np.ndarray:
    return {"unweighted": np.ones(len(r)), "state_mean": r.w_state.to_numpy(), "final": r.w_final.to_numpy()}[weight]


def spec_rows(R: pd.DataFrame, spec, mis) -> pd.DataFrame:
    m = R[spec[0]].to_numpy() & frame_mask(R, spec[1]) & np.isin(R.mish.to_numpy(), MIS_SETS[mis])
    return R[m].reset_index(drop=True)


def run_tests(R: pd.DataFrame, last: int) -> list[dict]:
    W = windows(last)
    out = []
    for spec in SPECS:
        for mis in MIS_SETS:
            r = spec_rows(R, spec, mis)
            for weight in WEIGHTS:
                w = weight_vector(r, weight)
                for test, win, baseline, adjusted in TESTS:
                    if adjusted and weight == "state_mean":
                        continue
                    row = test_row(r, spec, mis, weight, test, W[win], baseline, adjusted, w)
                    if row:
                        out.append(row)
            # MIS 1 against MIS 5 in the months whose MIS 5 reports predate the drive (difference in differences).
            if mis == "1+5":
                for weight in ("unweighted", "final"):
                    w = weight_vector(r, weight)
                    t, y = r.t.to_numpy(), r[spec[2]].to_numpy(float)
                    win = W["feb_2025_jan_2026"]
                    in_w, in_b = (t >= win[0]) & (t <= win[1]), (t >= BASE[0]) & (t <= BASE[1])
                    use = in_w | in_b
                    m1 = (r.mish.to_numpy() == 1)[use].astype(float)
                    D = in_w[use].astype(float)
                    X = np.column_stack([np.ones(use.sum()), D * m1, D, m1])
                    beta, V = wls(y[use], X, w[use], r.cluster.to_numpy()[use])
                    est, se = 100 * beta[1], 100 * math.sqrt(V[1, 1])
                    z = est / se
                    out.append(dict(group=spec[0], frame=spec[1], outcome=spec[2], mis="1 minus 5", weight=weight,
                                    test="feb_2025_jan_2026 vs 2022-24, MIS 1 change minus MIS 5 change",
                                    window=f"{label(win[0])}..{label(win[1])}", estimate_pp=est, se_pp=se, z=z,
                                    p=math.erfc(abs(z) / math.sqrt(2)), ci95_low_pp=est - 1.96 * se,
                                    ci95_high_pp=est + 1.96 * se, mde80_pp=2.8 * se, n_window=int(in_w.sum()),
                                    n_window_not=int((in_w & (y == 0)).sum()),
                                    hh_window=int(len(np.unique(r.cluster.to_numpy()[in_w]))), n_base=int(in_b.sum()),
                                    n_base_not=int((in_b & (y == 0)).sum()),
                                    hh_base=int(len(np.unique(r.cluster.to_numpy()[in_b]))),
                                    share_window=float(np.average(y[in_w], weights=w[in_w])),
                                    share_base=float(np.average(y[in_b], weights=w[in_b]))))
    return out


SERIES_MONTHLY = [s for s in SPECS if s[0] == "g3_mex" and s[1] in ("all", "child", "adult", "hd")]


def run_series(R: pd.DataFrame, last: int) -> tuple[list[dict], list[dict]]:
    monthly, quarterly = [], []
    for spec in SPECS:
        for mis in MIS_SETS:
            r = spec_rows(R, spec, mis)
            r = r[(r.t >= SERIES_START) & (r.t <= last)].reset_index(drop=True)
            y = r[spec[2]].to_numpy(float)
            for weight in WEIGHTS:
                w = weight_vector(r, weight)
                key = dict(group=spec[0], frame=spec[1], outcome=spec[2], mis=mis, weight=weight)
                if spec in SERIES_MONTHLY:
                    for p, s in period_stats(r, y, w, r.t.to_numpy()).iterrows():
                        monthly.append(dict(**key, month=label(int(p)), **s.to_dict()))
                q = r.year.to_numpy() * 10 + (r.month.to_numpy() - 1) // 3 + 1
                for p, s in period_stats(r, y, w, q).iterrows():
                    quarterly.append(dict(**key, quarter=f"{p // 10}Q{p % 10}", months=int(r.t[q == p].nunique()),
                                          **s.to_dict()))
    for rows in (monthly, quarterly):
        for x in rows:
            for k in ("n", "households", "n_not"):
                x[k] = int(x[k])
    return monthly, quarterly


ANNUAL_SPECS = [("g3_mex", "all", "mexican"), ("g3_mex", "child", "mexican"), ("g3_mex", "adult", "mexican"),
                ("g3_mex", "hd", "hispanic"), ("g3_latam", "all", "hispanic"), ("g3_asia", "all", "asian_race"),
                ("g2_mex", "all", "mexican")]


def run_annual(R: pd.DataFrame, last: int) -> list[dict]:
    """Shares over February Y - January Y+1, 2003-2025 (the last window ends at the latest month): the year-on-year
    spread the 2025 window is judged against. An MIS 5 window mostly repeats the MIS 1 reports of the window before."""
    out = []
    for spec in ANNUAL_SPECS:
        for mis in MIS_SETS:
            r = spec_rows(R, spec, mis)
            t = r.t.to_numpy()
            year = np.where(t % 12 == 0, t // 12 - 1, t // 12)  # January belongs to the window opened the February before
            keep = (year >= 2003) & (t >= ym(2003, 2))
            r, year = r[keep].reset_index(drop=True), year[keep]
            y = r[spec[2]].to_numpy(float)
            for weight in ("unweighted", "final"):
                for p, s in period_stats(r, y, weight_vector(r, weight), year).iterrows():
                    out.append(dict(group=spec[0], frame=spec[1], outcome=spec[2], mis=mis, weight=weight,
                                    window=f"{p}-02..{label(min(ym(int(p) + 1, 1), last))}",
                                    months=int(len(np.unique(r.t[year == p]))), n=int(s.n), households=int(s.households),
                                    n_not=int(s.n_not), share=s.share, se=s.se))
    return out


PLACEBO_SPECS = [("g3_mex", "all", "mexican"), ("g3_mex", "child", "mexican"), ("g3_mex", "hd", "hispanic"),
                 ("g3_latam", "all", "hispanic"), ("g3_asia", "all", "asian_race"), ("g2_mex", "all", "mexican")]


def run_placebos(R: pd.DataFrame, last: int) -> list[dict]:
    """The main tests in every earlier year Y: Feb-Apr of Y and February Y to the actual window's last month shifted
    to Y (18-19 months), against the mean of Y-3..Y-1; the long window also against a Y-6..Y-1 linear trend."""
    out = []
    span = last - DRIVE
    for spec in PLACEBO_SPECS:
        for mis in ("1", "1+5"):
            r = spec_rows(R, spec, mis)
            y = r[spec[2]].to_numpy(float)
            for weight in ("unweighted", "final"):
                w = weight_vector(r, weight)
                for Y in range(2006, 2026):
                    kinds = [("feb_apr vs mean", (ym(Y, 2), ym(Y, 4)), "mean"),
                             ("feb_to_latest_length vs mean", (ym(Y, 2), ym(Y, 2) + span), "mean")]
                    if Y >= 2009:
                        kinds.append(("feb_to_latest_length vs trend", (ym(Y, 2), ym(Y, 2) + span), "trend"))
                    for kind, win, baseline in kinds:
                        if win[1] > last or (Y < 2025 and win[1] >= DRIVE):
                            continue
                        res = window_effect(r, y, w, win, baseline, False, base=(ym(Y - 3, 1), ym(Y - 1, 12)),
                                            trend=(ym(Y - 6, 1), ym(Y - 1, 12)))
                        est, se, _, in_w, in_b = res
                        out.append(dict(group=spec[0], frame=spec[1], outcome=spec[2], mis=mis, weight=weight,
                                        window_kind=kind, year=Y, window=f"{label(win[0])}..{label(win[1])}",
                                        actual=int(Y == 2025), estimate_pp=est, se_pp=se, z=est / se,
                                        n_window=int(in_w.sum()), n_base=int(in_b.sum())))
    return out


def placebo_summary(P: list[dict]) -> list[dict]:
    """Placebo years against the actual 2025 window: the spread of the placebo estimates beside their mean SE (SD
    of z near 1 means the clustered SEs are calibrated), and where the actual estimate falls among them."""
    df = pd.DataFrame(P)
    out = []
    for key, g in df.groupby(["group", "frame", "outcome", "mis", "weight", "window_kind"]):
        pl, act = g[g.actual == 0], g[g.actual == 1]
        if act.empty:
            continue
        a = act.iloc[0]
        out.append(dict(zip(["group", "frame", "outcome", "mis", "weight", "window_kind"], key),
                        placebo_years=f"{pl.year.min()}-{pl.year.max()}", n_placebos=len(pl),
                        placebo_sd_pp=float(pl.estimate_pp.std(ddof=1)), mean_se_pp=float(pl.se_pp.mean()),
                        sd_of_placebo_z=float(pl.z.std(ddof=1)), share_abs_z_over_1_96=float((pl.z.abs() > 1.96).mean()),
                        actual_estimate_pp=float(a.estimate_pp), actual_se_pp=float(a.se_pp), actual_z=float(a.z),
                        share_placebos_at_or_below_actual=float((pl.estimate_pp <= a.estimate_pp).mean())))
    return out


def run_power(R: pd.DataFrame, last: int) -> list[dict]:
    """Power against a Hadah-Denteh-sized drop, two ways.

    Analytic: P(z < -1.96) for a true effect of -HD_DROP with the test's clustered SE, Phi(HD_DROP / SE - 1.96).
    Planted: each window household's identifiers stop identifying together with probability HD_DROP / (window rate),
    the test is rerun, and the shift of the estimate from the unplanted one is recorded with the share of draws
    significant; that share is conditional on this sample, whose own window estimate is not zero."""
    rng = np.random.Generator(np.random.PCG64(SEED))
    W = windows(last)
    phi = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))
    out = []
    for spec in [("g3_mex", "all", "mexican"), ("g3_mex", "child", "mexican"), ("g3_mex", "hd", "hispanic")]:
        r = spec_rows(R, spec, "1")
        y0 = r[spec[2]].to_numpy(float)
        ucl, inv = np.unique(r.cluster.to_numpy(), return_inverse=True)
        t = r.t.to_numpy()
        for win_name in ("feb_apr_2025", "feb_2025_latest"):
            win = W[win_name]
            in_w = (t >= win[0]) & (t <= win[1])
            for weight in ("unweighted", "final"):
                w = weight_vector(r, weight)
                for baseline in ("mean", "trend"):
                    est0, se0 = window_effect(r, y0, w, win, baseline, False)[:2]
                    q = HD_DROP / np.average(y0[in_w], weights=w[in_w])
                    ests, ses = [], []
                    for _ in range(SIM_DRAWS):
                        flip = rng.random(len(ucl)) < q
                        y = np.where(in_w & (y0 == 1) & flip[inv], 0.0, y0)
                        e, s = window_effect(r, y, w, win, baseline, False)[:2]
                        ests.append(e)
                        ses.append(s)
                    ests, ses = np.array(ests), np.array(ses)
                    out.append(dict(group=spec[0], frame=spec[1], outcome=spec[2], mis="1", weight=weight,
                                    window=win_name, baseline="2022-24 mean" if baseline == "mean" else "2019-24 trend",
                                    planted_drop_pp=100 * HD_DROP, draws=SIM_DRAWS, estimate_pp=est0, se_pp=se0,
                                    analytic_power=phi(100 * HD_DROP / se0 - 1.96),
                                    planted_shift_pp=float(ests.mean() - est0), planted_mean_se_pp=float(ses.mean()),
                                    planted_share_significant=float((ests / ses < -1.96).mean())))
    return out


def carry_forward(R: pd.DataFrame) -> list[dict]:
    """MIS 1 persons linked to their own MIS 5 record 12 months later: how often the reported origin changes."""
    out = []
    for idname in ("cpsidv", "cpsidp"):
        m5 = R[(R.mish == 5) & (R[idname] > 0)][[idname, "t", "mexican", "hispanic"]].drop_duplicates(idname)
        m5 = m5.rename(columns={"t": "t5", "mexican": "mex5", "hispanic": "hisp5"})
        for group in ("g3_mex", "g2_mex"):
            a = R[R[group] & (R.mish == 1) & (R[idname] > 0)][[idname, "t", "year", "mexican", "hispanic"]]
            j = a.merge(m5, on=idname)
            j = j[j.t5 == j.t + 12]
            for yr, g in [("2003-2025", j)] + [(str(y), g) for y, g in j.groupby("year")]:
                out.append(dict(link=idname.upper(), group=group, mis1_year=yr, mis1_persons=int(
                    (a.year.astype(str) == yr).sum() if yr != "2003-2025" else len(a)), linked=len(g),
                    mexican_changed=int((g.mexican != g.mex5).sum()),
                    share_mexican_changed=float((g.mexican != g.mex5).mean()) if len(g) else math.nan,
                    mexican_to_not=int(((g.mexican == 1) & (g.mex5 == 0)).sum()),
                    not_to_mexican=int(((g.mexican == 0) & (g.mex5 == 1)).sum()),
                    hispanic_changed=int((g.hispanic != g.hisp5).sum())))
    return out


def contrast_row(r, y, w, X, col, **key) -> dict:
    """One WLS contrast (coefficient `col`, in pp) with its household-clustered SE."""
    beta, V = wls(y, X, w, r.cluster.to_numpy())
    est, se = 100 * beta[col], 100 * math.sqrt(V[col, col])
    z = est / se
    return dict(**key, estimate_pp=est, se_pp=se, z=z, p=math.erfc(abs(z) / math.sqrt(2)),
                ci95_low_pp=est - 1.96 * se, ci95_high_pp=est + 1.96 * se, mde80_pp=2.8 * se)


def asec_frame(S: pd.DataFrame) -> tuple[list[dict], list[dict], list[dict], dict]:
    """G3 identification in the ASEC 2019-2026 by year, tests against 2022-24, and the ASEC 2025-26 records by when
    their identity was reported. The report month is the household's first-in-sample month (CPSIDP digits 1-6): a
    March ASEC household at MIS 1-2 first answered in February-March of the ASEC year, at MIS 3 in January, at MIS 4-8
    in December or earlier; the oversample's month is coded 13 (November households, and April MIS 1 and 5)."""
    by_year, tests, vint = [], [], []
    S = S.copy()
    S["first"] = S.cpsidp // 10**8
    S["over"] = S["first"] % 100 == 13
    ft = (S["first"] // 100) * 12 + S["first"] % 100 - 1
    S["vintage"] = np.select([S.over, ft >= DRIVE, ft == ym(2025, 1)], ["oversample", "post", "january_2025"], "pre")
    S["position"] = np.select([S.over, ft >= S.year * 12 + 1, ft == S.year * 12], ["oversample", "mis1_2", "mis3"],
                              "mis4_8")
    for frame in ("all", "child", "adult", "hd"):
        for outcome in ("mexican", "hispanic"):
            r = S[S.g3_mex & frame_mask(S, frame)].reset_index(drop=True)
            y = r[outcome].to_numpy(float)
            t = r.year.to_numpy()
            for weight in ("unweighted", "final"):
                w = np.ones(len(r)) if weight == "unweighted" else r.w_final.to_numpy()
                for p, s in period_stats(r, y, w, t).iterrows():
                    by_year.append(dict(frame=frame, outcome=outcome, weight=weight, asec_year=int(p),
                                        **{k: (int(v) if k in ("n", "households", "n_not") else v) for k, v in s.items()}))
                key = dict(frame=frame, outcome=outcome, weight=weight)
                for yr in (2025, 2026):
                    use = (t == yr) | ((t >= 2022) & (t <= 2024))
                    q = r[use].reset_index(drop=True)
                    D = (q.year == yr).to_numpy(float)
                    tests.append(dict(**contrast_row(q, y[use], w[use], np.column_stack([np.ones(len(q)), D]), 1,
                                                     **key, test=f"ASEC {yr} minus 2022-24"),
                                      n_window=int(D.sum()), n_window_not=int(((D == 1) & (y[use] == 0)).sum()),
                                      n_base=int((D == 0).sum())))
                # Within the ASEC: MIS 1-2 records (reports from February-March of the ASEC year) against MIS 4-8
                # records, 2025 against 2022-24.
                use = ((t >= 2022) & (t <= 2025) & r.position.isin(["mis1_2", "mis4_8"])).to_numpy()
                q = r[use].reset_index(drop=True)
                D = (q.year == 2025).to_numpy(float)
                m12 = (q.position == "mis1_2").to_numpy(float)
                X = np.column_stack([np.ones(len(q)), D * m12, D, m12])
                tests.append(dict(**contrast_row(q, y[use], w[use], X, 1, **key,
                                                 test="ASEC 2025 minus 2022-24, MIS 1-2 change minus MIS 4-8 change"),
                                  n_window=int((D * m12).sum()), n_window_not=int(((D * m12 == 1) & (y[use] == 0)).sum()),
                                  n_base=int(((1 - D) * m12).sum())))
                for yr in (2025, 2026):
                    sel = t == yr
                    q, wq, yq = r[sel], w[sel], y[sel]
                    for v in ("post", "january_2025", "pre", "oversample"):
                        m = (q.vintage == v).to_numpy()
                        vint.append(dict(frame=frame, outcome=outcome, weight=weight, asec_year=yr, vintage=v,
                                         n=int(m.sum()), weight_share=float(wq[m].sum() / wq.sum()),
                                         share=float(np.average(yq[m], weights=wq[m])) if m.any() else math.nan))
    info = {}
    for yr in (2025, 2026):
        q = S[(S.year == yr) & S.g3_mex]
        w = q.w_final
        info[yr] = dict(post=float(w[q.vintage == "post"].sum() / w.sum()),
                        january_2025=float(w[q.vintage == "january_2025"].sum() / w.sum()),
                        pre=float(w[q.vintage == "pre"].sum() / w.sum()), oversample=float(w[q.over].sum() / w.sum()),
                        first_months=sorted({int(f) for f in q["first"][~q.over].unique()}),
                        # Oversample codes are YYYY13, YYYY being the first ASEC whose oversample held the record
                        # (IPUMS CPS working paper 2025-01): YYYY = yr - 1 marks a second-year household.
                        records_by_first={str(int(k)): int(n) for k, n in q["first"].value_counts().sort_index().items()})
    return by_year, tests, vint, info


def composition(R: pd.DataFrame, last: int) -> list[dict]:
    """Sample composition by month (all persons at MIS 1 and 5) and the G3 lineage's share of the sample."""
    c = pd.read_parquet(CACHE / "monthly_composition.parquet")
    c = c[(c.YEAR * 12 + c.MONTH - 1 >= SERIES_START)]
    cells = pd.read_parquet(CACHE / "monthly_state_cells.parquet")
    out = []
    g3 = R[R.g3_mex & (R.t >= SERIES_START)].groupby(["t", "mish"]).agg(n=("w_final", "size"), w=("w_final", "sum"))
    for (yr, mo, mis), g in c.groupby(["YEAR", "MONTH", "MISH"]):
        n, w = g.n.sum(), g.w.sum()
        f = lambda col: (g.n[g[col]].sum() / n, g.w[g[col]].sum() / w)
        h, mx, mb, g2 = f("hispanic"), f("mexican"), f("mexico_born"), f("us_born_mexican_parent")
        mw_h = g.w[g.hispanic].sum() / g.n[g.hispanic].sum()
        mw_n = g.w[~g.hispanic].sum() / g.n[~g.hispanic].sum()
        t = ym(int(yr), int(mo))
        k = (t, int(mis))
        hh = int(cells[(cells.YEAR == yr) & (cells.MONTH == mo) & (cells.MISH == mis)].households.sum())
        out.append(dict(month=label(t), mis=int(mis), persons=int(n), households=hh, weighted_M=w / 1e6,
                        hispanic_share_unweighted=h[0], hispanic_share_weighted=h[1],
                        mexican_share_unweighted=mx[0], mexican_share_weighted=mx[1],
                        mexico_born_share_unweighted=mb[0], mexico_born_share_weighted=mb[1],
                        us_born_mexican_parent_share_unweighted=g2[0], us_born_mexican_parent_share_weighted=g2[1],
                        mean_weight_ratio_hispanic_to_not=mw_h / mw_n,
                        g3_lineage_per_1000=1000 * (g3.n.get(k, 0) / n),
                        g3_lineage_weighted_per_1000=1000 * (g3.w.get(k, 0) / w)))
    return out


def asec_raking_shares() -> list[dict]:
    """ASEC weights by year and age group. The G3+ Mexican identifiers' share of all Hispanic weight is what the
    raking returns to them when G3+ reports move from Hispanic to not Hispanic (the lost weight is re-spread over all
    Hispanics in each age x sex cell). The mean-weight ratio of G3+ Mexican to G3+ non-Hispanic records shows how
    much more weight each identifier record carries in a year, whatever its identity report."""
    a = pd.read_parquet(CACHE / "asec_composition.parquet")
    a = a[a.YEAR >= 2019]
    groups = [((int(yr), "under 18" if child else "18+"), g) for (yr, child), g in a.groupby(["YEAR", "child"])]
    groups += [((int(yr), "all ages"), g) for yr, g in a.groupby("YEAR")]
    out = []
    for (yr, label_), g in groups:
        hisp = (g.hisp_class > 0).to_numpy()
        g3m = ((g.hisp_class == 1) & (g.generation == 3)).to_numpy()
        g3n = ((g.hisp_class == 0) & (g.generation == 3)).to_numpy()
        mw = lambda m: g.w[m].sum() / g.n[m].sum()
        out.append(dict(asec_year=yr, group=label_, g3plus_mexican_M=g.w[g3m].sum() / 1e6,
                        g3plus_mexican_records=int(g.n[g3m].sum()), hispanic_M=g.w[hisp].sum() / 1e6,
                        mexican_M=g.w[(g.hisp_class == 1).to_numpy()].sum() / 1e6,
                        g3plus_mexican_share_of_hispanic=g.w[g3m].sum() / g.w[hisp].sum(),
                        mexican_g1_g2_share_of_hispanic=g.w[((g.hisp_class == 1) & (g.generation < 3)).to_numpy()].sum()
                        / g.w[hisp].sum(),
                        weight_ratio_g3plus_mexican_to_g3plus_not_hispanic=mw(g3m) / mw(g3n),
                        weight_ratio_hispanic_to_not_hispanic=mw(hisp) / mw(~hisp)))
    return out


# ---------------------------------------------------------------- gates

def gates(R: pd.DataFrame, S: pd.DataFrame, last: int) -> list[dict]:
    """Positive controls against the pooled lane's published counts, and data checks. Any failure stops the run."""
    out = []
    pub = pd.read_csv(POOLED / "derived/monthly_counts.csv").set_index(["rows", "years", "min_age"])
    cols = {"G3anc": None, "G3anc_id": 1.0, "G3anc_nonmex": 0.0}
    for rows, mis in (("monthly_nodedup", (1, 5)), ("monthly_mis1", (1,))):
        for yrs, (a, b) in (("2022_2025", (2022, 2025)), ("2022_2026", (2022, 2026)), ("1994_2026", (2003, 2026))):
            if yrs == "1994_2026":
                continue  # the staged rows start in 2003
            for lo in (18, 25):
                m = R.g3_mex & R.mish.isin(mis) & R.year.between(a, b) & (R.age >= lo)
                for col, val in cols.items():
                    got = int((m & (R.mexican == val)).sum()) if val is not None else int(m.sum())
                    want = int(pub.loc[(rows, yrs, lo), col])
                    out.append(dict(gate=f"pooled monthly_counts.csv {rows} {yrs} {lo}+ {col}", value=got, expected=want,
                                    passed=got == want))
    pub_a = pd.read_csv(POOLED / "derived/counts.csv").set_index(["period", "dedupe", "min_age"])
    for lo in (18, 25):
        m = S.g3_mex & S.year.between(2022, 2026) & (S.age >= lo)
        for col, val in cols.items():
            got = int((m & (S.mexican == val)).sum()) if val is not None else int(m.sum())
            want = int(pub_a.loc[("2022_2026", "nodedup", lo), col])
            out.append(dict(gate=f"pooled counts.csv (ASEC) 2022_2026 nodedup {lo}+ {col}", value=got, expected=want,
                            passed=got == want))
    months = sorted(set(R.t.unique()))
    expected = [t for t in range(ym(2003, 1), last + 1) if t != ym(2025, 10)]
    out.append(dict(gate="monthly samples 2003-01..latest, October 2025 absent", value=len(months),
                    expected=len(expected), passed=months == expected))
    out.append(dict(gate="MISH values", value=str(sorted(R.mish.unique())), expected="[1, 5]",
                    passed=sorted(R.mish.unique()) == [1, 5]))
    out.append(dict(gate="analysis rows with nonpositive final weight", value=int((R.w_final <= 0).sum()), expected=0,
                    passed=int((R.w_final <= 0).sum()) == 0))
    out.append(dict(gate="analysis rows without a state-mean weight", value=int(R.w_state.isna().sum()), expected=0,
                    passed=int(R.w_state.isna().sum()) == 0))
    out.append(dict(gate="analysis rows without a CPSID household", value=int((R.cpsid <= 0).sum()), expected=0,
                    passed=int((R.cpsid <= 0).sum()) == 0))
    bad = [g for g in out if not g["passed"]]
    if bad:
        raise SystemExit(f"[BLOCKED] gates failed: {bad}")
    return out


# ---------------------------------------------------------------- sizing

def sizing(T: list[dict], vint_info: dict, raking: list[dict]) -> list[dict]:
    """What a drop of the measured size, or of a bound on it, would do to the ASEC 2025 frame and the account.

    Only identity reports made from February 2025 can carry a drive effect. Their weighted share of the ASEC 2025 G3
    lineage is s: low = March MIS 1-2 only; central = + one tenth of the oversample (April MIS 1 among its ten
    Hispanic-household rotation groups); high = + the January 2025 reports + one seventh of the oversample (April
    MIS 1 among the seven groups of non-Hispanic households with children). A drop d in fresh reports moves the ASEC
    2025 rate by s d and the self-identified G3+ count by N = s d L, L the G3+ lineage (arm b's corrected
    third-plus, CPS frame), applying the G3 drop to all of G3+.

    Two readings of N in dollars (ladder 281's arm-b costs, v5_summary.json):
    - missing: the N fall out of the count and cost what an added arm-b person costs (the brief's first order);
    - self-corrected: p3 (0.888) is measured on the same ASEC 2025 children, so a frame-wide drop lowers it too and
      arm b adds the N back as G3-rate attriters; what remains is their price, (1 - C3) G3+ + C3 W instead of an
      identified member's G3+, if drive-induced non-identifiers are not selected on schooling."""
    df = pd.DataFrame(T)
    arms = pd.read_csv(ARMS).set_index("arm")
    L = float(arms.loc["b_one_step", "corrected_third_plus_M"]) * 1e6
    cps = pd.read_csv(POP / "arm1_counts_cps.csv").set_index("definition")
    selfid = float(cps.loc["G3+ native, 2 US-area parents, self-ID Mexican", "population"])
    mult = pd.read_csv(POP / "arm3_multiplier.csv").set_index("quantity")
    p3 = float(mult.loc["A and B: 3rd-generation identifiers", "children"]
               / mult.loc["B: objectively 3rd generation (>=1 Mexico-born grandparent)", "children"])
    v5 = json.loads(V5.read_text())["sets"]
    added = {k: v5[k]["arms"]["b"]["added_per_person_usd"] for k in ("set", "cash")}
    priced = {k: [g - a for g, a in zip(v5[k]["arms"]["b"]["g3plus_member_usd"], v5[k]["arms"]["b"]["g3_rate_attriter_usd"])]
              for k in ("set", "cash")}
    rk = next(r for r in raking if r["asec_year"] == 2025 and r["group"] == "all ages")
    v = vint_info[2025]
    shares = {"low": v["post"], "central": v["post"] + v["oversample"] / 10,
              "high": v["post"] + v["january_2025"] + v["oversample"] / 7}
    out = []
    for test in ("feb_2025_latest vs 2022-24", "feb_2025_latest vs 2019-24 trend", "feb_apr_2025 vs 2022-24"):
        row = df[(df.group == "g3_mex") & (df.frame == "all") & (df.outcome == "mexican") & (df.mis == "1")
                 & (df.weight == "unweighted") & (df.test == test)].iloc[0]
        for what, drop_pp in (("point estimate", -row.estimate_pp), ("95% bound", -row.ci95_low_pp),
                              ("detectable (2.8 SE)", row.mde80_pp), ("Hadah-Denteh 5.9 pp", 100 * HD_DROP)):
            for s_name, s in shares.items():
                n = s * max(drop_pp, 0.0) / 100 * L
                out.append(dict(test=test, drop=what, drop_pp=drop_pp, s_name=s_name, s=s,
                                asec2025_rate_change_pp=-s * max(drop_pp, 0.0), identifiers_missed=n,
                                missing_set_bn=[n * c / 1e9 for c in added["set"]],
                                missing_cash_bn=[n * c / 1e9 for c in added["cash"]],
                                self_corrected_set_bn=[n * c / 1e9 for c in priced["set"]],
                                self_corrected_cash_bn=[n * c / 1e9 for c in priced["cash"]],
                                lineage_g3plus_M=L / 1e6, selfid_g3plus_M=selfid / 1e6, p3=p3,
                                raking_share_to_g3plus_identifiers=rk["g3plus_mexican_share_of_hispanic"],
                                raking_share_to_g1_g2_mexicans=rk["mexican_g1_g2_share_of_hispanic"]))
    for r in out:  # flatten the low/high pairs
        for k in [k for k, x in r.items() if isinstance(x, list)]:
            lo, hi = r.pop(k)
            r[f"{k}_low"], r[f"{k}_high"] = lo, hi
    return out


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    meta = {k: stage.stage(k) for k in stage.SOURCES}
    R = load_rows("monthly")
    S = load_rows("asec")
    last = int(R.t.max())
    cells = pd.read_parquet(CACHE / "monthly_state_cells.parquet")
    cells["w_state"] = cells.w / cells.n
    R = R.merge(cells[["YEAR", "MONTH", "MISH", "STATEFIP", "w_state"]].rename(
        columns={"YEAR": "year", "MONTH": "month", "MISH": "mish", "STATEFIP": "statefip"}),
        on=["year", "month", "mish", "statefip"], how="left")
    print(f"  ✓ rows: monthly {len(R):,} (last month {label(last)}), ASEC {len(S):,}", flush=True)
    G = gates(R, S, last)
    write(G, DERIVED / "gates.csv")
    print(f"  ✓ gates: {len(G)} pass", flush=True)

    T = run_tests(R, last)
    write(T, DERIVED / "tests.csv")
    print(f"  ✓ tests: {len(T)} rows", flush=True)
    monthly, quarterly = run_series(R, last)
    write(monthly, DERIVED / "series_monthly.csv")
    write(quarterly, DERIVED / "series_quarterly.csv")
    print(f"  ✓ series: {len(monthly)} monthly, {len(quarterly)} quarterly rows", flush=True)
    write(run_annual(R, last), DERIVED / "series_annual.csv")
    P = run_placebos(R, last)
    write(P, DERIVED / "placebo_years.csv")
    write(placebo_summary(P), DERIVED / "placebo_summary.csv")
    PW = run_power(R, last)
    write(PW, DERIVED / "power.csv")
    print("  ✓ placebos and power", flush=True)
    write(carry_forward(R), DERIVED / "carry_forward.csv")
    by_year, asec_tests, vint, vint_info = asec_frame(S)
    write(by_year, DERIVED / "asec_by_year.csv")
    write(asec_tests, DERIVED / "asec_tests.csv")
    write(vint, DERIVED / "asec_vintage.csv")
    write(composition(R, last), DERIVED / "composition_monthly.csv")
    raking = asec_raking_shares()
    write(raking, DERIVED / "asec_raking_shares.csv")
    SZ = sizing(T, vint_info, raking)
    write(SZ, DERIVED / "sizing.csv")

    audit = dict(stage={k: {f: v for f, v in m.items() if f != "household_filter"} for k, m in meta.items()},
                 household_filter=stage.LINEAGE_BPL, last_month=label(last),
                 rows_monthly=len(R), rows_asec=len(S),
                 g3_mex_rows_monthly_2019_on=int((R.g3_mex & (R.t >= SERIES_START)).sum()),
                 asec_vintage_shares={str(k): v for k, v in vint_info.items()},
                 seed=SEED, power_draws=SIM_DRAWS, planted_drop=HD_DROP,
                 windows={k: [label(a), label(b)] for k, (a, b) in windows(last).items()},
                 baseline_mean=[label(BASE[0]), label(BASE[1])], baseline_trend=[label(TREND[0]), label(TREND[1])],
                 weights="unweighted; state_mean = summed WTFINL / persons in year x month x MIS x state (all persons); "
                         "final = WTFINL (ASECWT in the ASEC frame)",
                 se="CR1 cluster-robust, cluster = CPSID household")
    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")

    pd.set_option("display.width", 250)
    df = pd.DataFrame(T)
    show = df[(df.group == "g3_mex") & (df.outcome == "mexican") & df.frame.isin(["all", "child", "hd"])
              & df.mis.isin(["1", "5", "1+5", "1 minus 5"])]
    print(show[["frame", "mis", "weight", "test", "estimate_pp", "se_pp", "n_window", "n_base"]].round(2).to_string(index=False))
    print(pd.DataFrame(PW).round(3).to_string(index=False))
    print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MiB")


if __name__ == "__main__":
    main()
