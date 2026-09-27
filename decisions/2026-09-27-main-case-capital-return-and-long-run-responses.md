---
date: 2026-09-27
concepts: [headline, service-response, public-capital, cost-allocation, government-enterprises]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-09-26-main-case-schools-full-cost.md
  - revises: decisions/2026-09-20-category-service-response.md
  - revises: decisions/2026-09-24-main-case-audit-and-outside-checks.md
evidence: infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md
---

# 2026-09-27: The main case charges the return on public capital, and roads, parks, rental aid and government enterprises respond

## Context

Four items in the main case were zero because of how the source classifies them, not because of any
measurement:

- **The return on public capital.** BEA's government consumption charges depreciation on public capital
  but no return on the money tied up in it. The school lane (ladder 231) compared this with a cash basis.
  Without a return, the account charges $15.1–18.2bn for the group's school capital. The cash basis
  (outlay plus interest) is $22.7–28.2bn. A 2–3% return closes the gap. Pricing schools alone would have
  been inconsistent, since every responsive line uses capital.
- **Roads and parks.** Economic affairs ($451.9bn) and recreation ($54.3bn) were held at zero under CBO's
  short-run category lag (decision 2026-09-20). The repo's own scaling test finds highway spending rising
  0.727% and park spending 0.948% per 1% more residents across states. The congestion item beside the
  account ($19.2bn) was priced only because roads were held fixed.
- **Rental assistance.** `housing_subsidies` ($60.3bn) was held at zero only because NIPA files it as a
  subsidy (dataset audit, `dataset_integrity_2026_09_23/spending.md` item 6). The account's other capped
  means-tested transfers, TANF-type aid and energy assistance, respond at 1.
- **Government enterprises.** Transit, public housing, water, sewers, power, airports, ports and tolls run
  an operating loss of $47.46bn net of depreciation (NIPA 3.8). The account held this receipt at zero and
  charged no return on the enterprises' $4,960.4bn of capital.

The operator asked: "why wouldn't you add capital returns to main case? it's the honest value of the
thing ... why would you ignore it?" (13:26 JST), and then "we can maybe add that in if you think the
financial intuition checks out and most reasonable world models would include it" (14:40). The parent
judged that it does, for the capital return and for roads and parks. The operator set the open terms
by AskUserQuestion at 15:21:
- 2% at the low end and 3% at the high end, with 7% reported beside the account;
- rental assistance at 1;
- land left as a reported gap.

At 16:58 he chose option D for government enterprises: all respond.

## Alternatives considered

1. **Depreciation only, as NIPA records it.** This understates what the capital costs. Money tied up in a
   school or a road has a cost even when no cash changes hands, and the school comparison shows the gap.
   Kept as the reference: the schools case.
2. **The rate.**
   - The charge is what the money costs, not what the asset yields to its users. The users' benefit is
     not a budget item.
   - **2% (chosen, low end):** OMB A-4 (2023); Treasury's 2024 real yields were 1.94% (10-year) to
     2.15% (30-year).
   - **3% (chosen, high end):** OMB A-4 (2003), "the real rate of return on long-term government debt",
     reinstated by M-25-15.
   - **7%:** A-4 (2003)'s "average before-tax rate of return to private capital". It prices the capital
     displaced from private use, a social cost rather than a budget cost. Reported beside the account.
3. **Netting the return of user charges.** Rejected. The account's lines are consumption, that is gross
   output less sales, so every charge is already credited once. Netting would credit it a second time.
4. **Enterprises out (option A).** Charge no return on enterprise capital and keep their operating loss at
   zero. Kept as a variant beside the range.
5. **Enterprises in (option D).** Chosen by the operator.
   - Their operating loss moves with the group, like every other public budget.
   - They also carry the full return on their capital.
   - Fee-financed utilities do not earn a 2% return: their 2024 surplus covers it 0.29 times for water and
     sewerage and 0.91 times for gas and electricity. Only lotteries and liquor stores come out ahead.
6. **Roads and parks at the within-state slope.** Within states the slopes exceed 1 (1.46 highways, 1.41
   parks). Capped at 1, they set the high end, and the across-state readings set the low end.

## Decision

The main case is **$321.8–387.4bn** a year ($321.82–387.37bn; `main_case_long_run_2026_09_27`, case key
`sept27`), up from $258.5–292.0bn (+$63.3bn / +$95.4bn). The end specifications stay 48 (low) and 11 (high) in
both fill-in methods, so the moves add exactly:

| $bn a year, low / high | Change |
|---|---:|
| Schools case | 258.49 / 291.95 |
| Long-run road, park and economic-administration responses | +19.44 / +29.63 |
| Rental assistance at 1 | +4.53 / +4.53 |
| Return on the capital of the responsive lines (schools, colleges, offices, public safety, health) | +15.99 / +25.78 |
| Return on road and park capital | +6.18 / +12.47 |
| Government enterprises' operating loss at 1 | +5.56 / +5.56 |
| Return on government-enterprise capital (public housing $0.99 / $1.48bn of it) | +11.62 / +17.44 |
| **Main case** | **321.82 / 387.37** |

- **Capital return.** It totals $33.80bn / $55.69bn at the ends: state and local $32.97 / $53.95bn, federal
  $0.83 / $1.74bn.
- **Low side.** With schools at the within-district 0.836 read over the removal, as in the schools decision, the
  case is $295.9–363.0bn ($293.7–361.0bn with 0.836 taken as the response).
- **First-year budget response.** It stays the September 26 case, $200.9–245.7bn. A first year has CBO's
  short-run lags and no capital response.
- **Outer range.** $258.6–436.1bn with every component moved at once; $290.9–408.2bn in quadrature. It adds
  three components to the schools case's $198–324bn: the long-run responses, the rate (both ends at 2% or both at
  3%) and 12 capital definitions.

- **Specifications.** Each specification ties the rate and the long-run reading to general government's
  reading: 2% with the low readings, 3% with the high. The tied band equals the band from crossing them.
- **Keys and responses.** Each component of the return takes its key share and response from the engine's
  evaluation. A re-keyed evaluation, by generation for example, therefore splits the return consistently.
  - The enterprise pieces take the enterprise receipt's key.
  - That receipt is re-keyed from model.json's 0.1202 to the case's corrected population share, 0.1172, as
    the corrections already do for the population-keyed spending lines. The re-key lowers the case by
    $0.45bn / $0.60bn.
- **Congestion** beside the account falls from $19.16bn to $13.99bn (low end) and $12.02bn (high end),
  since lanes now grow with highway spending.
- **The sign break-even falls from 5.8–17.0% to 2.8–13.6%.** The test sets every public production response
  to a common share s; the account turns positive only below it.
  - The capital return moves with its line's s.
  - The enterprises move with s too: under option D they are public production, and their response is the
    same kind of assumption.
  - Rental assistance stays at 1 as a transfer, and general government at its adopted response.
  - Holding the enterprises at 1 while services fall to 0 gives −2.9% to 9.7%, a labelled variant. At its most
    adverse end no service response turns the account positive.
- **Rental assistance nets correctly against the enterprise receipt.**
  - Federal subsidies to public housing authorities are spending on the rental line: NIPA Handbook ch. 2,
    p. 2-13.
  - They are also revenue in the enterprises' surplus, which BEA defines as "current operating revenue and
    subsidies received ... less the current expenses".
  - With both responding, the two offset apart from their keys (0.0752 against 0.1172). That leaves a credit to
    the group of about $0.2bn for public housing's operating subsidies, and at most $2.53bn. [INFERENCE]
  - **This is a confirmed defect, and its fix is deferred.** The conceptual audit (§7) confirms it as a
    conservation failure: a synthetic $1bn on both legs lowers the group's cost by $0.041–0.043bn.
    - The fix: consolidate the transfer before keying, so one attributed amount sits on both legs.
    - It waits for the next case revision, together with the joint road scenario. At the likely size it moves the
      case by about +$0.2bn, under the headline's rounding; a second propagation for that would cost more than it
      corrects.
    - If the internal transfer turns out to be large (the bound is +$2.5bn), the fix comes first.
- **Beside the account, not in the range:**
  - capital at 7%: $406.3–461.6bn;
  - option A (enterprises out): $304.6–364.4bn;
  - rental assistance at 0: $317.3–382.8bn;
  - land [GAP]: $3.33bn / $5.49bn per 10% of land-to-structure value.
- **Scope.** The research record and the consumer lanes move to this case (`sept27_propagation_2026_09_27`).
  The explorer, the figures page and the prototypes stay on earlier cases until the operator asks.
- **What kind of cost each addition is.** The conceptual audit of the same day (§1) asked for this distinction.
  - The capital return is an imputed resource cost: the opportunity cost of capital at a chosen rate, not a
    payment. It belongs in annual resource-cost totals and never in a borrowing or debt flow.
  - Rental assistance is capped. Without the group, other eligible households would take the slots, so the $4.5bn
    is a loss to them and needs no budget change. It is still a cost to other residents, so it counts at 1 in
    the account, but nothing from it accumulates into debt.
  - The consumer lanes keep cash financing, resource cost and displaced beneficiaries in separate columns.
- **Superseded entries.** Ladder 231 (school capital alone) is subsumed; ladder 237–239 record this case. The
  schools case stays reproducible as `sept26_schools`.

## Evidence

- `infra/immigration-fiscal/capital_return_services_2026_09_27/RESULT.md` (250ccb5):
  - BEA FAAt701 net stocks, 2024 average;
  - 24 components (8 core, 5 road and park, 11 enterprise), 54 gates;
  - BEA MP-5 (2005), p. I-13: "In calculating the current surplus, expenses include consumption of fixed
    capital (CFC), but neither revenue nor expenses include interest." Enterprise interest therefore sits in
    the account's interest row, which stays at zero, and no interest is counted twice;
  - NIPA Handbook ch. 2 on federal subsidies to public housing authorities.
- `infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md`: the cash-basis comparison, the rate
  texts (A-4 2003 and 2023, M-25-15) and Treasury's 2024 real yields.
- `infra/immigration-fiscal/service_response_long_run_2026_09_27/RESULT.md` (bccf478): responses by
  subfunction, read over the removal as r = [1 − (1 − s)^b]/s; congestion re-derived.
- `research/immigration-service-scaling-test-2026-09-20.md`: highways 0.727 and parks 0.948 across states.
- `infra/immigration-fiscal/dataset_integrity_2026_09_23/spending.md` item 6: rental assistance held fixed
  as a business subsidy.
- `research/immigration-conceptual-audit-2026-09-27.md` §1 and §6: resource cost against borrowing, and the
  shared road response.
- `infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md` (f3031ab, 7e94324). Its gates:
  - the old settings reproduce the schools case;
  - each addition alone reproduces its lane;
  - applying the payload independently gives the same cost at every specification;
  - two runs are byte-identical.

## Revisit if

- **The rate.** The operator prefers the social-cost reading, 7%, at the high end.
- **Land.** BEA or Z.1 data make the value of public land measurable.
- **Roads.** A design with fixed boundaries finds road spending not keeping pace with population over ten
  years or more; the long-run response then falls toward the across-state 0.727.
- **A joint road scenario.** Road operations, road capital and congestion share one response, but the range
  varies them separately (audit §6). A joint scenario could move the case's high end.
  - It would compute operations, depreciation, return, capacity and congestion together under three cases: a
    fixed stock, replacement adjustment and a smaller stationary network.
  - The highway response also mixes a population removal share with a resources key. The population law gives
    $17.9bn instead of $12.0bn at the low end. The audit calls that an alternative model, not a correction.
- **The question changes.** The account moves from a yearly snapshot to a removal path. The first-year
  budget response then governs the first years, and capital responds with a lag.

## Supersedes

None. It refines the schools decision of 2026-09-26, whose case stays as the reference. It revises the
2026-09-20 category-response decision for economic affairs and recreation, and the 2026-09-24 audit
decision's treatment of rental assistance as a fixed subsidy.
