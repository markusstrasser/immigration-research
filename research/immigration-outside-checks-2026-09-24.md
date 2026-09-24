# Outside checks on the account's shares

Date: 2026-09-24. [MODEL / FRAMING-SENSITIVE] Proposed corrections only. The main case stays as
adopted until the operator decides, and narrative authorship remains the operator's.

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
| Direction of the errors in the crime ratios | `crime_ratio_direction_2026_09_24` | running |

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
| Adopted main case | 87.14–113.96 | 203.21–249.64 | — |
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
| Adopted main case | 203.21–249.64 | — |
| With the CBO keys (Medicaid excluded) and Treasury's credit shares | 209.2–254.8 | +6.0 / +5.1 (SE about 3.8 / 3.5) |
| Audit package with the same | 203.6–250.6 | +0.7 / −0.5, before rows 2 and 13 shrink the income-tax increment |

[CALCULATION: `derived/cbo_main_case.csv`, `ota_main_case.csv`; 203.207 + 10.560 − 4.554 and
249.640 + 9.444 − 4.313.] These changes are relative to the adopted main case and are not combined
with the school correction above. Combining them needs one engine run over the adopted set.

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
  (SE 0.58) [SOURCE: ACF TANF characteristics and financial data FY2024; DOL ETA 203 and 5159; FNS WIC
  Participant and Program Characteristics 2022; HUD Picture of Subsidized Households 2024].
- The literature agrees on citizenship: in linked SNAP records, noncitizens under-report no more than
  natives (49% against 49%, net) [SOURCE: Census SEHSD Working Paper 2017-49, Table 3, p. 25].

| Package | Change, $bn | Main case, $bn |
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
