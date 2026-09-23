"""Does the FY2022 financial-administration (E23) break move the two older lanes that read it?

This lane found local E23 doubling in the July 2026 re-release of the 2022 unit file (RESULT.md).
Two earlier lanes read the same Census series:
- administration_response_2026_09_20: state-by-level E23+E29+E31, 2012-2023. Check 1 tabulates
  national E23 by year from its own inputs, to date the break.
- local_spending_composition_2026_09_18: county budget shares of direct general expenditure,
  2012/2017/2022. Check 2 reruns its share arms with its own estimator on shares that exclude
  administration (functions 23/29/31) from the denominator in every year, which removes the break.
  Check 3 asks whether the unweighted arm's move comes from the break or from small counties.

Reads the other lanes' derived files; writes only derived/e23_other_lanes.csv here.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ADMIN = FISCAL / "administration_response_2026_09_20" / "derived"
LSC = FISCAL / "local_spending_composition_2026_09_18"
OUT = HERE / "derived" / "e23_other_lanes.csv"
STATES = {55: "WI", 36: "NY", 6: "CA", 34: "NJ", 17: "IL", 15: "HI"}
COUNTIES = {"36061": "New York County (NYC)", "42101": "Philadelphia", "17031": "Cook",
            "12086": "Miami-Dade"}


def load_lsc():
    spec = importlib.util.spec_from_file_location("lsc_estimate", LSC / "estimate_composition.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    rows = []

    print("[1] national E23 current operations, $bn (administration_response inputs)", flush=True)
    s = pd.read_csv(ADMIN / "selected_finance.csv")
    nat = s[(s.state == 0) & (s.code == "E23")].pivot_table(index="year", columns="level",
                                                            values="amount_thousands") / 1e6
    for year, r in nat.iterrows():
        print(f"  {year}  state+local {r[1]:6.1f}  state {r[2]:5.1f}  local {r[3]:5.1f}", flush=True)
        for level, name in ((1, "state_local"), (2, "state"), (3, "local")):
            rows.append({"check": "national_E23_bn", "spec": str(year), "outcome": name,
                         "published": round(r[level], 3)})
    p = pd.read_csv(ADMIN / "panel.csv")
    w = p[p.level == 1].pivot_table(index="state", columns="year", values="E23")
    for st, ab in STATES.items():
        r22, r23 = w.loc[st, 2022] / w.loc[st, 2021], w.loc[st, 2023] / w.loc[st, 2022]
        print(f"  {ab}: 2022/2021 {r22:.2f}, 2023/2022 {r23:.2f}", flush=True)
        rows.append({"check": "state_E23_ratio", "spec": ab, "outcome": "2022_over_2021",
                     "published": round(r22, 3)})
        rows.append({"check": "state_E23_ratio", "spec": ab, "outcome": "2023_over_2022",
                     "published": round(r23, 3)})

    lsc = load_lsc()
    orig_load = lsc.load_csv

    def load_ex_admin(path):
        out = orig_load(path)
        if not str(path).endswith("county_finance.csv"):
            return out
        fixed = []
        for r in out:
            r = dict(r)
            tot, adm = lsc.fnum(r.get("total_direct")), lsc.fnum(r.get("admin"))
            if tot is not None:
                r["total_direct"] = str(tot - (adm or 0.0))
            fixed.append(r)
        return fixed

    print("\n[2] administration share of county direct spending in the break counties", flush=True)
    for r in orig_load(str(LSC / "derived" / "county_finance.csv")):
        if r["fips"] in COUNTIES and r["year"] in ("2012", "2017", "2022"):
            share = 100 * (lsc.fnum(r["admin"]) or 0.0) / lsc.fnum(r["total_direct"])
            print(f"  {COUNTIES[r['fips']]:22s} {r['year']}  {share:5.2f}%", flush=True)
            rows.append({"check": "county_admin_share_pct", "spec": f"{r['fips']} {r['year']}",
                         "outcome": "admin", "published": round(share, 3)})

    base = lsc.build_panel()
    lsc.load_csv = load_ex_admin
    alt = lsc.build_panel()
    lsc.load_csv = orig_load
    keys = sorted(base)
    arms = [("A_share_wtd", {}, 2012, 2022), ("C_share_cov", {"covariates": True}, 2012, 2022),
            ("F_share_droptop25", {"drop_top": 25}, 2012, 2022),
            ("I_share_2017_2022", {}, 2017, 2022), ("A_weighted_2012_2017", {}, 2012, 2017),
            ("B_share_unwtd", {"weighted": False}, 2012, 2022),
            ("B_unwtd_2012_2017", {"weighted": False}, 2012, 2017),
            ("B_unwtd_2017_2022", {"weighted": False}, 2017, 2022),
            ("B_unwtd_trim", {"weighted": False, "trim": True}, 2012, 2022),
            ("B_unwtd_no_FL_NY_IL_PA", {"weighted": False, "drop_states": ("12", "36", "17", "42")},
             2012, 2022)]
    print("\n[3] share arms on the Hispanic share, per 10 points: published vs ex-administration",
          flush=True)
    for label, kw, y0, y1 in arms:
        for o in ("education", "police", "judicial", "law_order"):
            b = lsc.run_arm(base, keys, "sh_", o, "hisp", y0, y1, **kw)
            a = lsc.run_arm(alt, keys, "sh_", o, "hisp", y0, y1, **kw)
            print(f"  {label:24s} {o:10s} {b['coef10']:7.3f} ({b['se10']:.3f})  "
                  f"{a['coef10']:7.3f} ({a['se10']:.3f})  n={b['n']}", flush=True)
            rows.append({"check": "lsc_share_arm", "spec": label, "outcome": o,
                         "published": round(b["coef10"], 4), "published_se": round(b["se10"], 4),
                         "ex_admin": round(a["coef10"], 4), "ex_admin_se": round(a["se10"], 4),
                         "n": b["n"]})

    cols = ["check", "spec", "outcome", "published", "published_se", "ex_admin", "ex_admin_se", "n"]
    with OUT.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    print(f"\n[done] {OUT.relative_to(FISCAL.parent.parent)} ({len(rows)} rows)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
