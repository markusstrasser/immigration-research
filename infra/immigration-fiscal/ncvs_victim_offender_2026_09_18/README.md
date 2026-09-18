# NCVS victim–offender ethnicity lane (2026-09-18)

Who is hurt by non-fatal violent crime, by ethnicity of victim and of perceived offender,
and what that costs — the off-murder-margin companion to
`infra/immigration-fiscal/homicide_cost_2026_09_18/`.

## Run

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
UV='uv run --no-project --with "pandas>=2" --with "numpy>=2" python3'

PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 fetch.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 build.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 analysis.py
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 age_standardise.py
```

`fetch.py` needs network and, for `age_standardise.py`, `CENSUS_API_KEY` in
`infra/immigration-fiscal/acquire/config.local.env`. Every download lands in `_cache/`
(gitignored) and is skipped on a second run. `pdftotext` (poppler) is required for the
NCJ 250747 transcription gate.

## Inputs

| Source | What it gives | Where |
|---|---|---|
| BJS *Criminal Victimization* annual data tables, 2018, 2019, 2021–2024 | victim × offender race/Hispanic origin matrix of violent incidents, with BJS's own generalized-variance standard errors; offender-side marginal; NCVS population age 12+ | `cv{18,19,21,22,23,24}.zip` |
| BJS N-DASH static data | victimisation rate and count by victim race/Hispanic origin and crime type, 1993–2024 | `ncvs.bjs.ojp.gov/data/custom-graphics/person/racehispanicorigin_all.csv` |
| BJS NCJ 250747, *Race and Hispanic Origin of Victims and Offenders, 2012-15* | the published 2012–15 matrix, the single- vs multiple-offender split, rates by crime type, reported-to-police and injury shares by pair | `rhovo1215.pdf` |
| McCollister, French & Fang (2010) | unit costs per offence, 2008 dollars, inflated with BLS CPI-U | inline in `analysis.py` |
| ACS 2023 1-year B01001H/B/I | population by group and age, for the age arm | Census API |
| ICPSR 38963 (NCVS concatenated microdata) | **not obtained** — every download path redirects to `rpxlogin` | `derived/icpsr_route_probe.csv` |

## Outputs (`derived/`)

| File | Contents |
|---|---|
| `source_manifest.csv` | every cached file with its byte count and sha256 |
| `icpsr_route_probe.csv` | the HTTP status and redirect target of each ICPSR download path |
| `cv_matrix_violent.csv` | victim × offender cells and SEs, all violent incidents, by year |
| `cv_matrix_violent_excl_simple.csv` | the same for serious violent (2018, 2019) |
| `cv_offender_marginal.csv` | population, victim incidents and offender incidents by group and year |
| `cv_population_12plus.csv` | NCVS population age 12+ by group, 2014–2024 |
| `ndash_rate_by_victim_race.csv` | rate, count, SE and unweighted n by victim race and crime type, 1993–2024 |
| `matrix_pooled_2022_2024.csv` | the headline pooled matrix with row shares (unknown kept and dropped) and column shares |
| `matrix_pooled_2021_2024_three_victim_rows.csv` | the longer window, three victim rows |
| `matrix_by_crime_type_2019.csv` | violent, serious violent and simple assault matrices, 2019 |
| `single_vs_multiple_offender_2012_2015.csv` | offender ethnicity by number of offenders |
| `rates_by_victim_and_offender_2022_2024.csv` | incidents per 1,000 residents, both sides |
| `cross_group_shares_2022_2024.csv`, `intra_group_concentration_2022_2024.csv` | (d) |
| `offence_mix_by_victim_group.csv`, `cost_of_victimisation_by_group.csv`, `inter_group_cost_transfer.csv` | (e) |
| `disconfirmation_arms.csv` | every arm's intra-group share |
| `comparison_with_homicide.csv` | against the cleared-homicide matrix |
| `age_structure_by_group_acs2023.csv`, `age_expected_offender_rate*.csv`, `age_arm_observed_vs_expected.csv` | the age arm |
| `analysis_log.txt` | the full console transcript of `analysis.py`, gates included |
| `rhovo_t{1,2,3,6,8}_*.csv` | NCJ 250747 tables, transcribed and gated against the PDF text |

## Reproducibility

Re-running the four scripts leaves `derived/` byte-identical, both warm (cache kept) and
cold (cache deleted, everything re-fetched). Verified 2026-09-18; see `RESULT.md`.
