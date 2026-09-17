# Organized surveys: what changes the conclusions

**Verdict:** The supplied downloads are sorted into a [named, hash-verified library](../infra/immigration-fiscal/new_datasets_2026_09_17/library/README.md). New analysis improves NLS family-history coverage, confirms substantial language differences across Pew generations, and exposes two political-measurement mistakes: changing denominators and collapsing distinct legalization options. None of these results establishes a genetic explanation, a national causal generation effect, or a fiscal balance. [SOURCE: linked source-level analyses below.]

## Files, duplicates and legitimate joins

The library accounts for 22 supplied file paths and the extracted ICPSR folder. Fifteen distinct supplied file variants receive descriptive names; duplicate or equivalent downloads map to those copies. Originals are preserved. The 2016-named Pew nonidentifier archive is labeled by its actual 2015–2016 field period. Both ICPSR packages are explicitly marked documentation-only. The latest `nlsy97_gen_crime.zip` is present and its CSV/codebook/tagset match the completed `default.zip` export. The browser's HTTP error did not mean the local export was missing. [SOURCE: [catalog](../infra/immigration-fiscal/new_datasets_2026_09_17/library/catalog.json), [organizer](../infra/immigration-fiscal/new_datasets_2026_09_17/organize.py).]

| Source | Valid operation | What it adds / cannot supply |
|---|---|---|
| NLSY97 exports and already-held full archive | Join the same 8,984 people by validated PUBID | Additional family-history columns and cumulative reported outcomes; no independent replication or country-specific Mexican genealogy |
| Seven Pew surveys, 2011–2018 | Compare harmonized questions within survey; labeled pooled sensitivities | Repeated cross-sections, not a panel or a person-level join |
| Pew NSL2015 + 2015–2016 nonidentifiers | Externally calibrated complementary-population mixture | Includes ancestry respondents outside Hispanic identity; not matched individuals or a universal correction for every outcome |
| Supplied ICPSR20862 / 30302 | Read codebooks and access terms | No respondent data present; ICPSR20862 member-account gate independently explained by the user's browser report |
| Three newly located public LNS author replications | Analyze separately under their documented transformations | Actual data, but incomplete projections with differing weights/IDs; no justified cross-package join |

The [register](immigration-dataset-register.md), [access note](../infra/immigration-fiscal/new_datasets_2026_09_17/access-status.md) and [LNS replication audit](immigration-lns-public-replications-2026-09-17.md) preserve versions, checksums, variables and limitations. No respondent data are committed or published.

## Findings that change the reading

**1. NLS's earlier missing-parent result was partly an extraction mistake.** The supplemental mother/father questions apply when the main parent interview is absent. Reconstructing the main interview with corrected biological-parent IDs reduces unresolved detailed generations from **7,759 to 3,266 of 8,984**. Biological mother's birthplace is known for8,430 and father's for6,897. Roster position is not always person ID; the final implementation uses stored IDs and preserves contradictory reports as unknown. [SOURCE: [NLS reconstruction and independent checks](immigration-nlsy97-parent-linkage-2026-09-17.md).]

For Mexican/Chicano self-identifying men with positive round21 weights, reported cumulative incarceration is **16.67%, 17.30%, 14.57%** in the questionnaire-derived G2/G3/G4+ categories. Unweighted event counts are19/113,9/46,8/46; they are not the numerators of those weighted percentages. Arrest percentages instead rise41.73→49.20→49.52. Thus this sample does not show a monotonic incarceration gradient, and the arrest counterpattern must remain visible. Small cells cannot establish parity or disprove a population gradient. The unresolved own/parent group is24.32%, so simply discarding it is consequential. This outcome is cumulative reported incarceration, not an annual crime rate. [SOURCE: same NLS memo.]

**2. A blanket nonassimilation story conflicts with direct language and similarity measures.** Across seven Pew surveys, English conversation rated “very well” is **22.2–27.8% in G1 versus77.0–83.7% in G2**. These are ranges across survey-year estimates, not uncertainty intervals. Three surveys show progressively more perceived similarity to a typical American. Neither item measures loyalty, trust or fiscal contribution. Composition and continued Hispanic identification remain selection issues. [SOURCE: [Pew harmonization](immigration-pew-generation-denominators-2026-09-17.md).]

**3. The political denominator can reverse the answer.** On the same five-survey base, reported Democratic identification/leaning is55.89% in G1 and61.04% in G2 **among all respondents**. Among people reporting either major party it is75.05% versus71.93%. Both are correct: G2 reports a major-party affiliation more often, while Democrats have a smaller share conditional on that affiliation. The signs survive the reported age/sex/year and Mexican-origin sensitivities. These are descriptive comparisons, not causal generation effects or voting predictions. The earlier NSL2015 figure58.67% specifically used valid composite categories; all respondents gives55.86%. [SOURCE: same Pew memo and independent denominator verifier.]

**4. Immigration preferences are multidimensional.** In a freely posted 2006 LNS author derivative with a revised national weight, immediate legalization is59.0% among author-coded first-generation noncitizens,25.1% in second generation,14.4% in third and15.9% in fourth-plus. Including the offered guest-worker route to eventual legalization produces67.1%,59.8%,61.7% in the latter three groups. The evidence supports different preferred routes, not the claim that later groups uniformly oppose legalization. Raw lineage construction is absent, and the derivative does not exactly reproduce the paper's overall benchmark; its table is explicitly limited to the deposited data. It is not current opinion. [SOURCE: [LNS audit, full response options and limitations](immigration-lns-public-replications-2026-09-17.md); [public replication source](https://doi.org/10.7910/DVN/27113).]

The other conclusions—fiscal balances, automation, fertility, disability, welfare, agglomeration and political costs—retain the status established by the [broader conclusion audit](immigration-new-conclusions-audit-2026-09-17.md) and [initial dataset audit](immigration-new-datasets-and-conclusions-2026-09-17.md). These surveys supply no new identification of those effects. Adding datasets does not independently validate unrelated claims.

## A better classification than racial fractions

Use **family migration history** as a set of observed facts, with separate national-origin identification. “One Mexico-born grandparent; three US-born grandparents; self and both parents US-born” is more informative than “one-quarter Mexican.” It describes reported genealogy, not a measured genomic proportion. Someone can also have Mexican-origin grandparents born in the US; birthplace alone does not fully recover origin. [INFERENCE / measurement recommendation, based on the instruments' distinct birthplace and identity items.]

| Dimension | Store explicitly |
|---|---|
| Respondent migration | Birth country, age/year of arrival, citizenship-at-birth where observed; record territory convention |
| Biological family history | Each parent's and grandparent's reported birthplace/origin, branch and source; known/unknown/conflicting separately |
| Mixed histories | Number of known foreign-born parents/grandparents **and number observed**; origin sets can overlap |
| Upbringing | Adoptive/step/rearing parents, household language and relevant residence history separately from biological lineage |
| Identity | Self-described national/ethnic identity and survey-year wording, including nonidentification |

Generation can then be a convenient derived label: G2 if US-born with at least one known foreign-born parent; G3 if the respondent and both parents are known US-born and at least one grandparent foreign-born; G4+ only if the respondent, both parents and all four grandparents are known US-born. Unknown history must not become G3+/G4+ by default. “G3+” from parental birthplace alone is a different resolution, not exact third generation. These are generic migration labels until country-specific family information is observed. The NLS wording differences around territories require an additional caveat. [METHOD: implemented rules and source limits in the NLS/Pew memos.]

## Decision, alternatives and next useful evidence

The leading explanation for the changed conclusions is measurement: questionnaire routing, corrected identity links, response options and denominators. The competing explanation for substantive group differences is composition and selection—cohort, age, citizenship, origins, arrival age, survey retention and identity attrition. The analyses separate these mechanisms where the instruments permit, without asserting that the remaining differences identify causal assimilation. [INFERENCE]

The decisive next evidence would be a country-specific family-history sample that includes nonidentifiers, complete design variables and comparable outcomes/benchmarks, or authorized original LNS files with revised weights and verified IDs. It could change both category membership and estimates. No further NLS download is required for the current analysis. The browser should stop repeating ICPSR documentation downloads under the unchanged account; [specific remaining access options](../infra/immigration-fiscal/new_datasets_2026_09_17/access-status.md) involve a legitimate affiliation or another authorized source, with no payment undertaken.

LLM instrument check: language improvement, nonmonotonic incarceration, rising arrests, high outcomes among unresolved cases, both partisan denominators and both legalization routes are all retained. Source definitions and reproducible arithmetic, not an assumed political direction, govern these conclusions. [METHOD]
