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
- **Adoption payload** (specified, not built). [Built on 2026-09-29: see "Adoption payload (built, 2026-09-29)" below.
  Beyond this list it needed engine.js's three optional parts and a new capital key kind, `part_rekeyed`.] It would
  need four things beyond v3's D–G:
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

Nothing outside this directory was edited; nothing was committed, staged or stashed. [True of the first task. The
adoption-payload task edited `assumption_explorer_2026_09_21/engine.js`; see "Adoption payload (built, 2026-09-29)".]

```sh
L=infra/immigration-fiscal/main_case_candidate_v4_2026_09_29
node $L/main_case.cjs
uv run --no-project python3 scripts/rerun_lane.py $L --allow-unrun package.cjs "node {lane}/main_case.cjs"
```

## Adoption payload (built, 2026-09-29)

Candidate v4's adoption payload is built in the adopted schema, and all 46 of its gates pass. Nothing is adopted:
`meta.adopted` and `meta.decision` are null. `payload.cjs` writes two payloads:
- `derived/corrections_v4.json`: the set, with pension accrual;
- `derived/corrections_v4_cash.json`: the cash set.

A fresh process that loads only `engine.js`, `model.json` and a payload gives these results, with the ends at
specifications 48 and 11:
- the set: $371.4146–434.8410bn, or $9,353–10,950 per member;
- the cash set: $294.7011–361.8175bn.

[CALCULATION: payload.cjs; consumer.cjs]

### What a payload holds

Each payload starts with the adopted `main_case_long_run_2026_09_27/derived/corrections.json`, whose 3 lines and 278
edits are unchanged and come first. v4's parts follow.

- **`receipt_lines`** (a new field) adds two lines:
  - `housing_enterprise_surplus` (item 1): national −$45.555811bn, at the rental line's key;
  - `tenant_occupied_property` (item 5): national $83.840225bn, at the rent key 0.114667.
- **Three national-scale edits** (a new edit shape, `{side, line, national_bn}`):
  - `remaining_production_property` to $273.445297bn;
  - `enterprise_surplus` to −$7.162bn;
  - `housing_subsidies` to $55.003189bn.
- **Cell edits:** 135 in the set and 133 in the cash set. They cover:
  - 16 receipt lines;
  - `social_security` and `medicare`, in the set only;
  - `workers_compensation`;
  - the five synthetic lines.
- **`lines`** adds `roads_vmt_sl`, `roads_vmt_fed`, `state_price_public_order_safety`, `state_price_health_services` and
  `state_price_recreation_culture`.
- **`production`** (a new field) holds the row-4 grid with its dimensions. It accounts for most of the 317,807 bytes
  (the cash set: 315,374).
- **`meta`** adds:
  - nine `responses`: four receipt overrides, each equal at both readings (owner-occupied property 0.762903, tenant
    property 0.708443, personal property 1, public housing 1), and the five synthetic lines at their readings;
  - in `capital_return`:
    - `ent_housing_sl` is keyed at the rental line's key (item 4);
    - `hwy_sl` and `hwy_fed` use a new key kind, `part_rekeyed`, defined in `rule_kinds`;
  - `pension_accrual` (the set only):
    - `ratio_net` 0.973667, the Part A accrual $41.137bn and the Part A share 0.375113;
    - the OASDI share of self-employment tax, 0.803496;
    - the benefit-tax receipt: $2.091bn shared, $1.817bn personal;
    - the rule, and the source, 9ea1beb with its sha256;
  - provenance blocks: `production`, `state_pricing` and `roads_mileage_key` (constants, rules, `k_road` by method);
  - `candidate_v4` (items, rules, parts, and the items that move each line) and `status`.

The identity fields (`source`, `adopted`, `decision`, `case`, `builds_on`, `previous`) now describe v4, and
`builds_on` pins the adopted file by hash. Every other September 27 meta entry is kept. Of the September 27 responses
and capital components, only the three re-keyed components change.

**Each edit is the two fill-in methods' mean change** in its cell, from the September 27 case's model to v4's
(`package.cjs` `modelFor`), beyond any national scale. On a cell that several items touch, the edit is their
composition under the package's rules. The engine's cost is linear in every cell amount and in the production grid.
The mean payload therefore gives the methods' mean cost at each specification, as the adopted payload does. G2
confirms it.

**The road key is a rule, not a constant.**
- The package keys `hwy_sl` and `hwy_fed` by `k_road`, a number stored on its models for each method and allocation.
- The payload states the key as a rule on the evaluation instead. `part_rekeyed` is the parent line's amount over its
  national total, plus the correction line's amount over the part's national total ($201.005bn for S&L highways,
  $1.827bn for federal).
- Each synthetic line carries the part's national × (`k_road` − the economic-affairs key), so the rule returns `k_road`.
  It also follows a consumer's own evaluation, a generation's for example.
- The kind lives in `meta`, not in the engine. `consumer.cjs` implements it in one line.

### Engine change

`assumption_explorer_2026_09_21/engine.js` `applyCorrections` gains three optional parts (47 lines added, 1 changed). A
payload without them applies exactly as before.
- **`receipt_lines`:** new receipt lines, each with a national total and a cell for every incidence rule and allocation.
- **A national-scale edit, `{side, line, national_bn}`:** it scales the line's national total and every cell's group
  and other amounts, in order with the other edits. Shares hold.
- **`production`, `{dims, private_wtp_bn, induced_receipts_bn, sampling_se_bn}`:** it replaces the grid's arrays when
  the dimensions match.

Eight kinds of bad input throw, and each is gated. `test_engine.js` was not edited, because it belongs to the explorer
lane. The explorer's page (`derived/explorer.html`, ignored) inlines `engine.js` and was not rebuilt.

### Gates (46, all pass; `derived/payload_gates.json`)

- **G1.** With every item off, the builder finds nothing to add and returns the adopted payload, equal as JSON (key
  order included) and byte for byte.
  - The September 27 package's `correctionsPayload()` equals the file byte for byte.
  - Both methods' models equal the September 27 models in every cell.
- **G2.** `consumer.cjs` checked the payloads against `per_spec.csv`. It uses `engine.js`, `model.json` and the payload
  alone, with no package.
  - A payload built the same way on one method's models gives that method's set and cash costs at all 64
    specifications exactly: max |diff| 0.
  - The written payloads give the two methods' mean: max |diff| 1.7e-13.
  - The consumer's engine state equals the package's at every specification. Its capital components (key, response,
    return) equal the package's exactly.
  - The payload model equals the methods' mean model in every cell: 2.3e-13 in the set, 4.5e-13 in the cash set.
    National totals hold: each cell's group + other − national equals the September 27 payload's, scaled with its line
    (4.5e-13). The production grid is v4's exactly.
  - The payload moves exactly what the task-1 scan (`summary.json` `touch`) says its items touch: 35 entries in the
    set, 33 in the cash set. The two payloads differ only on federal income tax, social security and medicare.
- **G3.** Before the engine change, `rerun_lane.py` was IDENTICAL on:
  - `main_case_long_run_2026_09_27`: `main_case.cjs` and `sign_reversal.cjs`, 11/11 files;
  - `main_case_schools_full_2026_09_26`: 7/7 files.

  It was IDENTICAL on both again after the change.
  - `test_engine.js` prints the same bytes before and after: PASS, worst gap 4.28e-9.
  - Every earlier payload (09-24, 09-26, the schools case, 09-27) applies and evaluates exactly as with the engine at
    d710a74, the last commit that touched it. The check uses the case's 64 states; the 09-24 payload, which lacks the
    meta to build them, uses the default state.
- **G4.** Two passes of `rerun_lane.py` on this lane were IDENTICAL (15/15 files). The first pass after the engine change
  rewrote one line of `derived/summary.json`: the recorded `engine.js` hash went from 091ca312… to 055e0503….
  `payload_gates.json`, which records `summary.json`'s hash, followed. No number changed.

### Consumers

No consumer that follows the adopted case takes v4 unchanged. [INFERENCE: this comes from code reading, and no
consumer was run. A read-only survey by a subagent (claude-opus-5-5) read the 99 files that meet the brief's criteria at
each line cited here.
- I re-read these citations, and each matched: `band_variants.cjs:150-156`, winners `specs.cjs:140-152`,
  `sept24_specs.cjs:118-126`, `distribute.py:376-400`, `debt_legacy.py:494-502`, `run_generations.cjs:160-172`,
  `case_components.cjs:110-117`, `split_residual.py:64-100`, `generation_lines.cjs:36-42`, `export_lines.cjs:24-31` and
  this lane's `package.cjs:325-328`.
- The criteria: code that reads a `corrections.json`, `meta.responses` or `meta.capital_return`, reads the September 27
  lane's `main_case_bands.csv`, `summary.json` or `per_spec.csv`, or calls `stateFor` or `evaluateFull`.]

Two preconditions come before any consumer can change.
1. **A payload-first package for the adopted case.**
   - Nine consumers apply `corrections.json` themselves and then call the package's `evaluateFull` or `stateFor` on
     their own models: `run_generations`, `run_cells`, `band_variants`, `sept24_specs`, winners `specs`,
     `generation_lines`, `decompose`, `export_lines` and `engine_breaks`.
   - v4's `package.cjs` cannot serve them. Its `evaluateFull` rejects any model it did not build (`:325-328`), and it
     reads the road key from a stored constant.
   - `consumer.cjs` is the evaluator such a package needs: the state from `meta.responses`, the capital return from
     `meta.capital_return`, `part_rekeyed` included.
   - The package must also export the September 27 API the consumers destructure (`MAIN_SPECS`, `RESPONSES`,
     `correctionsPayload`, `componentsFor`, `withSyntheticLines` with the five new synthetic lines, and the rest).
2. **The September 27 output contract.** The adopted lane must write:
   - the `summary.json` fields the consumers read (bands, `responses`, `change_at_fixed_specifications`,
     `capital_at_end_specifications`, the enterprise fields, `end_specifications`);
   - `main_case_bands.csv` rows by name, with the first four columns in place, because `case_ends.cjs:74` reads them by
     position;
   - `per_spec.csv` with its capital columns.

`$F` is `infra/immigration-fiscal`, and `<case>` is the new case key. Commands run from the repository root.

| Consumer | Change at adoption | Rerun |
|---|---|---|
| `assumption_explorer_2026_09_21/engine.js` | Done here. A positive control for the three new parts belongs in the explorer lane's `test_engine.js`. | `node test_engine.js` in its directory |
| `generation_account_2026_09_24/run_generations.cjs` | Large code change:<br>• case table `:91-93`;<br>• the payload gate `:164-171` requires the tail to be the 8 re-key edits;<br>• netting `:420-449` reads `by`, which a scale edit lacks;<br>• `:499` needs a generation split of every v4 edit (tax key, payroll, property, housing split, state pricing, roads, workers' compensation, and the accrual through `meta.pension_accrual`);<br>• `:565` needs a row-4 production grid per generation;<br>• `PARTS27 :984` and `run_all.sh:36` need v4 steps. | `bash $F/generation_account_2026_09_24/run_all.sh` |
| `late_arrival_account_line_2026_09_27/run_cells.cjs` | Large code change. It copies the generation split over nine cells, so it needs the same rules:<br>• case table `:31`, with the default still `sept26_schools`;<br>• netting `:385-405`;<br>• `:431` needs row-4 production per cell;<br>• `RECEIPT_GROUPS :441` would file the tenant property tax under other receipts. | `LATE_DEF=<central\|lower\|upper> bash $F/late_arrival_account_line_2026_09_27/run_split.sh` |
| `late_arrival_account_line_2026_09_27/verify.py` (with `build_line.py:24`, `medicaid_check.py:122`) | Config: `MAIN :22`. | `uv run --no-project python3 $F/late_arrival_account_line_2026_09_27/verify.py` |
| `debt_legacy_2026_09_23/debt_legacy.py` (its own engine port) | Large code change:<br>• `apply_corrections :326` needs the three new parts;<br>• `production() :372` reads model.json's grid;<br>• the synthetic lines' responses never reach `line_responses` (`:576-595`);<br>• `capital_rows :500` stops on `part_rekeyed`;<br>• `split_corner :983` has no federal share for the new lines;<br>• `:1584` and `:1597` stop on the payload tail;<br>• case table `:299`. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/debt_legacy_2026_09_23/debt_legacy.py`; then pytest |
| `sept24_propagation_2026_09_24/band_variants.cjs` | Small code change:<br>• case table `:50-57`;<br>• it rebuilds line responses from three named entries (`:152-154`) and gates them against the package's specs (`:155`). Build them from every `meta.responses` entry instead. | `node $F/sept24_propagation_2026_09_24/band_variants.cjs --case <case>` |
| `sept24_propagation_2026_09_24/real_costs_totals.py` | Config:<br>• case tables `:105-133`;<br>• it quotes `meta.beside_the_account.congestion` (`:336`), which v4 did not recompute for roads by miles. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/real_costs_totals.py --case <case>` |
| `sept24_propagation_2026_09_24/constant_choices.py` | Config: `:50-51`. It runs after `debt_legacy.py`. | `... constant_choices.py --case <case>` |
| `uncertainty_propagation_2026_09_22/sept24_specs.cjs` | Code change:<br>• a `later_cases.json` entry;<br>• `lineTargets :62` fails on a new receipt line;<br>• `KLINES :86` lacks `housing_subsidies` and the road lines, so `:122` throws;<br>• `:125` throws on `part_rekeyed`;<br>• the model gate `:146` meets the new `housing_subsidies` national. | `node $F/uncertainty_propagation_2026_09_22/sept24_specs.cjs` |
| `uncertainty_propagation_2026_09_22/propagate.py` (with `test_uncertainty.py`) | Code change:<br>• `KCOEF_LINES :241`;<br>• the corrected enterprise national meets model.json's at `:416`;<br>• the base rebuild ignores the receipt overrides (`:440-452`);<br>• the capital rebuild `:501`;<br>• silent: the production error (`:745`) comes from model.json's grid. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/uncertainty_propagation_2026_09_22/propagate.py --case <case>`; then pytest |
| `winners_losers_2026_09_24/specs.cjs` | Small code change:<br>• case table `:59`;<br>• `:151` requires exactly 4 line responses, and v4 has 13;<br>• the `RESPONSES` gate `:142`;<br>• `:149` reads receipt overrides at `.low`, which holds because v4's are equal at both readings. | `node $F/winners_losers_2026_09_24/specs.cjs` |
| `winners_losers_2026_09_24/winners_losers.py` (with tests `:279`, `:298-299`) | Code change:<br>• `CASES :176` and the pins `:128-130`;<br>• `wages_equal_engine_P :1843` compares CPS wages with the engine's P, which row 4 moves;<br>• lines without a debt fraction stop it at `:537`. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/winners_losers.py`; `old_new.py`; then pytest |
| `historical_backcast_2026_09_20/case_components.cjs` | Code change:<br>• `CASES :27`;<br>• the fixed additions (`:62-63`) and the "no other line moves" gate (`:115`) fail on v4's lines;<br>• production is not an addition. | `node $F/historical_backcast_2026_09_20/case_components.cjs --case <case>` |
| `historical_backcast_2026_09_20/backcast.py` | Code change:<br>• `LATER_CASES :60`;<br>• `ADDITIONS :69` needs a national series for each v4 addition. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/historical_backcast_2026_09_20/backcast.py`; then pytest |
| `distribution_weights_2026_09_23/case_ends.cjs` | Path swap (`CASES :24`), once the two preconditions hold. | `node $F/distribution_weights_2026_09_23/case_ends.cjs --case <case>` |
| `distribution_weights_2026_09_23/distribute.py` | Code change, and a silent risk:<br>• `LATER_CASES :165`;<br>• `:378-400` books the whole change in the fiscal channel A on the premise that P and F never move, so v4's production item (+$1.643 / +1.107bn alone) would land in A with no gate. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/distribution_weights_2026_09_23/distribute.py`; then pytest |
| `world_ledger_2026_09_27/generation_lines.cjs` | Tiny code change:<br>• `CASES :38`;<br>• `ON27 :41` uses `evaluateFull` only for sept27;<br>• a `pins.json` entry. | `node $F/world_ledger_2026_09_27/generation_lines.cjs --case <case>` |
| `world_ledger_2026_09_27/split_residual.py` | Code change:<br>• `choices :78`;<br>• `edit_cost :67` reads `by`;<br>• the correction-only set (`:88`) comes from `lines`, so the new receipt lines fail `:99`;<br>• `:127` expects every line to move by its `by` edits. | `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/world_ledger_2026_09_27/split_residual.py --case <case>` |
| `world_ledger_2026_09_27/valuation.py` | Code change, 5 entries: `LINES :84` has no class for the synthetic lines, so `:137` stops them as unclassified. | `sh $F/world_ledger_2026_09_27/run_all.sh sept26_schools sept27 <case>` |
| `overview_2026_09_28/build.py` | Code change:<br>• `MAIN :36`;<br>• the waterfall's fixed steps (`:152`) and its sum gate (`:199`);<br>• named band rows (`:505-518`);<br>• about 20 registry rows bind September 27 paths. | `uv run --no-project python3 $F/overview_2026_09_28/build.py`; then pytest |

Some dated analyses follow the September 27 case by name. A rebase is optional; without one they stay dated records.
- `main_case_decomposition_2026_09_29/decompose.cjs`:
  - its payload gate (`:77`);
  - age rules for the new and scaled lines.
- `within_group_distribution_2026_09_29/export_lines.cjs` and `households.py`:
  - silent: `capRule` (`:29-30`) takes the capital lane's keys, not `meta.capital_return`'s;
  - `households.py` has no key vector for the synthetic lines.
- `break_conditions_2026_09_29/engine_breaks.cjs`:
  - its additions (`:65`) already hold items 5 and the pension, which would count twice;
  - `:130` passes only `lines` and `edits`.
- The Black and white comparators' `engine_lines.cjs`:
  - silent: `rekey.py:218` prices a line as national × share, so the synthetic lines, at national 0, drop out.

**Nothing needed:**
- 32 files are pinned by design:
  - the September 27 lane;
  - candidates v1–v3;
  - v4's item lanes, each priced on the September 27 base;
  - the audits and dated checks.
- 35 files read older payloads:
  - the explorer UI and figures;
  - the consumption-key lanes;
  - the older producers;
  - the September 23/24 readers.
- Five hits were false positives.

**v2's and v3's tables missed** the candidate package's model guard, `propagate.py`, `winners_losers.py`, `valuation.py`,
`backcast.py`, `overview/build.py`, the late-arrival `verify.py` and the dated analyses. v3's "none" for
`debt_legacy.py`'s capital keys no longer holds, because of `part_rekeyed`.

### What an adoption still needs

1. **A payload-first package** and the September 27 output contract, both described above. `payload.cjs` exports
   `build()`, so the adopting lane can rebuild the payload with its own `adopted` and `decision`.
2. **Code in 15 consumers**, mostly generation splits of v4's edits and a row-4 production grid per generation and
   cell.
3. **The engine change committed before `pension_accrual_2026_09_28/case_lines.cjs` runs.** Its frozen-file check
   stops while `engine.js` differs from HEAD.
4. **A note on provenance hashes.**
   - `capital_return_services_2026_09_27`, `school_capital_return_2026_09_26` and the pension lane record `engine.js`'s
     sha256, and a rerun rewrites it.
   - The adopted payload's `meta.capital_return.source` pins the capital lane's `engine_components.json` by hash.
   - So a rerun of the capital lane would ripple into the September 27 payload's meta. Only provenance would change.

### Files (this task)

- `payload.cjs`: the builder, with gates G1, G2 and the engine gates. It writes the two payloads and
  `derived/payload_gates.json` (gates, sizes, hashes and the G2 gaps), and exports `build()`.
- `consumer.cjs`: the payload consumer with no package, which generalizes the September 27 lane's independent path.
- `derived/corrections_v4.json`, `derived/corrections_v4_cash.json`, `derived/payload_gates.json`.
- `derived/summary.json`: only its recorded `engine.js` hash changed.
- Outside the lane: `assumption_explorer_2026_09_21/engine.js`.

Nothing was committed, staged or stashed.

```sh
L=infra/immigration-fiscal/main_case_candidate_v4_2026_09_29
uv run --no-project python3 scripts/rerun_lane.py $L --allow-unrun consumer.cjs "node {lane}/main_case.cjs" "node {lane}/payload.cjs"
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_long_run_2026_09_27 "node {lane}/main_case.cjs" "node {lane}/sign_reversal.cjs"
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_schools_full_2026_09_26 "node {lane}/main_case.cjs"
(cd infra/immigration-fiscal/assumption_explorer_2026_09_21 && node test_engine.js)
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
- 2026-09-29 10:36 JST: second task from the parent: build the adoption payload (`payload.cjs` →
  `derived/corrections_v4.json`, `corrections_v4_cash.json`), a consumer table and gates G1–G4. Stub section added.
- 2026-09-29 11:21 JST: the consumer survey came back from a read-only subagent (claude-opus-5-5): 99 files, 21
  follow the adopted case. Ten of its citations were re-read and matched.
- 2026-09-29 11:26 JST: baseline before the engine change. `rerun_lane.py` was IDENTICAL on the September 27 lane
  (11/11) and the schools lane (7/7); `test_engine.js` output saved.
- 2026-09-29 11:35 JST: `engine.js` gained its optional parts; `consumer.cjs` and `payload.cjs` written. The first run
  passed all 46 gates and wrote `derived/corrections_v4.json`, `corrections_v4_cash.json` and `payload_gates.json`.
- 2026-09-29 11:36 JST: G3 held after the change: both lanes IDENTICAL and `test_engine.js` byte-identical. G4's first
  pass rewrote `summary.json`'s recorded `engine.js` hash, and the second pass was IDENTICAL (15/15).
- 2026-09-29 11:38 JST: a fresh process loading only `consumer.cjs` and `engine.js` gave $371.4146–434.8410bn from the
  set payload and $294.7011–361.8175bn from the cash payload, with the ends at 48 and 11.
- 2026-09-29 11:40 JST: the section "Adoption payload (built, 2026-09-29)" was written, with bracketed pointers on the
  old bullet and on the Files line.
