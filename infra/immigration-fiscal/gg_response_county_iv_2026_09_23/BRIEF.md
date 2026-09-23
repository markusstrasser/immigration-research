# Brief: does local general government grow with population? A county IV test of the adopted 0.59–0.84

## Why

The main case ($203.2–249.6bn, `decisions/2026-09-23-main-case-general-government-and-use-keys.md`)
lets general government respond to population at 0.59–0.84. The low end holds the federal
executive and legislature fixed. The state-local part rests on a **cross-state scale elasticity**:
state administration scales at 0.842 (SE 0.039), financial administration at 0.789
(`assumption_explorer_2026_09_21/scaling_check.py` → composite 0.59/0.84). The only within-place
evidence is uninformative: a state panel, 2012–2023, gives 0.47 (95% CI −0.72 to 1.66)
(`administration_response_2026_09_20/`). Moving the response from 0 to 0.59–0.84 alone adds
$28.5–40.6bn to the main case (`main_case_2026_09_23/RESULT.md` line 8), so this is the account's
largest adopted assumption. The decision record
says to revisit "if a causal estimate of administration spending's response to population
contradicts the cross-state scale range". This lane produces that estimate, or shows it cannot be
had.

## Estimand

The elasticity of real local general-administration spending with respect to population, for
population changes not caused by the place's own spending, income or amenities. Primary outcome:
the same functions as the administration lane, as current operations: financial administration
(E23), central staff (E29) and general public buildings (E31). Sensitivities add judicial and legal
(E25), and use total direct expenditure on those functions. Deflate with CPI-U (the cached
`local_spending_composition_2026_09_18/_cache/cpi.json`).

## Data (all local; reuse, read-only)

- County-area local government finances for 2007 (GFD), 2012, 2017 and 2022 (Census individual-unit
  files; full censuses of governments in 2012, 2017 and 2022). The builders and the county panel
  are in `local_spending_composition_2026_09_18/` (`_cache/indunit_<year>.zip`,
  `_cache/gfd_county_waves.csv`, README). Use only census years for county sums; annual-survey years
  are samples. The full GFD archive (1967 on) is at
  `sources/immigration-fiscal/data/external/government_finance_database/gfd_entire.zip` (2.9 GB CSV
  inside: stream it, never extract it into the repo) if you need 1992–2002 waves for a pre-trend.
- County Business Patterns 2012, 2017, 2022 (copied from the corpus today):
  `sources/immigration-fiscal/data/external/cbp_county/cbp{12,17,22}co.txt`. More years are on
  `/Volumes/2TBPNY/corpus/census_cbp_20NN/`; the operator has approved copying what you need into
  `sources/immigration-fiscal/data/external/cbp_county/`.
- County population: `sources/immigration-fiscal/data/external/census_county_pop/cc-est2023-alldata.csv`
  (2020–2023), plus Census population estimates or ACS 5-year via the Census API for 2007/2012/2017
  (the key is in the untracked `acquire/config.local.env`; never print it; pipe output through
  `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`).
- County foreign-born by country of birth: 2000 Census SF3 and ACS 5-year `B05006`, as fetched by
  `local_spending_composition_2026_09_18` (`_cache/acs/`). Extend via the API if needed.

## Design

1. **Long differences**, county level: 2012→2022 (main), 2007→2017, and stacked 2012→2017 /
   2017→2022 with period effects. Regress Δ ln real outcome on Δ ln population, with state fixed
   effects (state × period when stacked) and base-year log population. Report weighted
   (base-year population) and unweighted results, and give each spec's n.
2. **Instruments:**
   - (a) **Industry-mix employment shock** (Bartik): base-year CBP county employment shares by
     3-digit NAICS × national leave-one-out employment growth over the window. Report the
     Goldsmith-Pinkham–Sorkin–Swift Rotemberg weights and a drop-top-5-industries variant.
   - (b) **Immigrant settlement shift-share**: 2000 county shares of each origin's foreign-born ×
     that origin's national 2012→2022 change, leave-one-out, with and without Mexico. Ladder 136:
     Mexico's national stock is flat after 2005, so Mexican-inflow instruments are weak here.
     Report (b)'s first stage on population, not only on the foreign-born share.
   - (c) Both, with a Hansen J test.
   - Effective F (Montiel Olea–Pflueger) and Anderson–Rubin sets for every IV spec.
3. **Checks:**
   - A pre-trend placebo: each instrument's 2012→2022 value against the 2002/2007→2012 outcome change.
   - Leave-out of the 25 largest counties.
   - Excluding consolidated city-counties.
   - An OLS benchmark.
   - The cross-sectional scale elasticity in levels on the same counties, to compare with 0.842.
4. **Exclusion threats, stated not assumed away.** The Bartik shock raises incomes, which can raise
   spending directly. Immigrant inflows change composition. Report reduced forms. Also run a
   variant controlling for the Bartik-predicted change in income per head. Note it is a
   potentially bad control, and show both.
5. **Map to the main case.** Rebuild `scaling_check.py`'s composite, read-only import or copy with
   attribution, with the lane's local elasticity (and CI ends) in place of the state-local scale
   elasticity. Then evaluate the adopted main case's `general_government_response` at those values
   through the explorer engine as `main_case_2026_09_23/main_case.js` does. Report the band.
   Proposal only; the operator adopts.

## Gates (before any new number; stop with `[BLOCKED]` on failure)

- `scaling_check.py`'s composite reproduces 0.59 / 0.84.
- The administration lane's main state-panel estimate reproduces 0.47.
- One function's 2012 and 2022 county totals from `local_spending_composition_2026_09_18` reproduce
  from the individual-unit files.
- `node main_case_2026_09_23/main_case.js` reports "all gates passed", and the lane's evaluator
  reproduces $203.207–249.640bn at 0.59/0.84.

## Rules and output

- Run with `OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 <script>`
  from the repository root.
- Put `--with <pkg>` wheels in the README.
- Fetch with `curl` through `subprocess`; Python urllib fails TLS here.
- Raw pulls go to `_cache/` (ignored).
- Tag every number `[DATA]`, `[CALCULATION]`, `[SOURCE]`, `[INFERENCE]` or `[TRAINING-DATA]`.
- Steel-man the zero-response view (budget scoring holds appropriations fixed) and the cross-state
  view before judging them.
- Report every specification computed, not selected signs.
- Output: `RESULT.md` opening with `**Verdict:**`, scripts, `derived/` tables, a reproduce block, and
  a full rerun showing `derived/` byte-identical.
- Do not commit. Do not edit outside this directory.
- Reply to the lead with the path and at most 10 lines.
