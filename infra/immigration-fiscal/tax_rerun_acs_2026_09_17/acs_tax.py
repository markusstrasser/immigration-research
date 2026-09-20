#!/usr/bin/env python3
"""ACS 2024 1-year PUMS tax units run through the same Tax-Calculator.

Tax units are approximated from household relationship, marital status, age
and school enrolment, because the public ACS carries no tax-unit identifier
and no parent pointer. Every construction choice is recorded in
derived/acs_audit.json and in RESULT.md.

Writes derived/acs_tax_cells.csv, derived/acs_tax_gaps.csv,
derived/acs_totals.csv and derived/acs_audit.json.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ACS_LANE = FISCAL / "acs_earnings_replication_2026_09_17"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ACS_LANE))

import common as C  # noqa: E402
import shared  # noqa: E402
import taxcalc_io as TC  # noqa: E402
import units as U  # noqa: E402

DATA = _data_paths.data_root(require_exists=False) / 'external/acs_pums_2024_1yr'
ZIP = DATA / "csv_pus.zip"
SRC_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip"
OUT = HERE / "derived"

REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = (["SERIALNO", "SPORDER", "PWGTP", "STATE", "AGEP", "NATIVITY", "POBP",
         "HISP", "RAC1P", "RELSHIPP", "MAR", "SCH",
         "WAGP", "SEMP", "INTP", "RETP", "SSP", "SSIP", "PAP", "OIP",
         "PINCP", "ADJINC"] + REPS)

# PUMS_Data_Dictionary_2024.csv, RELSHIPP block (lines 1628-1647)
REF_PERSON = 20
SPOUSE = (21, 23)          # opposite-sex and same-sex husband/wife/spouse
PARTNER = (22, 24)         # unmarried partners: separate returns
CHILD_REL = (25, 26, 27, 30, 35)   # son/daughter, adopted, step, grandchild, foster
ENROLLED = (2, 3)          # SCH: public / private-or-home school

GROUPS = {
    "mexico_born": lambda d: d.POBP.eq(303),
    "usborn_mexican_selfid": lambda d: d.NATIVITY.eq(1) & d.HISP.eq(2),
    "native_nh_white": lambda d: d.NATIVITY.eq(1) & d.HISP.eq(1) & d.RAC1P.eq(1),
    "all_native": lambda d: d.NATIVITY.eq(1),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(zip_path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(zip_path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        if not members:
            raise SystemExit(f"[BLOCKED] no csv members in {zip_path}")
        for name in members:
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                part = pd.read_csv(fh, usecols=COLS, dtype={"SERIALNO": str})
            hu = part.SERIALNO.str.slice(4, 6).eq("HU")
            gq = part.RELSHIPP.isin([37, 38])
            if (hu & gq).any() or (~hu & ~gq).any():
                raise SystemExit("[BLOCKED] SERIALNO housing-unit flag disagrees with RELSHIPP 37/38")
            frames.append(part[hu])
    d = pd.concat(frames, ignore_index=True)
    d = d.sort_values(["SERIALNO", "SPORDER"]).reset_index(drop=True)
    print(f"[read] household-population person records: {len(d):,}", flush=True)
    return d


def person_table(d: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, np.ndarray], dict]:
    """Assign every ACS person to one approximate tax return.

    Rule, in full:
      * the householder (RELSHIPP 20) heads return 1 of the household;
      * a person coded as the householder's spouse (RELSHIPP 21 or 23) with
        MAR == 1 joins that return; unmarried partners (22, 24) do not;
      * a dependent is a child of the householder (RELSHIPP 25, 26, 27, 30, 35)
        under 19, or under 24 and enrolled (SCH 2 or 3); any other person under
        18 is also treated as a dependent of the householder, so that every
        person lands on exactly one return;
      * every remaining person aged 18 or over heads his own single return.
        The public ACS carries no parent pointer, so a non-householder adult's
        own children cannot be identified: those children are attached to the
        householder's return. This is the approximation the RESULT.md scope
        note names.
      * a dependent with positive own earnings files a separate single return
        with DSI = 1 and is still claimed by the return that claims him. This
        is the same rule the CPS arm applies.
    """
    n = len(d)
    rel = d.RELSHIPP.to_numpy()
    age = d.AGEP.to_numpy()
    sch = d.SCH.fillna(-1).to_numpy()
    mar = d.MAR.to_numpy()
    serial = d.SERIALNO.to_numpy()

    href = rel == REF_PERSON
    hh_count = pd.Series(href).groupby(d.SERIALNO.to_numpy()).sum()
    if not (hh_count == 1).all():
        raise SystemExit("[BLOCKED] household without exactly one reference person")

    spouse_coded = np.isin(rel, SPOUSE)
    spouse = spouse_coded & (mar == 1)
    dup = pd.Series(spouse).groupby(serial).sum()
    if (dup > 1).max() > 1:
        raise SystemExit("[BLOCKED] household with more than one spouse of the reference person")

    dep_rel = np.isin(rel, CHILD_REL)
    dep_test = (age < 19) | ((age < 24) & np.isin(sch, ENROLLED))
    dependent = (dep_rel & dep_test) | ((age < 18) & ~href & ~spouse)
    own_adult = ~href & ~spouse & ~dependent
    if (own_adult & (age < 18)).any():
        raise SystemExit("[BLOCKED] minor left outside every return")

    adj = d.ADJINC.to_numpy(dtype=float) / 1e6
    g = lambda c: d[c].fillna(0).to_numpy(dtype=float) * adj  # noqa: E731
    wagp, semp = g("WAGP"), g("SEMP")
    intp, retp, ssp = g("INTP"), g("RETP"), g("SSP")
    earn = wagp + semp

    own_return = dependent & (earn > 0)
    claim_key = np.where(href | spouse | dependent, "H" + serial,
                         "A" + serial + "_" + d.SPORDER.astype(str).to_numpy())
    ret_key = np.where(own_return,
                       "D" + serial + "_" + d.SPORDER.astype(str).to_numpy(),
                       claim_key)
    keys = pd.Index(pd.unique(np.concatenate([claim_key, ret_key])))
    keys = keys.sort_values()
    ret = pd.Categorical(ret_key, categories=keys).codes.astype(np.int64)
    claim = pd.Categorical(claim_key, categories=keys).codes.astype(np.int64)

    claim_role = np.where(href, 0, np.where(spouse, 1, np.where(dependent, 2, 0)))
    ret_role = np.where(own_return, 0, claim_role)

    has_spouse = np.zeros(len(keys), dtype=bool)
    has_spouse[claim[spouse]] = True
    has_dep = np.zeros(len(keys), dtype=bool)
    np.add.at(has_dep, claim[dependent], True)
    hh_mars = np.where(has_spouse, 2, np.where(has_dep, 4, 1))
    mars = np.where(own_return, 1, np.where(href | spouse, hh_mars[claim], 1))
    dsi = own_return.astype(int)

    # statutory EITC qualifying child: under 19, or under 24 and a student
    eic_child = (age < 19) | ((age < 24) & np.isin(sch, ENROLLED))
    p = pd.DataFrame({"ret_unit": ret, "ret_role": ret_role,
                      "claim_unit": claim, "claim_role": claim_role,
                      "age": age, "mars": mars, "dsi": dsi, "earn": earn,
                      "eic_child": eic_child})
    p = U.promote_headless(p)

    income = {"e00200": wagp, "e00900": semp,
              "e00300": np.clip(intp, 0, None),
              "e02000": np.clip(intp, None, 0),
              "e01500": retp, "e01700": retp,
              "e02400": ssp}
    diag = {
        "returns": int(len(keys)),
        "households": int(href.sum()),
        "spouse_coded": int(spouse_coded.sum()),
        "spouse_coded_not_married": int((spouse_coded & (mar != 1)).sum()),
        "unmarried_partners_separate": int(np.isin(rel, PARTNER).sum()),
        "dependents": int(dependent.sum()),
        "dependents_by_child_relationship": int((dep_rel & dep_test).sum()),
        "dependents_residual_minors": int(((age < 18) & ~href & ~spouse & ~(dep_rel & dep_test)).sum()),
        "dependent_own_returns": int(own_return.sum()),
        "own_adult_returns": int(own_adult.sum()),
    }
    return p, income, diag


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path, default=ZIP)
    args = ap.parse_args()
    if not args.zip.exists():
        raise SystemExit(f"[BLOCKED] ACS PUMS zip not found: {args.zip}")
    OUT.mkdir(parents=True, exist_ok=True)

    digest = sha256(args.zip)
    d = load(args.zip)
    p, income, diag = person_table(d)
    n_ret = int(p.ret_unit.max()) + 1
    frame = U.build_frame(p, income, n_ret, eic_child=p.eic_child.to_numpy())
    print(f"[taxcalc] ACS: {len(frame):,} returns", flush=True)
    res = TC.run(frame)

    ret = p.ret_unit.to_numpy()
    earn = p.earn.to_numpy()
    person = {"iitax_acsmap": U.allocate(ret, earn, res["iitax"]),
              "payroll_acsmap": U.allocate(ret, earn, res["payroll_employee_equiv"])}

    weights = d[["PWGTP"] + REPS].to_numpy(dtype=float)
    band = C.bands_of(d.AGEP.to_numpy())
    masks = {k: f(d).to_numpy() for k, f in GROUPS.items()}

    fw = weights[:, 0]
    totals = []
    for name, m in masks.items():
        totals.append(dict(group=name, population=float(fw[m].sum()),
                           iitax_bn=float((person["iitax_acsmap"][m] * fw[m]).sum() / 1e9),
                           payroll_bn=float((person["payroll_acsmap"][m] * fw[m]).sum() / 1e9)))
    totals.append(dict(group="all_household_population", population=float(fw.sum()),
                       iitax_bn=float((person["iitax_acsmap"] * fw).sum() / 1e9),
                       payroll_bn=float((person["payroll_acsmap"] * fw).sum() / 1e9)))
    pd.DataFrame(totals).to_csv(OUT / "acs_totals.csv", index=False)

    rows, gaps = shared.cells_and_gaps(masks, band, weights, person,
                                       "national", denom=80, survey="ACS")
    pd.DataFrame(rows).to_csv(OUT / "acs_tax_cells.csv", index=False)
    pd.DataFrame(gaps).to_csv(OUT / "acs_tax_gaps.csv", index=False)

    audit = {
        "survey": "ACS 2024 1-year person PUMS",
        "acs_source_url": SRC_URL,
        "acs_zip": str(args.zip),
        "acs_zip_bytes": args.zip.stat().st_size,
        "acs_zip_sha256": digest,
        "household_person_records": int(len(d)),
        "taxcalc_version": TC.version(),
        "tax_year": TC.TAX_YEAR,
        "policy": "current law, no reform",
        "replicate_weights": 80,
        "variance": "4/80 * sum((rep - full)^2)",
        "adjinc_applied": "every mapped dollar amount multiplied by ADJINC/1e6",
        "domain": "SERIALNO[4:6] == 'HU' (housing unit; group quarters excluded)",
        "relationship_codes": {
            "source": "PUMS_Data_Dictionary_2024.csv lines 1628-1647",
            "reference_person": REF_PERSON, "spouse": list(SPOUSE),
            "unmarried_partner_separate_returns": list(PARTNER),
            "child_relationships": list(CHILD_REL)},
        "tax_unit_rule": person_table.__doc__,
        "allocation_rule": (
            "each return's iitax and payroll tax allocated to its members in "
            "proportion to own positive WAGP+SEMP, equal shares when the "
            "return has no positive earnings"),
        "income_mapping": {
            "WAGP": "e00200 (wages, split head/spouse)",
            "SEMP": "e00900 (self-employment, split head/spouse; ACS SEMP includes farm)",
            "INTP": "positive part e00300 (taxable interest), negative part e02000 "
                    "(Schedule E). ACS INTP is interest, dividends AND net rental "
                    "income combined, so no separate dividend or rent treatment "
                    "is possible and no qualified-dividend rate applies.",
            "RETP": "e01500 and e01700 (pensions, treated as fully taxable)",
            "SSP": "e02400 (gross social security)",
            "OIP": "UNMAPPED: 'all other income' mixes unemployment compensation, "
                   "alimony, child support and veterans' payments with no way to "
                   "separate taxable from untaxable parts",
            "SSIP": "UNMAPPED (not taxable)",
            "PAP": "UNMAPPED (not taxable)",
            "itemized deductions": "UNMAPPED: ACS has none, so every return takes "
                                   "the standard deduction",
            "child care expenses": "UNMAPPED, so no child and dependent care credit"},
        "unit_diagnostics": diag,
        "group_definitions": {
            "mexico_born": "POBP == 303",
            "usborn_mexican_selfid": "NATIVITY == 1 & HISP == 2",
            "native_nh_white": "NATIVITY == 1 & HISP == 1 & RAC1P == 1",
            "all_native": "NATIVITY == 1"},
    }
    (OUT / "acs_audit.json").write_text(json.dumps(audit, indent=2))
    print(f"[done] wrote {OUT/'acs_tax_gaps.csv'}", flush=True)


if __name__ == "__main__":
    main()
