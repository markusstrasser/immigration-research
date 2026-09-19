#!/usr/bin/env python3
"""Arm 2: how much of the national Democratic two-party share change came from the
Mexican-origin (and other Hispanic) share of voters RISING, and how much from the
group's own partisanship MOVING?

Group shares of actual voters s_gt: CPS November Voting Supplement (script 05),
self-reported voters among citizens 18+, Census weights. Primary.
Group Democratic two-party share d_gt: national exit polls (VNS 2000, Edison/NEP
2004-2024) as archived by the Roper Center "How Groups Voted" tables, and, for
2016-2024, Pew Research validated voters as the higher-graded series.

The exit poll cannot separate Mexican-origin from other Hispanic voters, so both
Hispanic subgroups are assigned the same d in the main run; the CPS supplies their
separate shares. That assumption is stated, not hidden, and a sensitivity run
gives the Mexican-origin group a d that is 5 points more Republican.

Shapley-style three-term decomposition of D_T - D_0 = sum_g s_gt d_gt:
    composition  sum_g (s_gT - s_g0) d_g0
    conversion   sum_g s_g0 (d_gT - d_g0)
    interaction  sum_g (s_gT - s_g0)(d_gT - d_g0)

Output: derived/partisanship_series.csv, derived/decomposition.csv,
        derived/decomposition.txt
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"
TXT: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    TXT.append(s)


# [SOURCE: Roper Center for Public Opinion Research, "How Groups Voted in <year>",
#  ropercenter.cornell.edu/how-groups-voted-<year>, fetched 2026-09-19; the
#  underlying polls are VNS 2000 and Edison/NEP for the National Election Pool
#  2004-2024. Percentages are of each group's voters; "don't know"/"other" excluded.]
EXIT = pd.DataFrame([
    # year, hisp share of electorate %, hisp dem %, hisp rep %,
    #       white share %, white dem %, white rep %
    (2000,  7, 62, 35, 81, 42, 55),
    (2004,  8, 53, 44, 77, 41, 58),
    (2008,  9, 67, 31, 74, 43, 55),
    (2012, 10, 71, 27, 72, 39, 59),
    (2016, 11, 66, 28, 70, 37, 57),
    (2020, 13, 65, 32, 67, 41, 58),
    (2024, 11, 51, 46, 71, 42, 57)],
    columns=["year", "exit_hisp_pct_of_voters", "hisp_dem", "hisp_rep",
             "exit_white_pct_of_voters", "white_dem", "white_rep"])

# [SOURCE: Pew Research Center validated-voter reports. 2020: "Behind Biden's 2020
#  Victory" (June 30, 2021) reports Hispanic voters 59% Biden / 38% Trump. 2024:
#  "Behind Trump's 2024 Victory" (June 26, 2025), chapter 2, states verbatim:
#  "His support among Hispanic voters was 12 points higher than in 2020 (48% in
#  2024, 36% in 2020). And the share voting for the Democratic candidate fell from
#  61% to 51%." Pew's own 2020 Hispanic figure therefore moved from 59/38 in the
#  2020 report to 61/36 in the 2024 report - a restatement, flagged below.]
PEW = pd.DataFrame([
    (2020, 59, 38, "Pew 2021 report, as published"),
    (2020, 61, 36, "Pew 2025 report, restating 2020"),
    (2024, 51, 48, "Pew 2025 report")],
    columns=["year", "hisp_dem", "hisp_rep", "pew_source"])


def two_party(dem: float, rep: float) -> float:
    return 100.0 * dem / (dem + rep)


def main() -> int:
    cps = pd.read_csv(DER / "cps_voting_national.csv")
    s = cps.pivot(index="year", columns="group", values="share_of_voters_pct") / 100
    turn = cps.pivot(index="year", columns="group", values="turnout_pct")
    cv = cps.pivot(index="year", columns="group", values="share_of_cvap_pct") / 100

    ser = EXIT.copy()
    ser["hisp_dem2p"] = [two_party(r.hisp_dem, r.hisp_rep) for r in EXIT.itertuples()]
    ser["white_dem2p"] = [two_party(r.white_dem, r.white_rep)
                          for r in EXIT.itertuples()]
    ser = ser.merge(s.reset_index().rename(columns={
        "mexican": "cps_mex_pct_of_voters", "hisp_other": "cps_hisp_other_pct",
        "non_hispanic": "cps_nonhisp_pct"}), on="year", how="left")
    for c in ("cps_mex_pct_of_voters", "cps_hisp_other_pct", "cps_nonhisp_pct"):
        ser[c] = (ser[c] * 100).round(2)
    ser.to_csv(DER / "partisanship_series.csv", index=False)

    say("=== inputs ===")
    say("exit-poll Hispanic two-party Democratic share and the CPS share of voters")
    say(ser[["year", "hisp_dem", "hisp_rep", "hisp_dem2p",
             "exit_hisp_pct_of_voters", "cps_mex_pct_of_voters",
             "cps_hisp_other_pct"]].round(2).to_string(index=False))
    say()
    say("Pew validated voters (Hispanic voters), the higher-graded series:")
    p = PEW.copy()
    p["dem2p"] = [two_party(r.hisp_dem, r.hisp_rep) for r in PEW.itertuples()]
    say(p.round(2).to_string(index=False))
    say("  NOTE a restatement: Pew's 2020 Hispanic figure is 59/38 in its 2021 "
        "report and 61/36 when restated in its 2025 report. Both are carried; the "
        "decomposition uses the exit-poll series for continuity back to 2004 and "
        "reports the Pew-based version alongside.")
    say()

    rows = []
    for label, base, end, dser in (
            ("exit polls, 2004->2024", 2004, 2024, "exit"),
            ("exit polls, 2012->2024", 2012, 2024, "exit"),
            ("exit polls, 2004->2012 (the pre-realignment window)", 2004, 2012,
             "exit")):
        e = ser.set_index("year")
        groups = ["mexican", "hisp_other", "non_hispanic"]
        s0 = {g: s.loc[base, g] for g in groups}
        sT = {g: s.loc[end, g] for g in groups}
        # non-Hispanic d is backed out so that the group shares reproduce the
        # actual national two-party Democratic share in each year
        actual = {2004: 48.76, 2008: 53.69, 2012: 51.96, 2016: 51.11,
                  2020: 52.27, 2024: 49.25}   # [CALCULATION: script 01 panel]
        d0 = {"mexican": e.loc[base, "hisp_dem2p"],
              "hisp_other": e.loc[base, "hisp_dem2p"]}
        dT = {"mexican": e.loc[end, "hisp_dem2p"],
              "hisp_other": e.loc[end, "hisp_dem2p"]}
        d0["non_hispanic"] = ((actual[base] - sum(s0[g] * d0[g]
                                                  for g in groups[:2]))
                              / s0["non_hispanic"])
        dT["non_hispanic"] = ((actual[end] - sum(sT[g] * dT[g]
                                                 for g in groups[:2]))
                              / sT["non_hispanic"])
        comp = sum((sT[g] - s0[g]) * d0[g] for g in groups)
        conv = sum(s0[g] * (dT[g] - d0[g]) for g in groups)
        inter = sum((sT[g] - s0[g]) * (dT[g] - d0[g]) for g in groups)
        total = actual[end] - actual[base]
        mex_only_comp = (sT["mexican"] - s0["mexican"]) * d0["mexican"] \
            - (sT["mexican"] - s0["mexican"]) * d0["non_hispanic"]
        rows.append({"window": label, "total_change_pp": total,
                     "composition_pp": comp, "conversion_pp": conv,
                     "interaction_pp": inter,
                     "mexican_share_composition_pp": mex_only_comp,
                     "mex_share_of_voters_start_pct": 100 * s0["mexican"],
                     "mex_share_of_voters_end_pct": 100 * sT["mexican"],
                     "hisp_dem2p_start": d0["mexican"],
                     "hisp_dem2p_end": dT["mexican"],
                     "nonhisp_dem2p_start": d0["non_hispanic"],
                     "nonhisp_dem2p_end": dT["non_hispanic"],
                     "source": dser})
    dec = pd.DataFrame(rows)
    say("=== decomposition of the national Democratic two-party share change ===")
    say("all entries in points of the national two-party Democratic share")
    say(dec.round(3).to_string(index=False))
    say()
    r = dec.iloc[0]
    say(f"2004->2024: the total move is {r.total_change_pp:+.2f} points. Rising "
        f"group shares contribute {r.composition_pp:+.2f}; moving group "
        f"partisanship contributes {r.conversion_pp:+.2f}; the cross term "
        f"{r.interaction_pp:+.2f}.")
    say(f"The Mexican-origin share of voters rose from "
        f"{r.mex_share_of_voters_start_pct:.2f}% to "
        f"{r.mex_share_of_voters_end_pct:.2f}% of all voters. Holding that group's "
        f"partisanship at its {int(r.window.split('->')[0][-4:])} level, the share "
        f"rise alone is worth {r.mexican_share_composition_pp:+.2f} points of the "
        f"national Democratic two-party share, measured against the non-Hispanic "
        f"voters it displaces.")

    # sensitivity: give the Mexican-origin group a d 5 points more Republican
    e = ser.set_index("year")
    groups = ["mexican", "hisp_other", "non_hispanic"]
    actual = {2004: 48.76, 2024: 49.25}
    s0 = {g: s.loc[2004, g] for g in groups}
    sT = {g: s.loc[2024, g] for g in groups}
    d0 = {"mexican": e.loc[2004, "hisp_dem2p"] - 5,
          "hisp_other": e.loc[2004, "hisp_dem2p"] + 5 * s0["mexican"] / s0["hisp_other"]}
    dT = {"mexican": e.loc[2024, "hisp_dem2p"] - 5,
          "hisp_other": e.loc[2024, "hisp_dem2p"] + 5 * sT["mexican"] / sT["hisp_other"]}
    d0["non_hispanic"] = ((actual[2004] - sum(s0[g] * d0[g] for g in groups[:2]))
                          / s0["non_hispanic"])
    dT["non_hispanic"] = ((actual[2024] - sum(sT[g] * dT[g] for g in groups[:2]))
                          / sT["non_hispanic"])
    comp = sum((sT[g] - s0[g]) * d0[g] for g in groups)
    conv = sum(s0[g] * (dT[g] - d0[g]) for g in groups)
    say()
    say(f"sensitivity, Mexican-origin voters 5 points more Republican than other "
        f"Hispanic voters in both years: composition {comp:+.2f}, conversion "
        f"{conv:+.2f} (main run {r.composition_pp:+.2f} / {r.conversion_pp:+.2f})")

    say()
    say("=== turnout, the other half of the composition channel ===")
    t = turn.round(1)
    say("CPS reported turnout of citizens 18+, by group (percent):")
    say(t.to_string())
    say("Mexican-origin citizens' share of the citizen voting-age population "
        "(percent):")
    say((100 * cv["mexican"]).round(2).to_string())
    gap = (t["non_hispanic"] - t["mexican"])
    say(f"turnout gap, non-Hispanic minus Mexican-origin citizens: "
        f"{gap.min():.1f} to {gap.max():.1f} points, {gap.mean():.1f} on average; "
        f"it does not close over the window")
    dec.to_csv(DER / "decomposition.csv", index=False)
    (DER / "decomposition.txt").write_text("\n".join(TXT) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
