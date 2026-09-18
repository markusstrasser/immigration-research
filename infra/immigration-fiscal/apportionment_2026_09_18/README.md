# Apportionment lane — House seats and electoral votes attributable to the Mexican-origin population

Arithmetic, not identification: run the statutory apportionment method (Huntington-Hill, method of
equal proportions) on the official state counts, then re-run it with a population removed from the
states where it actually lives, and read off the seat and electoral-vote differences.

## Run order

```bash
cd infra/immigration-fiscal/apportionment_2026_09_18
set -a && . ../acquire/config.local.env && set +a          # CENSUS_API_KEY

UV='uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl'

uv run --no-project --with "pandas>=2" --with numpy --with xlrd --with openpyxl python3 hh.py
uv run --no-project --with "pandas>=2" --with numpy python3 fetch_counts.py
uv run --no-project --with "pandas>=2" --with openpyxl python3 prep_unauthorized.py
uv run --with duckdb --with "pandas>=2" python3 kids_ipums.py
uv run --no-project --with "pandas>=2" python3 build_arm4.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 counterfactuals.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 robustness.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 projection_2030.py
```

`hh.py` must print `EXACT MATCH: True` for 2020 and 2010 before anything downstream is meaningful.

## Scripts

| script | what it does |
|---|---|
| `hh.py` | Huntington-Hill apportionment, official-count verification, priority-value table |
| `fetch_counts.py` | Census API pulls (DDHC-A, SF1, ACS 5-year) → `derived/state_counts.csv` |
| `prep_unauthorized.py` | Pew 1990-2023 and CMS 2010-2019 unauthorized-by-state tables → tidy CSVs |
| `kids_ipums.py` | local IPUMS panel: US-born children under 18 per Mexico-born person, by state |
| `build_arm4.py` | Mexico-born + their US-born children under 18, level-anchored to ACS |
| `counterfactuals.py` | every arm, placebo and redistribution twin, electoral-vote arithmetic |
| `robustness.py` | Monte Carlo over estimate error (4,000 draws, seed 20260918) |
| `projection_2030.py` | rough 2030 arm from Census Vintage 2024 estimates |

## Inputs (all cached under `_cache/`, which is gitignored)

| input | source |
|---|---|
| 2020 apportionment population and seats | `www2.census.gov/.../apportionment/apportionment-2020-table01.xlsx` |
| 2010 apportionment population and seats | `www2.census.gov/.../apportionment/apport2010-table1.xls` |
| Mexican origin 2020 (full count) | Census API `2020/dec/ddhca`, table T01001, POPGROUP 4015 |
| Mexican origin under 18, 2020 | `2020/dec/ddhca` T02003 (T02002 fallback for the smallest state cell) |
| Mexican origin 2010 (full count) | Census API `2010/dec/sf1`, PCT011004 |
| Mexico-born, foreign-born by state | Census API ACS 5-year `B05006_150E`/`_138E`, `B05002_013E` (+ MOEs) |
| Unauthorized by state, 1990-2023 | Pew Research Center, `RE_2025.08.21_..._state-trends.xlsx` |
| Unauthorized by state, 2010-2019 | Center for Migration Studies, `CMS-data-undoc-state_2010-2019.xlsx` |
| Household child linkage | local IPUMS USA panel, `~/research-data/.../immigration_microdata.duckdb` (read-only) |
| Vintage 2024 state estimates | `www2.census.gov/.../popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv` |

## Outputs (`derived/`)

`apportionment_pop_2020.csv`, `apportionment_pop_2010.csv`, `state_counts.csv`,
`unauthorized_pew_by_state.csv`, `unauthorized_cms_by_state.csv`, `kids_ipums_ratio.csv`,
`mexborn_plus_uskids.csv`, `arm_<name>.csv` (one per arm, per state: base and counterfactual
population and seats), `arms_summary.csv`, `ec_arithmetic.csv`, `house_size_sensitivity.csv`,
`mc_<arm>.csv` + `mc_summary.csv`, `projection_2030.csv`, `last_seat_margins_2020.json`.

## Limits

Apportionment counts every resident regardless of immigration status, by constitutional design.
These arms remove people from the counts, not from the country, and hold the House at 435 and each
state's certified presidential winner fixed. The child linkage is a household proxy, not a parent
pointer. Pew figures are rounded to 5,000-25,000; ACS figures carry sampling error (both are
propagated in `robustness.py`).
