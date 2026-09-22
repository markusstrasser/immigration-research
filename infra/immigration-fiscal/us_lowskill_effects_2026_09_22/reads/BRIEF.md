# Reader brief (one paper per agent)

You read ONE paper's full parsed text (path given in the task) and write ONE result file
(path given in the task). Do not read other files, do not search the web, do not edit
anything else. The parent decides how the paper is used; you extract, with page anchors.

The parent's context: a US fiscal account of the Mexican-origin population (three
generations) for income year 2024, a stationary comparison of taxes, benefits and public
services, with one modelled "production term" (native surplus from immigrant labour, nested
CES over two education cells, elasticity ε between native and foreign-born inside a cell).
The operator also plans non-fiscal sections (wages, employment, housing, schooling,
enforcement). Your job is to give the parent what the paper measured, exactly.

Result file format (Markdown):

**Verdict:** one sentence: what the paper identifies and how strong the design is.

## Population, period, unit
## Design and identification (instrument/experiment, first stage strength if reported, controls)
## Headline estimates
A table: outcome | estimate | SE or CI | table/figure and page | verbatim quote (≤40 words).
Every number MUST carry a verbatim quote copied from the text. No number without a quote.
## What it says about
- native wages by skill/education
- native employment / crowd-out
- housing prices, rents
- fiscal: taxes, transfers, public services, schooling
- firms, production, investment, profits
- mechanism the authors claim
(write "not studied" where the paper is silent)
## Elasticities or parameters a model could transport
Name the object precisely (e.g. "elasticity of substitution between natives and immigrants
within occupation, CZ level"), its value, and the population it was estimated on.
## Authors' stated limitations and external-validity notes
## Data availability (replication package? restricted?)

Verification, mandatory before you finish: for every numeric estimate in your table, run
`rg -F "<a distinctive 4-8 word fragment of the quote>" <paper path>` and confirm a hit.
Drop any row whose quote you cannot re-find. Say at the end how many rows you verified.

Return to the parent: the result file path and ≤10 lines summarising the Verdict and the
two or three estimates that matter most.
