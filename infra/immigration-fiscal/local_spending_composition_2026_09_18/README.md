# Lane: local spending composition and the immigrant share (2026-09-18)

Tests, on US local government finances, the composition claim Alex Tabarrok endorsed on
2023-12-02: that unauthorized inflows "reduce local public spending, and shift it away from
education towards law-and-order." The paper is Tiburcio and Camarena, *The Local Reaction to
Unauthorized Mexican Migration to the US* (2023 job-market version; current version May 2025).

Their treatment is a confidential Mexican consular-ID file and cannot be rebuilt. This lane runs
the **observable correlate** instead: county long differences in the Hispanic, foreign-born and
Mexico-born share of population against the same Census local-finance composition outcomes, over a
longer window. **Every estimate here is descriptive.** The post-2008 shift-share instrument is not
used (ladder 136).

## Inputs

| Input | Source | Cached as |
|---|---|---|
| Paper, Nov 2023 version | Wayback `20231203002131` of `ernestotiburcio.files.wordpress.com/2023/11/…pdf` (origin now 404) | `_cache/tiburcio_camarena_2023.pdf` |
| Paper, May 2025 version | `https://scholar.karaross.com/working-papers/localreactions-current.pdf` | `_cache/tc_current_2025.pdf` |
| Local government finances, individual unit files | census.gov, 2012 and 2017 under `gov-finances/datasets/<y>/public-use-datasets/`, 2018-2023 under `gov-finances/tables/<y>/` | `_cache/indunit_<year>.zip` |
| County shares | Census API, ACS 5-year `B03003` `B05002` `B05006` `B01001` `B19013` for 2009, 2012, 2017, 2022; 2000 Census `sf1` `P008` and `sf3` `P021` | `_cache/acs/` |
| Deflator | BLS `CUUR0000SA0` annual averages, CPI-U all items | `_cache/cpi.json` |

There is **no individual-unit file for 2007** anywhere on census.gov, and none for 2013-2016. The
2007 wave therefore comes from the Willamette Government Finance Database, whose 2012, 2017 and 2022
waves match the Census build to better than 0.25% on every function (correlation 0.99999+). That
archive downloads from Google Drive at about 35 kB/s to this machine; `modal_fetch_gfd.py` pulls it
in a container in 8 seconds at 39 MB/s, and `modal_gfd_2007.py` filters and aggregates its 2.9 GB
CSV in the container so only a 1 MB county file crosses the wire.

## Run

```bash
cd infra/immigration-fiscal/local_spending_composition_2026_09_18
UV='uv run --no-project'
set -a; . ../acquire/config.local.env; set +a        # CENSUS_API_KEY, never printed

PYTHONUNBUFFERED=1 $UV python3 fetch_census_finance.py      # ~50 MB, resumable, retries
PYTHONUNBUFFERED=1 $UV python3 pull_acs_counties.py         # ~2 min, cached per wave
PYTHONUNBUFFERED=1 $UV python3 build_county_panel.py        # ~2 min
PYTHONUNBUFFERED=1 $UV --with 'numpy>=2' python3 estimate_composition.py
```

The 2007 wave needs two Modal steps first; `build_county_panel.py` picks up
`_cache/gfd_county_waves.csv` automatically when it is there and skips 2007 when it is not:

```bash
modal run modal_fetch_gfd.py                  # 341 MB into the `gfd` volume, ~8 s
modal run modal_gfd_2007.py                   # aggregate to counties in the container
modal volume get gfd gfd_county_waves.csv _cache/gfd_county_waves.csv
```

## Scripts

| File | What it does |
|---|---|
| `fetch_census_finance.py` | downloads the individual-unit zips, five retries with backoff, skips what is cached |
| `pull_acs_counties.py` | county ACS shares; resolves `B05006`'s Mexico cell by label per year, since its number moves (138 in 2009, 137 in 2012, 139 in 2017, 160 in 2022) |
| `build_county_panel.py` | parses both fixed-width layouts, keeps local units, sums direct general expenditure by function to counties |
| `estimate_composition.py` | long differences with state fixed effects and state-clustered SEs; every arm below |
| `modal_fetch_gfd.py` | container-side Google Drive fetch for the historical database |
| `modal_gfd_2007.py` | streams the 2.9 GB database CSV in the container and returns a county-by-wave file |

## Outputs

| File | Contents |
|---|---|
| `derived/county_finance.csv` | county × year direct general expenditure by function, 2007, 2012 and 2017-2023 |
| `derived/county_shares.csv` | county × wave population, Hispanic, foreign-born, Mexico-born, under-19, 65+, median household income |
| `derived/composition_means.csv` | national composition by wave, weighted and unweighted |
| `derived/estimates_composition.csv` | 206 estimates across 38 arms |
| `derived/influence_education_share.csv` | leave-one-county-out on the weighted education-share coefficient, 40 largest counties |
| `derived/loo_state_logratio.csv`, `derived/loo_state_logratio_2007_2022.csv` | leave-one-state-out on the log law-and-order-to-education ratio, both windows |

## Two checks worth knowing about

**The county sums lose nothing.** Summing the 2012 county panel back to national totals reproduces
the Census's own `12statetypepu.txt` local-government aggregate exactly, function by function:
total direct general expenditure $1,422.9bn, education $597.3bn, police $84.0bn, judicial $21.6bn.

**Connecticut drops out after 2012.** The 2022 finance file codes Connecticut as the nine planning
regions (FIPS 09110-09190) while ACS 2022 still uses the eight counties (09001-09015), so no
Connecticut county survives the balanced-panel filter. Connecticut is absent from the sample rather
than mismatched.
