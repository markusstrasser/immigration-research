---
date: 2026-10-24
concepts: [estimate-screen, influence-test, public-land]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-10-24-influence-test-for-sums.md
evidence: infra/immigration-fiscal/land_price_check_2026_10_24/
---

# 2026-10-24: Test the land sum's concentration against independent prices for its five largest counties

## Context

The reworked land charge (`land_price_rule_r2_2026_10_24`, $16.2 / 15.6bn at the bound rates) fails drop-five: Los
Angeles, Orange, San Diego, Santa Clara and San Bernardino carry 51% of it. Dropping them deletes measured cost; repricing
them at the same source's county average duplicates the stability test (the reopened decision). The question a sum's
concentration raises is whether the few units carrying it are measured right. That is testable with prices that do not
come from FHFA's land series (Davis, Larson, Oliner and Shui), which supplies every urban price in the lane.

Operator, 2026-10-24, on the recommendation to check the five counties against an independent source: "can you
orchestrate deepseek subagents to do that?"

## Decision (pre-registered before any independent price is seen)

1. Three independent source families, one worker each: (A) California assessor land values on parcels whose base year
   was reset by a 2022–2024 transfer; (B) land-transaction studies and datasets (vacant-land sales); (C) prices
   governments paid to acquire land in those counties. FHFA land prices, and studies built on them, do not count.
2. Each source gives a 2024 price per acre of urban residential-comparable land for as many of the five counties as it
   can, with its observation count. A year adjustment must use the source's own series, a house-price index other than
   FHFA's land series, or the CPI, stated.
3. For source s, q_c = P_s,c ÷ the lane's FHFA price for county c (`derived/reference_top5.csv`); a county the source
   cannot price keeps q_c = 1. The repriced sum is total − Σ charge_c + Σ charge_c·q_c, at each end. Source s passes if
   the sum moves ≤ 25% (the screen's influence threshold) and it prices Los Angeles plus at least two other counties.
4. The land charge is identified if at least two of the three sources pass. Otherwise it stays "not identified" and
   beside. The parent computes q and the rule (`test.py`); the workers only supply prices.

## Alternatives considered

- Drop-five (standing rule): deletes measured cost when the group lives where land is dear. Kept as reported.
- County-average repricing: same source, so it tests stability, not concentration. Withdrawn.

## Revisit if

- A source turns out to derive from FHFA's land series.
- The sources disagree with each other by more than they disagree with FHFA (then none is a check).
