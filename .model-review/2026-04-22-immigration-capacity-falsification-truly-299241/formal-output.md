## 1. Logical Inconsistencies
Steel-man first: the tranche is materially improved. The final memo now distinguishes descriptive robustness from causal identification, narrows the threshold claim to wage-tuned exploratory performance, and explicitly says the annual wage/employment split is still provisional. That is a real downgrade from the earlier overclaiming posture. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md]

| Issue | Why it is a problem | Severity |
|---|---|---:|
| **A. “2018–2020 pretrend windows” language remains semantically loose** | The index and reasoning-evolution doc still describe the tranche as using “true `2018–2020` QCEW pretrend windows,” while the final memo says windows touching `2020` are COVID-contaminated and should not support the wage/employment split. That is not a code bug, but it is a meaning bug: “includes 2020 windows” is true; “supports causal pretrend inference from 2018–2020 windows” is not. [SOURCE: research/immigration-INDEX.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Medium |
| **B. “Rules out a one-state artifact” appears unsupported by the visible artifact set** | The review scope emphasized **division** leave-out; the visible output file is `county_capacity_geographic_leaveout.csv`; the code excerpt includes a `STATE_TO_DIVISION` map but no visible state-level leave-out output. Unless the CSV actually contains a state loop, the memo’s “not a one-state or one-division artifact” claim is too strong. [SOURCE: .model-review/plan-close-context.md] [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [INFERENCE] | Medium-High |
| **C. “Not a binning accident” is broader than the demonstrated checks** | What I can see supports monotonicity by decile and threshold-search robustness/null benchmarking. That is evidence against one specific discretization artifact, but not against binning dependence in general. To justify “not a binning accident,” I would want invariance across multiple binning schemes or a continuous-specification check. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py] [INFERENCE] | Medium |
| **D. Threshold-language is still under-quantified** | “Beats the null strongly,” “diffuse cutoff surface,” “poor transfer,” and “moderate transfer” are the right *directional* claims, but they are not yet fully constitutional because the memo does not expose the actual margins (e.g., sign-match share difference, median \|t\| difference, top-cell selection share). This is a quantification gap, not a logical reversal. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py] | Medium |
| **E. Sample-accounting audit is not aligned to the actual clean-window claim** | In `build_county_outcome_panel.py`, `qcew_row_missing` is keyed to `annual_avg_emplvl_2021`. But the substantive clean-window claim rests on `2018–2019`, and the script creates many window-specific outcomes. A county missing `2018` or `2019` but present in `2021` would be counted as not-missing in the panel audit, even though it is unusable for the key falsification window. The downstream analysis may still filter correctly, but the top-level audit can silently understate relevant missingness. [SOURCE: sources/immigration-causal/scripts/build_county_outcome_panel.py] | Medium |
| **F. The code still materializes contaminated windows without machine-readable “do not interpret causally” metadata** | Since the final conclusion depends on *not* leaning on `2019–2020`/`2020–2021`, the absence of an explicit contamination flag in outputs creates future semantic regression risk. The memo says the right thing; the artifacts do not enforce it. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: sources/immigration-causal/scripts/build_county_outcome_panel.py] [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py] [INFERENCE] | Medium |

Bottom line: I do **not** see a clear fatal numerical bug in the provided excerpts that makes the tranche categorically uncommittable. I **do** see two meaningful remaining overstatement risks: the unsupported “one-state artifact” language and the still-loose “2018–2020 pretrend” phrasing. [INFERENCE]

## 2. Cost-Benefit Analysis
Ranked by value adjusted for ongoing cost.

| Rank | Proposed change | Expected impact | Maintenance burden | Composability | Risk |
|---|---|---|---|---|---|
| 1 | **Add machine-readable window metadata (`clean_pre_covid`, `covid_contaminated`, `post_surge`) and use it in summaries** | High: prevents future overreading of `2019–2020`/`2020–2021`; directly protects the main corrected conclusion. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Low | High: reusable for every later memo/script | Low |
| 2 | **Either add explicit state leave-out analysis or delete “one-state artifact” language** | High: removes the clearest remaining unsupported causal-robustness claim. [SOURCE: .model-review/plan-close-context.md] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Low if wording-only; Low-Medium if code added | High | Low |
| 3 | **Quantify threshold claims in the memo with exact margins from summary JSON/CSV** | High: upgrades evidence labeling from adjectives to numbers; lowers supervision cost because future readers need not inspect CSVs manually. [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py] | Very low | High | Very low |
| 4 | **Expand audit/sample accounting to per-window usable N and zero-base counts** | Medium-High: catches silent sample drift tied to the actual clean window. [SOURCE: sources/immigration-causal/scripts/build_county_outcome_panel.py] | Low | High | Low |
| 5 | **Add binning-invariance check or narrow the wording from “not a binning accident” to “not driven by the specific threshold search/null benchmark”** | Medium: closes a semantic gap, but less central than the clean-window and state-leaveout issues. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Low | Medium | Low |

Commit guidance: **commit-eligible after wording fixes; stronger after audit/metadata fixes.** [INFERENCE]

## 3. Testable Predictions
Convert each surviving claim into a falsifiable statement.

| Claim in memo | Testable prediction | Success criterion |
|---|---|---|
| “Wage story is somewhat more promising than employment.” [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | In the clean annual window, the wage pretrend coefficient should be closer to 0 than the employment pretrend coefficient, and the post wage result should remain same-sign after controlling for clean pretrend. | `|t_wage_pre_2018_2019| < |t_emp_pre_2018_2019|` and wage post coefficient retains sign with `p < 0.05` or CI excluding 0 after pretrend control. |
| “Employment story is more suspicious.” [SOURCE] | Employment should show a negative clean pretrend in `2018–2019` and weaker post robustness than wage under the same controls. | Clean-window employment coefficient `< 0`; post employment effect loses more magnitude/significance than wage when adding pretrend control. |
| “Threshold search beats the null on performance but not stable location.” [SOURCE] | Actual wage search should exceed null search on out-of-sample performance, while selected-cell concentration should remain low. | Pre-register metrics such as `Δ sign-match share > 0.10` and `Δ median |t| > 0.2`, while top selected cell share `< 0.33` and top-3 share `< 0.60`. |
| “Load/capacity is a robust county stress marker.” [SOURCE] | Direction/sign should survive division leave-out and multiple discretizations. | Same sign in all 9 divisions; coefficient magnitude in each leave-out run stays within `[0.5, 1.5]x` full-sample estimate; monotonicity Spearman `rho > 0` with bootstrap CI above 0 across deciles and ventiles. |
| “Not a binning accident.” [SOURCE] | Results should hold under alternative binnings and continuous forms. | Same-sign association under quintiles, deciles, ventiles, and spline/continuous specification. If not, delete the claim. |
| “Policy relevance remains high.” [SOURCE] | **Not testable as written.** | Must specify policy objective, welfare metric, and counterfactual. Otherwise keep only as `[FRAMING-SENSITIVE] [INFERENCE]` or delete. |

## 4. Constitutional Alignment (Quantified)
| Principle | Coverage | Specific gaps | Suggested fix |
|---|---:|---|---|
| 1. Source everything | **78%** | Major claims are sourced, but some memo lines use bare `[SOURCE]` placeholders rather than citation-grade paths; some semantic claims rely on review artifacts instead of direct outputs. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Replace bare `[SOURCE]` with explicit file citations; when possible cite CSV/JSON directly. |
| 2. Steel-man before criticizing | **82%** | Rival explanations are listed, but not quantified/prioritized. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] | Add a small table: alternative, evidence for, evidence against, still-open discriminator. |
| 3. Distinguish levels of evidence | **88%** | Good descriptive/causal split, but threshold adjectives blur evidence strength. | Add numeric thresholds for “strong,” “moderate,” “poor,” “diffuse.” |
| 4. Disconfirmation is mandatory | **90%** | Strong pass: permutation, pretrend, leave-out, null search. Gap: possible missing state leave-out if that claim is retained. [SOURCE: .model-review/plan-close-context.md] | Either run state leave-out or remove the claim. |
| 5. Name the frame | **84%** | `[FRAMING-SENSITIVE]` is used, but “policy relevance remains high” lacks explicit frame definition. | State whose welfare function / policy objective is being optimized. |
| 6. Quantify when possible | **61%** | Biggest remaining weakness: memo still uses qualitative threshold terms without exposing magnitudes. | Pull exact margins from summary JSON/CSV into memo bullets. |
| 7. Flag instrument bias | **95%** | Explicit instrument note present in both memos. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] | No major fix needed. |

## 5. My Top 5 Recommendations (different from the originals)
1. **What:** Add a `window_registry` artifact and label each derived window as `clean_pre_covid`, `covid_contaminated`, or `post_surge`.  
   **Why:** The final substantive correction is window semantics. Right now that correction lives mainly in prose. Encoding it in outputs reduces future semantic regression risk across every downstream memo/script. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]  
   **How to verify:** Summary JSON should exclude contaminated windows from any field labeled `causal_support`; unit test that `2019–2020` and `2020–2021` cannot populate “clean pretrend” summaries.

2. **What:** Remove “one-state artifact” unless there is an explicit state leave-out result; otherwise add a state leave-out table.  
   **Why:** This is the most concrete remaining overclaim. The visible artifact set clearly supports division leave-out; state leave-out is not visible. [SOURCE: .model-review/plan-close-context.md] [INFERENCE]  
   **How to verify:** Either (a) grep the memo and index: zero occurrences of “one-state artifact,” or (b) add CSV rows for 50-state leave-out with same-sign share and min/max coefficient ratio.

3. **What:** Replace qualitative threshold prose with a four-number scoreboard in the memo.  
   **Why:** “Strongly,” “diffuse,” and “moderate” are supervision-expensive. The script already computes the needed ingredients (`share_sign_matches_train`, median `|t|`, modal share, top-3 share). [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py]  
   **How to verify:** Memo must report: actual wage sign-match share, null sign-match share, actual top-cell share, null top-cell share. Zero adjective-only threshold claims.

4. **What:** Expand panel audit to window-specific usable N and zero-base counts for the exact outcomes used in falsification.  
   **Why:** Current `qcew_row_missing` keyed to `2021` can understate missingness for `2018–2019`, which is now the pivotal clean window. [SOURCE: sources/immigration-causal/scripts/build_county_outcome_panel.py]  
   **How to verify:** Audit JSON contains counts for each logged change used downstream, and these counts match analysis sample-accounting JSON within tolerance `0`.

5. **What:** Add a binning-invariance mini-check, or narrow the language.  
   **Why:** “Not a binning accident” is broader than decile monotonicity plus threshold null. A quick continuous/spline or alternate-binning check closes that gap cheaply. [INFERENCE]  
   **How to verify:** Same-sign result under quintiles, deciles, ventiles, and a continuous spline; if any fail materially, revise wording to the narrower supported claim.

## 6. Where I'm Likely Wrong
- **I am reviewing from excerpts, not the full scripts/CSV outputs.** The apparent “one-state artifact” gap may disappear if `county_capacity_geographic_leaveout.csv` includes state leave-outs not shown here. [INFERENCE]
- **I may be overcautious about wording because the final memo is already substantially downgraded.** Relative to the earlier version, most of the serious causal overclaiming has been fixed. My remaining objections are mostly semantic-hardening and audit-hardening, not wholesale reversal. [INFERENCE]
- **I may overemphasize production-style metadata.** For a personal research repo, machine-readable window labels may feel heavy. I still think they are justified here because the central error corrected in this tranche was a semantics bug, and those recur. [INFERENCE]
- **I cannot verify the threshold-performance magnitudes from the memo alone.** If the actual/null gaps are numerically large in the CSVs, my criticism is about under-reporting the numbers, not about the underlying result. [SOURCE: sources/immigration-causal/scripts/analyze_capacity_falsification.py]
- **LLM-specific bias:** I am prone to favor narrower claims and explicit guardrails after seeing one semantics failure. That can produce useful caution, but it can also overshrink acceptable descriptive conclusions.