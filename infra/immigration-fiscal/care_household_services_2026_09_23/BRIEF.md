# Brief: household services, care and native labour supply — what is outside the account

`research/immigration-consumer-price-and-native-hours-2026-09-18.md` priced the two largest
pro-side channels: cheaper immigrant-intensive services ($23.76bn consumer surplus, Cortes 2008
elasticities) and more hours by top-quartile native college women (private earnings $11.5–24.9bn;
a small tax line). The FAQ treats both as overlapping the factor-income gains and adds neither.
Elder care: immigrant care labour lowers nursing-home use among the US-born elderly, but transfers
weakly to Mexican-origin immigrants (ladder 164; FAQ 13: $2.3–14.6bn upper bound).

## Task

1. **Rule on overlap, line by line.** In the account's one-good CES model, is the consumer surplus
   on cheaper services inside P? Are native women's extra hours (labour-supply elasticity 0 in the
   central) outside it? For the extra hours, separate the private welfare gain (near zero at the
   margin by the envelope argument, unless the paper shows otherwise), the induced taxes (a fiscal
   gain to other residents the account omits) and any output gain to others. State what adds.
2. **Price the additive parts** with the source intervals: induced taxes on native hours (use the
   account's tax rates), any welfare triangle, and the elder-care Medicaid saving for the
   Mexican-origin group specifically (tighten the FAQ 13 bound; read ladder 164's sources).
3. **Child care and household production** (Furtado 2016 and related): price only if the
   evidence reaches the Mexican-origin group.

Re-run or reuse the 2026-09-18 lane's computation rather than re-deriving it; find its lane
directory from the memo. If the memo's numbers need correcting, say so with evidence.
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
