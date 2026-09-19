"""Small inspectable tables selected from the complete scenario exports."""
import json
from pathlib import Path

import pandas as pd

from builder import sha

HERE = Path(__file__).resolve().parent
OUT = HERE/"derived"


def main():
    for audit_name in ["audit.json", "welfare_audit.json"]:
        audit = json.loads((OUT/audit_name).read_text())
        for source, expected in audit["source_hashes"].items():
            if sha(source) != expected:
                raise ValueError(f"Upstream input drift: {source}")
        for name, expected in audit["outputs"].items():
            if sha(OUT/f"{name}.csv") != expected:
                raise ValueError(f"Upstream output drift: {name}")
    w = pd.read_csv(OUT/"welfare_scenarios.csv")
    primary = w.query("service_response == 1 and public_goods_response == 0 and fiscal_weight == 1")
    core = primary.query("excluded_capital_owner_share == 0")
    baseline = primary.query("receipt_scenario == 'cbo_collective' and spending_scenario == 'complete_preferred_F_per_capita' and proxy == 'PEARNVAL' and split == 'hs_or_less' and labor_share == 0.65 and sigma == 2 and labor_supply_elasticity == 0 and capital_tax_retention == 1 and excluded_capital_owner_share == 0")
    columns = ["allocation", "normalization", "direct_fiscal_response_bn", "private_plus_receipts_bn",
               "welfare_bn", "break_even_service_response_beta1", "break_even_omitted_bn"]
    baseline[columns].to_csv(OUT/"headline_cases.csv", index=False)
    summary = dict(
        longrun_core_grid_welfare_bn=[float(core.welfare_bn.min()), float(core.welfare_bn.max())],
        longrun_core_max_incremental_service_fraction=float(core.break_even_service_response_beta1.max()),
        full_capital_all_ownership_endpoints_welfare_bn=[float(primary.welfare_bn.min()), float(primary.welfare_bn.max())],
        core_capacity_path=w.query("excluded_capital_owner_share == 0 and public_goods_response == 0 and fiscal_weight == 1").groupby("service_response").welfare_bn.agg(["min", "max"]).to_dict("index"),
        preferred_service_roots=core.query("receipt_scenario == 'cbo_collective' and spending_scenario == 'complete_preferred_F_per_capita'").groupby("allocation").break_even_service_response_beta1.agg(["min", "max"]).to_dict("index"),
        welfare_rows=len(w), complete_account_rows=int(pd.read_csv(OUT/"accounts.csv").complete.sum()),
    )
    (OUT/"headline_summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(baseline[columns].to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
