# Native–immigrant nest inside the production term

**Verdict:** the production term of the complete annual account is **not robust to the
perfect-substitution assumption in size**, and is robust in sign. Reproducing the account's own
counterfactual with a native–immigrant nest inside each skill cell moves the term from
**+13.32bn (gdp scaling) / +8.79bn (cash scaling)** at ε = ∞ to **+27.13bn / +17.90bn** at
ε = 3 under Option A, and to **+754.31bn / +497.71bn** at ε = 3 under the structurally
unverified Option B. Under Option A the move is almost entirely a transfer *inside* the
beneficiary set: natives gain **+53.97bn** and other foreign-born residents lose **−45.93bn**
at ε = 3, gdp scaling, so the net private change is **+8.04bn**
[CALCULATION: `derived/nest_headline.csv`].

All nine gates pass; G3 is reformulated and G9's criterion is option-neutral, both stated in
`RESULT.md` and in `derived/audit.json`. Numbers are conditional model scenarios under a
stationary comparison, never identified policy effects.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 -m unittest discover \
  -s infra/immigration-fiscal/production_nativity_nest_2026_09_22 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline \
  --no-project --with numpy --with pandas --with openpyxl --with pyreadstat --with duckdb \
  python3 infra/immigration-fiscal/production_nativity_nest_2026_09_22/builder.py \
  --source-root /Users/alien/Projects/immigration-research
```

The builder replays `matched_benefits_2026_09_19` into `derived/upstream_replay/` and binds every
input hash that replay declares, so it never reads a stale upstream file. Wall time is about
26 seconds [CALCULATION: `RESULT.md`, verification tails].

## Equations

Let `a[j]` be cell `j`'s share of national compensation, `b[g,j]` branch `g`'s share of cell
`j`'s current earnings, `r[g,j]` the share of that branch removed, `s` the labor share, `adj`
the capital adjustment, `η` the labor-supply elasticity, `ρ = 1 − 1/σ`, `κ = 1 − 1/ε` and
`power = s + adj*(1−s)`. Quantities, wages and capital are normalized to one in the
with-target economy.

```
z[g,j] = (1 - r[g,j]) * h[g,j]
x[j]   = ( Σ_g b[g,j] * z[g,j]**κ ) ** (1/κ)          # κ = 1 exactly at ε = ∞
q      = ( Σ_j a[j] * x[j]**ρ ) ** (1/ρ)
ŵ_g[j] = q**(power-ρ) * x[j]**(ρ-κ) * z[g,j]**(κ-1)
h[g,j] = ŵ_g[j] ** η                                   # damped fixed point, 1e-12, 5000 iters

current_pay[g,j]        = s * a[j] * b[g,j] * (1 - r[g,j])
counterfactual_pay[g,j] = current_pay[g,j] * h[g,j] * ŵ_g[j]
labor_gain[g,j]         = current_pay[g,j] - counterfactual_pay[g,j]     # with minus without
```

Everything above the cell is untouched, so `fiscal_and_private()` is reused verbatim from
`matched_benefits_2026_09_19/model.py`. `nest_model.solve` asserts Euler exhaustion twice, per
cell (`Σ_g counterfactual_pay[g,j] == s*a[j]*q**(power-ρ)*x[j]**ρ`) and in total
(`== s*q**power`), at every scenario and all 161 replicate weights.

`nest_model.py` implements the aggregate as a tree, so a branch may itself be a CES node. A
single-branch tree is the unnested model exactly; `three_level` builds the Cravino-shaped deep
variant, which is written and tested but not in the published grid (see `RESULT.md`).

Linearized around the with-target point at `adj = 1`, with `s_F[j]` the removed branch's share
of cell `j`, `nest_model.linearized_wage_response` implements

```
d log ŵ_N[j] = s_F[j] * ( 1/ε - (1 - a[j])/σ ) * d log f[j]
d log ŵ_N[k] = s_F[j] * ( a[j]/σ ) * d log f[j]                  # k ≠ j
d log ŵ_F[j] = ( s_F[j] * (1/ε - (1 - a[j])/σ) - 1/ε ) * d log f[j]
```

The first two are the coefficients recorded in
`research/immigration-marginal-revolution-leads-read-2026-09-21.md` §3; the third is the
other-immigrant counterpart the memo describes but does not write. Its `−1/ε` term dominates at
every ε in the grid, which is why other immigrants gain from removal under Option A.

## Two nest options, both reported

**`A_by_nativity`** — native (`PRCITSHP` 1–3, including union G2 and G3+) against foreign-born
(`PRCITSHP` 4–5, including union G1). Removal cuts both branches, because most of the union's
earnings belong to people who are US-born: US-born members hold **47.42%** of cell-0 union
earnings and **78.01%** of cell-1 union earnings
[CALCULATION: `derived/branch_composition.csv`]. This is the honest reading of the account's own
population.

**`B_target_branch`** — `[UNVERIFIED-STRUCTURAL]` native non-union, other foreign-born, and the
union as its own branch at the same ε against natives. It asserts that a third-generation
self-identified Mexican-origin US-born worker is a worse substitute for other natives than a
foreign-born non-Mexican worker is. This repository has no evidence for that, and the arm's
magnitudes (up to +4,306.73bn at ε = 1.3, gdp scaling) show how much the assertion carries. It
is reported beside Option A, never instead of it.

## Outputs

| File | Tracked | Contents |
|---|---|---|
| `derived/nest_headline.csv` | yes | the two published cases by ε and option, 28 rows |
| `derived/branch_composition.csv` | yes | four branches × two cells × four proxy/split, 32 rows |
| `derived/audit.json` | yes | 43 source hashes, ε citation status, all gate results, δ-floor table, limits |
| `derived/nest_scenarios.csv` | no | 54,432 rows: 3,888 upstream keys × 7 ε × 2 options |

## Limitations

Copied from `SPEC.md` §7 without softening; the machine-readable copy is `limitations` in
`derived/audit.json`.

1. **No change to the capital block.** One comparative-static capital response,
   `adjustment ∈ {0, .5, 1}`, not an estimated number of years. `domestic_capital_gain`,
   `opportunity_income` and the `.246` capital tax are untouched. The nest moves labor
   composition only.
2. **No dynamics.** Two stationary economies, with versus without the union's labor. No
   transition path, no arrival or removal timing, no capital accumulation path. Cravino's
   short-run/long-run distinction has no counterpart here.
3. **The union's own welfare stays out**, as the account defines its beneficiaries.
   `target_branch_gain_bn` is a diagnostic.
4. **No new fiscal channel.** The direct fiscal response `A` is unchanged. Only `P` and `F`
   move, and the $165–197bn headline is recomputed by re-running the parent, not here.
5. **"Other residents" contains both winners and losers.** Natives gain and other foreign-born
   residents lose from the union's presence under Option A, so the net moves much less than
   either side.
6. **The elasticity is transported, not estimated.** No ε here is estimated on this population.
7. **No occupations, no regions, no trade, no prices.** Two education cells and one closed
   economy. A number here is not comparable to Cravino's $38.6bn except in order of magnitude.
8. **No unauthorized/authorized split.** The union is defined by origin and generation; the CPS
   carries no legal-status variable.
9. **Sign is not at stake.** Ladder entry 166 already records that this affects size, not sign.
10. **Sampling standard errors condition on the model** and on every transported parameter. The
    spread across ε is a model range, not a confidence interval.
