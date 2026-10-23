# School land, 2024

Market value of the land under US public K-12 schools, nationally and where the Mexican-origin group's
pupils enroll, and the group's annual charge on it at the case's flat-real rate (2.081%; land does not
depreciate), with 3% and 7% beside. Beside the case, not adopted. Results and caveats: [RESULT.md](RESULT.md);
brief: [BRIEF.md](BRIEF.md).

## Run (from the repository root)

```sh
uv run --no-project python3 infra/immigration-fiscal/school_land_2026_10_24/acquire.py
uv run --no-project --with duckdb python3 infra/immigration-fiscal/school_land_2026_10_24/acquire_overture.py
uv run --no-project python3 -I infra/immigration-fiscal/school_land_2026_10_24/fhfa_extract.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/school_land_2026_10_24/build.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_land_2026_10_24/test_lane.py -q -p no:cacheprovider
```

Reproduction check (IDENTICAL 15/15, exit 0 on 2026-10-24):

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/school_land_2026_10_24 \
  "uv run --no-project python3 {lane}/acquire.py" \
  "uv run --no-project --with duckdb python3 {lane}/acquire_overture.py" \
  "uv run --no-project python3 -I {lane}/fhfa_extract.py" \
  "uv run --no-project --with duckdb python3 {lane}/build.py" \
  "uv run --no-project python3 -m pytest {lane}/test_lane.py -q -p no:cacheprovider"
```

The fetches are idempotent (an existing file is kept). The Overture pull is a remote DuckDB query, one
`SELECT` per box (CONUS, Alaska, Hawaii) joined by `UNION ALL`. An `OR` of boxes defeats row-group
pruning and read 2.5 GB in 20 minutes; the union reads in about 3 minutes. `_cache/` holds 402 MB, and
`derived/acquired_sources.json` records each file's URL, size and sha256. The build takes about 10 s.

## Inputs (all fetched by the scripts, parsed from the primary files)

| Input | Use |
|---|---|
| NCES EDGE public-school geocodes 2023-24; CCD 029 directory, 052 membership, 129 characteristics 2023-24 | school universe, points, K-12 and Hispanic pupils, charter and virtual flags |
| Overture Maps 2026-10-21.0 `base/land_use`, subtype education (OSM-derived) | campus polygons (school, kindergarten, schoolyard; education as fallback) |
| FHFA Working Paper 19-01 land data v4.0 (June 2024) | tract, county and state as-is residential land value per acre (pooled cross-section, 2015 prices); county/state panel 2012-2022; county lot-size elasticity bL |
| FHFA annual county all-transactions HPI (updated 2026-03-31) | carry land prices 2022 to 2024 |
| Census 2010 cartographic tract boundaries (500k) | the tract vintage FHFA uses (99.97% of FHFA tracts are 2010 tracts) |
| California School Campus Database 2025 (GreenInfo Network), FeatureServer layers 0 and 2 | parcel-aligned acreage benchmark |
| `school_cost_where_enrolled_2026_09_24` (`ccd.py`, `weighting.py`, imported by path) | membership aggregation and the district Mexican-origin share |
| `school_capital_return_2026_09_26/derived/summary.json` | pupil share s = 0.17481, K-12 structures $2,663.9bn |
| `main_case_2026_10_16/derived/summary.json` | case rate (`v9.one_rate.flat_real_equivalent`) and headline band |

Price-discount sources: Albouy, Ehrlich & Shin (2018, REStat 100(3), Table A.1: the vacant-land plattage
cubic) and Gyourko & Krimmel (2021, NBER w28993: the 65%/80% developable shares and four priced parcels).

## Outputs (`derived/`)

- `summary.json`: inputs, universe, matching, acreage and imputation fit, prices, the four arms, B's parts,
  sensitivities, validation and discount evidence.
- `arms.csv`: one row per arm, with national value, land/structures ratio, where-enrolled ratio and charges
  at the three rates.
- `by_state.csv`: schools, match rates, acres (and imputed acres), value per arm, group pupils.
- `schools.csv.gz`: one row per school, with acreage source, tract, price level, price and value per arm.
- `validation_cscd_ca.csv`: California schools against CSCD campus acreage.
- `discount_evidence.csv`: G&K parcels against FHFA's county price per acre.
- `acquired_sources.json`: the fetch manifest.

The gates in `test_lane.py` check the match-rate floors, the CSCD acreage error, the finite and ordered
land/structures ratios, the inputs against the case and capital lanes, the charge arithmetic, that the
school file adds to the totals, that group pupils agree with the weighting lane, and LF line endings.
