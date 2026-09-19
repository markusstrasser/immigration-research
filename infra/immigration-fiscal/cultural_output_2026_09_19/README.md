# Cultural output lane — Mexican-origin creative supply, canon share, and variety saturation

Measures what the repo has so far carried as an unpriced claim on both sides:
whether the Mexican-origin population supplies more, less or the same creative
output as SES-matched whites, and whether the variety natives consume
(restaurants, music) keeps scaling with group size or flattens.

Findings and their caveats are in `RESULT.md`. This file is how to re-run it.

## Layout

```
scripts/    numbered, run in order; each one validates its inputs by content
_cache/     raw downloads and the PUMS column subset (gitignored, ~4 GB)
derived/    every table the memo cites (all small; nothing over 5 MB)
logs/       fetch logs
```

## Environment

Every script runs under one interpreter spec. Never bare `python3`.

```bash
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/cultural_output_2026_09_19
set -a; . ../acquire/config.local.env; set +a     # CENSUS_API_KEY, never echoed
UV='uv run --no-project --with "pandas>=2" --with "numpy>=2" --with duckdb --with requests --with pyarrow'
```

## Run order

```bash
# Arm A — creative labour supply (ACS 2024 1-yr PUMS)
unzip -o -d _cache/pums \
  ~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip \
  psam_pusa.csv psam_pusb.csv
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with duckdb --with pyarrow python3 scripts/01_build_pums_parquet.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with duckdb --with pyarrow python3 scripts/02_arm_a_creative_labour.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/13_arm_a_cps_generation_check.py        # third-plus check

# Arm B — awards and canon
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/05_fetch_surnames.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/06_fetch_awards_wikidata.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/09_fetch_education_benchmarks.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 scripts/10_classify_awards.py

# Arm D — variety saturation
#   the Overpass sweep takes 1-3 h; two workers halve it
for r in 0 1; do LANE_MOD=2 LANE_REM=$r PYTHONUNBUFFERED=1 nohup \
  uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/03_fetch_osm_restaurants.py > logs/osm_fetch_$r.log 2>&1 & done
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/04_fetch_cbsa_covariates.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with shapely \
  --with pyshp python3 scripts/07_build_cbsa_restaurant_panel.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with duckdb --with pyarrow python3 scripts/08_arm_d_cooks.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with statsmodels python3 scripts/11_arm_d_elasticity.py
#   bias check: does OSM coverage move with the Mexican-origin share?
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with requests --with statsmodels python3 scripts/14_osm_coverage_check.py

# Arm E — Latin music share
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with requests \
  --with pypdf --with fonttools python3 scripts/12_arm_e_music.py

# Render RESULT.md from its template, substituting arm B and D numbers
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 scripts/15_fill_result.py

# Reproduction check: re-runs all fifteen scripts and cmp's derived/
bash scripts/16_verify_reproducible.sh
```

`RESULT.md` is generated: edit `scripts/RESULT_template.md` and re-run script 15,
so no arm D figure in the memo is hand-copied.

`LANE_STATES` overrides the state partition, which is how the states carrying the
high end of the Mexican-origin share (TX, NM, NV, UT) were fetched first when the
Overpass endpoint was slow:

```bash
LANE_STATES="TX,NM,NV,UT" LANE_REM=9 PYTHONUNBUFFERED=1 nohup \
  uv run --no-project --with "pandas>=2" --with requests \
  python3 scripts/03_fetch_osm_restaurants.py > logs/osm_fetch_prio.log 2>&1 &
```

Arm C (patent and copyright registrations) was stopped; the probe evidence is in
`derived/arm_c_stop_note.md`.

## Inputs

| source | where | note |
|---|---|---|
| ACS 2024 1-year PUMS person file | `~/research-data/.../acs_pums_2024_1yr/csv_pus.zip` (read-only) | 3,422,888 records, 80 replicate weights |
| ACS 5-year 2023, CBSA level | Census API `acs/acs5`, B03001 / B19013 / B01003 | 935 CBSAs |
| ACS 1-year 2010-2024, national | Census API, C15002I and B15002 | Hispanic share of BA+ adults |
| CPS ASEC March 2025 | Census API `cps/asec/mar` (`for=state:*`, not `us:*`) | parental nativity, generation check |
| Census 2010 surname file | Wayback capture of `www2.census.gov/topics/genealogy/2010surnames/names.zip` | direct fetch is blocked, see below |
| Wikidata award statements | `query.wikidata.org/sparql` | 27 award categories |
| OpenStreetMap restaurants | Overpass API, per state | cuisine tags |
| TIGER CBSA boundaries 2023 | `www2.census.gov/geo/tiger/GENZ2023` | point-in-polygon assignment |
| RIAA year-end Latin revenue reports | `riaa.com` PDFs | parsed here, not quoted from search results |

## Host quirks found on 2026-09-19 (all encoded in the scripts)

- `www2.census.gov/.../names.zip` answers scripted clients with an HTML
  "Request Rejected" page **under HTTP 200**; a browser user-agent and a
  referer header do not help. The Wayback capture works and arrives
  gzip-wrapped. Every fetch is validated by magic bytes, never by status code.
- The Overpass interpreter rejects a browser user-agent with HTTP 406 but
  accepts a descriptive one. `overpass.kumi.systems` accepts connections and
  never answers, so only `overpass-api.de` is used, with slot polling.
- Alaska's `admin_level=4` area query does not return inside the Overpass time
  limit; Alaska is fetched by bounding box instead. The boxes spill into
  Canada, and those points are dropped by the CBSA point-in-polygon step.
- The CPS ASEC API has no `us:*` geography; it needs `for=state:*`.
- Overpass throughput on 2026-09-19 varied by two orders of magnitude between
  states, from 20 s to 18 min for comparable query sizes, with the announced
  backend rotating between requests. The state sweep is therefore restartable
  and cache-first: a cached state file counts only if its JSON parses and its
  feature count clears a per-state floor, so an interrupted fetch is redone
  rather than trusted. State files are written atomically, since two workers
  can reach the same state.
- An HTTP error raised by `requests` prints the full request URL, which carries
  the Census API key. Script 13 catches `HTTPError` and prints only the status
  code for that reason.

## Reproducibility

Every script is cache-first and deterministic: re-running the whole chain over
a warm `_cache/` rewrites `derived/` byte for byte. Verified by copying
`derived/`, re-running, and comparing with `cmp` (see `RESULT.md`).
