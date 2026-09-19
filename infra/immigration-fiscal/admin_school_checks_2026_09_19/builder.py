"""Test transported pupil exposure and the Texas income-tax assignment.

ACS direct child counts are unused cells of an already used source, not a wholly
independent administrative validation. No recalibration changes the fiscal model.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
AREAS = {0: "US", 6: "California", 48: "Texas"}


def fingerprint(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def public_k12(frame):
    return frame.SCH.eq(2) & frame.SCHG.between(2, 14)


def area_mask(frame, fips):
    return np.ones(len(frame), bool) if fips == 0 else frame.STATE.eq(fips).to_numpy()


def summarize(values, replicates):
    return {"estimate": float(values[0]), "se": float(np.sqrt(
        4 / replicates * np.square(values[1:] - values[0]).sum()))}


def acs_counts(path):
    weights = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]
    # The 2024 PUMS schema names this STATE, not the older ST field.
    columns = ["AGEP", "RELSHIPP", "SCH", "SCHG", "STATE", "HISP", *weights]
    totals, raw_rows = {}, 0
    with zipfile.ZipFile(path) as archive:
        members = [n for n in archive.namelist() if n.lower().endswith(".csv")
                   and "psam_pus" in n.lower()]
        if len(members) != 2:
            raise ValueError("Expected two national ACS person files")
        for member in members:
            for frame in pd.read_csv(archive.open(member), usecols=columns, chunksize=100000):
                raw_rows += len(frame)
                frame = frame[frame.RELSHIPP.lt(37)].copy()
                if frame.loc[frame.AGEP.between(5, 17), "SCH"].isna().any():
                    raise ValueError("Missing school attendance for age5-17")
                w = frame[weights].to_numpy(float)
                for fips in AREAS:
                    area = area_mask(frame, fips)
                    for origin in ["all", "hispanic"]:
                        use = area & (np.ones(len(frame), bool) if origin == "all" else frame.HISP.gt(1))
                        masks = {"children_5_17": frame.AGEP.between(5, 17),
                                 "public_k12_5_17": public_k12(frame) & frame.AGEP.between(5, 17),
                                 "public_k12_all_ages": public_k12(frame)}
                        for metric, mask in masks.items():
                            key = (fips, origin, metric)
                            totals[key] = totals.get(key, np.zeros(81)) + w[use & mask].sum(axis=0)
    if raw_rows != 3422888:
        raise ValueError(f"Unexpected ACS2024 raw row count {raw_rows}")
    return totals


def run(root, out):
    fiscal = root / "infra/immigration-fiscal"
    sys.path.insert(0, str(fiscal / "gen_ledger_extension_2026_09_16"))
    import extend_ledger as ext
    cps = fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    acs = root / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
    sources = json.loads((HERE / "sources.json").read_text())
    if fingerprint(cps) != ext.CPS_SHA:
        raise ValueError("CPS source hash changed")
    if fingerprint(acs) != sources["acs_sha256"]:
        raise ValueError("ACS source hash changed")
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d, w = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    counts = acs_counts(acs)
    rows, comparisons = [], []
    ratio = ext.PUPIL_RATIO_NATIVE_ACS
    for fips, area in AREAS.items():
        geo = np.ones(len(d), bool) if fips == 0 else d.GESTFIPS.eq(fips).to_numpy()
        for origin in ["all", "hispanic"]:
            use = civilian & geo & d.A_AGE.between(5, 17).to_numpy()
            if origin == "hispanic":
                use &= d.PEHSPNON.eq(1).to_numpy()
            modeled = w[use].sum(axis=0) * ratio
            rows.append(dict(source="CPS2025_model", area=area, origin=origin,
                             metric="public_k12_5_17", **summarize(modeled, 160)))
            for metric in ["children_5_17", "public_k12_5_17", "public_k12_all_ages"]:
                rows.append(dict(source="ACS2024", area=area, origin=origin,
                                 metric=metric, **summarize(counts[fips, origin, metric], 80)))
            observed = counts[fips, origin, "public_k12_5_17"][0]
            comparisons.append(dict(area=area, origin=origin, model=modeled[0],
                acs=observed, difference=modeled[0] - observed,
                relative_error=modeled[0] / observed - 1,
                acs_direct_public_share=observed / counts[fips, origin, "children_5_17"][0],
                model_public_share=ratio))
    texas = civilian & d.GESTFIPS.eq(48).to_numpy()
    texas_tax = dict(unweighted_records=int(texas.sum()),
        records_with_nonzero_liability=int(d.loc[texas, "STATETAX_A"].ne(0).sum()),
        assigned_state_income_tax_bn=float(d.loc[texas, "STATETAX_A"] @ w[texas, 0]) / 1e9)
    if texas_tax["records_with_nonzero_liability"] != 0:
        raise ValueError(f"Nonzero Texas state-tax assignment requires investigation: {texas_tax}")
    out.mkdir(exist_ok=True, parents=True)
    pd.DataFrame(rows).to_csv(out / "pupil_counts.csv", index=False)
    pd.DataFrame(comparisons).to_csv(out / "pupil_comparison.csv", index=False)
    bridges = []
    for control in sources["administrative_controls"]:
        observed = counts[control["fips"], control["origin"], "public_k12_all_ages"][0]
        administrative = control["total"] - control["excluded_early_education"]
        bridges.append(dict(**control, acs_all_age_public_k12=observed,
            administrative_k12=administrative, relative_error=observed / administrative - 1,
            boundary="Annual-average household ACS vs fall membership; TK classification can differ"))
    pd.DataFrame(bridges).to_csv(out / "administrative_grade_bridge.csv", index=False)
    account_path = fiscal / "macro_closure_2026_09_19/derived/updated_account_components.csv"
    account = pd.read_csv(account_path)
    sensitivity = []
    for allocation in ["personal", "shared"]:
        chosen = account[account.allocation.eq(allocation) & account.group.eq("mexican_observed_total")]
        school = -chosen.loc[chosen.component.isin(["school", "K", "D"]), "signed_bn"].sum()
        baseline = chosen.signed_bn.sum()
        for proxy in ["all", "hispanic"]:
            share = counts[0, proxy, "public_k12_5_17"][0] / counts[0, proxy, "children_5_17"][0]
            change = -school * (share / ratio - 1)
            sensitivity.append(dict(allocation=allocation, proxy=proxy, baseline_balance_bn=baseline,
                school_operating_capital_differential_bn=school, alternative_public_share=share,
                balance_change_bn=change, scenario_balance_bn=baseline + change,
                rule="Uniform rate substitution for every child before allocation; scenario, not ethnic calibration"))
    pd.DataFrame(sensitivity).to_csv(out / "school_rate_sensitivity.csv", index=False)
    inputs = [cps, acs, account_path, Path(__file__), HERE / "sources.json",
              Path(ext.__file__), Path(ext.base.__file__), ext.HERE / "state_parameters.csv"]
    audit = dict(inputs=[dict(path=str(p), sha256=fingerprint(p)) for p in inputs],
        texas_tax=texas_tax, fixed_public_share=ratio,
        scope="CPS Mar2025 children versus ACS2024 annual-average households; conditional sampling SEs",
        source_reuse="ACS adult household exposure set ratio; direct state/child counts are unused cells",
        limits="No ethnic fiscal recalibration; Hispanic is not Mexican lineage; timing differs")
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(pd.DataFrame(comparisons).to_string(index=False))
    print(json.dumps(texas_tax))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    run(args.source_root, args.out)
