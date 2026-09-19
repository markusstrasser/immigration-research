#!/usr/bin/env python3
"""Arm 3b -- strict replication of Duncan & Trejo (2011) Table 8 on CPS ASEC 2025,
and the decomposition of the gap between their rates and today's.

Duncan & Trejo's sample: US-born children ages 17 and below who live in INTACT
families (both parents present) and either have at least one parent or grandparent
born in Mexico or else have at least one parent identified as Mexican by the CPS
Hispanic-origin question.  Suspected stepchildren are excluded.
[SOURCE: Duncan & Trejo 2011, "Intermarriage and the Intergenerational Transmission
of Ethnic Identity and Human Capital for Mexican Americans", Journal of Labor
Economics 29(2):195-227; CReAM Discussion Paper 02/09 copy, Table 8 on PDF page 49,
narrative on PDF pages 29-30.  Their source is 1994-2006 CPS data.]

This lane can exclude stepchildren exactly, because CPS ASEC carries PEPAR1TYP /
PEPAR2TYP (1 biological, 2 step, 3 adopted).  A step-parent's parents are not the
child's grandparents, so the strict arm keeps biological parents only.

Also computes the third-plus correction multiplier directly, from the children who
sit in the same universe as the standing adult "G3+ self-ID" count: US-born children
with two US-area-born parents.

Inputs : _cache/cps_asec2025_person_subset.parquet
Outputs: derived/arm3_dt_table8_replication.csv
         derived/arm3_dt_decomposition.csv
         derived/arm3_multiplier.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

MEXICO = 303
US_AREA = (57, 60, 66, 69, 73, 78)
REP_N = 160
W0 = "pwwgt0"
REPS = [f"pwwgt{i}" for i in range(1, REP_N + 1)]

# Duncan & Trejo 2011 Table 8, 1994-2006 CPS: percent identified as Mexican, and
# percent of the generation, for each cell.
DT2011 = {
    "2nd gen, both parents Mexico-born": (97.9, 68.4),
    "2nd gen, one parent Mexico-born": (80.6, 31.6),
    "2nd gen, all": (92.4, 100.0),
    "3rd gen, four grandparents Mexico-born": (96.2, 10.0),
    "3rd gen, three grandparents Mexico-born": (95.2, 7.1),
    "3rd gen, two grandparents Mexico-born": (78.7, 34.5),
    "3rd gen, one grandparent Mexico-born": (58.4, 48.5),
    "3rd gen, all": (71.8, 100.0),
    "4th+ gen, both parents identified Mexican": (98.4, 42.9),
    "4th+ gen, one parent identified Mexican": (50.1, 57.1),
    "4th+ gen, all": (70.8, 100.0),
    "all US-born Mexican children": (84.2, 100.0),
}
# share of all US-born Mexican children in each generation, Duncan & Trejo Table 8
DT2011_GEN_SHARE = {"2nd gen": 61.2, "3rd gen": 12.8, "4th+ gen": 26.0}


def sdr_se(full: float, reps: np.ndarray) -> float:
    return float(np.sqrt(4.0 / REP_N * np.sum((reps - full) ** 2)))


def wtot(d: pd.DataFrame, mask: np.ndarray) -> tuple[float, float]:
    sub = d.loc[mask]
    full = float(sub[W0].sum())
    return full, sdr_se(full, sub[REPS].sum().to_numpy(dtype=float))


def wratio(d: pd.DataFrame, num: np.ndarray, den: np.ndarray) -> tuple[float, float]:
    dn, nn = d.loc[den], d.loc[num & den]
    d0, n0 = float(dn[W0].sum()), float(nn[W0].sum())
    if d0 <= 0:
        return float("nan"), float("nan")
    dr = dn[REPS].sum().to_numpy(dtype=float)
    nr = nn[REPS].sum().to_numpy(dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        rr = np.where(dr > 0, nr / dr, np.nan)
    return n0 / d0, sdr_se(n0 / d0, rr[np.isfinite(rr)])


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    d = pd.read_parquet(CACHE / "cps_asec2025_person_subset.parquet")
    n = len(d)
    print(f"records: {n:,}", flush=True)

    key = d["PH_SEQ"].to_numpy().astype(np.int64)
    line = d["A_LINENO"].to_numpy().astype(np.int64)
    row_of = pd.Series(np.arange(n), index=pd.Index(key * 100 + line))

    par_idx = np.full((n, 2), -1, dtype=np.int64)
    bio = np.zeros((n, 2), dtype=bool)
    for j, (pcol, tcol) in enumerate((("PEPAR1", "PEPAR1TYP"), ("PEPAR2", "PEPAR2TYP"))):
        ln = d[pcol].to_numpy().astype(np.int64)
        ok = ln > 0
        looked = row_of.reindex(key[ok] * 100 + ln[ok]).to_numpy()
        par_idx[ok, j] = np.where(np.isnan(looked), -1, np.nan_to_num(looked, nan=-1.0))
        bio[:, j] = d[tcol].to_numpy() == 1

    def pattr(arr: np.ndarray, slot: int) -> np.ndarray:
        out = np.full(n, np.nan)
        ok = par_idx[:, slot] >= 0
        out[ok] = arr[par_idx[ok, slot]]
        return out

    pen, pmn, pfn = (d[c].to_numpy() for c in ("PENATVTY", "PEMNTVTY", "PEFNTVTY"))
    hisp = (d["PEHSPNON"] == 1).to_numpy()
    mex_id = hisp & (d["PRDTHSP"] == 1).to_numpy()
    native = d["PRCITSHP"].isin([1, 2, 3]).to_numpy()
    child = (d["A_AGE"] <= 17).to_numpy()

    par_born = np.stack([pattr(pen, 0), pattr(pen, 1)], axis=1)
    par_mom = np.stack([pattr(pmn, 0), pattr(pmn, 1)], axis=1)
    par_dad = np.stack([pattr(pfn, 0), pattr(pfn, 1)], axis=1)
    par_mexid = np.stack([pattr(mex_id.astype(float), 0),
                          pattr(mex_id.astype(float), 1)], axis=1) == 1.0

    for arm, bio_only in (("all parent types", False), ("biological parents only", True)):
        present = par_idx >= 0
        if bio_only:
            present = present & bio
        two_par = present.sum(axis=1) == 2
        pb = np.where(present, par_born, np.nan)
        gp_mex = np.where(present, (par_mom == MEXICO).astype(float)
                          + (par_dad == MEXICO).astype(float), 0.0).sum(axis=1)
        n_par_mexborn = np.where(present, pb == MEXICO, False).sum(axis=1)
        n_par_mexid = np.where(present, par_mexid, False).sum(axis=1)
        all_us = np.where(present, np.isin(pb, US_AREA), True).all(axis=1)

        base = native & child & two_par & ~(pen == MEXICO)
        g2 = base & (n_par_mexborn > 0)
        g3 = base & (n_par_mexborn == 0) & all_us & (gp_mex > 0)
        g4 = base & (n_par_mexborn == 0) & all_us & (gp_mex == 0) & (n_par_mexid > 0)
        universe = g2 | g3 | g4

        rows = []
        cells = [
            ("2nd gen, both parents Mexico-born", g2 & (n_par_mexborn == 2), "2nd gen"),
            ("2nd gen, one parent Mexico-born", g2 & (n_par_mexborn == 1), "2nd gen"),
            ("2nd gen, all", g2, "2nd gen"),
            ("3rd gen, four grandparents Mexico-born", g3 & (gp_mex == 4), "3rd gen"),
            ("3rd gen, three grandparents Mexico-born", g3 & (gp_mex == 3), "3rd gen"),
            ("3rd gen, two grandparents Mexico-born", g3 & (gp_mex == 2), "3rd gen"),
            ("3rd gen, one grandparent Mexico-born", g3 & (gp_mex == 1), "3rd gen"),
            ("3rd gen, all", g3, "3rd gen"),
            ("4th+ gen, both parents identified Mexican", g4 & (n_par_mexid == 2), "4th+ gen"),
            ("4th+ gen, one parent identified Mexican", g4 & (n_par_mexid == 1), "4th+ gen"),
            ("4th+ gen, all", g4, "4th+ gen"),
            ("all US-born Mexican children", universe, "all"),
        ]
        u_tot, _ = wtot(d, universe)
        gen_tot = {g: wtot(d, m)[0] for g, m in
                   (("2nd gen", g2), ("3rd gen", g3), ("4th+ gen", g4))}
        print(f"\nDuncan-Trejo Table 8 replication -- {arm}", flush=True)
        print(f"  universe: {int(universe.sum()):,} children, {u_tot/1e6:.3f}M weighted",
              flush=True)
        for label, m, gen in cells:
            r, se = wratio(d, mex_id, m)
            t, _ = wtot(d, m)
            dt_id, dt_share = DT2011[label]
            rows.append({
                "cell": label, "generation": gen,
                "pct_identified_mexican_2025": round(r * 100, 2),
                "se": round(se * 100, 2),
                "pct_identified_mexican_DT_1994_2006": dt_id,
                "pct_of_generation_2025": round(
                    100 * t / gen_tot[gen], 2) if gen in gen_tot else 100.0,
                "pct_of_generation_DT": dt_share,
                "pct_of_all_us_born_mexican_children_2025": round(100 * t / u_tot, 2),
                "weighted": round(t, 1), "unweighted_n": int(m.sum()),
            })
            print(f"  {label:<44} {r*100:6.2f}% (se {se*100:4.2f})  "
                  f"DT {dt_id:5.1f}%   n={int(m.sum()):,}", flush=True)
        df = pd.DataFrame(rows)
        suffix = "" if not bio_only else "_biological"
        df.to_csv(DERIVED / f"arm3_dt_table8_replication{suffix}.csv", index=False)

        # Duncan & Trejo 2017 (ILR Review) Table 1 uses the same third-generation
        # sample but the broader HISPANIC identification outcome, and pools five
        # source countries.  Their rates: 98.6 / 93.1 / 81.7 for first-generation
        # adults, second-generation adults and third-generation children.
        # The comparable Mexican-only cells on this file:
        if not bio_only:
            hrows = []
            for label, m, dt in (
                ("2nd generation children, identify as Hispanic", g2, None),
                ("3rd generation children, identify as Hispanic", g3, 81.7),
                ("4th+ generation children, identify as Hispanic", g4, None),
            ):
                r, se = wratio(d, hisp, m)
                hrows.append({"cell": label,
                              "pct_identified_hispanic_2025_mexican_only": round(r * 100, 2),
                              "se": round(se * 100, 2),
                              "pct_identified_hispanic_DT2017_pan_hispanic": dt,
                              "unweighted_n": int(m.sum())})
                print(f"  {label:<48} {r*100:6.2f}% (se {se*100:4.2f})"
                      + (f"  DT2017 {dt}%" if dt else ""), flush=True)
            pd.DataFrame(hrows).to_csv(
                DERIVED / "arm3_dt_hispanic_definition.csv", index=False)

        if not bio_only:
            keep = df[df["cell"].str.startswith("3rd gen, ") & (df["cell"] != "3rd gen, all")]
            now_rate = (100 - keep["pct_identified_mexican_2025"].to_numpy()) / 100
            dt_rate = (100 - keep["pct_identified_mexican_DT_1994_2006"].to_numpy()) / 100
            now_w = keep["pct_of_generation_2025"].to_numpy() / 100
            dt_w = keep["pct_of_generation_DT"].to_numpy() / 100
            dec = [
                {"arm": "Duncan-Trejo 1994-2006 composition x DT rates",
                 "third_gen_attrition_pct": round(100 * float(dt_w @ dt_rate), 2)},
                {"arm": "CPS 2025 composition x DT rates (composition effect)",
                 "third_gen_attrition_pct": round(100 * float(now_w @ dt_rate), 2)},
                {"arm": "DT composition x CPS 2025 rates (rate effect)",
                 "third_gen_attrition_pct": round(100 * float(dt_w @ now_rate), 2)},
                {"arm": "CPS 2025 composition x CPS 2025 rates",
                 "third_gen_attrition_pct": round(100 * float(now_w @ now_rate), 2)},
            ]
            pd.DataFrame(dec).to_csv(DERIVED / "arm3_dt_decomposition.csv", index=False)
            print("\n  decomposition of the 3rd-generation attrition gap:", flush=True)
            for r in dec:
                print(f"    {r['arm']:<52} {r['third_gen_attrition_pct']:5.2f}%", flush=True)

            # ---- the multiplier for the standing third-plus self-ID count ----
            # Universe matching the adult G3+ definition, at child ages:
            # US-born, both co-resident parents born in a US area.
            uni = native & child & two_par & ~(pen == MEXICO) & all_us
            A = uni & mex_id                       # self-identified Mexican (the count we have)
            B = uni & (gp_mex > 0)                 # objectively 3rd generation
            aA, seA = wtot(d, A)
            aB, seB = wtot(d, B)
            aAB, _ = wtot(d, A & B)
            aBnotA, seBnotA = wtot(d, B & ~mex_id)
            aAnotB, _ = wtot(d, A & ~(gp_mex > 0))
            mult = (aA + aBnotA) / aA
            mrows = [
                {"quantity": "A: self-identified Mexican, two US-area-born parents",
                 "children": round(aA, 1), "se": round(seA, 1)},
                {"quantity": "B: objectively 3rd generation (>=1 Mexico-born grandparent)",
                 "children": round(aB, 1), "se": round(seB, 1)},
                {"quantity": "A and B: 3rd-generation identifiers",
                 "children": round(aAB, 1), "se": None},
                {"quantity": "B not A: 3rd-generation attriters (recoverable)",
                 "children": round(aBnotA, 1), "se": round(seBnotA, 1)},
                {"quantity": "A not B: 4th-plus identifiers (no Mexico-born grandparent)",
                 "children": round(aAnotB, 1), "se": None},
                {"quantity": "multiplier (A + B\\A) / A applied to the adult G3+ count",
                 "children": round(mult, 5), "se": None},
            ]
            pd.DataFrame(mrows).to_csv(DERIVED / "arm3_multiplier.csv", index=False)
            print("\n  third-plus correction multiplier", flush=True)
            for r in mrows[:-1]:
                print(f"    {r['quantity']:<62} {r['children']/1e6:7.3f}M", flush=True)
            print(f"    multiplier = {mult:.4f}", flush=True)

    print("\nwrote derived/arm3_dt_*.csv, arm3_multiplier.csv", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
