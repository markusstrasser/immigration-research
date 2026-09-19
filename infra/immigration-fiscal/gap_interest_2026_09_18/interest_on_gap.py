"""Real-dollar financing scenarios on the current annual expanded account.

Native-First: consume validated annual age profiles and use the finite annuity.
Financing fractions are imposed scenarios. This does not estimate caused debt.
Per-person future values at different terminal dates and flat shifts are withdrawn.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ledger_absolute_2026_09_17"))
import lifetime as L

UNION = "mexican_observed_total"


def financing_path(annual_flow: float, real_rate: float, years: int, fraction: float) -> dict:
    rate = float(real_rate)
    if not np.isfinite([annual_flow, rate, fraction]).all() or rate <= -1 or years < 1 or not 0 <= fraction <= 1:
        raise ValueError("invalid financing scenario")
    # Annual real flows occur at year end; positive debt denotes borrowing.
    borrowing = -annual_flow * fraction
    growth = np.power(1.0 + rate, np.arange(years, dtype=float))
    debt = borrowing * growth.sum()
    principal = borrowing * years
    prior_debt = borrowing * growth[:-1].sum()
    return dict(debt_bn=float(debt), principal_bn=float(principal),
                interest_component_bn=float(debt - principal),
                interest_in_year_N_bn=float(rate * prior_debt))


def annual_flows(profiles: pd.DataFrame, allocation: str) -> dict[str, float]:
    selected = profiles[(profiles.allocation == allocation) & (profiles.account == "expanded")]
    target = selected[selected.group == UNION].set_index("band").sort_index()
    if len(target) != 8:
        raise ValueError("[BLOCKED] annual union profile is incomplete")
    flows = {"union_absolute": float(target.net_total.sum() / 1e9)}
    for ref in ("third_plus_nh_white", "all_native"):
        reference = selected[selected.group == ref].set_index("band").sort_index()
        if len(reference) != 8:
            raise ValueError(f"[BLOCKED] reference age profile missing: {ref}")
        gap = target.net_total - target.population * reference.net_per_person
        flows[f"union_age_matched_gap_vs_{ref}"] = float(gap.sum() / 1e9)
    return flows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=L.ROOT)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    parser.add_argument("--allocation", choices=["personal", "shared"], default="shared")
    parser.add_argument("--real-rates", type=float, nargs="+", default=[0.0, .02, .03, .05])
    parser.add_argument("--deficit-shares", type=float, nargs="+", default=[0.0, .5, 1.0])
    parser.add_argument("--years", type=int, nargs="+", default=[10, 20, 30])
    args = parser.parse_args()
    profiles, sources = L.load_age_profiles(args.root)
    rows = []
    for name, value in annual_flows(profiles, args.allocation).items():
        for fraction in args.deficit_shares:
            for rate in args.real_rates:
                for years in args.years:
                    rows.append(dict(flow=name, annual_flow_bn=value, allocation=args.allocation,
                                     price_year=2024, real_rate=rate, years=years,
                                     imposed_deficit_share=fraction,
                                     **financing_path(value, rate, years, fraction)))
    result = pd.DataFrame(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    target = args.out_dir / "aggregate_debt_paths.csv"
    result.to_csv(target, index=False)
    sources[str(Path(__file__))] = L.sha256(Path(__file__))
    audit = dict(schema="fiscal-real-financing-v2",
                 inputs=[dict(path=p, sha256=h) for p, h in sources.items()],
                 output_sha256=L.sha256(target), allocation=args.allocation,
                 flow="constant annual expanded-account real 2024 dollars; no population change",
                 timing="year-end flows, real annual compounding, positive debt is borrowing",
                 financing="specified fractions are assumptions, not observed immigration-caused borrowing",
                 excluded="federal-share fractions are not inferred from stale incidence outputs",
                 supersedes=["per_person_terminal_values.csv", "complete_minus_partial_per_person_year"])
    (args.out_dir / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(f"[written] {len(result)} real-dollar financing scenarios: {target}")


if __name__ == "__main__":
    main()
