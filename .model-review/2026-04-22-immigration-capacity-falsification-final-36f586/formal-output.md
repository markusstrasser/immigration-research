## 1. Logical Inconsistencies
| Issue | What I can verify | Why it matters |
|---|---|---|
| **1. County panel audit does not actually audit the new `2018–2020` falsification windows** | `build_county_outcome_panel.py` sets `qcew_row_missing = annual_avg_emplvl_2021.isna()`. That audits only one year/measure, not the newly claimed pretrend windows for `2018`, `2019`, `2020`, nor wages. [SOURCE: `sources/immigration-causal/scripts/build_county_outcome_panel.py`] | A county can pass the audit while still missing one or more inputs needed for the corrected falsification. So the memo’s “explicit sample accounting” language is stronger than the builder-level audit supports. [INFERENCE] |
| **2. “Zero base” audit counts are semantically contaminated by missingness** | In `add_log_change`, `zero_base_flag = panel[base_col].fillna(0) <= 0` and `missing_flag = panel[base_col].isna() \| panel[end_col].isna()`. Missing base values are counted as both `zero_base` and `missing_input`. [SOURCE: `sources/immigration-causal/scripts/build_county_outcome_panel.py`] | This makes `*_zero_base_count` not an actual zero-base count. It is a mixed “zero-or-missing base” count, so any downstream interpretation is formally wrong unless re-labeled. [INFERENCE] |
| **3. Memo claims more window construction than the visible builder shows** | The memo revision says the panel was rebuilt with true `2018–2020` **and `2018–2020 cumulative`** QCEW windows. The visible builder excerpt materializes annual levels and pairwise log changes (`2018_2019`, `2018_2020`, `2019_2020`, etc.), but no explicit cumulative `2018–2020` variable is shown. [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`; SOURCE: `sources/immigration-causal/scripts/build_county_outcome_panel.py`] | This may be fine if the analysis script derives cumulative controls from annual columns later, but as written the provenance chain is incomplete. The memo should either cite that derivation directly or stop claiming the builder materialized cumulative windows. [INFERENCE] |
| **4. Threshold-surface concentration comparison is likely apples-to-oranges** | In `build_summary`, `surface_actual = thresh_surface[thresh_surface["source"] == "actual"]`, while `surface_null = thresh_surface[thresh_surface["source"] == "null_search"]`. The null search is explicitly wage-only (`threshold_null_wage_only`), but `surface_actual` is not filtered to wage before comparing `actual_modal_share`/`actual_top3_share` to null. [SOURCE: `sources/immigration-causal/scripts/analyze_capacity_falsification.py`] | If `thresh_surface` contains actual surfaces for multiple outcomes, the memo’s “actual vs null cutoff diffuseness” comparison is not formally identified. Pooling wage+employment+margin actual cells against wage-only null would mechanically flatten actual concentration. [INFERENCE] |
| **5. Spatial robustness wording may outrun the demonstrated leave-out design** | The memo says the signal is “not a one-state or one-division artifact.” The review target emphasized **division leave-out** as the correction, and the visible materials only clearly mention division leave-out. I cannot verify a state leave-out design from the excerpts. [SOURCE: `.model-review/plan-close-context.md`; SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | Unless `county_capacity_geographic_leaveout.csv` includes leave-one-state-out rows, “not a one-state artifact” is too strong. Division leave-out and state leave-out answer different questions. [UNVERIFIED] |
| **6. Remaining bare `[SOURCE]` placeholders are constitution-level citation bugs** | The corrected memo still contains several claims with bare `[SOURCE]` and no path/citation, including the updated claim list and “What now survives.” The reasoning-evolution memo also contains a few unsupported `[SOURCE]` placeholders. [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`; SOURCE: `research/immigration-reasoning-evolution-2026-04-21.md`] | This directly violates “Source everything.” It also makes several key claims non-auditable. [SOURCE: Constitution in prompt] |
| **7. Review artifact is being used as empirical evidence, not just provenance** | The memo cites `.model-review/.../verified-disposition.md` to support substantive statements about the earlier placebo bug and the corrected interpretation. [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | That file is appropriate for correction history, but weaker as the primary support for empirical claims. The empirical support should point to CSV/JSON outputs or code paths. [INFERENCE] |

## 2. Cost-Benefit Analysis
| Rank | Proposed change | Expected impact | Ongoing burden | Composability | Risk if not done | Value / drag |
|---|---|---:|---:|---:|---:|---:|
| 1 | **Replace single-field QCEW audit with window-by-outcome coverage matrix** | High: catches silent failures in exactly the corrected falsification windows. [INFERENCE] | Low | High | High | **Very high** |
| 2 | **Fix threshold-surface summary to compare wage actual vs wage null only, plus entropy/top-k metrics** | High: directly affects one of the memo’s main downgraded claims. [INFERENCE] | Low-Med | High | High | **Very high** |
| 3 | **Tighten spatial wording unless state leave-out is actually exported** | Medium-High: removes overclaim risk in headline robustness language. [INFERENCE] | Very low | High | Medium | **High** |
| 4 | **Backfill all bare `[SOURCE]` placeholders with direct artifact citations** | Medium: improves auditability and constitutional compliance. [SOURCE: Constitution] | Low | High | Medium | **High** |
| 5 | **Separate empirical citations from correction-history citations** | Medium: improves provenance hygiene. | Very low | High | Medium | **High** |
| 6 | **Relabel or recompute `zero_base_count` to exclude missing bases** | Medium: cleans audit semantics. | Very low | High | Low-Med | **High** |
| 7 | **Add memo/output consistency checks (claim-check script)** | Medium: prevents future narrative drift. | Medium | Medium-High | Medium | **Moderate-High** |

## 3. Testable Predictions
| Claim | Make it testable how? | Success criterion | If not met |
|---|---|---|---|
| **“Wage pretrends are mostly weak before `2020`.”** [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | In `county_capacity_pretrend_results.csv`, filter wage outcomes for true presurge windows only (`2018–2019`, `2019–2020`, optionally `2018–2020`). | At least 2 of 3 core wage pretrend specs have `p >= 0.05` and the same-sign effect is materially smaller than the post `2023–2024` effect. [INFERENCE] | Memo should downgrade “mostly weak” to “mixed” or quantify exact windows. |
| **“Employment is more confounded by preexisting weakness.”** [SOURCE: same memo] | Compare employment pretrend coefficients and post coefficients with/without presurge controls. | Employment shows negative presurge coefficients in both early windows or larger attenuation from baseline to controlled post spec than wages. [INFERENCE] | The wage/employment asymmetry is overstated. |
| **“Stress marker beats random reassignment.”** [SOURCE: same memo] | In permutation output, verify empirical p-values for the main statistic under the stated permutation scheme. | Main descriptive statistic has empirical `p <= 0.001` with `1,000` draws, and the test statistic exceeds all or nearly all permutations. [INFERENCE] | Memo should report exact rank/floor, not “beats permutations” generically. |
| **“Threshold surface is diffuse.”** [SOURCE: same memo] | Compute concentration metrics on the threshold surface: modal share, top-3 share, entropy, Herfindahl. Do this **within outcome**. | For wage actual, concentration is low in absolute terms and not materially higher than wage null; e.g., `actual_top3_share - null_top3_share <= 0.05` or entropy ratio near 1. [INFERENCE] | “Diffuse” needs narrowing or quantification. |
| **“Not a one-state artifact.”** [SOURCE: same memo] | Require leave-one-state-out output, not just division leave-out. | Sign preserved in >=90% of state leave-outs and median beta remains within 20% of full-sample beta. [INFERENCE] | Remove “one-state” wording. |
| **“Policy relevance remains high.”** [FRAMING-SENSITIVE] [SOURCE: same memo] | Not directly testable from this tranche. | **Flag as non-testable normative framing from current outputs.** | Keep only as `[FRAMING-SENSITIVE] [INFERENCE]`, not as an empirical conclusion. |

## 4. Constitutional Alignment (Quantified)
| Principle | Coverage | Specific gaps | Suggested fix |
|---|---:|---|---|
| **1. Source everything** | **62%** | Bare `[SOURCE]` placeholders remain; some empirical claims cite review artifacts rather than primary outputs. [SOURCE: memos] | Replace every bare placeholder with file path(s); move `.model-review` cites to correction-history sentences only. |
| **2. Steel-man before criticizing** | **82%** | Rival explanations are listed clearly, but not always tied to explicit discriminating evidence thresholds. [SOURCE: falsification memo] | Add “what evidence would make rival explanation win?” bullets. |
| **3. Distinguish levels of evidence** | **86%** | Good use of `[SOURCE]` vs `[INFERENCE]`, but a few empirical-sounding sentences rely on narrative review artifacts. | Tighten citation provenance. |
| **4. Disconfirmation is mandatory** | **91%** | Strong falsification/permutation/placebo effort. Main gap is audit incompleteness for the corrected windows. [SOURCE: code + memo] | Add window-specific sample accounting and state-vs-division robustness separation. |
| **5. Name the frame** | **88%** | `[FRAMING-SENSITIVE]` appears where needed, but “policy relevance remains high” could still be read as stronger than the evidence tier warrants. | Keep it explicitly separate from empirical bottom line. |
| **6. Quantify when possible** | **74%** | “Diffuse cutoff surface,” “mostly weak,” and “moderate transfer” are not yet pinned to formal thresholds. | Add explicit numeric rules in summary JSON and memo. |
| **7. Flag the instrument’s bias** | **95%** | Present and appropriately scoped. | No major change needed. |

## 5. My Top 5 Recommendations (different from the originals)
1. **What:** Add a **window-by-outcome coverage audit** to `county_outcome_panel_audit.json`.  
   **Why:** The current audit can miss exactly the falsification inputs it claims to secure. Count nonmissing rows for wage/employment for each of `2018`, `2019`, `2020`, `2021`, `2023`, `2024`, plus each derived log-change window. That directly reduces silent semantic failure risk in the corrected tranche. [SOURCE: `build_county_outcome_panel.py`]  
   **How to verify:** Audit file must contain per-window counts; memo sample counts must match those values exactly.

2. **What:** Recompute threshold-surface concentration metrics **within outcome**, and compare **wage actual vs wage null** only.  
   **Why:** The current summary likely pools actual surfaces across outcomes while null is wage-only, which can bias the “diffuse vs null” interpretation. [SOURCE: `analyze_capacity_falsification.py`]  
   **How to verify:** Summary JSON should report outcome-specific `modal_share`, `top3_share`, entropy, and Herfindahl. Wage actual/null comparisons should use the same outcome filter.

3. **What:** Either add an explicit **leave-one-state-out** table or delete “not a one-state artifact.”  
   **Why:** Division robustness is not state robustness. This is a high-visibility wording risk with low maintenance cost to fix. [SOURCE: memo + review scope]  
   **How to verify:** `county_capacity_geographic_leaveout.csv` includes a `unit_type` column with both `state` and `division`, or the memo drops the state claim.

4. **What:** Run a **citation scrub** that fails on any bare `[SOURCE]`.  
   **Why:** Unsourced claims are constitutionally disallowed and are still present in both final memos. [SOURCE: Constitution; SOURCE: memos]  
   **How to verify:** Zero regex matches for `\[SOURCE\](?!:)` or similar bare tags; every empirical sentence links to a path or output file.

5. **What:** Add a lightweight **memo-to-output consistency checker**.  
   **Why:** The main remaining risks are narrative drift and semantic overstatement, not compute. A checker that asserts cited numbers/phrases exist in exported JSON/CSV will pay for itself across future tranches. [INFERENCE]  
   **How to verify:** CI-style script passes only if memo claims on permutation count, leave-out unit, threshold null scope, and sample counts all match machine-readable outputs.

## 6. Where I'm Likely Wrong
- I may be **overstating the threshold-surface apples-to-oranges bug** if `threshold_surface()` already encodes outcome-specific rows and the visible summary excerpt just hides an additional filter. [UNVERIFIED]
- I may be **too skeptical about the “one-state artifact” wording** if `county_capacity_geographic_leaveout.csv` does in fact contain leave-one-state-out estimates not shown in the packet. [UNVERIFIED]
- I may be **wrong about the cumulative-window provenance gap** if `analyze_capacity_falsification.py` constructs cumulative presurge controls from the annual QCEW columns downstream; the visible builder excerpt alone does not settle that. [UNVERIFIED]
- My bias here is toward **scope-limiting when provenance is imperfect**. That can under-credit a basically correct result whose implementation is stronger than its memo citation hygiene.
- I also have the standard LLM failure mode of **inferring too much from partial excerpts**. Where I flagged `[UNVERIFIED]`, I am explicitly not claiming the bug is proven—only that the current visible chain is insufficient for the memo’s wording.