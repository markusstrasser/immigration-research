# Yearly and lifetime fiscal results — repaired calculation index

**Latest annual update, 2026-09-20:** The [measured enrollment correction](immigration-four-fiscal-checks-2026-09-20.md)
produces −$259.38bn shared/−$283.20bn personal. Lifetime tables below retain their
pinned earlier age-profile inputs; neither subsequent annual change has been
applied as a flat lifetime shift.

**Later source update, 2026-09-19:** The [Census2024 finance refresh](immigration-macro-reconciliation-2026-09-19.md)
updates the union's annual partial balance to −$234.34bn shared/−$256.26bn
personal. Tables below preserve the earlier pinned profile version. The
[projection tests](immigration-projection-backtest-2026-09-19.md) assess historical
assumptions and composition/exit sensitivities; no lifetime admission forecast
is validated. See the [decision](../decisions/2026-09-19-matched-accounts-and-projection-checks.md).

**Status:** Pinned September 19 calculation release. The annual bookkeeping and age-profile propagation are repaired. This is an **expanded partial fiscal account**, with explicit allocation scenarios, not an exhaustive government account or an identified effect of immigration policy. Earlier $263.22bn, $2,246/household, 89% state/local and flat-adjustment lifetime headlines are superseded. Evidence remains in Git and the original files.

## Annual results

[MODEL OUTPUT] Net receipts minus attributed expenditure, billions of 2024-price dollars per year. Income-year-2024 CPS ASEC 2025 civilian household residents; MEPS 2024 public medical spending; administrative expansion described below. Negative is a deficit. These are resident stocks, not annual inflows. The two allocation columns are different conventions, **not confidence bounds**.

| Resident group | Population, millions | Household-shared balance, $bn/year | Personal-source balance, $bn/year |
|---|---:|---:|---:|
| Mexico-born | 12.221 | −72.46 | −41.93 |
| Mexican second generation | 14.333 | −84.29 | −97.44 |
| Mexican third-plus, self-identified | 14.343 | −60.57 | −99.87 |
| Observed Mexican-origin union | 40.897 | **−217.32** | **−239.24** |
| Third-plus non-Hispanic white reference | 173.054 | −211.31 | −200.05 |
| All natives | 283.672 | −669.22 | −896.32 |

[SOURCE: `infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/age_profiles.csv`, sum `net_total` over bands; shared rows reproduce `waterfall.csv`.]

Personal-source attribution places taxes, cash transfers, payroll and school costs on their reported source/recipient, with direct pupil allocation for school capital and district adjustments. Household-only noncash benefits and indirect taxes retain their documented allocations. Person survey weights mean that moving dollars between family members can change weighted group and national totals; this is disclosed, not normalized away. Personal attribution is the default for lifetime calculations. Both annual conventions remain visible.

The shared-account common-age shortfall for the union is $7,152 per standardized person-year against the third-plus non-Hispanic white reference, or $4,973 against all natives. Those are **comparisons with specified reference profiles**, not absolute costs or the taxes other residents would save under a policy. [SOURCE: `derived/complete_gaps.csv`; the historical filename now denotes expanded-partial coverage.]

## Lifetime results

[MODEL OUTPUT; FRAMING-SENSITIVE] Present values of the **current personal-source age profiles**, conditional survival from the stated starting age, common US-total 2024 mortality, 3% real discounting, 2024-price dollars, zero real growth. No outmigration, fertility or descendants. Broad age bands are held constant within bands; 75+ is extended through the life table, and the open 100+ exposure is discounted at age 100. Starting at 25 describes current residents conditional on reaching 25; it does **not** describe admission at 25. Starting at zero for foreign-born residents is likewise a synthetic profile, not an admission cohort.

| Group and valuation age | Expanded partial profile NPV | With average defense, interest and general-government allocation added |
|---|---:|---:|
| Mexico-born, age 25 | −$56,166 | −$194,855 |
| Second generation, age 0 | −$279,720 | −$437,080 |
| Third-plus self-identified, age 0 | −$225,309 | −$382,669 |
| White reference, age 0 | −$96,210 | −$253,570 |
| White reference, age 25 | +$265,713 | +$127,024 |
| All natives, age 0 | −$146,692 | −$304,052 |
| All natives, age 25 | +$200,160 | +$61,470 |

[SOURCE: `derived/lifetime/period_profiles.csv`, `primary=True`, `real_discount_rate=0.03`. The last column adds item F, net of TRICARE already priced, using the same discounted expected person-years. It still does not add every omitted program.]

The public-goods convention matters materially. It adds $5,175 per resident-year and about $157,360 to the age-zero 3% NPV cost. The discount rate also matters: Mexico-born age-25 balances are −$395,504 at 0%, −$116,074 at 2%, −$56,166 at 3%, and −$639 at 5%, before the extra F allocation. The second and third generations' age-25 balances change sign across this rate range. **Do not compress these scenarios into a universal lifetime price.** The full 768-row table also carries shared allocation, partial coverage, mortality proxies and a truncation-at-83 sensitivity.

The earlier child-versus-adult “birth subsidy” inference remains withdrawn. These results do not estimate the fiscal effect of an additional birth, admission or descendant. A projected lifetime requires assumptions about future earnings, policies, migration and cohort change that current cross-sectional profiles cannot establish.

## Accounting repairs and source ownership

| Component | Repair | Primary evidence / implementation |
|---|---|---|
| State/local service fees | Credit $177.307535bn nominal-2022 mapped fees, repriced with the same factor as the corresponding services. Do not credit education/hospital charges, mixed other charges or all miscellaneous revenue against G. | Census 2022 Table 1, lines 28–36; `consolidation.census_finance` |
| Transportation grants | Net $67.672bn of named highway/airport/port programs from R400 while retaining final service spending in G. Transit remains in R because G excludes utility transit. | OMB FY2027 account database, FY2024 actual; explicit row allowlist |
| Housing grants | Net only $8.659bn physical public-housing programs. Reject the broader $44.499bn candidate: direct renter aid/HOME can be welfare outside G. | Census classification manual, code 50; explicit OMB program rows |
| Justice and prisons | N owns institutional corrections; remove subfunction 753 from R. Net $6.264bn noncorrectional justice grants whose delivered services are represented by G/N. E is no longer added to R's justice outlays. | OMB program/subfunction mapping; E appropriations are not additional outlays |
| Veterans | Subtract the **actual weighted VA cash already in the base** before allocating the remaining nonmedical VA budget. | CPS VET_VAL; OMB 700 minus 703; allocation-specific conservation identity |
| Health | Replace the CY2023 Medicaid subtraction with FY2024 Medicaid $617.517bn and CHIP $19.449bn. Net already-priced TRICARE from the alternative defense allocation. | OMB Table 12.3; MEPS public-payer definitions |
| Transfer reporting | Apply the Social Security admin/survey ratio in the same direction as the other programs; remove the asymmetric rule that discarded only upward SS adjustments. | Existing sourced coverage parameters; the ratios remain historical transport assumptions |
| State coverage | Additional mixed-year state coverage appropriations are diagnostic, not extra 2024 central spending. | Program/year and overlap limitations in the parameter file |
| National comparator | Remove federal-to-state/local financing once. Classify lunch/district reversals as reductions of spending; classify fees as receipts. | Census direct spending includes grant financing; mixed-year comparator explicitly labeled |
| Lifetime | Export actual component dollars by age and allocation, then apply conditional person-years and real discounting. Remove group-wide flat shifts and unequal-date terminal-value comparisons. | Annual export and NVSS life tables; deterministic identities |

Primary source retrieval: [Census 2022 table](https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx), [Census definitions](https://www.census.gov/programs-surveys/state/about/glossary.html), [OMB account outlays](https://www.whitehouse.gov/wp-content/uploads/2026/04/outlays_fy2027.xlsx), [OMB grants by function](https://www.whitehouse.gov/wp-content/uploads/2026/04/hist12z3_fy2027.xlsx), [AHRQ payer scope](https://www.meps.ahrq.gov/data_files/publications/st456/stat456.shtml). Exact workbook hashes, rows and download URLs are enforced by `consolidation.py`; annual and lifetime audit files fingerprint their calculation inputs and code.

## Remaining limits that affect interpretation

- Grant netting is a **program/function matching scenario**, not an exact recipient-and-year reconciliation. Some federal program totals include territorial/tribal recipients, while G is Census 2022 spending repriced to 2024. Unmapped program overlaps and receipts remain. The national comparator excludes parts of enterprise/insurance finance and uses mismatched fiscal periods. Passing its arithmetic gates does not certify a complete fiscal account.
- Average service costs, district assignment, tax incidence, medical donor transport and historical underreporting multipliers are modeling assumptions. Public-good zeroes are another convention. The 63 admissible arm combinations are not all possible fiscal models, and their range is not a confidence interval.
- Institutional N is an external ACS cost proxy divided by CPS household-resident age populations, not an observed institutional transition cost. Generation splits and nursing/prison classification remain assumptions. CPS sampling errors do not cover all source and model uncertainty; lifetime scenarios have no claimed joint confidence interval.
- Native-household financing is imposed and the native denominator overlaps the US-born target groups. Federal prison financing is unidentified by this ACS proxy: regenerated 0/1 financing runs bound that assignment. The old 89% and $2,246 figures are not current findings.
- The Social Security money's-worth adjustment is disabled. A whole-career PV benefit/tax ratio does not identify annual entitlement accrual. Cash Social Security is already counted.
- Homicide consumers now use current profiles and survival; their family-benefit timing and expected-case interpretation remain limited. Arrival-window outputs are explicitly **partial plus G/K/X/R**, not the entire expanded account.

## Reproduction and checks

Run `consolidation.py --fetch`, `absolute_ledger.py --params params/params.json`, `check_gates.py`, then `lifetime.py` in the annual lane, using repository-root paths and `uv run --no-project python3`. See [lifetime interface](../infra/immigration-fiscal/ledger_absolute_2026_09_17/LIFETIME.md). The raw CPS/MEPS/NVSS/Census caches remain prerequisites.

Executed: **17 focused tests; 54 annual gates; 768 lifetime scenarios; annual/profile component and group sum checks; incidence reconstruction at both correctional financing endpoints; real-rate debt, homicide and arrival-window regeneration.** Code review identified an SS incidence omission, missing source fingerprints, federal-prison payer ambiguity and an overstated TRICARE residual line; each was repaired or made an explicit required financing sensitivity. Current consumers reject stale or altered manifests.

## Revisions

2026-09-19: [Program ownership and period-profile decision](../decisions/2026-09-19-fiscal-program-ownership-and-period-profiles.md). Replaces the affected annual, financing and lifetime headlines while preserving historical evidence. This file is a calculation index, not essay text.

2026-09-19, later: [Matched accounts and projection checks](../decisions/2026-09-19-matched-accounts-and-projection-checks.md)
versions the observed2024 refresh separately and retains these profiles for
comparisons. The older annual source vintage retained here is no longer the latest.

2026-09-20: [Measured enrollment and residual boundaries](../decisions/2026-09-20-measured-enrollment-and-residual-boundaries.md)
versions the new annual school correction separately. Lifetime age profiles remain
pinned; the new annual total cannot be propagated as a flat lifetime shift.
