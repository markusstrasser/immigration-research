# Brief — which lanes does the ACS 2019/2020 no-schooling step reach, and by how much?

Lane directory (you own it): `infra/immigration-fiscal/acs_schooling_break_2026_09_26/`. Written
2026-09-26 by the parent session. Peer sessions share this checkout. Do not edit files outside your
directory and do not commit; the parent integrates.

## The defect

Adults reporting "no schooling completed" (ACS `SCHL` 1; IPUMS `EDUCD` 2) step up between the 2019
and 2020 ACS and stay at the new level, while "grade 8 or less, including none" stays continuous.
Aged 20–64, 2019 → 2021 [DATA: parent's check on the Census PUMS files]:

| Group | None 2019 | None 2021 | Grade 8 or less 2019 | 2021 |
|---|---:|---:|---:|---:|
| Mexico-born | 5.55% | 8.66% | 29.22% | 29.00% |
| Other Latin America-born (Hispanic) | 4.05% | 6.30% | 17.17% | 17.99% |
| Non-Hispanic foreign-born | 2.67% | 3.45% | 4.91% | 5.26% |
| US-born | 0.67% | 0.92% | 1.68% | 1.80% |
| US-born Hispanic | 1.27% | 1.81% | 3.73% | 3.84% |

So reports move from grades 1–8 to "none". The source is
`return_vs_us_stayers_2026_09_26/RESULT.md` ("A 2020 step in ACS no-schooling reports") and its
`derived/acs_no_schooling_break.csv`. That lane's spec (e) re-scores the excess no-schooling share at
the grades-1–9 mean and moved its 2023 men's mean-years gap from −0.75 to −1.00 years. The cause
is not identified. Search Census ACS user notes, errata and the 2020–2021 questionnaire or
edit-change documentation once, and record what you find, including if you find nothing.

## Task

1. **Triage every lane** under `infra/immigration-fiscal/` that reads ACS or IPUMS USA schooling
   (`SCHL`, `EDUC`, `EDUCD`) in any survey year 2020–2024. Candidates from a grep: `arrival_cohorts_2026_09_18`,
   `schooling_selection_position_2026_09_23`, `high_skill_origin_screen_2026_09_21`, `admission_route_2026_09_21`,
   `crime_selection_cohorts_2026_09_23`, `labor_mobility_insurance_2026_09_23`, `compliance_gap_2026_09_24`,
   `service_by_ses_2026_09_23`, `dataset_integrity_2026_09_23`, `indian_generation_2026_09_21`, `indian_ledger_2026_09_18`,
   `housing_supply_ca_tx_2026_09_22`, `school_dilution_2026_09_24`, `school_cost_where_enrolled_2026_09_24`, `movers_reasons_2026_09_24`,
   `ledger_absolute_2026_09_17`, `external_benchmarks_2026_09_24`, `unauthorized_population_size_2026_09_19`,
   `employment_entry_2026_09_18`, `displacement_transfers_2026_09_18`, `tiebout_sorting_2026_09_18`, `build/`. Confirm or clear
   each one by reading its code. A lane is **exposed** only if its output depends on the split between no schooling
   and grades 1–8. That happens when it:
   - scores years of schooling;
   - uses a band boundary below grade 9;
   - ranks people within an origin distribution; or
   - compares survey years across 2019/2020, or pools across that boundary so that composition by year matters.

   Coarse bands such as "less than high school" (`SCHL` ≤ 15) or "grade 8 or less" are **not** exposed. Say which
   reason clears each lane.
2. **Size the exposed ones.** For each exposed lane, recompute its headline numbers with a break correction:
   re-score, or re-band, the excess no-schooling share in 2020+ survey years as the grades 1–8 distribution of the
   same group in 2019. Use the return-migration lane's spec (e) method, or a better one that you justify. Where a
   rerun is cheap, run the lane's own code on a copy in your directory. Never edit the lane itself. Otherwise compute
   the effect analytically from the lane's derived tables and say so. Report each headline's old value, its corrected
   value and whether any sign or conclusion changes. Look first at `schooling_selection_position_2026_09_23`: its
   verdict says the 2015–19 and 2020–23 arrival cohorts "have more at both ends", which the step could produce at the
   bottom. Then look at `arrival_cohorts_2026_09_18`, whose mean-years trend crosses the boundary.
3. **Write** `RESULT.md` opening with `**Verdict:**` and a table with one row per lane: exposed or not, the reason,
   the headline affected, old value, corrected value, and whether the conclusion changes. Add a
   `Model self-report:` line. Tag each number `[DATA]`, `[CALCULATION]` or `[SOURCE]`. Put any scripts and outputs
   in your directory, with CSVs written using `lineterminator="\n"`.

## Rules

- Run from the repository root with `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 …`. Read exit codes; rerun
  any script you keep and check that its outputs are byte-identical.
- Local data: the ACS person zips are in `sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_<year>.zip`
  (2005–2018, 2021, 2022), `acs_pums_2019_1yr/csv_pus.zip`, `acs_pums_2024_1yr/csv_pus.zip`, and
  `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`. The IPUMS store is described in
  `research/immigration-dataset-register.md`, card `IPUMS_USA_EXTRACTS_2026_09_23`.
- Hard gates raise; no silent fallback; label inference `[INFERENCE]`.
- Your final message is the RESULT.md path plus at most 10 lines: the exposed lanes, the size of each effect, any
  conclusion that changes, and what you did not check.
