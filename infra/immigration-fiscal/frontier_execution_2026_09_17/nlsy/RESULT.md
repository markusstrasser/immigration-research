**Verdict:** The previous fixed percentile-to-SD conversion is unsupported. Public NLSY97 permits survey-design uncertainty, and the official benchmark is reproduced. The new public-family-history analysis shows a G2-to-G3 AFQT point increase whose confidence interval crosses zero, and no clear G3-to-G4+ reversal. A high-school-completion decline appears among fully classified respondents, yet a possible assignment of the unresolved-grandparent pool reverses its point ordering. Small crime cells do not establish parity or a generational trend. [SOURCE: calculations in audit.json, means.csv, contrasts.csv, classification_sensitivity.csv]

These are Mexican/Chicano **self-identification × reported generic family birthplace** groups. They are not a replication of restricted Mexican-country ancestry or measures of genetic fractions. G2 means U.S.-born with at least one foreign-born biological parent; G3 means U.S.-born with both biological parents U.S.-born and at least one foreign-born grandparent; G4+ requires all four grandparents reported U.S.-born. Unknowns are retained. The inherited own/grandparent questions include Puerto Rico/territories, while some parent items simply say U.S.; consequently these are questionnaire-specific family-history labels, not a fully harmonized legal immigration definition. [SOURCE: inherited family source audit and exact variable codebooks]

The measurement frame is this U.S.-resident youth cohort, ordinarily born 1980–1984, observed across subsequent interviews. Comparing generations within one cohort is not tracking a representative immigrant's children and grandchildren across time. Migrant selection, historical source populations, marriage patterns, recognition of ancestry, and selective follow-up can change group composition. [INFERENCE]

Original AFQT units and the published claim

Duncan, Grogger, León and Trejo's published Table 8 column 1 gives these adjusted differences from fourth-plus-generation non-Hispanic whites, in **AFQT percentile points**:

| Published group | Difference | Heteroskedasticity-robust SE |
|---|---:|---:|
| 1.5 generation | −31.75 | 2.54 |
| G2 | −24.98 | 1.76 |
| G3 | −17.72 | 2.53 |
| G4+ | −25.63 | 1.91 |

The model controls sex and age at testing, uses sampling weights, and has 3,833 observations. Its G3–G2 point difference is 7.26 percentile points; a difference SE cannot be reconstructed from the two reported coefficient SEs without their covariance. Footnote 23 starts with restricted biological-parent/grandparent country-region variables that identify Mexico, then supplements missing cases from public U.S.-birth indicators. The public analysis here uses a different identification rule and no corresponding regression controls. [SOURCE: [published paper, Table 8 and footnote 23](https://pmc.ncbi.nlm.nih.gov/articles/PMC10836839/)]

R9829600 is the NLS-created four-subtest math/verbal summary percentile, normalized within birth-quarter groups, stored with three implied decimals. It is not a normally distributed raw AFQT or IQ score. A universal conversion such as one percentile point = 0.028 SD has no defensible basis. [SOURCE: [official ASVAB guide](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/administration-cat-asvab), selected_codebook.json]

Two explicitly named individual-data alternatives are supplied: percentile-rank SDs relative to the observed baseline-white G4+ group (mean 59.1719, SD 26.9835, n=1,840), and normal scores of the full AFQT sample's weighted empirical midranks. The first produces Mexican self-ID G2/G3/G4+ means −0.901/−0.713/−0.707 reference percentile-SDs. The second produces −0.499/−0.302/−0.371 normal-score means. These transformations answer different distributional questions; neither estimates latent IQ, and the reference transform is held fixed for its descriptive SEs. Original percentiles remain the principal result. [SOURCE: individual observations, analyze.py; audit.json]

Adult outcomes and direct uncertainty

All following rows are both sexes, Mexican/Chicano self-ID. Entries give estimate (valid n). Each direct interval includes covariance from the public survey design.

| Measure | G2 | G3 | G4+ | G4+ minus G3, 95% CI |
|---|---:|---:|---:|---:|
| AFQT percentile | 34.85 (332) | 39.94 (97) | 40.10 (121) | +0.16 [−8.24, +8.57] |
| Regular HS or higher, 2013 | 82.99% (278) | 88.01% (86) | 78.12% (110) | −9.90 pp [−18.73, −1.06] |
| BA or higher, 2013 | 17.35% (278) | 22.54% (86) | 20.02% (110) | −2.53 pp [−14.46, +9.41] |
| 2012 annual job wages, known zeros included | $31,151 (256) | $31,425 (80) | $35,150 (106) | +$3,725 [−$6,769, +$14,219] |

The AFQT G3–G2 contrast is +5.09 points [−1.83, +12.00]. Exploratory multiple outcomes were inspected, so the high-school interval should not be promoted into a preregistered discovery. Wide intervals around the other outcomes do not establish equivalence. [SOURCE: means.csv, contrasts.csv]

Within G2, one foreign-born plus one U.S.-born parent yields AFQT 41.02 (n=99), versus 31.04 (n=188) with two foreign-born parents: +9.98 [3.62, 16.34] points. The other-parent-unknown subgroup is separate: 32.17 (n=45). Thus a single G2 label hides substantial composition. These differences cannot identify a causal effect of intermarriage or a genetic dose. Education and earnings splits, both sexes separately, remain in the full tables. [SOURCE: means.csv, contrasts.csv; interpretation INFERENCE]

Degree is T8129600, from the 2013 interview. Code 1 is GED, 2 regular diploma, 3 associate, 4 BA, 5–7 higher degrees; the principal HS measure excludes GED and a GED-inclusive sensitivity is provided. T8976700 covers **2012 job wages**, not 2013/2015 wages, hourly pay, family income, or all self-employment income. Known nonreceipt T8976500=0 is assigned zero; refused/unknown wage amounts remain unknown. Top 2% wage values are replaced by their group mean, limiting tail analysis. T8135900 supplies 2013 interview weights. [SOURCE: audited_selected_codebook.json in the source lane]

What could reverse the narrative

Self-ID is collected in ASVAB origin/descent items R97023–R97025. All 897 Mexican/Chicano-identified respondents have AFQT, versus 3,582 of 4,334 in the baseline-white comparison category. This is joint identity/assessment selection, not evidence that all Mexican-origin participants were successfully assessed. People without that self-ID cannot be silently counted as having no Mexican ancestry. Exact generation remains unresolved for 242 of the 897 (177 unresolved own/parent generation; 65 U.S.-born/U.S.-parents but unknown grandparent status). [SOURCE: codebook ASVAB on-line questionnaire item 23; audit.json and family rows]

The known-U.S.-parent/unknown-grandparent pool has regular-HS+ 53.23% among 46 observed outcomes (65 baseline respondents). Its AFQT mean is 39.60. Assigning all of this pool to G3 changes G3/G4+ HS rates to 75.64/78.12%; assigning all to G4+ gives 88.01/71.26%. In a sensitivity split that assigns the same fraction of every pool outcome and weight to G3 and the rest to G4+, the HS point ordering reaches equality at **85.74% allocated to G3**. This is a scenario, not an estimate of their ancestry or a full worst-case bound. Both assignments preserve known U.S.-born parents. [SOURCE: classification_sensitivity.csv and classification_tipping_points.csv]

Changing among the justified parent-mapping sources leaves the classified HS contrast near −10 points; supplement-only classification produces tiny, highly selected samples. Thus the known mapping sensitivity is smaller than the missing-grandparent uncertainty. [SOURCE: classification_sensitivity.csv]

Separate retention bounds hold family classification fixed and use original baseline weights. For regular HS+, fully observed plus retained outcomes give baseline-completion bounds of 77.24–89.32% for G3 and 69.11–80.06% for G4+. Equality is possible, for example, if missing G3 outcomes have 20% HS completion and missing G4 outcomes about 96.28%. This is a demanding differential nonresponse scenario. Equal missing-group outcome rates do not erase this particular HS difference. These bounds address finite baseline-weight outcome completion, not unknown identity or unknown family classification, and are not the same estimand as the main later-wave-weighted means. [SOURCE: completion_bounds.csv, retention_tipping_points.csv]

Common-age crime does not resolve the small-cell problem

The official monthly histories start at age 12. We evaluate status in the month immediately before the 30th birthday, so follow-up age is common. Status 99 preserves a previous event; negative missing codes are never converted to no event. Arrest zeros with an undated reported arrest are excluded. Incarceration refers to jail/adult correctional facilities and excludes juvenile detention; dates may be imputed. The incomplete-history flag has a separate exclusion sensitivity. [SOURCE: [official event-history definitions](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/crime/crime-delinquency-arrest)]

An independent first-date check found three contradictions: one incarceration and two arrest records have a first date between age 12 and the cutoff but zero monthly status at the cutoff. These derived statuses are unknown; none belongs to the Mexican self-ID group. Four additional arrest differences are correctly explained by events before age 12. [SOURCE: timing_crosscheck.json]

Review also identified 11 incarceration-array zeros with an invalid first date (`E8043000=-3`); seven have positive 2023 weights, all in the other/unresolved identity category. These now remain unknown before the incomplete-history sensitivity is computed. Valid skip `-4` is preserved as the distinct no-incarceration route. The focal Mexican/white contrasts are unchanged. [SOURCE: held primary codebook, timing_crosscheck.json, independent review and rerun.]

| Mexican self-ID men | G2 | G3 | G4+ |
|---|---:|---:|---:|
| Adult-facility incarceration, age 12 to before 30 | 14.74% (16/113) | 14.71% (7/46) | 10.56% (7/46) |
| Arrest, age 12 to before 30 | 40.90% (49/113) | 49.20% (22/46) | 43.77% (21/45) |

Numerators/denominators are unweighted events/valid respondents; rates use 2023 interview weights and hence condition on retention to that wave. The G4–G3 incarceration contrast is −4.15 pp [−17.71, +9.41]; the arrest contrast is −5.43 pp [−25.31, +14.45]. Cumulative reported incarceration yields 16.67/17.30/14.57%, with G4–G3 −2.73 pp [−18.48, +13.01]. Neither analysis establishes parity or a monotonic trend, and neither equates arrest/incarceration with offending. [SOURCE: means.csv, contrasts.csv]

Validation and scope

The public design variables R1489700/R1489800 supply 117 strata and 234 pseudo-PSUs. Taylor linearization retains the full design grid for domain comparisons, uses the difference's influence function including covariance, and uses 117 degrees of freedom for t intervals. The principal benchmark gives AFQT n=7,093, mean=50.4099446909 and design SE=0.6376813718, reproducing official 50.410/0.638. These SEs cover sampling design, not missingness, misclassification, or model search. [SOURCE: [official design guide](https://www.nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects), audit.json]

The independent CSV/scalar checker reproduced 612 cells of means, direct contrasts and completion bounds, plus 20 feasible classification tipping-point equalities, without importing the analysis functions. It computes variance independently as the sum of squared within-stratum PSU influence differences. All 8,984 IDs and four overlapping adult variables match the sibling source cache exactly. [SOURCE: verification.json]

Files covered: verified family classifications, the earlier 98-field extract, the 806-field score/design/timing extract streamed from the full NLS archive, and the adult profile source parquet. Files skipped: Pew/ICPSR (other lanes), restricted geography/country variables (not held), broader crime-offending questions (changing questionnaire universes), causal wage/education models and genetic interpretations (not identified here). No original files were mutated. [SOURCE: manifest.json]

Leading explanation: the single generational-progress narrative mixes outcomes and selection mechanisms. Alternative: there is a true fourth-generation disadvantage obscured by noisy public self-ID definitions. Falsifier: a country-specific ancestry reanalysis with documented treatment of nonidentifiers and missing grandparents, followed by the same common-age outcomes and design-aware contrasts, could restore a consistent decline. Impact: withdraw the synthetic IQ-SD assertion; retain original published percentile results and separate our public descriptive evidence; qualify even the HS decline by the demonstrated classification sensitivity. Next action: use restricted country linkage if obtainable, or lead with the public source-tagged family-history/self-ID taxonomy and explicitly unresolved groups. [INFERENCE]

Instrument check: this synthesis is LLM-assisted; primary variable definitions, an official numeric benchmark, explicit competing interpretations, and independent arithmetic constrain its politically sensitive interpretation. They do not make the residual framing choices neutral.
