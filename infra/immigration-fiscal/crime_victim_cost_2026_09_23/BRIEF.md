# Lane brief: victim costs of crimes committed by the group against other residents

Operator request (2026-09-23): get at the real social costs, not only the fiscal ones.

## Frame (do not change)

The [complete annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
measures the annual 2024 effect of the 40.896574m CPS Mexican-origin residents (all generations
and schooling) on all **other** US residents in a stationary absent-target comparison. Its benefit
bridge has an omitted-effects term Z; crime was left out because no estimate matched this
beneficiary set and counterfactual. This lane builds that match for victim harm.

The governing rule is the crime-harm rule in
`research/immigration-policy-causal-evidence-2026-09-20.md` (section "Crime-harm rule"):
victim-only unit costs; exclude government criminal-justice costs (already in the fiscal ledger)
and offender costs; no overlapping mortality and earnings valuations; an immigration-only
violation carries no victim-harm price. Read it and
`research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md` first.

## Task

In the absent-target comparison, offences the group commits against other residents do not
occur. Estimate, for 2024:

`victim cost = Σ_offence (incidents committed by the group) × (share with a victim outside the group) × (victim-only unit cost)`

- Incidents by offence: non-fatal violence from NCVS perceived-offender tables (reuse
  `../ncvs_victim_offender_2026_09_18/derived/`: Hispanic perceived-offender rate 13.9 per 1,000
  residents 12+, matrix and cross-group shares 2022–2024); homicide from FBI supplementary
  homicide data by offender ethnicity (reuse `comparison_with_homicide*.csv` and
  `../crime_cost_2026_09_16/` before fetching); property crime only with an explicit arrest-based
  proxy and its caveat, or bounded and left out. Exclude drug and immigration-only offences.
- Hispanic-to-Mexican-origin scaling: state it, with a sensitivity (population share versus an
  ACS institutional-rate ratio from `../acs_institutional_2026_09_16/acs5_2020_2024_origins.csv`).
- Victims outside the group: NCVS gives a non-Hispanic victim share; non-Mexican Hispanic victims
  are also "other residents", so report the non-Hispanic share as a lower bound and an estimate.
- Unit costs: McCollister, French & Fang (2010) as reconstructed in `../crime_cost_2026_09_16/`
  and the Miller et al. 2021 price set in `../ncvs_victim_offender_2026_09_18/derived/`, in 2024
  dollars. Report victim tangible costs and full costs (tangible + pain and suffering +
  statistical life) separately; report murder's share of the total.
- Report the per-person figure for the group and explain any difference from the earlier
  white-reference result (+$1,421 per US-born adult aged 25–64, `../crime_cost_2026_09_16/RESULT.md`),
  which is a relative, not an absolute, measure.

## Output

- `derived/` CSVs with every intermediate (incidents, cross-group shares, unit costs, cost by offence).
- `RESULT.md` opening with `**Verdict:**`: the annual cost to other residents, tangible and full,
  central and range, murder's share, per person; then method, sources, limits, and a
  "Covered / skipped" list with reasons.

## Rules

- Run from the repo root: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`.
- Tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`, `[INFERENCE]`, `[UNVERIFIED]`.
  Parse primary PDFs or tables for any number used in a calculation; do not use schema extraction.
- Positive controls: reproduce the 13.9 rate and the 0.404 same-group share from the NCVS lane's
  derived files, and one McCollister unit cost in 2024 dollars from the crime_cost lane.
- The Census API key lives in `infra/immigration-fiscal/acquire/config.local.env`; never print it.
- Edit nothing outside this directory. Do not commit. Return the RESULT.md path and ≤10 lines.
