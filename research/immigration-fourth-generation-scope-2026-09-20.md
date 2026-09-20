# Fourth-generation scope: evidence index

Date: 2026-09-20. [MEASUREMENT / ACCOUNTING] Extended with an executed partial generation split; no change to the total population or fiscal account.

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
