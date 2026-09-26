claude-opus-5-5
**Verdict:** All four questions answered from primary documents, except that no source gives emergency Medicaid or uncompensated care per person for unauthorized people aged 65+ nationally. The usable per-person prices are state figures: about $16–17k a year for full state coverage (Illinois HBIS FY2026; LAO's California projection), about $5–7k for emergency-only coverage per enrollee or per user (California and North Carolina), and uncompensated care that scales about 1.6× with age at 55–64 in MEPS.

- **Q1 emergency Medicaid, national:** CMS-64 line 27, FY2024: **$9.12bn total ($6.15bn federal, $2.97bn state)**, of which California is 71%. CBO's FY2017–2023 series is the same line (FY2023 $3.78bn). No national age or service split exists. North Carolina 2004: **$6,940 per elderly recipient** (1.7% of spending; DuBard & Massing, Table 2). California projection: **$5.4k per enrollee-year at 65+** (LAO 4423). Coverage is everyone on restricted Medicaid because of status, not only the unauthorized. HHS-OIG's brief is still unpublished.
- **Q2 California:** the 50+ expansion peaked at **450,917 (July 2025)** and stood at **375,392 in June 2026** (CHHS/DHCS). The 50+ group includes some lawfully present people. **About 17% are 65+** (LAO, 2021-22 mix). The only DHCS cost line for the group alone is from May 2022: **$745M TF / $628M state** for FY2022-23, incremental and excluding IHSS. LAO's projection by age gives **$16.2k TF ($13.5k GF) per enrollee-year at 65+**. The freeze applies to ages **19+ with no 65+ exemption**, from **2026-01-01**. People already enrolled get a **three-month grace period** after any loss of coverage. Premiums apply to ages **19–59 only**: $30 from 2027-07-01, raised to $50 by the 2026 Budget Act.
- **Q3 2026 status:** **IL HBIS closed since 2023-11-06** (6,975 enrollees March 2026, $1,456 PMPM, 49% Mexican-origin) · **NY 65+ open** (FFS from 2027-01-01) · **OR Healthier Oregon open** (FFS 2027-01) · **WA Apple Health Expansion closed** (cap met; FFS 2027-01-01) · **DC Alliance closed to 26+ since 2025-10-01** (moratorium continued for FY2027).
- **Q4 uninsured care by age:** the named Urban/KFF studies cover only the nonelderly and have no age split. MEPS 2022–23 [CALCULATION]: full-year uninsured aged **55–64 receive 1.64×** the all-age (0–64) mean. **Foreign-born Mexicans aged 55–64 receive 1.03× that mean.** The 65+ uninsured are unmeasurable in MEPS (n = 37).

# Sources for pricing unauthorized seniors' public health costs (lineage lane)

Brief: `SENIOR_SOURCES_BRIEF.md` (same directory). Researcher: claude-opus-5-5, 2026-09-26.
Archived fetches: `_cache/` (ignored by git). Tags: `[SOURCE: …]` primary seen;
`[SECONDARY]` figure only in a summary, primary not seen; `[CALCULATION]` own arithmetic;
`[INFERENCE]` judgment.

## Repo figures read first (not re-sourced)

Read 2026-09-26 from the lanes the brief names; quoted here only so this file stands alone.

- Illinois HBIS (65+): FY2025 projected $139M for 8,931 enrollees (Feb 2025), about $15.6k per
  enrollee-year [CALCULATION: 139,000,000 / 8,931 = $15,564; enrollment is a point count, so this is
  per enrolled head at February, not per enrollee-month]. FY2024 HBIS actual $211M (auditor p5).
  `state_programs_unauthorized_2026_09_23/RESULT.md` rows IL.
- New York undocumented 65+ Medicaid: about $229M a year [INFERENCE there: $171.9M nine-month deferral
  × 12/9]. No enrollment count or dollar line in NY budget documents (same RESULT, gap 1).
- California UIS Medi-Cal: about $10.8bn GF 2025-26, all ages, including IHSS (LAO May-2025 handout
  p8; LAO Report 5083 ~$10bn GF/yr). DHCS estimate has no UIS subtotal
  (`california_program_costs_2026_09_23/RESULT.md`, `improper_payments_unauthorized_2026_09_23/RESULT.md`).
- Uncompensated care: $1,524 per uninsured person-year (the earlier lane's price, AHA 2020 $42.67bn at
  cost ÷ 28.0M full-year uninsured) and a 58–70% government offset share, VA and IHS removed
  (`uncompensated_care_2026_09_23/RESULT.md`).
- Emergency Medicaid state shares: none published outside California; HHS-OIG data brief
  OAS-26-01-061 on emergency services for "nonqualified aliens" opened 2026-03-16 (state programs
  RESULT §3, gap 8). This file re-checks whether it has since been published.

## Q1. Emergency Medicaid, national

### 1a. National totals (CMS-64 line 27, "Emergency Services for Undocumented Aliens")

**FY2024, the latest published year: $9,118.1M total computable, $6,145.9M federal, $2,972.2M
state.** California alone is $6,481.7M (71%). [SOURCE: CMS, *Financial Management Report FY 2024,
Net Expenditures* workbook (file dated 2025-07-30), sheet "MAP - National Totals", row "Emergency
Services for Undocumented Aliens": 9,118,148,687 total computable, 6,145,943,159 federal share;
`_cache/cms_fmr_fy2024.zip` fetched via Wayback capture 2025-10-02 of
https://www.medicaid.gov/medicaid/financial-management/downloads/financial-management-report-fy2024.zip
(medicaid.gov returns a bot page to curl); state = total − federal [CALCULATION]; per-state table
`_cache/cms64_line27_emergency_fy2023_fy2024.csv`]

**FY2017–2023 series** (CBO letter to Chairman Arrington, 2024-10-02, Table 1, $M): "2023 2,746
1,029 3,775 73" (federal, state, total, average federal share %); 2022 5,401; 2021 7,050; 2020 3,076;
2019 3,110; 2018 2,607; 2017 1,535; "Total 18,038 8,516 26,554". Text: "from 2017 to 2023, the
federal government spent about $18 billion and state governments spent about $9 billion on emergency
Medicaid services for non‑U.S. nationals who were ineligible for comprehensive Medicaid by reason of
immigration status or because they were still within the five-year waiting period". [SOURCE:
https://www.cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf,
p1–2, Table 1; `_cache/cbo_arrington_emergency_medicaid_2024-10-02.pdf` via Wayback 20241003,
sha256 dfe19719…] CBO's FY2023 row equals the FMR FY2023 line 27 to the dollar-million
(3,774,627,718 total; 2,745,761,291 federal) [DATA: `_cache/cms_fmr_fy2023.zip`], so the CBO series
*is* this line.

**Population covered.** CBO p3: "Based on the available data, CBO cannot distinguish how much of the
total spending is attributable to" qualified aliens in the five-year wait, parolees in the wait, or
"non-U.S. nationals who are lawfully present on a temporary basis, or non-U.S. nationals who are in
the country illegally." So the line covers everyone on restricted (emergency-only) Medicaid because
of immigration status, not only the unauthorized. [SOURCE: CBO letter p3]

**Reading the FY2024 jump.** Line 27 is net of prior-period adjustments reported in the year, and
states differ in what they book there. California rose from $1,678M (FY2023) to $6,482M (FY2024),
Illinois from $28M to $452M and Pennsylvania from $0 to $165M, while most states moved little
[DATA: the per-state CSV]. So the FY2024 national total mixes a claiming change or catch-up with
service volume [INFERENCE; no CMS note seen explaining it]. CMS's 2025-09-30 State Medicaid Director
letter tells states to report emergency services "on line 27 on the Form CMS-64 entitled 'Emergency
Services for Undocumented Aliens'" and ends federal match for capitation payments on behalf of these
enrollees from rating periods starting a year after publication (e.g. 2027-01-01) [SOURCE: CMS SMDL
2025-09-30, "Medicaid Managed Care and Emergency Medicaid", as reposted by Utah DHHS,
https://dhhs.stage.utah.gov/wp-content/uploads/Managed-Care-Payments-EM-Condition-Coverages-for-Ineligible-Aliens.pdf,
text seen via Exa search highlights only, PDF not archived — `[SECONDARY]` for the date and
enforcement timing]. The sister improper-payments lane records California returning $1,108.2M of
federal claims in 2025-26, which may reverse part of FY2024 [INFERENCE linking the two; not verified
against a CMS-64 revision].

[GAP] CMS-64 carries no age, service or enrollee count, so per-enrollee cost and any 65+ share
must come from claims studies (1b below).

### 1b. Age and service breakdowns (none national; three state sources)

**No national age or service split exists in CMS-64, CBO, KFF, MACPAC or HHS-OIG.** HHS-OIG's data
brief OAS-26-01-061 ("We will describe which types of services were covered as Medicaid emergency
medical services for nonqualified aliens in selected States") is still "Status Active", announced and
last modified 2026-03-16 — not published as of 2026-09-26. [SOURCE: oig.hhs.gov work-plan page, via Exa
search] The 2025 JAMA research letter (Santos, Chalmers, Chino, Cervantes, Sommers, doi
10.1001/jama.2025.18709) works from the same CMS-64 series by state; press summaries report "0.4% of
total Medicaid spending in both 2022 and 2023" and "$9.63 per resident in 2022" [SECONDARY: letter not
read; PMC/OAI gave no full text].

**North Carolina 2001–2004, the only claims study with an elderly row** (DuBard & Massing, *JAMA*
2007;297(10):1085–1092, doi 10.1001/jama.297.10.1085, Table 2, "Emergency Medicaid Use and Spending
by Eligibility Category, 2001 Through 2004"; read from the jamanetwork.com full-text HTML via Firecrawl,
the PDF is blocked to curl):

| NC Emergency Medicaid, 2004 | Recipients | Spending per recipient, mean (SE) | Median | Total | Share of EM spending |
|---|---:|---:|---:|---:|---:|
| Elderly | 133 | $6,940 (871) | $3,603 | $923,073 | 1.7% |
| Disabled | 233 | $13,856 (1,181) | $8,050 | $3,228,440 | 6.1% |
| Pregnant women | 14,008 | $3,106 (13) | $2,993 | $43,515,222 | 82.2% |

Elderly 2001: 89 recipients, $5,248 mean, $467,113 total. Over 2001–2004, 380 of 48,391 recipients
(0.8%) were 65+ at first service (Table 1). Abstract: "The patient population was 99% undocumented,
93% Hispanic"; "more rapid spending increases among elderly (98%)"; "In 2004, childbirth and
complications of pregnancy accounted for 82% of spending". Arithmetic check [CALCULATION]: 133 × $6,940
= $923,020 against the printed $923,073; pregnant-women total ÷ 0.822 = $52.9M, the abstract's 2004
total. Caveat: "per recipient" means per person with a paid claim that year, not per eligible person;
nominal 2004 dollars; one state.

**California restricted scope by age (LAO projection, 2021-22 costs):** restricted-scope (emergency and
pregnancy) Medi-Cal for undocumented people 65+ ≈ **$200M TF ($100M GF) for 37,000 enrollees ≈ $5.4k
TF per enrollee-year** (50–64: $520M for 198,000 ≈ $2.6k) [SOURCE: LAO Report 4423, Figure 3;
CALCULATION; see 2b]. Per enrollee, not per user. California's restricted scope also covers
nursing-facility care (county guidance quoted in 2c), which may inflate the 65+ figure relative to
other states [INFERENCE].

**Mississippi (service mix):** "roughly 95% of Medicaid spending on illegal immigrants in Mississippi on
medical services provided from July 2022 to June 2025 was attributed to childbirth"; Mississippi had
reported $0 on line 27 through FFY2024 while spending about $10.5M over FFY2023–2025. [SOURCE: Office
of the State Auditor of Mississippi, *Analyzing the Cost of Medicaid Services for Illegal Immigrants*,
https://www.osa.ms.gov/sites/default/files/osa/files/reports/25Analyzing%20the%20Cost%20of%20Medicaid%20Services%20for%20Illegal%20Immigrants.pdf,
text via Exa search highlights; PDF not archived here]

**New York (per enrollee, all ages):** "As of March 2024, sign-ups for emergency Medicaid stood at
480,000"; "Spending on emergency Medicaid has roughly tripled, from $207 million in fiscal 2013-14 to
$639 million in fiscal 2023-24 ... the share of enrollees who used services in any given year has
dropped from 43 percent to 21 percent, and the annual cost per enrollee has declined from $5,700 to
$1,300, officials said." [SECONDARY: Empire Center, Bill Hammond, 2025-02-19, citing "newly released
state records"; the state records were not seen.] Since 2024-01-01 New York's 65+ are in full
Medicaid, so this is effectively an under-65 figure.

**Dialysis (Colorado):** "Emergency dialysis was costing the state Medicaid department $20,291 per
month per person, according to a Department of Health Care Policy and Financing analysis. That's based
on March 2017-June 2018 Medicaid claims from hospitals that treated 137 immigrants here illegally."
[SECONDARY: Colorado Sun, 2019-02-25; HCPF analysis not seen]

**What this means for pricing [INFERENCE]:** the national line is not age-split. A 65+ unauthorized
person on emergency-only coverage costs roughly $5–7k a year *per user or enrollee* in the two sources
with an older-age row (NC 2004 $6.9k per user, nominal; CA $5.4k per enrollee projected for 2021-22,
including nursing-home care). Neither is per resident: take-up of emergency Medicaid among eligible
seniors is not measured anywhere found.

## Q2. California older adults

### 2a. Enrollment in the Older Adult Expansion (50+)

**Statewide 50+ expansion enrollment: 240,548 (May 2022, first month) → peak 450,917 (July 2025) →
442,218 (Dec 2025) → 375,392 (June 2026, latest), falling about 10–12k a month since the freeze
took effect in January 2026.** [SOURCE: DHCS via CalHHS Open Data, *Medi-Cal Adult Full Scope
Expansion Programs*, resource "Older AE (50 and over) Population (by County)", file
`oae-06-2026-suprsd-data_odp.csv`, resource last modified 2026-09-11, rows County = "Statewide";
`_cache/chhs_oae_50plus_06-2026.csv`. Note: the file also carries a "Statewide" row, so summing
counties double counts.] LAO confirms the level: "As of October 2025, the 50 and older Medi-Cal
expansion population included about 444,000 individuals, considerably higher than originally projected
for this population" [SOURCE: LAO Report 5126 (CFAP expansion), read from
`california_program_costs_2026_09_23/_cache/lao_5126.txt`; CHHS October 2025: 444,225]. Population covered, per the dataset description: "the monthly count of
individuals 50 years of age or older ... receiving full scope Medi-Cal benefits ... regardless of
immigration status. Lawfully present individuals 50 years of age or older, who are not in a pregnancy
aid code, are included in this count." So the count is UIS plus some lawfully present people without
federal full-scope eligibility; it is not purely unauthorized. [SOURCE: dataset page
https://data.chhs.ca.gov/dataset/medi-cal-adult-expansion]

**No published 65+ split of this count found.** The only age split is LAO's: "Based on data on the
restricted scope population prior to the expansions to adults and older adults, 17 percent of the
individuals in the older adult expansion were aged 65 and older in 2021-22." [SOURCE: LAO, *The
2025-26 Budget: Understanding Recent Increases in the Medi-Cal Senior Caseload*, Report 5010,
2025-03-06, p9; `_cache/lao_5010_senior_caseload_2025-03.pdf`] At 17%, the 65+ part of the
expansion was about 77k at the July 2025 peak and 64k in June 2026 [CALCULATION: 450,917 × 0.17;
375,392 × 0.17 — applies a 2021-22 age mix to later enrollment, INFERENCE]. LAO 5010 put the expansion's
contribution to *senior* caseload growth at about 23,000 as of January 2025 (Figure 13), i.e.
restricted-scope 65+ enrollees converted to full scope are not all "new" seniors.

### 2b. Cost of the 50+ expansion, total funds and General Fund

**No actual DHCS cost for the 50+ expansion alone found in the current estimates**: the November
2025 Local Assistance Estimate has no UIS subtotal and no 50+ policy change (the sister lane found the
same; `california_program_costs_2026_09_23/_cache/N25.txt` has only the freeze, dental, premiums and
H.R. 1 FMAP policy changes). The May 2023 estimate has no separate 50+ policy change either: the
expansion was already in the managed-care base ("the inclusion of the full-scope expansion to adults
ages 50 and older", p16) [SOURCE: DHCS *May 2023 Medi-Cal Estimate*, `_cache/dhcs_M23_medi-cal_la_estimate.pdf`,
1,261 pp, via Wayback 20250302]. Its only aggregate: "the May Revision includes increases for the two
most recent expansions for adults 50 and older and ages 26-49 of $1.6 billion General Fund in FY
2023-24 and an estimated $2.4 billion General Fund annually compared to the Governor's Budget."

**The only DHCS dollar line for the 50+ expansion alone is the original May 2022 policy change**
(PC 4, "Undocumented Older Californians Expansion", fiscal reference 2294, implementation 5/2022):
"FY 2022-23 ... FULL YEAR COST - TOTAL FUNDS $745,180,000 - STATE FUNDS $628,052,500 ... FEDERAL FUNDS
$117,127,500"; FY 2021-22 (two months) $67.2M TF / $53.2M state. Methodology: "In-Home Supportive
Services are not budgeted in this policy change"; "Assume offsetting cost savings for current
restricted-scope Medi-Cal expenditures". So $745M is the *incremental* cost of full scope over
restricted scope for all ages 50+, before IHSS, for the first full year. [SOURCE: DHCS *May 2022 Medi-Cal
Estimate*, PC pp14–16; `_cache/dhcs_M22_medi-cal_la_estimate.pdf`, 1,288 pp, via Wayback 20250121]
At the FY2022-23 average enrollment of about 326k (CHHS series, July 2022–June 2023 average
[CALCULATION: 3,911,613 member-months ÷ 12]), that is about $2.3k TF / $1.9k GF per enrollee-year incremental, all ages
50+, first year [CALCULATION; INFERENCE because the PC's own caseload is not printed].

**Age-specific per-enrollee costs exist only as LAO's pre-expansion projection** (LAO, *Estimated Cost
of Expanding Full-Scope Medi-Cal Coverage to All Otherwise-Eligible Californians Regardless of
Immigration Status*, 2021-05-05, https://lao.ca.gov/Publications/Report/4423, Figures 1 and 3,
"ongoing", 2021-22 service-cost levels; read from `california_program_costs_2026_09_23/_cache/lao_4423.html`):

| Ages | Ongoing caseload | Full-scope cost TF / GF ($M) | Restricted-scope cost TF / GF ($M) | Added cost TF / GF ($M) |
|---|---:|---:|---:|---:|
| 50–64 | 198,000 | 820 / 510 | 520 / 150 | 300 / 370 |
| 65+ | 37,000 | 600 / 500 | 200 / 100 | 400 / 400 |

Verbatim row: "Ages 65+ | 600 | 500 | 200 | 100 | 400 | 400". Restricted-scope = "Estimated costs for
emergency‑ and pregnancy‑related services that otherwise would be incurred". Full-scope includes IHSS
("IHSS costs account for about 20 percent of the estimated additional costs"; "undocumented immigrants
65 and older would have similar per-enrollee IHSS costs to current senior enrollees").

Per enrollee-year at 65+ [CALCULATION, dividing LAO's rounded $M by 37,000]: full scope **$16.2k TF
($13.5k GF)**; restricted scope (emergency + pregnancy, i.e. emergency Medicaid) **$5.4k TF ($2.7k
GF)**; added state cost of full scope **$10.8k GF**. At 50–64: full scope $4.1k TF, restricted
$2.6k TF. These are 2021-22 projections, rounded to $10M, and LAO later said the expansions cost
"more than originally estimated due to a combination of higher caseload and per-enrollee costs"
(Report 5010 p11). LAO 5010 p11 also gives $12,533 total funds per enrollee-year for the Medically
Needy senior aid category, which holds the asset-test and expansion growth (not UIS-specific).

### 2c. The 2025 Budget Act freeze and premiums (and 2026 amendments)

**Freeze: ages 19 and over, no exemption for 65+, from 2026-01-01.**
- DHCS: "The Budget adopts a freeze on new enrollment to full scope state-only coverage for otherwise
  eligible undocumented individuals, aged 19 and over ... The enrollment freeze does not apply to
  Qualified Non-Citizens ... under the five-year bar, individuals claiming Permanently Residing Under
  Color of Law, and pregnant individuals. The policy is effective January 1, 2026. Estimated General
  Fund savings are $77.9 million in 2025-26, increasing to $3.3 billion by 2028-29." [SOURCE: DHCS,
  *FY 2025-26 Budget Act Highlights*, p4; `california_program_costs_2026_09_23/_cache/DHCS-FY-2025-26-Budget-Act-Highlights.pdf`]
- November 2025 estimate, PC 2530: the freeze covers "the previous young adult expansion (19-25),
  26-49 expansion, or 50+ expansion ... for individuals aged 19 and older ... No sooner than January 1,
  2026, individuals aged 19 or older, including those previously enrolled, seeking to obtain full-scope
  coverage under these previous expansions will not be enrolled in full-scope coverage, but may
  receive restricted scope (emergency and pregnancy) services." Authority "AB 116 (Chapter 21,
  Statutes of 2025)". Savings −$94.7M TF / −$83.4M GF (2025-26), −$865.5M TF / −$742.5M GF (2026-27);
  "approximately 15,000 individuals that otherwise would have been enrolled in full-scope coverage each
  month will not be enrolled". [SOURCE: DHCS, *November 2025 Medi-Cal Local Assistance Estimate*, PC
  pp32–33; `california_program_costs_2026_09_23/_cache/N25.txt` lines 15163–15235]
- **Grace period for people already enrolled: three months, any discontinuance reason.** DHCS MEDIL
  I 25-27 (2025-10-30), Q&A 9: "Adult Expansion members, who were enrolled in full scope prior to
  January 1, 2026, who experience a discontinuance will have a three-month grace period to re
  establish eligibility and re-enroll in full scope Medi-Cal ... This grace period is available only to
  the Adult Expansion Freeze population and is not limited to specific discontinuance reasons." Q&A 1–2,
  4: applies to people 19+ who are not pregnant with "No immigration status", "Unverified immigration
  status" or "Certain non-immigrant visa holders". Q&A 14: new restricted-scope applicants aged 19+
  "will be ineligible for HCBS Waivers". [SOURCE:
  https://www.dhcs.ca.gov/wp-content/uploads/2025/12/I25-27.pdf, text via Exa crawl 2026-09-26;
  dhcs.ca.gov returns 403 to curl and Wayback has no capture; `[SECONDARY]` as to page layout only]
- Statute summary: AB 116 "Provides a three-month reenrollment period for an individual with UIS who
  is 19 years of age or older, enrolled in full-scope Medi-Cal and not pregnant, and loses full-scope
  Medi-Cal coverage"; people losing full scope while pregnant keep it through pregnancy plus 12 months
  (WIC 14007.65; 14007.8). [SECONDARY: CHEAC summary of AB 116,
  https://cheac.org/wp-content/uploads/2025/06/Health-TBL-Summary-AB-116.pdf; statute text itself not read]
- Restricted scope after the freeze still covers emergencies, pregnancy and nursing-home care: county
  guidance lists "emergency care, pregnancy-related care, or nursing home care" [SECONDARY: San Diego
  County HHSA Medi-Cal page]; DHCS MEDIL Q&A 8: "Restricted scope Medi-Cal will cover emergency-related
  dialysis only."
- LAO: "Beginning in January 2026, eligibility for comprehensive coverage for undocumented adults and
  seniors will be frozen. (Eligibility for children—those under 19 years old—will remain open for new
  enrollment.)" [SOURCE: LAO Report 5083, 2025-10-24, read from `california_program_costs_2026_09_23/_cache/lao_5083.txt`]
- Discrepancy: Health Access (2025-07-23) describes the freeze as "Undocumented adults age 19–64"
  [SOURCE: health-access.org PDF]. DHCS documents say 19 and older with no upper bound; I follow DHCS.
- Observed effect on the 50+ group: statewide 50+ enrollment fell from 442,218 (Dec 2025) to 375,392
  (June 2026), −15% in six months (2a above) [CALCULATION].

**Premiums: $30 a month, ages 19–59 only, from 2027-07-01; raised to $50 by the 2026 Budget Act.**
People aged 60+ pay none. DHCS 2025-26 Budget Act Highlights p4: "$30 monthly premiums for individuals
with UIS aged 19 through 59, effective July 1, 2027. Estimated General Fund savings are $695.7 million
in 2027-28." DHCS *FY 2026-27 Budget Act Highlights* ("Final 7.20.26") p5: "Increase Monthly Premium
for Adults with Unsatisfactory Immigration Status (Aged 19–59) from $30 to $50 ... effective July 1,
2027, subject to a determination in the 2027-28 May Revision." [SOURCE: both PDFs in
`california_program_costs_2026_09_23/_cache/`]

**Other 2026 Budget Act items that change what a UIS senior costs** (same 2026-27 highlights, p4–5):
- H.R. 1 FMAP: "$669 million General Fund cost ... due to the federal match reduction from 90 percent to
  50 percent for emergency services for Affordable Care Act adult expansion population members with
  unsatisfactory immigration status effective October 1, 2026" (ACA expansion adults are 19–64, so
  seniors' emergency services were already at the regular 50% match) [INFERENCE on the age scope].
- "Transition of Unsatisfactory Immigration Status (UIS) Members to Fee-for-Service": −$637.1M
  ($524.9M GF) in 2026-27 and −$1.6bn ($1.3bn GF) ongoing "due to discontinuing federal funded coverage
  of Medicaid emergency services for members with unsatisfactory immigration status through the
  managed care delivery system" — California's response to CMS's 2025-09-30 letter (1a).
- Dental elimination for UIS adults 19+ delayed from 2026-07-01 to 2027-07-01; PPS clinic-rate
  elimination delayed to 2027-07-01.

## Q3. Enrollment status in 2026

### Illinois HBIS (65+): open to renewals, **closed to new enrollees since 2023-11-06**

- "New enrollment for the HBIS program was suspended for applications dated after November 6, 2023, at
  5 p.m. due to having met an enrollment cap" and "remains paused at this time". [SOURCE: IDHS Manual
  Release #24.12, https://www.dhs.state.il.us/page.aspx?item=161600, text via Exa search; also IDHS PM
  06-36-00; Illinois Auditor General performance audit 2025, p4 of the digest section: "HBIS program
  was paused effective November 6, 2023. Individuals already enrolled in the programs remained eligible"]
- HFS program page (2026): "the Health Benefits for Immigrant Seniors program will continue to operate
  and provide coverage for enrollees aged 65 and over ... do not submit applications for this program,
  enrollment is currently paused". HFS FAQ: "HFS' FY26 budget proposal does not include reopening
  enrollment into the HBIS program." [SOURCE: hfs.illinois.gov HBIS page and HBIA FAQ, text via Exa]
- Illinois Legal Aid Online, reviewed 2026-01-19: "As of November 2025, people who were enrolled before
  November 6, 2023 can still receive and renew their HBIS benefits." [SECONDARY]
- **Current enrollment and cost (use this over the FY2025 projection the repo holds):** HFS *HBIS
  Tracking Report for March 2026* (PDF created 2026-05-12): enrollment "8,271" (July 2025) falling to
  "6,975" (March 2026); monthly liability "$10.5 ... $9.9" million; "65+ $1,456" estimated PMPM
  (managed-care rate), "Mar FFS Enrollment 419", "MCO Enrollment 6,556", July–March liability "$89",
  April–June projected "$30", "Total Proj. Costs $119" ($M, FY2026). Ethnicity of the 6,975:
  "Mexican, Mexican American, Chicano/a 3,448", "Another Hispanic, Latino, or Spanish origin 990",
  "Non-Hispanic/Latino 1,093". [SOURCE: https://hfs.illinois.gov/content/dam/soi/en/web/hfs/info/reports/hbia/062026hbis.pdf,
  pp1 and 3; `_cache/il_hfs_hbis_tracking_2026-03.pdf`]
  - Per enrollee-year [CALCULATION]: PMPM × 12 = **$17,472**; liability basis $89M ÷ (7,477 average
    enrollment × 9 months) = $1,323 a month = **$15.9k a year**; FY2025 basis $132M (same report p2,
    HBIS cumulative June 2025) ÷ 9,253 average FY2025 enrollment (111,031 member-months) = $14.3k;
    FY2025 liability is booked by claim-approval month, FY2026 by date of service, so the two are not
    strictly comparable. Share Mexican-origin: 3,448 / 6,975 = 49.4%.
  - Population: undocumented and other noncitizens 65+ not eligible for Medicaid; lawful permanent
    residents were moved out during the 2024 redeterminations (auditor, quoted in the state-programs lane).

### New York, undocumented 65+ Medicaid: **open to new enrollees in 2026**; moves to fee-for-service 2027-01-01

- Law: NY Social Services Law §366(1)(g)(4)(a): "Applicants and recipients who are age sixty-five or
  older, who are otherwise eligible for medical assistance under this section, but for their
  immigration status, are eligible for medical assistance". The SFY2027 budget (April 2026) amended
  clause (b), effective 2027-01-01, so these enrollees "shall receive the equivalent of the covered
  benefits available through a managed care provider ... through the fee-for-service program". No
  freeze or sunset in the quoted text. [SECONDARY: NY Health Access, *Medicaid for Undocumented
  Immigrants Age 65+*, https://nyhealthaccess.org/entry/251/, last updated 2026-08-21, quoting the
  statute; `_cache/nyha_entry251.html`. The enacted Article VII bill itself was not read.]
- Enrollment: "As of Jan. 22, 2024, DOH reported that 16,000 undocumented adults age 65+ already are
  receiving full Medicaid. 24,000 are expected to qualify." [SECONDARY: same page, citing a DOH webinar
  of 2024-01-30; the DOH slides were not read.] No later count and no dollar line found; the repo's
  $229M/yr inference stands. At 16,000–24,000 enrollees that would be $9.5k–14.3k per enrollee-year
  [CALCULATION on an INFERENCE; weak].
- KFF, as of April 2026: "New York state-funded coverage is limited to adults ages 65 and older", shown
  outside the "Limited or Closed Enrollment" group. [SECONDARY: KFF, *State Health Coverage for
  Immigrants and Implications for Health Coverage and Care*, published 2026-05-19, updated 2026-06-11]

### Oregon, Healthier Oregon (all ages): **open in 2026**; moves to fee-for-service ("Open Card") 2027-01

- OHA: "Members who have OHP through Healthier Oregon will move to OHP Open Card in January 2027 ...
  This affects adults with statuses including nonimmigrant visas, refugee or asylum statuses, most
  adults with permanent resident status for less than 5 years, and adults and children who do not have
  an immigration status that qualifies for other OHP programs." "In October 2026, about 7,000 OHP
  members will move to Healthier Oregon." No enrollment pause or cap on the program pages (checked
  2026-09-26). [SOURCE: https://www.oregon.gov/oha/hsd/ohp/pages/federal-changes.aspx and
  .../healthier-oregon.aspx; `_cache/or_oha_federal_changes.html`, `_cache/or_oha_healthier_oregon.html`]
- Enrollment: "about 95,000" (Nov 2024) [SOURCE: OHA *Progress Report: Healthier Oregon (July
  2022–present)*, le-817750.pdf, via Firecrawl PDF parse]; peak "107,000 people in June" 2025, then
  falling [SECONDARY: Oregon Capital Chronicle 2026-01-28, citing OHA data]. HOP enrollment includes
  lawfully present people. No age split found.
- KFF (April 2026) lists Oregon among states covering adults regardless of status, not among those
  with limited or closed enrollment [SECONDARY].

### Washington, Apple Health Expansion (19+ incl. 65+): **closed**; moves to fee-for-service 2027-01-01

- HCA: "Apple Health Expansion enrollment update - December 2025 ... Enrollment for Apple Health
  Expansion is currently closed. Apple Health Expansion is one of the few Apple Health programs with
  limited enrollment. At this time, the enrollment limit has been met and the state is not opening new
  enrollment into the program." "Starting January 1, 2027, Apple Health Expansion is moving from
  coverage with managed care to coverage without managed care (also known as fee-for-service)."
  [SOURCE: https://www.hca.wa.gov/free-or-low-cost-health-care/i-need-medical-dental-or-vision-care/apple-health-expansion,
  fetched 2026-09-26; `_cache/wa_hca_ahe_page.html`] The cap was reached soon after the July 2024
  launch: 11,936 enrolled in July 2024, including 692 aged 65+ (HCA 2024-07-18 deck, in the state-programs lane).
- Closed since: the page dates the notice to December 2025; the enrollment limit was met in 2024
  [INFERENCE from the July 2024 count against the ~$70M/FY budget; exact closing date not found].

### DC Health Care Alliance (21+): **closed to new enrollees aged 26+ since 2025-10-01**

- DHCF oversight testimony 2026-01-29: "Alliance enrollment was frozen for adults 26 and older,
  beginning October 1, 2025"; FY2026 eligibility cut to 138% FPL; "The scope of covered services was
  reduced for adults to exclude long-term care benefits, non-emergency transportation, cosmetic
  medication and organ transplants"; program moved to fee-for-service. The same deck listed a FY2027
  cut to 24% FPL and a freeze for all new applicants over 21. [SOURCE:
  `state_programs_unauthorized_2026_09_23/_cache/dc_dhcf_perf_testimony_2026-01-29.pdf`, Alliance slide]
- DHCF Medicaid Advisory Committee, April 2026 (FY2027 proposed budget): "Maintains FY26 income
  eligibility levels in FY27 (138% FPL for age 21 and older ...)"; "Continues the current law
  moratorium on new enrollment in Alliance adult coverage — Moratorium applies to individuals age 21+
  who seek to newly enroll in FY27"; people under the moratorium "remain eligible for coverage of
  emergency medical conditions under Medicaid". [SOURCE: `.../_cache/dc_dhcf_mac_april_fy26.pdf` p25]
- KFF (April 2026): "DC closed enrollment to adults ages 26 and older and reduced income limits for
  adults 21 and older starting October 2025. DC plans to end coverage for all adults ages 21 and older
  by October 2027." [SECONDARY] [GAP] The enacted FY2027 Budget Support Act was not read, so whether
  the October 2027 end stands is unverified. No 65+ enrollment count found (FY2026 Alliance average
  22,721 all ages, $121M).

### Summary for a 65+ unauthorized person in 2026

| Program | New 65+ applicants in 2026 | Since | People already enrolled |
|---|---|---|---|
| California 50+ expansion | closed (restricted scope only) | 2026-01-01 | keep full scope if they renew; 3-month grace |
| Illinois HBIS | closed | 2023-11-06 | keep if they renew |
| New York 65+ Medicaid | open | 2024-01-01 start | FFS from 2027-01-01 |
| Oregon Healthier Oregon | open | 2023-07-01 all ages | FFS from 2027-01 |
| Washington Apple Health Expansion | closed | limit met 2024; notice Dec 2025 | FFS from 2027-01-01 |
| DC Alliance | closed for 26+ | 2025-10-01 | keep if they renew; LTC excluded |

## Q4. Care received by uninsured seniors, by age

### 4a. The named literature has no age split

- KFF/Urban 2014 (*Uncompensated Care for the Uninsured in 2013: A Detailed Examination*; the report
  behind Coughlin, Holahan, Caswell & McGrath, *Health Affairs* 2014): nonelderly only — "we limit our
  analysis sample to respondents aged 0 to 64" (methods note 7). Per person, full-year uninsured:
  "$2,443" total care, of which "$1,702 per year, or 70% of their total annual expenses) is
  'uncompensated'", "$500 out-of-pocket", "$240" other public (projected 2013$, MEPS 2008–2010 pooled,
  Table 1). No age breakdown in the text or tables. [SOURCE:
  https://www.kff.org/uninsured/report/uncompensated-care-for-the-uninsured-in-2013-a-detailed-examination/,
  read via Firecrawl 2026-09-26]
- KFF/Urban 2021 (*Sources of Payment for Uncompensated Care for the Uninsured*, 2021-04-06): totals
  only ("$42.4 billion per year in the 2015-2017", "$33.6 billion in public funds ... in 2017"); no per
  person or age figures. [SOURCE: KFF page, read via Firecrawl 2026-09-26]
- So there is no published uncompensated-care-per-uninsured-person figure for 65+ or 55–64. The 65+
  uninsured are too few in household surveys to measure (below).

### 4b. MEPS 2022–2023: care received by the full-year uninsured, by age [CALCULATION]

Full-year uninsured (INSCOVyy = 3), MEPS-HC 2022 (HC-243) and 2023 (HC-251) pooled, person weights
halved, Taylor SEs. Expenditure is MEPS "total health care exp" (payments from all sources, not
charges), so it understates free care the provider never billed; use the **ratios**, not the levels.
[DATA: `_cache/meps/h243.dta`, `_cache/meps/h251.dta` from https://meps.ahrq.gov/data_files/pufs/;
script `_cache/meps_uninsured_by_age.py`; output `_cache/meps_uninsured_by_age_2022_2023.csv`]

| Full-year uninsured | Ages | n | Mean payments $ (SE) | Out-of-pocket $ | Ratio to all uninsured 0–64 |
|---|---|---:|---:|---:|---:|
| all | 0–64 | 2,600 | 1,201 (128) | 549 | 1.00 |
| all | 19–44 | 1,395 | 848 (111) | 485 | 0.71 |
| all | 45–54 | 512 | 1,581 (142) | 579 | 1.32 |
| all | **55–64** | 453 | **1,974 (244)** | 766 | **1.64** |
| all | 65+ | 37 | 962 (SE not estimable) | 371 | 0.80 — too few to use |
| foreign-born Mexican | 0–64 | 696 | 793 (79) | 286 | 0.66 |
| foreign-born Mexican | 45–54 | 204 | 905 (160) | 269 | 0.75 |
| foreign-born Mexican | **55–64** | 129 | **1,243 (174)** | 368 | **1.03** |
| foreign-born Mexican | 65+ | 12 | 876 | 843 | too few to use |

Reading [INFERENCE]: among the uninsured, people aged 55–64 receive about 1.6 times the all-age
(0–64) average; foreign-born Mexican uninsured aged 55–64 receive about the all-age average (1.03×),
which is 1.57× their own group's 0–64 mean. If uncompensated care scales with care received, the
repo's $1,524 per uninsured person-year would become about $2,500 at 55–64 on the all-uninsured
gradient, or about $1,570 for a foreign-born Mexican uninsured person of 55–64 [CALCULATION: 1,524 ×
1.64; 1,524 × 1.03]. Care needs rise past 65, so these understate 65+ [INFERENCE]; no source measures
the uninsured 65+ directly (MEPS n = 37). Payments to the uninsured exclude hospital charity write-offs,
so the ratio assumes the uncompensated share does not vary by age [INFERENCE, untested].

## Gaps

1. [GAP] National emergency Medicaid by age or service: none published. Next: HHS-OIG OAS-26-01-061
   when released; T-MSIS TAF (restricted-benefits code 2 = alien status) by age would answer it directly
   but needs a CMS DUA.
2. [GAP] Take-up of emergency Medicaid among eligible unauthorized seniors (the per-resident
   denominator): not measured anywhere found.
3. [GAP] California actual cost for the 50+ (or 65+) group since FY2022-23: DHCS folds it into the base
   and publishes no UIS subtotal; the May 2022 policy change is the last separate line.
4. [GAP] California 65+ count inside the 50+ expansion: only LAO's 2021-22 17% share.
5. [GAP] New York 65+ enrollment after January 2024 and dollars: only DOH's 16,000 (2024-01-22) via
   NY Health Access; DOH webinar slides and the enacted SFY2027 Article VII text not read.
6. [GAP] DC FY2027 enacted Budget Support Act (whether adult Alliance ends October 2027); Washington's
   exact enrollment-closing date.
7. [GAP] Uncompensated care for uninsured 65+: no survey has enough cases; the MEPS 55–64 ratio is the
   closest measured point.

## Search log

- CMS FMR FY2023/FY2024 zips: medicaid.gov bot page → Wayback `id_` (CDX `medicaid.gov/medicaid/financial-management/downloads/*`) worked; FY2025 FMR not yet posted (403 direct, no capture).
- CBO letter: cbo.gov bot page to curl → Wayback capture 20241003 `id_`.
- DHCS estimates: Wayback `id_` works but big PDFs reset mid-transfer; `curl -C -` resume loop completed M23 (29MB) and M22 (19MB). DHCS MEDIL PDF: 403, no capture, agent-browser timed out → Exa crawl text.
- CalHHS Open Data: CKAN `package_show` + `curl -L` (S3 redirect); the county CSVs carry a "Statewide" row.
- JAMA DuBard & Massing: PDF blocked; Firecrawl `query` directQuote on the full-text HTML returned Table 1–2 rows; checked by count × mean = total.
- Illinois HFS PDFs curl directly. hca.wa.gov and oregon.gov curl directly. KFF pages read via Firecrawl query mode.
- Exa `web_search_exa` reset (ECONNRESET) twice mid-session; Firecrawl search worked as fallback.
- MEPS HC-243/HC-251 .dta zips curl directly from meps.ahrq.gov/data_files/pufs/ (5–6MB each).
- Searched without result for a national 65+ emergency Medicaid figure: Exa (T-MSIS restricted benefits by age; emergency Medicaid 65+ spending), Firecrawl (MACPAC emergency Medicaid brief; MACStats Feb 2026), KFF, CBO, HHS-OIG work plan.
