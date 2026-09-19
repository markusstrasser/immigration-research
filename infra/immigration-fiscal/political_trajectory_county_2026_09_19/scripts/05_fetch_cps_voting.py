#!/usr/bin/env python3
"""Arm 2/3 step 1: CPS November Voting and Registration Supplement, presidential
years 2004-2024, from the Census API (cps/voting/nov).

2000 is not on the API (HTTP 400 for every variable set tried), so the CPS series
starts in 2004 and that is stated rather than patched.

Per person: PWSSWGT (supplement weight), PES1 (did you vote), PRCITSHP,
PEHSPNON, PRDTHSP (Mexican = 1 in every vintage used), PRTAGE, PENATVTY, state.

Validation is by content: weighted citizen-voting-age population inside a
published band for the year, and reported turnout of citizens inside 2 points of
the Census Bureau's published CPS figure (the CPS overstates turnout against the
vote count; the check is against the CPS's own published number, not the count).

Output (gitignored): _cache/cps_voting_<year>.parquet
        derived/cps_voting_state.csv, derived/cps_voting_national.csv
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
DER = LANE / "derived"
YEARS = [2004, 2008, 2012, 2016, 2020, 2024]
VARS = ["PWSSWGT", "PES1", "PRCITSHP", "PEHSPNON", "PRDTHSP", "PRTAGE",
        "PENATVTY", "PESEX", "PEEDUCA"]
# Census Bureau published CPS citizen turnout (percent of citizens 18+ reporting
# a vote) and citizen VAP, used as a +/- band content check.
# [TRAINING-DATA: Census Bureau Table 2/4a, "Voting and Registration in the
#  Election of November <year>"; band check only, no claim rests on it]
PUB_CIT_TURNOUT = {2004: 63.8, 2008: 63.6, 2012: 61.8, 2016: 61.4,
                   2020: 66.8, 2024: 65.0}
PUB_CVAP_M = {2004: (195, 205), 2008: (203, 212), 2012: (212, 222),
              2016: (220, 230), 2020: (228, 240), 2024: (236, 252)}


def key() -> str:
    k = os.environ.get("CENSUS_API_KEY")
    if not k:
        sys.exit("CENSUS_API_KEY not in environment; source config.local.env")
    return k


def pull(year: int, k: str) -> pd.DataFrame:
    dest = CACHE / f"cps_voting_{year}.parquet"
    if dest.exists():
        return pd.read_parquet(dest)
    frames = []
    for attempt in (1, 2, 3):
        try:
            r = requests.get(f"https://api.census.gov/data/{year}/cps/voting/nov",
                             params={"get": ",".join(VARS), "for": "state:*",
                                     "key": k}, timeout=600)
            r.raise_for_status()
            break
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else "?"
            print(f"  HTTP {code} (attempt {attempt})", flush=True)
            if attempt == 3:
                sys.exit(f"FAIL CPS {year}: HTTP {code}")
        except requests.RequestException as e:
            print(f"  {type(e).__name__} (attempt {attempt})", flush=True)
            if attempt == 3:
                sys.exit(f"FAIL CPS {year}: {type(e).__name__}")
    if not r.text.lstrip().startswith("["):
        sys.exit(f"FAIL CPS {year}: non-JSON body {r.text[:120]!r}")
    rows = r.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if len(df) < 80_000:
        sys.exit(f"FAIL CPS {year}: only {len(df):,} person rows (truncated?)")
    frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out.to_parquet(dest, index=False)
    return out


def derive(df: pd.DataFrame, year: int) -> pd.DataFrame:
    d = df.copy()
    # PWSSWGT carries four implied decimals in the public file; the API returns it
    # already as a decimal number in some vintages. Detect by the implied total.
    w = d.PWSSWGT.astype(float)
    if w.sum() > 1e10:
        w = w / 1e4
    d["w"] = w
    d = d[(d.PRTAGE >= 18)]
    d["citizen"] = d.PRCITSHP.isin([1, 2, 3, 4])
    d["hisp"] = d.PEHSPNON == 1
    d["mex"] = d.hisp & (d.PRDTHSP == 1)
    d["foreign"] = d.PRCITSHP.isin([4, 5])
    d["voted"] = d.PES1 == 1
    d["group"] = np.where(d.mex, "mexican",
                          np.where(d.hisp, "hisp_other", "non_hispanic"))
    d["year"] = year
    return d


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    DER.mkdir(exist_ok=True)
    k = key()
    nat_rows, st_rows = [], []
    for y in YEARS:
        print(f"CPS November {y}", flush=True)
        d = derive(pull(y, k), y)
        cit = d[d.citizen]
        cvap = cit.w.sum() / 1e6
        turn = 100 * cit.loc[cit.voted, "w"].sum() / cit.w.sum()
        lo, hi = PUB_CVAP_M[y]
        ok_c = lo <= cvap <= hi
        ok_t = abs(turn - PUB_CIT_TURNOUT[y]) <= 2.0
        print(f"  n={len(d):,} 18+ ; citizen VAP {cvap:.1f}M (band {lo}-{hi}) "
              f"{'OK' if ok_c else 'FAIL'}; citizen turnout {turn:.1f}% vs "
              f"published CPS {PUB_CIT_TURNOUT[y]} {'OK' if ok_t else 'FAIL'}",
              flush=True)
        if not (ok_c and ok_t):
            sys.exit(f"FAIL CPS {y} content check")
        for g, sub in cit.groupby("group"):
            nat_rows.append({
                "year": y, "group": g,
                "cvap_m": sub.w.sum() / 1e6,
                "voters_m": sub.loc[sub.voted, "w"].sum() / 1e6,
                "turnout_pct": 100 * sub.loc[sub.voted, "w"].sum() / sub.w.sum(),
                "foreign_born_pct": 100 * sub.loc[sub.foreign, "w"].sum() / sub.w.sum(),
                "share_of_cvap_pct": 100 * sub.w.sum() / cit.w.sum(),
                "share_of_voters_pct": (100 * sub.loc[sub.voted, "w"].sum()
                                        / cit.loc[cit.voted, "w"].sum())})
        for (st, g), sub in cit.groupby(["state", "group"]):
            tot = cit[cit.state == st]
            st_rows.append({
                "year": y, "state_fips": f"{int(st):02d}", "group": g,
                "cvap_m": sub.w.sum() / 1e6,
                "voters_m": sub.loc[sub.voted, "w"].sum() / 1e6,
                "turnout_pct": 100 * sub.loc[sub.voted, "w"].sum() / sub.w.sum(),
                "share_of_cvap_pct": 100 * sub.w.sum() / tot.w.sum(),
                "share_of_voters_pct": (100 * sub.loc[sub.voted, "w"].sum()
                                        / tot.loc[tot.voted, "w"].sum()),
                "n_unweighted": len(sub)})
    nat = pd.DataFrame(nat_rows)
    st = pd.DataFrame(st_rows)
    nat.to_csv(DER / "cps_voting_national.csv", index=False)
    st.to_csv(DER / "cps_voting_state.csv", index=False)
    print("\nnational, by group:", flush=True)
    print(nat.pivot(index="year", columns="group",
                    values=["share_of_voters_pct", "turnout_pct"]).round(2)
          .to_string(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
