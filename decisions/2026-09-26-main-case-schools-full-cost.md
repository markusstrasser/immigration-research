---
date: 2026-09-26
concepts: [headline, service-response, schools, cost-allocation]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md
  - revises: decisions/2026-09-20-category-service-response.md
  - revises: decisions/2026-09-25-school-dilution-priced-beside.md
evidence: infra/immigration-fiscal/main_case_schools_full_2026_09_26/RESULT.md
---

# 2026-09-26: The main case charges schools at their full average cost per pupil

## Context

The operator asked whether the marginal pupil can really be cheap at the scale of this account:
"I often see economists think that 'ohh one more student ... so class goes from 25 to 26 ... no need
to build classrooms ... ad infinitum'".

The main case charged schools at CBO's year-to-year coefficients:
- 0.63 for growth and 0.66 for decline;
- read over a removal as 0.6522/0.6813 since the finite-removal decision earlier the same day.

The group's 8.5 million pupils are 17.5% of public-school pupils. Absorbing them with no extra
teachers or rooms would mean classes of about 30 instead of 25.

The repo's evidence, ordered by horizon:
- **Next year's budget:** 0.63/0.66 (CBO's state panel of growth rates).
- **Same districts, 2000–2019:** 0.735 with districts counted equally, 0.836 weighted by pupils.
- **Across 2019 districts:** 0.945 and 1.004.
- **Across states:** 0.973.

Asked "what's the most intellectually and realistically honest", the answer was:
- full average cost at the centre;
- 0.836 as the low side;
- CBO's figures only for a one-year budget scenario.

The operator answered "well if we believe it ... then yes let's change the main case" (22:39 JST).
He added "but we don't have to update all the uis ... we're still researching .. i guess".

## Alternatives considered

1. **Keep CBO's coefficients, read over the removal.**
   - The account describes one year of a population present for decades. A year-to-year budget
     association answers a different question.
   - It implies that every pupil in the country gets about 6% less spent on them, permanently.
   - The data show no sign of that where the group's pupils enrol: those districts spend 2.5% more
     per pupil than their state averages.
   - Kept as the one-year scenario.
2. **The within-district 0.836 at the centre.**
   - It is the most direct measured response.
   - Part of its gap to 1 is plausibly lag, since the 2010 wave falls in the post-recession cuts.
     Another part is attenuation from noisy enrollment counts.
   - Some of the gap may be lasting dilution, which is a cost to other pupils, not a saving.
   - Kept as the low side.
3. **Full average cost, a response of 1.** Chosen.
   - Spending is proportional to pupils across districts and states.
   - Above 1,000 pupils a district has no fixed costs left to spread, and the big districts show
     slight diseconomies (1.028).
   - The main case already takes general administration from cross-state scale estimates, and the
     same estimate for K–12 is 0.97–1.00.
   - The National Academies (2017) treat schooling as roughly proportional to pupils.
4. **Above 1.** Not priced; recorded as an unpriced upside. The reasons it could be:
   - new seats at today's construction cost (the account carries depreciation on existing buildings
     only);
   - English-learner and poverty weights;
   - Mariel's sustained +26% in Miami school-district spending.

## Decision

- **The main case is $258.5–292.0bn** a year (`main_case_schools_full_2026_09_26`), up from
  $200.9–245.7bn (+$57.6bn / +$46.3bn). Only the school response changes; general government,
  row 8 and the consumption key stay as adopted earlier today.
- **Low side: $233.9–269.6bn.** This reads 0.836 over the removal (response 0.8489), the way the
  finite-removal decision reads every elasticity. Taken as the response, 0.836 gives $231.8–267.8bn.
- **One-year scenario: the September 26 case, $200.9–245.7bn.** It answers how next year's budget
  would move after a sudden change.
- **The outer range is $198–324bn.** It adds a school-response component (−$26.7bn / −$24.2bn,
  upper side 0). The finite-removal component keeps general government only, because at a response
  of 1 schools save 1 under any functional form.
- **School dilution** ($16.1bn beside the account, decision 2026-09-25) no longer applies to the main
  case, since nothing is left unfunded. It applies to the lower-response scenarios. The unfunded
  school cost is $46–58bn a year in the one-year scenario and $22–25bn at the low side.
- **The sign break-even is unchanged at 5.8–17.0%.** That test moves every service at one common
  share.
- **The "CBO-informed" label** now covers CBO's tax-incidence rules and its category rule for which
  budgets respond. The school response is no longer CBO's.
- **Scope.** The research record and the consumer lanes move to this case; the peer session
  immigration-research-1c edits the shared documents and repoints the lanes. The explorer, the
  figures page and the prototypes stay on earlier cases until the operator asks.

## Evidence

- `research/immigration-service-scaling-test-2026-09-20.md`:
  - across districts, 1.004 [0.991, 1.017] pupil-weighted;
  - by district size, 0.849 / 0.986 / 1.028;
  - within districts, 0.735 / 0.836;
  - across states, K–12 0.973.
- `notes/immigration-service-response-external-evidence-2026-09-20.md`:
  - CBO June 2025: one point faster enrollment growth goes with per-pupil spending growth 0.37 points
    lower (0.34 higher for declines);
  - National Academies 2017, chapter 8;
  - GAO-04-733's capacity approach;
  - St. Clair's Mariel study.
- `infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md`: the group's districts
  spend 2.5% more per pupil than their state averages.
- `infra/immigration-fiscal/main_case_schools_full_2026_09_26/RESULT.md`. The gates reproduce the
  September 26 case, its payload and its profiles. They also check:
  - the school option equals editing the specifications directly;
  - the proportional reference does not move;
  - the payload's edits are unchanged.

## Revisit if

- **Evidence for a lower response.** A design follows enrollment shocks in districts with unchanged
  boundaries for ten years or more. It finds per-pupil spending permanently lower while staffing and
  outcomes hold up.
- **Evidence for a higher response.** New-seat capital costs or need weights are priced.
- **A different question.** The account moves from a yearly snapshot to a removal path. The one-year
  response then governs the first years.

## Supersedes

None. It refines the finite-removal decision of the same day: its school part is replaced, and its
general-government part stands. It revises the school coefficient of the 2026-09-20 category-response
decision. It limits the 2026-09-25 dilution decision to responses below 1.
