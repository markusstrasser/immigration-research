## 1. Assessment of Strengths and Weaknesses

**Strengths:**
*   **Exceptional Disconfirmation Execution:** The downgrade of the employment-capacity claim based on `county_capacity_pretrend_results.csv` perfectly implements the constitutional mandate. The script found a negative pre-surge trend (`t = -4.80`, `p = 1.55e-06`) for employment in the clean `2018–2019` window. Instead of burying this, the memo correctly splits the causal certainty, categorizing the employment story as "more suspicious" while retaining the wage story.
*   **Window Metadata Rigor:** `build_county_outcome_panel.py` hardcodes epistemic bounds directly into the data generation pipeline via `QCEW_WINDOWS`. Explicitly labeling `2019–2020` and `2020–2021` as `contaminated: True` programmatically prevents future overlapping-window / COVID-anomaly regressions. 
*   **Threshold Null-Benchmarking:** `analyze_capacity_falsification.py` tests holdout sign stability against a permuted null (`thresh_null`). The `county_capacity_threshold_validation.csv` output clearly proves the cutoff surface is highly unstable (quantiles bounce between 60–85 for load and 25–50 for permits), which strictly limits overclaiming. The memos correctly adjust to "wage-search performance that beats a null search... [but] diffuse cutoff surface."
*   **Semantic Quarantine:** `analyze_internal_vs_immigrant_newcomers.py` correctly notes that IRS SOI code 97 (`Total Migration-US`) includes foreign-born residents who move domestically. The memos rigorously respect this, refusing to label it a "native-incumbent-only" result.

**Weaknesses & Bugs:**
*   **Implicit Nondisclosure Coercion (`build_county_outcome_panel.py`):** QCEW suppresses data for privacy (`disclosure_code == "N"`). The audit log catches 2 nondisclosures in 2018 and 2 in 2023. The script calculates log changes via `pd.to_numeric(ratio, errors="coerce")`, assuming string `"N"` cells will gracefully become `NaN`. While functionally surviving here because pandas coerces standard string garbage to NaN, silently relying on coercion for missing-data imputation is fragile.
*   **Naive Stock-to-Flow Proxy (`analyze_internal_vs_immigrant_newcomers.py`):** The script divides ACS B05005 (entered 2010 or later) by 12 to create `recent_fb_annual_avg`. A 12-year stock aggregate suffers heavy attrition from mortality and emigration. Dividing by 12 systematically underestimates historic annualized flow rates compared to the IRS 1-year inflow metric, artificially inflating the "domestic migration is 33x larger" ratio.
*   **Nominal Wage Comparisons vs. Regional Inflation:** The QCEW `annual_avg_wkly_wage` is a nominal metric. The primary independent variable (`low_permit`) is a proxy for housing inelasticity. Highly inelastic counties suffer higher local inflation (especially rent). By comparing nominal wage growth across capacity quantiles, the analysis likely *understates* the real-wage penalty in low-capacity counties because nominal wages inflate to chase local costs.

## 2. What Was Missed

*   **Pre-Trend Thinness:** The fallback to `2018–2019` provides exactly one clean delta window. A single pre-period difference cannot verify a "trend" (parallel trends require assessing the *slope* of differences). If 2019 had a localized economic shock (e.g., the 2019 manufacturing mini-recession), the `t = -4.80` employment failure might be anomalous. The script should pull `2017-2018` QCEW to check structural pretrend stability.
*   **Denominator Mismatch in Newcomer Ratio:** `analyze_internal_vs_immigrant_newcomers.py` drops counties with `<10k` population. However, immigrants and domestic migrants cluster in entirely different county densities. By filtering on the destination denominator, you bias the median inflow ratio. 
*   **Cross-Lagged Permitting:** The `2017-2019` permit baseline is used as the capacity instrument for the `2021-2024` shock. However, permits issued in 2019 convert to completions in 2020-2021. The script assumes static capacity throughput, but the 2021-2022 interest rate environment functionally destroyed the permit-to-completion pipeline. "Permits" shifted from being a proxy for "housing added" to a proxy for "zoning permissiveness" during the surge window.

## 3. Better Approaches

| Subsystem | Recommendation | Action | Rationale / Alternative |
| :--- | :--- | :--- | :--- |
| **QCEW Nondisclosures** | Explicit suppression handling | **Agree (Refinement)** | Mask `annual_avg_emplvl` and `annual_avg_wkly_wage` to `pd.NA` where `disclosure_code == "N"` *before* executing the log-change math. |
| **Pretrend Falsification** | Multi-period pre-trend | **Upgrade** | Add `2017–2018` delta to `QCEW_WINDOWS`. If employment `2017-2018` is flat, the `2018-2019` drop is noise. If both are negative, the region was structurally dying pre-surge. |
| **Foreign-Born Flow Proxy** | Use 1-yr mobility data | **Upgrade** | Instead of `B05005 / 12`, query ACS 1-yr or 5-yr table `B07001` (Geographical Mobility in the Past Year: Moved from abroad). This is a true annual flow metric and safely anchors against the IRS 1-year internal flow metric. |
| **Real vs. Nominal Wages** | BEA Regional Deflators | **Disagree (with alternative)** | Implementing BEA RPPs at the county level is complex and error-prone. Instead, simply note `[INFERENCE]` in the memo: "Because low-permit counties have higher housing inflation, the nominal wage penalty calculated (-1.49 pp) likely underestimates the true real-wage loss." |

## 4. What I'd Prioritize Differently

1.  **Refactor the FB Flow Proxy (High Impact, Low Effort):** Replace `B05005_002E / 12` with `B07001` (Moved from abroad) in `analyze_internal_vs_immigrant_newcomers.py`. Dividing a surviving 12-year stock by 12 invalidates direct ratio comparisons with 1-year gross IRS flows. *Verification:* The stylized fact ratio ("33x") will shrink, producing a more epistemically defensible baseline.
2.  **Add 2017–2018 QCEW Window (High Impact, Medium Effort):** To finalize the wage-vs-employment causal split, you need two pre-surge deltas. Modify `build_county_outcome_panel.py` to fetch 2017. *Verification:* `county_capacity_pretrend_results.csv` outputs a `2017-2018` beta.
3.  **Explicit Nondisclosure Nulling (Medium Impact, Low Effort):** Add `qcew.loc[qcew["disclosure_code"] == "N", ["annual_avg_emplvl", "annual_avg_wkly_wage"]] = pd.NA`. *Verification:* Audit log confirms coercion warnings are eliminated.
4.  **Acknowledge Nominal Wage Inflation Bias (Medium Impact, Zero Effort):** Update `immigration-county-outcome-panel-2026-04-21.md` to state that the `-1.49 pp` wage penalty is a *nominal* penalty, making it a lower bound for the real penalty due to localized shelter inflation in low-capacity zones. *Verification:* A new bullet in the "What remains uncertain" section.
5.  **Correlate IRS Outflow with Rent Burden (Low Impact, Low Effort):** The code tests IRS net migration. Test gross outflow against `high_rent_burden`. Net migration conflates native flight with repelled potential arrivals. *Verification:* `county_outcome_lever_comparison.csv` shows an outflow-specific beta.

## 5. Constitutional Alignment

*   **Principle 4 (Disconfirmation is mandatory):** *Flawlessly executed.* The agent built a permutation test, ran a pretrend placebo check, identified a failure in the employment branch, and actively demoted its own prior claim. The evolution memo specifically chronicles this self-correction.
*   **Generative Principle (Maximize convergence toward ground truth):** *Strongly upheld.* The threshold claim was aggressively narrowed from a "real threshold family" to a "diffuse wage-search surface" based on holdout degradation.
*   **Principle 1 (Source everything):** *Maintained.* Memos effectively segregate `[DATA]` assertions, `[INFERENCE]` jumps, and `[SOURCE: ...]` pathing.
*   **Principle 5 (Name the frame):** *Maintained.* The IRS migration layer is rigorously constrained from being framed as native-incumbent-flight.
*   **Principle 7 (Flag the instrument's bias):** *Maintained.* Both memos lead with the `[SOURCE: notes/llm-bias-caveat.md]` instrument note.

## 6. Blind Spots In My Own Analysis

*   **Hidden DAG Endogeneity:** I am evaluating the econometrics of the QCEW/Permit OLS (`high_recent_fb × low_permit`) without seeing the complete state-level controls. If state-level fixed effects aren't aggressively capturing tech/post-COVID remote work booms, the "high wage, high permit" correlation might be entirely driven by Texas/Florida pandemic migration dynamics rather than structural housing elasticity.
*   **Missing Analysis Scripts:** `analyze_county_outcome_panel.py` is listed in git status but was omitted from the context packet. I am trusting that the interactions summarized in `immigration-county-outcome-panel-2026-04-21.md` accurately reflect HC3 OLS regressions present in that script.
*   **Permit-to-Unit Conversion:** The summary JSON notes "no persons-per-unit housing conversion is used." I am accepting this as an index baseline, but comparing absolute foreign-born counts directly to permit counts (which vary in single vs. multi-family occupancy) could distort the capacity rankings in highly urbanized counties (e.g., NY/SF) compared to exurbs.