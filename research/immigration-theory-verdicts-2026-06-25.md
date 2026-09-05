# Generator-bank checks — corrected evidentiary status

**Current adjudication: 2026-09-05.** The earlier PASS/FAIL count is withdrawn as a count of empirically verified or falsified theories. Executable SQL, a true arithmetic identity and a successful empirical falsifier are different things. Later repairs that made 27 queries execute did not establish that they tested their stated scientific claims. [SOURCE: historical scorecard below] [SOURCE: [repair decision](../decisions/2026-09-05-material-inference-repair.md)]

| Historical result | Correct adjudication | Reason |
|---|---|---|
| M13: positive annual proxy versus negative NAS lifetime NPV | **Invalid input; scope warning survives analytically** | The +$1,519 proxy is invalidated by person/household and education errors. Even valid opposite signs for different populations, budgets and horizons would not empirically falsify a common-estimand theory. |
| I8: 25% assumed early exit produces 25% fewer person-years | **Scenario identity, not empirical rejection** | The output is imposed by the assumed multiplier. Exit can change fiscal NPV in either direction through timing and selection; taxes and benefits do not accrue uniformly. Check the source model's emigration assumptions before applying another exit discount. |
| F5: positive NPV without an innovation tag | **Mechanism unidentified** | A missing metadata field is not an intervention that removes innovation. The model must actually switch the mechanism off to test whether it is necessary. The historical row also mislabels HS/some-college benchmarks as college+. |
| I: India and Mexico net values halved at year 10+ | **Assumed persistence, not measured assimilation** | A common decay multiplier preserves proportional differences by construction. The entry-level fiscal inputs are also invalidated. |
| M: annuity ratio 2.47 against a predeclared factor-of-two band | **Outside the stated arithmetic band; no scientific equivalence verdict** | “Same order of magnitude” cannot retroactively change the threshold. Price years, populations and fiscal scope differ before any ratio is meaningful. |
| M: remittances exceed the fiscal proxy | **Not a common-ledger test** | The first denominator was wrong; the later repair still compares a private flow with a selected public balance and uses an invalid fiscal input. Gross remittances are not a net global resource loss. |
| O / P: national ITEP taxes or city spending exceed a Mexico subset's proxy | **Incomparable totals** | Population, geography, ledger and time coverage differ. A larger number does not test the proposed fiscal effect. |
| N: per-pupil spending falls within a band / exceeds $15k | **Unit or plausibility check only** | Neither test validates the population numerator, immigrant attribution or marginal school cost. A source-derived series correlated with its source is not independent validation. |
| T: nominal earnings rise from 1980 to 2010 | **Not a test of the composition mechanism** | Inflation, population growth, capital and productivity can all raise that total. “Holding incumbents' outcomes fixed, adding positive output raises the sum” is an identity, not this time-series estimate. |
| V: Texas status-rate ordering over 2012–2018 | **Descriptive persistence for the measured outcome** | It does not track people across generations or identify cultural persistence/decay, latent offending or the causal effect of immigration. |
| A: education ordering / scenario sign differences | **Model-output comparisons** | They describe the stored benchmark assumptions. They are not independent validation of those models or a measured universal education effect. |
| L: foreign-born health expenditure below native expenditure | **Descriptive comparison, conditional on source population and adjustment** | Differences in age, insurance, access and selection prevent reading spending alone as a causal health advantage. Missing elderly cells or ambiguous bridge queries remain unadjudicated. |
| Repaired K border/gateway RPP comparison | **Descriptive price-context contrast** | State RPP differences do not identify immigration's causal local cost or a border/gateway mechanism. |

[SOURCE: the original query descriptions and reported calculations preserved below] [INFERENCE: estimand, dimensional and identification checks]

No replacement numerical “theories verified” tally is reported. Original predictions and thresholds remain historical; redefining a test after seeing its output would be exploratory re-specification requiring new evidence. Any later empirical score must identify the source population, counterfactual, outcome, testable prediction, uncertainty and predeclared decision rule, and must not use invalidated fiscal inputs. Missing data is an unresolved test, not evidence for or against a theory. [INFERENCE]

The original generator JSONs are present under `research/.mining/`, which is the path declared by `build_lifetime_evidence_warehouse.py`; they are historical inputs, not fresh empirical verification. NAS's demographic projection explicitly already incorporates emigration as well as mortality and fertility (local source, chapter 8 demographic-method appendix, printed p.380). An extra blanket exit multiplier must therefore be labeled a sensitivity relative to that baseline, not a correction for omitted emigration. This correction does not claim a review of the original agent run. [SOURCE: builder declaration, mining inputs, and NAS demographic-method appendix]

## Revisions

- **2026-09-05:** Re-adjudicated the full historical scorecard by what each calculation can establish; withdrew unsupported empirical PASS/FAIL claims following the [material inference repair](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical version — retained for provenance</summary>

# Generator-Bank Theory Verdicts — running the falsifiers

**Date:** 2026-06-25
**What this is:** The generator banks (clusters A–V) embed **62 falsifiable theories**, of which **32 carry a runnable `duckdb_test`**. Apart from two run by hand this session (V08 crime-null, V04 assimilation), they had **never been executed against the built warehouse**. This memo runs all 32, scores each PASS / FAIL / INCONCLUSIVE against its own `prediction`/`falsifier`, and records the harness state. This is the project's generative principle made literal: verified/falsified ÷ total.

## Headline

- **32 runnable theories → 21 executed, 11 unrunnable.** 12 ran as-written; **9 more recovered** by fixing schema-alias drift (`ctx.`→`context.`, `life.`→`lifetime.` — the warehouse schema names changed after the tests were authored); **11 genuinely broken** (missing tables/columns, or prose accidentally in the SQL field).
- **Of the 21 scored: ~15 PASS, 3 FAIL, 3 INCONCLUSIVE.**
- **The 3 FAILs are the highest-value output** — each is a real disconfirmation or scope-limit the banks asserted away.
- **Meta-finding: the falsification harness was authored but never wired to actually run.** 20 of 32 errored on first execution. A scaffold of "falsifiable" predictions that no one has run is not yet falsifiable — it's aspirational. Fixing the source `duckdb_test`s is a concrete follow-up (below).

## The 3 FAILs (disconfirmations — read these first)

| Theory | What failed | Why it matters |
|---|---|---|
| **M13** — "Annual federal proxy confirms lifetime NAS sign" | Mexico annual federal net = **+$1,519** but NAS <HS lifetime NPV = **−$109k**. Opposite signs. | Empirically demonstrates the ledger-map's "coordinate-switching" warning: a positive annual federal cash-flow and a negative lifetime all-government NPV are different books. You cannot read one as the other's sign. |
| **I8** — "Return migration is fiscal-neutral" | Base-case 25% early-exit (years 0–5) cuts effective <HS person-years by **25%** (7.69M → 5.77M), far past the 5% neutrality threshold. | Return migration materially changes the fiscal denominator. "Fiscal-neutral exit" is false at realistic emigration rates — the lifetime NPV stock is over-counted if exit is ignored. |
| **F5** — "H-1B innovation spillover is load-bearing for positive high-skill NPV" | Positive college+ NPV (NAS: +$49k HS, +$205k some-college, +$514k other) stands under `baseline_public_goods` with **no innovation/spillover tag**. | Representation gap: the warehouse's positive high-skill NPV is NOT conditioned on the innovation mechanism the theory says drives it. The positive sign may be over-attributed; the sensitivity is untestable as built. |

## Data-quality flags surfaced by the run

- **M (remittance):** `remit_per_adult` = **$151,636** for the Mexico cell — implausible (annual remittance per adult is ~$2–5k). Almost certainly a total-vs-per-adult or unit error. The prediction ("remittance > federal net") passes only because the number is inflated; the figure needs auditing.
- **I (return-migration cells):** `weighted_adults` is identical (7,686,859) across Mexico/Guatemala/Honduras — a placeholder/stub, not real per-origin weights. Two I-cluster theories are INCONCLUSIVE because of it.
- **L9 (lifetime health NPV):** query returns **empty** — the 65+ Medicaid lifecycle cells aren't built, so the "elderly Medicaid flips the sign" theory can't be tested yet.

## Full scorecard (21 executed)

| Cluster | Theory (short) | Verdict | Evidence |
|---|---|---|---|
| A | Capital-tax adjustment flips sign only for <HS | PASS | NAS <HS −109k/−186k; Clemens <HS +128k |
| A | Education bucket monotone in lifetime NPV | PASS | NAS: <HS −109k < HS +49k < some-college +205k (within baseline) |
| A | Indirect annual incidence doesn't rescue <HS | PASS | Colas-Sachs +$750/yr can't offset −$109k direct |
| F | High-skill NPV not inheriting Mexico <HS scalar | PASS* | education-differentiated; *channel tag (H-1B vs family) absent |
| F | Innovation spillover load-bearing for + high-skill NPV | **FAIL** | positive college+ NPV robust without spillover tag |
| I | Origin fiscal heterogeneity persists at y10+ | PASS | India 6217→3108, Mexico 1519→760; spread 50% of entry (>20% floor) |
| I | Cross-sectional slope ≈ lifetime path | INCONCLUSIVE | weighted_adults stubbed identical |
| I | Return migration fiscal-neutral | **FAIL** | base 25% exit → −25% person-years |
| L | Lifetime 75yr health NPV flips sign (elderly Medicaid) | INCONCLUSIVE | empty result — 65+ cells not built |
| L | SIPP→MEPS bridge zero education variance | INCONCLUSIVE | query semantics ambiguous (cells show >1 value) |
| L | Working-age FB health spend < US-born | PASS | FB $3,607 < native $5,563 |
| M | 3% annuitized NAS <HS ≈ SIPP annual magnitude | PASS* | $3,759 vs $1,519 = 2.47× (same order; *just past strict 2× band) |
| M | Annual federal proxy confirms lifetime NAS sign | **FAIL** | +$1,519 annual vs −$109k lifetime (opposite) |
| M | Remittance outflow dominates federal net (Mexico) | PASS° | $151,636 > $1,519 °(remit figure implausible — flag) |
| N | County median per-pupil in NCES band | PASS | $19,385 ∈ [12k, 25k] |
| N | K-12 local cost material vs federal annual | PASS | $20,907 × 0.97 ≈ $20k ≫ $1,519 federal |
| N | Per-pupil unit-bug fix propagated | PASS | $20,907 > $15k (no longer ~$21) |
| O | ITEP tax floor > Mexico federal proxy | PASS | $96.7B > $664M |
| P | Receiver-city episodic spend > Mexico federal proxy | PASS | $3.84B > $664M |
| T | Falling mean-education with rising total output (additive) | PASS | total earnings 1.61T(1980)→8.01T(2010), monotone up |
| V | Crime channel runs pro-immigrant, doesn't erode | PASS | undoc < native every year 2012–18, no trend to parity |

\* PASS with a noted caveat. ° PASS only because of a suspect input number.

## Unrunnable (11) — the harness-rot list

Genuinely broken `duckdb_test`s (beyond the schema-alias drift already auto-fixed): **A** (more npv tables missing — `acs_foreign_born_education_bucket`, `origin_education_composition`), **E** housing (all 4 — missing `saiz_msa_rent_immigrant_2022`, missing `education_bucket` col, malformed VALUES list), **K** incidence (syntax `..`, missing `cost`/`avg_rpp_all_items_2023` cols), **T** (1 — prose "compare border…" placed in the SQL field).

## Update (2026-06-25, later) — harness REPAIRED

Acted on recommendation #1 below. Fixed the source `duckdb_test`s (alias drift at source + the 11 broken), rebuilt, re-ran: **27 of 27 runnable theories now execute, 0 errors** (was 21 ran / 11 errored). Breakdown of the repair:
- **6 FIXABLE repaired** (clusters A, K) — renamed/never-built object references corrected to real warehouse tables; all 6 now run. Scores: **A#2** annual-proxy↔NPV-rank PASS (proxy rank tracks NPV rank across buckets); **A#5** no-single-origin-scalar PASS (composition varies by origin); **K#1** receiver-city episodic $11.86B PASS. **Re-spec needed (runs but doesn't adjudicate its claim):** **A#4** (no recent-arrival table exists — tests stock-weighted NPV instead), **K#0** (CORR = 1.0 is a *provenance tautology* — the county per-pupil series is derived from the same NCES source it's correlated against), **K#2** (lists RPP by state but doesn't test the border-vs-gateway differential). Lesson: making a test *execute* ≠ making it *adjudicate* — three theories need re-specification, not just repair.
- **4 E-cluster → PENDING-DATA** — genuinely unbuilt (exhaustive schema check: no `msa_match_key`/`rent_burden`/`foreign_born_share`/`saiz_msa_rent_immigrant_2022`; no PUMA→MSA crosswalk). Marked as documented pending-data, not faked.
- **1 T-cluster → NOT-WAREHOUSE-TESTABLE** — the place-premium term is the migrant's own welfare, external to this fiscal warehouse; prose moved out of the SQL field.
- **Remittance unit bug FIXED** (M): the test hardcoded `$66.24B / 436,819` — Mexico's *total worldwide* remittances over a narrow 437K subsample. Denominator corrected to the ~8.52M Mexican-born adult base → **$7,774/adult** (was $151,636). Residual caveat: the numerator is still total-worldwide, not US-origin (~95%), so $7,774 is a slight over-estimate; direction (remittance ≈5× federal-net) holds. **Adjacent flag (forensic audit):** `origin_fiscal_scenario_2023` mixes total and per-adult columns — `avg_medicaid_total_computable` ≈ $109B for Mexico looks like another total-mislabeled-as-average; other theories reading that table may have sibling unit bugs. Needs a column-level audit (not done here).

## Recommendation (concrete follow-up)

1. **Fix the source `duckdb_test`s** in the cluster `.mining` JSONs: apply the `ctx.→context.`/`life.→lifetime.` alias correction at the source (so they run without the runner-side patch), and repair the 11 broken ones (or delete the prose-in-SQL one). Then a single re-run scores the full 32.
2. **Act on the 3 FAILs:** (M13) keep the annual-vs-lifetime sign divergence as an explicit ledger-map caveat — it's now empirically shown; (I8) add a return-migration exit-rate adjustment to the <HS person-year stock; (F5) either condition high-skill NPV on the innovation tag or downgrade the confidence that the positive sign is mechanism-explained.
3. **Audit the remittance unit bug** ($151k/adult).

## Revisions

**2026-06-25 (later) — the 3 re-spec items + the avg_medicaid flag resolved.**
- **A#4 → PENDING-DATA.** No recent-arrival-by-education aggregate exists, so the test could only compute STOCK-weighted NPV and cannot adjudicate "recent > stock." Marked PENDING-DATA in `cluster-a-npv.json` (needs a YRIMMIG≤5yr education-share table from IPUMS/ACS).
- **K#0 → NOT-TESTABLE.** Confirmed the provenance tautology — both `current_spend_per_pupil` series derive from the same NCES F-33 source, so CORR≈1.0 validates nothing. Marked NOT-TESTABLE (a real validation needs two independent products, e.g. Census F-33 vs NCES CCD).
- **K#2 → now ADJUDICATES.** Replaced the bare top-10 RPP listing with a real border(TX/AZ/NM)-vs-gateway(NY/NJ/MA/IL) test. Result: **destination spread 24.6% (>15% → SUPPORTED, the state cost dimension is real); clean border-vs-gateway split only ~10% (modest — CA is a high-cost border outlier).** So the state RPP dimension matters, but not as a clean border/gateway dichotomy.
- **The "Adjacent flag" (above) is RESOLVED.** The forensic data-integrity gate audited `origin_fiscal_scenario_2023`: `avg_medicaid_total_computable` (~$299B) was NOT a unit bug — it's a correct mean of state Medicaid TOTALS (a "which states does this origin concentrate in" context signal), just misleadingly named. Renamed → `mean_state_medicaid_total_usd`; gate now ✓ no flags.

</details>
