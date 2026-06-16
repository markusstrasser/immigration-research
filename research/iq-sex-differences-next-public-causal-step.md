# Next Public Causal Step

**Date:** 2026-03-07
**Purpose:** freeze the highest-value remaining causal analysis that is still doable with local public data.

**Status:** executed. The base `PSID CDS` sibling FE, caregiver behavior split, and school-facing teacher follow-up are now complete in `research/iq-sex-differences-psid-cds-first-pass.md`, `research/iq-sex-differences-psid-cds-behavior-pass.md`, `research/iq-sex-differences-psid-cds-teacher-pass.md`, and the branch-level closure memo `research/iq-sex-differences-public-child-branch-ach.md`. The public child branch is now close to saturation. [SOURCE: `research/iq-sex-differences-psid-cds-first-pass.md`; `research/iq-sex-differences-psid-cds-behavior-pass.md`; `research/iq-sex-differences-psid-cds-teacher-pass.md`; `research/iq-sex-differences-public-child-branch-ach.md`]

## Verdict

The best next public-data causal analysis is:

**`PSID CDS` sibling fixed-effects on early math-versus-reading geometry, with behavior/compliance staged separately.**

This is better than another `PISA` proxy pass, better than more `ECLS` descriptives, and better than another generic late-school wedge regression. [INFERENCE]

## Why This One

1. The main child-branch uncertainty is no longer direction; it is whether the aligned early-school relative math pattern survives once shared family background is blocked. [SOURCE: `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md`]
2. `PSID CDS` is public, local, sibling-linkable, and includes Woodcock-style achievement plus caregiver/child behavior modules. [SOURCE: `research/iq-sex-differences-dataset-cards.md`; `sources/iq-sex-diff/data/psid`]
3. A sibling fixed-effects design directly attacks the strongest remaining background alternative without pretending to identify every downstream channel. [INFERENCE]

## Observation, Null, Residual

> **Observation:** once score-family alignment is imposed, the child branch points toward a male relative math edge, but remaining uncertainty is whether that geometry is mostly family composition rather than something that survives inside families. [SOURCE: `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md`]
>
> **Null:** if the pattern is mostly family-background composition, it should attenuate sharply in opposite-sex sibling fixed-effects models. [INFERENCE]
>
> **Residual:** if it survives inside families, the pure background story weakens and the remaining live nodes become latent domain profile, behavior/compliance, and school/test design. [INFERENCE]

## DAG

```text
[Sex] ---------------------------> [Latent domain profile]
  |                                     |
  +-------------------------------> [Behavior / compliance]
                                        |
[Shared family background] ------------>+--------------------+
                                                             |
                                                             v
                                                 [Observed reading / verbal]
                                                 [Observed math / applied problems]
                                                             |
                                                             v
                                                 [Math minus reading geometry]
```

Sibling fixed effects block the shared-family node. They do not identify the latent-domain and behavior channels separately. [INFERENCE]

## Estimands

Primary:

1. `female -> math_z` within family, age-adjusted
2. `female -> reading_z` within family, age-adjusted
3. `female -> math_minus_reading_z` within family, age-adjusted

Secondary:

1. `female x age_bin -> math_minus_reading_z` within family
2. the same outcomes after adding a behavior/compliance index

Interpretation rule:

- the behavior-added spec is a descriptive channel split, not identified mediation
- if the female coefficient on `math_minus_reading_z` remains male-leaning inside families, that is evidence against a pure family-composition story

## Minimum Variable Block

From `PSID CDS`:

- child ID
- family / household ID
- wave / year
- sex
- age
- `Applied Problems`
- `Letter-Word`
- `Passage Comprehension`
- behavior / compliance items from child or caregiver modules
- weights for descriptive summaries where feasible

## Why Not The Other Obvious Options

- `More PISA`: the measurement branch is already near the public-data wall. Another proxy pass is likely repetition, not uncertainty reduction. [SOURCE: `research/iq-sex-differences-irt-tooling-feasibility.md`]
- `More ECLS descriptives`: useful for trajectories, weak for blocking family-level confounding because there is no sibling FE structure.
- `More NLSY97`: the late-school localized wedge is already characterized well enough that another public-use pass is lower leverage than a new child-level family design. [SOURCE: `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`]

## Falsifier

If the within-family `math_minus_reading_z` sex coefficient in `PSID CDS` is near zero across ages, the current early-school causal read should soften sharply toward family-composition explanations. [INFERENCE]

## Decision Impact

If this sibling FE result survives:

1. the early-school node becomes harder to dismiss as background composition
2. the live explanatory frontier shifts toward behavior/compliance and measurement design
3. the project gains a stronger public-data causal foothold before restricted transcript/process access lands
