# Lane brief: measure the back-cast's pandemic years instead of attributing them

Date 2026-09-28, 03:40 JST. Parent session immigration-research-1c. Follows the validation memo
(`research/immigration-validation-and-backtesting-2026-09-28.md` §3, "policy stress": income-2021 profiles carried
into 2024 miss the union's net-tax share by 4.77pp, $90.86bn).

## The problem

- `research/immigration-historical-backcast-2026-09-20.md` (lines 99–109) attributes 2020–2021 refundable credits
  to the group at its 2024 ratio, 2.3 times other residents per person. That makes the pandemic years 35–38% of
  the ten-year programme-rule total.
- The memo itself calls that attribution too high: pandemic payments were close to uniform per head, and the
  first round excluded households filing without SSNs [TRAINING-DATA there]. Its fix is a variant that sets
  2020–2021 to the 2019/2022 mean.
- The group's use of each programme in earlier years is unmeasured, yet CPS ASEC reports it.
  `validation_fiscal_years_2026_09_28/derived/annual_components.csv` now reconstructs income years 2021–2024 by
  group under each year's own tax model.

## Tasks

1. Measure the group's share of federal refundable credits, EIP payments and SNAP, SSI and Social Security
   receipt for income years 2019–2023 from CPS ASEC. Use the same union definition, weights and resource-sharing
   rules as the account. Use the validation lane's 2021–2024 reconstructions where they apply, and ASEC 2020–2021
   for income years 2019–2020 where they are local (check the dataset register).
   - Verify the EIP1 SSN exclusion from primary law: the CARES Act §2201 and the CAA 2021 amendment.
2. Replace the attributed 2020–2021 lines with the measured shares. Report the ten-year totals, old → new, for
   both rules and both ends. Also report the pandemic years' share of the total.
3. Report each other programme line where the measured 2019–2023 ratio differs from the 2024 ratio the back-cast
   applies by more than 10%.

## Rules

- A new lane in this directory. Import or read `historical_backcast_2026_09_20`; do not edit it.
- Scripts write to `derived/`; raw pulls go in `_cache/`. Two runs must be byte-identical.
- Write `RESULT.md` first with `**Verdict:** pending`, and append as you go. No commits, staging or stash.
- Never print the Census API key. Pipe Census output through a redaction filter.
- Final message: the RESULT path and at most ten lines.
