model self-report: claude-opus-5[1m]

**Verdict:** Three of the four Denmark charts reproduce from open Statistics Denmark tables,
essentially to the pixel. The @Scientific_Bird raw violent-crime chart (2010-2022) reproduces
exactly: my ratios match my read-off of all 20 substantive bars to within 0.04 (Kuwait 10.11,
Somalia 9.78, Lebanon 8.71, Tunisia 8.38, Jordan 6.54). The @jonatanpallesen 12-panel chart
reproduces once two of its labels are decoded: 54 of 60 bars land within 1x of the chart, median
absolute difference 0.3x, and the headline claims hold exactly (Somalia rape 19.6x vs 20x,
robbery 33.3x vs 33x, attempted homicide 26.9x vs 27x). Its "Palestine" bar is not a Statistics
Denmark category at all: STRAFNA4 has no Palestine, and the bar is the Lebanon+Kuwait+Jordan
origin group (mean error 2%, and it explains why those three high-rate origins never appear as
bars of their own); its "Ex-Yugoslavia" is Yugoslavia + Yugoslavia FR + Serbia and Montenegro
only, excluding Bosnia, Croatia and North Macedonia (3% vs 33%). The ft.dk chart reproduces
exactly, all 34 bars within 0.5 percentage points, but it does not measure what the thread says:
it is cumulative conviction prevalence to age 30 for men born 1985-87, not convictions per
arrest, so it carries no information about police profiling either way. The one chart that does
**not** reproduce is the age/sex-adjusted violent-crime chart: no open table crosses offence type
with age and sex, so a country-level age-sex-standardized *violent*-crime rate cannot be built
from statbank. The closest available construction (age-sex standardization of all-offence
convictions, STRAFNA3 x FOLK1C) removes 19-44% of each origin's gap to Danish origin, which
brackets the 13-58% the published adjusted chart implies, so the chart is consistent with the
open data without being checkable against it.

## Verification (both required checks PASS)

| check | value A | value B | diff |
|---|---|---|---|
| (a) persons guilty 2024, all persons | STRAFNA9 M+K, age TOT, ancestry TOT = 159,320 | STRAFNA4 "Criminal decisions total", IELAND Total = 159,320 | 0 (0.000%) |
| (b) population 2024Q1 ages 15-79 | FOLK1C IELAND Total, KØN Total = 4,703,107 | FOLK1E ancestry Total = 4,703,107 | 0 (0.0000%) |
| (b2) FOLK1C internal | sum of 241 country rows = 4,703,107 | Total row = 4,703,107 | 0 (0.0000%) |

STRAFNA9 has no `TOT` sex value, so men and women were summed. All 71 STRAFNA4 country-of-origin
labels matched a FOLK1C label with no manual crosswalk.

## Chart 1 — violent crime by origin, 2010-2022 (@Scientific_Bird, raw)

`STRAFNA4` offence "Crimes of violence, total" / `FOLK1C` all persons, ages 15-79, pooled
2010-2022. Danish-origin reference rate 117.6 per 100k per year. Chart values are my read-off
of the bar ends.

| origin | chart | mine | persons | origin | chart | mine |
|---|---|---|---|---|---|---|
| Kuwait | 10.1 | 10.11 | 226 | Syria | 4.15 | 4.15 |
| Somalia | 9.8 | 9.78 | 1,910 | Afghanistan | 4.05 | 4.07 |
| Lebanon | 8.7 | 8.71 | 2,594 | Egypt | 3.75 | 3.76 |
| Tunisia | 8.4 | 8.38 | 144 | Iran | 3.5 | 3.50 |
| Jordan | 6.5 | 6.54 | 179 | Turkey | 3.35 | 3.38 |
| Uganda | 5.65 | 5.67 | 125 | Kenya | 3.3 | 3.33 |
| Iraq | 4.9 | 4.93 | 1,774 | Ghana | 3.2 | 3.18 |
| Morocco | 4.85 | 4.87 | 632 | Myanmar | 2.85 | 2.85 |
| Algeria | 4.7 | 4.71 | 83 | Pakistan | 2.55 | 2.56 |
| Ethiopia | 4.2 | 4.19 | 87 | Tanzania | 2.4 | 2.40 |

Rank order is identical to the chart once the historical ex-Yugoslav codes (Yugoslavia 3.27,
Yugoslavia FR 4.47, Serbia and Montenegro 4.73) are dropped, which the chart also does. The
chart's Denmark bar sits at 1.0 by construction. Only the sub-0.5x tail disagrees, and there my
read-off precision is the binding constraint, not the data (chart Japan ~0.2 vs 0 convictions in
13 years; chart USA ~0.35 vs 0.22 on 27 persons). Full table: `chart1_comparison.csv`.

**Kuwait/Somalia/Lebanon ~10x violent: reproduces.** 10.11 / 9.78 / 8.71.

## Chart 3 — 12 offence types, top-5 origins, 2008-2024 (@jonatanpallesen)

The chart's own subtitle (STRAFNA4, FOLK1C, ages 15-79, 2008-2024, rate relative to
Danish-origin) is exactly the recipe, and it works, but two chart labels are not statbank
categories and had to be decoded numerically.

**"Palestine" is not a STRAFNA4 origin.** STRAFNA4's `IELAND` offers 75 values with no Palestine
and no stateless category; FOLK1C offers 242 including Palestine (5157) and Stateless (5103), but
requesting either code against STRAFNA4 returns `EXTRACT-NOTFOUND`. Testing candidate aggregates
against the chart's nine "Palestine" bars:

| candidate | mean relative error vs chart |
|---|---|
| Lebanon + Kuwait + Jordan | 2% |
| Lebanon alone | 3% |
| Lebanon + Kuwait | 3% |
| Kuwait alone | 37% |
| ex-Yugoslavia | 70% |

Lebanon alone fits nearly as well, but Lebanon+Kuwait+Jordan is the supported reading: Kuwait and
Jordan have among the highest rates in the whole table (Kuwait robbery 28x, assault on a public
servant 12x) yet never appear as bars anywhere in the 12 panels, which is only explained if they
were folded into the Palestine group. That is substantively defensible, since stateless
Palestinians in Denmark carry those countries as origin, but it is a relabeling by the chart's
author, not a Statistics Denmark category, and the chart does not say so.

**"Ex-Yugoslavia" is the narrow set.** Yugoslavia + Yugoslavia FR + Serbia and Montenegro gives
3% mean error; adding Bosnia, Croatia and North Macedonia gives 33% (it halves every ratio).

With those two decodings, all 60 bars: median |chart - mine| = 0.3x, 54/60 within 1x, 58/60
within 2x. The two misses are both Ex-Yugoslavia bars where my read-off of the chart may be off
(blackmail 13 vs 13.5 under the narrow set, shoplifting 7 vs 7.3). Headline claims:

| claim | chart | mine | persons |
|---|---|---|---|
| Somalia, rape etc. | 20x | 19.6x | 49 |
| Somalia, robbery | 33x | 33.3x | 572 |
| Somalia, attempted homicide | 27x | 26.9x | 24 |

All three reproduce. Full table: `chart3_comparison.csv`.

Offence-code mapping used: rape = "Rape, etc"; assault on public servant = 1210; attempted
homicide = 1240; blackmail = "Blackmail and usury"; burglary = sum of the three burglary codes
(banks/shops, household, uninhabited); forgery = 1304; fraud = 1357; grievous assault = 1255;
groping = "Offences against decency, by pawing"; robbery = 1380; shoplifting = 1332; theft = sum
of six theft codes. Burglary and theft are the only aggregations; both fit the chart well, which
is weak confirmation the author aggregated the same way.

## Chart 2 — "adjusted for age, sex and year", 2010-2021: NOT reproducible

No open Statistics Denmark table crosses **offence type** with **age** and **sex**. STRAFNA4 is
offence x origin x year with no age or sex dimension; STRAFNA3 is sex x age x origin x year but
covers all offences with no offence breakdown; STRAFNA6/9 have age and sex but only the
6-category ancestry classification, not country of origin. A country-level age-sex-standardized
*violent*-crime rate therefore cannot be built from the public API. Whoever made this chart used
either microdata access or an assumption not stated on the chart.

Best available substitute: direct standardization of STRAFNA3 (all offences) to the Danish-origin
sex x 3-age-band structure, 2010-2021, and then applying each origin's measured age-sex factor to
its raw violent-crime ratio.

| origin | raw violent 2010-2021 | my approx adjusted | chart adjusted | gap removed: chart | gap removed: mine |
|---|---|---|---|---|---|
| Kuwait | 10.51 | 8.16 | 6.5 | 42% | 25% |
| Tunisia | 8.60 | 7.18 | 6.4 | 29% | 19% |
| Somalia | 9.78 | 7.15 | 6.2 | 41% | 30% |
| Lebanon | 8.84 | 6.68 | 5.7 | 40% | 28% |
| Morocco | 4.93 | 4.16 | 3.8 | 29% | 20% |
| Iraq | 4.94 | 3.91 | 3.3 | 42% | 26% |
| Turkey | 3.44 | 2.84 | 2.4 | 43% | 25% |
| Pakistan | 2.59 | 2.21 | 1.9 | 43% | 24% |

My approximation systematically removes less of the gap than the published chart, which is
expected: the age-sex factor measured on *all* convictions (dominated by traffic and special-law
cases, which are far less age- and sex-concentrated than violence) understates the factor for
violence alone. The chart's implied 13-58% sits above my 6-34% but in the same regime, so the
chart is consistent with the open data. It is not verified by it. Full table:
`chart2_comparison.csv`, country-level standardization in `dk_agesex_standardized_totalcrime.csv`.

Aggregate cross-check on the ancestry classification (STRAFNA9 x FOLK1E, same method, 2010-2021,
all offences): non-western immigrants 1.69x crude to 1.60x standardized (13% of gap removed);
non-western descendants 3.67x to 2.53x (43%); western descendants 1.41x to 1.21x (48%); western
immigrants 0.92x to 0.86x (already below 1, so no gap to remove). Age and sex explain part of the
gap and nowhere near all of it, on every construction I could build.

## Chart 4 — "share of men penally convicted by nationality" (ft.dk)

Reproduces exactly. All 34 plotted bars land within 0.5 percentage points of the source table,
which is my read-off precision, and the 63 country rows sum to the printed totals exactly
(84,848 population, 16,730 convicted).

| origin | chart | source | origin | chart | source |
|---|---|---|---|---|---|
| Kuwait | 70% | 69.7% (23/33) | Turkey | 37% | 36.9% (507/1,374) |
| Ethiopia | 68% | 68.2% (15/22) | Pakistan | 36% | 35.5% (142/400) |
| Jordan | 64% | 63.6% (35/55) | Poland | 29% | 29.3% (56/191) |
| Somalia | 62% | 62.2% (222/357) | Bosnia | 28% | 28.3% (147/519) |
| Syria | 62% | 62.1% (36/58) | Sweden | 22% | 22.2% (12/54) |
| Lebanon | 60% | 60.2% (322/535) | Germany | 20% | 20.0% (18/90) |
| Morocco | 54% | 54.1% (98/181) | Total | 20% | 19.7% |
| Iraq | 48% | 47.6% (212/445) | Denmark | 18% | 18.0% (14,043/78,120) |

**What it actually measures, and what the thread claims.** The thread presents this chart as
evidence against police profiling: "if this were true, we should see lots of arrests but few
convictions, low conviction rate. We see the opposite." That is not this statistic. The source is
a 2020 parliamentary answer whose Table 1 counts **men born 1985, 1986 and 1987 who had at least
one criminal-code conviction between ages 15 and 30**, divided by everyone of that origin in the
birth cohort. The denominator is the resident male cohort, not arrests or charges. It is
cumulative lifetime-to-30 prevalence, so it says nothing about convictions per arrest and cannot
speak to profiling in either direction. Three further mismatches with the chart's own framing:
the chart says "nationality" but the table is oprindelsesland, country of origin, pooling
immigrants and descendants; the chart's "Total" bar is the all-origins total including Danes, not
a non-Danish total; and the table's Table 2 (adding special acts and traffic) puts the same
Danish cohort at 51.3%, which shows how much the level depends on which offences count.

Small-N caution on the top of this chart: Kuwait is 23 convicted out of 33 men, Ethiopia 15 of
22. The chart's note that small countries were dropped is doing real work, and several origins it
kept are still tiny. Czechoslovakia (6/8), Estonia (3/4), Nigeria (6/8) and Zambia (3/4) all
exceed Kuwait's 70% in the source and were, correctly, left off.

## Method notes and caveats

- Denominator throughout is **residents by country of origin** (FOLK1C, ancestry total, so
  immigrants plus descendants plus, for Denmark, persons of Danish origin), 1 January of each
  year, ages 15-79. Pooled ratios are sum of persons over sum of person-years, not a mean of
  annual ratios.
- STRAFNA4 counts **persons with at least one guilty decision in the year for that offence type**,
  so a person convicted of two offence types is counted in both rows. "Criminal decisions total"
  is the unduplicated person count and matches STRAFNA9 exactly (verification a).
- Ages: STRAFNA tables cover 15-79 and `ALDER=TOT` is that range, matching the FOLK1C 15-79
  denominator. STRAFNA3/9 offer only three age bands (15-29, 30-49, 50-79), so the standardization
  is coarse; residual age composition within bands is not removed.
- Small-N origins: Tunisia's violent-crime bar rests on 144 persons over 13 years, Kuwait's on
  226, Tanzania's on 28. Several Pallesen bars rest on 5-30 persons (Myanmar groping n=5, Tanzania
  forgery n=6, attempted homicide n=12-28). No confidence intervals are computed here; the
  adjusted chart's own intervals reach past 7 for Kuwait and past 5 for Czechoslovakia.
- Residence-based denominators do not count tourists, undocumented residents, or people convicted
  and then deported, and the numerator does include convictions of people whose origin group
  churns. This biases small, high-turnover origin groups in an unsigned direction.
- The chart read-offs in every comparison table are my eyeball estimates from the JPEGs, accurate
  to roughly the tick spacing. Where chart and data disagree by less than that, no discrepancy
  should be inferred.

## Files

- `pull_dk_origin.py` — statbank pulls; `analyze.py`, `analyze2.py`, `analyze3.py` — analysis.
- `raw/` — `strafna4_offence_origin_2008_2024.csv` (119,850 rows, 94 offences x 75 origins x 17
  years), `strafna3_sex_age_origin_2008_2024.csv`, `strafna9_sex_age_ancestry_2008_2024.csv`,
  `folk1c_pop_origin_sex_age_2008_2024.csv` (160,446 rows),
  `folk1e_sex_age_ancestry_2010_2021.csv`, `folk1e_2024q1_age15_79.csv`.
- `bodies/api_request_bodies.json`, `bodies/folk1e_ancestry_body.json` — every API request body.
- `meta/` — tableinfo JSON for STRAFNA1-9, FOLK1C, FOLK1E (STRAFNA1/2 return no metadata).
- `dk_origin_rates.csv` — tidy output, 2,556 rows
  (year_range, origin, offence, persons, population, rate_per_100k, ratio_to_danish_origin).
- `dk_agesex_standardized_totalcrime.csv`, `chart1_comparison.csv`, `chart2_comparison.csv`,
  `chart3_comparison.csv`, `chart4_comparison.csv`, `analysis_log.txt`.
- `ftdk/EXTRACTION_NOTE.md`, `ftdk/table1_transcribed.csv`.

[SOURCE: https://api.statbank.dk/v1/data — STRAFNA3, STRAFNA4, STRAFNA9, FOLK1C, FOLK1E, pulled 2026-09-16]
[SOURCE: https://www.ft.dk/samling/20191/almdel/reu/spm/291/svar/1618048/2123368.pdf]
