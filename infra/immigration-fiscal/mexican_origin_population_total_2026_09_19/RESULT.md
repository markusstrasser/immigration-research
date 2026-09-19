claude-opus-5[1m]

# The real size of the Mexican-origin population across generations

**Verdict:** 40 million is a little too low, not badly too low. The CPS ASEC 2025
self-identification union reproduces at **40.97M ± 0.38M**; the ACS ancestry write-in
gives a *smaller* population, not a larger one; ethnic attrition adds a measured
**+0.80M** and a central **+1.8M**; and coverage adds at most another **7.6%**. The
defensible central total is **42–45M** and the floor is **41.8M**. The reason the
correction is small is the lane's main finding: reproducing Duncan and Trejo's design
on today's CPS, ethnic attrition among Mexican-origin children runs at **roughly a
third to a half of their 1994–2006 rates** — third-generation children identify as
Mexican at 88.8% against their 71.8%, and as Hispanic at 93.7% against Duncan and
Trejo's 81.7% for 2003–2013. The repo's standing "17% of third-generation children"
figure (ladder 67) is a stale 2003–2013 pan-Hispanic number. Two thirds of the 40.97M
is definitionally immune to attrition anyway, because generations one and two are
defined by birthplace and parental birthplace, not by self-identification. On the
fiscal side the larger population *narrows* the per-person gap against third-plus
whites from −$7,105 to between −$6,969 and −$6,457 and moves the aggregate from
−$290.6bn to between −$290.6bn and −$301.2bn.

Arms 1, 2, 3, 4 and 5 all landed. Emeka & Vallejo 2011 was not obtained as a PDF and
is the one item skipped; §7 says what was done instead.

---

## 1. Arm 1 — the self-identification baseline, reproduced

CPS ASEC 2025 public-use person file, 142,125 records, income year 2024, interview
February–April 2025. Standard errors are successive-difference replication on the
160 published replicate weights, variance factor 4/160.
[SOURCE: `derived/arm1_counts_cps.csv`; CALCULATION `cps_counts.py`]

| Definition | Population | SE | n |
|---|---|---|---|
| G1 Mexico-born, foreign-born (`PENATVTY`=303, `PRCITSHP` 4/5) | 12.231M | 0.248M | 5,637 |
| G1 Mexico-born, any citizenship | 12.605M | 0.254M | 5,808 |
| G2 native, ≥1 Mexico-born parent | 14.354M | 0.284M | 6,364 |
| G3+ native, two US-area parents, `PRDTHSP`=1 | 14.383M | 0.309M | 6,373 |
| **UNION, repo definition** | **40.968M** | **0.379M** | 18,374 |
| All self-identifying Mexican, any nativity | 40.360M | 0.365M | 18,105 |
| Native self-ID Mexican in neither G2 nor G3+ | 0.661M | 0.059M | 284 |
| UNION, Census Bureau construction | 40.688M | 0.366M | 18,234 |

The Census Bureau's published 2024 generation table gives 12.10M / 13.79M / 13.13M =
**39.0M**. [SOURCE: `https://www2.census.gov/programs-surveys/demo/tables/foreign-born/2024/cps2024/2024_asec_generation_table4.xlsx`,
held at `../acs_institutional_2026_09_16/cps_2024_asec_generation_table4.xlsx`]
Rebuilding the Bureau's own construction on the 2025 file — second generation is
Mexican self-identification *plus* any foreign-born parent — gives 40.69M, so the
39.0M / 41.0M difference is one survey year plus that construction, not a coding
error. A 0.66M residual group (native, self-identifies Mexican, has one US-born and
one non-Mexican foreign-born parent) falls between the two constructions and is
counted by neither; it belongs in any careful total.

**The structural point that bounds everything below.** Of the 40.97M, 12.23M is fixed
by the respondent's own birthplace and 14.35M by the parents' birthplaces. Neither
can attrite. Only the 14.38M third-plus cell — 35% of the total — is a
self-identification count, so no attrition correction, however large, can move the
total by more than what that one cell can absorb.

## 2. Arm 2 — the ancestry definition gives a *smaller* population

ACS 2024 1-year PUMS, 3,422,888 person records, 80 replicate weights, factor 4/80.
Mexican ancestry is `ANC1P` or `ANC2P` in {210, 211, 212, 213, 215, 218, 219}.
[SOURCE: `derived/arm2_ancestry_crosstab.csv`, `arm2_ancestry_totals.csv`]

| ACS 2024 definition | Population | SE |
|---|---|---|
| Self-identification (`HISP` Mexican or Mexico-born) | 39.430M | 0.075M |
| Ancestry write-in (`ANC1P`/`ANC2P` Mexican) | 27.686M | 0.094M |
| Union of both self-reports | 40.544M | 0.072M |
| Gain from adding the ancestry question | **+1.115M** | — |

The cross-tab is the interesting part:

| Cell | Population | SE |
|---|---|---|
| Mexican ancestry **and** `HISP` Mexican | 26.470M | 0.094M |
| Mexican ancestry, reports another Hispanic origin | 0.884M | 0.019M |
| Mexican ancestry, reports **not Hispanic** | 0.331M | 0.011M |
| `HISP` Mexican, **no** Mexican ancestry | 12.462M | 0.072M |
| …of which, ancestry not reported at all | 7.992M | 0.062M |

This arm was run to see whether a second self-report recovers the missing population.
It does not. Twelve and a half million people who call themselves Mexican on the
Hispanic-origin question write no Mexican ancestry, and eight million of those write
no ancestry at all — the ACS ancestry item is dominated by non-response and is a
**weaker** instrument than the origin question, not a truer one. The one cell that
does the work conceptually, Mexican ancestry with a "no" on Hispanic origin, is
0.331M, or 1.20% of everyone claiming Mexican ancestry. Ancestry is a second
self-report with its own drift, not an attrition correction, and on these numbers it
is the drift that dominates. [FRAMING-SENSITIVE: which of the two self-reports is
treated as the truer one is a judgment, and the two disagree in both directions]

## 3. Arm 3 — attrition reproduced, and it has fallen by half

### 3.1 Method

Children are linked to co-resident parents through the `PEPAR1` / `PEPAR2` line
pointers; the linked parent's own `PEMNTVTY` / `PEFNTVTY` reveal the child's
grandparents' birthplaces. Mexican descent is therefore observed objectively, and the
measure is immune to the parent's own identification — a second-generation parent who
has stopped calling themselves Mexican still reports Mexico as their parent's
birthplace. [CALCULATION: `cps_counts.py`, `dt_replication.py`]

### 3.2 Rates by generation and parentage

Share of objectively Mexican-descent children **not** identified as Mexican, CPS ASEC
2025, SDR standard errors in parentheses.
[SOURCE: `derived/arm3_attrition_children.csv`]

| Group | not Mexican | not Hispanic at all | n |
|---|---|---|---|
| 2nd generation (any parent Mexico-born) | 6.32% (0.68) | 2.90% (0.44) | 3,868 |
| 2nd gen, both parents Mexican descent | 3.46% (0.71) | 1.74% (0.45) | 2,375 |
| 2nd gen, one parent Mexican descent | 10.74% (1.23) | 4.70% (0.89) | 1,493 |
| 3rd generation (≥1 Mexico-born grandparent) | 9.19% (1.00) | 5.05% (0.71) | 1,615 |
| 3rd gen, 4 of 4 Mexico-born grandparents | 2.10% (1.18) | 0.00% (0.00) | 253 |
| 3rd gen, 3 of 4 | 7.13% (3.30) | 1.49% (1.56) | 105 |
| 3rd gen, 2 of 4 | 11.78% (2.69) | 7.97% (2.12) | 336 |
| 3rd gen, 1 of 4 | 21.99% (3.50) | 15.28% (2.77) | 307 |

The gradient is monotone in the number of Mexico-born grandparents and the
mixed-parentage channel is the whole story, exactly as the literature says. Age bands
are flat: third-generation attrition is 9.23% at ages 0–5, 9.53% at 6–11 and 9.10% at
12–17, so there is no sign of the "higher for youth" pattern in this file.

### 3.3 Strict replication of Duncan & Trejo 2011 Table 8

Their sample: US-born children aged 17 and below in intact families with at least one
parent or grandparent born in Mexico, or at least one parent identified as Mexican;
suspected stepchildren excluded. This lane can exclude stepchildren exactly, because
CPS ASEC carries `PEPAR1TYP` / `PEPAR2TYP`.
[SOURCE: Duncan & Trejo 2011, *Journal of Labor Economics* 29(2):195–227; CReAM
Discussion Paper 02/09 copy, Table 8 on PDF page 49, narrative on PDF pages 29–30;
their source is 1994–2006 CPS data. `derived/arm3_dt_table8_replication.csv`]

Percent identified as Mexican:

| Cell | CPS 2025 | SE | Duncan & Trejo 1994–2006 |
|---|---|---|---|
| 2nd gen, both parents Mexico-born | 96.79 | 0.78 | 97.9 |
| 2nd gen, one parent Mexico-born | 86.48 | 2.10 | 80.6 |
| **2nd gen, all** | **92.46** | **1.01** | **92.4** |
| 3rd gen, four grandparents Mexico-born | 97.99 | 1.32 | 96.2 |
| 3rd gen, three grandparents | 91.30 | 4.08 | 95.2 |
| 3rd gen, two grandparents | 89.05 | 2.71 | 78.7 |
| 3rd gen, one grandparent | 78.04 | 4.29 | 58.4 |
| **3rd gen, all** | **88.81** | **1.53** | **71.8** |
| 4th+ gen, both parents identified Mexican | 98.44 | 1.24 | 98.4 |
| 4th+ gen, one parent identified Mexican | 81.90 | 2.38 | 50.1 |
| **4th+ gen, all** | **88.28** | **1.62** | **70.8** |
| **All US-born Mexican children** | **90.45** | **0.82** | **84.2** |

The second generation reproduces to the first decimal — 92.46% against 92.4% — which
is the validity gate. The method is right; the third-generation divergence is real.
Restricting to biological parents only moves nothing material (3rd gen all 89.38%).

On the broader Hispanic outcome, the same third-generation sample identifies as
Hispanic at **93.74%** (se 1.14) against Duncan & Trejo 2017's **81.7%** for
2003–2013. [SOURCE: `derived/arm3_dt_hispanic_definition.csv`; Duncan & Trejo 2017,
*ILR Review* 71(5), Table 1 p. 8: 98.6 / 93.1 / 81.7 for first-generation adults,
second-generation adults and third-generation children, pooled over Mexico, Puerto
Rico, Cuba, El Salvador and the Dominican Republic]

Decomposing the 28.25% → 11.19% fall in third-generation attrition
[SOURCE: `derived/arm3_dt_decomposition.csv`]:

| Arm | Third-generation attrition |
|---|---|
| Duncan & Trejo composition × their rates | 28.25% |
| CPS 2025 composition × their rates | 20.09% |
| Their composition × CPS 2025 rates | 15.25% |
| CPS 2025 composition × CPS 2025 rates | 11.19% |

Both terms matter and the rate term is the larger. Today's third generation has more
Mexico-born grandparents (25% have all four, against 10% in their sample) because the
Mexican second generation grew so much; and within every grandparent cell,
identification is higher than it was.

### 3.4 Disconfirmation: is this an imputation artefact?

If the CPS hot deck matched on Hispanic origin when imputing parental birthplace, a
child's imputed grandparent birthplace would agree with the child's own ethnicity by
construction and depress the measured attrition rate. It does not.
[SOURCE: `derived/arm3_allocation_check.csv`; CALCULATION `allocation_check.py`]
Allocation is rare — 99.2% of records have the child's ethnicity unallocated and
99.2% have all parental birthplace fields unallocated — and restricting to wholly
unallocated cases moves third-generation attrition from 9.19% **down** to 8.17%, and
second-generation attrition from 6.32% down to 5.42%. The imputed cases carry
slightly *more* attrition, not less. The finding survives.

### 3.5 What the literature says, from the primary PDFs

- **Duncan & Trejo 2011** (CReAM DP 02/09 copy, PDF pp. 29–30): "Among all U.S.-born
  children in the CPS with some identifiable Mexican ancestry, 16 percent do not
  subjectively identify as Mexican, and this rate of ethnic attrition rises to almost
  30 percent for children in the third generation and beyond." Table 10, PDF p. 51, narrative PDF p. 30:
  the fathers of third-generation children who do **not** identify average 13.3 years
  of schooling against 12.4 for those who do, are half as likely to be dropouts
  (12% vs 22%) and twice as likely to be college graduates (23% vs 11%).
- **Duncan & Trejo 2017** (ILR Review 71(5), Table 8 p. 23, Mexico row): non-identifiers
  have **+0.76 years** of schooling (se 0.11) among second-generation adults and
  **+0.57 years** of parental schooling (se 0.08) among third-generation children,
  conditional on controls. Table 2 p. 9, pan-Hispanic: 12.88 vs 13.64 years for
  second-generation adults, 13.17 vs 14.00 parental years for third-generation
  children.
- **Duncan & Trejo 2025** (AEA P&P 115:451–56 / IZA DP 17579, Table 1 on PDF p. 8,
  2000 Census + 2001–2019 ACS): Mexican immigrant parents who arrived as children fail
  to identify as Hispanic at 1.05% (arrived 0–8) against 0.79% (9–14); their US-born
  children at **3.33% vs 2.19%**. Table 3 on PDF p. 11: the other parent's nativity
  and Hispanicity account for **85.9%** of the explained part of the age-at-arrival
  effect. This lane's second-generation "not Hispanic at all" rate, 2.90% (se 0.44),
  sits inside their 2.19–3.33% band measured on a different instrument and decade.
- **1970 Census Content Reinterview Study** (US Bureau of the Census 1974, Table C
  p. 8, reproduced as Duncan & Trejo 2011 Table 2, PDF p. 43): Hispanic identification 98.7%
  first generation (n=77), 83.3% second (n=90), 73.0% third (n=89), 44.4% fourth
  (n=27), 5.6% fifth-plus (n=18); 97.0% with Hispanic ancestry on both sides against
  21.4% on one side. Duncan and Trejo themselves say these "should be regarded with
  caution."

### 3.6 Bounding the correction

The self-identified third-plus cell splits into exact third-generation identifiers and
fourth-plus identifiers. CPS measures the first group's attrition directly and cannot
see the second group's at all: a fourth-generation person of Mexican descent whose
parents both stopped identifying leaves no trace in the file. Measured on children
with two US-area-born parents [SOURCE: `derived/arm3_multiplier.csv`]: 3.770M self-ID
Mexican, of whom 1.668M are exact third generation and 2.102M are fourth-plus; 0.210M
third-generation attriters are recoverable; the third-generation identification rate
is 88.81%. [SOURCE: `derived/arm3_correction_bounds.csv`]

| Assumption on fourth-plus identification | Third-plus | Union | Added |
|---|---|---|---|
| Floor: third-generation attriters only | 15.185M | **41.770M** | +0.80M |
| Fourth-plus identifies at the measured third-generation rate (88.8%) | 16.195M | **42.780M** | +1.81M |
| Fourth-plus at Duncan & Trejo's 1994–2006 rate (70.8%) | 18.492M | **45.077M** | +4.11M |
| Fourth-plus at the 1970 reinterview fourth-generation rate (44.4%) | 25.227M | **51.812M** | +10.84M |

The last row is an upper bound and not an estimate: it rests on 27 observations from a
1970 population that was overwhelmingly old-stock Southwest, and every modern
measurement in this lane says identification is rising, not falling.

**Fractional counting.** Weighting each third-generation person by the share of their
grandparents born in Mexico (a quarter each) multiplies the third generation by
**0.5916** [SOURCE: `derived/arm3_fractional_counting.csv`]. On the central arm the
third-plus becomes 9.58M "Mexican-equivalent persons" instead of 16.20M. This is a
convention, not a measurement, and both are reported: whole-person counting answers
"how many people have Mexican ancestors", fractional counting answers "how much
Mexican ancestry is there". The fiscal arm uses whole persons throughout, because a
person consumes and pays whole.

## 4. Arm 4 — coverage adds at most 7.6%, and the naive multiplier is wrong

The CPS ASEC estimation procedure "adjusts weighted sample results to agree with
independently derived population controls", distributed by age, sex and Hispanic
origin among other margins. [SOURCE: CPS March 2025 technical documentation,
"Estimation Procedure", p. 4] Overall CPS undercoverage for March 2025 is about 11%,
and the March 2025 Hispanic coverage ratios are 0.81 male and 0.83 female for all ages
[SOURCE: same document, "Undercoverage" and Table 3, p. 7] — but that ratio is defined
as "the estimated population *before poststratification* divided by the independent
population control". After poststratification the CPS Hispanic estimate equals the
control by construction. **Multiplying the CPS Mexican-origin count by 1/0.82 would
double-count the weighting adjustment.** What remains is error in the controls.

The controls are built from a Blended Base drawing on the 2020 Census, the 2020
Demographic Analysis estimates and Vintage 2020 postcensal estimates, precisely
because of the 2020 Census's coverage problems [SOURCE: same document, footnote 19,
p. 10], so the 2020 Post-Enumeration Survey's Hispanic net undercount of **4.99%**
(se 0.53, statistically significant; non-Hispanic white alone **+1.64%** overcount)
[SOURCE: 2020 PES, "Net Coverage Error and Components of Census Coverage for Race
Groups and Hispanic Origin", Table B] is already partly absorbed. It is an upper bound
on the census-base component, not an additive correction.

| Scheme | US-born | Legal Mexico-born | Unauthorized Mexico-born | Adjusted union | Multiplier |
|---|---|---|---|---|---|
| A: controls are right | 0% | 0% | 0% | 40.968M | 1.0000 |
| B: PES Hispanic on everyone | 4.99% | 4.99% | 4.99% | 43.120M | 1.0525 |
| C: PES plus DHS OHSS decay on the unauthorized | 4.99% | 4.99% | 8.82% | 43.322M | 1.0574 |
| D: PES plus CMS 5/37 on the unauthorized | 4.99% | 4.99% | 20.97% | 44.092M | 1.0762 |
| E: unauthorized only | 0% | 0% | 20.97% | 42.180M | 1.0296 |

[SOURCE: `derived/arm4_coverage_grid.csv`] The unauthorized Mexico-born are 4.567M of
the 12.231M Mexico-born (37.3%), taken from the parallel lane rather than re-derived
[SOURCE: `../unauthorized_population_size_2026_09_19/derived/cps2025_residual_by_region.csv`].
The DHS OHSS scheme is 13% for the most recent arrival year declining 7.5% per year of
presence; CMS is 5% for pre-2021 entrants and 37% for 2021–2024 entrants, both as
settled by that lane. Applied through `PEINUSYR` band midpoints these average 3.29%
and 7.83% across all Mexico-born, which is why the union multipliers stay small: most
Mexico-born arrived long ago and most Mexican-origin people are US-born.

## 5. Arm 5 — the larger population narrows the per-person gap

Per-person and aggregate balances are the all-age ledger's, read-only, scenario
`all_age_shared`, age-band matched against third-plus non-Hispanic whites
[SOURCE: `../all_age_ledger_2026_09_17/derived/estimates.csv`]: Mexico-born −$8,437
(12.221M, −$103.1bn), Mexican second generation −$7,934 (14.333M, −$113.7bn),
self-identified third-plus −$5,143 (14.343M, −$73.8bn), union −$7,105 (40.897M,
−$290.6bn). The ledger's union population is 0.07M below this lane's because it
restricts to `PRPERTYP`=2 or age under 15.

Attriter characteristics, stated explicitly. On this file, adults 25+ in the Mexican
third-plus average **13.335** years of schooling against **14.384** for third-plus
non-Hispanic whites, a gap of **1.049 years** [SOURCE:
`derived/arm5_education_selectivity.csv`]. Duncan & Trejo's measured attriter
advantage of +0.76 years therefore closes **72.4%** of that gap, so the middle arm
assigns attriters 27.6% of the third-plus gap, −$1,418 per person. The three arms are:
fully converged (attriter gap $0), Duncan–Trejo selectivity (−$1,418), halfway
(−$2,572). [SOURCE: `derived/arm5_fiscal_implication.csv`]

| Population arm | Added | Attriter characteristics | Gap per person | Aggregate |
|---|---|---|---|---|
| — (standing) | — | — | −$7,105 | −$290.6bn |
| Floor, +0.80M | 0.80M | fully converged | −$6,969 | −$290.6bn |
| Floor | 0.80M | Duncan–Trejo | −$6,996 | −$291.7bn |
| Floor | 0.80M | halfway | −$7,018 | −$292.6bn |
| Central, +1.81M | 1.81M | fully converged | −$6,804 | −$290.6bn |
| Central | 1.81M | Duncan–Trejo | −$6,864 | −$293.2bn |
| Central | 1.81M | halfway | −$6,913 | −$295.2bn |
| DT 4th-plus, +4.11M | 4.11M | fully converged | −$6,457 | −$290.6bn |
| DT 4th-plus | 4.11M | Duncan–Trejo | −$6,586 | −$296.4bn |
| DT 4th-plus | 4.11M | halfway | −$6,692 | −$301.2bn |
| 1970 bound, +10.84M | 10.84M | fully converged | −$5,616 | −$290.6bn |
| 1970 bound | 10.84M | Duncan–Trejo | −$5,913 | −$306.0bn |
| 1970 bound | 10.84M | halfway | −$6,155 | −$318.5bn |

Reading. Adding attriters back always **narrows** the per-person gap, because they are
better off than the people who kept identifying — the selection runs the way Duncan
and Trejo say it does. The aggregate moves the other way or not at all: under full
convergence it is unchanged by construction (attriters carry a zero gap), and under
the other two arms it widens by $1–28bn because more people each carry some deficit.
So the attrition correction improves the group's *average* standing and slightly
worsens its *total*, and the direction of the headline depends on which quantity the
argument is about. [FRAMING-SENSITIVE] Across the entire grid the per-person gap stays
between −$5,616 and −$7,018 and the aggregate between −$290.6bn and −$318.5bn: the
ledger's order of magnitude does not move.

## 6. The answer: is 40M too low, and by how much

Yes, but modestly. The measured self-identification union is 40.97M ± 0.38M, and the
ancestry question does not raise it — on the ACS the ancestry definition gives 27.7M
against 38.9M for self-identification, and the union of both is 40.54M, so a second
self-report subtracts credibility from the idea that self-identification hides
millions. Ethnic attrition is real, positively selected and concentrated in mixed
parentage, exactly as Duncan and Trejo described, but it is smaller now than when they
measured it: the third generation identifies as Mexican at 88.8% against their 71.8%
and as Hispanic at 93.7% against 81.7%, the second generation reproduces their number
to the decimal, and the fall survives an imputation check. That leaves a measurable
floor of +0.80M, a central +1.8M, and +4.1M only if the unobservable fourth-plus
generation still attrites at mid-2000s rates. Coverage adds between zero and 7.6%, and
the popular 1/0.82 multiplier is a double count of the CPS weighting. Stacking the
central attrition arm on the PES coverage arm gives **45.0M**; the floor with no
coverage adjustment gives **41.8M**; the outside band running the 1970 reinterview
rates and the CMS coverage scheme reaches **55.8M** and should not be quoted as an
estimate. The honest headline is **42–45 million**, about **5–10% above** the standing
figure, with two thirds of the population immune to the correction by construction.

## 7. What was skipped, and every limit

- **Emeka & Vallejo 2011** (*Social Science Research* 40(6):1547–63) has no
  open-access PDF; `fetch_paper` on the DOI and two PubMed Central routes all failed.
  Their headline — 6% of respondents with Latin American ancestry answered "no" to the
  Hispanic-origin question in the 2006 ACS — is `[UNVERIFIED]`, taken from the
  Semantic Scholar abstract record, not from the paper. The same statistic was
  rebuilt on ACS 2024 instead: **2.09%** of people with any Latin American or Hispanic
  ancestry answer "not Hispanic", and **1.20%** of those with Mexican ancestry
  specifically [SOURCE: `derived/arm2_emeka_vallejo.csv`]. If the 6% is right, that is
  the same two-thirds fall in attrition the Duncan–Trejo comparison shows, on a third
  instrument. The page-referenced quotation the brief asked for could not be produced
  for this paper.
- **Attrition rates are measured on co-resident children and extrapolated to adults.**
  This is the load-bearing extrapolation. Children are observed in their parents'
  households, so the intermarriage history that produces attrition is the *parents'*,
  not the person's own; today's adults are the children of an earlier, less
  intermarried cohort, which argues the child-based rate overstates adult attrition,
  while adults have had a lifetime for identification to drift, which argues the other
  way. Neither direction is quantified here.
- **Fourth-plus attrition is unobservable in the CPS by construction**, and it is the
  largest single source of uncertainty in the total. The three assumptions in §3.6 are
  assumptions, not measurements.
- **The child's ethnicity is reported by the household respondent, usually a parent**,
  not by the child. Duncan & Trejo 2011 Table 9 (PDF p. 50) shows this matters a
  little: third-generation identification is 70.5% when the father responds, 71.5%
  when the mother does and 79.7% when someone else does.
- **Ancestry is a self-report with its own drift** and, on the ACS, massive
  non-response: 8.0M people who call themselves Mexican write no ancestry at all.
- **Coverage multipliers are assumptions.** The PES measures the 2020 Census, not the
  CPS; the OHSS and CMS rates were built for the unauthorized residual, not for a
  whole-population count.
- **Fractional counting is a convention**, given alongside whole-person counting
  everywhere it appears.
- The ACS and CPS disagree on the Mexico-born by 0.64M (11.59M against 12.23M) and on
  the self-identifying Mexican population by 1.43M (38.93M against 40.36M). Both are
  inside a couple of standard errors of nothing only on the first; the second is a
  real instrument difference and is not adjudicated here.
- This is a resident stock, not an admission question. Every gap is a benchmark
  contrast against third-plus non-Hispanic whites inside a partial annual account with
  no public goods, corporate tax incidence or general equilibrium. No policy advice is
  given or implied.

## 8. Draft memo section

> **How many people of Mexican origin are there, really?** The repo's union count is
> 40.97M ± 0.38M on CPS ASEC 2025 — 12.23M born in Mexico, 14.35M US-born with a
> Mexico-born parent, 14.38M US-born with two US-born parents who call themselves
> Mexican. Only the last of those three is a self-identification count, so only that
> third of the population can be hidden by ethnic attrition. Reproducing Duncan and
> Trejo's design on the current file — linking children to parents through the CPS
> parent pointers so that grandparents' birthplaces are observed rather than
> self-reported — their second-generation number comes back to the decimal (92.46%
> identify as Mexican against their 92.4%), which validates the method, and their
> third-generation number does not: 88.8% against 71.8%. On the broader Hispanic
> question the current third generation identifies at 93.7% against the 81.7% Duncan
> and Trejo measured for 2003–2013. Half the change is composition — today's third
> generation has more Mexico-born grandparents, because the second generation grew so
> much — and half is a genuine rise in identification within every grandparent cell.
> The gradient they found is intact: attrition runs 2.1% for children with four
> Mexico-born grandparents and 22.0% for those with one, and intermarriage is 86% of
> the explained channel in their own 2025 decomposition. It is the level that has
> fallen. Correcting the self-identified third-plus for the attrition the CPS can
> actually see adds 0.80M; assuming the fourth generation and beyond attrites at the
> same rate as the third adds 1.81M; assuming it still attrites at 1990s rates adds
> 4.11M. Survey coverage adds between nothing and 7.6%, and the familiar move of
> dividing by the CPS Hispanic coverage ratio of 0.82 is wrong, because that ratio is
> measured before the weighting that corrects it. The defensible total is 42 to 45
> million. The ancestry question, which ought to recover attriters if anything does,
> instead gives a smaller population than self-identification (27.7M against 38.9M on
> the ACS) and adds only 1.1M to the union, because eight million people who call
> themselves Mexican write no ancestry at all. Because attriters are better educated —
> Duncan and Trejo put them 0.76 years ahead, which closes 72% of the Mexican
> third-plus's 1.05-year schooling gap to third-plus whites — adding them back narrows
> the per-person fiscal gap from −$7,105 to −$6,864 on the central arm and leaves the
> aggregate between −$291bn and −$301bn. The correction is real, it runs in the
> direction the literature predicts, and it is smaller than the literature's own
> vintage numbers imply.
