# Lane brief, part 2: deconfound the European native decline

Date 2026-09-28, 01:50 JST. Parent session immigration-research-1c. The operator, after ladder 243: "so which
european countries didn't drop in pisa ... like can we deconfound?"

## What part 1 found (e7471ba)

- Natives' math fell from 2012 to 2022 in almost every European country. Only Sweden (+9.0) and Türkiye (+6.0) rose;
  Montenegro, Lithuania, the UK and Hungary sit within about one SE of zero.
- Countries with little immigration fell as much: Poland (+1.0 pp share, −26.5), Finland (+3.4 pp, −32.6), Iceland
  (+3.9 pp, −32.8) and the Netherlands (+2.7 pp, −22.5).
- The OECD slope is −7.4 points per 10 pp (SE 4.7), with an intercept of −11.7. Closure length is untested, and
  so are exclusion rates. `derived/crosscountry.csv`.

## Tests (bounded; stop and write after each)

1. **Covariates on the cross-country slope** (OECD, and the European subsample separately).
   - Add weeks of full and partial school closure, 2020–2022 (UNESCO's school-closure dataset).
   - Add the change in GDP per head and the change in natives' mean ESCS (the annex tables).
   - Keep the 2012 native level (done: −5.4).
   - Report the slope with each covariate and all jointly, in points per 10 pp, with HC1 SEs and n.
2. **Exclusion and coverage, the "shifty admin" channel in PISA.**
   - Collect the overall exclusion rate and Coverage Index 3, by country, for 2012, 2015, 2018 and 2022. Sources:
     the PISA Technical Reports and the Vol I annex A2 tables.
   - Does the change in exclusion move with the change in immigrant share?
   - Bound each country's native change assuming the excluded pupils would have scored at the 5th or 10th
     percentile.
   - Sweden 2018 case study: verify the reported exclusion rate from primary sources (OECD annex A2, and the
     Skolverket or SCB review), and state what it does to Sweden's 2012→2018 and 2018→2022 native changes.
3. **The regional panel, the main deconfounding design.**
   - Take the adjudicated regions with PISA results in at least two cycles: Spain's communities, Italy's regions
     or macro-areas, the UK's four countries, Belgium's communities, Canada's provinces, Australia's states, and
     any others.
   - Get native (non-immigrant) math and reading and the immigrant share, by region and cycle.
   - Regress the native change on the share change with country × cycle fixed effects, which removes national
     shocks (pandemic policy, curriculum, digital trends). Cluster SEs by region; report per 10 pp and n.
   - If the annex tables do not split natives by region, use the PISA student files (webfs.oecd.org) with plausible
     values and final weights. Check the download size first, and stop and report if it is over 10 GB.
4. **Pre-trends.** Native changes 2006→2012 and 2009→2012 against the later share change. Sources: the PISA 2015
   Vol I annex and PISA 2018 Vol II StatLinks, via `stat.link/files/<doi-suffix>/<id>.xlsx`.
5. **Verdict.**
   - List the European countries whose natives did not drop, with any documented reason: exclusion, reform,
     closure length.
   - Say how much of the native decline survives each control.
   - Say whether the regional design finds an immigration effect on an absolute scale.

## Rules

- Same lane and rules as `BRIEF.md`. Append a section "Deconfounding (part 2)" to `RESULT.md` after each test.
- Scripts are reproducible and write to `derived/`. Raw pulls go in `_cache/`. Two runs must be byte-identical.
- Quote every input in `reads/`; tag every number. Firecrawl is out of credits: use Exa or direct HTTP with a
  generic User-Agent and no personal identifier.
- No commits, staging or stash.
- If the turn cap nears, write what is done and the next queries first.
- Final message: the RESULT path and at most ten lines.

## Addendum (operator, 2026-09-28 01:51): exposure is lagged and cumulative

> "immigrant share isn't new immigrant children ... that takes 6-15 years"

PISA's immigrant share at age 15 is a stock. Its second generation descends from arrivals 15 or more years
earlier, and its first generation includes children who arrived when young. The exposure that could affect a
15-year-old native is their classmates across grades 1–9. Part 1 ran only the contemporaneous share change; the
first-generation share alone gave −2.2 per 10 pp (SE 7.7).

5. **Timing of exposure.** Run this after test 3, or before it if the data are quicker.
   - **Cohort-matched primary-school exposure.** Take immigrant-background shares from TIMSS and PIRLS grade 4
     for the same birth cohorts: PIRLS 2016 and TIMSS 2015 grade 4 are roughly the PISA 2022 cohort (born
     2006); PIRLS 2011 and TIMSS 2011 are roughly PISA 2015–2018. Regress the natives' PISA change on the
     change in grade-4 exposure, and on the average of the grade-4 and age-15 shares.
   - **Recent arrivals separated from settled pupils.** In the PISA student files, age at arrival (ST021, or its
     cycle equivalent) splits the first generation into arrivals within 5 years and earlier ones. Compare the
     share of recent arrivals with the share of settled pupils as regressors.
   - **Germany's 2015–16 wave.** The PISA 2022 cohort met these children from about grade 3–5, and the 2018
     cohort only from grade 7–9. Report whether the first-generation rise (6.5% → 9.2%) sits in the 2022 cohort,
     and what that implies for separating the wave from the pandemic.
   - Report every slope per 10 pp with its SE and n. State which lag structure the data can and cannot
     identify.
