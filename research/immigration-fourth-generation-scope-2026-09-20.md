# Fourth-generation scope: evidence index

Date: 2026-09-20. [MEASUREMENT / ACCOUNTING] Extended with an executed partial generation split; no change to the total population or fiscal account.

Follow-up: [aggregate later-generation estimates](immigration-later-generation-estimates-2026-09-20.md)
now execute the age-adjusted GSS model, historical checks and PSID access audit.
The observed classification counts below are unchanged.

**Finding:** The current 40.896574m Mexican-origin annual-account population already includes identifying fourth and later generations within G3+. Parent linkage separates 2.870m as observed G3 and 2.073m as observed G4+, leaving 9.399m unresolved within G3+. These are identified portions, not complete generation totals. Exact G4 versus G5+ remains unmeasured. Adding G4+ again would double-count residents already in the account.

## Current executable definition

The classifier defines `mexican_third_plus_selfid` using native birth, two parents born in US areas, and Mexican identification. It applies no grandparent cutoff. The current account combines this group with Mexico-born residents and the US-born second generation, restricting to civilian-household residents. Identifying G4+ residents therefore already contribute both receipts and spending. [SOURCE: [classifier](../infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py), group masks; [current receipt builder](../infra/immigration-fiscal/full_account_receipts_2026_09_20/builder.py), `derive_keys`; [current account](immigration-complete-annual-account-2026-09-20.md), population definition.]

## What a later-generation comparison can establish

[SOURCE A2: [Duncan, Grogger, Leon and Trejo, IZA DP12704](https://docs.iza.org/dp12704.pdf), sections 2–3 and 5–6, Tables 13 and 16.] Their NLSY97 analysis separates G3 using Mexican-born grandparents, while G4+ still depends on respondent or parental Mexican identification. It finds progress hidden by pooling G3 and G4+. Selective loss of ethnic identification can bias later-generation attainment downward; it does not establish that every persistent gap is an artifact. The adult nonidentifier sample is small, and measured geographic/family controls do not eliminate the observed G3/G4+ education gap.

[MEASUREMENT] Exact G4 requires a Mexican-born great-grandparent and the relevant nearer-generation birth histories. Native-born grandparents alone identify a possible G4+ category, not exact G4. Public CPS adult records lack the required history. Our public NLSY97 reconstruction also lacks the detailed grandparent-origin fields needed for an exact Mexican lineage classification. Unknown ancestry stays unknown. [SOURCE: [parent linkage](immigration-nlsy97-parent-linkage-2026-09-17.md); [conclusion audit](immigration-new-conclusions-audit-2026-09-17.md), family-history measurement.]

[SOURCE B2: [Pew ancestry-screen methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).] An ancestry screen including people who no longer identify as Hispanic helps test selection. This pan-Hispanic survey is not a Mexican G4 fiscal dataset.

## Executed separation in the current population

[MEASUREMENT: [generator, inputs and checks](../infra/immigration-fiscal/generation_split_2026_09_20/README.md).] CPS ASEC2025, civilian-household persons of all ages, existing Mexican-origin union; survey-weighted people in millions. G1/G2 use birthplace, G3+ additionally requires Mexican identification. This is a person-count ledger, not dollars, an immigration-policy effect, or a low-education-only sample.

| Category | All ages, millions | Under18 | Adults18+ | All-age sample n |
|---|---:|---:|---:|---:|
| G1: Mexico-born foreign-born | 12.221 | 0.546 | 11.675 | 5,631 |
| G2: native, Mexico-born parent | 14.333 | 5.418 | 8.915 | 6,349 |
| G3: Mexican grandparent observed | 2.870 | 2.321 | 0.549 | 1,165 |
| G4+: all four grandparents US-area-born | 2.073 | 1.634 | 0.440 | 878 |
| G3+ with unresolved grandparent history | 9.399 | 2.204 | 7.195 | 4,308 |
| **Existing total** | **40.897** | **12.123** | **28.774** | **18,331** |

The last three categories sum to the existing **14.343m G3+**. Grandparent
birthplaces come from co-resident biological parents' own parental-birthplace
reports. A known Mexican grandparent establishes G3; G4+ requires four explicitly
native grandparents. Missing branches, inconsistent linked parent records and
other unresolved histories remain unresolved. CPS may use a household proxy
respondent and edited/imputed fields; "observed" refers to released reports.

**65.53% of all G3+ and 87.92% of adult G3+ remain unresolved**; under18 the
unresolved share is 35.78%. The co-resident subset cannot supply the missing adults'
generation shares or fiscal profiles. All-age sampling SEs are 0.144m for observed
G3 and 0.111m for observed G4+; these exclude classification/coverage error.
Withholding classifications dependent on changed/imputed fields leaves 2.808m G3,
1.994m G4+ and 9.540m unresolved. This sensitivity does not alter the population
denominator or infer values for excluded histories. [SOURCE: generated
`cps_generation_split.csv`; [Census documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf).]

## Independent historical adult split

[MEASUREMENT / CALIBRATED SENSITIVITY: same reproduction directory, historical
outputs.] Weighted percentages **within each stated Mexican-origin adult sample**;
unknown generations retained. These are not alternative estimates of today's
all-age distribution.

| Sample | G1 | G2 | G3 | G4+ | Unresolved | n |
|---|---:|---:|---:|---:|---:|---:|
| Pew2015 Hispanic identifiers reporting Mexican origin | 54.21% | 26.80% | 10.26% | 5.61% | 3.12% | 831 |
| Pew2015–16 including nonidentifiers, historical calibration | 52.73% | 26.28% | 10.60% | 6.88% | 3.51% | 883 |
| NLSY97 Mexican/Chicano identifiers, retained1980–84 birth cohort | 9.18% | 32.98% | 13.92% | 16.76% | 27.17% | 676 |

Pew's pooled row normalizes the complete 1500/401 source surveys before applying
the historical 37.8/4.9m benchmarks and selecting Mexican origin. Only 52
nonidentifiers report narrow Mexican origin; 26 are G4+. Mixed-heritage answers
do not preserve component origins and are excluded. The released grandparent
fields identify foreign/US birth, not Mexico specifically; Puerto Rico counts
as migrant origin in this survey convention. The count-ratio calibration is a
sensitivity to rounded historical benchmarks, not fresh ancestry prevalence.
The NLSY row uses round 21 weights and excludes later immigrants to the cohort.
No design-based confidence interval or national fiscal extrapolation is claimed.
[SOURCE: [Pew methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/);
[NLSY linkage audit](immigration-nlsy97-parent-linkage-2026-09-17.md).]

## Can additional data resolve the missing histories?

**Partially.** The executed annual CPS linkage has low yield; GSS adds an
independent adult benchmark with substantially less missing grandparent history.
Neither check assigns the full 9.399m residual or separates exact G4 from G5+.
[MEASUREMENT: [reproduction and input locks](../infra/immigration-fiscal/generation_split_2026_09_20/README.md#additional-recovery-checks).]

### Why the current CPS records are unresolved

| Mutually exclusive reason | People, millions |
|---|---:|
| No co-resident biological parent linked | 6.655 |
| One linked biological parent; insufficient grandparent history | 2.054 |
| Linked parent's birthplace contradicts reported native parentage | 0.519 |
| Two linked parents; non-Mexico foreign grandparents prevent strict all-US G4+ | 0.171 |
| **Total unresolved** | **9.399** |

[MEASUREMENT] The first two rows explain 92.66% of the residual. Most missingness
is absent parental branches, not a missing surname-origin label. The last row
also exposes a definition issue: a Mexican identifier can have a foreign-born
grandparent from another country. That is generic immigrant G3, without proving
Mexican-lineage G3. The current Mexican-specific classifier is not silently
replaced with the generic convention.

Joining the held 2024 and 2026 ASEC waves on person IDs, retaining the 2025 target
weights and checking stable demographics and family histories, produces
**25,049–32,365 candidate people** (12–15 records), **0.27%–0.34%** of the residual.
The range reflects the rule for comparing currently observed parent branches,
not a confidence interval. No candidate classifications have been applied:
edited-field adjudication is incomplete. Complementary branches across waves
and all eight monthly CPS interviews remain untested; this annual check does
not bound their yield. CPS does not follow movers to their new addresses.
[SOURCE: generated recovery CSVs;
[Census ASEC matching documentation, chapter3](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf);
[Census Technical Paper63, longitudinal matching](https://www2.census.gov/programs-surveys/cps/methodology/tp63rv.pdf).]

### GSS supplies a useful adult benchmark

[MEASUREMENT] GSS Mexican/Mexican-American/Chicano identifiers, US-born with
both parents US-born, all adult education levels. Percentages are within that
subgroup, including unknown grandparents. The recent 2016–2024 window provides
more observations; 2021–2024 tests sensitivity to the older observations. These
are pooled repeated cross-sections, weighted by NORC's recommended WTSSNRPS,
not a 2025 population allocation or equal-year average.

| GSS window | Generic G3 | G4+ | Unknown grandparents | Sample n |
|---|---:|---:|---:|---:|
| 2016–2024 | 48.25% | 40.19% | 11.55% | 383 |
| 2021–2024 | 48.83% | 36.93% | 14.24% | 252 |

`GRANBORN` counts foreign-born grandparents; it does not give their countries.
G4+ here means four US-born grandparents among Mexican identifiers. It does not
prove a Mexican-born great-grandparent. The WTSSPS sensitivity gives G4+ shares
40.61% and 37.32%, respectively. Unknown grandparents cannot simply be dropped;
doing so would raise the headline share. The code retains them and age-missing
records. Age cells are small, no design-based interval is fitted, and survey
mode/nonresponse differences remain. [SOURCE:
[NORC data](https://gss.norc.org/get-the-data.html), held cumulative R3a source;
2024 R3a codebook p.40 for weights;
[primary grandparent question](https://sda.berkeley.edu/sdaweb/docs/gss21rel3/DOC/hcbk0032.htm).]

[INFERENCE] This supports a meaningful aggregate estimation route, not the
calculation `40.19% × 9.399m`. A further model needs age/cohort and sampling-frame
alignment, survey-design uncertainty, sensitivity to unknown grandparents and
identity selection, and validation against independently observed family history.
Estimating population shares is easier than identifying generation-specific
fiscal profiles: an aggregate share alone does not identify how taxes or benefits
are distributed within the missing group. Using income to predict generation
and then treating the inferred income gap as independently observed evidence
would overstate what the data establish.

### Names, panels and administrative records

| Route | What it can establish | Remaining requirement |
|---|---|---|
| Surname plus location, such as BISG | Probabilities of broad racial/ethnic identification | No validated G3/G4+ target; public CPS has no names |
| Original Latino National Survey2006, ICPSR20862 DS0001 | Larger historical adult sample with parent/grandparent questions | Acquire full original file; held documentation/replication subsets lack the full joint fields; limited geography and old cohort composition |
| PSID Family Identification Mapping System | Actual links to some biological parents, grandparents and great-grandparents | Audit Mexican sample size and birthplace completeness; panel generations are not immigration generations |
| Restricted Census survey/administrative linkages | Parent-child graphs linked to birthplace records | Approved access plus coverage audit; Hispanic and lower-income linkage gaps are documented |
| Purpose-built ancestry survey | Direct respondent, parent, grandparent and great-grandparent birthplace reports | Representative recruitment including people who no longer identify as Mexican; preserve don't-know answers |

[SOURCE: [CFPB BISG methodology](https://files.consumerfinance.gov/f/201409_cfpb_report_proxy-methodology.pdf);
[Census surname tables](https://www.census.gov/data/developers/data-sets/surnames.html);
[LNS2006](https://www.icpsr.umich.edu/web/ICPSR/studies/20862), held DS0001 codebook pp.32–33;
[PSID mapping manual](https://simba.isr.umich.edu/FIMS/FIMS_UG.pdf), pp.3–4,8,12–13;
[Census linkage example](https://www2.census.gov/ces/wp/2020/CES-WP-20-36.pdf), parent-child links and Numident birthplace;
[Census linkage coverage audit](https://www2.census.gov/ces/wp/2024/CES-WP-24-18.pdf);
[restricted access route](https://www.census.gov/programs-surveys/dcdl/accessing-linked-data.html).]

[INFERENCE] Names could assist aggregate identity-attrition sensitivity if
validated against actual ancestry; they do not record which ancestor immigrated.
Marriage can remove or introduce a surname, and the same surname can span many
generations and origin countries. High Hispanic-classification accuracy would
therefore not validate a generation classifier. Direct family histories are the
relevant target. PSID's 1990 Latino oversample ended in 1995, so its existence
does not guarantee a large continuously followed Mexican sample.
[SOURCE: [Duncan–Trejo, surname and attrition discussion](https://fraser.stlouisfed.org/files/docs/historical/frbatl/events/frbatl_2010hei_duncan.pdf);
[PSID FAQ](https://psidonline.isr.umich.edu/guide/faq.aspx).]

**Next useful work:** design-aware, age-aligned GSS/Pew/NLSY aggregate estimates,
then a PSID ancestry-completeness audit if exact G4/G5 still changes the research
question. These are feasible next steps, not completed national imputations.
More precise labels alone do not change the existing fiscal total.

**Follow-up, 2026-09-20:** The aggregate estimation step is now
[executed](immigration-later-generation-estimates-2026-09-20.md). PSID field and
access checks are complete; its joint pedigree count still requires the data.

## Is G5+ a rounding error?

**Not established.** The strongest version of the recent-wave argument is that
recent arrivals and their children occupy a large share of the population;
the current G1/G2 count above supports that. It does not identify how the
remaining population divides between exact generations. [INFERENCE]

Disconfirming evidence for treating *all older generations* as negligible:
Duncan–Trejo's 1994–2006 CPS sample of US-born Mexican-descent children in intact
families was 26.0% G4+ versus 12.8% G3. This is a selected child sample, not today's
national share, but older-generation families were already present decades ago.
The category explicitly pools fourth and higher generations.
[SOURCE A2: [author paper, Table8](https://discovery.ucl.ac.uk/id/eprint/14197/1/14197.pdf).]

Neither the new CPS linkage, Pew's combined great-grandparents/earlier-ancestors
question, nor the inspected public NLSY data separate G4 from G5+. G4+ includes
families identified as Mexican without observing a Mexican-born great-grandparent;
it is not proof of an exact recent-immigrant lineage. Exact great-grandparent
birthplaces and appropriate coverage/identity data would change this conclusion.
Until then, G5+ has an unknown size, with no justified zero or rounding-error
assumption. No missing-generation fiscal adjustment follows. [MEASUREMENT / GAP]

## Use in the account

- **Present residents:** retain observed G3+; a G4 breakdown changes description, not the population total.
- **Assimilation:** separate generations where measured, show age/cohort, location and mixed parentage, and test identity selection. Cross-sectional generation gaps are not changes observed within the same families.
- **Missing remote descendants:** model their population and outcomes together. Adding people while assigning the identifying subgroup's disadvantage to all of them is unsupported.
- **Arrival-to-descendants projections:** following G4 is legitimate under a declared horizon and counterfactual, carrying both taxes and costs. Attribution across mixed lineages must avoid counting a person repeatedly. A whole person's descriptive membership does not establish full causal attribution to one ancestral arrival. [INFERENCE / FRAMING-SENSITIVE]

[GAP] No exact-G4 national fiscal estimate or observed fiscal profile of all nonidentifying remote descendants was established. Earlier population-uplift scenarios cannot be imported mechanically into the current account. The partial split improves description; it changes no fiscal model result.

## Revisions

- **2026-09-20, executed extension:** The initial note documented G3+ coverage.
  The [new parent-linkage and historical tabulations](../infra/immigration-fiscal/generation_split_2026_09_20/README.md)
  now separate observed G3/G4+ where possible, retain unresolved cases and test
  the claim that later generations are negligible. The original total and
  ancestry-selection limits remain. Independent code review reproduced all 47
  generation-distribution rows. No new causal attribution rule is adopted.
- **2026-09-20, additional-data check:** [Unresolved-reason, adjacent-wave and GSS
  probes](../infra/immigration-fiscal/generation_split_2026_09_20/README.md#additional-recovery-checks)
  explain the missing history and establish a stronger independent adult
  benchmark. The annual-wave yield is small; survey transport and exact G4/G5
  remain unestablished. Independent review reproduced 72 recent GSS subgroup
  rows, 27 CPS diagnostics and 81 original linkage rows; two diagnostic issues
  were fixed without changing the reported totals. No canonical person
  classification or fiscal output changes.
- **2026-09-20, aggregate-model extension:** The previously proposed age-aligned
  survey estimates are now [executed](immigration-later-generation-estimates-2026-09-20.md).
  The [decision](../decisions/2026-09-20-estimate-generations-without-relabeling-records.md)
  keeps conditional population estimates separate from observed person labels.
  Historical sources disagree somewhat; missingness and transport remain material.
  PSID fields are verified but the joint completeness count needs authenticated access.
