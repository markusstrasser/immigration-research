**Verdict:** The adverse Mexican-origin fiscal gaps survive within-state standardization — matched on state group as well as age they get substantially *larger* (union vs third-plus NH white: −$290.6bn → −$411.8bn under `all_age_shared`), and erasing the union's age-matched gap would require overstating modeled employee taxes plus employer payroll for every Mexican-origin record by about 100% versus the white reference (85% versus all natives).

Model: claude-opus-5[1m]

[SOURCE: own computation on held CPS ASEC 2025 (income year 2024) + MEPS HC-256, reusing `infra/immigration-fiscal/all_age_ledger_2026_09_17/{analyze,estimator}.py` unmodified]
[INFERENCE] for every interpretive statement about what the shifts mean.

---

## Test 1 — within-state matched gaps

Joint cells are state group × 8 age bands (32 cells). State groups: `CA` (FIPS 6), `TX` (48), `SW_IL` (4, 8, 17, 32, 35), `rest`. Estimator, weights, donor model, coefficients and reporting domain are identical to the source lane; only the cell definition changes.

### Age-matched gap totals, 8 bands vs 32 cells ($bn, 32-cell SE in parentheses)

| Scenario | Target | vs third-plus NH white (8) | vs white (32) | vs all natives (8) | vs all natives (32) |
|---|---|---|---|---|---|
| all_age_shared | Mexico-born | −103.10 | −141.11 (9.10) | −85.16 | −103.60 (7.13) |
| all_age_shared | Second gen | −113.72 | −157.74 (8.07) | −84.28 | −98.86 (4.54) |
| all_age_shared | Third-plus self-ID | −73.77 | −112.96 (7.00) | −45.56 | −56.91 (4.46) |
| all_age_shared | **Union** | **−290.59** | **−411.81 (19.19)** | **−215.00** | **−259.36 (11.06)** |
| personal_sources | Mexico-born | −136.44 | −177.49 (10.11) | −115.47 | −136.41 (7.83) |
| personal_sources | Second gen | −60.29 | −89.71 (5.94) | −45.87 | −59.67 (3.87) |
| personal_sources | Third-plus self-ID | −43.28 | −65.89 (4.79) | −29.28 | −39.56 (3.62) |
| personal_sources | **Union** | **−240.01** | **−333.08 (16.17)** | **−190.63** | **−235.64 (10.14)** |

Matching within state makes every matched gap 20–55% more adverse. The mechanism is compositional: Mexican-origin people are concentrated in CA and TX, where the same-state white/native benchmark has a higher net balance than the national one, so the within-state counterfactual is more demanding. [INFERENCE]

### Common-age per-person gaps, stored 8-band standard vs 32-cell state×age standard ($ per standardized person, 95% intervals)

The 32-cell standard uses the white reference's joint state×age full-weight shares, so it reweights *geographically* toward where whites live as well as by age. It is a different standard population from the 8-band one, not a refinement of it.

| Scenario | Target | Reference | 8-band | 32-cell | Change | Direction |
|---|---|---|---|---|---|---|
| all_age_shared | Mexico-born | white | −6,562 [−7,545, −5,579] | −5,664 [−6,871, −4,457] | +898 | narrows |
| all_age_shared | Second gen | white | −5,943 [−6,867, −5,020] | −6,772 [−7,940, −5,604] | −829 | widens |
| all_age_shared | Third-plus | white | −4,622 [−5,349, −3,896] | −5,211 [−6,686, −3,735] | −588 | widens |
| all_age_shared | **Union** | white | −5,795 [−6,421, −5,170] | −5,830 [−6,634, −5,025] | −34 | ~unchanged |
| all_age_shared | Mexico-born | all natives | −5,056 [−5,997, −4,115] | −3,997 [−5,176, −2,818] | +1,059 | narrows |
| all_age_shared | Second gen | all natives | −4,437 [−5,313, −3,562] | −5,105 [−6,259, −3,951] | −668 | widens |
| all_age_shared | Third-plus | all natives | −3,116 [−3,816, −2,417] | −3,544 [−5,032, −2,056] | −427 | widens |
| all_age_shared | **Union** | all natives | −4,289 [−4,851, −3,728] | −4,163 [−4,944, −3,381] | +127 | ~unchanged |
| personal_sources | Mexico-born | white | −6,888 [−7,904, −5,872] | −5,814 [−7,114, −4,514] | +1,074 | narrows |
| personal_sources | Second gen | white | −5,278 [−6,561, −3,994] | −6,791 [−8,036, −5,546] | −1,514 | widens |
| personal_sources | Third-plus | white | −4,571 [−5,414, −3,728] | −4,896 [−6,493, −3,299] | −325 | widens |
| personal_sources | **Union** | white | −5,892 [−6,548, −5,236] | −5,928 [−6,766, −5,091] | −37 | ~unchanged |
| personal_sources | Mexico-born | all natives | −5,650 [−6,630, −4,670] | −4,427 [−5,698, −3,156] | +1,223 | narrows |
| personal_sources | Second gen | all natives | −4,040 [−5,279, −2,800] | −5,404 [−6,627, −4,181] | −1,365 | widens |
| personal_sources | Third-plus | all natives | −3,333 [−4,149, −2,517] | −3,509 [−5,113, −1,905] | −176 | widens |
| personal_sources | **Union** | all natives | −4,654 [−5,251, −4,057] | −4,542 [−5,345, −3,738] | +112 | ~unchanged |

Plainly: under the joint state×age standard the first-generation gap **narrows** by $0.9k–$1.2k per person, the second- and third-plus-generation gaps **widen** by $0.2k–$1.5k, and the union is essentially unchanged (|Δ| ≤ $127). Every 95% interval remains strictly adverse in both standards. The apparent first-to-third-plus improvement in the stored 8-band figures shrinks or reverses under the joint standard: under `all_age_shared` vs white it falls from +$1,939 to +$453 per standardized person, and under `personal_sources` vs white from +$2,317 to +$918. [INFERENCE] Standard errors rise by 15–100% because the 32-cell reference schedule is estimated in thinner cells.

### CA-only and TX-only common-age per-person gaps (own-state white age shares)

| Scenario | State | Target | vs white | vs all natives |
|---|---|---|---|---|
| all_age_shared | CA | Mexico-born | −14,101 [−16,198, −12,004] | −9,187 [−10,722, −7,652] |
| all_age_shared | CA | Second gen | −11,486 [−13,976, −8,996] | −6,572 [−8,479, −4,665] |
| all_age_shared | CA | Third-plus | −10,798 [−12,944, −8,652] | −5,884 [−7,459, −4,309] |
| all_age_shared | CA | **Union** | **−12,133 [−14,068, −10,198]** | **−7,219 [−8,406, −6,032]** |
| all_age_shared | TX | Mexico-born | −8,226 [−10,153, −6,299] | −5,271 [−6,812, −3,731] |
| all_age_shared | TX | Second gen | −7,912 [−10,384, −5,441] | −4,958 [−6,850, −3,067] |
| all_age_shared | TX | Third-plus | −6,617 [−8,544, −4,689] | −3,662 [−4,926, −2,399] |
| all_age_shared | TX | **Union** | **−7,479 [−9,253, −5,705]** | **−4,525 [−5,606, −3,443]** |
| personal_sources | CA | **Union** | −12,148 [−14,096, −10,200] | −8,063 [−9,247, −6,880] |
| personal_sources | TX | **Union** | −7,146 [−8,879, −5,412] | −4,895 [−6,065, −3,725] |

Full grid in `derived/state_matched.csv` (144 rows). Within CA every gap is roughly twice the national figure and within TX roughly 25–30% above it; no state restriction produces a non-adverse interval.

### Gates

| Gate | Result |
|---|---|
| 1. Positive population in all 161 weight vectors, every group × 32 cells | PASS. Minimum cell population: Mexico-born 48,091; second gen 15,413; third-plus self-ID 29,734; all natives 1,472,681; white 602,649 |
| 2. Collapse to one state group reproduces stored 8-band results | PASS. Max `gap_total` residual $3.05e−5 (tolerance $1); every `standardized_gap_per_person` residual exactly 0.0 (tolerance $0.001), 20 anchors across both scenarios |
| 3. Self-reference contrast vanishes on 32 cells | PASS. Max |gap| 0.0, max |gradient| 0.0, both scenarios |

Recorded in `derived/audit.json` with input SHA-256 hashes. `derived/state_populations.csv` carries group × state-group record counts, populations and the worst single age-band population, so sparse cells are visible: the thinnest are second gen in `rest` (28,553) and third-plus self-ID in `rest` (38,950).

## Test 2 — earnings/tax measurement sensitivity

Employee taxes (component 0: FICA + FEDTAX_AC + STATETAX_A) and employer payroll (component 3) multiplied by (1+δ) on all 18,331 records in the three target groups. References and every other record untouched. All 161 weight vectors recomputed at each δ; medical donor gradient is unchanged by δ, so MEPS variance carries through unaltered.

### Age-matched `gap_total` ($bn) vs third-plus NH white

| Scenario | Target | δ=0 | 0.05 | 0.10 | 0.20 | 0.30 | 0.50 |
|---|---|---|---|---|---|---|---|
| personal_sources | Mexico-born | −136.44 | −132.18 | −127.93 | −119.41 | −110.90 | −93.87 |
| personal_sources | Second gen | −60.29 | −55.83 | −51.37 | −42.45 | −33.53 | −15.69 |
| personal_sources | Third-plus | −43.28 | −38.63 | −33.97 | −24.67 | −15.37 | +3.24 |
| personal_sources | **Union** | **−240.01** | −226.64 | −213.27 | −186.54 | −159.80 | **−106.33** |
| all_age_shared | **Union** | **−290.59** | −276.15 | −261.70 | −232.81 | −203.93 | **−146.15** |

Vs all natives the union runs −190.63 → −71.26 ($bn) under `personal_sources` and −215.00 → −87.85 under `all_age_shared` across the same δ range. Union SEs move only modestly with δ (e.g. `all_age_shared` vs white: $11.69bn at δ=0 to $13.32bn at δ=0.50), so at every δ tested the gap stays many standard errors from zero.

### Union `absolute_total` ($bn)

| Scenario | δ=0 | 0.05 | 0.10 | 0.20 | 0.30 | 0.50 |
|---|---|---|---|---|---|---|
| personal_sources | 29.40 | 42.76 | 56.13 | 82.87 | 109.61 | 163.08 |
| all_age_shared | 50.24 | 64.68 | 79.13 | 108.01 | 136.90 | 194.68 |

The union's own partial balance is already positive at δ=0 under both scenarios; its break-even δ is negative (−0.110 `personal_sources`, −0.174 `all_age_shared`), i.e. taxes would have to be *overstated* by 11–17% in the current model for the absolute balance to reach zero. The adverse finding is a relative one against the reference populations, not an absolute negative balance.

### Standardized per-person gap vs white ($ per standardized person)

| Scenario | Target | δ=0 | 0.10 | 0.30 | 0.50 |
|---|---|---|---|---|---|
| personal_sources | Mexico-born | −6,888 | −6,362 | −5,310 | −4,257 |
| personal_sources | Second gen | −5,278 | −4,382 | −2,590 | −798 |
| personal_sources | Third-plus | −4,571 | −3,664 | −1,850 | −36 |
| personal_sources | Union | −5,892 | −5,193 | −3,796 | −2,398 |
| all_age_shared | Mexico-born | −6,562 | −6,027 | −4,957 | −3,887 |
| all_age_shared | Second gen | −5,943 | −5,161 | −3,597 | −2,033 |
| all_age_shared | Third-plus | −4,622 | −3,704 | −1,866 | −28 |
| all_age_shared | Union | −5,795 | −5,088 | −3,674 | −2,259 |

### Break-even δ*

| Scenario | Target | Reference | δ* for matched `gap_total` | δ* for standardized per-person |
|---|---|---|---|---|
| all_age_shared | Union | white | **1.006** | 0.819 |
| all_age_shared | Union | all natives | **0.845** | 0.674 |
| all_age_shared | Mexico-born | white | 1.366 | 1.227 |
| all_age_shared | Mexico-born | all natives | 1.291 | 1.090 |
| all_age_shared | Second gen | white | 1.258 | 0.760 |
| all_age_shared | Second gen | all natives | 1.089 | 0.624 |
| all_age_shared | Third-plus | white | 0.600 | 0.503 |
| all_age_shared | Third-plus | all natives | 0.411 | 0.368 |
| personal_sources | Union | white | **0.898** | 0.843 |
| personal_sources | Union | all natives | **0.798** | 0.736 |
| personal_sources | Mexico-born | white | 1.603 | 1.309 |
| personal_sources | Mexico-born | all natives | 1.566 | 1.229 |
| personal_sources | Second gen | white | 0.676 | 0.589 |
| personal_sources | Second gen | all natives | 0.573 | 0.487 |
| personal_sources | Third-plus | white | 0.465 | 0.504 |
| personal_sources | Third-plus | all natives | 0.345 | 0.397 |

Linearity verified: every reported quantity is exactly linear in δ, so δ* = −value(0)/slope is exact. The δ=0.10 and δ=0.20 points lie on the line through δ=0 and δ=0.50 with maximum relative residual **1.02e−14** (tolerance 1e−6), across all 34 series (2 scenarios × 17 target-reference-metric combinations).

**Income tax is convex in earnings.** A δ applied to modeled tax dollars therefore corresponds to a *smaller* proportional error in underlying earnings: the federal income-tax component rises faster than proportionally with wages, so recovering +100% of modeled tax would require substantially less than +100% of unreported wages. The two payroll pieces (FICA below the cap, employer OASDI/HI) are close to proportional in wages, which bounds how far the convexity argument runs. Treat δ* as a bound on the *tax-dollar* error, not on the earnings error. [INFERENCE]

**`all_age_shared` caveat.** Under sharing, unit tax and employer dollars are spread equally over SPM members before the scaling, so multiplying a target record's *allocated* share is a record-level approximation: it does not correspond to scaling the earnings of a specific earner, and in mixed-origin units it scales only the target members' shares. It also breaks the unit-conservation identity that `matrices()` checks at build time. The `personal_sources` arm, where taxes and employer payroll sit on the recorded person, is the interpretable one.

### Context (not group evidence)

| Quantity | Value |
|---|---|
| CPS ASEC 2025 aggregate wage and salary income, Σ WSAL_VAL × full person weight | $12.0724tn |
| BEA wage and salary disbursements 2024, FRED A576RC1, 2024 monthly SAAR average | $12.3879tn |
| CPS / NIPA coverage ratio | 0.9745 |

Fetched 2026-09-17 from `https://fred.stlouisfed.org/graph/fredgraph.csv?id=A576RC1`; all 12 months of 2024 present. This is an aggregate wage-coverage figure for the whole CPS, not a group-specific under-reporting rate, and it does not license transferring a 2.5% shortfall to the Mexican-origin targets. It does indicate that a δ near 1.0 on modeled taxes is far outside the range any aggregate wage-coverage shortfall could support. [INFERENCE]

## Files

Covered (this lane, all under `infra/immigration-fiscal/ledger_stress_2026_09_17/`):

- `common.py` — rebuilds `state`, `groups`, `civilian`, `bands`, `head_weights`, `exposure`, matrices, donor model exactly as `analyze.generate()` does, without running it
- `test1_state_matched.py` → `derived/state_matched.csv` (144 rows), `derived/state_populations.csv`, `derived/audit.json`
- `test2_earnings_scaling.py` → `derived/earnings_scaling.csv` (238 rows), `derived/breakeven.csv`, `derived/audit_test2.json`, `derived/fred_A576RC1.csv`

Read, not modified: `all_age_ledger_2026_09_17/{README.md,analyze.py,estimator.py,mean_weight_probe.py,generation_envelope.py}`, `gen_ledger_extension_2026_09_16/extend_ledger.py`, `all_age_ledger_2026_09_17/derived/estimates.csv`.

Skipped or not attempted: nothing in the brief. `head_weights` is rebuilt and available in `common.setup()` but neither test uses a head-weighted arm, since the brief fixes both tests to person weights. No commits made.

## Scope limits

These are conditional on the source lane's model: modeled rather than observed taxes, MEPS donor medical means, mixed-source state parameters, a partial account omitting corporate tax and pure public goods, and cross-sectional generation groups rather than linked families. The within-state cells sharpen the age/geography comparison; they do not identify a causal effect of immigration, and no result here speaks to marginal fiscal response. Intervals are pointwise normal 95% intervals conditional on fixed standard shares and model parameters, with CPS and MEPS variance added as first-order independent components; they are not simultaneous over the 16 target × reference × scenario combinations reported.

## Parent addition: paired generation contrasts by standard (`test1b_generation_contrasts.py`)

The per-person tables above imply that the stored first-to-third-plus narrowing depends on the standard population. This script computes the paired later-minus-earlier contrasts with replicate covariance under both standards; the 8-band rows reproduce the source lane's `generation_contrasts.csv` exactly (max residual 0.0). Output: `derived/generation_contrasts_by_standard.csv`.

| Scenario | Standard | G2 − G1 | G3+ − G2 | G3+ − G1 |
|---|---|---|---|---|
| all_age_shared | age (8 bands) | +618 [−592, +1,829] | +1,321 [+296, +2,345] | +1,939 [+766, +3,112] |
| all_age_shared | state × age (32 cells) | −1,108 [−2,688, +472] | +1,561 [−334, +3,457] | +453 [−1,446, +2,353] |
| personal_sources | age (8 bands) | +1,610 [+90, +3,131] | +707 [−752, +2,165] | +2,317 [+1,051, +3,582] |
| personal_sources | state × age (32 cells) | −977 [−2,771, +817] | +1,895 [−62, +3,853] | +918 [−1,216, +3,052] |

Dollars per standardized person per year, white reference, pointwise 95% intervals. At a common age and place the first-to-third-plus difference is not distinguishable from zero under either allocation rule. The 8-band narrowing was therefore partly geographic composition: the Mexico-born are concentrated in California, where every group's gap against local whites is largest, so an age-only standard that leaves each group at its own places makes the first generation look worst. Neither standard is uniquely correct; the age-only standard answers "at the places each group lives," the joint standard "at the places the reference lives." The level gaps are adverse under both. [INFERENCE on measured contrasts]

Re-run by the parent 2026-09-17: `test1_state_matched.py` (144 rows, gates 1–3 PASS), `test1b_generation_contrasts.py` (PASS), `test2_earnings_scaling.py` (238 rows, linearity residual 1.02e−14, union δ* 1.006 / 0.845 shared, 0.898 / 0.798 personal).
