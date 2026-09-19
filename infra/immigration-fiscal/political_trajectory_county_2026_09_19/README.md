# Lane: Mexican-origin composition and county political trajectory, 2000-2024

[DATA] measured county returns, Census API tables and CPS microdata ·
[SOURCE] MIT/MEDSL, tonmcg, Census API, Roper Center, Pew Research, MSU IPPSR ·
[INFERENCE] the regressions, decompositions and verdicts in `RESULT.md`

Answers the operator's question in `BRIEF.md`: over 2000-2024, did growth in a
county's Mexican-origin share change its political trajectory, and does the
California-Texas contrast show composition driving outcomes?

## Run

```bash
cd infra/immigration-fiscal/political_trajectory_county_2026_09_19
set -a; . ../acquire/config.local.env; set +a        # CENSUS_API_KEY
U='uv run --no-project --with pandas>=2 --with numpy>=2 --with requests --with pyarrow python3'
PYTHONUNBUFFERED=1 $U scripts/01_fetch_county_returns.py
PYTHONUNBUFFERED=1 $U scripts/02_fetch_census_county.py
PYTHONUNBUFFERED=1 $U scripts/03_build_panel.py
PYTHONUNBUFFERED=1 $U scripts/04_regressions.py
PYTHONUNBUFFERED=1 $U scripts/05_fetch_cps_voting.py
PYTHONUNBUFFERED=1 $U scripts/06_composition_vs_conversion.py
PYTHONUNBUFFERED=1 $U scripts/07_ca_tx_contrast.py
PYTHONUNBUFFERED=1 $U scripts/08_state_laws.py
```

Scripts 01, 02, 05 and 08 cache their downloads under `_cache/` (gitignored
repo-wide) and skip the network on a re-run. 03 depends on 01 and 02; 04, 07 and
08 depend on 03; 06 and 07 depend on 05. `scripts/fe.py` is the fixed-effect
absorption and cluster-robust WLS/2SLS module, with no external estimation
dependency.

## Inputs

| Source | What | Route |
|---|---|---|
| MEDSL `county-returns` (GitHub) | county presidential returns 2000-2016 | raw.githubusercontent.com |
| tonmcg `US_County_Level_Election_Results_08-24` | county returns 2020, 2024 | raw.githubusercontent.com |
| Census API `dec/sf1` 2000, 2010 | P001001, Hispanic total, PCT011004 Mexican origin | keyed API |
| Census API `acs/acs5` 2009, 2014, 2018, 2022, 2023 | B03001, B03002, B05003, B05003I, B19013 | keyed API |
| Census API `cps/voting/nov` 2004-2024 | November Voting and Registration Supplement | keyed API |
| Roper Center "How Groups Voted" 2000-2024 | national exit-poll vote by race | fetched pages |
| Pew Research validated-voter reports 2021, 2025 | Hispanic vote, higher-graded series | fetched pages |
| MSU IPPSR Correlates of State Policy v2.2 | state immigration-law variables | public CSV |

The MIT county file on Harvard Dataverse (doi:10.7910/DVN/VOQCHQ) **refuses
scripted download**: HTTP 400, "You may not download this file without the
required Guestbook response for guestbookID 458", with and without `gbrecs=true`.
The lane therefore uses MEDSL's own GitHub mirror for 2000-2016 and the tonmcg
mirror named in the brief for 2020 and 2024. Script 01 measures the splice error
on 2016, which both sources carry.

## Outputs (`derived/`)

| File | Contents |
|---|---|
| `county_panel.csv` | balanced panel, 3,103 counties x 7 elections (3.0 MB) |
| `panel_build_log.txt` | row counts, dropped geographies, panel-wide series |
| `regressions.csv` / `.txt` | S1-S10, T1-T2 with cluster-robust SEs |
| `rgv_swing.csv` | Rio Grande Valley and South Texas counties, by name |
| `cps_voting_national.csv` / `_state.csv` | CPS turnout and voter shares by group |
| `partisanship_series.csv` | exit-poll and Pew Hispanic vote series |
| `decomposition.csv` / `.txt` | composition vs conversion |
| `ca_tx_series.csv`, `ca_tx_gap_decomposition.csv`, `ca_tx.txt` | arm 3 |
| `state_law_table.csv`, `state_laws.txt` | arm 4 |

## Geography and source decisions, all stated

- Alaska dropped: returns are by state house district in both vote sources.
- Connecticut dropped: ACS 5-year 2022 and 2023 report the nine planning regions
  while the returns still use the eight old counties.
- 46102 Oglala Lakota mapped to 46113 Shannon; 51515 Bedford city summed into
  51019 Bedford County in every year and every source.
- The panel is balanced on counties observed in all seven years.
- Each ACS 5-year release is matched to the election year at its window midpoint;
  2004 is interpolated between the two decennials. 2024 uses the 2019-2023
  release, whose midpoint is 2021 - a real lag, reported as a limit.
