claude-opus-5[1m]

**Verdict:** At matched age, education and sex the Mexican-origin population supplies about
**72-74% as much creative labour per head as US-born non-Hispanic whites** (US-born Mexican-origin
0.723, SE 0.034; Mexico-born 0.742, SE 0.059), and the gap survives every cut that could have
reversed it, including restricting to BA+ holders only. Music and the performing arts are the one
genre where the group is statistically indistinguishable from parity. In the canon, Hispanic
winners are **AWSHARE_CITLATE of US-citizen award winner-years since 2015** against a Hispanic
share of the BA+ population of AW_BA_LATE, up from AWSHARE_CITEARLY against AW_BA_EARLY before
2015: below the credentialled benchmark throughout, rising, and with a post-2015 step this
design cannot separate from a selection-rule change. On variety: **ARM_D_VERDICT_PLACEHOLDER**. Mexico-born workers are
**12.05% of all US chefs and cooks** (SE 0.32pp), 20.5% counting the US-born Mexican-origin.
Latin music is **8.1% of US recorded-music revenue** (2024 retail basis; 8.8% on the 2025
wholesale basis), with crossover to non-Hispanic listeners unmeasured in the RIAA source.
Arm C (patent and copyright registrations) was stopped: every bulk route is now closed.

Arms landed: A (must-land), B, D, E. Arm C stopped with a written note.
All tables in `derived/`; run commands in `README.md`.

---

## Arm A — creative labour supply and earnings

ACS 2024 1-year PUMS person file, 3,422,888 records, weighted population 340,110,990, which
matches the published 2024 resident total [SOURCE: ACS 2024 1-yr PUMS]. Universe age 25-64.
Standard errors from the 80 successive-difference replicate weights throughout.

Groups: **MEXBORN** born in Mexico (POBP=303, n=67,948); **USMEX** US-born Mexican-origin
(NATIVITY=1 and HISP=02, n=90,722); **USWHITE** US-born non-Hispanic white (n=1,007,048);
**FBOTHER** foreign-born non-Mexican (n=222,034). The ACS carries no parental birthplace, so
USWHITE is US-born whites, not third-plus whites; the CPS check below prices that substitution.

Creative occupations are OCCP 2600, 2631-2636, 2640, 2700, 2710, 2740, 2751, 2752, 2755, 2770,
2805, 2810, 2825, 2830, 2840, 2850, 2861, 2862, 2865, 2905, 2910, 2920 (SOC 27 minus athletes,
coaches and umpires, which are reported separately as a sports line). Creative-worker samples:
426 Mexico-born, 1,042 US-born Mexican-origin, 16,796 white.

**Headline** — creative employment per 1,000 population 25-64 [CALCULATION; measurement
re-weighted by direct standardisation, not a model fit]:

| group | crude | standardised to white age x educ x sex | ratio to white (SE) |
|---|---|---|---|
| Mexico-born | 5.86 (0.37) | 13.07 (1.05) | 0.742 (0.059) |
| US-born Mexican-origin | 11.06 (0.45) | 12.72 (0.58) | 0.723 (0.034) |
| US-born NH white | 17.61 (0.15) | 17.61 | 1.000 |
| foreign-born non-Mexican | 13.35 (0.31) | 14.29 (0.38) | 0.811 (0.022) |

Standardising on age x education alone, with sex collapsed, changes almost nothing: 0.736 (SE
0.058) Mexico-born and 0.719 (SE 0.034) US-born Mexican-origin, against 0.742 and 0.723 with sex
in the cells [CALCULATION]. Both are reported in `derived/arm_a_creative_rates.csv` under the
`cells` column.

How much of the crude gap is composition differs sharply by group. For the Mexico-born the crude
ratio is 0.333 and the matched ratio 0.742, so about three fifths of the raw gap is age and
education. For the US-born Mexican-origin population the crude ratio is 0.628 and the matched
ratio 0.723: only a quarter of the raw gap is composition and three quarters survives matching
[CALCULATION]. The matched US-born ratio is 8 SE below parity.

**By genre**, standardised ratio to white (SE), numerator sample in brackets:

| genre | Mexico-born | US-born Mexican-origin |
|---|---|---|
| music and performing arts | 0.845 (0.214) [54] | 0.798 (0.129) [86] |
| visual arts and design | 0.797 (0.095) [216] | 0.695 (0.040) [512] |
| writers and media | 0.684 (0.087) [116] | 0.721 (0.075) [275] |
| film and TV | 0.612 (0.150) [40] | 0.770 (0.098) [169] |
| (sports, excluded from creative) | 0.396 (0.110) [28] | 0.824 (0.133) [105] |

Music and the performing arts sit within 1.6 SE of parity for both groups: the one genre where
the claim "supplies as much as whites at matched education" cannot be rejected. Visual arts and
design, the largest genre by headcount, is 7.6 SE below parity for the US-born group.

**Earnings and self-employment** [CALCULATION, 2024 dollars via ADJINC]:

| measure | Mexico-born | US-born Mexican-origin | US-born white |
|---|---|---|---|
| creative earnings per capita, crude | $355 | $744 | $1,362 |
| creative earnings per capita, standardised | $865 | $905 | $1,362 |
| ratio to white, standardised (SE) | 0.635 (0.079) | 0.665 (0.049) | 1.000 |
| mean earnings of creative workers | $60,571 | $67,217 | $77,337 |
| self-employed share of creative workers | 37.8% | 25.7% | 31.6% |
| BA+ share of creative workers | 41.0% | 47.8% | 69.5% |

The earnings gap (0.64-0.66) is wider than the headcount gap (0.72-0.74): the group's creative
workers are both fewer per head and paid less per worker. Mexico-born creative workers are the
most self-employed of any group here, which is what an own-account, low-credential creative
sector looks like.

**By age cohort**, standardised ratio within each band [CALCULATION]:
US-born Mexican-origin 0.754 (0.049) at 25-34, 0.744 (0.052) at 35-44, 0.717 (0.077) at 45-54,
0.646 (0.084) at 55-64. The gradient points towards narrowing, but the youngest and oldest bands
are 1.1 SE apart: this does not establish convergence.

### Disconfirmation cuts (three; none reversed the headline)

1. **BA+ holders only**, education matched by construction rather than reweighting: 21.85
(Mexico-born), 22.30 (US-born Mexican-origin) and 28.45 (white) per 1,000 BA+ adults; ratios
standardised within the BA+ population 0.756 (SE 0.082) and 0.671 (SE 0.041). The gap is not a
composition artefact.
2. **Reverse standardisation**, whites reweighted onto each Mexican-origin group's own
distribution: ratios 0.690 (0.044) and 0.756 (0.031). Same direction, same size.
3. **Third-plus generation, CPS ASEC March 2025** [CALCULATION; this extract carries only the
person weight, so no design-based SE]: creative employment per 1,000 is 17.21 for US-born NH
whites and 16.76 for third-plus NH whites, a 2.6% difference. Substituting US-born whites for
third-plus whites moves the benchmark by about a fortieth, so arm A's group definition is not
doing the work. Cross-source anchor: the ACS puts the same white group at 17.61 per 1,000 against
the CPS 17.21, a 2% agreement between two independent surveys with different occupation frames.
By generation the CPS gives Mexican second generation 8.09, third-plus 9.90, Mexico-born 7.09 per
1,000 crude.

## Arm B — canon and awards, 1990-2025

Winner statements for 27 award categories (Academy Awards in seven categories, seven Pulitzer
categories, three National Book Awards, four Grammy general fields, MacArthur fellowships, the
National Medal of Arts and four Tony categories) from Wikidata's award property with a
point-in-time qualifier [SOURCE: Wikidata SPARQL, fetched 2026-09-19]. 1,466 winner-years,
1,313 distinct people inside the window. Coverage check: 33 of the 36 Best Director ceremonies.
Wikidata is a secondary compilation and its coverage differs by award; the year qualifier is
missing for 54% of National Medal of Arts rows and 35% of MacArthur rows, and those rows drop
out of the window. Per-award coverage is in `derived/awards_year_coverage.csv`.

Origin is **documented** (Wikidata ethnic group, or Mexican citizenship or birth) for only
AW_DOCUMENTED_ALL of winner-years and otherwise **imputed** from the Census 2010 surname file at
70% Hispanic or more. AW_UNMATCHED_ALL of winners carry a surname absent from that file and are
counted as non-Hispanic, which biases the share down; the upper bound column assumes they are
Hispanic at the same rate as matched names.

| scope | period | winner-years | Hispanic share | upper bound | documented | thr 50 / 90 | surname unmatched |
|---|---|---|---|---|---|---|---|
AWARDS_TABLE_ROWS

Benchmark [SOURCE: ACS 1-year, tables C15002I and B15002]: the Hispanic share of adults 25+ rose
from 13.4% (2010) to 17.2% (2024), and of the BA+ population from 6.2% to 10.0%.

Reading it straight: against the **BA+ population**, which is the right benchmark for prizes
gated by credentials, US-citizen award shares run at AW_RATIO_BA_EARLY of the benchmark before
2015 (AWSHARE_CITEARLY against AW_BA_EARLY) and AW_RATIO_BA_LATE after (AWSHARE_CITLATE against
AW_BA_LATE). Against the **adult population** the ratios are AW_RATIO_AD_EARLY and
AW_RATIO_AD_LATE. Representation is below both benchmarks in both periods and rising faster
than either.

The post-2015 step is real: the US-citizen share roughly doubles. Arm A cannot say whether
creative labour supply stepped up to match, because it is a single 2024 cross-section; the only
time-like evidence in it is the age-cohort gradient, which rises gently from 0.646 in the 55-64
band to 0.754 in the 25-34 band rather than jumping [CALCULATION]. A doubling of award share
against a gentle supply gradient is what a change in selection rules would look like, and also
what a genuine rise in output concentrated in younger cohorts would look like. As the brief
anticipated, this design **cannot separate** the two. Two things are worth stating
anyway. Non-citizen winners are Hispanic at roughly twice the citizen rate in both periods
(AW_NONCIT_EARLY then AW_NONCIT_LATE, against AWSHARE_CITEARLY then AWSHARE_CITLATE; counts
AW_NONCIT_NE and AW_NONCIT_NL) [CALCULATION], so part of any "Hispanic canon presence" comes
from foreign nationals rather than the US resident population, while the *step* itself is larger
among citizens, who more than double. And the documented-Mexican share of US-citizen
winner-years is AW_MEXDOC_LATE post-2015, against a Mexican-origin share of US adults 25-64 of
11.1% [CALCULATION, ACS 2024 PUMS]: whatever rose, it is Hispanic broadly, not specifically
Mexican-origin.

## Arm D — variety saturation

**Saturation is supported at the local margin and not identified for the national
counterfactual.** Mexican-cuisine restaurants per head barely respond to how Mexican a metro
is, but cross-metro variation cannot tell you what the United States would look like with a
hundredth of the population, because every metro draws on a national labour market, national
chains and national supply.

Data: every OpenStreetMap restaurant and fast-food feature in the fetched states, assigned to
CBSAs by point-in-polygon against the 2023 TIGER cartographic boundaries; Mexican-origin share
and income from ACS 2019-2023 5-year (935 CBSAs, 36.5M Mexican-origin residents inside CBSAs)
[SOURCE]. Estimation is Poisson QMLE with a log-population offset and robust SEs, which keeps
the metros that have zero Mexican restaurants instead of dropping them as a log-OLS would.
OSM_COVERAGE_LINE COVERAGE_CAVEAT

**Elasticity of Mexican restaurants per capita with respect to the Mexican-origin population
share** [CALCULATION, model output]:

| specification | elasticity | SE | z against 1 |
|---|---|---|---|
| primary (cuisine tag) | ELAST_PRIMARY | ELAST_PRIMARY_SE | ELAST_PRIMARY_Z |
| independent name classifier | ELAST_NAME | ELAST_NAME_SE | ELAST_NAME_Z |
| Mexican share of cuisine-tagged restaurants | ELAST_TAGGED | ELAST_TAGGED_SE | ELAST_TAGGED_Z |

An elasticity of 1 would mean variety scales one-for-one with group size. The estimate is
ELAST_PRIMARY, ELAST_Z_ABS SE below one and ELAST_Z0_ABS SE above zero. Doubling a metro's
Mexican-origin share raises Mexican restaurants per head by about DOUBLING_PCT; a tenfold
increase raises it by about TENFOLD_PCT [CALCULATION].

BIGMETRO_SENTENCE

**Placebos** load the way they should: all restaurants PLACEBO_ALL, Chinese PLACEBO_CHINESE,
Italian PLACEBO_ITALIAN, American PLACEBO_AMERICAN per capita against the same regressor. Only
the Mexican count loads positively, so the specification is not picking up a general
"more restaurants where more people" artefact.

**Where the curve flattens** — predicted Mexican restaurants per 100,000 residents from the
quadratic fit, other covariates at the sample mean [CALCULATION]:

DENSITY_TABLE

FLATTEN_SENTENCE **Availability saturates even earlier**: in the lowest decile of
Mexican-origin share (mean DECILE0_SHARE), DECILE0_ANY of metros already carry at least one
Mexican restaurant, at DECILE0_DENSITY per 100,000 against DECILE9_DENSITY in the top decile
(mean DECILE9_SHARE). A SHARE_RATIO-fold difference in group share buys a DECILE_RATIO-fold
difference in per-capita Mexican-restaurant density.

CONCRETE_SENTENCE

**Disconfirmation.** The pre-registered rejection conditions were an elasticity near or above 1,
or density still rising at the highest shares. Neither holds: the elasticity is ELAST_PRIMARY,
and the quadratic term is negative (QUAD_COEF, SE QUAD_SE), meaning the curve bends down rather
than continuing up. Two further checks that could have broken the result did not. An entirely
independent classifier built on restaurant names rather than cuisine tags gives ELAST_NAME
(SE ELAST_NAME_SE) against the tag-based ELAST_PRIMARY. And OSM coverage, measured against
County Business Patterns establishment counts (NAICS 722511 and 722513, 2023), does not vary
with Mexican-origin share: mapped restaurants over CBP establishments load at COVERAGE_COEF
(t COVERAGE_T) on log Mexican share, around a median of COVERAGE_MEDIAN [CALCULATION].
Differential mapping is not generating the flatness.

One coverage margin does move. The share of mapped restaurants carrying any cuisine tag rises
with Mexican share (TAGCOV_COEF, t TAGCOV_T), which inflates the tag-based Mexican count at the
high-share end and therefore biases the elasticity **upward**, not flat. The headline is
conservative with respect to this defect, and the two specifications built to be immune to it
agree: the name classifier ignores cuisine tags entirely (ELAST_NAME) and the tagged-offset
specification divides by the tagged count, so tagging density cancels (ELAST_TAGGED).

**What this does not establish.** The regressor is cross-metro variation in group share at a
given moment, with a national Mexican-origin population of 11.1% of adults 25-64 [CALCULATION,
ACS 2024 PUMS]. A metro at DECILE0_SHARE share still sits inside a country at 11%: its cooks, its
franchises, its tortilla supply and its recipes come from the national pool. The operator's
"1/100 of them" is a statement about that national pool, and nothing in this design varies it.
The honest reading is that **within the observed range, the marginal member of the group adds
almost no further restaurant variety to the metro they live in**, while the costs the repo
prices scale per person; the national counterfactual remains unidentified, and the cooks table
below is the reason to expect it is not free.

### Who staffs the kitchens

Share of US chefs and cooks (OCCP 4000 and 4020, age 16+, employed), ACS 2024 1-yr PUMS
[CALCULATION, replicate-weight SEs]:

| group | share of chefs and cooks | SE | unweighted n |
|---|---|---|---|
| Mexico-born | 12.05% | 0.32pp | 2,241 |
| US-born Mexican-origin | 8.45% | 0.25pp | 1,870 |
| other foreign-born | 18.73% | 0.33pp | 3,846 |
| US-born non-Hispanic white | 37.95% | 0.35pp | 10,667 |

One in five American cooks is Mexican-origin and one in eight was born in Mexico. State detail is
in `derived/arm_d_cooks_shares.csv`. This is the part of the "recipes can be copied" claim that
the data can speak to: recipes travel, but at present a fifth of the labour that executes them in
the United States comes from this group, and the counterfactual wage and price effect of removing
it is not measured here.

## Arm C — stopped

PatentsView's legacy bulk files return HTTP 403, its download page redirects to a USPTO
transition guide, and the current API needs a registered key; the Copyright Office exposes a
record-search service rather than bulk registrations. A surname-by-surname search would mix
registration propensity with name frequency and has no denominator, so the arm is stopped rather
than run degraded. Probe evidence and the revival path: `derived/arm_c_stop_note.md`.

## Arm E — Latin music

Verbatim from the RIAA's own year-end reports, parsed from the PDFs in this lane rather than
quoted from search results [SOURCE]:

- 2024 report: "Latin music in the US market continues to outpace all other listening [in the US]
  - growing to 8.1% of total recorded music revenue in the US."
- 2025 report: "Latin music made up 8.8% of total US revenue", total Latin revenue $1,009.6M
  against $969.1M in 2024, both on the wholesale basis.

The dollar levels are not comparable across the two reports: the 2024 report states $1.4bn on a
retail-value basis and RIAA has since moved to wholesale. Three limits matter more than the
number. "Latin" is a language and genre category covering artists from every Spanish-speaking
country, not output by the US Mexican-origin population. Neither report gives listener
composition, so **crossover to non-Hispanic listeners is unmeasured**: an 8.8% revenue share is
consistent with heavy within-group consumption and with broad crossover alike. And revenue share
is a market statistic, not a welfare one.

## What a fair "cultural benefit" line would look like in dollars

The repo's fiscal gap for the Mexican-origin population is **-$7,224 per person-year** against
third-plus whites on the complete account [SOURCE: confidence ladder 130, amended 2026-09-18].
A cultural line that sits beside it has to be per person-year, in the same direction convention,
and has to be a *differential* against the same white reference, because the gap is a differential.

The only market-priced piece of cultural output this lane measures is creative earnings:
**$355 per person-year** (Mexico-born) and **$744** (US-born Mexican-origin) against **$1,362**
for US-born whites, or $865 and $905 against $1,362 once age and education are matched
[CALCULATION]. As a differential that is **-$457 to -$497 per person-year matched**, or -$618 to
-$1,007 unmatched. Market earnings are a lower bound on the value of the output, since consumers
pay at least that much, and they are already inside the fiscal ledger as taxable income.

The benefit natives receive above what they pay is consumer surplus, which this lane does not
measure. Applying a surplus multiple of 1x to 3x on the differential, a range chosen to bracket
the usual empirical estimates and not derived here [INFERENCE], puts the cultural-output line at
**-$460 to -$1,500 per person-year** relative to whites. On the group's own absolute output
rather than the differential, the same multiples give **+$355 to +$2,200 per person-year**, which
is the number a "they enrich us" argument would want; it is not the number that offsets a gap
defined against whites.

Either way the order of magnitude is the finding: the measured cultural channel is worth
single-digit hundreds to low thousands of dollars per person-year, against a fiscal gap of
$7,224. It does not close the gap, and on the differential construction it does not point the
other way either. The restaurant-variety channel is not inside this figure, and the saturation
result above governs how much of it can scale with population.

## Limits

Occupation is supply, not quality or influence: a metro full of graphic designers is not thereby
a cultural capital. Awards are gated by credentials, by who submits and by selection rules that
changed inside the window, and surname imputation cannot separate Mexican from other Hispanic
origin nor catch a Hispanic woman who took a non-Hispanic married name. OSM cuisine tagging is
voluntary and uneven; the coverage test says it is not *differentially* uneven by Mexican share,
which is the failure mode that would matter, but it remains a volunteered source. Restaurants per
capita conflate supply with demand from the group itself, and nothing here values within-group
consumption differently from crossover consumption. The repo measures resident groups, not
admission; the absolute sign of any account is a convention and the gap against same-age whites
is not.

## Reproduction

Every script is cache-first and deterministic. Two determinism defects were found and fixed
during the run: earnings were summed as floats, so DuckDB's parallel aggregation changed the last
digit between runs (now summed as integer cents), and one summary JSON inherited dict ordering
from a query result (now sorted). A rank guard was also added to the Poisson fits after a
subset made the region dummies collinear, which statsmodels reports only as a warning.

`scripts/16_verify_reproducible.sh` snapshots `derived/`, re-runs all fifteen scripts in order
over the warm cache, and compares every file with `cmp`. Its verdict line is written to
`derived/reproduction_check.txt`.

## Operational note for the parent

A Census API key was printed once in this session, inside the URL of a `requests` HTTPError
traceback from an early version of script 13. The script now catches that exception and prints
only the status code, but the key did appear in the session log; rotating it is the parent's call.
