"""Registration and turnout by birthplace, CPS November Voting & Registration Supplement.

Two conventions, both reported:
  census  : non-response to PES1 counted as NOT voted; denominator = all citizens 18+
            (this is the convention behind the published P20 tables)
  reported: non-response dropped from the denominator

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 scripts/analyze_voting.py
Outputs: derived/voting_rates.csv, derived/voting_arms.csv, derived/naturalization.csv,
         derived/gate_2020_turnout.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CACHE, DERIVED, FOREIGN, adults, assign_groups, load,  # noqa: E402
                    rate_table, wrate, write_csv)

YEARS = [2016, 2018, 2020, 2022, 2024]
W = "PWSSWGT"
CITIZEN = (1, 2, 3, 4)   # PRCITSHP values that are US citizens


def load_years() -> pd.DataFrame:
    frames = []
    for y in YEARS:
        p = CACHE / f"cps_voting_{y}.json"
        if not p.exists():
            print(f"[skip] {p.name} absent")
            continue
        d = adults(assign_groups(load(p)), W)
        d["year"] = y
        frames.append(d)
        print(f"[load] {y}: {len(d):,} adult records")
    if not frames:
        raise SystemExit("[DEGRADED] no voting files present")
    return pd.concat(frames, ignore_index=True)


def outcomes(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["voted"] = d.PES1.eq(1)
    d["regist"] = d.PES2.eq(1) | d.PES1.eq(1)     # voting implies registration in P20 tables
    d["vote_resp"] = d.PES1.isin([1, 2])
    d["reg_resp"] = d.PES2.isin([1, 2]) | d.PES1.eq(1)
    d["citizen"] = d.PRCITSHP.isin(CITIZEN)
    d["self_resp"] = d.HURESPLI.eq(d.PULINENO)
    return d


def extras(d: pd.DataFrame) -> dict:
    """Alternative definitions carried alongside the main groups.

    "8 Indian 2nd gen (self-ID)" is native-born with PRDASIAN==1 (Asian Indian), independent of
    parent birthplace; comparing it with the parent-birthplace group "5" shows whether the
    second-generation result is an artefact of how the generation is defined.
    "9 US-born Asian" is the wider native-born Asian comparison behind the P20 Table 11 puzzle
    that native-born Asian citizens report lower turnout than naturalized ones.
    """
    return {
        "8 Indian 2nd gen (self-ID)": d.is_usborn & d.PRDASIAN.eq(1),
        "9 US-born Asian (any)": d.is_usborn & d.PRDASIAN.ge(1),
    }


def block(d: pd.DataFrame, label: str, min_n: int = 50) -> pd.DataFrame:
    ex = extras(d)
    t = rate_table(d, d.voted, W, min_n=min_n, extra_rows=ex)
    t["measure"] = "turnout_census_convention"
    r = rate_table(d, d.regist, W, min_n=min_n, extra_rows=ex)
    r["measure"] = "registered_census_convention"
    sub = d[d.vote_resp]
    t2 = rate_table(sub, sub.voted, W, min_n=min_n, extra_rows=extras(sub))
    t2["measure"] = "turnout_reported_only"
    nr = rate_table(d, ~d.vote_resp, W, min_n=min_n, extra_rows=ex)
    nr["measure"] = "vote_item_nonresponse"
    out = pd.concat([t, r, t2, nr], ignore_index=True)
    out["arm"] = label
    return out


def main() -> None:
    d = outcomes(load_years())
    DERIVED.mkdir(exist_ok=True)

    # ---- gate: 2020 turnout vs the published Census P20-585 tables ----
    # Primary: all citizens 18+ (Table 1). Secondary: the nativity splits of Table 11, which
    # are the cells this lane actually leans on. Tolerance 0.5 points on the primary.
    y20 = d[d.year == 2020]
    cases = [
        ("all citizens 18+", y20[y20.citizen], 66.8, 72.7, 231593,
         "P20-585 Table 1, both sexes 18+: 154,628 / 231,593 thousand"),
        ("native-born citizens", y20[y20.PRCITSHP.isin([1, 2, 3])], 67.4, 73.3, 210083,
         "P20-585 Table 11, Native-born citizen, all races"),
        ("naturalized citizens", y20[y20.PRCITSHP.eq(4)], 60.8, 66.4, 21509,
         "P20-585 Table 11, Naturalized citizen, all races"),
        ("native-born NH white", y20[y20.PRCITSHP.isin([1, 2, 3]) & y20.PEHSPNON.eq(2)
                                     & y20.PTDTRACE.eq(1)], 71.2, 76.6, 150195,
         "P20-585 Table 11, Native-born citizen, White non-Hispanic alone"),
    ]
    lines = ["GATE: November 2020 reported turnout vs the published P20-585 tables",
             "(Census convention: item non-response counted as not voting, kept in the "
             "denominator)", ""]
    ok, delta = True, float("nan")
    for name, sub, pub_v, pub_r, pub_pop, src in cases:
        r = wrate(sub, sub.voted, W)
        rr = wrate(sub, sub.regist, W)
        dv = r["rate"] * 100 - pub_v
        if name == "all citizens 18+":
            ok, delta = abs(dv) <= 0.5, dv
        lines += [
            f"  {name}",
            f"    turnout    lane {r['rate'] * 100:6.2f}%   published {pub_v:5.1f}%   "
            f"delta {dv:+.2f}"
            + ("   <- PRIMARY GATE, tolerance 0.5 -> " + ("PASS" if abs(dv) <= 0.5 else "FAIL")
               if name == "all citizens 18+" else ""),
            f"    registered lane {rr['rate'] * 100:6.2f}%   published {pub_r:5.1f}%   "
            f"delta {rr['rate'] * 100 - pub_r:+.2f}",
            f"    weighted   lane {r['wpop'] / 1e3:9,.0f}k  published {pub_pop:9,}k  "
            f"delta {r['wpop'] / 1e3 - pub_pop:+,.0f}k   (n={r['n']:,})",
            f"    [SOURCE: {src}]",
            "",
        ]
    txt = "\n".join(lines)
    (DERIVED / "gate_2020_turnout.txt").write_text(txt)
    print(txt)

    # ---- headline: citizens 18+, pooled and by year ----
    rows = []
    cit = d[d.citizen]
    b = block(cit, "citizens_18plus_pooled")
    b["year"] = "pooled"
    rows.append(b)
    for y in sorted(cit.year.unique()):
        b = block(cit[cit.year == y], "citizens_18plus")
        b["year"] = str(y)
        rows.append(b)
    tab = pd.concat(rows, ignore_index=True)
    tab = tab[["arm", "year", "measure", "group", "n", "wpop", "rate", "se", "neff"]]
    tab = tab.sort_values(["arm", "year", "measure", "group"], kind="stable").reset_index(drop=True)
    write_csv(tab, "voting_rates.csv")

    # ---- disconfirmation arms ----
    arms = []
    a = block(d, "all_adults_18plus_incl_noncitizens")          # denominator = all adults
    a["year"] = "pooled"; arms.append(a)
    ba = cit[cit.PEEDUCA >= 43]
    a = block(ba, "citizens_BA_plus_only"); a["year"] = "pooled"; arms.append(a)
    nat = d[d.PRCITSHP.eq(4)]
    a = block(nat, "naturalized_citizens_only"); a["year"] = "pooled"; arms.append(a)
    sr = cit[cit.self_resp]
    a = block(sr, "citizens_self_respondent_only"); a["year"] = "pooled"; arms.append(a)
    yg = cit[(cit.PRTAGE >= 25) & (cit.PRTAGE <= 54)]
    a = block(yg, "citizens_age_25_54"); a["year"] = "pooled"; arms.append(a)
    at = pd.concat(arms, ignore_index=True)
    at = at[["arm", "year", "measure", "group", "n", "wpop", "rate", "se", "neff"]]
    at = at.sort_values(["arm", "year", "measure", "group"], kind="stable").reset_index(drop=True)
    write_csv(at, "voting_arms.csv")

    # ---- naturalization share among the foreign-born (all adults 18+) ----
    fb = d[d.PRCITSHP.isin(FOREIGN)]
    nrows = []
    for label, sub in [("pooled", fb)] + [(str(y), fb[fb.year == y]) for y in sorted(fb.year.unique())]:
        t = rate_table(sub, sub.PRCITSHP.eq(4), W)
        t = t[t.group.isin(["1 India-born", "2 China-born", "3 Mexico-born", "4 Other foreign-born"])]
        t["year"] = label
        nrows.append(t)
    for lo, hi in [(18, 34), (35, 49), (50, 64), (65, 99)]:
        sub = fb[(fb.PRTAGE >= lo) & (fb.PRTAGE <= hi)]
        t = rate_table(sub, sub.PRCITSHP.eq(4), W)
        t = t[t.group.isin(["1 India-born", "2 China-born", "3 Mexico-born", "4 Other foreign-born"])]
        t["year"] = f"pooled_age_{lo}_{hi}"
        nrows.append(t)
    nt = pd.concat(nrows, ignore_index=True)[["year", "group", "n", "wpop", "rate", "se", "neff"]]
    nt = nt.sort_values(["year", "group"], kind="stable").reset_index(drop=True)
    write_csv(nt, "naturalization.csv")

    print("[done] voting_rates.csv voting_arms.csv naturalization.csv gate_2020_turnout.txt")
    if not ok:
        print(f"[GATE-FAIL] delta {delta:+.2f} points", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
