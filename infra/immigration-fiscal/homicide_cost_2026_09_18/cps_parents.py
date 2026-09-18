"""Own minor children in the household, by adult age x sex x group, CPS ASEC 2025.

Uses the ledger's own group masks (extend_ledger.build, lines 228-239) reconstructed
from the public-use person file, and the basic-CPS parent pointers PEPAR1/PEPAR2 to
link every child under 18 to the one or two parents present in the same household.
Writes derived/cps_parent_channel.csv and derived/cps_parent_channel_by_age.csv.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ZIP = ROOT / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

COLS = ["PH_SEQ", "A_LINENO", "A_AGE", "A_SEX", "MARSUPWT", "PRCITSHP", "PEFNTVTY",
        "PEMNTVTY", "PENATVTY", "PEHSPNON", "PRDTRACE", "PRDTHSP", "PEPAR1", "PEPAR2",
        "PRPERTYP"]
US_AREA = [57, 60, 66, 69, 73, 78]
BANDS = [(18, 25), (25, 35), (35, 45), (45, 55), (55, 65), (65, 75), (75, 200)]


def groups(d: pd.DataFrame) -> dict:
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    g = {
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)),
        "mexico_born": (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)),
        "mexican_second_gen": (native & parent_mexico),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)),
        "all_hispanic": d.PEHSPNON.eq(1),
        "all_native": native,
    }
    g["mexican_observed_total"] = (g["mexico_born"] | g["mexican_second_gen"]
                                   | g["mexican_third_plus_selfid"])
    return {k: v.to_numpy() for k, v in g.items()}


def main() -> None:
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS, low_memory=False)
    d["w"] = d.MARSUPWT / 100.0
    print(f"[cps] person records {len(d):,}, weighted {d.w.sum()/1e6:.1f}m")

    kids = d[d.A_AGE.lt(18)].copy()
    edges = []
    for col in ["PEPAR1", "PEPAR2"]:
        e = kids[kids[col].gt(0)][["PH_SEQ", col, "A_AGE", "w"]].rename(
            columns={col: "parent_pos", "A_AGE": "child_age"})
        e["n_parents_in_hh"] = 0
        edges.append(e)
    edges = pd.concat(edges, ignore_index=True)
    # how many of the child's parents are present, per child
    nparents = (kids.PEPAR1.gt(0).astype(int) + kids.PEPAR2.gt(0).astype(int))
    kids = kids.assign(n_par=nparents.to_numpy())
    key = kids.set_index(["PH_SEQ", "A_LINENO"]).n_par
    print("[cps] children under 18:", f"{kids.w.sum()/1e6:.1f}m weighted; "
          f"with 2 resident parents {kids.loc[kids.n_par.eq(2), 'w'].sum()/kids.w.sum():.3f}, "
          f"1 parent {kids.loc[kids.n_par.eq(1), 'w'].sum()/kids.w.sum():.3f}, "
          f"0 {kids.loc[kids.n_par.eq(0), 'w'].sum()/kids.w.sum():.3f}")

    # child-side attributes carried to the parent
    ce = []
    for col in ["PEPAR1", "PEPAR2"]:
        sub = kids[kids[col].gt(0)]
        ce.append(pd.DataFrame({"PH_SEQ": sub.PH_SEQ.to_numpy(),
                                "parent_pos": sub[col].to_numpy(),
                                "child_age": sub.A_AGE.to_numpy(),
                                "child_n_par": sub.n_par.to_numpy()}))
    ce = pd.concat(ce, ignore_index=True)
    ce["years_to_18"] = 18 - ce.child_age
    ce["years_to_16"] = np.clip(16 - ce.child_age, 0, None)
    ce["sole_parent"] = (ce.child_n_par == 1).astype(float)
    agg = ce.groupby(["PH_SEQ", "parent_pos"]).agg(
        n_kids=("child_age", "size"),
        child_years=("years_to_18", "sum"),
        max_years_to_16=("years_to_16", "max"),
        mean_child_age=("child_age", "mean"),
        sole_kids=("sole_parent", "sum"),
        sole_child_years=("years_to_18", lambda s: 0.0),
    )
    sole_cy = ce.assign(cy=ce.years_to_18 * ce.sole_parent).groupby(
        ["PH_SEQ", "parent_pos"]).cy.sum()
    agg["sole_child_years"] = sole_cy
    d = d.merge(agg, left_on=["PH_SEQ", "A_LINENO"], right_index=True, how="left")
    for c in ["n_kids", "child_years", "max_years_to_16", "sole_kids", "sole_child_years"]:
        d[c] = d[c].fillna(0.0)
    d["has_kid"] = d.n_kids.gt(0).astype(float)
    d["any_under16"] = d.max_years_to_16.gt(0).astype(float)

    G = groups(d)
    adults = d.A_AGE.ge(18).to_numpy() & d.PRPERTYP.eq(2).to_numpy()
    band = np.digitize(d.A_AGE, [25, 35, 45, 55, 65, 75])
    band_lab = {i: f"{lo}-{hi-1}" if hi < 200 else f"{lo}+" for i, (lo, hi) in enumerate(BANDS)}

    rows, rows_age = [], []
    for name, mask in G.items():
        m = mask & adults
        for sex, slab in [(1, "male"), (2, "female"), (0, "all")]:
            sm = m & (d.A_SEX.eq(sex).to_numpy() if sex else np.ones(len(d), bool))
            for b in range(len(BANDS)):
                sel = sm & (band == b)
                w = d.w.to_numpy()[sel]
                if w.sum() <= 0:
                    continue
                sub = d[sel]
                rows_age.append(dict(
                    group=name, sex=slab, band=band_lab[b], n=int(sel.sum()),
                    pop=float(w.sum()),
                    share_with_minor_child=float(np.average(sub.has_kid, weights=w)),
                    mean_kids=float(np.average(sub.n_kids, weights=w)),
                    mean_kids_if_parent=float(np.average(sub.n_kids[sub.has_kid.gt(0)],
                                                         weights=w[sub.has_kid.gt(0)]))
                    if sub.has_kid.sum() else 0.0,
                    mean_child_years=float(np.average(sub.child_years, weights=w)),
                    mean_sole_child_years=float(np.average(sub.sole_child_years, weights=w)),
                    share_any_child_under16=float(np.average(sub.any_under16, weights=w)),
                    mean_years_to_16_max=float(np.average(sub.max_years_to_16, weights=w)),
                ))
            sel = sm
            w = d.w.to_numpy()[sel]
            sub = d[sel]
            rows.append(dict(group=name, sex=slab, band="18+", n=int(sel.sum()),
                             pop=float(w.sum()),
                             share_with_minor_child=float(np.average(sub.has_kid, weights=w)),
                             mean_kids=float(np.average(sub.n_kids, weights=w)),
                             mean_child_years=float(np.average(sub.child_years, weights=w)),
                             mean_sole_child_years=float(np.average(sub.sole_child_years, weights=w)),
                             share_any_child_under16=float(np.average(sub.any_under16, weights=w)),
                             mean_years_to_16_max=float(np.average(sub.max_years_to_16, weights=w))))
    pd.DataFrame(rows).to_csv(OUT / "cps_parent_channel.csv", index=False)
    pd.DataFrame(rows_age).to_csv(OUT / "cps_parent_channel_by_age.csv", index=False)
    print("\n[18+ summary]")
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
