# Lane brief: housing cost effects on other residents, as transfers

Operator request (2026-09-23): get at the real social costs. Housing was left out of the
complete account because price effects move money between residents rather than using it up.
Measure who pays and who gains.

## Frame (do not change)

The [complete annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
measures the annual 2024 effect of the 40.896574m CPS Mexican-origin residents (all generations
and schooling) on all **other** US residents in a stationary absent-target comparison, with
private capital adjusting in its primary long-run case. Higher rents are a loss to renters and a
gain to landlords; among other residents those largely cancel. The net for other residents is
the extra rent the group itself pays to landlords who are other residents, and owners gain on
home values. The distribution (renters versus owners) is the social-cost question.

## Task

1. From ACS 2024 one-year PUMS (household `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_hus.zip`,
   person `csv_pus.zip`; weights `WGTP`/`PWGTP`), tabulate for Mexican-origin households
   (define the rule, for example householder `HISP=02`, and report the alternative "any member")
   and all other households: tenure, aggregate gross rent (`GRNTP`), aggregate home value
   (`VALP`), counts. Gate: aggregate gross rent within a few percent of the published ACS 2024
   aggregate (table B25065 or the PUMS total).
2. Rent and price effect of the group's presence: use the repo's own estimates first:
   ladder 183 (`../housing_causal_2000_2010_2026_09_22/RESULT.md`: rents +1.4% per point of
   foreign-born share, SE 1.4; values +11.6%, +5.7% with the 2000 level), ladder 180
   (`research/immigration-housing-supply-ca-tx-2026-09-22.md`), and Wilson & Zhou 2026 as cited
   in `research/immigration-confidence-ladder.md` entry 50 (housing first stage F ≈ 14). Build a
   short-run arm (no supply response) and a long-run arm (supply adjusts; rent effect limited to
   land), with the elasticity per point of population share as an explicit, ranged input. Do not
   extrapolate a per-point estimate linearly to a 12-point share without saying so and showing
   the sensitivity.
3. Compute, per arm: other residents' renters' extra rent; landlords' gain split into rent paid by
   other residents (a transfer inside the beneficiary set) and rent paid by the group (a net gain
   to other residents), with an explicit range for the share of rental units owned by other
   residents versus the group, institutions and foreign owners; owners' home-value gain as a
   stock, not added to the annual flow; per native renter household.
4. State the overlap with the complete account: its production term covers labour and business
   capital; say whether residential rents are inside it (read
   `../full_account_benefits_2026_09_20/README.md`) and so whether the net figure can be added.

## Output

- `derived/` CSVs with the tabulations and every arm.
- `RESULT.md` opening with `**Verdict:**`: renters' loss, owners' and landlords' gain, net for
  other residents, per arm, with ranges; the overlap ruling; then method, sources, limits, and a
  "Covered / skipped" list with reasons.

## Rules

- Run from the repo root: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`.
  Read the ZIPs in chunks with only the needed columns.
- Tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`, `[INFERENCE]`, `[UNVERIFIED]`.
- Edit nothing outside this directory. Do not commit. Return the RESULT.md path and ≤10 lines.
