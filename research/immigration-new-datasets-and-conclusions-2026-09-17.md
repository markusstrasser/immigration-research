# New datasets and the remaining generation conclusions — 2026-09-17

**Verdict:** The new Pew files directly measure a population missing from ordinary ethnic self-identification samples: adults who report Hispanic ancestry without identifying as Hispanic. Including them reduces measured ethnic attachment and modestly reduces Democratic leaning. The existing CILS/IIMMLA crime tables largely reproduce, but their lower-bound and parity interpretations are too strong. The supplied ICPSR archives contain documentation only. The two NLSY ZIPs are byte-identical; their filename overstates their usable crime coverage.

Mode: adversarial measurement audit and descriptive analysis. Frame: what family migration history, current identity and observed outcomes can separately establish. Political and causal interpretations remain explicit inferences. LLM judgments are treated as fallible; the checks below use archived source instruments and reproducible calculations rather than a model's political intuition. This continues the [five-channel audit](immigration-new-conclusions-audit-2026-09-17.md); it does not claim to revalidate every fiscal or crime result in the repository.

## 1. All supplied files accounted for

Thirteen supplied files correspond to twelve distinct byte streams: nine distinct archives containing respondent data, two documentation-only ICPSR archives, and one standalone NLS Investigator variable-selection file. The eight Pew surveys contain 14,517 records in total; this is a record count across separate surveys, not a count of verified unique individuals. Originals remain in Downloads. Canonical copies are under `infra/immigration-fiscal/new_datasets_2026_09_17/raw/`, with raw and derived files ignored by Git. The existing `sources` symlink points outside the writable repository, so this acquisition uses a real local analysis directory. [SOURCE: [manifest](../infra/immigration-fiscal/new_datasets_2026_09_17/manifest.json), [acquisition ledger](../infra/immigration-fiscal/new_datasets_2026_09_17/ACQUIRED.md), staged Pew dictionaries.]

| Supplied input | Actual content and useful role | Limitation |
|---|---|---|
| Both `nlsy97_gen_crime_1` ZIPs | Same NLSY97 extract, codebook and syntax; keep one canonical archive | The `(9)` suffix is not a ninth wave or a new sample |
| `gen_crime_2026.NLSY97` | A separate Investigator selection basket | Variable requests do not prove those variables were exported |
| Pew NSL2011 | 1,220 respondents; earlier nativity, identity and political cross-section | Self-identified Hispanics only |
| Pew NSL2012 | 1,765 respondents, including non-Catholic oversample | Use its weight; no personal links to 2011 |
| Pew Latino Religion 2013 | 5,103 respondents; religion, nativity, identity | Split questionnaire forms require appropriate form weights |
| Pew NSL2014 | 1,520 respondents; parents' and grandparents' Hispanic/Spanish origin | Family-origin wording differs from 2015; no nonidentifier complement |
| Pew NSL2015 | 1,500 respondents; family origin, four-grandparent nativity, identity and party | Main identifying-Hispanic half of the paired analysis |
| Pew “2016 non-Hispanics” | 401 respondents, fielded November 2015–February 2016 | Complements **NSL2015**, not NSL2016; supplied generation recode unusable |
| Pew NSL2016 | 1,507 respondents; election, American dream, nativity | Separate cross-section, August–September 2016 |
| Pew NSL2018 | 1,501 respondents; later political and identity cross-section | No repeated-person linkage established |
| ICPSR30302 v1 | New York second-generation study: codebook, questionnaire, catalog | No respondent file; selected origins exclude a Mexican analytic group; catalog specifies restricted agreement |
| ICPSR20862 v6 | Latino National Survey 2006: questionnaires and four codebooks | No respondent file; four dataset variants are not four waves |

Source for the table: actual ZIP membership, packaged study catalogs/readmes, and SAV variable dictionaries, all tied to the acquisition manifest. Detailed cards are in the [dataset register](immigration-dataset-register.md).

## 2. Pew: ancestry-based inclusion changes the picture, selectively

The published design combines NSL2015 and the non-Hispanic omnibus using an external **89% identifying / 11% nonidentifying** population mixture. Each survey's weights must first be normalized within that survey. Raw sample sizes or weight sums cannot supply the mixture. The 11% is an input to our calculation, not an independent replication: the full omnibus screening denominator is not supplied. [SOURCE: [Pew methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).]

Own weighted calculations from the two supplied SAVs:

| Outcome | Identifying Hispanics | Nonidentifiers reporting Hispanic ancestry | Combined at 89/11 |
|---|---:|---:|---:|
| Democrat or Democratic leaner | 58.67% | 48.73% | 57.54% |
| Democratic identification without leaners | 37.52% | 30.63% | 36.74% |
| Describes self as a typical American | 53.23% | 64.95% | 54.55% |
| Hispanic ancestry/country of origin essential to identity | 38.64% | 13.62% | 35.91% |

Valid-response denominators, respectively: party leaning 1,423 / 395 / 1,818; party identification 1,407 / 394 / 1,801; typical American 1,389 / 386 / 1,775; ancestry-essential 1,480 / 391 / 1,871. Unknown/refused responses are excluded separately for each item; all-response distributions and weighted missing shares are retained. The ancestry item is a near-match: omnibus `q16cx` explicitly specifies Hispanic ancestry, whereas NSL `q16c` asks ancestry or country of origin. No survey-design confidence intervals or causal effects are claimed. [SOURCE: [Pew analysis](../infra/immigration-fiscal/new_datasets_2026_09_17/pew/analyze.py), generated `derived/pew/results.csv`, dictionaries and packaged question text.]

The more relevant correction is often within later generations. Among fourth-plus-generation identifiers, Democratic leaning is **50.28%**; including nonidentifiers moves it to **47.02%**. Ancestry-essential falls **27.82% → 18.92%**. The small all-generation party correction cannot be applied indiscriminately to every third/fourth-generation measure. [SOURCE: same outputs, `NSL2015` versus `pooled_89_11`, `group=gen4`.]

Among people reporting exactly **one Hispanic-origin grandparent**, 57.04% identify as Hispanic, versus 99.49% among those reporting four. Sample records are 126 versus 1,025, with Kish effective sample sizes approximately 63 versus 631. These are descriptive, complete-grandparent-count comparisons; the weight-concentration diagnostic is not a design-based confidence interval. The fields measure reported Hispanic origin, not Mexican birthplace or genetic ancestry. [SOURCE: same outputs, `grandparents_hispanic_1` and `_4`.]

### Two instrument corrections matter

First, the omnibus `immgen` contains **no valid generation values**: 367 records are code 9 and 34 code 8. We reconstruct both surveys from respondent `q4`, parents `q7/q8`, and grandparents `q8aa/q8ab/q8ba/q8bb`. A known foreign/PR-born parent can establish second generation even if the other parent is unknown; fourth-plus requires all four grandparents known US-born. Remaining uncertainty stays unknown. The reconstruction treats Puerto Rico as migrant origin to match this Pew analysis; this convention cannot silently replace legal nativity or the GSS/ANES conventions. [SOURCE: original SAV labels and generated `generation_audit`.]

The resulting identifying-Hispanic percentages are 97.49 / 92.71 / 78.10 / 51.40 across first, second, exact generic third and fourth-plus generations. “Exact third” identifies a foreign/PR-born grandparent, **not specifically a Mexican-born grandparent**. These figures recover the published pattern but are not claimed as exact replications of every rounded report value: the mixture is rounded, and five NSL records with unresolved direct birthplaces remain unknown despite the supplied recode classifying them first-generation. [SOURCE: direct-item reconstruction and [Pew report](https://www.pewresearch.org/hispanic/2017/12/20/hispanic-identity-fades-across-generations-as-immigrant-connections-fall-away/).]

Second, **80.83% of the entire weighted omnibus sample say they never personally thought of themselves as Hispanic**, reproducing Pew's 81% benchmark. “Stopped identifying” is therefore an inaccurate description of most respondents. Intergenerational nontransmission of identity and personal switching are different processes. [SOURCE: `q22=2`, 326/401 unweighted; same Pew report.]

The omnibus also includes earlier-ancestor-only reports: `ha_combo=3` is 39.41% weighted. Pew's methodology contains a narrower “parent or grandparent” formulation alongside broader ancestry screening and analysis of the full 401 records. We retain the full released sample and disclose this boundary; narrowing the sample while keeping the same 11% calibration would require justification. [SOURCE: omnibus screening/codebook and Pew methodology.]

**Independent calibration check:** Pew also publishes 37.8 million identifiers and 4.9 million nonidentifiers. Their ratio implies 88.5246/11.4754 rather than exactly 89/11. Using that count-based mixture, the four generation-identity estimates are **97.37 / 92.38 / 77.27 / 50.21%**, all rounding to Pew's published 97/92/77/50. Democratic leaning becomes **57.50% overall and 46.94% fourth-plus**, versus 57.54% and 47.02% under 89/11. Both constructions are saved. The count figures are themselves rounded; this is a useful benchmark replication, not recovery of confidential exact weights. Pew's published topline also explicitly includes earlier-ancestor-only nonidentifiers, supporting the full-sample reading. [SOURCE: same methodology and report; [published topline p.3](https://www.pewresearch.org/hispanic/wp-content/uploads/sites/5/2017/12/Pew-Research-Center_Hispanic-Identity-Report_Topline_12.20.2017.pdf); independently re-read original SAVs, `pooled_counts` outputs.]

### Verdict on attitude conclusions

Retain the observed GSS/ANES outcome-specific differences. Pew supports the selection mechanism behind the ethnic-attrition caveat and supplies a concrete partisan sensitivity. It does **not** demonstrate that the Hispanic-minus-white thermometer gap vanishes: it has neither that same outcome nor an ordinary non-Hispanic-white comparison sample. Party leaning also cannot substitute for redistribution, trust or fiscal effects. Describing all these measures as a single persistent “collectivism” trait is an untested measurement model. [INFERENCE grounded in instrument comparison.]

### Existing GSS/ANES coding repaired

The GSS loader previously classified all `PARBORN=1…8` US-born respondents as second-generation. The primary labels instead make 3/5/7 unresolved: one US-born parent plus one unknown, or both unknown. Only 1/2/4/6/8 establish a foreign-born parent. This affected 26 US-born Hispanic records in the 2000–2024 file. We corrected the shared generation function, and stopped both GSS and ANES loaders from assigning unknown-generation whites to their auxiliary “G1–2” category. Two regression tests preserve unknowns and verify respondent-nativity precedence. [SOURCE: original GSS R3a value labels, [generation function](../infra/immigration-fiscal/attitudes_gen_2026_09_16/generation.py), rerun loaders and tests.]

The substantive measured patterns survive. Corrected GSS adjusted Hispanic-minus-white trust gaps are −11.15 / −11.63 / −10.52 percentage points; redistribution gaps +0.630 / +0.613 / +0.500 on the seven-point item. Trust here excludes the “depends” response and compares the two definite answers, as in the original estimator. Corrected ANES adjusted net-warmth gaps are +13.405 / +14.098 / +12.394 points. This establishes robustness to this coding repair and the specified age/education controls, not immunity to all composition or ancestry selection. [SOURCE: regenerated `gss_gen_adjusted.csv` and `anes_gen_adjusted.csv`; ANES mean-difference gate passes.]

## 3. CILS and IIMMLA: descriptive findings survive, strong interpretations do not

### CILS generation increases are uncertain

The primary codebook confirms `V448J` and `V448L` refer to the **last five years**; detention includes reform school, detention center, jail or prison. They are not lifetime conviction measures. Our independent extraction reproduces the Mexican male rates. [SOURCE: ICPSR20520 codebook PDF printed pp. 306–307, local [audit script](../infra/immigration-fiscal/new_datasets_2026_09_17/audit_other.py); [study catalog](https://www.icpsr.umich.edu/web/DSDR/studies/20520).]

| Mexican men, CILS | Foreign-born youth | US-born second generation | Second minus foreign-born; illustrative 95% interval |
|---|---:|---:|---:|
| Arrest in last five years | 13/66 = 19.70% | 35/121 = 28.93% | +9.23 pp; −4.11 to +20.87 |
| Detention in last five years | 7/66 = 10.61% | 25/122 = 20.49% | +9.89 pp; −1.64 to +19.53 |

Intervals use the Newcombe construction from independent-binomial Wilson intervals, as a sampling-uncertainty illustration only. They are not design-based population intervals for this selected, attrited school panel. The observed direction agrees with the prior tabulation; a precise origin-specific generational deterioration is not established by these cells. No multiple-testing-adjusted origin interaction claim is made. [SOURCE: generated `derived/other_audit/cils_contrasts.csv`.]

### Selection is not a mathematical lower bound

The earlier finding that retained cases had higher GPA and fewer risk indicators is real descriptive evidence of selective retention. It makes downward selection plausible; it does not identify unobserved adult outcomes. Completing every missing binary record arbitrarily produces these bounds among the original sampled Mexican men:

| Arrest outcome | Observed-response rate | Missing-record completion bounds |
|---|---:|---:|
| Foreign-born youth: 149 baseline records, 66 valid | 19.70% | 8.72–64.43% |
| Second generation: 240 baseline records, 121 valid | 28.93% | 14.58–64.17% |

These bounds assume observed answers are truthful and range over missing-record completions; they are neither estimates nor population bounds. Both lower values lie below the observed rates. Consequently, “all rates are floors” is not established without an additional assumption about missing outcomes. Nor does undercounting both groups imply their **ratio** is a lower bound: true rates 20%/20%, observed 10%/5%, give an observed ratio 2 despite a true ratio 1. No ordering of an IIMMLA lifetime ratio and an ACS current-stock ratio follows from underreporting alone. [SOURCE: generated `cils_missing_record_bounds.csv`; arithmetic counterexample.]

### IIMMLA's parental-education claim is too categorical

We reproduced the source's sex coding (`gender=1` men), origin/generation cells, binary `evarre/evpriso`, and parental education (`q133a/q150a`). Its original parental-education table pooled men and women, whereas the preceding headline concerned men. Among **men** in the two usable strata:

| Highest reported parental education | Mexican second-generation detention | White third-plus detention | Difference; illustrative 95% interval |
|---|---:|---:|---:|
| High school/vocational | 14/102 = 13.73% | 16/54 = 29.63% | −15.90 pp; −30.15 to −2.71 |
| Some college or more | 13/72 = 18.06% | 16/140 = 11.43% | +6.63 pp; −2.95 to +17.89 |

Thus “at or below whites within parental-education strata” is false as a universal description of the point estimates, and “parity” has not been established by an equivalence test. The tiny below-high-school white male cell has only three observations and supports no stable comparison. Results using both parents' education known, versus one or two known, are saved separately. These strata are coarse and observational: neither attenuation of the crime gap nor persistence of an attainment gap proves a class mechanism or rules out family-resource effects. [SOURCE: ICPSR22627 supplied codebook and existing raw TSV; generated `iimmla_sex_parent_education.csv`.]

## 4. The ICPSR documentation still tells us something

**30302, Immigrant Second Generation in Metropolitan New York:** 3,415 adults aged 18–32, interviewed mainly 1998–1999 (36 records coded 2000). Five selected immigrant-origin groups plus local native white, Black and Puerto Rican controls; no Mexican analytic group. The retrospective family information is not a linked parent-child panel. Its universal grandparent-country information is insufficient: `GDPWIND` only asks West Indian ancestry. `INGRPWT`, `WEIGHT` and `SAMEWT` target different within-group, composition and equal-group analyses. The catalog specifies a restricted-data agreement; do not describe its missing data as an ordinary public download. [SOURCE: packaged 30302 catalog/codebook; [study](https://www.icpsr.umich.edu/web/ICPSR/studies/30302).]

**20862, Latino National Survey 2006:** 8,634 self-identified Latino respondents; public DS0001 has 275 variables, public contextual DS0003 has 427. DS0002/4 are restricted variants of the same study, not extra waves. Revised `WT_NATION_REV`, `WT_STATE_REV`, `WT_METRO_REV` target different geographies. `PARBORN` and `GRANBORN` can distinguish generic generations within Latino self-identifiers; no precise Mexican-born-grandparent lineage or respondent crime history is established. `INCSUPP`, `HEALTH`, `GOVTRUST`, party and immigration items are useful attitude outcomes once data arrive. Actual sample geography covers about 87.5% of US Hispanic adults; no non-Latino control is sampled. [SOURCE: packaged 20862 catalogs/codebooks; [study](https://www.icpsr.umich.edu/web/ICPSR/studies/20862).]

A small documentation-based check is possible without inventing joint records. The LNS codebook reports 6,847 supporters of income assistance among 8,634 records, and 5,704 Mexican self-identifiers. Even if every non-Mexican respondent supported it, at least **3,917/5,704 = 68.67%** of the unweighted Mexican self-ID sample must support it. This is an arithmetic sample bound, not a weighted population estimate, and provides no generation-specific slope. The corresponding mainland-US-born support bound is 27.06–100%, demonstrating why marginal tables cannot establish convergence. [SOURCE: parsed `INCSUPP`, `ETHNIC`, `BORNUS` tables; [codebook analysis](../infra/immigration-fiscal/new_datasets_2026_09_17/icpsr/analyze_codebooks.py).]

Official LNS data-documentation access returned HTTP403. The concrete missing public file is `20862-0001-Data.dta` or the expanded `20862-0003-Data.dta`; downloading documentation again will not supply it. No access controls were bypassed.

## 5. NLSY97: a real join, an incomplete export, and a bounded crime check

The supplied ZIP contains 6,795 variable references. The standalone basket contains 16,006, including all 6,795 exported references and **9,211 additional requested fields**. It requests cumulative arrest `E8033100`, incarceration `E8043100`, and incomplete-history flag `E8043601`, which are absent from the data ZIP. But it omits the audited own-birthplace field, four grandparent birthplace fields, ASVAB Mexican self-ID fields and the Mexico/Central-America parent count. Re-exporting that basket alone would still leave important measurement gaps. A [98-field reproduction request](../infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/required_analyzed_fields.NLSY97) is now provided. [SOURCE: exact tagset set differences, `derived/nlsy/tagset_coverage.json`, codebooks.]

The already-held full source, `iq-sex-differences/data/nlsy/nlsy97_all_1997-2023.zip`, supplies the missing public fields. It and the new extract have the same 8,984 unique respondent IDs. Checked overlapping fields agree exactly. The actual ability file supplies 7,059 unique matching IDs with agreeing sex indicators; the prior outcome cache's seven checked household/degree/age/weight/job/wage fields also agree. These support one-to-one **PUBID-based** joins to ability and adult outcomes; they are not independent samples or a validation of every unexamined variable. The cumulative crime fields are absent from the new ZIP, so current-release drift in those fields cannot be checked. [SOURCE: `derived/nlsy/join_and_coverage.json`; sibling script and actual source files inspected, not only its memo.]

The cohort comprises people born in 1980–1984 who resided in the US in 1997, excluding later arrivals. We restrict the diagnostic to positive round-21 cumulative weights (`U6365400/100`, 6,569 cases). Outcomes are cumulative self-reported arrests and separate jail/adult-correctional incarcerations available in the 1997–2023 release, by latest observed interview; incarceration excludes juvenile detention. They are not annual offense rates, convictions, a fixed-age hazard, or a current prison stock. [SOURCE: [BLS cohort](https://www.bls.gov/nls/nlsy97.htm), [NLS crime guide](https://nlsinfo.org/content/cohorts/nlsy97/topical-guide/crime/crime-delinquency-arrest), extracted cumulative-variable codebooks.]

| Group and sex | Valid incarceration n; unweighted events | Weighted ever-reported jail/adult-correctional incarceration |
|---|---:|---:|
| Mexican/Chicano self-ID men | 316; 60 | 18.17% |
| Specified non-Hispanic White comparator, men | 1,532; 207 | 13.56% |
| Mexican/Chicano self-ID women | 359; 15 | 4.80% |
| Specified non-Hispanic White comparator, women | 1,541; 90 | 5.82% |

Mexican self-ID means any ASVAB origin response is Chicano/Mexican/Mexican-American (21/22/23). The comparator is baseline household-informant non-Hispanic and White, excluding Mexican ASVAB self-ID to avoid overlap. It permits missing ASVAB responses; origin measurement availability is therefore asymmetric. Baseline non-Black/non-Hispanic alone was **not** mislabeled White. No survey-design significance or population equivalence claim is made. Positive weights do not solve ASVAB selection, recall, selective retention or missing family histories. [SOURCE: `t6_NHWhite_comparison.csv`, original ASVAB/baseline codebooks.]

The male descriptive ratio is 1.34, but this is not a second-generation estimate and cannot directly overturn IIMMLA's different local, lifetime, parental-education comparison. Among US-born Mexican self-ID men, those with all four grandparents known US-born have **15.17%** reported incarceration (n=70), versus **17.83%** with at least one foreign-born grandparent (n=171); unresolved histories have **26.35%** (n=43). This is a useful contrary diagnostic to a simple universal worsening story. Those categories cannot be relabeled exact Mexican generations, and their small cells do not identify a causal generational effect. [SOURCE: `t2_USborn_grandparent_history.csv`.]

Why the classification remains limited: public grandparent items indicate US/territories versus elsewhere, with no Mexican-specific birthplace. `PAR_MEXCAM` pools Mexico and Central America and explicitly includes nonbiological parent types; zero is not evidence of two US-born biological parents. The supplemental biological-parent US-birth questions apply mainly to a no-parent-interview/nonadopted branch, producing only 963/955 usable parent answers. Our strict parent-plus-grandparent classification consequently leaves **7,759/8,984 unresolved**. Five conflicting own-birth reports remain unknown; skipped parent fields never become native parents. A full biological-parent-roster derivation has not been implemented here, so this is the coverage of the audited fields, not proof that every possible public reconstruction is exhausted. [SOURCE: archived codebooks and `join_and_coverage.json`; [NLS parent guide](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/family-background/parent-characteristics).]

The incomplete-history sensitivity removes `E8043601=1` and changes male Mexican self-ID incarceration from 18.17% to 16.87%. This selects away potentially high-arrest histories and is not a correction or bound. Restricted country-specific parent/grandparent geography would be needed for the exact Mexican-birthplace lineage used in the published NLSY97 attrition study. No ability/crime regression or genetic inference was run. [SOURCE: `t1_self_identity.csv`, original flag codebook, [NLS ethnicity/birthplace guide](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/household/race-ethnicity-citizenship).]

**Achievement-test availability correction to ladder83:** “no SAT or ACT by generation exists” is too broad as a data-availability claim. NLS documents respondent-reported and school-transcript SAT/ACT scores in the same cohort. A custom cross-tab against observed family-history categories is possible in principle; this audit has not produced a valid ancestry-complete generation table or verified the earlier AFQT SD conversions. Test taking and transcript availability introduce additional selection. The defensible narrower claim is that the earlier lane did not locate a verified published SAT/ACT-by-generation estimate, not that the variables are absent. [SOURCE: [NLS achievement-test guide](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/achievement-tests), [transcript documentation](https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-11-collection-of-transcript-data).]

**Later September 17 export check:** the three newly supplied `nlsy97_gen_crime_2` ZIPs are exact duplicates, containing 8,608 fields and the same 8,984 unique respondent IDs. The cumulative arrest, incarceration and incomplete-history variables are now present and agree exactly with the earlier full archive, alongside four other checked non-ID fields. This closes the cumulative-history drift gap above for this export; the prior crime tables need no change on this evidence. It is not a check of every exported field or proof of the newest available release. The first and second exports together still lack 47 of the 98 frozen requested fields, including important family-history and self-ID items available in the older full archive. [SOURCE: [follow-up comparison and provenance](../infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/followup_export_check.json), generated by `nlsy/check_followup_export.py`.]

## 6. What can actually join

| Pair | Permitted operation | Meaning |
|---|---|---|
| NLSY97 extracts from the same cohort | Respondent-ID join after uniqueness and overlap checks | Additional columns for the same surveyed people; source vintages can disagree |
| Pew NSL2015 and omnibus2015–16 | Append with source-prefixed IDs and externally calibrated weights | Complementary sampled populations, not matched people |
| Different Pew years | Harmonize comparable questions, preserving survey year and design | Repeated cross-sections; no person-level change or lineage identification |
| LNS DS0001 and DS0003, when acquired | Validate same-case IDs, then use richer variant or add columns | Same 8,634 cases; never stack as independent samples |
| CILS, IIMMLA, NYC, NLSY97, Pew | Compare compatible group-level estimands | No cross-study person linkage from coincident numeric IDs |
| Survey plus geographic context | Only validated public geography × matching period | Area context, not an observed personal exposure or causal effect |

This mapping describes source capabilities; it does not change the project's central analysis protocol. Current family-history fields support labels such as **“US-born with one foreign-born parent; Mexican self-identification”**. A “third-generation Mexican” label requires saying whether Mexican origin is inferred from identity or actually observed in a grandparent's birthplace. Report counts of known parental/grandparent branches and unknowns separately. One Hispanic-origin grandparent is a genealogy/identity report, not “25% genetically Mexican.” [SOURCE: instruments compared above; [classification proposal](immigration-new-conclusions-audit-2026-09-17.md).]

## 7. Reproduction and remaining limits

Acquisition hashes and ZIP CRCs were checked; Pew's 81% benchmark and ICPSR codebook frequency totals reproduce. All eight Pew archives were inventoried, decoded and documented; the substantive Pew calculation uses the correctly paired two surveys. Other Pew years supply a question-level catalog, not eight completed trend replications. CILS and IIMMLA were independently re-tabulated from the already-held raw files. Scripts, the README and generated tables live in [the acquisition directory](../infra/immigration-fiscal/new_datasets_2026_09_17/README.md).

No new net-fiscal balance, crime-cost total, genetic explanation or national causal generational effect follows from these files. They can improve identity measurement, compare family backgrounds and trace within-cohort outcomes. The previous fiscal, automation, fertility and welfare conclusions retain their separately documented status; absence of a relevant outcome here is not confirmation.

## Revisions

- 2026-09-17 — [Decision](../decisions/2026-09-17-family-history-data-and-inference-audit.md): qualify ladder83/87/104–106, preserve unknown parent branches, and separate ancestry-inclusive comparisons from self-ID samples and cross-study estimands.
