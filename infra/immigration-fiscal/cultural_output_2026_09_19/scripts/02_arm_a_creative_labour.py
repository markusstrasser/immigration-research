#!/usr/bin/env python3
"""Arm A: creative labour supply and earnings, ACS 2024 1-year PUMS.

Groups (universe: age 25-64, household + GQ persons):
  MEXBORN  POBP=303 (born in Mexico)
  USMEX    NATIVITY=1 and HISP=02 (US-born, Mexican origin; 2nd+ generation,
           ACS cannot separate 2nd from 3rd+)
  USWHITE  NATIVITY=1, HISP=01, RAC1P=1 (US-born non-Hispanic white; NOT
           third-plus, ACS has no parental birthplace)
  FBOTHER  foreign born, not Mexico (context row)

Outcomes: employment in SOC 27 creative occupations (OCCP list below), by genre,
self-employment inside them, and person earnings (PERNP x ADJINC) inside them.

Rates are reported crude and direct-standardised to the USWHITE age x education
x sex distribution. Standard errors use the 80 ACS successive-difference
replicate weights: SE = sqrt(4/80 * sum_k (theta_k - theta_0)^2).

Input : _cache/pums_subset_2024.parquet
Output: derived/arm_a_creative_rates.csv, derived/arm_a_cells.csv,
        derived/arm_a_summary.json
"""
import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
PARQ = LANE / "_cache" / "pums_subset_2024.parquet"
DER = LANE / "derived"
DER.mkdir(exist_ok=True)

WCOLS = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]

GENRES = {
    # SOC 27 creative core, split into the four genre buckets of the brief
    "music_perf": ["2700", "2740", "2751", "2752", "2755", "2770"],
    "visual_design": ["2600", "2631", "2632", "2633", "2634", "2635", "2636",
                      "2640", "2910"],
    "writers_media": ["2805", "2810", "2825", "2830", "2840", "2850", "2861",
                      "2862", "2865"],
    "film_tv": ["2710", "2905", "2920"],
    # SOC 27-2020/27-2023 athletes, coaches, umpires: inside SOC 27 but not
    # creative output; reported separately, excluded from `creative`.
    "sports": ["2721", "2722", "2723"],
}
CREATIVE = sorted(sum([GENRES[k] for k in GENRES if k != "sports"], []))

GROUPS = {
    "MEXBORN": "POBP = '303'",
    "USMEX": "NATIVITY = '1' AND HISP = '02'",
    "USWHITE": "NATIVITY = '1' AND HISP = '01' AND RAC1P = '1'",
    "FBOTHER": "NATIVITY = '2' AND POBP <> '303'",
}

EMPLOYED = "ESR IN ('1','2','4','5')"
SELFEMP = "COW IN ('6','7')"


def inlist(col: str, vals) -> str:
    return col + " IN (" + ", ".join(f"'{v}'" for v in vals) + ")"


MEASURES = {
    "pop": "1",
    "emp": f"CASE WHEN {EMPLOYED} THEN 1 ELSE 0 END",
    "creative": f"CASE WHEN {EMPLOYED} AND {inlist('OCCP', CREATIVE)} THEN 1 ELSE 0 END",
    "creative_selfemp": (
        f"CASE WHEN {EMPLOYED} AND {inlist('OCCP', CREATIVE)} AND {SELFEMP} "
        "THEN 1 ELSE 0 END"
    ),
    # earnings are summed in whole cents as BIGINT: a float sum over many
    # rows depends on the order the parallel aggregate happens to combine
    # partials, which made this table differ in its last digit between runs
    "creative_earn": (
        f"CASE WHEN {EMPLOYED} AND {inlist('OCCP', CREATIVE)} "
        "THEN CAST(ROUND(COALESCE(PERNP,0) * ADJINC / 10000.0) AS BIGINT) "
        "ELSE 0 END"
    ),
    "emp_earn": (
        f"CASE WHEN {EMPLOYED} THEN "
        "CAST(ROUND(COALESCE(PERNP,0) * ADJINC / 10000.0) AS BIGINT) "
        "ELSE 0 END"
    ),
    "creative_ba": (
        f"CASE WHEN {EMPLOYED} AND {inlist('OCCP', CREATIVE)} AND "
        "CAST(SCHL AS INTEGER) >= 21 THEN 1 ELSE 0 END"
    ),
    "ba": "CASE WHEN CAST(SCHL AS INTEGER) >= 21 THEN 1 ELSE 0 END",
}
for gname, codes in GENRES.items():
    MEASURES[f"g_{gname}"] = (
        f"CASE WHEN {EMPLOYED} AND {inlist('OCCP', codes)} THEN 1 ELSE 0 END"
    )

CELL_SQL = """
CASE WHEN AGEP < 35 THEN '25-34' WHEN AGEP < 45 THEN '35-44'
     WHEN AGEP < 55 THEN '45-54' ELSE '55-64' END AS age_grp,
CASE WHEN CAST(SCHL AS INTEGER) <= 15 THEN '1_lths'
     WHEN CAST(SCHL AS INTEGER) <= 17 THEN '2_hs'
     WHEN CAST(SCHL AS INTEGER) <= 20 THEN '3_somecoll'
     WHEN CAST(SCHL AS INTEGER) = 21 THEN '4_ba'
     ELSE '5_grad' END AS educ,
SEX AS sex
"""


def build_cells(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    grp_case = "CASE " + " ".join(
        f"WHEN {cond} THEN '{g}'" for g, cond in GROUPS.items()
    ) + " ELSE NULL END AS grp"
    blocks = []
    for mname, expr in MEASURES.items():
        sums = ", ".join(
            f"SUM(({expr}) * {w}) AS w{i}" for i, w in enumerate(WCOLS)
        )
        blocks.append(
            f"SELECT '{mname}' AS measure, grp, age_grp, educ, sex, "
            f"COUNT(*) AS n_unw, {sums} FROM base WHERE grp IS NOT NULL "
            "GROUP BY grp, age_grp, educ, sex"
        )
    sql = (
        f"WITH base AS (SELECT {grp_case}, {CELL_SQL}, AGEP, SCHL, SEX, ESR, "
        f"OCCP, COW, PERNP, ADJINC, {', '.join(WCOLS)} "
        f"FROM read_parquet('{PARQ}') WHERE AGEP BETWEEN 25 AND 64 "
        "AND SCHL IS NOT NULL) "
        + " UNION ALL ".join(blocks)
    )
    return con.execute(sql).df()


def se_from_reps(theta: np.ndarray) -> float:
    """theta[0] point estimate, theta[1:] the 80 replicate estimates."""
    return float(np.sqrt(4.0 / 80.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def main() -> None:
    con = duckdb.connect()
    con.execute("PRAGMA threads=6")
    cells = build_cells(con)
    cells["cell"] = cells["age_grp"] + "|" + cells["educ"] + "|" + cells["sex"]
    wcols = [f"w{i}" for i in range(81)]

    # sample sizes for transparency (unweighted person records)
    nrows = (
        cells[cells.measure == "pop"].groupby("grp")["n_unw"].sum().to_dict()
    )
    grp_case2 = "CASE " + " ".join(
        f"WHEN {cond} THEN '{g}'" for g, cond in GROUPS.items()
    ) + " ELSE NULL END"
    ncreat_df = con.execute(
        f"SELECT {grp_case2} AS grp, COUNT(*) AS n FROM read_parquet('{PARQ}') "
        f"WHERE AGEP BETWEEN 25 AND 64 AND {EMPLOYED} AND "
        f"{inlist('OCCP', CREATIVE)} GROUP BY 1"
    ).df()
    ncreat = dict(zip(ncreat_df["grp"], ncreat_df["n"]))
    genre_n = {}
    for gname, codes in GENRES.items():
        df = con.execute(
            f"SELECT {grp_case2} AS grp, COUNT(*) AS n FROM read_parquet('{PARQ}') "
            f"WHERE AGEP BETWEEN 25 AND 64 AND {EMPLOYED} AND "
            f"{inlist('OCCP', codes)} GROUP BY 1"
        ).df()
        genre_n[gname] = {k: int(v) for k, v in zip(df["grp"], df["n"])
                          if isinstance(k, str)}

    # wide: (measure, grp, cell) -> 81 weighted sums
    wide = cells.pivot_table(
        index=["grp", "cell"], columns="measure", values=wcols, aggfunc="sum"
    ).fillna(0.0)

    all_cells = sorted(cells["cell"].unique())
    groups = list(GROUPS)

    def arr(measure: str) -> np.ndarray:
        """-> array [group, cell, 81]"""
        out = np.zeros((len(groups), len(all_cells), 81))
        for gi, g in enumerate(groups):
            for ci, c in enumerate(all_cells):
                if (g, c) in wide.index:
                    row = wide.loc[(g, c)]
                    out[gi, ci, :] = [row[(w, measure)] for w in wcols]
        return out

    M = {m: arr(m) for m in MEASURES}
    for m in ("creative_earn", "emp_earn"):      # cents -> dollars
        M[m] = M[m] / 100.0

    # the brief asks for both standardisations; MA collapses the sex dimension
    # so the same machinery produces age x education cells as well
    ae_cells = sorted({c.rsplit("|", 1)[0] for c in all_cells})
    AEMAP = np.zeros((len(all_cells), len(ae_cells)))
    for ci, c in enumerate(all_cells):
        AEMAP[ci, ae_cells.index(c.rsplit("|", 1)[0])] = 1.0
    M_AE = {m: np.einsum("gcr,ck->gkr", v, AEMAP) for m, v in M.items()}

    # white standard population shares, per replicate
    wi = groups.index("USWHITE")
    wpop = M["pop"][wi]                      # [cell, 81]
    std_share = wpop / wpop.sum(axis=0, keepdims=True)

    rows = []

    def n_num_for(num_m: str, g: str):
        if num_m == "creative":
            return ncreat.get(g)
        if num_m.startswith("g_"):
            return genre_n.get(num_m[2:], {}).get(g)
        return None

    def emit(name, num_m, den_m, standardise=True, per=1000.0,
             std_measure="pop", cells="age_educ_sex"):
        """std_measure names the white distribution used as the standard: for
        a rate defined only on BA+ holders the standard must be the white BA+
        distribution, not the whole white population."""
        src = M if cells == "age_educ_sex" else M_AE
        num = src[num_m]
        den = src[den_m]
        wstd = src[std_measure][wi]
        share = wstd / wstd.sum(axis=0, keepdims=True)
        for gi, g in enumerate(groups):
            crude = num[gi].sum(axis=0) / den[gi].sum(axis=0)
            rec = {
                "measure": name,
                "cells": cells,
                "numerator": num_m,
                "denominator": den_m,
                "group": g,
                "n_sample": nrows.get(g),
                "n_numerator_sample": n_num_for(num_m, g),
                "crude_per_1k": float(crude[0] * per),
                "crude_se": se_from_reps(crude) * per,
            }
            if standardise:
                with np.errstate(invalid="ignore", divide="ignore"):
                    cellrate = np.where(den[gi] > 0, num[gi] / den[gi], 0.0)
                std = (share * cellrate).sum(axis=0)
                rec["std_per_1k"] = float(std[0] * per)
                rec["std_se"] = se_from_reps(std) * per
                # ratio to white crude (= white std by construction)
                wcrude = num[wi].sum(axis=0) / den[wi].sum(axis=0)
                ratio = std / wcrude
                rec["ratio_std_to_white"] = float(ratio[0])
                rec["ratio_se"] = se_from_reps(ratio)
                rec["ratio_crude_to_white"] = float((crude / wcrude)[0])
                rec["ratio_crude_se"] = se_from_reps(crude / wcrude)
            rows.append(rec)

    def emit_reverse(name, num_m, den_m, per=1000.0):
        """Disconfirmation cut: standardise WHITE to each group's own age x
        educ x sex distribution instead of the other way round. If the gap is
        an artefact of the standardisation direction, this reverses it."""
        num, den = M[num_m], M[den_m]
        for gi, g in enumerate(groups):
            gpop = M["pop"][gi]
            gshare = gpop / gpop.sum(axis=0, keepdims=True)
            with np.errstate(invalid="ignore", divide="ignore"):
                wcell = np.where(den[wi] > 0, num[wi] / den[wi], 0.0)
            white_std_to_group = (gshare * wcell).sum(axis=0)
            crude = num[gi].sum(axis=0) / den[gi].sum(axis=0)
            ratio = crude / white_std_to_group
            rows.append({
                "measure": name, "cells": "age_educ_sex",
                "numerator": num_m, "denominator": den_m,
                "group": g, "n_sample": nrows.get(g),
                "n_numerator_sample": n_num_for(num_m, g),
                "crude_per_1k": float(crude[0] * per),
                "crude_se": se_from_reps(crude) * per,
                "std_per_1k": float(white_std_to_group[0] * per),
                "std_se": se_from_reps(white_std_to_group) * per,
                "ratio_std_to_white": float(ratio[0]),
                "ratio_se": se_from_reps(ratio),
            })

    # headline: creative employment per 1,000 population 25-64
    emit("creative_per_1k_pop", "creative", "pop")
    # the brief's second standardisation: age x education, sex collapsed
    emit("creative_per_1k_pop_ageeduc", "creative", "pop", cells="age_educ")
    # disconfirmation 1: the same comparison among BA+ holders only, where
    # education is matched by construction rather than by reweighting
    emit("creative_per_1k_ba_pop", "creative_ba", "ba", std_measure="ba")
    # disconfirmation 2: reverse standardisation direction
    emit_reverse("creative_per_1k_pop_REVSTD", "creative", "pop")
    # a rate conditional on employment is standardised onto the white EMPLOYED
    # distribution, so that the white reference row is 1.0 by construction
    emit("creative_per_1k_emp", "creative", "emp", std_measure="emp")
    for gname in GENRES:
        emit(f"{gname}_per_1k_pop", f"g_{gname}", "pop")
    emit("ba_per_1k_pop", "ba", "pop", standardise=False)
    emit("creative_selfemp_share", "creative_selfemp", "creative",
         standardise=False, per=1.0)
    emit("creative_earn_per_capita_usd", "creative_earn", "pop",
         standardise=True, per=1.0)
    emit("creative_mean_earn_usd", "creative_earn", "creative",
         standardise=False, per=1.0)
    emit("all_earn_per_capita_usd", "emp_earn", "pop", standardise=True, per=1.0)
    emit("creative_ba_share", "creative_ba", "creative", standardise=False,
         per=1.0)

    # age-cohort cut: is the gap narrower in younger cohorts? standardised on
    # the white educ x sex distribution WITHIN each age band
    age_rows = []
    for ag in sorted({c.split("|")[0] for c in all_cells}):
        idx = [i for i, c in enumerate(all_cells) if c.startswith(ag + "|")]
        wpop_a = M["pop"][wi][idx]
        share_a = wpop_a / wpop_a.sum(axis=0, keepdims=True)
        wnum = M["creative"][wi][idx].sum(axis=0)
        wden = M["pop"][wi][idx].sum(axis=0)
        wrate = wnum / wden
        for gi, g in enumerate(groups):
            num = M["creative"][gi][idx]
            den = M["pop"][gi][idx]
            crude = num.sum(axis=0) / den.sum(axis=0)
            with np.errstate(invalid="ignore", divide="ignore"):
                cellrate = np.where(den > 0, num / den, 0.0)
            std = (share_a * cellrate).sum(axis=0)
            ratio = std / wrate
            age_rows.append({
                "age_grp": ag, "group": g,
                "crude_per_1k": float(crude[0] * 1000),
                "crude_se": se_from_reps(crude) * 1000,
                "std_per_1k": float(std[0] * 1000),
                "std_se": se_from_reps(std) * 1000,
                "ratio_std_to_white": float(ratio[0]),
                "ratio_se": se_from_reps(ratio),
            })
    pd.DataFrame(age_rows).round(6).to_csv(
        DER / "arm_a_by_age_cohort.csv", index=False)

    out = pd.DataFrame(rows).round(6)
    out.to_csv(DER / "arm_a_creative_rates.csv", index=False)

    # cell table (point weights only) for inspection
    cellout = (
        cells[["measure", "grp", "age_grp", "educ", "sex", "n_unw", "w0"]]
        .rename(columns={"w0": "weighted"})
        .sort_values(["measure", "grp", "age_grp", "educ", "sex"])
    )
    money = cellout["measure"].isin(["creative_earn", "emp_earn"])
    cellout.loc[money, "weighted"] = cellout.loc[money, "weighted"] / 100.0
    cellout["weighted"] = cellout["weighted"].round(1)
    cellout.to_csv(DER / "arm_a_cells.csv", index=False)

    summary = {
        "source": "ACS 2024 1-year PUMS person file (psam_pusa/b), Census Bureau",
        "universe": "age 25-64, all persons",
        "occp_creative": CREATIVE,
        "occp_genres": GENRES,
        "groups": GROUPS,
        "sample_sizes": {g: int(nrows.get(g, 0)) for g in groups},
        "creative_worker_samples": {g: int(ncreat.get(g, 0)) for g in groups},
        "genre_worker_samples": {k: dict(sorted(v.items()))
                                 for k, v in sorted(genre_n.items())},
        "min_cell_unweighted_pop": {
            g: int(cells[(cells.measure == "pop") & (cells.grp == g)]["n_unw"].min())
            for g in groups
        },
        "n_cells": len(all_cells),
        "cells_with_zero_group_pop": {
            g: int(sum(
                1 for ci in range(len(all_cells)) if M["pop"][gi, ci, 0] == 0
            )) for gi, g in enumerate(groups)
        },
        "weighted_population": {
            g: float(M["pop"][gi].sum(axis=0)[0]) for gi, g in enumerate(groups)
        },
        "se_method": "80 successive-difference replicate weights, 4/80 factor",
    }
    (DER / "arm_a_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(out.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
