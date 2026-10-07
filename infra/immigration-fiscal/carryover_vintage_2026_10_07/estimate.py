"""Gaps, carry-over ratios and bootstrap SEs from vintage.py's aggregates (IPUMS-CPS monthly and ASEC).

Cross-section (derived/xs_gaps.csv, xs_rho.csv, xs_contrasts.csv): rho = gap(G3+ identifiers) / gap(G2),
adults 25-64, whites of the same stratum reweighted to each group's `pop` age x sex cells. Strata: all; birth
cohort; state group (whites of the same group, and national whites); cohort x state; cohort x survey period;
the ladder's 2022-25 window (gate against the Census-file 0.921). Lagged ratios put G3+ of cohort c over G2
of cohort c-30.

Lineage (derived/lineage_gaps.csv, lineage_rho.csv): parent-child pairs, rho_lin = gap(children) /
gap(their parents), by parent birth cohort and state group; white pairs of the same stratum are the
reference on both sides (children on the co-resident `cores_one` cells, parents on 5-year bands x sex).

SEs: B = 500 multinomial draws of vintage.py's K random groups of household clusters (seed 20261007),
the same draws for every statistic, so differences between strata carry their covariance.

Run from the repository root (after vintage.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/estimate.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
spec = importlib.util.spec_from_file_location("vintage", HERE / "vintage.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

B = 500
SEED = 20261007
K = v.K
XS_MEASURES = {"monthly": ["ba", "rank", "lths", "yrs", "emp"], "asec": ["ba", "rank", "lths", "yrs", "emp", "earn"]}
LIN_MEASURES = ["ba", "rank", "lths", "yrs"]
UNIT = {**v.UNIT, "rank": "pctile"}
ECOLS = [f"w_e{i}" for i in range(len(v.EDUC_CODES))]
COH = v.COHORTS
PCOH = v.PCOHORTS
PER = v.PERIODS
NCELL_POP, NCELL_CORES, NCELL_PAR = 16, 38, 26  # co.age_cells "pop" (8 bands x sex), "cores_one", 13 parent bands x sex
LAG = 3  # cohort bands: 30 years, one generation


def multiplicities() -> np.ndarray:
    rng = np.random.Generator(np.random.PCG64(SEED))
    M = np.ones((K, B + 1))
    for b in range(1, B + 1):
        M[:, b] = np.bincount(rng.integers(0, K, K), minlength=K)
    return M


M = multiplicities()


def totals(a: pd.DataFrame, cols: list[str], ncell: int) -> dict:
    out = {}
    ci, bi = a.cell.to_numpy(), a.bucket.to_numpy()
    if len(a) and ci.max() >= ncell:
        raise ValueError("cell out of range")
    for c in cols:
        D = np.zeros((ncell, K))
        np.add.at(D, (ci, bi), a[c].to_numpy(float))
        out[c] = D @ M
    out["records"] = int(a.n.sum())
    return out


def gap(G, R, wcol, xcol, scale):
    """Group mean minus the reference mean reweighted to the group's cells over covered cells
    (g3_identity_pooled analyze_monthly.gap_reps on cell totals)."""
    gw, gx, rw, rx = G[wcol], G[xcol], R[wcol], R[xcol]
    with np.errstate(invalid="ignore", divide="ignore"):
        mg = gx.sum(0) / gw.sum(0)
        cov = rw > 0
        share = np.where(cov, gw / gw.sum(0), 0.0)
        mr = np.divide(rx, rw, out=np.zeros_like(rx), where=cov)
        ref = (share * mr).sum(0) / share.sum(0)
        uncovered = float(1 - share[:, 0][cov[:, 0]].sum()) if gw[:, 0].sum() > 0 else float("nan")
    return (mg - ref) * scale, uncovered


def rank_gap(G, R):
    """Mean percentile rank of the group's completed schooling in the white distribution, minus 50: whites are
    reweighted to the group's age x sex cells over covered cells, ties take the mid-rank. Scale-free across
    cohorts, unlike a BA+ gap in points, which grows when the white BA+ share rises."""
    Ge = np.stack([G[c] for c in ECOLS])  # [codes, cells, draws]
    Re = np.stack([R[c] for c in ECOLS])
    gw, rw = Ge.sum(0), Re.sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        cov = rw > 0
        share = np.where(cov, gw / gw.sum(0), 0.0)
        pr = np.divide(Re, rw, out=np.zeros_like(Re), where=cov)
        F = (share * pr).sum(1) / share.sum(0)  # [codes, draws]
        mid = np.cumsum(F, 0) - F / 2
        pg = Ge.sum(1) / gw.sum(0)
        return 100 * ((pg * mid).sum(0) - 0.5)


def measure_gap(G, R, m):
    if m == "rank":
        return rank_gap(G, R), gap(G, R, "w", "w_ba", 1)[1]
    return gap(G, R, "w_earnw" if m == "earn" else "w", f"w_{m}", 100 if UNIT[m] == "pct" else 1)


def sd(x):
    x = x[1:][np.isfinite(x[1:])]
    return float(np.std(x, ddof=1)) if len(x) > 1 else float("nan")


def pct(x, q):
    x = x[1:][np.isfinite(x[1:])]
    return float(np.percentile(x, q)) if len(x) else float("nan")


def r6(x):
    return float(f"{x:.6g}") if np.isfinite(x) else float("nan")


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def bname(i, edges):
    return v.band_name(i, edges)


def ratio_row(base: dict, num, den, extra: dict) -> dict:
    rho = num / den
    sa = sd(den)
    return {**base, "rho": r6(rho[0]), "se": r6(sd(rho)), "p05": r6(pct(rho, 5)), "p95": r6(pct(rho, 95)),
            "change_in_gap": r6((num - den)[0]), "se_change": r6(sd(num - den)),
            "denominator_stable": bool(abs(den[0]) > 2 * sa), **extra}


# ---------------------------------------------------------------- cross-section
def xs_strata():
    cohs = list(range(len(COH) - 1))
    out = [("all", "all", {}, "same")]
    out += [("period_2022_2025", "2022-2025", {"period": [2]}, "same")]
    out += [("cohort", bname(c, COH), {"coh": [c]}, "same") for c in cohs]
    out += [("state", v.STATE_NAME[s], {"state": [s]}, "same") for s in v.STATE_NAME]
    out += [("state_national_whites", v.STATE_NAME[s], {"state": [s]}, "national") for s in v.STATE_NAME]
    out += [("cohort_x_state", f"{bname(c, COH)}|{v.STATE_NAME[s]}", {"coh": [c], "state": [s]}, "same")
            for c in cohs for s in v.STATE_NAME]
    out += [("cohort_x_period", f"{bname(c, COH)}|{bname(p, PER)}", {"coh": [c], "period": [p]}, "same")
            for c in cohs for p in range(len(PER) - 1)]
    return out


def select(a: pd.DataFrame, filt: dict) -> np.ndarray:
    m = np.ones(len(a), bool)
    for k, vals in filt.items():
        m &= a[k].isin(vals).to_numpy()
    return m


def xs_run(src: str):
    a = pd.read_parquet(CACHE / f"agg_{src}_xs.parquet")
    ids = pd.read_parquet(CACHE / f"agg_{src}_ids.parquet")
    ids = ids[ids.frame.eq("xs")]
    cols = ["w", "wage", "w_ba", "w_lths", "w_yrs", "w_emp", "w_earnw", "w_earn"] + ECOLS
    measures = XS_MEASURES[src]
    gaps, rhos, reps, cache = [], [], {}, {}
    for split, label, filt, ref in xs_strata():
        sel = select(a, filt)
        rfilt = filt if ref == "same" else {k: x for k, x in filt.items() if k != "state"}
        rkey = json.dumps(rfilt, sort_keys=True)
        if rkey not in cache:
            cache[rkey] = totals(a[select(a, rfilt) & a.grp.eq(0).to_numpy()], cols, NCELL_POP)
        R = cache[rkey]
        if split == "all" and abs(rank_gap(R, R)[0]) > 1e-9:  # gate: whites against themselves rank at 50
            raise ValueError("rank gap of the reference against itself is not zero")
        G = {g: totals(a[sel & a.grp.eq(g).to_numpy()], cols, NCELL_POP) for g in (1, 2)}
        idm = select(ids, filt)
        for m in measures:
            wcol = "w_earnw" if m == "earn" else "w"
            got = {}
            for g in (1, 2):
                if G[g]["records"] == 0:
                    continue
                val, unc = measure_gap(G[g], R, m)
                got[g] = val
                reps[(src, split, label, ref, m, g)] = val
                gaps.append(dict(source=src, split=split, stratum=label, reference=ref, group=v.XS_GROUPS[g],
                                 measure=m, unit=UNIT[m], records=G[g]["records"],
                                 unique_persons=int(ids[idm & ids.grp.eq(g).to_numpy()].pid.nunique()),
                                 ref_records=R["records"], weighted=r6(G[g][wcol][:, 0].sum()),
                                 mean_age=r6(G[g]["wage"][:, 0].sum() / G[g]["w"][:, 0].sum()),
                                 gap=r6(val[0]), se=r6(sd(val)), ref_cells_uncovered_share=r6(unc)))
            if 1 in got and 2 in got:
                rhos.append(ratio_row(dict(source=src, split=split, stratum=label, reference=ref, measure=m,
                                           step="G2->G3+id", gap_from=r6(got[1][0]), se_from=r6(sd(got[1])),
                                           gap_to=r6(got[2][0]), se_to=r6(sd(got[2]))),
                                      got[2], got[1],
                                      dict(unique_G2=int(ids[idm & ids.grp.eq(1).to_numpy()].pid.nunique()),
                                           unique_G3plus=int(ids[idm & ids.grp.eq(2).to_numpy()].pid.nunique()))))
    # Lagged: G3+ of cohort band c over G2 of band c - LAG (30 years), each against its own cohort's whites.
    for c in range(LAG, len(COH) - 1):
        for m in measures:
            num = reps.get((src, "cohort", bname(c, COH), "same", m, 2))
            den = reps.get((src, "cohort", bname(c - LAG, COH), "same", m, 1))
            if num is None or den is None:
                continue
            rhos.append(ratio_row(dict(source=src, split="lagged_30y", stratum=f"G3+ {bname(c, COH)} / G2 {bname(c - LAG, COH)}",
                                       reference="same", measure=m, step="G2(c-30)->G3+id(c)", gap_from=r6(den[0]),
                                       se_from=r6(sd(den)), gap_to=r6(num[0]), se_to=r6(sd(num))),
                                  num, den, dict(unique_G2=-1, unique_G3plus=-1)))
    return gaps, rhos, reps


def xs_contrasts(reps, src):
    """Differences in rho between strata, on the same draws."""
    out = []
    rho = lambda split, label, m, ref="same": (reps[(src, split, label, ref, m, 2)] / reps[(src, split, label, ref, m, 1)]
                                               if (src, split, label, ref, m, 1) in reps else None)
    for m in XS_MEASURES[src]:
        pairs = [("cohort", bname(len(COH) - 2, COH), "cohort", bname(2, COH)),
                 ("cohort", bname(len(COH) - 3, COH), "cohort", bname(2, COH)),
                 ("cohort", bname(len(COH) - 2, COH), "all", "all"),
                 ("state", "TX_NM", "state", "CA"), ("state", "TX_NM", "state", "elsewhere"),
                 ("state", "CA", "all", "all")]
        for s1, l1, s2, l2 in pairs:
            a, b = rho(s1, l1, m), rho(s2, l2, m)
            if a is None or b is None:
                continue
            dlt = a - b
            out.append(dict(source=src, measure=m, a=f"{s1}:{l1}", b=f"{s2}:{l2}", rho_a=r6(a[0]), rho_b=r6(b[0]),
                            diff=r6(dlt[0]), se=r6(sd(dlt)), z=r6(dlt[0] / sd(dlt))))
    return out


# ---------------------------------------------------------------- lineage
STEPS = {1: ("g1g2", 0), 2: ("g2g3", 0), 3: ("g3g4", 4)}


def lin_strata():
    pcs = list(range(len(PCOH) - 1))
    out = [("all", "all", {})]
    out += [("parent_cohort", bname(p, PCOH), {"pcoh": [p]}) for p in pcs]
    out += [("state", v.STATE_NAME[s], {"state": [s]}) for s in v.STATE_NAME]
    out += [("parent_cohort_x_state", f"{bname(p, PCOH)}|{v.STATE_NAME[s]}", {"pcoh": [p], "state": [s]})
            for p in pcs for s in v.STATE_NAME]
    # Coarser vintage split for the state cut: parents born before 1955 and from 1955 on.
    return out


def lin_run(src: str):
    lc = pd.read_parquet(CACHE / f"agg_{src}_lc.parquet")
    lp = pd.read_parquet(CACHE / f"agg_{src}_lp.parquet")
    ids = pd.read_parquet(CACHE / f"agg_{src}_ids.parquet")
    ids = ids[ids.frame.eq("lin")]
    cols = ["w", "wage", "w_ba", "w_lths", "w_yrs"] + ECOLS
    gaps, rhos, shares, reps = [], [], [], {}
    for split, label, filt in lin_strata():
        for t, (step, rt) in STEPS.items():
            selc, selp = select(lc, filt), select(lp, filt)
            Rc = totals(lc[selc & lc.type.eq(rt).to_numpy()], cols, NCELL_CORES)
            Rp = totals(lp[selp & lp.type.eq(rt).to_numpy()], cols, NCELL_PAR)
            for ident, cids in (("lineage", [0, 1]), ("identifiers", [1])):
                gc = selc & lc.type.eq(t).to_numpy() & lc.cid.isin(cids).to_numpy()
                gp = selp & lp.type.eq(t).to_numpy() & lp.cid.isin(cids).to_numpy()
                Gc, Gp = totals(lc[gc], cols, NCELL_CORES), totals(lp[gp], cols, NCELL_PAR)
                if Gc["records"] < 2:
                    continue
                im = select(ids, filt) & ids.type.eq(t).to_numpy() & ids.cid.isin(cids).to_numpy()
                uniq = int(ids[im].pid.nunique())
                for m in LIN_MEASURES:
                    ch, uc = measure_gap(Gc, Rc, m)
                    pa, up = measure_gap(Gp, Rp, m)
                    reps[(src, split, label, step, ident, m)] = (pa, ch)
                    base = dict(source=src, split=split, stratum=label, step=step, children=ident, measure=m)
                    for side, val, G, R, unc in (("parent", pa, Gp, Rp, up), ("child", ch, Gc, Rc, uc)):
                        gaps.append(dict(**base, side=side, records=G["records"], unique_children=uniq,
                                         ref_records=R["records"],
                                         mean_age=r6(G["wage"][:, 0].sum() / G["w"][:, 0].sum()),
                                         gap=r6(val[0]), se=r6(sd(val)), ref_cells_uncovered_share=r6(unc)))
                    rhos.append(ratio_row(dict(**base, gap_parent=r6(pa[0]), se_parent=r6(sd(pa)),
                                               gap_child=r6(ch[0]), se_child=r6(sd(ch))),
                                          ch, pa, dict(records=Gc["records"], unique_children=uniq)))
            # Share of the step's children who do not report Mexican origin (weighted).
            gall = totals(lc[selc & lc.type.eq(t).to_numpy()], ["w"], NCELL_CORES)
            gnon = totals(lc[selc & lc.type.eq(t).to_numpy() & lc.cid.eq(0).to_numpy()], ["w"], NCELL_CORES)
            if gall["records"]:
                sh = gnon["w"].sum(0) / gall["w"].sum(0)
                shares.append(dict(source=src, split=split, stratum=label, step=step, records=gall["records"],
                                   records_not_mexican=gnon["records"], share_not_mexican=r6(sh[0]), se=r6(sd(sh))))
    return gaps, rhos, shares, reps


def lin_contrasts(reps, src):
    out = []
    pcs = [bname(p, PCOH) for p in range(len(PCOH) - 1)]
    for step in ("g1g2", "g2g3", "g3g4"):
        for ident in ("lineage", "identifiers"):
            for m in LIN_MEASURES:
                for a, b in ((pcs[-1], pcs[0]), (pcs[-1], pcs[1]), (pcs[-2], pcs[0]), (pcs[-1], "all")):
                    sa = "all" if a == "all" else "parent_cohort"
                    sb = "all" if b == "all" else "parent_cohort"
                    ka, kb = (src, sa, a, step, ident, m), (src, sb, b, step, ident, m)
                    if ka not in reps or kb not in reps:
                        continue
                    ra = reps[ka][1] / reps[ka][0]
                    rb = reps[kb][1] / reps[kb][0]
                    dlt = ra - rb
                    out.append(dict(source=src, step=step, children=ident, measure=m, a=a, b=b, rho_a=r6(ra[0]),
                                    rho_b=r6(rb[0]), diff=r6(dlt[0]), se=r6(sd(dlt)), z=r6(dlt[0] / sd(dlt))))
                for a, b in (("TX_NM", "CA"), ("TX_NM", "elsewhere")):
                    ka, kb = (src, "state", a, step, ident, m), (src, "state", b, step, ident, m)
                    if ka not in reps or kb not in reps:
                        continue
                    ra, rb = reps[ka][1] / reps[ka][0], reps[kb][1] / reps[kb][0]
                    dlt = ra - rb
                    out.append(dict(source=src, step=step, children=ident, measure=m, a=a, b=b, rho_a=r6(ra[0]),
                                    rho_b=r6(rb[0]), diff=r6(dlt[0]), se=r6(sd(dlt)), z=r6(dlt[0] / sd(dlt))))
    return out


def main():
    xg, xr, xc, lg, lr, ls, lcn = [], [], [], [], [], [], []
    for src in ("monthly", "asec"):
        g, r, reps = xs_run(src)
        xg += g
        xr += r
        xc += xs_contrasts(reps, src)
        g, r, s, reps = lin_run(src)
        lg += g
        lr += r
        ls += s
        lcn += lin_contrasts(reps, src)
        print(f"  ✓ {src}", flush=True)
    write(xg, DERIVED / "xs_gaps.csv")
    write(xr, DERIVED / "xs_rho.csv")
    write(xc, DERIVED / "xs_contrasts.csv")
    write(lg, DERIVED / "lineage_gaps.csv")
    write(lr, DERIVED / "lineage_rho.csv")
    write(ls, DERIVED / "lineage_identity_shares.csv")
    write(lcn, DERIVED / "lineage_contrasts.csv")
    pd.set_option("display.width", 250)
    t = pd.DataFrame(xr)
    print(t[t.measure.eq("ba") & t.split.isin(["all", "period_2022_2025", "cohort", "state", "lagged_30y"])]
          [["source", "split", "stratum", "gap_from", "gap_to", "rho", "se", "unique_G2", "unique_G3plus"]].to_string(index=False))
    t = pd.DataFrame(lr)
    print(t[t.measure.eq("ba") & t.split.isin(["all", "parent_cohort", "state"])]
          [["source", "split", "stratum", "step", "children", "gap_parent", "gap_child", "rho", "se", "unique_children"]].to_string(index=False))


if __name__ == "__main__":
    main()
