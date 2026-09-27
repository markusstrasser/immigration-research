# Brief: the late-arrival (sponsored-parent) share of the main case

Operator question (2026-09-27): parents admitted late in life have not paid in; what do they cost
inside the annual account? The complete account already contains every Mexico-born resident at every
age; this lane breaks out the Mexico-born who arrived at 50 or older as their own line.

## Inputs (read-only; do not edit other lanes)

- Adopted main case: September 27 (`main_case_long_run_2026_09_27/`, decision
  `decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`; read its RESULT section
  "For consumers" first). A peer session is propagating consumers to it in
  `sept27_propagation_2026_09_27/` and may be editing `generation_account_2026_09_24/`. Read, never write,
  those directories. If the generation lane does not yet run `--case sept27`, run your split on the
  schools case (`--case sept26_schools`) and on the September 27 package directly if its package exposes
  the same shift lists; report which case each number is on.
- The subgroup split pattern: `generation_account_2026_09_24/` (masks in `frame.py`/`keys.py`, the engine
  run in `run_generations.cjs`). Copy what you need into this directory and change the mask only.
- CPS ASEC 2025 year-of-entry field (`PEINUSYR`, grouped) and age give an approximate age at arrival;
  document the grouping and bound the misclassification (arrived-at-50+ by the group's lower and upper
  edges).
- Sister lane with ACS late-arrival receipt: `late_arrival_tail_2026_09_27/derived/late_arrival_65plus.csv`.
- Senior medical pricing: ladder 173 (MCBS 65+ medical by ethnicity, 1.27) and ladder 206 (pooled MEPS
  Medicaid dollars per covered Mexican-origin person).

## Tasks

1. Subgroup: Mexico-born who arrived at 50+ (and a 55+ variant), and within it the 65+. Weighted count,
   compare the CPS count with the ACS lane's (13.6% of Mexico-born 65+).
2. Their line in the main case: net cost to other residents, $bn a year and per person, at the case's low
   and high specifications, with taxes and each benefit program shown (Medicaid, SSI, Medicare, Social
   Security, and the services shares). Same for Mexico-born who arrived younger, at the same ages, as the
   comparison.
3. Medicaid pricing check: the account prices Medicaid per covered person from a pooled figure. Price the
   late arrivals' Medicaid with the 65+ evidence (MCBS ladder 173; long-term care if the repo has an LTSS
   band — search `rg -l -i "ltss|long-term care" research/ infra/`) and report the difference as a
   proposed correction, not an edit to the case.
4. State the frame: an annual account nets this year's taxes and benefits; "didn't pay in" appears as low
   taxes and reliance on means-tested programs. The per-admission lifetime value is ladder 235 and is a
   separate object; never add the two.

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append), every computed spec in a table, files covered
  and skipped.
- Scripts here; `derived/late_arrival_line.csv` (case, spec, subgroup, program, $bn, per person),
  `derived/medicaid_check.csv`; `verify.py` that re-derives the Mexico-born total from the subgroup plus
  its complement and matches the generation lane's Mexico-born line for the same case to 1e-6.
- `.gitignore` with `_cache/`.

## Conventions

- `uv run --no-project python3 …` / `node …` from the repo root; `--with <pkg>` literally; stop on the first
  nonzero exit code; never trust an "identical" comparison after a failed run.
- The ledger loaders in `ledger_absolute_2026_09_17` verify source hashes; never edit fingerprinted files.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
