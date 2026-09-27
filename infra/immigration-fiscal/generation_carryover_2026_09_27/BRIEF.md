# Brief: does the Mexican-origin gap fade, stall or persist across generations? (G1 → G4+)

Operator question (2026-09-27): for Indians the fiscal premium roughly halves G2 → G3. For
Mexican origin, how much of the gap against third-plus non-Hispanic whites carries over from
one generation to the next, does G4+ improve on G3, and what does that imply for G4/G5?
Part of the first report on low-skill Mexican migration.

## What already exists (reuse, do not rebuild)

- Adopted account by generation (G1 / G2 / G3+, $ per adult, all three net costs):
  `infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results.csv`,
  memo `research/immigration-adopted-account-by-generation-2026-09-25.md`.
- Observed G3 vs G4+ split via co-resident parents' parental-birthplace reports, CPS ASEC 2025:
  `infra/immigration-fiscal/generation_split_2026_09_20/` (`analyze_cps.py` has the classifier;
  `analyze_gss.py` the GSS GRANBORN classifier). Memos
  `research/immigration-fourth-generation-scope-2026-09-20.md`,
  `research/immigration-later-generation-estimates-2026-09-20.md`.
- MASP (Telles–Ortiz) family follow-up with generation reconstruction:
  `infra/immigration-fiscal/masp_2026_09_20/` (`analyze.py`, RESULT.md).
- Pew identifier/nonidentifier schooling: `infra/immigration-fiscal/pew_outcomes_2026_09_20/`.
- Ethnic attrition in the lineage count (ladder 158, 11%):
  `research/immigration-mexican-origin-population-total-2026-09-19.md`.
- Stopping decision on ancestry-outcome data: `decisions/2026-09-20-ancestry-outcome-data-ceiling.md`
  (PSID excluded by its terms; do not re-open).
- Partial-ledger G2 and G3+ gaps: `research/immigration-mexican-origin-by-generation-2026-09-16.md`.

## Tasks

1. **Outcome gaps by generation, one table.** For Mexican-origin G1, G2, G3 (observed), G4+
   (observed) and unresolved G3+, against third-plus NH whites at matched ages: BA+, less than
   HS, employment, earnings (worker mean/median), and the partial own-tax-minus-cash measure
   where the ledger code supports it. Sources, each reported separately, never pooled across
   instruments:
   - CPS ASEC 2022–2025 pooled with the existing classifier (each year's grandparent linkage;
     check the ASEC years' variable availability first). Observed G3/G4+ adults are young and
     co-resident: report ages, n, and compare to same-age co-resident whites so the selection
     is symmetric.
   - GSS all available years, GRANBORN among Mexican-identifying respondents: education,
     degree, respondent income (REALRINC), occupational prestige. Age-adjust to a common age
     mix. Note GRANBORN counts foreign-born grandparents of any country.
   - MASP G3 vs G4 (adult children; the lane already reconstructs generation).
   - NLSY97 published results: Duncan, Grogger, Leon, Trejo, IZA DP12704
     (https://docs.iza.org/dp12704.pdf). Quote table numbers only after reading the PDF;
     record table and page.
2. **Carry-over ratios.** For each measure and source, ρ(n→n+1) = gap(G n+1) / gap(G n), with
   an SE or interval (replicates / delta method / bootstrap). Include the adopted account's
   $-per-adult G1→G2 and G2→G3+ ratios. State plainly whether G4+ improves on G3.
3. **Identity attrition.** Bound how much selective loss of Mexican identification could move
   the G3/G4+ gaps, using existing evidence (ladder 158 attrition rate, Pew nonidentifier BA,
   MASP nonidentifiers, Duncan–Trejo). Give the gap under "attriters look like identifiers",
   "attriters look like whites" and the measured nonidentifier values.
4. **Projection to G4/G5**, clearly labelled [MODEL]: apply the measured ρ range to the G3+
   gap, with the attrition bounds. Say which inputs are measured and which assumed.
5. **Disconfirmation:** search for evidence that the stall is an artifact (age, cohort,
   region — Texas/California, the 1848/1920s-origin G4+ in New Mexico/Colorado, "Hispano"
   populations) and report what survives.

## Outputs

- `RESULT.md` opening `**Verdict:**` (written first as a stub, appended as you go): the table,
  the ρ table, attrition bounds, projection, disconfirmation, files covered and skipped.
- Scripts in this directory; `derived/` CSVs (`gaps_by_generation.csv`, `carryover.csv`,
  `attrition_bounds.csv`, `projection.csv`) with an explicit `source`, `measure`, `generation`,
  `n`, `se` column set. Tests or a `verify.py` that checks the gates below.
- `.gitignore` with `_cache/`.

## Gates

- The CPS 2025 G3/G4+ weighted counts reproduce `generation_split_2026_09_20/derived/cps_generation_split.csv`
  (2.870m / 2.073m all ages) before any new year is added.
- The adopted account ratios are computed from the CSV, not retyped.
- Every published-paper number carries table/page and was read in the source file.

## Conventions

- Run with `uv run --no-project python3 …` from the repo root (main checkout venv). If a
  package is missing add `--with <pkg>` literally.
- Fetch with `subprocess.run(["curl","-sS","--fail",...])`, validate content (row counts), not
  status. Census key: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`;
  never print it, never dump `ps`/`pgrep`.
- `csv.writer(..., lineterminator="\n")`.
- Source tags per `CLAUDE.md` (`[SOURCE]`, `[DATA]`, `[CALCULATION]`, `[MODEL]`, `[INFERENCE]`).
- Do not commit; do not edit files outside this directory. The parent integrates.
- Return: path of RESULT.md and ≤10 lines.
