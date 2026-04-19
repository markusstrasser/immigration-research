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

## Paradigm-escape layer added 2026-04-18 (evening)

20. `Saiz elasticity-immigrant correlation operates through regulatory not topographic channel`
Rating: `strong`
Reason: log(FB share) ~ unaval (β=+0.12, t=0.58, n.s.) + WRLURI (β=+0.33, t=6.29***) + log_pop. The inelastic-MSA immigrant concentration is driven by zoning, not topography. Implication: zoning reform is a viable lever for the rent-burden problem; immigration restriction is not the only policy response. [SOURCE: scripts/saiz_decomposition.py]

21. `Sanctuary policy variation does not change native low-skill wages either direction`
Rating: `strong rejection (replicates E-Verify finding)`
Reason: TWFE on QWI 2003-2023 with 12 pro-sanctuary + 9 anti-sanctuary states; all E1 specifications |t|<1.0. Third convergent confirmation of Card-side null on the wage channel. [SOURCE: scripts/analyze_sanctuary_wages.py]

22. `Native US migration is ~33x larger per capita than recent immigration at median county`
Rating: `strong (administrative data, not survey)`
Reason: IRS SOI county-county migration 2022-23 + ACS B05005 recent-FB. Median county receives 3.0% native inflow vs 0.08% immigrant inflow per year. Top native-inflow counties (Geary KS, Liberty GA, Texas exurbs) are non-immigrant gateways. Reframes "newcomer burden" as predominantly native-driven outside specific immigrant gateways. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

23. `Open-borders welfare verdict is welfare-weight-determined, not data-determined`
Rating: `strong (framing claim)`
Reason: At immigrant-welfare-weight w=0 (current repo's implicit framing): negative by construction. At w≥0.25 under 25%-of-gross-gains native-cost benchmark: positive. At w=1.0 even under harsh 50%-cost benchmark: positive. Empirical evidence cannot adjudicate the values choice. Honest framing must name the weight. [SOURCE: data/clemens/gpt54_calibration_review.md, GPT-5.4 sensitivity analysis]

24. `Mass deportation of 7M unauthorized → ~$1.5-2.3T one-time output shock (5-8% GDP)`
Rating: `medium (calibration not estimate)`
Reason: BEA Use Table 2023 partial-equilibrium with industry FB-share assumptions from Pew/CMS. First-order $1.45T, with Type-II multiplier (~1.6) $2.32T. Per-removed-worker loss $207K-$332K. Most affected: Construction (-5.9%), Other services / cleaning (-8.8%), Agriculture (-4.3%). Calibration consistent with E-Verify empirical finding (-6% E1 employment under 50% compliance). [SOURCE: scripts/mass_deportation_sim.py]

## Surge layer added 2026-04-18 (late evening)

25. `Title 42 lift was not the surge cause; surge was a regime shift starting Dec 2022`
Rating: `medium`
Reason: SWB encounters peaked Jan-Mar 2023 at 50K+/month BEFORE Title 42 lift (May 2023). Lift coincided with April-May lull, then gradual rebuild to surge levels. Pre/post comparison is composition-driven, not policy-causal. [SOURCE: research/immigration-causal-surge-2021-2024.md]

26. `CHNV parole did not substitute legal flow for illegal flow; it added on top`
Rating: `strong`
Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023. Encounters from CHNV nationalities ROSE 787% post-program, not fell. Refutes the stated rationale that legal pathway would reduce irregular migration. [SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]

27. `Receiver-city local fiscal load was real and concentrated`
Rating: `strong (administrative data)`
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M peak; Denver $89M (with cuts to other services). Combined ~$5B+/yr peak across major receivers. System-collapse claim has empirical bite. [SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers`
Rating: `medium (correlation, multiple confounders)`
Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***). Top receivers (Bronx +11pp, Queens +11pp, Hidalgo +10pp, Cameron +10pp, El Paso +10pp, Miami-Dade +9pp) swung massively toward Trump. Confounders include national Hispanic realignment, inflation, and policy-endogenous busing destinations. Magnitude implausibly large for non-immigration causes alone. [SOURCE: research/immigration-causal-surge-2021-2024.md]

29. `Static-cycle Card-wins finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation`
Rating: `meta-update on prior entries 17, 19, 21`
Reason: Prior entries claim "decisive Card-side win for U.S. policy variation." True for variation 2008-2021 (E-Verify, sanctuary). The 2021-2024 surge is a regime shift outside that variation. Linear extrapolation is not warranted. Surge-period wage estimates remain to be done (require ACS PUMS 2023). [SOURCE: research/immigration-causal-surge-2021-2024.md]

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
generated: 2026-04-19T04:47:35Z
hash: 7c9873d31903

cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-surge-2021-2024.md, research/research/immigration-adversarial-review.md, research/research/immigration-economist-effects-matrix.md, research/research/immigration-household-weighted-correction.md, research/research/immigration-local-burden-puma-layer.md, research/research/immigration-low-skill-origin-incidence-memo.md, research/research/immigration-stage2-county-bridge-batch.md

end-knowledge-index -->
