claude-opus-5-5

**Verdict:** Candidate v3 (items 1–8, pension switch off) costs **$288.00–353.63bn** at specifications 48 / 11. That is
$33.81 / 33.74bn below the adopted September 27 case ($321.82–387.37bn). With the pension switch on (accrual, read from
the pension lane at c9d0077, after its national check passed) it costs **$404.46–464.39bn**. The second switch, item 10
(hospitals' uninsured use at 0.7×), lowers either total by $1.53 / $2.24bn. Every gate passes:
- with every item off, the package is the September 27 case exactly at all 64 specifications;
- with items 1–3 on, it is v2 exactly;
- each item alone reproduces its lane (workers' compensation and transit differ for the reasons below);
- each item moves only its named lines, and national totals hold.

Two `rerun_lane.py` passes are byte-identical. I recommend items 1–7 in the case ($287.84–353.45bn) and transit (8) beside
it. [Parent, 11:15 JST, after the session restart:
- item 10 belongs beside the case, because its evidence exists only between regions;
- the pension switch is the operator's call. The parent recommends it on, now that the national check has passed (bc071ba).
  Items 1–7 with accrual cost $404.29–464.21bn.
The re-pin and item 10's numbers were written in by the parent; see the log.] Nothing here is adopted.

## Items at 48 / 11

Each item alone on the September 27 case, both fill-in methods averaged, $bn. [CALCULATION: `main_case.cjs` →
`derived/fixed_specs.csv`, `attribution.csv`]

| Item | Old → new at 48 / 11 | Change | Recommendation |
|---|---|---:|---|
| 1. Public housing's deficit at the tenant key | 321.82 / 387.37 → 320.13 / 385.68 | −1.69 / −1.69 | **In.** The deficit subsidizes public housing's tenants, so their key carries it, not the population's (v2's revision after the attack on the first candidate). |
| 2. Production on the account's weights | → 323.46 / 388.48 | +1.64 / +1.11 | **In.** The production module should weigh the group as the rest of the account does (the row-4 grid), not with the published grid's weights. |
| 3. IRS-matched income-tax key | → 318.62 / 384.27 | −3.20 / −3.10 | **In.** A key held out against IRS 2023 AGI bins is measured on tax records; the survey gradient is not (ladder 249). |
| 4. Public housing's capital at the tenant key | → 321.47 / 386.84 | −0.35 / −0.53 | **In.** Without it, item 1 keys the enterprise's current account by tenants and its capital by population. |
| 5. Long-run property taxes | → 294.63 / 360.18 | −27.19 / −27.19 | **In.** The case already lets public capital, roads and parks respond in the long run; this applies the same rule on the receipt side (ladder 253). Range −24.08 to −40.41. |
| 6a. Payroll compliance, `all` central items | → 321.45 / 387.21 | −0.37 / −0.16 | **In.** Measured misreporting and filing rates replace a zero set by convention. It is small, and its readings range (−1.62 to +3.97 at 48) travels as a range component. |
| 6b. Row 2 through CBO's re-key, within-group rule | → 321.01 / 386.56 | −0.81 / −0.81 | **In.** The proportional rule counts the between-income-group difference twice, since CBO measures that difference on tax returns. |
| 7. Workers' compensation pooled over 2019–2024 | → 319.81 / 385.82 | −2.01 / −1.55 | **In.** The 2024 key is the outlier: all five earlier years run at 0.42–0.84 of it (z down to −4.8, ladder 251). |
| 8. Transit at the riders' key (deficit-weighted) | → 321.99 / 387.55 | +0.17 / +0.18 | **Beside.** Weighted by where the deficit falls, the riders' key is 1.019 (SE 0.017) times the population key, so it changes nothing distinguishable. The brief's −$2.2bn assumed the same subsidy per rider everywhere, which state finance data reject. |
| 9. Pension accrual (switch) | → 437.83 / 497.78 | +116.01 / +110.41 | **The operator's call.** Read at c9d0077: the national check passed (bc071ba), and Part A's spouse credit was removed. The parent recommends it on, with cash beside. |
| 10. Hospitals' uninsured use at 0.7× (switch) | → 320.29 / 385.13 | −1.53 / −2.24 | **Beside.** The S-10 slope implies a use rate of 0.49 (0.16–0.93). With region controls it implies 0.89 (0.61–1.24), so the evidence exists only between regions (ladder 256). |
| **Candidate, items 1–8, switch off** | **→ 288.00 / 353.63** | **−33.81 / −33.74** | |
| **Candidate, switch on** | **→ 404.46 / 464.39** | **+82.64 / +77.02** | |
| Recommended set, items 1–7 | → 287.84 / 353.45 | −33.98 / −33.92 | |
| Items 1–7 with the pension switch on | → 404.29 / 464.21 | +82.47 / +76.84 | |
| The candidate with item 10, pension switch off; on | → 286.47 / 351.39; 402.92 / 462.15 | −35.35 / −35.98; +81.10 / +74.78 | |

Beside the items, each alone on the September 27 case (change at 48 / 11) [CALCULATION: `fixed_specs.csv`]:
- 6a under the payroll lane's proportional rule (`r_cal_raw`, its sensitivity): +0.39 / +0.53. On the candidate, item 6
  under the proportional rule (6a at `r_cal_raw`, 6b off) is +1.58 / +1.51 above the candidate.
- 6a at the lane's low-cost and high-cost readings: −1.62 / −1.43 and +3.97 / +4.18.
- 5 at the lane's low responses: −24.08. At 1 everywhere with the case-scaled tenant national: −40.41.
- 8 on the deficit alone: +0.15. At the commuter key: −2.28 / −2.43 (the deficit alone −1.98). At the deficit-weighted
  key with NHTS 2017's all-trip adjustments: +1.18 / +1.26 (within-survey, 1.110) and −0.57 / −0.60 (cross-survey, 0.920).
- The candidate with transit at the commuter key: −2.45 / −2.61 from the candidate.

## Together: interactions and attribution

The items nearly add. Items 1–8 alone sum to −33.8107 / −33.7354, against a joint change of −33.8145 / −33.7364.
The interaction is −0.004 / −0.001. It sits in items 3 and 6: the payroll ratios scale the group's federal income tax
after item 3 has re-keyed it [CALCULATION: `attribution.csv`].

Sequential attribution, listed order (forward) and reverse, change at 48 / 11:

| Item | Alone | Forward | Reverse | Forward, switch on | Reverse, switch on |
|---|---:|---:|---:|---:|---:|
| 1 | −1.691 / −1.691 | same | same | same | same |
| 2 | +1.643 / +1.107 | same | same | same | same |
| 3 | −3.201 / −3.097 | −3.201 / −3.097 | −3.204 / −3.098 | −3.201 / −3.097 | −3.204 / −3.098 |
| 4 | −0.353 / −0.529 | same | same | same | same |
| 5 | −27.186 / −27.186 | same | same | same | same |
| 6a | −0.371 / −0.162 | −0.373 / −0.160 | −0.371 / −0.162 | −0.373 / −0.160 | −0.678 / −0.538 |
| 6b | −0.814 / −0.808 | −0.816 / −0.811 | −0.814 / −0.808 | −0.816 / −0.811 | −0.066 / −0.083 |
| 7 | −2.007 / −1.550 | same | same | same | same |
| 8 | +0.170 / +0.181 | same | same | same | same |
| 9 | +116.010 / +110.406 | | | +116.450 / +110.755 | +116.010 / +110.406 |
| Sum | −33.811 / −33.735 (with 9: +82.199 / +76.670) | −33.815 / −33.736 | −33.815 / −33.736 | +82.636 / +77.019 | +82.636 / +77.019 |

With the switch on, the interaction is +0.44 / +0.35. Payroll tax buys accrued benefits. Under accrual,
`social_security` becomes 1.298 times the group's OASDI receipts, so any item that moves those receipts moves the
accrual with them [CALCULATION]:
- With the switch in place first, 6b falls from −0.81 to −0.07 / −0.08. 6a grows to −0.68 / −0.54, because its
  self-employment item lowers the group's self-employment tax and so its accrual.
- With the switch last, it adds +116.45 / +110.76 instead of +116.01 / +110.41.
- Item 10 stands outside the sums. It moves only the Medicaid line, and it adds exactly: −1.534 / −2.242 alone, last on
  the candidate, and on the candidate with the switch on.

## Ends and range

**Ends.** The band's ends stay at specifications 48 (shared, GDP, school share 0.7153, gg 0.6000, uninsured use low, 2%)
and 11 (personal, cash, 0.8652, gg 0.8504, use high, 3%). This holds in both fill-in methods, with either switch off or on,
over the 32 distinct specifications (48 ≡ 52, 11 ≡ 15). The runner-ups are 56 (school share 0.8652; +$0.79bn above 48)
and 3 (school share 0.7153; $0.81bn below 11), the same with the switch on [CALCULATION: `ends.csv`].

**Outer range.** The components are v2's 19, re-run on each base at every specification, plus three item components:
- property: the lane's low responses, and 1 everywhere with the case-scaled tenant national;
- payroll: the low-cost and high-cost readings at row 2's central shares;
- transit: the commuter key and the two all-trip adjustments.

An item's component moves nothing on a base without the item. On the September 27 case and on v2, the components
reproduce each published range to 1e-9 [DATA: gates]. The joint reading adds the congestion item at each band end's
lane cut (the dependent-pieces placement rule).

| Base | Band 48 / 11 | Outer, account only | Outer, jointly with congestion | Quadrature |
|---|---|---|---|---|
| September 27 | 321.82 / 387.37 | 258.65–436.05 | 258.49–433.02 | 290.90–408.23 |
| v2 | 318.57 / 383.69 | 255.29–432.47 | 255.13–429.44 | 287.63–404.57 |
| **v3, switch off** | **288.00 / 353.63** | **208.11–410.68** | **207.95–407.65** | 254.30–375.15 |
| v3, switch on | 404.46 / 464.39 | 329.13–513.97 | 328.97–510.94 | 371.06–483.68 |
| v3, item 10 on (pension switch off) | 286.47 / 351.39 | 206.58–408.44 | 206.42–405.41 | 252.77–372.91 |

On v3 with the switch off, the new components at 48 / 11, lowest and highest [CALCULATION: `components.csv`]:
- property: −13.23 and +3.11 at both ends;
- payroll: −1.26 / −1.28 and +4.38 / +4.39;
- transit: −2.45 / −2.61 and +1.01 / +1.08.

The tax block narrows under 6b, from v2's −6.01 / −5.00 … +6.16 / +5.14 to −5.66 / −4.70 … +5.79 / +4.83. The
within-group rule gives row 2 a smaller effect at every on-books share. With the switch on, the tax block and payroll
components narrow further, because OASDI receipts partly buy accrual.

## Beside the range

- **Public pay:** unchanged by items 4–9, which touch no consumption line (gate, 1e-12). On the candidate:
  - unchanged workforce, +13.61 / +8.95;
  - on the account's own counterfactual workforce, +12.39 / +8.09 (low removal share) and +12.05 / +7.85 (high).
- **Road arm:** identical to v2's (gate, 1e-9). Account change / net of the congestion item at 48 / 11:
  - replacement, −5.23 / −10.75, net −0.06 / −3.60;
  - a fixed stock, −10.51 / −17.97, net −5.34 / −10.83;
  - construction with year effects, +0.90 / 0, net +0.44 / 0;
  - construction with a land control, +0.44 / 0, net +0.21 / 0.

  The stationary network's congestion item is 13.99 / 12.02 [CALCULATION: `road_arm.csv`].
- **Sign break-even.** This is v2's convention: the service share at which the group turns into a net cost, enterprises
  at s, from the personal low end to the shared high end [CALCULATION: `sign_reversal.cjs` → `sign_reversal.csv`]:
  - September 27: 2.83–13.60%;
  - v2: 3.55–13.95%;
  - **v3, switch off: 10.74–21.71%;**
  - v3, switch on: −16.08% to −8.01%. Negative means a net cost even if no service budget responds.

  With enterprises at 1, v3 is 5.88–15.29% (personal) and 8.84–18.44% (shared). The frozen-services welfare
  (capital fixed) is −19.16 to +89.39 on v3 and −129.92 to −27.06 with the switch on.
- **Defense** stays at response 0. FAQ 2's GDP-share bound is +47.51 (capital fixed) to +72.00 (full adjustment)
  [DATA: `receipt_side_long_run_2026_09_28/derived/probe.json` `defense_bound`].
- **Unpriced beside the switch:** interest on the group's existing pension liability. The switch replaces cash with the
  normal cost only; a full pension expense would add interest on the liability already accrued [SOURCE: pension lane
  RESULT at bec1cd7, lines 228–232].
- **The federal transit operating-subsidy crossing** (v2's `crossings.csv`) still crosses. The paying leg is a business
  subsidy held at response 0. The receiving leg is now the transit line at the riders' key and response 1: −117.18 →
  −119.38 $ million per $1bn [CALCULATION].

## Item notes

**1–3.** v2's items unchanged. Each alone equals v2's `summary.json` `at_fixed_specifications` to 1e-9, and together
they equal v2 at every specification and its committed `per_spec.csv` exactly [DATA: gates].

**4.** The capital lane's own rule for `ent_housing_sl` (`lines_amount_over_national` on `housing_subsidies`), from its
variant `public_housing_at_rental_assistance_key`, is applied on each evaluation. A capital variant that sets that
component's key itself wins. Alone, it equals the capital lane's variant at every specification (difference 0), and
the component's key is the rental line's evaluated key (1e-15). Its change is v2's reported companion, −0.3529 /
−0.5293 [DATA: gates].

**5.** The receipt-side lane's `items.cjs` `itemModel` and `itemOverrides` are imported and applied unchanged:
- owner-occupied property tax at 0.762903;
- the $83.840225bn tenant-occupied tax split out of business property, at the rent key (0.114667) and 0.708443;
- personal property re-keyed to vehicles (0.102082) at 1.

The receipt responses apply in every profile, as the lane applied them. Alone, the item and its two range ends equal
the lane's own evaluation path (`evaluateWith`) at every specification (difference 0), and its `probe.json` (1e-6, a
6-decimal file) [DATA: gates].

**6.** The payroll lane's `items.json` ratios are applied exactly as its `price.cjs` applies them: (ratio − 1) × the
group's reference-rule amount, expanded by the package's `expand()` and applied with `applyCorrections` on the model of
each fill-in method. 6a uses `r_cal`. 6b moves each row-2 line by (`r_cal_raw` − `r_cal`) of `row2_r_route/without`
times the amount. That is row 2 removed under the proportional rule, less row 2 removed under the within-group rule.
Both parts are read on the same amounts, so they add exactly.
- 6a, its readings and its proportional sensitivity equal `pricing.json`'s theta_calibrated and stack_factor_calibrated
  rows (1e-9). 6b equals `row2_r_route/without`'s stack_factor_calibrated less theta_calibrated (1e-9) [DATA: gates].
- For the tax block's low and high cases, 6b uses the lane's `row2_r_route/low` and `/high` ratios, r(without) / r(c).
  6a's `all` ratios exist only at row 2's central shares, so on the low and high stacks 6a applies the central ratios
  to those stacks' amounts. That is an approximation inside the tax-block component [INFERENCE].

**7.** The workers_comp key's group amounts are multiplied by pooled over 2024 relative use: 0.6289 (shared), 0.6799
(personal) [DATA: `ratio_vs_2024.csv`].
- The lane's "low / high" ends are its shared / personal allocations (`ALLOCATION_OF_END`). Here they coincide with
  specifications 48 (shared) and 11 (personal), so they compare directly.
- The lane reports −2.03 / −1.54 and v3 gives −2.01 / −1.55. The lane priced model.json's cells ($5.471bn shared,
  $4.826bn personal). The case carries its corrected amounts, $5.409bn at 48 and $4.842bn at 11 [CALCULATION].
- The ratio reproduces the lane's own change on its own amounts, at csv precision (1e-8 relative) [DATA: gate].

**8.** The brief's premise does not hold. `fed_transit_and_railroad` ($0.094bn) and `sl_transit_and_railroad`
($0.000bn) sit inside `economic_affairs_services` at the resources key (0.0810), not the population key [DATA:
model.json; `responses.json`].
- The population-keyed transit money is NIPA 3.8 line 14, S&L public transit's current surplus. That is −$66.69bn inside
  `enterprise_surplus` at the corrected population key, 0.117175. Its capital is `ent_transit_sl`, $505.80bn charged
  [DATA: `enterprise_surplus_vs_return.csv`, `engine_components.json`].
- Item 8 splits line 14 out as `transit_enterprise_surplus`, keyed by the enterprise cell's fraction × RU. It responds
  with the enterprise receipt. The rest of the enterprise line keeps every cell's fraction, so its key and every other
  enterprise component hold (1e-15; 1e-12). `ent_transit_sl` takes the new line's key. The $0.094bn is left alone.
  Railroad needs no split: line 14 is S&L public transit only.
- The deficit-weighted key is 0.119384 at 48 [CALCULATION: `per_spec.csv`].
- **The key** (`transit_key.py`, a subagent; I recomputed its three relative uses from its state table) [CALCULATION:
  `derived/transit_key.json`]:
  - ACS 2024 PUMS: the group, HISP 02 or born in Mexico, is 8.65% of transit commuters (codes 02–06) and 11.59% of
    persons, an RU of 0.7465 (SE 0.013).
  - Its mode shares, 2.83% against 3.68%, match S0201's 2.8% and 3.7% [DATA: Census API control, cached].
  - Weighting each state's group share of transit commuters by that state's transit deficit gives 1.0188 (SE 0.017).
    The deficit is current operations less transit utility revenue, from the Census 2024 state and local finance
    survey. ΣD = $55.53bn, 0.833 of NIPA's $66.69bn.
  - New York has 37.9% of transit commuters and 22.0% of the deficit, and the group is 4.9% of its riders. California
    has 10.1% and 20.7%, with the group at 26.8%. The deficit per resident transit commuter is about $5k in New York and
    $19k in California.
  - NHTS 2017 all-trip adjustments: 1.110 (within-survey) and 0.920 (against the same-year ACS). NHTS 2022 is too thin
    (59 Hispanic transit trips).
- **Limits:**
  - Commuters are not riders: the ACS counts workers' usual mode.
  - State weighting misses within-state differences, such as Los Angeles against the Bay Area.
  - Deficits are booked to the operating state (WMATA to DC, the MTA to New York), while riders are placed by
    residence.
  - Capital outlay weighting gives 1.169. That is a flow, not the stock, so it is not used.

**9.** The switch reads `pension_accrual_2026_09_28/derived/summary.json` at commit c9d0077 through `git show` (sha256
d1c8326b3b36…), not the working tree. It was built at bec1cd7 (sha256 9c2a447ee812…), and the parent re-pinned it after
the lane's national check (bc071ba). The central is the same at bc071ba and c9d0077.
- Ratio 1.297788, Part A accrual $45.3535bn (bec1cd7: $51.2828bn, before the spouse credit was removed), Part A share
  416.3 / 1,109.8, OASDI share of self-employment tax 0.8035.
- Switched on over the September 27 case, it gives the lane's +116.009525 / +110.405709 (1e-6). `social_security`
  equals the ratio times the group's OASDI receipts on every base. `medicare` equals (1 − 0.3751) × cash + the Part A
  accrual (1e-9) [DATA: gates].
- The re-pin changed only `PENSION_COMMIT` in `package.cjs` (bec1cd7 → c9d0077).

**10.** A switch on the Medicaid line's uncompensated-care key. At 0.7× it moves each specification's `uc` key to its
own 0.7×-use arm (`uninsured_use_07_low` / `_high`). The engine model already carries that arm, and the case's
corrections move it the same way as the keys in use (gate, 0.0).
- Alone it gives the back-test's frozen consequence, −$1.534 / −2.242bn (1e-9). It moves only the Medicaid line.
- `uninsured_use_slope.py` reads the back-test's two fits as use rates through the same key map: 0.49 (0.16–0.93) in the
  primary fit and 0.89 (0.61–1.24) with region controls (post hoc). It reproduces the back-test's slopes and SEs to
  1e-9. [CALCULATION: `derived/uninsured_use_slope.json`]

## Adoption path (specified, not implemented)

Beyond v2's three extensions of the September 27 `corrections.json` (A: the housing split; B: the row-4 production
grid; C: the tax-key edits; v2 RESULT "Adoption path"), the items need:
- **(D) Item 4.** In `meta.capital_return.components`, `ent_housing_sl`'s key becomes `{kind:
  lines_amount_over_national, numerator_lines: [housing_subsidies], denominator_line: housing_subsidies}`, the capital
  lane's own variant rule. No engine change is needed; consumers that compute the return from `meta` already implement
  that kind.
- **(E) Item 5.**
  - A new receipt line, `tenant_occupied_property`: national $83.840225bn, all 8 rules at the rent key 0.114667,
    `direct: false`, class `tenant_housing_property`. `remaining_production_property` is scaled down by the same
    national amount.
  - Ordinary receipt edits re-key `personal_property_tax` to 0.102082.
  - `meta.responses` receipt overrides: `modeled_owner_property` 0.762903, `tenant_occupied_property` 0.708443,
    `personal_property_tax` 1, in every profile.
  - This needs A's engine additions: a receipt-line field and a national-scale edit.
- **(F) Item 6.** Ordinary receipt edits: 14 lines for 6a and the row-2 lines for 6b, the methods' mean, expanded to
  the 8 rules and composed with the existing edits on those lines. The engine can express these today.
- **(G) Item 7.** Ordinary spending edits on `workers_compensation`, `temporary_disability` and `black_lung` at key
  `workers_comp`. The engine can express these today.
- **(H) Item 8, if taken.**
  - A new receipt line, `transit_enterprise_surplus`: national −$66.69bn, at RU × the enterprise key.
  - `enterprise_surplus` is scaled from −7.162 (after A) to +59.528.
  - A `meta.responses` entry that follows the enterprise receipt.
  - `ent_transit_sl`'s key becomes `receipt_amount_over_national` on the new line.
  - This needs A's engine additions.
- **(J) Item 10, if taken.** The specification set's `uc` key moves to its 0.7×-use arm. The payload already carries
  both arms, so no engine change is needed. Among the consumers, a grep finds the arm names in
  `debt_legacy_2026_09_23/debt_legacy.py` and `sept24_propagation_2026_09_24/band_variants.cjs`. Whether they would need
  the 0.7× pair was not traced [INFERENCE].
- **(I) Item 9, if taken.** Spending edits on `social_security` and `medicare`. As fixed numbers they hold only at the
  payload's own receipts. A consumer that re-keys OASDI receipts, such as the generation split, needs the rule, so
  `meta` would carry an accrual block: ratio, Part A accrual, Part A share, OASDI share of self-employment tax, and the
  source commit.

Consumers, from `rg -l corrections.json infra/` (98 files; the code files were listed, and their use of the payload was
matched against v2's table and grepped for `capital_return`, edit-set gates and key kinds). v3 adds to v2's table:

| Consumer | E, H (new receipt lines, national scale) | F, G, I (ordinary edits) | D, H (capital keys in meta) |
|---|---|---|---|
| `assumption_explorer_2026_09_21/engine.js` (the applier) | change, as for A | none | none |
| `generation_account_2026_09_24/run_generations.cjs` | change | change: it gates the payload's edit tail | none (reads `meta`) |
| `late_arrival_account_line_2026_09_27/run_cells.cjs` | change | change (same gates) | none |
| `debt_legacy_2026_09_23/debt_legacy.py` (own engine copy) | change | change: gate on the exact edit set | none: generic key kinds (lines 496–498) |
| `sept24_propagation_2026_09_24/band_variants.cjs` | change: line responses by name | none | none |
| `uncertainty_propagation_2026_09_22/sept24_specs.cjs` | change: `lineTargets` throws on a new receipt line | none | change for D and H: its capital rebuild knows only the enterprise receipt and its `KLINES` spending lines, which lack `housing_subsidies`, and throws otherwise (lines 86–87, 119–125) |
| `winners_losers_2026_09_24/specs.cjs` | change: exactly 4 line responses | none | none: component ids from `meta` |
| `historical_backcast_2026_09_20/case_components.cjs` | change | change | none |
| `world_ledger_2026_09_27/split_residual.py` | change | none | none |
| `world_ledger_2026_09_27/generation_lines.cjs` | a new pin | a new pin | none |
| `distribution_weights_2026_09_23/distribute.py` | check: it passes `meta.responses` through (lines 388–403), and E and H add receipt entries | none | none |

- **Case tables.** v2's list also needs a v3 entry: run_generations, run_cells, generation_lines, band_variants,
  sept24_specs, specs, case_components and `distribution_weights_2026_09_23/case_ends.cjs`.
- **Pinned to the September 27 payload by design**, needing nothing: the candidates' and the receipt-side lane's
  `sign_reversal.cjs`, `pension_accrual_2026_09_28/case_lines.cjs`, and the 09-27 conceptual audit probes.
- **On older payloads**, needing nothing now: the explorer UI, figures, consumption_key, the older producers, and the
  capital and response lanes.

The rows for F, G and I are extrapolated from v2's reading of the code and from these greps. They were not re-read in
full [INFERENCE].

## Gates (all pass)

`main_case.cjs`, 54 gates [DATA: its console output]:
- **The two bases:** September 27 exactly at all 64 specifications, against its package and its `per_spec.csv`; v2
  exactly, against its package and its `per_spec.csv`.
- **The specifications:** 32 distinct in each of 71 option sets, 48 ≡ 52 and 11 ≡ 15.
- **Each item against its lane,** as in the item notes.
- **Only its named lines move** for each item, and the candidate moves only the union; national totals hold per line,
  and the split lines sum to their old lines less the consolidated subsidy (1e-9).
- **Companions:** public pay and the road arm equal v2's; the congestion file was priced from this package, its transit
  key and the pension summary (sha256).
- **Range:** the September 27 and v2 ranges are reproduced, and every lane cut is priced.
- **Item 10:** the 0.7× arms add the uncompensated-care lane's amounts; alone the switch gives the back-test's frozen
  consequence; it moves only the Medicaid line, alone and on the candidate with the pension switch off and on.

`sign_reversal.cjs`, 16 gates:
- the September 27 and v2 columns reproduce v2's committed file (1e-4);
- each payload model gives its package's band (1e-9);
- at s = 1 the wrapped definition is the proportional reference on the candidate with the switch off and on (0.0);
- welfare is linear in s.

`road_congestion.py`, 9 gates: the bridge's B1 and four uniform rows are reproduced, and all 35 cuts are shared with
v2's `road_congestion.json` and price identically (0.0).

`transit_key.py`, 25 gates: hashes, the dictionary codes, the Census API controls, the NHTS totals and the state sums.

`uninsured_use_slope.py`, 7 gates: the back-test's r = 0.7 column, both fits' slopes and SEs, the primary implied r and
the map against the frozen 0.7× slope.

## Files

Scripts:
- `transit_acquire.py` and `transit_key.py`: the riders' key, by a subagent;
- `uninsured_use_slope.py`: item 10's evidence read as use rates;
- `package.cjs`: the definitions, importing v2's package and the receipt-side `items.cjs` unchanged;
- `road_congestion.py`, `main_case.cjs`, `sign_reversal.cjs`.

`derived/`:
- `transit_key.json`, `transit_key_states.csv`, `road_congestion.json`, `uninsured_use_slope.json`;
- `fixed_specs.csv`, `attribution.csv`, `candidate_bands.csv`, `ends.csv`, `components.csv`, `per_spec.csv`,
  `road_arm.csv`, `summary.json` (input hashes in `inputs`);
- `sign_reversal.csv`.

`_cache/transit/` is ignored: 22 pinned files and `manifest.json`. Nothing outside this directory was edited.

```sh
L=infra/immigration-fiscal/main_case_candidate_v3_2026_09_28
uv run --no-project python3 scripts/rerun_lane.py $L --allow-unrun package.cjs \
  "uv run --no-project python3 {lane}/transit_acquire.py" "uv run --no-project python3 {lane}/transit_key.py" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/uninsured_use_slope.py" \
  "uv run --no-project python3 {lane}/road_congestion.py" "node {lane}/main_case.cjs" "node {lane}/sign_reversal.cjs"
```

`package.cjs` is a module that the other scripts load, hence `--allow-unrun`.

## After the cross-lab review (parent, 2026-09-28)

GPT-6 Astra (xhigh) reviewed these items as a packet. It put items 1, 2 and 4 in, item 5 out as formulated, and the
rest beside. The parent checked every finding against the lanes and primary sources; a verification agent checked
items 3, 6 and 7 and the back-tests. The operator decides. The revised recommendation:

| Item | Before | Now | Change at 48 / 11 | Reason |
|---|---|---|---:|---|
| 1, 2, 4 | in | in | −1.69 / −1.69; +1.64 / +1.11; −0.35 / −0.53 | unchanged |
| 3 | in | in, relabeled | −3.20 / −3.10 | Calibrated to IRS totals by AGI bin; the group's share inside each bin stays the CPS's, as in the current key. "Measured on tax records" overstated it. The $500k+ pooled reading gives the same +$3.10bn (SE 0.5) and leans less on the 15 group records from $1M. |
| 5 | in | in, framing-sensitive | −27.19 | The structures' tax, about four-fifths, is lost in every long-run reading with full capital adjustment. The land part turns on framing: a consolidated fiscal reading gives r = 1 (−35.91 in all). See `receipt_side_long_run_2026_09_28`, "Corrections after the cross-lab review". |
| 6a | in, within-group rule | in, proportional rule | +0.39 / +0.53 | The within-group rule rests on CBO's shares carrying measured compliance. CBO computes payroll taxes from income and takes nonfilers' income from the CPS (CBO 60341, App. A), so they do not. |
| 6b | in | out | 0 | the same |
| 7 | in, three lines | in, workers' compensation only | −0.95 / −0.73 | The "z down to −4.8" was a ratio-scale statistic taken at the low ratio. On the difference scale the extremes are −2.6 / −2.1, and the six years fit one mean, so pooling stands. Temporary disability and black lung are ASEC disability or survivor income (DIS_SC1 codes 9 and 8), not WC_VAL; re-keying them is open. |
| 8, 10 | beside | beside | | unchanged |

Items 1–5, 6a under the proportional rule and 7 for workers' compensation only come to **about $290.5bn / $355.8bn**
at 48 / 11. That is the sum of each item alone on the September 27 case, not yet run as a set; apart from items 3 and 6
(−0.004), the items add to within $0.01bn. [CALCULATION: `derived/fixed_specs.csv`, item rows; the split of item 7
from `backcast_pandemic_measured_2026_09_28` (52.75% of the three nationals is temporary disability and black lung)]

**The pension switch after the review** (`pension_accrual_2026_09_28` at a238f19; this package still pins
c9d0077 until the adoption re-pin):
- The lane now nets the income tax the group will pay on the benefits it accrues. Under current law (the 2025 tax
  law, per SSA's Chief Actuary) the central is $433.46bn / $493.52bn on the September 27 case, +$111.64bn / +$106.15bn.
  Gross it was +$116.01bn / +$110.41bn.
- The switch must read `ratio_net` (1.241), not the gross `central_decomposition.low.accrual_per_tax_dollar` this
  package reads, and drop `benefit_tax.current_receipt_bn` ($2.09bn / $1.82bn) from the federal income tax line.
  The adoption re-pin does both. The stale comment at `main_case.cjs` line 20 (bec1cd7's +121.9 / +116.3) goes with
  it.
- The revised set with the switch comes to **about $402bn / $462bn**. The sum is approximate: 6a's self-employment
  item moves accrual with the SE tax, about −$0.3–0.4bn with the switch on.
- The switch prices every change in the group's OASDI receipts at the group's average ratio. The pension lane
  credits unauthorized workers' on-books taxes at 10%, so an item that moves only their receipts is overpriced
  there. It was 6b's +$0.74bn interaction, which leaves with 6b.

**Existing-case items found on the way** (not in any set):
- The federal transit operating-subsidy crossing understates the cost. If BEA books federal transit operating aid
  as subsidies (unverified), it is about +$0.5–1.2bn; at most +$2.89bn (v2's bound).
- Temporary disability and black lung are keyed on WC_VAL.

## Log (append-only)

- 2026-09-28 09:12 JST: stub written after reading `BRIEF.md` (0a83245). Candidate `sept28_candidate_v3` on candidate
  v2 (`main_case_candidate_v2_2026_09_28`, 08d9a86); neither v2 nor the adopted September 27 case is edited. Items 1–8
  first; the pension switch (item 9) waits for the parent's commit of `pension_accrual_2026_09_28`. Worker: mainbuild,
  model claude-opus-5-5.
- 2026-09-28 10:13 JST: item 8's premise checked against the case. `fed_transit_and_railroad` ($0.094bn) and
  `sl_transit_and_railroad` ($0.000bn) sit inside `economic_affairs_services` at the resources key (0.0810), not the
  population key [DATA: `service_response_long_run_2026_09_27/derived/responses.json` via the package's `LR`; model.json].
  The population-keyed transit money is NIPA 3.8 line 14, S&L public transit's current surplus (−$66.69bn) inside
  `enterprise_surplus` at the corrected population key (0.1172), and its capital `ent_transit_sl` ($505.80bn charged)
  [DATA: `capital_return_services_2026_09_27/derived/enterprise_surplus_vs_return.csv`, `engine_components.json`].
  Item 8 re-keys those two; the $0.094bn stays where it is.
- 2026-09-28 10:13 JST: transit key built by a subagent (`transit_acquire.py`, `transit_key.py` →
  `derived/transit_key.json`, `transit_key_states.csv`; 25 gates pass; two harness runs identical). I recomputed the
  three relative uses from `transit_key_states.csv` independently: 0.746518 (commuters), 1.018848 (state-deficit
  weighted), 1.168722 (capital-outlay weighted); ΣD $55.53bn [CALCULATION]. The group is 8.65% of transit commuters and
  11.59% of persons; deficit per resident transit commuter is about $5k in New York against $19k in California
  [CALCULATION]. Weighting by where the deficit falls reverses the brief's −$2.2bn estimate.
- 2026-09-28 10:19 JST: items 1–9 built in `package.cjs` on v2's package and the receipt-side `items.cjs`, both
  imported unchanged. The pension switch reads the lane at bec1cd7 through `git show`. That commit was found in the log;
  the parent has not yet messaged a validated commit, so the switch-on numbers are pre-validation. Each item alone
  reproduced its lane at the first run (items 4, 5, 6a, 6b and 9 exactly).
- 2026-09-28 10:28 JST: the first `main_case.cjs` run failed four gates, none of them in the candidate:
  - 6b's expected value had its sign reversed in the gate (row 2 removed costs less under the within-group rule, so the
    swap lowers the cost);
  - the workers' compensation check was tighter than the csv's 10 significant digits;
  - two range gates demanded an exact 0 where the joint reading carries 2.5e-14 of float cancellation.
  All three were fixed at their input precision, and all 47 gates then passed.
- 2026-09-28 10:37 JST: `rerun_lane.py`, first pass IDENTICAL 21/21 but exit 3: `package.cjs` is a module, not a
  command. Two further passes with `--allow-unrun package.cjs`: IDENTICAL 21/21, rc 0, both.
- 2026-09-28 10:39 JST: verdict written. The log's times were checked against file mtimes and corrected in place
  before the file was first reported (the stub had been written as 09:20, the two 10:13 entries as 10:25). Nothing outside this directory was edited; nothing was committed, staged or
  stashed.
- 2026-09-28 10:51–11:01 JST, from file mtimes, because the worker's session ended before it logged them: item 10 was
  built. `uninsured_use_slope.py` dates from 10:51 and the switch in `package.cjs` from 10:52; `main_case.cjs` ran at
  11:01 with the pension still pinned at bec1cd7.
- 2026-09-28 11:12 JST (parent, after the session restart): `PENSION_COMMIT` changed from bec1cd7 to c9d0077. That is the
  validated lane: the national check passed at bc071ba, Part A's spouse credit was removed, and c9d0077 adds the
  labels. Reran `uninsured_use_slope.py` (7 gates), `road_congestion.py` (9), `main_case.cjs` (54) and
  `sign_reversal.cjs` (16); every gate passes. The switch-on figures, item 10 and the gate counts above were updated
  in place. The candidate with the switch on is $404.46–464.39bn, against $410.38–470.32bn at bec1cd7.
- 2026-09-28 11:17 JST (parent): two `rerun_lane.py` passes with the command above, now including `uninsured_use_slope.py`: IDENTICAL 23/23, rc 0, both.
- 2026-09-28 13:48 JST (parent): section "After the cross-lab review (parent, 2026-09-28)" added: revised recommendation (items 1–5,
  6a under the proportional rule, 6b out, item 7 on workers' compensation only; about $290.5 / $355.8bn cash, about $402 /
  $462bn with the net accrual), what the adoption re-pin must change, and two existing-case items. Text only; no
  script or output changed.
