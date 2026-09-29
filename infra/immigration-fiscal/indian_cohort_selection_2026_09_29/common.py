"""Shared pieces for the Indian arrival-cohort lane.

Percentile definitions are the selection-curve lane's (`selection_curve_2026_09_27`), imported, not
re-implemented: a person's education or wage-earnings percentile is the weighted mid-rank in the
third-plus-generation non-Hispanic white CPS ASEC reference of the same survey year and five-year
age band (25-64), zeros included for earnings. ACS and census records are placed in that same CPS
reference through the code crosswalks below, so every percentile in this lane sits on one scale.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[2]
SC = REPO / "infra" / "immigration-fiscal" / "selection_curve_2026_09_27"
DER = LANE / "derived"
CACHE = LANE / "_cache"
sys.path.insert(0, str(SC))
import cps_curve  # noqa: E402  (selection_curve lane; imports its own `load`)

INDIA_CPS = 52100
INDIA_ACS = 210          # ACS POBP
INDIA_USA = 521          # IPUMS USA BPL
AGE_EDGES = cps_curve.AGE_EDGES
COHORTS = [(1900, 1979, "pre-1980"), (1980, 1989, "1980-89"), (1990, 1999, "1990-99"),
           (2000, 2009, "2000-09"), (2010, 2014, "2010-14"), (2015, 2019, "2015-19"),
           (2020, 2026, "2020+")]

# ACS SCHL -> CPS EDUC. Associate degrees go to 92; the reference merges 91 and 92 for these
# lookups (ACS does not split occupational and academic associate degrees).
SCHL08_TO_EDUC = {1: 2, 2: 2, 3: 2, 4: 10, 5: 10, 6: 10, 7: 10, 8: 20, 9: 20, 10: 30, 11: 30,
                  12: 40, 13: 50, 14: 60, 15: 71, 16: 73, 17: 73, 18: 81, 19: 81, 20: 92,
                  21: 111, 22: 123, 23: 124, 24: 125}
SCHL05_TO_EDUC = {1: 2, 2: 10, 3: 20, 4: 30, 5: 40, 6: 50, 7: 60, 8: 71, 9: 73, 10: 81, 11: 81,
                  12: 92, 13: 111, 14: 123, 15: 124, 16: 125}
# IPUMS USA EDUCD -> CPS EDUC (1990 and 2000 census, ACS 2010/2023 in the Borjas panel).
EDUCD_TO_EDUC = {1: 2, 2: 2, 10: 10, 11: 2, 12: 2, 13: 10, 14: 10, 15: 10, 16: 10, 17: 10,
                 20: 30, 21: 20, 22: 20, 23: 20, 24: 30, 25: 30, 26: 30, 30: 40, 40: 50, 50: 60,
                 60: 71, 61: 71, 62: 73, 63: 73, 64: 73, 65: 81, 70: 81, 71: 81, 80: 81, 81: 92,
                 82: 92, 83: 92, 90: 81, 100: 111, 101: 111, 110: 123, 111: 123, 112: 124,
                 113: 125, 114: 123, 115: 124, 116: 125}
BA_PLUS = {111, 123, 124, 125}
GRAD = {123, 124, 125}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})


def cohort_of(year: np.ndarray) -> np.ndarray:
    out = np.full(len(year), "", dtype=object)
    for lo, hi, lab in COHORTS:
        out[(year >= lo) & (year <= hi)] = lab
    return out


def cps_prepared() -> pd.DataFrame:
    """The selection-curve frame with its percentiles, cached in this lane."""
    p = CACHE / "cps_prepared.parquet"
    if p.exists():
        return pd.read_parquet(p)
    df = cps_curve.prepare()
    CACHE.mkdir(exist_ok=True)
    df.to_parquet(p, index=False)
    return df


class Reference:
    """CPS G3+ NH white reference cells (ASEC year x band) for placing outside records."""

    def __init__(self, df: pd.DataFrame):
        cpi = cps_curve.cpi_factor()             # ASEC year -> 2024 $ of its income year
        r = df.loc[df.ref.to_numpy()]
        self.cells: dict[tuple[str, int, int], tuple[np.ndarray, np.ndarray]] = {}
        for (yr, band), g in r.groupby(["year", "band"]):
            e = g[g.educ_ok]
            ed = e.educ.replace({91: 92}).to_numpy(float)
            self.cells[("educ", yr, band)] = (ed, e.w.to_numpy())
            m = g[g.earn_ok]
            self.cells[("earn", yr, band)] = (m.earn.to_numpy(float) * cpi[yr], m.w.to_numpy())
        self.years = sorted({k[1] for k in self.cells})

    def pct(self, var: str, year: np.ndarray, band: np.ndarray, value: np.ndarray) -> np.ndarray:
        """Mid-rank percentile of `value` (educ code, or 2024-$ wages) in the reference cell."""
        out = np.full(len(value), np.nan)
        year = np.asarray(year)
        band = np.asarray(band)
        value = np.asarray(value, float)
        keys = pd.MultiIndex.from_arrays([year, band])
        for (yr, b), idx in pd.Series(np.arange(len(value)), index=keys).groupby(level=[0, 1]):
            cell = self.cells.get((var, int(yr), int(b)))
            if cell is None or b < 0 or b >= len(AGE_EDGES) - 1:
                continue
            ix = idx.to_numpy()
            ok = np.isfinite(value[ix])
            out[ix[ok]] = cps_curve.midrank_pct(cell[0], cell[1], value[ix[ok]])
        return out


def band_of(age: np.ndarray) -> np.ndarray:
    b = np.digitize(age, AGE_EDGES) - 1
    return np.where((age >= 25) & (age <= 64), b, -1)
