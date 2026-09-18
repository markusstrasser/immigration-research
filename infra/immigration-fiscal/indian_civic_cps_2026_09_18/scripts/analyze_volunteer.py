"""Volunteering, giving and civic contact by birthplace, CPS September Volunteering &
Civic Life Supplement (2019, 2021, 2023; weight PWNRWGT).

Note on the giving question: the pre-2017 Volunteer Supplement asked about donations of
$25 or more. The 2017 redesign replaced it with PES18 "Donate to non-political org."
with no dollar threshold, and PES17 for political organisations. There is no amount
bracket in the redesigned instrument, so amounts cannot be reported.

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 scripts/analyze_volunteer.py
Outputs: derived/volunteer_rates.csv, derived/volunteer_arms.csv, derived/volunteer_hours.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CACHE, DERIVED, GROUP_ORDER, adults, assign_groups, kish_neff,  # noqa: E402
                    load, rate_table, write_csv)

YEARS = [2019, 2021, 2023]
W = "PWNRWGT"

# outcome -> (variable, positive codes, response codes)
OUTCOMES = {
    "volunteered_org":        ("PES16", (1,), (1, 2)),
    "donated_nonpolitical":   ("PES18", (1,), (1, 2)),
    "donated_political":      ("PES17", (1,), (1, 2)),
    "contacted_official":     ("PES13", (1,), (1, 2)),
    "group_membership":       ("PES15", (1,), (1, 2)),
    "neighbor_favors_monthly": ("PES6", (1, 2, 3, 4), (1, 2, 3, 4, 5, 6)),
    "talks_neighbors_weekly":  ("PES4", (1, 2), (1, 2, 3, 4, 5, 6)),
    "improved_neighborhood":   ("PES7", (1,), (1, 2)),
}


def load_years() -> pd.DataFrame:
    frames = []
    for y in YEARS:
        p = CACHE / f"cps_volunteer_{y}.json"
        if not p.exists():
            print(f"[skip] {p.name} absent")
            continue
        d = adults(assign_groups(load(p)), W)
        d["year"] = y
        d["self_resp"] = d.PUSLFPRX.isin([1, 3])
        frames.append(d)
        print(f"[load] {y}: {len(d):,} adult records with a supplement weight")
    if not frames:
        raise SystemExit("[DEGRADED] no volunteer files present")
    return pd.concat(frames, ignore_index=True)


def block(d: pd.DataFrame, label: str, year: str, min_n: int = 50) -> pd.DataFrame:
    out = []
    for name, (var, pos, resp) in OUTCOMES.items():
        sub = d[d[var].isin(resp)]          # respondents only; "not in universe" dropped
        ex = {"8 Indian 2nd gen (self-ID)": sub.is_usborn & sub.PRDASIAN.eq(1),
              "9 US-born Asian (any)": sub.is_usborn & sub.PRDASIAN.ge(1)}
        t = rate_table(sub, sub[var].isin(pos), W, min_n=min_n, extra_rows=ex)
        t["measure"] = name
        out.append(t)
    t = pd.concat(out, ignore_index=True)
    t["arm"] = label
    t["year"] = year
    return t[["arm", "year", "measure", "group", "n", "wpop", "rate", "se", "neff"]]


def hours_table(d: pd.DataFrame) -> pd.DataFrame:
    """Annual volunteer hours: mean and median among volunteers, and mean over all adults."""
    rows = []
    v = d[d.PES16.eq(1) & d.PTS16E.ge(0)]
    allad = d[d.PES16.isin([1, 2])].copy()
    allad["hours0"] = allad.PTS16E.where(allad.PTS16E.ge(0), 0).astype(float)
    for g in GROUP_ORDER[:-1] + ["7 All US-born"]:
        sub = v[v.grp.eq(g)] if g != "7 All US-born" else v[v.is_usborn]
        sub_all = allad[allad.grp.eq(g)] if g != "7 All US-born" else allad[allad.is_usborn]
        w = sub[W].to_numpy(float)
        h = sub.PTS16E.to_numpy(float)
        if len(sub) >= 50 and w.sum() > 0:
            mean_v = float((w * h).sum() / w.sum())
            o = np.argsort(h, kind="stable")
            cw = np.cumsum(w[o])
            med_v = float(h[o][cw >= cw[-1] / 2][0])
        else:
            mean_v = med_v = float("nan")
        wa = sub_all[W].to_numpy(float)
        ha = sub_all.hours0.to_numpy(float)
        mean_all = float((wa * ha).sum() / wa.sum()) if len(sub_all) >= 50 and wa.sum() > 0 else float("nan")
        rows.append(dict(group=g, n_volunteers=int(len(sub)), n_adults=int(len(sub_all)),
                         mean_hours_volunteers=mean_v, median_hours_volunteers=med_v,
                         mean_hours_all_adults=mean_all))
    return pd.DataFrame(rows).sort_values("group", kind="stable").reset_index(drop=True)


# Published national rates, CPS Civic Engagement & Volunteering supplement, population 16+.
# [SOURCE: AmeriCorps Open Data "2017-2023 CEV Findings: National Rates of All Measures",
#  data.americorps.gov/d/rhng-qtzw, cached at _cache/americorps_cev_national.csv]
# This lane's universe is 18+, so a small gap is expected and is not a failure; the check is
# for a coding error large enough to move a between-group comparison.
PUBLISHED = {
    "volunteered_org":      {2019: 0.300, 2021: 0.232, 2023: 0.283},
    "group_membership":     {2019: 0.271, 2021: 0.238, 2023: 0.249},
    "donated_nonpolitical": {2019: 0.505, 2021: 0.481, 2023: 0.485},
    "contacted_official":   {2019: 0.099, 2021: 0.095, 2023: 0.087},
}


def gate(d: pd.DataFrame) -> str:
    lines = ["CHECK: lane all-adult (18+) rates vs the published AmeriCorps/Census national",
             "rates for the same supplement (published universe is 16+, this lane's is 18+,",
             "so a gap of a point or so is expected).", ""]
    for measure, by_year in sorted(PUBLISHED.items()):
        var, pos, resp = OUTCOMES[measure]
        for y in sorted(by_year):
            sub = d[(d.year == y) & d[var].isin(resp)]
            if not len(sub):
                continue
            w = sub[W].to_numpy(float)
            r = float((w * sub[var].isin(pos).to_numpy(float)).sum() / w.sum())
            lines.append(f"  {measure:22s} {y}  lane {r * 100:5.1f}%   published "
                         f"{by_year[y] * 100:5.1f}%   delta {(r - by_year[y]) * 100:+.1f}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    d = load_years()
    DERIVED.mkdir(exist_ok=True)
    txt = gate(d)
    (DERIVED / "gate_civic_rates.txt").write_text(txt)
    print(txt)

    rows = [block(d, "adults_18plus", "pooled")]
    for y in sorted(d.year.unique()):
        rows.append(block(d[d.year == y], "adults_18plus", str(y)))
    tab = pd.concat(rows, ignore_index=True)
    tab = tab.sort_values(["arm", "year", "measure", "group"], kind="stable").reset_index(drop=True)
    write_csv(tab, "volunteer_rates.csv")

    arms = [
        block(d[d.self_resp], "self_respondent_only", "pooled"),
        block(d[d.PEEDUCA >= 43], "BA_plus_only", "pooled"),
        block(d[d.PRCITSHP.isin([1, 2, 3, 4])], "citizens_only", "pooled"),
        block(d[(d.PRTAGE >= 25) & (d.PRTAGE <= 54)], "age_25_54", "pooled"),
        block(d[d.HEFAMINC >= 15], "family_income_100k_plus", "pooled"),
    ]
    at = pd.concat(arms, ignore_index=True)
    at = at.sort_values(["arm", "year", "measure", "group"], kind="stable").reset_index(drop=True)
    write_csv(at, "volunteer_arms.csv")

    write_csv(hours_table(d), "volunteer_hours.csv")
    print("[done] volunteer_rates.csv volunteer_arms.csv volunteer_hours.csv")


if __name__ == "__main__":
    main()
