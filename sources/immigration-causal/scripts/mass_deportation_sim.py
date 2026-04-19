"""Mass-deportation 11M-scale counterfactual: industry-by-industry output collapse.

Streamlined partial-equilibrium calibration. Inputs:
- Industry × unauthorized employment share (Pew Research / CMS estimates, 2022)
- BEA labor share of value added by industry
- Total industry output (BEA Use Table)
- Short-run labor demand elasticity (literature: -0.3 to -0.5 for low-skill)

Output: Industry-level and national projections of output, employment, consumer
price impact under 100% removal of unauthorized workers.

This is a CALIBRATION, not a forecast. It gives order-of-magnitude bounds, not
point estimates. The actual response would involve capital-labor substitution,
relocation, output-mix adjustment, automation, illegal employment continuation,
etc — none of which this model captures.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
BEA = DATA / "bea_io" / "Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx"
OUT = DATA / "analysis"
OUT.mkdir(parents=True, exist_ok=True)


# === Industry × unauthorized employment share ===
# Sources:
#   Passel & Cohn (Pew Research, 2022) "Unauthorized immigrants in U.S. workforce 2017"
#   Center for Migration Studies (CMS) 2022 estimates
#   BLS occupation-industry crosswalks
# Numbers are 2022 best estimates; ranges in literature ±20%.
INDUSTRY_UNAUTH_SHARE = {
    "111CA": 0.24,       # Farms
    "113FF": 0.18,       # Forestry, fishing
    "23":    0.13,       # Construction
    "31G":   0.05,       # Manufacturing (durable + nondurable)
    "44RT":  0.06,       # Retail trade
    "48TW":  0.07,       # Transportation, warehousing
    "55":    0.02,       # Management
    "56":    0.10,       # Administrative & waste services (cleaning concentrated)
    "61":    0.03,       # Educational services
    "62":    0.03,       # Health & social assistance
    "71":    0.07,       # Arts, entertainment, recreation
    "72":    0.09,       # Accommodation & food services
    "81":    0.16,       # Other services (personal services, household, gardening)
    "GFGN":  0.0,        # Federal government — by definition no unauthorized
    "GSLG":  0.01,       # State & local govt
    # Default for unlisted industries: ~3%
}

# === Approx 11M unauthorized in US, ~7M in labor force ===
TOTAL_UNAUTH_LABOR_FORCE = 7e6     # Pew 2022
TOTAL_US_LABOR_FORCE = 168e6
TOTAL_UNAUTH_POP = 11e6


# === Labor share of value added by sector (BEA, 2022) ===
# Compensation of employees / Gross value added
LABOR_SHARE = {
    "111CA": 0.18,    # Farms (low — capital + land intensive)
    "113FF": 0.30,
    "23":    0.45,    # Construction (labor heavy)
    "31G":   0.42,
    "44RT":  0.48,
    "48TW":  0.50,
    "55":    0.65,
    "56":    0.55,
    "61":    0.75,    # Education (labor very heavy)
    "62":    0.60,
    "71":    0.45,
    "72":    0.40,
    "81":    0.55,
    "GFGN":  0.65,
    "GSLG":  0.65,
    "default": 0.45,
}

# === Industry → human-readable name ===
INDUSTRY_NAMES = {
    "111CA": "Farms",
    "113FF": "Forestry, fishing",
    "23":    "Construction",
    "31G":   "Manufacturing",
    "44RT":  "Retail trade",
    "48TW":  "Transportation, warehousing",
    "55":    "Management of companies",
    "56":    "Administrative & waste services",
    "61":    "Educational services (private)",
    "62":    "Health care & social assistance",
    "71":    "Arts, entertainment, recreation",
    "72":    "Accommodation & food services",
    "81":    "Other services (excl. govt)",
    "GFGN":  "Federal government",
    "GSLG":  "State & local government",
}


def load_bea_2023() -> pd.DataFrame:
    """Load BEA 2023 Use Table at summary level. Returns long format with industry codes."""
    df = pd.read_excel(BEA, sheet_name="2023", header=None)
    # Headers: row 5 has commodity codes (col 2+); row 6 has industry codes (col 2+)
    industry_codes = df.iloc[5, 2:].dropna().tolist()
    industry_names = df.iloc[6, 2:].dropna().tolist()
    # Find the "Total Industry Output" row
    output_row_idx = None
    for i in range(7, len(df)):
        cell = str(df.iloc[i, 1])
        if "Total Industry Output" in cell or cell.lower().startswith("total industry"):
            output_row_idx = i
            break

    industries = pd.DataFrame({
        "code": industry_codes,
        "name": industry_names,
    })
    if output_row_idx is not None:
        # Output values per industry are in same columns as industries
        outputs = df.iloc[output_row_idx, 2:2+len(industry_codes)].tolist()
        industries["total_output_M"] = pd.to_numeric(outputs, errors="coerce")
    return industries


def main():
    industries = load_bea_2023()
    print(f"Loaded {len(industries)} BEA industries from 2023 summary table")
    print()

    # Build industry-level shock table
    rows = []
    for _, row in industries.iterrows():
        code = str(row["code"]).strip()
        name = row.get("name", "")
        output_M = row.get("total_output_M", np.nan)
        unauth_share = INDUSTRY_UNAUTH_SHARE.get(code, 0.03)  # default 3%
        labor_share = LABOR_SHARE.get(code, LABOR_SHARE["default"])

        # First-order: labor supply contraction = unauth_share of industry employment
        # If industry is X% labor (factor share), removing all unauth → output falls by
        # roughly unauth_share × labor_share × 1/(1+sigma) where sigma is K-L substitution elasticity.
        # Use sigma=0.5 (low for short-run): output falls by ~unauth_share × labor_share × 0.67
        # Conservative: short-run output loss = unauth_share × labor_share
        short_run_output_loss_pct = unauth_share * labor_share * 100
        output_loss_M = (short_run_output_loss_pct / 100) * (output_M if pd.notna(output_M) else 0)
        rows.append({
            "code": code,
            "name": name if isinstance(name, str) else INDUSTRY_NAMES.get(code, ""),
            "output_M": output_M,
            "unauth_employment_share": unauth_share,
            "labor_share_of_VA": labor_share,
            "short_run_output_loss_pct": short_run_output_loss_pct,
            "short_run_output_loss_M": output_loss_M,
        })
    df = pd.DataFrame(rows)
    df = df.sort_values("short_run_output_loss_pct", ascending=False)
    df.to_csv(OUT / "mass_deportation_industry_shock.csv", index=False)

    print("=== Top-10 industries by short-run output loss % ===")
    top = df.nlargest(15, "short_run_output_loss_pct")
    for _, r in top.iterrows():
        print(f"  {r['code']:<6s}  {r['name']:<45s}  unauth={r['unauth_employment_share']:>5.1%}  loss={r['short_run_output_loss_pct']:>5.1f}%  ${r['short_run_output_loss_M']/1000:.1f}B")

    print()
    print("=== National aggregates ===")
    total_output_M = df["output_M"].sum()
    total_loss_M = df["short_run_output_loss_M"].sum()
    print(f"Total industry output (2023):              ${total_output_M/1e6:>8.2f} trillion")
    print(f"First-order output loss from removal:      ${total_loss_M/1e6:>8.2f} trillion")
    print(f"As % of US GDP ($27.4T 2023):              {100 * total_loss_M / 27.4e6:>8.2f}%")
    print(f"As % of total industry output:             {100 * total_loss_M / total_output_M:>8.2f}%")
    print()

    # With multiplier (rough I-O propagation factor ~1.6 for first-round + indirect)
    multiplier = 1.6
    propagated_loss_T = total_loss_M / 1e6 * multiplier
    print(f"With Type-II multiplier (~1.6, indirect+induced):  ${propagated_loss_T:.2f} trillion")
    print(f"As % of US GDP:                                     {100 * propagated_loss_T / 27.4:>5.2f}%")
    print()

    # Per-removed-worker output loss
    print(f"Implied first-order output loss per removed worker: ${total_loss_M*1e6 / TOTAL_UNAUTH_LABOR_FORCE:>8,.0f}")
    print(f"With multiplier:                                     ${propagated_loss_T*1e12 / TOTAL_UNAUTH_LABOR_FORCE:>8,.0f}")

    # Save summary JSON
    summary = {
        "scenario": "Full removal of 7M unauthorized workers",
        "total_industry_output_2023_T": total_output_M / 1e6,
        "first_order_output_loss_T": total_loss_M / 1e6,
        "first_order_loss_pct_gdp": 100 * total_loss_M / 27.4e6,
        "with_multiplier_loss_T": propagated_loss_T,
        "with_multiplier_loss_pct_gdp": 100 * propagated_loss_T / 27.4,
        "per_removed_worker_first_order_usd": total_loss_M*1e6 / TOTAL_UNAUTH_LABOR_FORCE,
        "per_removed_worker_with_multiplier_usd": propagated_loss_T*1e12 / TOTAL_UNAUTH_LABOR_FORCE,
        "top_5_affected_industries": df.nlargest(5, "short_run_output_loss_pct")[["code", "name", "short_run_output_loss_pct"]].to_dict(orient="records"),
        "caveats": [
            "Partial equilibrium — no capital-labor substitution",
            "No relocation, output-mix adjustment, or automation response",
            "Assumes 100% removal compliance (real enforcement <50%)",
            "Industry unauthorized shares from Pew/CMS — ranges ±20%",
            "Labor shares from BEA aggregate, not industry-time-specific",
            "No short vs long run distinction (LR may be 50-70% smaller)",
        ],
    }
    (OUT / "mass_deportation_summary.json").write_text(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
