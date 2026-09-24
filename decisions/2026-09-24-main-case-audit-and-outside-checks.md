---
date: 2026-09-24
concepts: [headline, dataset-audit, cost-allocation, tax-keys, medical-costs, outside-benchmarks, care-benefits]
supersedes: []
relations:
  - refines: decisions/2026-09-23-main-case-general-government-and-use-keys.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/main_case_2026_09_24/RESULT.md
---

# 2026-09-24: The main case takes the dataset audit, the pooled medical figure, care, shelter and the outside checks

## Context

Two sets of findings were pending against the adopted $203.2–249.6bn main case.

The first was the dataset audit (September 23–24, ladders 204 and 208–210). It found defects in the
account's inputs that run both ways and nearly cancel:
- the Census tax model treats every respondent as a legal, fully compliant filer;
- the CPS fill-ins give the group too much income;
- ACA premium credits are keyed as EITC;
- Medicaid long-term care is keyed by a community-only survey.

The second was the four outside checks (September 24, ladders 215–218). They tested the account's
shares against CBO's income distribution, Treasury's EITC shares, administrative benefit records,
where the group's pupils enroll, and crime-record errors.

Separate lanes priced the pooled-MEPS medical ratios, the care and household-service gains, migrant
shelter keying and the legacy of past deficits. The operator was asked six questions and answered
"1 ok 2 why hold? 3 ok 4 okk 5 ok 6 ok".

I had recommended holding decision 2 because of the MCBS–MEPS conflict at 65+. Sized on the
account, that conflict moves the medical figure $1.4bn when the two surveys are weighted by
precision, and $11.8bn only if MCBS is taken as the truth. Holding the figure for a conflicting
instrument was also the flaw I had accepted in the crime booking factor. I flipped to adopt, and
the operator answered "ok".

## Alternatives considered

1. **Keep the September 23 case and report the audit and checks beside it.** The account would keep
   charging the group premium credits it cannot receive, nursing-home dollars it does not use, and
   taxes a status-blind model assigns. A known key error would stay in the headline.
2. **Add the lanes' published figures together.** This gives $201.3–246.9bn. But the audit's row 3
   and CBO's income-tax gradient fix the same defect, and CBO and the benefit lane re-key the same
   lines. Several ratio corrections also act on keys the tax records already cut. Addition would
   double count by construction.
3. **One engine run with written combining rules** (selected). Where two measurements cover the
   same dollars, the more direct one wins. Ratio corrections scale with the tax records' change to
   the same key. Replacement corrections set the charge on named dollars.

## Decision

The main case is **$200.9–246.3bn a year** (low end shared allocation, high end personal), from
`main_case_2026_09_24/main_case.cjs`. It contains:

- **Decision 1:** the audit's tax records (rows 2, 13 and 4 and the state-aware status flag), audit
  row 1, audit row 6 run through the engine, audit row 7, and rows 8–10 with the small items.
- **Decision 2:** the pooled-MEPS ethnicity ratios with long-term care charged by use, in place of
  audit row 5. Its range runs from −21.1 to −5.8, the upper end set by MCBS.
- **Decision 3:** care and household services, −$4.15bn. It moves from the benefits beside the
  account into the account.
- **Decision 5:** shelter keying, −$0.5bn.
- **Decision 6:** CBO's income gradients (replacing audit row 3; SNAP, WIC, cash, Medicaid and
  Medicare left to the direct measurements), Treasury's EITC shares over the audit's SSN rule, the
  administrative benefit keys, schools priced where the group enrolls, and the booking correction
  on the 2024 arrest ratio.

**Decision 4:** the debt legacy ($30.5–38.9bn) stays beside the account. So do crime victims' harm
($30.9bn with the mixed-group correction) and audit rows 11 and 12.

The range is **$172–276bn** with every component at its extreme in the same direction, or about
$189–260bn with the spreads combined as independent. No combination changes the sign.

## Evidence

- [`main_case_2026_09_24/RESULT.md`](../infra/immigration-fiscal/main_case_2026_09_24/RESULT.md). With
  no change it reproduces the September 23 case to 1e-4, and each change alone reproduces its lane's
  published figure.
- Audit: [`dataset_integrity_2026_09_23/README.md`](../infra/immigration-fiscal/dataset_integrity_2026_09_23/README.md).
- Outside checks: [memo](../research/immigration-outside-checks-2026-09-24.md).
- Medical: [`medical_ethnicity_pooled_2026_09_23`](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md)
  and [`ltss_share_2026_09_23`](../infra/immigration-fiscal/ltss_share_2026_09_23/RESULT.md).
- Care: [`care_household_services_2026_09_23`](../infra/immigration-fiscal/care_household_services_2026_09_23/RESULT.md).
- Shelter: [`migrant_shelter_costs_2026_09_23`](../infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/RESULT.md).

## Revisit if

- Linked administrative earnings show whether the group's CPS nonrespondents resemble its
  respondents (audit row 13). The fill-in method moves the case ±$3.2bn; with no fill-in
  correction it is $193.1–237.6bn.
- A second MCBS year, or Medicare claims by ethnicity, settles the 65+ ratio (up to +$11.5bn).
- IRS SOI tables by state and AGI, crossed with ACS composition, test the group's share of top-bracket
  income tax (audit row 3 and CBO's gradient).
- The on-books share of unauthorized earnings for 2024 is measured (audit row 2, about ±$3bn).

## Supersedes

None. It refines the September 23 main-case decision, whose general-government response and use
keys stay in force.
