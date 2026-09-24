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
| Benefit keys against administrative records by ethnicity | `admin_benefit_keys_2026_09_24` | running |
| Taxes and transfers against CBO, Treasury, IRS and state hospital records | `external_benchmarks_2026_09_24` | running |
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
