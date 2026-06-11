## 1. Assessment of Strengths and Weaknesses

**Strengths (What Holds Up):**
*   **Methodological Self-Correction:** The implementation of `threshold_null` in `analyze_capacity_falsification.py` is a rigorous epistemic check. It successfully proved that even random (null) searches can find "significant" thresholds (Top 3 null shares = `0.30` vs actual = `0.366`), forcing the appropriate downgrade of the "generic threshold" claim in the memos.
*   **Explicit Window Metadata (`build_county_outcome_panel.py`):** The `QCEW_WINDOWS` object explicitly tracks `contaminated` flags, `touches_2020`, and `window_role`. Mapping this directly to `county_outcome_panel_audit.json` prevents silent scope creep where a transition year gets treated as a clean baseline.
*   **Pre-Trend Separation:** The expansion to `clean_pre_covid_early` (2017–2018) and `clean_pre_covid` (2018–2019) successfully broke the prior false confidence. The `county_capacity_pretrend_results.csv` shows wage betas flipping signs (`0.0016` in 17/18, `-0.0007` in 18/19), verifying the memo's conclusion that the annual wage channel is not cleanly identified.
*   **Artifact Provenance:** `immigration-reasoning-evolution-2026-04-21.md` correctly catalogs the specific bugs (e.g., "The first draft... treated 2021–2022 overlap windows as placebo... /critique close flagged that as a real semantics bug") rather than just presenting the final stance.

**Weaknesses (Errors & Methodological Risks):**
*   **Flawed "Surge" Flow Proxy:** `falsification_summary.json` notes the use of `ACS 2022 5-year B05005 entered-2010-or-later stock divided by 12` as the `recent_fb_proxy`. This is a severe methodological weakness. Dividing a 12-year accumulation by 12 heavily smooths the data, obliterating the specific 2021–2024 spike. It structurally misranks counties that experienced acute recent spikes versus steady historic accumulation.
*   **Instrument Mismatch on Newcomers:** `analyze_internal_vs_immigrant_newcomers.py` compares IRS SOI `us_inflow_persons` (2022–2023, 1-year tax exemptions) against ACS B07001 `moved_from_abroad_share` (2022 5-year, moving average of past-year mobility). Comparing a sharp 1-year administrative flow of tax filers to a 5-year smoothed survey estimate of all individuals introduces massive denominator/universe artifacts.
*   **Nominal vs. Real Wages:** The QCEW log change leverages nominal weekly wages (`annual_avg_wkly_wage`). Given the severe inflation variance between 2021 and 2024 (15–18% cumulatively), a nominal wage penalty of `~1.5 pp` (noted in the superseded memo) could be entirely an artifact of spatial inflation differences rather than a real wage reduction.

## 2. What Was Missed

| File / Component | Missed Pattern / Architectural Gap | Consequence |
| :--- | :--- | :--- |
| `analyze_internal_vs_immigrant_newcomers.py` | **IRS Universe Limitation:** IRS tracks tax *exemptions*. Undocumented immigrants and the lowest-income cohorts often do not file taxes. Comparing IRS domestic moves to ACS foreign moves systematically undercounts domestic low-income mobility while capturing all foreign mobility. | Downward bias on the `us_inflow / fb_inflow` ratio; domestic mobility looks smaller relative to foreign mobility than it actually is. |
| `analyze_internal_vs_immigrant_newcomers.py` | **Code 97 Nuance:** IRS SOI `y1_statefips == "97"` is "Total Migration-US". However, this includes *foreign-born residents already in the US* moving to a new county. The memos catch this ("not a native-incumbent-only measure"), but the code variable `us_inflow_share` implies a clean split that doesn't exist. | Potential for downstream users of the parquet file to misinterpret `us_inflow` as "native citizens". |
| `build_county_outcome_panel.py` | **QCEW Nondisclosure Contagion:** The code masks `disclosure_code == 'N'` correctly for the base/end year. But if a county switches from disclosed in 2017 to suppressed in 2018, the log change becomes `NaN`. The code does not verify if data missingness correlates with the treatment (e.g., sudden loss of small businesses). | Attrition bias in the `county_outcome_panel_audit.json` if smaller, highly-affected counties silently drop out of the regressions. |
| `analyze_capacity_falsification.py` | **Permutation Statistic Obfuscation:** The summary JSON lists `"spearman_rho"` for monotonicity, but it is unclear what test statistic the permutation test optimizes (e.g., absolute t-stat, beta coefficient). If it permutes within-state but tests a national OLS, the exchangeability assumption is violated. | Falsification floor (`p<=0.001`) might be artificially strict or loose depending on the spatial autocorrelation of the permuted vector. |

## 3. Better Approaches

| Current Approach | Recommendation | Rationale |
| :--- | :--- | :--- |
| **B05005 / 12 as Flow Proxy** | **DISAGREE** (Alternative: Use TRAC or OHSS). | A 12-year average cannot proxy a 3-year acute surge. Use TRAC immigration court notices-to-appear (NTA) by county, or OHSS credible fear / parole data for a true post-2020 acute stress marker. |
| **Nominal QCEW Wage Logs** | **UPGRADE** (Apply Regional Price Deflator). | Adjust QCEW `annual_avg_wkly_wage` using BEA Regional Price Parities (RPP) at the MSA/non-MSA level before calculating log changes. This prevents conflating local inflation spikes with real wage suppression. |
| **ACS 5-yr vs IRS SOI 1-yr** | **DISAGREE** (Alternative: Use ACS 1-yr exclusively). | For counties >65k, use ACS 1-yr data for both domestic in-migration (B07001_045E or similar) and foreign in-migration. This guarantees identical universes, denominators, and time horizons. |
| **Supersession Notes in Legacy Memos** | **AGREE** (With refinement). | Adding a YAML `status: falsified` or `status: superseded` in the frontmatter allows programmatic exclusion from RAG pipelines, preventing LLM context-window contamination in future tranches. |
| **Threshold Selection via Loop** | **AGREE** (With refinement). | The empirical null-distribution testing is excellent. Refine by adding a spatial-lag term to the null permutation to ensure the threshold isn't just capturing a regional artifact (e.g., all of Texas vs all of Ohio). |

## 4. What I'd Prioritize Differently

1.  **Swap the Surge Flow Proxy (High Impact, High Feasibility):**
    *   *Action:* Replace `B05005 / 12` with a true 2021–2024 flow proxy. If TRAC/OHSS is unavailable, use the delta between ACS 2022 1-year and ACS 2019 1-year total foreign-born stock, rather than a divided 12-year accumulation.
    *   *Verification:* The `recent_fb_proxy` metadata in the summary JSON reflects a metric strictly bound to 2019 or later.
2.  **Align the Migration Universes (High Impact, Medium Feasibility):**
    *   *Action:* In `analyze_internal_vs_immigrant_newcomers.py`, drop the IRS SOI merge entirely if the goal is a direct comparison to foreign inflows. Use ACS county-to-county migration flows or ACS 1-year internal mobility variables to ensure identical denominators.
    *   *Verification:* `us_inflow_share` and `moved_from_abroad_share` share the exact same measurement methodology and timeframe.
3.  **Real Wage Transformation (Medium Impact, High Feasibility):**
    *   *Action:* Download BEA RPP data, map to `fips5`, and deflate QCEW wages before computing `qcew_wkly_wage_log_change_2021_2024`.
    *   *Verification:* `county_outcome_panel_audit.json` includes `real_wage_log_change` fields, and the falsification tests are re-run on real wages.
4.  **Enforce Markdown Frontmatter for Artifact Status (Low Effort, Ongoing Drag Reduction):**
    *   *Action:* Add standard YAML frontmatter to all `research/*.md` files indicating `status: [active | superseded | falsified]`.
    *   *Verification:* An autonomous agent parsing the directory for RAG can cleanly drop `immigration-county-outcome-panel-2026-04-21.md` based on its structured header rather than parsing a prose supersession note.
5.  **Examine QCEW Attrition Bias (Medium Impact, Low Feasibility):**
    *   *Action:* In `build_county_outcome_panel.py`, add a diagnostic to `audit` that flags the count of counties that were disclosed in 2017 but suppressed in 2024.
    *   *Verification:* `qcew_window_metadata` tracks `newly_suppressed_count` to prove that the effect size isn't driven by specific local economies collapsing below disclosure thresholds.

## 5. Constitutional Alignment

*   **Principle 4 (Disconfirmation is mandatory): EXCELLENT.** The creation of a literal "null threshold search" to kill the agent's own prior claim about "clean generic post-surge causal thresholds" is best-in-class adherence to the constitution. The resulting downgrade in the memo is structurally honest.
*   **Generative Principle (Error correction is the mechanism): EXCELLENT.** `immigration-reasoning-evolution-2026-04-21.md` beautifully maps the error correction tree. Every claim was made "easier to kill than to keep alive."
*   **Principle 5 (Name the frame): GOOD.** The memos accurately named the frame on the IRS data ("Total Migration-US aggregate, not a native-incumbent-only measure") and adjusted the code variables accordingly.
*   **Principle 3 (Distinguish levels of evidence): VIOLATED.** The use of `B05005 / 12` is highly speculative proxy methodology masquerading as empirical fact. It passes statistical tests in the code, but the variable itself does not represent the "surge" it claims to represent. It should have been heavily flagged with `[CONTESTED EVIDENCE]` or `[SPECULATION]` regarding its construct validity.
*   **Principle 6 (Quantify when possible): MIXED.** The code quantifies the permutations excellently. However, the memo uses "slower wage growth" without explicitly contextualizing nominal vs. real magnitude, which borders on vague qualification given inflation dynamics.

## 6. Blind Spots In My Own Analysis

*   **Permutation Implementation Specifics:** I only have snippets of `analyze_capacity_falsification.py`. I am assuming the permutation test correctly respects county cluster structures (e.g., state-level blocks) based on the "within-state permutations" note in the memo, but if the code just does a naive `np.random.shuffle()`, the false positive rate is heavily inflated.
*   **ACS 5-Year Data Nuances:** I am penalizing the use of 5-year ACS data for point-in-time "surge" comparisons. However, for smaller counties (<65k population), 1-year ACS data is literally unavailable. If the agent relied on 5-year data to maintain a comprehensive N=2390 county panel, my recommendation to switch to 1-year data would destroy the panel's geographic coverage. The agent's choice might be the least-bad option for a unified county spine.
*   **QCEW Nondisclosure Severity:** I hypothesized attrition bias from QCEW "N" codes. Looking at the `county_outcome_panel_audit.json`, the nondisclosure rows are tiny (e.g., `2017: 1`, `2018: 2`). My concern about mass small-business suppression might be statistically irrelevant at the county aggregate level (as opposed to the industry level, where suppression is rampant).