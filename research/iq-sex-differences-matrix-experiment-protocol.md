# IQ Sex Differences - Matrix Experiment Protocol

**Date:** 2026-03-07
**Purpose:** smallest original study that can materially reduce uncertainty on the matrix branch.

## Aim

Test whether the observed male edge on matrix / figural-spatial surfaces is materially sensitive to:

1. time pressure
2. item difficulty
3. spatially loaded item design features

This is a direct causal test of `MeasurementSurface`, not another observational proxy pass. [INFERENCE]

## Design

### Core randomization

Between-subjects:

1. `tight time` condition
2. `generous time` condition

Optional second factor:

1. `fixed order`
2. `randomized order`

### Stimulus source

Use `OMIB` item assets and parameters:

- [omib_item_data_preview.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_item_data_preview.tsv#L1)
- [omib_pilot_forms.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_pilot_forms.tsv#L1)
- [web_version](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/repo/web_version/index.html#L1)

## Pilot forms

The repo now contains two matched `20`-item forms:

- `Form A`
- `Form B`

constructed from balanced difficulty bands, with item metadata carried through.

[SOURCE: `sources/iq-sex-diff/build_omib_pilot_forms.py`; `sources/iq-sex-diff/data/matrix_open/omib/omib_pilot_forms.tsv`]

Operationally, `Form A` should be treated as the **primary first pilot** and `Form B` as the reserve / replication form. They are balanced on difficulty bands, but they should not be assumed psychometrically identical just because they came from the same bank. [INFERENCE]

## Primary outcomes

1. total accuracy
2. item-level correctness
3. completion count
4. response-time pattern if log data are captured

## Main hypotheses

### H1

If timing design suppresses a real speed-linked male advantage, the male-female gap should widen in the `tight time` condition.

### H2

If the male edge is mostly latent-domain / item-family rather than speed, the sex gap should remain similar across time conditions.

### H3

If harder / more spatially loaded items are the main driver, the sex gap should be larger on the higher-`b` and higher-rotation items within each form.

## DAG

```text
Sex --> latent matrix reasoning --> observed accuracy
Sex --> pacing / speed ----------> observed accuracy
Sex --> pacing / speed ----------> completion count

Randomized time limit -----------> observed accuracy
Randomized time limit -----------> completion count
Randomized time limit x Sex -----> gap change of interest

Item difficulty / rotation ------> observed accuracy
Item difficulty / rotation x Sex -> item-level gap heterogeneity
```

Because time limit is randomized, it is admissible as a causal treatment. [INFERENCE]

## Analysis plan

### Descriptive

1. sex gap by condition
2. completion count by condition
3. sex gap by difficulty band
4. sex gap by rotation and rules

### Model

Primary item-level model:

`correct ~ female + tight_time + female:tight_time + difficulty_b + rotation + rules`

with participant-clustered standard errors or a multilevel logit if sample size supports it.

Primary person-level model:

`accuracy_mean ~ female * tight_time`

If a linear model is used, then `/causal-robustness` can be applied to the `tight_time` estimand because the treatment is randomized and omitted-confounding risk is low. [INFERENCE]

## Operational notes

The `OMIB` web template records:

1. a `solution` string
2. a click `log`

That makes it straightforward to collect both accuracy and process data in a survey tool or lightweight web deployment.

[SOURCE: `sources/iq-sex-diff/data/matrix_open/omib/repo/Instructions for Implementation.docx`]

The repo now also contains generated HTML fragments for the current pilot forms under:

- [pilot_web](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/pilot_web#L1)

Those were generated with:

- [build_omib_web_fragments.py](/Users/alien/Projects/research/sources/iq-sex-diff/build_omib_web_fragments.py#L1)
- [score_omib_pilot.py](/Users/alien/Projects/research/sources/iq-sex-diff/score_omib_pilot.py#L1)

## Success criterion

This study reduces uncertainty if it shows either:

1. clear sex-gap movement under timing randomization
2. near-zero gap movement under timing, with residual heterogeneity concentrated in higher-rotation / harder items

Either result is informative. The useless result is a poorly instrumented study with no time logs and no item metadata carried through. [INFERENCE]
