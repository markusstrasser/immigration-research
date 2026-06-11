## 1. Assessment of Strengths and Weaknesses

**Strengths**
*   **Epistemic hygiene in the evolution doc:** `immigration-reasoning-evolution-2026-04-21.md` brilliantly isolates bug-driven corrections (Phase 7: `/critique close` identifying placebo semantic errors) from data-driven updates. This fulfills the "adversarial self-correction" mandate.
*   **Threshold null benchmarking:** The use of within-state permuted recent-flow to generate a null distribution (`thresh_null`) in `analyze_capacity_falsification.py` is a robust way to bound exploratory search. It definitively kills the overclaim that the threshold family generalizes across all outcomes.
*   **Wilson intervals for holdout stability:** Using binomial confidence intervals (`wilson_interval`) for out-of-sample sign matching is a rigorous, mathematically sound way to quantify holdout performance rather than relying on raw point estimates.
*   **Explicit sample accounting:** Outputting `county_capacity_sample_accounting.json` ensures that exclusion criteria (e.g., zero-permit counties) are trackable, directly addressing earlier pipeline opacity.

**Weaknesses / Bugs**
*   **Missing 2018–2020 Window in Panel Builder:** The memo touts "true `2018–2020` QCEW pretrend windows", but `build_county_outcome_panel.py` fails to materialize this window. The `add_log_change()` loop iterates over `(2018, 2019)`, `(2019, 2020)`, `(2020, 2021)`, `(2021, 2022)`, `(2021, 2023)`, `(2023, 2024)`, and `(2021, 2024)`. Unless the downstream `analyze_capacity_falsification.py` script manually sums the `18-19` and `19-20` columns, this is a silent semantic disconnect between the data layer and the memo claims. 
*   **Silent FIPS Drop (IRS vs QCEW):** The panel relies on `fips5` joins across `elect` (threshold), `qcew`, `inflow`, and `outflow`. QCEW uses BLS-modified FIPS codes (e.g., combining certain Virginia independent cities or handling Oglala Lakota county changes), while IRS uses standard Census FIPS. The script executes `how="left"` merges on `elect`, which will silently produce `NaN`s for IRS or QCEW columns in FIPS-modified jurisdictions, skewing county-level aggregates without warning.
*   **Division-by-Zero Handling in Log Changes:** `pd.Series(panel[end_col]).div(panel[base_col]).where(panel[base_col] > 0)` returns `NaN` where `base_col == 0`. This silently drops counties with zero QCEW employment in the base year rather than treating them as a discrete category (entry/exit).

## 2. What Was Missed

*   **IRS vs QCEW Temporal Mismatch:** The script hardcodes IRS internal migration for `2022_23`. IRS 2022-2023 migration data usually reflects tax years 2021-2022 (returns filed in 22/23). Comparing this directly against QCEW post-surge outcomes (2023-2024) risks a temporal misalignment where the "native mobility" proxy actually predates the heaviest wage/employment shock of the 2023-2024 surge.
*   **Spatial Autocorrelation in Permutation Inference:** `analyze_capacity_falsification.py` uses within-state permutations (`np.random.default_rng(20260421)`). While this handles state-level fixed effects, it ignores spatial clustering of immigration loads. A cluster of counties in South Texas will have correlated unobservables. A true spatial permutation or Conley standard errors would yield wider confidence intervals than independent within-state shuffles. The division leave-out mitigates this partially, but the permutation p-values (`p<=0.001`) are likely overconfident.
*   **QCEW Quarter Assumptions:** The script filters `chunk["qtr"] == "A"` (Annual Average). Annual averages smear out intra-year volatility. The 2020 annual average includes pre-COVID Q1, COVID shock Q2/Q3, and recovery Q4. A true pre-surge baseline should probably cut off strictly at 2019 Q4, avoiding the 2020 COVID variance entirely.

## 3. Better Approaches

*   **Disagree** with doing math/aggregation of baseline years downstream of the panel builder.
    *   *Alternative:* Add `(2018, 2020)` explicitly to the tuple list in `build_county_outcome_panel.py` line 144 to guarantee the metric calculated matches the memo's text ("true 2018–2020 QCEW pretrend windows").
*   **Disagree** with left-merging external administrative datasets on raw `fips5` without a diagnostic check.
    *   *Alternative:* Write an explicit FIPS validation helper. 
    ```python
    missing_qcew = elect[~elect["fips5"].isin(qcew_wide["fips5"])]
    if len(missing_qcew) > 0:
        print(f"Warning: {len(missing_qcew)} threshold counties unmatched in QCEW")
    ```
*   **Agree** with splitting out the "wage story" from the "employment story" based on pretrend confounding.
    *   *Refinement:* Explicitly quantify the pretrend correlation in the memo. Instead of "mostly weak", provide the $R^2$ or coefficient of the 2018-2020 load vs employment lag to anchor the "employment pretrends are already negative" claim.
*   **Upgrade** the handling of `us_inflow_persons_2022_23`.
    *   *Better version:* Rename the variables to explicitly reflect the *tax year* of the migration, not just the file vintage, to prevent cognitive drift when interpreting the causal DAG (e.g., `net_us_migration_persons_ty21_22`).

## 4. What I'd Prioritize Differently

1.  **Add `(2018, 2020)` direct log-change calculation** to `build_county_outcome_panel.py`. **Verification:** The parquet file contains `qcew_employment_log_change_2018_2020` and `qcew_wkly_wage_log_change_2018_2020`.
2.  **Add FIPS reconciliation diagnostics** before the parquet export. **Verification:** Script prints the number of counties in the `elect` spine that ended up with `NaN` for QCEW or IRS columns due to join failures.
3.  **Address the 2020 COVID smear in QCEW.** **Verification:** The falsification memo explicitly states whether "2020" means the 2020 annual average (which includes pandemic variance) or if the pretrend baseline is cleanly isolated to 2018–2019. If 2020 annual is used, acknowledge it as a confounder.
4.  **Enforce temporal alignment transparency for IRS data.** **Verification:** Add a warning in the code or memo explicitly stating the lag between the IRS filing years and the QCEW outcome windows.
5.  **Calculate Conley SEs / Spatial permutations** for the falsification pass instead of just state-stratified shuffles. **Verification:** The falsification script incorporates distance-weighted permutations or acknowledges spatial autocorrelation as an unmitigated factor in the summary JSON.

## 5. Constitutional Alignment

*   **Well-served (Principle 1 & 4 - Source everything & Disconfirmation):** The `immigration-reasoning-evolution-2026-04-21.md` memo is a gold standard for Principle 4. It explicitly names previous errors, runs null-threshold validation, and downgrades confidence where warranted. The heavy use of `[SOURCE]` and `[INFERENCE]` tags conforms perfectly to Principle 1.
*   **Well-served (Principle 2 - Steel-man):** By testing monotonic severity and division leave-out, the agent is actively trying to kill its own threshold hypothesis before adopting it.
*   **Violated (Principle 6 - Quantify when possible):** "wage pretrends look mostly weak before 2020" (`immigration-capacity-falsification-2026-04-21.md`). "Mostly weak" is a vague qualifier. The constitution dictates: *Vague qualifiers become numbers. Say which, and ideally say how different.* The memo should cite the exact pretrend coefficients or p-values.
*   **Violated (Implicit Data Transparency):** The silent `NaN` coercion on FIPS left-joins violates the spirit of "Recursive node inspection." If FIPS drops are occurring because of BLS/IRS structural differences, the data is not being accurately passed up the tree.

## 6. Blind Spots In My Own Analysis

*   **Downstream computation:** Because `analyze_capacity_falsification.py` is truncated in the packet, I don't know if the agent constructs the `2018-2020` log change on the fly via `panel["..._2020"] - panel["..._2018"]`. If it does, my critique of the panel builder is an architectural gripe rather than a hard bug.
*   **BPS Parsing:** The `extract_pre_surge_permits` function is truncated. Building Permit Survey data is notoriously difficult to align perfectly with FIPS because of unincorporated county areas vs municipal borders. I cannot verify if the permit divisor is clean.
*   **Model Context Bias:** I am evaluating "wage pretrends" vs "employment pretrends" purely structurally based on the text. I don't have the actual coefficients generated by `analyze_capacity_falsification.py`, so I must trust that the script's statistical outputs genuinely support the "employment is already negative" split.