claude-opus-5-5

**Verdict:** In FY2028, the first fiscal year with every piece in full effect, current law roughly breaks even for main case v5's 42.75M lineage (2024 dollars, consolidated government). The net taken from the lineage is **−$0.3bn a year**, so the lineage comes out $0.3bn ahead. The ends run from −$4.2bn to +$5.8bn. The benefit cuts come to $9.6bn ($5.8–15.5bn). The 2025 budget law's individual tax cuts for the same people come to $9.9bn ($9.8–10.0bn), net of its remittance excise; that is the tax side, below. Six of the tax items lapse by tax year 2030: tips, overtime, car-loan interest, the senior deduction, the Trump-account deposit and the higher SALT cap. Once they do, the net is **$5.75bn** a year taken from the lineage, and the cuts outlast the tax relief. Counting the federal books alone adds the $0.9bn that the emergency-Medicaid match shifts to states. The figures sit beside the 2024 account, which is income-year 2024 under 2024 law. They are no headline change. [CALCULATION: `derived/rows.csv`, `derived/summary.json`, `derived/tax_rows.csv`, `derived/tax_summary.json`]

| Part (FY2028, 2024 $bn) | Lineage | Range | Lineage share |
|---|---|---|---|
| (c) 2026 public-charge rule, from `public_charge_share_2026_10_07` | 5.00 | 1.61–8.40 | 42.6% of DHS's dollars |
| (b) Enhanced premium tax credit expired after 2025 | 2.46 | 2.46–3.10 | 8.9% of enhancement dollars |
| (a) Child tax credit, taxpayer SSN rule §70104(b) | 1.19 | 0.77–1.65 | 33.9% of the national CPS amount |
| (a) PTC only for LPR / Cuban-Haitian / COFA §71301 | 0.47 | 0.47–1.22 | 6.1% (15.9% broad) |
| (a) No PTC below 100% FPL for the status-barred §71302 | 0.27 | 0.27–0.77 | 5.8% (16.4% broad) |
| (a) Medicaid/CHIP §71109, SNAP §10108, Medicare §71201 | 0.14 | 0.14–0.31 | 10–15% (29–32% broad) |
| Enhancement on (a)'s PTC classes (the bridge between (a) and (b)) | +0.07 | | |
| Public charge × (a), counted once | −0.01 | −0.02 to −0.00 | |
| **Consolidated government** | **9.59** | **5.77–15.52** | |
| Emergency-Medicaid match §71110, federal to states | 0.89 | 0.78–0.89 | 31.5% |
| **Federal books** | **10.47** | **6.55–16.41** | |

FY2027 gives $9.58bn consolidated and $10.30bn on the federal books. §71301 has only nine months in FY2027, which the expired-credit row offsets.

P.L. 119-21's own rows come to **$2.1bn** consolidated ($1.6–3.9bn) and $2.9bn federal. That replaces the reading worker's −$3–6bn. The child credit is most of it. The noncitizen eligibility limits are small for this lineage: Mexico has no TPS designation, almost no refugee admissions and no CHNV parole [TRAINING-DATA], and the lineage's noncitizens are mostly LPRs, whom the law keeps eligible, or unauthorized, who were never eligible. The 3.04M added descendants are US-born citizens. No eligibility rule touches them, and the script checks that none of the records carrying their weight is a noncitizen [CALCULATION: gate `added_descendants_are_citizens`].

The arm leaves out larger post-2024 changes. P.L. 119-21's programme-wide provisions hit the lineage as citizens. On the lineage's person shares they scale to about **$5.8bn** in FY2028:
- Medicaid work requirements §71119: $2.6bn.
- SNAP work requirements §10102: $1.2bn.
- The SNAP state match §10105, a shift to states: $0.9bn.
- PTC verification, special enrollment and recapture §§71303–71305: $1.0bn.

These scales are [INFERENCE], not measured [CALCULATION: `derived/context_not_in_arm.csv`; SOURCE: CBO 61570]. The law's tax cuts point the other way; they are priced in the next section.

## Tax side and the net line (added 2026-10-07 for symmetry)

`tax_side.py` prices the law's individual tax changes against 2024 law for the same lineage, by the evidence-symmetry rules (`decisions/2026-09-23-evidence-symmetry-rules.md`). The 2024 account already uses TCJA-era law, so the extension of TCJA is no change and is left out. Positive figures are tax cuts or new transfers to the lineage. [CALCULATION: `derived/tax_rows.csv`]

| Provision (verified in the enacted text) | National, nominal $bn | Level source | Lineage share | Lineage, 2024 $bn | Lapses by TY2030 |
|---|---|---|---|---|---|
| §70104 child credit: $2,200 indexed vs 2024 law's $2,000 | 16.26 | Tax-Calculator own data, TY2027 | 14.0% | 2.11 | no |
| §70202 overtime deduction (FLSA premium; cap $12,500 / $25,000) | 22.98 | JCT FY2028 | 9.1% | 1.89 | yes (after TY2028) |
| §70102 standard-deduction increase beyond TCJA indexing | 16.51 | Tax-Calculator own data, TY2027 | 9.9% | 1.50 | no |
| §70203 car-loan interest deduction (cap $10,000) | 9.92 | JCT FY2028 | 11.2% | 1.01 | yes |
| §70120 SALT cap $40,000 + 1% a year, phased down over $500k | 26.35 | Tax-Calculator own data, TY2027 | 3.8% | 0.92 | yes (2030: $10,000) |
| §70201 tips deduction (cap $25,000) | 8.08 | JCT FY2028 | 11.3% | 0.83 | yes |
| §70424 charitable deduction for non-itemizers ($1,000 / $2,000) | 8.15 | JCT FY2028 | 10.3% | 0.76 | no |
| §70103 senior deduction ($6,000 per person 65+) | 20.93 | Tax-Calculator own data, TY2027 | 3.9% | 0.76 | yes |
| §70204 Trump-account $1,000 for citizen children born 2025–28 (a transfer) | 3.69 | CBO/JCT FY2028 outlays | 19.0% | 0.63 | yes |
| §70604 1% excise on cash-funded remittances (a tax increase) | 1.09 | JCT FY2028 | 54% (40–65%) | −0.53 (−0.64 to −0.39) | no |
| **Tax side** | | | | **9.87** (9.76–10.00) | |
| Permanent items only | | | | 3.83 | |

| Net, FY2028, 2024 $bn (consolidated) | Central | Ends |
|---|---|---|
| Benefit cuts (the arm above) | 9.59 | 5.77–15.52 |
| Tax cuts and new transfers, net of the remittance excise | 9.87 | 9.76–10.00 |
| **Net taken from the lineage** | **−0.28** | −4.23 to +5.76 |
| Net once the lapsing items are gone (permanent tax items only) | 5.75 | |

**Construction.**
- **Shares.** Tax-Calculator 6.8.4, which models these provisions, runs on CPS ASEC 2025 tax units (`TAX_ID`, 76.7k records) at 2024 incomes. Each run is 2024 law against 2024 law plus one provision at its statutory values. The change in `iitax` is split equally over each unit's members and summed on the lineage weights over row-4 weights. This is the arm's frame (`post2024_law.build_frame`). The script gates that people without a tax record are under 1% [CALCULATION].
- **Take-up.** Every record claims the EITC and the refundable child credit. Tax-Calculator's random take-up draw was moving some records across the line between runs; the first run caught this as a spurious −$7,725 for a six-child family.
- **SSN rules.** Imputed-unauthorized people get no tips, overtime or senior deduction: §§70201(e), 70202(d) and 70103(iv) require a work-authorized SSN. Units that lose the child credit under the SSN rule (§70104(b), priced in the arm) get no child-credit increase, so no unit is counted on both sides.
- **Levels.** JCT's FY2028 score is used where a provision is scored alone (CBO 61570, Title VII). The child-credit increase, the standard-deduction increase, the senior deduction and the SALT change are scored only together with TCJA extensions (§§70102–70104 and 70120's rows). Their national levels come from Tax-Calculator on its own bundled data for TY2027: current law against the provision reverted to 2024 law. That is a model level, not a JCT score [CALCULATION]. Levels are deflated to 2024 dollars by CBO's CPI-U path (FY2028 × 0.906; TY2027 × 0.922).
- **Proxies** [ASSUMPTION]:
  - Tips: 0.40 of wages plus self-employment income in food and drink service (OCCUP 4040, 4110, 4120, 4130, 4150), 0.10 in fast food (4055), and 0.25 in personal care, transport and other tipped occupations (3630, 4400, 4500, 4510, 4521, 4522, 4530, 9141, 9142, 9350).
  - Overtime: the FLSA half-time premium for hourly employees (`A_HRLYWK`, asked in the outgoing rotation only, so the share uses those records) with usual hours over 40. Salaried non-exempt workers are missed.
  - Car-loan interest and cash giving are unobserved. Each unit gets a uniform $1,000 of interest or $500 of giving, so the share follows the tax value of the deduction. Giving rises with income, so the charity share is biased up.
  - Property tax: 1% of an owner household's property value. Mortgage interest is unobserved, so itemizing is understated for everyone.
  - Remittances: the Mexico corridor less H-2 pay ($58.8bn, `consumption_key_2026_09_24`) over the $108.9bn base that JCT's 1% revenue implies, with 0.40–0.65 around it [ASSUMPTION]. The corridor counts every US sender to Mexico, not only the lineage.
  - Trump accounts: the lineage's share of citizen children aged 0.
- **Not priced:** the extra year of inflation on the lower brackets (§70101), the 2/37 limit on itemized deductions (§70111), and the 0.5% floor on itemizers' giving (§70425; it raises $7.2bn nationally in FY2028). The lineage has few itemizers, so all three are small for it [INFERENCE].
- **Ranges.** The tax shares are point estimates; only the remittance share carries a range. The net line's ends pair the benefit side's ends with the tax side's.
- **Gates.** The Tax-Calculator version; every JCT FY2028 cell read back as printed (tips −8,078, overtime −22,982, car loans −9,916, charity −8,149, remittances +1,089, Trump-account outlays 3,685); each provision cuts tax for every record (no change below −$1); each national total is positive; the corridor fits inside JCT's base. Peak memory is 1.6 GB.

## Evidence

- **P.L. 119-21 text.** Enacted text, govinfo PLAW-119publ21, staged at `infra/immigration-fiscal/ir5_adjusters_2026_09_27/_cache/law/pl119_21_govinfo.txt` [SOURCE: https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm]. Section numbers below were checked against that text.
  - §70104(b) rewrites 26 U.S.C. 24(h)(7). No credit for a qualifying child unless the return carries "the taxpayer's social security number (or, in the case of a joint return, the social security number of at least 1 spouse)". The SSN must be issued to a citizen or under SSA's work-authorization clause. It applies to taxable years after 2024.
  - §§10108, 71109 and 71201 limit SNAP, Medicaid/CHIP payments and Medicare to citizens and nationals, LPRs, Cuban and Haitian entrants and COFA residents. SNAP took effect on enactment, Medicaid on 2026-10-01, and Medicare on enactment for new enrollees and 18 months after it for current ones.
  - §71301 limits the PTC to "eligible aliens", the same three classes, for taxable years after 2026-12-31.
  - §71302 strikes 36B(c)(1)(B) from tax year 2026. That ends the credit below 100% FPL for people barred from Medicaid by status, LPRs within the five-year bar included.
  - §71110 caps the FMAP for emergency Medicaid at the state's regular rate from 2026-10-01.
- **CBO scores of P.L. 119-21.** CBO 61570 (2025-07-21), Tables 1 and 7, against the January 2025 baseline, staged with ACQUIRED.md [SOURCE: `sources/immigration-fiscal/data/external/stage3/cbo/pl119_21_estimate/61570-pl119-21-2025Recon-CLB.xlsx`, sha b6f7a7ae…]. FY2028 outlays:
  - §10108: −$0.216bn.
  - §71109: −$0.665bn.
  - §71110: −$3.112bn.
  - §71201: −$0.214bn, rising to −$1.778bn by FY2034.
  - §71301: −$7.923bn, with revenues +$0.544bn.
  - §71302: −$5.159bn, with revenues +$0.018bn.

  The PTC rows use outlays plus revenues, because both are the credit. §71109 has no revenue row. §70104 is scored only as a whole, with the $2,200 credit, so the SSN rule is measured here.
- **The enhanced credit's status.** It expired 2025-12-31. The House passed a three-year extension in January 2026, and as of late July 2026 the Senate had not voted [SOURCE: https://news.ballotpedia.org/2026/01/12/house-passes-three-year-extension-of-expanded-aca-subsidies/; https://www.astho.org/communications/blog/2026/aca-enhanced-premium-tax-credits-legislative-developments-2025-2026/]. No later law was found [UNVERIFIED for August to October 2026].
- **CBO's cost of permanent extension.** CBO 61734 (2025-09-18) gives a net deficit effect of $31.919bn in FY2027 and $30.382bn in FY2028. Its baseline is updated through 2025-08-22, so it comes after P.L. 119-21 [SOURCE: `stage3/cbo/ptc_extension_61734/61734-data.xlsx`, sha 2e92669f…; https://www.cbo.gov/publication/61734].
- **The public-charge rule.** $5.00bn combined, $3.22bn federal, at DHS's 10.3%, and $1.61–8.40bn across 3.3–17.3% [DATA: `public_charge_share_2026_10_07/derived/summary.json`]. These are DHS's dollars as printed. The RIA's price year was not checked, so no deflator is applied [UNVERIFIED].
- **The deflator.** CBO's February 2026 CPI-U path (LTBO 2026, sheet 16, 2026 projections: 2.767%, 2.924%, 2.547% and 2.361% for 2025–2028). FY2028 dollars × 0.906 give calendar-2024 dollars, and FY2027 dollars × 0.928 [SOURCE: `stage3/cbo/ltbo_2026/62044-2026-LTBO.xlsx`].
- **How the account charges the PTC.** The main case carries audit row 1: the $118.35bn PTC part of BEA's refundable-credit line (Treasury MTS, CY2024) is keyed by subsidized-Marketplace persons (CPS `MRKS`), and the rest by EITC+ACTC [DATA: `main_case_2026_09_24/package.cjs` `row1Shifts`; `dataset_integrity_2026_09_23/derived/spending_mts_credits.json`]. The $324 per person-year is the lifetime ledger's per-capita charge, not the annual account's [DATA: `ir5_adjusters_2026_09_27/RESULT.md`, ladder 247]. On the lineage weights that key charges the lineage $13.36bn. At the lineage's modelled enhanced fraction (15.7%), the account's own key implies a $2.09bn cut, against $2.46bn here [CALCULATION].

## Construction

- **Frame.** CPS ASEC 2025 through the distribution lane's loader, with `population_basis.reweight(..., "lineage")`. Shares put the lineage weights in the numerator over a row-4 denominator, as `public_charge_share.py` does. The script gates that the lineage weights total the decomposition's NG (42,752,213) and the row-4 civilians its NC [CALCULATION].
- **Status.** The account's residual imputation (`status_impute_2026_09_16` `impute()`, Borjas rules, all origins). "Lawfully present" here means a noncitizen whom the rules do not class as unauthorized.
  - The CPS cannot separate LPRs from refugees, asylees, parolees or TPS holders. Each eligibility row therefore carries a broad share, every noncitizen recipient outside the kept classes, and a narrow one, those who arrived in 2016 or later. The narrow share is central [ASSUMPTION]. It still contains recent LPRs, so it overstates the lineage's part of the SNAP, Medicaid and Medicare rows.
  - Cuban-, Haitian-, Marshall Islands- and Micronesia-born people stay eligible by statute and leave every denominator.
  - Marketplace coverage is not one of the residual's rules. A subsidized noncitizen whom the rules class as unauthorized is most plausibly a parolee, TPS holder or applicant, so §71301's classes do not condition on the flag.
- **Child tax credit.** Tax units come from `TAX_ID`. A unit loses the credit when every non-dependent member is imputed unauthorized. The amount lost is the CPS tax model's `CTC_CRD + ACTC_CRD` for 2024, less the $500 credit for other dependents, which noncitizen or 17+ dependents keep. Each unit's loss is split equally over its members.
  - National total: $6.48bn. Lineage: $2.20bn, of which $1.02bn refundable, across 3.31M people in such units [CALCULATION].
  - Two factors scale it: the account's on-books share (0.44 / 0.60 / 0.75, `combine_status.py` `ON_BOOKS`), and a 0.80 / 0.90 / 1.00 share of residual-unauthorized filers who truly lack a work-authorized SSN [ASSUMPTION]. The second allows for DACA recipients, parolees and applicants with work permits, who keep the credit.
  - The amount is priced at 2024 credit values. The $2,200 credit indexed to 2028 is about the same in 2024 dollars, so no adjustment is made [INFERENCE].
- **Premium tax credit model.** Used for dollar weights and fractions only. Each tax unit's subsidized members are priced at KFF's 2024 US average benchmark of $477 a month at age 40 on the CMS default age curve [SOURCE: https://www.kff.org/affordable-care-act/state-indicator/average-marketplace-premiums-by-metal-tier/; `ir5_adjusters_2026_09_27/_cache/ptc/cms_state_age_curves_2017.txt`].
  - The contribution is unit AGI times the applicable percentage, measured against HHS's 2023 guidelines ($14,580 + $5,140 a person). Enhanced law uses the ARPA/IRA schedule: 0% below 150% FPL, 8.5% cap, no cliff. Original law uses Rev. Proc. 2025-25's 2026 table: 2.10–9.96%, no credit above 400% [SOURCE: `ir5_adjusters_2026_09_27/_cache/law/irs_revproc_2025-25.txt`]. Units below 100% FPL are priced at 100%.
  - Modelled enhanced fraction of credit dollars: 19.8% nationally, 15.7% for the lineage. The lineage holds 11.3% of subsidized persons, 11.3% of enhanced-law credit dollars and 8.9% of enhancement dollars [CALCULATION].
  - Row (b) is CBO's extension cost times 8.9%. The high end uses 11.3%, for the case where coverage losses take whole credits.
- **Emergency Medicaid.** The lineage's share of imputed-unauthorized adults aged 19–64 at or below 138% FPL in the 2024 expansion states (31.5%). The broad share adds noncitizens who arrived in 2020 or later (27.6%). It is a person share: emergency spending per person is not observed.

## Overlaps: each dollar counted once

- **(a) and (b).** CBO prices (a)'s PTC rows against a baseline where the enhancement has already expired, and prices (b) against a baseline where (a) is already law. The enhancement on (a)'s own people falls between the two. The bridge row adds it back at those classes' modelled enhanced/original ratio: +$0.07bn.
- **(c) and (a).** Someone whom (a) makes ineligible cannot also disenroll under the public-charge rule. The overlap is bounded at DHS's rate times (a)'s lineage SNAP and Medicaid cut: −$0.01bn.
- **(c) and the PTC or the CTC.** DHS's rule prices Medicaid, CHIP, SNAP, WIC, TANF, SSI and rental assistance. It does not cover the PTC or the CTC, so those rows do not overlap. Emergency Medicaid does not count toward public charge.
- **Emergency FMAP.** It moves cost from federal to state and leaves consolidated spending unchanged unless states cut coverage. It is excluded from the consolidated total.

## Gates

`post2024_law.py` stops with `[BLOCKED]` unless every gate passes:
- the staged files' SHA-256 match;
- CBO's FY2028 cells read back as printed (§10108 −216, §71110 −3,112, §71301 −7,923 / +544, §71119 −18,960; extension 30,382 and 31,919);
- the LTBO CPI path holds 2.547% for 2027;
- the CMS age curve reads 1.000 / 1.278 / 3.000 at 21 / 40 / 64;
- the status flags align with the frame;
- the lineage and row-4 totals match the decomposition;
- no record carrying the added descendants' weight is a noncitizen;
- the CTC loss is non-negative;
- original-law credits never exceed enhanced ones;
- every class share lies in [0, 1) with records.

The rerun ends `IDENTICAL: 6/6`, exit 0. Peak memory is about 0.5 GB.

## Limits

- **Recent LPRs in the narrow shares.** The share for each non-LPR class is a recency proxy, not a status measure. For SNAP, Medicaid and Medicare the bias raises the cut, but those rows are $0.14bn in all. For §71301 the narrow share (6.1%) could be low if Mexican nonimmigrants or applicants arrived before 2016. The broad share bounds it at 15.9%.
- **Fixed CTC factors.** The on-books share and the work-authorized-SSN share are judgment factors, not measurements. No public ITIN-by-origin tabulation was used.
- **National benchmark premium.** State benchmarks would shift the PTC fractions. The lineage lives mostly in CA and TX.
- **Static allocation of the PTC expiry.** CBO's $30.4bn includes people who drop coverage. The static share allocates by enhancement dollars, and the high end by whole credits.
- **Uncompensated care.** Coverage lost from Medicaid and the PTC partly returns as uncompensated care, which the account charges by use. That offset is not priced and would shrink every health row.
- **Population growth.** CBO's FY2028 dollars are for the FY2028 population, while the shares come from 2024 records.
- **The state Medicaid match on §71109 is left out.** CBO scores federal outlays only, so the state match the rule also saves is not counted. It is worth about +$0.06bn at a 59% FMAP [INFERENCE].
- **Medicaid-based status rule.** The status imputation prints `[DEGRADED]`: its Medicaid clause classes every Medicaid reporter as legal, which is wrong in status-blind states such as California. The state-aware variant (`california_medical_status_2026_09_23/cps_ca_status.py`) was not used. The bias undercounts the lineage's unauthorized adults. That understates the SSN-rule child-credit loss and the emergency-Medicaid share, and slightly overstates the lineage's tips, overtime and senior deductions. Both errors make the net cut look smaller than it is [INFERENCE].
- **Not part of the arm:** the 2025 Marketplace Integrity rule (CBO 61734 prices its nullification at $1.3bn nationally in FY2027), the programme-wide P.L. 119-21 provisions listed above, and the tax cuts.

## Reproduce

From the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/post2024_law_2026_10_07/post2024_law.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with taxcalc==6.8.4 python3 infra/immigration-fiscal/post2024_law_2026_10_07/tax_side.py
    uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/post2024_law_2026_10_07 "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/post2024_law.py" "OPENBLAS_NUM_THREADS=1 uv run --no-project --with taxcalc==6.8.4 python3 {lane}/tax_side.py"

The second script reads `derived/summary.json`, so it runs after the first. The rerun ends `IDENTICAL: 9/9`, exit 0.

Inputs staged for this lane: `sources/immigration-fiscal/data/external/stage3/cbo/ptc_extension_61734/` (ACQUIRED.md). Not committed; the lead commits.

## Log
- 2026-10-07 10:43 JST: lane opened; stub written.
- 2026-10-07 10:52 JST: inputs traced [DATA].
  - CBO 61570's Title I and VII rows for §§10108, 71109, 71110, 71201, 71301 and 71302 (FY2025–34) read from the staged workbook.
  - Statute text reused from `ir5_adjusters_2026_09_27/_cache/law/pl119_21_govinfo.txt`: §70104(b) taxpayer work-authorized SSN; §71301 eligible aliens = LPR / Cuban-Haitian entrant / COFA, effective tax years after 2026-12-31; §71110 effective 2026-10-01; §71201 18 months after enactment.
  - Enhanced PTC: expired 2025-12-31; the House's three-year extension (Jan 2026) not passed by the Senate as of late July 2026 [SOURCE: https://news.ballotpedia.org/2026/01/12/house-passes-three-year-extension-of-expanded-aca-subsidies/; https://www.astho.org/communications/blog/2026/aca-enhanced-premium-tax-credits-legislative-developments-2025-2026/].
  - CBO 61734 (2025-09-18) data workbook staged: permanent extension $31.9bn net deficit in FY2027, $30.4bn in FY2028.
  - The main case charges the PTC part of the refundable line ($118.35bn, Treasury MTS CY2024) by subsidized-Marketplace persons (MRKS), not per capita (audit row 1, `main_case_2026_09_24/package.cjs` row1Shifts). The $324 per capita is the lifetime ledger's (ladder 247).
- 2026-10-07 10:55 JST: first full run. The CTC national total ($6.48bn × on-books) ran above the scan memo's JCT-based $1.5–3bn, which led to adding the work-authorized-SSN factor (0.80–1.00), since the residual's unauthorized include DACA recipients and parolees with work permits.
- 2026-10-07 10:56 JST: rerun IDENTICAL 6/6, exit 0.
- 2026-10-07 10:57 JST: RESULT written.
- 2026-10-07 10:59 JST: lead asked for the tax side (symmetry). Read the enacted text of §§70102, 70103, 70104, 70120, 70201–70204, 70424 and 70604. Tax-Calculator 6.8.4 models the OBBBA provisions (TipIncomeDed, OvertimeIncomeDed, SeniorDed, AutoLoanInterestDed, ID_AllTaxes_c phase-down, STD_charity_ded_nonitemizers_max).
- 2026-10-07 11:05 JST: refactored the frame into `post2024_law.build_frame()`; rerun IDENTICAL 6/6, so the benefit rows are unchanged.
- 2026-10-07 11:10 JST: Tax-Calculator's random EITC/ACTC take-up draw gave spurious tax increases (one six-child family −$7,725). Fixed by setting full take-up in every run.
- 2026-10-07 11:13 JST: first full tax-side run. Peak memory 2.9 GB, over the 2.5 GB limit, so the national runs were moved ahead of the CPS frame with explicit frees: 1.6 GB.
- 2026-10-07 11:15 JST: rerun IDENTICAL 9/9, exit 0. Tax side $9.87bn; net −$0.28bn (−4.23 to +5.76); $5.75bn once the lapsing items are gone.
