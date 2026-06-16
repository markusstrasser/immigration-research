# IQ Sex Differences - Add Health Portal Fill Guide

**Date:** 2026-03-07  
**Purpose:** turn the existing `Add Health` / `AHAA` restricted-use packet into a field-by-field portal workflow the human can actually submit.

This is the operational companion to:

1. `research/iq-sex-differences-addhealth-ahaa-application-scope.md`
2. `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`
3. `research/iq-sex-differences-addhealth-contract-checklist.md`
4. `research/iq-sex-differences-addhealth-attachment-b-draft.md`

---

## Use This Guide In Order

1. open the `CPC Data Portal` project page [SOURCE: https://data.cpc.unc.edu/projects/2/view]
2. add the restricted-use `Core Files` bundle first [SOURCE: https://data.cpc.unc.edu/docs/Information%20Packet%20-%20Getting%20Started.pdf]
3. add the narrow `AHAA` files from the request manifest below [SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`]
4. only then fill the narrative fields and attachments

[INFERENCE] The point is to keep the request narrow enough that the portal, `Attachment B`, IRB, and security plan all describe the same project.

---

## Project Title

Use:

`Transcript-coded school mechanisms, tested achievement surfaces, and later educational outcomes in Add Health`

[SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`]

---

## Short Project Description

Paste this, then trim only if the field is too short:

> This project studies how transcript-coded course structure, transcript-coded academic evaluation, and curriculum exposure relate to later educational outcomes in the same respondents. Public-use analyses already show that school grades and tested achievement do not behave as one interchangeable construct. The requested restricted-use Add Health and AHAA files are limited to the minimum transcript-linked components needed to distinguish transcript-coded course structure, transcript-coded academic evaluation, curriculum exposure, school context, and later educational attainment. The project is not designed to estimate a generic sex difference in intelligence; it is designed to identify which specific school-pipeline channels account for the observed divergence between tested achievement surfaces and school-evaluated performance surfaces.

[SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`]

---

## Why Restricted Data Are Needed

Paste this into the justification field if the portal asks:

> Restricted-use transcript-linked data are required because the public Add Health files do not contain the transcript-coded course sequence, transcript-coded credits and failures, curriculum summaries, transcript timing/linking indicators, or transcript weights needed to separate exposure, evaluation, and curriculum channels. Without the AHAA transcript layer, public grades remain an evaluation surface and cannot adjudicate the live mechanism question.

[SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`]

---

## Exact Files To Request

Request the smallest useful bundle:

### Core

1. `Core Files`

[SOURCE: `research/iq-sex-differences-addhealth-contract-checklist.md`]

### AHAA mandatory

1. linking indicators
2. `edumsov1`
3. `edumsov2`
4. `edu1`
5. `edueng`
6. `edutmsum`
7. `edutssum`
8. `edugrad`
9. `eduocr`
10. `eduwgt`

[SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`]

### AHAA optional only if the portal makes them low-cost

1. `eduhis`
2. `edutmcl`
3. `edutscl`

[SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`]

Do **not** start with every contextual file, every imputed curriculum file, or every subject family. [INFERENCE]

---

## Attachment B Mapping

If the portal or downloaded form wants per-file justification, use this mapping.

| File | Copy-ready why needed |
| --- | --- |
| `Core Files` | needed to merge baseline background, baseline anchors, school-process variables, and later educational outcomes to the transcript sample [SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`] |
| linking indicators | needed to align transcript years to Add Health survey timing and grade placement [SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |
| `edumsov1`, `edumsov2`, `edu1` | needed to recover transcript-coded course structure, transcript-coded GPA, failures, and credit intensity so the project can distinguish transcript exposure from transcript evaluation [SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`; `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |
| `edueng` | needed as an English negative-control subject family to distinguish math/science-specific from broader school-evaluation patterns [SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |
| `edutmsum`, `edutssum` | needed for transcript-coded math/science curriculum exposure rather than course title alone [SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`; `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |
| `edugrad` | needed for transcript-coded graduation / exit outcomes [SOURCE: `research/iq-sex-differences-addhealth-attachment-b-draft.md`] |
| `eduocr` | needed for school-level OCR context so transcript differences are not overread as purely individual [SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |
| `eduwgt` | needed for defensible weighted inference on the transcript sample [SOURCE: `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`] |

---

## IRB Description

Use the narrow mechanism frame, not a broad ideology frame.

Good:

> The project analyzes transcript-coded course structure, transcript-coded academic evaluation, curriculum exposure, and later educational outcomes in Add Health/AHAA to distinguish school-pipeline mechanisms behind divergence between tested achievement and school-evaluated performance.

Bad:

> The project studies sex differences in intelligence.

[INFERENCE]

The first phrasing matches the actual request scope and is much easier to defend against scope creep. [INFERENCE]

---

## Security / User Roster

Before filing:

1. name only the people who actually need direct access [SOURCE: `research/iq-sex-differences-addhealth-contract-checklist.md`]
2. decide the real physical access location(s) [SOURCE: `research/iq-sex-differences-addhealth-contract-checklist.md`]
3. make the security plan match the actual workflow, not a hypothetical future one [INFERENCE]

Do **not** pad the roster “just in case.” Every added user expands the contract burden. [INFERENCE]

---

## Human Portal Checklist

1. confirm the portal still exposes `Core Files` and the exact `AHAA` components above
2. confirm those `AHAA` files sit under the same contract type as the core bundle
3. if the labels differ or `AHAA` appears bundled differently, use `addhealth_contracts@unc.edu` and [support_email_draft.txt](/Users/alien/Projects/research/research/addhealth_ahaa_submission_packet/support_email_draft.txt#L1) before widening the request [SOURCE: https://data.cpc.unc.edu/projects/2/view]
4. download the current portal-generated forms instead of assuming old PDF names are final
5. paste the short project description and the restricted-data justification
6. fill `Attachment B` using the exact file-justification map above
7. attach the IRB that explicitly mentions restricted-use Add Health / AHAA transcript-linked data
8. complete the security plan and the user pledges for the actual access roster
9. use the live portal as the authority on fee status; it currently says no fee is required [SOURCE: https://data.cpc.unc.edu/projects/2/view]

[SOURCE: `research/iq-sex-differences-addhealth-contract-checklist.md`]
