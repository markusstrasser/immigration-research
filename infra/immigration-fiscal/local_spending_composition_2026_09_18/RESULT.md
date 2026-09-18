claude-opus-5[1m]

**Verdict:** **NOT REPRODUCED.** On US local government finances, 3,126 counties across the 2007,
2012, 2017 and 2022 Censuses of Governments, **no arm shows local spending shifting from education
toward law and order as the immigrant share rises**, and **no arm shows total local spending
falling**. The paper's own strongest share result, the police share, comes out *negative* over
2007-2022 in both weightings: −0.463 (0.264) population-weighted and −0.435 (0.162) unweighted per
10 points of Hispanic share, against the +0.23 pp the paper reports at its own mean dose; the 95%
intervals at each sample's own mean treatment exclude that figure. Total direct general expenditure
per resident is flat in three of four arms and *up* in the fourth. **The opposite-signed shift is
itself not identified and is reported as a null, not a reversal:** over 2007-2022 the pre-period
placebo (−0.151, se 0.059) is as large as the estimate (−0.154, se 0.063), and over 2012-2022 the
estimate is a California artifact that halves to −0.093 (0.072) when that one state is dropped.
Separately, the sentence Tabarrok quoted is carried by the paper's log-level columns: in its own
*share* specification the education coefficient is +0.23 (se 0.61), an insignificant positive, and
the May 2025 revision drops the share columns while keeping the sentence in the abstract.
This lane is descriptive and has no instrument, so it cannot refute their causal estimate — see
"What this does and does not say about the paper".

# Local spending composition lane — does local spending shift from education to law-and-order where the Hispanic/foreign-born share rises?

All three phases are closed. Every number below carries its provenance tag; the re-run reproducibility check is at the end.

## Phase 1 — the paper Tabarrok endorsed

**Paper.** Ernesto Tiburcio and Kara Ross Camarena, *The Local Reaction to Unauthorized Mexican
Migration to the US*. Tufts job-market paper, November 2023 version; current version May 2025
(Tiburcio now at UC Berkeley Goldman School). Co-winner, MPSA Best Paper in Political Behavior
(2023 conference).
[SOURCE: https://marginalrevolution.com/marginalrevolution/2023/12/immigration-backlash.html,
archived 2024-03-27, `mr_archive_2026_09_18/derived/mr_posts.jsonl`]
[SOURCE: 2023 PDF via Wayback 20231203002131 of
`ernestotiburcio.files.wordpress.com/2023/11/the-local-reaction-to-unauthorized-mexican-migration-to-the-us.pdf`,
cached `_cache/tiburcio_camarena_2023.pdf`; 2025 PDF
`https://scholar.karaross.com/working-papers/localreactions-current.pdf`, cached `_cache/tc_current_2025.pdf`]
The 2023 wordpress URL Tabarrok linked is now a 404 at origin; only the Wayback copy survives.

**Design.**

- *Treatment.* A confidential Mexican Ministry of Foreign Affairs (SRE) file of 14m consular ID
  ("matrícula consular de alta seguridad") records covering 7.4m individuals, 2002–2020. New cards
  identify newcomers; the count of new IDs in a US county over a 4-year period (2007–10, 2011–14,
  2015–18), divided by *predicted* county population, is "Newcomers, pct. pop." Mean 0.55, sd 0.68.
  Cards issued in another county of the same CBSA in the same period are dropped as address changes.
- *Instruments.* Two shift-share designs sharing 2002–06 Mexican-municipality-to-US-county shares
  (2,449 municipalities). Shifter 1 is leave-one-CBSA-out national inflows from municipality m
  (Tabellini 2020 style); shifter 2 is a LASSO-selected Poisson prediction of municipality outflow
  from Mexican push factors (climate, mortality, poverty, firms, production). Both scaled by
  predicted population (2006 population grown at the rate of similar-urbanicity counties elsewhere).
- *Specification.* County and state-by-period fixed effects, no parametric covariates
  (citing Blandhol et al. 2022). Weighted by predicted population. SEs clustered at CBSA.
- *Fiscal outcomes.* Census **Annual Survey of State and Local Government Finances**, aggregating
  *all* local units inside a county — county government, cities, townships, special districts and
  school districts — by function. Years **2012 and 2017 only**, because the survey enumerates all
  local units only in years ending in 2 and 7. 5,338 county-period observations. Outcomes are
  log 2010 dollars per person (education per child under 19) and shares of total direct expenditure.

**Results the endorsement rests on** [SOURCE: 2023 version Table 4, p. 25; 2025 version Table 3, p. 22]

| outcome | 2SLS LOO | 2SLS push | mean of dep. var. |
|---|---|---|---|
| revenue, log pc | −0.03** (0.01) | −0.03** (0.01) | — |
| direct expenditure, log pc | −0.04*** (0.02) | −0.04** (0.02) | — |
| education, log per child | −0.05*** (0.02) | −0.03** (0.01) | — |
| police, log pc | +0.04** (0.02) | +0.04* (0.02) | — |
| judicial, log pc | +0.15** (0.07) | +0.11 (0.07) | — |
| **education share of direct expenditure** | **+0.23 (0.61) ns** | +0.92 (0.56) ns | 40.93% |
| **police share** | **+0.42*** (0.14)** | +0.38** (0.16) | 5.45% |
| **judicial share** | **+0.26*** (0.10)** | +0.21** (0.10) | 1.41% |

Coefficients are per 1 percentage point of newcomers; at the mean flow (0.55) that is +0.23 pp
police share and +0.15 pp judicial share, the numbers Tabarrok quoted.

**Two design facts the quoted summary does not carry.**

1. In the share specification the education coefficient is **positive and insignificant**
   (+0.23, se 0.61). The "shift away from education" is identified off the *log level* columns, not
   off education's share of the budget. The share result is a rise in the law-and-order share
   (police + judicial together about 6.9% of direct expenditure at the mean), with the offset spread
   across the remaining categories rather than located in education. [SOURCE: 2023 Table 4]
2. The **2025 version drops the share columns entirely**. Table 3 there has four columns
   (revenue, total, education, law-and-order), all in logs; the share footnote survives but the
   columns do not. The abstract still says "reallocation away from education toward support for law
   and order." [SOURCE: `_cache/tc_current_2025.txt` Table 3] Magnitudes are restated per 0.1 pp
   (interquartile) rather than per mean flow, so the headline "2% / 3%" of the 2023 abstract becomes
   "0.4% / 0.5%" per 0.1 pp — the same slope, a smaller quoted dose.

**What this lane can and cannot reproduce.** The consular-ID treatment is confidential and cannot be
rebuilt. The design here is therefore *descriptive and different*: within state-year, county long
differences in observed Hispanic and foreign-born *share* on the same Census local-finance
composition outcomes. It tests whether the composition pattern is visible in the observable
correlate of the treatment, over a longer window (2007–2022) than the paper's two cross-sections.
Per BRIEF and ladder 136, the post-2008 shift-share instrument is not used. Every estimate below is
descriptive.

## Phase 2 — data acquisition

**Local government finances.** Census individual-unit files, which carry every local unit's
finances by item code. They exist on census.gov for **2012 and 2017** (under
`gov-finances/datasets/<year>/public-use-datasets/`) and for **2018 through 2023** (under
`gov-finances/tables/<year>/`). There is **no individual-unit file for 2007** and none for
2013-2016; the 2007 directory holds only the state-by-type summary. The 2007 Census of
Governments county-area file is likewise absent. [SOURCE: directory listings of
`www2.census.gov/programs-surveys/gov-finances/{datasets,tables}/` and `www2.census.gov/govs/{estimate,local,cog,gid}/`,
probed 2026-09-18]

Two fixed-width layouts, both taken from the shipped technical documentation, not from memory:

| | 2012 and earlier | 2017 and later |
|---|---|---|
| ID | 1-14, Census state and county codes | 1-12, **FIPS** state in 1-2, FIPS county in 4-6 |
| Item code | 15-17 | 13-15 |
| Amount, thousands of dollars | 18-29 | 16-27 |
| Year | 30-33 | 28-31 |
| County FIPS | from `Fin_GID_2012.txt` positions 114-118 | from the ID itself |

[SOURCE: `2012 S&L Indiv Unit Data File Tech Doc.pdf` pp. 1-2; `2017 S&L Public Use Files
Technical Documentation.pdf` pp. 1-3]

Direct general expenditure is built from prefixes E (current operation), F (construction),
G (other capital outlay) and J (assistance and subsidies), plus I89 (interest on general debt),
excluding functions 90-94 (liquor stores and the four utilities) and the intergovernmental
prefixes L, M, Q and S. [SOURCE: item-code list, 2012 tech doc pp. 4-12]

**Validation.** Summing the county panel back to the nation reproduces the Census's own
`12statetypepu.txt` local-government aggregate **exactly**, function by function [CALCULATION]:

| | county panel | `12statetypepu.txt`, level 3, states only |
|---|---|---|
| total direct general expenditure | $1,422.9bn | $1,422.9bn |
| education | $597.3bn | $597.3bn |
| police | $84.0bn | $84.0bn |
| corrections | $26.7bn | $26.7bn |
| judicial | $21.6bn | $21.6bn |

Only 21 of 1.74m records in 2012 and 14 in 2017 lack a usable county code.

**County shares.** ACS 5-year via the Census API for 2009, 2012, 2017 and 2022 (`B03003` Hispanic,
`B05002` nativity, `B05006` place of birth, `B01001` age, `B19013` median household income), and the
2000 Census (`sf1` `P008` Hispanic, `sf3` `P021` nativity) for the pre-period. The Mexico cell of
`B05006` moves between years — `B05006_138E` in 2009, `_137E` in 2012, `_139E` in 2017, `_160E` in
2022 — so it is resolved from each year's group metadata by label rather than hard-coded.
[SOURCE: `api.census.gov/data/<year>/acs/acs5/groups/B05006.json`]

**Downloads.** Everything Census is 5-10 MB; no Modal needed there. The Willamette Government
Finance Database (341 MB, Google Drive) downloads to this machine at about **35 kB/s**, over three
hours; a Modal container pulled it in **8 seconds at 39 MB/s**, and the 2.9 GB CSV inside it is
filtered and aggregated in the container so only a small county file crosses the wire.

**Waves used.** 2012, 2017 and 2022 only. The annual-survey individual-unit files enumerate a
sample of local units rather than all of them, so county sums for 2018-2021 are not comparable in
composition; Tiburcio and Camarena restrict to census years for the same reason. Those years are
still written to `derived/county_finance.csv`.

**Connecticut drops out.** The 2022 finance file codes Connecticut as the nine planning regions
(FIPS 09110-09190) while ACS 2022 still uses the eight counties (09001-09015). No Connecticut county
survives the balanced-panel filter, so the state is absent rather than mismatched. [CALCULATION]

Panel: **3,126 counties** observed in all three waves.

The 2007 wave comes from the Willamette Government Finance Database rather than census.gov, which
has no 2007 individual-unit file. Its 2012, 2017 and 2022 waves were checked against the Census
build county by county before its 2007 wave was used [CALCULATION]:

| year | total direct | education | police | corrections | judicial | correlation |
|---|---|---|---|---|---|---|
| 2012 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.00000 |
| 2017 | 1.0010 | 1.0006 | 1.0002 | 1.0011 | 0.9988 | 0.99992+ |
| 2022 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.00000 |

(ratio of the database's national sum to the Census build's, across 3,137-3,139 matched counties).
The 2007 finance wave is paired with the 2005-2009 ACS, whose midpoint is 2007.

Panel: **3,126 counties** in all of 2012, 2017 and 2022; **3,124** of them also have 2007.

## Phase 3 — estimates

Design: Δy_c = α_s + β Δx_c + ε_c, with a state fixed effect on the differenced equation (the
long-difference analogue of the paper's state-by-period effects) and standard errors clustered on
state. Coefficients are **per 10 percentage points** of share change. Weights are base-year
population; the paper also weights. **Descriptive throughout — no instrument** (ladder 136).
206 estimates across 38 arms in `derived/estimates_composition.csv`.

### The claim in one number: log(law-and-order spending / education spending)

Law and order is police plus corrections plus judicial, as in the paper.

| arm | 2007-2022 | 2012-2022 |
|---|---|---|
| Hispanic share, weighted | **−0.154 (0.063)\*\*** | **−0.227 (0.113)\*\*** |
| Hispanic share, unweighted | −0.087 (0.057) | **+0.004 (0.069)** |
| Hispanic share, weighted, with covariates | — | −0.173 (0.083)\*\* |
| Foreign-born share, weighted | −0.209 (0.082)\*\* | −0.189 (0.065)\*\*\* |
| **California dropped**, weighted | −0.096 (0.058)\* | **−0.093 (0.072)** |
| **pre-period placebo** (2000-2009 share change) | **−0.151 (0.059)\*\*** | −0.119 (0.115) |

**Every arm that moves, moves the wrong way for the claim.** Where the immigrant share rose, local
budgets tilted *toward* education and *away* from law and order. Not one arm, at any weighting,
window or regressor, shows a shift toward law and order.

**But the opposite-signed finding does not survive its own checks either**, and this is the more
important result:

- Over **2007-2022** the pre-period placebo is **as large as the estimate itself** (−0.151 versus
  −0.154). Counties whose Hispanic share was already rising in 2000-2009 show the same later
  composition change, so the contemporaneous share change identifies nothing here. The 2000-2009
  placebo window overlaps the first two years of the outcome window, which if anything understates
  the problem.
- Over **2012-2022** the placebo is clean (−0.119, se 0.115) but the result is a **California
  artifact**. Leaving each state out in turn, the coefficient runs from −0.279 (dropping Texas) to
  −0.093 (dropping California), median −0.228; California is the only state whose removal changes
  the verdict. [CALCULATION: `derived/loo_state_logratio.csv`] California's Local Control Funding
  Formula, in force from 2013-14, routes state money to districts by English-learner and low-income
  counts, raising the education share where the Hispanic share is high for a reason that has nothing
  to do with local preferences. On the 2007-2022 window California is again the extreme
  (leave-one-out range −0.183 to −0.096, median −0.154).

**The defensible statement is the null:** no shift toward law and order is detectable, and the
unweighted 2012-2022 estimate is a precise zero at ±0.07 log points per 10 points.

### Shares of total direct general expenditure, Hispanic share

| outcome | mean share, base year | 2007-2022 weighted | 2007-2022 unweighted | 2012-2022 weighted |
|---|---|---|---|---|
| education | 45.3% / 44.5% | +4.164 (1.229)\*\*\* | +2.250 (0.576)\*\*\* | +6.709 (2.058)\*\*\* |
| police | 5.50% / 5.95% | **−0.463 (0.264)\*** | **−0.435 (0.162)\*\*\*** | −0.295 (0.319) |
| corrections | — | +0.101 (0.262) | +0.687 (0.398)\* | +0.054 (0.192) |
| judicial | — | −0.201 (0.078)\*\* | −0.003 (0.093) | −0.343 (0.301) |
| **law and order** | **8.81% / 9.42%** | **−0.562 (0.417)** | +0.248 (0.465) | −0.584 (0.647) |
| welfare | — | −0.162 (0.366) | −0.199 (0.112)\* | −0.532 (0.479) |
| health and hospitals | — | −1.404 (1.088) | −2.025 (0.641)\*\*\* | −1.344 (1.283) |
| highways | — | +0.265 (0.237) | +0.362 (0.274) | +1.034 (0.395)\*\*\* |

The police share, the paper's own strongest share result, is **negative in both weightings** over
the long window. Dropping California takes the 2007-2022 police share to −0.245 (0.280) and law and
order to −0.305 (0.497): zero, not positive. Dropping the 25 largest counties, or trimming counties
under 10,000 residents and the 1% tails of both variables, leaves the 2012-2022 pattern unchanged.
No single county drives the education share: removing Los Angeles County moves it from +6.71 to
+6.05 per 10 points, and the biggest single-county swing among the 40 largest is San Bernardino, to
+7.99. [CALCULATION: `derived/influence_education_share.csv`]

### The denominator-masking check: real per-capita levels

A composition result can be an artifact of its denominator. It is not here, and the levels
contradict the spending-cut half of the claim on their own. Log real dollars per resident, 2022
prices, per 10 points of Hispanic share:

| outcome | 2007-2022 wtd | 2007-2022 unwtd | 2012-2022 wtd | 2012-2022 unwtd |
|---|---|---|---|---|
| **total direct general expenditure** | **−0.022 (0.018)** | **+0.013 (0.027)** | **−0.002 (0.023)** | **+0.139 (0.052)\*\*\*** |
| education | +0.065 (0.038)\* | +0.039 (0.017)\*\* | +0.155 (0.064)\*\* | +0.069 (0.017)\*\*\* |
| police | −0.087 (0.031)\*\*\* | −0.108 (0.047)\*\* | −0.041 (0.042) | +0.071 (0.069) |
| corrections | +0.142 (0.170) | −0.059 (0.083) | +0.083 (0.137) | −0.137 (0.081)\* |
| judicial | −0.177 (0.089)\*\* | +0.036 (0.063) | −0.288 (0.212) | +0.310 (0.081)\*\*\* |
| law and order | −0.089 (0.044)\*\* | −0.048 (0.062) | −0.073 (0.068) | +0.140 (0.064)\*\* |
| welfare | −0.056 (0.086) | −0.122 (0.123) | −0.005 (0.219) | −0.089 (0.152) |
| health and hospitals | −0.450 (0.197)\*\* | −0.500 (0.106)\*\*\* | −0.346 (0.246) | −0.484 (0.177)\*\*\* |
| highways | +0.018 (0.055) | +0.103 (0.045)\*\* | +0.161 (0.081)\*\* | +0.319 (0.059)\*\*\* |

Total local spending per resident is **flat in three of four arms and up in the fourth**. Education
per capita rises in all four. Police per capita is negative over the long window in both weightings.
Education per child under 19 is −$579 (2,542) per 10 points over 2012-2022, an uninformative zero.

### Disconfirmation arms the brief required, and what they did

1. **Dropping the largest metros.** Removing the 25 largest counties leaves every 2012-2022 share
   coefficient within one standard error of the full-sample value; law and order goes from
   −0.584 (0.647) to +0.243 (0.591), still zero. **Did not reverse the headline.**
2. **Per-capita levels instead of shares.** Above. **Did not reverse it; strengthened the level
   half.**
3. **Pre-period placebo.** **Reversed the interpretation of the long window.** On 2007-2022 the
   placebo matches the estimate almost exactly on the ratio (−0.151 versus −0.154) and exceeds it on
   the police share (−1.094, se 0.272, versus −0.463). On 2012-2022 the placebo is clean on the
   ratio but still significant on the police share (−0.777, se 0.321) and the highway share
   (+1.010, se 0.361). Wherever the pre-period change predicts the later outcome, the
   contemporaneous coefficient is a correlate of a long-running county trajectory and nothing more.
4. **Dropping California** (not requested; added because the funding formula is a live confounder).
   **Halved the 2012-2022 ratio estimate and removed its significance.**

### Sub-windows and alternative regressors

2007-2012 gives −0.018 (0.075) on the ratio, 2012-2017 gives an education share of
+5.561 (2.314)\*\* with law and order at +0.054 (0.864), and 2017-2022 gives education
+5.143 (2.011)\*\* with law and order −1.150 (0.496)\*\*. The Mexico-born share gives education
+7.337 (2.133)\*\*\* and law and order +0.689 (1.820). Elementary and secondary education alone
behaves like total education (+6.576 (1.942)\*\*\* weighted, +0.463 (1.010) unweighted).

### What this does and does not say about the paper

**Dose, compared at each study's own mean.** The two treatments are different quantities, so the
comparison is made at the mean of each. Tiburcio and Camarena's mean four-year inflow of new
consular-ID holders is 0.55% of county population, and at that dose their police share rises
**+0.23 pp** and their judicial share +0.15 pp. This lane's weighted mean Hispanic-share change is
3.23 points over 2007-2022 and 2.08 points over 2012-2022; at those doses the police share moves
**−0.150 pp, 95% interval [−0.317, +0.018]** and **−0.061 pp, [−0.191, +0.069]**. Both intervals
exclude +0.23. [CALCULATION] That is a real inconsistency at each study's own mean treatment, not an
artifact of mapping one dose onto the other.

**What this cannot do.** The consular-ID file is confidential, so their treatment cannot be rebuilt,
and this lane has no instrument — the placebo failures show exactly why that matters. A resident
share is a stock that nets out-migration, naturalisation and internal moves; their newcomer count is
a gross flow of recent unauthorized arrivals. If the fiscal response is specific to that flow and is
offset in the stock by everything else moving, both sets of results can hold at once. This is a
failure to see the pattern in the observable correlate, not a refutation of their estimate.

**A gap in the endorsement itself.** The sentence Tabarrok quoted — "shift it away from education
towards law-and-order" — is carried by the paper's *log level* columns. In its own **share**
specification the education coefficient is **+0.23 with a standard error of 0.61**, an insignificant
positive: education's share of the budget does not fall even in the paper. The May 2025 revision
drops the share columns from the table while keeping the sentence in the abstract.
[SOURCE: 2023 version Table 4 p. 25; 2025 version Table 3 p. 22]

## Draft memo section

> ### Local spending does not shift from education to law and order as the immigrant share rises
>
> Tiburcio and Camarena (2023, revised May 2025) report that a mean four-year inflow of unauthorized
> Mexican migrants, identified from Mexican consular ID records and instrumented with two
> shift-share designs, cuts county-area local direct spending about 2% per person, cuts education
> spending per child about 3%, and raises the police and judicial shares of the local budget by 0.23
> and 0.15 percentage points. Alex Tabarrok endorsed the result on 2023-12-02 as evidence that
> unauthorized inflows "reduce local public spending, and shift it away from education towards
> law-and-order."
> [SOURCE: marginalrevolution.com/marginalrevolution/2023/12/immigration-backlash.html]
>
> Their treatment is confidential, so we tested the pattern on its observable correlate: the same
> Census local-finance data, aggregated the same way — every local unit inside a county, including
> the county government, municipalities, townships, special districts and school districts — against
> the change in the county's Hispanic and foreign-born share, over 2007-2022 and 2012-2022. The
> panel is 3,126 counties across the 2012, 2017 and 2022 Censuses of Governments, 3,124 of them also
> observed in 2007. The county sums reproduce the Census's own national local-government totals
> exactly, function by function. Estimates are within-state long differences, descriptive, with no
> instrument.
>
> **No arm shows a shift toward law and order.** Taking the claim as one number, the log of
> law-and-order spending over education spending, a 10-point rise in the county Hispanic share moves
> it by −0.154 (0.063) over 2007-2022 and −0.227 (0.113) over 2012-2022 — negative, that is, *toward*
> education, the opposite of the claim. The police share, the paper's strongest share result, is
> −0.463 (0.264) population-weighted and −0.435 (0.162) unweighted over the long window. At this
> sample's own mean Hispanic-share change of 3.23 points, the implied police-share move is −0.150
> percentage points with a 95% interval of [−0.317, +0.018], which excludes the +0.23 the paper
> reports at its own mean dose.
>
> **Nor does total local spending fall.** In log real dollars per resident, a 10-point rise in the
> Hispanic share moves total direct general expenditure by −0.022 (0.018) and −0.002 (0.023)
> weighted over the two windows, and +0.013 (0.027) and +0.139 (0.052) unweighted: flat in three
> arms and up in the fourth. Education per capita rises in all four.
>
> **The opposite-signed finding is not itself identified, and we report it as a null rather than a
> reversal.** Over 2007-2022 the pre-period placebo — the 2000-2009 Hispanic-share change run against
> the 2007-2022 outcome change — gives −0.151 (0.059), almost exactly the contemporaneous estimate
> of −0.154. Counties whose Hispanic share was already rising before the outcome window show the same
> later composition change, so the contemporaneous change identifies nothing there. Over 2012-2022
> the placebo is clean but the estimate is a California artifact: dropping California alone takes it
> to −0.093 (0.072), and California is the only state whose removal changes the verdict. California's
> Local Control Funding Formula, in force from 2013-14, routes state money to districts by
> English-learner and low-income counts, mechanically raising the education share where the Hispanic
> share is high. What survives every check is the absence of the claimed direction, not the presence
> of its opposite.
>
> **A resident share is not their treatment.** It is a stock that nets out-migration, naturalisation
> and internal moves, while their newcomer count is a gross flow of recent unauthorized arrivals.
> Both results can hold if the fiscal response is specific to that flow. This is a failure to find
> the pattern in the observable correlate, not a refutation of their estimate.
>
> **One feature of the endorsement is worth recording separately.** The quoted sentence is carried by
> the paper's log-level columns. In its own *share* specification the education coefficient is +0.23
> with a standard error of 0.61 — an insignificant positive — so education's share of the local
> budget does not fall even in the paper; what rises is the police and judicial share, with the
> offset spread across the remaining categories. The May 2025 revision drops the share columns from
> the table while keeping the sentence in the abstract.
> [SOURCE: 2023 version Table 4 p. 25; 2025 version Table 3 p. 22]

## Reproducibility

`build_county_panel.py`, `pull_acs_counties.py` and `estimate_composition.py` were re-run from
scratch against the cached inputs after the outputs were snapshotted. **All seven files in
`derived/` came back byte-identical** (`cmp` against the snapshot, exit 0 on each):

```
IDENTICAL  composition_means.csv
IDENTICAL  county_finance.csv
IDENTICAL  county_shares.csv
IDENTICAL  estimates_composition.csv
IDENTICAL  influence_education_share.csv
IDENTICAL  loo_state_logratio_2007_2022.csv
IDENTICAL  loo_state_logratio.csv
```

`fetch_census_finance.py` and the two Modal scripts are network fetches and are idempotent by
skip-if-present rather than by byte comparison.

## Covered / skipped

**Covered.** Phase 1 in full, from the archived Marginal Revolution post through both versions of
the paper, with the design and every fiscal coefficient read off the tables rather than recalled.
Phase 2 in full for 2007 and 2012-2023, including the two fixed-width layout changes taken from the
shipped documentation, an exact validation of the county sums against the Census's own aggregate,
and a county-by-county cross-check of the 2007 source against the Census build on the three
overlapping waves. Phase 3 with every arm the brief lists — shares and per-capita real levels,
Hispanic, foreign-born and Mexico-born regressors, weighted and unweighted, with and without the
school-lane covariates, 2007-2022 and 2012-2022 plus three sub-windows, dropping the largest metros,
and the pre-period placebo — plus five the brief did not ask for: the log law-and-order-to-education
ratio, leave-one-state-out on both windows, leave-one-county-out influence, a drop-California arm,
and a trimmed arm.

**Skipped or incomplete.**
- **Annual survey years.** 2013-2016 have no individual-unit file at all. 2018-2021 and 2023 do but
  enumerate only a sample of local units, so their county sums are not comparable in composition;
  they are written to `derived/county_finance.csv` and excluded from estimation, as the paper also
  restricts to census years.
- **Connecticut.** Absent from 2017 onward: the 2022 finance file codes it as nine planning regions
  (FIPS 09110-09190) while ACS 2022 still uses eight counties (09001-09015), so no Connecticut
  county survives the balanced-panel filter.
- **Mexico-born before 2009.** The 2000 Census place-of-birth detail was not pulled, so the
  Mexico-born regressor runs on 2012-2022 only and has no placebo.
- **Not attempted.** The paper's political and values outcomes — Republican vote share,
  DW-NOMINATE, moral universalism — are outside this lane, as is any attempt to rebuild the
  consular-ID treatment or an instrument for it.

Not committed, per the brief. Nothing under `research/` was touched.
