---
id: 2026-03-06-stop-public-regressions-pursue-identification
concept: research-strategy
repo: research
decision_date: 2026-03-06
recorded_date: 2026-03-07
provenance: backfilled
status: accepted
initial_leaning: continue public-use dataset expansion
relations:
  - type: depends_on
    target: 2026-03-05-adopt-causal-dag-discipline
---

# 2026-03-06: Stop treating more public-use regressions as the default next step

## Context
After running passes on NLSY79, NLSY97, PIAAC, TIMSS, PISA 2018, ECLS-K (both cohorts), NLSCYA, HSLS, ELS, and NELS, the project reached diminishing returns from public-use coefficient reshuffling. The surface families were stable: female-leaning school evaluation/GPA, male-leaning applied math and adult numeracy, and Math Knowledge as the localized late-school female anomaly.

## Alternatives considered
1. **Continue public-use expansion** — Acquire and analyze more public datasets (PSID CDS, FFCWS, Add Health public). Pro: cheap, immediate. Con: each new cohort mostly reshuffles the same surface families without separating mechanism.
2. **Pivot to restricted data** — Apply for Add Health restricted + AHAA transcripts, HSTS microdata, NAEP process data. Pro: cleanest transcript/test linkages, school-based designs, sibling samples. Con: months-long application process, institutional membership barriers.
3. **Pivot to experimental design** — Design and run an original matrix/Raven experiment using open stimulus banks (OMIB). Pro: direct randomization of item-family content. Con: requires recruitment, IRB-equivalent considerations.
4. **Combined: restricted data + experiment + targeted public passes** — Pursue restricted data applications now, design the matrix experiment, and run only targeted public passes that address specific causal nodes. Pro: attacks the identification ceiling from multiple angles. Con: highest complexity.

## Decision
Option 4, with explicit prioritization. The next-level research plan freezes four criteria for what counts as a "real upgrade": (1) separates measurement surface from latent domain, (2) separates school evaluation from transcript/track/tested math, (3) identifies mechanism under treatment-dependent-confounding discipline, (4) directly randomizes a candidate channel. Results that don't meet at least one criterion are descriptive extensions. P(identification ceiling is the bottleneck) = 0.72.

Immediate actions: Apply for Add Health restricted + AHAA; finalize matrix experiment protocol using OMIB stimuli; run remaining public passes only on early-school and transition surfaces (PSID CDS/TAS, FFCWS) that address specific DAG nodes.

## Evidence
- 12+ datasets analyzed with stable surface-family pattern
- School-wedge synthesis: GPA mean beta = +0.256, tested_math = -0.053 — pattern replicates across cohorts
- PISA 2018 family ordering survives 7 different robustness passes (leave-out, purified, iterative, logit, Rasch, theta-DIF, time-DIF)
- Dataset roadmap and mediator-design memo formalize the identification gap

Commits: `bbca3e9` (dataset roadmap), next-level-research-plan, execution-plan, mediator-design, master-plan

## Revisit if
A new public-use dataset with materially different instrumentation creates a qualitatively new surface family that the current pattern cannot accommodate.

## Supersedes
None (implicit assumption of "more data = more insight" was never formally recorded).
