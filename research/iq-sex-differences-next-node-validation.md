# IQ Sex Differences Next Node Validation

**Date:** 2026-03-05

**Scope:** identify the next highest-value causal node after the current `NLSY79`, `NLSY97`, and `PIAAC` passes, then freeze the data strategy, debias rules, and decision logic for validating it.

## Current Observation

The project now has a specific anomaly, not a generic "gender and math" question:

1. `NLSY79` quantitative is male-leaning at about `d = -0.179`; see [iq-sex-differences-second-pass-results.md](iq-sex-differences-second-pass-results.md).
2. `NLSY97` quantitative is slightly female-leaning at about `d = +0.054`; see [iq-sex-differences-nlsy97-replication.md](iq-sex-differences-nlsy97-replication.md).
3. `PIAAC` numeracy is male-leaning across countries, education groups, age bands, and broad occupation groups; see [iq-sex-differences-piaac-frontier.md](iq-sex-differences-piaac-frontier.md) and [iq-sex-differences-piaac-age-occupation.md](iq-sex-differences-piaac-age-occupation.md).

That is an isolated cohort-battery sign flip. It is now the most diagnostic unresolved node because it sits at the fork between:

- a real youth-stage quantitative difference that changed by cohort
- a school-exit sorting effect
- a `CAT-ASVAB` construct / scoring / process artifact

## 2026-03-05 Same-Cohort PIAT / CAT Update

The node is now narrower after [iq-sex-differences-nlsy97-piat-cat-pass.md](iq-sex-differences-nlsy97-piat-cat-pass.md).

Inside the explicit `PIAT` / `CAT` overlap `n=3,738`:

1. `PIAT Math` is slightly male-leaning / near null
2. `Arithmetic Reasoning` is slightly male-leaning / near null
3. `Math Knowledge` is clearly female-leaning
4. `Quantitative = AR + MK` stays only modestly female-leaning because the signal is sitting in `Math Knowledge`

That changes the geometry of the anomaly:

- it is no longer best described as a generic female edge on youth quantitative ability
- it is better described as a same-cohort wedge between a `Math Knowledge`-heavy adaptive surface and the alternate `PIAT` / applied-arithmetic surface

Updated local posterior after this pass:

- `P(H1) = 0.55`
- `P(H2) = 0.25`
- `P(H3) = 0.10`
- `P(H4) = 0.05`

with the remainder carried as model uncertainty around mixed mechanism stories.

So the next node is still the right node, but it is now more specific:

> why does `Math Knowledge` and some school-linked transcript math surfaces tilt female when `PIAT Math` and `Arithmetic Reasoning` do not?

## 2026-03-05 TIMSS Cognitive Update

The focused `TIMSS` pass in [iq-sex-differences-timss-cognitive-split.md](iq-sex-differences-timss-cognitive-split.md) pushes the same node in the same direction.

Key update:

1. from Grade 4 to Grade 8, the biggest femaleward shift is on `knowing`
2. `applying` moves less
3. `TIMSS Advanced` stays male-leaning across domains, especially on `reasoning`

That does not prove the `NLSY97` anomaly is the same mechanism.

It does make the active fork more specific:

> the project now needs to explain why school-knowledge-heavy broad-population surfaces tilt more female with age, while advanced-track and some applied / reasoning surfaces do not.

Updated posterior after the `TIMSS` cognitive split:

- `P(H1) = 0.50`
- `P(H2) = 0.30`
- `P(H3) = 0.08`
- `P(H4) = 0.04`

with the remaining mass still carried by mixed-mechanism uncertainty.

## Causal Check

### Observation Geometry

> **Observation:** one battery-surface, `NLSY97` quantitative on `CAT-ASVAB`, is slightly female-leaning, while the closest broad comparators we have so far, `NLSY79` quantitative and `PIAAC` numeracy, are male-leaning.  
> **Null:** the three batteries are measuring the same latent quantitative trait closely enough that their signs should agree up to noise.  
> **Residual after null:** a directionally different result remains in one cohort-battery pair.  
> **Geometry:** isolated cohort-battery sign flip.  
> **Magnitude:** modest in size, but high in decision value because it changes the verbal story.  
> **Lag window:** late schooling through early labor-market entry.

### Candidate Hypotheses

| ID | Hypothesis | Prior | Why it survives |
| --- | --- | ---: | --- |
| `H1` | `CAT-ASVAB` quantitative in `NLSY97` is not construct-equivalent to `NLSY79` quantitative or `PIAAC` numeracy because of adaptive scoring, item mix, item format, or other score-surface issues. | `0.45` | The anomaly is battery-local and directionally isolated. |
| `H2` | The `NLSY97` sign flip is a real school-exit sorting effect: girls in that cohort accumulated enough recent math exposure, grades, or track advantages to move the near-school-exit quantitative surface. | `0.30` | `NLSY97` sits closest to current schooling and exposes school variables the earlier runs did not use. |
| `H3` | Test-process effects created or inflated the sign flip: computer familiarity, effort, room quality, prior exposure, item completion, or posterior precision differ by sex. | `0.15` | `NLSY97` is adaptive and exposes process-quality variables that can distort observed means. |
| `H4` | Sampling / weighting / missingness drove most of the sign flip. | `0.10` | Always include the artifact null, but current cross-checks make it less specific than `H1` to `H3`. |

### Current Specificity Ranking

1. `H1` is currently the lead explanation because the anomaly is battery-local and the wider adult numeracy surface remains male-leaning even inside education, age, and occupation cells.
2. `H2` remains live because `NLSY97` is the only current cohort that sits close to school exit and includes schooling-context variables we have not yet used.
3. `H3` remains live because `NLSY97` is a computer-adaptive test and the public file exposes unusually rich process-quality variables.
4. `H4` is still a required null, but it currently lacks a sharper prediction than the other three.

**Provisional posterior:**

- `P(H1) = 0.45`
- `P(H2) = 0.30`
- `P(H3) = 0.15`
- `P(H4) = 0.10`

This is not a conclusion about reality yet. It is a ranking of what the next experiment should attack.

## H2 / H4 Split Added After External Review

The first pass treated schooling and missingness too coarsely. For the next tranche, split them:

### H2a - Curriculum Exposure / Track

Sex differences in course ladder, honors, and recent exposure move the near-school-exit quantitative surface.

### H2b - Evaluation / Placement Asymmetry

Grades, recommendations, and some school-placement surfaces are sex-coded enough that they are not clean proxies for latent math. The key footprint is a **grade/test wedge**:

- females retain a positive GPA or placement residual conditional on transcript ladder and standardized math
- males retain a positive standardized-math residual conditional on GPA and ladder

This does **not** directly explain the CAT-ASVAB score by itself. It explains why recent grades and school-placement variables are contaminated mechanism variables rather than nuisance controls.

### H2c - Identity / Aspiration Sorting

At the same measured math level, girls and boys may sort differently into advanced math, STEM intentions, or related coursework. This is a downstream schooling pathway, not the same thing as raw curriculum exposure.

### H4a - Generic Observability / Missingness

The sign flip partly reflects analyzable-subset differences with no more specific behavioral story.

### H4b - Behavior-Driven Observability

Part of the sign flip reflects sex-coded discipline, engagement, or school attachment, which changes who remains in the school-linked or transcript-linked analyzable subset.

This split is useful because it keeps grades and placement from being treated as clean causes when they may already embed evaluation and behavior channels.

## Local Data We Already Have But Have Not Exploited

The `NLSY97` manifest already exposes several channels that can discriminate `H1` to `H3` without downloading anything else:

- recent grades: `ASVAB_AVG_GRADE_REC_XRND`
- subject-taking block: `ASVAB_SUBJ_TAKEN*`
- school / shop exposure proxies: `ASVAB_HS_SCI_*`, `ASVAB_HS_SHOP_*`
- prior ASVAB exposure: `ASVAB_PREV_TAKEN_*`
- computer familiarity and mode comfort: `ASVAB_COMPUTER_USE_*`, `ASVAB_COMPUTER_TEST_*`
- effort and room conditions: `ASVAB_EFFORT_*`, `ASVAB_ROOM_COMFORT_*`, `ASVAB_ROOM_QUIET_*`
- test completeness and measurement precision: `ASVAB_*_ITEMS_COMPLETE_*`, `ASVAB_*_POST_VARIANCE_*`
- test date and age / grade-at-test proxies: `ASVAB_TEST_DATE_*`, `ASVAB_GR_F97_*`

That means the next internal pass should not start with another broad descriptive replication. It should start with a same-cohort cross-surface comparison inside `NLSY97`:

1. `CAT-ASVAB` quantitative versus `PIAT Math`
2. design-only controls first
3. transcript / honors / course-ladder variables as mechanism strata, not primary nuisance controls

This ordering is now preferred over jumping directly to external datasets. See `research/review-1-audit.md`.

## External Data That Actually Moves The Node

### Tier 1: Highest Value

| Dataset | Why it matters | Identification value | Access / notes |
| --- | --- | --- | --- |
| `HSLS:09` | U.S. school-exit pipeline with math assessment plus transcript / school data | Best public U.S. check on whether course-taking and school pipeline explain the near-school-exit math surface | NCES public-use study with transcript and math-related products: <https://nces.ed.gov/surveys/hsls09/> |
| `TIMSS 2019` / `eTIMSS` | Grade-based international math with process data | Better than adult batteries for locating when the math gap appears and whether digital process traces change the story | TIMSS 2019 international database and eTIMSS process-data materials: <https://timssandpirls.bc.edu/timss2019/international-database/> and <https://timssandpirls.bc.edu/timss2019/etimss/> |
| `PISA 2018` + `PISA 2022` | International age-15 math battery with cognitive item data; `2018` is stronger for public cognitive timing / visits, `2022` is still useful for current adaptive/item-content checks | Best public cross-country test of item-format / timing / school-system explanations before labor-market accumulation | OECD database pages: <https://www.oecd.org/en/data/datasets/pisa-2018-database.html> and <https://www.oecd.org/en/data/datasets/pisa-2022-database.html> |

### Tier 2: Strong Complements

| Dataset | Why it matters | Identification value | Access / notes |
| --- | --- | --- | --- |
| `PIAAC` log files | Adult numeracy process traces tied to the same adult surface we already observe | Best test of whether DIF / timing / navigation behavior can explain part of the adult numeracy pattern | OECD / GESIS first-cycle public-use and log-file resources: <https://www.oecd.org/en/data/datasets/piaac-public-use-files.html> and <https://www.gesis.org/en/piaac/rdc/access-to-data/first-cycle> |
| `ELS:2002` | Another U.S. school-to-college longitudinal with math and transcript products | U.S. cohort replication for course-taking / transcript pathways | NCES ELS data products: <https://nces.ed.gov/surveys/els2002/availdataproducts.asp> |
| `TIMSS Advanced 2015` | Advanced mathematics and physics near the upper academic track | Best public check on whether the real disagreement lives in advanced-track selection rather than general numeracy | IEA TIMSS Advanced 2015 international database: <https://timssandpirls.bc.edu/timss2015/advanced/international-database/> |

### Tier 3: High Upside, More Friction

| Dataset | Why it matters | Identification value | Access / notes |
| --- | --- | --- | --- |
| `Project Talent` | Broad cognitive battery plus school context, life-course follow-up, and family structure potential | Could connect spatial / quantitative / track / outcome questions in one design | AIR researcher portal: <https://www.air.org/project-talent/researchers> |
| `NAEP` process + transcript products | Large U.S. assessment and transcript infrastructure | Useful for item-format and course-taking decomposition, but public workflow is less clean than `HSLS` for this exact node | NAEP process-data resources and HSTS pages: <https://www.nationsreportcard.gov/processdata/> and <https://nces.ed.gov/surveys/hst/> |

## Other Perspectives The DOE Must Force Into The Room

### 1. Psychometric Fairness Perspective

Question: does the observed gap live in the latent trait or in item families, item formats, time pressure, and navigation behavior?

Useful anchors:

- Stoevenbelt et al. on time limits and gender gaps in math: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10311959/>
- Li et al. on interpreting DIF with `PIAAC` response-process data: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/>
- Shear on PISA item-format differences by gender: <https://par.nsf.gov/servlets/purl/10433095>

### 2. Education-Pipeline Perspective

Question: do course-taking, track timing, school environment, or confidence / expectation pathways move the observed surface before adulthood?

Useful anchors:

- Perez-Felkner et al. on gendered pathways from math ability beliefs to courses and fields: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5382838/>
- Breda et al. on math intentions over the PISA performance distribution: <https://www.nature.com/articles/s41467-023-39079-z>
- Ravest et al. on the longitudinal development of the math gap in Chile: <https://bibliotecadigital.mineduc.cl/bitstream/handle/20.500.12365/17701/37_PerezMejias2021_Article_ALongitudinalStudyOfTheGenderG.pdf?sequence=1>

### 3. Cross-System Policy Perspective

Question: is the gap sensitive to school-system structure such as tracking, which would argue against a single fixed latent explanation?

Useful anchor:

- cross-country policy analysis using `PISA`: <https://www.tandfonline.com/doi/full/10.1080/02671522.2019.1678065>

The point is not to swallow any one narrative whole. The point is to force the next DOE to face explanations that predict different data footprints.

## Debias Rules

1. Do not treat `NLSY97 quantitative`, `NLSY79 quantitative`, and `PIAAC numeracy` as the same construct just because the labels look similar.
2. Do not treat adjustment for grades, courses, or track as pure causal mediation. Those can be downstream consequences of earlier ability and family inputs.
3. Do not use adult cross-sections to settle school-age causes when school-exit data exist.
4. Do not read a mean gap as a latent-gap result until item-format, DIF, and timing channels are checked.
5. Do not read attenuation from adding controls as explanation unless the comparison is on the same estimation sample.
6. Do not let a single battery decide the story when the current observation itself is a battery disagreement.
7. Pre-register the sign, magnitude, and subgroup predictions for each hypothesis before each new dataset pass.
8. Run specification curves, not one preferred regression.
9. Blind early modeling where possible: have one pass decide transformations and missing-data rules before reopening the sex labels.
10. Keep negative controls in the design. If a proposed mechanism "explains everything," it should also predict domains it should not move.

## DOE

## Stage A - Internal `NLSY97` Node Attack

**Goal:** split `H1`, `H2`, and `H3` using data already in hand.

**Status:** first execution now lives in [iq-sex-differences-nlsy97-stage-a.md](iq-sex-differences-nlsy97-stage-a.md). The main update is that the raw `NLSY97` quantitative female edge does not survive the larger-sample process block cleanly.

### A1. Design-Only Cross-Surface Audit

First run:

- `CAT-ASVAB` `AR`
- `CAT-ASVAB` `MK`
- `CAT-ASVAB` `AR + MK`
- `PIAT Math`

Use only:

- exact age at test
- birth cohort / easy-form risk
- test date / session / site where exposed
- room comfort / quiet

Interpret this as the primary design-comparability test.

### A2. Process / Precision Audit

Add these variable blocks to the `NLSY97` rebuild:

- computer-use / computer-test
- effort and room conditions
- items completed for `AR`, `MK`, `NO`, `CS`
- posterior variance for quantitative-relevant subtests
- exact test date and grade-at-test proxies

**Predictions:**

- If `H3` is doing real work, the sign flip should shrink materially after conditioning on process-quality and precision variables.
- If `H1` is doing more work than `H3`, the overall sign may survive but should concentrate in specific quantitative item families or score-construction choices.

These variables are informative, but they are not a clean primary nuisance block. Treat them as mechanism or fragility channels, not as the main causal adjustment.

### A3. School Exposure Audit

Add these blocks:

- recent grades
- subject-taking variables
- science / shop exposure proxies
- school type and transcript-linked fields where available

**Predictions:**

- If `H2` is right, the female edge should compress or reverse inside comparable school-exposure cells.
- If `H1` is right, the edge should remain unstable across score constructions even after schooling controls.

Interpretive warning:

- grades, honors, and placement variables can be useful mechanism surfaces
- they are not clean ability controls
- if they move coefficients, the next question is whether they are measuring curriculum exposure, evaluation / placement asymmetry, or downstream identity sorting

### A3b. Grade-Test Wedge Audit

Run a same-cohort wedge decomposition inside `NLSY97` once `PIAT Math` and transcript-linked fields are staged.

Primary residuals:

1. `math_grade_residual = GPA net of transcript ladder + standardized math`
2. `math_test_residual = standardized math net of GPA + transcript ladder`

Primary read:

- if females retain a positive grade residual while males retain a positive test residual, then recent grades are partly evaluation / placement surfaces rather than clean latent-math proxies
- if the wedge collapses once ladder and prior math are fixed, then the issue is more curriculum exposure than evaluation asymmetry

Use this as a mechanism audit, not as a proof of motive or ideology.

### A3c. Behavior / Observability Audit

If school-attachment, discipline, or behavior items are staged, estimate:

`P(analyzable school-linked sample | sex, prior math, SES, behavior / discipline / school-attachment items)`

Then compare:

1. raw gap
2. same-sample base gap
3. IPW gap

Interpret this as an observability check. Do **not** put behavior / discipline items directly into the main sex-to-score regression and then call the coefficient movement a causal explanation.

### A4. Score-Surface Stress Test

Run sensitivity analyses for:

- `AR` only
- `MK` only
- `AR + MK`
- `AR + MK + NO`
- IRT-score standardization alternatives
- same-sample complete-case versus imputed / weighted surfaces

**Decision rule:** if the sign changes across plausible score surfaces, that is direct evidence against treating `NLSY97 quantitative` as a stable latent object.

## Stage B - School-Exit Replication Outside `NLSY`

**Goal:** test whether the sign flip survives in datasets closer to school exit with better curriculum information.

### B1. `HSLS:09`

Run math gaps:

- raw
- within transcript course ladder
- within school / counselor context
- within SES and prior achievement cells

**Why first:** this is the cleanest U.S. dataset for transcript and pipeline explanations.

### B2. `ELS:2002`

Replicate the `HSLS` logic one cohort earlier.

**Decision rule:** if `HSLS` and `ELS` both show male-leaning math once course ladders are held roughly constant, `H2` weakens sharply as an explanation for the `NLSY97` female edge.

## Stage C - Item-Format / Timing Natural Experiments

**Goal:** test whether sex differences change with item format, time pressure, or response processes.

### C1. `PISA 2018`

Use:

- math plausible values
- cognitive item file
- public cognitive time / visits files
- school-system and track proxies where exposed

Run:

- male-female gaps by item format
- male-female gaps by response-time / visit burden
- within-country and within-track comparisons

### C2. `PISA 2022`

Use:

- math plausible values
- cognitive item file
- questionnaire timing file
- school-system and track proxies where exposed

Run:

- male-female gaps by item format
- male-female gaps by response-time decile
- within-country and within-track comparisons

Treat this as the current adaptive/item-content complement, not the primary public timing file.

### C3. `TIMSS 2019` / `eTIMSS`

Run:

- item-family and content-domain decomposition
- process-data decomposition where available
- grade-level replication

**Decision rule:** if the gap changes sign or magnitude sharply by item format / time channel, `H1` gains posterior weight.

## Stage D - Upper-Tail / Advanced-Track Check

**Goal:** test whether the real disagreement lives in advanced mathematics selection rather than general numeracy.

Datasets:

- `TIMSS Advanced 2015`
- `Project Talent` if access is workable

**Decision rule:** if upper-track math remains clearly male-leaning while general school-exit math looks flatter, the project should stop talking as if there is one "quantitative" node.

## Stage E - Adult Process Reconciliation

**Goal:** connect the adult numeracy pattern to process data instead of only end scores.

Dataset:

- `PIAAC` log files

Run:

- DIF-informed numeracy decomposition
- timing and action-sequence comparison by sex
- re-estimate gap after removing or down-weighting strongly DIF-like item families

**Decision rule:** if the adult male numeracy gap survives process-aware correction, the "this is mostly test-navigation bias" story weakens materially.

## What Would Actually Change The Conclusion

### Evidence that would harden `H1`

- `NLSY97` sign depends strongly on score construction, item family, item format, timing, or posterior-precision filters.
- `PISA` / `TIMSS` show meaningful sex differences by item format even when overall math is flatter.
- adult `PIAAC` gaps survive within education / age cells but process data shows specific DIF-like families rather than a uniform latent gap.

### Evidence that would harden `H2`

- `HSLS` and `ELS` show near-zero or female-leaning math gaps until transcript course ladders and school pipeline are aligned, after which the gap compresses further.
- `NLSY97` female edge is concentrated in recent high-grade / high-course-exposure girls rather than being general.

### Evidence that would harden `H3`

- the `NLSY97` female edge disappears once process-quality variables and precision filters are applied.
- timing / navigation features explain a material share of item-level DIF in `PISA`, `TIMSS`, or `PIAAC`.

### Evidence that would harden `H4`

- the `NLSY97` sign flip is highly unstable to weights, missing-data handling, or sample restrictions, with no stable subgroup surface behind it.

## Recommended Execution Order

1. Rebuild `NLSY97` with process, precision, and school-exposure variables.
2. Run the `Stage A` audit before downloading another adult dataset.
3. Finish the remaining `PISA` public downloads before adding another large battery family. `TIMSS Grade 4` and `TIMSS Advanced` are now staged locally. See `research/iq-sex-differences-dataset-expansion.md`.
4. Use `PISA 2018` as the first public score-plus-timing school-exit pass, with `TIMSS 2019` grade 4 / grade 8 as the earlier-emergence companion.
5. Keep `HSLS:09` and `ELS:2002` as the first transcript-rich U.S. replications; the public-use respondent bundles are now local, so the gating issue is variable mapping and weighting discipline, not acquisition.
6. Add `PIAAC` log files after the school-exit datasets are in place.
7. Use `TIMSS Advanced` and `Project Talent` for the upper-tail branch, not as the first adjudicator.

## Bottom Line

The next most important causal node is:

> **Is the `NLSY97` quantitative sign flip a real school-exit sorting effect, or is it a battery-local measurement / process artifact?**

Right now the best next move is not another slogan-level argument. It is a targeted `NLSY97` rebuild plus a school-exit replication stack built around `PISA 2018`, `TIMSS 2019`, and then transcript-rich `HSLS:09` / `ELS:2002` using the now-local public-use respondent files.
