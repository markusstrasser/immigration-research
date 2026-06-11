## 1. Logical Inconsistencies

**Steel-man first:** the tranche *did* make the main substantive correction the review packet asked for: the county panel now exposes two clean pre-COVID annual windows (`2017–2018`, `2018–2019`), labels all `2020`-touching windows contaminated/descriptive-only, and the headline memo materially downgrades causal confidence rather than pretending the old result survived unchanged. [SOURCE: `sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json`] [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`]

| Severity | Issue | Formal problem | Evidence |
|---|---:|---|---|
| High | **Archival newcomer memo is internally contradictory** | The file now opens with a corrected supersession note (`20.5x`, ACS `B07001_081E`, descriptive-only), but the body still contains the **old method, old variable, old row count, and old `33x` claim**. A reader citing the body gets a different estimand than the header. That is not just “outdated”; it is a live semantic contradiction. | Supersession note says ACS `B07001_081E`, median `4.49%` vs `0.21%`, `~20.5x`. Body still says ACS `B05005`, “9,120 county-merged rows after one-to-many join,” “Recent FB annual flow,” “Fact 1: native flow is ~33× larger per year.” [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] |
| High | **Current citation graph points to a semantically stale source** | The confidence ladder and index now use the corrected weaker claim, but they point to a file whose internal tables still materially say the old thing. This breaks traceability: the cited source does not cleanly support the citing claim. | Confidence ladder item 22 cites `research/immigration-causal-internal-vs-immigrant-newcomers.md` for the downgraded “order-of-magnitude disparity” claim, but that same file still contains the old `33x` method/result body. [SOURCE: `research/immigration-confidence-ladder.md`] [SOURCE: `research/immigration-INDEX.md`] [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] |
| Medium | **Newcomer script semantics were only partially cleaned** | Code comments/docstrings still describe the old estimand. That makes future memo drift likely because readers will grep the script and see obsolete variable definitions. | Function `fetch_acs_county_population_and_recent_fb()` docstring still says it pulls “recent-arrival FB” and mentions `B05005_002E + B05005_004E`; code actually requests `B01003`, `B05002`, `B25064`, `B19013` only. [SOURCE: `sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py`] |
| Medium | **README output-path contract is stale for this tranche** | README says outputs land in `data/analysis/`, but the falsification tranche’s main artifacts are under `data/outcomes/analysis/`. Reproduction instructions that misstate artifact locations are a semantic failure. | README: “Outputs land in `data/analysis/`”; falsification outputs listed in review target and memo live under `sources/immigration-causal/data/outcomes/analysis/`. [SOURCE: `sources/immigration-causal/README.md`] [SOURCE: review packet touched files] |
| Medium | **Threshold-search confidence is qualitatively downgraded, but not fully quantified** | The memo says wage holdout sign stability “beats the null strongly,” but the design uses only `60` actual splits and `60` null splits. Even with large differences, Monte Carlo precision is limited, and split reuse means nominal binomial CIs are optimistic. The *direction* of the downgrade is right; the *strength* descriptor is under-quantified. | `THRESHOLD_SPLITS = 60`, `THRESHOLD_NULL_SPLITS = 60`; summary reports Wilson interval only for null sign-match share, not for actual-vs-null difference. [SOURCE: `sources/immigration-causal/scripts/analyze_capacity_falsification.py`] [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] |
| Low | **One remaining arithmetic ambiguity in newcomer ratio presentation** | `4.49 / 0.21 = 21.38`, not `20.5`. This may be harmless rounding from unrounded medians, but the memo should state whether the ratio uses rounded or exact medians. | Supersession note gives `4.49%` and `0.21%`, “roughly `20.5x`.” [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] [INFERENCE] |

**What looks formally okay, not buggy:**  
- QCEW window metadata now correctly distinguishes clean pre-COVID windows from contaminated `2020`-touching windows. [SOURCE: `sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json`]  
- Nondisclosure handling does **not** show silent leakage into the 2,390-county analysis sample; all analysis-sample nondisclosure counts are `0`. [SOURCE: `sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json`]  
- The falsification memo’s causal downgrades are directionally aligned with the artifact description in the audit and the review packet. [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] [SOURCE: review packet]

## 2. Cost-Benefit Analysis

Ranked by **value / ongoing drag**, not build time.

| Rank | Proposed change | Expected impact | Maintenance burden | Composability | Risk | Net value |
|---|---|---|---|---|---|---|
| 1 | **Split the newcomer memo into “current” vs “archival provenance appendix”** | Very high: removes the largest live contradiction in the citation layer and stops stale `33x` reuse. [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] | Low | High: helps every later memo cite a single stable estimand | Low | **Very high** |
| 2 | **Add machine-readable metadata to each analysis artifact: universe, time window, unit, comparability warning** | High: prevents semantic drift between IRS `97/000`, ACS `B07001_081E`, and ACS `recent_fb_annual_share`. | Low-medium | Very high: reusable across all topics and memos | Low | **High** |
| 3 | **Export exact threshold-search uncertainty metrics** (actual-null difference, bootstrap/split-seed sensitivity, joint-mode concentration index) | High: converts “beats null strongly” from rhetoric into a measured statement. [SOURCE: `sources/immigration-causal/scripts/analyze_capacity_falsification.py`] | Medium | High: useful for future threshold work | Low-medium | **High** |
| 4 | **Fetch ACS MOEs for `B07001_081E` and filter/flag unreliable counties** | Medium-high: sharpens the newcomer comparison from “descriptive but noisy” to “descriptive with reliability discipline.” | Low | High | Low | **High** |
| 5 | **Add a memo–artifact consistency linter** that checks cited numbers against current parquet/CSV summaries | Medium: prevents future stale-number regressions like `33x`. | Medium | Very high | Medium (false positives if text paraphrases) | **Medium-high** |
| 6 | **Correct README output-path and script docstrings** | Medium: improves reproducibility and lowers future confusion. | Very low | Medium | Low | **Medium-high** |
| 7 | **Increase threshold split counts** beyond `60/60` | Medium: better precision, but ongoing runtime/interpretation burden rises and may not change verdict. | Medium | Medium | Low | **Medium** |

## 3. Testable Predictions

| Claim | Testable prediction | Success criterion | Failure criterion |
|---|---|---|---|
| `flow/capacity is a robust county stress marker` [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | Under alternative random seeds and one additional year-free specification family, the permutation p-value remains at the empirical floor or near-floor and monotonicity remains positive across upper deciles. | Across `>=10` seeds, median empirical p `<=0.005`; decile slope sign positive in `>=9/10` runs. [INFERENCE] | Seed-sensitive sign flips or p-values regularly above `0.05`. |
| `annual county panel does not cleanly identify the wage channel` [SOURCE: same memo] | The two clean presurge wage windows (`2017–2018`, `2018–2019`) should not both show same-sign, similar-magnitude adverse coefficients under the preferred control set. | Opposite signs or materially different magnitudes persist. | Both clean windows become same-sign and similar once specification is stabilized. |
| `employment is more suspicious than wages in annual design` [SOURCE: same memo] | In both clean presurge windows, employment coefficients stay negative under leave-one-division-out and leave-one-state-out. | Negative sign in majority of leave-outs and both clean windows. | Sign becomes unstable or near-zero in most leave-outs. |
| `threshold evidence exists for wages, but stable cutoff location does not` [SOURCE: same memo] | Threshold surface concentration remains diffuse: no single cell dominates selection. | Top cell selection share stays low (e.g., `<0.30`) and top-3 sum modest. [INFERENCE] | One cell becomes dominant across seeds/splits. |
| `domestic newcomer counts are much larger than moved-from-abroad counts` [SOURCE: `research/immigration-confidence-ladder.md`] | After adding ACS MOE filtering, the median county ratio remains order-of-magnitude (`>=10x`) in counties with reliable ACS estimates. | Reliable-county median ratio `>=10`. | Ratio collapses toward low single digits once unreliable counties are removed. |
| `policy relevance remains high` [FRAMING-SENSITIVE] [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | **Not directly testable as stated.** Must be decomposed into measurable claims (effect size, population affected, policy lever elasticity). | N/A | N/A |

## 4. Constitutional Alignment (Quantified)

| Principle | Score | Specific gaps | Suggested fix |
|---|---:|---|---|
| 1. Source everything | **72%** | Major files still contain unsourced narrative blocks and stale internals; newcomer memo header/body contradiction breaks source traceability. [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] | Split archival/current memo; inline-source the corrected quantitative claims from the parquet/CSV itself. |
| 2. Steel-man before criticizing | **84%** | Falsification memo does fairly steel-man the earlier frontier claim before narrowing it. Newcomer memo less so because provenance note is brief, then stale body remains. | Add a one-paragraph “strongest old claim” + “what survives” section to archival/current transitions. |
| 3. Distinguish levels of evidence | **81%** | Mostly good (`descriptive`, `causal`, `provisional`), but “beats null strongly” and “policy relevance high” remain under-quantified. | Add exact effect-size deltas and uncertainty intervals. |
| 4. Disconfirmation is mandatory | **90%** | This tranche is strong here: placebo bug fixed, added `2017` window, null search added. [SOURCE: review packet] | Add ACS reliability disconfirmation for newcomer comparison. |
| 5. Name the frame | **88%** | Good use of `[FRAMING-SENSITIVE]` and instrument notes. Gap: newcomer memo still conflates frame layers in the old body. | Metadata contract for universe/time-window/unit. |
| 6. Quantify when possible | **76%** | Good on windows/counts, weaker on threshold uncertainty and newcomer estimate reliability. | Report actual-null deltas with CIs; fetch ACS MOEs. |
| 7. Flag the instrument’s bias | **93%** | Index and memos explicitly do this. [SOURCE: `research/immigration-INDEX.md`] [SOURCE: `research/immigration-capacity-falsification-2026-04-21.md`] | Keep; no major gap. |

**Overall weighted alignment:** **83/100**. [INFERENCE]

## 5. My Top 5 Recommendations (different from the originals)

1. **Create a clean current newcomer memo and demote the old one to appendix-only provenance.**  
   **Why:** Right now one file simultaneously asserts `20.5x` and `33x`, `B07001_081E` and `B05005`, aggregated county rows and one-to-many merged rows. That is the biggest live semantic bug in the tranche. [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`]  
   **Verify:** zero stale references to `33x`, `B05005`, and “9,120 rows” in any file cited by the index/confidence ladder; all current citations resolve to one estimand.

2. **Attach a “measurement contract” JSON to each output dataset.**  
   **Why:** The repo now uses at least three nearby but non-equivalent constructs: IRS `Total Migration-US`, ACS moved-from-abroad, and ACS recent-foreign-born annualized flow. A machine-readable contract would prevent future memo drift. [SOURCE: `sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py`] [SOURCE: `sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json`]  
   **Verify:** each artifact ships fields for `universe`, `time_window`, `unit`, `entity`, `comparability_warning`; memo linter checks these before publication.

3. **Quantify threshold-search uncertainty, not just null comparison direction.**  
   **Why:** With only `60` actual and `60` null splits, qualitative words like “strongly” are too loose. Export actual-null mean difference, SE across split seeds, and concentration entropy/top-cell share. [SOURCE: `sources/immigration-causal/scripts/analyze_capacity_falsification.py`]  
   **Verify:** summary JSON contains `delta_sign_match`, `delta_abs_t`, split-seed SD, and concentration metrics; memo replaces adverbs with numbers.

4. **Fetch ACS MOEs for `B07001_081E` and publish a reliability-filtered newcomer ratio.**  
   **Why:** This would turn the current comparison from “descriptive but incomparable” into “descriptive, incomparable, and reliability-bounded,” which is a materially stronger epistemic position. [INFERENCE]  
   **Verify:** add `B07001_081M`; compute coefficient of variation or MOE/share thresholds; report ratio for all counties and reliable subset. Stability of median ratio is the pass/fail.

5. **Add a repository-wide stale-claim test that compares memo numerics to current outputs.**  
   **Why:** The `33x` residue is exactly the kind of failure an automated check can catch. Ongoing value is high because this repo updates in bursts and reuses old memos. [SOURCE: review packet git status shows many bursty updates]  
   **Verify:** CI/report flags any memo whose cited number differs from artifact summary beyond tolerance or references retired variable names.

## 6. Where I'm Likely Wrong

1. **I may be overweighting source-hygiene relative to substantive econometric quality.** The biggest visible bug in the packet is semantic drift in the newcomer memo; hidden CSV results may matter more. [INFERENCE]

2. **I may be too cautious on the threshold-search evidence.** If the actual-null gap in holdout sign stability is very large, `60/60` splits may be enough for the repo’s purposes. I cannot verify magnitude from the excerpt alone. [SOURCE: `sources/immigration-causal/scripts/analyze_capacity_falsification.py`] [INFERENCE]

3. **I may be underestimating the value of provenance-in-place.** The current “supersession note + stale body” pattern may have been chosen to preserve history. My recommendation pushes harder toward archival separation than some researchers prefer. [INFERENCE]

4. **I may be over-recommending infrastructure for a personal research repo.** A metadata contract and memo linter are production-style moves. They are justified here only because the repo explicitly values autonomous multi-agent reuse and low supervision cost. [SOURCE: project development context] [INFERENCE]

5. **I may be wrong about the apparent `20.5x` arithmetic mismatch.** The ratio could be computed from unrounded medians, in which case the displayed percentages are rounded summaries, not the exact operands. [SOURCE: `research/immigration-causal-internal-vs-immigrant-newcomers.md`] [INFERENCE]