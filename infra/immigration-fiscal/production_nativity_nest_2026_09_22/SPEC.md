# Native–immigrant nest inside the production term — build specification

[UNVERIFIED]

A specification, not an executed result. Every number below is either read
from an existing output (tagged `[DATA: …]`), quoted from a source already in the repo
(`[SOURCE: …]`), derived here analytically (`[DERIVATION]`), or computed by a read-only
probe of the CPS file the production lane already reads (`[CALCULATION]`). No number in
this file comes from model memory. Nothing here has been run as a build.

Date: 2026-09-22. Scope: how to add a native–immigrant nest inside each skill cell of the
complete annual account's production term, so the production gain to other US residents can
be recomputed under imperfect substitution. Written against a read of the live code, not
against the memos' description of it.

---

## 0. What the account currently publishes, and what is at stake

The complete annual account's headline is a conditional net cost to other US residents of
**$165–197bn/year**, with a production term of **+8.79bn (cash scaling)** and **+13.32bn
(GDP scaling)**
[DATA: `research/immigration-complete-annual-account-2026-09-20.md`, table "Source-centered
long-run case", rows "Production plus induced receipts"].

Ladder 166 records the open item: the production term "assumes union and outside workers are
perfect substitutes within two skill groups; under the imperfect native–immigrant substitution
used in the 2026 general-equilibrium removal model, natives' wage gains are several times
larger and other immigrants bear the counterpart — the largest untested assumption found in
the account, affecting size, not sign"
[SOURCE: `research/immigration-confidence-ladder.md` entry 166].

The comparison figure is Cravino–Levchenko–Ortega–Pandalai-Nayar: removing half of 4.95m
unauthorized workers lowers native wages 0.33% at ε=3, which the memo converts to a
**$38.6bn/year** native loss ($26.8bn at ε=4.6, $80.4bn at ε=1.3) using BEA 2024 wages and
salaries of $12,410bn [SOURCE: `research/immigration-marginal-revolution-leads-read-2026-09-21.md` §3].

That is a different counterfactual from this account's (different population, different
removal, no fiscal block). The point of this build is **not** to import $38.6bn. It is to
re-run *this* account's own counterfactual with the substitution assumption relaxed, on this
account's own CPS data, and see what the production term becomes.

---

## 1. The current production model, in the code's own symbols

### 1.1 Where it lives

| Role | Path |
|---|---|
| CES equilibrium + factor prices | `infra/immigration-fiscal/matched_benefits_2026_09_19/model.py` → `equilibrium()`, `fiscal_and_private()` |
| Skill cells, grid, 1,296 scenarios | `infra/immigration-fiscal/matched_benefits_2026_09_19/builder.py` → `main()` |
| Ownership expansion to 3,888 scenarios | `infra/immigration-fiscal/full_account_benefits_2026_09_20/builder.py` → `expand_ownership()` |
| Consumption by the account | `infra/immigration-fiscal/full_account_2026_09_20/welfare.py` → `combine()` |
| CPS microdata | `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`, member `pppub25.csv` (ASEC 2025, income year 2024) |
| Group masks | `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py` lines 233–243 |

### 1.2 Cell definition, exactly as coded

Two skill cells on the CPS education recode `A_HGA`, with a `split` parameter choosing the cut
[DATA: `matched_benefits_2026_09_19/builder.py`, `cut = 39 if split == "hs_or_less" else 42`]:

- `split="hs_or_less"`: cell 0 = `A_HGA` 31–39, cell 1 = `A_HGA` 40–46.
- `split="below_ba"`: cell 0 = `A_HGA` 31–42, cell 1 = `A_HGA` 43–46.

Universe: `civilian = PRPERTYP == 2 or A_AGE < 15`. Earnings proxy: `max(PEARNVAL, 0)` or
`max(WSAL_VAL, 0)`, weighted by `MARSUPWT` with 160 replicate weights (161 columns).

Target (the "union"): `mexico_born ∪ mexican_second_gen ∪ mexican_third_plus_selfid`, masks
asserted disjoint. `mexico_born = PRCITSHP ∈ {4,5} and PENATVTY == 303`;
`mexican_second_gen = PRCITSHP ∈ {1,2,3} and (PEFNTVTY == 303 or PEMNTVTY == 303)`;
`mexican_third_plus_selfid = PRCITSHP ∈ {1,2,3} and both parents US-area and PRDTHSP == 1`
[DATA: `extend_ledger.py:233–243`].

"Other residents" (the beneficiaries) is the complement: every civilian CPS resident outside
that union, all ages and education, 340.110988m against the union's 40.896574m
[DATA: `full_account_2026_09_20/README.md`]. It is defined by *subtraction from the CPS
universe*, not by nativity. This matters in §3: the complement already contains both natives
and non-Mexican foreign-born workers, so a nest that moves income between those two groups
moves it **within** the beneficiary set.

### 1.3 Equations as coded

Quantities, wages and capital are normalized to 1 in the with-target economy. Let
`a[j]` = national compensation share of cell `j`, `m[j]` = target's share of cell `j`'s
earnings, `s` = `labor_share`, `adj` = `capital_adjustment`, `η` = `labor_supply_elasticity`,
`σ` = `sigma`, `ρ = 1 - 1/σ`, `power = s + adj*(1-s)`.

```
x[j]  = (1 - m[j]) * h[j]                      # cell j quantity without the target
q     = ( Σ_j a[j] * x[j]**ρ ) ** (1/ρ)         # geometric mean at σ = 1
K_wo  = q ** adj
Y_wo  = q ** power
ŵ[j]  = q**(power - ρ) * x[j]**(ρ - 1)          # without/with wage ratio in cell j
h[j]  = ŵ[j] ** η                               # fixed point, 1e-12, 5000 iterations
```

Income accounting [DATA: `matched_benefits_2026_09_19/model.py:equilibrium`]:

```
current_pay[j]        = s * a[j] * (1 - m[j])
counterfactual_pay[j] = current_pay[j] * h[j] * ŵ[j]
labor_gain[j]         = current_pay[j] - counterfactual_pay[j]     # with minus without
domestic_capital_gain = (1 - s) * (1 - Y_wo)
opportunity_income    = (1 - s) * (1 - K_wo)
capital_gain          = domestic_capital_gain - opportunity_income
```

Euler is asserted at every scenario and replicate: `Σ_j counterfactual_pay[j] == s * Y_wo`.

`fiscal_and_private()` then splits income into private WTP and current receipts with marginal
rates `τ = [.384, .426]` by cell, capital tax `.246`, `tax_retention` and
`excluded_owner_share`, and asserts `private_wtp + taxes == included_gross - resource_cost +
excluded_owner_share * capital_tax_gain`.

### 1.4 The assumption being relaxed

`x[j] = (1 - m[j]) * h[j]` subtracts the target's earnings share from the cell's efficiency
units. Target labor and outside labor inside a cell are therefore **the same input**, and the
only thing the model can credit other residents with is the *between-cell* composition effect.
The lane states this itself: "Within each skill target and outside workers are perfect
substitutes" [DATA: `matched_benefits_2026_09_19/derived/audit.json`, `model_assumptions`].

### 1.5 The 3,888-scenario grid

`matched_benefits_2026_09_19/builder.py` runs
`proxy(2) × split(2) × normalization(2) × labor_share(3) × sigma(3) × capital_adjustment(3) ×
labor_supply_elasticity(2) × capital_tax_retention(3) = 1,296` scenarios; values are
`("PEARNVAL","WSAL_VAL") × ("hs_or_less","below_ba") × ("gdp","cash") × (.60,.65,.70) ×
(1.5,2.,2.5) × (0.,.5,1.) × (0.,.33) × (0.,.5,1.)`.
`full_account_benefits_2026_09_20/builder.py:expand_ownership()` multiplies by
`excluded_capital_owner_share ∈ (0., .5, 1.)` → **3,888** rows, asserted by
`if len(source) != 1296` and confirmed by the file's 3,889 lines including the header
[DATA: `full_account_benefits_2026_09_20/derived/benefit_scenarios.csv`].

Scaling: `gdp` multiplies normalized results by $29,298bn; `cash` multiplies by
`national_earnings / labor_share`.

---

## 2. Calibration facts the build starts from

All from the existing lane outputs and a read-only probe of `pppub25.csv` using the exact
masks of §1.2. Proxy `PEARNVAL`, split `hs_or_less` (the reference case).

Cell aggregates [DATA: `matched_benefits_2026_09_19/derived/skill_composition.csv`]:

| Quantity | Cell 0 (A_HGA 31–39) | Cell 1 (A_HGA 40–46) |
|---|---:|---:|
| National earnings, $bn | 2,706.19 | 9,859.38 |
| `a[j]` | 0.215366 | 0.784634 |
| `m[j]` (union share of cell) | 0.178304 | 0.057515 |

Union share of all national earnings = **8.3528%**, matching the memo's 8.35%
[CALCULATION: 1,049.58 / 12,565.57 from the same file].

Four-branch decomposition of each cell, the input the nest needs
[CALCULATION: read-only probe of `pppub25.csv` with the §1.2 masks; cell totals reconcile to
`skill_composition.csv` to the cent]:

| Branch | Cell 0, $bn | Cell 0 share | Cell 1, $bn | Cell 1 share |
|---|---:|---:|---:|---:|
| Native, not union (US-born non-Mexican-origin) | 1,828.61 | 0.675713 | 7,607.74 | 0.771625 |
| Union, US-born (G2 + G3+) | 228.80 | 0.084547 | 442.39 | 0.044870 |
| Foreign-born, not union | 395.06 | 0.145983 | 1,684.58 | 0.170861 |
| Union, Mexico-born (G1) | 253.72 | 0.093757 | 124.67 | 0.012645 |
| Cell total | 2,706.19 | 1.000000 | 9,859.38 | 1.000000 |

The same four-way table for the other three proxy/split combinations is in §6's first build
step; the `below_ba` split moves 25.3% of cell-1 earnings into cell 0 and cuts cell 0's
union-G1 share from 0.0938 to 0.0583 with `PEARNVAL` [CALCULATION: same probe].

**The decisive calibration fact.** Inside the union, US-born members hold
228.80 / (228.80 + 253.72) = **47.42%** of cell-0 union earnings and
442.39 / (442.39 + 124.67) = **78.01%** of cell-1 union earnings [CALCULATION: same probe].
Most of the union's earnings in the high-skill cell belong to people who are US-born. A nest
built "by nativity" therefore puts most of the removed labor in the *native* branch, and the
native-branch result will not resemble Cravino's, whose removed group is entirely foreign-born
and entirely unauthorized. §3.3 is where this is decided, and it is the single choice that
most changes the answer.

---

## 3. The nested-CES extension

### 3.1 Structure

Replace the scalar cell quantity `x[j]` with a CES aggregate over branches. Let
`κ = 1 - 1/ε` with `ε = sigma_NI`, and let `b[j]` be the branch's share of cell `j`'s
current earnings (so the aggregate equals 1 at the with-target point).

**Two-branch form (nativity):**

```
x[j] = ( b[j] * n[j]**κ + (1 - b[j]) * f[j]**κ ) ** (1/κ)     # geometric mean at ε = 1
```

with `n[j]`, `f[j]` the normalized native and foreign-born efficiency labor in cell `j`.
At `n = f = 1`, `x[j] = 1`, so the with-target equilibrium is unchanged by construction; this
is the first gate in §5.

Everything above the cell is untouched: `q`, `K_wo`, `Y_wo`, `power`, the capital block and
the tax partition all keep their present form. Only `x[j]` gains internal structure.

### 3.2 Factor prices

[DERIVATION] Marginal product of a branch input, relative to its with-target level:

```
ŵ_N[j] = q**(power - ρ) * x[j]**(ρ - κ) * n[j]**(κ - 1)
ŵ_F[j] = q**(power - ρ) * x[j]**(ρ - κ) * f[j]**(κ - 1)
```

At `κ = ρ` (that is, `ε = σ`) both collapse to the current `ŵ[j]`, which is the second gate.
At `ε → ∞`, `κ → 1`, `x[j] = b[j]*n[j] + (1-b[j])*f[j]`, and the model reduces exactly to the
present one with `1 - m[j]` in place of the weighted sum — the third gate.

Euler still holds: branch payments sum to `s * a[j] * q**(power-ρ) * x[j]**ρ` per cell and to
`s * Y_wo` overall, so the existing `Counterfactual Euler conservation failed` assertion in
`equilibrium()` can be kept verbatim with the branch sum substituted.

Linearized around the with-target point at full capital adjustment (`adj = 1`, `power = 1`,
`power - ρ = 1/σ`, `ρ - κ = 1/ε - 1/σ`), with `s_F[j]` the removed branch's share of cell `j`
earnings:

```
d log ŵ_N[j] = s_F[j] * ( 1/ε - (1 - a[j])/σ ) * d log f[j]      # same cell
d log ŵ_N[k] = s_F[j] * ( a[j]/σ ) * d log f[j]                  # other cell, k ≠ j
d log ŵ_F[j] = ( s_F[j] * (1/ε - (1 - a[j])/σ) - 1/ε ) * d log f[j]
```

The first two reproduce the formulas recorded in the reading memo,
`s_F × (1/ε − (1 − a_j)/σ)` in the same group and `s_F × a_j/σ` in the other
[SOURCE: `research/immigration-marginal-revolution-leads-read-2026-09-21.md` §3]. This spec
adds the qualification that those formulas hold at `adj = 1`; at `adj < 1` the first
coefficient is `power - ρ = s + adj*(1-s) - 1 + 1/σ` in place of `1/σ`. The third line is the
other-immigrant counterpart, which the memo describes but does not write. Its `-1/ε` term
dominates at every `ε` in the grid, so other immigrants gain from removal — the mechanism
behind Cravino's +3.2% authorized / +12.2% unauthorized
[SOURCE: same memo §3; lane note `mr_leads_papers_2026_09_21/notes/cravino_levchenko_ortega_pandalai_w34790.md`].

These linearizations are for interpretation and for a small-shock test. The build solves the
exact system, as the present code does.

### 3.3 Where the union's US-born members go — two options, both to be built

The union spans three generations. G1 (`mexico_born`) is foreign-born; G2
(`mexican_second_gen`) and G3+ (`mexican_third_plus_selfid`) are US-born by construction
(`PRCITSHP ∈ {1,2,3}`). The nest must place them, and the placement is not innocuous: §2 shows
US-born union members hold 47.4% and 78.0% of union earnings in the two cells.

**Option A — by nativity (two branches).** Native branch = all `PRCITSHP ∈ {1,2,3}`, including
union G2 and G3+. Foreign branch = all `PRCITSHP ∈ {4,5}`, including union G1. Removal cuts
both branches:

```
ν[j] = union-G2G3 earnings / native earnings in cell j
φ[j] = union-G1  earnings / foreign earnings in cell j
n[j] = (1 - ν[j]) * h_N[j]
f[j] = (1 - φ[j]) * h_F[j]
b[j] = native share of cell j earnings
```

From §2, cell 0: `b = 0.760261`, `ν = 0.111208`, `φ = 0.391072`; cell 1: `b = 0.816495`,
`ν = 0.054954`, `φ = 0.068907` [CALCULATION: branch dollars of §2].
This option answers "what does imperfect native–immigrant substitution do to *this* account?"
It is the honest reading of the account's own population, and it will give a *smaller* native
gain than Cravino, because a large part of the removed labor is itself in the native branch.

**Option B — separate target branch (three branches).** Keep natives and non-union
foreign-born as branches, and give the union its own branch at the same `ε` against natives:

```
x[j] = ( b_N[j]*n[j]**κ + b_O[j]*o[j]**κ + b_T[j]*t[j]**κ ) ** (1/κ)
```

with `t[j] → 0` under removal (a `t[j] = δ` floor, `δ = 1e-9`, avoids `0**(κ-1)` at `κ < 1`;
the limit is finite in income terms and the build must assert convergence as `δ → 0`).
This option mirrors Cravino's own nesting more closely and isolates "how different is the union
from natives", but it asserts that a third-generation self-identified Mexican-origin US-born
worker is a worse substitute for other natives than a foreign-born non-Mexican worker is. That
is a strong claim the repo has no evidence for; the build must label Option B
`[UNVERIFIED-STRUCTURAL]` and report it beside, never instead of, Option A.

A **deeper variant of B** follows Cravino exactly: natives vs foreign at `ε`, then inside
foreign, union-G1 vs other foreign at `σ_FT = 14` [SOURCE: Cravino et al. Table 1 p.24,
"σ Authorized-unauthorized 14 Borjas and Cassidy (2019)", cached text line 1590 in
`mr_leads_papers_2026_09_21/_cache/cravino_levchenko_ortega_pandalai_w34790.txt`]. Build it
only if Option A and B are both clean; it is a fourth arm, not a replacement.

Both options are reported. The build does not pick one.

### 3.4 Wage and income changes to report

For each branch `g ∈ {native-non-union, other-foreign-born, union}` and cell `j`, with the
sign convention of the existing code (**with target minus without target**):

```
current_pay[g,j]        = s * a[j] * share[g,j]
counterfactual_pay[g,j] = current_pay[g,j] * h[g,j] * ŵ_g[j]
labor_gain[g,j]         = current_pay[g,j] - counterfactual_pay[g,j]
```

The union's own branch has `counterfactual_pay = 0` and is **excluded from every welfare
total**, exactly as the account excludes the target's own welfare (§6 (f)). It is reported
only as a diagnostic.

`labor_gain` for natives and other immigrants is then passed to the *unchanged*
`fiscal_and_private()`. One decision is forced: that function takes marginal tax rates by
skill cell, `τ = [.384, .426]`. Keep those rates per cell and apply them to each branch within
the cell. Do not invent branch-specific rates; the repo has none, and the source is a 2017
two-cell transport [SOURCE: `matched_benefits_2026_09_19/README.md`, "Current federal/state/
payroll marginal rates .384/.426 come from the 2017 components of Colas–Sachs Table 1"].

---

## 4. Parameter grid and where each value comes from

`sigma_NI` (`ε`) is a **new** dimension. The brief's grid is `{3, 5, 7, 20, ∞}`. Three of
those five have a repo citation; two do not.

| `ε` | Repo citation | Verbatim source |
|---|---|---|
| **3** | Yes | "We select 3, as roughly the midpoint between these two recent estimates, and evaluate robustness to higher and lower values." [SOURCE: Cravino–Levchenko–Ortega–Pandalai-Nayar w34790, p.23; cached text line 1545–1546 in `mr_leads_papers_2026_09_21/_cache/cravino_levchenko_ortega_pandalai_w34790.txt`; Table 1 p.24 "ϵ Native-foreign immigrants 3"] |
| **20** | Yes, as a range endpoint only | "While the earliest studies had put this elasticity in the 10-20 range, more recent estimates yield much lower values." [SOURCE: same paper, p.23, cached line 1542–1544]. The repo does **not** hold a numeric native–immigrant elasticity attributed to Ottaviano–Peri. The canon audit describes their design as "an *estimated* immigrant–native substitution elasticity" and gives outputs (+0.6% natives, −6.7% prior immigrants) but no elasticity value [SOURCE: `research/immigration-canon-citation-audit-2026-09-17.md` §P3]. Use 20 as *the upper end of the literature range the primary text states*, and label it that way. Do not attribute it to Ottaviano–Peri. |
| **∞** | Yes | The account's own current assumption: "Within each skill target and outside workers are perfect substitutes" [DATA: `matched_benefits_2026_09_19/derived/audit.json`, `model_assumptions`]. The falsification condition in the canon audit is "an estimate of the within-cell immigrant–native elasticity that is robust to the high-school-student sample choice and is indistinguishable from infinity" [SOURCE: `research/immigration-canon-citation-audit-2026-09-17.md` §P3(f)]. |
| **5** | **No repo citation.** No paper in this repo reports 5 as a native–immigrant elasticity. |
| **7** | **No repo citation.** Same. |

**Recommended change to the grid, for the operator to accept or reject.** Replace 5 and 7 with
the two published estimates the repo actually holds, keeping the grid at five points:

```
sigma_NI ∈ {1.3, 3, 4.6, 20, ∞}
```

- **1.3** — "Clemens and Lewis (2024), using a randomized experiment, estimate a value of 1.3."
  [SOURCE: Cravino et al. p.23, cached line 1544–1545]
- **4.6** — "Burstein et al. (2020) report an estimate of 4.6." [SOURCE: same sentence]

These are the two endpoints Cravino's own sensitivity table uses (ϵ=1.3 / ϵ=4.6 rows, cached
lines 2609–2627), so the arm is directly comparable to the paper the ladder entry cites. If
the operator wants 5 and 7 retained, the build must run all seven points and mark 5 and 7
`[UNVERIFIED: no repo source for this value]` in every output row. **Default: run all seven**
(`{1.3, 3, 4.6, 5, 7, 20, ∞}`) and carry the tag, so the choice costs nothing and no value is
silently dropped.

Everything else in the grid is unchanged, so the scenario count becomes
`3,888 × |sigma_NI|` per nest option. At seven points and two options that is 54,432 rows;
at five points and two options, 38,880. Both are far below the 497,664 rows
`full_account_2026_09_20/welfare.py` already writes, so no chunking is needed.

---

## 5. Gates — all must pass before the nest is reported

Ordered. A failure stops the build; none of these is a warning.

**G1 — reproduce the published production term to the dollar, before touching anything.**
Run the existing chain and read two named rows out of `benefit_scenarios.csv`:

| `scenario_id` | keys | `private_plus_receipts_bn` |
|---|---|---:|
| `ces_0086_owner000` | PEARNVAL, hs_or_less, **gdp**, s=.65, σ=2.0, adj=1.0, η=0.0, retention=1.0, owner=0.0 | **13.32259791925651** |
| `ces_0248_owner000` | PEARNVAL, hs_or_less, **cash**, s=.65, σ=2.0, adj=1.0, η=0.0, retention=1.0, owner=0.0 | **8.790627696465311** |

[DATA: `full_account_benefits_2026_09_20/derived/benefit_scenarios.csv`]. Components for
`ces_0086_owner000`: `private_after_tax_wtp_bn = -0.23592432475743744`,
`induced_current_receipts_bn = 13.558522244013947`. These two rows are the +13.32 / +8.79
published in the account table (§0), so matching them to the dollar is the reproduction gate
the brief asks for. Assert exact float equality after a fresh build; the existing
`close(..., atol)` helper is the right tool at `atol = 1e-9`.

**G2 — the grid is intact.** `len(benefit_scenarios) == 3888`, `len(scenarios) == 1296`, 18
ownership baselines reconciled — the assertions already in `expand_ownership()` and
`validate_ownership_baselines()`. Do not weaken them.

**G3 — the nest is a strict generalization.** With `ε = σ` for every scenario in the grid, the
nested solver must return the *existing* `labor_gain`, `capital_gain`, `private_wtp` and
`current_receipts_gain` to `1e-12` relative. This is the strongest single test and it covers
all 1,296 upstream scenarios, not a sample.

**G4 — the perfect-substitution limit.** At `ε = ∞` (`κ = 1`) the nested solver must return the
existing results to `1e-12` relative, for every scenario. G3 and G4 are different code paths
(`κ = ρ` vs `κ = 1`) and both must be checked.

**G5 — zero shock.** With `ν = φ = 0` (nothing removed) all gains are 0 at every `ε`, matching
`test_model.py::test_zero_and_homogeneous_limits`.

**G6 — Euler and the tax partition.** The existing assertions in `equilibrium()` and
`fiscal_and_private()` must be kept live, with branch sums substituted, at every scenario and
every one of the 161 replicate weights.

**G7 — calibration reconciliation.** The four branch earnings totals per cell must sum to the
`national` estimate in `skill_composition.csv` to `1e-6` relative, and the union branches must
sum to that file's `target` estimate. The probe in §2 already satisfies this; the build must
assert it rather than trust it.

**G8 — small-shock agreement with the linearization.** At a 1% removal, the exact solver and
the §3.2 formulas must agree to 3 significant figures, at `adj = 1`. This catches sign and
index errors that G3/G4 cannot, because those two collapse the nest.

**G9 — monotonicity, reported not asserted.** Natives' gain should fall monotonically in `ε`
and other immigrants' loss should fall with it. Report any non-monotone cell rather than
suppressing it; a non-monotonicity here would be a finding, not necessarily a bug.

---

## 6. Outputs

One directory, `infra/immigration-fiscal/production_nativity_nest_2026_09_22/derived/`
(git-ignored, as the sibling lanes' are).

**`branch_composition.csv`** — the §2 table for all four proxy × split combinations:
`proxy, split, skill, branch, population, positive_earners, earnings_estimate, se_sampling,
share_of_cell`, with all 161 weights. Four branches × 2 cells × 4 combinations = 32 rows.

**`nest_scenarios.csv`** — the main output. One row per
`(existing 3,888 keys) × sigma_NI × nest_option`, carrying:

| Column | Meaning |
|---|---|
| `nest_option` | `A_by_nativity`, `B_target_branch`; `B_deep_cravino` only if the first two pass every gate |
| `sigma_NI` | `ε`, with `inf` written as `inf` |
| `sigma_NI_sourced` | `true` / `false` per §4 |
| `native_production_gain_bn` | private after-tax WTP of natives outside the union, with minus without |
| `other_immigrant_production_gain_bn` | same for foreign-born outside the union |
| `other_residents_private_bn` | the two above summed = the account's `private_after_tax_wtp_bn` |
| `induced_current_receipts_bn` | `F`, unchanged definition |
| `private_plus_receipts_bn` | the production term the account consumes |
| `target_branch_gain_bn` | diagnostic only, never in a welfare total |
| `capital_gain_bn`, `capital_tax_gain_bn` | unchanged blocks, reported for reconciliation |
| `delta_vs_perfect_substitution_bn` | this row minus the matching `ε = ∞` row |
| `wage_pct_native_cell0/1`, `wage_pct_other_fb_cell0/1` | `100 * (ŵ - 1)`, for comparison with Cravino's −0.33% / +3.2% |
| `interpretation` | `CONDITIONAL_MODEL_NOT_IDENTIFIED_POLICY_EFFECT`, as the sibling lanes write |

**`nest_headline.csv`** — the four published cases only (PEARNVAL, hs_or_less, s=.65, σ=2.0,
adj=1.0, η=0.0, retention=1.0, owner=0.0, cash and gdp), by `ε` and `nest_option`, in $bn:
production gain to natives, loss to other immigrants, net to other residents, and the
perfect-substitution reproduction (13.32 / 8.79) as the first row of each block. This is the
table the memo and the ladder entry will quote.

**`audit.json`** — source hashes for the CPS file, `model.py`, `builder.py`, this SPEC, and
every input read; the `ε` grid with its per-value citation status; the gate results; and the
limitation list of §7.

Sampling: carry the 161-weight SE for the branch composition and for the core
`excluded_capital_owner_share == 0` rows only, following the existing rule
(`sampling_status = 'point_only_no_covariance_inference'` elsewhere). Do not invent covariance
for the new `ε` dimension — `ε` is an assumption, not a sampled quantity, and an interval
across `ε` is a model range, not a confidence interval.

---

## 7. What this extension cannot do

Stated so the memo cannot overclaim.

1. **No change to the capital block.** The module has one comparative-static capital response,
   `adjustment ∈ {0, .5, 1}`, "not an estimated number of years"
   [SOURCE: `matched_benefits_2026_09_19/README.md`]. The nest changes labor composition only.
   `domestic_capital_gain`, `opportunity_income` and the `.246` capital tax are untouched.
2. **No dynamics.** The comparison remains two stationary economies, with versus without the
   union's labor. There is no transition path, no arrival or removal timing, no capital
   accumulation path. Cravino's short-run/long-run distinction has no counterpart here.
3. **The union's own welfare stays out**, as the account defines its beneficiaries: "other US
   residents outside the canonical target" [DATA: `full_account_benefits_2026_09_20/derived/audit.json`].
   `target_branch_gain_bn` is a diagnostic.
4. **No new fiscal channel.** `A` (the direct fiscal response) is set by
   `full_account_2026_09_20/welfare.py` and is unchanged. Only `P` and `F` move. The headline's
   $165–197bn band is recomputed by re-running the parent, not by editing it here.
5. **"Other residents" contains both winners and losers.** Natives gain and other foreign-born
   residents lose from the union's presence under the nest. The account's beneficiary set holds
   both, so the *net* may move much less than either side. That is the expected result, and the
   build must report the gross sides so the netting is visible.
6. **The elasticity is transported, not estimated.** No `ε` here is estimated on this
   population. Every value is imported from a paper about a different population and a
   different shock, which is the same status the account already assigns `σ`, the tax rates and
   the capital tax.
7. **No occupations, no regions, no trade, no prices.** Cravino's mechanism runs through 36
   occupations, 44 sectors and 48 regions with trade costs
   [SOURCE: lane note `cravino_levchenko_ortega_pandalai_w34790.md` §1]. This model has two
   education cells and one closed economy. A number produced here is not comparable to
   Cravino's $38.6bn except in order of magnitude.
8. **No unauthorized/authorized split.** The union is defined by origin and generation, not by
   legal status; the CPS carries no status variable. Option B's deep variant borrows Cravino's
   `σ = 14` nesting shape but applies it to G1 vs other foreign-born, which is a different
   partition than authorized vs unauthorized.
9. **Sign is not at stake.** Ladder 166 already says this affects "size, not sign", and §7.5
   is why. A build that returns a sign flip in the headline should be treated as a bug until
   the netting in §7.5 is checked.

---

## 8. Build size and reuse

**Reused unchanged** (no edits to these files):

- `matched_benefits_2026_09_19/model.py`: `fiscal_and_private()` verbatim — it takes
  `labor_gain` as an array and does not care how many branches produced it, provided the
  skill axis is preserved. The `τ` reshape on `result["labor_gain"].ndim` already handles the
  replicate axis.
- `full_account_benefits_2026_09_20/builder.py`: `sha()`, `close()`, `accounting()`,
  `read_verified()`.
- `full_account_2026_09_20/builder.py`: `read_allocations()`, `verify_export()`.
- The group masks in `extend_ledger.py:233–243`, imported exactly as
  `matched_benefits_2026_09_19/builder.py` imports them (`sys.path.insert` +
  `import extend_ledger as ext`, with `A_HGA` appended to `ext.base.PERSON`). `PRCITSHP`,
  `PENATVTY`, `PEFNTVTY`, `PEMNTVTY` are **already** in `base.PERSON`
  [DATA: `infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py:24–34`], so no column
  extension is needed for the nest.

**Written new:**

| File | Purpose | Est. lines |
|---|---:|---:|
| `nest_model.py` | `nested_equilibrium(shares, branch_shares, removed, sigma, sigma_ni, labor_share, adjustment, elasticity)`; a generalization of `equilibrium()` with a branch axis, same fixed point, same Euler assertion | 110 |
| `builder.py` | branch composition from CPS, grid expansion over `ε` and `nest_option`, replay + G1/G2 gates, three CSVs, `audit.json` | 240 |
| `test_nest_model.py` | G3, G4, G5, G8 plus fail-loud input tests, in the style of `matched_benefits_2026_09_19/test_model.py` | 130 |
| `README.md` | verdict, reproduce commands, equations, limitations | 90 |
| **Total** | | **≈570** |

The `equilibrium()` fixed point generalizes cleanly: `log_hours` gains a branch axis, the
`desired = elasticity * log_wage` update is per branch, and the `.75/.25` damping and `1e-12`
tolerance carry over. Expect the iteration count to rise at low `ε`; if it does not converge in
5000 iterations, raise the damping rather than the tolerance, and fail loud if it still does
not — a silent tolerance relaxation would break G3.

Runtime: the upstream replay dominates. The nest multiplies the solver calls by
`|sigma_NI| × |nest_option|` (14 or 10), so expect roughly 10–15× the current
`matched_benefits` build time, still a single-digit number of minutes with the 161 replicate
weights vectorized on the trailing axis as they already are.

**Reproduce commands the build must carry in its README**, matching the sibling lanes:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 -m unittest discover \
  -s infra/immigration-fiscal/production_nativity_nest_2026_09_22 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline \
  --no-project --with numpy --with pandas --with openpyxl --with pyreadstat --with duckdb \
  python3 infra/immigration-fiscal/production_nativity_nest_2026_09_22/builder.py \
  --source-root /Users/alien/Projects/immigration-research
```

---

## 9. Open questions for the operator

1. **Grid.** §4 recommends `{1.3, 3, 4.6, 20, ∞}` over `{3, 5, 7, 20, ∞}`, because 5 and 7 have
   no source in this repo and 1.3 and 4.6 are the two published estimates the repo holds. The
   default in §4 runs all seven and tags the two unsourced values, which needs no decision.
2. **Nest option for the headline.** Option A is the defensible reading of this account's
   population; Option B is the closer analogue of Cravino's design but asserts something about
   third-generation US-born workers that the repo cannot support. The build reports both; which
   one a memo or ladder entry quotes is a framing judgment, not a technical one.
3. **Whether a result enters the account at all.** This lane recomputes `P` and `F`. Feeding it
   into the $165–197bn headline means re-running `full_account_2026_09_20` against a new
   `benefit_scenarios.csv`, which changes a published number. That is a separate, gated step
   and is not in this spec.
