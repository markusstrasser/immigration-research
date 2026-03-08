---
id: 2026-03-06-timss-item-wall-and-irt-ceiling
concept: measurement-tools
repo: research
decision_date: 2026-03-06
recorded_date: 2026-03-07
provenance: backfilled
status: accepted
initial_leaning: push through TIMSS item wall via IEA access
relations: []
---

# 2026-03-06: TIMSS item-level data is walled; local IRT tooling hits ceiling

## Context
The PISA 2018 DIF passes showed that item-level psychometric analysis is the most informative tool for separating measurement surface from latent domain. The natural next step was to replicate on TIMSS 2019 item-level data and to extend the Rasch/IRT work to weighted multi-group models.

## Alternatives considered
1. **Push through TIMSS item wall** — Contact IEA for item-response data or apply for restricted access. Pro: would enable direct cross-assessment DIF comparison. Con: unknown timeline, likely requires institutional affiliation.
2. **Extend local IRT to weighted multi-group** — Install heavier IRT packages (mirt via R, or lavaan). Pro: would enable the strongest psychometric identification. Con: `py-irt` has no survey-weight or multi-group support; `girth` handles unweighted Rasch only; switching to R adds friction.
3. **Accept the ceiling and work around it** — Continue with the current `girth`-based hybrid approach (Rasch for theta estimation, logistic regression for DIF, survey weights handled outside the IRT step). Pro: already works, produced 7 robust PISA passes. Con: not a clean joint model.
4. **Drop TIMSS item-level entirely** — Treat TIMSS as aggregate-level only. Pro: no wasted effort. Con: loses a valuable cross-assessment comparison.

## Decision
Options 3 + 4 for now. The TIMSS public files have item columns but they are blank in the actual data payload (confirmed by probing bsausam7.sav and bsaadum7.sav — item columns have 0 nonmissing values). TIMSS remains useful for aggregate grade-transition and cognitive-domain decomposition but not for item-level DIF. The local IRT stack (`girth` Rasch + logistic DIF + survey-weighted stratification) is "good enough" — it produced the anchored-Rasch, theta-DIF, and time-DIF passes that all confirm the PISA family ordering. Weighted joint multi-group IRT is deferred.

## Evidence
- TIMSS G8 public probe: `MP52024`, `MP52058A`, `MP52125`, `SP52006` all have 0 nonmissing values
- `py-irt`: no survey-weight or multi-group API found in package inspection
- `girth`: viable for unweighted Rasch, theta estimation; produced 3 working passes
- PISA 2018 family ordering survives all 7 robustness checks with the hybrid approach

Commits: `dfeaea1` (PISA time-DIF), irt-tooling-feasibility memo, timss-public-item-wall memo

## Revisit if
IEA releases item-response data publicly, or a Python/R multi-group IRT package with survey-weight support becomes easy to integrate.

## Supersedes
None.
