# Brief: the late-arrival tail — Mexico-born who arrive at 50+ (sponsored parents)

Operator question (2026-09-27): a citizen can sponsor a parent, who arrives in late middle age
with little US work history and later draws old-age programs. How large is that stream for
Mexico, what do late arrivals draw, and what does it add to the per-admission and lineage cost?
Part of the first report on low-skill Mexican migration.

## What already exists

- Complete annual account includes all Mexico-born residents at every age, so late arrivals
  are already in the annual totals; the question here is their per-person profile and the
  per-admission lifetime value, which the lineage model does not price (it starts the founder
  at 25): `infra/immigration-fiscal/lineage_cost_2026_09_19/`, memo
  `research/immigration-lineage-cost-century-2026-09-19.md`.
- Senior-program rules by legal status (statutory bars; the 2026-09-26 priced senior rule):
  see `research/immigration-INDEX.md` entries for 2026-09-26 and `ledger_absolute_2026_09_17`.
- Status imputation: `infra/immigration-fiscal/status_impute_2026_09_16/`.

## Tasks

1. **Flow.** DHS Yearbook of Immigration Statistics, LPRs by class of admission and country:
   immediate relatives — parents of US citizens (IR-5) from Mexico, FY2005–FY2023 (or latest),
   and age at admission (Yearbook table of LPRs by age, and any country × age table). Compare
   with India, China, Philippines. Read the tables from the files; cite table numbers.
2. **Stock and receipt.** ACS 2019–2023 (Census API microdata; key via
   `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`, never print it,
   pipe errors through a redaction filter): Mexico-born persons by age at arrival
   (AGEP − (survey year − YOEP)), 50+ vs under 50. For ages 65+: Medicaid (HINS4), Medicare
   (HINS3), SSI (SSIP), Social Security (SSP), citizenship, poverty, living with an adult child.
   Same for India-born and for US-born NH whites 65+. Replicate-weight SEs.
3. **Per-admission value.** Using the ledger's age profiles (read `ledger_absolute_2026_09_17`
   loaders; they verify source hashes — do not edit fingerprinted files) or the lineage model's
   parameterisation, compute the remaining-lifetime net fiscal value of a Mexico-born arrival at
   55, 60 and 65, legal permanent resident, under the statutory five-year bar and sponsor
   deeming rules, against a same-age white resident's remaining lifetime. State which rules
   are applied and which assumed. Add the result as arms, not as an edit to the lineage lane.
4. **Scale.** Multiply per-admission values by the annual IR-5 flow to give a $/year-of-
   admissions figure; state that it is a flow valuation, not an annual-account line (the
   annual account already contains these people).
5. **Disconfirmation.** Evidence that sponsored parents provide offsetting value (childcare
   letting a daughter work: find a measured labor-supply effect of co-resident grandparents
   among immigrants, e.g. Compton–Pollak-type or immigrant-specific estimates) and report it
   with page citations.

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append as you go), files covered/skipped.
- Scripts here; `derived/ir5_flow.csv`, `derived/late_arrival_65plus.csv`,
  `derived/per_admission.csv`; `verify.py` for the gates; `.gitignore` with `_cache/`.

## Gates

- ACS weighted Mexico-born total for each year within 1% of the published B05006 figure.
- Yearbook IR-5 totals equal the published all-country total for each year.
- If you use the ledger loaders, they run without `[BLOCKED]`.

## Conventions

- `uv run --no-project python3 …` from the repo root; `--with <pkg>` literally if needed.
- Fetch via `subprocess.run(["curl","-sS","--fail",...])`; validate content, not status.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
