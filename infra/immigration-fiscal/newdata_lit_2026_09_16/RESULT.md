# New-data literature & dataset-critique probe (2024-01 → 2026-09)

**Verdict:** COMPLETE. **Four hits threaten a repo number; none fully supersedes a ladder entry.**
(1) **Meyer, Mittag, Wu, Tatarka & Langetieg, NBER w35680 (2026-08)** — CPS ASEC bias >40% for nearly half of 18
income/transfer variables, dominated by false-negative measurement error, propagating into imputations. Biggest
live threat to ladder 76's fiscal ledger. (2) **Sabol, Johnson & Lynch 2025** — the 2023 ACS race redesign is a
measurement break (Hispanic-identifying White share 60%→26%), and single-race coding shifts disparity ratios by
20%; threatens the 2019→2023 leg of ladder 65/68, in the direction of UNDERSTATING the convergence the repo
found. (3) **Glassman, Census SEHSD-WP2025-07** — 45.1% of the 2023 incarcerated ACS cell is fully synthetic
(up from 35.4%); race/ethnicity/citizenship survive as imputation inputs, everything else does not.
(4) **Duncan & Trejo 2025 (AEA P&P / IZA DP 17579)** — intermarriage is 86% of the explained ethnic-attrition
channel, a mechanism ladder 75 does not carry; and second-generation adult attrition is ~2-3%, far below the 17%
third-generation-child figure ladder 67 cites.
Two more are substantive but non-threatening: **Bersani & Wy 2025** (Justice Quarterly, the successor the brief
asked for; arrest disparities are much less explained than self-report disparities) and **NBER w33558** (15-country
admin links, same 1978-84 cohort window as the Opportunity Insights tables, concludes destination not origin
drives mobility). **Q2(f) is a candidate VERIFIED NEGATIVE:** no critique of the Opportunity Insights 1978-83
cohort linkage or country-of-origin coding was found.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), researcher subagent.

Scope: Q1 = new/newly-linked US datasets on second-generation / origin-specific immigrant
outcomes, 2024-2026 only. Q2 = published or credible critiques (2024-2026) of the six dataset
families the repo relies on.

## Findings

(Findings appended in blocks below.)

---

## Block 1 (turn 6) — Q1 first sweep + Q2(a) Texas DPS dispute

### Q1 hits so far

| Hit | Cite / URL | Dataset | Number relevant to Mex-2G vs 3rd+ white | Supersedes? |
|---|---|---|---|---|
| Intergenerational Mobility of Immigrants in 15 Destination Countries | NBER w33558, Mar 2025; also IPR WP-25-11; SSRN 5172102. https://www.nber.org/papers/w33558 | Harmonized administrative parent-child links, 13 admin + 2 survey destinations, children born 1978-84 (the SAME cohort window as the OI tables the repo uses) | Headline: ~half the 2nd-gen income gap is parental income; the rest differential absolute mobility. Cross-country differences in absolute mobility are NOT driven by parental country-of-origin but by destination labor markets/policy. [needs full-text for the US/Mexico cell] | Does not supersede 65-76; directly relevant to ladder 75's origin-selectivity framing (it argues destination > origin for mobility) |
| Immigration and Inequality in the Next Generation | NBER w33961, Jun 2025. https://doi.org/10.3386/w33961 | [to verify] | [to verify] | [PENDING] |
| Climbing the Ladder: 2nd-gen mobility in France (CESifo 2025) | ifo.de WP 2025 | French admin | non-US, comparison only | no |
| Educational pathways/earnings of 2nd-gen immigrants in Australia | doi:10.1016/j.econedurev.2025.102716 (2025-09) | HILDA/Australian | non-US | no |

[GAP] S2 `search_papers` returns almost nothing post-2024 on US second-generation crime — the index is stale/poorly
matched for this query shape. Exa is the productive lane (consistent with memory note: Exa >> S2 on criminology).

### Q2(a) Texas DPS status-matched data — the CIS/Cato dispute, fully dated

The dispute is **blog/think-tank only; no peer-reviewed treatment located yet** [GAP].

| Date | Source | Claim |
|---|---|---|
| 2022-10-11 | CIS, "Misuse of Texas Data Understates Illegal Immigrant Criminality" https://cis.org/Report/Misuse-Texas-Data-Understates-Illegal-Immigrant-Criminality | Prior work (incl. Nowrasteh) undercounts because identification of illegal status takes time: some identified at arrest, some later in prison, some never. Adding the prison-identified column raises homicide and sexual-assault conviction rates above the Texas average. |
| 2022-10-20 | CIS (Richwine), "Continued Misuse of Texas Crime Data" | reply |
| 2024-02-28 | Nowrasteh, "Illegal Immigrants Have a Low Homicide Conviction Rate" | concedes his initial analysis missed prison-identified illegals; charges that the DPS extract CIS received **double-counted** individuals across categories, inflating CIS's homicide count |
| 2024-02-29 | CIS (Richwine), "Cato's Brazenly False Claim…" https://cis.org/Richwine/Catos-Brazenly-False-Claim-About-Our-Illegal-Immigrant-Crime-Research | Denies double-counting; quotes a DPS email (Chrystal Davila, 2022-10-19) stating the "illegal" and "prison" columns are mutually exclusive by construction |
| 2024-03-06 | Nowrasteh, "CIS Is Still Wrong About Illegal Immigrant Crime in Texas" | rebuttal |
| 2024-06-27 | Cato Policy Analysis 977, "Illegal Immigrant Murderers in Texas, 2013-2022" https://www.cato.org/sites/cato.org/files/2024-06/Policy-Analysis-977-new-release-date.pdf | Cato's post-concession re-estimate, the current Cato number |
| 2024-10-22 | Cato, response to Steven Malanga (Manhattan Institute) on migrant crime | third-party critic line |

**Load-bearing methodological point for the repo:** both sides now agree that status is assigned with a LAG
(arrest-time vs prison-time identification), so any Texas DPS rate computed from arrest-time flags alone is a
lower bound. The live disagreement is whether the DPS extract's columns overlap. The DPS email quoted by CIS is
the only primary evidence on that and it is quoted, not published. [SOURCE: the two URLs above] — grading:
think-tank primary-adjacent, **not peer-reviewed**.

**Does it change a repo number?** It threatens any repo figure taken from Cato's pre-2024 Texas homicide
conviction rate. Repo consumers should cite Cato PA-977 (2024-06) or later, not the pre-2024 series. [GAP] — I have
not yet grepped the repo for which vintage is cited.

Next queries if re-dispatched: NBER w33961 full text; CES working papers 2024-26 "second generation"; Bersani & Wy
2025 successors; Meyer-Mittag transfer under-reporting 2024-26; CBO 2024/2025 immigration surge fiscal reports.

---

## Block 2 (turn 9) — Q1 second sweep + Q2 (b)(c)(d)(e)

### Q1 additional hits — the two that matter

**Bersani & Wy 2025 is PUBLISHED and is the direct successor the brief asked about.**
"Assimilating into Crime? Explaining the Generational Disparity in Immigrant Offending", *Justice Quarterly*,
2025-07-24, doi:10.1080/07418825.2025.2534405. Dataset: **NLSY97** (not new data; new decomposition).
Finding: the first-vs-second-generation offending gap is "largely attributed to assimilation processes linked to
family, school, and contextual factors", NOT to immigrant selection. Critically: **"models explain much less of the
disparity in arrests" than in self-reported offending**, which the authors read as potential
**system-generated disparity**. [SOURCE: doi above]
→ Bears on ladder 65/70: it is independent support that an arrest/incarceration-based gap overstates the
behavioural gap relative to self-report. It does not supersede 65-76 (different data, different outcome), but it
is the best current published anchor for the "residual unidentified" clause in 65.

**Duncan & Trejo 2025 attrition update — supersedes the 17% figure's vintage in ladder 67.**
Duncan & Trejo, "Immigrant Age at Arrival and the Intergenerational Transmission of Ethnic Identification among
Mexican Americans", *AEA P&P* 115 (May 2025): 451-56, doi:10.1257/pandp.20251125; full version IZA DP 17579
(https://docs.iza.org/dp17579.pdf). Data: 2000 Census + 2001-2019 ACS.
Numbers: **intermarriage is 86% of the explained part** of the parental-age-at-arrival effect on child ethnic
attrition. Parent attrition ~1.05% (arrived young) vs ~0.79%; second-gen child attrition 3.3% (parent arrived
<9) vs 2.19% (parent arrived 9-14). A 2026 AEA-program successor extends it to Hispanics AND Asians using ACS
through 2023: intermarriage 73% (Hispanic) / 85% (Asian) of the explained part, parental English 19%/23%.
https://www.aeaweb.org/conference/2026/program/paper/8YEFb8eD
→ **Mechanism-supersession for ladder 75:** the repo's mechanism list has parental English and family structure;
this identifies **intermarriage as the dominant channel** of the attrition that ladder 67 and 75 both invoke.
Also note the second-generation adult attrition rate here (~2-3%) is far below the 17% third-generation-child
number in ladder 67 — the repo should not let the 17% do work at the second generation.

Also: Inkpen 2024, "Differences in Time to Reported First Arrest by Race, National Origin, and Immigrant
Generation", *Crime & Delinquency*, doi:10.1177/00111287231225125 (2024-02). Add Health/NLSY-style; finds
**Mexican-origin second generation offends at rates similar to third/fourth-generation Hispanics, while
other-Hispanic second generation offends LOWER** — an origin-divergence result inside the Hispanic category
that ladder 74's origin table is consistent with.

### Q2(b) ACS institutional group quarters as an incarceration measure — two 2025 items, both material

1. **Sabol, Johnson & Lynch 2025**, "Discrepancies in Measures of Racial and Ethnic Disparities: Implications for
   Research, Policy, and Practice", *Am J Crim Just*, doi:10.1007/s12103-025-09810-1 (2025-06-22). Compares ACS
   GQ (IPUMS), NPS, ASJ, SPI, BJS reports, BRPE, 2000-2023.
   - ACS and BJS **Hispanic shares correspond closely**; the White share diverges after the 2016 SPI adjustment.
   - **The 2023 ACS race/ethnicity redesign is a break, not a trend**: among people identifying Hispanic, the
     share also identifying White fell to 26% in 2023 from ~60% in 2019, and Hispanic-and-2+-races rose from 6%
     to 37%. "White and Hispanic" fell 24% → 10%; White 2-or-more rose 5.6% → 20.4%.
   - Single-race non-Hispanic coding **overstates Black and understates White** incarceration rates; by 2023 the
     two classification methods differ by **20% in the disparity ratio**.
   → **This threatens a repo number.** Ladder 65's 2023 ACS ratio (1.72×, ~2.1× after reallocation) and ladder
   68's state decomposition both use a white denominator across 2010→2023. If the white comparison group is
   built on a single-race non-Hispanic definition, the 2019→2023 leg is contaminated by the measurement change,
   in the direction of **understating the white rate in 2023 and therefore overstating the 2023 ratio** — i.e.
   the true convergence in ladder 65/68 may be even larger than measured. **Recommend a re-run of the 2023 cell
   with an alternative "White alone or in combination" denominator as a sensitivity arm.** [SOURCE: DOI above]

2. **Glassman 2025 (Census SEHSD-WP2025-07)**, "The Inclusion of the Incarcerated Population in Income and Poverty
   Estimates in the ACS", https://www2.census.gov/library/working-papers/2025/demo/sehsd-wp2025-07.pdf
   - Public ACS microdata **cannot distinguish the incarcerated from other institutional GQ**; only internal data
     separates six correctional types. This is a direct, Census-authored statement of the exact limitation the
     repo works around with an 18-55 age filter.
   - **Synthetic (fully imputed) share of the incarcerated ACS population rose 35.4% (2019) → 45.1% (2023)**;
     broader GQ 55.9% → 62.9%. From 2020-2023, federal prisoner records increasingly came from BOP administrative
     data with only sex, age, race, ethnicity, citizenship observed, everything else imputed.
   → **This threatens a repo number too**, and in a new way: nearly half the 2023 incarcerated ACS cell is
   synthetic. Race/ethnicity and citizenship survive (they are the imputation inputs), so ladder 65's
   ratio is safer than the ladder-76-style income work would be — but the imputation is a real caveat on any
   2023 GQ cross-tab beyond the five administrative variables. [SOURCE: URL above]

3. ICE contamination, supporting: GAO 2024 (via American Immigration Council, 2024-08-01,
   https://www.americanimmigrationcouncil.org/blog/ice-detention-data-undercounts-number-of-people-in-its-custody/)
   — ICE omitted **203,350 people, ~42% of 2022 detentions**, from its reported detained population because they
   were first held in temporary ICE/CBP facilities; ~70% of those were later detained for weeks or years. Confirms
   ladder 65's "ICE detention inflates foreign-born rows" as a live, large, and badly-measured channel.
   Structural note from the NAS GQ report: federal detention centers holding ICE detainees are **inside the ACS
   correctional GQ definition** (https://www.nationalacademies.org/read/13387/chapter/4).

4. Prison Gerrymandering Project 2024-10-30
   (https://www.prisonersofthecensus.org/news/2024/10/30/group_quarters_errors/): correctional facilities
   **failed to report Hispanic status for over a quarter of people reported in the 2020 Census**, and facilities
   are sometimes geocoded to the wrong place (4,000+ Black people at Angola coded white).
   → This is the same ~25% Hispanic-origin under-recording the repo already uses in ladder 70, now with a
   **second, independent, 2024-dated primary confirmation from the 2020 Census GQ operation**. Strengthens 70.

### Q2(c) BJS Hispanic estimation basis
Covered by Sabol/Johnson/Lynch 2025 above (the SPI-2016 adjustment is the break) plus the Prison Gerrymandering
2020-Census finding. **No separate 2024-26 critique of the BJS Prisoners Hispanic imputation located** [GAP].

### Q2(d) CPS ASEC under-reporting — a major 2026 paper, and it is the strongest hit in this probe

**Meyer, Mittag, Wu, Tatarka & Langetieg, "The Anatomy and Evolution of Survey Error", NBER WP 35680,
2026-08-27, https://www.nber.org/papers/w35680.** Linked administrative records, **18 income and program-receipt
variables in the CPS ASEC, over two decades**, in a Total Survey Error decomposition that puts coverage, unit
non-response, item non-response and measurement error on one scale for the first time.
- **For nearly half the 18 variables, bias exceeds 40%.**
- Eliminating all individual-level error would require changing **more than 80% of the true total**.
- The dominant source of bias is **measurement error among respondents who report NO receipt (false negatives)**,
  not non-response — reversing the conventional emphasis.
- Under-reporting **propagates into imputed values** for non-respondents, which are drawn from misreported donors.
→ **This is the largest live threat to the repo's fiscal ledger.** Ladder 76's per-adult net figures
(−$6,066 → −$8,286) come from a CPS ASEC 2025 generator. If transfer receipt is biased >40% for roughly half the
relevant variables, and the bias is concentrated in false negatives, then **transfer receipt is understated on
both sides of the generational comparison** and the sign of the net effect on the gap depends on which group
under-reports more. Meyer-Mittag's earlier work found under-reporting varies by population subgroup, so a
nativity-differential is plausible but **not established here** [GAP — the abstract does not split by nativity].
Recommended repo action: a sensitivity arm inflating transfer receipt to administrative totals.

Related, nativity-specific: **"Delayed Sampling of Recent Immigrants in the Current Population Survey"**,
Philadelphia Fed research brief, Jan 2025, doi:10.21799/frbp.rb.2025.jan.31 — CPS **systematically samples recent
immigrants late**, so the recently-arrived foreign-born are under-covered. Directly relevant to any
first-generation CPS cell. Also **Meyer et al., "Race, Ethnicity, and Measurement Error", NBER w32860 (2024-08),
doi:10.3386/w32860** — measurement error differs by race/ethnicity, which is exactly the differential the
generational ledger needs and does not currently carry.

### Q2(e) NAS 2016 ledger conventions, re-litigated 2024-26

| Source | Date | What it is |
|---|---|---|
| CBO, "Effects of the Immigration Surge on the Federal Budget and the Economy" https://www.cbo.gov/publication/60165 | 2024 | Counterfactual-scenario method (surge vs 200k/yr baseline). **Net deficit reduction $0.9 trillion over 2024-2034.** Explicitly federal revenues, mandatory spending and interest ONLY; a broad assessment of discretionary; **no state and local**. This is a MARGINAL-cost design, not NAS average-cost. |
| CBO, "Effects of the Surge in Immigration on State and Local Budgets in 2023" https://www.cbo.gov/publication/61464 | 2025 | The companion that fills the state/local gap above |
| Manhattan Institute, "The Fiscal Impact of Immigration (2025 Update)" https://manhattan.institute/article/the-fiscal-impact-of-immigration-2025-update | 2025-10-23 | Lifetime-NPV framing, the main rival convention |
| AEI, "The Fiscal Impact of Immigration: An Update" https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf | 2025-09 | |
| Cato white paper, "Immigrants' Recent Effects on Government Budgets: 1994-2023" https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023 | 2026-02-03 | The newest full ledger in the set; a 30-year retrospective rather than a projection |
| Cato WP-82 update, critique of MI's lifetime-fiscal-impact report https://www.cato.org/sites/cato.org/files/2024-11/working-paper-82-update.pdf | 2024-11 | The explicit Cato-vs-Manhattan methodological exchange |
| Cato, Statement for the Record on how CBO estimates budgetary effects https://www.cato.org/testimony/statement-record-improving-how-congressional-budget-office-estimates-reports-budgetary | 2024-01-31 | Argues CBO's conventions themselves are the problem |

→ The convention fight is fully live and **the repo's ladder-76 "still outside: public goods, corporate tax,
accrued entitlements, GE" caveat is exactly the disputed boundary**. None of these supersedes a repo number;
they establish that the repo's chosen boundary is one of at least four in current use. [SOURCE: URLs above]

### Q2(f) Opportunity Insights immigrant-origin tables
**No critique of the 1978-83 cohort linkage or country-of-origin coding located.** [GAP / candidate VERIFIED
NEGATIVE — one more targeted sweep would be needed to call it.] The nearest live item is NBER w33558 (2025),
which uses the same 1978-84 birth-cohort window in 15 countries and concludes origin country does NOT drive
cross-country mobility differences — a substantive challenge to origin-centric readings of the OI tables, not a
data critique.

---

## Block 3 (turn 11) — ranked new ideas

Ranked by (threat retired per unit of work). All are runnable on data the repo already holds unless noted.

1. **White-denominator sensitivity arm on the 2023 ACS ratio.** Dataset: ACS PUMS 2019 + 2023 (held).
   Question: does ladder 65's 1.72× and ladder 68's state decomposition move when the white comparison group is
   "White alone or in combination, non-Hispanic" instead of single-race? Sabol et al. predict the 2023 white rate
   is understated on single-race coding, so the true convergence is larger. Feasibility: **high, hours.** This is
   the single highest-value item because it touches two ladder entries at once.
2. **Transfer-receipt inflation arm on the generational ledger.** Dataset: CPS ASEC 2025 (held) + published
   administrative totals for the main programs. Question: does ladder 76's −$8,286 gap survive scaling reported
   receipt to administrative aggregates, under (a) proportional and (b) false-negative-only corrections?
   Feasibility: **high**, and it directly answers the w35680 threat without needing linked data.
3. **Nativity-differential under-reporting check.** Read w35680's subgroup tables (not in the abstract) for any
   nativity, Hispanic-origin or language split. If none exists, that is itself a [GAP] worth recording, and
   NBER w32860 ("Race, Ethnicity, and Measurement Error") is the substitute. Feasibility: **high**, one fetch.
4. **Synthetic-case flag sensitivity on the 2023 GQ cell.** The public PUMS does not carry the synthetic flag, so
   this cannot be run directly; instead bound it by re-running ladder 65's ratio on 2019 (35.4% synthetic) vs 2023
   (45.1%) and asking whether the ratio trend tracks the synthetic-share trend. Feasibility: **medium**, and it is
   a bound, not an identification.
5. **Recent-immigrant CPS coverage correction.** Philadelphia Fed Jan-2025 brief documents delayed sampling of
   recent immigrants. Re-weight or restrict the first-generation cells by years-since-arrival and see whether the
   first-generation fiscal and institutionalization numbers move. Feasibility: **medium.**
6. **Replicate Inkpen 2024's origin split inside Hispanic.** NLSY97/Add Health public files. Question: does
   "Mexican 2G ≈ third-plus Hispanic, other-Hispanic 2G lower" reproduce, and does it reconcile with ladder 74's
   ACS institutionalization ordering (Mexican 1.92 vs Salvadoran 0.89)? Feasibility: **medium**, needs the survey
   files; it is the only self-report cross-check on the repo's administrative ordering.
7. **Re-pin every Texas DPS citation to a post-2024-06 vintage.** Grep the repo for Cato Texas homicide-conviction
   figures and check each is PA-977 (2024-06) or later, since Nowrasteh conceded the pre-2024 series missed
   prison-identified illegals. Feasibility: **high, mechanical.**
8. **Close Q2(f) properly.** One targeted sweep (Google Scholar citing-articles on Chetty et al. 2020 and
   Abramitzky et al. 2021 AER, filtered 2024-2026) to convert "no critique of the OI country-of-origin coding
   found" from a [GAP] into a VERIFIED NEGATIVE. Feasibility: **high**, one epoch.

## Honest gaps in this probe

- [GAP] Semantic Scholar `search_papers` was near-useless for this query shape (returns pre-2020 sociology). All
  productive hits came from Exa. Any re-dispatch should skip S2 and drive Exa plus direct NBER/CES/IZA listings.
- [GAP] NBER w33961 "Immigration and Inequality in the Next Generation" (2025-06) was found but not read; it is
  the most likely place for a US Mexican-second-generation number in this batch.
- [GAP] No Census CES working-paper listing was swept directly; no state ERDC (Texas/California/Florida) linkage
  paper was found; no IPUMS full-count 1880-1940 parental-birthplace second-generation study 2024-26 was found.
- [GAP] No peer-reviewed treatment of the Texas DPS status-matching dispute was located; it remains think-tank.
- [GAP] Q2(c): no 2024-26 critique of the BJS Prisoners Hispanic imputation specifically, beyond Sabol et al.
