**Verdict:** The source-defined 2018 Texas violent-felony arrest-charge comparison reproduces at **103.52 versus 226.45 per 100,000**, unauthorized versus native-born residents: **ratio 0.4571**. The direction survives correction of a real double-subtraction bug. These are recorded arrest charges, not unique offenders or a current-cohort causal crime effect. A second bug inferred prison citizenship from skip patterns and compared 2016 prisoners with a later population; the official recode is now used and the unmatched rate is withdrawn. Official Minnesota and UK audits substantiate institutional and recording failures, but do not identify a numerical U.S. immigration-status detection gap. [SOURCE: raw replication, SPI codebook and primary audits below; INFERENCE]

# Conduct claims with explicit denominators

Date: 2026-09-05. This extends [the cohort narrative audit](immigration-cohort-narratives-2026-09-05.md). No new paid X requests were made; the prior 111-post sample supplied claim locators. The analysis considered six distinct mechanisms before selecting checks: population composition, exposure and opportunity, victim reporting, police detection and recording, prosecutorial selection, and administrative fraud controls.

## 1. A reproduced comparison, with the actual counting unit

Light, He and Robey's openICPSR124923 replication archive contains annual Texas aggregates for 2012–2018 with CMS denominators, and 2012–2017 with Pew denominators. The paper counts **each arrest charge** as an incident; one arrest can have multiple charges. Its state/local felony analysis excludes administrative federal holds. This is neither a count of unique offenders nor a conviction probability. [SOURCE: [published methods](https://doi.org/10.1073/pnas.2014704117), [replication archive](https://www.openicpsr.org/openicpsr/project/124923/version/V1/view); full text and replication code archived locally]

Recalculation from the source counts and population columns:

| 2018 violent-felony group | Arrest charges | Group population | Charges / population × 100,000 |
|---|---:|---:|---:|
| Unauthorized | 1,858 | 1,794,800 | 103.5213 |
| Native-born | 53,837 | 23,773,820 | 226.4550 |
| Study-classified legal immigrants, including naturalized | 5,632 | 3,133,224 | 179.7510 |
| Legal immigrants excluding naturalized, split variant | 2,468 | 1,276,552 | 193.3333 |
| Naturalized, split variant | 3,164 | 1,856,672 | 170.4124 |

The last two rows partition the third; adding all three would double-count. The native-born row is unchanged between the baseline and split files. Their count and population identities hold across all matched years/categories. Across 268 loaded rows, recomputed rates differ from the source's stored float rates by at most **0.00001484 per 100,000**, consistent with numerical storage precision. [CALCULATION: `analysis/tx_rates.csv` and `analysis/numerical-results.json` under the archive root below]

The previous loader instead subtracted naturalized people from the already-native group:

`(53,837 − 3,164) / (23,773,820 − 1,856,672) × 100,000 = 231.2025`.

That produced a spurious native-born variant. The correct unauthorized/native ratio is `103.5213 / 226.4550 = 0.4571385`, a **54.29% lower observed charge rate** in this comparison. The baseline legal-immigrant group also cannot be labeled noncitizen because it includes naturalized citizens. [CALCULATION; SOURCE: replication.do Figure 1 note and published classification rules]

There are 188 comparisons in the repository's dependent year/offense/group/denominator grid. All are below one after repair. This describes the checked cells; it is not 188 independent replications, a probability of truth, demographic standardization, or a universal bound on unobserved offending. CMS/Pew denominators, DHS classification, detection and the state/time scope still matter. [SOURCE: staged `v_crime_spec_curve`; INFERENCE]

## 2. Prison counts: official recode, adult universe and rate withdrawal

The SPI public-use file provides **RV0004**, the official citizenship recode: 1 citizen, 2 noncitizen, 8 missing, with a documented CAPI-missing code. The old loader inferred citizenship from V0950 (“also a U.S. citizen?”), treated many skipped/missing responses as citizens and recognized only eight ambiguous responses. Compared with RV0004, **112 of 24,848 assignments change**. [SOURCE: ICPSR37692 DS0001 codebook, RV0004; `analysis/spi_classification_changes.csv`]

| Official 2016 citizenship group | Sample people | Weighted prisoners | Share of SPI prison population |
|---|---:|---:|---:|
| Citizen, nativity not inferred | 22,982 | 1,319,011.12 | 92.775% |
| Noncitizen | 1,766 | 97,115.93 | 6.831% |
| Ambiguous/missing | 100 | 5,596.95 | 0.394% |

These are weighted survey estimates of prison stock, not crime rates or exact administrative counts. Citizenship is not unauthorized status. [SOURCE: `analysis/spi_official_citizenship.csv`; [ICPSR study](https://www.icpsr.umich.edu/web/NACJD/studies/37692)]

**The adult denominator is justified.** The codebook's “Additional Methodology—Universe” defines the target as people age 18+ held in state prison or serving a federal prison sentence during 2016. The facility sampling frame also included facilities holding sentenced minors; that does not extend the SPI respondent target to minors. The actual **RV0001 minimum is 18, with zero under-18 and zero missing ages among all 24,848 records**. The repaired loader checks this. The universe excludes specified military, immigration-only and other special facilities; this is not all U.S. detention. [SOURCE: codebook printed p.9, extracted lines217–226; empirical age check]

The former rate query selected the **latest** year of the IPUMS panel while retaining the 2016 prison numerator. That does not measure either year's incarceration prevalence. Rates now require a source-labeled, same-year national adult denominator including institutional group quarters. Wrong years, wrong population scope, duplicate groups, missing metadata or invalid populations fail explicitly.

The fresh 2016 Census B05003 API probe returned an HTML **“Missing Key”** page instead of data. No replacement number was fabricated. With SPI raw data present, default `build-context.sh` explicitly requests **counts only** and prints that rates are absent. Public/minimal builds without that gated source explicitly skip SPI; fresh context tables and cleared SPI exports cannot retain stale rates. If `SPI_DENOMINATOR_CSV` is explicitly supplied, including an empty value, validation is mandatory; a missing or invalid supplied file fails. [SOURCE: archived response, actual missing-source probe and repaired caller; GAP: matched denominator not acquired in this run]

## 3. More recent official counts and the limits of their denominators

The newly acquired **FY2024 SCAAP awards PDF** has nine columns, including an application number; the existing FY2023 parser expected eight. The audit parsed **485 applications**, with **416,666,980 total inmate-days**, **7,400,717 DHS-confirmed days**, **7,099,027 unknown-status days** and **$144,957,461 in awards**. The counts and denominator come from the same submitted application rows. These describe participating jurisdictions and custody person-time; they are not unique incarcerated people or population offending rates. The separate FY2023 parser was not repointed to the incompatible FY2024 layout. [SOURCE: [BJA FY2024 award detail](https://bja.ojp.gov/funding/scaap-fy24-awards.pdf), HTTP last-modified 2025-01-16; `analysis/scaap_fy24_awards.csv`]

The local FY2025 solicitation expressly uses custody during **July 1, 2023–June 30, 2024**, requires qualifying conviction and consecutive-custody criteria, and defines qualifying immigration status at incarceration. Its definition includes specified unauthorized entry/expired authorization and deportation or exclusion proceedings. Neither “all foreign-born” nor “all noncitizens” is equivalent. Unknown days are already filtered by applicants' reasonable belief; they are not a random missing-status sample. Awards are prorated reimbursements, not total or marginal incarceration cost. [SOURCE: local `scaap_fy25_solicitation.pdf`, pp.2,6,16–17; [BJA funding rules](https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/funding)]

A Texas DPS primary PDF indexed through **May 31, 2026** reports cumulative select-offense counts for people identified through arrests from June 1, 2011. Its homicide entries are **1,128 arrests and 614 convictions**. Dividing one by the other would not establish a case-level conviction probability without a linked cohort and disposition follow-up. Nor can the cumulative numerator be divided by today's unauthorized stock to get an annual rate. A rolling-table change may include backfilled classifications or dispositions. The PDF download timed out; the primary indexed text is archived, and May 2026 is the snapshot located, not a certification that no newer one exists. [SOURCE: [Texas DPS table](https://www.dps.texas.gov/sites/default/files/documents/administration/crime_records/pages/illegalarstconv.pdf); GAP: local PDF and annual compatible extract]

## 4. Fraud: reconcile the program, case and money measure first

| Official anchor | Program and period | Supported money/count claim | What cannot be added or inferred |
|---|---|---|---|
| Minnesota AG, August 17, 2026 | Reva Health/Medicaid, described operation 2024–2026 | Elmi faces eight felony charges involving over $1m in alleged ineligible/unprovided services | Charges are not convictions; the release's combined two-case total already includes this case |
| DOJ, August 27, 2026 | Feeding Our Future, pandemic child nutrition | Three defendants sentenced in a scheme DOJ describes as $250m | A later sentencing release is not another $250m loss; this is a different program from Medicaid and PPP/EIDL |
| SBA, July 14, 2026 | Pandemic PPP/EIDL loans | 6,900 Minnesota borrowers tied to $400m in suspected fraud | Loan/borrower exposure is not adjudicated net loss; program totals do not establish an ethnic group |
| DOJ, July 24, updated July 27, 2026 | Housing Stabilization Services/Medicaid, April2022–April2025 | Four men pleaded guilty; approximately $2.2m taken through claims associated with approximately350 recipients | Recipients are not thereby perpetrators; this case may already sit inside other enforcement totals |

Sources: [Minnesota AG](https://ag.state.mn.us/Office/Communications/2026/08/17_Medicaid-Fraud.asp), [DOJ Feeding Our Future sentences](https://www.justice.gov/usao-mn/pr/three-defendants-feeding-our-future-fraud-scheme-sentenced-total-155-months-imprisonment), [SBA July14 release](https://legacy.sba.gov/article/2026/07/14/sba-expands-use-palantir-software-accelerate-pandemic-fraud-crackdown), [DOJ HSS guilty pleas](https://www.justice.gov/opa/pr/four-men-plead-guilty-2m-minnesota-medicaid-fraud).

A limited same-case calculation is justified: **$2.2m / 350 ≈ $6,300 of admitted scheme loss per associated recipient over April2022–April2025**. Both inputs are approximate. This is neither an annual amount nor net loss after recoveries, and is not the rate of fraud among beneficiaries, providers, Somalis, refugees or recent immigrants. [CALCULATION: `fraud_case_arithmetic` in the numerical output]

The three federal funding streams involve distinct payments, but people, entities and published enforcement totals can overlap. A sound combined ledger needs case/provider/payment identifiers, adjudication status, paid versus intended loss, recoveries and reference periods. “Fraud detected,” “all program spending,” “suspected loan value,” and a cohort's net fiscal balance are different numerators. No population status or ethnicity was inferred from defendants' names.

**[GAP] The exact new $1b allegation in the prior X sample remains unverified at a public primary source.** The newer July14 SBA source still supplies the $400m Minnesota figure, but does not falsify a later, broader or differently defined $1b total. The figures above must not be summed into a certified net-loss total.

## 5. Underreporting and non-enforcement are testable measurement concerns

For victim-reported crime, distinguish **incident → disclosure/report → police recording → investigation/suspect identification/arrest → prosecutor filing → disposition/conviction**. Police-initiated offenses enter through a different detection route. These transitions may depend on resources, priorities, victim/offender circumstances and institutions. Conditional transition probabilities can be multiplied; treating marginal stage probabilities as independent would be an additional unsupported assumption. [INFERENCE: measurement model]

Light's numerator is **police arrest charges**, so downstream prosecutor declination does not mechanically delete an already recorded arrest charge. Reduced investigation or arrest activity, anticipatory non-enforcement, changes in recording, or feedback from prosecutor policy can affect it. Conviction comparisons additionally reflect prosecution and disposition. Prison stock also reflects sentence duration, release and removal. “Both arrests and convictions are lower” does not eliminate all common upstream selection. [SOURCE: Light's counting rule; INFERENCE]

| Primary audit/schema | Verified finding | Limit on the inference |
|---|---|---|
| Minnesota OLA, June13,2024 | MDE's inadequate oversight created opportunities for Feeding Our Future fraud; it failed to act on warning signs and inadequately investigated complaints. The audit says authority existed despite litigation or negative-press threats. | Supports a concrete institutional failure. It does not estimate missed fraud by immigrant cohort or establish a personal intent by Walz to protect a group. |
| Casey audit, June16,2025 | The published COCAD table has 6,670 records, including4,404 with ethnicity not declared; it warns that excluding unknowns misleads. It also documents local overrepresentation of Asian suspects in specified group-based exploitation data. | Missing ethnicity can distort profiles. Local, selected UK suspect evidence is not a U.S. immigrant rate, and ethnicity does not identify immigration status or religion. |
| FBI NIBRS collection guidelines and SPI2016 schema | NIBRS separates arrestee race and ethnicity; SPI has separate Hispanic-origin (V0015/V1951) and White-race (V0016/V1952) fields. | “White” alone need not mean non-Hispanic White and never identifies native birth or citizenship. |

Sources: [Minnesota OLA review](https://www.auditor.leg.state.mn.us/sreview/pdf/2024-mdefof.pdf), [Casey audit](https://www.gov.uk/government/publications/national-audit-on-group-based-child-sexual-exploitation-and-abuse/national-audit-on-group-based-child-sexual-exploitation-and-abuse-accessible), [FBI data-collection guidelines](https://ucr.fbi.gov/nibrs/nibrs_dcguide.pdf) (historical instrument documentation), and the held SPI codebook/schema.

The Casey table illustrates the denominator issue directly: **1,884 /6,670=28.25%** White among all listed records, versus **1,884 /(6,670−4,404)=83.14%** among records with declared ethnicity. Neither fraction identifies the ethnicity of the missing records or all unobserved offending. This is a missing-data problem with substantive consequences, not permission to choose a preferred ethnic profile. [CALCULATION from the cited table]

This lane's Texas rates use the paper's birthplace/citizenship/DHS categories; the prison calculation uses RV0004. **Neither infers status or native birth from White.** The Texas aggregate files lack the joint race/ethnicity/status information needed for a non-Hispanic-White standardized comparison. A Hispanic person recorded as White can be consistent with separate race and ethnicity questions; ignoring the ethnicity field changes the target comparison. [SOURCE: actual source schema and caller trace]

Lower recorded rates alone cannot settle true-offending rates under differential detection. Conversely, an unmeasured detection hypothesis cannot establish that the ranking reverses. For the 2018 point ratio, with denominator coverage held equal, equality requires the unauthorized group's expected recorded charges per comparable underlying offense to be **45.71%** of the native group's; reversal requires a smaller relative value. Charge multiplicity makes this an effective recording intensity, not necessarily a probability. This is a conditional threshold, not an estimate. Reporting by immigrant victims also cannot directly identify detection of immigrant offenders when victim and offender groups differ. [INFERENCE; see the expanded uncertainty analysis]

## 6. What the latest four calendar years can and cannot show

The latest four completed calendar years here mean **2022–2025**; 2026 is partial.

| Source | Actual observation coverage in this pass | Post-2020 arrival-cohort conduct identified? |
|---|---|---|
| Light replication | 2012–2018 CMS;2012–2017 Pew | No: aggregate year/offense/status tables predate the cohort |
| SPI public-use file | 2016 survey | No for recent cohorts; it does contain binary birthplace and years lived in the U.S., so lack of all residence-duration information would be a false claim |
| SCAAP FY2024 award data/FY2025 solicitation | Award year and custody period are distinct; FY2025 rules specify July2023–June2024; FY2024 custody-period crosswalk was not reverified here | No arrival-year field in award aggregates; no population offending denominator |
| Texas DPS located snapshot | Cumulative June2011–May2026 select-offense counts | No annual2022–2025 or entry-cohort split in the located table |
| HSS guilty-plea case | April2022–April2025 conduct, July2026 pleas | Conduct during much of the requested period, but no origin/admission/entry-cohort population denominator |
| Casey audit | Specific local2020–2025 records and national2023 data, documented2025 | UK selected suspects and recording systems; no transfer to recent U.S. cohorts |

The held Light aggregates have no entry year, country-of-origin-by-status cell, religion, individual identifier or validated extremism measure. SPI V0945 is U.S./other-country birthplace; detailed citizenship-country fields are suppressed, while V0951 records years lived in the U.S. Its age and observation date independently prevent a2021–2024 arrival analysis. The codebook's offense term “terroristic threat” is not a validated measure of ideological extremism. SCAAP awards contain jurisdiction/application, salary, days and award fields. These schemas demonstrate specific ceilings; they do not establish that every possible external dataset lacks the required fields. [SOURCE: `analysis/source_schema.json` and source codebook]

## Reproduction, validation and promotion

Archive root: `.scratch/clarity-next-20260905/conduct/`.

```bash
uv run --with pandas --with pyreadstat --with pdfplumber python3 \
  infra/immigration-fiscal/build/analyze_conduct_denominators.py \
  --data-root /Volumes/2TBPNY/research-data/immigration-fiscal/data \
  --output .scratch/clarity-next-20260905/conduct/analysis \
  --scaap-awards .scratch/clarity-next-20260905/conduct/scaap_fy24_awards.pdf

uv run --with pandas python3 -m unittest discover \
  -s infra/immigration-fiscal/tests -p test_conduct_status.py -v
```

For the isolated rebuild, set `PNY_DATA_ROOT` to that data root, `DERIVED_ROOT` to the archive's `staged/` directory and `DUCKDB_PATH` to `staged/validation.duckdb`. Initialize that empty database, then run `build_status_crosswalk.py`, `load_light_tx_crime.py`, `load_spi_citizenship.py --counts-only`, and `build_crime_views.py`, using DuckDB/pandas/pyreadstat dependencies as needed. **No canonical database was written.**

Six focused regression tests pass, including source-cell conservation, unresolved citizenship/nativity, unknown code rejection, SPI missingness, age and matched-denominator checks. The staged database contains **268 TX rows and188 grid rows**, identical native counts/rates across CMS and CMS_nat, and **no SPI rate table**. `staged/validation.json` records the query checks. The crime views have no dependency on the absent SPI rate. The unified builder recreates its destination database before copying current source tables/views (`build_unified_warehouse.py:78–108`), so a rebuild from the corrected source removes the old rate; **parent promotion and final union-absence verification remain the parent's responsibility**.

Changed code surfaces: `load_light_tx_crime.py`, `load_spi_citizenship.py`, `build_status_crosswalk.py`, `build_crime_views.py`, `build-context.sh`, the new analyzer and its focused tests. The ratio view now names its fields `native_born_rate_per_100k` and `rate_vs_native_born`; no other tracked code caller of the replaced column names was found. Broad canonical categories now retain unresolved citizenship/nativity instead of assigning a finer class. USSC code values remain explicitly unverified.

Current prose for parent repair, captured before peer integration: **confidence ladder:234** (native231, mixed-citizen explanation, SPI0.86 and universal direction); **dataset register:237** (CMS_nat described as adding a true-native split); **economist dismantling:68** (broad crime claim invokes the invalid SPI rate). Exact locator output is archived. No shared prose was edited by this lane.

**Included:** prior111-post claim archive and official case anchors; all three Light aggregate variants and replication instructions; SPI public-use schema/codebook and required analysis columns; local FY2023 SCAAP parser/source and FY2025 solicitation; new FY2024 awards; primary paper body; OLA, Casey and FBI source excerpts; all owned generators/tests and staged results. Source and artifact hashes are in `manifest.json`.

**Skipped with reasons:** new paid X retrieval (unnecessary); restricted applications and external messages (not authorized); a formal new SPI rate (matched denominator missing); current individual cohort/extremism rates (fields/time coverage absent in held artifacts); demographic standardization of the Texas aggregates (joint fields absent); a certified combined fraud total (case/payment overlap and recovery reconciliation incomplete); canonical DB/index/union writes (parent-owned). Public files downloaded were far below300MB; the missing-key Census response and timed-out DPS PDF are recorded as access failures, not negative findings.

## Revisions

- **2026-09-05 — Corrected source classification and measurement inference.** The first-pass reading of an old loader comment incorrectly suggested Light's baseline citizen group mixed native and naturalized people. The primary paper, replication code and conservation of raw cells disproved that interpretation. The actual double-subtraction and legal-group mapping errors were repaired. This is an observed LLM/source-summary failure, not a hypothetical neutrality claim. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).
