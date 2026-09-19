# How many unauthorized residents there are: definition, coverage and flow

**Verdict:** The repo's 14–15M is not too low. On the definition every publisher uses, no permanent status with parolees, TPS, DACA and pending asylum applicants included, the central range is 14.6–15.8M for mid-2024 and 15.4–16.7M for January 2025, each with its publisher's own coverage adjustment; on the narrow definition, no lawful status and no protection from removal, it is 8–9.5M (Pew's directly estimated split gives 8.0M of its 14.0M for July 2023). The repo's own residual reproduces exactly on CPS ASEC 2025 (14,896,401, SE 316,399; Mexico-born 4,567,144) and gives 12,973,901 (SE 98,154) on ACS 2024 with the same rules; rule choices move it by about 4%, the coverage assumption by up to 62%, and nearly all of that spread sits in the 2021–2024 arrival cohort. The one measured coverage rate, the 2020 Post-Enumeration Survey's 4.99% Hispanic net undercount, supports a multiplier of 1.05 against the 1.22 the Center for Migration Studies assumes, and the ACS 2024 and ASEC 2025 weights already embed the Census Bureau's December 2024 upward revision of net international migration, so layering a recent-arrival undercount on top partly adjusts twice. A stock-flow identity from the DHS January 2022 stock forward on CBO's net other-foreign-national series gives 16.7M for January 2025, above every survey, and moves by 2.7M across a 50–100% residency share for border releases and gotaways. The stock has been falling since early 2025 (CBO net −360,000 for 2025; CIS reads 13.5M for July 2026). No defensible definition reaches 40M: every non-citizen in the ACS is 24.4M, and the largest unauthorized-adjacent construction, applying a 65% undercount to all of them, is 38.1M; the only rungs above 40M count US citizens (non-citizens plus every US-born household member 42.2M; all foreign-born 50.3M). The 40.9M Mexican-origin union is a different population, overwhelmingly citizens. [SOURCE: `infra/immigration-fiscal/unauthorized_population_size_2026_09_19/RESULT.md`, `derived/`, `sources.json`] [FRAMING-SENSITIVE: the definition is worth 5–6M and must be stated with every figure]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/unauthorized_population_size_2026_09_19/`.

## 1. Definition

DHS OHSS: "Individuals who were paroled into the United States are considered to be unauthorized immigrants until they are admitted or otherwise acquire immigration status", with TPS, DACA and people awaiting removal proceedings likewise included [SOURCE: OHSS April 2024, Definitions, quoted in `derived/published_definitions.md`]. Pew, CMS and MPI follow the same convention; Pew alone splits its headline (8.0M without deportation protection, 6.0M with: asylum applicants 2.6M, border releases 1.0M, parole 0.7M, victims 0.7M, TPS 0.65M, DACA 0.6M) [SOURCE: Pew, 21 August 2025]. CMS: "More than one-third of the 'undocumented' (5.4 million) in these estimates are, in fact, documented and known to the federal government." Narrow definition mid-2024: 9.2M (CMS), 9.4M (MPI, a floor).

## 2. Published estimates

| Source | Date | Estimate | Coverage adjustment | Mexico-born |
|---|---|---|---|---|
| DHS OHSS | Jan 2022 | 10.99M | 13% at arrival, decaying 7.5%/yr | 44% |
| Pew | Jul 2023 | 14.0M | applied, rate not printed | 4.3M |
| MPI revised | Jul 2023 | 14.7M | applied, rate not printed | |
| CMS | Jul 2024 | 14.61M | 5% pre-2021, 37% for 2021–24 | 5.1M |
| MPI | Jul 2024 | 15.75M | applied, rate not printed | 5.52M |
| CIS | Jan 2025 | 15.4–15.8M | 2.25% flat | |
| CIS | Jul 2026 | 13.1–13.5M | 2.25% flat | |

CIS reaches the highest figure with the smallest coverage adjustment; the difference is a smaller legal-stock estimate, not a bolder undercount. [SOURCE: `derived/published_estimates.csv`, primary documents quoted in `derived/published_definitions.md`]

## 3. Residual reproduced

Borjas 2017 rules via `status_impute_2026_09_16/impute_status.py` unmodified: CPS ASEC 2025 14,896,401 (ladder 85 exactly); ACS 2024 PUMS 12,973,901 with rule (f), subsidised housing, unavailable in the ACS, so the 1.9M survey gap runs opposite to the missing rule. Rule sensitivity: dropping the occupation rule +2.2%, wide refugee list −4.4%. Arrivals 2022 or later in the CPS residual: 3.80M; the right comparison is CBO's net 2022–24 inflow of 5.7M, not the 8.7M gross figure the repo's earlier note used. [SOURCE: `derived/cps2025_summary.json`, `acs2024_residual_by_yrsince.csv`, `rule_sensitivity.csv`] [CALCULATION]

## 4. Coverage

One ACS base, six schemes: none 12.97M; CIS 2.25% 13.27M; PES 4.99% 13.66M; DHS 13.95M; CMS 15.86M; CMS's highest country rate (65%, Ecuadorians 2021–24) on every recent arrival 21.08M. Every cohort before 2021 moves under 6% on any scheme; the 2021–24 cohort moves from 4.11M counted to 4.21–11.75M. The ACS 2024 weighted total is 340,110,990 against Vintage 2024's 340,110,988, and Vintage 2024 raised net international migration for 2021–22 and 2022–23 by 70% and 102% to account for 75% of humanitarian migrants missed by the ACS [SOURCE: Census Bureau, Random Samplings, 19 December 2024], so the counted residual is already partly adjusted and CMS's 37% partly double-counts; the tension is real and not a refutation, since CMS calibrates to DHS release counts. The CPS grid figure of 18.1M under CMS rates should not be quoted for the same reason. [SOURCE: `derived/coverage_grid.csv`, `coverage_grid_by_cohort.csv`, `cps2025_coverage_grid.csv`] [CALCULATION]

## 5. Stock-flow

DHS 10.99M (Jan 2022) plus CBO net other-foreign-national migration of 2.0M (2022), 2.4M (2023), 1.3M (2024), −0.36M (2025) [SOURCE: CBO, Demographic Outlook 2026–2056, Appendix B] gives 15.39M (Jan 2024), 16.69M (Jan 2025), 16.33M (Jan 2026). DHS disposition tables through November 2024 give FY2022–24 releases, paroles and HHS transfers of 3.81M plus 1.63M known gotaways (FY24 partial, [UNVERIFIED] for the FY24 figure) against 0.61M removals; at 100% residency they account for 5.44M of CBO's 5.70M, leaving implausibly little for overstays, and at 70% the accounting reconciles. The implied stock moves 2.7M across a 50–100% residency share. For 2025–26 CBO's −360,000 and CIS's −2.3M cannot both be right. [SOURCE: `derived/stock_flow_*.csv`] [CALCULATION]

## 6. The 40M ladder

Borjas residual 12.97M; with DHS coverage 13.95M; with CMS 15.86M; with the upper-bound scheme 21.08M; CPS residual 14.90M; every non-citizen 24.40M; non-citizens with the upper-bound scheme 38.08M; non-citizens plus US-born children under 18 in their households 34.54M; non-citizens plus every US-born household member 42.16M (17.75M of them citizens by birth); all foreign-born 50.28M (about half naturalised). Reaching 40M by scaling non-citizens needs a 39% undercount of every non-citizen. [SOURCE: `derived/forty_million_ladder.csv`] [CALCULATION]

## 7. Limits and what was skipped

Coverage is assumed in every published estimate and measured only by the PES, which is a net decennial rate for all Hispanics, a floor rather than a substitute. Administrative anchors (SSA Earnings Suspense File, ITIN filers, matrícula issuance, emergency Medicaid, city shelter intakes, K-12 recent arrivals) and the Jensen et al. 2015 Census coverage factors were not obtained; two helper agents exhausted their turns. Each anchor bounds rather than point-estimates and would not move the verdict. No DHS disposition table exists after November 2024. Coverage-adjusted figures carry no sampling SE by design. Resident groups, not admission; no policy advice.

## Sources

DHS OHSS unauthorized estimates (April 2024) and enforcement monthly tables (November 2024); Pew (21 August 2025); Warren, Allen and Pacas, JMHS (July 2026); MPI (2026); Camarota and Zeigler, CIS (March 2025, September 2026); CBO Demographic Outlook 2026–2056 (January 2026); Census Bureau CB22-CN.02 (10 March 2022) and Random Samplings (19 December 2024); ACS 2024 1-year PUMS; CPS ASEC 2025; `status_impute_2026_09_16`; ladder 85.
