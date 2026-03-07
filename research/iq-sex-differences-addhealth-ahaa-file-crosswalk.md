# IQ Sex Differences - Add Health AHAA File Crosswalk

**Date:** 2026-03-06  
**Purpose:** map the current causal DAG and restricted-use application scope onto the exact `AHAA` component families and file names described in the official users guides.

This file is the companion to `research/iq-sex-differences-addhealth-ahaa-application-scope.md`.

---

## Why This File Exists

The application scope memo says what the project needs conceptually.

This file says what that means in the actual `AHAA` vocabulary:

1. which component family
2. which file names the official users guides expose
3. which DAG node each file attacks
4. what to request now versus later

[INFERENCE]

---

## Core Crosswalk

| Priority | DAG node / family | `AHAA` component | Official file names / examples | Why request it now | Source |
| --- | --- | --- | --- | --- | --- |
| `must` | transcript timing / linkage | Linking indicators | transcript-to-survey alignment indicators documented in the Linking component | needed to align transcript years to survey timing and prevent bad age/grade matching | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide7; https://www.laits.utexas.edu/ahaa/docs/Lnkng_2007.pdf] |
| `must` | transcript course structure: math / science / overall | Academic Courses | `edumsov1`, `edumsov2`, plus `edu1` for sequence, GPA, and failure variables | core exposure and evaluation family for the late-school wedge | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1; https://www.laits.utexas.edu/ahaa/docs/Crses_MthScnceOvrll_2007.pdf] |
| `must` | transcript course structure: English negative control | Academic Courses | `edueng` | lets the repo test whether transcript-coded evaluation/exposure patterns are math-specific or part of a broader school-evaluation family | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1] |
| `should` | transcript course structure: history / social science negative control | Academic Courses | `eduhis` | useful negative-control school surface if low marginal request cost | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1] |
| `defer` | transcript course structure: foreign language | Academic Courses | `eduflng1`, `eduflng2` | lower priority unless the contract structure makes them effectively free | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1] |
| `defer` | transcript course structure: PE | Academic Courses | `edupe1`, `edupe2` | not needed for the live math/science wedge unless cheap as a broad non-academic negative control | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1] |
| `must` | curriculum exposure: student-level math / science | Curriculum | `edutmsum`, `edutssum` | the cleanest low-burden curriculum node for distinguishing course title from curriculum content | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2] |
| `should` | curriculum exposure: course-level math / science | Curriculum | `edutmcl`, `edutscl` | useful if student-level summaries are too coarse for identifying content/performance expectations | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2] |
| `defer` | curriculum exposure: imputed course-level | Curriculum | `edutmcli`, `edutscli` | request only if missing textbook linkage becomes a binding data-loss problem | [SOURCE: https://www.laits.utexas.edu/ahaa/docs/Crrclm_IMMthScnce_2008.pdf] |
| `must` | graduation / exit | Primary component | `edugrad` with transcript-derived graduation / exit indicators | needed for transcript-coded completion / exit outcomes and school-pipeline closure | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide8; https://www.laits.utexas.edu/ahaa/docs/Archvd_Grdtn_2005.pdf] |
| `should` | school context | Contextual component | `eduocr` | strongest school-context addition for the current DAG because it captures school-level OCR structure | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide9; https://www.laits.utexas.edu/ahaa/users/contextualdata] |
| `defer` | school context | Contextual component | `educcd1`, `educcd2`, `edupss`, `educen`, `educx90` | useful if OCR is not enough, but these widen the request faster than the main node requires | [SOURCE: https://www.laits.utexas.edu/ahaa/users/contextualdata] |
| `must` | transcript sample design | Weights | `eduwgt` | required for any defensible transcript-sample inference | [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide11; https://www.laits.utexas.edu/ahaa/docs/Weights_2005_Riegle-Crumb.pdf] |

---

## What Each Requested Family Buys Causally

### 1. `edumsov1` / `edumsov2` / `edu1`

These are the core transcript files for the current question because the official guides say they cover:

1. course sequence
2. course grades
3. course failures
4. semesters attempted
5. credits earned

[SOURCE: http://www.laits.utexas.edu/ahaa/users/guide1]

[INFERENCE] Together they let the repo separate:

1. `transcript course ladder`
2. `transcript academic performance`
3. `transcript quantity / intensity`

That is exactly the live school-pipeline fork.

### 2. `edutmsum` / `edutssum`

The official curriculum guide says these are student-level summary indicators of math and science curriculum exposure, derived from textbook-linked coding grounded in `TIMSS` curriculum frameworks. [SOURCE: http://www.laits.utexas.edu/ahaa/users/guide2]

[INFERENCE] These are the cleanest “next-level” files because they move beyond course titles and toward actual content exposure without requiring the heaviest course-level request.

### 3. `edugrad`

The official graduation guide says these indicators come directly from transcripts or related materials and capture graduation / exit status and timing. [SOURCE: https://www.laits.utexas.edu/ahaa/docs/Archvd_Grdtn_2005.pdf]

[INFERENCE] This closes the school-pipeline branch with transcript-coded outcomes instead of relying only on later survey attainment.

### 4. `eduocr`

The contextual guide says `eduocr` contains school-level OCR indicators attached to high schools attended by `AHAA` students. [SOURCE: https://www.laits.utexas.edu/ahaa/users/contextualdata]

[INFERENCE] This is the least bloated way to add school context to the current transcript DAG.

### 5. `eduwgt`

The official weights materials say the transcript sample has dedicated weights and that nonresponse adjustment was part of the weight construction. [SOURCE: https://www.laits.utexas.edu/ahaa/docs/Weights_2005_Riegle-Crumb.pdf]

[INFERENCE] Without `eduwgt`, the transcript branch risks becoming another unweighted convenience panel.

---

## Recommended Request String

If the portal or `Attachment B` wants concrete file names, ask for the following first:

1. `AHAA` linking indicators
2. `edumsov1`
3. `edumsov2`
4. `edu1`
5. `edueng`
6. `edutmsum`
7. `edutssum`
8. `edugrad`
9. `eduocr`
10. `eduwgt`

[INFERENCE]

Optional second wave if the contract burden is modest:

1. `eduhis`
2. `edutmcl`
3. `edutscl`

[INFERENCE]

Do **not** start with every contextual file, every negative-control subject, and every imputed curriculum file. That is how the request becomes bloated before it teaches anything.

---

## Attachment B Logic

For `Attachment B` or any portal justification field, the clean mapping is:

1. `edumsov1` / `edumsov2` / `edu1`
   - justification: transcript-coded course structure, GPA, failure, and credit intensity are needed to distinguish transcript exposure from transcript evaluation [INFERENCE]
2. `edutmsum` / `edutssum`
   - justification: curriculum summaries are needed to test whether the remaining wedge tracks actual content exposure rather than course title alone [INFERENCE]
3. `edugrad`
   - justification: transcript-coded exit / graduation outcomes are needed to connect the transcript pipeline to completion outcomes [INFERENCE]
4. `eduocr`
   - justification: school-level OCR context is needed to avoid overreading transcript differences as purely individual [INFERENCE]
5. `eduwgt`
   - justification: transcript-sample weighting is required for valid inference [INFERENCE]

---

## What To Check In The Portal

Before submitting the request, verify three things manually:

1. the `AHAA` component names and file names exposed in the `CPC Data Portal` still match the current users guides [UNVERIFIED until cart is inspected]
2. the transcript files above are requestable under the same contract type as the standard restricted-use core [UNVERIFIED until cart is inspected]
3. no narrower pre-bundled transcript package already contains these files more cleanly than selecting them one by one [UNVERIFIED until cart is inspected]

If the portal exposes a bundled transcript package that already contains the mandatory files above, use the bundle instead of itemizing everything.

