claude-opus-5-5

# Child credits across the group's boundary in mixed tax units

**Verdict:** The personal allocation misses a net **+$4.30bn** (SE $0.33bn) of child-credit and filing-status cost
on the recommended reading, R3. The child credits alone are +$4.00bn. The forward term is +$4.68bn (SE $0.29bn):
credits that non-member filers claim for member children, which a removal would end. It splits into $1.80bn of
nonrefundable child and other-dependent credit, $1.13bn of refundable child credit, $1.63bn of child-related EITC and
$0.12bn of care credit. The reverse term is −$0.68bn on R3: credits that member filers claim for non-member children
whose claim would continue. It is −$1.69bn if every such credit continued (R1) and −$0.59bn if only a non-member
spouse who stays could claim (R2). Head-of-household status adds +$0.32bn forward and −$0.02bn reverse. By generation
on R3: G1 −$0.02bn, G2 +$1.25bn, G3+ +$3.07bn. `derived/item.json` carries the term as `R3_with_status` for both
sets, at the personal allocation with shared 0 and both lines at response 1:
- `federal_income_tax`: −$1.775bn of the group's receipts, listed once for each of the seven `federal_liability`
  rules (`federal_gap_high_agi` is absent);
- `refundable_tax_credits`: +$2.524bn of its spending.

The term is below the review's $10bn bar, as the review expected. The review also claims that the personal total
equals sharing among members only. That holds for a split that keeps each person's weight, exactly on four keys. It
fails for the builders' unweighted split, because person weights differ inside 45% of SPM units; that split alone
moves the four lines' net cost by +$1.44bn. Beside the term, not recommended: splitting mixed joint returns between
the spouses adds +$2.28bn, with an SE of $2.97bn.
[CALCULATION: `credits.py` → `derived/item.json`, `derived/summary.json`, `derived/terms.csv`,
`derived/allocation_check.csv`]

Everything is income year 2024 on CPS ASEC 2025 tax units. Weights are audit row 4's: 39,712,493 people in the
identified union. The 3.04M added descendants are out of scope. Account dollars are the main case's. A plus sign
raises the group's net cost.

## Where the credits land today

- **One record per return.** The Census tax model puts all of a return's amounts on one record: the tax unit's
  head, or a dependent filer. A joint return's spouse carries zeros, and each joint unit has exactly two filers and
  one record with amounts [DATA: gates `one_record_per_return`, `joint_units_hold_exactly_two_filers`,
  `filers_without_amounts_are_joint_spouses_only`]. A dependent's `DEP_STAT` names the claimant, always a head or a
  dependent filer. Dependent filers claim no credits in the model: none of their 3,300 returns has any [DATA: gate
  `dependent_filers_carry_no_credits`; `summary.json` `frame.dependent_filer_returns`].
- **What the credit variables feed.** `CTC_CRD`, the nonrefundable child and other-dependent credit, and the care
  credit sit inside `FEDTAX_BC`. That is the receipts builder's `federal_liability`
  (`full_account_receipts_2026_09_20/builder.py:95`), the key of `federal_income_tax` (`:182–191`). The line is the
  tax before refundable credits (`:238`). `EIT_CRED` and `ACTC_CRD` are moved to spending: the builder checks that
  tax before less tax after equals EITC plus ACTC (`:328–331`). The spending builder keys them as `refundable_credits`
  = `EIT_CRED + ACTC_CRD` on the record (`full_account_spending_2026_09_20/builder.py:204`), the preferred key of
  `refundable_tax_credits` (`:120`). That line is $228.809bn × the household fraction 0.99005 × the share. Its
  premium-credit part, $118.35bn, is re-keyed by audit row 1, so the CPS key prices the other $110.46bn
  [SOURCE: `dataset_integrity_2026_09_23/derived/spending_mts_credits.json`, Monthly Treasury Statement Table 5].
- **The case's keys after the builder.** v4 item 3 re-keys `federal_income_tax` with a receipt edit of stack factor ×
  national × (IRS-key share − `federal_liability` share) (`main_case_candidate_v2_2026_09_28/package.cjs:109–120`).
  The edit is measured on the reference rule `cbo_collective`, and every other rule takes the same proportional
  change (`main_case_2026_09_24/package.cjs:120–136`).
  - The lane prices the tax parts on the cells of that IRS-raked key (`tax_key_heldout_2026_09_28/keys.py:102`), at
    each cell's ratio over the key's mass on row 4's weights (0.99836). So the edit is on the case's key.
  - The status stack enters per return, as the claimant's flag and on-books share. The forward returns' tax is not
    the group's, so the group's aggregate stack factor does not apply to it [INFERENCE].
- **So, at the personal allocation,** a non-member head's credits for member children are charged to other
  residents, and a member head's credits for non-member children are charged to the group. 1.993M member dependents
  sit on returns that non-members head, and 0.737M non-member dependents on returns that members head
  [CALCULATION: `summary.json` `crossing_persons_m`].

## The terms

Account $bn, SE from the 160 replicates in brackets. The forward terms do not depend on the reading.
[CALCULATION: `derived/summary.json` `account`; components in `derived/terms.csv`]

| Term | R1 | R2 | R3 | G1 (R3) | G2 (R3) | G3+ (R3) |
|---|---|---|---|---|---|---|
| A: forward child credits | +4.682 (0.290) | +4.682 | +4.682 | +0.055 | +1.514 | +3.113 |
| B: reverse child credits | −1.695 (0.195) | −0.593 (0.093) | −0.684 (0.101) | −0.080 | −0.332 | −0.272 |
| A + B | +2.987 (0.354) | +4.089 (0.310) | +3.998 (0.316) | −0.025 | +1.182 | +2.841 |
| C: forward head-of-household status | +0.317 (0.039) | +0.317 | +0.317 | +0.003 | +0.075 | +0.239 |
| Cr: reverse head-of-household status | −0.120 (0.031) | 0 | −0.016 (0.009) | −0.002 | −0.003 | −0.011 |
| **A + B + C + Cr** | +3.184 (0.370) | +4.405 (0.318) | **+4.299 (0.326)** | −0.024 | +1.254 | +3.069 |
| D: mixed joint returns split (beside) | +2.279 (2.973) | +2.279 | +2.279 | −0.578 | +0.227 | +2.630 |
| Full recomputation (all of the above) | +5.463 (2.970) | +6.685 (2.966) | +6.578 (2.968) | −0.601 | +1.480 | +5.699 |

G2's net is printed by controlled rounding (file value 1.2534), so that the printed parts add.

- **A's parts** (account $bn): nonrefundable credit +1.804, care credit +0.124, refundable child credit +1.125, EITC
  +1.629. In CPS dollars A is $3.587bn. The spending parts convert at 1.902 account dollars per CPS dollar (the
  line's non-PTC $110.46bn × 0.99005 over the national key of $57.51bn after the status rule). The tax parts convert
  at 0.90 per CPS dollar on A's returns, against a national average of 1.215 under the IRS key: the IRS cells give
  low-income returns less of the line [CALCULATION: `summary.json` `conversion`].
- **A by return type**: joint returns a non-member heads with a member spouse +2.341; joint returns of two
  non-members +0.452; unmarried heads +1.889. $0.178bn of A is on non-member heads who report Mexican origin.
- **Conservation** (CPS dollars before the status rule, R1). Of $88.84bn of nonrefundable child credit, members'
  records carry $9.82bn; the removal attribution moves $2.01bn in and $0.75bn out, so members get $11.08bn and
  others $77.76bn, adding to the total. The refundable child credit is $21.59bn: $4.61bn on members' records, +$0.61bn
  in and −$0.20bn out. The EITC is $42.62bn: $9.34bn on members' records, +$0.90bn in and −$0.34bn out
  [CALCULATION: `summary.json` `conservation`, gated].

## Which reading of the reverse term

R1's reverse terms (B and Cr, −$1.815bn) split by why the child would stay [CALCULATION:
`summary.json` `reverse_R1_by_why_the_child_stays_bn`; dependents counted equally within a return]:

| The child's other claimant after the member leaves | $bn | R2 | R3 |
|---|---|---|---|
| the claimant's non-member spouse remains (a member head's joint return) | −0.593 | kept | kept |
| a non-member parent of the child lives in the household | −0.107 | — | kept |
| none: the member filer's own child, no non-member parent present | −1.033 | — | — |
| none: another relative or an unrelated child | −0.082 | — | — |

**Recommendation: R3.** A child's credit continues only if someone stays to claim it. The household roster shows
who that could be, a non-member spouse or a non-member parent. The largest class is −$1.03bn: a member filer's own
child who is not a member, with no non-member parent present. That is the lineage's identity-loss pattern, a child
who is not reported as Mexican-origin or who fails the G3+ rule that both parents be US-born. The case has counted
such descendants as whole members since v5, so they would leave with their parents and their credits would end.
R1 is the bound if every such child stays and someone claims them at the same credit [INFERENCE].

## How to apply it to the case (`derived/item.json`)

The item is `R3_with_status`: A + B + C + Cr on reading R3. It applies to both sets, because these are current-year
flows. Values are unrounded in the file. [CALCULATION: `derived/item.json`, gated against `summary.json`; its sha256
is in the Log]

- **`net_bn.personal`**: +4.2985 (SE 0.3258). **`by_generation`**: G1 −0.0237, G2 +1.2534, G3plus +3.0689.
- **`parts`**: 18 pieces, the terms A, B, C and Cr by side and generation.
  - A part's `bn` is its change to the group's target on its line, so the receipt parts add to the receipt edit and
    the spending parts to the spending edit. Its `cost_bn` is its effect on the net cost; for a receipt part that is
    minus `bn`.
  - In cost terms, the receipt side is A +1.928 (nonrefundable and care credits), B −0.454, C +0.317 and Cr −0.016,
    together +1.775. The spending side is A +2.754 (refundable child credit and EITC) and B −0.230, together +2.524.
- **`edits`**, the two fixed edits with shared 0:

| Edit | `by.personal` | `by.shared` |
|---|---|---|
| `receipt`, `federal_income_tax`, once each for `cbo_collective`, `corporate_all_capital`, `medicare_income_weighted`, `nas_80`, `property_residual_consumption`, `public_assets_tax_base` and `treasury_815` | −1.775 | 0 |
| `spending`, `refundable_tax_credits`, key `refundable_credits` | +2.524 | 0 |

  - `federal_gap_high_agi` is absent: its key, `observed_liability_plus_positive_gap_high_agi`, is not computed
    here.
  - The seven `federal_liability` rules share the reference's group target exactly, so the case's proportional rule
    gives each the same edit (`main_case_2026_09_24/package.cjs:120–136`; gated).
- **`lineage`**: the G3+ term per identified G3+ member, $213.97 (the G3+ term of $3.0689bn over 14,342,575). The
  rule: the v7 lane applies it to the lineage's G3+-priced members, the later losses plus (1 − C3) of the G3-rate
  attriters; the white-priced part takes 0, not measured.
- **`arms`**, each with its generations and its two edit amounts:
  - R1_with_status: +3.1836 (SE 0.3699);
  - R2_with_status: +4.4055 (SE 0.3181);
  - R3_without_status: +3.9976 (SE 0.3163).
- **`gates`**: 83, each with its value, all passed.
- **Responses.** `federal_income_tax` is a direct receipt and `refundable_tax_credits` a household transfer. The
  engine passes both at 1 (`assumption_explorer_2026_09_21/engine.js:40`, `:43`, `:165`, `:202`), so the edits add
  $4.30bn to both ends of both sets [INFERENCE for the cash set: current-year flows].

## Personal allocation and sharing among members only

**Person-level keys,** where the two allocations differ:
- The spending builder's `dollars` (`full_account_spending_2026_09_20/builder.py:202–205`): `SS_VAL`, `SSI_VAL`,
  `PAW_VAL`, `UC_VAL`, `VET_VAL`, `WC_VAL`, `WSAL_VAL`, `EIT_CRED + ACTC_CRD` and their cash sum. At the personal
  allocation a person keeps the record's value. At the shared allocation the SPM unit's sum is split equally
  (`equal_unit_share`, `:167–169`, applied at `:241`).
- The receipts builder's vectors (`full_account_receipts_2026_09_20/builder.py:89–99`): wages and OASDI wages,
  self-employment payroll, FICA workers, capital, interest and dividends, `FEDTAX_BC`, high-AGI liability,
  `STATETAX_A` ≥ 0, Medicare enrollment and its income weight. At the shared allocation the SPM unit's sum is split
  equally (`:120–122`; the unit is `SPM_ID`, `build/analyze_cps_fiscal_2025.py:119`, split at `:74`).
- The tax-unit amounts `FEDTAX_BC`, `EIT_CRED` and `ACTC_CRD` are person-level here, because the Census model puts
  them on the head's record.

**Unit-level or per-person keys,** the same under both allocations:
- The spending builder's `units` (`:206–207`): `SPM_SNAPSUB`, `SPM_ENGVAL`, `SPM_WICVAL`, `SPM_CAPHOUSESUB` and
  `SPM_RESOURCES`, each the unit's value over its size (`:198–201`), exported unchanged under both (`:242`).
- Its counts (`ages`, `:208–211`) and MEPS expected payments (`medical`, `:212–227`), also unchanged (`:243–244`).
- The receipts builder's `consumption`, `SPM_RESOURCES` over unit size (`:84–85`), and its counts `population` and
  `adults`.

The test runs on the builders' own weights (pwwgt0) and union. It reproduces `model.json`'s personal and shared
shares to 5e-9 for four keys.

| Key (line) | shared | members only, builders' split | shared, weight-keeping split | members only, weight-keeping split |
|---|---|---|---|---|
| `refundable_credits` (`refundable_tax_credits`) | +3.262 | +1.458 | +1.862 | 0 |
| `social_security` (`social_security`) | +2.803 | +0.676 | +1.688 | 0 |
| `federal_liability` (`federal_income_tax`) | +9.736 | +0.238 | +8.699 | 0 |
| `wage_oasdi` (`employee_oasdi`) | +2.827 | +0.452 | +2.277 | 0 |

Each cell is the change in the group's target on the line against the personal allocation, in $bn. The
weight-keeping split gives each person the weighted mean of the persons sharing with them. [CALCULATION:
`derived/allocation_check.csv`, gated]

- **The claim holds for a weight-keeping split.** Sharing among members only then reproduces the personal share
  exactly (gated to 1e-12 on all four keys). The group's total is the sum of its members' own values, whatever
  happens inside the group.
- **It fails for the builders' split.** The builders split a unit's unweighted sum equally, then weight each person
  by their own CPS weight. Person weights differ inside 44.6% of SPM units, so that split moves the group's share
  even when the sharing stays among members. Against the personal allocation it moves refundable credits by
  +$1.46bn, Social Security by +$0.68bn, federal income tax by +$0.24bn and employee OASDI by +$0.45bn: +$1.44bn of
  net cost on these four lines.
- **The review's mechanism.** The review says the whole shared-minus-personal difference is a transfer across the
  lineage's boundary. That holds for the weight-keeping split. With the builders' split, shared minus personal on
  these four lines is −$6.50bn of net cost: −$7.43bn is the transfer across the boundary and +$0.93bn the weight
  artifact.
- **For v7.** Take the group total at the personal allocation. It is members-only sharing with a weight-keeping
  split, so v7 needs no third allocation. One built on the builders' split would fail the review's proposed gate,
  equality with the personal total on person-level keys. The shared allocation that v7 keeps for readings within
  the group carries the same artifact, and a weight-keeping split removes it.
- **What neither allocation captures.** Both leave each joint return's tax on its head and each child's credits on
  the claimant. That gap is the removal recomputation priced here: the child-credit term and, beside it, D.

## Beside, not added

- **D, splitting mixed joint returns.** A joint return's tax sits on its head, the review's other limit of the
  personal allocation. When a non-member heads the return, the tax on the member spouse's income is charged to
  others: −$10.18bn once the non-member files alone. When a member heads it, the non-member spouse's tax is charged
  to the group: +$12.46bn. The net is +$2.28bn with an SE of $2.97bn.
  - The counterfactual returns use the rate schedule at each spouse's share of income, with the Census residual
    shared the same way, converted at the joint return's IRS cell, an approximation [CALCULATION: `summary.json`
    `joint_split_D_by_head_bn`; the 1.370M and 1.181M mixed joint returns].
  - Recommendation: leave D out of the case. It is indistinguishable from zero, and pricing it well would need the
    spouse's own IRS cell and a filing model the CPS supports only roughly.
- **State credits.** State income-tax credits also cross the boundary (`STATETAX_B − STATETAX_A`). Apportioned by
  the crossing dependents, all state credits on those returns come to $0.379bn forward and $0.095bn reverse on R3
  (R1 $0.181bn). That is at most +$0.28bn net in CPS dollars, an upper bound because it includes credits unrelated to
  children. Not priced [CALCULATION: `summary.json` `state_credits_on_crossing_returns_bound_cps_bn`].

## Method

**Rules.** The 2024 rules reproduce the Census credits on every actual return (64,276 returns, 36,245 linked
dependents) before any counterfactual. Constants come from Rev. Proc. 2023-34 §3.01, §3.05, §3.06 and §3.15
[SOURCE: https://www.irs.gov/pub/irs-drop/rp-23-34.pdf, sha256 544ba41c…aae57], Schedule 8812 (2024)
[SOURCE: https://www.irs.gov/pub/irs-prior/f1040s8--2024.pdf, 8b5143ca…f977] and Form 2441 (2024)
[SOURCE: https://www.irs.gov/pub/irs-prior/f2441--2024.pdf, aaaf70ba…f4df7]. `test_credits.py` checks each
constant against the cached texts.

| Census field | Census $bn | rule $bn | positive returns within $1 | dollars on returns within $1 |
|---|---|---|---|---|
| `CTC_CRD` (all returns within $1) | 88.843 | 88.843 | 1.0000 | 1.0000 |
| `ACTC_CRD` | 21.589 | 21.589 | 0.9998 | 1.0000 |
| `EIT_CRED` | 42.624 | 42.591 | 0.9991 | 0.9992 |
| care credit vs the rate schedule's gap (51,241 returns the ordinary schedule taxes in full) | 3.084 | 3.076 | 0.9940 | 0.9981 |

[CALCULATION: `derived/validation.csv`]

- The child tax credit is $2,000 per dependent under 17 plus $500 per other dependent, less $50 per $1,000 (or part)
  of AGI over $400,000 joint / $200,000 otherwise, limited to the tax before it. The refundable part is the unused
  credit, at most $1,700 per child and 15% of wages plus self-employment income over $2,500.
- The EITC uses §32's percentages with the Rev. Proc. amounts. The phase-out runs on the greater of AGI and earned
  income, and earned income is net of half the self-employment tax. Qualifying children are dependents under 19, or
  students under 24. Investment income is limited to $11,600, and the childless credit applies at ages 25–64.
- The care credit applies Form 2441's rate to the household's child-care spending (`HCHCARE_VAL`), capped at
  $3,000 / $6,000 and at the lower earner's earnings. The Census model takes the lower rate at exact $2,000 steps.

**Counterfactuals.** Each counterfactual credit is the Census credit plus the rule's change, floored at 0, so a
return keeps the residual the rules do not explain.
- A: a non-member head's return without its member dependents, with filing status and incomes held.
- B: a member head's return without its non-member dependents, held likewise.
- C: a non-member head of household whose dependents were all members files single. Cr: the same for a member head
  of household whose dependents are all non-members, read as B.
- D: the non-member spouse's own return.

An imputed unauthorized head's EITC counts at 0 and the rest of the return at the on-books share (central:
Mexico-born 0.5263, other Latin American-born 0.5501). This is the adopted stack `row4+status_state_aware|central`.
Its four stored frame totals are reproduced exactly
[DATA: `backtest_admin_totals_2026_09_28/derived/prediction_audit.json` `asec2025_adopted`]. Non-civilian claimants (48 returns) are outside the account's frame and are left out.

**Gates.** The script stops `[BLOCKED]` on any of its 83 gates, and `item.json` lists each with its value. They
cover:
- inputs: the CPS file's sha256, the replicates joining every person;
- frame: row 4's full and replicate factors, its 39,712,493 people, the lineage's identified G3+, the adopted
  stack's flagged counts, the household fraction;
- returns: the return structure, the head-of-household rule, dependent filers carrying no credits;
- rules: the fit, zero change on the actual returns;
- terms: A and B moving tax only through credits, C and Cr changing no credit, a generation for every nonzero term,
  conservation of each credit;
- keys: the IRS key's constant cell ratios, its civilians and its sum of 1;
- allocation check: the reproduced `model.json` shares;
- the item: its sums, the seven `federal_liability` rules and the arms against `summary.json`.

`test_credits.py` adds 14 tests.

**Example, checked by hand** (`derived/example.json`). PH_SEQ 51544 is a non-member head of household, aged 40,
with wages of $25,002 and one member child, 13, of G3+.
- Tax: taxable income is $25,002 − $21,900 = $3,102, taxed at 10%: $310.
- Child credit: min($2,000, $310) = $310. The refundable part is min($1,690, $1,700, 15% × $22,502) = $1,690.
- EITC: 34% × $25,002 capped at $4,213, less 15.98% × ($25,002 − $22,720), which is $3,848.
- A: without the child, the childless EITC has phased out ($25,002 > $18,591), so A is $310 + $1,690 + $3,848 =
  $5,848.
- C: as a single filer the head owes 10% × ($25,002 − $14,600) = $1,040, so C is $730.

Every figure matches the Census fields and the script [CALCULATION: `test_credits.py::test_example_return_by_hand`].

## Limits

- [FRAMING-SENSITIVE] The removal frame holds non-members and their incomes in place. The forward term counts a
  non-member parent's lost credits as the group's cost, because other residents' taxes and transfers change. The
  operator has declined the replacement-child frame [SOURCE: `decisions/2026-10-05-main-case-v5.md`, alternative 3].
- On D's returns, A is computed with the joint return held. A + D does not depend on the order; A alone does.
- Not modeled: the three-child alternative refundable credit (the Census model does not apply it); dependent-care
  accounts; and itemizers between the single and head-of-household standard deductions in C (overstates C slightly).
  The hot-deck fill-in methods' re-imputed shares are also left out. The case's OTA translation, −$0.34bn on the
  group's refundable credits, scales the union's credit dollars by about 0.99; it is ignored here, a change under 1%
  on the spending part [DATA: `external_benchmarks_2026_09_24/derived/ota_deltas.json` `vs_audit_package_ssn_rule`,
  taken at `main_case_2026_09_24/package.cjs:363`].
- The conversion is the case's line-level convention. Each CPS dollar of EITC or refundable child credit is worth
  1.90 account dollars, because the case scales the non-PTC $110.46bn to the CPS key.
- Frame. The case puts both lines' shares on row 4 through the status stack, which recomputes every responsive key
  and direct receipt under the weight arms (`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py:817–823`). Item
  3 scales its re-key by the stack factor. The lane's sums are on row 4 too, with the IRS key's mass normalized there.
- Ages are the survey's March 2025 ages. The rules reproduce the Census model, so the fit does not test the age
  convention.

## Adjacent defects (outside this lane, not fixed)

- `cps_imputation_keys_2026_09_23/taxcalc.py:73` subtracts the EITC phase-out from the phase-in credit instead of
  from the maximum (26 U.S.C. 32(a)(2) takes the smaller of the two). That is wrong where earnings are below the
  earned-income amount and AGI is above the threshold. `:140` defines earned income without deducting half the
  self-employment tax. The module is a difference operator in the status lane; its effect there is not measured
  here.
- The builders' shared allocation does not keep weighted totals (the section above). It splits a unit's unweighted
  sum equally, and person weights differ inside 44.6% of SPM units.

## Files and reproduction

- `credits.py`: the lane. `test_credits.py`: the rules, the constants against the cached texts, the example, the
  conservation of the outputs, the item's contract and the allocation check.
- `derived/item.json`: the v7 item.
- `derived/terms.csv`: components × generation × reading. Its `returns` columns count per generation row.
- `derived/summary.json`: sets, conversions, conservation and diagnostics.
- `derived/allocation_check.csv`: personal, shared and members-only shares.
- `derived/validation.csv`: the rules' fit. `derived/example.json`: the hand-checked return.
- `_cache/` (ignored): the three IRS PDFs and their text extracts.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_credits_2026_10_14/credits.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_credits_2026_10_14/test_credits.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/mixed_unit_credits_2026_10_14 \
  "uv run --no-project python3 {lane}/credits.py" "uv run --no-project python3 -m pytest {lane}/test_credits.py -q"
```

A run takes 10–11 s of CPU (wall 9–64 s, depending on the disk cache) with a peak memory footprint under 1.5 GB
(`/usr/bin/time -l`).

## Log

- 2026-10-14 14:17:10 JST: run 2 stopped at `rule_reproduces_ctc_crd_on_every_return`. Dependent filers get no
  credits in the Census model, and the care-credit fit mask read only the head's dividends.
- 2026-10-14 14:20:30 JST: run 3, all gates pass, readings R1 and R2.
- 2026-10-14 14:29:13 JST: added the reverse status term Cr, reading R3 from the household roster, the IRS key's mass
  on row 4 (0.99836) and the diagnostics. Peak footprint 1.46 GB.
- 2026-10-14 14:40:45 JST: `rerun_lane.py` IDENTICAL 6/6, exit 0, after the D split, head-origin split and state
  bound.
- 2026-10-14 14:44:01 JST: RESULT written.
- 2026-10-14 14:49:08 JST: added the gate `dependent_filers_carry_no_credits` (62 gates);
  `rerun_lane.py` IDENTICAL 7/7, exit 0, at 14:49:52.
- 2026-10-14 14:55:21 JST: the lead's output contract arrived (derived/item.json, the case's keys, the review's members-only claim). Traced item 3's re-key
  (stack factor x national x share change) and the case's proportional rule for other receipt scenarios.
- 2026-10-14 15:03:37 JST: `derived/item.json` written with the contract's fields, gates now recorded with their
  values. Added the allocation check: the builders' shares reproduced on four keys, with members-only sharing equal
  to personal only under a weight-keeping split (79 gates, 14 tests).
- 2026-10-14 15:08:08 JST: corrected the frame limit (the stack puts both lines on row 4); `rerun_lane.py`
  IDENTICAL 9/9, exit 0, at 15:09:52.
- 2026-10-14 15:14:02 JST: the lead's decision: the item is R3 with head-of-household status, for both sets. Rewrote
  `item.json` to the revised contract.
  - `reading` `R3_with_status`; 18 `parts` (A, B, C, Cr by side and generation) that add to the two edits.
  - The receipt edit is listed once per `federal_liability` rule (seven); `federal_gap_high_agi` is absent.
  - `lineage` is the G3+ term per identified G3+ member, with the lead's rule, replacing the scaled shortcut.
  - `arms` R1 and R2 with status, R3 without; 83 gates, 14 tests.
  - A timed run spent 8 s loading and 31 s in all. The slower walls (up to 77 s on 11–12 s of CPU) came with the
    machine's swap at 9.8 of 10.2 GB.
- 2026-10-14 15:17:48 JST: `rerun_lane.py` IDENTICAL 9/9, exit 0, at 15:18:53. `derived/item.json` sha256
  2773e34d4cb02a70dd21544f915b2b83bbdc00855d24d468ed67e81e0310b5ac.
- 2026-10-14 15:22:26 JST: the lead asked what changed in `item.json` after 41ac0da5 (the lead's commit, 15:12:36).
  Diffed the two field by field: the revised contract above. The parts' `bn` is now in edit sign, with the cost sign
  in `cost_bn`; the gap rule's edit and `readings` are gone, and `sets`, `edits_note`, `lineage` and `arms` are new.
  Net, SE, generations and `beside` are unchanged (within 1e-14, from summation order). `rerun_lane.py` IDENTICAL
  9/9, exit 0, at 15:23:14; `item.json` sha256 2773e34d4cb02a70dd21544f915b2b83bbdc00855d24d468ed67e81e0310b5ac.
