"""Closing share c of Mexican-origin G3 non-identifiers on the IPUMS-CPS basic monthly files, MIS 1 and 5.

The ASEC pool (analyze.py) reaches 325 unique G3 non-identifiers aged 25+. Parents' birthplace is asked every
month since January 1994, and every CPS household enters at month-in-sample (MIS) 1 and returns at MIS 5 a
year later, so the basic monthly files at MIS 1 and 5 see every household the CPS samples, about three times
the households that pass through a March ASEC. Data: IPUMS-CPS extract 5 (extract_monthly.py), 391 basic
monthly samples January 1994 - August 2026 (October 2025 was not fielded), case-selected to households at
MISH 1 and 5; no income questions, so no earnings.

Design: analyze.py's, imported read-only (classify, codes, measures, contrasts; the carry-over lane's age x
sex cells). Adults 18+ living with a linked parent (`cores_one`); G3 lineage = native-born, both own parents
US-born, civilian, every linked parent US-born, and a Mexico-born grandparent read from a linked parent's
MBPL/FBPL; identifiers report a Mexican HISPAN code. Reference: third-plus non-Hispanic whites in the same
frame, reweighted to each group's age x sex cells. Weights WTFINL (zero only for armed forces, who fail the
civilian screen).

One record per person: a person can appear at MIS 1 and again at MIS 5. Records are deduplicated on CPSIDV
(validated person ID) where nonzero, else CPSIDP, keeping the first record in time. IPUMS's person IDs do not
link MIS 1 months June 1994 - August 1995 to their MIS 5 a year later (no adult recurs; linkage() finds the
months from the data), so the primary rule also drops the MIS 5 records of those cohorts, which would
otherwise count most of their people twice. Sensitivities: the plain CPSIDV rule; CPSIDP; no dedupe; MIS 1
only (no linking); rule-11 parent links only; the union with March-basic ASEC persons the monthly frame never
sees (matched on CPSIDV/CPSIDP, ASECWT weights, 2014 halved). ASEC oversample persons cannot be linked to the
monthly files though their households were interviewed there, so the union that adds them is an upper bound.

SEs: cluster bootstrap, B = 500, seed 20261006. Cluster = CPSID household (fallback source-year-month-SERIAL);
stratum = the cluster's first year; clusters drawn with replacement within stratum, among clusters with
analysis rows. Every statistic is a function of weighted totals by age x sex cell, so the bootstrap runs on
(cell, cluster) totals instead of an n x B weight matrix.

Loading: DuckDB streams the gzipped CSVs twice: once to flag households holding a Mexico-born parent of anyone
or a white reference candidate (18+, native, both parents US-born, white, not Hispanic, with a parent link),
once to return those households' rows only. classify() is household-local, so the filter is exact.

Gates: (0) the ASEC frame rebuilt through this loader and estimator reproduces analyze.py's published points
exactly; (1) 2022-25 monthly unique counts against the ASEC frame's, and the identifier BA+ gap; (2) the
identity-loss rate by period against the ASEC's.

Run from the repository root (analyze.py first: gate 0 reads its derived/gaps.csv):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/analyze_monthly.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # imports from other lanes must not write their __pycache__

import csv
import importlib.util
import json
import math
import resource
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
MONTHLY = CACHE / "monthly_mis15.csv.gz"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load("g3_asec", HERE / "analyze.py")
cs = _load("carryover_corrected_step", FISCAL / "carryover_identity_2026_09_27/corrected_step.py")
co = an.co

B = 500
SEED = 20261006
CHUNK = 25  # bootstrap columns per pass over the (cell, cluster) totals
NCELLS = 38  # co.age_cells for the co-resident frames: 19 age bins x 2 sexes
DUCK_MEMORY = "512MB"
GROUPS = an.GROUPS
MEASURES = {m: an.MEASURES[m] for m in ("ba_plus", "ba_plus_22plus", "educ_years", "employed")}
VALIDITY = {"25": ["ba_plus", "educ_years"], "22": ["ba_plus_22plus"], "18": ["employed"]}
MIN_AGE = {"25": 25, "22": 22, "18": 18}
YEARSETS = {"1994_2026": (1994, 2026), "1994_2006": (1994, 2006), "2007_2021": (2007, 2021),
            "2022_2026": (2022, 2026), "1994_2002": (1994, 2002), "2003_2026": (2003, 2026),
            "2022_2025": (2022, 2025)}
PERIODS = ["1994_2006", "2007_2021", "2022_2026"]
COLS = ["YEAR", "MONTH", "SERIAL", "CPSID", "CPSIDP", "CPSIDV", "PERNUM", "AGE", "SEX", "RACE", "HISPAN", "BPL",
        "MBPL", "FBPL", "NATIVITY", "EMPSTAT", "EDUC", "MOMLOC", "POPLOC", "MOMLOC2", "POPLOC2", "MOMRULE", "POPRULE"]
BIG = {"CPSID", "CPSIDP", "CPSIDV"}
CANDIDATE = ("MBPL = 20000 OR FBPL = 20000 OR (AGE >= 18 AND NATIVITY BETWEEN 1 AND 4 AND MBPL < 15000 "
             "AND FBPL < 15000 AND HISPAN = 0 AND RACE = 100 AND (MOMLOC > 0 OR POPLOC > 0 OR MOMLOC2 > 0 OR POPLOC2 > 0))")


def load(path: Path, weight: str, extra: list[str]) -> tuple[pd.DataFrame, dict]:
    """Rows of every household that can hold an analysis person, sorted by year, month, SERIAL, PERNUM."""
    cols = COLS + [weight] + extra
    types = {c: "BIGINT" if c in BIG else "DOUBLE" if c == weight else "INTEGER" for c in cols}
    con = duckdb.connect()
    con.execute(f"SET memory_limit = '{DUCK_MEMORY}'")
    con.execute("SET threads = 2")
    con.execute(f"SET temp_directory = '{CACHE / 'duckdb_tmp'}'")
    src = f"read_csv('{path}', header = true, types = {types!r})"
    con.execute(f"CREATE TEMP TABLE hh AS SELECT YEAR, MONTH, SERIAL, count(*) AS n, bool_or({CANDIDATE}) AS keep "
                f"FROM {src} GROUP BY YEAR, MONTH, SERIAL")
    rows, households, kept_rows, kept_households = con.execute(
        "SELECT sum(n), count(*), sum(n) FILTER (WHERE keep), count(*) FILTER (WHERE keep) FROM hh").fetchone()
    rel = con.execute(f"SELECT {', '.join('s.' + c for c in cols)} FROM {src} s "
                      "JOIN (SELECT YEAR, MONTH, SERIAL FROM hh WHERE keep) k USING (YEAR, MONTH, SERIAL) "
                      "ORDER BY s.YEAR, s.MONTH, s.SERIAL, s.PERNUM")
    parts = []  # fetched in chunks: a single .df() peaked at 1.9 GiB for this 0.27 GiB frame, chunks at 1.2 GiB
    while len(chunk := rel.fetch_df_chunk(64)):
        parts.append(chunk)
    d = pd.concat(parts, ignore_index=True)
    del parts
    con.close()
    if d[cols].isna().any().any():
        raise ValueError(f"{path.name}: missing values in {d.columns[d.isna().any()].tolist()}")
    if d.duplicated(["YEAR", "MONTH", "SERIAL", "PERNUM"]).any():
        raise ValueError(f"{path.name}: duplicate person key")
    stats = dict(file=str(path.relative_to(FISCAL.parents[1])), sha256=an.sha(path), rows=int(rows),
                 households=int(households), kept_rows=int(kept_rows), kept_households=int(kept_households))
    return d, stats


def frame_rows(d: pd.DataFrame, source: int, weight: np.ndarray) -> dict:
    """Analysis rows (adults 18+ in a co-resident frame and a group or the reference, either link rule), one
    survey year at a time to bound memory (households never span years)."""
    years = d.YEAR.to_numpy()
    starts = np.flatnonzero(np.r_[True, years[1:] != years[:-1]])
    if (np.diff(years[starts]) <= 0).any():
        raise ValueError("rows are not sorted by year")
    ends = np.r_[starts[1:], len(d)]
    return concat([_frame_rows(d.iloc[a:b], source, weight[a:b]) for a, b in zip(starts, ends)])


def _frame_rows(d: pd.DataFrame, source: int, weight: np.ndarray) -> dict:
    sample = d.YEAR.to_numpy(np.int64) * 100 + d.MONTH.to_numpy(np.int64)
    flags, keep = {}, np.zeros(len(d), bool)
    for links, direct in (("all", False), ("direct", True)):
        g = an.classify(d, direct, sample)
        keep |= g["one"] & np.logical_or.reduce([g[k] for k in GROUPS + ["white3plus"]])
        for k in GROUPS + ["white3plus", "one", "single", "both"]:
            flags[f"{links}:{k}"] = g[k]
    keep &= d.AGE.ge(18).to_numpy()
    x = {f"x_{m}": fv(d).to_numpy(float) for m, (fv, _, _) in MEASURES.items()}
    if np.isnan(x["x_educ_years"][keep & d.AGE.ge(25).to_numpy()]).any():
        raise ValueError("unmapped EDUC code at 25+ among analysis rows")
    hh = -(source * 10**12 + sample * 100_000 + d.SERIAL.to_numpy(np.int64))
    out = dict(source=np.full(len(d), source, np.int8), year=d.YEAR.to_numpy(), month=d.MONTH.to_numpy(),
               mish=d.MISH.to_numpy() if "MISH" in d else np.zeros(len(d), int),
               cpsidp=d.CPSIDP.to_numpy(), cpsidv=d.CPSIDV.to_numpy(),
               cluster_key=np.where(d.CPSID.to_numpy() > 0, d.CPSID.to_numpy(), hh),
               w=weight, age=d.AGE.to_numpy(), sex=d.SEX.to_numpy(), **flags, **x)
    return {k: np.asarray(v)[keep] for k, v in out.items()}


def concat(parts: list[dict]) -> dict:
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}


def multiplicities(keys: np.ndarray, years: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Cluster index per row and uint8 multiplicities [clusters, B+1] (column 0 = the full sample)."""
    uk, cl = np.unique(keys, return_inverse=True)
    first = np.full(len(uk), 10_000)
    np.minimum.at(first, cl, years)
    rng = np.random.Generator(np.random.PCG64(SEED))
    mult = np.ones((len(uk), B + 1), np.uint8)
    for y in np.unique(first):
        ids = np.flatnonzero(first == y)
        n = len(ids)
        draws = rng.integers(0, n, (B, n)) + (np.arange(B) * n)[:, None]
        counts = np.bincount(draws.ravel(), minlength=B * n).reshape(B, n)
        if counts.max() > 255:
            raise ValueError("multiplicity overflows uint8")
        mult[ids, 1:] = counts.T
    return cl, mult


class Totals:
    """Weighted totals by age x sex cell for every bootstrap column, from (cell, cluster) aggregates."""

    def __init__(self, A: dict, cl: np.ndarray, mult: np.ndarray):
        self.A, self.cl, self.mult = A, cl, mult
        self.ncl = mult.shape[0]
        self.cell = co.age_cells(A["age"], A["sex"], "cores_one")
        if self.cell.max() >= NCELLS:
            raise ValueError("age x sex cell out of range")

    def sums(self, mask: np.ndarray, xs: list[np.ndarray]) -> list[np.ndarray]:
        idx = np.flatnonzero(mask)
        if idx.size == 0:
            return [np.zeros((NCELLS, B + 1)) for _ in range(1 + len(xs))]
        key = self.cell[idx].astype(np.int64) * self.ncl + self.cl[idx]
        uk, inv = np.unique(key, return_inverse=True)
        w = self.A["w"][idx]
        aggs = [np.bincount(inv, weights=w)] + [np.bincount(inv, weights=w * x[idx]) for x in xs]
        pc, pk = uk // self.ncl, uk % self.ncl
        starts = np.flatnonzero(np.r_[True, pc[1:] != pc[:-1]])
        cells = pc[starts]
        out = [np.zeros((NCELLS, B + 1)) for _ in aggs]
        for c0 in range(0, B + 1, CHUNK):
            m = self.mult[pk, c0:c0 + CHUNK].astype(np.float64)
            for o, a in zip(out, aggs):
                o[cells, c0:c0 + CHUNK] = np.add.reduceat(a[:, None] * m, starts, axis=0)
        return out


def gap_reps(gw, gx, rw, rx, scale):
    """Group mean, reference mean reweighted to the group's age x sex mix over covered cells, and the gap
    (co.reweight's estimator, written on cell totals)."""
    with np.errstate(invalid="ignore", divide="ignore"):  # a draw can miss a small group entirely
        mean_g = gx.sum(0) / gw.sum(0)
        cov = rw > 0
        share = np.where(cov, gw / gw.sum(0), 0.0)
        mref = np.divide(rx, rw, out=np.zeros_like(rx), where=cov)
        ref = (share * mref).sum(0) / share.sum(0)
    return mean_g * scale, ref * scale, (mean_g - ref) * scale


def estimate(T: Totals, runs: list[tuple]) -> tuple[list[dict], dict]:
    A, rows, reps_by = T.A, [], {}
    for label, links, mask, frames in runs:
        reps = {}
        for frame in frames:
            fr = mask & A[f"{links}:{frame.replace('cores_', '')}"]
            for vc, ms in VALIDITY.items():
                ok = fr & (A["age"] >= MIN_AGE[vc])
                xs = [A[f"x_{m}"] for m in ms]
                ref = ok & A[f"{links}:white3plus"]
                R = T.sums(ref, xs)
                for g in GROUPS:
                    use = ok & A[f"{links}:{g}"]
                    if use.sum() < 2:
                        continue
                    G = T.sums(use, xs)
                    for i, m in enumerate(ms):
                        unit = MEASURES[m][2]
                        vg, vr, gap = gap_reps(G[0], G[1 + i], R[0], R[1 + i], 100 if unit == "pct" else 1)
                        reps[(frame, m, g)] = gap
                        reps[(frame, m, g, "weight")] = G[0].sum(0)
                        rows.append(dict(label=label, links=links, frame=frame, measure=m, unit=unit, group=g,
                                         n=int(use.sum()), n_ref=int(ref.sum()), weighted=float(G[0][:, 0].sum()),
                                         mean_age=float(np.average(A["age"][use], weights=A["w"][use])),
                                         value=float(vg[0]), ref_value_age_matched=float(vr[0]), gap=float(gap[0]),
                                         se=float(np.std(gap[1:], ddof=1))))
        reps_by[(label, links)] = reps
        print(f"  ✓ {label} {links}", flush=True)
    return rows, reps_by


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def first_record(pid: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Rows of `mask` that are the first record (rows are in time order) of their person ID; rows without an
    ID are kept."""
    idx = np.flatnonzero(mask)
    dup = pd.Series(pid[idx]).duplicated().to_numpy() & (pid[idx] > 0)
    out = np.zeros(len(pid), bool)
    out[idx[~dup]] = True
    return out


def closing(reps, frame="cores_one", m="ba_plus", nid="G3anc_nonmex"):
    return 1 - reps[(frame, m, nid)] / reps[(frame, m, "G3anc_id")]


def sd(v):
    v = v[1:][np.isfinite(v[1:])]
    return float(np.std(v, ddof=1))


def linkage(d: pd.DataFrame) -> tuple[list[dict], list[int]]:
    """Share of adults 18+ seen at MIS 1 whose person ID recurs at MIS 5, by MIS 1 year (kept households), and
    the MIS 1 months whose people never recur (a break in IPUMS's person linking: no dedupe is possible for
    their MIS 5 records). MIS 1 months whose MIS 5 month is outside the extract are left out."""
    ym = d.YEAR.to_numpy() * 12 + d.MONTH.to_numpy() - 1
    months = set(np.unique(ym))
    mis1 = (d.MISH.to_numpy() == 1) & (d.AGE.to_numpy() >= 18) & np.isin(ym + 12, list(months))
    mis5 = d.MISH.to_numpy() == 5
    out, broken = [], []
    for idname in ("CPSIDV", "CPSIDP"):
        ids = d[idname].to_numpy()
        seen5 = np.isin(ids, ids[mis5])
        for y in np.unique(d.YEAR.to_numpy()[mis1]):
            m = mis1 & (d.YEAR.to_numpy() == y)
            out.append(dict(measure=f"adults at MIS 1 whose {idname} recurs at MIS 5", year=int(y), base=int(m.sum()),
                            hits=int((m & seen5).sum()), share=float((m & seen5).sum() / m.sum())))
        if idname == "CPSIDV":
            by_month = pd.DataFrame({"ym": ym[mis1], "seen": seen5[mis1]}).groupby("ym").seen.agg(["mean", "size"])
            broken = [int(t) for t, r in by_month.iterrows() if r["mean"] < 0.05 and r["size"] >= 100]
    return out, broken


def main():
    DERIVED.mkdir(exist_ok=True)
    (CACHE / "duckdb_tmp").mkdir(exist_ok=True)
    audit = {}

    dm, audit["monthly"] = load(MONTHLY, "WTFINL", ["MISH"])
    audit["monthly"]["mish_values"] = sorted(int(v) for v in dm.MISH.unique())
    link_rows, broken = linkage(dm)
    kept_ids = np.unique(dm.CPSIDP.to_numpy())
    M = frame_rows(dm, 0, dm.WTFINL.to_numpy(float))
    del dm
    print(f"  ✓ monthly: {audit['monthly']['rows']:,} rows, {len(M['w']):,} analysis rows", flush=True)
    da, audit["asec"] = load(an.DATA, "ASECWT", [])
    S = frame_rows(da, 1, da.ASECWT.to_numpy(float) * np.where(da.YEAR.to_numpy() == 2014, 0.5, 1.0))
    del da
    print(f"  ✓ ASEC: {audit['asec']['rows']:,} rows, {len(S['w']):,} analysis rows", flush=True)
    if (M["w"] <= 0).any():
        raise ValueError("monthly analysis row with zero weight")
    A = concat([M, S])
    del M, S
    mon, asec = A["source"] == 0, A["source"] == 1
    yr = A["year"]
    pid = np.where(A["cpsidv"] > 0, A["cpsidv"], A["cpsidp"])
    # MIS 5 records whose MIS 1 month is in a linking break cannot be matched to their MIS 1 record; the primary
    # rule drops them (one record per person), the brief's plain CPSIDV rule keeps them.
    unlinkable = mon & (A["mish"] == 5) & np.isin(A["year"] * 12 + A["month"] - 1 - 12, broken)
    keep_plain = first_record(pid, mon)
    keep_m = keep_plain & ~unlinkable
    keep_p = first_record(A["cpsidp"], mon) & ~unlinkable
    keep_a = first_record(np.where(asec, A["cpsidp"], 0), asec)  # analyze.dedupe: CPSIDP, first ASEC year
    # ASEC oversample records (IPUMS sets the first-in-sample month of their CPSIDP to 13) cannot be linked to the
    # basic monthly files, though their households were interviewed there, so only March-basic ASEC persons are
    # added without double counting; the version with the oversample is an upper bound.
    over = asec & ((A["cpsidp"] // 10**8) % 100 == 13)
    seen_v, seen_p = A["cpsidv"][mon], A["cpsidp"][mon]
    add_a = keep_a & ~((A["cpsidv"] > 0) & np.isin(A["cpsidv"], seen_v[seen_v > 0])) \
        & ~((A["cpsidp"] > 0) & np.isin(A["cpsidp"], seen_p[seen_p > 0]))
    cl, mult = multiplicities(A["cluster_key"], yr)
    T = Totals(A, cl, mult)
    print(f"  ✓ bootstrap: {mult.shape[0]:,} clusters x {B} draws", flush=True)

    def years(k):
        a, b = YEARSETS[k]
        return (yr >= a) & (yr <= b)

    ALL3 = ["cores_one", "cores_single", "cores_both"]
    runs = [("monthly_1994_2026_dedup", "all", keep_m, ALL3),
            ("monthly_1994_2026_dedup", "direct", keep_m, ["cores_one"]),
            ("monthly_1994_2026_dedup_plain", "all", keep_plain, ["cores_one"]),
            ("monthly_1994_2026_dedup_cpsidp", "all", keep_p, ["cores_one"]),
            ("monthly_1994_2026_nodedup", "all", mon, ["cores_one"]),
            ("monthly_1994_2026_mis1", "all", mon & (A["mish"] == 1), ["cores_one"]),
            ("union_1994_2026_dedup", "all", keep_m | (add_a & ~over), ["cores_one"]),
            ("union_with_oversample_1994_2026_dedup", "all", keep_m | add_a, ["cores_one"])]
    runs += [(f"monthly_{k}_dedup", "all", keep_m & years(k), ["cores_one"]) for k in YEARSETS if k != "1994_2026"]
    runs += [("asec_1994_2026_dedup", "all", keep_a, ALL3)]
    runs += [(f"asec_{k}_dedup", "all", keep_a & years(k), ["cores_one"]) for k in YEARSETS if k != "1994_2026"]
    runs += [("asec_2022_2025_nodedup", "all", asec & years("2022_2025"), ["cores_one"])]
    rows, R = estimate(T, runs)
    con = []
    for (label, links), reps in R.items():
        con += an.contrasts(reps, links, label)

    # Gate 0: the rebuilt ASEC frame reproduces analyze.py's published points.
    pub = pd.read_csv(DERIVED / "gaps.csv")
    got = pd.DataFrame(rows)
    pairs = {"asec_1994_2026_dedup": "pooled_1994_2026_dedup", "asec_2022_2025_nodedup": "gate_2022_2025",
             **{f"asec_{k}_dedup": f"period_{k}_dedup" for k in YEARSETS if k not in ("1994_2026", "2022_2025")}}
    cons = []
    for mine, theirs in pairs.items():
        a = got[got.label.eq(mine)].set_index(["frame", "measure", "group"])
        b = pub[pub.label.eq(theirs) & pub.links.eq("all") & pub.measure.isin(list(MEASURES))].set_index(
            ["frame", "measure", "group"])
        b = b[b.index.get_level_values("frame").isin(a.index.get_level_values("frame").unique())]
        j = a.join(b, rsuffix="_pub", how="inner")
        cons.append(dict(rebuilt=mine, published=theirs, cells=len(j), cells_published=len(b),
                         n_mismatch=int((j.n != j.n_pub).sum()), n_ref_mismatch=int((j.n_ref != j.n_ref_pub).sum()),
                         max_abs_gap_diff=float((j.gap - j.gap_pub).abs().max()),
                         max_abs_value_diff=float((j.value - j.value_pub).abs().max())))
        if len(j) != len(b) or cons[-1]["n_mismatch"] or cons[-1]["n_ref_mismatch"] or cons[-1]["max_abs_gap_diff"] > 1e-8:
            raise ValueError(f"[BLOCKED] gate 0: rebuilt {mine} does not reproduce {theirs}: {cons[-1]}")
    write(cons, DERIVED / "monthly_asec_consistency.csv")
    print("  ✓ gate 0: rebuilt ASEC reproduces analyze.py", flush=True)

    write(rows, DERIVED / "monthly_gaps.csv")
    write(con, DERIVED / "monthly_contrasts.csv")

    # Counts of the co-resident G3 lineage, unique persons unless stated.
    sets = {"monthly_dedup": keep_m, "monthly_dedup_plain": keep_plain, "monthly_nodedup": mon, "monthly_mis1": mon & (A["mish"] == 1),
            "asec_dedup": keep_a, "asec_dedup_march_basic": keep_a & ~over, "union_dedup": keep_m | (add_a & ~over),
            "union_with_oversample_dedup": keep_m | add_a}
    counts = []
    for sname, smask in sets.items():
        for k in ["1994_2026", *PERIODS, "2022_2025"]:
            for lo in (18, 25):
                m = smask & years(k) & A["all:one"] & (A["age"] >= lo)
                counts.append(dict(rows=sname, years=k, min_age=lo,
                                   **{g: int((m & A[f"all:{g}"]).sum()) for g in
                                      ["G3anc", "G3anc_id", "G3anc_nonmex", "G3anc_nonhisp", "white3plus"]}))
    write(counts, DERIVED / "monthly_counts.csv")

    # Gates 1 and 2: 2022-25 counts and identifier gap; identity-loss rate by period, monthly against ASEC.
    cdf = pd.DataFrame(counts).set_index(["rows", "years", "min_age"])
    gates = []
    for asec_rows, note in (("asec_dedup", "ratio monthly / ASEC unique persons; expected 1.5-2.5"),
                            ("asec_dedup_march_basic", "ratio monthly / ASEC unique persons outside the oversample")):
        for lo in (25, 18):
            for g in ["G3anc", "G3anc_id", "G3anc_nonmex", "white3plus"]:
                a, b = cdf.loc[("monthly_dedup", "2022_2025", lo), g], cdf.loc[(asec_rows, "2022_2025", lo), g]
                gates.append(dict(gate="1 counts 2022-25", item=f"{g} {lo}+, {asec_rows}", monthly=a, asec=b,
                                  diff=a / b, se=math.nan, z=math.nan, note=note))
    gm, ga = R[("monthly_2022_2025_dedup", "all")], R[("asec_2022_2025_dedup", "all")]
    gn = R[("asec_2022_2025_nodedup", "all")]
    for nm, (x, y) in {"identifier BA+ gap, monthly - ASEC IPUMS (dedup)": (gm, ga),
                       "identifier BA+ gap, monthly - ASEC IPUMS (no dedupe, analyze.py gate)": (gm, gn)}.items():
        dv = x[("cores_one", "ba_plus", "G3anc_id")] - y[("cores_one", "ba_plus", "G3anc_id")]
        gates.append(dict(gate="1 gap 2022-25", item=nm, monthly=float(x[("cores_one", "ba_plus", "G3anc_id")][0]),
                          asec=float(y[("cores_one", "ba_plus", "G3anc_id")][0]), diff=float(dv[0]), se=sd(dv),
                          z=float(dv[0] / sd(dv)), note="same bootstrap draws (overlapping March households)"))
    census = pd.read_csv(an.PUB / "cps_identity_gaps_CPS_ASEC_2022_2025.csv").query(
        "frame == 'cores_one' and measure == 'ba_plus' and generation == 'G3anc_id' and reference == 'white3plus'").iloc[0]
    v = gm[("cores_one", "ba_plus", "G3anc_id")]
    gates.append(dict(gate="1 gap 2022-25", item="identifier BA+ gap, monthly - Census-file ASEC (cps_identity.py)",
                      monthly=float(v[0]), asec=float(census.gap), diff=float(v[0] - census.gap),
                      se=math.hypot(sd(v), census.se), z=float((v[0] - census.gap) / math.hypot(sd(v), census.se)),
                      note="treated as independent; the Census SE is SDR"))
    for k in ["1994_2026", *PERIODS]:
        for m, lo in (("employed", 18), ("ba_plus", 25)):
            x, y = R[(f"monthly_{k}_dedup", "all")], R[(f"asec_{k}_dedup", "all")]
            sx = x[("cores_one", m, "G3anc_nonmex", "weight")] / x[("cores_one", m, "G3anc", "weight")]
            sy = y[("cores_one", m, "G3anc_nonmex", "weight")] / y[("cores_one", m, "G3anc", "weight")]
            dv = sx - sy
            gates.append(dict(gate="2 identity loss", item=f"{k} {lo}+ share not Mexican", monthly=float(sx[0]),
                              asec=float(sy[0]), diff=float(dv[0]), se=sd(dv), z=float(dv[0] / sd(dv)),
                              note="weighted share of the G3 lineage; same bootstrap draws"))
    write(gates, DERIVED / "monthly_gates.csv")

    # Period heterogeneity of c (BA+ and years, cores_one, monthly dedup).
    tests = []
    for m in ("ba_plus", "educ_years"):
        cp = {k: closing(R[(f"monthly_{k}_dedup", "all")], m=m) for k in [*PERIODS, "1994_2002", "2003_2026"]}
        for a, b in (("1994_2006", "2007_2021"), ("2007_2021", "2022_2026"), ("1994_2006", "2022_2026"),
                     ("1994_2002", "2003_2026")):
            dv = cp[a] - cp[b]
            tests.append(dict(measure=m, test=f"{a} - {b}", c_a=float(cp[a][0]), c_b=float(cp[b][0]), value=float(dv[0]),
                              se=sd(dv), z=float(dv[0] / sd(dv)), df=1, p=math.erfc(abs(dv[0] / sd(dv)) / math.sqrt(2))))
        est = np.array([cp[k][0] for k in PERIODS])
        se = np.array([sd(cp[k]) for k in PERIODS])
        wts = 1 / se ** 2
        pooled = (wts * est).sum() / wts.sum()
        q = float((wts * (est - pooled) ** 2).sum())
        tests.append(dict(measure=m, test="Cochran Q, three periods", c_a=float(pooled), c_b=math.nan, value=q,
                          se=math.nan, z=math.nan, df=2, p=math.exp(-q / 2)))
    write(tests, DERIVED / "monthly_period_tests.csv")

    # c3 candidate: the CPS c pooled with NLSY97 Table 13 by corrected_step.pooled_g3's inverse-variance rule, the
    # bootstrap SE in place of the SDR SE. The propagation reads the raw monthly row and pools it itself; the pooled
    # rows are its check. Raw rows carry the SE that enters the weights; n counts G3 non-identifiers. One row per
    # (measure, key); `key` is the machine label, `source` the description.
    sources = {"cps_monthly_1994_2026_raw": "CPS basic monthly MIS 1/5 1994-2026 (this script, B = 500), co-resident "
                                            "G3 adults 25+, not Mexican",
               "nlsy97_table13": "NLSY97 G3 cross-section, not Hispanic (IZA DP12704 Tables 2 and 13)",
               "cps_monthly_1994_2026_pooled": "inverse-variance pool of the monthly c and NLSY97 "
                                               "(corrected_step.pooled_g3 rule)",
               "cps_asec_1994_2026_raw": "CPS ASEC 1994-2026 (analyze.py, B = 400), co-resident G3 adults 25+, "
                                         "not Mexican",
               "cps_asec_1994_2026_pooled": "inverse-variance pool of the ASEC c and NLSY97 (corrected_step.pooled_g3 rule)"}
    asec_con = pd.read_csv(DERIVED / "contrasts.csv").query(
        "label == 'pooled_1994_2026_dedup' and links == 'all' and frame == 'cores_one' "
        "and contrast == 'G3anc: closing share, not Mexican'").set_index("measure")
    asec_n = pub.query("label == 'pooled_1994_2026_dedup' and links == 'all' and frame == 'cores_one' "
                       "and group == 'G3anc_nonmex'").set_index("measure").n
    mon_n = got.query("label == 'monthly_1994_2026_dedup' and links == 'all' and frame == 'cores_one' "
                      "and group == 'G3anc_nonmex'").set_index("measure").n
    c3 = []
    for m in ("ba_plus", "educ_years"):
        g_id = cs.T13[m]["id"][0] - cs.T2[m]["white4plus"][0]
        nl = (cs.T13[m]["nonid"][0] - cs.T13[m]["id"][0]) / -g_id
        nl_se = math.hypot(cs.T13[m]["nonid"][1], cs.T13[m]["id"][1]) / abs(g_id)
        c_mon = closing(R[("monthly_1994_2026_dedup", "all")], m=m)
        raw = {"cps_monthly_1994_2026": (float(c_mon[0]), sd(c_mon), int(mon_n[m])),
               "cps_asec_1994_2026": (float(asec_con.value[m]), float(asec_con.se[m]), int(asec_n[m]))}
        for frame_name, (cv, cse, n) in raw.items():
            wts = np.array([1 / cse ** 2, 1 / nl_se ** 2])
            c3.append(dict(measure=m, key=f"{frame_name}_raw", c=cv, se=cse, n=n))
            if frame_name == "cps_monthly_1994_2026":
                c3.append(dict(measure=m, key="nlsy97_table13", c=nl, se=nl_se, n=11))
            c3.append(dict(measure=m, key=f"{frame_name}_pooled", c=float((wts * [cv, nl]).sum() / wts.sum()),
                           se=float(1 / math.sqrt(wts.sum())), n=n + 11))
    c3 = [dict(measure=r["measure"], key=r["key"], source=sources[r["key"]], c=r["c"], se=r["se"], n=r["n"]) for r in c3]
    if len({(r["measure"], r["key"]) for r in c3}) != len(c3):
        raise ValueError("c3_candidate: duplicate (measure, key)")
    write(c3, DERIVED / "c3_candidate.csv")
    c3_main = next(r for r in c3 if r["measure"] == "ba_plus" and r["key"] == "cps_monthly_1994_2026_pooled")

    # Corrected step, rho* = rho (1 - a c), BA+ (carryover_identity RESULT §1).
    step = []
    for (label, links), reps in R.items():
        if ("cores_one", "ba_plus", "G3anc_nonmex") not in reps:
            continue
        c = closing(reps)
        step.append(dict(label=label, links=links, c=float(c[0]), se_c=sd(c)))
    step.append(dict(label="c3 candidate: monthly + NLSY97 pool", links="all", c=c3_main["c"], se_c=c3_main["se"]))
    for s in step:
        s.update(rho=an.RHO_BA, a=an.A_BA, rho_star=an.RHO_BA * (1 - an.A_BA * s["c"]),
                 se_rho_star=float(np.hypot((1 - an.A_BA * s["c"]) * an.RHO_BA_SE, an.RHO_BA * an.A_BA * s["se_c"])),
                 note="SE: delta method, rho and c independent")
    write(step, DERIVED / "monthly_corrected_step.csv")

    # Linkage and dedupe audit.
    for y in np.unique(yr[mon]):
        m = mon & (yr == y)
        for name, drop in (("monthly analysis rows dropped as a repeat person (CPSIDV)", ~keep_plain),
                           ("monthly analysis rows dropped as unlinkable MIS 5 records", keep_plain & unlinkable)):
            link_rows.append(dict(measure=name, year=int(y), base=int(m.sum()), hits=int((m & drop).sum()),
                                  share=float((m & drop).sum() / m.sum())))
    write(link_rows, DERIVED / "monthly_linkage.csv")
    audit.update(bootstrap_reps=B, seed=SEED, clusters=int(mult.shape[0]),
                 bootstrap="cluster = CPSID household (fallback source-year-month-SERIAL), stratum = first year; "
                           "clusters with analysis rows",
                 analysis_rows_monthly=int(mon.sum()), analysis_rows_asec=int(asec.sum()),
                 dedupe_rows_dropped_monthly=int((mon & ~keep_plain).sum()),
                 unlinkable_mis5_rows_dropped_monthly=int((keep_plain & unlinkable).sum()),
                 unlinkable_mis5_g3anc_nonmex_25plus=int((keep_plain & unlinkable & A["all:one"] & A["all:G3anc_nonmex"]
                                                         & (A["age"] >= 25)).sum()),
                 linking_break_mis1_months=[f"{t // 12}-{t % 12 + 1:02d}" for t in broken],
                 dedupe_rows_without_id_monthly=int((mon & (pid <= 0)).sum()),
                 dedupe_rows_dropped_g3anc_monthly=int((mon & ~keep_plain & A["all:G3anc"]).sum()),
                 union_asec_rows_added={"march_basic": int((add_a & ~over).sum()), "oversample": int((add_a & over).sum())},
                 union_asec_g3anc_nonmex_25plus_unmatched={
                     k: int((add_a & A["all:one"] & A["all:G3anc_nonmex"] & (A["age"] >= 25) & v).sum()) for k, v in {
                         "all": np.ones(len(yr), bool), "asec_oversample": over,
                         "march_basic_not_in_monthly_kept_households": ~over & ~np.isin(A["cpsidp"], kept_ids),
                         "march_basic_in_monthly_but_not_in_frame": ~over & np.isin(A["cpsidp"], kept_ids)}.items()},
                 asec_g3anc_nonmex_25plus_dedup={
                     k: int((keep_a & A["all:one"] & A["all:G3anc_nonmex"] & (A["age"] >= 25) & v).sum()) for k, v in {
                         "all": np.ones(len(yr), bool), "asec_oversample": over}.items()},
                 weights="monthly WTFINL; ASEC ASECWT, 2014 halved", duckdb_memory_limit=DUCK_MEMORY)
    (DERIVED / "monthly_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")

    pd.set_option("display.width", 250)
    print(pd.DataFrame(step).round(3).to_string(index=False))
    print(pd.DataFrame(gates).round(3).to_string(index=False))
    print(pd.DataFrame(tests).round(3).to_string(index=False))
    print(pd.DataFrame(c3).round(3).to_string(index=False))
    print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MiB")


if __name__ == "__main__":
    main()
