# Assumption review of main case v6, 2026-10-14

**Verdict:** Two findings clear the bar, in opposite directions, and both are method questions for the operator.

1. **The low end's allocation** raises the low end. Specification 48 uses the shared allocation, which splits every
   SPM unit's taxes and person-level benefits equally among everyone in the unit, members and non-members alike. In
   units that mix the two, that credits the lineage with part of its non-member partners' taxes. The headline is the
   change for all other residents, and a removal would leave those partners and their taxes in place. With the
   personal allocation at the same settings (specification 16), the low end is **$405.8bn instead of $389.1bn**; the
   high end is personal already.
2. **Taxes on the business capital that serves the group's jobs** count at zero, and that lowers both ends. The zero
   comes from the production module's unmeasured rule that this capital "pays the same taxes elsewhere". That rule
   contradicts the case's own long-run premise, which the same lane applies to housing: under full adjustment a tax
   on reproducible capital falls on its users. Counting these taxes would lower the main case by **$12.5–86.8bn**
   on the September 28 lane's keys; the central is not measured.

The first is read off the case's own run; the second needs a rerun of the production module. Both recommendations
are below. One recorded bound belongs beside the headline and is not there, seven statements in the docs and records
were stronger than their basis and are corrected, and the rest are answered by the record or are below the bar.

## What ran

- **Bar** (as on 2026-10-08): a finding counts if it plausibly moves the headline by $10bn or more, flips a stated
  qualitative claim, or invalidates a method.
- **Three packets** (critique skill, `model-review.py`, preset cross4 from triage, each with a repo-reading premise
  scout). Each carried the v6 decision, the CLAUDE.md headline block and the 10-08 red-team record, with the
  instruction not to re-raise its rejections without new evidence.
  - A, the counterfactual and which budgets respond (80 KB): decisions 2026-09-23, 09-26 (both), 09-27; FAQ 2, 11,
    13 and 20; the complete annual account's response sections.
  - B, receipts, incidence, accrual and the production term (64 KB): decision 2026-09-29 (v4); FAQ 3, 4, 14, 16,
    17, 21 and "Before combining"; the NRC 1997 low-skill memo.
  - C, who is counted, against whom, and what is left out (64 KB): decisions 2026-10-05 (v5) and 2026-09-24; FAQ 1,
    5–10, 12, 15, 18 and 19.
- **Axes:** Gemini 4 Argon on structure and gaps (paid API), GPT-6 Astra on correctness and contracts
  (subscription), Opus 5.5 at max effort (subscription).
- **Tokens:**
  - Argon: prompt 21.3–26.1k, output 4.0–5.6k and reasoning 11.8–19.6k per axis; six calls, about $1.5 at the
    introductory $2 / $10 per million.
  - The subscription transports recorded no usage for the Astra or Opus axes.
  - Scouts (GPT-6 Astra, low effort): 569k, 619k and 675k input, mostly cached; 3.2–3.6k output.
- **Transport:** packet B's Opus axis reached Claude Code's 128k output cap after 41 minutes. The CLI injected its
  "Output token limit hit. Resume directly" turn, and llmx's guard against injected turns refused the whole reply, so
  it returned nothing. llmx 00cba8e now joins a reply resumed after the cap and still refuses every other injected
  turn. The axis was rerun alone and finished in 20 minutes (12.8 KB).
- **Findings:** extraction gave 63 findings for A and 57 for C (five axes each, after deduplication) and 18 for B's
  Opus axis. B's other four axes and the three scouts were dispositioned by hand. All are merged below by assumption.
- **The skill's anchor check** marked five extracted claims as hallucinated. Each cited a real file by a bare or
  partial name it did not resolve (`builder.py`, `RESULT.md`), a review artifact (`premise-scout.md`) or a misnamed
  file (`model.js`; the engine is `engine.js` with `model.json`). One of them is item 1. Every disposition here rests
  on reading the cited sources, not on that check.
- **Artifacts:** ignored and kept locally under `.model-review/2026-10-14-assumptions-v6-*` (coverage.json,
  findings.json, every axis output); the packets are `.model-review/assumptions-2026-10-14-*.md`.

## For the operator

### 1. The shared allocation credits the lineage with non-members' taxes (C: Opus; new)

- **Where.** Specification 48 splits each SPM unit's keyed amounts equally among its members
  (`full_account_spending_2026_09_20/builder.py:239–243`; `within_group_distribution_2026_09_29/RESULT.md`, "Mixed
  households and the shared allocation"). Taxes and person-level benefits (Social Security, SSI, cash assistance,
  refundable credits) are split this way; unit benefits such as SNAP and housing are split equally under both
  allocations.
- **Mechanism.** Sharing inside a unit of members only cannot change the group's total. The allocation moves the
  total only through units that also hold non-members, so the whole difference is a transfer across the lineage's
  boundary. 8.684M members share SPM units with 6.970M non-members (`immigration-adversarial-audit-2026-09-28.md` §2,
  on the canonical CPS frame); non-members' taxes are 6%, 11% and 22% of the first, second and third-plus
  generations' shared OASDI key (`within_group_distribution_2026_09_29/RESULT.md`).
- **Size.** At the 16 pairs of cells that differ only in allocation, shared minus personal is −$17.93 to −18.23bn
  on the hotdeck method and −$15.48 to −15.78bn on the pooled method. Specification 16, which is specification 48
  with the personal allocation, gives $405.786bn against $389.083bn: **+$16.70bn at the low end**. The high end,
  specification 11, is personal already. [CALCULATION: `main_case_2026_10_07/derived/per_spec.csv`; the cash set is
  not computed here]
- **What the record said.** The 09-28 audit priced only the benefit side of mixed units ("no estimated fiscal
  correction") and kept assigning observed incidence as "a legitimate exercise". Nobody priced the tax side or
  noticed that the shared total is not the change for others.
- **Limits.** The personal allocation is not a removal recomputation either. A joint return's tax sits on the
  records the survey assigns it to, and a non-member parent's child credits for member children would be lost in a
  removal, which raises the cost a little (below the bar on the reviewer's estimate).
- **Recommendation.** Take the group total at members-only sharing, which equals the personal total on person-level
  keys, so the low end becomes the personal allocation's, about $405.8bn. Keep the shared allocation for
  distribution inside the group and for comparisons between groups, where both sides share alike. The same rule
  sits in the comparator lanes and the generation ledger, whose gaps are per-person comparisons, so they are a
  separate decision. A lane would confirm the figure on the case's own run (members-only sharing as a third
  allocation, gated to equal personal on person-level keys) and price the child-credit term.

### 2. Taxes on the business capital that serves the group's jobs count at zero (B: Opus; Argon on both B axes)

- **Where.** Corporate tax, business property and other production taxes are keyed by CBO's rules and respond at 0:
  `full_account_2026_09_20/welfare.py` lists them as capital categories and `engine.js` applies
  `indirect_receipt_response: 0` (`receipt_side_long_run_2026_09_28/RESULT.md`, item 1). The account's rule 1 hands
  them to the production module ("the production model handles induced capital taxes"), and at every specification
  the module's capital-tax term is exactly 0. Its retention is 1: the capital that follows the group's jobs "pays
  the same taxes elsewhere".
- **The rule is an assumption.** The module lets released capital earn "the initial rental rate elsewhere".
  Retention 1 "taxes the alternative capital return identically in the US". At any lower retention the owners'
  private welfare rises by the tax lost (`private_wtp` adds `capital_gain − capital_tax_gain`), so P + F stays
  $13.32bn (`matched_benefits_2026_09_19/model.py`, `fiscal_and_private`). Its docstring says: "Neither retention
  nor ownership is measured."
- **Why it does not hold under the case's own premise.**
  - Full adjustment means the capital that works with the group is not in the US without it. Its source taxes
    (corporate tax on US profits, business property and production taxes) are then not collected. Only US
    residents' personal taxes on their capital income would follow it abroad.
  - The owners gain the lost tax only if the capital would earn the same pre-tax return abroad, untaxed, and then it
    would not have been invested in the US. If returns are equal after tax, as mobile capital requires, the owners
    neither gain nor lose, and the lost revenue falls on other residents. The same holds if the capital is never
    accumulated: at the margin its after-tax return just pays for the saving.
  - The same lane rejects that view for housing. It calls the reading in which "the capital the group's homes would
    use pays the average rate elsewhere" "inconsistent with the case's own capital assumption", because full
    adjustment is "the premise under which a tax on reproducible capital falls on its users". Items 2 and 3 apply
    that rule to homes, adopted in v4; item 4 applies the opposite rule to business structures and equipment.
  - The case charges the mirror image: the return on the public capital that scales with the group, $36.6bn at the
    low end and $61.1bn at the high (`main_case_2026_10_07/derived/per_spec.csv`). The NRC memo names that charge as
    the mirror of Clemens's capital-tax adjustment (§5), the only published correction that turns a dropout's
    balance positive.
- **Size.** Not measured. The bounds are on the September 28 lane's keys; the v6 lineage's 3.04M added people would
  raise them by their share of the wage bill [INFERENCE].
  - Floor: the corporate tax that the case's own CBO keys put on the group's wages, $13.4bn at the low end and
    $12.5bn at the high (`corporate_labor`, 25% of $663.69bn; `derived/trace.csv`).
  - Ceiling: commercial and industrial property ($273.45bn), other production taxes ($145.26bn) and corporate tax
    ($663.69bn) at the group's wage share, 8.02% and 7.48%, lost in full: $86.8bn and $81.0bn
    (`derived/probe.json`).
  - In between: land under business property stays, as item 2's rule says; part of the corporate base is
    foreign-source income or rent that does not move with the group's labour; the group's employers may use less
    capital per wage dollar than average. Opus's own factors give about $45–55bn [INFERENCE; not measured].
  - Every reading clears the bar. Both ends move by about the same amount, and the cash set moves with them.
- **What the record said.** The 09-28 lane classed these lines "not a candidate" because each reading "drops a rule
  the account states", so they never reached the operator. The 09-28 decision put only the foreign-owned part to
  him and kept it beside as "retention unmeasured" ($0–21.3bn, $10.3bn at retention 0.5); the benefits inventory
  holds that "only foreign or excluded owners can make it a net gain" (`benefits_inventory_2026_09_28/RESULT.md`,
  item 4). The 10-08 red team
  answered general-equilibrium tax feedback with "the production term is the account's GE term", but that term is
  where the zero sits. This record's first version (0930ee22) kept the foreign-owned arm as its item 3 and rejected
  Argon's $32–87bn because domestic owners "cancel by construction". The construction is the unmeasured assumption,
  and Argon's range was close.
- **Limits.** If much of the corporate base is rent, such as profits on intangibles booked in the US, it does not
  scale with the group's labour, and the figure moves toward the floor. Partial capital adjustment would shrink the
  credit, but it would also shrink the public-capital charge and the housing items; that case is not priced.
- **Recommendation.** Price it on the case's run and adopt it. Rerun the module with τk split: source taxes at
  retention 0 with the owners' after-tax return unchanged, residence taxes at retention 1, residential property out
  of τk (it overlaps items 2 and 3), business land at item 2's rule, and the capital keyed by the group's industries
  (BEA fixed assets by industry against the group's wage bill by industry and legal form). It is the case's own
  housing rule applied to business capital, and the receipt side of the public-capital return the case already
  charges. Until it runs, state $12.5–86.8bn beside the headline. The foreign-owned arm becomes part of this item:
  with equal after-tax returns, ownership no longer matters.

### 3. The Hispanic undercount bound is not beside v6 (C: Opus)

- CPS weights are controlled to Census estimates. The 2020 PES Hispanic net undercount, 4.99% (×1.053), is recorded
  as "a partly absorbed upper bound" (`immigration-mexican-origin-population-total-2026-09-19.md` §3) and was never
  priced on any main case. Row 4 corrects the Mexico-born only.
- On the roughly 31.6M US-born members the reviewer's estimate is **+$16–19bn** at the bound [INFERENCE: 5.3% × the
  US-born count × $9.7–11.7k a person; not an engine run]. How much the Vintage 2024 controls already absorb is not
  measured.
- **Recommendation.** Price ×1.053 on the US-born on the case's run and state it beside the headline as an upper
  bound, as the count's arms are. Comparing the controls with the 2020 Demographic Analysis's Hispanic estimates for
  ages 0–29 would measure the absorbed share.

### 4. The 3% rate at the high end (A: Opus)

- The high end's capital return uses OMB A-4 (2003)'s 3%, reinstated by M-25-15; Treasury's 2024 real yields were
  1.94–2.15%. At 2.15% the high end would be about $444.2bn (−$17.3bn); the charge is linear in the rate.
- The operator set 2% / 3% on 2026-09-27 (15:21) knowing both, and the record states each source accurately. This
  is his call, already made. **Recommendation: keep it.** Both ends are federal guidance in force for the income
  year or now.

## Acted on

| Finding | Axes | Check | Change |
|---|---|---|---|
| FAQ 1 and 10 quote the generation ledger's age exercises next to an accrual headline | C: both Argon axes | The ledger counts Social Security and Medicare when paid; the main case charges the Social Security and Part A that members earn as they work. Confirmed: the basis was unstated, and part of FAQ 10's $70bn of Social Security is already in the headline | "Before combining" states the ledger's basis; FAQ 10 scopes its sign claim to it and says the re-weighting has not been run on the main case's basis; FAQ 1 notes the main case narrows the age advantage [INFERENCE] |
| FAQ 15's per-person gap barely moves while the total widens 45% | C: both Argon axes ("mathematically impossible") | Not an error: the per-person figures weight places and ages by whites' own mix, the totals by where the group lives (`metro_match_2026_09_17/RESULT.md` §1) | The sentence names both weightings |
| The cash set is "counting benefits when paid", but retiree health is on accrual in both sets | B: Astra correctness; A: Argon, Astra contracts on the capital return | Confirmed as a definition gap, not a numbers error: v6 item 2 is in both sets (+$0.58 / 0.77bn with its interaction), as BEA books public employees' compensation, and the capital return is in both | The INDEX says only the members' Social Security and Part A change |
| v6 rejects alternative 4 because adults report less loss than their cohort's children | C: both Astra axes, Opus, Argon | The age-mix lane reads the pattern as a changing label or selective departure; under selection, alternative 4 is favoured. Confirmed | Dated correction in the v6 decision; the central is unchanged |
| FAQ 4 says the account adds production gains "and the induced taxes on them" | B: Opus | Confirmed: the induced taxes are the labour-tax gain alone; the capital-tax term is 0 at every specification (item 2) | FAQ 4 says taxes on the business capital that works with the group count at zero and points to item 2 |
| The "CBO-informed" label reads as covering corporate tax | B: Opus | Confirmed: the CBO keys are computed for corporate, business-property and production taxes, and those lines respond at 0 | The INDEX and CLAUDE.md say those lines take CBO's keys and respond at zero |
| The schools decision lists new seats at today's construction cost as unpriced | A: Opus | Since 09-27 the case charges current-cost depreciation plus a return on the current-cost stock | Dated correction in the schools decision |

## Open: new, unmeasured, below the bar on current evidence

- **Fees on lines priced below 1** (A: Argon gaps, Astra correctness). Lines are consumption net of fees, so a
  response below 1 also shrinks the fees, while a departing payer's fees go in full. That overstates the group's
  cost. Argon's sign is backwards: the correction makes the frozen-budget row more favourable to the group, not less.
  The main case's large fee lines (tuition, hospitals) respond at 1, so the headline effect is small. The first-year
  and frozen-budget readings are exposed and not measured.
- **Nominal wages in the cross-district school slope** (A: Argon). The 1.004 absorbs state differences but not wage
  gaps between metros within a state, and lower public pay in a smaller metro moves money among other residents
  rather than saving resources. The real-quantity slope is likely a little lower; a few $bn [INFERENCE]. A
  wage-deflated slope (NCES CWIFT) would settle it. The within-district 0.836 is the stated low side.
- **One evidence rule for responses** (A: Opus). Roads and parks take within-state slopes at the high end, while the
  within-state administration reading (0.47) is used at neither end. Cross-state slopes at both ends lower the high
  end by $5.22bn on the 09-27 base (`service_response_long_run_2026_09_27`); the within-state administration
  reading at the low end would lower it by about $14bn on the reviewer's estimate, but it rests on a reading whose
  interval runs from −0.72 to 1.66. The record's reason (every highway and park window above 1) stands; a stated
  rule in FAQ 2 would make it visible.
- **The cap at 1** (A: Opus). Police, fire and hospitals scale above 1 across states and are held at 1; uncapped
  within-state readings would add $10.35bn at the high end (lane, 09-27 base). Stated in the lane; upward.
- **Counts and ages from different loss rates** (C: Astra ×2, Opus, Argon). The age-mix lane keeps arm b's counts
  while moving ages: the G3-rate part's count would be ×1.029 (+$0.3–0.4bn), and Opus estimates ×0.82 for the later
  part (−$1.6 / 2.3bn). A joint count-and-age table would settle it.
- **Emigration in the pension accrual** (B, C: Argon; B: Opus). The lane ignores emigration before retirement
  ("flagged, not priced"); Part A pays nothing abroad. The Mexico-born carry $9.7 / 14.0bn of the accrual (FAQ 5), so
  a plausible effect is −$1–3bn [INFERENCE]; Argon's −$10–20bn exceeds the base. Opus would pair it with the
  Hispanic mortality arm (+$19.6bn on the lane's 09-28 base), since return migration also hides deaths from US
  records (the lane's own caveat), and keep the central.
- **The accrual's national check runs high** (B: Opus): the OASDI ratio by 4.6% and the HI ratio by 1.7% against
  SSA's, within the lane's tolerance; under $5bn on the reviewer's estimate.
- **Trust-fund paths with and without the group** (B: both Astra axes). Fixed Trustees paths price the group's
  accrual; removing contributors and beneficiaries could change depletion and other residents' payable benefits.
  Direction and size unestablished.
- **Capital stock against spending responses** (A: Argon gaps, Astra correctness). The capital return inherits each
  line's spending response. Untested; either direction.
- **Smaller items** (C: Opus): equal fertility in the identity-loss propagation (−$1–3bn); child credits and filing
  status in mixed units (up, low single digits); the production function applies no phaseouts and no public-pay
  change (B: Astra contracts; the 09-28 audit's public-pay scenario).

## Rejected

Each group ends with the record that answers it and the reason this review gave no grounds to reopen it.

1. **FAQ 2's figures are stale** (A: Opus, Argon). The general-public-services $30.5–43.2bn is v6's operating
   effect: the "general government at 0" row, $32.70 / 47.89bn, less that line's capital return, $2.19 / 4.65bn.
   The "+$24.4 / +$42.9bn" capital return is the non-enterprise part (core plus block, 24.44 / 42.86); enterprises'
   capital is in the next item.
2. **Withdrawn: capital-tax cancellation hides $32–87bn** (B: Argon ×2). The first version rejected this because
   domestic owners cancel by construction. B's Opus axis and the module's code show the cancellation is the
   unmeasured assumption; it is item 2 above.
3. **Accrual against cash, closed funds and education** (B: Argon; B: Opus on why accrual stops at legal promises).
   The frame and the cash set beside it are the operator's (10-08 rejection 2). Post-depletion benefits are paid from
   future payroll taxes, the lineage's children's included, but in an annual stationary account their taxes are
   counted in their own years. Crediting today's schooling with its pupils' future taxes is the life-course reading,
   which FAQ 1 gives at today's rates (−$8,154 a person).
4. **Household services and a task nest** (B: Argon). FAQ 4 states that the $11.9–21.8bn is unreconciled with the
   production term and neither added nor counted; 10-08 rejection 9.
5. **The consolidated property-tax reading** (B: Argon; B: Opus, $8.7bn). Decision v4, item 5,
   [FRAMING-SENSITIVE], states it (−$35.91bn against −$27.19bn). It books the budget's loss on land and drops other
   holders' lower tax bills.
6. **The care item is private consumer surplus** (C: Argon). Its $4.15bn is taxes on natives' extra hours ($2.69bn),
   the Medicaid saving on elder care ($1.49bn) and a second-order output term (FAQ 4).
7. **Public procurement prices, $12–25bn** (C: Argon). The public-pay question is the 09-28 audit's §1; Opus puts it
   at a few $bn of unclear sign.
8. **Consumption and property taxes at national rates** (B: Argon). v4's state prices cover receipts too
   (`state_priced_services_2026_09_29`, adopted at +$2.18 / 2.27bn net): general sales tax at the group's state
   index, 1.1151 (California 0.93× the US, Texas 1.30×), +$5.65bn; owner-occupied property at each state's effective
   rate; income taxes are each state's own. Selective excises showed no difference beyond noise.
9. **Unauthorized filers' credits** (B: Argon). The audit's SSN rule and Treasury's EITC shares (decision 09-24,
   item 6) handle the EITC; the child-credit bar binds only for children without an SSN.
10. **Enterprises at response 1 on the population key** (A: both Argon axes). Option D is the operator's 09-27
    choice; option A is beside at $372.3–438.7bn. The scale elasticity of utilities is unmeasured.
11. **Road network geometry and freight** (A: Argon). The lane's land-area control gives 0.690 against 0.727; the
    high end is item "one evidence rule" above.
12. **Defense at 0 and capped programs at 1** (A: Argon). FAQ 2 states the defense sensitivity; rental assistance at
    1 counts the displaced beneficiaries, who are other residents (decision 09-27).
13. **Whole people and replacement fertility** (C: both Argon axes). 10-08 rejection 3; the ancestry-share count
    is beside.
14. **v6's own [ASSUMPTION]s** (A, C: Argon): arm b's ages in arms a and c, item 4 on the union, Pell through the
    education line. Stated in the decision and below the bar (10-08 B28).
15. **Stale finite-removal share and an unexecuted public-housing fix** (A: Argon). v6's responses are recomputed
    (0.6005 / 0.8511 against 09-26's 0.6000 / 0.8504), and v4 items 1 and 4 key public housing's deficit and capital
    by tenants.
16. **Already disclosed:** land (A: all; the thresholds are lower bounds, Opus), other sales by payer (A: all; v6
    Revisit-if, ±$1.75bn a point), the top tail of item T in state figures (C: Argon; FAQ 15), an all-resident
    accrual benchmark (C: Argon; FAQ 6 and 18), the presentation layers (C: Argon; 10-08 Revisions).

## Revisions

- 2026-10-14: written after the review. Concept affected: the low end's allocation rule (open, for the operator);
  the cash set's definition; the ledger's benefit basis in FAQ 1 and 10; FAQ 15's weights; the v6 age-mix
  rationale; the schools decision's unpriced upside.
- 2026-10-14, after packet B's Opus axis: its capital-tax finding clears the bar and is item 2. The first version's
  item 3 (the foreign-owned arm alone) and rejection 2 (cancellation by construction) are withdrawn: the module's
  code shows the cancellation is an unmeasured assumption about the alternative return, and the same lane rejects
  that assumption for housing. FAQ 4's induced-tax sentence and the "CBO-informed" label are scoped. Concept
  affected: capital taxes under full adjustment (open, for the operator).
