# Adversarial audit of the September 16–17 conclusions

**Verdict:** The new results contain useful evidence, but all five summaries overstate at least one inference. Retain the measured disability gradient and evidence that labor supply changes technology choices. Withdraw the political dollar bounds, the Central Valley composition percentage, and claims that imprecise nulls establish no effect. Better measurement of family migration history is central to interpreting the generational results.

Date: 2026-09-17. Scope: commits `f74ac66`, `eb1b9a5`, `cd2209b`, `9b5d1c4`, `6ead04c`; ladder entries 93–97 and their source lanes. This is an adversarial brief, not a complete re-audit of the fiscal ledger or earlier crime estimates. The frame is descriptive accuracy first, causal effects second, incumbent welfare third; these are different questions. This LLM-assisted assessment can have framing biases; its corrections rest on source definitions, numerical checks and explicit counterexamples. [SOURCE: audited commits and files below]

## 1. What survives, and what changes

| Conclusion | Survives | Correction |
|---|---|---|
| Native fertility | The archived estimates reproduce using the old code | Correcting age bins changes the weighted cross-section from −0.270 to −0.168. Neither it nor the imprecise fixed-effects result establishes no crowd-out |
| Automation | More low-skilled labor can reduce automation adoption/invention; H-2B winners invest more in the short run | Total investment, private farm value, automation intensity and national welfare are different outcomes. The welfare objection remains unresolved |
| Disability | Mexican second-generation adults have substantially more reported disability than Mexico-born adults | Complete loss of the advantage relative to whites is unproven; second-generation disability-income dollars are below whites at the point estimate |
| Crime/agglomeration | The proposed Mexican-origin dollar estimate is not supported | A wide productivity interval and rising residential population do not refute a productivity spillover |
| Political backlash | Immigration can change voting, with heterogeneous signs | The $1,300–$43,000 range is an assumption-driven scenario, not a bound. Its positive lower endpoint is unsupported |

These corrections do not establish the opposite policy verdict. They distinguish an unpriced effect from a measured zero. [INFERENCE]

## 2. Fertility: uncertainty and implementation defects

The stored two-way fixed-effects regression reproduces at −0.04257 (SE 0.25982), approximately **[−0.552, +0.467]** at 95%. Units: additional native women reporting a birth in the previous 12 months per 1,000 native women aged 15–50, per percentage point of the foreign-born population share. The −0.269 CIS cross-sectional estimate lies inside this interval. A five-point increase is compatible with about **2.76 fewer to 2.33 more birth-reporting women per 1,000**, under this model's variance assumptions. This is not an equivalence result or a causal confidence bound. B13008 counts women reporting a birth, not babies or completed fertility. [DATA: `infra/immigration-fiscal/native_fertility_2026_09_16/{fe_panel.csv,panel_fe.py}`; SOURCE: https://api.census.gov/data/2023/acs/acs1/groups/B13008.json]

Independent diagnostics using the stored panel give −0.300 (SE 0.333) for 2010–2019. The baseline model's own rent coefficient is negative, −9.86 (SE 4.88), so “the second link is missing” is not an accurate description of that fitted model. Neither coefficient identifies a rent-mediated causal effect. Controlling for rent could remove part of the very total effect being investigated. [DATA; INFERENCE]

Implementation defects found in the scripts:

- The age-control indices represent roughly women 18–29 / women 15–45, although the prose calls the measure women 20–34 / women 15–50. Correcting the indices in a diagnostic rerun gives −0.093 (SE 0.258); the substantive uncertainty remains.
- The origin instrument matches B05006 variable **codes** across 2010 and 2023, although 115 of 136 reused labels differ. A position in the table is not a stable country identifier.
- Its allocation uses a metro's share composition rather than each origin's base distribution across destinations. The appropriate mechanical allocation is `base metro-origin / base total-origin × total-origin change`, divided by base metro population. A sum across observed metros must be labeled as that coverage, not a nationwide inflow.
- Pandas' default sum converts an entirely missing origin row into zero predicted inflow. Missing exposure is not zero exposure.
- 2021 ACS one-year estimates exist; the omission is not explained by their nonpublication. Two CBSA-code substitutions do not harmonize changing county membership or Connecticut's geography.

The 432 areas also include micropolitan areas. Numerical agreement with the CIS coefficient is not an exact specification replication: the repo uses different controls and labels native-women weights as population weights. CIS's detailed specification was recovered from its indexed primary methods passage; its full page was blocked, so this is a scoped specification check. [SOURCE: https://cis.org/Report/Fertility-Among-Immigrants-and-NativeBorn-Americans; `analyze.py`]

**Completed repair and rerun:** both age-control callers now share one definition. From cached raw inputs, corrected 2015–19 top-50 coefficients are −0.2053 (SE 0.0923) with controls and **−0.1683 (SE 0.0950)** with native-women weights. The prior −0.270 agreement with CIS depended on the wrong age bins. Corrected annual FE is **−0.0930 (SE 0.2578), interval [−0.598, +0.412]**; native-women-weighted FE is +0.1213 (SE 0.2048). The full corrected IV diagnostic has n=26 and F≈2; causal 2SLS is explicitly disabled. Analyses rebuild source panels rather than consume stale derived CSVs. Original tracked outputs remain pre-audit snapshots, clearly superseded here. [DATA: isolated raw-cache reruns of corrected `build_panel.py`, `analyze.py`, `panel_fe.py`; regression checks in `infra/immigration-fiscal/tests/test_native_fertility.py`]

[SOURCE: `analyze.py`, `build_panel.py`, `panel_fe.py`; Census B05006/B01001 metadata for 2010 and 2023; https://www.census.gov/programs-surveys/acs/news/data-releases/2021/release.html]

After country-label matching, correct allocation and exclusion of missing origins, a diagnostic retains only 26 of 232 metros and gives first-stage F≈2.04. It supplies no usable causal estimate. The original “weak, wrong-sign IV” is therefore an implementation failure as well as an identification failure, not evidence about Mexican migration's economic response. [DATA]

**Better evidence:** a fixed-county-geography panel with complete years, clearly separated total-effect and mechanism regressions, age-specific native fertility, and a defensible migration shock. NVSS natality counts are a better birth-event outcome; the corresponding native-woman denominators still require measurement. Local residence changes, postponement versus completed fertility, and national effects remain separate questions. [INFERENCE: recommended analysis, not a completed replacement estimate]

## 3. Automation: a stronger mechanism, an unresolved welfare consequence

**San's paper explicitly does not estimate aggregate welfare.** Bracero exclusion induced innovation and reduced exposed farm values. Section VI, footnote 31, allows off-farm productivity, price and knowledge-spillover benefits to offset or reverse landowners' losses. Consequently, falling farm values reject the claim that the affected owners benefited; they do not refute an aggregate innovation externality. The converse also holds: the paper does not establish that those spillovers were large enough. [SOURCE: Shmuel San, 2023, https://mulysan.github.io/San_bracero.pdf, pp. 159–160, DOI 10.1257/app.20200664]

Clemens–Lewis' H-2B lottery measures firms' short-run outcomes, including spending on occasional equipment or real-estate investments. More workers can increase total investment through expansion while reducing machinery per worker or incentives to invent labor-saving technology. Its positive investment elasticity cannot settle that different question. Sections 5.2 and 9 discuss the short follow-up, sector coverage and general-equilibrium limits. [SOURCE: May 2024 revision of https://www.nber.org/papers/w30589; local full text `sources/immigration-fiscal/data/external/lifetime/nber/clemens_lewis_2022_low_skill_immigration_restrictions_w30589.pdf`; INFERENCE]

**The published Danzer–Feuerbaum–Gaessler article strengthens the mechanism evidence.** A 10% increase in the low-skilled workforce is associated with about a 3.3-point reduction in the automation-patent share, or 2.5 fewer automation patents annually in the average region. Section 5.2 tests patent counts directly, contrary to the old lane's “share not level” limitation. The effect peaks in year four and annual flows subsequently return toward zero; that does not show the missing inventions were caught up. It still supplies no monetary social-welfare estimate. [SOURCE: published 2024 article, sections 5.1–5.2, https://edoc.ku.de/id/eprint/33404/1/1-s2.0-S0047272724000720-main.pdf, DOI 10.1016/j.jpubeco.2024.105136; INFERENCE on flows versus accumulated knowledge]

The “two thirds compositional” Central Valley finding is invalid. It compares all-resident **mean per-capita income** with **median income among people aged 15+ with income who were born in their present state**. Subtracting these gaps is not a decomposition; state-born people are not a longitudinal incumbent cohort. The BEA series itself reproduces: Valley/US per-capita income is 0.9664 in 1970, 1.0237 in 1980, 0.7305 in 2000 and 0.7588 in 2024. Composition's contribution remains unquantified. [DATA: `bea_sjv.py`; SOURCE: https://data.census.gov/table/ACSDT5Y2023.B06011; https://apps.bea.gov/regional/zip/CAINC1.zip]

The broad “no enforcement paper studies technology-related firm adjustment” claim also fails: Ifft–Jodlowski's 2022 *Is ICE freezing US agriculture?* reports farm adjustment, including fuel expenses interpreted as mechanization. **Abstract-only verification:** fuel is a proxy; a direct capital-stock/robot-adoption effect was not verified. [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S092753712200094X, DOI 10.1016/j.labeco.2022.102203]

**Better perspective:** ask whether immigration changes the social value of future innovation, allowing for output expansion, other inventions, investment costs and benefits to consumers. Four quantities must stay distinct: total investment, automation per worker, invention flows/knowledge stocks, and welfare. [INFERENCE]

## 4. Disability: real attenuation, not demonstrated disappearance

The original estimator was rerun against the 142,125-person 2025 ASEC file with its 160 replicate weights. Age-standardized disability rates reproduce. Direct differences use replicate-level contrasts, not independent-group approximations. Reference ages are fixed at the full-sample white distribution, as in the original estimator. [DATA]

| Adults 25–64, age standardized | Prevalence | Difference from third-plus NH whites, approximate 95% interval |
|---|---:|---:|
| Mexico-born | 4.49% | — |
| Native with a Mexico-born parent | 8.61% | −1.20 points [−2.88, +0.47] |
| Native, native parents, Mexican self-ID | 11.27% | +1.45 points [−0.34, +3.24] |
| Third-plus NH whites | 9.82% | Reference |

The second-minus-first contrast is **+4.12 points [2.32, 5.92]**. That attenuation is supported. Complete parity with whites is not: the second-generation interval still permits a substantial advantage. The third-plus excess is also uncertain. The script's all-origin second-generation group retains a statistically supported disability advantage, independently defeating the broad “first-generation only” headline. [DATA: `disability_by_generation.py`, both output CSVs, independent direct-contrast rerun]

The second-generation total disability-income point estimate is **$942 versus $1,030** for whites, approximately −$87 after unrounded subtraction. “At or above white” and “no US-born line below white” contradict the source table. Moreover, the aggregate includes private disability/insurance payments and cannot itself be called government fiscal expenditure. [SOURCE: lane RESULT table; https://api.census.gov/data/2025/cps/asec/mar/variables/DIS_SC1.json]

BLS explicitly cautions against directly comparing disability prevalence across surveys with different universes, context, wording and modes. The CPS–ACS discrepancy establishes neither failed replication nor an upper bound on a latent true advantage. The SSI-under-65 eligibility check and Social Security disability reason code do survive the audit. [SOURCE: https://www.bls.gov/cps/cpsdisability_faq.htm; https://api.census.gov/data/2025/cps/asec/mar/variables/RESNSS1.json; https://www.ssa.gov/ssi/text-eligibility-ussi.htm]

These are contemporaneous groups from different birth and immigration cohorts, not successive observations of the same families. Age standardization does not establish a causal intergenerational loss. Health-selective ethnic attrition is directly documented in Antman–Duncan–Trejo: some healthier descendants cease identifying as Mexican. Their mostly child/self-rated-health analysis does **not** supply a correction factor for our adult disability measure. [SOURCE: https://spot.colorado.edu/~antmanf/AntmanDuncanTrejo-HealthEthnicAttrition.pdf, sections I–II; INFERENCE]

**Next useful measurement:** multiple ASEC years with overlap-aware uncertainty; report direct generation contrasts and intervals, one-versus-two immigrant parents, sex and birth cohort; keep public and private income distinct. Parenthood/education controls should answer named conditional questions rather than silently remove part of the pathway being studied. [INFERENCE]

## 5. Agglomeration: the dollar transfer fails, but several rebuttals also fail

The replication package's `output/accounting.txt` reports earnings per job **+0.4 log points, SE 2.9**. Its approximate 95% interval is **[−5.28, +6.08]**, which includes both the −2.01 imputation at elasticity 0.05 and −2.77 at 0.069. Thus its “precise-ish zero with the wrong sign” is not a statistical rejection of the modeled loss. An insignificant coefficient remains an estimate; selecting the smallest specification does not establish a lower bound. [DATA: archived package `agglom_crime_2026_09_17/_cache/pkg/replication/agglomeration_crime_replication/output/accounting.txt`, lines 1–5; package https://osf.io/xzfdw/]

Three additional problems with our rebuttal:

1. Residential tract population is not the package's **employment-weighted job density**. A tract can gain residents while employment redistributes across a metro. A positive net effect also does not rule out a negative component relative to an otherwise identical inflow without that component.
2. Rising aggregate rents can coexist with local amenity losses and slower relative appreciation. Saiz–Wachter's own published abstract describes the latter. Therefore “land prices must fall” and “cannot coexist with rent increases” are false general restrictions.
3. Direct victim costs, avoidance costs and productivity externalities can overlap, but are not automatically the same item. Establish overlap from the valuation method before claiming double counting. Voluntary avoidance of crime can improve welfare relative to staying in danger while still imposing a cost relative to a safe-city counterfactual.

[SOURCE: package outcome definition; https://www.aeaweb.org/articles?id=10.1257/pol.3.2.169; INFERENCE: counterexamples and accounting distinctions]

Conversely, the proposed Mexican-origin scaling remains unjustified. It substitutes institutionalization ratios into a homicide calculation and transports a historical migration response to a different population and period. Our lane alternately calls the resulting sensitivity $0 to −$1,700 and −$1,700 to −$3,200. None is an identified bound. Use **unestimated / excluded from the sum**, not a measured $0. [SOURCE: lane RESULT §§E–G; INFERENCE]

**Better evidence:** a directly matched origin/age-specific crime measure, workplace density and relocation, and productivity measured on the same fixed geography; an explicit counterfactual separating population expansion from crime-induced sorting. No reviewed source delivers this full chain for Mexican-origin descendants. [INFERENCE; scoped search result]

## 6. Political costs: withdraw the range

The restrictionist mechanism is coherent: an immigration policy could change electoral outcomes and thereby change other policies. Moral responsibility and causal consequences are different questions. But “Republican voting” across 1990–2016 is not synonymous with “populist government,” and none of the cited electoral results directly prices the relevant policies. The MPS published abstract supports skill-dependent voting effects and heterogeneity; its full published coefficient/counterfactual was not independently recovered in this audit. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/app.20190081; FRAMING-SENSITIVE; INFERENCE]

The range is constructed by assigning one entire presidency to an assumed ten million immigrants, assigning it $0.5T–$17T of losses, and dividing by forty years. It does not constrain the actual immigration-attributable change in government probability, the policies another government would have enacted, the net value of all policy changes, or the correct migrant exposure denominator. Consequently, neither endpoint is an empirical bound; a positive lower bound has not been established. Dividing a discounted present value by forty also does not produce a comparable discounted annual equivalent. [SOURCE: `backlash_cost_2026_09_17/RESULT.md`, THE JOIN; INFERENCE]

The proposed rescue—using an author's national counterfactual—cannot automatically cure the local-to-national assumptions when that counterfactual is composed from those same local coefficients. This needs verification, not a citation-based exemption. Likewise, “the estimate is too large, therefore wrong” is not an evidential test. Large effects require better scrutiny, not rejection by surprise. High anti-immigrant voting in low-immigration places is compatible with a positive within-place effect because baselines and confounding differ. [INFERENCE]

There is also no warrant for turning one historical paper's positive employment effect and culturally patterned backlash into proof that every affected native suffered no material harm. The survey literature contains economic and cultural mechanisms, plus opposite electoral effects under different contact conditions. The accessible Alesina–Tabellini 2021 working-paper version reviews these distinctions; the final 2024 publication's identity was checked, but that full version was not recovered. [SOURCE: https://docs.iza.org/dp14354.pdf, §§3–4; https://www.aeaweb.org/articles?id=10.1257/jel.20221643]

**Better perspective:** estimate immigration → actual officeholding/policy changes in a named institutional setting, then value the relevant policy outcomes. Keep admission composition, electoral institutions, communication and integration policies explicit. “Unpriced political externality” survives; “defensible $1,300–$43,000” does not. [INFERENCE]

## 7. A better non-racial classification: family migration history

**Recommendation, not an adopted change to the research protocol:** record places and timing of birth along the family tree, with ethnic self-identification as a separate variable. No genetic test is needed. “One of four grandparents was born in Mexico” measures a family migration connection; calling this “25% genetically Mexican” substitutes a different, unsupported construct. It also misses older Mexican-origin branches whose grandparents were already US-born. [INFERENCE]

| Record | Useful summary |
|---|---|
| Own birthplace and age/year of arrival | Adult-arriving immigrant, child-arriving immigrant, or US-born; retain actual arrival age |
| Both parents' birthplaces | US-born with one or two Mexico-born parents; retain the other parent's origin |
| All four grandparents' birthplaces, unknowns explicit | Exact third generation on a Mexican branch; one, two, three or four Mexico-born grandparents |
| Birth/arrival cohort and childhood residence | Separates generation from period, cohort and upbringing |
| Household language, parental education/income and legal history where observed | Candidate mechanisms, not ingredients that redefine ancestry |
| Respondent's identity, separately recorded | Can test who changes labels instead of losing them from the descendant group |

Keep mixed histories visible. Someone with a Mexico-born parent and an Italy-born grandparent has connections to both countries at different generations. A closest-immigrant-ancestor rule can supply one overall generation label, but it discards information; origin-specific records should remain available. When summing fiscal costs across origins, use mutually exclusive combinations or explicitly declared fractional accounting weights. Do not count the same person fully several times. Such weights are conventions, not genetic measurements. [INFERENCE]

**Why this matters empirically:** Duncan et al. use NLSY97 to distinguish exact third generation from fourth-plus. In their study, about 88% of third-generation Mexican-origin respondents had one or two Mexico-born grandparents; they averaged about 1.8 more years of schooling than those with three or four. This is a descriptive family-background difference, not evidence of a genetic dose effect. Separating exact third generation reveals educational progress hidden by third-plus pooling. Their fourth-plus category still depends on identity, so even this design does not identify all remote descendants. [SOURCE: https://docs.iza.org/dp12704.pdf, §2, §5 and Table 14; published record https://doi.org/10.1016/j.labeco.2019.101771]

**Data access determines what is feasible.** CPS records respondents' and parents' birthplaces, so one/two-parent splits are available without race. Its ordinary adult records do not give a complete four-grandparent country history. Family links can recover some history for co-resident children, with selection limits. NLSY97's public data identify US/territory versus foreign-born grandparents; detailed countries require restricted geocode data. The published researchers' country-specific result therefore does not prove we can reproduce it from a public extract. [SOURCE: https://cps.ipums.org/cps-action/variables/FBPL; https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/household/race-ethnicity-citizenship; Antman et al. methods]

More precisely, the NLSY97 paper uses restricted birthplace **regions with Mexico separately identified**; do not promise a distinct code for every country. Its three- and four-Mexico-born-grandparent cells contain only 8 and 13 people. GSS `GRANBORN` counts foreign-born grandparents without their countries. CPS can recover a child's grandparents from co-resident **parents'** parent-birthplace answers; the grandparents need not live there, and unobserved branches stay missing. One known Mexico-born grandparent plus two unknown branches means a possible count of one to three, not exactly one. [SOURCE: Duncan appendix footnote 23 and Table 14; https://sda.berkeley.edu/sdaweb/docs/gss21rel3/DOC/hcbk0032.htm; https://cps.ipums.org/cps-action/variables/MOMLOC; INFERENCE]

Villarreal–Tamborini's 2024 linked CPS–SSA earnings study is a useful design example, with childhood family links and adult earnings follow-up. Its exact-third-generation finding is **Hispanic-wide**, not a Mexican-specific replication. Single-parent households observe only two grandparent branches, and the data require restricted access. This qualifies the neighboring ladder-92 claim's Mexican-specific corroboration; it does not re-audit the paper's earnings regressions or the separate return-migration claim. [SOURCE: methods and endnotes 6, 13 and 16, https://pmc.ncbi.nlm.nih.gov/articles/PMC11784596/, DOI 10.1093/sf/soad128; full relevant text checked by the classification lane]

For the present CPS outputs, use the literal label **“US-native adults with US-native parents who identify as Mexican”**, not “all third-generation Mexican descendants.” For crime, do not graft CPS parental-generation categories onto ACS institutionalization records that cannot identify those same generations. Changing the comparator to all otherwise eligible native-born residents removes a racial benchmark; age/cohort/location matching then answers a specified conditional comparison. It does not turn ancestry into a randomized treatment. [INFERENCE]

## Verification and scope record

- Independent lanes inspected fertility scripts/outputs, disability code/raw ASEC/replicate weights, and automation source papers/BEA series. Parent read each lane report and checked the critical source passages: San footnote 31; published Danzer §5.2; original package accounting output; original disability income table; fertility instrument code; NLS official access documentation and Duncan definitions/results.
- Citation checker resolved all eight DOI identifiers with matching titles and no hallucinated/unreachable entries. Fertility's three regression checks test age-bin boundaries/missingness, changing origin codes and conservation of allocated growth while preserving missing exposure; compilation and complete isolated source-cache reruns passed. These validate the repaired arithmetic, not geographic comparability or causal identification.
- Successful primary routes: author/institutional PDFs, Census/BLS/NLS documentation, local raw inputs and archived author code/output. AEA, Harvard, PMC and some publisher endpoints blocked full text; available manuscripts were version-labeled, and inaccessible sources were not promoted to verified full-text evidence.
- Disconfirmation of this audit: the disability first-to-second difference is statistically clear; BEA decline reproduces; H-2B short-run investment complementarity remains real evidence; San's results do weigh against benefits to affected owners. None is erased by the broader inference corrections.
- Deferred: a fully harmonized fertility panel/credible IV, a full fiscal rebuild, complete ancestry-linked adult crime/disability estimates, re-estimation of the agglomeration package from its external raw data, and verification of every political paper. These require new data/design work rather than another reading of the same headline. The classification above is a proposal, not a silent ontology or causal-tree change.
- Source-search anchors: exact source titles/DOIs; `Saiz Wachter 0.134`; `Alesina Tabellini political effects immigration`; `NLSY97 grandparents birth country`; `Hispanic Men's Earnings Mobility`; `Is ICE freezing US agriculture`. Search snippets located sources; full text or source records supported the scoped claims above.

## Revisions

- 2026-09-17 — Created; [decision](../decisions/2026-09-17-new-conclusions-inference-audit.md) records the withdrawals and retained findings.
