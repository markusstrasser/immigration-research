**Verdict:** The National Taxpayer Advocate's TY2022 gap of **$3.69bn** between income tax before and after credits, on 3,791,421 returns carrying any ITIN, is **nonrefundable credits only**. It is Form 1040 line 18 minus line 22, and it fell to $1.71bn in TY2021, the one year the child tax credit was fully refundable. No IRS, TIGTA or NTA document read publishes the **refundable** credits on ITIN returns for any year after the 2017 tax law (TCJA). The largest refundable credit is the Additional Child Tax Credit (ACTC) for the Social Security number (SSN) holding, mostly US-citizen, children of ITIN filers. It is **of order $2–3bn a year** [INFERENCE], from about 2 million such children [SECONDARY, a JCT count quoted by the Tax Policy Center] times the TY2022 refundable amount per child. From TY2025 the 2025 reconciliation act (OBBBA) requires an SSN for the taxpayer or, on a joint return, at least one spouse, which ends the credit for ITIN-only households [SECONDARY]. About **0.6–0.85** of the credit dollars on ITIN returns plausibly reach households with an unauthorized adult [INFERENCE]; the rest go to nonresident filers, lawfully present people without work authorization, and SSN filers claiming ITIN spouses or dependents. Recurring state money found is an order of magnitude smaller. Colorado publishes its ITIN EITC: **$3.8m in TY2022** [SOURCE]. Washington's Working Families Tax Credit reaches ITIN households with about **$9–13m** a year and Maryland's EITC with about **$50m** [both INFERENCE from published counts]. California, the largest ITIN state (866,378 ITIN returns), does not publish an ITIN split of CalEITC or its Young Child Tax Credit. Its one-time 2021 Golden State Stimulus paid ITIN filers **$959.8m** [SOURCE]. State grants to undocumented students total about **$83m a year** where a figure exists or can be derived: California about $64m, Washington about $15m and Minnesota $4.9m. Texas's $12.3m (FY2017) ended in 2025, and Illinois and New York publish no counts. No source gives a Mexican share for any of these dollars. Evidence level: A for every count quoted from a primary table; C for every dollar figure marked [INFERENCE].

Model: claude-opus-5-5[1m] (Opus 5.5, 1M context), `itin_credits_student_aid` lane, 2026-09-23. Brief: `BRIEF.md`. Arithmetic: `calc.py`, output in `derived/calc_output.txt`. Cached primaries: `_cache/` (ignored).

Lawful credits are not fraud. TIGTA's March 2026 audit of credits allowed to potentially ineligible ITIN holders (1,769 returns, $3.93m) belongs to `../improper_payments_unauthorized_2026_09_23/` [SOURCE: TIGTA 2026-400-016, Oversight.gov summary page].

## 1. Federal credits on returns with an ITIN

### What the NTA's $3.7bn is

The NTA table covers Form 1040-series returns with an ITIN as primary, spouse or one of four dependents, from the IRS Individual Returns Transaction File [SOURCE: NTA 2024 Annual Report, research report 3, methodology, p.228].

| Tax year | Income tax before credits | After credits | Credits | Total tax paid | Net refund (−) / balance due |
|---|---|---|---|---|---|
| 2017 | $15.88bn | $13.40bn | $2.49bn | $15.28bn | −$6.20bn |
| 2018 | $16.34bn | $12.38bn | $3.96bn | $14.43bn | −$4.80bn |
| 2019 | $15.97bn | $12.14bn | $3.83bn | $14.14bn | −$4.59bn |
| 2020 | $15.89bn | $12.53bn | $3.36bn | $14.83bn | −$5.02bn |
| 2021 | $19.02bn | $17.31bn | $1.71bn | $20.15bn | −$5.54bn |
| 2022 | $18.21bn | $14.51bn | $3.69bn | $17.31bn | −$3.31bn |
| 2023 | $16.47bn | $13.16bn | $3.31bn | $15.70bn | −$3.03bn |

[SOURCE: NTA 2024 ARC, research report 3, Fig. 5.3.3, p.230; exact dollars in `calc.py`. The TY2023 row was incomplete when drawn, Sept. 26, 2024 (Fig. 5.3.2 note, p.229).]

- **The $3.69bn is nonrefundable.** On the TY2022 Form 1040, line 21 (the child tax credit and credit for other dependents, plus Schedule 3 nonrefundable credits) is subtracted from line 18 to give line 22. Refundable credits (lines 27–31: EITC, ACTC, the refundable American Opportunity Tax Credit (AOTC), recovery rebates) are payments and sit below line 24 [INFERENCE from the Form 1040 line structure; the NTA does not define its columns]. `calc.py` confirms that "Credits" equals before minus after in every year.
- **The series itself supports this reading.** Credits jumped in TY2018, when TCJA doubled the child tax credit and added the $500 credit for other dependents. They fell to $1.71bn in TY2021, when the American Rescue Plan Act moved the whole child credit to the refundable line, and returned to $3.69bn in TY2022. A column that included refundable credits would have risen in 2021. The refundable credits are therefore inside the net-refund column, mixed with over-withholding, and cannot be separated from this table.
- "Total tax paid" exceeds tax after credits by $2.80bn in TY2022. The excess is presumably line 23 other taxes, mainly self-employment tax [INFERENCE]. Returns with a Schedule C profit report about 10% of ITIN-return income [SOURCE: p.230].
- **The split the brief asks for is:** $3.69bn nonrefundable, and $0 of it refundable. The refundable credits come on top of it.

### Refundable credits reaching ITIN filers

| Credit | ITIN rule | Published figure | Estimate here |
|---|---|---|---|
| EITC | Barred since 1996 for filers without an SSN valid for work (taxpayer, spouse and child) | none (not payable) | $0 lawful. Illegal claims belong to the improper-payments lane [SOURCE: TIGTA 2011-41-061, background; page not verified, read from a search extract] |
| ACTC, pre-2018 | Filer and child could use ITINs | TY2000 $62m → TY2007 almost $1.8bn, 62,000 → 1.2M returns [SOURCE: TIGTA 2009-40-057, search extract, page not verified]; $4.2bn processed in 2010 [SOURCE: TIGTA 2011-41-061, title and summary], about $1bn of it multi-year claims [SOURCE: CRS IN11830, 2021] | — |
| ACTC, TY2018–2024 | Child needs a work-authorized SSN; filer may use an ITIN [SOURCE: CRS IN11830; CRS R48312] | **none found** (NTA ARC24 report read in full; TIGTA 2022-40-013 text searched) | **$2.0–3.0bn a year** [INFERENCE]: ~2M SSN children on returns without a taxpayer SSN [SECONDARY: TPC, citing JCT, on the House OBBBA text] × $1,000–1,500 refundable per child (TY2022 cap $1,500). At the median ITIN AGI of $31,033 with two children, 71% (head of household) to 85% (joint) of the child credit is refundable [CALCULATION: `calc.py`] |
| Credit for other dependents ($500) | ITIN dependents allowed | math errors erased over $6m in TY2022 [SOURCE: p.239] | nonrefundable, so it is inside the $3.69bn |
| AOTC, refundable part | ITIN student allowed if issued by the due date | none found | [GAP] |
| 2020–21 recovery rebates | CARES Act excluded joint returns with an ITIN spouse (military excepted); the Dec. 2020 act and ARPA paid SSN members of mixed-status households, including SSN children of ITIN parents [TRAINING-DATA, not verified here] | none found | [GAP]. The TY2020–21 net refunds (−$5.02bn, −$5.54bn) include rebates claimed on the return [INFERENCE] |
| 2021 expanded child credit | Child needs an SSN; filer may use an ITIN | none by ITIN; all advance payments $93.5bn in 216.9M payments [SOURCE: TIGTA 2023-47-035, search extract] | [GAP]. TY2021 is the year the NTA "credits" fell by $1.65bn, the refundable shift above |

Other JCT anchors [SOURCE: JCT JCX-35-17, footnotes 17–18, read from a search extract]:

- In 2015, 87% of ITIN filers claiming children claimed the refundable child tax credit.
- ITIN-only returns reported about $60bn in wages for TY2010.

The TCJA child-SSN rule was scored at $29.9bn of savings for FY2018–27 [SOURCE: CRS R48312, citing JCX-67-17]. That is the credit denied to children without SSNs, not credit paid.

**Check on the estimate.** Single-year ACTC to ITIN filers was about $3.2bn in 2010. That year's cap was $1,000 per child, and ITIN children still counted [CALCULATION: $4.2bn − $1bn multi-year]. After TCJA the refundable cap rose to $1,400–1,500 but ITIN children dropped out. $2–3bn is consistent with that history.

**Would change it:**
- a JCT or IRS tabulation of ACTC by filer TIN type;
- evidence that the 2M-children count is not concentrated on low-income returns, which would push the refundable share down.

**OBBBA (TY2025 onward).** The House Ways and Means text required the SSN of the taxpayer and, if married, the spouse [SOURCE: W&M committee print, §110004(c), May 12, 2025 draft]. The enacted §70104 requires the taxpayer's SSN, or at least one spouse's on a joint return [SECONDARY: bill summaries; enacted text not read]. The ACTC above therefore stops for single ITIN filers and ITIN–ITIN couples, and survives for mixed SSN–ITIN couples.

### Share reaching unauthorized filers

Composition facts [SOURCE: NTA ARC24 research report 3]:

- The 3.79M returns include returns where only a spouse or dependent holds the ITIN. In TY2023, over 2.4M returns had an ITIN primary, of about 3.3M filed by September 2024 (pp.229–230).
- Returns filed from the top 15 foreign countries total 135,705, or 3.6%; Canada alone is 56,700 [CALCULATION from Fig. 5.3.8, p.233].
- Of ITINs assigned in 2020–2023, an average 58% went to resident aliens (substantial-presence test) and 23% to dependents or spouses of US citizens or resident aliens (p.235).
- Filing status in TY2022 was 41% joint, 35% single, 19% head of household and 5% married filing separately (p.230).

**Inference [evidence C].** About 0.6–0.85 of the credit dollars on ITIN returns reach a household with an unauthorized adult. The share is at the high end for the ACTC, which requires US residence and an SSN child, so nonresident, treaty and student filers rarely claim it. It is lower for the $500 other-dependent credit, which SSN filers claim for ITIN relatives, including dependents living in Mexico or Canada. Lawfully present residents without work authorization also file with ITINs: visa holders' dependents, and asylum applicants before work authorization. The range is a judgment; no document measures status on ITIN returns.

## 2. State credits open to ITIN filers

| State | Credit (ITIN since) | ITIN split published? | ITIN count, latest | ITIN dollars | Program context | Source |
|---|---|---|---|---|---|---|
| California | CalEITC, Young Child Tax Credit, Foster Youth credit (TY2020) | **No** | — | not published | TY2024 CalEITC $933m on 3,202,365 returns; YCTC $418m on 390,479 [SOURCE: FTB report 2024, Table 1, p.8, via `../california_program_costs_2026_09_23/RESULT.md`] | FTB TY2023–24 reports have no ITIN breakout |
| California | Golden State Stimulus I and II (2021, one-time) | Yes | 651,069 (GSS I) + 408,562 (GSS II) payments | **$552.0m + $407.8m = $959.8m** (7% of GSS II dollars) | all GSS: $2.84bn + $6.03bn | [SOURCE: FTB GSS II report 2022, Table 2 p.4, Table 3 p.5] |
| Washington | Working Families Tax Credit, a sales-tax refund modelled on the EITC (TY2022) | Share of applications only | households with any ITIN member: 10% of 185,480 applications (Aug. 2023), 9% of 189,777 (Dec. 2023), 6% of 320,107 (CY2025), 4.4% of 325,200 (CY2026) | not published; **≈$9–13m a year** if the dollar share equals the application share [INFERENCE: `calc.py`] | refunds $133.4m (TY2022), $142.8m (TY2023), $205.6m (TY2024) | [SOURCE: DOR 2025 report to the Legislature, Table 2 p.4, Table 4 p.5; WFTC program-performance pages CY2025–26; DOR advisory-committee slides Aug. and Dec. 2023] |
| Maryland | EITC (TY2020, permanent since 2023) | Counts, through a Comptroller data partner | ITIN tax units claiming: 48,750 (TY2021), 51,442 (TY2022), **47,060 (TY2023)** [CALCULATION: eligible minus non-claimers] | not published; ≈$52m at the $1,100 average refund [INFERENCE] | 444,000+ state EITC claims TY2024 | [SOURCE: Urban Institute, Dec. 2025, Table 5, Comptroller data; Comptroller "Earned It" 2025 report] |
| Colorado | EITC via form DR 0104TN (TY2020); child tax credit and Family Affordability Tax Credit also admit ITIN households (not split) | **Yes, for the EITC** | 60,310 ITIN returns in DOR materials, 2023 [SECONDARY: Appalachian State FEPL memo, July 2026] | **$873,385 (TY2020), $3,822,758 (TY2022)**, the "expanded Colorado EITC" for filers, spouses or dependents without a work-valid SSN; the credit rose from 20% to 50% of the federal amount in TY2023, so ≈$9–10m if claims held [INFERENCE] | — | [SOURCE: DOR 2024 Tax Profile & Expenditure Report, p.89] |
| Oregon | EITC (2021 law) | No actual found | pre-enactment DOR estimate 20,000–25,000 ITIN claimants | $10m per biennium, an estimate | — | [SOURCE: Oregon EITC workgroup report, Jan. 2021, citing DOR] |
| IL, MN, NM, ME, VT, DC | EITC open to ITIN filers | not searched | — | — | ITIN returns TY2022: IL 170,218 | ITEP list [SECONDARY]; [GAP] |
| NJ, NY, MA | Brief candidates; ITEP's 2024 EITC list does not include them (CTCs not checked) | not searched | — | — | ITIN returns TY2022: NY 254,779; NJ 172,349; MA 65,244 | [GAP] |

NTA ITIN-return counts by state, TY2022 [SOURCE: Fig. 5.3.6, p.232]:

- CA 866,378 (22.9%); TX 446,522 (11.8%).
- NY 254,779; FL 185,119; NJ 172,349; IL 170,218; GA 142,125; MD 131,511.
- NC 111,982; VA 109,434; WA 88,816; CO 72,928; MA 65,244; AZ 54,824; NV 50,185.

The top 15 states hold 77.1% of ITIN returns [CALCULATION].

## 3. State student aid and tuition for undocumented students

| State | Program (application) | Year | Recipients | Dollars | Source |
|---|---|---|---|---|---|
| California | Cal Grant via the California Dream Act Application (CADAA) | 2025-26 | **16,844 offered** (2024-25: 15,606; 2023-24: 16,769; 2022-23: 17,680; 2020-21: 21,353) | paid amounts not published by application type; **≈$56–60m** [INFERENCE: 2024-25 all-filer paid rate 65.1% × $5,503 per paid recipient] | [SOURCE: CSAC Cal Grant offered-awardees reports, Table 1, p.9 (2024-25, 2025-26, cached in `../california_program_costs_2026_09_23/_cache/`); CSAC 2024-25 district report, totals: 696,333 offered, 453,482 paid, $2,495,572,964] |
| California | Dream Act Service Incentive Grant | budget years 2023-24 to 2025-26 | 750 / 765 / 796 | $7.5m a year | [SOURCE: Governor's Budget 2025-26, 6980 CSAC, program table] |
| California | Middle Class Scholarship, community-college fee waivers (CCPG), UC and CSU grants to AB 540 students | — | not published by status | — | [GAP]. CSAC says 14% of estimated undocumented college students got state aid in 2021-22 [SOURCE: CSAC undocumented-student affordability report page] |
| Texas | TEXAS Grant, TEOG, TPEG and others to "affidavit students" (TASFA) | FY2017 | 11,285 state/local awards; 25,930 affidavit students (1.5% of public enrollment) | **$12.32m** GR in state grant aid; $1.43m College Access Loans | [SOURCE: THECB "Overview: Eligibility for In-State Tuition and State Financial Programs", pp.3–5] |
| Texas | same | after June 2025 | ended: a federal court struck down the in-state provision; THECB's revised affidavit requires lawful presence (July 18, 2025) | — | [SECONDARY: Daily Texan, July 31, 2025] |
| Washington | Washington College Grant via WASFA | 2023-24 | 3,067 WASFA recipients of 97,269 WA Grant recipients; 8,410 WASFA applications | ≈$14.8m [INFERENCE: × $4,814 average]; WA Grant total $468.2m | [SECONDARY: Lynnwood Times, Aug. 2026, citing WSAC; SOURCE: WSAC 2023-24 state need-based report, p.2]. WASFA also serves filers with no immigration reason (privacy, loan default) |
| Minnesota | State Grant via MN Dream Act | FY2025 | **617** | **$4,930,829** (average $7,992) | [SOURCE: OHE State Grant end-of-year statistics FY2025, Table 5, p.18] |
| Minnesota | same | FY2024; FY2023 | 469; 411 | $3,667,970; ≈$2.76m (average $6,715) | [SOURCE: OHE FY2024, Table 6; OHE 2022-23 Dream Act applicant summary] |
| New Jersey | TAG and others via the NJ Alternative Financial Aid Application | 2018-19 | 749 | >$3.8m, of which >$3.5m TAG | [SECONDARY: NorthJersey.com, Aug. 2019, citing HESAA]; later years [GAP] |
| Illinois | MAP via the Alternative Application (RISE Act) | — | not published | — | [GAP]. Enjoined for 2026-27 as applied to people not lawfully present [SOURCE: US v. Illinois, S.D. Ill. 3:25-cv-01691, July 24, 2026; ISAC MAP page] |
| New York | TAP and Excelsior via the NYS DREAM Act | — | not published (HESC annual reports 2022-23 to 2024-25 describe it without numbers) | — | [GAP] |
| Colorado, Oregon, New Mexico and others | — | — | not searched | — | [GAP] |

**In-state tuition.** Only Texas has a state figure: general revenue attributed to affidavit students through formula funding was **$25.94m in FY2017** [SOURCE: THECB overview, p.3]. That is instruction funding attributed to these students, not a price discount. The same students paid $72.8m in tuition and fees, about $2,808 each [SOURCE: p.5; CALCULATION]. No other state or fiscal office estimate was found [GAP]. None is invented here.

**Total.** Recurring grants with a figure come to about $83m a year: California ≈$64m, Washington ≈$15m and Minnesota $4.9m [CALCULATION with the INFERENCE rows]. This excludes Texas (ended), New Jersey (only 2018-19), Illinois and New York (unpublished), and California's institutional aid.

## 4. Mexican share

- **ITIN credits: no data.** The NTA publishes ITIN returns by state and by country of filing from abroad, not by country of birth or citizenship. Mexico appears only as 2,512 returns filed from Mexico (Fig. 5.3.8, p.233). No IRS, TIGTA or state document read gives a Mexican share.
- **Anchors.** Mexico-born people were about 4.3M of 14.0M unauthorized in 2023, or 31% [SOURCE: Pew 2025, p.11, as recorded in `../onbooks_share_2026_09_23/RESULT.md` row 10]. California and Texas hold 34.7% of ITIN returns [CALCULATION].
- **The ACTC population** (long-resident parents of US-born children) is plausibly more Mexican than the unauthorized stock. **0.35–0.5 of the ACTC dollars** is an assumption, not a measurement [INFERENCE, evidence D].
- **Students.** No state aid agency publishes recipients by country of origin [GAP].

## Sources

| Source | Used for | Grade |
|---|---|---|
| NTA 2024 ARC research report 3 (`_cache/ARC24_RR_Research_3_wb.pdf`, Wayback copy; text also read via Exa) | ITIN return counts, taxes, credits, states, W-7 reasons | A (IRS administrative data) |
| FTB Golden State Stimulus II report 2022 (`_cache/ftb_gss2_report_2022.pdf`) | ITIN stimulus dollars | A |
| WA DOR WFTC 2025 report (`_cache/WFTC_2025-LegReport.pdf`); WFTC performance pages | WFTC totals, ITIN application share | A (counts); C (dollar inference) |
| Urban Institute Dec. 2025 (Comptroller of Maryland data) | MD ITIN EITC claimants | B (partner analysis of admin data) |
| THECB affidavit overview (`_cache/thecb_affidavit_overview.pdf`) | TX aid and formula funding | A, dated FY2017 |
| Colorado DOR 2024 Tax Profile & Expenditure Report (`_cache/co_tper_2024.pdf`, Wayback copy) | CO expanded (ITIN) EITC dollars | A |
| MN OHE FY2025 end-of-year statistics (`_cache/mn_state_grant_eoy_fy2025.pdf`) | MN Dream Act grants | A |
| WSAC 2023-24 state need-based report (`_cache/wsac_2024_stateneedbased_by_inst.pdf`) | WA Grant totals | A |
| CSAC offered-awardee and district reports; ebudget 6980 | CA offers, paid totals, service grant | A (offers); C (paid inference) |
| TIGTA 2009-40-057, 2011-41-061, 2023-47-035; JCX-35-17; CRS IN11830, R48312 | pre-TCJA ACTC, JCT anchors | A, but read from search extracts (pages not verified) |
| Tax Policy Center; Lynnwood Times; NorthJersey.com; Daily Texan; FEPL memo | 2M-children count, WASFA recipients, NJ 2018-19, TX end, CO ITIN returns | [SECONDARY] |

## Gaps and next queries

- **IRS SOI.** No SOI table splitting returns by ITIN turned up in this pass. The NTA's IRTF tabulation is the only IRS-data source used.
- **ACTC on ITIN returns after TCJA.** Find the JCT primary for the OBBBA SSN rule (a JCX score or JCT letter with the 2M-children count and dollars). Also try TIGTA 2026-400-016 in full: curl returns HTML and Wayback has no copy; `agent-browser` on tigta.gov is untried.
- **California.** Get the ITIN split of CalEITC/YCTC: FTB special request or PRA. Get Cal Grant paid to CADAA students: CSAC paid-recipient data by application type.
- **Illinois and New York.** ISAC Alternative Application MAP counts (ISAC data book, Commission materials) and HESC DREAM Act award counts; neither appeared in searches.
- **Other states.** IL, MN, NM, ME, VT and DC EITC ITIN splits; CO and OR state aid (CASFA, ORSAA); NJ after 2018-19.
- **Mexican share.** Needs IRS W-7 applicants by country of citizenship (TIGTA ITIN audits sometimes print it) or a state-weighted proxy from the lane's ACS status imputation.

## Disconfirmation

- The nonrefundable reading of the $3.69bn would fail if the NTA's "credits" included refundable credits. It does not: that column would have risen in TY2021 instead of falling to $1.71bn.
- The $2–3bn ACTC figure is the weakest number here. It rests on a secondary report of a JCT count made for a 2025 bill, applied to TY2022 law. Pre-TCJA ITIN ACTC history ($1.8bn TY2007, about $3.2bn single-year in 2010) keeps it in range. It is not a measurement.

## Parent check (2026-09-23)

`calc.py` rerun: stdout is byte-identical to `derived/calc_output.txt` (md5 33e0d51a…). Figures
checked against the cached primaries:
- NTA Fig. 5.3.3: 3,791,421 returns; $18,205,798,218 before credits, $14,511,054,710 after,
  $3,694,743,508 credits, −$3,313,974,360 net;
- Colorado TPER: expanded EITC $873,385 (TY2020) and $3,822,758 (TY2022);
- Minnesota OHE: 617 Dream Act State Grant recipients, $4,930,829;
- FTB: ITIN recipients 651,069 / $552,013,200 (GSS I) and 408,562 / $407,774,500 (GSS II);
- THECB: 25,930 affidavit students, 11,285 awards, $12.32M grant aid, $25.94M formula funding (FY2017).

The ACTC figure ($2–3bn) and every dollar marked [INFERENCE] remain unverified by construction.
