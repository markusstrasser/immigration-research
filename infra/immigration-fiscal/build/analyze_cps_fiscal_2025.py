#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2", "pandas>=2"]
# ///
"""Same-source 2024 tax/transfer accounts, with explicit resource-unit allocation.

Native-First: pandas reads the official CSV ZIP; NumPy computes the published
160-replicate SDR estimator. No tax calculator, status imputation, or warehouse
mutation. Output is an accounting scenario, never actual tax collection or a
complete fiscal effect. Run with --help for required raw/output locations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

PERSON = [
    "PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
    "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDTHSP",
    "PEINUSYR", "MARSUPWT", "SPM_ID", "SPM_HEAD", "SPM_NUMPER",
    "SPM_NUMADULTS", "SPM_WEIGHT", "FEDTAX_AC", "FEDTAX_BC", "ACTC_CRD",
    "CTC_CRD", "EIT_CRED", "STATETAX_A", "STATETAX_B", "FICA", "PEARNVAL",
    "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL",
    "SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL", "SPM_SCHLUNCH",
    "SPM_BBSUBVAL", "SPM_CAPHOUSESUB", "SPM_FEDTAX", "SPM_FICA",
    "PRIV", "PUB", "MCAID", "MCARE", "CAID", "VET_YN", "MIL", "CHAMPVA",
]
TAX = {"payroll": "FICA", "federal_before_refundable": "FEDTAX_BC",
       "federal_after_refundable": "FEDTAX_AC", "federal_eitc": "EIT_CRED",
       "federal_actc": "ACTC_CRD", "state_after_credits": "STATETAX_A"}
CASH = {"social_security": "SS_VAL", "ssi": "SSI_VAL",
        "cash_assistance": "PAW_VAL", "unemployment": "UC_VAL", "veterans": "VET_VAL"}
NONCASH = {"snap": "SPM_SNAPSUB", "energy": "SPM_ENGVAL", "wic": "SPM_WICVAL",
           "school_lunch": "SPM_SCHLUNCH", "broadband": "SPM_BBSUBVAL"}
REPS = [f"pwwgt{i}" for i in range(161)]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def estimate(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    den = weights.sum(axis=0)
    if (den <= 0).any():
        raise ValueError("Nonpositive estimate denominator, including a replicate")
    return (values @ weights) / den


def summarize(est: np.ndarray) -> dict:
    se = float(np.sqrt(4 / 160 * np.square(est[1:] - est[0]).sum()))
    return {"estimate": float(est[0]), "se_sampling": se,
            "ci95_sampling_low": float(est[0] - 1.96 * se),
            "ci95_sampling_high": float(est[0] + 1.96 * se)}


def health_model_for_metric(metric: str) -> str:
    for prefix in ("balance_excluding_school_lunch_after_health_", "balance_after_health_", "health_"):
        if metric.startswith(prefix):
            return metric.removeprefix(prefix)
    return ""


def allocate(unit_total: np.ndarray, unit_index: np.ndarray,
             eligible: np.ndarray, n_units: int) -> np.ndarray:
    """Allocate unit totals once; fail if any nonzero unit lacks a recipient."""
    count = np.bincount(unit_index, weights=eligible.astype(float), minlength=n_units)
    if np.any((count == 0) & (unit_total != 0)):
        raise ValueError("Nonzero resource unit without allocation recipient")
    amount = np.divide(unit_total, count, out=np.zeros_like(unit_total), where=count > 0)
    result = amount[unit_index] * eligible
    if not np.allclose(np.bincount(unit_index, weights=result, minlength=n_units), unit_total):
        raise ValueError("Resource allocation did not conserve each source unit")
    return result


def prepare(path: Path):
    with zipfile.ZipFile(path) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"))
    r = r.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if d[REPS].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    delta = (d.MARSUPWT / 100 - d.pwwgt0).abs().max()
    if delta >= .01:
        raise ValueError(f"Full-weight merge validation failed: {delta}")
    if not (d.FEDTAX_AC == d.FEDTAX_BC - d.ACTC_CRD - d.EIT_CRED).all():
        raise ValueError("Federal refundable-credit identity failed")
    if d[PERSON].isna().any().any():
        raise ValueError("Missing selected field; do not silently replace with zero")
    d = d.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    units = d.groupby("SPM_ID", sort=True)
    if not units.SPM_HEAD.sum().eq(1).all():
        raise ValueError("SPM unit lacks exactly one head")
    if not units.size().eq(units.SPM_NUMPER.first()).all():
        raise ValueError("SPM unit size mismatch")
    constant = ["SPM_WEIGHT", "SPM_NUMPER", "SPM_NUMADULTS", *NONCASH.values(),
                "SPM_CAPHOUSESUB", "SPM_FEDTAX", "SPM_FICA"]
    if not units[constant].nunique().eq(1).all().all():
        raise ValueError("Repeated SPM unit fields disagree")
    heads = d.loc[d.SPM_HEAD.eq(1)].set_index("SPM_ID").sort_index()
    if (heads.SPM_WEIGHT / 100 - heads.pwwgt0).abs().max() >= .01:
        raise ValueError("SPM weight differs from head's full weight")
    if not units.FEDTAX_AC.sum().eq(heads.SPM_FEDTAX).all():
        raise ValueError("Person tax amounts do not reproduce SPM federal tax")
    if not units.FICA.sum().eq(heads.SPM_FICA).all():
        raise ValueError("Person payroll amounts do not reproduce SPM payroll tax")
    index = pd.Categorical(d.SPM_ID, categories=heads.index).codes
    validation = {"person_rows": len(d), "replicate_rows": len(r), "spm_units": len(heads),
                  "max_full_weight_difference": float(delta),
                  "negative_replicate_weights": int((d[REPS[1:]] < 0).sum().sum()),
                  "federal_credit_identity": True, "unit_fields_constant": True,
                  "source_tax_sums_match_unit_fields": True}
    return d, heads, index, validation


def run(args):
    args.output.mkdir(parents=True, exist_ok=True)
    d, heads, index, validation = prepare(args.cps_zip)
    n_units = len(heads)
    units = d.groupby("SPM_ID", sort=True)
    totals = {k: units[v].sum().to_numpy(dtype=float) for k, v in (TAX | CASH).items()}
    totals.update({k: heads[v].to_numpy(dtype=float) for k, v in NONCASH.items()})
    totals["capped_housing_resource_value"] = heads.SPM_CAPHOUSESUB.to_numpy(dtype=float)
    totals["school_age_children_5_17"] = np.bincount(index, weights=d.A_AGE.between(5, 17), minlength=n_units)
    totals["modeled_tax_total"] = totals["payroll"] + totals["federal_after_refundable"] + totals["state_after_credits"]
    totals["state_positive_liability"] = d.STATETAX_A.clip(lower=0).groupby(d.SPM_ID).sum().to_numpy(dtype=float)
    totals["state_net_refund"] = (-d.STATETAX_A).clip(lower=0).groupby(d.SPM_ID).sum().to_numpy(dtype=float)
    totals["modeled_positive_liability"] = totals["payroll"] + totals["federal_before_refundable"] + totals["state_positive_liability"]
    totals["modeled_refund_amount"] = totals["federal_eitc"] + totals["federal_actc"] + totals["state_net_refund"]
    if not np.allclose(totals["modeled_positive_liability"] - totals["modeled_refund_amount"], totals["modeled_tax_total"]):
        raise ValueError("Tax liability/refund decomposition failed")
    totals["selected_cash_total"] = sum(totals[k] for k in CASH)
    totals["selected_noncash_total"] = sum(totals[k] for k in NONCASH)
    totals["cash_tax_balance"] = totals["modeled_tax_total"] - totals["selected_cash_total"]
    totals["cash_noncash_tax_balance"] = totals["cash_tax_balance"] - totals["selected_noncash_total"]
    # Eligibility and compliance stress inputs are explicit upper amounts, not actual noncompliance.
    noncit = d.PRCITSHP.eq(5)
    totals["noncitizen_modeled_payroll"] = (d.FICA * noncit).groupby(d.SPM_ID).sum().to_numpy(dtype=float)
    totals["federal_refundable_credits"] = totals["federal_eitc"] + totals["federal_actc"]
    # Generation groups (added 2026-09-16 for the Mexican-origin-by-generation memo): parents' birthplace
    # codes 57/60/66/69/73/78 are the US and its territories; "third-plus" pools every native-born
    # person with two US-born parents; Mexican third-plus is self-identified (PRDTHSP 1).
    native = d.PRCITSHP.isin([1, 2, 3])
    us_area = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    group = {
        "all_native": native.to_numpy(),
        "mexico_born": (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy(),
        "all_foreign_born": d.PRCITSHP.isin([4, 5]).to_numpy(),
        "noncitizens": noncit.to_numpy(),
        "foreign_born_entry_2022_2024": (d.PRCITSHP.isin([4, 5]) & d.PEINUSYR.eq(28)).to_numpy(),
        "all_second_gen": (native & ~parents_us).to_numpy(),
        "all_third_plus": (native & parents_us).to_numpy(),
        "mexican_second_gen": (native & parent_mexico).to_numpy(),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)).to_numpy(),
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy(),
    }
    base = (d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2)).to_numpy()
    health = {}
    if args.meps_zip is not None:
        from meps_health_transport_2024 import read_meps, donor_model
        if args.meps_sas is None:
            raise ValueError("MEPS data requires its SAS layout")
        medical, anchors = read_meps(args.meps_zip, args.meps_sas)
        validation["meps_published_population_anchors"] = anchors
        # Both coverage variables explicitly code infants born after the reference year as zero.
        alive_reference = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
        if (d.loc[~alive_reference, "A_AGE"] > 0).any():
            raise ValueError("Unexpected non-infant with post-reference-year insurance code")
        validation["post_reference_year_infants_no_health_exposure"] = int((~alive_reference).sum())
        for insured in (False, True):
            label = "age_birth_insurance" if insured else "age_birth"
            cells, codes, cov = donor_model(medical, d, insured)
            cells.to_csv(args.output / f"meps_{label}_cells.csv", index=False)
            np.save(args.output / f"meps_{label}_covariance.npy", cov)
            mean = cells.mean_public_paid.to_numpy()
            counts = np.zeros((n_units, len(cells)))
            # Exposure counts, including children, are assigned to their own current birth/age cell.
            for j in range(len(cells)):
                counts[:, j] = np.bincount(index, weights=((codes == j) & alive_reference), minlength=n_units)
            totals[f"health_{label}"] = counts @ mean
            totals[f"balance_after_health_{label}"] = totals["cash_noncash_tax_balance"] - counts @ mean
            # Total current school spending includes food services. A separate base
            # removes the SPM lunch resource before combining that school scenario.
            # It does not claim exact matching of lunch recipients to ACS pupils.
            totals[f"balance_excluding_school_lunch_after_health_{label}"] = (
                totals[f"balance_after_health_{label}"] + totals["school_lunch"]
            )
            health[label] = {"counts": counts, "covariance": cov, "minimum_cell_n": int(cells.n.min())}
    person_weights = d[REPS].to_numpy()
    # Unit-head weights apply to all allocated unit members, conserving weighted dollars
    # as well as raw unit totals. This is a resource-unit estimator, not person-weight CPS totals.
    unit_weights = heads[REPS].to_numpy()[index]
    rows, reps, contrasts = [], {}, []
    adults = d.A_AGE.ge(18).to_numpy()
    n_adults = np.bincount(index, weights=adults, minlength=n_units)
    validation["child_only_units_retained_with_children"] = int((n_adults == 0).sum())
    for allocation_name, eligible in [
        ("equal_all_members", np.ones(len(d), dtype=bool)),
        ("equal_adults_18plus", adults | (n_adults[index] == 0)),
    ]:
        allocated = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}
        exposure = {label: np.stack([allocate(info["counts"][:, j], index, eligible, n_units)
                                     for j in range(info["counts"].shape[1])])
                    for label, info in health.items()}
        for weighting, weights in [("resource_unit_head", unit_weights), ("person", person_weights)]:
            health_q = {}
            for name, mask in group.items():
                use = base & mask
                for label, matrix in exposure.items():
                    health_q[name, label] = matrix[:, use] @ weights[use, 0] / weights[use, 0].sum()
                # One matrix multiplication per domain; every replicate recomputes the ratio.
                metrics = list(allocated)
                values = np.stack([allocated[k][use] for k in metrics])
                estimates_all = estimate(values, weights[use])
                for metric, estimates in zip(metrics, estimates_all):
                    key = f"{allocation_name}|{weighting}|{name}|{metric}"
                    reps[key] = estimates.tolist()
                    result = summarize(estimates)
                    label = health_model_for_metric(metric)
                    if label in health:
                        q = health_q[name, label]
                        extra = float(q @ health[label]["covariance"] @ q)
                        se = float(np.sqrt(result["se_sampling"] ** 2 + extra))
                        result.update(se_sampling_cps_and_meps=se,
                                      ci95_sampling_combined_low=float(estimates[0] - 1.96 * se),
                                      ci95_sampling_combined_high=float(estimates[0] + 1.96 * se))
                    rows.append({"allocation": allocation_name, "weighting": weighting, "group": name,
                                 "metric": metric, "n": int(use.sum()), "weighted_adults": float(weights[use, 0].sum()),
                                 **result})
            for metric in allocated:
                stem = f"{allocation_name}|{weighting}|"
                diff = np.array(reps[stem + "all_native|" + metric]) - reps[stem + "mexico_born|" + metric]
                result = summarize(diff)
                label = health_model_for_metric(metric)
                if label in health:
                    q = health_q["all_native", label] - health_q["mexico_born", label]
                    extra = float(q @ health[label]["covariance"] @ q)
                    se = float(np.sqrt(result["se_sampling"] ** 2 + extra))
                    result.update(se_sampling_cps_and_meps=se,
                                  ci95_sampling_combined_low=float(diff[0] - 1.96 * se),
                                  ci95_sampling_combined_high=float(diff[0] + 1.96 * se))
                contrasts.append({"allocation": allocation_name, "weighting": weighting,
                                  "contrast": "all_native_minus_mexico_born", "metric": metric, **result})
    # Separate directly reported/modelled person components; no attribution of a joint tax return.
    for name, mask in group.items():
        use = base & mask
        for metric, values in {"earnings": d.PEARNVAL, "own_modeled_payroll": d.FICA,
                               "medicaid_or_means_tested_coverage": d.MCAID.eq(1).astype(float),
                               "medicare_coverage": d.MCARE.eq(1).astype(float)}.items():
            rows.append({"allocation": "own_person", "weighting": "person", "group": name,
                         "metric": metric, "n": int(use.sum()), "weighted_adults": float(person_weights[use, 0].sum()),
                         **summarize(estimate(values.to_numpy()[use], person_weights[use]))})
    pd.DataFrame(rows).to_csv(args.output / "accounts.csv", index=False)
    pd.DataFrame(contrasts).to_csv(args.output / "contrasts.csv", index=False)
    (args.output / "replicate_estimates.json").write_text(json.dumps(reps) + "\n")
    meta = {"source": str(args.cps_zip), "source_sha256": sha(args.cps_zip), "source_bytes": args.cps_zip.stat().st_size,
            "income_year": 2024, "survey_year": 2025, "age_basis": "interview age 25–64, civilian household members",
            "status": "No unauthorized status observed; noncitizens include lawful residents",
            "ledger": "Modeled federal/state income and personal payroll taxes minus selected cash and noncash transfers",
            "not_in_core_balance": ["health expenditures", "school operating expenditures", "employer payroll contribution",
                               "sales/excise/property/corporate taxes", "public pensions beyond Social Security",
                               "administration/public goods/security", "tax compliance and exact credit eligibility"],
            "housing": "Capped SPM housing resource value reported separately, not government fiscal expenditure",
            "school_combination": "The separate balance_excluding_school_lunch_after_health metrics remove SPM lunch before a total-school-spending scenario that includes food services; original balance_after_health retains lunch. These are distinct ledgers, not an exact recipient-level overlap correction.",
            "children": "All family members included before allocating; child count is not enrollment or cost",
            "sampling": "CPS 160 SDR replicates, 4/160; systematic model, coverage and allocation error excluded",
            "weights": "Head weighting conserves estimated unit totals; person weighting is a distinct allocation sensitivity",
            "validation": validation}
    if health:
        meta["health_transport"] = {"source": str(args.meps_zip), "source_sha256": sha(args.meps_zip),
            "income_year": 2024, "public_payers": "Medicare, Medicaid, VA, TRICARE, other federal and state/local",
            "models": {k: {"minimum_cell_n": v["minimum_cell_n"]} for k, v in health.items()},
            "limits": "US-born/not-US-born donors; Mexico health is modeled, not measured. Interview age proxies year-end age; post-reference-year infants have zero health exposure. Institutional costs and budget administration excluded. Means from both surveys treated independent for combined first-order sampling variance; transport bias excluded."}
    (args.output / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(validation))
    print(pd.DataFrame(contrasts).query("metric == 'cash_noncash_tax_balance'").to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cps-zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--meps-zip", type=Path)
    parser.add_argument("--meps-sas", type=Path)
    run(parser.parse_args())
