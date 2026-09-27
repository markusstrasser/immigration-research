"""ACS 2019/2021/2022/2023 1-year PUMS, Mexico-born: rates by arrival class and five-year age band.

Reads the sister lane's cached Census API responses read-only
(`late_arrival_tail_2026_09_27/_cache/acs/pums/<year>_mexico_A_<state>.json`, 51 states a year; that lane's
`acs_late_arrival.py` fetched them). Foreign-born only (NATIVITY 2): POBP 303 also returns natives born
abroad to US-citizen parents, which that lane drops the same way. Weights PWGTP / 4 (a pooled year).

Age at arrival is exact to the year here: AGEP - (survey year - YOEP), floored at 0 (the sister lane's
`arrival_age`). Classes: Y (< 50), L50 (50-54), L55 (55+), the same cuts as frame.py's G1 cells.

Proxies (the long-term-care lane's central proxies without the disability items, which the cached pull
does not carry):
  inst          institutionalized group quarters (RELSHIPP 37): the nursing-facility users' proxy;
  all           every resident: the mental-health-facility proxy;
  comm_medicaid community residents (not RELSHIPP 37) with Medicaid (HINS4 1): the ICF/IID and HCBS proxy,
                which the LTSS lane narrows further by a cognitive, self-care or independent-living difficulty.
  medicaid, medicare  coverage rates (HINS4 1, HINS3 1), for the pricing check.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PUMS = HERE.parent / "late_arrival_tail_2026_09_27/_cache/acs/pums"
YEARS = [2019, 2021, 2022, 2023]
STATES = [f"{i:02d}" for i in range(1, 57) if i not in (3, 7, 14, 43, 52)]
COLS = ["PWGTP", "AGEP", "YOEP", "HINS3", "HINS4", "RELSHIPP", "NATIVITY"]
BAND_EDGES = list(range(0, 90, 5))  # 0-4, ..., 80-84, 85+


@lru_cache(maxsize=1)
def load():
    frames = []
    for year in YEARS:
        for st in STATES:
            rows = json.loads((PUMS / f"{year}_mexico_A_{st}.json").read_text())
            if not rows:
                continue
            hdr = rows[0]
            idx = [hdr.index(c) for c in COLS]
            frames.append(pd.DataFrame([[r[i] for i in idx] for r in rows[1:]], columns=COLS).astype(float)
                          .assign(year=year))
    d = pd.concat(frames, ignore_index=True)
    d = d[d.NATIVITY.eq(2)].copy()
    if len(YEARS) != d.year.nunique():
        raise SystemExit("[BLOCKED] ACS years missing from the sister lane's cache")
    d["w"] = d.PWGTP / len(YEARS)
    d["alpha"] = np.maximum(d.AGEP - (d.year - d.YOEP), 0)
    d["cls"] = np.where(d.alpha < 50, "Y", np.where(d.alpha < 55, "L50", "L55"))
    d["band"] = np.minimum(d.AGEP // 5 * 5, 85).astype(int)
    inst = d.RELSHIPP.eq(37)
    d["inst"] = inst.astype(float)
    d["all"] = 1.0
    d["comm_medicaid"] = (~inst & d.HINS4.eq(1)).astype(float)
    d["medicaid"] = d.HINS4.eq(1).astype(float)
    d["medicare"] = d.HINS3.eq(1).astype(float)
    return d


@lru_cache(maxsize=None)
def rates(proxy):
    """{(cls, band): weighted share of the cell in the proxy}; a class-band cell with no ACS record takes
    the band's all-class rate."""
    d = load()
    num = d.assign(x=d[proxy] * d.w).groupby(["cls", "band"]).x.sum()
    den = d.groupby(["cls", "band"]).w.sum()
    out = (num / den).to_dict()
    band = (d.assign(x=d[proxy] * d.w).groupby("band").x.sum() / d.groupby("band").w.sum()).to_dict()
    for c in ("Y", "L50", "L55"):
        for b in range(0, 90, 5):
            out.setdefault((c, b), band.get(b, 0.0))
    return out


def person_rate(proxy, cls, age):
    """Per-person proxy rate for arrays of classes and ages (CPS persons, classed under frame.LATE_DEF)."""
    r = rates(proxy)
    band = np.minimum(np.asarray(age) // 5 * 5, 85).astype(int)
    return np.array([r[(c, int(b))] for c, b in zip(cls, band)])
