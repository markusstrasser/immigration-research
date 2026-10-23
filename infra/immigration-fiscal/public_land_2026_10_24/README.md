# Land under the case's public capital

This lane prices land beside each physical public-capital component in adopted case `oct16`.
It leaves the adopted case unchanged. Read [RESULT.md](RESULT.md) before interpreting a subtotal:
unknown ownership, unmapped sites, sale restrictions and overlapping rights do not become zero land.

## Reproduce

From the repository root, with the existing locked environment and the DuckDB spatial/httpfs
extensions used by the school lane:

```sh
uv run --no-project python3 infra/immigration-fiscal/public_land_2026_10_24/build.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/public_land_2026_10_24/ -q -s -p no:cacheprovider
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/public_land_2026_10_24 "uv run --no-project python3 {lane}/build.py"
```

`build.py` reexecutes itself with `-I` before parsing downloads, imports only trusted sibling source,
and invokes all three acquisition/normalization routes, the case contract, and `test_lane.py`.
This makes the requested single-build rerun exercise every new script. Acquisitions retain
existing raw files; source schemas and exact page counts fail loudly. Downloads live in separate
`_cache/roads`, `_cache/universes`, and `_cache/footprints` directories. The school lane's cache is
reused read-only. CPU time and peak resident memory are printed using Python `perf_counter` and
`resource.getrusage`; timing values are excluded from deterministic tables.

The first run requires network access. Cached reruns use the same primary snapshot. To acquire a new
snapshot, use a new dated lane rather than overwriting the raw records. No source over 10 GB or lane
cache over 5 GB is permitted. Full priced records are rederivable and stay in `_cache/priced_sites.parquet`.

Validation receipt, 2026-10-24: all 14 tests pass; the exact single-build `rerun_lane.py` command above
exited 0 with **IDENTICAL: 35/35 files unchanged**, with no script exemptions. The measured full
build took 35.954 seconds, including tests; peak process RSS was 2.831 GB on this Darwin host.

## Source and method register

| Source | Primary input, variables and use | Limitation |
|---|---|---|
| [FHFA WP 19-01](https://www.fhfa.gov/research/papers/wp1901), data v4.0 June 2024 | School cache `fhfa/csv/{xs_tract,xs_county,xs_state,panel_county,panel_state,std_params}.csv`, 2010 tract gazetteer; residential as-is land price/acre, average residential lot size, 2015→2022 county/state land growth | Single-family residential land; transfer to public parcels is modeled |
| [FHFA county HPI](https://www.fhfa.gov/data/hpi/datasets) | School cache `hpi/hpi_at_county.xlsx`; 2024/2022 all-transactions price growth | House-price growth proxies land-price growth after 2022 |
| [School-land lane](../school_land_2026_10_24/RESULT.md) | `derived/summary.json` and `schools.csv.gz`; acreage, school geography and three price arms | Source campus coverage and imputation retained; original pupil share differs from case key |
| [Census 2010 tract boundaries](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.2010.html) | School cache `tracts2010/`; containing tract for sites, exact park/tract intersections | Simplified shorelines; missing coastal geometry remains unpriced or uses authoritative source county |
| [Overture land use](https://docs.overturemaps.org/schema/reference/base/land_use/) and infrastructure, 2026-10-21.0 | Remote Parquet queries with US bounding-box and class pushdown; geometry, source tags, public/private owner and operator tags | Volunteer-map incompleteness; public operation is not proof of fee title |
| [USGS PAD-US](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-download), 4.1 Fee Managers | Public fee ownership STAT/DIST/LOC/TRIB, recreation designations SP/SREC/LP/LREC/REC; polygon areas and public-access codes | Includes undevelopable state-park land; excludes easements, federal estates and unselected designations |
| [FHWA 2024 HM-20](https://www.fhwa.dot.gov/policyinformation/statistics/2024/hm20.cfm) and [HPMS](https://data.transportation.gov/resource/42um-tgh5.json) | Mainline county/class/owner/toll aggregates plus county-summary local/rural-minor-collector miles; all 714 state×area×class mileage cells reconcile | Widths are design assumptions; toll IDs may cover managed lanes |
| [FHWA/ITE design tables](https://rosap.ntl.bts.gov/view/dot/42943/dot_42943_DS1.pdf) and [NCDOT ROW chapter](https://connect.ncdot.gov/projects/Roadway/Roadway%20Design%20Manual/09.%20Right%20of%20Way.pdf) | Parsed ROW widths by road class and urban/rural type; primary text guards retain exact table/range definitions | National transfer of typical design templates; no measured national ROW-width distribution |
| [NCES IPEDS HD2023](https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip) | Existing primary CSV and acquired dictionary; UNITID, CONTROL, ACT, coordinates and county | Institution control does not establish title to every campus; federal education is outside S&L college stock |
| [FEMA HIFLD hospitals](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/Hospitals_RAPT/FeatureServer/6) | OWNER, TYPE, STATUS, SOURCE, coordinates and county; public institution containment | Historical ownership and heterogeneous source dates; closed/defense sites excluded, unresolved scope held |
| [CMS Hospital General Information](https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0/download?format=csv) | Contemporary Hospital Ownership crosscheck, dictionary archived | Different Medicare universe, no coordinates; counts cannot expand HIFLD acreage |
| [HUD developments](https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/Public_Housing_Developments/FeatureServer/0) | Development code, quality/scattered-site flags and representative address point | A development point does not delineate its land; coarse/scattered points not matched to parcels |
| [USDOT BTS aviation facilities](https://services.arcgis.com/xOi1kZaI0eWDREZv/ArcGIS/rest/services/NTAD_Aviation_Facilities/FeatureServer/0), FAA NASR effective 2026/10/01 | PU publicly owned, O open, A airport; primary reported ACREAGE, reference point; [primary dictionary](https://doi.org/10.21949/1529011) parsed and gated | Missing acreage retained; reference point does not capture within-airport price variation; not federal air-traffic control sites |
| [Adopted case package](../main_case_2026_10_16/package.cjs) | `capitalMeta`, `evaluateFull`, typed coverage/count parts, college and health capital terms | National case allocation keys are retained; no new where-used factor for non-school land |

The acquisition manifests `derived/{roads_sources,universe_sources}.json` and footprint cache manifest
record primary URLs and hashes. `derived/footprint_sources.json` records ownership, area and overlap
coverage. `case_contract.cjs` calls the full case evaluator, rather than treating the rounded
`public_capital_rate_2026_10_24/derived/line_deltas.csv` as an exact allocation ledger.

## Valuation and allocation

`valuation.py` imports the existing school lane's price functions. There is one definition of the
2015→2022→2024 carry-forward and of the price arms: A prices every acre at the residential rate;
B uses 65% for source sites over two acres and 80% below two acres; C carries the vacant-lot
plattage cubic. These are conditional land-use constructions. A and C do not bound the true
opportunity cost of legally restricted parks or road easements.

Parks are intersected with the 2010 tracts. Overlapping park designations are assigned once by stable
source-ID priority; the original source site's acreage determines its B/C discount. For other
facilities, public ownership tags or containment of an authoritative public-institution point
identify known sites. Private-owner tags veto the point proxy. Same-line overlapping mapped sites
are dissolved into campuses before valuation. Unmatched sites receive no area expansion.

Roads use centerline miles × modeled ROW feet × 5,280 / 43,560. No road polygons are downloaded.
Arm C uses a representative one-mile strip, with 0.1- and 10-mile alternatives; county totals and
HPMS segmentation are not treated as parcel sizes. FAA's reported airport acres replace a map-based
airport-area proxy. Airport and other campus values use their reference/inside point's tract.

Each physical line is charged once. Signed fee-offset components share its land; they are not new
parcels. `case_contract.cjs` retains union completion, own coverage, selected count items, the college
response and item 21's health-capital rekeying. It independently closes their sum to the full
evaluator's capital-only 7% arm. The effective coefficient includes those components' responses, so
the charge is land × effective key-and-response × rate, with no depreciation. Schools also retain
their measured where-enrolled price factor; other lines use the national case key with geography
unmeasured. Applying the school's source pupil key reproduces $2.605156bn, separately from the
case-consistent school result.

The 2.42% column is the uniform rate requested in the brief. It is only a land-charge sensitivity:
the rate lane's paired-theta model has separate federal/state-local rates and a corporate-receipt
leg. Those changes to the existing case are not bundled into this lane's land increment.

## Failure regressions and checks

- Empty or wholly unlocated classes remain unpriced and do not crash the reused price engine.
- ArcGIS HTTP-200 error objects (including code 429) and truncated page sets fail loudly.
- Primary FAA definitions distinguish public ownership from public use and verify acre units.
- Case stock/key/response checks and the full 7% rate derivative include every post-engine capital term.
- Coverage and conditional land/structures ratios print for all classes/physical lines. Zero mapped
  acreage is never promoted to a measured zero national estate.
- LF CSV/JSON, finite numeric output and an explicit null complete-total field survive the rerun check.
- An initial combined class/spatial predicate selected a hash join. Partitioning by class selects
  DuckDB's spatial join; a probe reproduced the identical match-file hash in 3.89 seconds versus
  74.86 seconds. Same-line overlap queries use the same partitioning.
