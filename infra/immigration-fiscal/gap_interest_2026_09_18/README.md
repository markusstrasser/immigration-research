# Interest on the fiscal gap — September 18, 2026

**Verdict:** If the Mexican-origin population's complete-account absolute balance of −$263bn a year is financed by borrowing at the FY2024 effective federal rate (3.22% = net interest $879.9bn over average debt held by the public $27.3tn), the accumulated debt after 10 years is $3.05tn, of which $416bn is interest, and the interest bill alone in year 10 is $87bn a year, a third of the flow. After 30 years the debt is $13.0tn and the annual interest, $397bn, exceeds the flow itself. Half deficit-financed (states balance budgets, so the state-local part lands on current taxpayers): $1.52tn, $208bn and $43bn at year 10. On the same-age gap against third-plus whites (−$361bn) the year-10 figures are $4.18tn, $571bn and $119bn. Per person, compounding the pronatal lane's lifetime profile forward to age 83 instead of discounting it back reproduces the present-value ordering scaled by (1+r)^(83−age); the present-value budgets already carry the interest and remain the number to quote.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/gap_interest_2026_09_18/interest_on_gap.py
```

Inputs: `ledger_absolute_2026_09_17/derived/waterfall.csv` (step 14 endpoints), `derived/complete_gaps.csv`, `pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv`. Rate anchors fetched 2026-09-18 from Treasury FiscalData `debt_to_penny` (debt held by the public 2023-09-29 $26,330.14bn, 2024-09-30 $28,307.31bn) and OMB Table 3.2 net interest FY2024 (already in `params.json`). Outputs: `derived/aggregate_debt_paths.csv` (3 flows × 2 deficit shares × 4 rates × 3 horizons), `derived/per_person_terminal_values.csv`, `derived/audit.json`.

## Aggregate, union absolute −$263.2bn/yr, all deficit-financed

| years | debt at 3.22% | interest component | interest bill in year N | debt at 5% |
|---:|---:|---:|---:|---:|
| 10 | $3,048bn | $416bn | $87bn | $3,311bn |
| 20 | $7,234bn | $1,969bn | $218bn | $8,704bn |
| 30 | $12,981bn | $5,084bn | $397bn | $17,488bn |

## Caveats

- Arithmetic on a constant flow at today's population and today's profiles; no growth, no aging of the stock, no behavioural response, no inflation adjustment (nominal rate on a real-2024 flow overstates slightly).
- The F item of the complete account charges a share of existing net interest under its per-capita and tax-share arms; this file charges interest on the gap itself, a different object, and the two should not be added under the zero-F central arm without saying so.
- The deficit share is a convention. The incidence lane (`gap_incidence_2026_09_18`) is building the federal/state split; until then the half arm is a placeholder, not an estimate.
- The per-person terminal values compound 83 years of a period profile and are dominated by the horizon; they are stored for completeness, not quoted.
