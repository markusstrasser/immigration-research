#!/usr/bin/env python3
"""Arm D step 4: who staffs the kitchens.

Share of US cooks and chefs who are Mexico-born, US-born Mexican-origin, other
foreign-born, or US-born non-Hispanic white, from ACS 2024 1-year PUMS, with
replicate-weight SEs. Reported nationally and for the ten states with the most
cooks. PUMS carries PUMA, not CBSA, so the sub-national cut is by state.

OCCP 4000 = Chefs and head cooks (SOC 35-1011)
OCCP 4020 = Cooks (SOC 35-2011..35-2019)
Also reported: all food preparation and serving occupations (OCCP 4000-4160).

Input : _cache/pums_subset_2024.parquet
Output: derived/arm_d_cooks_shares.csv
"""
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
PARQ = LANE / "_cache" / "pums_subset_2024.parquet"
DER = LANE / "derived"
DER.mkdir(exist_ok=True)

WCOLS = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]
GROUPS = {
    "MEXBORN": "POBP = '303'",
    "USMEX": "NATIVITY = '1' AND HISP = '02'",
    "USWHITE": "NATIVITY = '1' AND HISP = '01' AND RAC1P = '1'",
    "FBOTHER": "NATIVITY = '2' AND POBP <> '303'",
    "OTHER_USBORN": ("NATIVITY = '1' AND NOT (HISP = '02') AND "
                     "NOT (HISP = '01' AND RAC1P = '1')"),
}
OCC_SETS = {
    "chefs_head_cooks": ["4000"],
    "cooks": ["4020"],
    "chefs_and_cooks": ["4000", "4020"],
    "all_food_prep_serving": ["4000", "4010", "4020", "4030", "4040", "4055",
                              "4110", "4120", "4130", "4140", "4150", "4160"],
}
EMPLOYED = "ESR IN ('1','2','4','5')"

STATE_NAMES = None


def se_from_reps(theta: np.ndarray) -> float:
    return float(np.sqrt(4.0 / 80.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def main() -> None:
    con = duckdb.connect()
    con.execute("PRAGMA threads=6")
    grp_case = "CASE " + " ".join(
        f"WHEN {c} THEN '{g}'" for g, c in GROUPS.items()) + " ELSE 'UNCLASS' END"
    rows = []
    for oname, codes in OCC_SETS.items():
        occ_in = ", ".join(f"'{c}'" for c in codes)
        sums = ", ".join(f"SUM({w}) AS w{i}" for i, w in enumerate(WCOLS))
        q = (f"SELECT {grp_case} AS grp, COUNT(*) AS n_unw, {sums} "
             f"FROM read_parquet('{PARQ}') WHERE AGEP >= 16 AND {EMPLOYED} "
             f"AND OCCP IN ({occ_in}) GROUP BY 1")
        df = con.execute(q).df()
        wcols = [f"w{i}" for i in range(81)]
        tot = df[wcols].sum(axis=0).to_numpy()
        for _, r in df.iterrows():
            share = r[wcols].to_numpy(dtype=float) / tot
            rows.append({
                "occupation": oname,
                "occp_codes": "+".join(codes),
                "group": r["grp"],
                "state": "US",
                "n_unweighted": int(r["n_unw"]),
                "weighted_workers": float(r["w0"]),
                "share": float(share[0]),
                "share_se": se_from_reps(share),
                "total_weighted_workers": float(tot[0]),
            })

    # top states by cook count, chefs_and_cooks only
    occ_in = ", ".join(f"'{c}'" for c in OCC_SETS["chefs_and_cooks"])
    sums = ", ".join(f"SUM({w}) AS w{i}" for i, w in enumerate(WCOLS))
    st = con.execute(
        f"SELECT STATE, {grp_case} AS grp, COUNT(*) AS n_unw, {sums} "
        f"FROM read_parquet('{PARQ}') WHERE AGEP >= 16 AND {EMPLOYED} "
        f"AND OCCP IN ({occ_in}) GROUP BY 1, 2").df()
    wcols = [f"w{i}" for i in range(81)]
    tot_by_state = st.groupby("STATE")[wcols].sum()
    top = tot_by_state["w0"].sort_values(ascending=False).head(10).index
    for state in top:
        tot = tot_by_state.loc[state].to_numpy(dtype=float)
        sub = st[st.STATE == state]
        for _, r in sub.iterrows():
            share = r[wcols].to_numpy(dtype=float) / tot
            rows.append({
                "occupation": "chefs_and_cooks",
                "occp_codes": "4000+4020",
                "group": r["grp"],
                "state": str(state),
                "n_unweighted": int(r["n_unw"]),
                "weighted_workers": float(r["w0"]),
                "share": float(share[0]),
                "share_se": se_from_reps(share),
                "total_weighted_workers": float(tot[0]),
            })

    out = pd.DataFrame(rows).sort_values(["occupation", "state", "group"])
    out.to_csv(DER / "arm_d_cooks_shares.csv", index=False)
    nat = out[(out.state == "US") & (out.occupation == "chefs_and_cooks")]
    print(nat[["group", "n_unweighted", "weighted_workers", "share",
               "share_se"]].to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
