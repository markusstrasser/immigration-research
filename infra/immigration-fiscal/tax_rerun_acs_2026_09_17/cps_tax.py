#!/usr/bin/env python3
"""CPS ASEC 2025 (income year 2024) tax units run through Tax-Calculator.

Builds the CPS state exactly as the ACS earnings-replication lane does (imports
the held `extend_ledger` builder), forms tax units from the Census tax-unit
identifier `TAX_ID`, runs the Policy Simulation Library Tax-Calculator under
2024 current law, allocates each return's `iitax` and payroll tax back to
persons, and compares the result with the Census Bureau's own modelled
`FEDTAX_AC` and `FICA` (the anchor gate).

Writes derived/cps_tax_cells.csv, derived/cps_tax_gaps.csv,
derived/cps_anchor.csv and derived/cps_audit.json. Reads nothing outside the
held CPS zip and the two sibling lanes; writes only inside this lane.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ACS_LANE = FISCAL / "acs_earnings_replication_2026_09_17"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(FISCAL / "build"))
sys.path.insert(0, str(ACS_LANE))

import extend_ledger as ext  # noqa: E402

# Person fields the base generator does not read. PERSON is consumed by
# prepare() as usecols at call time, so appending here is enough; nothing on
# disk is modified.
EXTRA = ["PTOTVAL", "TAX_ID", "FILESTAT", "DEP_STAT", "A_LINENO",
         "SEMP_VAL", "FRSE_VAL", "INT_VAL", "DIV_VAL", "RNT_VAL",
         "PNSN_VAL", "ANN_VAL", "A_ENRLW"]
for _f in EXTRA:
    if _f not in ext.base.PERSON:
        ext.base.PERSON.append(_f)

import common as C  # noqa: E402  (ACS lane's shared estimator machinery)
import cps_gaps as CG  # noqa: E402  (ACS lane's group definitions)
import shared  # noqa: E402
import taxcalc_io as TC  # noqa: E402
import units as U  # noqa: E402

CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
OUT = HERE / "derived"

# SOI Table 1.4: qualified dividends run about three quarters of ordinary
# dividends. ASEC reports one combined dividend amount, so a share is assumed.
QDIV_SHARE = 0.75

GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
          "usborn_mexican_selfid", "third_plus_nh_white", "native_nh_white",
          "all_native"]


# --------------------------------------------------------------------------
def person_table(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Assign every CPS person to exactly one tax return.

    Structure verified on this file (pppub25.csv, 142,125 persons): inside a
    Census TAX_ID the non-dependent persons number 0, 1 or 2 and share one
    FILESTAT, 1/2/3 meaning two persons filing jointly and 4/5/6 one person;
    no TAX_ID mixes a filer with a non-filing non-dependent. The guards below
    re-assert this at run time.

    A dependent with positive own earnings files his own single return with
    DSI=1 and is still claimed on the TAX_ID return. This is the same rule the
    ACS arm applies, and it keeps a working dependent's payroll tax inside the
    account; the Census model's own filer flag (FILESTAT != 6 for a dependent)
    is reported beside it as agreement diagnostics, not used.
    """
    n = len(d)
    row = np.arange(n)
    is_dep = (d.DEP_STAT > 0).to_numpy()
    earn = (d.WSAL_VAL.to_numpy(dtype=float) + d.SEMP_VAL.to_numpy(dtype=float)
            + d.FRSE_VAL.to_numpy(dtype=float))
    own_return = is_dep & (earn > 0)
    census_depfiler = is_dep & (d.FILESTAT != 6).to_numpy()

    # ---- structural guards on the Census tax-unit identifier --------------
    core = d.loc[~is_dep]
    per_unit = core.groupby("TAX_ID").FILESTAT
    if per_unit.nunique().max() > 1:
        raise SystemExit("[BLOCKED] non-dependents inside one TAX_ID disagree on FILESTAT")
    size = core.groupby("TAX_ID").size()
    joint = per_unit.first().isin([1, 2, 3])
    if not ((size == 2) == joint).all():
        raise SystemExit("[BLOCKED] joint filing status without exactly two non-dependents")
    if size.max() > 2:
        raise SystemExit("[BLOCKED] TAX_ID with more than two non-dependents")

    claim_key = "U" + d.TAX_ID.astype(str).to_numpy()
    ret_key = np.where(own_return, "D" + row.astype(str), claim_key)
    keys = pd.Index(sorted(set(claim_key) | set(ret_key)))
    ret = pd.Categorical(ret_key, categories=keys).codes.astype(np.int64)
    claim = pd.Categorical(claim_key, categories=keys).codes.astype(np.int64)

    # roles on the claiming return: non-dependents ordered by line number
    claim_role = np.full(n, 2)
    nd = np.where(~is_dep)[0]
    order = (pd.DataFrame({"u": claim[nd], "ln": d.A_LINENO.to_numpy()[nd]})
             .sort_values(["u", "ln"]).groupby("u").cumcount())
    seq = np.zeros(len(nd), dtype=int)
    seq[order.index.to_numpy()] = order.to_numpy()
    claim_role[nd] = np.where(seq == 1, 1, 0)

    ret_role = np.where(own_return, 0, claim_role)

    fs = d.FILESTAT.to_numpy()
    mars = np.where(own_return, 1,
                    np.where(np.isin(fs, [1, 2, 3]), 2, np.where(fs == 4, 4, 1)))
    dsi = own_return.astype(int)

    age = d.A_AGE.to_numpy()
    # statutory EITC qualifying child: under 19, or under 24 and a student.
    # A_ENRLW == 1 is "enrolled last week" (universe 16-24).
    eic_child = (age < 19) | ((age < 24) & (d.A_ENRLW.to_numpy() == 1))
    p = pd.DataFrame({"ret_unit": ret, "ret_role": ret_role,
                      "claim_unit": claim, "claim_role": claim_role,
                      "age": age, "mars": mars, "dsi": dsi,
                      "earn": earn, "eic_child": eic_child})
    p = U.promote_headless(p)
    diag = {
        "returns": int(len(keys)),
        "dependent_own_returns": int(own_return.sum()),
        "census_dependent_filers": int(census_depfiler.sum()),
        "rule_agrees_with_census_flag": float((own_return == census_depfiler).mean()),
        "headless_returns_promoted": int((p.dsi.to_numpy() != dsi).sum()),
    }
    return p, diag


def income_map(d: pd.DataFrame, arm: str) -> dict[str, np.ndarray]:
    """Person-level ASEC dollars mapped onto taxcalc input variables.

    `full` uses every separately reported ASEC income type. `acsmap` collapses
    them onto the blocks the ACS questionnaire actually has, so the
    cross-survey comparison is not confounded by the CPS income supplement's
    finer detail. Both are reported.
    """
    f = lambda c: d[c].to_numpy(dtype=float)  # noqa: E731
    wage, semp, frse = f("WSAL_VAL"), f("SEMP_VAL"), f("FRSE_VAL")
    pens = f("PNSN_VAL") + f("ANN_VAL")
    if arm == "full":
        return {"e00200": wage, "e00900": semp, "e02100": frse,
                "e00300": f("INT_VAL"),
                "e00600": f("DIV_VAL"), "e00650": QDIV_SHARE * f("DIV_VAL"),
                "e02000": f("RNT_VAL"),
                "e01500": pens, "e01700": pens,
                "e02400": f("SS_VAL"), "e02300": f("UC_VAL")}
    if arm == "acsmap":
        combined = f("INT_VAL") + f("DIV_VAL") + f("RNT_VAL")
        return {"e00200": wage, "e00900": semp + frse,
                "e00300": np.clip(combined, 0, None),
                "e02000": np.clip(combined, None, 0),
                "e01500": pens, "e01700": pens,
                "e02400": f("SS_VAL")}
    raise SystemExit(f"[BLOCKED] unknown arm {arm}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cps-zip", type=Path, default=CPS_ZIP)
    args = ap.parse_args()
    if not args.cps_zip.exists():
        raise SystemExit(f"[BLOCKED] CPS zip not found: {args.cps_zip}")
    OUT.mkdir(parents=True, exist_ok=True)

    state = ext.build(argparse.Namespace(cps_zip=args.cps_zip))
    d = state["d"]
    weights = state["person_weights"]
    groups = CG.build_groups(d, state["group"])
    masks = {k: groups[k] for k in GROUPS}
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()

    p, diag = person_table(d)
    n_ret = int(p.ret_unit.max()) + 1
    ret = p.ret_unit.to_numpy()
    earn = p.earn.to_numpy()
    band = C.bands_of(d.A_AGE.to_numpy())

    person: dict[str, np.ndarray] = {}
    arms = {}
    eic_child = p.eic_child.to_numpy()
    for arm in ["full", "full_salt", "acsmap", "full_eic18"]:
        inc = income_map(d, "acsmap" if arm == "acsmap" else "full")
        if arm == "full_salt":
            # State income tax as modelled by the Census Bureau, offered as the
            # deductible state/local income tax; taxcalc applies the SALT cap.
            inc = dict(inc, e18400=d.STATETAX_A.clip(lower=0).to_numpy(dtype=float))
        frame = U.build_frame(p, inc, n_ret,
                              eic_child=None if arm == "full_eic18" else eic_child)
        res = TC.run(frame)
        person[f"iitax_{arm}"] = U.allocate(ret, earn, res["iitax"])
        person[f"payroll_{arm}"] = U.allocate(ret, earn, res["payroll_employee_equiv"])
        if arm == "full":
            person["eitc_taxcalc"] = U.allocate(ret, earn, res["eitc"])
            person["actc_taxcalc"] = U.allocate(ret, earn, res["c11070"])
            person["ctc_nonref_taxcalc"] = U.allocate(ret, earn, res["c07220"])
        arms[arm] = {"returns": int(len(frame)),
                     "iitax_unweighted_sum": float(res["iitax"].sum()),
                     "payroll_employee_unweighted_sum": float(res["payroll_employee_equiv"].sum()),
                     "itemizing_returns": int((res["c04470"] > 0).sum())}
        print(f"[taxcalc] CPS arm {arm}: {len(frame):,} returns", flush=True)

    # Census tax model, as recorded and on this lane's allocation rule
    census_unit = np.bincount(ret, weights=d.FEDTAX_AC.to_numpy(dtype=float),
                              minlength=n_ret)
    person["FEDTAX_AC"] = d.FEDTAX_AC.to_numpy(dtype=float)
    person["FEDTAX_AC_alloc"] = U.allocate(ret, earn, census_unit)
    person["FICA"] = d.FICA.to_numpy(dtype=float)
    person["eitc_census"] = d.EIT_CRED.to_numpy(dtype=float)
    person["actc_census"] = d.ACTC_CRD.to_numpy(dtype=float)
    person["ctc_nonref_census"] = d.CTC_CRD.to_numpy(dtype=float)
    person["fedtax_before_credits_census"] = d.FEDTAX_BC.to_numpy(dtype=float)

    anchor = shared.anchor_table(person, masks, civ, weights[:, 0],
                                 union=["mexico_born", "mexican_second_gen",
                                        "mexican_third_plus_selfid"])
    anchor.to_csv(OUT / "cps_anchor.csv", index=False)
    r_union = float(anchor.loc[anchor.group.eq("union_of_targets"), "ratio_iitax"].iloc[0])
    r_white = float(anchor.loc[anchor.group.eq("native_nh_white"), "ratio_iitax"].iloc[0])
    gate = bool(0.85 <= r_union <= 1.15 and 0.85 <= r_white <= 1.15)
    print(f"[gate1] union {r_union:.4f} white {r_white:.4f} -> "
          f"{'PASS' if gate else 'FAIL'}", flush=True)

    civ_masks = {k: (m & civ) for k, m in masks.items()}
    rows, gaps = shared.cells_and_gaps(civ_masks, band, weights, person,
                                       "national", denom=160, survey="CPS")
    pd.DataFrame(rows).to_csv(OUT / "cps_tax_cells.csv", index=False)
    pd.DataFrame(gaps).to_csv(OUT / "cps_tax_gaps.csv", index=False)

    audit = {
        "survey": "CPS ASEC 2025 (income year 2024)",
        "cps_zip": str(args.cps_zip),
        "cps_sha256": ext.base.sha(args.cps_zip),
        "person_rows": int(len(d)),
        "taxcalc_version": TC.version(),
        "tax_year": TC.TAX_YEAR,
        "policy": "current law, no reform",
        "replicate_weights": 160,
        "variance": "4/160 * sum((rep - full)^2)",
        "tax_unit_rule": (
            "return keyed by the Census TAX_ID; inside it the non-dependents "
            "are head and (FILESTAT 1/2/3) spouse, everyone with DEP_STAT>0 is "
            "a dependent; a dependent with positive own earnings files a "
            "separate single return with DSI=1 and is still claimed on the "
            "TAX_ID return; FILESTAT 1/2/3 -> MARS 2, 4 -> MARS 4, 5/6 -> MARS 1"),
        "allocation_rule": (
            "each return's iitax and payroll tax allocated to its members in "
            "proportion to own positive WSAL_VAL+SEMP_VAL+FRSE_VAL, equal "
            "shares when the return has no positive earnings"),
        "qualified_dividend_share": QDIV_SHARE,
        "unit_diagnostics": diag,
        "arms": arms,
        "gate1": {"union_ratio": r_union, "white_ratio": r_white,
                  "band": [0.85, 1.15], "pass": gate},
        "domain": "civilian household population: PRPERTYP==2 | A_AGE<15",
        "group_definitions": "acs_earnings_replication_2026_09_17/cps_gaps.py build_groups",
    }
    (OUT / "cps_audit.json").write_text(json.dumps(audit, indent=2))
    print(f"[done] wrote {OUT/'cps_tax_gaps.csv'}", flush=True)


if __name__ == "__main__":
    main()
