# IQ Sex Differences - TIMSS Public Item-Level Wall

**Date:** 2026-03-06  
**Purpose:** document why a `TIMSS 2019` public item-level residual / DIF-style pass is currently blocked in the staged public files.

## What Was Checked

The staged Grade 8 public bundle has:

- achievement/data files in `sources/iq-sex-diff/data/timss/T19_G8_SPSS%20Data.zip`
- item-information workbooks in `sources/iq-sex-diff/data/timss/T19_G8_Item%20Information.zip`

[SOURCE: `sources/iq-sex-diff/data/timss/T19_G8_SPSS%20Data.zip`; `sources/iq-sex-diff/data/timss/T19_G8_Item%20Information.zip`]

The item-information workbook is usable and exposes direct item IDs such as:

- `MP52024`
- `MP52058A`
- `MP52125`
- `SP52006`

with content and cognitive-domain labels. [SOURCE: `sources/iq-sex-diff/data/timss/T19_G8_Item%20Information.zip`]

The Grade 8 achievement files also carry those item columns in metadata. [SOURCE: `sources/iq-sex-diff/data/timss/T19_G8_SPSS%20Data.zip`]

## The Problem

In the staged public files checked so far, the item columns appear to be blank in the actual data payload.

Probe results:

- `bsausam7.sav`: `ITSEX` and `TOTWGT` are fully populated, but `MP52024`, `MP52058A`, `MP52125`, and `SP52006` all have `0` nonmissing values.
- `bsaadum7.sav`: same result.
- `bsgusam7.sav`: sex and weight fields are present, but this file does not rescue the checked item-response columns.

[SOURCE: `sources/iq-sex-diff/data/timss/timss_public_item_probe.tsv`; `sources/iq-sex-diff/timss_public_item_probe.py`]

## Interpretation

This means the current staged public `TIMSS` payload is good enough for:

- plausible-value domain summaries
- grade / country / cognitive-domain comparisons

It is **not** currently good enough for the same kind of item-level residual or anchor-based pass used on local `PISA 2018`, because the checked public item-response cells are blank rather than merely matrix-sampled.

[INFERENCE]

## Causal / Measurement Implication

The repo should not claim item-level `TIMSS` hardening unless one of these happens:

1. a different public `TIMSS` file with actual response-level item cells is found
2. a restricted or alternative release exposes the responses
3. the current blank-item result is shown to be a parsing error rather than a public-release limit

[INFERENCE]

For now, `TIMSS` remains:

- a valid domain / grade / advanced-track battery
- not a validated local item-level DIF battery

[INFERENCE]
