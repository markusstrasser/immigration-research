"""Shared definitions for the movers' reasons lane: reason groups, sample flags, loaders and the
variance machinery (successive-difference replicate weights from ASEC 2005, a design-factor-scaled
household-cluster variance before that)."""
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
BUILD = CACHE / "build"
DERIVED = HERE / "derived"
NREP = 160

# IPUMS WHYMOVE -> the brief's reason groups
REASON_GROUP = {1: "family", 2: "family", 3: "family", 20: "family",
                4: "jobs", 5: "jobs", 6: "jobs", 8: "jobs",
                7: "retirement",
                9: "housing", 10: "housing", 12: "housing", 13: "housing", 19: "housing",
                11: "neighborhood_crime",
                15: "climate",
                14: "other", 16: "other", 17: "other", 18: "other"}
GROUPS = ["housing", "jobs", "family", "neighborhood_crime", "climate", "retirement", "other"]
DETAIL = {1: "change in marital status", 2: "establish own household", 3: "other family reason",
          20: "relationship with unmarried partner", 4: "new job or transfer", 5: "look for work or lost job",
          6: "easier commute", 8: "other job-related", 7: "retired", 9: "own home, not rent",
          10: "new or better housing", 12: "cheaper housing", 13: "other housing reason",
          19: "foreclosure or eviction", 11: "better neighborhood/less crime", 15: "change of climate",
          14: "attend or leave college", 16: "health", 17: "other reason", 18: "natural disaster"}
STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
          13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
          23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
          32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
          41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
          51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}
ANOMALY_YEARS = (2012, 2013, 2014, 2015)  # NXTRES college/climate/health/other collapse into "other housing"


def con():
    c = duckdb.connect()
    c.execute("SET memory_limit='1500MB'; SET threads=2")
    return c


def cpi_2024(c) -> dict:
    """Survey year -> factor converting that survey's prior-year dollars into 2024 dollars
    (IPUMS CPI99 converts to 1999 dollars; ASEC 2025 carries 2024 incomes)."""
    cpi = dict(c.execute(f"select YEAR, max(CPI99) from read_parquet('{BUILD / 'movers.parquet'}') group by 1").fetchall())
    return {y: v / cpi[2025] for y, v in cpi.items()}


def add_person_fields(d: pd.DataFrame, cpi: dict) -> pd.DataFrame:
    d = d.copy()
    d["usb"] = d.BPL == 9900
    d["adult"] = d.AGE >= 18
    d["group"] = d.WHYMOVE.map(REASON_GROUP)
    for g in GROUPS:
        d[g] = (d.group == g).astype(float)
    d["cheaper_housing"] = (d.WHYMOVE == 12).astype(float)
    d["better_housing"] = (d.WHYMOVE == 10).astype(float)
    d["own_home"] = (d.WHYMOVE == 9).astype(float)
    hisp = d.HISPAN.between(1, 612)
    mex = d.HISPAN.between(100, 109)
    d["race_eth"] = np.select(
        [mex, hisp, d.RACE == 100, d.RACE == 200, d.RACE.isin([650, 651, 652])],
        ["Hispanic, Mexican-origin", "Hispanic, other", "non-Hispanic white", "non-Hispanic Black",
         "non-Hispanic Asian or Pacific Islander"], default="non-Hispanic other or multiple")
    d["educ4"] = np.select([d.EDUC < 73, d.EDUC.between(73, 73), d.EDUC.between(80, 100), d.EDUC >= 110],
                           ["less than high school", "high school", "some college or associate", "bachelor's or more"],
                           default="unknown")
    d.loc[d.EDUC >= 999, "educ4"] = "unknown"
    inc = d.HHINCOME.where(d.HHINCOME < 99999999)
    d["hhinc24"] = inc * d.YEAR.map(cpi)
    d["inc_band"] = pd.cut(d.hhinc24, [-np.inf, 50_000, 100_000, 150_000, np.inf],
                           labels=["under $50k", "$50k-100k", "$100k-150k", "$150k or more"]).astype(str)
    d["age_band"] = pd.cut(d.AGE, [17, 34, 54, 64, 200], labels=["18-34", "35-54", "55-64", "65+"]).astype(str)
    # migration status or origin state allocated from the hot-deck matrix
    d["allocated"] = (d.QMIGRAT1 == 3) | (d.QMIGST1B >= 4)
    return d


def load_interstate(c, cpi: dict) -> pd.DataFrame:
    """Interstate movers (MIGRATE1 = 5), every year, with replicate weights joined for 2005+."""
    d = c.execute(f"""
        select m.*, {', '.join(f'r.r{i}' for i in range(1, NREP + 1))}
        from read_parquet('{BUILD / 'movers.parquet'}') m
        left join read_parquet('{BUILD / 'repwt.parquet'}') r using (YEAR, SERIAL, PERNUM)
        where m.MIGRATE1 = 5""").df()
    for i in range(1, NREP + 1):
        d[f"r{i}"] = d[f"r{i}"].astype("float32")
    if d.loc[d.YEAR >= 2005, "r1"].isna().any():
        raise SystemExit("[FAILED] interstate movers 2005+ without replicate weights")
    return add_person_fields(d, cpi)


REP = [f"r{i}" for i in range(1, NREP + 1)]


class Var:
    """Point estimates and variances for weighted ratios and totals over a subset of rows.

    ASEC 2005+: successive-difference replication, Var = 4/160 * sum_r (theta_r - theta)^2.
    ASEC 1999-2004 (no replicate weights): the with-replacement household-cluster variance of the
    linearised statistic, multiplied by DESIGN_FACTOR^2, the median ratio of replicate to cluster
    variance measured on the same kind of statistic in 2005-2025 (set by calibrate())."""
    DESIGN_FACTOR = None

    @staticmethod
    def _cluster_var(z: np.ndarray, cluster: np.ndarray) -> float:
        if len(z) == 0:
            return 0.0
        s = pd.Series(z).groupby(cluster).sum().to_numpy()
        n = len(s)
        return float(n / (n - 1) * ((s - s.mean()) ** 2).sum()) if n > 1 else 0.0

    @classmethod
    def ratio(cls, d: pd.DataFrame, y: str, *, factor: float | None = None) -> tuple[float, float, float, float]:
        """Weighted mean of y over d: (theta, se, se_replicate_part, se_cluster_part)."""
        w = d.wt.to_numpy(float)
        yy = d[y].to_numpy(float)
        W = w.sum()
        theta = float((w * yy).sum() / W) if W > 0 else np.nan
        a = (d.YEAR >= 2005).to_numpy()
        var_a = 0.0
        if a.any():
            num_b = (w[~a] * yy[~a]).sum()
            den_b = w[~a].sum()
            R = d.loc[a, REP].to_numpy(float)
            th_r = ((R * yy[a, None]).sum(0) + num_b) / (R.sum(0) + den_b)
            var_a = float(4 / NREP * ((th_r - theta) ** 2).sum())
        var_b = 0.0
        if (~a).any():
            z = w[~a] * (yy[~a] - theta) / W
            cl = (d.loc[~a, "YEAR"].astype(str) + "_" + d.loc[~a, "SERIAL"].astype(str)).to_numpy()
            f = cls.DESIGN_FACTOR if factor is None else factor
            var_b = cls._cluster_var(z, cl) * (f ** 2 if f else 1.0)
        return theta, float(np.sqrt(var_a + var_b)), float(np.sqrt(var_a)), float(np.sqrt(var_b))

    @classmethod
    def diff(cls, d1: pd.DataFrame, d2: pd.DataFrame, y: str) -> tuple[float, float]:
        """theta1 - theta2 with SE; replicate part computed jointly, cluster part summed."""
        t1, _, _, c1 = cls.ratio(d1, y)
        t2, _, _, c2 = cls.ratio(d2, y)
        reps = []
        for dd, t in ((d1, t1), (d2, t2)):
            w = dd.wt.to_numpy(float)
            yy = dd[y].to_numpy(float)
            a = (dd.YEAR >= 2005).to_numpy()
            R = dd.loc[a, REP].to_numpy(float)
            num_b, den_b = (w[~a] * yy[~a]).sum(), w[~a].sum()
            reps.append(((R * yy[a, None]).sum(0) + num_b) / (R.sum(0) + den_b) if a.any() else np.full(NREP, t))
        dr = reps[0] - reps[1]
        var_a = 4 / NREP * ((dr - (t1 - t2)) ** 2).sum()
        return t1 - t2, float(np.sqrt(var_a + c1 ** 2 + c2 ** 2))

    @classmethod
    def total(cls, d: pd.DataFrame, years: int) -> tuple[float, float]:
        """Weighted count per year (sum of weights / years) and its SE."""
        w = d.wt.to_numpy(float)
        tot = w.sum()
        a = (d.YEAR >= 2005).to_numpy()
        var = 0.0
        if a.any():
            R = d.loc[a, REP].to_numpy(float)
            tr = R.sum(0) + w[~a].sum()
            var += 4 / NREP * ((tr - tot) ** 2).sum()
        if (~a).any():
            cl = (d.loc[~a, "YEAR"].astype(str) + "_" + d.loc[~a, "SERIAL"].astype(str)).to_numpy()
            var += cls._cluster_var(w[~a], cl) * (cls.DESIGN_FACTOR ** 2 if cls.DESIGN_FACTOR else 1.0)
        return tot / years, float(np.sqrt(var)) / years

    @classmethod
    def calibrate(cls, d: pd.DataFrame) -> dict:
        """Median ratio of replicate SE to household-cluster SE for reason-group shares, 2005-2025."""
        ratios = []
        dd = d[d.YEAR >= 2005]
        for g in GROUPS:
            theta = float((dd.wt * dd[g]).sum() / dd.wt.sum())
            _, se, se_rep, _ = cls.ratio(dd, g)
            z = dd.wt.to_numpy(float) * (dd[g].to_numpy(float) - theta) / dd.wt.sum()
            cl = (dd.YEAR.astype(str) + "_" + dd.SERIAL.astype(str)).to_numpy()
            se_cl = np.sqrt(cls._cluster_var(z, cl))
            if se_cl > 0:
                ratios.append(se_rep / se_cl)
        cls.DESIGN_FACTOR = float(np.median(ratios))
        return {"design_factor": cls.DESIGN_FACTOR, "ratios": [round(r, 3) for r in ratios]}


def write_csv(df: pd.DataFrame, name: str) -> Path:
    DERIVED.mkdir(exist_ok=True)
    p = DERIVED / name
    df.to_csv(p, index=False, lineterminator="\n")
    return p
