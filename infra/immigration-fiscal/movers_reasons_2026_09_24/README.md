# Why US-born adults leave California (lane, 2026-09-24)

Results and their limits are in [RESULT.md](RESULT.md); the brief is [BRIEF.md](BRIEF.md). This
file says how to rebuild them.

## Inputs

All raw inputs sit under `_cache/` (git-ignored). Each fetch records its URL, byte count and
SHA256 in a manifest: `_cache/ipums/manifest.json` for the IPUMS extracts and
`_cache/public_manifest.json` for everything else.

| Input | Source | Script |
|---|---|---|
| IPUMS-CPS ASEC 1999–2025, every person, 35 variables (extract 2, 5,027,101 rows) | IPUMS API | `fetch_ipums.py` |
| IPUMS-CPS ASEC 2005–2025, interstate movers with REPWTP1–160 (extract 3, 59,734 rows) | IPUMS API | `fetch_ipums.py` |
| IPUMS published case counts for MIGRATE1 and WHYMOVE | cps.ipums.org | `fetch_public.py ipums_doc` |
| Census public ASEC microdata, movers, 2014, 2015, 2019–2025 | api.census.gov | `fetch_public.py cps_api` |
| ACS 1-year (2005–2024) and 5-year (2009–2024) state and county tables | api.census.gov | `fetch_public.py acs`, `acs5` |
| ACS state-to-state migration tables 2005–2024 | census.gov | `fetch_public.py s2s` |
| CPS historical migration Table A-1 | census.gov | `fetch_public.py cps_a1` |
| IRS SOI state migration files 2011–12 to 2022–23, county outflows 2018–19 to 2022–23, the 2022–23 California workbook | irs.gov | `fetch_public.py irs` |
| ITEP Who Pays? 7th edition, California and Texas | itep.org | `fetch_public.py itep` |
| Moving-cost sources the ledger reads (AMSA fact sheet, Bayer–Juessen, Kennan–Walker, IRS Table 1.4 for tax years 2014–2017) | as listed in `fetch_public.py` | `fetch_public.py lit` |

The literature notes in `lit/` quote further sources, cached under `_cache/lit/` by the workers
that read them. The ledger reads none of those files.

## Run order

Run from the repository root. The keys come from the untracked `acquire/config.local.env`; never
print them.

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
L=infra/immigration-fiscal/movers_reasons_2026_09_24
uv run --no-project python3 $L/fetch_ipums.py run            # skips extracts the manifest already holds
uv run --no-project python3 $L/fetch_public.py all           # idempotent, content-checked
export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 $L/build_cps.py                  # gate G1; writes _cache/build/*.parquet
uv run --no-project --with xlrd python3 $L/check_census.py   # gate G2
uv run --no-project python3 $L/reasons.py                    # questions 1 and 4 (counts)
uv run --no-project python3 $L/q2_gradient.py                # question 2
uv run --no-project python3 $L/irs_flows.py                  # question 3; gate G3
uv run --no-project --with xlrd --with beautifulsoup4 python3 $L/ledger.py   # question 4 costs, tax transfer, winners and losers
```

`build_cps.py`, `check_census.py` and `irs_flows.py` exit non-zero when a gate fails. `reasons.py`
stops if a pooled per-year count differs from the mean of its single years.

## Outputs (`derived/`, tracked)

| File | Contents |
|---|---|
| `gate_extract.csv`, `gate_census_check.csv`, `gate_movers_count.csv`, `gate_irs.csv` | gates G1–G3 |
| `census_allocation_flags.csv` | reasons allocated by the Census hot deck, 2019–2025 |
| `whymove_counts_by_year.csv` | unweighted reason codes by year, all movers |
| `reasons_ca_leavers.csv`, `reasons_compare.csv`, `reasons_ca_by_year.csv`, `reasons_ca_by_subgroup.csv` | question 1 |
| `ppic_crosscheck.csv`, `income_weighted_shares.csv`, `design_factor.json` | question 1 checks and variance calibration |
| `q2_regressions.csv`, `q2_bins.csv`, `q2_state_scatter.csv`, `q2_same_county_descriptive.csv` | question 2 |
| `irs_ca_tx.csv`, `irs_ca_austin.csv`, `tax_transfer.csv` | question 3 |
| `q4_counts.csv`, `q4_counts_by_year.csv`, `q4_costs.csv`, `irs_moving_expenses.csv` | question 4 |
| `winners_losers_rows.csv` | rows for the winners-and-losers ledger |
