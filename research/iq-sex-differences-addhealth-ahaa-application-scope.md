# IQ Sex Differences - Add Health AHAA Application Scope

**Date:** 2026-03-06  
**Purpose:** turn the live `Add Health` restricted-use frontier into an exact request scope, variable family list, and causal identification plan instead of a vague “get transcripts” placeholder.

For the exact `AHAA` file/component crosswalk behind this request, see `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`.
For the filing checklist and attachment workflow, see `research/iq-sex-differences-addhealth-contract-checklist.md`.

---

## Executive Answer

The next restricted-use move should be a **narrow** `Add Health` request:

1. core restricted-use `Add Health` files needed to align baseline anchors, school process, and later outcomes
2. `AHAA` transcript-linked files that recover math/science course structure, transcript GPA, curriculum exposure, and transcript timing
3. no broad fishing request for every education or school file

[INFERENCE]

That is the highest-value open path because:

1. the public stack already shows a repeated `tested-math` versus `evaluation / GPA / recommendation` wedge, but cannot separate transcript quantity, transcript grades, curriculum exposure, and school context cleanly enough to identify the surviving late-school node [SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-school-wedge-mechanism-triage.md`; `research/iq-sex-differences-school-outcome-decomposition.md`]
2. the official `Add Health` data page and current `Getting Started` materials still point to an active restricted-use application path through the `CPC Data Portal`, unlike the currently paused `NCES` `SAP` route [SOURCE: https://addhealth.cpc.unc.edu/data/; https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf; https://manager.researchdatagov.org/RDG_User_Guide.pdf]
3. the official `AHAA` materials say the transcript component contains detailed academic progress, course-taking, curriculum, contextual, and linking information built from transcript coding that is comparable to `HSTS`, `HS&B`, and `NELS` practice [SOURCE: https://addhealth.cpc.unc.edu/documentation/user-guides/; http://www.laits.utexas.edu/ahaa/users/guide1; http://www.laits.utexas.edu/ahaa/users/guide2; http://www.laits.utexas.edu/ahaa/users/guide7]

### Causal-check

> **Observation:** public `Add Health` replicates the broader school-performance wedge, but it does not expose transcript-coded course structure or transcript-coded curriculum strongly enough to discriminate `evaluation`, `exposure`, and `curriculum` channels. [SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `research/iq-sex-differences-school-outcome-decomposition.md`]
>
> **Null:** public school grades plus public verbal anchors are already enough to capture the late-school mechanism. [INFERENCE]
>
> **Residual after null:** the key late-school split is still structurally unresolved because public grades are an evaluation surface, not a transcript-coded exposure or curriculum surface. [INFERENCE]

- `P(cause)`: `0.82` that a narrow `Add Health` restricted-use / `AHAA` request is the best open next step for reducing uncertainty on the school-pipeline node. [INFERENCE]
- `Top alternative`: `0.12` that another public-use cohort or public-process extension would still materially reduce the same uncertainty faster. [INFERENCE]
- `Falsifier`: a public-use dataset already local that cleanly separates transcript quantity, transcript GPA, curriculum exposure, and later tested anchors without new restricted access. [INFERENCE]
- `Decision impact`: request `AHAA` now, keep the scope narrow, and stop spending cycles pretending public grades can do transcript work. [INFERENCE]

---

## What `AHAA` Adds That The Public Stack Does Not

The official `AHAA` description says it was built from high school transcripts and contains:

1. detailed measures of academic progress and high school curriculum [SOURCE: https://addhealth.cpc.unc.edu/wp-content/uploads/docs/user_guides/DesignPaperWave_I-IV.pdf]
2. academic course indicators by subject area, including performance indicators such as GPA, credits earned, course type, and sequence variables [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]
3. curriculum measures in math and science, including student-level summaries and course-level curriculum indicators derived from textbook-linked coding [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2]
4. transcript-to-survey linking indicators that identify when each student was in high school and how transcript years align to `Add Health` survey timing [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide7]
5. contextual and primary data components, including transcript-derived graduation / exit information and school-context data such as OCR-linked indicators [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide8; http://www.laits.utexas.edu/ahaa/users/guide9]
6. a weighting file for the transcript sample [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide11]

[INFERENCE] The combination matters because the live repo bottleneck is no longer “are school surfaces different from tested surfaces?” We already know they are. The bottleneck is whether the surviving wedge is mostly:

1. transcript quantity / course ladder
2. transcript grades / evaluation
3. curriculum exposure
4. school context
5. something else still living in tested or process surfaces

`AHAA` is the first currently open dataset in the repo’s frontier that can hit all four school-pipeline channels at once.

---

## DAG Fragment For The Request

The request should be justified against this narrower DAG, not against a vague “sex differences in education” story.

```text
[Sex] ------------------------------+
[Family SES / parent education] ----+-----------------------------+
[Race / ethnicity] -----------------+                             |
[Pre-HS achievement / anchors] -----+                             |
[Behavior / engagement] ------------+                             |
                                                                  v
                                                      [Transcript course structure]
                                                                  |
                                                                  +-------> [Curriculum exposure]
                                                                  |
                                                                  +-------> [Transcript GPA / grades]
                                                                  |
                                                                  +-------> [Graduation / exit status]
                                                                  |
                                                                  v
                                                        [Later attainment / STEM path]

[School context] ---------------------------------------> [Transcript course structure]
[School context] ---------------------------------------> [Transcript GPA / grades]
[School context] ---------------------------------------> [Later attainment / STEM path]
```

[INFERENCE] The restricted-use request should therefore target:

1. pre-treatment anchors
2. transcript course structure
3. transcript grade surfaces
4. curriculum exposure
5. school context
6. later outcomes

Not every other educational file in the portal.

---

## Exact Research Questions This Request Should Support

Keep the application framed around a narrow mechanism question.

### Primary questions

1. Do transcript-coded math/science course structure and transcript-coded GPA explain different parts of the female school-performance residual? [INFERENCE]
2. Does curriculum exposure compress the school-knowledge / evaluation wedge more than public grades alone do? [INFERENCE]
3. Conditional on baseline anchors and background, do transcript-coded math/science exposures predict later educational attainment or STEM-oriented outcomes differently by sex? [INFERENCE]

### Secondary questions

1. Is the stable female-leaning school surface mostly an evaluation family (`GPA`, recommendations, recognitions), or does it persist in transcript-coded course and curriculum measures once the transcript layer is restored? [INFERENCE]
2. Do transcript-coded math/science ladders behave more like the public tested-math family or the public evaluation family? [INFERENCE]

### What not to claim in the application

Do **not** claim that this request will “settle sex differences in intelligence.” That is too broad and will read like ideological fishing. [INFERENCE]

Do say that the request is designed to separate:

1. transcript-coded academic exposure
2. transcript-coded academic evaluation
3. baseline tested anchors
4. later educational outcomes

[INFERENCE]

---

## Minimum Request Package

Request the smallest bundle that can identify the school-pipeline DAG above.

### Tier 1: mandatory

1. `Add Health` restricted-use core files needed to align background, early anchors, school process, and later attainment across the same respondents [SOURCE: https://addhealth.cpc.unc.edu/data/]
2. `AHAA` linking indicators [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide7]
3. `AHAA` academic course indicators for math, science, and overall performance surfaces [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]
4. `AHAA` curriculum summary files for math and science [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2]
5. `AHAA` primary/contextual data needed for graduation / exit and school-context controls [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide8; http://www.laits.utexas.edu/ahaa/users/guide9]
6. `AHAA` transcript weights [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide11]

### Tier 2: useful if marginal cost is low

1. `AHAA` English / history / foreign-language course-indicator families as negative-control school surfaces [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]
2. course-level curriculum files if the student-level curriculum summaries look too coarse for the curriculum node [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2]
3. postsecondary follow-up files only if they slot cleanly onto the same IDs and do not materially expand the security burden [INFERENCE]

### Tier 3: defer

1. broad school administrator files not tied to transcript or curriculum identification [INFERENCE]
2. neighborhood or geocode layers not needed for the current DAG [INFERENCE]
3. any bundle added only because it “might be interesting” [INFERENCE]

---

## Variable Families To Ask For Explicitly

Do not ask for “all education variables.” Ask for these families.

### A. Linkage and design

1. respondent IDs needed to merge `AHAA` to core `Add Health`
2. transcript sample / selection indicators
3. transcript weights
4. transcript timing / survey-year alignment indicators

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide7; http://www.laits.utexas.edu/ahaa/users/guide11]

### B. Background and pre-treatment anchors

1. sex
2. race / ethnicity
3. parent education
4. family SES / household background
5. baseline school attachment / behavior where already available in restricted core
6. baseline public tested anchors already used in the repo

[SOURCE: https://addhealth.cpc.unc.edu/data/]
[INFERENCE] These are needed to keep the transcript models from collapsing background, behavior, and transcript exposure into one coefficient.

### C. Transcript course structure

1. math course sequence
2. science course sequence
3. cumulative credits earned
4. semesters attempted
5. honors / AP / IB / remedial course flags
6. course failures / repeats if present

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]

### D. Transcript evaluation surfaces

1. transcript GPA in math
2. transcript GPA in science
3. overall GPA or overall academic indicators from the transcript component

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]

### E. Curriculum exposure

1. student-level math curriculum summaries
2. student-level science curriculum summaries
3. course-level curriculum indicators only if student-level summaries prove too coarse

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2]

### F. School context

1. OCR or equivalent school-context indicators included in the transcript component
2. graduation / exit / completion indicators

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide8; http://www.laits.utexas.edu/ahaa/users/guide9]

### G. Later outcomes

1. later educational attainment
2. field / major / college progression if available in the restricted core
3. later labor-market outcomes only if they are already in the contracted core and do not widen the request materially

[SOURCE: https://addhealth.cpc.unc.edu/data/]
[INFERENCE]

---

## Why This Request Should Stay Narrow

The repo already has enough public data to know that:

1. evaluation surfaces are repeatedly more female-leaning than tested-math surfaces [SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`]
2. public `Add Health` adds a broad school-performance replication, not a transcript-test adjudication layer [SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`]
3. the main unresolved school-pipeline question is not “do girls do better in school?” but “which transcript-coded channel carries the residual?” [INFERENCE]

That means a bloated request is technically worse than a narrow one.

The narrow request is easier to justify because it is tied to one causal fork:

1. `transcript course structure`
2. `transcript evaluation`
3. `curriculum exposure`
4. `school context`

[INFERENCE]

---

## Copy-Ready Project Description

Use language close to this:

> This project studies how different school-performance surfaces map onto later educational outcomes. Existing public-use analyses repeatedly show that standardized tested-math surfaces, school grades, and other school-linked performance indicators do not behave as one interchangeable construct. The restricted-use request is limited to the transcript-linked `AHAA` components and the minimum core `Add Health` files needed to distinguish transcript-coded course structure, transcript-coded academic evaluation, curriculum exposure, and later attainment in the same respondents. The goal is not to estimate a generic “sex difference in intelligence,” but to determine which specific school-pipeline channels account for the divergence between tested achievement surfaces and school-evaluated performance surfaces. [INFERENCE]

Shorter version:

> We request the minimum `Add Health` restricted-use and `AHAA` transcript components needed to separate transcript-coded course structure, transcript-coded academic evaluation, curriculum exposure, and later attainment. Public-use data already show that grades and standardized achievement are not interchangeable. The restricted-use transcript layer is needed to identify which transcript-coded school mechanisms carry that divergence. [INFERENCE]

---

## Analysis Plan Once Access Is Granted

### Step 1: intake and validation

1. verify IDs and transcript weights
2. reproduce official transcript sample counts where possible
3. build one narrow analysis panel before any outcome modeling

[INFERENCE]

### Step 2: descriptive transcript geometry

1. weighted sex gaps on transcript math/science GPA
2. weighted sex gaps on transcript course ladder and credits
3. weighted sex gaps on curriculum summaries
4. negative-control surfaces from English/history if available

[INFERENCE]

### Step 3: DAG-valid modeling

Primary total-effect setup:

```text
Sex -> transcript course structure / transcript GPA / curriculum -> later attainment
```

Adjustment set:

1. background
2. baseline anchors
3. pre-transcript school-process variables if genuinely pre-treatment

[INFERENCE]

Do **not** adjust the total-effect model for descendants of the transcript mediators when the estimand is total effect. [INFERENCE]

### Step 4: mediator-style descriptive decomposition

Report attenuation sequentially:

1. background-only
2. + transcript course structure
3. + transcript GPA
4. + curriculum exposure
5. + school context

[INFERENCE]

Label this as descriptive channel decomposition unless the mediator assumptions are separately justified. [SOURCE: `research/iq-sex-differences-mediator-design.md`]

### Step 5: robustness

For any causal OLS interpreted substantively:

1. run `causal-dag` discipline first
2. run `causal-robustness` / `sensemakr` after estimation

[SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-analysis-protocol.md`]

---

## Human Application Steps

1. go to the `Add Health` data page and open the `CPC Data Portal` application flow [SOURCE: https://addhealth.cpc.unc.edu/data/]
2. use the current getting-started packet for the live portal and checkout path [SOURCE: https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf]
3. request:
   - restricted core files needed for baseline/background/outcomes
   - `AHAA` linking indicators
   - `AHAA` academic course indicators
   - `AHAA` curriculum summaries
   - `AHAA` primary/contextual data
   - `AHAA` weights
4. keep the request framed around transcript-coded school-mechanism identification, not broad ideology [INFERENCE]
5. prepare the required data-security materials using the current UNC restricted-use security guidance [SOURCE: https://data.cpc.unc.edu/docs/Security_Information_for_Remote_Add_Health_Access.pdf; https://data.cpc.unc.edu/docs/Security_Plans_for_Restricted-Use_Data_Information.pdf]

### Important access note

The current UNC security guidance says that new restricted-use contracts now access data through the `Secure Research Workspace` rather than sending encrypted local copies directly to users. [SOURCE: https://data.cpc.unc.edu/docs/Security_Information_for_Remote_Add_Health_Access.pdf]

[INFERENCE] That means the application should be designed around a realistic remote-workspace workflow, not around assumptions from older local-copy contracts.

---

## What Would Make This The Wrong Next Step

This would stop being the right move if:

1. the `Add Health` portal no longer exposes `AHAA` or the needed transcript bundles [UNVERIFIED until application cart is checked]
2. the contract burden is so broad that it delays the project more than it informs it [INFERENCE]
3. a better open transcript/process dataset appears before the request is submitted [INFERENCE]

Until then, this is the best open restricted-use path.
