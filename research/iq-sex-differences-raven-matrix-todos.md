# IQ Sex Differences - Raven / Matrix Todos

**Date:** 2026-03-11
**Purpose:** concrete next actions for the matrix / Raven-like branch that do **not** depend on immediately landing a new raw dataset.

## Current Verified State

1. The public `Raven` adolescent `OSF d5jph` route is real, but its live public `osfstorage` listing is empty. [SOURCE: https://osf.io/d5jph/]
2. `MaRs-IB` `OSF g96f4` is real, but its live public `osfstorage` listing is also empty. The paper says full datasets are not publicly available and item-level requests should go to the authors. [SOURCE: https://osf.io/g96f4/; https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/]
3. `OMIB` `OSF 4km79` is live and exposes a reusable item bank plus implementation files, but not participant-level rows. [SOURCE: https://osf.io/4km79/]
4. The repo's current narrow target is the matrix / figural / low-knowledge fluid branch, not broad `g`. [SOURCE: `decisions/2026-03-11-recenter-psychometric-target-on-matrix-fluid-branch.md`; `research/iq-sex-differences-matrix-certainty-plan.md`]

## Non-Dataset Work We Can Do Now

- [ ] Freeze the intake schema for any incoming Raven-like dataset:
  - sex field as recorded
  - age
  - participant-by-item responses
  - item order
  - response times
  - timing condition / form assignment
  [SOURCE: `research/iq-sex-differences-marsib-request-draft.md`; `research/iq-sex-differences-matrix-certainty-plan.md`]

- [ ] Run the stronger local `ICAR` matrix branch before waiting on outside data:
  - item-response latent model
  - partial invariance / anchor sensitivity
  - separate matrix reasoning from `3D rotation`
  [SOURCE: `research/iq-sex-differences-raven-open-data.md`; `research/iq-sex-differences-open-matrix-assets.md`]

- [ ] Treat `OMIB` as the default original-study fallback and stop pretending public Raven rows are one scrape away. [SOURCE: `research/iq-sex-differences-open-matrix-assets.md`; `research/iq-sex-differences-matrix-experiment-deployment.md`]

- [ ] Validate the candidate open `APM` lead `osf.io/whsnv`:
  - confirm that participant-level files are actually downloadable
  - confirm whether sex is present
  - confirm whether the task is really Raven `APM`
  [SOURCE: https://osf.io/whsnv/; lead checked 2026-03-11, not yet integrated into repo state]

## Outreach Queue

- [ ] Send the `MaRs-IB` request using the verified contact in `research/iq-sex-differences-raven-outreach-drafts.md`. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/]
- [ ] Resolve the current contact for Emily Savage-McGlynn before sending the `SPM+` request. [SOURCE: doi:10.1016/j.paid.2011.06.013]
- [ ] Resolve the current contact for Patrick Murphy or the corresponding `APM` paper contact before sending the 2023 normative-data request. [SOURCE: doi:10.1111/jnp.12308]
- [ ] If no reply after `10` business days, send one follow-up.
- [ ] If no usable data after the follow-up window, stop burning cycles on email limbo and field the `OMIB` pilot.

## Stop Rule

If the branch still lacks usable new participant rows after:

1. `MaRs-IB` request
2. `SPM+` request
3. `APM` request
4. one follow-up each

then the next default move is:

- local `ICAR` latent upgrade
- `OMIB` timing experiment

not more open-data wishcasting. [INFERENCE]
