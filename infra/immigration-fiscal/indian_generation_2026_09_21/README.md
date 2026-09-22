# Lane: Indian 2nd/3rd generation vs same-age 3rd+ NH whites

G2 was already on `indian_ledger_2026_09_18`. This lane adds G3+ (US-born, both parents US-area-born, `PRDASIAN=1`) on that ledger, pools ASEC 2022–2026 for own-person tax/earnings, and tabulates ACS 2023 income by age.

## Run

```bash
cd /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 infra/immigration-fiscal/indian_generation_2026_09_21/analyze_cps.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 infra/immigration-fiscal/indian_generation_2026_09_21/year_cluster.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 infra/immigration-fiscal/indian_generation_2026_09_21/analyze_acs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
    python3 infra/immigration-fiscal/indian_generation_2026_09_21/ledger_g3.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
    python3 infra/immigration-fiscal/indian_generation_2026_09_21/occ_split.py
```

`ledger_g3.py` imports `indian_ledger_2026_09_18/ledger_india.py` and `gen_ledger_extension_2026_09_16/extend_ledger.py`; it does not edit them.

## Inputs

| File | Where |
|---|---|
| CPS ASEC 2022–2023 | `latam_comparison_2026_09_17/_cache/{2022,2023}/asecpub2{2,3}csv.zip` |
| CPS ASEC 2024 | `same_year_tax_2026_09_20/_cache/asecpub24csv.zip` |
| CPS ASEC 2025 | `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` |
| CPS ASEC 2026 | `ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip` |
| MEPS 2024 | `sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/` |
| ACS 2023 1-year PUMS person | `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip` |

## Outputs (`derived/`)

| File | What |
|---|---|
| `cps_generation_years.csv` | Year × group × universe: n, BA, earnings, own tax minus cash, age-std |
| `cps_generation_pooled.csv` | Equal-year mean, adults 25–64 |
| `cps_generation_year_cluster.csv` | Between-year SEs of those means and of the white gap |
| `cps_generation_stock.csv` | All-age stock and mean age |
| `acs_age_bands.csv` | ACS 2023 PINCP/BA by age: India-born, US-born Asian Indian ancestry, US-born NH white |
| `india_g3_ledger.csv` | 2025 extended ledger, G3+ added; SDR SEs |
| `acs_occ_earnings.csv` | ACS 2023 employed 25–64 PINCP/WAGP by occupation bin |
| `cps_occ_earnings.csv` | ASEC 2022–2026 longest-job earnings by occupation bin |
| `occ_kitagawa.csv` | Mix vs within split of the earnings gap (IT vs not-IT, and 10 bins) |

## Verification

`ledger_g3.py` re-run from scratch: `cmp` identical on `india_g3_ledger.csv`. White-reference after-health $13,430.94 matches `indian_ledger_2026_09_18` to the cent. India-born and G2 gaps match that lane's published $+10,732$ and $+20,572$.
