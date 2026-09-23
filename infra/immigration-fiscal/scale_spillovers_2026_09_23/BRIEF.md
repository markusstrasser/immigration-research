# Brief: scale and human-capital spillovers and innovation — the counterpart of congestion

The congestion lane priced the cost of bigger cities: speed falls 0.12% per 1% more population at
fixed lanes (Couture–Duranton–Turner), $19.2bn a year to other residents
(`congestion_2026_09_23/RESULT.md`). Symmetry requires pricing what bigger and denser cities do
for productivity, with the same geography and the same standard. The account's production model
has constant returns, so none of this is inside it.

## Channels

1. **Agglomeration (scale).** Wages and productivity rise with city size or density. Use the
   literature's elasticities with their intervals and populations (Combes & Gobillon 2015
   Handbook chapter; Ahlfeldt & Pietrostefani 2019 meta-analysis; Ciccone–Hall; Glaeser–Maré), net
   of sorting where the paper does so. Apply metro by metro: other residents' earnings × elasticity
   × ln(1/(1 − s_m)), with s_m the group's share of the metro (reuse the congestion lane's
   `derived/ua_exposure.csv` or the housing lane's CBSA shares). Say whether the elasticity is per
   person, per worker or per density unit, and match it.
2. **Human-capital composition.** Metro wages also rise with the college share (Moretti 2004 JoE
   and AER; Acemoglu–Angrist 2000 for the null on average schooling; later replications). Without
   the group, metro college shares are higher. Price that spillover with the same care: it is a
   cost of the group's presence if the estimates hold. Report scale and composition separately and
   netted.
3. **Innovation.** Burchardi, Chaney, Hassan, Tarquinio & Terry, "Immigration, Innovation, and
   Growth" (NBER w27075), the paper behind the repo's ancestry instrument: local patenting and
   wage growth from immigration, by immigrants' education where reported. Scale to the group's
   education mix.

## Prior repo work to read first

- `research/immigration-new-conclusions-audit-2026-09-17.md` §5 (an earlier agglomeration transfer
  that failed; the replication package's earnings per job +0.4 log points, SE 2.9).
- `ancestry_instrument_2026_09_22/RESULT.md`. A parallel lane (`ancestry_iv_congestion_wages_2026_09_23`)
  is estimating native wage effects with that instrument; its estimate would net substitution and
  spillovers together, so do not add the two. Note the relationship in the overlap ruling.
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
