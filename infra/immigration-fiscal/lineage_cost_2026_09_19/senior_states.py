"""Where unauthorized Mexico-born people near and past 65 live, by state (ACS 2024).

The lineage model is national, so an unauthorized founder's public health cost after 65 depends
on the chance of living in a state that covers people regardless of status. This tabulates that
chance from the ACS 2024 residual imputation of `unauthorized_population_size_2026_09_19`,
imported unmodified, on two rule sets:

- `paper_rules`: the lane's rules as published (Medicaid at interview marks a person legal);
- `no_medicaid_rule`: the same with HINS4 set to "No", as `california_medical_status_2026_09_23`
  does, because status-blind state coverage (Medi-Cal for every age since 2024) is reported as
  Medicaid and would otherwise mark covered unauthorized people legal.

Ages 45–64 are the cohorts that reach 65 over the next two decades; 65+ is reported but the ACS
edits Medicare onto 65+ Medicaid reporters, so the residual finds almost no unauthorized seniors
in covering states (`california_medical_status_2026_09_23/RESULT.md` §3).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/lineage_cost_2026_09_19/senior_states.py
Writes derived/senior_state_shares.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "unauthorized_population_size_2026_09_19"
sys.path.insert(0, str(LANE))
import acs_residual as A  # noqa: E402

PARQUET = LANE / "_cache/acs2024_person_subset.parquet"
MEXICO = 303
# The imported lane's published totals (paper rules), reproduced before anything else.
GATE = {"national": 12_973_901, "mexico_born": 3_963_961}
AGE_GROUPS = {"45-64": (45, 64), "50-64": (50, 64), "55-64": (55, 64), "65+": (65, 200)}
# States named in the pricing; every other state is summed into "other".
STATES = {6: "California", 48: "Texas", 17: "Illinois", 4: "Arizona", 36: "New York",
          41: "Oregon", 53: "Washington", 11: "District of Columbia", 12: "Florida",
          13: "Georgia", 37: "North Carolina", 32: "Nevada", 8: "Colorado", 34: "New Jersey"}


def main() -> None:
    cols = ["SERIALNO", "SPORDER", "STATE", "PWGTP", "AGEP", "CIT", "YOEP", "NATIVITY", "POBP", "COW",
            "OCCP", "MIL", "HINS3", "HINS4", "HINS5", "SSP", "SSIP", "RELSHIPP"]
    d = pd.read_parquet(PARQUET, columns=cols)
    w = d.PWGTP.to_numpy(float)
    d_nm = d.copy()
    d_nm["HINS4"] = 2
    res = {"paper_rules": A.impute(d)["unauthorized"], "no_medicaid_rule": A.impute(d_nm)["unauthorized"]}
    mex = d.POBP.to_numpy() == MEXICO
    got = {"national": w[res["paper_rules"]].sum(), "mexico_born": w[res["paper_rules"] & mex].sum()}
    for k, v in GATE.items():
        if abs(got[k] - v) > 1.0:
            raise SystemExit(f"[BLOCKED] {k} {got[k]:,.0f} does not reproduce the lane's {v:,}")

    keep = mex & (res["paper_rules"] | res["no_medicaid_rule"])
    reps = pd.read_parquet(PARQUET, columns=A.REPS).to_numpy(np.float64)[keep]
    sub = d.loc[keep, ["STATE", "AGEP"]].reset_index(drop=True)
    ws = w[keep]
    state = sub.STATE.to_numpy().astype(int)
    age = sub.AGEP.to_numpy().astype(int)
    rows = []
    for rule, unauth in res.items():
        u = unauth[keep]
        for ag, (lo, hi) in AGE_GROUPS.items():
            base = u & (age >= lo) & (age <= hi)
            tot, tot_r = ws[base].sum(), reps[base].sum(axis=0)
            groups = [(str(f), name, base & (state == f)) for f, name in STATES.items()]
            groups.append(("other", "all other states", base & ~np.isin(state, list(STATES))))
            for fips, name, m in groups:
                num, num_r = ws[m].sum(), reps[m].sum(axis=0)
                share, share_r = num / tot, num_r / tot_r
                rows.append(dict(rule=rule, age_group=ag, state_fips=fips, state=name,
                                 persons=round(num), share=round(share, 6),
                                 se_share=round(float(np.sqrt(4 / 80 * ((share_r - share) ** 2).sum())), 6),
                                 n_unweighted=int(m.sum()), group_total=round(tot)))
    out = pd.DataFrame(rows)
    for (rule, ag), g in out.groupby(["rule", "age_group"]):
        if abs(g.share.sum() - 1) > 1e-5:
            raise SystemExit(f"[BLOCKED] shares for {rule}/{ag} sum to {g.share.sum():.6f}")
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived/senior_state_shares.csv", index=False, lineterminator="\n")
    show = out[out.state_fips.isin(["6", "48", "17", "36", "41", "53", "11"])]
    print(show.pivot_table(index=["state"], columns=["rule", "age_group"], values="share").round(3).to_string())
    print(out.groupby(["rule", "age_group"]).group_total.first().to_string())


if __name__ == "__main__":
    main()
