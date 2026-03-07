# IQ Sex Differences Stage -1 / 0A Protocol

**Date locked:** 2026-03-05
**Scope:** freeze the next empirical pass before running `ICAR`, `NLSY79`, `NLSY97`, or `PIAAC` models.
**Machine-readable companion:** `sources/iq-sex-diff/stage0_config.py`

---

## Purpose

This file is the pre-analysis lock for the next work tranche.

It freezes:

1. sign convention
2. estimands
3. ICAR composite grid
4. NLSY79 sibling-pair construction
5. score-layer and weight-layer handling
6. numeric decision thresholds already defined in the DOE

Anything that changes after this file should be treated as an amendment, not as a silent refactor.

## Sign Convention

All descriptive sex gaps use:

`d = (mean_female - mean_male) / pooled_sd`

Interpretation:

- positive values favor females
- negative values favor males

This matches the sign used in the timing-channel note and avoids switching polarity across files.

## Frozen Estimands

### 1. Subtest Mean Gap

Primary descriptive estimand for any subtest or domain:

`d = (mean_female - mean_male) / pooled_sd`

### 2. Within-Family NLSY79 Gap

Primary fixed-effects estimand:

`y_if = alpha_h + beta*female_i + gamma1*age_1981_i + gamma2*older_sibs_1979_i + epsilon_if`

Where:

- `alpha_h` is a household fixed effect using `HHID_1979`
- `female_i` is built from `SAMPLE_SEX_1979`
- `age_1981_i` is `AGE OF R 81`
- `older_sibs_1979_i` is `# SIBS OLDER THAN R 79`

Interpretation:

- `beta` is the within-household sex difference for the chosen subtest
- this is a shared-family-confounding test, not a full environment-purge

### 3. ICAR Composite Sensitivity

The overall sex gap is estimated across the frozen weight grid in [stage0_config.py](/Users/alien/Projects/research/sources/iq-sex-diff/stage0_config.py):

- `equal_weights`
- `verbal_heavy`
- `matrix_heavy`
- `spatial_heavy`

No additional composite weights may be added after inspecting the gaps unless they are marked as post-hoc.

## Frozen Dataset-Specific Score Rules

### ICAR

- Use the raw item matrix in `sapaICARData18aug2010thru20may2013.csv`
- Use the public domain key in `superKey60.tab`
- Score domain means from the fixed item groups:
  - `ln`
  - `mr`
  - `r3d`
  - `vr`
- Require at least `3` scored items per domain because the public SAPA release uses planned missingness and some domains top out at `4` administered items
- Treat the dataset as sample-descriptive and unweighted

### NLSY79

Primary score layer:

- use 1981 ASVAB section **scale scores**
- not raw section labels and not mixed raw / XRND scores

Frozen primary subtests:

- `R0616200` arithmetic reasoning
- `R0616400` word knowledge
- `R0616600` paragraph comprehension
- `R0616800` numerical operations
- `R0617000` coding speed
- `R0617200` auto and shop
- `R0617400` math knowledge
- `R0617600` mechanical comprehension
- `R0617800` electronic information

Sensitivity score layer:

- where available, use the later XRND ability scores for:
  - arithmetic reasoning
  - word knowledge
  - paragraph comprehension
  - math knowledge

Weight rule:

- descriptive ASVAB summaries use `R0614700`
- general background summaries can use `R0216101`
- sibling fixed-effects models are unweighted primary estimates

Missing-data rule:

- treat negative NLSY special codes as missing

### NLSY97

Primary score layer:

- use CAT-ASVAB ability estimates from the public-use XRND fields
- combine the public `POS` and `NEG` fields into one signed score
- use `R0536300` / `KEY!SEX_1997` as the respondent-sex field for this extract
- do not use `R0001000` for sex-gap estimation in the local public-use file because it is largely missing here

Frozen score surface:

- general science
- arithmetic reasoning
- word knowledge
- paragraph comprehension
- numerical operations
- coding speed
- auto information
- shop information
- math knowledge
- mechanical comprehension
- electronic information
- assembling objects

Summary-only sensitivity:

- `R9829600` math-verbal percentile

Weight rule:

- descriptive summaries use `R1236200`

### PIAAC

- analyze country files separately before any pooled estimate
- use all 10 plausible values per domain
- use `SPFWT0` plus the released replicate-weight system
- use `VARSTRAT`, `VARUNIT`, `VEMETHOD`, `VEFAYFAC`, and `VENREPS` as released
- detect delimiter by file family in the current local snapshot:
  - `p1` U.S. files are pipe-delimited
  - `p1` non-U.S. files are comma-delimited
  - current `p2` files are semicolon-delimited
- treat `p1` as the primary education-stratified surface because the current local `p2` files do not expose `EDCAT6/7/8`

## Frozen Domain Definitions

### NLSY79

- `clerical_speed` = mean of z-scored `numerical_operations` and `coding_speed`
- `verbal` = mean of z-scored `word_knowledge` and `paragraph_comprehension`
- `quantitative` = mean of z-scored `arithmetic_reasoning` and `math_knowledge`
- `mechanical` = mean of z-scored `auto_shop` and `mechanical_comprehension`
- `mechanical_plus_electronic` = mean of z-scored `auto_shop`, `mechanical_comprehension`, and `electronic_information`

### NLSY97

- `clerical_speed` = numerical operations + coding speed
- `verbal` = word knowledge + paragraph comprehension
- `quantitative` = arithmetic reasoning + math knowledge
- `mechanical` = auto information + shop information + mechanical comprehension

### ICAR

- `vr`
- `ln`
- `mr`
- `r3d`

## Frozen Covariate Blocks

### Block A: Descriptive

- sex only

### Block B: Minimal Pre-Test Demography

- sex
- age at test or closest age proxy
- race / ethnicity where available

### Block C: Shared-Family FE

- household fixed effect
- sex
- age at test proxy
- older-siblings count as birth-order proxy

### Block D: Pre-Test Schooling / Practice Proxies

Allowed variables are only those clearly measured before or at the test window.

For the first NLSY79 pass, the frozen candidate block is:

- `R0614900` ASVAB high-school grade status in 1981
- `R0006500` mother highest grade completed
- `R0007900` father highest grade completed
- `R0001800` urban / rural at age 14
- `R0009300` number of older siblings

Any later education variable, grade, or occupation measure is a secondary descriptive attenuation block, not a primary mediation block.

## Frozen NLSY79 Pair-Construction Rule

The executable implementation lives in [build_nlsy79_sibling_pairs.py](/Users/alien/Projects/research/sources/iq-sex-diff/build_nlsy79_sibling_pairs.py).

Primary rule:

1. Start from the full public-use respondent file.
2. Build candidate links from the five household-interviewed-youth slots:
   - `IDC1_1979` to `IDC5_1979`
3. Accept a slot as sibling evidence if either:
   - the relationship code is in `{6, 7}`; or
   - the 1993 sibling marker is positive
4. Require reciprocal linkage:
   - respondent `i` lists respondent `j`
   - respondent `j` lists respondent `i`
5. Require shared `HHID_1979`.
6. Keep opposite-sex pairs only for the primary keystone analysis.
7. Use a maximum age gap of 4 years in the primary analysis.
8. Keep one pair per household in the primary analysis.

Tie-break rule for households with multiple eligible opposite-sex pairs:

1. smallest age gap
2. most nonmissing primary ASVAB subtests
3. lowest sorted case IDs

Sensitivity rules:

- age gap <= 6 years
- all eligible opposite-sex pairs
- all sibling pairs including same-sex

## Reporting Firewall

Before any outcome model is run:

1. finish the ICAR write-up
2. finish the NLSY79 descriptive and sibling-FE write-up
3. finish the NLSY97 score-surface write-up
4. finish the PIAAC score / weight checks

This keeps the project from back-fitting psychometric interpretation to later outcome results.

## 2026-03-05 Amendment: NLSY97 Stage A Interpretation

The first `NLSY97` Stage A pass is now frozen as a **robustness / stress-test pass**, not as a clean causal-identification pass. [SOURCE: `research/review-1-audit.md`]

Operational consequence for the next `NLSY97` tranche:

1. **Primary design-only block**
   - exact age at test
   - birth cohort, including `1983` / `1984` easy-form risk
   - test date / session / site where exposed
   - room comfort / quiet only as narrow nuisance controls
2. **Mechanism blocks, kept separate**
   - transcript / honors / course-ladder variables
   - recent grades
   - computer familiarity / prior test-taking
3. **Bad-control stress tests, never primary causal specs**
   - `items_complete`
   - posterior variance
   - effort

Interpretive rule:

- movement under the primary design-only block can update design comparability
- movement under mechanism blocks can update pathway plausibility
- movement under bad-control stress tests can only be used as a fragility warning

Immediate next internal discriminating analysis:

1. same-cohort `NLSY97` cross-surface comparison of `CAT-ASVAB` quantitative versus `PIAT Math`
2. transcript / honors / course-ladder stratification inside that overlap

## 2026-03-05 Amendment: Same-Cohort PIAT / CAT Result

The next internal discriminating analysis is now executed in [iq-sex-differences-nlsy97-piat-cat-pass.md](iq-sex-differences-nlsy97-piat-cat-pass.md).

Operational update:

1. the `NLSY97` anomaly should now be treated as a **same-cohort surface wedge**
2. `PIAT Math` and `Arithmetic Reasoning` do not show the same female edge as `Math Knowledge`
3. future `NLSY97` work should therefore distinguish:
   - applied / reasoning-heavy math
   - school-knowledge-heavy math
   - school-linked transcript outputs

Interpretive rule after this pass:

- raw `NLSY97 quantitative` is no longer admissible as generic evidence about broad quantitative ability
- transcript math surfaces remain mechanism outputs, not nuisance controls
- the next discriminating datasets should emphasize item format and construct mapping, not another generic pooled regression

## 2026-03-06 Amendment: First Deep `NLSY97` Transcript Pass

The first deep late-school pass is now executed in [iq-sex-differences-nlsy97-transcript-deep-pass.md](iq-sex-differences-nlsy97-transcript-deep-pass.md).

Operational update:

1. `Math Knowledge` and transcript math surfaces stay female-leaning after `PIAT`, design, self-reported exposure, and school-offer controls
2. `Arithmetic Reasoning` does not move with that wedge
3. simple course-taking explanations are now weaker
4. the evaluation-heavy block is too attrited to carry the mechanism claim by itself

Interpretive rule after this pass:

- treat the deep transcript result as a **descriptive late-school wedge hardening pass**, not as final causal identification
- keep `course exposure`, `behavior / compliance`, `evaluation`, and `destination` in separate blocks
- do not let a wedge collapse in a `n < 250` evaluation-heavy slice overrule larger-sample design / exposure / offer results
- audit transcript categorical code scales explicitly; `transcript_mathpipe_hstr` uses `100..800`, not `1..8`

Public process-data preference:

- prefer `PISA 2018` over `PISA 2022` for cognitive time / visits work
- use `PISA 2022` mainly for adaptive/item-content checks

## 2026-03-05 Amendment: `PISA 2018` Item / Process First Pass

The first public school-age item/process pass is now executed in [iq-sex-differences-pisa2018-item-split.md](iq-sex-differences-pisa2018-item-split.md).

Operational update:

1. broad `PISA 2018` math is male-leaning in the current public first pass
2. the item surface is heterogeneous, but most math items are still male-leaning
3. simple burden quartile and generic time / visit load do not isolate the female-positive item subset cleanly

Interpretive rule after this pass:

- generic process burden alone is no longer a strong explanation for the school-age split
- the next `PISA` step should be framework-linked item mapping, not another pooled math regression
- movement in process-stress models remains a fragility signal, not causal mediation evidence

## 2026-03-05 Amendment: `PISA 2018` Framework-Proxy Pass

The next `PISA` measurement step is now executed in [iq-sex-differences-pisa2018-framework-proxy.md](iq-sex-differences-pisa2018-framework-proxy.md).

Operational update:

1. the public `PISA` item heterogeneity now has a coherent proxy geometry
2. proxy `space_shape` is the most male-leaning content family in the current pass
3. proxy `uncertainty_data` is the closest to parity
4. the current content ordering survives the higher-confidence sensitivity subset

Interpretive rule after this pass:

- school-age item heterogeneity should now be discussed in content/context terms, not only burden or timing terms
- the current proxy mapping is informative but not final; the official compendium or a second independent coding pass is still needed to harden the result fully
- another pooled `PISA` coefficient is lower-value than official-framework recovery or targeted DIF

## 2026-03-06 Amendment: `PISA 2018` DIF-Style Conditioning Pass

The first ability-conditioned item-fairness screen is now executed in [iq-sex-differences-pisa2018-dif-proxy.md](iq-sex-differences-pisa2018-dif-proxy.md).

Operational update:

1. much of the raw `PISA` item-family geometry compresses once item responses are conditioned on country-standardized overall math ability
2. the residual geometry does not disappear
3. proxy `space_shape` remains the most male-residual content family
4. proxy `uncertainty_data` moves to near parity on average

Interpretive rule after this pass:

- raw item gaps should no longer be treated as if they were the final school-age fairness surface
- the new pass is still a proxy because the conditioning score uses OECD plausible values that likely contain target-item information
- the new pass is useful as a shrinkage diagnostic, not as formal DIF
- do not harden the residual family ordering until the matching score is rebuilt without target-item contamination
- the next `PISA` measurement move is explicit anchor-item, leave-item-out, or IRT DIF before generic `TIMSS` porting

## 2026-03-06 Amendment: Cross-Model Blind-Spot Review

The first cross-model blind-spot review is now recorded in [iq-sex-differences-model-review-2026-03-06.md](iq-sex-differences-model-review-2026-03-06.md).

Operational update:

1. the current `PISA` conditional item pass should be treated as a useful-but-fragile proxy, not as hardened residual DIF geometry
2. the current child bridge resolves the `NLSCYA` versus `ECLS` sign conflict on a relative `math versus reading` estimand, not on a battery-independent absolute math scale
3. later school-surface work should explicitly separate:
   - pre-treatment baseline
   - course exposure
   - behavior / compliance / effort
   - evaluation / grading
4. repeated cuts of the same battery should be described as internal stress tests, not as independent replications

Interpretive rule after this review:

- keep the current `PISA` proxy result, but narrow its language
- keep the child bridge, but stop overstating what the anchor solves
- promote behavior / compliance / stakes into the live late-school mechanism set

## 2026-03-06 Amendment: `PISA 2018` Leave-Out Sensitivity Pass

The contamination-aware `PISA` follow-up is now executed in [iq-sex-differences-pisa2018-dif-leaveout.md](iq-sex-differences-pisa2018-dif-leaveout.md).

Operational update:

1. the residual `PISA` family ordering survives focal-item exclusion
2. it also survives focal-family exclusion
3. the rough low-time sensitivity does not erase the ordering
4. `space_shape` remains the strongest male-residual family and `uncertainty_data` remains closest to parity

Interpretive rule after this pass:

- the old plausible-value proxy is no longer the best available `PISA` conditioning result
- use the leave-out pass as the current operational school-age measurement read
- still do not translate this into a formal DIF claim without explicit anchor-item or IRT work

## 2026-03-05 Amendment: `NLSCYA` Early-School First Pass

The first local early-school pass is now executed in [iq-sex-differences-nlscya-early-school-first-pass.md](iq-sex-differences-nlscya-early-school-first-pass.md).

Operational update:

1. the widened `NLSCYA` intake now includes `PIAT Math` standard scores for `1986`, `1988`, and `1990`
2. the first local early-school `PIAT Math` surface is female-leaning at younger ages and moves toward parity by later childhood
3. early-school dynamics should therefore be treated as empirically open, not as already settled by recent-literature shorthand

Interpretive rule after this pass:

- the early-school node is now locally active and should be replicated in `ECLS-K:2011` immediately
- the project should not talk as if a simple immediate male broad-math divergence is already established in the local data
- late-school transcript and advanced-track mechanisms remain separate from the early-school node

## 2026-03-05 Amendment: `ECLS-K:2011` Early-School First Pass

The first `ECLS-K:2011` replication is now executed in [iq-sex-differences-eclsk2011-early-school-first-pass.md](iq-sex-differences-eclsk2011-early-school-first-pass.md).

Operational update:

1. the local `ECLSK2011_K5PUF.dct` was used to build a minimal six-wave early-school extract from `childK5p.dat`
2. the first pass uses `X1MSCALK5` through `X6MSCALK5`, `X1RSCALK5` through `X6RSCALK5`, revised sex `X_CHSEX_R`, and wave-matched full-sample weights
3. the early-school replication now has two local cohorts with different math shapes: `NLSCYA` and `ECLS-K:2011`

Interpretive rule after this pass:

- the early-school node is no longer speculative; it is active in two local cohorts
- the direction of early-school broad-math emergence is surface- and cohort-sensitive, so one child cohort cannot settle it alone
- the next early-school replication target is the older `ECLS-K` cohort, not more narrative

## 2026-03-05 Amendment: Older `ECLS-K` Early-School First Pass

The older `ECLS-K` school-entry replication is now executed in [iq-sex-differences-eclsk-early-school-first-pass.md](iq-sex-differences-eclsk-early-school-first-pass.md).

Operational update:

1. the older `ECLS-K` child archive required a refreshed concatenation path before the full ASCII could be extracted cleanly
2. the official Stata dictionary uses `_line(n)` sections, so the extractor now reads `15` physical lines per logical record and slices the selected fields from `_line(1)`
3. the current local early-school state now includes `NLSCYA`, `ECLS-K:2011`, and older `ECLS-K`

Interpretive rule after this pass:

- the early-school node is now acquisition-complete enough for score-family alignment work
- the two `ECLS` cohorts are directionally aligned on broad school-entry math
- the live disagreement is no longer whether early-school emergence exists, but why `PIAT Math` and the `ECLS` broad school-entry scales do not share the same geometry

## 2026-03-05 Amendment: Early-School Score Alignment Pass

The first cross-dataset score-family alignment pass is now executed in [iq-sex-differences-early-school-score-alignment.md](iq-sex-differences-early-school-score-alignment.md).

Operational update:

1. the alignment pass uses paired math and reading within the same child-wave surface
2. math and reading are standardized within wave before comparison
3. the key aligned surface is `math_minus_reading_z`, plus the weighted `math_z ~ female + reading_z` regression

Interpretive rule after this pass:

- raw child math gaps should no longer be compared across `NLSCYA` and `ECLS` without an internal anchor
- the first reading-anchor pass removes most of the directional conflict between `NLSCYA` and the two `ECLS` cohorts
- the next early-school question is now magnitude / timing mismatch, not sign mismatch

## 2026-03-05 Amendment: Early-School Age-Matched Alignment Pass

The next bridge step is now executed in [iq-sex-differences-early-school-age-matched-alignment.md](iq-sex-differences-early-school-age-matched-alignment.md).

What changed:

1. `ECLS-K:2011` was extended to later valid assessment waves with explicit age fields
2. the child bridge now uses explicit age bins instead of broad wave matching
3. older `ECLS-K` remains usable for the early valid-age window, but its wave `5` age field is not on the same month scale and should not be reused for late child age matching

Implications:

1. the early-school sign conflict is now treated as resolved locally
2. the live child-level question is the remaining aligned magnitude mismatch between `NLSCYA` and `ECLS-K:2011`
3. the next highest-leverage unresolved node shifts back toward the deeper `NLSY97` transcript payload pass unless a stronger psychometric child bridge becomes easy

## 2026-03-06 Amendment: Late-School DAG And Robustness Discipline

The first explicit late-school DAG and robustness pass is now executed in [iq-sex-differences-nlsy97-course-dag-robustness.md](iq-sex-differences-nlsy97-course-dag-robustness.md).

What changed:

1. late-school `NLSY97` work is now split into two estimands:
   - total `sex -> MathKnowledge` effect
   - current course-exposure effect on `MathKnowledge`
2. those estimands do **not** share the same valid control set
3. for the total effect of `sex`, `PIAT`, current ladder, grades, transcript outputs, honors, and process variables are not ordinary nuisance controls
4. for the narrower course-exposure question, the first observed DAG-valid set is `{sex, age, PIAT proxy, school-offer proxies}`
5. the first course-exposure pass does not show a clean positive explanation of the `Math Knowledge` wedge, and the observed exposure estimate is fragile under omitted-confounding sensitivity

Implications:

1. no new late-school regression should be interpreted causally unless it names the treatment, names the estimand, and passes a DAG audit first
2. any OLS causal fit worth discussing should now get a post-estimation robustness pass rather than relying only on coefficient movement
3. the next late-school mechanism branch is behavior / compliance versus evaluation-family surfaces, not generic current course-taking

## Decision Thresholds

These thresholds are frozen here and mirrored in [stage0_config.py](/Users/alien/Projects/research/sources/iq-sex-diff/stage0_config.py):

- strong within-family persistence: within-family coefficient is at least `50%` of the raw gap and the `95%` CI excludes zero
- sharp attenuation: clerical-speed coefficient attenuates by at least `40%` while the comparable nonclerical coefficient attenuates by less than `20%`
- large composite movement: gap moves by at least `0.15` SD across the frozen composite grid
- weak outcome increment: partial `R^2 <= 0.005` or standardized coefficient `< 0.05` after the full control set

## Immediate Execution Order

1. regenerate the NLSY ASVAB manifest
2. run the Stage 0 audit utility
3. build the NLSY79 sibling-pair file
4. run ICAR decomposition
5. run NLSY79 raw-gap and sibling-FE models

That is the locked next tranche. It is enough to start real empirical work without drifting back into narrative.

Current execution status:

- ASVAB manifest regenerated with the full `NLSY97` CAT-ASVAB ability-estimate block
- Stage 0 audit snapshot written to `sources/iq-sex-diff/data/stage0_audit_snapshot.json`
- NLSY79 pair builder produced `1,461` opposite-sex pairs in `sources/iq-sex-diff/data/nlsy/nlsy79_opposite_sex_sibling_pairs.tsv`
- NLSY79 same-sample schooling check and stats-stack pass written to `research/iq-sex-differences-second-pass-results.md`
- NLSY97 respondent-sex field corrected to `R0536300` / `KEY!SEX_1997` in the frozen config
- NLSY97 CAT-ASVAB replication written to `research/iq-sex-differences-nlsy97-replication.md`
- narrow cached extracts written to `sources/iq-sex-diff/data/nlsy/nlsy79_analysis_extract.parquet` and `sources/iq-sex-diff/data/nlsy/nlsy97_analysis_extract.parquet`
- PIAAC `p1` education-stratified frontier written to `research/iq-sex-differences-piaac-frontier.md`
- PIAAC age / occupation extension written to `research/iq-sex-differences-piaac-age-occupation.md`
- next-node validation memo written to `research/iq-sex-differences-next-node-validation.md`
- NLSY97 Stage A process / school pass written to `research/iq-sex-differences-nlsy97-stage-a.md`
- external review audit written to `research/review-1-audit.md`
- TIMSS Grade 4 versus Grade 8 and TIMSS Advanced pass written to `research/iq-sex-differences-timss-frontier.md`
- HSLS transcript-rich wedge pass written to `research/iq-sex-differences-hsls-wedge-first-pass.md`
- HSLS wedge outputs written to `sources/iq-sex-diff/data/hsls/hsls_wedge_*.tsv` and `sources/iq-sex-diff/data/hsls/hsls_wedge_extract.parquet`
- NLSY97 same-cohort `PIAT` versus `CAT` pass written to `research/iq-sex-differences-nlsy97-piat-cat-pass.md`
- NLSY97 `PIAT` / `CAT` outputs written to `sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_*.tsv` and `sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat*_extract.parquet`
- focused `TIMSS` cognitive split written to `research/iq-sex-differences-timss-cognitive-split.md`
- focused `TIMSS` cognitive outputs written to `sources/iq-sex-diff/data/timss_cognitive_split/*.tsv`
- `PISA 2018` item / process first pass written to `research/iq-sex-differences-pisa2018-item-split.md`
- `PISA 2018` outputs written to `sources/iq-sex-diff/data/pisa/pisa2018_*.tsv` and `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
- `PISA 2018` framework-proxy pass written to `research/iq-sex-differences-pisa2018-framework-proxy.md`
- `PISA 2018` framework-proxy outputs written to `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_*.tsv`
- widened `NLSCYA` variable map and extract written to `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv` and `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`
- `NLSCYA` early-school first pass written to `research/iq-sex-differences-nlscya-early-school-first-pass.md`
- `NLSCYA` early-school outputs written to `sources/iq-sex-diff/data/nlscya/nlscya_early_school_*.tsv` and `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
- `ECLS-K:2011` early-school first pass written to `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`
- `ECLS-K:2011` early-school outputs written to `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_*.tsv` and `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
- older `ECLS-K` early-school first pass written to `research/iq-sex-differences-eclsk-early-school-first-pass.md`
- older `ECLS-K` early-school outputs written to `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_*.tsv` and `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`
- early-school score-alignment pass written to `research/iq-sex-differences-early-school-score-alignment.md`
- early-school alignment outputs written to `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_*.tsv` and `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_pairs.parquet`
- age-matched early-school alignment pass written to `research/iq-sex-differences-early-school-age-matched-alignment.md`
- age-matched early-school alignment outputs written to `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_*.tsv` and `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_pairs.parquet`
- late-school DAG and robustness memo written to `research/iq-sex-differences-nlsy97-course-dag-robustness.md`
- DAG validator outputs written to `sources/iq-sex-diff/data/nlsy/nlsy97_dag_*.json`
- course-causal model outputs written to `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_models.tsv` and `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_model_data.csv`
- robustness outputs written to `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_sensemakr_*.json` and `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_partial_r2.tsv`
