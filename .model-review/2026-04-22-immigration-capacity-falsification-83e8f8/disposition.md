# Review Findings — 2026-04-22

**20 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[CRITICAL]** "Pre-trend" placebo uses a post-treatment, endogenous permit denominator
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review states that `analyze_capacity_falsification.py` defines the stress object with `permit_units_2021_2024` and then regresses `wage_log_change_2021_2022` on it. This creates reverse-causality risk: a 2021–2022 local economic shock can reduce 2023–2024 permitting, shrinking the denominator and mechanically raising `recent_fb_per_permit_unit`. The reviewer argues this makes the negative placebo result a mathematical artifact rather than evidence of pre-existing structural weakness.
   File: analyze_capacity_falsification.py
   Fix: Refactor `prepare()` to use a strictly pre-shock capacity baseline such as `permit_units_2017_2019 / 3.0`, with no denominator inputs from post-2020 data.

---

2. **[HIGH]** 2021–2022 is mislabeled as a placebo/pre-trend window
   Category: logic | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review argues that the immigration surge began in early-to-mid 2021, so `wage_log_change_2021_2022` is already within an early treatment period, not a valid pre-trend. Therefore a negative coefficient in that window cannot support the memo's claim that high-load counties were already structurally weaker before treatment. The reviewer says a true placebo should use pre-surge windows such as 2018–2019 or 2019–2020.
   File: analyze_capacity_falsification.py
   Fix: Replace the 2021–2022 placebo with genuinely pre-treatment outcome windows, ideally 2018–2019 and 2019–2020, and rerun the same stress-object regressions on those periods.

---

3. **[HIGH]** Invalid placebo/pre-trend semantics
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The code constructs exposure from permit_units_2021_2024 and contemporaneous share, then tests windows like 2021_2022. A true placebo requires exposure fixed before the outcome window. Currently, it only shows high-load places had weaker earlier outcomes, which is a persistence check, not a pre-trend identification.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Use strictly pre-treatment exposures or windows; alternatively, rename sections to 'earlier-window overlap/persistence check'.

---

4. **[HIGH]** Threshold stability metric uses median instead of original estimate
   Category: bug | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The 'share_same_sign' metric measures consistency relative to the median holdout beta rather than the original full-sample or train-selected estimate. This could report high stability even if holdout results contradict the original claim.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Redefine the metric to compare holdout sign against the full-sample or train-selected sign.

---

5. **[HIGH]** Acceleration null is misinterpreted as evidence against an effect
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review points to `wage_acceleration_2023_2024_vs_2021_2022 = df["wage_log_change_2023_2024"] - df["wage_log_change_2021_2022"]` and argues that because the surge was active in both periods, a null acceleration term only shows that deterioration may have remained constant rather than intensified. The reviewer says the memo incorrectly treats this as a reason to narrow the claim.
   File: immigration-reasoning-evolution-2026-04-21.md
   Fix: Revise the interpretation of the acceleration test to note that a null difference-in-differences between two treated periods does not imply no treatment effect; it may reflect a stable negative effect across both intervals.

---

6. **[HIGH]** Causal downgrade in falsification memo is premature because it relies on flawed tests
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says `immigration-capacity-falsification-2026-04-21.md` heavily downgrades causal confidence based on the placebo and acceleration failures, but argues those failures are themselves compromised by the endogenous denominator and concurrent-treatment timing. It recommends treating the downgrade as unverified until corrected pre-trend tests are run.
   File: immigration-capacity-falsification-2026-04-21.md
   Fix: Mark the placebo-based downgrade as `[UNVERIFIED]` or `[BUG]`, pause the current conclusion, and revisit the narrative only after rerunning falsification with a pre-shock denominator and true pre-treatment windows.

---

7. **[HIGH]** Over-claimed 'Real Threshold Family' without null benchmark
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Split-sample threshold search is a model-selection problem. Without repeating the nested search under a null/permuted treatment, it is unknown if the observed concentration around specific quantiles exceeds what random search would produce.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Add a nested permutation test for the full threshold search procedure to verify the 'family' is not a search artifact.

---

8. **[MEDIUM]** Permutation test resolution is too low and reported p-value is falsely precise
   Category: performance | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review notes that `PERMUTATIONS = 300` implies a minimum nonzero permutation p-value of about `1/300 ≈ 0.0033`. Because the script reports `p≈0.0033` after the estimate beat all permutations, the reviewer says the result is at the floor of the test's resolution and should be reported as a bound rather than an exact-looking value.
   File: analyze_capacity_falsification.py
   Fix: Increase permutations to at least 1000 and preferably 2000+, and report the result as `p < 1/N` when the observed statistic exceeds all simulated draws.

---

9. **[MEDIUM]** Silent exclusion of zero-permit counties
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Division by permit units replaces zeros with NaNs, causing the regression to silently drop counties with no permit issuance. This shifts the estimand from 'counties' to 'counties with positive permits' without disclosure.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Disclose sample exclusions and add sensitivity analyses (e.g., using an indicator or capped ratio) to include zero-permit counties.

---

10. **[MEDIUM]** Coarse permutation inference and missing multiplicity adjustment
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   With 300 permutations, the minimum possible p-value is 0.0033, which is a resolution floor. The memo treats this floor as a precise tail probability and fails to account for multiplicity across four primary outcomes.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Increase permutation count to 5,000 and report multiplicity-adjusted results or exact uncertainty bounds for p-values.

---

11. **[MEDIUM]** Lack of uncertainty intervals for split-share and permutation metrics
   Category: missing | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The report provides percentages for split-sample consistency and permutation results without binomial confidence intervals or tail uncertainty bounds.
   File: 
   Fix: Add binomial/Wilson confidence intervals for split-share metrics and permutation p-value bounds.

---

12. **[MEDIUM]** State-level leave-one-out is too weak for geographically clustered shocks
   Category: architecture | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review argues that `leave_one_state_out` does not adequately address spatial autocorrelation because immigration shocks are regionally clustered. Dropping one state may leave the same regional signal intact through neighboring states, especially in corridors like the Southwest or broader Sunbelt.
   File: analyze_capacity_falsification.py
   Fix: Add stronger geographic robustness checks such as leave-one-Census-division-out or leave-one-region-out, and compare results against state-level LOSO.

---

13. **[MEDIUM]** Mislabeling of exploratory findings as causal evidence
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   'Real family' and 'pre-trend' descriptions overstate the evidentiary level provided by the current descriptive analysis.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Label these findings as exploratory or descriptive until more rigorous tests (nested-null, lagged-placebo) are completed.

---

14. **[MEDIUM]** True pre-trend outcome windows are missing from the panel build
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review explicitly recommends adding `wage_log_change_2018_2019` and `employment_log_change_2018_2019` to the parquet build so the exact same stress-object analysis can be run on pre-surge windows. Without those fields, the falsification framework cannot test a genuine pre-trend placebo.
   File: build_county_outcome_panel.py
   Fix: Extend the panel-building pipeline to compute and store pre-2021 outcome changes, including at minimum 2018–2019 and 2019–2020 wage and employment log-change columns.

---

15. **[MEDIUM]** Reasoning-evolution doc lacks artifact provenance
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The timeline and artifact sequence are presented as narrative without commit hashes, revision blocks, or dated cross-links, making it an unverified reconstruction.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Add commit IDs, memo revision links, or explicitly label as narrative inference.

---

16. **[MEDIUM]** Recent foreign-born numerator may blur the treatment window via ACS rolling averages
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review claims `annual_recent_fb_persons` is derived from `recent_fb_annual_share * totpop`, and warns that if `recent_fb_annual_share` comes from ACS 2022/2023 5-year data, it is a rolling average rather than a clean post-surge flow measure. That would introduce temporal leakage and weaken the interpretation of the numerator as a sharp post-2020 shock.
   File: analyze_capacity_falsification.py
   Fix: Audit the construction of `recent_fb_annual_share`; if it uses rolling ACS shares, replace or supplement it with a cleaner post-surge flow proxy and document the measurement window explicitly.

---

17. **[MEDIUM]** Threshold validation likely leaks target information and overstates threshold stability
   Category: logic | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review infers that `threshold_validation` searches for the best `(recent-flow quantile, permit quantile)` pair on a training split and then evaluates on holdout using the same target variable, which would create optimization bias without nested validation. The reviewer specifically flags the reported modal quantiles (`80` and `50`) as vulnerable to noise if threshold selection is not fully separated from evaluation.
   File: analyze_capacity_falsification.py
   Fix: Use nested cross-validation or a fully separated tuning/validation design for threshold discovery, and report uncertainty around selected quantiles rather than treating the modal pair as stable.

---

18. **[LOW]** Missing framing-sensitivity tags on policy claims
   Category: constitutional | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Statements regarding policy relevance are framing-sensitive but not tagged as such per constitutional principles.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Mark policy-significance claims with [FRAMING-SENSITIVE] tags.

---

19. **[LOW]** Missing LLM-bias disclosure
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The memos do not include a required caveat regarding potential LLM instrument bias on a politically charged topic.
   File: 
   Fix: Add a short instrument-bias note in the synthesis sections.

---

20. **[LOW]** Insufficient steel-manning of alternative explanations
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Non-causal explanations such as selection into economically weak counties and omitted regional shocks are not fully addressed or modeled.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Add an explicit rival-model section predicting signatures for these alternative theories.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->

