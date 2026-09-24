claude-opus-5-5[1m]

**Verdict:** Outside distributions corroborate most of the account's shares that they can reach
and contradict two keys by more than $2bn a year: the CPS federal income tax key and the raw EITC
key. CBO's 2022 distribution puts 36% of income tax before refundable credits on the top 1%, where
the key puts 19%, which adds **+$13.2–14.1bn** of cost (SE 3.5–3.7; audit row 3 already takes
+$9.5–9.6bn), and Treasury's tax-return model gives Hispanic families **28% of the EITC against the
key's 38%**, −$4.3–4.6bn, which the audit's SSN rule already removes. With CBO's smaller gaps on
payroll, excise, Social Security, Medicare, SNAP, SSI and other transfers (each within $2.1bn), the
adopted main case would move **+$5.1–6.0bn to $209.2–254.8bn** and the audit package by less than
$1bn. The income-tax result holds on CBO's 2018 and 2019 data (+$12.1–14.6bn) but assumes the
union's position inside each income group is right. Medicaid's missing income gradient
corroborates the pooled-MEPS Medicaid line rather than adding to it, while the unauthorized-tax
anchors (models sharing the audit's compliance input) and the Florida and Texas hospital reports
(−$1.0bn to +$0.1bn on uncompensated care, at face value) bracket the account without settling it.
[CALCULATION: `benchmarks.py` → `derived/benchmarks.csv`, 116 rows; all gates and 9 tests pass]

Lane: `infra/immigration-fiscal/external_benchmarks_2026_09_24/`, 2026-09-24, brief
[BRIEF.md](BRIEF.md). The lane adopts nothing; every effect below is a proposal. Effects are $bn a
year of cost to other residents: low end = shared allocation, high end = personal, as in the adopted
main case ($203.2–249.6bn, `main_case_2026_09_23/`) and the audit package ($202.9–251.1bn,
`dataset_integrity_2026_09_23/synthesis.py`).

## Why the national closure cannot test shares

The account splits every BEA line between the Mexican-origin union and everyone else with a key.
Summed over both sides, those lines reproduce BEA's 2024 consolidated government account:
receipts $8,008.290bn, current expenditure $10,061.458bn, balance −$2,053.168bn [SOURCE:
`research/immigration-complete-annual-account-2026-09-20.md`, "Complete accounting"]. Any key,
right or wrong, splits 100% of its line, so the totals and the deficit hold by construction. A
wrong key moves dollars between the union and other residents and leaves every national figure
unchanged. The $2tn deficit therefore corroborates the account's totals, never its shares. Only an
independent distribution of the same dollars can test a key, over groups the key can be tabulated
on: income groups (CBO), ethnicity (Treasury), legal status (ITEP, SSA) and state by status
(hospital reports).

## Method

- **Frame and positive controls.** CPS ASEC 2025 public use (the account's pinned zip, sha256
  318845a2…, 161 weights). The lane's vectors reproduce all 28 published receipt-key shares and
  52 CPS/MEPS spending-key shares to 1e-9. The union is 40,896,574. The Node translator reproduces
  the adopted bands exactly with no change. The hospital translation reproduces the adopted
  uncompensated-care part ($3.6516–5.7476bn). Every hospital-report number is found verbatim in
  the saved text. [CALCULATION: `test_benchmarks.py`, 9 passed]
- **Arm 1 (CBO).** Households are ranked by income before transfers and taxes over √household
  size. Income is CPS total income less SSI and public assistance, plus employer OASDI/HI, capital
  gains and Medicare (BEA's $1,102.358bn spread over enrollees). Groups hold equal numbers of people; Q5 is
  split 81–90, 91–95, 96–99 and top 1%, and negative incomes are kept apart. For each CBO concept
  the account's key gives group shares π_j and the union's within-group share θ_j, so the union's
  share is Σπθ. Replacing π with CBO's shares and holding θ gives the benchmarked share. The change
  enters the explorer engine through `translate_main_case.js`. A gate checks it against a linear
  sum within each replicate. CBO's positive groups are renormalized to the key's positive-income
  mass, because CBO leaves negative incomes out of its quintiles. SEs come from 160 replicates.
- **Arm 2 (Treasury OTA).** The account's CPS tax-model keys are tabulated by the ethnicity of the
  tax-unit head. OTA imputes race and ethnicity to the primary filer. Credit dollars are translated
  onto the union by OTA/CPS ratios, credit by credit, holding totals. This assumes the CPS error is
  proportional within Hispanics.
- **Arm 3 (unauthorized taxes).** The account's taxes for the imputed-unauthorized Mexico-born
  union members (4.57m; `status_impute_2026_09_16`) are computed under the published keys ("raw")
  and under the audit's on-books rules (0.524, range 0.416–0.631). They are compared per person
  with ITEP, SSA and PWBM, indexed to 2024 wages by SSA's average wage index.
- **Arm 4 (hospital reports).** The account keys hospital uncompensated care by uninsured
  person-years (full-year uninsured plus half of part-year) at AHA's national $42.67bn for 2020,
  ×1.20 for 2024 prices. Applied to each state's imputed unauthorized, the keying gives the care the
  account implies for them. ρ is the unauthorized uninsured's cost per person-year over everyone
  else's, solved against the relevant total. The main case's inside part, g(s − k)N, is recomputed
  over the uncompensated lane's eight arms.
- **Verdict rule** (`benchmarks.py`):
  - "no" definitional match → context;
  - with a main-case effect: |effect| ≤ $2bn at both ends → corroborates, else contradicts;
  - otherwise: an external/account ratio in 0.8–1.25 corroborates.

## Arm 1: all households against CBO

CBO's latest edition is *The Distribution of Household Income, 2022* (publication 61911, January
2026). It is the newest on CBO's recurring-publication page at the last capture (Wayback,
2026-05-11); a search on 2026-09-24 found no later edition [SOURCE: `_cache/arm1/recurring_55134.html`].
Its researcher files are byte-identical to the copy in `distribution_weights_2026_09_23`.

**Definitions differ.**
- CBO measures income from tax records and administrative transfers, with employers' health
  premiums included [SOURCE: CBO 61911 p.11]. The CPS is a survey with top-coding: its top 1% hold
  7.9% of income before transfers and taxes, against CBO's 17.8% [DATA: `derived/cbo_ranking_check.csv`].
- The account's income tax line is gross of refundable credits (BEA line 25 carries them), so the
  central uses CBO's net tax plus CBO's Figure 15 credits for Q1–Q3 ("gross"). CBO's own net
  concept is reported as a bound.
- CBO's data year is 2022; the account's is 2024. The 2018 and 2019 editions give the same answers.
- Medicaid is compared on the community part ($954.2bn less the $264.7bn of long-term care that
  audit row 5 re-keys).

| Concept (2022) | Key's share: Q1 / top 1% | CBO: Q1 / top 1% | Union $bn: account → at CBO's shares | Main-case change, low / high | Verdict |
|---|---|---|---|---|---|
| Income tax before refundable credits | 0.4% / 19.2% | 0.4% / 36.1% | 128.2 → 115.0 | **+14.1 / +13.2** (SE 3.7 / 3.5) | contradicts |
| Payroll taxes (5 lines) | 4.3% / 4.2% | 4.6% / 4.7% | 150.6 → 150.7 | −0.1 / −0.1 | corroborates |
| Federal excise ($99.964bn part) | 5.6% / 7.0% | 10.7% / 6.4% | 8.1 → 9.4 | −1.3 / −1.3 | corroborates |
| Corporate (capital and labor lines) | top 1%: 10.6% | top 1%: 47.8% | 29.3 → 21.5 | 0 / 0 (engine) | key contradicted, unused |
| Medicaid, community part (MEPS θ) | 20.7% / 1.1% | 44.8% / 0.3% | 84.5 → 107.0 | +22.5 / +22.5 | contradicts key; see below |
| SNAP | 75.3% Q1 | 60.5% Q1 | 14.3 → 14.0 | −0.3 / −0.3 | corroborates |
| SSI | 58.7% Q1 | 60.9% Q1 | 5.30 → 5.22 | −0.1 / −0.1 | corroborates |
| Other means-tested (4 lines) | 76.0% Q1 | 54.6% Q1 | 23.6 → 22.5 | −0.4 / −0.7 | corroborates |
| Social Security (+ railroad) | 7.8% Q1 | 6.8% Q1 | 60.5 → 58.5 | −2.1 / −2.0 | at the $2bn line |
| Medicare | 12.8% Q1 | 13.8% Q1 | 64.0 → 64.7 | +0.7 / +0.7 | corroborates |
| UI, workers' compensation | | | | | untestable (CBO rounds to $100) |

[DATA: `derived/cbo_group_shares.csv`, `derived/cbo_translation.csv`; CALCULATION: `cbo_arm.py` →
`derived/cbo_spec_totals.csv`, `derived/cbo_main_case.csv`; CBO cells from researcher tables 01, 05,
07, 10–12 and figure-data Figure 15, SOURCE: https://www.cbo.gov/system/files/2026-01/61911-additional-data-for-researchers.zip]

**Income tax.** The key's income gradient is too flat. It gives Q4 17.7% and the top 1% 19.2% of
the line. CBO gives 11.7% and 36.1%. The union is concentrated in the lower groups: 57% of its
members are in Q1–Q2 and 0.3% in the top 1% [DATA: `cbo_ranking_check.csv`]. Its share of the line
therefore falls from 5.33% to 4.79% [CALCULATION: `cbo_translation.csv`]. This is the same defect as
audit row 3 (the $385bn BEA–CPS gap keyed by CPS liability), but CBO also corrects the CPS liability
itself, so it is larger:
- with CBO's credits added up to Q4, +$12.0–12.8bn;
- on CBO's 2019 data +$12.1–12.9bn, and on 2018 data +$13.6–14.6bn;
- with CBO's net tax, the wrong concept for this line, +$38.9–39.5bn.

Against the audit package the CBO figure replaces row 3's +9.5/+9.6, an increment of about
**+$4.6 / +$3.6bn**. That increment is an upper bound. Rows 2 and 13 lower the union's income tax
inside each group, and the reweighting scales with it [INFERENCE].

**Medicaid.** The account's Medicaid key is a MEPS payer mean by age band and US/non-US birth,
applied to everyone in the cell. It carries no income gradient: Q1–Q4 each hold about 20% of the
dollars, where CBO puts 44.8% in Q1 and 8.6% in Q4. Holding the union's within-group share gives
+$22.5bn. Using the union's share of Medicaid-covered persons inside each group gives +$47.5bn.

The pooled-MEPS lane measured the union's Medicaid directly by ethnicity. On this line it found
**+$12.2 to +$21.3bn** (winsorized +13.6), with offsets on Medicare (−9.9) and health services
(−5.7) [SOURCE: `medical_ethnicity_pooled_2026_09_23/RESULT.md`, verdict table]. CBO's gradient
corroborates the direction and rough size of that Medicaid line. It is not an additional change. The
coverage-θ figure is contradicted by the pooled lane's finding that covered Mexican-origin people
draw fewer dollars per head. Route to decision 2; no separate proposal.

**Excise.** CBO's federal excise is more regressive than the account's consumption key (Q1 10.7%
against 5.6%): −$1.3bn. The consumption key also carries $602bn of general sales tax, $271bn of
state and local excise, $84bn of customs duties and $141bn of personal current transfers, none of
which CBO distributes. Applying CBO's excise gradient to all of them gives **−$15.2bn**. That is a sensitivity, not a proposal: federal excises
(fuel, tobacco, alcohol) are more regressive than general sales taxes. The consumption key remains
the largest receipt key without an outside test.

**Corporate.** CBO puts 48% of corporate tax on the top 1%; the key puts 11%. At CBO's shares the
union's corporate receipts fall $7.1–7.8bn. The engine's change is 0: corporate cells are indirect
receipts, and the main case gives indirect receipts no response (`engine.js`,
`indirect_receipt_response: 0`). The key would matter only in a profile where incidence receipts
respond.

**Bundles** (every translated concept at its central, 2022): +$33.0 / +$31.9bn. Without Medicaid,
which belongs to decision 2: **+$10.6 / +$9.4bn** (SE 3.8 / 3.5). The 2019 data give +$9.7 / +$8.7bn
and the 2018 data +$13.7 / +$12.6bn. With the excise gradient on every consumption line, +$19.1 /
+$18.0bn. [DATA: `derived/cbo_spec_totals.csv`]

## Arm 2: taxes and credits by Hispanic ethnicity (Treasury OTA)

OTA is the only publisher found of tax-record distributions by Hispanic ethnicity. It imputes race
and ethnicity to the primary filer (BIFSG). Its universe is filers plus nonfilers with an
information return. It publishes no share of income tax liability or AGI.
[SOURCE: OTA Working Paper 122, January 2023, Table 5 (printed p.29),
https://home.treasury.gov/system/files/131/WP-122.pdf]

| Item | CPS, account's tax model | OTA | OTA / CPS | Verdict |
|---|---:|---:|---:|---|
| Tax units with a Hispanic head/primary filer | 18.9% | 15% (FY2023); 15.1% (27.9M of 184.5M, 2024 count) | 0.79–0.80 | contradicts (universes differ) |
| EITC incl. outlays, raw key | 37.7% | 28% | **0.74** | contradicts |
| EITC with the audit's SSN rule | 30.2% | 28% | 0.93 | corroborates |
| Child credits incl. outlays, raw | 22.0% | 22% | 1.00 | corroborates |
| Child credits, on-books rule 0.42–0.63 | 20.0–20.8% | 22% | 1.06–1.10 | corroborates |
| Premium credit: subsidized-marketplace persons vs dollars | 28.3% | 18% | 0.64 | contradicts (persons vs dollars) |
| Dividends and capital gains vs preferential-rate expenditure | 4.8% | 3% | 0.63 | context |
| Average income tax per joint return, Hispanic / white | 0.48 (CPS 2024: $11,010 / $23,059) | 0.33 (TY2023: $9,477 / $28,664) | 0.69 | contradicts |

[DATA: `derived/ota_shares.csv`; SOURCE: WP-122 Table 5; WP-124 Table 3 "Total" rows (PDF p.17),
https://home.treasury.gov/system/files/131/WP-124.pdf; OTA 2024 family counts,
https://home.treasury.gov/system/files/131/2024-Family-Counts-by-Filing-Status-Children-Race-Hispanic-Ethnicity-01142025.pdf]

**Translation onto the union's refundable-credit key** (the $110.46bn not in premium credits):
- EITC and child credits at OTA's shares, against the adopted raw keys: **−$4.6 / −$4.3bn**
  (SE 0.13). [CALCULATION: `ota_arm.py` → `derived/ota_main_case.csv`]
- Against the audit package, whose SSN rule already zeroes the EITC of the Latin-American-born
  imputed unauthorized: −$0.4 / −$0.3bn. OTA corroborates the audit's rule.
- Premium credits: audit row 1 keys them by the union's 10.9% of subsidized-marketplace persons.
  OTA's persons-to-dollars ratio would cut that further, **−$4.6bn** against the audit package. That
  check is weak. OTA's FY2023 figure is a projection from a 2016 sample. It predates the 2024
  enrollment rise, and it compares dollars with a person count. No change is proposed.

**Joint returns.** Indexed to 2024 wages (SSA average wage index 66,621.80 → 69,846.57), OTA's
figures are $9,936 per Hispanic joint return and $30,051 per white one [CALCULATION]. The CPS model
has Hispanic couples 11% too high and white couples 23% too low. The second is the top-coding that
arm 1 and audit row 3 correct. The first is the direction of audit rows 2 and 13 (compliance and
fill-ins); an 11% overstatement of the union's $128.2bn is about $14bn. That is not added: it is
Hispanic-wide, on one filing status, and those rows already take +$20.4–22.3bn over row 3
[SOURCE: `dataset_integrity_2026_09_23/README.md`, tax block].

## Arm 3: the unauthorized tax side

Every anchor is a model; none measures payment by the Mexico-born.
- **ITEP (July 2024)** puts 2022 taxes of 10.9M undocumented at $96.7bn. It assumes a 60%
  income-tax contribution rate [SOURCE: ITEP, *Tax Payments by Undocumented Immigrants*, pp.3–7,
  27; local copy `onbooks_share_2026_09_23/_cache/itep2024.pdf`].
- **SSA's Actuarial Note 151** gives $13bn of OASDI taxes in 2010 [SOURCE:
  https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf p.3].
- **Penn Wharton** puts OASDI at about $24bn in 2024, built on Note 151's shares [SOURCE:
  https://budgetmodel.wharton.upenn.edu/p/2025-06-18-the-impact-of-president-trumps-deportation-policies-the-social-security-program/].

The on-books lane built the audit's 0.52 share from the same Note 151. Agreement between SSA or PWBM
and the audit's rule is therefore not independent.

Union's imputed-unauthorized Mexico-born, 4.57m people, personal allocation, $ per person;
anchors are per person over all origins, indexed to 2024 wages:

| Item | Anchor | Anchor, 2024 | Account raw | Raw / anchor | Account at 0.524 | 0.524 / anchor |
|---|---|---:|---:|---:|---:|---:|
| Federal income tax less EITC/ACTC | ITEP | 1,959 | 1,709 | 0.87 | 1,399 | 0.71 |
| OASDI | ITEP | 2,581 | 3,633 | 1.41 | 1,928 | 0.75 |
| OASDI | SSA 2010 | 2,017 | 3,633 | 1.80 | 1,928 | 0.96 |
| OASDI | PWBM 2024 | 2,182 | 3,633 | 1.67 | 1,928 | 0.88 |
| Medicare HI | ITEP | 643 | 996 | 1.55 | 528 | 0.82 |
| Unemployment insurance | ITEP | 181 | 395 | 2.19 | 211 | 1.17 |
| State and local income tax | ITEP | 703 | 757 | 1.08 | 399 | 0.57 |
| State and local sales and excise | ITEP | 1,517 | 1,481 | 0.98 | 1,481 | 0.98 |

[CALCULATION: `unauthorized_arm.py` → `derived/unauthorized_gap_mexico_born.csv`,
`derived/unauthorized_anchors.csv`; AWI SOURCE: https://www.ssa.gov/oact/cola/AWI.html, Wayback
capture in `_cache/arm3b/`]

- **Against the adopted main case (raw keys),** the anchors say payroll taxes are overstated. OASDI
  alone is +$4.8bn (ITEP), +$6.6bn (PWBM) or +$7.4bn (SSA) of cost, and ITEP's six items total
  +$6.3bn. Every anchor that assumes partial compliance must say this, so the anchors support the
  direction of audit row 2 but add no measurement of its size.
- **Against the audit package (0.524),** the anchors sit above the account. OASDI is −$0.4bn (SSA),
  −$1.2bn (PWBM) or −$3.0bn (ITEP), and ITEP's six items total −$7.5bn. At the range's high share
  (0.631) the six items are −$3.4bn, and SSA and PWBM fall within ±$1.4bn.
- **Proposal:** none beyond a pointer. ITEP, the one anchor not built on Note 151, favors the upper
  half of the on-books range. At 0.63 the on-books lane puts row 2 at +$8.9–10.2bn instead of
  +$12.4–14.0bn [SOURCE: `onbooks_share_2026_09_23/RESULT.md`, verdict].
- **ITIN filings** are measured: returns carrying an ITIN paid $14.5bn of income tax after credits
  in TY2022 [SOURCE: National Taxpayer Advocate, 2024 Annual Report, research report 3, Fig. 5.3.3,
  printed p.230]. They cover a different population (SSN primaries with ITIN dependents, and none
  of the unauthorized who work under an SSN), so they cannot test the key.

## Arm 4: Florida and Texas hospital status reports

Both leads exist.
- **Florida.** Statute s. 395.3027 F.S. makes hospitals that accept Medicaid ask status. AHCA has
  published counts for June–December 2023 and calendar 2025, and a press release for 2024.
- **Texas.** Executive Order GA-46 requires Medicaid/CHIP-enrolled acute hospitals to report
  status counts and costs. HHSC published November 2024 and a FY2025 summary (November 2024 to
  August 2025).

[SOURCE: AHCA 2023-data report, https://ahca.myflorida.com/content/download/24244/file/Report_Hospital_Patient_Immigration.pdf
(Wayback 20240417170034) pp.2, 4; AHCA 2025 report,
https://ahca.myflorida.com/content/download/28608/file/2025_Immigration_Report.pdf (Wayback
20260331153722) pp.3–6; AHCA press release 2025-03-07,
https://ahca.myflorida.com/content/download/26215/file/3.7.25_Hospital_Patient_Immigration_Status.pdf;
HHSC FY2025 summary, https://www.hhs.texas.gov/sites/default/files/documents/executive-order-ga-summary-2025.pdf
(Wayback 20260109162316) p.1; HHSC GA-46 form,
https://pfd.hhs.texas.gov/sites/default/files/documents/hospital-svcs/exec-order-ga-46-form.pdf]

**Account side, CPS 2025** [DATA: `derived/hospital_states.csv`]:

| | Florida | Texas | United States |
|---|---:|---:|---:|
| Imputed unauthorized, all origins | 1.40m (SE 0.12), 6.0% of residents | 2.37m (SE 0.16), 7.7% of residents | 14.90m |
| Their uninsured person-years | 0.547m, 20.9% of the state's | 1.307m, 23.1% of the state's | 6.745m, 20.7% |
| Account keying, their uncompensated care, 2020 / 2024 prices | $0.72 / $0.86bn | $1.71 / $2.06bn | $8.84 / $10.61bn |

**Level checks: the uninsured keying at state scale.**
- **Texas.** The keying implies $7.4–8.9bn of uncompensated care. HHSC's pool model, as cited by
  the Texas Hospital Association, puts uninsured charity care at DSH and UC hospitals at "at least
  $8.1 billion" in 2023. That figure excludes bad debt. Ratio 0.91–1.09: corroborates [SOURCE:
  https://www.tha.org/wp-content/uploads/2024/09/Charity-care-FAQ-September-2024-FINAL.pdf p.3,
  secondary].
- **Florida.** FHURS 2022 puts care "not covered directly through Medicare, Medicaid, private
  insurance, or self-pay" at 3.76% of $69.05bn = $2.60bn, against the keying's $3.4–4.1bn. Ratio
  0.63–0.76: Florida's cost per uninsured person-year is below the national average, or its measure
  is narrower [SOURCE: AHCA 2023-data report p.2].

**Unlawfully present (NLP) patients, at face value:**

| Reading | Report | Account at equal use | ρ | Main-case change, low / high |
|---|---|---|---:|---|
| Texas, non-Medicaid cost ×12/10, against AHA's national total | $0.925bn | $1.71–2.06bn | 0.39–0.48 | −0.57 / −0.84 to −0.69 / −1.00 |
| Texas, against the state's $8.1bn floor | $0.925bn | $1.87bn | 0.43 | −0.64 / −0.94 |
| Florida 2023, NLP share of the state's uncompensated care (shares of one cost base) | 17.4–21.8% | 20.9% | 0.80–1.06 | +0.06 / +0.09 to −0.21 / −0.30 |
| Florida 2025, same | 11.9–15.0% | 20.9% | 0.51–0.67 | −0.35 / −0.51 to −0.54 / −0.78 |
| Florida in dollars (2024 press or restated, 2025; cost bases differ) | $0.48–0.61bn | $0.54bn | 0.86–1.17 | −0.15 / −0.22 to +0.16 / +0.23 |

[CALCULATION: `hospital_arm.py` → `derived/hospital_benchmarks.csv`, `derived/hospital_main_case.csv`]

How to read the table:
- The Florida share rows are the leading reading. AHCA prices every encounter at average cost, so
  NLP cost and uncompensated care are shares of one hospital cost base, and the base cancels.
- The Medicaid paid claims set the two ends of each Florida range: zero, or claims over the 2022
  operating expense. The 2023 claims are inferred from the 2025 report's "fell by 30% since 2023"
  [INFERENCE].
- The dollar rows set NLP costs built on 2023–24 cost bases against 2022 uncompensated care, so
  they overstate ρ.

**The reports cannot sign the account's error.**
- Their counts omit patients who declined to answer. Florida 2025 reaches equal use (ρ = 1) if 4.0–6.0% of its 703,600
  decliners were unlawfully present. Florida 2023 needs −0.5% to 1.8% of 486,235. Texas files but
  does not publish decliners. It would need 2.0–2.2× the reported NLP cost.
- Their costs are gross of payments, including privately insured NLP care.
- The first bias pushes ρ down and the second up.

Read at face value, the hospital reports put the main case's uncompensated part between **−$1.0bn
and +$0.1bn** of its adopted value. The adopted 0.7× sensitivity (−$1.5 / −$2.2bn) already covers
that. No change is proposed. The line is not in the audit package, so the same range applies there.

**Definitional gaps.**
- *Charges and costs.* Texas reports costs, "not charges", with no revenue offsets deducted
  [SOURCE: GA-46 form]. Florida does not collect cost: it multiplies NLP shares of admissions and
  ED visits by county hospital cost (FHURS), which is average cost, not patient cost [SOURCE: AHCA
  2025 report, p.6 method]. AHA's national total is uncompensated care at cost, net of payments.
- *Emergency Medicaid.* Texas splits Medicaid/CHIP NLP care: $0.34bn a year, emergency Medicaid
  plus CHIP's unborn-child option. Florida publishes Medicaid paid claims: $76.6M in 2024 and
  $80.2M in 2025. In the account those dollars sit on the Medicaid line. That line's nativity key
  gives Texas's imputed unauthorized $4.07bn and Florida's $2.38bn of Medicaid, over all services.
  The key is tested by ethnicity in the pooled-MEPS lane, so these are context only.
- *Who is counted.*
  - Self-reported status at registration, all origins, counted as encounters, not people.
  - Florida's decliners are 5.5–7.7% of encounters. Florida excludes seven Steward hospitals and
    state hospitals.
  - Texas covers ED and inpatient care only. Its FY2025 total covers ten months (September and
    October 2024 were not collected). Its November 2024 figure was restated from $121.8M to $102.2M.
  - The account side counts the CPS residual-method unauthorized.
- *Scale.* NLP patients are 0.56% of Florida's 2025 encounters, against 6.0% of residents imputed
  unauthorized. With every decliner counted NLP, the share is 6.1%.

## Arm 5: NAS 2017 chapter 8 (not done)

Not attempted, for three reasons.
- NAS publishes its 2013 cross-section only as federal and state-local per-capita receipts and
  outlays, and as scenario splits (interest, public goods). Components appear only in figures.
  First generation and dependents, 55.5M: receipts $10,887 and outlays $15,908 per capita
  [SOURCE: NAS 2017, Table 8-1, p.389, local `sources/immigration-fiscal/data/external/nas_2016/23550.pdf`].
  That is 0.79 and 0.90 of the all-group average [CALCULATION from Table 8-1's three groups].
- The account's education keys exist for the union only.
- NAS's group (independents plus dependents) needs parent links that the frame does not carry.

A later lane can compare those scale-free ratios with the account's first generation.

## Main-case proposals

| Finding | vs adopted main case | vs audit package | Status |
|---|---|---|---|
| Income tax key too flat at the top (CBO, gross) | +14.1 / +13.2 | about +4.6 / +3.6 over row 3; an upper bound | contradicted; propose |
| CBO gaps on payroll, excise, Social Security, Medicare, SNAP, SSI, other transfers | −3.5 / −3.7 together | same | corroborated; each ≤ $2.1bn |
| EITC and child credits at OTA's Hispanic shares | −4.6 / −4.3 | −0.4 / −0.3 | raw key contradicted; audit rule corroborated |
| Premium credits at OTA's ratio | — | −4.6 | weak check; not proposed |
| Medicaid income gradient | +22.5 (+47.5 coverage θ) | — | corroborates decision 2's Medicaid line; not additive |
| Consumption key on all consumption lines | −15.2 | same | sensitivity only |
| Corporate key | 0 | 0 | contradicted, unused by the main case |
| Unauthorized taxes (modelled anchors) | +4.8 to +7.4 payroll; +6.3 ITEP's six items | −0.4 to −3.0 OASDI; −7.5 ITEP six items (−3.4 at 0.631) | row 2's direction supported, not its size |
| Uncompensated care (hospital reports, face value) | −1.0 to +0.1 | same | consistent with equal use; not proposed |

The CBO bundle without Medicaid and the OTA credit change touch different lines, so they add. The
adopted main case would become **$209.2–254.8bn** (+6.0 / +5.1; SE about 3.8 / 3.5). The audit package
would become **$203.6–250.6bn** (+0.7 / −0.5), before rows 2 and 13 shrink the income-tax increment
[CALCULATION: 203.207 + 10.560 − 4.554; 249.640 + 9.444 − 4.313; 202.9 + 1.08 − 0.36;
251.1 − 0.15 − 0.34].

## Corroborated, contradicted, uncorroborated

- **Corroborated by an outside distribution:**
  - payroll-tax, SNAP, SSI, other means-tested, Medicare, federal-excise and Social Security
    income gradients (CBO);
  - child-credit Hispanic share (OTA);
  - EITC under the audit's SSN rule (OTA);
  - state and local sales tax per unauthorized person (ITEP, 0.98);
  - the uninsured keying's Texas level (HHSC/THA);
  - uncompensated care for the unauthorized within the reports' face-value bounds.
- **Contradicted:**
  - income tax gradient: +$13.2–14.1bn, +$3.6–4.6bn over the audit;
  - raw EITC key: −$4.3–4.6bn, already in the audit;
  - Medicaid income gradient: already in decision 2;
  - corporate gradient: no main-case effect;
  - raw payroll keys for the unauthorized: already in the audit;
  - Florida's level of uncompensated care per uninsured person-year: 0.63–0.76 of the national
    keying, no main-case effect.
- **Uncorroborated (no outside distribution found):**
  - state and local income tax and property tax keys for the whole group;
  - the consumption key for state and local sales taxes;
  - UI and workers' compensation (CBO too coarse);
  - income-tax liability by ethnicity (OTA publishes none);
  - any Mexico-born tax figure;
  - education, justice, general government and health-services keys (outside this lane).

## What would change these conclusions

- **Income tax.** The finding rests on holding the union's within-group share fixed. A published
  income-tax liability by ethnicity would test that share directly. So would an SOI-linked
  distribution of the gap. None was found.
- **Credits.** The AEA 2024 paper's updated OTA imputation would give 2024-year EITC and child
  credit shares by ethnicity (blocked below).
- **Consumption key.** A distribution of state and local sales taxes by income on CBO's groups
  would test it. ITEP's *Who Pays* is the lead; it was not read here.
- **Hospital reports.** Texas's decline counts would sharpen ρ by as much as the declines are
  large. The Florida 2024 report with its cost base would also help.
- **Unauthorized taxes.** Any measured Mexico-born figure.

## Limits

- CBO's year is 2022, the account's 2024. CBO's income comes from tax records and the CPS's from a
  survey. The frame omits employers' health premiums from income.
- The translation assumes CBO's gradient applies to the account's 2024 BEA lines.
- OTA's shares are FY2023 projections from a 2016 sample with imputed ethnicity. The OTA translation
  assumes the CPS error is proportional within Hispanics.
- Status comes from the repo's residual imputation. It prints [DEGRADED] for status-blind states;
  Florida and Texas are not among them. The all-origin imputed unauthorized carry far more income
  tax than any anchor: $93.6bn net under the raw keys, against ITEP's $19.5bn. The non-Latin cells
  that drive this are not used for the union and were not examined.
- The Texas statewide total is secondary (THA citing HHSC) and a floor. Florida's 3.76% ratio is
  for 2022.

## Specifications computed (spec columns)

- `derived/cbo_group_shares.csv`, `spec`: 45 values. Each of 2022, 2019 and 2018 has:
  - `individual_inc_tax=individual_inc_tax_gross` (central);
  - `individual_inc_tax` (CBO net: against the reading, +$38.9–49.6bn);
  - `individual_inc_tax=individual_inc_tax_gross_q4`;
  - `payroll_taxes`, `excise_taxes`, `corporate_inc_tax`, `medicaid_and_chip`, `snap`, `ssi`,
    `other_transfers`, `social_security`, `medicare`;
  - `unemployment_insurance` and `workers_compensation` (untestable);
  - `excise_all_consumption_lines=excise_taxes` (sensitivity, −$15.2 to −$16.2bn).
- `derived/cbo_translation.csv`, `spec`: the same, less UI and workers' compensation, plus
  `medicaid_and_chip=coverage_theta` for each year (+$47.5–49.0bn, against the pooled-MEPS evidence).
- `derived/cbo_spec_totals.csv`, `spec`: the translated main-case specs (corporate excluded) plus
  three bundles for each year: `all_concepts`, `all_but_medicaid` and
  `all_concepts_excise_on_all_consumption_lines`.
- `derived/cbo_main_case.csv`, `method`: those specs plus `corporate_inc_tax` for each year
  (engine change 0), for three profiles each.
- `derived/cbo_components.csv` and `derived/cbo_ranking_check.csv`: no spec column (2022 central
  decomposition; ranking check).
- `derived/ota_shares.csv`, `item`: 19 items, including the account's own key shares and the Mexican
  share of Hispanics (0.59).
- `derived/ota_translation.csv`, `spec`: `vs_adopted_raw_keys`, `vs_audit_package_ssn_rule` and
  `audit_row1_ptc_person_key`. `ota_main_case.csv` carries the first two.
- `derived/unauthorized_taxes.csv` and `derived/unauthorized_anchors.csv`:
  - `rule`: `raw`, `on_books_central`, `on_books_low` and `on_books_high`;
  - `allocation`: personal and shared;
  - groups: Mexico-born union, Latin-American-born, all origins.
  - Against the reading: all-origin ratios of 1.4–3.2 to the anchors (non-Latin cells), and
    `on_books_low` putting ITEP's six items at −$11.7bn.
- `derived/unauthorized_gap_mexico_born.csv`: the four rules × eight anchor items, personal.
- `derived/hospital_main_case.csv`, `spec`: 16 values. They cover Texas national 2020 and 2024 and
  within-state; Florida 2023 and 2025 within-state shares with and without Medicaid claims; and
  Florida dollar and national versions for 2025, the 2024 press figure and the 2024 restated
  figure. Against the reading: Florida 2023 without claims (+$0.06 / +$0.09bn) and Florida 2024
  dollars (up to +$0.23bn).
- `derived/hospital_benchmarks.csv` (19 rows, `spec` links the translated ones) and
  `derived/hospital_states.csv` (place × group).
- `derived/benchmarks.csv`: 116 rows. The `spec` column carries all of the above.

## Blocked and not done

- [BLOCKED] AEA *Papers & Proceedings* 114 (2024), Cronin, DeFilippes & Fisher, refundable credits
  by race and Hispanic ethnicity with OTA's updated imputation:
  https://www.aeaweb.org/articles/pdf/doi/10.1257/pandp.20241037 returns a paywall page, and its
  openICPSR package (e200502) requires a login.
- [BLOCKED] Florida AHCA calendar-2024 report PDF. It is not on the AHCA site or in Wayback; only the
  press release exists. The dashboard CSV export returned 403.
- [BLOCKED] Texas GA-46 counts of lawfully present and declined patients. The form collects them and
  HHSC does not publish them. The interim quarterly releases and HHSC's own UC pool model were not
  found or fetched.
- [BLOCKED] Any Mexico-born split of unauthorized taxes. ITEP gives only "just over 4 in 10 are from
  Mexico".
- Not found: SSA Earnings Suspense File additions by tax year; the National Taxpayer Advocate's 2025
  ITIN tables.
- Not done: arm 5 (above).

Primary documents are in `_cache/arm1`–`arm4` (ignored). Each arm's `NOTES.md` there records URLs,
Wayback timestamps, pages and verbatim lines; the URLs used in calculations are repeated above.

## Reproduce

From the repository root; `node` is needed for the main-case translation:

```sh
L=infra/immigration-fiscal/external_benchmarks_2026_09_24
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow --with openpyxl --with pytest python3 -m pytest $L/test_benchmarks.py -q
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow --with openpyxl python3 $L/cbo_arm.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow python3 $L/ota_arm.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow python3 $L/unauthorized_arm.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow python3 $L/hospital_arm.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with pyarrow python3 $L/benchmarks.py
```

The first run builds `_cache/cps25_frame.parquet` from the pinned CPS zip
(`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`). The CBO researcher zip is checked by
sha256 (703c3f8c…) under `_cache/arm1/`.
