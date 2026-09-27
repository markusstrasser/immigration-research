#!/usr/bin/env python3
"""Task 4: G2 -> G3 carry-over across ancestry origins in the GSS 1977-2024 cumulative file.

Generations from BORN, PARBORN and GRANBORN (Borjas 1994's GSS design):
  G1  BORN = 2
  G2  BORN = 1 and PARBORN in (1, 2, 8)          at least one parent born abroad
  G3  BORN = 1, PARBORN = 0, GRANBORN in 1..4    US-born parents, >= 1 grandparent born abroad
  G4+ BORN = 1, PARBORN = 0, GRANBORN = 0
Origin is ETHNIC, the respondent's country of family origin (the one felt closest to when
several). A G3 respondent's ETHNIC need not be the foreign-born grandparent's country; the
GRANBORN >= 2 arm tightens that.

Each adult 25-64 is placed in the education-years (EDUC) and real-income (REALRINC, positive
only) distribution of the reference: white, both parents US-born, non-Hispanic where HISPANIC
was asked (2000+) and not of Mexican, Puerto Rican or other Spanish ETHNIC before that; cells are
survey year x ten-year age band; weights WTSSPS. The same mid-rank percentile as cps_curve.py.

Run: uv run --no-project --with pyreadstat python3 \
       infra/immigration-fiscal/selection_curve_2026_09_27/gss_g3.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
from cps_curve import midrank_pct, wmean_se, wls  # noqa: E402

REPO = LANE.parents[2]
SRC = REPO / "infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta"
SRC_SHA = "a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344"
COLS = ["year", "age", "sex", "race", "hispanic", "born", "parborn", "granborn", "ethnic", "educ",
        "realrinc", "wtssps"]
SEED = 20260927
NBOOT = 2000
MIN_G2, MIN_G3 = 30, 40
# ETHNIC codes that are not an immigrant origin (or not one country) are excluded as origins.
NOT_ORIGIN = {1, 22, 29, 30, 38, 39, 40, 41, 97, 28, 299, 499, 599, 699, 799, 899, 999}
HISPANIC_ETHNIC = {17, 22, 38}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main() -> int:
    import pyreadstat
    if sha256(SRC) != SRC_SHA:
        raise SystemExit("[BLOCKED] GSS file hash changed")
    d, meta = pyreadstat.read_dta(str(SRC), usecols=COLS, encoding="latin1")
    lab = meta.variable_value_labels["ethnic"]
    for c in COLS:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d.age >= 25) & (d.age <= 64) & d.wtssps.notna() & d.born.isin([1, 2])].copy()
    d["band"] = ((d.age - 25) // 10).astype(int)
    d["gen"] = np.select(
        [d.born == 2, (d.born == 1) & d.parborn.isin([1, 2, 8]),
         (d.born == 1) & (d.parborn == 0) & d.granborn.between(1, 4),
         (d.born == 1) & (d.parborn == 0) & (d.granborn == 0)], [1, 2, 3, 4], 0)
    nonhisp = np.where(d.hispanic.notna(), d.hispanic == 1, ~d.ethnic.isin(HISPANIC_ETHNIC))
    d["ref"] = (d.race == 1) & (d.born == 1) & (d.parborn == 0) & nonhisp
    d["w"] = d.wtssps

    for var, out, ok in (("educ", "p_edu", d.educ.between(0, 20)),
                         ("realrinc", "p_inc", d.realrinc > 0)):
        pct = np.full(len(d), np.nan)
        for _, g in d.groupby(["year", "band"]):
            idx = g.index[ok.loc[g.index].to_numpy()]
            r = idx[d.loc[idx, "ref"].to_numpy()]
            if len(r) < 20:
                continue
            pct[d.index.get_indexer(idx)] = midrank_pct(d.loc[r, var].to_numpy(float),
                                                        d.loc[r, "w"].to_numpy(float),
                                                        d.loc[idx, var].to_numpy(float))
        d[out] = pct

    ref = d.ref.to_numpy()
    ref_share = d.loc[ref].groupby("band").w.sum() / d.loc[ref].w.sum()

    def gmean(mask, var):
        mm = mask & np.isfinite(d[var].to_numpy())
        if mm.sum() < 10:
            return np.nan, np.nan, int(mm.sum())
        sub = d.loc[mm]
        share = sub.groupby("band").w.sum() / sub.w.sum()
        ws = sub.w.to_numpy() * np.nan_to_num((ref_share / share).reindex(sub.band).to_numpy())
        m, se = wmean_se(sub[var].to_numpy(), ws)
        return m, se, int(mm.sum())

    rows = []
    for arm, g3mask in (("granborn_1plus", d.gen == 3), ("granborn_2plus", (d.gen == 3) & (d.granborn >= 2))):
        for e in sorted(d.ethnic.dropna().unique()):
            if int(e) in NOT_ORIGIN:
                continue
            em = (d.ethnic == e).to_numpy()
            row = {"arm": arm, "ethnic": int(e), "origin": lab.get(int(e), str(e))}
            for gname, gm in (("g1", d.gen == 1), ("g2", d.gen == 2), ("g3", g3mask), ("g4", d.gen == 4)):
                for var in ("p_edu", "p_inc"):
                    m, se, n = gmean(em & gm.to_numpy(), var)
                    row[f"{gname}_{var}"], row[f"{gname}_{var}_se"], row[f"n_{gname}_{var}"] = m, se, n
            rows.append(row)
    tab = pd.DataFrame(rows)
    tab.to_csv(LANE / "derived" / "gss_origin_generations.csv", index=False, float_format="%.6g",
               lineterminator="\n")

    rng = np.random.default_rng(SEED)
    out = []
    for arm in ("granborn_1plus", "granborn_2plus"):
        t0 = tab[tab.arm == arm]
        for var in ("p_edu", "p_inc"):
            for x, y, nx, ny in (("g2", "g3", MIN_G2, MIN_G3), ("g1", "g2", MIN_G2, MIN_G2),
                                 ("g1", "g3", MIN_G2, MIN_G3), ("g3", "g4", MIN_G3, MIN_G3)):
                if arm == "granborn_2plus" and "g3" not in (x, y):
                    continue
                t = t0[(t0[f"n_{x}_{var}"] >= nx) & (t0[f"n_{y}_{var}"] >= ny)].dropna(
                    subset=[f"{x}_{var}", f"{y}_{var}"])
                if len(t) < 5:
                    continue
                xv, yv = t[f"{x}_{var}"].to_numpy(), t[f"{y}_{var}"].to_numpy()
                sx, sy = t[f"{x}_{var}_se"].to_numpy(), t[f"{y}_{var}_se"].to_numpy()
                w = t[f"n_{y}_{var}"].to_numpy(float)
                b = wls(xv, yv, w)
                draws = []
                for _ in range(NBOOT):
                    i = rng.integers(0, len(t), len(t))
                    draws.append(wls(xv[i], yv[i], w[i]))
                draws = np.array(draws)
                vx = np.average((xv - np.average(xv, weights=w)) ** 2, weights=w)
                rel = 1 - np.average(sx ** 2, weights=w) / vx
                excl_mex = t[t.ethnic != 17]
                b_nomex = wls(excl_mex[f"{x}_{var}"].to_numpy(), excl_mex[f"{y}_{var}"].to_numpy(),
                              excl_mex[f"n_{y}_{var}"].to_numpy(float))
                out.append({"source": "GSS 1977-2024", "arm": arm, "outcome": var,
                            "link": f"{x}->{y}", "n_origins": len(t),
                            "origins": ";".join(t.origin), "slope": b[1],
                            "slope_lo": float(np.percentile(draws[:, 1], 2.5)),
                            "slope_hi": float(np.percentile(draws[:, 1], 97.5)),
                            "intercept": b[0], "x_reliability": rel,
                            "slope_disattenuated": b[1] / rel if rel > 0 else np.nan,
                            "slope_without_mexico": b_nomex[1]})
    with open(LANE / "derived" / "gss_slopes.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(out[0]), lineterminator="\n")
        wr.writeheader()
        for r in out:
            wr.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    ref_mean = {v: float(np.average(d.loc[ref & d[v].notna().to_numpy(), v],
                                    weights=d.loc[ref & d[v].notna().to_numpy(), "w"]))
                for v in ("p_edu", "p_inc")}
    (LANE / "derived" / "gss_audit.json").write_text(json.dumps(
        {"sha256": SRC_SHA, "n_adults_25_64": int(len(d)),
         "n_by_gen": {int(k): int(v) for k, v in d.gen.value_counts().items()},
         "reference_mean_pct": ref_mean}, indent=2) + "\n")
    for r in out:
        print(f"{r['arm']:<15} {r['outcome']:<6} {r['link']:<7} k={r['n_origins']:<3} slope {r['slope']:.3f} "
              f"[{r['slope_lo']:.3f}, {r['slope_hi']:.3f}] int {r['intercept']:.1f} rel {r['x_reliability']:.2f} "
              f"no-Mex {r['slope_without_mexico']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
