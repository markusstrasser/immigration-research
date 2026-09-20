"""Audit transfer national totals before any optional uniform raking sensitivity."""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from comparators import compare, read_comparators

HERE = Path(__file__).resolve().parent
PROGRAMS = {"snap": ("SPM_SNAPSUB", "unit"), "tanf": ("PAW_VAL", "person"),
            "ssi": ("SSI_VAL", "person"), "ui": ("UC_VAL", "person"),
            "social_security": ("SS_VAL", "person")}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def distribute(base, level, allocation, index, n_units, allocate):
    if level == "unit":
        return allocate(base, index, np.ones(len(index), bool), n_units)
    if allocation == "personal":
        return base.copy()
    units = np.bincount(index, weights=base, minlength=n_units)
    return allocate(units, index, np.ones(len(index), bool), n_units)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    fiscal = args.source_root.resolve() / "infra/immigration-fiscal"
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    helper = fiscal / "education_origin_fiscal_2026_09_19/builder.py"
    spec = importlib.util.spec_from_file_location("education_helper", helper)
    evidence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evidence)
    A, AL, arrival = evidence.configure(args.source_root.resolve())
    cps = fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d, w = state["d"], state["person_weights"][:, 0]
    index, n_units = state["index"], state["n_units"]
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    target = np.logical_or.reduce([state["group"][g] for g in AL.TARGETS]) & civilian
    groups = {"national_civilian": civilian, "mexican_observed_total": target,
              "other_residents": civilian & ~target}
    params_path = fiscal / "ledger_absolute_2026_09_17/params/params.json"
    params = json.loads(params_path.read_text())["underreporting"]
    macro_path = fiscal / "macro_closure_2026_09_19/derived/updated_account_components.csv"
    macro = pd.read_csv(macro_path)
    rows, diagnostics, checks = [], [], []
    for program, (column, level) in PROGRAMS.items():
        ratio = params["ratio_" + program]["value"]
        source = heads if level == "unit" else d
        base = source[column].to_numpy(float)
        if not np.isfinite(base).all() or (base < 0).any():
            raise ValueError(f"Invalid {program} benefit values")
        if level == "unit":
            diagnostics.append(dict(program=program,
                unique_spm_head_weighted_bn=float(base @ heads.pwwgt0.to_numpy()) / 1e9,
                wrong_repeated_person_weighted_bn=float(d[column].to_numpy() @ w) / 1e9))
        for allocation in ["shared", "personal"]:
            vector = distribute(base, level, allocation, index, n_units, A.ext.allocate)
            for group, mask in groups.items():
                total = float(vector[mask] @ w[mask]) / 1e9
                rows.append(dict(program=program, allocation=allocation, group=group,
                    baseline_bn=total, historical_ratio=ratio, after_U_bn=total * ratio,
                    U_signed_bn=-total * (ratio - 1)))
    table = pd.DataFrame(rows)
    for allocation in ["shared", "personal"]:
        for group in groups:
            got = table.loc[table.allocation.eq(allocation) & table.group.eq(group), "U_signed_bn"].sum()
            old = macro.loc[macro.allocation.eq(allocation) & macro.group.eq(group) & macro.component.eq("U"), "signed_bn"]
            if len(old) != 1 or abs(got - old.iloc[0]) > 1e-6:
                raise ValueError(f"Canonical U mismatch {allocation}/{group}: {got} vs {old.tolist()}")
            checks.append(dict(check=f"canonical U {allocation}/{group}", residual_bn=got-old.iloc[0]))
    table.to_csv(out / "program_totals.csv", index=False)
    pd.DataFrame(diagnostics).to_csv(out / "snap_unit_diagnostics.csv", index=False)
    official, months, arms, admin_sources = read_comparators(HERE, _data_paths.data_root(require_exists=False) / 'external/bea_nipa/Section3All_xls.xlsx')
    errors, components, sensitivities = compare(table, macro, official, arms)
    official.to_csv(out / "official_comparators.csv", index=False)
    months.to_csv(out / "snap_calendar2024_months.csv", index=False)
    errors.to_csv(out / "baseline_admin_errors.csv", index=False)
    components.to_csv(out / "raking_components.csv", index=False)
    sensitivities.to_csv(out / "raking_sensitivities.csv", index=False)
    if components.national_identity_residual_bn.abs().max() > 1e-9:
        raise ValueError("Raking national identity failed")
    for allocation, expected in [("shared",-234.339),("personal",-256.263)]:
        actual = sensitivities.loc[sensitivities.allocation.eq(allocation),"baseline_balance_bn"].iloc[0]
        if abs(actual-expected) > .001:
            raise ValueError(f"Macro closure baseline drifted: {allocation}: {actual}")
    sources = [*admin_sources, helper, cps, params_path, macro_path, fiscal / "ledger_absolute_2026_09_17/absolute_ledger.py",
               fiscal / "gen_ledger_extension_2026_09_16/extend_ledger.py",
               fiscal / "build/analyze_cps_fiscal_2025.py", HERE/"comparators.py", Path(__file__)]
    (out / "manifest.json").write_text(json.dumps(dict(checks=checks, files=[dict(path=str(p), sha256=sha(p)) for p in sources]), indent=2))
    print(table.loc[table.group.eq("national_civilian")].to_string(index=False))
    print(pd.DataFrame(diagnostics).to_string(index=False))
    print(sensitivities.drop(columns="interpretation").to_string(index=False))

if __name__ == "__main__":
    main()
