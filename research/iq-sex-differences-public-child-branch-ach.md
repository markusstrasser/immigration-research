# IQ Sex Differences - Public Child Branch ACH

**Date:** 2026-03-07  
**Purpose:** decide whether the remaining public child branch is still genuinely unresolved or whether the surviving explanation is already narrow enough that more public slicing will mostly repeat known results.

## Framing

**Observation:** across the public child branch, aligned `math minus verbal/reading` surfaces are now directionally male in `ECLS`, anchored `NLSCYA`, and family-linked `PSID CDS`; the remaining uncertainty is magnitude, anchor choice, and score family, not sign. [SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`; `research/iq-sex-differences-child-bridge-multi-anchor.md`; `research/iq-sex-differences-child-bridge-rank-sensitivity.md`; `research/iq-sex-differences-psid-cds-first-pass.md`]

**Geometry:** persistent sign with changing magnitude and anchor sensitivity, not a sharp break. [INFERENCE]

**Null process:** if there is no stable child branch at all, different anchors, school-entry scales, family composition, and behavior proxies should produce unstable sign and frequent reversals. [INFERENCE]

## Competing Hypotheses

- `H1`: there is a real child relative-domain divergence, modestly male on `math minus verbal`, and score-family / anchor choice mainly changes its magnitude rather than its direction
- `H2`: the public child branch is mostly a generic behavior/compliance artifact
- `H3`: the public child branch is mostly a school-facing teacher-perception / evaluation artifact
- `H4`: the public child branch is mostly family composition / sample artifact

Priors:

- `H1 = 0.35`
- `H2 = 0.25`
- `H3 = 0.20`
- `H4 = 0.20`

[INFERENCE]

## Diagnostic Evidence

### E1. Family-linked `PSID CDS` remains male on aligned child `math minus reading`

Prediction:

- `H1`: expected
- `H2`: possible but should shrink once behavior enters
- `H3`: weakly expected only if teacher/school channels are already embedded before direct observation
- `H4`: less expected because family fixed effects should sharply reduce it

Finding:

- aligned child `math minus reading` remains male in public family fixed effects

[SOURCE: `research/iq-sex-differences-psid-cds-first-pass.md`]

### E2. Multi-anchor and rank-based checks keep `PSID CDS` male under every tested verbal anchor, with `PPVT` the weak exception

Prediction:

- `H1`: expected
- `H2`: less expected
- `H3`: less expected
- `H4`: less expected

Finding:

- public child bridge is no longer reading-only and no longer obviously a raw-scale artifact

[SOURCE: `research/iq-sex-differences-child-bridge-multi-anchor.md`; `research/iq-sex-differences-child-bridge-rank-sensitivity.md`]

### E3. Generic caregiver behavior is clearly more male but barely changes the family-linked child bridge

Prediction:

- `H1`: expected
- `H2`: strongly inconsistent
- `H3`: not very diagnostic
- `H4`: weakly inconsistent

Finding:

- common caregiver behavior block does not materially compress the public child bridge

[SOURCE: `research/iq-sex-differences-psid-cds-behavior-pass.md`]

### E4. School-facing teacher behavior is also clearly more male, but on the richer `1997` teacher subset the aligned child bridge still survives

Prediction:

- `H1`: expected
- `H2`: inconsistent if behavior was supposed to be the main driver
- `H3`: inconsistent if teacher perception was supposed to dissolve the bridge
- `H4`: weakly inconsistent

Finding:

- public teacher behavior/disruption does not collapse the `1997` aligned child bridge

[SOURCE: `research/iq-sex-differences-psid-cds-teacher-pass.md`]

### E5. `2002` teacher relative math-versus-reading rating points male, not female

Prediction:

- `H1`: expected
- `H2`: weakly expected
- `H3`: inconsistent with a simple female-favoring teacher-perception explanation
- `H4`: not very diagnostic

Finding:

- teacher math-versus-reading relative rating is directionally more male

[SOURCE: `research/iq-sex-differences-psid-cds-teacher-pass.md`]

### E6. Early-school age-matched bridge resolves the old sign conflict

Prediction:

- `H1`: expected
- `H2`: less expected
- `H3`: less expected
- `H4`: inconsistent

Finding:

- once child math is aligned to same-wave verbal anchors and overlapping ages, the sign conflict between `NLSCYA` and `ECLS-K:2011` disappears

[SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`; `research/iq-sex-differences-early-school-score-alignment.md`]

## ACH Matrix

| Evidence | H1 | H2 | H3 | H4 |
| --- | ---: | ---: | ---: | ---: |
| E1 family-linked `PSID CDS` male | 0.75 | 0.45 | 0.40 | 0.20 |
| E2 multi-anchor/rank stability | 0.80 | 0.35 | 0.30 | 0.20 |
| E3 caregiver behavior fails to compress | 0.75 | 0.15 | 0.45 | 0.35 |
| E4 teacher behavior fails to compress | 0.70 | 0.20 | 0.20 | 0.35 |
| E5 teacher math-vs-reading points male | 0.70 | 0.45 | 0.10 | 0.35 |
| E6 age-matched sign conflict dies | 0.80 | 0.40 | 0.35 | 0.10 |

[INFERENCE]

Raw posterior shape after multiplicative scoring:

- `H1`: dominant
- `H2`: weak surviving alternative
- `H3`: strongly weakened
- `H4`: strongly weakened

[INFERENCE]

Calibrated read after accounting for evidence dependence:

- `H1 = 0.62`
- `H2 = 0.18`
- `H3 = 0.10`
- `H4 = 0.10`

[INFERENCE]

## Why The Losers Lose

- `H2` loses because both caregiver-facing and school-facing behavior blocks point male but do not dissolve the child bridge. The branch is not behavior-free, but “mostly behavior” no longer fits the evidence geometry. [INFERENCE]
- `H3` loses because the available teacher-facing evidence does not point in a female-math direction. In `2002`, teacher relative math-versus-reading ratings point male rather than female. [INFERENCE]
- `H4` loses because family fixed effects, age-matched alignment, and multi-anchor stability all reduce the space for a simple composition or sample-artifact story. [INFERENCE]

## Verdict

> **Most likely cause (`62%`):** `H1` — the public child branch is best explained by a real but modest relative-domain split, with score-family and anchor choice changing magnitude more than direction. [INFERENCE]
>
> **Top alternative (`18%`):** `H2` — behavior/compliance still matters, but the current public caregiver and teacher blocks do not support it as the main driver. [INFERENCE]
>
> **Falsifier:** a stronger public or restricted school-facing child panel where teacher ratings, placements, or transcript-like signals materially compress the same within-family child `math minus reading` effect. [INFERENCE]
>
> **Decision impact:** the public child branch is close to saturation. More public slicing is unlikely to overturn its current directional read. The next uncertainty reduction should come from psychometric refinement or restricted transcript/process access rather than another public child cohort hunt. [INFERENCE]

## What To Do Next

Do next:

1. treat the public child branch as provisionally closed on sign
2. move child work to psychometric refinement only
3. move the main uncertainty frontier to restricted school-facing data and later pipeline nodes

Do not do next:

1. another light public child regression with the same anchors
2. another generic behavior block unless it is clearly school-facing and materially richer than the current teacher pass
