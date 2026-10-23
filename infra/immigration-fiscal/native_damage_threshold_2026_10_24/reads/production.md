**Verdict:** None of the production papers identifies a new national annual loss to the complete Mexican-origin lineage's nonmembers. Automation is measured, but its output cost is imprecise; the adverse schooling-externality readings alter a row already priced in the fiscal-plus-social account but absent from the world ledger. Positive results have the same transport problem. [INFERENCE from primary estimates below]

# Production, automation, innovation and skill mix

## Log

- 2026-10-24 01:47 JST: source retrieval and primary-table verification started. Existing lanes are locators and overlap checks only; no lane is rerun.
- 2026-10-24 01:51 JST: recovered Lewis's author manuscript after the journal PDF returned HTTP 403; checked Table VII directly.
- 2026-10-24 01:55 JST: checked newer Terry et al. author manuscript and published Ottaviano–Peri table. The former differs from the older version used in the existing lane; version differences are preserved below.

## 1. Automation: Lewis (2011)

[SOURCE: Lewis, *Immigration, Skill Mix, and Capital-Skill Complementarity*, QJE 126:1029–1069, DOI 10.1093/qje/qjr011; [author-manuscript PDF](https://citeseerx.ist.psu.edu/document?doi=a01950deeeb8723f2dabb27e2afdfdad63f65cf4&repid=rep1&type=pdf), Table VII, PDF p44; Table VI, PDF p43; Table I, PDF p39. Cache: `production_lewis2011.pdf/.txt`.]

| Outcome | IV estimate (SE), per unit increase in metro dropout/HS-equivalent ratio |
|---|---:|
| Δln machinery/worker, 1987–1992 | −0.59 (0.31) |
| Δln value added/worker, 1987–1992 | −0.03 (0.24) |
| Technologies used, industry × price controls | −8.21 (1.90) |

This is an immigration-settlement IV, not random assignment. Technology outcomes cover SIC 34–38 plants with ≥20 employees; the output regression uses the wider Census of Manufactures sample. The regressor counts **all metropolitan labor-force heads**, using person weights, ages 16–65, ≥1 year potential experience; HS equivalents = HS/GED + half of some-college/no-BA. It is not the low-skill immigrant share.

For actual Δr = D/H with group minus without group, the linear output response is −0.03Δr; the coefficient's normal 95% range is [−0.5004, +0.4404]. The native-output conversion additionally requires the exposed manufacturing share and incidence. Multiplying −0.59 by national GDP wrongly treats foregone machinery as foregone output. [CALCULATION: β ± 1.96SE; INFERENCE]

## 2. Directed invention: San (2023), with an internal disconfirmer

[SOURCE: San, *Labor Supply and Directed Technical Change*, AEJ Applied 15(1):136–163, DOI 10.1257/app.20200664; [author-hosted published PDF](https://mulysan.github.io/San_bracero.pdf), Table 2 p147; Figure 3 p148; §VI pp159–160/Figure 6. Cache: `production_san2023.pdf/.txt`.]

Bracero exclusion's crop-level exposure DiD: patent coefficient **3.258 (SE 0.474)**, citations **2.271 (0.497)**, per unit pre-exclusion seasonal foreign-worker share. Thus a one-percentage-point increase in exposure changes log patents by 0.03258, not national output by 3.258%. Sixteen crops and 608 crop-years; crop and year effects. Effects persist 15–20 years.

The same paper finds farm land values fell in more-exposed counties after exclusion; it provides an event-study graph, not a national annual native-income number. Innovation did not recover the affected owners' lost profitability. This directly challenges the inference from more machines/patents to greater incumbent welfare, while leaving external idea spillovers unresolved. National translation requires crop exposure, innovation-to-productivity, ownership and geographic spillover parameters absent from this estimate. [INFERENCE]

## 3. Randomized low-skill visa counter-evidence

[SOURCE: Clemens–Lewis, *The Effect of Low-Skill Immigration Restrictions on US Firms and Workers*, [NBER w30589, May 2024 revision](https://www.nber.org/system/files/working_papers/w30589/w30589.pdf), Table 4 p34; Table 5 p35; discussion p36. Cache: `production_clemenslewis2022.pdf/.txt`.]

In the randomized H-2B lottery, the full-control 2SLS effect of foreign employment on inverse-hyperbolic-sine investment is **2.072 (SE 0.721)** using lottery win; **1.466 (0.610)** using expected authorized share. Anderson–Rubin p = .001/.012. Investment includes equipment, vehicles, structures and land. The full-control profit-rate-change coefficient is **0.152 (0.075)** or **0.151 (0.067)**. This is strong evidence against a universal firm-level crowding-out of capital by low-skill foreign labor.

It is a short-run firm LATE among petitioning employers, and capital quantity is not capital per worker or a national output externality. Multiplying 2.072 by the lineage's population share is invalid. Neither this favorable result nor Lewis's adverse machinery result independently identifies the requested national welfare effect. [INFERENCE]

## 4. Aggregate productivity: Peri (2012)

[SOURCE: Peri, *The Effect of Immigration on Productivity*, REStat 94:348–358, DOI 10.1162/REST_a_00137; [author-hosted published PDF](https://giovanniperi.ucdavis.edu/uploads/5/6/8/2/56826033/peri_effect_of_immigration_on_productivity_2011.pdf), Table 2 p352. Cache: `production_peri2012.pdf/.txt`.]

Basic 2SLS estimates: output/worker **0.88 (SE .25)**; TFP **1.37 (.27)**; capital-intensity contribution **−.08 (.13)**; skill-bias term **−1.14 (.15)**. Treatment = net immigrant-worker inflow during a decade / initial employment, US states and DC, 1960–2006; 255 observations. Instruments combine historical settlement and border-distance × decade terms; baseline first-stage F=17.42.

One pp of that inflow implies **+0.88% output/worker**, normal 95% **+0.39% to +1.37%**. A conditional national mapping is `100 × (exp(.88 × inflow/initial_employment) − 1)` under common proportional productivity transmission. The low-skill-only slope, native-only incidence and long-run stock-removal mapping are not estimated. This favorable aggregate finding is important disconfirmation of interpreting technique adaptation as an output loss; it cannot be added independently to the scale, task and innovation effects it can contain. [INFERENCE]

## 5. Schooling externalities: adverse and null readings

[SOURCE: Moretti, *Estimating the Social Return to Higher Education*, J Econometrics 121:175–212, DOI 10.1016/j.jeconom.2003.10.015; [published author PDF](https://eml.berkeley.edu/~moretti/socret.pdf), Table 5 p200; Table 2 p194. Cache: `production_moretti2004.pdf/.txt`.]

Age-structure-IV Table 5 col4: a unit increase in BA worker share changes log wages by **1.91 (.52)** for <HS, **1.67 (.45)** HS, **1.24 (.42)** some college, **.47 (.37)** BA+. Thus one pp is 1.91/1.67/1.24/.47 percent, respectively. NLSY individual-and-city effects yield **1.27 (.33)**; individual×city effects **1.08 (.32)**. These effects include skill substitution: they are not automatically productivity externalities. A national transport must use each nonmember education group's earnings, actual change in BA worker share, and net out the already-priced CES component. [INFERENCE]

[SOURCE: Ciccone–Peri, *Identifying Human-Capital Externalities*, REStud 73:381–412, DOI 10.1111/j.1467-937X.2006.00380.x; [published author PDF](https://giovanniperi.ucdavis.edu/uploads/5/6/8/2/56826033/ciccone_peri_identifying_human_capital_2006.pdf), Table 4 p402, Table 5 p403, interpretation p401. Cache: `production_cicconeperi2006.pdf/.txt`.]

The constant-composition IV explicitly removes substitution. Per extra year of average worker schooling, Table 4 col2 is **−.004 (.017)**; col1 **+.014 (.030)**; col4 **−.010 (.018)**. White-male Table 5 col2 is **−.001 (.021)**. The central col2 normal 95% coefficient interval is [−.03732,+.02932]. These are near-zero average-schooling externalities, not proof that BA-specific spillovers vanish. The treatment and instruments differ from Moretti; both require exclusion restrictions.

[SOURCE: Iranzo–Peri, *Schooling Externalities, Technology and Productivity*, [NBER w12440, August 2006](https://www.nber.org/system/files/working_papers/w12440/w12440.pdf), Table 8 p45, Table 9 p46. Cache: `production_iranzoperi2006.pdf/.txt`. This is the working-paper version, not a claim to have checked the published 2009 text.]

College-schooling coefficient **.06 (.025)**, 1970–2000; **.12 (.04)**, 1980–2000. Corresponding HS-schooling coefficients **−.01 (.01)** and **+.01 (.03)**. Table 9's sector-shift control gives college **.11 (.04)**. The school's quantity is a worker-average years measure, not BA share or low-skill immigrant share. A conditional proportional-productivity scenario uses `exp(βcollege Δschoolcollege + βHS ΔschoolHS)−1`; plugging a BA-share change straight into it is invalid. [INFERENCE]

**Overlap:** the existing `scale_spillovers_2026_09_23/RESULT.md` already contrasts these designs. The adopted **fiscal-plus-social** account carries its city-size-minus-schooling net. The **world ledger does not carry that row**: `world_ledger_2026_09_27/world_ledger.py` selects victims/property/care/congestion in `SOCIAL_PAIRING_ROWS`, while `derived/channels_scope_oct15.csv` excludes the `account_plus_social` object. The larger adverse college-share constructions must **replace** the fiscal-plus-social account's existing composition term, preserving its size benefit. Against the world ledger, scale and schooling would instead be omitted-channel scenarios, requiring compatible population and welfare-weight incidence before addition. The old lane's full uncertainty band is neither a Mexican-specific causal estimate nor a native-only effect. [DATA: FAQ4; scale-lane overlap ruling and Tables 3–4; world-ledger source and scope table]

## 6. Wage-incidence models: Borjas–Katz and Ottaviano–Peri

[SOURCE: Borjas–Katz, *The Evolution of the Mexican-Born Workforce*, [published 2007 chapter](https://www.nber.org/system/files/chapters/c0098/c0098.pdf), Table 1.11 p49, discussion p51. Cache: `production_borjaskatz2007.pdf/.txt`.]

For 1980–2000 arrivals, fixed-capital average wages: all arrivals **−3.4%**, no Mexican arrivals **−2.7%**. With elastic capital, both averages are **0.0%** by construction. <HS workers' long-run readings are **−4.8%** versus **+2.2%**: Mexican arrivals' marginal contribution is −7.0pp for that subgroup. These are model simulations with estimated elasticities, not a confidence interval on a national externality. Extrapolating the low-skill wage loss to all native output ignores other groups' gains and ownership. This is a distributional concern already addressed by the production/wage-incidence framework. [INFERENCE]

[SOURCE: Ottaviano–Peri, *Rethinking the Effect of Immigration on Wages*, JEEA 10:152–197, DOI 10.1111/j.1542-4774.2011.01052.x; [publisher full text](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1542-4774.2011.01052.x), §5, Table 6 (full table read through web tool; curl returned 403).]

Published preferred model B col6: native average wage **+0.6% (simulated SE .3pp)**, old immigrants **−6.4% (1.3pp)**, overall average **0.0% (.4pp)** for 1990–2006 arrivals. Col7: +.6 (.4), −6.7 (2.8). Thus the abstract's −6.7 is one specification, not col6. Production technology is fixed in this model; it excludes productivity externalities explicitly (§2). For conditional native-output accounting multiply native wage change by native labor income/native output, but a new inflow's skill vector cannot be replaced by this lineage's share. The source's US-born includes Mexican-origin descendants; the repo's nonmembers include other immigrants. [INFERENCE]

`production_op2008.pdf` and `production_op2011.pdf` are earlier NBER texts fetched during discovery; the latter's actual title is *Immigration and National Wages* (w14188, July 2008), not a 2011 revision. Use the published table above for the final claim.

## 7. Innovation: source-version and skill checks

[SOURCE: Terry–Chaney–Burchardi–Tarquinio–Hassan, [May 2024 author manuscript](https://www.hoover.org/sites/default/files/research/docs/ImmigrationInnovationandGrowth.pdf), Table 5 printed p38/PDF p39, discussion printed pp11–12; published AER 116(3):828–861 (2026), DOI 10.1257/aer.20211601. Cache: `production_bchtt2024.pdf/.txt`. Published PDF paywalled; do not claim manuscript coefficients were checked against it.]

Per 1,000 adult immigrants, Table5 col2 patent coefficient = **.254 (.082) + .281 (.094)×(schooling−10.88)**; wage coefficient = **.298 (.058) + .251 (.055)×(schooling−10.88)** in $100 of average annual earnings at 2010 prices. These are five-year county outcomes; patent units are per 100,000 baseline-1970 people. Low-schooling tercile: patents **−1.671 (5.620)**; wages **−.264 (.259)**, neither distinguished from zero. No covariance is supplied here for the linear combination. The footnote's native-nonmover ten-year coefficients are **.249 (.054)** and **.138 (.036)**, not the five-year total-county pair.

The existing lane used November2021 w27075 Table9: patent slope .235 rather than .281. Do not silently port its calibrated dollar arithmetic to this revision. Patents require an innovation-to-income model; total county wages mix compositional and native effects. This yields a quantitative null/positive-or-negative range at low schooling, **not an identified national marginal loss**. [INFERENCE]

[SOURCE: Hunt–Gauthier-Loiselle, [NBER w14312, September 2008](https://www.nber.org/system/files/working_papers/w14312/w14312.pdf), Table 6, PDF p40. Cache: `production_huntgauthier2008.pdf/.txt`.]

Table6 IV coefficient on immigrant college-graduate share among population aged18–65 is **17.7 (SE7.6)** on log patents per capita, 10-year differences, 1950–2000. One pp therefore implies **+.177 log patents**; WLS is **11.4 (4.1)**. First-stage F=16. This supports a high-skill innovation channel, not a negative slope for low-skill immigrants; the innovation-to-native-income bridge remains absent. The source was retrieved for the parent's requested comparison, not used as a low-skill offset. [INFERENCE]

## Coverage, access and summation

### Follow-up: Borjas's own surplus/externality distinction

[SOURCE: Borjas, *Lessons from Immigration Economics*, The Independent Review 22(3), **Winter 2018**, pp329–340; [published PDF](https://www.independent.org/wp-content/uploads/tir/2017/12/tir_22_3_02_borjas.pdf), Table1 p337 and discussion p338. Cache names `production_borjas2017.pdf/.txt` reflect the URL's 2017 upload path; the publication year is 2018.]

Table1's model for **all US immigration in 2015**, with capital fixed, gives native surplus **+$50.2bn**, native-worker loss **$515.7bn** and native-firm gain **$565.9bn**; GDP rises $2,104.0bn, of which $2,053.8bn pays immigrants. The worker loss is a redistribution, not an additional $515.7bn productivity externality. On p338 Borjas expressly excludes positive and negative externalities from this surplus and says they lack credible quantification. That is his dated assessment, not an audit of everything published since. It supplies **no causal negative low-skill productivity coefficient** for this lineage. [INFERENCE]

[SOURCE: Borjas, *Immigration and Economic Growth*, [NBER w25836, May2019](https://www.nber.org/system/files/working_papers/w25836/w25836.pdf), p17, Figure3. Cache: `production_borjas2019.pdf/.txt`; working paper, separately labeled from the published 2018 piece.]

His illustration assumes a 1% native-productivity externality against roughly $17tn pre-immigration GDP, producing about $170bn extra benefit. It demonstrates sensitivity to the **assumed** externality, with no estimate of its immigration-share derivative or adverse low-skill value. Its reverse-sign arithmetic is a threshold scenario, not evidence that low-skill migrants lower native productivity by 1%. [INFERENCE]

Covered: Lewis, San, randomized H-2B, Peri aggregate productivity, Moretti and Ciccone–Peri, Iranzo–Peri working paper, Borjas–Katz, published Ottaviano–Peri, updated Terry et al. author version, Hunt–Gauthier-Loiselle working paper. Skipped: Kerr–Lincoln exact table (high-skill treatment already represented by Hunt; no low-skill national bridge); Beerli Swiss skill-intensive-firm effects (different population, existing lane records the mechanism); Arkolakis–Lee–Peters w35392 retrieved but its historical spatial-growth model is not transported to this lineage. These are scope exclusions, not findings of no effect.

The causal designs identify their own firm/crop/metro/state outcomes. **No additional disjoint national-native-output term from this set passes both identification and transport.** An empty set of admissible additional terms has arithmetic sum zero, but that is an accounting convention and cannot identify total omitted damage. A full weak-evidence sum has no finite identified range because technology, schooling, patents and productivity overlap, and the national incidence/spillover bridges are missing. [INFERENCE]

## Reproduction and receipts

All source PDFs were fetched with `curl -L --fail --max-time` and extracted with `pdftotext -layout`; fetch and parse return codes were checked. No existing analysis script was run. PDF hashes: Lewis manuscript `a58b229d33ce0da033546ba766fb933fe0c8cdf7bdbcd7124cf0c50a736f8770`; Terry et al. May2024 `2f65cd10960df56242a1aa2058cfc3b678d75238f30a03ed3542ce09ec34e7be`. [DATA]

- 2026-10-24 01:57 JST: verified page numbers against form-feed page boundaries, corrected Moretti Table2 to p194 and Hunt Table6 to PDFp40. Finished the source note; only its listed source cache and this note were written.
- 2026-10-24 02:01 JST: corrected the scale/world overlap claim after checking `world_ledger.py` lines109–121 and 716–723 and the scope CSV. The fiscal-plus-social account includes scale; the world ledger excludes it. Added Borjas's published 2018 surplus/externality distinction and the separately labeled 2019 illustrative model; neither supplies an adverse low-skill productivity coefficient.

[DEGRADED] Direct journal downloads for Lewis/Ottaviano–Peri/Terry et al. returned HTTP403 or a purchase gate. Recovery: Lewis author manuscript; Ottaviano–Peri official full-text table through web; Terry et al. May2024 author manuscript plus official publication metadata. Failed speculative URLs were not treated as evidence. NBER w14188 and w14312 text extraction emitted recoverable xref warnings but produced readable text, including tables; the checked tables are reported above.
