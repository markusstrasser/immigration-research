# Immigration confidence ladder

Date: 2026-04-10

Scale:
1. `strong`
2. `medium`
3. `weak`
4. `contextual-only`

Rule:
A metric can be statistically clean and still be only `contextual-only` for the question we are asking.

## Strong

1. `ACS origin / education / recency composition counts`
Rating: `strong`
Reason: these are direct weighted ACS summaries, not inferred fiscal objects. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_origins.sql]

2. `PUMA-level median gross rent as destination cost exposure`
Rating: `strong`
Reason: official ACS geography, directly observed, useful as exposure context. It is not a welfare scalar. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]

3. `Household-normalized school-age child metrics after WGTP correction`
Rating: `strong`
Reason: the prior proxy was wrong; the corrected household join is materially better and uses the right unit. [SOURCE: /Users/alien/Projects/research/research/immigration-household-weighted-correction.md]

4. `Claim that the Clark “agree” papers are scope-limited rather than obviously false`
Rating: `strong`
Reason: that conclusion survives repeated paper review and is consistent with the actual paper scopes. [SOURCE: /Users/alien/Projects/research/research/immigration-economist-effects-matrix.md]

## Medium

5. `Federal versus state/local incidence split as a research frame`
Rating: `medium`
Reason: official sources strongly support the split, but our own warehouse only partially models the federal side. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

6. `County CHAS housing-stress shares`
Rating: `medium`
Reason: good background stress metric, but not immigrant-attributable marginal burden. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_stage2_incidence_context.py]

7. `State school-spending per pupil as school-pressure context`
Rating: `medium`
Reason: official and clean, but too coarse for marginal burden or district-specific claims. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql]

8. `Housing-heavy versus school-heavy origin-group typology`
Rating: `medium`
Reason: useful descriptive shorthand for destination exposure, but still proxy-based and sensitive to geography choice. [SOURCE: /Users/alien/Projects/research/research/immigration-local-burden-puma-layer.md]

9. `Descendant upside as a real channel`
Rating: `medium`
Reason: the long-run literature supports it, but sign and magnitude are heterogeneous and horizon-dependent. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.nber.org/system/files/working_papers/w33961/w33961.pdf]

## Weak

10. `Area-weighted PUMA-to-county bridge`
Rating: `weak`
Reason: land area is not people, renters, students, or immigrant households. This is a convenience bridge, not a precise exposure model. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py]

11. `IRS county migration balance as burden evidence`
Rating: `weak`
Reason: at best it is contextual mobility climate. It is not immigrant-specific and not causal. [SOURCE: /Users/alien/Projects/research/research/immigration-stage2-county-bridge-batch.md]

12. `Federal-positive versus federal-negative origin ranking from ACS income and benefit proxies`
Rating: `weak`
Reason: this is not a tax-transfer microsimulation. It is a partial proxy stack. [SOURCE: /Users/alien/Projects/research/research/immigration-low-skill-origin-incidence-memo.md]

13. `Magnitude claims for local school burden from current warehouse`
Rating: `weak`
Reason: district assignment, ELL intensity, migrant composition, and marginal cost are not modeled well enough yet. [SOURCE: /Users/alien/Projects/research/research/immigration-adversarial-review.md]

## Contextual-only

14. `County CHAS plus rent plus school-spend combined into one local burden scalar`
Rating: `contextual-only`
Reason: combining context layers does not make a causal burden estimate.

15. `Average citizen better off / worse off`
Rating: `contextual-only`
Reason: too much depends on weights over renters, employers, taxpayers, future descendants, and politics.

16. `Bad for the country`
Rating: `contextual-only`
Reason: without explicit horizon and counterfactuals, the phrase has almost no analytical content.

## Causal-design layer added 2026-04-18

17. `Borjas wage prediction for U.S. native low-skill workers from E-Verify`
Rating: `strong rejection`
Reason: TWFE on QWI 2003-2023, 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 controls. Coefficient on E1 in E-Verify-exposed industries: +0.51% (SE 0.81%, n=16,736). 95% CI excludes Borjas magnitudes (>2.1%). Replicates Card direction. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]

18. `Immigrants concentrate in inelastic-supply MSAs (welfare implication for rent burden)`
Rating: `strong (descriptive)`
Reason: top FB-share quintile median Saiz 2010 elasticity = 1.51, bottom = 3.40. n=237 MSAs, ACS 2018-22. Implication: rent exposure in destination markets is closer to welfare loss than the adversarial review allowed. [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

19. `Card-style labor-market complementarity for U.S. low-skill immigration`
Rating: `medium-strong`
Reason: convergent evidence — Card 1990 Mariel, Foged-Peri 2016 Denmark refugee assignment, this cycle's E-Verify TWFE 2003-2023. Borjas 2017 restricted-Mariel reanalysis does not generalize to broader staggered designs. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]

## Two weakest assumptions

1. `Federal-side proxy ledger`
Current shortcut: infer federal incidence from income plus selected benefit flags.
Why weak: taxes, credits, SNAP, SSI, Medicaid, payroll taxes, and household composition are not directly modeled.

2. `Coarse local burden bridge`
Current shortcut: state school-spend plus PUMA rent plus area-weighted county overlays.
Why weak: local service burden depends on actual district context, renter mix, crowding, tract population, and school-age distribution, not land area.

## Practical reading rule

If a conclusion depends mainly on items `10` through `16`, present it as a hypothesis or descriptive tendency, not a settled result.

<!-- knowledge-index
generated: 2026-04-19T03:45:46Z
hash: fcda332542b1

cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-saiz-elasticity-rent.md, research/research/immigration-adversarial-review.md, research/research/immigration-economist-effects-matrix.md, research/research/immigration-household-weighted-correction.md, research/research/immigration-local-burden-puma-layer.md, research/research/immigration-low-skill-origin-incidence-memo.md, research/research/immigration-stage2-county-bridge-batch.md

end-knowledge-index -->
