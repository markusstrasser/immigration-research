# Outside checks on the account's shares

Date: 2026-09-24. [MODEL / FRAMING-SENSITIVE] Proposed corrections only. The main case stays as
adopted until the operator decides, and narrative authorship remains the operator's.

**Adopted 2026-09-24 (ladder 219).** The operator adopted these checks together with the dataset audit. One
engine run gives a main case of $200.9–246.3bn ([lane](../infra/immigration-fiscal/main_case_2026_09_24/RESULT.md),
[decision](../decisions/2026-09-24-main-case-audit-and-outside-checks.md)). The proposals below are kept as computed on the September 23 case.

The complete annual account allocates BEA's 2024 consolidated government account exactly: $8,008.290bn
of current receipts and $10,061.458bn of current expenditure, a balance of −$2,053.168bn [SOURCE:
[complete account](immigration-complete-annual-account-2026-09-20.md), section "Complete accounting,
before any causal interpretation"]. Every dollar is assigned to someone, so that closure cannot catch a
keying error: a wrong key moves dollars between the Mexican-origin group and other residents and leaves
every total intact. The checks below test the shares instead, each against data built independently of
the account. They follow the operator's question on September 24 about what still looks wrong in the
account.

| Check | Lane | Status |
|---|---|---|
| School cost where the group's pupils enroll | [school_cost_where_enrolled_2026_09_24](../infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md) | done, ladder 215 |
| Benefit keys against administrative records by ethnicity | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) | done, ladder 217 |
| Taxes and transfers against CBO, Treasury, tax anchors and state hospital records | [external_benchmarks_2026_09_24](../infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md) | done, ladder 216 |
| Direction of the errors in the crime ratios | [crime_ratio_direction_2026_09_24](../infra/immigration-fiscal/crime_ratio_direction_2026_09_24/RESULT.md) | done, ladder 218 |
| Consumption taxes keyed on spending, net of remittances (2026-09-25) | [consumption_key_2026_09_24](../infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md) | done, ladder 225; proposed, not adopted |

## Schools: priced where the pupils enroll

The school step is the line that turns the account's balance into a cost: $87.14–113.96bn in the
adopted main case. The worry was that it charged the national average per pupil while the group's
pupils sit in cheaper states such as Texas and Arizona. It does not. Since the September 20 enrollment
correction, the key prices each of the group's 8.49m pupils at its own state's FY2024 current spending
per pupil (Census Annual Survey of School System Finances, Table 8): $16,860 per group pupil against
$17,669 for all pupils, a ratio of 0.954 [CALCULATION: `account_pupils.py` →
`derived/account_embedded_price.json`]. The state mix is already in the line. Multiplying the line by
the group's ratio to the national average (0.981) would count Texas and Arizona twice and wrongly cut
$1.6–2.1bn.

What the key misses is where the pupils sit inside their states. The lane weights each district's
FY2024 current spending per pupil (F-33) by its Mexican-origin pupils: CCD 2023–24 Hispanic membership
× ACS Mexican shares by district.
- The group's districts spend 2.47% more than their state averages. The lift is a big-city effect: Los
  Angeles Unified carries 38% of it, then New York City, Chicago, Dallas and Fresno. Growing suburban
  and border districts in Texas pull the other way.
- Its schools spend 0.57% more than their districts (NCES School-Level Finance Survey, FY2022).
- The administrative state mix adds 0.26%: it puts more of the group in California and Texas than the
  survey does.

Together these raise the school component of the key by k = 1.034 (low 1.020, high 1.047)
[CALCULATION: `weighting.py`, `within_district.py`, `checks.py` → `derived/r_by_spec.csv`,
`within_district.json`, `top_districts.csv`].

| Package | School line, $bn | Total, $bn | Change in total, $bn |
|---|---|---|---|
| Main case adopted September 23 | 87.14–113.96 | 203.21–249.64 | — |
| Main case, k = 1.034 | 89.94–117.62 | 206.59–252.67 | +3.38 / +3.03 |
| k = 1.020, pre-COVID district pattern | 88.76–116.07 | 205.16–251.39 | +1.95 / +1.75 |
| k = 1.047, adds the English-learner premium within districts | 91.01–119.03 | 207.89–253.84 | +4.68 / +4.20 |
| Audit package, k = 1.034 | — | 205.70–253.61 to 205.88–253.77 | +2.5 to +3.0 |

[CALCULATION: `lines.py` → `derived/per_pupil_weighting.csv`. The lane's engine run reproduces the
published school step and main case before any change (`test_lane.py`, 4 tests pass); the parent's
re-run left all 21 derived files byte-identical.]

The direction holds in every Mexican-origin weighting (k 1.010–1.072). Dropping Los Angeles Unified
leaves k unchanged, because its spending also raises the California average the other districts are
compared with. Hispanic-wide weights would overstate k (1.089), since non-Mexican Hispanic pupils sit
in dearer states. The size rests mostly on FY2024 spending, which includes COVID relief: 3.4% of
current spending nationally and 4.4% in California. Net of relief k is 1.022, and on FY2019 spending
1.016 [SOURCE: F-33 2024 form, Part XIII item 1; CALCULATION: `derived/price_source_check.csv`,
`r_by_spec.csv`].

**Audit row 6 needs an engine run before decision 1.** Through the engine, the audit's education-split
correction moves the main case by −1.8 to −2.6bn at the low end and −2.6 to −3.7bn at the high end,
not the −3.5bn the audit subtracts at both ends. The audit's figure matches the change in allocation
before the 63–66% school response is applied [CALCULATION: `per_pupil_weighting.csv`, specs
`audit_row6_w0.77_whole_line` and `audit_row6_w0.82_whole_line`; `lines_summary.json`] [INFERENCE on
the cause]. If so, at the midpoint of the split, the audit package sits about $1.3bn higher at its low
end and $0.4bn at its high end.

Limits: time frames are mixed (ACS 2020–2024 shares, CCD 2023–24 counts, F-33 FY2024, school-level
FY2022, English-learner counts 2018–19). The 0.68m group pupils in charters run by nongovernmental
bodies take their state's group mean. District Mexican shares cover residents of all ages and are
scaled to children by a state ratio. The 63–66% response and the education line are untouched.

## Taxes and transfers against outside distributions

Each key splits 100% of its line, so the only test of a key is an independent distribution of the
same dollars over groups the key can be tabulated on: income groups (CBO), ethnicity (Treasury),
legal status (tax anchors) and state by status (hospital reports). The lane reproduces all 28
published receipt-key shares and 52 spending-key shares before any comparison [CALCULATION:
`test_benchmarks.py`, 9 tests pass; the parent's re-run left all 18 derived files byte-identical].

**CBO's income distribution corroborates most transfer and payroll keys.** On CBO's *Distribution of
Household Income, 2022* (January 2026), the keys' income gradients for payroll taxes, federal
excise, Social Security, Medicare, SNAP, SSI and other means-tested transfers each move the main case
by $2.1bn or less, −$3.5bn / −$3.7bn together [SOURCE: CBO publication 61911, researcher tables;
CALCULATION: `cbo_arm.py` → `derived/cbo_main_case.csv`].

**The federal income tax key is too flat at the top.** It puts 19.2% of income tax before refundable
credits on the top 1% of households, where CBO puts 36.1%, because the CPS top-codes high incomes.
The group sits low in the distribution (57% in the bottom two fifths, 0.3% in the top 1%), so its
share of the line falls from 5.33% to 4.79%. That adds **+$14.1bn / +$13.2bn** of cost (SE 3.7 /
3.5; +$12.1–14.6bn on CBO's 2018 and 2019 data). Audit row 3 already takes +$9.5bn / +$9.6bn for the
same defect, so the increment over the audit package is at most +$4.6bn / +$3.6bn [CALCULATION:
`derived/cbo_translation.csv`, `cbo_spec_totals.csv`]. The finding holds the group's position inside
each income group fixed; no published income tax by ethnicity tests that.

**Treasury's EITC shares confirm the audit's rule and contradict the raw key.** Treasury's Office of
Tax Analysis finds that "Hispanic families are 15 percent of all families but receive 22 percent of
the benefits of the child tax credit (CTC) and 28 percent of the benefits of the Earned Income Tax
Credit" [SOURCE: OTA Working Paper 122, January 2023, Table 5 and text]. The account's raw CPS key
gives Hispanic tax units 37.7% of the EITC, the audit's SSN rule 30.2%, and 22.0% of child credits.
At Treasury's shares the adopted main case falls −$4.6bn / −$4.3bn; the audit package moves only
−$0.4bn / −$0.3bn [CALCULATION: `ota_arm.py` → `derived/ota_main_case.csv`].

**Other results.**
- Medicaid: the key has no income gradient (each of the bottom four fifths holds about 20% of the
  dollars; CBO puts 44.8% in the bottom fifth). CBO's gradient implies +$22.5bn, which corroborates
  the pooled-MEPS Medicaid line in pending decision 2 (+$12.2–21.3bn) and must not be added to it.
- Corporate tax: the key puts 11% on the top 1% against CBO's 48%, but the main case gives
  indirect receipts no response, so the effect is zero.
- Consumption: the largest receipt key without an outside test. CBO's federal excise gradient,
  spread over all consumption-keyed lines, would give −$15.2bn; general sales taxes are less
  regressive than fuel, tobacco and alcohol excises, so that is a sensitivity only.
- Unauthorized taxes: the outside figures are models. SSA's Actuarial Note 151 and Penn Wharton
  share their compliance input with the audit's on-books share, and ITEP assumes its own. Under the
  raw keys the group's imputed-unauthorized members pay 1.4–1.8 times the anchors' payroll taxes
  per person; at the audit's 0.524 on-books share they pay at or below them. The anchors support
  the direction of audit row 2, not its size; ITEP favors the upper half of the on-books range.
- Hospital reports: Florida's status reports (AHCA, under s. 395.3027) and Texas's (HHSC, under
  executive order GA-46), taken at face value, put the unauthorized uninsured's hospital use at
  0.39–1.06 times other uninsured people's. That moves uncompensated care by −$1.0bn to +$0.1bn,
  inside the adopted sensitivity.

| Package | Total, $bn | Change, $bn |
|---|---|---|
| Main case adopted September 23 | 203.21–249.64 | — |
| With the CBO keys (Medicaid excluded) and Treasury's credit shares | 209.2–254.8 | +6.0 / +5.1 (SE about 3.8 / 3.5) |
| Audit package with the same | 203.6–250.6 | +0.7 / −0.5, before rows 2 and 13 shrink the income-tax increment |

[CALCULATION: `derived/cbo_main_case.csv`, `ota_main_case.csv`; 203.207 + 10.560 − 4.554 and
249.640 + 9.444 − 4.313.] These changes are relative to the adopted main case and are not combined
with the school correction above. Combining them needs one engine run over the adopted set.

[2026-09-25: the consumption key now has one; see [Consumption taxes](#consumption-taxes-keyed-on-spending-2026-09-25).]
Still without an outside test: the state and local income and property tax keys, the consumption
key, unemployment insurance and workers' compensation (CBO rounds them too coarsely), income tax by
ethnicity, and any tax figure for the Mexico-born. Blocked: an AEA 2024 paper on credits by
ethnicity (paywall), Florida's 2024 report PDF and Texas's counts of patients who declined to answer.

## Benefits: survey keys against administrative records by ethnicity

The account splits each benefit programme's national dollars by what people report in CPS ASEC 2025.
Under-reporting across the whole survey washes out, because BEA totals are split by shares; under-reporting
by one group does not. The hypothesis tested: people with immigration exposure hide receipt out of
fear, so the keys under-charge the group. Administrative systems record Hispanic ethnicity, not
Mexican origin. The sharpest test (route A) therefore uses the states where most Hispanics are of Mexican origin
(California, Nevada, Arizona, and Texas and New Mexico where usable). There, the survey's reporting rate for Hispanic receipt
relative to other receipt, ρ, applies almost directly to the group. Route B uses national shares;
route C is the linked survey-to-records literature [CALCULATION: `compare.py` → `derived/program_keys.csv`;
positive control reproduces the account's SNAP key share 0.148150; 4 tests pass; the parent's re-run left
all 18 derived files byte-identical].

**Fear-driven under-reporting fails where the dollars are.**
- **SNAP** ($14.3bn charged to the group): no under-reporting. In California, SNAP's quality-control
  records show 44.0% of benefit dollars going to Hispanic participants, against 44.1% in the CPS; over
  the three route-A states ρ is 1.21 (SE 0.13), and 1.05 (0.06) over the 26 states whose records
  pass a validity screen [SOURCE: SNAP QC FY2024 public-use file, snapqcdata.net; CALCULATION:
  `snap_qc.py`, `derived/share_comparisons.csv`].
- **Medicaid coverage** ($116.9bn charged, through a medical-spending key): the CPS reports Hispanic
  coverage at the administrative rate (ρ 1.03 against T-MSIS enrollment in the route-A states).
- **Housing assistance**: over-reported (ρ 1.42–1.62 against HUD's Picture of Subsidized Households);
  the line is a subsidy with zero response, so the main case does not move.
- **Unemployment insurance**: under-reported, ρ 0.71–0.80 against DOL claimant records, matching the
  linked-record literature's 0.72–0.77. +$1.36bn (SE 0.55).
- **WIC**: modestly under-reported, ρ 0.77–0.84 against the FNS participant census. +$0.14bn.
- **TANF**: reported at about the administrative rate within states, but the CPS puts 27% of TANF-type
  dollars in California, where 48% of basic assistance is paid (New York 8% against 19%). +$1.14bn
  (SE 0.58). The literature points the other way on amounts: in seven states outside California,
  Hispanic recipients who report TANF state about twice their administrative amount, a dollar
  capture near 1.6 against whites from small cells [SOURCE: Census SEHSD Working Paper 2018-30,
  Tables 5–6]. If that held in the states used here, the TANF term would shrink; it does not touch
  the California share [SOURCE: ACF TANF characteristics and financial data FY2024; DOL ETA 203 and 5159; FNS WIC
  Participant and Program Characteristics 2022; HUD Picture of Subsidized Households 2024].
- The literature agrees on citizenship: in linked SNAP records, noncitizens under-report no more than
  natives (49% against 49%, net) [SOURCE: Census SEHSD Working Paper 2017-49, Table 3, p. 25].

| Package | Change, $bn | Main case on the September 23 frame, $bn |
|---|---|---|
| Central: administrative state dollars and validated state ethnicity | +2.27 / +2.17 (SE about 1.1) | 205.5–251.8 |
| Route A (Hispanic ≈ Mexican states, ρ applied to the group) | +0.01 / −0.04 | 203.2–249.6 |
| Route B over the states passing the screen | +1.29 / +1.27 | 204.5–250.9 |
| Unknown ethnicity all non-Hispanic / all Hispanic | +0.46 / +0.37 to +6.30 / +6.17 | 203.7–250.0 to 209.5–255.8 |
| Audit package with the central change | +1.8 to +2.3 | about 205–253 |

[CALCULATION: `compare.py` → `derived/line_deltas.json`, `package_se.csv`; `translate.js` →
`derived/main_case_translation.csv`.] Audit row 13 re-imputes the same survey keys; the overlap is
at most $0.4bn. As above, these changes are relative to the adopted main case and are not combined
with the other checks.

**A data defect found on the way.** SNAP's quality-control file cannot be used for national
tabulations by ethnicity; its own codebook "recommend[s] against using RACETHi for national
tabulations" (printed p. 82). Worse than missing codes, some states record Hispanic participants as
not Hispanic. In New Jersey, 2.4% of participants are coded Hispanic against 47% of people in SNAP
households in the ACS, and 0% of participants who live with an undocumented member (77.9% nationally).
Twenty-five states holding 38.6% of SNAP dollars fail the lane's screen. Any national SNAP-by-ethnicity
figure built on this file (a national route gives −$2.8bn here) is an artefact [CALCULATION:
`derived/admin_snap_qc_validity.csv`, `admin_validity.csv`].

Blocked: SSI (SSA publishes no ethnicity), SNAP ethnicity in Texas and New Mexico (64–66% unknown),
Medicaid spending by ethnicity (no administrative publication). School meals were not done.

## Crime: which way the errors lean

Four known problems seemed to push the police-based ratios down: offenders of unknown ethnicity,
lower clearance of homicides with Hispanic victims, jails that under-record Hispanic inmates, and
victims who may not report. One pushed up: subtracting all Hispanics from "White" in arrest tables.
The lane tested each on the NIBRS offending ratios, Hispanic ÷ non-Hispanic white, for Texas and
Arizona in 2022–23: murder 2.30 (1.53 to 3.93 with every unknown offender assigned to one side) and
robbery 4.22. Its positive control reproduces both [CALCULATION: `nibrs_base.py`; all figures here
from `ratio_adjustments.py` → `derived/ratio_adjustments.csv` and `dollar_effects.py` →
`derived/dollar_effects.csv`].

**The offending ratios barely move.**
- Murder stays at 2.30. Allocating unknown offenders by the victim's ethnicity and the incident's
  details (18 methods) gives 2.12–2.42. The low end comes from checking the imputation against arrestees.
  The national homicide reports (SHR) give 2.71–2.91 against their own 2.74.
- Robbery moves from 4.22 to 4.15 once reporting to police is weighed, which cannot be told from
  zero (band 3.65–4.29).
- The reporting hypothesis is false. In the victim survey (NCVS 2012–24), crimes by Hispanic
  offenders are reported to police more often than crimes by non-Hispanic whites (47.7% against
  43.8%), so police data slightly over-show the Hispanic ÷ white ratio.
- The victim survey gives a much lower robbery ratio (1.80). The difference lies in the white
  reference group, not the Hispanic count: police-recorded robbery by non-Hispanic whites in Texas and
  Arizona is low relative to every other group, and NCVS's Hispanic ÷ all-residents ratio (1.11) is
  above NIBRS's (0.92).
- Against all residents, Hispanic offending is at parity for murder (1.00; 0.96–1.02) and 0.92–0.96
  for robbery.
- If the 2020 census undercount of Hispanics (4.99%) carries into the population denominators, both
  ratios fall another 6.5% (murder 2.15, robbery 3.88). Whether it carries was not verified.

**The lean is real in custody and arrest records and in the victim-harm count.**
- Jails: BJS's 2023 jail count records 14.4% Hispanic. Five inmate self-report surveys against same-year
  jail counts imply 19.1% (17.1–20.9%) [SOURCE: BJS *Jail Inmates in 2023*, table 5; survey tables
  saved in the lane]. That moves only the account's BJS check arm (+$1.54bn), not the main case.
- Booking: in Texas and Arizona, 3.8% of offenders recorded as Hispanic in the incident are booked
  as non-Hispanic. Harris County books 38% of them that way; Arizona shows no gap. Carried to the
  national arrest key, which is an inference, the justice line rises **+$0.87bn** (+$0.33–0.95bn).
- Victims' harm, beside the account: BJS's table of offender ethnicity gives Hispanic members of
  mixed offender groups no share [SOURCE: *Criminal Victimization, 2024*, table 13, footnotes b and c].
  At the NIBRS mixed-group fraction (0.498), victims' harm rises from $28.9bn to **$30.9bn**
  (+$2.0bn; 0 to +$4.0bn).
- A sensitivity for how facilities record Hispanic origin in the ACS (+$1.99bn on the prisons key) is
  left as the operator's call.

Everything in this section is Hispanic of any origin, not Mexican origin. NIBRS covers Texas and
Arizona agencies that record offender ethnicity; NCVS is national or regional. The parent's re-run
reproduced the lane's derived files [see ladder 218].

## The proposals together

Run once through the explorer engine on the adopted main case, the school, tax-and-transfer and benefit
proposals give **$215.6–261.0bn** (+$12.35bn / +$11.32bn). Adding the crime lane's booking correction
on the justice key gives **$216.4–261.8bn** (+$13.22bn / +$12.18bn) [CALCULATION:
[`outside_checks_combined_2026_09_24/combine.cjs`](../infra/immigration-fiscal/outside_checks_combined_2026_09_24/README.md)
→ `derived/combined_bands.csv`]. Each change alone reproduces its lane's figure, and the changes add
without interaction. The income-tax gradient is the largest piece (+$13.2–14.1bn), then schools
(+$3.0–3.4bn), benefits (+$2.2bn) and booking (+$0.87bn, a national transfer of a Texas and Arizona
factor), while Treasury's credit shares take off $4.3–4.6bn. Where the benefit lane and CBO's bundle
re-key the same lines (SNAP, WIC, cash assistance), the combination keeps the administrative-records
change; applying both would give $214.9–260.0bn without the booking correction.

This is relative to the adopted main case. The audit package already takes most of the income-tax
and credit corrections (its row 3 and SSN rule), and its rows 3, 6 and 13 overlap these proposals,
so the two cannot be combined by addition; that needs the audit's rows in the engine. Victims' harm
(+$2.0bn, to $30.9bn) sits beside the account and is not in these figures. None of this is adopted.

## Consumption taxes: keyed on spending (2026-09-25)

The account splits four lines by each person's SPM resources per unit member: general sales tax
($602.4bn), selective excise ($371.3bn, of which $100.0bn federal), customs ($83.6bn) and personal
current transfers ($141.1bn), $1,198.3bn in all. The group holds 8.104% of that key, and one point
of it is worth about $12bn [CALCULATION: lane `cps_frame.py` reproduces the stored share]. The key
treats every resource dollar as spent in the United States. Richer households save more, and the
group sits low in the distribution, so the key hands other residents too large a share of these
taxes. Money sent abroad pulls the other way. The main case adopted September 24 is the base here
([lane](../infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md); its engine run with no
edits reproduces $200.875–246.318bn).

**Saving.** Each unit's resources are replaced by its consumption at the same income rank. The BLS
Consumer Expenditure Survey gives consumption per dollar of pre-tax income by decile: 3.18 in the
bottom decile, 0.73 in the sixth and 0.40 in the top [SOURCE: BLS CE Table 1110, 2024]. The 2024
Interview microdata shape the ratio within deciles, and the CPS converts it to a ratio to resources.
The group's share rises to 8.894% (SE 0.098) and the main case falls **$7.7bn** (SE 0.5). Nine
variants (published decile steps, level transport, total spending, taxable-type spending, a capped
bottom decile, family-size and age cells, the CE Mexican-origin residual) give −$6.1bn to −$11.0bn.
Raising the top decile's ratio by 25% or 50%, for CE's known shortfall at the top, gives −$5.6bn and
−$3.8bn [CALCULATION: `consumption_key.py` → `derived/key_specs.csv`].

**Remittances.** Each unit's outflow is its measured sending rate times its earnings, scaled to a
national flow. The rates come from the CPS Unbanked/Underbanked supplement (June 2015 and 2017):
37.3% of Mexico-born householders send money abroad, 11.8% of the second generation, 2.0% of the
third-plus and 1.3% of other natives with no foreign-born member [CALCULATION: `sender_rates.py` →
`derived/sender_rates_pooled.csv`]. Two calibrations bracket the flow:
- Banxico's US corridor less H-2 workers' pay, $58.8bn, cuts the share to 7.845% (+$3.3bn)
  [SOURCE: Banxico SIE CE167, 2024]. To reach it, each expected sending unit must send $20,203 a
  year, 28% of its earnings and 3.3 times the surveyed amount. The corridor therefore carries money
  that the CPS households do not generate at surveyed amounts: from migrants the CPS misses,
  temporary workers outside H-2, business and illicit flows, or under-reported sending. It is the
  upper bound on the group's outflow.
- Surveyed amounts (CEMLA's $380 a month per sender, at FDIC sending rates) give the group's units
  $18.4bn and +$0.9bn; BEA's modelled personal transfers give the same +$0.9bn. This is the lower
  bound.

**Together.** Consumption out of resources net of remittances, calibrated to the corridor as the
brief asked, gives a share of 8.599% and a main case of **$196.8–242.3bn (−$4.1bn)**. With surveyed
remittances the change is −$6.7bn; across the combined variants it runs from −$2.6bn to −$8.4bn.
Both ends move by the same amount, because the four lines carry one target in both allocations
[CALCULATION: `engine_run.cjs` → `derived/engine_summary.json`].

**Outside checks.** Three distributions built without the account agree on the direction:
- **CBO's federal excise by income group (2022).** The current key puts 5.6% of the line on the
  lowest fifth, where CBO puts 10.7%; the corrected key puts 11.1%, and it is within a point of CBO
  in every group except the top 1%. On the $100bn federal part the gap to CBO closes from −$1.3bn to
  +$0.1bn [SOURCE: CBO 61911, researcher Table 12; CALCULATION: `outside.py` →
  `derived/cbo_check.csv`]. Ladder 216's match on federal excise held only because that line is
  small.
- **ITEP, *Who Pays?* 7th edition.** Relative to the middle fifth, the corrected key is within 0.04 of
  ITEP's sales-and-excise gradient in the fourth fifth and the next 15%. It stays flatter at the top
  (0.44 against 0.21 for the top 1%) and steeper below the middle (2.61 against 1.46 in the lowest
  fifth), where resources exceed money income and CE's bottom decile spends 3.2 times its reported
  income. ITEP's rates applied to the account's own base give 9.133% and −$10.3bn [CALCULATION:
  `derived/itep_check.csv`, `itep_keyed_shares.csv`].
- **CE by Hispanic origin.** In the 2024 Interview files, Mexican-origin units consume 1.036 times
  what their income position predicts (SE 0.020), 0.984 with family size and 0.993 with size and
  age. The income-rank model fits them within two standard errors [CALCULATION: `saving.py` →
  `derived/ce_microdata_check.csv`].

CBO's excise gradient spread over all four lines, the September 24 sensitivity above (−$15.2bn),
lies beyond all three, as expected for fuel, tobacco and alcohol taxes.

**What else it touches.** Seven spending lines are keyed partly on resources (economic affairs,
subsidies, housing and community services, recreation). They have zero response in the main case, so
they do not move. Where those services respond (the proportional-reference profile), the same key
change adds $3.4bn of cost and offsets 44% of the saving correction. The September 19 generation
ledger keys sales and excise tax on a flat share of resources and carries the same error; it is named
here, not rerun. If adopted, the account's generation split (ladder 224) and the winners-and-losers
count move with the main case.

**Limits.** The CE-to-CPS transport rests on income rank. The Mexican-origin check classifies units
by the reference person and cannot separate the first generation. The FDIC sending rates date from
2015 and 2017. No source measures what US-born-only sending units send; from a quarter to all of what
other sending units send, it moves the result by less than $0.1bn. The account keys personal current
transfers (fines, fees, donations) on consumption, and the lane corrects that line like the others
without testing the keying.

**Status.** Proposed, not adopted. The choice is the operator's: the combined correction at the
corridor (−$4.1bn), the combined correction at surveyed remittances (−$6.7bn), or the current key.
[CALCULATION: the parent's rerun of `consumption_key.py`, `engine_run.cjs` and the lane's 8 tests
left all 19 derived files byte-identical; shared lanes untouched.]

## Revisions

- 2026-09-24 (later): the operator adopted all four checks with the dataset audit. In one engine run
  CBO's income-tax gradient replaces audit row 3, and the benefit keys replace CBO on SNAP, WIC and
  cash. The pooled-MEPS ratios replace CBO's Medicare gradient, and the booking factor applies to
  the 2024 arrest ratio. The main case is $200.9–246.3bn ([decision](../decisions/2026-09-24-main-case-audit-and-outside-checks.md), ladder 219). The
  figures above stay as computed on the September 23 case. Concept affected: the status of these
  corrections.
- 2026-09-25: added the consumption-key section and table row. The key the September 24 memo listed
  as untested now has an outside test; the saving correction net of remittances would lower the main
  case by $4.1bn (proposed, ladder 225). Concept affected: the consumption tax key.
