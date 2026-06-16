---
id: 2026-03-07-first-latent-family-prototypes
concept: latent-family-prototypes
repo: research
decision_date: 2026-03-07
recorded_date: 2026-03-07
provenance: contemporaneous
status: accepted
initial_leaning: the surface-family claim was still mostly a synthesis claim and the next likely step was more public observational decomposition
relations:
  - type: depends_on
    target: 2026-03-06-stop-public-regressions-pursue-identification
---

# 2026-03-07: Run first latent family prototypes — move past narrative surface claims

## Context

The project had reached diminishing returns on public pooled regressions. The next claim the repo needed to test was whether the recurring `surface-family` representation survives even a small latent prototype, and whether the late-school `evaluation` family can be treated as a clean latent scalar by sex.

## Alternatives considered

1. **Keep the surface-family claim narrative-only** — low effort, but it would leave the strongest synthesis claim structurally under-tested.
2. **Wait for restricted transcript data first** — higher ceiling, but it would leave the public alpha workstreams idle and slow.
3. **Run small latent prototypes now** — lower-powered than the final target, but enough to test whether the surface-family claim survives contact with formal measurement models.

## Decision

Run the smallest viable latent prototypes now.

Specifically:

1. use `PSID CDS 2002` for the first trait-versus-method prototype because it contains tested `math/reading` and teacher-rated `math/reading` in one public cohort
2. use public `Add Health` for the first joint measurement/prediction-invariance pilot on the school-evaluation family
3. treat poor latent fit as informative, not as a reason to force a cleaner story

## Evidence

1. The first `PSID CDS` prototype shows the two-trait-plus-method model fits materially better than a one-factor or trait-only model, with substantial teacher-method covariance in both sexes. [SOURCE: `research/iq-sex-differences-psid-cds-mtmm-prototype.md`]
2. The first `Add Health` evaluation pilot shows that a simple latent grade-family scalar is a weak measurement surface even before sex-differential prediction becomes the main issue. [SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md`]

## Revisit if

1. a stronger cross-cohort MTMM collapses to weak method structure
2. restricted transcript data produce a much cleaner latent evaluation/transcript model that makes the public prototypes misleading
3. weighted joint multi-group SEM becomes locally feasible and reverses the pilot conclusions

## Supersedes

None.
