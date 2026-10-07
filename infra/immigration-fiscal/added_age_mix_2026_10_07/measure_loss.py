#!/usr/bin/env python3
"""Identity loss by age, survey period and birth cohort, IPUMS-CPS basic monthly 1994-2026 (MIS 1 and 5).

Main case v5 prices the 3.04M added descendants (main_case_lineage_2026_10_05) at the identified third-plus's age
mix. This script measures how the loss rate varies with age and birth cohort, every age the CPS can see, so the
hidden people's age mix can be derived (age_mix.py).

Frame: g3_identity_pooled_2026_10_05's extract 5 (`_cache/monthly_mis15.csv.gz`, read in place, never copied) and its
classify() rules, ported to DuckDB SQL so that every age is kept with little memory:
  G3anc  native, both own parents US-born, civilian, every linked parent US-born, HISPAN known, and a Mexico-born
         grandparent read from a linked parent's MBPL/FBPL (analyze.py classify(), links MOMLOC/POPLOC/MOMLOC2/POPLOC2)
  G4anc  the same screen with no Mexico-born grandparent seen and a linked parent who reports Mexican origin and whose
         own parents are US-born: a child of an identified third-plus parent (Duncan-Trejo's fourth-plus cell)
Loss = the person's HISPAN is not a Mexican code. For children the household respondent reports it; adults are seen
only while they live with a parent. Weights WTFINL, person-records (no dedupe: a period's share is a weighted mean of
monthly cross-sections). SEs: linearised ratio variance with CPSID households as clusters, within survey year.

Gates (exit 1, nothing written):
  - classify(), imported from analyze.py and run on the same rows, gives the SQL's G3anc and identifier flags person
    for person in 1994, 2010 and 2025 (and the SQL never finds a link to a missing person, which classify() refuses);
  - the adult share not Mexican reproduces the pooled lane's monthly_1994_2026_nodedup cores_one 18+ value
    (derived/monthly_contrasts.csv, 1e-9).
Outputs: derived/loss_cells.csv (group x survey year x single age: weighted base and losses, records, clusters)
         derived/loss_tables.csv (period x age band, cohort x stage, with SEs), derived/gates_measure.json
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/measure_loss.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv
import importlib.util
import json
import resource
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
POOLED = FISCAL / "g3_identity_pooled_2026_10_05"
MONTHLY = POOLED / "_cache/monthly_mis15.csv.gz"
CONTRASTS = POOLED / "derived/monthly_contrasts.csv"
TMP = HERE / "_cache/duckdb_tmp"
DUCK_MEMORY = "512MB"
CONTROL_YEARS = (1994, 2010, 2025)
PERIODS = {"1994_2006": (1994, 2006), "2007_2021": (2007, 2021), "2022_2026": (2022, 2026), "1994_2026": (1994, 2026),
           "2007_2026": (2007, 2026)}
AGE_BANDS = [(0, 5), (6, 11), (12, 17), (18, 24), (25, 34), (35, 120)]
COHORTS = [(y, y + 4) for y in range(1960, 2030, 5)]
# The rates age_mix.py prices: CPS five-year bands, adults pooled where the co-resident sample thins out.
PRICING_BANDS = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 34), (35, 49), (50, 120)]
PRICING_PERIODS = ("2007_2026", "2022_2026", "1994_2026")
SURVEY_REF = 2025        # the account's ASEC year: a person aged a in 2025 was born in 2025 - a
FIVE_YEAR = [(a, a + 4) for a in range(0, 80, 5)] + [(80, 120)]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load("pooled_analyze", POOLED / "analyze.py")
MEX = ", ".join(str(c) for c in an.MEX_HISPAN)
UNK = ", ".join(str(c) for c in an.UNKNOWN_HISPAN)
US = an.US_MAX
MX = an.MEXICO
COLS = ["YEAR", "MONTH", "SERIAL", "PERNUM", "CPSID", "WTFINL", "AGE", "HISPAN", "BPL", "MBPL", "FBPL", "NATIVITY",
        "EMPSTAT", "MOMLOC", "POPLOC", "MOMLOC2", "POPLOC2", "MOMRULE", "POPRULE", "RACE"]
BIG = {"CPSID"}

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def connect() -> duckdb.DuckDBPyConnection:
    TMP.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit = '{DUCK_MEMORY}'")
    con.execute("SET threads = 2")
    con.execute(f"SET temp_directory = '{TMP}'")
    types = {c: "BIGINT" if c in BIG else "DOUBLE" if c == "WTFINL" else "INTEGER" for c in COLS}
    src = f"read_csv('{MONTHLY}', header = true, types = {types!r})"
    # Households that can hold a G3anc or G4anc person: someone with a Mexico-born parent (the G3anc's parent), or
    # someone of Mexican origin (the G4anc's parent). classify() is household-local, so the filter is exact.
    con.execute(f"""CREATE TEMP TABLE hh AS SELECT YEAR, MONTH, SERIAL FROM {src}
                    GROUP BY YEAR, MONTH, SERIAL
                    HAVING bool_or(MBPL = {MX} OR FBPL = {MX} OR HISPAN IN ({MEX}))""")
    con.execute(f"""CREATE TEMP TABLE p AS SELECT {', '.join('s.' + c for c in COLS)} FROM {src} s
                    JOIN hh USING (YEAR, MONTH, SERIAL)""")
    con.execute("DROP TABLE hh")
    return con


CLASSIFY_SQL = f"""
WITH links AS (
  SELECT c.YEAR, c.MONTH, c.SERIAL, c.PERNUM, l.loc
  FROM p c, LATERAL (VALUES (c.MOMLOC), (c.POPLOC), (c.MOMLOC2), (c.POPLOC2)) AS l(loc)
  WHERE l.loc > 0
), lp AS (
  SELECT k.YEAR, k.MONTH, k.SERIAL, k.PERNUM, q.PERNUM AS qn, q.BPL AS qb, q.MBPL AS qm, q.FBPL AS qf, q.HISPAN AS qh
  FROM links k LEFT JOIN p q ON q.YEAR = k.YEAR AND q.MONTH = k.MONTH AND q.SERIAL = k.SERIAL AND q.PERNUM = k.loc
), agg AS (
  SELECT YEAR, MONTH, SERIAL, PERNUM,
         count(*) FILTER (WHERE qn IS NULL) AS missing,
         count(*) FILTER (WHERE qn IS NOT NULL) AS nlink,
         bool_and(qn IS NULL OR qb < {US}) AS consistent,
         bool_or(qn IS NOT NULL AND qb < {US} AND (qm = {MX} OR qf = {MX})) AS mex_gp,
         bool_or(qn IS NOT NULL AND qb < {US} AND qh IN ({MEX}) AND qm < {US} AND qf < {US}) AS g3plus_mex_parent
  FROM lp GROUP BY ALL
)
SELECT c.YEAR, c.MONTH, c.SERIAL, c.PERNUM, c.CPSID, c.WTFINL AS w, c.AGE AS age,
       a.missing, a.nlink,
       (c.NATIVITY BETWEEN 1 AND 4) AND (c.MBPL < {US} AND c.FBPL < {US}) AND c.EMPSTAT <> 1 AND a.consistent
         AND c.HISPAN NOT IN ({UNK}) AS screen,
       a.mex_gp, a.g3plus_mex_parent, c.HISPAN IN ({MEX}) AS mex, c.HISPAN NOT IN ({UNK}) AND c.HISPAN > 0 AS hisp
FROM p c JOIN agg a USING (YEAR, MONTH, SERIAL, PERNUM)
ORDER BY c.YEAR, c.MONTH, c.SERIAL, c.PERNUM
"""


def control(con: duckdb.DuckDBPyConnection, flags: pd.DataFrame) -> None:
    """classify() on the same households, person for person."""
    cols = ["YEAR", "MONTH", "SERIAL", "PERNUM", "AGE", "HISPAN", "BPL", "MBPL", "FBPL", "NATIVITY", "EMPSTAT", "RACE",
            "MOMLOC", "POPLOC", "MOMLOC2", "POPLOC2", "MOMRULE", "POPRULE"]
    for y in CONTROL_YEARS:
        d = con.execute(f"SELECT {', '.join(cols)} FROM p WHERE YEAR = {y} ORDER BY MONTH, SERIAL, PERNUM").df()
        g = an.classify(d, False, d.YEAR.to_numpy(np.int64) * 100 + d.MONTH.to_numpy(np.int64))
        mine = flags[flags.YEAR == y].set_index(["MONTH", "SERIAL", "PERNUM"])
        key = pd.MultiIndex.from_frame(d[["MONTH", "SERIAL", "PERNUM"]])
        g3 = mine.reindex(key).g3.fillna(False).to_numpy(bool)
        idm = mine.reindex(key).g3id.fillna(False).to_numpy(bool)
        diff = int((g3 != g["G3anc"]).sum() + (idm != g["G3anc_id"]).sum())
        gate(f"{y}: the SQL's G3anc and identifier flags are classify()'s, person for person", diff == 0,
             f"{int(g['G3anc'].sum()):,} G3anc of {len(d):,} rows; {diff} differ")


def ratio_se(df: pd.DataFrame) -> tuple[float, float, float, int, int]:
    """Weighted loss share, its linearised SE (CPSID clusters within survey year), base, records and clusters."""
    W = df.w.sum()
    if W <= 0:
        return float("nan"), float("nan"), 0.0, 0, 0
    r = float((df.w * df.loss).sum() / W)
    z = df.assign(u=df.w * (df.loss - r)).groupby(["YEAR", "cl"]).u.sum()
    k = z.groupby(level=0).size()
    zc = z - z.groupby(level=0).transform("mean")
    v = float(((zc ** 2).groupby(level=0).sum() * k / (k - 1).clip(lower=1)).sum())
    return r, float(np.sqrt(v) / W), float(W), len(df), len(z)


def main() -> None:
    con = connect()
    print("[classify the frame in SQL]", flush=True)
    f = con.execute(CLASSIFY_SQL).df()
    gate("no parent pointer leads to a missing person (classify() would stop)", int(f.missing.sum()) == 0,
         f"{int(f.missing.sum())} missing")
    f["g3"] = f.screen & f.mex_gp
    f["g3id"] = f.g3 & f.mex
    f["g4"] = f.screen & ~f.mex_gp & f.g3plus_mex_parent
    control(con, f.rename(columns={}))
    con.close()
    f = f[f.g3 | f.g4].copy()
    f["group"] = np.where(f.g3, "G3anc", "G4anc")
    f["loss"] = (~f.mex).astype(float)
    f["loss_hisp"] = (~f.hisp).astype(float)
    # Cluster: the CPSID household (a household's MIS 1 and MIS 5 months share it); rows without one stand alone.
    f["cl"] = np.where(f.CPSID > 0, f.CPSID, -(f.YEAR * 10**8 + f.MONTH * 10**6 + f.SERIAL))
    f["cohort"] = f.YEAR - f.age
    del f["screen"]

    want = pd.read_csv(CONTRASTS)
    want = want[(want.label == "monthly_1994_2026_nodedup") & (want.links == "all") & (want.frame == "cores_one")
                & (want.measure == "employed") & (want.contrast == "G3anc: share not Mexican")].value
    adult = f[(f.group == "G3anc") & (f.age >= 18)]
    got = float((adult.w * adult.loss).sum() / adult.w.sum())
    gate("adults 18+: the share not Mexican is the pooled lane's monthly_1994_2026_nodedup cores_one value (1e-9)",
         len(want) == 1 and abs(got - float(want.iloc[0])) < 1e-9, f"{got:.10f} vs {float(want.iloc[0]):.10f}")
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")

    OUT.mkdir(exist_ok=True)
    cells = (f.assign(wl=f.w * f.loss, wlh=f.w * f.loss_hisp)
             .groupby(["group", "YEAR", "age"]).agg(base=("w", "sum"), lost=("wl", "sum"), lost_hispanic=("wlh", "sum"),
                                                    records=("w", "size"), clusters=("cl", "nunique")).reset_index())
    cells.to_csv(OUT / "loss_cells.csv", index=False, lineterminator="\n", float_format="%.6f")

    rows = []

    def add(kind, group, label, lo, hi, sub, outcome="not_mexican"):
        r, se, base, n, ncl = ratio_se(sub if outcome == "not_mexican" else sub.assign(loss=sub.loss_hisp))
        rows.append({"table": kind, "group": group, "outcome": outcome, "label": label, "lo": lo, "hi": hi,
                     "rate": r, "se": se, "weighted_base": base, "records": n, "clusters": ncl})

    for grp in ("G3anc", "G4anc"):
        g = f[f.group == grp]
        for pk, (y0, y1) in PERIODS.items():
            gp = g[g.YEAR.between(y0, y1)]
            for a0, a1 in AGE_BANDS + [(0, 17), (18, 120)]:
                sub = gp[gp.age.between(a0, a1)]
                for outcome in ("not_mexican", "not_hispanic"):
                    add("period_age", grp, pk, a0, a1, sub, outcome)
        for c0, c1 in COHORTS:
            gc = g[g.cohort.between(c0, c1)]
            for stage, (a0, a1) in (("child_0_17", (0, 17)), ("adult_18_plus", (18, 120))):
                sub = gc[gc.age.between(a0, a1)]
                if len(sub):
                    add("cohort_stage", grp, stage, c0, c1, sub)
        # Pricing bands by period (the cross-section of current reports), and the cohort reading: today's five-year band
        # [a0, a1] takes the child-stage (0-17) rate of the cohorts born SURVEY_REF - a1 ... SURVEY_REF - a0.
        for pk in PRICING_PERIODS:
            y0, y1 = PERIODS[pk]
            gp = g[g.YEAR.between(y0, y1)]
            for a0, a1 in PRICING_BANDS:
                add("pricing_band", grp, pk, a0, a1, gp[gp.age.between(a0, a1)])
        child = g[g.age <= 17]
        for a0, a1 in FIVE_YEAR:
            add("cohort_band", grp, "child_stage_rate_of_cohorts_born_2025_minus_band", a0, a1,
                child[child.cohort.between(SURVEY_REF - a1, SURVEY_REF - a0)])
    pd.DataFrame(rows).to_csv(OUT / "loss_tables.csv", index=False, lineterminator="\n", float_format="%.8f")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
    (OUT / "gates_measure.json").write_text(json.dumps({"gates": GATES, "records": int(len(f))}, indent=1) + "\n")
    print(f"  wrote {len(cells):,} cells, {len(rows)} table rows; {len(f):,} G3anc/G4anc records; peak RSS {peak:.2f} GiB",
          flush=True)


if __name__ == "__main__":
    main()
