# Main case: schools at their full average cost per pupil

**Verdict:** Charging the group's pupils at the full average cost per pupil, a school response of 1,
moves the main case from $200.9–245.7bn to **$258.5–292.0bn** a year (+$57.6bn / +$46.3bn). The
low side reads the within-district elasticity 0.836 over the removal (response 0.8489) and gives
$233.9–269.6bn. The September 26 case stays as the one-year budget scenario. The outer range is
$198–324bn.
[CALCULATION: `main_case.cjs` → `derived/`; every gate passes; a second run is byte-identical]

Adopted by the operator on 2026-09-26 at 22:39 JST: "well if we believe it ... then yes let's change
the main case". Decision: [`decisions/2026-09-26-main-case-schools-full-cost.md`](../../../decisions/2026-09-26-main-case-schools-full-cost.md).
Lane run by claude-opus-5-5[1m], session f5e074c6, on the September 26 package (199582e).

## What changed

Only the school response changed. Before, it was 0.6522/0.6813: CBO's year-to-year coefficients 0.63/0.66,
read over a removal of the group's 17.5% of pupils. Now it is 1. Everything else in the September 26
case stays:
- general government at 0.6000/0.8504;
- audit row 8 at 0.949;
- the consumption key.

The payload's lines and edits equal September 26's (gated deep-equal); `meta.responses.school` is
1/1 with its rule.

## Why a response of 1

The account is one year of a population present for decades, so it asks what a school system sized
for the group's pupils costs. It does not ask how next year's budget moves. The repo's evidence,
ordered by horizon:

| Horizon | Spending rise per 1% more pupils | Source |
|---|---|---|
| Next year's budget, within a state | 0.63 (growth) / 0.66 (decline) | CBO, June 2025, state panel 1999–2000 to 2019–20 |
| Same districts, 2000/2010/2019 | 0.735 (districts equal) / 0.836 (pupil-weighted) | [scaling test](../../../research/immigration-service-scaling-test-2026-09-20.md) |
| Across districts, 2019 | 0.945 (districts equal) / 1.004 (pupil-weighted) | same |
| Across states, K–12 | 0.973 | same |

Across 2019 districts the slope is 0.849 below 1,000 pupils, 0.986 from 1,000 to 9,999 and 1.028 above
10,000. The only economies are fixed costs in small districts. Many of the group's pupils are in the largest
districts: Los Angeles, Chicago and Clark County alone hold about 410,000 of them
(`school_cost_where_enrolled_2026_09_24/derived/top_districts.csv`).
[SOURCE: `notes/immigration-service-response-external-evidence-2026-09-20.md` for CBO, NAS 2017, GAO
and St. Clair; ESTIMATES: scaling test]

## Results, $bn a year, everyone else worse off

| Case | Low end | High end |
|---|---|---|
| One year: the September 26 case (school 0.6522/0.6813) | 200.92 | 245.69 |
| Low side: 0.836 read over the removal (0.8489) | 233.92 | 269.59 |
| 0.836 taken as the response | 231.76 | 267.75 |
| **Adopted: full average cost (1)** | **258.49** | **291.95** |
| Non-school education fixed | 204.78 | 265.81 |
| Proportional reference (charged schools at 1 already; unchanged) | 301.29 | 334.75 |
| No fill-in correction | 250.73 | 283.27 |
| Audit row 3 instead of CBO's income tax | 253.83 | 288.75 |
| Uncorrected model at the adopted responses | 265.59 | 298.68 |

[DATA: `derived/main_case_bands.csv`]

## The school line

At full cost the school line is $138.7bn at the case's low end and $172.5bn at its high end. The low end
is specification 48 (shared allocation, school share of education 0.715); the high end is specification
11 (personal, 0.865). Both fill-in methods agree.

At a fixed specification the cost is linear in its school response, so a response r leaves (1 − r) of
the line unfunded. At each scenario's own band ends, the part left unfunded is:
- one-year scenario (specifications 56/7): $58.4bn at the low end and $45.4bn at the high end;
- low side (56/3): $25.4bn and $21.6bn;
- 0.836 taken as the response: $27.5bn and $23.4bn.

The case's reported change from the one-year scenario, +$57.6bn / +$46.3bn, is a move of band ends. It
includes the switch of end specification (−$0.8bn / +$0.8bn). At a response of 1 nothing is unfunded.

The school-dilution figure
([decision 2026-09-25](../../../decisions/2026-09-25-school-dilution-priced-beside.md), $16.1bn beside
the account) therefore no longer applies to the main case. It belongs to the lower-response scenarios.
[DATA: `derived/summary.json` → `school`]

## Range

Every component at its extreme in the same direction gives **$197.8–324.3bn** (low end 197.8–291.3,
high end 234.3–324.3). Combined in quadrature: $228.8–305.8bn. The components are September 26's,
evaluated on the new case, with two changes:
- **Finite removal** keeps general government's functional form only (−$0.37 / −$0.39bn). At a
  response of 1, schools save 1 under any functional form or pupil share.
- **School response** is new: −$26.7bn / −$24.2bn, the low side taken as the response. No response
  above 1 is priced, so its upper side is 0 and the range is asymmetric by construction. Unpriced
  upward pressures: new seats at today's construction cost (the account carries depreciation on
  existing buildings only), English-learner and poverty weights, and Mariel's sustained +26% in
  Miami school spending (author's draft). [FRAMING-SENSITIVE]

[DATA: `derived/components.csv`]

## Unchanged

- **Sign break-even: 5.8–17.0%.** That test moves every service, schools included, at one common
  share, so the school response does not enter (`main_case_2026_09_26/derived/sign_reversal.csv`).
- **The group's receipts** (gated).
- **The payload's edits** (gated).

## For consumers

- **`derived/corrections.json`.** Same lines and edits as September 26. Set the responses from
  `meta.responses`: school 1/1 and general government 0.6000/0.8504. The payload with September 26's
  school responses is the September 26 case, not this one.
- **`derived/main_case_bands.csv`.**
  - Main profile variants: `adopted_2026_09_23`, `adopted_2026_09_24`, `adopted_2026_09_26` (with its
    range), `uncorrected_at_adopted_responses`, `school_within_district`,
    `school_within_district_as_response`, `adopted` (with the range), `audit_row3_instead_of_cbo_income_tax`
    and `no_fill_in_correction`.
  - The other two profiles carry `adopted_2026_09_23/24/26`, `uncorrected_at_adopted_responses` and
    `adopted`.
  - An uncorrected-model gate uses `uncorrected_at_adopted_responses` ($265.5903–298.6797bn).
  - The profile name `cbo_category_lag_non_school_full` is kept so consumers still find it. CBO's
    category rule still decides which budgets respond; schools now respond at 1 through the
    specifications.
- **`derived/summary.json`.** Keys: `main_case`, `change`, `responses`, `school`, `range`,
  `other_profiles`, `group_receipts_bn` (adds `adopted_2026_09_26`), `uncorrected_at_adopted_responses`
  and `components`.
- **`package.cjs`.** Has the September 26 interface. `central(o)`, `evalPackage(c, m, o)`,
  `specsFor(o)`, `band(m, profile)` and `correctionsPayload(o)` take `o.school_rule`: `"average"`
  (adopted), `"within_district"`, `"within_district_as_response"` or `"one_year"`.

Scope: the operator said "we don't have to update all the uis ... we're still researching", so the
explorer, the figures page and the prototypes stay on earlier cases. The research documents and
consumer lanes move to this case in the peer session (immigration-research-1c), as agreed on
2026-09-26.

## Limits

- **Neither end of the school response is a causal estimate.** The cross-sectional ~1 may partly
  reflect urban costs and pupil needs. The within-district 0.836 may reflect lag, enrollment noise or
  lasting dilution. [INFERENCE]
- **The upper side is unpriced** (see Range).

## Reproduce

```sh
node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs   # all gates must pass
```

## Corrections

- 2026-09-26, 23:50 JST. The first version (3922e68) reported the school line as $167.0bn / $143.4bn
  and the unfunded parts as $57.6bn / $46.3bn (one year) and $24.6bn / $22.4bn (low side). Each was a
  difference of band ends, and those ends come from different specifications: at response 1 the ends
  are specifications 48/11, at response 0 they are 56/3. The figures are now read at fixed
  specifications, and two gates guard the reading: per-specification costs must reproduce every rule's
  band, and unfunded must equal (1 − r) × line at every specification. The peer session found the
  defect; its per-specification check and the generation lane's school line (2441ac8, 138.73 / 172.47)
  agree with the corrected figures. The case, the range and every other output are unchanged.
