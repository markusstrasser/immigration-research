claude-opus-5-5

**Verdict:** The September 27 case charges public capital, roads and parks as if they scale with population in the long
run, but it holds the group's property taxes at response 0. The engine credits taxes the group pays directly at 1 and
every tax attributed to it through incidence at 0. Letting owner-occupied property tax leave with the group lowers the
case by **$19.7bn** at 0.79, highway construction's across-state scaling, and by **$25.0bn** at 1, at both ends:
$302.1–367.6bn and $296.8–362.4bn, against $321.8–387.4bn. This is a probe, not a candidate. Renters' share of
rental-property tax needs a use key, and the case carries none.

## What the case does

- **The engine switch.** `engine.js` sets `direct_receipt_response: 1, indirect_receipt_response: 0`. Six receipt
  lines are incidence ("direct: false") and carry an amount on the group, shared allocation, CBO rule:
  - owner-occupied property tax (`modeled_owner_property`), $24.97bn;
  - business property tax keyed to capital ownership (`remaining_production_property`), $13.28bn;
  - corporate tax, capital share, $18.50bn;
  - corporate tax, labor share, $14.57bn;
  - government asset income, $23.60bn;
  - other business taxes and transfers, $10.60bn.

  `meta.responses` in the adopted `corrections.json` overrides only the enterprise surplus. [DATA:
  `assumption_explorer_2026_09_21/derived/model.json`; `main_case_long_run_2026_09_27/derived/corrections.json`]
- **Where corporate tax is handled.** The production module (P + F) handles corporate tax through capital adjustment.
  At the reference cell, with full capital adjustment, P + F is $13.32bn at every capital-tax retention, 0, 0.5 and 1,
  so the headline does not depend on it. Government asset income does not scale with population, so 0 is right for it.
  Owner-occupied housing is outside the production module.

## The probe

`probe.cjs` loads the adopted package unchanged. It reproduces `evaluateFull` at specifications 48 and 11, both
fill-in methods averaged, and a gate checks this. It then sets `response_override["receipt:<line>"]`.
[CALCULATION: `derived/probe.json`]

| Receipt response | Spec 48 | Spec 11 |
|---|---:|---:|
| Adopted (owner-occupied property tax at 0) | 321.82 | 387.37 |
| Owner-occupied property tax at 0.79 | 302.09 (−19.73) | 367.64 (−19.73) |
| Owner-occupied property tax at 1 | 296.85 (−24.97) | 362.40 (−24.97) |
| Owner-occupied and capital-keyed business property tax at 0.79 | 292.93 (−28.89) | 360.21 (−27.16) |
| Owner-occupied and capital-keyed business property tax at 1 | 285.25 (−36.57) | 352.99 (−34.38) |

The capital-keyed business row uses the wrong key for this question. It keys property tax by who owns the capital,
while the long-run question is whose housing and jobs the capital serves. It is shown only as a rough bound.

## Why it matters, and the case for 0

- **The case for 0.** The houses stay and new owners pay the tax, which is capitalized into lower prices. That holds
  when the stock is fixed and fully reoccupied.
- **Against it.**
  - The adopted case is explicitly long-run. Public capital is charged at a 2–3% return because the stock scales
    with population, and highway construction scales 0.79 across states.
  - Under that premise the housing stock also follows households, and the tax on houses that would not exist is lost
    to other residents.
  - On the benefit-tax reading, property tax pays for the local services the case charges at their long-run response.
  - Land stays when the group leaves, which argues for a response below 1.

## Next

A receipt-side lane should cover four things:
- key renters' property tax by occupancy;
- split land from structures for the response;
- check payroll-tax compliance of workers paid off the books, which runs the other way;
- apply one long-run rule to every line whose base scales with population, on both sides of the account.

## Reproduce

```sh
node infra/immigration-fiscal/receipt_long_run_probe_2026_09_28/probe.cjs
```
