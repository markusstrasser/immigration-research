"""How far the MCBS 65+ conflict moves the account's Medicare and Medicaid lines (decision 2's range).

The pooled-MEPS lane (`medical_ethnicity_pooled_2026_09_23`) puts the group's 65+ public medical draw on
MCBS's definitions at 1.005 (SE 0.056, nine pooled years); MCBS 2023 gives 1.265 (SE 0.152, one year).
This scales the 65+ transport cells' Medicare and Medicaid ratios (the MCBS payer set) by k and
re-derives each line's change the lane's way: target x (key-weighted ratio - 1), p99.5 specification.

k = 1 must reproduce the lane's published changes (Medicare -9.912, Medicaid +13.639); the other two
cases are the precision-weighted combination of the two surveys and MCBS taken as the truth.
Run: uv run --no-project python3 infra/immigration-fiscal/main_case_2026_09_24/mcbs_bound.py
"""
import json
import pathlib

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parent / "medical_ethnicity_pooled_2026_09_23" / "derived"
MEPS, MEPS_SE, MCBS, MCBS_SE = 1.005, 0.056, 1.265, 0.152
SPEC = "winsor_p995"


def main():
    cells = pd.read_csv(LANE / "cps_cells.csv")
    ratios = pd.read_csv(LANE / "ratios.csv")
    account = pd.read_csv(LANE / "translation_account.csv")
    sel = ratios[(ratios["sample"] == "pooled_2016_2024") & (ratios["spec"] == SPEC)
                 & (ratios["scheme"] == "transport") & (ratios["comparison"] == "mexican_origin/all_donors")]
    w_meps, w_mcbs = 1 / MEPS_SE ** 2, 1 / MCBS_SE ** 2
    weighted = (w_meps * MEPS + w_mcbs * MCBS) / (w_meps + w_mcbs)
    cases = {"published": 1.0, "precision_weighted": weighted / MEPS, "mcbs_as_truth": MCBS / MEPS}
    out = {"spec": SPEC, "meps_65plus_on_mcbs_definitions": [MEPS, MEPS_SE], "mcbs_2023": [MCBS, MCBS_SE],
           "precision_weighted_ratio": weighted, "cases": {}}
    for name, k in cases.items():
        row = {"k": k}
        for line, key, measure in [("medicare", "key_medicare", "medicare"),
                                   ("medicaid_and_chip_other_medical", "key_medicaid", "medicaid")]:
            num = den = 0.0
            for _, c in cells.iterrows():
                hit = sel[(sel["measure"] == measure) & (sel["band"] == c["band"]) & (sel["nativity"] == c["nativity"])]
                if len(hit) != 1:
                    raise SystemExit(f"[BLOCKED] {len(hit)} ratio rows for {measure}/{c['band']}/{c['nativity']}")
                ratio = float(hit["ratio"].iloc[0]) * (k if c["band"] == "65+" else 1.0)
                num += c[key] * ratio
                den += c[key]
            target = float(account[(account["spec"] == SPEC) & (account["line"] == line)]["account_target_bn"].iloc[0])
            row[line] = target * (num / den - 1)
        out["cases"][name] = row
    pub = account[account["spec"] == SPEC].set_index("line")["delta_bn"]
    got = out["cases"]["published"]
    for line in ("medicare", "medicaid_and_chip_other_medical"):
        if abs(got[line] - float(pub[line])) > 1e-6:
            raise SystemExit(f"[BLOCKED] k = 1 does not reproduce the lane's {line}: {got[line]} vs {pub[line]}")
    (HERE / "derived" / "mcbs_bound.json").write_text(json.dumps(out, indent=1) + "\n")
    for name, row in out["cases"].items():
        print(f"{name:20s} k {row['k']:.4f}  Medicare {row['medicare']:+.3f}  "
              f"Medicaid {row['medicaid_and_chip_other_medical']:+.3f}")
    print("gate passed: k = 1 reproduces the lane's p99.5 changes")


if __name__ == "__main__":
    main()
