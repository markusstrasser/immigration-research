## 1. Assessment of Strengths and Weaknesses

**Strengths**
*   **Methodological Breadth:** The implementation of five parallel falsification checks (permutations, placebos, LOSO, split-sample thresholds, and monotonicity) in `analyze_capacity_falsification.py` is structurally superb. It directly answers the constitution's mandate for disconfirmation.
*   **Monotonicity Over Thresholds:** Testing Spearman rank correlation across deciles (`def monotonicity(df)`) is a highly effective way to prove the signal isn't an artifact of binning or a single anomalous cutoff point.
*   **Epistemic Honesty:** The update in `immigration-reasoning-evolution-2026-04-21.md` beautifully tracks the narrowing of causal confidence. Documenting *why* a hypothesis was downgraded prevents future reversions.

**Weaknesses & Fatal Flaws**
*   **Fatal Endogeneity Bug in "Pre-Trend" Placebo:** The script defines the stress object using `permit_units_2021_2024`. It then regresses `wage_log_change_2021_2022` on this stress object. If a county suffers an economic shock in 2021–2022 (low wage growth), developers will pull fewer permits in 2023–2024. This shrinks the denominator of your stress object (`recent_fb_per_permit_unit`), driving the ratio UP. 
    *   *The Mismatch:* The memo concludes "high-load counties were already structurally weaker before the full post-surge period."
    *   *The Reality:* You are predicting 2021–2022 wages using a denominator influenced by 2023–2024 economic conditions. The causal arrow runs backward. The "pre-trend" failure is a mathematical artifact of an endogenous denominator, not proof of structural pre-existing weakness.
*   **Temporal Misclassification:** 2021–2022 is *not* a pre-trend. The immigration surge began in early-to-mid 2021. 2021–2022 is an early treatment window. Finding a negative effect here doesn't mean the county was "already structurally weaker"; it means the treatment was already happening. A true pre-trend placebo must use 2018–2020 data.
*   **Permutation Resolution:** 300 permutations (`PERMUTATIONS = 300`) yields a minimum possible p-value of $1/300 \approx 0.0033$. The script claims `p≈0.0033`, meaning the true estimate beat *all* permutations. You hit the floor of your computational resolution. Claiming an exact p-value here is false precision; the true p-value is $<0.0033$, but you need at least $N=1000$ to claim stability for significant findings.

## 2. What Was Missed

*   **Numerator Endogeneity (Population vs. Flow):** In `analyze_capacity_falsification.py`, `annual_recent_fb_persons` is derived from `recent_fb_annual_share * totpop`. If the recent foreign-born share relies on ACS 2022/2023 5-year data, it is a rolling average, not a clean post-surge flow. You are blurring the temporal boundary of the shock.
*   **Spatial Autocorrelation in LOSO:** `leave_one_state_out` drops one state at a time. This is insufficient for immigration shocks, which are highly clustered regionally (e.g., the Sunbelt or specific border corridors). If an effect is driven by the broader Southwest, dropping Arizona alone won't kill the signal because Texas and New Mexico pick up the slack.
*   **Acceleration Test Mathematical Identity:** `wage_acceleration_2023_2024_vs_2021_2022 = df["wage_log_change_2023_2024"] - df["wage_log_change_2021_2022"]`. Since the surge was active in *both* periods, a null acceleration term simply means the rate of wage deterioration was constant across the surge, not that the surge had no effect. The memo misinterprets this as "the main reason to narrow the claim." 
*   **Split-Sample Leakage in Threshold Validation:** The `threshold_validation` function (inferred from the summary dictionary) seems to be running splits to find the best threshold. If the evaluation on the holdout uses the same target variable that was used to select the `(recent-flow quantile, permit quantile)` pair in the training split, you have optimization bias. The "modal quantiles" found (`80` and `50`) are highly susceptible to noise.

## 3. Better Approaches

| Recommendation | Status | Details |
| :--- | :--- | :--- |
| **Fix denominator endogeneity** | **Upgrade** | Do not use `permit_units_2021_2024` for baseline capacity. Use a pre-shock capacity baseline: `permit_units_2017_2019`. This represents the county's *structural* build capacity before the post-2020 economic shifts, breaking the reverse-causality loop. |
| **Fix temporal placebo windows** | **Disagree** | 2021–2022 is early treatment, not placebo. Fetch QCEW/IRS data for 2018–2019 and 2019–2020. Run the exact same `flow/capacity` stress object against *these* true pre-trend windows. |
| **Re-evaluate causal downgrade** | **Upgrade** | The `immigration-capacity-falsification-2026-04-21.md` memo heavily downgrades causal confidence based on the placebo/acceleration failure. Because the test itself was flawed (endogenous + concurrent), this downgrade might be a false negative. The "Best current formulation" needs to be paused until the pre-trend test is rerun correctly. |
| **Expand Permutations** | **Agree** | Increase `PERMUTATIONS` from 300 to at least 2,000. It costs seconds in Pandas/NumPy. Do not report `p≈0.0033` when you mean $p < 1/N$. |
| **Regional over State Holdouts** | **Upgrade** | Replace `leave_one_state_out` with `leave_one_census_division_out` (or Region). This is a much harder, much truer test of whether the effect generalizes beyond a single geographic cluster. |

## 4. What I'd Prioritize Differently

1.  **Block the Narrative Downgrade (Immediate):** The current repo state commits a severe epistemic error by downgrading a hypothesis using a compromised test. Do not accept `immigration-capacity-falsification-2026-04-21.md` as ground truth. Add a `[UNVERIFIED]` or `[BUG]` tag to the placebo section immediately.
2.  **Refactor `prepare()` for Exogeneity:** 
    *   Change the capacity denominator to `permit_units_2017_2019 / 3.0` (or similar available pre-surge data).
    *   *Testable criteria:* The denominator must contain *zero* data from >2020.
3.  **Implement True Pre-Trends:** 
    *   Add `wage_log_change_2018_2019` and `employment_log_change_2018_2019` to the parquet build.
    *   *Testable criteria:* Rerun the regressions. If *these* are negative and significant, *then* the structural weakness claim in the memo is correct. If they are null, the causal claim holds stronger than the current memo states.
4.  **Fix the Permutation Math:** 
    *   Update `PERMUTATIONS = 2000`. Adjust the p-value calculation to correctly bound at $1/N$ or return exact floats.
5.  **Re-evaluate the Acceleration Logic:** 
    *   Remove the assumption that a null `(23-24) - (21-22)` means the effect is weak. A constant negative treatment effect across a continuous multi-year shock produces exactly this result. Update `immigration-reasoning-evolution-2026-04-21.md` Phase 8 to reflect this.

## 5. Constitutional Alignment

*   **Principle 4 (Disconfirmation is mandatory):** **EXCELLENT.** The creation of a dedicated falsification script with five different adversarial checks is textbook adherence to the generative principle. The agent tried to kill its own darling.
*   **Principle 2 (Steel-man before criticizing):** **WEAK.** In trying to aggressively disconfirm its own finding, the agent steel-manned the *skeptical* case ("it's just a pre-trend") but failed to scrutinize the mechanics of its own falsification test. It accepted a flawed placebo test without checking the causal DAG of the denominator.
*   **Principle 5 (Name the frame):** **WEAK.** The agent completely missed the frame that "permits 2021-2024" is a post-treatment endogenous variable, not a static structural trait.

## 6. Blind Spots In My Own Analysis

*   **Dataset Schema Invisibility:** I cannot see the exact upstream build of `county_outcome_panel.parquet`. If `permit_units_2021_2024` was already instrumented or synthetically projected from pre-2020 data in the upstream DAG (e.g., in `build_county_outcome_panel.py`), then my endogeneity critique is invalid.
*   **The "Recent FB" Definition:** I am assuming `recent_fb_annual_share` derives from ACS >2021. If it relies on a specific vintage or is derived from 1-year vs 5-year ACS files, the temporal leakage might be either slightly better or vastly worse than I'm projecting.
*   **Holdout Threshold Logic:** Because the `permutation_check` and `threshold_validation` functions are truncated in the diff, I am inferring their exact operations from the `build_summary` output. My critique of the split-sample optimization bias assumes standard `sklearn` style `train_test_split` without nested cross-validation.