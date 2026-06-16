# CYCLE — Immigration causal analysis (autonomous)

Started: 2026-04-18
Goal: Acquire LEHD QWI, Saiz elasticity, E-Verify timing, DACA timing -> estimate native wage compression, link rent burden to housing supply elasticity, run staggered DiD on E-Verify and DACA -> test the observed E-Verify QWI wage margin and refine federal-vs-local incidence split.

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
8. Synthesis memo: observed E-Verify wage-channel update

## Discoveries
- QWI `se` endpoint supports multi-state, multi-quarter batching → 36 API calls returned full 2003-2023 panel for 51 states × 9 industries × 4 education = 151k rows in ~2 min (vs ~20h with naive per-cell loop).
- Saiz 2010 elasticity correlates inversely with FB share at MSA level (descriptive correlation, n=237). Top FB-share quintile median elasticity 1.51 vs bottom 3.40.
- E-Verify mandates show no statistically significant positive QWI wage effect on native low-skill workers in the wage specifications. This cuts against large Borjas-style native wage gains in the observed mandate margin, not every Borjas wage claim or surge/mass-shock regime.
- E-Verify mandates have a negative ~6% stable E1 W-2 employment point estimate in exposed industries, but it is not conventionally significant (t=-1.40, p≈0.16). Consistent in sign with Bohn-Lofstrom-Raphael 2014 AZ finding, but not a measured pooled employment drop. Capital, output, relocation, cash-economy substitution, hours, and composition remain candidate channels rather than measured mechanisms.

## Autonomous (done)
- 2026-04-18 Saiz 2010 MSA elasticity acquired (269 MSAs, 33 KB). Reflection: MIT Urban Economics Lab Google Drive link works one-shot; no scraping needed.
- 2026-04-18 E-Verify state mandate panel compiled from literature (Bohn-Lofstrom-Raphael 2014, Orrenius-Zavodny 2015). 18 states with mandates, 9 with binding all-employer-equivalent scope.
- 2026-04-18 DACA timeline + ACS-eligibility coding documented. Execution deferred (disk constraint, no PUMS pull this cycle).
- 2026-04-18 QWI 2003-2023 state×year×quarter×industry×education panel pulled via batched API (151k rows, 2 MB).
- 2026-04-18 Saiz × ACS rent merge — descriptive cross-section, immigrants concentrate in inelastic MSAs.
- 2026-04-18 E-Verify TWFE on QWI — bounded observed mandate-margin wage update, not a full Card-vs-Borjas verdict.
- 2026-04-18 Synthesis memo + index/ladder updates.

## Verification Results
- Saiz finding: descriptive cross-section with monotonic gradient across quartiles. Replicates known pattern (top-FB MSAs are coastal/inelastic — Miami, LA, SF, NY). PASS as descriptive claim; needs IV for causal interpretation.
- E-Verify TWFE: pre-trends visually flat in event study; formal staggered-DiD robustness was not run. The result is consistent with bounded Card-side wage evidence and passes at the level of "large Borjas-style native wage gains are not observed in this design"; it is not a direct replication of Card-Peri / Foged-Peri or a test of surge, mass-deportation, or extreme counterfactual regimes.

## Known blockers
- SSD unmount blocks reuse of existing warehouse (`acs_origin_*`, `origin_puma_household_context_2023`, etc.). Workaround: rebuild minimal PUMA rent table from Census API for Saiz merge. Not a blocker for LEHD/E-Verify/DACA analyses.

<!-- knowledge-index
generated: 2026-04-19T03:46:13Z
hash: bdb887477d5c

cross_refs: research/immigration-causal-*.md

end-knowledge-index -->
