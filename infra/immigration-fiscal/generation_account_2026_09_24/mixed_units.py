"""Why the shared allocation moves the generations' costs: who lives in an SPM unit with people outside
the union. The shared rule splits every key equally over the unit's members
(cps_imputation_keys_2026_09_23/common.py unit_equal), so a mixed unit passes taxes and costs across the
union's boundary; under the personal rule nothing crosses it.
Per generation, convention (a), full person weight: members, minors' share, mean age, the share of
members in a unit with at least one person outside the union, and the mean share of their unit's
members outside it. Also where each generation's minors count under convention (b) (F.assignments).
Outputs: derived/mixed_units.csv, derived/minors_convention_b.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/mixed_units.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import frame as F  # noqa: E402


def main():
    d = F.load()
    civilian, union, gens = F.masks(d)
    w = d.pwwgt0.to_numpy(float)
    age = d.A_AGE.to_numpy(float)
    minor = age < 18
    unit = pd.factorize(d.SPM_ID, sort=True)[0]
    size = np.bincount(unit).astype(float)
    outside = (1 - np.bincount(unit, weights=union.astype(float)) / size)[unit]
    rows = []
    for g, m in [*gens.items(), ("union", union)]:
        for who, sel in [("all", m), ("minors", m & minor), ("adults", m & ~minor)]:
            ws = w[sel]
            rows.append(dict(generation=g, members=who, population=ws.sum(),
                             share_minors=(w[m & minor].sum() / w[m].sum()) if who == "all" else np.nan,
                             mean_age=(ws * age[sel]).sum() / ws.sum(),
                             share_in_mixed_unit=ws[outside[sel] > 0].sum() / ws.sum(),
                             mean_outside_share_of_unit=(ws * outside[sel]).sum() / ws.sum()))
    out = pd.DataFrame(rows)
    pops = out[(out.members == "all") & (out.generation != "union")].population.to_numpy()
    if abs(pops.sum() / out[(out.members == "all") & (out.generation == "union")].population.iloc[0] - 1) > 1e-12:
        sys.exit("✗ generations do not partition the union")
    out.to_csv(F.OUT / "mixed_units.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(out.round(3).to_string(index=False))

    omega_b = F.assignments(d, civilian, union, gens)[0]["b"]
    lab = F.label(gens, len(d))
    moves = pd.DataFrame([{"own_generation": g, "minors": w[sel].sum(),
                           **{f"counted_in_{h}": (w[sel] * omega_b[sel, k]).sum() for k, h in enumerate(F.GENS)}}
                          for j, g in enumerate(F.GENS) for sel in [union & (lab == j) & minor]])
    if not np.allclose(moves[[f"counted_in_{h}" for h in F.GENS]].sum(axis=1), moves.minors, rtol=1e-12):
        sys.exit("✗ convention (b) does not partition the minors")
    moves.to_csv(F.OUT / "minors_convention_b.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(moves.round(0).to_string(index=False))


if __name__ == "__main__":
    main()
