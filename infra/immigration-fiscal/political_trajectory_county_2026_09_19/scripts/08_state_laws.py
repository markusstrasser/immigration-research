#!/usr/bin/env python3
"""Arm 4: do the laws follow the group's size, or the rest of the electorate's
politics?

Policy data: Correlates of State Policy Project v2.2 (Michigan State University
IPPSR), public CSV. The variables this lane can use:
  immigration_instate_tuition_illegalimmigrants  binary, 2001-2014
  immig_laws_restrict / immig_laws_accom / _total counts, 2005-2012 (compiled
      from the NCSL annual immigration-law reports)
  pctlatinoleg    Latino share of the state legislature, 2005-2015
NOT in this release, so NOT covered here rather than filled from memory: driver's
licences for unauthorized immigrants, E-Verify mandates, sanctuary and
anti-sanctuary statutes, 287(g) agreements.

Predictors, both built inside this lane:
  mex_share_pp_2010     Mexican-origin share of the state population (decennial)
  nonhisp_dem2p_2008    the Democratic two-party share in that state's counties
      below 10% Mexican origin in 2008 - a survey-free stand-in for how the rest
      of the electorate votes
n is about 48 states, so the tests are a logit, a rank correlation and a plain
2x2 ordering table, and the smallness is reported with them.

Output: derived/state_law_table.csv, derived/state_laws.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
DER = LANE / "derived"
URL = ("https://ippsr.msu.edu/sites/default/files/"
       "correlatesofstatepolicyprojectv2_2.csv")
COLS = ["year", "st", "state", "state_fips",
        "immigration_instate_tuition_illegalimmigrants",
        "immig_laws_restrict", "immig_laws_accom", "immig_laws_total",
        "pctlatinoleg"]
TXT: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    TXT.append(s)


def fetch() -> Path:
    dest = CACHE / "correlatesofstatepolicyprojectv2_2.csv"
    if dest.exists() and dest.stat().st_size > 20_000_000:
        print(f"cached {dest.name} ({dest.stat().st_size/1e6:.1f} MB)", flush=True)
        return dest
    try:
        r = requests.get(URL, timeout=900)
        r.raise_for_status()
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else "?"
        sys.exit(f"FAIL HTTP {code} fetching the Correlates of State Policy CSV")
    except requests.RequestException as e:
        sys.exit(f"FAIL {type(e).__name__} fetching the Correlates CSV")
    if len(r.content) < 20_000_000 or not r.content.lstrip()[:20].lower().startswith(
            b"\xef\xbb\xbfyear") and not r.content.lstrip()[:5].lower().startswith(b"year"):
        sys.exit(f"FAIL Correlates body looks wrong: {len(r.content):,} bytes, "
                 f"starts {r.content[:40]!r}")
    dest.write_bytes(r.content)
    print(f"wrote {dest.name} {len(r.content):,} bytes", flush=True)
    return dest


def logit(y: np.ndarray, X: np.ndarray, iters: int = 100) -> tuple:
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = X @ b
        pr = 1 / (1 + np.exp(-eta))
        W = pr * (1 - pr)
        H = X.T @ (X * W[:, None]) + 1e-8 * np.eye(X.shape[1])
        g = X.T @ (y - pr)
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    eta = X @ b
    pr = 1 / (1 + np.exp(-eta))
    V = np.linalg.pinv(X.T @ (X * (pr * (1 - pr))[:, None]))
    return b, np.sqrt(np.diag(V))


def main() -> int:
    DER.mkdir(exist_ok=True)
    path = fetch()
    d = pd.read_csv(path, usecols=COLS, encoding="utf-8-sig", low_memory=False)
    n_states = d.st.nunique()
    say(f"Correlates of State Policy v2.2: {len(d):,} state-years, "
        f"{n_states} state codes, {d.year.min()}-{d.year.max()}")
    if n_states < 50:
        sys.exit(f"FAIL only {n_states} states in the Correlates file")

    tui = d.dropna(subset=["immigration_instate_tuition_illegalimmigrants"])
    adopt = (tui[tui.immigration_instate_tuition_illegalimmigrants == 1]
             .groupby("st").year.min().rename("tuition_first_year"))
    ever = tui.groupby("st").immigration_instate_tuition_illegalimmigrants.max()
    say(f"in-state tuition, 2001-2014 window: {int(ever.sum())} of {len(ever)} "
        f"states ever coded 1; first years "
        f"{adopt.min()}-{adopt.max()}")

    laws = (d[d.year.between(2005, 2012)]
            .groupby("st")[["immig_laws_restrict", "immig_laws_accom"]]
            .sum(min_count=1))
    lat = d[d.year.between(2005, 2015)].groupby("st").pctlatinoleg.mean()

    p = pd.read_csv(DER / "county_panel.csv", dtype={"fips": str, "state": str})
    p["mex_pp"] = 100 * p.mex_share
    ab = (d[["st", "state_fips"]].dropna().drop_duplicates("st")
          .assign(state=lambda x: x.state_fips.astype(int).astype(str).str.zfill(2))
          .set_index("state").st)
    s08 = p[p.year == 2008]
    rows = []
    for st_fips, g in s08.groupby("state"):
        if st_fips not in ab.index:
            continue
        low = g[g.mex_pp < 10]
        g10 = p[(p.year == 2010) & (p.state == st_fips)] if False else None
        rows.append({"st": ab[st_fips], "state_fips": st_fips,
                     "mex_share_pp": 100 * g.mex.sum() / g["pop"].sum(),
                     "nonhisp_dem2p_2008": (
                         100 * low.dem.sum() / (low.dem.sum() + low.rep.sum())
                         if low.total_votes.sum() > 0.05 * g.total_votes.sum()
                         else np.nan),
                     "state_dem2p_2008": 100 * g.dem.sum() / (g.dem.sum() + g.rep.sum()),
                     "votes_2008": g.total_votes.sum()})
    st = pd.DataFrame(rows).set_index("st")
    tab = (st.join(ever.rename("tuition_ever"))
           .join(adopt).join(laws).join(lat.rename("pct_latino_legislature")))
    tab.to_csv(DER / "state_law_table.csv")
    say(f"analysis table: {len(tab)} states; "
        f"{tab.nonhisp_dem2p_2008.isna().sum()} have no county group under 10% "
        f"Mexican origin carrying at least 5% of the state's votes, so their "
        f"stand-in is missing")

    t = tab.dropna(subset=["tuition_ever", "nonhisp_dem2p_2008", "mex_share_pp"])
    y = t.tuition_ever.to_numpy(float)
    say()
    say(f"=== in-state tuition for unauthorized immigrants, n={len(t)} states ===")
    say(f"adopters' mean Mexican-origin share {t[y == 1].mex_share_pp.mean():.1f}% "
        f"vs non-adopters {t[y == 0].mex_share_pp.mean():.1f}%")
    say(f"adopters' mean non-Hispanic-county Democratic share "
        f"{t[y == 1].nonhisp_dem2p_2008.mean():.1f} vs non-adopters "
        f"{t[y == 0].nonhisp_dem2p_2008.mean():.1f}")
    X1 = np.column_stack([np.ones(len(t)), t.mex_share_pp])
    b1, se1 = logit(y, X1)
    say(f"logit, Mexican-origin share alone:      b={b1[1]:+.4f} se={se1[1]:.4f} "
        f"z={b1[1]/se1[1]:+.2f}")
    X2 = np.column_stack([np.ones(len(t)), t.nonhisp_dem2p_2008])
    b2, se2 = logit(y, X2)
    say(f"logit, non-Hispanic-county Dem share:   b={b2[1]:+.4f} se={se2[1]:.4f} "
        f"z={b2[1]/se2[1]:+.2f}")
    X3 = np.column_stack([np.ones(len(t)), t.mex_share_pp, t.nonhisp_dem2p_2008])
    b3, se3 = logit(y, X3)
    say(f"logit, both:  mex b={b3[1]:+.4f} se={se3[1]:.4f} z={b3[1]/se3[1]:+.2f} | "
        f"non-Hisp Dem b={b3[2]:+.4f} se={se3[2]:.4f} z={b3[2]/se3[2]:+.2f}")
    say("  (n is about fifty; these are ordering tests, not identified effects)")

    med_m = t.mex_share_pp.median()
    med_d = t.nonhisp_dem2p_2008.median()
    cross = pd.crosstab([t.mex_share_pp > med_m], [t.nonhisp_dem2p_2008 > med_d],
                        values=y, aggfunc="mean")
    cross.index = ["low Mexican-origin share", "high Mexican-origin share"]
    cross.columns = ["Republican-leaning rest of state",
                     "Democratic-leaning rest of state"]
    say()
    say("share of states with in-state tuition, split at the median of each:")
    say(cross.round(2).to_string())
    n_cross = pd.crosstab([t.mex_share_pp > med_m], [t.nonhisp_dem2p_2008 > med_d])
    say("cell counts:")
    say(n_cross.to_string())

    lw = tab.dropna(subset=["immig_laws_restrict", "nonhisp_dem2p_2008"])
    say()
    say(f"=== restrictive minus accommodating immigration laws 2005-2012, "
        f"n={len(lw)} states ===")
    net = lw.immig_laws_restrict - lw.immig_laws_accom
    for name, x in (("Mexican-origin share", lw.mex_share_pp),
                    ("non-Hispanic-county Dem share", lw.nonhisp_dem2p_2008)):
        r = np.corrcoef(x.rank(), net.rank())[0, 1]
        say(f"Spearman(net restrictive laws, {name}) = {r:+.3f}")
    say("  the Correlates law counts are missing for many state-years inside "
        "2005-2012 (Texas is absent in every even year), so this is the weakest "
        "arm in the lane and is reported as an ordering, not a coefficient")
    (DER / "state_laws.txt").write_text("\n".join(TXT) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
