"""Baseline open-borders calibration using Clemens (2011, JEP) parameters.

Produces scenario table for GPT-5.4 sensitivity analysis. The script does the
arithmetic; the LLM does the binding-constraint identification and welfare-
weight reasoning.
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path(__file__).parent.parent / "data" / "clemens"
OUT.mkdir(parents=True, exist_ok=True)


# === Clemens 2011 + Place Premium parameters (cited from PDF in same dir) ===
PLACE_PREMIUM = {  # ratio of US wage to home wage for observably equivalent worker
    "Bolivia": 2.7,
    "India": 4.5,    # Clemens-Montenegro-Pritchett 2008 estimate
    "Mexico": 2.5,
    "Philippines": 3.6,
    "Nigeria": 8.4,
    "Egypt": 6.0,
    "Haiti": 10.3,
    "Yemen": 14.7,
    "Vietnam": 5.5,
    "Bangladesh": 5.7,
    "Honduras": 5.0,
    "Guatemala": 4.2,
    "Pakistan": 5.2,
}

# === World stock parameters (UN DESA 2024, World Bank WDI 2024) ===
WORLD_POP_2024 = 8.1e9                  # 8.1 billion
RICH_QUARTILE_POP = 1.4e9               # HDI top quartile
POOR_THREE_QUARTERS_POP = 6.7e9
US_POP = 333e6
US_FB_POP = 47e6                        # ~14.3% foreign-born stock
GLOBAL_MIGRANT_STOCK_2020 = 281e6       # UN DESA: 3.5% of world
US_GDP_2024 = 27.4e12                   # $27.4 trillion
WORLD_GDP_2024 = 110e12                 # $110 trillion (PPP-ish)

# === Per-migrant gain (Clemens 2011 envelope estimate) ===
# Average annual gain from migration for poor-country migrant: $7,500
# (Conservative: assumes only 60% of nominal gap captured + diminishing returns)
PER_MIGRANT_AVG_GAIN_USD = 7500
PER_MIGRANT_HIGH_PREMIUM_USD = 15000   # for high-place-premium origins (Haiti, Nigeria)


# === Scenarios ===
def scenario(label: str, additional_migrants_to_rich: float, per_migrant_gain: float) -> dict:
    annual_gain = additional_migrants_to_rich * per_migrant_gain
    return {
        "label": label,
        "additional_migrants_to_rich_M": additional_migrants_to_rich / 1e6,
        "per_migrant_gain_usd": per_migrant_gain,
        "annual_gain_usd_T": annual_gain / 1e12,
        "as_pct_world_gdp": 100 * annual_gain / WORLD_GDP_2024,
        "as_pct_us_gdp": 100 * annual_gain / US_GDP_2024,
        "rich_pop_after_M": (RICH_QUARTILE_POP + additional_migrants_to_rich) / 1e6,
        "rich_pct_after": 100 * (RICH_QUARTILE_POP + additional_migrants_to_rich) / WORLD_POP_2024,
        "poor_pop_after_M": (POOR_THREE_QUARTERS_POP - additional_migrants_to_rich) / 1e6,
    }


SCENARIOS = [
    scenario("S0 Status quo (no change)", 0, PER_MIGRANT_AVG_GAIN_USD),
    scenario("S1 +50M (one-time, 1.5x current rich pop)", 50e6, PER_MIGRANT_AVG_GAIN_USD),
    scenario("S2 +200M (current global migrant stock doubled)", 200e6, PER_MIGRANT_AVG_GAIN_USD),
    scenario("S3 +500M (5% poor pop emigrates)", 500e6, PER_MIGRANT_AVG_GAIN_USD),
    scenario("S4 +1B (rich-pop nearly doubled)", 1e9, PER_MIGRANT_AVG_GAIN_USD),
    scenario("S5 +3B (50% poor emigrates, Clemens upper bound)", 3e9, PER_MIGRANT_AVG_GAIN_USD),
    # Same scenarios with HIGHER per-migrant gain (high-premium origin mix)
    scenario("S2hi +200M from high-premium origins", 200e6, PER_MIGRANT_HIGH_PREMIUM_USD),
    scenario("S3hi +500M from high-premium origins", 500e6, PER_MIGRANT_HIGH_PREMIUM_USD),
]


# === Capacity constraints (rough U.S. parameters) ===
CONSTRAINTS = {
    "housing_starts_per_year_2024": 1.4e6,           # US Census
    "housing_units_total_2024": 145e6,
    "people_per_unit": 2.5,
    "k12_enrollment_2024": 49.7e6,
    "labor_force_2024": 168e6,
    "employed_2024": 161e6,
    "physician_density_per_1000": 2.6,               # OECD avg
    "hospital_beds_per_1000": 2.8,
    "construction_workers_total": 11.4e6,
    "construction_workers_fb_share": 0.30,           # roughly 30% foreign-born
    "ag_workers_fb_share": 0.45,
    "food_service_fb_share": 0.22,
    "elder_care_fb_share": 0.32,
    "house_supply_elasticity_inelastic_q1_median": 1.23,  # Saiz
    "house_supply_elasticity_elastic_q4_median": 4.26,
    "saiz_msa_top_immigrant_concentration_pct": 41.5,    # Miami
}


def main():
    payload = {
        "world_parameters": {
            "world_pop_2024": WORLD_POP_2024,
            "rich_quartile_pop": RICH_QUARTILE_POP,
            "poor_three_quarters_pop": POOR_THREE_QUARTERS_POP,
            "us_pop": US_POP,
            "us_fb_pop": US_FB_POP,
            "global_migrant_stock_2020": GLOBAL_MIGRANT_STOCK_2020,
            "us_gdp_2024": US_GDP_2024,
            "world_gdp_2024": WORLD_GDP_2024,
        },
        "place_premium_by_origin": PLACE_PREMIUM,
        "per_migrant_gain_baseline_usd": PER_MIGRANT_AVG_GAIN_USD,
        "per_migrant_gain_high_premium_usd": PER_MIGRANT_HIGH_PREMIUM_USD,
        "scenarios": SCENARIOS,
        "capacity_constraints_us": CONSTRAINTS,
        "clemens_2011_key_claims": [
            "Half-poor-pop emigration → 50-150% world GDP gain (Tables 1+2)",
            "5% poor pop emigration → exceeds gains from full trade liberalization",
            "Currently ~280M migrants worldwide (~3.5%), ~46M in US",
            "13.6M DV lottery applications for 50K visas in FY2010 → 272 applicants per slot",
            "Per-migrant avg gain $7,500/yr (60% of nominal gap, with diminishing returns)",
            "Real wage gaps for identical low-skill workers exceed 1000% (10x) for Haiti, Nigeria, Egypt",
        ],
    }
    out = OUT / "open_borders_calibration_baseline.json"
    out.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {out}")
    print()
    print("=== Scenario table ===")
    print(f"{'Label':<55s}  {'AddM':>6s}  {'$/migr':>8s}  {'Total $T':>10s}  {'%WorldGDP':>10s}")
    for s in SCENARIOS:
        print(f"{s['label']:<55s}  {s['additional_migrants_to_rich_M']:>6.0f}M {s['per_migrant_gain_usd']:>8,.0f}  ${s['annual_gain_usd_T']:>9.2f}T  {s['as_pct_world_gdp']:>9.1f}%")


if __name__ == "__main__":
    main()
