# Brief: does ethnic fragmentation lower network connectedness, and does connectedness scale output?

Operator, 2026-09-28 22:23 JST: "I think this higher network and deeper connectedness and less
fragmentation would scale" (context: replacing the union with 40.9M native whites; sister lane
`white_replacement_2026_09_28`).

## Hypothesis to test (and to try to kill)

H1. Places with a larger Hispanic / Mexican-origin share have lower social connectedness at equal
income, urbanicity and region. H2. Connectedness raises economic outcomes superlinearly with
network size (a scale effect through ties), so a less fragmented population of equal size yields more.
Steel-man H1/H2 (Putnam 2007; Alesina–La Ferrara; Alesina–Baqir–Easterly 1999; Bettencourt urban
scaling) and the other side (Ottaviano–Peri 2006 diversity and wages; Alesina–Harnoss–Rapoport
2016 birthplace diversity; Burchardi et al. ancestry diversity and innovation; repo ladder 89, 117,
149, 233) before running anything.

## Data

Chetty et al. 2022 (Nature 608) Social Capital Atlas, county and ZIP files: economic connectedness
(EC), friending bias, exposure, clustering (cohesiveness), volunteering / civic organizations. Public
download (Opportunity Insights / HDX). Stage under `_cache/`, record URL, date and sha256 in the
RESULT; follow the data-acquisition skill. Group shares from ACS 5-year (Census API; key in
`infra/immigration-fiscal/acquire/config.local.env`, never print it, redact API output). Check the
dataset register first for already-staged county ACS tables.

## Tests

1. County and ZIP regressions of each Atlas measure on Hispanic share (and Mexican-origin share
   where available), controls: median income, poverty, education, density / urbanicity, Black share,
   state FE. Report coefficients with SEs clustered by state, and per 10 points of share.
2. Decompose: is any association exposure (who is around) or friending bias (who befriends whom)?
   The Atlas separates them.
3. Outcome bridge: does EC or clustering predict county earnings / mobility / patents per capita
   conditional on the same controls, and is the slope steeper in larger places (interaction with log
   population = the "scaling" claim)? Use Opportunity Atlas mobility (already in repo per ladder 82)
   and a patent count only if a primary county source is local or cheaply fetched.
4. Size it: if H1 and H2 both hold, what does the implied EC change from the union's share do to
   other residents' earnings, in $bn, with an interval? If either fails, say so and stop there.

Identification: cross-sectional; state it. No causal language beyond what a design supports. A null
is not zero: report what size the design could detect.

## Rules

Lane dir `infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/`; scripts at root, outputs
in `derived/`, raw in `_cache/`; `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 …` from the repo
root; CSV `lineterminator="\n"`; tag every number. Rerun twice, byte-identical. Do not edit other
lanes, the ladder, INDEX or memos; do not commit. `RESULT.md` written first, appended as you go; after
the model-ID line its first content line opens with `**Verdict:**`. Return its path and ≤10 lines.

Parent's pre-stated expectation: H1 holds partly and mostly through exposure (segregation), not
friending bias; H2's scale interaction is weak or imprecise in a county cross-section.
