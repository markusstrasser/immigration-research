"""Apportionment counterfactuals: remove a population from state counts and re-run Huntington-Hill.

Writes one CSV per arm to derived/, plus arms_summary.csv, ec_arithmetic.csv,
house_size_sensitivity.csv and last_seat_margins_2020.json.

The 2020 presidential election ran on the 2010 apportionment; the 2024 election ran on the
2020 apportionment. Electoral-vote arithmetic pairs each election with its own base accordingly.
"""
from pathlib import Path
import json
import pandas as pd

from hh import apportion, load_2010, load_2020, priority_table

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

# Certified statewide popular-vote winners. [SOURCE: certified 2020 and 2024 presidential results]
WINNER_2020 = {
    "Alabama": "R", "Alaska": "R", "Arizona": "D", "Arkansas": "R", "California": "D",
    "Colorado": "D", "Connecticut": "D", "Delaware": "D", "Florida": "R", "Georgia": "D",
    "Hawaii": "D", "Idaho": "R", "Illinois": "D", "Indiana": "R", "Iowa": "R", "Kansas": "R",
    "Kentucky": "R", "Louisiana": "R", "Maine": "D", "Maryland": "D", "Massachusetts": "D",
    "Michigan": "D", "Minnesota": "D", "Mississippi": "R", "Missouri": "R", "Montana": "R",
    "Nebraska": "R", "Nevada": "D", "New Hampshire": "D", "New Jersey": "D", "New Mexico": "D",
    "New York": "D", "North Carolina": "R", "North Dakota": "R", "Ohio": "R", "Oklahoma": "R",
    "Oregon": "D", "Pennsylvania": "D", "Rhode Island": "D", "South Carolina": "R",
    "South Dakota": "R", "Tennessee": "R", "Texas": "R", "Utah": "R", "Vermont": "D",
    "Virginia": "D", "Washington": "D", "West Virginia": "R", "Wisconsin": "D", "Wyoming": "R",
}
WINNER_2024 = dict(WINNER_2020)
for _s in ("Arizona", "Georgia", "Michigan", "Nevada", "Pennsylvania", "Wisconsin"):
    WINNER_2024[_s] = "R"
# Maine and Nebraska split by congressional district. Certified: 2020 ME 3 D / 1 R, NE 4 R / 1 D;
# 2024 ME 3 D / 1 R, NE 4 R / 1 D. A counterfactual seat delta in either state is credited to the
# statewide winner (the marginal district is unknowable); flagged in the memo.
SPLIT_BASE = {("Maine", "2020"): ("D", 3, 1), ("Nebraska", "2020"): ("R", 4, 1),
              ("Maine", "2024"): ("D", 3, 1), ("Nebraska", "2024"): ("R", 4, 1)}
SPLIT_STATES = {"Maine", "Nebraska"}


def run_arm(base: pd.DataFrame, removal: pd.Series, name: str, house: int = 435):
    pops = dict(zip(base["state"], base["pop"]))
    rem = {s: float(removal.get(s, 0.0)) for s in pops}
    cf = {s: max(int(round(pops[s] - rem[s])), 1) for s in pops}
    seats_base = apportion(pops, house)
    seats_cf = apportion(cf, house)
    df = pd.DataFrame([{
        "state": s, "pop_base": pops[s], "removed": round(rem[s]), "pop_cf": cf[s],
        "seats_base": seats_base[s], "seats_cf": seats_cf[s], "delta": seats_cf[s] - seats_base[s],
    } for s in pops]).sort_values("state").reset_index(drop=True)
    if house == 435:
        df.to_csv(DERIVED / f"arm_{name}.csv", index=False)
    movers = df[df.delta != 0]
    summary = {
        "arm": name, "house_size": house,
        "removed_total": int(round(sum(rem.values()))),
        "removed_pct_of_us": round(100 * sum(rem.values()) / sum(pops.values()), 3),
        "seats_moved": int(movers[movers.delta > 0].delta.sum()),
        "gainers": "; ".join(f"{r.state} {r.delta:+d}" for r in movers[movers.delta > 0].itertuples()),
        "losers": "; ".join(f"{r.state} {r.delta:+d}" for r in movers[movers.delta < 0].itertuples()),
    }
    return summary, df


def ec_arithmetic(df: pd.DataFrame, winners: dict, label: str):
    ev_base = {"D": 3, "R": 0}  # DC's 3 electoral votes, D in both elections, fixed
    ev_cf = {"D": 3, "R": 0}
    for r in df.itertuples():
        if r.state in SPLIT_STATES:
            continue
        w = winners[r.state]
        ev_base[w] += r.seats_base + 2
        ev_cf[w] += r.seats_cf + 2
    for st in SPLIT_STATES:
        sw, base_major, base_minor = SPLIT_BASE[(st, label)]
        other = "R" if sw == "D" else "D"
        row = df[df.state == st].iloc[0]
        d = int(row.seats_cf - row.seats_base)
        ev_base[sw] += base_major
        ev_base[other] += base_minor
        ev_cf[sw] += base_major + d
        ev_cf[other] += base_minor
    return {
        "election": label, "ev_D_base": ev_base["D"], "ev_R_base": ev_base["R"],
        "ev_D_cf": ev_cf["D"], "ev_R_cf": ev_cf["R"],
        "shift_to_R": ev_cf["R"] - ev_base["R"],
        "winner_base": "D" if ev_base["D"] > ev_base["R"] else "R",
        "winner_cf": "D" if ev_cf["D"] > ev_cf["R"] else "R",
        "outcome_flips": (ev_base["D"] > ev_base["R"]) != (ev_cf["D"] > ev_cf["R"]),
    }


def placebo_proportional(base: pd.DataFrame, total: float) -> pd.Series:
    """Same national total removed, allocated in proportion to state population. Any seat
    movement here is rounding, not geographic concentration. FALSIFICATION ARM."""
    pops = base.set_index("state")["pop"]
    return pops / pops.sum() * total


def redistributed(base: pd.DataFrame, removal: pd.Series) -> pd.Series:
    """'Same people, different geography': remove the group where it actually lives, then add the
    same national total back in proportion to the remaining population. Isolates concentration
    from level. FALSIFICATION ARM (a null here would mean the level, not the geography, matters)."""
    pops = base.set_index("state")["pop"].astype(float)
    rem = removal.reindex(pops.index).fillna(0.0)
    left = pops - rem
    return rem - left / left.sum() * rem.sum()


def last_seat_margins(pops: dict, house: int = 435, k: int = 6):
    pt = priority_table(pops, house + k)
    return [{"rank": r, "state": s, "seat_n": n, "priority": round(pv, 1)} for r, s, n, pv in pt[-(2 * k):]]


def build_arms():
    counts = pd.read_csv(DERIVED / "state_counts.csv", dtype={"state": str}).rename(columns={"NAME": "sname"}).set_index("sname")
    pew = pd.read_csv(DERIVED / "unauthorized_pew_by_state.csv")
    cms = pd.read_csv(DERIVED / "unauthorized_cms_by_state.csv")
    pw = lambda y: pew[pew.year == y].set_index("state_name")["unauth_pew"]
    cm = lambda y: cms[cms.year == y].set_index("state_name")["unauth_cms"]
    kids = None
    kp = DERIVED / "mexborn_plus_uskids.csv"
    if kp.exists():
        kids = pd.read_csv(kp).set_index("state_name")["mexborn_plus_kids"]
    arms_2020 = {
        "2020_mexico_born": counts["mex_born_acs2020"],
        "2020_mexican_origin": counts["mex_origin_2020_dec"],
        "2020_mexican_origin_acs": counts["mex_origin_acs2020"],
        "2020_unauth_pew2019": pw(2019),
        "2020_unauth_pew2021": pw(2021),
        "2020_unauth_cms2019": cm(2019),
        "2020_all_foreign_born": counts["fb_acs2020"],
    }
    if kids is not None:
        arms_2020["2020_mexborn_plus_uskids"] = kids
    arms_2010 = {
        "2010_mexico_born": counts["mex_born_acs2010"],
        "2010_mexican_origin": counts["mex_origin_2010_dec"],
        "2010_unauth_pew2010": pw(2010),
        "2010_unauth_cms2010": cm(2010),
        "2010_all_foreign_born": counts["fb_acs2010"],
    }
    return arms_2020, arms_2010


HEADLINE = {2020: "2020_mexican_origin", 2010: "2010_mexican_origin"}

if __name__ == "__main__":
    arms_2020, arms_2010 = build_arms()
    d20, d10 = load_2020(), load_2010()
    summaries, ec_rows, hs_rows = [], [], []
    for base, arms, yr in ((d20, arms_2020, 2020), (d10, arms_2010, 2010)):
        election = "2024" if yr == 2020 else "2020"
        winners = WINNER_2024 if yr == 2020 else WINNER_2020
        for name, rem in arms.items():
            s, df = run_arm(base, rem, name)
            summaries.append(s)
            print(f"{name}: removed {s['removed_total']:,} ({s['removed_pct_of_us']}%), "
                  f"seats moved {s['seats_moved']} | gain: {s['gainers'] or '-'} | lose: {s['losers'] or '-'}", flush=True)
            sp, _ = run_arm(base, placebo_proportional(base, s["removed_total"]), name + "_PLACEBOprop")
            summaries.append(sp)
            sr, _ = run_arm(base, redistributed(base, rem), name + "_REDISTRIBUTED")
            summaries.append(sr)
            print(f"    placebo(proportional): {sp['seats_moved']} moved | "
                  f"redistributed(same people, proportional geography): {sr['seats_moved']} moved "
                  f"| gain: {sr['gainers'] or '-'} | lose: {sr['losers'] or '-'}", flush=True)
            row = ec_arithmetic(df, winners, election)
            row["arm"] = name
            row["apportionment_base"] = yr
            ec_rows.append(row)
            if name == HEADLINE[yr] or "mexico_born" in name:
                for h in (435, 436, 437, 438, 440, 450, 500):
                    sh, _ = run_arm(base, rem, name, house=h)
                    hs_rows.append({"arm": name, "house_size": h, "seats_moved": sh["seats_moved"],
                                    "gainers": sh["gainers"], "losers": sh["losers"]})
    pd.DataFrame(summaries).to_csv(DERIVED / "arms_summary.csv", index=False)
    pd.DataFrame(ec_rows)[["arm", "apportionment_base", "election", "ev_D_base", "ev_R_base",
                           "ev_D_cf", "ev_R_cf", "shift_to_R", "winner_base", "winner_cf",
                           "outcome_flips"]].to_csv(DERIVED / "ec_arithmetic.csv", index=False)
    pd.DataFrame(hs_rows).to_csv(DERIVED / "house_size_sensitivity.csv", index=False)
    pops20 = dict(zip(d20["state"], d20["pop"]))
    (DERIVED / "last_seat_margins_2020.json").write_text(json.dumps(last_seat_margins(pops20), indent=1) + "\n")
    print("\nEC arithmetic (2020 election on the 2010 apportionment; 2024 on the 2020 apportionment):")
    print(pd.DataFrame(ec_rows)[["arm", "election", "ev_D_base", "ev_R_base", "ev_D_cf", "ev_R_cf",
                                 "shift_to_R", "outcome_flips"]].to_string(index=False))
