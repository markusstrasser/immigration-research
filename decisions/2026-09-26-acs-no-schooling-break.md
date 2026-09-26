---
date: 2026-09-26
concepts: [acs-schooling-measurement, arrival-cohort-selection, schooling-position, return-migration-selection, supply-shock-panel]
status: adopted
supersedes: []
relations:
  - refines: infra/immigration-fiscal/dataset_integrity_2026_09_23/acs.md
  - applies: infra/immigration-fiscal/acs_schooling_break_2026_09_26/RESULT.md
evidence: infra/immigration-fiscal/acs_schooling_break_2026_09_26/RESULT.md
---

# 2026-09-26: Qualify ACS 2020+ schooling measures for the no-schooling step, and score no schooling at zero

## Context

The returnee-versus-stayer lane (ladder 228) noticed a step in ACS reports of "no schooling
completed" between the 2019 and 2020 files. The dataset integrity audit had already reported it
on 2026-09-23 as F6, but that finding was not in the dataset register, and the returnee lane and
the parent session missed it. A triage lane (`acs_schooling_break_2026_09_26`) then checked every lane that
reads ACS or IPUMS USA schooling for 2020–2024.

The step is a reporting change, not a population change: a fixed population whose schooling
cannot change shows it too. Reports move to "none" from grades 1–8 and from grade 9. For the
Mexico-born aged 20–64 it adds about 3 points, and it touches every group, natives included. The
Census Bureau documents over-reporting of "No schooling completed" in mail and internet responses
and changed the question for the 2025 ACS, which will be a second break. Two of the exposed
scripts also dropped no-schooling records in every year, which is a separate defect.

## Alternatives considered

1. **Rebuild every exposed lane with a break correction.** This would carry one correction
   through every output. But the correction normalizes to the 2019 instrument, not to the truth:
   reports also drift about 0.4 points a year outside the step. Building it into lanes would hide
   that choice.
2. **Qualify each exposed headline with its corrected value and fix only real defects.** Chosen.
   The corrected values stay visible beside the published ones, and the two correction methods
   bracket the effect.
3. **Ignore it, as F6 did for coarse bands.** This is right for "less than high school"
   and wider bands, which move 0.4 points at most. It is wrong for any measure that scores years,
   ranks within an origin distribution or cuts below grade 9.

## Decision

- **Qualify, don't rebuild.** Each exposed headline carries a dated bracket with its corrected
  value. The lanes are schooling position (ladder 197), arrival cohorts (133), scale spillovers
  (201), returnees against stayers (228) and the Borjas panel memo. The flow-rate method (B) is
  preferred, and the brief's level method (A) gives the other end.
- **Score no schooling at zero wherever years are scored.** `arrival_cohorts_2026_09_18/origin_relative.py`
  now maps `EDUC` 0 to 0 years, as INEGI's grado promedio does, and was rerun. The 2000→2023 gain
  becomes 2.53 years (2.67–2.69 without the step), which is 0.03–0.49 above Mexico's. "The slopes
  are the same" is weakened to "within half a year". The reading that the rise is mostly Mexico's
  schooling expansion stands.
- **Defer the Borjas builder fix.** `build/build_borjas_supply_shock_panel.py` drops `EDUC` 0 in
  every year, so its < HS immigrant share reads 40.8% in 2023 instead of 44.1%. It writes the
  context warehouse table that feeds the downloadable release. A rebuild changes a shared,
  released artifact, and no analysis lane reads the table, so the memo, INDEX and guide carry the
  corrected figures until a deliberate release rebuild.
- **Register the step where readers look.** The dataset register's ACS 2024 and IPUMS USA cards
  describe it and cite F6 and the triage lane. Any lane that adds 2025 ACS data must handle the
  second break.

## Evidence

- `acs_schooling_break_2026_09_26/RESULT.md`. Every fix script first reproduces its lane's
  published numbers. All five scripts rerun byte-identical, confirmed by the parent's rerun.
- The parent reproduced the step from the Census PUMS files for 2017–2019 and 2021–2024, across
  five nativity groups.
- `dataset_integrity_2026_09_23/acs.md` F6 (2026-09-23), which these findings refine.

## Revisit if

- Census publishes a note on the 2020 change, or a mode variable becomes available.
- A lane reads the 2025 ACS.
- The context warehouse is rebuilt for a release: fix the builder's `EDUC` filter then.

## Supersedes

None. It refines F6's "none on any category at or above the high-school line" and "natives 65+
stay at 0.8–0.9%" as stated in that file's bracket.
