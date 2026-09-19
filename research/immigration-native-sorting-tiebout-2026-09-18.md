claude-opus-5[1m]

## Audit correction — September 19, 2026

**“Tax-driven” overstates the design.** Retain the descriptive association and the tax-rate comparison; the data do not identify moving motives. Native population change includes natural increase and IRS filer movement does not isolate natives. The index should say more strongly associated with taxes, with causal motives unresolved. [SOURCE: the memo's own scope limitations; mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


**Verdict:** The third-order channel is real in California, an order of magnitude too small
to matter fiscally, and not attributable to the Mexican-origin gap. California's net outflow
of adjusted gross income rose from about zero in 2012-2016 to $20.6bn in 2021 and $17.2bn in
2023; at ITEP's 12.1% effective state and local rate on top earners that is $2.1bn of revenue
in 2023, **1.1% of the state's $189.3bn Mexican-origin fiscal gap** and about $53 per
resident. Texas holds the same Mexican-origin share, 31.7-33.5% against California's
31.8-32.5%, and runs a net AGI **inflow** of $6.4bn a year throughout. Across 51 states and
twelve tax-year pairs, net out-migration of $200k-plus filers tracks the effective top-1%
tax rate (standardised beta +0.31, interval excluding zero on every outcome) and not the
Mexican-origin share (−0.12, interval spanning zero, and zero under region fixed effects).
At metro level the apparent native displacement is a normalisation artefact: −0.013 when the
regressor is the change in immigrant share, **+1.69 natives gained per Mexican-origin arrival**
when both sides are scaled by the same fixed base population, which reproduces Peri &
Sparber's (2011) critique of Borjas (2006) on a fresh 2010-2023 sample. The shift-share
instrument fails its strength gate (first-stage F 0.3 to 9.0 against a threshold of 10), so
nothing here is causal. [UNVERIFIED by any second party; all numbers reproducible from the
stored panels, commands in `RESULT.md`.]

Purpose: test whether natives, especially high-AGI filers, net-out-migrate from the states and metros where the Mexican-origin fiscal gap concentrates, and whether that erosion is large enough to matter fiscally.

---

## 1. What this lane can and cannot identify

Every estimate below is **correlational**. Movers' motives are unobserved in all three
data sources; nothing here randomises immigrant settlement. The shift-share instrument
that the literature uses for this purpose fails its own strength test on this sample
(section 3), so there is no identified causal quantity in this memo, only conditional
associations and an accounting exercise. [INFERENCE]

Three further limits, stated before results:

1. **No per-state fiscal gap exists.** The stress lane estimates gaps for four state
   groups (California, Texas, a five-state Southwest-plus-Illinois group, and the rest),
   not for fifty states. [SOURCE: `infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv`]
   The state regressions therefore use the Mexican-origin **share** as the exposure, and
   the four-group gaps only for the revenue arithmetic in section 4.
2. **The metro outcome is a population response, not an observed flow.** Native
   population growth contains natural increase and ageing as well as migration. It is the
   object Card (2001) and Borjas (2006) argue over, which is why it is used here, but a
   coefficient on it is not a migration elasticity. [INFERENCE]
3. **The IRS data have no nativity.** SOI counts tax filers, not natives. The nativity
   split comes from ACS microdata, which in turn has no income detail on out-migrants
   beyond the mover's own income. The two sources answer adjacent, not identical,
   questions.

## 2. Data

| Source | Unit | Years | Use |
|---|---|---|---|
| IRS SOI state migration, `<yy><yy>inmigall.csv` | state x AGI bracket | tax-year pairs 2011-12 onward | filer in/out flows and AGI by bracket [SOURCE: irs.gov/statistics/soi-tax-stats-migration-data] |
| ACS 1-year PUMS, `MIGSP`+`NATIVITY`+`PINCP` | person | selected years 2011-2023 | interstate flows split by nativity [SOURCE: api.census.gov/data/<yr>/acs/acs1/pums] |
| ACS 5-year detailed tables | metro (CBSA) | 2006-2010 and 2019-2023 windows | metro shares and native population [SOURCE: api.census.gov/data/<yr>/acs/acs5] |
| ACS 1-year detailed tables | state | 2011-2024 | state shares, rent, college, income [SOURCE: api.census.gov/data/<yr>/acs/acs1] |
| ITEP, *Who Pays?* 2024, effective state+local rate on the top 1% | state | 2024 law | tax-rate control and the revenue arithmetic [SOURCE: repo `data/itep/itep_table_5.tsv`, from itep.org] |
| Census 2000 SF3 metro origin base | metro | 2000 | shift-share instrument base, reused from the employment-entry lane [SOURCE: `infra/immigration-fiscal/employment_entry_2026_09_18/derived/metro_base_2000.csv`] |

Two data traps found and fixed while building this, both worth recording:

* The Census PUMS API accepts `MIGSP=1:56` as a range predicate and returns the **wrong**
  rows: foreign-country origin codes are included and own-state movers are dropped. The
  explicit OR list `MIGSP=001&MIGSP=002&...` is required. Validation after the fix: 2023
  California weighted domestic in-migrants come to 423,980, which matches the published
  ACS 2023 state-to-state flow for California. [SOURCE: own pull, 2026-09-18]
* `B03001` (Hispanic origin detail, the Mexican-origin variable) is published in the ACS
  1-year file for only 63-101 metros. The metro analysis therefore uses the 5-year file,
  which covers 846 metro and micro areas. [SOURCE: own pull]

The repo's existing metro panel
(`infra/immigration-fiscal/employment_entry_2026_09_18/derived/metro_year_panel.csv`) is
used here for a second treatment, the Mexico-**born** 18-64 share. Its per-sex `pop1864`,
`mex1864` and `fb1864` columns are identically zero, which looks like a defect but is not:
that lane puts the treatment block in the `sex == "T"` rows, which are dropped before the
per-sex outcome aggregation, and the live shares are the metro-level `t_pop1864`,
`t_mex1864`, `t_fb1864` columns and the `mex_share`/`fb_share` built from them. Checked:
367 distinct `mex_share` values across 377 metros in 2023, Los Angeles 13.34% against
New York 2.14%. [SOURCE: own check of the file and of `build_panel.py` lines 102-130.]
An earlier draft of this memo called those shares national; that was wrong and is
corrected here.

The two Mexican-origin measures are not interchangeable. Their **levels** correlate 0.93
across 370 metros in 2023, but their 2010-2023 **changes** correlate only 0.07, because the
Mexico-born 18-64 stock fell over the window while the US-born Mexican-origin generations
grew. Chicago is the clearest case: Mexican origin +2.46 points, Mexico-born 18-64 −1.71
points. [SOURCE: own computation.] The fiscal gap the brief asks about is measured on the
Mexican-origin union across three generations, so the ACS Mexican-origin share is the
matching exposure; the Mexico-born arm is reported alongside it because it is the variable
the immigration literature uses.

## 3. Metro-level: native population response, 2010 -> 2023

846 metro and micro areas observed in both ACS 5-year windows (Puerto Rico dropped).
Outcome: net change in native population over 2010-2023 divided by 2010 native population.
Treatment: change in the group's population share in percentage points. Weighted by 2010
native population, heteroskedasticity-robust standard errors.

A coefficient of −0.013 means a metro whose Mexican-origin share rose one point more than
another's had native population growth 1.3 percentage points lower over the thirteen years,
about 0.1 points a year.

| Treatment | raw | + size, age | + college | + rent | + region FE |
|---|---:|---:|---:|---:|---:|
| Mexican-origin share (all generations) | −0.005 | −0.015 | **−0.013** | −0.014 | −0.011 |
| Mexico-born 18-64 share (364 metros) | −0.029 | −0.020 | **−0.023** | −0.024 | −0.013 |
| foreign-born share | −0.009 | −0.004 | −0.007 | −0.007 | −0.007 |
| Asian share | +0.001 | −0.008 | **−0.013** | −0.014 | −0.013 |
| Cuban share | +0.060 | +0.093 | **+0.100** | +0.102 | +0.054 |

95% intervals, college specification: Mexican origin [−0.024, −0.003]; Mexico-born
[−0.036, −0.011]; Asian [−0.027, +0.001]; Cuban [+0.055, +0.145]; foreign-born
[−0.021, +0.006].
[SOURCE: `infra/immigration-fiscal/tiebout_sorting_2026_09_18/derived/metro_estimates.csv`]

Restricting to the 171 metros of 250,000 or more in 2010 roughly doubles the Mexican-origin
coefficient, to −0.027 [−0.041, −0.013] with the college control and −0.017 with region
fixed effects.

**The disconfirmation test bites here.** The Asian-share coefficient is the same size as
the Mexican-origin coefficient once college is controlled. Metros where the Asian share rose
lost native population growth at the same rate as metros where the Mexican-origin share rose,
and the Asian-origin population is not the population the fiscal gap is measured on. On the
metro evidence the association is a property of immigrant inflow in general, or of whatever
immigrant inflow correlates with, not of the Mexican-origin fiscal gap specifically.
[INFERENCE] The Cuban coefficient runs the other way but rests on a handful of Florida
metros and should not be read as evidence of anything.

### Shift-share IV: gate failed

The 2000-base instrument (the metro's share of the national 2000 Mexico-born or foreign-born
stock, times the national 2010-2023 change in that stock, scaled by 2010 population) does not
clear the first-stage F of 10 that the brief set as the stopping rule.

| Instrumented treatment | spec | coef | 95% CI | first-stage F |
|---|---|---:|---|---:|
| Mexican-origin share | raw | +0.061 | [−0.004, +0.126] | 9.0 |
| Mexican-origin share | + size, age | +0.026 | [−0.022, +0.073] | 8.0 |
| Mexican-origin share | + college | +0.046 | [−0.027, +0.118] | 5.8 |
| foreign-born share | raw | −0.040 | [−0.153, +0.074] | 2.1 |
| foreign-born share | + size, age | +0.095 | [−0.252, +0.442] | 0.3 |
| foreign-born share | + college | +0.079 | [−0.160, +0.318] | 0.4 |

Every F is below 10, so all six rows are reported as uninformative and no IV point estimate
is carried forward. This reproduces confidence-ladder entry 136: the past-settlement
instrument has little strength on post-2008 US metro data.
[SOURCE: same file; `research/immigration-confidence-ladder.md` entry 136 via the
employment-entry lane.]

### The sign is a normalisation artefact

The specification above regresses native population growth on the change in the immigrant
**share**. That share carries the native population in its denominator, so natives leaving
raises it mechanically. Peri & Sparber (2011) make exactly this argument against Borjas
(2006): "Borjas (2006) specifications are biased toward identifying displacement, and this
bias grows larger as the variance of native flows rises in proportion to the variance of
immigrant flows independently of their correlation." [SOURCE: 10.1016/j.jue.2010.08.005,
verbatim via `research/immigration-canon-citation-audit-2026-09-17.md` §C5.]

Rescaling both sides by the same fixed 2010 total population removes that denominator.
The coefficient then reads directly as natives gained per immigrant gained, and every sign
reverses:

| Treatment, per 100 of 2010 population | raw | + size, age | + college | + region FE |
|---|---:|---:|---:|---:|
| Mexican origin | +1.66 | +1.34 | **+1.69** | +1.50 |
| foreign born | +2.30 | +2.73 | **+2.73** | +2.46 |
| Asian | +1.83 | +1.96 | **+1.89** | +1.39 |
| Cuban | +3.05 | +4.57 | **+4.93** | +2.93 |

95% intervals, college specification: Mexican [+1.26, +2.12]; foreign born [+1.81, +3.64];
Asian [+0.21, +3.56]; Cuban [+0.59, +9.27].
[SOURCE: `derived/metro_estimates.csv`, arm `OLS per-capita`.]

Metros that gained immigrants gained natives too, roughly 1.7 natives per Mexican-origin
arrival. Neither specification identifies a causal effect, and the positive version is just
as contaminated, by metro-level demand shocks that attract everyone. The finding is that
**the displacement sign in this data is produced by the normalisation, not by the data**,
which is Peri & Sparber's claim reproduced on a fresh 2010-2023 sample rather than on
Borjas's 1960-2000 one. [INFERENCE] A reader who wants a displacement number from a metro
cross-section should take neither of these.

### Is rent the mechanism?

Adding the 2010-2023 change in log median gross rent to the share specification moves the
Mexican-origin coefficient from −0.013 to −0.016, and rent growth itself enters
**positively**, +0.69 [+0.50, +0.89]: metros where rents rose fastest gained native
population fastest. [SOURCE: `derived/metro_estimates.csv`, arm `OLS +d_lrent (mediator)`.]
Rent growth is jointly determined with population growth here, so this is not a clean
mediation test, but on this cross-section rising rents are a marker of places natives moved
**to**. That is a poor fit for the story in which immigrants raise housing costs and natives
leave because of them, even granting Wilson & Zhou's (2026) causal magnitude of +1.4% rents
per inflow equal to 1% of initial employment. [SOURCE: Dallas Fed WP 2607 Table 6, rent
coefficient 1.438 (SE 0.344), via `research/immigration-urbanism-frontier-2026-06-25.md`.]

## 4. State-level: who actually leaves

Panel of 51 states (50 plus the District of Columbia) over IRS tax-year pairs 2011-12
through 2022-23, matched to ACS state characteristics. The 2014-15 pair is dropped from
every bracket-based series because the IRS's own `1415inmigall.csv` covers only fourteen
states, Alaska through Illinois. [SOURCE: own check, 108 data rows against 409 in the
neighbouring years.] All flow variables are net **out**-migration, so a positive number
means the state lost people or income on net.

### The two states that carry the fiscal gap move in opposite directions

California and Texas hold almost identical Mexican-origin population shares over the whole
period, and their taxpayer migration is the mirror image of each other.

| | Mexican-origin share, 2012 | 2023 | mean net out-migration of filers, % of non-migrant base | mean net AGI outflow |
|---|---:|---:|---:|---:|
| California | 31.8% | 32.5% | **+0.55** | +0.53% of resident AGI |
| Texas | 33.5% | 31.7% | **−0.63** | −0.88% of resident AGI |

California's net outflow of $200k-and-over filers rises through the period, from +0.07% in
2012 to a peak of +1.98% in 2021 and +0.88% in 2023. Texas runs a net **inflow** of the
same group in every year of the panel. [SOURCE:
`infra/immigration-fiscal/tiebout_sorting_2026_09_18/derived/state_panel.csv`]
Whatever is pushing high-income filers out of California, it is not the Mexican-origin
share, because Texas has the same share and gains them. [INFERENCE]

### The cross-state association

State means over the panel, 51 states:

| outcome | correlation with Mexican-origin share | correlation with ITEP top-1% tax rate |
|---|---:|---:|
| net out-migration, all filers | −0.18 | **+0.51** |
| net out-migration, $200k+ filers | −0.15 | **+0.42** |
| net AGI outflow | −0.17 | **+0.47** |
| net out-migration of natives (ACS) | −0.13 | **+0.27** |

The sign on the Mexican-origin share is negative throughout: states with more
Mexican-origin residents lose slightly **fewer** filers on net, not more.

Regression coefficients, year fixed effects throughout, standard errors clustered on state,
487-561 state-years. Units: percentage points of net out-migration per one point of
population share or of effective tax rate.

| outcome | Mexican-origin share | + region FE | ITEP top-1% rate | Asian share | foreign-born share |
|---|---:|---:|---:|---:|---:|
| all filers | −0.010 [−0.025, +0.006] | −0.000 | **+0.112 [+0.051, +0.172]** | −0.009 | −0.011 |
| $200k+ filers | −0.012 [−0.046, +0.022] | +0.014 | **+0.240 [+0.088, +0.392]** | +0.001 | −0.052 |
| net AGI | −0.010 [−0.035, +0.016] | +0.009 | **+0.223 [+0.118, +0.328]** | +0.008 | −0.039 |
| natives (ACS) | −0.011 [−0.031, +0.009] | −0.007 | +0.073 [−0.002, +0.149] | −0.009 | −0.023 |

All columns carry log population, the tax rate, median rent, college share and median
household income except where that variable is the regressor.
[SOURCE: `derived/state_estimates.csv`]

**The disconfirmation result the brief asked for is the tax column.** High-AGI
out-migration tracks the effective state and local tax rate on top earners, and the
association is four to twenty times larger than the Mexican-origin association and is the
only one whose interval excludes zero. The ten states that lose the most $200k-plus filers
are the District of Columbia, New York, Illinois, Alaska, Maryland, West Virginia,
California, Virginia, New Jersey and Minnesota; seven of the ten have Mexican-origin shares
under 4%. The ten biggest net gainers include Nevada (21.6% Mexican origin) and Arizona
(27.6%). [SOURCE: `derived/state_panel.csv`]

Adding state fixed effects leaves the Mexican-origin coefficient at −0.046 [−0.212, +0.121]
for all filers. There is almost no within-state movement in the Mexican-origin share over
twelve years, so that arm is a check on how much of the cross-sectional pattern is
between-state composition, not a preferred specification; it cannot reject anything.

## 5. The fiscal consequence for California and Texas

SOI reports the AGI on out-migrants' returns for the year they were still resident, and the
AGI on in-migrants' returns for the year after they arrived. Net outflow is the difference.

California's net AGI outflow, $bn a year:

| 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| −0.6 | +0.9 | +2.5 | +0.1 | +0.7 | +5.4 | +5.2 | +5.8 | +15.3 | +20.6 | +12.1 | +17.2 |

Twelve-year mean +$7.09bn a year; the $200k-and-over bracket alone averages +$3.29bn.
California is one of the fourteen states the incomplete 2014-15 IRS file does cover, so its
series has no hole. Texas runs the opposite sign in every year, a mean net AGI **inflow** of
$6.44bn a year, $3.26bn of it in the $200k-and-over bracket.
[SOURCE: `derived/revenue_arithmetic.csv`]

Applying ITEP's effective state and local tax rate on the top 1% of taxpayers, 12.1% in
California and 4.6% in Texas [SOURCE: ITEP, *Who Pays?* 7th edition, via
`data/itep/itep_table_5.tsv`]:

| | annual revenue effect, mean | 2023 | cumulative 2012-2023 |
|---|---:|---:|---:|
| California, all net AGI | −$0.86bn | −$2.08bn | −$10.3bn |
| California, $200k+ only | −$0.40bn | −$0.99bn | −$4.8bn |
| Texas, all net AGI | +$0.30bn | +$0.19bn | +$3.3bn |

Set against California's Mexican-origin fiscal gap of $189.3bn a year against the local
white reference, or $111.7bn against all local natives
[SOURCE: `infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv`,
`all_age_shared`, `mexican_observed_total`, `CA_age`]:

* the worst single year of lost revenue, 2021, is **1.3%** of the $189.3bn gap and **2.2%**
  of the $111.7bn version;
* the twelve-year cumulative $10.3bn is **0.45%** of twelve years of the $189.3bn gap;
* per California resident the 2023 figure is about **$53 a year**.

Two honest caveats on this comparison, both of which cut against reading the ratio as
precise. The revenue figure is **state and local only**, while the fiscal gap it is set
beside is a whole-of-government account covering federal, state and local budgets, so the
denominator is larger than the matching one would be. [SOURCE: the stress lane's account
definition.] And applying the top-1% effective rate to the entire net AGI flow overstates
the loss under California's progressive schedule, which is why the $200k-only row is shown
separately. Neither correction changes the order of magnitude: the flow is one to two orders
of magnitude smaller than the gap.

**Reading.** The Tiebout channel exists in California and it has grown sharply since 2019.
It is not small in absolute terms: $17bn of AGI leaving net in one year is real money, and
it is under 1% of resident AGI each year but compounds in the base. It is nonetheless far
too small to be a material part of the arithmetic of a gap measured in the hundreds of
billions, and the state with the same Mexican-origin share and a quarter of the tax rate
gains rather than loses. [INFERENCE]

## 6. Disconfirmation

The four checks were fixed before the results were read. Three of them fail the hypothesis
and one is ambiguous.

### 6.1 Does the same out-migration appear where other immigrant groups concentrate?

At metro level, in the share specification, the Asian-share coefficient on native population
growth is −0.013 [−0.027, +0.001], statistically indistinguishable from the Mexican-origin
coefficient of −0.013 [−0.024, −0.003]. In the population-scaled specification both are
positive and again similar, +1.89 and +1.69 natives per 100 residents per immigrant arrival.
The Cuban coefficient is the largest of all in both specifications and has the opposite sign
in the share version.

At state level the pattern differs by group but never favours the hypothesis. Cuban share
predicts large net **in**-migration of high-AGI filers, −0.35 to −0.47 percentage points per
point of share, the biggest coefficient in the table, which is Florida. Asian share is near
zero once controls are added.

**Result: fails.** The association is not specific to the population on which the fiscal gap
is measured. Groups with no measured gap produce coefficients of the same size or larger.

### 6.2 Does high-AGI out-migration track tax rates better than immigrant shares?

Both entered in the same regression, with log population, median rent, college share, median
household income and year fixed effects. Reported per standard deviation of the regressor,
which is 8.71 points of Mexican-origin share and 2.47 points of effective tax rate.

| outcome | Mexican-origin share, per SD | ITEP top-1% rate, per SD |
|---|---|---|
| net out-migration, all filers | −0.09 [−0.25, +0.07] | **+0.28 [+0.13, +0.42]** |
| net out-migration, $200k+ filers | −0.20 [−0.53, +0.14] | **+0.51 [+0.20, +0.82]** |
| net AGI outflow | −0.15 [−0.40, +0.10] | **+0.46 [+0.25, +0.66]** |
| net AGI outflow, $200k+ | −0.32 [−0.74, +0.09] | **+0.73 [+0.39, +1.08]** |
| net out-migration of natives (ACS) | −0.11 [−0.30, +0.09] | **+0.21 [+0.03, +0.39]** |
| net out-migration of $75k+ movers (ACS) | −0.02 [−0.04, +0.01] | +0.04 [−0.00, +0.07] |

Adding region fixed effects pushes every Mexican-origin coefficient to zero (standardised
beta between −0.10 and +0.01) and leaves the tax coefficient between +0.20 and +0.34.
[SOURCE: `derived/horse_race.csv`]

**Result: fails, decisively.** On every outcome the tax rate carries the association and the
Mexican-origin share does not. This is the single clearest finding in the lane.

### 6.3 Does the metro association survive the college-share control?

Yes. The Mexican-origin share coefficient is −0.005 raw, −0.015 with size and age, −0.013
with the college share added and −0.011 with region fixed effects; the interval excludes zero
in the last three. The college control is not what kills it. **Result: survives** — but 6.1
shows the surviving coefficient is not specific to Mexican origin, and the normalisation test
in section 3 shows its sign is not robust.

### 6.4 The housing-cost channel

Rent growth 2010-2023 enters the metro native-growth regression at +0.69 [+0.50, +0.89]:
metros where rents rose fastest gained the most native population. Controlling for it makes
the Mexican-origin coefficient slightly more negative, not less. At state level, median gross
rent is among the controls in every specification reported above and its inclusion does not
move the Mexican-origin coefficient toward significance. **Result: no support** for natives
being pushed out by immigrant-driven housing costs at this level of aggregation, while noting
that Wilson & Zhou's causal rent magnitude is a within-metro effect and this is a cross-metro
comparison, so the two are not in direct contradiction. [INFERENCE]

## 7. Steel-manning the null

The strongest version of the opposing case is not that natives never move. It is this.

**Card's own design finds no mobility response.** Card (2001) reports that native mobility
rates are "insensitive to immigrant inflows" while simultaneously finding that inflows reduced
wages and employment of low-skilled natives in gateway cities like Miami and Los Angeles by
1 to 3 percentage points. [SOURCE: 10.1086/209979, abstract, verified at source 2026-09-17 per
`research/immigration-canon-citation-audit-2026-09-17.md`.] Those two findings together are
the null's core: the local labour market absorbs the shock in prices, not in native
relocation. If natives were leaving, the local wage effect should have been arbitraged away.
This repo's own verdict on Card is HOLDS-NARROWLY, with the native-mobility null holding and
the wage magnitudes not identified as short-run causal effects.

**The one specification that finds displacement is the one shown to be mechanically biased
toward it.** Borjas (2006) finds roughly three natives displaced per ten immigrants at city
level and argues this accounts for 40 to 60 percent of the gap between national and local
wage estimates. [SOURCE: NBER w11610, verbatim via the canon audit §C5.] Peri & Sparber (2011)
run the microsimulation: "Of the models we explore, only the Borjas (2006) specifications
reveal a significantly negative correlation. Given the bias uncovered in Section 3, we suspect
that this finding for native displacement is spurious." [SOURCE: 10.1016/j.jue.2010.08.005.]
The repo's standing position grants the direction and treats the magnitude as
specification-sensitive; the 40-60% figure has already been withdrawn as a correction factor
for Card's Mariel coefficient.

**Section 3 of this memo is a fresh instance of that bias.** On 2010-2023 metro data the
displacement sign appears when the regressor is the immigrant share and disappears, reversing
to +1.7 natives per Mexican-origin arrival, when both sides are scaled by the same fixed base
population. That is Peri & Sparber's mechanism, reproduced on a sample they never saw.
[INFERENCE] It does not prove there is no native mobility response. It does mean a
cross-sectional metro regression cannot measure one, and that any repo claim resting on such
a regression should be read as uninformative rather than supportive.

**The housing story is coherent and this lane cannot refute it within a metro.** Immigrants
raise local housing costs, Wilson & Zhou put the causal magnitude at +2.2% house prices and
+1.4% rents per inflow equal to 1% of initial employment, and higher costs push some natives
out. Cross-metro, rent growth and native growth move together, because both are driven by
local demand. A within-metro or within-neighbourhood design with an instrument for the inflow
would be needed to separate them, and that design is not in this lane.

## 8. What this does and does not identify

**Does not identify.** Any causal effect of immigration on native location. The shift-share
instrument fails its strength gate on this sample (first-stage F of 0.3 to 9.0 against a
threshold of 10), so there is no instrumented estimate to report. Movers' motives are
unobserved in SOI, in the ACS mobility tables and in the metro panel. The cross-state tax
association is equally correlational: states set tax rates for reasons correlated with
everything else about them, and a filer who moves from California to Texas changes climate,
housing cost, industry mix and tax rate at once.

**Does identify, as description.** The direction and size of the flows. California loses
taxpayers and AGI on net and the loss has grown sharply since 2019. Texas, with the same
Mexican-origin share, gains them throughout. Across states the loss of high-AGI filers lines
up with the effective tax rate on top earners and not with immigrant shares. The dollar size
of California's net AGI outflow is one to two orders of magnitude below its measured
Mexican-origin fiscal gap.

**Cannot rule out.** A native mobility response operating below the state and metro level,
within-metro sorting across school districts and neighbourhoods, which is where the Tiebout
mechanism is usually argued to work and which no data source used here can see. A response
concentrated in specific skill groups; the ACS high-income arm here is $75,000-plus movers of
all nativities, not high-income natives specifically, because the published tables do not
cross income with nativity and the PUMS pull that would have was abandoned on throughput
(about 2.5 minutes per large state-year). And a longer-run response: twelve years of SOI and
thirteen of ACS is short against the horizon over which a tax base relocates.

## 9. Instrument bias

This memo was produced through a language model, which carries systematic post-training
dispositions on immigration. Two directions of that bias are worth naming against these
particular results. The finding that the tax rate rather than the immigrant share explains
high-income out-migration is the politically comfortable answer for the instrument, and it
should be held to a higher bar for that reason; the mechanism was preregistered in the brief
as a disconfirmation test and the coefficients are reproducible from the stored panel, which
is the defence available here. In the other direction, the finding that the normalisation
choice flips the metro displacement sign cuts against a claim this repo has previously leaned
on, and the model has no incentive to produce it. [SOURCE: `notes/llm-bias-caveat.md` for the
standing caveat.]

## 10. Sources

Primary data, all fetched 2026-09-18:

* IRS SOI state migration data, landing page
  <https://www.irs.gov/statistics/soi-tax-stats-migration-data>; files pulled individually
  as `https://www.irs.gov/pub/irs-soi/<yy><yy>inmigall.csv`,
  `stateinflow<yy>.csv`, `stateoutflow<yy>.csv` for tax-year pairs 1112 through 2223. The
  bundled `<yy><yy>migrationdata.zip` archives time out on irs.gov and require `--http1.1`;
  the loose CSVs do not. `1415inmigall.csv` is incomplete on the IRS side, 14 states only.
* Census Data API, ACS 1-year detailed tables,
  `https://api.census.gov/data/<year>/acs/acs1` for 2011-2024 (no 2020 release), tables
  B01003, B02001, B03001, B05002, B15003, B19013, B25064, and the mobility groups B07007,
  B07407, B07010, B07410.
* Census Data API, ACS 5-year detailed tables,
  `https://api.census.gov/data/<year>/acs/acs5` for the 2010 and 2023 endpoints, metro
  geography.
* Census Data API, ACS 1-year PUMS, `https://api.census.gov/data/2023/acs/acs1/pums`, used
  only to validate the interstate-flow definition against the published California figure.
* ITEP, *Who Pays? A Distributional Analysis of the Tax Systems in All 50 States*, 7th
  edition, via the repo copy at `data/itep/itep_table_5.tsv` (column "Current Tax Rate,
  Top 1% of All Taxpayers"), scraped from <https://itep.org/undocumented-immigrants-taxes-2024/>.

Repo inputs:

* `infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv` and
  `state_populations.csv` — the California and Texas Mexican-origin fiscal gaps.
* `infra/immigration-fiscal/employment_entry_2026_09_18/derived/metro_base_2000.csv`,
  `metro_year_panel.csv` — shift-share instrument base and the Mexico-born metro share.
* `research/immigration-canon-citation-audit-2026-09-17.md` §P1 and §C5 — Card, Borjas,
  Peri & Sparber, with abstracts verified at source on 2026-09-17.
* `research/immigration-urbanism-frontier-2026-06-25.md` — Wilson & Zhou housing magnitudes.
* `research/immigration-confidence-ladder.md` entry 136 — the weak post-2008 past-settlement
  instrument.

Literature cited through the canon audit rather than fetched again in this lane: Card (2001)
*Immigrant Inflows, Native Outflows*, JOLE, 10.1086/209979; Borjas (2006) *Native Internal
Migration and the Labor Market Impact of Immigration*, JHR, NBER w11610; Peri & Sparber
(2011) *Assessing Inherent Model Bias*, JUE 69(1):82-91, 10.1016/j.jue.2010.08.005;
Jaeger, Ruist & Stuhler (2018), NBER w24285. Wilson & Zhou (2026), Dallas Fed WP 2607,
<https://www.dallasfed.org/~/media/documents/research/papers/2026/wp2607.pdf>, Table 6.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).
