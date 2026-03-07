1. Executive Verdict
   • The repo’s current next-node is directionally right but too binary. The real fork is not just school-exit sorting vs measurement/process artifact. It is documented score-surface non-equivalence + school-exit sorting + observability/missingness. Official NLSY97 docs already tell you the surface is unusual: adaptive power subtests, non-adaptive rate-scored speed tests, an “easy” start form for 1983/84 births, and NLS-created internal math/verbal percentiles. ￼ ￼
   • The local Stage A update is real as a robustness warning and overstated as a causal explanation. You can now say the raw NLSY97 female quantitative edge is fragile. You cannot yet say the cause is “probably process/measurement” with high confidence. The strongest local result is process_core: same-sample base +0.037 to adjusted -0.041; but in the school-heavy subsets the same-sample base is already near zero or negative before adjustment. ￼
   • The biggest local flaw is bad control logic. Recent grades, grade-at-test, course/exposure proxies, effort, items completed, and posterior variance are not clean confounders for sex → score. Several are mediators or descendants of the score-generating process itself. Schooling also causally shifts AFQT-like scores, so treating school-exposure variables as nuisance controls is backwards. ￼
   • The most damaging omission is that I do not see a clean audit of the documented NLSY97 design features most likely to matter: age at test / birth cohort / easy-form assignment / internal age-group scoring, while the reported Stage A tables do include downstream precision and completion variables. That is upside-down. ￼
   • A simple “CAT favored girls” story is weak. In the ASVAB CAT-vs-paper equating study, female differences on AFQT and VE were non-significant; the notable female differences favored paper on PC and Auto/Shop, not CAT. So H1 survives as surface non-equivalence, not as “computer adaptive testing gave girls a free lunch.” ￼
   • Best current probabilities: H1 0.36, H3 0.20, H4 0.18, H2 0.16, H5 0.10. Read that as: the leading cluster is still score-surface/process, but missingness/selection is too large to demote, and school sorting is live but currently underidentified.
   • The single best next move is not external. It is within NLSY97: use PIAT Math + transcript/honors/course data to test whether the female edge is CAT-surface-specific inside the same cohort. The official NLSY97 docs explicitly point you there. ￼
   • Best external stack: HSLS:09 and ELS:2002 for H2; TIMSS 2019/eTIMSS and PISA 2018 for H1/H3; PIAAC log files for adult reconciliation. PISA 2022 is useful, but weaker than the repo assumes for public process analysis: the public index I found lists cognitive item data and questionnaire timing, but not the cognitive time/visits file that OECD lists for 2015 and 2018. ￼

2. Fatal or Major Problems

3. Construct compression is doing fake work.
   “NLSY79 quantitative,” “NLSY97 quantitative,” and “PIAAC numeracy” are not one latent object with three labels. NLSY97 uses adaptive MAP/Bayes scores for power tests, non-adaptive rate scores for Numerical Operations and Coding Speed, and an NLS-created math/verbal percentile the documentation says is not DoD-endorsed. PIAAC numeracy is adult mathematical literacy in context. Treating these as interchangeable is the repo’s largest conceptual error. ￼

4. The Stage A “process” block is not a hygiene block.
   It includes variables like numerical_operations_items_complete and coding_speed_items_complete. Those are descendants of performance on the two speeded, female-leaning surfaces, not exogenous test-room dust. Using them to explain away an AR/MK-based quantitative score is a classic overcontrol trap wearing a fake mustache. Official ASVAB docs say NO and CS are non-adaptive speed tests scored with rate formulas; they are not neutral metadata. ￼ ￼

5. Same-sample movement is already doing a lot of the sign flip.
   In the local report, the raw +0.054 becomes +0.037 in process_core, -0.007 in school_core, and -0.010 in process_plus_school_core before adjustment. So the story is not “the controls revealed the truth.” Part of the truth is that the analyzable subsets are different populations. H4 should be upgraded. ￼

6. The wrong design features are being foregrounded.
   Official NLSY97 docs flag the easy-form start for the youngest respondents and age-structured score construction. Economists who compare NLSY79 to NLSY97 treat mode and age-at-test as major comparability problems. Yet the current local narrative foregrounds posterior variance and room quality more than birth cohort/easy form/age. That is causally inverted. ￼

7. The external DOE is slightly pointed at the wrong PISA.
   For public process work, PISA 2018 is stronger than PISA 2022 because OECD’s public index explicitly lists cognitive total time/visits files for 2015/2018, while the 2022 public page I found lists cognitive item data and questionnaire timing but not those cognitive time/visits files. The repo should stop acting like “PISA 2022” and “public timing/process” are the same thing. ￼

8. Best Current Causal Read

Inference, not direct fact. Local PIAAC results keep a broad adult male numeracy pattern alive across countries, education, age, and occupation, which caps how high H5 can go. ￼ ￼

Hypothesis P(cause) Why it currently survives Top alternative Falsifier Decision impact
H1 score-surface non-equivalence 0.36 Official CAT-ASVAB/NLSY97 scoring surface differs sharply from NLSY79 and PIAAC; local flip is concentrated in MK-like/constructed surfaces, not a stable all-math pattern H3 Same-cohort PIAT Math and transcript-aligned HSLS/ELS show the same female edge, and item-format/time effects are small Stop calling NLSY97 “quantitative” construct-equivalent to NLSY79/PIAAC
H2 school-exit sorting 0.16 AFQT/ASVAB is partly achievement; NLSY97 has course, honors, transcript, and school-experience data; school exposure can move the surface H1 Within transcript ladders in HSLS/ELS, the edge does not survive; NLSY97 PIAT Math is not female-leaning Treat school variables as mechanisms/strata, not nuisance controls
H3 process/test-taking channel 0.20 Local Stage A moves a lot when process/precision variables enter; external literature says timing, response process, and item format can move gender gaps H1 Design-only models do little, and format/time/process decompositions show minimal modulation Rebuild process analyses using only defensible nuisance/process designs
H4 sample/weight/missingness instability 0.18 Same-sample bases already erase much of the raw female edge in tighter subsets H1 IPW / missingness-harmonized analyses leave a stable female edge of similar size Make observability audit a stage gate, not housekeeping
H5 real cohort-specific female edge on this test surface 0.10 Still possible on a narrow late-adolescent school-math surface, especially MK-style knowledge H1/H2 Same-cohort alternative math surfaces and transcript-rich replications fail to show it Keep alive as minority hypothesis; do not headline it

These posteriors come from the local Stage A pattern, the official CAT-ASVAB scoring/admin docs, CAT-vs-paper comparability evidence, AFQT schooling evidence, and the item-format/time-pressure/DIF literature. ￼ ￼

4. Measurement Crosswalk

The table below is the real construct map. Label matching is a nerd trap. Use this or get conned by your own variable names. Official documentation for each battery supports the entries. ￼

Battery What it actually measures Timing / speededness Adaptive? Item-level / process access Transcript / track info Public status Comparability judgment
NLSY79 ASVAB Military aptitude battery; AR/MK are school math reasoning/knowledge; NO/CS are speeded Mixed power + 2 speeded paper tests No AFQT item responses public for AR/MK/WK/PC; no process traces verified Schooling vars; no rich public transcript verified here Public-use Medium family overlap, low surface equivalence to NLSY97 quant
NLSY97 CAT-ASVAB CAT military aptitude battery; AR/MK adaptive MAP scores; NO/CS non-adaptive rate scores; NLS-created math/verbal percentile Mixed adaptive power + speeded rate-scored tests Yes for 10 power subtests; No for NO/CS Scores, items answered, posterior variance, test-environment questionnaire; public item responses not verified Yes: school experience, honors/course reports, transcript survey Public-use; transcript survey exists Baseline object, but messy
PIAAC numeracy Adult mathematical literacy in real-life contexts Computer-based direct assessment; staged routing; adult low-stakes Yes, multistage for literacy/numeracy Public PUF; public log XML for 17 cycle-1 countries; released items No transcripts; only education/occupation/field proxies Public-use + RDC Low-medium vs NLSY97 quant
PISA math Mathematical literacy at age 15 Computer-based; format-sensitive; contextual items Yes, multistage adaptive since 2018/2022 major domains Public cognitive item file; 2015/2018 public cognitive time/visits; 2022 item+questionnaire timing, but no public cognitive time/visits found in index No transcripts; some grade/track/system proxies Public-use Low-medium overall; good for H1/H3
TIMSS 2019 / eTIMSS Curriculum-based school math at grade 4/8 Booklet design; paper + digital; interactive digital items in eTIMSS No CAT; fixed booklet design Public database and item stats; digital process richness exists, raw public traces not fully verified Student/teacher/school context; no transcripts Public-use Medium for format/mode, low for school-exit
HSLS:09 Algebraic reasoning in grade 9 and grade 11 Computer-delivered two-stage test Yes, two-stage Public score/theta/SEM; public item/process traces not verified here Rich: high school transcripts, counselor, course ladder, honors/STEM vars Public-use + restricted High for H2
ELS:2002 Broad school math achievement from arithmetic through advanced topics Two-stage adaptive forms Yes, two-stage Public standardized score; theta restricted; no public process found Rich high school transcript infrastructure; more detailed course-level work may need restricted data Public + restricted High for H2, medium overall
TIMSS Advanced 2015 Advanced mathematics/physics for students in special advanced tracks Conventional large-scale assessment No Public achievement/background data; item parameters public; restricted vars by request Track is built into sample; teacher/school/curricular context Public + restricted Low for general population; high for upper-tail branch
Project Talent Broad historical high-school cognitive battery + life-course follow-up Paper historical battery No Researcher access exists; item/process specifics not verified here School/context info; transcript richness not verified here Researcher portal Medium-low due era
NAEP / HSTS NAEP math achievement + HSTS transcript coursetaking/GPA Modern NAEP digital/paper varies by wave No CAT NAEP process data public; HSTS transcript data/public materials exist Yes on transcript side Public, but linkage/use is less frictionless Medium

Bottom line:
• HSLS/ELS are the clean adjudicators for H2.
• TIMSS/eTIMSS + PISA 2018 are the clean adjudicators for H1/H3.
• PIAAC logs are adult reconciliation, not school-exit adjudication. ￼

5. Audit of Local Stage A

The local result that matters is narrow and real: the reported NLSY97 female quantitative edge is not stable. In the largest local process_core sample, the same-sample base is +0.037 and the adjusted coefficient is -0.041; AR stays male-leaning, MK collapses sharply, and NO remains female-leaning after adjustment. That is enough to kill a confident “NLSY97 discovered a general female quant edge” story. It is not enough to identify mechanism. ￼

From the uploaded covariate-gap table, two local facts stand out: females complete more Numerical Operations items and have lower Math Knowledge posterior variance, while Arithmetic Reasoning posterior variance is near parity. That means the current “process” block is loading heavily on speed/completion and MK precision, not on generic room-quality noise. That makes overcontrol more plausible, not less.

Variable Causal status Why Use
recent grades Mediator / post-treatment Sex can affect classroom behavior, grading, confidence, course placement, and recent exposure; grades are also downstream of the same latent/school processes you are trying to explain Mechanism description only
grade-at-test Hybrid, but mostly post-treatment for total-effect questions Grade reflects prior school progression/retention/acceleration; it is not an exogenous nuisance. Use exact age/birth cohort instead for design Stratify; do not use as primary “control”
school-exposure proxies (science_experiment, science_equipment, shop_attention, subject-taking) Mediators and noisy proxies They are opportunity-to-learn / interest / track measures, not confounders; some are gender-coded in ugly ways and are not even math-specific Sorting/mechanism tests only
prior test-taking Selection/experience proxy Could matter for familiarity, but is not clearly exogenous to ability, age, or school pipeline Sensitivity / stratification only
computer-use / computer-test Mediator for total-effect estimands Digital familiarity is part of the process channel, not a confounder; okay only if the estimand is “mode-equalized score surface” Separate mode-equalization spec, not main causal spec
effort Descendant / collider risk Ability, confidence, stereotype activation, fatigue, and room conditions can all affect reported effort Do not adjust in primary models
room comfort / quiet Closest thing to defensible nuisance Plausibly exogenous test-condition noise, though still not perfect Okay in nuisance-only block
items completed Descendant of ability/speed/time pressure Especially bad here because NO/CS are the speeded female-leaning surfaces and the official docs treat them as rate scores Use as outcome/mechanism or quality filter, not regressor
posterior variance Descendant of ability + item path + response pattern It is part of the adaptive score-generation machinery; controlling it conditions on reliability generated by the latent variable Use as sensitivity filter, not main regressor
exact test date / age / birth cohort / easy form Legitimate design controls Official docs explicitly flag easy-form assignment and age-structured scoring Should be in the primary design-adjustment block

Official NLSY97 docs support the special status of the last row: adaptive routing, easy-form assignment for the youngest respondents, released items-answered counts, and posterior variance are all part of the administration/scoring design. ￼

Verdict on Stage A:
• Defensible hardening: “The raw NLSY97 female quantitative edge is fragile.”
• Necessary softening: “The current Stage A does not yet show that process/measurement caused the edge.”
• Reason: the current block mixes exogenous nuisance, downstream score precision, speed-surface descendants, and school mediators. That is a stress test, not identification. The local negative controls do help: mechanical stays strongly male and clerical remains female after adjustment, so the block is not flattening everything uniformly. But that specificity does not rescue the causal interpretation. ￼

6. Best External Datasets and Why

Highest-leverage missing data is still internal: NLSY97 PIAT Math + transcript survey + honors/course reports. The NLSY97 docs explicitly say PIAT Math can be compared with transcript and curriculum information. ￼

After that, external ranking:

Rank Dataset Exact access URL Best falsifiable question Limiting assumption
1 HSLS:09 https://nces.ed.gov/surveys/hsls09/hsls09_data.asp Does any female-leaning school-exit math edge survive within transcript-defined course ladders and prior-achievement cells? Algebraic reasoning is still a school-linked, semi-adaptive surface, not ASVAB
2 ELS:2002 https://nces.ed.gov/surveys/els2002/avail_data.asp Same question one cohort earlier: does transcript/course alignment kill or preserve the gap? Public math score is coarser; some assessment detail is restricted
3 TIMSS 2019 / eTIMSS https://timssandpirls.bc.edu/timss2019/international-database/ ; https://timssandpirls.bc.edu/timss2019/etimss/ Do sex gaps move by mode, item family, and interactive format in curriculum-aligned math before school exit? Grade 4/8, not late-adolescent school exit; transcript data absent
4 PISA 2018 + PISA 2022 https://www.oecd.org/en/data/datasets/pisa-2018-database.html ; https://www.oecd.org/en/data/datasets/pisa-2022-database.html Do sex gaps move by item format and adaptive routing/timing in mathematical literacy? No transcripts; 2022 public process is weaker than 2018 for time/visits
5 PIAAC log files https://www.oecd.org/en/data/datasets/piaac-public-use-files.html ; https://www.gesis.org/en/piaac/rdc/access-to-data/first-cycle Does adult male numeracy survive after process-aware DIF/item-family decomposition? Adult post-school surface; cannot adjudicate H2 directly
6 TIMSS Advanced 2015 https://timssandpirls.bc.edu/timss2015/advanced-international-database/ Is the real disagreement concentrated in the advanced-track upper tail rather than general school math? Highly selected sample; not general population
7 NAEP process + HSTS https://www.nationsreportcard.gov/processdata/ ; https://nces.ed.gov/nationsreportcard/hsts/ Within nationally representative 12th-grade course-taking patterns, do math gaps persist after transcript alignment? Linkage/use is more cumbersome than HSLS/ELS; process release differs by grade/wave
8 Project Talent https://www.air.org/project-talent/researchers In a huge historical school cohort, do broad cognitive batteries reproduce the same qualitative pattern? 1960 cohort; no digital process; era mismatch

Why the top two are top two: HSLS and ELS are the cleanest available tests of H2 because they are U.S. school-transition studies with transcript/course-ladder information and computer-delivered staged math assessments. Why TIMSS/PISA come next: they are the cleanest public tests of H1/H3 because they let you slice by format/mode/process much more cleanly than NLSY97 currently does. ￼

7. Strongest External Narratives Worth Taking Seriously

Taleb.
Useful update: he is right to attack reification and composite fetishism. Your repo’s current risk is exactly that—treating a battery-local sign flip as though it were a metaphysical statement about latent intelligence. Rhetoric: “IQ is a swindle” is too broad and overshoots the empirical question here. DOE update: make measurement non-equivalence a gate before causal storytelling. ￼

Cremieux.
Useful update: he is right that selection and exclusion can distort sex comparisons, and right that the means-vs-variability/tails distinction matters. Rhetoric: the discourse around his work often leans toward a stable male-baseline prior even when the psychometrics are mixed. DOE update: strengthen H4 and tail audits, but do not let that bypass the construct map. ￼

Gwern.
Useful update: not as a theorist here, but as a bibliography. The serious papers he hosts lean toward “no robust general g gap, real specific differences,” which is broadly where the cleaner literature sits. Rhetoric: the right-tail/SMPY material can seduce you into smuggling elite-sample math reasoning into population-level claims. DOE update: keep upper-tail work in its own branch. ￼

Gelman.
Useful update: multiverse discipline and measurement humility. Your current Stage A is exactly the kind of analysis where specification curves, selection checks, and explicit estimands beat one “preferred” regression. Rhetoric: he is not offering a substantive sex-differences model here. DOE update: lock design-only, mechanism, and bad-control specs separately. ￼

Scott Alexander.
Useful update: even small mean differences can matter in tails and institutions. That is a valid reason not to dismiss small effects as socially irrelevant. Rhetoric: social extrapolation can outrun causal identification very fast. DOE update: run tail analyses separately from the mean-gap adjudication; do not let “tails matter” rescue weak measurement. ￼

Psychometric fairness researchers.
Useful update: this is the strongest external correction the repo still underweights. Time limits, response processes, and item format can materially move sex gaps; PIAAC response-process data and PISA item-format work say so directly. Rhetoric: fairness diagnostics are not a proof of construct validity by themselves. DOE update: do item-family, time-pressure, and response-process decomposition before latent claims. ￼

Sociology / economics of education.
Useful update: AFQT/ASVAB is partly achievement, not pure ability; course ladders, beliefs, and school structures matter. But the strongest version of “girls just took more math” is too blunt—contemporary cohorts often show little average gender difference in overall high-school math course-taking, even if beliefs and track transitions differ. DOE update: stop using generic school-exposure proxies; move to transcript-defined ladder, honors, and on-track estimands. ￼

8. Recommended Next 3 Analyses

1. NLSY97 same-cohort cross-surface falsification

Estimand.
β_female on standardized AR, MK, AR+MK, and PIAT Math within the overlap sample, under three nested specs:
(a) raw;
(b) design-only adjustment: exact age at test, birth cohort / easy-form indicator, test date/site/session, room comfort/quiet;
(c) design-only + transcript/honors/course-ladder strata.

Key variables.
Sex, birth year (1983/84 easy-form risk), exact age at test, transcript variables, honors math/science, course-of-study, PIAT Math, CAT-ASVAB subtests. Official NLSY97 docs say PIAT Math can be compared to transcript/curriculum information. ￼

Identification logic.
Same cohort, same general schooling environment, different math surfaces. If the female edge is CAT-surface-specific, it should be much larger on CAT-ASVAB than on PIAT Math after design-only controls.

Do not adjust for.
Effort, items completed, posterior variance, recent grades, subject-taking, school-exposure proxies, computer familiarity in the primary model.

Negative controls.
Mechanical composite and verbal composite. If the design-only block “explains” everything, it is probably just blurring signal.

Successful falsifier.
After design-only controls, the CAT-vs-PIAT sex-gap difference shrinks below about 0.05 SD and the sign is the same on both surfaces. That would hit H1/H3 hard.

Weak evidence.
A flip that appears only after adding effort / posterior variance / items completed.

Could still fool us.
PIAT is a younger/grade-limited subset and may have ceiling issues. Transcript missingness can also fake clean comparisons.

2. HSLS:09 transcript-ladder replication

Estimand.
β_female on grade-11 algebraic reasoning score overall and within transcript-defined math ladders: highest math course, credits, honors/AP/IB, and 9th-grade baseline math placement. Use HSLS public-use and transcript files first; go restricted only if the public version blocks the needed ladder detail. HSLS public-use data and transcript products are officially available. ￼

Identification logic.
This is the cleanest external H2 test: near school exit, U.S. cohort, rich transcript/counselor context, staged computer math assessment.

Do not adjust for.
Contemporaneous aspirations, math self-concept, and recent grades in the primary causal spec. Those are downstream.

Negative controls.
Foreign-language credits, arts credits, PE credits. If your “schooling explanation” works equally well with non-math coursework, it is not a math-course explanation.

Successful falsifier.
Within transcript ladders and baseline placement cells, the math gap is male-leaning or near zero, not female-leaning. That would weaken H2 as an explanation for the NLSY97 raw female edge.

Weak evidence.
Attenuation only after adding grades or aspirations, or attenuation confined to tiny honors subgroups.

Could still fool us.
Transcript ladders are endogenous. Even perfect course matching is not random assignment.

3. School-age item-format / process decomposition

Primary dataset: TIMSS 2019/eTIMSS
Replication: PISA 2018; use PISA 2022 mainly for current adaptive/item-content checks, not as the primary public timing file.

Estimand.
Difference-in-differences in sex gaps by item format (MC vs CR vs interactive), mode (paper vs eTIMSS where bridge permits), and time/visit burden (PISA 2018). Official TIMSS docs explicitly discuss paper/eTIMSS linking and mode-equivalent item selection; OECD’s public PISA index explicitly lists cognitive time/visits files for 2015/2018. ￼

Identification logic.
If H1/H3 are right, sex gaps should move systematically when you change format, interface burden, or process load while staying inside the same broad domain.

Do not adjust for.
Attitudes, anxiety, effort, or self-concept as if they were confounders. They are mechanism variables.

Negative controls.
Science items or math items with minimal navigation/typing burden. The format story should bite hardest where format burden is highest.

Successful falsifier.
Across countries, the format/mode/time modulation of the sex gap is small (< 0.05 SD) and not consistently signed.

Weak evidence.
One country, one format family, or one lucky item bundle.

Could still fool us.
Low-stakes motivation, translation/adaptation, and curriculum heterogeneity can contaminate item-level comparisons.

Global rule for the next DOE:
Do not put grades, course-taking, effort, items-completed, or posterior variance in the main causal model and then talk as if the coefficient movement revealed cause. Run: 1. design-only, 2. selection-harmonized, 3. mechanism blocks, 4. bad-control stress tests.
In that order.

9. Claims Table

Claim Source URL(s) Status
NLSY97 CAT-ASVAB used adaptive routing, had an easy-form start for 1983/84 births, and released items-answered counts, posterior variance, and online-questionnaire variables https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/administration-cat-asvab ; https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-10-cat-asvab-scores Fact
NLSY97 adaptive power-test scores are MAP/Bayes modal estimates; NO and CS are non-adaptive rate scores https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-10-cat-asvab-scores Fact
The NLSY97 math/verbal percentile is NLS-created and not DoD-endorsed https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-10-cat-asvab-scores Fact
NLSY79 vs NLSY97 AFQT comparability is complicated by test format and age-at-test differences https://public.econ.duke.edu/~psarcidi/altonji.pdf Fact
Historical CAT-vs-paper ASVAB equating did not show a female AFQT advantage for CAT; notable female differences favored paper on PC and Auto/Shop https://www.officialasvab.com/wp-content/uploads/2019/08/asvab_techbulletin_1.pdf Fact
Schooling affects AFQT, so AFQT/ASVAB is not a pure ability measure https://www.nber.org/system/files/working_papers/w11113/w11113.pdf Fact
NLSY97 contains a PIAT Math assessment that the docs explicitly suggest comparing with transcript/curriculum information https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/piat-math-test ; https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/school-transcript-surveys Fact
HSLS:09 public-use data include transcript/admin records; ELS:2002 public-use includes a standardized math score and transcript products, with more detail under restricted use https://nces.ed.gov/surveys/hsls09/hsls09_data.asp ; https://nces.ed.gov/surveys/els2002/avail_data.asp ; https://nces.ed.gov/training/datauser/ELS_03/assets/ELS_03_transcript.pdf Fact
PISA 2022 public database lists cognitive item data and questionnaire timing; OECD’s public index lists cognitive time/visits files for PISA 2015 and 2018 https://www.oecd.org/en/data/datasets/pisa-2022-database.html ; https://webfs.oecd.org/pisa2022/index.html Fact
PISA mathematics since 2018/2022 uses multistage adaptive testing in computer-based assessment https://www.oecd.org/en/about/programmes/pisa/pisa-frequently-asked-questions-faqs.html ; https://www.oecd.org/en/publications/pisa-2022-results-volume-i_53f23881-en/full-report/adaptive-testing-in-pisa-2022_21364c8d.html Fact
TIMSS 2019 mixed paper and eTIMSS modes and explicitly linked them psychometrically across modes; TIMSS Advanced 2015 has a public-use advanced-track database https://timssandpirls.bc.edu/timss2019/methods/ ; https://timssandpirls.bc.edu/timss2019/international-database/ ; https://timssandpirls.bc.edu/timss2015/advanced-international-database/ Fact
PIAAC Cycle 1 public-use log files exist for 17 countries and can be linked to the public files by SEQID; full documentation may require agreement https://www.oecd.org/en/data/datasets/piaac-public-use-files.html ; https://www.gesis.org/en/piaac/rdc/access-to-data/first-cycle Fact
NAEP process data and the High School Transcript Study both exist and are relevant for transcript-by-achievement work https://www.nationsreportcard.gov/processdata/ ; https://nces.ed.gov/nationsreportcard/hsts/ Fact
Project Talent offers researcher access to data including cognitive assessment; item/process detail was not fully verified in this audit https://www.air.org/project-talent/researchers Fact + uncertainty
Best current synthesis is that H1/H3 dominate, but H4 is materially underweighted and H2 needs transcript-rich testing See sections 3, 5, 6 above Inference

The claims table is grounded in the official or primary sources cited throughout the report. ￼

10. Appendix: Search Log

What I searched
• Official NLSY97 CAT-ASVAB scoring/admin docs: easy form, posterior variance, items answered, internal percentile construction
• Official ASVAB technical docs: time limits, rate scoring, subgroup comparability, DIF/fairness
• NLSY79 ASVAB docs: public item responses, AFQT construction
• HSLS and ELS official data pages and manuals: assessment design, transcript access, public vs restricted
• OECD PISA official database pages and download index: 2022 vs 2018 file availability
• TIMSS/eTIMSS official methods: mode bridge, booklet design, digital assessment
• PIAAC official public-use/log-file access pages
• NAEP process data and HSTS official pages
• Project Talent official researcher portal
• Disconfirming literature: time limits, item format, response-process DIF, course-taking/track, schooling and AFQT

What turned out to be noise
• Blog/Substack rhetoric without technical documentation
• ResearchGate mirrors when primary or official versions existed
• Generic “gender and math” media pieces with no design detail
• Broad IQ debates that never touched CAT-ASVAB, transcript ladders, or item-format/process evidence

What was missing or inaccessible
• AIR Project Talent detailed study-design pages partly returned 403; I relied on official search snippets for access-level claims
• I did not verify public raw item-response files for NLSY97, HSLS, or ELS from official pages in this pass
• Some ASVAB DIF tables were accessible, but focal/reference coding for directionality was not clean enough in the fetched pages to support directional claims, so I did not use them that way
• For PISA 2022, I used the public download index as source of truth for available public files; it may still be possible to derive more from technical documentation, but the public index itself is thinner than 2015/2018 on cognitive time/visits
