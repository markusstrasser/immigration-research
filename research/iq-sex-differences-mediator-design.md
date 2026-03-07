# IQ Sex Differences - Mediator Design

**Date:** 2026-03-06  
**Purpose:** freeze a DAG-valid mediator design for the outcome branch so future work stops reusing attenuation tables as if they were identified causal mediation.

## Why This File Exists

The repo now has enough public evidence to say two things at once:

1. school-linked evaluation surfaces carry real later-attainment signal
2. attenuation in `sex -> attainment` models after adding grades, `PVT`, or child batteries is **not** identified mediation

[SOURCE: `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-school-outcome-interactions.md`]

This file exists to stop estimand slippage.

## Target Question

The outcome branch should answer this narrower question:

> Through which surface families does the female later-attainment edge appear to travel, and which parts of that decomposition can actually be identified with the current data?

[INFERENCE]

It should **not** answer:

> What is the direct effect of sex after controlling for grades, test scores, and school pipeline variables?

That question is usually structurally invalid in the current datasets because those controls are descendants of sex. [INFERENCE]

## Observation To Explain

> **Observation:** across the public outcome branch, later female attainment remains positive, adolescent school/evaluation surfaces partially compress that residual in `Add Health`, early-child cognitive surfaces barely compress it in `FFCWS`, and public outcome interactions do not support a strong generic “female school surfaces are inflated and low-value” story. [SOURCE: `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-school-outcome-interactions.md`]
>
> **Null:** if the remaining female later-attainment edge were already explained by one clean observed mediator block, the observed attenuation story would be both large and structurally valid. [INFERENCE]
>
> **Residual after null:** it is not structurally valid as mediation identification. The current public branch is informative about channels, but only descriptively. [INFERENCE]

- `P(cause)`: `0.86` that the main current problem is estimand confusion rather than lack of more coefficients. [INFERENCE]
- `Top alternative`: `0.10` that one of the current public cohorts already supports a near-identified mediation result and the repo is being too conservative. [INFERENCE]
- `Falsifier`: a public cohort with a DAG-valid treatment, mediator, and outcome structure where mediator-outcome confounding is credibly handled using only pre-treatment observables. [INFERENCE]
- `Decision impact`: freeze the estimands now, or future analyses will keep cycling between total-effect, decomposition, and direct-effect language. [INFERENCE]

## Estimands

There are four different estimands in play. Keep them separate.

### 1. Total effect of `female -> attainment`

Question:

> What is the overall association or causal effect of sex on later attainment under a background-only adjustment set?

This is the only sex-effect estimand that is usually admissible in the current public data. [INFERENCE]

### 2. Descriptive channel decomposition

Question:

> How much does the female later-attainment coefficient shrink when observed downstream surfaces are added on the same sample?

This is what the current attenuation tables actually estimate. Useful, but not causal mediation. [INFERENCE]

### 3. Predictor-value or effect-modification

Question:

> Do grades or test scores have materially different downstream slopes by sex?

This is what the current interaction tables estimate. It is not mediation either. [INFERENCE]

### 4. Causal mediation / interventional indirect effects

Question:

> How much of the effect of sex on attainment would change under a hypothetical intervention on school evaluation, tested math, or transcript exposure?

This requires stronger assumptions and better mediator/confounder measurement than the public stack currently gives. [INFERENCE]

## DAG 1 - Total Effect: `female -> attainment`

### Variable classification

| Variable | Classification | Temporal order | Justification |
| --- | --- | --- | --- |
| `female` | Treatment | fixed at birth | exposure of interest |
| `attainment` | Outcome | young adulthood / adulthood | later education outcome |
| `family SES` | Pre-treatment confounder | before schooling surfaces | affects opportunities and attainment |
| `parent education` | Pre-treatment confounder | before schooling surfaces | affects schooling context and attainment |
| `family structure at baseline` | Pre-treatment confounder | before schooling surfaces | affects both school process and later attainment |
| `race/ethnicity` | Pre-treatment background factor | before schooling surfaces | stratifies school context and attainment surfaces |
| `grades` | Descendant / mediator | after exposure, during schooling | downstream school-performance surface |
| `tested math` | Descendant / mediator | after exposure, during schooling | downstream tested surface |
| `transcript variables` | Descendant / mediator | after exposure, during schooling | downstream course/grade structure |
| `behavior/compliance in school` | Usually descendant / mediator | after schooling begins | partly caused by sexed school and social pathways |

### DAG

```text
female -> school_behavior
female -> school_evaluation
female -> tested_math
female -> transcript_exposure
female -> attainment

family_SES -> school_behavior
family_SES -> school_evaluation
family_SES -> tested_math
family_SES -> transcript_exposure
family_SES -> attainment

parent_education -> school_behavior
parent_education -> school_evaluation
parent_education -> tested_math
parent_education -> transcript_exposure
parent_education -> attainment

family_structure -> school_behavior
family_structure -> school_evaluation
family_structure -> tested_math
family_structure -> transcript_exposure
family_structure -> attainment

race_ethnicity -> school_behavior
race_ethnicity -> school_evaluation
race_ethnicity -> tested_math
race_ethnicity -> transcript_exposure
race_ethnicity -> attainment

school_behavior -> school_evaluation
school_behavior -> tested_math
school_behavior -> transcript_exposure
school_evaluation -> attainment
tested_math -> attainment
transcript_exposure -> attainment
```

### Valid adjustment set

For the total effect, the admissible set is background only:

- `family SES`
- `parent education`
- `family structure`
- `race/ethnicity`
- cohort / age nuisances where appropriate

### Forbidden controls

- `grades`
- `GPA`
- `tested math`
- `transcript quantity`
- `course ladder`
- `school encouragement / belonging / homework`
- `PVT` or child scores when they are descendants of earlier schooling or sexed development pathways in the same life-course model

These are not clean nuisance controls for the total effect. [INFERENCE]

## DAG 2 - Descriptive School-Evaluation Decomposition

### Target

This is **not** a total-effect DAG. It is a channel-description DAG.

Question:

> Conditional on baseline background, how much does the female later-attainment coefficient move when school-evaluation variables are added?

### Variable classification

| Variable | Classification | Temporal order | Justification |
| --- | --- | --- | --- |
| `school_evaluation` | Mediator bundle | during school | grades, teacher recognition, recommendation, GPA |
| `tested_math` | Parallel mediator bundle | during school | standardized test or ability surface |
| `transcript_exposure` | Parallel mediator bundle | during school | course-taking / credits / ladder |
| `school_behavior` | Mediator or mediator-outcome confounder | during school | can affect both evaluation and later attainment |

### Design rule

These models may be run, but they must be labeled:

- `descriptive channel decomposition`
- `descendant-path attenuation`

They may **not** be labeled:

- `direct effect`
- `controlled effect`
- `mediation identified`

unless stronger assumptions are explicitly defended. [INFERENCE]

## DAG 3 - Tested-Surface Mediation Branch

### Question

> Does a tested-math surface mediate more of the later-attainment edge than evaluation surfaces do?

### Problem

With current public data, the tested surfaces are too inconsistent across cohorts:

- `Add Health` public has `PVT`, not clean same-wave tested math
- `FFCWS` has early-child batteries, not transcript-linked adolescent test surfaces
- `PSID TAS` has `SAT/ACT` plus GPA, but not the richer school process block

[SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `research/iq-sex-differences-ffcws-achievement-first-pass.md`; `research/iq-sex-differences-psid-tas-transition-first-pass.md`]

So the current public stack can compare channel families descriptively, but not estimate a clean common tested-surface indirect effect. [INFERENCE]

## DAG 4 - Behavior / Compliance / Evaluation Chain

### Question

> Are behavior/compliance variables upstream of the evaluation family, and can they explain the later school-evaluation wedge?

### DAG

```text
female -> behavior_compliance
female -> school_evaluation
female -> tested_math
female -> attainment

background -> behavior_compliance
background -> school_evaluation
background -> tested_math
background -> attainment

behavior_compliance -> school_evaluation
behavior_compliance -> tested_math
behavior_compliance -> attainment
school_evaluation -> attainment
tested_math -> attainment
```

### Key implication

If the treatment is still `female`, then `behavior_compliance` is usually downstream and cannot be treated as an ordinary control for the total effect.

If the treatment changes to `behavior_compliance`, then sex becomes a background cause and the estimand changes completely. [INFERENCE]

That is why the repo’s current behavior blocks belong in mechanism triage, not in the main sex-effect adjustment set. [SOURCE: `research/iq-sex-differences-school-wedge-mechanism-triage.md`; `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`]

## What Public Data Can Identify Now

### Admissible with current public data

1. total-effect background-adjusted `female -> attainment`
2. descriptive attenuation under named descendant bundles
3. effect-modification / predictor-value checks by sex
4. family-by-family synthesis of which mediator bundles are stable across cohorts

### Not identified cleanly now

1. natural direct effects
2. natural indirect effects
3. controlled direct effects after grades/tests/transcripts are controlled
4. “how much of the female attainment edge is caused by evaluation bias” as a causal scalar

[INFERENCE]

## Public-Use Analysis Ladder

Use this order for any new outcome branch analysis.

### Step 1 - total effect

Fit:

`attainment ~ female + background`

with a DAG-valid background-only set.

### Step 2 - named channel decompositions

Run separate same-sample decompositions:

1. `+ school_evaluation_bundle`
2. `+ tested_surface_bundle`
3. `+ transcript_exposure_bundle`
4. `+ combined_bundle`

Report them as attenuation tables only. [INFERENCE]

### Step 3 - interaction / predictive-value

Run:

`attainment ~ female + predictor + female*predictor + background`

for the main school/test predictors.

### Step 4 - synthesis

Compare which channel family moves more across cohorts.

Do **not** average them into one “mediation” coefficient. [INFERENCE]

## Restricted-Data Upgrade Path

The first restricted-data upgrade should target the late-school node where the current public stack is weakest.

### `Add Health` restricted / `AHAA`

Needed to estimate:

1. transcript-coded course exposure
2. transcript-coded math/science GPA
3. transcript-coded curricular intensity
4. school-context or school-offer structure if available

This would support a better late-school mediator family comparison:

- evaluation
- transcript quantity
- transcript grade
- tested anchors

[SOURCE: https://addhealth.cpc.unc.edu/wp-content/uploads/docs/user_guides/DesignPaperWave_I-IV.pdf; `research/iq-sex-differences-restricted-data-plan.md`]

### `HSTS`

Needed to decide whether public suppression is hiding the true relation between:

1. transcript quantity
2. transcript grade
3. tested math
4. later transition outcomes or advanced-track positioning

[SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]

### `NAEP` process

Needed if the goal is not just mediation but also test-surface correction:

1. item timing
2. revisits
3. rapid guessing
4. navigation structure

[SOURCE: https://www.nationsreportcard.gov/process_data/]

## Minimal Reporting Template

Any future outcome-branch memo should state:

1. **Treatment**
2. **Outcome**
3. **Estimand**
4. **Valid background adjustment set**
5. **Whether downstream variables are being used descriptively or causally**
6. **What remains unidentified**

If a memo cannot fill those six lines cleanly, it should not claim mediation. [INFERENCE]

## Bottom Line

The repo now has enough evidence to stop speaking loosely about mediation.

Current public analyses support:

1. total-effect estimation under background-only adjustment
2. descriptive channel decomposition
3. predictor-value checks

They do **not** support:

1. direct-effect rhetoric after grades/tests are controlled
2. identified mediation of the female attainment edge

[INFERENCE]
