# Hedonic composition lane — what neighbourhood composition is worth in housing prices

Within-metro capitalisation of Hispanic, Mexican-origin and foreign-born neighbourhood
share into rents and house values, 2013–2023, reproducing the design of
**Saiz and Wachter (2011), "Immigration and the Neighborhood," American Economic Journal:
Economic Policy 3(2): 169–188, DOI 10.1257/pol.3.2.169.**

> The lane brief cited this paper as *REStat* 93(1):169–188, DOI `10.1162/REST_a_00052`.
> That DOI resolves to Cohen-Cole, "Credit Card Redlining." The correct venue, volume and
> page range are the AEJ:EP ones above; the page numbers in the brief were right.

## Verdict

See `RESULT.md`. In one line: the negative within-metro composition gradient appears only
when the price measure and the composition measure come from the same ACS sample, and it
reverses on an independent price index.

## How to run

Everything runs through `uv run --no-project`; there is no project virtualenv and no
`pip install`. Run from this directory, in this order. Steps 1–3 hit the network and cache
under `_cache/` (gitignored); steps 4–8 are pure computation over the cache.

```bash
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/hedonic_composition_2026_09_19
set -a; . ../acquire/config.local.env; set +a        # provides CENSUS_API_KEY

UV="uv run --no-project --with pandas>=2 --with numpy>=2 --with statsmodels --with scipy"

# 1. ACS 5-year tract tables, 3 vintages x 51 states (8 parallel workers, ~6 min)
PYTHONUNBUFFERED=1 uv run --no-project --with requests python3 src/fetch_acs.py

# 2. ZCTA composition + tract margins of error (~15 min; the ZCTA calls are slow)
PYTHONUNBUFFERED=1 uv run --no-project --with requests python3 src/fetch_extra.py

# 3. Bulk files that are not on the API (see "Manual downloads" below)

# 4. Geography crosswalks -> derived/geo_*.csv
PYTHONUNBUFFERED=1 uv run --no-project --with pandas>=2 --with numpy>=2 --with xlrd \
    python3 src/build_geo.py

# 5. Tract long-difference panel -> derived/tract_panel.csv
PYTHONUNBUFFERED=1 $UV python3 src/build_panel.py

# 6. Estimator self-test (must print ALL ESTIMATOR CONTROLS PASSED)
PYTHONUNBUFFERED=1 $UV python3 src/test_estim.py

# 7. Estimation
PYTHONUNBUFFERED=1 $UV python3 src/analyze.py        # OLS / gravity IV / shift-share IV
PYTHONUNBUFFERED=1 $UV python3 src/analyze2.py       # placebo, cross-period, heterogeneity, metro
PYTHONUNBUFFERED=1 $UV python3 src/zillow.py         # independent-outcome arm
PYTHONUNBUFFERED=1 $UV python3 src/attenuation.py    # ACS sampling-error correction
PYTHONUNBUFFERED=1 uv run --no-project --with pandas>=2 --with numpy>=2 \
    python3 src/dollars.py                           # dollar translation

# 8. Reproducibility gate
bash src/verify_repro.sh
```

### Manual downloads (step 3)

`src/fetch_acs.py` and `src/fetch_extra.py` cover the API. These four files come from
`www2.census.gov` and `files.zillowstatic.com` and are fetched with `curl --http1.1`;
**each one must be validated after download, because census.gov silently returns truncated
bodies** (this bit the lane twice; see "Traps" below).

| Cached as | Source URL | Validate by |
|---|---|---|
| `_cache/cbsa_list1_2013.xls` | `https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2013/delineation-files/list1.xls` | parses with `xlrd`, 1,882 counties |
| `_cache/gaz_tracts_2019.zip` | `https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2019_Gazetteer/2019_Gaz_tracts_national.zip` | unzips to 74,001 tracts |
| `_cache/tab20_tract20_tract10.txt` | `https://www2.census.gov/geo/docs/maps-data/data/rel2020/tract/tab20_tract20_tract10_natl.txt` | **56 distinct state codes**, 126,451 lines, 18,686,287 bytes |
| `_cache/zcta_county_rel_10.txt` | `https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt` | 44,410 lines |
| `_cache/zillow/zip_zhvi.csv` | `https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv` | byte count equals `Content-Length` (123,559,595) |
| `_cache/zillow/zip_zori.csv` | `https://files.zillowstatic.com/research/public_csvs/zori/Zip_zori_uc_sfrcondomfr_sm_month.csv` | byte count equals `Content-Length` (10,023,480) |

The metro-level Zillow files under `~/research-data/immigration-fiscal/data/external/urban_housing/zillow/`
are read-only and were not touched; this lane pulls its own ZIP-level copies.

## Inputs

- **ACS 5-year**, vintages 2013 (2009–2013), 2018 (2014–2018), 2023 (2019–2023), census-tract
  and ZCTA geography, via `api.census.gov`. Tables B03002, B03001, B05002, B05006, B25064,
  B25077, B25003, B25002, B25024, B25035, B19013, B15003, plus margins of error for the
  share numerators and denominators.
- **Zillow** ZHVI (ZIP, smoothed, seasonally adjusted, 33rd–67th percentile tier) and ZORI
  (ZIP, smoothed), annual means at the ACS period midpoints 2011 / 2016 / 2021.
- **Geography**: 2013 OMB CBSA delineations, 2019 tract gazetteer (interior points and land
  area), 2020→2010 tract relationship file, 2010 ZCTA→county relationship file.

## Outputs (`derived/`)

| File | What it holds |
|---|---|
| `tract_panel.csv` | tract long-difference panel, 2010 tract definitions, periods A and B |
| `est_universe_rent.csv`, `est_universe_value.csv` | estimation samples with instruments attached |
| `zcta_panel.csv` | ZCTA panel with Zillow indices merged |
| `results_main.csv` | 228 estimates: OLS specs 1–3, gravity IV, shift-share IV, by treatment, sample, period |
| `results_placebo_crossperiod.csv` | placebo, forward arm, same-period reference on one tract set |
| `results_heterogeneity.csv` | Saiz–Wachter Table 2 analogues, tipping, supply-response split |
| `results_metro.csv`, `metro_rent.csv`, `metro_value.csv` | metro-level demand effect |
| `results_zillow.csv` | independent-outcome arm, including matched-row head-to-head |
| `results_attenuation.csv` | ACS reliability ratios and corrected coefficients |
| `results_dollars.csv`, `dollars_summary.txt` | dollar translation |
| `geo_*.csv`, `build_panel_report.txt`, `analyze_notes.txt` | crosswalks and build logs |

## Design

Long differences on fixed 2010 census tracts within CBSA:

```
dlog(P_it) = a_{CBSA,period} + L * d(group share)_it + dZ_it * A + X_i,t0 * B + e_it
```

matching Saiz and Wachter's first-differences equation (their p. 173). Weights are initial
owner-occupied units for values and initial renter-occupied units for rents; fixed effects
are CBSA × period; standard errors are clustered on CBSA (the paper clusters on tract).
Period A is ACS 2013 → 2018 and needs no boundary crosswalk; period B is 2018 → 2023 with
2020 tracts aggregated into their dominant 2010 parent (92.7% of 2020 tracts sit at least
99% inside one parent).

Identification arms: OLS (three specifications), the paper's own geographic-diffusion
"gravity pull" instrument and its interactions, a Card-style shift-share on nine origin
regions, a placebo, a forward arm using independent ACS samples for treatment and outcome,
and an independent price index (Zillow).

## Traps this lane hit

1. **census.gov returns truncated bodies with HTTP 200.** `variables.json` truncated at the
   same byte count on eight consecutive attempts, and `curl -C -` resumed into a no-op. The
   tract relationship file truncated to 39 of 56 state codes, which silently dropped ~9,000
   2020 tracts concentrated in the tail of the FIPS order. **Validate content, never size
   alone, and never trust a single download.** Replacing `variables.json` with the
   table-scoped `groups/B05006.json` endpoint avoided the problem entirely.
2. **B05006 line numbers move between vintages** (Mexico is `B05006_138E` in 2013 and not in
   2023). `src/fetch_acs.py` resolves them by normalised label path per vintage.
3. **Connecticut replaced counties with planning regions in 2022**, so 2023 ACS county codes
   do not match the 2020 relationship file. About 880 CT tracts drop out of period B.
4. **ACS top codes** (rent 2,001 in 2013 and 3,501 later; value 1,000,001 in 2013 and
   2,000,001 later) are detected as a repeated series maximum and dropped.
5. **A single-origin shift-share is not an instrument.** `bartik_mex` reduces to the initial
   Mexican-born share times a scalar, so it carries no shift variation; it is reported but
   excluded from any headline.
