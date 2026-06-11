## 1. Assessment of Strengths and Weaknesses

### Strengths

*   **Epistemic Integrity and Disconfirmation (Rule 4):** The memos perfectly execute the required "adversarial self-correction" loop. The willingness to explicitly state *"The threshold result no longer supports a generic 'real family across outcomes' claim"* and publicly walk back the earlier causal wage/employment split as *"provisional"* is exemplary. The reasoning-evolution document traces the error correction transparently.
*   **Rigorous Null Validation:** `analyze_capacity_falsification.py` sets a high bar for the structural stress-marker claim. Generating a 1,000-draw within-state permutation test (`RNG = np.random.default_rng(20260421)`) and benchmarking against a `null_search` to prove that the threshold cutoff surface is diffuse rather than stable is exactly what the project's causal standards demand.
*   **QCEW Extraction Scope:** In `build_county_outcome_panel.py`, the filtering logic (`own_code == "0"`, `industry_code == "10"`, `agglvl_code == "70"`, `qtr == "A"`) correctly isolates total covered county-level aggregates without double-counting ownership types or industries.

### Weaknesses & Fatal Bugs

*   **CRITICAL SEMANTIC FAILURE in IRS Migration Data:** In `build_county_outcome_panel.py`, the functions `load_native_inflow()` and `load_native_outflow()` filter the IRS SOI data using `y1_statefips == "97"` and `y2_statefips == "97"`.
    *   In the standard IRS SOI Migration data dictionary, state FIPS `96` is "Total Migration-US", while state FIPS `97` is "Total Migration-Foreign".
    *   By filtering on `97`, the script is extracting **foreign inflows/outflows**, renaming them to `us_inflow_returns_2022_23` and `us_outflow_returns_2022_23`, and using this to calculate `net_us_migration_share_2022_23`.
    *   This completely invalidates the "native mobility" and "native sorting/backlash" claims in the county panel, as it is modeling foreign administrative tax-return migration instead of domestic native sorting.
*   **Endogeneity in the Pretrend Baseline:** The memo relies on the `2018–2019` QCEW log changes as the clean pre-COVID pretrend. However, the falsification script checks this outcome against a permit baseline drawn from `2017–2019` (`extract_pre_surge_permits()`). Measuring a 2018–2019 outcome against a capacity metric that incorporates 2019 data introduces reverse causality (permits issued in 2019 are directly downstream of 2018–2019 local economic growth).
*   **COVID-Era Averaging Blur:** The code calculates `2019-2020` and `2020-2021` log changes using QCEW `qtr == "A"` (annual averages). Annual averages for 2020 blend pre-lockdown (Q1) and lockdown (Q2-Q4) employment crashes. Using this in any threshold search creates massive noise that likely explains why the threshold surface was found to be "diffuse" and unstable.

## 2. What Was Missed

*   **QCEW Privacy Masking Bias:** The `build_county_outcome_panel.py` script drops duplicate/missing FIPS but doesn't explicitly account for BLS privacy suppressions in small rural counties. By ignoring non-disclosed counties (which drop out of the log-change calculations as `pd.NA`), the resulting panel implicitly overweights urban/suburban counties, altering the actual "capacity frontier" dynamics.
*   **The IRS Data Ceiling:** IRS migration data captures tax filers. The memo treats this as a generic proxy for "native mobility." It was missed that low-income natives (who might be most affected by low-skill immigration wage pressures) frequently fall below the filing threshold or don't file immediately upon moving, meaning the instrument structurally undercounts the exact demographic the hypothesis is targeting.
*   **Permit-to-Unit Conversion:** The falsification uses a hardcoded `OCCUPANTS_PER_UNIT = 2.5` to calculate capacity from permits. This assumes single-family zoning metrics. Surging immigrant populations (especially unauthorized or recent arrivals) have vastly different household formation sizes (often 4-6+ per unit in shared housing). The capacity ratio is systematically mis-scaled.

## 3. Better Approaches

| Recommendation | Status | Details / Implementation |
| :--- | :--- | :--- |
| **IRS Migration FIPS Correction** | **Upgrade** | Change the filter in `build_county_outcome_panel.py` from `97` to `96` to correctly capture "Total Migration-US" for native domestic sorting analysis. |
| **Pre-Surge Permit Baseline** | **Disagree** | Using `2017–2019` permits for a `2018–2019` pretrend is endogenous. **Alternative:** Restrict the pre-surge capacity baseline strictly to `2010–2017` to ensure it is temporally strictly antecedent to the `2018` pretrend window. |
| **QCEW Temporal Windows** | **Agree (with refinement)** | Keep the `2018–2019` window, but entirely abandon any log-change window that touches `2020` (`2019-2020`, `2020-2021`) for causal threshold generation. Replace with a `2021-2023` post-COVID recovery baseline vs `2023-2024` surge window. |
| **Threshold Surface Modeling** | **Upgrade** | Stop searching for a single scalar threshold. A "diffuse cutoff surface" indicates heterogeneous treatment effects. Switch to a causal forest or margin-tree approach to see if the threshold stabilizes when conditioned on state-level housing elasticity. |

## 4. What I'd Prioritize Differently

1.  **Fix the IRS FIPS Code (Semantic Blocker):** Immediately correct `y1_statefips == "97"` to `"96"` in `build_county_outcome_panel.py`.
    *   *Verification:* `county_outcome_panel_audit.json` should show median `net_us_migration_persons` magnitudes an order of magnitude larger than current outputs.
2.  **Rerun Native Mobility Null Tests:** Because the previous threshold search for the "native sorting" outcome was run on foreign IRS data (code 97), the poor transfer to the margin was invalid. Rerun the `threshold_null` and `threshold_surface` scripts on the corrected internal migration data.
    *   *Verification:* `share_sign_matches_train` for migration outcomes changes materially in `county_capacity_falsification_summary.json`.
3.  **De-couple the Pretrend Capacity Baseline:** Modify `extract_pre_surge_permits()` to only aggregate up through 2017. Re-evaluate the `2018-2019` pretrend regressions to see if the negative employment pretrend was just a mechanical artifact of 2019 permit endogeneity.
    *   *Verification:* The `test_beta` for the pretrend in `OUT_PRETREND` should decouple from the capacity denominator.
4.  **Quarterly Data Rollout:** Suspend annual causal claims entirely for the COVID overlap years. Put an explicit blocker in the memos that the wage/employment split cannot be finalized until QCEW quarterly data (`qtr IN ("1", "2", "3", "4")`) is used to bridge `Q4 2019` to `Q4 2021`.
    *   *Verification:* `immigration-capacity-falsification-2026-04-21.md` is updated to explicitly note the annual-averaging blur of 2020 as a data artifact rather than a behavioral finding.
5.  **Adjust the Capacity Scalar:** Parameterize `OCCUPANTS_PER_UNIT` or replace it with county-level ACS PUMS average household size.
    *   *Verification:* Code injects an external reference file (e.g., ACS 5-year household size by FIPS) rather than hardcoding `2.5`.

## 5. Constitutional Alignment

*   **Principle 1 (Source Everything / Check the Instrument):** *Violated.* The script blindly relied on IRS state code `97` without checking the primary IRS SOI data dictionary, representing a failure of the "recursive node inspection" strategy. The data didn't mean what the code said it meant.
*   **Principle 4 (Disconfirmation is Mandatory):** *Exceptionally well-served.* The creation of a 1,000-draw permutation null distribution and the subsequent public demotion of the threshold claim in the memos is the exact adversarial self-correction the Constitution demands. Every claim *was* easier to kill than to keep alive.
*   **Principle 6 (Quantify when possible):** *Well-served.* Vague qualifiers were replaced with explicit Wilson intervals, median $t$-statistics, and out-of-sample sign-match percentages in the JSON summary outputs.

## 6. Blind Spots In My Own Analysis

*   **IRS Dictionary Schema Variations:** IRS SOI FIPS codes occasionally shift across dataset vintages. While `96` is standard for "Total Migration-US" and `97` for "Total Migration-Foreign" in recent years, if the specific 2022-2023 release aggregated US and Foreign into `97` due to a one-off schema change, my primary critique is a false alarm. (However, given standard IRS practice, this is highly unlikely).
*   **QCEW Exclusions:** I am assuming the QCEW `own_code == "0"` and `agglvl_code == "70"` captures exactly what is needed. If the falsification strategy actually required isolating *private* sector employment (`own_code == "5"`) to avoid public sector stickiness during the 2020-2021 shock, then validating the "0" code is missing a deeper economic logic error.
*   **Truncated Code Context:** Because the `analyze_capacity_falsification.py` code is truncated, I cannot see the exact implementation of the `threshold_surface` generation. If the diffuse nature of the surface is due to a buggy search space grid (e.g., step-size errors) rather than underlying data variance, I am mistakenly validating the repo's "downgrade" of the causal claim when the real issue is just a parameter tuning bug.