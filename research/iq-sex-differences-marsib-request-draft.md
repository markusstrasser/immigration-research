# IQ Sex Differences - MaRs-IB Data Request Draft

**Date:** 2026-03-07
**Purpose:** ready-to-send request for the `MaRs-IB` participant-level data that are described in the paper but not currently public through the live archive.

## Why This Exists

The `MaRs-IB` paper says:

1. materials and item-level data were made available on the archive
2. the full datasets cannot currently be made publicly available
3. requests for item-level data can be sent to the listed contact

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/]

So the immediate next step is a direct request, not more scraping. [INFERENCE]

## Minimal Request Scope

Ask only for what materially advances the matrix-certainty branch:

1. participant sex/gender field as recorded
2. participant age
3. participant-level item responses
4. item-level response times
5. any form / shape-set assignment variables
6. item order as administered

Everything else is optional.

## Draft Email

Subject: Request for MaRs-IB item-level response data for psychometric replication

Body:

```text
Hello,

I am working on a psychometric replication project on sex differences across matrix / figural reasoning surfaces.

I am writing about the MaRs-IB paper:

Chierchia et al. (2019), “The matrix reasoning item bank (MaRs-IB): novel, open-access abstract reasoning items for adolescents and adults”

The paper states that materials and item-level data were archived, but that the full datasets could not be made publicly available and could be requested directly.

I would like to request the minimum participant-level data needed for a replication focused on measurement structure rather than personal profiling:

1. participant sex/gender field as recorded
2. participant age
3. item-level correctness / response data
4. item-level response times
5. form / shape-set assignment variables
6. item order as administered

I do not need any direct personal identifiers.

The planned use is:

1. multi-group latent-variable / invariance checks
2. item-difficulty-by-sex-gap replication
3. timing versus score-geometry analysis

If there is a data use agreement, citation requirement, or restricted sharing condition, I can work within that.

Thank you,
[name]
```

## Operational Notes

If the authors refuse or do not respond, the next honest path is:

1. use the local `OMIB` stimulus bank
2. run a new randomized timing/design study

Do not keep pretending the current `OSF` route will magically yield the raw `MaRs-IB` rows later. [INFERENCE]
