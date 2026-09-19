# Housing does not price the compositional amenity: Saiz–Wachter on 2013–2023 tract data

> **Current status, 2026-09-19:** The historical verdict below is superseded where it calls this an equivalent or failed reproduction. [Original-specification check and new computations](immigration-hedonic-replay-2026-09-19.md) establish different controls, sample rules, outcomes and gravity construction; original-data replay remains pending. Preserve the modern estimates as sensitivity results. They identify neither an amenity price nor the reason the historical estimate differs.

**Verdict:** The within-metro neighbourhood discount that Saiz and Wachter (2011, AEJ: Economic Policy 3(2):169–188) found for 1980–2000, about −2.5% in relative house value per ten-point rise in foreign-born share, does not reproduce on ACS 2013–2018 and 2018–2023 tract data, and no defensible dollar figure for what natives pay to live away from Hispanic or immigrant neighbours comes out of it. The same specification (long differences, CBSA-by-period fixed effects, initial owner-occupied units as weights, 110,000 tract-periods in 381 metros) gives a gradient of the same sign but three to six times smaller, and only on ethnic composition: a ten-point rise in Hispanic share is associated with 0.3–0.8% lower relative values and 0.3–0.6% lower relative rents, while foreign-born share shows nothing, which is the split the original authors themselves predicted. That gradient then fails three checks. Earlier price growth predicts later composition change with the same negative sign (placebo fails, t = −4.5). Treatment and outcome drawn from non-overlapping survey samples give a positive coefficient (+0.067, t = +5.2). And on identical ZIP rows with identical controls, a ten-point Hispanic-share rise is worth −0.96% in ACS median value and +0.84% in Zillow's home value index, so the sign is set by the price source: ACS medians are owner self-assessments and occupant medians that move when occupants change, and they share sampling error with the composition measure. Published margins of error imply four-fifths of the within-metro variance in measured five-year share changes is noise. At the metro level the positive association reproduces: a foreign-born inflow of 1% of metro population goes with rents 1.3% and values 3.4% higher, a descriptive regression with period fixed effects and no instrument. The dollar translation runs from −$979 to +$464 per additional group resident-year depending on the price series, so the compositional amenity stays in the repo as narrative, not as a priced line. [SOURCE: `infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md`, `derived/`] [FRAMING-SENSITIVE: within-metro relative prices partly redistribute across neighbourhoods and between renters and landlords, so they do not by themselves measure a welfare loss, and they price a bundle of school quality, crime and income mix, not a taste for ethnicity]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/hedonic_composition_2026_09_19/`. The lane brief cited the paper as REStat with a wrong DOI; the lane corrected it from the full text (Penn repository copy, pinned in the lane cache).

## 1. What was reproduced

Saiz and Wachter's estimating equation (their p. 173), weighting and clustering were taken from the paper's text and applied to ACS 5-year tract tables on fixed 2010 tract definitions, with period A 2013→2018 and period B 2018→2023, 2013 CBSA delineations, and a calibrated sample keeping the CBSA-periods that hold 76.5% of metro foreign-born growth, the paper's own coverage target. The paper's baseline is −0.246 (se 0.015) per unit of share, IV −0.211 to −0.214, first-stage F 76–362, Hansen not rejecting. [SOURCE: Saiz and Wachter 2011, Table 1, pp. 173–179, quoted in RESULT §1]

## 2. What came back

| Treatment | Rent per +10 pts | Value per +10 pts |
|---|---|---|
| Hispanic share | −0.56% (mean-reversion arm −0.30%) | −0.41% (−0.80%) |
| Mexican-origin share | −0.82% (−0.52%) | −1.05% (−1.39%) |
| Foreign-born share | +0.05% (+0.24%) | +0.46% (+0.21%) |

OLS, calibrated sample, 133 CBSA clusters. [SOURCE: `derived/`, RESULT §2] [CALCULATION] The paper's gravity instrument does not transfer: first-stage F of 0.003 to 8.9 here against 76 to 362 in the paper, because Mexican-born counts in the sample tracts fell 3% over these windows and the enclave-diffusion process it models is not running, and the Hansen test rejects at p < 0.001 in the column-6 form. One exactly identified shift-share arm has a usable first stage, foreign-born share on value with F 38.4, and gives +0.43 (se 0.30), positive and not significant; the Hispanic shift-share is weak (F 1.1), and the Mexican-origin one reduces to a rescaled initial-share exposure instrument, so its validity rests entirely on the exogeneity of initial enclave shares, which the placebo below argues against.

## 3. Why the gradient is not a price

- **Placebo.** Period-A price growth on period-B composition change: Hispanic share on value −0.066 (t = −4.5), Mexican −0.050 (t = −3.8). Groups move into neighbourhoods whose relative prices were already falling.
- **Independent price source.** Same ZCTA rows, same controls, same fixed effects, only the price differing: Hispanic share on value, ACS −0.096 (t = −2.4) against Zillow ZHVI +0.084 (t = +2.8); on rent, ACS −0.351 against ZORI +0.163. ZHVI holds the housing tier fixed; ACS median value is owner self-assessment and median rent is a median over occupants.
- **Non-overlapping samples.** Period-A composition change on period-B price growth, so sampling errors cannot be shared: Hispanic on value +0.067 (t = +5.2).
- **Attenuation.** Reliability of the residualised five-year share change is 0.19–0.23. A classical correction would give −0.254, the paper's number, but the Zillow arm shows the error is correlated with the outcome, so the correction magnifies contamination with signal; neither the small raw nor the large corrected coefficient is credible. [SOURCE: RESULT §3–4] [CALCULATION]

## 4. Metro level

Metro price growth on foreign-born inflow as a share of initial population, 758 metro-periods: rents +1.32% (se 0.42) and values +3.43% (se 0.69) per 1% inflow; Hispanic inflow +0.68% and +2.68%. The rent figure matches the +1.4% the repo carries from Wilson and Zhou 2026 (ladder revisions); the treatments differ (population vs employment inflow). These are descriptive associations without an instrument or local demand-shock control; the point is the level at which the sign is stable, not a causal magnitude. The within-metro composition gradient is below this data's resolution. [SOURCE: RESULT §6] [CALCULATION]

## 5. Dollars

Per additional group resident-year, rent channel plus value channel annualised at 4–6%: Hispanic share −$979 to −$86 on ACS-measured arms, +$303 to +$464 on independently measured arms; Mexican-origin −$955 to −$107 and +$231 to +$396. These are point-estimate scenarios across chosen arms, not a confidence bound, and no arm restricts omitted channels, so the range is not an identified ceiling. The most adverse point sits at about an eighth of the complete common-age fiscal gap of −$7,224 per person-year (ladder 130); the better-measured constructions have the wrong sign for a cost. Card, Dustmann and Preston's finding that compositional concerns carry 2–5× the weight of economic concerns in stated attitudes is not contradicted: attitude weights and revealed prices are different quantities, and most natives are inframarginal to neighbourhood composition, as Saiz and Wachter say themselves (p. 187). [SOURCE: RESULT §7–8] [CALCULATION]

## 6. Limits and what was skipped

Within-metro relative prices net to near zero across a metro and shift between renters and landlords within a tract; the price is for a bundle. Saiz 2010 supply elasticities were not obtainable (a realised quantity-response proxy is used, labelled endogenous); exposure diagnostics were not run because no instrument has a first stage; ZCTA margins of error timed out, so attenuation is tract-level only; the paper's online rent appendix was not consulted. Two acquisition traps recorded: census.gov returned truncated bodies under HTTP 200 and `curl -C -` resumed into a no-op, silently dropping 17 of 56 state codes from the tract relationship file until content was validated; the Zillow ZIP files were fetched intact.

## Sources

Saiz and Wachter 2011, AEJ: Economic Policy 3(2):169–188 (full text); ACS 5-year 2013, 2018, 2023 tract and ZCTA tables via the Census API; Census 2010→2020 tract relationship file; Zillow ZHVI and ZORI ZIP files; Card, Dustmann and Preston 2012, JEEA 10(1):78–119 (abstract and §6 as quoted in the lane brief, not re-fetched by the lane); ladder 130 and the Wilson–Zhou revision entry.

## Revisions

- **2026-09-19 (specification check):** [Decision](../decisions/2026-09-19-require-housing-specification-equivalence.md) withdraws exact-equivalence, established era-change and established measurement-explanation claims. The original appendix uses gravity exponent1.6 and reports negative median-price robustness. New modern comparisons preserve all original estimates and do not substitute for the pending original-data replay.

- **2026-09-19 (same day).** Wording corrected after the peer read-only audit in `notes/immigration-hedonic-audit-evidence-2026-09-19.md` (commit 47f8652): the foreign-born shift-share arm has a strong first stage (F 38.4) and is not rejected, so "every instrument weak or rejected" was wrong; the single-origin shift-share is a rescaled exposure instrument, not a non-instrument; the metro coefficients are associations, not a causal "raises"; the dollar range is a set of point scenarios, not an identified bound; and within-metro relative prices do not prove zero welfare loss. No number changed. Claim change: the lane supplies sensitivity checks and no identified amenity price or upper bound.
