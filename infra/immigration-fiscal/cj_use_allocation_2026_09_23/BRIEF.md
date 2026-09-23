# Lane brief: charge public order and safety by use, add attributable interior enforcement

Operator question (2026-09-23): the complete account charges police, courts and prisons as an
equal amount per resident. Should it be weighted by use? Compute the use-weighted charge.

## Frame (do not change)

The [complete annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
measures the annual 2024 effect of the 40.896574m CPS Mexican-origin residents (all generations
and schooling) on all other US residents, in a stationary absent-target comparison.
`../full_account_spending_2026_09_20/derived/allocations.csv` charges `public_order_safety`
(BEA NIPA Table 3.17 line 4, $519.153bn, all levels of government) by population: target share
0.121453, **$62.425bn** (alternative key `adults`: 0.109092, $56.072bn). In the main
CBO-informed case safety responds proportionally, so any change in this charge passes 1:1
into the $165–197bn band.

## Task

1. Split line 4 into BEA's sublines (police, fire, law courts, prisons, other) from
   `sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, table `T31700-A`.
   Gate: sublines sum to line 4.
2. Allocate each subline with a use key and keep the per-head key as the reference:
   - fire: per head (or housing units), unchanged;
   - prisons/corrections: share of people in correctional custody. Proxy with ACS institutional
     group-quarters residence at ages 18–64 by origin and nativity (reuse
     `../acs_institutional_2026_09_16/`, including `acs5_2020_2024_origins.csv`). Cross-check against
     BJS prisoners by Hispanic origin scaled to Mexican origin. Follow the reporting rule in
     `research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md`: ACS cannot separate
     correctional, noncorrectional and ICE custody; say so at the number and bound the effect;
   - law courts: criminal part by arrests or cases, civil part per head; the criminal share of
     court spending is a stated range if no source pins it;
   - police: report three keys: offending (arrest share), half offending and half per head
     (patrol protects everyone), and victimization share (who is protected).
   Hispanic-to-Mexican-origin scaling must be explicit (for example the ACS Mexican versus
   all-Hispanic institutional ratio at 18–64). Reuse `../crime_cost_2026_09_16/` (FBI arrests by
   ethnicity route) and `../ncvs_victim_offender_2026_09_18/derived/` (perceived-offender and
   victimization rates) before fetching anything.
3. Interior immigration custody and removal: FY2024 identified ICE custody outlays $2.917bn
   (`../detention_evidence_2026_09_20/ACTUAL_SPENDING_FY2024.md`). Allocate by Mexico's share of
   ICE book-ins, detained population or removals if an official FY2024 table is held or
   obtainable; otherwise report the share needed and leave it unallocated. Do not charge CBP
   border spending to the resident stock; state why in one sentence.
4. Where the keys allow, split Mexico-born from US-born.

## Output

- `derived/cj_allocation.csv`: subline × key → target $bn, other $bn, target share.
- `RESULT.md` opening with `**Verdict:**`: the change from the per-head $62.425bn under each key
  set, a central choice with reasons, the range, and the effect on the $165–197bn band. Then
  method, sources, limits, and a "Covered / skipped" list with reasons.
- Scripts in this directory; outputs in `derived/`; raw pulls in ignored `_cache/`.

## Rules

- Run from the repo root: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`.
- Tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`, `[INFERENCE]`, `[UNVERIFIED]`.
- The Census API key lives in `infra/immigration-fiscal/acquire/config.local.env`; never print it;
  pipe API output through a redaction filter.
- Positive control: reproduce $62.425bn and the 0.121453 share from `allocations.csv`.
- Edit nothing outside this directory. Do not commit. Return the RESULT.md path and ≤10 lines.
