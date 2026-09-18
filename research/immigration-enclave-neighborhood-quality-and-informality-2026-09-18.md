claude-opus-5[1m]

# Neighborhood maintenance and storefront formality in immigrant enclaves

**Verdict:** **H1 NOT SUPPORTED AS A GROUP EFFECT. H2 FALSIFIED.**

Four tests, two of them new since the first draft, and they converge.

The descriptive pattern the hypothesis points at is real. The Mission scores 3.12 on San
Francisco's 1–5 inspector litter scale against 2.50 in Chinatown, a gap of 0.67 points
adjusted for land use (t = 7.6), and Chinatown has the city's second-lowest household
income, highest poverty rate and highest crowding. That much holds and is not in dispute.

It does not survive as a **group** effect on any identified design.

**San Francisco, within neighborhoods.** Joining 7,291 audited blockfaces to their own
census tract across 235 tracts reproduces the coarse estimate exactly (+0.018 per point of
Hispanic share, t = 6.1, with tract income), then it falls by two-thirds to **+0.0056,
t = 2.00** once neighborhood fixed effects compare tracts inside the same neighborhood. For
**Mexican-origin share, the hypothesis as stated, the within-neighborhood estimate is
indistinguishable from zero (t = 1.53)**. Illegal dumping, graffiti and feces all lose
significance entirely. Housing crowding predicts litter at least as strongly as Hispanic
share does, and the tract poverty rate carries the wrong sign. What the neighborhood dummies
absorb is cleaning routes and frequencies, Community Benefit District coverage, refuse
contracts, commercial zoning, transit and tourist volume, and the political geography of
service delivery.

**The national household test.** In the American Housing Survey 2023, 55,669 households, at
equal household income, tenure, metro, structure age and crowding, Mexico-born householders
are **no more likely to live in physically inadequate housing (−0.05 percentage points,
t = −0.06; replicate-weight t = −0.08)**, report **no more abandoned buildings** and by the
replicate-weight estimate slightly fewer (t = −2.52), report **no more petty crime
(t = 0.62) or serious crime (t = 1.08)**, and rate both their neighborhoods (+0.27 points on
a 1–10 scale, replicate-weight t = 5.7) and their homes **better** than comparable
non-Hispanic households. Unit adequacy is the only outcome in the battery that is a physical
assessment rather than a perception, and it is flat.

**What survives, and it is narrow.** Trash within half a block remains higher for Hispanic
householders at equal income: +0.87 percentage points on a 2.5% base, replicate-weight
t = 2.64. For Mexican-origin householders specifically it is **not** significant (t = 1.72).
That single small effect agrees in sign and in smallness with the within-neighborhood San
Francisco estimate, and it is the whole of the surviving evidence.

**Los Angeles agrees.** Across 138 ZIP codes, Hispanic share predicts illegal dumping at
t = 5.4 raw and **t = 1.1 once income enters**, graffiti at t = 4.9 then t = 0.3; the
illegal-dumping-per-bulky-item-pickup ratio, built to divide out reporting propensity, flips
sign.

Three further findings point the same way. The San Francisco effect is **three times larger
on commercial blocks than residential ones** (0.033 versus 0.012 per point), which is not
where household housekeeping would put it. Chinatown, the counterexample the income story
cannot absorb, receives the city's **second-highest street-cleaning intensity** — 12,080
requests per square kilometre per year against 2,088 in Excelsior — so its cleanliness comes
after unusually heavy cleaning. And the Mission's $201,026 mean household income is a
number produced by a gentrification that removed about 3,000 Hispanic residents between 2011
and 2023, so the neighborhood-level income control was never controlling for the households
the hypothesis is about.

The largest robust ethnic gap anywhere in this memo is **bars on windows**, +5.2 points for
Mexico-born householders. It is not a maintenance measure: bars are installed by owners
against perceived burglary risk, they are a durable feature of older housing stock, and the
item counts *other* buildings within half a block. It describes a neighborhood's built
environment and security history, not how its residents keep it.

H2 is dead. Using San Francisco's commercial-vacancy-tax registry as the storefront
denominator — the parcel universe, after correcting a circularity in my own first pass —
**90.9% of occupied commercial spaces on Mission Street between 14th and Cesar Chavez have
an active business registration at the address**, against a citywide 83.6%. Valencia Street
is 92.6%, Columbus Avenue in North Beach 87.2%, Clement Street 83.4%, Geary Boulevard 82.8%
and Irving Street 62.8%. At neighborhood level the Mission is 89.9% and Chinatown 90.5%, a
gap of 0.6 points. There is no Mission informality gap in the storefront-registration data.
What registration cannot see — cash wages behind registered storefronts — is real, and the
repo has already sized it at $1.5k–$3.4k per unauthorized adult per year, first generation
only (§7).

Model self-report: `claude-opus-5[1m]`. Teammate lane, 2026-09-18.
Instrument-bias caveat applies (`notes/llm-bias-caveat.md`); this is a politically charged
question and the measures below were chosen before the results were seen.

---

## 1. What each measure can and cannot say

| Measure | What it is | What it cannot say |
|---|---|---|
| **SF Street & Sidewalk Maintenance Standards** (`qya8-uhsz`) | City Controller / Public Works inspectors score randomly sampled blockfaces on a fixed rubric: litter 1–5, graffiti counts, illegal dumping, broken glass, feces, sidewalk defects. 7,318 evaluations, Jan 2022 – Jun 2025. **Observational, not complaint-driven.** | Cannot attribute a condition to residents. A dirty block may reflect visitors, commerce, the unsheltered population, or a city that cleans it less. |
| **311 service requests** (`vw6y-z8j6`, 8.9M cases) | Resident and worker *complaints*. | Confounds condition with propensity to complain. Under-reports in lower-income, lower-English, immigrant neighborhoods. |
| **Commercial vacancy tax registry** (`rzkk-54yv`) | Every ground-floor commercial space in the city's designated commercial districts, with vacancy and filing status, 2022–2025. | Landlord-side. The `filed` flag measures the *owner's* compliance, not the tenant's. |
| **Registered Business Locations** (`g8m3-pdis`) | Active SF business tax registrations with addresses and coordinates. | Registration is not tax compliance. A registered business can still pay cash wages. |
| **HSH quarterly tent/vehicle count** (`w9ip-yrij`) | Field count of tents, structures and lived-in vehicles, 31 quarters 2019-04 → 2026-05. | Coarse; quarterly point counts. |

The 311 and audit measures disagree, and the disagreement is itself a finding (§5).

## 2. San Francisco: observed conditions by neighborhood

[SOURCE: DataSF `qya8-uhsz`, Street & Sidewalk Maintenance Standards Results Jan 2022 –
Jun 2025, fetched 2026-09-18; ACS 2019–2023 5-year via Census API, tracts aggregated to
Analysis Neighborhoods with DataSF crosswalk `sevw-6tgi`.]

Sidewalk litter is scored 1 = none, 2 = a few traces, 3 = more than a few traces but no
accumulation, 4 = distributed litter with some accumulation, 5 = widespread with
significant accumulation. Full table: `infra/immigration-fiscal/enclave_quality_2026_09_18/table1_sf_street_eval_by_group.csv`.

| Evaluation group | n routes | Sidewalk litter | Graffiti / route | Dumping (any) | Mean HH income | Hispanic % | NH Asian % | Poverty % | Crowded % |
|---|---|---|---|---|---|---|---|---|---|
| Bayview Hunters Point | 437 | **3.41** | 8.4 | 0.38 | $132,265 | 24.4 | 38.7 | 16.0 | 13.9 |
| Mission | 405 | **3.12** | **84.7** | 0.53 | $201,026 | 33.0 | 16.3 | 12.5 | 9.0 |
| Tenderloin | 121 | 3.00 | 75.3 | 0.43 | $75,910 | 25.2 | 29.3 | 26.7 | 12.9 |
| Portola / Visitacion Valley | 291 | 2.98 | 5.4 | 0.36 | $145,937 | 21.2 | 59.5 | 10.3 | 14.4 |
| Outer Mission | 302 | 2.92 | 18.3 | 0.31 | $182,702 | 23.4 | 58.6 | 9.4 | 12.1 |
| Excelsior | 309 | 2.89 | 12.2 | 0.35 | $153,569 | 30.6 | 48.7 | 9.8 | 12.6 |
| South of Market | 196 | 2.85 | 43.9 | 0.35 | $161,995 | 16.4 | 40.5 | 20.3 | 10.1 |
| Russian Hill / Nob Hill / **North Beach** | 405 | 2.57 | 32.3 | 0.29 | $181,874 | 12.1 | 29.9 | 9.9 | 4.6 |
| **Chinatown** | 135 | **2.50** | 32.0 | 0.30 | **$80,483** | 4.2 | 81.3 | **28.8** | **22.9** |
| **Japantown** / Pacific Heights | 255 | 2.45 | 15.0 | 0.31 | $245,427 | 9.8 | 20.1 | 7.4 | 2.8 |
| Marina | 213 | 2.40 | 12.8 | 0.22 | $306,838 | 9.4 | 10.9 | 4.6 | 3.3 |
| West of Twin Peaks | 544 | 2.18 | 6.1 | 0.13 | $274,549 | 10.2 | 36.2 | 4.7 | 1.6 |
| Noe Valley / Glen Park / Twin Peaks | 338 | 2.17 | 6.5 | 0.25 | $280,557 | 12.2 | 18.3 | 5.4 | 1.7 |

**Sampling design.** The evaluated routes are a random sample of San Francisco street
segments, stratified by street type (residential versus commercial/mixed use) and by
neighborhood group, each segment evaluated once per period, with surveys spread across the
year and across all weekdays so that weather, refuse-collection days and street-sweeping
schedules average out. Each survey covers both sides of a street between two intersections.
The sampling methodology was revised in July 2023 to support neighborhood-level reporting,
so the four evaluation periods are not perfectly comparable; every regression below carries
period fixed effects. [SOURCE: https://www.sf.gov/data--street-and-sidewalk-maintenance-standards
and the FY25 Annual Street & Sidewalk Maintenance Standards Report,
https://media.api.sf.gov/documents/FY25_Annual_Street_Sidewalks_Report.pdf, fetched 2026-09-18]

**Pairwise differences in mean sidewalk litter**, raw and adjusted for the commercial dummy
and evaluation period, heteroskedasticity-robust:

| Comparison | Raw difference | Adjusted | t (adjusted) | n routes |
|---|---|---|---|---|
| Mission − Chinatown | +0.62 | **+0.67** | 7.6 | 540 |
| Mission − Marina | +0.72 | +0.66 | 9.7 | 618 |
| Mission − Japantown/Pacific Heights | +0.67 | +0.62 | 9.5 | 660 |
| Mission − Russian Hill/Nob Hill/North Beach | +0.55 | +0.56 | 9.1 | 810 |
| Excelsior − Chinatown | +0.40 | +0.43 | 3.8 | 444 |
| Chinatown − Tenderloin | −0.50 | **−0.60** | −5.2 | 256 |

The Mission is about 0.67 points dirtier than Chinatown on a 1–5 scale, three-quarters of a
standard deviation, and Chinatown is 0.60 points cleaner than the Tenderloin at almost
identical income and poverty. These are the specific comparisons the hypothesis names, and
they go the hypothesis's way.

Three things in this table matter more than the rest.

**Chinatown is the counterexample the income theory needs and does not get.** It has the
second-lowest mean household income in the city ($80,483), the highest poverty rate
(28.8%), the highest crowding (22.9% of occupied units above one person per room), 71%
foreign-born residents, and 76% of its evaluated routes are commercial. It scores 2.50 on
sidewalk litter — cleaner than the citywide average and cleaner than eleven higher-income
neighborhoods. [SOURCE: same]

**The worst-scoring neighborhood is not Hispanic.** Bayview Hunters Point, at 3.41, is 38.7%
Asian and 23.3% Black with 24.4% Hispanic. Any account that runs purely on Mexican origin
has to explain Bayview first.

**The Mission's graffiti count is an outlier, not a gradient.** 84.7 instances per evaluated
route against 32.0 in Chinatown, 32.3 in the North Beach group and 6.1 west of Twin Peaks.
Graffiti in the Mission is a documented local phenomenon with its own street-art culture
and is not interchangeable with litter as a maintenance measure. [INFERENCE]

## 3. Does it survive controls at neighborhood level? Yes for litter, no for feces

> **Superseded in part by §4.** Everything in this section uses 24-unit neighborhood-group
> composition. §4 redoes it at census-tract level and adds neighborhood fixed effects, which
> cuts these coefficients by two-thirds. Read §3 as the descriptive between-neighborhood
> result and §4 as the identified one.

[Files: `table8_sf_robustness.csv`, `table9_sf_leave_one_out.csv`, `table10_sf_group_residuals.csv`.]

Route-level OLS, standard errors clustered on the 24 evaluation groups, evaluation-period
fixed effects throughout. Coefficient shown is on Hispanic population share, in points of
the outcome per percentage point of share.

| Outcome | +income, land use | + density | + street homelessness | + tenure, crowding, Black share | poverty instead of income |
|---|---|---|---|---|---|
| Sidewalk litter (1–5) | 0.022 (t 4.6) | 0.021 (t 5.1) | **0.019 (t 5.7)** | 0.017 (t 4.6) | 0.021 (t 4.6) |
| Street litter (1–5) | 0.013 (t 3.3) | 0.013 (t 3.3) | 0.010 (t 4.4) | 0.011 (t 4.2) | 0.012 (t 4.0) |
| Sidewalk litter ≥ 4 (share) | 0.008 (t 5.0) | 0.008 (t 5.8) | 0.007 (t 7.1) | 0.006 (t 5.9) | 0.008 (t 5.8) |
| Any illegal dumping | 0.005 (t 2.1) | 0.005 (t 2.3) | 0.004 (t 2.9) | 0.005 (t 3.2) | 0.005 (t 3.1) |
| Graffiti count | 1.00 (t 1.4) | 1.11 (t 1.7) | 0.83 (t 2.1) | 1.21 (t 3.2) | 0.77 (t 2.1) |
| **Feces count** | 0.015 (t 1.3) | 0.018 (t 1.5) | **0.006 (t 0.6)** | −0.001 (t −0.1) | 0.006 (t 0.7) |

The feces row is the honest control check. It is the outcome most obviously produced by
unsheltered homelessness rather than by residents, and the Hispanic-share coefficient goes
to zero the moment street homelessness enters. The litter and dumping coefficients do not.
That asymmetry is evidence the litter result is not simply a homelessness artefact.

Magnitude: 10 percentage points of Hispanic share buys 0.19 points of sidewalk litter, 0.21
standard deviations. Across the actual range in San Francisco (Marina 9.4% to Mission
33.0%) that is about half a standard deviation.

**Leave-one-out.** Dropping each evaluation group in turn, the coefficient moves between
0.0174 and 0.0226 and never falls below t = 3.85. Dropping the Mission gives 0.0182
(t = 3.89); dropping Chinatown gives 0.0174 (t = 5.62). The result is not a Mission artefact.

**Residuals.** After income, density, street homelessness, land use and period, the groups
that are dirtier than predicted are Excelsior (+0.38), Outer Mission (+0.29), Mission
(+0.27) and Portola/Visitacion Valley (+0.27); the cleanest relative to prediction are
Chinatown (−0.47) and the Tenderloin (−0.38). Excelsior, Outer Mission and Portola are
*majority-Asian* neighborhoods with large Hispanic minorities, which complicates a
straightforwardly Mexican-origin reading. Japantown/Pacific Heights (+0.16) and the Marina
(+0.14) are also dirtier than predicted, and they are the wealthiest and least Hispanic
places in the sample.

## 4. The tract-level test: the association is between neighborhoods, not within them

[SOURCE: route-centroid coordinates from "Streets and Sidewalks Maintenance Standards Survey
Coordinates Crosswalk.xlsx", the Controller's attachment to DataSF `qya8-uhsz`, 3,474 routes,
fetched 2026-09-18; joined point-in-polygon to 2020 census tracts and to ACS 2019–23
tract data. Script `sf_tract_level_test.py`, tables `table22_*`, `table23_*`.]

§3 assigns each audited blockface the composition of a 24-unit neighborhood group. That is
a coarse instrument, and §10 explains why neighborhood-mean income is the wrong control in a
gentrifying district. The Controller publishes route centroids, so each blockface can carry
the composition and income of **its own census tract** instead. 7,291 of 7,318 evaluations
(99.6%) matched, across **235 tracts**.

Coefficient on Hispanic population share, sidewalk litter on the 1–5 scale, cluster-robust
by tract:

| Specification | Hispanic share | t | per 10 pp, in sd | Mexican-origin share | t |
|---|---|---|---|---|---|
| Raw | 0.0208 | 6.90 | 0.23 | 0.0325 | 5.66 |
| + tract income | 0.0178 | 6.09 | 0.20 | 0.0264 | 4.72 |
| + land use, period | 0.0179 | 6.54 | 0.20 | 0.0264 | 5.05 |
| + density, street homelessness | 0.0163 | 7.39 | 0.18 | 0.0228 | 5.47 |
| + tenure, crowding, Black and Asian share | 0.0185 | 6.11 | 0.21 | 0.0226 | 4.23 |
| + poverty instead of income | 0.0176 | 7.81 | 0.20 | 0.0255 | 6.07 |
| **+ neighborhood-group fixed effects** | **0.0056** | **2.00** | **0.06** | **0.0065** | **1.53** |

The tract-level estimate reproduces §3 almost exactly — until neighborhood-group fixed
effects are added. Then it falls by two-thirds, to 0.06 standard deviations per ten points
of Hispanic share, marginally significant at p = 0.045; and for **Mexican-origin share
specifically, which is the hypothesis as stated, it is not statistically distinguishable
from zero (t = 1.53, p = 0.13)**.

Within neighborhoods, the other outcomes go away entirely:

| Outcome, within-neighborhood-group | Hispanic share | t | Mexican share | t |
|---|---|---|---|---|
| Sidewalk litter | 0.0056 | **2.00** | 0.0065 | 1.53 |
| Street litter | 0.0040 | 1.76 | 0.0011 | 0.36 |
| Sidewalk litter ≥ 4 | 0.0021 | 1.89 | 0.0034 | 2.00 |
| Any illegal dumping | −0.0006 | −0.45 | −0.0022 | −1.07 |
| Graffiti count | 0.304 | 1.73 | 0.153 | 0.60 |
| Feces count | 0.0101 | 1.41 | 0.0118 | 1.10 |

And within neighborhoods, Hispanic share is no larger a predictor than housing crowding,
while the poverty rate has the wrong sign:

| Within-group predictor of sidewalk litter | Coefficient | t | per 10 pp, in sd |
|---|---|---|---|
| Housing crowding (% of units > 1 person/room) | 0.0085 | 1.82 | 0.10 |
| Hispanic share | 0.0056 | 2.00 | 0.06 |
| NH Asian share | 0.0027 | 1.34 | 0.03 |
| NH Black share | −0.0030 | −0.65 | −0.03 |
| Poverty rate | −0.0047 | −0.96 | −0.05 |

**This is the most important result in the lane and it cuts against H1.** Essentially all of
the apparent association is *between* neighborhoods, and between-neighborhood variation is
exactly what is confounded with the things a neighborhood dummy absorbs: city cleaning
routes and frequencies, Community Benefit District coverage, refuse-contract terms,
commercial-corridor zoning, transit and tourist volume, and the political geography of
service delivery. When those are held fixed by comparing tracts inside the same
neighborhood, the litter gradient is one-third the size, and the Mexican-origin gradient
the hypothesis actually names disappears into noise.

The fixed-effects specification is not free of cost: neighborhood groups are large, several
are internally homogeneous, and absorbing them throws away real variation along with the
confounds. A defender of H1 can say the fixed effects are over-controlling. But the
direction of the evidence is unambiguous, and the burden it places on H1 is specific: the
claim now needs a mechanism that operates at the scale of a whole neighborhood rather than
at the scale of the households on a block.

## 5. The 311 evidence points the other way, and that is informative

[SOURCE: DataSF `vw6y-z8j6`, 8,923,552 cases; 2019–2025 window; denominators are ACS
2019–23 neighborhood population and active registered business counts. Table: `table4_sf_311_rates.csv`.]

Across 36 neighborhoods, Hispanic share predicts **nothing** in the 311 complaint rate.
Street-and-sidewalk-cleaning requests per 1,000 residents per year: β = 3.8, t = 0.63 raw;
t = 0.20 with income; t = 0.37 with the full control set. Graffiti requests: t = −0.10.
All 311 requests: t = 0.22. [SOURCE: `table5_sf_311_regressions.csv`]

The brief's disconfirmation clause said that if 311 rates per resident are similar across
enclaves at equal income, H1 fails on the SF evidence. On 311, it does fail. The reason it
fails is visible in two neighborhoods:

| | Sidewalk litter (observed) | 311 cleaning requests per 1,000 residents/yr | Hispanic % | Foreign-born % |
|---|---|---|---|---|
| Mission | 3.12 | **912** | 33.0 | 30.3 |
| Excelsior | 2.89 | **195** | 30.6 | 44.1 |
| Chinatown | 2.50 | 480 | 4.2 | 71.0 |
| Hayes Valley | 2.61 | 737 | 12.6 | 22.7 |

Excelsior has nearly the same observed litter as the Mission and one-fifth the complaint
rate. Two neighborhoods of near-identical Hispanic share differ almost fivefold in
complaints. 311 is measuring who calls the city, not what the street looks like. This is a
concrete, local instance of the known reporting-propensity bias in 311 data, and it means
any analysis of neighborhood quality built on 311 volume — including analyses that would
have supported H1 by pointing at the Mission's 912 — is measuring the wrong thing.
[INFERENCE, from the two-column comparison above]

## 6. H2: storefront formality

[SOURCE: DataSF `rzkk-54yv` Taxable Commercial Spaces, tax year 2024, fetched 2026-09-18;
DataSF `g8m3-pdis` Registered Business Locations, 99,106 active locations, fetched
2026-09-18. Script: `h2_storefront_registration_v2.py`. Tables `table6v2_*`, `table7v2_*`.]

San Francisco's Commercial Vacancy Tax requires every ground-floor commercial space in the
city's designated commercial districts to be registered with the Treasurer, whether or not
it is occupied. That registry is an independent storefront census and a far better
denominator than OpenStreetMap, which is volunteer-maintained and unevenly complete.

**A correction to my own first pass, which matters for the number.** The registry carries a
`lin` (Location Identification Number) that is built from the business tax account number:
`lin` = `<ban>-NN-NNN`. Restricting the denominator to rows that have a `lin` therefore
conditions on a business account already existing and makes any registration rate
circular. Only 4,439 of the 7,160 tax-year-2024 rows have one. The circularity is
measurable: among occupied spaces with a `lin`, 90.7% have an active registration at the
address; among those without, 77.4%. The numbers below use the **parcel universe** —
5,223 distinct `parcelnumber` + situs-address commercial spaces, LIN or no LIN. Situs
addresses are often ranges ("369-373 West Portal Av"), so a space counts as registered if
any active registered business has a house number inside the range on the same street.
The `filed` flag turns out to be perfectly collinear with having a `lin` in the 2024 data
(both 47.9%), so it carries no independent information and is not used as a compliance
measure.

Citywide, **83.6% of occupied commercial spaces have an active business registration at
the address** (92.1% allowing a four-house-number tolerance).

| Corridor | Spaces | Vacant % | **Registration %** |
|---|---|---|---|
| Stockton St, Chinatown | 54 | 5.6 | **98.0** |
| Castro St | 125 | 2.4 | 95.0 |
| Grant Ave, Chinatown | 58 | 5.2 | **94.5** |
| Haight St | 95 | 4.2 | 93.4 |
| Valencia St, 14th–Cesar Chavez | 501 | 2.6 | 92.6 |
| Polk St | 218 | 5.5 | 92.2 |
| Union St, Cow Hollow | 147 | 3.4 | 91.5 |
| **Mission St, 14th–Cesar Chavez** | **612** | **2.5** | **90.9** |
| Ocean Ave, Ingleside | 103 | 3.9 | 90.9 |
| **24th St, Mission–Potrero** | 184 | 3.8 | **89.8** |
| Columbus Ave, North Beach | 264 | 2.7 | 87.2 |
| Mission St, Excelsior | 246 | 2.0 | 86.6 |
| Fillmore St | 162 | 0.6 | 85.7 |
| 24th St, Noe Valley | 135 | 0.0 | 85.4 |
| Post St, Japantown | 89 | 2.2 | 85.1 |
| Clement St, Inner Richmond | 211 | 2.4 | 83.4 |
| Geary Blvd, Richmond | 226 | 2.2 | 82.8 |
| **Irving St, Inner Sunset** | 117 | 2.6 | **62.8** |

Mission Street sits at 90.9%, above the citywide 83.6% and above Columbus Avenue in North
Beach (87.2%), Post Street in Japantown (85.1%), Clement Street (83.4%), Geary Boulevard
(82.8%) and Irving Street (62.8%). Valencia Street, one block over, is 92.6%. Chinatown's
two corridors are the highest in the city at 94.5% and 98.0%.

By neighborhood, occupied spaces, minimum 30: Nob Hill 95.1, Castro/Upper Market 94.1,
West of Twin Peaks 92.9, Outer Richmond 92.1, Japantown 92.1, Marina 91.8, Haight Ashbury
91.2, **Chinatown 90.5**, **Mission 89.9**, Russian Hill 89.9, Glen Park 88.6,
Sunset/Parkside 86.9, Pacific Heights 86.8, Excelsior 86.8, Portola 86.4, North Beach 85.7,
Hayes Valley 85.5, Noe Valley 85.4, Oceanview/Merced/Ingleside 85.2, Bernal Heights 84.7,
Inner Richmond 83.7, Outer Mission 82.1, Lone Mountain/USF 79.6, Western Addition 72.4,
Presidio Heights 70.1, Inner Sunset 61.3, Visitacion Valley 60.0, South of Market 54.6,
Bayview Hunters Point 11.6.

**The Mission and Chinatown are within 0.6 percentage points of each other.** That is the
brief's stated disconfirmation condition for H2, and it is met.

**Caveats.** Bayview Hunters Point at 11.6% is almost certainly a data artefact rather than
an 88% informality rate: its commercial parcels are large industrial lots whose situs
addresses are parcel references, and the ±4 tolerance barely moves it (15.1%), which is the
signature of an address-space mismatch rather than of missing registrations. South of
Market (54.6%) and Presidio Heights (70.1%) are likely affected by the same problem in
milder form — multi-tenant buildings where the registration is filed at a different street
number. The tolerance column in `table6v2_sf_storefront_registration.csv` is the diagnostic:
neighborhoods whose rate jumps under tolerance (Visitacion Valley 60.0 → 93.3, Presidio
Heights 70.1 → 95.4) are matching problems; the Mission barely moves (89.9 → 96.3), so its
rate is not being propped up by tolerance. The registry also covers only the designated
commercial districts, and registration says nothing about payroll or sales-tax compliance,
which is what H2 was really reaching for; see §7.

## 7. What the storefront data cannot reach, and what the repo already knows

Registration measures whether a storefront has a business-tax certificate. It says nothing
about whether that business pays its employees on the books. The repo has already measured
the wage-side channel directly, and the answer there is not zero:

> "the *net* uncredited-tax loss from off-the-books unauthorized work [is] roughly **$1.5k–$3.4k
> per unauthorized adult per year** — real, but 13–29% of the −$11.5k Mexico-born gap … For
> the **US-born second generation the channel is approximately zero on the tax side**."
> [SOURCE: `infra/immigration-fiscal/informal_channel_2026_09_16/RESULT.md`]

That is the right place to look for informality, and it is a labour-market phenomenon, not
a storefront phenomenon. The SSA actuaries' own accounting puts 3.9M of 7.0M unauthorized
workers entirely off payroll in 2010, and the IRS net-misreporting rate is 1% for withheld
wages against 57% for nonfarm proprietor income. [SOURCE: same file, citing SSA Actuarial
Note 151 and IRS Pub 5784.] A storefront with a business registration and cash-paid staff
shows up as formal in §6 and informal in the tax gap. **H2 as stated — "a large share of
storefront businesses in the Mission are not registered" — is false. A weaker claim about
cash wages behind registered storefronts is not tested here and is not refuted here.**

California's Labor Enforcement Task Force publishes inspection results by industry, and
reports that more than 80% of its targeted inspections find non-compliance; its target
industries are car washes, restaurants, garment manufacturing, roofing, construction,
agriculture and auto repair. [SOURCE: https://www.dir.ca.gov/letf/letf.html, fetched
2026-09-18.] Those are selected inspections of suspected violators, so the 80% is a hit
rate on a targeted sample and carries no information about base rates by neighborhood or
by owner ethnicity. It cannot be used to support or refute H2.

## 8. The national household test (American Housing Survey 2023)

**At equal household income, tenure, metro, structure age and crowding, Mexico-born
householders are no more likely to live in physically inadequate housing, report no more
abandoned buildings, no more crime, and rate their neighborhoods and homes distinctly
better. The one maintenance-relevant item with any residual signal is trash within half a
block, and for Mexican origin specifically it is not significant once the survey's own
replicate weights are used.**

[SOURCE: AHS 2023 National Public Use File v1.0 flat CSV,
https://www2.census.gov/programs-surveys/ahs/2023/, downloaded and analysed 2026-09-18.
141,729,433 bytes, verified byte-exact; the zip opens to `ahs2023n.csv`, 837,082,564 bytes
uncompressed, 3,208 columns, **55,669 households**. Weighted Hispanic-householder share
13.57%, against roughly 14% in ACS, which is the sanity check that `HHSPAN == 1` is the
right recode. `HHNATVTY` code 057 is the United States (78.4% of non-missing) and code 303
is Mexico (n = 2,247). Scripts `modal_ahs_run.py` and `modal_ahs_codes.py`; tables
`table18*`, `table19_ahs_regressions_signed.csv`, `table20_ahs_sdr_se.csv`,
`table21_ahs_income_bands.csv`.]

**How this was run, and why.** The local link was saturated for the whole lane — Census
served fresh range requests at 17–27 kB/s and an unrelated control host at 1.6 kB/s — and a
resumed local download lost ground twice. The file was therefore downloaded and analysed in
a cloud container, which returns only the result tables. That is option (b): running the
regressions in the container rather than shipping 141 MB back over the same link. The
container verified the byte count, that the zip opens, and that the header has 3,208
columns before doing anything else.

**Version note.** A v1.1 of the national PUF exists. It has 3,214 columns against v1.0's
3,208 and the same 55,669 households, and for every variable used here — `NEARTRASH`,
`NEARABAND`, `NEARBARCL`, `ADEQUACY`, `HHSPAN`, `RATINGNH`, `NHQPCRIME` — the two versions
have **identical distributions**. [SOURCE: `table18b_ahs_version_check.csv`] The results
below are unaffected by the version choice.

### 8.1 The variable codings had to be established, not assumed

The brief's guessed names were partly wrong and the response scales were not what a yes/no
reading would suggest. Both corrections change what the coefficients mean.

- The litter, abandoned-buildings and bars-on-windows items are **`NEARTRASH`,
  `NEARABAND`, `NEARBARCL`**, not `NHQTRASH`/`NHQABAN`/`NHQBAN`. The `NHQ*` names the brief
  gave for crime, schools, transit and risk are correct.
- `NEARTRASH` is the **frequency** of trash, litter or junk within half a block;
  `NEARABAND` is the **number** of abandoned or vandalised buildings; `NEARBARCL` is the
  **number** of buildings with bars on windows. [SOURCE: AHS 2023 Mini Codebook,
  https://www.census.gov/data-tools/demo/data/uccb/ahsdict/minicodebooks/ahs_mini_2023National.pdf;
  2023 AHS Definitions, https://www2.census.gov/programs-surveys/ahs/2023/2023%20AHS%20Definitions.pdf]
  None is a yes/no item, so `== 1` cannot be assumed to mean "problem present".

Code order was therefore determined from the data, by the weighted mean of `RATINGNH`, the
respondent's own 1–10 rating of the neighborhood, within each category:

| Variable | Code 1 | Code 2 | Code 3 | Code 4 | Severe category |
|---|---|---|---|---|---|
| `NEARTRASH` mean rating | **6.28** (2.5%) | 7.01 (6.0%) | 8.48 (81.0%) | — | **1** |
| `NEARABAND` mean rating | 7.32 (2.4%) | **6.17** (2.5%) | 8.39 (80.4%) | 8.99 (3.8%) | **2** |
| `NEARBARCL` mean rating | 7.69 (1.8%) | **7.28** (6.8%) | 8.43 (79.8%) | — | **2** |
| `ADEQUACY` mean rating | 8.36 (93.9%) | 7.59 (4.2%) | 7.15 (1.9%) | — | 2 and 3 |

For trash, code 1 is the worst, matching the questionnaire's large-amount / small-amount /
none structure (`EJUNK1`, `EJUNK2`). For abandoned buildings and bars on windows the worst
category is **2, not 1**, so a naive `== 1` indicator would have pointed at the wrong
group. [SOURCE: `table18c_ahs_category_ordering.csv`]

The `NHQ*` items are agree/disagree and their polarity differs by item: `NHQPCRIME` "this
neighborhood has a lot of petty crime" and `NHQRISK` "at high risk for floods or other
disasters" are negative, while `NHQSCHOOL` "has good schools" and `NHQPUBTRN` "has good
bus, subway, or commuter train service" are **positive amenities**. Outcome names below
reflect that.

### 8.2 Results

Weighted least squares on `WEIGHT`. Coefficients are in percentage points for the binary
outcomes and in rating points for `nh_rating`. "Full" is income, tenure, metro (`OMB13CBSA`),
census division, structure age and structure type; "+crowding" adds persons per room and
household size.

**Mexico-born householder** (the hypothesis as stated):

| Outcome | Raw | + income | Full | + crowding |
|---|---|---|---|---|
| Physically inadequate unit | +1.88 (t 2.71) | +1.52 (t 2.20) | +1.06 (t 1.49) | **−0.05 (t −0.06)** |
| Large amount of trash within ½ block | +2.63 (t 4.30) | +2.43 (t 3.97) | +1.54 (t 2.47) | +1.07 (t 1.69) |
| Any trash within ½ block | +4.65 (t 4.87) | +4.20 (t 4.40) | +2.08 (t 2.15) | +0.84 (t 0.85) |
| Abandoned buildings, severe category | +0.97 (t 1.78) | +0.73 (t 1.32) | **+0.12 (t 0.21)** | −0.53 (t −0.90) |
| Bars on windows, severe category | +8.13 (t 8.19) | +7.75 (t 7.83) | **+5.16 (t 5.40)** | +4.35 (t 4.48) |
| Agrees: a lot of petty crime | +5.99 (t 5.23) | +5.13 (t 4.48) | **+0.70 (t 0.62)** | −1.13 (t −0.98) |
| Agrees: a lot of serious crime | +3.02 (t 3.67) | +2.41 (t 2.94) | **+0.89 (t 1.08)** | −0.23 (t −0.27) |
| Agrees: good schools | −0.74 (t −0.93) | −0.49 (t −0.61) | +0.56 (t 0.69) | +1.48 (t 1.73) |
| Agrees: good transit | +18.76 (t 13.48) | +18.17 (t 13.03) | **+12.41 (t 9.17)** | +10.75 (t 7.78) |
| Agrees: high disaster risk | −0.34 (t −0.43) | −0.58 (t −0.73) | **−2.37 (t −2.94)** | −2.68 (t −3.22) |
| Neighborhood rating, 1–10 | −0.056 (t −1.16) | −0.023 (t −0.46) | **+0.173 (t 3.60)** | +0.265 (t 5.35) |

**Hispanic householder, all origins:**

| Outcome | Raw | + income | Full | + crowding |
|---|---|---|---|---|
| Physically inadequate unit | +1.92 (t 4.94) | +1.62 (t 4.19) | +0.98 (t 2.43) | **+0.28 (t 0.67)** |
| Large amount of trash within ½ block | +2.16 (t 6.79) | +2.00 (t 6.30) | +1.16 (t 3.61) | +0.87 (t 2.67) |
| Abandoned buildings, severe category | +1.15 (t 3.75) | +0.95 (t 3.09) | +0.40 (t 1.23) | **−0.01 (t −0.03)** |
| Bars on windows, severe category | +9.40 (t 16.84) | +9.11 (t 16.39) | +4.76 (t 8.92) | +4.35 (t 7.99) |
| Agrees: a lot of petty crime | +8.04 (t 11.98) | +7.40 (t 11.02) | +3.35 (t 4.85) | +2.29 (t 3.22) |
| Agrees: good transit | +20.39 (t 25.42) | +19.97 (t 24.84) | +10.33 (t 13.08) | +9.42 (t 11.68) |
| Neighborhood rating, 1–10 | −0.163 (t −5.92) | −0.137 (t −4.96) | **+0.063 (t 2.24)** | +0.122 (t 4.22) |

**Replicate-weight standard errors.** AHS is a complex sample, so the HC1 errors above
understate uncertainty. Re-fitting the fullest specification on all 160 replicate weights
and taking the successive-difference estimate, Var = (4/160)·Σ(bᵣ − b)²:

| Regressor | Outcome | Coefficient | SDR standard error | t |
|---|---|---|---|---|
| Hispanic | Physically inadequate unit | +0.0028 | 0.0039 | **0.72** |
| Hispanic | Trash within ½ block | +0.0087 | 0.0033 | 2.64 |
| Hispanic | Abandoned buildings | −0.0011 | 0.0027 | **−0.39** |
| Hispanic | Bars on windows | +0.0089 | 0.0027 | 3.24 |
| Hispanic | Neighborhood rating | +0.1220 | 0.0288 | **+4.24** |
| Mexico-born | Physically inadequate unit | −0.0005 | 0.0061 | **−0.08** |
| Mexico-born | Trash within ½ block | +0.0107 | 0.0062 | **1.72** |
| Mexico-born | Abandoned buildings | −0.0099 | 0.0039 | **−2.52** |
| Mexico-born | Bars on windows | +0.0074 | 0.0047 | **1.57** |
| Mexico-born | Neighborhood rating | +0.2650 | 0.0468 | **+5.66** |

[SOURCE: `table20_ahs_sdr_se.csv`]

### 8.3 The plain equal-income comparison

Weighted means, no regression. [SOURCE: `table21_ahs_income_bands.csv`]

| Household income | Group | Inadequate unit | Large amount of trash | Abandoned buildings (code 1) | Neighborhood rating |
|---|---|---|---|---|---|
| Under $25k | non-Hispanic | 8.2% | 4.0% | 3.5% | 8.11 |
| Under $25k | Hispanic | 10.8% | 6.5% | 2.9% | 7.98 |
| $25–50k | non-Hispanic | 5.5% | 3.4% | 3.8% | 8.24 |
| $25–50k | Hispanic | 8.5% | 5.6% | 4.1% | 8.04 |
| $50–75k | non-Hispanic | 4.4% | 2.9% | 3.1% | 8.25 |
| $50–75k | Hispanic | 4.8% | 4.8% | 3.2% | 8.22 |
| $75–100k | non-Hispanic | 4.2% | 2.1% | 2.8% | 8.35 |
| $75–100k | Hispanic | 3.9% | 3.8% | 1.4% | 8.28 |
| $100–150k | non-Hispanic | 2.6% | 1.2% | 1.7% | 8.43 |
| $100–150k | Hispanic | 4.0% | 3.1% | 2.1% | 8.33 |
| $150k+ | non-Hispanic | 2.5% | 1.1% | 1.3% | 8.64 |
| $150k+ | Hispanic | 4.2% | 2.4% | 3.8% | 8.39 |

Within-band incomes match closely (for example $38,273 against $38,043 in the $25–50k band),
so this is a genuine like-for-like comparison and not the column-misalignment failure that
the consumption lane had to correct. The raw gaps are real but small in level terms, and the
adequacy gap closes above $50k while the trash gap does not.

### 8.4 What this does and does not establish

**Against H1, strongly.** Unit adequacy is the one outcome here that is a physical
assessment of the dwelling rather than a perception, and for Mexico-born householders the
gap is **−0.05 percentage points, t = −0.06** at equal income and crowding, and
**+1.06 points, t = 1.49** even without the crowding controls. Abandoned buildings show no
gap and by the replicate-weight estimate slightly fewer (t = −2.52). Perceived petty and
serious crime, which drove the raw differences hard, go to zero once metro and income enter
— they were describing which metros Mexican immigrants live in, not their blocks. Both
groups rate their neighborhoods and their homes **better** than comparable non-Hispanic
households at the same income.

**For H1, narrowly.** The trash item survives for all-Hispanic householders at
+0.87 percentage points on a 2.5% base with a replicate-weight t of 2.64. That is a real
but small effect, and for **Mexican-origin householders specifically it is not significant
(t = 1.72)**. It is the only maintenance-relevant item in the battery that points the
hypothesis's way, and it agrees in sign, and roughly in smallness, with the
within-neighborhood San Francisco estimate in §4.

**Neither, honestly.** Bars on windows is the largest and most robust gap in the table,
+5.2 points for Mexico-born householders. It is not a maintenance measure. Bars are
installed by owners against perceived burglary risk, they are a durable feature of an older
housing stock, and the item counts *other* buildings within half a block, so it describes a
neighborhood's built environment and security history rather than how its residents keep
it. Reading it as evidence of either neglect or crime would be wrong in both directions.

**Limits.** `RATINGNH` and `RATINGHS` are subjective; a higher rating at equal income could
reflect different reference points rather than better conditions, and the positive
coefficients should not be read as "Mexican immigrants live in objectively better
neighborhoods". The crowding control is contestable — if the hypothesis means that more
people per room produces more wear, then controlling for persons per room removes part of
the mechanism rather than a confound, which is why both specifications are shown; note that
the Mexico-born adequacy coefficient is insignificant either way. And AHS varies households
*within metros*, so a group effect operating at whole-metro scale would be absorbed by the
metro dummies, just as the San Francisco neighborhood dummies absorb one at neighborhood
scale.

## 9. Los Angeles: the income control wins

[SOURCE: MyLA311 Service Request Data 2019–2025, data.lacity.org resources `pvft-t768`,
`rq3b-xjk8`, `97z7-y5bt`, `i5ke-k6by`, `4a4x-mna2`, `b7dx-7gc3`, `h73f-gn57`, fetched
2026-09-18; ACS 2019–23 5-year ZCTA via Census API. 138 ZIPs with population ≥ 5,000.]

**Jurisdiction warning.** MyLA311 covers the City of Los Angeles. **East Los Angeles is
unincorporated county territory and does not appear in this data at all.** The brief named
East LA as a test site; it cannot be tested here. ZIP 90063 spans City Terrace and the city
edge and is included with that caveat.

The measure worth the most here is **illegal-dumping reports per bulky-item pickup request**.
Los Angeles gives residents free scheduled bulky-item collection. Both numerator and
denominator are 311 calls, so the ratio largely divides out the reporting-propensity problem
that wrecks the raw rates, and it asks a sharp question: when a household has a mattress to
get rid of, does it call the city or leave it on the kerb?

| Outcome, per 1,000 residents/yr | Hispanic share, raw | + income | + income, race shares, tenure, crowding |
|---|---|---|---|
| Illegal dumping pickup | **0.276 (t 5.43)** | 0.090 (t 1.12) | −0.063 (t −0.50) |
| Graffiti removal | **0.956 (t 4.87)** | 0.110 (t 0.32) | −0.026 (t −0.06) |
| Bulky items | 0.447 (t 1.89) | 0.457 (t 1.12) | 0.179 (t 0.22) |
| Homeless encampment | 0.001 (t 0.02) | −0.152 (t −2.81) | −0.186 (t −1.73) |
| **Dumping per bulky-item request** | **0.0019 (t 2.26)** | −0.0005 (t −0.32) | −0.0024 (t −1.30) |

**In Los Angeles the raw association is large and the income-adjusted association is zero.**
Hispanic share predicts illegal dumping at t = 5.4 with nothing in the model, and at
t = 1.1 once mean household income enters. Graffiti collapses from t = 4.9 to t = 0.3. The
dumping-to-bulky ratio flips sign. On this evidence the pattern is an income effect, which
is the brief's disconfirmation condition for H1.

Neighborhood councils, dumping per bulky-item request: Downtown Los Angeles 1.34 and 0.87
(two spellings of the same council in the data), Pico-Union 0.97, Westlake South 0.76,
**North Westwood 0.45**, South Central 0.45, MacArthur Park 0.42, Sun Valley 0.41. At the
clean end: Pacific Palisades 0.026, Porter Ranch 0.027, Bel Air–Beverly Crest 0.043,
Northwest San Pedro 0.042, Sherman Oaks 0.069, Eagle Rock 0.063. *(Parent note: the council
cache finished loading after the lane's first table; `table14` was regenerated from the completed
cache and the second-spelling rows moved at the second decimal, ranking unchanged.)* North Westwood — the
student district around UCLA, 6% Hispanic — is fifth worst in the city. [SOURCE:
`table14_la_nc_dump_ratio.csv`]

Focus ZIPs [SOURCE: `table13_la_focus_zips.csv`]:

| Area | ZIP | Hispanic % | Mean HH income | Crowded % | Dumping/bulky |
|---|---|---|---|---|---|
| Boyle Heights S | 90023 | 96.1 | $70,049 | 30.0 | 0.29 |
| City Terrace / E LA edge | 90063 | 93.7 | $86,538 | 23.2 | 0.17 |
| Boyle Heights N | 90033 | 89.8 | $68,844 | 26.4 | 0.19 |
| Pacoima | 91331 | 87.5 | $98,598 | 23.5 | 0.22 |
| Koreatown / Pico-Union | 90006 | 70.9 | $67,837 | 31.4 | 0.29 |
| Westlake / MacArthur Park | 90057 | 68.3 | $58,907 | 32.7 | 0.31 |
| South LA (Vermont Knolls) | 90044 | 67.2 | $70,206 | 19.3 | 0.32 |
| Koreatown | 90005 | 47.7 | $81,488 | 21.0 | 0.15 |
| South Park / Pico-Union | 90015 | 45.3 | $103,796 | 20.7 | **0.51** |
| Highland Park | 90042 | 56.5 | $125,850 | 10.4 | 0.08 |
| **Venice** | 90291 | **14.3** | **$188,925** | 2.4 | **0.17** |
| Westchester | 90045 | 19.1 | $175,995 | 3.3 | 0.07 |
| Sherman Oaks | 91403 | 16.0 | $183,910 | 2.1 | 0.08 |

Venice, at 14% Hispanic and $189k mean household income, dumps at the same rate as City
Terrace at 94% Hispanic. Highland Park, 56% Hispanic but gentrified to $126k, is at 0.08,
cleaner than every wealthy Westside ZIP except Westchester. The variable that moves this
measure is income and street population, not origin.

## 10. Gentrification: "cannot maintain" and "is being displaced from" are different stories

[SOURCE: ACS 5-year, Census API, tract-level, aggregated to Analysis Neighborhoods;
2011–2019 on 2010 tract boundaries, 2021–2023 on 2020 boundaries — the series has a
definitional break at that point and the two halves should not be differenced across it.]

| Mission District | 2011 | 2013 | 2015 | 2017 | 2019 | 2021 | 2023 |
|---|---|---|---|---|---|---|---|
| Total population | 55,220 | 56,873 | 57,873 | 58,630 | 58,770 | 57,018 | 54,431 |
| Hispanic population | 21,043 | 21,893 | 22,707 | 22,088 | 20,962 | 19,620 | **17,985** |
| Hispanic share | 38.1% | 38.5% | 39.2% | 37.7% | 35.7% | 34.4% | **33.0%** |

The Mission has lost roughly 3,000 Hispanic residents since 2011 while its total population
was flat and then fell. Outer Mission fell from 6,598 to 5,091 Hispanic residents and
Excelsior from 12,659 to 11,607. Over the same period Hispanic population rose in the
Tenderloin (5,177 → 8,055), the Marina (1,576 → 2,237) and North Beach (1,105 → 1,490).

This matters for the hypothesis in a specific way. The Mission's $201,026 mean household
income is the income of a neighborhood that has been substantially recomposed. When the
§3 and §4 regressions "control for income," they are controlling for a neighborhood average that
increasingly describes households who are not the ones the hypothesis is about. The
direction of that bias is not obvious: it makes the Mission look richer than its Latino
residents are, which should make the litter look *worse*-than-predicted for spurious
reasons, and inflate the estimated Hispanic coefficient. That is an argument for
discounting the §3 result, and it is the reason the household-level AHS test is the one
that settles this.

## 11. What the enclave literature says

Cutler, Glaeser and Vigdor find that selection into enclave neighborhoods is on balance
negative, but that correcting for that selection yields positive mean effects of residential
concentration, larger for groups with higher average human capital; residence *near* rather
than *in* an enclave is where the benefit concentrates. [SOURCE:
https://www.nber.org/papers/w13082, NBER WP 13082, 2007; published *Journal of Urban
Economics* 63(3), 2008.] Applied here, it predicts that enclaves of different origin groups
should show different outcomes for reasons that run through group human capital rather than
through enclave residence as such — which is consistent with a Chinatown/Mission gap and
is not the same claim as the operator's.

Edin, Fredriksson and Åslund exploit a Swedish refugee-placement policy that assigned
arrivals to municipalities independently of their preferences and find that enclave
residence *raised* earnings for less-skilled immigrants. [SOURCE: *Quarterly Journal of
Economics* 118(1), 2003, "Ethnic enclaves and the economic success of immigrants".] It is
the cleanest identification in this literature and it points away from enclave residence
being the damaging variable. Neither paper measures physical neighborhood upkeep, so
neither speaks directly to H1; they bound how much of any enclave difference should be
attributed to the enclave itself.

## 12. Where the San Francisco effect actually lives: commercial blocks, not residential ones

[SOURCE: `table15_sf_robustness2.csv`, `table16_sf_cleaning_effort.csv`.]

Splitting the audit sample by the inspectors' own land-use classification changes the
reading materially.

| Sample | Routes | Hispanic-share coefficient on sidewalk litter | t |
|---|---|---|---|
| All routes (income, land use, density, homelessness) | 7,318 | 0.0188 | 5.69 |
| + city cleaning effort control | 7,318 | 0.0183 | 6.35 |
| **Residential routes only** | 5,065 | **0.0115** | 3.04 |
| **Commercial / mixed-use routes only** | 2,253 | **0.0329** | 6.87 |
| Below-median-income groups | 3,590 | 0.0233 | 7.69 |
| Above-median-income groups | 3,728 | 0.0118 | 3.94 |
| Dropping Bayview, Tenderloin and SoMa | 6,564 | 0.0182 | 5.34 |

**The association is roughly three times larger on commercial blocks than on residential
blocks.** Ten points of Hispanic share buys 0.33 points of sidewalk litter on a commercial
corridor and 0.12 points on a residential street — the latter about an eighth of a standard
deviation. The hypothesis as the operator framed it is about how people keep the place they
live. On the blocks where people live, the effect is real but small; most of the measured
gap sits on shopping streets, where the plausible drivers are pedestrian volume, food
retail density, waste-contract coverage and hours of operation rather than resident
housekeeping. [INFERENCE]

**The Chinatown counterexample has a competing explanation that has to be stated.**
Chinatown receives 12,080 street-and-sidewalk-cleaning requests per square kilometre per
year, the second-highest service intensity in San Francisco after the Tenderloin (20,112),
against 2,088 in Excelsior and 1,518 in Bayview Hunters Point. Chinatown is also a
Community Benefit District with its own funded cleaning crews, and it is a tourist
destination the city has reason to keep presentable. Its 2.50 litter score is not a clean
read of resident behaviour; it is an outcome after an unusually large amount of cleaning.
[SOURCE: `table16_sf_cleaning_effort.csv`; CBD status from DataSF `c28a-f6gs`.] The same
qualification applies in reverse to Excelsior and Outer Mission, which score badly on
one-fifth of the Mission's service intensity. Controlling for cleaning effort does not move
the coefficient (0.0183 vs 0.0188), but cleaning effort is endogenous to litter — the
control enters positively, t = 3.6, because the city cleans where it is dirty — so that
control is close to uninformative.

## 13. Reading the five tests together

| Test | Units | Instrument | Hispanic share / origin, income controlled |
|---|---|---|---|
| SF inspector audit, neighborhood composition | 24 groups | observational | +0.019 per pp, t = 5.7 |
| SF inspector audit, tract composition | 235 tracts | observational | +0.018 per pp, t = 6.1 |
| **SF audit, tract composition, neighborhood FE** | 235 tracts | observational | **+0.0056, t = 2.00**; Mexican t = 1.53 |
| **AHS 2023, households within metros** | 55,669 households | inspected adequacy + self-report | **adequacy t = −0.06; trash t = 1.72 (Mexico-born)** |
| SF 311 complaint rates | 36 neighborhoods | complaint-driven | zero (t = 0.2 to 0.6) |
| MyLA311 complaint rates | 138 ZIPs | complaint-driven | zero, negative with full controls |

Two contrasts do the work.

**Between versus within, in San Francisco.** Moving from neighborhood-group composition to
tract composition changes nothing, which rules out simple aggregation error and confirms the
tract data reproduces the coarse result. Adding neighborhood fixed effects cuts the estimate
by two-thirds and takes the Mexican-origin estimate below conventional significance. So the
variance carrying the association is the variance *between* neighborhoods, and that variance
is loaded with everything a city does differently from one neighborhood to the next.

**Perception versus physical assessment, nationally.** In AHS the raw ethnic gaps are large
and the income-and-metro-adjusted gaps are not. Perceived petty crime falls from +6.0 points
to +0.7 for Mexico-born householders; serious crime from +3.0 to +0.9. The one outcome that
is a physical assessment of the dwelling rather than a perception — unit adequacy — is flat
at equal income and crowding, and insignificant even without the crowding controls. The raw
gaps were largely describing which metropolitan areas Mexican immigrants live in.

Both readings that were open before these two tests are now resolved in the same direction,
so the earlier symmetric presentation no longer holds. What remains is a specific residual
and a specific objection.

**The residual.** Trash within half a block is higher for Hispanic householders at equal
income, +0.87 percentage points on a 2.5% base, replicate-weight t = 2.64, and higher on
tracts with more Hispanic residents inside the same San Francisco neighborhood, +0.0056
points of litter per percentage point, t = 2.00. Two independent instruments, one national
and one local, agree in sign and in smallness on this one item. Neither is significant for
Mexican origin specifically. An honest statement of the surviving finding is: *litter,
slightly, not adequacy, not dumping, not graffiti, not crime, and not specifically Mexican.*

**The objection.** Neighborhood fixed effects in §4 and metro fixed effects in §8 both
absorb any group mechanism that operates at their own scale. If norms, collective
enforcement or merchant-association formation work at neighborhood or metro scale, these
designs subtract the effect along with the confound. That objection is legitimate and it is
not answerable with the data here. But it now has to carry the whole hypothesis, and it has
to explain why unit adequacy — a physical measure with no service-geography component —
shows nothing, and why the Mexican-origin coefficient specifically is the one that
disappears in both designs.

## 14. What would change the verdict

- **A physical neighborhood-condition measure at household level.** AHS settles unit
  adequacy, which is inspected, but its neighborhood battery is respondent-reported. A
  household-level survey with an enumerator assessment of the *block* rather than the
  dwelling would test the surviving trash residual on a non-perceptual instrument. No such
  national file exists to my knowledge. **[GAP]**
- **A within-metro replication of the AHS result on the metropolitan PUF.** The AHS 2023
  metropolitan file identifies 35 metros and would allow metro-by-metro estimates rather
  than one pooled coefficient, testing whether the national null hides offsetting positives
  and negatives. Not run. **[GAP]**
- **A second observational instrument.** Los Angeles CleanStat (Bureau of Sanitation
  quarterly street-cleanliness assessments by sanitation district) is the direct analogue of
  the San Francisco audit and is the single highest-value remaining item, because it would
  test the between-neighborhood result out of sample in a city whose complaint data already
  says no. It is not on data.lacity.org; a public-records route or the Bureau's published
  CleanStat maps would be needed. **[GAP]**
- **A design that separates neighborhood-scale group mechanisms from municipal service
  geography.** This is what §4 cannot do and what Reading A in §13 needs. Candidates: a
  regression discontinuity at Community Benefit District boundaries, where cleaning
  intensity jumps but composition does not; or a panel on the July 2023 change in Public
  Works route assignment. **[GAP]**
- **A tract-level estimate with the tracts, not the neighborhoods, as the fixed effect.**
  The audit samples each route once per period, so within-tract-over-time variation in
  composition is too small to identify anything over four periods. A longer audit panel
  would fix this. **[GAP]**
- **A service-intensity instrument.** Something exogenous to litter that shifts city
  cleaning effort — a Community Benefit District boundary discontinuity, or the staggered
  rollout of Public Works' Pit Stop programme — would let the Chinatown counterexample be
  read cleanly. **[GAP]**
- **For H2, a payroll measure.** Registration is settled. Cash wages behind registered
  storefronts are not, and no public dataset answers it at neighborhood level; the repo's
  existing informality memo is the right instrument and it works at the national level.

## 15. Framing and instrument caveats

[FRAMING-SENSITIVE] The hypotheses as posed attribute a physical condition to a group. Every
measure available here observes the condition, not the attribution. A street with more
litter is consistent with residents who litter, with visitors who litter, with a city that
cleans less, with denser commerce, with more people per square kilometre, and with a larger
unsheltered population. The audit design controls the last three imperfectly and the first
two not at all. That limit is structural, not a matter of adding covariates.

[INSTRUMENT BIAS] `notes/llm-bias-caveat.md` applies. The specific risk in a lane like this
is asymmetric scepticism: applying harder disconfirmation to the result that supports the
operator's hypothesis than to the one that refutes it. The record here is checkable in both
directions. The audit result was put through leave-one-out, five nested control sets, a
land-use split, an income split, a service-effort control and a homelessness control, and it
survived all of them; it was written up as supporting H1 before the tract-level test existed,
and the earlier verdict text is in this file's git history. It then failed the
within-neighborhood test, and the verdict was rewritten. The H2 result was put through a
second pass that found a circularity in my own first denominator and moved the Mission's
registration rate from 85.3% to 90.9%. The AHS pass caught two coding errors of my own
before they reached a conclusion: the neighborhood battery items are `NEAR*` rather than the
`NHQ*` names the brief supplied, and for abandoned buildings and bars on windows the severe
response category is code 2, not code 1, so a naive indicator would have measured the wrong
group. Code order was then fixed empirically from the respondents' own neighborhood ratings
rather than assumed. All corrections are reported with their mechanism so the asymmetry can
be audited rather than taken on trust.

## 16. Files

Scripts and outputs are in `infra/immigration-fiscal/enclave_quality_2026_09_18/`:
`acs_sf_neighborhoods.py`, `sf311_pull.py`, `sf_streeteval_pull.py`, `sf_business_pull.py`,
`sf_storefront_pull.py`, `sf_geo_context.py`, `sf_quality_analysis.py`,
`sf_quality_robustness.py`, `sf_quality_robustness2.py`, `sf_311_analysis.py`,
`sf_hispanic_series.py`, `sf_tract_level_test.py`, `la311_pull.py`, `acs_zcta_la.py`,
`la311_analysis.py`, `h2_storefront_registration.py`, `h2_storefront_registration_v2.py`,
`h2_match_sensitivity.py`, `ahs_analysis.py` (local runner, guards the exact byte count),
`modal_ahs.py`, `modal_ahs_run.py`, `modal_ahs_codes.py`, and tables `table1` through
`table23`. The two tests that decide the question are `sf_tract_level_test.py` (§4) and
`modal_ahs_run.py` plus `modal_ahs_codes.py` (§8); re-run those first. The AHS run logs
`ahs_run_log.txt` and `ahs_codes_log.txt` carry the byte-count, column-count and
weighted-share verifications.
`BRIEF.md` holds the dispatch prompt verbatim. `RESULT.md` holds the short verdict.
