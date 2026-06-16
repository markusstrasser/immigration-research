# Raven Open-Data Status And Matrix Follow-Up

**Date:** 2026-03-07
**Question:** Are there public datasets where we can analyze `Raven` or `Raven-like` matrix performance ourselves, and what do they show?

## Bottom Line

Yes, but with an important split:

1. **Clean public raw `Raven` data are not easy to recover.**
2. **Open matrix-reasoning human data do exist and are already local in this repo.**

In this pass:

- I verified that the public `OSF` project linked from a recent `RSPM` paper is real, but its public API file listings are empty.
- I downloaded the journal supplementary ZIP via a browser route, and it contained only a supplementary PDF, not raw participant data.
- I then ran the nearest honest open-data substitute we already have local: `ICAR / SAPA` matrix reasoning.

That local matrix-only result is useful:

- all `11/11` checked `ICAR` matrix items are male-leaning
- harder / later matrix items are **more** male-leaning, not less
- response-rate differences by sex are basically zero, so this does **not** look like a simple "girls never reached the hard items" story inside this dataset

[SOURCE: `sources/iq-sex-diff/data/raven_rspm/osf_d5jph_node.json`; `sources/iq-sex-diff/data/raven_rspm/osf_d5jph_osfstorage.json`; `sources/iq-sex-diff/data/raven_rspm/osf_phxrb_registration.json`; `sources/iq-sex-diff/data/raven_rspm/osf_phxrb_osfstorage.json`; `sources/iq-sex-diff/data/raven_rspm/jintelligence-11-00072-s001.zip`; `sources/iq-sex-diff/icar_matrix_item_pass.py`; `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`; `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`]

## 1. What I Could Actually Recover For Raven

### Public `RSPM` adolescent project

The recent article:

- `Raven’s Standard Progressive Matrices for Adolescents: A Case for a Shortened Version`
- says open data are at `https://osf.io/d5jph/`
- and exposes a supplementary ZIP from the journal page

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC10144826/]

### What the public endpoints actually gave me

The `OSF` node and registration are real:

- project node: `d5jph`
- linked registration: `phxrb`

But the public `OSF` storage listings are empty on both the project and registration:

- `sources/iq-sex-diff/data/raven_rspm/osf_d5jph_osfstorage.json`
- `sources/iq-sex-diff/data/raven_rspm/osf_phxrb_osfstorage.json`

[SOURCE: `sources/iq-sex-diff/data/raven_rspm/osf_d5jph_osfstorage.json`; `sources/iq-sex-diff/data/raven_rspm/osf_phxrb_osfstorage.json`]

I also downloaded the journal supplementary ZIP through a browser route because the direct `curl` path hit NCBI's proof-of-work page. The ZIP unpacked successfully, but it contains only:

- `jintelligence-2251912-supplementary.pdf`

and that PDF contains supplementary model tables and diagnostics, not raw participant rows.

[SOURCE: `sources/iq-sex-diff/data/raven_rspm/jintelligence-11-00072-s001.zip`; `sources/iq-sex-diff/data/raven_rspm/unpacked/jintelligence-2251912-supplementary.pdf`]

### Honest status

So for this project:

- the `Raven` paper and `OSF` links are real
- but I did **not** recover analyzable raw participant data from this public route

That means I am not going to pretend we now have a clean raw `Raven` dataset. [INFERENCE]

## 2. The Best Open Matrix Dataset We Already Have

The repo already has local `ICAR / SAPA` open data:

- file: `sources/iq-sex-diff/data/icar/sapaICARData18aug2010thru20may2013.csv`
- rows: `96,958`
- includes a matrix-reasoning domain and a `3D rotation` domain

[SOURCE: `research/iq-sex-differences-dataset-cards.md`]

This is **not** `Raven`, but it is the best currently local open human matrix-style dataset for direct analysis. [INFERENCE]

## 3. New ICAR Matrix-Only Result

I ran:

- `sources/iq-sex-diff/icar_matrix_item_pass.py`

Outputs:

- `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`
- `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`
- `sources/iq-sex-diff/data/icar/icar_matrix_age_summary.tsv`

### Matrix-domain summary

Across respondents with any matrix-reasoning data:

- female `n = 61,422`
- male `n = 31,134`
- female mean item accuracy = `0.5295`
- male mean item accuracy = `0.5774`
- `d = -0.136` favoring males

[SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`]

### Item-level pattern

All `11` checked matrix items are male-leaning on raw accuracy:

- easiest checked item `MR.43`: raw female-minus-male gap `-0.052`
- hardest checked item `MR.55`: raw female-minus-male gap `-0.091`

All `11` checked items also remain male-leaning after a simple leave-one-out anchor adjustment:

- `MR.43`: anchor-adjusted female logit beta `-0.248`
- `MR.55`: anchor-adjusted female logit beta `-0.367`

[SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`]

### Does the male edge get larger on harder matrix items?

Yes, in this open dataset.

Correlations:

- difficulty vs raw sex gap: `-0.373`
- difficulty vs anchor-adjusted sex beta: `-0.333`
- item order vs raw sex gap: `-0.598`
- item order vs anchor-adjusted sex beta: `-0.473`

Negative here means later / harder items are more male-leaning.

[SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`]

### Does this look like item exhaustion?

Not inside `ICAR` matrix reasoning.

Mean female-minus-male response-rate gap across the `11` matrix items is only:

- `+0.001854`

That is effectively zero at the descriptive level. In this dataset the matrix item pattern does **not** look like one sex simply failing to reach the later items. [SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`]

## 4. Age Pattern In ICAR Matrix Reasoning

The male edge is small at the youngest band and larger through most adult bands:

- `18andUnder`: `d = -0.022`
- `19to24`: `d = -0.148`
- `25to29`: `d = -0.179`
- `30to34`: `d = -0.199`
- `35to39`: `d = -0.254`

[SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_age_summary.tsv`]

This is convenience-sample internet data, so I would not overread the age curve. But the direction is not random. [INFERENCE]

## 5. Causal Check

**Observation:** In the best open matrix-style dataset currently local, every checked matrix item is male-leaning, and later / harder items are more male-leaning, while item response rates are essentially the same by sex. [SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_summary.tsv`; `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`]

**Null:** The matrix-family male edge reflects a real content-family or latent-domain difference on this surface, not a simple timing / exhaustion artifact. [INFERENCE]

**Residual after null:** We still do not know whether this pattern would survive in a representative raw `Raven` dataset, because I did not recover one here. [INFERENCE]

**Geometry:** broad across items, stronger on harder / later items, not concentrated in a few anomalous items. [SOURCE: `sources/iq-sex-diff/data/icar/icar_matrix_item_summary.tsv`]

**P(cause):** `0.70` that the open-data matrix pattern is mainly an item-family / domain pattern rather than a differential item-reach pattern.

**Top alternative:** `0.20` that some unmodeled convenience-sample process difference still explains part of the gradient.

**Falsifier:** a representative raw `Raven` or equivalent matrix dataset where harder items do **not** become more male-leaning once exposure / completion is aligned.

**Decision impact:** stop using "maybe girls just ran out of time on the hard matrix items" as the default explanation for open matrix-style male advantages. The data we actually have do not support that explanation here.

## 6. What This Does And Does Not Prove

What it proves:

- there are open human matrix-style datasets we can analyze ourselves
- the best current local one (`ICAR`) shows a male-leaning matrix pattern that strengthens on harder / later items
- the retrieved public `Raven` adolescent route did **not** yield raw rows

What it does **not** prove:

- that `Raven` itself always shows the same pattern
- that the open `ICAR` result equals a battery-invariant `g` difference
- that timing is irrelevant in every matrix battery

## 7. Best Next Step

There are now two clean options:

1. find a second raw matrix dataset with participant sex and item responses
2. treat `ICAR` as the open-data matrix sandbox and stop pretending the current `OSF` `Raven` route is solved

If the goal is "actual Raven, not just Raven-like," the next move is another raw-data hunt, not more inference from this article's summary tables. [INFERENCE]
