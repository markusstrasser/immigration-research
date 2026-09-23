"""Gate: reproduce the integrity audit's row-5 bound from the account's own files.

Reads the complete account's Medicaid allocation (full_account_spending_2026_09_20) and the
adopted main case (main_case_2026_09_23), then recomputes the audit's bound (spending.md #3):
institutional LTSS of $83-87bn and 0-70% of $129.4bn HCBS missed by MEPS, re-charged from the
account's rate to a true group share of 8% (least) or 4% (most). Also checks that a shift in the
group's Medicaid allocation moves the main case one-for-one (the line responds at 1), and
reproduces the medical-ethnicity lane's nursing-facility bound ($8.43bn charged, $2.20-4.41bn by
use) from that lane's own input cells.
Writes derived/gate.json. Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ltss_share_2026_09_23/gate.py
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
AUDIT = {"inst_bn": (83.0, 87.0), "hcbs_bn": 129.4, "missed": (0.0, 0.7), "true_share": (0.08, 0.04),
         "charged": 0.123, "bound_bn": (-3.6, -15.0)}


def main():
    alloc = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    rows = alloc[alloc.scenario_id.eq("complete_preferred_F_per_capita")
                 & alloc.category.eq("medicaid_and_chip_other_medical")].set_index("allocation")
    keys = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv")
    key = keys[keys.key.eq("medicaid")].set_index("allocation").target_share
    checks = {}
    for a in ("personal", "shared"):
        r = rows.loc[a]
        checks[a] = bool(abs(r.national_bn * r.household_pool_fraction * r.target_key_share - r.target_bn) < 1e-9
                         and abs(r.target_key_share - key[a]) < 1e-12 and r.allocation_key == "medicaid"
                         and r.response_class == "household_transfer")
    r = rows.loc["personal"]
    national_rate = r.target_bn / r.national_bn
    # Main case: the uncompensated-care shift sits on this line and moves the band one-for-one.
    bands = pd.read_csv(FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv")
    band = bands[bands.profile.eq("cbo_category_lag_non_school_full")].set_index("variant")
    uc = json.loads((FISCAL / "main_case_2026_09_23/derived/inputs.json").read_text())["uncompensated_inside_bn"]
    one_for_one = bool(abs(band.loc["uncompensated_inside_equal_use", "cost_low_bn"]
                       - band.loc["published", "cost_low_bn"] - uc["equal_low"]) < 1e-3
                   and abs(band.loc["uncompensated_inside_equal_use", "cost_high_bn"]
                           - band.loc["published", "cost_high_bn"] - uc["equal_high"]) < 1e-3)

    def bound(rate):
        least = AUDIT["inst_bn"][0] * (AUDIT["true_share"][0] - rate) \
            + AUDIT["missed"][0] * AUDIT["hcbs_bn"] * (AUDIT["true_share"][0] - rate)
        most = (AUDIT["inst_bn"][1] + AUDIT["missed"][1] * AUDIT["hcbs_bn"]) * (AUDIT["true_share"][1] - rate)
        return least, most

    variants = {"audit_stated_12.3pct": AUDIT["charged"], "national_rate": national_rate,
                "household_key_share": float(r.target_key_share)}
    bounds = {k: [round(x, 3) for x in bound(v)] for k, v in variants.items()}
    got = bounds["audit_stated_12.3pct"]
    reproduces = bool(round(got[0], 1) == AUDIT["bound_bn"][0] and round(got[1]) == AUDIT["bound_bn"][1])
    out = dict(
        medicaid_national_bn=float(r.national_bn), group_medicaid_bn=float(r.target_bn),
        household_pool_fraction=float(r.household_pool_fraction), household_key_share=float(r.target_key_share),
        national_rate=national_rate, allocation_rows_consistent=checks, main_case_one_for_one=one_for_one,
        main_case_adopted_bn=[float(band.loc["adopted", "cost_low_bn"]), float(band.loc["adopted", "cost_high_bn"])],
        audit_inputs=AUDIT, bound_bn_by_rate=bounds, audit_bound_reproduced=reproduces)
    # Gate 2: the medical-ethnicity lane's nursing-facility bound, from its own inputs.
    med = pd.read_csv(FISCAL / "medical_ethnicity_pooled_2026_09_23/derived/bounds.csv")
    nf = med[med.check.eq("nursing_facility")].set_index("quantity").value
    cells = pd.read_csv(FISCAL / "institutional_bound_2026_09_17/derived/acs_cells.csv")
    inst = cells[cells.typehugq.eq(2) & cells.band.isin(["65_74", "75_99"])].groupby("group").weighted.sum()
    ceiling = (inst["mexico_born"] + inst["usborn_mexican"]) / (inst["all_natives"] + inst["mexico_born"])
    nf_bn = 68.8  # CMS 2023 nursing facilities, as that lane rounds it
    med_gate = dict(ceiling=float(ceiling), charged_bn=nf_bn * national_rate,
                    use_based_bn=[nf_bn * ceiling, nf_bn * 2 * ceiling],
                    published=[float(nf[q]) for q in nf.index if q.startswith(("account charge", "use-based"))])
    med_ok = bool(abs(med_gate["charged_bn"] - float(nf.filter(like="account charge").iloc[0])) < 1e-9
                  and abs(med_gate["use_based_bn"][0] - float(nf.filter(like="use-based charge, union share =").iloc[0])) < 1e-9
                  and abs(med_gate["use_based_bn"][1] - float(nf.filter(like="use-based charge, union share doubled").iloc[0])) < 1e-9)
    out.update(med_lane_nf_gate=med_gate, med_lane_nf_gate_reproduced=med_ok)
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived/gate.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out.items():
        print(f"  {k}: {v}")
    if not (all(checks.values()) and one_for_one and reproduces and med_ok):
        raise SystemExit("✗ gate failed")
    print("  ✓ gate passed")


if __name__ == "__main__":
    main()
