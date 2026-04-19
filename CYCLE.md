# CYCLE — Immigration causal analysis (autonomous)

Started: 2026-04-18
Goal: Acquire LEHD QWI, Saiz elasticity, E-Verify timing, DACA timing → estimate native wage compression, link rent burden to housing supply elasticity, run staggered DiD on E-Verify and DACA → resolve Card-vs-Borjas verdict for U.S. data and refine federal-vs-local incidence split.

Working dir: `sources/immigration-causal/data/` (gitignored)
Scripts: `sources/immigration-causal/scripts/`
Output memos: `research/immigration-causal-*.md`

## Context constraints
- 15 active claude processes → rate-limit mode (subagent-light, avoid Codex dispatch)
- External SSD unmounted → existing warehouse unavailable, work standalone on new datasets
- 13 GiB free internal disk → keep LEHD pulls targeted (5 states max, by-county aggregations)

## Queue (executing in order)
1. Saiz 2010 elasticity (smallest, fastest)
2. E-Verify state mandate panel (text data)
3. DACA timing + ACS-eligibility coding
4. LEHD QWI county × industry × demographic for AZ, MS, CA, TX, NV
5. Wage compression analysis on LEHD
6. Saiz × PUMA rent burden link
7. E-Verify staggered DiD
8. Synthesis memo: Card-vs-Borjas verdict

## Discoveries
(none yet)

## Active Plan
Phase A — Acquisition (parallel where independent)
Phase B — Wage analysis on LEHD (depends on A.1, A.2, A.4)
Phase C — Saiz × rent merge (depends on A.1; warehouse PUMA table not accessible until SSD mounted, so build standalone PUMA-level table from ACS-API instead)
Phase D — DACA design (depends on A.3; ACS PUMS access via IPUMS API or census.gov)
Phase E — Synthesis

## Autonomous (done)
(none yet)

## Verification Results
(none yet)

## Known blockers
- SSD unmount blocks reuse of existing warehouse (`acs_origin_*`, `origin_puma_household_context_2023`, etc.). Workaround: rebuild minimal PUMA rent table from Census API for Saiz merge. Not a blocker for LEHD/E-Verify/DACA analyses.

<!-- knowledge-index
generated: 2026-04-19T03:25:33Z
hash: 661fc7dcd930

cross_refs: research/immigration-causal-*.md

end-knowledge-index -->
