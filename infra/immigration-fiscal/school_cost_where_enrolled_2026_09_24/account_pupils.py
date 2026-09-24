"""Where the account puts the group's pupils, and the per-pupil price its education key already embeds.

Rebuilds the `school` component of school_enrollment_2026_09_20 (the operating-school half of the
explorer's `education_mix` key) state by state: canonical March 2025 CPS records, October 2024 public
K-12 rates by age x origin cell (that lane's derived/national_rates.csv), each pupil priced at its
state's Census ASSF FY2024 Table 8 current spending per pupil. Imports the canonical builders
read-only (no bytecode written); gates the national totals against updated_account_components.csv
and transported_pupils.csv before writing derived/account_pupils_by_state.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/account_pupils.py
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SCHOOL = FISCAL / "school_enrollment_2026_09_20"
sys.path.insert(0, str(FISCAL / "ledger_absolute_2026_09_17"))
sys.path.insert(0, str(SCHOOL))
import absolute_ledger as al  # noqa: E402
from measurement import cells, origin_masks, sha  # noqa: E402

ext = al.ext
TOL_BN = 1e-6


def main():
    cps = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    if sha(cps) != ext.CPS_SHA:
        raise SystemExit("[BLOCKED] March CPS release checksum differs")
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"].copy()
    d["PRTAGE"] = d.A_AGE
    civil = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    target = origin_masks(d)["target"]
    union = np.logical_or.reduce([state["group"][g] for g in al.TARGETS])
    if not np.array_equal(target, union):
        raise SystemExit("[BLOCKED] canonical fiscal target drift")
    rates = pd.read_csv(SCHOOL / "derived/national_rates.csv").set_index("cell").rate.to_dict()
    code = cells(d)
    code[~civil] = "out"
    rate = np.array([rates.get(c, 0.0) for c in code])
    w = state["person_weights"][:, 0].astype(float)
    pp = d.GESTFIPS.map(state["params"].per_pupil_current_spending).to_numpy(float)
    index, n_units = state["index"], state["n_units"]
    pupils = w * rate

    def shared_weight(mask):
        unit = np.zeros(n_units)
        np.add.at(unit, index, w * mask)
        return unit[index] / np.bincount(index, minlength=n_units)[index]

    masks = {"target": target & civil, "national": civil}
    frame = pd.DataFrame({"fips": d.GESTFIPS.to_numpy(), "per_pupil_state": pp})
    for name, mask in masks.items():
        frame[f"{name}_pupils"] = pupils * mask
        frame[f"{name}_school_personal"] = pupils * mask * pp
        frame[f"{name}_school_shared"] = rate * pp * shared_weight(mask.astype(float))
    by_state = frame.groupby("fips").agg(
        per_pupil_state=("per_pupil_state", "first"),
        target_pupils=("target_pupils", "sum"), national_pupils=("national_pupils", "sum"),
        target_school_personal_bn=("target_school_personal", "sum"),
        target_school_shared_bn=("target_school_shared", "sum"),
        national_school_personal_bn=("national_school_personal", "sum"),
        national_school_shared_bn=("national_school_shared", "sum")).reset_index()
    for c in [c for c in by_state if c.endswith("_bn")]:
        by_state[c] /= 1e9
    name = {v: k for k, v in al.STATE_NAME_TO_FIPS.items()} if hasattr(al, "STATE_NAME_TO_FIPS") else {}
    by_state.insert(1, "state", by_state.fips.map(name))

    # Gates against the canonical outputs this reconstruction must reproduce.
    comp = pd.read_csv(SCHOOL / "derived/updated_account_components.csv")
    moved = pd.read_csv(SCHOOL / "derived/transported_pupils.csv")

    def canon(alloc, group):
        row = comp[(comp.allocation == alloc) & (comp.group == group) & (comp.component == "school")]
        return float(row.spending_bn.iloc[0])
    checks = {
        "target_school_personal_bn": (by_state.target_school_personal_bn.sum(), canon("personal", "mexican_observed_total")),
        "target_school_shared_bn": (by_state.target_school_shared_bn.sum(), canon("shared", "mexican_observed_total")),
        "national_school_personal_bn": (by_state.national_school_personal_bn.sum(), canon("personal", "national_civilian")),
        "national_school_shared_bn": (by_state.national_school_shared_bn.sum(), canon("shared", "national_civilian")),
    }
    pupil_rows = moved[(moved.state == 0) & (moved.age == "all_ages")].set_index("group").updated_pupils
    checks["target_pupils"] = (by_state.target_pupils.sum() / 1e6, pupil_rows["mexican_observed_total"] / 1e6)
    checks["national_pupils"] = (by_state.national_pupils.sum() / 1e6, pupil_rows["national_civilian"] / 1e6)
    failed = []
    for label, (got, want) in checks.items():
        ok = abs(got - want) < TOL_BN * max(1.0, abs(want))
        print(f"  {'PASS' if ok else 'FAIL'} {label}: {got:.6f} vs canonical {want:.6f}")
        if not ok:
            failed.append(label)
    if failed:
        raise SystemExit(f"[BLOCKED] reconstruction does not reproduce the canonical school component: {failed}")

    t = by_state.sum(numeric_only=True)
    r_embedded = (t.target_school_personal_bn / t.target_pupils) / (t.national_school_personal_bn / t.national_pupils)
    summary = dict(
        target_pupils=t.target_pupils, national_pupils=t.national_pupils,
        target_price_personal=t.target_school_personal_bn * 1e9 / t.target_pupils,
        national_price_personal=t.national_school_personal_bn * 1e9 / t.national_pupils,
        r_embedded_personal=r_embedded,
        target_school_personal_bn=t.target_school_personal_bn, target_school_shared_bn=t.target_school_shared_bn,
        national_school_personal_bn=t.national_school_personal_bn, national_school_shared_bn=t.national_school_shared_bn,
        note="school component of the education_mix key; pupils are transported October-2024 rates on March-2025 CPS")
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    by_state.sort_values("target_pupils", ascending=False).to_csv(
        out / "account_pupils_by_state.csv", index=False, lineterminator="\n", float_format="%.6f")
    (out / "account_embedded_price.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
