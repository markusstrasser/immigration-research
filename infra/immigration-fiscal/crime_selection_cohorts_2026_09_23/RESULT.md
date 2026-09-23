claude-opus-5-5[1m]

**Verdict:** Mostly no. Our data do not show each Mexican arrival cohort more positively selected
than the last. The sentence about interstate movers is overstated.

Butcher and Piehl's "increasingly positive selection" covers all immigrants and is measured as a
gap in percentage points. On a ratio scale, their own Table 2 puts arrivals of 0–5 years at 0.21
of the native rate in 1980, 0.31 in 1990 and 0.11 in 2000, so the 1980s arrivals were worse
[SOURCE: w13229 Table 2].

For Mexico-born men 18–40 at 0–5 years in the US, the ratio of their institutional share to that
of US-born men of the same ages was:

- 0.45 (SE 0.05) for the 1975–80 arrivals, in 1980;
- 0.42 (0.04) for the 1985–90 arrivals, in 1990;
- 0.13 (0.01) for the 1995–2000 arrivals, in 2000.

At 6–15 years, the cohorts observed in 1990 were worse than those observed in 1980 (0.50–0.54
against 0.30–0.31) [DATA: `derived/census_cohort_rates.csv`].

Only the 2000 census shows a large fall, and it shows it for every cohort. The same 1985–89
arrivals stood at 0.42 in 1990 and 0.19 in 2000. That census recorded a birthplace for only 32% of
Mexican-origin men in institutions. It classified 1.8% of the rest as foreign-born, against 38.5%
of those it recorded [DATA: `derived/census_allocation_mexorig.csv`]. Its Mexico-born count is too low.
Its count of all institutionalized noncitizens (73,395) is below the 89,676 noncitizens that BJS
counted in state and federal prisons alone at midyear 2000 [DATA: `derived/admin_check_2000.csv`;
SOURCE: BJS NCJ 198877, Table 6].
Spreading allocated birthplaces in the reported mix raises the 2000 ratios 2.1–2.6-fold and the
1980 and 1990 ratios 1.4–1.7-fold. Under that correction, at 0–5 years the three cohorts stand at
0.69–0.75, 0.59–0.65 and 0.26–0.33. The 1980s arrivals are still no clear improvement, and at 0–5
years the 1990s arrivals are the only cohort that improved [CALCULATION:
`derived/census_cohort_reassigned.csv`].

In the ACS for 2006–2019, men at 6–10 years in the US stood at 0.53, 0.58 and 0.61 of US-born men
across successive arrival cohorts. With education held fixed the figures are 0.16–0.19. There is
no improvement [DATA: `derived/acs_cohort_pooled.csv`, `acs_cohort_education.csv`].

US-born men living outside their birth state are institutionalized less than stayers at the same
ages: −0.54 to −0.62 points in 2019–2024. At the same ages and schooling the gap is −0.06 to
−0.09. Butcher and Piehl themselves report movers higher once education is held [DATA:
`derived/acs_movers.csv`; SOURCE: w13229 fn 23].

# Crime selection by arrival cohort: Mexico-born men 18–40, 1980–2024

Question (operator): "Selection is the main explanation. Butcher & Piehl found each recent cohort
more positively selected than the last. Americans who move between states show the same pattern.
-- can we see that in our data?" The three sentences are our own earlier chat answer.

Outcome throughout: the share of men living in an institution (prisons, jails, immigration
detention, psychiatric and long-term care) on census or survey day. This measures custody. It is
not a crime rate; see the lane rule in
`research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md`. A ratio below 1 means a
lower institutional share than US-born men of the same single years of age (indirect
standardization) [CALCULATION: `cohort_lib.standardized`].

## Part 1: what Butcher and Piehl say

Sources read in full:

- NBER w13229 (July 2007), Marker parse in the local corpus
  (`~/Projects/corpus/doi_10_3386_w13229`) [SOURCE: https://doi.org/10.3386/w13229].
- NBER w6067 (June 1997), the working paper behind the 1998 *ILR Review* article "Recent
  Immigrants: Unexpected Implications for Crime and Incarceration". It was downloaded from nber.org
  and OCRed with tesseract, because the scan's text layer is mirrored
  (`_cache/papers/w6067_ocr.txt`) [SOURCE: https://www.nber.org/papers/w6067].

The 1998 *JPAM* cross-city paper was not read. It studies city crime rates, and the mover
comparison is in the 2007 paper.

### Sentence 1: "Selection is the main explanation."

Supported, with a qualifier the chat answer dropped. The abstract reads: "the process of migration
selects individuals who either have lower criminal propensities or are more responsive to deterrent
effects than the average native" [SOURCE: w13229 abstract]. Their "selection" therefore includes
selection on how strongly men respond to deterrence.

They rule out deportation with one test. Naturalized citizens, who cannot be deported, lowered
their relative rates at least as much as other immigrants (Table 4) [SOURCE: w13229 §A].

### Sentence 2: "Butcher & Piehl found each recent cohort more positively selected than the last."

The authors say this about all immigrants, measured in percentage points. For the 1980s, their own
raw table does not show it on a ratio scale.

- **Their claim.** "the newly arrived immigrants in the 1980s and 1990s seem to be particularly
  unlikely to be involved in criminal activity, consistent with increasingly positive selection
  along this dimension" [SOURCE: w13229 abstract]. The 1997 paper: "the recent immigrants in 1990
  have from 0.43 percent to 1.3 percentage point lower relative institutionalization rates than the
  recent immigrants in 1980" [SOURCE: w6067 p. 22].
- **Their test.** Table 5, column 1, uses a logit marginal effect with age controls. The gap
  between arrivals of 0–5 years and natives changed by −0.0044 (SE 0.0005) from 1980 to 1990 and by
  −0.0110 (SE 0.0005) from 1990 to 2000 [SOURCE: w13229 Table 5].
- **Scope.** All foreign-born men 18–40. Mexico is never broken out [SOURCE: w13229 full text].
- **Raw rates, Table 2.** Arrivals of 0–5 years: 0.29% (1980), 0.68% (1990), 0.37% (2000).
  Natives: 1.35%, 2.17%, 3.45%. As ratios these are 0.21, 0.31 and 0.11; at 5–10 years they are
  0.27, 0.54 and 0.14 [CALCULATION: Table 2 cells divided].
- **Reading.** The "increasingly positive" reading of the 1980s rests on a gap in percentage points
  that widened because the native rate rose during the prison boom [INFERENCE].
- **Their allocation check.** They dropped records with allocated variables and found "qualitatively
  similar results, though the estimated cohort effects are less negative" [SOURCE: w13229 §A].
  Part 2b shows why that check does not settle the question.

### Sentence 3: "Americans who move between states show the same pattern."

Overstated. The comparison exists in the 2007 paper, but it is not a cohort pattern, and its sign
depends on controls.

- Verbatim: "In 1980, native-born movers were 0.04 percent less likely than nonmovers to be
  institutionalized. By 1990, this difference had risen to 0.2%, and by 2000 to 0.3%."
- Footnote 23: "These results come from logits controlling for a full set of age dummies, available
  upon request. Once education is controlled, native movers have higher institutionalization rates
  than nonmovers." [SOURCE: w13229 §B, fn 23]
- They read the result as deterrence: "a general deterrence effect, with both immigrants and
  native-born movers responding to the incentives of new policies toward criminals in similar ways"
  [SOURCE: w13229 §B].
- The 1997 paper has no mover comparison [SOURCE: w6067 OCR, searched for "state of birth",
  "mover", "migrant" and "moved"].

**Corrected sentence 3:** Butcher and Piehl (2007) report that, with only age held fixed, US-born
men living outside their birth state lowered their institutionalization relative to stayers
between 1980 and 2000 (gap 0.04 → 0.3 points). They read this as a shared response to harsher
punishment. With education held fixed, movers are institutionalized more than stayers.

## Part 2: Mexico-born men by years in the US

**Data.**

- 1980, 1990 and 2000 5% census samples (IPUMS USA, extract 4).
- ACS 1-year samples 2006–2024 without 2020 (IPUMS USA, extract 5, with 80 replicate weights).
- US-born reference by single year of age × education for the ACS, from Census API tabulations.

**Definitions.**

- Mexico-born immigrant: birthplace Mexico, excluding men born abroad to US-citizen parents.
- US-born: born in the 50 states or DC.
- Institutional: IPUMS GQ = 3 in the census, which is the same concept as ACS TYPE/TYPEHUGQ = 2.
- Years in US: survey year minus year of immigration. The 1980 and 1990 files report arrival
  intervals, which fit the bins 0–5 / 6–10 / 11–15 exactly (`analyze_census.INTERVAL_BINS`).

**Standard errors.**

- Census: delete-a-group jackknife over 80 household groups. In these files the IPUMS `CLUSTER` is
  the household. Against a Taylor-linearized SE with `STRATA` and `CLUSTER`, the jackknife SE is
  0.89–1.10 times as large [CALCULATION: `census_se_check.py` → `derived/census_se_check.csv`].
- ACS: successive-difference replication with REPWTP1–80. The US-born reference is held fixed; its
  own relative SE is about 1% (2019: 2.66%, SE 0.023 points) [DATA: `derived/acs_movers.csv`,
  reference row].

**Validation.** On the same files the pipeline reproduces Butcher and Piehl's Table 2:

| Group | Ours | Theirs |
|---|---|---|
| US-born | 1.348% / 2.173% / 3.446% | 1.35 / 2.17 / 3.45 |
| All foreign-born | 0.417% / 1.07% / 0.677% | 0.42 / 1.07 / 0.68 |
| Arrivals of 0–5 years, 1980 / 1990 | 0.290% / 0.682% | 0.29 / 0.68 |

[DATA: `derived/census_cohort_rates.csv`]

The ACS IPUMS microdata give the same weighted totals and institutional counts as independent
Census API tabulations in all 54 year × bin cells (largest relative gap 0) [DATA:
`derived/acs_api_crosscheck.csv`].

### 2a. Censuses as published

Mexico-born men 18–40. The last three columns are ratios to US-born men at the same ages
[CALCULATION: `analyze_census.py` → `derived/census_cohort_rates.csv`].

| Years in US | Census (arrived) | Records (institutional) | Rate, % | vs all US-born | vs NH white | vs Mexican-origin |
|---|---|---|---|---|---|---|
| 0–5 | 1980 (1975–80) | 12,032 (78) | 0.65 (0.07) | 0.45 (0.05) | 0.68 (0.08) | 0.29 (0.03) |
| 0–5 | 1990 (1985–90) | 23,104 (165) | 0.97 (0.09) | 0.42 (0.04) | 0.78 (0.08) | 0.27 (0.03) |
| 0–5 | 2000 (1995–2000) | 47,253 (252) | 0.45 (0.03) | 0.13 (0.01) | 0.26 (0.02) | 0.076 (0.006) |
| 6–10 | 1980 (1970–74) | 9,539 (39) | 0.41 (0.06) | 0.30 (0.04) | 0.46 (0.07) | 0.19 (0.03) |
| 6–10 | 1990 (1980–84) | 17,867 (159) | 1.20 (0.12) | 0.50 (0.05) | 0.96 (0.09) | 0.32 (0.03) |
| 6–10 | 2000 (1990–94) | 32,062 (213) | 0.59 (0.04) | 0.16 (0.01) | 0.33 (0.03) | 0.091 (0.007) |
| 11–15 | 1980 (1965–69) | 4,802 (19) | 0.40 (0.08) | 0.31 (0.06) | 0.47 (0.10) | 0.19 (0.04) |
| 11–15 | 1990 (1975–79) | 14,759 (122) | 1.20 (0.13) | 0.54 (0.06) | 1.02 (0.11) | 0.33 (0.04) |
| 11–15 | 2000 (1985–89) | 31,739 (238) | 0.65 (0.05) | 0.19 (0.01) | 0.38 (0.03) | 0.097 (0.007) |
| all | 1980 / 1990 / 2000 | 31,779 / 71,853 / 148,475 | 0.55 / 1.22 / 0.68 | 0.40 / 0.54 / 0.19 | 0.62 / 1.02 / 0.39 | 0.26 / 0.34 / 0.10 |

US-born reference rates for men 18–40 are 1.35%, 2.17% and 3.45%.

**Same cohorts, observed twice.** At fixed years in the US, a cohort difference cannot be told
apart from a period difference. Following one cohort across surveys separates the two [DATA: same
file; ACS rows from `derived/acs_cohort_rates.csv`]:

| Arrived | First observation | Second observation |
|---|---|---|
| 1975–79/80 | 1980, 0–5 years: 0.45 (0.05) | 1990, 11–15 years: 0.54 (0.06) |
| 1985–89/90 | 1990, 0–5 years: 0.42 (0.04) | 2000, 11–15 years: 0.19 (0.01) |
| 1990–94/95 | 2000, 6–10 years: 0.16 (0.01) | ACS 2006, 11–15 years: 0.51 (0.05) |
| 1995/96–2000 | 2000, 0–5 years: 0.13 (0.01) | ACS 2006, 6–10 years: 0.49 (0.04) |

In 2000 the ratio fell by about half or more for every cohort present. Six years later the same
cohorts stood 3–4 times higher in the ACS. Because the same men show both the fall and the
recovery, the 2000 values reflect the period or the instrument, not cohort selection [INFERENCE].

**Naturalized men only.** They cannot be held in immigration detention or deported. Against all
US-born men:

| Years in US | 1980 | 1990 | 2000 |
|---|---|---|---|
| 6–10 | 0.39 (0.12) | 0.45 (0.09) | 0.12 (0.04) |
| 11–15 | 0.41 (0.16) | 0.50 (0.11) | 0.16 (0.03) |
| all | 0.52 | 0.58 | 0.17 |

[DATA: `derived/census_cohort_rates.csv`, group `mexico_born_naturalized`]

The pattern is the same, so detention and deportation do not drive the 1990→2000 fall.
Naturalization is selective, so these levels are not the cohort's own [INFERENCE].

**Correctional institutions only, 1980.** This is the only public census that identifies them.

- 92% of institutionalized Mexico-born men at 0–5 years were in correctional institutions, against
  70% of institutionalized US-born men.
- On the correctional-only outcome, the 1975–80 arrivals stand at 0.57 (0.07) of all US-born men,
  1.02 (0.12) of US-born non-Hispanic white men and 0.32 (0.04) of US-born Mexican-origin men
  [DATA: same file, `outcome = correctional`].
- The 1990 and 2000 files code only "institution", so a correctional-only series cannot be carried
  forward.

**Education held fixed.** Adult arrivals only, meaning men old enough to have arrived at 18 or
older: ages 23–40 at 0–5 years. The ratio is standardized on age × education (fewer than 12 years /
grade 12 / any college) against all US-born men [DATA: `derived/census_cohort_education.csv`]:

| Adult arrivals, 0–5 years | 1980 | 1990 | 2000 |
|---|---|---|---|
| Age × education held | 0.17 (0.02) | 0.15 (0.02) | 0.05 (0.005) |
| Fewer than 12 years of school only | 0.16 | 0.12 | 0.04 |

Part of the fall comes from the native side. US-born men without a diploma became a smaller, more
negatively selected group, and their institutional rate rose from 3.9% to 11.0% [SOURCE: w13229
Table 2]. A ratio to natives at fixed education therefore shrinks even if immigrants do not change
[INFERENCE].

**Arrival-year profile, 2000.** The rate is 0.66% (SE 0.12) in the arrival year, against 0.38–0.44%
at 1–3 years. That is a small bump compared with the ACS spikes in 2d [DATA:
`derived/census_ysm_profile_2000.csv`].

### 2b. Birthplace allocation in the censuses

IPUMS allocation flags (extracts 6 and 14) show that a missing birthplace was filled in very
differently across the three censuses [DATA: `derived/census_allocation.csv`,
`census_allocation_mexorig.csv`].

- **Institutional men classified US-born with an allocated birthplace:** 22% (1980), 28% (1990),
  56% (2000). Among non-institutional US-born men the shares are 4.4%, 5.4% and 10%.
- **1980 and 1990.** The census never allocated Mexico as a birthplace to an institutional man. It
  used "abroad, country unknown" (BPL 900) instead: about 8,600 institutional men in 1980 and
  23,600 in 1990 (weighted), against 3,500 and 18,300 Mexico-born. The standard immigrant
  definition drops this code. Butcher and Piehl drop it too, since our Table 2 match requires the
  drop.
- **Mexican-origin institutional men (Hispanic origin reported as Mexican).** Comparing the
  foreign-born share among those with an allocated birthplace against those with a reported one
  gives 31% vs 16% (1980), 37% vs 32% (1990) and **1.8% vs 38.5% (2000)**. The 2000 census
  allocated a birthplace for 68% of these men (weighted) and made almost all of them native-born.
- **Year of arrival.** It was allocated for 41% of institutional Mexico-born men in 2000 (15% in
  1980, 9% in 1990), against 16% of non-institutional ones.

**Reported-only re-run.** Dropping records with an allocated birthplace or year of arrival, as
Butcher and Piehl's check does, gives these ratios against all US-born men [DATA:
`derived/census_cohort_rates_reported_only.csv`]:

| Years in US | 1980 | 1990 | 2000 |
|---|---|---|---|
| 0–5 | 0.48 (0.06) | 0.51 (0.06) | 0.18 (0.02) |
| 6–10 | 0.34 (0.05) | 0.64 (0.06) | 0.21 (0.02) |
| 11–15 | 0.36 (0.08) | 0.71 (0.08) | 0.28 (0.03) |

This check is biased toward low immigrant rates. Allocation is concentrated among institutional
records, and year of arrival, allocated mostly for institutional immigrants, has no US-born
counterpart [INFERENCE from the shares above].

**Reassignment.** Allocated records are spread within year × race/Hispanic origin × institutional
status, in the nativity mix of records with a reported birthplace [CALCULATION: `analyze_census.py`
`reassignment` → `derived/census_allocation_reassignment.csv`, `census_cohort_reassigned.csv`].
Three variants:

- **country:** only the "abroad, country unknown" records, spread over foreign birthplaces. This
  uses only what the census itself recorded, and it changes 1980 and 1990 only.
- **nativity_high:** also every record allocated to a US state. The exception is 1990
  institutional records whose citizenship answer (which includes "born in the United States") was
  reported: 35% of the 1990 pool, weighted. The 1980 file asks citizenship only of the foreign-born,
  and the 2000 file never flags it for the US-born.
- **nativity_low:** as nativity_high, but only the 1990 share with both items allocated (65%) is
  spread in 1980, in 2000 and among non-institutional records.

Spreading non-institutional records enlarges the Mexico-born denominator, which is the
conservative direction. The multiplier on the ratio to all US-born men is:

| Variant | 1980 | 1990 | 2000 |
|---|---|---|---|
| country | 1.54 | 1.42 | 1.00 |
| nativity_low | 1.63 | 1.57 | 2.06 |
| nativity_high | 1.68 | 1.55 | 2.62 |

The corrected bracket below uses country for 1980/1990 and nativity_low for 2000 as the low end,
and nativity_high for all three years as the high end. The 1980 and 1990 censuses kept foreign
status (as "abroad, country unknown") at or above the reported share, but the 2000 census did not.
That asymmetry justifies the low end.

| Years in US | 1980 | 1990 | 2000 | 2000 vs NH white |
|---|---|---|---|---|
| 0–5 | 0.69–0.75 | 0.59–0.65 | 0.26–0.33 | 0.53–0.66 |
| 6–10 | 0.45–0.50 | 0.71–0.78 | 0.33–0.42 | 0.67–0.84 |
| 11–15 | 0.47–0.52 | 0.77–0.84 | 0.38–0.48 | 0.77–0.96 |
| all | 0.62–0.67 | 0.77–0.84 | 0.39–0.50 | 0.79–0.99 |

These are point sensitivities with no SEs. They assume the reassigned men fall evenly over ages and
years-in-US bins.

What holds under every treatment [INFERENCE]:

- At 0–5 years, the 1985–90 arrivals sit 6–15% below the 1975–80 arrivals (as published: 0.42 vs
  0.45, within one SE).
- At 6–15 years, the cohorts observed in 1990 are 1.6–1.8 times the 1980 ones.
- The 1995–2000 arrivals are the lowest at 0–5 years. The size of that advantage, relative to
  natives, changes by a factor of 2–2.6 depending on the allocation treatment.
- After correction, the gap between the census and the ACS for the same 1990s cohorts shrinks from
  3.2–3.8× to 1.2–1.9×.

### 2b external check: administrative prison counts, 2000

**Administrative counts, quoted.**

- BJS, *Prison and Jail Inmates at Midyear 2002* (NCJ 198877), Table 6, "Number of noncitizens
  held in State or Federal prisons at midyear, 1999-2002": "2000 89,676 36,090 53,586" (total,
  Federal, State) [SOURCE: https://bjs.ojp.gov/content/pub/pdf/pjim02.pdf, p. 5].
- The same bulletin gives jurisdictions only for 2001 and 2002 ("6/30/02 6/30/01"): "California
  19,418 20,616" and "Texas 8,002 7,332"; "*New York reports foreign-born inmates rather than
  noncitizens" [same source].
- BJS, *Immigration Offenders in the Federal Criminal Justice System, 2000* (NCJ 191745): "in 2000,
  37,243 noncitizen inmates were 29% of all Federal prisoners" [SOURCE:
  https://bjs.ojp.gov/content/pub/pdf/iofcjs00.pdf, p. 7].
- BJS, *Profile of Jail Inmates, 2002* (NCJ 201932): "An estimated 8% of jail inmates were not
  U.S. citizens, unchanged from 1996"; its table row reads "Noncitizen 7.8" (2002) and "7.4" (1996)
  [SOURCE: https://bjs.ojp.gov/content/pub/pdf/pji02.pdf, p. 2].
- BJS, *Prison and Jail Inmates at Midyear 2000* (NCJ 185989), on June 30, 2000: "were held in
  local jails (621,149)" [SOURCE: https://bjs.ojp.gov/content/pub/pdf/pjim00.pdf, p. 1].

All PDFs were parsed with `pdftotext -layout` into `_cache/admin/`. From these, noncitizens in
jails at midyear 2000 were about 7.4–7.8% × 621,149 = 46,000–48,400 [CALCULATION]. INS average
daily detention in FY2000 was 19,458 (2c), part of it held inside jails.

Not pinned: BOP inmates who were Mexican citizens in 2000, the California Department of
Corrections' foreign-born or Mexican-national counts, INS detention by nationality, and a primary
SCAAP count for FY2000.

**Census counts.** Every institutional person in the 2000 5% sample, all ages and both sexes
(IPUMS extract 15). Noncitizen means foreign-born with CITIZEN 3. The reassignment is run within
state group (CA, TX, rest) × sex × race/Hispanic origin. nativity_low spreads 65.2% of the
allocated-to-US pool, the 1990 share with citizenship also allocated; nativity_high spreads all of
it [CALCULATION: `admin_check.py` → `derived/admin_check_2000.csv`].

| Scope | Administrative floor | Census as published | nativity_low | nativity_high |
|---|---|---|---|---|
| US, all noncitizens | prisons 89,676; with jails about 136,000–138,000; with INS at most about 158,000 | 73,395 | 126,084 | 154,214 |
| US, Mexico-born noncitizens | not pinned | 26,538 | 52,480 | 66,329 |
| US, noncitizen men 18–64 | — | 56,687 | 101,694 | 125,722 |
| California, all noncitizens | state prisons alone 20,616 (mid-2001) | 13,897 | 30,399 | 39,209 |
| Texas, all noncitizens | state prisons alone 7,332 (mid-2001) | 9,002 | 21,574 | 28,286 |

The census allocated a birthplace for 52% of all institutional persons in 2000: 64% in
California, 70% in Texas [DATA: same file]. No federal proxy is defensible, because the public file
does not identify federal facilities.

**Verdict of the check** [INFERENCE from the table].

- **The published 2000 count fails the prison floor.** The census found 73,395 institutionalized
  noncitizens across prisons, jails, INS detention and every other institution. That is 18% fewer
  than BJS counted in state and federal prisons alone three months later (89,676), and about half
  of prisons plus jails.
- **California fails too.** Its published count (13,897) is 33% below the noncitizens in its state
  prisons alone a year later (20,616). Timing is not the explanation, because the national state
  count barely moved from mid-2000 to mid-2001 (53,586 → 54,031).
- **The counts favour nativity_high.** Prisons plus jails alone (about 136,000–138,000) exceed
  nativity_low (126,084). nativity_high (154,214) lands in the prisons + jails + INS range.
- **The discrimination is weak.** The jail share is self-reported and dates from 1996 and 2002. New
  York reports foreign-born inmates, which overstates the prison count. The census may miss inmates
  altogether. Some INS detainees are inside the jail count.
- **Texas cannot discriminate.** Its only admin figure covers state prisons, and the published count
  already exceeds it.
- **What the check establishes.** The allocation made most foreign-born inmates native-born, and at
  least the nativity_low correction is needed to reach the administrative totals.

**Rumbaut et al. (2006), Table 1.** Men 18–39, Hispanic origin Mexican (HISPAN 1), US-born
(birthplace in the US) against foreign-born, institutional share [CALCULATION: `admin_check.py` →
`derived/rumbaut_2000.csv`].

| Treatment | Foreign-born Mexican | US-born Mexican | US-born ÷ foreign-born |
|---|---|---|---|
| Rumbaut et al. 2006, Table 1 (correctional institutions) | 0.70% | 5.90% | 8.4 |
| IPUMS, as published (all institutions) | 0.62% | 6.05% | 9.8 |
| nativity_low | 1.28% | 5.19% | 4.0 |
| nativity_high | 1.62% | 4.68% | 2.9 |

Rumbaut's figures inherit the bias: they come from the same 2000 5% file, and our as-published
replication is close to them.

- **Rescaled Table 1.** Scaling his two cells by our factors gives 1.45–1.84% for foreign-born
  Mexican men, 4.57–5.06% for US-born Mexican men, and a ratio of 2.5–3.5 instead of 8.4
  [CALCULATION].
- **The memo's headline.** The US-born non-Hispanic white rate barely moves under reassignment
  (factor 0.994–0.996 for men 18–40) [DATA: `derived/census_allocation_reassignment.csv`, column
  `rate_scale_us_nhw`]. The memo's "US-born Mexican-origin men 3.45× native whites" therefore
  becomes about 2.7–3.0× [CALCULATION: 3.45 × 0.775–0.858 / 0.994–0.996].
- **The memo's 2000–2010 comparison.** It reads the jump from 0.70% (2000) to 2.34% (2010 ACS) for
  foreign-born Mexican men as ICE detention. Part of that jump is this allocation instead.

### 2c. Immigration detention: a bound, not a subtraction

The lane rule forbids subtracting an ICE count from a survey estimate. The bound below is the
average daily detention population (all nationalities) times Mexico's share of detention book-ins.
Mexicans have shorter stays (CRS RL32369), so this bound overstates [CALCULATION: `ice_bound.py`
→ `derived/ice_bound.csv`; sources per row in the file].

| Year | ADP, all nationalities | Mexico share of book-ins | Bound on Mexican stock | Mexico-born institutional men 18–40, 0–5 yrs / all | Bound ÷ 0–5 cell / ÷ all |
|---|---|---|---|---|---|
| 1980 | 1,620 | not pinned | — | 1,560 / 3,500 | — |
| 1990 | 6,571 | not pinned | — | 4,564 / 18,267 | — |
| 2000 | 19,458 | not pinned | — | 4,580 / 21,269 | — |
| 2010 | 30,885 | 60.6% | 18,716 | 24,019 / 76,956 | 0.78 / 0.24 |
| 2011 | 33,330 | 67.2% | 22,398 | 17,727 / 87,238 | 1.26 / 0.26 |
| 2012 | 34,260 | 64.4% | 22,063 | 16,220 / 76,669 | 1.36 / 0.29 |
| 2019 | 50,165 | 24% | 12,040 | 10,306 / 39,919 | 1.17 / 0.30 |
| 2024 | 37,722 | 25.0% | 9,415 | 8,518 / 34,910 | 1.11 / 0.27 |

Detention can at most be about a quarter to 30% of all institutionalized Mexico-born men 18–40 in
these ACS years. It could be all of the recent-arrival cell. In 1980 and 1990 the INS daily
population of all nationalities is as large as the Mexico-born 0–5-year cell, so the 1980 and 1990
recent-arrival ratios may also contain detention. If they do, the 1975–80 arrivals were better than
measured, which weakens the case for improvement in the 1980s further [INFERENCE].

The FY2023 ADP is not pinned. Its share row (about 20%) is in the CSV without a bound.

### 2d. ACS 2006–2024

Pooled periods (per-year rows in `derived/acs_cohort_rates.csv`). Ratios to US-born men at the same
ages, replicate-weight SEs [CALCULATION: `analyze_acs.py` → `derived/acs_cohort_pooled.csv`]:

| Years in US | Measure | 2006–10 | 2011–15 | 2016–19 | 2021–24 |
|---|---|---|---|---|---|
| 0–5 | rate, % | 2.26 | 3.83 | 3.52 | 1.86 |
| 0–5 | vs all US-born | 0.72 (0.026) | 1.24 (0.055) | 1.23 (0.065) | 0.84 (0.054) |
| 0–5 | vs NH white | 1.41 (0.05) | 2.38 (0.11) | 2.23 (0.12) | 1.57 (0.10) |
| 3–5 | vs all US-born | 0.58 (0.032) | 0.84 (0.054) | 0.72 (0.054) | 0.64 (0.060) |
| 6–10 | rate, % | 1.77 | 1.87 | 1.81 | 1.72 |
| 6–10 | vs all US-born | 0.53 (0.016) | 0.58 (0.029) | 0.61 (0.047) | 0.72 (0.062) |
| 6–10 | vs NH white | 1.05 (0.03) | 1.11 (0.06) | 1.09 (0.08) | 1.32 (0.11) |
| 6–10 | vs Mexican-origin | 0.38 (0.011) | 0.44 (0.022) | 0.51 (0.039) | 0.71 (0.061) |
| 11–15 | rate, % | 1.91 | 1.70 | 1.59 | 1.84 |
| 11–15 | vs all US-born | 0.58 (0.023) | 0.52 (0.023) | 0.53 (0.028) | 0.73 (0.043) |
| 11–15 | vs NH white | 1.14 (0.05) | 1.00 (0.04) | 0.94 (0.05) | 1.31 (0.08) |
| all | vs all US-born | 0.66 (0.011) | 0.73 (0.015) | 0.66 (0.015) | 0.68 (0.017) |

US-born men 18–40: 3.09%, 3.03%, 2.75% and 2.19% [DATA: same file]. The row 3–5 drops the arrival
year and the next two years.

**Immigration custody dominates the first years.** The rate in the arrival year is 5.1%
(2006–10), 9.8% (2011–15), 8.5% (2016–19) and 4.1% (2021–24), against 1.0–2.7% from the third year
on [DATA: `derived/acs_ysm_profile.csv`]. The 0–5 cells therefore do not measure crime selection.
The 2000 census has no such spike (2a).

**Reading at 6–15 years** [INFERENCE]. Successive arrival cohorts at 6–10 years are 1996–2004,
2001–09, 2006–13 and 2011–18. Their levels are flat (1.72–1.87%), while the native rate fell, so the
ratio rises from 0.53 to 0.61 across 2006–2019 (and to 0.72 in 2021–24). At 11–15 years the ratio
is flat at 0.52–0.58 through 2019. Nothing here shows later cohorts more positively selected.

**Education held fixed.** Adult arrivals, age × education, against all US-born men [DATA:
`derived/acs_cohort_education.csv`]:

| Years in US | 2006–10 | 2011–15 | 2016–19 | 2021–24 |
|---|---|---|---|---|
| 0–5 | 0.25 (0.010) | 0.44 (0.022) | 0.46 (0.024) | 0.27 (0.017) |
| 6–10 | 0.16 (0.008) | 0.19 (0.015) | 0.19 (0.023) | 0.20 (0.025) |
| 11–15 | 0.17 (0.012) | 0.16 (0.012) | 0.16 (0.014) | 0.16 (0.018) |

At 6–15 years the ratio is flat across four periods.

**By citizenship, at 6–10 years** [DATA: `derived/acs_cohort_pooled_by_citizenship.csv`]:

| Group | 2006–10 | 2011–15 | 2016–19 | 2021–24 |
|---|---|---|---|---|
| Naturalized | 0.24 (0.04) | 0.28 (0.07) | 0.14 (0.05) | 0.21 (0.08) |
| Noncitizens | 0.55 (0.02) | 0.60 (0.03) | 0.67 (0.05) | 0.81 (0.07) |

**Allocation in the ACS** [DATA: `derived/acs_allocation.csv`, Census API tabulations by allocation
flag].

- Birthplace imputation is small on both sides: 4–9% of US-born institutional men in 2006–19 and
  11–13% in 2021–24. Dropping birthplace-imputed records on both sides changes the crude ratios by
  −8% to +4% (2006–19) and −12% to +7% (2021–24).
- Year of entry was imputed for 2–39% of institutional Mexico-born men in the 0–15-year bins in
  2006–19, 41–82% in 2021–23 and 28–42% in 2024.
- Placement in years-in-US bins therefore rests mostly on imputation in 2021–23, and the rise in
  the 2021–24 bin ratios should not be read as a cohort change [INFERENCE].

**Census and ACS do not splice.** For the same 1990s arrivals, the published 2000 census puts the
ratio at 0.13–0.16 and the ACS 2006 at 0.49–0.51. After the 2b correction, the 2000 values are
0.26–0.42. Cohorts after 2000 are ranked only within the ACS.

## Part 3: interstate movers

US-born men 18–40 living outside their state of birth (movers) against those living in it
(stayers). The gap is in percentage points of the institutional share: movers minus stayers, with
stayers' rates applied at movers' ages, or at ages × education.

### 3a. Censuses: Butcher and Piehl's comparison, re-run

[CALCULATION: `analyze_census.py` → `derived/census_movers.csv`]

| Census | Group | Movers % | Stayers % | Gap, age held | Gap, age × education held |
|---|---|---|---|---|---|
| 1980 | all US-born | 1.29 | 1.38 | −0.05 (0.02) | +0.16 (0.02) |
| 1990 | all US-born | 2.02 | 2.26 | −0.22 (0.03) | +0.17 (0.03) |
| 2000 | all US-born | 3.18 | 3.58 | −0.43 (0.04) | +0.28 (0.04) |
| 1980 / 1990 / 2000 | NH white | 0.85 / 1.19 / 1.69 | 0.89 / 1.15 / 1.69 | −0.02 / +0.04 / −0.02 | +0.12 / +0.23 / +0.29 |
| 1980 / 1990 / 2000 | NH Black | 4.12 / 7.59 / 11.25 | 4.62 / 8.15 / 11.58 | −0.35 / −0.54 / −0.51 | +0.14 / +0.54 / +1.52 |
| 1980 / 1990 / 2000 | Hispanic | 2.06 / 3.82 / 7.21 | 2.12 / 4.01 / 6.36 | −0.03 / −0.18 / +0.67 | +0.07 / +0.23 / +1.16 |

This reproduces the paper's age-only numbers (−0.04, −0.2, −0.3) and its footnote.

- Within NH white men the age-only gap is zero in all three censuses.
- The all-US-born advantage of movers is mostly composition: NH white men are the most mobile group
  (mover share 36% in 2000, against 29% for NH Black and 26% for Hispanic men).
- With education held fixed, movers are institutionalized more than stayers in every year and group.

### 3b. ACS 2019, 2023, 2024

IPUMS extract 9 [CALCULATION: `analyze_movers.py` → `derived/acs_movers.csv`].

| Year | Group | Movers % | Stayers % | Gap, age held | Gap, age × education held |
|---|---|---|---|---|---|
| 2019 | all US-born | 2.34 | 2.80 | −0.62 (0.05) | −0.06 (0.04) |
| 2023 | all US-born | 1.79 | 2.24 | −0.61 (0.04) | −0.09 (0.04) |
| 2024 | all US-born | 1.78 | 2.13 | −0.54 (0.04) | −0.08 (0.04) |
| 2019 | NH white | 1.40 | 1.56 | −0.26 (0.05) | +0.07 (0.04) |
| 2023 | NH white | 1.01 | 1.22 | −0.31 (0.04) | −0.01 (0.04) |
| 2024 | NH white | 0.98 | 1.13 | −0.25 (0.04) | +0.01 (0.04) |
| 2019 | NH Black | 6.74 | 7.91 | −1.44 (0.25) | +0.14 (0.27) |
| 2023 | NH Black | 5.95 | 6.80 | −1.22 (0.21) | +0.06 (0.19) |
| 2024 | NH Black | 5.52 | 6.76 | −1.72 (0.23) | −0.39 (0.21) |
| 2019 | Hispanic | 3.25 | 2.88 | +0.13 (0.15) | +0.19 (0.15) |
| 2023 | Hispanic | 2.17 | 2.22 | −0.24 (0.10) | −0.02 (0.10) |
| 2024 | Hispanic | 2.32 | 2.07 | +0.01 (0.11) | +0.16 (0.12) |

- **Age held.** White and Black movers are institutionalized less than stayers; Hispanic movers are
  not.
- **Age × education held.** The gaps shrink to between −0.39 and +0.19. Only one of twelve (all
  US-born, 2023: −0.09, SE 0.04) is more than two SEs from zero.
- As measured, the movers' advantage is their schooling [INFERENCE].

**Placement bias works against movers.** Prisoners are counted where they are held, so a stayer
held in another state counts as a mover. Moving a share f of stayers' institutional count back
gives these all-US-born gaps [CALCULATION: `placement_f04/08` columns]:

| Year | Age held, f = 0 / 0.04 / 0.08 | Age × education held, f = 0 / 0.04 / 0.08 |
|---|---|---|
| 2019 | −0.62 / −1.01 / −1.42 | −0.06 / −0.42 / −0.81 |
| 2023 | −0.61 / −0.91 / −1.23 | −0.09 / −0.37 / −0.67 |
| 2024 | −0.54 / −0.83 / −1.14 | −0.08 / −0.34 / −0.64 |

The value of f is illustrative. Federal prisoners were roughly 7% of the incarcerated in 2019,
and only some of them are held outside their birth state [UNVERIFIED: not pinned in this lane]. So
public data do not identify the education-held sign. As measured it is zero, and a placement share
of a few percent turns it into a mover advantage of 0.3–0.4 points (NH white −0.11 to −0.15 at
f = 0.04) [INFERENCE].

SEs in 3b are the household jackknife, because the replicate-weight version of this extract
(153 MB) was not downloaded. On the Mexico-born ACS file, the jackknife SE is 0.70–1.28 times the
replicate-weight SE, mostly below 1 after 2011, so these SEs may be understated by up to 30%
[DATA: `derived/acs_se_calibration.csv`].

## Every specification computed

- **Census cohorts** (`census_cohort_rates.csv`):
  - groups: Mexico-born, naturalized, noncitizen, and all foreign-born;
  - bins: 0–5, 6–10, 11–15, 16+ and all;
  - references: all US-born, NH white, Mexican-origin;
  - ratios: age-standardized and crude;
  - outcome: institutional in every census, plus correctional in 1980.
- **Census education** (`census_cohort_education.csv`): adult arrivals by education (all, <12,
  grade 12, college, grade 12+), age-held and age × education-held, against the three references.
- **Census allocation** (`census_allocation.csv`, `census_cohort_rates_reported_only.csv`,
  `census_allocation_mexorig.csv`, `census_allocation_reassignment.csv`,
  `census_cohort_reassigned.csv`): four treatments (as published, reported-only, country,
  nativity_low/high) against three references.
- **Census checks:** SE check (`census_se_check.csv`) and 2000 single-year profile
  (`census_ysm_profile_2000.csv`).
- **ACS cohorts:** per year 2006–2024 without 2020 (`acs_cohort_rates.csv`) and pooled in four
  periods (`acs_cohort_pooled.csv`), for bins 0–5, 3–5, 6–10, 11–15, 16+ and all, against the three
  references.
- **ACS subgroups and profiles:** by citizenship (`acs_cohort_pooled_by_citizenship.csv`), single
  years 0–16 (`acs_ysm_profile.csv`) and education (`acs_cohort_education.csv`).
- **ACS checks:** allocation (`acs_allocation.csv`), SE calibration (`acs_se_calibration.csv`) and
  IPUMS-vs-API totals (`acs_api_crosscheck.csv`).
- **Movers:** census 1980/1990/2000 and ACS 2019/2023/2024; four groups; crude, age-held and age ×
  education-held gaps; census ratios; ACS placement sensitivity at f = 0.04 and 0.08
  (`census_movers.csv`, `acs_movers.csv`).
- **Detention bound** (`ice_bound.csv`).
- **2000 external check:** noncitizen and Mexico-born noncitizen institutional counts for the US,
  CA and TX under three treatments (`admin_check_2000.csv`), and Rumbaut's Table 1 cells
  (`rumbaut_2000.csv`).

Results unfavourable to the immigrant-selection reading, all reported above:

- ACS arrivals of 0–5 years at 1.2–2.4 times the rate of US-born men (2011–19);
- the 1990 census cohorts worse than the 1980 ones;
- ACS ratios at 6–10 years rising across cohorts;
- noncitizens at 0.81 of US-born men in 2021–24.

## Limits

- **Custody, not crime.** Institutions include psychiatric and long-term care. In the 1980 file,
  92% of institutionalized recent Mexican arrivals and 70% of institutionalized US-born men were in
  correctional institutions.
- **Deportation removes offenders from later observations.** The naturalized-only rows are immune
  to deportation, but naturalization selects its own members.
- **Undercount.** Unauthorized men and inmates may be missed at different rates in different years.
  No correction is attempted.
- **Birthplace allocation.** This dominates the census comparison (2b). The corrected ratios rest on
  missingness being unrelated to birthplace within race/Hispanic origin × institutional status.
  1980/1990 evidence says foreign-born men were at least as likely to be missing.
- **Year of arrival.** In the 2021–23 ACS it is mostly imputed for institutional men.
- **Detention.** The ACS 0–5-year cells may be entirely immigration custody (2c). The census years
  have no Mexico share to bound them.
- **The 2000 census and the 2006 ACS do not splice** (2d).
- **Composition.** Age is held in every ratio and education in the adult-arrival tables. Region of
  origin within Mexico, legal status and region of residence are not held.
- **Movers.** Placement bias leaves the education-held sign unidentified (3b).

## Did not complete

- **ACS replicate-weight extracts** `acs_movers` (153 MB) and `acs_us` (128 MB) were submitted but
  not downloaded, so the mover SEs use the household jackknife. The ACS age × education reference
  comes from Census API tabulations with the main weight, held fixed across replicates.
- **1998 *JPAM* paper** (Butcher and Piehl, cross-city crime) not read.
- **2000 admin counts by origin.** BOP Mexican-citizen inmates, California Department of
  Corrections counts and a primary FY2000 SCAAP count were not pinned (2b external check).
- **Detention inputs.** FY2023 ICE average daily population not pinned, and no Mexico share for INS
  detention in 1980–2000. The 7% federal-prisoner share in 3b is [UNVERIFIED].
- **ACS reported-only ratios** are crude, not age-standardized.
- **Corrected census ratios** (2b) have no SEs.

## For the parent to check

1. **2b is the new, load-bearing result.** The external check (2b external check) rejects the
   published 2000 count and favours nativity_high. It uses noncitizens of all origins; a
   Mexican-citizen count for BOP or California around 2000 would test the Mexico-born piece
   directly.
2. **The chat sentences need correcting.** Sentence 2 should read "for all immigrants, as a gap in
   percentage points; on a ratio scale the 1980s arrivals were worse". Sentence 3 should be replaced
   by the corrected sentence in Part 1.
3. **Existing repo memos.** Any that cite Butcher and Piehl's 2000-census result for Mexicans, or a
   2000-census immigrant institutionalization rate, inherit the 2b allocation problem.

## Reproduce

From the repository root. Microdata stay in `_cache/`, which is ignored (`.gitignore`).

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # IPUMS and Census keys, never printed
L=infra/immigration-fiscal/crime_selection_cohorts_2026_09_23
X="census census_q census_inst_q census2000_inst acs_mex acs_movers_lite"
uv run --no-project python3 $L/ipums_extract.py submit $X
uv run --no-project python3 $L/ipums_extract.py wait $X --max-minutes 45
uv run --no-project python3 $L/ipums_extract.py download $X
uv run --no-project python3 $L/acs_tabulate.py 2>&1 | sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'
uv run --no-project python3 $L/acs_reference.py 2>&1 | sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/analyze_census.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/census_se_check.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/analyze_acs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/analyze_movers.py
uv run --no-project python3 $L/ice_bound.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/admin_check.py
```

Extract checksums (sha256, first 16 hex characters) are in `_cache/ipums/extracts.json`: census
af06286eb3753abc, census_q f77d405ca2601f93, census_inst_q 0824a2c7d867c17a, census2000_inst 76389afaabfbafaa, acs_mex
94c4ebc486dd2aee, acs_movers_lite 74d2e80c73722570. A new IPUMS extract of the same definition
can differ in row order; the tables should not.
