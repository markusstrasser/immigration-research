"""Shared loaders and weighted estimators for the CPS civic-participation lane.

Data: api.census.gov CPS November Voting & Registration Supplement (PES1/PES2, weight
PWSSWGT) and September Volunteering & Civic Life Supplement (PES13-PES18, weight PWNRWGT),
pulled by scripts/pull.sh into _cache/cps_<supp>_<year>.json.

Group definitions (person level, adults 18+, adult household members only):
  IN1  India-born      PENATVTY 210 & PRCITSHP in {4,5}
  CN1  China-born      PENATVTY 207 (mainland only; HK 209 / Taiwan 240 excluded)
  MX1  Mexico-born     PENATVTY 303
  OFB  other foreign-born
  IN2  2nd-gen Indian  native-born & (PEFNTVTY 210 or PEMNTVTY 210)
  NHW  US-born non-Hispanic white   native-born & PEHSPNON 2 & PTDTRACE 1
  USB  all US-born     PRCITSHP in {1,2,3}

SEs: Kish design-effect approximation from weight variation alone,
     n_eff = (sum w)^2 / sum w^2 ; SE = sqrt(p(1-p)/n_eff).
     This ignores CPS clustering/stratification, so it is a LOWER bound on the true SE.
     scripts/replicate_check.py validates it against the shipped successive-difference
     replicate weights for Sep 2023.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"

INDIA, CHINA, MEXICO = 210, 207, 303
NATIVE = (1, 2, 3)          # PRCITSHP: native born US / PR-outlying / abroad of US parents
FOREIGN = (4, 5)            # naturalized / non-citizen
US_AREA = (57, 60, 66, 69, 73, 78)  # PENATVTY codes counted as US-born parentage

GROUP_ORDER = [
    "1 India-born",
    "2 China-born",
    "3 Mexico-born",
    "4 Other foreign-born",
    "5 Indian 2nd gen",
    "6 US-born NH white",
    "7 All US-born",
]

NUMERIC = {
    "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRCITSHP", "PRTAGE", "PESEX", "PEEDUCA",
    "HEFAMINC", "GTMETSTA", "PRDASIAN", "PEHSPNON", "PRPERTYP", "HURESPLI", "PULINENO",
    "PES1", "PES2", "PES4", "PES6", "PES7", "PES13", "PES15", "PES16", "PES17", "PES18",
    "PTS16E", "PRSUPVOL", "PUSLFPRX", "state",
}
WEIGHTS = {"PWSSWGT", "PWNRWGT"}


def load(path: Path) -> pd.DataFrame:
    rows = json.loads(path.read_text())
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in df.columns:
        if c in WEIGHTS:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        elif c in NUMERIC or c == "PTDTRACE":
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    return df


def assign_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Add `grp` (mutually exclusive, USB overlaps by design and is handled separately)."""
    d = df.copy()
    native = d.PRCITSHP.isin(NATIVE)
    fb = d.PRCITSHP.isin(FOREIGN)
    par_india = d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA)
    nhw = d.PEHSPNON.eq(2) & d.PTDTRACE.eq(1)

    d["grp"] = pd.NA
    d.loc[fb, "grp"] = "4 Other foreign-born"
    d.loc[fb & d.PENATVTY.eq(INDIA), "grp"] = "1 India-born"
    d.loc[fb & d.PENATVTY.eq(CHINA), "grp"] = "2 China-born"
    d.loc[fb & d.PENATVTY.eq(MEXICO), "grp"] = "3 Mexico-born"
    d.loc[native & par_india, "grp"] = "5 Indian 2nd gen"
    d.loc[native & ~par_india & nhw, "grp"] = "6 US-born NH white"
    d["is_usborn"] = native
    d["foreign_born"] = fb
    return d


def adults(df: pd.DataFrame, weight: str) -> pd.DataFrame:
    return df[(df.PRTAGE >= 18) & df.PRPERTYP.isin([2, 3]) & (df[weight] > 0)].copy()


def kish_neff(w: np.ndarray) -> float:
    s = w.sum()
    return float(s * s / (w * w).sum()) if len(w) and (w * w).sum() > 0 else 0.0


def wrate(d: pd.DataFrame, num: pd.Series, weight: str) -> dict:
    """Weighted proportion with Kish-effective-n SE. `num` is a boolean over d's index."""
    w = d[weight].to_numpy(float)
    y = num.reindex(d.index).fillna(False).to_numpy(bool).astype(float)
    if w.sum() <= 0:
        return dict(n=len(d), wpop=0.0, rate=float("nan"), se=float("nan"), neff=0.0)
    p = float((w * y).sum() / w.sum())
    neff = kish_neff(w)
    se = float(np.sqrt(max(p * (1 - p), 0.0) / neff)) if neff > 0 else float("nan")
    return dict(n=int(len(d)), wpop=float(w.sum()), rate=p, se=se, neff=neff)


def rate_table(d: pd.DataFrame, num: pd.Series, weight: str, min_n: int = 50,
               extra_rows: dict | None = None) -> pd.DataFrame:
    """Rate by `grp`, plus All US-born and any extra named subsets. Cells n<min_n suppressed."""
    out = []
    for g in GROUP_ORDER[:-1]:
        sub = d[d.grp.eq(g)]
        r = wrate(sub, num, weight)
        r["group"] = g
        out.append(r)
    sub = d[d.is_usborn]
    r = wrate(sub, num, weight)
    r["group"] = "7 All US-born"
    out.append(r)
    for name, mask in (extra_rows or {}).items():
        sub = d[mask.reindex(d.index).fillna(False)]
        r = wrate(sub, num, weight)
        r["group"] = name
        out.append(r)
    t = pd.DataFrame(out)[["group", "n", "wpop", "rate", "se", "neff"]]
    t.loc[t.n < min_n, ["rate", "se"]] = float("nan")   # suppression
    return t.sort_values("group", kind="stable").reset_index(drop=True)


def fmt(t: pd.DataFrame) -> pd.DataFrame:
    """Deterministic rounding for byte-identical CSV output."""
    t = t.copy()
    for c in t.columns:
        if t[c].dtype.kind == "f":
            t[c] = t[c].round(6)
    return t


def write_csv(t: pd.DataFrame, name: str) -> Path:
    DERIVED.mkdir(exist_ok=True)
    p = DERIVED / name
    fmt(t).to_csv(p, index=False, lineterminator="\n", float_format="%.6f")
    return p
