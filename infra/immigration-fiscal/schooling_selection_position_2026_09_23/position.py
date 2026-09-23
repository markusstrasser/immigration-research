"""Where in Mexico's schooling distribution do Mexico-born US arrivals come from, by arrival cohort?

Migrant side: IPUMS USA extract #3 (_cache/us_mexborn.data.csv.gz): Mexico-born (BPL 200) records
from the 1980/1990/2000 5% censuses and the single-year ACS 2005-2024, with SEX and BIRTHYR.
Origin side: derived/origin_levels.csv (origin_inegi.py): INEGI 2000, 2010 and 2020 census
tabulations by sex x five-year age x attainment.

Each migrant is placed in the attainment distribution of Mexican residents of the same sex and
birth year (a mixture of the two five-year age groups the birth year straddles on census day).
Statistics are migrant-weighted (PERWT):
  ridit          mean percentile rank in the own-cohort Mexican distribution, ties spread
                 (0.5 = a random draw from Mexico), on the finest partition whose cut points
                 exist in both the US survey coding and the INEGI tabulation (no split assumed)
  quintile       share of migrants in each fifth of their cohort's Mexican distribution (ties
                 spread uniformly within a tied block)
  five-category  migrant vs Mexican shares (Mexico reweighted to the migrants' sex x birth-year
                 mix). US bins that straddle a category boundary (1990 "grade 5-8" and "some
                 college, no degree"; 2000/2005 "grade 5 or 6") are split by the same cohort's own
                 single-grade distribution in the ACS 2008-2012 ("empirical", main), by Mexico's
                 within-bin distribution ("neutral"), or wholly low/high (bounds).
Checks in position_all_specs.csv: fixed reference censuses, arrival-age and enrolment variants,
split rules, coding variants, and the same cohorts observed in the ACS 2019 and 2024 against the
2020 census (one instrument, one date and one reference for every cohort).
Standard errors: Taylor linearisation with households as with-replacement PSUs, strata ignored
(conservative); checked against ACS replicate weights in acs_pums_check.py. The origin tables are
full-count census tabulations and carry no sampling error.

Outputs in derived/ (aggregates only). Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/position.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from levels import FIVE, FIVE_CREDENTIAL, N_LEVELS  # noqa: E402

DATA = HERE / "_cache" / "us_mexborn.data.csv.gz"
OUT = HERE / "derived"

# ------------------------------------------------------------------ US coding
# IPUMS EDUCD -> interval on the shared scale (levels.py). 000/001/999 are missing.
EDUCD = {
    2: (0, 0), 10: (0, 4), 11: (0, 0), 12: (0, 0), 13: (1, 4), 14: (1, 1), 15: (2, 2), 16: (3, 3), 17: (4, 4),
    20: (5, 8), 21: (5, 6), 22: (5, 5), 23: (6, 6), 24: (7, 8), 25: (7, 7), 26: (8, 8),
    30: (9, 9), 40: (10, 10), 50: (11, 11),
    60: (13, 13),               # 1980 "grade 12" (finished 12th grade; no diploma item)
    61: (12, 12),               # 12th grade, no diploma
    62: (13, 13), 63: (13, 13), 64: (13, 13), 65: (13, 13),
    70: (14, 15), 80: (14, 15), 90: (14, 15),   # 1980 years of college, no degree information
    71: (14, 14), 81: (15, 15), 82: (15, 15), 83: (15, 15),
    100: (16, 16), 101: (16, 16), 110: (16, 16), 111: (16, 16), 112: (16, 16), 113: (16, 16),
    114: (16, 16), 115: (16, 16), 116: (16, 16),
}

# Bracketed YRIMMIG codes in the 1980 and 1990 censuses: code -> (first year, midpoint of the
# arrival interval in calendar time; census day 1 April).
BRACKET = {1980: {1975: (1975, 1977.6), 1970: (1970, 1972.5), 1965: (1965, 1967.5), 1960: (1960, 1962.5),
                  1950: (1950, 1955.0)},
           1990: {1987: (1987, 1988.6), 1985: (1985, 1986.0), 1982: (1982, 1983.5), 1980: (1980, 1981.0),
                  1975: (1975, 1977.5), 1970: (1970, 1972.5), 1965: (1965, 1967.5), 1960: (1960, 1962.5),
                  1950: (1950, 1955.0)}}

COHORTS = [(1975, 1979), (1980, 1984), (1985, 1989), (1990, 1994), (1995, 1999), (2000, 2004),
           (2005, 2009), (2010, 2014), (2015, 2019), (2020, 2023)]
# Survey in which each cohort is first observed at the shortest duration available.
MAIN_SURVEY = {1975: 1980, 1980: 1990, 1985: 1990, 1990: 2000, 1995: 2000, 2000: 2005, 2005: 2010,
               2010: 2015, 2015: 2019, 2020: 2024}
# Census nearest the arrival window among those tabulated here (no 1990 national table found).
MAIN_REF = {1975: 2000, 1980: 2000, 1985: 2000, 1990: 2000, 1995: 2000, 2000: 2000, 2005: 2010,
            2010: 2010, 2015: 2020, 2020: 2020}
NEXT_CENSUS = {2000: 2010, 2010: 2020, 2020: 2020}
CENSUS_DAY_FRAC = {2000: 44 / 366, 2010: 162 / 365, 2020: 74 / 366}   # share of the year before census day


# ------------------------------------------------------------------ data
def load_migrants(path: Path = DATA, all_samples: bool = False) -> pd.DataFrame:
    cols = ["YEAR", "SAMPLE", "SERIAL", "PERNUM", "CLUSTER", "STRATA", "GQ", "PERWT", "SEX", "AGE", "BIRTHYR",
            "CITIZEN", "YRIMMIG", "SCHOOL", "EDUCD"]
    d = pd.read_csv(path, usecols=cols)
    if not all_samples:
        d = d[d.SAMPLE % 100 == 1]        # single-year samples (census 5%, ACS 1-year); IPUMS SAMPLE yyyy01
    d = d[d.EDUCD.isin(list(EDUCD))].copy()
    d["lo"] = d.EDUCD.map(lambda c: EDUCD[c][0])
    d["hi"] = d.EDUCD.map(lambda c: EDUCD[c][1])
    # 1990 has one "some college, no degree" item, which IPUMS codes 071; it spans <1 year (L12)
    # and 1+ years (L13a).
    m90 = (d.YEAR == 1990) & (d.EDUCD == 71)
    d.loc[m90, "lo"], d.loc[m90, "hi"] = 13, 14
    arr_first, arr_mid = [], []
    for y, c in zip(d.YEAR.to_numpy(), d.YRIMMIG.to_numpy()):
        if y in BRACKET and c in BRACKET[y]:
            f, m = BRACKET[y][c]
        elif c > 0:
            f, m = c, c + 0.5
        else:
            f, m = np.nan, np.nan
        arr_first.append(f)
        arr_mid.append(m)
    d["arr_first"] = arr_first
    d["arr_mid"] = arr_mid
    d["arr_age"] = d.arr_mid - (d.BIRTHYR + 0.5)
    d["arr_age_min"] = d.arr_first - (d.BIRTHYR + 1.0)   # youngest possible age at arrival
    d["sex"] = d.SEX.map({1: "H", 2: "M"})
    d["noncit"] = d.CITIZEN.isin([3, 4, 5])
    return d


def cohort_rows(d: pd.DataFrame, survey: int, c0: int, c1: int) -> pd.DataFrame:
    g = d[d.YEAR == survey]
    if survey in BRACKET:
        return g[(g.arr_first >= c0) & (g.arr_first <= c1)]
    return g[(g.YRIMMIG >= c0) & (g.YRIMMIG <= c1)]


def empirical_splits(d: pd.DataFrame) -> dict:
    """Within-bin composition of each arrival cohort x sex from its single-grade ACS 2008-2012
    records (arrival age 20+), used to split US bins that straddle a category boundary."""
    a = d[(d.YEAR >= 2008) & (d.YEAR <= 2012) & (d.arr_age >= 20)]
    out = {}
    for c0, c1 in COHORTS:
        for sx in ("H", "M"):
            g = a[(a.YRIMMIG >= c0) & (a.YRIMMIG <= c1) & (a.sex == sx)]
            if len(g) < 200:
                continue
            w = lambda codes: float(g.PERWT[g.EDUCD.isin(codes)].sum())  # noqa: E731
            em = np.zeros(N_LEVELS)
            em[5], em[6], em[7], em[8] = w([22]), w([23]), w([25]), w([26])
            out[(c0, sx)] = {"grades": em, "lt1_in_somecoll": w([65]) / (w([65]) + w([71])),
                             "nodeg_in_college": w([71]) / (w([71]) + w([81, 82, 83]))}
    return out


# ------------------------------------------------------------------ origin
class Origin:
    def __init__(self, path: Path):
        o = pd.read_csv(path)
        self.cats = {}      # census -> sorted list of intervals present
        self.cells = {}     # (census, sex, age_lo) -> {interval: share}
        self.groups = {}    # census -> sorted list of (age_lo, age_hi)
        for (c, s, lo, hi), g in o.groupby(["census", "sex", "age_lo", "age_hi"]):
            tot = g["count"].sum()
            self.cells[(c, s, lo)] = {(int(a), int(b)): n / tot for a, b, n in zip(g.lvl_lo, g.lvl_hi, g["count"])}
            self.groups.setdefault(c, set()).add((lo, hi))
        for c in self.groups:
            self.groups[c] = sorted(self.groups[c])
            self.cats[c] = sorted({k for (cc, _, _), v in self.cells.items() if cc == c for k, x in v.items() if x > 0})
        self._memo = {}

    def group(self, census: int, age: int) -> int:
        age = max(age, 20)   # birth cohorts under 20 on census day use the 20-24 group (reported as clamped)
        for lo, hi in self.groups[census]:
            if lo <= age <= hi:
                return lo
        return self.groups[census][-1][0]

    def dist(self, census: int, sex: str, birthyr: int) -> dict:
        key = (census, sex, birthyr)
        if key not in self._memo:
            f = CENSUS_DAY_FRAC[census]
            out = {}
            for age, p in ((census - birthyr, f), (census - birthyr - 1, 1 - f)):
                cell = self.cells[(census, sex, self.group(census, age))]
                for k, v in cell.items():
                    out[k] = out.get(k, 0.0) + p * v
            self._memo[key] = out
        return self._memo[key]


def common_bins(us_cats: list, mx_cats: list) -> list[tuple[int, int]]:
    """Finest partition of 0..N_LEVELS-1 whose cut points exist on both sides."""
    def cuts(cats):
        return {c for c in range(N_LEVELS - 1) if not any(lo <= c and hi >= c + 1 for lo, hi in cats)}
    common = sorted(cuts(us_cats) & cuts(mx_cats))
    bins, start = [], 0
    for c in common:
        bins.append((start, c))
        start = c + 1
    bins.append((start, N_LEVELS - 1))
    return bins


def level_mass(dist: dict) -> np.ndarray:
    """Spread each interval's mass uniformly over its levels (used only to split straddling bins)."""
    m = np.zeros(N_LEVELS)
    for (lo, hi), v in dist.items():
        m[lo:hi + 1] += v / (hi - lo + 1)
    return m


# ------------------------------------------------------------------ statistics
def lin_se(y: np.ndarray, w: np.ndarray, cluster: np.ndarray) -> tuple[float, float]:
    """Weighted mean and its linearised SE with with-replacement clusters."""
    W = w.sum()
    theta = float((w * y).sum() / W)
    u = w * (y - theta) / W
    tot = pd.Series(u).groupby(cluster).sum().to_numpy()
    n = len(tot)
    return theta, float(np.sqrt(n / (n - 1) * ((tot - tot.mean()) ** 2).sum())) if n > 1 else np.nan


def split_fraction(lo: int, hi: int, clo: int, chi: int, split: str, lm: np.ndarray, emp: dict | None) -> float:
    """Share of a US interval [lo, hi] that falls in category [clo, chi]."""
    ov_lo, ov_hi = max(lo, clo), min(hi, chi)
    if ov_lo > ov_hi:
        return 0.0
    if lo >= clo and hi <= chi:
        return 1.0
    if split == "low":
        return 1.0 if clo <= lo <= chi else 0.0
    if split == "high":
        return 1.0 if clo <= hi <= chi else 0.0
    if split == "empirical" and emp is not None:
        if (lo, hi) == (13, 14):
            f13 = emp["lt1_in_somecoll"]
            return f13 if ov_lo == 13 and ov_hi == 13 else (1 - f13)
        if (lo, hi) == (14, 15):
            f14 = emp["nodeg_in_college"]
            return f14 if ov_lo == 14 and ov_hi == 14 else (1 - f14)
        m = emp["grades"]
        if m[lo:hi + 1].sum() > 0:
            return float(m[ov_lo:ov_hi + 1].sum() / m[lo:hi + 1].sum())
    inside = lm[lo:hi + 1]
    return float(lm[ov_lo:ov_hi + 1].sum() / inside.sum()) if inside.sum() > 0 else (ov_hi - ov_lo + 1) / (hi - lo + 1)


def person_scores(g: pd.DataFrame, origin: Origin, census: np.ndarray, sexref: str, five: dict,
                  split: str, emp: dict, cohort0: int):
    """Per-migrant ridit, quintile memberships, five-category memberships (migrant and Mexico)."""
    us_cats = sorted({(a, b) for a, b in zip(g.lo, g.hi)})
    mx_cats = sorted({k for c in set(census) for k in origin.cats[int(c)]})
    bins = common_bins(us_cats, mx_cats)
    bin_of = np.zeros(N_LEVELS, dtype=int)
    for i, (a, b) in enumerate(bins):
        bin_of[a:b + 1] = i
    n = len(g)
    ridit, quint = np.zeros(n), np.zeros((n, 5))
    mig5, mex5 = np.zeros((n, len(five))), np.zeros((n, len(five)))
    names = list(five)
    for i, (lo, hi, sx, by, cen) in enumerate(zip(g.lo.to_numpy(), g.hi.to_numpy(), g.sex.to_numpy(),
                                                 g.BIRTHYR.to_numpy(), census)):
        ref = origin.dist(int(cen), sx if sexref == "own" else "T", int(by))
        p = np.zeros(len(bins))
        for (a, b), v in ref.items():
            p[bin_of[a]] += v
        k = bin_of[lo]
        F0 = p[:k].sum()
        ridit[i] = F0 + p[k] / 2
        a0, a1 = F0, F0 + p[k]
        for q in range(5):
            qlo, qhi = q / 5, (q + 1) / 5
            if a1 > a0:
                quint[i, q] = max(0.0, min(a1, qhi) - max(a0, qlo)) / (a1 - a0)
            else:
                quint[i, q] = 1.0 if (qlo <= a0 < qhi or (q == 4 and a0 >= 1)) else 0.0
        lm = level_mass(ref)
        emp_i = emp.get((cohort0, sx))
        for j, name in enumerate(names):
            clo, chi = five[name]
            mex5[i, j] = lm[clo:chi + 1].sum()
            mig5[i, j] = split_fraction(lo, hi, clo, chi, split, lm, emp_i)
    return ridit, quint, mig5, mex5, bins


def ref_census(g: pd.DataFrame, rule: str, main_ref: int) -> np.ndarray:
    if rule == "nearest":
        return np.full(len(g), main_ref)
    if rule == "nearest_or_next":   # migrants under 20 at the nearest census use the next one
        young = (main_ref - g.BIRTHYR.to_numpy()) < 20
        return np.where(young, NEXT_CENSUS[main_ref], main_ref)
    return np.full(len(g), int(rule))


def summarize(g: pd.DataFrame, origin: Origin, emp: dict, cohort0: int, rule: str, sexref: str = "own",
              five: dict = FIVE, split: str = "empirical", weight: np.ndarray | None = None) -> dict:
    census = ref_census(g, rule, MAIN_REF[cohort0])
    ridit, quint, mig5, mex5, bins = person_scores(g, origin, census, sexref, five, split, emp, cohort0)
    w = g.PERWT.to_numpy(dtype=float) if weight is None else weight
    cl = (g.YEAR.astype(str) + "_" + g.SERIAL.astype(str)).to_numpy()
    clamped = (census - g.BIRTHYR.to_numpy()) < 20
    rec = {"n": len(g), "wN": w.sum(), "clamped_share": float((w * clamped).sum() / w.sum()),
           "ref_censuses": "/".join(str(c) for c in sorted(set(census.tolist()))),
           "bins": " ".join(f"{a}-{b}" for a, b in bins)}
    rec["ridit"], rec["ridit_se"] = lin_se(ridit, w, cl)
    for q in range(5):
        rec[f"q{q + 1}"], rec[f"q{q + 1}_se"] = lin_se(quint[:, q], w, cl)
    for j, name in enumerate(five):
        rec[f"mig_{name}"], rec[f"mig_{name}_se"] = lin_se(mig5[:, j], w, cl)
        rec[f"mex_{name}"] = float((w * mex5[:, j]).sum() / w.sum())
        rec[f"diff_{name}"], rec[f"diff_{name}_se"] = lin_se(mig5[:, j] - mex5[:, j], w, cl)
    b, t = rec["diff_c1_none_primary_incomplete"], rec["diff_c5_tertiary"]
    rec["position"] = ("middle (fewer in both tails)" if b < 0 and t < 0 else
                       "top (fewer at bottom, more at top)" if b < 0 <= t else
                       "bottom (more at bottom, fewer at top)" if t < 0 <= b else "both tails (more in both)")
    return rec


def undercount(g: pd.DataFrame, origin: Origin, emp: dict, cohort0: int,
               ks=(1.0, 1.1, 1.25, 1.5, 1.75)) -> list[dict]:
    """Inflate the weight of non-citizen migrants in the lowest category (C1) by k."""
    census = ref_census(g, "nearest", MAIN_REF[cohort0])
    ridit, quint, mig5, mex5, _ = person_scores(g, origin, census, "own", FIVE, "empirical", emp, cohort0)
    w0 = g.PERWT.to_numpy(dtype=float)
    c1 = mig5[:, 0] * g.noncit.to_numpy()
    out = []
    for k in ks:
        w = w0 * (1 + (k - 1) * c1)
        out.append({"k": k, "ridit": (w * ridit).sum() / w.sum(), "mig_c1": (w * mig5[:, 0]).sum() / w.sum(),
                    "mex_c1": (w * mex5[:, 0]).sum() / w.sum(), "q1": (w * quint[:, 0]).sum() / w.sum(),
                    "q5": (w * quint[:, 4]).sum() / w.sum()})
    # break-even k: ridit = 0.5, and migrant C1 share = Mexico C1 share (Mexico side at k = 1)
    num = (w0 * (ridit - 0.5)).sum()
    den = (w0 * c1 * (0.5 - ridit)).sum()
    k_ridit = 1 + num / den if den > 0 and num > 0 else np.nan
    W, S1, S1n = w0.sum(), (w0 * mig5[:, 0]).sum(), (w0 * c1).sum()
    m1 = (w0 * mex5[:, 0]).sum() / W
    k_c1 = 1 + (m1 * W - S1) / (S1n * (1 - m1)) if S1n > 0 else np.nan
    for r in out:
        r["breakeven_k_ridit_0.5"] = k_ridit
        r["breakeven_k_c1_equal_mexico"] = k_c1
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    origin = Origin(OUT / "origin_levels.csv")
    d = load_migrants()
    emp = empirical_splits(d)
    specs, under, drift = [], [], []

    def run(label, g, cohort0, rule="nearest", **kw):
        for sx in ("P", "H", "M"):
            gg = g if sx == "P" else g[g.sex == sx]
            if len(gg) < 30:
                continue
            specs.append({"spec": label, "sex": sx, "rule": rule, **summarize(gg, origin, emp, cohort0, rule, **kw)})

    for c0, c1 in COHORTS:
        s = MAIN_SURVEY[c0]
        base = cohort_rows(d, s, c0, c1)
        tag = f"{c0}-{c1}"
        meta = {"cohort": tag, "survey": s}
        adult20 = base[base.arr_age >= 20]
        n0 = len(specs)
        run("main", adult20, c0)
        run("nearest_or_next_census", adult20, c0, "nearest_or_next")
        for cen in (2000, 2010, 2020):
            if cen != MAIN_REF[c0]:   # fixed-census checks, only migrants aged 20+ on that census day
                run(f"ref{cen}", adult20[cen - adult20.BIRTHYR >= 20], c0, str(cen))
        run("arrival_age_18plus", base[base.arr_age >= 18], c0)
        run("arrival_age_25plus", base[base.arr_age >= 25], c0)
        run("arrival_age_20plus_certain", base[base.arr_age_min >= 20], c0)
        run("not_enrolled", adult20[adult20.SCHOOL != 2], c0)
        run("both_sex_reference", adult20, c0, sexref="T")
        run("credential_convention", adult20, c0, five=FIVE_CREDENTIAL)
        for sp in ("neutral", "low", "high"):
            run(f"split_{sp}", adult20, c0, split=sp)
        g12 = adult20.copy()
        g12.loc[g12.EDUCD == 61, ["lo", "hi"]] = 13
        run("12th_no_diploma_as_upper_secondary", g12, c0)
        coded = {"as coded": adult20}
        for phi in (0.25, 0.5):   # secundaria reported as a US high-school diploma (no diploma item in 1980)
            gs = adult20.copy()
            hs = gs.EDUCD.isin([62, 63])
            moved = gs[hs].copy()
            moved[["lo", "hi"]] = 9
            moved["PERWT"] = moved.PERWT * phi
            gs.loc[hs, "PERWT"] = gs.loc[hs, "PERWT"] * (1 - phi)
            coded[f"secundaria_as_diploma_{phi}"] = pd.concat([gs, moved])
            run(f"secundaria_as_diploma_{phi}", coded[f"secundaria_as_diploma_{phi}"], c0)
        for r in specs[n0:]:
            r.update(meta)
        # undercount alone, and combined with the larger secundaria-as-diploma correction
        for coding in ("as coded", "secundaria_as_diploma_0.5"):
            for r in undercount(coded[coding], origin, emp, c0):
                under.append({**meta, "coding": coding, "ref_census": MAIN_REF[c0], "n": len(adult20),
                              "noncit_share": float((adult20.PERWT * adult20.noncit).sum() / adult20.PERWT.sum()),
                              **r})
        # the same cohort observed in later surveys (survivors), fixed reference census
        for s2 in (1980, 1990, 2000, 2005, 2010, 2015, 2019, 2024):
            if s2 < s:
                continue
            g2 = cohort_rows(d, s2, c0, c1)
            g2 = g2[g2.arr_age >= 20]
            if len(g2) < 30:
                continue
            r = summarize(g2, origin, emp, c0, "nearest")
            drift.append({"cohort": tag, "survey": s2, "ref_census": MAIN_REF[c0], "n": r["n"], "wN": r["wN"],
                          "ridit": r["ridit"], "ridit_se": r["ridit_se"],
                          **{f"mig_{k[:2]}": r[f"mig_{k}"] for k in FIVE},
                          "hs_diploma_share": float(g2.PERWT[g2.EDUCD.isin([60, 62, 63, 64])].sum() / g2.PERWT.sum()),
                          "grade9_share": float(g2.PERWT[g2.EDUCD == 30].sum() / g2.PERWT.sum()),
                          "enrolled_share": float((g2.PERWT * (g2.SCHOOL == 2)).sum() / g2.PERWT.sum())})
    # alternative surveys for the two most recent cohorts
    for (c0, c1), s in (((2015, 2019), 2021), ((2015, 2019), 2020), ((2020, 2023), 2023)):
        g = cohort_rows(d, s, c0, c1)
        n0 = len(specs)
        run(f"survey{s}", g[g.arr_age >= 20], c0)
        for r in specs[n0:]:
            r.update({"cohort": f"{c0}-{c1}", "survey": s})

    # one instrument, one date and one reference census for every cohort
    for s in (2019, 2024):
        for c0, c1 in COHORTS:
            if c0 > s:
                continue
            g = cohort_rows(d, s, c0, c1)
            n0 = len(specs)
            run(f"acs{s}_ref2020", g[(g.arr_age >= 20) & (2020 - g.BIRTHYR >= 20)], c0, "2020")
            for r in specs[n0:]:
                r.update({"cohort": f"{c0}-{c1}", "survey": s})

    S = pd.DataFrame(specs)
    lead = ["cohort", "survey", "spec", "sex", "rule", "ref_censuses", "n", "wN", "clamped_share", "position",
            "ridit", "ridit_se"]
    S = S[lead + [c for c in S.columns if c not in lead]]
    S.to_csv(OUT / "position_all_specs.csv", index=False, float_format="%.5f")
    pd.DataFrame(under).to_csv(OUT / "undercount_sensitivity.csv", index=False, float_format="%.5f")
    pd.DataFrame(drift).to_csv(OUT / "survivor_drift.csv", index=False, float_format="%.5f")
    main_tab = S[S.spec == "main"]
    main_tab.to_csv(OUT / "position_main.csv", index=False, float_format="%.5f")
    pd.set_option("display.width", 250)
    show = ["cohort", "survey", "sex", "ref_censuses", "n", "clamped_share", "ridit", "ridit_se", "q1", "q5",
            "mig_c1_none_primary_incomplete", "mex_c1_none_primary_incomplete", "mig_c5_tertiary", "mex_c5_tertiary",
            "position"]
    print(main_tab[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()
