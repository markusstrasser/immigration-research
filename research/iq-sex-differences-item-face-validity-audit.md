# IQ Sex Differences - Public Item Face-Validity Audit

**Date:** 2026-03-05
**Purpose:** inspect released public test items directly, solve a small set of them, and check whether there is any obvious face-valid sex bias that is more concrete than the current content-family results.

This is a **mechanism probe**, not a DIF analysis. It can show what the item burden visibly is. It cannot prove psychometric unfairness by itself. [INFERENCE]

---

## Scope

Questions this memo answers:

1. do released items show obvious overt sex-coded or stereotype-driven bias on their face?
2. do released items visibly differ in burden in ways that match the repo's content-family findings?
3. does direct inspection make the current causal tree more or less plausible?

Questions this memo does **not** answer:

1. whether the operational `CAT-ASVAB` bank is biased
2. whether any item shows statistical DIF by sex
3. whether a content family is unfair rather than simply measuring a different construct mix

---

## Sources Inspected

Primary public item sources:

1. OECD released mathematics items PDF:
   - <https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/pisa/pisa-test/PISA%202012%20items%20for%20release_ENGLISH.pdf/_jcr_content/renditions/original./PISA%202012%20items%20for%20release_ENGLISH.pdf>
2. Official ASVAB sample-question hub:
   - <https://www.officialasvab.com/recruiters/sample-questions/>
3. Official ASVAB Mathematics Knowledge sample page:
   - <https://www.officialasvab.com/mathematics-knowledge-mk/>
4. Official ASVAB Arithmetic Reasoning sample page:
   - <https://www.officialasvab.com/arithmetic-reasoning-ar/>
5. Official ASVAB Assembling Objects sample image:
   - <https://www.officialasvab.com/wp-content/uploads/2024/03/ao-2.jpg>

Local project context used for comparison:

1. `research/iq-sex-differences-pisa2018-item-split.md`
2. `research/iq-sex-differences-pisa2018-framework-proxy.md`
3. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_unit_summary.tsv`

Important constraint:

- the official ASVAB program explicitly says actual operational test questions are not publicly released, so this memo can inspect only official sample questions for `ASVAB`, not the real `CAT-ASVAB` bank:
  - <https://www.officialasvab.com/applicants/asvab-test-preparation-disclaimer/>

---

## Items Directly Inspected

### PISA released items

The released `PISA 2012` PDF includes full public item stems, figures, and scoring intent. I directly inspected at least these items:

1. `Apartment Purchase`
2. `Oil Spill`
3. `Faulty Players`
4. `Charts`
5. `Drip Rate`
6. `Penguins`
7. `Power of the Wind`

### ASVAB public sample items

I directly inspected:

1. `Assembling Objects` sample image
2. `Mathematics Knowledge` sample geometry / volume image

---

## Spot-Check Solves

These were solved directly from the public items, not inferred from titles alone:

1. `Charts` question 1:
   - answer `500`
   - burden: basic bar-chart reading with low spatial burden and moderate legend-reading burden
2. `Faulty Players` question 2:
   - tester's claim is wrong because average faulty counts are `100` video versus `180` audio
   - burden: table reading plus percentage-to-count conversion
3. `Penguins` question 1:
   - answer `41%`
   - burden: percent increase on two concrete values in a lightly verbal biological context
4. `Drip Rate` question 1:
   - if `n` doubles while `d` and `v` stay fixed, `D` halves
   - burden: variable reasoning from a formula, not raw arithmetic
5. `ASVAB` `MK` rectangular prism sample:
   - visible task burden is standard `volume = 8 * 3 * 4 = 96`
   - burden: 3D diagram parsing plus school geometry recall

These spot-checks are enough to confirm that the inspected items are genuinely mathematical and that their visible burden matches the official item-intent descriptions in the OECD scoring notes. [SOURCE: OECD released items PDF]

---

## Visual Findings

### 1. I do **not** see obvious overt sex-coded bias in the inspected public items

I do **not** see anything like:

1. overt misogynistic or misandrist wording
2. obvious stereotype bait where one sex would plainly be advantaged by the text alone
3. hidden scoring tricks that reward social framing more than the stated mathematical task

That negative result matters because it pushes the project away from the laziest narrative of direct “gotcha” item bias. [INFERENCE]

### 2. I **do** see very clear construct-loading differences

The strongest thing visible on the page is not sex coding. It is **burden geometry**:

1. `Apartment Purchase`, `Oil Spill`, and `Power of the Wind` visibly load on diagram parsing, spatial decomposition, scale reasoning, and geometric modelling.
2. `Charts` and `Faulty Players` visibly load on table / graph reading, proportion, and translation from displayed data into statements.
3. `Drip Rate` visibly loads on formula fluency and symbolic dependence between variables.
4. `Penguins` loads on classroom-style percentage change in a concrete science story with low diagram burden.
5. `ASVAB` `Assembling Objects` visibly loads on mental assembly / part-whole spatial matching.
6. `ASVAB` `MK` sample visibly loads on 3D geometry and school-taught formula recall.

So the page-level impression is:

`different item families are obviously measuring different mixtures of spatial, symbolic, graph-reading, and classroom-practice burden`

That is exactly the kind of mechanism the repo has been converging on statistically. [INFERENCE]

### 3. The visible burden split matches the current local PISA content ordering better than a generic “timing burden” story

The current local `PISA 2018` proxy pass says:

1. `space_shape` is the most male-leaning content family
2. `change_relationships` is next
3. `uncertainty_data` is closest to parity

The released public items make that result look face-valid rather than arbitrary:

1. the `space_shape` items are visibly the ones where the student has to parse a plan, an irregular shape, or a geometric layout before any computation even starts
2. the data items are visibly more like graph / table / statement evaluation tasks
3. the formula items sit somewhere else again, with symbolic-relationship burden that is not the same as either pure chart reading or pure spatial layout

This is not proof, but it is a good sanity check that the local content-family result is tracking something real about the item surface. [INFERENCE]

### 4. The face-valid evidence supports construct-loading, not deliberate balancing

The inspected items do **not** look like they were tuned to “help girls” or “help boys” in any crude way.

They look like standard large-scale assessment items that happen to put weight on:

1. graph / table literacy
2. classroom percentage / formula fluency
3. geometric / spatial modelling
4. applied real-world scenario parsing

That makes the most plausible face-valid story:

`measurement disagreement is being driven by which of those burdens a battery rewards, not by an obvious overt ideological attempt to sex-balance scores`

[INFERENCE]

---

## What This Audit Supports

### Hardened

1. the content-family split is real enough to be visible to the eye on public released items
2. the strongest visible difference is construct-loading, especially spatial-layout versus data-display burden
3. the current repo interpretation is better framed as **measurement-surface heterogeneity** than as blatant stereotype bias

### Softened

1. the notion that simple generic time pressure is the main explanation for school-age item heterogeneity
2. the notion that a direct page-level “anti-male” or “anti-female” design bias is obvious in the public items

### Still open

1. whether any of these visible burden differences translate into sex-specific DIF after invariant rescoring
2. whether the same face-valid pattern holds in the non-public operational `CAT-ASVAB` bank
3. whether the school-knowledge / transcript wedge is mostly content-family, format-family, or evaluation-surface

---

## Best Read

The direct item inspection gives a useful but narrow update:

1. I do **not** see a page-level “smoking gun” of overt sexist test design in the inspected public items.
2. I **do** see an obvious construct split between spatial-layout items, graph/table items, and formula-schooling items.
3. That visible split matches the repo's strongest current statistical result better than any simple generic process-burden story.

So the right update is:

`public item inspection supports the repo's construct-loading story, but it does not by itself prove unfairness or latent-trait bias`

---

## Causal-Check Summary

- `P(cause)`: `0.65` that the inspected public items mainly support a construct-loading explanation for at least part of the observed sex-gap heterogeneity.
- `Top alternative`: `0.20` that the visible burden split is real but psychometrically unimportant once latent measurement models are applied.
- `Falsifier`: item-level DIF / invariant-item work showing little or no sex-specific distortion once content family is modeled explicitly.
- `Decision impact`: use this audit as a mechanism sanity check, not as proof. The next decisive step is still item-level DIF / invariant rescoring, not more page-level argument.
