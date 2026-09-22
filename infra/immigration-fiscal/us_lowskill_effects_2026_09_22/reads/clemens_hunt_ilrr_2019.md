<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
# Clemens & Hunt (2019), "The Labor Market Effects of Refugee Waves: Reconciling Conflicting Results", ILR Review

[SOURCE: /Users/alien/Projects/corpus/doi_10_1177_0019793918824597/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md — DOI 10.1177/0019793918824597]

**Note on the parsed text:** the PDF-to-markdown converter renders the minus sign as the
digit `2`. In every verbatim quote below, a leading `2` inside a number is a minus sign
(`20.454` = −0.454, `21.26` = −1.26, `22% to 28%` = −2% to −8%). Quotes are copied exactly
as they appear in the parse so they can be re-found with `rg`; the interpreted value is
given in the estimate column.

**Verdict:** This is a methodological reconciliation paper, not a new natural experiment: it
shows that Borjas's (2017) large negative Mariel wage effect coincides with an unrelated
tripling of the black share of his 17-observation-per-year subsample, and that Borjas and
Monras's (2017) instrumental-variables results for Israel, France and Europe reproduce with
a pure white-noise placebo instrument because instrument and endogenous variable share a
common divisor; the design is strong as a replication/falsification exercise (exact
replications plus placebo and Kronmal corrections on the original data and code) but it
identifies no new causal effect of its own.

## Population, period, unit

Four refugee episodes, reanalysed on the original authors' data:

- **Mariel Boatlift, Miami 1980.** CPS March Supplement and May/MORG extracts, survey years
  1977–1990 (earnings years 1976–1989). Unit for the headline regressions is the city-year
  (N = 75). Borjas's subsample: employed non-Hispanic males age 25–59 with less than high
  school. Card's: non-Cuban workers age 19–65 with high school or less. Control cities are
  Card's (Atlanta, Los Angeles, Houston, Tampa-St. Petersburg) or Borjas's (Anaheim,
  Rochester, Nassau-Suffolk, San Jose).
- **Soviet Jews to Israel, 1990–1994.** Education-by-occupation cells; N = 32 in the Borjas-
  Monras specification, N = 8,353 individuals in the Friedberg specification.
- **French repatriates from Algeria, 1962.** 88 French departments (Hunt) or region-education
  cells (Borjas-Monras); outcome is the 1962–1968 change in native unemployment. N = 88.
- **Yugoslav/Balkan refugees across Europe, 1990s.** Seven countries in the Borjas-Monras
  reanalysis (Austria, Greece, Ireland, Portugal, Romania, Spain, Switzerland), country-by-
  education cells, N = 195.

## Design and identification

**Mariel.** No instrument. Difference-in-differences at the city-year level with pre-treatment
period 1977–79 and 1980 dropped; the authors' contribution is to add a black indicator to the
individual-level first-stage wage adjustment, at three levels of flexibility (one nationwide
coefficient, one per city, one per city for the less-than-high-school group), and to show
what happens to Borjas's coefficients. They also document the composition shift directly in
sample counts (Table 1) and in scatterplots of black share against mean wage (Figure 3).

**The other three episodes.** All use the Altonji-Card prior-migration instrument as applied by
Borjas and Monras: current refugee shock over cell population, instrumented by lagged migrant
stock over the same cell population. Clemens and Hunt run two tests. (1) A **placebo
instrument**: replace the instrument's numerator with Poisson white noise of the same mean,
keep the same divisor. (2) The **Kronmal (1993) correction** adapted to IV: split the ratio
into numerator and denominator as separate regressors under an inverse hyperbolic sine
transform, instrument the numerator alone with the lagged absolute stock. First-stage strength
is reported throughout as Kleibergen-Paap F, and inference uses the weak-instrument-robust
Anderson-Rubin F-test, which is the correct test in this just-identified setting.

The stated mechanism of the spurious result is Pearson's (1896) common-divisor problem: because
native cell population barely changes over the window, instrument and endogenous variable share
a nearly identical denominator, so they correlate by construction.

## Headline estimates

Minus signs appear as `2` in the quote column (see the note above).

### Mariel: the composition shift

| Outcome | Estimate | SE or precision | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Size of the Mariel supply shock | +7% of Miami labor supply | — | p. 2 | "raised the labor supply in Miami, Florida, by 7%" |
| Borjas's reported wage effect (the claim being reconciled) | −10% to −30% | — | p. 3 | "found that the Boatlift caused the wages of males in this latter subgroup to fall ''dramatically, by 10 to 30%,''" |
| Black share of Borjas's Miami <HS sample, March CPS, survey year 1979 | 0.363 | 8 black / 14 non-black | Table 1, p. 9 | "1979 8 14 0.363 0.304 0.135 0.442" |
| Black share of the same sample, survey year 1985 | 0.910 | 14 black / 2 non-black | Table 1, p. 9 | "1985 14 2 0.910 0.276 0.180 0.541" |
| Change in black share 1979→1985, March CPS | roughly tripled, +55 pp | — | p. 9 | "the fraction of black workers roughly tripled between the survey conducted in 1979 and the survey in 1985, rising 55 percentage points" |
| Same change in the May/ORG extract | about one third as large | — | p. 9 | "The increase in the May/ORG was roughly one-third as large, with the main increase in 1985." |
| Borjas subsample size, 1983–1987 | ~17 obs/year; 91% of low-skill Miami workers dropped | avg 185/yr available | p. 8 | "This leaves an average of 17 observations per year during the period in which he found the largest effect (1983–1987); that is, he omitted 91% of the observations of low-skill workers in Miami" |
| Implied compositional wage change for black <HS men from the Haitian inflow alone | −0.25 log points | arithmetic from source counts | p. 10 | "This would produce a purely compositional change in earnings for black men with less than high school of 20.25 log points." |
| Implied compositional effect on the whole <HS sample | at least −0.17 log points | — | p. 10 | "the compositional effect on the wages of the whole sample would be on the order of at least 20.17 log points" |
| Haitian vs incumbent weekly earnings, black <HS men in Miami | $105 vs $263 per week | 1983–84 vs 1977–79 | p. 10 | "Individual earnings for typical newly arrived, employed Haitian workers were $105 per week in 1983–1984 ... compared to $263 for the Borjas March CPS subpopulation" |
| Black–non-black log wage gap, Miami <HS men | −0.487 | (0.0737) | Table 3, p. 15 | "Black 20.487*** 20.465*** 20.219*** 20.215*** 20.285*** 20.261***" |
| Black–non-black unemployment gap, Miami <HS men | −0.0048, not significant | (0.0320) | Table 3, p. 15 | "Black 20.00480 20.00345 0.0688*** 0.0513*** 0.0528*** 0.0515***" |

### Mariel: what happens to the Borjas estimate when composition is controlled

March CPS extract, Table 2a (p. 11), dependent variable log weekly real wage, N = 75 city-years.
Columns run: exact replication, black indicator nationwide, black indicator by city, black
indicator by city for the less-than-high-school group. Each pair is Card controls then Borjas
controls.

| Outcome | Estimate | SE | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| 1981–83, exact replication of Borjas | −0.204 (Card ctrl), −0.290 (Borjas ctrl) | (0.076), (0.073) | Table 2a, p. 11 | "1981–83 20.204*** 20.290*** 20.121 20.194*** 20.096 20.174** 0.001 20.078" |
| 1981–83, black indicator nationwide | −0.121 (ns), −0.194 | (0.078), (0.070) | Table 2a, p. 11 | same row as above |
| 1981–83, black indicator by city | −0.096 (ns), −0.174 | (0.081), (0.072) | Table 2a, p. 11 | same row as above |
| 1981–83, black indicator by city × <HS | +0.001 (ns), −0.078 (ns) | (0.062), (0.061) | Table 2a, p. 11 | same row as above |
| 1984–86, exact replication (peak effect) | −0.368, −0.454 | (0.060), (0.059) | Table 2a, p. 11 | "1984–86 20.368*** 20.454*** 20.202*** 20.301*** 20.137 20.227*** 0.109* 20.001" |
| 1984–86, black indicator nationwide | −0.202, −0.301 | (0.072), (0.053) | Table 2a, p. 11 | same row as above |
| 1984–86, black indicator by city | −0.137 (ns), −0.227 | (0.083), (0.058) | Table 2a, p. 11 | same row as above |
| 1984–86, black indicator by city × <HS | +0.109 (p<0.10), −0.001 (ns) | (0.063), (0.059) | Table 2a, p. 11 | same row as above |
| 1987–89, exact replication | −0.329, −0.303 | (0.081), (0.072) | Table 2a, p. 11 | "1987–89 20.329*** 20.303*** 20.202** 20.237*** 20.135 20.149** 20.025 20.049" |
| May/ORG extract, 1981–83, exact replication | −0.075, −0.140 | (0.026), (0.049) | Table 2b, p. 11 | "1981–83 20.075*** 20.140*** 20.047 20.104** 0.005 20.056 0.036 20.025" |
| May/ORG, 1981–83, black indicator by city | +0.005 (ns), −0.056 (ns) | (0.034), (0.040) | Table 2b, p. 11 | same row as above |
| May/ORG, 1987–89, exact replication | −0.106, −0.175 | (0.036), (0.064) | Table 2b, p. 11 | "1987–89 20.106*** 20.175*** 20.074* 20.137** 20.046 20.101 0.051 0.015" |
| Effect of moving to the by-city black indicator (March CPS) | attenuation of more than half; no longer significant vs Card controls | — | p. 15 | "The treatment effect is more heavily attenuated—by more than half of its original value—and is no longer statistically significant relative to the control cities preferred by Card." |
| Effect of the nationwide black indicator | about one third smaller | — | p. 14 | "This change reduces the magnitude of the treatment effect by approximately one-third." |
| Non-blacks-only sample size, 1983–87 | ~4 observations per year; >98% of the low-skill sample discarded | — | p. 16 | "an average of only four observations per year in the years when Borjas finds the largest treatment effect (1983–1987, see Table 1) ... more than 98% of the original sample of low-skill workers has been discarded" |
| **Authors' surviving range for Mariel <HS men** | **−2% to −8%, or zero** | not statistically significant | p. 17 and fn. 17 | "compatible with a model in which the Mariel Boatlift caused a modest fall in the wages of this subpopulation of roughly 22% to 28% in the few years immediately after the Boatlift, but it is also compatible with a model in which this effect was zero" |
| Largest surviving (composition-adjusted) coefficient | −8% March CPS, −2% May/ORG, none significant | — | fn. 17, p. 17 | "The coefficient estimate in Table 2a, column (8), row 1981–83 is –8%. ... The corresponding coefficient in Table 2b is –2%. ... None of the coefficients is statistically significant." |
| Wage change for Miami low-skill workers with exactly high school | about +30% to +40% vs pre-trend | significant | Figure 2d, p. 7 | "a large and statistically significant rise is seen in wages relative to the pre-trend (about + 30–40%) and relative to" |
| Wage change for Miami low-skill workers with less than high school (Peri-Yasenov definition) | about −10% to −20%, significant in 1982 only | imprecise | Figure 2e, p. 8 | "there may be a short-lived fall (about 210 to 220%) in wages relative to the pre-trend and the Borjas control cities—but it is not statistically precise (both are significant in 1982 only)" |
| Wage change in the Borjas subsample (Figure 2f) | about −30% to −50% | — | Figure 2f, p. 8 | "In Borjas’s subgroup, there is a large fall in Miami wages (about 230 to 250%) that lasted several years after 1980" |
| Association between black share and mean wage in the Borjas sample | doubling of black share ≈ −40% wage; log wage 5.6 → 5.1 | least-squares fit | Figure 3a, p. 13 | "The doubling of the black fraction between the pre-Boatlift years and the post-Boatlift years is associated with approximately a 40% decline in the average wage (the log weekly wage falls from about 5.6 to 5.1, that is, from $270 to $164)." |

Borjas and Monras's separate Mariel city-skill IV result rests on one cell. Table 13 itself is
missing from this parse (page 34 is not in the extracted text), so no numbers from it are
reported here; the text describing it is quotable: "the entire result in Borjas and Monras’s
city-skill cell regressions depends on a single cell: workers with less than high school in
Miami" (p. 33), and the Hispanic-only version has "a p value of 0.76" with "Kleibergen-Paap F
statistic of 1965" (p. 33).

### Israel (Soviet Jews, 1990–1994)

| Outcome | Estimate | SE | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Size of the shock | +12% of Israel's population | — | p. 20 | "an influx large enough to raise Israel's population by 12%" |
| Borjas-Monras IV, émigré supply shock on native wage (real instrument) | −0.616 (p<0.10) | (0.316) | Table 4b col 1 / Table 5 col 1, pp. 20, 22 | "E [´] migre´ supply shock/population 20.616* 20.820*** 20.611* 20.873*" |
| Same specification with a **white-noise placebo** instrument | −0.820, more significant than the original | (0.315) | Table 4b col 2, p. 20 | same row as above |
| Kleibergen-Paap F, real vs placebo instrument | 27.37 vs 5.059 | — | Table 4b, p. 20 | "Kleibergen-Paap F 27.37 5.059 23.19 3.728" |
| Kronmal-corrected coefficient on the absolute émigré shock | −0.0348, not significant; adjusted −0.284 | (0.0443) | Table 5 col 3, p. 22 | "asinh e´migre´ supply shock 20.0348" |
| Anderson-Rubin p-value, Kronmal specification | 0.548 (cannot reject zero) | K-P F 14.41 | Table 5, p. 22 | "p value Anderson-Rubin F-test 0.0985 0.0995 0.548" |
| Share of refugee-shock variance explained by cell size | 72%, regression coefficient 1.15 | (0.196) | Table 5 col 4, p. 22 | "The coefficient of 1.15 is indistinguishable from unity, and 72% of the variance in the size of the refugee supply shock is explained simply by the size of the native population in each education-occupation cell." |
| Friedberg's original IV, native wage | +0.718 (p<0.10 in Table 4b/6b, p<0.05 in Table 7) | (0.339) | Table 6b col 1 / Table 7 col 1, pp. 24, 24 | "E [´] migre´ supply shock/population (‘r’) 0.718* 0.402" |
| Friedberg's result under the placebo instrument | +0.402, not significant (the placebo **fails**) | (0.807) | Table 6b col 2, p. 24 | same row as above |
| Friedberg under the Kronmal correction | +0.0780, ns; adjusted +0.572 | (0.0666) | Table 7 col 3, p. 24 | "asinh e´migre´s in cell, 1994 0.0780" |

### France (repatriates from Algeria, 1962)

| Outcome | Estimate | SE | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Size of the inflow | 900,000 Europeans plus ~140,000 Muslim "Harkis"; repatriates = 1.6% of the 1968 labor force | — | pp. 25, 25 | "the arrival from Algeria in 1962 of 900,000 people of European (and Jewish) origin"; "the repatriates represented 1.6% of the 1968 labor force" |
| Hunt (1992) original: 1 pp more repatriates in the labor force → native unemployment | +0.19 pp; total effect "at most 0.3 percentage points" | 0.195, (0.080) | Table 10 col 1, p. 30, and p. 25 | "she found that the arrival of the repatriates raised French native unemployment by ''at most 0.3 percentage points.''" |
| Hunt's coefficient, replicated with robust SEs | 0.195 (p<0.05), transformed 0.189 | (0.080) | Table 10 col 1, p. 30 | "Repatriate share 0.195**" |
| Hunt re-estimated with the temperature instrument only | 0.120, not significant; upper bound 0.31 pp | (0.096) | Table 10 col 2, p. 28 | "The coefficient drops to 0.120 with a slightly larger standard error, which renders the coefficient statistically insignificant. Nevertheless, we can rule out that a percentage point increase in repatriate's share in the population increases unemployment by more than 0.31 percentage point." |
| Hunt under the Kronmal correction | 0.00254 (p<0.01); transformed 0.156 pp per 1% labor-force increase | (0.00117) | Table 10 col 5, p. 30 | "asinh number of repatriates 1968 - - - - 0.00254***" |
| Borjas-Monras: 1% population increase from repatriates → native unemployment | +0.0887 pp (p<0.05) | (0.0384) | Table 8b col 1, p. 27 | "Repatriate supply shock/population 0.0887** 0.04888" |
| Borjas-Monras: 1% population increase from Algerian nationals → native unemployment | +0.247 pp (p<0.01) | (0.0667) | Table 8b col 1, p. 27 | "Algerian supply shock/population 0.247*** 0.419*** 0.282*** 0.437*** 0.443***" |
| Same, with the **placebo** instrument | +0.419 to +0.443, still highly significant (effect grows) | (0.126), (0.118) | Table 8b cols 2, 4, 5, p. 27 | same row as above |
| Kleibergen-Paap F, real vs placebo, France | 54.23 / 247.7 vs 2.440 / 5.285 | — | Table 8b, p. 27 | "Kleibergen-Paap F 54.23 2.440 247.7 5.285 5.116" |
| Kronmal-corrected Algerian shock coefficient | 0.00182 (p<0.05), transformed 0.226 pp | (0.000904) | Table 9 col 4, p. 29 | "asinh Algerian supply shock 0.00234*** 0.00182**" |
| Kronmal-corrected repatriate shock coefficient | 0.00151, not significant; transformed 0.044 | (0.00249) | Table 9 col 4, p. 29 | "asinh repatriate supply shock 0.00151" |
| Authors' France conclusion | 1% population rise from Algerians → 0.23–0.24 pp unemployment, in all specifications | — | p. 28 | "both Borjas and Monras and Table 9 imply that if Algerians increase the population by 1%, unemployment rises by 0.23–0.24 percentage point." |
| Share of Algerian-shock variance explained by cell size | 81% | — | fn. 30, p. 28 | "Of the variance in the refugee shock, 81% is explained by the size of the cell." |

### Europe (Balkan refugees, 1990s)

| Outcome | Estimate | SE | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Angrist-Kugler (2003) original | +1 pp migrant stock → +0.83 pp native unemployment | — | p. 30 | "They found that a sudden increase in the migrant stock of one percentage point raises native unemployment by 0.83 percentage point." |
| Borjas-Monras reanalysis | +0.49 pp (their text); 0.456, not significant in the replication | (0.311) | p. 31 and Table 11b col 1, p. 31 | "An increase in the migrant stock of one percentage point raises native unemployment by 0.49 percentage points."; "Balkan supply shock/population 0.456 0.583* 0.487 0.657" |
| Same with the **placebo** instrument | 0.583 (p<0.10), i.e. stronger than the original | (0.323) | Table 11b col 2, p. 31 | same row as above |
| Kronmal-corrected Balkan shock | −0.0132, not significant; adjusted −0.26 (sign flips) | (0.0119) | Table 12 col 3, p. 32 | "asinh Balkan supply shock 20.0132" |
| First-stage strength under the correction | Kleibergen-Paap F = 1.498 (weak) | — | Table 12, p. 32 | "Instrumentation is quite weak, with a Kleibergen-Paap F statistic of just 1.5." |

### Cross-episode summary (Table 14, p. 35)

| Episode and outcome | Borjas-Monras coefficient (Panel B) | Kronmal-corrected, comparable units (Panel C) | Verbatim quote (≤40 words) |
|---|---|---|---|
| Miami wage | −1.26 (p<0.05) | +0.005 (ns) | "B. Borjas and Monras (BM) (2017) 21.26** 20.62* 0.09** 0.25** 0.46" |
| Israel wage | −0.62 (p<0.10) | −0.28 (ns); Friedberg route +0.57 | same row as above; "Borjas and Monras 0.005 20.28 0.04 0.23** 20.26" |
| France unemployment, repatriates | +0.09 (p<0.05) | +0.04 (ns); Hunt route +0.16 (p<0.05) | "Borjas and Monras 0.005 20.28 0.04 0.23** 20.26" |
| France unemployment, Algerians | +0.25 (p<0.05) | +0.23 (p<0.05) — the one survivor | same rows as above |
| Europe unemployment | +0.46 (ns) | −0.26 (ns) | same rows as above |
| Authors' reading of the table | only France survives; Miami and Europe show nothing; Israel bounded between −0.3% and +0.5–0.7% | — | "The important exception is the case of France, which robustly shows that a 1% rise in population due to refugees caused a 0.2 percentage point rise in unemployment (columns (3)–(4)). The cases of Miami and Europe show no deleterious effects" |

## What it says about

**Native wages by skill/education.** This is the paper's core. For workers with high school or
less (Card's group) there is no negative effect; for workers with exactly high school there is
a large positive movement relative to pre-trend; for workers with less than high school the
apparent large negative effect is attributed to sample composition. The paper's own summary for
the less-than-high-school group is the closing sentence: "Evidence does not support claims of
large detrimental impacts on workers with less than high school education." The residual range
they will not rule out is −2% to −8% for prime-age non-Hispanic <HS men in Miami in the first
few post-Boatlift years, statistically indistinguishable from zero. For Israel, the corrected
estimate is bounded as "at worst a 1% rise in population due to refugees reduced wages by 0.3%
but may also have raised wages by 0.5–0.7%".

They also flag as a puzzle that the effect is absent for Hispanics: "No reanalysis of the
Mariel Boatlift finds negative wage impacts for samples that include non-Cuban Hispanics, nor
is there a negative wage impact for non-Cuban Hispanics separately" (p. 4), and that Borjas's
own 1987 national-census work found Cuban immigrants to be complements: "Cubans have not had an
adverse impact on the earnings of any of the native-born male groups." (fn. 5, p. 4).

**Native employment / crowd-out.** Mariel: no effect on unemployment, agreed by every study
including Borjas and Monras. Their explanation is mechanical — the black/non-black unemployment
gap in the Miami <HS sample is essentially zero (−0.0048, ns) even though the wage gap is −0.487,
so a composition shift moves measured wages but not measured unemployment. France: a real and
robust positive effect on native unemployment, roughly 0.16–0.23 pp per 1% population increase
depending on which shock and which specification. Europe: unstable and statistically
insignificant, sign flips under correction. Israel: employment not studied in the reanalysis
(the Israel reanalysis has wage but not employment; the France reanalysis has employment but
not wage).

**Housing prices, rents.** Not studied.

**Fiscal: taxes, transfers, public services, schooling.** Not studied. The only fiscal-adjacent
fact is incidental: ethnographers found that some blacks had been concealed from surveyors "in
order to preserve welfare benefits" (p. 12), which is offered as a survey-coverage mechanism,
not a fiscal finding.

**Firms, production, investment, profits.** Not studied. No production function is estimated
and no capital adjustment channel is modelled.

**Mechanism the authors claim.** Two, one per half of the paper. (1) For Mariel, a
composition-driven measurement artifact: a sharp post-1980 rise in the black share of a very
small CPS subsample, caused by the 1980 Haitian inflow, by post-Levitan-Commission census and
CPS efforts to reduce undercount of low-income black men, and by negative selection among the
newly covered. Since black <HS men in Miami earned about 0.49 log points less, the measured
mean wage falls without any true wage change. (2) For the IV studies, Pearson's common-divisor
spurious correlation: "This similarity is a consequence of spurious correlation between the
instrument and the endogenous variable introduced by applying a common divisor to both."

## Elasticities or parameters a model could transport

These are reduced-form coefficients, not structural elasticities. The paper estimates no
elasticity of substitution and no production function, so it supplies **no parameter that can be
plugged into a nested-CES production term.** What it does supply is a set of upper bounds on
reduced-form wage and displacement responses, plus one structural-ish claim borrowed from
elsewhere.

1. **Wage response of low-education natives to a large, sudden, low-skill labor supply shock,
   city level.** Mariel, Miami, prime-age non-Hispanic male workers with less than high school,
   CPS 1977–1990: between −8% and 0 in the first few post-Boatlift years, not statistically
   distinguishable from zero, against a 7% labor-supply shock. That implies an implied wage
   elasticity with respect to the supply shock of roughly −1.1 to 0 at the extreme upper bound
   of the surviving range, and zero as the central reading.
2. **Wage response, occupation-cell level, Israel.** Per 1% population increase from refugees:
   between −0.3% and +0.7% depending on which original instrument is used. Estimated on Israeli
   natives across education-by-occupation cells, 1989–1994.
3. **Unemployment response to a refugee inflow, region level, France.** +0.16 to +0.23
   percentage points of native unemployment per 1% increase in population or labor force,
   estimated on French departments/regions 1962–1968, on natives of similar education. This is
   the one estimate the authors call robust. Note it is an unemployment response, not a wage
   response, and the labor-market institutions are 1960s France.
4. **Unemployment response, Europe, 1990s.** Not identified; the corrected point estimate is
   −0.26 with a weak first stage. Treat as uninformative.
5. **Black–non-black log wage gap among <HS men, by city, March CPS 1977–1986.** Miami −0.487
   (0.0737), Card control cities −0.219 (0.0315), Borjas control cities −0.285 (0.0760). Useful
   only as a composition-adjustment input, and the authors stress it varies by city and skill.
6. **A cited, not estimated, substitution claim.** The authors lean on Card (2009) for the
   premise that "Workers with high school only and less than high school are close substitutes
   in the US labor market", which is what makes the Borjas pattern (nothing for HS, large effect
   for <HS, despite Mariel migrants being roughly evenly split between the two) hard to
   rationalize. If a model puts natives with less than high school and natives with exactly high
   school in separate cells, this paper is an argument against that partition.

## Authors' stated limitations and external-validity notes

- The direct test — drop blacks and re-run — is impossible. "the already small size of the
  samples makes this approach impossible in practice", leaving about four observations per year.
  So the paper cannot positively establish a zero effect for non-blacks; it can only show that
  the Borjas estimate does not survive plausible composition controls.
- Controlling for a black indicator specific to the <HS group in each city also controls away any
  genuine differential effect of the Boatlift on black <HS workers. The authors say so: these
  columns have "the disadvantage of controlling away any additional effect that the Mariel
  Boatlift might have had on the wages of blacks".
- The surviving Mariel range is explicitly two-sided: modest negative or zero, not established
  zero.
- Placebo robustness is not proof of a false result. "Robustness to this placebo substitution
  does not invalidate the result, but it does show that the result requires further scrutiny".
- The CPS before 1994 does not record country of birth, so "natives" is an inference throughout;
  Haitian and US-born blacks are indistinguishable in the data.
- The Borjas-Monras French data identify neither repatriates nor Harkis directly; the imputation
  "identifies 1.4 million repatriates, more than 50% too many".
- The authors do not test sensitivity to excluding women: "We do not investigate the sensitivity
  of the results to the exclusion of women", noting Borjas's own mixed-sex results are one-half
  to two-thirds the size of the male-only ones.
- Cross-episode transport is weak by construction: four episodes, four different institutional
  settings, three different outcome variables, and the one robust effect (France 1962
  unemployment) sits in a labor market with different institutions from the US.
- The Kronmal correction's bite is specification-dependent: it matters most "when serial
  correlation in the denominators ... is highest relative to serial correlation in the
  numerators", which is an empirical property of each application.

## Data availability

No public replication package is announced in the article text. The stated route is direct
contact with the corresponding author: "For information regarding the data and/or computer
programs used for this study, please contact mclemens@cgdev.org." An Online Appendix is public
at http://journals.sagepub.com/doi/suppl/10.1177/0019793918824597 and carries the CPS sampling-
procedure discussion, the proof of the coefficient-comparability adjustment, the
lnð1+xÞ-versus-asinh invariance check, the serial-correlation analysis, and the placebo/Kronmal
analysis for the Hispanic-only Mariel case. The underlying inputs are public or author-supplied:
IPUMS CPS and the 1980 census 5% sample, and the authors thank "the IPUMS project and to Rachel
Friedberg, George Borjas, and Joan Monras for making data and code available to researchers."

**One gap in this parse:** Table 13 (Borjas-Monras Mariel city-skill IV, the single-cell
sensitivity and the Hispanic-only column) is absent from the extracted text — the parse skips
from page 33 to the page-35 header. The surrounding prose is intact and quoted above, but the
Table 13 coefficients themselves are not reported here.

## Verification

All 62 numeric table rows above were checked with `rg -F` against the parsed paper, using 81
distinct verbatim fragments (table-row strings, coefficient strings and prose sentences).

- **81 of 81 fragments re-found. 0 misses. 0 rows dropped.**
- Because the parse hard-wraps prose, quotes that span a line break were matched against a
  whitespace-flattened copy of the same file (`tr '\n' ' ' | tr -s ' '`). Table-row and
  coefficient strings were matched against the raw file directly.
- Two quotes initially missed on a straight-apostrophe-versus-curly-apostrophe mismatch and
  were corrected to the paper's characters, then re-verified: "In Borjas’s subgroup…" and
  "…Borjas and Monras’s city-skill cell regressions…".
- Table 13 contributes no numeric rows because that table is absent from this parse.
