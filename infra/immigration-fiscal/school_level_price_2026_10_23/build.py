#!/usr/bin/env python3
"""School-level price of the group's pupils, CCD membership x SLFS spending.

Question: the case prices each group pupil at its state's average spending per
pupil. The `school_cost_where_enrolled` lane found the group's districts spend
2.5% more than their state averages (k = 1.034, proposed). This lane goes one
level finer: the school the pupil attends.

Inputs (both already in the sibling lane's cache, FY2021-22):
  CCD SCH_052_2122 membership by race/ethnicity and school.
  SLFS FY2022 school-level current expenditures (TCURELSCS) and membership.

Outputs:
  derived/ccd_school_2122.csv   one row per school, total/Hispanic/white/black
  derived/slfs_school_2122.csv  one row per sampled school, spending and membership
  derived/school_merge.csv      the merged school-level table
  derived/state_k.csv           Hispanic- and white-weighted price vs state average
  derived/district_k.csv        within-district price gap, by district
  derived/summary.json          national and top-state readings

Limitation: CCD reports Hispanic, not Mexican origin. The Hispanic-weighted
price is a proxy for the group; in the high-Mexican-share states it is close,
elsewhere it is a broader Hispanic reading. SLFS is a sample, not the universe.
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
OUT.mkdir(parents=True, exist_ok=True)

CCD = CACHE / "ccd_SCH_052_2122_l_1a_071722.csv"
SLFS = CACHE / "slfs22_1a.txt"


def build_school_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        f"""
        COPY (
          SELECT NCESSCH, LEAID, ST AS STABR, SCH_NAME,
            SUM(CASE WHEN RACE_ETHNICITY='No Category Codes' AND SEX='No Category Codes'
                      AND TOTAL_INDICATOR='Education Unit Total'
                     THEN TRY_CAST(STUDENT_COUNT AS BIGINT) ELSE 0 END) AS total,
            SUM(CASE WHEN RACE_ETHNICITY='Hispanic/Latino'
                     THEN TRY_CAST(STUDENT_COUNT AS BIGINT) ELSE 0 END) AS hispanic,
            SUM(CASE WHEN RACE_ETHNICITY='White'
                     THEN TRY_CAST(STUDENT_COUNT AS BIGINT) ELSE 0 END) AS white,
            SUM(CASE WHEN RACE_ETHNICITY='Black or African American'
                     THEN TRY_CAST(STUDENT_COUNT AS BIGINT) ELSE 0 END) AS black
          FROM read_csv_auto('{CCD}', header=true, all_varchar=true)
          WHERE GRADE='No Category Codes'
          GROUP BY 1,2,3,4
        ) TO '{CACHE / "ccd_school_2122.csv"}' (HEADER, DELIMITER ',')
        """
    )
    con.execute(
        f"""
        COPY (
          SELECT NCESSCH, FIPST, LEAID, LEA_NAME, STABBR, LEVEL, MEMBER, TCURELSCS
          FROM read_csv('{SLFS}', delim='\t', header=true, all_varchar=true, encoding='latin-1', ignore_errors=true)
          WHERE TRY_CAST(MEMBER AS BIGINT) > 0 AND TRY_CAST(TCURELSCS AS DOUBLE) > 0
        ) TO '{CACHE / "slfs_school_2122.csv"}' (HEADER, DELIMITER ',')
        """
    )
    con.execute(
        f"""
        COPY (
          SELECT c.NCESSCH, c.LEAID, c.STABR, c.SCH_NAME, c.total, c.hispanic, c.white, c.black,
                 s.LEA_NAME, s.LEVEL, CAST(s.MEMBER AS BIGINT) AS member,
                 CAST(s.TCURELSCS AS DOUBLE) AS tcur,
                 CAST(s.TCURELSCS AS DOUBLE) / CAST(s.MEMBER AS BIGINT) AS pp
          FROM read_csv('{CACHE / "ccd_school_2122.csv"}') c
          JOIN read_csv('{CACHE / "slfs_school_2122.csv"}') s USING (NCESSCH)
          WHERE c.total > 0
        ) TO '{CACHE / "school_merge.csv"}' (HEADER, DELIMITER ',')
        """
    )


def weighted_price(df: pd.DataFrame, weight: str) -> float:
    w = df[weight].clip(lower=0)
    denom = w.sum()
    return float((w * df["pp"]).sum() / denom) if denom else float("nan")


def main() -> None:
    con = duckdb.connect()
    build_school_tables(con)
    df = pd.read_csv(CACHE / "school_merge.csv", dtype={"NCESSCH": str, "LEAID": str})
    df["pp"] = pd.to_numeric(df["pp"], errors="coerce")
    df = df.loc[df["pp"].gt(0) & df["member"].gt(0)].copy()

    rows = []
    for state, g in df.groupby("STABR"):
        state_pp = float(g["tcur"].sum() / g["member"].sum())
        rows.append(
            {
                "state": state,
                "schools": int(len(g)),
                "members": int(g["member"].sum()),
                "hispanic": int(g["hispanic"].sum()),
                "hispanic_share": float(g["hispanic"].sum() / g["member"].sum()),
                "state_pp": state_pp,
                "hispanic_pp": weighted_price(g, "hispanic"),
                "white_pp": weighted_price(g, "white"),
                "k_hispanic": weighted_price(g, "hispanic") / state_pp,
                "k_white": weighted_price(g, "white") / state_pp,
                "k_relative": weighted_price(g, "hispanic") / weighted_price(g, "white"),
            }
        )
    state_k = pd.DataFrame(rows).sort_values("k_hispanic", ascending=False)
    state_k.to_csv(OUT / "state_k.csv", index=False)

    dist = []
    for leaid, g in df.groupby("LEAID"):
        if len(g) < 5 or g["hispanic"].sum() < 100 or g["member"].sum() < 500:
            continue
        district_pp = float(g["tcur"].sum() / g["member"].sum())
        dist.append(
            {
                "leaid": leaid,
                "state": g["STABR"].iloc[0],
                "lea_name": g["LEA_NAME"].iloc[0],
                "schools": int(len(g)),
                "members": int(g["member"].sum()),
                "hispanic": int(g["hispanic"].sum()),
                "hispanic_share": float(g["hispanic"].sum() / g["member"].sum()),
                "district_pp": district_pp,
                "hispanic_pp": weighted_price(g, "hispanic"),
                "k_within": weighted_price(g, "hispanic") / district_pp,
            }
        )
    district_k = pd.DataFrame(dist).sort_values("k_within", ascending=False)
    district_k.to_csv(OUT / "district_k.csv", index=False)

    national_pp = float(df["tcur"].sum() / df["member"].sum())

    # Group-weighted chain: P1 state, P2 district, P3 school.
    state_avg = (
        df.groupby("STABR")
        .apply(lambda g: pd.Series({"pp": g["tcur"].sum() / g["member"].sum(), "w": g["hispanic"].sum()}), include_groups=False)
    )
    dist_avg = (
        df.groupby("LEAID")
        .apply(lambda g: pd.Series({"pp": g["tcur"].sum() / g["member"].sum(), "w": g["hispanic"].sum(), "n": len(g)}), include_groups=False)
    )
    P1 = float((state_avg["pp"] * state_avg["w"]).sum() / state_avg["w"].sum())
    P2 = float((dist_avg["pp"] * dist_avg["w"]).sum() / dist_avg["w"].sum())
    P3 = float((df["pp"] * df["hispanic"]).sum() / df["hispanic"].sum())
    multi = dist_avg.loc[(dist_avg["n"] > 1) & (~dist_avg.index.astype(str).str.startswith("36"))]
    P2x = float((multi["pp"] * multi["w"]).sum() / multi["w"].sum())
    chain = {
        "P0_national": national_pp,
        "P1_state": P1,
        "P2_district": P2,
        "P3_school": P3,
        "between_states": P1 / national_pp,
        "between_districts": P2 / P1,
        "within_districts": P3 / P2,
        "within_districts_ex_single_and_nyc": P3 / P2x,
        "single_school_districts": int((dist_avg["n"] == 1).sum()),
        "districts": int(len(dist_avg)),
    }

    hispanic_weight = state_k["hispanic"].clip(lower=0)
    white_weight = state_k["members"] - state_k["hispanic"]
    summary = {
        "schools": int(len(df)),
        "members": int(df["member"].sum()),
        "hispanic": int(df["hispanic"].sum()),
        "national_pp": national_pp,
        "national_hispanic_pp": weighted_price(df, "hispanic"),
        "national_white_pp": weighted_price(df, "white"),
        "national_k_hispanic": weighted_price(df, "hispanic") / national_pp,
        "national_k_white": weighted_price(df, "white") / national_pp,
        "national_k_relative": weighted_price(df, "hispanic") / weighted_price(df, "white"),
        "state_k_median": float(state_k["k_hispanic"].median()),
        "state_k_iqr": [float(state_k["k_hispanic"].quantile(q)) for q in (0.25, 0.75)],
        "district_k_median": float(district_k["k_within"].median()),
        "district_k_iqr": [float(district_k["k_within"].quantile(q)) for q in (0.25, 0.75)],
        "chain": chain,
        "hispanic_weighted_state_k": float((hispanic_weight * state_k["k_hispanic"]).sum() / hispanic_weight.sum()),
        "white_weighted_state_k": float(
            ((white_weight.clip(lower=0) * state_k["k_white"]).sum() / white_weight.clip(lower=0).sum())
        ),
        "checks": {
            "schools_with_hispanic_gt_total": int((df["hispanic"] > df["total"]).sum()),
            "schools_with_white_gt_total": int((df["white"] > df["total"]).sum()),
            "schools_with_negative_pp": int((df["pp"] <= 0).sum()),
            "hispanic_share_of_members": float(df["hispanic"].sum() / df["member"].sum()),
        },
        "top_states": state_k.head(8)[["state", "k_hispanic", "k_white", "hispanic"]].to_dict("records"),
        "top_districts": district_k.head(8)[["leaid", "state", "k_within", "hispanic"]].to_dict("records"),
        "note": "Hispanic proxy for Mexican origin; SLFS FY2022 sample; current expenditures only",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"schools {len(df):,}  members {df.member.sum():,}  Hispanic {df.hispanic.sum():,}")
    print(f"national pp ${national_pp:,.0f}  Hispanic ${summary['national_hispanic_pp']:,.0f}  "
          f"white ${summary['national_white_pp']:,.0f}")
    print(f"national k: Hispanic {summary['national_k_hispanic']:.4f}  white {summary['national_k_white']:.4f}")
    print(f"state k median {summary['state_k_median']:.4f}  IQR {summary['state_k_iqr']}")
    print(f"Hispanic-weighted state k {summary['hispanic_weighted_state_k']:.4f}  "
          f"white-weighted {summary['white_weighted_state_k']:.4f}")
    print(f"district k median {summary['district_k_median']:.4f}  IQR {summary['district_k_iqr']}")
    print(f"checks {summary['checks']}")
    print(state_k.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
