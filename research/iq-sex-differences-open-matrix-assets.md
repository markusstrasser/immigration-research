# IQ Sex Differences - Open Matrix Assets

**Date:** 2026-03-07
**Purpose:** exact status of the currently usable open matrix / Raven-like assets for the next certainty jump.

## Bottom Line

`Raven` itself is still not locally analyzable at the raw-row level.

But the open-matrix branch is now materially better than it was:

1. `ICAR` remains the best local open human matrix-response dataset with sex and item rows. [SOURCE: `research/iq-sex-differences-raven-open-data.md`]
2. `MaRs-IB` is partially open but does **not** currently expose full participant-level raw rows publicly through the live `OSF` API. The paper itself says the full datasets cannot currently be made publicly available and requests should be sent to the authors. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/; `sources/iq-sex-diff/data/matrix_open/marsib_g96f4_osfstorage.json`; `sources/iq-sex-diff/data/matrix_open/marsib_g96f4_node.json`]
3. `OMIB` is fully usable as a stimulus bank right now. The `OSF` repository exposes item SVGs, a web implementation, implementation instructions, and an item-parameter spreadsheet. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC9326670/; `sources/iq-sex-diff/data/matrix_open/omib/omib_4km79_osfstorage.json`]

## MaRs-IB

### What is public

- paper and methods
- open-access items claimed in the repository
- public `OSF` project node `g96f4`
- article text stating that all materials and item-level data have been made available on the archive

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/]

### What is not public in practice

The live public `OSF` storage listing is empty:

- [marsib_g96f4_osfstorage.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/marsib_g96f4_osfstorage.json#L1)

And the paper’s data-availability text explicitly says the **full datasets cannot currently be made publicly available** and should be requested from the authors.

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC6837216/]

### Operational implication

`MaRs-IB` is a **request / author-contact** path, not an immediate raw-data path. [INFERENCE]

## OMIB

The `OMIB` `OSF` node `4km79` is publicly accessible and currently exposes:

- `Web Version.zip`
- `Instructions for Implementation.docx`
- `Item Template.docx`
- `Item Data.xlsx`
- `Figural Matrices.zip`
- `Construction Elements.zip`

[SOURCE: `sources/iq-sex-diff/data/matrix_open/omib/omib_4km79_osfstorage.json`]

These are now local in:

- [repo](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/repo)

Useful local artifacts:

- [download_omib_assets.py](/Users/alien/Projects/research/sources/iq-sex-diff/download_omib_assets.py#L1)
- [inspect_omib_item_data.py](/Users/alien/Projects/research/sources/iq-sex-diff/inspect_omib_item_data.py#L1)
- [omib_item_data_preview.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_item_data_preview.tsv#L1)
- [build_omib_pilot_forms.py](/Users/alien/Projects/research/sources/iq-sex-diff/build_omib_pilot_forms.py#L1)
- [omib_pilot_forms.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_pilot_forms.tsv#L1)
- [build_omib_web_fragments.py](/Users/alien/Projects/research/sources/iq-sex-diff/build_omib_web_fragments.py#L1)
- [pilot_web](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/pilot_web#L1)
- [omib_pilot_package.zip](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_pilot_package.zip#L1)

### What OMIB gives us

1. A reusable open matrix stimulus bank.
2. Item-level parameters (`a`, `b`, rules, rotation, p-values).
3. A working HTML/CSS/JS item implementation template.
4. Enough assets to run a new experiment even without the original participant rows.

### What OMIB does not give us

1. Raw participant-by-item rows from the validation study.
2. Sex-linked performance data from the original sample.

So `OMIB` is a **stimulus / experiment** asset, not a solved observational dataset. [INFERENCE]

## Current Best Use

The cleanest next move is:

1. keep `ICAR` as the current open observational matrix dataset
2. treat `MaRs-IB` as a request path
3. use `OMIB` as the stimulus bank for a randomized timing / item-design study

That is now an executable plan rather than a vague future idea. [INFERENCE]
