# Imperfect substitution inside the production term: a native–immigrant nest on the account's own data

Date: 2026-09-22. [CALCULATION on the account's own CPS calibration; MODEL, transported
elasticities; FRAMING-SENSITIVE in §4] Calculation record; narrative authorship remains
operator-owned.

**Verdict:** The complete annual account's production term, +$13.3bn (GDP scaling) or
+$8.8bn (cash scaling) a year to other US residents, assumes that Mexican-origin and other
workers within the same skill group are perfect substitutes. Relaxing that with a nested CES,
natives against foreign-born inside each of the two skill cells, on the same CPS file and the
same replayed chain, **roughly doubles the term at the elasticity the 2026 removal model uses
(ε = 3): +$27.1bn GDP / +$17.9bn cash**, and moves it to +$46.2 / +$30.5bn at ε = 1.3,
+$22.3 / +$14.7bn at ε = 4.6 and +$15.4 / +$10.1bn at ε = 20. The perfect-substitution
limit reproduces the published +13.3226 / +8.7906 to 1e-12. Most of the movement is a
transfer inside the beneficiary set: at ε = 3 natives gain **+$54.0bn** after tax and other
foreign-born residents lose **−$45.9bn**, netting to +$8.0bn of private gain, the rest of the
term being induced tax receipts. The sign never changes. Placing the whole union in a branch
of its own instead (Option B) gives +$754bn at ε = 3, a number produced by removing an entire
CES branch and not by the data; it is reported as structurally unverified. Applied to the
headline, ε = 3 would lower the $165–197bn conditional net cost by $9–14bn; it is **not
applied**, because the choice of ε is a convention the account has not adopted.
[CALCULATION: [`production_nativity_nest_2026_09_22`](../infra/immigration-fiscal/production_nativity_nest_2026_09_22/RESULT.md),
`derived/nest_headline.csv`; independent re-derivation `independent_check.py`]

## 1. Object

The production term lives in `matched_benefits_2026_09_19/model.py`: two skill cells on the
CPS education recode (high school or less; more), a CES between them with σ ∈ {1.5, 2, 2.5},
capital adjusting fully, half or not at all, and the union's earnings share `m[j]` removed
from each cell's labor as if union and outside workers were the same input. The published
figures are the σ = 2, full-adjustment, no-hours-response case, scaled to GDP ($29,298bn) or
to cash earnings. [DATA: `matched_benefits_2026_09_19/derived/audit.json`,
`model_assumptions`; `full_account_benefits_2026_09_20/derived/benefit_scenarios.csv`,
rows `ces_0086_owner000` and `ces_0248_owner000`]

The nest replaces each cell's scalar labor input with a CES aggregate over branches at
elasticity ε, leaving everything above the cell (σ, capital, taxes, the 3,888-scenario grid)
untouched. Two placements of the union's own members are built, because the union is three
generations and its US-born members hold 47% of its low-cell and 78% of its high-cell
earnings [CALCULATION: `derived/branch_composition.csv`]:

- **Option A, by nativity.** Native branch = every US-born worker, including the union's
  G2 and G3+; foreign-born branch = every foreign-born worker, including the union's G1.
  Removal cuts 11.1% of the native branch and 39.1% of the foreign-born branch in the low
  cell (5.5% and 6.9% in the high cell). This is the reading of the account's own population.
- **Option B, union as its own branch.** Natives, other foreign-born and the union as three
  branches at the same ε; removal deletes the union branch entirely. This mirrors the removal
  model's nesting but asserts that a third-generation US-born self-identified Mexican-origin
  worker substitutes worse for other natives than a foreign-born non-Mexican worker does.
  [UNVERIFIED-STRUCTURAL]

The ε grid is {1.3, 3, 4.6, 5, 7, 20, ∞}: 3 is the removal model's chosen midpoint, 1.3 and
4.6 are the two published estimates it cites (Clemens–Lewis; Burstein et al.), 20 is the
upper end of the older literature range it states, ∞ is the account's current assumption; 5
and 7 have no source in this repository and are tagged as such in every row. Every ε is
transported from other populations and other shocks, the same status the account already
gives σ and the tax rates. [SOURCE: Cravino–Levchenko–Ortega–Pandalai-Nayar w34790 p.23 and
Table 1, cached in `mr_leads_papers_2026_09_21/_cache/`; DATA: `derived/audit.json`,
`sigma_NI_grid`]

## 2. Results, Option A

Published case (PEARNVAL earnings, high-school split, s = 0.65, σ = 2, full capital
adjustment, no hours response, full tax retention, no excluded owners), $bn a year, with
minus without the union. Natives and other foreign-born are after-tax private gains; the
production term is their sum plus induced receipts. [CALCULATION: `derived/nest_headline.csv`]

| ε | sourced | natives | other foreign-born | private, net | induced receipts | **term, GDP** | **term, cash** | Δ vs ∞ (GDP) |
|---:|:--:|---:|---:|---:|---:|---:|---:|---:|
| ∞ (current) | yes | −0.61 | +0.38 | −0.24 | 13.56 | **13.32** | **8.79** | 0 |
| 20 | yes | +7.35 | −6.37 | +0.98 | 14.37 | **15.35** | **10.13** | +2.03 |
| 7 | no | +22.36 | −19.09 | +3.26 | 15.90 | **19.16** | **12.64** | +5.84 |
| 5 | no | +31.72 | −27.04 | +4.68 | 16.85 | **21.53** | **14.21** | +8.21 |
| 4.6 | yes | +34.59 | −29.48 | +5.12 | 17.14 | **22.25** | **14.68** | +8.93 |
| 3 | yes | +53.97 | −45.93 | +8.04 | 19.09 | **27.13** | **17.90** | +13.81 |
| 1.3 | yes | +130.54 | −111.09 | +19.44 | 26.72 | **46.17** | **30.46** | +32.85 |

Replicate standard errors of the term (161 joint CPS weights, sampling only) run from $1.1bn
at ε = ∞ to $3.9bn at ε = 1.3; the spread across ε is a model range, not an interval. At
every ε about 85% of the native gain is offset by the other foreign-born residents' loss,
because both sit inside "other US residents", the account's beneficiary set. The term still
rises, through two channels: the netting is not complete, and induced receipts grow with the
gross wage movements because the two branches face different marginal tax rates by cell.

Branch wages under removal, `100 × (ŵ − 1)`, for comparison with the removal model's −0.33%
for natives and +3.2% / +12.2% for authorized and unauthorized immigrants
[CALCULATION: `derived/nest_headline.csv`]:

| ε | natives, low cell | natives, high cell | other foreign-born, low | other foreign-born, high |
|---:|---:|---:|---:|---:|
| ∞ | +5.57 | −1.43 | +5.57 | −1.43 |
| 3 | +2.87 | −1.56 | +16.69 | −1.07 |
| 1.3 | −0.96 | −1.73 | +32.48 | −0.59 |

Only at ε = 1.3 do natives lose in both cells from removal. From ε = 3 up, the between-cell
composition effect dominates in the low cell, where 17.8% of earnings are removed, and native
wages there rise; the native gain in the first table is driven by the high cell. That is a real
difference from the removal model, whose removed group is entirely foreign-born and
low-skill-concentrated; here 47–78% of the removed earnings are US-born.

## 3. Option B, and why its magnitude is not a finding

Option B gives +$754bn GDP / +$498bn cash at ε = 3, +$4,307bn at ε = 1.3 and +$93bn at
ε = 20 [CALCULATION: `derived/nest_headline.csv`, `B_target_branch` rows]. Under it nothing
outside the union is removed, so natives and other immigrants face the same wage change and
both gain (+$357bn and +$79bn at ε = 3). The size comes from the functional form: a CES with
ε < ∞ values the last unit of a vanishing branch at an unbounded marginal product, so deleting
a branch that holds 17.8% of low-cell and 5.8% of high-cell earnings costs the economy far
more than those earnings. That is a statement about the curvature of the aggregator at zero,
not about Mexican-origin workers, and it rests on the untested claim that US-born union
members are a separate input from other natives. The rows are carried so the reader can see
what the removal model's nesting does on this population; they are not a range.
[INFERENCE; UNVERIFIED-STRUCTURAL]

## 4. What it means for the account

[FRAMING-SENSITIVE] The headline band, $165–197bn a year of conditional net cost to other
US residents, uses the ε = ∞ term in each of its four cases (shared or personal allocation,
cash or GDP scaling). Substituting Option A at ε = 3 lowers each case by the Δ in §2, $9.1bn
in the cash cases and $13.8bn in the GDP cases, so the band would read about **$151–188bn**;
at ε = 1.3 about **$132–176bn**; at ε = 20 about **$163–196bn** [INFERENCE: arithmetic on
the account's table, not a re-run of `full_account_2026_09_20`]. None of this is applied.
The account's convention is a choice between transported elasticities from studies of other
populations, and adopting one is an analysis-protocol change for the operator. What the lane
settles is the size of the item ladder entry 166 left open: on this account's own data the
imperfect-substitution correction is a doubling of a small term, $9–14bn a year at the removal
model's elasticity, and $22–33bn at the lowest published estimate, against a $165–197bn net
cost. It moves the size, not the sign, exactly as the entry predicted. The gross sides are
larger than the net, and a reader who counts only natives as beneficiaries would see a
+$54bn gain at ε = 3 while a reader who counts all other residents sees +$8bn; the account
counts all other residents.

## 5. Gates and verification

Nine gates in `derived/audit.json`, all passed on the committed build: the replayed upstream
chain reproduces the two published rows at zero deviation (G1) and the 1,296- and
3,888-row grids intact (G2); the four branch earnings per cell sum bitwise to the upstream
national and union totals in all 161 weights (G7); Euler and the tax partition hold at every
one of 54,432 scenarios and every replicate (G6); zero removal gives zero at every ε (G5);
the ε = ∞ path reproduces the unnested results for both options (G4). One gate was
reformulated. The specification demanded that ε = σ reproduce the unnested model; that is
unsatisfiable, because the nest's cell aggregate is a power mean of the branches and the
unnested model's is an arithmetic mean, and the two differ whenever removal is uneven across
branches (measured: cell-0 quantity 0.8169 nested against 0.8217 unnested). The gate as built
checks that proportional removal reproduces the unnested model at every ε, that ε = σ matches
an independently written flat four-input CES to 1e-12, and that a one-branch tree reproduces
the unnested model. The linearization check agrees to about 2.5 significant figures at a 1%
shock, with the deviation falling two decades per two decades of shock size, so the residual is
the first-order truncation, not a solver defect. No tolerance was loosened; one calibration
defect found by a failing gate (branch shares summing to 1 only to 1.3e-14) was fixed at its
source. The parent session re-derived all seven Option A GDP rows from `branch_composition.csv`
with a separate calculation before committing; `independent_check.py` reproduces them to 5e-12.
[CALCULATION: `derived/audit.json`; `test_nest_model.py`, 11 tests; `independent_check.py`]

## 6. Limits

- Two education cells, one closed economy, no occupations, regions, trade or prices; the
  removal model's mechanism runs through 36 occupations, 44 sectors and 48 regions. Comparable
  in order of magnitude only.
- Two stationary economies, no transition path, no timing. The capital block is unchanged:
  one comparative-static adjustment parameter, not years.
- Every ε is transported; none is estimated on this population. The CPS carries no legal
  status, so the removal model's authorized–unauthorized split has no counterpart, and its
  deeper nesting (σ = 14 inside the foreign-born branch) was left out of the grid for that
  reason, with the machinery built and tested.
- The union's own welfare is excluded, as the account defines beneficiaries; its vanished
  earnings ($1,591bn at GDP scaling) appear only as a diagnostic column.
- The direct fiscal response A is unchanged; only the production term and its induced
  receipts move. Re-running the account with a chosen ε is a separate step.

## 7. Sources

[DATA: CPS ASEC 2025 `pppub25.csv` via `gen_ledger_extension_2026_09_16`; upstream lanes
`matched_benefits_2026_09_19`, `full_account_benefits_2026_09_20`, `full_account_2026_09_20`;
43 input hashes in `derived/audit.json`]
[SOURCE: Cravino, Levchenko, Ortega, Pandalai-Nayar, NBER w34790, as read in
[papers read](immigration-marginal-revolution-leads-read-2026-09-21.md#3-the-removal-model-and-the-accounts-production-term)]
[CALCULATION: `infra/immigration-fiscal/production_nativity_nest_2026_09_22/` — `SPEC.md`,
`BRIEF.md`, `nest_model.py`, `builder.py`, `test_nest_model.py`, `independent_check.py`,
`RESULT.md`, `derived/nest_headline.csv`, `derived/branch_composition.csv`, `derived/audit.json`]

## Revisions

- 2026-09-22: created. Ladder 176; qualifies ladder 166 ("not yet executed" is now
  executed) and FAQ entry 14. No published value changes; the headline band keeps the
  perfect-substitution term pending the operator's choice of ε.
