# Review Findings — 2026-04-22

**18 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Semantically incorrect 'pretrend' naming for lead associations
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The falsification regressors use a 2022-based exposure proxy against 2017–2019 outcomes. This is a lead-association or placebo test of the geographic proxy, not a literal pretrend test of pre-measured treatment, yet it is labeled 'pretrend' in outputs.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json
   Fix: Rename all 'pretrend' objects to 'lead_association' and add 'exposure_reference_year' metadata to schemas.

---

2. **[HIGH]** Employment post-effect fails magnitude check against pre-surge leads
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The absolute value of the post-surge coefficient for employment (|β_2023_2024|=0.00230) is smaller than both clean pre-surge lead coefficients (0.00246 and 0.00299), invalidating claims that the panel isolates a surge-specific effect.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv
   Fix: Remove causal prose regarding employment; introduce effect-size benchmarks comparing lead vs. post magnitudes in memo tables.

---

3. **[HIGH]** `recent_fb_proxy` is an invalid proxy for the 2021–2024 surge
   Category: logic | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review flags `falsification_summary.json` for using `ACS 2022 5-year B05005 entered-2010-or-later stock divided by 12` as `recent_fb_proxy`. The reviewer argues this averages a 12-year accumulation into a pseudo-flow, heavily smoothing the data and structurally obscuring the specific 2021–2024 spike. Their stated consequence is county misranking: places with acute recent increases can look similar to places with steady historic accumulation. The review further says this should have been marked as contested/speculative evidence rather than treated as a direct measure of a recent surge.
   File: falsification_summary.json
   Fix: Replace `B05005 / 12` with a post-2020 flow-aligned measure, such as TRAC/OHSS county-level indicators if available, or a bounded post-2019 stock change proxy (for example ACS 2022 1-year minus ACS 2019 1-year foreign-born stock). If retained temporarily, explicitly label it as a weak construct-validity proxy.

---

4. **[HIGH]** Domestic-vs-foreign newcomer comparison mixes incompatible sources, time windows, and universes
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says `analyze_internal_vs_immigrant_newcomers.py` compares IRS SOI `us_inflow_persons` for 2022–2023 (a 1-year administrative tax-exemption flow) against ACS B07001 `moved_from_abroad_share` from 2022 5-year data (a smoothed survey measure of past-year movers among all individuals). The reviewer calls this a major denominator/universe artifact because a sharp 1-year admin flow is being set against a 5-year smoothed survey estimate with a different target population and timeframe.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Align both measures to the same source and horizon. The review recommends dropping the IRS merge for this head-to-head comparison and using ACS 1-year domestic and foreign migration variables where available, or another matched migration dataset with identical denominators and timing.

---

5. **[HIGH]** Threshold validation mislabeled as holdout stability
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   In threshold validation, margin and employment outcomes use the same training statistics as wage. The 'test_sign_matches_train' field represents cross-outcome transfer from a wage-trained model, not within-outcome holdout stability.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv
   Fix: Rename field to 'test_sign_matches_wage_train' to reflect actual statistical operation.

---

6. **[MEDIUM]** Modal threshold calculated using marginal modes instead of joint mode
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The script computes modal_recent_quantile and modal_permit_quantile separately. This can yield a modal pair that is not the most frequent joint combination in the distribution.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Compute the joint mode of (recent_quantile, permit_quantile) and add concentration metrics like HHI or entropy.

---

7. **[MEDIUM]** QCEW wage-change outcome is nominal and may confound inflation with real wage effects
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review flags the use of nominal QCEW `annual_avg_wkly_wage` in the log-change outcome. It argues that with roughly 15–18% cumulative inflation variation between 2021 and 2024, a reported wage penalty of about 1.5 percentage points could be an artifact of spatial inflation differences rather than a real wage decline. It also notes the memos use language like `slower wage growth` without clearly distinguishing nominal from real magnitudes.
   File: build_county_outcome_panel.py
   Fix: Deflate QCEW weekly wages before computing log changes, using BEA Regional Price Parities or another regional price deflator mapped to county/MSA geography. Re-run the falsification and outcome analyses on the real-wage series and label nominal results as such.

---

8. **[MEDIUM]** Semantic regression in migration-series labels
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Despite downgrading IRS 97/000 interpretation, comparison scripts still label ACS 'Moved from abroad' as 'FB-inflow' (foreign-born), which incorrectly excludes native-born returnees and reintroduces semantic error.
   File: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py
   Fix: Implement a semantic quarantine via grep/lint tests to ban 'FB-inflow' labels for non-FB variables.

---

9. **[MEDIUM]** Narrative overreach regarding 'causal amplifier' vs 'stress marker'
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Memo text claims capacity likely operates as a 'real amplifier of local strain', which goes beyond the descriptive stress markers identified, as annual causal channel tests remain unresolved.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Downgrade language to 'descriptive stress marker' and separate descriptive vs. causal headings in memo claims.

---

10. **[MEDIUM]** QCEW nondisclosure audit lacks analysis-sample intersection evidence
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The audit shows non-disclosure rows in raw data but zero missing cells in the analysis panel. While plausible if suppressed rows are outside the 2,390-county sample, it is not currently verifiable from the JSON logs.
   File: sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json
   Fix: Add fields for 'suppressed_rows_in_analysis_sample_by_year' and 'suppressed_window_endpoints'.

---

11. **[MEDIUM]** Lack of hard narrative gate for causal prose
   Category: architecture | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The system lacks an enforceable rule to prevent causal synthesis when basic clean-window lead tests fail (as seen in the employment data).
   File: 
   Fix: Adopt rule: No causal wage/employment wording allowed unless lead coefficients are |lead| < 0.5 * |post|.

---

12. **[MEDIUM]** IRS migration data likely undercounts low-income and undocumented movers, biasing the domestic/foreign ratio
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that IRS SOI tracks tax exemptions rather than all movers. It specifically warns that undocumented immigrants and some lowest-income cohorts often do not file, so comparing IRS-based domestic moves to ACS-based foreign moves does not represent comparable universes. The stated consequence is downward bias in the `us_inflow / fb_inflow` ratio, making domestic mobility appear smaller relative to foreign mobility than it really is.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Do not interpret the IRS-derived count as a full-population domestic inflow. Either switch to a common survey-based migration universe for both sides or clearly bound the result as tax-filer migration only and avoid ratio comparisons to ACS all-person foreign-move measures.

---

13. **[MEDIUM]** `us_inflow_share` overstates what IRS code 97 measures
   Category: logic | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review says `y1_statefips == "97"` in IRS SOI is `Total Migration-US`, which includes foreign-born residents already in the U.S. moving between counties. It argues that the variable name `us_inflow_share` implies a clean domestic/native split that does not exist, creating downstream risk that consumers of the parquet output will misread it as a native-incumbent-only measure.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Rename the variable and document it explicitly as a `Total Migration-US` inflow measure rather than a native-only or incumbent-only measure. Add metadata warnings anywhere the field is exported.

---

14. **[MEDIUM]** Permutation test is under-specified and may violate exchangeability or ignore spatial structure
   Category: logic | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review says `analyze_capacity_falsification.py` reports `spearman_rho` but does not make clear which statistic the permutation procedure optimizes, such as absolute t-statistic versus beta magnitude. It further warns that if values are permuted within state but then evaluated with a national OLS, the exchangeability assumption may be violated. The reviewer also recommends adding a spatial component so the null does not simply reflect regional clustering.
   File: analyze_capacity_falsification.py
   Fix: Document the exact permutation target statistic in outputs and ensure the permutation scheme matches the estimation design. If state-block permutations are used, justify exchangeability explicitly; otherwise use a spatially aware or cluster-consistent null, potentially including a spatial-lag or region-preserving permutation design.

---

15. **[MEDIUM]** QCEW suppression-induced attrition is not audited for treatment correlation
   Category: missing | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review says `build_county_outcome_panel.py` correctly masks `disclosure_code == 'N'` in base/end years, but if a county is disclosed in one year and suppressed in the next, the log change becomes `NaN`. The reviewer argues the code does not test whether this missingness is correlated with treatment intensity, creating possible attrition bias if affected small counties drop out disproportionately. The review later notes the observed nondisclosure counts may be small, so the concern remains plausible but not strongly evidenced.
   File: build_county_outcome_panel.py
   Fix: Add an audit diagnostic for counties that transition from disclosed to suppressed within each analysis window, including counts such as `newly_suppressed_count` and treatment-rate comparisons between retained and dropped counties.

---

16. **[LOW]** Research memos lack machine-readable status metadata for superseded/falsified artifacts
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review recommends adding YAML frontmatter such as `status: active|superseded|falsified` to `research/*.md`. The stated problem is that prose supersession notes are harder for automated retrieval or RAG pipelines to exclude, increasing the chance that outdated memos contaminate later reasoning.
   File: research/*.md
   Fix: Add standardized YAML frontmatter to all research markdown artifacts and update any retrieval/indexing logic to filter out `superseded` and `falsified` documents automatically.

---

17. **[LOW]** Missing finite-sample permutation reporting
   Category: architecture | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Current inference reporting does not include the exact finite-sample formula or minimum detectable p-values for the permutation tests.
   File: 
   Fix: Report permutation results as (b+1)/(B+1) with confidence intervals.

---

18. **[LOW]** Lack of source-transparency in threshold metadata
   Category: constitutional | Confidence: 0.7 | Source: GPT-5.4 (quantitative/formal)
   In accordance with Principle 1, threshold semantics are not currently source-transparent within the summary output labels.
   File: 
   Fix: Embed schema/column definitions directly into the summary JSON outputs.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->

