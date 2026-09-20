**Custody/offense scope, 2026-09-20:** These are felony arrest charges, not civil ICE detention, convictions or distinct incidents. Named offenses allow narrower comparisons; the residual category is not certified immigration-offense-free. Unit-cost weighting is a scenario, not observed government spending. See the [reporting and fiscal rule](../../../research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md).

# First-generation crime, cost-weighted (Texas felony arrest charges 2012–2018)

Question: the foreign-born are arrested less often than the US-born; is their offence mix costlier, so that the gap narrows or reverses once each charge carries its social cost?

Run (from the repo root):
```
uv run --no-project --with "pandas>=2" python3 infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/tabulate_texas.py      # raw counts by status × offence
uv run --no-project --with "pandas>=2" python3 infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/firstgen_cost_weighted.py # derived/*.csv, audit.json
uv run --no-project --with "pandas>=2" python3 infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/per_year_check.py       # per-year ratio stability
```
Inputs: `~/research-data/immigration-fiscal/data/external/crime_frontier/light_texas/124923-V1.zip` (Light, He & Robey PNAS 2020 replication package), unzipped to `_cache/light_texas/`; ACS 1-year PUMS API tabulations of Texas population by CIT × AGEP for 2015 and 2018 in `_cache/tx_age_by_cit_raw.txt` (key redacted; re-pull with `CENSUS_API_KEY` from `acquire/config.local.env`).
Unit costs: McCollister, French & Fang 2010, copied from `../crime_cost_2026_09_16/crime_cost.py`.
Outputs: `derived/firstgen_cost_weighted.csv` (all arms), `derived/rates_by_status_offence_{cms,pew,cms_split}.csv`, `derived/audit.json` (age factors).
Memo: `research/immigration-first-generation-crime-cost-weighted-2026-09-18.md`; ladder 144.
