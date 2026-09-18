"""Monte-Carlo robustness of the seat counterfactuals to sampling / rounding error in the
removed-population estimates. FALSIFICATION ARM: if the headline seat shift is an artifact of
estimate noise, the simulated distribution will straddle a materially different value.

Draws each state's removal from Normal(estimate, MOE90/1.645), truncated at 0, and re-runs
Huntington-Hill. 4,000 draws per arm, fixed seed.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

from hh import apportion, load_2020

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
N_DRAWS = 4000
SEED = 20260918

WINNER_2024_R = {
    "Alabama", "Alaska", "Arkansas", "Florida", "Idaho", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Mississippi", "Missouri", "Montana", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "West Virginia",
    "Wyoming", "Arizona", "Georgia", "Michigan", "Nevada", "Pennsylvania", "Wisconsin",
}


def acs_moe():
    rows = json.loads((CACHE / "acs5_2020_moe_states.json").read_text())
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df[~df["state"].isin({"11", "72"})]
    for c in ("B05006_150E", "B05006_150M", "B05002_013E", "B05002_013M"):
        df[c] = pd.to_numeric(df[c])
    return df.set_index("NAME")


def simulate(base, est: pd.Series, moe90: pd.Series, label: str):
    rng = np.random.default_rng(SEED)
    states = list(base["state"])
    pops = np.array([base.set_index("state")["pop"][s] for s in states], dtype=float)
    e = np.array([est.get(s, 0.0) for s in states], dtype=float)
    m = np.array([moe90.get(s, 0.0) for s in states], dtype=float)
    sd = np.maximum(m / 1.645, 1.0)
    base_seats = apportion(dict(zip(states, pops.astype(int))))
    base_vec = np.array([base_seats[s] for s in states])
    moved, ca, tx, ev_shift = [], [], [], []
    ca_i, tx_i = states.index("California"), states.index("Texas")
    r_mask = np.array([s in WINNER_2024_R for s in states])
    for _ in range(N_DRAWS):
        draw = np.clip(rng.normal(e, sd), 0, None)
        cf = np.maximum(pops - draw, 1).astype(int)
        seats = apportion(dict(zip(states, cf)))
        v = np.array([seats[s] for s in states])
        d = v - base_vec
        moved.append(int(d[d > 0].sum()))
        ca.append(int(d[ca_i]))
        tx.append(int(d[tx_i]))
        # EV gained by 2024-Republican-carried states = net seat delta in those states
        # (ME/NE lumped by statewide winner: ME -> D, NE -> R)
        ev_shift.append(int(d[r_mask].sum()))
    out = pd.DataFrame({"seats_moved": moved, "california_delta": ca, "texas_delta": tx,
                        "ev_shift_to_R_2024": ev_shift})
    out.to_csv(DERIVED / f"mc_{label}.csv", index=False)
    q = lambda s: (int(np.percentile(s, 2.5)), int(np.median(s)), int(np.percentile(s, 97.5)))
    return {"arm": label, "draws": N_DRAWS,
            "seats_moved_p2.5_med_p97.5": q(moved),
            "california_delta": q(ca), "texas_delta": q(tx),
            "ev_shift_to_R_2024": q(ev_shift)}


if __name__ == "__main__":
    base = load_2020()
    moe = acs_moe()
    pew = pd.read_csv(DERIVED / "unauthorized_pew_by_state.csv")
    p19 = pew[pew.year == 2019].set_index("state_name")
    res = [
        simulate(base, moe["B05006_150E"], moe["B05006_150M"], "2020_mexico_born"),
        simulate(base, moe["B05002_013E"], moe["B05002_013M"], "2020_all_foreign_born"),
        simulate(base, p19["unauth_pew"], p19["moe90_pew"], "2020_unauth_pew2019"),
    ]
    df = pd.DataFrame(res)
    df.to_csv(DERIVED / "mc_summary.csv", index=False)
    print(df.to_string(index=False))
