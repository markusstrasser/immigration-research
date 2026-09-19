#!/usr/bin/env python3
"""Arm 2 (ACS half) and Arm 6: Borjas-style residual on ACS 2024 1-year PUMS,
plus the definition ladder that the "40 million" claim has to climb.

Input : _cache/acs2024_person_subset.parquet (built by extract_pums.py)
Output: derived/acs2024_residual_by_region.csv
        derived/acs2024_residual_by_yrsince.csv
        derived/acs2024_definition_ladder.csv
        derived/acs2024_rule_hits.csv

The rule list is George J. Borjas, "The Labor Supply of Undocumented Immigrants",
NBER WP 22102 (2016) / Labour Economics 46 (2017), pp. 10-11, reproduced verbatim
in infra/immigration-fiscal/status_impute_2026_09_16/impute_status.py.  That lane
implements it on CPS ASEC fields.  The ACS carries different variables, so each
rule is mapped below and every mapping that is not exact is flagged.

Mapping, rule by rule:
  a. arrived before 1980        -> YOEP < 1980 (exact; ACS records year of entry)
  b. citizen                    -> CIT in {1,2,3,4} (exact)
  c. SS / SSI / Medicaid / Medicare / military insurance
                                -> SSP>0 | SSIP>0 | HINS4==1 | HINS3==1 | HINS5==1
                                   [INFERENCE] ACS records Medicaid/Medicare/TRICARE
                                   as COVERAGE, the CPS as receipt; close but not identical.
  d. veteran or in armed forces -> MIL in {1,2,3} (active now, active in past,
                                   training only in Reserves/National Guard)
  e. government sector          -> COW in {3,4,5} (exact)
  f. public housing / rent subsidy
                                -> NOT AVAILABLE.  ACS PUMS carries no public-housing
                                   or rental-subsidy flag.  Rule (f) is DROPPED and the
                                   omission is reported; it makes the ACS residual
                                   mechanically LARGER than the CPS residual.
  g. born in Cuba               -> POBP==327 (exact); --wide-refugee adds the same
                                   origin list the CPS lane uses, as a sensitivity.
  h. licensed occupation        -> OCCP in the CPS lane's 2018-code list (exact code
                                   system; the list itself is that lane's [INFERENCE]).
  i. spouse legal or citizen    -> ACS has no spouse line pointer.  Reference person
                                   (RELSHIPP==20) is linked to the person in the same
                                   SERIALNO with RELSHIPP in {21,23} (opposite- or
                                   same-sex spouse).  Households with several such
                                   records, or none, get no spouse link.  [INFERENCE]

Every count is ACS-weighted (PWGTP).  Sampling standard errors use the 80
successive-difference replicate weights, the Census Bureau's published design.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

REPS = [f"PWGTP{i}" for i in range(1, 81)]

CUBA = 327
# Same wider refugee-origin list as the CPS lane, translated to ACS POBP codes.
WIDE_REFUGEE = {150, 163, 164, 165, 200, 203, 205, 206, 212, 213, 223, 239,
                242, 247, 327, 412, 416, 417, 448, 451, 459}

# 2018 Census occupation codes; identical list to status_impute_2026_09_16.
LICENSED_OCC = {2100, 2110, 3000, 3010, 3030, 3040, 3050, 3090, 3100, 3110,
                3120, 3140, 3150, 3160, 3200, 3210, 3220, 3230, 3245, 3250,
                3255, 3256, 3258, 3300, 3600, 3700, 3740, 3800, 3820, 3850,
                3870, 9030, 9040}

GOVERNMENT_COW = [3, 4, 5]

# POBP region bands, from the 2024 PUMS data dictionary ordering.
REGIONS = [
    ("United States", 1, 99),
    ("Europe", 100, 199),
    ("Asia", 200, 299),
    ("Mexico", 303, 303),
    ("Other North/Central America and Caribbean", 300, 359),
    ("South America", 360, 399),
    ("Africa", 400, 499),
    ("Oceania and at sea", 500, 559),
]


def se_from_reps(point: float, reps: np.ndarray) -> float:
    """Census successive-difference replication: SE = sqrt(4/80 * sum (r_i - x)^2)."""
    return float(np.sqrt(4.0 / 80.0 * np.square(reps - point).sum()))


def weighted(mask: np.ndarray, w: np.ndarray, rw: np.ndarray) -> tuple[float, float]:
    point = float(w[mask].sum())
    reps = rw[mask].sum(axis=0).astype(float)
    return point, se_from_reps(point, reps)


def region_of(pobp: np.ndarray) -> np.ndarray:
    out = np.full(len(pobp), "Unknown", dtype=object)
    for name, lo, hi in REGIONS:
        if name == "Mexico":
            continue
        out[(pobp >= lo) & (pobp <= hi)] = name
    out[pobp == 303] = "Mexico"
    return out


def build_rules(d: pd.DataFrame, *, refugee: str, use_occupation_rule: bool) -> dict:
    n = len(d)
    cit = d.CIT.to_numpy()
    rule = {}
    yoep = d.YOEP.to_numpy()
    rule["a_arrived_pre_1980"] = np.nan_to_num(yoep, nan=0).astype(int) > 0
    rule["a_arrived_pre_1980"] &= np.nan_to_num(yoep, nan=9999).astype(int) < 1980
    rule["b_citizen"] = np.isin(cit, [1, 2, 3, 4])
    rule["c_benefits"] = ((d.SSP.fillna(0).to_numpy() > 0)
                          | (d.SSIP.fillna(0).to_numpy() > 0)
                          | (d.HINS4.to_numpy() == 1)
                          | (d.HINS3.to_numpy() == 1)
                          | (d.HINS5.to_numpy() == 1))
    rule["d_veteran_or_armed_forces"] = np.isin(d.MIL.to_numpy(), [1, 2, 3])
    rule["e_government_sector"] = np.isin(d.COW.to_numpy(), GOVERNMENT_COW)
    rule["f_subsidised_housing"] = np.zeros(n, dtype=bool)   # unavailable in ACS PUMS
    if refugee == "cuba":
        rule["g_refugee_origin"] = d.POBP.to_numpy() == CUBA
    elif refugee == "wide":
        rule["g_refugee_origin"] = np.isin(d.POBP.to_numpy(), sorted(WIDE_REFUGEE))
    else:
        raise ValueError(f"unknown refugee option {refugee!r}")
    rule["h_licensed_occupation"] = (np.isin(d.OCCP.fillna(-1).to_numpy(),
                                             sorted(LICENSED_OCC))
                                     if use_occupation_rule
                                     else np.zeros(n, dtype=bool))
    return rule


def spouse_index(d: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Reference person <-> spouse link inside each SERIALNO.

    Returns (has_spouse, spouse_row).  Only households with exactly one
    reference person and exactly one spouse record get a link.
    """
    n = len(d)
    rel = d.RELSHIPP.to_numpy()
    # SERIALNO is a 13-character string; factorize to a dense integer household id.
    hh, _ = pd.factorize(d.SERIALNO.to_numpy(), sort=False)
    nhh = int(hh.max()) + 1
    is_ref = rel == 20
    is_sp = np.isin(rel, [21, 23])
    pos = np.arange(n)

    def unique_pos(flag: np.ndarray) -> np.ndarray:
        """Per household: the row index of the single flagged record, else -1."""
        count = np.bincount(hh, weights=flag.astype(float), minlength=nhh)
        best = np.full(nhh, -1, dtype=np.int64)
        np.maximum.at(best, hh, np.where(flag, pos, -1))
        best[count != 1] = -1
        return best

    ref_row = unique_pos(is_ref)[hh]
    sp_row = unique_pos(is_sp)[hh]

    spouse_row = np.full(n, -1, dtype=int)
    ok = (ref_row >= 0) & (sp_row >= 0)
    spouse_row[ok & is_ref] = sp_row[ok & is_ref]
    spouse_row[ok & is_sp] = ref_row[ok & is_sp]
    return spouse_row >= 0, np.where(spouse_row >= 0, spouse_row, 0)


def impute(d: pd.DataFrame, *, refugee: str = "cuba",
           use_occupation_rule: bool = True) -> dict:
    rule = build_rules(d, refugee=refugee, use_occupation_rule=use_occupation_rule)
    own_legal = np.zeros(len(d), dtype=bool)
    for v in rule.values():
        own_legal |= v

    has_spouse, sp_idx = spouse_index(d)
    legal = own_legal.copy()
    for _ in range(10):
        nxt = legal | (has_spouse & legal[sp_idx])
        if np.array_equal(nxt, legal):
            break
        legal = nxt
    else:
        raise ValueError("spouse legality did not reach a fixpoint")
    rule["i_spouse_legal_or_citizen"] = legal & ~own_legal

    foreign_born = d.NATIVITY.to_numpy() == 2
    return {"foreign_born": foreign_born, "legal": legal,
            "unauthorized": foreign_born & ~legal, "rule": rule,
            "own_legal": own_legal, "has_spouse": has_spouse}


# --- OHSS coverage model -----------------------------------------------------
# "the undercount rate for unauthorized immigrants in the ACS is 13 percent for
# those who arrived in the most recent year and declines by 7.5 percent with each
# year of presence."  [SOURCE: DHS OHSS April 2024, appendix item 1e]
# Read as a geometric decline: rate(y) = 0.13 * (1 - 0.075)^y, y = years of
# presence.  The multiplier applied to a counted person is 1/(1-rate).
def ohss_multiplier(years_present: np.ndarray) -> np.ndarray:
    y = np.clip(years_present, 0, None)
    rate = 0.13 * np.power(1.0 - 0.075, y)
    return 1.0 / (1.0 - rate)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refugee", choices=["cuba", "wide"], default="cuba")
    ap.add_argument("--no-occupation-rule", action="store_true")
    args = ap.parse_args()

    DERIVED.mkdir(exist_ok=True)
    # Non-default rule settings write to their own files so a sensitivity run can
    # never overwrite the headline tables.
    sfx = "" if (args.refugee == "cuba" and not args.no_occupation_rule) else (
        f"_{args.refugee}" + ("_noocc" if args.no_occupation_rule else ""))
    src = CACHE / "acs2024_person_subset.parquet"
    print(f"reading {src}", flush=True)
    d = pd.read_parquet(src)
    print(f"{len(d):,} person rows", flush=True)

    w = d.PWGTP.to_numpy(float)
    rw = d[REPS].to_numpy(float)
    print(f"weighted total population: {w.sum():,.0f}", flush=True)

    res = impute(d, refugee=args.refugee,
                 use_occupation_rule=not args.no_occupation_rule)
    fb, legal, unauth = res["foreign_born"], res["legal"], res["unauthorized"]

    # ---- rule hit table -----------------------------------------------------
    rows = []
    for name, m in res["rule"].items():
        pt, se = weighted(m & fb, w, rw)
        rows.append({"rule": name, "foreign_born_hits": round(pt),
                     "se": round(se), "unweighted_rows": int((m & fb).sum())})
    pd.DataFrame(rows).to_csv(DERIVED / f"acs2024_rule_hits{sfx}.csv", index=False)
    print(f"wrote acs2024_rule_hits{sfx}.csv", flush=True)

    # ---- years since arrival, and the OHSS coverage multiplier --------------
    yoep = pd.to_numeric(d.YOEP, errors="coerce").to_numpy(float)
    years_present = np.where(np.isnan(yoep), np.nan, 2024.0 - yoep)
    mult = np.where(np.isnan(years_present), 1.0,
                    ohss_multiplier(np.nan_to_num(years_present, nan=0.0)))

    # ---- residual by region of birth ---------------------------------------
    reg = region_of(d.POBP.fillna(-1).to_numpy())
    rows = []
    for name in ["Mexico", "Other North/Central America and Caribbean",
                 "South America", "Asia", "Europe", "Africa",
                 "Oceania and at sea", "Unknown"]:
        m = unauth & (reg == name)
        if not m.any():
            continue
        pt, se = weighted(m, w, rw)
        fbpt, _ = weighted(fb & (reg == name), w, rw)
        rows.append({"region_of_birth": name,
                     "foreign_born": round(fbpt),
                     "residual_unadjusted": round(pt),
                     "se": round(se),
                     "residual_ohss_coverage": round(float((w * mult)[m].sum())),
                     "share_of_foreign_born_pct": round(100 * pt / fbpt, 1)})
    tot = unauth
    tot_pt, tot_se = weighted(tot, w, rw)
    fbpt, fbse = weighted(fb, w, rw)
    rows.append({"region_of_birth": "TOTAL", "foreign_born": round(fbpt),
                 "residual_unadjusted": round(tot_pt), "se": round(tot_se),
                 "residual_ohss_coverage": round(float((w * mult)[tot].sum())),
                 "share_of_foreign_born_pct": round(100 * tot_pt / fbpt, 1)})
    pd.DataFrame(rows).to_csv(DERIVED / f"acs2024_residual_by_region{sfx}.csv", index=False)
    print(f"wrote acs2024_residual_by_region{sfx}.csv", flush=True)

    # ---- residual by years since arrival ------------------------------------
    bands = [(0, 0, "2024 (survey year)"), (1, 3, "2021-2023"), (4, 5, "2019-2020"),
             (6, 10, "2014-2018"), (11, 15, "2009-2013"), (16, 25, "1999-2008"),
             (26, 44, "1980-1998"), (45, 200, "before 1980")]
    rows = []
    for lo, hi, label in bands:
        m = unauth & ~np.isnan(years_present) & (years_present >= lo) & (years_present <= hi)
        if not m.any():
            continue
        pt, se = weighted(m, w, rw)
        rows.append({"years_since_arrival": f"{lo}-{hi}", "arrival_window": label,
                     "residual_unadjusted": round(pt), "se": round(se),
                     "implied_ohss_multiplier": round(float((w * mult)[m].sum() / pt), 4),
                     "residual_ohss_coverage": round(float((w * mult)[m].sum()))})
    pd.DataFrame(rows).to_csv(DERIVED / f"acs2024_residual_by_yrsince{sfx}.csv", index=False)
    print(f"wrote acs2024_residual_by_yrsince{sfx}.csv", flush=True)

    # ---- Arm 6: the definition ladder --------------------------------------
    cit = d.CIT.to_numpy()
    noncit = cit == 5
    post1980 = ~np.isnan(yoep) & (yoep >= 1980)
    ladder = []

    def add(label, mask, note):
        pt, se = weighted(mask, w, rw)
        ladder.append({"definition": label, "acs2024_weighted": round(pt),
                       "se": round(se), "note": note})

    add("Borjas residual, ACS 2024, no coverage adjustment", unauth,
        "foreign born minus everyone a Borjas rule marks legal; ACS lacks rule (f)")
    add("Borjas residual, non-citizens only", unauth & noncit,
        "drops the naturalised; identical by construction of rule (b)")
    add("All non-citizens, ACS 2024", noncit,
        "CIT==5; includes students, H-1B, green-card holders, TPS, parolees")
    add("All non-citizens who arrived 1980 or later", noncit & post1980,
        "the base CIS subtracts its legal-stock estimate from")
    add("All foreign born, ACS 2024", fb, "NATIVITY==2; includes naturalised citizens")
    add("All foreign born plus US-born children under 18 of a non-citizen parent",
        fb, "PLACEHOLDER - not computed here; see note in RESULT.md")
    lad = pd.DataFrame(ladder)
    lad = lad[lad.definition != "All foreign born plus US-born children under 18 of a non-citizen parent"]
    lad.to_csv(DERIVED / f"acs2024_definition_ladder{sfx}.csv", index=False)
    print(f"wrote acs2024_definition_ladder{sfx}.csv", flush=True)

    summary = {
        "acs_2024_1yr_person_rows": int(len(d)),
        "weighted_total_population": round(float(w.sum())),
        "foreign_born": round(fbpt), "foreign_born_se": round(fbse),
        "non_citizens": round(float(w[noncit].sum())),
        "non_citizens_post_1980_arrival": round(float(w[noncit & post1980].sum())),
        "borjas_residual_unadjusted": round(tot_pt), "borjas_residual_se": round(tot_se),
        "borjas_residual_ohss_coverage": round(float((w * mult)[tot].sum())),
        "rules": {"refugee": args.refugee,
                  "occupation_rule": not args.no_occupation_rule,
                  "rule_f_available": False},
    }
    out = DERIVED / f"acs2024_summary{sfx or '_cuba'}.json"
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
