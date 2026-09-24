**Verdict:** In calendar 2024 the five jurisdictions spent about $4.7bn on migrant shelter and
emergency response ($4.6–5.2bn; New York City $3.4bn of it) [CALCULATION: cy2024_outlays.csv].
About 95% was state and local money [CALCULATION: federal ≈ NYC ½×120 + ½×88, Massachusetts
½×6 + ½×19, Chicago 141.5 = $0.26bn of $4.7bn, from Table 1].
FEMA covered 3% of NYC's FY2024 spending, 1–2% of Massachusetts's and 39% of Chicago's 2024
payments. Every FY2024 Shelter and Services Program award to these governments now shows $0 on
USAspending [DATA: _cache/src/usaspending_ssp_97141.json].

Mexican nationals were 0.50–0.84% of the people served wherever origins are published: NYC
shelters in 2025 and Chicago shelter exits in 2024. Venezuelans were 33% and 81% [SOURCE/DATA:
part 2].

The Census individual-unit files do not isolate the outlays. NYC's reported current spending in
welfare, housing, health and other/unallocable rose by $1.47bn in FY2023 and $3.86bn in FY2024 over
FY2022. That is about the size of its asylum spending ($1.47bn; $3.75bn). However, none of those
functions grew faster than the peer median in FY2024. NYC's FY2024 hospital line also repeats the
FY2022 figure to the thousand dollars, so H+H's $1.53bn cannot show. Chicago's functions were
recoded in the same years. Denver's and DC's outlays are smaller than the ordinary swings in
their lines [CALCULATION: census_unit_test.py → derived/].

The complete account spreads these outlays with national keys. Those keys give the Mexican-origin
union 12.9–22.6% of the outlays, against its 0.5–0.84% share of the people served. The account
therefore over-charges the union by about $0.5bn a year (central; $0.45–0.84bn across mappings A–C,
up to $1.16bn). That is 0.2–0.5% of the $203–250bn main case [CALCULATION: census_unit_test.py →
derived/account_keying.csv].

Scope: NYC, New York State, Massachusetts (Emergency Assistance family shelter), Chicago and Illinois,
Denver, Washington DC, FY2023–FY2026. Dollar figures are $ million unless marked bn. Sources are in
`_cache/src/` (ignored); page numbers are printed page numbers unless marked PDF.

## 1. Budgets

### Table 1. Spending on migrants and asylum seekers, by fiscal year ($M)

| Jurisdiction (fiscal year) | Year | Total | Local | State | Federal | Source |
|---|---|---:|---:|---:|---:|---|
| New York City (Jul–Jun) | FY2023 actual | 1,474 | 1,139 | 335 | 0 | [SOURCE: NYC Comptroller, *Accounting for Asylum Seeker Services: Fiscal Impacts*, Table 2 (OMB, Adopted FY2026 Plan)] |
| | FY2024 actual | 3,752 | 2,323 | 1,310 | 120 | same |
| | FY2025 actual | 3,020 | 1,477 | 1,455 | 88 | same |
| | FY2026 adopted | 1,303 | 1,162 | 103 | 37 | same |
| New York State, own funds (Apr–Mar) | SFY2023 actual | 27 | – | 27 | 0 | [SOURCE: NYS DOB, FY2026 Enacted Budget Financial Plan, p.124] |
| | SFY2024 actual | 895 (519 paid to NYC) | – | 895 | 0 | same |
| | SFY2025 actual | 1,179 (772 to NYC) | – | 1,179 | 0 | same |
| | SFY2026 projected | 1,602 (1,331 to NYC) | – | 1,602 | 0 | same |
| Massachusetts EA shelter, **all families** (Jul–Jun) | FY2023 | not recovered | | | | see gaps |
| | FY2024 actual | 894.0 | – | ≈888 | 6 SSP | [SOURCE: A&F/EOHLC EA report 8 Sep 2025 (HD5125), Fiscal table; SSP: EA report 16 Dec 2024, p.6] |
| | FY2025 actual | 978.2 | – | ≈959 | 19 SSP | same |
| | FY2026 appropriation | 276.4 | – | | | HD5125 |
| Chicago, city payments by invoice year (Jan–Dec) | 2022 | 12.2 | 11.2 | 0 | 1.0 | [DATA: portal gxzc-43gg → derived/chicago_payments_by_year_fund.csv] |
| | 2023 | 254.8 | 63.4 | 80.2 | 111.2 | same |
| | 2024 | 366.0 | 224.5 (city 188.1, Cook County 36.3) | 0 | 141.5 (69.6 via the State) | same |
| | 2025 (file to July) | 6.6 | 6.6 | 0 | 0 | same |
| Illinois State | Aug 2022–FY2024, provided or committed | ≥638, plus 160 announced | – | most | ≥82 inside | [SOURCE: Illinois Governor's office overview, 16 Nov 2023, p.1] |
| Denver (Jan–Dec) | 2023 actual, partial | 14.5 | 11.0 | 3.5 | FEMA SSP FY2023 award 8.0 | [SOURCE: Denver 2025 Adopted Budget, pp.138, 576; DATA: USAspending] |
| | 2024 estimate | 45.4 (90 budgeted) | | | | pp.138, 20 |
| | 2025 budget | 12.5 | | | | pp.20, 138 |
| Washington DC, DHS Office of Migrant Services (Oct–Sep) | FY2022 actual | 0 | | | | [SOURCE: DC FY2025 Approved Budget, DHS schedule 30-PBB, PDF p.2] |
| | FY2023 actual | 52.2 | split not published | | | [SOURCE: DC FY2026 Proposed Budget, DHS schedule 30-PBB, PDF p.2] |
| | FY2024 actual | 63.1 | split not published | | | same |
| | FY2025 approved | 39.9 | 39.9 | – | 0 | same |
| | FY2026 request | 0 | | | | same |

The following notes explain how to read Table 1.

- NYC "State" is State aid as the City accrues it. By 31 July 2025 the State had paid $1.26bn of the
  $3.25bn budgeted for FY2023–FY2026 [SOURCE: Comptroller, Fiscal Impacts]. New York State's "paid
  to NYC" rows are the same dollars; do not add them. The State's direct uses were 376 in SFY2024,
  407 in SFY2025 and 271 in SFY2026: National Guard, Medicaid/vaccines/testing, Safety Net
  Assistance, resettlement and case management/legal [CALCULATION: rows of the p.124 table].
- Massachusetts's figures cover every family in Emergency Assistance. Migrant families were 3,265
  of 6,878 on 12 Dec 2024 (47.5%) and 2,955 of 6,167 in January 2025 (47.9%) [SOURCE: EA reports
  16 Dec 2024 p.2 and 27 Jan 2025]. The draft Special Commission report says "approximately half".
  On 4 Sep 2025 the figure was 907 of 2,709 (33.5%) [SOURCE: HD5125]. The migrant part is
  therefore about $0.36–0.45bn in FY2024 and $0.39–0.49bn in FY2025 [CALCULATION: 0.40–0.50 ×
  total].
  "≈888" and "≈959" subtract only the FEMA SSP amounts the State says it applied. An 1115-waiver
  Medicaid reimbursement is mentioned without an amount.
- Chicago's local column is City Corporate Fund plus the Cook County grant. Federal is FEMA (SSP,
  EFSP, and two unlabeled FEMA funds totalling $25.7M), ARPA SLFRF and a $1.6M federal
  public-health preparedness grant.
  The City's own count through end-2023 is $295M: $72M city, $80M State and $143M federal
  [SOURCE: City press release, 12 Apr 2024]. The payment file gives $267.0M for 2022–2023.
- Denver's 2023 figure is the new Border Crisis Response special revenue fund plus a State (DOLA)
  grant. It misses general-fund agency spending before the fund existed. The high case in part 4
  uses $90M budgeted less $22.5M returned for 2024 [SECONDARY: Colorado Springs Gazette,
  6 Mar 2025].
- Federal programs: in FY2023 Congress moved $800M from CBP to FEMA. FEMA awarded EFSP-Humanitarian
  grants of $75M and $350M and made $363.8M available for the Shelter and Services Program (SSP)
  [SOURCE: CRS R47681]. FY2024 SSP-Allocated was $300M [SOURCE: FEMA FY2024 SSP-A fact sheets].
  NYC received $120M ($70.6M SSP, $49.0M EFSP). FEMA paid NYC a further $80.5M of FY2024 SSP in
  February 2025 and then reversed the deposit [SOURCE: Comptroller, Fiscal Impacts]. On USAspending,
  pulled 23 Sep 2026, the SSP awards with positive obligations sum to $123.4M. Every FY2024 award to
  NYC, Chicago, Illinois DHS, Denver, DC (two) and Massachusetts (EOHLC, EOHHS) shows $0 [DATA:
  usaspending_ssp_97141.json]. This fits withheld or terminated awards [INFERENCE]. Chicago's
  payments charged to FEMA funds may therefore not all have been reimbursed.

### Peak migrant shelter census

| Place | Peak | Source |
|---|---|---|
| New York City | "nearly 70,000 individuals in January 2024"; more than 239,200 entered the shelter system since spring 2022; about 33,300 on 28 Sep 2025 | [SOURCE: NYC Comptroller, asylum-seeker census page] |
| Chicago | "a peak of nearly 16,000 in December 2023" | [SOURCE: City press release, 15 May 2024] |
| Massachusetts | capacity capped at 7,500 families; 5,500 families by August 2023; 6,878 certified families, 3,265 of them migrant, on 12 Dec 2024 (families, not people) | [SOURCE: Special Commission draft 15 Nov 2024; EA report 16 Dec 2024 pp.2, 5] |
| Denver | not recovered from a primary document; the archived dashboard page holds its numbers in an embedded widget | [UNVERIFIED] |
| Washington DC | not recovered | [UNVERIFIED] |

### What the money bought

- **NYC, by work type, FY2023 / FY2024 / FY2025 ($M):** services and supplies 569 / 1,540 / 1,160;
  housing, rent and initial outfitting 568 / 1,530 / 1,160; IT, administration and other
  149 / 343 / 228; food 106 / 259 / 217; medical 57 / 77 / 60; total 1,450 / 3,750 / 2,820.
  By agency: DHS 764 / 1,190 / 1,070, H+H 469 / 1,530 / 982, HPD 33 / 413 / 272, DCAS
  38 / 293 / 294, NYCEM 88 / 111 / 47, OTI 30 / 91 / 75, Law 0 / 33 / 40, DOE 0 / 0.5 / 0.6
  [SOURCE: NYC Council Terms and Conditions report, June 2025, p.2]. Legal services are the Law
  Department line plus State "Legal Services" grants of $40M and $49M spent through several
  agencies [SOURCE: same report, pp.8–9]. Schooling of migrant children sits in the Department of
  Education's regular budget, not in these totals [INFERENCE: DOE's asylum line is $0.5M].
- **New York State:** Medicaid/vaccines/testing 137 in each of SFY2024 and SFY2025; Safety Net
  Assistance 26 and 67; case management/legal/other 42 and 34. The Medicaid and Safety Net figures
  are estimates [SOURCE: NYS DOB FY2026 Enacted Financial Plan, p.124, footnote 1].
- **Massachusetts FY2025 ($M):** direct shelter 734.0, respite and assessment sites 63.1, National
  Guard 10.2, exits (incl. HomeBASE) 99.4, education aid and support 32.5, room-tax reimbursements
  1.4, new-arrival supports 9.3, public and mental health 7.1. Supplemental school-district aid
  totalled $74.6M over FY2023–FY2025 [SOURCE: HD5125 Appendices B and C, via Firecrawl text; see
  gaps].
- **Chicago:** the payment file covers shelter operations and vendors. Chicago Public Schools
  "enrolled 11,692 children who meet three newcomer criteria" [SOURCE: press release, 12 Apr 2024].
  New arrivals made more than 90,000 health visits at Cook County Health [SOURCE: press release,
  15 May 2024]; the County's cost of them is outside the City's payment file [INFERENCE].

### Page quotes (verbatim, from `_cache/src/`)

- NYC Comptroller, Fiscal Impacts (`nyc_comptroller_fiscal_impacts.txt`), about Table 2:
  - "Table 2: Funding for Asylum Seekers (FY 2023 FY 2024, and FY 2025 Actuals), as of the Adopted
    2026 Financial Plan"
  - "“Actuals” represent amounts in the City’s Financial Management System as of October 2025,
    which are still preliminary accrued costs and are subject to revision; FY 23 Actuals are
    adjusted for an anticipated write-down of State funding."
  - "Prior to February 4, 2025, the City received $120 million in FEMA funding ($70.6 million for
    the Shelter and Services Program (SSP), and $49.0 million for the Emergency Food and Shelter
    Program (EFSP))."
  - "the federal government reversed the deposit to the City."
- NYC Comptroller, census page (`nyc_comptroller_census.txt`): "a significant decline of 51
  percent from the peak of nearly 70,000 individuals in January 2024. Since the spring of 2022,
  more than 239,200 asylum seekers have entered the City’s shelter system."
- NYS DOB, FY2026 Enacted Budget Financial Plan (`nys_dob_fy26_enacted_fp.pdf`), p.124 (PDF p.130):
  - "The table below summarizes the extraordinary State Funding for asylum seeker assistance spent
    through FY 2025 and planned over the multi-year Financial Plan period."
  - "Total State Funding 27 895 1,179 1,602 620 4,323"
  - "To date, New York State has received little to no Federal funding assistance"
- Massachusetts EA report, 16 Dec 2024 (`ma_af_ea_report_2024_12_16.pdf`):
  - p.2, Caseload table (datapoint | value | notes; the PDF text interleaves the columns): "Total
    families in EA who entered as migrants, refugees, or asylum seekers" | "3,265" | "Estimate
    based on family head of household citizenship status and primary language spoken."
  - p.6: "$7 M award for additional FEMA SSP-A grant via the first 2024 funding round … $6 M of
    award will be used for FY24 TRC/CSR costs"
- HD5125, EA report of 8 Sep 2025 (`ma_af_ea_report_2025_09_firecrawl_excerpt.md`): "Total amount
  expended on the emergency housing assistance program in FY24 | $894.0 M | Figure includes
  $393.2 M from reserves 1599-0514 and 1599-1213".
- Massachusetts Special Commission draft, 15 Nov 2024 (`ma_special_commission_2024_firecrawl_excerpt.md`):
  "Recognizing that new arrival families represent approximately half of the EA shelter caseload"
- Massachusetts State Auditor, EOHLC Emergency Shelter audit, May 2025 (`ma_auditor_eohlc_shelter_2025.pdf`):
  - p.8: "During the audit period, a total of 17,848 families applied for an EA shelter. Out of
    these, 7,708 families were successfully placed"
  - p.52: "payment records made to shelter providers during the audit period totaled $700,020,207"
- Chicago press release, 12 Apr 2024 (`chi_pr_2024_04.txt`): "Costs for the Mission, since it
  began in August of 2022, through the end of 2023 have totaled $295 million."
- Chicago press release, 15 May 2024 (`chi_pr_2024_05.txt`): "down more than 50 percent from a
  peak of nearly 16,000 in December 2023".
- Illinois overview (`il_gov_investment_overview_2023_11.pdf`), p.1: "Since August 2022, Illinois
  has provided or committed over $638 million in funding to address the humanitarian asylum seeker
  crisis, including direct funding to the City of Chicago."
- Denver 2025 Adopted Budget (`den_budget_2025_adopted.pdf`):
  - p.138, columns 2023 Actuals / 2024 Estimated / 2025 Estimated: "Human Services 13809 Border
    Crisis Response - - - 11,001,278 45,400,000 12,500,000"
  - p.576: "Migrant Response Program 3,500,000"
  - p.112: "In 2024, a total of $44.9 million was transferred into this fund to support the
    Newcomer program"
  - p.20: "this budget includes $12.5 million for newcomer support in 2025, a decrease from the $90
    million budgeted in 2024."
- DC FY2026 Proposed Budget, DHS schedule 30-PBB (`dc_dhs_tables_fy26m.pdf`), PDF p.2, columns
  FY2023 Actual / FY2024 Actual / FY2025 Approved / FY2026 Request: "MIGRANT SERVICES H03028 52,186
  63,121 39,860 0".
- CRS R47681 (`crs_R47681.html`): "In FY2023, a total of $363.8 million is being made available
  for the SSP in two tranches."
- FEMA FY2024 SSP-A fact sheet (`fema_ssp_a_fy24_factsheet.txt`): "In FY 2024, the total amount
  awarded under SSP-A is $300 million."

## 2. Who was served

| Population | Date | People | Venezuela | Mexico | Source |
|---|---|---:|---:|---:|---|
| NYC asylum seekers in City care | 28 Feb 2025 | 43,578 | 14,438 (33.1%) | 219 (0.50%) | [SOURCE: NYC Council T&C report, Feb 2025, p.10] |
| NYC asylum seekers in City care | 30 Jun 2025 | 36,684 | 12,034 (32.8%) | 231 (0.63%) | [SOURCE: NYC Council T&C report, June 2025, p.11] |
| Chicago shelter exits at the stay limit | weeks ending 5 May–29 Dec 2024, 35 weeks | 4,190 exits | 3,383 (80.7%) | 35 (0.84%) | [DATA: portal fk7i-xuiy → derived/chicago_exits_by_country.csv] |
| Massachusetts EA families | 12 Dec 2024 | 3,265 migrant of 6,878 | not published | not published | [SOURCE: EA report 16 Dec 2024, p.2] |

- In NYC, Mexico ranks 20th (February) and 19th (June). The larger groups are Ecuador (7,394;
  6,229), Colombia (4,182; 3,545), Guinea (2,995; 2,589), Peru and Honduras. "USA" (1,155; 1,104)
  "Includes children born in United States".
- In Chicago the next groups are Colombia 366, Ecuador 153 and Peru 45.
- Massachusetts classifies families from head-of-household citizenship and language and publishes
  no nationality list. Denver and DC published none that I could recover.

**Mexican nationals are not a material share of those served:** 0.50–0.84% where measured, against
the union's 12.0% of the population key [DATA: `../full_account_spending_2026_09_20/derived/allocations.csv`].
The measured dates are 2025 in NYC and May–December
2024 in Chicago. The 2022–2023 peak period is not covered, so part 4 also runs a 2% allowance.

## 3. The Census-file test

### Method

`census_unit_test.py` reads the Annual Survey of State and Local Government Finances
individual-unit files for survey years 2021–2024. The 2021–2023 files come from
`../local_spending_composition_2026_09_18/_cache/`; the 2024 file comes from
`../detention_reconciliation_2026_09_20/_cache/`. The script covers 7 target and 25 peer
governments. It asserts every unit's name, record length and year in every file, and it stops if
any is missing.

Survey year Y covers fiscal years ending 1 July Y−1 to 30 June Y. For example, NYC's survey-2024
figures are its FY2024 (July 2023–June 2024), and Chicago's and Denver's are calendar 2023.

The Census manual codes "temporary shelters and other services for the homeless" to public welfare
\*79 (PDF p.188). It excludes "shelters or housing for the homeless" from housing \*50 (PDF p.166)
[SOURCE: Census Government Finance and Employment Classification Manual,
`../detention_reconciliation_2026_09_20/_cache/census_classification.pdf`].

The baseline is 2022, not 2021. The 2021 file carries finer codes: E74/E75 vendor payments, J67/J68
cash assistance, G capital and C/L codes by function. The 2022–2024 files, all re-released on
15 July 2026, fold these into E79, F, C89 and other codes. For example, Massachusetts's E79 goes
from $2.2bn in 2021 to $31.7bn in 2022 [DATA: derived/census_target_items.csv].

The test measure is current operations (E codes) in the candidate functions: welfare, housing,
health, hospitals and other/unallocable. It excludes construction because NYC's construction codes
are imputed. It also excludes financial administration (E23), which carries a reporting break in
the 2022 file (see "The E23 reporting break" below). A target's peer comparison is its growth over
2022 against the median growth of peer governments of the same kind.

### Result by government

| Government | Survey year = fiscal period | Migrant outlay | Change vs 2022, current ops in candidate functions | Target growth | Peer median growth (range) |
|---|---|---:|---:|---:|---|
| NYC | 2023 = FY2023 | 1,474 | +1,220 | +3.0% | +13.5% |
| NYC | 2024 = FY2024 | 3,752 | +3,859 | +9.6% | +29.7% (18.8 to 32.0) |
| New York State | 2024 = SFY2024 | 895 (376 direct) | +19,775 | +19.3% | +9.7% (1.3 to 22.4) |
| Massachusetts | 2024 = FY2024 | 894 (EA, all families) | +4,593 | +11.9% | +9.7% (1.3 to 22.4) |
| Chicago | 2024 = CY2023 | 255 | −412 | −14.8% | +8.2% (−13.7 to 28.2) |
| Denver | 2024 = CY2023 | ≥14.5 | −64 | −8.1% | +11.7% (−14.7 to 56.1) |
| DC | 2024 = FY2023 | 52.2 | +293 | +3.1% | +29.7% (18.8 to 32.0) |

[CALCULATION: derived/census_vs_budget.csv, derived/census_jump_test.csv]. The peers are
Philadelphia, San Francisco, Los Angeles County and City, and Baltimore for NYC and DC. For
Chicago they are Houston, Phoenix, San Antonio, San Diego, Dallas, Seattle and Columbus. For Denver
they are Nashville, Louisville, Indianapolis, Jacksonville and Honolulu. The state peers are eight
states from Connecticut to Wisconsin (list in the script).

### Which functions carry the change: NYC

| NYC code (all reported, flag R) | FY2023 vs FY2022 | FY2024 vs FY2022 | Asylum spending of the agency likely coded there [INFERENCE], FY2023 / FY2024 |
|---|---:|---:|---|
| E79 public welfare n.e.c. (shelters) | +675 | +1,020 | DHS 764 / 1,190 |
| E50 housing and community development | +295 | +1,364 | HPD 33 / 413 |
| E89 other and unallocable | +275 | +1,204 | DCAS + NYCEM + OTI 156 / 495 |
| E32 health | +224 | +271 | DOHMH 6 / 10 |
| **Sum of the four** | **+1,470** | **+3,859** | all agencies 1,450 / 3,750 |
| E36 hospitals | −249 | **0: the FY2022 value repeated** | H+H 469 / 1,530 |

[DATA: derived/census_target_items.csv; SOURCE for agencies: NYC Council T&C report, June 2025,
p.2]

- The four codes' increase matches the asylum total, but not code by code. E50's increase is 3.3
  times HPD's asylum spending, and the FY2024 increase includes H+H's share only if H+H's shelter
  costs were coded outside hospitals.
- Against peers, nothing stands out. In FY2024 NYC grew slower than the peer median in every
  candidate function: welfare +10.8% vs +21.2%, housing +30.0% vs +30.9%, health +13.3% vs
  +25.8%, hospitals −1.7% vs +18.5%, other +9.3% vs +18.4%. In FY2023 only health outgrew its
  peers (+10.6% vs +3.4%, about $0.15bn), against $6M of health-department asylum spending
  [CALCULATION: derived/census_jump_test.csv].
- NYC's E36 (hospital current operations) is $10,297,619 thousand in both the 2022 and the 2024
  files, flagged R, while FY2023 differs ($10,048,141 thousand). This is the only large repeated
  value among NYC's codes [DATA: derived/census_repeated_values.csv]. A $10.3bn line matching to
  the thousand dollars two years apart is almost certainly carried forward, not reported afresh
  [INFERENCE]. The 2024 file therefore cannot show H+H's $1.53bn of FY2024 humanitarian-center
  spending, whether or not it would have been coded to hospitals.
- NYC's state aid (all C codes) rose $4.15bn by FY2023 and $4.49bn by FY2024. State asylum aid was
  $0.34bn and $1.31bn in those years, so other programs dominate the aid series [DATA:
  derived/census_jump_test.csv].

### Other targets

- **Chicago (CY2023):**
  - E79 rose $231M, close to the $255M of 2023 payments and the right code for shelters.
  - In the same file E50 fell from $369M to $11M, E23 (financial administration) rose from $2.23bn
    to $4.46bn, F89 rose $560M and F44 fell to zero. This is a reclassification, and it leaves no
    stable baseline.
  - Welfare grew 58.9% against a peer median of 44.0% (range −98% to +1,110%): an excess of $58M.
- **Denver (CY2023):**
  - Welfare rose $58M (+38%) while its peers' median fell 9.4%, an excess of $73M. That is larger
    than the partial $14.5M budget figure and plausible for Denver's late-2023 surge [INFERENCE].
  - In the same year housing fell $94M and the hospital line went to zero, so current operations in
    candidate functions fell $64M. Not identified.
- **DC (FY2023):** the Office of Migrant Services' $52.2M is 0.9% of DC's welfare line, which grew
  9.5% against the peer median's 21.2%. Undetectable.
- **Massachusetts (FY2024):**
  - Housing (E50) rose $523M; all housing spending rose 33.6%, in line with the peers' +34.9%.
  - Other/unallocable rose $1.42bn (+51.3% against +17.7%), an excess of $0.93bn. That is about the
    size of the $894M EA total and could hold the $393M the program spent from reserve accounts
    [INFERENCE]. The catch-all code does not identify it.
  - Welfare (+7.4%) is dominated by Medicaid, which the 2022+ files fold into E79.
- **New York State (SFY2024):**
  - Direct asylum uses ($376M) vanish inside a Medicaid-driven welfare line of $97bn.
  - State aid to local governments for welfare (M79) rose $1.95bn, of which $0.37bn is above the
    peer median. That is consistent in size with the $519M paid to NYC, but not identified.
- **Illinois:** welfare grew $3.3bn faster than its peers. The shelter payments are too small to
  explain that; the size points to other programs such as Medicaid [INFERENCE].

[DATA: derived/census_target_items.csv, derived/census_jump_test.csv]

### The E23 reporting break

Financial administration current operations (E23) jumps in the 2022 file for many governments,
with no offsetting fall in their other items. The county IV lane found this first
(`../gg_response_county_iv_2026_09_23/RESULT.md`). In these unit files the break is present in 2022
and stays at the new level, or keeps rising, through 2024:

| Unit | 2021 | 2022 | 2023 | 2024 | Share of 2024 total |
|---|---:|---:|---:|---:|---:|
| NYC | 565 | 10,118 | 9,528 | 9,807 | 7.6% |
| Chicago | 163 | 2,227 | 2,927 | 4,465 | 30.0% |
| Cook County government | 58 | 80 | 76 | 63 | 0.8% |
| Denver | 121 | 163 | 150 | 296 | 6.0% |
| DC | 350 | 823 | 286 | 284 | 1.4% |
| Massachusetts state | 876 | 987 | 1,090 | 1,222 | 1.8% |

[DATA: derived/census_e23_by_unit.csv, which covers all 33 units]

- Cook County government's own E23 has no break. The county IV lane's "Cook County +$2.0bn" is a
  county-area figure; Chicago city's +$2.06bn from 2021 to 2022 accounts for it [INFERENCE:
  that lane sums all local units in a county].
- Peers break too: Philadelphia (80 → 1,035), Wisconsin (221 → 2,464), New Jersey (1,114 → 3,982 in
  2022, then 1,839), Jacksonville (249 → 777). Massachusetts has no break.

**What it changes here.** Nothing in parts 3 or 4 rests on E23:
- The candidate functions, the current-operations test measure and the part weights (E79, E50,
  E89, E32) exclude it.
- `census_jump_test.csv` and `census_vs_budget.csv` report total direct spending with and without
  E23. Without it, NYC grows 7.8% against the peer median's 21.6% (with it: 6.9% against 22.1%).
  Denver and DC stay below their peers either way. Massachusetts, New York State and Illinois keep
  their excess (for Massachusetts, +$2.07bn without E23, +$2.15bn with it).
- Chicago's total is the one reading E23 reverses. With E23 Chicago outgrows its peers (+27.3%
  against +20.3%); without it, it falls behind (+10.1% against +18.4%). Chicago's total should not
  be read with E23 in it.
- NYC's E23 fell $311M from 2022 to 2024 while E89 rose $1.20bn. Netting the two changes the part
  weights from 26/35/31/7% to 29/38/25/8%. Mapping A's key share moves from 12.9% to 13.0%.
  The arithmetic is (1,020, 1,364, 1,204 − 311, 271) ÷ 3,549, weighted by 16.5/12.0/12.0/7.7%
  [CALCULATION]. At the general-government responses of 0.59–0.84, the central over-charge rises
  by $0.01–0.02bn: $508–550M becomes $525–559M.

[DATA: derived/census_jump_test.csv, rows total_direct_general and total_direct_general_ex_e23]

### Sampling and reporting limits

Sampling does not limit this comparison; reporting does.

- The 2024 methodology puts "All county governments with a 2022 population of 500,000 or more",
  "All cities and townships with a 2022 population of 200,000 or more" and "All local government
  units in Hawaii and the District of Columbia" in certainty strata. It adds that "All 50 state
  governments, the District of Columbia, and independent school districts were also designated as
  certainty units" [SOURCE: Census, 2024 Annual Survey of Local Government Finances methodology,
  PDF p.4, `../detention_reconciliation_2026_09_20/_cache/census_2024_method.pdf`].
- All 32 governments appear in all four files. No target has imputed amounts in current operations
  in the candidate functions in 2022–2024 [DATA: derived/census_unit_measures.csv,
  imputed_thousands].
- NYC's imputed items there are construction codes: $2.26bn in 2023 and $2.70bn in 2024, excluded
  from the test measure. Chicago's imputed items are airports, parking, sewerage, water, federal
  revenue and debt items, all outside the candidate functions.
- The limits that bind are these:
  - carried-forward lines: NYC E36;
  - the E23 break in the 2022 file, kept out of every measure above;
  - recoding between years: Chicago, and the peers' own swings, e.g. Los Angeles City welfare
    +3,960% and Columbus +1,110%;
  - the 2021→2022 code-set break;
  - growth elsewhere of the same order as the outlays. NYC's peers grew 30% in two years.

## 4. Account implication

### Where the outlays sit in the account

The outlays are state and local current spending, so they are inside BEA's calendar-2024 national
totals, which the complete account distributes through keys [INFERENCE: BEA does not itemize
them].

By the Census functions they land in (NYC: E79, E50, E89, E32), the likely BEA categories are
these [SOURCE: `../full_account_spending_2026_09_20/derived/categories.csv`; shares from
`../full_account_spending_2026_09_20/derived/allocations.csv`, scenario
complete_preferred_F_per_capita, personal allocation]:

| BEA category (account name) | Key | Union share of key | Main-case response |
|---|---|---:|---|
| Income security consumption (`income_security_services`) | cash_assistance | 16.5% | full |
| Housing and community services (`housing_community_services`) | population | 12.0% | full |
| General public services (`general_public_services`) | population | 12.0% | 0.59–0.84 |
| Health consumption (`health_services`) | health_other | 7.7% | full |
| State and local "Other" social benefits (`other_state_welfare`) | wic | 22.6% | full |

The "Other" line includes "payments to nonprofit welfare institutions" [SOURCE: BEA Table 3.12
footnote 11, as recorded in `../dataset_integrity_2026_09_23/spending.md` row 9]. It is where
shelter contracts would sit if BEA treats them as benefits rather than purchases. The most likely
home is mapping A or C [INFERENCE].

| Mapping | Parts sent to | Weighted key share |
|---|---|---:|
| A | welfare→income security, housing→housing, other→general public services, health→health | 12.9% |
| B | all to income security | 16.5% |
| C | as A, but welfare→"Other" social benefits | 14.5% |
| D | all to "Other" social benefits (bound) | 22.6% |

The part weights come from NYC's FY2022→FY2024 current-operations increases: welfare 26%, housing
35%, other 31%, health 7% [DATA: derived/account_keying_parts.csv].

### Charge against use (calendar 2024, $M)

Calendar-2024 outlays are $4,627 low, $4,698 central and $5,244 high [CALCULATION:
cy2024_outlays.csv]. Each row there blends fiscal years by months and keeps Massachusetts's migrant
share only. The high case adds a $500M allowance for Illinois State, Cook County Health, other
cities and border NGOs [INFERENCE].

| Mapping (central outlays) | Account charges the union | Charge by use (NYC Jun 2025, 0.63%) | Over-charge | Charge ÷ use |
|---|---:|---:|---:|---:|
| A | 534–578 | 26–28 | 508–550 | 21× |
| B | 775 | 30 | 746 | 26× |
| C | 610–654 | 26–28 | 584–626 | 23–24× |
| D (bound) | 1,064 | 30 | 1,034 | 36× |

Ranges within a row are the general-government response of 0.59–0.84. Across low–high outlays,
the four served shares (0.50%, 0.63%, 0.84% and a 2% allowance) and mappings A–C, the over-charge
runs $445–839M; with D it reaches $1,161M. Against the 2% allowance the charge is still 6.5–11
times use [CALCULATION: derived/account_keying.csv].

A cross-check replaces the part weights with NYC's FY2024 agency split: H+H 1,530 to health, DHS
1,190 to income security, HPD 413 to housing, and the other 617 to general public services. That
gives an effective key share of 10.9–11.4% and an over-charge of about $0.48–0.51bn. The
arithmetic is (1,530×0.0768 + 1,190×0.1650 + 413×0.1202 + 617×0.1202×r) / 3,750 with
r = 0.59–0.84 [CALCULATION]. The result does not depend on the weights.

**Direction and size.** The account over-charges the Mexican-origin union for migrant shelter and
emergency response. Charging by use would lower the union's main-case net cost by about $0.5bn
(central; $0.45–0.84bn for mappings A–C, at most $1.16bn). That is 0.2–0.5% of $203.2–249.6bn.
The other immigrants and natives in the account would carry the difference.

### Assumptions (stated so they can be broken)

1. The outlays are inside the national BEA totals the account keys. Federal FEMA money that reached
   border NGOs directly is not in the five jurisdictions' figures.
2. The served share is the Mexican-national share of shelter residents or exits. It adds nothing
   for US-born children of Mexican-origin parents in shelters. The NYC tables bound these: the
   whole "USA" row, which "Includes children born in United States", was 1,104 of 36,684.
3. The fiscal-year blending is linear within years. Massachusetts's migrant share is 0.40 / 0.475 /
   0.50. NYS's support payments to NYC are counted once, inside NYC.
4. The main-case responses apply unchanged: services and transfers in full, general public services
   at 0.59–0.84.

## 5. Gaps

1. **Massachusetts FY2023 and earlier.** The bi-weekly reports start with FY2024. The Special
   Commission gives appropriations (about $325M a year since FY2023 plus reserves of $20M, $40.1M
   and $7.0M in November 2022 and March 2023) but no FY2023 total.
2. **Massachusetts source route.** HD5125 (malegislature.gov) timed out over curl and is not in
   Wayback (404). The Special Commission draft (mass.gov) returned 403 to curl and 500 from Wayback.
   Both were read through Firecrawl's PDF text parser; the verbatim excerpts are kept in
   `_cache/src/`. The FY2024 $894.0M
   is consistent with the 16 Dec 2024 report's $856.8M to date (p.4). The FY2025 sum ($978.2M) is
   consistent with the projected $1.094bn (p.5). Neither was checked against a curl-fetched PDF.
3. **Illinois State and Cook County actuals by year.** Only the Nov 2023 overview (commitments,
   including federal pass-through) and the State and County money inside Chicago's payment file
   are covered. Cook County Health's migrant costs are not recovered.
4. **Denver.** General-fund spending in 2023 before the Border Crisis fund existed, the full 2024
   actual, and the peak shelter census are not recovered from primary documents. The 2024 high
   case is [SECONDARY].
5. **DC.** The federal/local split of the FY2023–FY2024 actuals and the peak census are not
   recovered.
6. **FEMA FY2024 totals.** SSP-Competitive and the FY2024 total are [UNVERIFIED]; the $640.9M
   figure in circulation was not confirmed. USAspending's $0 on FY2024 awards could reflect
   termination, withholding or reporting lag [INFERENCE].
7. **Origins at the peak (2022–2023) and in Massachusetts, Denver and DC.** Not recovered. A higher
   Mexican share in 2022–2023 would narrow the over-charge. The 2% allowance still leaves the
   account charging 6.5–11 times use.
8. **BEA treatment of shelter contracts** (purchases vs. payments to nonprofit institutions) is
   [INFERENCE]. Mappings A–D bracket it.
9. **Schooling and Medicaid for migrant children and adults** are outside these budgets. The
   account charges them through its enrollment and Medicaid keys. The direction is the same, but
   the amount is not sized here. Chicago's 11,692 newcomer pupils are one primary data point.
10. **Census attribution.** NYC's code-level mapping of agencies to functions is [INFERENCE]. Census
    publishes no crosswalk, and NYC's submission would be needed to settle whether H+H's
    humanitarian-center costs were coded to hospitals or welfare.

## Files and rerun

The lane's files are:

- `census_unit_test.py`: parts 3 and 4.
- `budget_figures.csv`: hand-entered budget rows with sources.
- `cy2024_outlays.csv`: calendar-2024 outlays with derivations.
- `derived/`, eleven outputs:
  - `census_unit_measures.csv`, `census_jump_test.csv`, `census_target_items.csv`,
    `census_repeated_values.csv`, `census_e23_by_unit.csv` and `census_vs_budget.csv`;
  - `chicago_payments_by_year_fund.csv` and `chicago_exits_by_country.csv`;
  - `account_keying.csv` and `account_keying_parts.csv`;
  - `inputs_manifest.json`, with the sha256 of the script, every input and every output.
- `_cache/src/`: raw pulls, ignored.

```sh
# from the repository root
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
  infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/census_unit_test.py
```

The script ran twice in a row on 24 Sep 2026, and `md5 -r derived/*` was identical for all eleven
outputs. The two Chicago portal exports (`_cache/src/chi_gxzc-43gg.csv`, `chi_fk7i-xuiy.csv`) are
inputs, and their hashes are in the manifest.

Model self-report: claude-opus-5-5[1m]
