"""Is the Mexican-origin G2 -> G3+ stall a vintage effect? IPUMS-CPS basic monthly and ASEC, 1994-2026.

Ladder 232 finds G2 -> G3+ carries 0.84-0.86 of the gap to third-plus non-Hispanic whites, and lists arrival
vintage as not excluded: today's G3+ descend partly from early, Texas-heavy migration. Two designs split the
carry-over by vintage where the CPS lets one see it.

1. Cross-section (the ladder's convention). rho = gap(G3+ identifiers) / gap(G2), adults 25-64, each gap
   against third-plus non-Hispanic whites reweighted to the group's age x sex cells (the carry-over lane's
   `pop` cells) in the same stratum. Strata: birth cohort (survey year minus age), state group (Texas and New
   Mexico, California, elsewhere) and both. Also a lagged ratio: G3+ of cohort c against G2 of cohort c-30, the
   G2 that could be their parents.
2. Lineage. Adults 25+ living with a linked parent: the parent's own record gives the parent's schooling and
   birth year. rho_lin = gap(children) / gap(their parents), each against white pairs (third-plus white child,
   third-plus white parent) of the same parent-birth-cohort band and state group, children matched on the
   co-resident frames' age x sex cells, parents on 5-year age bands x sex. The parent's birth cohort is the
   vintage proxy: a G2 parent born before 1950 is the child of a pre-1950 arrival. Steps:
   - g1g2: Mexico-born parent -> US-born child with a Mexico-born parent (G2);
   - g2g3: US-born parent with a Mexico-born parent (G2) -> child with both parents US-born (the pooled lane's
     G3 lineage, G3anc; gate: equal to analyze.py's classify() on every year);
   - g3g4: G3+ parent who reports Mexican origin, with both of the child's parents linked and all four
     grandparents US-born -> child (G4+ by NLSY97's definition).
   Children are counted whatever origin they report (the lineage); identifiers alone are the published
   convention. Schooling only (BA+, less than high school, years): parents are 40-85, and their employment
   and earnings mix in retirement.

Definitions, codes and weights are the pooled lane's (analyze.py, imported read-only): native NATIVITY 1-4;
civilian EMPSTAT != 1; HISPAN 901/902 unknown and excluded; Mexican HISPAN 100/102/103/104/108/109; US
birthplace code < 15000. Weights WTFINL (monthly) and ASECWT (ASEC; 2014 halved). Earnings (ASEC only):
INCWAGE > 0 in 2024 dollars (BLS CPI-U, income year = survey year - 1). Records, not unique persons, enter
the means (a household is seen up to twice).

This script reads one survey year at a time and writes weighted totals by (group, stratum, age x sex cell,
random group) to _cache/agg_*.parquet; estimate.py turns them into gaps, ratios and bootstrap SEs. Each
household cluster (CPSID, else the survey month's household) is assigned to one of K random groups by a fixed
hash, so both appearances of a household stay together.

Run from the repository root (stage.py first, estimate.py after):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/vintage.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # imports from other lanes must not write their __pycache__

import gc
import importlib.util
import json
import resource
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute  # noqa: F401  (pa.compute)
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
CPI = FISCAL / "ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load("g3_asec", FISCAL / "g3_identity_pooled_2026_10_05/analyze.py")
co = an.co

K = 1000  # random groups of household clusters (estimate.py draws them)
XS_KEYS = ["grp", "coh", "period", "state", "cell", "bucket"]
LIN_KEYS = ["type", "pcoh", "state", "cid", "cell", "bucket"]
STATE = {48: 1, 35: 1, 6: 2}  # 1 Texas + New Mexico, 2 California, 0 elsewhere
STATE_NAME = {0: "elsewhere", 1: "TX_NM", 2: "CA"}
COHORTS = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2002]  # birth-year band edges for the cross-section
PCOHORTS = [1900, 1940, 1950, 1960, 1970, 2010]  # parent birth-year bands for the lineage
PERIODS = [1994, 2007, 2022, 2026, 2027]  # survey-year bands: 1994-2006, 2007-21, 2022-25 (the ladder's), 2026
XS_GROUPS = {0: "white3plus", 1: "G2", 2: "G3plus_id"}
LIN_TYPES = {0: "white_pair", 1: "g1g2", 2: "g2g3", 3: "g3g4", 4: "white_pair_both"}
X = ["ba", "lths", "yrs", "emp", "earn"]
UNIT = {"ba": "pct", "lths": "pct", "yrs": "years", "emp": "pct", "earn": "usd2024"}
LX = ["ba", "lths", "yrs"]
# Weighted counts by completed-schooling code (an.EDUC_YEARS order) give estimate.py the rank (percentile) gap,
# which, unlike a BA+ gap in points, does not grow when the white BA+ share rises across cohorts.
EDUC_CODES = sorted(an.EDUC_YEARS)


def band(v, edges):
    """Band index of v in [edges[i], edges[i+1]); -1 outside."""
    i = np.searchsorted(edges, v, side="right") - 1
    return np.where((v >= edges[0]) & (v < edges[-1]), i, -1)


def band_name(i, edges):
    return f"{edges[i]}-{edges[i + 1] - 1}"


def bucket(cluster: np.ndarray) -> np.ndarray:
    """splitmix64 of the cluster key, mod K: a fixed random partition of households into K groups."""
    z = cluster.astype(np.int64).view(np.uint64) + np.uint64(0x9E3779B97F4A7C15)
    with np.errstate(over="ignore"):
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
    return (z % np.uint64(K)).astype(np.int64)


def parent_index(d: pd.DataFrame, sample: np.ndarray) -> np.ndarray:
    """Row index of each linked parent [n, 4] in the order of an.PARENT_LINKS (-1 if none), linked within
    (sample, SERIAL) by PERNUM, as an.classify() links them."""
    n = len(d)
    key = (sample * 100_000 + d.SERIAL.to_numpy(np.int64)) * 100 + d.PERNUM.to_numpy(np.int64)
    order = np.argsort(key, kind="stable")
    skey = key[order]
    hh = key - d.PERNUM.to_numpy(np.int64)
    P = np.full((n, 4), -1, np.int64)
    for j, (loc, _) in enumerate(an.PARENT_LINKS):
        line = d[loc].to_numpy(np.int64)
        has = line > 0
        pos = np.minimum(np.searchsorted(skey, hh + line), n - 1)
        found = has & (skey[pos] == hh + line)
        if np.any(has & ~found):
            raise ValueError(f"{loc}: pointer to a missing person")
        P[found, j] = order[pos[found]]
    return P


def first_slot(P: np.ndarray, flag: np.ndarray) -> np.ndarray:
    """Index of the first linked parent (slot order) whose flag is true; -1 if none."""
    out = np.full(len(P), -1, np.int64)
    for j in range(P.shape[1] - 1, -1, -1):
        p = P[:, j]
        ok = (p >= 0) & flag[np.maximum(p, 0)]
        out = np.where(ok, p, out)
    return out


def process(d: pd.DataFrame, source: str, cpi: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    year = int(d.YEAR.iloc[0])
    sample = d.YEAR.to_numpy(np.int64) * 100 + d.MONTH.to_numpy(np.int64)
    n = len(d)
    age, sex = d.AGE.to_numpy(), d.SEX.to_numpy()
    bpl, mbpl, fbpl = d.BPL.to_numpy(), d.MBPL.to_numpy(), d.FBPL.to_numpy()
    hisp, race = d.HISPAN.to_numpy(), d.RACE.to_numpy()
    if source == "asec":
        w = d.ASECWT.to_numpy(float) * (0.5 if year == 2014 else 1.0)
    else:
        w = d.WTFINL.to_numpy(float)
    us = lambda b: b < an.US_MAX
    native = d.NATIVITY.between(1, 4).to_numpy()
    civ = ~d.EMPSTAT.eq(1).to_numpy()
    known = ~np.isin(hisp, an.UNKNOWN_HISPAN)
    mex = np.isin(hisp, an.MEX_HISPAN)
    par_us = us(mbpl) & us(fbpl)
    mex_par = (mbpl == an.MEXICO) | (fbpl == an.MEXICO)
    white = native & civ & par_us & (hisp == 0) & (race == 100)
    educ = d.EDUC.to_numpy()
    x = {"ba": (educ >= 111).astype(float), "lths": (educ <= 71).astype(float),
         "yrs": pd.Series(educ).map(an.EDUC_YEARS).to_numpy(float),
         "emp": d.EMPSTAT.isin([10, 12]).to_numpy().astype(float)}
    worker = np.zeros(n, bool)
    x["earn"] = np.zeros(n)
    if source == "asec":
        inc = d.INCWAGE.to_numpy(float)
        worker = (inc > 0) & (inc < 99999998)
        x["earn"] = np.where(worker, inc * cpi.loc[2024] / cpi.loc[year - 1], 0.0)
    if np.isnan(x["yrs"][age >= 25]).any():
        raise ValueError(f"{source} {year}: unmapped EDUC at 25+")
    hhkey = -(sample * 100_000 + d.SERIAL.to_numpy(np.int64))
    cid = d.CPSID.to_numpy(np.int64)
    bk = bucket(np.where(cid > 0, cid, hhkey))
    state = pd.Series(d.STATEFIP.to_numpy()).map(STATE).fillna(0).astype(int).to_numpy()

    # 1. Cross-section, adults 25-64.
    grp = np.full(n, -1)
    grp[white] = 0
    grp[native & civ & known & mex_par] = 1
    grp[native & civ & mex & par_us] = 2
    xs = (grp >= 0) & (age >= 25) & (age <= 64)
    coh = band(year - age, np.array(COHORTS))
    if (xs & (coh < 0)).any():
        raise ValueError("birth cohort outside the bands")
    cell = co.age_cells(age, sex, "pop")
    period = int(band(np.array([year]), np.array(PERIODS))[0])
    r = np.flatnonzero(xs)  # build only the analysis rows: memory
    wr = w[r]
    X_ = pd.DataFrame({"grp": grp[r], "coh": coh[r], "period": period, "state": state[r], "cell": cell[r],
                       "bucket": bk[r], "n": 1, "w": wr, "wage": wr * age[r],
                       **{f"w_{k}": wr * x[k][r] for k in ("ba", "lths", "yrs", "emp")},
                       "w_earnw": wr * worker[r], "w_earn": wr * x["earn"][r],
                       **{f"w_e{i}": wr * (educ[r] == c) for i, c in enumerate(EDUC_CODES)}})
    xs_agg = X_.groupby(XS_KEYS, sort=True).sum().reset_index()
    del X_
    ids = pd.DataFrame({"grp": grp, "coh": coh, "period": period, "state": state,
                        "pid": np.where(d.CPSIDP.to_numpy() > 0, d.CPSIDP.to_numpy(), -(np.arange(n) + year * 10**7))})
    ids = ids[xs & (grp > 0)]

    # 2. Lineage pairs, children 25+.
    P = parent_index(d, sample)
    linked = P >= 0
    nlink = linked.sum(1)
    if nlink.max() > 2:
        raise ValueError("more than two linked parents")
    pb = np.where(linked, bpl[np.maximum(P, 0)], 0)
    consistent = ~(linked & ~us(pb)).any(1)
    p_mexborn = bpl == an.MEXICO
    p_g2 = us(bpl) & mex_par
    p_gpus = us(bpl) & par_us
    p_g3mex = p_gpus & mex
    p_white = p_gpus & (hisp == 0) & (race == 100)
    all_gp_us = (nlink == 2) & (~linked | p_gpus[np.maximum(P, 0)]).all(1)
    base = native & civ & known & (age >= 25)
    child = {
        1: (base & mex_par, first_slot(P, p_mexborn)),
        2: (base & par_us & consistent, first_slot(P, p_g2)),
        3: (base & par_us & consistent & all_gp_us, first_slot(P, p_g3mex)),
        0: (white & (age >= 25) & consistent, first_slot(P, p_white)),
    }
    # Gate: the g2g3 children are exactly the pooled lane's G3 lineage at 25+ (an.classify, all link rules).
    g = an.classify(d, False, sample)
    mine = child[2][0] & (child[2][1] >= 0)
    theirs = g["G3anc"] & g["one"] & (age >= 25)
    if not np.array_equal(mine, theirs):
        raise ValueError(f"{source} {year}: g2g3 children differ from an.classify G3anc ({mine.sum()} vs {theirs.sum()})")
    rows = []
    for t, (m, par) in child.items():
        use = m & (par >= 0)
        if t == 0:
            for tt, extra in ((0, np.ones(n, bool)), (4, all_gp_us)):
                rows.append((tt, use & extra, par))
        else:
            rows.append((t, use, par))
    parts_c, parts_p, lin_ids = [], [], []
    implausible = {}
    for t, use, par in rows:
        idx = np.flatnonzero(use)
        p = par[idx]
        # A linked parent fewer than 14 years older than the child is a mislink or a step-parent of the
        # child's own generation; such pairs are dropped and counted.
        old_enough = age[p] - age[idx] >= 14
        implausible[LIN_TYPES[t]] = int((~old_enough).sum())
        ok = (age[p] >= 25) & old_enough
        idx, p = idx[ok], p[ok]
        if np.isnan(x["yrs"][p]).any():
            raise ValueError("unmapped parent EDUC")
        pc = band(year - age[p], np.array(PCOHORTS))
        if (pc < 0).any():
            raise ValueError("parent cohort outside the bands")
        keys = dict(type=np.full(len(idx), t), pcoh=pc, state=state[idx], cid=mex[idx].astype(int), bucket=bk[idx])
        wi = w[idx]
        parts_c.append(pd.DataFrame({**keys, "cell": co.age_cells(age[idx], sex[idx], "cores_one"), "n": 1, "w": wi,
                                     "wage": wi * age[idx], **{f"w_{k}": wi * x[k][idx] for k in LX},
                                     **{f"w_e{i}": wi * (educ[idx] == c) for i, c in enumerate(EDUC_CODES)}}))
        pcell = np.minimum(np.digitize(age[p], np.arange(30, 90, 5)), 12) * 2 + (sex[p] - 1)
        parts_p.append(pd.DataFrame({**keys, "cell": pcell, "n": 1, "w": wi, "wage": wi * age[p],
                                     **{f"w_{k}": wi * x[k][p] for k in LX},
                                     **{f"w_e{i}": wi * (educ[p] == c) for i, c in enumerate(EDUC_CODES)}}))
        if t:
            lin_ids.append(pd.DataFrame({"type": t, "pcoh": pc, "state": state[idx], "cid": mex[idx].astype(int),
                                         "pid": np.where(d.CPSIDP.to_numpy()[idx] > 0, d.CPSIDP.to_numpy()[idx],
                                                         -(idx + year * 10**7))}))
    keys = ["type", "pcoh", "state", "cid", "cell", "bucket"]
    lc = pd.concat(parts_c).groupby(keys, sort=True).sum().reset_index()
    lp = pd.concat(parts_p).groupby(keys, sort=True).sum().reset_index()
    audit = dict(year=year, rows=n, xs_rows=int(xs.sum()), g2g3_children=int(mine.sum()),
                 pairs_dropped_parent_under_14_years_older=implausible)
    return xs_agg, (lc, lp), pd.concat([ids.assign(frame="xs"), *[i.assign(frame="lin") for i in lin_ids]]), audit


def main():
    # mimalloc, Arrow's default pool, kept each year's buffers: peak RSS reached 2.1 GiB; the system pool
    # with a collection per year stays near 0.6 GiB.
    pa.set_memory_pool(pa.system_memory_pool())
    DERIVED.mkdir(exist_ok=True)
    cpi = pd.read_csv(CPI).set_index("year").cpi_u
    audit = {"stage": json.loads((DERIVED / "stage_audit.json").read_text()), "K": K, "years": {}}
    for src in ("monthly", "asec"):
        pf = pq.ParquetFile(CACHE / f"{src}.parquet")
        stats = [pf.metadata.row_group(i).column(0).statistics for i in range(pf.num_row_groups)]
        if pf.schema_arrow.names[0] != "YEAR" or any(st is None for st in stats):
            raise ValueError("staged parquet lacks YEAR row-group statistics")
        years = sorted(pq.read_table(CACHE / f"{src}.parquet", columns=["YEAR"]).column(0).unique().to_pylist())
        # Each year's totals go to a part file; DuckDB then sums them by key (one thread, keys ordered, so the
        # summation order and the output bytes are fixed). Holding the running totals in pandas grew the
        # process past 2 GiB.
        parts = CACHE / "parts"
        parts.mkdir(exist_ok=True)
        for old in parts.glob(f"{src}_*.parquet"):
            old.unlink()
        for y in years:
            # Row groups whose YEAR range covers y (the file is in year order), then the year's rows.
            t = pf.read_row_groups([j for j, st in enumerate(stats) if st.min <= y <= st.max])
            d = t.filter(pa.compute.equal(t.column("YEAR"), y)).to_pandas()
            del t
            xa, (lc, lp), ids, au = process(d, src, cpi)
            del d
            for k, v in (("xs", xa), ("lc", lc), ("lp", lp), ("ids", ids)):
                v.to_parquet(parts / f"{src}_{k}_{y}.parquet", index=False)
            del xa, lc, lp, ids
            gc.collect()
            audit["years"][f"{src}_{y}"] = au
        con = duckdb.connect()
        con.execute("SET threads = 1")
        con.execute("SET memory_limit = '512MB'")
        con.execute(f"SET temp_directory = '{CACHE / 'duckdb_tmp'}'")
        for k, keys in (("xs", XS_KEYS), ("lc", LIN_KEYS), ("lp", LIN_KEYS), ("ids", None)):
            src_glob = f"read_parquet('{parts}/{src}_{k}_*.parquet', union_by_name = true)"
            out = CACHE / f"agg_{src}_{k}.parquet"
            if keys is None:
                con.execute(f"COPY (SELECT * FROM {src_glob}) TO '{out}' (FORMAT parquet)")
                continue
            cols = [c for c in con.execute(f"SELECT * FROM {src_glob} LIMIT 0").df().columns if c not in keys]
            k_sql = ", ".join(keys)
            con.execute(f"COPY (SELECT {k_sql}, {', '.join(f'sum({c}) AS {c}' for c in cols)} FROM {src_glob} "
                        f"GROUP BY {k_sql} ORDER BY {k_sql}) TO '{out}' (FORMAT parquet)")
        con.close()
        print(f"  ✓ {src}: {len(years)} years aggregated, peak RSS "
              f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MiB", flush=True)
    (DERIVED / "aggregate_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
