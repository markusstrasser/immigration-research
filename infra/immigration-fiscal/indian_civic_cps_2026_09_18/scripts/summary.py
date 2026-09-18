"""Compact digest of everything in derived/, for reading the numbers into the memo.

Run: uv run --no-project --with "pandas>=2" python3 scripts/summary.py
Writes derived/summary.txt and prints it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DERIVED  # noqa: E402

pd.set_option("display.width", 200)
pd.set_option("display.max_rows", 400)
OUT: list[str] = []


def say(*a: object) -> None:
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


def pct(t: pd.DataFrame, cols=("group", "n", "rate", "se")) -> str:
    t = t.copy()
    if "rate" in t:
        t["rate"] = (t["rate"] * 100).round(1)
        t["se"] = (t["se"] * 100).round(2)
    return t[list(cols)].to_string(index=False)


def main() -> None:
    g = DERIVED / "gate_2020_turnout.txt"
    if g.exists():
        say("=" * 78); say(g.read_text())

    f = DERIVED / "voting_rates.csv"
    if f.exists():
        v = pd.read_csv(f)
        say("=" * 78); say("TURNOUT, citizens 18+, pooled 2016-2024")
        for m in ["turnout_census_convention", "turnout_reported_only",
                  "registered_census_convention", "vote_item_nonresponse"]:
            s = v[(v.year == "pooled") & (v.measure == m)]
            if len(s):
                say(f"\n-- {m}"); say(pct(s))
        say("\n-- turnout_census_convention by year (rate %, n)")
        s = v[(v.measure == "turnout_census_convention") & (v.year != "pooled")]
        p = s.pivot_table(index="group", columns="year", values="rate") * 100
        say(p.round(1).to_string())
        p = s.pivot_table(index="group", columns="year", values="n")
        say("\n   unweighted n"); say(p.astype("Int64").to_string())

    f = DERIVED / "voting_arms.csv"
    if f.exists():
        a = pd.read_csv(f)
        say("=" * 78); say("TURNOUT ARMS (turnout_census_convention unless noted)")
        for arm in sorted(a.arm.unique()):
            s = a[(a.arm == arm) & (a.measure == "turnout_census_convention")]
            if len(s):
                say(f"\n-- {arm}"); say(pct(s))

    f = DERIVED / "naturalization.csv"
    if f.exists():
        n = pd.read_csv(f)
        say("=" * 78); say("NATURALIZED SHARE OF THE FOREIGN-BORN 18+ (Nov supplements)")
        p = n.pivot_table(index="group", columns="year", values="rate") * 100
        say(p.round(1).to_string())

    f = DERIVED / "asec_naturalization_by_entry.csv"
    if f.exists():
        n = pd.read_csv(f)
        say("=" * 78); say("NATURALIZED SHARE BY YEARS SINCE ENTRY (CPS ASEC)")
        for y in sorted(n.asec_year.unique()):
            s = n[n.asec_year == y]
            p = s.pivot_table(index="group", columns="years_since_entry",
                              values="naturalized_rate") * 100
            order = [c for c in ["0_4", "5_9", "10_19", "20_29", "30_99"] if c in p.columns]
            say(f"\n-- ASEC {y}"); say(p[order].round(1).to_string())

    g = DERIVED / "gate_civic_rates.txt"
    if g.exists():
        say("=" * 78); say(g.read_text())

    f = DERIVED / "volunteer_rates.csv"
    if f.exists():
        c = pd.read_csv(f)
        say("=" * 78); say("VOLUNTEERING / GIVING / CIVIC CONTACT, adults 18+, pooled 2019-2023")
        for m in sorted(c.measure.unique()):
            s = c[(c.year == "pooled") & (c.measure == m)]
            if len(s):
                say(f"\n-- {m}"); say(pct(s))

    f = DERIVED / "volunteer_arms.csv"
    if f.exists():
        a = pd.read_csv(f)
        say("=" * 78); say("CIVIC ARMS")
        for m in ["volunteered_org", "donated_nonpolitical"]:
            for arm in sorted(a.arm.unique()):
                s = a[(a.arm == arm) & (a.measure == m)]
                if len(s):
                    say(f"\n-- {m} / {arm}"); say(pct(s))

    f = DERIVED / "volunteer_hours.csv"
    if f.exists():
        say("=" * 78); say("VOLUNTEER HOURS")
        say(pd.read_csv(f).round(1).to_string(index=False))

    for f, title in [(DERIVED / "regression_turnout.csv", "REGRESSION: TURNOUT"),
                     (DERIVED / "regression_civic.csv", "REGRESSION: CIVIC")]:
        if f.exists():
            r = pd.read_csv(f)
            say("=" * 78); say(title + "  (LPM coefficient in points vs US-born NH white)")
            r["coef_pts"] = (r.coef_lpm * 100).round(2)
            r["se_pts"] = (r.se_lpm * 100).round(2)
            r["ame_pts"] = (r.ame_logit * 100).round(2)
            for oc in sorted(r.outcome.unique()):
                for sp in sorted(r[r.outcome == oc].spec.unique()):
                    s = r[(r.outcome == oc) & (r.spec == sp)]
                    p = s.pivot_table(index="group", columns="model", values="coef_pts")
                    ps = s.pivot_table(index="group", columns="model", values="se_pts")
                    say(f"\n-- {oc} / {sp}  (n={int(s.n.max()):,})")
                    say(p.join(ps, lsuffix="_coef", rsuffix="_se").to_string())

    (DERIVED / "summary.txt").write_text("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
