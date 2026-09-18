claude-opus-5[1m]

# Homicide: the victim–offender joint distribution, and what one homicide costs the treasury

Model self-report: claude-opus-5[1m] (Opus 5, 1M context). Lane
`infra/immigration-fiscal/homicide_cost_2026_09_18/`. September 18, 2026.

**Verdict:** One cleared homicide costs the treasury about **$1.5–1.8 million** in the
repo's period-profile frame, and the number is **dominated by prison, not by the victim**.
On the central arm (partial account, undiscounted, 23.1% of murder sentences life or death)
the total is **$1.55m** where the offender is Hispanic, **$1.61m** where non-Hispanic white,
**$1.81m** where non-Hispanic Black. Corrections plus the offender's own foregone fiscal
profile is **91–97%** of every one of those figures; the victim's foregone lifetime balance
is between **−$56k and +$75k** and the minor-children channel about **$0.1m**. Against the
$13.1m social cost of a murder the repo already carries, the treasury share is **11.8% to
13.8%**. The ordering by offender ethnicity is **the reverse of the intuition the lane was
built to test**: the Hispanic-offender cell is the *cheapest* to the treasury, because the
victims Hispanic offenders produce are overwhelmingly Hispanic, and a Hispanic victim's
remaining lifetime balance in this frame is **negative**. [FRAMING-SENSITIVE]

That last sentence is the whole memo's health warning and it is stated plainly below: a
frame in which killing a low-earning or elderly person scores as a treasury gain is a
**property of the average-cost accounting convention, not a valuation of the life**. Every
fiscal line in this memo carries the Department of Transportation's 2024 value of a
statistical life, **$13.7m** [SOURCE: transportation.gov VSL guidance, fetched 2026-09-18],
beside it. On that measure every homicide costs about the same, roughly a hundred times the
treasury line, and none of the ethnic ordering below survives.

On the distribution side the headline is a **disconfirmation hit**. The widely quoted
intra-group share — 72% of Hispanic offenders' victims are Hispanic, 81% of white
offenders' victims are white — is computed on the 61% of cleared cases where ethnicity is
reported on both sides, and that subsample is not representative. Imputing the missing
ethnicities moves the Hispanic intra-group share to **0.55–0.67** depending on how the
imputation is done, while the white figure barely moves (0.74–0.81). The pairing structure
is much less firmly identified for Hispanic offenders than the raw table suggests.

---

## 1. Data, with missingness and scaling

| Source | What | Coverage | Fetched |
|---|---|---|---|
| FBI Supplementary Homicide Reports, compiled by the Murder Accountability Project | `SHR76_25a.csv`, 352,107,592 bytes, sha256 `eeedbf5e…b88a12`, 929,433 victim records 1976–2025, 905,648 of them murder or non-negligent manslaughter | agency-reported, voluntary | 2026-09-18 |
| CDC WONDER, Underlying Cause of Death 2018–2024 Single Race (D158) | NCHS 113-cause category "Assault (homicide)" GR113-127 (`*U01-*U02, X85-Y09`) | complete death registration | 2026-09-18 |
| Census ACS 2023 1-year PUMS (API, `tabulate`) | Hispanic origin × group-quarters type | full sample | 2026-09-18 |
| CPS ASEC 2025 (`asecpub25csv.zip`, repo copy) | adults' own minor children in household | household population only | held |
| BJS NCJ 250747, *Race and Hispanic Origin of Victims and Offenders, 2012–15* | non-lethal violence, context only | NCVS | 2026-09-18 |
| FBI Crime Data Explorer NIBRS victim/offender tables | **not obtained** | — | — |

[SOURCE: https://www.murderdata.org/p/data-docs.html → Dropbox `SHR76_25a.csv`]
[SOURCE: https://wonder.cdc.gov/controller/datarequest/D158]
[SOURCE: https://bjs.ojp.gov/content/pub/pdf/rhovo1215.pdf]

**The CDE is closed without a key.** `api.usa.gov/crime/fbi/cde/...` returns
`API_KEY_MISSING`; the bulk-download S3 bucket the web app used to serve from returns
`NoSuchBucket` and the signed-URL endpoint returns an empty object. Per the brief this lane
stops on that source. NIBRS would have added the offender's age and relationship for
non-fatal offences and a second, incident-based read on ethnicity; neither enters the cost
model, so nothing below depends on it.

**Homicide definition.** The NCHS 113-cause category reproduces the published homicide
series exactly (2021 = 26,031 deaths, the figure in *Deaths: Final Data for 2021*). The raw
ICD-10 range `X85-Y09` alone runs **1.0–1.4% lower** every year (2021 = 25,761). The lane
uses the 113-cause list as the denominator and keeps `X85-Y09` as a cross-check; both series
are in `derived/`. Terrorism codes `*U01-*U02` contribute **20 deaths in 2019 and zero or
suppressed in every other year 2018–2024** — a rounding error [SOURCE: WONDER D158].

**Missingness is the central data problem and it is on the SHR side only.** Death
certificates report Hispanic origin for 99.8% of homicide deaths (254 "Not Stated" out of
117,427 in 2019–2023). The SHR does far worse, though it has improved sharply since 2016:

| Year | SHR victim records | victim ethnicity unknown | offender ethnicity unknown (cleared) | cleared |
|---|---|---|---|---|
| 2015 | 16,165 | 54.5% | 56.9% | 66.9% |
| 2017 | 18,079 | 29.1% | 41.5% | 67.0% |
| 2019 | 16,007 | 26.8% | 38.6% | 68.3% |
| 2021 | 21,959 | 25.0% | 36.2% | 64.0% |
| 2023 | 18,533 | 25.5% | 33.4% | 71.4% |

Victim *race* is missing for only 1.6–3.0%; it is the Hispanic-origin field that agencies
skip. The step change between 2016 and 2017 is a reporting change, not a change in
homicide, and it is the reason this memo leads with the 2019–2023 window.

**SHR-to-WONDER scaling.** SHR criminal-homicide victim records 2019–2023 total **93,929**
against **117,427** homicide deaths in WONDER: a coverage ratio of **0.800**. The shortfall
is agencies that do not report (Florida is the largest single gap), and it is not uniform.
Among SHR cleared single-victim/single-offender cases with ethnicity known, the victim
composition is **28.2% non-Hispanic white, 45.5% non-Hispanic Black, 18.9% Hispanic**; the
WONDER victim composition for the same years is **23.2% / 54.2% / 17.1%**. The SHR analysis
sample therefore **over-represents white victims by about a fifth and under-represents Black
victims by about a sixth**, mixing two selections — which agencies report, and which cases
clear. Every cost figure in section 3 is computed on SHR cells reweighted so the victim
ethnicity × 5-year age × sex marginal matches WONDER; 98.1% of the raw cell weight survives
the reweighting. `derived/shr_to_wonder_scaling.csv` carries the 128 cell factors.

**Mexican origin is not separable in the SHR, or in any US homicide record.** The SHR
carries Hispanic origin as a yes/no field and nothing else. The only bridge available is the
ACS, and it is an imputation, not a measurement:

| ACS 2023 1-year PUMS | Hispanic total | Mexican-origin | Mexican share | generic "All Other Spanish/Hispanic/Latino" |
|---|---|---|---|---|
| Ages 18–34, housing units | 16,718,080 | 10,129,387 | **60.6%** | 4.1% |
| Ages 18–34, institutional group quarters | 180,715 | 95,744 | **53.0%** | 25.7% |
| Ages 18–64, institutional group quarters | 400,510 | 210,956 | 52.7% | 26.7% |

The institutional cell is the repo's standing prisoner proxy. The generic-Hispanic coding
problem the ledger already documents is visible here: a quarter of institutionalised
Hispanics are coded to the residual origin category against 4% in housing units. If the
excess residual is Mexican-origin in the same proportion as the rest, the Mexican share of
Hispanic prisoners is bounded above at about **74.6%**. **[INFERENCE]** The honest statement
is a band of **53% to 75%**, and nothing in this memo should be read as a Mexican-origin
figure.

---

## 2. Distributions

### 2.1 Victim × offender ethnicity

Universe A is cleared single-victim/single-offender criminal homicides; universe B is every
victim with a known offender, using the first offender's record. Justifiable homicides
(felon killed by police, felon killed by a private citizen: 3,892 records 2019–2023) are
excluded from both and tabulated separately in `derived/shr_justifiable_2019_2023.csv`.

**Universe A, 2019–2023, counts.** Rows are victim ethnicity, columns offender ethnicity.

| victim ↓ / offender → | Hispanic | NH white | NH Black | NH other | unknown |
|---|---|---|---|---|---|
| Hispanic | 3,501 | 540 | 854 | 58 | 920 |
| NH white | 763 | 5,385 | 1,499 | 125 | 2,237 |
| NH Black | 538 | 615 | 10,875 | 72 | 2,496 |
| NH other | 79 | 117 | 153 | 501 | 147 |
| unknown | 459 | 668 | 1,031 | 62 | 8,518 |

Ethnicity is known on both sides in **25,675 of 42,213** cases (60.8%). Universe B gives
37,449 of 62,326 (60.1%) and an almost identical matrix.

**Victim distribution of each offender group, ethnicity known on both sides** (rows sum to 1):

| offender | Hispanic victim | NH white victim | NH Black victim | NH other victim |
|---|---|---|---|---|
| Hispanic | **0.717** | 0.156 | 0.110 | 0.016 |
| NH white | 0.081 | **0.809** | 0.092 | 0.018 |
| NH Black | 0.064 | 0.112 | **0.813** | 0.011 |
| NH other | 0.077 | 0.165 | 0.095 | **0.663** |

Pooling 2015–2023 changes no cell by more than 0.01. Universe B changes no cell by more than
0.015. **These numbers are not robust to the missing 39%** — see section 4.

For context, and it is only context: in the NCVS for 2012–15, half (51%) of all violent
victimizations were intra-group; white victims' offenders were white in 57% of cases and
Black victims' offenders Black in 63% [SOURCE: BJS NCJ 250747, Highlights]. The rate of
violence against a Hispanic victim by a Hispanic offender was 8.3 per 1,000 Hispanic
persons, against 4.1 by a white offender and 4.2 by a Black offender — an intra-group share
near 50%, well below the homicide figure. Lethal violence is more intra-group than
non-lethal violence, or the victim's perception of the offender's ethnicity in the NCVS
differs systematically from the police record. This lane cannot separate those.

### 2.2 Clearance, which conditions everything about offenders

| victim ethnicity | criminal-homicide victims 2019–2023 | cleared | **unsolved share** |
|---|---|---|---|
| NH white | 16,622 | 13,977 | **0.159** |
| NH other | 1,901 | 1,430 | 0.248 |
| Hispanic | 14,252 | 9,069 | **0.364** |
| NH Black | 37,835 | 22,154 | **0.414** |
| unknown | 23,319 | 15,696 | 0.327 |

A homicide with a white victim is **two and a half times** as likely to be cleared as one
with a Black victim. Every offender distribution in this memo is conditional on clearance,
so it over-weights whatever kinds of homicide clear: domestic and acquaintance killings
clear, street and gang killings do not. This is the single largest identification problem in
section 2 and it cannot be fixed from the SHR.

### 2.3 Age

Victim age, share of that ethnicity's criminal-homicide victims, 2019–2023, all victims
including uncleared cases:

| band | Hispanic | NH white | NH Black |
|---|---|---|---|
| 0–14 | 0.039 | 0.047 | 0.036 |
| 15–24 | 0.296 | 0.136 | 0.307 |
| 25–34 | 0.284 | 0.197 | 0.319 |
| 35–44 | 0.201 | 0.200 | 0.176 |
| 45–54 | 0.100 | 0.150 | 0.085 |
| 55–64 | 0.047 | 0.137 | 0.051 |
| 65+ | 0.025 | 0.127 | 0.022 |

Offender age, cleared cases, share of that ethnicity's offenders:

| band | Hispanic | NH white | NH Black |
|---|---|---|---|
| 15–24 | 0.388 | 0.202 | 0.362 |
| 25–34 | 0.298 | 0.258 | 0.319 |
| 35–44 | 0.167 | 0.226 | 0.159 |
| 45–54 | 0.075 | 0.135 | 0.064 |
| 55+ | 0.034 | 0.170 | 0.043 |

Mean offender age on the raw single-year ages is **30.9 for Hispanic offenders and 40.2 for
non-Hispanic white offenders** in 2019–2023 (31.0 and 40.0 pooling 2015–2023), a nine-year
gap that drives a large part of the cost result in section 3, because a younger offender
serving a life sentence serves more prisoner-years. Section 4 takes that gap apart on the
ethnicity-imputed sample and 5-year band midpoints, where the same gap reads 32.9 against
39.4 before standardisation.

### 2.4 Relationship and circumstance

Relationship of victim to offender, universe A 2019–2023, ethnicity known on both sides:

| offender | acquaintance | family | intimate | stranger | unknown |
|---|---|---|---|---|---|
| Hispanic | 0.339 | 0.116 | 0.147 | **0.191** | 0.207 |
| NH white | 0.352 | **0.194** | **0.246** | 0.092 | 0.116 |
| NH Black | 0.344 | 0.088 | 0.118 | 0.151 | 0.299 |
| NH other | 0.313 | 0.189 | 0.218 | 0.112 | 0.167 |

The white-offender profile is domestic; the Hispanic-offender profile is not. White
offenders kill a family member or an intimate partner in **44%** of cleared cases against
**26%** for Hispanic offenders, and a stranger in 9% against 19%. Inside the
white-offender/white-victim cell the family-plus-intimate share reaches 49%.

Circumstance, universe A 2019–2023:

| offender | argument | felony | gang | other known | undetermined |
|---|---|---|---|---|---|
| Hispanic | 0.396 | 0.060 | **0.038** | 0.199 | 0.306 |
| NH white | 0.444 | 0.073 | **0.002** | 0.246 | 0.236 |
| NH Black | 0.378 | 0.068 | 0.018 | 0.170 | 0.366 |

Gang-coded homicides are 3.8% of cleared Hispanic-offender cases and 0.2% of white-offender
cases — a nineteen-fold ratio on a small base. The category is police-coded and known to be
applied unevenly across departments; treat the ratio as a real difference of unknown
magnitude. [UNVERIFIED]

---

## 3. What one homicide costs the treasury

### 3.1 The frame, stated before the numbers

The repo's all-age partial account gives a **period profile**: a per-person-year fiscal
balance for each age band of each group, measured on today's cross-section and applied as if
it were a lifetime (`pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv`,
83-year constructed lifetime). A person alive at age *a* carries a remaining stream
Σ *b(t)* for *t = a…82*. Killing them deletes that stream. **The treasury cost of the death
is that remaining balance**: positive where the person would have been a net contributor,
negative where they would have been a net beneficiary.

Three things follow and all three are uncomfortable.

1. **An elderly victim scores as a treasury gain** in this frame, by construction: the
   65–74 band carries −$14,024 per person-year for the white reference. That is the average-
   cost convention talking, not a judgment about the life.
2. **A Hispanic victim of any age scores as a gain on the partial account**, because the
   Mexican-origin period profile is negative in every band from age 0. The white profile is
   positive to about age 47.
3. **Under the complete account every victim of every group scores as a gain.** The complete
   account adds roughly −$6,900 to −$7,800 per person-year to every group
   (`gap_interest_2026_09_18/derived/audit.json`), which is enough to turn a white child's
   whole remaining life from +$360k to −$160k.

None of this is a statement about the value of a life. It is a statement about what an
average-cost fiscal ledger does when you delete a person from it. The VSL line runs beside
every number below for exactly this reason.

### 3.2 Victim channel: remaining lifetime balance, 2024 dollars

| age at death | white 3rd+ profile, partial, r=0 | at 3% | complete, r=0 | Mexican-origin profile, partial, r=0 | at 3% | complete, r=0 |
|---|---|---|---|---|---|---|
| 8 | +359,949 | +246,517 | −159,515 | −70,945 | +35,052 | −645,802 |
| 21 | +279,210 | +264,965 | −150,214 | −60,348 | +67,403 | −535,563 |
| 30 | +163,046 | +212,241 | −204,042 | −109,231 | +32,447 | −515,463 |
| 40 | +30,051 | +126,764 | −267,776 | −166,223 | −24,953 | −495,807 |
| 50 | −95,516 | +22,877 | −324,081 | −209,451 | −84,513 | −462,388 |
| 60 | −236,711 | −135,398 | −396,013 | −250,548 | −162,356 | −426,837 |
| 70 | −240,503 | −198,985 | −330,543 | −202,291 | −168,743 | −301,932 |
| 78 | −106,489 | −100,464 | −141,120 | −84,330 | −79,559 | −122,654 |

The Mexican-origin column is the population-weighted composite of the three nativity strata;
`derived/victim_remaining_balance.csv` carries each separately (Mexico-born, second
generation, third-plus self-identified) and the all-native reference. Discounting at 3%
**reverses the sign for young Hispanic victims** — the negative old-age years get discounted
away faster than the positive prime-age years — which is why both rates are carried
throughout.

**Selection is the weakness here and it is severe.** These are group *averages* by age.
Homicide victims are not average members of their age–ethnicity cell: they have far lower
labour-market attachment, higher rates of prior justice-system contact, and lower earnings
than the group mean. The group-average profile therefore **overstates** a homicide victim's
foregone contribution, and the overstatement is larger for young male victims. Nothing in
the CPS or the SHR lets this lane measure that gap. **[UNVERIFIED]** Every victim-channel
number should be read as an upper bound on the contribution actually lost.

### 3.3 Children of the victim

CPS ASEC 2025, own children under 18 in the household, linked through the basic-CPS parent
pointers `PEPAR1`/`PEPAR2`. 73.0m children under 18; 70.3% have two resident parents, 25.7%
one, 4.0% none.

| group | sex | band | share with a minor child | mean children | mean child-years to 18 | child-years where the victim is the only resident parent |
|---|---|---|---|---|---|---|
| white 3rd+ | male | 25–34 | 0.268 | 0.483 | 6.49 | 0.30 |
| white 3rd+ | male | 35–44 | 0.534 | 1.101 | 10.83 | 0.50 |
| white 3rd+ | female | 25–34 | 0.404 | 0.768 | 9.81 | 1.53 |
| white 3rd+ | female | 35–44 | 0.653 | 1.339 | 11.98 | 1.45 |
| Mexican-origin | male | 25–34 | 0.295 | 0.574 | 6.84 | 0.42 |
| Mexican-origin | male | 35–44 | 0.473 | 0.997 | 8.59 | 0.61 |
| Mexican-origin | female | 25–34 | 0.475 | 0.982 | 11.07 | 3.15 |
| Mexican-origin | female | 35–44 | 0.694 | 1.403 | 11.20 | 2.70 |

Priced with [SOURCE: SSA Monthly Statistical Snapshot, July 2026, Table 2, fetched
2026-09-18]: children of deceased workers receive **$1,179.88 a month** on average
(1,979,000 beneficiaries); non-disabled widowed mothers and fathers with a child in care
receive **$1,384.94 a month** (94,000 beneficiaries); the lump-sum death payment is **$255**
[SOURCE: ssa.gov/survivor/amount]. Eligibility runs to the child's 18th birthday, or 19 if
still in secondary school full time, and a surviving spouse qualifies only while caring for
a child under 16 [SOURCE: ssa.gov/survivor/eligibility; SSA POMS RS 00208.001].

Expected child-channel cost per homicide comes out at **$96,690 to $100,897** depending on
the offender group, almost all of it the child survivor benefit. Two caveats. The SSA
average is an average over all deceased workers, who are older and had higher primary
insurance amounts than a homicide victim; it is therefore **an overestimate for this
population** [INFERENCE]. And the family maximum (150–188% of the worker's PIA) binds in
larger families, which this calculation ignores.

The **foster-care arm is small and bounded**. Texas pays $57.71 a day for the basic service
level through a child-placing agency, $21,064 a year [SOURCE: Texas DFPS rate sheet
effective 2025-09-01, fetched 2026-09-18]; the national caseload was 331,747 children on
2025-09-30 [SOURCE: ACF AFCARS dashboard No. 33]. Charging **every** child-year where the
victim was the only resident parent to foster care adds just **$8,100 to $10,100** per
homicide, because that exposure averages under half a child-year per adult. Most such
children have a living non-resident parent, so the true figure is nearer the bottom of that
range. The central arm carries zero and the table below shows 0%, 25% and 100%.

### 3.4 Offender channel

Corrections at **$59,619 per prisoner-year** and mean time served for murder of **15.0
years** are the peer lane's figures (`crime_cost_2026_09_16/RESULT.md`, from BJS released
prisoners, which by construction excludes lifers). The life arm uses **23.1%** of persons
sentenced in state courts for murder or non-negligent manslaughter receiving a life sentence
[SOURCE: BJS, *Felony Sentences in State Courts, 2006*, NCJ 226846 — **the last edition BJS
published**, so this is a twenty-year-old parameter and is carried as a sensitivity, not a
point estimate]. A lifer is charged corrections to age 82, which overstates: prison life
expectancy is shorter than the general population's. The stock cross-check is 194,803 people
serving life, life without parole or a virtual life sentence of 50 years or more in 2024,
59% of them for homicide [SOURCE: The Sentencing Project, *A Matter of Life*].

The offender's own foregone fiscal profile is charged over the years served, from the same
period profiles. It adds $100k–$190k and moves nothing.

### 3.5 The combined table

Expected treasury cost of **one cleared homicide**, by offender ethnicity, integrating over
the victim age × ethnicity × sex distribution that each offender group actually produces
(SHR universe A 2019–2023, reweighted to the WONDER victim marginal). Partial account,
undiscounted, life share 23.1%, no foster arm:

| offender | mean offender age | mean victim age | victim channel | children | offender channel | **total** | share of $13.1m social cost | share of $13.7m VSL |
|---|---|---|---|---|---|---|---|---|
| Hispanic | 30 | 32 | **−56,487** | 100,897 | 1,503,436 | **1,547,846** | 11.8% | 11.3% |
| NH white | 38 | 40 | +21,432 | 100,836 | 1,485,050 | **1,607,318** | 12.3% | 11.7% |
| NH other | 34 | 34 | +49,764 | 98,774 | 1,572,789 | **1,721,327** | 13.2% | 12.6% |
| NH Black | 30 | 32 | +74,546 | 96,690 | 1,640,153 | **1,811,389** | 13.8% | 13.2% |

At a 3% discount rate the totals are $1.24m, $1.28m, $1.37m and $1.42m in the same order and
the victim channel turns positive for every group. On the complete account they are $0.99m,
$1.16m, $1.20m and $1.27m and the victim channel turns negative for every group.

**Read this table carefully.** The spread across offender groups is **17%**, and it is not
produced by anything about offenders' behaviour. It is produced by two mechanical facts:
the victims a group produces are mostly from the same group, and the groups' fiscal profiles
differ; and younger offenders under a life sentence serve more prisoner-years. The
Hispanic-offender cell is cheapest **because Hispanic victims score negative in the ledger**,
which is a property of the ledger, not of the homicide. Against the VSL every cell is
within 2 percentage points of the others and the ordering is noise.

**The VSL line, carried as instructed.** At $13.7m per statistical life, the 22,425 homicide
deaths of 2023 represent $307bn of mortality cost. The treasury lines above are 11–14% of
that. No fiscal ledger should be the operative number in a discussion about homicide.

---

## 4. Disconfirmation

The four tests were specified in the brief before any result was read.

### C1. Does the victim-ethnicity matrix change when missing ethnicity is imputed rather than dropped?

**Yes, materially, and only for the Hispanic row.** Three arms, universe A 2019–2023:

| offender | drop missing (n=25,675) | independent hot-deck per side (n=42,213) | **joint pair hot-deck (n=42,213)** |
|---|---|---|---|
| Hispanic → Hispanic victim | 0.717 | 0.554 | **0.667** |
| NH white → NH white victim | 0.809 | 0.743 | **0.811** |
| NH Black → NH Black victim | 0.813 | 0.798 | **0.803** |
| NH other → NH other victim | 0.663 | 0.620 | **0.631** |

The independent arm draws the victim's and the offender's ethnicity separately inside
race × state × year cells. That is the obvious implementation and it is **biased**: drawing
the two sides independently destroys the within-incident correlation, pushing the matrix
toward the product of the marginals and mechanically understating intra-group pairing. The
joint arm draws the *pair* from the observed joint distribution of same-race-pair,
same-state, same-year donors and conditions on whichever side is observed; it does not have
that defect. **The joint arm is the one to quote.**

Even so, the Hispanic intra-group share moves from 0.717 to 0.667 — a 5-point drop, five
times the movement in the white row — and the interracial Hispanic-offender/Black-victim
cell rises from 0.110 to 0.148. Offender composition of universe A moves only slightly
(Hispanic 0.190 → 0.195, white 0.259 → 0.265, Black 0.521 → 0.510). **Conclusion: the
Hispanic-offender row is the least well identified row in the matrix, and 0.72 should not be
quoted as a point estimate. The defensible statement is 0.67 with a plausible range of 0.55
to 0.72.**

### C2. Is the offender age difference more than population age structure?

**Partly, and less than half of it.** Age-specific offending rates, cleared
single-victim/single-offender criminal homicides per 100,000 population per year, using
CPS ASEC 2025 population by age × ethnicity (WONDER refused the population measure on this
crossing, so the denominator is CPS):

| age | Hispanic | NH white | NH Black |
|---|---|---|---|
| 15–19 | 3.3 | 1.4 | 16.5 |
| 20–24 | 5.2 | 2.6 | 28.8 |
| 25–29 | 5.1 | 2.7 | 26.5 |
| 30–34 | 4.2 | 2.6 | 18.4 |
| 40–44 | 2.8 | 2.1 | 11.5 |
| 55–59 | 1.4 | 1.2 | 4.7 |
| 65+ | 0.7 | 0.4 | 1.0 |

These are rates of **being identified as the offender in a cleared single-offender
homicide**, not offending rates. Roughly 45% of homicides reach that universe, so the levels
are low by about that factor; the ratios are the usable quantity and they inherit the
clearance selection of section 2.2.

Standardising the offender age distribution to the pooled population age structure closes
most but not all of the gap:

| | raw mean offender age | standardised |
|---|---|---|
| Hispanic | 32.9 | 35.5 |
| NH white | 39.4 | 38.0 |
| NH Black | 31.6 | 32.2 |

**The 6.5-year raw gap between Hispanic and white offenders falls to 2.5 years once the
populations' age structures are equalised — about 62% of it is demography.** The residual
2.5 years is real: the Hispanic offender rate peaks harder at 20–29 and falls off faster
after 45 than the white rate, which is comparatively flat across ages. This matters for the
cost table, where a younger offender is a more expensive offender under the life arm.

### C3. Does the cost by offender ethnicity change sign under the complete-account shift?

**The victim channel flips sign for every group; the total does not flip, it falls by
about a third, and the ordering is unchanged.**

| offender | victim channel, partial | victim channel, complete | total, partial | total, complete |
|---|---|---|---|---|
| Hispanic | −56,487 | −436,528 | 1,547,846 | 987,595 |
| NH white | +21,432 | −283,753 | 1,607,318 | 1,155,063 |
| NH other | +49,764 | −310,761 | 1,721,327 | 1,195,435 |
| NH Black | +74,546 | −300,593 | 1,811,389 | 1,265,071 |

The complete account charges every person-year a share of unallocated federal spending and
of interest on the deficit, which makes the marginal resident fiscally negative at almost
every age. On that account **every** homicide victim is a treasury gain and the only reason
a homicide still costs money is the prison sentence. This is the clearest possible
demonstration that the frame is not a valuation of life, and it is the reason the memo
leads with the VSL.

### C4. Sensitivity to the life-sentence arm

| offender | life share 0 | life share 0.231 | life share 1.0 |
|---|---|---|---|
| Hispanic | 1,004,647 | 1,547,846 | 3,057,702 |
| NH white | 1,137,471 | 1,607,318 | 2,805,562 |
| NH other | 1,186,229 | 1,721,327 | 3,113,773 |
| NH Black | 1,219,341 | 1,811,389 | 3,365,425 |

**This is the dominant uncertainty in the whole exercise — a factor of three, wider than
every other arm combined**, and it turns on a parameter BJS stopped publishing in 2006. It
also **reverses the Hispanic/white ordering**: at a life share of 1.0 the Hispanic-offender
cell becomes the *most* expensive, because Hispanic offenders are nine years younger and a
young lifer serves more prisoner-years. Any claim about the ranking of offender groups by
treasury cost is therefore **not identified** by this lane.

---

## 5. What is and is not identified

**Identified.**
- Victim ethnicity and age composition of US homicide, 2019–2023, from complete death
  registration (WONDER).
- SHR coverage, 80% of deaths, and its composition bias against Black victims.
- Clearance by victim ethnicity, and therefore the size of the selection that every
  offender-side table inherits.
- The magnitude ordering of the three cost channels: prison ≫ children > victim.

**Not identified.**
- **Mexican origin**, anywhere in the criminal-justice record. The ACS bridge is 53–75% and
  is an imputation.
- **The offender distribution for uncleared homicides**, which are 32% of all homicides and
  41% of those with Black victims.
- **The Hispanic-offender victim row** to better than ±0.08 (section 4, C1).
- **The victim's own counterfactual fiscal profile.** The lane uses group-by-age averages;
  homicide victims are strongly selected within those cells and the direction of the bias is
  known (overstatement) but not its size.
- **Dependents.** No crime record carries them. The children channel is imputed entirely
  from CPS cohort averages by age × sex × group, which is what the brief directs, but it
  means a childless victim and a father of four are priced identically inside a cell.
- **Period profile, not cohort.** Every lifetime figure applies today's cross-section to a
  83-year life. No growth, no behavioural response, no general equilibrium.
- **Life sentences**, the largest single uncertainty (C4), resting on a 2006 BJS parameter.
- **Conviction probability.** The cost table is per *cleared* homicide with an identified
  offender. Scaling to all homicides requires the clearance rate and a conviction-given-
  clearance rate that this lane did not source.

**Instrument bias.** `notes/llm-bias-caveat.md` applies with unusual force here. This memo
computes fiscal quantities attached to homicide by ethnic group, a configuration where an
LLM's post-training dispositions push in two directions at once: toward suppressing the
group comparison, and toward over-explaining it once computed. The defence used here is
mechanical — every table is generated by a script in the lane from a named public file, the
disconfirmation tests were specified in the brief before results were read, and the one test
that contradicted the headline (C1) is reported in the headline. The ordering of the cost
table is reported as **not identified** because C4 reverses it, not because the result is
uncomfortable.

---

## 6. Sources

- Murder Accountability Project, SHR 1976–2025, `SHR76_25a.csv`, 352,107,592 bytes, sha256
  `eeedbf5e58a4a2e91d88e8078341210bd2034b57e6d42d0e2de2667020b88a12`.
  https://www.murderdata.org/p/data-docs.html — fetched 2026-09-18.
- CDC WONDER, Underlying Cause of Death 2018–2024 Single Race (D158), 113-cause category
  GR113-127. https://wonder.cdc.gov/controller/datarequest/D158 — fetched 2026-09-18.
- US Census Bureau, ACS 2023 1-year PUMS tabulate API, HISP × TYPEHUGQ.
  https://api.census.gov/data/2023/acs/acs1/pums — fetched 2026-09-18.
- US Census Bureau, CPS ASEC March 2025, `asecpub25csv.zip` (repo copy).
- BJS, *Race and Hispanic Origin of Victims and Offenders, 2012–15*, NCJ 250747.
  https://bjs.ojp.gov/content/pub/pdf/rhovo1215.pdf — fetched 2026-09-18.
- BJS, *Felony Sentences in State Courts, 2006*. https://bjs.ojp.gov/content/pub/pdf/fssc06st.pdf
- The Sentencing Project, *A Matter of Life* (2024).
  https://www.sentencingproject.org/reports/a-matter-of-life-the-scope-and-impact-of-life-and-long-term-imprisonment-in-the-united-states/
- SSA, Monthly Statistical Snapshot, July 2026.
  https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/ — fetched 2026-09-18.
- SSA, survivor eligibility and amounts. https://www.ssa.gov/survivor/eligibility ;
  https://www.ssa.gov/survivor/amount — fetched 2026-09-18.
- Texas DFPS residential child-care rates, effective 2025-09-01.
  https://www.dfps.texas.gov/Doing_Business/Purchased_Client_Services/Residential_Child_Care_Contracts/rates.asp — fetched 2026-09-18.
- HHS ACF, AFCARS dashboard No. 33 (caseload 2025-09-30).
- US DOT, revised departmental VSL guidance, $13.7m base year 2024 ($14.2m for 2025).
  https://www.transportation.gov/office-policy/transportation-policy/revised-departmental-guidance-on-valuation-of-a-statistical-life-in-economic-analysis — fetched 2026-09-18.
- Unit costs and corrections cost: `infra/immigration-fiscal/crime_cost_2026_09_16/RESULT.md`
  (McCollister, French & Fang 2010, restated to 2024 dollars).
- Period profiles: `infra/immigration-fiscal/pronatal_equivalence_2026_09_18/`.
  Complete-account shift: `infra/immigration-fiscal/gap_interest_2026_09_18/derived/audit.json`.
