---
id: 2026-03-05-ach-for-early-school-conflict
concept: methodology
repo: research
decision_date: 2026-03-05
recorded_date: 2026-03-07
provenance: backfilled
status: accepted
initial_leaning: average across datasets
relations:
  - type: depends_on
    target: 2026-03-04-battery-determines-answer
---

# 2026-03-05: Use Analysis of Competing Hypotheses for the early-school dataset conflict

## Context
NLSCYA PIAT Math showed female-leaning early-childhood scores while both ECLS-K cohorts showed male-leaning broad school-entry math. This three-dataset conflict needed resolution before the project could treat any early-school result as a reliable anchor.

## Alternatives considered
1. **Average across datasets** — Pool or meta-analyze the three surfaces. Pro: simple. Con: destroys the structured disagreement, which is informative about measurement vs sampling vs cohort effects.
2. **Pick the largest sample** — Treat ECLS-K:2011 as ground truth. Pro: largest, most recent. Con: ignores that PIAT Math measures a different construct than ECLS IRT math.
3. **ACH framework** — Enumerate competing hypotheses (measurement mismatch, sample composition, real cohort shift, data artifact), assign priors, derive predicted data footprints, and update posteriors from evidence. Pro: structured, auditable, forces explicit probability assignments. Con: more work, subjective priors.

## Decision
Option 3. The ACH analysis assigned highest posterior to H1 (measurement/score-family mismatch, prior 0.40) because: the two independent ECLS cohorts align directionally while NLSCYA uses a different instrument (PIAT Math) at different ages, and the project's broader evidence already gives measurement mismatch a high base rate across NLSY97, TIMSS, PISA, and PIAAC.

Resolution: the conflict is primarily a construct mismatch, not a contradiction. PIAT Math and ECLS broad school-entry IRT measure different child math surfaces, and different surfaces produce different sex-gap geometry. This is consistent with the battery-determines-answer framing.

## Evidence
- Two ECLS cohorts align directionally on both math and reading
- NLSCYA diverges specifically on math (not reading), pointing to instrument rather than sample
- Broader project evidence: 4 other dataset families showed surface-sensitive sex-gap geometry
- ACH likelihood matrix with 4 hypotheses x multiple evidence rows

Commits: early-school-ach memo (part of 2026-03-05 batch), early-school intake/alignment files

## Revisit if
A dataset with both PIAT Math and an ECLS-style IRT math measure administered to the same children shows the gap is not primarily instrument-driven.

## Supersedes
None.
