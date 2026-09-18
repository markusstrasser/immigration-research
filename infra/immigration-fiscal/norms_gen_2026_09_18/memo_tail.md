---

## C. External anchors: what the origin country looks like

### C1. World Values Survey wave 7, Mexico 2018 versus the United States 2017

Computed from the WVS7 cross-national microdata with the WVS country weight `W_WEIGHT`, on valid responses (the WVS convention, dropping don't-know and refused). "Good" is very good plus fairly good; confidence is a great deal plus quite a lot. Unweighted n is 1,741 for Mexico, fielded January to May 2018 in a single mode, and 2,596 for the United States, fielded April to May 2017 in mixed mode. The two country samples are a year apart, so this is not a synchronous comparison. [SOURCE: `WVS_Cross-National_Wave_7_csv_v6_0.csv` v6.0, 190,499,076 bytes, obtained via the Kaggle mirror `lauriszon/wvs-cross-national-wave-7` and computed 2026-09-18; underlying study DOI https://doi.org/10.14281/18241.24. The WVS site's own download endpoint returns a one-byte body to plain HTTP, documented in `ANCHORS.md`. The mirror's country-year composition matches the WVS7 country list and the weight sums to the unweighted n, which is a consistency check, not a byte-level match against the official archive. Every figure in this table was recomputed independently by this lane with `wvs_recheck.py`, written without reading the fetching agent's script, and all ten reproduce to the stated precision along with both sample sizes and country-years.]

| Item | Mexico 2018 | United States 2017 |
|---|---:|---:|
| Strong leader who does not have to bother with parliament and elections — good | 71.6% | 38.1% |
| Having a democratic political system — good | 75.8% | 85.0% |
| Having experts, not government, make decisions — good | 76.2% | 52.6% |
| Having the army rule — good | 45.5% | 20.9% |
| Importance of living in a democracy, 1-10 mean | 8.30 | 8.28 |
| …share answering 8-10 | 72.0% | 71.3% |
| Confidence in the police | 21.3% | 68.8% |
| Confidence in the courts and justice system | 22.5% | 57.8% |
| Confidence in the government | 17.4% | 33.7% |
| Confidence in parliament | 14.6% | 15.1% |

### C2. The two instruments disagree on levels, so treat the levels as unusable

A Pew Global Attitudes Spring 2017 battery asked near-parallel questions and gives very different numbers: a strong leader who can decide without interference from parliament or the courts is rated good by 27 percent in Mexico and 22 percent in the United States, against the World Values Survey's 71.6 and 38.1 percent. [SOURCE: https://www.pewresearch.org/global/wp-content/uploads/sites/2/2017/10/Pew-Research-Center_Democracy-Report-Topline-Questionnaire_2017.10.16.pdf, fetched 2026-09-18]

The wordings differ, Pew keeps don't-knows in the denominator while the World Values Survey convention drops them, and the modes differ. What survives both instruments is the **ordering**: Mexico is above the United States on strong-leader rule (71.6 versus 38.1 on one instrument, 27 versus 22 on the other), on army rule (45.5 versus 20.9, and 42 versus 17), and on rule by experts (76.2 versus 52.6, and 53 versus 40), and below the United States on representative democracy (75.8 versus 85.0, and 58 versus 86). What does not survive is the magnitude: the Mexico-United States gap on the strong-leader item is 33 points on one instrument and 5 on the other. The memo therefore quotes the World Values Survey throughout section C1 and uses Pew only as the labelled second instrument here; the two are never mixed into one series, and no numerical gap from either is carried into the synthesis. Pew's own institutional readings for Mexico are 6 percent satisfied with the way democracy is working and 17 percent trusting the national government a lot or somewhat, against 46 percent satisfied in the United States.

### C3. What the anchor can and cannot do

**It cannot be differenced against sections A and B at all on the confidence items.** A respondent in Mexico rating confidence in the police is rating the Mexican police; a respondent in the General Social Survey is rating American institutions. Institutional confidence is a judgement about a particular object, not a portable disposition, so Mexico's 21.3 percent confidence in its police and the finding that Mexican-origin first-generation respondents are *more* confident in American institutions than native whites are not in tension and do not need reconciling. They are answers to different questions.

**The regime-preference items are more comparable**, because "is a strong leader a good way of governing" is closer to an abstract disposition. There the origin-country prior is real: on both instruments Mexicans are more favourable than Americans to strong-leader rule, army rule and technocratic rule. If that disposition transported intact, Mexican-origin Americans should be visibly more permissive on the ANES executive-overreach and strong-leader items than whites. What section B measures instead is a third generation at +4.0 points on "the president acting without Congress and the courts" and +3.6 on "a strong leader who bends the rules", both inside the white ideological range and statistically indistinguishable from white conservatives and from whites without a bachelor's degree. So the origin-country disposition, to the extent it exists, is not showing up at anything like its origin-country magnitude. [INFERENCE]

**Selection, not transmission, remains uncontrolled.** Emigrants are not a random draw: migration selects on age, education, risk tolerance, labour-market position and family networks, and plausibly on political disposition too. The direction of political selection among Mexican emigrants is [GAP] — no evidence either way was located. So the gap between Mexico's national regime preferences and Mexican-origin Americans' could be selection at the point of migration, socialisation in the United States, the different meaning of the questions in the two contexts, or any mixture; nothing here separates them.

**LAPOP and Pew-on-US-Hispanics are still [GAP].** The 2026 *Pulse of Democracy* was retrieved in full after three failed streamed downloads by using HTTP range requests in 2 MB chunks [SOURCE: https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf, 21,426,820 bytes, 67 pages, fetched 2026-09-18], but its country bars for Churchillian support for democracy, coup tolerance and institutional trust are images with no text layer. What the narrative carries: Mexico's crime victimization is 33 percent, third highest in the region; perceived criminal-group presence in the neighbourhood is 28 percent, second highest; asked what democracy means to them, 33 percent of Mexicans name law enforcement and 28 percent name equality, against a regional pattern in which law enforcement (30.3 percent), equality (25.0) and freedom (24.4) far outrank participation (10.5) and elections (9.7); and trust in the Chinese government runs 55 percent against 23 percent for the United States government. The report places Mexico among the countries with "more substantial democratic backsliding" and finds that in Mexico its new Support for Illiberal Majoritarianism index is positively and significantly associated with Churchillian support for democracy, meaning professed support for democracy there coexists with a majoritarian rather than a checks-and-balances conception. Region-wide, at least half of respondents in most countries score 4 or higher on that 1-7 index, so this is not a Mexican peculiarity.

On Pew and US Hispanics: the most recent National Survey of Latinos was fielded 6-16 October 2025, n = 8,046 US adults of whom 4,923 Hispanic, online probability panel, English and Spanish [SOURCE: https://www.pewresearch.org/race-and-ethnicity/2026/07/09/u-s-hispanics-are-divided-on-whether-their-identity-helps-or-hurts-them-in-america/, fetched 2026-09-18]. Pew routinely breaks it out by immigrant generation, but on identity rather than on democracy or institutions, and a site search returned no dedicated Latinos-and-democracy release. That is weak evidence of absence, not a verified negative.

Full route notes, failure modes and the Pew topline tables are in `infra/immigration-fiscal/norms_gen_2026_09_18/ANCHORS.md`.

---

## Synthesis

### (a) Do Hispanic and Mexican-origin generations converge to whites?

On the two domains the brief asks about directly, yes, and with a twist on the first.

**Institutional confidence never had a deficit to close.** The first generation is more confident than native whites in eleven of thirteen institutions, and the generational movement is downward toward the white level, reaching parity on the full index (+0.001 scale points, SE 0.018) and near-parity on the three branches of government (+0.040, SE 0.025). Whatever else immigration does to American institutional trust, first-generation Hispanic immigrants are not importing distrust of American institutions; they arrive with more of it than natives have and their grandchildren end up with the native amount. The military is the standing exception.

**Civil liberties had a large deficit and it closes.** The fifteen-item Stouffer scale moves from −1.58 to −0.42 adjusted scale points across three generations, a precise change of +1.16 (SE 0.25). At the third generation the residual gap against whites overall is about four tenths of a scale point on a fifteen-point scale.

**Generalised trust remains the standing counter-example**, unchanged from confidence-ladder entries 87 and 117 and not re-litigated here: adjusted gaps near −10 to −12 points with no precise generational trend.

### (b) Where do they sit against white conservatives and white non-graduates?

This is the part that changes the picture. On almost every item measured, the Hispanic third generation lands inside the range that already exists inside the native white population, and usually at the white-conservative or white-non-graduate end of it.

| Item | Hisp G3+ vs whites overall | vs white conservatives | vs whites without a BA | White conservative − liberal |
|---|---:|---:|---:|---:|
| Stouffer 15-item tolerance (scale pts) | −0.42 (0.18) | **−0.03 (0.19)** | −0.28 (0.20) | −0.98 (0.10) |
| Anti-American Muslim clergyman, 3 items | −0.17 (0.07) | **−0.04 (0.07)** | −0.07 (0.07) | −0.46 (0.04) |
| Obedience as a top child quality (pp) | +3.2 (1.8) | **−1.6 (1.9)** | +2.1 (1.9) | +11.5 (1.0) |
| All-13 confidence index (scale pts) | +0.00 (0.02) | +0.03 (0.02) | +0.01 (0.02) | −0.04 (0.01) |
| Death penalty (pp) | −4.2 (1.9) | −15.7 (1.9) | −7.7 (1.9) | +33.7 (1.1) |
| President without Congress or courts (pp) | +4.0 (2.8) | **+2.0 (3.0)** | **+1.1 (2.9)** | +7.5 (1.3) |
| Strong leader who bends the rules (pp) | +3.6 (3.2) | −8.3 (3.4) | **−0.9 (3.2)** | +29.0 (1.7) |
| Democracy is preferable (2024, pp) | −3.0 (4.9) | −7.7 (5.0) | **−0.4 (5.2)** | −2.7 (2.2) |
| Authoritarian child-rearing (0-4) | +0.16 (0.08) | −0.24 (0.09) | **−0.07 (0.09)** | +1.25 (0.05) |
| Government should reduce income differences (1-7) | +0.46 (0.09) | +1.50 (0.09) | +0.47 (0.09) | −2.18 (0.05) |
| Political violence at least a little justified (pp) | **+10.1 (2.6)** | **+14.1 (2.8)** | **+9.6 (2.7)** | −8.3 (1.4) |

Bold marks the cells where the Hispanic third generation is statistically indistinguishable from that white comparator, or, in the last row, where it is not inside the white range at all. Read down the table: on tolerance, obedience, institutional confidence, executive overreach, strong-leader preference, preference for democracy and authoritarian child-rearing, the third-generation Hispanic position is a white-conservative or white-non-college position. It is not an exotic position. The internal white ideological spread on the same items is usually larger than the Hispanic-white difference, often several times larger.

### (b2) Does this hold for Mexican-origin respondents on their own?

The brief's central group is Mexican-origin, not all Hispanics, and Mexican-origin cells are thinner. Run separately, they reproduce the all-Hispanic pattern on ten of twelve headline items, with two substantive differences.

| Item | Mex G1 vs whites | Mex G2 | Mex G3+ | Mex G3+ vs white cons | vs white no BA | Mex G3+ − G1 |
|---|---:|---:|---:|---:|---:|---:|
| Stouffer 15-item tolerance (scale pts) | -1.37 (0.27) | -1.42 (0.26) | -0.34 (0.23) | +0.04 (0.24) | -0.30 (0.25) | +1.03 (0.34) |
| Anti-American Muslim clergyman, 3 items | -0.44 (0.07) | -0.27 (0.08) | -0.25 (0.09) | -0.13 (0.09) | -0.20 (0.10) | +0.19 (0.11) |
| Obedience as a top child quality (pp) | +16.1 (2.7) | +2.6 (2.4) | +4.4 (2.4) | -0.3 (2.5) | +4.0 (2.6) | -11.7 (3.6) |
| All-13 confidence index (scale pts) | +0.13 (0.02) | +0.02 (0.02) | +0.03 (0.02) | +0.06 (0.02) | +0.04 (0.02) | -0.10 (0.03) |
| Death penalty (pp) | -35.5 (2.3) | -9.7 (2.6) | -4.1 (2.2) | -15.5 (2.2) | -6.7 (2.2) | +31.4 (3.2) |
| Ever approves police striking a citizen (pp) | -42.8 (2.4) | -25.7 (3.4) | -8.7 (3.3) | -14.2 (3.3) | -8.9 (3.3) | +34.1 (3.8) |
| Government should reduce income differences (1-7) | +0.59 (0.11) | +0.58 (0.11) | +0.32 (0.10) | +1.35 (0.10) | +0.33 (0.10) | -0.27 (0.14) |
| President without Congress or courts (pp) | +1.9 (4.1) | +5.2 (3.8) | +5.7 (4.6) | +3.7 (4.6) | +2.7 (4.6) | +3.8 (6.4) |
| Strong leader who bends the rules (pp) | -6.4 (6.5) | -2.4 (4.8) | +2.7 (4.7) | -9.2 (4.6) | -1.5 (4.7) | +9.0 (7.9) |
| Democracy is preferable (2024, pp) | -3.4 (8.3) | -10.9 (6.9) | -3.7 (7.8) | -8.3 (7.8) | -1.0 (7.8) | -0.3 (11.0) |
| Authoritarian child-rearing (0-4) | +0.11 (0.17) | +0.34 (0.11) | -0.03 (0.13) | -0.43 (0.13) | -0.25 (0.14) | -0.14 (0.22) |
| Political violence at least a little justified (pp) | +20.3 (4.7) | +9.5 (4.2) | +13.7 (4.6) | +17.8 (4.7) | +13.0 (4.6) | -6.6 (6.9) |

The Stouffer scale converges just as cleanly (Mexican third-plus minus first +1.03 scale points, SE 0.34) and lands at white-conservative parity (+0.04, SE 0.24). Institutional confidence converges from above, obedience converges in one generation, the death-penalty and police-force items converge upward, and redistribution stays unconverged at a smaller magnitude than for Hispanics overall.

**The exception is the anti-American Muslim clergyman battery.** For Mexican-origin respondents the third-plus generation is still −0.25 scale points below whites overall (SE 0.09) and −0.20 below whites without a bachelor's degree (SE 0.10), against −0.17 and −0.07 for Hispanics as a whole, and the Mexican generational change of +0.19 (SE 0.11) is not clearly distinguishable from zero. On this one battery the Mexican-origin third generation has *not* reached the white-non-graduate level. The all-Hispanic result should not be read as covering it.

**Political violence is larger, not smaller, among Mexican-origin respondents**, at +13.7 points adjusted at the third generation (SE 4.6) against +10.1 for Hispanics overall, and +17.8 against white conservatives. The cells behind these are 158-227 respondents, so the point estimates are soft, but the sign and rough magnitude of the memo's one out-of-range finding are not an artefact of pooling Puerto Rican, Cuban and other-Hispanic respondents with Mexican ones.

Two caveats on that framing. First, the ratio of a Hispanic gap to a white spread is only interpretable where whites actually divide; on items where the white conservative-to-liberal difference is near zero (the thirteen-institution index, confidence in Congress, the 2024 preference-for-democracy item) the ratio explodes and means nothing, and it is not used. Second, "inside the white range" is a descriptive statement about where a group mean falls, not a normative one about whether the position is good.

### (c) What does not converge

Three things.

1. **The economic role of government.** Adjusted gaps of +0.46 scale points on the seven-point redistribution item at the third generation, with a generational change of −0.14 (SE 0.11) that is indistinguishable from zero. This reproduces confidence-ladder entry 87 with income now controlled and with design-based variance. Its size relative to the white ideological spread is 21 percent.
2. **Confidence in the military**, −8.6 points at the third generation with essentially no generational gradient, placing Hispanics at the white-liberal end of an item on which whites divide by 19 points.
3. **Endorsement of political violence in ANES**, +10.1 points adjusted at the third generation, outside the white ideological range, with a generational contrast of −6.0 points (SE 4.1) that cannot distinguish convergence from flatness. This is the one measured norm where the Hispanic position is not a position that some substantial white subgroup already holds. It is also the result that most deserves scepticism, for the reasons in the next section.

A single latent "collectivism" or "tribalism" factor does not organise this pattern. Such a factor predicts that the first generation arrives low on institutional confidence, low on tolerance, high on in-group preference and high on support for redistribution, with all four moving together. What the data show is the first generation arriving *high* on institutional confidence, low on tolerance, high on redistribution, and with the tolerance and confidence components converging fast while the redistribution component does not move at all. [INFERENCE]

---

## Disconfirmation

**Response style is doing real work, and it was measured, not assumed.** Section A6 shows first-generation respondents differentiating far less than whites between survey scenarios, on two independent checks, with the differentiation gap closing across generations on the same schedule as the substantive gaps. Any reading of the first-generation numbers as pure attitude is wrong, and the measured convergence is partly a convergence in how the instrument is answered. This is the strongest single caveat in the memo and it cuts *against* the memo's own convergence story as well as against the gap story.

**Interview language does not resolve into a single bias direction, and the two surveys disagree.** In the GSS, restricting to 2006 onward (Spanish-language interviewing began that year, so the earlier first generation is mechanically all-English and the unrestricted split is confounded with period), Spanish-interviewed first-generation respondents are *more* tolerant than English-interviewed ones (15-item scale 9.32 versus 7.57), *less* likely to rank obedience highly (33.5 versus 52.3 percent) and *less* pro-redistribution (4.69 versus 5.30). The two instrument checks barely move with language at all. In ANES the child-trait battery runs the opposite way: Spanish-interviewed first-generation respondents pick obedience 70.3 percent of the time against 48.2 for English-interviewed ones, and prefer democracy 51.3 against 76.6 percent, though those cells hold only 36-90 respondents. Interview language therefore cannot be treated as a known-sign correction. [DATA: `derived/gss_language_check.csv`, `derived/anes_language_check.csv`]

**The political-violence item is the weakest measurement in the memo.** The published methodological literature finds that standard survey items on support for political violence substantially overstate real endorsement, because a meaningful fraction of respondents answer inattentively or expressively rather than literally, and because the low-bar wording "at least a little justified" absorbs a large share of non-committal answers [SOURCE: Westwood, Grimmer, Tyler and Nall, "Current research overstates American support for political violence", *PNAS* 119(12), 2022, https://doi.org/10.1073/pnas.2116870119]. Combined with the A6 finding that the groups differ systematically in how discriminately they answer batteries, the +10.1-point Hispanic gap on this item is the result in the memo least safe to treat as a real attitude difference. It should be replicated on a behaviourally validated instrument before it carries any weight.

**Mode changed inside both series, and it moves two items.** The GSS `MODE` variable shows the shift directly: every round from 2004 to 2018 is in-person or telephone with zero web interviews, 2021 is 92 percent web and telephone with no in-person fielding at all, and 2022 and 2024 are mixed, roughly half web. ANES 2020 and 2024 are likewise mixed web, video and telephone. Year fixed effects absorb the average mode shift but not a group-by-mode interaction, so the interaction was estimated directly: in 2022 and 2024, the only rounds where web and interviewer-administered interviews coexist, the adjusted Hispanic-white gaps were re-estimated separately within each arm.

On nine of eleven headline outcomes the two arms agree within noise, which is the main result. Two do not. The first-generation gap on ranking obedience a top child quality is +8.2 points in the web arm and +27.7 in the interviewer arm, a difference of 19.5 points with an approximate standard error of 7.2. The first-generation gap on death-penalty support is −13.8 in the web arm and −34.8 in the interviewer arm, a difference of 21.0 with an approximate standard error of 8.6. Both are items where an interviewer is physically present for an answer about obedience and punishment, and in both the interviewer-administered arm produces the larger first-generation deviation from whites. The arms are disjoint respondent sets but share design strata, so treating them as independent for that difference is an approximation, and the sub-samples are small (2,044 and 1,759). The direction is what matters: on at least these two items, some of the first-generation gap reported in section A3 is interviewer presence rather than belief, which compounds the response-style problem above. [DATA: `derived/gss_mode_check.csv`, `derived/gss_mode_difference.csv`]

**Social desirability plausibly runs toward the memo's findings.** Foreign-born respondents in a survey administered by an institution of the host country have an obvious reason to over-report confidence in that country's institutions and commitment to its laws. Sections A1 and A5 are the two places this bites hardest, and both are places where the first generation looks *better* than natives. The A5 result that first-generation Hispanics rate respecting America's laws as very important at 79.5 percent against 64.5 for whites should be discounted accordingly.

**GSS Hispanic oversamples.** The GSS ran Spanish-language capability and associated design changes from 2006, which changes the composition of the Hispanic sample mid-series. Year fixed effects and the nonresponse-adjusted weights handle the average level shift; they do not guarantee a stable Hispanic sampling frame across the window. A year-interacted specification was not fitted. [GAP]

**Ethnic attrition biases toward the non-convergence findings.** Third-generation Hispanic identifiers are a selected subset of third-generation Hispanic descendants, selected toward those who still identify, who are on average less assimilated [SOURCE: confidence-ladder entry 107, reproducing Pew's identity-selection evidence]. Every convergence estimate here is therefore a lower bound on true lineage convergence, and every non-convergence estimate an upper bound on true lineage persistence.

**Cells are thin where the question is most interesting.** The Mexican-origin national-identity cells hold 25-109 respondents. Those tables cannot support a Mexican-specific verdict and are reported with all-Hispanic pooling alongside.

**ANES nulls are underpowered.** No ANES generational contrast is distinguishable from zero, but the standard errors are 4 to 13 points on gaps of similar size. "ANES shows no convergence" is not a finding.

**What would falsify the central claim.** The claim is that third-generation Hispanic positions on institutional confidence and civil liberties fall inside the range already spanned by white ideological and educational subgroups. It would be falsified by: a design-based estimate on a larger Hispanic sample showing the third-generation tolerance gap against white conservatives to be reliably non-zero; a behaviourally validated measure of institutional commitment showing the survey parity to be an artefact of acquiescence; or a within-lineage panel showing that third-generation identifiers are not selected in the direction the ethnic-attrition literature assumes.

---

## Sources

- General Social Survey 1972-2024 cumulative file, release R3a, NORC at the University of Chicago. Local copy `raw/GSS_stata/gss7224_r3a.dta`; obtained 2026-09-16 from https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip. Read with `pyreadstat`, `encoding="latin1"`.
- NORC design-variable guidance, https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/GSS%20design%20variables.pdf, and GSS Methodological Report 137 on post-stratification weights, https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR137%20Poststratification%20Weights.pdf. Both cited via the `frontier_execution_2026_09_17/social` lane, which established the design contract reused here.
- American National Election Studies 2020 Time Series Study, public CSV release 20220210, and 2024 Time Series Study, public CSV release 20260519, with their user-guide codebooks. Local copies under `raw/`; obtained 2026-09-17 by the `attitudes_gen_2026_09_16` lane.
- Westwood, Grimmer, Tyler and Nall (2022), "Current research overstates American support for political violence", *PNAS* 119(12), https://doi.org/10.1073/pnas.2116870119.
- Abrajano and Alvarez (2009), "Assessing the Causes and Effects of Political Trust Among U.S. Latinos", https://doi.org/10.1177/1532673x08330273 — first-generation Latinos are more trusting of government than later generations, matching section B's trust result and contrasting with the generalised-trust result.
- Citrin, Lerman, Murakami and Pearson (2007), "Testing Huntington: Is Hispanic Immigration a Threat to American Identity?", *Perspectives on Politics*, https://www.cambridge.org/core/journals/perspectives-on-politics/article/abs/testing-huntington-is-hispanic-immigration-a-threat-to-american-identity/3FEF0D64DFC062082551717A1141F15E — finds patriotism growing generation to generation, consistent with section A5.
- World Values Survey wave 7 cross-national microdata, v6.0, study DOI https://doi.org/10.14281/18241.24, obtained 2026-09-18 via the Kaggle mirror `lauriszon/wvs-cross-national-wave-7` because the WVS site's download endpoint returns a one-byte body to plain HTTP; country-year list cross-checked against https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7&COUNTRY=, fetched 2026-09-18.
- Pew Research Center, Spring 2017 Global Attitudes democracy topline, https://www.pewresearch.org/global/wp-content/uploads/sites/2/2017/10/Pew-Research-Center_Democracy-Report-Topline-Questionnaire_2017.10.16.pdf, fetched 2026-09-18 — the second instrument in section C2.
- LAPOP / Vanderbilt Center for Global Democracy, 2026 AmericasBarometer *Pulse of Democracy*, https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf, fetched 2026-09-18 (narrative numbers only; the country bar charts are images and those percentages are [GAP]).
- Pew Research Center, National Survey of Latinos 2025 release, https://www.pewresearch.org/race-and-ethnicity/2026/07/09/u-s-hispanics-are-divided-on-whether-their-identity-helps-or-hurts-them-in-america/, fetched 2026-09-18 (design facts only; democracy and institutions items not located).
- Lane anchor file `infra/immigration-fiscal/norms_gen_2026_09_18/ANCHORS.md`, which holds the full Pew Spring-2017 topline tables, the WVS7 fieldwork and mode detail, and every route tried and failed.
- Prior lanes: `infra/immigration-fiscal/attitudes_gen_2026_09_16/RESULT.md` (loader, generation coding, ANES thermometer results), `infra/immigration-fiscal/frontier_execution_2026_09_17/social/RESULT.md` (weights, design variance, trust re-estimation).
- Confidence-ladder entries 87, 100, 107, 110, 112 and 117, `research/immigration-confidence-ladder.md`.

## Reproduction

All scripts in `infra/immigration-fiscal/norms_gen_2026_09_18/`, run with `UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3`.

| Script | Does |
|---|---|
| `norms_lib.py` | GSS loader, generation coding, stratified design covariance |
| `outcomes.py` | all 92 GSS outcome recodes with their sign conventions |
| `estimate.py` | weighted means and design-linearised WLS with arbitrary contrasts |
| `gate_var.py` | vectorised-versus-loop covariance gate |
| `gate_prior.py` | reproduction gate against the 2026-09-17 social lane |
| `gate_anes.py` | reproduction gate against the 2026-09-16 attitudes lane |
| `run_gss.py` | Part A, writes `derived/gss_raw_means.csv` and `derived/gss_adjusted.csv` |
| `cb_index.py` | extracts the ANES variable index from the codebook PDFs |
| `anes_spec.py`, `anes_norms.py` | Part B, writes `derived/anes_*.csv` |
| `lang_check.py`, `lang_anes.py` | interview-language disconfirmation |
| `mode_check.py` | GSS web-versus-interviewer mode test, 2022 and 2024 |
| `mex_synth.py` | Mexican-origin-only synthesis table |
| `ratio.py` | gap relative to the internal white spread |
| `wvs_recheck.py` | independent recomputation of the WVS7 anchors from the microdata |
| `make_tables.py` | regenerates every table in this memo from the CSVs |
| `verify_memo.py`, `verify_tail.py`, `verify_mode.py` | re-check every number quoted in this memo against the CSVs |

Derived outputs: `derived/gss_raw_means.csv`, `derived/gss_adjusted.csv`, `derived/anes_raw_means.csv`, `derived/anes_adjusted.csv`, `derived/gss_language_check.csv`, `derived/anes_language_check.csv`, `derived/gss_mode_check.csv`, `derived/gss_mode_difference.csv`, `derived/gap_vs_white_spread.csv`, `derived/item_coverage.csv`, `derived/gss_audit.json`, `derived/anes_audit.json`, `derived/cb_index.json`, `derived/tables.md`.

## Revisions

2026-09-18, first version. Extends confidence-ladder entry 87 from immigration, redistribution and trust to institutional confidence, civil liberties, rule-of-law and national-identity items, adds the white-subgroup comparators the earlier work lacked, adds ANES democratic-norms items, adds World Values Survey wave 7 origin-country anchors recomputed from microdata, and adds three measurement checks (two response-style instrument checks, an interview-language split in both surveys and a direct GSS web-versus-interviewer mode test) that qualify every generational comparison in the earlier lanes as partly a convergence in survey response behaviour. Does not revise the trust or redistribution findings of entries 87, 110 and 117; reproduces the trust estimate exactly as a gate.
