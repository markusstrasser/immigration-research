# Adopted main case of the complete annual account

**Verdict:** With the three changes the operator adopted on 2026-09-23, the complete account's
main CBO-informed case is a net cost to other US residents of **$203.2–249.6bn a year**, up from
the published $165.1–197.4bn. That is $4,969–6,104 per member of the 40.9m Mexican-origin union.
[CALCULATION: `main_case.js` → `derived/main_case_bands.csv`; all gates pass]

- **General government** responds at 0.59–0.84 instead of zero: +$28.5bn to +$40.6bn.
- **Public order and safety** is keyed by use: +$5.94bn.
- **Uncompensated hospital care**: the under-charged part is keyed to uninsured use, +$3.65bn to
  +$5.75bn.

The other published benchmarks move the same way. With non-school education budgets also fixed,
the cost is $158.9–212.6bn (was $120.8–160.3bn). With every service proportional it is
$307.9–341.0bn (was $269.8–288.7bn). Defense, interest on existing debt and business subsidies
stay at zero response.

Date: 2026-09-23. Decision: [decisions/2026-09-23-main-case-general-government-and-use-keys.md](../../../decisions/2026-09-23-main-case-general-government-and-use-keys.md).

## Method

`main_case.js` runs the explorer's evaluator (`../assumption_explorer_2026_09_21/engine.js`) on
its executed model (`derived/model.json`). The evaluator implements the account's formula,
`welfare = P + weight × (direct + F)`, and `test_engine.js` gates it against 2,629 rows of the
executed grid. The script first reproduces the three published bands exactly (gate, 1e-6 bn).
Then it applies the three changes.

1. **General government.** `general_government_response` is set to 0.59 and 0.84, read from
   `scaling_check.json`. The low end holds the federal executive and legislative budget fixed and
   scales federal tax collection at 0.79; the high end scales everything at the cross-state
   administration elasticity, 0.842 (SE 0.039). The assigned amount is $48.29bn.
   [SOURCE: [explorer README](../assumption_explorer_2026_09_21/README.md), "General government: a proposal"]
2. **Public order and safety by use.** The target's allocation on the line rises by the justice
   lane's central change, +$5.94bn, with the national total conserved: prisons by adjusted ACS
   custody, police half by arrests, courts 60% criminal, CBP per head.
   [SOURCE: [justice lane](../cj_use_allocation_2026_09_23/RESULT.md), `summary.json`]
3. **Uncompensated care.** The target's Medicaid allocation rises by the part of government
   uncompensated-care offsets that the account keys below the union's 25.7% share of uninsured
   person-years: $3.65–5.75bn at equal use. The part borne outside government budgets
   ($3.2–5.6bn) is not fiscal. It is reported as a social item beside the headline.
   [SOURCE: [uncompensated-care lane](../uncompensated_care_2026_09_23/RESULT.md), corrected 575e2ee]

Changes 2 and 3 move allocations inside the account, and both lines respond at 1 in every
published profile. A gate checks that the adopted main band equals the published band plus the
three deltas.

## Sensitivities on the adopted main case

| Variant | $bn a year | Per member |
|---|---:|---:|
| Adopted | 203.2–249.6 | $4,969–6,104 |
| Justice with census ethnicity codes as recorded (+$1.67bn) | 198.9–245.4 | $4,864–6,000 |
| Justice across its 216-set grid (−$1.03bn to +$8.65bn) | 196.2–252.3 | $4,798–6,170 |
| CBP held fixed (+$2.84bn) | 200.1–246.5 | $4,893–6,028 |
| Uncompensated care at 0.7× use ($2.12–3.51bn) | 201.7–247.4 | $4,931–6,049 |
| General government at 0.59 only / 0.84 only, without changes 2–3 | 193.6–225.9 / 205.7–237.9 | |

The account's statistical standard error, about $12bn per case (ladder 184), was computed before
these changes and is not re-propagated here. [DATA: `derived/main_case_bands.csv`]

## Reproduce

```sh
node infra/immigration-fiscal/main_case_2026_09_23/main_case.js
```

It reads `assumption_explorer_2026_09_21/derived/{model.json,scaling_check.json}`,
`cj_use_allocation_2026_09_23/derived/summary.json` and
`uncompensated_care_2026_09_23/derived/summary.json`, and writes `derived/main_case_bands.csv`
and `derived/inputs.json`. It exits 1 if any gate fails.
