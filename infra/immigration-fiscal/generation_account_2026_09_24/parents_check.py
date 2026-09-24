"""How the CPS records parents' birthplaces for union members who do not live with their parents.

CPS TP77 (2019), Table 3-2.5 part 2, p. 123: the household roster asks, for every member, "What is
his/her mother's country of birth?" and "... father's country of birth?" (items MNTVT, FNTVT) in the
first month in sample and for members added later; the data dictionary gives PEMNTVTY/PEFNTVTY the
universe "All Persons". The answers are reported, not copied from a linked parent record. This script
measures, on the union: co-residence with a linked parent, the allocation rate of the two items with and
without a co-resident parent, and agreement between a member's reported parent birthplace and the linked
co-resident parent's own reported birthplace.
Output: derived/parent_birthplace_check.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/parents_check.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import frame as F


def main():
    d = F.load()
    civ, union, gens = F.masks(d)
    parents = F.parent_rows(d)
    w = d.pwwgt0.to_numpy(float)
    age = d.A_AGE.to_numpy()
    coresident = (parents >= 0).any(axis=1)
    allocated = (d.PXMNTVTY.to_numpy() != 0) | (d.PXFNTVTY.to_numpy() != 0)
    rows = []
    for g in F.GENS + ["union"]:
        m = union if g == "union" else gens[g]
        for band, a in [("under18", age < 18), ("18plus", age >= 18), ("all", np.ones(len(d), bool))]:
            base = m & a
            for status, s in [("parent_in_household", coresident), ("no_parent_in_household", ~coresident)]:
                use = base & s
                rows.append(dict(generation=g, age=band, coresidence=status, n=int(use.sum()),
                                 people=w[use].sum(), share_of_cell=w[use].sum() / w[base].sum(),
                                 parent_birthplace_allocated=w[use & allocated].sum() / w[use].sum()
                                 if use.any() else np.nan))
    # Agreement: a member's reported mother's (father's) birthplace against the linked co-resident
    # biological mother's (father's) own reported birthplace, both unallocated.
    sex = d.A_SEX.to_numpy()
    born = d.PENATVTY.to_numpy()
    for g in F.GENS + ["union"]:
        m = union if g == "union" else gens[g]
        agree = total = 0.0
        for slot in (0, 1):
            p = parents[:, slot]
            typ = d[f"PEPAR{slot + 1}TYP"].to_numpy()
            ok = m & (p >= 0) & (typ == 1)
            pp = np.where(ok, p, 0)
            for field, flag, parent_sex in [("PEMNTVTY", "PXMNTVTY", 2), ("PEFNTVTY", "PXFNTVTY", 1)]:
                use = ok & (sex[pp] == parent_sex) & (d[flag].to_numpy() == 0) & (d.PXNATVTY.to_numpy()[pp] == 0)
                total += w[use].sum()
                agree += w[use & (d[field].to_numpy() == born[pp])].sum()
        rows.append(dict(generation=g, age="all", coresidence="linked_biological_parent_agreement",
                         n=np.nan, people=total, share_of_cell=np.nan, parent_birthplace_allocated=np.nan,
                         agreement=agree / total))
    out = pd.DataFrame(rows)
    F.OUT.mkdir(exist_ok=True)
    out.to_csv(F.OUT / "parent_birthplace_check.csv", index=False, lineterminator="\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
