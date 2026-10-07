# Yearly and lifetime fiscal results — repaired calculation index

**Item T, 2026-10-08:** The tables below are restated on the ledger's current outputs. Its expanded
account adds the income tax the survey misses, placed on the main case's keys (item T;
[decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)); the lifetime file's
partial-coverage rows keep taxes as the survey reports them.

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

[MODEL OUTPUT] Net receipts minus attributed expenditure, billions of 2024-price dollars per year. Income-year-2024 CPS ASEC 2025 civilian household residents; MEPS 2024 public medical spending; administrative expansion described below; the income tax the survey misses (item T). Negative is a deficit. These are resident stocks, not annual inflows. The two allocation columns are different conventions, **not confidence bounds**.

| Resident group | Population, millions | Household-shared balance, $bn/year | Personal-source balance, $bn/year |
|---|---:|---:|---:|
| Mexico-born | 12.221 | −68.84 | −37.72 |
| Mexican second generation | 14.333 | −81.79 | −91.56 |
| Mexican third-plus, self-identified | 14.343 | −52.89 | −94.66 |
| Observed Mexican-origin union | 40.897 | **−203.52** | **−223.94** |
| Third-plus non-Hispanic white reference | 173.054 | +51.83 | +85.79 |
| All natives | 283.672 | −308.63 | −510.97 |

[SOURCE: `infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/age_profiles.csv`, sum `net_total` over bands; shared rows reproduce `waterfall.csv`.]

Personal-source attribution places taxes, cash transfers, payroll and school costs on their reported source/recipient, with direct pupil allocation for school capital and district adjustments. Household-only noncash benefits and indirect taxes retain their documented allocations. Person survey weights mean that moving dollars between family members can change weighted group and national totals; this is disclosed, not normalized away. Personal attribution is the default for lifetime calculations. Both annual conventions remain visible.

The shared-account common-age shortfall for the union is $8,306 per standardized person-year against the third-plus non-Hispanic white reference, or $5,935 against all natives. Those are **comparisons with specified reference profiles**, not absolute costs or the taxes other residents would save under a policy. [SOURCE: `derived/complete_gaps.csv`; the historical filename now denotes expanded-partial coverage.]

## Lifetime results

[MODEL OUTPUT; FRAMING-SENSITIVE] Present values of the **current personal-source age profiles**, conditional survival from the stated starting age, common US-total 2024 mortality, 3% real discounting, 2024-price dollars, zero real growth. No outmigration, fertility or descendants. Broad age bands are held constant within bands; 75+ is extended through the life table, and the open 100+ exposure is discounted at age 100. Starting at 25 describes current residents conditional on reaching 25; it does **not** describe admission at 25. Starting at zero for foreign-born residents is likewise a synthetic profile, not an admission cohort.

| Group and valuation age | Expanded partial profile NPV | With average defense, interest and general-government allocation added |
|---|---:|---:|
| Mexico-born, age 25 | −$41,058 | −$179,747 |
| Second generation, age 0 | −$266,917 | −$424,278 |
| Third-plus self-identified, age 0 | −$215,392 | −$372,752 |
| White reference, age 0 | −$68,163 | −$225,523 |
| White reference, age 25 | +$323,794 | +$185,105 |
| All natives, age 0 | −$120,194 | −$277,554 |
| All natives, age 25 | +$253,069 | +$114,380 |

[SOURCE: `derived/lifetime/period_profiles.csv`, `primary=True`, `real_discount_rate=0.03`. The last column adds item F, net of TRICARE already priced, using the same discounted expected person-years. It still does not add every omitted program.]

The public-goods convention matters materially. It adds $5,175 per resident-year and about $157,360 to the age-zero 3% NPV cost. The discount rate also matters: Mexico-born age-25 balances are −$375,350 at 0%, −$99,630 at 2%, −$41,058 at 3%, and +$12,435 at 5%, before the extra F allocation. The age-25 balances of the Mexico-born and of the second and third generations all change sign across this rate range. **Do not compress these scenarios into a universal lifetime price.** The full 768-row table also carries shared allocation, partial coverage, mortality proxies and a truncation-at-83 sensitivity.

The earlier child-versus-adult “birth subsidy” inference remains withdrawn. These results do not estimate the fiscal effect of an additional birth, admission or descendant. A projected lifetime requires assumptions about future earnings, policies, migration and cohort change that current cross-sectional profiles cannot establish.

## Same rates under different age structures

[DERIVATION; FRAMING-SENSITIVE; added 2026-09-20] Current age-specific expanded balances are held fixed and only the age structure varies. Net dollars per person per year, household-shared allocation; the gap against the white reference **under the same structure** is in parentheses. Each gap equals the printed balance less the printed white balance; to keep that true, six cells are rounded away from the nearest dollar, by under $1 each.

| Age structure applied | White reference | Mexico-born | Second generation | Third-plus self-identified | Union |
|---|---:|---:|---:|---:|---:|
| Each group's own ages today | +299 | −5,633 (−5,932) | −5,706 (−6,005) | −3,688 (−3,987) | −4,977 (−5,276) |
| White reference's ages today | +299 | −8,491 (−8,790) | −8,121 (−8,420) | −6,740 (−7,039) | −7,937 (−8,236) |
| Union's ages today | +4,852 | −5,957 (−10,809) | −5,616 (−10,468) | −2,897 (−7,749) | −4,977 (−9,829) |
| Stationary life course | +387 | −8,389 (−8,776) | −8,107 (−8,494) | −6,413 (−6,800) | −7,767 (−8,154) |

The stationary row weights ages by US-total 2024 life-table person-years (22.6% under 18, 20.9% aged 65+; the white reference today is 18.0%/23.4%, the union 29.6%/7.7%). It equals the 0% period-profile NPV divided by its 78.97 person-years, so it puts both populations through a whole life course instead of ageing one toward the other. The eight-band white-age gaps sit within 2% of the published finer-cell gaps above. Personal-source stationary gaps are −8,608, −7,322, −6,405 and −7,801.

[INFERENCE] The union's young age structure is worth about $4,550 per person a year: the white reference would run +$4,852 at the union's ages against +$299 at its own. The raw −$5,276 difference therefore understates every same-age comparison (−$8,154 to −$9,829). Under the stationary structure the union's gap is −$10,588 of receipts against +$2,434 of lower spending; the second generation's lower-spending offset is only +$822.

[DERIVATION] In dollars at the observed 40.9m headcount, giving the union the white reference's ages moves its shared balance from −$203.5bn to **−$324.6bn** (−$121.1bn); personal-source, −$223.9bn to −$321.9bn. The shared change is cash transfers including Social Security −$70.2bn, public medical −$80.2bn, institutions −$7.9bn, rest of federal −$7.4bn, K-12 +$30.9bn, all taxes +$12.8bn, noncash aid +$1.4bn and state and local services and capital −$0.5bn. Within institutions, under-65 cost falls $1.3bn and 65+ nursing cost rises $9.2bn (item N by band); police and courts are per capita here and do not vary with age, and victim costs are outside a fiscal account. The same number of white-reference residents at those ages runs +$12.2bn, so the like-for-like difference is −$336.8bn against −$215.7bn when each group keeps its own ages. The parts add to the printed totals; three of these figures (the −$121.1bn change, rest of federal and the −$215.7bn) are rounded away from the nearest $0.1bn, by under $0.1bn each. [SOURCE: `derived/age_normalizations_by_category.csv`.]

This is a statement about age composition, not a forecast. Old-age rates for the second and third-plus generations come from 0.52m and 1.00m residents aged 65+ born before about 1960; schooling and earnings of younger cohorts, policy, outmigration and descendants are held out, defense/interest/general government stay at zero, and the later annual corrections are not propagated into these profiles. The [projection back-tests](immigration-projection-backtest-2026-09-19.md) show how sensitive cohort projections are to those assumptions. [SOURCE: `infra/immigration-fiscal/ledger_absolute_2026_09_17/age_normalizations.py` → `derived/age_normalizations.csv`; the script fails unless its own-age, stationary and white-age rows reproduce the annual, period-profile and published-gap exports.]

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

2026-09-20, age structures: added the four-structure comparison from the existing
age-profile and period-profile exports. No existing value changes. The ledger was
rebuilt after the data-root refactor changed two fingerprinted source files; all ten
data outputs were byte-identical and only `audit.json` fingerprints moved.

2026-09-20: [Measured enrollment and residual boundaries](../decisions/2026-09-20-measured-enrollment-and-residual-boundaries.md)
versions the new annual school correction separately. Lifetime age profiles remain
pinned; the new annual total cannot be propagated as a flat lifetime shift.

2026-09-22: [MCBS 2023 check](immigration-elderly-medical-by-ethnicity-2026-09-22.md) bounds
the missing ethnicity dimension of the 65+ community public medical transport (age and US
birth only) at −3% to +56% of the union's −$43.6bn 65+ cell: up to about $24bn more cost and
no reduction (ladder 173). Institutional item N is not bounded by it. No value changes; the
re-aged and lifetime 65+ cells inherit the bound.

2026-09-22, later: the [MEPS Mexican-origin check](immigration-mexican-origin-medical-transport-check-2026-09-22.md)
on the transport's own donor file gives 0.89 (CI 0.61–1.18) at 65+ and 0.69 (SE 0.10) at
18–64 against the all-donor cell means, so the two files together leave the 65+ ethnicity
dimension unsigned (about −40% to +56%) and the earlier "no reduction" clause is withdrawn;
under 65 the direction is a smaller cost. No value changes (ladder 175).

2026-10-08: restated the annual, lifetime and age-structure tables and their prose on the
ledger's current outputs, because the white-reference ledger's expanded account now charges the
income tax the survey misses on the main case's keys (item T;
[decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)): union −$217.32bn → −$203.52bn
shared and −$239.24bn → −$223.94bn personal; white reference −$211.31bn → +$51.83bn shared;
common-age union gap against whites $7,152 → $8,306; Mexico-born age-25 NPV at 3% −$56,166 →
−$41,058, positive at 5% (+$12,435); white-age union gap −$7,082 → −$8,236; re-aged shared balance
−$339.6bn → −$324.6bn. The re-aging sentence also gains the noncash and state-local categories it
left out, so its parts add, and its under-65 institutions fall reads $1.3bn (the file holds $1.34bn
before and after item T). Concept affected: expanded-account annual and lifetime balances against
the white reference.
