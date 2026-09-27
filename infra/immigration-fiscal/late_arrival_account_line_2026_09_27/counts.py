"""Task 1: the late-arrival subgroup's weighted count in the account's CPS ASEC 2025 frame, under the three
age-at-arrival readings, with replicate standard errors (161 weights: full sample + 160 replicates, SE =
sqrt(4/160 * sum (theta_r - theta)^2), the Census Bureau's successive-difference formula for the ASEC).

Output: derived/counts.csv (reading, cell, persons, se, n_unweighted, share of Mexico-born 65+).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/late_arrival_account_line_2026_09_27/counts.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402

import numpy as np  # noqa: E402

import frame as F  # noqa: E402


def main():
    d = F.load()
    civ, union, gens = F.masks(d)
    g1 = F.g1(gens)
    W = d[F.REPS].to_numpy(float)
    age = d.A_AGE.to_numpy()
    rows = []
    for reading in ("central", "lower", "upper"):
        cells = F.g1_cells(d, g1, reading)
        late50 = cells["G1_L50_50_64"] | cells["G1_L50_65p"] | cells["G1_L55_55_64"] | cells["G1_L55_65p"]
        late55 = cells["G1_L55_55_64"] | cells["G1_L55_65p"]
        young = cells["G1_Y_u50"] | cells["G1_Y_50_64"] | cells["G1_Y_65p"]
        groups = {**cells, "G1": g1, "G1_65p": g1 & (age >= 65), "G1_50p": g1 & (age >= 50),
                  "late50": late50, "late50_65p": late50 & (age >= 65), "late55": late55,
                  "late55_65p": late55 & (age >= 65), "young_50p": young & (age >= 50), "young_65p": young & (age >= 65)}
        base = W[g1 & (age >= 65)].sum(axis=0)
        for name, m in groups.items():
            t = W[m].sum(axis=0)
            se = float(np.sqrt(4 / 160 * ((t[1:] - t[0]) ** 2).sum()))
            sh = t / base
            sse = float(np.sqrt(4 / 160 * ((sh[1:] - sh[0]) ** 2).sum()))
            rows.append(dict(reading=reading, cell=name, persons=round(float(t[0]), 1), se=round(se, 1),
                             n_unweighted=int(m.sum()), share_of_g1_65p=round(float(sh[0]), 6), share_se=round(sse, 6)))
    F.HERE.joinpath("derived").mkdir(exist_ok=True)
    with (F.HERE / "derived/counts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
