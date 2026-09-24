**Verdict:** Federal courts sentence noncitizens for fraud at 1.8–2.0 times the citizen rate per adult. That is about their ratio for all federal crime outside immigration (1.84). In government-program fraud the gap shrinks from 1.9× in cases to 1.1× in dollars.

- **Rates, FY2015–FY2024:** per year and per 100,000 adults of the same status, 2.1 US citizens and 3.7 resident noncitizens were sentenced under the fraud guideline (§2B1.1). That is a ratio of 1.8, or 2.0 over FY2018–24.
- **By status:** on the Commission's own codes, "illegal aliens" ran at 3.6 per 100,000 (band 3.3–4.4) and legal aliens at 3.5 (3.2–4.3).
- **Legal noncitizens lean toward fraud:** 1.7× the citizen rate for fraud and 2.0× for health-care fraud, against 1.1× for all non-immigration crime.
- **Dollars:** in government-program fraud sentenced FY2018–22, noncitizens were 14.6% of offenders but held 8.5% of guideline loss, against 7.7% of adults. On GAO's $233–521bn a year of federal fraud, that implies about $20–44bn a year by noncitizens and $213–477bn by citizens [CALCULATION; assumes sentenced cases represent all fraud].
- **Minnesota (alleged / proven / recovered):**
  - Feeding Our Future: $250m alleged, 18–30% of FY2018–22 child-nutrition payments to sponsors; 65 convicted; no aggregate proven loss.
  - Housing Stabilization: $30.5m alleged; $5.7m stated in plea releases; $302m paid in 2021–mid-2025.
  - EIDBI: $21.2m paid on $46.6m billed.
  - CCAP: $4.6m in one case.
  - No document gives aggregate restitution or recovery for any scheme.
- **Origin:** no DOJ release, court or auditor document read states a defendant's origin or citizenship.
  - "85 of Somali descent" comes from DOJ and Attorney General social-media posts, quoted in a House report, with no method.
  - The "$9 billion" is a prosecutor's spoken "very possible" about half of $18bn of total spending. A House staff report restated it as a DOJ estimate of federal loss.
- **Our account:** these dollars already sit inside BEA program totals and are charged to program users. The Mexican-origin union carries 12.25% of Medicaid, fraud included: $1.17bn per percentage point of Medicaid fraud. At a 5.6% perpetrator share, a perpetrator key would assign $0.64bn less per point.

Scope: BRIEF.md tasks 1–4, run 2026-09-24. Task 1 is `ussc_fraud.py`. Tasks 2–3 used a research subagent whose case file (`_cache/mn/MN_CASES.md`) I spot-checked against the saved primary documents (§3.5).

## 1. Sentencing Commission: federal fraud by citizenship

### 1.1 Data, definitions and checks

**Sentenced individuals** [SOURCE: USSC individual offender datafiles FY2015–FY2024, CSV, <https://www.ussc.gov/research/datafiles/commission-datafiles>; codebook "Standardized Research Data Documentation for Fiscal Years 1999–2025", revised April 7, 2026]:
- 663,377 records, about 27,000 columns per year [DATA: derived/validation.json].
- Read with pyarrow, which is already in the repo `.venv`, so no `--with` reader is needed.
- The Commission's economic-crime files classify every §2B1.1 case into one type (health care, government benefits, ...). They join on `USSCIDN` for 98.1–99.0% of §2B1.1 cases a year [DATA: derived/validation.json].

**Citizenship** (`CITIZEN`, from the PSR; codebook PDF p.23): "1 = U.S. Citizen, 2 = Resident/Legal Alien, 3 = Illegal Alien, 4 = Not a U.S. Citizen/Alien Status Unknown, 5 = Extradited Alien".
- "Illegal alien" is the Commission's code, not ours.
- Naturalized citizens are code 1, so citizenship is not nativity.
- `CITWHERE` gives country of citizenship; `HISPORIG` gives Hispanic origin.

**Loss** (`LOSSHI`, codebook PDF p.37): "The dollar amount of loss for which the sentenced individual is held responsible."
- It is the guideline loss: "loss is the greater of actual loss or intended loss" [SOURCE: USSG §2B1.1 comment. n.3(A), 2023 Manual, `_cache/refs/ussg2023_GLMFull.pdf` p.100].
- In government health-care cases, "the aggregate dollar amount of fraudulent bills submitted … shall constitute prima facie evidence of the amount of the intended loss" (n.3(F)(viii), p.103).
- The public file does not say which of actual or intended loss applied, so read these amounts as intended-or-actual. For health care they usually mean billed.
- Co-defendants can each be held responsible for the reasonably foreseeable loss of the jointly undertaken scheme (§1B1.3(a)(1)(B), p.31). Sums over offenders therefore double count schemes.
- Dollar sums use the 45,386 of 56,693 §2B1.1 cases with a usable amount. 10,755 are coded "Some Loss, Amount Not Specified", and 552 are missing or flagged by `LOSSPROB` as inconsistent with the guideline range; the codebook advises screening those out (p.37).
- "Positive loss" below means `LOSSHI` above zero, which includes the amount-not-specified cases.

**Two fraud definitions**, because they catch different people:
- **Primary guideline §2B1.1** (`GDLINEHI`), FY2015–24, 56,693 offenders. This is the universe of the loss variable and the economic-crime types.
- **Commission offense type "Fraud/Theft/Embezzlement"** (`OFFGUIDE` 16, FY2018+). This is the Sourcebook definition. It adds 297–683 cases a year that have no §2B1.1 computation. Among illegal aliens those cases are identity-document offenses: 18 USC 1028(a)(4) in 499 of 1,047 and 1028(b)(6) in 319 [DATA: derived/top_statutes.csv]. Their median prison term (`SENSPLT0`) is 3.1 months in FY2019 and 1.0 in FY2024 [CALCULATION: one-off check, not written to derived/].

**Denominators:**
- ACS 1-year B05003 supplies citizen adults (native plus naturalized) and noncitizen adults; FY *t* is matched to ACS *t*. FY2020 uses the mean of 2019 and 2021, because there is no standard 2020 1-year release [DATA: derived/denominators.csv].
- The register lists no annual unauthorized series, so noncitizen adults are split with a share *s* = 0.50 unauthorized (band 0.45–0.55), taken from **Pew Research Center** (Passel & Krogstad, August 21, 2025; local PDF):
  - Pew 2015: 11.0M against 22.6M ACS noncitizens, 0.487.
  - Pew 2019: 10.2M against 21.7M, 0.469.
  - Pew 2021: 10.5M against 21.2M, 0.495.
  - Pew 2023 on its own base: 14.0M against 28.0M, 0.500 (p.5 chart; p.10 lawful 37.8M, naturalized 23.8M).
  - The repo's ACS 2024 residual: 12.97M against 24.4M, 0.532 [DATA: derived/unauth_share_check.csv].
- Rates are per 100,000 adults of the same status, and "resident noncitizens" means codes 2–4. Code 5 (extradited) is excluded from rates.
- The central legal and illegal rates use *s* = 0.50 and leave out code-4 cases. Each band has two ends. The low end uses the bigger denominator. The high end adds every code-4 case and uses the smaller denominator.

**Validation:**
- The script reproduces Sourcebook Table 9 exactly for Fraud/Theft/Embezzlement [SOURCE: `_cache/ussc/sourcebook/table9_2019.pdf`, `table9_2022.pdf`; `../detention_evidence_2026_09_20/_cache/ussc_2024_table9.pdf`]:
  - FY2019: 6,328 cases; 5,116 citizens; 1,212 noncitizens.
  - FY2022: 5,489 / 4,645 / 844.
  - FY2024: 5,287 / 4,569 / 718.
- Record totals match too: 76,538, 64,142 and 61,678 [DATA: derived/validation.json].
- Repeated runs of `ussc_fraud.py` produced byte-identical sha256 for all 16 derived files (§8).

### 1.2 Offenders and rates per year, §2B1.1

| FY | US citizens | Legal aliens | Illegal aliens | Unknown + extradited | Citizen rate | Resident noncitizen rate | Ratio | Legal-alien rate (band) | Illegal-alien rate (band) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2015 | 6,939 | 474 | 368 | 53 | 3.06 | 4.26 | 1.39 | 4.56 (4.15–5.52) | 3.54 (3.22–4.39) |
| 2016 | 6,244 | 445 | 313 | 95 | 2.73 | 4.02 | 1.47 | 4.31 (3.92–5.57) | 3.03 (2.76–4.15) |
| 2017 | 5,488 | 471 | 331 | 57 | 2.37 | 4.05 | 1.71 | 4.56 (4.15–5.43) | 3.21 (2.91–3.93) |
| 2018 | 5,091 | 435 | 365 | 51 | 2.18 | 4.13 | 1.89 | 4.30 (3.91–5.17) | 3.60 (3.28–4.40) |
| 2019 | 4,810 | 382 | 440 | 71 | 2.04 | 4.36 | 2.13 | 3.85 (3.50–4.77) | 4.43 (4.03–5.42) |
| 2020 | 3,509 | 271 | 509 | 58 | 1.48 | 4.16 | 2.81 | 2.76 (2.51–3.48) | 5.19 (4.72–6.17) |
| 2021 | 3,601 | 262 | 329 | 39 | 1.51 | 3.18 | 2.11 | 2.70 (2.46–3.29) | 3.39 (3.09–4.06) |
| 2022 | 4,458 | 320 | 368 | 58 | 1.85 | 3.70 | 2.00 | 3.24 (2.95–4.08) | 3.73 (3.39–4.62) |
| 2023 | 4,241 | 292 | 314 | 46 | 1.76 | 3.09 | 1.76 | 2.83 (2.57–3.48) | 3.04 (2.76–3.72) |
| 2024 | 4,417 | 235 | 309 | 49 | 1.80 | 2.62 | 1.46 | 2.15 (1.95–2.69) | 2.82 (2.56–3.44) |
| **Pooled** | **48,798** | **3,587** | **3,646** | **577** | **2.07** | **3.75** | **1.81** | **3.53 (3.21–4.35)** | **3.58 (3.26–4.41)** |

Rates are per 100,000 adults of the same status [DATA: derived/rates_per_100k.csv, offense `fraud_2B1.1`]. 85 cases lack citizenship. Citizen adults run from 227.0M (2015) to 245.3M (2024), noncitizen adults from 19.4M (2021) to 21.9M (2024) [DATA: derived/denominators.csv].

**Loss held responsible**, §2B1.1 [DATA: derived/fraud_by_citizenship_year.csv]:

| FY | Sum, all offenders ($bn) | Median, citizens | Median, legal aliens | Median, illegal aliens | Amount not specified (cases) |
|---|---:|---:|---:|---:|---:|
| 2015 | 14.0 | $129k | $239k | $95k | 1,542 |
| 2016 | 10.4 | $135k | $227k | $97k | 1,240 |
| 2017 | 26.9 | $138k | $274k | $96k | 1,064 |
| 2018 | 12.1 | $132k | $224k | $65k | 1,241 |
| 2019 | 17.4 | $138k | $233k | $51k | 1,243 |
| 2020 | 6.7 | $114k | $174k | $0 | 715 |
| 2021 | 17.9 | $135k | $290k | $29k | 834 |
| 2022 | 16.4 | $166k | $213k | $40k | 1,061 |
| 2023 | 16.2 | $187k | $393k | $124k | 907 |
| 2024 | 12.4 | $205k | $588k | $199k | 908 |
| Pooled | 150.4 | $145k | $259k | $60k | 10,755 |

Summed loss, pooled: citizens $114.3bn, legal aliens $20.2bn, illegal aliens $10.6bn, unknown status $3.9bn, extradited $1.3bn. A few cases dominate the sums:
- 15 legal-alien offenders with at least $100m each account for 77% of their group's summed loss.
- 17 illegal aliens account for 69% of theirs.
- 132 citizens account for 47% of theirs.
- The FY2017 spike comes from two legal-alien offenders who hold $8.9bn of their group's $9.7bn that year.

Use the medians and the government-program subset (§1.4, §2.3) rather than raw sums.

### 1.3 Is the gap specific to fraud?

Pooled FY2018–2024, the window in which the Commission's offense type exists [DATA: derived/rates_per_100k.csv, derived/ratio_by_offense.csv]:

| Offense | Citizens /100k | Resident noncitizens /100k | Ratio | Legal aliens /100k (× citizen) | Illegal aliens /100k (× citizen) |
|---|---:|---:|---:|---:|---:|
| §2B1.1 fraud | 1.80 | 3.59 | 1.99 | 3.11 (1.7) | 3.73 (2.1) |
| §2B1.1 with positive loss | 1.75 | 2.95 | 1.69 | 2.93 (1.7) | 2.65 (1.5) |
| §2B1.1 plus fraud schemes sentenced as laundering (§2S1.1 with a fraud statute) | 1.86 | 3.74 | 2.01 | 3.26 (1.8) | 3.85 (2.1) |
| Commission type Fraud/Theft/Embezzlement | 1.89 | 4.49 | 2.37 | 3.28 (1.7) | 5.21 (2.8) |
| Drug trafficking | 6.23 | 16.75 | 2.69 | 8.53 (1.4) | 23.11 (3.7) |
| Firearms | 3.32 | 1.66 | 0.50 | 0.62 (0.2) | 2.62 (0.8) |
| Money laundering | 0.35 | 1.61 | 4.67 | 1.43 (4.1) | 1.61 (4.7) |
| Child pornography | 0.53 | 0.21 | 0.40 | 0.19 (0.4) | 0.21 (0.4) |
| **All offenses except immigration** | **15.58** | **28.64** | **1.84** | **16.63 (1.1)** | **37.52 (2.4)** |

The legal/illegal columns use *s* = 0.50; their bands are in `rates_per_100k.csv`.

What the table shows:
- **All noncitizens:** the §2B1.1 ratios of 1.7–2.0 bracket the 1.84 for all non-immigration federal crime, so the gap is not specific to fraud. The Commission type's 2.4 is higher because it adds document cases.
- **Legal noncitizens:** fraud is where they stand out, at 1.7× against 1.1× overall, along with money laundering at 4.1×.
- **Unauthorized immigrants:** fraud with a real loss is less over-represented (1.5×) than their non-immigration offending overall (2.4×).
- **The broader Commission type** raises the illegal-alien rate because it adds short document cases.
- **Trend:** the §2B1.1 citizen–noncitizen ratio rose from 1.4 (FY2015) to 2.8 (FY2020) and fell back to 1.5 (FY2024). Both groups fell over the decade, citizens faster until FY2020.

### 1.4 Health-care and government-benefits fraud

Economic-crime types within §2B1.1, pooled FY2015–2024 [DATA: derived/rates_per_100k.csv; derived/fraud_subtypes_by_citizenship.csv]:

| Type | Citizens: offenders, loss | Legal aliens | Illegal aliens | Rate /100k: citizen / legal / illegal |
|---|---|---|---|---|
| Health care | 3,772, $21.3bn | 331, $1.11bn | 126, $0.78bn | 0.160 / 0.325 / 0.124 |
| Government benefits | 4,582, $4.27bn | 216, $0.15bn | 641, **$0.05bn** | 0.194 / 0.212 / 0.630 |
| Government benefits, positive loss only | 4,508 | 194 | 258 | 0.191 / 0.191 / 0.254 |
| Government procurement | 578, $1.31bn | 19, $0.03bn | 9, $0.05bn | 0.025 / 0.019 / 0.009 |

**Government benefits, illegal aliens.** The high "government benefits" rate for illegal aliens reflects Social Security number cases, and little money was lost.
- 477 of the 641 cases include 42 USC 408(a)(7)(B), false representation of a Social Security number [DATA: derived/top_statutes.csv].
- The median loss is $0.
- Citizens' benefit-fraud cases most often cite wire fraud (1,302 of 4,582), conspiracy (18 USC 1349 in 843, 371 in 739), mail fraud (312), SNAP fraud (7 USC 2024(b), 192) and theft of public money (18 USC 641, 185). Only 167 cite the SSN statute.
- Counting only cases with a positive loss, illegal aliens run 1.3× the citizen rate.

**Health care.** Legal aliens run at 2.0× the citizen rate; illegal aliens run below it.

**Loss is intended or actual.** Health-care loss is usually billed amounts (n.3(F)(viii)).

The Commission's type "Government Benefits Fraud" means "Defrauding of government agencies providing assistance programs such as social security, disaster assistance, unemployment and retirement benefits, and educational loans" [SOURCE: economic-crime codebook PDF p.6].

### 1.5 Hispanic origin

Pooled FY2015–2024, §2B1.1, per 100,000 adults (denominator ACS B05003I) [DATA: derived/fraud_by_hispanic_citizenship.csv]:
- Hispanic citizens: 2.09. Non-Hispanic citizens: 1.99.
- Hispanic resident noncitizens: 3.40. Non-Hispanic resident noncitizens: 4.06.
- 1,607 cases lack Hispanic origin.

Within government-program fraud sentenced FY2018–22 [DATA: derived/gov_victim_fraud_by_origin.csv]:
- Hispanic defendants are 24.0% of offenders and 18.1% of loss, against 16.7% of adults.
- 76% of that Hispanic loss was sentenced in the Southern District of Florida, where Cuba is the top noncitizen country (§1.6) [CALCULATION: the district holds 23.2% of all loss].
- Outside that district, Hispanic defendants are 17.9% of offenders but **5.6% of loss**.
- Noncitizens with Mexican citizenship are 3.5% of offenders and 0.05% of loss.

### 1.6 Country of citizenship and districts

Noncitizen §2B1.1 offenders by country, pooled FY2015–2024. 7,745 of the 7,810 noncitizen offenders, extradited included, have a country recorded [DATA: derived/fraud_by_country_pooled.csv]:

| Country | Fraud offenders (legal / illegal) | Health care | Gov. benefits | Card and financial | Commission fraud type as share of non-immigration sentences, FY2018–24 |
|---|---|---:|---:|---:|---:|
| Cuba | 1,165 (800 / 253) | 218 | 25 | 604 | 53% (806 of 1,519) |
| Mexico | 1,031 (272 / 731) | 19 | 316 | 65 | 5.8% (1,298 of 22,277) |
| Dominican Republic | 480 (249 / 211) | 29 | 123 | 87 | 11% |
| Nigeria | 443 (228 / 179) | 22 | 20 | 103 | 63% |
| Romania | 431 (56 / 342) | 0 | 9 | 311 | 84% |
| Guatemala | 329 (16 / 305) | 2 | 106 | 5 | 30% |
| Honduras | 294 (14 / 272) | 2 | 51 | 7 | 17% |
| India | 192 (112 / 71) | 26 | 8 | 13 | 44% |
| Somalia | 18 (15 / 1) | 6 | 5 | 1 | 38% (12 of 32) |
| Kenya | 22 (12 / 8) | 1 | 4 | 2 | 34% (12 of 35) |

For comparison, fraud is 12.1% of US citizens' non-immigration federal sentences and 15.7% of resident noncitizens' (FY2018–24).

**Where government-program fraud is sentenced.** This is health care, benefits and procurement, FY2015–2024: 10,362 offenders and $29.4bn of guideline loss [DATA: derived/gov_victim_fraud_by_district.csv]:
- **Southern District of Florida:** 12% of offenders and **26% of loss** ($7.55bn); 22% of its offenders are noncitizens, and Cuba is the top noncitizen country (232).
- **Five districts** hold 51% of loss: S.D. Fla., N.D. Tex., S.D. Tex., C.D. Cal. and S.D. Cal.
- **Top noncitizen countries by district:** Armenia (12) in C.D. Cal. (Los Angeles), India (14) in E.D. Mich., Dominican Republic (14) in S.D.N.Y.
- **Massachusetts:** noncitizens are 50% of offenders (Dominican Republic 90) but hold 4.4% of the district's loss.
- **Minnesota:** 70 offenders and $332m. Noncitizens are 19% of offenders and hold 1.9% of the district's loss; Somalia is the top noncitizen country (5).

These are recorded citizenship countries, not ancestry, and the counts are district-wide, not city-wide.

### 1.7 Caveats

- **Federal only, and prosecution selects.**
  - Noncitizens reach federal court through immigration-linked investigations and SSN and document statutes (§1.4).
  - Much Medicaid provider fraud is prosecuted by state Medicaid Fraud Control Units in state courts and never appears here [INFERENCE].
  - Federal rates therefore do not measure offending.
- **Citizenship is not nativity.** Naturalized immigrants count as citizens. Origin-specific fraud among naturalized immigrants (§3.3) is invisible in these rates.
- **The numerators include people the denominators miss.** A short-term visitor sentenced here is presumably coded "Resident/Legal Alien" but is not in the ACS, which counts people living here two months or more [INFERENCE; the codebook does not say]. ACS also undercounts unauthorized immigrants: the coverage adjustments compared in `../unauthorized_population_size_2026_09_19/RESULT.md` §4 run from 2% to 16%, and the 2020 Post-Enumeration Survey measured a 5.0% Hispanic net undercount. An undercount of that size overstates the illegal-alien rates by the same proportion, most in FY2022–24 when recent arrivals were many.
- **The legal/illegal split is modelled.** It rests on *s* = 0.45–0.55, and the Commission's code 4 adds further uncertainty. Both are carried in the bands.
- **The economic-crime types changed in FY2020** (codebook PDF p.3). "Retirement/Unemployment" and "Disaster" folded into "All Other", while the FY2020+ definition of Government Benefits names unemployment. Pandemic UI cases may sit in either.

## 2. Account implication

### 2.1 Where the dollars sit

Fraud dollars are already inside BEA's 2024 program totals. The account assigns each line by a use key, not by who committed the fraud. Lines and preferred keys come from `../full_account_spending_2026_09_20/derived/allocations.csv`, scenario `complete_preferred_F_per_capita`, personal allocation; BEA footnotes come from the pinned Section 3 workbook, T3.12:

| Minnesota scheme | BEA line (Table 3.12) | Account category, 2024 total | Key; union share |
|---|---|---|---|
| Housing Stabilization, EIDBI (Medicaid) | Medicaid, line 33 ($938.2bn) | `medicaid_and_chip_other_medical`, $954.2bn (lines 33–34) | MEPS 2024 payer means by age × birth; **12.25%** of the national total |
| Feeding Our Future, CACFP/SFSP | [INFERENCE] federal "Other", line 26 (fn 7: "payments to nonprofit institutions"), or state and local "Other", line 39 (fn 11: "payments to nonprofit welfare institutions") | `other_federal_benefits` $86.4bn or `other_state_welfare` $22.4bn | all-cash receipt, 4.6%; or WIC receipt, 22.9% |
| CCAP (child care) | [INFERENCE] "Family assistance", line 35 (fn 9: "assistance programs operating under the Personal Responsibility and Work Opportunity Reconciliation Act of 1996"; CCDF was created by that Act) | `family_and_general_assistance`, $63.1bn | CPS cash assistance, 16.7% |

The union share is target key share times the 0.990 household pool fraction; 12.25% = 0.12376 × 0.99005 [CALCULATION]. BEA's program crosswalk for the child-nutrition and child-care lines was not checked [GAP].

**Timing.** The account is income-year 2024. Feeding Our Future's money went out in 2020–22 and is outside it. Minnesota's 2024 HSS payments ($104m, DOJ) and EIDBI cost ($324.9m, OLA) are inside the 2024 Medicaid line.

### 2.2 Whether any of them reach the Mexican-origin union

Yes, through the use keys. The Medicaid key charges the union 12.25% of every Medicaid dollar nationally, fraudulent or not.

- **Minnesota.**
  - HSS and EIDBI paid $428.9m in 2024, so the key puts about **$53m** of it on the union [CALCULATION: 0.1225 × $428.9m].
  - All 14 "high-risk" Minnesota services cost "$3.5 billion in 2024 alone" [SOURCE: House report p.6], so about **$0.43bn** of that sits on the union.
  - If half were fraud, as the report says the USAO "suspects" (p.6), about $0.21bn of fraud dollars would reach the union through the key [CALCULATION].
- **Medicaid nationally.**
  - No measured Medicaid fraud rate exists. GAO's 3–7% of federal obligations "should not be applied at the agency or program level" [SOURCE: GAO-24-105833 PDF p.3].
  - So the result is stated per point: each 1% of Medicaid spending that is fraud puts **$1.17bn** on the union [CALCULATION: 0.1225 × $954.2bn × 0.01].
  - At GAO's government-wide 3–7%, used only for scale, that is $3.5–8.2bn a year.

The union's share of fraud **perpetrators** is probably smaller than its 12.25% use share:
- Outside the Southern District of Florida, Hispanic defendants hold 5.6% of government-program fraud loss (§1.5).
- The union is a subset of Hispanics, and few of its members live in that district [INFERENCE].
- At a 5.6% perpetrator share, a perpetrator key would move **$0.64bn per point of Medicaid fraud** off the union [CALCULATION: (0.1225 − 0.0558) × $9.54bn]. At 3–7% that is $1.9–4.5bn a year, 1–2% of the $203–250bn main case.

This moves cost between groups and leaves total spending unchanged. Whether fraud proceeds should be charged to recipients or to perpetrators is a choice about the account's concept [FRAMING-SENSITIVE]. It also depends on sentenced cases representing perpetrators (§1.7). The direction is supported by the data; the size is not measured.

### 2.3 Fraud implied by group, $bn a year

Base: government-program fraud (health care, government benefits, procurement) sentenced FY2018–2022, GAO's window. That is 4,309 offenders with a citizenship code.

The shares are applied to GAO's direct federal fraud losses of **$233–521bn a year**, based on FY2018–2022 data [SOURCE: GAO-24-105833, `_cache/refs/gao-24-105833.pdf` PDF p.24, printed p.18] [CALCULATION, DATA: derived/implied_fraud_by_group.csv]. GAO's estimate has two exclusions:
- "fraud loss associated with revenues, such as tax credits or other fees collected by the federal government, are not included";
- it "does not capture losses that occur at the state, local, tribal, or other government level unless those losses included a federal investigative, administrative, or related action".

| Group | Offenders | Loss ($m) | Share of offenders with loss | Share of loss | Share of adults | Implied $bn/yr, loss share | Implied $bn/yr, offender share |
|---|---:|---:|---:|---:|---:|---:|---:|
| US citizens | 3,681 | 11,160 | 89.8% | 91.5% | 92.3% | 213–477 | 209–468 |
| Legal aliens | 205 | 557 | 4.9% | 4.6% | 3.8% | 11–24 | 11–25 |
| Illegal aliens | 389 | 434 | 4.7% | 3.6% | 3.8% | 8–19 | 11–24 |
| Unknown or extradited | 34 | 41 | 0.6% | 0.3% | — | 1–2 | 1–3 |
| **All noncitizens** | 628 | 1,032 | 10.2% | 8.5% | 7.7% | **20–44** | **24–53** |

Assumptions:
1. Sentenced cases represent all federal-program fraud in how it splits by citizenship. Federal prosecution selects, and the direction of that bias is unknown.
2. Guideline loss, intended or actual and double-counted across co-defendants, is proportional to real loss within each group.
3. The legal/illegal adult split is *s* = 0.5.

Prefer the loss-share column; the offender-share column overweights low-loss SSN cases.

Cases and dollars point in different directions. Noncitizens are 14.6% of those sentenced for government-program fraud, 1.9× their adult share, but hold 8.5% of the loss, 1.1× their adult share [CALCULATION from the table].

## 3. Minnesota cases

### 3.1 Case table

Sources are in `_cache/mn/`. "Lnn" is a line in the `.txt` conversion and "p" is a PDF page. Alleged, proven, restitution and recovered dollars are kept apart.

| Scheme | Charged | Convicted | Sentenced | Alleged | Proven at plea or trial | Restitution | Recovered | Program spending | Origin or citizenship stated? |
|---|---|---|---|---|---|---|---|---|---|
| **Feeding Our Future and related child nutrition** (CACFP/SFSP) | 70 as of May 2024 [SOURCE: OLA 2024 special review p.103]; 79–80 by Sept 2026 [SECONDARY] | 63 by Mar 20, 2026 [SOURCE: DOJ, `fof_2026-03-20…txt` L56]; **65** by Apr 9, 2026 [SOURCE: DOJ, `fof_2026-04-09…txt` L58] | ≥28 by Sept 8, 2026: the "24th, 25th, and 26th" on Aug 27 plus two on Sept 8 [SOURCE: IRS-CI, `fof_2026-08-27…txt` L259, `fof_2026-09-09…txt` L256]. Bock received 500 months (DOJ, May 22, 2026) | "$250 million fraud scheme"; FOF "fraudulently obtained and disbursed more than $240 million", including "more than $18 million in administrative fees" [SOURCE: DOJ Bock release L56, L61–62] | No aggregate [GAP]; the Bock trial's loss finding was not retrieved. Example group: five defendants who pleaded in March 2026 "worked together to steal and then launder $14.6 million" [SOURCE: `fof_2026-03-20…txt` L59] | No total; individual orders overlap (joint and several) | No total [GAP] | MDE paid **$845m** to nonprofit sponsors and about **$545m** to public sponsors, FY2018–22 [SOURCE: OLA 2024 p.16]. $250m is **29.6%** of nonprofit-sponsor funds and **18.0%** of all sponsor funds [CALCULATION] | Not in any fraud-case document read |
| **Housing Stabilization Services** (Medicaid) | 21 across three DOJ waves (Sept 2025, Dec 2025, May 2026) [SOURCE: DOJ/IRS-CI releases; case summaries] | 6 pleas, no trials | 0 | ≈$30.5m across 12 providers, mixing paid and claimed amounts [CALCULATION from DOJ releases] | $5.7m in DOJ's plea releases: two defendants "stole approximately $3.5 million", four "approximately $2.2 million"; each pleaded to one wire-fraud count [SOURCE: `hss_2026-02-10…txt` L67–68; `hss_2026-07-24…txt` L63–64] | None found | None found | "more than $21 million" (2021), $42m (2022), $74m (2023), $104m (2024), $61m (Jan–Jun 2025), against a forecast of $2.6m a year [SOURCE: DOJ/IRS-CI Dec 18, 2025, L266]. Total **$302m**; alleged is 10.1%, proven 1.9% [CALCULATION] | Not stated; residence only (Philadelphia "fraud tourism" cases) |
| **EIDBI** (autism therapy, Medicaid) | 4 | 2 pleas | 0 | "$46.6 million scheme … of which approximately $21.2 million was paid" (May 2026 indictment; covers the two centers in the earlier $14m and $6m cases, so those are not added) [SOURCE: DOJ case summaries L57] | Not in the releases [GAP] | "nearly $16 million" agreed in one plea [SECONDARY] | None found | $38.1m (2020) to **$324.9m** (2024) [SOURCE: OLA March 2026 review p.10]; 2021–23 missing | Not stated. "Parents in the Somali community" describes recruited families, not defendants [SOURCE: USAO Sept 24, 2025, L52] |
| **CCAP** (child care) | 1 federal CCAP case (Future Leaders) | 1 plea, July 9, 2026 [SECONDARY] | 0 | "approximately $4.6 million to which it was not entitled" in CCAP, plus about $854,000 of child nutrition already counted in FOF; $5,480,329 total [SOURCE: DOJ case summaries L75] | [GAP] | None yet | None | "Funding for the Child Care Assistance Program for 2017 was $248.2 million" [SOURCE: OLA 2019 p.17]; recent totals missing | Not stated |

Two defendants appear in two schemes: Asha Farhan Hassan (FOF $465,000, and EIDBI) and Fahima Mahamud of Future Leaders (FOF about $854,000, and CCAP) [SOURCE: `hss_eidbi_2025-12-18_six_more_irs.txt` L263; case summaries L75]. Other Minnesota programs charged in the same waves (ICS, IHS, Great Start) are outside the four schemes.

### 3.2 Headline totals checked against primary documents

- **"$9 billion."**
  - A House Oversight staff report (June 2026) says: "The DOJ estimates that $9 billion in federal dollars has been lost to fraud in these programs since 2018" [SOURCE: `house_oversight_2026-06…pdf` p.9, fn 39–40, citing the livestream of a December 18, 2025 press conference].
  - What the prosecutor said aloud, as CBS and FOX 9 report it: the 14 "high-risk" services cost $18bn since 2018, and "When I say significant amount, I'm talking on the order of half or more. But we'll see." Asked whether more than half could be fraud, he said "I'm saying that's very possible." [SECONDARY: CBS, FOX 9, Dec 18, 2025].
  - The written DOJ release that day contains neither figure.
  - The report's own p.6 gives the base: the 14 services "have cost taxpayers more than $18 billion, including $3.5 billion in 2024 alone", per CMS claims data, and "the USAO suspects that half or more of the $18 billion in total expenditures attributed to these programs were fraudulent". The $18bn is spending, and it includes the state share [SECONDARY: Minnesota Reformer]. So "$9 billion in federal dollars" relabels a suspicion about total spending as a DOJ estimate of federal loss.
  - Dollars tied to prosecutions that day were "closer to $300 million" [SECONDARY: MPR], 1.7% of $18bn [CALCULATION].
- **"$1 billion."** This came from a July 2025 TV interview. The prosecutor later said: "we will have prosecuted $1 billion worth of fraud. Not that there was $1 billion (in fraud). There's far more." Asked "Billions, with an 'S'?", he answered "Billions." [SECONDARY: KSTP, Oct 20, 2025]. The $1bn is a forecast of prosecutions. The larger figure is his belief, with no stated method.
- **"Stolen billions."** A written DOJ release says the schemes "form a web that has stolen billions of dollars" but gives no figure or method [SOURCE: USAO Sept 24, 2025, L45].
- **Minnesota auditor (OLA) on CCAP:** "We did not find evidence to substantiate the allegation that the level of CCAP fraud in Minnesota is $100 million annually … we believe the level of CCAP fraud is more than the $5 to $6 million that prosecutors have been able to prove, but we cannot offer a reliable estimate" [SOURCE: OLA 2019 p.11].
- **OLA on FOF and EIDBI:** OLA relays DOJ's $250m and gives no fraud estimate of its own [SOURCE: OLA 2024 p.103; OLA 2026].

### 3.3 Origin and citizenship

**Fraud-case documents.** No DOJ release, IRS-CI release, case summary or OLA report read states any defendant's national origin, birthplace or citizenship. They give age and city of residence.

**The one DOJ document that attaches a country to a person linked to these schemes** is a denaturalization release: "Abdikadir Ali Kadiye (Age 54/Somalia) … filed a civil denaturalization complaint", about identity fraud in 1997–98 [SOURCE: DOJ June 8, 2026, L70].
- The release does not mention Feeding Our Future.
- News reports match him to an FOF defendant [SECONDARY: MPR].
- The complaint has not been adjudicated.

**Descent claim.** DOJ's and the Attorney General's X posts of December 29, 2025 said "we have charged 98 individuals – 85 of Somali descent" [SOURCE: quoted in the House report p.6, fn 1; the posts themselves were not fetched]. These are official social-media statements. They give descent, not citizenship, and no method.

**Sentencing Commission, District of Minnesota** [DATA: derived/minnesota_district.csv, derived/minnesota_noncitizen_country.csv]:
- FY2022–FY2025 (FY2025 is the latest release): 178 people sentenced under §2B1.1, of whom **159 were US citizens (89%)**, 10 legal aliens, 8 illegal aliens and 1 of unknown status.
- FY2015–2025: 544 of 622 were citizens.
- Noncitizen countries, FY2015–2025: Liberia 17, Somalia 8, Nigeria 7, Cuba 6.
- Because naturalized citizens are code 1, this is consistent with DOJ's descent claim and cannot test it.
- Most Feeding Our Future sentencings fall in FY2026, which is not yet released.
- The public file has no names or docket numbers, and this lane made no attempt to link records to named defendants.

### 3.4 Elsewhere: status updates (trace-index format)

| Program / entity | Record and amount | Status and limit |
|---|---|---|
| Adult day care, Happy Family / Family Social, Brooklyn | "fraudulently billed Medicaid approximately $64 million. Medicaid paid approximately $56 million" (2017–2024) [SOURCE: EDNY release, Sept 9, 2026, read through Exa; direct fetch blocked] | **Owner sentenced Sept 9, 2026 to 76 months, "over $56 million in restitution", $5 million forfeited.** Sentencings of the 6th and 7th plea defendants (set for May 2026) were not checked. |
| Hospice, Azure Hospice Care | $2,266,694 false claims; $2,140,606 paid (trace index) | Sentencing set for Dec 3, 2026 [SECONDARY] |
| Child care and nutrition, Future Leaders, Minneapolis | $5,480,329 in total, of which about $4.6m CCAP and about $854,000 nutrition [SOURCE: DOJ case summaries L75] | Pleaded guilty July 9, 2026 [SECONDARY]; not sentenced |
| Child care, twelve San Diego complaints | Over $10m alleged | Charged Sept 15, 2026; no dispositions found as of Sept 24 |
| SNAP, Jesula Variety Store, Boston | About $7m in fraudulent redemptions (trace index) | Sentenced July 8, 2026 (trace index) is still the latest status. No newer primary document found; the DOJ page was blocked, so restitution was not rechecked |
| LA hospice and home-health suspensions (CMS, May 13, 2026) | About 800 providers; $1.4bn prior-year spending; $70m suspended | No newer CMS release; no updated recoveries |

### 3.5 Parent spot-check of the case file

Checked against the saved files with `rg` and `pdftotext`:
- DOJ Bock release: "$250 million", "more than $240 million", "more than $18 million" (L56, L61–62).
- DOJ releases: "63 convictions" (Mar 20) and "65" (Apr 9); "24th, 25th, and 26th" (Aug 27).
- IRS-CI: HSS payments by year (Dec 18, 2025, L266).
- DOJ case summaries: EIDBI "$46.6 million … $21.2 million was paid" (L57) and Future Leaders "$5,480,329" (L75).
- OLA 2024: "$845 million" (p.16) and "70 individuals" (p.103).
- OLA 2026: "$38.1 million" and "$324.9 million" (p.10).
- OLA 2019: CCAP "$100 million … $5 to $6 million" (p.11).
- House report: "$9 billion" (p.3, p.9) and "$18 billion" (p.6).
- Denaturalization release: "Abdikadir Ali Kadiye (Age 54/Somalia)" (L70).

All matched. So did the lines added to §3.1–3.2 when this file was written: the plea-release wording (FOF L59; HSS L67–68 and L63–64), Hassan's FOF amount (L263), the House report's p.6 text, and the CBS, FOX 9, MPR and KSTP quotes in the saved `sec_*.html` pages.

## 4. Steel-man of both readings

**That provider fraud concentrates in immigrant networks.**
- Legal noncitizens' federal offending is tilted toward fraud: 1.7× the citizen rate for fraud, 2.0× for health-care fraud and 4.1× for money laundering, against 1.1× overall.
- Noncitizen fraud clusters by country and scheme:
  - Cuban citizens are 45% of noncitizen health-care fraud offenders with a recorded country (218 of 481).
  - Fraud is 53% of Cuban noncitizens' non-immigration sentences, 63% of Nigerians' and 84% of Romanians'. For Romanians it is mostly credit-card and financial-instrument fraud (311 of 431).
- Government-program fraud loss is geographically concentrated: the Southern District of Florida holds 26%, and five districts hold half.
- Citizenship coding hides naturalized immigrants, so these data cannot rule out origin-specific concentration.
  - DOJ says 85 of the 98 people charged in Minnesota are "of Somali descent".
  - In FY2025 the District of Minnesota sentenced 65 people for §2B1.1 fraud, up from 34 in FY2024, and 58 of them were US citizens. Across FY2015–25 it sentenced 8 noncitizens with Somali citizenship for fraud.
  - Any Somali-descent defendants sentenced so far were therefore mostly coded as citizens [INFERENCE; records not linked; FY2026 not released].
- In Minnesota:
  - DOJ's alleged $250m equals 18–30% of the child-nutrition program's payments to sponsors.
  - Housing Stabilization paid $104m in 2024 against a forecast of about $2.6m a year, 40 times the forecast [SOURCE: `hss_eidbi_2025-12-18_six_more_irs.txt` L266; CALCULATION].

**That the pattern is ordinary federal selection.**
- The noncitizen fraud ratios (1.7–2.0) bracket their ratio for all non-immigration federal crime (1.84).
- Unauthorized immigrants are under-represented in fraud with real loss compared with their other federal offending.
- Their excess "benefits fraud" is mostly false-SSN prosecutions with a median loss of $0.
- In dollars, noncitizens hold 8.5% of government-program fraud loss against 7.7% of adults; citizens hold 91.5%.
- Outside the Southern District of Florida, Hispanic defendants hold 5.6% of that loss, against 16.7% of adults nationally.
- Federal venue selects noncitizens, because immigration enforcement surfaces their document and SSN cases. State Medicaid fraud units prosecute much provider fraud outside these data [INFERENCE].

Whether fraud is "endemic in democratic institutions" is a claim these data cannot test [FRAMING-SENSITIVE].

## 5. Gaps

- **FY2026 Commission data** (most FOF sentencings) is not released. State prosecutions, including Medicaid Fraud Control Unit cases and state CCAP cases, are not in the Commission data.
- **No birthplace or ancestry in the Commission data.** Fraud by national origin, or by the Mexican-origin union, cannot be measured. The Hispanic and Mexican-citizen shares are proxies.
- **Loss detail.** Actual and intended loss cannot be separated in the public file. 19% of §2B1.1 cases have no loss amount. Scheme-level (deduplicated) loss is not available.
- **Minnesota:**
  - No aggregate restitution or recovery for any scheme.
  - Plea status of 15 of 21 HSS defendants is unknown.
  - EIDBI costs for 2021–23 and CCAP totals after 2017 were not retrieved.
  - The Bock loss finding and the plea agreements (Hassan, Mahamud) were not retrieved.
  - The HHS-OIG CCAP audit is unreachable from this machine (DNS).
- **Headline sources not retrieved:** the December 18, 2025 livestream and the X posts behind "85 of Somali descent" (x.com is blocked here) were not viewed.
- **BEA placement:** where CACFP/SFSP and CCDF sit in BEA is inferred from footnotes; the program crosswalk was not checked.
- **Unauthorized denominator:** it is a modelled share. There is no annual unauthorized series in the register.

## 6. Reproduce

```sh
# from the repository root; inputs in _cache/ (ignored). --fetch downloads missing ones:
# USSC zips by curl, ACS B05003/B05003I by Census API (needs CENSUS_API_KEY; never printed)
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
  infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/ussc_fraud.py [--fetch]
```

Runtime is about 15 seconds. The script streams each 1–2 GB CSV out of its zip with pyarrow column projection, so nothing is unzipped to disk. It stops with `[BLOCKED]` if an input is missing, if the Sourcebook check fails, or if an economic-crime record is duplicated, fails to join or falls outside §2B1.1.

## 7. Files

`derived/` (tracked):
- `fraud_by_citizenship_year.csv`: offenders, loss (sum, median, mean, count at $100m+) and restitution by status and year.
- `fraud_subtypes_by_citizenship.csv`: the same by economic-crime type.
- `rates_per_100k.csv`: rates with bands for every offense definition.
- `ratio_by_offense.csv`: noncitizen-to-citizen ratios.
- `fraud_by_hispanic_citizenship.csv`: rates by Hispanic origin and citizenship.
- `fraud_by_country_pooled.csv`: noncitizen offenders by country.
- `gov_victim_fraud_by_district.csv`: government-program fraud by district.
- `gov_victim_fraud_by_origin.csv`: Hispanic and Mexican-citizen shares.
- `implied_fraud_by_group.csv`: the §2.3 table.
- `minnesota_district.csv`, `minnesota_noncitizen_country.csv`: the District of Minnesota, FY2015–2025.
- `top_statutes.csv`: most frequent statutes by status.
- `denominators.csv`, `unauth_share_check.csv`: population denominators and the unauthorized-share check.
- `validation.json`: Sourcebook checks and join coverage.
- `manifest.json`: sha256 of the script and every input.

`_cache/` (ignored):
- `ussc/`: 11 individual zips (FY2015–25), 11 economic-crime zips, codebooks, Sourcebook Table 9 (FY2019, FY2022).
- `acs/`: 18 Census API table pulls (B05003 and B05003I for nine years) and 2 variable lists.
- `refs/`: GAO-24-105833, 2023 Guidelines Manual, and three pages of NIPA Handbook chapter 9 (no program crosswalk found there).
- `mn/`: 17 primary documents, 10 secondary pages, `MN_CASES.md`, `exa_captures_2026-09-24.md`, `urls.tsv`.

## 8. Validation run

The brief requires a rerun with byte-identical outputs. `ussc_fraud.py` (sha256 `5accf08d41568fc3b0644ab71e7904641c2a64d3db4aad7afc9a093b8076e375`) was run twice from an empty `derived/`, and all 16 files matched. A third run, made after this file's numbers were checked against `derived/`, matched again. The hashes:

```
8cb317081d2ab6b7908dbb0b40bb9ced45c8b2a64404988fc2998f3e920907d3  denominators.csv
6deecebde428c8b432e7c6f99a63a1ff430e6fba32129a028a0b50c17d3f517e  fraud_by_citizenship_year.csv
c565079e49680ac362786586e54bd044366586496e1228bb5f59b40940f0cf82  fraud_by_country_pooled.csv
12a760eaf140cc925dc5f665fc0e598036ecf6f0c53584ed374bf1ffe5e61826  fraud_by_hispanic_citizenship.csv
b354f858b1fb02d48589812bc5dcf08caac4dbf5fef3005eb46ec1421cd813ac  fraud_subtypes_by_citizenship.csv
e307d7dc0a7a04a9498b1d13a2260d737c648e654ae0b381d2a42f6adff5203c  gov_victim_fraud_by_district.csv
cdecbe28c0eff0e5ff64b26bbb206e7223320ea912361e763dcbe89330d66f79  gov_victim_fraud_by_origin.csv
13c424b3a922cdaf1d77c3f04852c1c192bf002f11ae46f8d27d5a7fbdebfeb2  implied_fraud_by_group.csv
09f502c8552d3fa740494e47bbd0330eea55dfcb2be84e9290c0c21439cf3921  manifest.json
65b6b9d039a0318d60b8b55cab478785f2bbfc6590c95ab6fa3bf40044c1cda0  minnesota_district.csv
d106fcdb3281fe39a70c8e92b7f327c293afa3be83c853fd5212b8ed11410b14  minnesota_noncitizen_country.csv
f05d65a01633841f1d4b9703181ac92f1c19328c2f3d8ce8ae4ed7e4612b4b6e  rates_per_100k.csv
757e5d6b909bd3652d42a94186d9f3c651f8f6a0957322d425012a9aa9690dc8  ratio_by_offense.csv
b68cef7fbdad46d0702e8a606be41ea2dad338b431530f3cbdfacd5b9ecf3ded  top_statutes.csv
6cc8aa5881d195aba7b01608865d8eff838d449f6b11f5fad537c01c188d3221  unauth_share_check.csv
1a96981c3923f5878a1ea8eac840494e24f0c2c08413509934d15f9160b55e16  validation.json
```

Model self-report: claude-opus-5-5[1m].
