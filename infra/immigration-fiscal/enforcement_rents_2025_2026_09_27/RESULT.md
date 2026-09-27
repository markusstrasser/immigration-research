claude-opus-5-5

**Verdict:** The post is mostly wrong. Its one checkable enforcement fact holds: Texas made 24.4% of ICE arrests
in July 2026 [DATA]. Its nine rent figures match no rent index, and on Zillow's repeat-rent index seven of the nine
metros had rising rents in the year to August 2026 [DATA]. Its premise, that inflows raise rents, is right in
direction, at about 1% of rent per 1% of population, but removals have not been shown to work in reverse [SOURCE].
Its attribution fails. High-arrest metros, Texas above all, had weaker rent growth before the 2025 surge. The gradient
was about as steep in the year to August 2023, before inflows fell, as in the post's window, and steeper in 2024. Measured
in pp of annual rent growth per arrest per 1,000 residents, the placebo-differenced change in the gradient against 2024
is +0.33 for 2025 (wild-bootstrap 95% interval −0.55 to +1.19) and +0.52 for the post's window (−0.41 to +1.43). In
levels against 2023 it is −0.13 (−1.12 to +0.71). The post implies −1.50 [CALCULATION]. Effects of the size population
accounting predicts (−0.1 to −0.4 per arrest per 1,000) are neither detected nor excluded.

# Did 2025–26 interior enforcement lower rents? (DHS claim test)

Lane: `infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/`. Brief: `BRIEF.md` (commit 8f3b4aa), amended by
the team lead on 2026-09-27 to make the post's own window the primary test. Complete as of 2026-09-28. Numbers come
from `derived/` unless a tag says otherwise.

## Verdict by claim

| Claim in the post | Verdict | Evidence |
|---|---|---|
| "Texas accounted for about a quarter of ICE arrests in July" | True, and not new | 11,986 of 49,091 July 2026 arrests, 24.4%; 25.5% in July 2025 and 26.8% a month in 2024, before the surge; Texas has 9.3% of the US population [DATA] |
| Texas "posted the country's sharpest rent drops" | Right on rank, wrong on size, and old | San Antonio has the steepest ZORI change of 194 metros (−1.27% to August 2026); Texas metros trailed the rest by 1.2–1.9 pp in every year since 2023, most in the year to August 2024 [CALCULATION] |
| The nine metro figures (−2.6% to −8%) | Not reproduced; unsourced | None of 73 readings from eight sources equals a figure; nearest readings are 0.1–1.4 pp away and come from different indexes, geographies and unit types; on ZORI 7 of 9 metros rose [CALCULATION] |
| "Illegal-worker inflows push rents and home prices up" | True for arrivals; not shown for removals | About +1% rent per 1% of population (Saiz 2007, US metros 1983–97); +1.44% (SE 0.34) per unauthorized-worker inflow equal to 1% of employment (Wilson–Zhou 2026, US MSAs 2021–24); Secure Communities cut construction 5.7% and moved resale prices +0.1% (SE 1.1) on average (Howard–Wang–Zhang 2025, US counties 2008–13) [SOURCE] |
| "That inflow has been reversed in the states running the hardest interior enforcement" | Not established by state; total inflow false through June 2025 | Texas net international migration +167,475 in the year to June 2025 (+354,864 a year earlier) and population +391,243 [DATA]; unauthorized workers' net flows turned negative nationally in February–July 2025, largest where the 2021–24 inflows had been largest [SOURCE] |
| Implied: enforcement caused the declines | Rejected at the post's size; small effects not identified | Against 2024, placebo-differenced gradients are positive in all 23 specifications and all 92 leave-one-state-out runs; against 2023, the level gradient steepened by 0.13 (SE 0.21); the post's −1.50 lies outside every interval [CALCULATION] |

## The claim, steel-manned

The strongest version of DHS's case runs as follows. Each step has support.

1. **Texas enforces hardest.** It made 80,644 ICE arrests in 2025, 2.54 per 1,000 residents against 0.64 in the
   median state, and 107,948 in the year to July 2026, 3.40 against 0.89 [DATA: `state_arrests.csv`, `summary.json`].
2. **Texas metros have the weakest rents.** On ZORI, San Antonio's change in the year to August 2026 (−1.27%) is the
   lowest of 194 metros, and the 17 Texas metros trail the other 177 by 1.35 pp [CALCULATION: `texas_gap.csv`].
3. **Across metros, rent growth falls with arrest intensity.** In the year to August 2026 each arrest per 1,000
   residents goes with −0.84 pp of rent growth (SE 0.22), and −0.79 (SE 0.18) with the supply control
   [CALCULATION: `regressions.csv`, L1 and L2].
4. **Inflows raise rents.** Saiz (2007) finds about +1% per 1% of population [SOURCE: `housing_deport_2026_09_16/RESULT.md`].
   Wilson and Zhou (2026) find +1.438% (SE 0.344) in ZORI rents per unauthorized-worker inflow equal to 1% of
   employment over 2021–24 [SOURCE: `us_lowskill_effects_2026_09_22/reads/wilson_zhou_dallasfed_2026.md`, Table 6b].
5. **The inflow did reverse, at least for unauthorized workers.** Wilson and Zhou identify "a period of net aggregate
   outflows (February 2025–July 2025)", largest where the boom inflows were largest (county correlation −0.96)
   [SOURCE: Dallas Fed WP 2607, p. 19]. Census net international migration fell from 2.73 million to 1.26 million a
   year nationally and from 354,864 to 167,475 in Texas [DATA: Census V2025].
6. **Enforcement's footprint exceeds its arrest count.** Brookings finds employment 0.43% below trend six months after
   a local surge, "one arrest associated with four jobs lost" [SOURCE: Brookings, 2026-09-04,
   https://www.brookings.edu/articles/beyond-arrests-how-ice-enforcement-depressed-local-employment-in-2025/].
   Operator surveys and CoStar analysts reported occupancy losses in Texas, Florida and Arizona apartments in late
   2025 [SOURCE: `housing_deport_2026_09_16/RESULT.md`, append 1].

On this reading, the collapse in inflows and the surge in arrests cut housing demand most where enforcement is
heaviest, and rents fell there first. The White House made the same argument with different figures in January 2026
(Austin −21.5%); `housing_deport_2026_09_16` found those figures did not reproduce either.

For the reading to hold, three things must be true. The enforcement gradient in rent growth must appear or steepen
after the surge, net of supply. The Texas gap must be new. The population change must be large enough to move rents
by 3–8%. The sections below test each.

## Design fixed before any regression was run (appended 2026-09-28 00:20 JST)

The DHS post is dated 2026-09-25 [SOURCE: WLT Report embed "Homeland Security (@DHSgov) September 25, 2026",
https://wltreport.com/2026/09/25/dhs-reveals-cities-leading-in-deportations-see-the-steepest-rent-declines/;
Newsweek 2026-09-27, https://www.newsweek.com/dhs-says-ice-deportations-are-pushing-down-rent-other-factors-are-at-play-12493918].
Its "July" is July 2026, so the brief's "July 2025" premise is wrong by a year. The brief's 2025 design is kept, and a
second window covering the post's own period is added.

- **Rents:** Zillow ZORI, metro level, all homes plus multifamily, smoothed, not seasonally adjusted. Growth is the
  12-month percent change. Calendar-year growth runs December to December. The July and August year-over-year
  changes match the post's timing.
- **Enforcement:** ICE arrests from the Deportation Data Project FOIA file (`arrests-latest.parquet`, 2022-10-01 to
  2026-08-06), with DDP's duplicate rows dropped. A state measure uses the filled-in apprehension state. An AOR measure
  uses the apprehension AOR, with AOR population from DDP's county-to-AOR file and Census V2025 county estimates.
  The rate is arrests per 1,000 residents. A metro's exposure is the population-weighted mean over its counties.
  SEs are clustered by the modal state or AOR.
- **Supply:** multifamily (5+ unit) permits 2021–2023 per 1,000 housing units (Census BPS metro annual files; ACS 2021
  1-year B25001).
- **Main sample:** metropolitan statistical areas with a 2025 population of at least 250,000 and complete ZORI data.
  The robustness samples are MSAs of at least 500,000 and all matched MSAs. The regressions are unweighted; a
  population-weighted run is a check.
- **Test A (brief):** the change in calendar-year growth, 2025 minus 2024, regressed on 2025 arrests per 1,000,
  adding supply and then 2024 growth.
  **Placebo:** 2024 minus 2023 on the same 2025 measure.
- **Test B (the post's window):** growth to August 2026 minus growth to August 2025, regressed on arrests per 1,000 from
  August 2025 to July 2026. The placebo is the same as Test A's.
- **Sign convention:** if enforcement lowered rents, the enforcement coefficient on the change in growth is negative and
  the placebo is about zero. p-values use t with G−1 degrees of freedom; a wild-cluster restricted bootstrap
  (Webb weights, 9,999 draws, fixed seed) is reported beside them.

## Additions made after the first results (appended 2026-09-28)

The design above already carried the team lead's amendment. Its heading says 00:20 JST, but the session log shows it
was appended at 00:08 JST (15:08 UTC on 2026-09-27), eight minutes before the first run at 00:16 JST. The first run
had Tests A and B with all five exposure measures, the three samples and the checks A3w, B3w, A3sa, A3jul/P3jul,
A3all and A3pop. The following were added after its results were seen. Every one is reported below.

- **Test B's placebo** became the August version: the year to August 2024 minus the year to August 2023 (PB), and the
  level in the year to August 2024 (LP), on the Test B measure. The design had reused Test A's calendar placebo.
- **Stacked placebo-differenced estimates** (S_A, S_B) with wild-bootstrap intervals. They turn the brief's
  comparison of treated and placebo years into one coefficient with a joint SE.
- **The sample without Texas** and leave-one-state-out runs.
- **After a context break (2026-09-28):**
  - the July window (B3jul, PB3jul, S_Bjul), which the team lead had asked for;
  - placebos for the weighted checks (P3w, PB3w);
  - the lost-inflow test (N1–NP3, S_N);
  - supply by period (S_A_ps, S_B_ps) and a gate on its coverage;
  - the level gradient in the year to August 2023 (LP0, LP0s) and the level contrasts S_L23 and S_L24, added to answer
    the objection that the 2024 placebo overlaps the fall in inflows;
  - the Texas gap table;
  - control coefficients for every row;
  - a fix removing Puerto Rico from the national totals and from the median state. The median rate moved from 0.857
    to 0.889 arrests per 1,000, and no regression changed.
- **The exposure window** is August 2025 to July 2026, not the team lead's "2025 through March 2026". That instruction
  rested on my early report that DDP's file ends in March 2026; the file in fact runs to 6 August 2026.

## Q1. The numbers

**Source.** The post names no source. Newsweek reports that DHS "did not identify the source" and that the
percentages "do not appear to correspond with several major publicly available rental indexes" [SOURCE: Newsweek,
2026-09-27]. I checked 73 readings from eight sources against the nine metros: 55 published readings entered in
`index_readings.csv` with their URLs, plus 18 ZORI changes computed here. My ZORI values reproduce Zillow's August
report to 0.05 pp for the three metros it quotes [DATA: `gates.csv`].

- No reading equals a post figure within 0.05 pp [CALCULATION: `source_check.csv`].
- Only 1 of 73 readings is within 0.15 pp: Apartment List's San Antonio city median, −4.9% [CALCULATION].
- No source comes within 0.5 pp on even half of its readings [CALCULATION: `summary.json`, `source_agreement`].
  Apartment List does on 3 of 7, Zumper on 3 of 18 and Realtor.com on 1 of 10. Apartments.com (0 of 11), Yardi
  Matrix (0 of 5), RealPage (0 of 1), RentCafe (0 of 3) and ZORI (0 of 18) never do.

Readings are year-over-year percent changes to August 2026 unless a month is given (m = metro, c = city)
[DATA: `index_readings.csv`, `dhs_metros.csv`]:

| Metro | Post | ZORI Aug (Jul) | Apartment List | Realtor.com 0–2BR | Apartments.com | Yardi Matrix | Zumper 1BR / 2BR (c) | Other | Nearest (gap) |
|---|---|---|---|---|---|---|---|---|---|
| San Antonio | −4.8 | −1.27 (−1.74) | −5.1 m, −4.9 c | −3.8 | −2.2 m, −1.6 c | — | −8.6 / −4.5 | RealPage −3.7; RentCafe −1.59 c (Jul) | Apartment List c (0.1) |
| Austin | −4.3 | −0.02 (−0.93) | −2.9 m | −2.5 | −0.1 c | −2.8 | −16.6 / −19.1 | | Apartment List m (1.4) |
| Dallas | about −3 | +0.43 (+0.10) | −1.5 c | −2.4 | −0.1 c | −1.4 | −13.0 / −13.4 | | Realtor.com (0.6) |
| Houston | about −3 | +0.04 (−0.06) | −2.6 c | −2.7 | −1.2 m, −1.0 c | −1.7 | −14.6 / −5.4 | | Realtor.com (0.3) |
| Miami | −2.6 | +1.60 (+1.38) | — | −1.0 (Jul −1.3) | +1.6 c | — | −2.3 / −4.9 | | Zumper 1BR (0.3) |
| Phoenix | −4.2 | +0.72 (+0.37) | −3.5 c | −3.2 | −1.2 m, −0.7 c | −1.6 | −2.5 / −3.3 | | Apartment List c (0.7) |
| Atlanta | −3.2 | +2.02 (+2.02) | — | −1.8 | +1.6 c | — | +0.6 / +5.0 | | Realtor.com (1.4) |
| Nashville | −5.3 | +0.80 (+0.50) | −3.6 c (Jul) | −2.9 (Jul −3.9) | −0.6 c | −1.1 | −10.1 / −0.6 | RentCafe −0.78 c | Realtor.com Jul (1.4) |
| New Orleans | −8.0 | +1.40 (+1.22) | — | — | — | — | −4.7 / −8.4 | RentCafe −2.52 c (Jun) | Zumper 2BR (0.4) |

**Metro by metro:**

- **New Orleans.** The post's −8% matches only Zumper's two-bedroom city median (−8.4%). Zumper's one-bedroom
  figure is −4.7%, and ZORI is +1.4%, at the July 2026 peak.
- **Nashville and Atlanta.** Their figures (−5.3%, −3.2%) are 1.4 pp from anything published. Atlanta rose on five
  of its six readings.
- **All-time highs.** ZORI puts Atlanta, Miami and Nashville at all-time highs in August 2026 [DATA: `dhs_metros.csv`].

[INFERENCE] The figures look like the largest asking-rent declines, picked metro by metro. The one untested single
candidate is Apartment List's full July 2026 city file, whose CSV answered HTTP 403. Its published July figure for
Nashville, −3.6%, misses the post's −5.3% by 1.7 pp.

**The period.** The post gives none. Every reading above is year-over-year. The arrest share is for July 2026, so the
rent figures are presumably mid-2026 readings too [INFERENCE].

**The Texas share.** DDP's file runs to 6 August 2026, so July 2026 can be checked. Texas made 11,986 of 49,091 ICE
arrests, 24.4%, or 24.5% of arrests with a known state [DATA: `arrests_monthly_texas.csv`]. DHS says August's roughly
51,000 arrests topped July's, which fits DDP's July count [SOURCE: Financial Express, 2026-09-26,
https://www.financialexpress.com/immigration/trump-administration-says-deportations-are-lowering-rents-what-the-data-shows/4347940/].

The share is not a sign of new Texan zeal:

- Texas made 25.5% of arrests in July 2025 and averaged 26.8% a month in 2024, before the surge (29.4% of arrests with
  a known state) [DATA].
- Texas has 9.28% of the US population [DATA: Census V2025].
- From 2024 to the year to July 2026, Texas's arrests rose 3.7-fold (29,372 to 107,948) and the nation's 3.9-fold
  (109,936 to 424,460) [CALCULATION].

**"Sharpest drops".** On ZORI, San Antonio has the steepest year-over-year change of 194 metros in both July and August
2026. In August the four Texas metros rank 1, 10, 11 and 16 [CALCULATION: `texas_gap.csv`]. The declines are small:
−1.27% in San Antonio, and only 10 of the 194 metros fell at all [CALCULATION: `metro_panel.csv`]. The post's own list
contradicts its headline, since its New Orleans (−8%) and Nashville (−5.3%) figures exceed every Texas figure.

## Q2. Timing

ZORI growth in percent: calendar years, then year-over-year to the month shown. "From peak" is August 2026 against the
series maximum [DATA: `dhs_metros.csv`].

| Metro | 2023 | 2024 | 2025 | YoY Jul 2025 | YoY Jul 2026 | YoY Aug 2026 | Peak | From peak |
|---|---|---|---|---|---|---|---|---|
| San Antonio | −0.49 | −1.38 | −1.10 | −1.07 | −1.74 | −1.27 | 2022-08 | −3.7 |
| Austin | −2.77 | −4.28 | −2.87 | −3.59 | −0.93 | −0.02 | 2022-08 | −10.8 |
| Dallas | +0.25 | −0.48 | +0.06 | −0.17 | +0.10 | +0.43 | 2022-08 | −0.8 |
| Houston | +2.15 | +1.84 | +0.01 | +0.46 | −0.06 | +0.04 | 2025-05 | −0.3 |
| Miami | +1.46 | +1.62 | +0.56 | +0.84 | +1.38 | +1.60 | 2026-08 | 0.0 |
| Phoenix | +0.05 | +0.12 | −0.62 | −1.04 | +0.37 | +0.72 | 2022-08 | −1.0 |
| Atlanta | −0.36 | +1.09 | +2.25 | +1.48 | +2.02 | +2.02 | 2026-08 | 0.0 |
| Nashville | +0.04 | +1.18 | +0.48 | +0.34 | +0.50 | +0.80 | 2026-08 | 0.0 |
| New Orleans | +2.80 | +2.88 | +0.23 | +1.83 | +1.22 | +1.40 | 2026-07 | 0.0 |
| Denver | +2.56 | −0.65 | −1.50 | −1.79 | −0.89 | −0.55 | 2024-07 | −2.7 |

San Antonio, Austin, Dallas and Phoenix peaked in August 2022, 29 months before the surge began in January 2025. Austin
is 10.8% below that peak and fell in each of 2023, 2024 and 2025 [DATA].

The Texas gap is older than the surge and was widest before it. Below are the 17 Texas metros against the other 177
in the main sample, with ranks out of 194 (1 = weakest) [CALCULATION: `texas_gap.csv`]:

| Growth | Texas | Others | Gap (pp) | Rank: San Antonio / Austin / Dallas / Houston |
|---|---|---|---|---|
| Calendar 2023 | +2.03 | +3.87 | −1.84 | 6 / 1 / 19 / 52 |
| Calendar 2024 | +2.06 | +3.63 | −1.57 | 4 / 1 / 6 / 38 |
| Calendar 2025 | +1.36 | +2.67 | −1.31 | 8 / 3 / 16 / 15 |
| Year to Aug 2023 | +2.23 | +3.60 | −1.37 | 5 / 1 / 12 / 54 |
| Year to Aug 2024 | +1.67 | +3.57 | −1.90 | 5 / 1 / 3 / 31 |
| Year to Aug 2025 | +1.52 | +2.70 | −1.17 | 8 / 1 / 13 / 20 |
| Year to Aug 2026 | +1.51 | +2.86 | −1.35 | 1 / 10 / 16 / 11 |

The gap was as wide in the years of peak inflow. Texas's net international migration was 251,690 in the year to June
2023 and 354,864 in the year to June 2024, its largest in the series; the nation's was 2.26 and 2.73 million
[DATA: Census V2025, `NST-EST2025-ALLDATA.csv`]. In those years Texas metros trailed the rest by 1.4–1.9 pp, and Austin
had the weakest rent growth of the 194 metros.

Two post metros slowed sharply in 2025 without an old peak or heavy supply: Houston (+1.84% in 2024, +0.01% in 2025;
supply rank 39) and New Orleans (+2.88%, +0.23%; rank 156). Both are Brookings surge metros [DATA]. Neither fell.
Houston is 0.3% below its May 2025 peak, New Orleans is at its July 2026 peak, and both rose in the year to August 2026.
These two are the best cases for the post, and they show slower growth, not declines.

## Q3. Supply

The supply proxy is 5+ unit permits for 2021–2023 per 1,000 housing units [DATA: `dhs_metros.csv`, rank of 194]:

- Austin 69.8 (rank 1)
- Nashville 42.6 (4)
- Denver 31.4 (16)
- San Antonio 28.0 (21)
- Dallas 26.4 (26)
- Phoenix 26.2 (27)
- Houston 21.0 (39)
- Atlanta 17.6 (51)
- Miami 16.6 (55)
- New Orleans 3.0 (156)

Share of cross-metro variation explained (R²) and slopes, main sample, N = 194; SEs clustered by state. Enforcement
is 2025 state arrests per 1,000 [CALCULATION: `supply_r2.csv`, which also has the Aug 2025–Jul 2026 measure]:

| Outcome | Supply R² | Supply slope (SE) | Enforcement R² | Enforcement slope (SE) | Both R² |
|---|---|---|---|---|---|
| Growth 2023 | 0.216 | −0.094 (0.017) | 0.147 | −1.50 (0.45) | 0.335 |
| Growth 2024 | 0.326 | −0.096 (0.015) | 0.171 | −1.34 (0.40) | 0.459 |
| Growth 2025 | 0.230 | −0.083 (0.014) | 0.128 | −1.19 (0.39) | 0.331 |
| YoY to Aug 2026 | 0.083 | −0.047 (0.013) | 0.125 | −1.13 (0.31) | 0.192 |
| Cumulative Dec 2022–Dec 2025 | 0.347 | −0.285 (0.041) | 0.204 | −4.25 (1.27) | 0.509 |
| Change, 2025 − 2024 | 0.008 | +0.013 (0.012) | 0.003 | +0.15 (0.16) | 0.010 |
| Change, Aug 2026 − Aug 2025 | 0.077 | +0.044 (0.009) | 0.000 | −0.03 (0.13) | 0.078 |

Supply explains 22–33% of the cross-metro variation in each year's rent growth and 35% of the cumulative change from
December 2022 to December 2025. There, each extra 10 permits per 1,000 housing units cost 2.9 pp of rent growth. It
explains almost none of the change from 2024 to 2025 (R² 0.008). In the year to August 2026, high-supply metros
recovered faster (+0.044 pp per permit per 1,000) as their pipelines emptied.

Arrest intensity behaves like a lasting trait of these metros, not a 2025 shock. The 2025 arrest rate "explains" 2023
rent growth (R² 0.147, slope −1.50) better than 2025 growth (0.128, −1.19). With supply controlled, its slope shrinks
from −1.35 in 2023 to −1.06 in 2025 [CALCULATION].

## Q4. Enforcement regressions

**Sample and units.**

- The main sample has 194 metropolitan areas of at least 250,000 with complete ZORI and supply data. The robustness
  samples have 111 (at least 500,000) and 339 (all matched MSAs).
- Coefficients are percentage points of annual rent growth per ICE arrest per 1,000 residents. One arrest per 1,000
  is 0.1% of the population.
- SEs are clustered by state (46 clusters in the main sample) or AOR (25). p-values use t with G−1 degrees of freedom.
  "Wild" is the restricted wild-cluster bootstrap with Webb weights and 9,999 draws.
- Every row, with every control coefficient, is in `derived/regressions.csv` (240 rows) [CALCULATION].

**Test A, the brief's specification** (state measure, 2025 arrests per 1,000; mean 0.89, SD 0.61):

| Spec | Outcome | Controls: coefficient (SE) | Coef | SE | p | p wild | N | G | R² |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Δ growth 2025 − 2024 | none | +0.150 | 0.164 | 0.365 | 0.407 | 194 | 46 | 0.003 |
| A2 | same | supply +0.013 (0.012) | +0.129 | 0.154 | 0.407 | 0.447 | 194 | 46 | 0.010 |
| A3 | same | supply −0.039 (0.013); 2024 growth −0.565 (0.120) | −0.545 | 0.212 | 0.014 | 0.060 | 194 | 46 | 0.230 |
| P1 | Δ growth 2024 − 2023 (placebo) | none | +0.155 | 0.174 | 0.378 | 0.408 | 194 | 46 | 0.002 |
| P2 | same | supply −0.003 (0.013) | +0.159 | 0.170 | 0.355 | 0.413 | 194 | 46 | 0.002 |
| P3 | same | supply −0.070 (0.014); 2023 growth −0.767 (0.065) | −0.877 | 0.207 | <0.001 | 0.059 | 194 | 46 | 0.538 |

AOR measure, 25 clusters (coefficient, SE):

- A1 +0.013 (0.091), A2 +0.009 (0.075), A3 −0.289 (0.103; p 0.010, wild 0.148).
- P1 −0.145 (0.107), P2 −0.145 (0.108), P3 −0.436 (0.131; p 0.003, wild 0.220).
- Controls in A3: supply −0.038 (0.013), 2024 growth −0.538 (0.113). In P3: supply −0.068 (0.013), 2023 growth
  −0.711 (0.066).

**Test B, the post's window** (state measure, arrests August 2025 to July 2026 per 1,000; mean 1.21, SD 0.83):

| Spec | Outcome | Controls: coefficient (SE) | Coef | SE | p | p wild | N | G | R² |
|---|---|---|---|---|---|---|---|---|---|
| B1 | Δ YoY, Aug 2026 − Aug 2025 | none | −0.017 | 0.099 | 0.865 | 0.869 | 194 | 46 | 0.000 |
| B2 | same | supply +0.045 (0.009) | −0.072 | 0.089 | 0.419 | 0.450 | 194 | 46 | 0.078 |
| B3 | same | supply −0.004 (0.015); YoY Aug 2025 −0.553 (0.107) | −0.467 | 0.106 | <0.001 | 0.051 | 194 | 46 | 0.286 |
| PB1 | Δ YoY, Aug 2024 − Aug 2023 (placebo) | none | −0.466 | 0.226 | 0.045 | 0.061 | 194 | 46 | 0.032 |
| PB2 | same | supply +0.004 (0.017) | −0.471 | 0.230 | 0.047 | 0.073 | 194 | 46 | 0.032 |
| PB3 | same | supply −0.066 (0.012); YoY Aug 2023 −0.790 (0.048) | −0.987 | 0.256 | <0.001 | 0.095 | 194 | 46 | 0.602 |
| L1 | YoY to Aug 2026 (level) | none | −0.839 | 0.223 | <0.001 | 0.074 | 194 | 46 | 0.128 |
| LP1 | YoY to Aug 2024 (level, placebo) | none | −1.228 | 0.343 | <0.001 | 0.074 | 194 | 46 | 0.253 |
| B3jul | Δ YoY, Jul 2026 − Jul 2025 | supply −0.016 (0.014); YoY Jul 2025 −0.514 (0.084) | −0.443 | 0.111 | <0.001 | 0.063 | 194 | 46 | 0.202 |
| PB3jul | Δ YoY, Jul 2024 − Jul 2023 (placebo) | supply −0.067 (0.011); YoY Jul 2023 −0.730 (0.050) | −0.841 | 0.276 | 0.004 | 0.079 | 194 | 46 | 0.574 |

With supply controlled, the level slope is −0.786 (0.183) to August 2026 against −1.124 (0.263) to August 2024.

On the AOR measure (25 clusters): B3 −0.116 (0.086) against PB3 −0.375 (0.138), and L1 −0.262 (0.175) against LP1
−0.416 (0.240).

**Placebo-differenced estimates.** Each metro enters twice, in the placebo year and the treated year. The enforcement,
supply and lagged-growth slopes all differ by period. The enforcement × post coefficient is therefore the treated-year
gradient minus the placebo-year gradient, with a joint SE. A negative value would mean rent growth fell more in
high-arrest metros after the surge than before it.

| Estimate | Sample | Coef | SE | p | p wild | Wild 95% CI | Placebo-year gradient (SE) | N | G |
|---|---|---|---|---|---|---|---|---|---|
| 2025 vs 2024, state (S_A) | main | +0.332 | 0.191 | 0.089 | 0.256 | −0.55 to +1.19 | −0.877 (0.207) | 388 | 46 |
| Year to Aug 2026 vs Aug 2024, state (S_B) | main | +0.520 | 0.186 | 0.007 | 0.049 | −0.41 to +1.43 | −0.987 (0.257) | 388 | 46 |
| Year to Jul 2026 vs Jul 2024, state (S_Bjul) | main | +0.398 | 0.210 | 0.064 | 0.038 | −0.59 to +1.36 | −0.841 (0.276) | 388 | 46 |
| S_A, supply by period (S_A_ps) | main | +0.300 | 0.186 | 0.114 | 0.265 | −0.56 to +1.14 | −0.852 (0.204) | 388 | 46 |
| S_B, supply by period (S_B_ps) | main | +0.509 | 0.182 | 0.008 | 0.049 | −0.40 to +1.42 | −0.981 (0.258) | 388 | 46 |
| Levels: year to Aug 2026 vs Aug 2023 (S_L23) | main | −0.133 | 0.206 | 0.521 | 0.510 | −1.12 to +0.71 | −0.653 (0.182) | 388 | 46 |
| Levels: year to Aug 2026 vs Aug 2024 (S_L24) | main | +0.338 | 0.140 | 0.020 | 0.085 | −0.17 to +0.99 | −1.124 (0.263) | 388 | 46 |
| S_A, AOR | main | +0.147 | 0.102 | 0.163 | 0.212 | | −0.436 (0.131) | 388 | 25 |
| S_B, AOR | main | +0.259 | 0.076 | 0.002 | 0.193 | | −0.375 (0.138) | 388 | 25 |
| S_A, Brookings surge metro (0/1) | main | +0.714 | 0.375 | 0.063 | 0.101 | | −0.868 (0.277) | 388 | 46 |
| S_A, state | ≥500,000 | +0.958 | 0.236 | <0.001 | | | −1.342 (0.196) | 222 | 40 |
| S_B, state | ≥500,000 | +0.819 | 0.259 | 0.003 | | | −1.214 (0.265) | 222 | 40 |
| S_A, state | all MSAs | +0.901 | 0.207 | <0.001 | | | −1.075 (0.257) | 678 | 50 |
| S_B, state | all MSAs | +0.876 | 0.179 | <0.001 | | | −0.974 (0.228) | 674 | 50 |
| S_A, state | main without Texas | +0.422 | 0.521 | 0.422 | 0.425 | | −1.604 (0.352) | 354 | 45 |
| S_B, state | main without Texas | +0.991 | 0.243 | <0.001 | 0.003 | | −1.718 (0.279) | 354 | 45 |

"Supply by period" replaces the single 2021–23 proxy with 5+ permits two and three years before each growth year:
2021–22 for the placebo years, 2022–23 for calendar 2025 and 2023–24 for the year to August 2026. The two level rows
stack year-over-year growth with supply (× post) and no lagged-growth control.

All 23 lagged-growth estimates against 2024 are positive. The table shows 14 of them; the other nine, the AOR and
Brookings versions in the other samples, are in `regressions.csv`. In the 46 leave-one-state-out runs of each, S_A
ranges from +0.23 (without Michigan) to +0.42 (without Texas), and S_B from +0.45 (without Florida) to +0.99 (without
Texas) [CALCULATION: `leave_one_state_out.csv`]. Dropping Texas makes the change more positive.

**Other checks.** Each pairs the treated year with its placebo, coefficient (SE) [CALCULATION]:

| Check | Treated | Placebo |
|---|---|---|
| Population-weighted, Test A | −0.602 (0.204) | −0.951 (0.167) |
| Population-weighted, Test B | −0.267 (0.128) | −0.870 (0.200) |
| At-large arrests only, Test A | −0.940 (0.445) | −1.464 (0.397) |
| At-large arrests only, Test B | −0.924 (0.206) | −1.475 (0.282) |
| Change in the arrest rate, 2025 − 2024 | −0.931 (0.336) | −1.397 (0.303) |
| July-to-July years | −0.398 (0.125) | −1.062 (0.352) |
| Brookings surge dummy | −0.153 (0.208) | −0.868 (0.277) |

Three variants of A3 have no placebo and move it by at most 0.17: seasonally adjusted ZORI −0.551 (0.209), all-unit
permits as the supply control −0.375 (0.164), and 2024 population growth added −0.478 (0.203).

**Reading.**

- **No raw gradient.** Without the lagged-growth control, rent growth did not change more where arrests were higher
  (A1 +0.15, B1 −0.02).
- **The conditional gradient is older than the surge.** With the control the gradient turns negative (A3 −0.55,
  B3 −0.47), which is the number a DHS-style reading would cite. It was more negative in every placebo year (P3 −0.88,
  PB3 −0.99, PB3jul −0.84). High-arrest metros had been failing to rebound from slow growth before any surge, and
  after the surge they failed less.
- **The base year matters, but neither choice supports the post.** The 2024 placebo years overlap the start of the
  border-driven fall in inflows (mid-2024), and 2024 had the steepest gradient. The year to August 2023 overlaps
  nothing. Against it, the level gradient in the post's window is 0.13 steeper (−0.84 against −0.76 without the
  supply control, −0.79 against −0.65 with it; stacked SE 0.21). That is a change indistinguishable from zero, and the
  Texas gap is the same size in both years (−1.37 and −1.35 pp).
- **The post's size is rejected.** The post implies −1.50 pp per arrest per 1,000: its Texas figures average −3.8%,
  and Texas has 2.52 more arrests per 1,000 than the median state. The raw ZORI contrast between Texas and the other
  metros implies −1.22 [CALCULATION: `implied_gradients.csv`]. Both lie outside every wild-bootstrap interval,
  including the level contrast against 2023 (lower end −1.12). The largest population-accounting gradient, four
  departures per arrest at ladder 180's association (−1.2), sits just outside it.
- **Small effects are not identified.** Three gradients lie inside every interval except one:
  - −0.1 (one resident per arrest, rent elasticity 1);
  - −0.3 (ladder 180, one per arrest);
  - −0.4 (four departures, elasticity 1).

  The exception is the level contrast against 2024, whose lower end of −0.17 excludes −0.3 and −0.4. The contrast
  against 2023 includes all three.
- **The ceiling.** Texas has 2.52 more arrests per 1,000 than the median state. At the lower end of the post's-window
  interval against 2024 (−0.41), its extra enforcement cut its rent growth by at most about 1.0 pp a year relative to
  the median state. At the lower end of the noisier level contrast against 2023 (−1.12), the ceiling is 2.8 pp
  [CALCULATION: −0.41 × 2.52; −1.12 × 2.52].

**Lost inflow instead of arrests.** The same tests on the fall in Census net international migration per 1,000
residents (the year to June 2025 against the year to June 2024; mean 3.6, SD 2.8 across the 194 metros) give the same
pattern [CALCULATION: `regressions.csv`, N1, N3, NP1, NP3, S_N]:

- The raw association with the 2025 change in rent growth is −0.004 (SE 0.029).
- With lagged growth controlled, the slope is −0.080 (SE 0.035). It is steeper in the placebo year: −0.127
  (SE 0.026).
- The placebo-differenced change is +0.047 (SE 0.041; wild 95% CI −0.125 to +0.158). That interval excludes ladder
  180's association (−0.3 per 1 per 1,000) but not an elasticity of 1 (−0.1).

This test measures exposure, not a counted local flow, because Census allocates county migration from ACS patterns.
Its placebo year also overlaps the first half of the migration fall (July–December 2024).

## Q5. Counterexamples

**Denver**, the brief's case, has high supply and light enforcement:

- Colorado made 0.70 ICE arrests per 1,000 residents in 2025, about a quarter of Texas's 2.54. Denver's AOR made 0.91
  per 1,000 in the year to July 2026, against 4.31 in San Antonio's AOR [DATA].
- With heavy supply (31.4 permits per 1,000 housing units, rank 16), Denver's rents fell 1.50% in 2025. That is
  more than San Antonio (−1.10%), Dallas, Houston or Phoenix; among the post's metros only Austin (−2.87%) fell
  further [DATA].
- In the year to August 2026, Denver (−0.55%) is third-lowest of 194 metros, below every post metro except San Antonio.
- Colorado Springs, in the same state, fell 1.32% in 2025.

**The heaviest enforcement is on the border, and rents there are rising** [DATA: `aor_arrests.csv`, `metro_panel.csv`,
`brookings_surge_metros.csv`]:

- In the year to July 2026, the Harlingen AOR made 10.9 arrests per 1,000 residents, San Diego 4.4 and El Paso 3.7,
  against 4.3 in San Antonio's AOR.
- In the year to August 2026, McAllen (+0.5%), Brownsville (+3.7%) and El Paso (+3.2%) rose; McAllen and El Paso are
  at all-time highs.
- San Diego rose 2.0%, to a record.
- Laredo rose 1.5%. Brookings counts 56.3 excess arrests per 1,000 workers there in the seven months from its June 2025
  surge, 57 times the median surge metro's 1.0.
- Los Angeles, a Brookings surge metro from June 2025, rose 2.2% in 2025 and stands at a record.

**The post's own metros are not ordered by enforcement.** On Brookings's measure, excess arrests per 1,000 workers in
the seven months from each local surge were [DATA]:

- San Antonio 3.29
- Houston 1.92
- New Orleans 1.00
- Atlanta 0.71
- Nashville 0.58
- Austin 0.56
- Miami 0.45

Dallas and Phoenix are not surge metros. Austin, with the steepest decline since 2022, had one of the lighter surges.

**Top supply quintile, by enforcement tercile** (39 metros; 2025 state arrests per 1,000) [CALCULATION:
`counterexamples_summary.csv`, `counterexamples.csv`]:

| Tercile | Metros | Arrests per 1,000 | Supply | Growth 2024 | Growth 2025 | Change | YoY Aug 2026 | Change to Aug 2026 |
|---|---|---|---|---|---|---|---|---|
| Low | 13 | 0.42 | 29.9 | +2.45 | +2.18 | −0.27 | +2.51 | +0.40 |
| Mid | 7 | 0.72 | 37.1 | +1.85 | +1.17 | −0.68 | +2.40 | +1.40 |
| High | 19 | 1.52 | 31.1 | +0.96 | +0.03 | −0.92 | +0.90 | +0.80 |

The high-enforcement group grew more slowly already in 2024. It slowed 0.65 pp more than the low group from 2024 to
2025, then recovered 0.40 pp more in the post's window. The 2025 comparison leans the post's way; the post's own
window reverses it.

## Q6. Magnitude

**Population moved.**

- **Arrests.** In the year to July 2026, Texas's 107,948 ICE arrests equal 0.34% of its population [CALCULATION].
- **Departures per arrest.** Brookings finds four jobs lost per excess arrest: excess arrests are about 0.11% of the
  workforce against a 0.43% employment shortfall [SOURCE: Brookings]. That estimate comes from 64 surge metros in
  2025, set against control cities in a staggered difference-in-differences. The slope change behind it is −0.073 pp
  a month (95% CI −0.12 to −0.02) [SOURCE: Brookings appendix B,
  https://www.brookings.edu/wp-content/uploads/2026/09/Beyond-Arrests-Appendices.pdf]. Over six months that puts the shortfall between
  about 0.12% and 0.72%, or 1 to 6.5 jobs per arrest [CALCULATION]. About half the missing jobs would have been held
  by US-born workers [SOURCE: Brookings], and a job lost is not a resident gone, so four departures per arrest is an
  upper bound [INFERENCE].
- **DHS's own claim.** DHS claims "more than 3 million" departures since January 2025 [SOURCE: Financial Express,
  quoting DHS; unverified]. Annualised over 20 months and allocated to Texas by its 25.4% arrest share, that is
  1.44% of Texas's population [CALCULATION].

Implied rent change at a rent elasticity of 1 (Saiz 2007; `housing_deport_2026_09_16` puts the credible range across
studies at 0.8–2.2) and at ladder 180's association (×3) [CALCULATION: `magnitude.csv`]:

| Scenario | Population | Rent, elasticity 1 | Rent, ladder 180 |
|---|---|---|---|
| Texas arrests, year to Jul 2026, one resident each | −0.34% | −0.34% | −1.02% |
| Four departures per arrest | −1.36% | −1.36% | −4.09% |
| DHS's 3 million departures, by arrest share | −1.44% | −1.44% | −4.33% |
| Texas's arrests over the median state's | −0.25% | −0.25% | −0.75% |
| Lost inflow, Texas (year to June 2025 vs a year earlier) | −0.60% | −0.60% | −1.80% |
| Lost inflow, US | −0.43% | −0.43% | −1.30% |
| Lost inflow, four Texas metros | −0.68% | −0.68% | −2.03% |

**Against the post's declines.**

- **Only one route reaches −3.0% to −4.8%:** the upper-bound departures at ladder 180's association.
- **That association is too long-run for this use.** It measures +0.030 log points of 2015–2026 rent growth per point
  of 2010–2023 rise in the Mexican-origin share, within state. It is descriptive and eleven years long. Ladder 183's
  instrumented decade estimate, now a diagnostic, is +1.4% (SE 1.4) per point, an interval that holds both zero and
  one-for-one [SOURCE: `research/immigration-confidence-ladder.md`, entries 180 and 183]. Applied to one year, the
  association overstates the response [INFERENCE].
- **At an elasticity of 1**, the scenarios span −0.25% to −1.44%.
- **ZORI shows −1.27% (San Antonio) to +0.43% (Dallas)** for the four Texas metros [DATA].

**Relative effects are what a cross-section can see.** Arrests happen everywhere. What sets Texas apart is its excess
of 2.52 arrests per 1,000 over the median state: 0.25% of population, or up to 1.0% with four departures
[CALCULATION]. At an elasticity of 1 that is −0.25% to −1.0% of rent relative to the median state. At ladder 180's
association it is −0.75% to −3.0%.

**Border inflow against interior enforcement.**

- **Size.** Census net international migration fell by 1,472,266 between the year to June 2024 and the year to June
  2025, 0.43% of the US population [DATA; CALCULATION]. In Texas it fell by 187,389 (0.60%); in the four Texas metros,
  by 145,231 (0.68%).
- **Timing.** The fall came before most of the interior surge. Monthly ICE arrests rose from 12,174 in January 2025
  to 26,819 in July and 39,722 in December [DATA: `arrests_monthly_texas.csv`]. It is therefore mostly the national,
  border-driven fall [INFERENCE].
- **The Texas-specific part.** Texas's fall exceeds the national one by 0.17 pp. That is the most a Texas-specific
  cause could explain through the inflow channel up to June 2025 [CALCULATION].
- **Population still grew.** Texas grew by 391,243 (1.25%) in the year to June 2025. Its four big metros grew
  1.4–2.1%: San Antonio +38,402, Austin +53,796, Dallas +123,557, Houston +126,720 [DATA: Census V2025,
  `cbsa-est2025-alldata.csv`, NPOPCHG2025].
- **Growth slowed, not reversed.** The lost inflow slowed population growth; it did not reverse it through June 2025.
  Census V2026, due in December 2026, will show how far the 2025–26 surge reversed it.

## The premise (claim 2)

The studies the repo has pinned agree that inflows raise rents and differ on the size [SOURCE:
`housing_deport_2026_09_16/RESULT.md`, append 3; `us_lowskill_effects_2026_09_22/reads/wilson_zhou_dallasfed_2026.md`;
ladder entries 180 and 183; Howard, Wang and Zhang, Tables 3–4,
http://www.trouphoward.com/uploads/1/2/7/7/127764736/howard_wang_and_zhang_-_cracking_down_pricing_up_-_nov_2025.pdf]:

| Study | Population and design | Estimate |
|---|---|---|
| Saiz (2007), JUE | US metros, 1983–1997; shift-share IV | +1.0% rents per 1% of population (robust range 0.8–1.6) |
| Wilson and Zhou (2026), Dallas Fed WP 2607 | US MSAs, unauthorized-worker inflows 2021–24; leave-out shift-share IV, first-stage F 14.0 | +1.438% ZORI rents (SE 0.344) per inflow equal to 1% of employment |
| Ladder 180 (this repo) | 168 metros, within state; descriptive | +0.030 log points (SE 0.007) of 2015–26 rent growth per point of 2010–23 rise in Mexican-origin share |
| Ladder 183 (this repo) | 334 metros, 2000–2010; IV, downgraded to a diagnostic | +1.4% rents (SE 1.4) per point of foreign-born share |
| Howard, Wang and Zhang (2025) | US counties, Secure Communities rollout 2008–13; staggered DiD | See the list below |

Howard, Wang and Zhang's estimates:

- new construction fell by 0.165 units per 1,000 residents a year (SE 0.068), or 5.7%;
- new-home prices rose 4.4% (SE 1.0);
- resale prices moved +0.1% (SE 1.1) on average;
- resale prices rose 3.4% (SE 0.9) in the tracts with the fewest low-education immigrants and fell 4.1% (SE 2.0) in
  those with the most.

The one causal study of enforcement finds that it cut homebuilding and left average existing-home prices unchanged.

Newsweek identifies the post's unnamed "research" as probably the Wilson–Zhou paper [SOURCE: Newsweek, 2026-09-27].
That paper declines the step the post takes. Its data cover "only a limited period of net aggregate outflows
(February–July 2025), which precludes a comprehensive evaluation of deportation effects" [SOURCE: Dallas Fed WP 2607,
pp. 19–20]. Its 2024–25 extension estimates employment and wages only.

The premise therefore holds for arrivals, but no direct evidence supports the post's step from it to "enforcement lowers
rents" [INFERENCE].

## Limitations

- **Instrument.** This test was run through an LLM with post-training dispositions on politically charged topics
  (`notes/llm-bias-caveat.md`). The verdicts rest on pinned data and scripts that anyone can rerun, and the design let
  the post's claim win: a negative placebo-differenced gradient would have supported it.
- **Rent measure.** ZORI is a smoothed repeat-rent index of all home types. Asking-rent and new-lease series fall more
  when a supply glut brings concessions, and the post's figures may be real readings of such series. All regressions
  use ZORI; I found no free metro panel of asking rents. The multifamily-only ZORI was not fetched.
- **Border arrests in the state measure.** The state measure includes border-area and jail-transfer arrests, which
  inflate Texas's rate (the Harlingen AOR alone runs at 10.9 per 1,000). The AOR and at-large measures reduce this, and
  the results hold on both.
- **Exposure level.** Exposure varies by state or AOR (46 or 25 clusters). City-level operations and local 287(g)
  agreements are not measured; the Brookings surge dummy is the only metro-level measure.
- **Power.** The intervals against 2024 allow effects down to −0.4 to −0.6 pp per arrest per 1,000, and the level
  contrast against 2023 down to −1.1. That is up to about 1.0–1.5 pp a year of rent growth in Texas relative to the
  median state, or 2.8 pp on the level contrast. Mean reversion in the Sun Belt supply cycle could hide an effect that
  size, and the lagged-growth control only partly removes it.
- **Supply proxy.** Permits for 2021–2023 per 2021 housing unit are a crude stand-in for completions. If Texas's
  pipeline lasted longer than the proxy says, the remaining supply would push the enforcement coefficient toward the
  post's story, not away from it. Timing the proxy to each growth year leaves the stacked estimates at +0.30 and +0.51.
  Permits are not completions, and the 2024 permits are in the 2023 metro delineation while the housing-unit
  denominator is in the 2020 one.
- **Population data.** Census V2025 ends in June 2025, before most of the surge.
- **Hand-entered inputs.** The 58 index readings were entered by hand from published pages. Apartment List's full
  panel was blocked. The Brookings table was transcribed from an image PDF and checked against its own column
  identities; the published table carries small rounding inconsistencies (`test_analysis.py`).
- **2024 arrest records.** Only 91.1% of 2024 arrests carry a state, against 99.3% in the post's window. Texas's 2024
  share of all arrests (26.7% for the year) therefore understates its share of arrests with a known state (29.3%)
  [CALCULATION: `arrests_monthly_texas.csv`].

## Reproduction

From the repository root:

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # Census key, for the ACS call only
uv run --no-project python3 infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/fetch.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/analysis.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/ -q
```

- **`analysis.py`** takes about two minutes. It checks every input against the sha256 in `_cache/manifest.json` and
  exits 1 if any of its 27 gates fails.
- **Byte-identical reruns.** Two consecutive runs gave byte-identical copies of all 17 files in `derived/`
  (2026-09-28), and the 15 tests pass.
- **Upstream updates.** `fetch.py` pulls the latest ZORI and DDP files. A fresh fetch after an upstream update will
  change the numbers; `summary.json` records the hashes these results used.

## Files

- **Scripts:**
  - `fetch.py` downloads the 18 inputs to `_cache/` (ignored) and writes the manifest;
  - `analysis.py` runs everything else and writes `derived/`;
  - `test_analysis.py` holds the 15 checks: the statistics helpers against closed forms, the Brookings transcription
    against its identities, and this file's claims against `derived/`.
- **Hand-entered inputs:**
  - `brookings_surge_metros.csv` is Brookings's 64-metro table;
  - `index_readings.csv` holds 58 published readings with their URLs.
- **Outputs in `derived/`:**
  - `regressions.csv` holds every regression;
  - `metro_panel.csv` has one row per matched metro;
  - `state_arrests.csv` and `aor_arrests.csv` give arrests and rates by window;
  - `arrests_monthly_texas.csv` gives monthly arrests and the Texas share;
  - `dhs_metros.csv` covers the post's metros plus Denver;
  - `source_check.csv` puts every reading beside the post's figure;
  - `texas_gap.csv`, `supply_r2.csv`, `counterexamples.csv`, `counterexamples_summary.csv`, `magnitude.csv`,
    `implied_gradients.csv`, `leave_one_state_out.csv` and `zillow_match_failures.csv` hold the other tables;
  - `summary.json` holds the headline numbers and input hashes;
  - `gates.csv` holds the 27 gates.
