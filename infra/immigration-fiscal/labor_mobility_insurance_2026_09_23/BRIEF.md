# Brief: labour-market mobility and adjustment — gains a static account omits

A stationary one-year account cannot show gains from how the group moves across local labour
markets. Mexican-born workers move toward booming places and away from busts more than natives do,
which can cushion natives' employment losses in downturns ("immigrants equilibrate local labor
markets", Cadena & Kovak 2016 AEJ Applied; Borjas 2001 BPEA, "Does immigration grease the wheels
of the labor market?").

## Task

1. Read both with intervals and populations, and search for later tests on both sides (for
   example the COVID shock, and studies finding weaker or no insurance effect). Grade them alike.
2. Price the insurance value to other residents: the reduction in natives' employment and earnings
   losses across local shocks, annualised over a cycle, using the papers' estimates and our own
   data where possible (ACS or CPS by metro, the Great Recession and 2020). Price Borjas's
   efficiency gain as he defines it, updated to 2024.
3. Check whether the group's present-day mobility still exceeds natives' (ACS migration-in-past-
   year by nativity, Mexico-born vs US-born Mexican-origin vs other natives, 2019–2024).
4. Overlap: the static account and its production term contain none of this; say what adds and
   whether any part is a fiscal effect (unemployment insurance and transfers avoided).
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
