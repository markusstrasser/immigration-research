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

17. `Large Borjas-style native wage gains under observed E-Verify mandates`
Rating: `strong against large gains in this design`
Reason: TWFE on QWI 2003-2023, 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 controls. Coefficient on E1 in E-Verify-exposed industries: +0.51% (SE 0.81%, n=16,736). 95% CI excludes large Borjas-style magnitudes (>2.1%) for this observed mandate margin. Aligns with Card direction; not a direct replication or a global wage-family rejection. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]

18. `Immigrants concentrate in inelastic-supply MSAs (welfare implication for rent burden)`
Rating: `strong (descriptive)`
Reason: top FB-share quintile median Saiz 2010 elasticity = 1.51, bottom = 3.40. n=237 MSAs, ACS 2018-22. Implication: rent exposure in inelastic destination markets is a stronger renter-incidence warning than the adversarial review allowed; aggregate welfare loss remains unmeasured. [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

19. `Card-style labor-market complementarity for U.S. low-skill immigration`
Rating: `medium-strong`
Reason: convergent evidence — Card 1990 Mariel, Foged-Peri 2016 Denmark refugee assignment, this cycle's E-Verify TWFE 2003-2023. Borjas 2017 restricted-Mariel reanalysis does not generalize to broader staggered designs. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]

## Paradigm-escape layer added 2026-04-18 (evening)

20. `Saiz elasticity-immigrant correlation operates through regulatory not topographic channel` — **QUALIFIED by entry 38**
Rating: `strong`
Reason: log(FB share) ~ unaval (β=+0.12, t=0.58, n.s.) + WRLURI (β=+0.33, t=6.29***) + log_pop. The inelastic-MSA immigrant concentration is driven by zoning, not topography. Implication: zoning reform is a viable lever for the rent-burden problem; immigration restriction is not the only policy response. [SOURCE: scripts/saiz_decomposition.py]

21. `Sanctuary policy variation does not change native low-skill wages either direction`
Rating: `strong null result in this design`
Reason: TWFE on QWI 2003-2023 with 12 pro-sanctuary + 9 anti-sanctuary states; all E1 specifications |t|<1.0. Additional QWI policy-margin check consistent with the E-Verify null; supports the bounded Card-side reading for observed marginal policy variation. [SOURCE: scripts/analyze_sanctuary_wages.py]

22. `Domestic newcomer counts are much larger than moved-from-abroad counts at median county`
Rating: `medium`
Reason: IRS SOI `Total Migration-US` 2022-23 and ACS `B07001_081E` point in the same descriptive direction, but they are not like-for-like universes. The current median county comparison is roughly `4.59%` vs `0.21%`, with a ratio of medians around `21.7x` and a median county-level ratio around `20.5x`, so the safe claim is order-of-magnitude disparity, not a precise burden ratio. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

23. `Open-borders welfare verdict is welfare-weight-determined, not data-determined` — **QUALIFIED by entry 39**
Rating: `strong (framing claim)`
Reason: At immigrant-welfare-weight w=0 (current repo's implicit framing): negative by construction. At w≥0.25 under 25%-of-gross-gains native-cost benchmark: positive. At w=1.0 even under harsh 50%-cost benchmark: positive. Empirical evidence cannot adjudicate the values choice. Honest framing must name the weight. [SOURCE: data/clemens/gpt54_calibration_review.md, GPT-5.4 sensitivity analysis]

24. `Mass deportation of 7M unauthorized → ~$1.45T first-order output shock (~5% GDP); Type-II endpoint is sensitivity only` — **presentation qualified by entry 32**
Rating: `medium (calibration not estimate)`
Reason: BEA Use Table 2023 partial-equilibrium with industry FB-share assumptions from Pew/CMS. First-order $1.45T; a Type-II multiplier (~1.6) gives a $2.32T sensitivity, not a headline estimate. Per-removed-worker loss $207K first-order and $332K under Type-II sensitivity. Most affected: Construction (-5.9%), Other services / cleaning (-8.8%), Agriculture (-4.3%). Calibration consistent with E-Verify empirical finding (-6% E1 employment under 50% compliance). [SOURCE: scripts/mass_deportation_sim.py]

## Surge layer added 2026-04-18 (late evening)

25. `Title 42 lift was not the surge cause; surge was a regime shift starting Dec 2022` — **EVIDENCE SUPERSEDED by entry 35**
Rating: `medium`
Reason: SWB encounters peaked Jan-Mar 2023 at 50K+/month BEFORE Title 42 lift (May 2023). Lift coincided with April-May lull, then gradual rebuild to surge levels. Pre/post comparison is composition-driven, not policy-causal. [SOURCE: research/immigration-causal-surge-2021-2024.md]

26. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
Rating: `strong`
Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023. Encounters from CHNV nationalities ROSE 787% post-program, not fell. Refutes the stated rationale that legal pathway would reduce irregular migration. [SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]

27. `Receiver-city local fiscal load was real and concentrated` — **scope qualified by entry 33**
Rating: `strong (administrative data)`
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M peak; Denver $89M (with cuts to other services). Combined ~$5B+/yr peak across major receivers. Receiver-load stress has empirical bite, but these are gross outlays; entry 33 supplies the net-burden caveat. [SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers` — **QUALIFIED by entries 31 and 36; final causal-implausibility sentence superseded**
Rating: `medium (correlation, multiple confounders)`
Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***). Top receivers (Bronx +11pp, Queens +11pp, Hidalgo +10pp, Cameron +10pp, El Paso +10pp, Miami-Dade +9pp) swung massively toward Trump. Confounders include national Hispanic realignment, inflation, and policy-endogenous busing destinations. Magnitude implausibly large for non-immigration causes alone. **Do not reuse the final sentence; entries 31 and 36 supersede it with the controlled +2.4pp upper-bound framing.** [SOURCE: research/immigration-causal-surge-2021-2024.md]

29. `Static-cycle Card-wins finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation`
Rating: `meta-update on prior entries 17, 19, 21`
Reason: Prior entries over-compressed the E-Verify/sanctuary wage results as a "decisive Card-side win for U.S. policy variation." The safer reading is strong Card-side evidence for observed 2008-2021 marginal policy variation. The 2021-2024 surge is a regime shift outside that variation. Linear extrapolation is not warranted. Surge-period wage estimates remain to be done (require ACS PUMS 2023). [SOURCE: research/immigration-causal-surge-2021-2024.md]

## Bias-audit layer added 2026-06-11

Trigger: mirror-test against the criticisms of the Cato 2026 fiscal study ("did we commit its biases?"). Full audit and the general checklist live in [notes/quant-bias-checklist.md](../notes/quant-bias-checklist.md). Prior entries are not rewritten (append-only); these supersede where they conflict.

30. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
Reason: interim downgrade before the OHSS parser correction. The source memo itself listed reverse causation as a live mechanism, but entry 34 later reversed the descriptive reading too: the "+787%" rise was the program's lawful OFO channel on a scrambled clock, while corrected USBP between-port crossings fell sharply. Do not reuse the "substitution did not happen" language or the `+787%` figure except as an error trace. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]

31. `Receiver-city 2024 GOP swing` (entry 28) — **grade unchanged (medium), headline language corrected**
The phrase "magnitude implausibly large for non-immigration causes alone" is a plausibility assertion doing causal work and should not be reused. The top swing counties (Bronx, Queens, Miami-Dade, Hidalgo, El Paso) are among the most Hispanic-populous counties in the country; the national 2024 Hispanic realignment is near-collinear with "receiver city" in that list, and the multivariate pass controls FB share but not Hispanic share. Use the controlled estimate (+2.4pp, receiver_city β=+0.024, state FE) rather than the raw +4.41pp gap, and treat even that as upper-bound until a Hispanic-share control or within-Hispanic-county comparison is run. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: notes/quant-bias-checklist.md item 25]

32. `Mass deportation output shock` (entry 24) — **grade unchanged (medium, calibration), presentation rule added**
Lead with the first-order figure (`~$1.45T`, ~5% GDP); the `$2.32T` Type-II-multiplier endpoint appears only as labeled sensitivity, never inside a headline range. Stacking the modeled amplifier into the headline is the same move as Cato's `$3.9T` interest-savings add-on (27% of their `$14.5T`), in the opposite political direction. The calibration also freezes replacement hiring, wage response, and capital reallocation at zero — state this when quoting. [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] [SOURCE: notes/quant-bias-checklist.md items 4, 15]

33. `Receiver-city fiscal load` (entry 27) — **grade unchanged (strong, administrative data), scope annotation**
The figures are **gross city outlays**, not net burden: federal Shelter and Services Program reimbursements and the counterfactual baseline growth of homeless-services spending are not netted out. "NYC spent $3.7B in FY24" is strong; "the surge cost NYC $3.7B net" is not yet supported. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv] [SOURCE: notes/quant-bias-checklist.md item 10]

## Data-correction layer added 2026-06-11 (evening)

Trigger: the morning layer's two open kill-tests were run against local data and exposed two bugs in the OHSS encounter parser (fiscal-index dates; agency-block overwrite that made the series OFO-ports-only). Full trace: [decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md). These entries supersede 25, 26, and 30 where they conflict.

34. `CHNV substituted lawful port flow for irregular crossings in its initial year` — **reversal of entry 26**
Rating: `strong (initial period); medium beyond ~12 months`
Reason: corrected USBP (between-ports) event study with staggered dates and flat pre-trends: Cuba −95.3%, Nicaragua −96.2%, Venezuela −57.5% (initial, decaying by τ+11 — Darién rebound), Haiti structurally ~0 between ports. Mean τ[0,+3] = −2.17 log points. The old "+787% — added on top" figure was the program's own lawful OFO channel on a scrambled clock; corrected total-CBP DiD is null (β=+0.45, t=1.29). Ledger discipline: lawful parole inflow (~530K) still lands in receiver cities — substitution-of-channel, not reduction-of-arrivals. [SOURCE: sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json]

35. `Title 42 lift did not cause the surge` — **conclusion of entry 25 retained, evidence replaced**
Rating: `medium`
Reason: the entry's timing facts were artifacts. Corrected series: Dec-2022 local peak 252K → Jan-Feb 2023 trough (CHNV substitution visible) → April-May 2023 anticipation spike (212K/207K) → June post-lift crash (−30%) → Dec 2023 record 301,980. Post-lift 6-month mean −14.5% vs pre-lift. [SOURCE: scripts/analyze_surge_title42_chnv.py rerun 2026-06-11]

36. `Receiver-city 2024 GOP swing survives the Hispanic-realignment control` — **closes entry 31's open work**
Rating: `medium (correlation; robust to the named rival channel)`
Reason: pre-registered kill-test with 2020 county Hispanic share (popest baseline): receiver β +0.0256 → +0.0238 (t≈7.2) with the control in; Hispanic share itself β=+0.062 (t=17.2); within top-Hispanic-quintile, receivers +4.3pp raw vs comparable counties. Hispanic-share robustness gate passed. Still cross-sectional; busing destinations policy-endogenous; use the controlled +2.4pp. [SOURCE: sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json]

37. `OHSS-derived series require an external-anchor check before regression`
Rating: `strong (process rule)`
Reason: one known published value per series (e.g., Dec 2023 = 302K) would have caught both bugs at build time; the bugs survived 7 weeks and three ladder entries because year-boundary cuts masked them. [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]

38. `Saiz WRLURI result is descriptive, not identified zoning causation` — **scope correction to entry 20**
Rating: `strong descriptive regression; causal lever unverified`
Reason: WRLURI is a much stronger correlate of foreign-born share than topographic unavailability in the Saiz decomposition, but the cross-section does not prove that zoning causes immigrant concentration, that zoning reform would reduce immigrant renter burden, or that immigration restriction is dominated as a policy response. Treat zoning reform as a plausible policy hypothesis pending panel/IV evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

39. `Open-borders verdict has a normative weight and empirical-input components`
Rating: `strong framing correction`
Reason: The immigrant-welfare weight is a value parameter; empirical evidence cannot choose it. But native-cost benchmarks, fiscal ledgers, housing/capacity constraints, and sending-country effects remain empirical inputs that can move scenario break-evens. Treat entry 23 as a weight-sensitivity claim under the then-current GPT-5.4/Clemens calibration, not as a reason to stop collecting cost or feasibility evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: data/clemens/gpt54_calibration_review.md]

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
