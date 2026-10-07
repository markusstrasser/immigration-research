"""Ladder 232's own frame, split by vintage proxies: Census CPS ASEC public files 2022-2025, adults 25-64.

The carry-over lane's cross-sectional step rho = gap(G3+) / gap(G2) (G2: a Mexico-born parent; G3+: US-born of
US-born parents reporting Mexican origin), each gap against third-plus non-Hispanic whites reweighted to the
group's age x sex cells, with the lane's partial ledger and mean worker earnings. Split here by birth cohort
(survey year minus age) and by state group (Texas + New Mexico, California, elsewhere; whites of the same state
group, and national whites), and cohort x state. Loaders, groups, ledger, cells and measures are
generation_carryover_2026_09_27/analyze_cps.py's, imported read-only; SEs are its 160 SDR replicates (4/160),
pooled at weight / 4 with a common replicate index.

Memory: the lane's build() holds four years of 161 replicate weights (3 GiB peak). Here each year is reduced to
weighted totals by (group, cohort band, state group, age x sex cell, replicate) and freed; every statistic is a
mean, so the totals carry it exactly (the median earnings measure is left out). Gate: the unsplit stratum
reproduces the carry-over lane's published pop gaps and SEs to a relative 1e-9.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/census_asec.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import gc
import importlib.util
import json
import resource
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
CARRY = FISCAL / "generation_carryover_2026_09_27"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


co = _load("carryover_cps", CARRY / "analyze_cps.py")
YEARS = [2022, 2023, 2024, 2025]
LABEL = "CPS_ASEC_2022_2025"
STATE = {48: 1, 35: 1, 6: 2}
STATE_NAME = {1: "TX_NM", 2: "CA", 0: "elsewhere"}
COHORTS = [(1958, 1969), (1970, 1979), (1980, 1989), (1990, 2000)]
HALVES = {"1958-1979": [0, 1], "1980-2000": [2, 3]}
GROUPS = ["white3plus", "G2", "G3plus_all"]
MEASURES = ["ba_plus", "less_than_hs", "employed", "earnings_worker_mean", "ledger_partial_per_adult"]
NCELL = 16  # co.age_cells "pop": 8 age bands x 2 sexes


def sdr(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def reduce_year(y: int, cpi: pd.Series, T: dict, counts: dict, ages: dict) -> dict:
    d = co.load_year(y)
    g, _, _ = co.groups(d)
    d["ledger_raw"] = co.ledger(d)
    f = cpi.loc[2024] / cpi.loc[y - 1]
    d["earn24"] = d.PEARNVAL * f
    d["ledger24"] = d.ledger_raw * f
    W = d[co.REPS].to_numpy(float) / len(YEARS)
    age, sex = d.A_AGE.to_numpy(), d.A_SEX.to_numpy()
    born = y - age
    coh = np.full(len(d), -1)
    for i, (a, b) in enumerate(COHORTS):
        coh[(born >= a) & (born <= b)] = i
    state = d.GESTFIPS.map(STATE).fillna(0).astype(int).to_numpy()
    frame = (age >= 25) & (age <= 64)
    if (frame & (coh < 0)).any():
        raise ValueError(f"{y}: birth year outside the cohort bands")
    cell = co.age_cells(age, sex, "pop")
    for m in MEASURES:
        fv, fvalid, kind, unit = co.MEASURES[m]
        if kind != "mean":
            raise ValueError(f"{m}: only means reduce to totals")
        x = fv(d).to_numpy(float)
        ok = frame & fvalid(d).to_numpy()
        for gname in GROUPS:
            use = ok & g[gname]
            for c in range(len(COHORTS)):
                for s in STATE_NAME:
                    idx = np.flatnonzero(use & (coh == c) & (state == s))
                    key = (gname, c, s, m)
                    tw, tx = T.setdefault(key, (np.zeros((NCELL, 161)), np.zeros((NCELL, 161))))
                    np.add.at(tw, cell[idx], W[idx])
                    np.add.at(tx, cell[idx], W[idx] * x[idx, None])
                    counts[key] = counts.get(key, 0) + len(idx)
                    a0 = ages.setdefault(key, [0.0, 0.0])
                    a0[0] += float((W[idx, 0] * age[idx]).sum())
                    a0[1] += float(W[idx, 0].sum())
    out = dict(source=str(co.SOURCES[y][0].relative_to(FISCAL.parents[1])), sha256=co.sha(co.SOURCES[y][0]),
               rows=len(d), income_year=y - 1, cpi_factor_to_2024=float(f))
    del d, W
    gc.collect()
    return out


def gap(G, R, scale):
    """Group mean minus the reference mean reweighted to the group's cells over covered cells: co.reweight's
    estimator on cell totals."""
    gw, gx, rw, rx = G[0], G[1], R[0], R[1]
    mg = gx.sum(0) / gw.sum(0)
    cov = rw > 0
    share = np.where(cov, gw / gw.sum(0), 0.0)
    mr = np.divide(rx, rw, out=np.zeros_like(rx), where=cov)
    unc = float(1 - share[:, 0][cov[:, 0]].sum())
    return (mg - (share * mr).sum(0) / share.sum(0)) * scale, unc


def strata():
    allc, alls = list(range(len(COHORTS))), list(STATE_NAME)
    out = [("all", "all", (allc, alls), (allc, alls))]
    out += [("cohort", f"{a}-{b}", ([i], alls), ([i], alls)) for i, (a, b) in enumerate(COHORTS)]
    for s, name in STATE_NAME.items():
        out.append(("state", name, (allc, [s]), (allc, [s])))
        out.append(("state_national_whites", name, (allc, [s]), (allc, alls)))
    for h, cs in HALVES.items():
        for s, name in STATE_NAME.items():
            out.append(("cohort_x_state", f"{h}|{name}", (cs, [s]), (cs, [s])))
    return out


def total(T, gname, sel, m):
    cs, ss = sel
    return tuple(sum(T[(gname, c, s, m)][k] for c in cs for s in ss) for k in (0, 1))


def main():
    DERIVED.mkdir(exist_ok=True)
    cpi = pd.read_csv(co.CPI)
    cpi = cpi.set_index(cpi.columns[0]).iloc[:, 0]
    T, counts, ages, audit = {}, {}, {}, {}
    for y in YEARS:
        audit[y] = reduce_year(y, cpi, T, counts, ages)
        print(f"  ✓ {y} reduced, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MiB",
              flush=True)
    gaps, rhos = [], []
    for split, label, gsel, rsel in strata():
        for m in MEASURES:
            scale = 100 if co.MEASURES[m][3] == "pct" else 1
            R = total(T, "white3plus", rsel, m)
            got, n = {}, {}
            for gname in ("G2", "G3plus_all"):
                G = total(T, gname, gsel, m)
                v, unc = gap(G, R, scale)
                got[gname] = v
                n[gname] = sum(counts[(gname, c, s, m)] for c in gsel[0] for s in gsel[1])
                aw = [sum(ages[(gname, c, s, m)][k] for c in gsel[0] for s in gsel[1]) for k in (0, 1)]
                gaps.append(dict(source=LABEL, split=split, stratum=label, measure=m, generation=gname, n=n[gname],
                                 n_ref=sum(counts[("white3plus", c, s, m)] for c in rsel[0] for s in rsel[1]),
                                 mean_age=aw[0] / aw[1], gap=float(v[0]), se=sdr(v), ref_cells_uncovered_share=unc))
            rho = got["G3plus_all"] / got["G2"]
            rhos.append(dict(source=LABEL, split=split, stratum=label, measure=m, gap_G2=float(got["G2"][0]),
                             se_G2=sdr(got["G2"]), gap_G3plus=float(got["G3plus_all"][0]),
                             se_G3plus=sdr(got["G3plus_all"]), rho=float(rho[0]), se=sdr(rho),
                             change_in_gap=float((got["G3plus_all"] - got["G2"])[0]),
                             se_change=sdr(got["G3plus_all"] - got["G2"]),
                             denominator_stable=bool(abs(got["G2"][0]) > 2 * sdr(got["G2"])),
                             n_G2=n["G2"], n_G3plus=n["G3plus_all"]))
    # Gate: the unsplit stratum is the carry-over lane's published pop frame.
    pub = pd.read_csv(CARRY / "derived" / f"cps_gaps_{LABEL}.csv")
    pub = pub[pub.frame.eq("pop")]
    checked = 0
    for r in gaps:
        if r["split"] != "all":
            continue
        b = pub[pub.measure.eq(r["measure"]) & pub.generation.eq(r["generation"])].iloc[0]
        if (abs(r["gap"] - b.gap) > 1e-9 * abs(b.gap) or abs(r["se"] - b.se) > 1e-9 * b.se or r["n"] != b.n):
            raise ValueError(f"[BLOCKED] gate: {r['measure']} {r['generation']}: {r['gap']} vs {b.gap}")
        checked += 1
    # Nine significant digits: summation order cannot move a rerun's bytes.
    for rows, name in ((gaps, "census_gaps.csv"), (rhos, "census_rho.csv")):
        rows = [{k: (float(f"{v:.9g}") if isinstance(v, float) else v) for k, v in r.items()} for r in rows]
        with open(DERIVED / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    (DERIVED / "census_audit.json").write_text(json.dumps(dict(
        gate_cells_checked=checked, years={str(k): v for k, v in audit.items()},
        pooling="replicate weights / 4, common replicate index; overlapping households in adjacent ASECs are "
                "person-years, as in the carry-over lane"), indent=1, sort_keys=True) + "\n")
    pd.set_option("display.width", 250)
    print(f"  ✓ gate: {checked} published cells reproduced")
    t = pd.DataFrame(rhos)
    print(t[["split", "stratum", "measure", "gap_G2", "gap_G3plus", "rho", "se", "n_G2", "n_G3plus"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
