# Brief: construction labour and housing supply — the supply side of the housing channel

The housing lane (`housing_transfer_2026_09_23/RESULT.md`) priced the demand side: in the long
run other renters pay about $34bn a year more rent ($22–58bn), 96.5% to landlords who are other
residents, a small net gain (+$0.7–3.5bn). Mexican-born workers are a large share of the
construction trades. If their labour lowers construction costs or raises the pace of building,
housing supply is larger and rents lower than a demand-only calculation implies. That is the
matching benefit channel.

## Task

1. Measure the group's share of construction employment by trade and metro (ACS 2024 PUMS; OCC
   and IND codes; Mexico-born and US-born Mexican-origin separately).
2. Read the causal evidence with intervals: labour-shortage and enforcement shocks to construction
   (Secure Communities and 287(g) studies of residential construction, starts, costs and prices;
   Howard, Wang & Zhang on labour shortages and housing affordability, if that is the right cite;
   search for others on both sides; grade them alike). Record the population and period of each.
3. Price the supply effect in the housing lane's own model: how much lower are construction costs
   and how much larger is the long-run stock with the group present, and what does that do to
   other residents' rents and home values? Report it as an offset to the renters' transfer and
   the owners' gain, not as a free-standing number.
4. Overlap: the account's production term treats construction output as part of the one good.
   Say whether the rent effect of a lower supply curve is already inside P, beside it, or a
   correction to the housing lane's demand-only arm.
## Frame and overlap (common to the benefit lanes)

Date: 2026-09-23. Operator: "if there's benefits and gains ... we need to research and calculate
them obv". Rule 5 of the evidence-symmetry rules (`notes/quant-bias-checklist.md`, decision
`decisions/2026-09-23-evidence-symmetry-rules.md`): benefits are priced to the same standard as
the costs already priced beside the account
([real costs](../../../research/immigration-real-fiscal-and-social-costs-2026-09-23.md)). Rules
1–4 also apply: quote every external estimate with its interval or SE and the population it was
measured on; grade studies on both sides alike; no weight for affiliation.

Frame: the complete annual account, a stationary 2024 comparison of the United States with and
without the 40,896,574 CPS Mexican-origin residents; effects on all other residents; 2024
dollars. The adopted main case is a net cost of $203.2–249.6bn
(`main_case_2026_09_23/RESULT.md`).

**What the account already contains.** Its production term (P plus induced receipts F,
$8.8–13.3bn) is a one-good CES economy with constant returns, capital adjusting, native labour
supply fixed in the central (elasticity 0; 0.33 in the grid) and perfect substitution in the
central (the nest's ε variants in `production_nativity_nest_2026_09_22`). A gain that is the same
surplus seen from another side (for example cheaper services, which is the expenditure side of
the immigration surplus) is inside P and is reported as a side view only. A gain a constant-returns,
fixed-labour-supply, static model cannot contain (scale spillovers, induced native hours and
their taxes, mobility across local shocks, supply responses) is a candidate addition. Every lane
must state, channel by channel, which it is, and must not double count with another lane: say
explicitly what the other benefit lanes and the cost lanes cover.

**Deliverables.** `RESULT.md` opening with `**Verdict:**`: central, range, per group member and per
other resident; an overlap ruling (adds to the fiscal account, sits beside it as a social benefit,
or is inside P); sources with intervals; every specification computed; limits. Scripts and
`derived/*.csv` aggregates only; raw pulls in `_cache/` (add a `.gitignore` with `_cache/`). Census
key in `infra/immigration-fiscal/acquire/config.local.env` (source it, never print it; pipe
URL-bearing output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`). Run with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root. Write only in the
lane directory. Do not commit.
