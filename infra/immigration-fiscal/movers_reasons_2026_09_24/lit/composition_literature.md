**Verdict:** Natives, whites especially, do leave neighbourhoods as the minority or foreign-born share rises, but where studies separate the Hispanic or Mexican-origin share it adds little or nothing (Pais et al. 2009: Latino slope .004 (se .003); Hall & Crowder 2014: 10 points more Mexican share moves exit odds by −7% to +5%), randomized vignettes that hold crime and schools fixed disagree on Hispanics (null nationally in 2001, negative in Houston in 2011), none of the move studies measures crime, and no study links California's out-migration to its Hispanic share, whose leavers name jobs, housing and family. [INFERENCE] [SOURCE: sections 1–3 below]
Model: claude-opus-5-5[1m] (resumed worker, 2026-09-24; the first worker wrote only the stub before a rate limit)

# Do natives move away from Hispanic/Mexican-origin neighbours? Steel-man and disconfirming literature

Lane: `infra/immigration-fiscal/movers_reasons_2026_09_24/` (literature worker, 2026-09-24).
Question: do US natives (California in particular) leave places because of the Hispanic or
Mexican-origin share of their neighbours, as a disamenity distinct from housing costs, jobs or crime?
Rules: every number quoted verbatim from the fetched primary text with page/table; external causal
estimates carry interval or SE and population; both sides graded by the same standard
(`notes/quant-bias-checklist.md`, evidence-symmetry rules 1–4).

Provenance tags used: [SOURCE: …] = fetched primary text (cached under `../_cache/lit/`);
[INFERENCE] = this worker's reading; [UNVERIFIED] = not read in full; [GAP] = open.

Grading rule, applied to every study whichever way it points [INFERENCE]:
- **A** — design that separates composition from correlated neighbourhood traits (discontinuity,
  randomized vignette/video, or panel with the rival channels measured), interval reported,
  population matches the question.
- **B** — longitudinal individual data with the rival channels (crime, schools, prices, income)
  controlled, but selection on unobservables open.
- **C** — cross-section, stated preference without randomization, or aggregate flows.
- **D** — poll, descriptive tabulation, or claim without an interval.
A grade says how far a study can separate composition from its correlates; it does not say which
side the study supports.

## Already covered in the repo (cited, not re-fetched)

- Card (2001), Borjas (2006), Peri & Sparber (2011) on native internal migration in response to
  immigrant inflows: `research/immigration-native-sorting-tiebout-2026-09-18.md` lines 161–186
  (Peri & Sparber's bias argument against Borjas, reproduced on 2010–2023) and 392–416 (Card's
  design finds no mobility response; Borjas ~3 natives displaced per 10 immigrants), citations at
  502–504. Metro-level labour-market sorting, not neighbourhood composition.
- Saiz & Wachter (2011), within-metro house-price discount for immigrant/Hispanic composition:
  `infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md` (verdict line 5: the
  discount does not reproduce on 2013–2023 data; the paper's own caveats at lines 52, 206, 296).
- White flight from schools (Betts & Fairlie 2003; Poterba; Putnam 2007 vs Abascal & Baldassarri;
  Kustov & Pardelli 2018): `infra/immigration-fiscal/school_flight_2026_09_18/LIT.md` §§1, 2,
  5a–5c. White flight was not reproduced in the repo's own school data.

## Gap 1 — Stated versus revealed reasons and social desirability

### 1.1 Emerson, Yancey & Chai (2001), "Does Race Matter in Residential Segregation? Exploring the Preferences of White Americans" — grade A for design, abstract-only here

American Sociological Review 66(6):922–935, doi:10.2307/3088879 (also 10.1177/000312240106600607).
Full text NOT obtained (see failed sources); the numbers below are from the publisher abstract
only. [SOURCE: https://doi.org/10.1177/000312240106600607, abstract via Exa, 2026-09-24]

Design: "An over-the-telephone factorial experiment … measuring variables that shape white
Americans' choice of purchasing a home. Based on a national, random-digit-dial survey of 1,663
white Americans, the effects of African American, Asian, and Hispanic neighborhood composition on
whites' likelihood of buying a house are explored, as well as the other variables for which race
may serve as a proxy." Result: "Results indicate that Asian and Hispanic neighborhood composition do
not matter to whites. Black neighborhood composition, however, does matter, and matters even more
for white Americans with children under age 18. The effect of black composition is net of the
variables that whites offer as the primary reasons they do not want to live with blacks." (The
vignette varied crime, schools and housing values alongside composition — this worker's reading of
"the other variables for which race may serve as a proxy"; [UNVERIFIED] until the full text is
read.) [GAP] coefficients and intervals for the Hispanic-share term not seen.

Which side [INFERENCE]: disconfirms a Hispanic-composition disamenity in stated purchase intent
among whites nationally, 1999–2000-era survey, with crime, schools and values randomized
alongside. The randomization makes this the cleanest test of the "not separable" hypothesis: here
it is separable, and the Hispanic term is null. Weakness: stated intent to buy, not moves; a
hypothetical purchase, not an exit decision; one telephone survey.

### 1.2 Krysan, Couper, Farley & Forman (2009), "Does Race Matter in Neighborhood Preferences? Results from a Video Experiment" — grade A for design; black–white only

American Journal of Sociology 115(2):527–559, doi:10.1086/599248. Read in full.
[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC3704191/ via PMC OAI; cached
`_cache/lit/krysan2009_video_pmc3704191.txt`.] Face-to-face CAPI samples of Detroit and Chicago
residents rated videos of neighbourhoods whose residents' race (white, black, mixed) and social
class were manipulated. Table 1, white respondents, Model 1 (rating scale, se): relative to the
mixed video, white residents +0.158 (0.057), black residents −0.247 (0.057); relative to upper
middle class, lower working class −2.069 (0.063), blemished middle class −1.442 (0.068).
Abstract: "net of social class, the race of a neighborhood's residents significantly influenced
how it was rated. Whites said the all-white neighborhoods were most desirable."

Which side [INFERENCE]: race matters net of class, but the class manipulation (a stand-in for
disorder, upkeep and safety) moves ratings about eight times as much as the black-versus-mixed
contrast (2.069 vs 0.247). No Latino condition, so it does not speak to Hispanic composition
directly; it is here because it is the design standard for separating race from its proxies.

### 1.3 Lewis, Emerson & Klineberg (2011), "Who We'll Live With: Neighborhood Racial Composition Preferences of Whites, Blacks and Latinos" — grade A for design, abstract-only here; contradicts 1.1 on Hispanics

Social Forces 89(4):1385–1407, doi:10.1093/sf/89.4.1385. Full text NOT obtained. [SOURCE: ERIC
record EJ929939, https://eric.ed.gov/?id=EJ929939, abstract; cached `_cache/lit/eric_lewis2011.html`]
Verbatim: "Using the Houston Area Survey, we employ a factorial experiment to assess the effect of
racial composition on neighborhood desirability independent of crime, school quality, and property
values. … Results show that independent of proxies, whites find neighborhoods less attractive as
the proportion black or Hispanic increases; the proportion Asian has no impact. Racial composition
has little effect on Hispanics' and blacks' neighborhood preferences. We find no evidence of
in-group preferences; rather, results suggest that whites express negative out-group preferences
toward black and Hispanic neighborhoods." [GAP] coefficients, intervals, survey year and white n
not seen.

Which side [INFERENCE]: the same randomized design as 1.1, with crime, schools and values held
fixed, finds a Hispanic-composition penalty among Houston whites where the national 1.1 sample
found none. It supports "a composition preference exists and is separable from crime and schools"
— for a metro with a large Mexican-origin population, i.e. the setting closest to California. It
measures stated desirability, not moves or their size. 1.1 and 1.3 together: the Hispanic term is
design-identified in both, and their signs differ by place and period.

### 1.4 What the CPS "better neighborhood" move reason is

IPUMS: "WHYMOVE reports the primary reason for moving, for people who lived in a different
residence a year ago." Code 11 is labelled "Wanted better neighborhood" and sits in the housing
block beside code 10 (new or better housing), 12 "For cheaper housing" and 13 "Other housing
reason". [SOURCE: https://cps.ipums.org/cps-action/variables/WHYMOVE, fetched 2026-09-24; cached
`_cache/lit/ipums_whymove.html`.] One main reason per person; no follow-up on what "better" means.
No study was found that validates what this CPS category captures (crime, schools, disorder or
composition) against a second measure [GAP]. Implication [INFERENCE]: any composition motive
would be recorded here, under "other", or behind a housing or job reason, and the vignette studies
above (1.1–1.3) exist because respondents are not expected to name composition directly; the CPS
share is therefore neither a floor nor a clean ceiling for composition-driven moves.

## Gap 2 — Hispanic composition at neighbourhood level (separate from Black share)

### 2.1 Card, Mas & Rothstein (2008), "Tipping and the Dynamics of Segregation" — grade A (for tipping), C (for the Hispanic question)

Read in NBER Working Paper 13052 (April 2007), the pre-publication version of QJE 123(1):177–218.
[SOURCE: https://www.nber.org/papers/w13052; cached `_cache/lit/cmr_w13052.txt`, pdftotext
layout. Published-version numbers not checked; [GAP] QJE tables may differ slightly.]

Population, period, design. Census tracts in 104–114 MSAs, decades 1970–80, 1980–90, 1990–2000.
Regression discontinuity: change in a tract's non-Hispanic white population (as % of base-year
total population) at a city-specific candidate tipping point in the tract's minority share, with
MSA fixed effects, a quartic in the distance from the tipping point and tract controls
(unemployment, income, vacancy, renter share, single-unit share, transit use). Tipping points are
found on a 2/3 subsample and tested on the held-out 1/3; SEs clustered on the MSA (Table 3 notes).

Main estimates, verbatim from Table 3, column 1 (pooled, fixed-point, with controls):
| Decade | Beyond tipping point: change in white pop., % of base pop. (SE) | N tracts |
|---|---|---|
| 1970–80 | −12.1 (2.7) | 11,611 |
| 1980–90 | −13.6 (2.0) | 12,151 |
| 1990–2000 | −7.3 (1.5) | 13,371 |

Tipping points (Table 2, fixed-point method, % minority in tract): mean 11.87 (SD 9.51) in
1970–80, 13.53 (10.19) in 1980–90, 14.46 (9.00) in 1990–2000. Abstract: "White population flows
exhibit tipping-like behavior in most cities, with a distribution of tipping points ranging from
5% to 20% minority share."

Does it separate Hispanic from Black share? Only partly. "Minority" is defined as "all non-whites
plus white Hispanics" (p. 19). Table 5 re-estimates with black-only and black-plus-Hispanic
definitions; no Hispanic-only tipping point is estimated. The authors' reading, verbatim: "In the
1970s, tipping behavior seems to have been driven more by the black share than by the presence of
other groups. In the 1980s and 1990s, however, estimates are similar across all three definitions.
In the composite models … none of the measures consistently dominates, though the black plus
Hispanic measure has the smallest point estimate." (pp. 19–20). Table 5 values, read off the
pdftotext layout by decade (single-definition columns match Table 3):
| Decade | Minority only | Black only | Black+Hispanic only | Composite: minority / black / black+Hispanic |
|---|---|---|---|---|
| 1970–80 | −12.1 (2.7) | −22.0 (2.5) | −13.2 (2.9) | −6.4 (3.1) / −16.2 (3.3) / 0.0 (3.7) |
| 1980–90 | −13.6 (2.0) | −10.3 (2.9) | −11.0 (1.8) | −12.6 (2.1) / −3.0 (3.2) / 0.0 (2.6) |
| 1990–2000 | −7.3 (1.5) | −11.7 (1.8) | −10.3 (1.6) | −3.9 (1.4) / −4.3 (1.6) / −3.2 (1.7) |

Mechanism evidence. Table 9 (234 MSA-decades) relates the tipping point's location to a GSS
race-attitudes index (positive = less tolerant): −2.77 (1.16) without and −2.66 (0.94) with
controls for murders per 100,000 (−0.50 (0.18)), other index crimes and a riots index; "a standard
deviation change in the value of the attitudes index produces a 1.8 percentage point rise in the
tipping point" (p. 29). City % Hispanic enters with 0.65 (0.07): tipping points are higher in
cities with more Hispanics, "but less than proportionately so" (p. 27). Prices: "the estimated
discontinuities in the change in rents are small (-1.5% in 1970-80 and -0.6% in 1980-90 and
1990-2000) and statistically insignificant" (p. 23).

Which side [INFERENCE]: supports "composition-driven moves are real and sizeable" for white
households choosing among tracts inside a metro, 1970–2000: the discontinuity is not explained by
smooth tract traits, and its location tracks white racial attitudes after crime controls. It does
**not** isolate Hispanic composition: from the 1980s on, black-only, black+Hispanic and
all-minority thresholds fit alike and the composite cannot tell them apart. It is also a
within-metro sorting result; it says nothing about leaving a metro or a state such as California.

### 2.2 Crowder, Hall & Tolnay (2011), "Neighborhood Immigration and Native Out-Migration" — grade B

American Sociological Review 76(1):25–47, doi:10.1177/0003122410396197. Read in full from the PMC
author manuscript. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC3124827/ via the PMC OAI
JATS record; cached `_cache/lit/cht2011_pmc3124827.xml` and `.txt` (flattened by
`_cache/lit/jats2txt.py`).]

Population, period, design. "16,516 native-born non-Latino white and non-Latino black heads of
PSID households who were interviewed between 1968 … and 2005"; outcome is moving to a different
census tract over a two-year interval; logistic regression on person-periods (154,848; whites
92,506 person-periods, 9,538 persons, Table 3 footnote). Immigrant concentration is "the percentage
of the population in the tract of residence made up of individuals born outside of the U.S." — all
origins, not Hispanic or Mexican specifically. No tract crime or school measure is in any model.

Main estimates, verbatim. Pooled black and white householders: "a one standard-deviation increase
in the tract percent foreign-born increases the odds of out-mobility by 11.2%"; "a 2
percentage-point (about one standard deviation) increase in the foreign-born concentration during
the five years preceding the observation year increases the odds of out-mobility by about 6%".
Table 3, native-born whites, logit b (se):
| Term | M1 (no controls) | M2 (+ individual) | M3 (+ % other race) | M4 (+ tract income) | M5 (+ housing market) |
|---|---|---|---|---|---|
| % foreign-born in tract | .027 (.004) | .011 (.004) | .006 (.004) | .007 (.004) | .002 (.004) |
| 5-year change in % foreign-born | .043 (.008) | .050 (.007) | .043 (.007) | .043 (.007) | .038 (.008) |
| % foreign-born in surrounding tracts | −.022 (.004) | −.013 (.004) | −.012 (.004) | −.015 (.004) | −.013 (.004) |
| % neighbours of another race | | | .005 (.001) | .006 (.001) | .004 (.001) |
"% other racial groups" is "Percent of R's tract of residence at time t with race different from
race of the respondent", i.e. for whites everyone not non-Hispanic white — Hispanic, Black and
Asian together. Authors: "controlling for the racial composition of the tract reduces the
coefficient for the relative size of the immigrant population by almost half (from .011 to .006)";
"Among whites, mobility away from non-white neighbors, as emphasized in the ethnic flight thesis,
appears to be an especially important component"; and "the data do not lend themselves to explicit
statements of causality". Housing controls cut the growth coefficient "by about 12% (from .043
to .038)" for whites; for blacks, rents and low homeownership carry the effect instead.

Which side [INFERENCE]: supports a real but modest composition response by native whites at the
tract level (≈11% higher odds of leaving per SD of foreign-born share; the level effect is carried
by the non-white share, and the growth effect .038 (.008) survives every control). It cannot
separate Hispanic from Black or Asian neighbours, and with no crime or school measure it cannot
separate composition from crime or schools. Immigrants in surrounding tracts *lower* native exit
(fewer attractive nearby destinations), so the net metro-level response is smaller than the
local coefficient. Tract-to-tract moves, mostly within a metro: not evidence on leaving a state.

### 2.3 Hall & Crowder, "Native Out-Migration and Neighborhood Immigration in New Destinations" — grade B; the only study found that enters Mexican-origin share directly

Working paper dated December 10, 2013 (PDF created February 2014), the manuscript of the
Demography article [UNVERIFIED: published volume/pages not checked against the journal].
[SOURCE: https://globalmigration.ucdavis.edu/sites/g/files/dgvnsk821/files/inline-files/reserach-paper_native-flight.pdf;
cached `_cache/lit/hall_crowder_2013_new_destinations.pdf` / `.txt`.]

Population, period, design. PSID native-born white and black householders linked to tract data,
1980–2009: 104,787 person-periods, 16,523 persons, 345 MSAs (Table 2). Three-level
random-coefficient logit of leaving the tract; metros typed as established, new, developing or
non-gateways (Table 1; e.g. Atlanta and Raleigh "developing" in 1980–90). Controls: individual
traits, tract median house value, vacancy and poverty, metro job growth and wages. No tract crime
or school measure. The paper's own limit: "tract data on the racial composition or birth country of
immigrant populations are not available for our entire study period" (fn. 5).

Main estimates, verbatim (Table 2, p. 38, logit b (se)):
| Term | M1 | M2 | M5 (+ % Mexican) | M6 (+ metro) | Blacks | Whites |
|---|---|---|---|---|---|---|
| Tract % immigrant | .039 (.006) | .018 (.004) | .010 (.003) | .012 (.003) | .005 (.004) | .013 (.004) |
| % immigrant × developing gateway | | .048 (.009) | .030 (.008) | .027 (.008) | .022 (.011) | .033 (.012) |
| Tract % Mexican | | | −.001 (.002) | .000 (.002) | .003 (.003) | −.001 (.003) |
Text: "the odds of out-migration increase by nearly 50% with a ten-percentage point increase in
neighborhood immigrant concentration (e(.039*10) = 1.477)"; with controls, "a ten-point increase
in tract immigrant concentration increases the odds of out-migration for natives in established
gateways by 19.7%"; in developing gateways "a ten-point increase in neighborhood immigrant
concentration corresponds with a nearly 50% increase in the odds". On Mexican share: "Results
indicate that Mexican concentrations have little effect – above and beyond the effects of other
variables in our model – on native out-migration and do not alter the more-general impact of
neighborhood immigrant concentration on native out-migration."

Bound on a Mexican-specific response, whites [CALCULATION: from Table 2, whites column,
−.001 ± 1.96×.003 = −.0069 to +.0049 per point]: a 10-point higher Mexican-ethnic share, holding
the foreign-born share fixed, moves white natives' odds of leaving the tract by between −7% and
+5% (e^−.069 = 0.93, e^.049 = 1.05). The Mexican-ethnic share includes US-born Mexican Americans,
so this tests ethnicity beyond nativity, not the Mexican-born share as such.

Which side [INFERENCE]: two-sided. Natives do leave tracts as the foreign-born share rises (about
+14% odds per 10 points for whites in the full model, e^.13), most steeply in fast-changing
"developing" gateways, not in established ones like Los Angeles. But the Mexican-origin share adds
nothing once nativity and tract poverty, vacancy and values are held fixed, with an interval that
excludes large effects. This disconfirms a Mexican-ethnic disamenity as a separate driver of
tract exits; it cannot separate the nativity response from crime or schools.

### 2.4 Pais, South & Crowder (2009), "White Flight Revisited: A Multiethnic Perspective on Neighborhood Out-Migration" — grade B; enters black and Latino shares side by side

Population Research and Policy Review 28:321–346, doi:10.1007/s11113-008-9101-x. Read in full.
[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC2778315/ via PMC OAI; cached
`_cache/lit/pais_south_crowder2009_pmc2778315.xml` / `.txt`.]

Population, period, design. PSID geocoded to census tracts, 1990–1995 (the years with the PSID's
Latino sample), 31,594 person-years; logit of annual neighbourhood out-migration for Anglos
(non-Hispanic whites, the reference group), blacks, Mexicans, Puerto Ricans and Cubans. Controls:
age, family, income, education, tenure, crowding, public housing, employment and marital changes,
MSA % minority and a tract socioeconomic-disadvantage index. No crime or school measure.

Abstract, verbatim: "Anglos have a higher likelihood of moving when they have many minority
neighbors and there is little difference whether minority neighbors are black or Latino."
Table 2, Model 4 (main effects are the Anglo slopes, logit b (se)): neighbourhood % black
.006 (.003), p<.05; neighbourhood % Latino .004 (.003), not significant. Model 2: % minority
.004 (.002). [CALCULATION: 10-point odds ratios from those b and 1.96×se] A 10-point higher Latino
share multiplies Anglo odds of leaving by e^.04 = 1.04 (95% CI 0.98–1.10); a 10-point higher black
share by 1.06 (1.00–1.13). Mexicans themselves are *less* likely to leave as the Latino share rises
(interaction −.006 (.003)).

Which side [INFERENCE]: the Latino-share slope for Anglos is small, imprecise, and the same size as
the black-share slope; the paper cannot reject either zero or a black-sized effect for Latino
neighbours. Five years (1990–95) of annual moves, tract to tract; the disadvantage index absorbs
some of what a composition effect would carry, crime is not measured.

### 2.5 Crowder & South (2008), "Spatial Dynamics of White Flight" — grade B, combined minority share only

American Sociological Review 73(5):792–812, doi:10.1177/000312240807300505.
[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC2835167/ via PMC OAI; cached
`_cache/lit/crowder_south2008_pmc2835167.txt`.] White PSID householders 1980–2003; Table 2, Model
2: tract minority concentration .0231 (.0059) (with a cubic), minority concentration in surrounding
tracts −.0092 (.0021), change in surrounding minority concentration .0445 (.0163). Abstract:
"controlling for extralocal conditions provides substantially greater support for the white flight
thesis than has previously been observed". Minority is not split by group, so it cannot answer
the Hispanic question; it supports composition-linked exits by whites in general [INFERENCE].

## Gap 3 — Native flight from immigrant gateways, including California

Already in the repo, not re-read: Borjas (2006) finds about three natives displaced per ten
immigrants at city level; Card (2001) finds no mobility response; Peri & Sparber (2011) show the
Borjas specification is biased toward displacement
(`research/immigration-native-sorting-tiebout-2026-09-18.md` lines 161–186, 392–416). None of the
three separates ethnic composition from labour-market or housing channels.

### 3.1 Frey (1995), "Immigration and internal migration 'flight': A California case study", and Frey (1996), "Immigration, Domestic Migration, and Demographic Balkanization in America" — grade C; the steel-man at state level

Population and Environment 16(4):353–375, doi:10.1007/BF02208119; Population and Development
Review 22(4):741 (end page not in Crossref), doi:10.2307/2137808 (volumes and pages from Crossref). Full texts NOT
obtained; quoted from the publisher abstracts. [SOURCE: abstracts on the doi.org landing pages,
as returned by Exa on 2026-09-24; no numbers are taken from them]

1995, 1990 census, California: "California's out-migration consists of two different migration
systems: first, an immigration-induced 'flight' that exports lower income and less-educated
Californians, primarily, to the nearby states of Washington, Oregon, Nevada and Arizona. And
second, a more conventional migration exchange with the rest of the United States that involves
the redistribution of better educated, higher income migrants. It is the former migration system
which appears to be most responsive to the low-skilled immigration flows". 1996, 1990–95: "migration
patterns among domestic migrants favoring areas that are not attracting immigrants; and
accentuated domestic outmigration away from high immigration areas that is most evident for less
educated and lower-income long-term residents."

Which side [INFERENCE]: the strongest published statement that natives left California and other
gateways as immigrants arrived, concentrated among less-educated, lower-income natives. It rests on
aggregate census flows and says nothing on motive: the skill gradient fits labour-market
competition and housing costs, and fits composition avoidance only on the untested argument that
richer natives can buy into whiter neighbourhoods inside the state while poorer ones must leave
it. No interval; no individual controls in what was read.

### 3.2 Wright, Ellis & Reibel (1997), "The Linkage between Immigration and Internal Migration in Large Metropolitan Areas in the United States" — grade C; disconfirms the flight reading

Economic Geography 73(2):234–254 (Crossref),
doi:10.1111/j.1944-8287.1997.tb00069.x. Full text NOT obtained. [SOURCE: Crossref abstract,
https://api.crossref.org/works/10.1111/j.1944-8287.1997.tb00069.x]
1980 and 1990 census microsamples, "five overlapping samples of the largest metropolitan areas …
and five mutually exclusive segments of the labor force". Verbatim: "the finding of a significant
linkage between internal migration and immigration depends critically on the empirical experiment
used. In direct opposition to previous published research, we conclude that net migration of the
native born for metropolitan areas is either positively related or unrelated to immigration. Our
models show that the net migration loss of unskilled native workers from metropolitan areas is
probably a function of those cities' population size rather than immigrant flow to them."

Which side [INFERENCE]: against metro-level native flight; the authors attribute Frey's pattern to
metro size and industrial restructuring. Same grade as Frey: aggregate metro regressions, no
motive measured, and by their own words the answer depends on the specification.

### 3.3 California leavers' stated reasons, 2010–2026 — grade D (descriptive), cross-reference to `moving_costs_and_surveys.md` Task 2

- PPIC (Hans Johnson, blog, May 6, 2021), from the CPS: "The vast majority of adults who left
  California in the 2010s cited jobs (49%), housing (23%), or family (20%) as the primary reason
  (according to the Current Population Survey)." [SOURCE:
  https://ppic.org/wp-content/uploads/whos-leaving-california-and-whos-moving-in-may-2021.pdf;
  cached `_cache/lit/ppic_whos_leaving_2021.pdf` / `.txt`, p. 2] All adults, not natives only; no
  SE; the grouping is not defined. If PPIC's "housing" follows the CPS code layout (1.4), the
  "better neighborhood" reason sits inside the 23% [INFERENCE].
- Berkeley IGS Poll #2019-08 (online, English and Spanish, 4,527 registered voters, September
  13–18, 2019). Question: "What is the main reason why you have considered moving out of the
  state? You may select more than one reason". Among voters giving serious or some consideration
  (Table 2, p. 3): high cost of housing 71%, high taxes 58%, political culture 47%,
  "Overcrowding/too many people" 38%, family 14%, lack of job opportunities 13%, other 26%.
  [SOURCE: https://escholarship.org/content/qt96j2704t/qt96j2704t.pdf; cached
  `_cache/lit/igs_2019_08.pdf` / `.txt`] Offered no crime, neighbourhood or composition option,
  and measures considering a move, not moving.

Which side [INFERENCE]: no 2010–2026 study found links California's domestic out-migration to its
Hispanic share. The stated-reason record names jobs, housing and family; it cannot exclude a
composition motive hidden behind those answers (1.4), but nothing in it points to one.

## Sources tried and failed
- Emerson, Yancey & Chai (2001) full text: `fetch_paper` on 10.2307/3088879 and
  10.1177/000312240106600607 failed; the academia.edu hit was a different paper. Abstract only (Crossref).
- Lewis, Emerson & Klineberg (2011) full text: `fetch_paper` failed; not in PMC (idconv). ERIC abstract only.
- Krysan (2002), "Whites Who Say They'd Flee", Demography 39:675, doi:10.2307/3180826: `fetch_paper`
  failed; not in PMC. Not covered. [GAP] Highest-value re-dispatch target for Gap 1.
- Frey (1995, Urban Studies 32:733, doi:10.1080/00420989550012861; 1995, Population and
  Environment; 1996, PDR): `fetch_paper` failed for all three; Crossref carries no abstract.
- Kritz & Gurak (2001), Demography 38:133–145 (doi:10.2307/3088293 and 10.1353/dem.2001.0006):
  `fetch_paper` failed; Springer `/content/pdf/` for both DOIs and a guessed Duke UP URL returned
  HTML. Not covered. [GAP]
- White & Liang (1998), Population Research and Policy Review 17:141–166,
  doi:10.1023/a:1005961111419: `fetch_paper` failed. Not covered. [GAP]
- Ellen (2000), Crowder (2000), Krysan & Bader (2007): not attempted within the turn budget. [GAP]
- PPIC "Who's Leaving California" March 2023 PDF: downloaded, but `pdftotext` returns garbled
  font encoding (5 lines); not used.
- The old NCBI idconv endpoint (`www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/`) returned non-JSON;
  the current one (`pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/`) worked.

Suggested next queries if re-dispatched: Krysan 2002 via Springer DOI search; Kritz & Gurak 2001
tables via a university reading-list PDF; Lewis et al. 2011 Table 2 (Hispanic-share coefficient
and SE); Ellen (2000) race-based neighbourhood stereotyping; any study adding tract crime to the
PSID out-migration models.
