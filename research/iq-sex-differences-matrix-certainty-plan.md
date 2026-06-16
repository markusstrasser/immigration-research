# IQ Sex Differences - Matrix Certainty Plan

**Date:** 2026-03-07
**Question:** How do we get materially more certainty on the current matrix / abstract-pattern branch without going in circles?

This memo is about the **matrix / figural / Raven-like branch**, not the full `g` question.

## 1. Current Observation

The current local and sourced footprint is:

1. In local open `ICAR` matrix reasoning, males score modestly higher overall (`d = -0.136`, female minus male), all `11/11` checked matrix items are male-leaning, and later / harder items are more male-leaning. Response-rate differences are near zero. [SOURCE: `research/iq-sex-differences-raven-open-data.md`; `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`; `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`]
2. In local `PISA 2018`, the residual content-family ordering survives multiple hardening passes: `space_shape` remains the strongest male-residual family and `uncertainty_data` remains closest to parity. [SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-dif-purified.md`; `research/iq-sex-differences-pisa2018-dif-iterative.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`; `research/iq-sex-differences-pisa2018-dif-rasch.md`]
3. In local `TIMSS Advanced`, `reasoning` remains male-leaning. [SOURCE: `research/iq-sex-differences-timss-cognitive-split.md`]
4. The direct public `Raven` open-data route tried so far did not yield raw rows. [SOURCE: `research/iq-sex-differences-raven-open-data.md`]
5. Recent open psychometric work shows that figural-matrix instruments can be evaluated with modern IRT and invariance methods, and that item-design features can induce sex-related DIF. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11433340/; https://pmc.ncbi.nlm.nih.gov/articles/PMC10551052/; https://eric.ed.gov/?id=EJ984245]

## 2. Causal-Check

**Observation:** Male advantage appears on several matrix / figural / spatially loaded surfaces, and in local open matrix data the harder / later items are more male-leaning without a visible item-reach gap. [SOURCE: `research/iq-sex-differences-raven-open-data.md`; `research/iq-sex-differences-current-position.md`]

**Null:** There is a real but modest male edge on some matrix / figural reasoning surfaces, and much of the remaining argument is about whether that edge is inflated, damped, or selectively localized by test design and item family rather than whether it exists at all. [INFERENCE]

**Residual after null:** We still do not know whether the same geometry survives in a representative raw `Raven`-like dataset after full multi-group latent-variable treatment, nor whether the matrix edge transports to a battery-invariant `g` claim. [INFERENCE]

**Geometry:** clustered on figural-spatial / matrix / advanced-reasoning surfaces, not on every cognitive surface; stronger on harder / later `ICAR` matrix items; not well explained by simple response-time burden in current `PISA`. [SOURCE: `research/iq-sex-differences-raven-open-data.md`; `research/iq-sex-differences-pisa2018-time-dif-theta.md`]

**Magnitude:** current local matrix-only evidence is modest, not huge. `ICAR` matrix `d = -0.136` is real enough to use, but it is not a decisive general-intelligence result. [SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`]

**Most likely cause (0.62):** a real sex difference on some figural-spatial / matrix-like reasoning surfaces, modulated by item design and measurement precision. [INFERENCE]

**Top alternative (0.25):** the observed edge is materially inflated by measurement-surface choices, item family, ceiling / routing structure, or sample-selection artifacts, and would shrink substantially in better representative / latent-variable designs. [INFERENCE]

**Falsifier:** a representative raw matrix dataset with item responses and timing, analyzed under multi-group IRT with partial invariance, showing that the latent male edge disappears or reverses once noninvariant items are handled. [INFERENCE]

**Decision impact:** stop arguing about this branch with pooled composites or GPA wedges. The next uncertainty reduction has to come from matrix-specific psychometrics, open matrix replications, or direct timing/format experiments. [INFERENCE]

## 3. DAG For The Matrix Branch

This is the relevant DAG for observational matrix-score work.

```text
[Sex] --> [Latent figural-spatial reasoning]
[Sex] -?> [Latent verbal/analytic strategy mix]
[Sex] -?> [Response speed / pacing]
[Sex] -?> [Effort / persistence / engagement]

[Family background] --> [Schooling / practice exposure]
[Family background] --> [Selection into sample]
[Age / cohort] --> [Schooling / practice exposure]
[Age / cohort] --> [Selection into sample]
[Country / institution] --> [Schooling / practice exposure]
[Country / institution] --> [Test administration context]

[Schooling / practice exposure] --> [Latent figural-spatial reasoning]
[Schooling / practice exposure] --> [Latent verbal/analytic strategy mix]

[Test design / item family / timing] --> [Observed matrix score]
[Test design / item family / timing] --> [Observed response time]
[Latent figural-spatial reasoning] --> [Observed matrix score]
[Latent verbal/analytic strategy mix] --> [Observed matrix score]
[Response speed / pacing] --> [Observed response time]
[Response speed / pacing] -?> [Observed matrix score]
[Effort / persistence / engagement] --> [Observed matrix score]
[Effort / persistence / engagement] --> [Observed response time]

[Sex] --> [Selection into sample]
[Observed matrix score] --> [Selection into analyzable subset]
[Observed response time] --> [Selection into analyzable subset]
```

## 4. DAG Classification

| Variable | Classification | Temporal Order | Justification |
|----------|----------------|----------------|---------------|
| `Sex` | Treatment (`X`) | fixed before testing | exposure of interest |
| `Observed matrix score` | Outcome (`Y`) | at test | measured endpoint |
| `Observed response time` | Descendant / parallel process | during test | downstream of latent ability, pacing, design |
| `Age / cohort` | Effect modifier / sample-structure variable | before test | affects exposure history and sample composition, does not cause sex |
| `Family background` | Upstream background cause | before test | shapes schooling/practice and selection, does not cause sex |
| `Schooling / practice exposure` | Mediator / descendant of background | before test | part of pathway from background and possibly sexed socialization to score |
| `Test design / item family / timing` | Design node | fixed at administration | changes how latent traits map to observed score |
| `Selection into sample` | Collider / selection node | before or at recruitment | influenced by sex, age/cohort, SES, platform access, motivation |
| `Selection into analyzable subset` | Collider / bad-control risk | after testing | influenced by score, completion, timing, missingness |
| `Current grades / GPA / transcript variables` | Off-branch descendant | later or separate surface | not a confounder of matrix score; wrong branch for this question |

## 5. Valid Adjustment Logic

For the total effect of `Sex -> observed matrix score`, there is **no rich observed back-door adjustment set** in the current open matrix datasets.

That is not a bug in the project. It is the structure of the problem:

1. `age`, `family background`, and `schooling` do not cause sex, so they are not standard confounders of `Sex -> Score`
2. the real threats are:
   - **selection**
   - **measurement noninvariance**
   - **test-design surface**
   - **external validity**

So the right certainty tools are:

1. representative sampling
2. multi-group IRT / partial invariance
3. direct design experiments
4. cross-surface replication

not “control for more variables.”

## 6. Why Causal-Robustness Is Not The Main Lever Here

`PySensemakr` is useful when:

1. there is a well-defined OLS estimand
2. you have a plausible observed adjustment set
3. your main threat is omitted-variable bias

That is **not** the main uncertainty on the matrix branch. The main threats are:

1. measurement noninvariance
2. item-family / timing design
3. ceiling / routing structure
4. convenience-sample selection

So `/causal-robustness` is secondary here. It is appropriate for narrower questions like:

1. `CourseExposure -> MathKnowledge`
2. `Grades -> Attainment`

It is not the main tool for deciding whether a male matrix edge is “real” versus “surface-shaped.” [INFERENCE]

## 7. Certainty Ladder

These are ranked by expected uncertainty reduction, not convenience.

### Tier 1. Recover A Second Raw Open Matrix Dataset

**Why**

Right now the open matrix result is too concentrated in `ICAR`.

**Best targets**

1. `MaRs-IB`
   - open-access item bank
   - initial published sample had `N = 659`, item-level accuracy and response-time summaries
   - later IRT calibration paper has `N = 1501` adults and explicitly models gender, mean response time, and response-time slope
   - current public `OSF` node is real but its storage listing appears empty from the public API
   [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/; https://pmc.ncbi.nlm.nih.gov/articles/PMC10551052/; `sources/iq-sex-diff/data/matrix_open/marsib_g96f4_node.json`; `sources/iq-sex-diff/data/matrix_open/marsib_g96f4_osfstorage.json`]
2. `OMIB`
   - `220` figural matrices
   - openly accessible item bank
   - untimed administration in the published validation study
   - may be easier to use for an original data collection even if raw participant rows are not public
   [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC9326670/]

**What counts as success**

Another open matrix dataset shows either:

1. the same male-leaning harder-item geometry
2. or a materially different geometry that falsifies overconfidence in `ICAR`

### Tier 2. Multi-Group IRT On A Matrix Battery With Raw Item Rows

**Why**

This is the cleanest observational method upgrade.

**Target design**

1. fit a multi-group Rasch / 2PL / partial-invariance model
2. identify anchor items rather than assuming full invariance
3. estimate latent mean difference before and after freeing noninvariant items

**Why it matters**

The 2024 Norwegian Armed Forces figural matrices paper is the right model of what “more certainty” looks like here:

1. unidimensional IRT fit
2. formal measurement invariance tests
3. explicit note that adjusting for invariance reduces but does not eliminate sex differences
4. explicit ceiling warning

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11433340/]

**What counts as success**

1. latent male edge survives partial invariance -> certainty rises
2. latent male edge collapses once noninvariant items are handled -> current matrix claim softens sharply

### Tier 3. Direct Time-Limit Experiment On Released Matrix Items

**Why**

This is the cleanest causal test of the “deweighted speed” dispute.

**Design**

Randomize participants across:

1. tight time limit
2. generous time limit
3. optionally fixed-order vs randomized-order

Use the same or parallel matrix items.

**What this identifies**

1. whether male advantage expands under tighter speed pressure
2. whether current open matrix results are being damped by generous timing
3. whether later-item male lean is partly a time-pressure effect or not

**What counts as success**

If the sex gap moves sharply under timing on the same items, timing design is causally important.
If it barely moves, the latent-domain interpretation strengthens.

### Tier 4. Item-Design Feature Experiment

The 2012 experimental matrices paper is the right template: manipulate item-design features thought to induce male-favoring DIF, not just total difficulty.

Candidate features:

1. rule-direction ambiguity
2. element complexity
3. spatial transformation burden
4. distractor elimination opportunity

[SOURCE: https://eric.ed.gov/?id=EJ984245]

### Tier 5. Predictive-Validity Check

Even if males are modestly better on matrix surfaces, the next certainty question is:

**Does that surface matter the same way for later outcomes?**

Needed:

1. a dataset with matrix-like score plus later STEM / attainment / occupational outcomes
2. sex interactions on predictive validity

This does **not** answer the `g` question directly. It answers whether the matrix edge is merely psychometric or also practically consequential. [INFERENCE]

## 8. What Will Not Materially Raise Certainty

1. Another pooled composite regression on `quantitative` or `IQ`
2. More GPA-based school wedge work to settle the matrix branch
3. More descendant-heavy “explained by” tables
4. More public `PISA` proxy regressions that do not change the latent-variable structure
5. Treating `Raven` as automatically culture-free or schooling-free

## 9. Best Immediate Next Moves

### Fastest high-value move

1. recover or request raw `MaRs-IB` rows
2. if unavailable, build a small original online study using `OMIB` or `MaRs-IB` items
3. randomize time limit and order
4. fit multi-group IRT to the collected data

### Best observational move if restricted data opens

1. get a representative raw matrix dataset with item responses and timing
2. do partial-invariance IRT before any mean comparison

## 10. Current Posterior

**What we can say now**

1. There is enough current evidence to say males are modestly better on some matrix / figural-spatial reasoning surfaces. [SOURCE: `research/iq-sex-differences-raven-open-data.md`; `research/iq-sex-differences-current-position.md`]
2. There is **not** enough current evidence to say that this settles a battery-invariant male `g` advantage. [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-verification.md`]
3. The highest-value certainty increase is now matrix-specific latent-variable work or an original timing/design experiment, not more general observational slicing. [INFERENCE]
