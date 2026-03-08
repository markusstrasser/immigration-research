---
id: 2026-03-05-nlsy97-anomaly-diagnosis
concept: nlsy97-anomaly
repo: research
decision_date: 2026-03-05
recorded_date: 2026-03-07
provenance: backfilled
status: accepted
initial_leaning: accept sign flip as real cohort shift
relations:
  - type: depends_on
    target: 2026-03-04-battery-determines-answer
  - type: depends_on
    target: 2026-03-05-adopt-causal-dag-discipline
---

# 2026-03-05: NLSY97 quantitative female edge is a fragile artifact, not a real signal

## Context
NLSY97 showed a raw female-leaning quantitative composite, contradicting NLSY79's male-leaning pattern. This was the sharpest cross-cohort anomaly in the project and needed diagnosis before building on it.

## Alternatives considered
1. **Real cohort shift** — Accept the sign flip as evidence that the male quantitative advantage genuinely closed between NLSY79 and NLSY97 cohorts. Pro: simplest reading of raw numbers. Con: does not explain why the effect concentrates in Math Knowledge rather than Arithmetic Reasoning.
2. **Measurement/process artifact** — The CAT-ASVAB format change, process covariates, and sample-selection into the analyzable subset explain most of the sign flip. Pro: consistent with Stage A results and the broader battery-sensitivity finding. Con: requires accepting that Stage A is a robustness warning, not clean causal identification.
3. **Mixed real + artifact** — Some real narrowing plus some process/selection artifact. Pro: most nuanced. Con: hard to separate without stronger design.

## Decision
Option 2, with the caveat from the external GPT review audit that Stage A includes bad controls (descendants of the score-generating process). The `process_core` sample moves the gap from +0.037 to -0.041 — a sign reversal — but this is robustness evidence, not identified mediation. The fragile female edge is concentrated in Math Knowledge (school-knowledge-heavy), not in applied reasoning subtests.

## Evidence
- Stage A `process_core` (n=5,267): base +0.037 → adjusted -0.041, 95% CI (-0.060, -0.022)
- Signal concentrated in Math Knowledge, not Arithmetic Reasoning or PIAT Math
- Review-1 audit correctly identified bad-control problem in Stage A covariates
- CAT-vs-paper ASVAB format difference between cohorts is a known confound

Commits: `84b9691` (ASVAB data), NLSY97 stage-a pass, `a47ecf2` (review corrections)

## Revisit if
A clean sibling or twin design within NLSY97 shows a stable female quantitative advantage after excluding process/format covariates.

## Supersedes
None.
