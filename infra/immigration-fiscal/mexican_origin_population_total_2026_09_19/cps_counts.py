#!/usr/bin/env python3
"""Arm 1 (self-identification baseline) and Arm 3 (attrition reproduced on children).

CPS ASEC 2025 person file, income year 2024, interview February-April 2025.

Arm 1 -- counts of the Mexican-origin population under each self-report definition,
with 160-replicate successive-difference standard errors (Census SDR, factor 4/160).

Arm 3 -- for children living with their parents, Mexican descent is observed from the
PARENT's birthplace (second generation) and from the parent's own parents' birthplace
(third generation, i.e. the child's grandparents).  Ethnic attrition is then the share
of those children whose own Hispanic-origin report is not Mexican.

Country codes: 057 United States, 060 American Samoa, 066 Guam, 069 Northern Marianas,
073 Puerto Rico, 078 U.S. Virgin Islands, 303 Mexico.
[SOURCE: CPS March 2025 technical documentation, Appendix J "Countries and Areas of
the World", p. J-1, extracted from cpsmar25.pdf]
PRDTHSP 1 = Mexican, universe PEHSPNON = 1.  [SOURCE: 2025 ASEC data dictionary,
record type Person, position 152]

Inputs : _cache/cps_asec2025_person_subset.parquet  (from extract_cps.py)
Outputs: derived/arm1_counts_cps.csv
         derived/arm1_definition_notes.json
         derived/arm3_attrition_children.csv
         derived/arm3_grandparent_counts.csv
         derived/arm3_applied_correction.csv
"""
from __future__ import annotations

import json
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


def sdr_se(full: float, reps: np.ndarray) -> float:
    """Census successive-difference replication SE for the ASEC, 160 replicates."""
    return float(np.sqrt(4.0 / REP_N * np.sum((reps - full) ** 2)))


def weighted_total(d: pd.DataFrame, mask: np.ndarray) -> tuple[float, float]:
    sub = d.loc[mask]
    full = float(sub[W0].sum())
    reps = sub[REPS].sum().to_numpy(dtype=float)
    return full, sdr_se(full, reps)


def weighted_ratio(d: pd.DataFrame, num: np.ndarray, den: np.ndarray) -> tuple[float, float, float, int]:
    """Ratio of weighted totals with an SDR SE computed on the ratio itself."""
    dn = d.loc[den]
    nn = d.loc[num & den]
    d0 = float(dn[W0].sum())
    n0 = float(nn[W0].sum())
    if d0 <= 0:
        return float("nan"), float("nan"), 0.0, 0
    r0 = n0 / d0
    dr = dn[REPS].sum().to_numpy(dtype=float)
    nr = nn[REPS].sum().to_numpy(dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        rr = np.where(dr > 0, nr / dr, np.nan)
    se = sdr_se(r0, rr[~np.isnan(rr)]) if np.isfinite(rr).all() else float("nan")
    return r0, se, d0, int(len(dn))


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    src = CACHE / "cps_asec2025_person_subset.parquet"
    d = pd.read_parquet(src)
    print(f"records: {len(d):,}", flush=True)

    native = d["PRCITSHP"].isin([1, 2, 3]).to_numpy()
    fb = d["PRCITSHP"].isin([4, 5]).to_numpy()
    mex_born = (d["PENATVTY"] == MEXICO).to_numpy()
    mom_mex = (d["PEMNTVTY"] == MEXICO).to_numpy()
    dad_mex = (d["PEFNTVTY"] == MEXICO).to_numpy()
    mom_us = d["PEMNTVTY"].isin(US_AREA).to_numpy()
    dad_us = d["PEFNTVTY"].isin(US_AREA).to_numpy()
    mom_fb = (~mom_us) & (d["PEMNTVTY"] > 0).to_numpy()
    dad_fb = (~dad_us) & (d["PEFNTVTY"] > 0).to_numpy()
    hisp = (d["PEHSPNON"] == 1).to_numpy()
    mex_id = hisp & (d["PRDTHSP"] == 1).to_numpy()

    g1 = mex_born & fb
    g1_any = mex_born
    g2 = native & (mom_mex | dad_mex)
    g3_selfid = native & mom_us & dad_us & mex_id
    # Census Bureau's second-generation construction: Mexican self-ID + any foreign-born parent
    g2_census = native & mex_id & (mom_fb | dad_fb)
    g3_census = native & mex_id & mom_us & dad_us
    native_mex_id = native & mex_id
    # native self-ID Mexican who is neither g2 nor g3_selfid (one US parent, one non-Mexican
    # foreign parent), the definitional residual between the two constructions
    residual = native_mex_id & ~g2 & ~g3_selfid

    rows = []

    def add(label: str, mask: np.ndarray, definition: str) -> None:
        total, se = weighted_total(d, mask)
        rows.append({"definition": label, "population": round(total, 1),
                     "se": round(se, 1), "unweighted_n": int(mask.sum()),
                     "construction": definition})
        print(f"  {label:<44} {total/1e6:8.3f}M  se {se/1e6:.3f}M  n={int(mask.sum()):,}",
              flush=True)

    print("\nArm 1 -- CPS ASEC 2025 self-report definitions", flush=True)
    add("total civilian household population", np.ones(len(d), bool), "all person records")
    add("G1 Mexico-born, foreign-born", g1, "PENATVTY=303 & PRCITSHP in (4,5)")
    add("G1 Mexico-born, any citizenship", g1_any, "PENATVTY=303")
    add("G2 native, >=1 Mexico-born parent", g2,
        "PRCITSHP in (1,2,3) & (PEMNTVTY=303 | PEFNTVTY=303)")
    add("G3+ native, 2 US-area parents, self-ID Mexican", g3_selfid,
        "PRCITSHP in (1,2,3) & both parents US-area & PRDTHSP=1")
    add("UNION repo definition (G1+G2+G3+)", g1 | g2 | g3_selfid, "disjoint union of the three")
    add("G2 Census construction (self-ID + any FB parent)", g2_census,
        "PRCITSHP in (1,2,3) & PRDTHSP=1 & >=1 foreign-born parent")
    add("G3+ Census construction (self-ID + 2 US parents)", g3_census,
        "identical to G3+ self-ID")
    add("all natives self-identifying Mexican", native_mex_id,
        "PRCITSHP in (1,2,3) & PRDTHSP=1")
    add("residual: native self-ID Mexican in neither G2 nor G3+", residual,
        "native & PRDTHSP=1 & not G2 & not G3+")
    add("all self-identifying Mexican (any nativity)", mex_id, "PRDTHSP=1")
    add("UNION Census construction (G1 any + G2c + G3c)", g1_any | g2_census | g3_census,
        "Mexico-born + self-ID with FB parent + self-ID with US parents")

    overlap = int((g1 & g2).sum() + (g1 & g3_selfid).sum() + (g2 & g3_selfid).sum())
    if overlap:
        raise SystemExit(f"repo definition groups are not disjoint: {overlap} records")

    pd.DataFrame(rows).to_csv(DERIVED / "arm1_counts_cps.csv", index=False)

    # ---------------- Arm 3: attrition among co-resident children ----------------
    print("\nArm 3 -- ethnic attrition among children living with their parents", flush=True)
    n = len(d)
    key = d["PH_SEQ"].to_numpy().astype(np.int64)
    line = d["A_LINENO"].to_numpy().astype(np.int64)
    # (household, line) -> row position.  Line numbers run 1..16, so a single
    # integer key is exact.
    row_of = pd.Series(np.arange(n), index=pd.Index(key * 100 + line))
    if row_of.index.has_duplicates:
        raise SystemExit("duplicate (PH_SEQ, A_LINENO) pairs")

    par_idx = np.full((n, 2), -1, dtype=np.int64)
    for j, col in enumerate(("PEPAR1", "PEPAR2")):
        ln = d[col].to_numpy().astype(np.int64)
        ok = ln > 0
        looked = row_of.reindex(key[ok] * 100 + ln[ok]).to_numpy()
        par_idx[ok, j] = np.where(np.isnan(looked), -1, np.nan_to_num(looked, nan=-1.0))
        miss = int(np.isnan(looked).sum())
        if miss:
            print(f"  {col}: {miss} pointers with no matching record (dropped)", flush=True)

    has_p1 = par_idx[:, 0] >= 0
    has_p2 = par_idx[:, 1] >= 0
    n_par = has_p1.astype(int) + has_p2.astype(int)
    print(f"  children with >=1 linked parent record: {int((n_par>0).sum()):,}", flush=True)
    print(f"  with 2 linked parents:                  {int((n_par==2).sum()):,}", flush=True)

    def parent_attr(arr: np.ndarray, slot: int) -> np.ndarray:
        """Value of `arr` for the linked parent in `slot`, NaN when absent."""
        out = np.full(n, np.nan)
        ok = par_idx[:, slot] >= 0
        out[ok] = arr[par_idx[ok, slot]]
        return out

    pen = d["PENATVTY"].to_numpy()
    pmn = d["PEMNTVTY"].to_numpy()
    pfn = d["PEFNTVTY"].to_numpy()

    par_born = np.stack([parent_attr(pen, 0), parent_attr(pen, 1)], axis=1)
    par_mom = np.stack([parent_attr(pmn, 0), parent_attr(pmn, 1)], axis=1)
    par_dad = np.stack([parent_attr(pfn, 0), parent_attr(pfn, 1)], axis=1)

    par_is_mexborn = par_born == MEXICO                      # parent born in Mexico
    par_us_born = np.isin(par_born, US_AREA)                 # parent born in a US area
    # number of Mexico-born grandparents visible through each linked parent
    gp_mex = (par_mom == MEXICO).astype(float) + (par_dad == MEXICO).astype(float)
    gp_mex = np.where(np.isnan(par_born), 0.0, gp_mex)
    n_gp_mex = gp_mex.sum(axis=1)
    n_gp_seen = np.where(par_idx >= 0, 2.0, 0.0).sum(axis=1)

    # a parent is "of Mexican descent" if born in Mexico or has a Mexico-born parent
    par_mex_descent = par_is_mexborn | (gp_mex > 0)
    n_par_mex = np.where(par_idx >= 0, par_mex_descent.astype(float), 0.0).sum(axis=1)

    child_native = native & ~mex_born
    any_par_mexborn = np.where(par_idx >= 0, par_is_mexborn, False).any(axis=1)
    all_par_usborn = np.where(par_idx >= 0, par_us_born, True).all(axis=1) & (n_par > 0)

    obj_g2 = child_native & (n_par > 0) & any_par_mexborn
    obj_g3 = child_native & (n_par > 0) & ~any_par_mexborn & all_par_usborn & (n_gp_mex > 0)

    not_mexican = ~mex_id
    not_hispanic = ~hisp
    hisp_not_mex = hisp & ~mex_id

    arows = []

    def attr(label: str, base: np.ndarray, extra: str = "") -> None:
        for outcome, m in (("not Mexican", not_mexican),
                           ("not Hispanic at all", not_hispanic),
                           ("Hispanic but not Mexican", hisp_not_mex)):
            r, se, den, nrec = weighted_ratio(d, m, base)
            arows.append({"group": label, "outcome": outcome,
                          "attrition_rate": round(r, 5) if r == r else None,
                          "se": round(se, 5) if se == se else None,
                          "weighted_base": round(den, 1), "unweighted_n": nrec,
                          "note": extra})
            print(f"  {label:<40} {outcome:<26} {r*100:6.2f}%  se {se*100:4.2f}  n={nrec:,}",
                  flush=True)

    both_mex = n_par_mex == 2
    one_mex = n_par_mex == 1

    attr("2nd gen children (any parent Mexico-born)", obj_g2)
    attr("2nd gen, both parents Mexican descent", obj_g2 & both_mex)
    attr("2nd gen, one parent Mexican descent", obj_g2 & one_mex)
    attr("2nd gen, two parents present", obj_g2 & (n_par == 2))
    attr("3rd gen children (>=1 Mexico-born grandparent)", obj_g3)
    attr("3rd gen, both parents Mexican descent", obj_g3 & both_mex)
    attr("3rd gen, one parent Mexican descent", obj_g3 & one_mex)
    attr("3rd gen, two parents present", obj_g3 & (n_par == 2))
    for lo, hi, lab in ((0, 5, "0-5"), (6, 11, "6-11"), (12, 17, "12-17")):
        band = (d["A_AGE"] >= lo).to_numpy() & (d["A_AGE"] <= hi).to_numpy()
        attr(f"3rd gen children aged {lab}", obj_g3 & band, "age band")
        attr(f"2nd gen children aged {lab}", obj_g2 & band, "age band")
    # grandparent-count gradient inside the third generation, two parents present
    for k in (1, 2, 3, 4):
        attr(f"3rd gen, {k} Mexico-born grandparent(s) of 4",
             obj_g3 & (n_par == 2) & (n_gp_mex == k), "two parents linked")

    pd.DataFrame(arows).to_csv(DERIVED / "arm3_attrition_children.csv", index=False)

    # fractional vs whole counting of third-generation children
    grows = []
    for k in (1, 2, 3, 4):
        m = obj_g3 & (n_par == 2) & (n_gp_mex == k)
        tot, se = weighted_total(d, m)
        idm = obj_g3 & (n_par == 2) & (n_gp_mex == k) & mex_id
        idt, _ = weighted_total(d, idm)
        grows.append({"mexican_grandparents_of_4": k, "children": round(tot, 1),
                      "se": round(se, 1), "self_id_mexican": round(idt, 1),
                      "fractional_weight": k / 4,
                      "fractional_children": round(tot * k / 4, 1)})
    pd.DataFrame(grows).to_csv(DERIVED / "arm3_grandparent_counts.csv", index=False)
    print("\n  grandparent gradient written", flush=True)

    # ---------------- apply the measured rates to the standing counts ------------
    g3_total, g3_se = weighted_total(d, g3_selfid)
    g2_total, g2_se = weighted_total(d, g2)
    g1_total, g1_se = weighted_total(d, g1)
    a3 = {r["group"]: r for r in arows if r["outcome"] == "not Mexican"}
    rate3 = a3["3rd gen children (>=1 Mexico-born grandparent)"]["attrition_rate"]
    se3 = a3["3rd gen children (>=1 Mexico-born grandparent)"]["se"]
    rate2 = a3["2nd gen children (any parent Mexico-born)"]["attrition_rate"]
    se2 = a3["2nd gen children (any parent Mexico-born)"]["se"]

    crows = []
    for label, base, base_se, rate, rse in (
        ("G2 (parental birthplace, no self-ID needed)", g2_total, g2_se, 0.0, 0.0),
        ("G3+ self-ID, corrected at the reproduced 3rd-gen child rate",
         g3_total, g3_se, rate3, se3),
    ):
        corrected = base / (1 - rate) if rate < 1 else float("nan")
        # delta method on 1/(1-a)
        cse = corrected * np.sqrt((base_se / base) ** 2 + (rse / (1 - rate)) ** 2) if rate else base_se
        crows.append({"group": label, "self_id_count": round(base, 1),
                      "self_id_se": round(base_se, 1),
                      "attrition_rate_applied": round(rate, 5),
                      "attrition_se": round(rse, 5),
                      "corrected_count": round(corrected, 1),
                      "corrected_se": round(cse, 1),
                      "added": round(corrected - base, 1)})
    pd.DataFrame(crows).to_csv(DERIVED / "arm3_applied_correction.csv", index=False)

    notes = {
        "file": "CPS ASEC 2025 public-use person file (pppub25.csv), income year 2024",
        "weights": "pwwgt0 full, pwwgt1..160 replicate; SDR variance factor 4/160",
        "marsupwt_ratio_to_pwwgt0": 100.0,
        "mexico_code": MEXICO,
        "us_area_codes": list(US_AREA),
        "records": int(len(d)),
        "union_repo": round(float(weighted_total(d, g1 | g2 | g3_selfid)[0]), 1),
        "g1": round(g1_total, 1), "g2": round(g2_total, 1), "g3_selfid": round(g3_total, 1),
        "third_gen_child_attrition_not_mexican": rate3,
        "second_gen_child_attrition_not_mexican": rate2,
    }
    (DERIVED / "arm1_definition_notes.json").write_text(
        json.dumps(notes, indent=2, sort_keys=True) + "\n")
    print("\nwrote derived/arm1_counts_cps.csv, arm3_*.csv", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
