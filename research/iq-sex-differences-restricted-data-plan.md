# IQ Sex Differences - Restricted Data Plan

**Date:** 2026-03-06  
**Purpose:** turn the remaining restricted-data frontier into an operational decision document rather than a vague “maybe we need richer data” placeholder.

## Executive Answer

The next restricted-data step is **not** “apply everywhere.”

The current live path splits in two:

1. `Add Health` restricted-use / `AHAA` is the best **open** restricted path.
2. `NCES` restricted-use targets (`HSTS`, `NAEP` process) are currently the best **blocked** paths because the official `ResearchDataGov` guide says new `NCES` `SAP` applications are paused until further notice.

[SOURCE: https://addhealth.cpc.unc.edu/data/; https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf; https://manager.researchdatagov.org/RDG_User_Guide.pdf]

That changes the priority order:

1. pursue `Add Health` restricted-use / transcript access now
2. prepare, but do not actively file, `NCES` restricted-use materials until the pause lifts
3. do not spend more cycles pretending the current public-use stack will identify mediation cleanly

[INFERENCE]

## Why This File Exists

The public-use branch is now close to saturation on generic regression work.

The remaining uncertainty is concentrated in:

1. transcript quantity versus transcript grade versus tested-math surfaces
2. real process-log evidence on score generation
3. mediator identification rather than descendant-heavy attenuation tables

[SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-school-outcome-interactions.md`]

So the right question is no longer “what else can we download?” It is:

1. which restricted dataset is actually open now
2. which one would falsify the most important remaining node
3. what human steps are required

[INFERENCE]

## Current Causal Bottleneck

> **Observation:** the public stack now repeatedly separates tested-math surfaces from evaluation / GPA / recommendation surfaces, but cannot cleanly identify whether the surviving late-school wedge is mainly transcript structure, institutional evaluation, behavior/compliance, or score-generation artifacts. [SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-school-wedge-mechanism-triage.md`; `research/iq-sex-differences-school-outcome-decomposition.md`]
>
> **Null:** if the public stack were already sufficient, the remaining disagreement would mostly be numerical rather than structural. [INFERENCE]
>
> **Residual after null:** it is structural. The best remaining discriminators require transcript microdata or process logs that the public stack does not expose. [INFERENCE]

- `P(cause)`: `0.84` that the next real progress now depends more on access state than on another public-use slice. [INFERENCE]
- `Top alternative`: `0.12` that a yet-unrun public cohort still contains enough untapped transcript/process leverage to change the causal ranking materially. [INFERENCE]
- `Falsifier`: a public-use cohort or analysis already local that materially compresses the evaluation-versus-tested wedge without restricted transcript/process fields. [INFERENCE]
- `Decision impact`: do the access work on the one live restricted path and stop treating all remaining frontier items as equally actionable. [INFERENCE]

## Ranked Targets

## 1. `Add Health` Restricted-Use / `AHAA`

### Why it is first

This is the best currently **open** path because:

1. the official `Add Health` data page routes restricted-use acquisition through the `CPC Data Portal`
2. the official getting-started packet gives a live application path
3. the official design paper explicitly describes `AHAA` as transcript-based and says it collected detailed academic progress, course taking, and curriculum

[SOURCE: https://addhealth.cpc.unc.edu/data/; https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf; https://addhealth.cpc.unc.edu/wp-content/uploads/docs/user_guides/DesignPaperWave_I-IV.pdf]

### What it can falsify

1. whether the `Add Health` public school-performance wedge is mostly grade-only or also present in transcript-coded high-school curriculum
2. whether transcript math/science GPA, course-taking intensity, and curricular exposure behave more like `HSLS` / `NELS` evaluation surfaces or more like tested surfaces
3. whether later attainment or STEM-pathway differences are better predicted by transcript-coded course structure than by public grades alone

[INFERENCE]

### Why it matters causally

The repo already knows public `Add Health` is useful as a broad school-performance replication, but not as a transcript/test adjudication dataset. Restricted transcript access is the cleanest way to upgrade it from “broad school wedge” to “transcript-coded mechanism dataset.” [SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `research/iq-sex-differences-addhealth-public-pair-note.md`]

### Official application path

1. start at the data page: `https://addhealth.cpc.unc.edu/data/`
2. use the `CPC Data Portal`
3. the getting-started packet says to begin at `https://data.cpc.unc.edu/projects/2/view`, add bundles, then proceed through checkout and the follow-up contract steps

[SOURCE: https://addhealth.cpc.unc.edu/data/; https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf]

### Security / operational burden

`Add Health` restricted-use requires a real data-security plan. The current official materials include:

- remote-access security instructions
- secure workstation / stand-alone desktop rules

[SOURCE: https://data.cpc.unc.edu/docs/Security_Information_for_Remote_Add_Health_Access.pdf; https://data.cpc.unc.edu/docs/Security_Plans_for_Restricted-Use_Data_Information.pdf]

### What to request

Request the smallest bundle that can answer the current node:

1. `AHAA` high school transcripts
2. transcript-coded GPA and course-taking surfaces
3. transcript-coded math/science ladder or Carnegie-type course exposure if available
4. any linked school contextual fields needed to avoid overreading transcript differences as pure individual ability

[INFERENCE]

### Manual steps

1. create the `CPC Data Portal` application
2. request core files plus the transcript / academic-achievement bundle
3. prepare the security plan for the actual machine/location that would hold the data
4. keep the request narrow and explicitly tied to transcript/test / school-wedge adjudication

[INFERENCE]

## 2. `HSTS` Transcript Microdata

### Why it is still high value

`HSTS` remains the best transcript/test linkage target in the NCES world.

The transcript page says transcript data across `HS&B`, `NELS`, `ELS`, `HSLS`, and `NAEP HSTS` are available only as restricted-use data because of sensitivity. [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]

The `HSTS` pages confirm the study and design structure are live. [SOURCE: https://nces.ed.gov/nationsreportcard/hsts/; https://nces.ed.gov/nationsreportcard/hsts/design.aspx]

### What it can falsify

1. whether transcript quantity and transcript grade are really separate families once the full transcript microdata are used
2. whether the female-leaning evaluation family is just a public-use suppression artifact
3. whether transcript-coded advanced curriculum explains more of the later male tested-math surfaces than current public cohorts imply

[INFERENCE]

### Why it is not first

Because the official new-application path is effectively blocked right now.

The `ResearchDataGov.org User Guide` says:

> `NCES is currently not accepting new applications for access to data through the Standard Application Process. Review of applications for access to data from NCES is also paused until further notice.`

[SOURCE: https://manager.researchdatagov.org/RDG_User_Guide.pdf]

At the same time, NCES pages still route restricted-use acquisition through the licensing / SAP path. [SOURCE: https://nces.ed.gov/statprog/instruct.asp; https://nces.ed.gov/surveys/slsp/transcripts.asp]

So the correct operational read is:

1. `HSTS` is still scientifically high value
2. it is currently a preparation target, not an actively fileable one

[INFERENCE]

## 3. `NAEP` Process Data

### Why it matters

This is still the best U.S. process-log target for the `MeasurementSurface` node.

The official `NAEP Process Data` page says the files include cognitive responses, process files, and survey data, and that researchers must apply for restricted-use access. [SOURCE: https://www.nationsreportcard.gov/process_data/]

### What it can falsify

1. whether navigation / timing / rapid-guess / item-visit patterns create a meaningful part of the school-age sex-gap geometry
2. whether the `PISA` / `TIMSS` residual family ordering generalizes to U.S. process-log data
3. whether the current public `PISA` / `TIMSS` proxy passes are materially overstating or understating response-process effects

[INFERENCE]

### Why it is blocked

Same reason as `HSTS`: `NCES` new `SAP` applications are currently paused according to the `ResearchDataGov` user guide. [SOURCE: https://manager.researchdatagov.org/RDG_User_Guide.pdf]

## 4. `Project Talent`

This is still useful for upper-tail / sibling / twin structure, but it is not the next best move for the current bottleneck.

The current repo bottleneck is the school/transcript/process node, not upper-tail metaphysics. [INFERENCE]

AIR’s researcher page also says several federally funded repositories and active projects are on hold. [SOURCE: https://www.air.org/project-talent/researchers]

## Decision Table

| Dataset | Scientific value now | Access state now | Best use | Recommendation |
| --- | --- | --- | --- | --- |
| `Add Health` restricted / `AHAA` | high | open | transcript-coded school-wedge adjudication | do now |
| `HSTS` transcript microdata | very high | administratively paused via NCES SAP | transcript quantity vs grade vs tested math | prepare, do not actively file |
| `NAEP` process data | very high | administratively paused via NCES SAP | U.S. process-log test-surface adjudication | prepare, do not actively file |
| `Project Talent` | medium-high | friction / hold | upper-tail / sibling extension | defer |

## Manual Work For The Human

### Track A - do now

1. open `https://addhealth.cpc.unc.edu/data/`
2. start the `CPC Data Portal` application
3. request the smallest transcript / academic-achievement bundle that covers `AHAA`
4. prepare the required security-plan paperwork
5. save copies of the request scope and the exact bundle names in the repo once submitted

[SOURCE: https://addhealth.cpc.unc.edu/data/; https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf]

### Track B - prepare, do not file yet

1. draft the `HSTS` and `NAEP` project descriptions
2. draft the data-security language
3. monitor the `NCES` / `ResearchDataGov` pause status
4. do **not** spend time building a full NCES application package until the pause is lifted

[SOURCE: https://manager.researchdatagov.org/RDG_User_Guide.pdf; https://nces.ed.gov/statprog/instruct.asp]

## Exact Research Questions To Name In The Applications

Keep the requests narrow.

### `Add Health` restricted-use / `AHAA`

1. do transcript-coded math/science course-taking and transcript GPA compress the female school-evaluation residual more than public grade surfaces do?
2. does transcript-coded curriculum exposure explain the split between public school-performance surfaces and later attainment?
3. does transcript-coded course structure predict later attainment or STEM-oriented outcomes differently by sex, conditional on baseline public anchors?

[INFERENCE]

### `HSTS`

1. after full transcript detail is restored, do transcript quantity and transcript grade still separate cleanly from tested math?
2. is the female-leaning evaluation family still the most stable school-linked family once public suppression is removed?

[INFERENCE]

### `NAEP` process

1. how much of the school-age item-family geometry survives once process logs are used directly?
2. do rapid-guessing, dwell time, and revisit patterns differ enough by sex to change the interpretation of broad school-math gaps?

[INFERENCE]

## Bottom Line

Do not flatten the restricted-data frontier into one generic “apply for restricted data” step.

The right operational split is:

1. `Add Health` restricted-use / `AHAA` is live now and should be pursued first.
2. `HSTS` and `NAEP` remain scientifically first-rate, but administratively paused under the current `NCES` / `ResearchDataGov` path.

[INFERENCE]
