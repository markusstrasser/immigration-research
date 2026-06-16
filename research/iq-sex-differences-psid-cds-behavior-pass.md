# IQ Sex Differences - PSID CDS Behavior Pass

**Date:** 2026-03-07  
**Purpose:** test whether a common caregiver-reported behavior/compliance block materially explains the family-linked child `math minus reading` pattern in public `PSID CDS`.

## What Was Added

The public `PSID CDS` panel now includes a common five-item caregiver behavior block across `1997`, `2002`, and `2007`, merged from the primary caregiver child files. [SOURCE: `sources/iq-sex-diff/psid_cds_build_panel.py`; `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`]

Common items:

- `argues_too_much`
- `difficulty_concentrating`
- `mean_to_others`
- `impulsive`
- `restless`

[SOURCE: `sources/iq-sex-diff/data/psid/unpacked/CDS1997/1997/PCG97_CHLD.do`; `sources/iq-sex-diff/data/psid/unpacked/CDS2002/2002/PCG_CHLD.do`; `sources/iq-sex-diff/data/psid/unpacked/CDS2007/2007/PCG_CHILD07.do`]

Coding note:

- `1997` and `2002` already code `1 = not true`, `3 = often true`
- `2007` reverses that ordering in the public file, so the build recodes `2007` to the same higher-is-worse direction before constructing the pooled index

[SOURCE: `sources/iq-sex-diff/data/psid/unpacked/CDS2007/2007/PCG_CHILD07_codebook.txt`; `sources/iq-sex-diff/psid_cds_build_panel.py`]

## Main Result

The pooled weighted caregiver behavior index is male-worse:

- pooled `d_female_minus_male = -0.263`

By wave:

- `1997`: `-0.295`
- `2002`: `-0.250`
- `2007`: `-0.248`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_behavior_gaps.tsv`]

Inside families, the same direction survives:

- `behavior_index_z ~ female + age + wave + family FE`
- `beta_female = -0.327`
- `SE = 0.055`
- `95% CI [-0.436, -0.218]`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_behavior_fe.tsv`]

So the common caregiver behavior block is not just pooled composition noise. It is sex-separated within families too. [INFERENCE]

## Channel Split

Primary within-family child outcomes:

- `applied_minus_reading`
- `calculation_minus_reading`

Base family fixed-effects result:

- `applied_minus_reading`: `beta_female = -5.087`, `SE = 0.905`
- `calculation_minus_reading`: `beta_female = -4.518`, `SE = 1.497`

After adding the behavior index:

- `applied_minus_reading`: `beta_female = -5.054`, `SE = 0.920`
- `calculation_minus_reading`: `beta_female = -4.982`, `SE = 1.520`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_behavior_fe.tsv`]

That is the important result: this common behavior/compliance block barely moves the family-linked child `math minus reading` pattern. [INFERENCE]

## Causal DAG

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

Interpretation rule:

- the family fixed-effects base model attacks shared-family composition
- the behavior-added model is a descriptive channel split, not identified mediation
- behavior is downstream of `sex`, so conditioning on it does **not** estimate the total effect of `sex`

[INFERENCE]

## Causal Check

> **Observation:** boys are worse on the common caregiver behavior block both descriptively and within-family, but adding that block barely changes the within-family child `math minus reading` gap. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_behavior_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_behavior_fe.tsv`]
>
> **Null:** the public child `math minus reading` pattern is mostly a behavior/compliance story that should collapse once a shared caregiver-rated behavior block is added within families. [INFERENCE]
>
> **Residual:** the common caregiver behavior block is not enough. Either the child pattern is not mainly driven by this mechanism, or this block is only a weak proxy for the school-facing behavior/compliance channel that would matter more for later school surfaces. [INFERENCE]

- `P(cause)`: `0.70` that this common caregiver behavior block does **not** explain most of the public `PSID CDS` within-family child `math minus reading` pattern. [INFERENCE]
- `Top alternative`: `0.20` that the relevant behavior/compliance mechanism is real but undercaptured here because these are caregiver reports rather than school-facing behavior or effort measures. [INFERENCE]
- `Falsifier`: a stronger child behavior/compliance block that materially compresses the same within-family coefficient on a common child surface. [INFERENCE]
- `Decision impact`: the public child branch should stop treating generic caregiver-rated externalizing/attention as the leading explanation. The live child mechanisms narrow toward latent domain profile, psychometric bridge choice, and more school-facing behavior/process channels. [INFERENCE]

## What This Settles

What it settles enough to use:

- the public child branch now has a family-linked behavior check, not just a family-linked score check
- a simple “boys behave worse, therefore the relative math pattern is just behavior” story is weaker

What it does not settle:

- whether teacher-facing or classroom-facing compliance would do more explanatory work
- whether other child anchors would behave differently under the same split
- whether later school knowledge / evaluation surfaces are partly driven by behavior in ways that are not visible in this child caregiver block
