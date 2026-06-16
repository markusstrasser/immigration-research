---
id: 2026-03-07-lightweight-eiv-is-not-the-alpha
concept: measurement-error-frontier
repo: research
decision_date: 2026-03-07
recorded_date: 2026-03-07
provenance: contemporaneous
status: accepted
initial_leaning: lightweight public measurement-error correction was the best immediate local methods upgrade
relations:
  - type: branches_from
    target: 2026-03-07-first-latent-family-prototypes
---

# 2026-03-07: Lightweight public EIV is not the alpha

## Context

The methods-frontier review correctly said plain `do`-calculus was not the main missing ingredient and that measurement-aware latent modeling was the right direction. The open question was whether a lightweight public attenuation pass on the existing `HSLS` / `Add Health` prototypes would materially change the surface-family story, or whether the real remaining gain required heavier weighted joint latent modeling and restricted transcript-theta data.

## Alternatives considered

1. **Keep treating simple public EIV as the best immediate move** — cheap and local, but only valuable if the current public families are noisy enough for measurement correction to move the geometry materially.
2. **Run the bounded pilot and decide empirically** — costs a small amount of implementation time, but directly tests whether the methods-frontier claim pays rent on current data.
3. **Skip straight to weighted joint latent modeling** — likely the real frontier, but at higher implementation cost and without knowing whether the simpler correction already captures most of the gain.

## Decision

Run the bounded public pilot, then downgrade lightweight public `EIV` as a major uncertainty reducer if the coefficient geometry barely moves.

That is now the accepted decision. On the current public branch, reliabilities are already fairly high and loading-weighted latent proxies barely move the `HSLS` / `Add Health` prediction geometry. The simple divide-by-reliability correction overshoots the factor-proxy result and should not become the canonical estimator.

So the real remaining gain is:

1. weighted joint latent modeling
2. restricted transcript-theta work
3. richer process-DIF reduction

## Evidence

1. `research/iq-sex-differences-measurement-error-pilot.md`
2. `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_reliability.tsv`
3. `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`
4. `research/iq-sex-differences-causal-methods-frontier.md`

## Revisit if

Reopen this decision if:

1. a weighted joint latent model produces materially different geometry from both composites and the current factor-proxy pilot
2. restricted transcript-theta data show much larger attenuation than the public grade/test families
3. a stronger local measurement-error method produces consistent changes large enough to alter the current surface-family conclusions

## Supersedes

No direct supersession. This refines the methods-frontier direction rather than reversing it.
