"""Freeze evidence bytes explicitly; run only when intentionally refreshing pins.

Native-First: hashlib plus existing local source files. No data or model edits.
"""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
INPUTS = {
    "_cache/epa_scghg_2023.pdf": "https://www.epa.gov/system/files/documents/2023-12/epa_scghg_2023_report_final.pdf Table A.5.1",
    "_cache/iwg_2021.pdf": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2021/02/TechnicalSupportDocument_SocialCostofCarbonMethaneNitrousOxide.pdf Table A-1",
    "_cache/bea_gdp4q24_2nd.pdf": "https://www.bea.gov/sites/default/files/2025-02/gdp4q24-2nd.pdf Table 8, annual 2024; fixed Feb 2025 vintage",
    "_cache/bea_pi0125.pdf": "https://www.bea.gov/sites/default/files/2025-02/pi0125.pdf; acquisition probe, monthly table not used for annual PCE",
    "inputs/band_variants.json": "snapshot sept24_propagation_2026_09_24/derived/oct14/band_variants.json; lineage_social_keys",
    "inputs/band_variants.csv": "snapshot oct14 band_variants.csv; exact justice footing difference for social pairing",
    "inputs/baseline_totals_oct14.csv": "pre-P7 baseline social pairing, preserved by peer's social_costs_unpriced inputs",
    "../air_pollution_2026_09_28/_cache/owid-co2-data.csv": "https://github.com/owid/co2-data; Global Carbon Budget consumption-based series, pinned original lane file",
    "../air_pollution_2026_09_28/air_items.py": "inherited PM/CO2 model assumptions and positive control",
    "../air_pollution_2026_09_28/derived/items.csv": "legacy producer controls",
    "../air_pollution_2026_09_28/derived/ce_group_spending.csv": "CE 2024 Interview spending, parsed by ce_energy.py",
    "../consumption_key_2026_09_24/_cache/sources/bls_cpi_u_2015_2024.json": "BLS CPI-U annual inflation 2020 to 2024",
    "../main_case_2026_10_14/derived/corrections_cash.json": "frozen v7 cash payload",
    "../main_case_2026_10_14/derived/corrections.json": "frozen v7 accrual payload",
    "../main_case_2026_10_14/derived/summary.json": "frozen v7 endpoints and capital controls",
    "../main_case_decomposition_2026_09_29/derived/headcount.csv": "published and row4 population bridge",
    "../disease_food_2026_09_28/derived/items.csv": "legacy restaurant model output",
    "../disease_food_2026_09_28/derived/inputs.csv": "legacy restaurant model assumptions",
    "../population_basis_2026_09_29/derived/consumer_scale_rerun/row4/items.csv": "row4 consumer scale output",
    "../air_pollution_2026_09_28/derived/mortality_items.csv": "mortality producer; uniform/VSLY alternative replacement rows",
    "../air_pollution_2026_09_28/derived/mortality_context.json": "mortality producer; source/receptor/valuation primitives",
    "../air_pollution_2026_09_28/derived/binding_caps.json": "air producer; primary program facts and unidentified marginal cap share",
    "../road_crash_externality_2026_09_28/derived/capacity_items.csv": "crash producer; density-interpretation and recipient-boundary alternatives",
    "../benefits_inventory_2026_09_28/derived/volunteering_flows.csv": "benefits producer; measured food receipt with conditional incoming labour/displacement",
    "../benefits_inventory_2026_09_28/derived/city_tax_decomposition.csv": "benefits producer; existing gross includes induced receipts",
}
if sys.argv[1:] == ["--freeze"]:
    rows = [{"path": p, "sha256": hashlib.sha256((HERE/p).read_bytes()).hexdigest(), "source":s}
            for p,s in INPUTS.items()]
    (HERE/"inputs/pins.json").write_text(json.dumps(rows,indent=2)+"\n")
    print(f"pinned {len(rows)} inputs; intentional evidence refresh")
elif sys.argv[1:] == ["--check"]:
    rows = json.loads((HERE/"inputs/pins.json").read_text())
    assert set(INPUTS) == {r["path"] for r in rows}, "[BLOCKED] pin coverage changed"
    for r in rows:
        assert hashlib.sha256((HERE/r["path"]).read_bytes()).hexdigest()==r["sha256"], f"[BLOCKED] changed input {r['path']}"
    print(f"verified {len(rows)} pins")
else:
    raise SystemExit("use --freeze for an intentional evidence refresh, --check for reproduction")
