"""Step 6 test: do imputed annual wages fit the same person's basic-CPS weekly earnings?

Supplement nonrespondents (FL_665 != 1) have their whole ASEC income record imputed, but most of
them answered the March basic interview, and those in the outgoing rotation groups reported usual
weekly earnings there. The 2025 ASEC public file blanks its copy of that item (A_GRSWK is nonzero
for 45 of 15,207 earnings-eligible records), so this script links the March 2025 basic monthly
public file: the dictionary's rule is "Concatenate HRHHID and HRHHID2 on the non-ASEC file to match
to H_IDNUM on the ASEC file", plus PULINENO for persons, which gives PERIDNUM
[SOURCE: _cache/cpsmar25.txt, "Matching Housing Units"]. Neither this lane's hot deck nor its
reweighting uses weekly earnings, so the test is outside both corrections.

Outcome y = ln(WSAL_VAL) - ln(weekly): annual wage and salary income over usual weekly earnings
(PTERNWA / 100). For each group g (union, other residents) and imputation status s (reported;
whole supplement; item-level imputed), the gap is mean y(g, s) - mean y(g, reported). If the
Census imputation treats union members like other residents, the union's gap equals other
residents' gap. DiD = gap(union) - gap(other) is the union-specific drift of imputed annual wages
relative to the person's own weekly earnings, in log points. "cell" versions take the gaps within
sex x age (6) x education (4) cells, weighted by the union's imputed weight.

The same statistics are computed on this lane's re-imputed frames (union-matched hot deck and
pooled-donor control, main specification, 5 seeds each). If the union-matched hot deck removes the
drift, its DiD falls toward zero while the control keeps it.

Universe: civilians 16+ linked to the March basic file, PRERELG = 1 (earnings eligible),
PRWERNAL = 0 (weekly earnings reported, not allocated), PTWK = 0 (not top-coded), weekly > 0, and
WSAL_VAL > 0 in the frame evaluated. Weights: ASEC person weight; SEs from the 160 ASEC replicates.
Output: derived/weekly_validation.csv, derived/weekly_validation_counts.csv.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/cps_imputation_keys_2026_09_23/validate_weekly.py
"""
from __future__ import annotations

import hashlib
import subprocess
import zipfile

import numpy as np
import pandas as pd

import common as c
import hotdeck

SEEDS = [20260923 + i for i in range(5)]
BASIC = c.CACHE / "basic/mar25pub.csv"
BASIC_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/mar25pub.csv"
BASIC_SHA = "c7ad5dad0e4955a73494eebce7a8379a7ae8ffe9c7869e7d29088394208418e2"
BASIC_COLS = ["hrhhid", "hrhhid2", "PULINENO", "HRMIS", "prerelg", "prwernal", "pternwa", "ptwk", "prtage", "pesex"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def attach_weekly(d):
    if not BASIC.exists():
        BASIC.parent.mkdir(parents=True, exist_ok=True)
        print(f"[weekly] fetching {BASIC_URL}", flush=True)
        subprocess.run(["curl", "-sS", "-o", str(BASIC), BASIC_URL], check=True)
    if sha256(BASIC) != BASIC_SHA:
        raise SystemExit("[BLOCKED] March 2025 basic file changed")
    b = pd.read_csv(BASIC, usecols=BASIC_COLS, dtype={"hrhhid": str, "hrhhid2": str}).dropna(subset=["PULINENO"])
    b["PERIDNUM"] = b.hrhhid.str.zfill(15) + b.hrhhid2.str.zfill(5) + b.PULINENO.astype(int).map("{:02d}".format)
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        ids = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "PERIDNUM"], dtype={"PERIDNUM": str})
    ids = ids.merge(b.drop(columns=["hrhhid", "hrhhid2", "PULINENO"]), on="PERIDNUM", how="left", validate="one_to_one")
    out = d.merge(ids, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    linked = out.prtage.notna()
    agree = (out.A_SEX[linked] == out.pesex[linked]).mean(), ((out.A_AGE - out.prtage).abs()[linked] <= 1).mean()
    print(f"[weekly] linked {int(linked.sum())} of {len(out)} ASEC persons; sex agrees {agree[0]:.4f}, "
          f"age within 1 year {agree[1]:.4f}", flush=True)
    if agree[0] < 0.99 or agree[1] < 0.99:
        raise SystemExit("[BLOCKED] ASEC-basic link disagrees on sex or age")
    out["weekly"] = out.pternwa / 100
    return out


def stats(frame, base, civ, union, W, cells):
    """Gaps and DiD (raw and within cells) under all 161 weights."""
    wage = frame.WSAL_VAL.to_numpy(float)
    weekly = base.weekly.fillna(0).to_numpy(float)
    universe = (civ & base.A_AGE.ge(16).to_numpy() & base.prerelg.eq(1).to_numpy()
                & base.prwernal.eq(0).to_numpy() & base.ptwk.eq(0).to_numpy() & (weekly > 0) & (wage > 0))
    y = np.zeros(len(frame))
    y[universe] = np.log(wage[universe]) - np.log(weekly[universe])
    full = base.FL_665.ne(1).to_numpy()
    imputed = c.person_status(base)["wage"]
    status = {"reported": ~imputed & ~full, "whole_supplement": full, "item_imputed": imputed & ~full}
    groups = {"union": union, "other": civ & ~union}
    rows, reps = [], {}
    for g, gm in groups.items():
        for s, sm in status.items():
            m = universe & gm & sm
            wsum = W[m].sum(axis=0)
            reps[(g, s)] = (W[m] * y[m, None]).sum(axis=0) / wsum
            rows.append(dict(group=g, status=s, n=int(m.sum()), weighted_m=float(wsum[0]) / 1e6,
                             mean_y=float(reps[(g, s)][0])))
    ncell = cells.max() + 1
    out = {}
    for s in ["whole_supplement", "item_imputed"]:
        gu = reps[("union", s)] - reps[("union", "reported")]
        go = reps[("other", s)] - reps[("other", "reported")]
        out[(s, "raw")] = (gu, go, gu - go, 1.0)
        sums = {}
        for g, gm in groups.items():
            for st in [s, "reported"]:
                m = universe & gm & status[st]
                num = np.stack([np.bincount(cells[m], weights=W[m, r] * y[m], minlength=ncell)
                                for r in range(W.shape[1])], axis=1).astype(float)
                den = np.stack([np.bincount(cells[m], weights=W[m, r], minlength=ncell)
                                for r in range(W.shape[1])], axis=1).astype(float)
                sums[(g, st)] = (num, den)
        usable = np.all([v[1][:, 0] > 0 for v in sums.values()], axis=0)
        wt = sums[("union", s)][1] * usable[:, None]
        mean = {k: np.divide(v[0], v[1], out=np.zeros_like(v[0]), where=v[1] > 0) for k, v in sums.items()}
        cu = ((mean[("union", s)] - mean[("union", "reported")]) * wt).sum(axis=0) / wt.sum(axis=0)
        co = ((mean[("other", s)] - mean[("other", "reported")]) * wt).sum(axis=0) / wt.sum(axis=0)
        coverage = wt[:, 0].sum() / sums[("union", s)][1][:, 0].sum()
        out[(s, "cell")] = (cu, co, cu - co, coverage)
    return rows, out


def main():
    d = attach_weekly(c.load_frame())
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    cells = c.cell_codes(c.cell_vars(d), ["sex", "age6", "edu4"])
    frames = [("published", None, d)]
    for seed in SEEDS:
        for variant, base_cells in [("hotdeck_union_matched", hotdeck.BASE), ("hotdeck_pooled_control", [])]:
            print(f"[weekly] hot deck seed {seed} {variant}", flush=True)
            new, _ = hotdeck.run(d, seed=seed, verbose=False, base=base_cells)
            frames.append((variant, seed, new))
    counts, results = None, []
    for name, seed, frame in frames:
        rows, out = stats(frame, d, civ, union, W, cells)
        if name == "published":
            counts = pd.DataFrame(rows)
        for (s, kind), (gu, go, did, coverage) in out.items():
            results.append(dict(frame=name, seed=seed, status=s, kind=kind, union_gap=float(gu[0]),
                                union_gap_se=c.sdr(gu), other_gap=float(go[0]), other_gap_se=c.sdr(go),
                                did=float(did[0]), did_se=c.sdr(did), cell_coverage=float(coverage)))
    res = pd.DataFrame(results)
    summary = (res.groupby(["frame", "status", "kind"], sort=False)
               .agg(seeds=("did", "size"), union_gap=("union_gap", "mean"), union_gap_se=("union_gap_se", "mean"),
                    other_gap=("other_gap", "mean"), other_gap_se=("other_gap_se", "mean"), did=("did", "mean"),
                    did_se=("did_se", "mean"), did_seed_sd=("did", "std"), cell_coverage=("cell_coverage", "mean"))
               .reset_index())
    counts.to_csv(c.OUT / "weekly_validation_counts.csv", index=False)
    summary.to_csv(c.OUT / "weekly_validation.csv", index=False)
    print(counts.round(4).to_string(index=False), flush=True)
    print(summary.round(4).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
