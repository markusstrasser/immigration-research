# IQ Sex Differences - Add Health / AHAA Literature Gap

**Date:** 2026-03-07  
**Purpose:** determine whether the planned restricted-use `Add Health / AHAA` branch is likely to generate genuinely new information or mostly replicate existing `AHAA` work.

This is a narrow literature-gap memo, not a full review of all `Add Health` education papers.

---

## Executive answer

The `AHAA` branch still looks worth doing.

Not because `AHAA` has never been used for gender and schooling. It has.

It still looks distinct because I did **not** find a paper that combines all of the following in one design:

1. transcript-coded course structure
2. transcript-coded GPA / evaluation
3. transcript-coded curriculum exposure
4. baseline tested anchors from core `Add Health`
5. later attainment outcomes
6. explicit comparison of `tested achievement` versus `evaluation / transcript` surfaces

[INFERENCE]

That means the likely contribution is still not “new transcript fact about girls and boys.” It is a better decomposition of the school-pipeline wedge inside a transcript-linked national cohort.

---

## What clearly already exists

### 1. Gender and advanced course-taking in `AHAA`

This is already in the literature.

- Riegle-Crumb used `AHAA` transcript data to study math course sequences and academic performance by race/ethnicity and gender:  
  [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC2889488/]

This means:

- `AHAA` is not novel as a transcript source for gendered course-taking
- a claim like “boys and girls differ in math course sequences” is not new

### 2. Gender and transition-to-high-school GPA / transcript performance

This also already exists.

- Sutton et al. used `AHAA` to study academic performance at the transition to high school across race/ethnicity and gender:  
  [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC5975961/]

This means:

- the repo should not pretend that transcript-linked gender differences in GPA are a new discovery

### 3. Gender typicality and transcript GPA

Also already exists.

- Yavorsky and Buchmann use `Add Health` plus transcript data and explicitly discuss overall GPA, math GPA, and science GPA:  
  [SOURCE: https://sociologicalscience.com/articles-v6-25-661/]
  [SOURCE: https://sociologicalscience.com/download/vol-6/december/SocSci_v6_661to683.pdf]

This means:

- the repo should not pitch “girls have higher transcript GPA” as if that were new

### 4. Official `AHAA` data design is explicitly about academic trajectories

The `AHAA` site itself says the study was built to add:

- detailed measures of academic progress
- high school curriculum
- transcript coding and curriculum indicators

[SOURCE: https://www.laits.utexas.edu/ahaa/]
[SOURCE: https://www.laits.utexas.edu/ahaa/descrip]
[SOURCE: https://www.laits.utexas.edu/ahaa/descrip/transcriptcoding]

So:

- using `AHAA` for course structure or curriculum is normal and expected
- novelty has to come from the **design and decomposition**, not from merely requesting the files

---

## What I did not find

I did **not** find a paper that cleanly does this specific decomposition:

```text
baseline tested anchors
    +
transcript-coded course structure
    +
transcript-coded GPA / failures / credits
    +
curriculum summaries
    +
school context
    ->
later attainment
```

with the explicit goal of separating:

1. `evaluation`
2. `school-knowledge`
3. `track / quantity`
4. `curriculum exposure`
5. `tested achievement`

[INFERENCE]

I also did **not** find a paper that frames the `AHAA` transcript layer as the adjudicator of the repo’s live wedge:

> do transcript-coded exposure and transcript-coded evaluation explain different parts of the divergence between tested achievement surfaces and school-evaluated performance surfaces?

[INFERENCE]

That is the real reason the branch still looks valuable.

---

## What would be weak or redundant

These would not be strong uses of `AHAA`:

1. another paper that only says girls have higher GPA
2. another paper that only says boys and girls sort differently into advanced math
3. another paper that only says gendered course-taking predicts later outcomes

Why:

- those are already close to existing `AHAA` usage
- they would not justify the current restricted-data burden

---

## What could still be genuinely useful

The `AHAA` branch is worth filing if it is kept narrow and pitched correctly.

Best-use framing:

1. distinguish transcript-coded exposure from transcript-coded evaluation
2. distinguish transcript-coded structure from curriculum content
3. connect both to baseline tested anchors and later attainment
4. ask which school-pipeline channels explain different parts of the wedge

[INFERENCE]

That is much stronger than:

> “use `AHAA` to study gender differences in achievement”

---

## Recommended claim discipline

### Safe claims

1. `AHAA` has already been used for gendered course-taking and GPA work.  
   [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC2889488/; https://pmc.ncbi.nlm.nih.gov/articles/PMC5975961/; https://sociologicalscience.com/articles-v6-25-661/]

2. The branch still looks useful because the repo’s target decomposition is more integrated than the existing `AHAA` studies I found.  
   [INFERENCE]

3. The likely value of `AHAA` is not discovering a new raw gender gap, but identifying whether transcript-coded exposure, transcript-coded evaluation, and curriculum exposure load onto different parts of the existing wedge.  
   [INFERENCE]

### Unsafe claims

1. “No one has used `AHAA` for gender and academics.”
2. “`AHAA` will definitely produce a novel finding.”
3. “The `AHAA` branch will settle sex differences in intelligence.”

Those are not supported.

---

## Causal-check

> **Observation:** existing `AHAA` work covers gendered course-taking and transcript performance, but I did not find the repo’s specific transcript/test/curriculum/attainment decomposition.
>
> **Null:** the restricted `AHAA` branch would mostly replicate what is already known.
>
> **Residual after null:** there is still room for a more integrated school-pipeline design that the current literature does not obviously exhaust.

- `P(cause) = 0.68` that the restricted `AHAA` branch can still create new information if it is framed as a decomposition problem, not a generic gender-gap project. [INFERENCE]
- `Top alternative = 0.22` that the branch mainly yields a cleaner replication of already-known transcript/GPA/course-taking facts. [INFERENCE]
- `Falsifier:` a paper already doing transcript-coded course structure + transcript GPA + curriculum + baseline anchors + later attainment in one `AHAA` design. [INFERENCE]

---

## Search note

Searches used:

1. `Add Health AHAA transcript GPA test score sex differences`
2. `Add Health AHAA transcript course taking GPA gender`
3. `site:addhealth.cpc.unc.edu AHAA transcript GPA gender math course paper`

[INFERENCE] This is not an exhaustive systematic review. It is enough to discipline the novelty claim before filing the restricted request.
