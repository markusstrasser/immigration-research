# IQ Sex Differences - Add Health Public Pair-Link Note

**Date:** 2026-03-06  
**Purpose:** decide whether the local public-use `Add Health` files support a clean within-family or pair-linked extension.

## Probe Result

The public wave I and wave II in-home files clearly expose sibling/twin **flags**, but not an obvious pair identifier or household/family linkage field that would support a clean within-family design in the current local snapshot.

[SOURCE: `sources/iq-sex-diff/addhealth_public_pair_probe.py`; `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]

## What Is Present

Wave I sibling/twin slots:

- `STUDSIBA` to `STUDSIBG`
- `TWINA` to `TWING`

Wave II sibling/twin slots:

- `h2siba` to `h2sibg`
- `h2twina` to `h2twing`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]

Observed values on the first wave-I slots behave like indicator flags rather than linkage IDs:

- `STUDSIBA`: mostly `7`, then `0`, then `1`
- `TWINA`: mostly `7`, then `0`, then `1`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]

## What Is Missing

The only obvious ID-like fields found in the local wave I / II in-home files were:

- `AID` / `aid`
- `H1IR22HH`
- `h2ir22hh`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]

The stronger follow-up check now narrows this further:

- `H1IR22HH` is not a household key; in the public wave-I codebook it behaves like a yes/no item with values `0/1/6/7/8` and in the local wave-I file it has only `6` distinct values, dominated by `7`
- `h2ir22hh` is not a usable household key either; in the local wave-II file it has only `4` distinct values, dominated by `7.0`

[SOURCE: `sources/iq-sex-diff/data/addhealth/codebooks/wave1_W1inhome_codebook.pdf`; `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]

That is not enough to justify a claim that the current public files expose recoverable sibling-pair or household-pair linkage. In the current probe, no explicit public pair ID or household/family ID surfaced, and the two most tempting `*HH` fields do not behave like linkage keys. [INFERENCE]

## Operational Decision

Treat the public `Add Health` within-family extension as **blocked for now**.

- `P(cause)`: `0.78` that the current public files simply do not expose the right linkage surface for a clean within-family design. [INFERENCE]
- `Top alternative`: `0.17` that the linkage surface exists under a non-obvious name in a companion public file we have not yet joined. [INFERENCE]
- `Falsifier`: a public codebook or companion file showing an actual recoverable family/pair identifier linked to the in-home respondents. [INFERENCE]
- `Decision impact`: stop treating public `Add Health` family linkage as the next obvious extension; if a family-linked `Add Health` design becomes important, it likely requires a richer companion file or restricted path. [INFERENCE]

## Consequence For The Project

The canonical public-use `Add Health` branch remains:

- a broad school-performance / evaluation-family replication
- not a clean transcript/test adjudication dataset
- not a clean within-family dataset in the current local public snapshot

[SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `sources/iq-sex-diff/data/addhealth/addhealth_public_pair_probe.json`]
