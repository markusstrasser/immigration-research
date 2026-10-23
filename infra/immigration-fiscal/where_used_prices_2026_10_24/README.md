# Where-used college and park prices — oct16

Read [RESULT.md](RESULT.md) before using a factor. This is a read-only sensitivity
lane on `main_case_2026_10_16`, not an adoption. Two proposed operating refinements
are already included; a complete national replacement-cost correction is not
identified. [CALCULATION: `build.py`, `parks.py`, `case_prices.cjs`]

## Reproduce

Run from the repository root with the existing locked environment and Bun:

```sh
uv run --no-project python3 -I infra/immigration-fiscal/where_used_prices_2026_10_24/acquire.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -I infra/immigration-fiscal/where_used_prices_2026_10_24/build.py
uv run --no-project python3 -I -m pytest infra/immigration-fiscal/where_used_prices_2026_10_24/test_lane.py -q
uv run --no-project python3 -I scripts/rerun_lane.py infra/immigration-fiscal/where_used_prices_2026_10_24 \
  "uv run --no-project python3 -I {lane}/acquire.py" \
  "uv run --no-project python3 -I {lane}/build.py" \
  "uv run --no-project python3 -I -m pytest {lane}/test_lane.py -q"
```

`build.py` executes `parks.py` and `case_prices.cjs`, checking their exit codes.
CSVs use LF. Python reads downloads with `-I`, explicit text dtypes and bounded
PUMS chunks. Timings and RSS use `time.perf_counter()` and `resource.getrusage()`;
no `/usr/bin/time`, `ps` or `sysctl`. The recorded full build took about 30 s,
375 MB maximum parent-process RSS; children print their own RSS. Timing is stdout,
not a nondeterministic derived file. [CALCULATION: RESULT execution log]

## Primary inputs

`derived/acquisition.json` pins URLs, ZIP members, bytes and SHA256 for 14 new
source/codebook files under ignored `_cache/ipeds/` and `_cache/parks/`.
`sources.json` and `park_sources.json` fingerprint reused primary inputs.

| Input | Primary path / official route | Use |
|---|---|---|
| IPEDS FY2023 GASB finance, annual FTE, finance reporting links | `sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/{F2223_F1A,EFIA2023,FLAGS2023}.zip`; [NCES data center](https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?gotoReportId=7&rtid=7&year=2023) | Functional expenses, sales, assets, finance parent/child links |
| IPEDS HD2023 and EF2023A | `affirmative_action_cost_2026_09_24/_cache/ipeds/{HD2023,ef2023a}.csv` | Public institutions and fall FT/PT undergraduate/graduate enrollment by race |
| IPEDS EFFY2023 and F2223_F2 | Lane `_cache/ipeds/`, with dictionaries | Revised annual race/attendance counts; public FASB finance inventory |
| ACS 2024 one-year person PUMS | `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`; [official ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip) | `STATE PWGTP SCH SCHG HISP POBP`: public-college state/degree origin ratios |
| CoG FY2022 finance and government directory | `receipt_side_long_run_2026_09_28/_cache/census_2022_individual_unit_file.zip`; [official ZIP](https://www2.census.gov/programs-surveys/gov-finances/tables/2022/2022_Individual_Unit_File.zip) | Municipal current operations E61 and PID place identifiers; documentation in ZIP |
| ACS 2024 five-year B03001 | Lane `_cache/parks/acs5_2024_{place,us}.json`; existing school lane `_cache/acs5_2024_B03001_county.json`; [codebook](https://api.census.gov/data/2024/acs/acs5/groups/B03001.json) | `B03001_001E` population, `B03001_004E` Mexican origin |
| Case state-price primary inputs | FY2024 individual-unit state/type finance, Census Vintage 2024 population, CPS ASEC 2025 person/household/base weights | Reproduce FY2024/direct/group/parks+libraries index before refining it |
| TPL City Park Facts 2024 | Lane `_cache/parks/`, [primary downloads](https://www.tpl.org/park-data-downloads) | Public operating spending, construction/land flow, acreage and methodology; diagnostic city sample |
| Census classification manual | Lane `_cache/parks/census_classification.pdf`, [official](https://www2.census.gov/govs/class/classfull.pdf), printed p.93 | Function 61 includes culture, museums, zoos, stadiums and convention facilities |

The external source disk unmounted during the run. `acquire.py` recovered five
**identical-hash** public files into `_cache/source_mirror/`, retaining their
original source identities. `acquire.source()` is the single resolver used by both
builders. It prints mirrored reads; missing or changed bytes stop. No raw source
was moved or changed and no new release substitutes for a pin. The ignored recovery
receipt records original paths, URLs and hashes. Cache is about 616 MB, below 5 GB.

## College method

Reconstruct the existing E&R key by finance unit:

```
g_i = (Mexican_UG_FTE_i + 2*Mexican_GR_FTE_i) / (UG_FTE_i + 2*GR_FTE_i)
S_ER = sum(g_i * instruction_and_support_i) / sum(instruction_and_support_i)
```

ACS state/degree ratios reproduce the adopted six-decimal serialization for cells
with at least 100 records; thin cells use the state pooled ratio. Unrounded ratios
are retained. A new asset share is divided by this **existing cost-weighted key**.
The college/library blend keeps its library share unchanged.

Annual Hispanic FTE uses attendance-weighted headcounts normalized to actual EFIA
level FTE; race-specific credit hours are unavailable. Annual state/degree weights
are raked to the case's existing **college** distribution, not K-12 geography.
Graduate weights 1/2/3 are assumptions. Every arm preserves the case's overall
cost-adjusted group-FTE share. Inspect finance-dollar coverage: system offices
without assigned students hold material assets. Negative constructed net-plant
values are screened out. Public FASB units remain an explicit uncovered inventory.

## Parks method

Join PID **state+place** to ACS; do not assign a city's budget to its headquarters
county. Consolidated-government mismatches stay unpriced. Group allocation is
`E61_i * Mexican_i / population_i`, a residence proxy for use.

For the conditional fiscal bridge, `w_s` is the existing case state weight, `I_s`
its FY2024 E61+F61+E52+F52 relative price, `b_s` the FY2022 matched municipal E61
fraction of that state's same budget, and `f_s` its within-state municipal factor:

```
delta_index = sum(w_s * I_s * b_s * (f_s - 1))
delta_case = full_unpriced_recreation_exposure * (48.901 / 54.483657029) * delta_index
```

The existing state-price correction stays in place. Federal, library, nonmunicipal,
construction and capital allocations receive no municipal factor. Fiscal-year,
cash-to-NIPA, residence-to-use and population-addition transport are assumptions.
TPL's exact-FIPS sample excludes PS-prefixed regional systems. Construction and
acreage do not identify monetary capital stock.

## Case integration and outputs

Every scenario calls `evaluateFull` on both methods at specifications 16/11.
Scoped capital includes engine, completion, item15, one-rate, coverage and count
parts. Scoped repricing entries pass through the engine as correction constants;
gates verify exact deltas and unchanged original receipts, capital and post totals.
This preserves all existing machinery without editing the adopted package.

- `colleges.json`, `college_factors.csv`: principal key, factors and limitations.
- `college_units.csv`, `college_states.csv`, `college_raking.csv`, `acs_college_states.csv`: weights and audit trail.
- `college_finance_coverage.csv`, `college_unallocated_finance.csv`, `college_public_fasb.csv`: uncovered finance and bounds.
- `parks.json`, `park_municipalities.csv`, `park_states.csv`, `park_unmatched.csv`, `park_tpl_cities.csv`: geographic prices, coverage and bounds.
- `case_prices.json`, `case_scenarios.csv`, `case_scenario_methods.csv`: full-post exposures, gates, methods, ends and separate K-12 denominator readings.
- `acquisition.json`, `sources.json`, `park_sources.json`: primary provenance.
- [failure-catalog.md](failure-catalog.md): guards and regressions.

Independent review covered all five source files including `.cjs`, outputs and
principal callers, and independently passed all 15 tests. It found no material
implementation defect; it did not validate the unresolved empirical bridges.
