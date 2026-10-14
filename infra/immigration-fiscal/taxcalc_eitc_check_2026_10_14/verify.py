"""Check the probe's accounting and its baseline against the adopted stack."""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
OUT = LANE / "derived"
UP = FISCAL / "cps_imputation_keys_2026_09_23"


def check(label, value):
    if not value:
        raise SystemExit(f"[BLOCKED] {label}")
    print(f"[PASS] {label}")


def main():
    summary = json.loads((OUT / "summary.json").read_text())
    keys = pd.read_csv(OUT / "keys.csv")
    totals = pd.read_csv(OUT / "totals.csv")
    base = np.load(UP / "_cache/hotdeck_key_shares.npz")
    stacks = json.loads((UP / "_cache/onbooks_lane_line_deltas.json").read_text())
    audit = json.loads((FISCAL / "backtest_admin_totals_2026_09_28/derived/prediction_audit.json").read_text())
    hf = audit["household_fraction"]
    mts = json.loads((FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json").read_text())
    found = keys[(keys.spec == "main") & (keys.seed == "mean") & (keys.key == "refundable_credits")
                & keys.basis.str.startswith("case_")]
    check("both methods x three status arms x two allocations", len(found) == 12)
    for r in found.itertuples():
        case = r.basis.removeprefix("case_")
        wanted = stacks[f"row4+status_state_aware|{case}|{r.method}"]["spending"]["refundable_tax_credits"]["refundable_credits"][r.allocation]
        measured = mts["non_ptc_remainder_bn"] * hf * (r.published_share - base[f"base|{r.allocation}|refundable_credits"][0])
        check(f"adopted stack refundable baseline {case} {r.method} {r.allocation}", abs(wanted-measured) < 1e-9)
    fit = totals[totals.field == "FEDTAX_BC"]
    check("every FEDTAX_BC total is unchanged", (fit.change_bn == 0).all())
    check("all sixteen donor runs recorded", len(summary["donor_checks"]) == 16)
    for spec, count in (("main", 5), ("all_items", 3)):
        z = totals[(totals.spec == spec) & (totals.seed != "mean")]
        check(f"{spec} each requested seed/variant/frame/group/field", len(z) == count * 2 * 2 * 2 * 3)
        for group, rows in z.groupby(["variant", "basis", "group", "field"]):
            m = totals[(totals.spec == spec) & (totals.seed == "mean")]
            for col, value in zip(("variant", "basis", "group", "field"), group):
                m = m[m[col] == value]
            check(f"{spec} total mean {' '.join(group)}", len(m) == 1 and abs(m.change_bn.iloc[0]-rows.change_bn.mean()) < 1e-12)
    t = pd.DataFrame(summary["translation"])
    check("1.90 conversion on all translations", np.allclose(t.refundable_change_bn, 1.9 * t.cps_group_equivalent_change_bn, atol=1e-12))
    check("finite CSVs, LF only", all(b"\r" not in p.read_bytes() and np.isfinite(pd.read_csv(p).select_dtypes("number")).all().all()
                                  for p in OUT.glob("*.csv")))
    print("All accounting and adopted-stack checks passed.")


if __name__ == "__main__":
    main()
