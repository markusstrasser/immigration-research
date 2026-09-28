claude-opus-5-5

**Verdict:** Run as one set, the operator's pending bundle costs **$371.41–434.84bn** at specifications 48 / 11 with
the pension switch on (payable benefits, net of the tax on benefits). That is $9,353–10,950 per member of the account's
39,712,493 people. With the switch off (the cash set) it costs **$294.70–361.82bn**, or $7,421–9,111 per member.
Specifications 48 and 11 remain the ends in both fill-in methods, so the set's own band is the same.

The items nearly add. The set's interaction is −$0.47 / −$0.50bn with the switch and +$0.09 / +$0.08bn cash, and all of
it is pairwise. One pair exceeds $0.1bn: payroll compliance (6a) with the pension switch, at −$0.56 / −$0.58bn. The
accrual follows the OASDI receipts, and 6a lowers them. The parent's hand total ($368 / $429bn plus the two lanes, about
$372.1 / $435.0bn) was $0.7 / $0.1bn high for two reasons: "$368bn" rounds up by about $0.5bn, and this pair is about
twice v3's scaled estimate.

Four lines take two or more items: personal motor vehicle licences, general sales tax, selective excise and federal
income tax. Two more reads cross items: the accrual's OASDI receipts and the road key's freight part. Each composition
rule is an option, and each alternative is reported beside the rule chosen. Against its alternatives, the chosen rule
moves the set by less than $0.1bn except in three places:
- the accrual's read, ±$0.56–0.58bn;
- the Part A read, −$0.17 / −0.19bn;
- the two extreme licence rules, +$0.69bn and −$0.26 / −0.14bn.

Every gate passes, and two `rerun_lane.py` passes are byte-identical. Nothing is adopted. [CALCULATION: `main_case.cjs`
→ `derived/`]

## The set at 48 / 11

$bn. Each row is one run of the engine and the capital return with every item on at once. "Mean" is the two fill-in
methods averaged, as v3 reports it. Per member uses the row-4 union headcount, 39,712,493.33
(`main_case_candidate_2026_09_28/derived/production_row4.json`, `populations.row4`). [CALCULATION: `derived/bands.csv`]

| Case | Hot-deck (union, matched) | Matched over pooled | **Mean** | Per member |
|---|---:|---:|---:|---:|
| September 27 case (adopted) | 318.58 / 385.11 | 325.06 / 389.63 | 321.82 / 387.37 | $8,104 / $9,754 |
| **v4 set, pension switch on** | 367.31 / 431.97 | 375.52 / 437.71 | **371.41 / 434.84** | **$9,353 / $10,950** |
| **v4 cash set** | 291.39 / 359.46 | 298.01 / 364.18 | **294.70 / 361.82** | **$7,421 / $9,111** |

- **Change from the September 27 case:** +$49.60 / +$47.47bn with the switch; −$27.12 / −$25.55bn cash.
- **Ends.** In both methods and both sets, 48 is the cheapest of the 32 distinct specifications and 11 the dearest.
  The runners-up are 56 (+$0.79bn above 48) and 3 ($0.81bn below 11), as in v3.
- **The set** is:
  - v3's items 1–5 unchanged;
  - 6a under the payroll lane's proportional rule, with 6b off;
  - item 7 on the workers' compensation line only;
  - the pension switch at payable benefits: `ratio_net` 0.973667, Part A accrual $41.137bn, and the benefit-tax
    receipt dropped from federal income tax, $2.091bn shared and $1.817bn personal;
  - state pricing's central package;
  - roads keyed by miles at the 2017 south-western NHTS ratio.

## Attribution

Change at 48 / 11, $bn. "Alone" is the item on the September 27 case. "Marginal" is the set less the set without the
item. [CALCULATION: `derived/attribution.csv`, `pairwise.csv`]

| Item | Alone | Marginal in the set | Interaction | Marginal, cash set | Interaction, cash |
|---|---:|---:|---:|---:|---:|
| 1. Public housing's deficit, tenant key | −1.691 / −1.691 | same | 0 | same | 0 |
| 2. Production on the account's weights | +1.643 / +1.107 | same | 0 | same | 0 |
| 3. IRS-matched income-tax key | −3.201 / −3.097 | −3.192 / −3.085 | +0.008 / +0.012 | −3.192 / −3.085 | +0.008 / +0.012 |
| 4. Public housing's capital, tenant key | −0.353 / −0.529 | same | 0 | same | 0 |
| 5. Long-run property taxes | −27.186 / −27.186 | same | 0 | same | 0 |
| 6a. Payroll compliance, proportional rule | +0.387 / +0.527 | −0.139 / +0.000 | **−0.525 / −0.527** | +0.424 / +0.583 | +0.038 / +0.056 |
| 7. Workers' compensation line, pooled | −0.948 / −0.732 | same | 0 | same | 0 |
| Pension switch (payable, net) | +77.277 / +73.606 | +76.714 / +73.023 | **−0.563 / −0.583** | | |
| State pricing, central package | +2.185 / +2.271 | +2.205 / +2.268 | +0.021 / −0.004 | +2.205 / +2.268 | +0.021 / −0.004 |
| Roads keyed by miles | +1.956 / +3.693 | +2.072 / +3.798 | **+0.116 / +0.105** | +2.072 / +3.798 | **+0.116 / +0.105** |
| Sum of the items alone | +50.067 / +47.970 | | | −27.209 / −25.637 | |
| **Joint change** | **+49.595 / +47.471** | | **−0.472 / −0.499** | **−27.118 / −25.553** | **+0.091 / +0.084** |

The pairwise interactions on the September 27 case add to the joint interaction exactly; higher orders are 0 (1e-13).
Five pairs are nonzero:

| Pair | Interaction | Where |
|---|---:|---|
| **6a × pension** | **−0.563 / −0.583** | `social_security`: the accrual reads the OASDI receipts 6a moves |
| 6a × roads | +0.062 / +0.077 | excise (+0.034 / +0.033) and the road key's freight part (+0.029 / +0.044) |
| state × roads | +0.053 / +0.028 | personal motor vehicle licences |
| 6a × state | −0.033 / −0.032 | general sales tax |
| 3 × 6a | +0.008 / +0.012 | federal income tax: 6a's ratio applies to item 3's shift |

**Interactions above $0.1bn.**
- **6a × pension is the only pair above $0.1bn.** Under accrual, `social_security` is 0.974 times the group's OASDI
  receipts. The proportional rule cuts the group's self-employment tax by 11.97% (personal) and 10.63% (shared), and
  raises employee and employer OASDI by about 0.05%. The accrual follows those receipts. Misreported self-employment
  income pays no tax and earns no benefit credit. Cash accounting counts only the lost tax. Accrual nets 97% of the
  OASDI part of it (80% of self-employment tax) against the lost benefits; the HI part is not netted, because the Part A
  accrual is fixed. So 6a's marginal falls from +$0.39 / +0.53bn alone to −$0.14 / +0.00bn in the set.
- **Roads' item-level interaction** is +$0.12 / +0.10bn, in both sets. It adds two pairs, neither above $0.1bn:
  6a × roads (+$0.06 / +0.08bn) and state × roads (+$0.05 / +0.03bn).

## Lines two or more items touch

**The search.** The scan in `main_case.cjs` compares each item alone with the September 27 case at every
specification and method. It checks every receipt and spending line, capital component and production term, and
lists what moves.
- Each item moves exactly its named lines (gate).
- The set moves only their union: 35 lines, or 33 cash.
- Four lines are moved by two or more set items.

A read is a rule that takes one item's input from a line another item moves. The reads were found in the code and are
listed after the four lines. For every line in the set, `derived/line_interactions.csv` gives:
- the line's change;
- the sum of the items' changes alone;
- the difference.

The differences add to the set's interaction (gate, 1e-9).

Amounts are the group's, $bn at 48 / 11 (mean). Cost effects are the set's cost under the alternative less its cost
under the chosen rule. [CALCULATION: `derived/overlaps.csv`, `summary.json` `overlaps`, `rules`]

**1. Personal motor vehicle licences** (receipt, $26.125bn, all S&L). The September 27 case keys them by adults:
$2.848 / $2.752bn.
- *State pricing:* multiplies the group's amount by the state index, 1.2624, mostly California's vehicle licence fee.
  Alone that is +$0.747 / +0.722bn.
- *Roads:* re-keys the line from adults to the group's share of driver miles, 10.12%. Alone that is −$0.203 / −0.107bn.
- **Chosen: the index applied to the miles-keyed amount**, 26.125 × 0.1012 × 1.2624 = $3.339bn at both ends. The
  index is a price and the miles share a quantity. The index weights states by the group's adults, so the rule assumes
  the group's miles are spread across states like its adults.
- Against the two lanes' changes added, the line costs +$0.053 / +0.028bn.

| Alternative | Cost effect on the set |
|---|---:|
| Additive: each lane's change on the adults key | −0.053 / −0.028 |
| Miles only: the state index dropped on this line | +0.694 / +0.694 |
| Index only: the line left at the adults key, state-priced (the roads lane's own variant) | −0.257 / −0.135 |

**2. General sales tax** (receipt, $602.43bn, all S&L). September 27: $49.050bn.
- *6a:* its ratio, 1.0057 (personal) and 1.0058 (shared), scales the group's measured consumption for misreported
  income. Alone that is +$0.285 / +0.277bn.
- *State pricing:* the index 1.1151 reflects Texas, Arizona and others taxing sales above the US rate per PCE dollar.
  Alone that is +$5.646bn.
- **Chosen: multiplicative**, consumption × rate: $55.014 / $55.005bn. That is −$0.033 / −0.032bn against the two
  changes added.
- Alternative, additive: +$0.033 / +0.032bn.

**3. Selective excise** (receipt, $371.262bn). September 27: $30.141bn.
- *6a:* its ratio, 1.0057 / 1.0058, on the whole line. Alone that is +$0.175 / +0.170bn.
- *Roads:* the gasoline part, $71.711bn, moves from the consumption key to the miles share. Alone that is +$1.438bn.
- **Chosen: gasoline at the miles share, with 6a's ratio on the rest**: $31.720 / $31.716bn. Miles are measured
  driving, not consumption inferred from income, so 6a's income-misreporting ratio has nothing to scale on the
  gasoline part. Against the changes added this is +$0.034 / +0.033bn.

| Alternative | Cost effect on the set |
|---|---:|
| Additive: 6a's ratio kept on the gasoline part at its September 27 share | −0.034 / −0.033 |
| Multiplicative: 6a's ratio also on the miles-keyed gasoline | −0.042 / −0.041 |

**4. Federal income tax** (receipt). September 27: $111.177 / $101.447bn.
- *Item 3:* adds the IRS-matched key's shift, +$3.201 / +3.097bn.
- *6a:* its ratio, 0.9974 (shared) and 0.9963 (personal), −$0.286 / −0.377bn alone. It applies after item 3, in v3's
  order.
- *Pension:* drops the tax the group's 2024 benefits carry: −$2.091bn (shared) and −$1.817bn (personal).
- **Chosen: 6a's ratio on the re-keyed amount, with the benefit-tax drop fixed at the lane's dollars.** The set's
  amount is $111.993 / $102.338bn. The brief's re-pin names those dollars. The pension lane measured them on the Census
  key, and neither item 3 (a re-key by AGI bin) nor 6a says how much of its change falls on benefits. The line differs
  from the three changes added by +$0.008 / +0.012bn, all of it item 3 × 6a; the fixed drop adds exactly.

| Alternative | Cost effect on the set |
|---|---:|
| Benefit-tax drop scaled by the group's income tax, set over September 27 | +0.055 / +0.049 |
| 6a's ratio on the September 27 amount, added to item 3's shift | −0.008 / −0.012 |

**Reads across items:**
- **The road key's freight part.** The roads lane keys 28.3% of highway cost at the consumption key, which it reads
  from the excise line. 6a raises that key by its ratio.
  - **Chosen: the set's own consumption key**, so the account keeps one consumption key.
  - Effect in the set: +$0.029 / +0.044bn, in `roads_vmt_sl`, `hwy_sl` and, at the high end, the federal parts.
  - Alternative (the September 27 key): −$0.029 / −0.044bn.
- **OASDI receipts → `social_security`.** 6a moves employee and employer OASDI (×1.0005) and self-employment tax
  (×0.8803 personal, ×0.8937 shared). The accrual is `ratio_net` × those receipts.
  - **Chosen: the set's receipts** (v3's rule). OASDI benefits depend on credited earnings.
  - Effect: −$0.563 / −0.583bn.
  - Alternative (the September 27 receipts): +$0.563 / +0.583bn.
  - Limit: the rule prices each dollar at the group's average ratio (0.974). The pension lane credits unauthorized
    workers' on-books taxes at 10%, so whose self-employment tax 6a moves matters [INFERENCE].
- **HI receipts → the Part A accrual.** 6a moves the HI receipts. The switch keeps the lane's Part A accrual fixed,
  $41.137bn at both allocations, although the case's HI receipts differ between them ($31.28bn and $29.15bn).
  - **Chosen: fixed** (v3's rule). Part A benefits depend on insured status (40 quarters), not on the amount of HI tax
    paid.
  - Alternative (scaled by the group's HI receipts, set over September 27): −$0.169 / −0.188bn.

**Lines the brief named that one item moves:**
- **Highway spending.** Only roads moves it: two synthetic lines on top of `economic_affairs_services`, whose own key
  does not move, so `air_fed` stays keyed as before. Its one cross-item read is the freight part above.
- **The road capital return** (`hwy_sl`, `hwy_fed`). Only roads re-keys it, at the road key, with the same read.
- **Public order and safety.** Only state pricing moves it: a synthetic line at the parent's `use` key and response 1.
  - No other item moves the line or its key, so `pos_sl` and `pos_fed` keep the September 27 key.
  - The state-pricing lane priced current spending only. If the S&L capital on public order and safety, health and
    recreation took the same indexes as their S&L spending, the set would rise by +$0.26 / +0.39bn:
    - public order and safety, +0.084 / +0.127;
    - health, +0.104 / +0.156;
    - recreation, +0.071 / +0.112.
  - This sits beside the set, not in it [CALCULATION: `summary.json` `beside.state_price_on_sl_capital_bn`].
- **Two lines item 5 makes live that state pricing left national.** The state-pricing lane left
  `tenant_occupied_property` and `personal_property_tax` national because they respond at 0 in the September 27 case.
  - Under item 5 they respond at 0.708 and 1: the group's receipts are $6.81bn and $1.33bn.
  - The lane's reason no longer holds in the set, and no state index for them exists. They are unpriced by state
    **[GAP]**.
  - Item 5 keys personal property tax by household vehicles (10.21%), while roads keys licences by miles (10.12%). These
    are two lines and no overlap, noted for consistency.

## Beside the set

v3's items 8 and 10, not in the set [CALCULATION: `derived/bands.csv`, `summary.json` `beside`]:
- **8, transit at the riders' key:** +$0.170 / +0.181bn alone, the same on the set and on the cash set. The set with it
  costs $371.58 / 435.02bn; the cash set with it, $294.87 / 362.00bn.
- **10, hospitals' uninsured use at 0.7×:** −$1.534 / −2.242bn alone, the same on both sets. The set with it costs
  $369.88 / 432.60bn; the cash set with it, $293.17 / 359.58bn.

## Against the hand composition

- **Cash.** v3's revised items, each alone and summed, give $290.47 / 355.77bn. Adding the two lanes gives
  $294.61 / 361.73bn. The run gives $294.70 / 361.82bn; the +$0.09 / +0.08bn difference is the cash interactions.
- **With the switch.**
  - The items alone sum to $371.89 / 435.34bn. The run gives $371.41 / 434.84bn; the −$0.47 / −0.50bn difference is the
    interactions.
  - The parent's composition ($368 / $429bn, then the lanes) comes to about $372.1 / $435.0bn, $0.7 / $0.1bn above the
    run. Unrounded, v3's figures with its −$0.25bn midpoint give $367.5 / $429.1bn, so about +$0.5 / −$0.1bn of the gap
    is rounding.
  - The rest is the 6a × pension pair: −$0.56 / −0.58bn, against v3's scaled −$0.2–0.3bn. v3 scaled the within-group
    rule's interaction, but the revised 6a uses the proportional rule. That rule's self-employment ratios are
    0.880 / 0.894, against 0.927 / 0.942 [DATA: `payroll_compliance_2026_09_28/derived/items.json`].

## Gates (all pass)

`main_case.cjs`, 19 gates, 102 option sets [DATA: its console output]:
- **Every item off.** The set is the September 27 case at all 64 specifications in both methods: exactly against its
  own package, and against its committed `per_spec.csv` (128 rows). Its band is $321.82–387.37bn at 48 / 11
  (`summary.json` `main_case`, 1e-9).
- **Specifications.** Every option set has 32 distinct specifications, and 48 ≡ 52, 11 ≡ 15.
- **v3's items reproduce v3.** Items 1–5, 6a (proportional), v3's three-line item 7, and items 8 and 10, plus v3's
  candidate, match v3's `derived/summary.json` `at_fixed_specifications` (change and new at 48 / 11; max |diff|
  5.7e-14, gate 1e-6). That summary carries the same rows as `fixed_specs.csv` at full precision. Against
  `fixed_specs.csv`'s four printed decimals the gap is 4.9e-5.
- **Item 7 on one line.** The change is the line's response × (ratio − 1) × its amount at every specification (7.6e-14).
  v3's three-line item is the same formula on the other two lines as well. Alone, item 7 is −$0.948 / −0.732bn,
  against the parent's hand split of −$0.95 / −0.73bn.
- **Pension alone** gives the lane's payable central, $399.096 / $460.976bn, the printed $399.10 / $460.98bn. It was
  checked against `pension_accrual_2026_09_28/derived/summary.json`, `case_on_accrual_net_bn`, read at 9ea1beb (identical
  at HEAD and in the working tree): |diff| 5.7e-14 (gate 1e-6).
  - `social_security`, `medicare` and federal income tax sit at their formulas at every specification, alone and in
    the set (0.0).
- **State pricing alone** gives 2.184555874 / 2.271331215 against `net_state_correction.csv`'s 2.184555863 /
  2.271331204: |diff| 1.1e-8.
  - The tolerance is the rounding bound of the lane's printed inputs, 6.5e-8, because its CSVs print 10 significant
    digits.
  - Each re-priced line matches `corrections.csv` and `receipts_corrections.csv` (1e-8).
  - Each synthetic line sits at its formula (1e-12) and at its parent's response (exact).
- **Roads alone** gives +1.9559713 / +3.6930753 against `roads_mileage_key_2026_09_29/derived/summary.json`
  `by_ratio.2017_southwest.cost_change_bn`, +1.955971 / +3.693075 (6-decimal file, |diff| 3.2e-7).
  - Its four parts match (1e-6), and the keys match `keys.csv` (5.0e-7).
  - The synthetic lines and road capital take the subfunctions' responses and the road key (exact).
- **National totals** are the September 27 case's on every line an item re-keys, in every option set and method (4.5e-13
  over 132,504 cells). Three items' own lanes change a national amount:
  - item 1 lowers `housing_subsidies` by the consolidated $5.258bn and splits `housing_enterprise_surplus` out of
    `enterprise_surplus`;
  - item 5 splits `tenant_occupied_property` out of `remaining_production_property`;
  - item 8, beside, splits out `transit_enterprise_surplus`.

  Each split line sums to its old line less the consolidated subsidy. The five synthetic lines have national 0, and
  every cell keeps its September 27 partition.
- **The rules.** In both sets, each overlapping line sits at its chosen rule's formula at every allocation and method
  (3.6e-15).
- **Sums.** The line contributions sum to each cost (1.1e-13), and the line interactions to each set's interaction.

`scripts/rerun_lane.py`, two passes: IDENTICAL 10/10, rc 0, both.

## Not done

- **Not rerun on v4:** the outer range, public pay, the road arm with congestion and the sign break-even. v3 carries
  them on its own set.
- **The inputs' own open points carry over:**
  - roads' NHTS ratio: +$0.88 to +$2.06bn at the low end;
  - state pricing's jails and county level;
  - the pension lane's scheduled arm and the unpriced interest on the existing liability.
- **Adoption payload** (specified, not built). It would need four things beyond v3's D–G:
  - item 7 as one spending edit;
  - the pension as spending edits, a receipt edit on federal income tax, and v3's accrual block in `meta` with
    `ratio_net` and the benefit-tax receipt;
  - state pricing as three synthetic spending lines at their parents' responses and two receipt edits;
  - roads as the roads lane's two synthetic lines, two receipt edits and a road-key override for `hwy_sl` and `hwy_fed`
    in `meta.capital_return`.

  Consumers that gate the payload's edit set or line responses change as v3's table says.

## Files

- `package.cjs`: the definitions. It imports v3's package unchanged, which imports v2, the first candidate and the
  September 27 case unchanged. It holds every item and every composition rule as options.
- `main_case.cjs`: the gates and `derived/`.
- `derived/`:
  - `bands.csv`: each case per method and mean, per member, and own ends;
  - `per_spec.csv`: the 32 distinct specifications × 2 methods, with the September 27, set and cash costs, the sets
    with items 8 and 10, each item alone and each item's marginal;
  - `attribution.csv`, `pairwise.csv`, `line_interactions.csv`;
  - `overlaps.csv`: every rule chosen and each alternative, on the set and the cash set;
  - `summary.json`: everything, with input hashes.

Nothing outside this directory was edited; nothing was committed, staged or stashed.

```sh
L=infra/immigration-fiscal/main_case_candidate_v4_2026_09_29
node $L/main_case.cjs
uv run --no-project python3 scripts/rerun_lane.py $L --allow-unrun package.cjs "node {lane}/main_case.cjs"
```

## Log (append-only; times from `date`)

- 2026-09-29 05:45 JST: stub written after reading the brief (`v4_BRIEF.md` in the parent's scratchpad). Worker model
  claude-opus-5-5. Nothing outside this directory is edited; nothing is committed.
- 2026-09-29 05:57 JST: read v3 (RESULT, package.cjs, main_case.cjs), the pension decision and lane summary at HEAD
  (9ea1beb: `ratio_net` 0.973667, Part A accrual $41.137bn, benefit-tax receipt $2.091bn shared / $1.817bn personal,
  case $399.096 / $460.976bn), the state-pricing lane (central package 2.184555863 / 2.271331204) and the roads lane
  (+1.955971 / +3.693075). Plan: a v4 package that imports v3's unchanged and adds item 7 on workers' compensation
  only, the pension at payable benefits net of benefit tax, state pricing (synthetic spending lines, receipt edits) and
  roads by miles (the lane's synthetic lines, receipt shifts and road-capital re-key), with every overlap rule an
  explicit option. Candidate overlaps found by reading the code: personal motor vehicle licences (state x roads),
  general sales tax (6a x state), selective excise (6a x roads, and roads' freight key), federal income tax (3 x 6a x
  pension), OASDI receipts read by the accrual (6a x pension). A mechanical scan of every line each item moves will
  check this list.
- 2026-09-29 06:01 JST: `package.cjs` written and smoke-tested (not yet gated). Each item alone at 48 / 11, change
  from the September 27 case: 1 −1.691230; 2 +1.642719 / +1.107389; 3 −3.200535 / −3.096568; 4 −0.352869 / −0.529304;
  5 −27.186326; 6a (proportional) +0.386558 / +0.527189; 7 (workers' compensation only) −0.948248 / −0.732410; pension
  +77.276718 / +73.606405; state pricing +2.184556 / +2.271331; roads +1.955971 / +3.693075. First run of the set:
  $371.41 / 434.84bn with the pension switch, $294.70 / 361.82bn cash [UNVERIFIED until the gates in `main_case.cjs`
  pass].
- 2026-09-29 06:10 JST: `main_case.cjs` written. Its first run (between 06:01 and 06:10) failed two gates, neither in the
  set:
  - the state-pricing total at a fixed 1e-8: the recomputation from the lane's 10-significant-digit CSVs differs by
    1.1e-8. The tolerance became the rounding bound of those printed inputs (6.5e-8); the per-line check stays at 1e-8;
  - national totals: the check demanded group + other = national in every cell, but model.json's foreign and corporate
    cells do not partition by design (50 cells in the September 27 model). It now compares each cell's gap with the
    September 27 cell's, and demands 0 on new lines.

  All 19 gates then passed. `derived/` was written in place, byte-identical to a scratch `--out-dir` run.
- 2026-09-29 06:11 JST: two `rerun_lane.py` passes (command in "Files"): IDENTICAL 10/10, rc 0, both.
- 2026-09-29 06:15 JST: verdict and sections written from `derived/`. Nothing outside this directory was edited; nothing was
  committed, staged or stashed.
- 2026-09-29 06:15 JST: two more `rerun_lane.py` passes on the final files: IDENTICAL 10/10, rc 0, both. In the meantime
  b3f4d84 (the peer's general-government row) touched only `main_case_long_run_2026_09_27/main_case.cjs` and
  `main_case_bands.csv`. This lane reads neither; it reads that lane's `package.cjs`, `summary.json` and
  `per_spec.csv`.
